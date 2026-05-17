"""Human Field x Base-12 Pullback Atlas v0.1 — exploratory atlas (Lane 1 only).

Governing artifacts
===================
- docs/human_field_base12_pullback_atlas_design_memo_v0.1.md (v0.1, revised 2026-05-17)
- docs/human_field_base12_pullback_atlas_implementation_plan_v0.1.md (v0.1)

This module is EXPLORATORY ATLAS MODE. It is not a confirmatory cell. It
computes no p-value, no permutation null, no beat count, no verdict. It does
not interpret results. It produces full descriptive grids only. "No coherent
joint structure" (Candidate H0) is an equal-weight outcome, never a fallback.

Hard boundaries enforced in code
================================
- Single anchor only. Phase labels come from
  candidate_c_lens.assign_annual_sector_phase (design memo 7.1, civil-date
  March-20). candidate_c_lens.assign_anchor_shifted_phase (the 365-DOY
  surface, 7.2) is deliberately NOT imported or referenced here.
- r_multiple is the only outcome (Decision 2). No fixed-horizon outcome.
- No post-2022 row is used in any computation. The SPY auxiliary frame is
  filtered to MAX_PERMITTED_FEATURE_DATE BEFORE any feature is constructed.
- Missing/insufficient state data -> reserved 'indeterminate-state' label
  (Decision 3); retained in grids, excluded from narrative/hypothesis work.

This module performs NO data loading at import time. The canonical run path
(preflight + real frozen substrate) is invoked only by the run script and
only under explicit authorization. Pure feature/grid/PSS functions are unit
tested with synthetic fixtures.
"""

from __future__ import annotations

import bisect
import math
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np

# Audited infrastructure reuse. Importing assign_annual_sector_phase ONLY;
# assign_anchor_shifted_phase is intentionally not imported (Decision 1).
from candidate_c_lens import assign_annual_sector_phase
from candidate_c_pss import DegenerateLongShareError, pss_long_share
from candidate_b_loader import (
    FREEZE_MANIFEST_PATH,
    PHASE3B_DATASETS,
    ReducedTrades,
    load_reduced_phase3b_pool,
    verify_frozen_inputs,
)

# ── Provenance / governance constants ─────────────────────────────────────────

DESIGN_MEMO_PATH = "docs/human_field_base12_pullback_atlas_design_memo_v0.1.md"
IMPLEMENTATION_PLAN_PATH = (
    "docs/human_field_base12_pullback_atlas_implementation_plan_v0.1.md"
)
CANDIDATE_C_REFERENCES = {
    "design_memo": "401ce45 docs/candidate_c_design_memo_v0.1.md",
    "lock_acceptance": "dc97576 docs/candidate_c_design_memo_v0.1_lock_acceptance.md",
    "verdict_log": (
        "a19b2e9 results/candidate_c_results_20260515_051236_f3a6bf48.{json,md}"
    ),
    "closure_memo": "1659819 docs/candidate_c_closure_memo_v0.1.md",
    "phase_label_source": "src/candidate_c_lens.py::assign_annual_sector_phase",
}
FREEZE_MANIFEST_REFERENCE = "{} @ 5225bfd".format(FREEZE_MANIFEST_PATH)
SPY_FROZEN_CSV = (
    "data/raw/spy_yahoo_v8_19930129_20241231_"
    "e8fc0357410ce499da8f67e09b4c9908232e18a55445f38969e77fa712aaaa56.csv"
)
SPY_ARTIFACT_REFERENCE = "{} @ ed199bd".format(SPY_FROZEN_CSV)

# Substrate expectations (freeze manifest 5225bfd).
EXPECTED_ASSET_COUNTS: Dict[str, int] = {
    "SPY": 243,
    "EFA": 283,
    "EEM": 261,
    "GLD": 253,
    "TLT": 242,
}
EXPECTED_POOLED_ROW_COUNT = 1282

# Date bounds. Latest frozen pullback entry_date is 2022-12-21. Features end at
# t-1, so the latest auxiliary feature date is 2022-12-20.
MAX_PERMITTED_EVENT_ENTRY_DATE = date(2022, 12, 21)
MAX_PERMITTED_FEATURE_DATE = date(2022, 12, 20)

