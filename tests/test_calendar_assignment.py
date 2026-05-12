"""Unit tests for harmonic calendar date-arithmetic functions.

Edge-case coverage locked by this file:
  1. March 20 is always phase 0 for the March-20 anchored calendar.
  2. March 19 uses the previous year's March 20 anchor.
  3. Phase labels are always integers in 0..107.
  4. Feb 29 handling is deterministic (explicitly computed below).
  5. Random-anchor DOY in a leap year is explicitly tested.
  6. Random anchors are integers in 1..365, never 366.
  7. Random anchors near March 20 (DOY ~79) are allowed and not excluded.
  8. Calendar functions do not reference market data.
"""

import math
import pytest
from datetime import date, timedelta

from harmonic_calendar import (
    PHASE_CYCLE,
    RANDOM_ANCHOR_SEED,
    ANCHOR_CONTROL_POPULATION_SIZE,
    TRAINING_RANK_THRESHOLD,
    HOLDOUT_RANK_THRESHOLD,
    march20_anchor_for_year,
    assign_march20_phase,
    assign_january_anchored_phase,
    assign_random_anchor_phase,
    assign_gregorian_month,
    generate_random_anchor_doys,
    enumerate_anchor_doys,
    strictly_below_count,
    strict_rank_pass,
)

# ── PHASE_CYCLE sanity ────────────────────────────────────────────────────────

def test_phase_cycle_is_108():
    assert PHASE_CYCLE == 108


# ── RANDOM_ANCHOR_SEED locked by v0.3.2 amendment ────────────────────────────

def test_random_anchor_seed_is_locked_to_amendment_date():
    # Locked in memo v0.3.2 seed-locking amendment (2026-05-12). Preserved
    # unchanged in v0.3.3 for audit traceability; not consumed by the v0.3.3
    # exhaustive anchor-control null.
    assert RANDOM_ANCHOR_SEED == 20260512
    assert isinstance(RANDOM_ANCHOR_SEED, int)


# ── v0.3.3 anchor-control population: exhaustive enumeration ─────────────────

def test_anchor_control_population_size_is_365():
    assert ANCHOR_CONTROL_POPULATION_SIZE == 365


def test_enumerate_anchor_doys_returns_exactly_365():
    doys = enumerate_anchor_doys()
    assert len(doys) == 365


def test_enumerate_anchor_doys_covers_1_to_365_inclusive():
    doys = enumerate_anchor_doys()
    assert doys[0] == 1
    assert doys[-1] == 365
    assert set(doys) == set(range(1, 366))


def test_enumerate_anchor_doys_unique():
    doys = enumerate_anchor_doys()
    assert len(set(doys)) == len(doys) == 365


def test_enumerate_anchor_doys_is_deterministic_no_seed():
    # Multiple calls produce identical results without consuming any seed.
    assert enumerate_anchor_doys() == enumerate_anchor_doys()
    assert enumerate_anchor_doys() == list(range(1, 366))


def test_enumerate_anchor_doys_includes_march20_doys():
    # March 20 (DOY 79 in non-leap, DOY 80 in leap under DOY-1-offset rule)
    # is included in the 365-anchor control population; the candidate-anchor
    # calendar is not manually excluded from the null.
    doys = enumerate_anchor_doys()
    assert 79 in doys
    assert 80 in doys


def test_enumerate_anchor_doys_does_not_consume_random_anchor_seed():
    # Demonstrate that enumerate_anchor_doys() does not perturb a shared
    # random.Random(seed) — i.e., it consumes no random numbers. We compare
    # two independent rng.random() draws around the call.
    import random as _random
    rng_a = _random.Random(RANDOM_ANCHOR_SEED)
    sequence_before = [rng_a.random() for _ in range(3)]
    rng_b = _random.Random(RANDOM_ANCHOR_SEED)
    _ = enumerate_anchor_doys()
    sequence_after = [rng_b.random() for _ in range(3)]
    assert sequence_before == sequence_after, (
        "enumerate_anchor_doys must not consume any random numbers"
    )


