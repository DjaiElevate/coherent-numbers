"""Streaming-writer amendment tests (no-network, value-blind) for the TTG archive
build path.

Covers §5.1-§5.16: byte/order equivalence over offsets {-1,0,+1}; release depth
derived from ELIGIBILITY_DELTA_DAYS; retained-offset > EDD hard-fail; bounded
buffer high-water ~2*EDD+1; terminal post-loop flush; interior gap fan-out under
streaming; edge exclusions from the same mechanism; all-gap empty header-only byte
identity; hard-fail mid-stream atomicity; integrity/cache/fetch hard fail;
single-manifest-only abort; exact-58 hard fail; per-row guard distinct; public
return/provenance shape; local_archive unchanged; suite-wide no-network backstop.

All tests run under an autouse no-network backstop with the source gate False.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os

import pytest

import lane2_type_tone_goldstein_archive_fetch_path as fp
import lane2_type_tone_goldstein_local_archive as archive

LOCAL_ARCHIVE_PIN = "6a3d715e078c796391a930270c1f34a086e6ef9df2d663752d1922241ee5f40d"


# ── §5.16 / §5.10-backstop: suite-wide no-network guard ──────────────────────

@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    assert fp.REAL_FETCH_SOURCE_GATE_ENABLED is False

    def _boom(*_a, **_k):
        raise AssertionError("no-network backstop: _open_url must not be called")

    monkeypatch.setattr(fp, "_open_url", _boom)
    yield


# ── helpers (synthetic, value-blind) ─────────────────────────────────────────

_N = 58


def _row(sqldate_iso, ncols=_N):
    """A row with `ncols` columns; approved fields placed when wide enough.
    `sqldate_iso` is a YYYY-MM-DD; serialized SQLDATE token is YYYYMMDD."""
    cells = ["FILLER"] * ncols
    tok = sqldate_iso.replace("-", "")
    if ncols > archive.DATE_FIELD_COLUMN_INDEX:
        cells[archive.DATE_FIELD_COLUMN_INDEX] = tok
    for idx, val in ((archive.QUADCLASS_COLUMN_INDEX, "4"),
                     (archive.GOLDSTEINSCALE_COLUMN_INDEX, "1.0"),
                     (archive.NUMMENTIONS_COLUMN_INDEX, "5"),
                     (archive.AVGTONE_COLUMN_INDEX, "0.5")):
        if ncols > idx:
            cells[idx] = val
    return "\t".join(cells)


def _payload(rows):
    return ("\n".join(rows) + "\n").encode("utf-8")


def _d(y, m, day):
    return datetime.date(y, m, day)


def _iso(dt):
    return dt.isoformat()


def _mk_manifests(file_map):
    md5 = ["{}  {}".format(hashlib.md5(b).hexdigest(), fn) for fn, b in file_map.items()]
    siz = ["{} {}".format(len(b), fn) for fn, b in file_map.items()]
    return (("\n".join(md5) + "\n").encode(), ("\n".join(siz) + "\n").encode())


def _guarded(monkeypatch):
    monkeypatch.setattr(archive, "TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED", True)
    return dict(cli_flag=True, module_authorized=True, env={archive.ENV_GUARD_NAME: "1"})


class _Fetcher:
    def __init__(self, payloads):
        self.payloads = payloads
        self.dates = []

    def __call__(self, source_file_date, url):
        self.dates.append(source_file_date)
        if source_file_date not in self.payloads:
            raise AssertionError("gap/edge date must not be fetched: %s" % source_file_date)
        return self.payloads[source_file_date]


def _run(monkeypatch, tmp_path, present_dates, payloads, *, md5_b=None, size_b=None,
         fetcher=None, start=None, end=None, out="out"):
    g = _guarded(monkeypatch)
    if md5_b is None or size_b is None:
        file_map = {fp.expected_source_filename(d): payloads[d] for d in present_dates}
        md5_b, size_b = _mk_manifests(file_map)
    if fetcher is None:
        fetcher = _Fetcher(payloads)
    start = start or _iso(min(present_dates))
    end = end or _iso(max(present_dates))
    res = fp.run_bounded_integrity_build(
        start, end, out_dir=str(tmp_path / out),
        md5sums_bytes=md5_b, filesizes_bytes=size_b,
        fetch_callable=fetcher, **g)
    return res, fetcher


def _reference_archive_bytes(present_dates, payloads, available_dates, ref_path):
    """TEST-LOCAL accumulate-then-write reference (NOT in production): classify each
    present file in ascending order, accumulate retained rows, filter by the
    production coverage oracle over `available_dates`, write once with the
    production serializer. Returns (sha256, bytes)."""
    acc = []
    for d in sorted(present_dates):
        cls = archive.classify_payload_rows(
            payloads[d], source_file_date=d, is_zip=False,
            route_edge_incomplete=True, enforce_exact_columns=True)
        acc.extend(cls.retained_rows)
    primary = [r for r in acc
               if archive.fetched_set_fully_covers(datetime.date.fromisoformat(r["sqldate"]),
                                                    set(available_dates))]
    art = archive.write_approved_archive_csv(primary, ref_path)
    with open(ref_path, "rb") as fh:
        return art["sha256"], fh.read()


# ── §5.1 byte/order equivalence over offsets {-1, 0, +1} ─────────────────────

def test_byte_order_equivalence_offsets(monkeypatch, tmp_path):
    # contiguous span; each file f carries SQLDATE f-1 (+1), f (0), f+1 (-1).
    base = _d(2014, 6, 10)
    present = [base + datetime.timedelta(days=i) for i in range(6)]
    payloads = {}
    for f in present:
        rows = [_row(_iso(f - datetime.timedelta(days=1))),
                _row(_iso(f)),
                _row(_iso(f + datetime.timedelta(days=1)))]
        payloads[f] = _payload(rows)
    res, _ = _run(monkeypatch, tmp_path, present, payloads)
    streamed = res["archive_artifact"]["output_path"]
    with open(streamed, "rb") as fh:
        streamed_bytes = fh.read()
    ref_sha, ref_bytes = _reference_archive_bytes(
        present, payloads, set(present), str(tmp_path / "ref.csv"))
    assert streamed_bytes == ref_bytes
    assert res["archive_artifact"]["sha256"] == ref_sha
    assert hashlib.sha256(streamed_bytes).hexdigest() == ref_sha


# ── §5.2 release depth derived from ELIGIBILITY_DELTA_DAYS ────────────────────

def test_release_depth_derived_from_edd(monkeypatch):
    assert fp.streaming_release_depth() == 2 * archive.ELIGIBILITY_DELTA_DAYS
    # If the production eligibility constant changes, the rule follows it.
    monkeypatch.setattr(archive, "ELIGIBILITY_DELTA_DAYS", 2)
    assert fp.streaming_release_depth() == 4


# ── §5.3 retained offset > EDD hard-fails ────────────────────────────────────

def test_retained_offset_beyond_edd_hard_fails(monkeypatch, tmp_path):
    f = _d(2014, 6, 10)
    edd = archive.ELIGIBILITY_DELTA_DAYS
    bad_sqldate = f + datetime.timedelta(days=edd + 1)  # offset > EDD
    payloads = {f: _payload([_row(_iso(f)), _row(_iso(bad_sqldate))])}
    out = tmp_path / "out"
    with pytest.raises(fp.RetainedOffsetHardFail) as ei:
        _run(monkeypatch, tmp_path, [f], payloads, start=_iso(f), end=_iso(f))
    msg = str(ei.value)
    assert fp.expected_source_filename(f) in msg and bad_sqldate.isoformat() in msg
    assert not (out / "ttg_approved_fields_archive.csv").exists()
    assert not (out / "ttg_archive_provenance_manifest.json").exists()


# ── §5.4 bounded buffer high-water ~2*EDD+1, independent of length ────────────

def test_bounded_buffer_high_water(monkeypatch, tmp_path):
    expected_hw = 2 * archive.ELIGIBILITY_DELTA_DAYS + 1

    def hw_for(n_days):
        base = _d(2015, 1, 1)
        present = [base + datetime.timedelta(days=i) for i in range(n_days)]
        payloads = {f: _payload([_row(_iso(f))]) for f in present}
        res, _ = _run(monkeypatch, tmp_path, present, payloads, out="out%d" % n_days)
        return res["max_buffered_source_file_blocks"]

    hw_short = hw_for(30)
    hw_long = hw_for(120)
    assert hw_short == expected_hw
    assert hw_long == expected_hw  # does NOT grow with window length


# ── §5.5 terminal post-loop flush ────────────────────────────────────────────

def test_terminal_post_loop_flush(monkeypatch, tmp_path):
    base = _d(2016, 3, 10)
    present = [base + datetime.timedelta(days=i) for i in range(5)]  # 10..14
    payloads = {f: _payload([_row(_iso(f))]) for f in present}
    res, _ = _run(monkeypatch, tmp_path, present, payloads)
    last = present[-1]
    second_last = present[-2]
    # last covered prior day present; final boundary edge-excluded (no f+1 support).
    assert _iso(second_last) in res["primary_covered_sqldates"]
    assert _iso(last) not in res["primary_covered_sqldates"]
    assert _iso(last) in res["ledger_edge_excluded_sqldates"]


# ── §5.6 interior gap fan-out under streaming ────────────────────────────────

def test_interior_gap_fanout_streaming(monkeypatch, tmp_path):
    base = _d(2017, 5, 1)
    all_days = [base + datetime.timedelta(days=i) for i in range(10)]  # 05-01..05-10
    gap = all_days[4]  # 05-05
    present = [d for d in all_days if d != gap]
    payloads = {f: _payload([_row(_iso(f))]) for f in present}
    file_map = {fp.expected_source_filename(d): payloads[d] for d in present}  # gap absent in BOTH
    md5_b, size_b = _mk_manifests(file_map)
    fetcher = _Fetcher(payloads)
    res = fp.run_bounded_integrity_build(
        _iso(all_days[0]), _iso(all_days[-1]), out_dir=str(tmp_path / "out"),
        md5sums_bytes=md5_b, filesizes_bytes=size_b, fetch_callable=fetcher,
        **_guarded(monkeypatch))
    expected = sorted(t.isoformat() for t in all_days
                      if fp.sqldate_support_set(t) & {gap}
                      and not archive.fetched_set_fully_covers(t, set(present)))
    assert res["ledger_gap_uncovered_sqldates"] == expected
    assert expected == ["2017-05-04", "2017-05-05", "2017-05-06"]
    for iso in expected:
        assert iso not in res["primary_covered_sqldates"]
        assert "20170505.export.CSV.zip" in res["coverage_ledger"][iso]["gap_causes"]
    assert gap not in fetcher.dates  # never fetched


# ── §5.7 edge exclusions from the same support-aware mechanism ────────────────

def test_edge_exclusions_same_mechanism(monkeypatch, tmp_path):
    base = _d(2018, 7, 1)
    present = [base + datetime.timedelta(days=i) for i in range(6)]
    payloads = {f: _payload([_row(_iso(f))]) for f in present}
    res, _ = _run(monkeypatch, tmp_path, present, payloads)
    led = res["coverage_ledger"]
    assert led[_iso(present[0])]["state"] == fp.COVERAGE_EDGE_EXCLUDED
    assert led[_iso(present[-1])]["state"] == fp.COVERAGE_EDGE_EXCLUDED
    # same oracle the streamed row-filter uses:
    for d in (present[0], present[-1]):
        assert archive.fetched_set_fully_covers(d, set(present)) is False
    assert led[_iso(present[2])]["state"] == fp.COVERAGE_COVERED


# ── §5.8 all-gap window: completed empty build + header-only byte identity ────

def test_all_gap_window_empty_byte_identity(monkeypatch, tmp_path):
    g = _guarded(monkeypatch)
    md5_b = b"\n"
    size_b = b"\n"

    def _never(d, url):
        raise AssertionError("no daily fetch in all-gap window")

    out = tmp_path / "out"
    res = fp.run_bounded_integrity_build(
        "2019-02-01", "2019-02-10", out_dir=str(out),
        md5sums_bytes=md5_b, filesizes_bytes=size_b, fetch_callable=_never, **g)
    assert res["primary_covered_sqldates"] == []
    assert res["fetched_dates"] == []
    # header-only empty archive byte-identical to write_approved_archive_csv([]).
    ref = archive.write_approved_archive_csv([], str(tmp_path / "empty_ref.csv"))
    with open(res["archive_artifact"]["output_path"], "rb") as fh:
        streamed = fh.read()
    with open(str(tmp_path / "empty_ref.csv"), "rb") as fh:
        ref_bytes = fh.read()
    assert streamed == ref_bytes
    assert res["archive_artifact"]["sha256"] == ref["sha256"]
    # all applicable SQLDATEs gap-uncovered, causes named.
    assert res["ledger_covered_sqldates"] == []
    assert "20190205.export.CSV.zip" in res["coverage_ledger"]["2019-02-05"]["gap_causes"]


# ── §5.9 hard-fail mid-stream atomicity (no final archive/manifest) ──────────

def test_hard_fail_mid_stream_atomicity(monkeypatch, tmp_path):
    base = _d(2014, 8, 1)
    present = [base + datetime.timedelta(days=i) for i in range(5)]  # 01..05
    payloads = {f: _payload([_row(_iso(f))]) for f in present}
    # Make the LAST file non-58 so earlier blocks have already streamed to temp.
    bad = present[-1]
    payloads[bad] = _payload(["\t".join(["x"] * 45)])
    out = tmp_path / "out"
    with pytest.raises(fp.ColumnLayoutHardFail):
        _run(monkeypatch, tmp_path, present, payloads)
    # No final archive, no final manifest published (temp partial may remain).
    assert not (out / "ttg_approved_fields_archive.csv").exists()
    assert not (out / "ttg_archive_provenance_manifest.json").exists()


# ── §5.10 manifest-listed integrity failure stays hard fail (not a gap) ──────

def test_listed_integrity_failure_hard_fail(monkeypatch, tmp_path):
    base = _d(2015, 9, 1)
    present = [base + datetime.timedelta(days=i) for i in range(4)]
    payloads = {f: _payload([_row(_iso(f))]) for f in present}
    file_map = {fp.expected_source_filename(d): payloads[d] for d in present}
    md5_b, size_b = _mk_manifests(file_map)
    corrupt_at = present[2]

    def _corrupt(d, url):
        return b"CORRUPT" if d == corrupt_at else payloads[d]

    out = tmp_path / "out"
    with pytest.raises(fp.IntegrityVerificationError):
        fp.run_bounded_integrity_build(
            _iso(present[0]), _iso(present[-1]), out_dir=str(out),
            md5sums_bytes=md5_b, filesizes_bytes=size_b, fetch_callable=_corrupt,
            **_guarded(monkeypatch))
    assert not (out / "ttg_approved_fields_archive.csv").exists()


# ── §5.11 single-manifest-only aborts ────────────────────────────────────────

def test_single_manifest_only_aborts(monkeypatch, tmp_path):
    base = _d(2016, 10, 1)
    present = [base + datetime.timedelta(days=i) for i in range(4)]
    payloads = {f: _payload([_row(_iso(f))]) for f in present}
    file_map = {fp.expected_source_filename(d): payloads[d] for d in present}
    md5_b, size_b = _mk_manifests(file_map)
    drop = fp.expected_source_filename(present[1])
    size_b2 = ("\n".join(l for l in size_b.decode().splitlines() if drop not in l) + "\n").encode()
    out = tmp_path / "out"
    with pytest.raises(fp.IntegrityManifestError):
        fp.run_bounded_integrity_build(
            _iso(present[0]), _iso(present[-1]), out_dir=str(out),
            md5sums_bytes=md5_b, filesizes_bytes=size_b2,
            fetch_callable=_Fetcher(payloads), **_guarded(monkeypatch))
    assert not (out / "ttg_approved_fields_archive.csv").exists()


# ── §5.12 exact-58 file-level hard fail ──────────────────────────────────────

@pytest.mark.parametrize("ncols", [35, 45, 59])
def test_exact58_hard_fail(monkeypatch, tmp_path, ncols):
    f = _d(2017, 11, 5)
    payloads = {f: _payload([_row(_iso(f), ncols=ncols)])}
    out = tmp_path / "out"
    with pytest.raises(fp.ColumnLayoutHardFail) as ei:
        _run(monkeypatch, tmp_path, [f], payloads, start=_iso(f), end=_iso(f))
    assert fp.expected_source_filename(f) in str(ei.value)
    assert not (out / "ttg_approved_fields_archive.csv").exists()


# ── §5.13 per-row approved-index / short-row guard remains row-level ─────────

def test_per_row_short_row_guard_distinct():
    f = _d(2014, 6, 10)
    short = "\t".join(["x"] * 10)
    good = _row(_iso(f))
    cls = archive.classify_payload_rows(_payload([short, good]), source_file_date=f,
                                        enforce_exact_columns=False)
    assert cls.retained_row_count == 1
    assert cls.dropped_by_reason[archive.DROP_REASON_SHORT_ROW] == 1
    assert cls.dropped_by_reason[archive.DROP_REASON_COLUMN_COUNT_MISMATCH] == 0


# ── §5.14 public return/provenance shape preserved ───────────────────────────

def test_public_shape_preserved(monkeypatch, tmp_path):
    # No-gap happy path analogous to April: covered = interior, edges excluded.
    base = _d(2013, 4, 1)
    present = [base + datetime.timedelta(days=i) for i in range(30)]  # 04-01..04-30
    payloads = {f: _payload([_row(_iso(f))]) for f in present}
    res, _ = _run(monkeypatch, tmp_path, present, payloads)
    for k in ("manifest", "manifest_path", "archive_artifact", "universe",
              "fetched_dates", "tolerated_source_gaps", "primary_covered_sqldates",
              "coverage_ledger", "ledger_covered_sqldates",
              "ledger_edge_excluded_sqldates", "ledger_gap_uncovered_sqldates",
              "slice_edge_incomplete_sqldates", "window_edge_incomplete_days",
              "reconcile_status", "agg_raw_rows", "agg_date_eligibility_failure",
              "agg_edge_window_exclusion", "agg_classify_retained",
              "primary_archive_rows", "archive_sha256",
              "max_buffered_source_file_blocks", "streaming_release_depth"):
        assert k in res, k
    # no-gap happy-path coverage: 04-02 .. 04-29
    assert res["primary_covered_sqldates"] == ["2013-04-%02d" % d for d in range(2, 30)]
    assert res["ledger_edge_excluded_sqldates"] == ["2013-04-01", "2013-04-30"]
    assert res["ledger_gap_uncovered_sqldates"] == []
    assert res["tolerated_source_gaps"] == []
    # aggregate counters consistent + present in manifest too.
    m = res["manifest"]
    assert m["agg_raw_rows"] == res["agg_raw_rows"]
    assert m["primary_archive_rows"] == res["archive_artifact"]["row_count"]
    assert res["archive_sha256"] == res["archive_artifact"]["sha256"]
    assert m["boundary_declarations"]["streaming_archive_write"] is True
    # provenance manifest persisted to disk with the same keys.
    with open(res["manifest_path"]) as fh:
        disk = json.load(fh)
    assert disk["max_buffered_source_file_blocks"] == res["max_buffered_source_file_blocks"]


# ── §5.15 local_archive.py remains unchanged ─────────────────────────────────

def test_local_archive_unchanged():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "src", "lane2_type_tone_goldstein_local_archive.py")
    with open(path, "rb") as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    assert got == LOCAL_ARCHIVE_PIN, "local_archive.py must remain byte-identical"


# ── no production whole-window accumulator left behind ───────────────────────

def test_no_production_full_window_accumulator():
    # Scope to the REAL build path (run_bounded_integrity_build). The synthetic/
    # legacy harness run_phase2_archive_build is out of scope (it is not real-fetch
    # capable and only ever processes small synthetic test inputs).
    src = open(fp.__file__).read()
    start = src.index("def run_bounded_integrity_build(")
    nxt = src.find("\ndef ", start + 1)
    body = src[start: nxt if nxt != -1 else len(src)]
    code = "\n".join(ln for ln in body.splitlines() if not ln.lstrip().startswith("#"))
    # No whole-window row-list accumulator in the real build path.
    assert "classify_retained: List" not in code
    assert "primary_rows" not in code
    assert ".extend(cls.retained_rows)" not in code
    # The streaming buffer + writer are present.
    assert "_StreamingArchiveCsvWriter(" in code
    assert "held.append(" in code