# Locked windows / thresholds (design memo 8). Not parameters of this code.
RETURN_WINDOW_SESSIONS = 30
RVOL_WINDOW_SESSIONS = 20
RVOL_PCTILE_WINDOW_SESSIONS = 252
# Locked sample-volatility convention (design memo 8.2). ddof=1. Because the
# realized-vol window is a fixed 20 sessions, changing ddof would multiply
# every rolling-vol value by a constant factor and therefore would not change
# percentile ranks under complete fixed-length windows. Not an open question.
RVOL_STD_DDOF = 1
AROUSAL_PCTILE_THRESHOLD = 0.75
LOW_DATA_THRESHOLD = 20

BASE12 = 12
BASE10 = 10

# Fixed display orders (design memo 11 / implementation plan 6).
STATE_CALM_BULL = "calm bull"
STATE_MANIC = "manic / unstable rally"
STATE_PANIC = "panic / crisis"
STATE_QUIET_BEAR = "quiet bearish / exhaustion"
STATE_INDETERMINATE = "indeterminate-state"
STATE_ORDER: Tuple[str, ...] = (
    STATE_CALM_BULL,
    STATE_MANIC,
    STATE_PANIC,
    STATE_QUIET_BEAR,
    STATE_INDETERMINATE,
)
ASSET_ORDER: Tuple[str, ...] = ("SPY", "EFA", "EEM", "GLD", "TLT")

# NA sentinel. Honest missing value; never silently coerced to 0.0.
NA = None


class ImplementationCheckFailed(RuntimeError):
    """Raised when a canonical-run preflight check fails.

    Per the design memo's QA rule: a non-zero indeterminate-state count, a
    substrate-shape mismatch, or any date-bound violation aborts the canonical
    run rather than silently proceeding to a candidate-hypothesis summary.
    """


# ── SPY auxiliary frame (bounded BEFORE feature construction) ──────────────────

@dataclass(frozen=True)
class SpyFrame:
    """Bounded, ascending SPY session series used for both state axes.

    `dates` is strictly ascending and contains no date past
    MAX_PERMITTED_FEATURE_DATE: the frame is truncated at construction, before
    any feature is read, so no post-2022 row can enter any computation.
    """

    dates: List[date]
    adj_close: np.ndarray
    log_return: np.ndarray

    def __len__(self) -> int:
        return len(self.dates)

    def session_index_strictly_before(self, day: date) -> Optional[int]:
        """Index of the last session strictly before `day`, or None."""
        pos = bisect.bisect_left(self.dates, day)
        if pos == 0:
            return None
        return pos - 1


def build_spy_frame(
    raw_dates: Sequence[date],
    raw_adj_close: Sequence[float],
    raw_log_return: Sequence[float],
    max_feature_date: date = MAX_PERMITTED_FEATURE_DATE,
) -> SpyFrame:
    """Build a bounded SPY frame, filtering to date <= max_feature_date first.

    The truncation happens here, before any windowing, so the structural
    guarantee ("no post-2022 row used in any computation") holds regardless of
    how far the frozen artifact extends. A post-filter assertion enforces it.
    """
    rows = sorted(
        zip(
            [_as_date(d) for d in raw_dates],
            [float(x) for x in raw_adj_close],
            [float(x) for x in raw_log_return],
        ),
        key=lambda r: r[0],
    )
    kept = [r for r in rows if r[0] <= max_feature_date]
    if kept:
        max_kept = max(r[0] for r in kept)
        if max_kept > max_feature_date:  # defensive; cannot happen post-filter
            raise ImplementationCheckFailed(
                "SPY frame retains a row past {}: {}".format(
                    max_feature_date, max_kept
                )
            )
    dates = [r[0] for r in kept]
    if any(dates[i] >= dates[i + 1] for i in range(len(dates) - 1)):
        raise ValueError("SPY session dates must be strictly ascending/unique")
    return SpyFrame(
        dates=dates,
        adj_close=np.asarray([r[1] for r in kept], dtype=np.float64),
        log_return=np.asarray([r[2] for r in kept], dtype=np.float64),
    )


def _as_date(value) -> date:
    if isinstance(value, date) and not hasattr(value, "hour"):
        return value
    if hasattr(value, "date") and callable(value.date):
        return value.date()
    if isinstance(value, date):
        return value
    raise TypeError("unsupported date value: {!r}".format(value))


