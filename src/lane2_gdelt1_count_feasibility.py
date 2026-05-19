"""Lane 2 — GDELT 1.0 count-only data-source feasibility (implementation draft).

Governing artifacts (committed):
  - Step 1 framework            357fba585965818da853a6ba560a7ea2b3213c0b
  - Step 2 readiness memo       af64ee2f5e12d867bc7b70a1afe7d3c41a7c03fa
  - count-only protocol         147c0d40568636ba0cf24ca00cc39c330e77ea03  (BINDING)
  - source-selection + auth     8fef80db0e103d2c22e36d589fe041abd1fb4c78

COUNT-ONLY. This module computes only source availability, daily
attention/event-volume counts, missingness, spike counts, clustering/overlap
counts, by-year summaries, and feasibility-class scaffolding. It does NOT and
must NOT compute returns, CAR, abnormal returns, volatility/VIX response, any
market outcome, model fits, M0/M1/M2/M3 comparisons, p-values, feature
importance, attention-response, or state-response relationships. It never
touches 2023+. GDELT 1.0 selection here is for count-only feasibility, NOT a
Step 2 source lock.

No network/data access happens at import or in unit tests. Real retrieval is
deferred to a future, separately authorized run via the (inert) runner.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Callable, Dict, List, Optional, Sequence, Tuple

# ── Governance constants ──────────────────────────────────────────────────────

GOVERNING_PROTOCOL_COMMIT = "147c0d40568636ba0cf24ca00cc39c330e77ea03"
AUTHORIZATION_COMMIT = "8fef80db0e103d2c22e36d589fe041abd1fb4c78"
RUN_AUTHORIZATION_COMMIT = "60ec1521106e6a980f6450cb21a1ef510b4c37d5"
RUN_AUTHORIZATION_MEMO_PATH = (
    "docs/lane2_gdelt1_count_feasibility_run_authorization_v0.1.md"
)
SELECTED_SOURCE = "GDELT 1.0 Event database"

# Run-authorization memo (60ec152) pinned parameters. These are the ONLY
# values the one authorized count-only run may use; they are not hypothesis
# choices and not market results.
PINNED_COVERAGE_START = date(2005, 1, 1)
PINNED_COVERAGE_END = date(2022, 12, 31)
PINNED_MIN_EVENT_FLOOR = 100
PINNED_NORMALIZATION_STATUS = "not_used"
PINNED_OPTION_C_THRESHOLD = None        # Option C disabled for this run
PINNED_OPTION_C_ENABLED = False
PINNED_CLUSTERING_DAYS = (5, 10, 20)
PINNED_PRIMARY_CLUSTER_DAYS = 10        # primary feasibility floor window

# Controlled vocabulary for the archive_layout_status metadata field
# (run-authorization memo §17 requires this field in run metadata).
ARCHIVE_LAYOUT_STATUS_VALUES = (
    "ok",
    "mismatch",
    "missing",
    "unexpected",
    "f4_layout_issue",
    "not_checked",
    # Layout verification was entered but aborted on a protocol breach
    # (e.g. a 2023+ key surfaced during the layout check) -> F5. Distinct
    # from "not_checked" (breach occurred before layout was attempted).
    "breach_during_check",
)

# Hard seal. Nothing on/after this date may be planned, parsed, counted, or
# referenced. 2023+ is sealed.
SEAL_START = date(2023, 1, 1)

# Documentation-level GDELT 1.0 file/dating regime (to be verified at freeze;
# overridable — not asserted as a data-derived fact):
#   - through 2013-03-31: monthly/yearly files, by EVENT date
#   - from   2013-04-01: daily files, by date FOUND IN NEWS MEDIA
REGIME_DAILY_START = date(2013, 4, 1)
# Within the pre-boundary regime, documentation-level sub-granularity default:
#   - years <= 2005 : yearly files
#   - 2006-01 .. 2013-03 : monthly files
PRE_REGIME_YEARLY_THROUGH_YEAR = 2005

GDELT1_SQLDATE_COL_DEFAULT = 1  # GLOBALEVENTID=0, SQLDATE=1 (YYYYMMDD)


class ProtocolBreach(RuntimeError):
    """Generic count-only protocol breach (maps to feasibility class F5)."""


class Protocol2023PlusBreach(ProtocolBreach):
    """A 2023+ file/date/row was planned, parsed, or counted."""


def assert_no_2023plus(dates: Sequence[date], where: str) -> None:
    for d in dates:
        if d >= SEAL_START:
            raise Protocol2023PlusBreach(
                "2023+ encountered in {}: {}".format(where, d)
            )


# ── 1. Source/file planning (regime-aware; pre-2023 by construction) ──────────

@dataclass(frozen=True)
class PlannedUnit:
    """One planned GDELT 1.0 retrieval unit. No file is fetched here."""

    key: str          # e.g. "1985", "2009-07", "2015-03-12"
    regime: str       # "yearly" | "monthly" | "daily"
    rep_date: date    # representative date used for the 2023+ guard


def plan_gdelt1_files(
    start: date,
    end: date,
    daily_start: date = REGIME_DAILY_START,
    yearly_through_year: int = PRE_REGIME_YEARLY_THROUGH_YEAR,
) -> List[PlannedUnit]:
    """Build a regime-aware, strictly pre-2023 retrieval plan.

    No download occurs. Aborts if the window or any planned unit reaches 2023+.
    The pre-boundary yearly/monthly split is a documentation-level expectation
    and is overridable; it is not asserted as observed data.
    """
    if start > end:
        raise ValueError("start must be <= end")
    if end >= SEAL_START or start >= SEAL_START:
        raise Protocol2023PlusBreach(
            "planning window must be entirely pre-2023; got {}..{}".format(
                start, end
            )
        )

    units: List[PlannedUnit] = []

    # Yearly regime: whole years <= yearly_through_year.
    y = start.year
    while y <= end.year and y <= yearly_through_year:
        units.append(PlannedUnit(str(y), "yearly", date(y, 1, 1)))
        y += 1

    # Monthly regime: from max(start, first non-yearly month) to day before
    # daily_start.
    monthly_lo = date(max(start.year, yearly_through_year + 1), 1, 1)
    if monthly_lo < start:
        monthly_lo = date(start.year, start.month, 1)
    monthly_hi = min(end, daily_start - timedelta(days=1))
    cur = date(max(monthly_lo, date(yearly_through_year + 1, 1, 1)).year,
               max(monthly_lo, date(yearly_through_year + 1, 1, 1)).month, 1)
    while cur <= monthly_hi and cur < daily_start:
        units.append(
            PlannedUnit("{:04d}-{:02d}".format(cur.year, cur.month),
                        "monthly", cur)
        )
        cur = date(cur.year + (cur.month // 12),
                   (cur.month % 12) + 1, 1)

    # Daily regime: daily_start .. end.
    d = max(start, daily_start)
    while d <= end:
        units.append(PlannedUnit(d.isoformat(), "daily", d))
        d += timedelta(days=1)

    assert_no_2023plus([u.rep_date for u in units], "plan_gdelt1_files")
    units.sort(key=lambda u: (u.rep_date, u.regime))
    return units


# ── 2. Freeze / manifest scaffolding ─────────────────────────────────────────

def build_freeze_manifest(
    coverage_start: date,
    coverage_end: date,
    planned_units: Sequence[PlannedUnit],
    file_hashes: Optional[Dict[str, str]] = None,
    endpoint_attempted_2023plus: bool = False,
    urls_per_unit: Optional[Dict[str, str]] = None,
    file_sizes: Optional[Dict[str, int]] = None,
    aggregate_content_hash: Optional[str] = None,
    row_counts: Optional[Dict[str, int]] = None,
    access_timestamp: Optional[str] = None,
    gdelt_2013_regime_boundary_handled: bool = True,
    gdelt_normalization_files_status: str = "deferred",
    min_event_floor: Optional[int] = None,
    option_c_threshold: Optional[float] = None,
) -> Dict[str, object]:
    if coverage_end >= SEAL_START:
        raise Protocol2023PlusBreach("manifest coverage_end is 2023+")
    if gdelt_normalization_files_status not in NORMALIZATION_STATUS_VALUES:
        raise ValueError(
            "gdelt_normalization_files_status must be one of {}".format(
                NORMALIZATION_STATUS_VALUES
            )
        )
    assert_no_2023plus([u.rep_date for u in planned_units],
                       "build_freeze_manifest")
    return {
        "source_product": SELECTED_SOURCE,
        "retrieval_method": "GDELT 1.0 static archive (per-unit files); "
                            "no download performed in this draft",
        "url_template_default": DEFAULT_GDELT1_BASE_URL,
        "urls_per_unit": dict(urls_per_unit or {}),
        "coverage_start": coverage_start.isoformat(),
        "coverage_end": coverage_end.isoformat(),
        "date_restriction_excluding_2023plus": "units strictly < {}".format(
            SEAL_START.isoformat()
        ),
        "access_timestamp": access_timestamp,
        "file_list": [u.key for u in planned_units],
        "file_count": len(planned_units),
        "file_sizes": dict(file_sizes or {}),
        "row_counts": dict(row_counts or {}),  # filled by a future real run
        "sha256_per_file": dict(file_hashes or {}),
        "aggregate_content_hash": aggregate_content_hash,
        "endpoint_attempted_2023plus": bool(endpoint_attempted_2023plus),
        "no_2023plus_downloaded_or_counted": True,
        "confirm_no_2023plus_downloaded_stored_sampled_counted_inspected": True,
        "gdelt_2013_regime_boundary_handled": bool(
            gdelt_2013_regime_boundary_handled
        ),
        "gdelt_normalization_files_status": gdelt_normalization_files_status,
        "min_event_floor": min_event_floor,
        "option_c_threshold": option_c_threshold,
        "governing_protocol_commit": GOVERNING_PROTOCOL_COMMIT,
        "authorization_commit": AUTHORIZATION_COMMIT,
    }


# ── 3. Count-only parser scaffolding ─────────────────────────────────────────

def _read_lines(path: str) -> List[str]:
    """Read a local fixture file (.zip with one inner file, or text)."""
    if path.endswith(".zip"):
        with zipfile.ZipFile(path) as zf:
            inner = zf.namelist()[0]
            with zf.open(inner) as fh:
                return fh.read().decode("utf-8").splitlines()
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().splitlines()


def _parse_sqldate(token: str) -> date:
    token = token.strip()
    if len(token) != 8 or not token.isdigit():
        raise ValueError("bad SQLDATE token: {!r}".format(token))
    return date(int(token[0:4]), int(token[4:6]), int(token[6:8]))


def parse_gdelt1_file_daily_counts(
    path: str,
    sqldate_col: int = GDELT1_SQLDATE_COL_DEFAULT,
    delimiter: str = "\t",
) -> Dict[date, int]:
    """Count event rows by event date from one local frozen/fixture file.

    Count-only: no content interpretation, no outcome, no market data. Aborts
    on any 2023+ row.
    """
    counts: Dict[date, int] = {}
    for line in _read_lines(path):
        if not line.strip():
            continue
        parts = line.split(delimiter)
        if len(parts) <= sqldate_col:
            raise ValueError("row has no SQLDATE column: {!r}".format(line))
        d = _parse_sqldate(parts[sqldate_col])
        if d >= SEAL_START:
            raise Protocol2023PlusBreach(
                "2023+ row in {}: {}".format(path, d)
            )
        counts[d] = counts.get(d, 0) + 1
    return counts


def aggregate_daily_counts(
    per_file: Sequence[Dict[date, int]],
) -> Dict[date, int]:
    out: Dict[date, int] = {}
    for fc in per_file:
        for d, c in fc.items():
            if d >= SEAL_START:
                raise Protocol2023PlusBreach("2023+ in aggregate: {}".format(d))
            out[d] = out.get(d, 0) + c
    return out


def missingness_by_year(
    daily_counts: Dict[date, int],
    coverage_start: date,
    coverage_end: date,
) -> Dict[int, Dict[str, int]]:
    """Per-year expected vs observed calendar-day coverage (count-only)."""
    if coverage_end >= SEAL_START:
        raise Protocol2023PlusBreach("missingness coverage_end is 2023+")
    report: Dict[int, Dict[str, int]] = {}
    d = coverage_start
    while d <= coverage_end:
        yr = report.setdefault(d.year, {"expected_days": 0, "observed_days": 0})
        yr["expected_days"] += 1
        if daily_counts.get(d, 0) > 0:
            yr["observed_days"] += 1
        d += timedelta(days=1)
    for yr in report.values():
        yr["missing_days"] = yr["expected_days"] - yr["observed_days"]
    return report


def by_year_counts(daily_counts: Dict[date, int]) -> Dict[int, int]:
    assert_no_2023plus(list(daily_counts.keys()), "by_year_counts")
    out: Dict[int, int] = {}
    for d, c in daily_counts.items():
        out[d.year] = out.get(d.year, 0) + c
    return dict(sorted(out.items()))


# ── 4. Attention-spike count definitions (count-only, pre-2023) ──────────────

def _ordered_valid_series(
    daily_counts: Dict[date, int],
) -> List[Tuple[date, int]]:
    items = sorted((d, c) for d, c in daily_counts.items() if c > 0)
    assert_no_2023plus([d for d, _ in items], "_ordered_valid_series")
    return items


def option_a_percentile_spikes(
    daily_counts: Dict[date, int], baseline: int = 60, pct: float = 0.95
) -> List[date]:
    """Spike if count >= the `pct` quantile of the trailing `baseline`
    strictly-prior valid observations. Count-only."""
    s = _ordered_valid_series(daily_counts)
    spikes: List[date] = []
    vals = [c for _, c in s]
    for i in range(len(s)):
        if i < baseline:
            continue
        window = sorted(vals[i - baseline:i])
        # nearest-rank quantile (deterministic, no interpolation)
        rank = max(0, min(len(window) - 1,
                          int(round(pct * (len(window) - 1)))))
        if vals[i] >= window[rank]:
            spikes.append(s[i][0])
    return spikes


def option_b_zscore_spikes(
    daily_counts: Dict[date, int], baseline: int = 60, z: float = 2.5
) -> List[date]:
    s = _ordered_valid_series(daily_counts)
    vals = [c for _, c in s]
    spikes: List[date] = []
    for i in range(len(s)):
        if i < baseline:
            continue
        w = vals[i - baseline:i]
        mean = sum(w) / len(w)
        var = sum((x - mean) ** 2 for x in w) / (len(w) - 1)  # ddof=1
        if var == 0:
            continue  # undefined z; not a spike (honest, not silently 0)
        if (vals[i] - mean) / (var ** 0.5) >= z:
            spikes.append(s[i][0])
    return spikes


def option_c_acceleration_spikes(
    daily_counts: Dict[date, int], threshold: Optional[float] = None
) -> List[date]:
    """Spike if day-over-day acceleration (Δcount) >= threshold.

    The authorization memo does not pin a threshold; it is REQUIRED here. No
    silent default.
    """
    if threshold is None:
        raise ValueError(
            "option_c_acceleration_spikes requires an explicit threshold "
            "(authorization memo pins none; no silent default)"
        )
    s = _ordered_valid_series(daily_counts)
    spikes: List[date] = []
    for i in range(1, len(s)):
        if (s[i][1] - s[i - 1][1]) >= threshold:
            spikes.append(s[i][0])
    return spikes


# ── 5. Clustering and overlap counts (calendar-day; no market data) ──────────

def cluster_spikes(
    spike_dates: Sequence[date], separation_days: int
) -> List[date]:
    """Collapse spikes within `separation_days` calendar days; keep first."""
    ds = sorted(spike_dates)
    assert_no_2023plus(ds, "cluster_spikes")
    clustered: List[date] = []
    last: Optional[date] = None
    for d in ds:
        if last is None or (d - last).days > separation_days:
            clustered.append(d)
            last = d
    return clustered


def event_window_overlap_count(
    spike_dates: Sequence[date], lo: int, hi: int
) -> Dict[str, object]:
    """Count events whose hypothetical [d+lo, d+hi] calendar window overlaps
    another event's window. NO returns, NO market data."""
    ds = sorted(spike_dates)
    assert_no_2023plus(ds, "event_window_overlap_count")
    intervals = [(d + timedelta(days=lo), d + timedelta(days=hi)) for d in ds]
    overlapping = 0
    for i, (a0, a1) in enumerate(intervals):
        for j, (b0, b1) in enumerate(intervals):
            if i != j and a0 <= b1 and b0 <= a1:
                overlapping += 1
                break
    n = len(ds)
    return {
        "window": "t+{}:t+{}".format(lo, hi),
        "n_events": n,
        "overlapping_events": overlapping,
        "overlap_fraction": (overlapping / n) if n else None,
    }


