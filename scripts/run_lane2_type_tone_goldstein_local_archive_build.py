"""Lane 2 TTG local approved-fields archive build runner — Phase 1 (synthetic).

This runner is a thin CLI over `lane2_type_tone_goldstein_local_archive`. It
recognizes — but in Phase 1 cannot execute — a future three-part run gate:

  1. module constant TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED True
     (ships False);
  2. CLI flag --authorize-local-archive-build;
  3. env var LANE2_TTG_LOCAL_ARCHIVE_BUILD_AUTHORIZED == "1".

Phase-1 boundary (by construction): this runner contains NO network code.
It imports no `urllib` / `requests` / `socket` and constructs no opener,
URL, or fetch object. Even if all three guards are satisfied, the build
hard-errors at the acquisition step with the exact message
`NETWORK NOT AUTHORIZED IN PHASE 1`. Enabling a real fetch (Phase 2) is a
reviewed code change, not a flag / env / constant flip in this turn.

This runner authorizes no network, no archive execution, no TTG extraction,
and no join.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
# Mirror the conftest pattern so direct CLI invocation finds src/.
_SRC_DIR = str(REPO_ROOT / "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

import lane2_type_tone_goldstein_local_archive as archive  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_lane2_type_tone_goldstein_local_archive_build",
        description=(
            "Phase-1 synthetic-only TTG local approved-fields archive build "
            "runner. Refuses to run unless all three guards are satisfied, "
            "and even then hard-errors at acquisition (network is impossible "
            "by construction in Phase 1)."
        ),
    )
    parser.add_argument(
        "--authorize-local-archive-build",
        action="store_true",
        help=(
            "CLI guard 2/3. Must accompany the module constant guard "
            "(TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED=True) AND env "
            "LANE2_TTG_LOCAL_ARCHIVE_BUILD_AUTHORIZED=1. Phase 1 still "
            "hard-errors at acquisition."
        ),
    )
    parser.add_argument(
        "--candidate-date",
        action="append",
        default=[],
        metavar="YYYY-MM-DD",
        help=(
            "Repeatable. Optional in-window candidate source date(s) for the "
            "enumeration step. 2023+ dates hard-error at enumeration."
        ),
    )
    parser.add_argument(
        "--repo-root",
        default=os.getcwd(),
        help="Repository root. Defaults to CWD.",
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        archive.run_local_archive_build(
            cli_flag=args.authorize_local_archive_build,
            candidate_dates=args.candidate_date,
            module_authorized=archive.TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED,
            env=os.environ,
        )
    except archive.ArchiveBuildRefused as e:
        print("REFUSED: {}".format(e), file=sys.stderr)
        return 2
    except archive.Phase1NetworkNotAuthorized as e:
        # Exact message: NETWORK NOT AUTHORIZED IN PHASE 1
        print("HALT: {}".format(e), file=sys.stderr)
        return 3
    except archive.Post2022SealBreach as e:
        print("HALT: {}".format(e), file=sys.stderr)
        return 4
    # Unreachable in Phase 1 (acquisition always hard-errors).
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
