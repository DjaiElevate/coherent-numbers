"""Influential Numbers Cell 1 protocol (Neighborhood Influence Test).

Locked design memo docs/influential_numbers_cell_1_design_memo_v0.1.md at
commit a765098 (sections 8-20), lock-accepted at commit 3d44e9e. Forked
structurally from src/candidate_c_protocol.py (commit 4432591); the
result-defining surface/lens/PSS/attenuation logic lives entirely in the Cell 1
namespace per design memo section 19. Only the generic ReducedTrades container
is imported from candidate_b_loader. No Candidate C module is imported.

Cell 1 asks whether k = 12 sits inside a structured local neighborhood, not
whether 12 beats 10 (that was Candidate C). The primary statistic is the
focal-centered continuous attenuation score; the contrast is max_gap against
the strongest control focal; the verdict is a four-class map with a hard-binary
Class 4 (pathology only, never a near-threshold escape hatch).
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Mapping, Optional, Tuple

import numpy as np

from candidate_b_loader import ReducedTrades  # noqa: F401  (generic container)

from influential_numbers_cell_1_lens import (
    assign_anchor_shifted_phase,
    enumerate_anchor_doys,
    enumerate_bucket_counts,
)
from influential_numbers_cell_1_pss import (
    DegenerateLongShareError,
    pss_long_share,
)

# ── Locked constants (design memo sections 8, 12-19) ─────────────────────────

LABEL_PERM_SEED_CELL1: int = 20260518
ASSET_STRAT_DIAG_SEED_CELL1: int = 20260519
N_PERM: int = 10_000
BEAT_COUNT_THRESHOLD: int = 9_500  # both primary beat counts use this
FOCAL_CENTERS: Tuple[int, int, int, int] = (10, 12, 14, 16)
PRIMARY_FOCAL: int = 12
CONTROL_FOCALS: Tuple[int, int, int] = (10, 14, 16)
BUCKET_COUNTS: Tuple[int, ...] = tuple(range(7, 20))
ANCHOR_DOYS: Tuple[int, ...] = tuple(range(1, 366))
WINDOW_RADIUS: int = 3
ACTIVE_MEMO_VERSION: str = "v0.1"
DESIGN_MEMO_COMMIT: str = "a765098"
LOCK_COMMIT: str = "3d44e9e"
FRAMEWORK_MEMO_COMMIT: str = "8ff619c"
FREEZE_COMMIT: str = "5225bfd"
CANDIDATE_C_VERDICT_LOG_PATH: str = (
    "results/candidate_c_results_20260515_051236_f3a6bf48.json"
)
CANDIDATE_C_VERDICT_LOG_SHA256: str = (
    "130235fef110cca141fa8873bfa3a6c630a44ac11dfcad953822f41f9cd3c7d4"
)
C_SURFACE_JSON_KEYS: Tuple[str, str] = ("pss_surface_10", "pss_surface_12")
PROVENANCE_TOLERANCE: float = 1e-12

VERDICT_CLASS_NAMES: Tuple[str, str, str, str] = (
    "12-centered neighborhood structure",
    "Generic substrate smoothness",
    "No neighborhood evidence",
    "Non-confirmatory / unresolved",
)

# Verbatim section 15.1a..15.4b (a)/(b) blocks, extracted character-exact from
# docs/influential_numbers_cell_1_design_memo_v0.1.md at commit a765098
# (lines 237, 239, 245, 247, 253, 255, 268, 270), markdown blockquote "> "
# prefix removed. Tests verify these against the locked memo; do not paraphrase.

_C1_A = (
    "**(a) What it supports** *(REQUIRED-VERBATIM, §15.1a):* Under the "
    "locked decision rules, the bucket count `k = 12` sits on a focal-centered "
    "local elevation whose attenuation away from 12 is distinguished from "
    "chance, and that attenuation exceeds the strongest attenuation at any of "
    "the control focals `10`, `14`, `16` on this substrate. The "
    "12-neighborhood behaves as a structured local peak rather than an "
    "isolated point under the locked protocol."
)
_C1_B = (
    "**(b) What it does not support** *(REQUIRED-VERBATIM, §15.1b):* The "
    "verdict does not establish that 12 is uniquely neighborhood-structured "
    "among all bucket counts (only `10, 14, 16` were used as controls); it "
    "does not attribute the structure to a duodecimal, divisor, multiple, "
    "harmonic, or 12-family property (those are Layer 2 and untested here); it "
    "does not establish base-12 mathematics; it does not retroactively "
    "reinterpret Candidate C's `12-privileged` verdict, which remains exactly "
    "\"12 beat 10 under its locked rules\"; it does not confirm or rescue "
    "Candidate B's split-null equinox result; and it does not generalize "
    "beyond the pre-registered substrate, window, or focal set."
)
_C2_A = (
    "**(a) What it supports** *(REQUIRED-VERBATIM, §15.2a):* Under the "
    "locked decision rules, the 12-neighborhood shows attenuation "
    "distinguished from chance, but that attenuation is **not** distinguished "
    "from the attenuation at the strongest control focal. The substrate "
    "appears to produce locally smooth neighborhoods around multiple bucket "
    "centers; 12's local structure is consistent with that generic smoothness "
    "rather than being 12-specific."
)
_C2_B = (
    "**(b) What it does not support** *(REQUIRED-VERBATIM, §15.2b):* The "
    "verdict does not say 12 is unstructured, and it does not say the "
    "substrate is structureless; it specifically does not support a "
    "12-specific neighborhood claim; it does not weaken Candidate C (a "
    "generic-smoothness reading of the neighborhood is independent of C's "
    "binary 12-vs-10 result); and it does not motivate Layer 2 extension as a "
    "rescue."
)
_C3_A = (
    "**(a) What it supports** *(REQUIRED-VERBATIM, §15.3a):* Under the "
    "locked decision rules, there is no evidence that 12 sits inside a "
    "structured local neighborhood on this substrate: either 12's median PSS "
    "does not exceed its non-focal window neighbors, or the 12-neighborhood "
    "attenuation is not distinguished from chance. 12, on the neighborhood "
    "operationalization, behaves as an isolated point rather than a structured "
    "local peak."
)
_C3_B = (
    "**(b) What it does not support** *(REQUIRED-VERBATIM, §15.3b):* This "
    "null does not weaken Candidate C's `12-privileged` verdict — Cell 1 "
    "asks a different question and a no-neighborhood result leaves \"12 beat "
    "10 under C's locked rules\" untouched. It does not say the substrate is "
    "structureless. It does not motivate or authorize Layer 2 (divisor, "
    "multiple, harmonic, 12-family, recursive, weighted) as a rescue; per "
    "§3 and §21, Layer 2 on a Layer 1 null requires a separate "
    "decision memo argued on its own grounds. It does not bear on Candidate B."
)
_C4_A = (
    "**(a) What it supports** *(REQUIRED-VERBATIM, §15.4a):* Under the "
    "locked decision rules, the result does not support any of Class 1, 2, or "
    "3. A design-validity or pathology condition prevented a valid "
    "neighborhood adjudication. Beat counts, if computed, are reported as "
    "diagnostic texture only and do not upgrade the verdict."
)
_C4_B = (
    "**(b) What it does not support** *(REQUIRED-VERBATIM, §15.4b):* This "
    "class does not say the substrate is structureless, does not adjudicate "
    "the neighborhood question, does not rescue or weaken Candidate C or "
    "Candidate B, and does not authorize amending the locked design after the "
    "fact."
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


class CellOnePathology(RuntimeError):
    """Raised internally for design-validity / pathology conditions (Class 4)."""


# ── Focal windows and distances (design memo sections 8, 10) ─────────────────

def window_for_focal(focal: int) -> Tuple[int, ...]:
    """Exact +/-3 linear-integer window W(f) = {f-3, ..., f+3} (ascending k)."""
    return tuple(range(focal - WINDOW_RADIUS, focal + WINDOW_RADIUS + 1))


def distance_vector_for_focal(focal: int) -> np.ndarray:
    """Distances |k - focal| aligned to window_for_focal order: 3,2,1,0,1,2,3."""
    win = window_for_focal(focal)
    return np.asarray([abs(k - focal) for k in win], dtype=np.float64)


# ── Phase cubes and PSS surfaces (forked from Candidate C, Cell 1 namespace) ──

def _entry_dates(reduced) -> List[Any]:
    return list(reduced.entry_date)


def _is_long_int(reduced) -> np.ndarray:
    return np.asarray(reduced.is_long, dtype=bool).astype(np.int64)


def _build_phase_cube(reduced, bucket_count: int) -> np.ndarray:
    """Deterministic (365, n_trades) int64 phase array for one bucket count.

    Row j corresponds to anchor DOY (j + 1). Independent of is_long, so it is
    built once and reused across every permutation (the performance lever).
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

    Used for observed outcomes and the section 17 provenance check so the
    numbers are bit-comparable with Candidate C's stored surfaces.
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


