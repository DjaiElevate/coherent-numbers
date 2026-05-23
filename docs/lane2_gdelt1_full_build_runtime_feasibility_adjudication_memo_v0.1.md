# Lane 2 GDELT1 full-build runtime-feasibility adjudication memo v0.1

## 1. Title and status

This memo is **memo-only**. It authorizes no live full-build run, no GDELT contact, no guard flip, no runner code change, no test change, no production output-directory creation, no market data, no Step 2, no spike/burst threshold tuning, no return-window logic, no asset selection, no F4 modification, no recognized-list capture modification, no locked-memo edit, no event-file probe re-run, no row-date characterization re-run, no count-feasibility run, and no staging / commit / push of any artifact other than this memo file.

The memo's authorization scope is the persistence of one tracked file at `docs/lane2_gdelt1_full_build_runtime_feasibility_adjudication_memo_v0.1.md`. Its purpose is to **adjudicate the `RUNTIME-FEASIBILITY-BLOCK — AWAIT ADJUDICATION` outcome** from the attempted full-build execution-authorization turn against the implementation at `bc7b66b` (as amended by the adjudication memo at `c10ae74`), and to **decide the next execution strategy** before any runner patch, guard flip, GDELT contact, or build execution.

| Anchor | Value |
|---|---|
| Current `HEAD = origin/main` | `c10ae7498d03d66c0b2a7b60e44d0926be1503a5` |
| Short SHA | `c10ae74` |
| Ahead count | `0` |
| Tracked tree | clean |
| Full-build design memo | `7780a97` |
| Full-build runner implementation | `bc7b66b` |
| Implementation adjudication memo | `c10ae74` |
| Latest runtime-feasibility block report | the immediately-prior execution-authorization turn's halt response (chat-only; no tracked artifact written under the `RUNTIME-FEASIBILITY-BLOCK` branch of that prompt) |
| §10 recognized-list capture SHA-256 | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` |
| `FULL_BUILD_AUTHORIZED` location | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95` (value: `False`) |

## 2. Scope and non-scope

**In scope:**

- Recording the runtime-feasibility facts that produced the block.
- Calibrating the prompt-scope authority of the block (was the pre-enable halt authorized by the execution prompt, or a defensive scope extension?).
- Decision 1: whether single-session sequential Claude Code execution remains authorized for this runner.
- Decision 2: choosing the next execution strategy.
- Stating the consequences for runner design.
- Boundary-constraint statement for the next workstream.

**Out of scope (explicit, binding):**

- No runner code edit (no change to `scripts/run_lane2_gdelt1_full_daily_count_build.py`).
- No test edit (no change to `tests/test_lane2_gdelt1_full_daily_count_build.py`).
- No live full-build execution.
- No GDELT contact.
- No guard flip on any runner.
- No production output-directory creation under `results/lane2_gdelt1_full_daily_count_build/`.
- No market data, Step 2, spike/burst threshold tuning, return-window logic, asset selection, signal extraction, category/theme/actor/geography/tone filtering, or any market-predictiveness claim.
- No retirement of the no-market-data firewall.
- No retirement of the no-2023+ posture.
- No locked-memo edit to `9319d30` / `a8a9dd2` / `a2a8fd5` / `e9f8781` / `487dadb` / `3537a62` / `73a7911` / `858b501` / `0065d10` / `7780a97` / `bc7b66b` / `c10ae74` / `e55e09a` / `0b341b4` / `845c51c`.
- No F4 modification (baselines `41c80c0…624c39d` / `00ce9b2…f5e37552c` preserved).
- No recognized-list capture modification (SHA `84ea721e…fff835fc` preserved).
- No event-file probe re-run, no row-date characterization re-run, no count-feasibility run, no Gate 5 run.
- No payload-preserving runner variant authorization.
- No staging / commit / push of unrelated untracked files.

## 3. Source anchors

In commit-chain order:

| # | Anchor | Description |
|---|---|---|
| 1 | `9319d30` | First event-file probe execution report |
| 2 | `a8a9dd2` | Substrate-validation memo |
| 3 | `a2a8fd5` | Row-date characterization plan lock |
| 4 | `e9f8781` | Row-date characterization runner implementation |
| 5 | `487dadb` | Exact-integer offset taxonomy corrective patch |
| 6 | `3537a62 → 73a7911 → 858b501` | Row-date characterization enable / restore / report |
| 7 | `0065d10` | Post-characterization decision memo |
| 8 | `7780a97` | Full-build design memo (eleven locked design decisions A–K) |
| 9 | `bc7b66b` | Full-build runner implementation + paired tests |
| 10 | `c10ae74` | Implementation adjudication memo (Decision 1A: 7-entry `coverage_quality_flag` closed domain; Decision 2A: `halt_diagnostic.json` allow-listed) |
| 11 | (chat-only) | Runtime-feasibility block report from the attempted execution-authorization turn |

