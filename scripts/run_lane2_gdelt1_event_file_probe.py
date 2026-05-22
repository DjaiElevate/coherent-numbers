"""Standalone Lane 2 GDELT 1.0 event-file probe (5 + 1 deterministic sentinel).

THIS PROBE DOES NOT RUN BY DEFAULT AND PERFORMS NO DATA ACCESS UNLESS THREE
INDEPENDENT GUARDS ARE ALL SATISFIED:

  1. module constant EVENT_FILE_PROBE_AUTHORIZED is set True (ships False);
  2. CLI flag --authorize-event-file-probe-run is passed;
  3. env var LANE2_EVENT_FILE_PROBE_AUTHORIZED == "1".

If any guard is missing, the probe prints a refusal and exits BEFORE any
network call, directory creation, or artifact write.

This script is **standalone**. It does NOT import the count-feasibility
runner, the count-feasibility source module, or Gate 4D's index-listing
opener. It builds its own redirect-disabled opener (mirroring the Gate 4D
pattern with script-local names) scoped only to event-file URLs.

Authorization basis: design note
`docs/lane2_gdelt1_event_file_probe_design_note_v0.1.md` (commit `e55e09a`).
The design note authorizes neither source addition nor execution; the
script-implementation authorization is a separate explicit step. The probe
script ships inert; execution requires its own separate authorization step
that flips the guard.

Scope: count-only daily-event-file feasibility probe over the §10
recognized universe. No market data, no Step 2, no asset/return logic,
no category/theme/actor filtering, no spike thresholds.
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
# (mirrors the count-feasibility runner's `COUNT_FEASIBILITY_AUTHORIZED` /
# `fe74255 → 9e329c2` enable-then-inert-restore pattern). A run-enablement
# commit must be followed by a separate inert-restore commit; this constant
# is restored to False after the single authorized probe run.
EVENT_FILE_PROBE_AUTHORIZED = True


# ── Substrate-pinned constants (no CLI / env / config override) ──────────────
#
# RECOGNIZED_LIST_PATH is hardcoded by design. Lane 2's v0.3 posture memo
# (`0ddbd51`) selects the §10 capture as the canonical recognized universe
# anchor; the design note (`e55e09a`) §4 pins this exact path. Exposing
# this as a CLI argument / environment variable / config field would break
# the substrate-pin contract.
RECOGNIZED_LIST_PATH = (
    "results/lane2_gdelt1_turn_b_recognized_list_capture/"
    "20260521T124853Z/recognized_list.json"
)

# Event-file URL pattern: `<base><YYYYMMDD>.export.CSV.zip`.
# Index-listing URL `index.html` is OUT OF SCOPE for this probe and is
# never constructed; this is enforced by `_date_to_url`.
EVENT_FILE_BASE_URL = "http://data.gdeltproject.org/events/"

# Pre-2023 protocol seal. Any 2023+ date is hard-refused at URL-construction
# and again at parse-time. This mirrors the count-feasibility module's
# `SEAL_START` semantics but is enforced locally here so the probe is
# self-contained.
SEAL_START = date(2023, 1, 1)

DEFAULT_TIMEOUT = 30.0

# GDELT 1.0 `.export.CSV` schema: SQLDATE is column index 1 (0-based).
SQLDATE_COLUMN_INDEX = 1


# ── Deterministic sample (design note §3) ────────────────────────────────────
#
# Four structurally pinned positive dates with no fallback. Mid-window date
# has a median fallback rule because the planned daily partition has an
# even-length sequence and there are two equally valid medians.
PINNED_POSITIVE_DATES: Tuple[date, ...] = (
    date(2013, 4, 1),    # first daily-regime unit
    date(2014, 1, 22),   # day before the known 2014-01-23/24/25 substrate gap
    date(2014, 1, 26),   # day after the known substrate gap
    date(2022, 12, 31),  # final in-window daily unit
)
MID_WINDOW_PRIMARY = date(2018, 2, 14)    # lower median
MID_WINDOW_FALLBACK = date(2018, 2, 15)   # upper median
NEGATIVE_CONTROL_DATE = date(2014, 1, 23)  # known substrate gap


# ── Output allow-list (design note §9) ───────────────────────────────────────
#
# Exact-match basenames + a strict regex for compressed positive-sample
# payloads. Extracted CSV files are NOT allowed; only the raw compressed
# response bytes are written.
ALLOWED_PROBE_OUTPUTS: Tuple[str, ...] = (
    "probe_metadata.json",
    "probe_summary.md",
)
_PAYLOAD_BASENAME_RE = re.compile(r"^payload_(\d{8})\.zip$")


_REFUSAL = (
    "Lane 2 event-file probe is NOT authorized. Requires "
    "EVENT_FILE_PROBE_AUTHORIZED=True AND "
    "--authorize-event-file-probe-run AND env "
    "LANE2_EVENT_FILE_PROBE_AUTHORIZED=1. No network, no fetch, "
    "no directory created."
)


# ── Exception classes ────────────────────────────────────────────────────────

class RedirectBlocked(RuntimeError):
    """Raised by the probe's redirect-disabled opener on any 3xx response."""