def compute_median_pss_map(reduced) -> Dict[int, float]:
    """median_k for every k in BUCKET_COUNTS = {7, ..., 19} (canonical path)."""
    out: Dict[int, float] = {}
    for k in BUCKET_COUNTS:
        out[k] = median_pss(pss_surface(reduced, k))
    return out


# ── OLS slope and attenuation (design memo section 10) ───────────────────────

def ols_slope(x, y) -> float:
    """Deterministic ordinary-least-squares slope of y on x. No scipy.

    Rejects non-finite values and a zero-variance regressor by raising
    CellOnePathology (routes to Class 4 per design memo section 15.4).
    """
    xa = np.asarray(x, dtype=np.float64)
    ya = np.asarray(y, dtype=np.float64)
    if xa.shape != ya.shape:
        raise ValueError(
            "x and y must have matching shape: {} vs {}".format(
                xa.shape, ya.shape
            )
        )
    if xa.size < 2:
        raise ValueError("need at least two points for a slope")
    if not (np.isfinite(xa).all() and np.isfinite(ya).all()):
        raise CellOnePathology("non-finite value in OLS slope inputs")
    xbar = float(xa.mean())
    ybar = float(ya.mean())
    dx = xa - xbar
    denom = float((dx * dx).sum())
    if denom == 0.0:
        raise CellOnePathology("zero-variance regressor in OLS slope")
    num = float((dx * (ya - ybar)).sum())
    slope = num / denom
    if not np.isfinite(slope):
        raise CellOnePathology("non-finite OLS slope result")
    return float(slope)


