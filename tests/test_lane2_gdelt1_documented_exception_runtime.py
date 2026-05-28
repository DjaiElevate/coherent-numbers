"""Runtime conformance tests for the chunk_2022 documented-exception path.

Synthetic fixtures + fake openers only. NO real network, NO real GDELT data,
NO production runner execution against live endpoints. Proves the carve-out
from FetchFailure-halt is narrow: it applies ONLY to the exact committed
quintuple (chunk_2022 + 2022-11-10 + 20221110.export.CSV.zip + label + md5/size)
and ONLY on a genuine 404. Every other 404 (other date, other chunk, wrong
filename), every non-404 failure, and missing contract/representation still halt.
"""

import importlib.util
import io
import json
import os
import re
import shutil
import urllib.error
import zipfile
from datetime import date, timedelta

import pytest

# Forbidden-phrasing tokens F1..F6 (provenance: merge-gate representation design
# memo, scaffold commit 5f43a13 / memo commit 50dda46). These are audited ONLY
# against runtime-emitted summary OUTPUT — never against test scaffolding — so
# this test file may itself contain the literals without self-failing.
FORBIDDEN_PATTERNS = {
    "F1": r"365/365",
    "F2": r"raw 365/365",
    "F3": r"ordinary",
    "F4": r"no caveat",
    "F5": r"gap[ -]day",
    "F6": r"no[ -]data[ -]day",
}


def _forbidden_counts(text):
    return {
        k: len(re.findall(p, text, flags=re.IGNORECASE))
        for k, p in FORBIDDEN_PATTERNS.items()
    }

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
DOC_DATE = "2022-11-10"
DOC_URL_SUFFIX = "/20221110.export.CSV.zip"
LABEL = "UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY"
CONFIG_REL = "configs/lane2_gdelt1_documented_exceptions.json"
REP_REL = (
    "representations/lane2_gdelt1/chunk_2022_documented_exception_20221110/"
    "representation.json"
)


def _load_runner():
    path = os.path.join(
        os.path.dirname(__file__), "..", "scripts",
        "run_lane2_gdelt1_full_daily_count_build.py",
    )
    spec = importlib.util.spec_from_file_location("l2_docexc", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _make_payload_zip(nominal_date):
    yyyymmdd = nominal_date.strftime("%Y%m%d")
    tsv = "1\t{}\tA".format(yyyymmdd)  # one in-window (offset 0) row
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("{}.export.CSV".format(yyyymmdd), tsv)
    return buf.getvalue()


class _FakeResponse:
    def __init__(self, status=200, body=b""):
        self._status, self._body = status, body

    def getcode(self):
        return self._status

    def read(self):
        return self._body

    def close(self):
        pass


def _year_isos(year, n=365):
    start = date(year, 1, 1)
    return [(start + timedelta(days=i)).isoformat() for i in range(n)]


def _all_2022_isos():
    return _year_isos(2022)


def _write_capture(tmp_path, isos):
    rel = (
        "results/lane2_gdelt1_turn_b_recognized_list_capture/"
        "20260521T124853Z/recognized_list.json"
    )
    full = tmp_path / rel
    full.parent.mkdir(parents=True, exist_ok=True)
    cap = {
        "recognized_in_window_units": list(isos),
        "recognized_in_window_count": len(isos),
        "schema_version": "v0.1",
    }
    full.write_text(json.dumps(cap), encoding="utf-8")
    return str(full)


def _copy_committed(tmp_path, config=True, rep=True):
    if config:
        dst = tmp_path / CONFIG_REL
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(os.path.join(REPO_ROOT, CONFIG_REL), dst)
    if rep:
        dst = tmp_path / REP_REL
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(os.path.join(REPO_ROOT, REP_REL), dst)


def _setup(m, monkeypatch, tmp_path, config=True, rep=True, isos=None):
    cap_path = _write_capture(tmp_path, isos if isos is not None else _all_2022_isos())
    actual_sha = m._hash_file_sha256(cap_path)
    monkeypatch.setattr(m, "RECOGNIZED_LIST_SHA256", actual_sha)
    monkeypatch.setattr(m, "assert_reconciliation_consistent", lambda r: None)
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_FULL_BUILD_AUTHORIZED", "1")
    _copy_committed(tmp_path, config=config, rep=rep)


def _opener_factory(m, fail_iso=None, fail_code=404, fail_reason="Not Found"):
    fail_url = m.date_to_daily_url(date.fromisoformat(fail_iso)) if fail_iso else None

    def opener(url, timeout=60.0):
        if fail_url is not None and url == fail_url:
            raise urllib.error.HTTPError(url, fail_code, fail_reason, {}, None)
        # derive nominal date from URL filename YYYYMMDD.export.CSV.zip
        fname = url.rsplit("/", 1)[-1]
        ymd = fname.split(".", 1)[0]
        nom = date(int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8]))
        return _FakeResponse(200, _make_payload_zip(nom))

    return opener


