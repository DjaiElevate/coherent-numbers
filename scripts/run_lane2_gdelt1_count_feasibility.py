"""Inert-by-default runner for the Lane 2 GDELT 1.0 count-only feasibility.

THIS RUNNER DOES NOT RUN BY DEFAULT AND PERFORMS NO DATA ACCESS UNLESS THREE
INDEPENDENT GUARDS ARE ALL SATISFIED:

  1. module constant COUNT_FEASIBILITY_AUTHORIZED is set True (ships False);
  2. CLI flag --authorize-count-feasibility-run is passed;
  3. env var LANE2_COUNT_FEASIBILITY_AUTHORIZED == "1".

If any guard is missing, the runner prints a refusal and exits BEFORE any
data access, GDELT retrieval, directory creation, or artifact write.

The real retrieval/freeze/count path IS now wired (src.run_count_only_
feasibility). It is reached ONLY after all three guards pass. Source ships
inert on every constant:

  * COUNT_FEASIBILITY_AUTHORIZED = False (this file);
  * REAL_RETRIEVAL_ENABLED      = False (src module).

REAL_RETRIEVAL_ENABLED is flipped TRANSIENTLY IN-PROCESS, only inside the
all-guards-passed branch, immediately around the retrieval call, and the run
metadata records post_run_safety_reset_required so a separate inert-restore
safety commit is mandated if any source constant is ever left permissive
(run-authorization memo 60ec152 §13).

Count-only. No returns, CAR, outcomes, models, p-values, 2023+, or Step 2.
This file does NOT execute the run; only the guarded path can, and the
shipped guards forbid it.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date, datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Ships False. Flipping this is a separate, explicit run-enablement commit
# under run authorization 60ec1521 (memo §13). The single authorized count-only
# feasibility run was executed (F4 archive-layout) under commit fe742555; this
# constant is restored to False (inert-restore safety reset).
# The v0.2 single count-only run authorized under 57f42cc was executed under
# commit 89a5bcb (RUN-HALTED-BOUNDARY: Protocol2023PlusBreach raised inside
# fetch_archive_index — the live index listing now contains 2023+ filenames,
# rejected_2023plus=1219; the §6 caveat was not exercised). This constant is
# restored to False (inert-restore safety reset).
COUNT_FEASIBILITY_AUTHORIZED = False

_REFUSAL = (
    "Lane 2 count-only feasibility run is NOT authorized. Requires "
    "COUNT_FEASIBILITY_AUTHORIZED=True AND --authorize-count-feasibility-run "
    "AND env LANE2_COUNT_FEASIBILITY_AUTHORIZED=1. No data accessed, no "
    "directory created."
)


def _guards_ok(cli_flag: bool) -> bool:
    return (
        COUNT_FEASIBILITY_AUTHORIZED
        and cli_flag
        and os.environ.get("LANE2_COUNT_FEASIBILITY_AUTHORIZED") == "1"
    )


def _fresh_output_dir(repo_root: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = os.path.join(repo_root, "results",
                       "lane2_gdelt1_count_feasibility", ts)
    os.makedirs(out, exist_ok=False)  # must be fresh
    return out


def _real_opener(url, timeout=30.0):
    """Default real network opener. Constructed/used ONLY inside the
    all-guards-passed branch; never imported or called at module load or in
    tests (tests inject a fake opener)."""
    import urllib.request

    return urllib.request.urlopen(url, timeout=timeout)  # noqa: S310


def run_count_feasibility(
    repo_root: str,
    cli_flag: bool = True,
    opener=None,
    coverage_start: date = date(2005, 1, 1),
    coverage_end: date = date(2022, 12, 31),
) -> str:
    """Wired count-only path. Refuses (no data access, no dir) unless all
    three guards pass. Enables retrieval transiently in-process, only here,
    only after guards pass. `opener` is injectable for tests (fake, no
    network); defaults to the real opener in a true run."""
    if not _guards_ok(cli_flag):
        raise SystemExit(_REFUSAL)

    import lane2_gdelt1_count_feasibility as m

    output_dir = _fresh_output_dir(repo_root)
    use_opener = opener if opener is not None else _real_opener

    # Run-enablement under run authorization 60ec1521 §13: flip retrieval ON
    # transiently, in-process, ONLY inside this guarded branch. Source constant
    # stays False; a separate inert-restore safety commit is still required if
    # any source constant is ever left permissive (recorded in metadata).
    prev = m.REAL_RETRIEVAL_ENABLED
    m.REAL_RETRIEVAL_ENABLED = True
    try:
        available, slots = m.fetch_archive_index(use_opener)
        m.run_count_only_feasibility(
            output_dir=output_dir,
            opener=use_opener,
            available_keys=available,
            slot_actual_keys=slots,
            coverage_start=coverage_start,
            coverage_end=coverage_end,
            post_run_safety_reset_required=True,
        )
    finally:
        # Restore in-process default immediately. Source already ships False;
        # this keeps even the live process inert after the single run.
        m.REAL_RETRIEVAL_ENABLED = prev
    return output_dir


def main() -> None:
    p = argparse.ArgumentParser(description="Lane 2 GDELT1 count-only runner")
    p.add_argument("--authorize-count-feasibility-run", action="store_true")
    p.add_argument("--repo-root", default=os.getcwd())
    args = p.parse_args()
    if not _guards_ok(args.authorize_count_feasibility_run):
        print(_REFUSAL)
        return
    out = run_count_feasibility(
        args.repo_root, cli_flag=args.authorize_count_feasibility_run
    )
    print("Count-only feasibility outputs written under: {}".format(out))


if __name__ == "__main__":
    main()
