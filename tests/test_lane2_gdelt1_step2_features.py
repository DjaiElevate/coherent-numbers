"""Focused tests for the Lane 2 GDELT1 Step 2 daily-feature generator.

These tests pre-register the design-memo locks. They never write the three
Step 2 result-output artifacts and never invoke the `--write-step2-output`
CLI path (which is blocked closed by design until a separate execution-
authorization prompt).
"""

from __future__ import annotations

import copy
import json
import math
import statistics
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

import lane2_gdelt1_step2_features as step2

REPO_ROOT = Path(__file__).resolve().parents[1]
MERGED_DIR = (
    REPO_ROOT
    / "results"
    / "lane2_gdelt1_full_daily_count_build"
    / step2.CANONICAL_MERGED_DIR_BASENAME
)
CLI_SCRIPT = REPO_ROOT / "scripts" / "run_lane2_gdelt1_step2_features.py"


# ----------------------------------------------------------------------------
# Synthetic-fixture helpers
# ----------------------------------------------------------------------------

def _make_input_row(
    civil_date_str: str,
    *,
    offsets: dict[str, int] | None = None,
    coverage_quality_flag: str = "full",
    coverage_completeness: float = 1.0,
    represented_only: bool = False,
    documented_exception_label: str = "",
    t0_file_status: str = "present",
    expected_files: int = 6,
    available_files: int = 6,
) -> dict:
    """Build a single synthetic merged-substrate input row dict."""
    if offsets is None:
        offsets = {col: 0 for col in step2.OFFSET_COLUMNS}
        offsets["rows_from_offset_0"] = 100
    full = {col: int(offsets.get(col, 0)) for col in step2.OFFSET_COLUMNS}
    total = sum(full.values())
    row = {
        "civil_date": civil_date_str,
        "total_row_count": total,
        "t0_file_status": t0_file_status,
        "expected_contributing_files_count": expected_files,
        "available_contributing_files_count": available_files,
        "coverage_quality_flag": coverage_quality_flag,
        "coverage_completeness": coverage_completeness,
        "represented_only": represented_only,
        "documented_exception_label": documented_exception_label,
    }
    row.update(full)
    return row


def _make_increasing_dataset(n: int, start: str = "2013-04-01") -> list[dict]:
    """Make `n` rows with rows_from_offset_0 = i+1 and zero other offsets, so
    total_row_count = i+1 for i in [0, n).  Useful for verifying rolling math."""
    base = date.fromisoformat(start)
    rows = []
    for i in range(n):
        d = (base + timedelta(days=i)).isoformat()
        offsets = {col: 0 for col in step2.OFFSET_COLUMNS}
        offsets["rows_from_offset_0"] = i + 1
        rows.append(_make_input_row(d, offsets=offsets))
    return rows


# ----------------------------------------------------------------------------
# §6 schema — locked names and order
# ----------------------------------------------------------------------------

def test_feature_schema_locked_names_and_order():
    schema = step2.FEATURE_SCHEMA
    # §6.1 identity / passthrough block leads the schema
    assert schema[:6] == (
        "civil_date",
        "represented_only",
        "documented_exception_label",
        "is_known_substrate_gap",
        "terminal_status",
        "coverage_quality_flag",
    )
    # §6.2 raw counts: seven offsets in order, then total_row_count
    assert schema[6:13] == step2.OFFSET_COLUMNS
    assert schema[13] == "total_row_count"
    # §6.3 scale transforms present
    assert "log1p_total_row_count" in schema
    for col in step2.OFFSET_COLUMNS:
        assert ("log1p_" + col) in schema
    # §6.5 share columns and neighbor aggregates
    for share in (
        "offset_0_share_of_total",
        "share_offset_minus_1",
        "share_offset_minus_7",
        "share_offset_minus_30",
        "share_offset_minus_365",
        "share_offset_minus_3650",
        "share_offset_plus_1",
        "neighbor_offset_sum",
        "neighbor_offset_share_of_total",
        "nonzero_offset_count",
    ):
        assert share in schema
    # §6.6 raw-count descriptives present but distinct from z-denominator names
    for w in step2.ROLLING_WINDOWS_MEAN_STD:
        assert f"roll_mean_total_w{w}" in schema
        assert f"roll_std_total_w{w}" in schema
        assert f"roll_mean_log1p_total_w{w}" in schema
        assert f"roll_std_log1p_total_w{w}" in schema
        assert f"roll_z_log1p_total_w{w}" in schema
    for w in step2.ROLLING_WINDOWS_PERCENTILE:
        assert f"roll_pct_log1p_total_w{w}" in schema
    # §6.6 day-over-day + offset_0 share rolling family
    assert "delta_log1p_total_dod" in schema
    assert "roll_mean_offset_0_share_w30" in schema
    assert "roll_std_offset_0_share_w30" in schema
    assert "roll_z_offset_0_share_w30" in schema
    # §6.7 spike flags (locked thresholds)
    for w in step2.ROLLING_WINDOWS_MEAN_STD:
        assert f"spike_w{w}_z_ge_2" in schema
        assert f"spike_w{w}_z_ge_3" in schema
    # §6.8 edge / domain flags trail the schema
    assert schema[-5:] == (
        "is_domain_start_edge",
        "is_rolling_window_warmup",
        "has_full_7d_history",
        "has_full_30d_history",
        "has_full_365d_history",
    )
    # No duplicate names anywhere
    assert len(schema) == len(set(schema))


