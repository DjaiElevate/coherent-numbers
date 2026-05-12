"""Synthetic-data tests for the v0.3.3 harmonic calendar protocol orchestration.

These tests deliberately do NOT:
  - read the frozen SPY CSV
  - call spy_loader.load_spy() on the frozen CSV
  - assign phases to real SPY data
  - compute real-data PSS
  - run the locked verdict protocol

They verify the orchestration logic (verdict rule, secondary-diagnostics gate,
exhaustive 365-anchor enumeration, strict-rank pass/fail, runner-script
integrity) on small toy data.
"""

import inspect
import math
import os
import re
from datetime import date, timedelta

import pandas as pd
import pytest

import harmonic_calendar_protocol as hcp
import harmonic_calendar
import spy_loader

from harmonic_calendar import (
    PHASE_CYCLE,
    RANDOM_ANCHOR_SEED,
    ANCHOR_CONTROL_POPULATION_SIZE,
    TRAINING_RANK_THRESHOLD,
    HOLDOUT_RANK_THRESHOLD,
    assign_march20_phase,
)
from harmonic_calendar_protocol import (
    ACTIVE_MEMO_VERSION,
    FDR_Q,
    OUTCOMES,
    _benjamini_hochberg,
    _strict_percentile,
    compute_secondary_diagnostics,
    evaluate_outcome_verdict,
    run_protocol,
)


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNNER_PATH = os.path.join(REPO_ROOT, "scripts", "run_harmonic_calendar_protocol.py")


# ── Module-level constants are exactly the locked protocol's ─────────────────

def test_outcomes_are_log_return_and_squared_log_return():
    assert OUTCOMES == ("log_return", "log_return_sq")


def test_anchor_control_population_size_is_365():
    # v0.3.3 fixed control: exhaustive enumeration of 365 integer-DOY anchors.
    assert ANCHOR_CONTROL_POPULATION_SIZE == 365


def test_training_rank_threshold_is_347():
    assert TRAINING_RANK_THRESHOLD == 347


def test_holdout_rank_threshold_is_329():
    assert HOLDOUT_RANK_THRESHOLD == 329


def test_fdr_q_is_0_05():
    assert FDR_Q == 0.05


def test_active_memo_version_is_v0_3_3():
    assert ACTIVE_MEMO_VERSION == "v0.3.3"


def test_random_anchor_seed_is_20260512_preserved():
    # Preserved from v0.3.2 for audit traceability; not consumed by v0.3.3.
    assert RANDOM_ANCHOR_SEED == 20260512


# ── _strict_percentile (v0.3.3 strict-rank convention) ───────────────────────

def test_strict_percentile_basic_below():
    # target below everything: 0/3 = 0.0
    assert _strict_percentile([1.0, 2.0, 3.0], -10.0) == 0.0


def test_strict_percentile_basic_above():
    # target above everything: 3/3 = 1.0
    assert _strict_percentile([1.0, 2.0, 3.0], 999.0) == 1.0


def test_strict_percentile_tied_value_not_counted():
    # Ties never count: target equals one element → strictly_below = 2/4
    assert _strict_percentile([1.0, 2.0, 3.0, 4.0], 3.0) == pytest.approx(0.5)


def test_strict_percentile_empty_raises():
    with pytest.raises(ValueError, match="empty"):
        _strict_percentile([], 1.0)


# ── _benjamini_hochberg ──────────────────────────────────────────────────────

def test_benjamini_hochberg_empty():
    assert _benjamini_hochberg([]) == []


def test_benjamini_hochberg_all_zero_rejects_all():
    # All p=0: all rejected at any q > 0.
    result = _benjamini_hochberg([0.0, 0.0, 0.0], q=0.05)
    assert result == [True, True, True]


def test_benjamini_hochberg_all_ones_rejects_none():
    # All p=1: none rejected.
    result = _benjamini_hochberg([1.0, 1.0, 1.0], q=0.05)
    assert result == [False, False, False]


def test_benjamini_hochberg_classic_example():
    # Classic BH: p = [0.01, 0.04, 0.03, 0.005], q=0.05, m=4
    # sorted: [0.005, 0.01, 0.03, 0.04] thresholds: [0.0125, 0.025, 0.0375, 0.05]
    # below: [True, True, True, True] → all 4 rejected.
    result = _benjamini_hochberg([0.01, 0.04, 0.03, 0.005], q=0.05)
    assert result == [True, True, True, True]


