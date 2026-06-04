"""Gap-tolerance amendment tests (no-network, value-blind) for the TTG archive
fetch/build path.

Covers §6.1-§6.10 of the gap-tolerance amendment:
  - mutual manifest-attested absence tolerated as a source gap;
  - single-manifest-only aborts (inconsistency, not a gap);
  - manifest-listed fetch/verify/cache failures remain hard fail-closed;
  - one unified support-aware coverage rule for edges AND interior gaps;
  - interior-gap fan-out with the EXACT dependent SQLDATE set, derived from the
    production support rule (not a mock, not count>1);
  - exact-58 file-level hard fail (terminal abort, named file, not a gap);
  - the per-row approved-index / short-row guard stays a row-level structural
    guard distinct from source-gap tolerance;
  - degenerate all-gap window completes empty/gap-ledgered (no abort);
  - production reconcile/coverage/classification logic is driven directly.

All tests run under a suite-wide no-network backstop (_open_url patched to raise)
with the source gate confirmed False.
"""

from __future__ import annotations

import datetime
import hashlib

import pytest

import lane2_type_tone_goldstein_archive_fetch_path as fetch_path
import lane2_type_tone_goldstein_local_archive as archive


# ── §6.1 Suite-wide no-network backstop ──────────────────────────────────────

@pytest.fixture(autouse=True)
def _no_network_backstop(monkeypatch):
    """Patch the network primitive to raise across the whole amendment suite,
    and confirm the source gate is disarmed. Any accidental real fetch fails."""
    assert fetch_path.REAL_FETCH_SOURCE_GATE_ENABLED is False

    def _boom(*_a, **_k):
        raise AssertionError("no-network backstop: _open_url must not be called")

    monkeypatch.setattr(fetch_path, "_open_url", _boom)
    yield


# ── helpers (synthetic, value-blind) ─────────────────────────────────────────

_N_COLS = 58


def _row58(sqldate_yyyymmdd):
    """One exactly-58-column TAB row with a valid SQLDATE + approved values."""
    cells = ["FILLER"] * _N_COLS
    cells[archive.DATE_FIELD_COLUMN_INDEX] = sqldate_yyyymmdd
    cells[archive.QUADCLASS_COLUMN_INDEX] = "4"
    cells[archive.GOLDSTEINSCALE_COLUMN_INDEX] = "1.0"
    cells[archive.NUMMENTIONS_COLUMN_INDEX] = "5"
    cells[archive.AVGTONE_COLUMN_INDEX] = "0.5"
    return "\t".join(cells)


def _payload(rows):
    return ("\n".join(rows) + "\n").encode("utf-8")


def _april(day):
    return datetime.date(2013, 4, day)


def _april_payloads(days):
    return {_april(d): _payload([_row58("201304{:02d}".format(d))]) for d in days}


def _mk_manifests(file_map):
    """Build official-style md5sums + filesizes bytes from {filename: bytes}."""
    md5_lines = ["{}  {}".format(hashlib.md5(b).hexdigest(), fn) for fn, b in file_map.items()]
    size_lines = ["{} {}".format(len(b), fn) for fn, b in file_map.items()]
    return (("\n".join(md5_lines) + "\n").encode("utf-8"),
            ("\n".join(size_lines) + "\n").encode("utf-8"))


def _guarded(monkeypatch):
    monkeypatch.setattr(
        archive, "TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED", True)
    return dict(cli_flag=True, module_authorized=True,
                env={archive.ENV_GUARD_NAME: "1"})


class _Fetcher:
    """Serves payloads for present dates; records requested dates; raises if a
    gap date is ever requested (proving gaps are not fetched)."""

    def __init__(self, payloads):
        self.payloads = payloads
        self.dates = []

    def __call__(self, source_file_date, url):
        self.dates.append(source_file_date)
        if source_file_date not in self.payloads:
            raise AssertionError("gap/edge date must not be fetched: {}".format(source_file_date))
        return self.payloads[source_file_date]