def test_feature_row_keys_match_schema_exactly_on_synthetic():
    rows = _make_increasing_dataset(40)
    feats = step2.derive_features(rows)
    for r in feats:
        assert tuple(r.keys()) == step2.FEATURE_SCHEMA


# ----------------------------------------------------------------------------
# §11 seven-offset-sum invariant
# ----------------------------------------------------------------------------

def test_seven_offset_sum_invariant_passes_on_synthetic():
    rows = _make_increasing_dataset(10)
    step2.assert_seven_offset_sum_invariant(rows)


def test_seven_offset_sum_invariant_fails_on_corrupt_row():
    rows = _make_increasing_dataset(3)
    rows[1]["total_row_count"] = rows[1]["total_row_count"] + 1  # break invariant
    with pytest.raises(step2.Step2ConformanceError, match="seven-offset-sum"):
        step2.assert_seven_offset_sum_invariant(rows)


# ----------------------------------------------------------------------------
# §10 documented-exception fail-closed checks (synthetic)
# ----------------------------------------------------------------------------

def _doc_exc_synthetic_pair():
    """Build a minimal (rows, metadata) pair containing only the 2022-11-10
    documented-exception row, sized for §10 conformance checks."""
    offsets = {col: 0 for col in step2.OFFSET_COLUMNS}
    offsets["rows_from_offset_minus_1"] = 91
    offsets["rows_from_offset_minus_7"] = 849
    offsets["rows_from_offset_minus_30"] = 327
    row = _make_input_row(
        step2.DOCUMENTED_EXCEPTION_DATE,
        offsets=offsets,
        coverage_quality_flag="right_truncated_2022_seal",
        coverage_completeness=0.8,
        represented_only=True,
        documented_exception_label=step2.DOCUMENTED_EXCEPTION_LABEL,
        t0_file_status="present",
        expected_files=5,
        available_files=4,
    )
    metadata = {
        "documented_exceptions": [
            {
                "chunk_id": "chunk_2022",
                "date": step2.DOCUMENTED_EXCEPTION_DATE,
                "raw_filename": "20221110.export.CSV.zip",
                "label": step2.DOCUMENTED_EXCEPTION_LABEL,
                "catalog_md5": "91e15516016f986e5b8a08712e1de95a",
                "catalog_filesize_bytes": 6714105,
                "http_status": 404,
                "raw_object_parsed": False,
                "rows_recovered": False,
                "no_data_gap": False,
                "recovered": False,
                "known_substrate_gap_amended": False,
                "representation_artifact": "x",
                "representation_artifact_sha256": "y",
                "contract": "z",
                "contract_sha256": "w",
                "source_chunk_output_dir": "p",
                "source_chunk_metadata_sha256": "q",
            }
        ],
    }
    return [row], metadata


def test_doc_exception_passes_when_correct():
    rows, metadata = _doc_exc_synthetic_pair()
    step2.assert_documented_exception_invariants(rows, metadata)


def test_doc_exception_fails_when_missing():
    _, metadata = _doc_exc_synthetic_pair()
    with pytest.raises(step2.Step2ConformanceError, match="missing"):
        step2.assert_documented_exception_invariants([], metadata)


def test_doc_exception_fails_when_label_changed():
    rows, metadata = _doc_exc_synthetic_pair()
    rows[0]["documented_exception_label"] = "OTHER_LABEL"
    with pytest.raises(step2.Step2ConformanceError, match="label mismatch"):
        step2.assert_documented_exception_invariants(rows, metadata)