def attenuation_score_for_focal(
    median_map: Mapping[int, float], focal: int
) -> float:
    """-slope(median_k ~ |k - focal|) over all 7 points of W(focal).

    The focal (distance 0) is included. Missing focal surface or non-finite /
    degenerate inputs raise CellOnePathology (Class 4).
    """
    win = window_for_focal(focal)
    try:
        y = np.asarray([float(median_map[k]) for k in win], dtype=np.float64)
    except KeyError as exc:
        raise CellOnePathology(
            "missing focal surface: k={} absent from median map".format(exc)
        )
    x = distance_vector_for_focal(focal)
    return float(-ols_slope(x, y))


def compute_attenuation_scores(
    median_map: Mapping[int, float]
) -> Dict[int, float]:
    """attenuation_score_f for f in FOCAL_CENTERS = (10, 12, 14, 16)."""
    return {f: attenuation_score_for_focal(median_map, f) for f in FOCAL_CENTERS}


# ── Focal-elevation gate (design memo section 11) ────────────────────────────

def focal_elevation_gate_12(median_map: Mapping[int, float]) -> Dict[str, Any]:
    """Strict median_12 > mean(median_k for k in W(12), k != 12).

    'ambiguous' is True on an exact floating-point tie or any non-finite input
    (design memo section 15.4 routes that to Class 4).
    """
    win = window_for_focal(PRIMARY_FOCAL)
    try:
        m12 = float(median_map[PRIMARY_FOCAL])
        neighbor_vals = np.asarray(
            [float(median_map[k]) for k in win if k != PRIMARY_FOCAL],
            dtype=np.float64,
        )
    except KeyError as exc:
        return {
            "pass": False,
            "median_12": None,
            "neighbor_mean": None,
            "focal_excess": None,
            "ambiguous": True,
            "ambiguity_reason": "missing focal surface: k={}".format(exc),
        }
    neighbor_mean = float(neighbor_vals.mean())
    finite = bool(np.isfinite(m12) and np.isfinite(neighbor_mean))
    excess = (m12 - neighbor_mean) if finite else None
    tie = bool(finite and m12 == neighbor_mean)
    ambiguous = bool((not finite) or tie)
    reason = None
    if not finite:
        reason = "non-finite value entered the focal-elevation gate"
    elif tie:
        reason = "exact floating-point tie: median_12 == neighbor_mean"
    return {
        "pass": bool(finite and (m12 > neighbor_mean)),
        "median_12": m12 if finite else None,
        "neighbor_mean": neighbor_mean if finite else None,
        "focal_excess": float(excess) if excess is not None else None,
        "ambiguous": ambiguous,
        "ambiguity_reason": reason,
    }


# ── Max-gap contrast (design memo section 12) ────────────────────────────────

