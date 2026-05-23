"""Standalone Lane 2 GDELT 1.0 row-date characterization runner
(16-date deterministic sweep).

THIS RUNNER DOES NOT RUN BY DEFAULT AND PERFORMS NO DATA ACCESS UNLESS
THREE INDEPENDENT GUARDS ARE ALL SATISFIED:

  1. module constant ROW_DATE_CHARACTERIZATION_AUTHORIZED is True (ships False);
  2. CLI flag --authorize-row-date-characterization-run is passed;
  3. env var LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED == "1".

If any guard is missing, the runner prints a refusal and exits BEFORE any
network call, opener construction, directory creation, or artifact write.

This script is **standalone**. It does NOT import the event-file probe
runner, the count-feasibility runner, the count-feasibility source
module, or Gate 4D's index-listing opener. It builds its own
redirect-disabled opener (mirroring the Gate 4D / event-file-probe
pattern with script-local names) scoped only to the 16 hardcoded
characterization URLs.

Authorization basis: characterization-plan lock memo
`docs/lane2_gdelt1_row_date_mismatch_characterization_plan_v0.1.md`
(commit `a2a8fd5`). The memo authorizes neither source addition nor
execution; this implementation step (the present file + the paired tests
file) is the authorized source-addition step. The script ships inert;
execution requires its own separate authorization step that flips the
guard.

Scope: substrate-side row-date offset taxonomy characterization over the
16 deterministic dates locked by `a2a8fd5` §5/§6. No market data, no
Step 2, no asset/return logic, no category/theme/actor/geography/tone
filtering, no spike/burst thresholds. No negative control (the gap
model is settled by the first probe at `9319d30`).
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
import zipfile
from datetime import date, datetime, timezone
from typing import Callable, Dict, List, Optional, Tuple


# ── Module-level authorization guard ─────────────────────────────────────────
#
# Ships False. Flipping this is a separate, explicit run-enablement commit
# under the future characterization-execution-authorization prompt.
# Mirrors the count-feasibility runner's `COUNT_FEASIBILITY_AUTHORIZED`
# and the event-file probe's `EVENT_FILE_PROBE_AUTHORIZED` patterns.
ROW_DATE_CHARACTERIZATION_AUTHORIZED = False


# ── Substrate-pinned constants (no CLI / env / config override) ──────────────

RECOGNIZED_LIST_PATH = (
    "results/lane2_gdelt1_turn_b_recognized_list_capture/"
    "20260521T124853Z/recognized_list.json"
)

EVENT_FILE_BASE_URL = "http://data.gdeltproject.org/events/"

SEAL_START = date(2023, 1, 1)
DEFAULT_TIMEOUT = 30.0
SQLDATE_COLUMN_INDEX = 1

EXPECTED_OFFSETS: Tuple[int, ...] = (-3650, -365, -30, -7, -1, 0, 1)

# Excluded dates (memo §4): known substrate gaps + already-sampled first-probe
# positive dates. The characterization sample must not include any of these.
KNOWN_SUBSTRATE_GAPS: Tuple[str, ...] = (
    "2014-01-23",
    "2014-01-24",
    "2014-01-25",
    "2014-03-19",
)
ALREADY_SAMPLED_PROBE_POSITIVES: Tuple[str, ...] = (
    "2013-04-01",
    "2014-01-22",
    "2014-01-26",
    "2018-02-14",
    "2022-12-31",
)


# ── Locked 16 characterization dates (from `a2a8fd5` §5) ─────────────────────
#
# Pre-registered deterministic sample. No CLI / env / config override.
CHARACTERIZATION_DATES: Tuple[date, ...] = (
    date(2013, 9, 7),
    date(2014, 2, 16),
    date(2014, 7, 26),
    date(2014, 12, 31),
    date(2015, 10, 2),
    date(2016, 7, 2),
    date(2017, 4, 2),
    date(2017, 12, 31),
    date(2018, 10, 2),
    date(2019, 7, 3),
    date(2020, 4, 2),
    date(2020, 12, 31),
    date(2021, 7, 2),
    date(2022, 1, 1),
    date(2022, 7, 2),
    date(2022, 12, 30),
)


# ── Locked 16 URLs (from `a2a8fd5` §6) ───────────────────────────────────────

CHARACTERIZATION_URLS: Tuple[str, ...] = tuple(
    "{}{:04d}{:02d}{:02d}.export.CSV.zip".format(
        EVENT_FILE_BASE_URL, d.year, d.month, d.day,
    )
    for d in CHARACTERIZATION_DATES
)


# ── Output allow-list (memo §8) ──────────────────────────────────────────────
#
# Payload-preservation policy: preserve compressed raw payloads for ALL
# HTTP 200 responses among the 16 characterization dates. No exclusion
# (unlike the first probe at `9319d30`, which excluded the negative-control
# payload). The characterization sample contains only positive dates;
# preserving all successful payloads mirrors the probe's audit pattern and
# allows future read-only deep dives without re-fetch authorization.
ALLOWED_CHARACTERIZATION_OUTPUTS: Tuple[str, ...] = (
    "characterization_metadata.json",
    "characterization_summary.md",
)
_PAYLOAD_BASENAME_RE = re.compile(r"^payload_(\d{8})\.zip$")


_REFUSAL = (
    "Lane 2 row-date characterization run is NOT authorized. Requires "
    "ROW_DATE_CHARACTERIZATION_AUTHORIZED=True AND "
    "--authorize-row-date-characterization-run AND env "
    "LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED=1. No network, no fetch, "
    "no directory created."
)


# ── Exception classes ────────────────────────────────────────────────────────

class RedirectBlocked(RuntimeError):
    """Raised by the characterization redirect-disabled opener on any
    3xx response."""


class CharacterizationBoundaryBreach(RuntimeError):
    """Raised when a hard boundary (2023+ date, disallowed output,
    substrate-pin violation, etc.) is hit."""


class SampleValidationError(RuntimeError):
    """Raised when pre-run substrate validation against the §10
    recognized list fails (a locked date is absent / collides with a
    known gap / collides with an already-sampled probe date / is 2023+)."""


# ── Local redirect-disabled opener (characterization-scoped) ─────────────────
#
# Mirrors the Gate 4D / event-file-probe pattern with script-local names.
# Does NOT reuse Gate 4D's index-listing opener (scoped to
# `DEFAULT_GDELT1_INDEX_URL` only) or the event-file probe's opener
# (scoped to the 5+1 probe URLs). This opener is used only for the 16
# hardcoded characterization URLs constructed from
# `CHARACTERIZATION_DATES`.

class _RowDateNoFollowRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Redirect handler whose 3xx hooks raise rather than follow.

    Overriding every 30x http_error_NNN hook makes the no-follow property
    structural — every redirect status is intercepted — not a runtime
    convention a caller could forget."""

    def _block(self, req, fp, code, msg, headers):
        raise RedirectBlocked(
            "characterization opener blocked redirect (status {!r}); "
            "no follow, no fallback".format(code)
        )

    http_error_301 = _block
    http_error_302 = _block
    http_error_303 = _block
    http_error_307 = _block
    http_error_308 = _block


