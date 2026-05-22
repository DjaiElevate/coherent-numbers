# Lane 2 GDELT1 Count-Feasibility v0.2 Post-Run Report

## 1. Status

This report is now written to disk at `docs/lane2_gdelt1_gate5_post_run_report_v0.2.md` under a disk-write-only authorization. It is **not** committed by this turn; staging, committing, and pushing require a separate explicit prompt. No execution, rerun, guard flip, network call, memory update, or downstream design decision is authorized by this disk-write turn.

The Lane 2 GDELT1 count-only feasibility v0.2 run produced verdict **`RUN-HALTED-BOUNDARY`**.

## 2. Authorization chain

The run sits at the end of a four-anchor chain on `origin/main`:

| Role | Commit | Notes |
|---|---|---|
| v0.2 authorization anchor | `57f42cc6d2e4170bc32f477853f6aeeaa4bd633c` | Committed Gate 5 v0.2 run-enablement memo locking the §6 binding caveat; verdict `AUTHORIZE COUNT-FEASIBILITY LATER`. |
| Enablement commit | `89a5bcb785e25e52757a60cc313dfdb36c1aece9` | Single-file edit to `scripts/run_lane2_gdelt1_count_feasibility.py`; flipped `COUNT_FEASIBILITY_AUTHORIZED = False → True`; comment block updated to cite `57f42cc` and the §6 caveat. Pushed fast-forward `57f42cc..89a5bcb`. |
| Inert-restore commit | `a6e5ebb018979c32a297e026b9ad915910944654` | Same file; flipped `True → False` and recorded the RUN-HALTED-BOUNDARY outcome and `rejected_2023plus=1219` in the surrounding comment. Pushed fast-forward `89a5bcb..a6e5ebb`. |

v0.2 memo: `docs/lane2_gdelt1_gate5_run_enablement_memo_v0.2.md`, SHA-256 `d7e8bbf45940ca139f8b68e8302b214f8fad4ae2c35f76142be7b7fc23dcf276` (byte-identical to the SHA in MEMORY).

Count-feasibility execution was attempted **exactly once** (one runner invocation that loaded the runner module and entered `run_count_feasibility`). The discipline of one enablement commit + one runner invocation + one inert-restore commit matches the prior `fe74255 → run → 9e329c2` pattern.

## 3. Execution summary

**Two shell invocations were issued; only the second loaded the runner.**

The first invocation used the literal command from the execution prompt (`python …`), but `python` is not present on PATH on this machine — only `python3` (Python 3.8.2 at `/usr/bin/python3`). The shell returned exit 127 (`command not found: python`) before any process was spawned. Consequences:

- No Python interpreter started.
- The runner script was never read, parsed, or imported.
- `fetch_archive_index` was not called.
- No network socket was opened; no GET was issued.
- The `LANE2_COUNT_FEASIBILITY_AUTHORIZED=1` environment variable was set inside the same Bash invocation and never persisted to a runner process.

The second invocation substituted the available interpreter (`python3`) and was the single execution of the runner under v0.2 authorization. Command actually invoked:

```
LANE2_COUNT_FEASIBILITY_AUTHORIZED=1
python3 scripts/run_lane2_gdelt1_count_feasibility.py \
  --authorize-count-feasibility-run \
  --repo-root /Users/jay/Documents/GitHub/coherent-numbers
```

The interpreter substitution is judged not to constitute a "retry" of the run, because the first invocation failed at the shell layer before any runner code, network code, or guard-checked code path was reached. This judgment is flagged explicitly so that a reviewer may adjudicate; it is not load-bearing for the verdict.

The runner loaded, passed the three-guard gate (`_guards_ok` returned True), called `_fresh_output_dir` to create `results/lane2_gdelt1_count_feasibility/20260522T133715Z/`, then called `m.fetch_archive_index(use_opener)`. **Exactly one** live HTTP GET was performed by `_real_opener` against the authorized endpoint:

- URL: `http://data.gdeltproject.org/events/index.html` (`DEFAULT_GDELT1_INDEX_URL`).
- Method: GET via `urllib.request.urlopen`.
- No event-file URL requested. No second GET. No `capture_recognized_list_once`, no `fetch_index_live_once`, no `fetch_archive_index_live_safe`. No host other than `data.gdeltproject.org`.

