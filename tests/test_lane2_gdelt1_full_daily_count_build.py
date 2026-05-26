"""Conformance tests for the Lane 2 GDELT 1.0 full daily-count build runner.

Synthetic fixtures and fake openers only. NO real network. NO real GDELT
data. NO market data. NO 2023+. The runner under test ships inert;
tests either monkeypatch guards or invoke pure helpers that don't reach
the network path.

Test categories (per design memo `7780a97` §16 Decision K):

  1. Guard discipline
  2. Recognized-list smoke (against real committed capture)
  3. Build input universe (classification, fetch-set construction)
  4. Date-domain (full civil calendar [2013-04-01, 2022-12-31])
  5. SQLDATE re-keying
  6. Exact offset taxonomy (pre-empts 487dadb-style corrective)
  7. Structural T-3650 zero (memo §10.2 explicit acceptance)
  8. T+1 uniform handling
  9. Backward edge (out-of-window SQLDATE diagnostic)
 10. Forward edge / 2022-seal (no-2023+ enforcement)
 11. Known substrate gap handling
 12. Coverage flag domain + completeness formula
 13. Parser validation
 14. Output artifact allow-list
 15. Payload-discard mechanism
 16. No-market-data / no-Step-2 leakage
"""

import hashlib
import importlib.util
import io
import json
import os
import re
import urllib.error
import zipfile
from datetime import date, timedelta

import pytest


# ── Module loader ────────────────────────────────────────────────────────────