def compute_max_gap(
    attenuation_scores: Mapping[int, float]
) -> Dict[str, Any]:
    """max_gap = score_12 - max(score_10, score_14, score_16)."""
    s12 = float(attenuation_scores[PRIMARY_FOCAL])
    control_pairs = [(f, float(attenuation_scores[f])) for f in CONTROL_FOCALS]
    strongest_focal, strongest_score = max(control_pairs, key=lambda fp: fp[1])
    return {
        "max_gap": float(s12 - strongest_score),
        "score_12": s12,
        "strongest_control_focal": int(strongest_focal),
        "strongest_control_score": float(strongest_score),
        "control_scores": {str(f): float(s) for f, s in control_pairs},
    }


# ── Observed outcomes (design memo sections 9-12) ────────────────────────────

def compute_observed_outcomes(reduced) -> Dict[str, Any]:
    """median_pss_by_k, pss_surfaces_by_k, attenuation_scores, gate, max_gap.

    Surfaces use integer DOY keys internally; run() stringifies for the
    payload. Raises CellOnePathology on any design-validity failure.
    """
    surfaces: Dict[int, Dict[int, float]] = {}
    for k in BUCKET_COUNTS:
        surfaces[k] = pss_surface(reduced, k)
        if len(surfaces[k]) != 365:
            raise CellOnePathology(
                "missing focal surface: k={} did not yield 365 anchors".format(k)
            )
    median_map: Dict[int, float] = {}
    for k in BUCKET_COUNTS:
        mk = median_pss(surfaces[k])
        if not np.isfinite(mk):
            raise CellOnePathology(
                "non-finite median_k for k={}".format(k)
            )
        median_map[k] = float(mk)
    attenuation = compute_attenuation_scores(median_map)
    for f, s in attenuation.items():
        if not np.isfinite(s):
            raise CellOnePathology(
                "non-finite attenuation score for focal {}".format(f)
            )
    gate = focal_elevation_gate_12(median_map)
    max_gap = compute_max_gap(attenuation)
    if not np.isfinite(max_gap["max_gap"]):
        raise CellOnePathology("non-finite max_gap")
    return {
        "median_pss_by_k": median_map,
        "pss_surfaces_by_k": surfaces,
        "attenuation_scores": attenuation,
        "focal_elevation_gate_12": gate,
        "max_gap": max_gap,
    }


# ── Fast vectorized surface for the permutation pool (forked) ────────────────

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
    """Vectorized 365-anchor surface median for a permuted is_long.

    Arithmetic mirrors influential_numbers_cell_1_pss.pss_long_share exactly:
    only l_p varies across permutations (n_p, total_k, share_pooled are
    permutation-invariant).
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


def _pool_core(
    reduced, n_perm: int, seed: int, stratified: bool
) -> Dict[str, np.ndarray]:
    """One shared is_long permutation pool -> attenuation_12 + max_gap nulls.

    stratified=False: unstratified pooled shuffle (section 13 primary).
    stratified=True : within-asset shuffle (section 16 diagnostic).
    The same permutation index underlies both returned arrays.
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

    dist_vectors = {f: distance_vector_for_focal(f) for f in FOCAL_CENTERS}
    windows = {f: window_for_focal(f) for f in FOCAL_CENTERS}

    rng = np.random.Generator(np.random.PCG64(seed))
    attn12 = np.empty(n_perm, dtype=np.float64)
    max_gap = np.empty(n_perm, dtype=np.float64)

    permuted = is_long_int.copy()
    if stratified:
        asset = np.asarray(reduced.asset)
        groups = [
            np.where(asset == a)[0]
            for a in sorted({str(x) for x in asset.tolist()})
        ]

    for i in range(n_perm):
        if stratified:
            for idx in groups:
                vals = permuted[idx]
                rng.shuffle(vals)
                permuted[idx] = vals
        else:
            rng.shuffle(permuted)

        median_map: Dict[int, float] = {}
        for k in BUCKET_COUNTS:
            flat_k, np_k, nr_k, nn_k = prep[k]
            median_map[k] = _median_surface_fast(
                permuted, flat_k, np_k, nr_k, nn_k, k, total_k, share_pooled
            )

        scores: Dict[int, float] = {}
        for f in FOCAL_CENTERS:
            y = np.asarray(
                [median_map[k] for k in windows[f]], dtype=np.float64
            )
            scores[f] = -ols_slope(dist_vectors[f], y)

        attn12[i] = scores[PRIMARY_FOCAL]
        strongest = max(scores[f] for f in CONTROL_FOCALS)
        max_gap[i] = scores[PRIMARY_FOCAL] - strongest

    return {
        "attenuation_score_12_null": attn12,
        "max_gap_null": max_gap,
    }


