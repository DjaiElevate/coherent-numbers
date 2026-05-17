"""Canonical runner for Human Field x Base-12 Pullback Atlas v0.1.

THIS SCRIPT DOES NOT RUN THE CANONICAL ATLAS BY DEFAULT.

Governance
==========
The canonical run loads the real frozen 1,282-trade substrate and the frozen
SPY series and writes result artifacts. Per the active authorization scope,
that is gated behind an explicit flag AND a module constant that ships False.
Running this file without both does nothing but print the refusal notice.

Exploratory atlas mode. No success criterion, no verdict, no p-value as
evidence, no confirmation, no rescue, no profitability, no Lane 2, no OOS.
Full grids only; low-data cells (n < 20) retained but flagged and excluded
from candidate-hypothesis formation; Candidate H0 is equal-weight.
"""

from __future__ import annotations

import argparse
import datetime
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from human_field_base12_pullback_atlas import (  # noqa: E402
    SPY_FROZEN_CSV,
    build_events,
    build_metadata,
    build_spy_frame,
    preflight,
)

# Ships False. Flipping this is a separate, explicit authorization step. Even
# when True, the --authorize-canonical-run flag is still required.
CANONICAL_RUN_AUTHORIZED = False

_REFUSAL = (
    "Canonical atlas run is NOT authorized.\n"
    "This implementation draft does not authorize canonical atlas generation. "
    "No atlas tables, heatmaps, candidate hypotheses, or closure observations "
    "have been produced. The next gate is explicit authorization to run the "
    "atlas (set CANONICAL_RUN_AUTHORIZED=True and pass "
    "--authorize-canonical-run)."
)


def _shared_timestamp_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")


def run_canonical(repo_root: str) -> None:
    """Wired but inert unless explicitly authorized. Loads NO data otherwise."""
    if not CANONICAL_RUN_AUTHORIZED:
        raise SystemExit(_REFUSAL)

    # The body below is intentionally only reached under explicit
    # authorization. It is wired against the audited loaders but left for the
    # next gate; it deliberately performs no curation and emits full grids.
    from candidate_b_loader import load_reduced_phase3b_pool, verify_frozen_inputs
    from spy_loader import load_spy

    timestamp = _shared_timestamp_utc()
    observed = verify_frozen_inputs(repo_root)
    trades = load_reduced_phase3b_pool(repo_root)

    spy_clean = load_spy(os.path.join(repo_root, SPY_FROZEN_CSV))
    spy = build_spy_frame(
        spy_clean["date"].tolist(),
        spy_clean["adj_close"].tolist(),
        spy_clean["log_return"].tolist(),
    )

    events = build_events(trades, spy)
    status, details = preflight(trades, spy, events)
    asset_counts = {}
    for a in trades.asset:
        asset_counts[str(a)] = asset_counts.get(str(a), 0) + 1
    metadata = build_metadata(
        timestamp_utc=timestamp,
        observed_hashes=observed,
        row_count=len(trades),
        asset_counts=asset_counts,
        methodological_status=status,
        indeterminate_n=details["indeterminate_count"],
    )
    if status != "ok":
        raise SystemExit(
            "Preflight set methodological_status={}; aborting before any "
            "candidate-hypothesis summary. Details: {}".format(status, details)
        )
    # Grid emission + artifact writing intentionally deferred to the next
    # authorized gate. metadata is computed but not written here.
    _ = metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Human Field x Base-12 Atlas runner")
    parser.add_argument(
        "--authorize-canonical-run",
        action="store_true",
        help="Required (with CANONICAL_RUN_AUTHORIZED=True) to run canonically.",
    )
    parser.add_argument("--repo-root", default=os.getcwd())
    args = parser.parse_args()

    if not (args.authorize_canonical_run and CANONICAL_RUN_AUTHORIZED):
        print(_REFUSAL)
        return
    run_canonical(args.repo_root)


if __name__ == "__main__":
    main()
