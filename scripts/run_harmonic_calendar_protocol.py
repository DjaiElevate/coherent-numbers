"""Commit 4 — single locked run of the v0.3.3 harmonic calendar protocol.

This script is the SINGLE OFFICIAL invocation of the locked protocol against
the frozen SPY CSV. It reads:

  data/raw/spy_yahoo_v8_19930129_20241231_<sha256>.csv
  docs/harmonic_calendar_design_memo_v0.3.3.md   (active locked memo)

It writes:

  results/harmonic_calendar_mvt_results_<run_date>_<hashprefix>.json
  results/harmonic_calendar_mvt_results_<run_date>_<hashprefix>.md

No live network calls. No Yahoo fetching. The canonical loader load_spy() is
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

from spy_loader import load_spy, make_train_holdout_split  # noqa: E402
from harmonic_calendar import (  # noqa: E402
    ANCHOR_CONTROL_POPULATION_SIZE,
    RANDOM_ANCHOR_SEED,
    TRAINING_RANK_THRESHOLD,
    HOLDOUT_RANK_THRESHOLD,
)
from harmonic_calendar_protocol import (  # noqa: E402
    ACTIVE_MEMO_VERSION,
    OUTCOMES,
    run_protocol,
)

FROZEN_CSV_PATH = os.path.join(
    REPO_ROOT,
    "data",
    "raw",
    "spy_yahoo_v8_19930129_20241231_"
    "e8fc0357410ce499da8f67e09b4c9908232e18a55445f38969e77fa712aaaa56.csv",
)
EXPECTED_CSV_SHA256 = (
    "e8fc0357410ce499da8f67e09b4c9908232e18a55445f38969e77fa712aaaa56"
)
ACTIVE_MEMO_PATH = os.path.join(
    REPO_ROOT, "docs", "harmonic_calendar_design_memo_v0.3.3.md"
)
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
RUN_DATE_TAG = "20260512"
HASH_PREFIX = EXPECTED_CSV_SHA256[:8]


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
    lines.append("# Harmonic Calendar MVT — v0.3.3 Verdict")
    lines.append("")
    lines.append("**Project:** Coherent Numbers")
    lines.append(f"**Active memo:** `{payload['active_memo_path']}` ({payload['active_memo_version']})")
    lines.append(f"**Repo commit before run:** `{payload['repo_commit_before_run']}`")
    lines.append(f"**Run timestamp (UTC):** {payload['run_timestamp_utc']}")
    lines.append(f"**Frozen CSV:** `{payload['frozen_csv_path']}`")
    lines.append(f"**Frozen CSV SHA256:** `{payload['frozen_csv_sha256']}`")
    lines.append(f"**Loader:** `{payload['loader']}`")
    lines.append(
        "**Anchor-control:** exhaustive enumeration, "
        f"{payload['anchor_control_population_size']} integer-DOY anchors (1..365)"
    )
    lines.append(
        f"**Rank thresholds:** training strictly_below ≥ "
        f"{payload['training_rank_threshold']} (= ceil(0.95 × 365)); "
        f"holdout strictly_below ≥ {payload['holdout_rank_threshold']} "
        f"(= ceil(0.90 × 365))"
    )
    lines.append(
        f"**Seed (preserved, not consumed):** RANDOM_ANCHOR_SEED = "
        f"{payload['random_anchor_seed_preserved']}"
    )
    lines.append("")
    lines.append("## Data ranges")
    lines.append("")
    lines.append(f"- Loaded rows: {payload['row_counts']['loaded']}")
    lines.append(
        f"- Training: {payload['train']['n_rows']} rows, "
        f"{payload['train']['date_min']} → {payload['train']['date_max']}"
    )
    lines.append(
        f"- Holdout: {payload['holdout']['n_rows']} rows, "
        f"{payload['holdout']['date_min']} → {payload['holdout']['date_max']}"
    )
    lines.append("")
    lines.append("## Per-outcome verdicts")
    lines.append("")
    for outcome in payload["outcomes_tested"]:
        result = payload["outcomes"][outcome]
        lines.append(f"### Outcome: `{outcome}`")
        lines.append("")
        lines.append(f"- **Verdict: `{result['verdict']}`**")
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
        lines.append("Anchor-control null distribution (n = {}, exhaustive):".format(null_summary["n"]))
        lines.append("")
        lines.append(
            "- PSS_in:  mean={:.6e}, median={:.6e}, min={:.6e}, max={:.6e}".format(
                null_summary["pss_in_mean"],
                null_summary["pss_in_median"],
                null_summary["pss_in_min"],
                null_summary["pss_in_max"],
            )
        )
        lines.append(
            "- PSS_oos: mean={:.6e}, median={:.6e}, min={:.6e}, max={:.6e}".format(
                null_summary["pss_oos_mean"],
                null_summary["pss_oos_median"],
                null_summary["pss_oos_min"],
                null_summary["pss_oos_max"],
            )
        )
        lines.append("")
        lines.append(
            "- March20 PSS_in:  strictly_below {} of 365 (strict_percentile {:.4f})".format(
                result["march20_pss_in_strictly_below_count"],
                result["march20_pss_in_strict_percentile_vs_null"],
            )
        )
        lines.append(
            "- March20 PSS_oos: strictly_below {} of 365 (strict_percentile {:.4f})".format(
                result["march20_pss_oos_strictly_below_count"],
                result["march20_pss_oos_strict_percentile_vs_null"],
            )
        )
        lines.append("")
        lines.append("Threshold gates (per memo v0.3.3 success criteria):")
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
            "- Holdout auxiliary (PSS_oos > Gregorian AND PSS_oos > January-108): **{}**".format(
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
        verdict_line = "Both outcomes pass all three success-criterion thresholds. Per memo v0.3.3, this is a **positive** result."
    elif overall == "null":
        verdict_line = "Neither outcome clears the success criterion. Per memo v0.3.3, this is a **null** result."
    else:
        verdict_line = "One outcome passes and the other fails. Per memo v0.3.3, this is a **partial / mixed** signal, interpreted with caution."
    lines.append(f"**Overall:** `{overall}` — {verdict_line}")
    lines.append("")
    lines.append("Per-outcome verdicts:")
    lines.append("")
    for outcome, v in payload["per_outcome_verdicts"].items():
        lines.append(f"- `{outcome}`: **{v}**")
    lines.append("")
    lines.append(
        "_No exploratory follow-up, post-hoc rescue, energy-conditioning, or "
        "time-energy-coupling analysis was performed. The locked memo v0.3.3 "
        "and frozen CSV were not modified during this run._"
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if not os.path.exists(FROZEN_CSV_PATH):
        print("ERROR: frozen CSV not found at {}".format(FROZEN_CSV_PATH), file=sys.stderr)
        return 2

    actual_hash = _file_sha256(FROZEN_CSV_PATH)
    if actual_hash != EXPECTED_CSV_SHA256:
        print(
            "ERROR: frozen CSV SHA256 mismatch.\n"
            "  expected: {}\n"
            "  actual:   {}".format(EXPECTED_CSV_SHA256, actual_hash),
            file=sys.stderr,
        )
        return 2

    head_commit = _git_head_commit(REPO_ROOT)
    run_ts = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")

    df = load_spy(FROZEN_CSV_PATH)
    train_df, holdout_df = make_train_holdout_split(df)

    results = run_protocol(train_df, holdout_df)

    provenance = {
        "repo_commit_before_run": head_commit,
        "run_timestamp_utc": run_ts,
        "frozen_csv_path": os.path.relpath(FROZEN_CSV_PATH, REPO_ROOT),
        "frozen_csv_sha256": actual_hash,
        "active_memo_path": os.path.relpath(ACTIVE_MEMO_PATH, REPO_ROOT),
        "active_memo_version": ACTIVE_MEMO_VERSION,
        "loader": "spy_loader.load_spy",
        "row_counts": {
            "loaded": int(len(df)),
            "train": int(len(train_df)),
            "holdout": int(len(holdout_df)),
        },
    }
    payload: Dict[str, Any] = dict(provenance)
    payload.update(results)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    json_path = os.path.join(
        RESULTS_DIR,
        "harmonic_calendar_mvt_results_{}_{}.json".format(RUN_DATE_TAG, HASH_PREFIX),
    )
    md_path = os.path.join(
        RESULTS_DIR,
        "harmonic_calendar_mvt_results_{}_{}.md".format(RUN_DATE_TAG, HASH_PREFIX),
    )

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
