"""End-to-end tests for the Influential Numbers Cell 1 locked protocol.

Mirrors tests/test_candidate_c_protocol.py (commit 4432591), adapted to the
Cell 1 design surface: multi-focal F = {10,12,14,16}, K = {7,...,19},
focal-centered attenuation, focal-elevation gate, max_gap, two primary beat
counts, the four-class verdict map with a hard-binary Class 4, and the
section 17 provenance gate against Candidate C's stored surfaces.

Synthetic in-memory fixtures only, except one gated integration test
(CELL1_INTEGRATION=1) that exercises provenance against the real Candidate C
verdict log. Runner-adjacent tests are included in this file (no fourth test
module; the locked file list expects exactly three) and skip cleanly if the
runner is not yet importable.
"""

import json
import math
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

import influential_numbers_cell_1_protocol as proto
from candidate_b_loader import ReducedTrades

CELL1_MEMO = os.path.join(
    REPO_ROOT, "docs", "influential_numbers_cell_1_design_memo_v0.1.md"
)
REAL_C_LOG = os.path.join(
    REPO_ROOT, "results", "candidate_c_results_20260515_051236_f3a6bf48.json"
)

try:
    import run_influential_numbers_cell_1_protocol as runner  # noqa: E402
    _RUNNER = True
except Exception:  # pragma: no cover - runner not yet promoted
    runner = None
    _RUNNER = False

_need_runner = pytest.mark.skipif(
    not _RUNNER, reason="Cell 1 runner module not importable yet"
)


# ── Fixtures ─────────────────────────────────────────────────────────────────

def _synthetic_reduced(seed=4242, n=60, assets=("SPY", "EFA", "GLD")):
    rng = np.random.Generator(np.random.PCG64(seed))
    assets_arr = np.array(list(assets), dtype=object)
    asset = rng.choice(assets_arr, size=n)
    start = date(2010, 1, 1)
    offs = rng.integers(0, 365 * 6, size=n)
    entry = np.array(
        [start + timedelta(days=int(o)) for o in offs], dtype=object
    )
    exit_ = np.array(
        [d + timedelta(days=int(rng.integers(3, 25))) for d in entry],
        dtype=object,
    )
    is_long = (rng.integers(0, 2, size=n) == 1)
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


def _full_median_map(center_value_at=12, peak=0.05, slope=0.005):
    """A K-wide median map peaked at one focal, linear falloff in |k-center|."""
    return {
        k: peak - slope * abs(k - center_value_at)
        for k in range(7, 20)
    }


def _write_fake_c_log(tmp_path, surf10_int, surf12_int):
    payload = {
        "protocol_payload": {
            "pss_surface_10": {str(d): float(v) for d, v in surf10_int.items()},
            "pss_surface_12": {str(d): float(v) for d, v in surf12_int.items()},
        }
    }
    p = tmp_path / "fake_c_log.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return str(p)


def _memo_lines():
    return open(CELL1_MEMO, encoding="utf-8").read().split("\n")


def _verbatim_line(tag_substring):
    """Return the memo body line carrying tag_substring, structural prefix
    ('> ' for blockquotes, '* ' for guardrail bullets) removed only."""
    for ln in _memo_lines():
        if tag_substring in ln:
            if ln.startswith("> "):
                return ln[2:]
            if ln.startswith("* "):
                return ln[2:]
            return ln
    raise AssertionError("tag not found in memo: " + tag_substring)


# ── A. Constants and locked design ───────────────────────────────────────────

def test_locked_seeds_and_constants():
    assert proto.LABEL_PERM_SEED_CELL1 == 20260518
    assert proto.ASSET_STRAT_DIAG_SEED_CELL1 == 20260519
    assert proto.N_PERM == 10_000
    assert proto.BEAT_COUNT_THRESHOLD == 9_500
    assert proto.FOCAL_CENTERS == (10, 12, 14, 16)
    assert proto.PRIMARY_FOCAL == 12
    assert proto.CONTROL_FOCALS == (10, 14, 16)
    assert proto.BUCKET_COUNTS == tuple(range(7, 20))
    assert proto.WINDOW_RADIUS == 3