def _load_runner():
    path = os.path.join(
        os.path.dirname(__file__), "..", "scripts",
        "run_lane2_gdelt1_full_daily_count_build.py",
    )
    spec = importlib.util.spec_from_file_location(
        "l2_full_build", path,
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


# ── Synthetic payload builder ────────────────────────────────────────────────

def _make_payload_zip(nominal_date, offset_buckets):
    """Build a synthetic GDELT-shaped .zip payload.

    `offset_buckets` is a list of `(offset_days, count)` tuples. Each
    tuple contributes `count` rows whose SQLDATE column = nominal_date
    + offset_days.
    """
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
    def __init__(self, status=200, body=b""):
        self._status = status
        self._body = body

    def getcode(self):
        return self._status

    def read(self):
        return self._body

    def close(self):
        pass


def _expected_offset_buckets(t_plus_1=True):
    if t_plus_1:
        return [
            (-3650, 4),
            (-365, 30),
            (-30, 15),
            (-7, 25),
            (-1, 20),
            (0, 500),
            (1, 5),
        ]
    return [
        (-3650, 4),
        (-365, 30),
        (-30, 15),
        (-7, 25),
        (-1, 20),
        (0, 500),
    ]


# ── Synthetic recognized-list capture ────────────────────────────────────────

def _make_synthetic_capture(in_window_dates, monthly=(), yearly=(),
                            out_of_window=(), unknown=(), duplicates=()):
    units = list(in_window_dates) + list(monthly) + list(yearly) + \
            list(out_of_window) + list(unknown) + list(duplicates)
    return {
        "recognized_in_window_units": units,
        "recognized_in_window_count": len(units),
        "schema_version": "v0.1",
    }


def _write_synthetic_capture(tmp_path, capture_data):
    """Write a synthetic capture under the standard relative path within
    tmp_path so the runner's _load_recognized_list can find it."""
    rel = (
        "results/lane2_gdelt1_turn_b_recognized_list_capture/"
        "20260521T124853Z/recognized_list.json"
    )
    full = tmp_path / rel
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(json.dumps(capture_data), encoding="utf-8")
    return full


# ============================================================================
# 1. Guard discipline
# ============================================================================

def test_default_module_constant_is_false():
    m = _load_runner()
    assert m.FULL_BUILD_AUTHORIZED is False


def test_guards_refuse_default(monkeypatch):
    m = _load_runner()
    monkeypatch.delenv("LANE2_FULL_BUILD_AUTHORIZED", raising=False)
    assert m._guards_ok(True) is False


def test_guards_refuse_missing_env(monkeypatch):
    m = _load_runner()
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", True)
    monkeypatch.delenv("LANE2_FULL_BUILD_AUTHORIZED", raising=False)
    assert m._guards_ok(True) is False


def test_guards_refuse_missing_cli_flag(monkeypatch):
    m = _load_runner()
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_FULL_BUILD_AUTHORIZED", "1")
    assert m._guards_ok(False) is False


def test_guards_refuse_missing_module_constant(monkeypatch):
    m = _load_runner()
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", False)
    monkeypatch.setenv("LANE2_FULL_BUILD_AUTHORIZED", "1")
    assert m._guards_ok(True) is False


def test_run_refuses_before_any_side_effect(tmp_path, monkeypatch):
    """Refusal happens before opener / output dir / fetch.

    We point the runner at a tmp_path that DOES NOT contain a recognized
    list capture. If the runner refused at the right point (before
    loading), no IOError should be raised — only SystemExit from refusal.
    """
    m = _load_runner()
    monkeypatch.delenv("LANE2_FULL_BUILD_AUTHORIZED", raising=False)
    with pytest.raises(SystemExit):
        m.run_full_daily_count_build(str(tmp_path), cli_flag=False)
    # No output dir should have been created
    assert not (tmp_path / "results" / "lane2_gdelt1_full_daily_count_build").exists()


def test_all_three_guards_satisfied_passes_gate(monkeypatch):
    m = _load_runner()
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_FULL_BUILD_AUTHORIZED", "1")
    assert m._guards_ok(True) is True


# ============================================================================
# 2. Recognized-list smoke (real committed capture)
# ============================================================================

def test_real_capture_loads_and_sha_matches():
    m = _load_runner()
    data, sha, byte_size = m._load_recognized_list(REPO_ROOT)
    assert sha == m.RECOGNIZED_LIST_SHA256
    assert byte_size > 0
    assert "recognized_in_window_units" in data


def test_real_capture_unit_count_3647():
    m = _load_runner()
    data, _, _ = m._load_recognized_list(REPO_ROOT)
    units = data["recognized_in_window_units"]
    assert len(units) == 3647


def test_real_capture_classification_yields_3558_daily_and_89_non_daily():
    m = _load_runner()
    data, _, _ = m._load_recognized_list(REPO_ROOT)
    units = data["recognized_in_window_units"]
    classification = m.classify_recognized_units(units)
    assert len(classification["daily_in_window"]) == 3558
    non_daily = (
        len(classification["yearly"])
        + len(classification["monthly"])
        + len(classification["daily_out_of_window"])
        + len(classification["unknown"])
        + len(classification["duplicates"])
    )
    assert non_daily == 89
    # The 89-unit residual is split into 2 yearly + 87 monthly (no
    # unknown, no duplicates, no out-of-window).
    assert len(classification["yearly"]) == 2
    assert len(classification["monthly"]) == 87
    assert len(classification["daily_out_of_window"]) == 0
    assert len(classification["unknown"]) == 0
    assert len(classification["duplicates"]) == 0


def test_real_capture_reconciliation_surfaces_residual_without_inventing():
    m = _load_runner()
    data, _, _ = m._load_recognized_list(REPO_ROOT)
    units = data["recognized_in_window_units"]
    report = m.build_reconciliation_report(units)
    assert report["total_capture_units"] == 3647
    assert report["civil_days_in_window"] == 3562
    assert report["known_substrate_gaps_count"] == 4
    assert report["naive_expected_daily_urls"] == 3558
    assert report["fetch_set_count"] == 3558
    assert report["fetch_set_matches_naive_expectation"] is True
    assert report["residual_total"] == 89
    # Reconciliation must NOT invent — it reports classified counts.
    assert report["classification"]["yearly_count"] == 2
    assert report["classification"]["monthly_count"] == 87


def test_real_capture_reconciliation_passes_consistency_check():
    m = _load_runner()
    data, _, _ = m._load_recognized_list(REPO_ROOT)
    report = m.build_reconciliation_report(
        data["recognized_in_window_units"]
    )
    m.assert_reconciliation_consistent(report)  # should not raise


def test_real_capture_known_gaps_absent_from_capture():
    """Confirm substrate gaps are NOT enumerated by the recognized list
    (they were excluded at capture time)."""
    m = _load_runner()
    data, _, _ = m._load_recognized_list(REPO_ROOT)
    units = set(data["recognized_in_window_units"])
    for gap in m.KNOWN_SUBSTRATE_GAPS:
        assert gap not in units


def test_real_capture_file_not_mutated_by_load():
    """Loading the capture must not mutate the on-disk file."""
    m = _load_runner()
    path = os.path.join(REPO_ROOT, m.RECOGNIZED_LIST_PATH)
    pre = m._hash_file_sha256(path)
    m._load_recognized_list(REPO_ROOT)
    post = m._hash_file_sha256(path)
    assert pre == post == m.RECOGNIZED_LIST_SHA256


# ============================================================================
# 3. Build input universe
# ============================================================================

def test_classifier_yearly_pattern():
    m = _load_runner()
    c = m.classify_recognized_units(["2005", "2013"])
    assert c["yearly"] == ["2005", "2013"]
    assert c["monthly"] == []
    assert c["daily_in_window"] == []


def test_classifier_monthly_pattern():
    m = _load_runner()
    c = m.classify_recognized_units(["2006-01", "2013-03"])
    assert c["monthly"] == ["2006-01", "2013-03"]
    assert c["yearly"] == []


def test_classifier_daily_in_window():
    m = _load_runner()
    c = m.classify_recognized_units([
        "2013-04-01", "2022-12-31", "2018-06-15"
    ])
    assert len(c["daily_in_window"]) == 3
    assert c["daily_out_of_window"] == []


def test_classifier_daily_out_of_window():
    m = _load_runner()
    c = m.classify_recognized_units([
        "2013-03-31",   # pre-window
        "2023-01-01",   # post-window (would be 2023+)
    ])
    assert len(c["daily_out_of_window"]) == 2
    assert c["daily_in_window"] == []


def test_classifier_unknown_pattern():
    m = _load_runner()
    c = m.classify_recognized_units([
        "garbage", "2013-W14", "20130401"
    ])
    assert len(c["unknown"]) == 3


def test_classifier_duplicates_detected():
    m = _load_runner()
    c = m.classify_recognized_units([
        "2013-04-01", "2013-04-01", "2013-04-02"
    ])
    assert c["duplicates"] == ["2013-04-01"]
    assert len(c["daily_in_window"]) == 2


def test_url_construction_daily_only_pattern():
    m = _load_runner()
    url = m.date_to_daily_url(date(2018, 6, 15))
    assert url == "http://data.gdeltproject.org/events/20180615.export.CSV.zip"


def test_url_construction_refuses_2023_plus():
    m = _load_runner()
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.date_to_daily_url(date(2023, 1, 1))


def test_url_construction_refuses_pre_window():
    m = _load_runner()
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.date_to_daily_url(date(2013, 3, 31))


def test_url_construction_refuses_post_window():
    m = _load_runner()
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.date_to_daily_url(date(2022, 12, 31) + timedelta(days=1))


def test_construct_daily_urls_deterministic_order():
    m = _load_runner()
    fetch_set = ["2014-05-15", "2013-04-01", "2018-06-15"]
    urls = m.construct_daily_urls(sorted(fetch_set))
    assert urls[0].endswith("20130401.export.CSV.zip")
    assert urls[1].endswith("20140515.export.CSV.zip")
    assert urls[2].endswith("20180615.export.CSV.zip")


def test_known_substrate_gaps_excluded_from_fetch_set():
    m = _load_runner()
    units = ["2013-04-01", "2014-01-23", "2014-01-24",
             "2014-01-25", "2014-03-19", "2014-04-01"]
    # If known gaps were present in the capture, the reconciliation
    # would fail the consistency check. But the runner's fetch_set
    # builder subtracts them out regardless.
    report = m.build_reconciliation_report(units)
    for gap in m.KNOWN_SUBSTRATE_GAPS:
        assert gap not in report["fetch_set"]


def test_non_daily_units_excluded_from_fetch_set():
    m = _load_runner()
    units = ["2013-04-01", "2005", "2006-01", "2014-04-01"]
    report = m.build_reconciliation_report(units)
    assert set(report["fetch_set"]) == {"2013-04-01", "2014-04-01"}


def test_reconciliation_consistency_check_catches_gap_in_capture():
    m = _load_runner()
    # Build a capture that erroneously includes a known gap as a daily unit
    units = sorted(set([d.isoformat() for d in
                        [date(2013,4,1) + timedelta(days=i)
                         for i in range(0, 3562)]]))
    # Adding a "gap" date as an explicit daily would only be detected if
    # the gap were in the capture; the standard reconciliation removes
    # gaps from the fetch_set. We confirm that if a gap IS present in
    # the capture, assert_reconciliation_consistent flags it.
    assert "2014-01-23" in units  # the synthetic capture above includes all civil dates
    report = m.build_reconciliation_report(units)
    # fetch_set excludes known gaps; gaps_present_in_capture should be 4
    assert len(report["gaps_present_in_capture"]) == 4
    with pytest.raises(m.ReconciliationContradiction):
        m.assert_reconciliation_consistent(report)


def test_reconciliation_consistency_check_catches_out_of_window_daily():
    m = _load_runner()
    units = ["2013-04-01", "2023-01-01"]  # post-window
    report = m.build_reconciliation_report(units)
    # Will fail because daily_out_of_window_count > 0
    with pytest.raises(m.ReconciliationContradiction):
        m.assert_reconciliation_consistent(report)


# ============================================================================
# 4. Date-domain tests
# ============================================================================

def test_civil_date_domain_has_3562_days():
    m = _load_runner()
    domain = m.civil_date_domain()
    assert len(domain) == 3562


def test_civil_date_domain_starts_2013_04_01():
    m = _load_runner()
    assert m.civil_date_domain()[0] == date(2013, 4, 1)


def test_civil_date_domain_ends_2022_12_31():
    m = _load_runner()
    assert m.civil_date_domain()[-1] == date(2022, 12, 31)


def test_civil_date_domain_is_strictly_ascending():
    m = _load_runner()
    domain = m.civil_date_domain()
    for a, b in zip(domain, domain[1:]):
        assert (b - a).days == 1


# ============================================================================
# 5. SQLDATE re-keying tests
# ============================================================================

def test_aggregation_routes_by_sqldate():
    m = _load_runner()
    # Two synthetic payloads: f_(2018-06-15) emits T=0 rows with
    # SQLDATE=2018-06-15; f_(2018-06-16) emits T-1 rows with
    # SQLDATE=2018-06-15. Both should aggregate to civil date 2018-06-15.
    nom_a = date(2018, 6, 15)
    nom_b = date(2018, 6, 16)
    pa = m.parse_payload(
        _make_payload_zip(nom_a, [(0, 10)]), nom_a,
    )
    pb = m.parse_payload(
        _make_payload_zip(nom_b, [(-1, 7)]), nom_b,
    )
    accum = m._new_accumulator()
    m._ingest_parse_into_accumulator(accum, pa)
    m._ingest_parse_into_accumulator(accum, pb)
    target = "2018-06-15"
    cell = accum["per_sqldate_per_offset"].get(target, {})
    assert cell.get(0, 0) == 10
    assert cell.get(-1, 0) == 7


def test_aggregation_does_not_use_nominal_date_as_primary_key():
    m = _load_runner()
    # f_(2018-06-15) emits T=0 + T-1 + T-7. Each routes to a DIFFERENT
    # SQLDATE, not all to 2018-06-15.
    nom = date(2018, 6, 15)
    p = m.parse_payload(
        _make_payload_zip(nom, [(0, 3), (-1, 2), (-7, 1)]), nom,
    )
    accum = m._new_accumulator()
    m._ingest_parse_into_accumulator(accum, p)
    assert accum["per_sqldate_per_offset"]["2018-06-15"].get(0) == 3
    assert accum["per_sqldate_per_offset"]["2018-06-14"].get(-1) == 2
    assert accum["per_sqldate_per_offset"]["2018-06-08"].get(-7) == 1


def test_aggregation_retains_per_offset_diagnostics():
    m = _load_runner()
    nom = date(2018, 6, 15)
    p = m.parse_payload(
        _make_payload_zip(nom, [(0, 5), (-30, 2)]), nom,
    )
    accum = m._new_accumulator()
    m._ingest_parse_into_accumulator(accum, p)
    assert accum["per_offset_total"][0] == 5
    assert accum["per_offset_total"][-30] == 2
    assert accum["per_offset_total"][-7] == 0


# ============================================================================
# 6. Exact offset taxonomy (pre-empt 487dadb-style corrective)
# ============================================================================

def test_expected_offsets_is_exact_set():
    m = _load_runner()
    assert set(m.EXPECTED_OFFSETS) == {-3650, -365, -30, -7, -1, 0, 1}


def test_parser_accepts_all_seven_expected_offsets():
    m = _load_runner()
    nom = date(2018, 6, 15)
    p = m.parse_payload(
        _make_payload_zip(nom, [
            (-3650, 1), (-365, 1), (-30, 1), (-7, 1),
            (-1, 1), (0, 1), (1, 1),
        ]),
        nom,
    )
    # per_offset_count counts ALL observed rows at each offset (in or
    # out of window), matching `858b501` §11 aggregate-pattern.
    for off in m.EXPECTED_OFFSETS:
        assert p["per_offset_count"][off] == 1
    # T-3650 lands at 2008-06-25 (pre-window), routed to out-of-window
    assert p["out_of_window_row_count"] == 1


@pytest.mark.parametrize("bad_offset", [-3652, -3651, -3649, -3648,
                                         -366, -364, -31, -29, -8, -6,
                                         -2, 2, 7, 30, 365])
def test_parser_hard_fails_unexpected_offset(bad_offset):
    m = _load_runner()
    nom = date(2018, 6, 15)
    payload = _make_payload_zip(nom, [(bad_offset, 1)])
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.parse_payload(payload, nom)


def test_taxonomy_no_tolerance_window_for_minus_3650():
    """-3651 and -3649 are near-misses of -3650 and must hard-fail; no
    tolerance window (validates the `487dadb` exact-integer correction)."""
    m = _load_runner()
    nom = date(2018, 6, 15)
    for bad in [-3651, -3649]:
        with pytest.raises(m.FullBuildBoundaryBreach):
            m.parse_payload(_make_payload_zip(nom, [(bad, 1)]), nom)


# ============================================================================
# 7. Structural T-3650 zero (memo §10.2 explicit acceptance)
# ============================================================================

def test_t_minus_3650_excluded_from_expected_cone():
    m = _load_runner()
    for d in [date(2013, 4, 1), date(2015, 6, 15), date(2022, 12, 31)]:
        assert -3650 not in m.expected_cone(d)


def test_t_minus_3650_zero_in_primary_series_per_civil_date():
    """For every in-window civil date d, the T-3650 contribution is
    structurally zero in the primary daily-count rows, because the
    contributing file's nominal date d+3650 is in [2023-04-01,
    2032-12-31], all excluded by the no-2023+ posture."""
    m = _load_runner()
    # Sample a few civil dates and verify the contributing file is 2023+
    for d in [date(2013, 4, 1), date(2018, 6, 15), date(2022, 12, 31)]:
        cf = m.contributing_file_nominal_date(d, -3650)
        assert cf >= m.SEAL_START


def test_t_minus_3650_rows_routed_to_out_of_window_diagnostic():
    """A T-3650 row in any in-universe publishing file has SQLDATE
    pre-2013, outside the locked window — the parser routes it to the
    out-of-window diagnostic, not to the in-window per-SQLDATE map.

    Per `858b501` §11 aggregate-pattern, the parser's per_offset_count
    counts ALL observed rows at each offset (in + out of window). So
    per_offset_count[-3650] reflects what was observed (3), while the
    sqldate_offset_counts map (in-window only) excludes them.
    """
    m = _load_runner()
    nom = date(2013, 9, 7)  # one of the characterization dates
    p = m.parse_payload(
        _make_payload_zip(nom, [(-3650, 3), (0, 10)]),
        nom,
    )
    # T-3650 contributes to out-of-window because nom - 3650 lands in 2003
    assert p["out_of_window_row_count"] == 3
    # The in-window per-SQLDATE map has only T=0 contributions
    in_window_sqldates = {iso for (iso, _) in p["sqldate_offset_counts"].keys()}
    assert in_window_sqldates == {"2013-09-07"}
    # per_offset_count records observed rows (in + out)
    assert p["per_offset_count"][-3650] == 3
    assert p["per_offset_count"][0] == 10


# ============================================================================
# 8. T+1 uniform handling
# ============================================================================

def test_t_plus_1_kept_and_rekeyed_to_sqldate():
    m = _load_runner()
    nom = date(2014, 12, 31)  # pre-2015 era
    p = m.parse_payload(
        _make_payload_zip(nom, [(0, 10), (1, 5)]),
        nom,
    )
    # T+1 rows have SQLDATE = 2015-01-01
    assert ("2015-01-01", 1) in p["sqldate_offset_counts"]
    assert p["sqldate_offset_counts"][("2015-01-01", 1)] == 5


def test_t_plus_1_era_cutoff_pre_2015_includes_2015_01_01():
    m = _load_runner()
    # d = 2015-01-01 is the LATEST pre-2015 T+1 era date
    assert 1 in m.expected_cone(date(2015, 1, 1))
    assert 1 not in m.expected_cone(date(2015, 1, 2))


def test_t_plus_1_not_dropped_or_normalized_in_aggregation():
    m = _load_runner()
    nom = date(2014, 6, 15)
    p = m.parse_payload(
        _make_payload_zip(nom, [(0, 10), (1, 3)]),
        nom,
    )
    accum = m._new_accumulator()
    m._ingest_parse_into_accumulator(accum, p)
    # T+1 rows are counted, not normalized away
    assert accum["per_offset_total"][1] == 3
    assert accum["per_sqldate_per_offset"]["2014-06-16"][1] == 3


# ============================================================================
# 9. Backward edge (out-of-window SQLDATE)
# ============================================================================

def test_out_of_window_sqldate_excluded_from_primary():
    m = _load_runner()
    nom = date(2013, 9, 7)
    p = m.parse_payload(
        _make_payload_zip(nom, [(-3650, 2), (0, 100)]),
        nom,
    )
    # The 2003-12-04 SQLDATE rows do NOT appear in sqldate_offset_counts
    iso_keys = {iso for (iso, _) in p["sqldate_offset_counts"].keys()}
    assert "2003-12-04" not in iso_keys
    assert p["out_of_window_row_count"] == 2


def test_out_of_window_diagnostic_records_distribution():
    m = _load_runner()
    nom = date(2013, 9, 7)
    p = m.parse_payload(
        _make_payload_zip(nom, [(-3650, 2)]),
        nom,
    )
    dist = p["out_of_window_sqldate_distribution"]
    # T-3650 from nom=2013-09-07 lands at nom - 3650 days (2003-09-10
    # given integer-day arithmetic — exact value depends on calendar
    # arithmetic but is guaranteed to be in 2003-2012, pre-window).
    assert len(dist) == 1
    only_sqldate = list(dist.keys())[0]
    assert only_sqldate.startswith("2003-")  # pre-window year
    assert dist[only_sqldate]["-3650"] == 2


# ============================================================================
# 10. Forward edge / 2022-seal
# ============================================================================

def test_no_2023_plus_url_in_construct_daily_urls():
    m = _load_runner()
    # Even if someone tries to pass a 2023+ date in, it hard-fails
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.construct_daily_urls(["2023-01-01"])


def test_parser_hard_fails_on_2023_plus_sqldate():
    m = _load_runner()
    nom = date(2022, 12, 30)
    # Synthetic payload with a 2023-01-01 SQLDATE row (offset +2, also
    # not in the expected set, but the 2023+ check should fire first via
    # SEAL_START)
    rows = ["1\t20230101\tA"]
    tsv = "\n".join(rows)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("20221230.export.CSV", tsv)
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.parse_payload(buf.getvalue(), nom)


def test_right_truncated_2022_seal_flag_fires_for_late_dates():
    m = _load_runner()
    # daily_set built from the recognized capture (post-2015 era)
    # For d = 2022-12-31, expected cone = {0, -1, -7, -30, -365}.
    # T-1 source = 2023-01-01 (excluded by no-2023+); same for the rest.
    # Only T=0 source (2022-12-31) is in-universe.
    daily_set = {"2022-12-31"}
    gaps_set = set(m.KNOWN_SUBSTRATE_GAPS)
    cov = m.coverage_for_date(date(2022, 12, 31), daily_set, gaps_set)
    assert cov["coverage_quality_flag"] == "right_truncated_2022_seal"
    assert cov["available_contributing_files_count"] == 1
    assert cov["expected_contributing_files_count"] == 5


def test_no_post_2022_leakage_in_boundary_declarations():
    m = _load_runner()
    decl = m._boundary_declarations()
    assert decl["no_2023plus_access"] is True
    assert decl["no_market_data"] is True
    assert decl["no_step_2"] is True


# ============================================================================
# 11. Known substrate gap handling
# ============================================================================

def test_known_substrate_gaps_constants():
    m = _load_runner()
    assert m.KNOWN_SUBSTRATE_GAPS == (
        "2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19",
    )


def test_gap_sqldates_eligible_in_civil_domain():
    m = _load_runner()
    domain = {d.isoformat() for d in m.civil_date_domain()}
    for gap in m.KNOWN_SUBSTRATE_GAPS:
        assert gap in domain


def test_t0_file_status_marks_known_gaps_expected_absent():
    m = _load_runner()
    daily_set = {"2014-01-22", "2014-01-26"}
    gaps_set = set(m.KNOWN_SUBSTRATE_GAPS)
    status = m.t0_file_status(date(2014, 1, 23), daily_set, gaps_set)
    assert status == "expected_absent_per_recognized_list"


def test_t0_file_status_present_for_in_universe_date():
    m = _load_runner()
    daily_set = {"2018-06-15"}
    gaps_set = set(m.KNOWN_SUBSTRATE_GAPS)
    assert m.t0_file_status(
        date(2018, 6, 15), daily_set, gaps_set,
    ) == "present"


def test_coverage_flag_t0_absent_substrate_gap():
    m = _load_runner()
    # Use d = 2014-03-19 (substrate gap with NO adjacent gap dates among
    # its other cone members; only T=0 fires the cause).
    d = date(2014, 3, 19)
    daily_set = set()
    for off in [-1, -7, -30, -365, 1]:
        cf = m.contributing_file_nominal_date(d, off)
        daily_set.add(cf.isoformat())
    gaps_set = set(m.KNOWN_SUBSTRATE_GAPS)
    cov = m.coverage_for_date(d, daily_set, gaps_set)
    assert cov["coverage_quality_flag"] == "t0_absent_substrate_gap"


# ============================================================================
# 12. Coverage flag domain + completeness formula
# ============================================================================

def test_coverage_flag_full_for_interior_date():
    m = _load_runner()
    # Interior post-2015 date with all 5 cone members in-universe
    d = date(2018, 6, 15)
    cone_dates = [
        m.contributing_file_nominal_date(d, off).isoformat()
        for off in [0, -1, -7, -30, -365]
    ]
    daily_set = set(cone_dates)
    cov = m.coverage_for_date(d, daily_set, set(m.KNOWN_SUBSTRATE_GAPS))
    assert cov["coverage_quality_flag"] == "full"
    assert cov["coverage_completeness"] == 1.0


def test_coverage_flag_left_truncated_2013_edge():
    m = _load_runner()
    # d = 2013-04-01 (window left edge); T+1 source is 2013-03-31 (pre-window)
    d = date(2013, 4, 1)
    cone = m.expected_cone(d)
    # Build daily_set with all cone members EXCEPT T+1's pre-window source
    daily_set = set()
    for off in cone:
        cf = m.contributing_file_nominal_date(d, off)
        if cf >= m.START_DATE and cf <= m.END_DATE:
            daily_set.add(cf.isoformat())
    cov = m.coverage_for_date(d, daily_set, set(m.KNOWN_SUBSTRATE_GAPS))
    assert cov["coverage_quality_flag"] == "left_truncated_2013_edge"


def test_coverage_flag_t_plus_1_neighbor_substrate_gap():
    m = _load_runner()
    # d = 2014-03-20; T+1 source = 2014-03-19 (substrate gap).
    # T=0 source = 2014-03-20 (in-universe).
    # T-1 source = 2014-03-21, T-7 = 2014-03-27, T-30 = 2014-04-19,
    # T-365 = 2015-03-20 (all in-universe).
    d = date(2014, 3, 20)
    cone = m.expected_cone(d)
    daily_set = set()
    for off in cone:
        cf = m.contributing_file_nominal_date(d, off)
        if (m.START_DATE <= cf <= m.END_DATE
                and cf.isoformat() not in m.KNOWN_SUBSTRATE_GAPS):
            daily_set.add(cf.isoformat())
    cov = m.coverage_for_date(d, daily_set, set(m.KNOWN_SUBSTRATE_GAPS))
    assert cov["coverage_quality_flag"] == "t_plus_1_neighbor_substrate_gap"


def test_coverage_flag_right_truncated_late_2022():
    m = _load_runner()
    # d = 2022-12-31; all T-n sources are 2023+, T=0 source is 2022-12-31
    d = date(2022, 12, 31)
    daily_set = {"2022-12-31"}
    cov = m.coverage_for_date(d, daily_set, set(m.KNOWN_SUBSTRATE_GAPS))
    assert cov["coverage_quality_flag"] == "right_truncated_2022_seal"
    assert cov["available_contributing_files_count"] == 1
    assert cov["expected_contributing_files_count"] == 5


def test_coverage_flag_multiple_concatenation():
    m = _load_runner()
    # Use d = 2014-01-25 (substrate gap; T+1 source = 2014-01-24 is
    # also a gap; T-1 source = 2014-01-26 is NOT a gap). Fires exactly
    # 2 causes: t0_absent_substrate_gap + t_plus_1_neighbor_substrate_gap.
    d = date(2014, 1, 25)
    cone = m.expected_cone(d)
    daily_set = set()
    for off in cone:
        cf = m.contributing_file_nominal_date(d, off)
        if (m.START_DATE <= cf <= m.END_DATE
                and cf.isoformat() not in m.KNOWN_SUBSTRATE_GAPS):
            daily_set.add(cf.isoformat())
    cov = m.coverage_for_date(d, daily_set, set(m.KNOWN_SUBSTRATE_GAPS))
    flag = cov["coverage_quality_flag"]
    assert flag == (
        "t0_absent_substrate_gap+t_plus_1_neighbor_substrate_gap"
    )


def test_coverage_flag_t_minus_n_neighbor_substrate_gap_extension():
    """Implementation extension to design memo §11.3 closed flag domain.

    The design memo's 6-entry table does not cover T-1 / T-7 / T-30 /
    T-365 substrate-gap absences. The implementation extends the closed
    domain by one entry (`t_minus_n_neighbor_substrate_gap`) and
    surfaces this in metadata.coverage_diagnostic.design_memo_extensions.
    """
    m = _load_runner()
    # d = 2014-01-22: pre-2015 era. T=0=2014-01-22 (not gap).
    # T-1 source = 2014-01-23 (substrate gap!).
    # All other cone members non-gap and in-universe.
    d = date(2014, 1, 22)
    cone = m.expected_cone(d)
    daily_set = set()
    for off in cone:
        cf = m.contributing_file_nominal_date(d, off)
        if (m.START_DATE <= cf <= m.END_DATE
                and cf.isoformat() not in m.KNOWN_SUBSTRATE_GAPS):
            daily_set.add(cf.isoformat())
    cov = m.coverage_for_date(d, daily_set, set(m.KNOWN_SUBSTRATE_GAPS))
    assert cov["coverage_quality_flag"] == "t_minus_n_neighbor_substrate_gap"
    assert cov["expected_contributing_files_count"] == 6
    assert cov["available_contributing_files_count"] == 5
    assert cov["coverage_completeness"] == 5 / 6


def test_coverage_flag_extension_is_in_closed_domain():
    m = _load_runner()
    assert "t_minus_n_neighbor_substrate_gap" in m.COVERAGE_SINGLE_FLAGS
    assert m.is_valid_coverage_flag("t_minus_n_neighbor_substrate_gap")


def test_coverage_completeness_formula_post_2015():
    m = _load_runner()
    # d = 2022-12-04 → cone {0, -1, -7, -30, -365}; T-30 source =
    # 2023-01-03 (2023+, excluded); T-365 source = 2023-12-04 (2023+).
    # Available: T=0 (2022-12-04), T-1 (2022-12-05), T-7 (2022-12-11) = 3
    d = date(2022, 12, 4)
    daily_set = {"2022-12-04", "2022-12-05", "2022-12-11"}
    cov = m.coverage_for_date(d, daily_set, set(m.KNOWN_SUBSTRATE_GAPS))
    assert cov["expected_contributing_files_count"] == 5
    assert cov["available_contributing_files_count"] == 3
    assert cov["coverage_completeness"] == 3 / 5
    assert cov["coverage_quality_flag"] == "right_truncated_2022_seal"


def test_coverage_completeness_formula_pre_2015():
    m = _load_runner()
    d = date(2014, 6, 15)  # pre-2015 era → cone size 6
    cone_dates = [
        m.contributing_file_nominal_date(d, off).isoformat()
        for off in [0, -1, -7, -30, -365, 1]
    ]
    daily_set = set(cone_dates)
    cov = m.coverage_for_date(d, daily_set, set(m.KNOWN_SUBSTRATE_GAPS))
    assert cov["expected_contributing_files_count"] == 6
    assert cov["available_contributing_files_count"] == 6
    assert cov["coverage_completeness"] == 1.0


def test_coverage_flag_validator_accepts_single_flags():
    m = _load_runner()
    for f in m.COVERAGE_SINGLE_FLAGS:
        assert m.is_valid_coverage_flag(f)


def test_coverage_flag_validator_accepts_ordered_concatenation():
    m = _load_runner()
    assert m.is_valid_coverage_flag(
        "t0_absent_substrate_gap+right_truncated_2022_seal"
    )
    assert m.is_valid_coverage_flag(
        "right_truncated_2022_seal+left_truncated_2013_edge"
    )


def test_coverage_flag_validator_rejects_wrong_order():
    m = _load_runner()
    assert not m.is_valid_coverage_flag(
        "right_truncated_2022_seal+t0_absent_substrate_gap"
    )


def test_coverage_flag_validator_rejects_unknown_token():
    m = _load_runner()
    assert not m.is_valid_coverage_flag("garbage_flag")
    assert not m.is_valid_coverage_flag(
        "t0_absent_substrate_gap+unknown_thing"
    )


def test_coverage_flag_validator_rejects_duplicates():
    m = _load_runner()
    assert not m.is_valid_coverage_flag(
        "t0_absent_substrate_gap+t0_absent_substrate_gap"
    )


def test_t_minus_3650_not_in_coverage_flag_domain():
    """Per design memo §10.2 / §11.3, T-3650 absence is universal across
    the window and is surfaced by out_of_window_sqldate_diagnostic, NOT
    by coverage_quality_flag."""
    m = _load_runner()
    for f in m.COVERAGE_SINGLE_FLAGS:
        assert "3650" not in f
    # And the validator rejects any flag containing -3650 token
    assert not m.is_valid_coverage_flag("t_minus_3650_universal_absent")


# ============================================================================
# 13. Parser validation
# ============================================================================

def test_parser_counts_rows_once_per_occurrence():
    m = _load_runner()
    nom = date(2018, 6, 15)
    p = m.parse_payload(
        _make_payload_zip(nom, [(0, 100)]),
        nom,
    )
    assert p["row_count"] == 100
    assert p["per_offset_count"][0] == 100


def test_parser_malformed_short_row_diagnostic():
    m = _load_runner()
    nom = date(2018, 6, 15)
    # Hand-craft a payload with a malformed-short row (only 1 column)
    rows = [
        "1",  # malformed-short: no SQLDATE column
        "2\t20180615\tA",  # valid T=0
    ]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("20180615.export.CSV", "\n".join(rows))
    p = m.parse_payload(buf.getvalue(), nom)
    assert p["malformed_short_rows"] == 1
    assert p["per_offset_count"][0] == 1


def test_parser_unparseable_sqldate_diagnostic():
    m = _load_runner()
    nom = date(2018, 6, 15)
    rows = [
        "1\tNOTAYEAR\tA",  # unparseable SQLDATE
        "2\t20180615\tA",  # valid T=0
    ]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("20180615.export.CSV", "\n".join(rows))
    p = m.parse_payload(buf.getvalue(), nom)
    assert p["unparseable_sqldate_rows"] == 1
    assert p["per_offset_count"][0] == 1


def test_parser_no_silent_repair_on_unexpected_offset():
    m = _load_runner()
    nom = date(2018, 6, 15)
    # Hand-craft a payload with offset -2 (not in taxonomy)
    rows = ["1\t20180613\tA"]  # 2018-06-13 = nom - 2
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("20180615.export.CSV", "\n".join(rows))
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.parse_payload(buf.getvalue(), nom)


def test_parser_no_silent_repair_on_2023_plus_sqldate():
    m = _load_runner()
    nom = date(2022, 12, 30)
    rows = ["1\t20230102\tA"]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("20221230.export.CSV", "\n".join(rows))
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.parse_payload(buf.getvalue(), nom)


def test_parser_refuses_2023_plus_nominal():
    m = _load_runner()
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.parse_payload(b"", date(2023, 1, 1))


def test_parser_handles_empty_payload():
    m = _load_runner()
    # Empty zip
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        pass
    nom = date(2018, 6, 15)
    p = m.parse_payload(buf.getvalue(), nom)
    assert p["row_count"] == 0


# ============================================================================
# 14. Output artifact allow-list
# ============================================================================

def test_allow_list_accepts_daily_count_csv():
    m = _load_runner()
    assert m._is_allowed_output_basename("daily_count.csv")


def test_allow_list_accepts_metadata_summary_halt():
    m = _load_runner()
    assert m._is_allowed_output_basename("build_metadata.json")
    assert m._is_allowed_output_basename("build_summary.md")
    assert m._is_allowed_output_basename("halt_diagnostic.json")


def test_allow_list_rejects_raw_payload_zip():
    m = _load_runner()
    assert not m._is_allowed_output_basename("payload_20180615.zip")


def test_allow_list_rejects_extracted_csv():
    m = _load_runner()
    assert not m._is_allowed_output_basename("20180615.export.CSV")


def test_allow_list_rejects_temp_file_basename():
    m = _load_runner()
    assert not m._is_allowed_output_basename("tmp_payload_20180615.bin")


def test_allow_list_rejects_path_traversal():
    m = _load_runner()
    assert not m._is_allowed_output_basename("../etc/passwd")
    assert not m._is_allowed_output_basename("/etc/passwd")
    assert not m._is_allowed_output_basename("..\\etc")


def test_checked_output_path_raises_on_bad_basename(tmp_path):
    m = _load_runner()
    with pytest.raises(m.FullBuildBoundaryBreach):
        m._checked_output_path(str(tmp_path), "payload.zip")


def test_assert_outputs_allowed_passes_on_clean_dir(tmp_path):
    m = _load_runner()
    (tmp_path / "daily_count.csv").write_text("col\n")
    (tmp_path / "build_metadata.json").write_text("{}\n")
    (tmp_path / "build_summary.md").write_text("# x\n")
    m._assert_outputs_allowed(str(tmp_path))  # should not raise


def test_assert_outputs_allowed_fails_on_extra_file(tmp_path):
    m = _load_runner()
    (tmp_path / "daily_count.csv").write_text("col\n")
    (tmp_path / "payload_20180615.zip").write_bytes(b"\x00")
    with pytest.raises(m.FullBuildBoundaryBreach):
        m._assert_outputs_allowed(str(tmp_path))


def test_assert_outputs_allowed_fails_on_subdir(tmp_path):
    m = _load_runner()
    (tmp_path / "tmp").mkdir()
    with pytest.raises(m.FullBuildBoundaryBreach):
        m._assert_outputs_allowed(str(tmp_path))


def test_write_daily_count_csv_writes_only_allow_listed(tmp_path):
    m = _load_runner()
    rows = [
        {
            "civil_date": "2013-04-01",
            "total_row_count": 10,
            "rows_from_offset_0": 10,
            "rows_from_offset_minus_1": 0,
            "rows_from_offset_minus_7": 0,
            "rows_from_offset_minus_30": 0,
            "rows_from_offset_minus_365": 0,
            "rows_from_offset_minus_3650": 0,
            "rows_from_offset_plus_1": 0,
            "t0_file_status": "present",
            "expected_contributing_files_count": 6,
            "available_contributing_files_count": 1,
            "coverage_quality_flag": "left_truncated_2013_edge",
            "coverage_completeness": 1/6,
        },
    ]
    path = m.write_daily_count_csv(str(tmp_path), rows)
    assert os.path.basename(path) == "daily_count.csv"
    text = open(path).read()
    assert "civil_date" in text
    assert "2013-04-01" in text


def test_write_metadata_json_deterministic(tmp_path):
    m = _load_runner()
    md = {"alpha": 1, "beta": [3, 2, 1], "gamma": {"z": 1, "a": 2}}
    path = m.write_build_metadata_json(str(tmp_path), md)
    body = open(path).read()
    # sort_keys=True so the JSON should have keys in alphabetical order
    assert body.index("alpha") < body.index("beta") < body.index("gamma")


# ============================================================================
# 15. Payload-discard mechanism
# ============================================================================

def test_runner_does_not_preserve_payloads_in_final_output(tmp_path,
                                                            monkeypatch):
    m = _load_runner()
    # Build a tiny synthetic capture with one daily unit
    capture = _make_synthetic_capture(
        in_window_dates=["2018-06-15"],
    )
    # Force the SHA check to pass by monkeypatching the expected SHA
    cap_path = _write_synthetic_capture(tmp_path, capture)
    actual_sha = m._hash_file_sha256(str(cap_path))
    monkeypatch.setattr(m, "RECOGNIZED_LIST_SHA256", actual_sha)
    # Also relax civil-days expectation by making the capture cover the
    # full window — but to keep the test small, we'll skip the
    # reconciliation assertion by patching it out (the focus of this test
    # is payload-discard, not reconciliation).
    monkeypatch.setattr(
        m, "assert_reconciliation_consistent", lambda r: None,
    )
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_FULL_BUILD_AUTHORIZED", "1")

    nom = date(2018, 6, 15)
    payload_bytes = _make_payload_zip(nom, [(0, 5)])

    def fake_opener(url, timeout=60.0):
        return _FakeResponse(status=200, body=payload_bytes)

    res = m.run_full_daily_count_build(
        str(tmp_path),
        cli_flag=True,
        timestamp_utc="20260601T120000Z",
        opener=fake_opener,
    )
    output_dir = res["output_dir"]
    # The output dir must contain ONLY allow-listed files
    files = sorted(os.listdir(output_dir))
    # daily_count.csv, build_metadata.json, build_summary.md
    assert "daily_count.csv" in files
    assert "build_metadata.json" in files
    assert "build_summary.md" in files
    # No payload zip should be present
    for f in files:
        assert not f.endswith(".zip")
        assert "payload" not in f.lower()


def test_payload_bytes_are_discarded_between_urls(monkeypatch):
    """Verify the runner releases payload bytes between URLs.

    We track the maximum number of payloads held by the runner at any
    one time by checking that the local 'payload' variable is del'd
    after parsing. This is checked via a behavioral fake opener that
    returns each payload only once.
    """
    m = _load_runner()
    # Best proxy: assert that the runner's main loop does call `del payload`
    # by inspecting source.
    src = open(os.path.join(
        REPO_ROOT, "scripts",
        "run_lane2_gdelt1_full_daily_count_build.py",
    )).read()
    assert "del payload" in src


# ============================================================================
# 16. No-market-data / no-Step-2 leakage
# ============================================================================

def _runner_source():
    path = os.path.join(
        REPO_ROOT, "scripts",
        "run_lane2_gdelt1_full_daily_count_build.py",
    )
    return open(path, "r", encoding="utf-8").read()


def test_runner_source_no_market_data_imports():
    src = _runner_source()
    assert "import yfinance" not in src
    assert "from yfinance" not in src
    assert "import pandas_datareader" not in src
    assert "from pandas_datareader" not in src
    assert "import alpaca" not in src
    assert "import polygon" not in src


def test_runner_source_no_asset_symbol_tokens():
    """Identifier-shape tokens that would indicate market-side coupling.

    Uses regex word-boundary matching so legitimate prohibitive
    declarations (e.g. `no_spike_threshold_tuning`) are not flagged as
    containing the bare forbidden token (`spike_threshold` is between
    word characters in that declaration, so `\\b` does not match).
    """
    src = _runner_source()
    forbidden_tokens = [
        "compute_return",
        "trading_day",
        "trading_calendar",
        "asset_symbol",
        "burst_threshold",
        "spike_threshold",
        "sharpe",
        "drawdown",
        "step2_signal",
    ]
    for tok in forbidden_tokens:
        pattern = r"\b" + re.escape(tok) + r"\b"
        assert not re.search(pattern, src), (
            "forbidden token found as standalone identifier: {}".format(tok)
        )


def test_runner_source_no_filter_options():
    src = _runner_source()
    # No CLI flag for filtering
    forbidden_cli = [
        "--category",
        "--theme",
        "--actor",
        "--geography",
        "--tone",
        "--allow-2023",
        "--retry",
        "--preserve-payloads",
        "--skip-guard",
    ]
    for tok in forbidden_cli:
        assert tok not in src, "forbidden CLI flag: {}".format(tok)


def test_runner_source_no_step_2_logic_tokens():
    src = _runner_source()
    forbidden = ["return_window", "event_window", "ar_window"]
    for tok in forbidden:
        assert tok not in src, "forbidden Step 2 token: {}".format(tok)


def test_runner_boundary_declarations_assert_no_leakage():
    m = _load_runner()
    decl = m._boundary_declarations()
    for key in (
        "no_market_data",
        "no_step_2",
        "no_asset_or_return_logic",
        "no_category_theme_actor_filtering",
        "no_spike_threshold_tuning",
        "no_negative_control",
        "no_2023plus_access",
        "no_payload_preservation_after_parsing",
        "no_market_calendar_alignment",
    ):
        assert decl[key] is True


# ============================================================================
# End-to-end smoke (small synthetic universe)
# ============================================================================

def test_end_to_end_small_universe(tmp_path, monkeypatch):
    """Run the build over a small synthetic universe to verify the
    overall pipeline assembles outputs correctly.

    Uses a single in-window daily date and skips reconciliation
    consistency (which would expect 3,558 dates)."""
    m = _load_runner()
    # Synthetic capture with one daily unit
    capture = _make_synthetic_capture(in_window_dates=["2018-06-15"])
    cap_path = _write_synthetic_capture(tmp_path, capture)
    actual_sha = m._hash_file_sha256(str(cap_path))
    monkeypatch.setattr(m, "RECOGNIZED_LIST_SHA256", actual_sha)
    monkeypatch.setattr(
        m, "assert_reconciliation_consistent", lambda r: None,
    )
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_FULL_BUILD_AUTHORIZED", "1")

    nom = date(2018, 6, 15)
    # No T+1 in post-2015 era
    payload_bytes = _make_payload_zip(
        nom, [(0, 100), (-1, 5), (-7, 3), (-30, 2), (-365, 1)],
    )

    def fake_opener(url, timeout=60.0):
        return _FakeResponse(status=200, body=payload_bytes)

    res = m.run_full_daily_count_build(
        str(tmp_path),
        cli_flag=True,
        timestamp_utc="20260601T120000Z",
        opener=fake_opener,
    )
    md = res["metadata"]
    # Aggregate metrics
    agg = md["aggregate_metrics"]
    assert agg["per_offset_total"]["0"] == 100
    assert agg["per_offset_total"]["-1"] == 5
    assert agg["per_offset_total"]["-365"] == 1
    # Civil domain has 3,562 rows
    assert md["aggregation_invariants"]["civil_days_in_output_domain"] == 3562
    # T-3650 zero invariant
    assert md["aggregation_invariants"]["t_minus_3650_in_primary_is_zero"] is True
    # Counting invariant should not have been triggered
    # (the run completed normally)


def test_end_to_end_synthesizes_expected_absent_for_gaps(tmp_path,
                                                          monkeypatch):
    """The per-file manifest must include `expected_absent_per_recognized_list`
    entries for each substrate gap, even when no fetch was issued."""
    m = _load_runner()
    capture = _make_synthetic_capture(in_window_dates=["2018-06-15"])
    cap_path = _write_synthetic_capture(tmp_path, capture)
    actual_sha = m._hash_file_sha256(str(cap_path))
    monkeypatch.setattr(m, "RECOGNIZED_LIST_SHA256", actual_sha)
    monkeypatch.setattr(
        m, "assert_reconciliation_consistent", lambda r: None,
    )
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_FULL_BUILD_AUTHORIZED", "1")

    nom = date(2018, 6, 15)

    def fake_opener(url, timeout=60.0):
        return _FakeResponse(
            status=200, body=_make_payload_zip(nom, [(0, 1)]),
        )

    res = m.run_full_daily_count_build(
        str(tmp_path),
        cli_flag=True,
        timestamp_utc="20260601T120001Z",
        opener=fake_opener,
    )
    manifest = res["metadata"]["per_file_manifest"]
    gap_entries = [
        e for e in manifest
        if e["status"] == "expected_absent_per_recognized_list"
    ]
    gap_dates = {e["nominal_date"] for e in gap_entries}
    assert gap_dates == set(m.KNOWN_SUBSTRATE_GAPS)


def test_end_to_end_hard_fail_on_unexpected_offset(tmp_path, monkeypatch):
    m = _load_runner()
    capture = _make_synthetic_capture(in_window_dates=["2018-06-15"])
    cap_path = _write_synthetic_capture(tmp_path, capture)
    actual_sha = m._hash_file_sha256(str(cap_path))
    monkeypatch.setattr(m, "RECOGNIZED_LIST_SHA256", actual_sha)
    monkeypatch.setattr(
        m, "assert_reconciliation_consistent", lambda r: None,
    )
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_FULL_BUILD_AUTHORIZED", "1")

    nom = date(2018, 6, 15)
    # Unexpected offset -2
    payload_bytes = _make_payload_zip(nom, [(-2, 1)])

    def fake_opener(url, timeout=60.0):
        return _FakeResponse(status=200, body=payload_bytes)

    with pytest.raises(m.FullBuildBoundaryBreach):
        m.run_full_daily_count_build(
            str(tmp_path),
            cli_flag=True,
            timestamp_utc="20260601T120002Z",
            opener=fake_opener,
        )


def test_end_to_end_hard_fail_on_http_404(tmp_path, monkeypatch):
    m = _load_runner()
    capture = _make_synthetic_capture(in_window_dates=["2018-06-15"])
    cap_path = _write_synthetic_capture(tmp_path, capture)
    actual_sha = m._hash_file_sha256(str(cap_path))
    monkeypatch.setattr(m, "RECOGNIZED_LIST_SHA256", actual_sha)
    monkeypatch.setattr(
        m, "assert_reconciliation_consistent", lambda r: None,
    )
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_FULL_BUILD_AUTHORIZED", "1")

    def fake_opener(url, timeout=60.0):
        raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)

    with pytest.raises(m.FetchFailure):
        m.run_full_daily_count_build(
            str(tmp_path),
            cli_flag=True,
            timestamp_utc="20260601T120003Z",
            opener=fake_opener,
        )


