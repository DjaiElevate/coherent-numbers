"""Lane 2 GDELT 1.0 count-only feasibility — tests (synthetic fixtures only).

NO real GDELT data, NO market data, NO network, NO 2023+, NO outcomes.
"""

import importlib.util
import os
import zipfile
from datetime import date

import pytest

import lane2_gdelt1_count_feasibility as m


# ── 1. regime-aware, pre-2023 file planning ───────────────────────────────────

def test_plan_is_regime_aware():
    units = m.plan_gdelt1_files(date(2005, 1, 1), date(2022, 12, 31))
    regimes = {u.regime for u in units}
    assert regimes == {"yearly", "monthly", "daily"}
    # 2005 yearly, 2006-01 monthly, 2013-04-01 first daily
    keys = {u.key for u in units}
    assert "2005" in keys
    assert "2006-01" in keys
    assert "2013-04-01" in keys
    assert all(u.rep_date < m.SEAL_START for u in units)
    # 2013-03 is last monthly; 2013-03-31 must not be a daily unit
    assert "2013-03" in keys
    assert "2013-03-31" not in keys


def test_plan_excludes_and_aborts_on_2023plus():
    with pytest.raises(m.Protocol2023PlusBreach):
        m.plan_gdelt1_files(date(2022, 12, 1), date(2023, 1, 5))
    with pytest.raises(m.Protocol2023PlusBreach):
        m.plan_gdelt1_files(date(2023, 1, 1), date(2023, 2, 1))


# ── 2. manifest scaffolding ───────────────────────────────────────────────────

def test_manifest_scaffolding(tmp_path):
    units = m.plan_gdelt1_files(date(2013, 4, 1), date(2013, 4, 3))
    man = m.build_freeze_manifest(date(2013, 4, 1), date(2013, 4, 3), units,
                                  {"2013-04-01": "deadbeef"})
    assert man["source_product"] == m.SELECTED_SOURCE
    assert man["file_count"] == 3
    assert man[
        "confirm_no_2023plus_downloaded_stored_sampled_counted_inspected"
    ] is True
    p = tmp_path / "manifest.json"
    m.write_json(str(p), man)
    assert p.exists()


# ── 3. parser scaffolding (synthetic pre-2013 + post-2013 + 2023 abort) ──────

def _write(path, lines):
    path.write_text("\n".join(lines), encoding="utf-8")


def test_parser_counts_pre_and_post_2013(tmp_path):
    pre = tmp_path / "pre2013.tsv"   # event-date regime style
    _write(pre, ["1\t20091115\tX", "2\t20091115\tY", "3\t20091116\tZ"])
    post = tmp_path / "post2013.tsv"  # daily regime style
    _write(post, ["10\t20150312\tA", "11\t20150312\tB"])
    cpre = m.parse_gdelt1_file_daily_counts(str(pre))
    cpost = m.parse_gdelt1_file_daily_counts(str(post))
    assert cpre[date(2009, 11, 15)] == 2 and cpre[date(2009, 11, 16)] == 1
    assert cpost[date(2015, 3, 12)] == 2
    agg = m.aggregate_daily_counts([cpre, cpost])
    assert agg[date(2009, 11, 15)] == 2


def test_parser_zip_fixture(tmp_path):
    z = tmp_path / "day.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("day.csv", "1\t20180704\tA\n2\t20180704\tB\n")
    counts = m.parse_gdelt1_file_daily_counts(str(z))
    assert counts[date(2018, 7, 4)] == 2


def test_parser_aborts_on_2023plus_row(tmp_path):
    bad = tmp_path / "bad.tsv"
    _write(bad, ["1\t20230101\tX"])
    with pytest.raises(m.Protocol2023PlusBreach):
        m.parse_gdelt1_file_daily_counts(str(bad))


# ── missingness / by-year ─────────────────────────────────────────────────────

def test_missingness_and_by_year():
    counts = {date(2010, 1, 1): 5, date(2010, 1, 3): 2, date(2011, 1, 1): 1}
    miss = m.missingness_by_year(counts, date(2010, 1, 1), date(2010, 1, 3))
    assert miss[2010]["expected_days"] == 3
    assert miss[2010]["observed_days"] == 2
    assert miss[2010]["missing_days"] == 1
    assert m.by_year_counts(counts) == {2010: 7, 2011: 1}


# ── 4. spike definitions ──────────────────────────────────────────────────────

def _ramp_counts(n, base=date(2009, 1, 1)):
    from datetime import timedelta
    c = {}
    for i in range(n):
        c[base + timedelta(days=i)] = 10
    return c


