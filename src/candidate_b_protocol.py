"""Candidate B locked protocol — pure-function orchestration.

Implements sections 9.1 (PSS_B1), 10.1 (N.1 unstratified label permutation),
10.2 (N.2 exhaustive 365-DOY anchor control), 11.1–11.5 (controls and
diagnostics), 12 (verdict map), and 14 (seeds) of the locked design memo
at commit 1e9a3e6, ratified at lock-acceptance 159cccd.

This module does no file I/O, no network access, and emits no volatile
metadata. It accepts an in-memory ReducedTrades view and returns the
deterministic protocol payload. Header composition (timestamps, paths,
repo HEAD, etc.) lives in the runner.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

import numpy as np

from candidate_b_lens import (
    BUCKET_COUNT,
    MARCH20_ANCHOR_DAY,
    MARCH20_ANCHOR_MONTH,
    assign_anchor_shifted_phase,
    assign_annual_sector_phase,
    enumerate_anchor_doys,
)
from candidate_b_pss import (
    DegenerateLongShareError,
    pss_b1_long_share,
    pss_b2_r_multiple,
)

# Locked constants — section 14 of the design memo.
LABEL_PERM_SEED: int = 20260514
ASSET_STRAT_DIAG_SEED: int = 20260515
N_PERM: int = 10_000

# Locked verdict thresholds — section 12.1 of the design memo.
PERM_BEAT_THRESHOLD: int = 9_500
ANCHOR_BEAT_THRESHOLD: int = 347

ACTIVE_MEMO_VERSION: str = "v0.1"
LOCK_COMMIT: str = "159cccd"
DESIGN_MEMO_COMMIT: str = "1e9a3e6"
FREEZE_COMMIT: str = "5225bfd"


def _phase_array_march20(entry_dates) -> np.ndarray:
    out = np.empty(len(entry_dates), dtype=np.int64)
    for i, d in enumerate(entry_dates):
        out[i] = assign_annual_sector_phase(d)
    return out


def _phase_array_anchor(entry_dates, anchor_doy: int) -> np.ndarray:
    out = np.empty(len(entry_dates), dtype=np.int64)
    for i, d in enumerate(entry_dates):
        out[i] = assign_anchor_shifted_phase(d, anchor_doy)
    return out


def _gregorian_month_phase(entry_dates) -> np.ndarray:
    out = np.empty(len(entry_dates), dtype=np.int64)
    for i, d in enumerate(entry_dates):
        out[i] = d.month - 1
    return out


def compute_observed_pss_b1(reduced) -> float:
    """Compute observed PSS_B1 on the pooled reduced population."""
    phase = _phase_array_march20(reduced.entry_date)
    return pss_b1_long_share(reduced.is_long, phase, n_phases=BUCKET_COUNT)


def run_n1_label_permutation_null(
    reduced,
    n_perm: int = N_PERM,
    seed: int = LABEL_PERM_SEED,
) -> np.ndarray:
    """N.1 — unstratified label permutation across the pooled population.

    Section 10.1. Phase labels and asset labels are held fixed; only the
    is_long vector is uniformly shuffled (ignoring asset). Returns a
    length-`n_perm` float64 array of permuted PSS_B1 values.
    """
    phase = _phase_array_march20(reduced.entry_date)
    is_long = np.asarray(reduced.is_long, dtype=bool)
    rng = np.random.Generator(np.random.PCG64(seed))
    null = np.empty(n_perm, dtype=np.float64)
    permuted = is_long.copy()
    for i in range(n_perm):
        rng.shuffle(permuted)
        null[i] = pss_b1_long_share(permuted, phase, n_phases=BUCKET_COUNT)
    return null


def run_n2_anchor_control_null(reduced) -> Dict[int, float]:
    """N.2 — exhaustive 365-DOY anchor-control null.

    Section 10.2. Deterministic enumeration; no seed is consumed.
    """
    is_long = np.asarray(reduced.is_long, dtype=bool)
    null: Dict[int, float] = {}
    for doy in enumerate_anchor_doys():
        phase = _phase_array_anchor(reduced.entry_date, doy)
        null[doy] = pss_b1_long_share(is_long, phase, n_phases=BUCKET_COUNT)
    return null


def run_asset_stratified_diagnostic(
    reduced,
    n_perm: int = N_PERM,
    seed: int = ASSET_STRAT_DIAG_SEED,
) -> np.ndarray:
    """Section 11.3 asset-stratified label-permutation diagnostic.

    Shuffles is_long within each asset's index slice independently. Uses a
    separate PCG64 seed so the diagnostic's permutation sequence is not a
    sub-sample of the primary N.1 sequence. Returns length-`n_perm` array.
    """
    phase = _phase_array_march20(reduced.entry_date)
    is_long = np.asarray(reduced.is_long, dtype=bool)
    asset = np.asarray(reduced.asset)
    unique_assets = sorted({str(a) for a in asset.tolist()})
    asset_indices = {a: np.where(asset == a)[0] for a in unique_assets}

    rng = np.random.Generator(np.random.PCG64(seed))
    null = np.empty(n_perm, dtype=np.float64)
    permuted = is_long.copy()
    for i in range(n_perm):
        for a in unique_assets:
            idx = asset_indices[a]
            values = permuted[idx]
            rng.shuffle(values)
            permuted[idx] = values
        null[i] = pss_b1_long_share(permuted, phase, n_phases=BUCKET_COUNT)
    return null


def _per_asset_pss(reduced, phase: np.ndarray) -> Dict[str, Optional[float]]:
    is_long = np.asarray(reduced.is_long, dtype=bool)
    asset = np.asarray(reduced.asset)
    out: Dict[str, Optional[float]] = {}
    for a in sorted({str(x) for x in asset.tolist()}):
        mask = asset == a
        try:
            out[a] = float(
                pss_b1_long_share(is_long[mask], phase[mask], n_phases=BUCKET_COUNT)
            )
        except DegenerateLongShareError:
            out[a] = None
    return out


def _phase_cell_occupancy(phase: np.ndarray, is_long: np.ndarray) -> List[Dict[str, int]]:
    out: List[Dict[str, int]] = []
    for p in range(BUCKET_COUNT):
        mask = phase == p
        n_p = int(mask.sum())
        l_p = int(is_long[mask].sum()) if n_p > 0 else 0
        out.append({"phase": p, "N_p": n_p, "L_p": l_p})
    return out


def _c4_directional_counts(phase: np.ndarray, is_long: np.ndarray) -> List[Dict[str, int]]:
    out: List[Dict[str, int]] = []
    for p in range(BUCKET_COUNT):
        mask = phase == p
        n_long = int((mask & is_long).sum())
        n_short = int((mask & ~is_long).sum())
        out.append({"phase": p, "n_long": n_long, "n_short": n_short})
    return out


def _c4_within_direction_r_multiple(
    phase: np.ndarray, is_long: np.ndarray, r_multiple: np.ndarray
) -> Dict[str, List[Dict[str, Any]]]:
    longs: List[Dict[str, Any]] = []
    shorts: List[Dict[str, Any]] = []
    for p in range(BUCKET_COUNT):
        mask = phase == p
        l_mask = mask & is_long
        s_mask = mask & ~is_long
        longs.append({
            "phase": p,
            "n": int(l_mask.sum()),
            "mean_r_multiple": (float(r_multiple[l_mask].mean()) if l_mask.any() else None),
        })
        shorts.append({
            "phase": p,
            "n": int(s_mask.sum()),
            "mean_r_multiple": (float(r_multiple[s_mask].mean()) if s_mask.any() else None),
        })
    return {"long": longs, "short": shorts}


def compute_diagnostics(reduced) -> Dict[str, Any]:
    """Sections 11.1, 11.2, 11.4, 11.5, and C.4 diagnostics. No verdict effect."""
    is_long = np.asarray(reduced.is_long, dtype=bool)
    r_multiple = np.asarray(reduced.r_multiple, dtype=np.float64)
    phase_march = _phase_array_march20(reduced.entry_date)

    month_phase = _gregorian_month_phase(reduced.entry_date)
    pss_greg_month = float(
        pss_b1_long_share(is_long, month_phase, n_phases=BUCKET_COUNT)
    )

    jan_phase = _phase_array_anchor(reduced.entry_date, 1)
    pss_jan = float(pss_b1_long_share(is_long, jan_phase, n_phases=BUCKET_COUNT))

    per_asset = _per_asset_pss(reduced, phase_march)
    occupancy = _phase_cell_occupancy(phase_march, is_long)
    c4_counts = _c4_directional_counts(phase_march, is_long)
    c4_r = _c4_within_direction_r_multiple(phase_march, is_long, r_multiple)

    pss_b2 = float(pss_b2_r_multiple(r_multiple, phase_march, n_phases=BUCKET_COUNT))

    return {
        "pss_greg_month": pss_greg_month,
        "pss_jan": pss_jan,
        "per_asset_pss_b1": per_asset,
        "phase_cell_occupancy": occupancy,
        "c4_directional_counts": c4_counts,
        "c4_within_direction_r_multiple": c4_r,
        "pss_b2_r_multiple": pss_b2,
    }


def evaluate_verdict(
    observed: float,
    perm_null,
    anchor_null,
    asset_strat_null=None,
    perm_beat_threshold: int = PERM_BEAT_THRESHOLD,
    anchor_beat_threshold: int = ANCHOR_BEAT_THRESHOLD,
) -> Dict[str, Any]:
    """Section 12. Three-class verdict map + section 12.4 verbalization rule."""
    perm_arr = np.asarray(list(perm_null), dtype=np.float64)
    if isinstance(anchor_null, Mapping):
        anchor_arr = np.asarray(list(anchor_null.values()), dtype=np.float64)
    else:
        anchor_arr = np.asarray(list(anchor_null), dtype=np.float64)

    if perm_arr.size == 0 or anchor_arr.size == 0:
        raise ValueError("permutation and anchor nulls must be non-empty")

    beat_count_perm = int((perm_arr < observed).sum())
    beat_count_anchor = int((anchor_arr < observed).sum())
    perm_pass = beat_count_perm >= perm_beat_threshold
    anchor_pass = beat_count_anchor >= anchor_beat_threshold

    if perm_pass and anchor_pass:
        verdict = "Confirmatory"
    elif perm_pass or anchor_pass:
        verdict = "Split-null"
    else:
        verdict = "Non-confirmatory"

    asset_strat_beat: Optional[int] = None
    asset_strat_size: Optional[int] = None
    if asset_strat_null is not None:
        asset_strat_arr = np.asarray(list(asset_strat_null), dtype=np.float64)
        asset_strat_beat = int((asset_strat_arr < observed).sum())
        asset_strat_size = int(asset_strat_arr.size)

    if verdict == "Confirmatory":
        if asset_strat_beat is not None and asset_strat_size is not None:
            asset_strat_strong = asset_strat_beat >= perm_beat_threshold
            verbalization_class = (
                "pooled-modulation-persists-under-asset-mix"
                if asset_strat_strong
                else "pooled-population-modulation"
            )
        else:
            verbalization_class = "pooled-population-modulation"
    elif verdict == "Split-null":
        verbalization_class = "n/a-split-null"
    else:
        verbalization_class = "n/a-non-confirmatory"

    return {
        "observed_pss_b1": float(observed),
        "beat_count_perm": beat_count_perm,
        "beat_count_anchor": beat_count_anchor,
        "perm_strict_percentile": beat_count_perm / float(perm_arr.size),
        "anchor_strict_percentile": beat_count_anchor / float(anchor_arr.size),
        "perm_threshold_pass": perm_pass,
        "anchor_threshold_pass": anchor_pass,
        "verdict": verdict,
        "verbalization_class": verbalization_class,
        "asset_stratified_beat_count": asset_strat_beat,
        "asset_stratified_perm_size": asset_strat_size,
        "thresholds": {
            "perm_beat_threshold": perm_beat_threshold,
            "anchor_beat_threshold": anchor_beat_threshold,
        },
    }


def run(
    reduced,
    n_perm: int = N_PERM,
    label_perm_seed: int = LABEL_PERM_SEED,
    asset_strat_seed: int = ASSET_STRAT_DIAG_SEED,
    perm_beat_threshold: int = PERM_BEAT_THRESHOLD,
    anchor_beat_threshold: int = ANCHOR_BEAT_THRESHOLD,
) -> Dict[str, Any]:
    """Top-level protocol invocation. Returns only the deterministic payload."""
    observed = compute_observed_pss_b1(reduced)
    perm_null = run_n1_label_permutation_null(
        reduced, n_perm=n_perm, seed=label_perm_seed
    )
    anchor_null = run_n2_anchor_control_null(reduced)
    asset_strat_null = run_asset_stratified_diagnostic(
        reduced, n_perm=n_perm, seed=asset_strat_seed
    )

    verdict_info = evaluate_verdict(
        observed,
        perm_null,
        anchor_null,
        asset_strat_null=asset_strat_null,
        perm_beat_threshold=perm_beat_threshold,
        anchor_beat_threshold=anchor_beat_threshold,
    )

    diagnostics = compute_diagnostics(reduced)
    asset_strat_arr = np.asarray(asset_strat_null, dtype=np.float64)
    diagnostics["asset_stratified_beat_count"] = int(
        (asset_strat_arr < observed).sum()
    )
    diagnostics["asset_stratified_perm_strict_percentile"] = (
        diagnostics["asset_stratified_beat_count"] / float(asset_strat_arr.size)
    )

    return {
        "active_memo_version": ACTIVE_MEMO_VERSION,
        "design_memo_commit": DESIGN_MEMO_COMMIT,
        "lock_acceptance_commit": LOCK_COMMIT,
        "freeze_commit": FREEZE_COMMIT,
        "n_trades": int(len(reduced)),
        "n_perm": int(n_perm),
        "anchor_population_size": 365,
        "locked_parameters": {
            "anchor_month": MARCH20_ANCHOR_MONTH,
            "anchor_day": MARCH20_ANCHOR_DAY,
            "bucket_count": BUCKET_COUNT,
            "perm_beat_threshold": int(perm_beat_threshold),
            "anchor_beat_threshold": int(anchor_beat_threshold),
        },
        "seeds": {
            "LABEL_PERM_SEED": int(label_perm_seed),
            "ASSET_STRAT_DIAG_SEED": int(asset_strat_seed),
        },
        "observed_pss_b1": verdict_info["observed_pss_b1"],
        "beat_count_perm": verdict_info["beat_count_perm"],
        "beat_count_anchor": verdict_info["beat_count_anchor"],
        "perm_strict_percentile": verdict_info["perm_strict_percentile"],
        "anchor_strict_percentile": verdict_info["anchor_strict_percentile"],
        "perm_threshold_pass": verdict_info["perm_threshold_pass"],
        "anchor_threshold_pass": verdict_info["anchor_threshold_pass"],
        "verdict": verdict_info["verdict"],
        "verbalization_class": verdict_info["verbalization_class"],
        "n1_null_full": [float(x) for x in perm_null.tolist()],
        "n2_null_full": {str(k): float(v) for k, v in anchor_null.items()},
        "asset_stratified_null_full": [float(x) for x in asset_strat_arr.tolist()],
        "diagnostics": diagnostics,
    }