# ── State-axis features (all windows end at t-1; never include the event day) ──

@dataclass(frozen=True)
class StateFeatures:
    prior_30d_return: Optional[float]
    realized_vol_20d: Optional[float]
    realized_vol_pctile_252: Optional[float]
    state: str
    indeterminate_reason: Optional[str]


def empirical_cdf_pctile(trailing: Sequence[float], current: float) -> float:
    """Q2: fraction of trailing values strictly less than `current`.

    Deterministic empirical CDF. Denominator is the trailing count.
    """
    if not trailing:
        raise ValueError("empirical_cdf_pctile requires a non-empty trailing window")
    strictly_less = sum(1 for v in trailing if v < current)
    return strictly_less / float(len(trailing))


def is_high_arousal(pctile: float) -> bool:
    """High arousal iff percentile >= AROUSAL_PCTILE_THRESHOLD (0.75)."""
    return pctile >= AROUSAL_PCTILE_THRESHOLD


def _realized_vol_at(spy: SpyFrame, pos: int) -> Optional[float]:
    """Sample std (ddof=1) of log_return over the 20 sessions ending at pos."""
    lo = pos - (RVOL_WINDOW_SESSIONS - 1)
    if lo < 0:
        return None
    window = spy.log_return[lo : pos + 1]
    if window.shape[0] != RVOL_WINDOW_SESSIONS:
        return None
    return float(np.std(window, ddof=RVOL_STD_DDOF))


def compute_state_features(spy: SpyFrame, entry_date: date) -> StateFeatures:
    """Compute valence/arousal and the nervous-system state for one event.

    All windows terminate at t-1 (the last session strictly before
    entry_date). If any required window cannot be fully populated from
    sessions <= t-1, the event is 'indeterminate-state' with a recorded
    reason. No future leakage: the event day is never read.
    """
    pos = spy.session_index_strictly_before(entry_date)
    if pos is None:
        return StateFeatures(
            None, None, None, STATE_INDETERMINATE, "no_session_before_entry_date"
        )

    # Valence: 30-session simple return ending at t-1.
    ret_lo = pos - RETURN_WINDOW_SESSIONS
    if ret_lo < 0:
        return StateFeatures(
            None, None, None, STATE_INDETERMINATE, "insufficient_return_history"
        )
    base_px = spy.adj_close[ret_lo]
    if not math.isfinite(base_px) or base_px <= 0:
        return StateFeatures(
            None, None, None, STATE_INDETERMINATE, "invalid_base_price"
        )
    prior_30d_return = float(spy.adj_close[pos] / base_px - 1.0)

    # Arousal: 20-session realized vol at t-1, percentile within the 252
    # strictly-trailing realized-vol values (positions pos-252 .. pos-1).
    rvol_now = _realized_vol_at(spy, pos)
    if rvol_now is None:
        return StateFeatures(
            prior_30d_return, None, None,
            STATE_INDETERMINATE, "insufficient_rvol_history",
        )
    trailing: List[float] = []
    for p in range(pos - RVOL_PCTILE_WINDOW_SESSIONS, pos):
        if p < 0:
            return StateFeatures(
                prior_30d_return, rvol_now, None,
                STATE_INDETERMINATE, "insufficient_rvol_pctile_history",
            )
        rv = _realized_vol_at(spy, p)
        if rv is None:
            return StateFeatures(
                prior_30d_return, rvol_now, None,
                STATE_INDETERMINATE, "insufficient_rvol_pctile_history",
            )
        trailing.append(rv)
    if len(trailing) != RVOL_PCTILE_WINDOW_SESSIONS:
        return StateFeatures(
            prior_30d_return, rvol_now, None,
            STATE_INDETERMINATE, "insufficient_rvol_pctile_history",
        )

    # Q2: empirical CDF — fraction of trailing values strictly less than now.
    pctile = empirical_cdf_pctile(trailing, rvol_now)

    positive_valence = prior_30d_return > 0.0
    high_arousal = is_high_arousal(pctile)
    if positive_valence and not high_arousal:
        state = STATE_CALM_BULL
    elif positive_valence and high_arousal:
        state = STATE_MANIC
    elif (not positive_valence) and high_arousal:
        state = STATE_PANIC
    else:
        state = STATE_QUIET_BEAR
    return StateFeatures(prior_30d_return, rvol_now, pctile, state, None)


