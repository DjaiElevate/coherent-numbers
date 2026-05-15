"""End-to-end tests for the Candidate C locked-protocol orchestration.

Synthetic in-memory fixtures except for one gated integration test that
exercises the section 11.6 provenance check against Candidate B's real
verdict log (authorized from lock-acceptance dc97576 forward, per section 6
of the lock-acceptance, for the provenance check only).
"""

import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

import candidate_c_protocol as proto
from candidate_b_loader import ReducedTrades
from candidate_b_rerun_gate import (
    assert_byte_identical_reruns,
    canonicalize_protocol_payload,
)
from run_candidate_c_protocol import (
    DISCLOSURE_SECTION_12_4,
    DISCLOSURE_SECTION_12_5,
    DISCLOSURE_SECTION_13,
    compose_header,
    render_markdown,
)

C_MEMO = os.path.join(REPO_ROOT, "docs", "candidate_c_design_memo_v0.1.md")
B_REAL_LOG = os.path.join(
    REPO_ROOT, "results", "candidate_b_results_20260514_231323_c1982503.json"
)


# ── Fixtures ─────────────────────────────────────────────────────────────────

def _synthetic_reduced(seed=4242, n=180, assets=("SPY", "EFA", "GLD")):
    rng = np.random.Generator(np.random.PCG64(seed))
    assets_arr = np.array(list(assets), dtype=object)
    asset = rng.choice(assets_arr, size=n)
    start = date(2010, 1, 1)
    offs = rng.integers(0, 365 * 6, size=n)
    entry = np.array([start + timedelta(days=int(o)) for o in offs], dtype=object)
    exit_ = np.array(
        [d + timedelta(days=int(rng.integers(3, 25))) for d in entry],
        dtype=object,
    )
    is_long = (rng.integers(0, 2, size=n) == 1)
    # guarantee not all-one-direction
    is_long[0] = True
    is_long[1] = False
    r = rng.standard_normal(n)
    return ReducedTrades(
        trade_id=np.arange(n, dtype=np.int64),
        asset=asset,
        entry_date=entry,
        exit_date=exit_,
        is_long=is_long,
        r_multiple=r.astype(np.float64),
        frozen_artifact_id=np.array(["synthetic"] * n, dtype=object),
    )


def _write_fake_b_log(tmp_path, surface_12_int_keyed):
    payload = {
        "protocol_payload": {
            "n2_null_full": {
                str(d): float(v) for d, v in surface_12_int_keyed.items()
            }
        }
    }
    p = tmp_path / "fake_b_log.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return str(p)


def _extract_ab(class_heading):
    text = open(C_MEMO, encoding="utf-8").read().split("\n")
    idx = next(i for i, l in enumerate(text) if l.strip() == class_heading)
    a = b = None
    for l in text[idx + 1:]:
        if l.startswith("### ") or l.startswith("## "):
            break
        if a is None and l.startswith("(a) "):
            a = l
        elif b is None and l.startswith("(b) "):
            b = l
        if a and b:
            break
    return a + "\n\n" + b


# ── Locked constants ─────────────────────────────────────────────────────────

def test_locked_constants():
    assert proto.LABEL_PERM_SEED_C == 20260516
    assert proto.ASSET_STRAT_DIAG_SEED_C == 20260517
    assert proto.N_PERM == 10_000
    assert proto.BEAT_COUNT_THRESHOLD == 9_500
    assert proto.BUCKET_COUNTS == (12, 10)
    assert proto.ANCHOR_DOYS == tuple(range(1, 366))
    assert proto.ACTIVE_MEMO_VERSION == "v0.1"
    assert proto.DESIGN_MEMO_COMMIT == "401ce45"
    assert proto.LOCK_COMMIT == "dc97576"
    assert proto.FREEZE_COMMIT == "5225bfd"
    assert proto.PROVENANCE_TOLERANCE == 1e-12
    assert proto.B_VERDICT_LOG_PATH == (
        "results/candidate_b_results_20260514_231323_c1982503.json"
    )
    assert proto.B_N2_NULL_FULL_JSON_PATH == ("protocol_payload", "n2_null_full")


