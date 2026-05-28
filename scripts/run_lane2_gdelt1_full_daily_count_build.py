"""Standalone Lane 2 GDELT 1.0 full daily-count build runner.

Authorization basis: full-build design memo
`docs/lane2_gdelt1_full_daily_count_build_design_memo_v0.1.md`
(commit `7780a97`). The design memo authorizes neither source addition
nor execution; this implementation step (the present file + the paired
tests file) is the authorized source-addition step. The script ships
inert; execution requires its own separate authorization step that flips
the guard.

THIS RUNNER DOES NOT RUN BY DEFAULT AND PERFORMS NO DATA ACCESS UNLESS
THREE INDEPENDENT GUARDS ARE ALL SATISFIED:

  1. module constant FULL_BUILD_AUTHORIZED is True (ships False);
  2. CLI flag --authorize-full-build-run is passed;
  3. env var LANE2_FULL_BUILD_AUTHORIZED == "1".

If any guard is missing, the runner prints a refusal and exits BEFORE
any network opener construction, URL construction, output directory
creation, or artifact write.

This script is **standalone**. It does NOT import the event-file probe
runner, the row-date characterization runner, the count-feasibility
runner, the count-feasibility source module, or Gate 4D's index-listing
opener. It builds its own redirect-disabled opener (mirroring the prior
Lane 2 runner pattern with script-local names) scoped only to the daily
event-file URLs derived from the §10 recognized-list capture at SHA
`84ea721e…fff835fc`.

Scope: substrate-side daily attention row-count over the Lane 2
daily-regime window 2013-04-01 through 2022-12-31, keyed by event date
(SQLDATE). No market data, no Step 2, no asset/return logic, no
category/theme/actor/geography/tone filtering, no spike/burst
thresholds, no return-window logic, no signal-design choices, no claim
about market predictiveness. No payload preservation after parsing
(per memo §15.11): each fetched payload is hashed + parsed + discarded
before the next URL is fetched.

Eleven design decisions from `7780a97` are inherited verbatim:

  A: §10 recognized-list capture is the sole input authority.
  B: Output domain = full civil calendar [2013-04-01, 2022-12-31].
  C: Raw event rows, no dedup, no filters, no weights.
  D: Aggregate by SQLDATE only; per-file/per-offset diagnostics retained.
  E: Out-of-window SQLDATEs excluded from primary series; diagnostic recorded.
  F: Right-truncated counts with coverage_quality_flag + coverage_completeness.
  G: Known substrate gaps as expected-absent diagnostics; gap SQLDATEs eligible
     via neighbor contributions.
  H: Three-guard exact-once live retrieval; no retries.
  I: Hard-fail structural violations; reportable diagnostics elsewhere.
  J: Derived artifacts only; no raw payload preservation; default untracked.
  K: Future runner+test paths + 12 test categories.

Structural T-3650 zero (memo §10.2) is accepted: T-3650 contribution
is structurally zero for every in-window primary-series date under the
no-2023+ posture; future Step 2 logic may not treat T-3650 as an
available in-window signal feature unless a later explicit revision
memo changes the no-2023+ posture or output window.

No-2023+ posture (memo §11.1) is locked: no 2023+ URL construction,
no post-2022 publishing files, no 2023+ SQLDATE acceptance, no lifting
of the seal to fill coverage gaps, no post-2022 leakage. Lifting
requires a separately authorized memo.

Filtering by category/theme/actor/geography/tone is Step 2 /
instrument-construction territory (memo §8 Option C) and is forbidden
here; availability requires a future explicit revision memo that
retires the no-market-data firewall and explicitly authorizes
Step 2-style instrument-construction logic.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from datetime import date, datetime, timedelta, timezone
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


# ── Module-level authorization guard ─────────────────────────────────────────
#
# Ships False. Flipping this is a separate, explicit run-enablement commit
# under the future build-execution-authorization prompt. Mirrors prior
# Lane 2 runners' guard patterns (count-feasibility, event-file probe,
# row-date characterization).
FULL_BUILD_AUTHORIZED = True


# ── Substrate-pinned constants (no CLI / env / config override) ──────────────

RECOGNIZED_LIST_PATH = (
    "results/lane2_gdelt1_turn_b_recognized_list_capture/"
    "20260521T124853Z/recognized_list.json"
)

# Expected SHA-256 of the recognized-list capture (Gate 4C / turn-b live
# capture committed at `4015b97`). The runner asserts this at preflight.
RECOGNIZED_LIST_SHA256 = (
    "84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc"
)

EVENT_FILE_BASE_URL = "http://data.gdeltproject.org/events/"

# Locked daily-regime window (memo §2 / §4).
START_DATE = date(2013, 4, 1)
END_DATE = date(2022, 12, 31)
SEAL_START = date(2023, 1, 1)

# Exact-integer offset taxonomy (memo §4.2 / §9). No tolerance windows.
# Order is canonical: ascending offset value.
EXPECTED_OFFSETS: Tuple[int, ...] = (-3650, -365, -30, -7, -1, 0, 1)

# Sentinel SQLDATE subclass (substrate amendment memos at commits
# `7206e30` and `a1f2c4c`, R3 + Option α). Rows whose parsed SQLDATE
# equals a value in this set are recognized as placeholder-dated rather
# than lookback-retrocoded, routed into per-sentinel diagnostics,
# excluded from `total_in_window_rows` / `total_out_of_window_rows`
# under Option α, and NOT subject to the `EXPECTED_OFFSETS` halt. The
# halt-on-other-unexpected behavior is preserved verbatim for any
# non-sentinel SQLDATE whose offset is outside `EXPECTED_OFFSETS` —
# the discovery-preservation property remains load-bearing. Empirical
# basis: (i) `7206e30` — the 2019-12-31 daily-export file contained 120
# rows with SQLDATE `1920-01-01` (chunk_2019 substrate amendment;
# halt diagnostic archived under
# `archive/halted_attempts/lane2_gdelt1_full_daily_count_build/`
# `chunk_2019_20260525T192552Z/halt_diagnostic.json`); (ii) `a1f2c4c` —
# chunk_2020 Option B bounded-envelope research (D2 — narrow
# early-January-1920 family under precedence `D3 ⪼ D2 ⪼ D1`; 23/23
# inspected; 6 affected nominal file dates `2019-12-31`,
# `2020-01-01..2020-01-05`; 6 distinct placeholder/sentinel SQLDATE
# values `1920-01-01..1920-01-06`, contiguous, all directly observed;
# research output memo `dc48f55`; research output directory
# `results/lane2_gdelt1_placeholder_sqldate_research/`
# `chunk_2020_option_b_20260526T210247Z/`). Set is **evidence-bounded
# discrete tuple** — every member is directly observed; zero predicted
# values; no row-count threshold (`1920-01-06` is included despite
# being marginal at 85 rows in 1 file because it is directly
# observed). `date(1920, 1, 7)` and any other not-yet-observed
# placeholder-like value must still trigger halt-on-other-unexpected;
# extend only on direct substrate evidence via a separately scoped
# substrate amendment memo.
SENTINEL_SQLDATES: Tuple[date, ...] = (
    date(1920, 1, 1),
    date(1920, 1, 2),
    date(1920, 1, 3),
    date(1920, 1, 4),
    date(1920, 1, 5),
    date(1920, 1, 6),
)

# Known publishing-file substrate gaps from `a8a9dd2` §2 / §10 (memo §12).
# These dates are excluded from the recognized-list capture by construction;
# the runner does not fetch them.
KNOWN_SUBSTRATE_GAPS: Tuple[str, ...] = (
    "2014-01-23",
    "2014-01-24",
    "2014-01-25",
    "2014-03-19",
)

# Era cutoff for the T+1 era cone (memo §11.3). The latest publishing file
# confirmed to emit T+1 rows is `f_(2014-12-31)` per `858b501`; its T+1
# rows have SQLDATE = 2015-01-01. Therefore civil dates <= 2015-01-01 are
# treated as pre-2015 T+1 era for coverage purposes; dates >= 2015-01-02
# are treated as post-2015 era (T+1 not in expected cone).
T_PLUS_1_ERA_CUTOFF = date(2015, 1, 1)

# Timeouts (memo §13.7). Connection 30s, read 60s. The runner halts on
# any timeout (no retries; memo §13.4).
DEFAULT_CONNECT_TIMEOUT = 30.0
DEFAULT_READ_TIMEOUT = 60.0

# Parser constants. GDELT 1.0 .export.CSV files are TAB-separated and
# headerless positional; SQLDATE is column index 1 (memo §9 / `e55e09a`).
SQLDATE_COLUMN_INDEX = 1

# Civil-day arithmetic invariant (memo §6.8 reconciliation table).
CIVIL_DAYS_IN_WINDOW = (END_DATE - START_DATE).days + 1  # 3562

# Naive-expected daily URL count from the reconciliation table.
NAIVE_EXPECTED_DAILY_URLS = (
    CIVIL_DAYS_IN_WINDOW - len(KNOWN_SUBSTRATE_GAPS)
)  # 3558


# ── Output allow-list (memo §15.10 / Decision I §14.1) ───────────────────────
#
# Final-output basenames. Raw payload zips, extracted CSVs, and temp files
# are NOT in the allow-list and trigger a hard-fail per Decision I.
ALLOWED_OUTPUT_BASENAMES: Tuple[str, ...] = (
    "daily_count.csv",
    "build_metadata.json",
    "build_summary.md",
    "halt_diagnostic.json",
)


# ── Coverage flag closed domain (memo §11.3) ─────────────────────────────────

COVERAGE_SINGLE_FLAGS: Tuple[str, ...] = (
    "full",
    "t0_absent_substrate_gap",
    "right_truncated_2022_seal",
    "left_truncated_2013_edge",
    "t_plus_1_neighbor_substrate_gap",
    # IMPLEMENTATION EXTENSION (documented finding; surfaced in metadata):
    # The design memo §11.3 closed-domain table does NOT include a named
    # flag for T-1 / T-7 / T-30 / T-365 substrate-gap absences (cases
    # where the contributing publishing file at d+n is one of the four
    # known substrate-gap dates `2014-01-23/-24/-25/2014-03-19`).
    # This occurs in production at ~12 in-window dates near the early-
    # 2014 substrate-gap region. The implementation extends the closed
    # domain by ONE entry to handle these cases without silent
    # repair / silent design change. The extension is explicit and
    # surfaced in metadata.coverage_diagnostic.design_memo_extensions.
    "t_minus_n_neighbor_substrate_gap",
)

# Numeric order for joining multi-cause flags (memo §11.3 numeric order
# with the implementation extension inserted at position 6, before
# `multiple` which is the categorical name for multi-cause concatenation):
# 2 t0_absent_substrate_gap
# 3 right_truncated_2022_seal
# 4 left_truncated_2013_edge
# 5 t_plus_1_neighbor_substrate_gap
# 6 t_minus_n_neighbor_substrate_gap (implementation extension)
_COVERAGE_FLAG_ORDER: Tuple[str, ...] = (
    "t0_absent_substrate_gap",
    "right_truncated_2022_seal",
    "left_truncated_2013_edge",
    "t_plus_1_neighbor_substrate_gap",
    "t_minus_n_neighbor_substrate_gap",
)


# ── Refusal message ──────────────────────────────────────────────────────────

_REFUSAL = (
    "Lane 2 full daily-count build is NOT authorized. Requires "
    "FULL_BUILD_AUTHORIZED=True AND --authorize-full-build-run AND env "
    "LANE2_FULL_BUILD_AUTHORIZED=1. No network, no opener, no URL, no "
    "directory, no fetch, no artifact write."
)


# ── Exception classes ────────────────────────────────────────────────────────

class FullBuildRedirectBlocked(RuntimeError):
    """Raised by the full-build redirect-disabled opener on any 3xx
    response."""


class FullBuildBoundaryBreach(RuntimeError):
    """Raised when a hard boundary is hit (2023+ URL/SQLDATE, disallowed
    output, unexpected offset, non-recognized URL, etc.)."""


class RecognizedListSchemaError(RuntimeError):
    """Raised when the recognized-list capture JSON has an unexpected
    schema or fails SHA verification."""


class ReconciliationContradiction(RuntimeError):
    """Raised when the build-universe reconciliation finds a structural
    contradiction with the design memo's locked counts."""


class FetchFailure(RuntimeError):
    """Raised when a fetch fails (HTTP non-200, redirect, connection
    error, timeout) for an in-universe URL — hard-fail per Decision I.

    `code` carries the HTTP status when known (e.g. 404), else None. It is
    used ONLY to narrowly scope the committed documented-exception carve-out
    to a genuine upstream-object-unavailable 404; it does not relax hard-fail
    behavior for any other failure class or status."""

    def __init__(self, message: str, code: Optional[int] = None) -> None:
        super().__init__(message)
        self.code = code


