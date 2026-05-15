"""Candidate C v0.1 locked-protocol runner — single official invocation.

Parallel to scripts/run_candidate_b_protocol.py. Reads the six frozen
pullback CSVs under SHA-256 verification (via Candidate B's already-tested
loader), constructs the reduced in-memory view, runs the locked Candidate C
protocol twice through the rerun gate, and writes the verdict log to
results/.

Re-running after the verdict log is committed is permitted ONLY as a
non-mutating reproduction check via --reproduce.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

# Reuse under section 17 item 3 inheritance (reduced row schema) and locked
# infrastructure reuse (rerun gate is content-agnostic and already tested
# under Candidate B). No new shared/common module is introduced.
from candidate_b_loader import (  # noqa: E402
    FREEZE_MANIFEST_PATH,
    FROZEN_DATASETS,
    _file_sha256,
    load_reduced_phase3b_pool,
    verify_frozen_inputs,
)
from candidate_b_rerun_gate import (  # noqa: E402
    assert_byte_identical_reruns,
    canonicalize_protocol_payload,
)
from candidate_c_protocol import (  # noqa: E402
    ACTIVE_MEMO_VERSION,
    ASSET_STRAT_DIAG_SEED_C,
    B_VERDICT_LOG_PATH,
    BEAT_COUNT_THRESHOLD,
    BUCKET_COUNTS,
    DESIGN_MEMO_COMMIT,
    FREEZE_COMMIT,
    LABEL_PERM_SEED_C,
    LOCK_COMMIT,
    N_PERM,
    PROVENANCE_TOLERANCE,
)
from candidate_c_protocol import run as protocol_run  # noqa: E402


class WorkingTreeNotClean(RuntimeError):
    """Raised when non-ignored files are modified/untracked at run start."""


class RepoHeadNotDescendedFromLock(RuntimeError):
    """Raised when HEAD is not descended from C's lock-acceptance commit."""


class ReproductionDigestMismatch(RuntimeError):
    """Raised when a reproduction check produces a different payload digest."""


# Verbatim disclosure text, extracted character-exact from
# docs/candidate_c_design_memo_v0.1.md at commit 401ce45 (sections 12.4,
# 12.5, 13), markdown blockquote markers removed.

DISCLOSURE_SECTION_12_4 = (
    "The four-class verdict map compares the median PSS across the 365-anchor "
    "surface at two different temporal resolutions: ≈ 30.4 days per phase for "
    "k = 12 and ≈ 36.5 days per phase for k = 10. Median PSS is interpretable "
    "as \"typical phase-structure for this bucket count\" rather than "
    "\"phase-structure at a specific anchor configuration.\" The "
    "locked decision rules are methodologically valid as pre-registered, but "
    "the interpretation of every verdict class must acknowledge that the "
    "comparison is between two different temporal resolutions, not a test of "
    "which resolution is \"correct\" in any absolute sense:\n\n"
    "* A 12-privileged or 10-privileged verdict reflects which resolution "
    "better organizes long/short allocation on this substrate under the "
    "anchor surface, not which bucket count is structurally correct in any "
    "absolute sense.\n"
    "* A Tied / both-structured verdict reflects that both resolutions are "
    "individually non-random and cannot be distinguished from each other "
    "under the comparison threshold, not that the underlying signal is "
    "resolution-independent.\n"
    "* A Non-confirmatory / unresolved verdict does not adjudicate the "
    "resolution question at all; it states that the pre-registered decision "
    "rules do not separate the alternatives under the locked threshold "
    "structure.\n\n"
    "This caveat applies to all four verdict classes."
)

DISCLOSURE_SECTION_12_5 = (
    "The four beat counts that drive the verdict are coupled. They are "
    "derived from the same shared pool of 10,000 pooled-population is_long "
    "permutations. The verdict classes are pre-registered decision rules "
    "under that joint distribution, not independent p-value claims. The "
    "false-positive interpretation of a class assignment is therefore not "
    "identical to the false-positive rate of a single independent test at "
    "the 95th percentile, and the four classes do not partition probability "
    "mass uniformly under the null."
)