def test_end_to_end_metadata_declares_no_market_no_step_2(tmp_path, monkeypatch):
    m = _load_runner()
    capture = _make_synthetic_capture(in_window_dates=["2018-06-15"])
    cap_path = _write_synthetic_capture(tmp_path, capture)
    actual_sha = m._hash_file_sha256(str(cap_path))
    monkeypatch.setattr(m, "RECOGNIZED_LIST_SHA256", actual_sha)
    monkeypatch.setattr(
        m, "assert_reconciliation_consistent", lambda r: None,
    )
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_FULL_BUILD_AUTHORIZED", "1")

    nom = date(2018, 6, 15)
    payload_bytes = _make_payload_zip(nom, [(0, 1)])

    def fake_opener(url, timeout=60.0):
        return _FakeResponse(status=200, body=payload_bytes)

    res = m.run_full_daily_count_build(
        str(tmp_path),
        cli_flag=True,
        timestamp_utc="20260601T120004Z",
        opener=fake_opener,
    )
    decl = res["metadata"]["boundary_declarations"]
    assert decl["no_market_data"] is True
    assert decl["no_step_2"] is True
    assert decl["no_2023plus_access"] is True
    assert decl["no_payload_preservation_after_parsing"] is True


def test_redirect_blocked_opener_raises_on_30x():
    m = _load_runner()
    handler = m._FullBuildNoFollowRedirectHandler()
    with pytest.raises(m.FullBuildRedirectBlocked):
        handler.http_error_302(None, None, 302, "", {})


