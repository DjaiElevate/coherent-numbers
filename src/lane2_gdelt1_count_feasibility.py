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
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Callable, Dict, List, Optional, Sequence, Tuple

# ── Governance constants ──────────────────────────────────────────────────────

GOVERNING_PROTOCOL_COMMIT = "147c0d40568636ba0cf24ca00cc39c330e77ea03"
AUTHORIZATION_COMMIT = "8fef80db0e103d2c22e36d589fe041abd1fb4c78"
SELECTED_SOURCE = "GDELT 1.0 Event database"

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
) -> Dict[str, object]:
    if coverage_end >= SEAL_START:
        raise Protocol2023PlusBreach("metadata coverage_end is 2023+")
    if gdelt_normalization_files_status not in NORMALIZATION_STATUS_VALUES:
        raise ValueError(
            "gdelt_normalization_files_status must be one of {}; got {!r}".format(
                NORMALIZATION_STATUS_VALUES, gdelt_normalization_files_status
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

# Visible (not hidden) documentation-level GDELT 1.0 base URL. The exact
# remote layout MUST be verified at freeze time; this is overridable.
DEFAULT_GDELT1_BASE_URL = "http://data.gdeltproject.org/events/"

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