def test_commit_constants():
    assert proto.FRAMEWORK_MEMO_COMMIT == "8ff619c"
    assert proto.DESIGN_MEMO_COMMIT == "a765098"
    assert proto.LOCK_COMMIT == "3d44e9e"
    assert proto.FREEZE_COMMIT == "5225bfd"


def test_candidate_c_verdict_log_sha_constant():
    assert proto.CANDIDATE_C_VERDICT_LOG_SHA256 == (
        "130235fef110cca141fa8873bfa3a6c630a44ac11dfcad953822f41f9cd3c7d4"
    )
    assert proto.C_SURFACE_JSON_KEYS == ("pss_surface_10", "pss_surface_12")
    assert proto.PROVENANCE_TOLERANCE == 1e-12


def test_verdict_display_names_exact():
    assert proto.VERDICT_CLASS_NAMES == (
        "12-centered neighborhood structure",
        "Generic substrate smoothness",
        "No neighborhood evidence",
        "Non-confirmatory / unresolved",
    )
    assert proto._MACHINE_TO_DISPLAY["class_1"] == \
        "12-centered neighborhood structure"
    assert proto._MACHINE_TO_DISPLAY["class_4"] == \
        "Non-confirmatory / unresolved"


# ── B. Focal windows / distance vectors ──────────────────────────────────────

def test_window_for_focal_exact():
    assert proto.window_for_focal(10) == (7, 8, 9, 10, 11, 12, 13)
    assert proto.window_for_focal(12) == (9, 10, 11, 12, 13, 14, 15)
    assert proto.window_for_focal(14) == (11, 12, 13, 14, 15, 16, 17)
    assert proto.window_for_focal(16) == (13, 14, 15, 16, 17, 18, 19)


def test_distance_vector_alignment_and_multiset():
    dv = proto.distance_vector_for_focal(12)
    assert list(dv) == [3.0, 2.0, 1.0, 0.0, 1.0, 2.0, 3.0]
    assert sorted(int(x) for x in dv) == [0, 1, 1, 2, 2, 3, 3]


def test_all_window_members_within_K():
    for f in proto.FOCAL_CENTERS:
        for k in proto.window_for_focal(f):
            assert k in proto.BUCKET_COUNTS


# ── C. OLS / attenuation ─────────────────────────────────────────────────────

def test_ols_slope_negative_for_decreasing_y():
    x = proto.distance_vector_for_focal(12)
    y = np.array([0.0, 0.1, 0.2, 0.5, 0.2, 0.1, 0.0])  # peak at distance 0
    assert proto.ols_slope(x, y) < 0.0


def test_ols_slope_zero_for_flat_y():
    x = proto.distance_vector_for_focal(12)
    y = np.full(7, 0.3)
    assert proto.ols_slope(x, y) == pytest.approx(0.0, abs=1e-12)


def test_ols_slope_rejects_non_finite():
    x = proto.distance_vector_for_focal(12)
    y = np.array([0.5, 0.4, 0.3, np.nan, 0.3, 0.4, 0.5])
    with pytest.raises(proto.CellOnePathology):
        proto.ols_slope(x, y)


def test_ols_slope_rejects_zero_variance_x():
    with pytest.raises(proto.CellOnePathology):
        proto.ols_slope(np.zeros(7), np.arange(7.0))


def test_attenuation_positive_for_focal_peak():
    mm = _full_median_map(12, peak=0.05, slope=0.004)
    assert proto.attenuation_score_for_focal(mm, 12) > 0.0


def test_attenuation_uses_all_seven_points_incl_focal():
    mm = _full_median_map(12)
    # removing the focal key must break it (focal is part of the regression)
    broken = dict(mm)
    del broken[12]
    with pytest.raises(proto.CellOnePathology):
        proto.attenuation_score_for_focal(broken, 12)


def test_attenuation_non_positive_when_focal_is_trough():
    mm = {k: 0.01 * abs(k - 12) for k in range(7, 20)}  # trough at 12
    assert proto.attenuation_score_for_focal(mm, 12) <= 0.0


def test_compute_attenuation_scores_all_focals():
    mm = _full_median_map(12)
    scores = proto.compute_attenuation_scores(mm)
    assert set(scores.keys()) == set(proto.FOCAL_CENTERS)


