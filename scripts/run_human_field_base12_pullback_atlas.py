"""Canonical runner for Human Field x Base-12 Pullback Atlas v0.1.

Authorized canonical run (the "next gate" the prior draft deferred to).

The computational implementation is the committed
src/human_field_base12_pullback_atlas.py, used UNCHANGED. This runner only
orchestrates: load audited frozen inputs, build events via the committed
module, run the committed preflight, and EMIT the descriptive artifacts the
implementation plan specifies. It adds no statistic, no null, no p-value, no
verdict, no candidate hypotheses, no interpretation.

Exploratory atlas mode. Full grids only; low-data cells (n < 20) retained but
flagged and excluded from candidate-hypothesis formation; Candidate H0 is
equal-weight. No post-2022 row enters any computation (the SPY frame is
filtered before feature construction). No Lane 2. No OOS analysis.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")  # headless; no interactive backend
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import human_field_base12_pullback_atlas as atlas  # noqa: E402

# Authorized canonical run gate (this is the explicitly authorized gate).
CANONICAL_RUN_AUTHORIZED = True

_REFUSAL = (
    "Canonical atlas run is NOT authorized. Set CANONICAL_RUN_AUTHORIZED=True "
    "and pass --authorize-canonical-run."
)


def _shared_timestamp_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")


def _na(v):
    return "NA" if v is atlas.NA else v


def _phase_label(p0: int) -> int:
    """Chronological 1-based phase label (no clustering/reordering)."""
    return p0 + 1


# ── artifact emission (descriptive only) ──────────────────────────────────────

def _write_phase_state_csv(path, cells, phase_name):
    lines = ["{},state,value,n,low_data,marker".format(phase_name)]
    for c in cells:
        phase, state = c.keys
        lines.append(
            "{},{},{},{},{},{}".format(
                _phase_label(phase), state, _na(c.value), c.n,
                str(c.low_data).lower(), c.marker,
            )
        )
    path.write_text("\n".join(lines) + "\n")


def _write_grid4_csv(path, rows):
    lines = ["state,n,pss_12,pss_10,low_data"]
    for r in rows:
        lines.append(
            "{},{},{},{},{}".format(
                r["state"], r["n"], _na(r["pss_12"]), _na(r["pss_10"]),
                str(r["low_data"]).lower(),
            )
        )
    path.write_text("\n".join(lines) + "\n")


def _write_grid5_csv(path, cells):
    lines = ["asset,base12_phase,state,long_pct,n,low_data,marker"]
    for c in cells:
        asset, phase, state = c.keys
        lines.append(
            "{},{},{},{},{},{},{}".format(
                asset, _phase_label(phase), state, _na(c.value), c.n,
                str(c.low_data).lower(), c.marker,
            )
        )
    path.write_text("\n".join(lines) + "\n")


def _write_sparsity_csv(path, report):
    lines = ["grid,total_cells,low_data_cells,fraction_events_in_low_data_cells"]
    for r in report:
        lines.append(
            "{},{},{},{}".format(
                r["grid"], r["total_cells"], r["low_data_cells"],
                _na(r["fraction_events_in_low_data_cells"]),
            )
        )
    path.write_text("\n".join(lines) + "\n")


def _heatmap(path, cells, n_phases, title, fname):
    """phase x state heatmap; NA blanked, low-data hatched, n annotated."""
    states = list(atlas.STATE_ORDER)
    grid = [[None] * len(states) for _ in range(n_phases)]
    ncnt = [[0] * len(states) for _ in range(n_phases)]
    low = [[False] * len(states) for _ in range(n_phases)]
    for c in cells:
        p, s = c.keys
        j = states.index(s)
        grid[p][j] = (None if c.value is atlas.NA else c.value)
        ncnt[p][j] = c.n
        low[p][j] = c.low_data
    import numpy as np

    arr = np.array(
        [[(np.nan if v is None else v) for v in row] for row in grid],
        dtype=float,
    )
    fig, ax = plt.subplots(figsize=(1.6 + 1.1 * len(states), 0.5 * n_phases + 1.5))
    im = ax.imshow(arr, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(states)))
    ax.set_xticklabels(states, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(n_phases))
    ax.set_yticklabels([_phase_label(p) for p in range(n_phases)], fontsize=8)
    ax.set_ylabel("phase (chronological 1..{})".format(n_phases))
    ax.set_title(title, fontsize=9)
    for p in range(n_phases):
        for j in range(len(states)):
            txt = "n={}".format(ncnt[p][j])
            ax.text(j, p, txt, ha="center", va="center", color="white", fontsize=6)
            if low[p][j]:
                ax.add_patch(
                    plt.Rectangle(
                        (j - 0.5, p - 0.5), 1, 1, fill=False, hatch="xxx",
                        edgecolor="red", linewidth=0.0,
                    )
                )
    fig.colorbar(im, ax=ax, shrink=0.7)
    fig.text(
        0.01, 0.01,
        "hatched = low-data (n < 20), excluded from candidate-hypothesis "
        "formation; blank = NA",
        fontsize=6,
    )
    fig.tight_layout()
    fig.savefig(path / fname, dpi=120)
    plt.close(fig)


def run_canonical(repo_root: str) -> str:
    if not CANONICAL_RUN_AUTHORIZED:
        raise SystemExit(_REFUSAL)

    import pathlib

    from candidate_b_loader import load_reduced_phase3b_pool, verify_frozen_inputs
    from spy_loader import load_spy

    timestamp = _shared_timestamp_utc()

    observed = verify_frozen_inputs(repo_root)
    trades = load_reduced_phase3b_pool(repo_root)

    # Full frozen SPY CSV is read here, then bounded BEFORE any feature is
    # constructed. Hence the audit-safe wording: "no post-2022 rows used in
    # computation", not "no OOS contact".
    spy_clean = load_spy(os.path.join(repo_root, atlas.SPY_FROZEN_CSV))
    spy = atlas.build_spy_frame(
        spy_clean["date"].tolist(),
        spy_clean["adj_close"].tolist(),
        spy_clean["log_return"].tolist(),
    )

    events = atlas.build_events(trades, spy)
    status, details = atlas.preflight(trades, spy, events)

    asset_counts = {}
    for a in trades.asset:
        asset_counts[str(a)] = asset_counts.get(str(a), 0) + 1

    metadata = atlas.build_metadata(
        timestamp_utc=timestamp,
        observed_hashes=observed,
        row_count=len(trades),
        asset_counts=asset_counts,
        methodological_status=status,
        indeterminate_n=details["indeterminate_count"],
    )

    # Grids (committed module; full cartesian, every cell n + low_data).
    g1 = atlas.grid1_event_count(events)
    g2 = atlas.grid2_long_pct(events)
    g3 = atlas.grid3_median_r(events)
    g4 = atlas.grid4_state_pss(events)
    g5 = atlas.grid5_asset_phase_state(events)
    g6 = atlas.grid6_direction_splits(events)
    g8 = atlas.grid8_base10_views(events)
    g7 = atlas.grid7_sparsity_report(
        {
            "grid1_count": g1,
            "grid2_long_pct": g2,
            "grid3_median_r": g3,
            "grid5_asset_phase_state": g5,
            "grid8_base10_count": g8["count"],
            "grid8_base10_long_pct": g8["long_pct"],
        }
    )

    out_root = pathlib.Path(repo_root) / "results"
    tables = out_root / "human_field_base12_pullback_atlas_tables_{}".format(timestamp)
    heat = out_root / "human_field_base12_pullback_atlas_heatmaps_{}".format(timestamp)
    tables.mkdir(parents=True, exist_ok=False)
    heat.mkdir(parents=True, exist_ok=False)

    _write_phase_state_csv(tables / "grid1_count.csv", g1, "base12_phase")
    _write_phase_state_csv(tables / "grid2_long_pct.csv", g2, "base12_phase")
    _write_phase_state_csv(tables / "grid3_median_r.csv", g3, "base12_phase")
    _write_grid4_csv(tables / "grid4_state_pss.csv", g4)
    _write_grid5_csv(tables / "grid5_asset_phase_state.csv", g5)
    _write_phase_state_csv(
        tables / "grid6_long_only_count.csv", g6["long_only"]["count"], "base12_phase"
    )
    _write_phase_state_csv(
        tables / "grid6_long_only_long_pct.csv",
        g6["long_only"]["long_pct"], "base12_phase",
    )
    _write_phase_state_csv(
        tables / "grid6_long_only_median_r.csv",
        g6["long_only"]["median_r"], "base12_phase",
    )
    _write_phase_state_csv(
        tables / "grid6_short_only_count.csv",
        g6["short_only"]["count"], "base12_phase",
    )
    _write_phase_state_csv(
        tables / "grid6_short_only_long_pct.csv",
        g6["short_only"]["long_pct"], "base12_phase",
    )
    _write_phase_state_csv(
        tables / "grid6_short_only_median_r.csv",
        g6["short_only"]["median_r"], "base12_phase",
    )
    _write_phase_state_csv(tables / "grid8_base10_count.csv", g8["count"], "base10_phase")
    _write_phase_state_csv(
        tables / "grid8_base10_long_pct.csv", g8["long_pct"], "base10_phase"
    )
    _write_phase_state_csv(
        tables / "grid8_base10_median_r.csv", g8["median_r"], "base10_phase"
    )
    _write_grid4_csv(tables / "grid8_base10_state_pss.csv", g8["state_pss"])
    _write_sparsity_csv(tables / "grid7_sparsity_report.csv", g7)

    _heatmap(heat, g1, atlas.BASE12, "Grid1 base-12 phase x state: event count",
             "grid1_count_base12.png")
    _heatmap(heat, g2, atlas.BASE12, "Grid2 base-12 phase x state: long %",
             "grid2_long_pct_base12.png")
    _heatmap(heat, g3, atlas.BASE12, "Grid3 base-12 phase x state: median r_multiple",
             "grid3_median_r_base12.png")
    _heatmap(heat, g8["count"], atlas.BASE10,
             "Grid8 base-10 (Candidate C comparator) phase x state: event count",
             "grid8_count_base10.png")
    _heatmap(heat, g8["long_pct"], atlas.BASE10,
             "Grid8 base-10 (Candidate C comparator) phase x state: long %",
             "grid8_long_pct_base10.png")

    meta_path = out_root / "human_field_base12_pullback_atlas_metadata_{}.json".format(
        timestamp
    )
    metadata["grids_emitted"] = sorted(p.name for p in tables.iterdir())
    metadata["heatmaps_emitted"] = sorted(p.name for p in heat.iterdir())
    metadata["preflight_details"] = details
    metadata["candidate_hypotheses_generated"] = []
    metadata["candidate_hypotheses_note"] = (
        "No candidate hypotheses authored in this run. Hypothesis formation is "
        "a separately reviewed step; low-data (n<20) and indeterminate-state "
        "cells are excluded from any future formation. Candidate H0 "
        "(no coherent joint structure) remains a valid equal-weight outcome."
    )
    meta_path.write_text(json.dumps(metadata, indent=2, default=str) + "\n")

    # Descriptive summary (no verdict / no interpretation / no hypotheses).
    sp = "\n".join(
        "- {}: {} cells, {} low-data, {} of events in low-data cells".format(
            r["grid"], r["total_cells"], r["low_data_cells"],
            r["fraction_events_in_low_data_cells"],
        )
        for r in g7
    )
    g4_lines = "\n".join(
        "- {}: n={}, PSS_12={}, PSS_10={}{}".format(
            r["state"], r["n"], _na(r["pss_12"]), _na(r["pss_10"]),
            " [low-data]" if r["low_data"] else "",
        )
        for r in g4
    )
    summary_path = (
        out_root
        / "human_field_base12_pullback_atlas_summary_{}.md".format(timestamp)
    )
    summary_path.write_text(
        "# Human Field x Base-12 Pullback Atlas v0.1 — Summary ({} UTC)\n\n"
        "Exploratory atlas. Descriptive only: no success criterion, no "
        "verdict, no p-value as evidence, no permutation, no beat count, no "
        "confirmation, no rescue, no profitability, no Lane 2, no candidate "
        "hypotheses authored here. Full grids emitted; low-data cells "
        "(n < 20) retained, flagged, and excluded from any future "
        "candidate-hypothesis formation. Candidate H0 (no coherent joint "
        "structure) remains a valid equal-weight outcome.\n\n"
        "Commit: 8493c951b877b266c937bd498c11a9a1fc572794\n"
        "Methodological status: {}\n"
        "Row count: {} (SPY 243 / EFA 283 / EEM 261 / GLD 253 / TLT 242 "
        "expected)\n"
        "Indeterminate-state count: {}\n"
        "No post-2022 rows were used in any atlas computation. The SPY "
        "auxiliary frame was filtered before feature construction.\n\n"
        "## Sparsity\n{}\n\n## State-level PSS_12 vs PSS_10 (descriptive)\n"
        "{}\n\n"
        "Tables: {}\nHeatmaps: {}\n".format(
            timestamp, status, len(trades),
            details["indeterminate_count"], sp, g4_lines,
            tables.name, heat.name,
        )
    )

    # Closure memo: fixed sealed-data/no-verdict boilerplate + descriptive
    # observations only. No candidate hypotheses. No interpretation.
    closure_path = (
        pathlib.Path(repo_root)
        / "docs"
        / "human_field_base12_pullback_atlas_closure_memo_v0.1.md"
    )
    closure_path.write_text(
        atlas.CLOSURE_MEMO_FIXED_BOILERPLATE
        + "\n\n## Run provenance\n\n"
        "- Commit: 8493c951b877b266c937bd498c11a9a1fc572794\n"
        "- Timestamp (UTC): {}\n- Methodological status: {}\n"
        "- Row count: {}; indeterminate-state: {}\n"
        "- No post-2022 rows were used in any atlas computation; the SPY "
        "auxiliary frame was filtered before feature construction.\n\n"
        "## Descriptive observations (no verdict, no hypotheses)\n\n"
        "The full grids are in results/.../tables_{}. Every cell carries n "
        "and a low_data flag. State-level PSS_12 / PSS_10 are reported as "
        "plain descriptive numbers with no null, permutation, beat count, or "
        "verdict. Low-data (n<20) and indeterminate-state cells are excluded "
        "from any candidate-hypothesis formation, which is deferred to a "
        "separately reviewed step. Candidate H0 (no coherent joint structure) "
        "remains a valid equal-weight outcome of this atlas.\n".format(
            timestamp, status, len(trades), details["indeterminate_count"],
            timestamp,
        )
    )

    print("ATLAS_OUTPUT_DIR_TABLES:", tables)
    print("ATLAS_OUTPUT_DIR_HEATMAPS:", heat)
    print("ATLAS_METADATA:", meta_path)
    print("ATLAS_SUMMARY:", summary_path)
    print("ATLAS_CLOSURE:", closure_path)
    print("METHODOLOGICAL_STATUS:", status)
    print("INDETERMINATE_COUNT:", details["indeterminate_count"])
    return timestamp


def main() -> None:
    parser = argparse.ArgumentParser(description="Human Field x Base-12 Atlas runner")
    parser.add_argument("--authorize-canonical-run", action="store_true")
    parser.add_argument("--repo-root", default=os.getcwd())
    args = parser.parse_args()
    if not (args.authorize_canonical_run and CANONICAL_RUN_AUTHORIZED):
        print(_REFUSAL)
        return
    run_canonical(args.repo_root)


if __name__ == "__main__":
    main()
