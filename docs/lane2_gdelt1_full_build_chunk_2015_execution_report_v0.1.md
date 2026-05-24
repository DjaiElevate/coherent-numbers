# Lane 2 GDELT1 chunk_2015 execution report v0.1

## Outcome

**SUCCESS.**

The chunk_2015 live execution completed with `actual_completed_file_count = expected_file_count = 365`; the runner exited normally with exit code `0`; all three success artifacts were produced; the substrate-gap diagnostic matched the **corrected** canonical expected shape (four 2014 dates on both surfaces, NOT `[]`); the full-build guard was restored and committed; the runner is byte-identical to `389747e` post-restore; both prior completed chunks (`chunk_2013_partial`, `chunk_2014`) remain unmodified.

## Commits

| Step | Subject | Full SHA | Short SHA |
|---|---|---|---|
| Enable | `Enable Lane 2 full-build chunk_2015 run` | `14c2f6b05d2696f87923bea30dd960ca1e0bce41` | `14c2f6b` |
| Restore | `Restore Lane 2 full-build guard after chunk_2015` | `083649b675b2352c7059731ebb2131c82492cb37` | `083649b` |
| Report | `Record Lane 2 chunk_2015 execution report` | (this commit; full SHA recorded post-stage) | — |

Each guard-flip commit changed exactly one file (`scripts/run_lane2_gdelt1_full_daily_count_build.py`) with numstat `1\t1`. Enable: `False → True` at line 95. Restore: `True → False` at line 95. After restore, `git diff 389747e HEAD -- scripts/run_lane2_gdelt1_full_daily_count_build.py` is empty (runner byte-identical to `389747e`).

## Planning authority

- Planning memo commit: `f4590eb884d4e5b9c3d194890403dbc4b9b07559` (short `f4590eb`).
- Planning memo path: `docs/lane2_gdelt1_full_build_chunk_2015_execution_authorization_plan_v0.1.md`.
- Planning memo review verdict: **`PASS — PLAN CONFORMANT WITH NON-BLOCKING NOTES`** (one non-blocking presentation note only — "locked-memo edit" vs "locked-commit edits" grouping, protective effect preserved either way; not corrected in this cycle).

## Live command

Exact command (inline `LANE2_FULL_BUILD_AUTHORIZED=1`, no `export`, no other `LANE2_*_AUTHORIZED` env var):

```
LANE2_FULL_BUILD_AUTHORIZED=1 python3 scripts/run_lane2_gdelt1_full_daily_count_build.py --authorize-full-build-run --chunk-id chunk_2015
```

| Field | Value |
|---|---|
| Execution mode | Same-session in-session background execution via Bash tool `run_in_background=true`. Same-session, **not** off-session. Mirrors the proven `chunk_2013_partial` (`bgzz8eqe5`) and `chunk_2014` (`blywiekhg`) patterns. |
| Harness shell ID | `bnb2fqhzw` |
| Capture path | `/tmp/lane2_chunk_2015_run/` (stdout.log / stderr.log / exit_code.txt / start_utc.txt / end_utc.txt) |
| Wrapper start UTC | `2026-05-24T16:35:56Z` |
| Wrapper end UTC | `2026-05-24T16:52:50Z` |
| Runner-recorded start UTC | `2026-05-24T16:35:56.432986+00:00` |
| Runner-recorded finish UTC | `2026-05-24T16:52:50.552506+00:00` |
| Elapsed (runner-recorded) | ~`16m 54.12s` |
| Per-URL rate | `~2.78 s/URL` × 365 URLs (above the ~2.3 s/URL conservative anchor; see runtime calibration note below) |
| Exit code | `0` |
| Stdout summary | One line: `Chunk chunk_2015 outputs written under: /Users/jay/Documents/GitHub/coherent-numbers/results/lane2_gdelt1_full_daily_count_build/chunk_2015_20260524T163556Z` |
| Stderr summary | Empty |
| Harness completion notification | Background shell `bnb2fqhzw` reported `status: completed; exit code 0` |
| Retries / second runs / next-chunk / prior-chunk reruns | None |