# ── D. Focal-elevation gate ──────────────────────────────────────────────────

def test_gate_pass_when_focal_above_neighbor_mean():
    mm = _full_median_map(12, peak=0.05, slope=0.004)
    g = proto.focal_elevation_gate_12(mm)
    assert g["pass"] is True
    assert g["ambiguous"] is False


def test_gate_fail_when_focal_below_neighbor_mean():
    mm = {k: 0.01 * abs(k - 12) for k in range(7, 20)}  # trough at 12
    g = proto.focal_elevation_gate_12(mm)
    assert g["pass"] is False
    assert g["ambiguous"] is False


def test_gate_exact_tie_is_ambiguous():
    # 0.5 is exactly binary-representable, so mean([0.5]*6) == 0.5 bit-exactly
    # and median_12 == neighbor_mean is a true exact tie. (0.2 is not
    # binary-exact, so its six-element mean was 0.20000000000000004 != 0.2.)
    mm = {k: 0.5 for k in range(7, 20)}  # median_12 == neighbor mean exactly
    g = proto.focal_elevation_gate_12(mm)
    assert g["ambiguous"] is True
    assert g["pass"] is False


def test_gate_non_finite_is_ambiguous():
    mm = _full_median_map(12)
    mm[12] = math.inf
    g = proto.focal_elevation_gate_12(mm)
    assert g["ambiguous"] is True


def test_gate_neighbor_set_is_exactly_9_10_11_13_14_15():
    win = proto.window_for_focal(12)
    nonfocal = tuple(k for k in win if k != 12)
    assert nonfocal == (9, 10, 11, 13, 14, 15)


# ── E. max_gap ───────────────────────────────────────────────────────────────

def test_max_gap_formula_and_strongest_control():
    scores = {10: 0.1, 12: 0.5, 14: 0.3, 16: 0.2}
    mg = proto.compute_max_gap(scores)
    assert mg["max_gap"] == pytest.approx(0.5 - 0.3)
    assert mg["strongest_control_focal"] == 14
    assert mg["strongest_control_score"] == pytest.approx(0.3)


def test_max_gap_can_be_negative():
    scores = {10: 0.9, 12: 0.1, 14: 0.2, 16: 0.3}
    mg = proto.compute_max_gap(scores)
    assert mg["max_gap"] == pytest.approx(0.1 - 0.9)
    assert mg["strongest_control_focal"] == 10


# ── F. PSS surface / observed outcomes ───────────────────────────────────────

def test_pss_surface_365_entries():
    reduced = _synthetic_reduced(n=40)
    s = proto.pss_surface(reduced, 12)
    assert len(s) == 365
    assert set(s.keys()) == set(range(1, 366))


def test_median_pss_is_183rd_order_statistic():
    surface = {d: float(d) for d in range(1, 366)}  # 1..365
    assert proto.median_pss(surface) == 183.0


def test_compute_median_pss_map_keys_7_to_19():
    reduced = _synthetic_reduced(n=40)
    mm = proto.compute_median_pss_map(reduced)
    assert set(mm.keys()) == set(range(7, 20))


def test_compute_observed_outcomes_keys():
    reduced = _synthetic_reduced(n=40)
    obs = proto.compute_observed_outcomes(reduced)
    for key in (
        "median_pss_by_k", "pss_surfaces_by_k", "attenuation_scores",
        "focal_elevation_gate_12", "max_gap",
    ):
        assert key in obs
    assert set(obs["attenuation_scores"].keys()) == set(proto.FOCAL_CENTERS)


# ── G. Permutation pool ──────────────────────────────────────────────────────

def test_pool_lengths_and_keys():
    reduced = _synthetic_reduced(n=40)
    pool = proto.run_shared_permutation_pool(reduced, n_perm=12, seed=1)
    assert set(pool.keys()) == {"attenuation_score_12_null", "max_gap_null"}
    assert len(pool["attenuation_score_12_null"]) == 12
    assert len(pool["max_gap_null"]) == 12


