"""Adversarial synthetic-fixture tests for the Phase-1 Lane 2 TTG local
approved-fields archive scaffold.

These tests are SYNTHETIC-ONLY. They contact no network, read no real
GDELT / result / market / outcome files, and write only under pytest's
`tmp_path`. They pre-register the design-memo boundaries (no network, no
2023+, approved-fields-only, value-blind structural metadata only) and
prove the Phase-1 network boundary is impossible to cross by flipping
guards.
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

import lane2_type_tone_goldstein_local_archive as archive

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "scripts" / "run_lane2_type_tone_goldstein_local_archive_build.py"

# ── Synthetic fixture helpers (no real data) ─────────────────────────────────

# Forbidden-field sentinels placed in the input rows. None of these may ever
# appear in the archive output, the manifest, or any emitted text.
FORBIDDEN_SENTINELS = (
    "FORBID_ACTOR1NAME",
    "FORBID_EVENTCODE",
    "FORBID_EVENTBASECODE",
    "FORBID_EVENTROOTCODE",
    "FORBID_SOURCEURL",
    "FORBID_ACTIONGEO",
    "next_session_return",
    "FORBID_MARKET",
)

_N_COLS = 58  # GDELT 1.0 positional row width used for synthetic fixtures


def make_gdelt_row(
    sqldate: str,
    quadclass: str,
    goldsteinscale: str,
    nummentions: str,
    avgtone: str,
) -> str:
    """Build one synthetic TAB-separated GDELT 1.0 row with approved values
    at their documented indices and forbidden sentinels everywhere else."""
    cells = ["FILLER"] * _N_COLS
    cells[0] = "1000001"  # GLOBALEVENTID (ignored)
    cells[archive.DATE_FIELD_COLUMN_INDEX] = sqldate
    cells[6] = "FORBID_ACTOR1NAME"
    cells[16] = "FORBID_ACTOR1NAME"
    cells[26] = "FORBID_EVENTCODE"
    cells[27] = "FORBID_EVENTBASECODE"
    cells[28] = "FORBID_EVENTROOTCODE"
    cells[archive.QUADCLASS_COLUMN_INDEX] = quadclass
    cells[archive.GOLDSTEINSCALE_COLUMN_INDEX] = goldsteinscale
    cells[archive.NUMMENTIONS_COLUMN_INDEX] = nummentions
    cells[archive.AVGTONE_COLUMN_INDEX] = avgtone
    cells[36] = "FORBID_ACTIONGEO"
    cells[40] = "next_session_return"
    cells[50] = "FORBID_MARKET"
    cells[57] = "FORBID_SOURCEURL"
    return "\t".join(cells)


def make_payload(rows) -> bytes:
    return ("\n".join(rows) + "\n").encode("utf-8")


def make_zip_payload(rows, member_name="20130401.export.CSV") -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(member_name, ("\n".join(rows) + "\n"))
    return buf.getvalue()


class FetchSpy:
    """Spy standing in for an opener / fetch object. Records every call.
    Never performs I/O. A non-zero call count after a 2023+ enumeration
    would prove a seal breach — so tests assert it stays at zero."""

    def __init__(self):
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return b""


# ── 1. Approved fields retained exactly ──────────────────────────────────────

def test_approved_fields_retained_exactly():
    row = make_gdelt_row("20130401", "4", "-9.8765", "987654", "-87.654321")
    res = archive.parse_approved_rows(make_payload([row]))
    assert res.parsed_row_count == 1
    assert len(res.rows) == 1
    r = res.rows[0]
    assert set(r.keys()) == set(archive.APPROVED_FIELD_NAMES)
    assert r["sqldate"] == "2013-04-01"
    assert r["quadclass"] == "4"
    assert r["goldsteinscale"] == "-9.8765"
    assert r["nummentions"] == "987654"
    assert r["avgtone"] == "-87.654321"


# ── 2 & 3. Forbidden fields dropped; output contains none ────────────────────

def test_forbidden_fields_dropped_from_parsed_rows():
    row = make_gdelt_row("20140102", "1", "2.0", "10", "0.5")
    res = archive.parse_approved_rows(make_payload([row]))
    blob = json.dumps([dict(r) for r in res.rows])
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in blob, sentinel
    assert set(res.rows[0].keys()) == set(archive.APPROVED_FIELD_NAMES)


def test_archive_output_contains_no_forbidden_fields(tmp_path):
    rows = [
        make_gdelt_row("20130401", "4", "-9.8765", "987654", "-87.654321"),
        make_gdelt_row("20221231", "2", "3.3", "42", "1.25"),
    ]
    res = archive.parse_approved_rows(make_payload(rows))
    out = tmp_path / "approved_archive.csv"
    meta = archive.write_approved_archive_csv(res.rows, str(out))
    data = out.read_bytes()
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel.encode() not in data, sentinel
    assert b"FILLER" not in data
    assert meta["row_count"] == 2


# ── 4. 2023+ hard-errors at enumeration before any open ──────────────────────

def test_2023plus_enumeration_hard_errors():
    with pytest.raises(archive.Post2022SealBreach):
        archive.enumerate_source_universe(["2022-12-31", "2023-01-01"])


def test_in_window_enumeration_returns_sorted_unique():
    got = archive.enumerate_source_universe(
        ["2014-05-02", "2013-04-01", "2014-05-02"]
    )
    assert got == ["2013-04-01", "2014-05-02"]


# ── 5. Spy proves no post-2022 file opened after enumeration detects it ──────

def test_spy_no_post2022_file_opened(monkeypatch):
    monkeypatch.setattr(
        archive, "TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED", True
    )
    spy = FetchSpy()
    env = {archive.ENV_GUARD_NAME: "1"}
    with pytest.raises(archive.Post2022SealBreach):
        archive.run_local_archive_build(
            cli_flag=True,
            candidate_dates=["2014-01-01", "2023-06-15"],
            fetch_callable=spy,
            module_authorized=True,
            env=env,
        )
    assert spy.calls == [], "no file/opener may be touched after a 2023+ seal breach"


# ── 6. Extreme approved values never leak into manifest/logs ─────────────────

def test_extreme_values_not_in_manifest(tmp_path):
    rows = [make_gdelt_row("20130401", "4", "-9.8765", "987654", "-87.654321")]
    res = archive.parse_approved_rows(make_payload(rows))
    out = tmp_path / "approved_archive.csv"
    artifact = archive.write_approved_archive_csv(res.rows, str(out))
    manifest = archive.build_structural_manifest(
        source_date_universe=["2013-04-01"],
        per_file_status=[{
            "nominal_date": "2013-04-01",
            "status": "parsed",
            "row_count": 1,
            "sha256": artifact["sha256"],
            "byte_size": artifact["byte_size"],
        }],
        archive_artifacts=[artifact],
        total_row_count=1,
    )
    manifest_json = json.dumps(manifest)
    # Float/signed value tokens cannot occur in a hex hash, so scan the full
    # manifest for them.
    for tok in ("-9.8765", "-87.654321"):
        assert tok not in manifest_json, tok
    # The pure-digit token could in principle collide with a hex hash; scan a
    # hash-stripped copy.
    stripped = _strip_hashes(manifest)
    assert "987654" not in json.dumps(stripped)
    # ...but the values DO live in the archive itself (the archive is not a
    # summary).
    archive_text = out.read_text()
    for tok in ("-9.8765", "-87.654321", "987654"):
        assert tok in archive_text, tok


def _strip_hashes(obj):
    if isinstance(obj, dict):
        return {
            k: ("<sha256>" if k == "sha256" else _strip_hashes(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_strip_hashes(v) for v in obj]
    return obj


# ── 7. SHA-256 present and not misclassified as a value leak ─────────────────

def test_sha256_is_structural_and_present(tmp_path):
    rows = [make_gdelt_row("20130401", "1", "0.0", "5", "0.0")]
    res = archive.parse_approved_rows(make_payload(rows))
    out = tmp_path / "a.csv"
    artifact = archive.write_approved_archive_csv(res.rows, str(out))
    h = artifact["sha256"]
    assert isinstance(h, str) and len(h) == 64
    assert all(c in "0123456789abcdef" for c in h)
    manifest = archive.build_structural_manifest(
        source_date_universe=["2013-04-01"],
        per_file_status=[{"nominal_date": "2013-04-01", "status": "parsed",
                          "row_count": 1, "sha256": h, "byte_size": artifact["byte_size"]}],
        archive_artifacts=[artifact],
        total_row_count=1,
    )
    assert manifest["archive_artifacts"][0]["sha256"] == h


# ── 8. No value summaries emitted ────────────────────────────────────────────

_FORBIDDEN_SUMMARY_TERMS = (
    "mean", "median", "histogram", "distribution", "correlation",
    "z-score", "zscore", "stdev", "variance", "percentile", "quantile",
    "sample_row", "sample row", "aggregate", "_min", "_max", "minimum",
    "maximum",
)


def test_manifest_has_no_value_summary_keys(tmp_path):
    rows = [make_gdelt_row("20130401", "4", "9.0", "100", "5.5")]
    res = archive.parse_approved_rows(make_payload(rows))
    out = tmp_path / "a.csv"
    artifact = archive.write_approved_archive_csv(res.rows, str(out))
    manifest = archive.build_structural_manifest(
        source_date_universe=["2013-04-01"],
        per_file_status=[{"nominal_date": "2013-04-01", "status": "parsed",
                          "row_count": 1, "sha256": artifact["sha256"]}],
        archive_artifacts=[artifact],
        total_row_count=1,
    )
    keys = _all_keys(manifest)
    for k in keys:
        low = k.lower()
        for term in _FORBIDDEN_SUMMARY_TERMS:
            assert term not in low, (k, term)


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


# ── 9 & 10. Manifest structural-only; counts + hashes present ────────────────

def test_manifest_is_structural_only(tmp_path):
    rows = [make_gdelt_row("20130401", "4", "1.0", "7", "0.1")]
    res = archive.parse_approved_rows(make_payload(rows))
    out = tmp_path / "a.csv"
    artifact = archive.write_approved_archive_csv(res.rows, str(out))
    manifest = archive.build_structural_manifest(
        source_date_universe=["2013-04-01"],
        per_file_status=[{"nominal_date": "2013-04-01", "status": "parsed",
                          "row_count": 1, "sha256": artifact["sha256"],
                          "byte_size": artifact["byte_size"]}],
        archive_artifacts=[artifact],
        total_row_count=1,
    )
    # No per-row content / field values anywhere in the manifest.
    assert "rows" not in manifest
    assert manifest["total_approved_row_count"] == 1
    assert manifest["archive_artifacts"][0]["sha256"] == artifact["sha256"]
    assert manifest["archive_artifacts"][0]["row_count"] == 1
    # per_file_status carries only structural keys.
    allowed = {"nominal_date", "status", "row_count", "sha256", "byte_size"}
    for entry in manifest["per_file_status"]:
        assert set(entry.keys()).issubset(allowed)
    # boundary declarations present and asserting the firewalls.
    bd = manifest["boundary_declarations"]
    for flag in ("no_network_phase1", "no_2023plus", "no_market_data",
                 "no_outcome_data", "no_join", "no_forbidden_fields_retained",
                 "value_blind_structural_metadata_only"):
        assert bd[flag] is True


# ── 11. No market/outcome/join fields can pass through ───────────────────────

def test_no_market_outcome_join_in_schema():
    banned = ("next_session_return", "abs(next_session_return)", "market",
              "outcome", "join", "price", "volatility", "return")
    for name in archive.APPROVED_FIELD_NAMES:
        for b in banned:
            assert b not in name.lower(), (name, b)


def test_zip_payload_path_also_drops_forbidden(tmp_path):
    rows = [make_gdelt_row("20130401", "4", "-9.8765", "987654", "-87.654321")]
    res = archive.parse_approved_rows(make_zip_payload(rows), is_zip=True)
    assert res.parsed_row_count == 1
    out = tmp_path / "a.csv"
    archive.write_approved_archive_csv(res.rows, str(out))
    data = out.read_bytes()
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel.encode() not in data


# ── 12. Network impossible (no network libs in the module) ───────────────────

def test_module_imports_no_network_libraries():
    for name in ("urllib", "requests", "socket", "http"):
        assert not hasattr(archive, name), name
    src = Path(archive.__file__).read_text()
    # No functional network import lines in the module source.
    for bad in ("import urllib", "import requests", "import socket",
                "from urllib", "urlopen", "build_opener", "http://", "https://"):
        assert bad not in src, bad


def test_phase1_fetch_stub_raises_exact_message():
    with pytest.raises(archive.Phase1NetworkNotAuthorized) as ei:
        archive._phase1_fetch_disabled()
    assert str(ei.value) == "NETWORK NOT AUTHORIZED IN PHASE 1"


# ── 13 & 14. Guard gating ────────────────────────────────────────────────────

def test_guards_satisfied_requires_all_three():
    assert archive.guards_satisfied(True, module_authorized=True,
                                    env={archive.ENV_GUARD_NAME: "1"}) is True
    assert archive.guards_satisfied(False, module_authorized=True,
                                    env={archive.ENV_GUARD_NAME: "1"}) is False
    assert archive.guards_satisfied(True, module_authorized=False,
                                    env={archive.ENV_GUARD_NAME: "1"}) is False
    assert archive.guards_satisfied(True, module_authorized=True,
                                    env={}) is False


def test_build_refuses_without_guards():
    with pytest.raises(archive.ArchiveBuildRefused):
        archive.run_local_archive_build(
            cli_flag=False,
            candidate_dates=["2014-01-01"],
            fetch_callable=FetchSpy(),
            module_authorized=False,
            env={},
        )


def test_default_guard_blocks_runner_subprocess():
    env = dict(os.environ)
    env[archive.ENV_GUARD_NAME] = "1"  # env guard set...
    proc = subprocess.run(
        [sys.executable, str(CLI_SCRIPT), "--authorize-local-archive-build"],
        cwd=str(REPO_ROOT),
        env=env,  # ...and CLI flag passed, but module constant ships False
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.returncode == 2, proc.stderr.decode()
    assert b"REFUSED" in proc.stderr


# ── 15. All three guards flipped -> still hard-errors at network step ────────

def test_all_guards_flipped_still_network_hard_error(monkeypatch):
    monkeypatch.setattr(
        archive, "TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED", True
    )
    spy = FetchSpy()  # would record if any opener/fetch object were used
    env = {archive.ENV_GUARD_NAME: "1"}
    with pytest.raises(archive.Phase1NetworkNotAuthorized) as ei:
        archive.run_local_archive_build(
            cli_flag=True,
            candidate_dates=["2014-01-01"],
            fetch_callable=None,  # default = Phase-1 hard-error stub
            module_authorized=True,
            env=env,
        )
    assert str(ei.value) == "NETWORK NOT AUTHORIZED IN PHASE 1"
    # The spy was never wired in (default stub used) and no opener/socket
    # object exists to construct.
    assert spy.calls == []
    for name in ("urllib", "requests", "socket"):
        assert not hasattr(archive, name)


# ── 16. No real results/ writes; temp dir only ───────────────────────────────

def test_writes_only_under_tmp_path(tmp_path):
    rows = [make_gdelt_row("20130401", "1", "0.0", "1", "0.0")]
    res = archive.parse_approved_rows(make_payload(rows))
    out = tmp_path / "sub" / "approved_archive.csv"
    meta = archive.write_approved_archive_csv(res.rows, str(out))
    assert out.exists()
    assert str(tmp_path) in meta["output_path"]
    # Nothing was written under the repo results/ tree by this test.
    assert str(REPO_ROOT / "results") not in str(out)
