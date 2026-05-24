# Lane 2 GDELT1 chunk_2016 execution report v0.1

## Outcome

**SUCCESS.**

The chunk_2016 live execution completed with `actual_completed_file_count = expected_file_count = 366`; the runner exited normally with exit code `0`; all three success artifacts were produced; the substrate-gap diagnostic matched the canonical post-`f4590eb` shape (four 2014 dates on both surfaces, NOT `[]`); the full-build guard was restored and committed; the runner is byte-identical to `389747e` post-restore; all three prior completed chunks (`chunk_2013_partial`, `chunk_2014`, `chunk_2015`) remain unmodified.

## Pre-run anchor

| Item | Value |
|---|---|
| Starting HEAD = origin/main | `edef49132393931870172c5755adb853ecd3c9a9` (short `edef491`) |
| Ahead / behind at start | `0 / 0` |
| Planning memo path | `docs/lane2_gdelt1_full_build_chunk_2016_execution_authorization_plan_v0.1.md` |
| Planning memo commit anchor | `edef491` (subject: *"Add Lane 2 chunk_2016 execution-authorization plan"*) |
| Runner implementation anchor | `389747e` (byte-identical at preflight and post-restore) |
| Prior execution-report anchors | `065d475` (chunk_2013_partial); `770f982` (chunk_2014); `ed4e74c` (chunk_2015) |
| Recognized-list authority SHA-256 (pre-run) | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` |
| F4 baseline SHA-256 (pre-run) | `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d` / `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c` |
| Memory `MEMORY.md` mtime / size / SHA-256 (pre-run) | May 24 21:06:13 2026 / 155,677 B / `fbb881206b90890695b8794084586b1225f28e8c0cbd2c4981e45cd4d1e24a05` |
| Memory `project_lane2_attention_spike.md` mtime / size / SHA-256 (pre-run) | May 24 21:07:13 2026 / 293,596 B / `99e6df27ea7d3af98a07d15b8cca7b41209871dedae13daf7017c06e58b585be` |
| Target chunk | `chunk_2016` |
| Expected chunk URL count | `366` |
| Expected chunk date range | `2016-01-01` through `2016-12-31` (inclusive; 2016 IS a leap year) |
| Known 2016 substrate gaps | none (KNOWN_SUBSTRATE_GAPS contains only the four 2014 dates) |
| Five-guard pre-run state | all `False` on disk |
| `LANE2_*_AUTHORIZED` env vars pre-run | unset |
| Target post-chunk report pre-run | did not exist |
| `chunk_2016_*` output subdirectory pre-run | did not exist |
| `/tmp/lane2_chunk_2016_run/` pre-run | did not exist |

## Commits

| Step | Subject | Full SHA | Short SHA |
|---|---|---|---|
| Enable | `Enable Lane 2 full-build chunk_2016 run` | `14818204c0b96d3a0f7510aeb070cdcce3344421` | `14818204` (alias `1481820`) |
| Restore | `Restore Lane 2 full-build guard after chunk_2016` | `3fe1b589f96bfb03b417b759a84d3f57882a44a6` | `3fe1b589` (alias `3fe1b58`) |
| Report | `Record Lane 2 chunk_2016 execution report` | (this commit; full SHA recorded post-stage) | — |

Each guard-flip commit touched exactly one file (`scripts/run_lane2_gdelt1_full_daily_count_build.py:95`) with numstat `1\t1`. Enable: `False → True`. Restore: `True → False`. Runner byte-identical to `389747e` post-restore (`git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py` returns exit 0).

## Live execution

Exact command (inline `LANE2_FULL_BUILD_AUTHORIZED=1`, no `export`, no other `LANE2_*_AUTHORIZED` env var, scoped to the single command):

```
LANE2_FULL_BUILD_AUTHORIZED=1 python3 scripts/run_lane2_gdelt1_full_daily_count_build.py --authorize-full-build-run --chunk-id chunk_2016
```

| Field | Value |
|---|---|
| Execution strategy | Same-session in-session background execution via Bash tool `run_in_background=true`. Same-session, **not** off-session. Mirrors the proven `chunk_2013_partial` `bgzz8eqe5`, `chunk_2014` `blywiekhg`, and `chunk_2015` `bnb2fqhzw` patterns. |
| Harness shell ID | `bikkl185t` |
| Capture path | `/tmp/lane2_chunk_2016_run/` (stdout.log / stderr.log / exit_code.txt / start_utc.txt / end_utc.txt) |
| Wrapper start UTC | `2026-05-24T19:44:35Z` |
| Wrapper end UTC | `2026-05-24T20:03:09Z` |
| Runner-recorded start UTC | `2026-05-24T19:44:35.964301+00:00` |
| Runner-recorded finish UTC | `2026-05-24T20:03:09.491233+00:00` |
| Subprocess state | Normal clean-exit path. Runner exited cleanly via harness completion notification of background shell `bikkl185t` with known exit code `0`. No tool-layer timeout, abort, interruption, or subprocess-state ambiguity. Guard restore performed only after exit code was read. |
| Exit code | `0` |
| Stdout summary | One line: `Chunk chunk_2016 outputs written under: /Users/jay/Documents/GitHub/coherent-numbers/results/lane2_gdelt1_full_daily_count_build/chunk_2016_20260524T194435Z` |
| Stderr summary | Empty |
| Retries / second runs / next-chunk / prior-chunk reruns | None |

## Runtime

| Metric | Value |
|---|---|
| Wrapper elapsed | ~18m 34s (`2026-05-24T19:44:35Z → 2026-05-24T20:03:09Z`) |
| Runner-recorded elapsed | ~18m 33.53s (`2026-05-24T19:44:35.964301+00:00 → 2026-05-24T20:03:09.491233+00:00`) |
| URLs | `366` |
| Per-URL rate | **`~3.04 s/URL`** (1,113.53 s / 366 URLs) |
| Anchor pre-run | `~2.8 s/URL` (conservative, from chunk_2015 closure) |
| Pre-run projection | `366 × 2.8 s/URL ≈ 1,024.8 s ≈ 17m 4.8s ≈ ~17m 5s` (triple-form convention) |
| Actual vs projection | ~1,113.53 s vs ~1,024.8 s — actual ~88.7 s (~8.7%) above the conservative projection |
| Per-URL slowdown vs `chunk_2015` (~2.78 s/URL) | **~+9.4%** (smaller magnitude than prior step's +22%) |
| Per-URL slowdown vs `chunk_2013_partial` (~1.8 s/URL) | ~+69% cumulative |

**Runtime classification per the memory watch-item rule**:

- ~3.04 s/URL is **below** the `≥~3.4 s/URL` bump-trigger. The conservative `~2.8 s/URL` planning anchor is **preserved** for `chunk_2017` planning under the rule's "otherwise" branch.
- ~3.04 s/URL is **not** flatter or improved relative to `chunk_2015` (~2.78 s/URL). The slowdown trend has not been refuted, but its per-step magnitude has decelerated from ~22% (chunk_2014 → chunk_2015) to ~9% (chunk_2015 → chunk_2016).
- The conservative anchor `~2.8 s/URL` was exceeded by ~8.7% on the wall-clock projection, but remains within reasonable range for a "conservative" estimate (i.e., not catastrophically optimistic). The post-`chunk_2016` execution-closure memory update should record this observation and continue using `~2.8 s/URL` as the chunk_2017 conservative anchor unless `chunk_2017` data warrants a revision.

## Output artifacts

Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2016_20260524T194435Z/` — exactly one new chunk_2016 subdirectory created by this run. The output directory remains **untracked by default** per `0065d10` Decision 3A + `5962c20` §8.2 + `chunk_2013_partial` `065d475` + `chunk_2014` `770f982` + `chunk_2015` `ed4e74c` precedent. Not committed.

