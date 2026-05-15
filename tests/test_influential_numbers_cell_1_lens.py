"""Tests for the Influential Numbers Cell 1 lens.

Mirrors tests/test_candidate_c_lens.py (commit 4432591), adapted to the
Cell 1 bucket-count universe K = {7, ..., 19} and the no-percent grep gate.
Synthetic dates only; no frozen CSV is read.
"""

import os
import sys
from datetime import date

from pathlib import Path

import pytest

REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

import influential_numbers_cell_1_lens as lens

LENS_FILE = os.path.join(
    REPO_ROOT, "src", "influential_numbers_cell_1_lens.py"
)


# ── Constants ────────────────────────────────────────────────────────────────

def test_constants():
    assert lens.MARCH20_ANCHOR_MONTH == 3
    assert lens.MARCH20_ANCHOR_DAY == 20
    assert lens.ANCHOR_DOY_MIN == 1
    assert lens.ANCHOR_DOY_MAX == 365


def test_no_module_level_bucket_count_constant():
    # bucket_count must be a required argument, never a module constant.
    for bad in ("BUCKET_COUNT", "BUCKET_COUNTS", "K", "N_PHASES"):
        assert not hasattr(lens, bad), bad


def test_enumerate_anchor_doys():
    doys = lens.enumerate_anchor_doys()
    assert doys == list(range(1, 366))
    assert len(doys) == 365


def test_enumerate_bucket_counts_is_K_7_to_19():
    assert lens.enumerate_bucket_counts() == tuple(range(7, 20))
    assert lens.enumerate_bucket_counts() == (
        7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
    )


# ── bucket_count is required ─────────────────────────────────────────────────

def test_bucket_count_required_annual():
    with pytest.raises(TypeError):
        lens.assign_annual_sector_phase(date(2010, 6, 1))  # noqa


def test_bucket_count_required_anchor_shifted():
    with pytest.raises(TypeError):
        lens.assign_anchor_shifted_phase(date(2010, 6, 1), 100)  # noqa


# ── phase 0 and phase k-1 for representative k ───────────────────────────────

@pytest.mark.parametrize("k", [7, 12, 19])
def test_phase_zero_at_cycle_start(k):
    # March 20 is the civil anchor: cycle start -> phase 0.
    assert lens.assign_annual_sector_phase(date(2011, 3, 20), k) == 0


@pytest.mark.parametrize("k", [7, 12, 19])
def test_phase_k_minus_1_near_cycle_end(k):
    # The day before the next March 20 is in the last phase.
    p = lens.assign_annual_sector_phase(date(2012, 3, 19), k)
    assert p == k - 1


@pytest.mark.parametrize("k", [7, 12, 19])
def test_phase_in_range_full_cycle(k):
    d = date(2011, 3, 20)
    for _ in range(366):
        p = lens.assign_annual_sector_phase(d, k)
        assert 0 <= p <= k - 1
        d = date.fromordinal(d.toordinal() + 1)


# ── cycle bounds, non-leap and leap ──────────────────────────────────────────

def test_cycle_bounds_non_leap():
    s, e = lens.cycle_bounds_for(date(2011, 6, 1))
    assert s == date(2011, 3, 20)
    assert e == date(2012, 3, 20)
    assert (e - s).days == 366  # 2011-03-20 .. 2012-03-20 traverses 2012 leap?


def test_cycle_bounds_before_anchor():
    s, e = lens.cycle_bounds_for(date(2011, 1, 5))
    assert s == date(2010, 3, 20)
    assert e == date(2011, 3, 20)


# ── leap conventions ─────────────────────────────────────────────────────────

def test_doy_60_leap_year_is_feb_29():
    assert lens._anchor_date_in_year(2020, 60) == date(2020, 2, 29)


def test_doy_60_non_leap_is_mar_1():
    assert lens._anchor_date_in_year(2019, 60) == date(2019, 3, 1)


def test_civil_march20_doy_79_nonleap_80_leap():
    assert lens._anchor_date_in_year(2019, 79) == date(2019, 3, 20)
    assert lens._anchor_date_in_year(2020, 80) == date(2020, 3, 20)


def test_doy79_sweep_march20_nonleap_march19_leap():
    assert lens._anchor_date_in_year(2019, 79) == date(2019, 3, 20)
    assert lens._anchor_date_in_year(2020, 79) == date(2020, 3, 19)


# ── type coercion ────────────────────────────────────────────────────────────

def test_pandas_timestamp_accepted():
    pd = pytest.importorskip("pandas")
    ts = pd.Timestamp("2012-07-04")
    assert lens.assign_annual_sector_phase(ts, 12) == \
        lens.assign_annual_sector_phase(date(2012, 7, 4), 12)


def test_non_date_type_rejected():
    with pytest.raises(TypeError):
        lens.assign_annual_sector_phase("2012-07-04", 12)


# ── anchor-shifted validation ────────────────────────────────────────────────

@pytest.mark.parametrize("bad", [0, -1, 366, 999])
def test_anchor_doy_out_of_range_rejected(bad):
    with pytest.raises(ValueError):
        lens.assign_anchor_shifted_phase(date(2012, 7, 4), bad, 12)


def test_anchor_shifted_doy1_jan1_phase0():
    for k in (7, 12, 19):
        assert lens.assign_anchor_shifted_phase(date(2012, 1, 1), 1, k) == 0


# ── PhaseRangeError on forced overflow ───────────────────────────────────────

def test_phase_range_error_on_forced_overflow(monkeypatch):
    # Force a degenerate one-day cycle so the floor-division phase exceeds
    # k - 1; the lens must raise PhaseRangeError, never silently clamp.
    def _tiny_cycle(_entry):
        return date(2011, 3, 20), date(2011, 3, 21)

    monkeypatch.setattr(lens, "cycle_bounds_for", _tiny_cycle)
    with pytest.raises(lens.PhaseRangeError):
        lens.assign_annual_sector_phase(date(2011, 9, 1), 12)


# ── no-percent grep gate (design memo section 7) ─────────────────────────────

def test_no_percent_character_anywhere_in_lens_module():
    text = open(LENS_FILE, encoding="utf-8").read()
    assert "%" not in text, (
        "the percent character must not appear anywhere in the Cell 1 lens "
        "module (code, comments, or docstrings); use the word 'modulo'"
    )