def run_shared_permutation_pool(
    reduced, n_perm: int, seed: int
) -> Dict[str, np.ndarray]:
    """Section 13 primary pool: unstratified pooled is_long shuffle."""
    return _pool_core(reduced, n_perm, seed, stratified=False)


# ── Beat counts and verdict (design memo sections 14-15) ─────────────────────

def compute_beat_counts(
    observed: Mapping[str, Any], perm_pool: Mapping[str, np.ndarray]
) -> Dict[str, int]:
    """Two strict-`<` beat counts (section 14); ties do not pass."""
    attn12_null = np.asarray(
        perm_pool["attenuation_score_12_null"], dtype=np.float64
    )
    maxgap_null = np.asarray(perm_pool["max_gap_null"], dtype=np.float64)
    obs_attn12 = float(observed["attenuation_scores"][PRIMARY_FOCAL])
    obs_maxgap = float(observed["max_gap"]["max_gap"])
    return {
        "beat_count_12_structure": int((attn12_null < obs_attn12).sum()),
        "beat_count_max_gap": int((maxgap_null < obs_maxgap).sum()),
    }


def evaluate_verdict(
    gate_result: Mapping[str, Any],
    beat_counts: Mapping[str, int],
    threshold: int = BEAT_COUNT_THRESHOLD,
    pathology: Optional[str] = None,
) -> Dict[str, Any]:
    """Four-class verdict map (section 15). Class 4 is pathology-only.

    A near-threshold beat count below the threshold is a fail routed to
    Class 3 (or Class 2 by the max_gap split), never Class 4.
    """
    gate_pass = bool(gate_result.get("pass", False))
    gate_ambiguous = bool(gate_result.get("ambiguous", False))

    bc12 = int(beat_counts.get("beat_count_12_structure", 0))
    bcmax = int(beat_counts.get("beat_count_max_gap", 0))
    bc12_pass = bc12 >= threshold
    bcmax_pass = bcmax >= threshold

    if pathology is not None or gate_ambiguous:
        machine = "class_4"
    elif gate_pass and bc12_pass and bcmax_pass:
        machine = "class_1"
    elif gate_pass and bc12_pass and (not bcmax_pass):
        machine = "class_2"
    else:
        # gate fails OR beat_count_12_structure < threshold (section 15.3)
        machine = "class_3"

    return {
        "verdict_class": _MACHINE_TO_DISPLAY[machine],
        "verdict_class_machine": machine,
        "verbalization": VERBALIZATION_BLOCKS[machine],
        "threshold_pass": {
            "beat_count_12_structure": bool(bc12_pass),
            "beat_count_max_gap": bool(bcmax_pass),
        },
        "pathology": pathology,
        "gate_ambiguous": gate_ambiguous,
    }


# ── Asset-stratified diagnostic (design memo section 16; non-verdict) ────────

def run_asset_stratified_diagnostic(
    reduced, n_perm: int, seed: int
) -> Dict[str, Any]:
    """Within-asset is_long shuffle. Diagnostic only; cannot alter the verdict."""
    pool = _pool_core(reduced, n_perm, seed, stratified=True)
    observed = compute_observed_outcomes(reduced)
    beat_counts = compute_beat_counts(observed, pool)
    return {
        "attenuation_score_12_null": [
            float(x) for x in pool["attenuation_score_12_null"].tolist()
        ],
        "max_gap_null": [
            float(x) for x in pool["max_gap_null"].tolist()
        ],
        "asset_stratified_beat_count_12_structure": int(
            beat_counts["beat_count_12_structure"]
        ),
        "asset_stratified_beat_count_max_gap": int(
            beat_counts["beat_count_max_gap"]
        ),
        "note": (
            "Diagnostic only (design memo section 16 / 21.5): cannot rescue, "
            "upgrade, alter, or convert generic smoothness into 12-centered "
            "structure."
        ),
    }


# ── Strict monotonic attenuation (secondary diagnostic; section 10) ──────────

