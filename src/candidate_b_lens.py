"""Candidate B calendar lens — 12-phase March-20 annual-sector partition.

Implements section 7.1 of the locked Candidate B design memo
(docs/candidate_b_design_memo_v0.1.md, ratified at lock-acceptance 159cccd):

  phase = floor( days_since_start * 12 / cycle_length_days )

This module deliberately does NOT use the modulo operator. The lens is an
annual-sector partition, not a day-residue cycle. An automated grep test
in tests/test_candidate_b_lens.py asserts the absence of that operator from
non-comment code in this file.

Out-of-range phases must abort the run loudly — they cannot occur for valid
in-cycle entry dates and would indicate a bug elsewhere. A silent clamp is
forbidden.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import List, Tuple

MARCH20_ANCHOR_MONTH: int = 3
MARCH20_ANCHOR_DAY: int = 20
BUCKET_COUNT: int = 12
ANCHOR_DOY_MIN: int = 1
ANCHOR_DOY_MAX: int = 365


class PhaseRangeError(AssertionError):
    """Raised when an assigned phase escapes the locked 0..BUCKET_COUNT-1 range."""


def _coerce_to_date(value) -> date:
    """Accept datetime.date or pandas.Timestamp; normalize to datetime.date."""
    if isinstance(value, date) and not hasattr(value, "hour"):
        return value
    if hasattr(value, "date") and callable(value.date):
        return value.date()
    if isinstance(value, date):
        return value
    raise TypeError(
        "entry_date must be datetime.date or pandas.Timestamp, got {!r}".format(
            type(value).__name__
        )
    )


def cycle_bounds_for(entry_date) -> Tuple[date, date]:
    """Locate the March-20 anchored annual cycle containing *entry_date*.

    Returns (cycle_start, cycle_end) where cycle_start is March 20 of the
    appropriate year and cycle_end is March 20 of the year after that. The
    cycle is half-open: [cycle_start, cycle_end).
    """
    d = _coerce_to_date(entry_date)
    march20_this_year = date(d.year, MARCH20_ANCHOR_MONTH, MARCH20_ANCHOR_DAY)
    if d >= march20_this_year:
        cycle_start = march20_this_year
    else:
        cycle_start = date(d.year - 1, MARCH20_ANCHOR_MONTH, MARCH20_ANCHOR_DAY)
    cycle_end = date(cycle_start.year + 1, MARCH20_ANCHOR_MONTH, MARCH20_ANCHOR_DAY)
    return cycle_start, cycle_end


def _assert_phase_in_range(phase: int, entry_date, label: str) -> None:
    if phase < 0 or phase > BUCKET_COUNT - 1:
        raise PhaseRangeError(
            "{} produced phase {} out of range 0..{} for entry_date {}".format(
                label, phase, BUCKET_COUNT - 1, entry_date
            )
        )


def assign_annual_sector_phase(entry_date) -> int:
    """Assign a 12-phase annual-sector label anchored at March 20.

    Locked design memo section 7.1. Returns an integer in 0..11. Raises
    PhaseRangeError if the locked formula produces a value outside that
    range. There is no silent clamp.
    """
    d = _coerce_to_date(entry_date)
    cycle_start, cycle_end = cycle_bounds_for(d)
    cycle_length_days = (cycle_end - cycle_start).days
    days_since_start = (d - cycle_start).days
    phase = (days_since_start * BUCKET_COUNT) // cycle_length_days
    _assert_phase_in_range(phase, d, "assign_annual_sector_phase")
    return int(phase)


def _anchor_date_in_year(year: int, anchor_doy: int) -> date:
    """Map an integer DOY 1..365 to a concrete date in *year*.

    Following the prior-cell convention, date(year, 1, 1) + (anchor_doy - 1)
    days resolves leap days through standard datetime arithmetic.
    """
    return date(year, 1, 1) + timedelta(days=anchor_doy - 1)


def assign_anchor_shifted_phase(entry_date, anchor_doy: int) -> int:
    """Assign a 12-phase annual-sector label with anchor swapped to DOY d.

    Implements section 10.2 of the locked design memo. The same annual-sector
    formula is used; only the anchor changes. anchor_doy must be in 1..365
    (inclusive); February 29 is not a separate anchor.
    """
    if not (ANCHOR_DOY_MIN <= anchor_doy <= ANCHOR_DOY_MAX):
        raise ValueError(
            "anchor_doy must be in {}..{}, got {}".format(
                ANCHOR_DOY_MIN, ANCHOR_DOY_MAX, anchor_doy
            )
        )
    d = _coerce_to_date(entry_date)
    anchor_this_year = _anchor_date_in_year(d.year, anchor_doy)
    if d >= anchor_this_year:
        cycle_start = anchor_this_year
    else:
        cycle_start = _anchor_date_in_year(d.year - 1, anchor_doy)
    cycle_end = _anchor_date_in_year(cycle_start.year + 1, anchor_doy)
    cycle_length_days = (cycle_end - cycle_start).days
    days_since_start = (d - cycle_start).days
    phase = (days_since_start * BUCKET_COUNT) // cycle_length_days
    _assert_phase_in_range(phase, d, "assign_anchor_shifted_phase")
    return int(phase)


def enumerate_anchor_doys() -> List[int]:
    """Return the exhaustive integer-DOY anchor population [1, 2, ..., 365].

    February 29 is not enumerated as a separate anchor; leap years still
    affect cycle_length_days through the annual-sector formula. This follows
    the prior-cell finite-control convention (v0.3.1 / v0.3.3).
    """
    return list(range(ANCHOR_DOY_MIN, ANCHOR_DOY_MAX + 1))
