"""Lane 2 GDELT1 Step 2 feature-generator CLI.

Default behavior: **dry-run / in-memory only**. Loads the canonical merged
substrate, builds the Step 2 feature table in memory, runs the §§9-11
conformance gate, and prints a one-page report. NO output artifacts are written.

The actual write path requires the dedicated `--write-step2-output` flag,
which itself requires a separate, future Step 2 **execution-authorization**
prompt. Until then the flag is wired but blocked-closed: invoking it raises
Step2BoundaryError with a message pointing back to the design memo.

The CLI does NOT reuse `FULL_BUILD_AUTHORIZED` (live-fetch guard; Step 2 is
offline) and does NOT reuse `--write-merge-output` (merge-writer scoped).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
# Ensure src/ is on sys.path when this script is invoked directly (the repo's
# conftest.py only loads under pytest; standalone CLI invocations need their
# own path setup, mirroring the conftest pattern).
_SRC_DIR = str(REPO_ROOT / "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

import lane2_gdelt1_step2_features as step2  # noqa: E402

CANONICAL_MERGED_DIR_PATH = (
    REPO_ROOT
    / "results"
    / "lane2_gdelt1_full_daily_count_build"
    / step2.CANONICAL_MERGED_DIR_BASENAME
)

# Canonical parent for a real (separately authorized) execution's output.
# The writer creates a fresh `<UTC-ts>Z/` subdir under this path. This turn
# never writes here: the write path is blocked closed (see below).
CANONICAL_STEP2_OUTPUT_PARENT_PATH = (
    REPO_ROOT
    / "results"
    / step2.CANONICAL_STEP2_OUTPUT_PARENT_BASENAME
)

# Locked False. A real Step 2 execution requires a separate, explicit
# execution-authorization prompt that flips this to True in that authorized
# turn. While it is False, `--write-step2-output` is blocked closed and raises
# Step2BoundaryError before any byte is written.
STEP2_EXECUTION_AUTHORIZED = False  # locked False; do not flip here


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_lane2_gdelt1_step2_features",
        description=(
            "Dry-run / in-memory Step 2 feature generation + conformance gate. "
            "Writing the three Step 2 result-output artifacts requires the "
            "dedicated --write-step2-output flag AND a separate execution "
            "authorization."
        ),
    )
    parser.add_argument(
        "--merged-dir",
        type=Path,
        default=CANONICAL_MERGED_DIR_PATH,
        help=(
            "Path to the canonical merged substrate directory "
            "(default: results/lane2_gdelt1_full_daily_count_build/"
            f"{step2.CANONICAL_MERGED_DIR_BASENAME})."
        ),
    )
    parser.add_argument(
        "--skip-input-pin-verification",
        action="store_true",
        help=(
            "Skip SHA-256 / build_manifest_digest pin verification on the "
            "merged substrate. Intended for synthetic-fixture tests only; "
            "the conformance gate proper requires pins to match."
        ),
    )
    parser.add_argument(
        "--write-step2-output",
        action="store_true",
        help=(
            "Reserved dedicated write flag. Currently BLOCKED CLOSED until a "
            "separate execution-authorization prompt flips "
            "STEP2_EXECUTION_AUTHORIZED to True. While blocked, invoking it "
            "raises Step2BoundaryError before any byte is written."
        ),
    )
    parser.add_argument(
        "--output-parent-dir",
        type=Path,
        default=CANONICAL_STEP2_OUTPUT_PARENT_PATH,
        help=(
            "Parent directory under which a real execution writes a fresh "
            "<UTC-ts>Z/ output directory (default: results/"
            f"{step2.CANONICAL_STEP2_OUTPUT_PARENT_BASENAME}). Only used when "
            "--write-step2-output is authorized."
        ),
    )
    parser.add_argument(
        "--report-json",
        action="store_true",
        help="Print the conformance-gate report as JSON instead of text.",
    )
    return parser


def _format_text_report(report: dict) -> str:
    lines = [
        "=== Lane 2 GDELT1 Step 2 Conformance Gate ===",
        f"merged_dir: {report['merged_dir']}",
        f"step2_implementation_version: {report['step2_implementation_version']}",
        f"design_memo_sha256: {report['design_memo_sha256']}",
        f"build_manifest_digest_expected: {report['build_manifest_digest_expected']}",
        f"verify_pins: {report['verify_pins']}",
        f"input_row_count: {report['input_row_count']}",
        f"feature_row_count: {report['feature_row_count']}",
        f"feature_schema_size: {len(report['feature_schema'])}",
        f"summary_audit_hits: {report['summary_audit_hits']}",
        f"metadata_audit_hits: {report['metadata_audit_hits']}",
        f"summary_byte_count: {report['summary_byte_count']}",
        "boundary_declarations: "
        + ", ".join(
            f"{k}={v}" for k, v in report["boundary_declarations"].items()
        ),
        f"verdict: {report['verdict']}",
    ]
    return "\n".join(lines)


def _format_write_manifest(manifest: dict) -> str:
    lines = [
        "=== Lane 2 GDELT1 Step 2 Output Write ===",
        f"output_dir: {manifest['output_dir']}",
        f"verdict: {manifest['verdict']}",
        f"input_row_count: {manifest['input_row_count']}",
        f"feature_row_count: {manifest['feature_row_count']}",
        f"build_manifest_digest: {manifest['build_manifest_digest']}",
        "artifacts_sha256:",
    ]
    for basename, digest in manifest["artifacts_sha256"].items():
        lines.append(f"  {basename}: {digest}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.write_step2_output:
        if not STEP2_EXECUTION_AUTHORIZED:
            # Blocked closed: the write path is implemented and tested, but a
            # real write requires a separate execution-authorization prompt
            # that flips STEP2_EXECUTION_AUTHORIZED to True in that authorized
            # turn. We fail before any byte is written.
            raise step2.Step2BoundaryError(
                "--write-step2-output is blocked closed in this implementation. "
                "A separate execution-authorization prompt is required (it "
                "flips STEP2_EXECUTION_AUTHORIZED to True), and the §§9-11 "
                "conformance gate must independently PASS first. "
                "See docs/lane2_gdelt1_step2_implementation_design_memo_v0.1.md "
                "§§5, 11, 14."
            )
        # Authorized execution path (only reachable when a separately
        # authorized turn has set STEP2_EXECUTION_AUTHORIZED = True). The
        # writer re-runs the §11 conformance gate and fails closed on any
        # mismatch before writing.
        manifest = step2.write_step2_outputs(
            args.merged_dir,
            args.output_parent_dir,
            verify_pins=not args.skip_input_pin_verification,
        )
        if args.report_json:
            print(json.dumps(manifest, indent=2, sort_keys=True))
        else:
            print(_format_write_manifest(manifest))
        return 0

    report = step2.run_conformance_gate(
        args.merged_dir,
        verify_pins=not args.skip_input_pin_verification,
    )

    if args.report_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(_format_text_report(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