# ── Local redirect-disabled opener (full-build-scoped) ───────────────────────
#
# Mirrors the prior Lane 2 redirect-disabled openers with script-local
# names. Does NOT reuse the row-date characterization opener, the
# event-file probe opener, or the Gate 4D index-listing opener. This
# opener is used only for daily event-file URLs constructed from the §10
# recognized-list capture's daily-classified in-window units.

class _FullBuildNoFollowRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Redirect handler whose 3xx hooks raise rather than follow.

    Overriding every 30x http_error_NNN hook makes the no-follow
    property structural — every redirect status is intercepted — not a
    runtime convention a caller could forget."""

    def _block(self, req, fp, code, msg, headers):
        raise FullBuildRedirectBlocked(
            "full-build opener blocked redirect (status {!r}); "
            "no follow, no fallback".format(code)
        )

    http_error_301 = _block
    http_error_302 = _block
    http_error_303 = _block
    http_error_307 = _block
    http_error_308 = _block


def _build_full_build_redirect_disabled_opener(
    timeout: float = DEFAULT_READ_TIMEOUT,
) -> Callable:
    """Build a callable opener with redirect-following disabled by
    construction. Used only for in-universe daily event-file URLs.

    The factory call fires no request; a single request occurs only when
    the returned callable is invoked. Guards are not flipped.
    """
    _opener = urllib.request.build_opener(
        _FullBuildNoFollowRedirectHandler()
    )
    _default_timeout = timeout

    def _full_build_opener(url, timeout=_default_timeout):
        # Exactly-once fetch per URL per run. No retry, no second GET,
        # no fallback. The caller (`_fetch_one_payload`) consumes
        # `.read()` once and discards the bytes before the next URL.
        return _opener.open(url, timeout=timeout)

    return _full_build_opener


# ── Three-guard gate ─────────────────────────────────────────────────────────

def _guards_ok(cli_flag: bool) -> bool:
    return (
        FULL_BUILD_AUTHORIZED
        and cli_flag
        and os.environ.get("LANE2_FULL_BUILD_AUTHORIZED") == "1"
    )


# ── Recognized-list loading + classification ─────────────────────────────────

_YEARLY_RE = re.compile(r"^\d{4}$")
_MONTHLY_RE = re.compile(r"^\d{4}-\d{2}$")
_DAILY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _hash_file_sha256(path: str) -> str:
    """Return SHA-256 hex digest of file contents."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_recognized_list(repo_root: str) -> Tuple[Dict[str, Any], str, int]:
    """Load the recognized_list.json capture read-only.

    Returns (capture_dict, sha256_hex, byte_size). Verifies the SHA-256
    against `RECOGNIZED_LIST_SHA256`; mismatch raises
    `RecognizedListSchemaError`.
    """
    path = os.path.join(repo_root, RECOGNIZED_LIST_PATH)
    if not os.path.isfile(path):
        raise RecognizedListSchemaError(
            "recognized-list capture missing at {}".format(path)
        )
    sha256 = _hash_file_sha256(path)
    if sha256 != RECOGNIZED_LIST_SHA256:
        raise RecognizedListSchemaError(
            "recognized-list SHA mismatch: got {} expected {}".format(
                sha256, RECOGNIZED_LIST_SHA256
            )
        )
    byte_size = os.path.getsize(path)
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if "recognized_in_window_units" not in data:
        raise RecognizedListSchemaError(
            "recognized_list.json missing 'recognized_in_window_units' "
            "key at {}".format(path)
        )
    units = data["recognized_in_window_units"]
    if not isinstance(units, list):
        raise RecognizedListSchemaError(
            "'recognized_in_window_units' is not a list at {}".format(path)
        )
    return data, sha256, byte_size


def classify_recognized_units(units: List[str]) -> Dict[str, List[str]]:
    """Classify each unit by pattern.

    Returns a dict with keys: yearly, monthly, daily_in_window,
    daily_out_of_window, unknown, duplicates.

    Pattern rules:
      yearly:           ^\\d{4}$
      monthly:          ^\\d{4}-\\d{2}$
      daily_in_window:  ^\\d{4}-\\d{2}-\\d{2}$ AND date in [START_DATE, END_DATE]
      daily_out_of_window: ^\\d{4}-\\d{2}-\\d{2}$ AND date outside window
      unknown:          anything else
      duplicates:       any unit appearing more than once
    """
    yearly: List[str] = []
    monthly: List[str] = []
    daily_in_window: List[str] = []
    daily_out_of_window: List[str] = []
    unknown: List[str] = []
    duplicates: List[str] = []
    seen: Set[str] = set()

    for u in units:
        if not isinstance(u, str):
            unknown.append(repr(u))
            continue
        if u in seen:
            duplicates.append(u)
            continue
        seen.add(u)
        if _YEARLY_RE.match(u):
            yearly.append(u)
        elif _MONTHLY_RE.match(u):
            monthly.append(u)
        elif _DAILY_RE.match(u):
            try:
                d = date.fromisoformat(u)
            except ValueError:
                unknown.append(u)
                continue
            if START_DATE <= d <= END_DATE:
                daily_in_window.append(u)
            else:
                daily_out_of_window.append(u)
        else:
            unknown.append(u)

    return {
        "yearly": sorted(yearly),
        "monthly": sorted(monthly),
        "daily_in_window": sorted(daily_in_window),
        "daily_out_of_window": sorted(daily_out_of_window),
        "unknown": sorted(unknown),
        "duplicates": sorted(duplicates),
    }


def build_reconciliation_report(units: List[str]) -> Dict[str, Any]:
    """Compute the reconciliation report comparing capture / civil-window
    arithmetic / gaps.

    The report surfaces the documented residual rather than inventing
    explanations. Per design memo §6.8: capture has 3,647 units; civil
    days 3,562; substrate gaps 4; naive-expected daily URLs 3,558;
    89-unit residual.
    """
    classification = classify_recognized_units(units)

    total_capture_units = len(units)
    daily_in_window_count = len(classification["daily_in_window"])

    daily_set = set(classification["daily_in_window"])
    gaps_set = set(KNOWN_SUBSTRATE_GAPS)
    gaps_present_in_capture = sorted(daily_set & gaps_set)
    fetch_set = sorted(daily_set - gaps_set)
    fetch_set_count = len(fetch_set)

    non_daily_units = (
        len(classification["yearly"])
        + len(classification["monthly"])
        + len(classification["daily_out_of_window"])
        + len(classification["unknown"])
        + len(classification["duplicates"])
    )

    residual = total_capture_units - daily_in_window_count

    report = {
        "total_capture_units": total_capture_units,
        "civil_days_in_window": CIVIL_DAYS_IN_WINDOW,
        "known_substrate_gaps": list(KNOWN_SUBSTRATE_GAPS),
        "known_substrate_gaps_count": len(KNOWN_SUBSTRATE_GAPS),
        "naive_expected_daily_urls": NAIVE_EXPECTED_DAILY_URLS,
        "classification": {
            "yearly_count": len(classification["yearly"]),
            "monthly_count": len(classification["monthly"]),
            "daily_in_window_count": daily_in_window_count,
            "daily_out_of_window_count": len(
                classification["daily_out_of_window"]
            ),
            "unknown_count": len(classification["unknown"]),
            "duplicates_count": len(classification["duplicates"]),
        },
        "yearly_units": classification["yearly"],
        "monthly_units": classification["monthly"],
        "daily_out_of_window_units": classification["daily_out_of_window"],
        "unknown_units": classification["unknown"],
        "duplicates": classification["duplicates"],
        "gaps_present_in_capture": gaps_present_in_capture,
        "fetch_set_count": fetch_set_count,
        "fetch_set": fetch_set,
        "residual_total": residual,
        "residual_non_daily_units": non_daily_units,
        "fetch_set_matches_naive_expectation": (
            fetch_set_count == NAIVE_EXPECTED_DAILY_URLS
        ),
    }
    return report


def assert_reconciliation_consistent(report: Dict[str, Any]) -> None:
    """Hard-fail if reconciliation structure contradicts the design memo.

    Surfaces concrete findings rather than inventing explanations.
    """
    if not report["fetch_set_matches_naive_expectation"]:
        raise ReconciliationContradiction(
            "fetch_set count {} != naive expectation {} ("
            "civil_days={} − gaps={})".format(
                report["fetch_set_count"],
                report["naive_expected_daily_urls"],
                report["civil_days_in_window"],
                report["known_substrate_gaps_count"],
            )
        )
    if report["gaps_present_in_capture"]:
        raise ReconciliationContradiction(
            "known substrate gap(s) present in recognized-list capture: "
            "{}".format(report["gaps_present_in_capture"])
        )
    if report["classification"]["duplicates_count"] > 0:
        raise ReconciliationContradiction(
            "recognized-list capture contains duplicate unit(s): "
            "{}".format(report["duplicates"])
        )
    if report["classification"]["unknown_count"] > 0:
        raise ReconciliationContradiction(
            "recognized-list capture contains unknown-pattern unit(s): "
            "{}".format(report["unknown_units"])
        )
    if report["classification"]["daily_out_of_window_count"] > 0:
        raise ReconciliationContradiction(
            "recognized-list capture contains daily unit(s) outside "
            "locked window [{}, {}]: {}".format(
                START_DATE.isoformat(),
                END_DATE.isoformat(),
                report["daily_out_of_window_units"],
            )
        )


# ── URL construction ─────────────────────────────────────────────────────────

def date_to_daily_url(d: date) -> str:
    """Build a daily event-file URL for a given date.

    Raises `FullBuildBoundaryBreach` on:
      - 2023+ date (no-2023+ posture; memo §11.1);
      - pre-window or post-window date (Decision A; memo §6.5).
    """
    if d >= SEAL_START:
        raise FullBuildBoundaryBreach(
            "refusing to construct URL for 2023+ date: {}".format(
                d.isoformat()
            )
        )
    if d < START_DATE or d > END_DATE:
        raise FullBuildBoundaryBreach(
            "refusing to construct URL for out-of-window date: "
            "{}".format(d.isoformat())
        )
    yyyymmdd = "{:04d}{:02d}{:02d}".format(d.year, d.month, d.day)
    return "{}{}.export.CSV.zip".format(EVENT_FILE_BASE_URL, yyyymmdd)


def construct_daily_urls(fetch_set: List[str]) -> List[str]:
    """Construct daily URLs for all dates in fetch_set, in canonical
    (sorted) order. Each fetch_set entry must be an ISO date string."""
    out: List[str] = []
    for iso in fetch_set:
        d = date.fromisoformat(iso)
        out.append(date_to_daily_url(d))
    return out


# ── Output allow-list ────────────────────────────────────────────────────────

def _is_allowed_output_basename(basename: str) -> bool:
    """Return True iff basename is on the final-output allow-list and
    contains no path-traversal characters."""
    if "/" in basename or "\\" in basename or ".." in basename:
        return False
    return basename in ALLOWED_OUTPUT_BASENAMES


def _checked_output_path(output_dir: str, basename: str) -> str:
    """Pre-write gate: assert basename is allow-listed BEFORE any write."""
    if not _is_allowed_output_basename(basename):
        raise FullBuildBoundaryBreach(
            "non-allow-listed full-build output: {!r}".format(basename)
        )
    return os.path.join(output_dir, basename)


def _assert_outputs_allowed(output_dir: str) -> None:
    """Post-hoc tripwire: every file in output_dir must be allow-listed.

    Raises `FullBuildBoundaryBreach` if any file fails the check.
    Subdirectories are not allowed at all (no `tmp/` left behind).
    """
    for name in sorted(os.listdir(output_dir)):
        full = os.path.join(output_dir, name)
        if os.path.isdir(full):
            raise FullBuildBoundaryBreach(
                "unexpected subdirectory in full-build output dir: "
                "{!r}".format(name)
            )
        if not _is_allowed_output_basename(name):
            raise FullBuildBoundaryBreach(
                "non-allow-listed file in full-build output dir: "
                "{!r}".format(name)
            )


# ── Fresh output directory ───────────────────────────────────────────────────

def _fresh_output_dir(repo_root: str, timestamp_utc: str) -> str:
    """Create the timestamped output dir under
    `results/lane2_gdelt1_full_daily_count_build/`.

    Uses os.makedirs(..., exist_ok=False) so a collision is a hard
    error. Called immediately before the network loop.
    """
    parent = os.path.join(
        repo_root,
        "results",
        "lane2_gdelt1_full_daily_count_build",
    )
    os.makedirs(parent, exist_ok=True)
    path = os.path.join(parent, timestamp_utc)
    os.makedirs(path, exist_ok=False)
    return path


# ── Parser ───────────────────────────────────────────────────────────────────