def test_option_a_percentile_spike_detects_outlier():
    c = _ramp_counts(70)
    from datetime import timedelta
    spike_day = date(2009, 1, 1) + timedelta(days=65)
    c[spike_day] = 9999
    spikes = m.option_a_percentile_spikes(c, baseline=60, pct=0.95)
    assert spike_day in spikes


def test_option_b_zscore_spike_and_zero_var_safe():
    # constant ramp -> zero-variance trailing windows -> honestly skipped
    assert m.option_b_zscore_spikes(_ramp_counts(70), baseline=60,
                                    z=2.5) == []
    # nonzero baseline variance (small alternating noise) + a clear outlier
    from datetime import timedelta
    base = date(2009, 1, 1)
    c = {base + timedelta(days=i): (10 if i % 2 == 0 else 12)
         for i in range(70)}
    sd = base + timedelta(days=64)
    c[sd] = 500
    assert sd in m.option_b_zscore_spikes(c, baseline=60, z=2.5)


def test_option_c_requires_threshold():
    c = _ramp_counts(5)
    with pytest.raises(ValueError):
        m.option_c_acceleration_spikes(c)  # no silent default
    from datetime import timedelta
    c[date(2009, 1, 1) + timedelta(days=3)] = 1000
    got = m.option_c_acceleration_spikes(c, threshold=100)
    assert date(2009, 1, 1) + timedelta(days=3) in got


# ── 5. clustering / overlap ───────────────────────────────────────────────────

def test_clustering_windows():
    ds = [date(2010, 1, 1), date(2010, 1, 4), date(2010, 1, 20),
          date(2010, 2, 15)]
    assert m.cluster_spikes(ds, 5) == [date(2010, 1, 1), date(2010, 1, 20),
                                       date(2010, 2, 15)]
    assert len(m.cluster_spikes(ds, 10)) == 3
    assert len(m.cluster_spikes(ds, 20)) == 2


def test_overlap_count():
    ds = [date(2010, 1, 1), date(2010, 1, 3), date(2010, 6, 1)]
    r5 = m.event_window_overlap_count(ds, 1, 5)
    assert r5["overlapping_events"] == 2  # the two January events overlap
    assert r5["n_events"] == 3


# ── 6. non-trading-day ────────────────────────────────────────────────────────

def test_non_trading_day_unresolved_without_calendar():
    r = m.non_trading_day_count([date(2010, 1, 2)])
    assert r["status"] == "calendar_unavailable"
    assert r["non_trading_day_count"] is None


def test_non_trading_day_with_calendar():
    r = m.non_trading_day_count(
        [date(2010, 1, 2), date(2010, 1, 4)], [date(2010, 1, 4)]
    )
    assert r["status"] == "resolved" and r["non_trading_day_count"] == 1


# ── 7. state feasibility ──────────────────────────────────────────────────────

def test_state_feasibility_unresolved_without_frozen_source():
    r = m.state_count_feasibility()
    assert r["status"] == "unresolved"


# ── 8. feasibility-class scaffolding ─────────────────────────────────────────

def test_feasibility_classes():
    assert m.assign_feasibility_class(True, 100, 30, "resolved", True,
                                      False)[0] == "F3"
    assert m.assign_feasibility_class(True, 5, 30, "resolved", True,
                                      False)[0] == "F1"
    assert m.assign_feasibility_class(True, 100, 30, "unresolved", True,
                                      False)[0] == "F2"
    assert m.assign_feasibility_class(False, 0, 30, "unresolved", True,
                                      False)[0] == "F0"
    assert m.assign_feasibility_class(True, 100, 30, "resolved", False,
                                      False)[0] == "F4"
    assert m.assign_feasibility_class(True, 100, 30, "resolved", True,
                                      True)[0] == "F5"
    # F3 wording must not read as hypothesis evidence
    assert "does NOT confirm" in m.F_NOTES["F3"]


# ── 13. metadata ──────────────────────────────────────────────────────────────

def test_metadata_fields_and_seal():
    md = m.build_metadata(date(2005, 1, 1), date(2022, 12, 31), True, True,
                          "unresolved", "F2")
    for k, v in {
        "no_2023_plus": True, "outcomes_computed": False,
        "returns_computed": False, "models_fit": False,
        "p_values_computed": False, "step2_lock_drafted": False,
        "feasibility_only": True, "hypothesis_verdict": False,
    }.items():
        assert md[k] is v
    assert md["governing_protocol_commit"] == m.GOVERNING_PROTOCOL_COMMIT
    with pytest.raises(m.Protocol2023PlusBreach):
        m.build_metadata(date(2005, 1, 1), date(2023, 1, 1), True, True,
                         "unresolved", "F2")


