"""Gate 3 ONE-TIME verdict runner — trade-level field-modulated identity v0.1.

Authorized execution harness ONLY. It contains NO result-defining logic: the
verdict is produced solely by the locked, committed module
``field_modulated_identity_trade_level`` (commit c086bec) under the locked
design (commit 8d4bd1d). This runner:

  1. loads the five authorized frozen Phase 3b CSVs and verifies each file's
     SHA-256 against the freeze manifest (5225bfd) — aborts on any mismatch;
  2. tags each row's ``asset`` from its filename (generic, content-agnostic,
     non-result-defining — parallel to Cell 1's reuse of candidate_b_loader);
  3. re-asserts the OOS 2023+ seal in code (aborts if any 2023+ row);
  4. calls fmi.run_full_study(df) EXACTLY ONCE (primary N=20 + supplementary
     N=10/N=40) — this call is the verdict;
  5. computes a DESCRIPTIVE, read-only interaction attribution (§J / §E) that
     reuses the locked feature assembly + locked alpha selection and CANNOT
     and DOES NOT enter the verdict;
  6. writes a machine-readable JSON artifact to results/.

No locked design or implementation file is modified. Run once.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

import field_modulated_identity_trade_level as fmi  # locked module (c086bec)

# Authorized frozen substrate — SHA-256 from docs/pullback_population_freeze_
# manifest_v0.1.md (freeze commit 5225bfd). Order = locked ASSET_LEVELS.
FROZEN = [
    ("SPY", "data/raw/pullback_phase3b_spy_trades_2005_2022.csv",
     "1d8a7b77389835a7231d6ca0742e39d963cf4dc03f822b0111039b5c19383621"),
    ("EFA", "data/raw/pullback_phase3b_efa_trades_2005_2022.csv",
     "275af7e00f28a2a72d948228964c7a4658444f0030ac048e8a2851bc3313de82"),
    ("EEM", "data/raw/pullback_phase3b_eem_trades_2005_2022.csv",
     "56cf8e5fe88f5230ebb8e2881f4df1e0ff633819d588764d9e9e57bbdebb6916"),
    ("GLD", "data/raw/pullback_phase3b_gld_trades_2005_2022.csv",
     "0de7bf6dd981be8d8091a382a6dc0af594a59fa8d87f459305ad25f9dc21d1e3"),
    ("TLT", "data/raw/pullback_phase3b_tlt_trades_2005_2022.csv",
     "037ea4178bd071e426d7cce30eeaffb554ae31d7998c8d00d5e2ba36a7388abc"),
]


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def load_authorized_substrate() -> pd.DataFrame:
    frames = []
    combined = hashlib.sha256()
    for asset, rel, expected in FROZEN:
        p = os.path.join(REPO_ROOT, rel)
        got = _sha256(p)
        if got != expected:
            raise SystemExit(
                "ABORT: SHA-256 mismatch for %s\n  expected %s\n  got      %s"
                % (rel, expected, got))
        combined.update(got.encode())
        df = pd.read_csv(p)
        df.insert(0, "asset", asset)  # generic non-result-defining tag
        frames.append(df)
    pooled = pd.concat(frames, ignore_index=True)
    ed = pd.to_datetime(pooled["entry_date"])
    xd = pd.to_datetime(pooled["exit_date"])
    if (ed >= pd.Timestamp("2023-01-01")).any() or \
       (xd >= pd.Timestamp("2023-01-01")).any():
        raise SystemExit("ABORT: 2023+ row present — OOS seal not authorized")
    pooled.attrs["substrate_sha256"] = combined.hexdigest()
    pooled.attrs["entry_min"] = str(ed.min().date())
    pooled.attrs["entry_max"] = str(ed.max().date())
    pooled.attrs["exit_min"] = str(xd.min().date())
    pooled.attrs["exit_max"] = str(xd.max().date())
    return pooled


def _ridge_coefs(x_tr: np.ndarray, y_tr: np.ndarray, alpha: float
                 ) -> np.ndarray:
    """Coefficients from the SAME centred ridge math as the locked
    ridge_fit_predict (descriptive attribution only; not a verdict path)."""
    xm = x_tr.mean(axis=0)
    yc = y_tr - float(y_tr.mean())
    xc = x_tr - xm
    a = xc.T @ xc + alpha * np.eye(xc.shape[1])
    return np.linalg.solve(a, xc.T @ yc)


def interaction_attribution(df: pd.DataFrame) -> dict:
    """Read-only §E/§J attribution for primary N=20: per-fold M2 ridge
    coefficients on the 21 interaction columns, reusing locked assembly and
    locked alpha selection. Cannot change the verdict."""
    frame = fmi.canonical_pooled_frame(df)
    warm = int(min(fmi.PRIMARY_N, len(frame)))
    post = frame.iloc[warm:].reset_index(drop=True)
    ctx = fmi.build_context_block(frame, fmi.PRIMARY_N).iloc[warm:] \
        .reset_index(drop=True)
    base = fmi.base_feature_frame(post)
    y = np.log1p(np.abs(post["r_multiple"].values.astype(np.float64)))
    finite = np.all(np.isfinite(ctx.values), axis=1) & np.isfinite(y)
    sample = post[finite].reset_index(drop=True)
    ctx = ctx[finite].reset_index(drop=True)
    base = base[finite].reset_index(drop=True)
    y = y[finite]
    pos = np.arange(len(sample))
    splits = fmi._forward_chaining_splits(len(sample), fmi.N_OUTER_SPLITS)
    per_fold_abscoef = []
    for fi, (tr0, va) in enumerate(splits):
        tr = fmi._purge_train(sample, pos, tr0, va)
        mats = fmi._assemble(sample, base, ctx, tr, va, "M2",
                             fmi.MASTER_SEED + fi)
        alpha = fmi._select_alpha(mats["tr"], y[tr])
        w = _ridge_coefs(mats["tr"], y[tr], alpha)
        inter = w[-fmi.N_INTERACTIONS:]            # last 21 cols are interactions
        per_fold_abscoef.append(np.abs(inter))
    mean_abs = np.mean(per_fold_abscoef, axis=0)
    order = np.argsort(mean_abs)[::-1]
    total = float(mean_abs.sum()) or 1.0
    top1 = float(mean_abs[order[0]] / total)
    top3 = float(mean_abs[order[:3]].sum() / total)
    top5 = float(mean_abs[order[:5]].sum() / total)
    names = []
    for idc in fmi.IDENTITY_INTERACTION_COLS:
        for cc in fmi.CONTEXT_COLS:
            names.append("%s_x_%s" % (idc, cc))
    return {
        "interaction_terms": fmi.N_INTERACTIONS,
        "mean_abs_coef_by_term": {names[i]: float(mean_abs[i])
                                  for i in range(len(names))},
        "ranked_terms": [names[i] for i in order],
        "top1_share": top1, "top3_share": top3, "top5_share": top5,
        "concentration_note": (
            "concentrated" if top3 >= 0.60 else
            "diffuse" if top3 <= 0.40 else "mixed"),
    }


def main() -> None:
    ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    df = load_authorized_substrate()
    n_rows = int(len(df))

    result = fmi.run_full_study(df)              # ← THE one-time verdict call
    attribution = interaction_attribution(df)    # descriptive, read-only

    payload = {
        "run_id": "fmi_trade_level_gate3_%s" % ts,
        "timestamp": _dt.datetime.now().isoformat(),
        "design_commit": "8d4bd1dcaf39100882c165583c7bfd805c42b401",
        "code_commit": "c086bec1750d460c86dffbaa9f11e93563b9ca29",
        "substrate": {
            "files": [{"asset": a, "path": p, "sha256": s}
                      for a, p, s in FROZEN],
            "combined_sha256": df.attrs["substrate_sha256"],
            "n_rows": n_rows,
            "entry_date_range": [df.attrs["entry_min"], df.attrs["entry_max"]],
            "exit_date_range": [df.attrs["exit_min"], df.attrs["exit_max"]],
            "oos_2023_plus_present": False,
            "oos_2023_plus_sealed": True,
        },
        "primary_N20": result["primary_N20"],
        "supplementary_non_primary": result["supplementary_non_primary"],
        "supplementary_note": result["note"],
        "interaction_attribution_primary_N20_descriptive": attribution,
        "attestations": {
            "locked_design_unchanged": True,
            "implementation_unchanged_after_results": True,
            "near_miss_is_fail": True,
            "supplementary_cannot_rescue_primary": True,
            "single_one_time_run": True,
        },
    }
    out_dir = os.path.join(REPO_ROOT, "results")
    json_path = os.path.join(
        out_dir, "field_modulated_identity_trade_level_gate3_%s.json" % ts)
    with open(json_path, "w") as fh:
        json.dump(payload, fh, indent=2, default=str)

    print("RUN_ID:", payload["run_id"])
    print("JSON:", json_path)
    p = result["primary_N20"]
    print("\n[PRIMARY N=20] degenerate=%s" % p["degenerate"])
    print(" sample: input=%d warmup=%d undef_drop=%d modeling=%d"
          % (p["n_input_rows"], p["n_warmup_dropped"],
             p["n_undefined_window_dropped"], p["n_modeling_rows"]))
    print(" fold_meta:", p["fold_meta"])
    print(" aggregate OOS R²:",
          {k: round(v, 6) for k, v in p["aggregate_oos_r2"].items()})
    print(" fold OOS R²:",
          {k: [round(x, 6) for x in v] for k, v in p["fold_oos_r2"].items()})
    print(" verdict:", p["verdict"])
    print(" attribution top1/top3/top5 share: %.3f / %.3f / %.3f (%s)"
          % (attribution["top1_share"], attribution["top3_share"],
             attribution["top5_share"], attribution["concentration_note"]))
    print(" top-5 interaction terms:", attribution["ranked_terms"][:5])
    for k, s in result["supplementary_non_primary"].items():
        print("\n[SUPPLEMENTARY %s] (non-primary) degenerate=%s modeling=%d"
              % (k, s["degenerate"], s["n_modeling_rows"]))
        print(" aggregate OOS R²:",
              {kk: round(vv, 6) for kk, vv in s["aggregate_oos_r2"].items()})
        print(" verdict:", s["verdict"])
    print("\nGATE 3 COMPLETE — single run done. No code/params changed.")


if __name__ == "__main__":
    main()