def test_doc_exception_fails_when_represented_only_false():
    rows, metadata = _doc_exc_synthetic_pair()
    rows[0]["represented_only"] = False
    with pytest.raises(step2.Step2ConformanceError, match="represented_only"):
        step2.assert_documented_exception_invariants(rows, metadata)


def test_doc_exception_fails_when_offset_0_imputed():
    rows, metadata = _doc_exc_synthetic_pair()
    rows[0]["rows_from_offset_0"] = 50  # imputation attempt
    rows[0]["total_row_count"] = step2.DOCUMENTED_EXCEPTION_TOTAL + 50
    with pytest.raises(step2.Step2ConformanceError, match="rows_from_offset_0|total_row_count"):
        step2.assert_documented_exception_invariants(rows, metadata)


def test_doc_exception_fails_when_neighbor_parts_wrong():
    rows, metadata = _doc_exc_synthetic_pair()
    # Keep total at 1267 but shift the neighbor partition away from (91,849,327)
    rows[0]["rows_from_offset_minus_1"] = 100
    rows[0]["rows_from_offset_minus_7"] = 840
    rows[0]["rows_from_offset_minus_30"] = 327
    rows[0]["total_row_count"] = 100 + 840 + 327
    with pytest.raises(step2.Step2ConformanceError, match="neighbor"):
        step2.assert_documented_exception_invariants(rows, metadata)


def test_doc_exception_fails_when_provenance_missing():
    rows, metadata = _doc_exc_synthetic_pair()
    del metadata["documented_exceptions"][0]["catalog_md5"]
    with pytest.raises(step2.Step2ConformanceError, match="provenance"):
        step2.assert_documented_exception_invariants(rows, metadata)


def test_doc_exception_fails_when_metadata_empty():
    rows, _ = _doc_exc_synthetic_pair()
    with pytest.raises(step2.Step2ConformanceError, match="exactly one entry"):
        step2.assert_documented_exception_invariants(rows, {"documented_exceptions": []})


def test_documented_exception_duplicate_row_fails_closed():
    """§10 hard-stop: the documented-exception row must appear EXACTLY once.

    A second civil_date == '2022-11-10' row — even if its fields are identical
    to the canonical row — must fire the duplicate branch in
    `assert_documented_exception_invariants` (the `>1 matches` check). This
    exercises the §10 documented-exception duplicate-row branch specifically,
    independently of any broad date-domain duplicate detection.
    """
    rows, metadata = _doc_exc_synthetic_pair()
    duplicate_row = copy.deepcopy(rows[0])
    rows.append(duplicate_row)
    assert sum(1 for r in rows if r["civil_date"] == step2.DOCUMENTED_EXCEPTION_DATE) == 2
    with pytest.raises(step2.Step2ConformanceError, match=r"appears.*\(>1\)"):
        step2.assert_documented_exception_invariants(rows, metadata)


def test_doc_exception_fails_when_total_row_count_wrong():
    """§10 hard-stop: total_row_count on 2022-11-10 must equal 1267."""
    rows, metadata = _doc_exc_synthetic_pair()
    rows[0]["total_row_count"] = step2.DOCUMENTED_EXCEPTION_TOTAL + 1
    with pytest.raises(
        step2.Step2ConformanceError,
        match=f"total_row_count must be {step2.DOCUMENTED_EXCEPTION_TOTAL}",
    ):
        step2.assert_documented_exception_invariants(rows, metadata)


def test_doc_exception_fails_when_reclassified():
    """§10 hard-stop: the documented-exception row must not be reclassified
    to any terminal_status other than represented_only_documented_exception."""
    rows, metadata = _doc_exc_synthetic_pair()
    # Inject a non-DOC_EXC terminal_status to simulate downstream reclassification.
    rows[0]["terminal_status"] = step2.TERMINAL_STATUS_RAW
    with pytest.raises(
        step2.Step2ConformanceError,
        match="reclassified",
    ):
        step2.assert_documented_exception_invariants(rows, metadata)


# ----------------------------------------------------------------------------
# §9 KSG policy and `known_no_data_gap` enum zoning
# ----------------------------------------------------------------------------

def test_ksg_policy_full_passes_on_synthetic_full_set():
    feats = []
    for d in step2.KNOWN_SUBSTRATE_GAPS:
        feats.append({
            "civil_date": d,
            "is_known_substrate_gap": True,
            "terminal_status": step2.TERMINAL_STATUS_KSG,
            "represented_only": False,
            "documented_exception_label": "",
        })
    step2.assert_ksg_invariants(feats)


