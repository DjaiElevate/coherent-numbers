"""End-to-end tests for the Candidate B locked-protocol orchestration.

All tests use synthetic in-memory fixtures generated from fixed seeds.
None of the tests load real frozen pullback CSVs. Git-state pre-flight tests
use temporary repositories in tmp_path; the real project repo is never
made dirty.
"""

import hashlib
import os
import subprocess
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

import candidate_b_protocol as protocol
from candidate_b_loader import ReducedTrades
from candidate_b_rerun_gate import (
    RerunInconsistency,
    assert_byte_identical_reruns,
    canonicalize_protocol_payload,
    payload_digest,
)
from run_candidate_b_protocol import (
    RepoHeadNotDescendedFromLock,
    WorkingTreeNotClean,
    check_repo_head_descended_from_lock,
    check_working_tree_clean,
    compose_header,
    render_markdown,
)


# ── Fixtures ─────────────────────────────────────────────────────────────────


def _build_synthetic_reduced(seed=12345, n_trades=200, assets=("A", "B", "C")):
    rng = np.random.Generator(np.random.PCG64(seed))
    assets_arr = np.array(list(assets), dtype=object)
    asset = rng.choice(assets_arr, size=n_trades)
    start = date(2010, 1, 1)
    days_offset = rng.integers(0, 365 * 5, size=n_trades)
    entry_dates = np.array(
        [start + timedelta(days=int(d)) for d in days_offset], dtype=object
    )
    exit_dates = np.array(
        [d + timedelta(days=int(rng.integers(5, 30))) for d in entry_dates], dtype=object
    )
    is_long = rng.integers(0, 2, size=n_trades).astype(bool)
    r_multiple = rng.standard_normal(n_trades) * 1.5
    trade_id = np.arange(n_trades, dtype=np.int64)
    frozen_artifact_id = np.array(["synthetic"] * n_trades, dtype=object)
    return ReducedTrades(
        trade_id=trade_id,
        asset=asset,
        entry_date=entry_dates,
        exit_date=exit_dates,
        is_long=is_long,
        r_multiple=r_multiple,
        frozen_artifact_id=frozen_artifact_id,
    )


def _git_env():
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = "Test"
    env["GIT_AUTHOR_EMAIL"] = "test@example.com"
    env["GIT_COMMITTER_NAME"] = "Test"
    env["GIT_COMMITTER_EMAIL"] = "test@example.com"
    return env


def _init_tmp_repo(tmp_path):
    env = _git_env()
    subprocess.run(
        ["git", "init", "--initial-branch=main", str(tmp_path)],
        check=True, capture_output=True, env=env,
    )
    subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "--allow-empty", "-m", "root"],
        check=True, capture_output=True, env=env,
    )
    return env


# ── Locked constants ─────────────────────────────────────────────────────────


def test_locked_constants():
    assert protocol.LABEL_PERM_SEED == 20260514
    assert protocol.ASSET_STRAT_DIAG_SEED == 20260515
    assert protocol.N_PERM == 10_000
    assert protocol.PERM_BEAT_THRESHOLD == 9_500
    assert protocol.ANCHOR_BEAT_THRESHOLD == 347
    assert protocol.LOCK_COMMIT == "159cccd"
    assert protocol.DESIGN_MEMO_COMMIT == "1e9a3e6"
    assert protocol.FREEZE_COMMIT == "5225bfd"


# ── N.1 unstratified label permutation ──────────────────────────────────────


def test_n1_returns_correct_size():
    reduced = _build_synthetic_reduced()
    null = protocol.run_n1_label_permutation_null(reduced, n_perm=200)
    assert null.shape == (200,)


def test_n1_is_deterministic_with_same_seed():
    reduced = _build_synthetic_reduced(seed=1)
    a = protocol.run_n1_label_permutation_null(reduced, n_perm=300, seed=42)
    b = protocol.run_n1_label_permutation_null(reduced, n_perm=300, seed=42)
    np.testing.assert_array_equal(a, b)


def test_n1_diverges_with_different_seeds():
    reduced = _build_synthetic_reduced(seed=2)
    a = protocol.run_n1_label_permutation_null(reduced, n_perm=300, seed=42)
    b = protocol.run_n1_label_permutation_null(reduced, n_perm=300, seed=99)
    assert not np.array_equal(a, b)


# ── N.2 exhaustive anchor null ──────────────────────────────────────────────


def test_n2_returns_365_anchors():
    reduced = _build_synthetic_reduced()
    null = protocol.run_n2_anchor_control_null(reduced)
    assert len(null) == 365
    assert set(null.keys()) == set(range(1, 366))


