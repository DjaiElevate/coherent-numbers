"""Trade-level field-modulated identity scoping study — locked protocol.

Implements docs/influential_numbers_field_modulated_identity_trade_level_scoping_study_v0.1.md
(LOCK-ACCEPTED 2026-05-16, committed 8d4bd1d) and its lock-acceptance memo.

This is a CV-only pre-registered SCOPING STUDY, not the coordinate-axis cell
and not a full registered charter cell. Result-defining logic lives entirely
in this module. It contains NO real-data path: every entry point takes an
in-memory pandas DataFrame supplied by the caller. The synthetic conformance
harness in scripts/ is the only thing wired to call it, and it builds a
synthetic frame. Contacting the frozen substrate is a separately gated step
that is intentionally NOT implemented here.

Pure numpy/pandas; ridge is the closed-form penalised normal equation (no
sklearn dependency, fully deterministic). Memo section letters are cited inline.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

# ── Locked constants (memo §G/§H/§I/§P) ──────────────────────────────────────

MASTER_SEED: int = 20260516                       # §P-7
ALPHA_GRID: np.ndarray = np.logspace(-3, 3, 13)   # §I-B3, §P-3
N_OUTER_SPLITS: int = 5                            # §I, §P-8
N_INNER_SPLITS: int = 5                            # §I-B3
PRIMARY_N: int = 20                                # §G
SUPPLEMENTARY_NS: Tuple[int, int] = (10, 40)       # §G
MIN_VAL_BLOCK_ROWS: int = 50                       # §P-6 degeneracy guard
ASSET_LEVELS: Tuple[str, ...] = ("SPY", "EFA", "EEM", "GLD", "TLT")  # §F
DOW_LEVELS: Tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6)                  # §F (Mon..Sun)
MONTH_LEVELS: Tuple[int, ...] = tuple(range(1, 13))                  # §F

# §H/§P-5 interaction identity columns (exactly these 3) and §G context (7).
IDENTITY_INTERACTION_COLS: Tuple[str, ...] = (
    "direction", "initial_risk", "log_entry_price",
)
CONTEXT_COLS: Tuple[str, ...] = (
    "ctx_time_since_prior_trade",
    "ctx_recent_mean_R",
    "ctx_recent_win_rate",
    "ctx_recent_std_R",
    "ctx_recent_longshort_imbalance",
    "ctx_recent_trade_frequency",
    "ctx_recent_mean_abs_R",
)
N_CONTEXT: int = len(CONTEXT_COLS)                       # 7
N_INTERACTIONS: int = len(IDENTITY_INTERACTION_COLS) * N_CONTEXT  # 21 (§H/§P-5)

REQUIRED_INPUT_COLUMNS: Tuple[str, ...] = (
    "asset", "entry_date", "setup_date", "direction", "entry_price",
    "exit_price", "exit_date", "exit_reason", "bars_held", "r_multiple",
    "first_target_hit", "initial_risk",
)
# §E/§D leakage exclusions — never used as predictive features.
LEAKAGE_COLUMNS: Tuple[str, ...] = (
    "exit_reason", "exit_date", "exit_price", "bars_held",
    "first_target_hit", "r_multiple",
)

MODELS: Tuple[str, ...] = ("M0", "M1", "M1L", "M2", "M3a", "M3b")
COMPARATORS: Tuple[str, ...] = ("M1L", "M3a", "M3b")  # §I primary success set

ABS_MARGIN: float = 0.01      # §I locked absolute OOS-R² margin
REL_MARGIN: float = 0.20      # §I locked 20% relative margin
FOLD_WIN_MIN: int = 4         # §I "at least 4 of 5 folds"


# ── Input validation / canonical pooled ordering (§G) ────────────────────────

def _to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="raise")


def canonical_pooled_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Validate schema and return the LOCKED pooled stream ordered by entry_date.

    §G: "a single pooled stream ordered by entry_date". Ties are broken
    deterministically by (entry_date, asset, original input order) so the
    stream is a pure function of the input — this tie-break does not change
    the locked design, it only makes "ordered by entry_date" reproducible.
    """
    missing = [c for c in REQUIRED_INPUT_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("input frame missing required columns: %s" % missing)
    work = df.copy().reset_index(drop=True)
    work["_input_order"] = np.arange(len(work), dtype=np.int64)
    work["entry_date"] = _to_datetime(work["entry_date"])
    work["exit_date"] = _to_datetime(work["exit_date"])
    work["_asset_rank"] = work["asset"].map(
        {a: i for i, a in enumerate(ASSET_LEVELS)}
    )
    if work["_asset_rank"].isna().any():
        bad = sorted(set(work.loc[work["_asset_rank"].isna(), "asset"]))
        raise ValueError("unknown asset label(s): %s" % bad)
    work = work.sort_values(
        ["entry_date", "_asset_rank", "_input_order"], kind="mergesort"
    ).reset_index(drop=True)
    return work


# ── Context features (§G) — leakage-safe, computed on the pooled stream ───────

def _resolved_prior_mask(entry_dates: np.ndarray, exit_dates: np.ndarray,
                         i: int) -> np.ndarray:
    """Indices < i whose exit_date is strictly before focal entry_date (§G)."""
    focal_entry = entry_dates[i]
    return np.where(exit_dates[:i] < focal_entry)[0]


def build_context_block(frame: pd.DataFrame, n_window: int) -> pd.DataFrame:
    """The 7 LOCKED context features (§G), using only pre-entry information.

    Outcome-bearing features use the most recent ``n_window`` *resolved*
    prior trades (exit_date strictly before focal entry_date). Entry-time
    features use the most recent ``n_window`` prior trades by stream position.
    Where a window is empty the feature is NaN; such rows are dropped by
    ``_finite_row_mask`` (a well-definedness exclusion analogous to the
    spec's "exclude if unavailable", reported in diagnostics — not a new lock).
    """
    entry_dates = frame["entry_date"].values.astype("datetime64[ns]")
    exit_dates = frame["exit_date"].values.astype("datetime64[ns]")
    r = frame["r_multiple"].values.astype(np.float64)
    is_long = (frame["direction"].astype(str).str.lower() == "long").values
    n = len(frame)

    cols: Dict[str, np.ndarray] = {c: np.full(n, np.nan) for c in CONTEXT_COLS}
    one_day = np.timedelta64(1, "D")

    for i in range(n):
        # entry-time window: most recent n_window prior by stream position
        lo = max(0, i - n_window)
        ent_idx = np.arange(lo, i)
        if ent_idx.size > 0:
            prev_entry = entry_dates[i - 1]
            cols["ctx_time_since_prior_trade"][i] = (
                (entry_dates[i] - prev_entry) / one_day
            )
            long_w = is_long[ent_idx]
            cols["ctx_recent_longshort_imbalance"][i] = (
                (long_w.sum() - (~long_w).sum()) / ent_idx.size
            )
            span_days = (entry_dates[i - 1] - entry_dates[lo]) / one_day
            span_days = float(span_days)
            cols["ctx_recent_trade_frequency"][i] = (
                ent_idx.size / span_days if span_days > 0.0 else float(ent_idx.size)
            )
        # resolved (outcome) window: most recent n_window resolved prior
        res_all = _resolved_prior_mask(entry_dates, exit_dates, i)
        if res_all.size > 0:
            res_idx = res_all[-n_window:]
            rr = r[res_idx]
            cols["ctx_recent_mean_R"][i] = rr.mean()
            cols["ctx_recent_win_rate"][i] = (rr > 0.0).mean()
            cols["ctx_recent_std_R"][i] = rr.std(ddof=0) if rr.size >= 2 else 0.0
            cols["ctx_recent_mean_abs_R"][i] = np.abs(rr).mean()

    return pd.DataFrame(cols, index=frame.index)


# ── Identity / expanded-identity design blocks (§E/§F/§H) ────────────────────

def _dummy_matrix(values: Sequence[Any], levels: Sequence[Any]
                  ) -> Tuple[np.ndarray, List[str], Any]:
    """Fixed-category indicator contrasts, drop-first (collinearity-safe).

    Category set is fixed (not data-derived) so column structure is identical
    across folds and across M2/M3a/M3b — required by the pooled-residual
    concatenation (§I-B1) and the equal-structure control rule (§H).
    """
    levels = list(levels)
    drop = levels[0]
    keep = levels[1:]
    v = np.asarray(values)
    mat = np.zeros((len(v), len(keep)), dtype=np.float64)
    for j, lv in enumerate(keep):
        mat[:, j] = (v == lv).astype(np.float64)
    names = ["%s" % str(k) for k in keep]
    return mat, names, drop  # type: ignore[return-value]


def base_feature_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Raw (pre-standardisation) identity + expanded-identity columns (§E/§F).

    M1 identity = {direction, initial_risk, log_entry_price}. Calendar content
    of M1 is empty by lock (§E/§F); calendar + asset enter only at M1L.
    """
    out = pd.DataFrame(index=frame.index)
    out["direction"] = (
        frame["direction"].astype(str).str.lower() == "long"
    ).astype(np.float64)                                   # dummy (not z-scored)
    out["initial_risk"] = frame["initial_risk"].astype(np.float64)
    out["log_entry_price"] = np.log(frame["entry_price"].astype(np.float64))
    out["_asset"] = frame["asset"].astype(str).values
    ed = frame["entry_date"]
    out["_dow"] = ed.dt.weekday.values
    out["_month"] = ed.dt.month.values
    return out


# ── Standardisation (train-fold only; §E/§H/§I) ──────────────────────────────

@dataclasses.dataclass
class Scaler:
    mean: float
    std: float

    @staticmethod
    def fit(x: np.ndarray) -> "Scaler":
        m = float(np.mean(x))
        s = float(np.std(x, ddof=0))
        return Scaler(m, s if s > 0.0 else 1.0)  # std==0 -> 1.0 (deterministic)

    def transform(self, x: np.ndarray) -> np.ndarray:
        return (x - self.mean) / self.std


def _fit_within_asset_logep(train_assets: np.ndarray,
                            train_logep: np.ndarray) -> Dict[str, Scaler]:
    """log(entry_price) standardised WITHIN asset on train-fold stats (§E)."""
    scalers: Dict[str, Scaler] = {}
    for a in ASSET_LEVELS:
        m = train_assets == a
        scalers[a] = Scaler.fit(train_logep[m]) if m.any() else Scaler(0.0, 1.0)
    return scalers


# ── Ridge (closed form, intercept unpenalised) ───────────────────────────────

def ridge_fit_predict(x_tr: np.ndarray, y_tr: np.ndarray,
                      x_va: np.ndarray, alpha: float) -> np.ndarray:
    """Centre-then-solve ridge: w=(XᵀX+αI)⁻¹Xᵀy on centred data; intercept
    recovered from train means so it is never penalised. Deterministic."""
    xm = x_tr.mean(axis=0)
    ym = float(y_tr.mean())
    xc = x_tr - xm
    yc = y_tr - ym
    p = xc.shape[1]
    a = xc.T @ xc + alpha * np.eye(p)
    b = xc.T @ yc
    w = np.linalg.solve(a, b)
    return (x_va - xm) @ w + ym


def _forward_chaining_splits(n: int, n_splits: int
                             ) -> List[Tuple[np.ndarray, np.ndarray]]:
    """Expanding-window forward-chaining splits (§I). Block size = n//(k+1);
    fold j (1..k): train=[0,j*bs), val=[j*bs,(j+1)*bs); remainder appended to
    the final validation block so no time-ordered rows are wasted."""
    if n < (n_splits + 1):
        return []
    bs = n // (n_splits + 1)
    splits: List[Tuple[np.ndarray, np.ndarray]] = []
    for j in range(1, n_splits + 1):
        tr_end = j * bs
        va_start = j * bs
        va_end = n if j == n_splits else (j + 1) * bs
        splits.append((np.arange(0, tr_end), np.arange(va_start, va_end)))
    return splits


# ── Model design-matrix assembly (§H) ────────────────────────────────────────

def _standardise_continuous(train_raw: Dict[str, np.ndarray],
                            va_raw: Dict[str, np.ndarray],
                            names: Sequence[str]
                            ) -> Tuple[np.ndarray, np.ndarray]:
    tr_cols, va_cols = [], []
    for nm in names:
        sc = Scaler.fit(train_raw[nm])
        tr_cols.append(sc.transform(train_raw[nm]))
        va_cols.append(sc.transform(va_raw[nm]))
    if not names:
        return (np.empty((len(next(iter(train_raw.values()))), 0)),
                np.empty((len(next(iter(va_raw.values()))), 0)))
    return np.column_stack(tr_cols), np.column_stack(va_cols)


def _interactions(identity_z: np.ndarray, context_z: np.ndarray) -> np.ndarray:
    """21 = 3 identity × 7 context products (§H/§P-5), column order fixed."""
    blocks = []
    for k in range(identity_z.shape[1]):
        blocks.append(identity_z[:, [k]] * context_z)
    return np.column_stack(blocks)


def _assemble(frame: pd.DataFrame, base: pd.DataFrame, ctx: pd.DataFrame,
              tr_idx: np.ndarray, va_idx: np.ndarray, model: str,
              rng_seed: int) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """Return {model: (X_train, X_val)} feature matrices for one model.

    Standardisation is fit on the training rows only (§E/§H/§I). Asset/calendar
    are fixed-category drop-first dummies (unstandardised). M3a permutes the
    raw context block jointly within train and (independently) within val; M3b
    replaces it with N(0,1) draws. Interactions are always recomputed from the
    context actually used, so M2/M3a/M3b share identical 21-term structure.
    """
    a_tr = base["_asset"].values[tr_idx]
    a_va = base["_asset"].values[va_idx]
    logep = base["log_entry_price"].values
    ws = _fit_within_asset_logep(a_tr, logep[tr_idx])
    logep_tr = np.array([ws[a].transform(np.array([logep[i]]))[0]
                         for a, i in zip(a_tr, tr_idx)])
    logep_va = np.array([ws[a].transform(np.array([logep[i]]))[0]
                         for a, i in zip(a_va, va_idx)])

    ir = base["initial_risk"].values
    dir_tr = base["direction"].values[tr_idx]
    dir_va = base["direction"].values[va_idx]

    # identity continuous standardised on train: initial_risk; logep already z.
    ir_sc = Scaler.fit(ir[tr_idx])
    ident_tr = np.column_stack(
        [dir_tr, ir_sc.transform(ir[tr_idx]), logep_tr])
    ident_va = np.column_stack(
        [dir_va, ir_sc.transform(ir[va_idx]), logep_va])
    ident_names = ["direction", "initial_risk", "log_entry_price"]

    # expanded identity dummies (fixed categories, drop-first)
    asset_tr, _, _ = _dummy_matrix(a_tr, ASSET_LEVELS)
    asset_va, _, _ = _dummy_matrix(a_va, ASSET_LEVELS)
    dow_tr, _, _ = _dummy_matrix(base["_dow"].values[tr_idx], DOW_LEVELS)
    dow_va, _, _ = _dummy_matrix(base["_dow"].values[va_idx], DOW_LEVELS)
    mon_tr, _, _ = _dummy_matrix(base["_month"].values[tr_idx], MONTH_LEVELS)
    mon_va, _, _ = _dummy_matrix(base["_month"].values[va_idx], MONTH_LEVELS)
    expanded_tr = np.column_stack([asset_tr, dow_tr, mon_tr])
    expanded_va = np.column_stack([asset_va, dow_va, mon_va])

    if model == "M1":
        return {"tr": ident_tr, "va": ident_va}
    if model == "M1L":
        return {"tr": np.column_stack([ident_tr, expanded_tr]),
                "va": np.column_stack([ident_va, expanded_va])}

    # context for M2/M3a/M3b
    ctx_raw_tr = ctx.values[tr_idx]
    ctx_raw_va = ctx.values[va_idx]
    if model == "M3a":  # §I-B4 joint row-permutation, train & val independent
        rs_tr = np.random.RandomState(rng_seed)
        rs_va = np.random.RandomState(rng_seed + 500)
        ctx_raw_tr = ctx_raw_tr[rs_tr.permutation(len(tr_idx))]
        ctx_raw_va = ctx_raw_va[rs_va.permutation(len(va_idx))]
    elif model == "M3b":  # §I-B5 i.i.d. N(0,1), post-standardisation scale
        rs_tr = np.random.RandomState(rng_seed + 1000)
        rs_va = np.random.RandomState(rng_seed + 1500)
        ctx_z_tr = rs_tr.standard_normal((len(tr_idx), N_CONTEXT))
        ctx_z_va = rs_va.standard_normal((len(va_idx), N_CONTEXT))
        inter_tr = _interactions(ident_tr, ctx_z_tr)
        inter_va = _interactions(ident_va, ctx_z_va)
        return {
            "tr": np.column_stack([ident_tr, expanded_tr, ctx_z_tr, inter_tr]),
            "va": np.column_stack([ident_va, expanded_va, ctx_z_va, inter_va]),
        }

    # M2 (and M3a continues here with permuted raw context) — standardise
    # context on train stats, then recompute interactions.
    ctx_tr_raw_d = {CONTEXT_COLS[j]: ctx_raw_tr[:, j] for j in range(N_CONTEXT)}
    ctx_va_raw_d = {CONTEXT_COLS[j]: ctx_raw_va[:, j] for j in range(N_CONTEXT)}
    ctx_z_tr, ctx_z_va = _standardise_continuous(
        ctx_tr_raw_d, ctx_va_raw_d, CONTEXT_COLS)
    inter_tr = _interactions(ident_tr, ctx_z_tr)
    inter_va = _interactions(ident_va, ctx_z_va)
    return {
        "tr": np.column_stack([ident_tr, expanded_tr, ctx_z_tr, inter_tr]),
        "va": np.column_stack([ident_va, expanded_va, ctx_z_va, inter_va]),
    }


# ── Nested-CV alpha selection (§I-B3) ────────────────────────────────────────

def _select_alpha(x_tr: np.ndarray, y_tr: np.ndarray) -> float:
    inner = _forward_chaining_splits(len(x_tr), N_INNER_SPLITS)
    if not inner:
        return float(ALPHA_GRID[len(ALPHA_GRID) // 2])
    sse = np.zeros(len(ALPHA_GRID))
    for ai, alpha in enumerate(ALPHA_GRID):
        tot = 0.0
        for itr, iva in inner:
            pred = ridge_fit_predict(x_tr[itr], y_tr[itr], x_tr[iva], alpha)
            tot += float(np.sum((y_tr[iva] - pred) ** 2))
        sse[ai] = tot
    return float(ALPHA_GRID[int(np.argmin(sse))])  # ties -> smallest alpha


# ── Per-fold purge (§I embargo) ──────────────────────────────────────────────

def _purge_train(frame: pd.DataFrame, sample_pos: np.ndarray,
                 tr_idx: np.ndarray, va_idx: np.ndarray) -> np.ndarray:
    """Drop train trades whose exit_date >= first val entry_date (§I)."""
    ed = frame["entry_date"].values.astype("datetime64[ns]")
    xd = frame["exit_date"].values.astype("datetime64[ns]")
    first_val_entry = ed[sample_pos[va_idx]].min()
    keep = xd[sample_pos[tr_idx]] < first_val_entry
    return tr_idx[keep]


# ── Verdict logic (§I) ───────────────────────────────────────────────────────

def _pooled_r2(y_true: np.ndarray, y_pred: np.ndarray,
               y_m0: np.ndarray) -> float:
    ss_res = float(np.sum((y_true - y_pred) ** 2))
    ss_m0 = float(np.sum((y_true - y_m0) ** 2))
    return 1.0 - ss_res / ss_m0 if ss_m0 > 0.0 else 0.0


def _beats_aggregate(m2: float, comp: float) -> bool:
    """M2 beats comparator by max(0.01 absolute, 20% relative) (§I).

    Relative margin = 0.20*comp only when comp>0; otherwise the relative term
    is undefined and the absolute 0.01 floor governs. This is the natural
    reading of "beat by max(absolute, relative)"; flagged in the conformance
    artifact as an operationalisation of the locked text.
    """
    rel = REL_MARGIN * comp if comp > 0.0 else 0.0
    required = max(ABS_MARGIN, rel)
    return (m2 - comp) >= required


def _classify(agg: Dict[str, float],
              fold_r2: Dict[str, List[float]],
              degenerate: bool) -> Dict[str, Any]:
    if degenerate:
        return {"interpretation": "iv_non_confirmatory_degenerate",
                "primary_success": False}
    fold_wins = {c: sum(1 for f in range(len(fold_r2["M2"]))
                        if fold_r2["M2"][f] > fold_r2[c][f])
                 for c in COMPARATORS}
    agg_beat = {c: _beats_aggregate(agg["M2"], agg[c]) for c in COMPARATORS}
    success = (all(agg_beat.values())
               and all(fold_wins[c] >= FOLD_WIN_MIN for c in COMPARATORS))
    if success:
        interp = "i_field_modulated_supported"
    elif agg["M1L"] > agg["M1"]:
        interp = "ii_expanded_identity_only"
    else:
        interp = "iii_no_field_evidence"
    return {"interpretation": interp, "primary_success": bool(success),
            "fold_wins": fold_wins, "aggregate_beat": agg_beat}


# ── Top-level protocol entry point ───────────────────────────────────────────

def run_protocol(df: pd.DataFrame, n_window: int = PRIMARY_N,
                 master_seed: int = MASTER_SEED) -> Dict[str, Any]:
    """Run the locked scoping protocol on an IN-MEMORY frame for one window N.

    No file or network I/O; ``df`` is supplied by the caller. Returns the
    full result dict (aggregate + fold-level OOS R², verdict, diagnostics).
    """
    frame = canonical_pooled_frame(df)
    # §G warmup exclusion: drop the first n_window trades of the pooled stream.
    warmup_dropped = int(min(n_window, len(frame)))
    post_warmup = frame.iloc[warmup_dropped:].reset_index(drop=True)

    ctx = build_context_block(frame, n_window).iloc[warmup_dropped:] \
        .reset_index(drop=True)
    base = base_feature_frame(post_warmup)
    y = np.log1p(np.abs(post_warmup["r_multiple"].values.astype(np.float64)))

    finite = np.all(np.isfinite(ctx.values), axis=1) & np.isfinite(y)
    n_dropped_undef = int((~finite).sum())
    sample = post_warmup[finite].reset_index(drop=True)
    ctx = ctx[finite].reset_index(drop=True)
    base = base[finite].reset_index(drop=True)
    y = y[finite]
    sample_pos = np.arange(len(sample))

    splits = _forward_chaining_splits(len(sample), N_OUTER_SPLITS)
    degenerate = (len(splits) != N_OUTER_SPLITS)

    oof: Dict[str, np.ndarray] = {m: np.full(len(sample), np.nan)
                                  for m in MODELS}
    fold_r2: Dict[str, List[float]] = {m: [] for m in MODELS}
    fold_meta: List[Dict[str, Any]] = []

    for fi, (tr_idx0, va_idx) in enumerate(splits):
        tr_idx = _purge_train(sample, sample_pos, tr_idx0, va_idx)
        if len(va_idx) < MIN_VAL_BLOCK_ROWS or len(tr_idx) < (N_INNER_SPLITS + 1):
            degenerate = True
        fold_meta.append({"fold": fi + 1, "n_train_pre_purge": int(len(tr_idx0)),
                          "n_train_post_purge": int(len(tr_idx)),
                          "n_val": int(len(va_idx))})
        if degenerate:
            continue
        y_tr, y_va = y[tr_idx], y[va_idx]
        m0_pred = np.full(len(va_idx), float(y_tr.mean()))
        oof["M0"][va_idx] = m0_pred
        fold_r2["M0"].append(_pooled_r2(y_va, m0_pred, m0_pred))
        seed = master_seed + fi  # documented per-fold offset (§I-B4/B5, §P-7)
        for m in ("M1", "M1L", "M2", "M3a", "M3b"):
            mats = _assemble(sample, base, ctx, tr_idx, va_idx, m, seed)
            alpha = _select_alpha(mats["tr"], y_tr)
            pred = ridge_fit_predict(mats["tr"], y_tr, mats["va"], alpha)
            oof[m][va_idx] = pred
            fold_r2[m].append(_pooled_r2(y_va, pred, m0_pred))

    if degenerate:
        verdict = {"interpretation": "iv_non_confirmatory_degenerate",
                   "primary_success": False}
        agg = {m: float("nan") for m in MODELS}
    else:
        mask = ~np.isnan(oof["M0"])
        y_obs = y[mask]
        m0_obs = oof["M0"][mask]
        agg = {m: _pooled_r2(y_obs, oof[m][mask], m0_obs) for m in MODELS}
        verdict = _classify(agg, fold_r2, degenerate=False)

    return {
        "n_window": int(n_window),
        "is_primary": bool(n_window == PRIMARY_N),
        "master_seed": int(master_seed),
        "alpha_grid": [float(a) for a in ALPHA_GRID],
        "n_input_rows": int(len(df)),
        "n_warmup_dropped": warmup_dropped,
        "n_undefined_window_dropped": n_dropped_undef,
        "n_modeling_rows": int(len(sample)),
        "n_interactions": N_INTERACTIONS,
        "context_cols": list(CONTEXT_COLS),
        "models": list(MODELS),
        "aggregate_oos_r2": agg,
        "fold_oos_r2": {m: [float(v) for v in fold_r2[m]] for m in MODELS},
        "fold_meta": fold_meta,
        "degenerate": bool(degenerate),
        "verdict": verdict,
    }


def run_full_study(df: pd.DataFrame,
                   master_seed: int = MASTER_SEED) -> Dict[str, Any]:
    """Primary N=20 plus supplementary N=10/40 (§G). Supplementary results are
    explicitly marked non-primary and cannot rescue a failed primary (§G/§N)."""
    primary = run_protocol(df, PRIMARY_N, master_seed)
    supplementary = {
        "N=%d" % n: run_protocol(df, n, master_seed)
        for n in SUPPLEMENTARY_NS
    }
    return {"primary_N20": primary, "supplementary_non_primary": supplementary,
            "note": ("supplementary N=10/40 are non-primary and cannot "
                     "rescue or reinterpret a failed primary (§G, §N)")}