def test_seeds_distinct_from_b():
    assert proto.LABEL_PERM_SEED_C != 20260514
    assert proto.ASSET_STRAT_DIAG_SEED_C != 20260515


def test_bucket_counts_tuple():
    assert proto.BUCKET_COUNTS == (12, 10)


def test_verdict_class_names_exact():
    assert proto.VERDICT_CLASS_NAMES == (
        "12-privileged",
        "10-privileged",
        "Tied / both-structured",
        "Non-confirmatory / unresolved",
    )


# ── Surfaces and observed ────────────────────────────────────────────────────

def test_pss_surface_365_entries_both_k():
    r = _synthetic_reduced()
    s12 = proto.pss_surface(r, 12)
    s10 = proto.pss_surface(r, 10)
    assert len(s12) == 365 and set(s12.keys()) == set(range(1, 366))
    assert len(s10) == 365 and set(s10.keys()) == set(range(1, 366))


def test_median_pss_odd_n_middle_order_statistic():
    surface = {d: float(d) for d in range(1, 366)}
    assert proto.median_pss(surface) == 183.0


def test_compute_observed_outcomes_keys():
    r = _synthetic_reduced()
    o = proto.compute_observed_outcomes(r)
    for k in (
        "median_12_observed",
        "median_10_observed",
        "diff_observed",
        "pss_surface_12",
        "pss_surface_10",
    ):
        assert k in o
    assert o["diff_observed"] == pytest.approx(
        o["median_12_observed"] - o["median_10_observed"]
    )
    assert len(o["pss_surface_12"]) == 365
    assert "1" in o["pss_surface_12"]  # str keys


# ── Shared permutation pool ──────────────────────────────────────────────────

def test_pool_lengths():
    r = _synthetic_reduced()
    pool = proto.run_shared_permutation_pool(r, n_perm=100, seed=proto.LABEL_PERM_SEED_C)
    for key in ("matched_null_12", "matched_null_10", "comparison_null"):
        assert pool[key].shape == (100,)


def test_pool_coupling_invariant():
    r = _synthetic_reduced()
    pool = proto.run_shared_permutation_pool(r, n_perm=100, seed=123)
    np.testing.assert_allclose(
        pool["comparison_null"],
        pool["matched_null_12"] - pool["matched_null_10"],
        rtol=0, atol=0,
    )


def test_pool_determinism_same_seed():
    r = _synthetic_reduced()
    a = proto.run_shared_permutation_pool(r, n_perm=100, seed=999)
    b = proto.run_shared_permutation_pool(r, n_perm=100, seed=999)
    for key in ("matched_null_12", "matched_null_10", "comparison_null"):
        np.testing.assert_array_equal(a[key], b[key])


def test_pool_diverges_different_seed():
    r = _synthetic_reduced()
    a = proto.run_shared_permutation_pool(r, n_perm=100, seed=1)
    b = proto.run_shared_permutation_pool(r, n_perm=100, seed=2)
    assert not np.array_equal(a["matched_null_12"], b["matched_null_12"])


# ── Beat counts ──────────────────────────────────────────────────────────────

def test_beat_counts_strict_ties_do_not_pass():
    observed = {
        "median_12_observed": 0.5,
        "median_10_observed": 0.4,
        "diff_observed": 0.1,
    }
    pool = {
        "matched_null_12": np.array([0.5, 0.5, 0.4, 0.6]),  # two ties at 0.5
        "matched_null_10": np.array([0.4, 0.4, 0.3, 0.5]),
        "comparison_null": np.array([0.1, 0.1, 0.05, 0.2]),
    }
    bc = proto.compute_beat_counts(observed, pool)
    # only values strictly < observed count
    assert bc["beat_count_12_individual"] == 1  # only 0.4 < 0.5
    assert bc["beat_count_10_individual"] == 1  # only 0.3 < 0.4
    assert bc["beat_count_comparison_12"] == 1  # only 0.05 < 0.1
    assert bc["beat_count_comparison_10"] == 1  # only 0.2 > 0.1


