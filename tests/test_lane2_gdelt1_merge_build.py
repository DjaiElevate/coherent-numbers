"""Tests for the documented-exception-aware Lane 2 GDELT1 merge writer
(v0.2 merge-implementation design memo).

Synthetic fixtures / tmp_path only. NO real network, NO GDELT fetch, NO
BigQuery, NO market data, NO Step 2. NO production write under results/.
The structural digest/union guards in `merge_chunks` are validated against
the real committed recognized-list capture via REPO_ROOT (read-only).
"""

import importlib.util
import json
import os

import pytest


def _load_runner():
    path = os.path.join(
        os.path.dirname(__file__), "..", "scripts",
        "run_lane2_gdelt1_full_daily_count_build.py",
    )
    spec = importlib.util.spec_from_file_location("l2_merge_build", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

DOC_DATE = "2022-11-10"
DOC_FILE = "20221110.export.CSV.zip"
DOC_MD5 = "91e15516016f986e5b8a08712e1de95a"
DOC_SIZE = 6714105

REPRESENTATION_ARTIFACT = (
    "representations/lane2_gdelt1/"
    "chunk_2022_documented_exception_20221110/representation.json"
)
REPRESENTATION_SHA256 = (
    "91276597f4f3882d15133e32ec2d845badd244f7c89e706d06482a9d729c4ee3"
)
CONTRACT_PATH = "configs/lane2_gdelt1_documented_exceptions.json"
CONTRACT_SHA256 = (
    "afee1c0d1e0e1d73fbe1ef45161deba4d174a4903e4b90093d00ac00472dda97"
)

F1_F6_FORBIDDEN = (
    "raw 365/365",
    "ordinary completion",
    "no-data gap",
    "recovered day",
    "raw-processed day",
    "exact runner-output gate from BigQuery count 105041",
)


def _real_fetch_set(m):
    data, _, _ = m._load_recognized_list(REPO_ROOT)
    report = m.build_reconciliation_report(data["recognized_in_window_units"])
    return report["fetch_set"]


def _chunk_2022_ded():
    return {
        "documented_exception_label": (
            "UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY"
        ),
        "documented_exceptions": [{
            "date": DOC_DATE,
            "raw_filename": DOC_FILE,
            "label": (
                "UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY"
            ),
            "catalog_md5": DOC_MD5,
            "catalog_filesize_bytes": DOC_SIZE,
            "http_status": 404,
            "raw_object_parsed": False,
            "rows_recovered": False,
        }],
        "documented_unavailable_data_confirmed_days": 1,
        "expected_calendar_days": 365,
        "raw_processed_days": 364,
        "recovered_days": 0,
        "known_no_data_gap_days": 0,
        "terminal_status_days": 365,
        "terminal_status_complete": True,
        "no_data_gap": False,
        "recovered": False,
        "known_substrate_gap_amended": False,
    }


def _build_basic_chunk_dirs(m, tmp_path):
    """10 chunks with correct manifest digests; chunk_2022 raw-complete-shaped
    (no documented exception). Mirrors the existing-suite builder."""
    fs = _real_fetch_set(m)
    manifests = m.build_all_chunk_manifests(fs)
    chunk_dirs = {}
    for cid in m.CHUNK_IDS:
        cdir = tmp_path / "results" / "lane2_gdelt1_full_daily_count_build" / cid
        cdir.mkdir(parents=True, exist_ok=False)
        counts = {(iso, 0): 10 for iso in manifests[cid][:3]}
        m.write_chunk_contributions_csv(str(cdir), cid, counts)
        m.write_chunk_metadata_json(str(cdir), {
            "chunk_id": cid,
            "chunk_manifest_digest": m.chunk_manifest_digest(manifests[cid]),
            "expected_file_count": m.EXPECTED_CHUNK_COUNTS[cid],
            "actual_completed_file_count": m.EXPECTED_CHUNK_COUNTS[cid],
        })
        (cdir / "chunk_summary.md").write_text(
            "# synthetic summary {}\n".format(cid), encoding="utf-8"
        )
        chunk_dirs[cid] = str(cdir)
    return chunk_dirs


def _build_doc_aware_chunk_dirs(m, tmp_path):
    """Like _build_basic_chunk_dirs but chunk_2022 carries the documented
    exception (raw=364) and a represented-only 2022-11-10 neighbor-offset row."""
    fs = _real_fetch_set(m)
    manifests = m.build_all_chunk_manifests(fs)
    chunk_dirs = {}
    for cid in m.CHUNK_IDS:
        cdir = tmp_path / "results" / "lane2_gdelt1_full_daily_count_build" / cid
        cdir.mkdir(parents=True, exist_ok=False)
        counts = {(iso, 0): 10 for iso in manifests[cid][:3]}
        md = {
            "chunk_id": cid,
            "chunk_manifest_digest": m.chunk_manifest_digest(manifests[cid]),
            "expected_file_count": m.EXPECTED_CHUNK_COUNTS[cid],
            "actual_completed_file_count": m.EXPECTED_CHUNK_COUNTS[cid],
        }
        if cid == "chunk_2022":
            # represented-only: 2022-11-10 has neighbor (-1) contribution, no t0.
            counts[(DOC_DATE, -1)] = 5
            md["actual_completed_file_count"] = 364
            md["documented_exception_diagnostic"] = _chunk_2022_ded()
        m.write_chunk_contributions_csv(str(cdir), cid, counts)
        m.write_chunk_metadata_json(str(cdir), md)
        (cdir / "chunk_summary.md").write_text(
            "# synthetic summary {}\n".format(cid), encoding="utf-8"
        )
        chunk_dirs[cid] = str(cdir)
    return chunk_dirs


def _row(m, civil_date, **offsets):
    cols = {c: 0 for c in m._MERGE_OFFSET_COLUMNS}
    cols.update(offsets)
    total = sum(cols[c] for c in m._MERGE_OFFSET_COLUMNS)
    row = {
        "civil_date": civil_date,
        "total_row_count": total,
        "t0_file_status": "present",
        "expected_contributing_files_count": 7,
        "available_contributing_files_count": 7,
        "coverage_quality_flag": "full",
        "coverage_completeness": 1.0,
        "represented_only": False,
        "documented_exception_label": "",
    }
    row.update(cols)
    return row


def _synthetic_result(m):
    per_chunk = []
    for cid in m.CHUNK_IDS:
        if cid == "chunk_2022":
            rec = {
                "status_class": "labeled_complete_documented_exception",
                "expected_calendar_days": 365, "raw_processed_days": 364,
                "documented_unavailable_data_confirmed_days": 1,
                "recovered_days": 0, "known_no_data_gap_days": 0,
                "terminal_status_days": 365, "terminal_status_complete": True,
            }
        elif cid == "chunk_2014":
            rec = {
                "status_class": "raw_complete",
                "expected_calendar_days": 365, "raw_processed_days": 361,
                "documented_unavailable_data_confirmed_days": 0,
                "recovered_days": 0, "known_no_data_gap_days": 4,
                "terminal_status_days": 365, "terminal_status_complete": True,
            }
        else:
            term = m.PINNED_TERMINAL_STATUS_DAYS[cid]
            rec = {
                "status_class": "raw_complete",
                "expected_calendar_days": term, "raw_processed_days": term,
                "documented_unavailable_data_confirmed_days": 0,
                "recovered_days": 0, "known_no_data_gap_days": 0,
                "terminal_status_days": term, "terminal_status_complete": True,
            }
        rec.update({
            "chunk_id": cid, "canonical_output_dir": "results/.../" + cid,
            "chunk_metadata_sha256": "0" * 64,
            "chunk_summary_sha256": "1" * 64,
            "chunk_contributions_sha256": "2" * 64,
            "chunk_manifest_digest": cid + "_digest",
        })
        per_chunk.append(rec)
    aggregate = {
        "raw_processed_days": 3557,
        "documented_unavailable_data_confirmed_days": 1,
        "recovered_days": 0, "known_no_data_gap_days": 4,
        "terminal_status_days": 3562,
        "total_in_window_rows": 100, "civil_days_in_output_domain": 3562,
        "chunks_merged": list(m.CHUNK_IDS),
    }
    documented_exceptions = [{
        "chunk_id": "chunk_2022", "date": DOC_DATE, "raw_filename": DOC_FILE,
        "label": m.DOCUMENTED_EXCEPTION_LABEL, "catalog_md5": DOC_MD5,
        "catalog_filesize_bytes": DOC_SIZE, "http_status": 404,
        "raw_object_parsed": False, "rows_recovered": False,
        "no_data_gap": False, "recovered": False,
        "known_substrate_gap_amended": False,
        "representation_artifact": REPRESENTATION_ARTIFACT,
        "representation_artifact_sha256": REPRESENTATION_SHA256,
        "contract": CONTRACT_PATH,
        "contract_sha256": CONTRACT_SHA256,
        "source_chunk_output_dir": "chunk_2022",
        "source_chunk_metadata_sha256": "0" * 64,
    }]
    rows = [
        _row(m, "2015-06-01", rows_from_offset_0=10),
        _row(m, DOC_DATE, rows_from_offset_minus_1=5),
    ]
    rows[1]["represented_only"] = True
    rows[1]["documented_exception_label"] = m.DOCUMENTED_EXCEPTION_LABEL
    return {
        "daily_count_rows": rows,
        "per_chunk": per_chunk,
        "aggregate": aggregate,
        "documented_exceptions": documented_exceptions,
        "retained_halt_history": [dict(h) for h in m.RETAINED_HALT_HISTORY],
        "input_chunk_manifest_digests": [
            r["chunk_manifest_digest"] for r in per_chunk
        ],
        "merge_implementation_version": m.MERGE_IMPLEMENTATION_VERSION,
    }


# ── 1. existing structural merge still works ─────────────────────────────────

def test_existing_merge_chunks_still_succeeds(tmp_path):
    m = _load_runner()
    chunk_dirs = _build_basic_chunk_dirs(m, tmp_path)
    result = m.merge_chunks(chunk_dirs, REPO_ROOT)
    assert len(result["daily_count_rows"]) == 3562


# ── 2. --merge without --write-merge-output performs no write ────────────────

def test_cli_merge_without_write_flag_writes_nothing(tmp_path, capsys):
    m = _load_runner()
    chunk_dirs = _build_basic_chunk_dirs(m, tmp_path)
    argv = ["--merge", "--repo-root", REPO_ROOT]
    for cid, d in chunk_dirs.items():
        argv += ["--merge-input", "{}={}".format(cid, d)]
    rc = m.main(argv)
    out = capsys.readouterr().out
    assert rc == 0
    assert "in-memory only" in out
    # No merge output dir created anywhere under the temp tree.
    assert not list(tmp_path.glob("**/merged_*"))


# ── 3-4. writer file set, determinism, non-circular digest ───────────────────

def test_writer_writes_exactly_three_files(tmp_path):
    m = _load_runner()
    out = tmp_path / "merged_test"
    written = m.write_merge_artifacts(_synthetic_result(m), str(out))
    names = sorted(os.listdir(out))
    assert names == [
        "build_daily_counts.csv", "build_metadata.json", "build_summary.md",
    ]
    assert written["build_manifest_digest"]


def test_writer_deterministic_and_digest_non_circular(tmp_path):
    m = _load_runner()
    res = _synthetic_result(m)
    a = m.write_merge_artifacts(res, str(tmp_path / "a"))
    b = m.write_merge_artifacts(res, str(tmp_path / "b"))
    # Deterministic across runs.
    assert a["build_daily_counts_sha256"] == b["build_daily_counts_sha256"]
    assert a["build_summary_sha256"] == b["build_summary_sha256"]
    assert a["build_metadata_sha256"] == b["build_metadata_sha256"]
    assert a["build_manifest_digest"] == b["build_manifest_digest"]
    # build_manifest_digest stored in metadata, but metadata's own sha is NOT
    # an input to it (non-circular).
    meta = json.loads((tmp_path / "a" / "build_metadata.json").read_text())
    assert meta["build_manifest_digest"] == a["build_manifest_digest"]
    assert "build_metadata.json" not in meta["output_artifact_sha256s"]
    assert set(meta["output_artifact_sha256s"]) == {
        "build_daily_counts.csv", "build_summary.md",
    }
    # Recompute the digest from its declared non-circular inputs.
    import hashlib
    h = hashlib.sha256()
    for d in meta["input_chunk_manifest_digests"]:
        h.update(str(d).encode("ascii")); h.update(b"\n")
    h.update(meta["output_artifact_sha256s"]["build_daily_counts.csv"]
             .encode("ascii")); h.update(b"\n")
    h.update(meta["output_artifact_sha256s"]["build_summary.md"]
             .encode("ascii")); h.update(b"\n")
    assert h.hexdigest() == meta["build_manifest_digest"]


# ── 5-7. row rules: total sum; represented_only is label-derived ─────────────

def test_total_row_count_must_equal_seven_offset_sum(tmp_path):
    m = _load_runner()
    bad = _row(m, "2015-06-01", rows_from_offset_0=10)
    bad["total_row_count"] = 999  # corrupt
    with pytest.raises(m.ChunkManifestError, match="seven-offset"):
        m._enrich_merge_row(bad, set())


def test_documented_date_is_represented_only_with_zero_t0(tmp_path):
    m = _load_runner()
    row = _row(m, DOC_DATE, rows_from_offset_minus_1=5)
    assert row["rows_from_offset_0"] == 0
    out = m._enrich_merge_row(row, {DOC_DATE})
    assert out["represented_only"] is True
    assert out["documented_exception_label"] == m.DOCUMENTED_EXCEPTION_LABEL
    assert out["total_row_count"] == 5


def test_ksg_date_is_not_represented_only_even_with_neighbors(tmp_path):
    m = _load_runner()
    # A 2014 KSG date, with neighbor contributions, but NOT a documented date.
    row = _row(m, "2014-01-23", rows_from_offset_minus_1=3, rows_from_offset_plus_1=2)
    out = m._enrich_merge_row(row, {DOC_DATE})
    assert out["represented_only"] is False
    assert out["documented_exception_label"] == ""


# ── 8-11. documented-exception validation / fail-closed ──────────────────────

def _canonical_chunk_2022_record():
    return {
        "chunk_id": "chunk_2022",
        "canonical_output_dir":
            "results/lane2_gdelt1_full_daily_count_build/"
            "chunk_2022_20260528T234738Z",
        "chunk_metadata_sha256":
            "e986e217d1906aa3e7fbe3bf412add975738bf10fba8334b704440b9d3184de1",
    }


def test_documented_exception_metadata_carried_exactly():
    m = _load_runner()
    contract = m.load_documented_exceptions(REPO_ROOT)
    assert ("chunk_2022", DOC_DATE) in contract
    provenance = m.documented_exception_provenance(
        REPO_ROOT, contract[("chunk_2022", DOC_DATE)]["representation_artifact"]
    )
    md2022 = {"documented_exception_diagnostic": _chunk_2022_ded()}
    record = _canonical_chunk_2022_record()
    entries = m._build_documented_entries(contract, md2022, provenance, record)
    assert len(entries) == 1
    e = entries[0]
    assert e["date"] == DOC_DATE
    assert e["raw_filename"] == DOC_FILE
    assert e["label"] == m.DOCUMENTED_EXCEPTION_LABEL
    assert e["catalog_md5"] == DOC_MD5
    assert e["catalog_filesize_bytes"] == DOC_SIZE
    assert e["http_status"] == 404
    assert e["raw_object_parsed"] is False
    assert e["rows_recovered"] is False
    assert e["no_data_gap"] is False
    assert e["recovered"] is False
    assert e["known_substrate_gap_amended"] is False
    # §8 provenance fields (computed-and-validated; consistent-by-construction).
    assert e["representation_artifact"] == REPRESENTATION_ARTIFACT
    assert e["representation_artifact_sha256"] == REPRESENTATION_SHA256
    assert e["contract"] == CONTRACT_PATH
    assert e["contract_sha256"] == CONTRACT_SHA256
    assert e["source_chunk_output_dir"] == "chunk_2022_20260528T234738Z"
    assert e["source_chunk_metadata_sha256"] == record["chunk_metadata_sha256"]
    assert e["source_chunk_metadata_sha256"] == (
        "e986e217d1906aa3e7fbe3bf412add975738bf10fba8334b704440b9d3184de1"
    )


def test_contract_mismatch_hard_stops():
    m = _load_runner()
    contract = m.load_documented_exceptions(REPO_ROOT)
    provenance = m.documented_exception_provenance(REPO_ROOT, REPRESENTATION_ARTIFACT)
    ded = _chunk_2022_ded()
    ded["documented_exceptions"][0]["catalog_md5"] = "f" * 32  # wrong md5
    with pytest.raises(m.ChunkManifestError, match="disagree with the contract"):
        m._build_documented_entries(
            contract, {"documented_exception_diagnostic": ded},
            provenance, _canonical_chunk_2022_record(),
        )


def test_documented_exception_provenance_fails_closed_on_bad_representation():
    m = _load_runner()
    # A path whose file content does not match the pinned representation SHA.
    with pytest.raises(m.ChunkManifestError, match="representation SHA-256"):
        m.documented_exception_provenance(REPO_ROOT, CONTRACT_PATH)


def test_undocumented_documented_exception_hard_stops():
    m = _load_runner()
    md2022 = {"documented_exception_diagnostic": _chunk_2022_ded()}
    # Empty contract => the chunk's documented exception is undocumented.
    with pytest.raises(m.ChunkManifestError, match="undocumented"):
        m._chunk_category_counts("chunk_2022", md2022, {})


def test_documented_label_on_2013_2021_chunk_hard_stops():
    m = _load_runner()
    contract = m.load_documented_exceptions(REPO_ROOT)
    # chunk_2015 carrying a documented exception is not in the contract.
    md = {"documented_exception_diagnostic": _chunk_2022_ded()}
    with pytest.raises(m.ChunkManifestError, match="undocumented"):
        m._chunk_category_counts("chunk_2015", md, contract)


# ── 12-15. structural guards still hard-stop ─────────────────────────────────

def test_missing_chunk_hard_stops(tmp_path):
    m = _load_runner()
    chunk_dirs = _build_doc_aware_chunk_dirs(m, tmp_path)
    del chunk_dirs["chunk_2017"]
    with pytest.raises(m.ChunkManifestError, match="missing"):
        m.merge_chunks_with_documented_exceptions(chunk_dirs, REPO_ROOT)


def test_unexpected_chunk_id_hard_stops(tmp_path):
    m = _load_runner()
    chunk_dirs = _build_doc_aware_chunk_dirs(m, tmp_path)
    chunk_dirs["chunk_2099_fake"] = chunk_dirs["chunk_2017"]
    with pytest.raises(m.ChunkManifestError):
        m.merge_chunks_with_documented_exceptions(chunk_dirs, REPO_ROOT)


def test_halted_only_dir_rejected_as_chunk_input(tmp_path):
    m = _load_runner()
    halted = tmp_path / "halted"
    halted.mkdir()
    (halted / "halt_diagnostic.json").write_text("{}", encoding="utf-8")
    with pytest.raises(m.ChunkManifestError, match="missing"):
        m.load_chunk_metadata(str(halted))


def test_manifest_digest_mismatch_hard_stops(tmp_path):
    m = _load_runner()
    chunk_dirs = _build_doc_aware_chunk_dirs(m, tmp_path)
    cdir = chunk_dirs["chunk_2018"]
    md = m.load_chunk_metadata(cdir)
    md["chunk_manifest_digest"] = "0" * 64
    m.write_chunk_metadata_json(cdir, md)
    with pytest.raises(m.ChunkManifestError, match="digest mismatch"):
        m.merge_chunks_with_documented_exceptions(chunk_dirs, REPO_ROOT)


# ── 16-17. category-count coherence (pinned 3562) ────────────────────────────

def _per_chunk_counts(m, contract):
    out = []
    for cid in m.CHUNK_IDS:
        if cid == "chunk_2022":
            md = {"documented_exception_diagnostic": _chunk_2022_ded()}
        elif cid == "chunk_2014":
            md = {"actual_completed_file_count": 361}
        else:
            md = {"actual_completed_file_count": m.EXPECTED_CHUNK_COUNTS[cid]}
        rec = m._chunk_category_counts(cid, md, contract)
        rec["chunk_id"] = cid
        out.append(rec)
    return out


def test_pinned_aggregate_3562_partition_passes():
    m = _load_runner()
    contract = m.load_documented_exceptions(REPO_ROOT)
    per_chunk = _per_chunk_counts(m, contract)
    agg = m._assert_merge_aggregate(per_chunk)
    assert agg["terminal_status_days"] == 3562
    assert agg["raw_processed_days"] == 3557
    assert agg["documented_unavailable_data_confirmed_days"] == 1
    assert agg["recovered_days"] == 0
    assert agg["known_no_data_gap_days"] == 4
    # Leap years pinned at 366.
    assert m.PINNED_TERMINAL_STATUS_DAYS["chunk_2016"] == 366
    assert m.PINNED_TERMINAL_STATUS_DAYS["chunk_2020"] == 366


def test_pinned_per_chunk_deviation_hard_stops():
    m = _load_runner()
    contract = m.load_documented_exceptions(REPO_ROOT)
    # chunk_2016 with 365 (should be 366) deviates from the pinned count.
    with pytest.raises(m.ChunkManifestError, match="pinned"):
        m._chunk_category_counts(
            "chunk_2016", {"actual_completed_file_count": 365}, contract
        )


def test_aggregate_deviation_hard_stops_when_doc_missing():
    m = _load_runner()
    contract = m.load_documented_exceptions(REPO_ROOT)
    per_chunk = _per_chunk_counts(m, contract)
    # Make chunk_2022 raw-complete-shaped (no documented exception): agg breaks.
    for r in per_chunk:
        if r["chunk_id"] == "chunk_2022":
            r["raw_processed_days"] = 365
            r["documented_unavailable_data_confirmed_days"] = 0
            r["terminal_status_days"] = 365
    with pytest.raises(m.ChunkManifestError):
        m._assert_merge_aggregate(per_chunk)


# ── 18. F1-F6 audit on generated summary ─────────────────────────────────────

def test_build_summary_has_no_forbidden_f1_f6_literals():
    m = _load_runner()
    summary = m.render_merge_build_summary(_synthetic_result(m))
    for lit in F1_F6_FORBIDDEN:
        assert lit not in summary, "forbidden literal in summary: {!r}".format(lit)
    assert "10/10 terminal-status" in summary


# ── 19-20. boundary firewalls / guard untouched ──────────────────────────────

def test_metadata_boundary_declarations_all_true(tmp_path):
    m = _load_runner()
    m.write_merge_artifacts(_synthetic_result(m), str(tmp_path / "o"))
    meta = json.loads((tmp_path / "o" / "build_metadata.json").read_text())
    bd = meta["boundary_declarations"]
    for k in (
        "no_step_2", "no_market_data", "no_gdelt_fetch", "no_bigquery",
        "no_row_export", "no_known_substrate_gaps_amendment",
    ):
        assert bd[k] is True
    assert meta["merge_authorization"]["full_build_authorized_reused"] is False


def test_full_build_authorized_remains_false():
    m = _load_runner()
    assert m.FULL_BUILD_AUTHORIZED is False


# ── 21. end-to-end documented-exception-aware merge + writer ─────────────────

def test_doc_aware_merge_end_to_end_and_order_independent(tmp_path):
    m = _load_runner()
    dirs = _build_doc_aware_chunk_dirs(m, tmp_path)
    result = m.merge_chunks_with_documented_exceptions(dirs, REPO_ROOT)

    assert len(result["per_chunk"]) == 10
    assert result["aggregate"]["terminal_status_days"] == 3562
    assert result["aggregate"]["raw_processed_days"] == 3557
    assert result["aggregate"]["documented_unavailable_data_confirmed_days"] == 1
    assert result["aggregate"]["known_no_data_gap_days"] == 4
    assert len(result["documented_exceptions"]) == 1
    de = result["documented_exceptions"][0]
    assert de["date"] == DOC_DATE
    # §8 provenance: computed-and-validated contract/representation SHAs +
    # source-chunk fields consistent-by-construction with per_chunk.
    assert de["representation_artifact"] == REPRESENTATION_ARTIFACT
    assert de["representation_artifact_sha256"] == REPRESENTATION_SHA256
    assert de["contract"] == CONTRACT_PATH
    assert de["contract_sha256"] == CONTRACT_SHA256
    c2022 = next(r for r in result["per_chunk"] if r["chunk_id"] == "chunk_2022")
    assert de["source_chunk_output_dir"] == os.path.basename(
        c2022["canonical_output_dir"]
    )
    assert de["source_chunk_output_dir"] == "chunk_2022"
    assert de["source_chunk_metadata_sha256"] == c2022["chunk_metadata_sha256"]

    rows = {r["civil_date"]: r for r in result["daily_count_rows"]}
    doc_row = rows[DOC_DATE]
    assert doc_row["rows_from_offset_0"] == 0
    assert doc_row["rows_from_offset_minus_1"] == 5
    assert doc_row["total_row_count"] == 5
    assert doc_row["represented_only"] is True
    assert doc_row["documented_exception_label"] == m.DOCUMENTED_EXCEPTION_LABEL

    written = m.write_merge_artifacts(result, str(tmp_path / "merged_out"))
    assert sorted(os.listdir(tmp_path / "merged_out")) == [
        "build_daily_counts.csv", "build_metadata.json", "build_summary.md",
    ]

    # Order-independence of build_manifest_digest.
    reversed_dirs = dict(reversed(list(dirs.items())))
    result2 = m.merge_chunks_with_documented_exceptions(reversed_dirs, REPO_ROOT)
    written2 = m.write_merge_artifacts(result2, str(tmp_path / "merged_out2"))
    assert written["build_manifest_digest"] == written2["build_manifest_digest"]
    assert written["build_daily_counts_sha256"] == written2["build_daily_counts_sha256"]