def _build_row_date_redirect_disabled_opener(
    timeout: float = DEFAULT_TIMEOUT,
) -> Callable:
    """Build a callable opener with redirect-following disabled by
    construction. Used only for the 16 authorized characterization URLs.

    The factory call fires no request; a single request occurs only when
    the returned callable is invoked. Guards are not flipped.
    """
    _opener = urllib.request.build_opener(_RowDateNoFollowRedirectHandler())
    _default_timeout = timeout

    def _row_date_opener(url, timeout=_default_timeout):
        # Exactly one request per invocation. No retry, no second GET, no
        # fallback. The caller (`_characterize_one_file`) consumes
        # `.read()` once and never re-invokes this opener for the same
        # URL.
        return _opener.open(url, timeout=timeout)

    return _row_date_opener


# ── Three-guard gate ─────────────────────────────────────────────────────────

def _guards_ok(cli_flag: bool) -> bool:
    return (
        ROW_DATE_CHARACTERIZATION_AUTHORIZED
        and cli_flag
        and os.environ.get(
            "LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED",
        ) == "1"
    )


# ── Recognized-list loading ──────────────────────────────────────────────────

def _load_recognized_units(repo_root: str) -> List[str]:
    """Load `recognized_in_window_units` from the §10 capture at the
    hardcoded substrate-pinned path. No override is permitted."""
    path = os.path.join(repo_root, RECOGNIZED_LIST_PATH)
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    units = data.get("recognized_in_window_units")
    if not isinstance(units, list):
        raise CharacterizationBoundaryBreach(
            "recognized_list.json missing 'recognized_in_window_units' "
            "list at {}".format(path)
        )
    return units


# ── Pre-run substrate validation (memo §3) ───────────────────────────────────

