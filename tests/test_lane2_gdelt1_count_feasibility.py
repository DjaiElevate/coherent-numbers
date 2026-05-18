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


# ── archive-layout: dedicated file/date-unit mismatch category ───────────────

def _plan_small():
    units = m.plan_gdelt1_files(date(2005, 1, 1), date(2013, 4, 3))
    return units, m.build_retrieval_plan(units)


def test_unit_key_parser_and_2023plus_guard():
    assert m.parse_gdelt1_unit_key("2005") == (date(2005, 1, 1), "yearly")
    assert m.parse_gdelt1_unit_key("2012-05") == (date(2012, 5, 1), "monthly")
    assert m.parse_gdelt1_unit_key("2015-03-12") == (
        date(2015, 3, 12), "daily")
    with pytest.raises(m.Protocol2023PlusBreach):
        m.parse_gdelt1_unit_key("2023-01-01")
    with pytest.raises(ValueError):
        m.parse_gdelt1_unit_key("GHOST")


def test_layout_matching_slots_no_mismatch():
    units, plan = _plan_small()
    keys = [e.key for e in plan]
    slot = {k: k for k in keys}  # actual == planned
    rep = m.verify_archive_layout(plan, keys, slot_actual_keys=slot)
    assert rep["files_date_unit_mismatch"] == []
    assert rep["actual_layout_differs_from_documented"] is False
    assert rep["note"] == m.LAYOUT_FEASIBILITY_NOTE
    assert m.layout_outcome(rep)[0] == "ok"


def test_layout_daily_monthly_yearly_mismatch_reported():
    units, plan = _plan_small()
    keys = [e.key for e in plan]
    slot = {k: k for k in keys}
    # daily mismatch
    slot["2013-04-02"] = "2013-04-03"
    # monthly mismatch
    slot["2012-05"] = "2012-06"
    # yearly mismatch
    slot["2005"] = "2006"
    rep = m.verify_archive_layout(plan, keys, slot_actual_keys=slot)
    mm = {d["planned_key"] for d in rep["files_date_unit_mismatch"]}
    assert {"2013-04-02", "2012-05", "2005"} <= mm
    assert rep["actual_layout_differs_from_documented"] is True
    cls, reason = m.layout_outcome(rep)
    assert cls == "F4"
    assert "not hypothesis evidence" in reason


def test_layout_mismatch_when_actual_key_not_parseable():
    units, plan = _plan_small()
    keys = [e.key for e in plan]
    slot = {"2005": "GHOSTKEY"}
    rep = m.verify_archive_layout(plan, keys, slot_actual_keys=slot)
    assert any(d["planned_key"] == "2005"
               for d in rep["files_date_unit_mismatch"])
    assert m.layout_outcome(rep)[0] == "F4"


def test_layout_existing_categories_still_work():
    units, plan = _plan_small()
    keys = [e.key for e in plan]
    rep = m.verify_archive_layout(plan, keys[:-1] + ["GHOST"])
    assert rep["files_missing"] and rep["files_in_archive_not_planned"]
    assert rep["files_date_unit_mismatch"] == []  # no slot map -> none
    assert rep["actual_layout_differs_from_documented"] is True
    # naming category
    rep2 = m.verify_archive_layout(
        plan, keys, expected_naming=lambda e: e.regime != "yearly"
    )
    assert rep2["files_unexpected_naming"]  # yearly flagged
    assert rep2["actual_layout_differs_from_documented"] is True


def test_layout_2023plus_aborts_before_classification():
    units, plan = _plan_small()
    keys = [e.key for e in plan]
    # 2023+ in available listing
    with pytest.raises(m.Protocol2023PlusBreach):
        m.verify_archive_layout(plan, keys + ["2023-01-01"])
    # 2023+ in slot actual key
    with pytest.raises(m.Protocol2023PlusBreach):
        m.verify_archive_layout(plan, keys,
                                slot_actual_keys={"2005": "2023-06-01"})


# ════════════════════════════════════════════════════════════════════════════
# Retrieval-wiring patch — synthetic fixtures, fake openers, NO real network,
# NO real GDELT, NO 2023+, NO market data, NO outcomes.
# ════════════════════════════════════════════════════════════════════════════