| File | Size (B) | SHA-256 |
|---|---|---|
| `chunk_contributions.csv` | `36,820` | `91d82561f7296d08e8e134adf59729fb6c82fc2d4d3f11e02112b1a8393c2883` |
| `chunk_metadata.json` | `264,950` | `b933d2f920716684a71a6ec1db7cce482519546c571f3572a53b08c03070b371` |
| `chunk_summary.md` | `420` | `16570ed6a234045f3dc7892d6b5f5c9250220838ba94fdcaf79d402dc15326df` |

No `halt_diagnostic.json`. No raw payload bytes. No `.zip` files. No extracted CSV rows. No final `daily_count.csv` / `build_metadata.json` / `build_summary.md`. No merge artifacts.

`chunk_2016` `chunk_manifest_digest = e03e84ac29045a46ba4d2f207227b6f8f6c1222ba24bafbeefc7e02bd382c7a2` (distinct from the three prior chunks' digests).

## Validation

| Field | Value | Status |
|---|---|---|
| `chunk_id` | `chunk_2016` | ✓ |
| `expected_file_count` | `366` | ✓ |
| `actual_completed_file_count` | `366` | ✓ |
| `actual == expected` | `366 == 366` | ✓ |
| Date range (recorded indirectly via canonical chunk-list entry) | `2016-01-01..2016-12-31` (inclusive) | ✓ |
| `chunk_manifest_digest` | `e03e84ac29045a46ba4d2f207227b6f8f6c1222ba24bafbeefc7e02bd382c7a2` | ✓ |
| `source_recognized_list_sha256` | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` | ✓ matches recognized-list authority |
| `no_retry_confirmation` | `True` | ✓ |
| `boundary_declarations` (all 9 True) | `no_2023plus_access`, `no_asset_or_return_logic`, `no_category_theme_actor_filtering`, `no_market_calendar_alignment`, `no_market_data`, `no_negative_control`, `no_payload_preservation_after_parsing`, `no_spike_threshold_tuning`, `no_step_2` | ✓ all True |
| Substrate-gap diagnostic (both surfaces) | `["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]` on both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` | ✓ canonical post-`f4590eb` shape (NOT `[] / []`) |
| Halt diagnostic present | no | ✓ |
| Raw payload bytes | none | ✓ |
| `.zip` files | none | ✓ |
| Extracted CSV rows | none | ✓ |
| Merge artifacts | none | ✓ |
| Output dir untracked by default | yes | ✓ |
| Five guards `False` post-restore | yes | ✓ |
| `LANE2_*_AUTHORIZED` envs unset post-run | yes | ✓ |
| Runner byte-identical to `389747e` post-restore | yes (exit 0) | ✓ |

Chunk-summary aggregates (from `chunk_summary.md`):

- `total_in_window_rows`: `73,372,638`
- `total_out_of_window_rows`: `13,060`
- `per_offset_total`: `{-3650:13060, -365:730911, -30:405125, -7:684555, -1:448996, 0:71103051, 1:0}`

## Substrate-gap diagnostic

Carrying forward the load-bearing canonical shape from the `f4590eb` planning correction and the empirically validated `chunk_2015` run at `ed4e74c`.

**Distinction**: `chunk_2016` has **zero in-range 2016 substrate gaps** — the KNOWN_SUBSTRATE_GAPS at runner lines 126–129 are all 2014 dates that fall outside `chunk_2016`'s `2016-01-01..2016-12-31` range. **Yet the runner unconditionally surfaces the global `KNOWN_SUBSTRATE_GAPS` tuple to both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched`** (runner lines 1349–1351 halt-path, 2011–2013 success-path). It is **not** a per-chunk intersection. This is the canonical post-`f4590eb` shape.

**Expected** (canonical):

```
known_substrate_gap_dates       = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
substrate_gap_dates_not_fetched = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
```

**Observed in `chunk_2016` `chunk_metadata.json`** (read-only):

```
known_substrate_gap_dates       = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
substrate_gap_dates_not_fetched = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
```

**Both surfaces matched exactly the canonical four-date list in the exact expected order.** This is the corrected expected shape, **not** `[]` / `[]`. No `OUTPUT VERIFICATION FAILURE / SUBSTRATE GAP DIAGNOSTIC MISMATCH` was triggered. This is the second empirical confirmation (after `chunk_2015`) that the `f4590eb` correction holds across consecutive zero-in-range-gap chunks.

## Prior chunk continuity

Verified at all four required checkpoints: preflight, post-run, after report creation, final post-push. The preflight + post-run + after-report-creation checks are recorded below; the final post-push checkpoint is appended in a subsequent verification step.

### `chunk_2013_partial`

- Tracked report: `docs/lane2_gdelt1_full_build_chunk_2013_partial_execution_report_v0.1.md` (commit `065d4754f69e2c35eef1ebdb7e4bf960ca9e806b`) — tracked and unmodified.
- Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2013_partial_20260524T135157Z/` — present and untracked.
- `chunk_contributions.csv`: 17,642 B / SHA-256 `9f07c8018c322027841dbf6484f19c2218d2945731e775b9ced03099cfa37247` — unchanged.
- `chunk_metadata.json`: 214,857 B / SHA-256 `14a407a49e53f660a581bcdc7cee224e3228046aa1ea51eaae5e7eb5dc8a03c1` — unchanged.
- `chunk_summary.md`: 440 B / SHA-256 `9e88e95cc33e4f99ddc3a810db23cd076ac51928d7504b7bab35780d5d15ed42` — unchanged.
- `chunk_manifest_digest`: `6ac92439455d3f59df64cfeca6256f54a319c0ac82d40886f11b26becbfc8b43` — unchanged.

### `chunk_2014`

- Tracked report: `docs/lane2_gdelt1_full_build_chunk_2014_execution_report_v0.1.md` (commit `770f982afdf736575a8bdfdd1b8ef57c4fc6f578`) — tracked and unmodified.
- Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2014_20260524T150055Z/` — present and untracked.
- `chunk_contributions.csv`: 32,908 B / SHA-256 `2ffd56fbd039ef5e7825c048358d7dc0a0b1e6f24d3d8614902de6217ce43660` — unchanged.
- `chunk_metadata.json`: 265,975 B / SHA-256 `e0a944e38204d3fa6deb904d1b71b1a465a284c8203d75c025df372c80fd69d6` — unchanged.
- `chunk_summary.md`: 424 B / SHA-256 `93db53b075e0e15bf1e91d5a4b41a75eb03695925aa5ff0e8a7ceae5c5c3459d` — unchanged.
- `chunk_manifest_digest`: `93f9709656cb30252e1a9e5a8167dadb17b4f63bbb58ac6e4f4405b593994aba` — unchanged.

### `chunk_2015`

- Tracked report: `docs/lane2_gdelt1_full_build_chunk_2015_execution_report_v0.1.md` (commit `ed4e74cc1a7b19d425dd474371b936491d38a056`) — tracked and unmodified.
- Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2015_20260524T163556Z/` — present and untracked.
- `chunk_contributions.csv`: 36,820 B / SHA-256 `7f7307be58e450190db5925cbc69861b95a827bbf279598a9eccecf549301ea2` — unchanged.
- `chunk_metadata.json`: 264,289 B / SHA-256 `a73d5a252610c8610d22d579cbef18e8a58338a7985dac56d9f4d1fe5158d4e2` — unchanged.
- `chunk_summary.md`: 424 B / SHA-256 `2de7dd3595d340d31c27993e416204050c1734dfd4d6ebd137f21c7135d5b2f9` — unchanged.
- `chunk_manifest_digest`: `a5c61b06dee77a9916db6725cabe3a41d74d47d5807dce6ca2be1709bf17bd67` — unchanged.

All nine prior artifact SHAs unchanged; all three prior `chunk_manifest_digest` values unchanged; all three tracked reports unchanged at their committed states. **Continuity envelope intact across all completed chunks.**

## Guard state

All five guards confirmed `False` on disk after the restore commit `3fe1b589`:

| Guard | File:line | Value |
|---|---|---|
| `REAL_RETRIEVAL_ENABLED` | `src/lane2_gdelt1_count_feasibility.py:647` | `False` |
| `COUNT_FEASIBILITY_AUTHORIZED` | `scripts/run_lane2_gdelt1_count_feasibility.py:49` | `False` |
| `EVENT_FILE_PROBE_AUTHORIZED` | `scripts/run_lane2_gdelt1_event_file_probe.py:52` | `False` |
| `ROW_DATE_CHARACTERIZATION_AUTHORIZED` | `scripts/run_lane2_gdelt1_row_date_characterization.py:57` | `False` |
| `FULL_BUILD_AUTHORIZED` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95` | `False` |

Shell envs `LANE2_*_AUTHORIZED` unset post-restore (`printenv | grep -E '^LANE2_.*_AUTHORIZED'` empty). Runner byte-identical to `389747e` post-restore (empty `git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py`).

## Boundary checks

| Check | Status |
|---|---|
| No retry of the live runner | yes |
| No rerun of `chunk_2016` | yes |
| No rerun of any prior chunk | yes |
| No next chunk (`chunk_2017`+) run | yes |
| No merge run | yes |
| No Step 2 | yes |
| No market data | yes |
| No market-data logic / instrument construction | yes |
| No output artifacts committed | yes |
| No raw payload preservation | yes |
| No `.zip` / extracted CSV preservation | yes |
| No checkpoint / resume | yes |
| No off-session execution (background was same-session) | yes |
| No bounded parallelism | yes |
| No recognized-list mutation (`84ea721e…fff835fc` preserved) | yes |
| No F4 mutation (`41c80c0…624c39d` / `00ce9b2…f5e37552c` preserved) | yes |
| No memory edits (`MEMORY.md` and `project_lane2_attention_spike.md` mtimes/sizes/SHA-256 unchanged) | yes |
| No docs edits except this report | yes |
| No code edits except the enable/restore guard flips | yes |
| No test edits | yes |
| No config edits | yes |
| No tests run | yes |
| No GDELT contact except the one authorized live command | yes |
| No `curl` / `wget` / browser / manual fetch | yes |
| No `LANE2_*_AUTHORIZED` env vars exported (inline-env only) | yes |
| No 2023+ posture change | yes |
| Exactly-once fetch semantics preserved | yes |
| No force push | yes |
| No tag push | yes |
| No other-branch push | yes |
| All three prior completed chunk artifacts and reports unmodified | yes (nine SHAs + three digests + three reports re-verified) |

## Substrate progress

| Metric | Before | After (this cycle) |
|---|---|---|
| Chunks complete | 3 / 10 | **4 / 10** |
| Completed chunks list | `chunk_2013_partial`, `chunk_2014`, `chunk_2015` | `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, `chunk_2016` |
| Daily URLs complete | 1,001 / 3,558 | **1,367 / 3,558** (= 1,001 + 366) |
| Percent complete by URL count | ~28.1% | ~**38.4%** |
| Remaining daily URLs | 2,557 | **2,191** |
| Remaining chunks | 7 | **6** (`chunk_2017` through `chunk_2022`) |

Merge remains blocked until 10/10 chunks succeed per `5962c20` §9.1.2.

## Next step

A separately authorized **chunk_2016 execution-closure memory update prompt** is the next step — recording the new HEAD (final report-commit SHA after push), the three-commit chain (`14818204` → `3fe1b589` → report-SHA), the new chunk_2016 output artifact SHAs and `chunk_manifest_digest e03e84ac…382c7a2`, the runtime calibration observation (~3.04 s/URL preserves the ~2.8 s/URL anchor under the "otherwise" branch of the watch-item rule), advancing substrate progress to **4 of 10 chunks** complete (**1,367 of 3,558 daily URLs**, ~38.4%), and superseding the prior "⏸️ Next frontier — chunk_2016 live execution-authorization prompt" bullet with a ✅ execution-closure bullet plus a new ⏸️ frontier pointing to **chunk_2017 planning**.

This is **not** chunk_2017 execution, **not** merge, **not** Step 2, **not** market data. Merge remains blocked until 10/10 chunks succeed. Do not initiate the memory update prompt without explicit user authorization.