def parse_payload(
    payload_bytes: bytes,
    nominal_date: date,
    sqldate_col: int = SQLDATE_COLUMN_INDEX,
) -> Dict[str, Any]:
    """Decompress + parse a GDELT 1.0 daily event-file payload.

    Returns a dict with per-row aggregation results and diagnostics.

    Hard-fails on:
      - 2023+ nominal date (caller should never construct one);
      - 2023+ SQLDATE row;
      - unexpected offset outside `EXPECTED_OFFSETS`.

    Reportable diagnostics (do not halt):
      - malformed-short rows (column count < expected);
      - unparseable-SQLDATE rows (value not parseable as YYYYMMDD);
      - header anomaly on first row;
      - out-of-window SQLDATE rows (excluded from primary series,
        recorded in `out_of_window_sqldate_distribution`);
      - sentinel-SQLDATE rows (rows whose SQLDATE is in
        `SENTINEL_SQLDATES`; excluded from primary series and from offset
        computation under Option α; recorded in `per_sentinel_count` /
        `sentinel_sqldate_distribution` / `total_sentinel_rows`; substrate
        amendment memo at commit `7206e30`, R3 + Option α).
    """
    if nominal_date >= SEAL_START:
        raise FullBuildBoundaryBreach(
            "refusing to parse payload nominally dated 2023+: {}".format(
                nominal_date.isoformat()
            )
        )

    with zipfile.ZipFile(io.BytesIO(payload_bytes)) as zf:
        names = zf.namelist()
        if not names:
            return _empty_parse_result(nominal_date)
        with zf.open(names[0]) as fh:
            text = fh.read().decode("utf-8", "replace")

    lines = [ln for ln in text.splitlines() if ln.strip()]
    row_count = len(lines)

    per_offset_count: Dict[int, int] = {
        off: 0 for off in EXPECTED_OFFSETS
    }
    # In-window SQLDATE -> offset -> count
    sqldate_offset_counts: Dict[Tuple[str, int], int] = {}
    out_of_window_count = 0
    out_of_window_sqldate_distribution: Dict[str, Dict[str, int]] = {}
    # Sentinel-SQLDATE diagnostics (substrate amendment memo at commit
    # `7206e30`, R3 + Option α).
    per_sentinel_count: Dict[str, int] = {
        s.isoformat(): 0 for s in SENTINEL_SQLDATES
    }
    sentinel_sqldate_distribution: Dict[str, Dict[str, int]] = {}
    total_sentinel_rows = 0
    malformed_short = 0
    unparseable_sqldate = 0
    header_anomaly = False

    for idx, ln in enumerate(lines):
        parts = ln.split("\t")
        if len(parts) <= sqldate_col:
            malformed_short += 1
            if idx == 0:
                header_anomaly = True
            continue
        tok = parts[sqldate_col].strip()
        if len(tok) != 8 or not tok.isdigit():
            unparseable_sqldate += 1
            if idx == 0:
                header_anomaly = True
            continue
        try:
            d = date(int(tok[0:4]), int(tok[4:6]), int(tok[6:8]))
        except ValueError:
            unparseable_sqldate += 1
            if idx == 0:
                header_anomaly = True
            continue
        if d >= SEAL_START:
            raise FullBuildBoundaryBreach(
                "2023+ SQLDATE row in payload nominally dated {}: "
                "{}".format(nominal_date.isoformat(), d.isoformat())
            )
        if d in SENTINEL_SQLDATES:
            # Sentinel-SQLDATE row: placeholder-dated, NOT lookback-
            # retrocoded. Route to per-sentinel diagnostics only; exclude
            # from per_offset_count / sqldate_offset_counts /
            # out_of_window_sqldate_distribution (Option α). Halt-on-other-
            # unexpected behavior below is preserved for non-sentinel rows.
            iso_sentinel = d.isoformat()
            per_sentinel_count[iso_sentinel] = (
                per_sentinel_count.get(iso_sentinel, 0) + 1
            )
            nominal_iso = nominal_date.isoformat()
            entry = sentinel_sqldate_distribution.setdefault(
                iso_sentinel, {}
            )
            entry[nominal_iso] = entry.get(nominal_iso, 0) + 1
            total_sentinel_rows += 1
            continue
        offset = (d - nominal_date).days
        if offset not in EXPECTED_OFFSETS:
            raise FullBuildBoundaryBreach(
                "unexpected offset {!r} in payload nominally dated {}: "
                "SQLDATE {}".format(
                    offset, nominal_date.isoformat(), d.isoformat()
                )
            )
        # per_offset_count counts ALL observed rows at each offset
        # regardless of in/out-of-window status, matching the
        # `858b501` §11 aggregate-pattern (where T-3650 = 315 rows
        # across 16 files even though all T-3650 SQLDATEs were
        # out-of-window).
        per_offset_count[offset] += 1
        if START_DATE <= d <= END_DATE:
            iso = d.isoformat()
            key = (iso, offset)
            sqldate_offset_counts[key] = (
                sqldate_offset_counts.get(key, 0) + 1
            )
        else:
            out_of_window_count += 1
            iso = d.isoformat()
            if iso not in out_of_window_sqldate_distribution:
                out_of_window_sqldate_distribution[iso] = {}
            ostr = str(offset)
            out_of_window_sqldate_distribution[iso][ostr] = (
                out_of_window_sqldate_distribution[iso].get(ostr, 0) + 1
            )

    return {
        "nominal_date": nominal_date.isoformat(),
        "row_count": row_count,
        "header_anomaly_detected": header_anomaly,
        "malformed_short_rows": malformed_short,
        "unparseable_sqldate_rows": unparseable_sqldate,
        "per_offset_count": per_offset_count,
        "sqldate_offset_counts": sqldate_offset_counts,
        "out_of_window_row_count": out_of_window_count,
        "out_of_window_sqldate_distribution": (
            out_of_window_sqldate_distribution
        ),
        "per_sentinel_count": per_sentinel_count,
        "sentinel_sqldate_distribution": sentinel_sqldate_distribution,
        "total_sentinel_rows": total_sentinel_rows,
    }


def _empty_parse_result(nominal_date: date) -> Dict[str, Any]:
    return {
        "nominal_date": nominal_date.isoformat(),
        "row_count": 0,
        "header_anomaly_detected": False,
        "malformed_short_rows": 0,
        "unparseable_sqldate_rows": 0,
        "per_offset_count": {off: 0 for off in EXPECTED_OFFSETS},
        "sqldate_offset_counts": {},
        "out_of_window_row_count": 0,
        "out_of_window_sqldate_distribution": {},
        "per_sentinel_count": {
            s.isoformat(): 0 for s in SENTINEL_SQLDATES
        },
        "sentinel_sqldate_distribution": {},
        "total_sentinel_rows": 0,
    }


# ── Coverage flag + completeness computation ─────────────────────────────────

def expected_cone(d: date) -> Set[int]:
    """Era-conditioned expected cone (T-3650 excluded a priori per
    memo §10.2 / §11.3).

    Pre-2015 T+1 era:  d <= 2015-01-01 → {0, -1, -7, -30, -365, +1}
    Post-2015 era:     d >= 2015-01-02 → {0, -1, -7, -30, -365}
    """
    if d <= T_PLUS_1_ERA_CUTOFF:
        return {0, -1, -7, -30, -365, 1}
    return {0, -1, -7, -30, -365}


def contributing_file_nominal_date(d: date, offset: int) -> date:
    """Return the publishing-file nominal date that would contribute
    rows at the given offset to target SQLDATE d.

    Examples:
      offset = 0:    file at nominal d           (T=0)
      offset = -1:   file at nominal d+1         (T-1)
      offset = -7:   file at nominal d+7         (T-7)
      offset = -30:  file at nominal d+30        (T-30)
      offset = -365: file at nominal d+365       (T-365)
      offset = -3650:file at nominal d+3650      (T-3650)
      offset = +1:   file at nominal d-1         (T+1)
    """
    return d + timedelta(days=-offset)


def _classify_cone_member(
    d: date, offset: int, daily_set: Set[str], gaps_set: Set[str],
) -> str:
    """Classify a cone member's availability:
       'available' / 'substrate_gap' / 'out_of_universe_2023plus' /
       'out_of_universe_pre_2013' / 'unknown_absent'.
    """
    contributing = contributing_file_nominal_date(d, offset)
    if contributing >= SEAL_START:
        return "out_of_universe_2023plus"
    if contributing < START_DATE:
        return "out_of_universe_pre_2013"
    iso = contributing.isoformat()
    if iso in gaps_set:
        return "substrate_gap"
    if iso in daily_set:
        return "available"
    return "unknown_absent"


def coverage_for_date(
    d: date, daily_set: Set[str], gaps_set: Set[str],
) -> Dict[str, Any]:
    """Compute coverage_quality_flag, coverage_completeness, and details
    for civil date d.

    Returns a dict with keys: coverage_quality_flag,
    coverage_completeness, expected_contributing_files_count,
    available_contributing_files_count, cone_status (offset -> status).
    """
    cone = expected_cone(d)
    expected_count = len(cone)
    cone_status: Dict[int, str] = {}
    for offset in cone:
        cone_status[offset] = _classify_cone_member(
            d, offset, daily_set, gaps_set,
        )
    available_count = sum(
        1 for st in cone_status.values() if st == "available"
    )
    completeness = (
        available_count / expected_count if expected_count > 0 else 0.0
    )

    # Determine which named causes fire
    causes: List[str] = []
    if cone_status.get(0) == "substrate_gap":
        causes.append("t0_absent_substrate_gap")
    elif cone_status.get(0) == "unknown_absent":
        # Synthetic test condition: in-window non-gap date NOT in
        # daily_set. In production this cannot happen (daily_set ==
        # fetch_set ⊇ all in-window non-gap dates). For tests, map to
        # the t0-substrate-gap flag — the semantics is equivalent
        # ("T=0 contributing file absent for whatever reason").
        causes.append("t0_absent_substrate_gap")
    right_truncated = any(
        cone_status.get(off) == "out_of_universe_2023plus"
        for off in (-1, -7, -30, -365) if off in cone
    )
    if right_truncated:
        causes.append("right_truncated_2022_seal")
    if 1 in cone:
        st = cone_status[1]
        if st == "out_of_universe_pre_2013":
            causes.append("left_truncated_2013_edge")
        elif st in ("substrate_gap", "unknown_absent"):
            causes.append("t_plus_1_neighbor_substrate_gap")
    # IMPLEMENTATION EXTENSION (closed-domain extension; surfaced in
    # metadata): T-1 / T-7 / T-30 / T-365 substrate-gap absences are
    # not covered by the design memo §11.3 closed flag domain. Map them
    # to a new flag `t_minus_n_neighbor_substrate_gap`. Also covers the
    # synthetic test case where daily_set is incomplete (unknown_absent).
    t_minus_n_neighbor_absent = any(
        cone_status.get(off) in ("substrate_gap", "unknown_absent")
        for off in (-1, -7, -30, -365) if off in cone
    )
    if t_minus_n_neighbor_absent:
        causes.append("t_minus_n_neighbor_substrate_gap")

    # Build flag value
    if available_count == expected_count:
        flag = "full"
    else:
        # Order causes per _COVERAGE_FLAG_ORDER
        ordered = [c for c in _COVERAGE_FLAG_ORDER if c in causes]
        if not ordered:
            # Defensive — should not happen if classification is sound.
            # Surface as a hard-fail rather than silently emit garbage.
            raise FullBuildBoundaryBreach(
                "coverage classification produced no named cause for "
                "incomplete coverage at date {} (cone_status={})".format(
                    d.isoformat(), cone_status,
                )
            )
        if len(ordered) == 1:
            flag = ordered[0]
        else:
            flag = "+".join(ordered)

    return {
        "civil_date": d.isoformat(),
        "coverage_quality_flag": flag,
        "coverage_completeness": completeness,
        "expected_contributing_files_count": expected_count,
        "available_contributing_files_count": available_count,
        "cone_status": {str(k): v for k, v in cone_status.items()},
    }


def is_valid_coverage_flag(flag: str) -> bool:
    """Return True iff `flag` is in the closed value domain.

    Single-cause: one of COVERAGE_SINGLE_FLAGS.
    Multi-cause: an ordered concatenation joined by '+' of two-or-more
    distinct causes from _COVERAGE_FLAG_ORDER, in numeric order.
    """
    if flag in COVERAGE_SINGLE_FLAGS:
        return True
    parts = flag.split("+")
    if len(parts) < 2:
        return False
    if len(set(parts)) != len(parts):
        return False
    for p in parts:
        if p not in _COVERAGE_FLAG_ORDER:
            return False
    # Order check: parts must appear in numeric order
    indices = [_COVERAGE_FLAG_ORDER.index(p) for p in parts]
    return indices == sorted(indices)


# ── Per-date output domain enumeration ───────────────────────────────────────

def civil_date_domain() -> List[date]:
    """Return the canonical civil-calendar output domain
    [START_DATE, END_DATE] in ascending order. 3,562 dates."""
    out: List[date] = []
    d = START_DATE
    while d <= END_DATE:
        out.append(d)
        d += timedelta(days=1)
    return out