def test_pool_deterministic_same_seed():
    reduced = _synthetic_reduced(n=40)
    a = proto.run_shared_permutation_pool(reduced, n_perm=10, seed=20260518)
    b = proto.run_shared_permutation_pool(reduced, n_perm=10, seed=20260518)
    assert np.array_equal(a["attenuation_score_12_null"],
                          b["attenuation_score_12_null"])
    assert np.array_equal(a["max_gap_null"], b["max_gap_null"])


def test_pool_diverges_different_seed():
    reduced = _synthetic_reduced(n=40)
    a = proto.run_shared_permutation_pool(reduced, n_perm=10, seed=1)
    b = proto.run_shared_permutation_pool(reduced, n_perm=10, seed=2)
    assert not np.array_equal(a["attenuation_score_12_null"],
                              b["attenuation_score_12_null"])


def test_pool_all_finite():
    reduced = _synthetic_reduced(n=40)
    pool = proto.run_shared_permutation_pool(reduced, n_perm=10, seed=7)
    assert np.isfinite(pool["attenuation_score_12_null"]).all()
    assert np.isfinite(pool["max_gap_null"]).all()


def test_pool_coupling_same_index_same_permutation():
    # max_gap_null[i] - attenuation_score_12_null[i] equals -max(control
    # scores at permutation i): both derive from the same K-wide median map,
    # so the implied strongest-control series is finite and consistent.
    reduced = _synthetic_reduced(n=40)
    pool = proto.run_shared_permutation_pool(reduced, n_perm=8, seed=3)
    implied_control = (
        pool["attenuation_score_12_null"] - pool["max_gap_null"]
    )
    assert np.isfinite(implied_control).all()
    assert len(implied_control) == 8


# ── H. Beat counts ───────────────────────────────────────────────────────────

def test_beat_counts_strict_ties_do_not_pass():
    observed = {
        "attenuation_scores": {12: 0.50},
        "max_gap": {"max_gap": 0.20},
    }
    pool = {
        "attenuation_score_12_null": np.array([0.49, 0.50, 0.51, 0.10]),
        "max_gap_null": np.array([0.19, 0.20, 0.21, 0.05]),
    }
    bc = proto.compute_beat_counts(observed, pool)
    # strict <: 0.50 beats {0.49,0.10}=2 (0.50 tie excluded); 0.20 beats
    # {0.19,0.05}=2 (0.20 tie excluded)
    assert bc["beat_count_12_structure"] == 2
    assert bc["beat_count_max_gap"] == 2


# ── I. Verdict map ───────────────────────────────────────────────────────────

_GATE_PASS = {"pass": True, "ambiguous": False}
_GATE_FAIL = {"pass": False, "ambiguous": False}
_GATE_AMBIG = {"pass": False, "ambiguous": True}


def test_verdict_class_1():
    v = proto.evaluate_verdict(
        _GATE_PASS,
        {"beat_count_12_structure": 9500, "beat_count_max_gap": 9500},
        9500, None,
    )
    assert v["verdict_class_machine"] == "class_1"
    assert v["verdict_class"] == "12-centered neighborhood structure"


def test_verdict_class_2():
    v = proto.evaluate_verdict(
        _GATE_PASS,
        {"beat_count_12_structure": 9700, "beat_count_max_gap": 9499},
        9500, None,
    )
    assert v["verdict_class_machine"] == "class_2"
    assert v["verdict_class"] == "Generic substrate smoothness"


def test_verdict_class_3_gate_fail():
    v = proto.evaluate_verdict(
        _GATE_FAIL,
        {"beat_count_12_structure": 9999, "beat_count_max_gap": 9999},
        9500, None,
    )
    assert v["verdict_class_machine"] == "class_3"


def test_verdict_class_3_bc12_below_threshold():
    v = proto.evaluate_verdict(
        _GATE_PASS,
        {"beat_count_12_structure": 9499, "beat_count_max_gap": 9999},
        9500, None,
    )
    assert v["verdict_class_machine"] == "class_3"


def test_verdict_class_4_pathology():
    v = proto.evaluate_verdict(
        _GATE_PASS,
        {"beat_count_12_structure": 9999, "beat_count_max_gap": 9999},
        9500, "provenance failure: ...",
    )
    assert v["verdict_class_machine"] == "class_4"
    assert v["verdict_class"] == "Non-confirmatory / unresolved"