def test_n2_is_deterministic():
    reduced = _build_synthetic_reduced(seed=3)
    a = protocol.run_n2_anchor_control_null(reduced)
    b = protocol.run_n2_anchor_control_null(reduced)
    assert a == b


# ── Asset-stratified diagnostic ─────────────────────────────────────────────


def test_asset_stratified_returns_correct_size():
    reduced = _build_synthetic_reduced()
    null = protocol.run_asset_stratified_diagnostic(reduced, n_perm=100)
    assert null.shape == (100,)


def test_asset_stratified_uses_different_seed_than_n1():
    reduced = _build_synthetic_reduced(seed=4)
    n1 = protocol.run_n1_label_permutation_null(reduced, n_perm=300, seed=protocol.LABEL_PERM_SEED)
    strat = protocol.run_asset_stratified_diagnostic(reduced, n_perm=300, seed=protocol.ASSET_STRAT_DIAG_SEED)
    assert not np.array_equal(n1, strat)


# ── Verdict map ──────────────────────────────────────────────────────────────


def test_verdict_map_confirmatory_when_both_thresholds_pass():
    perm = np.zeros(10_000)
    anchor = {d: 0.0 for d in range(1, 366)}
    verdict = protocol.evaluate_verdict(
        observed=1.0,
        perm_null=perm,
        anchor_null=anchor,
    )
    assert verdict["verdict"] == "Confirmatory"
    assert verdict["beat_count_perm"] == 10_000
    assert verdict["beat_count_anchor"] == 365


def test_verdict_map_non_confirmatory_when_neither_passes():
    perm = np.ones(10_000)  # all >= observed
    anchor = {d: 1.0 for d in range(1, 366)}
    verdict = protocol.evaluate_verdict(observed=0.5, perm_null=perm, anchor_null=anchor)
    assert verdict["verdict"] == "Non-confirmatory"
    assert verdict["beat_count_perm"] == 0
    assert verdict["beat_count_anchor"] == 0


def test_verdict_map_split_null_when_only_perm_passes():
    perm = np.zeros(10_000)
    anchor = {d: 2.0 for d in range(1, 366)}  # all > observed=1
    verdict = protocol.evaluate_verdict(observed=1.0, perm_null=perm, anchor_null=anchor)
    assert verdict["verdict"] == "Split-null"


def test_verdict_map_split_null_when_only_anchor_passes():
    perm = np.full(10_000, 2.0)  # all > observed
    anchor = {d: 0.0 for d in range(1, 366)}
    verdict = protocol.evaluate_verdict(observed=1.0, perm_null=perm, anchor_null=anchor)
    assert verdict["verdict"] == "Split-null"


def test_verdict_strict_inequality_for_beat_count():
    """Ties do NOT count toward beat_count."""
    perm = np.full(10_000, 0.5)
    anchor = {d: 0.5 for d in range(1, 366)}
    verdict = protocol.evaluate_verdict(observed=0.5, perm_null=perm, anchor_null=anchor)
    assert verdict["beat_count_perm"] == 0
    assert verdict["beat_count_anchor"] == 0
    assert verdict["verdict"] == "Non-confirmatory"


def test_verbalization_pooled_population_when_asset_strat_weak():
    perm = np.zeros(10_000)
    anchor = {d: 0.0 for d in range(1, 366)}
    asset_strat_weak = np.full(10_000, 5.0)  # all > observed=1
    verdict = protocol.evaluate_verdict(
        observed=1.0, perm_null=perm, anchor_null=anchor,
        asset_strat_null=asset_strat_weak,
    )
    assert verdict["verdict"] == "Confirmatory"
    assert verdict["verbalization_class"] == "pooled-population-modulation"


def test_verbalization_persists_under_mix_when_asset_strat_strong():
    perm = np.zeros(10_000)
    anchor = {d: 0.0 for d in range(1, 366)}
    asset_strat_strong = np.zeros(10_000)  # all < observed=1
    verdict = protocol.evaluate_verdict(
        observed=1.0, perm_null=perm, anchor_null=anchor,
        asset_strat_null=asset_strat_strong,
    )
    assert verdict["verdict"] == "Confirmatory"
    assert verdict["verbalization_class"] == "pooled-modulation-persists-under-asset-mix"


def test_verbalization_for_non_confirmatory():
    perm = np.ones(10_000)
    anchor = {d: 1.0 for d in range(1, 366)}
    verdict = protocol.evaluate_verdict(observed=0.5, perm_null=perm, anchor_null=anchor)
    assert verdict["verbalization_class"] == "n/a-non-confirmatory"


