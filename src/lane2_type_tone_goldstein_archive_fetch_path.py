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
    # 0. Synthetic-harness guard: refuse real/default fetch (footgun closure).
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


def run_bounded_integrity_build(
    start_date: str,
    end_date: str,
    out_dir: str,
    *,
    md5sums_bytes: bytes,
    filesizes_bytes: bytes,
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
      4.  Compute manifest provenance (SHA-256 + size of the supplied manifest
          bytes) and parse official-style md5sums / filesizes.
      5.  Reconcile the bounded universe against BOTH manifests (fail closed).
      6.  Per source date:
          a. cache check first: if a cached zip exists, `verify_cached_zip`
             re-verifies official MD5/size before use (CacheIntegrityError on
             failure; no silent re-download);
          b. else `fetch_stable` (retry-stability) via the injected fetcher
             (default = real gated fetch), then `verify_file_integrity`
             (official MD5/size; SHA-256 recorded as local provenance), then
             write the verified bytes to cache (after verification only);
          c. `classify_payload_rows(..., enforce_exact_columns=True)`.
      7.  Slice-aware coverage: re-filter classify survivors with
          `fetched_set_fully_covers` against the ACTUAL fetched date set, so a
          slice-edge SQLDATE (e.g. 2013-04-30 needing an unfetched 2013-05-01)
          is routed OUT of the primary archive — never completed by fetching
          outside the bounded set.
      8.  Write the approved-fields archive (primary, slice-covered rows only)
          and a value-agnostic provenance manifest.

    `fetch_callable(source_file_date, source_file_url) -> bytes` is a test seam;
    its DEFAULT is the real gated fetch via `fetch_stable`. Integrity is applied
    unconditionally to the returned bytes, so an injected fetcher cannot bypass
    `verify_file_integrity` / exact-58 / slice coverage. Value-blind throughout.
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

    # 3. Bounded universe + window/2023+ rejection BEFORE any fetch/open.
    candidate_isos = [d.isoformat() for d in _date_range_inclusive(start_date, end_date)]
    universe = archive.enumerate_source_universe(candidate_isos)  # sorted, in-window
    fetched_dates = {date.fromisoformat(x) for x in universe}
    expected_filenames = expected_source_filenames(sorted(fetched_dates))

    # 4. Manifest provenance + parse official-style manifests.
    prov = manifest_provenance(md5sums_bytes, filesizes_bytes)
    md5map = parse_md5sums(md5sums_bytes.decode("utf-8", "replace"))
    sizemap = parse_filesizes(filesizes_bytes.decode("utf-8", "replace"))

    # 5. Reconcile bounded universe against BOTH manifests (fail closed).
    reconcile_status = reconcile_universe_against_manifests(
        expected_filenames, md5map, sizemap
    )

    fetch = fetch_callable  # may be None -> fetch_stable uses the real gated fetch

    classify_retained: List[Dict[str, str]] = []
    per_file_provenance: List[Dict[str, Any]] = []
    window_edge_incomplete_days: set = set()

    # 6. Per source date: cache-or-stable-fetch -> integrity verify -> classify.
    for f_date in sorted(fetched_dates):
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
            # 6b. Cache miss: stable fetch (retry) -> official verify -> cache write.
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
        classify_retained.extend(cls.retained_rows)
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
        per_file_provenance.append(entry)

    # 7. Slice-aware coverage against the ACTUAL fetched date set. A classify
    #    survivor whose SQLDATE is not slice-complete is routed OUT of the
    #    primary archive (slice-edge incomplete) — never completed by fetching
    #    outside the bounded set.
    primary_rows: List[Dict[str, str]] = []
    slice_edge_incomplete_sqldates: set = set()
    for row in classify_retained:
        sqld = date.fromisoformat(row["sqldate"])
        if archive.fetched_set_fully_covers(sqld, fetched_dates):
            primary_rows.append(row)
        else:
            slice_edge_incomplete_sqldates.add(row["sqldate"])

    # 8. Write archive (primary slice-covered rows) + structural manifest.
    os.makedirs(out_dir, exist_ok=True)
    archive_path = os.path.join(out_dir, "ttg_approved_fields_archive.csv")
    artifact = archive.write_approved_archive_csv(primary_rows, archive_path)

    covered_sqldates = sorted({r["sqldate"] for r in primary_rows})
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
        total_retained_row_count=len(primary_rows),
        edge_incomplete_day_count=len(window_edge_incomplete_days),
    )
    # Wired-path structural provenance (value-agnostic).
    manifest["wired_orchestrator"] = "run_bounded_integrity_build"
    manifest["manifest_provenance"] = prov
    manifest["manifest_reconciliation"] = reconcile_status
    manifest["fetched_source_file_count"] = len(fetched_dates)
    manifest["window_edge_incomplete_day_count"] = len(window_edge_incomplete_days)
    manifest["slice_edge_incomplete_sqldate_count"] = len(slice_edge_incomplete_sqldates)
    manifest["primary_covered_sqldate_count"] = len(covered_sqldates)
    manifest["boundary_declarations"]["single_real_network_entrypoint"] = True
    manifest["boundary_declarations"]["integrity_checked_before_archive_write"] = True
    manifest["boundary_declarations"]["slice_aware_coverage_applied"] = True

    manifest_path = os.path.join(out_dir, "ttg_archive_provenance_manifest.json")
    with open(manifest_path, "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=False)

    return {
        "manifest": manifest,
        "manifest_path": manifest_path,
        "archive_artifact": artifact,
        "universe": universe,
        "fetched_dates": sorted(x.isoformat() for x in fetched_dates),
        "primary_covered_sqldates": covered_sqldates,
        "slice_edge_incomplete_sqldates": sorted(slice_edge_incomplete_sqldates),
        "window_edge_incomplete_days": sorted(window_edge_incomplete_days),
        "reconcile_status": reconcile_status,
    }
