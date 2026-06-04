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


# ═════════════════════════════════════════════════════════════════════════════
# Pre-contact real-run hardening tests (§8 items 1-20). Synthetic / local only.
# ═════════════════════════════════════════════════════════════════════════════

def _make_row_ncols(n, sqldate="20140610"):
    """Build a TAB row with EXACTLY n columns, with a valid SQLDATE at idx 1 and
    valid approved values at idx 29/30/31/34 when n is wide enough. Used to prove
    the exact-58 guard rejects wrong-width rows that would otherwise satisfy the
    approved-index short-row guard."""
    cells = ["FILLER"] * n
    if n > archive.DATE_FIELD_COLUMN_INDEX:
        cells[archive.DATE_FIELD_COLUMN_INDEX] = sqldate
    for idx, val in ((archive.QUADCLASS_COLUMN_INDEX, "4"),
                     (archive.GOLDSTEINSCALE_COLUMN_INDEX, "1.0"),
                     (archive.NUMMENTIONS_COLUMN_INDEX, "5"),
                     (archive.AVGTONE_COLUMN_INDEX, "0.5")):
        if n > idx:
            cells[idx] = val
    return "\t".join(cells)


def _mk_manifests(file_map):
    """Build official-style md5sums + filesizes bytes from {filename: bytes}."""
    md5_lines = ["{}  {}".format(hashlib.md5(b).hexdigest(), fn)
                 for fn, b in file_map.items()]
    size_lines = ["{} {}".format(len(b), fn) for fn, b in file_map.items()]
    return (("\n".join(md5_lines) + "\n").encode("utf-8"),
            ("\n".join(size_lines) + "\n").encode("utf-8"))


# 1 & 2. _open_url itself is gated before urllib import/open; not runtime-flippable.

def test_open_url_itself_gated_before_urllib_import():
    spy = FetchSpy()
    # Direct call to _open_url must hard-error while the gate is False.
    with pytest.raises(fetch_path.RealFetchNotAuthorized) as ei:
        fetch_path._open_url("http://data.gdeltproject.org/events/20140610.export.CSV.zip",
                             _opener=spy)
    assert "_open_url defense-in-depth" in str(ei.value)
    assert spy.calls == [], "no opener may be invoked while the gate is False"
    # Source-order proof: the gate check precedes the lazy urllib import inside _open_url.
    src = Path(fetch_path.__file__).read_text()
    body = src.split("def _open_url(", 1)[1]
    gate_pos = body.index("if not REAL_FETCH_SOURCE_GATE_ENABLED:")
    import_pos = body.index("import urllib")
    assert gate_pos < import_pos, "gate must be checked before the urllib import"


def test_open_url_gate_not_runtime_flippable(monkeypatch):
    monkeypatch.setenv("REAL_FETCH_SOURCE_GATE_ENABLED", "1")
    monkeypatch.setenv("ENABLE_REAL_FETCH", "1")
    with pytest.raises(fetch_path.RealFetchNotAuthorized):
        fetch_path._open_url("http://example.invalid/x")


# 3. Source gate remains disabled in committed code.

def test_source_gate_remains_disabled_in_committed_code():
    assert fetch_path.REAL_FETCH_SOURCE_GATE_ENABLED is False
    src_lines = Path(fetch_path.__file__).read_text().splitlines()
    assigns = [ln for ln in src_lines
               if ln.strip().startswith("REAL_FETCH_SOURCE_GATE_ENABLED =")
               and not ln.strip().startswith("REAL_FETCH_SOURCE_GATE_ENABLED ==")]
    assert assigns == ["REAL_FETCH_SOURCE_GATE_ENABLED = False"], assigns


# 4 & 12. Integrity manifests required + universe reconciled against them.

def test_universe_reconciliation_ok_and_required():
    import datetime
    dates = [datetime.date(2013, 4, d) for d in (2, 3, 4)]
    fnames = fetch_path.expected_source_filenames(dates)
    file_map = {fn: ("payload-" + fn).encode() for fn in fnames}
    md5_b, size_b = _mk_manifests(file_map)
    md5map = fetch_path.parse_md5sums(md5_b.decode())
    sizemap = fetch_path.parse_filesizes(size_b.decode())
    status = fetch_path.reconcile_universe_against_manifests(fnames, md5map, sizemap)
    assert status["reconciled_ok"] is True
    assert status["expected_count"] == 3
    assert status["missing_from_md5sums"] == [] and status["missing_from_filesizes"] == []