def test_verbalization_for_split_null():
    perm = np.zeros(10_000)
    anchor = {d: 2.0 for d in range(1, 366)}
    verdict = protocol.evaluate_verdict(observed=1.0, perm_null=perm, anchor_null=anchor)
    assert verdict["verbalization_class"] == "n/a-split-null"


# ── End-to-end run ───────────────────────────────────────────────────────────


def test_run_returns_expected_top_level_keys():
    reduced = _build_synthetic_reduced(seed=5)
    result = protocol.run(reduced, n_perm=300)
    for key in (
        "observed_pss_b1", "beat_count_perm", "beat_count_anchor",
        "perm_strict_percentile", "anchor_strict_percentile",
        "verdict", "verbalization_class",
        "n1_null_full", "n2_null_full", "asset_stratified_null_full",
        "diagnostics", "locked_parameters", "seeds",
        "design_memo_commit", "lock_acceptance_commit", "freeze_commit",
    ):
        assert key in result, "missing key: {}".format(key)


def test_run_n1_size_matches_n_perm():
    reduced = _build_synthetic_reduced(seed=6)
    result = protocol.run(reduced, n_perm=250)
    assert len(result["n1_null_full"]) == 250
    assert len(result["asset_stratified_null_full"]) == 250


def test_run_n2_full_has_365_keys():
    reduced = _build_synthetic_reduced(seed=7)
    result = protocol.run(reduced, n_perm=100)
    assert len(result["n2_null_full"]) == 365
    keys_int = sorted(int(k) for k in result["n2_null_full"].keys())
    assert keys_int == list(range(1, 366))


def test_run_diagnostics_has_all_sections():
    reduced = _build_synthetic_reduced(seed=8)
    result = protocol.run(reduced, n_perm=100)
    d = result["diagnostics"]
    for key in (
        "pss_greg_month", "pss_jan", "per_asset_pss_b1",
        "phase_cell_occupancy", "c4_directional_counts",
        "c4_within_direction_r_multiple",
        "asset_stratified_beat_count",
    ):
        assert key in d


def test_run_non_confirmatory_on_random_synthetic_fixture():
    """Randomly-labelled synthetic data should not produce Confirmatory at
    locked thresholds."""
    reduced = _build_synthetic_reduced(seed=99, n_trades=300)
    result = protocol.run(reduced)
    assert result["verdict"] in ("Non-confirmatory", "Split-null")


def test_run_is_deterministic_under_rerun_gate():
    reduced = _build_synthetic_reduced(seed=10, n_trades=120)

    def runner():
        return protocol.run(reduced, n_perm=200)

    canonical = assert_byte_identical_reruns(runner)
    digest = hashlib.sha256(canonical).hexdigest()
    assert len(digest) == 64


def test_run_payload_digest_stable_across_invocations():
    reduced = _build_synthetic_reduced(seed=11, n_trades=80)
    a = protocol.run(reduced, n_perm=150)
    b = protocol.run(reduced, n_perm=150)
    assert payload_digest(a) == payload_digest(b)


def test_rerun_gate_detects_divergence_when_payload_perturbed():
    reduced = _build_synthetic_reduced(seed=12, n_trades=80)
    counter = {"n": 0}

    def runner_with_perturbation():
        counter["n"] += 1
        out = protocol.run(reduced, n_perm=150)
        if counter["n"] == 2:
            out["observed_pss_b1"] = out["observed_pss_b1"] + 1e-9  # perturb
        return out

    with pytest.raises(RerunInconsistency):
        assert_byte_identical_reruns(runner_with_perturbation)


def test_compute_observed_pss_b1_is_deterministic():
    reduced = _build_synthetic_reduced(seed=13)
    a = protocol.compute_observed_pss_b1(reduced)
    b = protocol.compute_observed_pss_b1(reduced)
    assert a == b


# ── Header composition (runner side) ─────────────────────────────────────────


def test_compose_header_excludes_payload_fields():
    """Header object must contain only metadata, not protocol payload values."""
    observed_hashes = {p: "deadbeef" * 8 for p in protocol.__dict__.get("FROZEN_DATASETS", {})}
    # Use a synthetic context — the header function relies on git and FROZEN_DATASETS
    # so call it via the actual loader constants.
    from candidate_b_loader import FROZEN_DATASETS
    observed_hashes = {p: FROZEN_DATASETS[p] for p in FROZEN_DATASETS}
    header = compose_header(
        repo_root=REPO_ROOT,
        observed_hashes=observed_hashes,
        manifest_sha="0" * 64,
        run_timestamp_utc="2026-05-15T00:00:00Z",
        rerun_verification_digest="a" * 64,
    )
    for key in ("rerun_verification_digest", "run_timestamp_utc", "seeds",
                 "locked_parameters", "frozen_csv_inputs", "freeze_manifest_sha256"):
        assert key in header
    # No payload-only keys should appear in the header
    for forbidden in ("observed_pss_b1", "verdict", "n1_null_full", "diagnostics"):
        assert forbidden not in header