# ── Per-event feature record ──────────────────────────────────────────────────

@dataclass(frozen=True)
class AtlasEvent:
    trade_id: int
    asset: str
    entry_date: date
    is_long: bool
    r_multiple: float
    base12_phase: int
    base10_phase: int
    prior_30d_return: Optional[float]
    realized_vol_20d: Optional[float]
    realized_vol_pctile_252: Optional[float]
    state: str
    indeterminate_reason: Optional[str]


def build_events(trades: ReducedTrades, spy: SpyFrame) -> List[AtlasEvent]:
    """Attach phase labels and nervous-system state to each frozen trade.

    Phases use the single March-20 anchor only (assign_annual_sector_phase).
    """
    events: List[AtlasEvent] = []
    for i in range(len(trades)):
        ed = _as_date(trades.entry_date[i])
        sf = compute_state_features(spy, ed)
        events.append(
            AtlasEvent(
                trade_id=int(trades.trade_id[i]),
                asset=str(trades.asset[i]),
                entry_date=ed,
                is_long=bool(trades.is_long[i]),
                r_multiple=float(trades.r_multiple[i]),
                base12_phase=assign_annual_sector_phase(ed, BASE12),
                base10_phase=assign_annual_sector_phase(ed, BASE10),
                prior_30d_return=sf.prior_30d_return,
                realized_vol_20d=sf.realized_vol_20d,
                realized_vol_pctile_252=sf.realized_vol_pctile_252,
                state=sf.state,
                indeterminate_reason=sf.indeterminate_reason,
            )
        )
    return events


# ── Grids (full cartesian; every cell carries n + low_data + honest NA) ────────

@dataclass(frozen=True)
class Cell:
    keys: Tuple
    n: int
    value: Optional[float]
    low_data: bool

    @property
    def marker(self) -> str:
        return "LOW_DATA" if self.low_data else ""


def _median(values: Sequence[float]) -> Optional[float]:
    """Standard median; for even n, average of the two middle values (Q6)."""
    xs = sorted(values)
    n = len(xs)
    if n == 0:
        return NA
    mid = n // 2
    if n % 2 == 1:
        return float(xs[mid])
    return float((xs[mid - 1] + xs[mid]) / 2.0)


def _long_pct(events: Sequence[AtlasEvent]) -> Optional[float]:
    if not events:
        return NA
    return 100.0 * sum(1 for e in events if e.is_long) / len(events)


def _phase_states_grid(
    events: Sequence[AtlasEvent],
    phase_attr: str,
    n_phases: int,
    reducer,
) -> List[Cell]:
    """Full phase x state grid, every combination emitted (including empty)."""
    bucket: Dict[Tuple[int, str], List[AtlasEvent]] = {}
    for e in events:
        bucket.setdefault((getattr(e, phase_attr), e.state), []).append(e)
    cells: List[Cell] = []
    for phase in range(n_phases):
        for state in STATE_ORDER:
            grp = bucket.get((phase, state), [])
            n = len(grp)
            cells.append(
                Cell(
                    keys=(phase, state),
                    n=n,
                    value=reducer(grp),
                    low_data=n < LOW_DATA_THRESHOLD,
                )
            )
    return cells


def grid1_event_count(events) -> List[Cell]:
    return _phase_states_grid(events, "base12_phase", BASE12, lambda g: float(len(g)))


def grid2_long_pct(events) -> List[Cell]:
    return _phase_states_grid(events, "base12_phase", BASE12, _long_pct)


def grid3_median_r(events) -> List[Cell]:
    return _phase_states_grid(
        events, "base12_phase", BASE12, lambda g: _median([e.r_multiple for e in g])
    )


def _pss_or_na(events: Sequence[AtlasEvent], phase_attr: str, n_phases: int):
    """Eta-squared/PSS for one event group; honest NA on degeneracy/empty (Q5).

    Reuses the audited candidate_c_pss.pss_long_share. No null, no permutation,
    no beat count, no verdict — the eta-squared form only.
    """
    if not events:
        return NA
    is_long = np.asarray([e.is_long for e in events], dtype=bool)
    phase = np.asarray([getattr(e, phase_attr) for e in events], dtype=np.int64)
    try:
        return float(pss_long_share(is_long, phase, n_phases))
    except DegenerateLongShareError:
        return NA  # total variance zero -> undefined, never silently 0.0