def validate_characterization_sample(
    recognized_units: List[str],
) -> None:
    """Verify before any network that:

    - all 16 hardcoded characterization dates are present in
      `recognized_in_window_units`;
    - none collide with `KNOWN_SUBSTRATE_GAPS`;
    - none collide with `ALREADY_SAMPLED_PROBE_POSITIVES`;
    - no characterization date is on/after `SEAL_START`.

    Raises `SampleValidationError` on any failure (caller halts before
    any network).
    """
    recognized = set(recognized_units)
    iso_dates = [d.isoformat() for d in CHARACTERIZATION_DATES]

    missing = [d for d in iso_dates if d not in recognized]
    if missing:
        raise SampleValidationError(
            "characterization date(s) absent from recognized universe: "
            "{}".format(missing)
        )

    gap_collision = [
        d for d in iso_dates if d in set(KNOWN_SUBSTRATE_GAPS)
    ]
    if gap_collision:
        raise SampleValidationError(
            "characterization date(s) collide with known substrate "
            "gaps: {}".format(gap_collision)
        )

    probe_collision = [
        d for d in iso_dates if d in set(ALREADY_SAMPLED_PROBE_POSITIVES)
    ]
    if probe_collision:
        raise SampleValidationError(
            "characterization date(s) collide with already-sampled "
            "first-probe positive dates: {}".format(probe_collision)
        )

    seal_violations = [
        d for d in CHARACTERIZATION_DATES if d >= SEAL_START
    ]
    if seal_violations:
        raise SampleValidationError(
            "characterization date(s) on/after SEAL_START 2023-01-01: "
            "{}".format([d.isoformat() for d in seal_violations])
        )


# ── URL construction ─────────────────────────────────────────────────────────

def construct_characterization_urls() -> List[str]:
    """Return the 16 locked URLs in canonical order (sorted by date).

    No CLI/env/config override. No external date list. The URLs are
    derived deterministically from `CHARACTERIZATION_DATES`.
    """
    urls = []
    for d in CHARACTERIZATION_DATES:
        if d >= SEAL_START:
            raise CharacterizationBoundaryBreach(
                "refusing to construct URL for 2023+ date: {}".format(
                    d.isoformat()
                )
            )
        yyyymmdd = "{:04d}{:02d}{:02d}".format(d.year, d.month, d.day)
        urls.append("{}{}.export.CSV.zip".format(
            EVENT_FILE_BASE_URL, yyyymmdd,
        ))
    return urls


# ── Output allow-list (memo §8) ──────────────────────────────────────────────

def _is_allowed_characterization_output(
    basename: str, locked_yyyymmdd: List[str],
) -> bool:
    """Return True iff `basename` matches the characterization output
    allow-list.

    Exact-match: `characterization_metadata.json`,
    `characterization_summary.md`.
    Pattern-match: `payload_<YYYYMMDD>.zip` where `<YYYYMMDD>` is one of
    the 16 locked characterization dates. Path traversal characters
    (anything containing `/`, `\\`, `..`) are rejected at the basename
    layer; this is a defense-in-depth check (the basename should never
    contain a separator in normal use, but the allow-list explicitly
    refuses).
    """
    if "/" in basename or "\\" in basename or ".." in basename:
        return False
    if basename in ALLOWED_CHARACTERIZATION_OUTPUTS:
        return True
    m = _PAYLOAD_BASENAME_RE.match(basename)
    if m is None:
        return False
    return m.group(1) in set(locked_yyyymmdd)


def _checked_characterization_path(
    output_dir: str, basename: str, locked_yyyymmdd: List[str],
) -> str:
    """Pre-write gate: assert basename is allow-listed BEFORE any write."""
    if not _is_allowed_characterization_output(basename, locked_yyyymmdd):
        raise CharacterizationBoundaryBreach(
            "non-allow-listed characterization output: {!r}".format(
                basename
            )
        )
    return os.path.join(output_dir, basename)


def _assert_characterization_outputs_allowed(
    output_dir: str, locked_yyyymmdd: List[str],
) -> None:
    """Post-hoc tripwire: only allow-listed files may exist in the
    output dir."""
    for name in os.listdir(output_dir):
        if os.path.isdir(os.path.join(output_dir, name)):
            continue
        if not _is_allowed_characterization_output(name, locked_yyyymmdd):
            raise CharacterizationBoundaryBreach(
                "non-allow-listed file in characterization output dir: "
                "{!r}".format(name)
            )


# ── Parser / row-count contract (memo §9) ────────────────────────────────────