def test_benjamini_hochberg_step_up_handles_gap():
    # sorted p=[0.001, 0.5, 0.5, 0.5] thresholds at q=0.05, m=4: [0.0125, 0.025, 0.0375, 0.05]
    # below: [True, False, False, False] → max_idx=0 → reject only the smallest.
    result = _benjamini_hochberg([0.5, 0.001, 0.5, 0.5], q=0.05)
    assert result == [False, True, False, False]


# ── evaluate_outcome_verdict — v0.3.3 rank-based verdict rule ────────────────
#
# Synthetic gate tests use a small synthetic anchor population (10 values)
# with explicit small rank thresholds, exercising the same strict-rank
# convention used in production with 365 anchors and thresholds (347, 329).

def _null_pop_10():
    # 10-value anchor-control population: [0.0, 0.1, ..., 0.9]
    return [i / 10.0 for i in range(10)]


def test_verdict_pass_when_all_three_gates_clear():
    info = evaluate_outcome_verdict(
        march20_pss_in=1.0,       # strictly beats all 10
        march20_pss_oos=1.0,      # strictly beats all 10, > 0
        anchor_pss_in=_null_pop_10(),
        anchor_pss_oos=_null_pop_10(),
        gregorian_pss_oos=0.1,
        january_pss_oos=0.2,
        training_rank_threshold=10,   # needs all 10 below
        holdout_rank_threshold=9,     # needs ≥ 9 below
    )
    assert info["training_screen_pass"] is True
    assert info["holdout_primary_pass"] is True
    assert info["holdout_auxiliary_pass"] is True
    assert info["verdict"] == "pass"


def test_verdict_null_when_training_screen_fails():
    info = evaluate_outcome_verdict(
        march20_pss_in=0.4,       # only 4 strictly below → < threshold 5
        march20_pss_oos=1.0,
        anchor_pss_in=_null_pop_10(),
        anchor_pss_oos=_null_pop_10(),
        gregorian_pss_oos=0.1,
        january_pss_oos=0.2,
        training_rank_threshold=5,
        holdout_rank_threshold=5,
    )
    assert info["training_screen_pass"] is False
    assert info["verdict"] == "null"


def test_verdict_null_when_holdout_rank_gate_fails():
    info = evaluate_outcome_verdict(
        march20_pss_in=1.0,
        march20_pss_oos=0.4,      # 4 strictly below < threshold 5
        anchor_pss_in=_null_pop_10(),
        anchor_pss_oos=_null_pop_10(),
        gregorian_pss_oos=0.1,
        january_pss_oos=0.2,
        training_rank_threshold=5,
        holdout_rank_threshold=5,
    )
    assert info["holdout_pct_pass"] is False
    assert info["verdict"] == "null"


def test_verdict_null_when_holdout_oos_not_positive():
    # Rank gate could clear, but absolute-positivity must also hold.
    # All anchor values negative; march20 = -0.05 strictly beats most, but not > 0.
    info = evaluate_outcome_verdict(
        march20_pss_in=1.0,
        march20_pss_oos=-0.05,
        anchor_pss_in=_null_pop_10(),
        anchor_pss_oos=[-1.0 + i / 10.0 for i in range(10)],  # -1.0 .. -0.1
        gregorian_pss_oos=-0.5,
        january_pss_oos=-0.5,
        training_rank_threshold=10,
        holdout_rank_threshold=10,
    )
    assert info["holdout_pct_pass"] is True
    assert info["holdout_positive_pass"] is False
    assert info["holdout_primary_pass"] is False
    assert info["verdict"] == "null"


def test_verdict_null_when_auxiliary_fails_via_gregorian():
    info = evaluate_outcome_verdict(
        march20_pss_in=1.0,
        march20_pss_oos=1.0,
        anchor_pss_in=_null_pop_10(),
        anchor_pss_oos=_null_pop_10(),
        gregorian_pss_oos=2.0,
        january_pss_oos=0.2,
        training_rank_threshold=10,
        holdout_rank_threshold=10,
    )
    assert info["control_comparison_pass_gregorian"] is False
    assert info["holdout_auxiliary_pass"] is False
    assert info["verdict"] == "null"


def test_verdict_null_when_auxiliary_fails_via_january():
    info = evaluate_outcome_verdict(
        march20_pss_in=1.0,
        march20_pss_oos=1.0,
        anchor_pss_in=_null_pop_10(),
        anchor_pss_oos=_null_pop_10(),
        gregorian_pss_oos=0.1,
        january_pss_oos=2.0,
        training_rank_threshold=10,
        holdout_rank_threshold=10,
    )
    assert info["control_comparison_pass_january"] is False
    assert info["holdout_auxiliary_pass"] is False
    assert info["verdict"] == "null"