Supporting: §10 recognized-list capture (SHA `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`); no-2023+ posture (`0ddbd51`); F4 baselines (`41c80c0…624c39d` / `00ce9b2…f5e37552c`); event-file probe execution chain `e81208d → 7c85e3f → 9319d30`; count-feasibility execution chain `60ec1521 → fe74255 → 9e329c2`; row-date characterization execution chain `3537a62 → 73a7911 → 858b501`.

## 4. Runtime-feasibility finding

The following facts are recorded from the immediately-prior execution-authorization turn's read-only source inspection and chat-only `RUNTIME-FEASIBILITY-BLOCK` report. No additional GDELT contact, code execution, or test run was performed to produce these facts.

### 4.1 Concurrency model — fully sequential

The full-build runner at `scripts/run_lane2_gdelt1_full_daily_count_build.py` (committed at `bc7b66b`) is **fully sequential**.

- Source inspection (`grep -nE "concurrent\.futures|ThreadPool|ProcessPool|asyncio|aiohttp|multiprocessing|threading|gevent|Pool\("`) returned **zero matches**.
- The main fetch loop at line 1254 is a single-threaded `for iso, url in zip(fetch_set, urls):` with one `_fetch_one_payload(...)` call per iteration and `del payload` between iterations.
- Line 287 source comment: *"Exactly-once fetch per URL per run. No retry, no second GET, no fallback."*
- The exactly-once + no-retry contract is a binding part of `7780a97` Decision H (retrieval policy) and `7780a97` Decision I (parser validation / no silent repair).

### 4.2 Fetch-count expectation

