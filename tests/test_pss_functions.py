"""Unit tests for Phase Structure Score (PSS) functions in harmonic_calendar.

Pre-registered definitions (v0.3.1 memo):
  PSS_in  = η²  = SS_between / SS_total
  PSS_oos = 1 - SS_residual_oos / SS_total_oos
"""

import math
import pytest
from harmonic_calendar import pss_in_sample, pss_out_of_sample


# ── pss_in_sample: η² correctness ────────────────────────────────────────────

def test_pss_in_sample_perfect_structure():
    # All variance lies between phases: η² == 1.0.
    # values=[1,1,3,3], phases=[0,0,1,1]
    # grand_mean=2, SS_total=4, SS_between=4 → η²=1.0
    result = pss_in_sample([1.0, 1.0, 3.0, 3.0], [0, 0, 1, 1])
    assert result == pytest.approx(1.0)


def test_pss_in_sample_no_structure():
    # All values in same phase: phase_mean == grand_mean → SS_between=0 → η²=0.
    result = pss_in_sample([1.0, 2.0, 3.0, 4.0], [0, 0, 0, 0])
    assert result == pytest.approx(0.0)


def test_pss_in_sample_partial_structure():
    # values=[1,2,3,4], phases=[0,0,1,1]
    # grand_mean=2.5, SS_total=5.0
    # phase0 mean=1.5, phase1 mean=3.5
    # SS_between = 2*(1.5-2.5)^2 + 2*(3.5-2.5)^2 = 2+2 = 4.0
    # η² = 4.0/5.0 = 0.8
    result = pss_in_sample([1.0, 2.0, 3.0, 4.0], [0, 0, 1, 1])
    assert result == pytest.approx(0.8)


def test_pss_in_sample_zero_variance_returns_0():
    # SS_total == 0 is degenerate → return 0.0.
    result = pss_in_sample([5.0, 5.0, 5.0], [0, 1, 2])
    assert result == pytest.approx(0.0)


def test_pss_in_sample_single_observation():
    # One observation → SS_total = 0 → return 0.0.
    result = pss_in_sample([7.0], [0])
    assert result == pytest.approx(0.0)


def test_pss_in_sample_result_in_unit_interval():
    # η² must always be in [0, 1].
    result = pss_in_sample([1.0, 4.0, 2.0, 9.0, 3.0], [0, 1, 0, 2, 1])
    assert 0.0 <= result <= 1.0


def test_pss_in_sample_whole_number_float_phases_accepted():
    # Float phases that are whole numbers are accepted and coerced to int.
    result = pss_in_sample([1.0, 1.0, 3.0, 3.0], [0.0, 0.0, 1.0, 1.0])
    assert result == pytest.approx(1.0)


# ── pss_out_of_sample: OOS R² correctness ────────────────────────────────────

def test_pss_oos_perfect_prediction():
    # Training phase means exactly predict test values → residual=0 → OOS=1.0.
    # train: phases=[0,0,1,1], values=[1,1,3,3] → phase_means={0:1, 1:3}, grand=2
    # test:  phases=[0,1],     values=[1,3]     → preds=[1,3], SS_res=0, SS_tot=2
    result = pss_out_of_sample(
        [1.0, 1.0, 3.0, 3.0], [0, 0, 1, 1],
        [1.0, 3.0], [0, 1],
    )
    assert result == pytest.approx(1.0)


def test_pss_oos_negative_skill():
    # Phase means anti-predict: worse than always guessing grand mean → OOS < 0.
    # train: grand=2, phase_means={0:1, 1:3}
    # test:  values=[3,1], phases=[0,1] → preds=[1,3]
    # SS_res=(3-1)^2+(1-3)^2=8, SS_tot=(3-2)^2+(1-2)^2=2 → OOS=1-4=-3.0
    result = pss_out_of_sample(
        [1.0, 1.0, 3.0, 3.0], [0, 0, 1, 1],
        [3.0, 1.0], [0, 1],
    )
    assert result == pytest.approx(-3.0)


def test_pss_oos_unseen_phase_uses_grand_mean():
    # Phase 99 absent from training → fallback to grand mean.
    # train: values=[2,2], phases=[0,0] → grand=2.0
    # test:  values=[2.0,2.0], phases=[99,99] → preds=[2,2]
    # SS_res=0, SS_tot=0 → degenerate case: both 0 → return 1.0
    result = pss_out_of_sample(
        [2.0, 2.0], [0, 0],
        [2.0, 2.0], [99, 99],
    )
    assert result == pytest.approx(1.0)


def test_pss_oos_partial_unseen_fallback():
    # Phase 0 known (mean=1), phase 99 unseen (falls back to grand=2).
    # train: values=[1,1,3,3], phases=[0,0,1,1] → grand=2, phase_means={0:1,1:3}
    # test:  values=[1.0, 2.0], phases=[0, 99]
    #   preds=[1.0, 2.0 (grand)]
    #   SS_res=(1-1)^2+(2-2)^2=0, SS_tot=(1-2)^2+(2-2)^2=1 → OOS=1.0
    result = pss_out_of_sample(
        [1.0, 1.0, 3.0, 3.0], [0, 0, 1, 1],
        [1.0, 2.0], [0, 99],
    )
    assert result == pytest.approx(1.0)