def parse_characterization_payload(
    payload_bytes: bytes,
    nominal_date: date,
    sqldate_col: int = SQLDATE_COLUMN_INDEX,
) -> Dict[str, object]:
    """Decompress + row-count + offset-distribute + presence/absence
    against the expected offset taxonomy.

    GDELT 1.0 `.export.CSV` files are treated as **headerless positional
    files**. The function counts ALL non-empty data rows; it never
    silently subtracts a header. A header-like first-row anomaly is
    flagged. Per-SQLDATE counts and per-offset counts are returned, plus
    presence flags for each member of `EXPECTED_OFFSETS`, plus any
    unexpected offsets.

    A 2023+ SQLDATE raises `CharacterizationBoundaryBreach`.
    """
    if nominal_date >= SEAL_START:
        raise CharacterizationBoundaryBreach(
            "refusing to parse payload nominally dated 2023+: {}".format(
                nominal_date.isoformat()
            )
        )
    with zipfile.ZipFile(io.BytesIO(payload_bytes)) as zf:
        names = zf.namelist()
        if not names:
            return _empty_parse_result()
        with zf.open(names[0]) as fh:
            text = fh.read().decode("utf-8", "replace")

    lines = [ln for ln in text.splitlines() if ln.strip()]
    row_count = len(lines)
    sqldate_counts: Dict[date, int] = {}
    unparseable = 0
    malformed_short = 0
    header_anomaly = False

    for idx, ln in enumerate(lines):
        parts = ln.split("\t")
        if len(parts) <= sqldate_col:
            malformed_short += 1
            unparseable += 1
            if idx == 0:
                header_anomaly = True
            continue
        tok = parts[sqldate_col].strip()
        if len(tok) != 8 or not tok.isdigit():
            unparseable += 1
            if idx == 0:
                header_anomaly = True
            continue
        try:
            d = date(int(tok[0:4]), int(tok[4:6]), int(tok[6:8]))
        except ValueError:
            unparseable += 1
            if idx == 0:
                header_anomaly = True
            continue
        if d >= SEAL_START:
            raise CharacterizationBoundaryBreach(
                "2023+ SQLDATE row in payload nominally dated {}: "
                "{}".format(nominal_date.isoformat(), d.isoformat())
            )
        sqldate_counts[d] = sqldate_counts.get(d, 0) + 1

    # Per-SQLDATE distribution with offsets
    sqldate_distribution = []
    for d in sorted(sqldate_counts):
        cnt = sqldate_counts[d]
        offset = (d - nominal_date).days
        pct = (cnt / row_count * 100.0) if row_count else 0.0
        sqldate_distribution.append({
            "sqldate": d.isoformat(),
            "row_count": cnt,
            "offset_days": offset,
            "percentage_of_file_rows": round(pct, 6),
        })

    # Offset-bucket distribution
    offset_counts: Dict[int, int] = {}
    for entry in sqldate_distribution:
        offset_counts[entry["offset_days"]] = (
            offset_counts.get(entry["offset_days"], 0) + entry["row_count"]
        )
    offset_distribution = []
    for off in sorted(offset_counts):
        cnt = offset_counts[off]
        pct = (cnt / row_count * 100.0) if row_count else 0.0
        offset_distribution.append({
            "offset_days": off,
            "row_count": cnt,
            "percentage_of_file_rows": round(pct, 6),
        })

    nominal_count = offset_counts.get(0, 0)
    mismatch_count = sum(c for o, c in offset_counts.items() if o != 0)
    nominal_pct = (nominal_count / row_count * 100.0) if row_count else 0.0
    mismatch_pct = (mismatch_count / row_count * 100.0) if row_count else 0.0

    # Exact-integer bucket presence. Memo `a2a8fd5` §7 / §10 list the
    # locked taxonomy as bare integers `{0, -1, -7, -30, -365, -3650, +1}`
    # with no tolerance language; any observed offset that is not exactly
    # one of those integers is an unexpected offset and may trigger
    # `TAXONOMY-DEVIATION-REQUIRES-REVISION`. Leap-year arithmetic that
    # lands the 10-year lookback bucket on -3651 / -3652 / -3649 etc. is
    # itself a substrate finding the characterization run must surface,
    # not silently absorb.
    def _bucket_present(target: int) -> bool:
        return any(
            (o == target) and (c > 0)
            for o, c in offset_counts.items()
        )

    presence = {
        "0": _bucket_present(0),
        "-1": _bucket_present(-1),
        "-7": _bucket_present(-7),
        "-30": _bucket_present(-30),
        "-365": _bucket_present(-365),
        "-3650": _bucket_present(-3650),
        "+1": _bucket_present(1),
    }

    expected_set = set(EXPECTED_OFFSETS)
    unexpected_offsets = []
    for off in sorted(offset_counts):
        if off not in expected_set:
            unexpected_offsets.append({
                "offset_days": off,
                "row_count": offset_counts[off],
            })

    return {
        "row_count": row_count,
        "distinct_sqldates": len(sqldate_counts),
        "sqldate_distribution": sqldate_distribution,
        "offset_distribution": offset_distribution,
        "nominal_row_count": nominal_count,
        "nominal_percentage": round(nominal_pct, 6),
        "mismatch_row_count": mismatch_count,
        "mismatch_percentage": round(mismatch_pct, 6),
        "expected_offsets_presence": presence,
        "unexpected_offsets": unexpected_offsets,
        "header_anomaly_detected": header_anomaly,
        "unparseable_sqldate_rows": unparseable,
        "malformed_short_rows": malformed_short,
        "boundary_2023plus_flag": False,
    }