DISCLOSURE_SECTION_13 = (
    "Candidate C's verdict is conditional on a previously contacted, "
    "audit-frozen pullback-event population. The pullback Phase 1–3b "
    "series for SPY and the Phase 3b 2005–2022 series for "
    "SPY/EFA/EEM/GLD/TLT were inspected, partitioned, and used to estimate "
    "within-population statistics during pullback research before Coherent "
    "Numbers contacted them. The pullback BacktestParams were locked early at "
    "pullback commit 50ee2d1 and not re-tuned, which limits but does not "
    "eliminate that prior exposure. Candidate B previously applied 12-phase "
    "March-20-anchored machinery to this same population — specifically a "
    "10,000-element unstratified label-permutation null (§10.1 of "
    "docs/candidate_b_design_memo_v0.1.md) and an exhaustive 365-DOY "
    "anchor-control null (§10.2) — and reported the resulting verdict in "
    "results/candidate_b_results_20260514_231323_c1982503.json. Candidate C "
    "applies parallel 12-phase and 10-phase machinery to the same population "
    "under symmetrical anchor-surface rules. Candidate C's verdict is "
    "therefore conditional on (i) the pullback program's prior contact with "
    "the underlying series, and (ii) Candidate B's prior contact with the "
    "pooled Phase 3b population under 12-phase machinery. OOS 2023+ remains "
    "sealed in both repos and is out of scope for Candidate C. This "
    "disclosure is required wording; a hash citation alone does not satisfy "
    "it."
)


def check_working_tree_clean(repo_root: str) -> None:
    result = subprocess.run(
        ["git", "-C", repo_root, "status", "--short", "--untracked-files=all"],
        capture_output=True, text=True, check=True,
    )
    if result.stdout.strip():
        raise WorkingTreeNotClean(
            "non-ignored modifications or untracked files present:\n"
            + result.stdout
        )