def test_metadata_normalization_status_default_and_note():
    md = m.build_metadata(date(2005, 1, 1), date(2022, 12, 31), True, True,
                          "unresolved", "F2")
    assert md["gdelt_normalization_files_status"] == "deferred"
    assert "must be pinned before any real count-only run" in (
        md["gdelt_normalization_files_note"]
    )


def test_metadata_normalization_status_validated():
    for s in ("used", "not_used", "deferred"):
        md = m.build_metadata(date(2005, 1, 1), date(2022, 12, 31), True, True,
                              "unresolved", "F2",
                              gdelt_normalization_files_status=s)
        assert md["gdelt_normalization_files_status"] == s
    with pytest.raises(ValueError):
        m.build_metadata(date(2005, 1, 1), date(2022, 12, 31), True, True,
                         "unresolved", "F2",
                         gdelt_normalization_files_status="maybe")


def test_metadata_min_event_floor_and_threshold_present_even_when_none():
    md = m.build_metadata(date(2005, 1, 1), date(2022, 12, 31), True, True,
                          "unresolved", "F2")
    assert "min_event_floor" in md and md["min_event_floor"] is None
    assert "option_c_threshold" in md and md["option_c_threshold"] is None
    assert "must be pinned" in md["min_event_floor_note"]
    assert "no silent default" in md["option_c_threshold_note"]


def test_metadata_echoes_supplied_floor_and_threshold():
    md = m.build_metadata(date(2005, 1, 1), date(2022, 12, 31), True, True,
                          "resolved", "F3", min_event_floor=40,
                          option_c_threshold=125.0)
    assert md["min_event_floor"] == 40
    assert md["option_c_threshold"] == 125.0


def test_unused_field_import_removed():
    import inspect
    src = inspect.getsource(m)
    assert "from dataclasses import dataclass\n" in src
    assert "from dataclasses import dataclass, field" not in src
    # dataclasses.field is not bound in the module namespace
    assert not hasattr(m, "field")


# ── 12. prohibited-computation guards ────────────────────────────────────────

def test_no_prohibited_symbols_in_module():
    names = [n.lower() for n in dir(m)]
    for forbidden in ("car", "abnormal_return", "fit_model", "pvalue",
                      "p_value", "regress", "sharpe", "backtest"):
        assert not any(forbidden in n for n in names), forbidden
    # explicitly no market-return / outcome public functions
    assert not any(n.startswith("compute_return") for n in dir(m))


# ── 10. runner safety ─────────────────────────────────────────────────────────