def _empty_parse_result() -> Dict[str, object]:
    return {
        "row_count": 0,
        "distinct_sqldates": 0,
        "sqldate_distribution": [],
        "offset_distribution": [],
        "nominal_row_count": 0,
        "nominal_percentage": 0.0,
        "mismatch_row_count": 0,
        "mismatch_percentage": 0.0,
        "expected_offsets_presence": {
            "0": False, "-1": False, "-7": False, "-30": False,
            "-365": False, "-3650": False, "+1": False,
        },
        "unexpected_offsets": [],
        "header_anomaly_detected": False,
        "unparseable_sqldate_rows": 0,
        "malformed_short_rows": 0,
        "boundary_2023plus_flag": False,
    }


# ── Per-file fetch (memo §6, exactly one GET attempt; no retry) ──────────────

def _characterize_one_file(
    nominal_date: date,
    url: str,
    opener: Callable,
    timeout: float,
) -> Tuple[Dict[str, object], Optional[bytes]]:
    """Make exactly one GET attempt. No retries. Returns
    `(result_dict, body_bytes_or_None)`. Body is None unless the response
    is HTTP 200."""
    result: Dict[str, object] = {
        "nominal_date": nominal_date.isoformat(),
        "url": url,
        "status": None,
        "location": None,
        "bytes_received": 0,
        "fetch_outcome": None,
        "exception_class": None,
        "exception_str": None,
    }
    body: Optional[bytes] = None
    try:
        resp = opener(url, timeout=timeout)
    except RedirectBlocked as exc:
        result["fetch_outcome"] = "REDIRECT_BLOCKED"
        result["exception_class"] = "RedirectBlocked"
        result["exception_str"] = str(exc)
        return result, None
    except urllib.error.HTTPError as exc:
        result["status"] = int(getattr(exc, "code", 0)) or None
        result["fetch_outcome"] = "HTTP_NON_200"
        result["exception_class"] = "HTTPError"
        result["exception_str"] = str(exc)
        headers = getattr(exc, "headers", None)
        if headers is not None and hasattr(headers, "get"):
            result["location"] = headers.get("Location")
        return result, None
    except Exception as exc:  # noqa: BLE001
        result["fetch_outcome"] = "CONNECTION_ERROR"
        result["exception_class"] = type(exc).__name__
        result["exception_str"] = str(exc)
        return result, None

    try:
        status = (
            int(resp.getcode())
            if hasattr(resp, "getcode") and resp.getcode() is not None
            else 200
        )
        result["status"] = status
        body_read = resp.read()
        result["bytes_received"] = len(body_read)
        if status == 200:
            result["fetch_outcome"] = "200_OK"
            body = body_read
        else:
            result["fetch_outcome"] = "HTTP_NON_200"
            headers = getattr(resp, "headers", None)
            if headers is not None and hasattr(headers, "get"):
                result["location"] = headers.get("Location")
            body = None
    finally:
        try:
            resp.close()
        except Exception:  # noqa: BLE001
            pass
    return result, body


# ── Aggregate metrics + outcome classification (memo §10/§11/§12) ────────────

