"""Lane 2 Type-Tone-Goldstein (TTG) local approved-fields archive — pure logic.

This module implements the pure parsing / filtering / structural-manifest logic
for the local approved-fields archive, plus a hard, by-construction network
boundary. It carries both the Phase-1 synthetic scaffold and the Phase-2
network-free build logic (source-file-date parsing, `file_date <= SQLDATE + 1`
availability eligibility, fully-covered-window classification, value-agnostic
provenance manifest, codebook-index verification — see the Phase-2 section at
the bottom of the file).

The Phase-2 REAL fetch path lives in a SEPARATE reviewed module
(`lane2_type_tone_goldstein_archive_fetch_path`), where real GDELT network
contact is disabled by a source-level gate. This module stays network-free.

It implements the design locked in
`docs/lane2_type_tone_goldstein_local_approved_fields_archive_design_memo_v0.1.md`
(content SHA-256 `c97e5593f5fa607f91ab8fb4a3a7e07c13efd6e385219f87431caedfd36abc99`,
DRAFT-LOCKED, NOT SETTLED).

Hard Phase-1 boundary (by construction, not by configuration):
  - This module imports NO network library: no `urllib`, no `requests`,
    no `socket`, no `http.client`. There is no opener, no URL fetch, no
    HTTP helper anywhere in this file.
  - The acquisition entrypoint is a bare hard-error stub that raises
    `Phase1NetworkNotAuthorized("NETWORK NOT AUTHORIZED IN PHASE 1")`.
  - Therefore Phase 2 (real GDELT fetch) requires a *reviewed code change*
    that adds a network path, NOT merely flipping a CLI flag / env var /
    module constant. Flipping all three guards still hard-errors at the
    acquisition step.

Scope firewalls (per memo):
  - Retains ONLY the five approved fields (§7); every forbidden field
    (§8) is dropped at parse time and never retained / written / logged /
    summarized / surfaced / exposed.
  - Value-blind (§12): the structural manifest carries structural
    metadata only (row counts, file counts, per-file status, schema
    names/types, SHA-256 hashes, source date universe, boundary
    declarations). It computes / emits NO value-level summary
    (no distribution, histogram, mean, median, min, max, correlation,
    z-score, per-date aggregate, sample row, or example).
  - 2023+ is sealed: any candidate date > 2022-12-31 hard-errors at
    enumeration, BEFORE any payload is opened or parsed.
  - No market data, no outcome, no join, no TTG feature/statistic.

This module authorizes no network contact, no archive execution, no TTG
extraction, and no join. Running a real build requires a separate,
explicit future authorization prompt AND the Phase-2 reviewed code change.
"""

from __future__ import annotations

import csv
import hashlib
import io
import os
import zipfile
from datetime import date, timedelta
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

# Intentionally NOT imported here (network boundary, by construction):
#   urllib, urllib.request, requests, socket, the std-lib HTTP client.
# This module remains network-free. The Phase-2 real fetch path is a SEPARATE
# reviewed module (lane2_type_tone_goldstein_archive_fetch_path); the only code
# added here is PURE, network-free build logic (source-file-date parsing,
# availability eligibility, window-coverage, value-agnostic provenance
# manifest, codebook-index verification). No URL literal, no network import,
# and no runtime switch may live in this module.

PHASE = "phase-1-synthetic-only"
IMPLEMENTATION_VERSION = "v0.1"

DESIGN_MEMO_PATH = (
    "docs/lane2_type_tone_goldstein_local_approved_fields_archive_design_memo_v0.1.md"
)
DESIGN_MEMO_SHA256 = (
    "c97e5593f5fa607f91ab8fb4a3a7e07c13efd6e385219f87431caedfd36abc99"
)

# ── Phase-1 default-false build guard ────────────────────────────────────────
#
# Ships False. This is the canonical run-enable constant. Even with this
# True AND the CLI flag passed AND the env var set, the Phase-1 acquisition
# entrypoint still hard-errors (network is impossible by construction).
TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED = False

# Env var recognized (but not honored for network) in Phase 1.
ENV_GUARD_NAME = "LANE2_TTG_LOCAL_ARCHIVE_BUILD_AUTHORIZED"

# Exact, frozen Phase-1 network refusal message. Tests assert string equality.
PHASE1_NETWORK_BLOCK_MESSAGE = "NETWORK NOT AUTHORIZED IN PHASE 1"

# ── Date / seal window (§15) ─────────────────────────────────────────────────

WINDOW_START = date(2013, 4, 1)
WINDOW_END = date(2022, 12, 31)
SEAL_START = date(2023, 1, 1)