def t0_file_status(d: date, daily_set: Set[str], gaps_set: Set[str]) -> str:
    """Return one of 'present', 'expected_absent_per_recognized_list',
    'out_of_universe'."""
    iso = d.isoformat()
    if iso in gaps_set:
        return "expected_absent_per_recognized_list"
    if iso in daily_set:
        return "present"
    return "out_of_universe"


# ── Aggregation accumulator ──────────────────────────────────────────────────

def _new_accumulator() -> Dict[str, Any]:
    """Build an empty aggregation accumulator."""
    return {
        # civil_date_iso -> {offset_int -> count}
        "per_sqldate_per_offset": {},
        # Aggregate per-offset row totals across all in-window rows
        "per_offset_total": {off: 0 for off in EXPECTED_OFFSETS},
        # Aggregate out-of-window
        "out_of_window_row_count": 0,
        # out_of_window_sqldate_iso -> offset_str -> count
        "out_of_window_sqldate_distribution": {},
        # Aggregate diagnostics
        "total_malformed_short_rows": 0,
        "total_unparseable_sqldate_rows": 0,
        # Sentinel-SQLDATE aggregates (substrate amendment memo at commit
        # `7206e30`, R3 + Option α). per_sentinel_total maps sentinel
        # ISO-date string -> running count across all fetched files;
        # sentinel_sqldate_distribution maps sentinel ISO-date string ->
        # nominal-file-date ISO string -> count.
        "per_sentinel_total": {
            s.isoformat(): 0 for s in SENTINEL_SQLDATES
        },
        "sentinel_sqldate_distribution": {},
        "total_sentinel_rows": 0,
        # Per-file manifest (one entry per fetched URL)
        "per_file_manifest": [],
        # Aggregate parsed row count across all fetched files
        "total_parsed_rows": 0,
    }


def _ingest_parse_into_accumulator(
    accum: Dict[str, Any], parse_result: Dict[str, Any],
) -> None:
    """Fold a single payload's parse result into the running accumulator."""
    accum["total_parsed_rows"] += parse_result["row_count"]
    accum["total_malformed_short_rows"] += (
        parse_result["malformed_short_rows"]
    )
    accum["total_unparseable_sqldate_rows"] += (
        parse_result["unparseable_sqldate_rows"]
    )
    for off, cnt in parse_result["per_offset_count"].items():
        accum["per_offset_total"][off] += cnt
    for (iso, offset), cnt in parse_result["sqldate_offset_counts"].items():
        cell = accum["per_sqldate_per_offset"].setdefault(iso, {})
        cell[offset] = cell.get(offset, 0) + cnt
    accum["out_of_window_row_count"] += parse_result["out_of_window_row_count"]
    for iso, dist in parse_result[
        "out_of_window_sqldate_distribution"
    ].items():
        entry = accum["out_of_window_sqldate_distribution"].setdefault(
            iso, {}
        )
        for ostr, cnt in dist.items():
            entry[ostr] = entry.get(ostr, 0) + cnt
    accum["total_sentinel_rows"] += parse_result.get(
        "total_sentinel_rows", 0
    )
    for iso_sentinel, cnt in parse_result.get(
        "per_sentinel_count", {}
    ).items():
        accum["per_sentinel_total"][iso_sentinel] = (
            accum["per_sentinel_total"].get(iso_sentinel, 0) + cnt
        )
    for iso_sentinel, dist in parse_result.get(
        "sentinel_sqldate_distribution", {}
    ).items():
        entry = accum["sentinel_sqldate_distribution"].setdefault(
            iso_sentinel, {}
        )
        for nominal_iso, cnt in dist.items():
            entry[nominal_iso] = entry.get(nominal_iso, 0) + cnt


# ── Per-civil-date output row construction ───────────────────────────────────

def build_daily_count_rows(
    accum: Dict[str, Any], daily_set: Set[str], gaps_set: Set[str],
) -> List[Dict[str, Any]]:
    """Construct the primary daily_count rows: one per civil date in
    [START_DATE, END_DATE], with total / per-offset / coverage columns."""
    rows: List[Dict[str, Any]] = []
    for d in civil_date_domain():
        iso = d.isoformat()
        per_offset_cells = accum["per_sqldate_per_offset"].get(iso, {})
        total = sum(per_offset_cells.values())
        cov = coverage_for_date(d, daily_set, gaps_set)
        row = {
            "civil_date": iso,
            "total_row_count": total,
            "rows_from_offset_0": per_offset_cells.get(0, 0),
            "rows_from_offset_minus_1": per_offset_cells.get(-1, 0),
            "rows_from_offset_minus_7": per_offset_cells.get(-7, 0),
            "rows_from_offset_minus_30": per_offset_cells.get(-30, 0),
            "rows_from_offset_minus_365": per_offset_cells.get(-365, 0),
            "rows_from_offset_minus_3650": per_offset_cells.get(-3650, 0),
            "rows_from_offset_plus_1": per_offset_cells.get(1, 0),
            "t0_file_status": t0_file_status(d, daily_set, gaps_set),
            "expected_contributing_files_count": cov[
                "expected_contributing_files_count"
            ],
            "available_contributing_files_count": cov[
                "available_contributing_files_count"
            ],
            "coverage_quality_flag": cov["coverage_quality_flag"],
            "coverage_completeness": cov["coverage_completeness"],
        }
        if not is_valid_coverage_flag(row["coverage_quality_flag"]):
            raise FullBuildBoundaryBreach(
                "coverage_quality_flag {!r} for date {} is not in the "
                "closed value domain".format(
                    row["coverage_quality_flag"], iso,
                )
            )
        rows.append(row)
    return rows


# ── Artifact writers ─────────────────────────────────────────────────────────

_DAILY_COUNT_COLUMNS: Tuple[str, ...] = (
    "civil_date",
    "total_row_count",
    "rows_from_offset_0",
    "rows_from_offset_minus_1",
    "rows_from_offset_minus_7",
    "rows_from_offset_minus_30",
    "rows_from_offset_minus_365",
    "rows_from_offset_minus_3650",
    "rows_from_offset_plus_1",
    "t0_file_status",
    "expected_contributing_files_count",
    "available_contributing_files_count",
    "coverage_quality_flag",
    "coverage_completeness",
)


def write_daily_count_csv(
    output_dir: str, rows: List[Dict[str, Any]],
) -> str:
    """Write daily_count.csv (allow-list gated). Returns full path."""
    path = _checked_output_path(output_dir, "daily_count.csv")
    lines = [",".join(_DAILY_COUNT_COLUMNS)]
    for r in rows:
        cells = []
        for col in _DAILY_COUNT_COLUMNS:
            v = r[col]
            if isinstance(v, float):
                cells.append("{:.6f}".format(v))
            else:
                cells.append(str(v))
        lines.append(",".join(cells))
    body = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return path


def write_build_metadata_json(
    output_dir: str, metadata: Dict[str, Any],
) -> str:
    """Write build_metadata.json (allow-list gated). Returns full path.

    Metadata is serialized with sort_keys=True for deterministic output.
    """
    path = _checked_output_path(output_dir, "build_metadata.json")
    body = json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return path


def write_build_summary_md(
    output_dir: str, summary_text: str,
) -> str:
    """Write build_summary.md (allow-list gated). Returns full path."""
    path = _checked_output_path(output_dir, "build_summary.md")
    if not summary_text.endswith("\n"):
        summary_text = summary_text + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(summary_text)
    return path


def render_build_summary(
    metadata: Dict[str, Any], daily_rows: List[Dict[str, Any]],
) -> str:
    """Render a human-readable summary from the metadata + rows."""
    aggregate = metadata.get("aggregate_metrics", {})
    parts = [
        "# Lane 2 full daily-count build summary",
        "",
        "- output_domain: {} → {} ({} civil days)".format(
            START_DATE.isoformat(), END_DATE.isoformat(),
            len(daily_rows),
        ),
        "- total_parsed_rows: {}".format(
            aggregate.get("total_parsed_rows", 0)
        ),
        "- total_in_window_rows: {}".format(
            aggregate.get("total_in_window_rows", 0)
        ),
        "- total_out_of_window_rows: {}".format(
            aggregate.get("total_out_of_window_rows", 0)
        ),
        "- per_offset_totals (in-window): {}".format(
            aggregate.get("per_offset_total", {})
        ),
        "- fetch_set_count: {}".format(
            metadata.get("recognized_list_capture", {}).get(
                "fetch_set_count", 0
            )
        ),
        "- coverage_flag_distribution: {}".format(
            aggregate.get("coverage_flag_distribution", {})
        ),
        "- substrate_gap_dates_not_fetched: {}".format(
            list(KNOWN_SUBSTRATE_GAPS)
        ),
    ]
    return "\n".join(parts)


# ── Boundary declarations ────────────────────────────────────────────────────

def _boundary_declarations() -> Dict[str, bool]:
    return {
        "no_market_data": True,
        "no_step_2": True,
        "no_asset_or_return_logic": True,
        "no_category_theme_actor_filtering": True,
        "no_spike_threshold_tuning": True,
        "no_negative_control": True,
        "no_2023plus_access": True,
        "no_payload_preservation_after_parsing": True,
        "no_market_calendar_alignment": True,
    }


# ── Fetch one payload (with hash + parse + discard) ──────────────────────────

def _fetch_one_payload(
    opener: Callable, url: str, timeout: float = DEFAULT_READ_TIMEOUT,
) -> Tuple[bytes, str]:
    """Fetch a single URL, return (payload_bytes, sha256_hex).

    Raises:
      - FullBuildBoundaryBreach via the redirect-disabled opener on 3xx
        (translated below to FetchFailure for uniform hard-fail handling);
      - FetchFailure on HTTP non-200, urllib HTTPError/URLError, or
        any other network exception.

    The caller is responsible for discarding the returned bytes after
    parsing (payload-discard mechanism per memo §15.11).
    """
    try:
        resp = opener(url, timeout=timeout)
    except FullBuildRedirectBlocked as e:
        raise FetchFailure(
            "redirect blocked for {}: {}".format(url, e)
        )
    except urllib.error.HTTPError as e:
        raise FetchFailure(
            "HTTP error {} for {}: {}".format(e.code, url, e.reason),
            code=e.code,
        )
    except urllib.error.URLError as e:
        raise FetchFailure(
            "URL error for {}: {}".format(url, e.reason)
        )
    except (TimeoutError, OSError) as e:
        raise FetchFailure(
            "connection error / timeout for {}: {!r}".format(url, e)
        )
    status = resp.getcode() if hasattr(resp, "getcode") else None
    if status != 200:
        raise FetchFailure(
            "non-200 HTTP {} for {}".format(status, url),
            code=status,
        )
    payload = resp.read()
    if hasattr(resp, "close"):
        resp.close()
    sha = hashlib.sha256(payload).hexdigest()
    return payload, sha


# ── Halt diagnostic writer (hard-fail path) ──────────────────────────────────

def _write_halt_diagnostic(output_dir: str, diagnostic: Dict[str, Any]) -> None:
    """Write halt_diagnostic.json on hard-fail. Allow-list gated."""
    try:
        path = _checked_output_path(output_dir, "halt_diagnostic.json")
        body = json.dumps(diagnostic, indent=2, sort_keys=True) + "\n"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
    except Exception:
        # Best-effort; don't mask the original hard-fail.
        pass


# ── Main run function ────────────────────────────────────────────────────────

