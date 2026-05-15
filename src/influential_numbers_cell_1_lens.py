"""Influential Numbers Cell 1 parameterized annual-sector lens.

Locked design memo docs/influential_numbers_cell_1_design_memo_v0.1.md at
commit a765098 (section 7), lock-accepted at commit 3d44e9e. Forked from
src/candidate_c_lens.py (commit 4432591); the phase math is behavior-identical
to Candidate C so the section 17 provenance gate against Candidate C's stored
k = 10 and k = 12 365-anchor surfaces can reproduce them exactly.

phase = floor(days_since_start * bucket_count / cycle_length_days)

This module deliberately does NOT use the modulo operator. The lens is an
annual-sector partition, not a day-residue cycle. An automated grep gate test
in tests/test_influential_numbers_cell_1_lens.py asserts the absence of that
operator from this file. The gate scans non-comment code and string text
alike, so that character is kept out of docstrings too; the word "modulo" is
used instead.

Out-of-range phases abort the run loudly via PhaseRangeError; there is no
silent clamp. bucket_count is a required argument on every phase function;
there is deliberately no module-level bucket-count constant. Focal centers and
per-focal windows are protocol-level concepts (design memo section 8) and are
deliberately absent here; the lens only knows the bucket-count universe K.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import List, Tuple

MARCH20_ANCHOR_MONTH: int = 3
MARCH20_ANCHOR_DAY: int = 20
ANCHOR_DOY_MIN: int = 1
ANCHOR_DOY_MAX: int = 365


class PhaseRangeError(AssertionError):
    """Raised when an assigned phase escapes the locked 0..bucket_count-1 range."""


def _coerce_to_date(value) -> date:
    """Accept datetime.date or pandas.Timestamp; normalize to datetime.date."""
    if isinstance(value, date) and not hasattr(value, "hour"):
        return value
    if hasattr(value, "date") and callable(value.date):
        return value.date()
    if isinstance(value, date):
        return value
    raise TypeError(
        "entry_date must be datetime.date or pandas.Timestamp, got {}".format(
            type(value).__name__
        )
    )


def cycle_bounds_for(entry_date) -> Tuple[date, date]:
    """Locate the March-20 anchored annual cycle containing entry_date.

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


def _assert_phase_in_range(
    phase: int, bucket_count: int, entry_date, label: str
) -> None:
    if phase < 0 or phase > bucket_count - 1:
        raise PhaseRangeError(
            "{} produced phase {} out of range 0..{} for entry_date {}".format(
                label, phase, bucket_count - 1, entry_date
            )
        )


def assign_annual_sector_phase(entry_date, bucket_count: int) -> int:
    """Assign a bucket_count-phase annual-sector label, civil-date March-20 anchor.

    Design memo section 7.1. bucket_count is required. Returns an integer in
    0..bucket_count-1. Raises PhaseRangeError if the locked formula produces a
    value outside that range. There is no silent clamp.
    """
    d = _coerce_to_date(entry_date)
    cycle_start, cycle_end = cycle_bounds_for(d)
    cycle_length_days = (cycle_end - cycle_start).days
    days_since_start = (d - cycle_start).days
    phase = (days_since_start * bucket_count) // cycle_length_days
    _assert_phase_in_range(phase, bucket_count, d, "assign_annual_sector_phase")
    return int(phase)


def _anchor_date_in_year(year: int, anchor_doy: int) -> date:
    """Map an integer DOY 1..365 to a concrete date in year.

    Following the inherited Candidate B / Candidate C convention, date(year,
    1, 1) plus (anchor_doy - 1) days resolves leap days through standard
    datetime arithmetic; DOY 60 in a leap year lands on Feb 29.
    """
    return date(year, 1, 1) + timedelta(days=anchor_doy - 1)


def assign_anchor_shifted_phase(
    entry_date, anchor_doy: int, bucket_count: int
) -> int:
    """Assign a bucket_count-phase label with anchor swapped to integer DOY d.

    Design memo section 7.2. Same annual-sector formula; only the anchor
    changes. anchor_doy must be in 1..365 (inclusive). bucket_count is
    required.
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
    phase = (days_since_start * bucket_count) // cycle_length_days
    _assert_phase_in_range(phase, bucket_count, d, "assign_anchor_shifted_phase")
    return int(phase)


def enumerate_anchor_doys() -> List[int]:
    """Return the exhaustive integer-DOY anchor population [1, 2, ..., 365]."""
    return list(range(ANCHOR_DOY_MIN, ANCHOR_DOY_MAX + 1))


def enumerate_bucket_counts() -> Tuple[int, ...]:
    """Return the locked Cell 1 bucket-count universe K = {7, 8, ..., 19}.

    Design memo section 8 (Lock 3): the 13 distinct bucket counts spanned by
    the four focal windows W(10), W(12), W(14), W(16) with the +/-3 linear
    window. Cell 1 differs from Candidate C here: Candidate C enumerated the
    locked pair (12, 10); Cell 1 enumerates the full 13-element K. Focal
    centers and per-focal windows are protocol-level concepts, not lens
    concepts.
    """
    return tuple(range(7, 20))