def test_ksg_policy_fails_when_one_ksg_missing():
    feats = [
        {
            "civil_date": d,
            "is_known_substrate_gap": True,
            "terminal_status": step2.TERMINAL_STATUS_KSG,
            "represented_only": False,
            "documented_exception_label": "",
        }
        for d in step2.KNOWN_SUBSTRATE_GAPS[:-1]
    ]
    with pytest.raises(step2.Step2ConformanceError, match="KSG row missing"):
        step2.assert_ksg_invariants(feats)


def test_known_no_data_gap_enum_zoned_to_ksg_only():
    """The literal `known_no_data_gap` is the internal terminal-status enum
    only for the four pinned KSG dates. Any non-KSG date carrying that enum
    must hard-fail the gate."""
    feats = []
    for d in step2.KNOWN_SUBSTRATE_GAPS:
        feats.append({
            "civil_date": d,
            "is_known_substrate_gap": True,
            "terminal_status": step2.TERMINAL_STATUS_KSG,
            "represented_only": False,
            "documented_exception_label": "",
        })
    feats.append({
        "civil_date": "2015-06-15",  # non-KSG, ordinary date
        "is_known_substrate_gap": False,
        "terminal_status": step2.TERMINAL_STATUS_KSG,  # smuggled
        "represented_only": False,
        "documented_exception_label": "",
    })
    with pytest.raises(step2.Step2ConformanceError, match="non-KSG row"):
        step2.assert_ksg_invariants(feats)


def test_doc_exception_date_never_ksg_via_assert():
    feats = [
        {
            "civil_date": d,
            "is_known_substrate_gap": True,
            "terminal_status": step2.TERMINAL_STATUS_KSG,
            "represented_only": False,
            "documented_exception_label": "",
        }
        for d in step2.KNOWN_SUBSTRATE_GAPS
    ]
    feats.append({
        "civil_date": step2.DOCUMENTED_EXCEPTION_DATE,
        "is_known_substrate_gap": True,  # smuggled: must hard-fail
        "terminal_status": step2.TERMINAL_STATUS_KSG,
        "represented_only": False,
        "documented_exception_label": "",
    })
    with pytest.raises(step2.Step2ConformanceError, match="must never be a KSG"):
        step2.assert_ksg_invariants(feats)


def test_doc_exception_date_never_ksg_via_derive():
    # If the upstream label is intact, the label wins and the row is
    # represented_only_documented_exception, never KSG.
    ts = step2.derive_terminal_status(
        step2.DOCUMENTED_EXCEPTION_DATE,
        step2.DOCUMENTED_EXCEPTION_LABEL,
        is_known_substrate_gap=False,
    )
    assert ts == step2.TERMINAL_STATUS_DOC_EXC
    # And if a corruption tries to mark it as KSG with no label, the
    # derivation hard-fails.
    with pytest.raises(step2.Step2ConformanceError, match="never be labeled"):
        step2.derive_terminal_status(
            step2.DOCUMENTED_EXCEPTION_DATE,
            "",  # label missing
            is_known_substrate_gap=True,
        )


def test_terminal_status_enum_values_are_locked():
    assert step2.TERMINAL_STATUS_RAW == "raw_t0_present"
    assert step2.TERMINAL_STATUS_DOC_EXC == "represented_only_documented_exception"
    assert step2.TERMINAL_STATUS_KSG == "known_no_data_gap"


# ----------------------------------------------------------------------------
# §6.6 / §7 rolling current-row-inclusive semantics
# ----------------------------------------------------------------------------

def test_rolling_current_row_inclusive_window_math():
    rows = _make_increasing_dataset(10)  # totals = 1..10
    feats = step2.derive_features(rows)
    # row index 6 is the seventh row; w=7 trailing window covers indices 0..6
    expected_mean_w7 = statistics.fmean([1, 2, 3, 4, 5, 6, 7])
    assert feats[6]["roll_mean_total_w7"] == pytest.approx(expected_mean_w7)
    expected_std_w7 = statistics.stdev([1, 2, 3, 4, 5, 6, 7])
    assert feats[6]["roll_std_total_w7"] == pytest.approx(expected_std_w7)
    # row index < 6 is warmup for w=7 → None
    assert feats[5]["roll_mean_total_w7"] is None
    assert feats[5]["roll_std_total_w7"] is None
    # current-row-inclusive: at row index 9, w=7 covers indices 3..9
    expected_mean_at_9 = statistics.fmean([4, 5, 6, 7, 8, 9, 10])
    assert feats[9]["roll_mean_total_w7"] == pytest.approx(expected_mean_at_9)