def test_comparison_beatcount_algebra():
    r = _synthetic_reduced()
    o = proto.compute_observed_outcomes(r)
    pool = proto.run_shared_permutation_pool(r, n_perm=100, seed=55)
    bc = proto.compute_beat_counts(o, pool)
    ties = int((pool["comparison_null"] == o["diff_observed"]).sum())
    assert (
        bc["beat_count_comparison_12"]
        + bc["beat_count_comparison_10"]
        + ties
        == 100
    )


# ── Verdict map ──────────────────────────────────────────────────────────────

def test_verdict_class_1():
    bc = {
        "beat_count_12_individual": 9600,
        "beat_count_10_individual": 100,
        "beat_count_comparison_12": 9700,
        "beat_count_comparison_10": 300,
    }
    v = proto.evaluate_verdict(bc, 9500)
    assert v["verdict_class"] == "12-privileged"
    assert v["verdict_class_machine"] == "class_1"


def test_verdict_class_2():
    bc = {
        "beat_count_12_individual": 100,
        "beat_count_10_individual": 9600,
        "beat_count_comparison_12": 200,
        "beat_count_comparison_10": 9800,
    }
    v = proto.evaluate_verdict(bc, 9500)
    assert v["verdict_class"] == "10-privileged"
    assert v["verdict_class_machine"] == "class_2"


def test_verdict_class_3():
    bc = {
        "beat_count_12_individual": 9700,
        "beat_count_10_individual": 9700,
        "beat_count_comparison_12": 5000,
        "beat_count_comparison_10": 5000,
    }
    v = proto.evaluate_verdict(bc, 9500)
    assert v["verdict_class"] == "Tied / both-structured"
    assert v["verdict_class_machine"] == "class_3"


def test_verdict_class_4_residual():
    bc = {
        "beat_count_12_individual": 100,
        "beat_count_10_individual": 100,
        "beat_count_comparison_12": 100,
        "beat_count_comparison_10": 100,
    }
    v = proto.evaluate_verdict(bc, 9500)
    assert v["verdict_class"] == "Non-confirmatory / unresolved"
    assert v["verdict_class_machine"] == "class_4"


def test_verdict_class_4_heterogeneous_only_individual_12():
    # 12 individually passes, both comparison thresholds fail -> still Class 4.
    bc = {
        "beat_count_12_individual": 9900,
        "beat_count_10_individual": 100,
        "beat_count_comparison_12": 4000,
        "beat_count_comparison_10": 6000,
    }
    v = proto.evaluate_verdict(bc, 9500)
    assert v["verdict_class"] == "Non-confirmatory / unresolved"
    assert v["verdict_class_machine"] == "class_4"


def test_verbalization_matches_memo_for_each_class():
    headings = {
        "class_1": "### Class 1 — 12-privileged",
        "class_2": "### Class 2 — 10-privileged",
        "class_3": "### Class 3 — Tied / both-structured",
        "class_4": "### Class 4 — Non-confirmatory / unresolved",
    }
    for machine, heading in headings.items():
        expected = _extract_ab(heading)
        assert proto.VERBALIZATION_BLOCKS[machine] == expected, machine


def test_evaluate_verdict_emits_matching_verbalization():
    bc = {
        "beat_count_12_individual": 9600,
        "beat_count_10_individual": 100,
        "beat_count_comparison_12": 9700,
        "beat_count_comparison_10": 300,
    }
    v = proto.evaluate_verdict(bc, 9500)
    assert v["verbalization"] == _extract_ab("### Class 1 — 12-privileged")


# ── Asset-stratified diagnostic ──────────────────────────────────────────────

def test_asset_stratified_three_coupled_nulls():
    r = _synthetic_reduced()
    d = proto.run_asset_stratified_diagnostic(
        r, n_perm=80, seed=proto.ASSET_STRAT_DIAG_SEED_C
    )
    for key in ("matched_null_12", "matched_null_10", "comparison_null"):
        assert d[key].shape == (80,)
    np.testing.assert_allclose(
        d["comparison_null"],
        d["matched_null_12"] - d["matched_null_10"],
        rtol=0, atol=0,
    )