def aggregate_metrics(
    per_file_results: List[Dict[str, object]],
) -> Dict[str, object]:
    """Compute the aggregate metrics required by memo §11 across all
    16 per-file results."""

    offset_file_count: Dict[int, int] = {}
    offset_row_total: Dict[int, int] = {}
    mismatch_rates: List[float] = []
    nominal_counts: List[int] = []
    lookback_counts: List[int] = []
    tplus1_by_date: List[Tuple[str, bool]] = []
    unexpected_files: List[Dict[str, object]] = []

    for r in per_file_results:
        parse = r.get("parse") or {}
        if not parse or "error" in parse:
            continue
        # Per-offset tallies
        for entry in parse.get("offset_distribution", []):
            off = entry["offset_days"]
            offset_file_count[off] = offset_file_count.get(off, 0) + 1
            offset_row_total[off] = (
                offset_row_total.get(off, 0) + entry["row_count"]
            )
        # Mismatch rates
        rate = parse.get("mismatch_percentage")
        if rate is not None:
            mismatch_rates.append(float(rate))
        # Denominator relationship inputs
        nominal_counts.append(int(parse.get("nominal_row_count", 0)))
        lookback_counts.append(
            int(parse.get("mismatch_row_count", 0))
        )
        # T+1 presence
        presence = parse.get("expected_offsets_presence", {}) or {}
        tplus1_by_date.append(
            (r["nominal_date"], bool(presence.get("+1", False)))
        )
        # Unexpected offsets
        unexpected = parse.get("unexpected_offsets") or []
        if unexpected:
            unexpected_files.append({
                "nominal_date": r["nominal_date"],
                "unexpected_offsets": unexpected,
            })

    # Mismatch-rate distribution
    if mismatch_rates:
        rate_min = min(mismatch_rates)
        rate_max = max(mismatch_rates)
        rate_mean = sum(mismatch_rates) / len(mismatch_rates)
        sorted_rates = sorted(mismatch_rates)
        mid = len(sorted_rates) // 2
        if len(sorted_rates) % 2 == 1:
            rate_median = sorted_rates[mid]
        else:
            rate_median = (sorted_rates[mid - 1] + sorted_rates[mid]) / 2.0
    else:
        rate_min = rate_max = rate_mean = rate_median = None

    # T+1 boundary: latest date with T+1, earliest date without T+1.
    # Sort by date.
    tplus1_sorted = sorted(tplus1_by_date, key=lambda x: x[0])
    latest_with_tplus1 = None
    earliest_without_tplus1 = None
    for d, present in tplus1_sorted:
        if present:
            latest_with_tplus1 = d
    for d, present in tplus1_sorted:
        if not present:
            earliest_without_tplus1 = d
            break

    # Taxonomy conformance
    expected_set = set(EXPECTED_OFFSETS)
    any_unexpected = len(unexpected_files) > 0
    all_conform = not any_unexpected

    return {
        "offset_file_count": {str(k): v for k, v in sorted(offset_file_count.items())},
        "offset_row_total": {str(k): v for k, v in sorted(offset_row_total.items())},
        "mismatch_rate_distribution": {
            "files": len(mismatch_rates),
            "min": rate_min,
            "max": rate_max,
            "mean": rate_mean,
            "median": rate_median,
        },
        "denominator_evidence": {
            "nominal_counts": nominal_counts,
            "lookback_counts": lookback_counts,
        },
        "tplus1_by_date": [
            {"nominal_date": d, "tplus1_present": p}
            for d, p in tplus1_sorted
        ],
        "latest_with_tplus1": latest_with_tplus1,
        "earliest_without_tplus1": earliest_without_tplus1,
        "all_files_conform_to_expected_taxonomy": all_conform,
        "any_unexpected_offset_observed": any_unexpected,
        "files_with_unexpected_offsets": unexpected_files,
    }