def grid4_state_pss(events) -> List[Dict[str, object]]:
    """State-level PSS_12 vs PSS_10, side by side, descriptive only."""
    rows: List[Dict[str, object]] = []
    by_state: Dict[str, List[AtlasEvent]] = {s: [] for s in STATE_ORDER}
    for e in events:
        by_state[e.state].append(e)
    for state in STATE_ORDER:
        grp = by_state[state]
        rows.append(
            {
                "state": state,
                "n": len(grp),
                "pss_12": _pss_or_na(grp, "base12_phase", BASE12),
                "pss_10": _pss_or_na(grp, "base10_phase", BASE10),
                "low_data": len(grp) < LOW_DATA_THRESHOLD,
            }
        )
    return rows


def grid5_asset_phase_state(events) -> List[Cell]:
    """Diagnostic, expected predominantly low-data (~5 trades/cell)."""
    bucket: Dict[Tuple[str, int, str], List[AtlasEvent]] = {}
    for e in events:
        bucket.setdefault((e.asset, e.base12_phase, e.state), []).append(e)
    cells: List[Cell] = []
    for asset in ASSET_ORDER:
        for phase in range(BASE12):
            for state in STATE_ORDER:
                grp = bucket.get((asset, phase, state), [])
                n = len(grp)
                cells.append(
                    Cell(
                        keys=(asset, phase, state),
                        n=n,
                        value=_long_pct(grp),
                        low_data=n < LOW_DATA_THRESHOLD,
                    )
                )
    return cells


def grid6_direction_splits(events) -> Dict[str, Dict[str, List[Cell]]]:
    longs = [e for e in events if e.is_long]
    shorts = [e for e in events if not e.is_long]
    return {
        "long_only": {
            "count": grid1_event_count(longs),
            "long_pct": grid2_long_pct(longs),
            "median_r": grid3_median_r(longs),
        },
        "short_only": {
            "count": grid1_event_count(shorts),
            "long_pct": grid2_long_pct(shorts),
            "median_r": grid3_median_r(shorts),
        },
    }


def grid7_sparsity_report(named_grids: Mapping[str, Sequence[Cell]]) -> List[Dict]:
    report: List[Dict] = []
    for name, cells in named_grids.items():
        total_cells = len(cells)
        low = [c for c in cells if c.low_data]
        total_events = sum(c.n for c in cells)
        below_events = sum(c.n for c in low)
        report.append(
            {
                "grid": name,
                "total_cells": total_cells,
                "low_data_cells": len(low),
                "fraction_events_in_low_data_cells": (
                    below_events / total_events if total_events else NA
                ),
            }
        )
    return report


def grid8_base10_views(events) -> Dict[str, object]:
    """Base-10 comparator views matching base-12 (Candidate C comparator only).

    Presented strictly as Candidate C's comparator, never as an additional
    search surface.
    """
    return {
        "count": _phase_states_grid(
            events, "base10_phase", BASE10, lambda g: float(len(g))
        ),
        "long_pct": _phase_states_grid(
            events, "base10_phase", BASE10, _long_pct
        ),
        "median_r": _phase_states_grid(
            events, "base10_phase", BASE10,
            lambda g: _median([e.r_multiple for e in g]),
        ),
        "state_pss": grid4_state_pss(events),  # already reports pss_10 alongside
    }


def indeterminate_count(events: Sequence[AtlasEvent]) -> int:
    return sum(1 for e in events if e.state == STATE_INDETERMINATE)


# ── Substrate validation / preflight (canonical run only) ──────────────────────

def validate_substrate(trades: ReducedTrades) -> None:
    """Row-count, asset-count and date-bound checks. Abort on any failure."""
    if len(trades) != EXPECTED_POOLED_ROW_COUNT:
        raise ImplementationCheckFailed(
            "pooled row count {} != expected {}".format(
                len(trades), EXPECTED_POOLED_ROW_COUNT
            )
        )
    counts: Dict[str, int] = {}
    for a in trades.asset:
        counts[str(a)] = counts.get(str(a), 0) + 1
    if counts != EXPECTED_ASSET_COUNTS:
        raise ImplementationCheckFailed(
            "asset counts {} != expected {}".format(counts, EXPECTED_ASSET_COUNTS)
        )
    max_entry = max(_as_date(d) for d in trades.entry_date)
    if max_entry > MAX_PERMITTED_EVENT_ENTRY_DATE:
        raise ImplementationCheckFailed(
            "latest entry_date {} exceeds permitted {}".format(
                max_entry, MAX_PERMITTED_EVENT_ENTRY_DATE
            )
        )