# 5. Missing md5sums entry fails closed.

def test_missing_md5sums_entry_fails_closed():
    import datetime
    fnames = fetch_path.expected_source_filenames(
        [datetime.date(2013, 4, 2), datetime.date(2013, 4, 3)])
    file_map = {fn: b"x" for fn in fnames}
    md5_b, size_b = _mk_manifests(file_map)
    md5map = fetch_path.parse_md5sums(md5_b.decode())
    sizemap = fetch_path.parse_filesizes(size_b.decode())
    del md5map[fnames[1]]  # drop one md5 entry
    with pytest.raises(fetch_path.IntegrityManifestError):
        fetch_path.reconcile_universe_against_manifests(fnames, md5map, sizemap)


# 6. Missing filesizes entry fails closed.

def test_missing_filesizes_entry_fails_closed():
    import datetime
    fnames = fetch_path.expected_source_filenames(
        [datetime.date(2013, 4, 2), datetime.date(2013, 4, 3)])
    file_map = {fn: b"x" for fn in fnames}
    md5_b, size_b = _mk_manifests(file_map)
    md5map = fetch_path.parse_md5sums(md5_b.decode())
    sizemap = fetch_path.parse_filesizes(size_b.decode())
    del sizemap[fnames[0]]  # drop one size entry
    with pytest.raises(fetch_path.IntegrityManifestError):
        fetch_path.reconcile_universe_against_manifests(fnames, md5map, sizemap)


# 7. MD5 mismatch fails closed.

def test_md5_mismatch_fails_closed():
    fn = "20130402.export.CSV.zip"
    data = b"the-real-bytes"
    md5_b, size_b = _mk_manifests({fn: data})
    md5map = fetch_path.parse_md5sums(md5_b.decode())
    sizemap = fetch_path.parse_filesizes(size_b.decode())
    tampered = b"tampered-bytes!"  # different content
    assert len(tampered) != len(data) or True
    with pytest.raises(fetch_path.IntegrityVerificationError):
        fetch_path.verify_file_integrity(fn, tampered, md5map, sizemap)


# 8. Byte-size mismatch fails closed (MD5 map points at the right md5, size wrong).

def test_byte_size_mismatch_fails_closed():
    fn = "20130402.export.CSV.zip"
    data = b"abc"
    md5map = {fn: hashlib.md5(data).hexdigest()}
    sizemap = {fn: 999}  # wrong size on purpose
    with pytest.raises(fetch_path.IntegrityVerificationError):
        fetch_path.verify_file_integrity(fn, data, md5map, sizemap)


# 9. Unstable retry fails closed.

def test_unstable_retry_fails_closed():
    import datetime
    seq = [b"v1", b"v2-different"]  # second attempt differs

    def _flaky(source_file_date, url):
        return seq.pop(0)

    with pytest.raises(fetch_path.UnstableDownloadError):
        fetch_path.fetch_stable(datetime.date(2013, 4, 2),
                                fetch_callable=_flaky, attempts=2)


def test_stable_retry_returns_bytes():
    import datetime

    def _steady(source_file_date, url):
        return b"identical-bytes"

    out = fetch_path.fetch_stable(datetime.date(2013, 4, 2),
                                  fetch_callable=_steady, attempts=3)
    assert out == b"identical-bytes"


# 10 & 11. Cached zip re-verified before use; cache is not a bypass.

def test_cached_zip_reverified_before_use(tmp_path):
    fn = "20130402.export.CSV.zip"
    data = b"cached-good-bytes"
    md5_b, size_b = _mk_manifests({fn: data})
    md5map = fetch_path.parse_md5sums(md5_b.decode())
    sizemap = fetch_path.parse_filesizes(size_b.decode())
    cache_file = tmp_path / fn
    cache_file.write_bytes(data)
    status = fetch_path.verify_cached_zip(str(cache_file), fn, md5map, sizemap)
    assert status["integrity_status"] == "verified"
    assert status["source"] == "cache"
    assert status["cache_path"] == str(cache_file)