# ── 6. Non-trading-day count (no market price loading) ───────────────────────

def non_trading_day_count(
    spike_dates: Sequence[date],
    session_calendar: Optional[Sequence[date]] = None,
) -> Dict[str, object]:
    if session_calendar is None:
        return {"status": "calendar_unavailable",
                "non_trading_day_count": None}
    sessions = set(session_calendar)
    cnt = sum(1 for d in spike_dates if d not in sessions)
    return {"status": "resolved", "non_trading_day_count": cnt}


# ── 7. State-axis feasibility (no market-derived state here) ──────────────────

def state_count_feasibility(
    frozen_pre2023_state_source: Optional[object] = None,
) -> Dict[str, object]:
    """State counts are allowed ONLY if a frozen pre-2023 state source is
    provided. None is selected/frozen, so this is unresolved. No SPY/VIX/
    returns/CAR/market data is loaded here."""
    if frozen_pre2023_state_source is None:
        return {
            "status": "unresolved",
            "reason": "no frozen pre-2023 state source provided; "
                      "price-derived state intentionally not computed "
                      "(construction-coupling burden, see readiness memo)",
        }
    return {"status": "resolved",
            "note": "state source must itself be frozen and pre-2023"}


# ── 8. Feasibility-class scaffolding (NOT hypothesis verdicts) ────────────────