# ── A. Contract/artifact loading ────────────────────────────────────────────

def test_load_documented_exceptions_from_committed_repo():
    m = _load_runner()
    exc = m.load_documented_exceptions(REPO_ROOT)
    key = ("chunk_2022", DOC_DATE)
    assert key in exc
    e = exc[key]
    assert e["label"] == LABEL
    assert e["raw_filename"] == "20221110.export.CSV.zip"
    assert e["catalog_md5"] == "91e15516016f986e5b8a08712e1de95a"
    assert e["catalog_filesize_bytes"] == 6714105


def test_load_returns_empty_when_contract_absent(tmp_path):
    m = _load_runner()
    assert m.load_documented_exceptions(str(tmp_path)) == {}


def test_load_drops_entry_when_representation_absent(tmp_path):
    m = _load_runner()
    _copy_committed(tmp_path, config=True, rep=False)
    assert m.load_documented_exceptions(str(tmp_path)) == {}


def _tamper_contract(tmp_path, **scope_overrides):
    _copy_committed(tmp_path, config=True, rep=True)
    cfg_path = tmp_path / CONFIG_REL
    cfg = json.loads(cfg_path.read_text())
    cfg["documented_exceptions"][0]["allowed_scope"].update(scope_overrides)
    cfg_path.write_text(json.dumps(cfg))


def test_load_drops_on_md5_mismatch(tmp_path):
    m = _load_runner()
    _tamper_contract(tmp_path, catalog_md5="0" * 32)
    assert m.load_documented_exceptions(str(tmp_path)) == {}


def test_load_drops_on_filesize_mismatch(tmp_path):
    m = _load_runner()
    _tamper_contract(tmp_path, catalog_filesize_bytes=1)
    assert m.load_documented_exceptions(str(tmp_path)) == {}


def test_load_drops_on_label_mismatch(tmp_path):
    m = _load_runner()
    _copy_committed(tmp_path, config=True, rep=True)
    cfg_path = tmp_path / CONFIG_REL
    cfg = json.loads(cfg_path.read_text())
    cfg["documented_exceptions"][0]["label"] = "WRONG_LABEL"
    cfg_path.write_text(json.dumps(cfg))
    assert m.load_documented_exceptions(str(tmp_path)) == {}


# ── B. Narrow application (pure matcher) ─────────────────────────────────────

def test_match_exact_quintuple():
    m = _load_runner()
    exc = m.load_documented_exceptions(REPO_ROOT)
    url = m.date_to_daily_url(date(2022, 11, 10))
    assert m.documented_exception_match("chunk_2022", DOC_DATE, url, exc) is not None


def test_match_rejects_wrong_chunk():
    m = _load_runner()
    exc = m.load_documented_exceptions(REPO_ROOT)
    url = m.date_to_daily_url(date(2022, 11, 10))
    assert m.documented_exception_match("chunk_2021", DOC_DATE, url, exc) is None


def test_match_rejects_wrong_date():
    m = _load_runner()
    exc = m.load_documented_exceptions(REPO_ROOT)
    url = m.date_to_daily_url(date(2022, 11, 11))
    assert m.documented_exception_match("chunk_2022", "2022-11-11", url, exc) is None


def test_match_rejects_wrong_filename_for_right_key():
    m = _load_runner()
    exc = m.load_documented_exceptions(REPO_ROOT)
    # right key but URL points at a different filename
    assert m.documented_exception_match(
        "chunk_2022", DOC_DATE, "http://x/20221109.export.CSV.zip", exc
    ) is None


# ── C. Canon preservation (end-to-end run_chunk_build) ───────────────────────