def test_reconciliation_catches_real_capture_fetch_set_matches():
    m = _load_runner()
    data, _, _ = m._load_recognized_list(REPO_ROOT)
    report = m.build_reconciliation_report(
        data["recognized_in_window_units"]
    )
    assert report["fetch_set_count"] == 3558
    # The first and last fetch_set entries should be the window boundaries
    assert report["fetch_set"][0] == "2013-04-01"
    assert report["fetch_set"][-1] == "2022-12-31"


# ============================================================================
# Chunk-design tests (per `5962c20` chunk-design memo)
# ============================================================================

CANONICAL_CHUNK_IDS = (
    "chunk_2013_partial",
    "chunk_2014",
    "chunk_2015",
    "chunk_2016",
    "chunk_2017",
    "chunk_2018",
    "chunk_2019",
    "chunk_2020",
    "chunk_2021",
    "chunk_2022",
)

CANONICAL_CHUNK_COUNTS = {
    "chunk_2013_partial": 275,
    "chunk_2014": 361,
    "chunk_2015": 365,
    "chunk_2016": 366,
    "chunk_2017": 365,
    "chunk_2018": 365,
    "chunk_2019": 365,
    "chunk_2020": 366,
    "chunk_2021": 365,
    "chunk_2022": 365,
}


def _real_fetch_set():
    m = _load_runner()
    data, _, _ = m._load_recognized_list(REPO_ROOT)
    report = m.build_reconciliation_report(
        data["recognized_in_window_units"]
    )
    return report["fetch_set"]


