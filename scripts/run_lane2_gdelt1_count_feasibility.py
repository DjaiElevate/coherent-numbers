"""Inert-by-default runner for the Lane 2 GDELT 1.0 count-only feasibility.

THIS RUNNER DOES NOT RUN BY DEFAULT AND PERFORMS NO DATA ACCESS UNLESS THREE
INDEPENDENT GUARDS ARE ALL SATISFIED:

  1. module constant COUNT_FEASIBILITY_AUTHORIZED is set True (ships False);
  2. CLI flag --authorize-count-feasibility-run is passed;
  3. env var LANE2_COUNT_FEASIBILITY_AUTHORIZED == "1".

If any guard is missing, the runner prints a refusal and exits BEFORE any
data access, GDELT retrieval, or artifact write. Real GDELT retrieval is
deliberately not implemented in this draft (raises NotImplementedError) so the
runner cannot fetch even if mis-authorized.

Count-only. No returns, CAR, outcomes, models, p-values, 2023+, or Step 2.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Ships False. Flipping this is a separate, explicit authorization step.
COUNT_FEASIBILITY_AUTHORIZED = False

_REFUSAL = (
    "Lane 2 count-only feasibility run is NOT authorized. Requires "
    "COUNT_FEASIBILITY_AUTHORIZED=True AND --authorize-count-feasibility-run "
    "AND env LANE2_COUNT_FEASIBILITY_AUTHORIZED=1. No data accessed."
)


def _guards_ok(cli_flag: bool) -> bool:
    return (
        COUNT_FEASIBILITY_AUTHORIZED
        and cli_flag
        and os.environ.get("LANE2_COUNT_FEASIBILITY_AUTHORIZED") == "1"
    )


def run_count_feasibility(repo_root: str) -> None:
    """Wired but inert. Real GDELT retrieval is intentionally not implemented."""
    if not COUNT_FEASIBILITY_AUTHORIZED:
        raise SystemExit(_REFUSAL)
    # Even when authorized, real retrieval is deferred to a future change that
    # must itself pass review; this draft refuses to fetch.
    raise NotImplementedError(
        "Real GDELT 1.0 retrieval is deferred. This draft authorizes no "
        "network access; a future reviewed change implements frozen retrieval."
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Lane 2 GDELT1 count-only runner")
    p.add_argument("--authorize-count-feasibility-run", action="store_true")
    p.add_argument("--repo-root", default=os.getcwd())
    args = p.parse_args()
    if not _guards_ok(args.authorize_count_feasibility_run):
        print(_REFUSAL)
        return
    run_count_feasibility(args.repo_root)


if __name__ == "__main__":
    main()