def _run_april(monkeypatch, tmp_path, present_days, gap_days, *, out="out"):
    """Drive run_bounded_integrity_build over 2013-04-01..2013-04-30 with the
    given present/gap day sets via injected manifest bytes + injected fetcher."""
    g = _guarded(monkeypatch)
    payloads = _april_payloads(present_days)
    file_map = {fetch_path.expected_source_filename(_april(d)): payloads[_april(d)]
                for d in present_days}
    md5_b, size_b = _mk_manifests(file_map)  # gap days absent from BOTH manifests
    fetcher = _Fetcher(payloads)
    res = fetch_path.run_bounded_integrity_build(
        "2013-04-01", "2013-04-30", out_dir=str(tmp_path / out),
        md5sums_bytes=md5_b, filesizes_bytes=size_b,
        fetch_callable=fetcher, **g,
    )
    return res, fetcher


# ── §6.10 production logic driven directly (not doubles) ──────────────────────

def test_classify_manifest_presence_three_way():
    fns = [fetch_path.expected_source_filename(_april(d)) for d in (1, 2, 3)]
    md5 = {fns[0]: "x" * 32, fns[2]: "y" * 32}          # 1 both? no: see below
    size = {fns[0]: 10, fns[1]: 20}
    # fns[0]: in both; fns[1]: size only; fns[2]: md5 only.
    out = fetch_path.classify_manifest_presence(fns, md5, size)
    assert out["present_in_both"] == [fns[0]]
    assert out["single_manifest_only"] == [fns[1], fns[2]]
    assert out["absent_in_both"] == []


def test_support_set_pinned_to_production_oracle():
    # The support set must equal the EXACT 'needed' set of the production oracle
    # `fetched_set_fully_covers`: present -> covered; remove any one -> uncovered.
    t = _april(10)  # interior, in-window
    support = fetch_path.sqldate_support_set(t)
    assert archive.fetched_set_fully_covers(t, support) is True
    for missing in support:
        assert archive.fetched_set_fully_covers(t, support - {missing}) is False
    # spans three distinct source dates (not "own date only").
    assert support == {_april(9), _april(10), _april(11)}


# ── §6.2 mutual absence tolerated ────────────────────────────────────────────

def test_mutual_absence_tolerated_as_gap(monkeypatch, tmp_path):
    present = [d for d in range(1, 31) if d != 10]
    res, fetcher = _run_april(monkeypatch, tmp_path, present, [10])
    # gap recorded, not fetched.
    assert "20130410.export.CSV.zip" in res["tolerated_source_gaps"]
    assert _april(10) not in fetcher.dates
    # dependent SQLDATEs marked gap-uncovered and excluded from primary.
    assert "2013-04-10" in res["ledger_gap_uncovered_sqldates"]
    assert "2013-04-10" not in res["primary_covered_sqldates"]
    # completed build (manifest written), not aborted.
    assert res["manifest"]["coverage_summary"]["gap_uncovered_count"] >= 1


# ── §6.3 single-manifest-only aborts ─────────────────────────────────────────