`extract_index_units` consumed the response body, identified 2023+ filenames, and raised `Protocol2023PlusBreach`. The runner's outer `try / finally` reset `m.REAL_RETRIEVAL_ENABLED` to its previous (False) value, and the exception propagated to `main()` and out to the shell as exit code 1. The `LANE2_COUNT_FEASIBILITY_AUTHORIZED` env var was `unset` immediately after.

## 4. Boundary halt

- **Verdict**: `RUN-HALTED-BOUNDARY` (mapping rule from the execution prompt §2.7: `Protocol2023PlusBreach` → `RUN-HALTED-BOUNDARY`).
- **Exception class**: `lane2_gdelt1_count_feasibility.Protocol2023PlusBreach`.
- **Diagnostic field**: `rejected_2023plus = 1219` (count of 2023+ filenames detected in the live index listing before the parser aborted).
- **Example flagged tokens** (from the runner's diagnostic string, surfaced verbatim — not retained on disk in this run): `20260521.export.CSV.zip`, `20260520.export.CSV.zip`, `20260519.export.CSV.zip`.
- **Call-site of the raise**: `extract_index_units` (`src/lane2_gdelt1_count_feasibility.py:1131`) → re-raised by `fetch_archive_index` (`src/lane2_gdelt1_count_feasibility.py:1666`) → propagated to `run_count_feasibility` (`scripts/run_lane2_gdelt1_count_feasibility.py:110`).
- **Branch never entered**: `m.run_count_only_feasibility(...)` was not called. Therefore:
  - no `feasibility_class` was assigned;
  - `verify_archive_layout` was not run, so no `files_missing` and no `files_in_archive_not_planned` were produced;
  - the F4 / F5 branches inside `run_count_only_feasibility` did not write metadata, so no `stopped_before_count_computation` flag exists for this run;
  - the per-file `download_one` loop was not reached, so no event-file network traffic occurred;
  - the freeze manifest, daily-count table, and feasibility summary were not produced.

The 2023+ guard in `extract_index_units` is by design a hard pre-filter on any token that parses as a date on or after `SEAL_START = 2023-01-01`. It fires unconditionally on the *listing*, before any in-window subset is extracted.

## 5. §6 caveat status

The §6 binding caveat from the v0.2 memo — *"`'2013'` yearly identifier is dropped at universe-construction time; the four 2014 dailies (`2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`) are recorded as known substrate gaps"* — was **not exercised** by this run.

The caveat is operationalized inside `verify_archive_layout`'s `files_missing` and `files_in_archive_not_planned` outputs, downstream of `extract_index_units`. Because the breach raised inside `extract_index_units` before any keys were returned, the planner-vs-recognized comparison never ran. The caveat is neither corroborated nor contradicted by this run.

Specifically:

- H2 (*"the upstream index advertises a `'2013'` yearly aggregate"*) — **not testable on this run**. `extract_index_units` does not return a keys list when it aborts; the recognized in-window subset is never computed. The boundary breach is independent of and prior to whatever H2's answer would have been.
- The four 2014 dailies as known substrate gaps — **not testable on this run** for the same reason.

The §10 recognized-list capture remains the only live, on-disk evidence on this question. Its artifact at `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json` (SHA-256 `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`, tracked at `4015b97`) attests `recognized_in_window_count=3647`, `extras=['2013']`, `missing=['2014-01-23','2014-01-24','2014-01-25','2014-03-19']`. The §6 caveat in the v0.2 memo derives from the Gate 4C re-review at `3176652` (`docs/lane2_gdelt1_gate4c_recognized_list_integrity_re_review_report_v0.1.md`, SHA-256 `992a395c4a23cbe6270e88b7352b1fe20b59e2eccc08d0864be59aad2d7a0de4`, verdict `RECOGNIZED-LIST-USABLE-WITH-CAVEAT`). The Gate 4C documentation remains the load-bearing on-disk record of the `'2013'` and four-2014-dailies issue; this v0.2 run halted strictly above that layer and therefore neither affirms nor unsettles it.

## 6. Fresh output directory

- Path: `results/lane2_gdelt1_count_feasibility/20260522T133715Z/`.
- Created by `_fresh_output_dir` (`scripts/run_lane2_gdelt1_count_feasibility.py:62`) immediately before the call to `fetch_archive_index`; `os.makedirs(..., exist_ok=False)` succeeded against the fresh timestamp.
- Current contents: **empty** (`ls -la` shows only `.` and `..`; zero files).
- No `count_feasibility_metadata.json`, no `feasibility_summary.md`, no allow-listed artifact was written, because the breach occurred inside `fetch_archive_index` — strictly before `run_count_only_feasibility` entered either its main F-class flow or its `Protocol2023PlusBreach` handler (the handler that *would* have written F5 metadata is local to `run_count_only_feasibility`, not the outer `run_count_feasibility`).
- The directory is untracked under `?? results/lane2_gdelt1_count_feasibility/`. It is intentionally **not** being staged in this turn or in any prior turn.

## 7. Guard discipline

- The enablement commit `89a5bcb` flipped `COUNT_FEASIBILITY_AUTHORIZED` from `False` to `True` in `scripts/run_lane2_gdelt1_count_feasibility.py`. Adjacent comment was expanded to cite the v0.2 authorization anchor `57f42cc` and mark inert-restore as mandatory.
- The inert-restore commit `a6e5ebb` flipped `COUNT_FEASIBILITY_AUTHORIZED` back to `False` in the same file and recorded the run outcome (`RUN-HALTED-BOUNDARY`, `89a5bcb`, `rejected_2023plus=1219`) in the surrounding comment.
- Final on-disk guard state:
  - `src/lane2_gdelt1_count_feasibility.py:647` — `REAL_RETRIEVAL_ENABLED = False`.
  - `scripts/run_lane2_gdelt1_count_feasibility.py:49` (the constant; line shifted by the expanded comment block) — `COUNT_FEASIBILITY_AUTHORIZED = False`.
  - Shell `LANE2_COUNT_FEASIBILITY_AUTHORIZED` — unset.
- `src/lane2_gdelt1_count_feasibility.py` was **not edited** at any point in the v0.2 workflow. The in-process transient flip of `REAL_RETRIEVAL_ENABLED` from `False` to `True` inside `run_count_feasibility`'s `try` block was correctly restored in the `finally` block; the source constant on disk was never modified.
- The two-commit pattern (`enablement → run → inert-restore`) mirrors the established prior discipline (`fe74255 → run → 9e329c2`). The structural shape is identical; only the underlying authorization anchor (`57f42cc` vs. the v0.1 `60ec152`) and the recorded outcome differ.

## 8. Protected baselines

| Baseline | Expected SHA-256 | Observed | Status |
|---|---|---|---|
| Historical F4 metadata: `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json` | `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d` | matches | ✅ untouched |
| Historical F4 summary: `…/20260518T163302Z/feasibility_summary.md` | `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c` | matches | ✅ untouched |
| v0.2 memo: `docs/lane2_gdelt1_gate5_run_enablement_memo_v0.2.md` | `d7e8bbf45940ca139f8b68e8302b214f8fad4ae2c35f76142be7b7fc23dcf276` | matches | ✅ untouched |
| Post-§10 diagnostic report: `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md` | untracked, commit-prohibited under §7.2 | still untracked, not edited | ✅ |
| §10 recognized-list capture: `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json` | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` (tracked at `4015b97`) | not read or modified in this run | ✅ untouched |

No event files were fetched. No market data was loaded. No Step 2 lock was drafted. No Gate 5 execution occurred. No second GET. No capture path was invoked. The full set of downstream-blocked artifacts named in the v0.2 memo's §10 remains undisturbed.

## 9. Interpretation

The structurally new finding from this run is that the live GDELT 1.0 index listing at `http://data.gdeltproject.org/events/index.html` now advertises 2023+ daily files. As of execution time (2026-05-22 13:37:15Z), at least 1,219 file tokens parsed as dates on or after `SEAL_START = 2023-01-01`. Concrete examples (current as of run time): `20260521.export.CSV.zip`, `20260520.export.CSV.zip`, `20260519.export.CSV.zip`.

Consequences for the count-feasibility pathway:

1. The 2023+ guard inside `extract_index_units` is now **load-bearing** for any future live count-feasibility run. It will fire on any GDELT 1.0 index listing that the upstream serves between today and any future cutoff, because the listing is cumulative and now includes the seal-breaching tokens by construction.
2. This finding is **structurally distinct** from the F4 / §6 caveat issue. F4 / §6 concerns *which planned in-window units the recognized listing advertises* and how to interpret the `'2013'` vs. four-2014-dailies discrepancies. The boundary halt is *upstream* of that question: the listing parser refuses the listing as a whole because it contains seal-breaching tokens that should never appear in a pre-2023 protocol.
3. The live-run path for count-feasibility is therefore **blocked** at this layer until one of the following is explicitly authorized:
   - A code-level pre-filter that strips 2023+ tokens from the listing string before `extract_index_units` parses it (would require a Gate 4-style review, an authorization memo, conformance tests, and an explicit guard discipline of its own — the pre-filter must be auditable, must preserve every in-window token byte-for-byte, and must not silently drop ambiguous tokens).
   - Use of a frozen historical listing snapshot (e.g., the byte-captured `recognized_list.json` from §10, or a deliberately frozen new snapshot taken under a separate authorization) in lieu of a live GET. This would replace the live-archive contract with a snapshot contract and would need its own pre-registration.
   - A different upstream data source whose listing semantics meet the protocol — out of scope for the existing v0.2 design.
4. No interpretation of the §6 caveat is updated by this run. The caveat continues to bind any future count-feasibility execution attempt under the v0.2 design; the new finding compounds (rather than supersedes) the v0.2 boundary conditions.
5. The fact that the breach raised *before* the §6 caveat could be tested means a future v0.3 (or successor) design must address the boundary layer first; testing the §6 caveat in live conditions is downstream of solving the 2023+ listing problem.

## 10. Candidate next workstreams

These are options for explicit user initiation; none is being selected here.

- Post-run report disk-write and commit (this draft → a tracked `.md` artifact under `docs/`, plus a single explicit commit; commit-prohibited until separately authorized, sibling to the post-§10 diagnostic report's status).
- Boundary-handling design decision / v0.3 memo: a Gate 5 v0.3 run-enablement memo that supersedes the v0.2 verdict with an explicit posture toward the 2023+ listing problem.
- 2023+ pre-filter transform design: a separate authorization for a code-level transform that filters seal-breaching tokens from the listing string upstream of `extract_index_units`, with conformance tests and Gate-4-style review.
- Frozen-snapshot / reuse-of-prior-capture consideration: an authorization to substitute a frozen listing (e.g., the §10 byte-captured `recognized_list.json`, or a fresh frozen snapshot) for the live GET, under a redefined snapshot contract.
- `python3` canonicalization hygiene: a small workflow hardening to either pin `python3` in the count-feasibility runner's shebang (`#!/usr/bin/env python3`) or normalize all execution prompts to specify `python3` explicitly — removes the recurring RUN-HALTED-PREFLIGHT-by-typo risk surfaced by Attempt 1 in this run.

## 11. Still blocked

The following remain blocked and require explicit user initiation before any further action:

- Gate 5 execution.
- Count-feasibility re-run (under any guard configuration).
- Market data ingest or read.
- Step 2 (lock or any precursor drafting).
- Second live GET to the GDELT archive or index.
- Capture wrapper invocation (`capture_recognized_list_once`, `fetch_index_live_once`, `fetch_archive_index_live_safe`).
- F4 modification or any touch of `results/lane2_gdelt1_count_feasibility/20260518T163302Z/`.
- Guard flips of `REAL_RETRIEVAL_ENABLED` or `COUNT_FEASIBILITY_AUTHORIZED` in any file.
- Post-§10 diagnostic report staging, committing, editing, deleting, renaming, or moving.

## 12. Boundary confirmation

In this disk-write turn:

- Exactly one new file was written: `docs/lane2_gdelt1_gate5_post_run_report_v0.2.md` (this report). No other file was written.
- No tracked repository file was modified (no Edit on any tracked path, no Write on any tracked path, no shell redirection to a tracked path).
- No staging, committing, pushing, tagging, branching, pulling, or merging occurred. Commit of this report requires a separate explicit prompt.
- No network call was issued; no live GET; no capture; no contact with GDELT or any other host.
- No guard flip; both `REAL_RETRIEVAL_ENABLED` and `COUNT_FEASIBILITY_AUTHORIZED` remain `False` on disk; `LANE2_COUNT_FEASIBILITY_AUTHORIZED` remains unset in the shell.
- No memory edits; MEMORY.md and per-topic memory files are unchanged.
- No run executed; the count-feasibility runner was not invoked again, and no Python process was spawned for it.
- The fresh-run output dir `results/lane2_gdelt1_count_feasibility/20260522T133715Z/` is unchanged (still empty, still untracked).
- The post-§10 diagnostic report remains untracked and unmodified.