def strict_monotonic_diagnostic(
    median_map: Mapping[int, float], focal: int
) -> Dict[str, Any]:
    """Per-side step-wise non-increase of median_k in |k - focal|.

    Secondary diagnostic only (design memo section 10): does not drive, alter,
    upgrade, or rescue any verdict.
    """
    win = window_for_focal(focal)
    try:
        m_focal = float(median_map[focal])
        left = [float(median_map[focal - r]) for r in range(1, WINDOW_RADIUS + 1)]
        right = [float(median_map[focal + r]) for r in range(1, WINDOW_RADIUS + 1)]
    except KeyError as exc:
        return {
            "focal": int(focal),
            "computable": False,
            "reason": "missing window member k={}".format(exc),
        }
    left_seq = [m_focal] + left   # increasing distance to the left
    right_seq = [m_focal] + right  # increasing distance to the right
    left_mono = all(
        left_seq[j] >= left_seq[j + 1] for j in range(len(left_seq) - 1)
    )
    right_mono = all(
        right_seq[j] >= right_seq[j + 1] for j in range(len(right_seq) - 1)
    )
    return {
        "focal": int(focal),
        "computable": True,
        "window": list(win),
        "left_non_increasing": bool(left_mono),
        "right_non_increasing": bool(right_mono),
        "strictly_monotonic_both_sides": bool(left_mono and right_mono),
        "note": "Secondary diagnostic only; cannot affect the verdict.",
    }


# ── Provenance gate against Candidate C (design memo section 17) ─────────────

def _file_sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def verify_candidate_c_provenance(
    pss_surfaces_by_k: Mapping[int, Mapping[int, float]],
    candidate_c_verdict_log_path: str,
    tolerance: float = PROVENANCE_TOLERANCE,
) -> Dict[str, Any]:
    """Validity gate (section 17), NOT a diagnostic. Failure routes to Class 4.

    Verifies the Candidate C verdict-log SHA-256, then compares Cell 1's
    recomputed k=10 and k=12 365-anchor surfaces to the stored
    protocol_payload.pss_surface_10 / pss_surface_12 (stringified DOY keys
    "1".."365") at <= tolerance per anchor, independently for each k. Returns
    a result dict with pass=False (never silently passes) on any failure.
    """
    result: Dict[str, Any] = {
        "pass": False,
        "max_abs_diff_10": None,
        "max_abs_diff_12": None,
        "n_anchors_checked_10": 0,
        "n_anchors_checked_12": 0,
        "tolerance": float(tolerance),
        "candidate_c_json_sha256": None,
        "expected_candidate_c_json_sha256": CANDIDATE_C_VERDICT_LOG_SHA256,
        "path": candidate_c_verdict_log_path,
        "failure_reason": None,
    }
    try:
        observed_sha = _file_sha256(candidate_c_verdict_log_path)
    except OSError as exc:
        result["failure_reason"] = "cannot read Candidate C verdict log: {}".format(
            exc
        )
        return result
    result["candidate_c_json_sha256"] = observed_sha
    if observed_sha != CANDIDATE_C_VERDICT_LOG_SHA256:
        result["failure_reason"] = (
            "Candidate C verdict-log SHA-256 mismatch: got {}, expected {}"
        ).format(observed_sha, CANDIDATE_C_VERDICT_LOG_SHA256)
        return result

    with open(candidate_c_verdict_log_path, "r", encoding="utf-8") as fh:
        c_log = json.load(fh)
    try:
        payload = c_log["protocol_payload"]
    except (KeyError, TypeError):
        result["failure_reason"] = "protocol_payload absent in Candidate C log"
        return result

    key_for_k = {10: C_SURFACE_JSON_KEYS[0], 12: C_SURFACE_JSON_KEYS[1]}
    diffs: Dict[int, float] = {}
    for k in (10, 12):
        json_key = key_for_k[k]
        if json_key not in payload:
            result["failure_reason"] = "{} absent in Candidate C log".format(
                json_key
            )
            return result
        c_surface = payload[json_key]
        if not isinstance(c_surface, dict) or len(c_surface) != 365:
            result["failure_reason"] = (
                "{} is not a 365-entry object".format(json_key)
            )
            return result
        try:
            cell_surface = pss_surfaces_by_k[k]
        except KeyError:
            result["failure_reason"] = (
                "Cell 1 surface for k={} missing".format(k)
            )
            return result
        max_abs = 0.0
        checked = 0
        for d in range(1, 366):
            skey = str(d)
            if skey not in c_surface:
                result["failure_reason"] = (
                    "{} missing DOY key {}".format(json_key, skey)
                )
                return result
            if d not in cell_surface:
                result["failure_reason"] = (
                    "Cell 1 k={} surface missing DOY {}".format(k, d)
                )
                return result
            diff = abs(float(cell_surface[d]) - float(c_surface[skey]))
            if not np.isfinite(diff):
                result["failure_reason"] = (
                    "non-finite difference at k={} DOY {}".format(k, d)
                )
                return result
            if diff > max_abs:
                max_abs = diff
            checked += 1
        diffs[k] = max_abs
        result["max_abs_diff_{}".format(k)] = float(max_abs)
        result["n_anchors_checked_{}".format(k)] = int(checked)

    passed = (diffs[10] <= tolerance) and (diffs[12] <= tolerance)
    result["pass"] = bool(passed)
    if not passed:
        result["failure_reason"] = (
            "surface divergence exceeds tolerance: "
            "max_abs_diff_10={}, max_abs_diff_12={}, tolerance={}"
        ).format(diffs[10], diffs[12], tolerance)
    return result