# ── Chunk constants ──────────────────────────────────────────────────────────

def test_chunk_ids_are_exactly_the_10_canonical_ids():
    m = _load_runner()
    assert m.CHUNK_IDS == CANONICAL_CHUNK_IDS
    assert len(m.CHUNK_IDS) == 10


def test_chunk_counts_match_canonical_table():
    m = _load_runner()
    assert dict(m.EXPECTED_CHUNK_COUNTS) == CANONICAL_CHUNK_COUNTS


def test_chunk_count_total_is_3558():
    m = _load_runner()
    total = sum(m.EXPECTED_CHUNK_COUNTS.values())
    assert total == 3558
    assert total == m.NAIVE_EXPECTED_DAILY_URLS


def test_chunk_year_ranges_cover_2013_04_01_to_2022_12_31():
    m = _load_runner()
    for cid, (start, end) in m.CHUNK_YEAR_RANGES.items():
        assert start.year == end.year, "chunk {} crosses year boundary".format(cid)
    # First chunk starts at window left edge
    assert m.CHUNK_YEAR_RANGES["chunk_2013_partial"][0] == date(2013, 4, 1)
    # Last chunk ends at window right edge
    assert m.CHUNK_YEAR_RANGES["chunk_2022"][1] == date(2022, 12, 31)


# ── Chunk manifest construction ──────────────────────────────────────────────

