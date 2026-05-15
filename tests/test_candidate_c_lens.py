"""Tests for the Candidate C parameterized annual-sector lens."""

from datetime import date, timedelta

import pytest

import candidate_c_lens as lens
from candidate_c_lens import (
    ANCHOR_DOY_MAX,
    ANCHOR_DOY_MIN,
    MARCH20_ANCHOR_DAY,
    MARCH20_ANCHOR_MONTH,
    PhaseRangeError,
    assign_anchor_shifted_phase,
    assign_annual_sector_phase,
    cycle_bounds_for,
    enumerate_anchor_doys,
    enumerate_bucket_counts,
)


def test_constants():
    assert MARCH20_ANCHOR_MONTH == 3
    assert MARCH20_ANCHOR_DAY == 20
    assert ANCHOR_DOY_MIN == 1
    assert ANCHOR_DOY_MAX == 365


def test_no_module_level_bucket_count_constant():
    assert not hasattr(lens, "BUCKET_COUNT")


def test_enumerate_anchor_doys():
    doys = enumerate_anchor_doys()
    assert doys == list(range(1, 366))
    assert len(doys) == 365


def test_enumerate_bucket_counts():
    assert enumerate_bucket_counts() == (12, 10)


def test_phase_0_for_both_k():
    assert assign_annual_sector_phase(date(2021, 3, 20), 12) == 0
    assert assign_annual_sector_phase(date(2021, 3, 20), 10) == 0


def test_phase_k_minus_1_for_both_k():
    # March 19 of the following year is the last in-cycle day (non-leap cycle).
    assert assign_annual_sector_phase(date(2022, 3, 19), 12) == 11
    assert assign_annual_sector_phase(date(2022, 3, 19), 10) == 9


def test_cycle_bounds_non_leap_year():
    cs, ce = cycle_bounds_for(date(2021, 6, 1))
    assert cs == date(2021, 3, 20)
    assert ce == date(2022, 3, 20)
    assert (ce - cs).days == 365


def test_cycle_bounds_leap_cycle():
    # Cycle 2019-03-20 .. 2020-03-20 traverses Feb 29 2020 -> 366 days.
    cs, ce = cycle_bounds_for(date(2020, 1, 15))
    assert cs == date(2019, 3, 20)
    assert ce == date(2020, 3, 20)
    assert (ce - cs).days == 366


def test_monotone_within_cycle_k12():
    d = date(2021, 3, 20)
    prev = 0
    for off in range(0, 365):
        cur = assign_annual_sector_phase(d + timedelta(days=off), 12)
        assert cur >= prev
        prev = cur
    assert 0 <= prev <= 11


def test_monotone_within_cycle_k10():
    d = date(2021, 3, 20)
    prev = 0
    for off in range(0, 365):
        cur = assign_annual_sector_phase(d + timedelta(days=off), 10)
        assert cur >= prev
        prev = cur
    assert 0 <= prev <= 9


def test_doy_60_leap_year_is_feb_29():
    # Section 7.3 inherited convention.
    assert lens._anchor_date_in_year(2020, 60) == date(2020, 2, 29)
    assert lens._anchor_date_in_year(2021, 60) == date(2021, 3, 1)


def test_civil_march20_doy_equivalent_79_nonleap_80_leap():
    # Section 7.4: civil March 20 is DOY 79 in non-leap, 80 in leap years.
    assert date(2021, 3, 20).timetuple().tm_yday == 79
    assert date(2020, 3, 20).timetuple().tm_yday == 80


def test_doy79_sweep_is_march20_nonleap_march19_leap():
    assert lens._anchor_date_in_year(2021, 79) == date(2021, 3, 20)
    assert lens._anchor_date_in_year(2020, 79) == date(2020, 3, 19)


def test_pandas_timestamp_accepted():
    import pandas as pd

    assert assign_annual_sector_phase(pd.Timestamp("2021-03-20"), 12) == 0
    assert assign_anchor_shifted_phase(pd.Timestamp("2021-03-20"), 79, 12) == 0


def test_non_date_type_rejected():
    with pytest.raises(TypeError):
        assign_annual_sector_phase("2021-03-20", 12)


def test_anchor_shifted_doy1_jan1_phase0_both_k():
    assert assign_anchor_shifted_phase(date(2021, 1, 1), 1, 12) == 0
    assert assign_anchor_shifted_phase(date(2021, 1, 1), 1, 10) == 0


def test_anchor_shifted_boundaries_k12():
    # anchor DOY 1 (Jan 1), non-leap 2021 cycle length 365; Dec 31 -> day 364.
    assert assign_anchor_shifted_phase(date(2021, 12, 31), 1, 12) == 11


def test_anchor_shifted_boundaries_k10():
    assert assign_anchor_shifted_phase(date(2021, 12, 31), 1, 10) == 9


def test_anchor_shifted_rejects_invalid_doy():
    with pytest.raises(ValueError):
        assign_anchor_shifted_phase(date(2021, 3, 20), 0, 12)
    with pytest.raises(ValueError):
        assign_anchor_shifted_phase(date(2021, 3, 20), 366, 12)


def test_phase_range_error_on_forced_overflow(monkeypatch):
    def bad_bounds(entry_date):
        return (date(2021, 1, 1), date(2021, 1, 11))  # 10-day cycle

    monkeypatch.setattr(lens, "cycle_bounds_for", bad_bounds)
    with pytest.raises(PhaseRangeError):
        lens.assign_annual_sector_phase(date(2021, 2, 1), 12)


def test_bucket_count_is_required_annual():
    with pytest.raises(TypeError):
        assign_annual_sector_phase(date(2021, 3, 20))  # missing bucket_count


def test_bucket_count_is_required_anchor_shifted():
    with pytest.raises(TypeError):
        assign_anchor_shifted_phase(date(2021, 3, 20), 79)  # missing bucket_count


def test_phase_in_range_full_leap_cycle_k12():
    d = date(2019, 3, 20)
    while d < date(2020, 3, 20):
        assert 0 <= assign_annual_sector_phase(d, 12) <= 11
        d += timedelta(days=1)


def test_phase_in_range_full_leap_cycle_k10():
    d = date(2019, 3, 20)
    while d < date(2020, 3, 20):
        assert 0 <= assign_annual_sector_phase(d, 10) <= 9
        d += timedelta(days=1)


def test_no_modulo_operator_in_lens_module():
    """No percent-sign operator in non-comment code in src/candidate_c_lens.py."""
    path = lens.__file__
    offenders = []
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            code = line.split("#", 1)[0]
            if chr(37) in code:  # chr(37) is the percent sign
                offenders.append((lineno, line.rstrip()))
    assert not offenders, (
        "percent-sign operator found in non-comment code of "
        "src/candidate_c_lens.py: {}".format(offenders)
    )