def test_verdict_default_thresholds_are_v0_3_3_locked_values():
    # If thresholds are omitted, the function uses the locked v0.3.3 values
    # (347 training, 329 holdout). Build a 365-anchor population matching this
    # and verify pass/fail at the locked boundaries.
    anchor_pop = [0.0] * 347 + [10.0] * 18   # 347 below 5.0
    info = evaluate_outcome_verdict(
        march20_pss_in=5.0,
        march20_pss_oos=5.0,
        anchor_pss_in=anchor_pop,
        anchor_pss_oos=anchor_pop,
        gregorian_pss_oos=0.0,
        january_pss_oos=0.0,
    )
    assert info["training_screen_pass"] is True
    assert info["holdout_pct_pass"] is True
    assert info["rank_thresholds"]["training_strictly_below_min"] == 347
    assert info["rank_thresholds"]["holdout_strictly_below_min"] == 329


def test_verdict_ties_do_not_help_pass():
    # 346 strictly below + 1 tie at march20 value: rank gate uses strictly_below
    # only, so training screen at default threshold 347 fails.
    anchor_pop = [0.0] * 346 + [5.0] + [10.0] * 18   # 346 below, 1 tie
    info = evaluate_outcome_verdict(
        march20_pss_in=5.0,
        march20_pss_oos=5.0,
        anchor_pss_in=anchor_pop,
        anchor_pss_oos=anchor_pop,
        gregorian_pss_oos=0.0,
        january_pss_oos=0.0,
    )
    assert info["march20_pss_in_strictly_below_count"] == 346
    assert info["training_screen_pass"] is False
    assert info["verdict"] == "null"


def test_verdict_empty_distribution_raises():
    with pytest.raises(ValueError):
        evaluate_outcome_verdict(0.5, 0.5, [], [0.1], 0.0, 0.0)


# ── compute_secondary_diagnostics ────────────────────────────────────────────

def test_secondary_diagnostics_shape_and_fdr():
    # Two phases, one with strong constant deviation, one near grand mean.
    values = [0.0] * 30 + [1.0] * 30
    phases = [0] * 30 + [1] * 30
    out = compute_secondary_diagnostics(values, phases)
    assert out["computed"] is True
    assert out["n_total"] == 60
    assert out["n_phases_with_data"] == 2
    # Both phases differ strongly from grand mean (0.5); expect both rejected.
    rejected_flags = [r["fdr_rejected"] for r in out["per_phase"]]
    assert all(rejected_flags)


def test_secondary_diagnostics_no_rejection_when_phases_match_grand_mean():
    # All phases share identical means and variance: no per-phase rejection.
    rng_seed_values = []
    for phase in range(5):
        rng_seed_values.extend([0.1, -0.1, 0.1, -0.1, 0.1, -0.1])  # mean 0 per phase
    phases = []
    for phase in range(5):
        phases.extend([phase] * 6)
    out = compute_secondary_diagnostics(rng_seed_values, phases)
    assert out["computed"] is True
    assert out["n_phases_rejected"] == 0


def test_secondary_diagnostics_zero_variance_phase_handled():
    # A phase with std=0 and mean != grand mean → finite p_value, no crash.
    values = [5.0, 5.0, 5.0, 0.0, 0.0, 0.0, 10.0]
    phases = [0, 0, 0, 1, 1, 1, 2]
    out = compute_secondary_diagnostics(values, phases)
    assert out["computed"] is True


# ── run_protocol on synthetic data: shape, gating, seed plumbing ─────────────

def _synthetic_split(n_train_years: int = 4, n_holdout_years: int = 2, seed: int = 7):
    """Build small synthetic train/holdout DataFrames matching loader schema."""
    import random as _random
    rng = _random.Random(seed)
    start = date(2010, 1, 4)
    train_end = date(2010 + n_train_years, 1, 1) - timedelta(days=1)
    holdout_end = date(2010 + n_train_years + n_holdout_years, 1, 1) - timedelta(days=1)

    dates = []
    d = start
    while d <= holdout_end:
        if d.weekday() < 5:  # business days only
            dates.append(d)
        d += timedelta(days=1)

    log_returns = [rng.gauss(0.0, 0.01) for _ in dates]
    log_return_sq = [r * r for r in log_returns]
    df = pd.DataFrame({
        "date": dates,
        "adj_close": [100.0] * len(dates),  # not used by orchestration
        "log_return": log_returns,
        "log_return_sq": log_return_sq,
    })
    train_df = df[df["date"] <= train_end].reset_index(drop=True)
    holdout_df = df[df["date"] > train_end].reset_index(drop=True)
    return train_df, holdout_df


