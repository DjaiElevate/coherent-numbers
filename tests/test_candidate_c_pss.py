"""Tests for Candidate C parameterized PSS (pss_long_share)."""

import numpy as np
import pytest

from candidate_c_pss import DegenerateLongShareError, pss_long_share


def test_max_separation_k12():
    is_long = np.array([1, 1, 0, 0])
    phase = np.array([0, 0, 6, 6])
    assert pss_long_share(is_long, phase, 12) == pytest.approx(1.0)


def test_max_separation_k10():
    is_long = np.array([1, 1, 0, 0])
    phase = np.array([0, 0, 5, 5])
    assert pss_long_share(is_long, phase, 10) == pytest.approx(1.0)


def test_no_separation_returns_zero_k12():
    is_long = np.array([1, 0, 1, 0])
    phase = np.array([0, 0, 7, 7])
    assert pss_long_share(is_long, phase, 12) == pytest.approx(0.0)


def test_no_separation_returns_zero_k10():
    is_long = np.array([1, 0, 1, 0])
    phase = np.array([0, 0, 9, 9])
    assert pss_long_share(is_long, phase, 10) == pytest.approx(0.0)


def test_all_long_aborts():
    with pytest.raises(DegenerateLongShareError):
        pss_long_share(np.array([1, 1, 1, 1]), np.array([0, 1, 2, 3]), 12)


def test_all_short_aborts():
    with pytest.raises(DegenerateLongShareError):
        pss_long_share(np.array([0, 0, 0]), np.array([0, 1, 2]), 10)


def test_empty_phase_contributes_zero():
    is_long = np.array([1, 1, 0, 0])
    phase = np.array([0, 0, 11, 11])  # phases 1..10 unoccupied
    val = pss_long_share(is_long, phase, 12)
    assert 0.0 <= val <= 1.0
    assert val == pytest.approx(1.0)


def test_bounds_random_k12():
    rng = np.random.Generator(np.random.PCG64(101))
    is_long = rng.integers(0, 2, size=400)
    phase = rng.integers(0, 12, size=400)
    v = pss_long_share(is_long, phase, 12)
    assert 0.0 <= v <= 1.0


def test_bounds_random_k10():
    rng = np.random.Generator(np.random.PCG64(202))
    is_long = rng.integers(0, 2, size=400)
    phase = rng.integers(0, 10, size=400)
    v = pss_long_share(is_long, phase, 10)
    assert 0.0 <= v <= 1.0


def _hand(is_long, phase, n_phases):
    return pss_long_share(np.array(is_long), np.array(phase), n_phases)


def test_hand_k12_case_a():
    # share_p=[1, .5, 0]; pooled=.5; total=.25; between=2/12; PSS=2/3
    v = _hand([1, 1, 1, 0, 0, 0], [0, 0, 1, 1, 2, 2], 12)
    assert v == pytest.approx(2.0 / 3.0)


def test_hand_k12_case_b():
    v = _hand([1, 1, 0, 0], [0, 0, 3, 3], 12)
    assert v == pytest.approx(1.0)


def test_hand_k12_case_c():
    # uniform: every phase share == pooled -> 0
    v = _hand([1, 0, 1, 0, 1, 0], [0, 0, 4, 4, 9, 9], 12)
    assert v == pytest.approx(0.0)


def test_hand_k10_case_a():
    v = _hand([1, 1, 1, 0, 0, 0], [0, 0, 1, 1, 2, 2], 10)
    assert v == pytest.approx(2.0 / 3.0)


def test_hand_k10_case_b():
    v = _hand([1, 1, 0, 0], [0, 0, 3, 3], 10)
    assert v == pytest.approx(1.0)


def test_hand_k10_case_c():
    v = _hand([1, 0, 1, 0, 1, 0], [0, 0, 4, 4, 8, 8], 10)
    assert v == pytest.approx(0.0)


def test_shape_reject_mismatched_lengths():
    with pytest.raises(ValueError):
        pss_long_share(np.array([1, 0]), np.array([0, 1, 2]), 12)


def test_empty_input_rejected():
    with pytest.raises(ValueError):
        pss_long_share(np.array([]), np.array([], dtype=np.int64), 12)


def test_n_phases_mismatch_rejected():
    # phase value 12 outside [0, 11] for n_phases=12
    with pytest.raises(ValueError):
        pss_long_share(np.array([1, 0, 1]), np.array([0, 1, 12]), 12)
    # phase value 10 outside [0, 9] for n_phases=10
    with pytest.raises(ValueError):
        pss_long_share(np.array([1, 0, 1]), np.array([0, 1, 10]), 10)


def test_rank_invariance_under_phase_preserving_relabel():
    rng = np.random.Generator(np.random.PCG64(7))
    is_long = rng.integers(0, 2, size=240)
    phase = rng.integers(0, 12, size=240)
    base = pss_long_share(is_long, phase, 12)
    # Relabel phases by a fixed permutation of phase ids; PSS is invariant
    # because it is a sum over phase groups.
    relabel = {p: (p + 5) % 12 for p in range(12)}
    phase2 = np.array([relabel[int(p)] for p in phase])
    assert pss_long_share(is_long, phase2, 12) == pytest.approx(base)