def run_full_daily_count_build(
    repo_root: str,
    cli_flag: bool = False,
    timestamp_utc: Optional[str] = None,
    timeout: float = DEFAULT_READ_TIMEOUT,
    opener: Optional[Callable] = None,
) -> Dict[str, Any]:
    """Execute the full daily-count build.

    Three-guard refusal applies BEFORE any opener construction, URL
    construction, output directory creation, or artifact write.

    `opener` is optional; if not provided, the runner constructs its own
    redirect-disabled opener. Tests may inject a fake opener.
    """
    if not _guards_ok(cli_flag):
        print(_REFUSAL, file=sys.stderr)
        raise SystemExit(2)

    if timestamp_utc is None:
        timestamp_utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # 1. Load + verify recognized-list capture
    capture_data, sha256, byte_size = _load_recognized_list(repo_root)
    units = capture_data["recognized_in_window_units"]

    # 2. Reconciliation
    reconciliation = build_reconciliation_report(units)
    assert_reconciliation_consistent(reconciliation)

    fetch_set = reconciliation["fetch_set"]
    daily_set: Set[str] = set(fetch_set)  # gaps NOT in daily_set (per Decision G)
    gaps_set: Set[str] = set(KNOWN_SUBSTRATE_GAPS)

    # 3. Fresh output dir
    output_dir = _fresh_output_dir(repo_root, timestamp_utc)

    # 4. Opener
    if opener is None:
        opener = _build_full_build_redirect_disabled_opener(timeout=timeout)

    # 5. Aggregation
    accum = _new_accumulator()
    urls = construct_daily_urls(fetch_set)
    started_at = datetime.now(timezone.utc).isoformat()

    try:
        for iso, url in zip(fetch_set, urls):
            nominal = date.fromisoformat(iso)
            payload, payload_sha = _fetch_one_payload(opener, url, timeout=timeout)
            parse_result = parse_payload(payload, nominal)
            # Payload-discard: drop the bytes immediately after parsing.
            del payload
            accum["per_file_manifest"].append({
                "url": url,
                "nominal_date": iso,
                "http_status": 200,
                "http_status_class": "200_OK",
                "payload_sha256": payload_sha,
                "row_count": parse_result["row_count"],
                "malformed_short_rows": parse_result["malformed_short_rows"],
                "unparseable_sqldate_rows": parse_result[
                    "unparseable_sqldate_rows"
                ],
                "header_anomaly_detected": parse_result[
                    "header_anomaly_detected"
                ],
                "out_of_window_row_count": parse_result[
                    "out_of_window_row_count"
                ],
                "per_offset_count": {
                    str(k): v
                    for k, v in parse_result["per_offset_count"].items()
                },
                "status": "fetched_and_parsed",
            })
            _ingest_parse_into_accumulator(accum, parse_result)
        # Synthesize expected-absent entries for substrate-gap dates.
        for gap in KNOWN_SUBSTRATE_GAPS:
            accum["per_file_manifest"].append({
                "url": None,
                "nominal_date": gap,
                "http_status": None,
                "http_status_class": "not_requested",
                "payload_sha256": None,
                "row_count": 0,
                "malformed_short_rows": 0,
                "unparseable_sqldate_rows": 0,
                "header_anomaly_detected": False,
                "out_of_window_row_count": 0,
                "per_offset_count": {
                    str(k): 0 for k in EXPECTED_OFFSETS
                },
                "status": "expected_absent_per_recognized_list",
            })
    except (FullBuildBoundaryBreach, FetchFailure,
            RecognizedListSchemaError, ReconciliationContradiction) as e:
        _write_halt_diagnostic(output_dir, {
            "halt_class": type(e).__name__,
            "message": str(e),
            "started_at_utc": started_at,
            "halted_at_utc": datetime.now(timezone.utc).isoformat(),
        })
        raise

    finished_at = datetime.now(timezone.utc).isoformat()

    # 6. Build daily_count rows
    daily_rows = build_daily_count_rows(accum, daily_set, gaps_set)

    # 7. Coverage distribution diagnostic
    coverage_flag_distribution: Dict[str, int] = {}
    for row in daily_rows:
        f = row["coverage_quality_flag"]
        coverage_flag_distribution[f] = (
            coverage_flag_distribution.get(f, 0) + 1
        )

    # 8. Build metadata
    metadata: Dict[str, Any] = {
        "run_anchors": {
            "design_memo_commit": "7780a97",
            "decision_memo_commit": "0065d10",
            "characterization_report_commit": "858b501",
            "recognized_list_capture_commit": "4015b97",
            "start_date": START_DATE.isoformat(),
            "end_date": END_DATE.isoformat(),
            "seal_start": SEAL_START.isoformat(),
            "no_2023plus_posture_commit": "0ddbd51",
            "started_at_utc": started_at,
            "finished_at_utc": finished_at,
        },
        "recognized_list_capture": {
            "path": RECOGNIZED_LIST_PATH,
            "sha256": sha256,
            "byte_size": byte_size,
            "total_capture_units": reconciliation["total_capture_units"],
            "fetch_set_count": reconciliation["fetch_set_count"],
            "reconciliation": reconciliation,
        },
        "per_file_manifest": accum["per_file_manifest"],
        "substrate_gap_diagnostic": {
            "known_substrate_gap_dates": list(KNOWN_SUBSTRATE_GAPS),
            "substrate_gap_dates_not_fetched": list(KNOWN_SUBSTRATE_GAPS),
        },
        "out_of_window_sqldate_diagnostic": {
            "total_out_of_window_rows": accum["out_of_window_row_count"],
            "out_of_window_rows_excluded_from_primary_series": True,
            "per_sqldate_distribution": accum[
                "out_of_window_sqldate_distribution"
            ],
        },
        "parser_anomaly_diagnostic": {
            "total_malformed_short_rows": accum[
                "total_malformed_short_rows"
            ],
            "total_unparseable_sqldate_rows": accum[
                "total_unparseable_sqldate_rows"
            ],
        },
        "coverage_diagnostic": {
            "coverage_flag_distribution": coverage_flag_distribution,
            "closed_value_domain_single_flags": list(
                COVERAGE_SINGLE_FLAGS
            ),
            "era_cutoff": T_PLUS_1_ERA_CUTOFF.isoformat(),
            "design_memo_extensions": {
                "t_minus_n_neighbor_substrate_gap": (
                    "Implementation extension to design memo §11.3 "
                    "closed flag domain. The design memo's 6-entry "
                    "closed domain (full / t0_absent_substrate_gap / "
                    "right_truncated_2022_seal / "
                    "left_truncated_2013_edge / "
                    "t_plus_1_neighbor_substrate_gap / multiple) does "
                    "not include a named flag for T-1 / T-7 / T-30 / "
                    "T-365 substrate-gap absences (cases where a "
                    "contributing publishing file at d+n is one of "
                    "the four known substrate-gap dates "
                    "2014-01-23/-24/-25/2014-03-19). This occurs in "
                    "production at ~12 in-window dates near the "
                    "early-2014 substrate-gap region. The "
                    "implementation extends the closed domain by ONE "
                    "entry to handle these cases without silent "
                    "repair or silent design change. The extension is "
                    "explicit and surfaced here. A future revision "
                    "memo may formalize this extension or revise "
                    "§11.3."
                ),
            },
        },
        "output_allow_list": list(ALLOWED_OUTPUT_BASENAMES),
        "boundary_declarations": _boundary_declarations(),
        "aggregation_invariants": {
            "civil_days_in_output_domain": len(daily_rows),
            "expected_civil_days": CIVIL_DAYS_IN_WINDOW,
            "domain_matches_expected": (
                len(daily_rows) == CIVIL_DAYS_IN_WINDOW
            ),
            "per_offset_total": {
                str(k): v
                for k, v in accum["per_offset_total"].items()
            },
            "t_minus_3650_in_primary_is_zero": (
                # Structural T-3650 zero invariant (memo §10.2): every
                # in-window date's per-SQLDATE T-3650 count is 0,
                # because every in-window d would require f_(d+3650)
                # in [2023-04-01, 2032-12-31], all excluded by no-2023+.
                sum(
                    cells.get(-3650, 0)
                    for cells in accum["per_sqldate_per_offset"].values()
                ) == 0
            ),
        },
        "aggregate_metrics": {
            "total_parsed_rows": accum["total_parsed_rows"],
            "total_in_window_rows": sum(
                sum(cells.values())
                for cells in accum["per_sqldate_per_offset"].values()
            ),
            "total_out_of_window_rows": accum["out_of_window_row_count"],
            "per_offset_total_observed_in_plus_out": {
                str(k): v
                for k, v in accum["per_offset_total"].items()
            },
            "per_offset_total": {
                str(k): v
                for k, v in accum["per_offset_total"].items()
            },
            "coverage_flag_distribution": coverage_flag_distribution,
        },
    }

    # 9. Counting invariant assertion. Note: per_offset_total now
    # counts ALL observed rows at each offset (in + out of window),
    # matching the `858b501` §11 aggregate pattern. The in-window total
    # comes from summing per_sqldate_per_offset (which is in-window
    # only).
    total_in_window = sum(
        sum(cells.values())
        for cells in accum["per_sqldate_per_offset"].values()
    )
    total_observed_per_offset = sum(accum["per_offset_total"].values())
    total_out_of_window = accum["out_of_window_row_count"]
    total_malformed = accum["total_malformed_short_rows"]
    total_unparseable = accum["total_unparseable_sqldate_rows"]
    # per_offset_total = in_window + out_of_window (parser-observed rows)
    if total_observed_per_offset != total_in_window + total_out_of_window:
        raise FullBuildBoundaryBreach(
            "per_offset_total invariant violation: "
            "per_offset_total={} != in_window={} + out_of_window={}".format(
                total_observed_per_offset,
                total_in_window,
                total_out_of_window,
            )
        )
    counted_total = (
        total_observed_per_offset
        + total_malformed
        + total_unparseable
    )
    if counted_total != accum["total_parsed_rows"]:
        raise FullBuildBoundaryBreach(
            "counting invariant violation: observed_per_offset={} + "
            "malformed={} + unparseable={} = {} != total_parsed={}".format(
                total_observed_per_offset, total_malformed,
                total_unparseable, counted_total,
                accum["total_parsed_rows"],
            )
        )

    # 10. Write artifacts
    csv_path = write_daily_count_csv(output_dir, daily_rows)
    md_text = render_build_summary(metadata, daily_rows)
    md_path = write_build_summary_md(output_dir, md_text)
    json_path = write_build_metadata_json(output_dir, metadata)

    # 11. Post-hoc tripwire
    _assert_outputs_allowed(output_dir)

    print(
        "Full daily-count build outputs written under: {}".format(output_dir),
        file=sys.stdout,
    )

    return {
        "output_dir": output_dir,
        "daily_count_csv_path": csv_path,
        "build_metadata_json_path": json_path,
        "build_summary_md_path": md_path,
        "metadata": metadata,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Chunked execution support (chunk-design memo `5962c20`)
# ─────────────────────────────────────────────────────────────────────────────
#
# Yearly fetch-file-date chunks. The full 3,558-URL fetch set is partitioned
# into 10 disjoint per-year chunks; each chunk is a separately authorized
# execution unit. The merge step (offline, no GDELT contact) consumes the
# per-chunk derived artifacts and produces the canonical full-build outputs.
#
# Chunking does NOT change SQLDATE re-keying, the no-2023+ posture, the
# no-retry rule, exactly-once fetch semantics, recognized-list authority,
# the no-market-data firewall, or `c10ae74`'s coverage-domain amendment.

CHUNK_IDS: Tuple[str, ...] = (
    "chunk_2013_partial",
    "chunk_2014",
    "chunk_2015",
    "chunk_2016",
    "chunk_2017",
    "chunk_2018",
    "chunk_2019",
    "chunk_2020",
    "chunk_2021",
    "chunk_2022",
)

EXPECTED_CHUNK_COUNTS: Dict[str, int] = {
    "chunk_2013_partial": 275,
    "chunk_2014": 361,
    "chunk_2015": 365,
    "chunk_2016": 366,
    "chunk_2017": 365,
    "chunk_2018": 365,
    "chunk_2019": 365,
    "chunk_2020": 366,
    "chunk_2021": 365,
    "chunk_2022": 365,
}

CHUNK_YEAR_RANGES: Dict[str, Tuple[date, date]] = {
    "chunk_2013_partial": (date(2013, 4, 1), date(2013, 12, 31)),
    "chunk_2014": (date(2014, 1, 1), date(2014, 12, 31)),
    "chunk_2015": (date(2015, 1, 1), date(2015, 12, 31)),
    "chunk_2016": (date(2016, 1, 1), date(2016, 12, 31)),
    "chunk_2017": (date(2017, 1, 1), date(2017, 12, 31)),
    "chunk_2018": (date(2018, 1, 1), date(2018, 12, 31)),
    "chunk_2019": (date(2019, 1, 1), date(2019, 12, 31)),
    "chunk_2020": (date(2020, 1, 1), date(2020, 12, 31)),
    "chunk_2021": (date(2021, 1, 1), date(2021, 12, 31)),
    "chunk_2022": (date(2022, 1, 1), date(2022, 12, 31)),
}

# Per-chunk derived artifact allow-list (chunk-design memo §8).
ALLOWED_CHUNK_OUTPUT_BASENAMES: Tuple[str, ...] = (
    "chunk_contributions.csv",
    "chunk_metadata.json",
    "chunk_summary.md",
    "halt_diagnostic.json",
)


class ChunkManifestError(RuntimeError):
    """Raised on chunk manifest / merge contract violations
    (chunk-design memo §11 / §12)."""


def validate_chunk_id(chunk_id: str) -> None:
    """Raise ChunkManifestError if chunk_id is not one of the canonical
    10 IDs."""
    if chunk_id not in CHUNK_IDS:
        raise ChunkManifestError(
            "unknown chunk_id {!r}; valid ids are: {}".format(
                chunk_id, list(CHUNK_IDS)
            )
        )


def build_chunk_manifest(chunk_id: str, fetch_set: List[str]) -> List[str]:
    """Filter the full recognized-list-derived `fetch_set` to ISO date
    strings whose date lies in chunk_id's yearly range.

    `fetch_set` must be the 3,558-URL set from
    `build_reconciliation_report(units)["fetch_set"]` (= daily-in-window
    minus the 4 known substrate gaps).

    Returns sorted in-chunk ISO date strings. Hard-fails on count
    mismatch against `EXPECTED_CHUNK_COUNTS`.
    """
    validate_chunk_id(chunk_id)
    start, end = CHUNK_YEAR_RANGES[chunk_id]
    start_iso = start.isoformat()
    end_iso = end.isoformat()
    out = sorted(u for u in fetch_set if start_iso <= u <= end_iso)
    expected = EXPECTED_CHUNK_COUNTS[chunk_id]
    if len(out) != expected:
        raise ChunkManifestError(
            "chunk {!r}: actual count {} != expected {}".format(
                chunk_id, len(out), expected
            )
        )
    return out


def build_all_chunk_manifests(fetch_set: List[str]) -> Dict[str, List[str]]:
    """Return all 10 chunk manifests as a dict {chunk_id -> [iso, ...]}."""
    return {cid: build_chunk_manifest(cid, fetch_set) for cid in CHUNK_IDS}


def chunk_manifest_digest(chunk_iso_dates: List[str]) -> str:
    """Compute the deterministic SHA-256 digest of a chunk's URL list.

    URLs are constructed from the sorted date list (no network);
    each URL is ASCII-encoded and newline-terminated before hashing.
    """
    sorted_dates = sorted(chunk_iso_dates)
    h = hashlib.sha256()
    for iso in sorted_dates:
        d = date.fromisoformat(iso)
        url = date_to_daily_url(d)
        h.update(url.encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()


def assert_chunk_manifests_partition(
    manifests: Dict[str, List[str]],
    full_fetch_set: List[str],
) -> None:
    """Validate chunk-manifest partition contract:
      - exact set of 10 chunk IDs (no missing, no extra);
      - pairwise disjoint (no URL in multiple chunks);
      - union equals full recognized-list-derived fetch set;
      - no 2023+ dates;
      - no non-daily units (regex YYYY-MM-DD only).

    Raises ChunkManifestError on any violation.
    """
    expected_ids = set(CHUNK_IDS)
    actual_ids = set(manifests.keys())
    if actual_ids != expected_ids:
        raise ChunkManifestError(
            "chunk id set mismatch: missing={}, extra={}".format(
                sorted(expected_ids - actual_ids),
                sorted(actual_ids - expected_ids),
            )
        )
    seen: Dict[str, str] = {}
    for cid in CHUNK_IDS:
        urls = manifests[cid]
        for u in urls:
            if u in seen:
                raise ChunkManifestError(
                    "duplicate URL {!r} in chunks {!r} and {!r}".format(
                        u, seen[u], cid
                    )
                )
            seen[u] = cid
            if not _DAILY_RE.match(u):
                raise ChunkManifestError(
                    "chunk {!r} contains non-daily unit: {!r}".format(cid, u)
                )
            if u >= "2023-01-01":
                raise ChunkManifestError(
                    "chunk {!r} contains 2023+ date: {!r}".format(cid, u)
                )
    union = set(seen.keys())
    full = set(full_fetch_set)
    missing = sorted(full - union)
    extra = sorted(union - full)
    if missing or extra:
        raise ChunkManifestError(
            "union != full fetch set: missing_from_union={}, "
            "extra_in_union={}".format(missing, extra)
        )


def is_allowed_chunk_output_basename(basename: str) -> bool:
    """Return True iff basename is on the per-chunk artifact allow-list
    and contains no path-traversal characters."""
    if "/" in basename or "\\" in basename or ".." in basename:
        return False
    return basename in ALLOWED_CHUNK_OUTPUT_BASENAMES


def _checked_chunk_output_path(output_dir: str, basename: str) -> str:
    """Pre-write gate for per-chunk artifacts."""
    if not is_allowed_chunk_output_basename(basename):
        raise FullBuildBoundaryBreach(
            "non-allow-listed chunk output: {!r}".format(basename)
        )
    return os.path.join(output_dir, basename)


def _assert_chunk_outputs_allowed(output_dir: str) -> None:
    """Post-hoc tripwire for per-chunk output directories."""
    for name in sorted(os.listdir(output_dir)):
        full = os.path.join(output_dir, name)
        if os.path.isdir(full):
            raise FullBuildBoundaryBreach(
                "unexpected subdirectory in chunk output dir: {!r}".format(name)
            )
        if not is_allowed_chunk_output_basename(name):
            raise FullBuildBoundaryBreach(
                "non-allow-listed file in chunk output dir: {!r}".format(name)
            )


def _fresh_chunk_output_dir(
    repo_root: str, chunk_id: str, timestamp_utc: str,
) -> str:
    """Create `results/lane2_gdelt1_full_daily_count_build/<chunk_id>_<ts>/`.

    Uses `os.makedirs(..., exist_ok=False)` so any collision is hard-fail
    (chunk-design memo §12 "no successful chunk may be overwritten").
    """
    validate_chunk_id(chunk_id)
    parent = os.path.join(
        repo_root, "results", "lane2_gdelt1_full_daily_count_build",
    )
    os.makedirs(parent, exist_ok=True)
    path = os.path.join(parent, "{}_{}".format(chunk_id, timestamp_utc))
    os.makedirs(path, exist_ok=False)
    return path


_CHUNK_CONTRIBUTIONS_COLUMNS: Tuple[str, ...] = (
    "civil_date",
    "chunk_id",
    "rows_from_offset_0",
    "rows_from_offset_minus_1",
    "rows_from_offset_minus_7",
    "rows_from_offset_minus_30",
    "rows_from_offset_minus_365",
    "rows_from_offset_minus_3650",
    "rows_from_offset_plus_1",
    "total_rows",
)


def write_chunk_contributions_csv(
    output_dir: str, chunk_id: str,
    sqldate_offset_counts: Dict[Tuple[str, int], int],
) -> str:
    """Write `chunk_contributions.csv`: per-in-window-SQLDATE per-offset
    contributions tagged with `chunk_id`.

    Out-of-window SQLDATEs (e.g., the T-3650 routing per §10.2 of `7780a97`)
    are NOT written here; they go into chunk_metadata.json's
    out_of_window_sqldate_diagnostic section.
    """
    path = _checked_chunk_output_path(output_dir, "chunk_contributions.csv")
    per_sqldate: Dict[str, Dict[int, int]] = {}
    for (iso, offset), cnt in sqldate_offset_counts.items():
        per_sqldate.setdefault(iso, {})[offset] = cnt
    lines = [",".join(_CHUNK_CONTRIBUTIONS_COLUMNS)]
    for iso in sorted(per_sqldate.keys()):
        cells = per_sqldate[iso]
        total = sum(cells.values())
        row = [
            iso, chunk_id,
            str(cells.get(0, 0)),
            str(cells.get(-1, 0)),
            str(cells.get(-7, 0)),
            str(cells.get(-30, 0)),
            str(cells.get(-365, 0)),
            str(cells.get(-3650, 0)),
            str(cells.get(1, 0)),
            str(total),
        ]
        lines.append(",".join(row))
    body = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return path


def write_chunk_metadata_json(
    output_dir: str, metadata: Dict[str, Any],
) -> str:
    """Write `chunk_metadata.json` (deterministic via sort_keys)."""
    path = _checked_chunk_output_path(output_dir, "chunk_metadata.json")
    body = json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return path


def write_chunk_summary_md(output_dir: str, text: str) -> str:
    """Write `chunk_summary.md`."""
    path = _checked_chunk_output_path(output_dir, "chunk_summary.md")
    if not text.endswith("\n"):
        text = text + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def _write_chunk_halt_diagnostic(
    output_dir: str, diagnostic: Dict[str, Any],
) -> None:
    """Write per-chunk `halt_diagnostic.json` on hard-fail
    (per `c10ae74` Decision 2A)."""
    try:
        path = _checked_chunk_output_path(output_dir, "halt_diagnostic.json")
        body = json.dumps(diagnostic, indent=2, sort_keys=True) + "\n"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
    except Exception:
        pass


def render_chunk_summary(
    chunk_id: str,
    metadata: Dict[str, Any],
) -> str:
    """Human-readable summary for one chunk."""
    aggregate = metadata.get("aggregate_metrics", {})
    parts = [
        "# Lane 2 full daily-count build chunk summary: {}".format(chunk_id),
        "",
        "- chunk_id: {}".format(chunk_id),
        "- expected_file_count: {}".format(
            EXPECTED_CHUNK_COUNTS.get(chunk_id, "unknown")
        ),
        "- actual_completed_file_count: {}".format(
            aggregate.get("actual_completed_file_count", 0)
        ),
        "- total_in_window_rows: {}".format(
            aggregate.get("total_in_window_rows", 0)
        ),
        "- total_out_of_window_rows: {}".format(
            aggregate.get("total_out_of_window_rows", 0)
        ),
        "- per_offset_total: {}".format(
            aggregate.get("per_offset_total", {})
        ),
        "- chunk_manifest_digest: {}".format(
            metadata.get("chunk_manifest_digest", "")
        ),
    ]
    ded = metadata.get("documented_exception_diagnostic", {})
    if ded.get("documented_unavailable_data_confirmed_days", 0):
        parts.extend([
            "",
            "- documented_exception_label: {}".format(
                ded.get("documented_exception_label", "")
            ),
            "- expected_calendar_days: {}".format(
                ded.get("expected_calendar_days", "")
            ),
            "- raw_processed_days: {}".format(
                ded.get("raw_processed_days", "")
            ),
            "- documented_unavailable_data_confirmed_days: {}".format(
                ded.get("documented_unavailable_data_confirmed_days", 0)
            ),
            "- recovered_days: {}".format(ded.get("recovered_days", 0)),
            "- known_no_data_gap_days: {}".format(
                ded.get("known_no_data_gap_days", 0)
            ),
            "- terminal_status_days: {} (= raw_processed_days + "
            "documented_unavailable_data_confirmed_days)".format(
                ded.get("terminal_status_days", "")
            ),
            "- NOTE: this chunk reaches terminal status with one date "
            "carrying the documented-exception label above (official-source "
            "data-confirmed; raw object unavailable; represented only). The "
            "per-category day counts are itemized above and in "
            "documented_exception_diagnostic; raw_processed_days and "
            "documented_unavailable_data_confirmed_days are reported "
            "separately so each category stays distinct.",
        ])
    return "\n".join(parts)


# ── Documented-exception support (narrow upstream-object-unavailable carve-out) ─
#
# Runtime carve-out from the FetchFailure-halt path, governed by the committed
# contract + representation artifact (commit `5f43a13`; design memos
# `e60a88a` → `854a606` → `36202b9` → `50dda46`). It applies ONLY to the exact
# committed quintuple (chunk_id + date + raw_filename + label + md5/size
# agreement) and ONLY on a genuine 404. It does NOT fetch/recover/parse rows,
# does NOT treat the date as a no-data gap, does NOT amend `KNOWN_SUBSTRATE_GAPS`,
# and does NOT reduce expected_file_count. Any other 404 (other date, other
# chunk, wrong filename) or any non-404 failure still hard-fails as before.
DOCUMENTED_EXCEPTIONS_CONFIG_PATH = (
    "configs/lane2_gdelt1_documented_exceptions.json"
)
DOCUMENTED_EXCEPTION_LABEL = (
    "UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY"
)


def load_documented_exceptions(
    repo_root: str,
) -> Dict[Tuple[str, str], Dict[str, Any]]:
    """Load committed documented-exception entries keyed by (chunk_id, date).

    Returns {} if the contract file is absent (ordinary halt-on-fetch-failure
    behavior fully preserved). Each contract entry is cross-validated against
    its committed representation artifact; an entry is DROPPED (not loaded) if
    the artifact is missing, the label is wrong, the md5/size disagree, or any
    of the negative-evidence booleans are not False. A dropped/mismatched entry
    therefore CANNOT widen the carve-out — it falls through to the normal halt.
    """
    config_path = os.path.join(repo_root, DOCUMENTED_EXCEPTIONS_CONFIG_PATH)
    if not os.path.isfile(config_path):
        return {}
    with open(config_path, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    out: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for entry in cfg.get("documented_exceptions", []):
        label = entry.get("label")
        scope = entry.get("allowed_scope", {})
        rep_rel = entry.get("representation_artifact")
        if label != DOCUMENTED_EXCEPTION_LABEL or not rep_rel:
            continue
        rep_path = os.path.join(repo_root, rep_rel)
        if not os.path.isfile(rep_path):
            continue
        with open(rep_path, "r", encoding="utf-8") as fh:
            rep = json.load(fh)
        if (
            rep.get("label") != DOCUMENTED_EXCEPTION_LABEL
            or rep.get("chunk_id") != scope.get("chunk_id")
            or rep.get("date") != scope.get("date")
            or rep.get("raw_filename") != scope.get("raw_filename")
            or rep.get("catalog_md5") != scope.get("catalog_md5")
            or rep.get("catalog_filesize_bytes")
            != scope.get("catalog_filesize_bytes")
            or rep.get("raw_object_parsed") is not False
            or rep.get("rows_recovered") is not False
            or rep.get("no_data_gap") is not False
            or rep.get("recovered") is not False
            or rep.get("raw_processed") is not False
        ):
            continue
        if not (
            scope.get("chunk_id")
            and scope.get("date")
            and scope.get("raw_filename")
            and scope.get("catalog_md5")
            and scope.get("catalog_filesize_bytes")
        ):
            continue
        out[(scope["chunk_id"], scope["date"])] = {
            "label": label,
            "chunk_id": scope["chunk_id"],
            "date": scope["date"],
            "raw_filename": scope["raw_filename"],
            "catalog_md5": scope["catalog_md5"],
            "catalog_filesize_bytes": scope["catalog_filesize_bytes"],
            "representation_artifact": rep_rel,
        }
    return out


def documented_exception_match(
    chunk_id: str,
    iso: str,
    url: str,
    exceptions: Dict[Tuple[str, str], Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Return the documented-exception entry IFF the exact quintuple matches.

    Quintuple = chunk_id + date + raw_filename (verified against the URL) +
    label + (md5 AND size as recorded in the committed contract/representation,
    validated during load). Any deviation returns None -> normal hard-fail.
    Caller must additionally require a genuine 404 before invoking the carve-out.
    """
    entry = exceptions.get((chunk_id, iso))
    if entry is None:
        return None
    if entry["label"] != DOCUMENTED_EXCEPTION_LABEL:
        return None
    if not url.endswith("/" + entry["raw_filename"]):
        return None
    return entry


def run_chunk_build(
    chunk_id: str,
    repo_root: str,
    cli_flag: bool = False,
    timestamp_utc: Optional[str] = None,
    timeout: float = DEFAULT_READ_TIMEOUT,
    opener: Optional[Callable] = None,
) -> Dict[str, Any]:
    """Execute one chunk's daily fetch set.

    Same three-guard discipline as `run_full_daily_count_build`. Refusal
    fires BEFORE recognized-list load, output dir creation, opener
    construction, URL construction, or any fetch.

    Writes per-chunk derived artifacts (`chunk_contributions.csv` +
    `chunk_metadata.json` + `chunk_summary.md`) under
    `results/lane2_gdelt1_full_daily_count_build/<chunk_id>_<ts>/`.

    Does NOT write `daily_count.csv` / `build_metadata.json` /
    `build_summary.md` (those are merge-step outputs, not chunk-step
    outputs).
    """
    # 1. chunk_id validation BEFORE guard check (the chunk_id is the
    #    operational primary key and an unknown id is a structural
    #    contract violation, not a guard-gated execution attempt).
    validate_chunk_id(chunk_id)

    # 2. Three-guard refusal — applies BEFORE any side effect.
    if not _guards_ok(cli_flag):
        print(_REFUSAL, file=sys.stderr)
        raise SystemExit(2)

    if timestamp_utc is None:
        timestamp_utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # 3. Load recognized list + reconciliation (mirrors full-build path).
    capture_data, sha256, byte_size = _load_recognized_list(repo_root)
    units = capture_data["recognized_in_window_units"]
    reconciliation = build_reconciliation_report(units)
    assert_reconciliation_consistent(reconciliation)
    fetch_set_full = reconciliation["fetch_set"]
    daily_set: Set[str] = set(fetch_set_full)
    gaps_set: Set[str] = set(KNOWN_SUBSTRATE_GAPS)

    # 4. Construct chunk manifest + digest.
    chunk_manifest = build_chunk_manifest(chunk_id, fetch_set_full)
    digest = chunk_manifest_digest(chunk_manifest)

    # 5. Fresh chunk output dir.
    output_dir = _fresh_chunk_output_dir(
        repo_root, chunk_id, timestamp_utc,
    )

    # 6. Opener.
    if opener is None:
        opener = _build_full_build_redirect_disabled_opener(timeout=timeout)

    # 7. Aggregate per-chunk.
    sqldate_offset_counts: Dict[Tuple[str, int], int] = {}
    per_offset_total: Dict[int, int] = {off: 0 for off in EXPECTED_OFFSETS}
    out_of_window_row_count = 0
    out_of_window_distribution: Dict[str, Dict[str, int]] = {}
    total_parsed_rows = 0
    total_malformed_short = 0
    total_unparseable_sqldate = 0
    # Sentinel-SQLDATE chunk-local accumulators (substrate amendment memo
    # at commit `7206e30`, R3 + Option α).
    per_sentinel_total: Dict[str, int] = {
        s.isoformat(): 0 for s in SENTINEL_SQLDATES
    }
    sentinel_sqldate_distribution: Dict[str, Dict[str, int]] = {}
    total_sentinel_rows = 0
    per_file_manifest: List[Dict[str, Any]] = []
    documented_exceptions = load_documented_exceptions(repo_root)
    documented_exception_entries: List[Dict[str, Any]] = []
    started_at = datetime.now(timezone.utc).isoformat()
    actual_completed = 0

    try:
        for iso in chunk_manifest:
            nominal = date.fromisoformat(iso)
            url = date_to_daily_url(nominal)
            try:
                payload, payload_sha = _fetch_one_payload(
                    opener, url, timeout=timeout,
                )
            except FetchFailure as fe:
                match = (
                    documented_exception_match(
                        chunk_id, iso, url, documented_exceptions,
                    )
                    if fe.code == 404
                    else None
                )
                if match is None:
                    raise
                # Committed documented exception: officially data-confirmed
                # but raw object unavailable. Do NOT fetch/recover/parse rows;
                # do NOT treat as a no-data gap; do NOT amend
                # KNOWN_SUBSTRATE_GAPS. Record and continue to later raw days.
                # This does NOT count as a raw-processed day (actual_completed
                # is not incremented).
                per_file_manifest.append({
                    "url": url,
                    "nominal_date": iso,
                    "http_status": 404,
                    "http_status_class": "404_upstream_object_unavailable",
                    "status": (
                        "documented_exception_upstream_object_"
                        "unavailable_data_confirmed_represented_only"
                    ),
                    "documented_exception_label": match["label"],
                    "catalog_md5": match["catalog_md5"],
                    "catalog_filesize_bytes": match["catalog_filesize_bytes"],
                    "representation_artifact": match["representation_artifact"],
                    "raw_object_parsed": False,
                    "rows_recovered": False,
                })
                documented_exception_entries.append({
                    "date": iso,
                    "raw_filename": match["raw_filename"],
                    "url": url,
                    "label": match["label"],
                    "catalog_md5": match["catalog_md5"],
                    "catalog_filesize_bytes": match["catalog_filesize_bytes"],
                    "representation_artifact": match["representation_artifact"],
                    "http_status": 404,
                    "raw_object_parsed": False,
                    "rows_recovered": False,
                })
                continue
            parse_result = parse_payload(payload, nominal)
            del payload
            per_file_manifest.append({
                "url": url,
                "nominal_date": iso,
                "http_status": 200,
                "http_status_class": "200_OK",
                "payload_sha256": payload_sha,
                "row_count": parse_result["row_count"],
                "malformed_short_rows": parse_result["malformed_short_rows"],
                "unparseable_sqldate_rows":
                    parse_result["unparseable_sqldate_rows"],
                "header_anomaly_detected":
                    parse_result["header_anomaly_detected"],
                "out_of_window_row_count":
                    parse_result["out_of_window_row_count"],
                "per_offset_count": {
                    str(k): v
                    for k, v in parse_result["per_offset_count"].items()
                },
                "status": "fetched_and_parsed",
            })
            total_parsed_rows += parse_result["row_count"]
            total_malformed_short += parse_result["malformed_short_rows"]
            total_unparseable_sqldate += (
                parse_result["unparseable_sqldate_rows"]
            )
            for off, cnt in parse_result["per_offset_count"].items():
                per_offset_total[off] += cnt
            for key, cnt in parse_result["sqldate_offset_counts"].items():
                sqldate_offset_counts[key] = (
                    sqldate_offset_counts.get(key, 0) + cnt
                )
            out_of_window_row_count += parse_result["out_of_window_row_count"]
            for d_iso, dist in parse_result[
                "out_of_window_sqldate_distribution"
            ].items():
                entry = out_of_window_distribution.setdefault(d_iso, {})
                for ostr, cnt in dist.items():
                    entry[ostr] = entry.get(ostr, 0) + cnt
            total_sentinel_rows += parse_result.get(
                "total_sentinel_rows", 0
            )
            for iso_sentinel, cnt in parse_result.get(
                "per_sentinel_count", {}
            ).items():
                per_sentinel_total[iso_sentinel] = (
                    per_sentinel_total.get(iso_sentinel, 0) + cnt
                )
            for iso_sentinel, dist in parse_result.get(
                "sentinel_sqldate_distribution", {}
            ).items():
                entry = sentinel_sqldate_distribution.setdefault(
                    iso_sentinel, {}
                )
                for nominal_iso, cnt in dist.items():
                    entry[nominal_iso] = entry.get(nominal_iso, 0) + cnt
            actual_completed += 1
    except (FullBuildBoundaryBreach, FetchFailure,
            RecognizedListSchemaError, ReconciliationContradiction,
            ChunkManifestError) as e:
        _write_chunk_halt_diagnostic(output_dir, {
            "halt_class": type(e).__name__,
            "message": str(e),
            "started_at_utc": started_at,
            "halted_at_utc": datetime.now(timezone.utc).isoformat(),
            "chunk_id": chunk_id,
            "actual_completed_file_count": actual_completed,
        })
        raise

    finished_at = datetime.now(timezone.utc).isoformat()

    total_in_window_rows = sum(sqldate_offset_counts.values())
    counted_total = (
        total_in_window_rows
        + out_of_window_row_count
        + total_sentinel_rows
        + total_malformed_short
        + total_unparseable_sqldate
    )
    if counted_total != total_parsed_rows:
        raise FullBuildBoundaryBreach(
            "chunk {!r} counting invariant violation: "
            "in_window={} + out_of_window={} + sentinel={} + "
            "malformed={} + unparseable={} = {} != total_parsed={}".format(
                chunk_id, total_in_window_rows, out_of_window_row_count,
                total_sentinel_rows, total_malformed_short,
                total_unparseable_sqldate, counted_total, total_parsed_rows,
            )
        )

    metadata: Dict[str, Any] = {
        "chunk_id": chunk_id,
        "source_recognized_list_sha256": sha256,
        "recognized_list_byte_size": byte_size,
        "chunk_manifest_digest": digest,
        "expected_file_count": EXPECTED_CHUNK_COUNTS[chunk_id],
        "actual_completed_file_count": actual_completed,
        "script_commit_anchor": "bc7b66b (+5962c20 chunk-design + this patch)",
        "guard_state_after_run": {
            "FULL_BUILD_AUTHORIZED_module_constant_at_completion":
                FULL_BUILD_AUTHORIZED,
        },
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "no_retry_confirmation": True,
        "boundary_declarations": _boundary_declarations(),
        "per_file_manifest": per_file_manifest,
        "substrate_gap_diagnostic": {
            "known_substrate_gap_dates": list(KNOWN_SUBSTRATE_GAPS),
            "substrate_gap_dates_not_fetched": list(KNOWN_SUBSTRATE_GAPS),
        },
        "documented_exception_diagnostic": {
            "documented_exception_label": DOCUMENTED_EXCEPTION_LABEL,
            "expected_calendar_days": len(chunk_manifest),
            "raw_processed_days": actual_completed,
            "documented_unavailable_data_confirmed_days": len(
                documented_exception_entries
            ),
            "recovered_days": 0,
            "known_no_data_gap_days": 0,
            "terminal_status_days": (
                actual_completed + len(documented_exception_entries)
            ),
            "terminal_status_complete": (
                (actual_completed + len(documented_exception_entries))
                == len(chunk_manifest)
            ),
            "raw_object_parsed_for_documented_days": False,
            "rows_recovered_for_documented_days": False,
            "recovered": False,
            "no_data_gap": False,
            "known_substrate_gap_amended": False,
            "bigquery_count_semantics_note": (
                "Any official BigQuery COUNT(*) for a documented-exception "
                "date is coverage evidence, NOT an exact runner-output "
                "validation gate."
            ),
            "documented_exceptions": documented_exception_entries,
        },
        "out_of_window_sqldate_diagnostic": {
            "total_out_of_window_rows": out_of_window_row_count,
            "out_of_window_rows_excluded_from_chunk_contributions": True,
            "per_sqldate_distribution": out_of_window_distribution,
        },
        "parser_anomaly_diagnostic": {
            "total_malformed_short_rows": total_malformed_short,
            "total_unparseable_sqldate_rows": total_unparseable_sqldate,
        },
        "output_allow_list": list(ALLOWED_CHUNK_OUTPUT_BASENAMES),
        "aggregate_metrics": {
            "total_parsed_rows": total_parsed_rows,
            "total_in_window_rows": total_in_window_rows,
            "total_out_of_window_rows": out_of_window_row_count,
            "total_sentinel_rows": total_sentinel_rows,
            "actual_completed_file_count": actual_completed,
            "per_offset_total": {
                str(k): v for k, v in per_offset_total.items()
            },
            "per_sentinel_total": per_sentinel_total,
            "sentinel_sqldate_distribution": (
                sentinel_sqldate_distribution
            ),
        },
    }

    csv_path = write_chunk_contributions_csv(
        output_dir, chunk_id, sqldate_offset_counts,
    )
    json_path = write_chunk_metadata_json(output_dir, metadata)
    md_path = write_chunk_summary_md(
        output_dir, render_chunk_summary(chunk_id, metadata),
    )

    _assert_chunk_outputs_allowed(output_dir)

    print(
        "Chunk {} outputs written under: {}".format(chunk_id, output_dir),
        file=sys.stdout,
    )

    return {
        "chunk_id": chunk_id,
        "output_dir": output_dir,
        "chunk_contributions_csv_path": csv_path,
        "chunk_metadata_json_path": json_path,
        "chunk_summary_md_path": md_path,
        "metadata": metadata,
    }


# ── Merge support (offline; no GDELT contact) ─────────────────────────────────

def load_chunk_contributions(chunk_dir: str) -> Dict[Tuple[str, int], int]:
    """Read `chunk_contributions.csv` from a chunk output dir into a
    `(SQLDATE_iso, offset_int) -> count` dict. Raises ChunkManifestError
    on missing file."""
    path = os.path.join(chunk_dir, "chunk_contributions.csv")
    if not os.path.isfile(path):
        raise ChunkManifestError(
            "chunk_contributions.csv missing in {}".format(chunk_dir)
        )
    out: Dict[Tuple[str, int], int] = {}
    col_offset_map = {
        "rows_from_offset_0": 0,
        "rows_from_offset_minus_1": -1,
        "rows_from_offset_minus_7": -7,
        "rows_from_offset_minus_30": -30,
        "rows_from_offset_minus_365": -365,
        "rows_from_offset_minus_3650": -3650,
        "rows_from_offset_plus_1": 1,
    }
    with open(path, "r", encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split(",")
        for ln in fh:
            row = ln.rstrip("\n").split(",")
            if len(row) != len(header):
                continue
            iso = row[0]
            for col_name, offset in col_offset_map.items():
                if col_name not in header:
                    continue
                idx = header.index(col_name)
                try:
                    cnt = int(row[idx])
                except ValueError:
                    continue
                if cnt > 0:
                    out[(iso, offset)] = cnt
    return out


def load_chunk_metadata(chunk_dir: str) -> Dict[str, Any]:
    """Read `chunk_metadata.json` from a chunk output dir.
    Raises ChunkManifestError on missing file."""
    path = os.path.join(chunk_dir, "chunk_metadata.json")
    if not os.path.isfile(path):
        raise ChunkManifestError(
            "chunk_metadata.json missing in {}".format(chunk_dir)
        )
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def merge_chunks(
    chunk_dirs: Dict[str, str],
    repo_root: str,
) -> Dict[str, Any]:
    """Merge per-chunk derived artifacts into the final canonical
    aggregation. Reads the recognized-list capture from `repo_root` to
    verify chunk-manifest digests against expected.

    Returns a dict with:
      - `daily_count_rows`: list of per-civil-date row dicts
        (one per civil day in `[2013-04-01, 2022-12-31]`), with
        merge-time coverage flags recomputed from the union `daily_set`
        (preserving `c10ae74` Decision 1A's 7-entry closed flag domain).
      - `aggregate_metrics`: totals (in-window, out-of-window, etc.).
      - `per_chunk_summary`: per-chunk row counts.

    Does NOT write canonical artifacts; the caller (merge-mode CLI
    handler) writes them. Does NOT contact GDELT. Does NOT issue any
    fetch.

    Halts (raises ChunkManifestError) on:
      - any required chunk missing;
      - manifest-digest mismatch for any chunk;
      - cross-chunk URL duplicate;
      - union of chunks != recognized-list-derived full fetch set.
    """
    # Verify chunk set
    expected = set(CHUNK_IDS)
    actual = set(chunk_dirs.keys())
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise ChunkManifestError(
            "merge halt: missing chunks: {}".format(missing)
        )
    if extra:
        raise ChunkManifestError(
            "merge halt: unexpected chunk ids: {}".format(extra)
        )

    # Load recognized list (offline; no GDELT contact)
    capture_data, _, _ = _load_recognized_list(repo_root)
    units = capture_data["recognized_in_window_units"]
    reconciliation = build_reconciliation_report(units)
    assert_reconciliation_consistent(reconciliation)
    fetch_set_full = reconciliation["fetch_set"]
    daily_set: Set[str] = set(fetch_set_full)
    gaps_set: Set[str] = set(KNOWN_SUBSTRATE_GAPS)

    expected_manifests = build_all_chunk_manifests(fetch_set_full)
    assert_chunk_manifests_partition(expected_manifests, fetch_set_full)

    # Verify per-chunk manifest digests + cross-chunk URL uniqueness
    seen_urls: Dict[str, str] = {}
    per_chunk_summary: Dict[str, Dict[str, Any]] = {}
    for cid in CHUNK_IDS:
        md = load_chunk_metadata(chunk_dirs[cid])
        expected_digest = chunk_manifest_digest(expected_manifests[cid])
        actual_digest = md.get("chunk_manifest_digest")
        if actual_digest != expected_digest:
            raise ChunkManifestError(
                "merge halt: chunk {!r} digest mismatch "
                "(expected {}, got {})".format(
                    cid, expected_digest, actual_digest,
                )
            )
        for iso in expected_manifests[cid]:
            if iso in seen_urls:
                raise ChunkManifestError(
                    "merge halt: duplicate URL {!r} in chunks "
                    "{!r} and {!r}".format(iso, seen_urls[iso], cid)
                )
            seen_urls[iso] = cid
        per_chunk_summary[cid] = {
            "expected_file_count":
                md.get("expected_file_count"),
            "actual_completed_file_count":
                md.get("actual_completed_file_count"),
            "chunk_manifest_digest": actual_digest,
        }

    # Union-equals-full check (redundant given the digest+partition
    # checks above, but explicit per chunk-design memo §9.1.5).
    union = set(seen_urls.keys())
    if union != daily_set:
        raise ChunkManifestError(
            "merge halt: union of chunks ({}) != recognized-list-derived "
            "full daily fetch set ({})".format(len(union), len(daily_set))
        )

    # Sum SQLDATE contributions across chunks
    merged: Dict[str, Dict[int, int]] = {}
    for cid in CHUNK_IDS:
        contribs = load_chunk_contributions(chunk_dirs[cid])
        for (iso, offset), cnt in contribs.items():
            cell = merged.setdefault(iso, {})
            cell[offset] = cell.get(offset, 0) + cnt

    # Build per-civil-date rows (restricted to [START_DATE, END_DATE])
    rows: List[Dict[str, Any]] = []
    for d in civil_date_domain():
        iso = d.isoformat()
        cells = merged.get(iso, {})
        cov = coverage_for_date(d, daily_set, gaps_set)
        row = {
            "civil_date": iso,
            "total_row_count": sum(cells.values()),
            "rows_from_offset_0": cells.get(0, 0),
            "rows_from_offset_minus_1": cells.get(-1, 0),
            "rows_from_offset_minus_7": cells.get(-7, 0),
            "rows_from_offset_minus_30": cells.get(-30, 0),
            "rows_from_offset_minus_365": cells.get(-365, 0),
            "rows_from_offset_minus_3650": cells.get(-3650, 0),
            "rows_from_offset_plus_1": cells.get(1, 0),
            "t0_file_status": t0_file_status(d, daily_set, gaps_set),
            "expected_contributing_files_count":
                cov["expected_contributing_files_count"],
            "available_contributing_files_count":
                cov["available_contributing_files_count"],
            "coverage_quality_flag": cov["coverage_quality_flag"],
            "coverage_completeness": cov["coverage_completeness"],
        }
        if not is_valid_coverage_flag(row["coverage_quality_flag"]):
            raise FullBuildBoundaryBreach(
                "merge halt: invalid coverage_quality_flag {!r} "
                "for date {}".format(row["coverage_quality_flag"], iso)
            )
        rows.append(row)

    # Aggregate metrics
    total_in_window = sum(r["total_row_count"] for r in rows)

    return {
        "daily_count_rows": rows,
        "aggregate_metrics": {
            "total_in_window_rows": total_in_window,
            "civil_days_in_output_domain": len(rows),
            "chunks_merged": list(CHUNK_IDS),
        },
        "per_chunk_summary": per_chunk_summary,
    }


# ── CLI ─────────────────────────────────────────────────────────────────────

def _make_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description=(
            "Lane 2 GDELT 1.0 full daily-count build runner "
            "(design memo `7780a97`; chunk-design memo `5962c20`). "
            "Refuses to run live unless all three guards are satisfied. "
            "Supports yearly fetch-file-date chunk execution and "
            "offline merge."
        ),
    )
    ap.add_argument(
        "--authorize-full-build-run",
        action="store_true",
        help=(
            "CLI guard 2/3. Must be passed alongside the module-constant "
            "guard (FULL_BUILD_AUTHORIZED=True) AND env "
            "LANE2_FULL_BUILD_AUTHORIZED=1 to execute any live fetch "
            "(un-chunked full build OR a single chunk)."
        ),
    )
    ap.add_argument(
        "--repo-root",
        default=os.getcwd(),
        help=(
            "Repository root containing the §10 recognized-list capture "
            "and the results/ output parent. Defaults to CWD."
        ),
    )
    ap.add_argument(
        "--chunk-id",
        default=None,
        choices=list(CHUNK_IDS) + [None],
        help=(
            "If set, executes only the named yearly fetch-file-date "
            "chunk (under the same three-guard discipline). One of: {}. "
            "Mutually exclusive with --merge.".format(", ".join(CHUNK_IDS))
        ),
    )
    ap.add_argument(
        "--list-chunks",
        action="store_true",
        help=(
            "Print canonical chunk IDs and expected file counts and "
            "exit. Offline; no guard / network required."
        ),
    )
    ap.add_argument(
        "--merge",
        action="store_true",
        help=(
            "Run the offline merge step. Requires --merge-input flags "
            "specifying chunk output directories. No GDELT contact; no "
            "guard flip required. Mutually exclusive with --chunk-id."
        ),
    )
    ap.add_argument(
        "--merge-input",
        action="append",
        default=[],
        metavar="CHUNK_ID=DIR",
        help=(
            "Repeatable. One per chunk; binds a chunk_id to its output "
            "directory for merge."
        ),
    )
    return ap


def _parse_merge_inputs(merge_inputs: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for spec in merge_inputs:
        if "=" not in spec:
            raise ChunkManifestError(
                "invalid --merge-input {!r}; expected CHUNK_ID=DIR".format(spec)
            )
        cid, _, dir_ = spec.partition("=")
        cid = cid.strip()
        dir_ = dir_.strip()
        validate_chunk_id(cid)
        if cid in out:
            raise ChunkManifestError(
                "duplicate --merge-input for chunk_id {!r}".format(cid)
            )
        out[cid] = dir_
    return out


def main(argv: Optional[List[str]] = None) -> int:
    args = _make_argparser().parse_args(argv)
    if args.list_chunks:
        for cid in CHUNK_IDS:
            print("{}\t{}".format(cid, EXPECTED_CHUNK_COUNTS[cid]))
        return 0
    if args.chunk_id and args.merge:
        print(
            "HALT: --chunk-id and --merge are mutually exclusive.",
            file=sys.stderr,
        )
        return 1
    try:
        if args.merge:
            chunk_dirs = _parse_merge_inputs(args.merge_input)
            merge_chunks(chunk_dirs, repo_root=args.repo_root)
            print(
                "Merge complete (in-memory only; CLI does not "
                "write canonical artifacts in this implementation turn).",
                file=sys.stdout,
            )
            return 0
        if args.chunk_id:
            run_chunk_build(
                args.chunk_id,
                repo_root=args.repo_root,
                cli_flag=args.authorize_full_build_run,
            )
            return 0
        run_full_daily_count_build(
            repo_root=args.repo_root,
            cli_flag=args.authorize_full_build_run,
        )
    except SystemExit:
        raise
    except (FullBuildBoundaryBreach, FetchFailure,
            RecognizedListSchemaError, ReconciliationContradiction,
            ChunkManifestError) as e:
        print("HALT: {}: {}".format(type(e).__name__, e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
