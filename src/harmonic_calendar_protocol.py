"""Harmonic calendar protocol orchestration (memo v0.3.3).

Pure-function orchestration: accepts already-split DataFrames and returns a
structured result dict. This module does NOT read files, does NOT make network
calls, and does NOT write artifacts. All I/O lives in the runner script.

The protocol implemented here is exactly the v0.3.3 locked protocol:

  * Two outcomes (log_return, log_return_sq) tested independently.
  * Primary calendar: March-20-anchored 108-phase.
  * Auxiliary control 1: January-anchored 108-phase.
  * Auxiliary control 2: Gregorian month (12 buckets).
  * Anchor-control null: EXHAUSTIVE enumeration of all 365 integer-DOY anchored
    108-phase calendars (DOY 1..365 inclusive), each evaluated exactly once.
    No random sampling; RANDOM_ANCHOR_SEED is not consumed.
  * Per-outcome verdict requires all three thresholds to pass:
      1. March20 PSS_in strictly beats at least 347 of 365 anchor calendars
         (ceil(0.95 * 365)). Ties do not help.
      2. March20 PSS_oos strictly beats at least 329 of 365 anchor calendars
         (ceil(0.90 * 365)) AND PSS_oos > 0. Ties do not help.
      3. March20 PSS_oos strictly exceeds both January-108 and Gregorian-month
         PSS_oos.
  * Secondary diagnostics (per-phase t-test + BH-FDR at q=0.05) computed only
    when the per-outcome verdict passes ("primary gate").
"""

from typing import Any, Dict, List, Sequence

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

from harmonic_calendar import (
    PHASE_CYCLE,
    RANDOM_ANCHOR_SEED,
    ANCHOR_CONTROL_POPULATION_SIZE,
    TRAINING_RANK_THRESHOLD,
    HOLDOUT_RANK_THRESHOLD,
    assign_march20_phase,
    assign_january_anchored_phase,
    assign_random_anchor_phase,
    assign_gregorian_month,
    enumerate_anchor_doys,
    strictly_below_count,
    strict_rank_pass,
    pss_in_sample,
    pss_out_of_sample,
)

OUTCOMES = ("log_return", "log_return_sq")
FDR_Q = 0.05
ACTIVE_MEMO_VERSION = "v0.3.3"

REQUIRED_COLUMNS = {"date", "log_return", "log_return_sq"}


# ── Statistical helpers ──────────────────────────────────────────────────────

def _strict_percentile(distribution: Sequence[float], target: float) -> float:
    """Strict-rank percentile of *target* within *distribution*, in [0, 1].

    Returns `strictly_below_count(target, distribution) / len(distribution)`.
    Locked v0.3.3 convention: ties are NOT counted as below the target.

    Reported for human readability only; pass/fail uses the integer rank
    thresholds via `strict_rank_pass`, not this float.
    """
    if len(distribution) == 0:
        raise ValueError("empty distribution")
    return strictly_below_count(target, distribution) / float(len(distribution))


def _benjamini_hochberg(pvalues: Sequence[float], q: float = FDR_Q) -> List[bool]:
    """BH-FDR rejection mask at level *q*. Returns booleans aligned with input order."""
    pvals = np.asarray(pvalues, dtype=float)
    m = pvals.size
    if m == 0:
        return []
    order = np.argsort(pvals)
    ranked = pvals[order]
    thresholds = (np.arange(1, m + 1, dtype=float) / m) * q
    below = ranked <= thresholds
    rejected = np.zeros(m, dtype=bool)
    if np.any(below):
        max_idx = int(np.max(np.where(below)[0]))
        rejected[order[: max_idx + 1]] = True
    return [bool(x) for x in rejected]


# ── Verdict rule ──────────────────────────────────────────────────────────────