- Recognized-list capture units: **`3,647`** (per the SHA-verified capture at `84ea721e…fff835fc`).
- Civil output domain days: **`3,562`** (full civil calendar from `2013-04-01` through `2022-12-31` inclusive).
- Known publishing-file substrate gaps: **`4`** (`2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19` per `a8a9dd2` §2 / §10).
- Expected daily fetch set: **`3,558`** (= `3,562 − 4`).
- Recognized-list classification residual: **`89`** units, deterministically classified by `classify_recognized_units` as **2 yearly + 87 monthly** (no out-of-window dailies, no unknowns, no duplicates per the real capture's static structure).
- The runner's preflight (`build_reconciliation_report` + `assert_reconciliation_consistent`) would hard-fail with `ReconciliationContradiction` if the fetch_set count differs from `3,558` or if any of the residual sub-counts diverge from expectation.

### 4.3 Conservative wall-clock estimate

Per-URL operations (sequential, no retries): HTTP GET to `data.gdeltproject.org` CDN + SHA-256 hash + in-memory ZIP decompression + headerless CSV parse with offset-taxonomy check + payload discard.

Per-URL assumptions:

- Mean file size: ~7.5 MiB (extrapolated from the characterization sample at `858b501` §8: 119.4 MiB / 16 files).
- Connection setup: ~100–300 ms per request (no HTTP keep-alive across requests; each URL gets a fresh opener.open call).
- Download bandwidth: 1–10 MiB/s sustained to GDELT's CDN (typical residential / cloud network).
- Parse + hash: ~0.3–1.0 s per file (~100k rows × O(1) per row).
- Per-URL total: **~2–5 s optimistic; ~5–15 s pessimistic**.

Total wall-clock for 3,558 sequential URLs:

| Scenario | Per-URL avg | Total seconds | Total hours |
|---|---:|---:|---:|
| Optimistic | 3 s | 10,674 | **3.0** |
| Realistic | 5 s | 17,790 | **4.9** |
| Conservative | 8 s | 28,464 | **7.9** |
| Pessimistic | 15 s | 53,370 | **14.8** |

### 4.4 No-retry reliability multiplier

Decision I's no-retry rule means a single transient HTTP failure (non-200, redirect, connection error, timeout) over the entire 3,558-URL sequential run causes hard-fail. Under realistic GDELT-CDN per-URL success rates:

- At `p = 0.9995` per-URL success: probability of zero failures across 3,558 = `0.9995^3558 ≈ 0.17` → ~17% expected first-pass success.
- At `p = 0.999` per-URL success: `0.999^3558 ≈ 0.028` → ~3% expected first-pass success.
- At `p = 0.998` per-URL success: `0.998^3558 ≈ 0.0008` → <0.1% expected first-pass success.

A multi-hour run with no retries is **very likely to halt** before successful completion. This is an expected Decision I outcome, not a runner defect — but it materially affects strategy selection.

### 4.5 Final state from the runtime-feasibility block turn

The attempted execution-authorization turn halted **before any side effect**, per its step-6 instruction. Specifically:

- No enable commit occurred (line 95 of the runner remains `FULL_BUILD_AUTHORIZED = False`).
- No guard flip occurred (all five runner guards remain `False` on disk; all four `LANE2_*_AUTHORIZED` env vars `UNSET`).
- No GDELT contact occurred (no URL constructed, no fetch issued, no `curl`/`wget`/browser/manual fetch).
- No output directory was created (`results/lane2_gdelt1_full_daily_count_build/` does not exist).
- Final repo state remained `HEAD = origin/main = c10ae74`, ahead = `0`, tracked tree clean.

Preflight re-verification by this memo (re-run read-only): all five facts above hold.

## 5. Prompt-scope calibration

The execution-authorization prompt explicitly included a section titled *"Runtime/session-feasibility gate before guard flip"* with eight numbered sub-steps, of which step 6 reads:

> *6. If the run appears unsuitable for one uninterrupted session, halt before the enable commit and report:*
> *`RUNTIME-FEASIBILITY-BLOCK — AWAIT ADJUDICATION`*

The pre-enable halt was therefore **explicitly authorized by the execution prompt**. It was not a defensive scope extension by Claude Code: the prompt-author specified the gate, defined the conditions under which to halt, defined the verdict string, and defined the post-halt next frontier (adjudication).

**Prompt-scope calibration verdict**: the runtime-feasibility halt was **explicitly authorized**. No calibration issue arises from this specific turn.

**Forward-looking calibration note (advisory, not corrective)**: future execution prompts should continue to **explicitly state whether Claude Code may halt pre-enable on runtime/session infeasibility, or whether runtime risk is accepted and execution must be attempted**. Without such explicit framing, a Claude Code session would either (a) default to attempting execution and risk session-interruption recovery (per the session-interruption rule), or (b) extend scope defensively to halt. Future prompts that omit the gate language should declare the intent explicitly to avoid ambiguity.

## 6. Decision 1 — single-session Claude Code execution

**Decision: Option B — reject single-session sequential Claude Code execution as operationally unsuitable for this runner in its current form.**

### 6.1 Options evaluated

| Option | Verdict | Rationale |
|---|---|---|
| **A. Proceed with the original single-session sequential execution despite runtime/session risk** | Rejected | A 3.0–14.8-hour wall-clock with no retries is incompatible with typical Claude Code session dynamics. The single-Bash-command 10-minute timeout makes synchronous orchestration impossible; `run_in_background` defers but does not eliminate session-lifetime risk. The probability of session interruption (forced restore + `SESSION-INTERRUPTED-MID-CYCLE — AWAIT ADJUDICATION`) is high enough that the cycle would, in expectation, terminate via the session-interruption recovery rule rather than via normal restore. |
| **B. Reject single-session sequential Claude Code execution as operationally unsuitable** | **SELECTED** | The runner is sound but the execution context is wrong. Halting before guard flip preserved repo safety (no enable commit; no guard flip; no GDELT contact; no output dir; HEAD unchanged). This is **not** a scientific failure of the substrate, the design memo, the adjudication memo, or the runner — it is a session-suitability finding for the chosen execution context. |
| C. Defer the decision | Rejected | Deferring leaves the implementation accepted-but-unexecuted indefinitely, which would silently weaken the "no execution until separately initiated" framing by accumulating an ambiguous state. Decision 2 below addresses the strategy choice explicitly. |

### 6.2 Why a multi-hour sequential run is unsuitable for a normal Claude Code session

- Estimated realistic wall-clock (4.9 hours) exceeds typical Claude Code session lifetimes by a factor of several.
- The single-Bash-command timeout in this environment is 10 minutes (600,000 ms); even `run_in_background=true` only defers orchestration, not the underlying process lifetime constraint.
- Network reliability: at realistic GDELT-CDN per-URL success rates (`p ≈ 0.999`), the probability of completing all 3,558 sequential requests without ANY transient failure is < 3%. The no-retry rule (Decision I) means any single failure aborts the run. The cycle is therefore very likely to halt rather than complete on a first attempt.
- The session-interruption recovery rule (the prior execution prompt's steps 1–13 of "Session-interruption recovery rule") is a graceful-degradation path, not a primary execution mode. Designing for it as the expected outcome would conflate "primary execution" with "interruption recovery".

### 6.3 Why halting before guard flip preserved repo safety

- `HEAD` remained at `c10ae74`; no commit was added to the chain.
- `FULL_BUILD_AUTHORIZED` remained `False` on disk at line 95; no enable diff was produced.
- All five runner guards remained `False`; all four LANE2_*_AUTHORIZED env vars remained `UNSET`.
- No production output directory exists; no payload bytes were fetched or persisted.
- No locked-memo edit, no recognized-list capture modification, no F4 modification.

The halt produced a clean, restartable state. No corrective action is required to "back out" of the halt — the system is exactly where it was before the execution-authorization turn began.

### 6.4 Why this is not a scientific failure

- **Substrate**: the substrate (GDELT 1.0 daily event files indexed by SQLDATE) is unchanged. The substrate-validation memo `a8a9dd2`, the row-date characterization at `858b501`, the post-characterization decision memo `0065d10`, and the full-build design memo `7780a97` all remain valid.
- **Runner**: the runner at `bc7b66b` is implementation-conformant under the amended design contract (Decision 1A + Decision 2A from `c10ae74`). No corrective patch is required for substrate or design conformance.
- **Tests**: the test baselines from `bc7b66b` (119 full-build / 236 paired / 957 + 2 skipped repo-wide) are unaffected.
- **Design contract**: the locked design decisions in `7780a97`, as amended by `c10ae74`, are not modified by this memo.

The finding is purely **operational**: the chosen execution context (a single uninterrupted Claude Code session running the existing fully-sequential runner) is unsuitable for a 3,558-URL no-retry sweep. The runner is sound; the execution context choice was wrong.

### 6.5 Why this does not weaken locked posture

- **No-retry rule**: this memo **preserves** the no-retry rule. Decision 2 below does not introduce retries.
- **No-market-data firewall**: this memo does not approach, weaken, or relax the firewall. None of the Decision 2 options requires market data.
- **No-2023+ posture (`0ddbd51`)**: this memo does not lift the seal. None of the Decision 2 options requires fetching 2023+ URLs.
- **Exact-once design**: this memo preserves exactly-once fetch semantics. Decision 2 below (whichever option is chosen) must guarantee that no URL is fetched more than once across a complete logical execution.

## 7. Decision 2 — next execution strategy

**Decision: Option C — chunked execution plan (yearly chunks with deterministic merge), conditional on a future chunk-design memo formalizing the chunk boundaries, per-chunk artifact schema, deterministic merge rule, and across-chunk coverage diagnostics. Plan-B-reserve: Option A (checkpoint/resume) remains available if the chunked path encounters a downstream issue, but is not selected here.**

### 7.1 Options evaluated

| Option | Verdict | Requirements (design / code / test / new-prompt / chain-of-custody) |
|---|---|---|
| **A. Runner patch for checkpoint/resume** | **Plan-B reserve (available only if chunked execution encounters a downstream issue; not selected as primary)** | Requires: a separately authorized **runner-patch design memo** defining checkpoint format + resume semantics + exactness-of-fetch invariant; a **runner code patch** committing checkpoint writes after each successful URL and a resume-from-checkpoint code path; **paired tests** covering checkpoint deterministic invariants, mid-run resume, and resume-against-modified-fetch-set hard-fail; a **new execution-authorization prompt** specifying enable/run/restore semantics under resume; **no chain-of-custody memo required** (single session per resume attempt). Risk: checkpoint format is a new design surface; resume semantics need careful "continuation vs new execution" framing. |
| **B. Runner patch for bounded parallelism and/or HTTP keep-alive** | Rejected (not for this design) | Requires: a separately authorized **design memo revision** to `7780a97` Decision H (retrieval policy) defining concurrency bound, in-flight failure handling, fair-queueing if any, and how exactness-of-fetch is preserved under parallelism; a **runner code patch** introducing a thread or async pool with worker-coordinated halt semantics; **substantial test updates** covering race conditions, partial-completion halts, and deterministic-manifest invariants under parallel ordering; a **new execution-authorization prompt** specifying enable/run/restore under parallelism; **chain-of-custody memo** for parallel-fetch attribution. Concurrency changes the exactness-of-fetch failure semantics: a single in-flight URL failure under parallelism affects multiple sibling URLs (which may complete or be canceled), and exactness-of-fetch becomes "at most once per worker per URL" rather than "exactly once globally". Not selected on the grounds of complexity, design-surface expansion, and risk to the locked Decision H. |
| **C. Chunked execution plan, e.g., yearly chunks with deterministic merge** | **SELECTED** | Requires: a separately authorized **chunk-design memo** (`docs/lane2_gdelt1_full_build_chunk_design_memo_v0.1.md`) defining chunk boundaries (yearly by publishing-file nominal date is the recommended starting point: 2013 / 2014 / 2015 / … / 2022 = ~10 chunks), per-chunk output schema, deterministic merge rule across chunks, coverage diagnostic recomputation at merge time, halt semantics (chunk-level halt does not invalidate other chunks), and duplicate-counting prevention; **runner code patch** introducing a `--year YYYY` (or equivalent date-range) CLI flag that subsets `fetch_set` to chunk membership; **paired tests** covering chunk-membership classification, per-chunk artifact schema, merge determinism, and across-chunk coverage flag computation; a **new execution-authorization prompt template** specifying enable/run/restore per chunk; a **merge-step authorization prompt** for the final daily_count.csv assembly. **No chain-of-custody memo required** beyond the per-chunk SHA manifests (which mirror the existing audit pattern). Risk: 10 chunks × 3-step cycle = ~30 authorization sub-prompts, plus a merge prompt. High prompt-overhead, but each sub-prompt is small, well-bounded, and research-safe. Each chunk fits well within a typical Claude Code session (per-chunk ≈ 356 URLs × 5 s ≈ 30 min). Per-chunk failure isolation: a single chunk's halt does not invalidate other chunks. |
| D. Off-session long-running execution with chain-of-custody controls | Rejected (not for this design; available only through a separately authorized off-session execution prompt) | Requires: a separately authorized **chain-of-custody memo** specifying exact command capture, environment capture, runner SHA pinning, stdout/stderr capture, SHA manifests for all artifacts before transit back into the repo, guard enable/restore discipline executed *outside* Claude Code, no-manual-URL-fetch confirmation, and a `bc7b66b`-equivalent runner-image fingerprint. Higher complexity than chunked execution; introduces an external execution surface that requires its own audit. Plan-B-reserve if both chunked and checkpoint/resume prove unworkable. |
| E. Override runtime block and proceed with single-session execution anyway | Rejected (permanently forbidden by Decision 1B) | Decision 1 above rejects single-session sequential execution as unsuitable. Overriding would re-open Decision 1, defeating its purpose. |
| F. Defer full-build execution | Rejected (Decision 2 must make a selection) | Per Decision 1, deferring would leave the implementation in an accepted-but-unexecuted-indefinitely state. Decision 2 must choose a forward path. Chunked execution is the chosen path. |

### 7.2 Required follow-up for the selected Option C (chunked execution)

The selected option requires a **future chunk-design memo** at the proposed path `docs/lane2_gdelt1_full_build_chunk_design_memo_v0.1.md`. The chunk-design memo must specify, at minimum:

1. **Chunk boundaries**: recommended starting point is by publishing-file nominal calendar year (`2013` = chunk for `[2013-04-01, 2013-12-31]`; `2014` = `[2014-01-01, 2014-12-31]`; …; `2022` = `[2022-01-01, 2022-12-31]`). This yields 10 chunks (one for each of 2013–2022). The chunk-design memo may revise the boundaries if substrate-side or audit-side reasons emerge.

2. **Per-chunk output artifacts**: each chunk produces its own `results/lane2_gdelt1_full_daily_count_build/<chunk_id>_<UTC_TIMESTAMP>/` directory containing per-chunk derivatives (`daily_count_chunk_<chunk_id>.csv`, `build_metadata_chunk_<chunk_id>.json`, `build_summary_chunk_<chunk_id>.md`, embedded per-file manifest and SHA manifest). The existing allow-list (`daily_count.csv`, `build_metadata.json`, `build_summary.md`, `halt_diagnostic.json`) is amended to allow chunk-named variants OR is reused verbatim and the directory name encodes the chunk id.

3. **Deterministic merge rule**:
   - Per civil date `d`, `total_row_count[d]` = sum of `total_row_count[d]` across all chunks whose contributing files cover `d`'s era-conditioned cone.
   - Per-offset diagnostic columns sum across chunks.
   - `coverage_quality_flag` and `coverage_completeness` are **recomputed at merge time** using the union of all chunks' fetch sets as `daily_set` (NOT computed per chunk; per-chunk computation would produce incorrect coverage flags because each chunk's daily_set covers only that chunk's URLs, missing contributing files from neighboring chunks).
   - `out_of_window_sqldate_diagnostic` and `per_offset_total` sum across chunks.

4. **Coverage diagnostics across chunk boundaries**: civil dates near year boundaries (e.g., `d = 2013-12-31`'s T+1 source = `2013-12-30`, T-1 source = `2014-01-01`) draw contributions from multiple chunks. The merge step must:
   - Aggregate per-SQLDATE-per-offset counts from all chunks.
   - Reconstruct `daily_set = ⋃ chunks.fetch_set` (= the full recognized-list daily-in-window minus gaps).
   - Compute `coverage_for_date(d, daily_set, gaps_set)` per `7780a97` §11.3 (as amended by `c10ae74` Decision 1A) at merge time, using the **combined** daily_set.
   - Result: coverage flags are identical to what a single non-chunked run would produce. This is the deterministic-equivalence invariant.

5. **Halt semantics**:
   - A chunk-level hard-fail (any Decision I condition: HTTP non-200, redirect, connection error, timeout, unexpected offset, 2023+ SQLDATE, etc.) halts ONLY that chunk's run.
   - Other chunks' runs (already completed) remain valid.
   - The failed chunk's enable/run/restore cycle still completes its restore phase (per `7780a97` §13's enable-then-inert-restore discipline).
   - The merge step requires all chunks' outputs to be present and SHA-verified; if any chunk is missing or hard-failed, the merge step halts with `MERGE-HALT — AWAIT ADJUDICATION` and the user can either re-run the failed chunk (a separately authorized retry-after-halt prompt) or proceed to per-chunk-only outputs.

6. **Duplicate-counting prevention**:
   - Each chunk's fetch_set is **disjoint** from every other chunk's fetch_set (chunks partition the year-by-year recognized publishing-file dates).
   - The runner's chunk-membership filter (the `--year YYYY` flag or equivalent) must hard-fail if it would emit a URL from outside the chunk's year boundary.
   - The merge step must hard-fail with `DUPLICATE-FETCH-DETECTED` if any URL appears in more than one chunk's per-file manifest.

7. **SQLDATE aggregation across chunks**:
   - Per the locked SQLDATE re-key premise from `0065d10` §5, each row's count flows to its `SQLDATE`, not the publishing-file's nominal date. A row in chunk-2014's `f_(2014-01-01)` with `SQLDATE = 2013-12-25` (a T-7 contribution) is routed to civil-date `2013-12-25` (which is in chunk 2013's output domain).
   - The merge step assembles per-civil-date totals from all chunks' per-SQLDATE-per-offset cells. The era-conditioned cone (cutoff `2015-01-01` / `2015-01-02`) is applied at merge time using the canonical era logic, not chunk-by-chunk.

8. **No-2023+ posture preservation**:
   - No chunk is permitted to fetch 2023+ URLs (the post-2022 dates are excluded by the existing `date_to_daily_url`'s `SEAL_START` check).
   - The 2022 chunk's late-year dates inherit the right-truncation coverage flag at merge time, per `c10ae74` Decision 1A.

9. **No-market-data preservation**:
   - No chunk introduces market data. No chunk-design CLI option introduces a market-data input path. Chunked execution is purely a substrate-side runtime-feasibility solution.

10. **Per-chunk authorization-prompt template**: the chunk-design memo must provide a template for the per-chunk execution-authorization prompt, mirroring the structure of the prior execution-authorization prompt but scoped to one chunk's URLs. The template must include enable / single live run (one chunk only) / restore / post-chunk report.

11. **Merge-step authorization prompt**: a separate merge-step authorization prompt must take all 10 (or N) per-chunk output directories + their committed reports as input and produce the final `daily_count.csv` + `build_metadata.json` + `build_summary.md` + `docs/lane2_gdelt1_full_daily_count_build_execution_report_v0.1.md`. The merge step is **derived-only** — it reads per-chunk artifacts, recomputes coverage flags, writes the final aggregate artifacts, and writes the final execution report.

### 7.3 What Decision 2C does NOT do

- Does not implement the chunk-design memo, the runner patch, the per-chunk authorization prompts, or the merge-step prompt — each is a **separately authorized future workstream**.
- Does not flip any guard.
- Does not contact GDELT.
- Does not create any production output directory.
- Does not authorize parallelism (Option B was explicitly rejected).
- Does not authorize off-session execution (Option D remains plan-B-reserve).
- Does not authorize override of the runtime block (Option E is rejected; single-session execution remains unsuitable).
- Does not modify the runner at `bc7b66b` or its tests.
- Does not modify any locked memo.

## 8. Consequences for runner design

### 8.1 Runner patch required

A separately authorized **future runner patch** is required to implement the `--year YYYY` (or equivalent date-range) CLI flag introduced by Decision 2C. The patch must:

- Add a new CLI argument to `_make_argparser` that accepts a year (or other chunk identifier per the chunk-design memo).
- Filter the `fetch_set` computed by `build_reconciliation_report` to chunk membership.
- Add hard-fail on any chunk-filter contradiction (e.g., a passed-in year outside `[2013, 2022]`, or a chunk producing zero URLs).
- Preserve all existing locked behavior: SHA-verified recognized-list capture, exact-integer offset taxonomy, no 2023+ URL construction, no payload preservation, three-guard discipline, no retries, exactly-once fetch within the chunk.
- Add chunk identification to the output dir path: `results/lane2_gdelt1_full_daily_count_build/<chunk_id>_<UTC_TIMESTAMP>/`.
- Add chunk identification to the metadata's `run_anchors` section.
- Optionally rename per-chunk output basenames (e.g., `daily_count_chunk_2014.csv`) to make multi-chunk inspection unambiguous; the chunk-design memo will choose between in-name encoding vs in-directory encoding.

### 8.2 Test updates required

Paired test updates to `tests/test_lane2_gdelt1_full_daily_count_build.py`:

- Tests for chunk-membership filtering correctness.
- Tests for per-chunk output schema.
- Tests for merge determinism (two chunked runs over the same input produce the same merged output).
- Tests for across-chunk coverage flag computation (e.g., `d = 2013-12-31`'s T-1 source from `f_(2014-01-01)` in a different chunk is correctly accounted for in the merge step).
- Tests for hard-fail on cross-chunk URL duplication.
- Tests for hard-fail on year-out-of-range.

### 8.3 New execution-authorization prompt template

The chunk-design memo must produce a per-chunk execution-authorization prompt template that:

- Replicates the structure of the prior execution-authorization prompt (preflight + enable + single run + restore + post-chunk report).
- Scopes the runtime/session-feasibility gate to per-chunk fetch counts (~356 URLs × ~5 s ≈ 30 minutes per chunk — well within a normal Claude Code session).
- Specifies the per-chunk halt diagnostic format.
- Specifies the merge-step prompt that follows the last chunk's restore.

### 8.4 No design memo revision required for `7780a97`

Decision 2C is implemented **outside** the existing design memo `7780a97`'s scope: the chunk-design memo is a *supplementary* memo that introduces the chunked execution surface without modifying the locked design decisions A–K. `7780a97`'s eleven design decisions, including the no-2023+ posture (§11.1), the structural T-3650 zero acceptance (§10.2), the SQLDATE re-key premise (§5), the locked output domain (§7), and the exact-integer offset taxonomy (§9), all remain unchanged and binding on each chunk's per-URL behavior.

The `c10ae74` adjudication memo (Decision 1A: 7-entry `coverage_quality_flag` closed domain; Decision 2A: `halt_diagnostic.json` allow-listed) also remains unchanged and binding on each chunk's per-URL behavior.

## 9. Boundaries that remain in force

Until the chunk-design memo, the runner patch + paired tests, the per-chunk execution-authorization prompts (one per chunk × 10 chunks), the per-chunk post-run reports, the merge-step authorization prompt, and the final consolidated memory update have all closed cleanly, the following remain **blocked**:

- **Full daily-count build execution** (single-session sequential).
- **Market data of any kind.**
- **Step 2 of any kind.**
- **Spike / burst threshold tuning.**
- **Return-window logic.**
- **Asset selection.**
- **Signal-design choices.**
- **Category / theme / actor / geography / tone filtering** (Step 2 / instrument-construction territory per `c10ae74`).
- **Additional GDELT contact** beyond what a future explicitly-authorized per-chunk execution-authorization prompt may approve.
- **Event-file probe re-run** under the existing implementation.
- **Row-date characterization re-run** under the existing implementation.
- **Count-feasibility run**, **Gate 5 run**.
- **Output-artifact disposition change** for `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` or `results/lane2_gdelt1_row_date_characterization/20260523T033234Z/` beyond `0065d10` Decision 3A.
- **F4 modification** (baselines `41c80c0…624c39d` / `00ce9b2…f5e37552c` preserved).
- **Recognized-list capture modification** (SHA `84ea721e…fff835fc` preserved).
- **Guard flips on any runner** (`REAL_RETRIEVAL_ENABLED`, `COUNT_FEASIBILITY_AUTHORIZED`, `EVENT_FILE_PROBE_AUTHORIZED`, `ROW_DATE_CHARACTERIZATION_AUTHORIZED`, `FULL_BUILD_AUTHORIZED` — all remain `False` on disk; shell envs `UNSET`).
- **Source / test / config edits** beyond this memo file.
- **Locked-memo edits** to any of `9319d30` / `a8a9dd2` / `a2a8fd5` / `e9f8781` / `487dadb` / `3537a62` / `73a7911` / `858b501` / `0065d10` / `7780a97` / `bc7b66b` / `c10ae74` / `e55e09a` / `0b341b4` / `845c51c`.
- **Design-note edits** to the existing probe design note (`e55e09a`).
- **Post-§10 diagnostic report staging / commit / edit / delete.**
- **2023+ pre-filter authorization** (no-2023+ posture at `0ddbd51` remains in force; `7780a97` §11.1 explicit keep/lock decision is unaffected by this memo).
- **Frozen-snapshot execution.**
- **`python3` canonicalization changes.**
- **Negative-control payload allow-list change.**
- **Payload-preserving runner variant** (default per `7780a97` §15.11 remains "not preserve").
- **Filtered / weighted / deduplicated variant runners.**
- **Concurrent / parallel runner variant** (Decision 2B explicitly rejected by this memo).
- **Off-session long-running execution** (Decision 2D explicitly rejected as primary; available only as plan-B reserve via a separately authorized chain-of-custody memo).
- **Override of the runtime block** (Decision 2E explicitly rejected).
- **Staging / commit / push of this memo or any other artifact** unless separately authorized after review.

**Market data and Step 2 remain blocked unconditionally until the no-market-data firewall is explicitly retired by a future, separately authorized memo.** This memo does not authorize any such retirement.

## 10. Final verdict / next frontier

**Final verdict**: 

- **Decision 1B**: single-session sequential Claude Code execution of the full-build runner at `bc7b66b` is **REJECTED as operationally unsuitable**. The runner is sound; the execution context choice was wrong.
- **Decision 2C**: the **chunked execution plan** is **SELECTED** as the next execution strategy. Implementation requires a separately authorized future chunk-design memo at `docs/lane2_gdelt1_full_build_chunk_design_memo_v0.1.md`, a separately authorized runner patch + paired tests, ~10 separately authorized per-chunk execution-authorization prompts, ~10 corresponding per-chunk post-run reports, a separately authorized merge-step authorization prompt, and a final consolidated memory update.
- **Option A (checkpoint/resume)** is reserved as plan-B if Decision 2C encounters a downstream issue.
- **Option D (off-session execution)** is reserved as plan-C if both Decision 2C and Option A prove unworkable.
- **Options B (parallelism), E (override), and F (defer)** are rejected.

**Next frontier (NOT next; awaits explicit user initiation)**: **chunk-design memo** at `docs/lane2_gdelt1_full_build_chunk_design_memo_v0.1.md`. The chunk-design memo is **memo-only** and must not flip guards, execute the build, contact GDELT, or modify the runner or its tests. After the chunk-design memo closes cleanly, the next-eligible workstreams (each separately authorized) are:

1. **Chunk-runner patch + paired tests** — implementing the `--year YYYY` (or equivalent) CLI flag and chunk-membership filtering; runner ships inert; tests offline-only with mocked HTTP; no guard flip; mirror of `bc7b66b` discipline.
2. **Per-chunk execution-authorization prompts** (one per chunk × ~10 chunks) — each prompts an enable / single live run / restore / post-chunk report cycle mirroring `3537a62 → 73a7911 → 858b501` discipline. Each chunk's per-URL count is ~356 (chunk_2013 = 275; 2014 = 365 minus 4 gaps = 361; …; 2022 = 365; total ≈ 3,558). Each chunk's wall-clock estimate at 5 s/URL is well within a normal Claude Code session.
3. **Per-chunk post-run reports** at `docs/lane2_gdelt1_full_daily_count_build_chunk_<chunk_id>_execution_report_v0.1.md`.
4. **Merge-step authorization prompt** — reads all chunk outputs, recomputes coverage flags using the union daily_set, writes the final `daily_count.csv` + `build_metadata.json` + `build_summary.md` + `docs/lane2_gdelt1_full_daily_count_build_execution_report_v0.1.md`.
5. **Consolidated memory update** — records the chunked execution completion lineage.

Until those workstreams close cleanly in sequence, the no-market-data firewall, the no-2023+ posture, the no-retry rule, the exactly-once fetch semantics, and the locked design contract from `7780a97` as amended by `c10ae74` remain in force.

This memo's authorization scope is complete upon persistence of `docs/lane2_gdelt1_full_build_runtime_feasibility_adjudication_memo_v0.1.md`. No staging, commit, or push is authorized by this memo's content; the commit + push step is a separate operational instruction in the prompt itself.