## Subprocess state

Not applicable — normal clean-exit path. The runner subprocess exited cleanly via harness completion notification of background shell `bnb2fqhzw` with known exit code `0`. No tool-layer timeout, abort, interruption, or subprocess-state ambiguity. Guard restore was performed only after the exit code was read.

## Output artifacts

Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2015_20260524T163556Z/` — exactly one new chunk_2015 subdirectory created by this run. The output directory remains **untracked by default** per `0065d10` Decision 3A + `5962c20` §8.2 + `chunk_2013_partial` `065d475` + `chunk_2014` `770f982` precedent. Not committed.

| File | Size (B) | SHA-256 |
|---|---|---|
| `chunk_contributions.csv` | `36,820` | `7f7307be58e450190db5925cbc69861b95a827bbf279598a9eccecf549301ea2` |
| `chunk_metadata.json` | `264,289` | `a73d5a252610c8610d22d579cbef18e8a58338a7985dac56d9f4d1fe5158d4e2` |
| `chunk_summary.md` | `424` | `2de7dd3595d340d31c27993e416204050c1734dfd4d6ebd137f21c7135d5b2f9` |

No `halt_diagnostic.json`. No raw payload bytes. No `.zip` files. No extracted CSV rows. No final `daily_count.csv` / `build_metadata.json` / `build_summary.md`. No merge artifacts. No tracked full-build execution report beyond this per-chunk report.

## Validation facts

| Field | Value |
|---|---|
| `chunk_id` | `chunk_2015` |
| `expected_file_count` | `365` |
| `actual_completed_file_count` | `365` |
| `actual_completed_file_count == expected_file_count` | **yes** |
| Date range | `2015-01-01` through `2015-12-31` (inclusive) |
| `chunk_manifest_digest` | `a5c61b06dee77a9916db6725cabe3a41d74d47d5807dce6ca2be1709bf17bd67` |
| `source_recognized_list_sha256` | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` |
| `no_retry_confirmation` | `True` |
| `boundary_declarations` (all `True`) | `no_2023plus_access`, `no_asset_or_return_logic`, `no_category_theme_actor_filtering`, `no_market_calendar_alignment`, `no_market_data`, `no_negative_control`, `no_payload_preservation_after_parsing`, `no_spike_threshold_tuning`, `no_step_2` |
| Chunk-summary aggregates | `total_in_window_rows = 66,357,922`; `total_out_of_window_rows = 12,897`; `per_offset_total = {-3650:12897, -365:815596, -30:395422, -7:651860, -1:427065, 0:64056015, 1:11964}` |

## Substrate-gap diagnostic

This is the load-bearing check carried forward from the chunk_2015 planning memo at `f4590eb` and the subsequent planning-closure memory update.

