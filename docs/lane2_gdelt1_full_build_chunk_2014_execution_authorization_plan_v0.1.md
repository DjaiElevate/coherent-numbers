# Lane 2 GDELT1 chunk_2014 execution-authorization plan v0.1

## Title

`Lane 2 GDELT1 chunk_2014 execution-authorization plan v0.1`

This memo is **planning-only**. It does not by itself authorize execution of any chunk, GDELT contact, guard flip, output-artifact creation, retry, checkpoint/resume, off-session execution, merge execution, Step 2 work, or market-data logic. Its persistence scope is one tracked file at `docs/lane2_gdelt1_full_build_chunk_2014_execution_authorization_plan_v0.1.md`.

## Current anchor

| Item | Value |
|---|---|
| `HEAD = origin/main` | `065d4754f69e2c35eef1ebdb7e4bf960ca9e806b` |
| Short SHA | `065d475` |
| Latest execution commit (closing `chunk_2013_partial`) | report `065d475` (preceded by enable `c6b313c` → restore `167a08a`) |
| `chunk_2013_partial` execution status | **SUCCESS** — `actual_completed_file_count = expected_file_count = 275`; output untracked at `results/lane2_gdelt1_full_daily_count_build/chunk_2013_partial_20260524T135157Z/`; report committed at `docs/lane2_gdelt1_full_build_chunk_2013_partial_execution_report_v0.1.md` |
| `chunk_2013_partial` manifest digest | `6ac92439455d3f59df64cfeca6256f54a319c0ac82d40886f11b26becbfc8b43` |
| Target chunk | **`chunk_2014`** |
| Expected chunk URL count | **`361`** |
| Chunk date range | `2014-01-01` through `2014-12-31` (inclusive) |
| Calendar-arithmetic check | `365 calendar days − 4 known substrate gaps = 361` |
| Known absent substrate-gap dates inside this range | `2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19` |
| Recognized-list authority SHA-256 | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` |
| F4 baseline SHAs (preserved) | `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d` / `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c` |
| Locked offset taxonomy | `{0, −1, −7, −30, −365, −3650, +1}` (exact-integer; `487dadb`) |
| Locked output window | `[2013-04-01, 2022-12-31]` (`7780a97` §6.8 / no-2023+ posture at `0ddbd51`) |
| Chunk-runner module guard line | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95:FULL_BUILD_AUTHORIZED = False` |
| Runner anchors for `chunk_2014` | `EXPECTED_CHUNK_COUNTS["chunk_2014"] = 361` (line 1529); canonical chunk list entry (line 1516); date-range tuple `(date(2014,1,1), date(2014,12,31))` (line 1542); `KNOWN_SUBSTRATE_GAPS = ["2014-01-23","2014-01-24","2014-01-25","2014-03-19"]` (lines 126–129) |
| Substrate progress as of this memo | 1 of 10 chunks complete (`chunk_2013_partial`); 275 of 3,558 daily URLs complete; 9 chunks + 3,283 daily URLs remain |

## Purpose

This memo prepares the **future live execution envelope** for `chunk_2014` only — the second of 10 yearly fetch-file chunks per the chunk-design memo `5962c20`. It defines the enable / single live run / restore / post-chunk-report sequence in design-level detail, the stop conditions, the expected successful output, the halt output, the boundary statement, and the prior-chunk continuity checks. It is a **planning artifact for review**, not an execution authorization.

Explicitly:

- This memo does **not** execute the chunk.
- This memo does **not** authorize GDELT contact by itself.
- This memo does **not** flip guards.
- This memo does **not** create output artifacts.
- This memo does **not** authorize retries.
- This memo does **not** authorize checkpoint/resume.
- This memo does **not** authorize off-session execution.
- This memo does **not** authorize merge execution.
- This memo does **not** authorize Step 2 or market-data logic.
- This memo does **not** authorize re-running `chunk_2013_partial`.
- This memo does **not** authorize bundling chunks 2015 through 2022 — each requires its own separately authorized execution prompt.

## Inherited locked rules

The future execution prompt and the live run it authorizes will inherit all of the following locked premises without re-litigation:

- **Recognized-list authority** (`84ea721e…fff835fc`): only daily URLs derived from the §10 capture, filtered to `chunk_2014`'s year range, may be fetched.
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
- **Merge remains blocked until all 10 chunks succeed** (`5962c20` §9.1.2): a successful `chunk_2014` would advance progress to 2 of 10, not unblock merge.
- **`c10ae74` coverage-domain amendment**: 7-entry closed `coverage_quality_flag` domain including `t_minus_n_neighbor_substrate_gap`; `+`-joined multi-cause representation (`bc7b66b`).

## Chunk manifest expectation

The future live run for `chunk_2014` will fetch:

- **Only daily publishing-file URLs** with nominal date in `[2014-01-01, 2014-12-31]` inclusive.
- **Exactly `361` URLs** (verified by `EXPECTED_CHUNK_COUNTS["chunk_2014"] = 361` in the runner; `build_chunk_manifest` will hard-fail if the actual count differs).
- **Zero yearly recognized units** (the 2-element yearly subset of the recognized list is excluded by the daily-only regex filter).
- **Zero monthly recognized units** (the 87-element `YYYY-MM` subset is excluded by the same filter).
- **Zero 2023+ URLs** (the year range stops at `2014-12-31`; `date_to_daily_url` enforces a redundant `SEAL_START` precondition check).
- **Exactly 4 substrate-gap exclusions** inside this calendar year: `2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`. The recognized-list-derived chunk manifest already omits these dates (they have no corresponding daily URL in the §10 capture). Calendar arithmetic: `365 − 4 = 361`.

The runner will compute the chunk manifest **digest** at execution time as `chunk_manifest_digest(chunk_iso_dates)` (`scripts/run_lane2_gdelt1_full_daily_count_build.py:1609`): sorted ASCII-encoded URLs joined by `\n`, then SHA-256. The digest is recorded in `chunk_metadata.json` for later cross-check by the merge step. The `chunk_2014` digest is **not** computable in advance from this planning memo (it is derived at execution time from the per-URL strings) and will be a new value distinct from `chunk_2013_partial`'s `6ac92439…bfc8b43`.

Chunk output must contain **derived-only** artifacts (per `5962c20` §8 and `c10ae74` Decision 2A):

- `chunk_contributions.csv` — per-SQLDATE per-offset in-window contributions for this chunk only.
- `chunk_metadata.json` — provenance (chunk_id, source recognized-list SHA, chunk manifest digest, expected_file_count = 361, actual_completed_file_count, script anchor commit, guard state after restore, started/finished UTC, no_retry_confirmation, boundary_declarations, per-URL manifest with HTTP status + payload SHA-256 + per-offset row count, substrate-gap diagnostic, out-of-window SQLDATE diagnostic, parser-anomaly diagnostic, output allow-list).
- `chunk_summary.md` — human-readable summary.
- `halt_diagnostic.json` — only on hard-fail paths; derived metadata only (`halt_class`, `message`, `started_at_utc`, `halted_at_utc`, `chunk_id`, `actual_completed_file_count`).

**No raw payload bytes** in any artifact. **No extracted CSV rows** in any artifact. **No SQLDATE values per individual event row** — only per-SQLDATE per-offset aggregate counts.

## Prior chunk continuity

`chunk_2013_partial` succeeded and remains the only chunk yet executed. The future `chunk_2014` execution must not modify, re-run, or overwrite any `chunk_2013_partial` output.

| Item | Value |
|---|---|
| `chunk_2013_partial` output directory | `results/lane2_gdelt1_full_daily_count_build/chunk_2013_partial_20260524T135157Z/` (untracked by default; not committed) |
| `chunk_2013_partial` artifacts | `chunk_contributions.csv` (17,642 B, SHA-256 `9f07c8018c322027841dbf6484f19c2218d2945731e775b9ced03099cfa37247`); `chunk_metadata.json` (214,857 B, SHA-256 `14a407a49e53f660a581bcdc7cee224e3228046aa1ea51eaae5e7eb5dc8a03c1`); `chunk_summary.md` (440 B, SHA-256 `9e88e95cc33e4f99ddc3a810db23cd076ac51928d7504b7bab35780d5d15ed42`) |
| `chunk_2013_partial` manifest digest | `6ac92439455d3f59df64cfeca6256f54a319c0ac82d40886f11b26becbfc8b43` |
| `chunk_2013_partial` completed count | `275 / 275` |
| `chunk_2013_partial` execution report | `docs/lane2_gdelt1_full_build_chunk_2013_partial_execution_report_v0.1.md` (tracked; committed at `065d475`) |