def _load_runner():
    path = os.path.join(os.path.dirname(__file__), "..", "scripts",
                        "run_lane2_gdelt1_count_feasibility.py")
    spec = importlib.util.spec_from_file_location("l2_runner", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_runner_inert_by_default(monkeypatch):
    r = _load_runner()
    assert r.COUNT_FEASIBILITY_AUTHORIZED is False
    monkeypatch.setenv("LANE2_COUNT_FEASIBILITY_AUTHORIZED", "1")
    assert r._guards_ok(True) is False  # constant still False
    with pytest.raises(SystemExit):
        r.run_count_feasibility(os.getcwd())


def test_runner_guards_need_all_three(monkeypatch):
    r = _load_runner()
    monkeypatch.delenv("LANE2_COUNT_FEASIBILITY_AUTHORIZED", raising=False)
    assert r._guards_ok(True) is False


# ── live retrieval / freeze scaffolding (synthetic; NO real network) ─────────

def test_url_construction_from_templates():
    units = m.plan_gdelt1_files(date(2005, 1, 1), date(2013, 5, 2))
    plan = m.build_retrieval_plan(units, base_url="http://example.test/ev")
    by_regime = {e.regime: e for e in plan}
    assert by_regime["yearly"].filename == "2005.zip"
    assert by_regime["monthly"].filename.endswith(".zip")
    daily = [e for e in plan if e.regime == "daily"][0]
    assert daily.filename == "20130401.export.CSV.zip"
    assert all(e.url.startswith("http://example.test/ev/") for e in plan)
    assert all(e.rep_date < m.SEAL_START for e in plan)


def test_retrieval_plan_aborts_on_2023plus():
    bad = [m.PlannedUnit("2023-01-01", "daily", date(2023, 1, 1))]
    with pytest.raises(m.Protocol2023PlusBreach):
        m.build_retrieval_plan(bad)


def test_source_index_validation_excludes_2023plus():
    ok = m.validate_source_index(
        [{"date": "2010-05-01"}, {"rep_date": date(2012, 1, 1)}]
    )
    assert ok == [date(2010, 5, 1), date(2012, 1, 1)]
    with pytest.raises(m.Protocol2023PlusBreach):
        m.validate_source_index([{"date": "2023-02-01"}])
    with pytest.raises(ValueError):
        m.validate_source_index([{"nope": 1}])


def test_download_one_refuses_without_authorization(tmp_path):
    # default draft: not authorized -> RetrievalNotAuthorized, no network
    with pytest.raises(m.RetrievalNotAuthorized):
        m.download_one("http://x/y.zip", str(tmp_path / "f.zip"),
                       date(2015, 3, 12))


def test_download_one_refuses_2023plus_before_anything(tmp_path):
    with pytest.raises(m.Protocol2023PlusBreach):
        m.download_one("http://x/2023.zip", str(tmp_path / "f.zip"),
                       date(2023, 1, 1), network_authorized=True)


def test_download_one_temp_then_atomic_with_fake_opener(tmp_path, monkeypatch):
    # enable retrieval ONLY within this test; inject a fake opener (no network)
    monkeypatch.setattr(m, "REAL_RETRIEVAL_ENABLED", True)

    class _Resp:
        def __init__(self, data):
            self._d = data

        def read(self):
            return self._d

    seen = {}

    def fake_opener(url, timeout=None):
        seen["url"] = url
        seen["timeout"] = timeout
        return _Resp(b"FAKE-GDELT-BYTES")

    dest = tmp_path / "sub" / "20150312.export.CSV.zip"
    res = m.download_one(
        "http://example.test/ev/20150312.export.CSV.zip", str(dest),
        date(2015, 3, 12), timeout=12.0, retries=3,
        network_authorized=True, opener=fake_opener,
    )
    assert dest.exists()
    assert dest.read_bytes() == b"FAKE-GDELT-BYTES"
    assert res["size_bytes"] == len(b"FAKE-GDELT-BYTES")
    import hashlib as _h
    assert res["sha256"] == _h.sha256(b"FAKE-GDELT-BYTES").hexdigest()
    assert seen["timeout"] == 12.0
    # no leftover .part temp files
    assert not any(p.suffix == ".part" for p in (tmp_path / "sub").iterdir())


def test_freeze_manifest_includes_retrieval_fields():
    units = m.plan_gdelt1_files(date(2013, 4, 1), date(2013, 4, 2))
    plan = m.build_retrieval_plan(units)
    man = m.build_freeze_manifest(
        date(2013, 4, 1), date(2013, 4, 2), units,
        file_hashes={"2013-04-01": "abc"},
        urls_per_unit={e.key: e.url for e in plan},
        file_sizes={"2013-04-01": 123},
        aggregate_content_hash="agg",
        row_counts={"2013-04-01": 10},
        access_timestamp="20260518T000000Z",
        gdelt_normalization_files_status="deferred",
        min_event_floor=40, option_c_threshold=125.0,
    )
    for k in ("urls_per_unit", "file_sizes", "sha256_per_file",
              "aggregate_content_hash", "access_timestamp",
              "no_2023plus_downloaded_or_counted",
              "gdelt_2013_regime_boundary_handled",
              "gdelt_normalization_files_status", "min_event_floor",
              "option_c_threshold", "url_template_default"):
        assert k in man
    assert man["min_event_floor"] == 40
    assert man["gdelt_normalization_files_status"] == "deferred"
    with pytest.raises(ValueError):
        m.build_freeze_manifest(date(2013, 4, 1), date(2013, 4, 2), units,
                                gdelt_normalization_files_status="bogus")


def test_archive_layout_verification_and_outcome():
    units = m.plan_gdelt1_files(date(2005, 1, 1), date(2013, 4, 3))
    plan = m.build_retrieval_plan(units)
    keys = [e.key for e in plan]
    # full match -> ok
    rep_ok = m.verify_archive_layout(plan, keys)
    assert rep_ok["actual_layout_differs_from_documented"] is False
    assert m.layout_outcome(rep_ok)[0] == "ok"
    # missing + unexpected -> differs -> F4
    rep_bad = m.verify_archive_layout(plan, keys[:-1] + ["GHOST"])
    assert rep_bad["files_missing"] and rep_bad["files_in_archive_not_planned"]
    assert rep_bad["actual_layout_differs_from_documented"] is True
    assert m.layout_outcome(rep_bad)[0] == "F4"
    assert rep_ok["boundary_2013_04_01_handled"] is True


def test_retrieval_section_adds_no_prohibited_symbols():
    names = [n.lower() for n in dir(m)]
    for forbidden in ("car", "abnormal", "regress", "pvalue", "p_value",
                      "sharpe", "backtest", "model_fit"):
        assert not any(forbidden in n for n in names), forbidden
