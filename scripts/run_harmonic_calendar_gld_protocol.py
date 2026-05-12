"""GLD verdict run — single locked execution of the v0.1 GLD harmonic calendar protocol.

This script is the SINGLE OFFICIAL invocation of the locked protocol against
the frozen GLD CSV for the Harmonic Calendar × GLD cell.

Active cell memo:    docs/harmonic_calendar_gld_v0.1.md   (commit 11b00d6)
Inherited lens:      harmonic_calendar_protocol v0.3.3    (commit 30faabb)
Data freeze:         commit 4dc56c4
GLD loader:          commit 87e5578

It reads:
  data/raw/gld_yahoo_v8_20041118_20241231_<sha256>.csv
  docs/harmonic_calendar_gld_v0.1.md   (active locked cell memo)

It writes:
  results/harmonic_calendar_gld_results_<run_date>_<hashprefix>.json
  results/harmonic_calendar_gld_results_<run_date>_<hashprefix>.md

No live network calls. No Yahoo fetching. The canonical loader load_gld() is
the only data entry point, and it reads from the frozen local CSV only.

The anchor-control null is the deterministic exhaustive enumeration of all 365
integer-DOY anchors (v0.3.3). No random sampling. RANDOM_ANCHOR_SEED is not
consumed by this run.

Re-running this script after the verdict has been committed would constitute
a protocol violation.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import subprocess
import sys
from typing import Any, Dict, List

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

from gld_loader import load_gld, make_train_holdout_split  # noqa: E402
from harmonic_calendar import (  # noqa: E402
    ANCHOR_CONTROL_POPULATION_SIZE,
    RANDOM_ANCHOR_SEED,
    TRAINING_RANK_THRESHOLD,
    HOLDOUT_RANK_THRESHOLD,
)
from harmonic_calendar_protocol import (  # noqa: E402
    ACTIVE_MEMO_VERSION as HCP_ACTIVE_MEMO_VERSION,
    OUTCOMES,
    run_protocol,
)

ASSET = "GLD"
GLD_ACTIVE_MEMO_VERSION = "v0.1"
INHERITED_LENS_VERSION = HCP_ACTIVE_MEMO_VERSION  # "v0.3.3"

GLD_VERDICT_H1 = "Harmonic Calendar × GLD — v0.1 Verdict"

FROZEN_CSV_PATH = os.path.join(
    REPO_ROOT,
    "data",
    "raw",
    "gld_yahoo_v8_20041118_20241231_"
    "368fe45094eafa277c81accd2c71b2b593ddcf917c29c7b269de088a31fd1b2c.csv",
)
EXPECTED_CSV_SHA256 = (
    "368fe45094eafa277c81accd2c71b2b593ddcf917c29c7b269de088a31fd1b2c"
)
ACTIVE_MEMO_PATH = os.path.join(
    REPO_ROOT, "docs", "harmonic_calendar_gld_v0.1.md"
)
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
RUN_DATE_TAG = "20260512"
HASH_PREFIX = EXPECTED_CSV_SHA256[:8]

RAW_DESIGN_DATA_RANGE = "2004-11-18 through 2024-12-31"
DESIGN_TRAINING_RULE = "GLD inception through 2014-12-31"

_TRAINING_POWER_CAVEAT = (
    "Training-power caveat (pre-registered in design memo v0.1): "
    "The GLD training window is approximately 10.1 years "
    "(effective loaded first return: 2004-11-19, through 2014-12-31), "
    "versus approximately 22 years for the SPY cell "
    "(effective loaded first return: 1993-02-01, through 2014-12-31). "
    "The strict-rank convention is identical across cells "
    "(March20 must beat 347 of 365 anchors in training, 329 of 365 in holdout). "
    "Per-anchor PSS estimates are noisier on GLD's shorter training window. "
    "This asymmetry is accepted as a limitation of the GLD cell and must be "
    "considered when comparing GLD verdicts to SPY verdicts. "
    "A null verdict on GLD carries less power than a null verdict on SPY. "
    "A positive verdict on GLD would be directly interpretable against the "
    "holdout window, which is matched in length to SPY's holdout (2015-2024)."
)


def _file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_head_commit(repo: str) -> str:
    out = subprocess.check_output(
        ["git", "-C", repo, "rev-parse", "HEAD"], stderr=subprocess.STDOUT
    )
    return out.decode("utf-8").strip()


def _format_markdown(payload: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Harmonic Calendar × GLD — v0.1 Verdict")
    lines.append("")
    lines.append("**Project:** Coherent Numbers")
    lines.append("**Asset:** {}".format(payload["asset"]))
    lines.append(
        "**Active cell memo:** `{}` ({})".format(
            payload["active_memo_path"], payload["active_memo_version"]
        )
    )
    lines.append(
        "**Inherited lens version:** {} (harmonic_calendar_protocol)".format(
            payload["inherited_lens_version"]
        )
    )
    lines.append(
        "**Repo commit before run:** `{}`".format(payload["repo_commit_before_run"])
    )
    lines.append("**Run timestamp (UTC):** {}".format(payload["run_timestamp_utc"]))
    lines.append("**Frozen CSV:** `{}`".format(payload["frozen_csv_path"]))
    lines.append("**Frozen CSV SHA256:** `{}`".format(payload["frozen_csv_sha256"]))
    lines.append("**Loader:** `{}`".format(payload["loader"]))
    lines.append(
        "**Anchor-control:** exhaustive enumeration, "
        "{} integer-DOY anchors (1..365)".format(
            payload["anchor_control_population_size"]
        )
    )
    lines.append(
        "**Rank thresholds:** training strictly_below ≥ "
        "{} (= ceil(0.95 × 365)); "
        "holdout strictly_below ≥ {} "
        "(= ceil(0.90 × 365))".format(
            payload["training_rank_threshold"],
            payload["holdout_rank_threshold"],
        )
    )
    lines.append(
        "**Seed (preserved, not consumed):** RANDOM_ANCHOR_SEED = {}".format(
            payload["random_anchor_seed_preserved"]
        )
    )
    lines.append("")

    lines.append("## Data ranges")
    lines.append("")
    lines.append(
        "- Raw/design data range: {} (2004-11-18 = GLD inception; "
        "2024-12-31 = freeze terminus, matching SPY cell)".format(
            payload["raw_design_data_range"]
        )
    )
    lines.append(
        "- Design training rule: {} "
        "(first-row log-return drop means effective loaded first return = 2004-11-19)".format(
            payload["design_training_rule"]
        )
    )
    lines.append(
        "- Effective loaded training date range used for PSS: {}".format(
            payload["effective_loaded_training_date_range"]
        )
    )
    lines.append(
        "- Effective loaded holdout date range used for PSS: {}".format(
            payload["effective_loaded_holdout_date_range"]
        )
    )
    lines.append(
        "- Loaded rows: {} (training: {}, holdout: {})".format(
            payload["row_counts"]["loaded"],
            payload["row_counts"]["train"],
            payload["row_counts"]["holdout"],
        )
    )
    lines.append("")

    lines.append("## Training-power caveat (pre-registered)")
    lines.append("")
    lines.append(_TRAINING_POWER_CAVEAT)
    lines.append("")

    lines.append("## Per-outcome verdicts")
    lines.append("")
    for outcome in payload["outcomes_tested"]:
        result = payload["outcomes"][outcome]
        lines.append("### Outcome: `{}`".format(outcome))
        lines.append("")
        lines.append("- **Verdict: `{}`**".format(result["verdict"]))
        lines.append("")
        lines.append("Calendar PSS values:")
        lines.append("")
        lines.append("| Calendar | PSS_in | PSS_oos |")
        lines.append("|---|---:|---:|")
        for cal in ("march20_108", "january_108", "gregorian_month"):
            cal_v = result["calendars"][cal]
            lines.append(
                "| {} | {:.6e} | {:.6e} |".format(
                    cal, cal_v["pss_in"], cal_v["pss_oos"]
                )
            )
        lines.append("")
        null_summary = result["anchor_control_null_summary"]
        lines.append(
            "Anchor-control null distribution (n = {}, exhaustive):".format(
                null_summary["n"]
            )
        )
        lines.append("")
        lines.append(
            "- PSS_in:  mean={:.6e}, median={:.6e}, "
            "min={:.6e}, max={:.6e}".format(
                null_summary["pss_in_mean"],
                null_summary["pss_in_median"],
                null_summary["pss_in_min"],
                null_summary["pss_in_max"],
            )
        )
        lines.append(
            "- PSS_oos: mean={:.6e}, median={:.6e}, "
            "min={:.6e}, max={:.6e}".format(
                null_summary["pss_oos_mean"],
                null_summary["pss_oos_median"],
                null_summary["pss_oos_min"],
                null_summary["pss_oos_max"],
            )
        )
        lines.append("")
        lines.append(
            "- March20 PSS_in:  strictly_below {} of 365 "
            "(strict_percentile {:.4f})".format(
                result["march20_pss_in_strictly_below_count"],
                result["march20_pss_in_strict_percentile_vs_null"],
            )
        )
        lines.append(
            "- March20 PSS_oos: strictly_below {} of 365 "
            "(strict_percentile {:.4f})".format(
                result["march20_pss_oos_strictly_below_count"],
                result["march20_pss_oos_strict_percentile_vs_null"],
            )
        )
        lines.append("")
        lines.append(
            "Threshold gates (per v0.3.3 success criteria, "
            "inherited by GLD v0.1):"
        )
        lines.append("")
        lines.append(
            "- Training screen (strictly_below ≥ {} of 365): **{}**".format(
                payload["training_rank_threshold"],
                "PASS" if result["training_screen_pass"] else "fail",
            )
        )
        lines.append(
            "- Holdout primary (strictly_below ≥ {} of 365 AND PSS_oos > 0): **{}**".format(
                payload["holdout_rank_threshold"],
                "PASS" if result["holdout_primary_pass"] else "fail",
            )
        )
        lines.append(
            "  - rank gate: {} ; PSS_oos > 0: {}".format(
                result["holdout_pct_pass"], result["holdout_positive_pass"]
            )
        )
        lines.append(
            "- Holdout auxiliary (PSS_oos > Gregorian AND PSS_oos > "
            "January-108): **{}**".format(
                "PASS" if result["holdout_auxiliary_pass"] else "fail"
            )
        )
        lines.append(
            "  - vs Gregorian: {} ; vs January-108: {}".format(
                result["control_comparison_pass_gregorian"],
                result["control_comparison_pass_january"],
            )
        )
        lines.append("")
        secondary = result["secondary_diagnostics"]
        if secondary["computed"]:
            lines.append(
                "Secondary diagnostics: computed ({} phases tested, "
                "{} phases rejected at q={}).".format(
                    secondary["n_phases_with_data"],
                    secondary["n_phases_rejected"],
                    secondary["fdr_q"],
                )
            )
        else:
            lines.append(
                "Secondary diagnostics: **{}** ({}).".format(
                    "not computed", secondary["reason"]
                )
            )
        lines.append("")

    lines.append("## Final summary")
    lines.append("")
    overall = payload["overall_summary"]
    if overall == "positive":
        verdict_line = (
            "Both outcomes pass all three success-criterion thresholds. "
            "Per design memo v0.1 (inheriting v0.3.3 criteria), "
            "this is a **positive** result."
        )
    elif overall == "null":
        verdict_line = (
            "Neither outcome clears the success criterion. "
            "Per design memo v0.1 (inheriting v0.3.3 criteria), "
            "this is a **null** result."
        )
    else:
        verdict_line = (
            "One outcome passes and the other fails. "
            "Per design memo v0.1 (inheriting v0.3.3 criteria), "
            "this is a **partial / mixed** signal, interpreted with caution."
        )
    lines.append("**Overall:** `{}` — {}".format(overall, verdict_line))
    lines.append("")
    lines.append("Per-outcome verdicts:")
    lines.append("")
    for outcome, v in payload["per_outcome_verdicts"].items():
        lines.append("- `{}`: **{}**".format(outcome, v))
    lines.append("")
    lines.append(
        "_No exploratory follow-up, post-hoc rescue, energy-conditioning, or "
        "time-energy-coupling analysis was performed. The locked design memo v0.1 "
        "and frozen GLD CSV were not modified during this run. "
        "The training-power caveat above applies when comparing this result to SPY._"
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if not os.path.exists(FROZEN_CSV_PATH):
        print(
            "ERROR: frozen GLD CSV not found at {}".format(FROZEN_CSV_PATH),
            file=sys.stderr,
        )
        return 2

    actual_hash = _file_sha256(FROZEN_CSV_PATH)
    if actual_hash != EXPECTED_CSV_SHA256:
        print(
            "ERROR: frozen GLD CSV SHA256 mismatch.\n"
            "  expected: {}\n"
            "  actual:   {}".format(EXPECTED_CSV_SHA256, actual_hash),
            file=sys.stderr,
        )
        return 2

    json_path = os.path.join(
        RESULTS_DIR,
        "harmonic_calendar_gld_results_{}_{}.json".format(RUN_DATE_TAG, HASH_PREFIX),
    )
    md_path = os.path.join(
        RESULTS_DIR,
        "harmonic_calendar_gld_results_{}_{}.md".format(RUN_DATE_TAG, HASH_PREFIX),
    )
    if os.path.exists(json_path) or os.path.exists(md_path):
        print(
            "ERROR: result files already exist. Re-running the verdict script "
            "after the verdict has been committed is a protocol violation.\n"
            "  json: {}\n"
            "  md:   {}".format(json_path, md_path),
            file=sys.stderr,
        )
        return 2

    head_commit = _git_head_commit(REPO_ROOT)
    run_ts = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")

    df = load_gld(FROZEN_CSV_PATH)
    train_df, holdout_df = make_train_holdout_split(df)

    results = run_protocol(train_df, holdout_df)

    # run_protocol returns "active_memo_version": "v0.3.3" (the protocol module's
    # memo version). For GLD, rename this to inherited_lens_version and inject
    # the GLD cell's own active_memo_version = "v0.1".
    inherited = results.pop("active_memo_version")  # "v0.3.3"

    effective_train_range = "{} through {}".format(
        train_df["date"].iloc[0], train_df["date"].iloc[-1]
    )
    effective_holdout_range = "{} through {}".format(
        holdout_df["date"].iloc[0], holdout_df["date"].iloc[-1]
    )

    provenance = {
        "asset": ASSET,
        "active_memo_path": os.path.relpath(ACTIVE_MEMO_PATH, REPO_ROOT),
        "active_memo_version": GLD_ACTIVE_MEMO_VERSION,
        "inherited_lens_version": inherited,
        "repo_commit_before_run": head_commit,
        "run_timestamp_utc": run_ts,
        "frozen_csv_path": os.path.relpath(FROZEN_CSV_PATH, REPO_ROOT),
        "frozen_csv_sha256": actual_hash,
        "loader": "gld_loader.load_gld",
        "raw_design_data_range": RAW_DESIGN_DATA_RANGE,
        "design_training_rule": DESIGN_TRAINING_RULE,
        "effective_loaded_training_date_range": effective_train_range,
        "effective_loaded_holdout_date_range": effective_holdout_range,
        "row_counts": {
            "loaded": int(len(df)),
            "train": int(len(train_df)),
            "holdout": int(len(holdout_df)),
        },
    }

    payload: Dict[str, Any] = dict(provenance)
    payload.update(results)

    os.makedirs(RESULTS_DIR, exist_ok=True)

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=str)

    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(_format_markdown(payload))

    print("Wrote JSON: {}".format(json_path))
    print("Wrote MD:   {}".format(md_path))
    print("Overall summary: {}".format(payload["overall_summary"]))
    for outcome, v in payload["per_outcome_verdicts"].items():
        print("  {}: {}".format(outcome, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