def test_asset_stratified_beat_counts_computable_and_nonverdict():
    r = _synthetic_reduced()
    o = proto.compute_observed_outcomes(r)
    d = proto.run_asset_stratified_diagnostic(r, n_perm=80, seed=777)
    bc = proto.compute_beat_counts(o, d)
    assert set(bc.keys()) == {
        "beat_count_12_individual",
        "beat_count_10_individual",
        "beat_count_comparison_12",
        "beat_count_comparison_10",
    }
    # diagnostic beat counts are just ints; they do not feed evaluate_verdict
    v = proto.evaluate_verdict(
        {
            "beat_count_12_individual": 0,
            "beat_count_10_individual": 0,
            "beat_count_comparison_12": 0,
            "beat_count_comparison_10": 0,
        },
        9500,
    )
    assert v["verdict_class"] == "Non-confirmatory / unresolved"


# ── Provenance check ─────────────────────────────────────────────────────────

def test_provenance_pass_on_matching_surface(tmp_path):
    r = _synthetic_reduced()
    s12 = proto.pss_surface(r, 12)
    fake = _write_fake_b_log(tmp_path, s12)
    res = proto.verify_b_provenance(
        {str(k): v for k, v in s12.items()}, fake, 1e-12
    )
    assert res["pass"] is True
    assert res["n_anchors_checked"] == 365
    assert res["max_abs_diff"] <= 1e-12


def test_provenance_raises_on_perturbation(tmp_path):
    r = _synthetic_reduced()
    s12 = proto.pss_surface(r, 12)
    perturbed = dict(s12)
    perturbed[200] = perturbed[200] + 1e-6
    fake = _write_fake_b_log(tmp_path, s12)
    with pytest.raises(RuntimeError):
        proto.verify_b_provenance(
            {str(k): v for k, v in perturbed.items()}, fake, 1e-12
        )


# ── Full run, rerun gate, header ─────────────────────────────────────────────

def _run_with_fake_b(tmp_path, r, n_perm=60):
    s12 = proto.pss_surface(r, 12)
    fake = _write_fake_b_log(tmp_path, s12)
    return proto.run(r, fake, n_perm=n_perm), fake


def test_run_payload_structure(tmp_path):
    r = _synthetic_reduced()
    payload, _ = _run_with_fake_b(tmp_path, r, n_perm=60)
    for k in (
        "observed",
        "beat_counts",
        "threshold_pass",
        "verdict_class",
        "verdict_class_machine",
        "verbalization",
        "matched_null_12_full",
        "matched_null_10_full",
        "comparison_null_full",
        "pss_surface_12",
        "pss_surface_10",
        "asset_stratified_diagnostic",
        "diagnostics",
        "bucket_counts",
        "seeds",
        "locked_parameters",
    ):
        assert k in payload, k
    assert payload["verdict_class"] in proto.VERDICT_CLASS_NAMES
    assert len(payload["matched_null_12_full"]) == 60
    d = payload["diagnostics"]
    for k in (
        "best_anchor_pss_12",
        "best_anchor_pss_10",
        "anchor_distribution_shape_12",
        "anchor_distribution_shape_10",
        "per_asset_pss_civil_march20_12",
        "per_asset_pss_civil_march20_10",
        "per_asset_pss_peak_anchor_12",
        "per_asset_pss_peak_anchor_10",
        "top_10_anchors_12",
        "top_10_anchors_10",
        "provenance_check",
    ):
        assert k in d, k
    assert d["provenance_check"]["pass"] is True


def test_run_payload_json_serializable(tmp_path):
    r = _synthetic_reduced()
    payload, _ = _run_with_fake_b(tmp_path, r, n_perm=40)
    s = json.dumps(payload, ensure_ascii=False)
    assert isinstance(s, str) and len(s) > 0
    # also canonicalizable by B's rerun gate
    cb = canonicalize_protocol_payload(payload)
    assert isinstance(cb, (bytes, bytearray))


def test_rerun_gate_determinism(tmp_path):
    r = _synthetic_reduced()
    s12 = proto.pss_surface(r, 12)
    fake = _write_fake_b_log(tmp_path, s12)

    def runner():
        return proto.run(r, fake, n_perm=60)

    cb = assert_byte_identical_reruns(runner)
    assert isinstance(cb, (bytes, bytearray))


