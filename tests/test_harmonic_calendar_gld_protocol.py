"""Tests for scripts/run_harmonic_calendar_gld_protocol.py and GLD orchestration.

These tests deliberately do NOT:
  - read the frozen GLD CSV for PSS computation
  - call gld_loader.load_gld() against real data for protocol execution
  - assign phases to real GLD data
  - compute real-data PSS values

They verify runner-script integrity, GLD-specific metadata fields, H1 string
exactness, version distinguishability, and orchestration correctness on toy data.
"""

import inspect
import math
import os
import random
from datetime import date, timedelta

import pandas as pd
import pytest

import harmonic_calendar_protocol as hcp
from harmonic_calendar import (
    ANCHOR_CONTROL_POPULATION_SIZE,
    RANDOM_ANCHOR_SEED,
    TRAINING_RANK_THRESHOLD,
    HOLDOUT_RANK_THRESHOLD,
)
from harmonic_calendar_protocol import (
    ACTIVE_MEMO_VERSION as HCP_ACTIVE_MEMO_VERSION,
    OUTCOMES,
    run_protocol,
)
import gld_loader

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLD_RUNNER_PATH = os.path.join(
    REPO_ROOT, "scripts", "run_harmonic_calendar_gld_protocol.py"
)

GLD_EXPECTED_ACTIVE_MEMO_VERSION = "v0.1"
GLD_EXPECTED_INHERITED_LENS_VERSION = "v0.3.3"
GLD_EXPECTED_CSV_SHA256 = (
    "368fe45094eafa277c81accd2c71b2b593ddcf917c29c7b269de088a31fd1b2c"
)
GLD_EXPECTED_H1 = "Harmonic Calendar × GLD — v0.1 Verdict"
GLD_EXPECTED_MEMO_PATH_FRAGMENT = "harmonic_calendar_gld_v0.1.md"


# ── Synthetic data helpers ────────────────────────────────────────────────────

def _synthetic_gld_split(seed: int = 7) -> tuple:
    """Build a minimal synthetic split resembling GLD's date range."""
    rng = random.Random(seed)
    start = date(2004, 11, 19)  # effective first loaded return date
    n_train = 2520   # ~10 years of business days
    n_holdout = 2516  # ~10 years of business days
    n_total = n_train + n_holdout

    rows = []
    price = 45.0
    d = start
    for _ in range(n_total):
        while d.weekday() >= 5:
            d += timedelta(days=1)
        lr = rng.gauss(0.0003, 0.008)
        rows.append({"date": d, "adj_close": price, "log_return": lr, "log_return_sq": lr ** 2})
        price = max(1.0, price * (1 + lr))
        d += timedelta(days=1)

    df = pd.DataFrame(rows)
    train_df = df.iloc[:n_train].copy().reset_index(drop=True)
    holdout_df = df.iloc[n_train:].copy().reset_index(drop=True)
    return train_df, holdout_df


# ── GLD runner exists and has correct structure ───────────────────────────────

def test_gld_runner_exists():
    assert os.path.exists(GLD_RUNNER_PATH), (
        "scripts/run_harmonic_calendar_gld_protocol.py not found"
    )


def _gld_runner_source() -> str:
    with open(GLD_RUNNER_PATH, "r", encoding="utf-8") as fh:
        return fh.read()


# ── H1 string must be exactly right ──────────────────────────────────────────

def test_gld_runner_h1_string_is_exact():
    src = _gld_runner_source()
    assert GLD_EXPECTED_H1 in src, (
        "GLD runner must contain H1 exactly: {!r}".format(GLD_EXPECTED_H1)
    )


def test_gld_runner_h1_rendered_with_hash_prefix():
    src = _gld_runner_source()
    assert "# {}".format(GLD_EXPECTED_H1) in src, (
        "H1 must appear as a markdown heading: '# {}'".format(GLD_EXPECTED_H1)
    )


# ── Version fields are distinguishable ───────────────────────────────────────