def test_documented_exception_applies_and_continues(tmp_path, monkeypatch):
    m = _load_runner()
    _setup(m, monkeypatch, tmp_path, config=True, rep=True)
    opener = _opener_factory(m, fail_iso=DOC_DATE, fail_code=404)
    res = m.run_chunk_build(
        "chunk_2022", str(tmp_path), cli_flag=True,
        timestamp_utc="20260601T000000Z", opener=opener,
    )
    ded = res["metadata"]["documented_exception_diagnostic"]
    assert ded["documented_unavailable_data_confirmed_days"] == 1
    assert ded["raw_processed_days"] == 364
    assert ded["expected_calendar_days"] == 365
    assert ded["terminal_status_days"] == 365
    assert ded["terminal_status_complete"] is True
    assert ded["recovered_days"] == 0
    assert ded["known_no_data_gap_days"] == 0
    assert res["metadata"]["actual_completed_file_count"] == 364
    assert res["metadata"]["expected_file_count"] == 365
    doc_entries = ded["documented_exceptions"]
    assert len(doc_entries) == 1
    assert doc_entries[0]["date"] == DOC_DATE
    assert doc_entries[0]["raw_object_parsed"] is False
    assert doc_entries[0]["rows_recovered"] is False


def test_arbitrary_404_other_date_in_chunk_2022_halts(tmp_path, monkeypatch):
    m = _load_runner()
    _setup(m, monkeypatch, tmp_path, config=True, rep=True)
    opener = _opener_factory(m, fail_iso="2022-06-15", fail_code=404)
    with pytest.raises(m.FetchFailure):
        m.run_chunk_build(
            "chunk_2022", str(tmp_path), cli_flag=True,
            timestamp_utc="20260601T000001Z", opener=opener,
        )


def test_non_404_failure_on_doc_date_halts(tmp_path, monkeypatch):
    m = _load_runner()
    _setup(m, monkeypatch, tmp_path, config=True, rep=True)
    opener = _opener_factory(m, fail_iso=DOC_DATE, fail_code=500,
                             fail_reason="Server Error")
    with pytest.raises(m.FetchFailure):
        m.run_chunk_build(
            "chunk_2022", str(tmp_path), cli_flag=True,
            timestamp_utc="20260601T000002Z", opener=opener,
        )


def test_doc_date_404_without_contract_halts(tmp_path, monkeypatch):
    m = _load_runner()
    _setup(m, monkeypatch, tmp_path, config=False, rep=False)
    opener = _opener_factory(m, fail_iso=DOC_DATE, fail_code=404)
    with pytest.raises(m.FetchFailure):
        m.run_chunk_build(
            "chunk_2022", str(tmp_path), cli_flag=True,
            timestamp_utc="20260601T000003Z", opener=opener,
        )


def test_doc_date_404_without_representation_halts(tmp_path, monkeypatch):
    m = _load_runner()
    _setup(m, monkeypatch, tmp_path, config=True, rep=False)
    opener = _opener_factory(m, fail_iso=DOC_DATE, fail_code=404)
    with pytest.raises(m.FetchFailure):
        m.run_chunk_build(
            "chunk_2022", str(tmp_path), cli_flag=True,
            timestamp_utc="20260601T000004Z", opener=opener,
        )


# ── D. Raw-preference behavior ───────────────────────────────────────────────

def test_raw_available_processes_normally_no_exception(tmp_path, monkeypatch):
    m = _load_runner()
    _setup(m, monkeypatch, tmp_path, config=True, rep=True)
    opener = _opener_factory(m, fail_iso=None)  # all dates succeed
    res = m.run_chunk_build(
        "chunk_2022", str(tmp_path), cli_flag=True,
        timestamp_utc="20260601T000005Z", opener=opener,
    )
    ded = res["metadata"]["documented_exception_diagnostic"]
    assert ded["documented_unavailable_data_confirmed_days"] == 0
    assert ded["documented_exceptions"] == []
    assert res["metadata"]["actual_completed_file_count"] == 365
    assert ded["raw_processed_days"] == 365


# ── E. Metadata behavior / KNOWN_SUBSTRATE_GAPS / summary phrasing ───────────

def test_known_substrate_gaps_unchanged():
    m = _load_runner()
    assert tuple(m.KNOWN_SUBSTRATE_GAPS) == (
        "2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19",
    )