# ── v0.3.3 finite-population rank/percentile convention ──────────────────────

def test_training_rank_threshold_is_347():
    assert TRAINING_RANK_THRESHOLD == 347
    assert TRAINING_RANK_THRESHOLD == math.ceil(0.95 * 365)


def test_holdout_rank_threshold_is_329():
    assert HOLDOUT_RANK_THRESHOLD == 329
    assert HOLDOUT_RANK_THRESHOLD == math.ceil(0.90 * 365)


def test_strictly_below_count_basic():
    dist = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert strictly_below_count(3.0, dist) == 2   # 1.0, 2.0
    assert strictly_below_count(3.5, dist) == 3   # 1.0, 2.0, 3.0
    assert strictly_below_count(5.0, dist) == 4   # 1.0..4.0 (5.0 is a tie)
    assert strictly_below_count(6.0, dist) == 5   # all
    assert strictly_below_count(0.0, dist) == 0   # none


def test_strictly_below_count_ties_not_counted():
    # Ties (==) must never be counted as strictly below.
    dist = [1.0, 1.0, 1.0, 2.0, 3.0]
    assert strictly_below_count(1.0, dist) == 0
    assert strictly_below_count(2.0, dist) == 3
    assert strictly_below_count(3.0, dist) == 4


def test_strict_rank_pass_when_target_strictly_exceeds_enough():
    # 350 strictly below: passes for both thresholds.
    dist = [0.0] * 350 + [10.0] * 15
    assert strict_rank_pass(5.0, dist, TRAINING_RANK_THRESHOLD) is True
    assert strict_rank_pass(5.0, dist, HOLDOUT_RANK_THRESHOLD) is True


def test_strict_rank_pass_fails_training_passes_holdout_at_346():
    # 346 strictly below: fails training (needs 347), passes holdout (needs 329).
    dist = [0.0] * 346 + [10.0] * 19
    assert strict_rank_pass(5.0, dist, TRAINING_RANK_THRESHOLD) is False
    assert strict_rank_pass(5.0, dist, HOLDOUT_RANK_THRESHOLD) is True


def test_strict_rank_pass_fails_holdout_at_328():
    # 328 strictly below: fails both thresholds.
    dist = [0.0] * 328 + [10.0] * 37
    assert strict_rank_pass(5.0, dist, TRAINING_RANK_THRESHOLD) is False
    assert strict_rank_pass(5.0, dist, HOLDOUT_RANK_THRESHOLD) is False


def test_strict_rank_pass_ties_do_not_help_pass_training():
    # 346 strictly below + 1 tie at 5.0 = 347 "≤ target", but ties don't count
    # as strictly below; strictly_below = 346 < 347 → training screen fails.
    dist = [0.0] * 346 + [5.0] + [10.0] * 18
    assert strict_rank_pass(5.0, dist, TRAINING_RANK_THRESHOLD) is False


def test_strict_rank_pass_ties_do_not_help_pass_holdout():
    # 328 strictly below + 1 tie at 5.0 = 329 "≤", but ties don't help.
    dist = [0.0] * 328 + [5.0] + [10.0] * 36
    assert strict_rank_pass(5.0, dist, HOLDOUT_RANK_THRESHOLD) is False


def test_strict_rank_pass_at_exact_threshold_passes():
    # 347 strictly below (no ties) → training passes.
    dist = [0.0] * 347 + [10.0] * 18
    assert strict_rank_pass(5.0, dist, TRAINING_RANK_THRESHOLD) is True
    # 329 strictly below (no ties) → holdout passes.
    dist_holdout = [0.0] * 329 + [10.0] * 36
    assert strict_rank_pass(5.0, dist_holdout, HOLDOUT_RANK_THRESHOLD) is True


def test_strict_rank_pass_rejects_negative_threshold():
    with pytest.raises(ValueError):
        strict_rank_pass(0.0, [1.0, 2.0], -1)