F_NOTES = {
    "F0": "no suitable source found",
    "F1": "source available but event counts too low",
    "F2": "source available, event counts adequate, state counts inadequate",
    "F3": "source and counts adequate enough for Step 2 lock DRAFTING ONLY "
          "— this does NOT confirm the Lane 2 hypothesis",
    "F4": "feasibility inconclusive (coverage / missingness / reproducibility)",
    "F5": "methodological failure / protocol breach",
}


def assign_feasibility_class(
    source_found: bool,
    raw_spike_count: int,
    min_event_floor: int,
    state_status: str,
    reproducibility_ok: bool,
    protocol_breach: bool,
) -> Tuple[str, str]:
    if protocol_breach:
        cls = "F5"
    elif not source_found:
        cls = "F0"
    elif not reproducibility_ok:
        cls = "F4"
    elif raw_spike_count < min_event_floor:
        cls = "F1"
    elif state_status != "resolved":
        cls = "F2"
    else:
        cls = "F3"
    return cls, F_NOTES[cls]


# ── 9. Output scaffolding (writes only where caller points; tests use tmp) ────

def write_json(path: str, obj: object) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, default=str)
        fh.write("\n")


def write_csv(path: str, header: Sequence[str], rows: Sequence[Sequence]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def write_markdown(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text if text.endswith("\n") else text + "\n")


# ── 13. Metadata builder ─────────────────────────────────────────────────────

NORMALIZATION_STATUS_VALUES = ("used", "not_used", "deferred")


def build_metadata(
    coverage_start: date,
    coverage_end: date,
    regime_boundary_handled: bool,
    by_year_reported: bool,
    state_status: str,
    feasibility_class: str,
    gdelt_normalization_files_status: str = "deferred",
    min_event_floor: Optional[int] = None,
    option_c_threshold: Optional[float] = None,
    archive_layout_status: str = "not_checked",
    option_c_enabled: bool = False,
    run_authorization_memo: str = RUN_AUTHORIZATION_MEMO_PATH,
    post_run_safety_reset_required: bool = False,
) -> Dict[str, object]:
    if coverage_end >= SEAL_START:
        raise Protocol2023PlusBreach("metadata coverage_end is 2023+")
    if gdelt_normalization_files_status not in NORMALIZATION_STATUS_VALUES:
        raise ValueError(
            "gdelt_normalization_files_status must be one of {}; got {!r}".format(
                NORMALIZATION_STATUS_VALUES, gdelt_normalization_files_status
            )
        )
    if archive_layout_status not in ARCHIVE_LAYOUT_STATUS_VALUES:
        raise ValueError(
            "archive_layout_status must be one of {}; got {!r}".format(
                ARCHIVE_LAYOUT_STATUS_VALUES, archive_layout_status
            )
        )
    return {
        "governing_protocol_commit": GOVERNING_PROTOCOL_COMMIT,
        "authorization_commit": AUTHORIZATION_COMMIT,
        "selected_source": SELECTED_SOURCE,
        "coverage_window_attempted": "{}..{}".format(
            coverage_start.isoformat(), coverage_end.isoformat()
        ),
        "no_2023_plus": True,
        # Run-authorization memo §17 spells this key without an underscore;
        # both are emitted so neither the memo nor prior tests drift.
        "no_2023plus": True,
        "outcomes_computed": False,
        "returns_computed": False,
        "models_fit": False,
        "p_values_computed": False,
        "step2_lock_drafted": False,
        "feasibility_only": True,
        "hypothesis_verdict": False,
        "gdelt_2013_regime_boundary_handled": bool(regime_boundary_handled),
        "by_year_counts_reported": bool(by_year_reported),
        "state_count_feasibility_status": state_status,
        "feasibility_class": feasibility_class,
        "feasibility_class_note": F_NOTES.get(feasibility_class, ""),
        # Run-authorization memo §17: archive-layout status (controlled vocab).
        # For the real run this must reflect verify_archive_layout /
        # layout_outcome (see archive_layout_status_token / orchestrator).
        "archive_layout_status": archive_layout_status,
        "option_c_enabled": bool(option_c_enabled),
        "run_authorization_commit": RUN_AUTHORIZATION_COMMIT,
        "run_authorization_memo": run_authorization_memo,
        # True only if a run left REAL_RETRIEVAL_ENABLED / the runner constant
        # permissive; a separate inert-restore safety commit is then required.
        "post_run_safety_reset_required": bool(post_run_safety_reset_required),
        "post_run_safety_reset_note": (
            "If the run enabled retrieval by leaving REAL_RETRIEVAL_ENABLED "
            "or COUNT_FEASIBILITY_AUTHORIZED permissive in source, a separate "
            "inert-restore safety commit is required (memo §13)."
        ),
        # Authorization-memo requirement: record normalization-file choice.
        "gdelt_normalization_files_status": gdelt_normalization_files_status,
        "gdelt_normalization_files_note": (
            "Normalization files are not applied in this scaffold. The "
            "normalization choice must be pinned before any real count-only "
            "run authorization."
        ),
        # Pinned-parameter echoes. Explicit None when unpinned (never omitted).
        "min_event_floor": min_event_floor,
        "min_event_floor_note": (
            "min_event_floor must be pinned before any real count-only "
            "feasibility run."
        ),
        "option_c_threshold": option_c_threshold,
        "option_c_threshold_note": (
            "Option-C threshold must be explicitly supplied; no silent "
            "default is allowed."
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Live retrieval / freeze scaffolding (draft).
#
# NOTHING here performs a real network download. download_one() fails closed
# unless explicitly network-authorized AND given an opener; the runner never
# enables that. Tests inject a fake opener / local fixtures only. Still
# count-only: no returns, CAR, market data, models, p-values, Step 2, 2023+.
# ─────────────────────────────────────────────────────────────────────────────

# Visible (not hidden) documentation-level GDELT 1.0 base URL. This is the
# per-FILE download base (base + "<YYYYMMDD>.export.CSV.zip"). The exact
# remote layout MUST be verified at freeze time; this is overridable.
# R1 (Gate 4A, authorization 745af67) does NOT change this constant — per-file
# URLs must keep resolving under the directory path.
DEFAULT_GDELT1_BASE_URL = "http://data.gdeltproject.org/events/"

# R1 (Gate 4A offline patch, authorized by docs/lane2_gdelt1_gate4A_r1_
# offline_patch_authorization_v0.1.md = 745af67; evidence: Substep 1 doc-fetch
# 10b80c7 names this resource, Substep 2A HEAD 9a8fb7b confirmed it returns
# 200/non-empty/text/html). The INDEX/LISTING target is the documented
# index.html resource, NOT the bare directory path. This corrects the
# request-target defect identified through the diagnostic chain. It does NOT
# perform any request, flip any guard, or alter the Gate 2 parser.
DEFAULT_GDELT1_INDEX_URL = "http://data.gdeltproject.org/events/index.html"

# Documentation-level filename templates per regime (overridable; verify at
# freeze). Keys: yearly -> "YYYY", monthly -> "YYYYMM", daily -> "YYYYMMDD".
DEFAULT_GDELT1_FILENAME_TEMPLATES = {
    "yearly": "{yyyy}.zip",
    "monthly": "{yyyy}{mm}.zip",
    "daily": "{yyyy}{mm}{dd}.export.CSV.zip",
}

# Real retrieval is NOT enabled in this draft. A future, separately reviewed
# change flips this; download_one() also requires an explicit opener.
REAL_RETRIEVAL_ENABLED = False


class RetrievalNotAuthorized(RuntimeError):
    """Raised when a download is attempted without explicit authorization."""


@dataclass(frozen=True)
class RetrievalEntry:
    key: str
    regime: str
    rep_date: date
    filename: str
    url: str


def build_unit_filename(
    unit: PlannedUnit,
    templates: Optional[Dict[str, str]] = None,
) -> str:
    tpl = (templates or DEFAULT_GDELT1_FILENAME_TEMPLATES)[unit.regime]
    d = unit.rep_date
    return tpl.format(
        yyyy="{:04d}".format(d.year),
        mm="{:02d}".format(d.month),
        dd="{:02d}".format(d.day),
    )


def build_retrieval_plan(
    units: Sequence[PlannedUnit],
    base_url: str = DEFAULT_GDELT1_BASE_URL,
    templates: Optional[Dict[str, str]] = None,
) -> List[RetrievalEntry]:
    """Attach URL/filename to each planned unit. Pre-2023 enforced."""
    assert_no_2023plus([u.rep_date for u in units], "build_retrieval_plan")
    base = base_url if base_url.endswith("/") else base_url + "/"
    out: List[RetrievalEntry] = []
    for u in units:
        fn = build_unit_filename(u, templates)
        out.append(RetrievalEntry(u.key, u.regime, u.rep_date, fn, base + fn))
    return out


def validate_source_index(
    index_entries: Sequence[Dict[str, object]],
) -> List[date]:
    """Validate an externally supplied source index/list.

    Each entry must carry a parseable pre-2023 date under key 'date'
    (YYYY-MM-DD) or 'rep_date' (datetime.date). Aborts on any 2023+ entry or
    missing date. Returns the validated, sorted date list.
    """
    dates: List[date] = []
    for e in index_entries:
        if "rep_date" in e and isinstance(e["rep_date"], date):
            d = e["rep_date"]
        elif "date" in e and isinstance(e["date"], str):
            d = date.fromisoformat(e["date"])
        else:
            raise ValueError("source-index entry lacks a usable date: "
                             "{!r}".format(e))
        dates.append(d)
    assert_no_2023plus(dates, "validate_source_index")
    return sorted(dates)


def download_one(
    url: str,
    dest_path: str,
    expected_pre2023_date: date,
    timeout: float = 30.0,
    retries: int = 2,
    network_authorized: bool = False,
    opener: Optional[Callable] = None,
) -> Dict[str, object]:
    """Download one planned file: temp write -> fsync -> atomic move; sha256
    + size. Fails closed.

    Does NOT perform a real download in this draft: requires BOTH
    REAL_RETRIEVAL_ENABLED and network_authorized AND an explicit `opener`.
    Tests pass a fake opener (no real network). The runner never authorizes
    this.
    """
    if expected_pre2023_date >= SEAL_START:
        raise Protocol2023PlusBreach(
            "refusing download for 2023+ unit: {}".format(expected_pre2023_date)
        )
    if not (REAL_RETRIEVAL_ENABLED and network_authorized):
        raise RetrievalNotAuthorized(
            "real retrieval is not authorized in this draft "
            "(REAL_RETRIEVAL_ENABLED={}, network_authorized={})".format(
                REAL_RETRIEVAL_ENABLED, network_authorized
            )
        )
    if opener is None:
        raise RetrievalNotAuthorized(
            "no opener provided; refusing to construct a live network client"
        )

    last_err: Optional[Exception] = None
    for _ in range(max(1, retries)):
        try:
            resp = opener(url, timeout=timeout)
            data = resp.read()
            dest_dir = os.path.dirname(os.path.abspath(dest_path)) or "."
            os.makedirs(dest_dir, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=dest_dir, suffix=".part")
            try:
                with os.fdopen(fd, "wb") as fh:
                    fh.write(data)
                    fh.flush()
                    os.fsync(fh.fileno())
                os.replace(tmp, dest_path)  # atomic
            finally:
                if os.path.exists(tmp):
                    os.remove(tmp)
            return {
                "url": url,
                "dest_path": dest_path,
                "sha256": hashlib.sha256(data).hexdigest(),
                "size_bytes": len(data),
                "expected_pre2023_date": expected_pre2023_date.isoformat(),
            }
        except Exception as exc:  # fail closed; retry
            last_err = exc
    raise RuntimeError("download failed after retries: {}".format(last_err))


LAYOUT_FEASIBILITY_NOTE = (
    "This is a coverage/layout feasibility issue, not hypothesis evidence."
)


def parse_gdelt1_unit_key(key: str) -> Tuple[date, str]:
    """Parse a PlannedUnit-style key into (rep_date, regime).

    "YYYY" -> yearly, "YYYY-MM" -> monthly, "YYYY-MM-DD" -> daily.
    Raises ValueError if unparseable. Raises Protocol2023PlusBreach if the
    parsed date is 2023+ (prior 2023+ guard).
    """
    parts = key.split("-")
    try:
        if len(parts) == 1 and len(parts[0]) == 4:
            d, regime = date(int(parts[0]), 1, 1), "yearly"
        elif len(parts) == 2:
            d, regime = date(int(parts[0]), int(parts[1]), 1), "monthly"
        elif len(parts) == 3:
            d, regime = (
                date(int(parts[0]), int(parts[1]), int(parts[2])),
                "daily",
            )
        else:
            raise ValueError("unrecognized unit-key shape: {!r}".format(key))
    except ValueError as exc:
        if isinstance(exc, ValueError) and "unrecognized unit-key" in str(exc):
            raise
        raise ValueError("unparseable unit key: {!r}".format(key))
    if d >= SEAL_START:
        raise Protocol2023PlusBreach(
            "2023+ unit key encountered: {}".format(key)
        )
    return d, regime


def _try_parse_unit_key(
    key: str, key_parser: Callable[[str], Tuple[date, str]]
) -> Optional[Tuple[date, str]]:
    """Parse if possible; None if not a unit-shaped key. 2023+ still aborts."""
    try:
        return key_parser(key)
    except Protocol2023PlusBreach:
        raise  # prior 2023+ guard: never swallow
    except ValueError:
        return None


def verify_archive_layout(
    planned: Sequence[RetrievalEntry],
    available_keys: Sequence[str],
    expected_naming: Optional[Callable[[RetrievalEntry], bool]] = None,
    slot_actual_keys: Optional[Dict[str, str]] = None,
    key_parser: Optional[Callable[[str], Tuple[date, str]]] = None,
) -> Dict[str, object]:
    """Freeze-time scaffold: compare the documented plan to a (fake, in this
    draft) listing of what the archive actually exposes.

    `slot_actual_keys` maps a planned unit key -> the actual key string the
    archive exposes for that slot. When supplied, each is parsed and compared
    to the planned unit's (rep_date, regime); divergence is a first-class
    file/date-unit mismatch (not folded into missing/unexpected/naming).
    """
    parser = key_parser or parse_gdelt1_unit_key
    # Prior 2023+ guards: planned units, and any parseable available/slot key.
    assert_no_2023plus([p.rep_date for p in planned], "verify_archive_layout")
    for k in available_keys:
        _try_parse_unit_key(k, parser)  # raises Protocol2023PlusBreach on 2023+
    for k in (slot_actual_keys or {}).values():
        _try_parse_unit_key(k, parser)

    avail = set(available_keys)
    planned_keys = [p.key for p in planned]
    planned_by_key = {p.key: p for p in planned}
    missing = [k for k in planned_keys if k not in avail]
    unexpected = [k for k in avail if k not in set(planned_keys)]
    naming_bad = []
    if expected_naming is not None:
        naming_bad = [p.key for p in planned if not expected_naming(p)]

    # Dedicated file/date-unit mismatch detection.
    date_unit_mismatch: List[Dict[str, str]] = []
    for planned_key, actual_key in (slot_actual_keys or {}).items():
        p = planned_by_key.get(planned_key)
        if p is None:
            continue
        parsed = _try_parse_unit_key(actual_key, parser)
        if parsed is None:
            # actual key not unit-shaped -> a regime/naming mismatch
            date_unit_mismatch.append({
                "planned_key": planned_key,
                "actual_key": actual_key,
                "reason": "actual key not unit-parseable",
            })
            continue
        a_date, a_regime = parsed
        if a_date != p.rep_date or a_regime != p.regime:
            date_unit_mismatch.append({
                "planned_key": planned_key,
                "planned": "{} {}".format(p.regime, p.rep_date.isoformat()),
                "actual": "{} {}".format(a_regime, a_date.isoformat()),
            })

    pre = [p for p in planned if p.rep_date < REGIME_DAILY_START]
    post = [p for p in planned if p.rep_date >= REGIME_DAILY_START]
    layout_differs = bool(
        missing or unexpected or naming_bad or date_unit_mismatch
    )
    return {
        "files_available": sorted(k for k in planned_keys if k in avail),
        "files_missing": missing,
        "files_unexpected_naming": naming_bad,
        "files_in_archive_not_planned": unexpected,
        "files_date_unit_mismatch": date_unit_mismatch,
        "pre_2013_regime_coverage": len(pre),
        "post_2013_daily_coverage": len(post),
        "boundary_2013_04_01_handled": True,
        "actual_layout_differs_from_documented": layout_differs,
        "note": LAYOUT_FEASIBILITY_NOTE,
    }


def layout_outcome(report: Dict[str, object]) -> Tuple[str, str]:
    """Map a layout report to a feasibility action. Differing layout -> F4
    (inconclusive) unless separately approved; never silently 'ok'."""
    if report.get("actual_layout_differs_from_documented"):
        return "F4", (
            "actual archive layout differs from documented-overridable "
            "assumptions (missing/unexpected/naming/date-unit mismatch); "
            "separate approval required. " + LAYOUT_FEASIBILITY_NOTE
        )
    return "ok", "layout matches documented plan"


def archive_layout_status_token(
    report: Optional[Dict[str, object]],
) -> str:
    """Reduce a verify_archive_layout report to one ARCHIVE_LAYOUT_STATUS_VALUES
    token for run metadata (memo §17).

    None -> "not_checked"; clean -> "ok". Otherwise a single, deterministic
    token by priority: file/date-unit mismatch -> "mismatch"; else missing
    files -> "missing"; else unexpected/naming -> "unexpected"; else any other
    documented divergence -> "f4_layout_issue".
    """
    if report is None:
        return "not_checked"
    if not report.get("actual_layout_differs_from_documented"):
        return "ok"
    if report.get("files_date_unit_mismatch"):
        return "mismatch"
    if report.get("files_missing"):
        return "missing"
    if report.get("files_in_archive_not_planned") or report.get(
        "files_unexpected_naming"
    ):
        return "unexpected"
    return "f4_layout_issue"


# ── Drift / concentration feasibility flags (descriptive, unthresholded) ──────

def concentration_flags(
    daily_counts: Dict[date, int],
    spike_dates: Sequence[date],
    clustered_spike_dates: Sequence[date],
    regime_daily_start: date = REGIME_DAILY_START,
) -> Dict[str, object]:
    """Count-only drift/concentration flags (memo §12).

    Reports by-year daily-observation counts, by-year raw and clustered spike
    counts, and the post-2013-04-01 / later-half *fractions*. The
    run-authorization memo pins NO thresholds, so no spike/non-spike verdict
    is rendered: interpretation is explicitly descriptive/unthresholded and
    is NOT hypothesis evidence.
    """
    assert_no_2023plus(list(daily_counts.keys()), "concentration_flags")
    assert_no_2023plus(list(spike_dates), "concentration_flags")
    assert_no_2023plus(list(clustered_spike_dates), "concentration_flags")

    def _by_year(ds: Sequence[date]) -> Dict[int, int]:
        out: Dict[int, int] = {}
        for d in ds:
            out[d.year] = out.get(d.year, 0) + 1
        return dict(sorted(out.items()))

    n_sp = len(spike_dates)
    yrs = [d.year for d in daily_counts] or [PINNED_COVERAGE_START.year]
    mid_year = (min(yrs) + max(yrs)) / 2.0
    post_2013 = sum(1 for d in spike_dates if d >= regime_daily_start)
    later_half = sum(1 for d in spike_dates if d.year >= mid_year)
    return {
        "daily_observation_counts_by_year": by_year_counts(daily_counts),
        "raw_spike_counts_by_year": _by_year(spike_dates),
        "clustered_spike_counts_by_year": _by_year(clustered_spike_dates),
        "raw_spikes_post_2013_04_01_fraction": (
            (post_2013 / n_sp) if n_sp else None
        ),
        "raw_spikes_later_half_fraction": (
            (later_half / n_sp) if n_sp else None
        ),
        "concentration_interpretation": "descriptive_unthresholded",
        "note": (
            "Distributions only; the run-authorization memo pins no "
            "concentration threshold. Feasibility flag, NOT hypothesis "
            "evidence."
        ),
    }


# ── Robust index/listing extractor (Gate 2 offline remediation) ──────────────
#
# Authorized by docs/lane2_gdelt1_remediation_patch_authorization_v0.1.md
# (be2a7df), bounded by the design memo (12ae078). OFFLINE PARSER/DISCOVERY
# logic only — operates on already-supplied listing text (HTML or plain). It
# does NOT change which resource is fetched (R1 is OUT OF SCOPE / deferred to
# Gate 4), performs no network/GET/HEAD, and adds no live path.
#
#   R2 — HTML/listing-robust filename extraction (regex over the whole text;
#        survives anchor tags, quotes, angle brackets, attributes).
#   R4 — instrumentation: recognized / ignored_out_of_window /
#        rejected_2023plus / unrecognized counts (no silent token drops).
#   R5 — immediate 2005–2022 extraction filter (pinned window) at extraction.
#   R6 — hard-fail (Protocol2023PlusBreach) on ANY 2023+ GDELT-form filename
#        BEFORE any keys are returned or any downstream planning/count logic.

# GDELT 1.0 filename forms: yearly "YYYY.zip", monthly "YYYYMM.zip",
# daily "YYYYMMDD.export.CSV.zip". Matched anywhere in arbitrary HTML/text.
_GDELT1_FILE_RE = re.compile(
    r"(?<![0-9])(\d{4}|\d{6}|\d{8})(\.export\.CSV)?\.zip\b",
    re.IGNORECASE,
)
# Any file-like token, for unrecognized-token instrumentation (R4).
_FILELIKE_RE = re.compile(r"[A-Za-z0-9_.\-]+\.(?:zip|html?|txt|csv)\b",
                          re.IGNORECASE)


@dataclass(frozen=True)
class IndexExtraction:
    """Result of robust listing extraction.

    `keys`/`slot_actual_keys` are the in-window (2005–2022) recognized unit
    keys (PlannedUnit-style). `instrumentation` records counts so a future F4
    is self-diagnosing (no silent drops). 2023+ never reaches here: it
    hard-fails earlier (R6).
    """

    keys: List[str]
    slot_actual_keys: Dict[str, str]
    instrumentation: Dict[str, int]


def _legacy_whitespace_index_tokens(text: str) -> List[str]:
    """The PRE-remediation whitespace tokenizer, preserved ONLY so the failure
    mode is representable in a synthetic regression test. Not used by the
    pipeline. No network, no 2023+ raising (pure demonstration helper)."""
    out: List[str] = []
    for tok in text.split():
        name = tok.strip().strip('"\'<>')
        if "." not in name:
            continue
        stem = name.split(".")[0]
        if not (stem.isdigit() and len(stem) in (4, 6, 8)):
            continue
        out.append(stem)
    return out


def _classify_gdelt1_filename(
    stem: str, is_export: bool
) -> Optional[Tuple[str, date]]:
    """Map a matched (stem, is_export) to (unit_key, rep_date), or None if the
    form is malformed/ambiguous (counted as unrecognized, never silently
    dropped)."""
    try:
        if len(stem) == 4 and not is_export:
            return stem, date(int(stem), 1, 1)
        if len(stem) == 6 and not is_export:
            return ("{}-{}".format(stem[:4], stem[4:6]),
                    date(int(stem[:4]), int(stem[4:6]), 1))
        if len(stem) == 8 and is_export:
            return ("{}-{}-{}".format(stem[:4], stem[4:6], stem[6:8]),
                    date(int(stem[:4]), int(stem[4:6]), int(stem[6:8])))
    except ValueError:
        return None  # impossible calendar date -> unrecognized
    return None  # e.g. 8-digit w/o .export.CSV, 6-digit w/ .export.CSV


def extract_index_units(
    text: str,
    window_start: date = PINNED_COVERAGE_START,
    window_end: date = PINNED_COVERAGE_END,
) -> IndexExtraction:
    """Robustly extract GDELT 1.0 unit keys from listing `text` (HTML or
    plain). R2+R4+R5+R6. Fails closed on 2023+ (R6) BEFORE returning any keys.

    All counts are computed first so the rejection is fully instrumented; the
    Protocol2023PlusBreach is then raised (with `.instrumentation` and
    `.rejected_examples` attached) before any keys/downstream logic.
    """
    recognized: List[str] = []
    seen: set = set()
    seen_files: set = set()   # dedupe by distinct filename (href vs link text)
    n_ignored = 0          # distinct GDELT-form file, parseable, pre-2023, <2005
    rejected: List[str] = []   # distinct 2023+ GDELT-form filenames (R6)
    n_malformed = 0        # distinct GDELT-ish .zip, ambiguous/invalid form

    for mt in _GDELT1_FILE_RE.finditer(text):
        fname = mt.group(0).lower()
        if fname in seen_files:          # same file in href + text -> once
            continue
        seen_files.add(fname)
        stem = mt.group(1)
        is_export = mt.group(2) is not None
        classified = _classify_gdelt1_filename(stem, is_export)
        if classified is None:
            n_malformed += 1
            continue
        key, rep = classified
        if rep >= SEAL_START:                       # R6: 2023+ -> reject
            rejected.append(mt.group(0))
            continue
        if rep < window_start or rep > window_end:  # R5: out-of-window
            n_ignored += 1
            continue
        if key not in seen:                         # in-window recognized
            seen.add(key)
            recognized.append(key)

    # Unrecognized non-GDELT file-like tokens (R4: never silently dropped),
    # deduped by distinct filename.
    gdelt_files = {f for f in seen_files}
    n_unrecognized = len({
        fm.group(0).lower()
        for fm in _FILELIKE_RE.finditer(text)
        if fm.group(0).lower() not in gdelt_files
    })

    instrumentation = {
        "recognized_in_window": len(recognized),
        "ignored_out_of_window": n_ignored,
        "rejected_2023plus": len(rejected),
        "unrecognized_tokens": n_unrecognized,
        "malformed_gdelt_tokens": n_malformed,
    }

    if rejected:  # R6: fail closed BEFORE returning keys / downstream logic
        exc = Protocol2023PlusBreach(
            "2023+ filename(s) in index listing (hard-fail before "
            "planning/count): e.g. {} (rejected_2023plus={})".format(
                rejected[:3], len(rejected)
            )
        )
        exc.instrumentation = instrumentation        # type: ignore[attr-defined]
        exc.rejected_examples = rejected[:10]         # type: ignore[attr-defined]
        raise exc

    recognized.sort()
    return IndexExtraction(
        keys=recognized,
        slot_actual_keys={k: k for k in recognized},
        instrumentation=instrumentation,
    )


# ── Gate 4C: Strategy II live-path-safe firewall / redaction (54fb16a) ────────
#
# Authorized by Gate 4C authorization memo (54fb16a). Design route (i):
# redaction/aggregation layered over the existing Gate 2 extractor logic.
# extract_index_units R6 hard-fail is PRESERVED for synthetic/offline use.
# This parallel live-path counterpart applies ONLY under Strategy II.
#
# Binding constraint (Gate 4C §3): no real post-2022 filename appears in any
# field of LiveSafeExtraction, any exception message, .rejected_examples, log,
# JSON, markdown, stdout, test, report, or persisted artifact. Only the
# aggregate count (rejected_2023plus=N) and non-identifying form-class labels
# are retained. No guard is flipped; no run is authorized; no network path is
# added here. REAL_RETRIEVAL_ENABLED=False, COUNT_FEASIBILITY_AUTHORIZED=False.


@dataclass(frozen=True)
class LiveSafeExtraction:
    """Live-path-safe extraction result (Strategy II, Gate 4C, 54fb16a).

    No exact post-2022 filename in any field. In-window (pre-2023) keys are
    returned; post-2022 tokens are aggregated to count + non-identifying
    form-class labels only (no filename, no post-2022 date digits).
    Gate 2 (extract_index_units) is not modified and retains its hard-fail.
    """

    keys: List[str]
    slot_actual_keys: Dict[str, str]
    instrumentation: Dict[str, int]
    post2022_form_classes: List[str]   # e.g. ["daily_export"] — no date digits


def extract_index_units_live_safe(
    text: str,
    window_start: date = PINNED_COVERAGE_START,
    window_end: date = PINNED_COVERAGE_END,
) -> LiveSafeExtraction:
    """Strategy II live-path-safe index extraction (Gate 4C firewall, 54fb16a).

    Mirrors extract_index_units R2/R4/R5 logic for in-window tokens.
    R6 hard-fail is replaced by silent aggregation: post-2022 tokens increment
    rejected_2023plus, record a non-identifying form-class label, and are
    discarded — the exact filename is never placed in any return field,
    exception message, or emitted value.

    extract_index_units is NOT modified; Gate 2 synthetic/offline hard-fail
    behavior is fully preserved. This function is a parallel live-path
    counterpart only and does not wire any request or flip any guard.
    """
    recognized: List[str] = []
    seen: set = set()
    seen_files: set = set()
    n_ignored = 0
    n_rejected_2023plus = 0
    n_malformed = 0
    _post2022_form_classes_seen: set = set()

    for mt in _GDELT1_FILE_RE.finditer(text):
        fname = mt.group(0).lower()
        if fname in seen_files:          # dedupe href vs link text
            continue
        seen_files.add(fname)
        stem = mt.group(1)
        is_export = mt.group(2) is not None
        classified = _classify_gdelt1_filename(stem, is_export)
        if classified is None:
            n_malformed += 1
            continue
        key, rep = classified
        if rep >= SEAL_START:
            # Strategy II: aggregate only — exact filename dropped immediately,
            # no post-2022 date digits emitted anywhere.
            n_rejected_2023plus += 1
            if len(stem) == 8 and is_export:
                _post2022_form_classes_seen.add("daily_export")
            elif len(stem) == 6:
                _post2022_form_classes_seen.add("monthly")
            elif len(stem) == 4:
                _post2022_form_classes_seen.add("yearly")
            continue
        if rep < window_start or rep > window_end:
            n_ignored += 1
            continue
        if key not in seen:
            seen.add(key)
            recognized.append(key)

    gdelt_files = set(seen_files)
    n_unrecognized = len({
        fm.group(0).lower()
        for fm in _FILELIKE_RE.finditer(text)
        if fm.group(0).lower() not in gdelt_files
    })

    instrumentation = {
        "recognized_in_window": len(recognized),
        "ignored_out_of_window": n_ignored,
        "rejected_2023plus": n_rejected_2023plus,
        "unrecognized_tokens": n_unrecognized,
        "malformed_gdelt_tokens": n_malformed,
    }

    recognized.sort()
    return LiveSafeExtraction(
        keys=recognized,
        slot_actual_keys={k: k for k in recognized},
        instrumentation=instrumentation,
        post2022_form_classes=sorted(_post2022_form_classes_seen),
    )


def fetch_archive_index_live_safe(
    opener: Callable,
    index_url: str = DEFAULT_GDELT1_INDEX_URL,
    timeout: float = 30.0,
) -> LiveSafeExtraction:
    """Live-path-safe archive index fetch (Strategy II, Gate 4C, 54fb16a).

    Uses extract_index_units_live_safe instead of extract_index_units.
    No default network client; requires an injected opener. Post-2022 tokens
    are redacted/aggregated — no exact filename surfaces. Guards remain inert;
    no run is authorized by the presence of this function.
    """
    if opener is None:
        raise RetrievalNotAuthorized(
            "fetch_archive_index_live_safe requires an explicit opener; "
            "no hidden default network client is permitted"
        )
    resp = opener(index_url, timeout=timeout)
    text = resp.read()
    if isinstance(text, bytes):
        text = text.decode("utf-8", "replace")
    return extract_index_units_live_safe(text)


# ── Archive index fetch (injected opener only; no hidden network client) ──────

def fetch_archive_index(
    opener: Callable,
    index_url: str = DEFAULT_GDELT1_INDEX_URL,
    timeout: float = 30.0,
    return_detail: bool = False,
):
    """Fetch the GDELT 1.0 listing using an INJECTED opener, then extract via
    the robust offline extractor (`extract_index_units`).

    Returns `(available_unit_keys, slot_actual_keys)` by default (unchanged
    signature for the runner/orchestrator); returns the full `IndexExtraction`
    when `return_detail=True`. No default network client is ever constructed:
    `opener` is required.

    R1 (Gate 4A, authorization 745af67): the default `index_url` is the
    documented index/listing resource `DEFAULT_GDELT1_INDEX_URL`
    (`…/events/index.html`), NOT the bare directory path
    `DEFAULT_GDELT1_BASE_URL` (`…/events/`). This is the only behavioral
    change; no request is performed here (the injected `opener` is the sole
    request path) and no guard is flipped. 2023+ hard-fails inside
    `extract_index_units` before any keys are returned.
    """
    if opener is None:
        raise RetrievalNotAuthorized(
            "fetch_archive_index requires an explicit opener; no hidden "
            "default network client is permitted"
        )
    resp = opener(index_url, timeout=timeout)
    text = resp.read()
    if isinstance(text, bytes):
        text = text.decode("utf-8", "replace")
    detail = extract_index_units(text)
    if return_detail:
        return detail
    return detail.keys, detail.slot_actual_keys


# ── Output allow-list (prohibited artifacts can never be written) ────────────

ALLOWED_OUTPUT_BASENAMES = (
    "source_freeze_manifest.json",
    "count_feasibility_metadata.json",
    "daily_count_table.csv",
    "missingness_table.csv",
    "by_year_count_summary.csv",
    "spike_counts_option_a.csv",
    "spike_counts_option_b.csv",
    "clustering_counts.csv",
    "overlap_counts.csv",
    "feasibility_summary.md",
)

_PROHIBITED_OUTPUT_MARKERS = (
    "return", "car", "abnormal", "vix", "model", "pvalue", "p_value",
    "p-value", "sharpe", "backtest", "feature_importance", "verdict",
    "step2", "2023",
)


def _check_basename(name: str) -> None:
    """Single source of truth for the output allow-list. Raises
    ProtocolBreach (maps to F5) on any non-allow-listed or
    prohibited-marker basename. Used both pre-write and post-hoc."""
    if name not in ALLOWED_OUTPUT_BASENAMES:
        raise ProtocolBreach(
            "non-allow-listed output: {!r}".format(name)
        )
    low = name.lower()
    for bad in _PROHIBITED_OUTPUT_MARKERS:
        if bad in low:
            raise ProtocolBreach(
                "prohibited marker {!r} in output {!r}".format(bad, name)
            )


def _checked_path(output_dir: str, basename: str) -> str:
    """Pre-write gate: assert `basename` is allow-listed BEFORE any write,
    then return the full path. All artifact writes go through this so a
    prohibited file is never created on disk in the first place."""
    _check_basename(basename)
    return os.path.join(output_dir, basename)


def _assert_outputs_allowed(output_dir: str) -> None:
    """Post-hoc tripwire (retained as defense-in-depth alongside the
    pre-write _checked_path gate): only allow-listed count-only artifacts
    may exist in the run output directory."""
    for name in os.listdir(output_dir):
        if os.path.isdir(os.path.join(output_dir, name)):
            continue
        _check_basename(name)


# ── Count-only feasibility orchestrator (steps A–Q of the memo) ──────────────
#
# This is the wired retrieval/freeze/count flow. It performs a REAL download
# ONLY through the injected `opener` and ONLY when download_one's own guards
# pass (REAL_RETRIEVAL_ENABLED True at call time + network_authorized + opener).
# The shipped module keeps REAL_RETRIEVAL_ENABLED = False; the runner flips it
# transiently in-process inside the all-guards-passed branch only. Tests inject
# a fake opener + synthetic frozen files — no real network, no real GDELT.
# Count-only throughout: NO returns/CAR/outcomes/models/p-values/2023+/Step 2.

def run_count_only_feasibility(
    output_dir: str,
    opener: Callable,
    available_keys: Sequence[str],
    slot_actual_keys: Optional[Dict[str, str]] = None,
    coverage_start: date = PINNED_COVERAGE_START,
    coverage_end: date = PINNED_COVERAGE_END,
    min_event_floor: int = PINNED_MIN_EVENT_FLOOR,
    base_url: str = DEFAULT_GDELT1_BASE_URL,
    expected_naming: Optional[Callable[[RetrievalEntry], bool]] = None,
    post_run_safety_reset_required: bool = False,
) -> Dict[str, object]:
    """Execute one count-only feasibility pass into a fresh `output_dir`.

    Caller (runner) is responsible for guard checks and for creating the
    fresh timestamped `output_dir` before calling this. Option C is never
    computed. State feasibility stays unresolved (no market data loaded).
    Returns the metadata dict; writes only allow-listed count artifacts.
    """
    if coverage_start < PINNED_COVERAGE_START or coverage_end > \
            PINNED_COVERAGE_END:
        raise ProtocolBreach(
            "coverage window outside the pinned 2005-01-01..2022-12-31"
        )
    # Layout-status provenance: "not_checked" until layout verification is
    # entered; "breach_during_check" if a breach aborts the check itself;
    # otherwise the computed token (or, if a breach occurs AFTER a clean
    # layout pass, the real post-check token is retained — truthful).
    layout_status = "not_checked"
    try:
        # A. plan strictly-pre-2023 units. B. 2023+ asserted inside.
        units = plan_gdelt1_files(coverage_start, coverage_end)
        # C. URL/source plan.
        plan = build_retrieval_plan(units, base_url=base_url)
        # D. verify archive layout BEFORE any count computation.
        try:
            layout = verify_archive_layout(
                plan, available_keys,
                expected_naming=expected_naming,
                slot_actual_keys=slot_actual_keys,
            )
        except Protocol2023PlusBreach:
            layout_status = "breach_during_check"
            raise
        layout_cls, layout_reason = layout_outcome(layout)
        layout_status = archive_layout_status_token(layout)

        if layout_cls == "F4":
            # Memo §11/§14: do NOT proceed into counts, do NOT patch-and-rerun.
            # Counts/by-year/regime-boundary work never ran on this path, so
            # those attestations are False (not silently True).
            md = build_metadata(
                coverage_start, coverage_end,
                regime_boundary_handled=False,
                by_year_reported=False,
                state_status="unresolved",
                feasibility_class="F4",
                gdelt_normalization_files_status=PINNED_NORMALIZATION_STATUS,
                min_event_floor=min_event_floor,
                option_c_threshold=PINNED_OPTION_C_THRESHOLD,
                archive_layout_status=layout_status,
                option_c_enabled=PINNED_OPTION_C_ENABLED,
                post_run_safety_reset_required=post_run_safety_reset_required,
            )
            md["layout_report"] = layout
            md["stopped_before_count_computation"] = True
            md["by_year_counts_status"] = "not_computed"
            md["regime_boundary_status"] = "not_evaluated"
            md["stop_reason"] = layout_reason
            write_json(_checked_path(output_dir,
                                     "count_feasibility_metadata.json"), md)
            write_markdown(
                _checked_path(output_dir, "feasibility_summary.md"),
                "# Lane 2 count-only feasibility — F4 (archive layout)\n\n"
                "Stopped before count computation. {}\n\n"
                "F4 does not disprove the hypothesis; separate approval is "
                "required before any rerun.\n".format(layout_reason),
            )
            _assert_outputs_allowed(output_dir)
            return md

        # E/F. download + hash each unit via the injected opener.
        raw_dir = os.path.join(output_dir, "raw")
        os.makedirs(raw_dir, exist_ok=True)
        file_hashes: Dict[str, str] = {}
        file_sizes: Dict[str, int] = {}
        urls_per_unit: Dict[str, str] = {}
        local_paths: List[str] = []
        for e in plan:
            dest = os.path.join(raw_dir, e.filename)
            info = download_one(
                e.url, dest, e.rep_date,
                network_authorized=True, opener=opener,
            )
            file_hashes[e.key] = info["sha256"]
            file_sizes[e.key] = info["size_bytes"]
            urls_per_unit[e.key] = e.url
            local_paths.append(dest)

        # H/I. parse frozen files -> daily counts; parser aborts on any 2023+.
        per_file = [parse_gdelt1_file_daily_counts(p) for p in local_paths]
        daily = aggregate_daily_counts(per_file)

        # G. freeze manifest.
        manifest = build_freeze_manifest(
            coverage_start, coverage_end, units,
            file_hashes=file_hashes, urls_per_unit=urls_per_unit,
            file_sizes=file_sizes,
            gdelt_2013_regime_boundary_handled=True,
            gdelt_normalization_files_status=PINNED_NORMALIZATION_STATUS,
            min_event_floor=min_event_floor,
            option_c_threshold=PINNED_OPTION_C_THRESHOLD,
        )

        # J. missingness + by-year.
        miss = missingness_by_year(daily, coverage_start, coverage_end)
        byyr = by_year_counts(daily)

        # K/L. Option A & B spikes. M. Option C NOT computed (disabled).
        assert PINNED_OPTION_C_THRESHOLD is None and not PINNED_OPTION_C_ENABLED
        spikes_a = option_a_percentile_spikes(daily)
        spikes_b = option_b_zscore_spikes(daily)

        # N. clustering at 5/10/20 days for A and B.
        clusters: Dict[str, Dict[int, List[date]]] = {"A": {}, "B": {}}
        for sep in PINNED_CLUSTERING_DAYS:
            clusters["A"][sep] = cluster_spikes(spikes_a, sep)
            clusters["B"][sep] = cluster_spikes(spikes_b, sep)

        # O. overlap counts (hypothetical t+1:t+5 and t+1:t+20 windows).
        overlaps = []
        for opt, sp in (("A", spikes_a), ("B", spikes_b)):
            for lo, hi in ((1, 5), (1, 20)):
                r = event_window_overlap_count(sp, lo, hi)
                r["option"] = opt
                overlaps.append(r)

        # P. feasibility class. Primary floor = 10-day clustered count,
        # max over Option A / Option B.
        primary = max(
            len(clusters["A"][PINNED_PRIMARY_CLUSTER_DAYS]),
            len(clusters["B"][PINNED_PRIMARY_CLUSTER_DAYS]),
        )
        state = state_count_feasibility()  # unresolved: no market data
        cls, _note = assign_feasibility_class(
            source_found=True,
            raw_spike_count=primary,
            min_event_floor=min_event_floor,
            state_status=state["status"],
            reproducibility_ok=True,
            protocol_breach=False,
        )
        # F3 is unreachable here: state is unresolved by construction.

        conc = concentration_flags(
            daily, spikes_a + spikes_b,
            clusters["A"][PINNED_PRIMARY_CLUSTER_DAYS]
            + clusters["B"][PINNED_PRIMARY_CLUSTER_DAYS],
        )

        md = build_metadata(
            coverage_start, coverage_end, True, True,
            state["status"], cls,
            gdelt_normalization_files_status=PINNED_NORMALIZATION_STATUS,
            min_event_floor=min_event_floor,
            option_c_threshold=PINNED_OPTION_C_THRESHOLD,
            archive_layout_status=layout_status,
            option_c_enabled=PINNED_OPTION_C_ENABLED,
            post_run_safety_reset_required=post_run_safety_reset_required,
        )
        md["primary_10d_clustered_count"] = primary
        md["concentration_flags"] = conc
        md["layout_report"] = layout

        # Q. write ONLY allow-listed count artifacts (pre-write gated).
        write_json(_checked_path(output_dir,
                                 "source_freeze_manifest.json"), manifest)
        write_json(_checked_path(output_dir,
                                 "count_feasibility_metadata.json"), md)
        write_csv(
            _checked_path(output_dir, "daily_count_table.csv"),
            ["date", "event_count"],
            [[d.isoformat(), c] for d, c in sorted(daily.items())],
        )
        write_csv(
            _checked_path(output_dir, "missingness_table.csv"),
            ["year", "expected_days", "observed_days", "missing_days"],
            [[y, v["expected_days"], v["observed_days"], v["missing_days"]]
             for y, v in sorted(miss.items())],
        )
        write_csv(
            _checked_path(output_dir, "by_year_count_summary.csv"),
            ["year", "event_count"],
            [[y, c] for y, c in byyr.items()],
        )
        for opt, sp in (("a", spikes_a), ("b", spikes_b)):
            write_csv(
                _checked_path(output_dir,
                              "spike_counts_option_{}.csv".format(opt)),
                ["date"], [[d.isoformat()] for d in sp],
            )
        crows = []
        for opt in ("A", "B"):
            for sep in PINNED_CLUSTERING_DAYS:
                crows.append([opt, sep, len(clusters[opt][sep])])
        write_csv(
            _checked_path(output_dir, "clustering_counts.csv"),
            ["option", "separation_days", "clustered_count"], crows,
        )
        write_csv(
            _checked_path(output_dir, "overlap_counts.csv"),
            ["option", "window", "n_events", "overlapping_events",
             "overlap_fraction"],
            [[r["option"], r["window"], r["n_events"],
              r["overlapping_events"], r["overlap_fraction"]]
             for r in overlaps],
        )
        write_markdown(
            _checked_path(output_dir, "feasibility_summary.md"),
            "# Lane 2 GDELT 1.0 count-only feasibility summary\n\n"
            "Class: **{cls}** — {note}\n\n"
            "Primary 10-day clustered count (max A/B): {primary} "
            "(floor={floor}).\n\n"
            "State-count feasibility: {state} (no market data loaded).\n\n"
            "F3 does not confirm the hypothesis; F0/F1/F2/F4/F5 do not "
            "disprove it. Counts, availability, and clustering only — no "
            "returns, CAR, outcomes, models, p-values, or 2023+.\n".format(
                cls=cls, note=F_NOTES.get(cls, ""), primary=primary,
                floor=min_event_floor, state=state["status"],
            ),
        )
        _assert_outputs_allowed(output_dir)
        return md

    except Protocol2023PlusBreach as exc:
        # Any 2023+ breach -> F5 (protocol breach). Memo §10/§16. Counts/
        # by-year/regime work never completed on this path, so those
        # attestations are False. archive_layout_status carries provenance:
        # "not_checked" (breach before layout), "breach_during_check"
        # (breach aborted the layout check), or the real post-check token
        # (breach occurred after a clean layout pass).
        md = build_metadata(
            coverage_start, coverage_end,
            regime_boundary_handled=False,
            by_year_reported=False,
            state_status="unresolved",
            feasibility_class="F5",
            gdelt_normalization_files_status=PINNED_NORMALIZATION_STATUS,
            min_event_floor=min_event_floor,
            option_c_threshold=PINNED_OPTION_C_THRESHOLD,
            archive_layout_status=layout_status,
            option_c_enabled=PINNED_OPTION_C_ENABLED,
            post_run_safety_reset_required=post_run_safety_reset_required,
        )
        md["protocol_breach"] = str(exc)
        md["stopped_before_count_computation"] = True
        md["by_year_counts_status"] = "not_computed"
        md["regime_boundary_status"] = "not_evaluated"
        write_json(_checked_path(output_dir,
                                 "count_feasibility_metadata.json"), md)
        write_markdown(
            _checked_path(output_dir, "feasibility_summary.md"),
            "# Lane 2 count-only feasibility — F5 (protocol breach)\n\n"
            "{}\n\nF5 does not disprove the hypothesis. No rerun without a "
            "new authorization (memo §14).\n".format(exc),
        )
        _assert_outputs_allowed(output_dir)
        raise