def test_rerun_gate_detects_perturbation(tmp_path):
    r = _synthetic_reduced()
    payload, _ = _run_with_fake_b(tmp_path, r, n_perm=40)
    a = canonicalize_protocol_payload(payload)
    perturbed = json.loads(json.dumps(payload))
    perturbed["observed"]["median_12_observed"] += 1e-9
    b = canonicalize_protocol_payload(perturbed)
    assert a != b


def test_header_excludes_protocol_payload(tmp_path):
    from candidate_b_loader import FROZEN_DATASETS

    observed_hashes = {p: FROZEN_DATASETS[p] for p in FROZEN_DATASETS}
    header = compose_header(
        repo_root=REPO_ROOT,
        observed_hashes=observed_hashes,
        manifest_sha="0" * 64,
        run_timestamp_utc="2026-05-15T00:00:00Z",
        rerun_verification_digest="a" * 64,
    )
    for forbidden in (
        "observed",
        "beat_counts",
        "verdict_class",
        "matched_null_12_full",
        "diagnostics",
        "verbalization",
    ):
        assert forbidden not in header
    for required in (
        "rerun_verification_digest",
        "seeds",
        "locked_parameters",
        "frozen_csv_inputs",
        "design_memo_commit",
        "lock_acceptance_commit",
    ):
        assert required in header


def test_markdown_render_contains_required_blocks(tmp_path):
    r = _synthetic_reduced()
    payload, _ = _run_with_fake_b(tmp_path, r, n_perm=40)
    full = {
        "schema_version": "candidate_c_v0.1",
        "header": {
            "design_memo_path": "docs/candidate_c_design_memo_v0.1.md",
            "active_memo_version": "v0.1",
            "design_memo_commit": "401ce45",
            "lock_acceptance_commit": "dc97576",
            "freeze_commit": "5225bfd",
            "run_timestamp_utc": "2026-05-15T00:00:00Z",
            "repo_commit_before_run": "abc123",
            "rerun_verification_digest": "d" * 64,
            "seeds": {"N_PERM": 10000},
            "locked_parameters": {"beat_count_threshold": 9500},
        },
        "protocol_payload": payload,
        "disclosure_paragraph_section_12_4": DISCLOSURE_SECTION_12_4,
        "disclosure_paragraph_section_12_5": DISCLOSURE_SECTION_12_5,
        "disclosure_paragraph_section_13": DISCLOSURE_SECTION_13,
    }
    md = render_markdown(full)
    assert "beat_count_12_individual" in md
    assert "beat_count_10_individual" in md
    assert "beat_count_comparison_12" in md
    assert "beat_count_comparison_10" in md
    assert payload["verdict_class"] in md
    assert "This caveat applies to all four verdict classes." in md
    assert "not independent p-value claims" in md
    assert "a hash citation alone does not satisfy" in md


def test_disclosures_are_verbatim_from_memo():
    memo = open(C_MEMO, encoding="utf-8").read()
    # section 12.5 is a single blockquote line; strip "> "
    l356 = memo.split("\n")
    s125 = next(l[2:] for l in l356 if l.startswith("> The four beat counts"))
    assert DISCLOSURE_SECTION_12_5 == s125
    s13 = next(l[2:] for l in l356 if l.startswith("> Candidate C's verdict"))
    assert DISCLOSURE_SECTION_13 == s13


# ── Gated integration test against the real Candidate B verdict log ──────────

@pytest.mark.skipif(
    not os.environ.get("CANDIDATE_C_INTEGRATION"),
    reason="set CANDIDATE_C_INTEGRATION=1 to run the real-data provenance test",
)
def test_provenance_against_real_b_verdict_log():
    from candidate_b_loader import load_reduced_phase3b_pool

    reduced = load_reduced_phase3b_pool(REPO_ROOT)
    surface_12 = proto.pss_surface(reduced, 12)
    res = proto.verify_b_provenance(
        {str(k): v for k, v in surface_12.items()}, B_REAL_LOG, 1e-12
    )
    assert res["pass"] is True
    assert res["n_anchors_checked"] == 365
    assert res["max_abs_diff"] <= 1e-12
