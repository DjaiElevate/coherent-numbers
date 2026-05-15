"""Influential Numbers Cell 1 v0.1 locked-protocol runner.

Single official invocation. Parallel to scripts/run_candidate_c_protocol.py
(commit 4432591). Reads the six frozen pullback CSVs under SHA-256
verification via Candidate B's already-tested loader (generic, non
result-defining), constructs the reduced in-memory view, runs the locked
Cell 1 protocol twice through the content-agnostic rerun gate, and writes the
verdict log to results/.

Re-running after the verdict log is committed is permitted ONLY as a
non-mutating reproduction check via --reproduce.

Result-defining logic lives entirely in influential_numbers_cell_1_protocol
(design memo section 19). No Candidate C module is imported; only the generic
candidate_b_loader / candidate_b_rerun_gate utilities are reused.
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
from typing import Any, Dict, Optional

REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

# Generic, content-agnostic infrastructure reuse (design memo section 19): the
# loader and rerun gate are already tested under Candidate B and define no
# Cell 1 result. No new shared/common module is introduced.
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
from influential_numbers_cell_1_protocol import (  # noqa: E402
    ACTIVE_MEMO_VERSION,
    ASSET_STRAT_DIAG_SEED_CELL1,
    BEAT_COUNT_THRESHOLD,
    CANDIDATE_C_VERDICT_LOG_PATH,
    DESIGN_MEMO_COMMIT,
    FRAMEWORK_MEMO_COMMIT,
    FREEZE_COMMIT,
    LABEL_PERM_SEED_CELL1,
    LOCK_COMMIT,
    N_PERM,
    PROVENANCE_TOLERANCE,
)
from influential_numbers_cell_1_protocol import run as protocol_run  # noqa: E402

SCHEMA_VERSION = "influential_numbers_cell_1_v0.1"
OUTPUT_STEM = "influential_numbers_cell_1_results"
DESIGN_MEMO_PATH = "docs/influential_numbers_cell_1_design_memo_v0.1.md"
LOCK_ACCEPTANCE_COMMIT = "3d44e9e"


class WorkingTreeNotClean(RuntimeError):
    """Raised when non-ignored files are modified/untracked at run start."""


class RepoHeadNotDescendedFromLock(RuntimeError):
    """Raised when HEAD is not descended from Cell 1's lock-acceptance commit."""


class ReproductionDigestMismatch(RuntimeError):
    """Raised when a reproduction check produces a different payload digest."""


# Required-verbatim disclosure text, extracted character-exact from
# docs/influential_numbers_cell_1_design_memo_v0.1.md at commit a765098.
# Convention (mirrors Candidate C / Stage B): each constant equals the memo
# body line with its leading Markdown structural prefix removed only -- "> "
# for the blockquote sections (15.5, 15.6, 20) and "* " for the guardrail
# bullets (21.3, 21.4). Nothing else is altered. Stage D tests verify each
# constant against the locked memo. Do not paraphrase; do not edit wording.

DISCLOSURE_SECTION_15_5 = (
    "*(REQUIRED-VERBATIM, §15.5):* Every Cell 1 verdict is scope-bounded "
    "by the locked neighborhood operationalization. \"Neighborhood\" here "
    "means a `±3` linear-integer window of bucket counts evaluated as "
    "the median of each bucket count's 365-anchor PSS surface; different "
    "bucket counts correspond to different temporal resolutions (e.g. `k = "
    "12` ≈ 30.4 days/phase, `k = 16` ≈ 22.8 days/phase, `k = 7` "
    "≈ 52 days/phase). A neighborhood verdict reflects how "
    "phase-allocation structure varies with bucket-count resolution near the "
    "focal, not a claim that any bucket count is structurally \"correct,\" "
    "and not a test of divisor/multiple/harmonic/12-family structure. This "
    "caveat applies to all four verdict classes."
)