def test_verdict_class_4_gate_ambiguous():
    v = proto.evaluate_verdict(
        _GATE_AMBIG,
        {"beat_count_12_structure": 9999, "beat_count_max_gap": 9999},
        9500, None,
    )
    assert v["verdict_class_machine"] == "class_4"


def test_hard_binary_9499_is_not_class_4():
    # near-threshold below 9500 with a valid (non-ambiguous) gate is a fail
    # routed to Class 3, never the pathology class.
    v = proto.evaluate_verdict(
        _GATE_PASS,
        {"beat_count_12_structure": 9499, "beat_count_max_gap": 9499},
        9500, None,
    )
    assert v["verdict_class_machine"] == "class_3"
    assert v["verdict_class_machine"] != "class_4"


def test_hard_binary_bc12_pass_bcmax_9499_is_class_2_not_class_4():
    v = proto.evaluate_verdict(
        _GATE_PASS,
        {"beat_count_12_structure": 9500, "beat_count_max_gap": 9499},
        9500, None,
    )
    assert v["verdict_class_machine"] == "class_2"


# ── J. Asset-stratified diagnostic ───────────────────────────────────────────

def test_asset_stratified_diagnostic_shape_and_seed():
    reduced = _synthetic_reduced(n=48)
    d = proto.run_asset_stratified_diagnostic(
        reduced, n_perm=8, seed=proto.ASSET_STRAT_DIAG_SEED_CELL1
    )
    assert "asset_stratified_beat_count_12_structure" in d
    assert "asset_stratified_beat_count_max_gap" in d
    assert len(d["attenuation_score_12_null"]) == 8
    assert len(d["max_gap_null"]) == 8


def test_asset_stratified_is_diagnostic_only():
    # The diagnostic does not feed evaluate_verdict; verdict ignores it.
    v_no_path = proto.evaluate_verdict(
        _GATE_PASS,
        {"beat_count_12_structure": 9999, "beat_count_max_gap": 9999},
        9500, None,
    )
    assert v_no_path["verdict_class_machine"] == "class_1"


# ── K. Strict monotonic diagnostic ───────────────────────────────────────────

def test_strict_monotonic_diagnostic_both_sides():
    mm = _full_median_map(12, peak=0.05, slope=0.004)
    r = proto.strict_monotonic_diagnostic(mm, 12)
    assert r["computable"] is True
    assert r["left_non_increasing"] is True
    assert r["right_non_increasing"] is True


def test_strict_monotonic_detects_non_monotone():
    mm = _full_median_map(12, peak=0.05, slope=0.004)
    mm[14] = 0.999  # break the right side
    r = proto.strict_monotonic_diagnostic(mm, 12)
    assert r["right_non_increasing"] is False


# ── L. Candidate C provenance ────────────────────────────────────────────────

def _surfaces_for(reduced):
    obs = proto.compute_observed_outcomes(reduced)
    return obs["pss_surfaces_by_k"]


def test_provenance_pass_on_matching_surface(tmp_path, monkeypatch):
    reduced = _synthetic_reduced(n=40)
    surfaces = _surfaces_for(reduced)
    path = _write_fake_c_log(tmp_path, surfaces[10], surfaces[12])
    monkeypatch.setattr(
        proto, "CANDIDATE_C_VERDICT_LOG_SHA256", proto._file_sha256(path)
    )
    res = proto.verify_candidate_c_provenance(surfaces, path, 1e-12)
    assert res["pass"] is True
    assert res["max_abs_diff_10"] == 0.0
    assert res["max_abs_diff_12"] == 0.0
    assert res["n_anchors_checked_10"] == 365
    assert res["n_anchors_checked_12"] == 365


def test_provenance_fails_on_perturbation(tmp_path, monkeypatch):
    reduced = _synthetic_reduced(n=40)
    surfaces = _surfaces_for(reduced)
    perturbed12 = dict(surfaces[12])
    perturbed12[1] = perturbed12[1] + 1e-6
    path = _write_fake_c_log(tmp_path, surfaces[10], perturbed12)
    monkeypatch.setattr(
        proto, "CANDIDATE_C_VERDICT_LOG_SHA256", proto._file_sha256(path)
    )
    res = proto.verify_candidate_c_provenance(surfaces, path, 1e-12)
    assert res["pass"] is False
    assert "tolerance" in (res["failure_reason"] or "")


