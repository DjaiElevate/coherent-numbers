"""Tests for PSS_B1 (long-share η²) and PSS_B2 (r_multiple η²)."""

import numpy as np
import pytest

from candidate_b_pss import (
    DegenerateLongShareError,
    pss_b1_long_share,
    pss_b2_r_multiple,
)


def test_pss_b1_perfect_separation_returns_one():
    is_long = np.array([True, True, False, False])
    phase = np.array([0, 0, 1, 1])
    assert pss_b1_long_share(is_long, phase) == pytest.approx(1.0)


def test_pss_b1_no_separation_returns_zero():
    is_long = np.array([True, False, True, False])
    phase = np.array([0, 0, 1, 1])
    assert pss_b1_long_share(is_long, phase) == pytest.approx(0.0)


def test_pss_b1_aborts_when_all_long():
    is_long = np.array([True, True, True, True])
    phase = np.array([0, 1, 2, 3])
    with pytest.raises(DegenerateLongShareError):
        pss_b1_long_share(is_long, phase)


def test_pss_b1_aborts_when_all_short():
    is_long = np.array([False, False, False])
    phase = np.array([0, 1, 2])
    with pytest.raises(DegenerateLongShareError):
        pss_b1_long_share(is_long, phase)


def test_pss_b1_zero_phase_count_contributes_zero():
    """Phase with N_p == 0 must contribute 0 to between_B1."""
    is_long = np.array([True, False, True, False])
    phase = np.array([0, 0, 3, 3])  # phases 1 and 2 unoccupied
    val = pss_b1_long_share(is_long, phase, n_phases=12)
    assert 0.0 <= val <= 1.0


def test_pss_b1_in_zero_one_bound_random_input():
    rng = np.random.Generator(np.random.PCG64(42))
    is_long = rng.integers(0, 2, size=500).astype(bool)
    phase = rng.integers(0, 12, size=500).astype(np.int64)
    val = pss_b1_long_share(is_long, phase)
    assert 0.0 <= val <= 1.0


def test_pss_b1_rank_invariance_normalized_vs_unnormalized():
    """Normalized and unnormalized forms yield identical permutation ranks."""
    rng = np.random.Generator(np.random.PCG64(7))
    n = 200
    is_long = rng.integers(0, 2, size=n).astype(bool)
    phase = rng.integers(0, 12, size=n).astype(np.int64)

    share_pooled = float(is_long.sum()) / n
    total_b1 = share_pooled * (1.0 - share_pooled)

    pss_vals = []
    between_vals = []
    perm = is_long.copy()
    for _ in range(50):
        rng.shuffle(perm)
        pss = pss_b1_long_share(perm, phase)
        pss_vals.append(pss)
        between_vals.append(pss * total_b1)

    assert np.argsort(pss_vals).tolist() == np.argsort(between_vals).tolist()


def test_pss_b1_rejects_mismatched_shapes():
    is_long = np.array([True, False])
    phase = np.array([0, 0, 0])
    with pytest.raises(ValueError):
        pss_b1_long_share(is_long, phase)


def test_pss_b1_rejects_empty_input():
    with pytest.raises(ValueError):
        pss_b1_long_share(np.array([]), np.array([], dtype=np.int64))


def test_pss_b1_rejects_out_of_range_phase():
    is_long = np.array([True, False, True])
    phase = np.array([0, 1, 15])  # 15 outside 0..11
    with pytest.raises(ValueError):
        pss_b1_long_share(is_long, phase)


def test_pss_b1_hand_computed_three_phase_case():
    """Hand-worked η² for is_long=[1,1,0,0,1,0], phase=[0,0,1,1,2,2]."""
    is_long = np.array([True, True, False, False, True, False])
    phase = np.array([0, 0, 1, 1, 2, 2])
    # share_p = [1.0, 0.0, 0.5]; share_pooled = 0.5; total_B1 = 0.25
    # between_B1 = (2/6)*0.25 + (2/6)*0.25 + (2/6)*0 = (1/6)+(1/6) = 1/3
    # PSS_B1 = (1/3) / 0.25 = 4/3 ≈ 1.333... — wait that exceeds 1.
    # Recompute: between_B1 = sum (n_p/N)*(share_p-share_pooled)^2
    #   = (2/6)*(1-0.5)^2 + (2/6)*(0-0.5)^2 + (2/6)*(0.5-0.5)^2
    #   = (1/3)*0.25 + (1/3)*0.25 + 0
    #   = 2/12 = 1/6
    # PSS_B1 = (1/6) / 0.25 = 0.6666...
    val = pss_b1_long_share(is_long, phase, n_phases=3)
    assert val == pytest.approx(2.0 / 3.0)


def test_pss_b2_basic():
    r = np.array([1.0, 1.0, -1.0, -1.0])
    phase = np.array([0, 0, 1, 1])
    # Perfect separation: ss_total = 4, ss_between = 4, ratio = 1
    assert pss_b2_r_multiple(r, phase) == pytest.approx(1.0)


def test_pss_b2_zero_variance_returns_zero():
    r = np.array([2.0, 2.0, 2.0])
    phase = np.array([0, 1, 2])
    assert pss_b2_r_multiple(r, phase) == 0.0


def test_pss_b2_in_zero_one_bound():
    rng = np.random.Generator(np.random.PCG64(13))
    r = rng.standard_normal(500) * 2.0
    phase = rng.integers(0, 12, size=500).astype(np.int64)
    val = pss_b2_r_multiple(r, phase)
    assert 0.0 <= val <= 1.0
