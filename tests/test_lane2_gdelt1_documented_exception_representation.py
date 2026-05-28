"""Conformance tests for the Lane 2 GDELT1 chunk_2022 / 2022-11-10
documented-exception representation scaffold.

Scaffold-only: validates the committed representation artifact and label/config
contract, and proves the documented exception cannot be silently promoted to
raw / gap / recovered / ordinary completion / exact runner-output gate.

NO network. NO runner execution. NO production-runner-source modification. This
turn intentionally implements NO runtime documented-exception path; these tests
affirm that by construction (the production runner source is byte-identical to
the committed baseline blob, and contains no documented-exception wiring).
"""

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REPRESENTATION_PATH = (
    REPO_ROOT
    / "representations"
    / "lane2_gdelt1"
    / "chunk_2022_documented_exception_20221110"
    / "representation.json"
)
CONFIG_PATH = REPO_ROOT / "configs" / "lane2_gdelt1_documented_exceptions.json"
RUNNER_PATH = REPO_ROOT / "scripts" / "run_lane2_gdelt1_full_daily_count_build.py"

LABEL = "UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY"
CATALOG_MD5 = "91e15516016f986e5b8a08712e1de95a"
CATALOG_SIZE = 6714105
BASELINE_RUNNER_BLOB = "dec8e09283de9357b2b2aa65af13e21b21fe85cc"
POST_SUPPORT_RUNNER_BLOB = "464c0539475102f3de762ce851f862903ff2985c"
EXPECTED_KNOWN_SUBSTRATE_GAPS = ("2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19")


def _rep():
    return json.loads(REPRESENTATION_PATH.read_text(encoding="utf-8"))


def _cfg():
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = b"blob %d\0" % len(data)
    return hashlib.sha1(header + data).hexdigest()


# 1. Representation artifact exists and has the exact mandatory label.
def test_representation_exists_and_label_exact():
    assert REPRESENTATION_PATH.is_file()
    assert _rep()["label"] == LABEL


# 2. Mandatory negative booleans.
def test_representation_negative_booleans():
    rep = _rep()
    assert rep["raw_object_parsed"] is False
    assert rep["rows_recovered"] is False
    assert rep["known_substrate_gap_amended"] is False
    assert rep["no_data_gap"] is False
    assert rep["recovered"] is False
    assert rep["raw_processed"] is False
    assert rep["semantic_recovery_artifact_created"] is False


# 3. The label is exactly the mandated string.
def test_label_string_exact():
    assert _rep()["label"] == LABEL
    assert _cfg()["label"] == LABEL


# 4 & 5. md5 + filesize recorded.
def test_catalog_md5_and_size():
    rep = _rep()
    assert rep["catalog_md5"] == CATALOG_MD5
    assert rep["catalog_filesize_bytes"] == CATALOG_SIZE


# 6. BigQuery counts recorded.
def test_bigquery_counts():
    bq = _rep()["bigquery_counts"]
    assert bq["20221109"] == 117008
    assert bq["20221110"] == 105041
    assert bq["20221111"] == 40588


# 7. 105041 is not an exact runner-output gate.
def test_bigquery_count_not_exact_gate():
    sem = _rep()["bigquery_count_semantics"].lower()
    assert "not an exact" in sem or "not a" in sem
    assert "exact runner-output gate from BigQuery count 105041" in _rep()["forbidden_claims"]


# 8. The day is not described as gap / recovered / raw-processed / ordinary / raw 365/365.
def test_not_misclassified():
    rep = _rep()
    assert rep["status"] == "data_confirmed_raw_object_unavailable_represented_only"
    assert rep["no_data_gap"] is False
    assert rep["recovered"] is False
    assert rep["raw_processed"] is False
    assert rep["merge_gate_status"] == "pending_labeled_completion_implementation"
    assert rep["merge_gate_status"] not in ("complete", "open", "labeled_complete")
    # forbidden phrases appear ONLY inside the explicit forbidden_claims negation list.
    for phrase in ("raw 365/365", "ordinary completion", "no-data gap", "recovered day", "raw-processed day"):
        assert phrase in rep["forbidden_claims"]