Continuity-check requirements for the future execution prompt (preflight, read-only):

- The four `chunk_2013_partial` artifact SHA-256 values above must still match on disk.
- The `chunk_2013_partial` output directory must remain at the exact path above (no rename, no move, no deletion).
- The `chunk_2013_partial` execution report must remain tracked at the path above and byte-identical to the `065d475` committed copy.
- No `chunk_2014_*` subdirectory must already exist inside `results/lane2_gdelt1_full_daily_count_build/` pre-enable (the runner's `os.makedirs(..., exist_ok=False)` would hard-fail on collision).

The `chunk_2014` execution must not touch the `chunk_2013_partial` output directory in any way (read-only continuity preservation is sufficient and required).

## Future execution sequence

The future execution prompt (separately initiated; **NOT** authorized by this plan) will perform the following steps in order. The future prompt must reproduce this sequence verbatim or revise it explicitly via a corrective plan.

1. **Preflight read-only verification**. Confirm: `HEAD = origin/main = 065d475` (or its accepted successor if a memory-update or other intervening commit has landed); ahead = `0`; tracked tree clean; all five guards `False` on disk; production `results/lane2_gdelt1_full_daily_count_build/` exists (from the prior `chunk_2013_partial` cycle) but does not contain a colliding `chunk_2014_<UTC_TIMESTAMP>/` subdirectory; recognized-list SHA `84ea721e…fff835fc` intact; F4 baselines intact; chunk-runner source file byte-identical to its current committed state at `065d475` (which is byte-identical to `389747e`); `chunk_2013_partial` output + report continuity checks above pass.
2. **Enable commit**: flip `FULL_BUILD_AUTHORIZED = False` → `True` on **line 95** of `scripts/run_lane2_gdelt1_full_daily_count_build.py` via a single one-line `+1/−1` edit. Subject: **`Enable Lane 2 full-build chunk_2014 run`**. The commit must contain exactly one file changed; `git diff HEAD~ HEAD --numstat` must show `1\t1\tscripts/run_lane2_gdelt1_full_daily_count_build.py`. Mirrors the `chunk_2013_partial` enable precedent at `c6b313c`.
3. **Single live run** of exactly one shell command (single invocation, inline env var, NOT `export`):
   ```
   LANE2_FULL_BUILD_AUTHORIZED=1 python3 scripts/run_lane2_gdelt1_full_daily_count_build.py \
     --authorize-full-build-run --chunk-id chunk_2014
   ```
   Capture stdout, stderr, exit code, start UTC, end UTC, output directory path. The runner is expected to create `results/lane2_gdelt1_full_daily_count_build/chunk_2014_<UTC_TIMESTAMP>/` and write `chunk_contributions.csv` + `chunk_metadata.json` + `chunk_summary.md` (success path) or `halt_diagnostic.json` (halt path) + the partial allowable artifacts. The env var `LANE2_FULL_BUILD_AUTHORIZED` must be `UNSET` after the run command's process exits (inline-env discipline; no leaked-to-shell session state). The future prompt should default to **in-session background execution** with harness completion capture (per the successful `chunk_2013_partial` strategy at shell `bgzz8eqe5`), unless its own preflight surfaces a stronger reason not to. Background execution is same-session, not off-session.
4. **Restore commit**: flip line-95 back to `False`. Subject: **`Restore Lane 2 full-build guard after chunk_2014`**. Same `1\t1` numstat. The runner source must be byte-identical to its `065d475`-equivalent (and `389747e`-equivalent) committed state after restore (verify via `git diff 389747e HEAD -- scripts/run_lane2_gdelt1_full_daily_count_build.py` returning empty). Restore happens **regardless of success or halt** of the live run.
5. **Verify all five guards `False` after restore** via `grep -nE "^(REAL_RETRIEVAL_ENABLED|COUNT_FEASIBILITY_AUTHORIZED|EVENT_FILE_PROBE_AUTHORIZED|ROW_DATE_CHARACTERIZATION_AUTHORIZED|FULL_BUILD_AUTHORIZED) = "` against the five guard files; all four `LANE2_*_AUTHORIZED` shell envs `UNSET`.
6. **Verify output-artifact allow-list**: the `chunk_2014` output directory, if present, must contain only files from `ALLOWED_CHUNK_OUTPUT_BASENAMES` = `{chunk_contributions.csv, chunk_metadata.json, chunk_summary.md, halt_diagnostic.json}`. No `.zip` / `.CSV` / `tmp_*` / subdirectories. The runner's `_assert_chunk_outputs_allowed` tripwire runs on the success path; the future prompt should manually re-verify via `ls` post-restore.
7. **Verify `chunk_2013_partial` continuity post-run**: the four SHA-256 values for the `chunk_2013_partial` artifacts must still match on disk; the report file must remain tracked and byte-identical.
8. **Write a tracked post-chunk execution report** at `docs/lane2_gdelt1_full_build_chunk_2014_execution_report_v0.1.md`, mirroring the `chunk_2013_partial` report at `065d475`. The report records: preflight state; enable-commit SHA; live-run command verbatim + timeout/subprocess strategy + start/end UTC + exit code + stdout/stderr summary + harness-shell ID if backgrounded; output directory path; chunk manifest digest; URL count (expected 361 / actual N); per-URL summary (HTTP status, SHA-256, row count, offset distribution); aggregate in-window/out-of-window row counts; per-offset totals; parser anomalies (malformed-short, unparseable SQLDATE, header anomaly); substrate-gap diagnostic for the four 2014 gaps; halt class + diagnostic SHA if halted; restore-commit SHA; post-restore guard state; output artifact SHA-256 manifest; boundary confirmations; `chunk_2013_partial` continuity confirmation.
9. **Commit cycle**: three commits in order — `Enable Lane 2 full-build chunk_2014 run` → `Restore Lane 2 full-build guard after chunk_2014` → `Record Lane 2 chunk_2014 execution report`. Push only after the restore commit and report commit both exist and all guards are `False` on disk. Mirrors the `chunk_2013_partial` cycle exactly.

The future execution prompt may NOT:

- Authorize a second URL fetch for any URL whose first fetch failed.
- Authorize fetching outside `chunk_2014`'s 361-URL manifest.
- Authorize flipping any guard other than `FULL_BUILD_AUTHORIZED`.
- Authorize bundling the next chunk's execution into the same prompt (each of the remaining 8 chunks after `chunk_2014` requires its own separate authorization).
- Authorize the merge step.
- Authorize re-running `chunk_2013_partial` or modifying its output / report.

## Stop conditions for future execution

Hard stop conditions that the future execution prompt must enforce. Any single one halts the cycle.

### Preflight / procedurally enforced (execution does not begin)

- HEAD ≠ accepted ancestor (e.g., not `065d475` or a successor that has been reviewed and recorded in memory).
- `origin/main` mismatch with HEAD.
- Tracked tree dirty (any `M`/`A`/`D`/`R` entries from `git status --porcelain`, ignoring pre-existing untracked items).
- Any staged files pre-enable.
- Any of the five guards is already `True` on disk pre-enable.
- Any `LANE2_*_AUTHORIZED` shell env is set pre-enable.
- Recognized-list SHA mismatch with `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`.
- F4 baseline SHA mismatch with `41c80c0…624c39d` or `00ce9b2…f5e37552c`.
- Memory mtime drift if the future prompt pins memory mtimes (sister rule to the `chunk_2013_partial` preflight pattern).
- Target post-chunk report `docs/lane2_gdelt1_full_build_chunk_2014_execution_report_v0.1.md` already exists pre-write.
- Existing `chunk_2014_<UTC_TIMESTAMP>/` subdirectory inside `results/lane2_gdelt1_full_daily_count_build/` (runner's `os.makedirs(..., exist_ok=False)` would hard-fail on collision).
- `chunk_2013_partial` output directory or any of its three artifacts missing, renamed, or SHA-256-mutated.
- `chunk_2013_partial` execution report missing or byte-diverged from its committed `065d475` copy.
- Chunk-runner source file diverges from `065d475`'s committed state (and therefore from `389747e`'s committed state) pre-enable.
- Inability to run the live command with captured exit status and sufficient timeout / background-harness coverage (a foreground tool-timeout that could orphan the subprocess is a stop condition until a viable background strategy is confirmed; see `chunk_2013_partial` precedent for the in-session background pattern).

### Runner-internal / machine-enforced (during the live run; `run_chunk_build` raises and `_write_chunk_halt_diagnostic` writes the halt artifact, then `raise` re-raises)

- Chunk manifest actual count ≠ `361` (`ChunkManifestError` from `build_chunk_manifest`).
- Recognized-list SHA mismatch at runtime (`RecognizedListSchemaError`).
- Reconciliation contradiction (`ReconciliationContradiction`): per-year classification differs from expected (e.g., capture mutated between memory-recording and execution).
- HTTP non-200 for any in-chunk URL (`FetchFailure` via `_fetch_one_payload`).
- Redirect (any 3xx) for any in-chunk URL (`FullBuildRedirectBlocked` via `_FullBuildNoFollowRedirectHandler` → translated to `FetchFailure`).
- Connection error / timeout for any in-chunk URL (`FetchFailure`).
- Unexpected offset outside `{0, −1, −7, −30, −365, −3650, +1}` for any parsed row (`FullBuildBoundaryBreach`).
- 2023+ SQLDATE in any parsed row (`FullBuildBoundaryBreach`).
- 2023+ URL construction attempt (`FullBuildBoundaryBreach` via `date_to_daily_url` precondition).
- Output allow-list violation (`FullBuildBoundaryBreach` via `_checked_chunk_output_path` or post-hoc tripwire).
- Header anomaly on a parsed file (recorded as reportable diagnostic in the per-file manifest; does NOT by itself halt under current implementation but is logged).
- Counting-invariant violation (`FullBuildBoundaryBreach`): in-window + out-of-window + malformed + unparseable ≠ total parsed rows.

### Post-run / defense-in-depth (block report commit / push)

- Inability to restore `FULL_BUILD_AUTHORIZED = False` (e.g., source-edit failure). Guard restoration on disk is the highest priority if anything fails post-run.
- Any guard `True` on disk after the restore commit.
- Any raw payload bytes (`.zip`) present in the `chunk_2014` output directory.
- Any extracted CSV rows (`.CSV`) present in the `chunk_2014` output directory.
- Any output outside `ALLOWED_CHUNK_OUTPUT_BASENAMES` present in the `chunk_2014` output directory.
- Any retry attempt observed in the runner's per-URL manifest (defense-in-depth — runner no-retry semantics should prevent this).
- Any second-GET attempt for the same URL.
- Any accidental market-data / Step 2 / spike-burst / return-window logic in the chunk metadata or summary.
- Any `chunk_2014`-cycle-time modification to `chunk_2013_partial`'s output directory or its three artifacts (SHA-256 mismatch on the post-run continuity check).
- Any accidental next-chunk run (e.g., a `chunk_2015` directory appearing in the production output dir).
- Any accidental merge run (e.g., a top-level `daily_count.csv` / `build_metadata.json` / `build_summary.md` appearing in the production output dir).

Any halt condition triggers the **session-interruption recovery rule**: the future execution prompt's halt branch must restore the guard, preserve partial output as-is, and emit verdict `FULL-BUILD CHUNK_2014 RUN HALTED — AWAIT ADJUDICATION`.

## Expected successful output

If the future live run completes without halt, the chunk output directory will contain **exactly three files** (allow-list gated):

- `results/lane2_gdelt1_full_daily_count_build/chunk_2014_<UTC_TIMESTAMP>/chunk_contributions.csv` — per-SQLDATE per-offset in-window contributions from the 361 fetched files. Expected non-trivial rows for SQLDATEs covering T−3650 through T+1 contributions from the 2014-01-01 through 2014-12-31 files; in-window subset restricted to `[2013-04-01, 2022-12-31]` so T−3650 rows (which fall pre-window for early-2014 publishing dates) go to the out-of-window diagnostic, not this CSV.
- `chunk_metadata.json` — derived provenance (`chunk_id = "chunk_2014"`, source recognized-list SHA `84ea721e…fff835fc`, chunk manifest digest, `expected_file_count = 361`, `actual_completed_file_count = 361` on full success, script anchor, guard state after run, started/finished UTC, `no_retry_confirmation = True`, boundary_declarations all `True`, per-URL manifest, substrate-gap diagnostic surfacing the four 2014 gaps, out-of-window SQLDATE diagnostic, parser-anomaly diagnostic, output allow-list, aggregate_metrics).
- `chunk_summary.md` — human-readable summary.

On successful completion:

- **No `halt_diagnostic.json`** is written (the success path does not invoke `_write_chunk_halt_diagnostic`).
- **No raw payload bytes** are present (per-URL discard via `del payload` between iterations).
- **No extracted CSV rows** are present.
- **No `.zip` payload files**.
- **No final `daily_count.csv`** — that is a merge-step artifact, not a chunk-step artifact.
- **No `build_metadata.json`** (merge-step artifact).
- **No `build_summary.md`** (merge-step artifact).
- **No merge outputs** — merge is separately authorized.
- **No tracked full-build execution report** at `docs/lane2_gdelt1_full_daily_count_build_execution_report_v0.1.md` — that is also a separately authorized post-merge artifact.
- **No modification to `chunk_2013_partial`'s output directory** (post-run SHA-256 continuity check passes).

The tracked post-chunk report is the only new `docs/` artifact for this chunk cycle:

**`docs/lane2_gdelt1_full_build_chunk_2014_execution_report_v0.1.md`**

## Halt output

If the future live run halts on any Decision I condition or any of the stop conditions in §"Stop conditions for future execution":

- The chunk output directory may contain a **derived-only** `halt_diagnostic.json` with: `halt_class` (Python exception class name), `message` (`str(e)` representation), `started_at_utc`, `halted_at_utc`, `chunk_id = "chunk_2014"`, `actual_completed_file_count` (integer count of URLs successfully fetched + parsed before halt; may be 0 if halt fires before the first fetch).
- The chunk output directory may exist with no other files if halt fires before any artifact-write call; may also exist with no files if halt fires before the `_fresh_chunk_output_dir` call (e.g., chunk_id validation or guard refusal).
- **No retry**: the runner does not re-fetch the failing URL.
- **No continuation**: the runner does not skip past the failing URL to subsequent URLs.
- **No merge**: any halt at `chunk_2014` blocks the merge step (merge already requires all 10 chunks successful per `5962c20` §9.1.2).
- **No automatic next chunk**: chunks 2015 through 2022 require their own separately authorized execution prompts; a `chunk_2014` halt does not block them in principle, but any rational sequencing would adjudicate the halt before proceeding.
- **No modification to `chunk_2013_partial`** (its output and report remain untouched).
- **Any halt requires adjudication before proceeding**: a separately authorized halt-adjudication memo (or a retry-without-this-plan corrective) is required before any further Lane 2 execution.

The future execution prompt should commit only:

- The enable commit (line-95 flip to True).
- The restore commit (line-95 flip back to False; runner byte-identical to `389747e`).
- The tracked post-chunk execution report (which documents the halt class, diagnostic SHA, partial output disposition, and verdict).

The `chunk_2014` output directory and its `halt_diagnostic.json` remain **untracked by default** per the policy in §"Decision points before live execution".

## Boundary statement

This plan authorizes **none** of the following:

- Live execution of `chunk_2014` or any other chunk.
- GDELT contact.
- Guard flip on any runner (the five guards remain `False` on disk and the four `LANE2_*_AUTHORIZED` shell envs remain `UNSET` throughout the planning turn).
- Retry of any URL.
- Checkpoint/resume implementation.
- Off-session execution.
- Merge execution.
- Market data of any kind.
- Step 2 of any kind.
- Output-artifact mutation (the `chunk_2013_partial` output directory remains untouched read-only; the pre-existing `results/lane2_gdelt1_event_file_probe/`, `results/lane2_gdelt1_row_date_characterization/`, `results/lane2_gdelt1_count_feasibility/` directories also untouched).
- Recognized-list mutation (SHA `84ea721e…fff835fc` preserved).
- F4 mutation (baselines `41c80c0…624c39d` / `00ce9b2…f5e37552c` preserved).
- Memory edit.
- Code edit (`scripts/`, `src/`, `tests/` byte-identical to `065d475`).
- Test edit.
- Re-running `chunk_2013_partial` or any other chunk.
- Running any chunk other than `chunk_2014`.
- Locked-memo edit to `9319d30` / `a8a9dd2` / `a2a8fd5` / `e9f8781` / `487dadb` / `3537a62` / `73a7911` / `858b501` / `0065d10` / `7780a97` / `bc7b66b` / `c10ae74` / `d7c8775` / `fbc605b` / `5962c20` / `389747e` / `447656d` / `c6b313c` / `167a08a` / `065d475` / `e55e09a` / `0b341b4` / `845c51c` / `e81208d` / `7c85e3f`.
- Staging / commit / push of this plan or any other artifact (the plan's commit is a separately authorized follow-up step, NOT part of this planning turn).

The no-market-data firewall, the no-2023+ posture, the no-retry rule, the exactly-once fetch semantics, the no-merge-until-10/10 rule, and the locked design contract from `7780a97` as amended by `c10ae74` + the chunk-design contract from `5962c20` all remain in force.

## Decision points before live execution

The three decision points that were open for `chunk_2013_partial` are now resolved by precedent. The `chunk_2014` execution prompt should adopt the same resolutions unless evidence shows otherwise.

| Decision point | Resolution by precedent |
|---|---|
| (1) Chunk-output artifact disposition | **Untracked by default** per `0065d10` Decision 3A + `5962c20` §8.2; output artifacts referenced by path / SHA-256 from the tracked post-chunk report only. Re-affirmed by the successful `chunk_2013_partial` cycle at `065d475`, which left the output dir untracked and recorded the three SHA-256 values in the report. Adopting a tracked-artifact policy for `chunk_2014` only (without a separate consistent policy across all 10 chunks) would violate the "consistent across all chunks" qualifier of the open question in the `chunk_2013_partial` plan and is therefore not authorized by precedent. |
| (2) Commit sequence | **Three commits in order: Enable → Restore → Report.** Reaffirmed by the `chunk_2013_partial` cycle (`c6b313c → 167a08a → 065d475`). Live-run output remains untracked under the §1 resolution. Push only after the restore commit and report commit both exist and all guards are `False` on disk. |
| (3) Post-chunk report commit timing | **Report committed in its own commit, not bundled with output**, since output is untracked under §1. Resolves automatically. |

Additional decision points specific to `chunk_2014` (resolved by precedent unless evidence shows otherwise):

- **Timeout / subprocess strategy** — default to **in-session background execution via Bash tool `run_in_background=true`** with stdout / stderr / exit code / wall-clock captured to a tmpfs directory, mirroring the successful `chunk_2013_partial` pattern (shell `bgzz8eqe5`). Rationale: foreground tool-layer max timeout (≤ 10 min) may not cover the chunk's runtime; background avoids tool-layer-kill-while-subprocess-continues orphaning; same-session, not off-session. The actual `chunk_2013_partial` runtime was ~8 min 20 s for 275 URLs (~1.8 s/URL); a 361-URL `chunk_2014` is plausibly ~10–12 min at the same rate, which still motivates background execution as the safer default. **This calibration is record-only and does not weaken the no-retry / exactly-once / no-off-session rules.**
- **Output-directory timestamping** — runner-controlled via `chunk_2014_<UTC_TIMESTAMP>/`. The future prompt must not pre-commit to a specific timestamp; collision detection is handled by the runner's `os.makedirs(..., exist_ok=False)`.
- **Substrate-gap diagnostic surfacing** — the four 2014 substrate gaps must surface in `chunk_metadata.json`'s `substrate_gap_diagnostic` field (not in the manifest itself, which excludes them upstream). The future report must list the four gaps explicitly and confirm none of them appear in any per-URL row count (since no URL exists for these dates).

Precedent citations:

- `0065d10 Decision 3A` — untracked-by-default for per-cycle output artifacts.
- `5962c20 §8.2` — chunk-design memo's untracked-by-default codification.
- `chunk_2013_partial` execution at `065d475` (enable `c6b313c` → restore `167a08a` → report `065d475`) — successful end-to-end demonstration of the three-commit cycle with untracked output.

## Next step

The next step after persistence of this planning memo is **review of the plan**, not execution. The review may be performed read-only by the user or by a separately invoked review-only prompt. If the review surfaces no issues, the next eligible workstream is the **chunk_2014 execution-authorization prompt** itself — a separately initiated prompt that performs the steps in §"Future execution sequence" above.

If the review surfaces issues (e.g., a calibration concern about background execution, or a corrective on the substrate-gap diagnostic surfacing), a corrective revision of this plan would precede the execution-authorization prompt.

**No execution is initiated by this planning memo.** Its persistence scope is complete upon writing the single tracked file at `docs/lane2_gdelt1_full_build_chunk_2014_execution_authorization_plan_v0.1.md`. No staging, commit, or push is authorized by the content of this plan.