# ── GDELT 1.0 positional schema (§9; V2 confirms before any real fetch) ──────
#
# GDELT 1.0 `.export.CSV` rows are TAB-separated, headerless, positional.
# These 0-based column indices reflect the documented GDELT 1.0 Event
# layout. They are used ONLY to read the approved fields out of synthetic
# fixtures in Phase 1. Phase 2's V2 schema verification must confirm the
# exact positions (and the exact date / information-date field locked by
# `294494a`) against a committed codebook reference before any real fetch.
DATE_FIELD_COLUMN_INDEX = 1        # SQLDATE (YYYYMMDD), keyed date field
QUADCLASS_COLUMN_INDEX = 29
GOLDSTEINSCALE_COLUMN_INDEX = 30
NUMMENTIONS_COLUMN_INDEX = 31
AVGTONE_COLUMN_INDEX = 34

# Highest index we must read; rows with fewer columns are malformed and are
# counted (structurally) but never contribute values.
_MAX_APPROVED_INDEX = max(
    DATE_FIELD_COLUMN_INDEX,
    QUADCLASS_COLUMN_INDEX,
    GOLDSTEINSCALE_COLUMN_INDEX,
    NUMMENTIONS_COLUMN_INDEX,
    AVGTONE_COLUMN_INDEX,
)

# Approved output schema (§7): column names + declared types. Order is
# canonical and is the archive CSV header order.
APPROVED_SCHEMA: Tuple[Tuple[str, str], ...] = (
    ("sqldate", "date_yyyymmdd"),
    ("quadclass", "int"),
    ("goldsteinscale", "float"),
    ("avgtone", "float"),
    ("nummentions", "int"),
)
APPROVED_FIELD_NAMES: Tuple[str, ...] = tuple(name for name, _ in APPROVED_SCHEMA)

# Forbidden field tokens (§8) — documented so tests can assert their absence.
# These are never read into the approved row and never written / surfaced.
FORBIDDEN_FIELD_NAMES: Tuple[str, ...] = (
    "EventCode",
    "EventBaseCode",
    "EventRootCode",
    "Actor1Code",
    "Actor1Name",
    "Actor2Code",
    "Actor2Name",
    "ActionGeo_FullName",
    "ActionGeo_Lat",
    "ActionGeo_Long",
    "SOURCEURL",
    "market",
    "outcome",
    "next_session_return",
)


# ── Exceptions ───────────────────────────────────────────────────────────────

class ArchiveBoundaryError(RuntimeError):
    """Base for hard archive-build boundary violations."""


class Phase1NetworkNotAuthorized(ArchiveBoundaryError):
    """Raised by the Phase-1 acquisition stub. Message is exactly
    `NETWORK NOT AUTHORIZED IN PHASE 1`."""


class Post2022SealBreach(ArchiveBoundaryError):
    """Raised when a candidate date / content row date is > 2022-12-31.

    At enumeration this fires BEFORE any payload is opened / parsed."""


class ArchiveBuildRefused(ArchiveBoundaryError):
    """Raised / signalled when the run-enable guards are not all satisfied."""


# ── Structural helpers (value-blind) ─────────────────────────────────────────