def test_rolling_does_not_look_ahead_into_future_rows():
    rows = _make_increasing_dataset(15)
    # Mutate row 10's total to a huge value; rows 0..9 must not see it via
    # any current-row-inclusive trailing window of length <= 10.
    rows[10]["rows_from_offset_0"] = 10_000_000
    rows[10]["total_row_count"] = 10_000_000
    feats = step2.derive_features(rows)
    # The huge value appears at row 10 only; rolling mean at row 9 over
    # window 7 (covering rows 3..9) must equal the pre-mutation expectation.
    assert feats[9]["roll_mean_total_w7"] == pytest.approx(
        statistics.fmean([4, 5, 6, 7, 8, 9, 10])
    )


def test_log1p_z_score_reference_distribution_is_log1p_not_raw():
    """`roll_z_log1p_total_wN` must use trailing rolling mean/std OF
    `log1p_total_row_count`, NOT of raw `total_row_count`.

    The fixture uses geometric (powers-of-5) totals so the log1p transform
    is approximately linear-spaced while the raw values are heavily
    right-skewed. The two z-scores for the same row must therefore differ
    materially; a constant-baseline-plus-spike fixture would produce
    coincidentally identical z's by symmetry (raw_z = log1p_z = 6/sqrt(7))
    and so cannot distinguish the implementation.
    """
    n = 7
    rows = []
    base = date.fromisoformat("2013-04-01")
    geometric_totals = (1, 5, 25, 125, 625, 3125, 15625)
    for i, total in enumerate(geometric_totals):
        offsets = {col: 0 for col in step2.OFFSET_COLUMNS}
        offsets["rows_from_offset_0"] = total
        rows.append(_make_input_row(
            (base + timedelta(days=i)).isoformat(), offsets=offsets,
        ))
    feats = step2.derive_features(rows)
    last = feats[-1]
    totals = [float(r["total_row_count"]) for r in rows]
    log1p_totals = [math.log1p(t) for t in totals]
    expected_log1p_mean_w7 = statistics.fmean(log1p_totals)
    expected_log1p_std_w7 = statistics.stdev(log1p_totals)
    expected_log1p_z_w7 = (
        log1p_totals[-1] - expected_log1p_mean_w7
    ) / expected_log1p_std_w7
    assert last["roll_mean_log1p_total_w7"] == pytest.approx(expected_log1p_mean_w7)
    assert last["roll_std_log1p_total_w7"] == pytest.approx(expected_log1p_std_w7)
    assert last["roll_z_log1p_total_w7"] == pytest.approx(expected_log1p_z_w7)
    # The raw-count mean/std are separate descriptives, computed on the raw
    # totals and emitted in their own columns:
    raw_mean = statistics.fmean(totals)
    raw_std = statistics.stdev(totals)
    raw_z_if_used = (totals[-1] - raw_mean) / raw_std
    assert last["roll_mean_total_w7"] == pytest.approx(raw_mean)
    assert last["roll_std_total_w7"] == pytest.approx(raw_std)
    # The log1p z and the raw z must NOT be equal — proves the denominator
    # used for the `roll_z_log1p_total_w7` column is the log1p reference,
    # not the raw-count one.
    assert abs(last["roll_z_log1p_total_w7"] - raw_z_if_used) > 0.1
    # Belt-and-suspenders: the raw-count rolling std/mean columns must NOT
    # accidentally equal the log1p ones.
    assert last["roll_mean_total_w7"] != pytest.approx(
        last["roll_mean_log1p_total_w7"]
    )
    assert last["roll_std_total_w7"] != pytest.approx(
        last["roll_std_log1p_total_w7"]
    )


def test_represented_only_and_ksg_rows_included_in_rolling():
    """§7: represented-only and KSG rows remain present AND their recorded
    `total_row_count` is included verbatim in rolling-window computations."""
    n = 7
    rows = _make_increasing_dataset(n - 1, start="2013-04-01")
    # Inject a "KSG-like" or "represented-only-like" row whose total is large.
    # The rolling mean over the full 7-row trailing window must include it.
    base = date.fromisoformat("2013-04-01")
    odd = _make_input_row(
        (base + timedelta(days=n - 1)).isoformat(),
        offsets={**{c: 0 for c in step2.OFFSET_COLUMNS},
                 "rows_from_offset_0": 1000},
        coverage_quality_flag="full",
    )
    rows.append(odd)
    feats = step2.derive_features(rows)
    totals = [float(r["total_row_count"]) for r in rows]
    assert feats[-1]["roll_mean_total_w7"] == pytest.approx(
        statistics.fmean(totals)
    )
    # Sanity: the odd row's large total dominates the trailing mean — proof it
    # was not masked or excluded.
    assert feats[-1]["roll_mean_total_w7"] > 100