def test_render_markdown_contains_verdict_and_disclosure():
    full = {
        "schema_version": "candidate_b_v0.1",
        "header": {
            "design_memo_path": "docs/candidate_b_design_memo_v0.1.md",
            "active_memo_version": "v0.1",
            "design_memo_commit": "1e9a3e6",
            "lock_acceptance_commit": "159cccd",
            "freeze_commit": "5225bfd",
            "run_timestamp_utc": "2026-05-15T00:00:00Z",
            "repo_commit_before_run": "abc123",
            "rerun_verification_digest": "d" * 64,
            "seeds": {"N_PERM": 10000},
            "locked_parameters": {
                "perm_beat_threshold": 9500,
                "anchor_beat_threshold": 347,
            },
        },
        "protocol_payload": {
            "verdict": "Non-confirmatory",
            "verbalization_class": "n/a-non-confirmatory",
            "observed_pss_b1": 0.001234,
            "beat_count_perm": 100,
            "beat_count_anchor": 50,
            "perm_strict_percentile": 0.01,
            "anchor_strict_percentile": 0.137,
        },
        "disclosure_paragraph_section_13": "DISCLOSURE TEXT MARKER",
    }
    md = render_markdown(full)
    assert "Non-confirmatory" in md
    assert "DISCLOSURE TEXT MARKER" in md
    assert "Candidate B v0.1" in md


# ── Runner pre-flight git-state checks ───────────────────────────────────────


def test_check_working_tree_clean_passes_on_clean_temp_repo(tmp_path):
    _init_tmp_repo(tmp_path)
    check_working_tree_clean(str(tmp_path))  # should not raise


def test_check_working_tree_clean_raises_on_dirty_temp_repo(tmp_path):
    _init_tmp_repo(tmp_path)
    (tmp_path / "junk.txt").write_text("hello")
    with pytest.raises(WorkingTreeNotClean):
        check_working_tree_clean(str(tmp_path))


def test_check_working_tree_clean_raises_on_modified_tracked_file(tmp_path):
    env = _init_tmp_repo(tmp_path)
    f = tmp_path / "tracked.txt"
    f.write_text("v1")
    subprocess.run(["git", "-C", str(tmp_path), "add", "tracked.txt"], check=True, env=env)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", "add tracked"], check=True, env=env)
    f.write_text("v2")
    with pytest.raises(WorkingTreeNotClean):
        check_working_tree_clean(str(tmp_path))


def test_check_repo_head_descended_from_lock_passes_when_ancestor(tmp_path):
    env = _init_tmp_repo(tmp_path)
    # Make a commit and treat it as the "lock" commit, then advance HEAD
    (tmp_path / "a.txt").write_text("a")
    subprocess.run(["git", "-C", str(tmp_path), "add", "a.txt"], check=True, env=env)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", "lock"], check=True, env=env)
    lock_commit = subprocess.check_output(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"], env=env, text=True,
    ).strip()
    (tmp_path / "b.txt").write_text("b")
    subprocess.run(["git", "-C", str(tmp_path), "add", "b.txt"], check=True, env=env)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", "advance"], check=True, env=env)
    # HEAD is descended from lock_commit
    check_repo_head_descended_from_lock(str(tmp_path), lock_commit)  # should not raise


def test_check_repo_head_descended_from_lock_raises_when_not_ancestor(tmp_path):
    env = _init_tmp_repo(tmp_path)
    # Create a divergent commit on a new orphan branch; HEAD on this orphan is
    # not descended from the main-branch commit.
    (tmp_path / "x.txt").write_text("x")
    subprocess.run(["git", "-C", str(tmp_path), "add", "x.txt"], check=True, env=env)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", "main commit"], check=True, env=env)
    main_commit = subprocess.check_output(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"], env=env, text=True,
    ).strip()
    subprocess.run(
        ["git", "-C", str(tmp_path), "checkout", "--orphan", "branch2"],
        check=True, env=env, capture_output=True,
    )
    subprocess.run(["git", "-C", str(tmp_path), "rm", "-rf", "."], check=True, env=env, capture_output=True)
    (tmp_path / "y.txt").write_text("y")
    subprocess.run(["git", "-C", str(tmp_path), "add", "y.txt"], check=True, env=env)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", "orphan"], check=True, env=env)
    # HEAD now points at the orphan; main_commit is not its ancestor.
    with pytest.raises(RepoHeadNotDescendedFromLock):
        check_repo_head_descended_from_lock(str(tmp_path), main_commit)
