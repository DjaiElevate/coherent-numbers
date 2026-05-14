"""Candidate B v0.1 locked-protocol runner — single official invocation.

Reads the six frozen pullback CSVs under SHA-256 verification, constructs
the reduced in-memory view, runs the locked protocol twice through the
rerun gate, and writes the verdict log to results/.

Re-running this script after the verdict log is committed is permitted ONLY
as a non-mutating reproduction check via --reproduce. The original committed
verdict log is never modified.

This script is the runner. The numeric protocol lives in
src/candidate_b_protocol.py. This file is responsible for pre-flight checks,
provenance capture, header composition, rerun-gating, and artifact writing.
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

from candidate_b_loader import (  # noqa: E402
    FREEZE_MANIFEST_PATH,
    FROZEN_DATASETS,
    FrozenCsvHashMismatch,
    OosRowDetected,
    _file_sha256,
    load_reduced_phase3b_pool,
    verify_frozen_inputs,
)
from candidate_b_protocol import (  # noqa: E402
    ACTIVE_MEMO_VERSION,
    ANCHOR_BEAT_THRESHOLD,
    ASSET_STRAT_DIAG_SEED,
    DESIGN_MEMO_COMMIT,
    FREEZE_COMMIT,
    LABEL_PERM_SEED,
    LOCK_COMMIT,
    N_PERM,
    PERM_BEAT_THRESHOLD,
)
from candidate_b_protocol import run as protocol_run  # noqa: E402
from candidate_b_rerun_gate import (  # noqa: E402
    RerunInconsistency,
    assert_byte_identical_reruns,
    canonicalize_protocol_payload,
)


class WorkingTreeNotClean(RuntimeError):
    """Raised when non-ignored files are modified/untracked at run start."""


class RepoHeadNotDescendedFromLock(RuntimeError):
    """Raised when HEAD is not descended from the lock-acceptance commit."""


class ReproductionDigestMismatch(RuntimeError):
    """Raised when a reproduction check produces a different protocol-payload digest."""


DISCLOSURE_SECTION_13 = (
    "Candidate B's verdict is conditional on a previously contacted, "
    "audit-frozen pullback-event population. The pullback Phase 1-3b series "
    "for SPY and the Phase 3b 2005-2022 series for SPY/EFA/EEM/GLD/TLT were "
    "inspected, partitioned, and used to estimate within-population statistics "
    "during pullback research before Coherent Numbers contacted them. The "
    "pullback BacktestParams were locked early at pullback commit 50ee2d1 and "
    "not re-tuned, which limits but does not eliminate this exposure. OOS "
    "2023+ remains sealed and is out of scope for B."
)


def check_working_tree_clean(repo_root: str) -> None:
    """Raise WorkingTreeNotClean if any non-ignored file is dirty or untracked."""
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
    """Raise RepoHeadNotDescendedFromLock if HEAD is not a descendant of lock_commit."""
    result = subprocess.run(
        ["git", "-C", repo_root, "merge-base", "--is-ancestor", lock_commit, "HEAD"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RepoHeadNotDescendedFromLock(
            "HEAD is not descended from lock-acceptance commit {}".format(lock_commit)
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
    """Compose the verdict-log header (volatile metadata + run constants).

    The contents of this header are deliberately EXCLUDED from
    rerun_verification_digest itself, per the digest-scope clarification.
    """
    return {
        "active_memo_version": ACTIVE_MEMO_VERSION,
        "design_memo_path": "docs/candidate_b_design_memo_v0.1.md",
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
            "LABEL_PERM_SEED": LABEL_PERM_SEED,
            "ASSET_STRAT_DIAG_SEED": ASSET_STRAT_DIAG_SEED,
            "N_PERM": N_PERM,
        },
        "locked_parameters": {
            "anchor_month": 3,
            "anchor_day": 20,
            "bucket_count": 12,
            "perm_beat_threshold": PERM_BEAT_THRESHOLD,
            "anchor_beat_threshold": ANCHOR_BEAT_THRESHOLD,
        },
        "rerun_verification_digest": rerun_verification_digest,
    }


def render_markdown(full: Dict[str, Any]) -> str:
    h = full["header"]
    p = full["protocol_payload"]
    lines = [
        "# Candidate B v0.1 — Verdict",
        "",
        "**Active memo:** `{}` ({})".format(h["design_memo_path"], h["active_memo_version"]),
        "**Design memo commit:** `{}`".format(h["design_memo_commit"]),
        "**Lock-acceptance commit:** `{}`".format(h["lock_acceptance_commit"]),
        "**Freeze commit:** `{}`".format(h["freeze_commit"]),
        "**Run timestamp (UTC):** {}".format(h["run_timestamp_utc"]),
        "**Repo commit before run:** `{}`".format(h["repo_commit_before_run"]),
        "**Rerun verification digest:** `{}`".format(h["rerun_verification_digest"]),
        "",
        "## Verdict",
        "",
        "- **Verdict:** **{}**".format(p["verdict"]),
        "- **Verbalization class:** {}".format(p["verbalization_class"]),
        "- **Observed PSS_B1:** {:.6f}".format(p["observed_pss_b1"]),
        "- **N.1 beat count:** {} / {} (strict pct {:.4f}; threshold {})".format(
            p["beat_count_perm"], h["seeds"]["N_PERM"],
            p["perm_strict_percentile"], h["locked_parameters"]["perm_beat_threshold"],
        ),
        "- **N.2 beat count:** {} / 365 (strict pct {:.4f}; threshold {})".format(
            p["beat_count_anchor"], p["anchor_strict_percentile"],
            h["locked_parameters"]["anchor_beat_threshold"],
        ),
        "",
        "## Data-contact disclosure (section 13)",
        "",
        full["disclosure_paragraph_section_13"],
        "",
    ]
    return "\n".join(lines)


def write_verdict_log(
    repo_root: str, header: Dict[str, Any], payload: Dict[str, Any]
) -> Dict[str, str]:
    """Write the JSON + MD verdict sidecars to results/. Returns the two paths."""
    digest = header["rerun_verification_digest"]
    short = digest[:8]
    run_tag = _utc_tag()
    results_dir = os.path.join(repo_root, "results")
    os.makedirs(results_dir, exist_ok=True)
    json_path = os.path.join(
        results_dir, "candidate_b_results_{}_{}.json".format(run_tag, short)
    )
    md_path = os.path.join(
        results_dir, "candidate_b_results_{}_{}.md".format(run_tag, short)
    )

    full = {
        "schema_version": "candidate_b_v0.1",
        "header": header,
        "protocol_payload": payload,
        "disclosure_paragraph_section_13": DISCLOSURE_SECTION_13,
    }
    with open(json_path, "w") as f:
        json.dump(full, f, indent=2, sort_keys=True)
    with open(md_path, "w") as f:
        f.write(render_markdown(full))
    return {"json": json_path, "md": md_path}


def run_locked(repo_root: str = REPO_ROOT) -> Dict[str, str]:
    check_working_tree_clean(repo_root)
    check_repo_head_descended_from_lock(repo_root, LOCK_COMMIT)

    observed_hashes = verify_frozen_inputs(repo_root)
    reduced = load_reduced_phase3b_pool(repo_root)
    verify_frozen_inputs(repo_root)  # defense in depth: re-verify post-load.

    def runner_call():
        return protocol_run(reduced)

    canonical_bytes = assert_byte_identical_reruns(runner_call)
    rerun_digest = hashlib.sha256(canonical_bytes).hexdigest()

    verify_frozen_inputs(repo_root)  # third hash check inside the gate window.
    payload = protocol_run(reduced)

    manifest_sha = _file_sha256(os.path.join(repo_root, FREEZE_MANIFEST_PATH))
    header = compose_header(
        repo_root=repo_root,
        observed_hashes=observed_hashes,
        manifest_sha=manifest_sha,
        run_timestamp_utc=_utc_iso(),
        rerun_verification_digest=rerun_digest,
    )

    return write_verdict_log(repo_root, header, payload)


def run_reproduction_check(previous_json_path: str, repo_root: str = REPO_ROOT) -> Dict[str, Any]:
    """Reproduction check — never overwrites the original committed verdict log."""
    with open(previous_json_path, "r") as f:
        original = json.load(f)
    previous_digest = original["header"]["rerun_verification_digest"]

    verify_frozen_inputs(repo_root)
    reduced = load_reduced_phase3b_pool(repo_root)
    payload = protocol_run(reduced)
    new_canonical = canonicalize_protocol_payload(payload)
    new_digest = hashlib.sha256(new_canonical).hexdigest()

    repro_dir = os.path.join(
        repo_root, "results", "candidate_b_reproduction_check_{}".format(_utc_tag())
    )
    os.makedirs(repro_dir)

    match = previous_digest == new_digest
    comparison = {
        "previous_digest": previous_digest,
        "new_digest": new_digest,
        "match": match,
    }
    repro_header = {
        "run_timestamp_utc": _utc_iso(),
        "output_dir": repro_dir,
        "repo_head": get_git_head(repo_root),
        "previous_verdict_log_path": previous_json_path,
        "reproduction_status": "match" if match else "mismatch",
    }

    with open(os.path.join(repro_dir, "header.json"), "w") as f:
        json.dump(repro_header, f, indent=2, sort_keys=True)
    with open(os.path.join(repro_dir, "protocol_payload.json"), "w") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
    with open(os.path.join(repro_dir, "reproduction_digest_comparison.json"), "w") as f:
        json.dump(comparison, f, indent=2, sort_keys=True)

    if match:
        with open(os.path.join(repro_dir, "_reproduction_success.md"), "w") as f:
            f.write(
                "Reproduction success. Digest {} matches the committed verdict log.\n".format(
                    new_digest
                )
            )
        return {"status": "match", "dir": repro_dir, "comparison": comparison}
    else:
        with open(os.path.join(repro_dir, "_reproduction_failure.md"), "w") as f:
            f.write(
                "Reproduction FAILURE.\nPrevious digest: {}\nNew digest:      {}\n".format(
                    previous_digest, new_digest
                )
            )
        raise ReproductionDigestMismatch(previous_digest, new_digest)


def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Candidate B v0.1 locked-protocol runner")
    p.add_argument(
        "--reproduce", default=None,
        help="Path to a previously committed verdict JSON; runs a non-mutating reproduction check.",
    )
    return p


if __name__ == "__main__":
    args = build_argparser().parse_args()
    if args.reproduce:
        run_reproduction_check(args.reproduce)
    else:
        run_locked()
