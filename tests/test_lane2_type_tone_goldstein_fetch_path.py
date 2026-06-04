"""Adversarial synthetic-fixture tests for the Phase-2 Lane 2 TTG archive
fetch path.

These tests are SYNTHETIC-ONLY. They contact NO network, read no real GDELT /
result / market / outcome / join files, and write only under pytest `tmp_path`.
They prove the §11 Phase-2 fetch-path gate requirements:

  1.  no real network path is used by tests;
  2.  the real network/fetch path hard-errors by default before URL open;
  3.  real-fetch enablement is not reachable by env var, CLI flag, config-file
      toggle, local settings file, default parameter, or other runtime switch;
  4.  2023+ files are rejected before open/enumeration;
  5.  `source_file_date <= SQLDATE + 1` is enforced;
  6.  late rows from +2/+7/+30/+365/later are dropped before archive write;
  7.  same-day and +1 rows are eligible;
  8.  any civil_date+1 / bucket seam cannot double-shift eligibility;
  9.  edge-incomplete predictor days are excluded or diagnostic-routed;
  10. pre-window files are not opened to complete first-day coverage;
  11. DATEADDED is not used as an availability instrument;
  12. row-level SOURCEURL and DATEADDED are not retained as row fields;
  13. file-download URL provenance remains allowed in manifest metadata;
  14. forbidden fields are dropped;
  15. manifest/report output is structural-only (no sample rows / value summaries);
  16. manifest counts are value-agnostic (no QuadClass/Goldstein/NumMentions/
      AvgTone/sign/tone buckets);
  17. malformed or short rows fail closed;
  18. codebook/header index mismatch fails closed;
  19. source-file provenance manifest is deterministic from the pinned universe;
  20. outcome-convention inspection is read-only (no outcome/market/join reads);
  21. outcome/join-gate governing docs are not modified.
"""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
from pathlib import Path

import pytest

import lane2_type_tone_goldstein_local_archive as archive
import lane2_type_tone_goldstein_archive_fetch_path as fetch_path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Forbidden-field sentinels placed in input rows; none may surface in the
# archive, the manifest, or emitted text.
FORBIDDEN_SENTINELS = (
    "FORBID_ACTOR1NAME",
    "FORBID_EVENTCODE",
    "FORBID_DATEADDED",
    "FORBID_SOURCEURL",
    "FORBID_ACTIONGEO",
    "next_session_return",
    "FORBID_MARKET",
)

_N_COLS = 58


def make_gdelt_row(sqldate, quadclass, goldsteinscale, nummentions, avgtone):
    """One synthetic 58-col GDELT 1.0 row: approved values at documented
    indices, forbidden sentinels everywhere else (incl. DATEADDED idx 56 and
    SOURCEURL idx 57)."""
    cells = ["FILLER"] * _N_COLS
    cells[0] = "1000001"
    cells[archive.DATE_FIELD_COLUMN_INDEX] = sqldate
    cells[6] = "FORBID_ACTOR1NAME"
    cells[26] = "FORBID_EVENTCODE"
    cells[archive.QUADCLASS_COLUMN_INDEX] = quadclass
    cells[archive.GOLDSTEINSCALE_COLUMN_INDEX] = goldsteinscale
    cells[archive.NUMMENTIONS_COLUMN_INDEX] = nummentions
    cells[archive.AVGTONE_COLUMN_INDEX] = avgtone
    cells[36] = "FORBID_ACTIONGEO"
    cells[40] = "next_session_return"
    cells[50] = "FORBID_MARKET"
    cells[archive.FORBIDDEN_DATEADDED_COLUMN_INDEX] = "FORBID_DATEADDED"
    cells[archive.FORBIDDEN_SOURCEURL_COLUMN_INDEX] = "FORBID_SOURCEURL"
    return "\t".join(cells)


def make_payload(rows):
    return ("\n".join(rows) + "\n").encode("utf-8")


def make_zip_payload(rows, member_name="20140102.export.CSV"):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(member_name, ("\n".join(rows) + "\n"))
    return buf.getvalue()


class FetchSpy:
    """Records every call; performs no I/O. Used to prove a URL is never
    opened while the source gate is False."""

    def __init__(self):
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return b""


