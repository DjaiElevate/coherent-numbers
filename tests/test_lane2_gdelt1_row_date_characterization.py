"""Conformance tests for the Lane 2 GDELT 1.0 row-date characterization
runner.

Synthetic fixtures and fake openers only. NO real network. NO real GDELT
data. NO market data. NO 2023+. The runner under test ships inert;
tests either monkeypatch guards or invoke pure helpers that don't reach
the network path.
"""

import importlib.util
import inspect
import io
import json
import os
import pathlib
import re
import urllib.error
import urllib.request
import zipfile
from datetime import date

import pytest


# ── Module loader ────────────────────────────────────────────────────────────

def _load_runner():
    path = os.path.join(
        os.path.dirname(__file__), "..", "scripts",
        "run_lane2_gdelt1_row_date_characterization.py",
    )
    spec = importlib.util.spec_from_file_location(
        "l2_row_date_char", path,
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── Synthetic fixtures ───────────────────────────────────────────────────────

LOCKED_DATES = [
    "2013-09-07", "2014-02-16", "2014-07-26", "2014-12-31",
    "2015-10-02", "2016-07-02", "2017-04-02", "2017-12-31",
    "2018-10-02", "2019-07-03", "2020-04-02", "2020-12-31",
    "2021-07-02", "2022-01-01", "2022-07-02", "2022-12-30",
]

LOCKED_URLS = [
    "http://data.gdeltproject.org/events/{}.export.CSV.zip".format(
        d.replace("-", "")
    )
    for d in LOCKED_DATES
]

KNOWN_GAPS = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
PROBE_POSITIVES = [
    "2013-04-01", "2014-01-22", "2014-01-26", "2018-02-14", "2022-12-31",
]


def _good_recognized_units():
    """Recognized list with all 16 characterization dates present plus
    representative probe-positive dates (which are present in the real
    capture but excluded by the characterization sample), and which
    explicitly omits the four known substrate gaps."""
    return sorted(set(
        LOCKED_DATES
        + PROBE_POSITIVES
        + ["2013-04-02", "2020-06-15", "2005", "2006-01"]
    ))


def _make_payload_zip(nominal_date, offset_buckets):
    """Build a synthetic GDELT-shaped .zip payload with row counts per
    offset bucket.

    `offset_buckets` is a list of `(offset_days, count)` tuples. Each
    tuple contributes `count` rows whose SQLDATE column is
    `nominal_date + offset_days`.
    """
    from datetime import timedelta
    rows = []
    row_id = 0
    yyyymmdd_nominal = nominal_date.strftime("%Y%m%d")
    for offset, count in offset_buckets:
        actual = nominal_date + timedelta(days=offset)
        actual_str = actual.strftime("%Y%m%d")
        for _ in range(count):
            row_id += 1
            rows.append("{}\t{}\tA".format(row_id, actual_str))
    tsv = "\n".join(rows)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("{}.export.CSV".format(yyyymmdd_nominal), tsv)
    return buf.getvalue()


class _FakeResponse:
    def __init__(self, status=200, body=b"", headers=None):
        self._status = status
        self._body = body
        self.headers = headers or {}

    def getcode(self):
        return self._status

    def read(self):
        return self._body

    def close(self):
        pass


def _expected_offset_buckets():
    """Synthetic offset buckets that mirror the real lookback taxonomy
    `{0, -1, -7, -30, -365, -3650, +1}` in modest counts."""
    return [
        (-3650, 4),
        (-365, 30),
        (-30, 15),
        (-7, 25),
        (-1, 20),
        (0, 500),
        (1, 5),
    ]


def _expected_offset_buckets_no_tplus1():
    return [
        (-3650, 4),
        (-365, 30),
        (-30, 15),
        (-7, 25),
        (-1, 20),
        (0, 500),
    ]


def _make_feasible_opener_all_taxonomy_stable_with_tplus1_boundary():
    """Fake opener: all 16 dates return HTTP 200 with payloads that
    have T+1 in early files (2013-09-07 → 2014-12-31) and no T+1 in
    later files (2015+ → 2022)."""
    payloads = {}
    for d_iso in LOCKED_DATES:
        d = date.fromisoformat(d_iso)
        if d.year <= 2014:
            buckets = _expected_offset_buckets()
        else:
            buckets = _expected_offset_buckets_no_tplus1()
        payloads[d_iso.replace("-", "")] = _make_payload_zip(d, buckets)

    def fake_opener(url, timeout=30.0):
        m = re.search(r"/events/(\d{8})\.export\.CSV\.zip$", url)
        assert m, "unexpected URL: {}".format(url)
        yyyymmdd = m.group(1)
        if yyyymmdd in payloads:
            return _FakeResponse(status=200, body=payloads[yyyymmdd])
        raise urllib.error.HTTPError(
            url, 404, "Not Found (unexpected)", {}, None,
        )

    return fake_opener


# ── 1. Guard discipline ──────────────────────────────────────────────────────

def test_default_module_constant_is_false():
    m = _load_runner()
    assert m.ROW_DATE_CHARACTERIZATION_AUTHORIZED is False


def test_guards_refuse_default(monkeypatch):
    m = _load_runner()
    monkeypatch.delenv(
        "LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED", raising=False,
    )
    assert m._guards_ok(True) is False
    with pytest.raises(SystemExit):
        m.run_row_date_characterization(os.getcwd())


def test_guards_refuse_missing_env(monkeypatch):
    m = _load_runner()
    monkeypatch.setattr(m, "ROW_DATE_CHARACTERIZATION_AUTHORIZED", True)
    monkeypatch.delenv(
        "LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED", raising=False,
    )
    assert m._guards_ok(True) is False
    with pytest.raises(SystemExit):
        m.run_row_date_characterization(os.getcwd())


def test_guards_refuse_missing_cli_flag(monkeypatch):
    m = _load_runner()
    monkeypatch.setattr(m, "ROW_DATE_CHARACTERIZATION_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED", "1")
    assert m._guards_ok(False) is False


def test_guards_refuse_missing_module_constant(monkeypatch):
    m = _load_runner()
    monkeypatch.setenv("LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED", "1")
    # ROW_DATE_CHARACTERIZATION_AUTHORIZED ships False; do not flip.
    assert m._guards_ok(True) is False


def test_guards_pass_with_all_three(monkeypatch):
    m = _load_runner()
    monkeypatch.setattr(m, "ROW_DATE_CHARACTERIZATION_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED", "1")
    assert m._guards_ok(True) is True


def test_accidental_invocation_refuses_before_network(monkeypatch):
    """Invoking the runner without all three guards must refuse before
    any opener is constructed, any directory is created, or any network
    call is attempted."""
    m = _load_runner()
    monkeypatch.delenv(
        "LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED", raising=False,
    )
    builds = []
    opens = []

    def _spy_build(*a, **kw):
        builds.append((a, kw))
        return None

    def _spy_urlopen(*a, **kw):
        opens.append((a, kw))
        return None

    monkeypatch.setattr(
        m, "_build_row_date_redirect_disabled_opener", _spy_build,
    )
    monkeypatch.setattr(urllib.request, "urlopen", _spy_urlopen)

    with pytest.raises(SystemExit):
        m.run_row_date_characterization(os.getcwd())
    assert builds == []
    assert opens == []


# ── 2. Hardcoded dates ───────────────────────────────────────────────────────

def test_characterization_dates_exactly_match_a2a8fd5():
    m = _load_runner()
    iso_dates = [d.isoformat() for d in m.CHARACTERIZATION_DATES]
    assert iso_dates == LOCKED_DATES
    assert len(iso_dates) == 16


def test_characterization_dates_no_duplicates():
    m = _load_runner()
    iso_dates = [d.isoformat() for d in m.CHARACTERIZATION_DATES]
    assert len(set(iso_dates)) == 16


def test_characterization_dates_no_known_substrate_gap_overlap():
    m = _load_runner()
    iso_dates = set(d.isoformat() for d in m.CHARACTERIZATION_DATES)
    for gap in KNOWN_GAPS:
        assert gap not in iso_dates


def test_characterization_dates_no_already_sampled_probe_overlap():
    m = _load_runner()
    iso_dates = set(d.isoformat() for d in m.CHARACTERIZATION_DATES)
    for d in PROBE_POSITIVES:
        assert d not in iso_dates


def test_characterization_dates_no_2023_plus():
    m = _load_runner()
    seal = date(2023, 1, 1)
    for d in m.CHARACTERIZATION_DATES:
        assert d < seal


# ── 3. URL construction ──────────────────────────────────────────────────────

def test_construct_urls_exactly_sixteen():
    m = _load_runner()
    urls = m.construct_characterization_urls()
    assert len(urls) == 16


def test_construct_urls_match_a2a8fd5():
    m = _load_runner()
    urls = m.construct_characterization_urls()
    assert urls == LOCKED_URLS


def test_construct_urls_no_index_listing_url():
    m = _load_runner()
    urls = m.construct_characterization_urls()
    for u in urls:
        assert "index.html" not in u
        assert u != m.EVENT_FILE_BASE_URL
        assert u.endswith(".export.CSV.zip")
        assert "?" not in u


def test_construct_urls_module_constant_matches_function():
    m = _load_runner()
    urls = m.construct_characterization_urls()
    assert list(m.CHARACTERIZATION_URLS) == urls


# ── 4. Recognized-list parser tests ──────────────────────────────────────────

def _write_fixture_capture(tmp_path, payload):
    m = _load_runner()
    rel = m.RECOGNIZED_LIST_PATH
    full = pathlib.Path(tmp_path) / rel
    full.parent.mkdir(parents=True, exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        json.dump(payload, fh)
    return full


def test_load_recognized_units_parses_fixture(tmp_path):
    m = _load_runner()
    units = LOCKED_DATES + PROBE_POSITIVES + ["2005", "2006-01"]
    _write_fixture_capture(tmp_path, {
        "schema_version": "v0.1",
        "recognized_in_window_count": len(units),
        "recognized_in_window_units": units,
    })
    out = m._load_recognized_units(str(tmp_path))
    assert out == units


def test_load_recognized_units_raises_on_missing_key(tmp_path):
    m = _load_runner()
    _write_fixture_capture(tmp_path, {"schema_version": "v0.1"})
    with pytest.raises(m.CharacterizationBoundaryBreach):
        m._load_recognized_units(str(tmp_path))


@pytest.mark.parametrize("malformed", [
    {}, {"2013-09-07": True}, "2013-09-07", 42, None,
])
def test_load_recognized_units_raises_on_non_list(tmp_path, malformed):
    m = _load_runner()
    _write_fixture_capture(tmp_path, {
        "recognized_in_window_units": malformed,
    })
    with pytest.raises(m.CharacterizationBoundaryBreach):
        m._load_recognized_units(str(tmp_path))


def test_real_committed_capture_contains_all_16_dates():
    """Read-only smoke test against the real tracked §10 capture.

    Confirms: real capture parses cleanly; all 16 characterization
    dates are present in `recognized_in_window_units`; the four known
    substrate gaps are absent; the five already-sampled probe positive
    dates are present (because the characterization sample explicitly
    excludes them, not because the capture omits them).
    """
    m = _load_runner()
    repo_root = str(pathlib.Path(__file__).resolve().parents[1])
    units = m._load_recognized_units(repo_root)
    assert isinstance(units, list)
    assert len(units) == 3647
    for d in LOCKED_DATES:
        assert d in units, "characterization date missing: {}".format(d)
    for gap in KNOWN_GAPS:
        assert gap not in units, "known gap unexpectedly present: {}".format(gap)
    for p in PROBE_POSITIVES:
        assert p in units, (
            "already-sampled probe positive missing from real capture: "
            "{}".format(p)
        )


def test_validate_characterization_sample_passes_good_units():
    m = _load_runner()
    units = LOCKED_DATES + PROBE_POSITIVES + ["2013-04-02", "2005"]
    m.validate_characterization_sample(units)  # must not raise


def test_validate_characterization_sample_raises_on_missing_date():
    m = _load_runner()
    units = [d for d in LOCKED_DATES if d != "2018-10-02"]
    with pytest.raises(m.SampleValidationError):
        m.validate_characterization_sample(units)


def test_validate_characterization_sample_real_capture():
    """The real committed capture must pass the substrate validator."""
    m = _load_runner()
    repo_root = str(pathlib.Path(__file__).resolve().parents[1])
    units = m._load_recognized_units(repo_root)
    m.validate_characterization_sample(units)  # must not raise


# ── 5. Redirect-disabled opener tests ────────────────────────────────────────

def test_redirect_handler_subclass():
    m = _load_runner()
    assert issubclass(
        m._RowDateNoFollowRedirectHandler,
        urllib.request.HTTPRedirectHandler,
    )


def test_redirect_handler_blocks_all_3xx():
    m = _load_runner()
    h = m._RowDateNoFollowRedirectHandler()
    for code in (301, 302, 303, 307, 308):
        hook = getattr(h, "http_error_{}".format(code))
        with pytest.raises(m.RedirectBlocked):
            hook(None, None, code, "msg", {})


def test_build_redirect_disabled_opener_returns_callable():
    m = _load_runner()
    opener = m._build_row_date_redirect_disabled_opener()
    assert callable(opener)


def test_default_timeout_is_thirty():
    m = _load_runner()
    assert m.DEFAULT_TIMEOUT == 30.0
    opener = m._build_row_date_redirect_disabled_opener()
    sig = inspect.signature(opener)
    assert sig.parameters["timeout"].default == 30.0


# ── 6. Output allow-list tests ───────────────────────────────────────────────

def _locked_yyyymmdd():
    return [d.replace("-", "") for d in LOCKED_DATES]


def test_allow_list_accepts_metadata_and_summary():
    m = _load_runner()
    lock = _locked_yyyymmdd()
    assert m._is_allowed_characterization_output(
        "characterization_metadata.json", lock,
    )
    assert m._is_allowed_characterization_output(
        "characterization_summary.md", lock,
    )


def test_allow_list_accepts_all_16_locked_payloads():
    m = _load_runner()
    lock = _locked_yyyymmdd()
    for yyyymmdd in lock:
        assert m._is_allowed_characterization_output(
            "payload_{}.zip".format(yyyymmdd), lock,
        )


def test_allow_list_rejects_nonlocked_payload_date():
    m = _load_runner()
    lock = _locked_yyyymmdd()
    # Not one of the 16 locked dates
    assert not m._is_allowed_characterization_output(
        "payload_20130401.zip", lock,  # this is a probe-positive, not locked
    )
    assert not m._is_allowed_characterization_output(
        "payload_20140123.zip", lock,  # known gap
    )


def test_allow_list_rejects_extracted_csv():
    m = _load_runner()
    lock = _locked_yyyymmdd()
    for bad in ("data.csv", "20130907.export.CSV", "payload_20130907.csv"):
        assert not m._is_allowed_characterization_output(bad, lock), bad


def test_allow_list_rejects_arbitrary_filenames():
    m = _load_runner()
    lock = _locked_yyyymmdd()
    for bad in (
        "probe.log", "anything.txt", ".hidden",
        "payload_2013090.zip",  # 7 digits
        "payload_201309077.zip",  # 9 digits
        "payload_abcdefgh.zip",
        "CHARACTERIZATION_METADATA.JSON",  # case-sensitive
    ):
        assert not m._is_allowed_characterization_output(bad, lock), bad


def test_allow_list_rejects_path_traversal():
    m = _load_runner()
    lock = _locked_yyyymmdd()
    for bad in (
        "../escape.json", "../../etc/passwd",
        "subdir/payload_20130907.zip", "..\\windows.txt",
    ):
        assert not m._is_allowed_characterization_output(bad, lock), bad


def test_checked_path_raises_on_disallowed(tmp_path):
    m = _load_runner()
    lock = _locked_yyyymmdd()
    with pytest.raises(m.CharacterizationBoundaryBreach):
        m._checked_characterization_path(str(tmp_path), "bad.csv", lock)


def test_post_hoc_tripwire_catches_disallowed_file(tmp_path):
    m = _load_runner()
    lock = _locked_yyyymmdd()
    bad = tmp_path / "rogue.txt"
    bad.write_text("not allowed")
    with pytest.raises(m.CharacterizationBoundaryBreach):
        m._assert_characterization_outputs_allowed(str(tmp_path), lock)


# ── 7. Parser / metrics tests ────────────────────────────────────────────────

def test_parser_counts_taxonomy_stable_no_tplus1():
    m = _load_runner()
    nominal = date(2020, 4, 2)
    payload = _make_payload_zip(nominal, _expected_offset_buckets_no_tplus1())
    out = m.parse_characterization_payload(payload, nominal_date=nominal)
    assert out["row_count"] == 4 + 30 + 15 + 25 + 20 + 500
    assert out["nominal_row_count"] == 500
    assert out["mismatch_row_count"] == 4 + 30 + 15 + 25 + 20
    presence = out["expected_offsets_presence"]
    assert presence["0"] is True
    assert presence["-1"] is True
    assert presence["-7"] is True
    assert presence["-30"] is True
    assert presence["-365"] is True
    assert presence["-3650"] is True
    assert presence["+1"] is False
    assert out["unexpected_offsets"] == []
    assert out["header_anomaly_detected"] is False
    assert out["unparseable_sqldate_rows"] == 0


def test_parser_counts_taxonomy_stable_with_tplus1():
    m = _load_runner()
    nominal = date(2013, 9, 7)
    payload = _make_payload_zip(nominal, _expected_offset_buckets())
    out = m.parse_characterization_payload(payload, nominal_date=nominal)
    assert out["expected_offsets_presence"]["+1"] is True


def test_parser_detects_unexpected_offset():
    m = _load_runner()
    nominal = date(2020, 4, 2)
    buckets = _expected_offset_buckets_no_tplus1() + [(-100, 7)]  # unexpected
    payload = _make_payload_zip(nominal, buckets)
    out = m.parse_characterization_payload(payload, nominal_date=nominal)
    unexpected = out["unexpected_offsets"]
    assert any(u["offset_days"] == -100 for u in unexpected)


def test_parser_flags_3650_near_miss_as_unexpected():
    """Memo `a2a8fd5` §7 / §10 list the taxonomy as bare integers
    `{0, -1, -7, -30, -365, -3650, +1}` with no tolerance language.
    A near-miss offset like `-3652` (which could plausibly arise from
    10-year leap-year arithmetic) is NOT silently absorbed into the
    -3650 bucket — it surfaces as an unexpected offset, so the
    characterization run can decide whether to revise the taxonomy.
    """
    m = _load_runner()
    nominal = date(2018, 10, 2)
    buckets = _expected_offset_buckets_no_tplus1()
    # Replace the -3650 bucket with -3652
    buckets = [(o, c) if o != -3650 else (-3652, c) for o, c in buckets]
    payload = _make_payload_zip(nominal, buckets)
    out = m.parse_characterization_payload(payload, nominal_date=nominal)
    # -3650 bucket is absent — -3652 does NOT count as -3650.
    assert out["expected_offsets_presence"]["-3650"] is False
    # -3652 surfaces as an unexpected offset.
    unexpected = out["unexpected_offsets"]
    assert any(u["offset_days"] == -3652 for u in unexpected)


def test_parser_flags_various_near_miss_offsets_as_unexpected():
    """Near-miss offsets like -3649, -3651, and -366 are all rejected
    as unexpected — exact integer matching applies to every locked
    offset, not just -3650."""
    m = _load_runner()
    nominal = date(2020, 4, 2)
    # Build a payload with rows at the exact -3650 and -365 buckets,
    # plus off-by-one near-miss buckets that should NOT be absorbed.
    buckets = [
        (0, 100),
        (-1, 10),
        (-365, 20),
        (-366, 3),     # near miss for -365
        (-3650, 5),
        (-3649, 2),    # near miss for -3650
        (-3651, 2),    # near miss for -3650
    ]
    payload = _make_payload_zip(nominal, buckets)
    out = m.parse_characterization_payload(payload, nominal_date=nominal)
    unexpected_offsets = sorted(
        u["offset_days"] for u in out["unexpected_offsets"]
    )
    assert -3651 in unexpected_offsets
    assert -3649 in unexpected_offsets
    assert -366 in unexpected_offsets
    # The exact -3650 and -365 buckets are present and not flagged.
    assert out["expected_offsets_presence"]["-3650"] is True
    assert out["expected_offsets_presence"]["-365"] is True


def test_outcome_classification_triggers_deviation_on_3650_near_miss(monkeypatch, tmp_path):
    """End-to-end: when an otherwise-clean characterization run
    contains a single near-miss offset (here -3652 instead of -3650 in
    one file), the verdict map flips from
    `TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY` to
    `TAXONOMY-DEVIATION-REQUIRES-REVISION`."""
    m = _load_runner()
    monkeypatch.setattr(m, "ROW_DATE_CHARACTERIZATION_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED", "1")
    monkeypatch.setattr(
        m, "_load_recognized_units",
        lambda repo_root: _good_recognized_units(),
    )

    # Build a fake opener that returns the usual stable-with-T+1 payloads
    # for all 16 dates EXCEPT one file (2018-10-02), where the -3650
    # bucket is replaced with a near-miss -3652.
    payloads = {}
    for d_iso in LOCKED_DATES:
        d = date.fromisoformat(d_iso)
        if d.year <= 2014:
            buckets = _expected_offset_buckets()
        else:
            buckets = _expected_offset_buckets_no_tplus1()
        if d_iso == "2018-10-02":
            buckets = [
                (o, c) if o != -3650 else (-3652, c) for o, c in buckets
            ]
        payloads[d_iso.replace("-", "")] = _make_payload_zip(d, buckets)

    def fake_opener(url, timeout=30.0):
        m2 = re.search(r"/events/(\d{8})\.export\.CSV\.zip$", url)
        assert m2, "unexpected URL: {}".format(url)
        yyyymmdd = m2.group(1)
        if yyyymmdd in payloads:
            return _FakeResponse(status=200, body=payloads[yyyymmdd])
        raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)

    out_dir = str(tmp_path / "out")
    m.run_row_date_characterization(
        repo_root=str(tmp_path),
        cli_flag=True,
        opener=fake_opener,
        output_dir=out_dir,
    )
    with open(os.path.join(out_dir, "characterization_metadata.json")) as fh:
        md = json.load(fh)
    assert md["outcome"] == "TAXONOMY-DEVIATION-REQUIRES-REVISION"


def test_parser_detects_header_anomaly():
    m = _load_runner()
    nominal = date(2020, 4, 2)
    # Construct payload with a non-numeric first row
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        rows = ["1\tGLOBALEVENTID\tA", "2\t20200402\tB", "3\t20200402\tC"]
        zf.writestr("20200402.export.CSV", "\n".join(rows))
    out = m.parse_characterization_payload(buf.getvalue(), nominal_date=nominal)
    assert out["header_anomaly_detected"] is True


def test_parser_detects_unparseable_sqldate():
    m = _load_runner()
    nominal = date(2020, 4, 2)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        rows = ["1\t20200402\tA", "2\tnotadate\tB", "3\t20200402\tC"]
        zf.writestr("20200402.export.CSV", "\n".join(rows))
    out = m.parse_characterization_payload(buf.getvalue(), nominal_date=nominal)
    assert out["unparseable_sqldate_rows"] >= 1


def test_parser_detects_malformed_short_row():
    m = _load_runner()
    nominal = date(2020, 4, 2)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        rows = ["1\t20200402\tA", "shortrow", "3\t20200402\tC"]
        zf.writestr("20200402.export.CSV", "\n".join(rows))
    out = m.parse_characterization_payload(buf.getvalue(), nominal_date=nominal)
    assert out["malformed_short_rows"] >= 1


def test_parser_raises_on_2023_plus_sqldate():
    m = _load_runner()
    nominal = date(2022, 12, 30)
    buckets = [(0, 5), (2, 1)]  # 2022-12-30 + 2 days = 2023-01-01
    payload = _make_payload_zip(nominal, buckets)
    with pytest.raises(m.CharacterizationBoundaryBreach):
        m.parse_characterization_payload(payload, nominal_date=nominal)


def test_parser_raises_on_2023_plus_nominal():
    m = _load_runner()
    with pytest.raises(m.CharacterizationBoundaryBreach):
        m.parse_characterization_payload(b"", nominal_date=date(2023, 1, 1))


# ── 8. Aggregate metrics tests ───────────────────────────────────────────────

def test_aggregate_metrics_compute_distribution():
    m = _load_runner()
    fake_results = [
        {
            "nominal_date": "2013-09-07",
            "fetch_outcome": "200_OK",
            "parse": {
                "row_count": 100,
                "offset_distribution": [
                    {"offset_days": 0, "row_count": 80, "percentage_of_file_rows": 80.0},
                    {"offset_days": -1, "row_count": 10, "percentage_of_file_rows": 10.0},
                    {"offset_days": 1, "row_count": 10, "percentage_of_file_rows": 10.0},
                ],
                "expected_offsets_presence": {
                    "0": True, "-1": True, "-7": False, "-30": False,
                    "-365": False, "-3650": False, "+1": True,
                },
                "unexpected_offsets": [],
                "nominal_row_count": 80, "mismatch_row_count": 20,
                "mismatch_percentage": 20.0,
            },
        },
        {
            "nominal_date": "2020-04-02",
            "fetch_outcome": "200_OK",
            "parse": {
                "row_count": 200,
                "offset_distribution": [
                    {"offset_days": 0, "row_count": 180, "percentage_of_file_rows": 90.0},
                    {"offset_days": -1, "row_count": 20, "percentage_of_file_rows": 10.0},
                ],
                "expected_offsets_presence": {
                    "0": True, "-1": True, "-7": False, "-30": False,
                    "-365": False, "-3650": False, "+1": False,
                },
                "unexpected_offsets": [],
                "nominal_row_count": 180, "mismatch_row_count": 20,
                "mismatch_percentage": 10.0,
            },
        },
    ]
    agg = m.aggregate_metrics(fake_results)
    assert agg["offset_file_count"]["0"] == 2
    assert agg["offset_file_count"]["-1"] == 2
    assert agg["offset_file_count"]["1"] == 1  # only the 2013 file
    assert agg["offset_row_total"]["0"] == 80 + 180
    assert agg["mismatch_rate_distribution"]["files"] == 2
    assert agg["mismatch_rate_distribution"]["min"] == 10.0
    assert agg["mismatch_rate_distribution"]["max"] == 20.0
    assert agg["latest_with_tplus1"] == "2013-09-07"
    assert agg["earliest_without_tplus1"] == "2020-04-02"
    assert agg["all_files_conform_to_expected_taxonomy"] is True


def test_aggregate_metrics_flags_unexpected():
    m = _load_runner()
    fake_results = [
        {
            "nominal_date": "2020-04-02",
            "fetch_outcome": "200_OK",
            "parse": {
                "row_count": 100, "offset_distribution": [],
                "expected_offsets_presence": {
                    "0": True, "-1": False, "-7": False, "-30": False,
                    "-365": False, "-3650": False, "+1": False,
                },
                "unexpected_offsets": [{"offset_days": -100, "row_count": 5}],
                "nominal_row_count": 95, "mismatch_row_count": 5,
                "mismatch_percentage": 5.0,
            },
        },
    ]
    agg = m.aggregate_metrics(fake_results)
    assert agg["any_unexpected_offset_observed"] is True
    assert agg["all_files_conform_to_expected_taxonomy"] is False


# ── 9. Outcome classification tests ──────────────────────────────────────────

def _all_clean_no_tplus1_results():
    return [
        {
            "nominal_date": d,
            "fetch_outcome": "200_OK",
            "parse": {
                "row_count": 100,
                "offset_distribution": [
                    {"offset_days": 0, "row_count": 90, "percentage_of_file_rows": 90.0},
                    {"offset_days": -1, "row_count": 10, "percentage_of_file_rows": 10.0},
                ],
                "expected_offsets_presence": {
                    "0": True, "-1": True, "-7": False, "-30": False,
                    "-365": False, "-3650": False, "+1": False,
                },
                "unexpected_offsets": [],
                "header_anomaly_detected": False,
                "unparseable_sqldate_rows": 0,
                "malformed_short_rows": 0,
                "boundary_2023plus_flag": False,
                "nominal_row_count": 90, "mismatch_row_count": 10,
                "mismatch_percentage": 10.0,
            },
        }
        for d in LOCKED_DATES
    ]


def test_outcome_taxonomy_stable_rekey():
    m = _load_runner()
    per_file = _all_clean_no_tplus1_results()
    agg = m.aggregate_metrics(per_file)
    assert m.classify_outcome(per_file, agg) == "TAXONOMY-STABLE-REKEY-BY-SQLDATE"


def test_outcome_taxonomy_stable_with_tplus1_boundary():
    m = _load_runner()
    per_file = _all_clean_no_tplus1_results()
    # Add T+1 to the first 4 files (2013-2014 subwindow A)
    for i in range(4):
        per_file[i]["parse"]["expected_offsets_presence"]["+1"] = True
    agg = m.aggregate_metrics(per_file)
    assert m.classify_outcome(per_file, agg) == "TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY"


def test_outcome_taxonomy_deviation():
    m = _load_runner()
    per_file = _all_clean_no_tplus1_results()
    per_file[5]["parse"]["unexpected_offsets"] = [
        {"offset_days": -100, "row_count": 3}
    ]
    agg = m.aggregate_metrics(per_file)
    assert m.classify_outcome(per_file, agg) == "TAXONOMY-DEVIATION-REQUIRES-REVISION"


def test_outcome_retrieval_or_parser_block_on_404():
    m = _load_runner()
    per_file = _all_clean_no_tplus1_results()
    per_file[3] = {
        "nominal_date": "2014-12-31",
        "fetch_outcome": "HTTP_NON_200",
        "status": 404,
        "parse": None,
    }
    agg = m.aggregate_metrics(per_file)
    assert m.classify_outcome(per_file, agg) == "RETRIEVAL-OR-PARSER-BLOCK"


def test_outcome_retrieval_or_parser_block_on_header_anomaly():
    m = _load_runner()
    per_file = _all_clean_no_tplus1_results()
    per_file[3]["parse"]["header_anomaly_detected"] = True
    agg = m.aggregate_metrics(per_file)
    assert m.classify_outcome(per_file, agg) == "RETRIEVAL-OR-PARSER-BLOCK"


def test_outcome_insufficient_when_tplus1_interleaved():
    m = _load_runner()
    per_file = _all_clean_no_tplus1_results()
    # Interleaved T+1 pattern: T+1 in files 0, 5, 10 (not chronologically clean)
    per_file[0]["parse"]["expected_offsets_presence"]["+1"] = True
    per_file[5]["parse"]["expected_offsets_presence"]["+1"] = True
    per_file[10]["parse"]["expected_offsets_presence"]["+1"] = True
    # files 1-4, 6-9, 11-15 have +1 absent
    agg = m.aggregate_metrics(per_file)
    # latest_with_tplus1 will be index 10 (2020-04-02); earliest_without
    # will be index 1 (2014-02-16). earliest < latest, so boundary order
    # is not satisfied → INSUFFICIENT-CHARACTERIZATION.
    assert m.classify_outcome(per_file, agg) == "INSUFFICIENT-CHARACTERIZATION"


# ── 10. End-to-end fake-opener test (no network) ─────────────────────────────

def test_end_to_end_taxonomy_stable_with_tplus1_boundary(
    monkeypatch, tmp_path,
):
    m = _load_runner()
    monkeypatch.setattr(m, "ROW_DATE_CHARACTERIZATION_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED", "1")
    monkeypatch.setattr(
        m, "_load_recognized_units",
        lambda repo_root: _good_recognized_units(),
    )

    fake_opener = (
        _make_feasible_opener_all_taxonomy_stable_with_tplus1_boundary()
    )
    out_dir = str(tmp_path / "out")
    returned = m.run_row_date_characterization(
        repo_root=str(tmp_path),
        cli_flag=True,
        opener=fake_opener,
        output_dir=out_dir,
    )
    assert returned == out_dir

    # Allowed outputs only.
    names = sorted(os.listdir(out_dir))
    assert "characterization_metadata.json" in names
    assert "characterization_summary.md" in names
    # All 16 HTTP-200 payloads preserved
    expected_payloads = {
        "payload_{}.zip".format(d.replace("-", "")) for d in LOCKED_DATES
    }
    assert expected_payloads.issubset(set(names))
    # No extracted CSV
    assert not any(n.endswith(".CSV") for n in names)
    assert not any(n.endswith(".csv") for n in names)

    with open(os.path.join(out_dir, "characterization_metadata.json")) as fh:
        md = json.load(fh)
    assert md["outcome"] == "TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY"
    assert md["plan_lock_memo_commit"] == "a2a8fd5"
    assert md["characterization_dates"] == LOCKED_DATES
    assert md["characterization_urls"] == LOCKED_URLS
    assert md["no_market_data"] is True
    assert md["no_step_2"] is True
    assert md["no_negative_control"] is True


def test_end_to_end_refuses_when_guards_off(monkeypatch, tmp_path):
    m = _load_runner()
    monkeypatch.delenv(
        "LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED", raising=False,
    )

    def boom(*a, **kw):
        raise AssertionError("opener invoked despite guards being off")

    out_dir = str(tmp_path / "out")
    with pytest.raises(SystemExit):
        m.run_row_date_characterization(
            repo_root=str(tmp_path),
            cli_flag=True,
            opener=boom,
            output_dir=out_dir,
        )
    assert not os.path.exists(out_dir)


# ── 11. No-market / no-Step-2 leakage ────────────────────────────────────────

def test_no_market_or_step2_surface_in_source():
    """The script declares via metadata + comments that market data /
    Step 2 / category filtering are NOT touched. The forbidden list
    therefore must NOT include tokens like `step_2`, `market_data`,
    `spike_threshold`, or bare `theme`/`actor`/`geography`, which appear
    inside the negation declarations themselves. The list below contains
    only identifier-shape tokens that would appear in actual
    implementation logic."""
    m = _load_runner()
    src = open(m.__file__, "r", encoding="utf-8").read().lower()
    forbidden = (
        "compute_return",
        "abnormal_return",
        "vix",
        "sharpe",
        "asset_label",
        "burst_threshold",
        "step2_lock",
    )
    for f in forbidden:
        assert f not in src, (
            "characterization source unexpectedly mentions forbidden "
            "surface {!r}".format(f)
        )


def test_no_market_or_step2_keys_in_end_to_end_metadata(
    monkeypatch, tmp_path,
):
    m = _load_runner()
    monkeypatch.setattr(m, "ROW_DATE_CHARACTERIZATION_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED", "1")
    monkeypatch.setattr(
        m, "_load_recognized_units",
        lambda repo_root: _good_recognized_units(),
    )
    fake_opener = (
        _make_feasible_opener_all_taxonomy_stable_with_tplus1_boundary()
    )
    out_dir = str(tmp_path / "out")
    m.run_row_date_characterization(
        repo_root=str(tmp_path),
        cli_flag=True,
        opener=fake_opener,
        output_dir=out_dir,
    )
    with open(os.path.join(out_dir, "characterization_metadata.json")) as fh:
        md = json.load(fh)
    md_str = json.dumps(md).lower()
    forbidden = (
        "vix",
        "asset_label",
        "compute_return",
        "abnormal_return",
        "burst_threshold",
        "step2_lock",
    )
    for f in forbidden:
        assert f not in md_str, (
            "characterization metadata unexpectedly mentions forbidden "
            "surface {!r}".format(f)
        )