def test_run_protocol_returns_per_outcome_verdicts():
    train_df, holdout_df = _synthetic_split()
    out = run_protocol(train_df, holdout_df)
    assert set(out["per_outcome_verdicts"].keys()) == set(OUTCOMES)
    for outcome in OUTCOMES:
        assert "verdict" in out["outcomes"][outcome]
        assert out["outcomes"][outcome]["verdict"] in {"pass", "null"}


def test_run_protocol_overall_summary_is_one_of_three_categories():
    train_df, holdout_df = _synthetic_split()
    out = run_protocol(train_df, holdout_df)
    assert out["overall_summary"] in {"positive", "null", "partial_mixed"}


def test_run_protocol_uses_exhaustive_365_anchor_enumeration():
    train_df, holdout_df = _synthetic_split()
    out = run_protocol(train_df, holdout_df)
    assert out["anchor_control_method"] == "exhaustive_enumeration_doy_1_to_365"
    assert out["anchor_control_population_size"] == 365
    assert out["training_rank_threshold"] == 347
    assert out["holdout_rank_threshold"] == 329
    # Anchor DOY list is exactly 1..365 in order.
    anchor_doys = out["outcomes"]["log_return"]["anchor_control_null_full"]["anchor_doys"]
    assert anchor_doys == list(range(1, 366))


def test_run_protocol_preserves_seed_but_does_not_consume_it():
    train_df, holdout_df = _synthetic_split()
    out = run_protocol(train_df, holdout_df)
    assert out["random_anchor_seed_preserved"] == 20260512
    assert out["random_anchor_seed_consumed_by_control"] is False


def test_run_protocol_signature_has_no_random_sampling_params():
    sig = inspect.signature(run_protocol)
    # v0.3.3 removed n_random_anchors and seed from the signature.
    assert "n_random_anchors" not in sig.parameters
    assert "seed" not in sig.parameters


def test_run_protocol_requires_log_return_columns():
    train_df, holdout_df = _synthetic_split()
    bad = train_df.drop(columns=["log_return_sq"])
    with pytest.raises(ValueError, match="missing required columns"):
        run_protocol(bad, holdout_df)


def test_run_protocol_failing_outcome_skips_secondary_diagnostics():
    # With random synthetic data, both outcomes' march20 PSS won't clear all
    # three gates. Both verdicts should be 'null' and both should report
    # secondary diagnostics as not computed.
    train_df, holdout_df = _synthetic_split()
    out = run_protocol(train_df, holdout_df)
    for outcome in OUTCOMES:
        result = out["outcomes"][outcome]
        if result["verdict"] == "null":
            assert result["secondary_diagnostics"]["computed"] is False
            assert "primary gate failed" in result["secondary_diagnostics"]["reason"]


def _localized_spike_dataframe(spike_phases_per_outcome):
    """Build a synthetic train/holdout split with phase-localized signals.

    *spike_phases_per_outcome* is a dict mapping outcome name → integer phase
    (in 0..107). For that outcome, the value is 1.0 exactly when the date's
    March20-anchored phase equals the spike phase, else 0.0. A localized spike
    is captured cleanly by March20-anchored bucketing but only diffusely by
    January-anchored and Gregorian-month bucketing, which lets March20 strictly
    beat the auxiliary controls.
    """
    dates: list = []
    d = date(2010, 1, 4)
    while d <= date(2017, 12, 29):
        if d.weekday() < 5:
            dates.append(d)
        d += timedelta(days=1)
    march20_phases = [assign_march20_phase(d_) for d_ in dates]
    cols = {"date": dates, "adj_close": [100.0] * len(dates)}
    for outcome in OUTCOMES:
        if outcome in spike_phases_per_outcome:
            target = spike_phases_per_outcome[outcome]
            cols[outcome] = [1.0 if p == target else 0.0 for p in march20_phases]
        else:
            cols[outcome] = [0.01] * len(dates)
    df = pd.DataFrame(cols)
    train_end = date(2015, 12, 31)
    train_df = df[df["date"] <= train_end].reset_index(drop=True)
    holdout_df = df[df["date"] > train_end].reset_index(drop=True)
    return train_df, holdout_df