def test_single_manifest_only_aborts(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    present = list(range(1, 31))
    payloads = _april_payloads(present)
    file_map = {fetch_path.expected_source_filename(_april(d)): payloads[_april(d)] for d in present}
    md5_b, size_b = _mk_manifests(file_map)
    # Drop 2013-04-12 from filesizes ONLY -> single-manifest-only -> abort.
    drop = fetch_path.expected_source_filename(_april(12))
    size_b2 = ("\n".join(ln for ln in size_b.decode().splitlines() if drop not in ln) + "\n").encode()
    out = tmp_path / "out"
    with pytest.raises(fetch_path.IntegrityManifestError):
        fetch_path.run_bounded_integrity_build(
            "2013-04-01", "2013-04-30", out_dir=str(out),
            md5sums_bytes=md5_b, filesizes_bytes=size_b2,
            fetch_callable=_Fetcher(payloads), **g,
        )
    assert not (out / "ttg_approved_fields_archive.csv").exists()


def test_single_manifest_only_not_classified_as_gap():
    fns = [fetch_path.expected_source_filename(_april(d)) for d in (1, 2)]
    md5 = {fns[0]: "a" * 32, fns[1]: "b" * 32}
    size = {fns[0]: 10}  # fns[1] missing from filesizes only
    out = fetch_path.classify_manifest_presence(fns, md5, size)
    assert out["single_manifest_only"] == [fns[1]]
    assert out["absent_in_both"] == []  # NOT a tolerated gap


# ── §6.4 manifest-listed integrity failure remains hard fail ─────────────────

def test_listed_file_md5_failure_hard_fails_even_with_a_gap(monkeypatch, tmp_path):
    # 2013-04-20 is a tolerated gap; 2013-04-10 is present-in-both but its fetched
    # bytes are corrupt -> IntegrityVerificationError (NOT reclassified as a gap).
    g = _guarded(monkeypatch)
    present = [d for d in range(1, 31) if d != 20]
    payloads = _april_payloads(present)
    file_map = {fetch_path.expected_source_filename(_april(d)): payloads[_april(d)] for d in present}
    md5_b, size_b = _mk_manifests(file_map)

    def _corrupt(source_file_date, url):
        if source_file_date == _april(10):
            return b"CORRUPT-bytes"
        return payloads[source_file_date]

    out = tmp_path / "out"
    with pytest.raises(fetch_path.IntegrityVerificationError):
        fetch_path.run_bounded_integrity_build(
            "2013-04-01", "2013-04-30", out_dir=str(out),
            md5sums_bytes=md5_b, filesizes_bytes=size_b,
            fetch_callable=_corrupt, **g,
        )
    assert not (out / "ttg_approved_fields_archive.csv").exists()


# ── §6.5 interior-gap fan-out: EXACT dependent set from the production rule ───

def test_interior_gap_fanout_exact_dependent_set(monkeypatch, tmp_path):
    gap_day = 15
    present = [d for d in range(1, 31) if d != gap_day]
    res, fetcher = _run_april(monkeypatch, tmp_path, present, [gap_day])

    universe = [_april(d) for d in range(1, 31)]
    available = set(_april(d) for d in present)
    gaps = {_april(gap_day)}
    # Expected gap-uncovered set DERIVED FROM the production support function:
    expected = sorted(
        t.isoformat() for t in universe
        if fetch_path.sqldate_support_set(t) & gaps   # support includes the gap
        and not archive.fetched_set_fully_covers(t, available)  # and not covered
    )
    assert res["ledger_gap_uncovered_sqldates"] == expected
    # Concrete fan-out: a single missing interior file uncovers MORE than its day.
    assert expected == ["2013-04-14", "2013-04-15", "2013-04-16"]
    # Each dependent SQLDATE excluded from primary; gap cause names the file.
    for iso in expected:
        assert iso not in res["primary_covered_sqldates"]
        assert "20130415.export.CSV.zip" in res["coverage_ledger"][iso]["gap_causes"]
    # The gap file itself was never fetched.
    assert _april(gap_day) not in fetcher.dates


# ── §6.6 edge and interior gap use the SAME support-aware rule ────────────────

def test_edge_and_interior_gap_same_rule(monkeypatch, tmp_path):
    gap_day = 15
    present = [d for d in range(1, 31) if d != gap_day]
    res, _ = _run_april(monkeypatch, tmp_path, present, [gap_day])
    led = res["coverage_ledger"]
    # Edge days are edge-excluded; interior-gap days are gap-uncovered; both come
    # from the same classify_sqldate_coverage / fetched_set_fully_covers mechanism.
    assert led["2013-04-01"]["state"] == fetch_path.COVERAGE_EDGE_EXCLUDED
    assert led["2013-04-30"]["state"] == fetch_path.COVERAGE_EDGE_EXCLUDED
    assert led["2013-04-15"]["state"] == fetch_path.COVERAGE_GAP_UNCOVERED
    available = set(_april(d) for d in present)
    # Same oracle reports all three uncovered:
    for iso in ("2013-04-01", "2013-04-30", "2013-04-15"):
        t = datetime.date.fromisoformat(iso)
        assert archive.fetched_set_fully_covers(t, available) is False
    # Interior days away from edges and gap are covered.
    assert led["2013-04-10"]["state"] == fetch_path.COVERAGE_COVERED


# ── §6.7 exact-58 file-level hard fail (also covered in fetch_path suite) ─────

def test_exact58_file_level_hard_fail_names_file(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    d = _april(10)
    bad_row = "\t".join(["x"] * 45)  # 45 cols, not 58
    payload = _payload([bad_row])
    fn = fetch_path.expected_source_filename(d)
    md5_b, size_b = _mk_manifests({fn: payload})
    out = tmp_path / "out"
    with pytest.raises(fetch_path.ColumnLayoutHardFail) as ei:
        fetch_path.run_bounded_integrity_build(
            "2013-04-10", "2013-04-10", out_dir=str(out),
            md5sums_bytes=md5_b, filesizes_bytes=size_b,
            fetch_callable=lambda dd, u: payload, **g,
        )
    assert fn in str(ei.value)
    assert not (out / "ttg_approved_fields_archive.csv").exists()


# ── §6.8 per-row approved-index / short-row guard stays row-level + distinct ──

def test_per_row_short_row_guard_is_row_level_not_gap():
    # Without exact-58 enforcement, a short row is a ROW-LEVEL structural drop
    # (short_row), NOT a source-file gap and NOT a column_count_mismatch.
    f = _april(10)
    short = "\t".join(["x"] * 10)             # below max approved index
    good = _row58("20130410")
    cls = archive.classify_payload_rows(
        _payload([short, good]), source_file_date=f, enforce_exact_columns=False)
    assert cls.retained_row_count == 1
    assert cls.dropped_by_reason[archive.DROP_REASON_SHORT_ROW] == 1
    assert cls.dropped_by_reason[archive.DROP_REASON_COLUMN_COUNT_MISMATCH] == 0
    # The short-row guard is a row-level reason in the closed structural set; it
    # is unrelated to manifest presence / source-gap tolerance.
    assert archive.DROP_REASON_SHORT_ROW in archive.CLOSED_DROP_REASONS


# ── §6.9 degenerate all-gap window completes empty / gap-ledgered ─────────────

def test_all_gap_window_completes_empty(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    # Manifests list NO April daily files at all -> every requested date is
    # absent-in-both -> all tolerated gaps.
    md5_b = b"\n"
    size_b = b"\n"

    def _never(source_file_date, url):
        raise AssertionError("no daily fetch in an all-gap window")

    out = tmp_path / "out"
    res = fetch_path.run_bounded_integrity_build(
        "2013-04-01", "2013-04-30", out_dir=str(out),
        md5sums_bytes=md5_b, filesizes_bytes=size_b,
        fetch_callable=_never, **g,
    )
    # Completed (archive written), empty, no fetches.
    assert (out / "ttg_approved_fields_archive.csv").exists()
    assert res["primary_covered_sqldates"] == []
    assert res["fetched_dates"] == []
    assert res["tolerated_gap_dates"] == ["2013-04-{:02d}".format(d) for d in range(1, 31)]
    # Every requested SQLDATE is ledgered; none covered; all uncovered states.
    led = res["coverage_ledger"]
    assert len(led) == 30
    assert res["ledger_covered_sqldates"] == []
    # Interior all-gap days are gap-uncovered with the causing file named.
    assert led["2013-04-15"]["state"] == fetch_path.COVERAGE_GAP_UNCOVERED
    assert "20130415.export.CSV.zip" in led["2013-04-15"]["gap_causes"]
    # No state outside the completed-build vocabulary.
    assert set(v["state"] for v in led.values()) <= {
        fetch_path.COVERAGE_COVERED,
        fetch_path.COVERAGE_EDGE_EXCLUDED,
        fetch_path.COVERAGE_GAP_UNCOVERED,
    }


# ── happy path still covered under gap-tolerance (no gaps) ────────────────────

def test_no_gap_happy_path_unchanged(monkeypatch, tmp_path):
    res, fetcher = _run_april(monkeypatch, tmp_path, list(range(1, 31)), [])
    assert res["tolerated_source_gaps"] == []
    assert res["primary_covered_sqldates"] == ["2013-04-{:02d}".format(d) for d in range(2, 30)]
    assert res["ledger_covered_sqldates"] == ["2013-04-{:02d}".format(d) for d in range(2, 30)]
    assert res["ledger_edge_excluded_sqldates"] == ["2013-04-01", "2013-04-30"]
    assert res["ledger_gap_uncovered_sqldates"] == []