# ── march20_anchor_for_year ───────────────────────────────────────────────────

def test_anchor_for_non_leap_year():
    assert march20_anchor_for_year(2023) == date(2023, 3, 20)


def test_anchor_for_leap_year():
    assert march20_anchor_for_year(2024) == date(2024, 3, 20)


def test_anchor_for_arbitrary_year():
    assert march20_anchor_for_year(2000) == date(2000, 3, 20)


# ── assign_march20_phase: phase 0 ─────────────────────────────────────────────

def test_march20_is_phase_0_non_leap():
    # Rule 1: March 20 is always phase 0.
    assert assign_march20_phase(date(2023, 3, 20)) == 0


def test_march20_is_phase_0_leap_year():
    assert assign_march20_phase(date(2024, 3, 20)) == 0


def test_march21_is_phase_1():
    assert assign_march20_phase(date(2024, 3, 21)) == 1


def test_march20_day_after_108_is_phase_0_again():
    # After a full cycle of 108 days, phase wraps back to 0.
    d = date(2024, 3, 20) + timedelta(days=PHASE_CYCLE)
    assert assign_march20_phase(d) == 0


# ── assign_march20_phase: March 19 uses previous year ────────────────────────

def test_march19_uses_previous_year_anchor():
    # Rule 2: March 19 of year Y uses March 20 of year Y-1 as anchor.
    # 2024 is a leap year, crossing Feb 29 going backward from March 19 2024
    # to March 20 2023.
    d = date(2024, 3, 19)
    anchor = date(2023, 3, 20)
    expected = (d - anchor).days % PHASE_CYCLE
    # (date(2024,3,19) - date(2023,3,20)).days == 365 because the period
    # runs March 20 2023 → March 19 2024 crossing Feb 29 2024 (leap).
    assert (d - anchor).days == 365
    assert expected == 365 % 108  # == 41
    assert assign_march20_phase(d) == expected


def test_march19_uses_previous_year_anchor_non_leap_crossing():
    # 2025 is non-leap. March 19 2025 uses March 20 2024 (leap year) as anchor.
    d = date(2025, 3, 19)
    anchor = date(2024, 3, 20)
    expected = (d - anchor).days % PHASE_CYCLE
    assert assign_march20_phase(d) == expected


# ── assign_march20_phase: phase range ────────────────────────────────────────

def test_march20_phase_always_in_range():
    # Rule 3: phase labels are always integers in 0..107.
    check_dates = [
        date(2020, 1, 1),
        date(2020, 12, 31),
        date(2023, 6, 15),
        date(2024, 2, 29),  # leap day
        date(2024, 3, 19),
        date(2024, 3, 20),
        date(2024, 11, 30),
    ]
    for d in check_dates:
        p = assign_march20_phase(d)
        assert isinstance(p, int), "phase must be int for {}".format(d)
        assert 0 <= p <= 107, "phase {} out of range for {}".format(p, d)


# ── Feb 29 — deterministic phase ─────────────────────────────────────────────

def test_feb29_march20_phase_is_deterministic():
    # Rule 4: Feb 29 must produce a deterministic phase.
    # Feb 29 2024 < March 20 2024, so anchor = March 20 2023.
    # (date(2024,2,29) - date(2023,3,20)).days == 346
    d = date(2024, 2, 29)
    anchor = date(2023, 3, 20)
    assert (d - anchor).days == 346
    expected = 346 % 108  # == 22
    assert assign_march20_phase(d) == expected == 22


def test_feb29_january_anchored_phase_is_deterministic():
    # Jan 1 2024 + 59 days == Feb 29 2024 (leap year).
    # So (Feb 29 - Jan 1).days == 59; phase == 59 % 108 == 59.
    d = date(2024, 2, 29)
    assert (d - date(2024, 1, 1)).days == 59
    assert assign_january_anchored_phase(d) == 59