def test_run_protocol_passing_outcome_computes_secondary_diagnostics():
    # log_return has a phase-0-localized spike (only March 20-22 days are 1.0);
    # log_return_sq is constant. March20-108 captures the spike perfectly while
    # January-108 and Gregorian-month buckets dilute it across other dates, so
    # March20 strictly beats both auxiliary controls and nearly all 365
    # integer-DOY anchors.
    train_df, holdout_df = _localized_spike_dataframe({"log_return": 0})
    out = run_protocol(train_df, holdout_df)
    log_return_result = out["outcomes"]["log_return"]
    assert log_return_result["verdict"] == "pass"
    assert log_return_result["secondary_diagnostics"]["computed"] is True
    sq_result = out["outcomes"]["log_return_sq"]
    assert sq_result["verdict"] == "null"
    assert sq_result["secondary_diagnostics"]["computed"] is False


def test_run_protocol_partial_mixed_overall_label():
    train_df, holdout_df = _localized_spike_dataframe({"log_return": 0})
    out = run_protocol(train_df, holdout_df)
    assert out["overall_summary"] == "partial_mixed"


def test_run_protocol_all_pass_overall_label():
    # Each outcome gets its own phase-localized spike at a different phase.
    train_df, holdout_df = _localized_spike_dataframe(
        {"log_return": 0, "log_return_sq": 50}
    )
    out = run_protocol(train_df, holdout_df)
    assert out["overall_summary"] == "positive"
    for outcome in OUTCOMES:
        assert out["outcomes"][outcome]["verdict"] == "pass"
        assert out["outcomes"][outcome]["secondary_diagnostics"]["computed"] is True


def test_run_protocol_all_null_overall_label():
    # Pure random data → both outcomes null.
    train_df, holdout_df = _synthetic_split(seed=123)
    out = run_protocol(train_df, holdout_df)
    if all(v == "null" for v in out["per_outcome_verdicts"].values()):
        assert out["overall_summary"] == "null"


# ── Runner script: no live network calls, frozen-CSV-only path ───────────────

def test_runner_exists():
    assert os.path.exists(RUNNER_PATH), "scripts/run_harmonic_calendar_protocol.py missing"


def _runner_source() -> str:
    with open(RUNNER_PATH, "r", encoding="utf-8") as fh:
        return fh.read()


def test_runner_does_not_import_requests():
    # The canonical loader has no live network calls; the runner must inherit
    # that property by not importing requests directly.
    src = _runner_source()
    for line in src.splitlines():
        stripped = line.strip()
        assert stripped != "import requests", "runner must not import requests"
        assert not stripped.startswith("from requests"), "runner must not import from requests"


def test_runner_does_not_call_acquire_or_download():
    src = _runner_source()
    assert "_download_yahoo_adjclose" not in src
    assert "acquire_spy_from_yahoo" not in src


def test_runner_uses_load_spy_only():
    src = _runner_source()
    assert "from spy_loader import load_spy" in src
    assert "load_spy(" in src


def test_runner_points_at_frozen_csv_with_expected_hash():
    src = _runner_source()
    expected_hash = (
        "e8fc0357410ce499da8f67e09b4c9908232e18a55445f38969e77fa712aaaa56"
    )
    assert expected_hash in src
    assert "spy_yahoo_v8_19930129_20241231_" in src


def test_runner_imports_v0_3_3_constants():
    src = _runner_source()
    # Runner reports the locked v0.3.3 constants but does not pass them as
    # call-time parameters to run_protocol (it has no such parameters).
    assert "ANCHOR_CONTROL_POPULATION_SIZE" in src
    assert "TRAINING_RANK_THRESHOLD" in src
    assert "HOLDOUT_RANK_THRESHOLD" in src
    assert "RANDOM_ANCHOR_SEED" in src   # preserved for audit reporting only


def test_runner_does_not_pass_n_random_anchors_or_seed_to_run_protocol():
    src = _runner_source()
    # v0.3.3: run_protocol has no seed/n_random_anchors parameters.
    assert "n_random_anchors=" not in src
    assert "seed=RANDOM_ANCHOR_SEED" not in src


def test_runner_active_memo_is_v0_3_3():
    src = _runner_source()
    assert "harmonic_calendar_design_memo_v0.3.3.md" in src


# ── Real-data firewall is enforced by the runner-source tests above and by
#    construction (this module never calls load_spy() and never opens the
#    frozen CSV). String mentions of "load_spy" and the CSV hash live only
#    inside tests that read the runner script's source for verification.