def evaluate_outcome_verdict(
    march20_pss_in: float,
    march20_pss_oos: float,
    anchor_pss_in: Sequence[float],
    anchor_pss_oos: Sequence[float],
    gregorian_pss_oos: float,
    january_pss_oos: float,
    training_rank_threshold: int = TRAINING_RANK_THRESHOLD,
    holdout_rank_threshold: int = HOLDOUT_RANK_THRESHOLD,
) -> Dict[str, Any]:
    """Apply v0.3.3 per-outcome success criteria (finite-population rank).

    Verdict is "pass" iff *all three* gates clear:
      1. March20 PSS_in strictly beats at least `training_rank_threshold` of
         the anchor-control PSS_in population. Default 347 (= ceil(0.95 * 365)).
      2. March20 PSS_oos strictly beats at least `holdout_rank_threshold` of
         the anchor-control PSS_oos population. Default 329 (= ceil(0.90 * 365)).
         AND PSS_oos > 0 (positive in absolute terms).
      3. PSS_oos strictly exceeds both January-108 and Gregorian-month PSS_oos.

    Threshold parameters are exposed for synthetic-data unit testing only;
    production runs use the defaults bound to the locked v0.3.3 constants.
    Ties between March20 and an anchor calendar do NOT contribute to a pass.
    """
    if len(anchor_pss_in) == 0 or len(anchor_pss_oos) == 0:
        raise ValueError("empty anchor-control distribution")

    training_screen_pass = strict_rank_pass(
        march20_pss_in, anchor_pss_in, training_rank_threshold
    )
    holdout_pct_pass = strict_rank_pass(
        march20_pss_oos, anchor_pss_oos, holdout_rank_threshold
    )
    holdout_positive_pass = bool(march20_pss_oos > 0)
    holdout_primary_pass = holdout_pct_pass and holdout_positive_pass
    control_pass_gregorian = bool(march20_pss_oos > gregorian_pss_oos)
    control_pass_january = bool(march20_pss_oos > january_pss_oos)
    holdout_auxiliary_pass = control_pass_gregorian and control_pass_january

    verdict = "pass" if (
        training_screen_pass
        and holdout_primary_pass
        and holdout_auxiliary_pass
    ) else "null"

    return {
        "training_screen_pass": training_screen_pass,
        "holdout_pct_pass": holdout_pct_pass,
        "holdout_positive_pass": holdout_positive_pass,
        "holdout_primary_pass": holdout_primary_pass,
        "control_comparison_pass_gregorian": control_pass_gregorian,
        "control_comparison_pass_january": control_pass_january,
        "holdout_auxiliary_pass": holdout_auxiliary_pass,
        "verdict": verdict,
        "rank_thresholds": {
            "training_strictly_below_min": int(training_rank_threshold),
            "holdout_strictly_below_min": int(holdout_rank_threshold),
        },
        "march20_pss_in_strictly_below_count": int(
            strictly_below_count(march20_pss_in, anchor_pss_in)
        ),
        "march20_pss_oos_strictly_below_count": int(
            strictly_below_count(march20_pss_oos, anchor_pss_oos)
        ),
        "march20_pss_in_strict_percentile_vs_null": _strict_percentile(
            anchor_pss_in, march20_pss_in
        ),
        "march20_pss_oos_strict_percentile_vs_null": _strict_percentile(
            anchor_pss_oos, march20_pss_oos
        ),
        "anchor_control_population_size": int(len(anchor_pss_in)),
    }


# ── Secondary diagnostics (gated per outcome) ─────────────────────────────────

def compute_secondary_diagnostics(
    values: Sequence[float],
    phases: Sequence[int],
) -> Dict[str, Any]:
    """Per-phase mean t-test against grand mean + BH-FDR at q=0.05.

    Per memo v0.3.2: descriptive only. Computed only when an outcome's primary
    verdict passes ("primary gate"). The result records which phases (if any)
    carry observed structure in the training data.
    """
    values_arr = np.asarray(values, dtype=float)
    phases_arr = np.asarray(phases, dtype=int)
    grand_mean = float(np.mean(values_arr))
    n_total = int(values_arr.size)

    phase_records: List[Dict[str, Any]] = []
    for p in range(PHASE_CYCLE):
        mask = phases_arr == p
        n_p = int(mask.sum())
        if n_p == 0:
            continue
        y_p = values_arr[mask]
        mean_p = float(np.mean(y_p))
        record: Dict[str, Any] = {
            "phase": int(p),
            "n": n_p,
            "mean": mean_p,
        }
        if n_p < 2:
            record["p_value"] = None
        else:
            std_p = float(np.std(y_p, ddof=1))
            if std_p == 0.0:
                record["p_value"] = 1.0 if mean_p == grand_mean else 0.0
            else:
                t_stat = (mean_p - grand_mean) / (std_p / np.sqrt(n_p))
                record["p_value"] = float(
                    2.0 * scipy_stats.t.sf(abs(t_stat), df=n_p - 1)
                )
        phase_records.append(record)

    testable_idx = [i for i, r in enumerate(phase_records) if r["p_value"] is not None]
    rejected = _benjamini_hochberg(
        [phase_records[i]["p_value"] for i in testable_idx], q=FDR_Q
    )
    for i, rej in zip(testable_idx, rejected):
        phase_records[i]["fdr_rejected"] = bool(rej)
    for r in phase_records:
        r.setdefault("fdr_rejected", False)

    return {
        "computed": True,
        "method": "per-phase two-sided one-sample t-test against grand mean; BH-FDR q=0.05",
        "fdr_q": FDR_Q,
        "grand_mean": grand_mean,
        "n_total": n_total,
        "n_phases_with_data": len(phase_records),
        "n_phases_rejected": int(sum(1 for r in phase_records if r["fdr_rejected"])),
        "per_phase": phase_records,
    }


