"""Lane 2 Type-Tone-Goldstein (TTG) archive — Phase-2 REAL fetch path.

This is the reviewed code module that ADDS the real GDELT network fetch path
the Phase-1 scaffold deliberately omitted. The real fetch is present here so a
future reviewer can byte-review it — but it is DISABLED by a source-level gate
and cannot be enabled by any runtime configuration.

═══════════════════════════════════════════════════════════════════════════════
NON-RUNTIME SOURCE GATE
═══════════════════════════════════════════════════════════════════════════════
`REAL_FETCH_SOURCE_GATE_ENABLED` ships ``False``. Enabling the real GDELT fetch
requires EDITING THAT LINE in this source file (a reviewed code change) AND a
separate, explicit execution authorization. It is intentionally NOT read from:
  - any environment variable,
  - any CLI flag,
  - any config file or local settings file,
  - any function parameter / default parameter,
  - any other one-line runtime switch.
No runtime configuration can flip it. With the gate ``False`` (as shipped), the
real fetch entrypoint HARD-ERRORS before constructing a URL, before importing
any network library, and before opening any connection. The runtime three-guard
build gate (module constant + CLI flag + env var) controls whether the *build
run* proceeds at all; it does NOT, and cannot, enable the network.

This module:
  - performs NO real network contact when imported or when the shipped gate is
    in force;
  - retains ONLY the five approved fields via the pure logic in
    `lane2_type_tone_goldstein_local_archive`;
  - is value-blind (structural / provenance metadata only);
  - touches NO market / outcome / join / 2023+ data and computes NO TTG
    feature or statistic.

Running a real build requires (a) editing the source gate below, (b) a separate
explicit execution-authorization prompt, and (c) the codebook/availability
preconditions — none of which are granted by importing or testing this module.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
from datetime import date, timedelta
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence

import lane2_type_tone_goldstein_local_archive as archive

# ═════════════════════════════════════════════════════════════════════════════
# SOURCE-LEVEL REAL-FETCH GATE — edit-to-enable only. NOT runtime-configurable.
# Do NOT wire this to os.environ, argparse, a config file, or a parameter.
REAL_FETCH_SOURCE_GATE_ENABLED = False
# ═════════════════════════════════════════════════════════════════════════════

# Exact, frozen real-fetch refusal message. Tests assert string equality.
REAL_FETCH_BLOCK_MESSAGE = (
    "REAL GDELT FETCH NOT AUTHORIZED: source gate "
    "REAL_FETCH_SOURCE_GATE_ENABLED is False. Enabling requires a reviewed "
    "source edit AND a separate execution authorization; it is not reachable "
    "via env var, CLI flag, config file, settings file, or parameter."
)

# GDELT 1.0 Event daily-update download base. The file-DOWNLOAD URL built from
# this base is provenance metadata (allowed in the manifest). It is a different
# namespace from the row-level GDELT `SOURCEURL` field (codebook idx 57), which
# is forbidden and never retained as a row column.
GDELT1_EVENT_BASE_URL = "http://data.gdeltproject.org/events/"

REAL_FETCH_TIMEOUT_SECONDS = 60

# Approved positional indices, independently re-derived from the committed
# codebook reference (docs/lane2_gdelt1_event_codebook_reference_v0.1.md,
# content SHA-256 3c5fa5bc054fbefaea2a26f9700ee827f2ff86a059d1625ffa127b10bf035a58):
# SQLDATE -> py idx 1, QuadClass -> 29, GoldsteinScale -> 30, NumMentions -> 31,
# AvgTone -> 34. The build verifies the module constants against this map and
# fails closed on mismatch (archive.assert_codebook_indices).
CANONICAL_CODEBOOK_DERIVED_INDICES: Dict[str, int] = {
    "sqldate": 1,
    "quadclass": 29,
    "goldsteinscale": 30,
    "nummentions": 31,
    "avgtone": 34,
}


class RealFetchNotAuthorized(archive.ArchiveBoundaryError):
    """Raised by the real fetch entrypoint while the source gate is False.

    Message is exactly `REAL_FETCH_BLOCK_MESSAGE`."""


class SyntheticOrchestratorViolation(archive.ArchiveBoundaryError):
    """Raised by `run_phase2_archive_build` (the synthetic/legacy harness) when
    it is asked to perform a real or default fetch. The bare harness is NOT a
    real-fetch-capable orchestrator: it requires an explicitly injected
    non-network fetcher and refuses the real-network entrypoints. The single
    real/default fetch entrypoint is `run_bounded_integrity_build`."""


# ── Provenance URL (file-download namespace, distinct from row SOURCEURL) ────

def build_source_file_url(source_file_date: date) -> str:
    """Build the file-download URL for a GDELT daily update file. This is the
    file-download URL (provenance metadata), NOT the row-level `SOURCEURL`
    field. The two namespaces are kept strictly separate.
    """
    name = archive.SOURCE_FILE_NAME_TEMPLATE.format(
        yyyymmdd=source_file_date.strftime("%Y%m%d")
    )
    return GDELT1_EVENT_BASE_URL + name


# ── Real fetch entrypoint (gated; hard-errors before any URL open) ───────────

def fetch_one_source_file(
    source_file_date: date,
    source_file_url: Optional[str] = None,
) -> bytes:
    """Real GDELT fetch entrypoint for one daily source file.

    Order of operations is load-bearing:
      1. CHECK THE SOURCE GATE FIRST. If `REAL_FETCH_SOURCE_GATE_ENABLED` is
         False (as shipped), raise `RealFetchNotAuthorized` immediately — before
         building any URL, before importing any network library, before opening
         any connection.
      2. (Only if the gate is enabled by a future source edit) re-assert the
         authorized source-file window / 2023+ seal on `source_file_date`.
      3. Build the download URL and open it via `_open_url`.

    The gate is checked unconditionally and is not influenced by any argument,
    environment variable, or config. No parameter can bypass it.
    """
    if not REAL_FETCH_SOURCE_GATE_ENABLED:
        raise RealFetchNotAuthorized(REAL_FETCH_BLOCK_MESSAGE)
    # --- Below is reachable only after a reviewed source edit + future auth. ---
    if not (archive.WINDOW_START <= source_file_date <= archive.WINDOW_END):
        raise archive.Post2022SealBreach(
            "source file date {} outside authorized window".format(
                source_file_date.isoformat()
            )
        )
    if source_file_url is None:
        source_file_url = build_source_file_url(source_file_date)
    return _open_url(source_file_url)


def _open_url(url: str, _opener: Optional[Any] = None) -> bytes:
    """Open a URL and return its bytes. Reached ONLY after the source gate has
    been enabled by a reviewed source edit.

    DEFENSE-IN-DEPTH SOURCE GATE: the FIRST statement re-checks
    `REAL_FETCH_SOURCE_GATE_ENABLED` and hard-errors while it is False — BEFORE
    the lazy `urllib` import and BEFORE any network open. This is belt-and-
    suspenders: it does not replace the higher-level gate in
    `fetch_one_source_file`; it guarantees that even a direct call to `_open_url`
    (bypassing the entrypoint) cannot import a network library or open a socket
    while the gate is disabled. The gate is a source literal — no env var, CLI
    flag, config/settings file, parameter, or runtime switch can flip it.

    The network library is imported lazily AFTER the gate check — so when the
    gate is False (shipped), no network library is imported at all. `_opener` is
    a future test seam; the shipped gate prevents this function from ever being
    reached in this dispatch.
    """
    if not REAL_FETCH_SOURCE_GATE_ENABLED:
        raise RealFetchNotAuthorized(
            REAL_FETCH_BLOCK_MESSAGE + " [_open_url defense-in-depth gate]"
        )
    # --- Below is reachable only after a reviewed source edit + future auth. ---
    import urllib.request  # lazy: only after the source gate passes

    opener = _opener if _opener is not None else urllib.request.build_opener()
    with opener.open(url, timeout=REAL_FETCH_TIMEOUT_SECONDS) as resp:
        return resp.read()


def fetch_manifest_bytes(
    url: str,
    *,
    manifest_fetch_callable: Optional[Callable[[str], bytes]] = None,
) -> bytes:
    """Acquire official-manifest bytes (`md5sums` / `filesizes`) for one URL.

    The DEFAULT real path routes through the SAME reviewed gated `_open_url` used
    for daily zips — so with `REAL_FETCH_SOURCE_GATE_ENABLED = False` (shipped)
    this hard-errors before any `urllib` import or network open, exactly like a
    daily fetch. There is NO separate `urllib` / `requests` / `curl` / `wget`
    route for manifests.

    `manifest_fetch_callable(url) -> bytes` is a synthetic/test-only seam so tests
    can supply in-memory manifest bytes without a network. The seam is rejected in
    a gate-enabled (real) session by the caller's seam-mode guard
    (`run_bounded_integrity_build`), so it cannot be used as a real-run bypass.
    """
    if manifest_fetch_callable is not None:
        return manifest_fetch_callable(url)
    return _open_url(url)


# ── SYNTHETIC/LEGACY build harness (cannot perform real fetches) ─────────────

# The real-network primitives the synthetic harness must never wire in. Used by
# an identity check so the bare harness cannot reach `_open_url` for real bytes.
def _real_fetch_entrypoints():
    return (fetch_one_source_file, fetch_stable, _open_url)


def run_phase2_archive_build(
    candidate_dates: Sequence[str],
    out_dir: str,
    *,
    cli_flag: bool = False,
    module_authorized: Optional[bool] = None,
    env: Optional[Mapping[str, str]] = None,
    fetch_callable: Optional[Callable[..., bytes]] = None,
    codebook_derived_indices: Optional[Mapping[str, int]] = None,
    route_edge_incomplete: bool = False,
    is_zip: bool = False,
    enforce_exact_columns: bool = True,
) -> Dict[str, Any]:
    """SYNTHETIC / LEGACY build harness — NOT a real-fetch-capable orchestrator.

    This harness exercises the classify/accumulate/manifest logic on bytes
    supplied by an INJECTED, NON-NETWORK `fetch_callable`. It deliberately does
    NOT default to the real fetch and cannot reach `_open_url` for real bytes:

      - `fetch_callable=None` -> raise `SyntheticOrchestratorViolation` (it does
        NOT silently fall back to the real gated fetch);
      - a `fetch_callable` that is one of the real-network entrypoints
        (`fetch_one_source_file` / `fetch_stable` / `_open_url`) -> raise.

    The single real/default fetch entrypoint for future real runs is
    `run_bounded_integrity_build`, which always applies manifest reconciliation,
    official MD5/size verification, exact-58 classification, and slice-aware
    coverage around the fetch. This harness has NONE of that wiring and is for
    synthetic classification/provenance tests only.

    Sequence: (0) refuse real/default fetch; (1) verify codebook indices;
    (2) three-guard run gate; (3) enumerate (2023+/pre-window hard-error);
    (4) per file: injected fetch -> classify -> accumulate; (5) write archive +
    value-agnostic provenance manifest.
    """
    # 0a. Defense-in-depth: this synthetic harness must never run during a
    # gate-enabled (real) session. If the source gate is True it fails closed
    # before any fetch/callable use, so it cannot be used as a real-run bypass.
    if REAL_FETCH_SOURCE_GATE_ENABLED:
        raise SyntheticOrchestratorViolation(
            "run_phase2_archive_build (synthetic/legacy harness) must not run while "
            "REAL_FETCH_SOURCE_GATE_ENABLED is True. Use run_bounded_integrity_build "
            "for any real-mode run."
        )
    # 0b. Synthetic-harness guard: refuse real/default fetch (footgun closure).
    if fetch_callable is None:
        raise SyntheticOrchestratorViolation(
            "run_phase2_archive_build is a synthetic/legacy harness and requires "
            "an explicitly injected non-network fetch_callable; it does NOT "
            "default to the real fetch. Use run_bounded_integrity_build for the "
            "real/default integrity-checked path."
        )
    if fetch_callable in _real_fetch_entrypoints():
        raise SyntheticOrchestratorViolation(
            "run_phase2_archive_build refuses a real-network fetch entrypoint as "
            "its fetcher; the bare harness cannot reach _open_url for real bytes. "
            "Use run_bounded_integrity_build for the real/default path."
        )

    # 1. Codebook index verification — fail closed before anything else.
    archive.assert_codebook_indices(
        codebook_derived_indices
        if codebook_derived_indices is not None
        else CANONICAL_CODEBOOK_DERIVED_INDICES
    )

    # 2. Three-guard run gate.
    if not archive.guards_satisfied(
        cli_flag, module_authorized=module_authorized, env=env
    ):
        raise archive.ArchiveBuildRefused(archive.REFUSAL_MESSAGE)

    # 3. Enumerate (2023+ / pre-window hard-error at enumeration).
    universe = archive.enumerate_source_universe(candidate_dates or [])

    # The §0 guard guarantees `fetch_callable` is a non-None, non-real fetcher.
    fetch = fetch_callable

    retained_rows: List[Dict[str, str]] = []
    per_file_provenance: List[Dict[str, Any]] = []
    edge_incomplete_days: set = set()

    for iso in universe:
        f_date = date.fromisoformat(iso)
        url = build_source_file_url(f_date)
        # `fetch` is the injected non-network synthetic fetcher (guaranteed by
        # the §0 guard); this harness performs no real network contact.
        payload = fetch(f_date, url)
        byte_hash = archive.sha256_hex(payload)
        cls = archive.classify_payload_rows(
            payload,
            source_file_date=f_date,
            is_zip=is_zip,
            route_edge_incomplete=route_edge_incomplete,
            enforce_exact_columns=enforce_exact_columns,
        )
        retained_rows.extend(cls.retained_rows)
        if cls.dropped_by_reason.get(archive.DROP_REASON_EDGE_WINDOW_EXCLUSION, 0):
            edge_incomplete_days.add(iso)
        per_file_provenance.append(
            archive.build_per_file_provenance_entry(
                source_file_date=f_date,
                source_file_url=url,
                attempted=True,
                opened=True,
                classification=cls,
                byte_hash=byte_hash,
                byte_size=len(payload),
                error_status=None,
            )
        )

    os.makedirs(out_dir, exist_ok=True)
    archive_path = os.path.join(out_dir, "ttg_approved_fields_archive.csv")
    artifact = archive.write_approved_archive_csv(retained_rows, archive_path)

    manifest = archive.build_phase2_provenance_manifest(
        source_file_window={
            "start": archive.WINDOW_START.isoformat(),
            "end": archive.WINDOW_END.isoformat(),
            "enumeration": "deterministic YYYYMMDD per-day; no 2023+; no pre-window",
        },
        per_file_provenance=per_file_provenance,
        archive_artifacts=[artifact],
        total_retained_row_count=len(retained_rows),
        edge_incomplete_day_count=len(edge_incomplete_days),
    )
    manifest_path = os.path.join(out_dir, "ttg_archive_provenance_manifest.json")
    with open(manifest_path, "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=False)

    return {
        "manifest": manifest,
        "manifest_path": manifest_path,
        "archive_artifact": artifact,
        "universe": universe,
    }


# ═════════════════════════════════════════════════════════════════════════════
# Official integrity-manifest + raw-cache verification + retry stability.
#
# These functions implement the real-run integrity checks the FUTURE bounded run
# will use. In THIS dispatch they operate ONLY on synthetic/local fixture bytes;
# no official manifest is fetched and no daily zip is downloaded. The official
# manifest URL templates are DEFINED here (provenance), but this module NEVER
# opens them (network remains behind the source gate / `_open_url`).
#
# Authority model: the OFFICIAL `md5sums` and `filesizes` entries are the
# authoritative integrity check; SHA-256 (of manifest bytes and of file bytes) is
# recorded as ADDITIONAL local provenance, not a substitute. All functions are
# value-blind: they operate on whole-file bytes and filenames only and never read,
# branch on, summarise, or bucket any TTG field value.
# ═════════════════════════════════════════════════════════════════════════════

# Official GDELT v1 event-directory integrity manifests (DEFINED, never opened
# in this dispatch). Reconciliation/verification below consumes manifest BYTES
# supplied by the caller; fetching these is a separate future authorization.
GDELT1_MD5SUMS_URL = "http://data.gdeltproject.org/events/md5sums"
GDELT1_FILESIZES_URL = "http://data.gdeltproject.org/events/filesizes"

# Where real runs will cache raw zips: under the gitignored data/raw/ tree.
# This module never creates this directory or writes into it in this dispatch;
# synthetic tests use pytest temp dirs instead.
RAW_CACHE_DIR = "data/raw/lane2_ttg_gdelt1_event_zip_cache"

_DAILY_ZIP_SUFFIX = ".export.CSV.zip"


class IntegrityManifestError(archive.ArchiveBoundaryError):
    """Raised when an expected bounded-slice file is missing from the official
    md5sums/filesizes manifest, or a manifest cannot be reconciled. Fail closed."""


class IntegrityVerificationError(archive.ArchiveBoundaryError):
    """Raised on an official MD5 mismatch or byte-size mismatch. Fail closed."""


class UnstableDownloadError(archive.ArchiveBoundaryError):
    """Raised when a retried download returns non-identical bytes. Fail closed."""


class CacheIntegrityError(archive.ArchiveBoundaryError):
    """Raised when a cached zip exists but fails official integrity verification.
    Cache presence NEVER bypasses verification; re-download requires a future
    explicit authorization. Fail closed."""


def expected_source_filename(source_file_date: date) -> str:
    """`date -> '<YYYYMMDD>.export.CSV.zip'` (daily event-file name)."""
    return archive.SOURCE_FILE_NAME_TEMPLATE.format(
        yyyymmdd=source_file_date.strftime("%Y%m%d")
    )


def expected_source_filenames(source_file_dates: Sequence[date]) -> List[str]:
    """Deterministic expected bounded source-file universe (filenames)."""
    return [expected_source_filename(d) for d in source_file_dates]


def _is_daily_zip_name(token: str) -> bool:
    """True iff `token` is an `<8 digits>.export.CSV.zip` daily event filename."""
    if not token.endswith(_DAILY_ZIP_SUFFIX):
        return False
    head = token[: -len(_DAILY_ZIP_SUFFIX)]
    return len(head) == 8 and head.isdigit()


def parse_md5sums(text: str) -> Dict[str, str]:
    """Parse official-style `md5sums` bytes into `{filename: md5hex}`.

    Official format is coreutils-style `<32-hex-md5>  <filename>`. This parser is
    tolerant of token order: on each line it locates a 32-hex-char token and a
    daily `*.export.CSV.zip` filename token. Only daily event-file entries are
    retained (GKG/mentions/other lines are ignored). Value-blind: filenames and
    hex digests only.
    """
    out: Dict[str, str] = {}
    for line in text.splitlines():
        toks = line.split()
        if not toks:
            continue
        fname = next((t for t in toks if _is_daily_zip_name(t)), None)
        md5 = next(
            (
                t.lower()
                for t in toks
                if len(t) == 32 and all(c in "0123456789abcdefABCDEF" for c in t)
            ),
            None,
        )
        if fname is not None and md5 is not None:
            out[fname] = md5
    return out


def parse_filesizes(text: str) -> Dict[str, int]:
    """Parse official-style `filesizes` bytes into `{filename: byte_size}`.

    Tolerant of token order: on each line it locates a daily `*.export.CSV.zip`
    filename token and an all-digit byte-size token. Only daily event-file
    entries are retained. Value-blind: filenames and integer sizes only.
    """
    out: Dict[str, int] = {}
    for line in text.splitlines():
        toks = line.split()
        if not toks:
            continue
        fname = next((t for t in toks if _is_daily_zip_name(t)), None)
        size = next((t for t in toks if t.isdigit()), None)
        if fname is not None and size is not None:
            out[fname] = int(size)
    return out


def manifest_provenance(
    md5sums_bytes: Optional[bytes] = None,
    filesizes_bytes: Optional[bytes] = None,
) -> Dict[str, Any]:
    """Record SHA-256 + byte size of supplied manifest bytes as provenance.

    SHA-256 here is LOCAL provenance of the manifest artifacts; the official MD5
    and size entries inside them remain the authoritative file-integrity check.
    """
    prov: Dict[str, Any] = {
        "md5sums_url": GDELT1_MD5SUMS_URL,
        "filesizes_url": GDELT1_FILESIZES_URL,
    }
    if md5sums_bytes is not None:
        prov["md5sums_sha256"] = archive.sha256_hex(md5sums_bytes)
        prov["md5sums_byte_size"] = len(md5sums_bytes)
    if filesizes_bytes is not None:
        prov["filesizes_sha256"] = archive.sha256_hex(filesizes_bytes)
        prov["filesizes_byte_size"] = len(filesizes_bytes)
    return prov


def reconcile_universe_against_manifests(
    expected_filenames: Sequence[str],
    md5sums: Mapping[str, str],
    filesizes: Mapping[str, int],
) -> Dict[str, Any]:
    """Fail closed unless EVERY expected bounded-slice file is present in BOTH
    the official md5sums and filesizes manifests.

    Returns a value-agnostic reconciliation status on success. Raises
    `IntegrityManifestError` if any expected file is missing from either
    manifest.
    """
    missing_md5 = [f for f in expected_filenames if f not in md5sums]
    missing_size = [f for f in expected_filenames if f not in filesizes]
    if missing_md5:
        raise IntegrityManifestError(
            "expected file(s) missing from official md5sums: {}".format(missing_md5)
        )
    if missing_size:
        raise IntegrityManifestError(
            "expected file(s) missing from official filesizes: {}".format(missing_size)
        )
    return {
        "expected_count": len(expected_filenames),
        "present_in_md5sums": len(expected_filenames),
        "present_in_filesizes": len(expected_filenames),
        "missing_from_md5sums": [],
        "missing_from_filesizes": [],
        "reconciled_ok": True,
    }


# ── Gap-tolerance amendment: manifest presence classification + coverage ─────
#
# Tolerance is MUTUAL-manifest-attested absence only. A date absent from BOTH
# official manifests is a tolerated source gap (not fetched); a date present in
# exactly one manifest is inconsistency/corruption and aborts. Fetch / verify /
# cache failures for a present-in-both date remain hard fail-closed (handled in
# the daily loop) and are NEVER reclassified as gaps.


class ColumnLayoutHardFail(archive.ArchiveBoundaryError):
    """Raised when a manifest-listed source file violates exact-58 file-level
    layout conformance under `enforce_exact_columns`. Terminal abort: the file is
    NOT silently dropped and NOT reclassified as a tolerated gap."""


# Per-SQLDATE coverage-ledger vocabulary for a COMPLETED build (only these three;
# a hard-fail finding is a terminal abort, never a per-SQLDATE archive label).
COVERAGE_COVERED = "covered"
COVERAGE_EDGE_EXCLUDED = "edge-excluded"
COVERAGE_GAP_UNCOVERED = "gap-uncovered"


def classify_manifest_presence(
    expected_filenames: Sequence[str],
    md5sums: Mapping[str, str],
    filesizes: Mapping[str, int],
) -> Dict[str, Any]:
    """Classify each expected (authorized) source filename by manifest presence:

      - `present_in_both`:       in md5sums AND filesizes -> mandatory file;
      - `absent_in_both`:        in NEITHER -> tolerated source gap (no fetch);
      - `single_manifest_only`:  in exactly one -> manifest inconsistency.

    Pure / value-blind (filenames + presence only); raises nothing. Callers must
    abort on any `single_manifest_only` before daily processing.
    """
    present_in_both: List[str] = []
    absent_in_both: List[str] = []
    single_manifest_only: List[str] = []
    expected = list(expected_filenames)
    for f in expected:
        in_md5 = f in md5sums
        in_size = f in filesizes
        if in_md5 and in_size:
            present_in_both.append(f)
        elif (not in_md5) and (not in_size):
            absent_in_both.append(f)
        else:
            single_manifest_only.append(f)
    return {
        "expected_count": len(expected),
        "present_in_both": present_in_both,
        "absent_in_both": absent_in_both,
        "single_manifest_only": single_manifest_only,
    }


def sqldate_support_set(sqldate: date) -> set:
    """Source-file dates that can contribute eligible rows to `sqldate` under the
    production availability convention `source_file_date <= SQLDATE + 1` (offset
    buckets {+1, 0, -1}): `{sqldate-1, sqldate, sqldate+ELIGIBILITY_DELTA_DAYS}`.

    This mirrors the `needed` set used by the production coverage oracle
    `archive.fetched_set_fully_covers`. A test pins the two together so this
    derivation cannot silently drift from the production rule. NOT hand-coded as
    "missing file only affects its own SQLDATE": the set spans 3 source dates.
    """
    d = archive.ELIGIBILITY_DELTA_DAYS
    return {
        sqldate - timedelta(days=1),
        sqldate,
        sqldate + timedelta(days=d),
    }


def classify_sqldate_coverage(
    sqldate: date,
    available_source_dates: Iterable[date],
    gap_source_dates: Iterable[date],
) -> Dict[str, Any]:
    """ONE unified support-aware coverage rule for start-edge, slice-edge, and
    interior manifest-gap days.

    `available_source_dates` = source-file dates present-in-both and successfully
    available (in-window). `gap_source_dates` = absent-in-both tolerated gaps.

    Returns `{state, missing_support, gap_causes}`:
      - `covered`       iff the production oracle `archive.fetched_set_fully_covers`
                        reports every support file available;
      - `gap-uncovered` iff any missing support file is a manifest gap
                        (gap precedence; `gap_causes` names the missing gap file(s));
      - `edge-excluded` iff uncovered but no missing support file is a gap (the
                        missing support lies outside the window / requested slice).

    The covered/not decision is delegated to the production oracle; the support
    set comes from `sqldate_support_set` (pinned to the oracle by test).
    """
    available = set(available_source_dates)
    gaps = set(gap_source_dates)
    if archive.fetched_set_fully_covers(sqldate, available):
        return {"state": COVERAGE_COVERED, "missing_support": [], "gap_causes": []}
    missing = sorted(sqldate_support_set(sqldate) - available)
    missing_gaps = [d for d in missing if d in gaps]
    if missing_gaps:
        return {
            "state": COVERAGE_GAP_UNCOVERED,
            "missing_support": [d.isoformat() for d in missing],
            "gap_causes": [expected_source_filename(d) for d in missing_gaps],
        }
    return {
        "state": COVERAGE_EDGE_EXCLUDED,
        "missing_support": [d.isoformat() for d in missing],
        "gap_causes": [],
    }


def verify_file_integrity(
    filename: str,
    file_bytes: bytes,
    md5sums: Mapping[str, str],
    filesizes: Mapping[str, int],
) -> Dict[str, Any]:
    """Verify one file's bytes against the official MD5 + byte size. Fail closed.

    Raises `IntegrityManifestError` if no official entry exists, and
    `IntegrityVerificationError` on an MD5 mismatch or byte-size mismatch.
    Records SHA-256 as additional local provenance. Value-blind (whole-file
    bytes only).
    """
    if filename not in md5sums:
        raise IntegrityManifestError(
            "no official md5sums entry for {}".format(filename)
        )
    if filename not in filesizes:
        raise IntegrityManifestError(
            "no official filesizes entry for {}".format(filename)
        )
    official_md5 = md5sums[filename].lower()
    official_size = int(filesizes[filename])
    computed_md5 = archive.md5_hex(file_bytes)
    computed_size = len(file_bytes)
    if computed_md5 != official_md5:
        raise IntegrityVerificationError(
            "MD5 mismatch for {}: official={} computed={}".format(
                filename, official_md5, computed_md5
            )
        )
    if computed_size != official_size:
        raise IntegrityVerificationError(
            "byte-size mismatch for {}: official={} computed={}".format(
                filename, official_size, computed_size
            )
        )
    return {
        "filename": filename,
        "byte_size": computed_size,
        "official_md5": official_md5,
        "computed_md5": computed_md5,
        "md5_ok": True,
        "size_ok": True,
        "sha256_local_provenance": archive.sha256_hex(file_bytes),
        "integrity_status": "verified",
    }


def verify_cached_zip(
    cache_path: str,
    filename: str,
    md5sums: Mapping[str, str],
    filesizes: Mapping[str, int],
) -> Dict[str, Any]:
    """Re-verify a cached zip against official MD5 + size BEFORE use.

    Reads bytes from `cache_path` (a local file; real runs place it under
    `data/raw/...`, synthetic tests use a temp dir) and verifies them. Cache
    presence NEVER bypasses verification. On any integrity failure, raises
    `CacheIntegrityError` (fail closed); re-download requires a future explicit
    authorization and is NOT performed here. Returns a value-agnostic status with
    cache path, byte size, MD5, SHA-256, and integrity status.
    """
    with open(cache_path, "rb") as fh:
        data = fh.read()
    try:
        status = verify_file_integrity(filename, data, md5sums, filesizes)
    except (IntegrityVerificationError, IntegrityManifestError) as exc:
        raise CacheIntegrityError(
            "cached zip {} failed official integrity ({}); fail closed, "
            "re-download requires separate authorization".format(cache_path, exc)
        )
    status = dict(status)
    status["cache_path"] = cache_path
    status["source"] = "cache"
    return status


def fetch_stable(
    source_file_date: date,
    *,
    fetch_callable: Optional[Callable[..., bytes]] = None,
    attempts: int = 2,
) -> bytes:
    """Fetch a file `attempts` times and require byte-identical results.

    A retried download that returns non-identical bytes is treated as unstable
    and fails closed (`UnstableDownloadError`). The DEFAULT `fetch_callable` is
    the gated real fetch (`fetch_one_source_file`), which hard-errors before any
    network contact; synthetic tests inject a non-network callable. This function
    performs no network access itself.
    """
    if attempts < 2:
        raise ValueError("fetch_stable requires attempts >= 2 to assess stability")
    fetch = fetch_callable if fetch_callable is not None else fetch_one_source_file
    url = build_source_file_url(source_file_date)
    first = fetch(source_file_date, url)
    first_md5 = archive.md5_hex(first)
    for _ in range(attempts - 1):
        nxt = fetch(source_file_date, url)
        if archive.md5_hex(nxt) != first_md5:
            raise UnstableDownloadError(
                "unstable download for {}: retried bytes differ".format(
                    source_file_date.isoformat()
                )
            )
    return first


# ═════════════════════════════════════════════════════════════════════════════
# WIRED bounded-run orchestration — the SINGLE real/default fetch entrypoint.
#
# This is the one orchestrator the future bounded real run will use. It wires the
# already-reviewed integrity primitives together in a fixed order so that the
# real-bytes path is ALWAYS: manifest reconciliation -> (cache verify | stable
# fetch) -> official MD5/size verification -> exact-58 classification ->
# slice-aware coverage. There is NO bare `fetch -> classify` real path: the
# synthetic harness `run_phase2_archive_build` cannot reach `_open_url` (it
# refuses real/default fetch), and the only orchestrator whose default byte
# source is the real gated fetch is THIS function — and it applies integrity
# unconditionally to whatever bytes it receives, so an injected fetcher cannot
# bypass the checks either.
#
# In THIS dispatch the function is exercised only with synthetic manifest bytes,
# synthetic fixture daily bytes, injected non-network fetchers, and pytest temp
# cache dirs. The shipped source gate keeps the real default inert.
# ═════════════════════════════════════════════════════════════════════════════


def _date_range_inclusive(start_iso: str, end_iso: str) -> List[date]:
    """Every civil date from `start_iso` to `end_iso` inclusive (structural)."""
    start = date.fromisoformat(start_iso)
    end = date.fromisoformat(end_iso)
    if end < start:
        raise ValueError("end_date {} precedes start_date {}".format(end_iso, start_iso))
    out: List[date] = []
    d = start
    while d <= end:
        out.append(d)
        d = d + timedelta(days=1)
    return out


class RetainedOffsetHardFail(archive.ArchiveBoundaryError):
    """Raised when a manifest-listed source file yields a retained row whose
    forward offset `SQLDATE - source_file_date` exceeds `ELIGIBILITY_DELTA_DAYS`.

    The bounded sliding-window release depth (`2 * ELIGIBILITY_DELTA_DAYS`) and the
    support model both assume retained rows are not forward-dated beyond
    `ELIGIBILITY_DELTA_DAYS`. A row beyond that bound is a terminal hard-fail
    finding: NOT streamed, NOT silently dropped, NOT a tolerated gap, and never a
    completed archive."""


def streaming_release_depth() -> int:
    """Release/finality depth, DERIVED from the production
    `archive.ELIGIBILITY_DELTA_DAYS` (not a hard-coded magic number).

    A source file dated `f` can carry retained rows up to SQLDATE `f + EDD`
    (offset `+EDD`); coverage of SQLDATE `s` needs support through `s + EDD`, so a
    block for file `b` is final once source dates through `b + 2*EDD` are final.
    Hence release depth = `2 * EDD`; the held-block high-water is bounded around
    `2*EDD + 1`."""
    return 2 * archive.ELIGIBILITY_DELTA_DAYS


class _StreamingArchiveCsvWriter:
    """Bounded streaming writer that reproduces `write_approved_archive_csv`
    BYTE-FOR-BYTE while writing incrementally to a temp file.

    Reuses the production approved field order (`archive.APPROVED_FIELD_NAMES`) and
    the identical CSV serialization semantics (`csv.writer(lineterminator="\\n")`,
    UTF-8) so the streamed bytes equal the single-call output for the same row
    sequence (each `writerow` is independent; block boundaries fall on ASCII
    newlines, so concatenation-of-encodes == encode-of-concatenation). The SHA-256
    is computed incrementally and equals `archive.sha256_hex` over the full bytes.
    The header is emitted on construction, so a zero-row build yields the same
    header-only bytes as `write_approved_archive_csv([])`.
    """

    def __init__(self, temp_path: str) -> None:
        self.temp_path = temp_path
        self._fh = open(temp_path, "wb")
        self._hash = hashlib.sha256()
        self.byte_size = 0
        self.row_count = 0
        self._closed = False
        self._emit([list(archive.APPROVED_FIELD_NAMES)])  # header, once

    def _emit(self, rows_as_lists: Sequence[Sequence[str]]) -> None:
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        for r in rows_as_lists:
            w.writerow(r)
        data = buf.getvalue().encode("utf-8")
        self._fh.write(data)
        self._hash.update(data)
        self.byte_size += len(data)

    def write_row(self, row: Mapping[str, str]) -> None:
        self._emit([[row[name] for name in archive.APPROVED_FIELD_NAMES]])
        self.row_count += 1

    @property
    def sha256(self) -> str:
        return self._hash.hexdigest()

    def close(self) -> None:
        if not self._closed:
            self._fh.close()
            self._closed = True


def run_bounded_integrity_build(
    start_date: str,
    end_date: str,
    out_dir: str,
    *,
    md5sums_bytes: Optional[bytes] = None,
    filesizes_bytes: Optional[bytes] = None,
    manifest_fetch_callable: Optional[Callable[[str], bytes]] = None,
    cli_flag: bool = False,
    module_authorized: Optional[bool] = None,
    env: Optional[Mapping[str, str]] = None,
    cache_dir: Optional[str] = None,
    fetch_callable: Optional[Callable[..., bytes]] = None,
    codebook_derived_indices: Optional[Mapping[str, int]] = None,
    is_zip: bool = False,
    fetch_attempts: int = 2,
    write_cache: bool = True,
) -> Dict[str, Any]:
    """Wired, integrity-checked bounded-run orchestration (single real entrypoint).

    Fixed order (fail closed at every step):
      1.  Verify codebook indices.
      2.  Three-guard run gate.
      3.  Build the bounded source-file universe from start/end and enumerate
          (rejects any date outside the authorized window and any 2023+ date
          BEFORE any fetch/open).
      4.  ACQUIRE the official manifests (after enumeration, before daily
          processing): if `md5sums_bytes` / `filesizes_bytes` are not supplied,
          fetch them through `fetch_manifest_bytes` -> the SAME gated `_open_url`
          path used for daily zips (default real path). Then compute manifest
          provenance (SHA-256 + size) and parse official-style md5sums/filesizes.
      5.  Classify the bounded universe against BOTH manifests (gap-tolerant):
          present-in-both -> mandatory; absent-in-both -> tolerated source gap
          (NO fetch); single-manifest-only -> manifest inconsistency, abort
          before daily processing.
      6.  Per PRESENT-IN-BOTH source date only (gaps not fetched):
          a. cache check first: if a cached zip exists, `verify_cached_zip`
             re-verifies official MD5/size before use (CacheIntegrityError on
             failure; no silent re-download);
          b. else `fetch_stable` (retry-stability) via the injected fetcher
             (default = real gated fetch), then `verify_file_integrity`
             (official MD5/size; SHA-256 recorded as local provenance), then
             write the verified bytes to cache (after verification only);
          c. `classify_payload_rows(..., enforce_exact_columns=True)`, then an
             exact-58 FILE-LEVEL hard-fail check (any column-count deviation in a
             manifest-listed file is a terminal `ColumnLayoutHardFail`, never a
             silent drop and never a gap).
          Integrity / stable-retry / cache failures for a present-in-both file
          remain hard fail-closed and are NEVER reclassified as gaps.
      7.  ONE unified support-aware coverage rule (same for start-edge, slice-edge,
          and interior manifest gaps): re-filter classify survivors with the
          production oracle `fetched_set_fully_covers` against the AVAILABLE source
          set (present-in-both, gaps removed); build a per-SQLDATE coverage ledger
          (`covered` / `edge-excluded` / `gap-uncovered`) over the requested window.
          A missing interior source file strands every SQLDATE whose support set
          includes it (fan-out), all named in the ledger.
      8.  Write the approved-fields archive (primary, covered rows only) and a
          value-agnostic provenance manifest incl. the coverage ledger. A window
          that is entirely absent-in-both completes as an empty, fully
          gap-ledgered build (no abort, no fetch).

    Manifest acquisition: `md5sums_bytes` / `filesizes_bytes` /
    `manifest_fetch_callable` / `fetch_callable` are SYNTHETIC/TEST-ONLY seams.
    In the future real/default path none of them is supplied: manifests are
    fetched through the gated `_open_url`, and daily bytes through `fetch_stable`
    -> the gated fetch. In a gate-enabled (real) session, supplying ANY of those
    seams fails closed (seam-mode guard below), so the seams cannot be used as a
    real-run bypass. Integrity / exact-58 / slice coverage are applied
    unconditionally to whatever bytes are obtained. Value-blind throughout.
    """
    # 1. Codebook index verification (fail closed before anything else).
    archive.assert_codebook_indices(
        codebook_derived_indices
        if codebook_derived_indices is not None
        else CANONICAL_CODEBOOK_DERIVED_INDICES
    )

    # 2. Three-guard run gate.
    if not archive.guards_satisfied(
        cli_flag, module_authorized=module_authorized, env=env
    ):
        raise archive.ArchiveBuildRefused(archive.REFUSAL_MESSAGE)

    # 2b. Seam-mode guard: in a gate-enabled (real) session, NO synthetic/test
    # seam may be supplied — real mode must use the gated _open_url for manifests
    # and the gated fetch for daily zips. This makes the injected seams
    # synthetic/test-only and not a real-run bypass.
    if REAL_FETCH_SOURCE_GATE_ENABLED and any(
        x is not None
        for x in (md5sums_bytes, filesizes_bytes, manifest_fetch_callable, fetch_callable)
    ):
        raise SyntheticOrchestratorViolation(
            "injected manifest/daily byte seams are synthetic/test-only and must "
            "not be supplied while REAL_FETCH_SOURCE_GATE_ENABLED is True; the "
            "real path fetches manifests and daily zips through the gated _open_url."
        )

    # 3. Bounded universe + window/2023+ rejection BEFORE any fetch/open.
    candidate_isos = [d.isoformat() for d in _date_range_inclusive(start_date, end_date)]
    universe = archive.enumerate_source_universe(candidate_isos)  # sorted, in-window
    fetched_dates = {date.fromisoformat(x) for x in universe}
    expected_filenames = expected_source_filenames(sorted(fetched_dates))

    # 4. Acquire official manifests (AFTER enumeration; BEFORE daily processing).
    # Default real path routes through the gated `_open_url` (no separate route);
    # with the gate False this hard-errors before any network import/open.
    manifest_source_mode = (
        "synthetic_injected"
        if (md5sums_bytes is not None or filesizes_bytes is not None
            or manifest_fetch_callable is not None)
        else "gated_open_url_default"
    )
    if md5sums_bytes is None:
        md5sums_bytes = fetch_manifest_bytes(
            GDELT1_MD5SUMS_URL, manifest_fetch_callable=manifest_fetch_callable
        )
    if filesizes_bytes is None:
        filesizes_bytes = fetch_manifest_bytes(
            GDELT1_FILESIZES_URL, manifest_fetch_callable=manifest_fetch_callable
        )

    # 4b. Manifest provenance + parse official-style manifests.
    prov = manifest_provenance(md5sums_bytes, filesizes_bytes)
    md5map = parse_md5sums(md5sums_bytes.decode("utf-8", "replace"))
    sizemap = parse_filesizes(filesizes_bytes.decode("utf-8", "replace"))

    # 5. Classify the bounded universe against BOTH manifests (gap-tolerant).
    #    present-in-both -> mandatory (fetch+verify); absent-in-both -> tolerated
    #    source gap (NO fetch); single-manifest-only -> manifest inconsistency,
    #    abort BEFORE any daily processing (NOT a tolerated gap).
    universe_dates = sorted(date.fromisoformat(x) for x in universe)
    presence = classify_manifest_presence(expected_filenames, md5map, sizemap)
    if presence["single_manifest_only"]:
        raise IntegrityManifestError(
            "manifest inconsistency: file(s) present in exactly one official "
            "manifest (md5sums XOR filesizes), not a tolerated gap: {}".format(
                sorted(presence["single_manifest_only"])
            )
        )
    present_dates = sorted(archive.parse_source_file_date(f) for f in presence["present_in_both"])
    gap_dates = sorted(archive.parse_source_file_date(f) for f in presence["absent_in_both"])
    available_dates_set = set(present_dates)
    gap_dates_set = set(gap_dates)

    reconcile_status = {
        "expected_count": presence["expected_count"],
        "present_in_both": len(present_dates),
        "absent_in_both": len(gap_dates),
        "single_manifest_only": 0,
        "tolerated_gap_count": len(gap_dates),
        "reconciled_ok": True,
        # back-compat keys (single-only aborts above, so present == present_in_both):
        "present_in_md5sums": len(present_dates),
        "present_in_filesizes": len(present_dates),
        "missing_from_md5sums": [],
        "missing_from_filesizes": [],
    }

    fetch = fetch_callable  # may be None -> fetch_stable uses the real gated fetch

    per_file_provenance: List[Dict[str, Any]] = []
    window_edge_incomplete_days: set = set()
    slice_edge_incomplete_sqldates: set = set()
    covered_sqldates_set: set = set()

    # Incremental aggregate counters replace whole-window row accumulation; no
    # whole-window row list is retained (bounded memory, see streaming buffer).
    agg_raw_rows = 0
    agg_date_eligibility_failure = 0
    agg_edge_window_exclusion = 0
    agg_classify_retained = 0

    # Bounded sliding file-block buffer + atomic streaming writer.
    edd = archive.ELIGIBILITY_DELTA_DAYS
    release_depth = streaming_release_depth()  # = 2 * EDD (derived, not hard-coded)
    held: List[Dict[str, Any]] = []            # FIFO of {"f_date": date, "rows": [...]}
    max_buffered_file_blocks = 0

    os.makedirs(out_dir, exist_ok=True)
    archive_final_path = os.path.join(out_dir, "ttg_approved_fields_archive.csv")
    archive_temp_path = archive_final_path + ".partial"
    manifest_final_path = os.path.join(out_dir, "ttg_archive_provenance_manifest.json")
    manifest_temp_path = manifest_final_path + ".partial"

    writer = _StreamingArchiveCsvWriter(archive_temp_path)

    def _release_block(block: Dict[str, Any]) -> None:
        # Apply final coverage filtering (production oracle over the precomputed
        # available set) and stream-write covered rows in classify order.
        for row in block["rows"]:
            sqld = date.fromisoformat(row["sqldate"])
            if archive.fetched_set_fully_covers(sqld, available_dates_set):
                writer.write_row(row)
                covered_sqldates_set.add(row["sqldate"])
            else:
                slice_edge_incomplete_sqldates.add(row["sqldate"])

    try:
        # 6. Per PRESENT-IN-BOTH source date only (tolerated gaps are NOT fetched):
        #    cache-or-stable-fetch -> integrity verify -> exact-58 file-level check
        #    -> retained-offset guard -> buffer whole file-block -> bounded release.
        #    Integrity / stable-retry / cache failures stay hard fail-closed; they
        #    are never reclassified as gaps.
        for f_date in present_dates:
            filename = expected_source_filename(f_date)
            url = build_source_file_url(f_date)
            cache_path = os.path.join(cache_dir, filename) if cache_dir else None
            source = None
            if cache_path is not None and os.path.exists(cache_path):
                # 6a. Cache hit: re-verify official MD5/size BEFORE use (fail closed).
                integ = verify_cached_zip(cache_path, filename, md5map, sizemap)
                with open(cache_path, "rb") as fh:
                    payload = fh.read()
                source = "cache"
            else:
                # 6b. Cache miss: stable fetch -> official verify -> cache write.
                payload = fetch_stable(
                    f_date, fetch_callable=fetch, attempts=fetch_attempts
                )
                integ = verify_file_integrity(filename, payload, md5map, sizemap)
                integ = dict(integ)
                integ["source"] = "fetch"
                if cache_path is not None and write_cache:
                    # Write to cache ONLY after integrity verification succeeded.
                    os.makedirs(cache_dir, exist_ok=True)
                    with open(cache_path, "wb") as fh:
                        fh.write(payload)
                    integ["cache_path"] = cache_path
                source = "fetch"

            # 6c. Exact-58 classification of VERIFIED bytes only.
            cls = archive.classify_payload_rows(
                payload,
                source_file_date=f_date,
                is_zip=is_zip,
                route_edge_incomplete=True,
                enforce_exact_columns=True,
            )
            # 6d. Exact-58 FILE-LEVEL hard fail: any column-count deviation in a
            #     manifest-listed processed file is terminal (NOT a silent drop,
            #     NOT a tolerated gap, NOT a per-SQLDATE label). Before any release.
            col_mismatch = cls.dropped_by_reason.get(
                archive.DROP_REASON_COLUMN_COUNT_MISMATCH, 0
            )
            if col_mismatch:
                raise ColumnLayoutHardFail(
                    "exact-58 file-level conformance violated for {}: {} row(s) not "
                    "exactly {} columns; terminal hard-fail (offending file named, "
                    "not classified as a gap)".format(
                        filename, col_mismatch, archive.EXPECTED_DAILY_COLUMN_COUNT
                    )
                )
            # 6e. Retained-offset guard: no retained row may be forward-dated
            #     beyond ELIGIBILITY_DELTA_DAYS (it would break the bounded-release
            #     support model). Terminal hard-fail; named; not streamed/dropped/gap.
            for row in cls.retained_rows:
                offset_days = (date.fromisoformat(row["sqldate"]) - f_date).days
                if offset_days > edd:
                    raise RetainedOffsetHardFail(
                        "retained-offset bound violated in {}: SQLDATE {} is offset "
                        "+{} days from source-file date {} (> ELIGIBILITY_DELTA_DAYS "
                        "= {}); terminal hard-fail (not streamed, not a gap)".format(
                            filename, row["sqldate"], offset_days,
                            f_date.isoformat(), edd
                        )
                    )

            # Incremental counters + O(days) per-file provenance metadata.
            agg_raw_rows += cls.raw_row_count
            agg_date_eligibility_failure += cls.dropped_by_reason.get(
                archive.DROP_REASON_DATE_ELIGIBILITY_FAILURE, 0)
            agg_edge_window_exclusion += cls.dropped_by_reason.get(
                archive.DROP_REASON_EDGE_WINDOW_EXCLUSION, 0)
            agg_classify_retained += cls.retained_row_count
            if cls.dropped_by_reason.get(archive.DROP_REASON_EDGE_WINDOW_EXCLUSION, 0):
                window_edge_incomplete_days.add(f_date.isoformat())

            entry = archive.build_per_file_provenance_entry(
                source_file_date=f_date,
                source_file_url=url,
                attempted=True,
                opened=True,
                classification=cls,
                byte_hash=integ.get("sha256_local_provenance"),
                byte_size=integ.get("byte_size"),
                error_status=None,
            )
            entry["integrity"] = {
                "source": source,
                "md5_ok": integ.get("md5_ok"),
                "size_ok": integ.get("size_ok"),
                "integrity_status": integ.get("integrity_status"),
                "official_md5": integ.get("official_md5"),
            }
            entry["exact58_file_level_ok"] = True
            per_file_provenance.append(entry)

            # Buffer this file's whole row-block (classify order), record the
            # high-water, then release any block whose support window is now final
            # (f_date >= b + release_depth). Bounded ~ release_depth+1 = 2*EDD+1.
            held.append({"f_date": f_date, "rows": cls.retained_rows})
            if len(held) > max_buffered_file_blocks:
                max_buffered_file_blocks = len(held)
            while held and (held[0]["f_date"] + timedelta(days=release_depth)) <= f_date:
                _release_block(held.pop(0))

        # 6f. Terminal post-loop flush: release the remaining held blocks in
        #     source-file order; their forward support (f+1 .. f+EDD) is now
        #     out-of-window/sealed/unavailable, resolving the final boundary edge.
        while held:
            _release_block(held.pop(0))

        writer.close()
        os.replace(archive_temp_path, archive_final_path)  # promote ONLY on success
    except BaseException:
        # Hard-fail / interrupt: leave the un-promoted partial temp (gitignored,
        # untracked); publish NO final archive and NO manifest.
        writer.close()
        raise

    artifact = {
        "output_path": archive_final_path,
        "row_count": writer.row_count,
        "sha256": writer.sha256,
        "byte_size": writer.byte_size,
    }

    # 7. Coverage ledger over the requested universe (covered / edge-excluded /
    #    gap-uncovered) — O(days), from the SAME support-aware production oracle.
    coverage_ledger: Dict[str, Any] = {}
    for d in universe_dates:
        coverage_ledger[d.isoformat()] = classify_sqldate_coverage(
            d, available_dates_set, gap_dates_set
        )
    ledger_covered = sorted(k for k, v in coverage_ledger.items()
                            if v["state"] == COVERAGE_COVERED)
    ledger_edge_excluded = sorted(k for k, v in coverage_ledger.items()
                                  if v["state"] == COVERAGE_EDGE_EXCLUDED)
    ledger_gap_uncovered = sorted(k for k, v in coverage_ledger.items()
                                  if v["state"] == COVERAGE_GAP_UNCOVERED)
    tolerated_gap_source_files = [expected_source_filename(d) for d in gap_dates]
    covered_sqldates = sorted(covered_sqldates_set)

    # 8. Structural manifest (atomic temp -> promote AFTER archive promotion).
    manifest = archive.build_phase2_provenance_manifest(
        source_file_window={
            "start": start_date,
            "end": end_date,
            "authorized_window_start": archive.WINDOW_START.isoformat(),
            "authorized_window_end": archive.WINDOW_END.isoformat(),
            "enumeration": "bounded YYYYMMDD per-day; no 2023+; no pre-window; no out-of-slice fetch",
        },
        per_file_provenance=per_file_provenance,
        archive_artifacts=[artifact],
        total_retained_row_count=writer.row_count,
        edge_incomplete_day_count=len(ledger_edge_excluded),
    )
    # Wired-path structural provenance (value-agnostic).
    manifest["wired_orchestrator"] = "run_bounded_integrity_build"
    manifest["manifest_provenance"] = prov
    manifest["manifest_source_mode"] = manifest_source_mode
    manifest["manifest_reconciliation"] = reconcile_status
    manifest["requested_source_file_count"] = len(universe_dates)
    manifest["fetched_source_file_count"] = len(present_dates)
    manifest["tolerated_source_gap_count"] = len(gap_dates)
    manifest["tolerated_source_gaps"] = tolerated_gap_source_files
    manifest["coverage_ledger"] = coverage_ledger
    manifest["coverage_summary"] = {
        "covered_count": len(ledger_covered),
        "edge_excluded_count": len(ledger_edge_excluded),
        "gap_uncovered_count": len(ledger_gap_uncovered),
        "covered_sqldates": ledger_covered,
        "edge_excluded_sqldates": ledger_edge_excluded,
        "gap_uncovered_sqldates": ledger_gap_uncovered,
    }
    manifest["window_edge_incomplete_day_count"] = len(window_edge_incomplete_days)
    manifest["slice_edge_incomplete_sqldate_count"] = len(slice_edge_incomplete_sqldates)
    manifest["primary_covered_sqldate_count"] = len(covered_sqldates)
    # Streaming-write structural provenance (value-agnostic).
    manifest["streaming_release_depth"] = release_depth
    manifest["max_buffered_source_file_blocks"] = max_buffered_file_blocks
    manifest["agg_raw_rows"] = agg_raw_rows
    manifest["agg_date_eligibility_failure"] = agg_date_eligibility_failure
    manifest["agg_edge_window_exclusion"] = agg_edge_window_exclusion
    manifest["agg_classify_retained"] = agg_classify_retained
    manifest["primary_archive_rows"] = writer.row_count
    manifest["boundary_declarations"]["single_real_network_entrypoint"] = True
    manifest["boundary_declarations"]["integrity_checked_before_archive_write"] = True
    manifest["boundary_declarations"]["slice_aware_coverage_applied"] = True
    manifest["boundary_declarations"]["manifest_acquired_via_gated_open_url_in_real_mode"] = True
    manifest["boundary_declarations"]["gap_tolerant_coverage_applied"] = True
    manifest["boundary_declarations"]["streaming_archive_write"] = True

    with open(manifest_temp_path, "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=False)
    os.replace(manifest_temp_path, manifest_final_path)
    manifest_path = manifest_final_path

    return {
        "manifest": manifest,
        "manifest_path": manifest_path,
        "archive_artifact": artifact,
        "universe": universe,
        "fetched_dates": [d.isoformat() for d in present_dates],
        "tolerated_source_gaps": tolerated_gap_source_files,
        "tolerated_gap_dates": [d.isoformat() for d in gap_dates],
        "primary_covered_sqldates": covered_sqldates,
        "coverage_ledger": coverage_ledger,
        "ledger_covered_sqldates": ledger_covered,
        "ledger_edge_excluded_sqldates": ledger_edge_excluded,
        "ledger_gap_uncovered_sqldates": ledger_gap_uncovered,
        "slice_edge_incomplete_sqldates": sorted(slice_edge_incomplete_sqldates),
        "window_edge_incomplete_days": sorted(window_edge_incomplete_days),
        "reconcile_status": reconcile_status,
        # Streaming-amendment additions (incremental counters; bounded buffer).
        "agg_raw_rows": agg_raw_rows,
        "agg_date_eligibility_failure": agg_date_eligibility_failure,
        "agg_edge_window_exclusion": agg_edge_window_exclusion,
        "agg_classify_retained": agg_classify_retained,
        "primary_archive_rows": writer.row_count,
        "archive_sha256": writer.sha256,
        "max_buffered_source_file_blocks": max_buffered_file_blocks,
        "streaming_release_depth": release_depth,
    }
