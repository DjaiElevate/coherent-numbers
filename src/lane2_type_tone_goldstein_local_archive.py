"""Lane 2 Type-Tone-Goldstein (TTG) local approved-fields archive — Phase 1.

Phase 1 = SYNTHETIC-ONLY scaffold. This module implements the pure
parsing / filtering / structural-manifest logic for a future local
approved-fields archive, plus a hard, by-construction network boundary.

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
from datetime import date
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

# Intentionally NOT imported (Phase-1 network boundary, by construction):
#   urllib, urllib.request, requests, socket, http.client.
# Adding any of these is a Phase-2 reviewed code change, not a Phase-1 edit.

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