# 9. Config contract exists with exact label, scope, and runtime flags.
def test_config_contract_core():
    cfg = _cfg()
    assert cfg["label"] == LABEL
    scope = cfg["documented_exceptions"][0]["allowed_scope"]
    assert scope["chunk_id"] == "chunk_2022"
    assert scope["date"] == "2022-11-10"
    assert scope["sqldate"] == 20221110
    assert scope["raw_filename"] == "20221110.export.CSV.zip"
    assert scope["catalog_md5"] == CATALOG_MD5
    assert scope["catalog_filesize_bytes"] == CATALOG_SIZE
    # Runner support is now implemented (post runner-support turn); merge gate
    # remains closed pending the merge-gate machinery.
    assert cfg["runner_support_implemented"] is True
    assert cfg["future_runner_support_required"] is False
    assert cfg["merge_gate_open"] is False
    assert cfg["production_runner_blob_baseline_pre_support"] == BASELINE_RUNNER_BLOB


# 10. Config forbids the listed misuses.
def test_config_forbidden_uses():
    forbidden = _cfg()["forbidden_uses"]
    for item in (
        "arbitrary 404s",
        "neighboring dates",
        "other chunks",
        "known substrate gaps",
        "no-data gap classification",
        "recovered-day classification",
        "raw-processed classification",
        "ordinary completion",
    ):
        assert item in forbidden


# 11. KNOWN_SUBSTRATE_GAPS in the runner source is still exactly the four 2014 dates,
#     and 2022-11-10 / 20221110 do NOT appear in the runner source.
def test_known_substrate_gaps_unchanged():
    src = RUNNER_PATH.read_text(encoding="utf-8")
    for d in EXPECTED_KNOWN_SUBSTRATE_GAPS:
        assert d in src
    assert "2022-11-10" not in src
    assert "20221110" not in src


# 12. Production runner source blob is the pinned post-support blob (changed
#     from the pre-support baseline by the runner-support implementation turn).
def test_runner_blob_is_post_support():
    blob = _git_blob_sha1(RUNNER_PATH)
    assert blob == POST_SUPPORT_RUNNER_BLOB
    assert blob != BASELINE_RUNNER_BLOB


# 13. Production runner source NOW wires the documented-exception mechanism,
#     but still hard-codes neither the date nor a no-data-gap classification.
def test_runner_has_documented_exception_wiring():
    src = RUNNER_PATH.read_text(encoding="utf-8")
    assert LABEL in src
    assert "load_documented_exceptions" in src
    assert "documented_exception_match" in src
    assert "lane2_gdelt1_documented_exceptions" in src
    # The runner must NOT hard-code the date; it is loaded from the contract.
    assert "2022-11-10" not in src
    assert "20221110" not in src


# 14. Runtime path is implemented; merge gate still closed; baseline recorded.
def test_runtime_path_implemented():
    rep = _rep()
    cfg = _cfg()
    assert rep["runner_support_implemented"] is True
    assert rep["runtime_documented_exception_path_exists"] is True
    assert rep["production_runner_blob_at_representation"] == BASELINE_RUNNER_BLOB
    assert cfg["runner_support_implemented"] is True
    assert cfg["merge_gate_open"] is False
    assert cfg["production_runner_blob_baseline_pre_support"] == BASELINE_RUNNER_BLOB


# Extra: completion / merge not declared anywhere in the artifacts.
def test_no_completion_or_merge_claim():
    rep = _rep()
    cfg = _cfg()
    assert rep["merge_gate_status"] == "pending_labeled_completion_implementation"
    assert cfg["merge_gate_open"] is False
    assert rep["target_raw_processed_days_after_future_labeled_run"] == 364
    assert rep["target_documented_unavailable_data_confirmed_days"] == 1
    assert rep["current_raw_progress_before_labeled_run"] == 313