def _synthetic_fetcher(date_to_payload):
    """Return a fetch_callable(source_file_date, url) -> bytes that serves only
    in-memory synthetic payloads keyed by ISO date. Never touches the network."""

    def _fetch(source_file_date, source_file_url):
        return date_to_payload[source_file_date.isoformat()]

    return _fetch


# Run-gate kwargs: satisfy the three guards so the synthetic pipeline runs.
def _guarded(monkeypatch):
    monkeypatch.setattr(
        archive, "TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED", True
    )
    return dict(cli_flag=True, module_authorized=True,
                env={archive.ENV_GUARD_NAME: "1"})


# ── 1. No real network path used by tests ────────────────────────────────────

def test_source_gate_ships_false_and_no_network_lib_imported():
    assert fetch_path.REAL_FETCH_SOURCE_GATE_ENABLED is False
    # No network library is a module attribute of either module.
    for mod in (archive, fetch_path):
        for name in ("urllib", "requests", "socket", "http"):
            assert not hasattr(mod, name), (mod.__name__, name)


# ── 2. Real fetch hard-errors before URL open ────────────────────────────────

def test_real_fetch_hard_errors_before_url_open(monkeypatch):
    spy = FetchSpy()
    # If the gate were bypassed, _open_url would be reached; spy proves it isn't.
    monkeypatch.setattr(fetch_path, "_open_url", spy)
    with pytest.raises(fetch_path.RealFetchNotAuthorized) as ei:
        fetch_path.fetch_one_source_file(__import__("datetime").date(2014, 1, 2))
    assert str(ei.value) == fetch_path.REAL_FETCH_BLOCK_MESSAGE
    assert spy.calls == [], "no URL may be opened while the source gate is False"


# ── 3. Enablement not reachable via env / CLI / config / settings / param ────

def test_gate_not_reachable_via_runtime_config(monkeypatch):
    import datetime
    # Set every plausible runtime toggle; the gate must still block.
    monkeypatch.setenv("REAL_FETCH_SOURCE_GATE_ENABLED", "1")
    monkeypatch.setenv("LANE2_TTG_LOCAL_ARCHIVE_BUILD_AUTHORIZED", "1")
    monkeypatch.setenv("TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED", "1")
    monkeypatch.setenv("ENABLE_REAL_FETCH", "1")
    with pytest.raises(fetch_path.RealFetchNotAuthorized):
        fetch_path.fetch_one_source_file(
            datetime.date(2014, 1, 2), source_file_url="anything"
        )
    # The gate constant is a hard-coded boolean literal — assigned exactly once,
    # and its right-hand side is the literal `False` (never derived from an
    # environment variable, CLI parser, config/settings file, or any call).
    src_lines = Path(fetch_path.__file__).read_text().splitlines()
    assigns = [ln for ln in src_lines
               if ln.strip().startswith("REAL_FETCH_SOURCE_GATE_ENABLED =")
               and not ln.strip().startswith("REAL_FETCH_SOURCE_GATE_ENABLED ==")]
    assert assigns == ["REAL_FETCH_SOURCE_GATE_ENABLED = False"], assigns
    rhs = assigns[0].split("=", 1)[1].strip()
    assert rhs == "False"  # literal; not os.environ/getenv/argparse/config/bool(...)
    for bad in ("environ", "getenv", "argv", "argparse", "ArgumentParser",
                "configparser", "open(", "bool("):
        assert bad not in assigns[0], bad


# ── 4. 2023+ rejected before open / enumeration ──────────────────────────────

def test_2023plus_rejected_at_enumeration(monkeypatch):
    spy = FetchSpy()
    g = _guarded(monkeypatch)
    with pytest.raises(archive.Post2022SealBreach):
        fetch_path.run_phase2_archive_build(
            ["2022-12-30", "2023-01-01"], out_dir="UNUSED",
            fetch_callable=spy, **g
        )
    assert spy.calls == [], "no file fetched after a 2023+ seal breach"


# ── 5 & 7. Eligibility: same-day and +1 eligible; F>SQLDATE+1 ineligible ─────