def test_provenance_fails_on_sha_mismatch(tmp_path):
    reduced = _synthetic_reduced(n=40)
    surfaces = _surfaces_for(reduced)
    path = _write_fake_c_log(tmp_path, surfaces[10], surfaces[12])
    # do NOT monkeypatch the expected SHA: file sha != hardcoded constant
    res = proto.verify_candidate_c_provenance(surfaces, path, 1e-12)
    assert res["pass"] is False
    assert "SHA-256" in (res["failure_reason"] or "")


@pytest.mark.skipif(
    not os.environ.get("CELL1_INTEGRATION"),
    reason="set CELL1_INTEGRATION=1 to run provenance against the real "
           "Candidate C verdict log (loads the frozen pool)",
)
def test_provenance_against_real_candidate_c_log():
    from candidate_b_loader import load_reduced_phase3b_pool

    reduced = load_reduced_phase3b_pool(REPO_ROOT)
    surfaces = _surfaces_for(reduced)
    res = proto.verify_candidate_c_provenance(
        surfaces, REAL_C_LOG, proto.PROVENANCE_TOLERANCE
    )
    assert res["pass"] is True
    assert res["max_abs_diff_10"] <= 1e-12
    assert res["max_abs_diff_12"] <= 1e-12


# ── M. Run payload ───────────────────────────────────────────────────────────

_REQUIRED_PAYLOAD_KEYS = (
    "active_memo_version", "framework_memo_commit", "design_memo_commit",
    "lock_acceptance_commit", "freeze_commit", "n_trades", "n_perm",
    "anchor_population_size", "bucket_counts", "focal_centers",
    "primary_focal", "control_focals", "window_radius", "locked_parameters",
    "seeds", "observed", "focal_elevation_gate_12", "attenuation_scores",
    "max_gap", "beat_counts", "threshold_pass", "verdict_class",
    "verdict_class_machine", "verbalization", "attenuation_score_12_null_full",
    "max_gap_null_full", "pss_surfaces_by_k", "asset_stratified_diagnostic",
    "diagnostics",
)