import io
from datetime import timedelta


def _zip_bytes(rows):
    """Build in-memory .zip bytes with one inner TSV (GLOBALEVENTID, SQLDATE)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("inner.csv",
                    "\n".join("{}\t{}\tX".format(i, sd)
                              for i, sd in enumerate(rows)))
    return buf.getvalue()


class _Resp:
    def __init__(self, data):
        self._d = data

    def read(self):
        return self._d


def _make_fake_opener(start, end, rows_per_day=3, calls=None):
    """Fake opener: index URL -> filename listing; file URL -> zip bytes.
    Records calls; performs NO network."""
    days = []
    d = start
    while d <= end:
        days.append(d)
        d += timedelta(days=1)
    index_txt = " ".join(
        "{:04d}{:02d}{:02d}.export.CSV.zip".format(x.year, x.month, x.day)
        for x in days
    )

    def opener(url, timeout=None):
        if calls is not None:
            calls.append(url)
        if url.rstrip("/").endswith("events"):
            return _Resp(index_txt.encode("utf-8"))
        stem = url.rsplit("/", 1)[-1].split(".")[0]
        dd = date(int(stem[:4]), int(stem[4:6]), int(stem[6:8]))
        return _Resp(_zip_bytes(["{:04d}{:02d}{:02d}".format(
            dd.year, dd.month, dd.day)] * rows_per_day))

    return opener


# ── archive_layout_status: controlled vocabulary + metadata field ────────────

def test_archive_layout_status_controlled_vocab_in_metadata():
    for s in m.ARCHIVE_LAYOUT_STATUS_VALUES:
        md = m.build_metadata(date(2005, 1, 1), date(2022, 12, 31), True, True,
                              "unresolved", "F2", archive_layout_status=s)
        assert md["archive_layout_status"] == s
    with pytest.raises(ValueError):
        m.build_metadata(date(2005, 1, 1), date(2022, 12, 31), True, True,
                         "unresolved", "F2",
                         archive_layout_status="totally-bogus")
    # default present and valid
    md = m.build_metadata(date(2005, 1, 1), date(2022, 12, 31), True, True,
                          "unresolved", "F2")
    assert md["archive_layout_status"] == "not_checked"


def test_metadata_run_authorization_and_pinned_echoes():
    md = m.build_metadata(
        date(2005, 1, 1), date(2022, 12, 31), True, True, "unresolved", "F2",
        gdelt_normalization_files_status=m.PINNED_NORMALIZATION_STATUS,
        min_event_floor=m.PINNED_MIN_EVENT_FLOOR,
        option_c_threshold=m.PINNED_OPTION_C_THRESHOLD,
        option_c_enabled=m.PINNED_OPTION_C_ENABLED,
        archive_layout_status="ok",
        post_run_safety_reset_required=True,
    )
    assert md["gdelt_normalization_files_status"] == "not_used"
    assert md["min_event_floor"] == 100
    assert md["option_c_threshold"] is None
    assert md["option_c_enabled"] is False
    assert md["no_2023plus"] is True and md["no_2023_plus"] is True
    assert md["run_authorization_memo"].endswith(
        "lane2_gdelt1_count_feasibility_run_authorization_v0.1.md")
    assert md["run_authorization_commit"] == m.RUN_AUTHORIZATION_COMMIT
    assert md["post_run_safety_reset_required"] is True
    # prohibited computations are negatively attested, not present as results
    assert md["returns_computed"] is False
    assert md["outcomes_computed"] is False
    assert md["models_fit"] is False
    assert md["p_values_computed"] is False
    assert md["hypothesis_verdict"] is False
    assert md["step2_lock_drafted"] is False
    # no value in metadata is a numeric market result
    for bad in ("car", "abnormal", "vix", "sharpe", "feature_importance"):
        assert not any(bad in k.lower() for k in md), bad


def test_archive_layout_status_token_mapping():
    units = m.plan_gdelt1_files(date(2005, 1, 1), date(2013, 4, 3))
    plan = m.build_retrieval_plan(units)
    keys = [e.key for e in plan]
    assert m.archive_layout_status_token(None) == "not_checked"
    assert m.archive_layout_status_token(
        m.verify_archive_layout(plan, keys)) == "ok"
    assert m.archive_layout_status_token(
        m.verify_archive_layout(plan, keys[:-1])) == "missing"
    rep_mm = m.verify_archive_layout(
        plan, keys, slot_actual_keys={**{k: k for k in keys}, "2005": "2006"})
    assert m.archive_layout_status_token(rep_mm) == "mismatch"
    rep_unx = m.verify_archive_layout(plan, keys + ["1999"])
    assert m.archive_layout_status_token(rep_unx) == "unexpected"


# ── concentration flags: descriptive, unthresholded, no hypothesis verdict ───

def test_concentration_flags_unthresholded_and_pre2023():
    daily = {date(2010, 1, 1): 5, date(2015, 6, 1): 9}
    flags = m.concentration_flags(daily, [date(2015, 6, 1)],
                                  [date(2015, 6, 1)])
    assert flags["concentration_interpretation"] == "descriptive_unthresholded"
    assert "NOT hypothesis evidence" in flags["note"]
    assert flags["raw_spikes_post_2013_04_01_fraction"] == 1.0
    with pytest.raises(m.Protocol2023PlusBreach):
        m.concentration_flags({date(2023, 1, 1): 1}, [], [])


# ── archive index fetch: injected opener only; aborts on 2023+ ───────────────

def test_fetch_archive_index_requires_opener():
    with pytest.raises(m.RetrievalNotAuthorized):
        m.fetch_archive_index(None)


def test_fetch_archive_index_parses_and_blocks_2023plus():
    op = _make_fake_opener(date(2013, 4, 1), date(2013, 4, 3))
    avail, slots = m.fetch_archive_index(op, index_url="http://x/events")
    assert avail == ["2013-04-01", "2013-04-02", "2013-04-03"]
    assert slots == {k: k for k in avail}

    def bad_opener(url, timeout=None):
        return _Resp(b"20230101.export.CSV.zip")
    with pytest.raises(m.Protocol2023PlusBreach):
        m.fetch_archive_index(bad_opener, index_url="http://x/events")


# ── orchestrator: F-classes, output allow-list, Option C never computed ──────

def test_orchestrator_f1_below_floor_writes_only_allowed(tmp_path,
                                                         monkeypatch):
    # enable retrieval ONLY within this test; fake opener, no real network
    monkeypatch.setattr(m, "REAL_RETRIEVAL_ENABLED", True)
    op = _make_fake_opener(date(2013, 4, 1), date(2013, 4, 5))
    avail = ["2013-04-0{}".format(i) for i in range(1, 6)]
    md = m.run_count_only_feasibility(
        str(tmp_path), opener=op, available_keys=avail,
        slot_actual_keys={k: k for k in avail},
        coverage_start=date(2013, 4, 1), coverage_end=date(2013, 4, 5),
    )
    assert md["feasibility_class"] == "F1"  # 0 clustered < 100
    assert md["min_event_floor"] == 100
    assert md["option_c_threshold"] is None
    assert md["option_c_enabled"] is False
    assert md["gdelt_normalization_files_status"] == "not_used"
    assert md["archive_layout_status"] == "ok"
    written = sorted(p.name for p in tmp_path.iterdir() if p.is_file())
    assert set(written) <= set(m.ALLOWED_OUTPUT_BASENAMES)
    assert "count_feasibility_metadata.json" in written
    assert not any("option_c" in w for w in written)
    assert not any(("return" in w or "car" in w or "model" in w
                    or "pvalue" in w or "2023" in w) for w in written)


def test_orchestrator_f2_when_counts_adequate_state_unresolved(
        tmp_path, monkeypatch):
    monkeypatch.setattr(m, "REAL_RETRIEVAL_ENABLED", True)
    op = _make_fake_opener(date(2013, 4, 1), date(2013, 4, 3))
    avail = ["2013-04-0{}".format(i) for i in range(1, 4)]
    big = [date(2013, 4, 1) + timedelta(days=i) for i in range(150)]
    monkeypatch.setattr(m, "option_a_percentile_spikes", lambda c: list(big))
    monkeypatch.setattr(m, "option_b_zscore_spikes", lambda c: [])
    monkeypatch.setattr(m, "cluster_spikes", lambda ds, sep: list(ds))
    md = m.run_count_only_feasibility(
        str(tmp_path), opener=op, available_keys=avail,
        slot_actual_keys={k: k for k in avail},
        coverage_start=date(2013, 4, 1), coverage_end=date(2013, 4, 3),
    )
    assert md["feasibility_class"] == "F2"
    assert md["state_count_feasibility_status"] == "unresolved"
    assert md["primary_10d_clustered_count"] >= 100


def test_orchestrator_f3_unreachable_without_state():
    # state always unresolved in the run -> never F3 even with huge counts
    assert m.assign_feasibility_class(
        True, 10_000_000, 100, "unresolved", True, False)[0] == "F2"


def test_orchestrator_f4_layout_mismatch_stops_before_counts(tmp_path):
    calls = []
    op = _make_fake_opener(date(2013, 4, 1), date(2013, 4, 3), calls=calls)
    avail = ["2013-04-0{}".format(i) for i in range(1, 4)]
    slots = {k: k for k in avail}
    slots["2013-04-02"] = "2013-04-03"  # date-unit mismatch
    md = m.run_count_only_feasibility(
        str(tmp_path), opener=op, available_keys=avail,
        slot_actual_keys=slots,
        coverage_start=date(2013, 4, 1), coverage_end=date(2013, 4, 3),
    )
    assert md["feasibility_class"] == "F4"
    assert md["archive_layout_status"] == "mismatch"
    assert md["stopped_before_count_computation"] is True
    # truthfulness: by-year / regime work did NOT run on the F4 short-circuit
    assert md["by_year_counts_reported"] is False
    assert md["gdelt_2013_regime_boundary_handled"] is False
    assert md["by_year_counts_status"] == "not_computed"
    assert md["regime_boundary_status"] == "not_evaluated"
    assert calls == []  # opener NEVER called: no retrieval before layout pass
    written = sorted(p.name for p in tmp_path.iterdir() if p.is_file())
    assert set(written) <= set(m.ALLOWED_OUTPUT_BASENAMES)


def test_orchestrator_f5_on_2023plus_protocol_breach(tmp_path):
    op = _make_fake_opener(date(2013, 4, 1), date(2013, 4, 3))
    avail = ["2013-04-0{}".format(i) for i in range(1, 4)]
    slots = {k: k for k in avail}
    slots["2013-04-01"] = "2023-01-01"  # 2023+ slot -> breach
    with pytest.raises(m.Protocol2023PlusBreach):
        m.run_count_only_feasibility(
            str(tmp_path), opener=op, available_keys=avail,
            slot_actual_keys=slots,
            coverage_start=date(2013, 4, 1), coverage_end=date(2013, 4, 3),
        )
    md_path = tmp_path / "count_feasibility_metadata.json"
    assert md_path.exists()
    import json as _j
    rec = _j.loads(md_path.read_text())
    assert rec["feasibility_class"] == "F5"
    # provenance: breach aborted the layout check itself
    assert rec["archive_layout_status"] == "breach_during_check"
    assert rec["by_year_counts_reported"] is False
    assert rec["gdelt_2013_regime_boundary_handled"] is False
    assert rec["by_year_counts_status"] == "not_computed"


def test_f5_breach_after_clean_layout_keeps_real_token(tmp_path,
                                                       monkeypatch):
    # layout passes cleanly, then a 2023+ row in a frozen file -> F5.
    # archive_layout_status must keep the truthful post-check token ("ok"),
    # NOT be overwritten to not_checked/breach_during_check.
    monkeypatch.setattr(m, "REAL_RETRIEVAL_ENABLED", True)
    avail = ["2013-04-0{}".format(i) for i in range(1, 4)]

    def opener(url, timeout=None):
        if url.rstrip("/").endswith("events"):
            return _Resp(
                b"20130401.export.CSV.zip 20130402.export.CSV.zip "
                b"20130403.export.CSV.zip")
        # frozen file content carries a synthetic 2023+ SQLDATE row
        return _Resp(_zip_bytes(["20230101"]))

    with pytest.raises(m.Protocol2023PlusBreach):
        m.run_count_only_feasibility(
            str(tmp_path), opener=opener, available_keys=avail,
            slot_actual_keys={k: k for k in avail},
            coverage_start=date(2013, 4, 1), coverage_end=date(2013, 4, 3),
        )
    import json as _j
    rec = _j.loads(
        (tmp_path / "count_feasibility_metadata.json").read_text())
    assert rec["feasibility_class"] == "F5"
    assert rec["archive_layout_status"] == "ok"  # truthful: layout WAS clean


def test_checked_path_pre_write_gate():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        # allow-listed basename passes and returns a joined path
        p = m._checked_path(d, "count_feasibility_metadata.json")
        assert p.endswith("count_feasibility_metadata.json")
        # non-allow-listed basename is rejected BEFORE any write
        for bad in ("spy_returns.csv", "model_fit.json", "car_table.csv",
                    "step2_lock.md", "counts_2023.csv", "anything.txt"):
            with pytest.raises(m.ProtocolBreach):
                m._checked_path(d, bad)
        # nothing was created by the rejected calls
        assert os.listdir(d) == []
        # post-hoc tripwire still present and consistent
        m._assert_outputs_allowed(d)  # empty dir -> no raise


def test_orchestrator_rejects_window_outside_pinned(tmp_path):
    op = _make_fake_opener(date(2004, 1, 1), date(2004, 1, 2))
    with pytest.raises(m.ProtocolBreach):
        m.run_count_only_feasibility(
            str(tmp_path), opener=op, available_keys=["2004"],
            coverage_start=date(2004, 1, 1), coverage_end=date(2004, 1, 2),
        )


# ── runner: refuses before any data access / dir; wired path under guards ────

def test_runner_refuses_without_guards_and_creates_no_dir(tmp_path,
                                                          monkeypatch):
    r = _load_runner()
    monkeypatch.delenv("LANE2_COUNT_FEASIBILITY_AUTHORIZED", raising=False)
    with pytest.raises(SystemExit):
        r.run_count_feasibility(str(tmp_path), cli_flag=True)
    assert not (tmp_path / "results").exists()  # no directory created


def test_runner_wired_path_writes_only_count_outputs(tmp_path, monkeypatch):
    r = _load_runner()
    import lane2_gdelt1_count_feasibility as src
    monkeypatch.setattr(r, "COUNT_FEASIBILITY_AUTHORIZED", True)
    monkeypatch.setenv("LANE2_COUNT_FEASIBILITY_AUTHORIZED", "1")
    op = _make_fake_opener(date(2013, 4, 1), date(2013, 4, 3))
    assert src.REAL_RETRIEVAL_ENABLED is False  # source ships inert
    out = r.run_count_feasibility(
        str(tmp_path), cli_flag=True, opener=op,
        coverage_start=date(2013, 4, 1), coverage_end=date(2013, 4, 3),
    )
    # fresh timestamped dir under results/lane2_gdelt1_count_feasibility/
    assert os.path.isdir(out)
    assert "lane2_gdelt1_count_feasibility" in out
    files = sorted(f for f in os.listdir(out)
                   if os.path.isfile(os.path.join(out, f)))
    assert set(files) <= set(src.ALLOWED_OUTPUT_BASENAMES)
    import json as _j
    with open(os.path.join(out, "count_feasibility_metadata.json")) as fh:
        md = _j.load(fh)
    assert md["post_run_safety_reset_required"] is True
    assert "post_run_safety_reset_note" in md
    assert md["archive_layout_status"] == "ok"
    # in-process flag restored; source constant remains inert
    assert src.REAL_RETRIEVAL_ENABLED is False


def test_runner_main_refusal_path_no_data(capsys, monkeypatch):
    r = _load_runner()
    monkeypatch.setattr(r, "COUNT_FEASIBILITY_AUTHORIZED", False)
    monkeypatch.setattr("sys.argv", ["prog"])
    r.main()
    assert "NOT authorized" in capsys.readouterr().out