def test_eligibility_same_day_and_plus_one():
    import datetime
    t = datetime.date(2014, 6, 10)
    assert archive.row_is_eligible(t, t) is True                      # offset 0
    assert archive.row_is_eligible(t + datetime.timedelta(1), t) is True   # +1
    assert archive.row_is_eligible(t - datetime.timedelta(1), t) is True   # pre-2015 +1 bucket
    assert archive.row_is_eligible(t + datetime.timedelta(2), t) is False  # late


# ── 6. Late rows (+2/+7/+30/+365/later) dropped before archive write ─────────

# In-window late offsets: the file date stays inside [2013-04-01, 2022-12-31]
# so the late row is dropped by the per-row date-eligibility rule.
@pytest.mark.parametrize("late_days", [2, 7, 30, 365])
def test_late_rows_dropped(monkeypatch, tmp_path, late_days):
    import datetime
    sqld = datetime.date(2014, 6, 10)        # interior, fully covered
    file_d = sqld + datetime.timedelta(days=late_days)
    assert archive.WINDOW_START <= file_d <= archive.WINDOW_END
    row = make_gdelt_row(sqld.strftime("%Y%m%d"), "4", "1.0", "5", "0.5")
    cls = archive.classify_payload_rows(make_payload([row]), source_file_date=file_d)
    assert cls.retained_row_count == 0
    assert cls.dropped_by_reason[archive.DROP_REASON_DATE_ELIGIBILITY_FAILURE] == 1


# A far-later file (offset -3650 => file ~10y after SQLDATE) falls OUTSIDE the
# authorized 2013-2022 window: it is never enumerated, and a defensive classify
# call fails closed rather than folding it in.
def test_far_late_file_outside_window_fails_closed():
    import datetime
    sqld = datetime.date(2014, 6, 10)
    file_d = sqld + datetime.timedelta(days=3650)  # ~2024, outside window
    assert not (archive.WINDOW_START <= file_d <= archive.WINDOW_END)
    row = make_gdelt_row(sqld.strftime("%Y%m%d"), "4", "1.0", "5", "0.5")
    with pytest.raises(archive.Post2022SealBreach):
        archive.classify_payload_rows(make_payload([row]), source_file_date=file_d)


# ── 8. civil_date+1 / bucket seam cannot double-shift eligibility ────────────

def test_no_double_shift_of_eligibility(monkeypatch, tmp_path):
    import datetime
    # SQLDATE=t row arriving in file F=t+1 (offset -1): eligible, retained, and
    # KEYED at t (not t+1). Proves the single +1 lives only in the inequality.
    t = datetime.date(2014, 6, 10)
    f = t + datetime.timedelta(days=1)
    row = make_gdelt_row(t.strftime("%Y%m%d"), "2", "3.0", "9", "1.0")
    cls = archive.classify_payload_rows(make_payload([row]), source_file_date=f)
    assert cls.retained_row_count == 1
    assert cls.retained_rows[0]["sqldate"] == t.isoformat()  # not t+1
    # A second +1 would make F=t+2 eligible; it must NOT.
    assert archive.row_is_eligible(t + datetime.timedelta(days=2), t) is False
    # ELIGIBILITY_DELTA_DAYS is exactly one.
    assert archive.ELIGIBILITY_DELTA_DAYS == 1


# ── 9. Edge-incomplete predictor days excluded / diagnostic-routed ───────────

def test_edge_incomplete_excluded_and_routable():
    import datetime
    # End edge: SQLDATE=2022-12-31 needs F=2023-01-01 (sealed) -> not covered.
    end = datetime.date(2022, 12, 31)
    assert archive.is_sqldate_fully_covered(end) is False
    # Start edge: SQLDATE=2013-04-01 needs F=2013-03-31 (pre-window) -> not covered.
    start = datetime.date(2013, 4, 1)
    assert archive.is_sqldate_fully_covered(start) is False
    # Interior day is covered.
    assert archive.is_sqldate_fully_covered(datetime.date(2014, 6, 10)) is True

    # Excluded from primary by default ...
    row = make_gdelt_row(end.strftime("%Y%m%d"), "1", "0.0", "3", "0.0")
    cls = archive.classify_payload_rows(make_payload([row]), source_file_date=end)
    assert cls.retained_row_count == 0
    assert cls.dropped_by_reason[archive.DROP_REASON_EDGE_WINDOW_EXCLUSION] == 1
    assert cls.edge_routed_rows == []
    # ... or routed to a separately governed diagnostic set when requested.
    cls2 = archive.classify_payload_rows(
        make_payload([row]), source_file_date=end, route_edge_incomplete=True
    )
    assert cls2.retained_row_count == 0
    assert len(cls2.edge_routed_rows) == 1