def test_cache_is_not_a_bypass_around_integrity(tmp_path):
    fn = "20130402.export.CSV.zip"
    good = b"official-bytes"
    md5_b, size_b = _mk_manifests({fn: good})
    md5map = fetch_path.parse_md5sums(md5_b.decode())
    sizemap = fetch_path.parse_filesizes(size_b.decode())
    cache_file = tmp_path / fn
    cache_file.write_bytes(b"CORRUPT-cache-bytes")  # present but wrong
    with pytest.raises(fetch_path.CacheIntegrityError):
        fetch_path.verify_cached_zip(str(cache_file), fn, md5map, sizemap)


# 13-16. Exact 58-column layout enforcement.

def test_exact_58_layout_passes():
    assert archive.EXPECTED_DAILY_COLUMN_COUNT == 58
    assert archive.is_exact_daily_layout(58) is True
    st = archive.exact_daily_layout_status(_make_row_ncols(58))
    assert st["ok"] is True and st["column_count"] == 58 and st["expected"] == 58


@pytest.mark.parametrize("ncols", [35, 45, 59])
def test_wrong_width_rows_fail_exact_layout(ncols):
    # Unit check on the validator.
    assert archive.is_exact_daily_layout(ncols) is False
    assert archive.exact_daily_layout_status(_make_row_ncols(ncols))["ok"] is False


def test_exact_layout_enforced_in_classify_distinct_from_short_guard():
    import datetime
    f = datetime.date(2014, 6, 10)
    # 35/45/59-col rows all carry the max approved index (34) and a valid SQLDATE.
    rows = [_make_row_ncols(35), _make_row_ncols(45), _make_row_ncols(59)]
    payload = ("\n".join(rows) + "\n").encode("utf-8")
    cls = archive.classify_payload_rows(payload, source_file_date=f,
                                        enforce_exact_columns=True)
    assert cls.retained_row_count == 0
    assert cls.dropped_by_reason[archive.DROP_REASON_COLUMN_COUNT_MISMATCH] == 3
    assert cls.dropped_by_reason[archive.DROP_REASON_SHORT_ROW] == 0
    # Distinctness: WITHOUT exact enforcement, a 45-col row (max approved idx
    # present) slips past the short-row guard and is retained — which is exactly
    # why the exact-58 guard is needed.
    cls_off = archive.classify_payload_rows(
        ("\n".join([_make_row_ncols(45)]) + "\n").encode("utf-8"),
        source_file_date=f, enforce_exact_columns=False)
    assert cls_off.retained_row_count == 1
    assert cls_off.dropped_by_reason[archive.DROP_REASON_COLUMN_COUNT_MISMATCH] == 0
    # Exactly-58 valid row is retained under enforcement.
    good = make_gdelt_row("20140610", "4", "1.0", "5", "0.5")
    cls_good = archive.classify_payload_rows(make_payload([good]), source_file_date=f,
                                             enforce_exact_columns=True)
    assert cls_good.retained_row_count == 1


# 17 & 18. Integrity/report output value-agnostic; no sample rows / value summaries.

def test_integrity_status_value_agnostic():
    fn = "20130402.export.CSV.zip"
    data = b"some-zip-bytes"
    md5map = {fn: hashlib.md5(data).hexdigest()}
    sizemap = {fn: len(data)}
    status = fetch_path.verify_file_integrity(fn, data, md5map, sizemap)
    keys = _all_keys(status)
    for bad in ("quadclass", "goldstein", "nummentions", "avgtone", "tone",
                "rows", "sample", "mean", "median", "bucket", "distribution",
                "value_counts", "groupby"):
        for k in keys:
            assert bad not in k.lower(), (k, bad)
    # Only structural keys present.
    assert set(status.keys()) >= {"filename", "byte_size", "official_md5",
                                  "computed_md5", "md5_ok", "size_ok",
                                  "sha256_local_provenance", "integrity_status"}
    # Manifest provenance is SHA-256 + size only (no field values).
    prov = fetch_path.manifest_provenance(b"md5sums-bytes", b"filesizes-bytes")
    assert "md5sums_sha256" in prov and "filesizes_sha256" in prov
    assert "quadclass" not in json.dumps(prov)