def test_gld_runner_active_memo_version_is_v0_1():
    src = _gld_runner_source()
    assert 'GLD_ACTIVE_MEMO_VERSION = "v0.1"' in src or \
           "GLD_ACTIVE_MEMO_VERSION = 'v0.1'" in src, (
        "GLD runner must set GLD_ACTIVE_MEMO_VERSION = 'v0.1'"
    )


def test_gld_runner_has_inherited_lens_version():
    src = _gld_runner_source()
    assert "INHERITED_LENS_VERSION" in src, (
        "GLD runner must define INHERITED_LENS_VERSION to distinguish "
        "cell memo version (v0.1) from inherited protocol version (v0.3.3)"
    )


def test_gld_runner_inherited_lens_version_is_v0_3_3():
    src = _gld_runner_source()
    assert HCP_ACTIVE_MEMO_VERSION == "v0.3.3", (
        "harmonic_calendar_protocol ACTIVE_MEMO_VERSION must be v0.3.3"
    )
    assert "HCP_ACTIVE_MEMO_VERSION" in src, (
        "GLD runner must import HCP_ACTIVE_MEMO_VERSION from harmonic_calendar_protocol"
    )


def test_gld_active_memo_version_differs_from_hcp_version():
    assert GLD_EXPECTED_ACTIVE_MEMO_VERSION != GLD_EXPECTED_INHERITED_LENS_VERSION, (
        "GLD active_memo_version (v0.1) must differ from inherited_lens_version (v0.3.3)"
    )


# ── Active memo path references GLD design memo ───────────────────────────────

def test_gld_runner_references_gld_design_memo():
    src = _gld_runner_source()
    assert GLD_EXPECTED_MEMO_PATH_FRAGMENT in src, (
        "GLD runner must reference docs/harmonic_calendar_gld_v0.1.md"
    )


# ── Loader: uses load_gld, not load_spy ──────────────────────────────────────

def test_gld_runner_uses_load_gld():
    src = _gld_runner_source()
    assert "from gld_loader import load_gld" in src, (
        "GLD runner must import load_gld from gld_loader"
    )
    assert "load_gld(" in src, (
        "GLD runner must call load_gld()"
    )


def test_gld_runner_does_not_use_load_spy():
    src = _gld_runner_source()
    assert "load_spy" not in src, (
        "GLD runner must not reference load_spy — asset is GLD, not SPY"
    )


# ── Frozen CSV hash is the GLD hash ──────────────────────────────────────────

def test_gld_runner_points_at_frozen_gld_csv():
    src = _gld_runner_source()
    assert GLD_EXPECTED_CSV_SHA256 in src, (
        "GLD runner must embed the GLD frozen CSV SHA256"
    )
    assert "gld_yahoo_v8_20041118_20241231_" in src, (
        "GLD runner must reference the GLD frozen CSV filename stem"
    )


def test_gld_runner_does_not_embed_spy_hash():
    src = _gld_runner_source()
    spy_hash = "e8fc0357410ce499da8f67e09b4c9908232e18a55445f38969e77fa712aaaa56"
    assert spy_hash not in src, (
        "GLD runner must not embed the SPY CSV hash"
    )


# ── Protocol constants: exhaustive 365-anchor, locked thresholds ──────────────

def test_gld_runner_imports_locked_constants():
    src = _gld_runner_source()
    assert "ANCHOR_CONTROL_POPULATION_SIZE" in src
    assert "TRAINING_RANK_THRESHOLD" in src
    assert "HOLDOUT_RANK_THRESHOLD" in src
    assert "RANDOM_ANCHOR_SEED" in src


def test_gld_runner_does_not_pass_seed_to_run_protocol():
    src = _gld_runner_source()
    assert "n_random_anchors=" not in src, (
        "GLD runner must not pass n_random_anchors to run_protocol"
    )
    assert "seed=RANDOM_ANCHOR_SEED" not in src, (
        "GLD runner must not pass seed to run_protocol"
    )


# ── Raw/design vs effective-loaded ranges are distinguishable ─────────────────