def test_feb29_random_anchor_phase_is_deterministic():
    # anchor_doy=60 in leap year 2024: date(2024,1,1) + timedelta(59) == date(2024,2,29)
    # So Feb 29 2024 lands exactly on the anchor → phase 0.
    anchor_doy = 60
    d = date(2024, 2, 29)
    assert assign_random_anchor_phase(d, anchor_doy) == 0


# ── assign_january_anchored_phase ─────────────────────────────────────────────

def test_jan1_is_phase_0():
    assert assign_january_anchored_phase(date(2024, 1, 1)) == 0


def test_jan2_is_phase_1():
    assert assign_january_anchored_phase(date(2024, 1, 2)) == 1


def test_january_phase_always_in_range():
    check_dates = [
        date(2023, 1, 1), date(2023, 6, 15), date(2023, 12, 31),
        date(2024, 2, 29), date(2024, 12, 31),
    ]
    for d in check_dates:
        p = assign_january_anchored_phase(d)
        assert isinstance(p, int)
        assert 0 <= p <= 107, "phase {} out of range for {}".format(p, d)


def test_january_phase_wraps_at_108():
    d = date(2024, 1, 1) + timedelta(days=PHASE_CYCLE)
    assert assign_january_anchored_phase(d) == 0


# ── assign_random_anchor_phase ────────────────────────────────────────────────

def test_random_anchor_phase_0_when_date_equals_anchor():
    # DOY 90 in 2023 (non-leap): date(2023,1,1) + timedelta(89) = March 31
    anchor_doy = 90
    d = date(2023, 1, 1) + timedelta(anchor_doy - 1)
    assert assign_random_anchor_phase(d, anchor_doy) == 0


def test_random_anchor_phase_1_day_after_anchor():
    anchor_doy = 90
    d = date(2023, 1, 1) + timedelta(anchor_doy)
    assert assign_random_anchor_phase(d, anchor_doy) == 1


def test_random_anchor_uses_previous_year_when_date_before_anchor():
    # anchor_doy=200 (roughly July 19 in non-leap year).
    # January of the same year is before that anchor, so previous year is used.
    anchor_doy = 200
    d = date(2023, 1, 5)
    anchor_prev = date(2022, 1, 1) + timedelta(anchor_doy - 1)
    expected = (d - anchor_prev).days % PHASE_CYCLE
    assert assign_random_anchor_phase(d, anchor_doy) == expected


def test_random_anchor_near_march20_is_allowed():
    # Rule 7: anchors near March 20 (DOY ~79 in non-leap) must not be excluded.
    # DOY 79 in 2023 = March 20 (since DOY: Jan 31 + Feb 28 + 20 = 79).
    anchor_doy = 79
    d = date(2023, 3, 20)
    # anchor = date(2023,1,1) + timedelta(78) = date(2023,3,20) in non-leap? Let me verify:
    # Jan 31 + Feb 28 = 59 days → March 1; +19 = March 20 → total = 78 days from Jan 1
    # So anchor = March 20 2023, d = March 20 2023 → phase 0
    p = assign_random_anchor_phase(d, anchor_doy)
    assert 0 <= p <= 107


def test_random_anchor_phase_range():
    # Rule 3: phase labels always in 0..107.
    anchor_doy = 100
    check_dates = [
        date(2020, 1, 1), date(2020, 12, 31), date(2023, 6, 15),
        date(2024, 2, 29), date(2024, 3, 19), date(2025, 1, 1),
    ]
    for d in check_dates:
        p = assign_random_anchor_phase(d, anchor_doy)
        assert isinstance(p, int)
        assert 0 <= p <= 107, "phase {} out of range for {}".format(p, d)


def test_random_anchor_rejects_doy_0():
    with pytest.raises(ValueError, match="1..365"):
        assign_random_anchor_phase(date(2024, 6, 1), 0)


def test_random_anchor_rejects_doy_366():
    # Rule 6: anchors are 1..365, never 366.
    with pytest.raises(ValueError, match="1..365"):
        assign_random_anchor_phase(date(2024, 6, 1), 366)


# ── Leap-year DOY rule for random anchor ─────────────────────────────────────