# 19. No 2023+ enumeration/open path exists.

def test_no_2023plus_enumeration_or_open_path():
    import datetime
    with pytest.raises(archive.Post2022SealBreach):
        archive.enumerate_source_universe(["2023-01-01"])
    # The real fetch of a 2023 date hard-errors at the gate before any window/open.
    with pytest.raises(fetch_path.RealFetchNotAuthorized):
        fetch_path.fetch_one_source_file(datetime.date(2023, 6, 15))
    assert archive.WINDOW_END == datetime.date(2022, 12, 31)
    assert archive.SEAL_START == datetime.date(2023, 1, 1)


# 20. No real network contact occurs in tests (gate False => fetch path inert).

def test_no_real_network_contact_possible_in_tests():
    import datetime
    assert fetch_path.REAL_FETCH_SOURCE_GATE_ENABLED is False
    # Default (real) fetch_stable path hard-errors at the gate, no network.
    with pytest.raises(fetch_path.RealFetchNotAuthorized):
        fetch_path.fetch_stable(datetime.date(2014, 6, 10), attempts=2)
    # Neither module exposes a live network library as an attribute.
    for mod in (archive, fetch_path):
        for name in ("urllib", "requests", "socket", "http"):
            assert not hasattr(mod, name), (mod.__name__, name)


# Slice-aware coverage helper (future bounded-run requirement, §10).

def test_slice_aware_coverage_for_bounded_april_2013():
    import datetime
    fetched = {datetime.date(2013, 4, d) for d in range(1, 31)}  # 2013-04-01..30
    # Interior days fully covered.
    assert archive.fetched_set_fully_covers(datetime.date(2013, 4, 2), fetched) is True
    assert archive.fetched_set_fully_covers(datetime.date(2013, 4, 29), fetched) is True
    # Slice edges NOT fully covered (need pre-window 03-31 / unfetched 05-01).
    assert archive.fetched_set_fully_covers(datetime.date(2013, 4, 1), fetched) is False
    assert archive.fetched_set_fully_covers(datetime.date(2013, 4, 30), fetched) is False


# ═════════════════════════════════════════════════════════════════════════════
# WIRED bounded-run orchestration tests (§10 items 1-28). Synthetic / local only.
# ═════════════════════════════════════════════════════════════════════════════

def _april_dates():
    import datetime
    return [datetime.date(2013, 4, d) for d in range(1, 31)]  # 2013-04-01..30


def _april_payloads():
    """One exactly-58-col row per file, SQLDATE == file date (offset 0)."""
    out = {}
    for d in _april_dates():
        out[d] = make_payload([make_gdelt_row(d.strftime("%Y%m%d"), "4", "1.0", "5", "0.5")])
    return out


def _manifests_for(payloads):
    file_map = {fetch_path.expected_source_filename(d): payloads[d] for d in payloads}
    return _mk_manifests(file_map)


class RecordingFetcher:
    """Injected non-network fetcher that serves in-memory payloads and records
    the dates it was asked for (to prove no out-of-slice fetch is attempted)."""

    def __init__(self, payloads):
        self.payloads = payloads
        self.dates = []

    def __call__(self, source_file_date, source_file_url):
        self.dates.append(source_file_date)
        return self.payloads[source_file_date]


def _run_april(monkeypatch, tmp_path, *, payloads=None, fetcher=None, cache_dir=None,
               md5_b=None, size_b=None, fetch_attempts=2, write_cache=True,
               out_name="out"):
    g = _guarded(monkeypatch)
    payloads = payloads if payloads is not None else _april_payloads()
    if md5_b is None or size_b is None:
        md5_b, size_b = _manifests_for(payloads)
    if fetcher is None:
        fetcher = RecordingFetcher(payloads)
    res = fetch_path.run_bounded_integrity_build(
        "2013-04-01", "2013-04-30", out_dir=str(tmp_path / out_name),
        md5sums_bytes=md5_b, filesizes_bytes=size_b,
        cache_dir=cache_dir, fetch_callable=fetcher,
        fetch_attempts=fetch_attempts, write_cache=write_cache, **g,
    )
    return res, fetcher


