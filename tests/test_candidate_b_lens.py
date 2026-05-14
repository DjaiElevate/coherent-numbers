"""Tests for the Candidate B 12-phase March-20 annual-sector lens."""

from datetime import date, timedelta

import pytest

from candidate_b_lens import (
    ANCHOR_DOY_MAX,
    ANCHOR_DOY_MIN,
    BUCKET_COUNT,
    MARCH20_ANCHOR_DAY,
    MARCH20_ANCHOR_MONTH,
    PhaseRangeError,
    assign_anchor_shifted_phase,
    assign_annual_sector_phase,
    cycle_bounds_for,
    enumerate_anchor_doys,
)


def test_constants_match_locked_design():
    assert MARCH20_ANCHOR_MONTH == 3
    assert MARCH20_ANCHOR_DAY == 20
    assert BUCKET_COUNT == 12
    assert ANCHOR_DOY_MIN == 1
    assert ANCHOR_DOY_MAX == 365


def test_march_20_is_phase_0():
    for y in (2005, 2010, 2015, 2020, 2022):
        assert assign_annual_sector_phase(date(y, 3, 20)) == 0


def test_day_after_march_20_is_phase_0():
    assert assign_annual_sector_phase(date(2010, 3, 21)) == 0


def test_march_19_uses_previous_year_cycle_and_is_phase_11():
    assert assign_annual_sector_phase(date(2010, 3, 19)) == 11


def test_cycle_bounds_for_post_anchor_date():
    cs, ce = cycle_bounds_for(date(2010, 6, 15))
    assert cs == date(2010, 3, 20)
    assert ce == date(2011, 3, 20)


def test_cycle_bounds_for_pre_anchor_date():
    cs, ce = cycle_bounds_for(date(2010, 2, 15))
    assert cs == date(2009, 3, 20)
    assert ce == date(2010, 3, 20)


def test_every_in_cycle_day_yields_phase_in_range_leap_cycle():
    start = date(2007, 3, 20)
    end = date(2008, 3, 20)  # 366-day cycle (contains 2008-02-29)
    d = start
    while d < end:
        p = assign_annual_sector_phase(d)
        assert 0 <= p <= BUCKET_COUNT - 1
        d += timedelta(days=1)


def test_every_in_cycle_day_yields_phase_in_range_nonleap_cycle():
    start = date(2009, 3, 20)
    end = date(2010, 3, 20)  # 365-day cycle
    d = start
    while d < end:
        p = assign_annual_sector_phase(d)
        assert 0 <= p <= BUCKET_COUNT - 1
        d += timedelta(days=1)


def test_phase_is_monotone_within_a_cycle():
    """Phase is a non-decreasing step function within a cycle."""
    d = date(2010, 3, 20)
    prev = 0
    for offset in range(0, 365):
        cur = assign_annual_sector_phase(d + timedelta(days=offset))
        assert cur >= prev
        prev = cur


def test_phase_assignment_for_leap_february_29():
    # 2008-02-29 is in cycle 2007-03-20 .. 2008-03-20 (366 days),
    # days_since_start = 346, phase = floor(346*12/366) = 11.
    assert assign_annual_sector_phase(date(2008, 2, 29)) == 11


def test_phase_assignment_accepts_pandas_timestamp():
    import pandas as pd
    p = assign_annual_sector_phase(pd.Timestamp("2010-03-20"))
    assert p == 0


def test_phase_assignment_rejects_unsupported_type():
    with pytest.raises(TypeError):
        assign_annual_sector_phase("2010-03-20")  # str not accepted


def test_anchor_shifted_doy_1_jan_1_is_phase_0():
    assert assign_anchor_shifted_phase(date(2010, 1, 1), 1) == 0


def test_anchor_shifted_doy_79_close_to_march_20():
    # DOY 79 in non-leap year is March 20.
    assert assign_anchor_shifted_phase(date(2010, 3, 20), 79) == 0


def test_anchor_shifted_rejects_invalid_doy():
    with pytest.raises(ValueError):
        assign_anchor_shifted_phase(date(2010, 3, 20), 0)
    with pytest.raises(ValueError):
        assign_anchor_shifted_phase(date(2010, 3, 20), 366)
    with pytest.raises(ValueError):
        assign_anchor_shifted_phase(date(2010, 3, 20), -1)


def test_enumerate_anchor_doys_is_365_inclusive():
    result = enumerate_anchor_doys()
    assert result == list(range(1, 366))
    assert len(result) == 365
    assert 79 in result  # March-20 twin retained
    assert 60 in result  # Feb 29 / Mar 1 boundary
    assert 366 not in result  # February 29 is not a separate anchor


def test_phase_range_error_raised_when_cycle_bounds_force_overflow(monkeypatch):
    """If cycle_bounds_for is forced to return a 10-day cycle, an entry_date 30
    days later overflows to phase >= 12 and must abort, not silently clamp."""
    import candidate_b_lens

    def bad_cycle(entry_date):
        return (date(2010, 1, 1), date(2010, 1, 11))

    monkeypatch.setattr(candidate_b_lens, "cycle_bounds_for", bad_cycle)
    with pytest.raises(PhaseRangeError):
        candidate_b_lens.assign_annual_sector_phase(date(2010, 2, 1))


def test_no_modulo_operator_in_lens_module():
    """No `%` operator in non-comment code in candidate_b_lens.py."""
    import candidate_b_lens
    path = candidate_b_lens.__file__
    offenders = []
    with open(path, "r") as f:
        for lineno, line in enumerate(f, start=1):
            code = line.split("#", 1)[0]
            if "%" in code:
                offenders.append((lineno, line.rstrip()))
    assert not offenders, (
        "`%` operator found in non-comment code of candidate_b_lens.py: {!r}".format(
            offenders
        )
    )