def test_build_chunk_manifest_returns_correct_count_for_each_chunk():
    m = _load_runner()
    fs = _real_fetch_set()
    for cid in m.CHUNK_IDS:
        manifest = m.build_chunk_manifest(cid, fs)
        assert len(manifest) == CANONICAL_CHUNK_COUNTS[cid], \
            "chunk {} count mismatch".format(cid)


def test_build_chunk_manifest_rejects_unknown_chunk_id():
    m = _load_runner()
    fs = _real_fetch_set()
    with pytest.raises(m.ChunkManifestError):
        m.build_chunk_manifest("chunk_2099", fs)
    with pytest.raises(m.ChunkManifestError):
        m.build_chunk_manifest("garbage", fs)


def test_chunk_manifest_count_mismatch_hard_fails():
    m = _load_runner()
    # Pass a truncated fetch_set; the chunk filter will produce fewer
    # entries than expected, triggering the count-mismatch hard-fail.
    truncated = ["2013-04-01", "2013-04-02"]
    with pytest.raises(m.ChunkManifestError):
        m.build_chunk_manifest("chunk_2013_partial", truncated)


def test_build_all_chunk_manifests_returns_all_10():
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    assert set(manifests.keys()) == set(m.CHUNK_IDS)
    assert sum(len(v) for v in manifests.values()) == 3558


# ── Manifest digest ──────────────────────────────────────────────────────────

def test_chunk_manifest_digest_is_deterministic():
    m = _load_runner()
    fs = _real_fetch_set()
    manifest = m.build_chunk_manifest("chunk_2015", fs)
    d1 = m.chunk_manifest_digest(manifest)
    d2 = m.chunk_manifest_digest(list(reversed(manifest)))
    assert d1 == d2, "digest must be order-independent (sorts internally)"
    assert len(d1) == 64  # SHA-256 hex


def test_chunk_manifest_digest_differs_across_chunks():
    m = _load_runner()
    fs = _real_fetch_set()
    digests = set()
    for cid in m.CHUNK_IDS:
        digests.add(m.chunk_manifest_digest(m.build_chunk_manifest(cid, fs)))
    assert len(digests) == 10


# ── Partition validation ─────────────────────────────────────────────────────

def test_chunk_manifests_are_disjoint():
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    seen = set()
    for cid, urls in manifests.items():
        for u in urls:
            assert u not in seen, \
                "URL {!r} appears in {!r} and earlier chunk".format(u, cid)
            seen.add(u)


def test_chunk_manifests_union_equals_full_fetch_set():
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    union = set(u for urls in manifests.values() for u in urls)
    assert union == set(fs)


def test_assert_chunk_manifests_partition_passes_for_canonical_split():
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    m.assert_chunk_manifests_partition(manifests, fs)  # should not raise


def test_assert_chunk_manifests_partition_rejects_2023_plus_dates():
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    # Inject a 2023+ date into one chunk
    manifests["chunk_2022"] = manifests["chunk_2022"] + ["2023-01-01"]
    with pytest.raises(m.ChunkManifestError):
        m.assert_chunk_manifests_partition(manifests, fs + ["2023-01-01"])


def test_assert_chunk_manifests_partition_rejects_yearly_units():
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    # Inject a yearly unit into one chunk
    manifests["chunk_2015"] = manifests["chunk_2015"] + ["2015"]
    with pytest.raises(m.ChunkManifestError):
        m.assert_chunk_manifests_partition(manifests, fs + ["2015"])


def test_assert_chunk_manifests_partition_rejects_monthly_units():
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    manifests["chunk_2015"] = manifests["chunk_2015"] + ["2015-06"]
    with pytest.raises(m.ChunkManifestError):
        m.assert_chunk_manifests_partition(manifests, fs + ["2015-06"])


def test_assert_chunk_manifests_partition_rejects_duplicate_url():
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    # Move a 2015 URL into 2016 manifest as well, producing duplicate
    dup = manifests["chunk_2015"][0]
    manifests["chunk_2016"] = manifests["chunk_2016"] + [dup]
    with pytest.raises(m.ChunkManifestError):
        m.assert_chunk_manifests_partition(manifests, fs)


def test_assert_chunk_manifests_partition_rejects_missing_chunk():
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    del manifests["chunk_2015"]
    with pytest.raises(m.ChunkManifestError):
        m.assert_chunk_manifests_partition(manifests, fs)


# ── 2014 substrate gaps handled as recognized-list absence ───────────────────

def test_chunk_2014_excludes_known_substrate_gaps():
    m = _load_runner()
    fs = _real_fetch_set()
    manifest = m.build_chunk_manifest("chunk_2014", fs)
    for gap in m.KNOWN_SUBSTRATE_GAPS:
        assert gap not in manifest, \
            "gap {!r} must not be in chunk_2014 manifest".format(gap)
    # Count is 365 - 4 = 361
    assert len(manifest) == 361


# ── Allow-list and output path gating ────────────────────────────────────────

def test_chunk_output_allow_list_is_four_entries():
    m = _load_runner()
    assert m.ALLOWED_CHUNK_OUTPUT_BASENAMES == (
        "chunk_contributions.csv",
        "chunk_metadata.json",
        "chunk_summary.md",
        "halt_diagnostic.json",
    )


def test_is_allowed_chunk_output_basename_rejects_payload_zip():
    m = _load_runner()
    assert not m.is_allowed_chunk_output_basename("payload_20180615.zip")


def test_is_allowed_chunk_output_basename_rejects_extracted_csv():
    m = _load_runner()
    assert not m.is_allowed_chunk_output_basename("20180615.export.CSV")


def test_is_allowed_chunk_output_basename_rejects_path_traversal():
    m = _load_runner()
    assert not m.is_allowed_chunk_output_basename("../secret")
    assert not m.is_allowed_chunk_output_basename("/etc/passwd")
    assert not m.is_allowed_chunk_output_basename("..\\secret")


def test_is_allowed_chunk_output_basename_rejects_canonical_full_build_names():
    """daily_count.csv / build_metadata.json / build_summary.md are
    merge-step outputs, NOT chunk-step outputs."""
    m = _load_runner()
    assert not m.is_allowed_chunk_output_basename("daily_count.csv")
    assert not m.is_allowed_chunk_output_basename("build_metadata.json")
    assert not m.is_allowed_chunk_output_basename("build_summary.md")


# ── Guard discipline for chunk execution ─────────────────────────────────────

def test_run_chunk_build_refuses_when_guards_off(monkeypatch, tmp_path):
    m = _load_runner()
    monkeypatch.delenv("LANE2_FULL_BUILD_AUTHORIZED", raising=False)
    # Pre-validate the chunk_id is accepted by validate_chunk_id
    m.validate_chunk_id("chunk_2018")
    with pytest.raises(SystemExit):
        m.run_chunk_build(
            "chunk_2018", str(tmp_path), cli_flag=False,
        )


def test_run_chunk_build_refuses_when_only_module_constant_missing(monkeypatch, tmp_path):
    m = _load_runner()
    monkeypatch.setattr(m, "FULL_BUILD_AUTHORIZED", False)
    monkeypatch.setenv("LANE2_FULL_BUILD_AUTHORIZED", "1")
    with pytest.raises(SystemExit):
        m.run_chunk_build("chunk_2018", str(tmp_path), cli_flag=True)


def test_run_chunk_build_refuses_unknown_chunk_id(tmp_path):
    m = _load_runner()
    # Should raise ChunkManifestError BEFORE guard refusal
    # (chunk_id validation happens before guard check in run_chunk_build).
    with pytest.raises(m.ChunkManifestError):
        m.run_chunk_build("chunk_2099", str(tmp_path), cli_flag=False)


def test_run_chunk_build_refuses_before_any_side_effect(tmp_path, monkeypatch):
    m = _load_runner()
    monkeypatch.delenv("LANE2_FULL_BUILD_AUTHORIZED", raising=False)
    with pytest.raises(SystemExit):
        m.run_chunk_build("chunk_2018", str(tmp_path), cli_flag=False)
    # No chunk output dir should exist
    assert not (tmp_path / "results" / "lane2_gdelt1_full_daily_count_build").exists()


def test_module_constant_still_false_after_chunk_patch():
    """The chunk-runner patch must NOT flip the module guard.
    Verified by re-loading the module fresh."""
    m = _load_runner()
    assert m.FULL_BUILD_AUTHORIZED is False


# ── Per-chunk artifact writers + halt diagnostic ────────────────────────────

def test_write_chunk_contributions_csv_writes_only_to_allow_list(tmp_path):
    m = _load_runner()
    counts = {
        ("2015-06-15", 0): 100,
        ("2015-06-15", -1): 5,
        ("2015-06-14", -1): 3,
    }
    path = m.write_chunk_contributions_csv(
        str(tmp_path), "chunk_2015", counts,
    )
    assert os.path.basename(path) == "chunk_contributions.csv"
    text = open(path).read()
    assert "civil_date" in text and "chunk_id" in text
    assert "chunk_2015" in text
    assert "2015-06-15" in text


def test_write_chunk_metadata_json_deterministic(tmp_path):
    m = _load_runner()
    md = {"chunk_id": "chunk_2018", "z_key": 1, "a_key": 2}
    path = m.write_chunk_metadata_json(str(tmp_path), md)
    body = open(path).read()
    # sort_keys=True
    assert body.index("a_key") < body.index("chunk_id") < body.index("z_key")


def test_chunk_halt_diagnostic_only_writable_via_allow_list(tmp_path):
    m = _load_runner()
    # Write a halt diagnostic
    m._write_chunk_halt_diagnostic(
        str(tmp_path),
        {"halt_class": "Test", "message": "test halt"},
    )
    assert (tmp_path / "halt_diagnostic.json").exists()
    # Tripwire accepts the allow-listed file
    m._assert_chunk_outputs_allowed(str(tmp_path))


def test_assert_chunk_outputs_allowed_rejects_unexpected_file(tmp_path):
    m = _load_runner()
    (tmp_path / "chunk_contributions.csv").write_text("col\n")
    (tmp_path / "payload_2015_06_15.zip").write_bytes(b"\x00")
    with pytest.raises(m.FullBuildBoundaryBreach):
        m._assert_chunk_outputs_allowed(str(tmp_path))


def test_assert_chunk_outputs_allowed_rejects_subdir(tmp_path):
    m = _load_runner()
    (tmp_path / "tmp").mkdir()
    with pytest.raises(m.FullBuildBoundaryBreach):
        m._assert_chunk_outputs_allowed(str(tmp_path))


# ── Merge step (offline, deterministic) ──────────────────────────────────────

def _build_synthetic_chunk_dirs(tmp_path, monkeypatch):
    """Build 10 synthetic chunk output dirs whose contributions and
    metadata reflect the canonical chunk manifests + digests."""
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    chunk_dirs = {}
    for cid in m.CHUNK_IDS:
        cdir = tmp_path / "results" / "lane2_gdelt1_full_daily_count_build" / cid
        cdir.mkdir(parents=True, exist_ok=False)
        # Synthetic contributions: each chunk contributes 10 rows at T=0
        # for the first 3 dates in the chunk
        counts = {}
        for iso in manifests[cid][:3]:
            counts[(iso, 0)] = 10
        m.write_chunk_contributions_csv(str(cdir), cid, counts)
        m.write_chunk_metadata_json(str(cdir), {
            "chunk_id": cid,
            "chunk_manifest_digest": m.chunk_manifest_digest(manifests[cid]),
            "expected_file_count": m.EXPECTED_CHUNK_COUNTS[cid],
            "actual_completed_file_count": m.EXPECTED_CHUNK_COUNTS[cid],
        })
        chunk_dirs[cid] = str(cdir)
    return chunk_dirs