# ── 10. Pre-window files not opened to complete first-day coverage ───────────

def test_pre_window_files_not_opened(monkeypatch):
    spy = FetchSpy()
    g = _guarded(monkeypatch)
    with pytest.raises(archive.Post2022SealBreach):
        fetch_path.run_phase2_archive_build(
            ["2013-03-31", "2013-04-02"], out_dir="UNUSED",
            fetch_callable=spy, **g
        )
    assert spy.calls == [], "no pre-window file may be fetched"


# ── 11. DATEADDED is not used as an availability instrument ──────────────────

def test_dateadded_not_used_for_availability():
    import datetime
    sqld = datetime.date(2014, 6, 10)
    file_d = sqld + datetime.timedelta(days=1)  # eligible by file date
    # DATEADDED cell holds an absurd far-future-looking token; it must be
    # ignored entirely — eligibility uses source_file_date only.
    cells = make_gdelt_row(sqld.strftime("%Y%m%d"), "4", "1.0", "5", "0.5").split("\t")
    cells[archive.FORBIDDEN_DATEADDED_COLUMN_INDEX] = "20991231"
    cls = archive.classify_payload_rows(
        make_payload(["\t".join(cells)]), source_file_date=file_d
    )
    assert cls.retained_row_count == 1  # eligible despite DATEADDED value
    assert "20991231" not in json.dumps(cls.retained_rows)


# ── 12. Row-level SOURCEURL and DATEADDED not retained as row fields ─────────

def test_sourceurl_and_dateadded_not_retained():
    import datetime
    row = make_gdelt_row("20140610", "4", "-9.8765", "987654", "-87.654321")
    cls = archive.classify_payload_rows(
        make_payload([row]), source_file_date=datetime.date(2014, 6, 10)
    )
    r = cls.retained_rows[0]
    assert set(r.keys()) == set(archive.APPROVED_FIELD_NAMES)
    assert "dateadded" not in r and "sourceurl" not in r
    blob = json.dumps(cls.retained_rows)
    assert "FORBID_DATEADDED" not in blob
    assert "FORBID_SOURCEURL" not in blob
    # The approved schema (5 fields) contains neither.
    assert archive.FORBIDDEN_DATEADDED_COLUMN_INDEX not in (
        archive.DATE_FIELD_COLUMN_INDEX, archive.QUADCLASS_COLUMN_INDEX,
        archive.GOLDSTEINSCALE_COLUMN_INDEX, archive.NUMMENTIONS_COLUMN_INDEX,
        archive.AVGTONE_COLUMN_INDEX,
    )
    assert archive.FORBIDDEN_SOURCEURL_COLUMN_INDEX not in (
        archive.DATE_FIELD_COLUMN_INDEX, archive.QUADCLASS_COLUMN_INDEX,
        archive.GOLDSTEINSCALE_COLUMN_INDEX, archive.NUMMENTIONS_COLUMN_INDEX,
        archive.AVGTONE_COLUMN_INDEX,
    )


# ── 13. File-download URL provenance allowed in manifest metadata ────────────