def check_repo_head_descended_from_lock(repo_root: str, lock_commit: str) -> None:
    result = subprocess.run(
        ["git", "-C", repo_root, "merge-base", "--is-ancestor",
         lock_commit, "HEAD"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RepoHeadNotDescendedFromLock(
            "HEAD is not descended from C lock-acceptance commit {}".format(
                lock_commit
            )
        )


def get_git_head(repo_root: str) -> str:
    return subprocess.check_output(
        ["git", "-C", repo_root, "rev-parse", "HEAD"], text=True
    ).strip()


def _utc_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_tag() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d_%H%M%S")


def compose_header(
    repo_root: str,
    observed_hashes: Dict[str, str],
    manifest_sha: str,
    run_timestamp_utc: str,
    rerun_verification_digest: str,
) -> Dict[str, Any]:
    """Volatile metadata + run constants. Excluded from the rerun digest."""
    return {
        "active_memo_version": ACTIVE_MEMO_VERSION,
        "design_memo_path": "docs/candidate_c_design_memo_v0.1.md",
        "design_memo_commit": DESIGN_MEMO_COMMIT,
        "lock_acceptance_commit": LOCK_COMMIT,
        "freeze_commit": FREEZE_COMMIT,
        "freeze_manifest_path": FREEZE_MANIFEST_PATH,
        "freeze_manifest_sha256": manifest_sha,
        "repo_commit_before_run": get_git_head(repo_root),
        "working_tree_clean": True,
        "run_timestamp_utc": run_timestamp_utc,
        "frozen_csv_inputs": [
            {
                "path": p,
                "expected_sha256": FROZEN_DATASETS[p],
                "observed_sha256": observed_hashes[p],
                "match": True,
            }
            for p in sorted(FROZEN_DATASETS.keys())
        ],
        "seeds": {
            "LABEL_PERM_SEED_C": LABEL_PERM_SEED_C,
            "ASSET_STRAT_DIAG_SEED_C": ASSET_STRAT_DIAG_SEED_C,
            "N_PERM": N_PERM,
        },
        "locked_parameters": {
            "anchor_month": 3,
            "anchor_day": 20,
            "bucket_counts": list(BUCKET_COUNTS),
            "beat_count_threshold": BEAT_COUNT_THRESHOLD,
            "provenance_tolerance": PROVENANCE_TOLERANCE,
        },
        "rerun_verification_digest": rerun_verification_digest,
    }


def render_markdown(full: Dict[str, Any]) -> str:
    h = full["header"]
    p = full["protocol_payload"]
    bc = p["beat_counts"]
    tp = p["threshold_pass"]
    lines = [
        "# Candidate C v0.1 — Verdict",
        "",
        "**Active memo:** `{}` ({})".format(
            h["design_memo_path"], h["active_memo_version"]
        ),
        "**Design memo commit:** `{}`".format(h["design_memo_commit"]),
        "**Lock-acceptance commit:** `{}`".format(h["lock_acceptance_commit"]),
        "**Freeze commit:** `{}`".format(h["freeze_commit"]),
        "**Run timestamp (UTC):** {}".format(h["run_timestamp_utc"]),
        "**Repo commit before run:** `{}`".format(h["repo_commit_before_run"]),
        "**Rerun verification digest:** `{}`".format(
            h["rerun_verification_digest"]
        ),
        "",
        "## Verdict",
        "",
        "- **Verdict class:** **{}**".format(p["verdict_class"]),
        "- **Observed median PSS (k=12):** {:.8f}".format(
            p["observed"]["median_12_observed"]
        ),
        "- **Observed median PSS (k=10):** {:.8f}".format(
            p["observed"]["median_10_observed"]
        ),
        "- **diff_observed (12 - 10):** {:.8f}".format(
            p["observed"]["diff_observed"]
        ),
        "",
        "### Beat counts (threshold {} of {})".format(
            h["locked_parameters"]["beat_count_threshold"], h["seeds"]["N_PERM"]
        ),
        "",
        "- `beat_count_12_individual` = {}  (pass={})".format(
            bc["beat_count_12_individual"], tp["beat_count_12_individual"]
        ),
        "- `beat_count_10_individual` = {}  (pass={})".format(
            bc["beat_count_10_individual"], tp["beat_count_10_individual"]
        ),
        "- `beat_count_comparison_12` = {}  (pass={})".format(
            bc["beat_count_comparison_12"], tp["beat_count_comparison_12"]
        ),
        "- `beat_count_comparison_10` = {}  (pass={})".format(
            bc["beat_count_comparison_10"], tp["beat_count_comparison_10"]
        ),
        "",
        "## Verbalization (verbatim §12.2 block for the assigned class)",
        "",
        p["verbalization"],
        "",
        "## §12.4 Granularity caveat (verbatim)",
        "",
        full["disclosure_paragraph_section_12_4"],
        "",
        "## §12.5 Compound-verdict disclosure (verbatim)",
        "",
        full["disclosure_paragraph_section_12_5"],
        "",
        "## §13 Data-contact disclosure (verbatim)",
        "",
        full["disclosure_paragraph_section_13"],
        "",
    ]
    return "\n".join(lines)


def assemble_full(header: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "candidate_c_v0.1",
        "header": header,
        "protocol_payload": payload,
        "disclosure_paragraph_section_12_4": DISCLOSURE_SECTION_12_4,
        "disclosure_paragraph_section_12_5": DISCLOSURE_SECTION_12_5,
        "disclosure_paragraph_section_13": DISCLOSURE_SECTION_13,
    }


def write_verdict_log(
    repo_root: str, header: Dict[str, Any], payload: Dict[str, Any]
) -> Dict[str, str]:
    digest = header["rerun_verification_digest"]
    short = digest[:8]
    run_tag = _utc_tag()
    results_dir = os.path.join(repo_root, "results")
    os.makedirs(results_dir, exist_ok=True)
    json_path = os.path.join(
        results_dir, "candidate_c_results_{}_{}.json".format(run_tag, short)
    )
    md_path = os.path.join(
        results_dir, "candidate_c_results_{}_{}.md".format(run_tag, short)
    )
    full = assemble_full(header, payload)
    with open(json_path, "w") as fh:
        json.dump(full, fh, indent=2, sort_keys=True, ensure_ascii=False)
    with open(md_path, "w") as fh:
        fh.write(render_markdown(full))
    return {"json": json_path, "md": md_path}


def run_locked(repo_root: str = REPO_ROOT) -> Dict[str, str]:
    check_working_tree_clean(repo_root)
    check_repo_head_descended_from_lock(repo_root, LOCK_COMMIT)

    observed_hashes = verify_frozen_inputs(repo_root)
    reduced = load_reduced_phase3b_pool(repo_root)
    verify_frozen_inputs(repo_root)  # defense in depth: re-verify post-load.

    b_log_path = os.path.join(repo_root, B_VERDICT_LOG_PATH)

    def runner_call():
        return protocol_run(reduced, b_log_path)

    canonical_bytes = assert_byte_identical_reruns(runner_call)
    rerun_digest = hashlib.sha256(canonical_bytes).hexdigest()

    verify_frozen_inputs(repo_root)  # third check inside the gate window.
    payload = protocol_run(reduced, b_log_path)

    manifest_sha = _file_sha256(os.path.join(repo_root, FREEZE_MANIFEST_PATH))
    header = compose_header(
        repo_root=repo_root,
        observed_hashes=observed_hashes,
        manifest_sha=manifest_sha,
        run_timestamp_utc=_utc_iso(),
        rerun_verification_digest=rerun_digest,
    )
    return write_verdict_log(repo_root, header, payload)


def run_reproduction_check(
    previous_json_path: str, repo_root: str = REPO_ROOT
) -> Dict[str, Any]:
    with open(previous_json_path, "r") as fh:
        original = json.load(fh)
    previous_digest = original["header"]["rerun_verification_digest"]

    verify_frozen_inputs(repo_root)
    reduced = load_reduced_phase3b_pool(repo_root)
    b_log_path = os.path.join(repo_root, B_VERDICT_LOG_PATH)
    payload = protocol_run(reduced, b_log_path)
    new_canonical = canonicalize_protocol_payload(payload)
    new_digest = hashlib.sha256(new_canonical).hexdigest()

    repro_dir = os.path.join(
        repo_root, "results",
        "candidate_c_reproduction_check_{}".format(_utc_tag()),
    )
    os.makedirs(repro_dir)
    match = previous_digest == new_digest
    comparison = {
        "previous_digest": previous_digest,
        "new_digest": new_digest,
        "match": match,
    }
    with open(os.path.join(repro_dir, "header.json"), "w") as fh:
        json.dump(
            {
                "run_timestamp_utc": _utc_iso(),
                "output_dir": repro_dir,
                "repo_head": get_git_head(repo_root),
                "previous_verdict_log_path": previous_json_path,
                "reproduction_status": "match" if match else "mismatch",
            },
            fh, indent=2, sort_keys=True,
        )
    with open(os.path.join(repro_dir, "protocol_payload.json"), "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True, ensure_ascii=False)
    with open(
        os.path.join(repro_dir, "reproduction_digest_comparison.json"), "w"
    ) as fh:
        json.dump(comparison, fh, indent=2, sort_keys=True)
    if match:
        with open(
            os.path.join(repro_dir, "_reproduction_success.md"), "w"
        ) as fh:
            fh.write(
                "Reproduction success. Digest {} matches.\n".format(new_digest)
            )
        return {"status": "match", "dir": repro_dir, "comparison": comparison}
    with open(os.path.join(repro_dir, "_reproduction_failure.md"), "w") as fh:
        fh.write(
            "Reproduction FAILURE.\nPrevious: {}\nNew:      {}\n".format(
                previous_digest, new_digest
            )
        )
    raise ReproductionDigestMismatch(previous_digest, new_digest)


def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Candidate C v0.1 locked-protocol runner"
    )
    p.add_argument(
        "--reproduce", default=None,
        help="Path to a previously committed verdict JSON; runs a "
             "non-mutating reproduction check.",
    )
    return p


if __name__ == "__main__":
    args = build_argparser().parse_args()
    if args.reproduce:
        run_reproduction_check(args.reproduce)
    else:
        run_locked()