There are **zero in-range 2015 substrate gaps** (the four `KNOWN_SUBSTRATE_GAPS` entries at runner lines 126–129 are all 2014 dates that fall outside chunk_2015's `2015-01-01..2015-12-31` range). However, the runner **unconditionally** writes the global `KNOWN_SUBSTRATE_GAPS` tuple to both diagnostic surfaces (runner lines 1349–1351 halt-path and 2011–2013 success-path); it is **not** a per-chunk intersection. The corrected canonical expected success-path shape is therefore the four 2014 dates on both surfaces, **not** `[]` / `[]`.

**Corrected expected shape (canonical after `f4590eb`):**

```
known_substrate_gap_dates       = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
substrate_gap_dates_not_fetched = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
```

**Observed shape in `chunk_2015` `chunk_metadata.json`:**

```
known_substrate_gap_dates       = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
substrate_gap_dates_not_fetched = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
```

**Both surfaces matched exactly the corrected four-date list in the exact expected order.** This is the corrected expected shape, **not** `[]` / `[]`. Zero in-range 2015 gaps is distinct from the global diagnostic output shape — the runner surfaces the global `KNOWN_SUBSTRATE_GAPS` regardless of which chunk runs. No `OUTPUT VERIFICATION FAILURE / SUBSTRATE GAP DIAGNOSTIC MISMATCH` condition was triggered.

## Prior chunk continuity

Verified at all four required checkpoints (preflight; post-run; after report creation; final post-push) — preflight + post-run + after-report-creation confirmed below; the final post-push checkpoint is recorded after `git push` later in this cycle.

### `chunk_2013_partial`

- Tracked report: `docs/lane2_gdelt1_full_build_chunk_2013_partial_execution_report_v0.1.md` (commit `065d4754f69e2c35eef1ebdb7e4bf960ca9e806b` / short `065d475`) — remains tracked and unmodified.
- Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2013_partial_20260524T135157Z/` — remains present and untracked.
- `chunk_contributions.csv`: 17,642 B / SHA-256 `9f07c8018c322027841dbf6484f19c2218d2945731e775b9ced03099cfa37247` — unchanged.
- `chunk_metadata.json`: 214,857 B / SHA-256 `14a407a49e53f660a581bcdc7cee224e3228046aa1ea51eaae5e7eb5dc8a03c1` — unchanged.
- `chunk_summary.md`: 440 B / SHA-256 `9e88e95cc33e4f99ddc3a810db23cd076ac51928d7504b7bab35780d5d15ed42` — unchanged.

### `chunk_2014`

- Tracked report: `docs/lane2_gdelt1_full_build_chunk_2014_execution_report_v0.1.md` (commit `770f982afdf736575a8bdfdd1b8ef57c4fc6f578` / short `770f982`) — remains tracked and unmodified.
- Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2014_20260524T150055Z/` — remains present and untracked.
- `chunk_contributions.csv`: 32,908 B / SHA-256 `2ffd56fbd039ef5e7825c048358d7dc0a0b1e6f24d3d8614902de6217ce43660` — unchanged.
- `chunk_metadata.json`: 265,975 B / SHA-256 `e0a944e38204d3fa6deb904d1b71b1a465a284c8203d75c025df372c80fd69d6` — unchanged.
- `chunk_summary.md`: 424 B / SHA-256 `93db53b075e0e15bf1e91d5a4b41a75eb03695925aa5ff0e8a7ceae5c5c3459d` — unchanged.

## Guard state

All five guards confirmed `False` on disk after the restore commit `083649b`:

| Guard | File:line | Value |
|---|---|---|
| `REAL_RETRIEVAL_ENABLED` | `src/lane2_gdelt1_count_feasibility.py:647` | `False` |
| `COUNT_FEASIBILITY_AUTHORIZED` | `scripts/run_lane2_gdelt1_count_feasibility.py:49` | `False` |
| `EVENT_FILE_PROBE_AUTHORIZED` | `scripts/run_lane2_gdelt1_event_file_probe.py:52` | `False` |
| `ROW_DATE_CHARACTERIZATION_AUTHORIZED` | `scripts/run_lane2_gdelt1_row_date_characterization.py:57` | `False` |
| `FULL_BUILD_AUTHORIZED` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95` | `False` |

Shell envs `LANE2_*_AUTHORIZED` unset (post-restore `env | grep '^LANE2_.*_AUTHORIZED'` is empty). Runner byte-identical to `389747e` post-restore (empty `git diff 389747e HEAD -- scripts/run_lane2_gdelt1_full_daily_count_build.py`).

## Boundary checks

| Check | Status |
|---|---|
| No retry | yes |
| No rerun (chunk_2015) | yes |
| No `chunk_2013_partial` or `chunk_2014` rerun | yes |
| No next chunk (chunk_2016+) run | yes |
| No merge run | yes |
| No Step 2 | yes |
| No market data | yes |
| No market-data logic / instrument construction | yes |
| No output artifacts committed | yes |
| No raw payload preservation | yes |
| No `.zip` / extracted CSV preservation | yes |
| No checkpoint / resume | yes |
| No off-session execution | yes (background was same-session) |
| No bounded parallelism | yes |
| No recognized-list mutation (`84ea721e…fff835fc` preserved) | yes |
| No F4 mutation (`41c80c0…624c39d` / `00ce9b2…f5e37552c` preserved) | yes |
| No memory edits | yes (memory unchanged: `MEMORY.md` `142,474 B / May 24 18:20:13`; `project_lane2_attention_spike.md` `271,402 B / May 24 18:21:36`) |
| No docs edits except this report | yes |
| No code edits except the enable/restore guard flips | yes |
| No test edits | yes |
| No config edits | yes |
| No tests run | yes |
| No GDELT contact except the one authorized live command | yes |
| No `curl` / `wget` / browser / manual fetch | yes |
| No `LANE2_*_AUTHORIZED` env vars exported (inline-env only) | yes |
| No 2023+ posture change | yes |
| No SQLDATE re-keying change | yes |
| Exactly-once fetch semantics preserved | yes |
| No force push | yes |
| No tag push | yes |
| No other-branch push | yes |
| No `chunk_2013_partial` or `chunk_2014` output modified (six prior SHAs preserved) | yes |

## Substrate progress

**3 of 10 chunks complete** (`chunk_2013_partial`, `chunk_2014`, `chunk_2015`); **1,001 of 3,558 daily URLs complete** (`275 + 361 + 365 = 1,001`, ≈ **28.1%** by URL count); 7 chunks remain (`chunk_2016` through `chunk_2022`); 2,557 daily URLs remain. Merge remains blocked until all 10 chunks succeed per `5962c20` §9.1.2.

## Runtime calibration update

| Chunk | URLs | Wall-clock | Per-URL rate |
|---|---|---|---|
| `chunk_2013_partial` | 275 | ~8m 20s | ~1.8 s/URL |
| `chunk_2014` | 361 | ~13m 44s | ~2.28 s/URL |
| `chunk_2015` | 365 | ~16m 54s | **~2.78 s/URL** |

`chunk_2015` ran ~22% slower per URL than `chunk_2014` and ~54% slower than `chunk_2013_partial`. The planning-memo projection was `365 × 2.3 s ≈ 13m 59.5s ≈ ~14m`; the actual was ~16m 54s, ~21% longer than the projection. The `~2.3 s/URL` conservative anchor is no longer conservative. **For future planning, prefer `~2.8 s/URL` as the new conservative anchor unless later evidence supersedes it.** This calibration is record-only and does NOT weaken any of the no-retry / exactly-once / no-off-session / no-market-data / no-Step-2 / no-checkpoint-resume / no-bounded-parallelism rules. Same-session background execution via Bash `run_in_background=true` with harness capture remains the default and is further reinforced — every remaining full-year chunk is now expected to exceed the 10-min Bash foreground tool ceiling by an even larger margin.

## Next step

A separate **chunk_2015 execution-cycle closure memory update prompt** is the next step — recording the new HEAD (final report-commit SHA), the three-commit chain (`14c2f6b` → `083649b` → report), output artifact SHAs, the corrected substrate-gap diagnostic verification, the new `~2.8 s/URL` runtime calibration anchor, advancing substrate progress to 3 of 10 chunks (1,001 of 3,558 URLs), and updating the `chunk_2015` planning-closure frontier to a ✅ execution closure followed by a new ⏸️ frontier pointing to `chunk_2016` planning.

This is **not** chunk_2016 execution, **not** merge, **not** Step 2, **not** market data. Merge remains blocked until 10/10 chunks succeed; Step 2 and market-data work remain blocked until the no-market-data firewall is explicitly retired by a separately authorized memo.
