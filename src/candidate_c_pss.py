"""Candidate C parameterized PSS (design memo 401ce45, section 9.1).

    between_k = sum_p (N_p / N_total) * (share_p - share_pooled) ** 2
    total_k   = share_pooled * (1 - share_pooled)
    PSS_k     = between_k / total_k

eta-squared / correlation-ratio form for the binary outcome is_long, the
same functional family as Candidate B section 9.1 generalized over an
explicit bucket count. total_k = 0 (pooled all-long or all-short marginal)
aborts via DegenerateLongShareError; no fallback. n_phases is a required
argument; no default. Candidate C has no r_multiple PSS variant.

The between-sum expression is kept bit-identical to Candidate B's
candidate_b_pss.pss_b1_long_share so the section 11.6 provenance check
against B's stored k = 12 surface compares like for like.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np


class DegenerateLongShareError(RuntimeError):
    """Raised when total_k = 0 and PSS_k is undefined."""


def _coerce_bool_array(is_long: Sequence) -> np.ndarray:
    arr = np.asarray(is_long)
    if arr.dtype == np.bool_:
        return arr
    return arr.astype(bool)


def _coerce_phase_array(phase: Sequence) -> np.ndarray:
    return np.asarray(phase, dtype=np.int64)


def pss_long_share(is_long, phase, n_phases: int) -> float:
    """eta-squared phase-conditional long-share dispersion.

    Returns a float in [0, 1] when total_k > 0. Raises
    DegenerateLongShareError when total_k == 0.
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
    if (phase_arr < 0).any() or (phase_arr >= n_phases).any():
        raise ValueError(
            "phase values must be in 0..{}, got min={} max={}".format(
                n_phases - 1, int(phase_arr.min()), int(phase_arr.max())
            )
        )

    n_total = is_long_arr.size
    is_long_int = is_long_arr.astype(np.int64)

    n_p = np.bincount(phase_arr, minlength=n_phases).astype(np.float64)
    l_p = np.bincount(
        phase_arr, weights=is_long_int, minlength=n_phases
    ).astype(np.float64)

    share_pooled = float(is_long_int.sum()) / float(n_total)
    total_k = share_pooled * (1.0 - share_pooled)
    if total_k == 0.0:
        raise DegenerateLongShareError(
            "total_k = 0 (share_pooled = {}); allocation heterogeneity "
            "undefined".format(share_pooled)
        )

    with np.errstate(divide="ignore", invalid="ignore"):
        share_p = np.where(n_p > 0, l_p / n_p, 0.0)
    weights = n_p / float(n_total)
    between_k = float(
        ((share_p - share_pooled) ** 2 * weights * (n_p > 0)).sum()
    )
    return between_k / total_k
