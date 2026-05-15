"""Candidate C locked protocol — pure-function orchestration.

Implements the design memo locked at commit 401ce45 and ratified by the
lock-acceptance at commit dc97576: parameterized 12 vs 10 annual-sector
partitions, the symmetrical exhaustive 365-DOY anchor surface absorbed into
a median-PSS primary statistic per bucket count, the three coupled
shared-permutation nulls, the four-class verdict map, and the section 11.6
provenance check against Candidate B's stored k = 12 surface.

This module does no file I/O for inputs other than reading Candidate B's
already-committed verdict log for the section 11.6 provenance check. It emits
no volatile metadata; header composition lives in the runner.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Mapping, Tuple

import numpy as np

# Reuse under section 17 item 3 inheritance (reduced row schema) and locked
# infrastructure reuse: the loader and rerun gate are content-agnostic and
# already tested under Candidate B. No new shared/common module is introduced.
from candidate_b_loader import ReducedTrades  # noqa: F401  (re-exported for tests)

from candidate_c_lens import (
    assign_anchor_shifted_phase,
    assign_annual_sector_phase,
    enumerate_anchor_doys,
    enumerate_bucket_counts,
)
from candidate_c_pss import DegenerateLongShareError, pss_long_share

# ── Locked constants ─────────────────────────────────────────────────────────

LABEL_PERM_SEED_C: int = 20260516
ASSET_STRAT_DIAG_SEED_C: int = 20260517
N_PERM: int = 10_000
BEAT_COUNT_THRESHOLD: int = 9_500  # all four beat counts use this
BUCKET_COUNTS: Tuple[int, int] = (12, 10)
ANCHOR_DOYS: Tuple[int, ...] = tuple(range(1, 366))
ACTIVE_MEMO_VERSION: str = "v0.1"
DESIGN_MEMO_COMMIT: str = "401ce45"
LOCK_COMMIT: str = "dc97576"
FREEZE_COMMIT: str = "5225bfd"
B_VERDICT_LOG_PATH: str = (
    "results/candidate_b_results_20260514_231323_c1982503.json"
)
B_N2_NULL_FULL_JSON_PATH: Tuple[str, str] = ("protocol_payload", "n2_null_full")
PROVENANCE_TOLERANCE: float = 1e-12
VERDICT_CLASS_NAMES: Tuple[str, str, str, str] = (
    "12-privileged",
    "10-privileged",
    "Tied / both-structured",
    "Non-confirmatory / unresolved",
)

# Verbatim section 12.2 (a)/(b) blocks, extracted character-exact from
# docs/candidate_c_design_memo_v0.1.md at commit 401ce45 (lines 300-334).
_C1_A = (
    "(a) What it supports: under the locked decision rules, the 12-bucket "
    "partition is distinguished from the 10-bucket partition on this "
    "substrate and the 12-bucket partition is itself non-random against its "
    "own null. The comparison and individual evidence are jointly consistent "
    "with 12 carrying structure that 10 does not capture under the locked "
    "protocol."
)
_C1_B = (
    "(b) What it does not support: the verdict does not establish that 12 is "
    "uniquely privileged among all bucket counts (the locked design tests "
    "only 12 vs 10); it does not establish that 12 is privileged because of a "
    "duodecimal property as opposed to a feature of this substrate at this "
    "resolution; it does not confirm or rescue Candidate B's equinox "
    "hypothesis; and it does not generalize to other populations, windows, or "
    "anchor configurations not pre-registered here."
)
_C2_A = (
    "(a) What it supports: under the locked decision rules, the 10-bucket "
    "partition is distinguished from the 12-bucket partition on this "
    "substrate and the 10-bucket partition is itself non-random against its "
    "own null. Comparison and individual evidence are jointly consistent "
    "with 10 carrying structure that 12 does not capture under the locked "
    "protocol."
)
_C2_B = (
    "(b) What it does not support: the verdict does not falsify the "
    "duodecimal program in general; it does not establish 10 as uniquely "
    "privileged among all bucket counts; it does not show that 10 is "
    "structurally meaningful (the result might reflect a base-rate "
    "periodicity unrelated to \"10-ness\"); and it does not "
    "generalize to other populations or anchors."
)
_C3_A = (
    "(a) What it supports: under the locked decision rules, both 12-bucket "
    "and 10-bucket partitions are individually non-random on this substrate, "
    "but neither is distinguished from the other in direct comparison. The "
    "phase-conditional long-share signal is present at a resolution scale "
    "that the comparison cannot tell apart at the 9500-threshold level. This "
    "is informative texture about the structural scale: the signal is "
    "unlikely to be specific to either bucket count."
)
_C3_B = (
    "(b) What it does not support: the verdict does not adjudicate whether 12 "
    "or 10 is the \"correct\" frame; it does not establish that the "
    "underlying signal is continuous, multi-scale, or anchor-related; it does "
    "not rescue Candidate B; and it does not motivate selecting either bucket "
    "count for downstream work."
)
_C4_A = (
    "(a) What it supports: under the locked decision rules, the result does "
    "not support 12-privileged, 10-privileged, or Tied / both-structured. "
    "The individual and comparison beat counts are reported as diagnostic "
    "texture but they do not upgrade the verdict. This class may include "
    "cases where one bucket count shows individual structure without a "
    "decisive 12-vs-10 comparison — e.g., 12 individually passes but the "
    "comparison threshold is not met; or where comparison favours one "
    "direction without the individual structure threshold being cleared on "
    "either side."
)
_C4_B = (
    "(b) What it does not support: the verdict does not say the substrate is "
    "structureless; it does not adjudicate the broader duodecimal framing "
    "question; it does not rescue Candidate B's equinox hypothesis; it does "
    "not motivate amending the locked design after the fact; and it does not "
    "constrain future cells that might test different bucket-count pairs, "
    "different substrates, or different lens families."
)

VERBALIZATION_BLOCKS: Dict[str, str] = {
    "class_1": _C1_A + "\n\n" + _C1_B,
    "class_2": _C2_A + "\n\n" + _C2_B,
    "class_3": _C3_A + "\n\n" + _C3_B,
    "class_4": _C4_A + "\n\n" + _C4_B,
}

_MACHINE_TO_DISPLAY = {
    "class_1": VERDICT_CLASS_NAMES[0],
    "class_2": VERDICT_CLASS_NAMES[1],
    "class_3": VERDICT_CLASS_NAMES[2],
    "class_4": VERDICT_CLASS_NAMES[3],
}


# ── Phase cubes and PSS surfaces ─────────────────────────────────────────────

def _entry_dates(reduced) -> List[Any]:
    return list(reduced.entry_date)


def _is_long_int(reduced) -> np.ndarray:
    return np.asarray(reduced.is_long, dtype=bool).astype(np.int64)


def _build_phase_cube(reduced, bucket_count: int) -> np.ndarray:
    """Deterministic (365, n_trades) int64 phase array for one bucket count.

    Row j corresponds to anchor DOY (j + 1). Independent of is_long, so it is
    built once and reused across every permutation (the required performance
    lever).
    """
    eds = _entry_dates(reduced)
    n = len(eds)
    cube = np.empty((365, n), dtype=np.int64)
    for j in range(365):
        doy = j + 1
        for t in range(n):
            cube[j, t] = assign_anchor_shifted_phase(eds[t], doy, bucket_count)
    return cube


def _surface_canonical(
    is_long, cube: np.ndarray, bucket_count: int
) -> Dict[int, float]:
    """365-anchor PSS surface via the canonical pss_long_share path.

    Used for observed outcomes and the section 11.6 provenance check so the
    numbers are bit-comparable with Candidate B's stored surface.
    """
    surface: Dict[int, float] = {}
    for j in range(365):
        surface[j + 1] = pss_long_share(is_long, cube[j], bucket_count)
    return surface


def pss_surface(reduced, bucket_count: int) -> Dict[int, float]:
    """Public: 365-entry {doy: PSS_k(doy)} surface for one bucket count."""
    cube = _build_phase_cube(reduced, bucket_count)
    is_long = np.asarray(reduced.is_long, dtype=bool)
    return _surface_canonical(is_long, cube, bucket_count)


def median_pss(surface: Mapping[int, float]) -> float:
    """Median over the anchor surface. Odd N = 365 -> exact middle order stat."""
    values = np.asarray(list(surface.values()), dtype=np.float64)
    return float(np.median(values))


def compute_observed_outcomes(reduced) -> Dict[str, Any]:
    """median_12_observed, median_10_observed, diff_observed + both surfaces."""
    surfaces: Dict[int, Dict[int, float]] = {}
    for k in BUCKET_COUNTS:
        surfaces[k] = pss_surface(reduced, k)
    median_12 = median_pss(surfaces[12])
    median_10 = median_pss(surfaces[10])
    return {
        "median_12_observed": float(median_12),
        "median_10_observed": float(median_10),
        "diff_observed": float(median_12 - median_10),
        "pss_surface_12": {str(d): float(v) for d, v in surfaces[12].items()},
        "pss_surface_10": {str(d): float(v) for d, v in surfaces[10].items()},
    }


# ── Fast vectorized surface for the permutation pool ─────────────────────────

def _prep_fast(cube: np.ndarray, bucket_count: int):
    """Precompute flattened bin index and constant per-anchor phase counts."""
    n_rows, n = cube.shape
    rowbase = np.arange(n_rows, dtype=np.int64)[:, None] * bucket_count
    flat = (rowbase + cube).ravel()
    n_bins = n_rows * bucket_count
    n_p = np.bincount(flat, minlength=n_bins).astype(np.float64).reshape(
        n_rows, bucket_count
    )
    return flat, n_p, n_rows, n


def _median_surface_fast(
    is_long_int: np.ndarray,
    flat: np.ndarray,
    n_p: np.ndarray,
    n_rows: int,
    n: int,
    bucket_count: int,
    total_k: float,
    share_pooled: float,
) -> float:
    """Vectorized 365-anchor surface for a permuted is_long; returns its median.

    Arithmetic mirrors candidate_c_pss.pss_long_share exactly: only l_p varies
    across permutations (n_p, total_k, share_pooled are permutation-invariant).
    """
    n_bins = n_rows * bucket_count
    weights_flat = np.broadcast_to(
        is_long_int.astype(np.float64), (n_rows, n)
    ).reshape(-1)
    l_p = np.bincount(flat, weights=weights_flat, minlength=n_bins).reshape(
        n_rows, bucket_count
    )
    with np.errstate(divide="ignore", invalid="ignore"):
        share_p = np.where(n_p > 0, l_p / n_p, 0.0)
    weights = n_p / float(n)
    between = (
        (share_p - share_pooled) ** 2 * weights * (n_p > 0)
    ).sum(axis=1)
    pss = between / total_k
    return float(np.median(pss))


def _shared_pool(
    reduced,
    n_perm: int,
    seed: int,
    stratified: bool,
) -> Dict[str, np.ndarray]:
    """One shared pool of n_perm is_long permutations -> three coupled nulls.

    stratified=False: unstratified pooled shuffle (section 10.1 primary).
    stratified=True : within-asset shuffle (section 11.3 diagnostic).
    """
    is_long_int = _is_long_int(reduced)
    n = is_long_int.size
    n_long = int(is_long_int.sum())
    share_pooled = float(n_long) / float(n)
    total_k = share_pooled * (1.0 - share_pooled)
    if total_k == 0.0:
        raise DegenerateLongShareError(
            "total_k = 0 (share_pooled = {}); allocation heterogeneity "
            "undefined".format(share_pooled)
        )

    prep = {}
    for k in BUCKET_COUNTS:
        cube = _build_phase_cube(reduced, k)
        prep[k] = _prep_fast(cube, k)

    rng = np.random.Generator(np.random.PCG64(seed))
    m12 = np.empty(n_perm, dtype=np.float64)
    m10 = np.empty(n_perm, dtype=np.float64)

    permuted = is_long_int.copy()
    if stratified:
        asset = np.asarray(reduced.asset)
        groups = [np.where(asset == a)[0] for a in sorted({str(x) for x in asset.tolist()})]

    for i in range(n_perm):
        if stratified:
            for idx in groups:
                vals = permuted[idx]
                rng.shuffle(vals)
                permuted[idx] = vals
        else:
            rng.shuffle(permuted)
        flat12, np12, nr12, n12 = prep[12]
        flat10, np10, nr10, n10 = prep[10]
        m12[i] = _median_surface_fast(
            permuted, flat12, np12, nr12, n12, 12, total_k, share_pooled
        )
        m10[i] = _median_surface_fast(
            permuted, flat10, np10, nr10, n10, 10, total_k, share_pooled
        )

    comparison = m12 - m10
    return {
        "matched_null_12": m12,
        "matched_null_10": m10,
        "comparison_null": comparison,
    }


def run_shared_permutation_pool(
    reduced, n_perm: int, seed: int
) -> Dict[str, np.ndarray]:
    """Section 10.1 primary pool: three coupled nulls, unstratified shuffle."""
    return _shared_pool(reduced, n_perm, seed, stratified=False)


def run_asset_stratified_diagnostic(
    reduced, n_perm: int, seed: int
) -> Dict[str, np.ndarray]:
    """Section 11.3 diagnostic pool: three coupled nulls, within-asset shuffle."""
    return _shared_pool(reduced, n_perm, seed, stratified=True)


# ── Beat counts and verdict ──────────────────────────────────────────────────

def compute_beat_counts(
    observed: Mapping[str, Any], perm_pool: Mapping[str, np.ndarray]
) -> Dict[str, int]:
    """Four strict-`<`/`>` beat counts (section 10.3); ties do not pass."""
    m12 = np.asarray(perm_pool["matched_null_12"], dtype=np.float64)
    m10 = np.asarray(perm_pool["matched_null_10"], dtype=np.float64)
    cmp_null = np.asarray(perm_pool["comparison_null"], dtype=np.float64)
    med12 = float(observed["median_12_observed"])
    med10 = float(observed["median_10_observed"])
    diff = float(observed["diff_observed"])
    return {
        "beat_count_12_individual": int((m12 < med12).sum()),
        "beat_count_10_individual": int((m10 < med10).sum()),
        "beat_count_comparison_12": int((cmp_null < diff).sum()),
        "beat_count_comparison_10": int((cmp_null > diff).sum()),
    }


def evaluate_verdict(
    beat_counts: Mapping[str, int], threshold: int = BEAT_COUNT_THRESHOLD
) -> Dict[str, Any]:
    """Four-class verdict map (section 12.2). MECE over the beat-count vector."""
    i12 = int(beat_counts["beat_count_12_individual"]) >= threshold
    i10 = int(beat_counts["beat_count_10_individual"]) >= threshold
    c12 = int(beat_counts["beat_count_comparison_12"]) >= threshold
    c10 = int(beat_counts["beat_count_comparison_10"]) >= threshold

    if c12 and i12:
        machine = "class_1"
    elif c10 and i10:
        machine = "class_2"
    elif (not c12 and not c10) and (i12 and i10):
        machine = "class_3"
    else:
        machine = "class_4"

    return {
        "verdict_class": _MACHINE_TO_DISPLAY[machine],
        "verdict_class_machine": machine,
        "verbalization": VERBALIZATION_BLOCKS[machine],
        "threshold_pass": {
            "beat_count_12_individual": bool(i12),
            "beat_count_10_individual": bool(i10),
            "beat_count_comparison_12": bool(c12),
            "beat_count_comparison_10": bool(c10),
        },
    }


# ── Diagnostics (section 11) ─────────────────────────────────────────────────

def _surface_str_keys(surface: Mapping[int, float]) -> Dict[str, float]:
    return {str(d): float(v) for d, v in surface.items()}


def _best_anchor(surface: Mapping[int, float]) -> Tuple[int, float]:
    best_d = max(surface, key=lambda d: surface[d])
    return (int(best_d), float(surface[best_d]))


def _shape(surface: Mapping[int, float]) -> Dict[str, float]:
    vals = np.asarray(list(surface.values()), dtype=np.float64)
    return {
        "mean": float(vals.mean()),
        "std": float(vals.std()),
        "min": float(vals.min()),
        "max": float(vals.max()),
    }


def _top_10(surface: Mapping[int, float]) -> List[Tuple[int, float]]:
    ordered = sorted(surface.items(), key=lambda kv: kv[1], reverse=True)
    return [(int(d), float(v)) for d, v in ordered[:10]]


def _per_asset_pss_civil_march20(reduced, bucket_count: int) -> Dict[str, Any]:
    """Per-asset PSS at the civil-date March-20 anchor via section 7.1.

    Section 11.4 / 7.4: this uses the civil-date formula (March 20 -> DOY 80
    in leap years), NOT a DOY anchor from the section 7.2 sweep.
    """
    asset = np.asarray(reduced.asset)
    is_long = np.asarray(reduced.is_long, dtype=bool)
    eds = _entry_dates(reduced)
    phase = np.fromiter(
        (assign_annual_sector_phase(d, bucket_count) for d in eds),
        dtype=np.int64,
        count=len(eds),
    )
    out: Dict[str, Any] = {}
    for a in sorted({str(x) for x in asset.tolist()}):
        mask = asset == a
        try:
            out[a] = float(
                pss_long_share(is_long[mask], phase[mask], bucket_count)
            )
        except DegenerateLongShareError:
            out[a] = None
    return out


def _per_asset_pss_at_anchor(
    reduced, bucket_count: int, anchor_doy: int
) -> Dict[str, Any]:
    asset = np.asarray(reduced.asset)
    is_long = np.asarray(reduced.is_long, dtype=bool)
    eds = _entry_dates(reduced)
    phase = np.fromiter(
        (
            assign_anchor_shifted_phase(d, anchor_doy, bucket_count)
            for d in eds
        ),
        dtype=np.int64,
        count=len(eds),
    )
    out: Dict[str, Any] = {}
    for a in sorted({str(x) for x in asset.tolist()}):
        mask = asset == a
        try:
            out[a] = float(
                pss_long_share(is_long[mask], phase[mask], bucket_count)
            )
        except DegenerateLongShareError:
            out[a] = None
    return out


def compute_diagnostics(reduced) -> Dict[str, Any]:
    """Section 11.1/11.2/11.4/11.5 diagnostics. No verdict effect.

    The section 11.6 provenance check is intentionally NOT performed here; it
    is added by run() with the same b_verdict_log_path that run() received,
    per the path-handling discipline.
    """
    surfaces = {k: pss_surface(reduced, k) for k in BUCKET_COUNTS}
    best12 = _best_anchor(surfaces[12])
    best10 = _best_anchor(surfaces[10])
    return {
        "best_anchor_pss_12": list(best12),
        "best_anchor_pss_10": list(best10),
        "anchor_distribution_shape_12": _shape(surfaces[12]),
        "anchor_distribution_shape_10": _shape(surfaces[10]),
        "per_asset_pss_civil_march20_12": _per_asset_pss_civil_march20(
            reduced, 12
        ),
        "per_asset_pss_civil_march20_10": _per_asset_pss_civil_march20(
            reduced, 10
        ),
        "per_asset_pss_peak_anchor_12": _per_asset_pss_at_anchor(
            reduced, 12, best12[0]
        ),
        "per_asset_pss_peak_anchor_10": _per_asset_pss_at_anchor(
            reduced, 10, best10[0]
        ),
        "top_10_anchors_12": [list(t) for t in _top_10(surfaces[12])],
        "top_10_anchors_10": [list(t) for t in _top_10(surfaces[10])],
        "_pss_surface_12_str": _surface_str_keys(surfaces[12]),
        "_pss_surface_10_str": _surface_str_keys(surfaces[10]),
    }


# ── Section 11.6 provenance check ────────────────────────────────────────────

def verify_b_provenance(
    c_pss_surface_12: Mapping[Any, float],
    b_verdict_log_path: str,
    tolerance: float = PROVENANCE_TOLERANCE,
) -> Dict[str, float]:
    """Compare C's k = 12 365-anchor surface to B's stored n2_null_full.

    Reads protocol_payload.n2_null_full from b_verdict_log_path (stringified
    integer DOY keys "1".."365"). Raises RuntimeError if the max absolute
    per-anchor difference exceeds tolerance.
    """
    with open(b_verdict_log_path, "r") as fh:
        b_log = json.load(fh)
    node: Any = b_log
    for key in B_N2_NULL_FULL_JSON_PATH:
        node = node[key]
    b_surface = node  # dict: str(doy) -> float

    def _lookup(d: int) -> float:
        if d in c_pss_surface_12:
            return float(c_pss_surface_12[d])
        return float(c_pss_surface_12[str(d)])

    max_abs_diff = 0.0
    for d in range(1, 366):
        c_val = _lookup(d)
        b_val = float(b_surface[str(d)])
        diff = abs(c_val - b_val)
        if diff > max_abs_diff:
            max_abs_diff = diff

    passed = max_abs_diff <= tolerance
    if not passed:
        raise RuntimeError(
            "Candidate C k=12 365-anchor surface diverges from Candidate B's "
            "stored protocol_payload.n2_null_full: max_abs_diff={} exceeds "
            "tolerance={} (audit-chain inconsistency; run aborted)".format(
                max_abs_diff, tolerance
            )
        )
    return {
        "max_abs_diff": float(max_abs_diff),
        "n_anchors_checked": 365,
        "pass": bool(passed),
    }


# ── Top-level run ────────────────────────────────────────────────────────────

def run(
    reduced,
    b_verdict_log_path: str,
    n_perm: int = N_PERM,
    label_perm_seed: int = LABEL_PERM_SEED_C,
    asset_strat_seed: int = ASSET_STRAT_DIAG_SEED_C,
    beat_count_threshold: int = BEAT_COUNT_THRESHOLD,
) -> Dict[str, Any]:
    """Top-level protocol invocation. Returns the JSON-serializable payload."""
    observed = compute_observed_outcomes(reduced)

    primary_pool = run_shared_permutation_pool(reduced, n_perm, label_perm_seed)
    beat_counts = compute_beat_counts(observed, primary_pool)
    verdict = evaluate_verdict(beat_counts, beat_count_threshold)

    strat_pool = run_asset_stratified_diagnostic(
        reduced, n_perm, asset_strat_seed
    )
    strat_beat_counts = compute_beat_counts(observed, strat_pool)

    diagnostics = compute_diagnostics(reduced)
    surface_12_str = diagnostics.pop("_pss_surface_12_str")
    surface_10_str = diagnostics.pop("_pss_surface_10_str")
    diagnostics["provenance_check"] = verify_b_provenance(
        surface_12_str, b_verdict_log_path, PROVENANCE_TOLERANCE
    )

    return {
        "active_memo_version": ACTIVE_MEMO_VERSION,
        "design_memo_commit": DESIGN_MEMO_COMMIT,
        "lock_acceptance_commit": LOCK_COMMIT,
        "freeze_commit": FREEZE_COMMIT,
        "n_trades": int(len(reduced)),
        "n_perm": int(n_perm),
        "anchor_population_size": 365,
        "bucket_counts": list(BUCKET_COUNTS),
        "locked_parameters": {
            "anchor_month": 3,
            "anchor_day": 20,
            "bucket_counts": list(BUCKET_COUNTS),
            "beat_count_threshold": int(beat_count_threshold),
            "provenance_tolerance": PROVENANCE_TOLERANCE,
        },
        "seeds": {
            "LABEL_PERM_SEED_C": int(label_perm_seed),
            "ASSET_STRAT_DIAG_SEED_C": int(asset_strat_seed),
            "N_PERM": int(n_perm),
        },
        "observed": {
            "median_12_observed": observed["median_12_observed"],
            "median_10_observed": observed["median_10_observed"],
            "diff_observed": observed["diff_observed"],
        },
        "beat_counts": {k: int(v) for k, v in beat_counts.items()},
        "threshold_pass": verdict["threshold_pass"],
        "verdict_class": verdict["verdict_class"],
        "verdict_class_machine": verdict["verdict_class_machine"],
        "verbalization": verdict["verbalization"],
        "matched_null_12_full": [float(x) for x in primary_pool["matched_null_12"].tolist()],
        "matched_null_10_full": [float(x) for x in primary_pool["matched_null_10"].tolist()],
        "comparison_null_full": [float(x) for x in primary_pool["comparison_null"].tolist()],
        "pss_surface_12": observed["pss_surface_12"],
        "pss_surface_10": observed["pss_surface_10"],
        "asset_stratified_diagnostic": {
            "matched_null_12": [float(x) for x in strat_pool["matched_null_12"].tolist()],
            "matched_null_10": [float(x) for x in strat_pool["matched_null_10"].tolist()],
            "comparison_null": [float(x) for x in strat_pool["comparison_null"].tolist()],
            "beat_counts": {k: int(v) for k, v in strat_beat_counts.items()},
        },
        "diagnostics": diagnostics,
    }
