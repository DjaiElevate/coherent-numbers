# Lane 2 GDELT1 chunk_2013_partial execution-authorization plan v0.1

## Title

`Lane 2 GDELT1 chunk_2013_partial execution-authorization plan v0.1`

This memo is **planning-only**. It does not by itself authorize execution of any chunk, GDELT contact, guard flip, output-artifact creation, retry, checkpoint/resume, off-session execution, merge execution, Step 2 work, or market-data logic. Its persistence scope is one tracked file at `docs/lane2_gdelt1_full_build_chunk_2013_partial_execution_authorization_plan_v0.1.md`.

## Current anchor

| Item | Value |
|---|---|
| `HEAD = origin/main` | `389747eb904302e33fc6f76ba1f2bf215b2723c4` |
| Short SHA | `389747e` |
| Implementation review verdict for `389747e` | `PASS — IMPLEMENTATION CONFORMANT` |
| Target chunk | `chunk_2013_partial` |
| Expected chunk URL count | **`275`** |
| Chunk date range | `2013-04-01` through `2013-12-31` (inclusive) |
| Recognized-list authority SHA-256 | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` |
| Locked offset taxonomy | `{0, −1, −7, −30, −365, −3650, +1}` (exact-integer; `487dadb`) |
| Locked output window | `[2013-04-01, 2022-12-31]` (`7780a97` §6.8 / no-2023+ posture at `0ddbd51`) |
| Chunk-runner module guard line | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95:FULL_BUILD_AUTHORIZED = False` |

## Purpose

This memo prepares the **future live execution envelope** for `chunk_2013_partial` only — the first of 10 yearly fetch-file chunks per the chunk-design memo `5962c20`. It defines the enable / single live run / restore / post-chunk-report sequence in design-level detail, the stop conditions, the expected successful output, the halt output, the boundary statement, and the open pre-execution decision points. It is a **planning artifact for review**, not an execution authorization.

Explicitly:

- This memo does **not** execute the chunk.
- This memo does **not** authorize GDELT contact by itself.
- This memo does **not** flip guards.
- This memo does **not** create production output artifacts.
- This memo does **not** authorize retries.
- This memo does **not** authorize checkpoint/resume.
- This memo does **not** authorize off-session execution.
- This memo does **not** authorize merge execution.
- This memo does **not** authorize Step 2 or market-data logic.
- This memo does **not** authorize a chain of subsequent chunks (`chunk_2014` through `chunk_2022` each require their own separately authorized execution prompt).

## Inherited locked rules

The future execution prompt and the live run it authorizes will inherit all of the following locked premises without re-litigation:

- **Recognized-list authority** (`84ea721e…fff835fc`): only daily URLs derived from the §10 capture, filtered to chunk_2013_partial's year range, may be fetched.
- **SQLDATE re-keying** (`0065d10` §5): every parsed row contributes to its `SQLDATE`, not to the publishing-file nominal date.
- **No-market-data firewall**: in force unconditionally.
- **No-2023+ posture** (`0ddbd51` / `7780a97` §11.1): no 2023+ URL construction; no 2023+ SQLDATE accepted in primary logic; hard-fail per Decision I on any breach.
- **No-retry rule** (`7780a97` §13.4 / Decision I): single transient HTTP/network failure halts the chunk; no recovery within the cycle.
- **Exactly-once fetch semantics** (`7780a97` §13.3): each in-chunk URL is fetched at most once.
- **No raw payload preservation** (`7780a97` §15.11): each fetched payload is hashed + parsed + discarded before the next URL; only the SHA-256 is retained in the per-chunk manifest.
- **No category/theme/actor/geography/tone filtering** (`7780a97` §8 + `c10ae74` §8 firewall framing): Step 2 / instrument-construction territory; forbidden.
- **No instrument construction**: gated behind a separately authorized firewall-retirement memo + Step 2 authorization.
- **No Step 2**: same gate.
- **No off-session execution** (`fbc605b`): Plan-C reserve only; not authorized.
- **No checkpoint/resume** (`fbc605b`): Plan-B reserve only; not implemented.
- **No bounded parallelism** (`d7c8775` Decision 2B rejected).
- **Per-chunk output is NOT the final canonical `daily_count.csv`**: the merge step is the only producer of `daily_count.csv` + `build_metadata.json` + `build_summary.md` + manifests, and the merge step is **separately authorized later** (`5962c20` §14 step 6).
- **`c10ae74` coverage-domain amendment**: 7-entry closed `coverage_quality_flag` domain including `t_minus_n_neighbor_substrate_gap`; `+`-joined multi-cause representation as implementation reality (`bc7b66b`).