# ── Diagnostics bundle (non-verdict; design memo section 16) ─────────────────

def compute_diagnostics(reduced, observed: Mapping[str, Any]) -> Dict[str, Any]:
    """Non-verdict texture. Cannot rescue, upgrade, or alter the verdict."""
    median_map = observed["median_pss_by_k"]
    attenuation = observed["attenuation_scores"]
    max_gap = observed["max_gap"]
    monotonic = {
        str(f): strict_monotonic_diagnostic(median_map, f)
        for f in FOCAL_CENTERS
    }
    per_focal_window_medians = {
        str(f): {str(k): float(median_map[k]) for k in window_for_focal(f)}
        for f in FOCAL_CENTERS
    }
    return {
        "strict_monotonic_attenuation": monotonic,
        "per_focal_window_medians": per_focal_window_medians,
        "attenuation_scores": {
            str(f): float(s) for f, s in attenuation.items()
        },
        "control_focal_scores": {
            str(f): float(attenuation[f]) for f in CONTROL_FOCALS
        },
        "strongest_control_focal": int(max_gap["strongest_control_focal"]),
        "strongest_control_score": float(max_gap["strongest_control_score"]),
        "note": (
            "Diagnostics are non-verdict texture (design memo section 16 / "
            "21.5). The no-rescue rule is absolute."
        ),
    }


# ── Top-level run (deterministic payload only) ───────────────────────────────

def _stringify_surfaces(
    surfaces: Mapping[int, Mapping[int, float]]
) -> Dict[str, Dict[str, float]]:
    return {
        str(k): {str(d): float(v) for d, v in surf.items()}
        for k, surf in surfaces.items()
    }