DISCLOSURE_SECTION_15_6 = (
    "*(REQUIRED-VERBATIM, §15.6):* The two primary beat counts "
    "(`beat_count_12_structure`, `beat_count_max_gap`) are coupled: both are "
    "derived from the same shared pool of 10,000 pooled-population `is_long` "
    "permutations, and the per-permutation attenuation scores entering both "
    "are functions of the same recomputed `K`-wide median-PSS map. The "
    "verdict classes are pre-registered decision rules under that joint "
    "distribution, not independent p-value claims. The false-positive "
    "interpretation of a class assignment is not identical to the "
    "false-positive rate of a single independent test at the 95th "
    "percentile, and the four classes do not partition probability mass "
    "uniformly under the null."
)

DISCLOSURE_SECTION_20 = (
    "*(REQUIRED-VERBATIM, §20):* Cell 1's verdict is conditional on a "
    "previously contacted, audit-frozen pullback-event population. The "
    "pullback Phase 1–3b series for SPY and the Phase 3b 2005–2022 "
    "series for SPY/EFA/EEM/GLD/TLT were inspected, partitioned, and used to "
    "estimate within-population statistics during pullback research before "
    "Coherent Numbers contacted them. The pullback BacktestParams were locked "
    "early at pullback commit 50ee2d1 and not re-tuned, which limits but does "
    "not eliminate that prior exposure. Candidate B previously applied "
    "12-phase March-20-anchored machinery to this same population (a "
    "10,000-element unstratified label-permutation null and an exhaustive "
    "365-DOY anchor-control null) and reported a split-null verdict. "
    "Candidate C subsequently applied parallel 12-phase and 10-phase "
    "machinery to the same population under symmetrical 365-DOY "
    "anchor-surface rules and reported a 12-privileged verdict. Cell 1 "
    "applies a multi-focal neighborhood operationalization over bucket counts "
    "K = {7,…,19} to the same population. Cell 1's verdict is therefore "
    "conditional on (i) the pullback program's prior contact with the "
    "underlying series, (ii) Candidate B's prior 12-phase contact, and (iii) "
    "Candidate C's prior 12-and-10-phase contact, including the k=10 and k=12 "
    "365-anchor surfaces Cell 1 reuses as a provenance check. OOS 2023+ "
    "remains sealed in both repos and is out of scope for Cell 1. This "
    "disclosure is required wording; a hash citation alone does not satisfy "
    "it."
)

DISCLOSURE_SECTION_21_3 = (
    "**21.3 (REQUIRED-VERBATIM anti-rescue — Layer 1 / Layer 2):** "
    "Layer 2 (divisor, multiple, 12-family/duodecimal, harmonic-family, "
    "recursive-field, or weighted-neighbor influence) is out of scope for "
    "Cell 1 and may not be added as a \"diagnostic,\" may not be used to "
    "rescue a Class 2/3/4 verdict, and may not borrow authority from the "
    "Kryon source. If a Layer 1 null (Class 3) or non-confirmatory result "
    "(Class 4) is followed by any Layer 2 consideration, it requires a "
    "separate decision memo explaining why Layer 2 remains scientifically "
    "justified on its own grounds; it is never an escape hatch from a "
    "Layer 1 null."
)