def test_summary_runtime_output_forbidden_tokens_absent(tmp_path, monkeypatch):
    """Row 22: ALL of F1..F6 must be absent from the runtime-emitted summary
    output for the documented-exception state (generalizes the prior
    slash-count-only check). The audited corpus is the generated `summary`
    string — NOT this test's own scaffolding."""
    m = _load_runner()
    _setup(m, monkeypatch, tmp_path, config=True, rep=True)
    opener = _opener_factory(m, fail_iso=DOC_DATE, fail_code=404)
    res = m.run_chunk_build(
        "chunk_2022", str(tmp_path), cli_flag=True,
        timestamp_utc="20260601T000006Z", opener=opener,
    )
    summary = m.render_chunk_summary("chunk_2022", res["metadata"])
    counts = _forbidden_counts(summary)
    assert counts == {"F1": 0, "F2": 0, "F3": 0, "F4": 0, "F5": 0, "F6": 0}, counts
    # Positive status assertions: the label and separated category counts
    # are present and explicit.
    assert "documented_exception_label" in summary
    assert "raw_processed_days: 364" in summary
    assert "documented_unavailable_data_confirmed_days: 1" in summary
    # documented metadata must not misclassify
    ded = res["metadata"]["documented_exception_diagnostic"]
    assert ded["no_data_gap"] is False
    assert ded["recovered"] is False
    assert ded["known_substrate_gap_amended"] is False


# ── Row 10: malformed-artifact fail-closed coverage ──────────────────────────

def test_malformed_contract_fails_closed(tmp_path, monkeypatch):
    """Row 10: a syntactically malformed contract must NOT silently apply the
    carve-out. Current behavior is fail-closed (the loader raises during JSON
    parse); the run aborts rather than applying any documented exception."""
    m = _load_runner()
    _copy_committed(tmp_path, config=True, rep=True)
    (tmp_path / CONFIG_REL).write_text("{ this is : not valid json ,,, ",
                                       encoding="utf-8")
    # Loader-level: fails closed by raising (no entry dict returned).
    with pytest.raises(json.JSONDecodeError):
        m.load_documented_exceptions(str(tmp_path))
    # End-to-end: a 404 on the documented date does NOT become a silent
    # carve-out; the run aborts (no successful result with a documented entry).
    _setup(m, monkeypatch, tmp_path, config=True, rep=True)
    (tmp_path / CONFIG_REL).write_text("{ this is : not valid json ,,, ",
                                       encoding="utf-8")
    opener = _opener_factory(m, fail_iso=DOC_DATE, fail_code=404)
    with pytest.raises(Exception):
        m.run_chunk_build(
            "chunk_2022", str(tmp_path), cli_flag=True,
            timestamp_utc="20260601T000010Z", opener=opener,
        )


def test_malformed_representation_fails_closed(tmp_path, monkeypatch):
    """Row 10: a syntactically malformed representation artifact must NOT
    silently apply the carve-out (fail-closed: loader raises during parse)."""
    m = _load_runner()
    _copy_committed(tmp_path, config=True, rep=True)
    (tmp_path / REP_REL).write_text("{ broken json :::", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        m.load_documented_exceptions(str(tmp_path))


# ── Row 12: other-chunk arbitrary-404 e2e halt (direct) ──────────────────────

def test_other_chunk_arbitrary_404_halts_e2e(tmp_path, monkeypatch):
    """Row 12: an arbitrary 404 in a chunk OTHER than chunk_2022 halts via the
    normal failure path, even with the committed contract present. The carve-out
    is keyed to (chunk_2022, 2022-11-10) only and must not apply to chunk_2021.
    KNOWN_SUBSTRATE_GAPS must remain the four 2014 dates."""
    m = _load_runner()
    # chunk_2021 universe (non-leap, 365 days) + committed contract present.
    _setup(m, monkeypatch, tmp_path, config=True, rep=True, isos=_year_isos(2021))
    opener = _opener_factory(m, fail_iso="2021-06-15", fail_code=404)
    with pytest.raises(m.FetchFailure):
        m.run_chunk_build(
            "chunk_2021", str(tmp_path), cli_flag=True,
            timestamp_utc="20260601T000012Z", opener=opener,
        )
    # Canon preserved: the matcher never applies to a non-target chunk, and KSG
    # is untouched.
    exc = m.load_documented_exceptions(str(tmp_path))
    url = m.date_to_daily_url(date(2021, 6, 15))
    assert m.documented_exception_match("chunk_2021", "2021-06-15", url, exc) is None
    assert tuple(m.KNOWN_SUBSTRATE_GAPS) == (
        "2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19",
    )