# ----------------------------------------------------------------------------
# §6.8 broad warmup flag policy
# ----------------------------------------------------------------------------

def test_broad_warmup_iff_not_full_365d_history():
    n = 370
    rows = _make_increasing_dataset(n)
    feats = step2.derive_features(rows)
    # The first 364 rows lack a full 365-day window → warmup True
    for i in range(0, step2.WARMUP_WINDOW - 1):
        assert feats[i]["is_rolling_window_warmup"] is True
        assert feats[i]["has_full_365d_history"] is False
    # From row index 364 onward, the trailing 365-day window is full
    for i in range(step2.WARMUP_WINDOW - 1, n):
        assert feats[i]["is_rolling_window_warmup"] is False
        assert feats[i]["has_full_365d_history"] is True


def test_granular_history_flags_retained():
    rows = _make_increasing_dataset(40)
    feats = step2.derive_features(rows)
    assert feats[6]["has_full_7d_history"] is True
    assert feats[5]["has_full_7d_history"] is False
    assert feats[29]["has_full_30d_history"] is True
    assert feats[28]["has_full_30d_history"] is False


# ----------------------------------------------------------------------------
# §6.7 spike thresholds locked + NaN handling
# ----------------------------------------------------------------------------

def test_spike_thresholds_locked_constants():
    assert step2.SPIKE_THRESHOLD_LOW == 2.0
    assert step2.SPIKE_THRESHOLD_HIGH == 3.0


def test_spike_flags_false_when_z_is_nan_during_warmup():
    rows = _make_increasing_dataset(6)  # < 7 rows → w=7 z is None
    feats = step2.derive_features(rows)
    for f in feats:
        assert f["spike_w7_z_ge_2"] is False
        assert f["spike_w7_z_ge_3"] is False
        assert f["roll_z_log1p_total_w7"] is None


def test_spike_flags_false_when_rolling_std_is_zero():
    # 8 rows all with identical total = 100; w=7 std == 0 → z is None →
    # spike flags must be False (not NaN, not True).
    n = 8
    base = date.fromisoformat("2013-04-01")
    rows = []
    for i in range(n):
        offsets = {col: 0 for col in step2.OFFSET_COLUMNS}
        offsets["rows_from_offset_0"] = 100
        rows.append(_make_input_row(
            (base + timedelta(days=i)).isoformat(), offsets=offsets,
        ))
    feats = step2.derive_features(rows)
    for f in feats[6:]:  # rows with a full 7-day trailing window
        assert f["roll_std_log1p_total_w7"] == 0.0
        assert f["roll_z_log1p_total_w7"] is None
        assert f["spike_w7_z_ge_2"] is False
        assert f["spike_w7_z_ge_3"] is False


def test_spike_flags_correctly_fire_above_thresholds():
    # Build a 7-row baseline of 1s then a single huge spike. The log1p z
    # should exceed 2.0 at the spike day.
    n = 7
    rows = []
    base = date.fromisoformat("2013-04-01")
    for i in range(n - 1):
        offsets = {col: 0 for col in step2.OFFSET_COLUMNS}
        offsets["rows_from_offset_0"] = 1
        rows.append(_make_input_row(
            (base + timedelta(days=i)).isoformat(), offsets=offsets,
        ))
    offsets = {col: 0 for col in step2.OFFSET_COLUMNS}
    offsets["rows_from_offset_0"] = 999
    rows.append(_make_input_row(
        (base + timedelta(days=n - 1)).isoformat(), offsets=offsets,
    ))
    feats = step2.derive_features(rows)
    last = feats[-1]
    assert last["roll_z_log1p_total_w7"] > 2.0
    assert last["spike_w7_z_ge_2"] is True


# ----------------------------------------------------------------------------
# §7 offset_plus_1 retained as current-row component
# ----------------------------------------------------------------------------

def test_offset_plus_1_retained_as_current_row_component():
    """The seven offset columns — including rows_from_offset_plus_1 — are
    finalized components of the per-civil_date substrate row, not future rows
    in Step 2 civil-date ordering."""
    offsets = {col: 0 for col in step2.OFFSET_COLUMNS}
    offsets["rows_from_offset_0"] = 100
    offsets["rows_from_offset_plus_1"] = 25
    row = _make_input_row("2013-04-01", offsets=offsets)
    feats = step2.derive_features([row])
    assert feats[0]["rows_from_offset_plus_1"] == 25
    assert feats[0]["log1p_rows_from_offset_plus_1"] == pytest.approx(math.log1p(25))
    assert feats[0]["share_offset_plus_1"] == pytest.approx(25 / 125)
    # No look-ahead leakage either: this single row produces deterministic
    # output without referencing any future civil_date.
    assert feats[0]["civil_date"] == "2013-04-01"