# 1. Source gate remains disabled (committed).

def test_wired_source_gate_remains_disabled():
    assert fetch_path.REAL_FETCH_SOURCE_GATE_ENABLED is False


# 2 & 16-19. Wired happy path: reconciliation runs; slice-aware coverage applied.

def test_wired_happy_path_slice_coverage(monkeypatch, tmp_path):
    res, fetcher = _run_april(monkeypatch, tmp_path)
    # Manifest reconciliation ran and reconciled all 30 expected files.
    assert res["reconcile_status"]["reconciled_ok"] is True
    assert res["reconcile_status"]["expected_count"] == 30
    # 17/18: 2013-04-01 and 2013-04-30 routed OUT of the primary archive.
    assert "2013-04-01" not in res["primary_covered_sqldates"]
    assert "2013-04-30" not in res["primary_covered_sqldates"]
    assert "2013-04-30" in res["slice_edge_incomplete_sqldates"]
    assert "2013-04-01" in res["window_edge_incomplete_days"]
    # 19: covered primary dates are exactly 2013-04-02 .. 2013-04-29.
    expected = ["2013-04-{:02d}".format(d) for d in range(2, 30)]
    assert res["primary_covered_sqldates"] == expected


# 20. No 2013-03-31 or 2013-05-01 fetch/open is attempted.

def test_wired_no_out_of_slice_fetch(monkeypatch, tmp_path):
    import datetime
    res, fetcher = _run_april(monkeypatch, tmp_path)
    assert datetime.date(2013, 3, 31) not in fetcher.dates
    assert datetime.date(2013, 5, 1) not in fetcher.dates
    assert min(fetcher.dates) == datetime.date(2013, 4, 1)
    assert max(fetcher.dates) == datetime.date(2013, 4, 30)
    assert "2013-03-31" not in res["fetched_dates"]
    assert "2013-05-01" not in res["fetched_dates"]


# 2/9. Reconciliation happens BEFORE any daily fetch (missing entry -> no fetch).

def test_wired_reconciliation_before_fetch(monkeypatch, tmp_path):
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    # Drop one expected file from md5sums -> reconcile must fail before any fetch.
    import datetime
    drop_fn = fetch_path.expected_source_filename(datetime.date(2013, 4, 15))
    md5map = fetch_path.parse_md5sums(md5_b.decode())
    lines = [ln for ln in md5_b.decode().splitlines() if drop_fn not in ln]
    md5_b2 = ("\n".join(lines) + "\n").encode()
    fetcher = RecordingFetcher(payloads)
    with pytest.raises(fetch_path.IntegrityManifestError):
        _run_april(monkeypatch, tmp_path, payloads=payloads, fetcher=fetcher,
                   md5_b=md5_b2, size_b=size_b)
    assert fetcher.dates == [], "no daily file may be fetched before reconciliation passes"


# 3 & 4. Missing md5sums / filesizes entry fails closed before archive write.

def test_wired_missing_md5_entry_fails_closed(monkeypatch, tmp_path):
    import datetime
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    drop_fn = fetch_path.expected_source_filename(datetime.date(2013, 4, 10))
    md5_b2 = ("\n".join(ln for ln in md5_b.decode().splitlines() if drop_fn not in ln) + "\n").encode()
    with pytest.raises(fetch_path.IntegrityManifestError):
        _run_april(monkeypatch, tmp_path, payloads=payloads, md5_b=md5_b2, size_b=size_b)
    assert not (tmp_path / "out" / "ttg_approved_fields_archive.csv").exists()


def test_wired_missing_filesizes_entry_fails_closed(monkeypatch, tmp_path):
    import datetime
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    drop_fn = fetch_path.expected_source_filename(datetime.date(2013, 4, 10))
    size_b2 = ("\n".join(ln for ln in size_b.decode().splitlines() if drop_fn not in ln) + "\n").encode()
    with pytest.raises(fetch_path.IntegrityManifestError):
        _run_april(monkeypatch, tmp_path, payloads=payloads, md5_b=md5_b, size_b=size_b2)
    assert not (tmp_path / "out" / "ttg_approved_fields_archive.csv").exists()