def run(
    reduced,
    candidate_c_verdict_log_path: str = CANDIDATE_C_VERDICT_LOG_PATH,
    n_perm: int = N_PERM,
    label_perm_seed: int = LABEL_PERM_SEED_CELL1,
    asset_strat_seed: int = ASSET_STRAT_DIAG_SEED_CELL1,
    beat_count_threshold: int = BEAT_COUNT_THRESHOLD,
) -> Dict[str, Any]:
    """Top-level protocol invocation. Returns the JSON-serializable payload.

    Deterministic content only; volatile metadata belongs to the runner. On
    any design-validity / pathology condition (non-finite, degenerate
    variance, missing focal surface, provenance failure, exact gate
    ambiguity) the verdict is Class 4 and the run does not proceed to a
    confirmatory adjudication.
    """
    pathology: Optional[str] = None
    observed: Optional[Dict[str, Any]] = None
    try:
        observed = compute_observed_outcomes(reduced)
    except (CellOnePathology, DegenerateLongShareError, ValueError) as exc:
        pathology = "observed-outcome failure: {}".format(exc)

    if observed is not None:
        gate = observed["focal_elevation_gate_12"]
        surfaces = observed["pss_surfaces_by_k"]
        provenance = verify_candidate_c_provenance(
            surfaces, candidate_c_verdict_log_path, PROVENANCE_TOLERANCE
        )
        if not provenance["pass"] and pathology is None:
            pathology = "provenance failure: {}".format(
                provenance.get("failure_reason")
            )
    else:
        gate = {
            "pass": False,
            "median_12": None,
            "neighbor_mean": None,
            "focal_excess": None,
            "ambiguous": True,
            "ambiguity_reason": "observed outcomes not computable",
        }
        provenance = {
            "pass": False,
            "max_abs_diff_10": None,
            "max_abs_diff_12": None,
            "n_anchors_checked_10": 0,
            "n_anchors_checked_12": 0,
            "tolerance": float(PROVENANCE_TOLERANCE),
            "candidate_c_json_sha256": None,
            "expected_candidate_c_json_sha256": CANDIDATE_C_VERDICT_LOG_SHA256,
            "path": candidate_c_verdict_log_path,
            "failure_reason": "observed outcomes not computable",
        }

    run_pool = observed is not None and provenance["pass"]
    if run_pool:
        primary_pool = run_shared_permutation_pool(
            reduced, n_perm, label_perm_seed
        )
        beat_counts = compute_beat_counts(observed, primary_pool)
        attn12_null_full = [
            float(x) for x in primary_pool["attenuation_score_12_null"].tolist()
        ]
        max_gap_null_full = [
            float(x) for x in primary_pool["max_gap_null"].tolist()
        ]
        asset_strat = run_asset_stratified_diagnostic(
            reduced, n_perm, asset_strat_seed
        )
        diagnostics = compute_diagnostics(reduced, observed)
    else:
        beat_counts = {
            "beat_count_12_structure": 0,
            "beat_count_max_gap": 0,
        }
        attn12_null_full = []
        max_gap_null_full = []
        asset_strat = {
            "attenuation_score_12_null": [],
            "max_gap_null": [],
            "asset_stratified_beat_count_12_structure": 0,
            "asset_stratified_beat_count_max_gap": 0,
            "note": "not computed: Class 4 pathology halted the run",
        }
        diagnostics = (
            compute_diagnostics(reduced, observed)
            if observed is not None
            else {"note": "diagnostics not computable under pathology"}
        )

    verdict = evaluate_verdict(
        gate, beat_counts, beat_count_threshold, pathology=pathology
    )

    if observed is not None:
        observed_block = {
            "median_pss_by_k": {
                str(k): float(v)
                for k, v in observed["median_pss_by_k"].items()
            }
        }
        attenuation_block = {
            str(f): float(s)
            for f, s in observed["attenuation_scores"].items()
        }
        max_gap_block = observed["max_gap"]
        pss_surfaces_block = _stringify_surfaces(observed["pss_surfaces_by_k"])
    else:
        observed_block = {"median_pss_by_k": {}}
        attenuation_block = {}
        max_gap_block = {
            "max_gap": None,
            "score_12": None,
            "strongest_control_focal": None,
            "strongest_control_score": None,
            "control_scores": {},
        }
        pss_surfaces_block = {}

    diagnostics["provenance_check"] = provenance

    return {
        "active_memo_version": ACTIVE_MEMO_VERSION,
        "framework_memo_commit": FRAMEWORK_MEMO_COMMIT,
        "design_memo_commit": DESIGN_MEMO_COMMIT,
        "lock_acceptance_commit": LOCK_COMMIT,
        "freeze_commit": FREEZE_COMMIT,
        "n_trades": int(len(reduced)),
        "n_perm": int(n_perm),
        "anchor_population_size": 365,
        "bucket_counts": list(BUCKET_COUNTS),
        "focal_centers": list(FOCAL_CENTERS),
        "primary_focal": int(PRIMARY_FOCAL),
        "control_focals": list(CONTROL_FOCALS),
        "window_radius": int(WINDOW_RADIUS),
        "locked_parameters": {
            "anchor_month": 3,
            "anchor_day": 20,
            "focal_centers": list(FOCAL_CENTERS),
            "primary_focal": int(PRIMARY_FOCAL),
            "control_focals": list(CONTROL_FOCALS),
            "window_radius": int(WINDOW_RADIUS),
            "bucket_counts": list(BUCKET_COUNTS),
            "beat_count_threshold": int(beat_count_threshold),
            "provenance_tolerance": PROVENANCE_TOLERANCE,
        },
        "seeds": {
            "LABEL_PERM_SEED_CELL1": int(label_perm_seed),
            "ASSET_STRAT_DIAG_SEED_CELL1": int(asset_strat_seed),
            "N_PERM": int(n_perm),
        },
        "observed": observed_block,
        "focal_elevation_gate_12": gate,
        "attenuation_scores": attenuation_block,
        "max_gap": max_gap_block,
        "beat_counts": {k: int(v) for k, v in beat_counts.items()},
        "threshold_pass": verdict["threshold_pass"],
        "verdict_class": verdict["verdict_class"],
        "verdict_class_machine": verdict["verdict_class_machine"],
        "verbalization": verdict["verbalization"],
        "attenuation_score_12_null_full": attn12_null_full,
        "max_gap_null_full": max_gap_null_full,
        "pss_surfaces_by_k": pss_surfaces_block,
        "asset_stratified_diagnostic": asset_strat,
        "diagnostics": diagnostics,
        "provenance_check": provenance,
        "pathology": pathology,
    }