# ----------------------------------------------------------------------------
# §11 conformance gate rejects market/outcome (extra) columns
# ----------------------------------------------------------------------------

def test_conformance_gate_rejects_unauthorized_extra_columns():
    rows = _make_increasing_dataset(40)
    feats = step2.derive_features(rows)
    # Smuggle in an unauthorized extra column (any column outside the locked
    # schema is rejected — this catches market-data / outcome smuggling).
    for r in feats:
        r["smuggled_extra_column"] = 0.0
    with pytest.raises(step2.Step2ConformanceError, match="schema mismatch"):
        step2.assert_feature_schema_exact(feats)


def test_conformance_gate_rejects_missing_locked_column():
    rows = _make_increasing_dataset(40)
    feats = step2.derive_features(rows)
    for r in feats:
        r.pop("spike_w7_z_ge_2", None)
    with pytest.raises(step2.Step2ConformanceError, match="schema mismatch"):
        step2.assert_feature_schema_exact(feats)


# ----------------------------------------------------------------------------
# §13 F1-F6 audit
# ----------------------------------------------------------------------------

def test_f1_f6_audit_catches_each_forbidden_literal():
    for lit in step2.FORBIDDEN_F1_F6_LITERALS:
        hits = step2.audit_f1_f6(
            f"Some prose that affirmatively asserts {lit} for the substrate."
        )
        assert lit in hits, f"failed to detect forbidden literal: {lit!r}"


def test_f1_f6_audit_clean_on_safe_text():
    assert step2.audit_f1_f6(
        "Substrate is 10/10 terminal-status (9 raw-complete + 1 labeled-"
        "complete documented-exception). No market data, no instrument."
    ) == []


def test_render_step2_summary_passes_f1_f6_audit():
    rows, metadata = _doc_exc_synthetic_pair()
    text = step2.render_step2_summary(rows, metadata, Path("/tmp/x"))
    assert step2.audit_f1_f6(text) == []
    # Sanity: the summary mentions 10/10 terminal-status, never raw-complete-10/10
    assert "raw-complete-10/10" not in text


def test_render_step2_metadata_passes_f1_f6_audit_and_boundaries():
    rows, metadata = _doc_exc_synthetic_pair()
    meta = step2.render_step2_metadata(rows, metadata, Path("/tmp/x"))
    text = json.dumps(meta, indent=2)
    assert step2.audit_f1_f6(text) == []
    for k in step2.BOUNDARY_DECLARATIONS_KEYS:
        assert meta["boundary_declarations"][k] is True
    assert meta["full_build_authorized_reused"] is False
    assert meta["merge_write_flag_reused"] is False
    assert meta["write_authorization_mechanism"] == "write_step2_output_cli_flag"


# ----------------------------------------------------------------------------
# CLI behavior
# ----------------------------------------------------------------------------