# 5 & 6. MD5 mismatch / byte-size mismatch fails closed before archive write.

def test_wired_md5_mismatch_fails_closed(monkeypatch, tmp_path):
    import datetime, hashlib as _h
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    bad_fn = fetch_path.expected_source_filename(datetime.date(2013, 4, 12))
    # Corrupt the md5 for one file (reconcile still passes; per-file verify fails).
    lines = []
    for ln in md5_b.decode().splitlines():
        if bad_fn in ln:
            lines.append("{}  {}".format("0" * 32, bad_fn))
        else:
            lines.append(ln)
    md5_b2 = ("\n".join(lines) + "\n").encode()
    with pytest.raises(fetch_path.IntegrityVerificationError):
        _run_april(monkeypatch, tmp_path, payloads=payloads, md5_b=md5_b2, size_b=size_b)
    assert not (tmp_path / "out" / "ttg_approved_fields_archive.csv").exists()


def test_wired_size_mismatch_fails_closed(monkeypatch, tmp_path):
    import datetime
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    bad_fn = fetch_path.expected_source_filename(datetime.date(2013, 4, 12))
    lines = []
    for ln in size_b.decode().splitlines():
        if bad_fn in ln:
            lines.append("{} {}".format(999999, bad_fn))
        else:
            lines.append(ln)
    size_b2 = ("\n".join(lines) + "\n").encode()
    with pytest.raises(fetch_path.IntegrityVerificationError):
        _run_april(monkeypatch, tmp_path, payloads=payloads, md5_b=md5_b, size_b=size_b2)
    assert not (tmp_path / "out" / "ttg_approved_fields_archive.csv").exists()


# 7. Unstable retry fails closed before archive write.

def test_wired_unstable_retry_fails_closed(monkeypatch, tmp_path):
    import datetime
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    flaky_date = datetime.date(2013, 4, 5)
    calls = {"n": 0}

    def _flaky(source_file_date, url):
        if source_file_date == flaky_date:
            calls["n"] += 1
            # Return different bytes on the 2nd attempt -> unstable.
            return payloads[source_file_date] if calls["n"] == 1 else payloads[source_file_date] + b"X"
        return payloads[source_file_date]

    with pytest.raises(fetch_path.UnstableDownloadError):
        _run_april(monkeypatch, tmp_path, payloads=payloads, fetcher=_flaky,
                   md5_b=md5_b, size_b=size_b, fetch_attempts=2)
    assert not (tmp_path / "out" / "ttg_approved_fields_archive.csv").exists()


# 8 & 11. Cache hit re-verified before use; mixed cache/fetch records provenance.

def test_wired_all_from_verified_cache(monkeypatch, tmp_path):
    import datetime
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    for d in _april_dates():
        (cache_dir / fetch_path.expected_source_filename(d)).write_bytes(payloads[d])

    # A fetcher that errors if called — proves all bytes came from cache.
    def _never(source_file_date, url):
        raise AssertionError("fetch must not be called when cache is complete")

    res, _ = _run_april(monkeypatch, tmp_path, payloads=payloads, fetcher=_never,
                        cache_dir=str(cache_dir), md5_b=md5_b, size_b=size_b)
    sources = {pf["integrity"]["source"] for pf in res["manifest"]["per_file_provenance"]}
    assert sources == {"cache"}
    assert res["primary_covered_sqldates"] == ["2013-04-{:02d}".format(d) for d in range(2, 30)]