DISCLOSURE_SECTION_21_4 = (
    "**21.4 (REQUIRED-VERBATIM anti-rescue — cross-cell):** Candidate "
    "C's `12-privileged` verdict remains independent and is not "
    "retroactively reinterpreted by any Cell 1 outcome. Candidate B's "
    "split-null equinox result remains **not confirmed** and is not rescued, "
    "confirmed, or reinterpreted by any Cell 1 outcome. \"12 beat 10 under "
    "Candidate C's locked rules\" and \"Cell 1's neighborhood verdict\" are "
    "distinct claims that do not transfer authority in either direction."
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


def check_repo_head_descended_from_lock(
    repo_root: str, lock_commit: str
) -> None:
    result = subprocess.run(
        ["git", "-C", repo_root, "merge-base", "--is-ancestor",
         lock_commit, "HEAD"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RepoHeadNotDescendedFromLock(
            "HEAD is not descended from Cell 1 lock-acceptance commit "
            "{}".format(lock_commit)
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
        "framework_memo_commit": FRAMEWORK_MEMO_COMMIT,
        "design_memo_path": DESIGN_MEMO_PATH,
        "design_memo_commit": DESIGN_MEMO_COMMIT,
        "lock_acceptance_commit": LOCK_ACCEPTANCE_COMMIT,
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
            "LABEL_PERM_SEED_CELL1": LABEL_PERM_SEED_CELL1,
            "ASSET_STRAT_DIAG_SEED_CELL1": ASSET_STRAT_DIAG_SEED_CELL1,
            "N_PERM": N_PERM,
        },
        "locked_parameters": {
            "anchor_month": 3,
            "anchor_day": 20,
            "bucket_counts": list(range(7, 20)),
            "focal_centers": [10, 12, 14, 16],
            "primary_focal": 12,
            "control_focals": [10, 14, 16],
            "window_radius": 3,
            "anchor_population_size": 365,
            "n_perm": N_PERM,
            "beat_count_threshold": BEAT_COUNT_THRESHOLD,
            "provenance_tolerance": PROVENANCE_TOLERANCE,
        },
        "rerun_verification_digest": rerun_verification_digest,
    }


def _fmt(value: Any, spec: str = "{}") -> str:
    if value is None:
        return "n/a"
    try:
        return spec.format(value)
    except (ValueError, TypeError):
        return str(value)


def render_markdown(full: Dict[str, Any]) -> str:
    h = full["header"]
    p = full["protocol_payload"]
    gate = p.get("focal_elevation_gate_12", {})
    attn = p.get("attenuation_scores", {})
    mg = p.get("max_gap", {})
    bc = p.get("beat_counts", {})
    tp = p.get("threshold_pass", {})
    prov = p.get("provenance_check", {})
    asd = p.get("asset_stratified_diagnostic", {})
    lp = h["locked_parameters"]
    lines = [
        "# Influential Numbers Cell 1 v0.1 — Verdict",
        "",
        "**Active memo:** `{}` ({})".format(
            h["design_memo_path"], h["active_memo_version"]
        ),
        "**Framework memo commit:** `{}`".format(h["framework_memo_commit"]),
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
        "- **Verdict class:** **{}**".format(p.get("verdict_class")),
        "- **Machine label:** `{}`".format(p.get("verdict_class_machine")),
        "- **Pathology:** {}".format(_fmt(p.get("pathology"))),
        "",
        "### Focal-elevation gate (k = 12)",
        "",
        "- `pass` = {}".format(gate.get("pass")),
        "- `median_12` = {}".format(_fmt(gate.get("median_12"), "{:.10f}")),
        "- `neighbor_mean` = {}".format(
            _fmt(gate.get("neighbor_mean"), "{:.10f}")
        ),
        "- `focal_excess` = {}".format(
            _fmt(gate.get("focal_excess"), "{:.10f}")
        ),
        "- `ambiguous` = {}".format(gate.get("ambiguous")),
        "- `ambiguity_reason` = {}".format(_fmt(gate.get("ambiguity_reason"))),
        "",
        "### Attenuation scores (per focal)",
        "",
    ]
    for f in ("10", "12", "14", "16"):
        lines.append(
            "- focal `{}` : attenuation_score = {}".format(
                f, _fmt(attn.get(f), "{:.10f}")
            )
        )
    lines += [
        "",
        "### max_gap contrast",
        "",
        "- `max_gap` = {}".format(_fmt(mg.get("max_gap"), "{:.10f}")),
        "- `score_12` = {}".format(_fmt(mg.get("score_12"), "{:.10f}")),
        "- `strongest_control_focal` = {}".format(
            _fmt(mg.get("strongest_control_focal"))
        ),
        "- `strongest_control_score` = {}".format(
            _fmt(mg.get("strongest_control_score"), "{:.10f}")
        ),
        "",
        "### Beat counts (threshold {} of {})".format(
            lp["beat_count_threshold"], h["seeds"]["N_PERM"]
        ),
        "",
        "- `beat_count_12_structure` = {}  (pass={})".format(
            bc.get("beat_count_12_structure"),
            tp.get("beat_count_12_structure"),
        ),
        "- `beat_count_max_gap` = {}  (pass={})".format(
            bc.get("beat_count_max_gap"), tp.get("beat_count_max_gap")
        ),
        "",
        "### Provenance gate vs Candidate C surfaces (validity gate, "
        "not a diagnostic)",
        "",
        "- `pass` = {}".format(prov.get("pass")),
        "- `max_abs_diff_10` = {}".format(
            _fmt(prov.get("max_abs_diff_10"))
        ),
        "- `max_abs_diff_12` = {}".format(
            _fmt(prov.get("max_abs_diff_12"))
        ),
        "- `n_anchors_checked_10` = {}".format(
            _fmt(prov.get("n_anchors_checked_10"))
        ),
        "- `n_anchors_checked_12` = {}".format(
            _fmt(prov.get("n_anchors_checked_12"))
        ),
        "- `tolerance` = {}".format(_fmt(prov.get("tolerance"))),
        "- `candidate_c_json_sha256` = {}".format(
            _fmt(prov.get("candidate_c_json_sha256"))
        ),
        "- `failure_reason` = {}".format(_fmt(prov.get("failure_reason"))),
        "",
        "### Asset-stratified diagnostic (non-verdict)",
        "",
        "- `asset_stratified_beat_count_12_structure` = {}".format(
            asd.get("asset_stratified_beat_count_12_structure")
        ),
        "- `asset_stratified_beat_count_max_gap` = {}".format(
            asd.get("asset_stratified_beat_count_max_gap")
        ),
        "",
        "## Verbalization (verbatim §15.x (a)/(b) block for the "
        "assigned class)",
        "",
        p.get("verbalization", ""),
        "",
        "## §15.5 Granularity / neighborhood-window caveat (verbatim)",
        "",
        full["disclosure_paragraph_section_15_5"],
        "",
        "## §15.6 Compound-verdict / coupled-null disclosure (verbatim)",
        "",
        full["disclosure_paragraph_section_15_6"],
        "",
        "## §20 Data-contact disclosure (verbatim)",
        "",
        full["disclosure_paragraph_section_20"],
        "",
        "## §21.3 Layer 1 / Layer 2 anti-rescue (verbatim)",
        "",
        full["disclosure_paragraph_section_21_3"],
        "",
        "## §21.4 Cross-cell anti-rescue (verbatim)",
        "",
        full["disclosure_paragraph_section_21_4"],
        "",
    ]
    return "\n".join(lines)


def assemble_full(
    header: Dict[str, Any], payload: Dict[str, Any]
) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "header": header,
        "protocol_payload": payload,
        "disclosure_paragraph_section_15_5": DISCLOSURE_SECTION_15_5,
        "disclosure_paragraph_section_15_6": DISCLOSURE_SECTION_15_6,
        "disclosure_paragraph_section_20": DISCLOSURE_SECTION_20,
        "disclosure_paragraph_section_21_3": DISCLOSURE_SECTION_21_3,
        "disclosure_paragraph_section_21_4": DISCLOSURE_SECTION_21_4,
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
        results_dir, "{}_{}_{}.json".format(OUTPUT_STEM, run_tag, short)
    )
    md_path = os.path.join(
        results_dir, "{}_{}_{}.md".format(OUTPUT_STEM, run_tag, short)
    )
    full = assemble_full(header, payload)
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(full, fh, indent=2, sort_keys=True, ensure_ascii=False)
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(render_markdown(full))
    return {"json": json_path, "md": md_path}


def run_locked(repo_root: str = REPO_ROOT) -> Dict[str, str]:
    check_working_tree_clean(repo_root)
    check_repo_head_descended_from_lock(repo_root, LOCK_COMMIT)

    observed_hashes = verify_frozen_inputs(repo_root)
    reduced = load_reduced_phase3b_pool(repo_root)
    verify_frozen_inputs(repo_root)  # defense in depth: re-verify post-load.

    c_log_path = os.path.join(repo_root, CANDIDATE_C_VERDICT_LOG_PATH)

    def runner_call():
        verify_frozen_inputs(repo_root)  # re-verify inside the gate window.
        return protocol_run(reduced, c_log_path)

    canonical_bytes = assert_byte_identical_reruns(runner_call)
    rerun_digest = hashlib.sha256(canonical_bytes).hexdigest()

    verify_frozen_inputs(repo_root)  # third check inside the gate window.
    payload = protocol_run(reduced, c_log_path)

    manifest_sha = _file_sha256(
        os.path.join(repo_root, FREEZE_MANIFEST_PATH)
    )
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
    with open(previous_json_path, "r", encoding="utf-8") as fh:
        original = json.load(fh)
    previous_digest = original["header"]["rerun_verification_digest"]

    verify_frozen_inputs(repo_root)
    reduced = load_reduced_phase3b_pool(repo_root)
    c_log_path = os.path.join(repo_root, CANDIDATE_C_VERDICT_LOG_PATH)
    payload = protocol_run(reduced, c_log_path)
    new_canonical = canonicalize_protocol_payload(payload)
    new_digest = hashlib.sha256(new_canonical).hexdigest()

    repro_dir = os.path.join(
        repo_root, "results",
        "influential_numbers_cell_1_reproduction_check_{}".format(_utc_tag()),
    )
    os.makedirs(repro_dir)
    match = previous_digest == new_digest
    comparison = {
        "previous_digest": previous_digest,
        "new_digest": new_digest,
        "match": match,
    }
    with open(
        os.path.join(repro_dir, "header.json"), "w", encoding="utf-8"
    ) as fh:
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
    with open(
        os.path.join(repro_dir, "protocol_payload.json"), "w",
        encoding="utf-8",
    ) as fh:
        json.dump(payload, fh, indent=2, sort_keys=True, ensure_ascii=False)
    with open(
        os.path.join(repro_dir, "reproduction_digest_comparison.json"), "w",
        encoding="utf-8",
    ) as fh:
        json.dump(comparison, fh, indent=2, sort_keys=True)
    if match:
        with open(
            os.path.join(repro_dir, "_reproduction_success.md"), "w",
            encoding="utf-8",
        ) as fh:
            fh.write(
                "Reproduction success. Digest {} matches.\n".format(new_digest)
            )
        return {"status": "match", "dir": repro_dir, "comparison": comparison}
    with open(
        os.path.join(repro_dir, "_reproduction_failure.md"), "w",
        encoding="utf-8",
    ) as fh:
        fh.write(
            "Reproduction FAILURE.\nPrevious: {}\nNew:      {}\n".format(
                previous_digest, new_digest
            )
        )
    raise ReproductionDigestMismatch(previous_digest, new_digest)


def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Influential Numbers Cell 1 v0.1 locked-protocol runner"
    )
    p.add_argument(
        "--reproduce", default=None,
        help="Path to a previously committed verdict JSON; runs a "
             "non-mutating reproduction check.",
    )
    return p


def main(argv: Optional[Any] = None) -> Dict[str, Any]:
    args = build_argparser().parse_args(argv)
    if args.reproduce:
        return run_reproduction_check(args.reproduce)
    return run_locked()


if __name__ == "__main__":
    main()