def test_cli_default_blocks_write_step2_output():
    """Invoking --write-step2-output must raise Step2BoundaryError; the flag
    is reserved for a separate future execution-authorization prompt."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    try:
        import importlib
        # Load the CLI module by spec from its file path, since scripts/ is
        # not a package.
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "run_lane2_gdelt1_step2_features", CLI_SCRIPT
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with pytest.raises(step2.Step2BoundaryError, match="blocked closed"):
            mod.main(["--write-step2-output", "--skip-input-pin-verification"])
    finally:
        sys.path.pop(0)


def test_cli_default_does_not_write_step2_output_dir(tmp_path):
    """A dry-run CLI invocation must not create the result-output directory."""
    expected_dir = (
        REPO_ROOT / "results" / "lane2_gdelt1_step2_daily_features"
    )
    existed_before = expected_dir.exists()
    cmd = [
        sys.executable,
        str(CLI_SCRIPT),
        "--report-json",
    ]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, cwd=REPO_ROOT, timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["verdict"] == "PASS — STEP 2 IMPLEMENTATION CONFORMS TO DESIGN MEMO"
    assert payload["feature_row_count"] == step2.EXPECTED_ROW_COUNT
    # No write side-effects allowed even when the gate PASSes
    assert expected_dir.exists() == existed_before
    if not existed_before:
        assert not expected_dir.exists()


def test_cli_help_documents_write_flag_as_reserved():
    cmd = [sys.executable, str(CLI_SCRIPT), "--help"]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert proc.returncode == 0
    assert "--write-step2-output" in proc.stdout
    # argparse may wrap the phrase "BLOCKED CLOSED" across lines in the help
    # output; normalize whitespace before checking so the assertion stays
    # resilient to terminal-width-driven wrapping.
    normalized_help = " ".join(proc.stdout.split())
    assert "BLOCKED CLOSED" in normalized_help


# ----------------------------------------------------------------------------
# End-to-end integration test against the real merged substrate
# ----------------------------------------------------------------------------

@pytest.mark.skipif(
    not (MERGED_DIR / "build_daily_counts.csv").is_file(),
    reason="canonical merged substrate not present in this checkout",
)
def test_conformance_gate_passes_on_real_merged_substrate():
    report = step2.run_conformance_gate(MERGED_DIR)
    assert report["verdict"] == "PASS — STEP 2 IMPLEMENTATION CONFORMS TO DESIGN MEMO"
    assert report["input_row_count"] == step2.EXPECTED_ROW_COUNT
    assert report["feature_row_count"] == step2.EXPECTED_ROW_COUNT
    assert report["summary_audit_hits"] == []
    assert report["metadata_audit_hits"] == []
    for k in step2.BOUNDARY_DECLARATIONS_KEYS:
        assert report["boundary_declarations"][k] is True


@pytest.mark.skipif(
    not (MERGED_DIR / "build_daily_counts.csv").is_file(),
    reason="canonical merged substrate not present in this checkout",
)
def test_real_doc_exception_row_carries_expected_propagation():
    rows, metadata = step2.load_inputs(MERGED_DIR)
    feats = step2.derive_features(rows)
    matches = [r for r in feats if r["civil_date"] == step2.DOCUMENTED_EXCEPTION_DATE]
    assert len(matches) == 1
    r = matches[0]
    assert r["represented_only"] is True
    assert r["documented_exception_label"] == step2.DOCUMENTED_EXCEPTION_LABEL
    assert r["total_row_count"] == step2.DOCUMENTED_EXCEPTION_TOTAL
    assert r["rows_from_offset_0"] == 0
    assert r["terminal_status"] == step2.TERMINAL_STATUS_DOC_EXC
    # 2022-11-10 must never be labeled KSG / known_no_data_gap
    assert r["is_known_substrate_gap"] is False
    assert r["terminal_status"] != step2.TERMINAL_STATUS_KSG
    # Neighbor cross-check 1267 = 91 + 849 + 327
    assert r["rows_from_offset_minus_1"] == 91
    assert r["rows_from_offset_minus_7"] == 849
    assert r["rows_from_offset_minus_30"] == 327


@pytest.mark.skipif(
    not (MERGED_DIR / "build_daily_counts.csv").is_file(),
    reason="canonical merged substrate not present in this checkout",
)
def test_real_ksg_rows_carry_internal_enum_only():
    rows, _ = step2.load_inputs(MERGED_DIR)
    feats = step2.derive_features(rows)
    by_date = {r["civil_date"]: r for r in feats}
    for d in step2.KNOWN_SUBSTRATE_GAPS:
        r = by_date[d]
        assert r["is_known_substrate_gap"] is True
        assert r["terminal_status"] == step2.TERMINAL_STATUS_KSG
        assert r["represented_only"] is False
        assert r["documented_exception_label"] == ""
    # And the document exception date is NOT KSG
    r2 = by_date[step2.DOCUMENTED_EXCEPTION_DATE]
    assert r2["is_known_substrate_gap"] is False
    assert r2["terminal_status"] != step2.TERMINAL_STATUS_KSG


@pytest.mark.skipif(
    not (MERGED_DIR / "build_daily_counts.csv").is_file(),
    reason="canonical merged substrate not present in this checkout",
)
def test_real_input_pins_verified():
    observed = step2.verify_input_pins(MERGED_DIR)
    assert (
        observed["build_daily_counts.csv"]
        == step2.INPUT_ARTIFACT_SHA256["build_daily_counts.csv"]
    )
    assert (
        observed["build_metadata.json"]
        == step2.INPUT_ARTIFACT_SHA256["build_metadata.json"]
    )
    assert (
        observed["build_summary.md"]
        == step2.INPUT_ARTIFACT_SHA256["build_summary.md"]
    )