def _no_nan_inf(obj):
    if isinstance(obj, float):
        return math.isfinite(obj)
    if isinstance(obj, dict):
        return all(_no_nan_inf(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(_no_nan_inf(v) for v in obj)
    return True


def test_run_payload_structure_and_serializable(tmp_path, monkeypatch):
    reduced = _synthetic_reduced(n=40)
    surfaces = _surfaces_for(reduced)
    path = _write_fake_c_log(tmp_path, surfaces[10], surfaces[12])
    monkeypatch.setattr(
        proto, "CANDIDATE_C_VERDICT_LOG_SHA256", proto._file_sha256(path)
    )
    payload = proto.run(
        reduced, candidate_c_verdict_log_path=path, n_perm=12,
        label_perm_seed=20260518, asset_strat_seed=20260519,
    )
    for k in _REQUIRED_PAYLOAD_KEYS:
        assert k in payload, k
    s = json.dumps(payload)  # must be serializable
    assert isinstance(s, str)
    assert _no_nan_inf(payload)
    # surfaces stringified in payload
    for kk, surf in payload["pss_surfaces_by_k"].items():
        assert isinstance(kk, str)
        assert all(isinstance(d, str) for d in surf.keys())
    assert payload["verdict_class_machine"] in (
        "class_1", "class_2", "class_3", "class_4"
    )


def test_run_provenance_failure_routes_to_class_4(tmp_path):
    reduced = _synthetic_reduced(n=40)
    surfaces = _surfaces_for(reduced)
    path = _write_fake_c_log(tmp_path, surfaces[10], surfaces[12])
    # expected SHA constant left as the real hardcoded value -> mismatch
    payload = proto.run(
        reduced, candidate_c_verdict_log_path=path, n_perm=8,
    )
    assert payload["verdict_class_machine"] == "class_4"
    assert payload["pathology"]
    assert payload["provenance_check"]["pass"] is False
    assert payload["attenuation_score_12_null_full"] == []


# ── N. Required-verbatim blocks ──────────────────────────────────────────────

def _memo_ab_block(class_no):
    lines = _memo_lines()
    a = _verbatim_line("REQUIRED-VERBATIM, §15.{}a".format(class_no))
    b = _verbatim_line("REQUIRED-VERBATIM, §15.{}b".format(class_no))
    return a + "\n\n" + b


def test_verbalization_blocks_match_memo_character_exact():
    for n, machine in (
        (1, "class_1"), (2, "class_2"), (3, "class_3"), (4, "class_4")
    ):
        assert proto.VERBALIZATION_BLOCKS[machine] == _memo_ab_block(n), machine


def test_evaluate_verdict_emits_matching_verbalization():
    v = proto.evaluate_verdict(
        _GATE_PASS,
        {"beat_count_12_structure": 9600, "beat_count_max_gap": 9600},
        9500, None,
    )
    assert v["verbalization"] == _memo_ab_block(1)


# ── O. Runner-adjacent tests (skip if runner not yet importable) ─────────────

@_need_runner
def test_runner_disclosure_constants_verbatim():
    pairs = (
        (runner.DISCLOSURE_SECTION_15_5, "REQUIRED-VERBATIM, §15.5)"),
        (runner.DISCLOSURE_SECTION_15_6, "REQUIRED-VERBATIM, §15.6)"),
        (runner.DISCLOSURE_SECTION_20, "REQUIRED-VERBATIM, §20)"),
        (runner.DISCLOSURE_SECTION_21_3,
         "REQUIRED-VERBATIM anti-rescue — Layer 1 / Layer 2)"),
        (runner.DISCLOSURE_SECTION_21_4,
         "REQUIRED-VERBATIM anti-rescue — cross-cell)"),
    )
    for constant, tag in pairs:
        assert constant == _verbatim_line(tag), tag


@_need_runner
def test_runner_output_stem_and_lock_commit():
    assert runner.OUTPUT_STEM == "influential_numbers_cell_1_results"
    assert runner.LOCK_ACCEPTANCE_COMMIT == "3d44e9e"
    assert runner.LOCK_COMMIT == "3d44e9e"


@_need_runner
def test_runner_assemble_full_excludes_payload_from_digest_inputs():
    full = runner.assemble_full({"h": 1}, {"p": 2})
    assert set(full.keys()) == {
        "schema_version", "header", "protocol_payload",
        "disclosure_paragraph_section_15_5",
        "disclosure_paragraph_section_15_6",
        "disclosure_paragraph_section_20",
        "disclosure_paragraph_section_21_3",
        "disclosure_paragraph_section_21_4",
    }
    assert full["schema_version"] == "influential_numbers_cell_1_v0.1"


@_need_runner
def test_runner_markdown_contains_five_disclosure_sections():
    full = {
        "header": {
            "design_memo_path": "docs/x.md", "active_memo_version": "v0.1",
            "framework_memo_commit": "8ff619c", "design_memo_commit": "a765098",
            "lock_acceptance_commit": "3d44e9e", "freeze_commit": "5225bfd",
            "run_timestamp_utc": "2026-05-15T00:00:00Z",
            "repo_commit_before_run": "deadbeef",
            "rerun_verification_digest": "0" * 64,
            "seeds": {"N_PERM": 10000},
            "locked_parameters": {"beat_count_threshold": 9500},
        },
        "protocol_payload": {
            "verdict_class": "No neighborhood evidence",
            "verdict_class_machine": "class_3",
            "focal_elevation_gate_12": {}, "attenuation_scores": {},
            "max_gap": {}, "beat_counts": {}, "threshold_pass": {},
            "provenance_check": {}, "asset_stratified_diagnostic": {},
            "verbalization": "x", "pathology": None,
        },
        "disclosure_paragraph_section_15_5": "D155",
        "disclosure_paragraph_section_15_6": "D156",
        "disclosure_paragraph_section_20": "D20",
        "disclosure_paragraph_section_21_3": "D213",
        "disclosure_paragraph_section_21_4": "D214",
    }
    md = runner.render_markdown(full)
    for marker in ("§15.5", "§15.6", "§20", "§21.3", "§21.4"):
        assert marker in md
    for body in ("D155", "D156", "D20", "D213", "D214"):
        assert body in md