def classify_outcome(
    per_file_results: List[Dict[str, object]],
    aggregate: Dict[str, object],
) -> str:
    """Classify the run outcome per memo §12 / `a2a8fd5` §10.

    Deterministic decision logic:

    1. If any positive file has retrieval problems (non-200, redirect,
       connection error) OR any clean-200 file has a parser anomaly /
       unparseable rows / malformed-short rows / 2023+ boundary →
       `RETRIEVAL-OR-PARSER-BLOCK`.
    2. Else if any file contains an unexpected offset outside the
       expected taxonomy `{0, -1, -7, -30, -365, -3650, +1}` →
       `TAXONOMY-DEVIATION-REQUIRES-REVISION`.
    3. Else if all files conform to the expected taxonomy except that
       `+1` appears only in early files and disappears later (i.e.
       `latest_with_tplus1` precedes `earliest_without_tplus1` AND
       both are non-null) → `TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY`.
    4. Else if all files conform and the T+1 presence pattern is uniform
       (always present or always absent) → `TAXONOMY-STABLE-REKEY-BY-SQLDATE`.
    5. Else (clean files but ambiguous T+1 pattern, or fewer than
       expected files in the conforming set) → `INSUFFICIENT-CHARACTERIZATION`.
    """
    # Rule 1: retrieval/parser block
    for r in per_file_results:
        outcome = r.get("fetch_outcome")
        if outcome in ("REDIRECT_BLOCKED", "HTTP_NON_200", "CONNECTION_ERROR"):
            return "RETRIEVAL-OR-PARSER-BLOCK"
        parse = r.get("parse") or {}
        if not parse:
            return "RETRIEVAL-OR-PARSER-BLOCK"
        if "error" in parse:
            return "RETRIEVAL-OR-PARSER-BLOCK"
        if parse.get("header_anomaly_detected"):
            return "RETRIEVAL-OR-PARSER-BLOCK"
        if (parse.get("unparseable_sqldate_rows") or 0) > 0:
            return "RETRIEVAL-OR-PARSER-BLOCK"
        if (parse.get("malformed_short_rows") or 0) > 0:
            return "RETRIEVAL-OR-PARSER-BLOCK"
        if parse.get("boundary_2023plus_flag"):
            return "RETRIEVAL-OR-PARSER-BLOCK"

    # Rule 2: taxonomy deviation
    if aggregate.get("any_unexpected_offset_observed"):
        return "TAXONOMY-DEVIATION-REQUIRES-REVISION"

    # T+1 boundary logic
    latest = aggregate.get("latest_with_tplus1")
    earliest = aggregate.get("earliest_without_tplus1")
    tplus1_entries = aggregate.get("tplus1_by_date") or []
    if not tplus1_entries:
        return "INSUFFICIENT-CHARACTERIZATION"

    has_any_tplus1 = any(e["tplus1_present"] for e in tplus1_entries)
    has_any_no_tplus1 = any(not e["tplus1_present"] for e in tplus1_entries)

    if has_any_tplus1 and has_any_no_tplus1:
        # Boundary exists. Check ordering: latest_with_tplus1 must
        # precede earliest_without_tplus1.
        if latest is not None and earliest is not None and latest < earliest:
            return "TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY"
        # Otherwise the pattern is ambiguous (interleaved presence).
        return "INSUFFICIENT-CHARACTERIZATION"

    # Uniform T+1 pattern (always present or always absent).
    if aggregate.get("all_files_conform_to_expected_taxonomy"):
        return "TAXONOMY-STABLE-REKEY-BY-SQLDATE"

    return "INSUFFICIENT-CHARACTERIZATION"


# ── Summary / report writers ─────────────────────────────────────────────────

def _build_summary_md(metadata: Dict[str, object]) -> str:
    lines: List[str] = []
    lines.append("# Lane 2 GDELT 1.0 row-date characterization — summary")
    lines.append("")
    lines.append("Outcome: **{}**".format(metadata.get("outcome")))
    lines.append("")
    lines.append("Plan-lock memo: `a2a8fd5` — `docs/lane2_gdelt1_row_date_mismatch_characterization_plan_v0.1.md`")
    lines.append("Substrate-validation memo: `a8a9dd2`")
    lines.append("Event-file probe execution report: `9319d30`")
    lines.append("Design note: `e55e09a`")
    lines.append("Event-file probe implementation: `0b341b4`")
    lines.append("Parser-coverage patch: `845c51c`")
    lines.append("")
    lines.append("Recognized-list anchor: `{}`".format(
        metadata.get("recognized_list_path")
    ))
    lines.append("")
    lines.append("Characterization sample size: 16 dates")
    lines.append("")
    lines.append("Per-file fetch outcomes:")
    for r in metadata.get("per_file_results", []) or []:
        lines.append(
            "- {}: status={} outcome={} rows={} mismatch%={}".format(
                r.get("nominal_date"),
                r.get("status"),
                r.get("fetch_outcome"),
                (r.get("parse") or {}).get("row_count"),
                (r.get("parse") or {}).get("mismatch_percentage"),
            )
        )
    lines.append("")
    agg = metadata.get("aggregate") or {}
    lines.append("T+1 boundary:")
    lines.append("- latest with T+1: {}".format(agg.get("latest_with_tplus1")))
    lines.append("- earliest without T+1: {}".format(
        agg.get("earliest_without_tplus1")
    ))
    lines.append("")
    lines.append(
        "No market data; no Step 2; no spike-threshold tuning; no "
        "category / theme / actor / geography / tone filtering."
    )
    lines.append("")
    return "\n".join(lines)


# ── Output directory ─────────────────────────────────────────────────────────

