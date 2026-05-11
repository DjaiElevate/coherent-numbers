"""Harmonic calendar phase assignment and Phase Structure Score (PSS) functions.

Phase labels are integers in 0..107 (PHASE_CYCLE = 108 distinct values).
Phase arithmetic: phase = (date - anchor_date).days % PHASE_CYCLE.

PSS statistics (pre-registered in docs/harmonic_calendar_design_memo_v0.3.1.md):
  PSS_in  = η²  = SS_between / SS_total
  PSS_oos = 1 - SS_residual_oos / SS_total_oos

RUN_ANALYSIS = False  # Guard: no protocol execution yet.
"""

import math
import random
from datetime import date, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple

RUN_ANALYSIS = False

PHASE_CYCLE = 108  # 0..107 inclusive


# ── March-20 anchor calendar ──────────────────────────────────────────────────

def march20_anchor_for_year(year: int) -> date:
    """Return March 20 of *year* as the harmonic-year anchor."""
    return date(year, 3, 20)


def assign_march20_phase(d: date) -> int:
    """Assign phase 0..107 relative to the nearest past March 20.

    March 20 is always phase 0.
    Dates before March 20 of their calendar year use the previous year's anchor,
    so March 19 of year Y is (date(Y,3,19) - date(Y-1,3,20)).days % 108.
    Feb 29 in a leap year is handled by standard datetime subtraction; no
    special-case adjustment is applied.
    """
    if d >= march20_anchor_for_year(d.year):
        anchor = march20_anchor_for_year(d.year)
    else:
        anchor = march20_anchor_for_year(d.year - 1)
    return (d - anchor).days % PHASE_CYCLE


# ── January-1 anchor calendar ─────────────────────────────────────────────────

def assign_january_anchored_phase(d: date) -> int:
    """Assign phase 0..107 counting from January 1 of the same year.

    Jan 1 is always phase 0. Feb 29 in a leap year is handled by standard
    datetime subtraction ((date - Jan 1).days == 59 for Feb 29), so its phase
    is 59 % 108 == 59. No special-case adjustment is applied.
    """
    anchor = date(d.year, 1, 1)
    return (d - anchor).days % PHASE_CYCLE


# ── Random DOY anchor calendar ────────────────────────────────────────────────

def _anchor_date_for_doy(year: int, anchor_doy: int) -> date:
    """Convert a 1..365 DOY anchor to a concrete date in *year*.

    Leap-year rule: date(year, 1, 1) + timedelta(anchor_doy - 1) is used
    directly. In a leap year anchor_doy==60 resolves to Feb 29; in a
    non-leap year it resolves to March 1. No further adjustment is made.
    """
    return date(year, 1, 1) + timedelta(days=anchor_doy - 1)


def assign_random_anchor_phase(d: date, anchor_doy: int) -> int:
    """Assign phase 0..107 relative to an integer DOY anchor.

    anchor_doy must be in 1..365 (inclusive; never 366).
    The anchor date is date(year, 1, 1) + timedelta(anchor_doy - 1) for the
    appropriate year. If *d* falls before that anchor within its calendar year,
    the previous year's anchor is used instead.

    Leap-year rule for anchor construction: see _anchor_date_for_doy.
    Feb 29 as an input date is computed by normal datetime subtraction; no
    special-case adjustment is applied.
    Anchors near DOY 79 (≈ March 20) are allowed and not excluded.
    """
    if not (1 <= anchor_doy <= 365):
        raise ValueError(
            "anchor_doy must be in 1..365 (inclusive), got {}".format(anchor_doy)
        )
    anchor = _anchor_date_for_doy(d.year, anchor_doy)
    if d < anchor:
        anchor = _anchor_date_for_doy(d.year - 1, anchor_doy)
    return (d - anchor).days % PHASE_CYCLE


def assign_gregorian_month(d: date) -> int:
    """Return the Gregorian month number 1..12."""
    return d.month


def generate_random_anchor_doys(n_anchors: int, seed: int) -> List[int]:
    """Return *n_anchors* distinct random DOY integers sampled from 1..365.

    Anchors are always in the 365-day DOY space (never 366), regardless of
    whether any particular year is a leap year.
    Anchors near DOY 79 (≈ March 20) are allowed and not excluded.
    Uses *seed* for full reproducibility.
    Raises ValueError when n_anchors > 365.
    """
    if n_anchors < 0:
        raise ValueError("n_anchors must be non-negative, got {}".format(n_anchors))
    if n_anchors > 365:
        raise ValueError(
            "Cannot draw {} distinct anchors from 1..365".format(n_anchors)
        )
    rng = random.Random(seed)
    return rng.sample(range(1, 366), n_anchors)


# ── PSS (Phase Structure Score) ───────────────────────────────────────────────
#
# Pre-registered definitions (v0.3.1 memo):
#
#   PSS_in  = η²  = SS_between / SS_total
#
#     SS_total   = Σ (value_i - grand_mean)²
#     SS_between = Σ_phase  n_phase * (phase_mean - grand_mean)²
#
#   PSS_oos = 1 - SS_residual_oos / SS_total_oos
#
#     For each OOS observation, prediction = training phase mean for that phase,
#     or training grand mean when the phase was absent from training data.
#     SS_residual_oos = Σ (actual - prediction)²
#     SS_total_oos    = Σ (actual - training_grand_mean)²
#
#     Negative values are allowed (skill worse than grand-mean baseline).
#     Degenerate case: SS_total_oos == 0 → return 1.0 if residual == 0,
#                                           else return -inf.