def test_wired_mixed_cache_and_fetch_records_provenance(monkeypatch, tmp_path):
    import datetime
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    # Cache only the even days; odd days are fetched.
    cached_dates = [d for d in _april_dates() if d.day % 2 == 0]
    for d in cached_dates:
        (cache_dir / fetch_path.expected_source_filename(d)).write_bytes(payloads[d])
    fetcher = RecordingFetcher(payloads)
    res, _ = _run_april(monkeypatch, tmp_path, payloads=payloads, fetcher=fetcher,
                        cache_dir=str(cache_dir), md5_b=md5_b, size_b=size_b)
    sources = {pf["source_file_date"]: pf["integrity"]["source"]
               for pf in res["manifest"]["per_file_provenance"]}
    assert sources["2013-04-02"] == "cache"
    assert sources["2013-04-03"] == "fetch"
    # Only odd (uncached) days were fetched.
    assert all(d.day % 2 == 1 for d in fetcher.dates)
    # Provenance is structural-only for every file.
    for pf in res["manifest"]["per_file_provenance"]:
        assert pf["integrity"]["integrity_status"] == "verified"
        assert pf["integrity"]["md5_ok"] is True and pf["integrity"]["size_ok"] is True


# 9. Cache cannot bypass manifest reconciliation.

def test_wired_cache_cannot_bypass_reconciliation(monkeypatch, tmp_path):
    import datetime
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    for d in _april_dates():
        (cache_dir / fetch_path.expected_source_filename(d)).write_bytes(payloads[d])
    # Even with a complete cache, a missing manifest entry fails closed first.
    drop_fn = fetch_path.expected_source_filename(datetime.date(2013, 4, 20))
    md5_b2 = ("\n".join(ln for ln in md5_b.decode().splitlines() if drop_fn not in ln) + "\n").encode()
    with pytest.raises(fetch_path.IntegrityManifestError):
        _run_april(monkeypatch, tmp_path, payloads=payloads, fetcher=lambda d, u: payloads[d],
                   cache_dir=str(cache_dir), md5_b=md5_b2, size_b=size_b)


# 10. Cache integrity failure fails closed without silent re-download.

def test_wired_cache_integrity_failure_no_silent_redownload(monkeypatch, tmp_path):
    import datetime
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    for d in _april_dates():
        (cache_dir / fetch_path.expected_source_filename(d)).write_bytes(payloads[d])
    # Corrupt ONE cached file.
    bad_d = datetime.date(2013, 4, 14)
    (cache_dir / fetch_path.expected_source_filename(bad_d)).write_bytes(b"CORRUPT")
    fetched = []

    def _record(source_file_date, url):
        fetched.append(source_file_date)
        return payloads[source_file_date]

    with pytest.raises(fetch_path.CacheIntegrityError):
        _run_april(monkeypatch, tmp_path, payloads=payloads, fetcher=_record,
                   cache_dir=str(cache_dir), md5_b=md5_b, size_b=size_b)
    # No silent re-download of the corrupt cached file.
    assert bad_d not in fetched


# 12-15. Exact-58 enforcement is invoked BY the orchestration.

@pytest.mark.parametrize("ncols", [35, 45, 59])
def test_wired_exact58_enforced_in_orchestration(monkeypatch, tmp_path, ncols):
    import datetime
    g = _guarded(monkeypatch)
    d = datetime.date(2013, 4, 10)
    # A single wrong-width row for this file's payload.
    payload = ("\n".join([_make_row_ncols(ncols, sqldate="20130410")]) + "\n").encode()
    fn = fetch_path.expected_source_filename(d)
    md5_b, size_b = _mk_manifests({fn: payload})  # whole-file integrity passes
    res = fetch_path.run_bounded_integrity_build(
        "2013-04-10", "2013-04-10", out_dir=str(tmp_path / "out"),
        md5sums_bytes=md5_b, filesizes_bytes=size_b,
        fetch_callable=lambda dd, u: payload, **g,
    )
    pf = res["manifest"]["per_file_provenance"][0]
    # Integrity passed (whole-file), but the wrong-width row failed exact-58.
    assert pf["integrity"]["integrity_status"] == "verified"
    assert pf["dropped_by_reason"]["column_count_mismatch"] == 1
    assert pf["retained_row_count"] == 0
    # Nothing wrong-width reached the archive.
    assert res["primary_covered_sqldates"] == []


# 21-23. Generated manifest/report data structural-only, value-agnostic.