# ── Protocol entry point ──────────────────────────────────────────────────────

def _assign_static_phases(dates: Sequence) -> Dict[str, List[int]]:
    """Compute the three non-random calendar phase lists for *dates*."""
    return {
        "march20_108": [assign_march20_phase(d) for d in dates],
        "january_108": [assign_january_anchored_phase(d) for d in dates],
        "gregorian_month": [assign_gregorian_month(d) for d in dates],
    }


def _compute_calendar_pss(
    train_y: List[float],
    holdout_y: List[float],
    train_phases: List[int],
    holdout_phases: List[int],
) -> Dict[str, float]:
    return {
        "pss_in": pss_in_sample(train_y, train_phases),
        "pss_oos": pss_out_of_sample(train_y, train_phases, holdout_y, holdout_phases),
    }


def run_protocol(
    train_df: pd.DataFrame,
    holdout_df: pd.DataFrame,
) -> Dict[str, Any]:
    """Run the locked v0.3.3 protocol on already-split DataFrames.

    Both DataFrames must contain columns: date, log_return, log_return_sq.

    Uses the exhaustive 365-anchor enumeration (no random sampling). Applies
    the locked finite-population strict-rank thresholds (training 347,
    holdout 329). Returns a structured dict containing per-outcome verdicts,
    all PSS values (March20-108 / January-108 / Gregorian-month), the full
    365-anchor null distributions (pss_in and pss_oos per outcome), rank-based
    pass/fail flags with strict_percentiles for readability, control
    comparisons, and gated secondary diagnostics.
    """
    missing_train = REQUIRED_COLUMNS - set(train_df.columns)
    missing_holdout = REQUIRED_COLUMNS - set(holdout_df.columns)
    if missing_train:
        raise ValueError("train_df missing required columns: {}".format(sorted(missing_train)))
    if missing_holdout:
        raise ValueError("holdout_df missing required columns: {}".format(sorted(missing_holdout)))

    train_dates = list(train_df["date"])
    holdout_dates = list(holdout_df["date"])

    # Static-calendar phase assignments (once)
    train_phases = _assign_static_phases(train_dates)
    holdout_phases = _assign_static_phases(holdout_dates)

    # Per-outcome / per-calendar PSS for the three static calendars
    calendar_pss: Dict[str, Dict[str, Dict[str, float]]] = {o: {} for o in OUTCOMES}
    for outcome in OUTCOMES:
        train_y = list(train_df[outcome])
        holdout_y = list(holdout_df[outcome])
        for cal in ("march20_108", "january_108", "gregorian_month"):
            calendar_pss[outcome][cal] = _compute_calendar_pss(
                train_y, holdout_y, train_phases[cal], holdout_phases[cal]
            )

    # Anchor-control null (exhaustive enumeration, v0.3.3)
    anchor_doys = enumerate_anchor_doys()
    if len(anchor_doys) != ANCHOR_CONTROL_POPULATION_SIZE:
        raise ValueError(
            "enumerate_anchor_doys produced {} anchors, expected {}".format(
                len(anchor_doys), ANCHOR_CONTROL_POPULATION_SIZE
            )
        )

    train_y_by_outcome = {o: list(train_df[o]) for o in OUTCOMES}
    holdout_y_by_outcome = {o: list(holdout_df[o]) for o in OUTCOMES}

    anchor_null: Dict[str, Dict[str, List[float]]] = {
        o: {"pss_in": [], "pss_oos": []} for o in OUTCOMES
    }
    for anchor_doy in anchor_doys:
        train_p = [assign_random_anchor_phase(d, anchor_doy) for d in train_dates]
        holdout_p = [assign_random_anchor_phase(d, anchor_doy) for d in holdout_dates]
        for outcome in OUTCOMES:
            anchor_null[outcome]["pss_in"].append(
                pss_in_sample(train_y_by_outcome[outcome], train_p)
            )
            anchor_null[outcome]["pss_oos"].append(
                pss_out_of_sample(
                    train_y_by_outcome[outcome], train_p,
                    holdout_y_by_outcome[outcome], holdout_p,
                )
            )

    # Per-outcome verdicts and secondary diagnostics
    outcome_results: Dict[str, Any] = {}
    for outcome in OUTCOMES:
        march20 = calendar_pss[outcome]["march20_108"]
        gregorian = calendar_pss[outcome]["gregorian_month"]
        january = calendar_pss[outcome]["january_108"]

        verdict_info = evaluate_outcome_verdict(
            march20_pss_in=march20["pss_in"],
            march20_pss_oos=march20["pss_oos"],
            anchor_pss_in=anchor_null[outcome]["pss_in"],
            anchor_pss_oos=anchor_null[outcome]["pss_oos"],
            gregorian_pss_oos=gregorian["pss_oos"],
            january_pss_oos=january["pss_oos"],
        )

        if verdict_info["verdict"] == "pass":
            secondary = compute_secondary_diagnostics(
                values=train_y_by_outcome[outcome],
                phases=train_phases["march20_108"],
            )
        else:
            secondary = {
                "computed": False,
                "reason": "not computed because primary gate failed",
            }

        in_arr = np.asarray(anchor_null[outcome]["pss_in"], dtype=float)
        oos_arr = np.asarray(anchor_null[outcome]["pss_oos"], dtype=float)
        null_summary = {
            "n": int(in_arr.size),
            "pss_in_mean": float(np.mean(in_arr)),
            "pss_in_median": float(np.median(in_arr)),
            "pss_in_min": float(np.min(in_arr)),
            "pss_in_max": float(np.max(in_arr)),
            "pss_oos_mean": float(np.mean(oos_arr)),
            "pss_oos_median": float(np.median(oos_arr)),
            "pss_oos_min": float(np.min(oos_arr)),
            "pss_oos_max": float(np.max(oos_arr)),
        }

        outcome_results[outcome] = {
            "calendars": {
                "march20_108": march20,
                "january_108": january,
                "gregorian_month": gregorian,
            },
            "anchor_control_null_summary": null_summary,
            "anchor_control_null_full": {
                "anchor_doys": list(anchor_doys),
                "pss_in_values": list(anchor_null[outcome]["pss_in"]),
                "pss_oos_values": list(anchor_null[outcome]["pss_oos"]),
            },
            "march20_pss_in_strictly_below_count": verdict_info["march20_pss_in_strictly_below_count"],
            "march20_pss_oos_strictly_below_count": verdict_info["march20_pss_oos_strictly_below_count"],
            "march20_pss_in_strict_percentile_vs_null": verdict_info["march20_pss_in_strict_percentile_vs_null"],
            "march20_pss_oos_strict_percentile_vs_null": verdict_info["march20_pss_oos_strict_percentile_vs_null"],
            "training_screen_pass": verdict_info["training_screen_pass"],
            "holdout_pct_pass": verdict_info["holdout_pct_pass"],
            "holdout_positive_pass": verdict_info["holdout_positive_pass"],
            "holdout_primary_pass": verdict_info["holdout_primary_pass"],
            "control_comparison_pass_gregorian": verdict_info["control_comparison_pass_gregorian"],
            "control_comparison_pass_january": verdict_info["control_comparison_pass_january"],
            "holdout_auxiliary_pass": verdict_info["holdout_auxiliary_pass"],
            "verdict": verdict_info["verdict"],
            "secondary_diagnostics": secondary,
        }

    verdicts = {o: outcome_results[o]["verdict"] for o in OUTCOMES}
    n_pass = sum(1 for v in verdicts.values() if v == "pass")
    if n_pass == len(OUTCOMES):
        overall = "positive"
    elif n_pass == 0:
        overall = "null"
    else:
        overall = "partial_mixed"

    return {
        "active_memo_version": ACTIVE_MEMO_VERSION,
        "anchor_control_method": "exhaustive_enumeration_doy_1_to_365",
        "anchor_control_population_size": ANCHOR_CONTROL_POPULATION_SIZE,
        "training_rank_threshold": TRAINING_RANK_THRESHOLD,
        "holdout_rank_threshold": HOLDOUT_RANK_THRESHOLD,
        "random_anchor_seed_preserved": int(RANDOM_ANCHOR_SEED),
        "random_anchor_seed_consumed_by_control": False,
        "outcomes_tested": list(OUTCOMES),
        "train": {
            "n_rows": int(len(train_df)),
            "date_min": str(train_dates[0]),
            "date_max": str(train_dates[-1]),
        },
        "holdout": {
            "n_rows": int(len(holdout_df)),
            "date_min": str(holdout_dates[0]),
            "date_max": str(holdout_dates[-1]),
        },
        "outcomes": outcome_results,
        "per_outcome_verdicts": verdicts,
        "overall_summary": overall,
    }