def sha256_hex(data: bytes) -> str:
    """SHA-256 of raw bytes. A content hash is a structural integrity
    address, not a value-level summary of the approved fields."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("sha256_hex requires bytes")
    return hashlib.sha256(bytes(data)).hexdigest()


def _parse_sqldate_token(tok: str) -> date:
    tok = tok.strip()
    if len(tok) != 8 or not tok.isdigit():
        raise ValueError("unparseable SQLDATE token")
    return date(int(tok[0:4]), int(tok[4:6]), int(tok[6:8]))


# ── Enumeration-time 2023+ guard (§15) ───────────────────────────────────────

def enumerate_source_universe(candidate_dates: Iterable[str]) -> List[str]:
    """Validate a candidate file/date universe BEFORE any content is opened.

    `candidate_dates` is an iterable of ISO date strings (YYYY-MM-DD)
    identifying source files. Returns the sorted, de-duplicated in-window
    universe. Hard-errors (`Post2022SealBreach`) on the FIRST date
    > 2022-12-31 — this happens at enumeration, before any payload is
    fetched, opened, or parsed. Also rejects pre-window dates.

    This function performs NO I/O and NO network access; it only inspects
    date strings.
    """
    seen: Dict[str, None] = {}
    for raw in candidate_dates:
        try:
            d = date.fromisoformat(str(raw).strip())
        except ValueError:
            raise Post2022SealBreach(
                "refusing un-parseable candidate date at enumeration: "
                "{!r}".format(raw)
            )
        if d >= SEAL_START:
            raise Post2022SealBreach(
                "2023+ candidate date {} rejected at enumeration BEFORE any "
                "content row is opened or parsed (seal: dates must be "
                "<= {})".format(d.isoformat(), WINDOW_END.isoformat())
            )
        if d < WINDOW_START:
            raise Post2022SealBreach(
                "pre-window candidate date {} rejected at enumeration "
                "(in-sample window starts {})".format(
                    d.isoformat(), WINDOW_START.isoformat()
                )
            )
        seen[d.isoformat()] = None
    return sorted(seen.keys())


# ── Pure parse / filter (approved fields only) ───────────────────────────────

class ParseResult:
    """Structural-only result of parsing one payload. Holds approved-field
    rows (the archive content) plus structural counts. Holds NO forbidden
    field and NO value-level summary."""

    __slots__ = ("rows", "parsed_row_count", "malformed_row_count")

    def __init__(
        self,
        rows: List[Dict[str, str]],
        parsed_row_count: int,
        malformed_row_count: int,
    ) -> None:
        self.rows = rows
        self.parsed_row_count = parsed_row_count
        self.malformed_row_count = malformed_row_count


def _tsv_text_from_payload(payload_bytes: bytes, is_zip: bool) -> str:
    """Return the TAB-separated text for a payload. If `is_zip`, unzip the
    single inner member. Operates only on the provided (synthetic) bytes."""
    if not isinstance(payload_bytes, (bytes, bytearray)):
        raise TypeError("payload must be bytes")
    if is_zip:
        with zipfile.ZipFile(io.BytesIO(bytes(payload_bytes))) as zf:
            names = zf.namelist()
            if len(names) != 1:
                raise ArchiveBoundaryError(
                    "expected exactly one member in payload zip, got "
                    "{}".format(len(names))
                )
            raw = zf.read(names[0])
    else:
        raw = bytes(payload_bytes)
    return raw.decode("utf-8", "replace")


def parse_approved_rows(
    payload_bytes: bytes,
    nominal_date: Optional[str] = None,
    is_zip: bool = False,
) -> ParseResult:
    """Parse a synthetic GDELT 1.0 payload, retaining ONLY the five
    approved fields per row.

    Forbidden columns may be present in the input row but are never read
    into the result, never written, never logged. Rows whose content
    SQLDATE is 2023+ hard-error (`Post2022SealBreach`) as defense-in-depth
    behind the enumeration guard. Malformed-short / unparseable rows are
    counted structurally but contribute no values.
    """
    text = _tsv_text_from_payload(payload_bytes, is_zip=is_zip)
    rows: List[Dict[str, str]] = []
    malformed = 0
    parsed = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) <= _MAX_APPROVED_INDEX:
            malformed += 1
            continue
        sqldate_tok = parts[DATE_FIELD_COLUMN_INDEX].strip()
        try:
            d = _parse_sqldate_token(sqldate_tok)
        except ValueError:
            malformed += 1
            continue
        if d >= SEAL_START:
            raise Post2022SealBreach(
                "2023+ content row SQLDATE {} encountered during parse "
                "(seal breach)".format(d.isoformat())
            )
        # Retain ONLY the approved fields. Forbidden columns in `parts`
        # are simply never referenced.
        rows.append(
            {
                "sqldate": d.isoformat(),
                "quadclass": parts[QUADCLASS_COLUMN_INDEX].strip(),
                "goldsteinscale": parts[GOLDSTEINSCALE_COLUMN_INDEX].strip(),
                "avgtone": parts[AVGTONE_COLUMN_INDEX].strip(),
                "nummentions": parts[NUMMENTIONS_COLUMN_INDEX].strip(),
            }
        )
        parsed += 1
    return ParseResult(rows=rows, parsed_row_count=parsed, malformed_row_count=malformed)


# ── Approved-fields archive writer ───────────────────────────────────────────

def write_approved_archive_csv(
    rows: Sequence[Mapping[str, str]],
    out_path: str,
) -> Dict[str, Any]:
    """Write the approved-fields archive CSV (header = APPROVED_FIELD_NAMES).

    The archive rows are the only place approved-field VALUES appear; this
    is the archive itself, not a summary. Returns structural metadata only:
    output path, row count, and the SHA-256 of the written bytes.
    """
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(list(APPROVED_FIELD_NAMES))
    n = 0
    for r in rows:
        writer.writerow([r[name] for name in APPROVED_FIELD_NAMES])
        n += 1
    data = buf.getvalue().encode("utf-8")
    out_dir = os.path.dirname(os.path.abspath(out_path)) or "."
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(data)
    return {
        "output_path": out_path,
        "row_count": n,
        "sha256": sha256_hex(data),
        "byte_size": len(data),
    }


# ── Structural manifest (value-blind, §11/§12) ───────────────────────────────

def build_structural_manifest(
    source_date_universe: Sequence[str],
    per_file_status: Sequence[Mapping[str, Any]],
    archive_artifacts: Sequence[Mapping[str, Any]],
    total_row_count: int,
    code_version: str = IMPLEMENTATION_VERSION,
    code_commit_placeholder: str = "UNCOMMITTED-PHASE-1",
) -> Dict[str, Any]:
    """Build a structural-only manifest.

    Includes: approved schema, source date universe, per-file status, row
    counts, SHA-256 hashes, output artifact paths, code version/commit
    placeholder, boundary declarations. Includes NO field values and NO
    value-derived summary (no min/max/mean/median/distribution/histogram/
    correlation/z-score/per-date aggregate/sample row).

    Each `per_file_status` entry must carry only structural keys; each
    `archive_artifacts` entry carries path/row_count/sha256/byte_size.
    """
    manifest: Dict[str, Any] = {
        "phase": PHASE,
        "implementation_version": code_version,
        "code_commit_placeholder": code_commit_placeholder,
        "design_memo_path": DESIGN_MEMO_PATH,
        "design_memo_sha256": DESIGN_MEMO_SHA256,
        "approved_schema": [
            {"name": name, "type": typ} for name, typ in APPROVED_SCHEMA
        ],
        "source_date_universe": list(source_date_universe),
        "source_file_count": len(per_file_status),
        "per_file_status": [_structural_file_entry(e) for e in per_file_status],
        "total_approved_row_count": int(total_row_count),
        "archive_artifacts": [
            {
                "path": a.get("path", a.get("output_path")),
                "row_count": int(a["row_count"]),
                "sha256": a["sha256"],
                "byte_size": int(a.get("byte_size", 0)),
            }
            for a in archive_artifacts
        ],
        "boundary_declarations": {
            "no_network_phase1": True,
            "no_gdelt_contact": True,
            "no_market_data": True,
            "no_outcome_data": True,
            "no_join": True,
            "no_2023plus": True,
            "no_forbidden_fields_retained": True,
            "no_ttg_feature_or_statistic": True,
            "value_blind_structural_metadata_only": True,
        },
    }
    return manifest


def _structural_file_entry(entry: Mapping[str, Any]) -> Dict[str, Any]:
    """Project a per-file status entry to structural keys only."""
    allowed = ("nominal_date", "status", "row_count", "sha256", "byte_size")
    out: Dict[str, Any] = {}
    for k in allowed:
        if k in entry:
            out[k] = entry[k]
    return out


# ── Phase-1 acquisition boundary (by construction) ───────────────────────────

def _phase1_fetch_disabled(*_args: Any, **_kwargs: Any) -> "bytes":
    """Phase-1 acquisition entrypoint.

    There is no network code in this module. This stub is the only
    acquisition path, and it hard-errors immediately, constructing no
    opener, no socket, and no request object. Phase 2 must replace this
    via a reviewed code change that adds a network path; flipping guards
    cannot reach the network because there is none to reach.
    """
    raise Phase1NetworkNotAuthorized(PHASE1_NETWORK_BLOCK_MESSAGE)


def guards_satisfied(
    cli_flag: bool,
    module_authorized: Optional[bool] = None,
    env: Optional[Mapping[str, str]] = None,
) -> bool:
    """Return True only if all three run-enable guards are satisfied:
    module constant True, CLI flag True, env var == '1'. This gates the
    *run*; it does NOT enable network (Phase-1 acquisition still hard-errors).
    """
    if module_authorized is None:
        module_authorized = TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED
    if env is None:
        env = os.environ
    return bool(module_authorized) and bool(cli_flag) and (
        env.get(ENV_GUARD_NAME) == "1"
    )


REFUSAL_MESSAGE = (
    "Lane 2 TTG local archive build is NOT authorized. Requires "
    "TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED=True AND "
    "--authorize-local-archive-build AND env "
    "LANE2_TTG_LOCAL_ARCHIVE_BUILD_AUTHORIZED=1. Even then, Phase-1 "
    "acquisition hard-errors: network is impossible by construction."
)


def run_local_archive_build(
    cli_flag: bool = False,
    candidate_dates: Optional[Sequence[str]] = None,
    fetch_callable: Optional[Callable[..., bytes]] = None,
    module_authorized: Optional[bool] = None,
    env: Optional[Mapping[str, str]] = None,
) -> Dict[str, Any]:
    """Phase-1 build orchestration.

    1. Three-guard gate. If not all satisfied, raise `ArchiveBuildRefused`
       BEFORE any acquisition / enumeration.
    2. Even with all guards satisfied, the acquisition step hard-errors:
       the default `fetch_callable` is the Phase-1 stub. There is no
       network code path to reach.

    `fetch_callable` exists ONLY so synthetic tests can inject a fake
    (non-network) callable to exercise ordering. Phase 1 ships no network
    callable; the default is the hard-error stub.
    """
    if not guards_satisfied(cli_flag, module_authorized=module_authorized, env=env):
        raise ArchiveBuildRefused(REFUSAL_MESSAGE)
    # Guards passed. Enumerate the (in-window) universe first — this still
    # hard-errors on any 2023+ date before acquisition. Then the acquisition
    # entrypoint is invoked; in Phase 1 it hard-errors by construction.
    universe = enumerate_source_universe(candidate_dates or [])
    acquire = fetch_callable if fetch_callable is not None else _phase1_fetch_disabled
    # Acquisition is gated by the stub: there is no reachable network code.
    acquire(universe)
    # Unreachable in Phase 1 (acquisition always raises). Present only to
    # document the post-acquisition structural-only shape.
    raise Phase1NetworkNotAuthorized(PHASE1_NETWORK_BLOCK_MESSAGE)


# ═════════════════════════════════════════════════════════════════════════════
# Phase-2 PURE build logic (network-free).
#
# The functions below implement the deterministic, value-blind build logic for
# the Phase-2 local approved-fields archive: source-file-date parsing,
# availability eligibility (`file_date <= SQLDATE + 1`), fully-covered
# predictor-window classification, row classification into retained / dropped-
# by-closed-reason, a value-agnostic per-file/whole-run provenance manifest, and
# a codebook/header index verifier.
#
# NONE of this touches the network. The real GDELT fetch lives in the separate
# reviewed module `lane2_type_tone_goldstein_archive_fetch_path`, whose real
# fetch is disabled by a source-level gate. These helpers operate only on bytes
# that some injected fetcher provides; they neither fetch nor enable fetching.
#
# Spend boundary: this build path may parse and COPY approved field values into
# the archive and emit structural/provenance status only. It computes NO
# function over the four substantive retained fields (quadclass, goldsteinscale,
# nummentions, avgtone): no buckets, sign buckets, tone/Goldstein buckets,
# thresholds, distributions, value summaries, or sample rows. Date operations
# over SQLDATE and the source-file date are structural and allowed.
# ═════════════════════════════════════════════════════════════════════════════

# Source-file naming (filename token only — NOT a URL; no scheme literal lives
# in this network-free module). The download URL is built in the separate fetch
# module from this filename; the file-download URL namespace is kept strictly
# separate from the row-level GDELT `SOURCEURL` field (forbidden, never
# retained — see FORBIDDEN_SOURCEURL_COLUMN_INDEX below).
SOURCE_FILE_NAME_TEMPLATE = "{yyyymmdd}.export.CSV.zip"

# Availability eligibility: a retained predictor row for information-date
# `SQLDATE = t` is eligible iff its source-file/update date `F` satisfies
# `F <= t + ELIGIBILITY_DELTA_DAYS`. ELIGIBILITY_DELTA_DAYS is the single,
# canonical `+1`. There is no second bucket shift / `civil_date + 1` transform
# applied anywhere in this build path (double-shift guard, amendment §6/§7).
ELIGIBILITY_DELTA_DAYS = 1

# Forbidden positional indices, recorded ONLY so the build can prove it never
# retains them. These are independently re-derived from the committed GDELT 1.0
# Event codebook reference (docs/lane2_gdelt1_event_codebook_reference_v0.1.md,
# content SHA-256 3c5fa5bc054fbefaea2a26f9700ee827f2ff86a059d1625ffa127b10bf035a58):
#   DATEADDED  = 1-based ordinal 57 -> python idx 56 (management metadata)
#   SOURCEURL  = 1-based ordinal 58 -> python idx 57 (article/source URL)
# DATEADDED is NOT used as an availability instrument (amendment §9); neither is
# retained as a row field (amendment §10). They are NOT in APPROVED_SCHEMA.
FORBIDDEN_DATEADDED_COLUMN_INDEX = 56
FORBIDDEN_SOURCEURL_COLUMN_INDEX = 57

# Codebook-derived approved index map (re-derived from the committed reference,
# not hard-coded from any dispatch prompt). Used by assert_codebook_indices to
# fail closed on a module/codebook mismatch before any fetch.
CODEBOOK_REFERENCE_PATH = "docs/lane2_gdelt1_event_codebook_reference_v0.1.md"
CODEBOOK_REFERENCE_SHA256 = (
    "3c5fa5bc054fbefaea2a26f9700ee827f2ff86a059d1625ffa127b10bf035a58"
)

# ── Closed structural drop-reason set (§10) ──────────────────────────────────
DROP_REASON_MALFORMED_ROW = "malformed_row"
DROP_REASON_SHORT_ROW = "short_row"
DROP_REASON_FIELD_PARSE_FAILURE = "field_parse_failure"
DROP_REASON_DATE_ELIGIBILITY_FAILURE = "date_eligibility_failure"
DROP_REASON_SOURCE_FILE_OUTSIDE_UNIVERSE = "source_file_outside_authorized_universe"
DROP_REASON_EDGE_WINDOW_EXCLUSION = "edge_window_exclusion"
DROP_REASON_FORBIDDEN_FIELD_RETENTION_VIOLATION = "forbidden_field_retention_violation"
DROP_REASON_DUPLICATE_PROVENANCE_INTEGRITY_FAILURE = (
    "duplicate_provenance_integrity_failure"
)

CLOSED_DROP_REASONS: Tuple[str, ...] = (
    DROP_REASON_MALFORMED_ROW,
    DROP_REASON_SHORT_ROW,
    DROP_REASON_FIELD_PARSE_FAILURE,
    DROP_REASON_DATE_ELIGIBILITY_FAILURE,
    DROP_REASON_SOURCE_FILE_OUTSIDE_UNIVERSE,
    DROP_REASON_EDGE_WINDOW_EXCLUSION,
    DROP_REASON_FORBIDDEN_FIELD_RETENTION_VIOLATION,
    DROP_REASON_DUPLICATE_PROVENANCE_INTEGRITY_FAILURE,
)


class CodebookIndexMismatch(ArchiveBoundaryError):
    """Raised when the module's approved indices do not match the committed
    codebook-derived indices. Fails closed before any fetch."""


def assert_codebook_indices(codebook_derived: Mapping[str, int]) -> None:
    """Fail closed unless the module's approved positional indices exactly match
    the indices independently derived from the committed codebook reference.

    `codebook_derived` maps approved field name -> python 0-based index, derived
    from the codebook reference (NOT from this module). Any mismatch (including a
    missing or extra approved field) raises `CodebookIndexMismatch`.
    """
    module_map = {
        "sqldate": DATE_FIELD_COLUMN_INDEX,
        "quadclass": QUADCLASS_COLUMN_INDEX,
        "goldsteinscale": GOLDSTEINSCALE_COLUMN_INDEX,
        "nummentions": NUMMENTIONS_COLUMN_INDEX,
        "avgtone": AVGTONE_COLUMN_INDEX,
    }
    if dict(codebook_derived) != module_map:
        raise CodebookIndexMismatch(
            "codebook/module index mismatch: module={} codebook_derived={}".format(
                module_map, dict(codebook_derived)
            )
        )
    # Forbidden indices must never collide with any approved index.
    approved_indices = set(module_map.values())
    for forbidden in (
        FORBIDDEN_DATEADDED_COLUMN_INDEX,
        FORBIDDEN_SOURCEURL_COLUMN_INDEX,
    ):
        if forbidden in approved_indices:
            raise CodebookIndexMismatch(
                "forbidden index {} collides with an approved index".format(forbidden)
            )


# ── Source-file date (structural; from filename/URL token) ───────────────────

def parse_source_file_date(name_or_url: str) -> date:
    """Parse the source-file/update date `F` from a GDELT daily filename or
    download URL (e.g. `...events/20140102.export.CSV.zip` -> 2014-01-02).

    `F` is the GDELT update-file civil date. It is derived ONLY from the
    filename's leading 8-digit `YYYYMMDD` token — never from DATEADDED, never
    from download time, never shifted by local timezone or by an extra
    `civil_date + 1` transform. Raises ValueError if no token is found.
    """
    base = str(name_or_url).strip().rsplit("/", 1)[-1]
    tok = base[:8]
    if len(tok) != 8 or not tok.isdigit():
        raise ValueError("unparseable source-file date token in {!r}".format(name_or_url))
    return date(int(tok[0:4]), int(tok[4:6]), int(tok[6:8]))


# ── Availability eligibility (§6) and window coverage (§7) ───────────────────

def row_is_eligible(source_file_date: date, sqldate: date) -> bool:
    """Amendment §6 eligibility: include a contribution iff
    `source_file_date <= SQLDATE + 1` (the single canonical `+1`).

    Equivalently offset = SQLDATE - source_file_date >= -1, i.e. only the
    `{0, -1, +1}` offset buckets. Late-arriving lookback buckets
    (`-7/-30/-365/-3650`) are ineligible.
    """
    return source_file_date <= sqldate + timedelta(days=ELIGIBILITY_DELTA_DAYS)


def is_sqldate_fully_covered(sqldate: date) -> bool:
    """Amendment §7 fully-covered predictor-window rule.

    SQLDATE day `t` belongs to the PRIMARY no-lookahead archive only if every
    potentially eligible source-file date under §6 — `{t-1, t, t+1}` — lies
    inside the authorized source-file window [WINDOW_START, WINDOW_END]. So `t`
    is fully covered iff `t-1 >= WINDOW_START` and `t+1 <= WINDOW_END`.

    Consequence: the end day (t+1 -> sealed 2023-01-01) and the start day
    (t-1 -> pre-window 2013-03-31) are edge-incomplete and must be routed out of
    the primary archive — never completed by reading a sealed or pre-window file.
    """
    lo_needed = sqldate - timedelta(days=1)
    hi_needed = sqldate + timedelta(days=ELIGIBILITY_DELTA_DAYS)
    return lo_needed >= WINDOW_START and hi_needed <= WINDOW_END


# ── Per-file row classification (structural counts + retained rows) ──────────

class FileClassification:
    """Structural-only result of classifying one source file's rows.

    Holds the retained approved-field rows (the archive content) plus a
    value-agnostic count breakdown. Holds NO forbidden field, NO value summary,
    NO sample of dropped rows.
    """

    __slots__ = (
        "retained_rows",
        "raw_row_count",
        "retained_row_count",
        "dropped_by_reason",
        "edge_routed_rows",
    )

    def __init__(
        self,
        retained_rows: List[Dict[str, str]],
        raw_row_count: int,
        dropped_by_reason: Dict[str, int],
        edge_routed_rows: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        self.retained_rows = retained_rows
        self.raw_row_count = raw_row_count
        self.retained_row_count = len(retained_rows)
        self.dropped_by_reason = dropped_by_reason
        self.edge_routed_rows = edge_routed_rows if edge_routed_rows is not None else []


def classify_payload_rows(
    payload_bytes: bytes,
    source_file_date: date,
    is_zip: bool = False,
    route_edge_incomplete: bool = False,
) -> FileClassification:
    """Classify one synthetic payload's rows for the Phase-2 build.

    For every non-empty line:
      - short row (< required columns)      -> drop (short_row)
      - unparseable SQLDATE token           -> drop (field_parse_failure)
      - content SQLDATE 2023+               -> Post2022SealBreach (defense-in-depth)
      - source_file_date > SQLDATE + 1      -> drop (date_eligibility_failure)
      - SQLDATE day not fully covered       -> edge_window_exclusion
            (routed to `edge_routed_rows` iff `route_edge_incomplete`, else dropped)
      - otherwise retain ONLY the five approved fields.

    Forbidden columns are never read into a retained row. A defensive check
    confirms each retained row carries exactly the approved field names; a
    violation raises (forbidden_field_retention_violation) — fail closed.

    The source-file date must be inside the authorized window; otherwise the
    whole file is rejected (source_file_outside_authorized_universe).
    """
    if not (WINDOW_START <= source_file_date <= WINDOW_END):
        raise Post2022SealBreach(
            "source file date {} outside authorized window [{}, {}]".format(
                source_file_date.isoformat(),
                WINDOW_START.isoformat(),
                WINDOW_END.isoformat(),
            )
        )
    text = _tsv_text_from_payload(payload_bytes, is_zip=is_zip)
    retained: List[Dict[str, str]] = []
    edge_routed: List[Dict[str, str]] = []
    drops: Dict[str, int] = {r: 0 for r in CLOSED_DROP_REASONS}
    raw = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        raw += 1
        parts = line.split("\t")
        if len(parts) <= _MAX_APPROVED_INDEX:
            drops[DROP_REASON_SHORT_ROW] += 1
            continue
        try:
            d = _parse_sqldate_token(parts[DATE_FIELD_COLUMN_INDEX].strip())
        except ValueError:
            drops[DROP_REASON_FIELD_PARSE_FAILURE] += 1
            continue
        if d >= SEAL_START:
            raise Post2022SealBreach(
                "2023+ content row SQLDATE {} encountered during classify "
                "(seal breach)".format(d.isoformat())
            )
        if not row_is_eligible(source_file_date, d):
            drops[DROP_REASON_DATE_ELIGIBILITY_FAILURE] += 1
            continue
        row = {
            "sqldate": d.isoformat(),
            "quadclass": parts[QUADCLASS_COLUMN_INDEX].strip(),
            "goldsteinscale": parts[GOLDSTEINSCALE_COLUMN_INDEX].strip(),
            "avgtone": parts[AVGTONE_COLUMN_INDEX].strip(),
            "nummentions": parts[NUMMENTIONS_COLUMN_INDEX].strip(),
        }
        # Defensive: retained rows must carry exactly the approved field names.
        if set(row.keys()) != set(APPROVED_FIELD_NAMES):
            drops[DROP_REASON_FORBIDDEN_FIELD_RETENTION_VIOLATION] += 1
            raise ArchiveBoundaryError(
                "retained row carries non-approved keys: {}".format(sorted(row.keys()))
            )
        if not is_sqldate_fully_covered(d):
            drops[DROP_REASON_EDGE_WINDOW_EXCLUSION] += 1
            if route_edge_incomplete:
                edge_routed.append(row)
            continue
        retained.append(row)
    return FileClassification(
        retained_rows=retained,
        raw_row_count=raw,
        dropped_by_reason=drops,
        edge_routed_rows=edge_routed,
    )


# ── Value-agnostic provenance manifest (§10/§11) ─────────────────────────────

def build_per_file_provenance_entry(
    source_file_date: date,
    source_file_url: str,
    attempted: bool,
    opened: bool,
    classification: Optional[FileClassification] = None,
    byte_hash: Optional[str] = None,
    byte_size: Optional[int] = None,
    error_status: Optional[str] = None,
) -> Dict[str, Any]:
    """Build one value-agnostic per-file provenance entry.

    `source_file_url` is the file-DOWNLOAD URL (provenance metadata, allowed). It
    is a different namespace from the row-level GDELT `SOURCEURL` field, which is
    forbidden and never retained. Counts here are structural volume only — never
    partitioned by any substantive field value.
    """
    entry: Dict[str, Any] = {
        "source_file_date": source_file_date.isoformat(),
        "source_file_url": source_file_url,
        "attempted": bool(attempted),
        "opened": bool(opened),
        "coverage_status": (
            "fully_covered"
            if is_sqldate_fully_covered(source_file_date)
            else "edge_or_provenance_only"
        ),
        "error_status": error_status,
    }
    if byte_hash is not None:
        entry["byte_sha256"] = byte_hash
    if byte_size is not None:
        entry["byte_size"] = int(byte_size)
    if classification is not None:
        entry["raw_row_count"] = int(classification.raw_row_count)
        entry["retained_row_count"] = int(classification.retained_row_count)
        # Dropped counts keyed ONLY by closed structural reasons — never by any
        # substantive field value.
        entry["dropped_by_reason"] = {
            reason: int(classification.dropped_by_reason.get(reason, 0))
            for reason in CLOSED_DROP_REASONS
        }
    return entry


def build_phase2_provenance_manifest(
    source_file_window: Mapping[str, str],
    per_file_provenance: Sequence[Mapping[str, Any]],
    archive_artifacts: Sequence[Mapping[str, Any]],
    total_retained_row_count: int,
    edge_incomplete_day_count: int = 0,
    code_version: str = IMPLEMENTATION_VERSION,
    code_commit_placeholder: str = "UNCOMMITTED-PHASE-2",
) -> Dict[str, Any]:
    """Build a value-agnostic Phase-2 provenance manifest.

    Structural / provenance only: the source-file window pin, per-file
    provenance (date, download URL, attempted/opened, byte hash/size, raw &
    retained counts, dropped-by-closed-reason, coverage status, error status),
    archive artifact hashes, the approved schema (names/types), and boundary
    declarations. NO field values, NO value-derived summary, NO sample row, NO
    per-value bucket.
    """
    return {
        "phase": "phase-2-fetch-path",
        "implementation_version": code_version,
        "code_commit_placeholder": code_commit_placeholder,
        "design_memo_path": DESIGN_MEMO_PATH,
        "design_memo_sha256": DESIGN_MEMO_SHA256,
        "codebook_reference_path": CODEBOOK_REFERENCE_PATH,
        "codebook_reference_sha256": CODEBOOK_REFERENCE_SHA256,
        "approved_schema": [
            {"name": name, "type": typ} for name, typ in APPROVED_SCHEMA
        ],
        "source_file_window": dict(source_file_window),
        "eligibility_rule": "source_file_date <= sqldate + {}".format(
            ELIGIBILITY_DELTA_DAYS
        ),
        "source_file_count": len(per_file_provenance),
        "per_file_provenance": [dict(e) for e in per_file_provenance],
        "total_approved_retained_row_count": int(total_retained_row_count),
        "edge_incomplete_day_count": int(edge_incomplete_day_count),
        "archive_artifacts": [
            {
                "path": a.get("path", a.get("output_path")),
                "row_count": int(a["row_count"]),
                "sha256": a["sha256"],
                "byte_size": int(a.get("byte_size", 0)),
            }
            for a in archive_artifacts
        ],
        "boundary_declarations": {
            "no_real_network_contact_this_run": True,
            "no_gdelt_event_data_fetched": True,
            "no_dateadded_as_availability_instrument": True,
            "no_dateadded_retained": True,
            "no_row_level_sourceurl_retained": True,
            "no_market_data": True,
            "no_outcome_data": True,
            "no_join": True,
            "no_2023plus": True,
            "no_forbidden_fields_retained": True,
            "no_ttg_feature_or_statistic": True,
            "value_blind_structural_metadata_only": True,
        },
    }