def test_pss_oos_degenerate_ss_total_zero_residual_zero():
    # SS_total_oos == 0 and SS_residual == 0 → return 1.0.
    # test values all equal grand_mean; unseen phase falls back to grand_mean.
    result = pss_out_of_sample(
        [1.0, 3.0], [0, 1],
        [2.0], [99],
    )
    assert result == pytest.approx(1.0)


def test_pss_oos_degenerate_ss_total_zero_residual_nonzero():
    # SS_total_oos == 0 but SS_residual > 0 → return -inf.
    # train: values=[1,3], phases=[0,1] → grand=2, phase_means={0:1, 1:3}
    # test:  values=[2.0], phases=[0] → pred=1.0 (not grand mean)
    # SS_tot=(2-2)^2=0, SS_res=(2-1)^2=1 → -inf
    result = pss_out_of_sample(
        [1.0, 3.0], [0, 1],
        [2.0], [0],
    )
    assert math.isinf(result) and result < 0


def test_pss_oos_allows_negative_values():
    # Confirm negative OOS is returned, not clamped.
    result = pss_out_of_sample(
        [1.0, 1.0, 3.0, 3.0], [0, 0, 1, 1],
        [3.0, 1.0], [0, 1],
    )
    assert result < 0


# ── Rejection: empty arrays ───────────────────────────────────────────────────

def test_pss_in_sample_rejects_empty_values():
    with pytest.raises(ValueError, match="empty"):
        pss_in_sample([], [])


def test_pss_in_sample_rejects_empty_phases():
    with pytest.raises(ValueError, match="empty"):
        pss_in_sample([1.0], [])


def test_pss_oos_rejects_empty_train_values():
    with pytest.raises(ValueError, match="empty"):
        pss_out_of_sample([], [], [1.0], [0])


def test_pss_oos_rejects_empty_test_values():
    with pytest.raises(ValueError, match="empty"):
        pss_out_of_sample([1.0], [0], [], [])


# ── Rejection: NaN and infinity ───────────────────────────────────────────────

def test_pss_in_sample_rejects_nan_in_values():
    with pytest.raises(ValueError, match="non-finite"):
        pss_in_sample([1.0, float("nan")], [0, 1])


def test_pss_in_sample_rejects_inf_in_values():
    with pytest.raises(ValueError, match="non-finite"):
        pss_in_sample([1.0, float("inf")], [0, 1])


def test_pss_in_sample_rejects_neg_inf_in_values():
    with pytest.raises(ValueError, match="non-finite"):
        pss_in_sample([float("-inf"), 1.0], [0, 1])


def test_pss_oos_rejects_nan_in_train_values():
    with pytest.raises(ValueError, match="non-finite"):
        pss_out_of_sample([1.0, float("nan")], [0, 1], [1.0], [0])


def test_pss_oos_rejects_nan_in_test_values():
    with pytest.raises(ValueError, match="non-finite"):
        pss_out_of_sample([1.0, 2.0], [0, 1], [float("nan")], [0])


def test_pss_oos_rejects_inf_in_test_values():
    with pytest.raises(ValueError, match="non-finite"):
        pss_out_of_sample([1.0, 2.0], [0, 1], [float("inf")], [0])


# ── Rejection: negative phase labels ─────────────────────────────────────────

def test_pss_in_sample_rejects_negative_phase():
    with pytest.raises(ValueError, match="negative"):
        pss_in_sample([1.0, 2.0, 3.0], [0, -1, 2])


def test_pss_oos_rejects_negative_train_phase():
    with pytest.raises(ValueError, match="negative"):
        pss_out_of_sample([1.0, 2.0], [0, -1], [1.0], [0])


def test_pss_oos_rejects_negative_test_phase():
    with pytest.raises(ValueError, match="negative"):
        pss_out_of_sample([1.0, 2.0], [0, 1], [1.0], [-1])


# ── Rejection: non-integer phase labels ──────────────────────────────────────

def test_pss_in_sample_rejects_non_integer_float_phase():
    # 1.9 is not a whole number → TypeError, not silent cast to 1.
    with pytest.raises(TypeError, match="non-integer"):
        pss_in_sample([1.0, 2.0, 3.0], [0, 1.9, 2])


def test_pss_in_sample_rejects_fractional_float():
    with pytest.raises(TypeError, match="non-integer"):
        pss_in_sample([1.0], [0.5])


def test_pss_oos_rejects_non_integer_train_phase():
    with pytest.raises(TypeError, match="non-integer"):
        pss_out_of_sample([1.0, 2.0], [0, 1.9], [1.0], [0])


def test_pss_oos_rejects_non_integer_test_phase():
    with pytest.raises(TypeError, match="non-integer"):
        pss_out_of_sample([1.0, 2.0], [0, 1], [1.0], [0.7])


# ── Rejection: mismatched lengths ────────────────────────────────────────────

def test_pss_in_sample_rejects_mismatched_lengths():
    with pytest.raises(ValueError, match="same length"):
        pss_in_sample([1.0, 2.0, 3.0], [0, 1])


def test_pss_oos_rejects_mismatched_train_lengths():
    with pytest.raises(ValueError, match="same length"):
        pss_out_of_sample([1.0, 2.0], [0], [1.0], [0])


def test_pss_oos_rejects_mismatched_test_lengths():
    with pytest.raises(ValueError, match="same length"):
        pss_out_of_sample([1.0, 2.0], [0, 1], [1.0, 2.0], [0])