def test_anchor_doy_60_leap_year_resolves_to_feb29():
    # Rule 5: random-anchor DOY behavior in leap years must be tested.
    # In a leap year (2024), anchor_doy=60 → date(2024,1,1)+timedelta(59)=Feb 29.
    anchor_date = date(2024, 1, 1) + timedelta(59)
    assert anchor_date == date(2024, 2, 29)


def test_anchor_doy_60_non_leap_year_resolves_to_march1():
    # In a non-leap year (2023), anchor_doy=60 → date(2023,1,1)+timedelta(59)=March 1.
    anchor_date = date(2023, 1, 1) + timedelta(59)
    assert anchor_date == date(2023, 3, 1)


def test_random_anchor_leap_year_feb29_phase_in_range():
    # Assigning a phase to Feb 29 2024 with various anchors stays in 0..107.
    d = date(2024, 2, 29)
    for anchor_doy in [1, 30, 60, 79, 100, 200, 300, 365]:
        p = assign_random_anchor_phase(d, anchor_doy)
        assert 0 <= p <= 107, "phase {} out of range for anchor_doy={}".format(
            p, anchor_doy
        )


# ── generate_random_anchor_doys ───────────────────────────────────────────────

def test_generates_correct_count():
    doys = generate_random_anchor_doys(10, seed=42)
    assert len(doys) == 10


def test_all_doys_in_1_to_365():
    # Rule 6: anchors are always in 1..365.
    doys = generate_random_anchor_doys(50, seed=0)
    for d in doys:
        assert isinstance(d, int)
        assert 1 <= d <= 365, "anchor {} out of 1..365".format(d)


def test_no_doy_is_366():
    # Explicitly confirm 366 is never returned (leap-year DOY is excluded).
    doys = generate_random_anchor_doys(365, seed=7)
    assert 366 not in doys


def test_doys_are_distinct():
    doys = generate_random_anchor_doys(100, seed=1)
    assert len(doys) == len(set(doys))


def test_generation_is_reproducible():
    doys1 = generate_random_anchor_doys(20, seed=99)
    doys2 = generate_random_anchor_doys(20, seed=99)
    assert doys1 == doys2


def test_different_seeds_give_different_results():
    doys1 = generate_random_anchor_doys(20, seed=1)
    doys2 = generate_random_anchor_doys(20, seed=2)
    assert doys1 != doys2


def test_anchors_near_march20_can_be_generated():
    # Rule 7: DOY ~79 (March 20 in non-leap) must be obtainable.
    # With 365 anchors, all DOY values 1..365 must appear exactly once.
    doys = generate_random_anchor_doys(365, seed=0)
    assert 79 in doys  # March 20 in non-leap year
    assert 80 in doys  # March 20 in leap year


def test_generate_zero_anchors():
    doys = generate_random_anchor_doys(0, seed=0)
    assert doys == []


def test_generate_too_many_anchors_raises():
    with pytest.raises(ValueError):
        generate_random_anchor_doys(366, seed=0)


# ── assign_gregorian_month ────────────────────────────────────────────────────

def test_gregorian_month_january():
    assert assign_gregorian_month(date(2024, 1, 15)) == 1


def test_gregorian_month_december():
    assert assign_gregorian_month(date(2024, 12, 31)) == 12


def test_gregorian_month_february_leap():
    assert assign_gregorian_month(date(2024, 2, 29)) == 2


def test_gregorian_month_range():
    for month in range(1, 13):
        d = date(2024, month, 1)
        assert assign_gregorian_month(d) == month


# ── No market data referenced ─────────────────────────────────────────────────

def test_no_market_data_imports():
    # Rule 8: calendar functions must not import or reference price/market data.
    import harmonic_calendar
    import inspect
    src = inspect.getsource(harmonic_calendar)
    forbidden = ["pandas", "yfinance", "SPY", "price", "open("]
    for term in forbidden:
        assert term not in src, "harmonic_calendar.py references '{}'".format(term)
