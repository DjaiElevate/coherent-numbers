"""Phase Structure Score (PSS) for Candidate B.

Implements section 9.1 of the locked design memo:

    between_B1 = Σ_p ( N_p / N_total ) × ( share_p − share_pooled )²
    total_B1   = share_pooled × ( 1 − share_pooled )
    PSS_B1     = between_B1 / total_B1

PSS_B1 is the η² / correlation-ratio form of phase-conditional dispersion
for a binary outcome (`is_long`). If `total_B1 == 0` (degenerate pooled
marginal — all longs or all shorts), the run aborts. No fallback estimand.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np


class DegenerateLongShareError(RuntimeError):
    """Raised when total_B1 = 0 and PSS_B1 is undefined."""


def _coerce_bool_array(is_long: Sequence) -> np.ndarray:
    arr = np.asarray(is_long)
    if arr.dtype == np.bool_:
        return arr
    return arr.astype(bool)


def _coerce_phase_array(phase: Sequence) -> np.ndarray:
    return np.asarray(phase, dtype=np.int64)


def pss_b1_long_share(is_long, phase, n_phases: int = 12) -> float:
    """η²-form phase-conditional long-share dispersion (primary outcome).

    Returns a float in [0, 1] when total_B1 > 0. Raises
    DegenerateLongShareError when total_B1 == 0.
    """
    is_long_arr = _coerce_bool_array(is_long)
    phase_arr = _coerce_phase_array(phase)

    if is_long_arr.shape != phase_arr.shape:
        raise ValueError(
            "is_long and phase must have matching shape: {} vs {}".format(
                is_long_arr.shape, phase_arr.shape
            )
        )
    if is_long_arr.size == 0:
        raise ValueError("empty input arrays")

    n_total = is_long_arr.size
    is_long_int = is_long_arr.astype(np.int64)

    if (phase_arr < 0).any() or (phase_arr >= n_phases).any():
        raise ValueError(
            "phase values must be in 0..{}, got min={} max={}".format(
                n_phases - 1, int(phase_arr.min()), int(phase_arr.max())
            )
        )

    n_p = np.bincount(phase_arr, minlength=n_phases).astype(np.float64)
    l_p = np.bincount(phase_arr, weights=is_long_int, minlength=n_phases).astype(np.float64)

    share_pooled = float(is_long_int.sum()) / float(n_total)
    total_b1 = share_pooled * (1.0 - share_pooled)

    if total_b1 == 0.0:
        raise DegenerateLongShareError(
            "total_B1 = 0 (share_pooled = {}); allocation heterogeneity undefined".format(
                share_pooled
            )
        )

    with np.errstate(divide="ignore", invalid="ignore"):
        share_p = np.where(n_p > 0, l_p / n_p, 0.0)
    weights = n_p / float(n_total)
    between_b1 = float(((share_p - share_pooled) ** 2 * weights * (n_p > 0)).sum())

    return between_b1 / total_b1


def pss_b2_r_multiple(r_multiple, phase, n_phases: int = 12) -> float:
    """η²-form phase-conditional r_multiple dispersion (secondary diagnostic).

    Returns 0.0 in the degenerate ss_total == 0 case (diagnostic-only path,
    no abort). Raises ValueError for malformed inputs.
    """
    r_arr = np.asarray(r_multiple, dtype=np.float64)
    phase_arr = _coerce_phase_array(phase)

    if r_arr.shape != phase_arr.shape:
        raise ValueError("r_multiple and phase must have matching shape")
    if r_arr.size == 0:
        raise ValueError("empty input arrays")
    if (phase_arr < 0).any() or (phase_arr >= n_phases).any():
        raise ValueError(
            "phase values must be in 0..{}, got min={} max={}".format(
                n_phases - 1, int(phase_arr.min()), int(phase_arr.max())
            )
        )

    grand_mean = float(r_arr.mean())
    ss_total = float(((r_arr - grand_mean) ** 2).sum())
    if ss_total == 0.0:
        return 0.0

    ss_between = 0.0
    for p in range(n_phases):
        mask = phase_arr == p
        n_p = int(mask.sum())
        if n_p == 0:
            continue
        phase_mean = float(r_arr[mask].mean())
        ss_between += n_p * (phase_mean - grand_mean) ** 2

    return ss_between / ss_total