class ProbeBoundaryBreach(RuntimeError):
    """Raised when a hard boundary (2023+ date, disallowed output, etc.) is hit."""


class SampleSelectionError(RuntimeError):
    """Raised when sample preflight fails (pinned date absent / negative
    control present / both mid candidates absent)."""


# ── Local redirect-disabled opener (probe-scoped) ────────────────────────────
#
# Mirrors Gate 4D's `_NoFollowRedirectHandler` / `build_redirect_disabled_opener`
# pattern with script-local names. Does NOT reuse Gate 4D's opener, which
# is scoped to `DEFAULT_GDELT1_INDEX_URL` only — a different scope from
# event-file URLs.

class _ProbeNoFollowRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Redirect handler whose 3xx hooks raise rather than follow.

    Overriding every 30x http_error_NNN hook makes the no-follow property
    structural — every redirect status is intercepted — not a runtime
    convention a caller could forget."""

    def _block(self, req, fp, code, msg, headers):
        raise RedirectBlocked(
            "probe opener blocked redirect (status {!r}); no follow, "
            "no fallback".format(code)
        )

    http_error_301 = _block
    http_error_302 = _block
    http_error_303 = _block
    http_error_307 = _block
    http_error_308 = _block


def _build_probe_redirect_disabled_opener(
    timeout: float = DEFAULT_TIMEOUT,
) -> Callable:
    """Build a callable opener with redirect-following disabled by
    construction. Used only for the 6 authorized per-file URLs.

    The factory call fires no request; a single request occurs only when
    the returned callable is invoked. Guards are not flipped.
    """
    _opener = urllib.request.build_opener(_ProbeNoFollowRedirectHandler())
    _default_timeout = timeout

    def _probe_opener(url, timeout=_default_timeout):
        # Exactly one request per invocation. No retry, no second GET, no
        # fallback. Callers (`_probe_one_file`) consume `.read()` once and
        # never re-invoke this opener for the same URL.
        return _opener.open(url, timeout=timeout)

    return _probe_opener


# ── Three-guard gate ─────────────────────────────────────────────────────────

def _guards_ok(cli_flag: bool) -> bool:
    return (
        EVENT_FILE_PROBE_AUTHORIZED
        and cli_flag
        and os.environ.get("LANE2_EVENT_FILE_PROBE_AUTHORIZED") == "1"
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
        raise ProbeBoundaryBreach(
            "recognized_list.json missing 'recognized_in_window_units' "
            "list at {}".format(path)
        )
    return units


# ── Sample selection (design note §3 + §4) ───────────────────────────────────

def select_sample(recognized_units: List[str]) -> Tuple[List[date], date]:
    """Returns `(positive_dates_sorted, negative_control_date)` after
    verifying all preconditions.

    Halts (raises `SampleSelectionError`) on:
    - any of the four pinned positive dates absent from `recognized_units`;
    - both mid-window candidates absent;
    - negative-control date present in `recognized_units`.

    The mid-window date uses lower-median primary (`MID_WINDOW_PRIMARY`)
    with upper-median fallback (`MID_WINDOW_FALLBACK`). The four pinned
    dates have NO fallback because they are boundary-defined.
    """
    recognized = set(recognized_units)

    missing_pinned = [
        d for d in PINNED_POSITIVE_DATES if d.isoformat() not in recognized
    ]
    if missing_pinned:
        raise SampleSelectionError(
            "pinned positive date(s) absent from recognized universe: "
            "{}".format([d.isoformat() for d in missing_pinned])
        )

    if MID_WINDOW_PRIMARY.isoformat() in recognized:
        mid = MID_WINDOW_PRIMARY
    elif MID_WINDOW_FALLBACK.isoformat() in recognized:
        mid = MID_WINDOW_FALLBACK
    else:
        raise SampleSelectionError(
            "neither mid-window primary {} nor fallback {} present in "
            "recognized universe".format(
                MID_WINDOW_PRIMARY.isoformat(),
                MID_WINDOW_FALLBACK.isoformat(),
            )
        )

    if NEGATIVE_CONTROL_DATE.isoformat() in recognized:
        raise SampleSelectionError(
            "negative-control date {} unexpectedly present in recognized "
            "universe; gap model violated before fetch".format(
                NEGATIVE_CONTROL_DATE.isoformat()
            )
        )

    positive_dates = sorted(list(PINNED_POSITIVE_DATES) + [mid])
    return positive_dates, NEGATIVE_CONTROL_DATE


# ── URL construction ─────────────────────────────────────────────────────────

def _date_to_url(d: date) -> str:
    """Construct exactly one event-file URL for a pre-2023 date.

    Refuses 2023+ at construction time. Does not construct
    `events/index.html`, the base `events/` URL alone, or any other
    listing/directory URL. Used by `construct_probe_urls` only."""
    if d >= SEAL_START:
        raise ProbeBoundaryBreach(
            "refusing to construct URL for 2023+ date: {}".format(
                d.isoformat()
            )
        )
    yyyymmdd = "{:04d}{:02d}{:02d}".format(d.year, d.month, d.day)
    return "{}{}.export.CSV.zip".format(EVENT_FILE_BASE_URL, yyyymmdd)


def construct_probe_urls(
    positive_dates: List[date],
    negative_control: date,
) -> Dict[str, str]:
    """Returns `{date.isoformat(): url}` for all 6 authorized GETs.

    Order: positive dates (in input order), then the negative control.
    """
    urls: Dict[str, str] = {}
    for d in positive_dates:
        urls[d.isoformat()] = _date_to_url(d)
    urls[negative_control.isoformat()] = _date_to_url(negative_control)
    return urls


# ── Output allow-list ────────────────────────────────────────────────────────

def _is_allowed_probe_output(
    basename: str, positive_yyyymmdd: List[str],
) -> bool:
    """Return True iff `basename` matches the probe output allow-list.

    Exact-match: `probe_metadata.json`, `probe_summary.md`.
    Pattern-match: `payload_<YYYYMMDD>.zip` where `<YYYYMMDD>` is one of
    the positive-sample dates (negative-control payloads are NOT allowed
    on disk).
    """
    if basename in ALLOWED_PROBE_OUTPUTS:
        return True
    m = _PAYLOAD_BASENAME_RE.match(basename)
    if m is None:
        return False
    return m.group(1) in set(positive_yyyymmdd)


def _checked_probe_path(
    output_dir: str, basename: str, positive_yyyymmdd: List[str],
) -> str:
    """Pre-write gate: assert basename is allow-listed BEFORE any write."""
    if not _is_allowed_probe_output(basename, positive_yyyymmdd):
        raise ProbeBoundaryBreach(
            "non-allow-listed probe output: {!r}".format(basename)
        )
    return os.path.join(output_dir, basename)


def _assert_probe_outputs_allowed(
    output_dir: str, positive_yyyymmdd: List[str],
) -> None:
    """Post-hoc tripwire: only allow-listed files may exist in the dir."""
    for name in os.listdir(output_dir):
        if os.path.isdir(os.path.join(output_dir, name)):
            continue
        if not _is_allowed_probe_output(name, positive_yyyymmdd):
            raise ProbeBoundaryBreach(
                "non-allow-listed file in probe output dir: {!r}".format(
                    name
                )
            )


# ── Parser / row-count contract (headerless positional, design note §6) ──────

def parse_event_file_payload(
    payload_bytes: bytes,
    nominal_date: date,
    sqldate_col: int = SQLDATE_COLUMN_INDEX,
) -> Dict[str, object]:
    """Decompress + row-count + detect header-anomaly + validate dates.

    GDELT 1.0 `.export.CSV` files are treated as **headerless positional
    files**. The function counts ALL non-empty data rows; it never
    silently subtracts a header. If the first row's SQLDATE column is not
    parseable as a date, that is flagged `header_anomaly_detected=True`
    and the row is still included in the total `row_count` so the contract
    is observable, not silently absorbed.

    A 2023+ SQLDATE row raises `ProbeBoundaryBreach`.
    """
    if nominal_date >= SEAL_START:
        raise ProbeBoundaryBreach(
            "refusing to parse payload nominally dated 2023+: {}".format(
                nominal_date.isoformat()
            )
        )
    with zipfile.ZipFile(io.BytesIO(payload_bytes)) as zf:
        names = zf.namelist()
        if not names:
            return {
                "row_count": 0,
                "header_anomaly_detected": False,
                "rows_matching_nominal_date": 0,
                "rows_mismatching_nominal_date": 0,
                "rows_unparseable_sqldate": 0,
                "date_validation_pass": False,
            }
        with zf.open(names[0]) as fh:
            text = fh.read().decode("utf-8", "replace")

    lines = [ln for ln in text.splitlines() if ln.strip()]
    row_count = len(lines)
    matching = 0
    mismatching = 0
    unparseable = 0
    header_anomaly = False
    for idx, ln in enumerate(lines):
        parts = ln.split("\t")
        if len(parts) <= sqldate_col:
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
            raise ProbeBoundaryBreach(
                "2023+ SQLDATE row in payload nominally dated {}: {}".format(
                    nominal_date.isoformat(), d.isoformat()
                )
            )
        if d == nominal_date:
            matching += 1
        else:
            mismatching += 1

    date_validation_pass = (
        matching > 0
        and mismatching == 0
        and unparseable == 0
    )
    return {
        "row_count": row_count,
        "header_anomaly_detected": header_anomaly,
        "rows_matching_nominal_date": matching,
        "rows_mismatching_nominal_date": mismatching,
        "rows_unparseable_sqldate": unparseable,
        "date_validation_pass": date_validation_pass,
    }


# ── Per-file fetch (exactly one GET attempt; no retry) ───────────────────────

def _probe_one_file(
    date_iso: str,
    url: str,
    opener: Callable,
    timeout: float,
    is_positive: bool,
) -> Tuple[Dict[str, object], Optional[bytes]]:
    """Make exactly one GET attempt. No retries. Returns
    `(result_dict, body_bytes_or_None)`. Body is None unless the response
    is HTTP 200; non-200 responses don't yield a usable body for parsing."""
    result: Dict[str, object] = {
        "date": date_iso,
        "url": url,
        "is_positive": bool(is_positive),
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
        # Non-2xx response (3xx is intercepted by RedirectBlocked above).
        result["status"] = int(getattr(exc, "code", 0)) or None
        result["fetch_outcome"] = "HTTP_NON_200"
        result["exception_class"] = "HTTPError"
        result["exception_str"] = str(exc)
        headers = getattr(exc, "headers", None)
        if headers is not None and hasattr(headers, "get"):
            result["location"] = headers.get("Location")
        return result, None
    except Exception as exc:  # noqa: BLE001
        # URLError, socket.timeout, OSError, etc. — connection-level.
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


# ── Verdict aggregation (design note §8) ─────────────────────────────────────

def _compute_verdict(
    pos_results: List[Dict[str, object]],
    neg_result: Dict[str, object],
) -> str:
    """Compute one of the design note §8 verdict tokens from per-file
    results. `BOUNDARY-FAILURE` and `FIREWALL-BREACH` are not produced
    here: BOUNDARY-FAILURE would have raised earlier in the pipeline, and
    FIREWALL-BREACH is structurally impossible because no market-data
    surface exists in the probe."""

    # Positive-side checks first.
    if any(
        r.get("fetch_outcome") in (
            "REDIRECT_BLOCKED", "HTTP_NON_200", "CONNECTION_ERROR",
        )
        for r in pos_results
    ):
        return "INFEASIBLE-RETRIEVAL"

    if any(
        r.get("parse") is None or "error" in (r.get("parse") or {})
        for r in pos_results
    ):
        return "INFEASIBLE-PARSER"

    if any(
        (r["parse"].get("rows_mismatching_nominal_date", 0) or 0) > 0
        for r in pos_results
    ):
        return "ROW-DATE-MISMATCH"

    if any(
        (r["parse"].get("rows_unparseable_sqldate", 0) or 0) > 0
        and not r["parse"].get("header_anomaly_detected")
        for r in pos_results
    ):
        return "INFEASIBLE-PARSER"

    # Negative-control classification.
    nc_outcome = neg_result.get("fetch_outcome")
    nc_status = neg_result.get("status")
    if nc_outcome == "200_OK":
        return "GAP-MODEL-FAILED"
    if nc_outcome == "REDIRECT_BLOCKED":
        return "GAP-MODEL-AMBIGUOUS"
    if nc_outcome == "CONNECTION_ERROR":
        return "GAP-MODEL-AMBIGUOUS"
    if nc_outcome == "HTTP_NON_200" and nc_status in (403, 404, 410):
        return "FEASIBLE"
    return "GAP-MODEL-AMBIGUOUS"


def _build_summary_md(metadata: Dict[str, object]) -> str:
    lines: List[str] = []
    lines.append("# Lane 2 GDELT 1.0 event-file probe — summary")
    lines.append("")
    lines.append("Verdict: **{}**".format(metadata.get("verdict")))
    lines.append("")
    lines.append("Recognized-list anchor: `{}`".format(
        metadata.get("recognized_list_path")
    ))
    lines.append("Design note: `docs/lane2_gdelt1_event_file_probe_design_note_v0.1.md`")
    lines.append("")
    lines.append("Positive sample dates: {}".format(
        ", ".join(metadata.get("positive_sample_dates", []) or [])
    ))
    lines.append("Negative control: {}".format(
        metadata.get("negative_control_date")
    ))
    lines.append("")
    lines.append("Per-date results:")
    for r in metadata.get("results", []) or []:
        lines.append(
            "- {} ({}): status={} outcome={}".format(
                r.get("date"),
                "positive" if r.get("is_positive") else "negative-control",
                r.get("status"),
                r.get("fetch_outcome"),
            )
        )
    lines.append("")
    lines.append(
        "No market data; no Step 2; no signal-threshold tuning; no "
        "category / theme / actor / geography filtering."
    )
    lines.append("")
    return "\n".join(lines)


# ── Output directory ─────────────────────────────────────────────────────────

def _fresh_output_dir(repo_root: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = os.path.join(
        repo_root, "results", "lane2_gdelt1_event_file_probe", ts,
    )
    os.makedirs(out, exist_ok=False)
    return out


# ── Main probe entry ─────────────────────────────────────────────────────────

def run_event_file_probe(
    repo_root: str,
    cli_flag: bool = True,
    opener: Optional[Callable] = None,
    timeout: float = DEFAULT_TIMEOUT,
    output_dir: Optional[str] = None,
) -> str:
    """Execute the 5 + 1 sentinel probe. Returns the output directory.

    Refuses (`SystemExit(_REFUSAL)`) unless all three guards pass: module
    constant, CLI flag, env var. The shipped module constant is False, so
    the default behavior is refusal.

    `opener` is injectable for tests (no real network). `output_dir` is
    likewise injectable for tests; production runs use a fresh timestamped
    directory under `results/lane2_gdelt1_event_file_probe/`.
    """
    if not _guards_ok(cli_flag):
        raise SystemExit(_REFUSAL)

    units = _load_recognized_units(repo_root)
    positive_dates, neg_ctrl = select_sample(units)
    urls = construct_probe_urls(positive_dates, neg_ctrl)
    positive_yyyymmdd = [
        "{:04d}{:02d}{:02d}".format(d.year, d.month, d.day)
        for d in positive_dates
    ]

    if output_dir is None:
        output_dir = _fresh_output_dir(repo_root)
    else:
        os.makedirs(output_dir, exist_ok=False)

    use_opener = (
        opener
        if opener is not None
        else _build_probe_redirect_disabled_opener(timeout=timeout)
    )

    results: List[Dict[str, object]] = []
    for date_iso, url in urls.items():
        is_positive = date_iso != neg_ctrl.isoformat()
        result, body = _probe_one_file(
            date_iso=date_iso,
            url=url,
            opener=use_opener,
            timeout=timeout,
            is_positive=is_positive,
        )
        if is_positive and result.get("fetch_outcome") == "200_OK" \
                and body is not None:
            d = date.fromisoformat(date_iso)
            yyyymmdd = "{:04d}{:02d}{:02d}".format(d.year, d.month, d.day)
            payload_path = _checked_probe_path(
                output_dir,
                "payload_{}.zip".format(yyyymmdd),
                positive_yyyymmdd,
            )
            with open(payload_path, "wb") as fh:
                fh.write(body)
            try:
                result["parse"] = parse_event_file_payload(
                    body,
                    nominal_date=d,
                    sqldate_col=SQLDATE_COLUMN_INDEX,
                )
            except ProbeBoundaryBreach as exc:
                # Boundary breach during parse is reported in metadata,
                # not silently swallowed.
                result["parse"] = {"error": str(exc)}
        results.append(result)

    pos_results = [r for r in results if r["is_positive"]]
    neg_result = next(r for r in results if not r["is_positive"])
    verdict = _compute_verdict(pos_results, neg_result)

    metadata: Dict[str, object] = {
        "schema_version": "v0.1",
        "design_note_anchor":
            "docs/lane2_gdelt1_event_file_probe_design_note_v0.1.md",
        "recognized_list_path": RECOGNIZED_LIST_PATH,
        "event_file_base_url": EVENT_FILE_BASE_URL,
        "positive_sample_dates": [d.isoformat() for d in positive_dates],
        "negative_control_date": neg_ctrl.isoformat(),
        "urls": urls,
        "results": results,
        "verdict": verdict,
        "no_market_data": True,
        "no_step_2": True,
        "no_asset_or_return_logic": True,
        "no_category_theme_actor_filtering": True,
        "no_spike_threshold_tuning": True,
    }

    meta_path = _checked_probe_path(
        output_dir, "probe_metadata.json", positive_yyyymmdd,
    )
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(metadata, fh, indent=2, sort_keys=True)

    summary_path = _checked_probe_path(
        output_dir, "probe_summary.md", positive_yyyymmdd,
    )
    with open(summary_path, "w", encoding="utf-8") as fh:
        fh.write(_build_summary_md(metadata))

    _assert_probe_outputs_allowed(output_dir, positive_yyyymmdd)
    return output_dir


def main() -> None:
    p = argparse.ArgumentParser(
        description="Lane 2 GDELT 1.0 event-file probe (5 + 1 sentinel)"
    )
    p.add_argument(
        "--authorize-event-file-probe-run", action="store_true",
    )
    p.add_argument("--repo-root", default=os.getcwd())
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    args = p.parse_args()
    if not _guards_ok(args.authorize_event_file_probe_run):
        print(_REFUSAL)
        return
    out = run_event_file_probe(
        args.repo_root,
        cli_flag=args.authorize_event_file_probe_run,
        timeout=args.timeout,
    )
    print("Event-file probe outputs written under: {}".format(out))


if __name__ == "__main__":
    main()