def preflight(trades: ReducedTrades, spy: SpyFrame, events: Sequence[AtlasEvent]):
    """Run all pre-run checks. Returns (methodological_status, details).

    A non-zero indeterminate count is a QA warning that, per the design memo,
    blocks any candidate-hypothesis summary: methodological_status is set to
    'implementation_check_failed' and the caller must not proceed silently.
    """
    validate_substrate(trades)
    if spy.dates and max(spy.dates) > MAX_PERMITTED_FEATURE_DATE:
        raise ImplementationCheckFailed(
            "SPY frame exceeds permitted feature date bound"
        )
    n_indet = indeterminate_count(events)
    details = {
        "row_count": len(trades),
        "indeterminate_count": n_indet,
        "indeterminate_reasons": sorted(
            {
                e.indeterminate_reason
                for e in events
                if e.indeterminate_reason is not None
            }
        ),
    }
    if n_indet > 0:
        details["qa_warning"] = (
            "indeterminate_count > 0 — expected ~0 for the 2005-2022 pullback "
            "population given SPY history from 1993; explicit review required "
            "before any candidate-hypothesis summary."
        )
        return "implementation_check_failed", details
    return "ok", details


# ── Metadata scaffolding ──────────────────────────────────────────────────────

def build_metadata(
    timestamp_utc: str,
    observed_hashes: Mapping[str, str],
    row_count: int,
    asset_counts: Mapping[str, int],
    methodological_status: str,
    indeterminate_n: int,
) -> Dict[str, object]:
    return {
        "design_memo_path": DESIGN_MEMO_PATH,
        "implementation_plan_path": IMPLEMENTATION_PLAN_PATH,
        "candidate_c_references": dict(CANDIDATE_C_REFERENCES),
        "freeze_manifest_reference": FREEZE_MANIFEST_REFERENCE,
        "spy_artifact_reference": SPY_ARTIFACT_REFERENCE,
        "latest_permitted_feature_date": str(MAX_PERMITTED_FEATURE_DATE),
        "latest_permitted_event_entry_date": str(MAX_PERMITTED_EVENT_ENTRY_DATE),
        "row_count_verified": row_count == EXPECTED_POOLED_ROW_COUNT,
        "asset_counts_verified": dict(asset_counts) == EXPECTED_ASSET_COUNTS,
        "observed_frozen_hashes": dict(observed_hashes),
        "indeterminate_count": indeterminate_n,
        "methodological_status": methodological_status,
        "timestamp_utc": timestamp_utc,
        "rvol_std_ddof": RVOL_STD_DDOF,
        "exploratory_atlas_only": True,
        "verdict_language_allowed": False,
        "confirmation_claim_allowed": False,
        "post_2022_rows_used_in_computation": False,
        "post_2022_note": (
            "No post-2022 rows were used in any atlas computation. The SPY "
            "auxiliary frame was filtered to the maximum permitted feature "
            "date before feature construction."
        ),
        "lane2_attention_spike_study_included": False,
        "no_oos_analysis": True,
    }


CLOSURE_MEMO_FIXED_BOILERPLATE = """\
# Human Field x Base-12 Pullback Atlas — Closure Memo v0.1 (boilerplate)

Status: fixed sealed-data / no-verdict boilerplate, authored at implementation
time. Descriptive observations are added ONLY after a separately authorized
atlas run. None are present here.

Sealed-data framing (fixed before any atlas generation):
(a) The atlas itself does not validate anything.
(b) Hypotheses generated are discovery-seeded.
(c) Confirmation requires data not used in the atlas.
(d) Within the existing audit chain, the natural confirmatory set is the 2023+
    sealed data; using it for any atlas-generated hypothesis is a deliberate
    decision that consumes part of the seal for that specific question.

Candidate H0 (no coherent joint structure) is an equal-weight outcome, never a
fallback. No verdict, p-value-as-evidence, rescue, profitability, OOS, or
confirmation claim appears in any atlas artifact.
"""