def test_gld_runner_has_raw_design_data_range_field():
    src = _gld_runner_source()
    assert "raw_design_data_range" in src, (
        "GLD runner must include raw_design_data_range field to distinguish "
        "design range (2004-11-18 through 2024-12-31) from effective loaded range"
    )


def test_gld_runner_has_design_training_rule_field():
    src = _gld_runner_source()
    assert "design_training_rule" in src, (
        "GLD runner must include design_training_rule field"
    )


def test_gld_runner_has_effective_loaded_training_date_range_field():
    src = _gld_runner_source()
    assert "effective_loaded_training_date_range" in src, (
        "GLD runner must include effective_loaded_training_date_range field "
        "(first raw row 2004-11-18 is dropped; effective first return is 2004-11-19)"
    )


def test_gld_runner_has_effective_loaded_holdout_date_range_field():
    src = _gld_runner_source()
    assert "effective_loaded_holdout_date_range" in src


# ── No live network calls ─────────────────────────────────────────────────────

def test_gld_runner_does_not_import_requests():
    src = _gld_runner_source()
    for line in src.splitlines():
        stripped = line.strip()
        assert stripped != "import requests", "GLD runner must not import requests"
        assert not stripped.startswith("from requests"), (
            "GLD runner must not import from requests"
        )


def test_gld_runner_does_not_call_acquire_or_download():
    src = _gld_runner_source()
    assert "_download_yahoo_adjclose" not in src
    assert "acquire_gld_from_yahoo" not in src


# ── Training-power caveat is present ─────────────────────────────────────────

def test_gld_runner_contains_training_power_caveat():
    src = _gld_runner_source()
    assert "10.1 year" in src or "training window" in src.lower(), (
        "GLD runner must include the training-power caveat from design memo v0.1"
    )


# ── No PSS in tests except on synthetic data ──────────────────────────────────

def test_gld_protocol_run_on_synthetic_data_returns_correct_structure():
    train_df, holdout_df = _synthetic_gld_split(seed=42)
    result = run_protocol(train_df, holdout_df)

    assert "per_outcome_verdicts" in result
    assert "overall_summary" in result
    assert result["overall_summary"] in ("positive", "null", "partial_mixed")
    for outcome in OUTCOMES:
        assert outcome in result["per_outcome_verdicts"]
        assert result["per_outcome_verdicts"][outcome] in ("pass", "null")
    assert result["anchor_control_population_size"] == 365
    assert result["training_rank_threshold"] == TRAINING_RANK_THRESHOLD
    assert result["holdout_rank_threshold"] == HOLDOUT_RANK_THRESHOLD
    assert result["random_anchor_seed_consumed_by_control"] is False


def test_gld_protocol_synthetic_strict_rank_thresholds():
    assert TRAINING_RANK_THRESHOLD == 347
    assert HOLDOUT_RANK_THRESHOLD == 329


def test_gld_protocol_random_anchor_seed_preserved():
    assert RANDOM_ANCHOR_SEED == 20260512


def test_gld_protocol_anchor_population_size_is_365():
    assert ANCHOR_CONTROL_POPULATION_SIZE == 365


def test_gld_protocol_synthetic_train_holdout_contain_no_overlap():
    train_df, holdout_df = _synthetic_gld_split(seed=99)
    train_dates = set(train_df["date"])
    holdout_dates = set(holdout_df["date"])
    assert train_dates.isdisjoint(holdout_dates)


def test_gld_protocol_synthetic_verdict_per_outcome():
    train_df, holdout_df = _synthetic_gld_split(seed=7)
    result = run_protocol(train_df, holdout_df)
    for outcome in OUTCOMES:
        v = result["per_outcome_verdicts"][outcome]
        assert v in ("pass", "null"), "verdict must be 'pass' or 'null', got {!r}".format(v)


def test_gld_loader_does_not_reference_pss_functions():
    src = inspect.getsource(gld_loader)
    for symbol in ("pss_in_sample", "pss_out_of_sample"):
        assert symbol not in src, (
            "gld_loader.py must not reference {!r}".format(symbol)
        )