def test_wired_manifest_structural_and_value_agnostic(monkeypatch, tmp_path):
    res, _ = _run_april(monkeypatch, tmp_path)
    manifest = res["manifest"]
    # No value-summary / value-bucket KEYS anywhere. (The approved field NAMES
    # may appear as schema name/type values — that is the schema, not a value
    # summary — so we scan KEYS, not values.)
    keys = _all_keys(manifest)
    for bad in ("quadclass", "goldsteinscale", "nummentions", "avgtone",
                "by_value", "by_tone", "by_sign", "_bucket", "bucketed", "sample",
                "mean", "median", "histogram", "distribution", "value_counts"):
        for k in keys:
            assert bad not in k.lower(), (k, bad)
    assert "rows" not in keys
    # Wired structural markers present.
    assert manifest["wired_orchestrator"] == "run_bounded_integrity_build"
    assert manifest["boundary_declarations"]["single_real_network_entrypoint"] is True
    assert manifest["boundary_declarations"]["integrity_checked_before_archive_write"] is True
    assert manifest["boundary_declarations"]["slice_aware_coverage_applied"] is True


# 24. No 2023+ enumeration/open path exists (wired path).

def test_wired_no_2023plus_enumeration(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    spy = FetchSpy()
    with pytest.raises(archive.Post2022SealBreach):
        fetch_path.run_bounded_integrity_build(
            "2022-12-30", "2023-01-02", out_dir=str(tmp_path / "out"),
            md5sums_bytes=md5_b, filesizes_bytes=size_b,
            fetch_callable=spy, **g,
        )
    assert spy.calls == [], "no fetch after a 2023+ enumeration breach"


# 25. No real network contact occurs in tests (default reaches the real gate).

def test_wired_default_fetch_is_real_gated(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    # No injected fetcher, no cache: the default per-file source is the real
    # gated fetch, which hard-errors (proving the default IS the real entrypoint
    # and that no test performs real network contact).
    with pytest.raises(fetch_path.RealFetchNotAuthorized):
        fetch_path.run_bounded_integrity_build(
            "2013-04-01", "2013-04-30", out_dir=str(tmp_path / "out"),
            md5sums_bytes=md5_b, filesizes_bytes=size_b,
            fetch_callable=None, cache_dir=None, **g,
        )


# 26 & 27. Single real/default entrypoint; bare harness cannot reach _open_url.

def test_bare_harness_refuses_default_and_real_fetch(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    # Default (None) -> fail closed (no fall-back to real fetch).
    with pytest.raises(fetch_path.SyntheticOrchestratorViolation):
        fetch_path.run_phase2_archive_build(["2014-06-10"], out_dir="UNUSED", **g)
    # Real-network entrypoints rejected as the fetcher.
    for real_fn in (fetch_path.fetch_one_source_file, fetch_path.fetch_stable,
                    fetch_path._open_url):
        with pytest.raises(fetch_path.SyntheticOrchestratorViolation):
            fetch_path.run_phase2_archive_build(
                ["2014-06-10"], out_dir="UNUSED", fetch_callable=real_fn, **g)


def test_bare_harness_synthetic_fetcher_never_opens_url(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    spy = FetchSpy()
    # A synthetic spy is accepted; it is the ONLY way the bare harness fetches,
    # and a spy never reaches _open_url.
    with pytest.raises(archive.Post2022SealBreach):
        fetch_path.run_phase2_archive_build(
            ["2023-01-01"], out_dir="UNUSED", fetch_callable=spy, **g)
    assert spy.calls == []


# 28. Injected-fetcher seam cannot bypass integrity in the wired path.

def test_wired_injected_fetcher_cannot_bypass_integrity(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    payloads = _april_payloads()
    md5_b, size_b = _manifests_for(payloads)
    # An injected fetcher that returns CORRUPT bytes (not matching the official
    # manifest) must still be caught by verify_file_integrity in the wired path.
    def _corrupt(source_file_date, url):
        return b"CORRUPT-bytes-not-matching-manifest"

    with pytest.raises(fetch_path.IntegrityVerificationError):
        fetch_path.run_bounded_integrity_build(
            "2013-04-01", "2013-04-30", out_dir=str(tmp_path / "out"),
            md5sums_bytes=md5_b, filesizes_bytes=size_b,
            fetch_callable=_corrupt, **g,
        )
    assert not (tmp_path / "out" / "ttg_approved_fields_archive.csv").exists()


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