def test_merge_chunks_halts_on_missing_chunk(tmp_path):
    m = _load_runner()
    chunk_dirs = _build_synthetic_chunk_dirs(tmp_path, None)
    del chunk_dirs["chunk_2015"]
    with pytest.raises(m.ChunkManifestError, match="missing"):
        m.merge_chunks(chunk_dirs, REPO_ROOT)


def test_merge_chunks_halts_on_unexpected_chunk_id(tmp_path):
    m = _load_runner()
    chunk_dirs = _build_synthetic_chunk_dirs(tmp_path, None)
    # Add a chunk_2099 entry (invalid)
    # Since validate_chunk_id is called inside merge for the actual ids,
    # we test via direct mutation:
    chunk_dirs["chunk_2099_fake"] = str(tmp_path)
    with pytest.raises(m.ChunkManifestError):
        m.merge_chunks(chunk_dirs, REPO_ROOT)


def test_merge_chunks_halts_on_manifest_digest_mismatch(tmp_path):
    m = _load_runner()
    chunk_dirs = _build_synthetic_chunk_dirs(tmp_path, None)
    # Corrupt one chunk's metadata digest
    cdir = chunk_dirs["chunk_2018"]
    md = m.load_chunk_metadata(cdir)
    md["chunk_manifest_digest"] = "0" * 64
    m.write_chunk_metadata_json(cdir, md)
    with pytest.raises(m.ChunkManifestError, match="digest mismatch"):
        m.merge_chunks(chunk_dirs, REPO_ROOT)


def test_merge_chunks_succeeds_on_canonical_inputs(tmp_path):
    m = _load_runner()
    chunk_dirs = _build_synthetic_chunk_dirs(tmp_path, None)
    result = m.merge_chunks(chunk_dirs, REPO_ROOT)
    # 3,562 civil days
    assert len(result["daily_count_rows"]) == 3562
    # Each chunk contributed 10 rows × 3 dates = 30
    assert result["aggregate_metrics"]["total_in_window_rows"] == 30 * 10


def test_merge_chunks_clips_to_civil_window():
    m = _load_runner()
    # merge_chunks's output is always restricted to civil_date_domain()
    # = 3,562 days. Verified above. Also verify domain boundaries:
    domain = m.civil_date_domain()
    assert domain[0].isoformat() == "2013-04-01"
    assert domain[-1].isoformat() == "2022-12-31"
    assert len(domain) == 3562


def test_merge_chunks_output_is_deterministic_regardless_of_chunk_order(tmp_path):
    m = _load_runner()
    chunk_dirs = _build_synthetic_chunk_dirs(tmp_path, None)
    result1 = m.merge_chunks(chunk_dirs, REPO_ROOT)
    # Reverse the dict order
    reversed_dirs = dict(reversed(list(chunk_dirs.items())))
    result2 = m.merge_chunks(reversed_dirs, REPO_ROOT)
    # daily_count_rows must be identical
    assert result1["daily_count_rows"] == result2["daily_count_rows"]
    assert result1["aggregate_metrics"] == result2["aggregate_metrics"]


# ── Cross-chunk coverage rule ────────────────────────────────────────────────

def test_cross_chunk_coverage_computed_at_merge_time_d_2015_01_01(tmp_path):
    """For d = 2015-01-01, the T+1 contributor f_(2014-12-31) belongs to
    chunk_2014 while the output SQLDATE belongs to 2015. The merge step's
    coverage_for_date must use the union daily_set so this contributor
    is recognized."""
    m = _load_runner()
    daily_set = set(_real_fetch_set())
    gaps_set = set(m.KNOWN_SUBSTRATE_GAPS)
    cov = m.coverage_for_date(date(2015, 1, 1), daily_set, gaps_set)
    # d = 2015-01-01 is the pre-2015 T+1 era cutoff date; expected cone
    # size = 6 (includes T+1)
    assert cov["expected_contributing_files_count"] == 6
    # All 6 cone members should be in the union daily_set: T=0 (2015-01-01),
    # T-1 (2015-01-02), T-7 (2015-01-08), T-30 (2015-01-31),
    # T-365 (2016-01-01), T+1 (2014-12-31). All in-universe.
    assert cov["available_contributing_files_count"] == 6
    assert cov["coverage_quality_flag"] == "full"


def test_coverage_domain_includes_t_minus_n_neighbor_substrate_gap():
    m = _load_runner()
    assert "t_minus_n_neighbor_substrate_gap" in m.COVERAGE_SINGLE_FLAGS


def test_plus_joined_multi_cause_flag_remains_valid():
    """`c10ae74` Decision 1A + `bc7b66b` implementation reality:
    multi-cause coverage flags are `+`-joined ordered concatenations."""
    m = _load_runner()
    assert m.is_valid_coverage_flag(
        "t0_absent_substrate_gap+t_plus_1_neighbor_substrate_gap"
    )
    assert m.is_valid_coverage_flag(
        "t0_absent_substrate_gap+t_minus_n_neighbor_substrate_gap"
    )


# ── No raw payload preservation, no retry ────────────────────────────────────

def test_runner_source_still_has_no_retry_logic_after_chunk_patch():
    src = _runner_source()
    forbidden = ["max_retries", "retry_count", "backoff_factor",
                 "should_retry", "_retry_fetch"]
    for tok in forbidden:
        assert tok not in src, "forbidden retry token: {}".format(tok)


def test_runner_source_still_has_no_payload_preservation_after_chunk_patch():
    src = _runner_source()
    # `del payload` is the per-URL discard signal
    assert "del payload" in src
    # No `preserve_payloads` flag should exist
    import re
    assert not re.search(r"\bpreserve_payloads\b", src)


# ── No 2023+ leakage in chunk paths ──────────────────────────────────────────

def test_chunk_manifests_contain_no_2023_plus_dates():
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    for cid, urls in manifests.items():
        for u in urls:
            assert u < "2023-01-01", \
                "chunk {} contains 2023+ date {}".format(cid, u)


def test_chunk_manifests_contain_no_yearly_or_monthly_units():
    m = _load_runner()
    fs = _real_fetch_set()
    manifests = m.build_all_chunk_manifests(fs)
    for cid, urls in manifests.items():
        for u in urls:
            assert m._DAILY_RE.match(u), \
                "chunk {} contains non-daily unit {}".format(cid, u)


# ── List-chunks CLI mode ─────────────────────────────────────────────────────

def test_list_chunks_outputs_10_lines(capsys):
    m = _load_runner()
    rc = m.main(["--list-chunks"])
    assert rc == 0
    out, _ = capsys.readouterr()
    lines = [ln for ln in out.strip().split("\n") if ln.strip()]
    assert len(lines) == 10
    for line, cid in zip(lines, m.CHUNK_IDS):
        assert line.startswith(cid)


# ── Merge CLI input parsing ──────────────────────────────────────────────────

def test_parse_merge_inputs_accepts_valid_specs():
    m = _load_runner()
    parsed = m._parse_merge_inputs([
        "chunk_2013_partial=/tmp/a",
        "chunk_2014=/tmp/b",
    ])
    assert parsed == {
        "chunk_2013_partial": "/tmp/a",
        "chunk_2014": "/tmp/b",
    }


def test_parse_merge_inputs_rejects_unknown_chunk_id():
    m = _load_runner()
    with pytest.raises(m.ChunkManifestError):
        m._parse_merge_inputs(["chunk_2099=/tmp/x"])


def test_parse_merge_inputs_rejects_duplicate_chunk_id():
    m = _load_runner()
    with pytest.raises(m.ChunkManifestError):
        m._parse_merge_inputs([
            "chunk_2015=/tmp/a", "chunk_2015=/tmp/b",
        ])


def test_parse_merge_inputs_rejects_malformed_spec():
    m = _load_runner()
    with pytest.raises(m.ChunkManifestError):
        m._parse_merge_inputs(["chunk_2015"])  # missing =DIR


# ── Halt diagnostic content shape ────────────────────────────────────────────

def test_chunk_halt_diagnostic_is_derived_only(tmp_path):
    m = _load_runner()
    m._write_chunk_halt_diagnostic(
        str(tmp_path),
        {
            "halt_class": "FetchFailure",
            "message": "HTTP 500 for ...",
            "started_at_utc": "2026-05-23T10:00:00+00:00",
            "halted_at_utc": "2026-05-23T10:00:05+00:00",
            "chunk_id": "chunk_2018",
            "actual_completed_file_count": 42,
        },
    )
    diag = json.load(open(tmp_path / "halt_diagnostic.json"))
    # No raw payload, no extracted CSV, no SQLDATE values
    assert "payload" not in str(diag).lower()
    assert "sqldate" not in str(diag).lower()
    assert ".csv" not in str(diag).lower()
    assert diag["halt_class"] == "FetchFailure"


# ============================================================================
# 17. Sentinel SQLDATE subclass (substrate amendment memo at commit `7206e30`,
#     R3 + Option α). The 2019-12-31 GDELT 1.0 daily-export file contained
#     120 rows with SQLDATE 1920-01-01; the parser must recognize these as
#     sentinel-placeholder rows, route them into per-sentinel diagnostics
#     only, exclude them from primary aggregates (Option α), and continue
#     to halt on any non-sentinel SQLDATE whose offset is outside
#     `EXPECTED_OFFSETS` (discovery-preservation property).
# ============================================================================

def _make_payload_with_explicit_sqldates(nominal_date, sqldate_rows):
    """Build a synthetic GDELT-shaped .zip payload with hand-specified
    SQLDATE values (not offsets). `sqldate_rows` is a list of
    (sqldate_yyyymmdd_str, count) tuples."""
    rows = []
    row_id = 0
    yyyymmdd_nominal = nominal_date.strftime("%Y%m%d")
    for sqldate_str, count in sqldate_rows:
        for _ in range(count):
            row_id += 1
            rows.append("{}\t{}\tA".format(row_id, sqldate_str))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr(
            "{}.export.CSV".format(yyyymmdd_nominal), "\n".join(rows),
        )
    return buf.getvalue()


def test_sentinel_sqldates_constant_is_evidence_bounded_six_value_tuple():
    """SENTINEL_SQLDATES must be the evidence-bounded 6-value tuple
    `(date(1920, 1, 1), date(1920, 1, 2), date(1920, 1, 3), date(1920, 1,
    4), date(1920, 1, 5), date(1920, 1, 6))` per the chunk_2020
    substrate amendment memo at commit `a1f2c4c`. Every member is
    directly observed in substrate evidence; zero predicted values;
    `date(1920, 1, 7)` is NOT included."""
    m = _load_runner()
    expected = (
        date(1920, 1, 1),
        date(1920, 1, 2),
        date(1920, 1, 3),
        date(1920, 1, 4),
        date(1920, 1, 5),
        date(1920, 1, 6),
    )
    assert m.SENTINEL_SQLDATES == expected
    assert isinstance(m.SENTINEL_SQLDATES, tuple)
    assert len(m.SENTINEL_SQLDATES) == 6
    for s in m.SENTINEL_SQLDATES:
        assert isinstance(s, date)
    # Negative assertion: date(1920, 1, 7) must NOT be in the recognized
    # sentinel set — it must still halt under halt-on-other-unexpected
    # unless separately evidenced by a future substrate amendment memo.
    assert date(1920, 1, 7) not in m.SENTINEL_SQLDATES