def _validate_values_phases(
    values: object, phases: object, label: str
) -> Tuple[List[float], List[int]]:
    """Validate and coerce value/phase iterables for PSS functions.

    Rules enforced (ValueError or TypeError on violation):
    - Neither array may be empty.
    - Both arrays must have equal length.
    - values must be finite (no NaN, no ±inf).
    - phases must be non-negative integers; float phases whose fractional part
      is non-zero (e.g. 1.9) are rejected rather than silently truncated;
      whole-number floats like 1.0 are accepted and converted to int.
    """
    values_list = list(values)
    phases_list = list(phases)

    if len(values_list) == 0:
        raise ValueError("{} values array is empty".format(label))
    if len(phases_list) == 0:
        raise ValueError("{} phases array is empty".format(label))
    if len(values_list) != len(phases_list):
        raise ValueError(
            "{} values and phases must have the same length ({} vs {})".format(
                label, len(values_list), len(phases_list)
            )
        )

    coerced_values: List[float] = []
    for v in values_list:
        fv = float(v)
        if not math.isfinite(fv):
            raise ValueError(
                "{} values contain non-finite entry {!r}".format(label, v)
            )
        coerced_values.append(fv)

    coerced_phases: List[int] = []
    for p in phases_list:
        if isinstance(p, bool):
            raise TypeError("{} phases must be int, got bool".format(label))
        if isinstance(p, float):
            if p != math.floor(p):
                raise TypeError(
                    "{} phases contain non-integer float {!r}; "
                    "coercion is not allowed".format(label, p)
                )
            coerced_phases.append(int(p))
        elif isinstance(p, int):
            coerced_phases.append(p)
        else:
            raise TypeError(
                "{} phases must be int or whole-number float, got {!r}".format(
                    label, type(p).__name__
                )
            )
        if coerced_phases[-1] < 0:
            raise ValueError(
                "{} phases contain negative value {}".format(label, coerced_phases[-1])
            )

    return coerced_values, coerced_phases


def _phase_stats(values: List[float], phases: List[int]) -> Tuple[float, Dict[int, float]]:
    """Return (grand_mean, {phase: phase_mean}) for a validated dataset."""
    grand_mean = sum(values) / len(values)
    sums: Dict[int, float] = defaultdict(float)
    counts: Dict[int, int] = defaultdict(int)
    for p, v in zip(phases, values):
        sums[p] += v
        counts[p] += 1
    phase_means = {p: sums[p] / counts[p] for p in sums}
    return grand_mean, phase_means


def pss_in_sample(values: object, phase_labels: object) -> float:
    """Phase Structure Score (in-sample): η² = SS_between / SS_total.

    Measures how much of the total variance in *values* is explained by
    phase group membership. Range: 0.0 .. 1.0.

    Returns 0.0 when SS_total == 0 (zero-variance input is degenerate).

    Raises ValueError for empty arrays, non-finite values, or negative phases.
    Raises TypeError for non-integer or non-whole-number float phases.
    """
    vals, phases = _validate_values_phases(values, phase_labels, "in-sample")

    grand_mean, phase_means = _phase_stats(vals, phases)

    ss_total = sum((v - grand_mean) ** 2 for v in vals)
    if ss_total == 0.0:
        return 0.0

    counts: Dict[int, int] = defaultdict(int)
    for p in phases:
        counts[p] += 1

    ss_between = sum(
        counts[p] * (phase_means[p] - grand_mean) ** 2
        for p in phase_means
    )

    return ss_between / ss_total


def pss_out_of_sample(
    train_values: object,
    train_phases: object,
    test_values: object,
    test_phases: object,
) -> float:
    """Phase Structure Score (out-of-sample): 1 - SS_residual_oos / SS_total_oos.

    For each holdout observation, the prediction is the training phase mean for
    that phase. If the phase was absent from training data, the training grand
    mean is used as the fallback prediction.

    Negative values are allowed (model worse than predicting training grand mean).

    Degenerate case: if SS_total_oos == 0, returns 1.0 when SS_residual_oos is
    also 0, and -inf otherwise.

    Raises ValueError for empty arrays, non-finite values, or negative phases.
    Raises TypeError for non-integer or non-whole-number float phases.
    """
    tr_vals, tr_phases = _validate_values_phases(train_values, train_phases, "train")
    te_vals, te_phases = _validate_values_phases(test_values, test_phases, "test")

    grand_mean, phase_means = _phase_stats(tr_vals, tr_phases)

    ss_residual = 0.0
    ss_total_oos = 0.0
    for p, v in zip(te_phases, te_vals):
        pred = phase_means.get(p, grand_mean)
        ss_residual += (v - pred) ** 2
        ss_total_oos += (v - grand_mean) ** 2

    if ss_total_oos == 0.0:
        return 1.0 if ss_residual == 0.0 else float("-inf")

    return 1.0 - ss_residual / ss_total_oos
