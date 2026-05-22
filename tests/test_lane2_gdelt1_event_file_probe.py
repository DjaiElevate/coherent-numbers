"""Conformance tests for the Lane 2 GDELT 1.0 event-file probe.

Synthetic fixtures and fake openers only. NO real network. NO real GDELT
data. NO market data. NO 2023+. The probe under test ships inert; tests
either monkeypatch guards or invoke pure helpers that don't reach the
network path.
"""

import importlib.util
import inspect
import io
import json
import os
import re
import urllib.error
import urllib.request
import zipfile
from datetime import date

import pytest


# ── Module loader (mirrors test_lane2_gdelt1_count_feasibility::_load_runner) ─

def _load_probe():
    path = os.path.join(
        os.path.dirname(__file__), "..", "scripts",
        "run_lane2_gdelt1_event_file_probe.py",
    )
    spec = importlib.util.spec_from_file_location("l2_event_probe", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── Synthetic fixtures ───────────────────────────────────────────────────────

def _good_recognized_units():
    """Synthetic recognized list with all required dates present."""
    return [
        "2005",
        "2013-04-01",
        "2014-01-22",
        "2014-01-26",
        "2018-02-14",
        "2018-02-15",
        "2022-12-31",
        # representative extras to make the list non-trivial
        "2013-04-02",
        "2020-06-15",
    ]


def _make_payload_zip(nominal_date, n_rows=3, header_first_row=False):
    """Build a synthetic GDELT-1.0-shaped .zip payload with TSV rows."""
    yyyymmdd = nominal_date.strftime("%Y%m%d")
    rows = []
    if header_first_row:
        rows.append("GLOBALEVENTID\tSQLDATE\tACTOR1NAME")
    for i in range(n_rows):
        rows.append("{}\t{}\tA".format(i + 1, yyyymmdd))
    tsv = "\n".join(rows)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("{}.export.CSV".format(yyyymmdd), tsv)
    return buf.getvalue()


def _make_mismatched_payload_zip(nominal_date, wrong_date, n_rows=3):
    """Payload whose SQLDATE column points to a different date."""
    yyyymmdd_actual = wrong_date.strftime("%Y%m%d")
    yyyymmdd_nominal = nominal_date.strftime("%Y%m%d")
    rows = []
    for i in range(n_rows):
        rows.append("{}\t{}\tA".format(i + 1, yyyymmdd_actual))
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


def _make_feasible_opener():
    """Fake opener: 5 positive 200s + 1 negative 404."""
    positive_dates = [
        date(2013, 4, 1),
        date(2014, 1, 22),
        date(2014, 1, 26),
        date(2018, 2, 14),
        date(2022, 12, 31),
    ]
    payloads = {
        d.strftime("%Y%m%d"): _make_payload_zip(d, n_rows=3)
        for d in positive_dates
    }
    neg_yyyymmdd = "20140123"

    def fake_opener(url, timeout=30.0):
        m = re.search(r"/events/(\d{8})\.export\.CSV\.zip$", url)
        assert m, "unexpected URL: {}".format(url)
        yyyymmdd = m.group(1)
        if yyyymmdd == neg_yyyymmdd:
            raise urllib.error.HTTPError(
                url, 404, "Not Found", {}, None,
            )
        if yyyymmdd in payloads:
            return _FakeResponse(status=200, body=payloads[yyyymmdd])
        raise urllib.error.HTTPError(
            url, 404, "Not Found (unexpected)", {}, None,
        )

    return fake_opener


# ── 1. Module guards ─────────────────────────────────────────────────────────

def test_default_module_constant_is_false():
    p = _load_probe()
    assert p.EVENT_FILE_PROBE_AUTHORIZED is False


def test_guards_refuse_default(monkeypatch):
    p = _load_probe()
    monkeypatch.delenv("LANE2_EVENT_FILE_PROBE_AUTHORIZED", raising=False)
    assert p._guards_ok(True) is False
    with pytest.raises(SystemExit):
        p.run_event_file_probe(os.getcwd())


def test_guards_refuse_missing_env(monkeypatch):
    p = _load_probe()
    monkeypatch.setattr(p, "EVENT_FILE_PROBE_AUTHORIZED", True)
    monkeypatch.delenv("LANE2_EVENT_FILE_PROBE_AUTHORIZED", raising=False)
    assert p._guards_ok(True) is False
    with pytest.raises(SystemExit):
        p.run_event_file_probe(os.getcwd())


def test_guards_refuse_missing_cli_flag(monkeypatch):
    p = _load_probe()
    monkeypatch.setattr(p, "EVENT_FILE_PROBE_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_EVENT_FILE_PROBE_AUTHORIZED", "1")
    assert p._guards_ok(False) is False


def test_guards_refuse_missing_module_constant(monkeypatch):
    p = _load_probe()
    monkeypatch.setenv("LANE2_EVENT_FILE_PROBE_AUTHORIZED", "1")
    # EVENT_FILE_PROBE_AUTHORIZED is False at rest; do not flip.
    assert p._guards_ok(True) is False


def test_guards_pass_with_all_three(monkeypatch):
    p = _load_probe()
    monkeypatch.setattr(p, "EVENT_FILE_PROBE_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_EVENT_FILE_PROBE_AUTHORIZED", "1")
    assert p._guards_ok(True) is True


def test_accidental_invocation_refuses_before_network(monkeypatch):
    """Invoking the script's main() without any of the three guards should
    print the refusal and exit before any opener is constructed or any
    network call is attempted."""
    p = _load_probe()
    monkeypatch.delenv("LANE2_EVENT_FILE_PROBE_AUTHORIZED", raising=False)
    # Spy on _build_probe_redirect_disabled_opener — should never be called.
    builds = []

    def _spy_build(*a, **kw):
        builds.append((a, kw))
        return None

    monkeypatch.setattr(
        p, "_build_probe_redirect_disabled_opener", _spy_build,
    )
    # Spy on the urllib opener entry too, in case anything bypasses the
    # local builder.
    opens = []

    def _spy_urlopen(*a, **kw):
        opens.append((a, kw))
        return None

    monkeypatch.setattr(urllib.request, "urlopen", _spy_urlopen)

    with pytest.raises(SystemExit):
        p.run_event_file_probe(os.getcwd())
    assert builds == []
    assert opens == []


# ── 2. Recognized-list path discipline ───────────────────────────────────────

def test_recognized_list_path_is_substrate_pinned():
    p = _load_probe()
    assert p.RECOGNIZED_LIST_PATH == (
        "results/lane2_gdelt1_turn_b_recognized_list_capture/"
        "20260521T124853Z/recognized_list.json"
    )


def test_no_cli_env_or_function_override_for_recognized_list_path():
    """No CLI flag, no environment variable, and no function parameter
    permits overriding the substrate-pinned recognized-list path."""
    p = _load_probe()

    # run_event_file_probe's signature: no recognized-list parameter.
    sig = inspect.signature(p.run_event_file_probe)
    forbidden_param_substrings = (
        "recognized", "capture_path", "capture_dir", "list_path",
    )
    for name in sig.parameters:
        for f in forbidden_param_substrings:
            assert f not in name.lower(), (
                "run_event_file_probe exposes forbidden param "
                "containing {!r}: {!r}".format(f, name)
            )

    # _load_recognized_units's signature: only repo_root.
    sig2 = inspect.signature(p._load_recognized_units)
    assert list(sig2.parameters) == ["repo_root"], (
        "_load_recognized_units signature must be (repo_root,) only; "
        "got: {}".format(list(sig2.parameters))
    )

    # Source-level check: no add_argument anywhere references the
    # recognized-list path; no os.environ.get for a recognized-list env
    # var.
    src = open(p.__file__, "r", encoding="utf-8").read()
    forbidden_src_substrings = (
        "--recognized-list",
        "--capture-path",
        "LANE2_RECOGNIZED_LIST",
        "RECOGNIZED_LIST_OVERRIDE",
    )
    for f in forbidden_src_substrings:
        assert f not in src, (
            "probe source unexpectedly references override surface {!r}"
            .format(f)
        )


# ── 3. Sample selection logic ────────────────────────────────────────────────

def test_select_sample_primary_path():
    p = _load_probe()
    units = _good_recognized_units()
    positive, neg = p.select_sample(units)
    assert neg == date(2014, 1, 23)
    assert date(2018, 2, 14) in positive
    assert date(2018, 2, 15) not in positive
    assert positive == sorted(positive)
    assert len(positive) == 5


def test_select_sample_fallback_when_lower_median_absent():
    p = _load_probe()
    units = [u for u in _good_recognized_units() if u != "2018-02-14"]
    positive, neg = p.select_sample(units)
    assert date(2018, 2, 14) not in positive
    assert date(2018, 2, 15) in positive
    assert len(positive) == 5


def test_select_sample_halts_when_both_mid_candidates_absent():
    p = _load_probe()
    units = [
        u for u in _good_recognized_units()
        if u not in ("2018-02-14", "2018-02-15")
    ]
    with pytest.raises(p.SampleSelectionError):
        p.select_sample(units)


def test_select_sample_halts_when_pinned_positive_absent():
    p = _load_probe()
    # Drop the first daily-regime unit; no fallback.
    units = [u for u in _good_recognized_units() if u != "2013-04-01"]
    with pytest.raises(p.SampleSelectionError):
        p.select_sample(units)


def test_select_sample_halts_when_negative_control_present():
    p = _load_probe()
    units = _good_recognized_units() + ["2014-01-23"]
    with pytest.raises(p.SampleSelectionError):
        p.select_sample(units)


def test_pinned_constants_match_design_note():
    p = _load_probe()
    assert p.PINNED_POSITIVE_DATES == (
        date(2013, 4, 1),
        date(2014, 1, 22),
        date(2014, 1, 26),
        date(2022, 12, 31),
    )
    assert p.MID_WINDOW_PRIMARY == date(2018, 2, 14)
    assert p.MID_WINDOW_FALLBACK == date(2018, 2, 15)
    assert p.NEGATIVE_CONTROL_DATE == date(2014, 1, 23)


# ── 4. URL construction ──────────────────────────────────────────────────────

def test_construct_probe_urls_returns_exactly_six():
    p = _load_probe()
    positive, neg = p.select_sample(_good_recognized_units())
    urls = p.construct_probe_urls(positive, neg)
    assert len(urls) == 6


def test_construct_probe_urls_pattern():
    p = _load_probe()
    positive, neg = p.select_sample(_good_recognized_units())
    urls = p.construct_probe_urls(positive, neg)
    pattern = re.compile(
        r"^http://data\.gdeltproject\.org/events/(\d{8})\.export\.CSV\.zip$"
    )
    for date_iso, url in urls.items():
        m = pattern.match(url)
        assert m, "URL does not match event-file pattern: {}".format(url)
        expected_yyyymmdd = date_iso.replace("-", "")
        assert m.group(1) == expected_yyyymmdd


def test_construct_probe_urls_contains_no_index_or_listing_url():
    p = _load_probe()
    positive, neg = p.select_sample(_good_recognized_units())
    urls = p.construct_probe_urls(positive, neg)
    for url in urls.values():
        assert "index.html" not in url
        assert url != p.EVENT_FILE_BASE_URL
        assert "?" not in url  # no query string
        assert url.endswith(".export.CSV.zip")


def test_date_to_url_refuses_2023_plus():
    p = _load_probe()
    with pytest.raises(p.ProbeBoundaryBreach):
        p._date_to_url(date(2023, 1, 1))
    with pytest.raises(p.ProbeBoundaryBreach):
        p._date_to_url(date(2026, 5, 22))


# ── 5. Redirect-disabled opener ──────────────────────────────────────────────

def test_redirect_handler_blocks_all_3xx():
    p = _load_probe()
    h = p._ProbeNoFollowRedirectHandler()
    for code in (301, 302, 303, 307, 308):
        hook = getattr(h, "http_error_{}".format(code))
        with pytest.raises(p.RedirectBlocked):
            hook(None, None, code, "msg", {})


def test_redirect_handler_subclasses_urllib_handler():
    p = _load_probe()
    assert issubclass(
        p._ProbeNoFollowRedirectHandler,
        urllib.request.HTTPRedirectHandler,
    )


def test_build_probe_redirect_disabled_opener_returns_callable():
    p = _load_probe()
    opener = p._build_probe_redirect_disabled_opener()
    assert callable(opener)
    # Calling it would fire a network request; do not invoke here.


def test_probe_opener_default_timeout_is_thirty():
    p = _load_probe()
    assert p.DEFAULT_TIMEOUT == 30.0
    # Confirm the factory's default also resolves to 30.
    opener = p._build_probe_redirect_disabled_opener()
    sig = inspect.signature(opener)
    assert sig.parameters["timeout"].default == 30.0


# ── 6. Output allow-list ─────────────────────────────────────────────────────

def test_allowed_outputs_constant():
    p = _load_probe()
    assert "probe_metadata.json" in p.ALLOWED_PROBE_OUTPUTS
    assert "probe_summary.md" in p.ALLOWED_PROBE_OUTPUTS


def test_allow_list_accepts_metadata_and_summary():
    p = _load_probe()
    pos = ["20130401", "20140122", "20140126", "20180214", "20221231"]
    assert p._is_allowed_probe_output("probe_metadata.json", pos)
    assert p._is_allowed_probe_output("probe_summary.md", pos)


def test_allow_list_accepts_positive_payload_only():
    p = _load_probe()
    pos = ["20130401", "20140122", "20140126", "20180214", "20221231"]
    for d in pos:
        assert p._is_allowed_probe_output(
            "payload_{}.zip".format(d), pos
        )
    # negative-control payload is NOT allowed
    assert not p._is_allowed_probe_output("payload_20140123.zip", pos)


def test_allow_list_rejects_extracted_csv():
    p = _load_probe()
    pos = ["20130401"]
    assert not p._is_allowed_probe_output("data.csv", pos)
    assert not p._is_allowed_probe_output("20130401.export.CSV", pos)
    assert not p._is_allowed_probe_output("payload_20130401.csv", pos)


def test_allow_list_rejects_arbitrary_files():
    p = _load_probe()
    pos = ["20130401"]
    for bad in (
        "probe.log",
        "anything.txt",
        ".hidden",
        "../escape.json",
        "payload_2013040.zip",   # 7 digits
        "payload_201304015.zip",  # 9 digits
        "payload_abcdefgh.zip",
        "PROBE_METADATA.JSON",   # case-sensitive
    ):
        assert not p._is_allowed_probe_output(bad, pos), bad


def test_checked_probe_path_raises_for_disallowed_basename(tmp_path):
    p = _load_probe()
    pos = ["20130401"]
    with pytest.raises(p.ProbeBoundaryBreach):
        p._checked_probe_path(str(tmp_path), "bad.csv", pos)


# ── 7. Parser / row-count contract ───────────────────────────────────────────

def test_parser_counts_all_data_rows():
    p = _load_probe()
    nominal = date(2018, 2, 14)
    payload = _make_payload_zip(nominal, n_rows=7)
    out = p.parse_event_file_payload(payload, nominal_date=nominal)
    assert out["row_count"] == 7
    assert out["header_anomaly_detected"] is False
    assert out["rows_matching_nominal_date"] == 7
    assert out["rows_mismatching_nominal_date"] == 0
    assert out["rows_unparseable_sqldate"] == 0
    assert out["date_validation_pass"] is True


def test_parser_detects_header_anomaly_and_does_not_silently_subtract():
    p = _load_probe()
    nominal = date(2018, 2, 14)
    payload = _make_payload_zip(nominal, n_rows=5, header_first_row=True)
    out = p.parse_event_file_payload(payload, nominal_date=nominal)
    # 1 header + 5 data rows = 6 total rows counted (no silent subtraction)
    assert out["row_count"] == 6
    assert out["header_anomaly_detected"] is True
    assert out["rows_matching_nominal_date"] == 5
    assert out["rows_unparseable_sqldate"] == 1
    # date_validation_pass is False because of the unparseable header row.
    assert out["date_validation_pass"] is False


def test_parser_flags_date_mismatch():
    p = _load_probe()
    nominal = date(2018, 2, 14)
    wrong = date(2018, 2, 15)
    payload = _make_mismatched_payload_zip(nominal, wrong, n_rows=4)
    out = p.parse_event_file_payload(payload, nominal_date=nominal)
    assert out["row_count"] == 4
    assert out["rows_matching_nominal_date"] == 0
    assert out["rows_mismatching_nominal_date"] == 4
    assert out["date_validation_pass"] is False


def test_parser_refuses_2023_plus_sqldate_row():
    p = _load_probe()
    nominal = date(2022, 12, 31)
    # Build a payload whose SQLDATE column is in 2023.
    payload = _make_mismatched_payload_zip(
        nominal, wrong_date=date(2023, 1, 1), n_rows=2,
    )
    with pytest.raises(p.ProbeBoundaryBreach):
        p.parse_event_file_payload(payload, nominal_date=nominal)


def test_parser_refuses_nominal_2023_plus():
    p = _load_probe()
    with pytest.raises(p.ProbeBoundaryBreach):
        p.parse_event_file_payload(b"", nominal_date=date(2023, 1, 1))


# ── 8. Per-file fetch outcome handling ───────────────────────────────────────

def test_probe_one_file_200_ok():
    p = _load_probe()
    nominal = date(2018, 2, 14)
    payload = _make_payload_zip(nominal, n_rows=2)

    def fake_opener(url, timeout=30.0):
        return _FakeResponse(status=200, body=payload)

    result, body = p._probe_one_file(
        date_iso="2018-02-14",
        url="http://data.gdeltproject.org/events/20180214.export.CSV.zip",
        opener=fake_opener,
        timeout=30.0,
        is_positive=True,
    )
    assert result["fetch_outcome"] == "200_OK"
    assert result["status"] == 200
    assert body == payload


def test_probe_one_file_redirect_blocked():
    p = _load_probe()

    def fake_opener(url, timeout=30.0):
        raise p.RedirectBlocked(
            "probe opener blocked redirect (status 302); no follow"
        )

    result, body = p._probe_one_file(
        date_iso="2014-01-23",
        url="http://data.gdeltproject.org/events/20140123.export.CSV.zip",
        opener=fake_opener,
        timeout=30.0,
        is_positive=False,
    )
    assert result["fetch_outcome"] == "REDIRECT_BLOCKED"
    assert result["exception_class"] == "RedirectBlocked"
    assert body is None


def test_probe_one_file_http_404():
    p = _load_probe()
    url = "http://data.gdeltproject.org/events/20140123.export.CSV.zip"

    def fake_opener(u, timeout=30.0):
        raise urllib.error.HTTPError(u, 404, "Not Found", {}, None)

    result, body = p._probe_one_file(
        date_iso="2014-01-23",
        url=url,
        opener=fake_opener,
        timeout=30.0,
        is_positive=False,
    )
    assert result["fetch_outcome"] == "HTTP_NON_200"
    assert result["status"] == 404
    assert body is None


def test_probe_one_file_connection_error():
    p = _load_probe()

    def fake_opener(url, timeout=30.0):
        raise urllib.error.URLError("simulated DNS failure")

    result, body = p._probe_one_file(
        date_iso="2014-01-23",
        url="http://data.gdeltproject.org/events/20140123.export.CSV.zip",
        opener=fake_opener,
        timeout=30.0,
        is_positive=False,
    )
    assert result["fetch_outcome"] == "CONNECTION_ERROR"
    assert result["status"] is None
    assert body is None


# ── 9. Verdict map ───────────────────────────────────────────────────────────

def test_verdict_map_feasible_via_404_negative():
    p = _load_probe()
    pos = [
        {
            "is_positive": True,
            "fetch_outcome": "200_OK",
            "parse": {
                "row_count": 3,
                "header_anomaly_detected": False,
                "rows_matching_nominal_date": 3,
                "rows_mismatching_nominal_date": 0,
                "rows_unparseable_sqldate": 0,
                "date_validation_pass": True,
            },
        }
        for _ in range(5)
    ]
    neg = {
        "is_positive": False,
        "fetch_outcome": "HTTP_NON_200",
        "status": 404,
    }
    assert p._compute_verdict(pos, neg) == "FEASIBLE"


def test_verdict_map_gap_model_failed_on_negative_200():
    p = _load_probe()
    pos = [
        {
            "is_positive": True,
            "fetch_outcome": "200_OK",
            "parse": {
                "row_count": 3,
                "header_anomaly_detected": False,
                "rows_matching_nominal_date": 3,
                "rows_mismatching_nominal_date": 0,
                "rows_unparseable_sqldate": 0,
                "date_validation_pass": True,
            },
        }
        for _ in range(5)
    ]
    neg = {"is_positive": False, "fetch_outcome": "200_OK", "status": 200}
    assert p._compute_verdict(pos, neg) == "GAP-MODEL-FAILED"


def test_verdict_map_gap_model_ambiguous_on_negative_connection_error():
    p = _load_probe()
    pos = [
        {
            "is_positive": True,
            "fetch_outcome": "200_OK",
            "parse": {
                "row_count": 3,
                "header_anomaly_detected": False,
                "rows_matching_nominal_date": 3,
                "rows_mismatching_nominal_date": 0,
                "rows_unparseable_sqldate": 0,
                "date_validation_pass": True,
            },
        }
        for _ in range(5)
    ]
    neg = {
        "is_positive": False,
        "fetch_outcome": "CONNECTION_ERROR",
        "status": None,
    }
    assert p._compute_verdict(pos, neg) == "GAP-MODEL-AMBIGUOUS"


def test_verdict_map_infeasible_retrieval_on_positive_failure():
    p = _load_probe()
    pos = [
        {"is_positive": True, "fetch_outcome": "HTTP_NON_200", "status": 503,
         "parse": None}
    ]
    neg = {"is_positive": False, "fetch_outcome": "HTTP_NON_200", "status": 404}
    assert p._compute_verdict(pos, neg) == "INFEASIBLE-RETRIEVAL"


def test_verdict_map_row_date_mismatch():
    p = _load_probe()
    pos = [
        {
            "is_positive": True,
            "fetch_outcome": "200_OK",
            "parse": {
                "row_count": 3,
                "header_anomaly_detected": False,
                "rows_matching_nominal_date": 1,
                "rows_mismatching_nominal_date": 2,
                "rows_unparseable_sqldate": 0,
                "date_validation_pass": False,
            },
        }
    ]
    neg = {"is_positive": False, "fetch_outcome": "HTTP_NON_200", "status": 404}
    assert p._compute_verdict(pos, neg) == "ROW-DATE-MISMATCH"


# ── 10. End-to-end (synthetic opener; no network) ────────────────────────────

def test_end_to_end_feasible_with_fake_opener(monkeypatch, tmp_path):
    p = _load_probe()
    monkeypatch.setattr(p, "EVENT_FILE_PROBE_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_EVENT_FILE_PROBE_AUTHORIZED", "1")
    monkeypatch.setattr(
        p, "_load_recognized_units",
        lambda repo_root: _good_recognized_units(),
    )

    fake_opener = _make_feasible_opener()
    out_dir = str(tmp_path / "out")
    returned = p.run_event_file_probe(
        repo_root=str(tmp_path),
        cli_flag=True,
        opener=fake_opener,
        output_dir=out_dir,
    )
    assert returned == out_dir

    # Allowed outputs only.
    names = sorted(os.listdir(out_dir))
    expected_payloads = {
        "payload_20130401.zip", "payload_20140122.zip",
        "payload_20140126.zip", "payload_20180214.zip",
        "payload_20221231.zip",
    }
    assert "probe_metadata.json" in names
    assert "probe_summary.md" in names
    assert expected_payloads.issubset(set(names))
    # No negative-control payload on disk.
    assert "payload_20140123.zip" not in names
    # No extracted CSV.
    assert not any(n.endswith(".CSV") for n in names)
    assert not any(n.endswith(".csv") for n in names)

    with open(os.path.join(out_dir, "probe_metadata.json"), "r") as fh:
        md = json.load(fh)
    assert md["verdict"] == "FEASIBLE"
    assert md["recognized_list_path"] == p.RECOGNIZED_LIST_PATH
    assert md["event_file_base_url"] == p.EVENT_FILE_BASE_URL
    assert md["no_market_data"] is True
    assert md["no_step_2"] is True
    assert md["positive_sample_dates"] == [
        "2013-04-01", "2014-01-22", "2014-01-26",
        "2018-02-14", "2022-12-31",
    ]
    assert md["negative_control_date"] == "2014-01-23"
    # Per-result shape sanity.
    by_date = {r["date"]: r for r in md["results"]}
    assert by_date["2013-04-01"]["fetch_outcome"] == "200_OK"
    assert by_date["2014-01-23"]["fetch_outcome"] == "HTTP_NON_200"
    assert by_date["2014-01-23"]["status"] == 404


def test_end_to_end_refuses_when_guards_off(monkeypatch, tmp_path):
    p = _load_probe()
    monkeypatch.delenv("LANE2_EVENT_FILE_PROBE_AUTHORIZED", raising=False)
    # Inject a fake opener that, if reached, would raise.

    def boom(*a, **kw):
        raise AssertionError("opener invoked despite guards being off")

    out_dir = str(tmp_path / "out")
    with pytest.raises(SystemExit):
        p.run_event_file_probe(
            repo_root=str(tmp_path),
            cli_flag=True,
            opener=boom,
            output_dir=out_dir,
        )
    assert not os.path.exists(out_dir)


# ── 11. No market / Step 2 / category-filter leakage ─────────────────────────

def test_no_market_or_step2_or_filtering_surface_in_source():
    """The script declares via metadata + comments that market data /
    Step 2 / category filtering are NOT touched. The forbidden list
    therefore must NOT include tokens like `step_2`, `market_data`,
    `spike_threshold`, or bare `theme`/`actor`/`geography`, which appear
    inside the negation declarations themselves. The list below contains
    only identifier-shape tokens that would appear in actual
    implementation logic (function names, computation names, filter
    helpers) and that the script's negation declarations never use."""
    p = _load_probe()
    src = open(p.__file__, "r", encoding="utf-8").read().lower()
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
            "probe source unexpectedly mentions forbidden surface {!r}"
            .format(f)
        )


def test_no_market_or_step2_keys_in_end_to_end_metadata(
    monkeypatch, tmp_path,
):
    """End-to-end metadata must not contain identifier-shape mentions of
    market / signal / asset machinery. Tokens like `step_2`,
    `market_data`, `spike_threshold` are deliberately emitted as
    negation keys (`no_step_2: True`, etc.) and are NOT in the forbidden
    set; this test catches accidental positive emission only."""
    p = _load_probe()
    monkeypatch.setattr(p, "EVENT_FILE_PROBE_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_EVENT_FILE_PROBE_AUTHORIZED", "1")
    monkeypatch.setattr(
        p, "_load_recognized_units",
        lambda repo_root: _good_recognized_units(),
    )
    fake_opener = _make_feasible_opener()
    out_dir = str(tmp_path / "out")
    p.run_event_file_probe(
        repo_root=str(tmp_path),
        cli_flag=True,
        opener=fake_opener,
        output_dir=out_dir,
    )
    with open(os.path.join(out_dir, "probe_metadata.json"), "r") as fh:
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
            "probe metadata unexpectedly mentions forbidden surface "
            "{!r}".format(f)
        )