## Chunk manifest expectation

The future live run for `chunk_2013_partial` will fetch:

- **Only daily publishing-file URLs** with nominal date in `[2013-04-01, 2013-12-31]` inclusive.
- **Exactly `275` URLs** (verified by `EXPECTED_CHUNK_COUNTS["chunk_2013_partial"]` in the runner; the runner's `build_chunk_manifest` will hard-fail if the actual count differs).
- **Zero yearly recognized units** (`"2005"`, `"2013"` from the recognized-list capture's 2-element yearly subset are excluded by the daily-only regex filter).
- **Zero monthly recognized units** (the 87-element `YYYY-MM` subset is excluded by the same filter).
- **Zero 2023+ URLs** (the year range stops at `2013-12-31`; `date_to_daily_url` enforces a redundant `SEAL_START` precondition check).
- **Zero substrate-gap dates** (the four known gaps `2014-01-23`/`-24`/`-25`/`2014-03-19` are all in 2014, outside chunk_2013_partial's range — so the gap-exclusion logic happens at a chunk that this plan does not authorize).

The runner will compute the chunk manifest **digest** at execution time as `chunk_manifest_digest(chunk_iso_dates)` (`scripts/run_lane2_gdelt1_full_daily_count_build.py:1609`): sorted ASCII-encoded URLs joined by `\n`, then SHA-256. The digest is recorded in `chunk_metadata.json` for later cross-check by the merge step.

Chunk output must contain **derived-only** artifacts (per `5962c20` §8 and `c10ae74` Decision 2A):

- `chunk_contributions.csv` — per-SQLDATE per-offset in-window contributions for this chunk only.
- `chunk_metadata.json` — provenance (chunk_id, source recognized-list SHA, chunk manifest digest, expected file count, actual completed file count, script anchor commit, guard state after restore, started/finished UTC, no-retry confirmation, boundary declarations, per-URL manifest with HTTP status + payload SHA-256 + per-offset row count, substrate-gap diagnostic, out-of-window SQLDATE diagnostic, parser-anomaly diagnostic, output allow-list).
- `chunk_summary.md` — human-readable summary.
- `halt_diagnostic.json` — only on hard-fail paths; derived metadata only (`halt_class`, `message`, `started_at_utc`, `halted_at_utc`, `chunk_id`, `actual_completed_file_count`).

**No raw payload bytes** in any artifact. **No extracted CSV rows** in any artifact. **No SQLDATE values per individual event row** — only per-SQLDATE per-offset aggregate counts.

## Future execution sequence

The future execution prompt (separately initiated; **NOT** authorized by this plan) will perform the following steps in order. The future prompt must reproduce this sequence verbatim or revise it explicitly via a corrective plan.

1. **Preflight read-only verification**. Confirm: `HEAD = origin/main = 389747e` (or its accepted successor if a memory-update or other intervening commit has landed); ahead = `0`; tracked tree clean; all five guards `False` on disk; production `results/lane2_gdelt1_full_daily_count_build/` does not contain a colliding `chunk_2013_partial_<UTC_TIMESTAMP>/` subdirectory; recognized-list SHA `84ea721e…fff835fc` intact; F4 baselines intact; chunk-runner source file byte-identical to `389747e`'s committed version (no in-flight edits).
2. **Enable commit**: flip `FULL_BUILD_AUTHORIZED = False` → `True` on **line 95** of `scripts/run_lane2_gdelt1_full_daily_count_build.py` via a single one-line `+1/−1` edit. Subject: `Enable Lane 2 full-build chunk_2013_partial run`. The commit must contain exactly one file changed; `git diff HEAD~ HEAD --numstat` must show `1\t1\tscripts/run_lane2_gdelt1_full_daily_count_build.py`. Mirrors `3537a62` / `e81208d` / `60ec1521` precedent.
3. **Single live run** of exactly one shell command (single invocation, inline env var, NOT `export`):
   ```
   LANE2_FULL_BUILD_AUTHORIZED=1 python3 scripts/run_lane2_gdelt1_full_daily_count_build.py \
     --authorize-full-build-run --chunk-id chunk_2013_partial
   ```
   Capture stdout, stderr, exit code, start UTC, end UTC, output directory path. The runner is expected to create `results/lane2_gdelt1_full_daily_count_build/chunk_2013_partial_<UTC_TIMESTAMP>/` and write `chunk_contributions.csv` + `chunk_metadata.json` + `chunk_summary.md` (success path) or `halt_diagnostic.json` (halt path) + the partial allowable artifacts. The env var `LANE2_FULL_BUILD_AUTHORIZED` must be `UNSET` after the run command's process exits (inline-env discipline; no leaked-to-shell session state).
4. **Restore commit**: flip line-95 back to `False`. Subject: `Restore Lane 2 full-build guard after chunk_2013_partial`. Same `1\t1` numstat. The runner source must be byte-identical to its `389747e` committed state after restore (verify via `git diff 389747e HEAD -- scripts/run_lane2_gdelt1_full_daily_count_build.py` returning empty). Restore happens **regardless of success or halt** of the live run.
5. **Verify all five guards `False` after restore** via `git grep -nE "^(REAL_RETRIEVAL_ENABLED|COUNT_FEASIBILITY_AUTHORIZED|EVENT_FILE_PROBE_AUTHORIZED|ROW_DATE_CHARACTERIZATION_AUTHORIZED|FULL_BUILD_AUTHORIZED) = "`; all four `LANE2_*_AUTHORIZED` shell envs `UNSET`.
6. **Verify output-artifact allow-list**: the chunk's output directory, if present, must contain only files from `ALLOWED_CHUNK_OUTPUT_BASENAMES` = `{chunk_contributions.csv, chunk_metadata.json, chunk_summary.md, halt_diagnostic.json}`. No `.zip` / `.CSV` / `tmp_*` / subdirectories. The runner's `_assert_chunk_outputs_allowed` tripwire runs on the success path; the future prompt should manually re-verify via `ls` post-restore.
7. **Write a tracked post-chunk execution report** at `docs/lane2_gdelt1_full_build_chunk_2013_partial_execution_report_v0.1.md` (mirrors `858b501` discipline for the row-date characterization execution report). The report records: preflight state; enable-commit SHA; live-run command verbatim + start/end UTC + exit code + stdout/stderr summary; output directory path; chunk manifest digest; URL count (expected 275 / actual N); per-URL summary (HTTP status, SHA-256, row count, offset distribution); aggregate in-window/out-of-window row counts; per-offset totals (which by construction will include zero T-3650 rows in the chunk's per-SQLDATE-per-offset map, since all T-3650 rows in 2013-04-01 through 2013-12-31 files have pre-window SQLDATEs); parser anomalies (malformed-short, unparseable SQLDATE, header anomaly); halt class + diagnostic SHA if halted; restore-commit SHA; post-restore guard state; output artifact SHA-256 manifest; boundary confirmations.
8. **Commit cycle** for the guard flips and the post-chunk report (the chunk-output artifacts themselves remain **untracked by default** per `5962c20` §8.2 / `7780a97` §15.10, unless the policy decision in §"Open decision before live execution" below is resolved otherwise pre-execution). See the policy-decision section for the exact commit-order question.

The future execution prompt may NOT:

- Authorize a second URL fetch for any URL whose first fetch failed.
- Authorize fetching outside `chunk_2013_partial`'s 275-URL manifest.
- Authorize flipping any guard other than `FULL_BUILD_AUTHORIZED`.
- Authorize bundling the next chunk's execution into the same prompt (each of the remaining 9 chunks requires its own separate authorization).
- Authorize the merge step.

## Stop conditions for future execution

Hard stop conditions that the future execution prompt must enforce. Any single one halts the cycle:

**Preflight hard-stops** (execution does not begin):

- HEAD ≠ accepted ancestor (e.g., not `389747e` or a successor that has been reviewed and recorded in memory).
- `origin/main` mismatch with HEAD.
- Tracked tree dirty (any `M`/`A`/`D`/`R` entries from `git status --porcelain`).
- Any of the five guards is `True` on disk pre-enable.
- Any `LANE2_*_AUTHORIZED` shell env is set pre-enable.
- Production target output directory `results/lane2_gdelt1_full_daily_count_build/chunk_2013_partial_<UTC_TIMESTAMP>/` already exists with the chosen timestamp (runner's `os.makedirs(..., exist_ok=False)` will hard-fail on collision).
- Recognized-list SHA mismatch with `84ea721e…fff835fc`.
- F4 baseline SHA mismatch.
- Chunk-runner source file diverges from `389747e`'s committed state pre-enable.

**Runner-internal hard-stops** during the live run (`run_chunk_build` raises and `_write_chunk_halt_diagnostic` writes the halt artifact, then `raise` re-raises):

- Chunk manifest actual count ≠ `275` (`ChunkManifestError` from `build_chunk_manifest`).
- Recognized-list SHA mismatch at runtime (`RecognizedListSchemaError`).
- Reconciliation contradiction (`ReconciliationContradiction`): per-year classification differs from expected (e.g., capture mutated between memory-recording and execution).
- HTTP non-200 for any in-chunk URL (`FetchFailure` via `_fetch_one_payload`).
- Redirect (any 3xx) for any in-chunk URL (`FullBuildRedirectBlocked` via `_FullBuildNoFollowRedirectHandler` → translated to `FetchFailure`).
- Connection error / timeout for any in-chunk URL (`FetchFailure`).
- Unexpected offset outside `{0, −1, −7, −30, −365, −3650, +1}` for any parsed row (`FullBuildBoundaryBreach`).
- 2023+ SQLDATE in any parsed row (`FullBuildBoundaryBreach`).
- 2023+ URL construction attempt (`FullBuildBoundaryBreach` via `date_to_daily_url` precondition).
- Output allow-list violation (`FullBuildBoundaryBreach` via `_checked_chunk_output_path` or post-hoc tripwire).
- Header anomaly on a parsed file (recorded as reportable diagnostic in the per-file manifest; does NOT by itself halt unless promoted by a future tightening — current implementation reports but continues).
- Counting-invariant violation (`FullBuildBoundaryBreach`): in-window + out-of-window + malformed + unparseable ≠ total parsed rows.

**Post-run hard-stops** that block report-commit:

- Inability to restore `FULL_BUILD_AUTHORIZED = False` (e.g., source-edit failure).
- Any guard `True` on disk after the restore commit.
- Any output outside `ALLOWED_CHUNK_OUTPUT_BASENAMES` present in the chunk output directory.
- Any raw payload bytes (`.zip`) present in the chunk output directory.
- Any extracted CSV rows (`.CSV`) present in the chunk output directory.
- Any retry attempt observed in the runner's per-URL manifest (the runner's no-retry semantics should prevent this; the post-run check is defense-in-depth).
- Any second-GET attempt for the same URL.
- Any accidental market-data / Step 2 / spike-burst / return-window logic appearing in the chunk metadata or summary (e.g., from a runner regression that this plan would not anticipate).

Any halt condition triggers the **session-interruption recovery rule** from the prior runtime-feasibility-block execution prompt (steps 1–13 of "Session-interruption recovery rule"): the future execution prompt's halt branch must restore the guard, preserve partial output as-is, and emit verdict `FULL-BUILD CHUNK_2013_PARTIAL RUN HALTED — AWAIT ADJUDICATION` (mirroring `RUNTIME-FEASIBILITY-BLOCK — AWAIT ADJUDICATION`).

## Expected successful output

If the future live run completes without halt, the chunk output directory will contain **exactly three files** (allow-list gated):

- `results/lane2_gdelt1_full_daily_count_build/chunk_2013_partial_<UTC_TIMESTAMP>/chunk_contributions.csv` — per-SQLDATE per-offset in-window contributions from the 275 fetched files. Expected non-trivial rows for SQLDATEs in roughly `[2003-04, 2014-01]` (T−3650 through T+1 contributions from the 2013-04-01 through 2013-12-31 files; the in-window subset is restricted to `[2013-04-01, 2022-12-31]` so T−3650 rows go to the out-of-window diagnostic, not this CSV).
- `chunk_metadata.json` — derived provenance (chunk_id, source recognized-list SHA, chunk manifest digest, expected_file_count=275, actual_completed_file_count=275 on full success, script anchor, guard state after restore, started/finished UTC, no_retry_confirmation=true, boundary_declarations, per-URL manifest, substrate-gap diagnostic, out-of-window SQLDATE diagnostic, parser-anomaly diagnostic, allow-list, aggregate_metrics).
- `chunk_summary.md` — human-readable summary.

On successful completion:

- **No `halt_diagnostic.json`** is written (the success path does not invoke `_write_chunk_halt_diagnostic`).
- **No raw payload bytes** are present (per-URL discard via `del payload` between iterations).
- **No extracted CSV rows** are present.
- **No final `daily_count.csv`** — that is a merge-step artifact, not a chunk-step artifact.
- **No `build_metadata.json`** (merge-step artifact).
- **No `build_summary.md`** (merge-step artifact).
- **No merge outputs** — merge is separately authorized.
- **No tracked full-build execution report** at `docs/lane2_gdelt1_full_daily_count_build_execution_report_v0.1.md` — that is also a separately authorized post-merge artifact.

The tracked post-chunk report is the only `docs/` artifact for this chunk cycle:

**`docs/lane2_gdelt1_full_build_chunk_2013_partial_execution_report_v0.1.md`**

## Halt output

If the future live run halts on any Decision I condition or any of the stop conditions in §"Stop conditions for future execution" above:

- The chunk output directory may contain a **derived-only** `halt_diagnostic.json` with: `halt_class` (Python exception class name), `message` (`str(e)` representation), `started_at_utc`, `halted_at_utc`, `chunk_id = "chunk_2013_partial"`, `actual_completed_file_count` (integer count of URLs successfully fetched + parsed before halt; may be 0 if halt fires before the first fetch).
- The chunk output directory **may exist with no other files** if halt fires before any artifact-write call; **may also exist with no files** if halt fires before the `_fresh_chunk_output_dir` call (e.g., chunk_id validation or guard refusal).
- **No retry**: the runner does not re-fetch the failing URL.
- **No continuation**: the runner does not skip past the failing URL to subsequent URLs.
- **No merge**: any halt at chunk_2013_partial automatically blocks the merge step (merge requires all 10 chunks successful per `5962c20` §9.1.2).
- **No automatic next chunk**: chunks 2014 through 2022 require their own separately authorized execution prompts; a chunk_2013_partial halt does not block them in principle, but any rational sequencing would adjudicate the halt before proceeding.
- **Any halt requires adjudication before proceeding**: a separately authorized halt-adjudication memo (or a retry-without-this-plan corrective) is required before any further Lane 2 execution.

The future execution prompt should commit only:

- The enable commit (line-95 flip to True).
- The restore commit (line-95 flip back to False; runner byte-identical to `389747e`).
- The tracked post-chunk execution report (which documents the halt class, diagnostic SHA, partial output disposition, and verdict).

The chunk output directory and its `halt_diagnostic.json` remain **untracked by default** per the §"Open decision before live execution" policy question below.

## Boundary statement

This plan authorizes **none** of the following:

- Live execution of `chunk_2013_partial` or any other chunk.
- GDELT contact.
- Guard flip on any runner (the five guards remain `False` on disk and the four `LANE2_*_AUTHORIZED` shell envs remain `UNSET` throughout the planning turn).
- Retry of any URL.
- Checkpoint/resume implementation.
- Off-session execution.
- Merge execution.
- Market data of any kind.
- Step 2 of any kind.
- Output-artifact mutation (pre-existing `results/lane2_gdelt1_event_file_probe/`, `results/lane2_gdelt1_row_date_characterization/`, `results/lane2_gdelt1_count_feasibility/` untouched).
- Recognized-list mutation (SHA `84ea721e…fff835fc` preserved).
- F4 mutation (baselines `41c80c09…624c39d` / `00ce9b24…5e37552c` preserved).
- Memory edit.
- Code edit (`scripts/`, `src/`, `tests/` byte-identical to `389747e`).
- Test edit.
- Production output directory creation (`results/lane2_gdelt1_full_daily_count_build/` still does not exist).
- Locked-memo edit to `9319d30` / `a8a9dd2` / `a2a8fd5` / `e9f8781` / `487dadb` / `3537a62` / `73a7911` / `858b501` / `0065d10` / `7780a97` / `bc7b66b` / `c10ae74` / `d7c8775` / `fbc605b` / `5962c20` / `389747e` / `e55e09a` / `0b341b4` / `845c51c` / `e81208d` / `7c85e3f`.
- Staging / commit / push of this plan or any other artifact (the plan's commit is a separately authorized follow-up step, NOT part of this planning turn).

The no-market-data firewall, the no-2023+ posture, the no-retry rule, the exactly-once fetch semantics, and the locked design contract from `7780a97` as amended by `c10ae74` + the chunk-design contract from `5962c20` all remain in force.

## Open decision before live execution

Three explicit decision points must be resolved by the future execution prompt (or by a separately authorized policy memo) before live execution begins. The current Lane 2 policy does not unambiguously answer all three, so each is flagged as a **pre-execution decision point**.

### Decision point 1 — chunk-output artifact disposition

**Question**: are the chunk_2013_partial output artifacts (`chunk_contributions.csv`, `chunk_metadata.json`, `chunk_summary.md`) **committed to the repo** alongside the post-chunk execution report, or **kept untracked** and referenced by SHA-256 / path from the tracked post-chunk report?

**Default policy** (per `5962c20` §8.2 and §10.2's "untracked by default" framing, mirroring `0065d10` Decision 3A): per-chunk artifacts are **untracked by default**. The tracked post-chunk execution report records SHA-256 references and path. This is the prevailing precedent (e.g., `858b501` for the row-date characterization sample).

**Counter-argument**: chunk_contributions.csv is small (~275 rows × ~10 columns = a few KiB) and a tracked copy would provide bytes-witness independent of GDELT-side mutability. A tracked copy would also enable downstream tools to read chunk artifacts directly from a clean clone without needing to re-fetch from GDELT or rely on the original author's local disk.

**Pre-execution decision required**: the future execution prompt must **explicitly state** whether it follows the untracked-by-default precedent or adopts a tracked-artifact policy. If the latter, the policy must specify how all 10 chunks' artifacts will be committed consistently (a future tracked-artifact policy memo would govern all 10 chunks, not just chunk_2013_partial).

### Decision point 2 — commit sequence

**Question**: what is the **exact commit sequence** for the four commit-candidate items?

The four items are:

- **(a)** Enable commit (line-95 `True`).
- **(b)** Live run output (the chunk output directory + its three or four files).
- **(c)** Restore commit (line-95 `False`).
- **(d)** Post-chunk execution report.

The prevailing precedent (e.g., `3537a62 → 73a7911 → 858b501`) is:

1. Enable commit (a).
2. Live run produces output dir (b) — but per the untracked-by-default default of Decision point 1, (b) is **NOT committed**.
3. Restore commit (c).
4. Post-chunk report commit (d).

So the prevailing precedent has three commits: `enable → restore → report`. The live-run output is left untracked.

If Decision point 1 adopts the tracked-artifact policy instead, the commit count grows: `enable → output → restore → report` (four commits) OR `enable → restore → output+report` (three commits, with output+report bundled). The future execution prompt must pick one explicitly.

**Pre-execution decision required**: the future execution prompt must state the exact ordered list of commits and which file(s) each commit stages. Recommended starting point (matches prevailing precedent): three commits `enable → restore → report` with output left untracked.

### Decision point 3 — post-chunk report commit timing

**Question**: does the post-chunk report get committed in the **same cycle** as the output artifacts (if Decision point 1 adopts tracking), or in a **separate** subsequent cycle?

Under the untracked-by-default precedent, this question is moot — the post-chunk report is committed in its own commit (item (d) above) and the output is untracked.

If Decision point 1 adopts tracking, the question becomes: a single commit containing both the output artifacts AND the report (one atomic record of the cycle), OR two commits (output first, report second)?

**Recommended position**: if Decision point 1 stays at untracked-by-default (the default position), Decision point 3 resolves automatically — the report is committed in its own commit and there is no "same-cycle" question.

**Pre-execution decision required only if Decision point 1 adopts tracking**: state the commit-timing relationship between output and report.

### Decision point summary

If the future execution prompt accepts the **untracked-by-default** position on Decision point 1, then Decision points 2 and 3 resolve to:

- **Three commits**, in order: `Enable Lane 2 full-build chunk_2013_partial run` → `Restore Lane 2 full-build guard after chunk_2013_partial` → `Record Lane 2 full-build chunk_2013_partial execution report`.
- Output artifacts remain untracked under `results/lane2_gdelt1_full_daily_count_build/chunk_2013_partial_<UTC_TIMESTAMP>/`.
- Report at `docs/lane2_gdelt1_full_build_chunk_2013_partial_execution_report_v0.1.md`.

If the future execution prompt adopts a **tracked-artifact policy**, a separate policy-decision memo should land first (analogous to a future revision of `0065d10` Decision 3A or `5962c20` §8.2).

## Next step

The next step after persistence of this planning memo is **review of the plan**, not execution. The review may be performed read-only by the user or by a separately invoked review-only prompt. If the review surfaces no issues, the next eligible workstream is the **chunk_2013_partial execution-authorization prompt** itself — a separately initiated prompt that performs the steps in §"Future execution sequence" above.

If the review surfaces issues (e.g., an unresolved decision point that requires a policy-decision memo first), a corrective revision of this plan or a precursor policy memo would precede the execution-authorization prompt.

**No execution is initiated by this planning memo.** Its persistence scope is complete upon writing the single tracked file at `docs/lane2_gdelt1_full_build_chunk_2013_partial_execution_authorization_plan_v0.1.md`. No staging, commit, or push is authorized by the content of this plan.