def test_download_url_provenance_allowed_distinct_from_sourceurl(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    rows = [make_gdelt_row("20140610", "4", "1.0", "5", "0.5")]
    fetcher = _synthetic_fetcher({"2014-06-10": make_payload(rows)})
    res = fetch_path.run_phase2_archive_build(
        ["2014-06-10"], out_dir=str(tmp_path / "out"),
        fetch_callable=fetcher, **g
    )
    pf = res["manifest"]["per_file_provenance"][0]
    # The file-download URL is present as provenance ...
    assert pf["source_file_url"].endswith("20140610.export.CSV.zip")
    assert "data.gdeltproject.org/events/" in pf["source_file_url"]
    # ... and the row-level SOURCEURL value never appears anywhere in manifest.
    assert "FORBID_SOURCEURL" not in json.dumps(res["manifest"])


# ── 14. Forbidden fields dropped from archive output ─────────────────────────

def test_forbidden_fields_dropped_from_archive(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    rows = [make_gdelt_row("20140610", "4", "-9.8765", "987654", "-87.654321")]
    fetcher = _synthetic_fetcher({"2014-06-10": make_payload(rows)})
    res = fetch_path.run_phase2_archive_build(
        ["2014-06-10"], out_dir=str(tmp_path / "out"),
        fetch_callable=fetcher, **g
    )
    data = Path(res["archive_artifact"]["output_path"]).read_bytes()
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel.encode() not in data, sentinel
    assert b"FILLER" not in data


# ── 15. Manifest structural-only: no sample rows / value summaries ───────────

def test_manifest_structural_only_no_value_summaries(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    rows = [make_gdelt_row("20140610", "4", "-9.8765", "987654", "-87.654321")]
    fetcher = _synthetic_fetcher({"2014-06-10": make_payload(rows)})
    res = fetch_path.run_phase2_archive_build(
        ["2014-06-10"], out_dir=str(tmp_path / "out"),
        fetch_callable=fetcher, **g
    )
    manifest = res["manifest"]
    # No retained row content / approved-field values in the manifest.
    stripped = json.dumps(_strip_hashes(manifest))
    for tok in ("-9.8765", "-87.654321", "987654"):
        assert tok not in stripped, tok
    # No "rows"/"sample"/"example" container at any level.
    keys = _all_keys(manifest)
    forbidden_terms = (
        "mean", "median", "histogram", "distribution", "correlation", "zscore",
        "z-score", "stdev", "variance", "percentile", "quantile", "sample",
        "example", "_min", "_max", "minimum", "maximum",
    )
    for k in keys:
        low = k.lower()
        for term in forbidden_terms:
            assert term not in low, (k, term)
    assert "rows" not in keys
    # The values DO live in the archive itself (the archive is not a summary).
    archive_text = Path(res["archive_artifact"]["output_path"]).read_text()
    for tok in ("-9.8765", "-87.654321", "987654"):
        assert tok in archive_text


# ── 16. Manifest counts value-agnostic (no Quad/Goldstein/NumMentions/Tone) ──

def test_manifest_counts_value_agnostic(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    rows = [
        make_gdelt_row("20140610", "1", "5.0", "10", "9.0"),
        make_gdelt_row("20140610", "4", "-5.0", "20", "-9.0"),
    ]
    fetcher = _synthetic_fetcher({"2014-06-10": make_payload(rows)})
    res = fetch_path.run_phase2_archive_build(
        ["2014-06-10"], out_dir=str(tmp_path / "out"),
        fetch_callable=fetcher, **g
    )
    pf = res["manifest"]["per_file_provenance"][0]
    # Retained count is a single structural integer, not partitioned by value.
    assert pf["retained_row_count"] == 2
    assert isinstance(pf["retained_row_count"], int)
    # Dropped counts keyed ONLY by closed structural reasons.
    assert set(pf["dropped_by_reason"].keys()) == set(archive.CLOSED_DROP_REASONS)
    keys = _all_keys(res["manifest"])
    # No key bucketed by a substantive field value or by sign/tone category.
    bad_key_tokens = (
        "quadclass", "goldstein", "nummentions", "avgtone",
        "by_value", "by_tone", "by_sign", "by_quad", "by_goldstein",
        "_bucket", "bucketed", "positive_", "negative_", "tone_band",
    )
    for k in keys:
        low = k.lower()
        for bad in bad_key_tokens:
            assert bad not in low, (k, bad)


# ── 17. Malformed / short rows fail closed ───────────────────────────────────

def test_short_and_malformed_rows_fail_closed():
    import datetime
    f = datetime.date(2014, 6, 10)
    short = "\t".join(["x"] * 10)  # far fewer than required columns
    baddate = make_gdelt_row("NOTADATE", "4", "1.0", "5", "0.5")
    good = make_gdelt_row("20140610", "4", "1.0", "5", "0.5")
    cls = archive.classify_payload_rows(
        make_payload([short, baddate, good]), source_file_date=f
    )
    assert cls.retained_row_count == 1
    assert cls.dropped_by_reason[archive.DROP_REASON_SHORT_ROW] == 1
    assert cls.dropped_by_reason[archive.DROP_REASON_FIELD_PARSE_FAILURE] == 1


# ── 18. Codebook / header index mismatch fails closed ────────────────────────

def test_codebook_index_mismatch_fails_closed():
    # Matching map passes.
    archive.assert_codebook_indices(fetch_path.CANONICAL_CODEBOOK_DERIVED_INDICES)
    # A wrong index fails closed.
    bad = dict(fetch_path.CANONICAL_CODEBOOK_DERIVED_INDICES)
    bad["avgtone"] = 33  # NumArticles, not AvgTone
    with pytest.raises(archive.CodebookIndexMismatch):
        archive.assert_codebook_indices(bad)
    # Build refuses with a mismatched map, before guards/enumeration/fetch.
    with pytest.raises(archive.CodebookIndexMismatch):
        fetch_path.run_phase2_archive_build(
            ["2014-06-10"], out_dir="UNUSED",
            fetch_callable=FetchSpy(), codebook_derived_indices=bad,
        )


# ── 19. Provenance manifest deterministic from the pinned universe ───────────

def test_provenance_manifest_deterministic(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    rows = {
        "2014-06-10": make_payload([make_gdelt_row("20140610", "4", "1.0", "5", "0.5")]),
        "2014-06-11": make_payload([make_gdelt_row("20140611", "2", "2.0", "6", "1.0")]),
    }
    fetcher = _synthetic_fetcher(rows)
    r1 = fetch_path.run_phase2_archive_build(
        ["2014-06-11", "2014-06-10"], out_dir=str(tmp_path / "a"),
        fetch_callable=fetcher, **g
    )
    r2 = fetch_path.run_phase2_archive_build(
        ["2014-06-10", "2014-06-11"], out_dir=str(tmp_path / "b"),
        fetch_callable=fetcher, **g
    )
    # Same archive bytes regardless of candidate ordering (enumeration sorts).
    assert r1["archive_artifact"]["sha256"] == r2["archive_artifact"]["sha256"]
    assert r1["manifest"]["per_file_provenance"] == r2["manifest"]["per_file_provenance"]


# ── 20. Outcome-convention inspection read-only (no outcome/market/join reads) ─

def test_no_outcome_market_join_reads_in_modules():
    # The modules must not OPEN or COMPUTE outcome/market/join data. (Note:
    # "next_session_return" legitimately appears only in the archive module's
    # forbidden-field DENYLIST — that is a drop instruction, not a read — so it
    # is not banned here.) Ban operational outcome/market/join tokens instead.
    for mod in (archive, fetch_path):
        src = Path(mod.__file__).read_text().lower()
        for bad in ("adj_close", "market_daily", "join_gdelt_spy",
                    "pct_change", "return_price_col", "build_next_session_return"):
            assert bad not in src, (mod.__name__, bad)


# ── 21. Outcome / join-gate governing docs not modified ──────────────────────

_PINNED_DOC_SHA256 = {
    "docs/lane2_type_tone_goldstein_outcome_basis_close_field_resolution_v0.1.md":
        "95bb9596a99cf87269d6115947f42542b9bfe2e4ccb87bc22b11b6a47ccfa7f9",
    "docs/lane2_type_tone_goldstein_outcome_side_join_gate_locks_v0.1.md":
        "4cacb0b6b26f4d75a3c747bc1973a8916d6d0fcdb012b8ff6a2830840eb1d09b",
}


def test_outcome_join_gate_docs_unmodified():
    for rel, want in _PINNED_DOC_SHA256.items():
        data = (REPO_ROOT / rel).read_bytes()
        got = hashlib.sha256(data).hexdigest()
        assert got == want, "governing doc modified: {}".format(rel)


# ── helpers ──────────────────────────────────────────────────────────────────

def _strip_hashes(obj):
    if isinstance(obj, dict):
        return {
            k: ("<hash>" if k in ("sha256", "byte_sha256") else _strip_hashes(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_strip_hashes(v) for v in obj]
    return obj


def _all_keys(obj):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.append(k)
            out.extend(_all_keys(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(_all_keys(v))
    return out