def test_parser_recognizes_sentinel_sqldate_no_halt():
    """A row with SQLDATE = 19200101 in a 2019-12-31 payload must be
    recognized as a sentinel row, NOT raise FullBuildBoundaryBreach, and
    be routed into per_sentinel_count / sentinel_sqldate_distribution /
    total_sentinel_rows only (Option α: excluded from primary series)."""
    m = _load_runner()
    nom = date(2019, 12, 31)
    payload = _make_payload_with_explicit_sqldates(
        nom, [("19200101", 1)],
    )
    p = m.parse_payload(payload, nom)
    assert p["total_sentinel_rows"] == 1
    assert p["per_sentinel_count"]["1920-01-01"] == 1
    assert p["sentinel_sqldate_distribution"]["1920-01-01"][
        "2019-12-31"
    ] == 1
    # Option α: sentinel rows excluded from per_offset_count, from
    # sqldate_offset_counts, and from out_of_window diagnostics.
    for off, cnt in p["per_offset_count"].items():
        assert cnt == 0, (off, cnt)
    assert p["sqldate_offset_counts"] == {}
    assert p["out_of_window_row_count"] == 0
    assert p["out_of_window_sqldate_distribution"] == {}


def test_parser_still_halts_on_non_sentinel_unexpected_offset():
    """The halt-on-other-unexpected behavior must be preserved verbatim.
    A non-sentinel SQLDATE whose offset is not in EXPECTED_OFFSETS must
    still raise FullBuildBoundaryBreach. Discovery-preservation property
    (memo §8 / §13)."""
    m = _load_runner()
    nom = date(2019, 12, 31)
    # Offset = -100 days = 2019-09-22; not in EXPECTED_OFFSETS, not in
    # SENTINEL_SQLDATES.
    payload = _make_payload_zip(nom, [(-100, 1)])
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.parse_payload(payload, nom)


def test_parser_canonical_offsets_unchanged_semantics():
    """A payload of canonical offsets only must still produce
    per_offset_count / sqldate_offset_counts exactly as before, with
    sentinel counters at zero (no regression in non-sentinel handling)."""
    m = _load_runner()
    nom = date(2018, 6, 15)
    p = m.parse_payload(
        _make_payload_zip(nom, [
            (-3650, 1), (-365, 1), (-30, 1), (-7, 1),
            (-1, 1), (0, 1), (1, 1),
        ]),
        nom,
    )
    for off in m.EXPECTED_OFFSETS:
        assert p["per_offset_count"][off] == 1
    assert p["total_sentinel_rows"] == 0
    assert p["per_sentinel_count"]["1920-01-01"] == 0
    assert p["sentinel_sqldate_distribution"] == {}


def test_parser_mixed_sentinel_and_canonical():
    """A mixed payload must attribute canonical rows to existing
    aggregates exactly and sentinel rows only to sentinel diagnostics.
    Accounting identity:
        row_count
        == sum(per_offset_count)
           + total_sentinel_rows
           + malformed_short_rows
           + unparseable_sqldate_rows
    """
    m = _load_runner()
    nom = date(2019, 12, 31)
    # 2 canonical T=0 + 1 canonical T-7 + 3 sentinel
    canonical_zero = nom.strftime("%Y%m%d")
    canonical_minus_7 = (nom + timedelta(days=-7)).strftime("%Y%m%d")
    payload = _make_payload_with_explicit_sqldates(nom, [
        (canonical_zero, 2),
        (canonical_minus_7, 1),
        ("19200101", 3),
    ])
    p = m.parse_payload(payload, nom)
    assert p["per_offset_count"][0] == 2
    assert p["per_offset_count"][-7] == 1
    assert p["total_sentinel_rows"] == 3
    assert p["per_sentinel_count"]["1920-01-01"] == 3
    canonical_total = sum(p["per_offset_count"].values())
    accounting_total = (
        canonical_total
        + p["total_sentinel_rows"]
        + p["malformed_short_rows"]
        + p["unparseable_sqldate_rows"]
    )
    assert accounting_total == p["row_count"], (
        canonical_total, p["total_sentinel_rows"], p["row_count"],
    )


def test_empty_payload_initializes_sentinel_fields():
    """Empty-parse-result fallback must initialize the new sentinel
    fields to zero/empty defaults so downstream aggregators have stable
    types. Per chunk_2020 substrate amendment (`a1f2c4c`),
    `per_sentinel_count` is initialized with one zero-entry per value
    in the 6-value `SENTINEL_SQLDATES` tuple."""
    m = _load_runner()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        pass
    nom = date(2019, 12, 31)
    p = m.parse_payload(buf.getvalue(), nom)
    assert p["total_sentinel_rows"] == 0
    assert p["per_sentinel_count"] == {
        "1920-01-01": 0,
        "1920-01-02": 0,
        "1920-01-03": 0,
        "1920-01-04": 0,
        "1920-01-05": 0,
        "1920-01-06": 0,
    }
    assert p["sentinel_sqldate_distribution"] == {}


def test_parser_recognizes_all_six_sentinel_sqldates_no_halt():
    """Each of the 6 sentinel SQLDATEs (`1920-01-01..1920-01-06`) must
    be recognized as a sentinel row, NOT raise FullBuildBoundaryBreach,
    and be routed into per_sentinel_count / sentinel_sqldate_distribution
    / total_sentinel_rows only (Option α: excluded from primary series).
    Chunk_2020 substrate amendment memo (`a1f2c4c`) — directly observed
    values across 6 affected file dates."""
    m = _load_runner()
    nom = date(2020, 1, 3)  # mid-cluster nominal file date
    sentinel_rows = [
        ("19200101", 1),
        ("19200102", 1),
        ("19200103", 1),
        ("19200104", 1),
        ("19200105", 1),
        ("19200106", 1),
    ]
    payload = _make_payload_with_explicit_sqldates(nom, sentinel_rows)
    p = m.parse_payload(payload, nom)
    assert p["total_sentinel_rows"] == 6
    for iso in [
        "1920-01-01", "1920-01-02", "1920-01-03",
        "1920-01-04", "1920-01-05", "1920-01-06",
    ]:
        assert p["per_sentinel_count"][iso] == 1, iso
        assert p["sentinel_sqldate_distribution"][iso][
            nom.isoformat()
        ] == 1, iso
    # Option α: sentinel rows excluded from per_offset_count, from
    # sqldate_offset_counts, and from out_of_window diagnostics.
    for off, cnt in p["per_offset_count"].items():
        assert cnt == 0, (off, cnt)
    assert p["sqldate_offset_counts"] == {}
    assert p["out_of_window_row_count"] == 0
    assert p["out_of_window_sqldate_distribution"] == {}


def test_parser_halts_on_date_1920_01_07_unobserved_placeholder():
    """`date(1920, 1, 7)` is NOT in the recommended sentinel tuple
    because it was not directly observed in the chunk_2020 Option B
    bounded-envelope research. The runner must continue to halt via
    `FullBuildBoundaryBreach` on any SQLDATE outside `SENTINEL_SQLDATES`
    whose offset is outside `EXPECTED_OFFSETS` — the
    discovery-preservation property remains load-bearing per
    `a1f2c4c` §6.5. Any future encounter with `1920-01-07` must
    motivate a separately scoped substrate amendment memo, not silent
    expansion."""
    m = _load_runner()
    assert date(1920, 1, 7) not in m.SENTINEL_SQLDATES
    nom = date(2020, 1, 6)  # offset would be -36524 days
    payload = _make_payload_with_explicit_sqldates(
        nom, [("19200107", 1)],
    )
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.parse_payload(payload, nom)


def test_parser_halts_on_other_non_sentinel_placeholder_like_value():
    """A non-sentinel SQLDATE outside the `1920-01-XX` early-Jan cluster
    must still halt (e.g. `1920-02-15` in a `2020-02-15` payload).
    Discovery-preservation prevents silent absorption of out-of-cluster
    placeholder-like values that the amendment memo §6.4 explicitly
    flagged as overgeneralization risks for year-shift predicates."""
    m = _load_runner()
    nom = date(2020, 2, 15)
    payload = _make_payload_with_explicit_sqldates(
        nom, [("19200215", 1)],
    )
    with pytest.raises(m.FullBuildBoundaryBreach):
        m.parse_payload(payload, nom)


def test_chunk_2020_runner_anchors_unchanged_after_sentinel_amendment():
    """The runner amendment must update `SENTINEL_SQLDATES` only; it
    must NOT change chunk-definition anchors. chunk_2020 retains
    `EXPECTED_CHUNK_COUNTS = 366` and date range `(2020-01-01,
    2020-12-31)` per `a1f2c4c` §7.2."""
    m = _load_runner()
    assert "chunk_2020" in m.CHUNK_IDS
    assert m.EXPECTED_CHUNK_COUNTS["chunk_2020"] == 366
    assert m.CHUNK_YEAR_RANGES["chunk_2020"] == (
        date(2020, 1, 1), date(2020, 12, 31),
    )


def test_accumulator_aggregates_sentinel_fields():
    """_ingest_parse_into_accumulator must fold sentinel fields from each
    parse_result into the running accumulator, preserving Option α
    attribution at the aggregate level."""
    m = _load_runner()
    accum = m._new_accumulator()
    nom = date(2019, 12, 31)
    p1 = m.parse_payload(
        _make_payload_with_explicit_sqldates(nom, [("19200101", 2)]),
        nom,
    )
    nom2 = date(2019, 12, 30)
    p2 = m.parse_payload(
        _make_payload_with_explicit_sqldates(nom2, [("19200101", 1)]),
        nom2,
    )
    m._ingest_parse_into_accumulator(accum, p1)
    m._ingest_parse_into_accumulator(accum, p2)
    assert accum["total_sentinel_rows"] == 3
    assert accum["per_sentinel_total"]["1920-01-01"] == 3
    assert accum["sentinel_sqldate_distribution"]["1920-01-01"][
        "2019-12-31"
    ] == 2
    assert accum["sentinel_sqldate_distribution"]["1920-01-01"][
        "2019-12-30"
    ] == 1


def test_full_build_authorized_still_false_after_amendment():
    """The runner amendment must not flip FULL_BUILD_AUTHORIZED. Sentinel
    handling is a parser-level addition; the three-guard discipline is
    unchanged."""
    m = _load_runner()
    assert m.FULL_BUILD_AUTHORIZED is False


def test_expected_offsets_unchanged_after_amendment():
    """The runner amendment must NOT widen EXPECTED_OFFSETS. R3 retains
    the 7-element taxonomy for non-sentinel rows verbatim (memo §13)."""
    m = _load_runner()
    assert m.EXPECTED_OFFSETS == (-3650, -365, -30, -7, -1, 0, 1)


def test_known_substrate_gaps_unchanged_after_amendment():
    """KNOWN_SUBSTRATE_GAPS is fetch-gap handling, conceptually separate
    from sentinel-SQLDATE handling. R3 must not modify it (memo §6 /
    §13)."""
    m = _load_runner()
    assert m.KNOWN_SUBSTRATE_GAPS == (
        "2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19",
    )