def _fresh_output_dir(repo_root: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = os.path.join(
        repo_root, "results", "lane2_gdelt1_row_date_characterization", ts,
    )
    os.makedirs(out, exist_ok=False)
    return out


# ── Main characterization entry ──────────────────────────────────────────────

def run_row_date_characterization(
    repo_root: str,
    cli_flag: bool = True,
    opener: Optional[Callable] = None,
    timeout: float = DEFAULT_TIMEOUT,
    output_dir: Optional[str] = None,
) -> str:
    """Execute the 16-date row-date characterization sweep. Returns the
    output directory.

    Refuses (`SystemExit(_REFUSAL)`) unless all three guards pass: module
    constant, CLI flag, env var. The shipped module constant is False, so
    the default behavior is refusal.

    `opener` is injectable for tests (no real network). `output_dir` is
    likewise injectable for tests; production runs use a fresh timestamped
    directory under `results/lane2_gdelt1_row_date_characterization/`.
    """
    if not _guards_ok(cli_flag):
        raise SystemExit(_REFUSAL)

    units = _load_recognized_units(repo_root)
    validate_characterization_sample(units)
    urls = construct_characterization_urls()
    locked_yyyymmdd = [
        "{:04d}{:02d}{:02d}".format(d.year, d.month, d.day)
        for d in CHARACTERIZATION_DATES
    ]

    if output_dir is None:
        output_dir = _fresh_output_dir(repo_root)
    else:
        os.makedirs(output_dir, exist_ok=False)

    use_opener = (
        opener
        if opener is not None
        else _build_row_date_redirect_disabled_opener(timeout=timeout)
    )

    per_file_results: List[Dict[str, object]] = []
    for nominal, url in zip(CHARACTERIZATION_DATES, urls):
        result, body = _characterize_one_file(
            nominal_date=nominal,
            url=url,
            opener=use_opener,
            timeout=timeout,
        )
        if result.get("fetch_outcome") == "200_OK" and body is not None:
            yyyymmdd = "{:04d}{:02d}{:02d}".format(
                nominal.year, nominal.month, nominal.day,
            )
            payload_path = _checked_characterization_path(
                output_dir,
                "payload_{}.zip".format(yyyymmdd),
                locked_yyyymmdd,
            )
            with open(payload_path, "wb") as fh:
                fh.write(body)
            try:
                result["parse"] = parse_characterization_payload(
                    body,
                    nominal_date=nominal,
                    sqldate_col=SQLDATE_COLUMN_INDEX,
                )
            except CharacterizationBoundaryBreach as exc:
                result["parse"] = {
                    "error": str(exc),
                    "boundary_2023plus_flag": True,
                }
        per_file_results.append(result)

    aggregate = aggregate_metrics(per_file_results)
    outcome = classify_outcome(per_file_results, aggregate)

    metadata: Dict[str, object] = {
        "schema_version": "v0.1",
        "plan_lock_memo_anchor":
            "docs/lane2_gdelt1_row_date_mismatch_characterization_plan_v0.1.md",
        "plan_lock_memo_commit": "a2a8fd5",
        "substrate_validation_memo_commit": "a8a9dd2",
        "event_file_probe_execution_report_commit": "9319d30",
        "design_note_commit": "e55e09a",
        "event_file_probe_implementation_commit": "0b341b4",
        "parser_coverage_patch_commit": "845c51c",
        "recognized_list_path": RECOGNIZED_LIST_PATH,
        "event_file_base_url": EVENT_FILE_BASE_URL,
        "characterization_dates": [d.isoformat() for d in CHARACTERIZATION_DATES],
        "characterization_urls": urls,
        "expected_offsets": list(EXPECTED_OFFSETS),
        "per_file_results": per_file_results,
        "aggregate": aggregate,
        "outcome": outcome,
        "no_market_data": True,
        "no_step_2": True,
        "no_asset_or_return_logic": True,
        "no_category_theme_actor_filtering": True,
        "no_spike_threshold_tuning": True,
        "no_negative_control": True,
        "payload_preservation_policy":
            "all HTTP 200 responses among the 16 locked characterization dates",
    }

    meta_path = _checked_characterization_path(
        output_dir, "characterization_metadata.json", locked_yyyymmdd,
    )
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(metadata, fh, indent=2, sort_keys=True)

    summary_path = _checked_characterization_path(
        output_dir, "characterization_summary.md", locked_yyyymmdd,
    )
    with open(summary_path, "w", encoding="utf-8") as fh:
        fh.write(_build_summary_md(metadata))

    _assert_characterization_outputs_allowed(output_dir, locked_yyyymmdd)
    return output_dir


def main() -> None:
    p = argparse.ArgumentParser(
        description=(
            "Lane 2 GDELT 1.0 row-date characterization (16-date sweep)"
        )
    )
    p.add_argument(
        "--authorize-row-date-characterization-run",
        action="store_true",
    )
    p.add_argument("--repo-root", default=os.getcwd())
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    args = p.parse_args()
    if not _guards_ok(args.authorize_row_date_characterization_run):
        print(_REFUSAL)
        return
    out = run_row_date_characterization(
        args.repo_root,
        cli_flag=args.authorize_row_date_characterization_run,
        timeout=args.timeout,
    )
    print(
        "Row-date characterization outputs written under: {}".format(out)
    )


if __name__ == "__main__":
    main()
