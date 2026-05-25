# Lane 2 GDELT1 chunk_2018 execution report v0.1

## Verdict

**SUCCESS — CHUNK_2018 EXECUTION COMPLETE.**

The chunk_2018 live execution completed cleanly with `actual_completed_file_count = expected_file_count = 365`, exit code `0`, three success artifacts written, the substrate-gap diagnostic matching the canonical post-`f4590eb` shape (fourth empirical confirmation), the full-build guard restored, the runner byte-identical to `389747e` post-restore, and all five prior chunks' continuity preserved.

## Repo state before execution

HEAD = origin/main = b8d0b2f6485f1bf3235e9c23bd8ec7107383c326 (short `b8d0b2f`); ahead/behind = 0/0; tracked tree clean. HEAD literal written as contiguous prose per the HEAD-literal grep discipline.

## Commit chain

| Step | Subject | Full SHA | Short |
|---|---|---|---|
| Enable | `Enable Lane 2 full-build chunk_2018 run` | `eb83ffa052feeaccc9489e67e08a94646d8d922c` | `eb83ffa` |
| Restore | `Restore Lane 2 full-build guard after chunk_2018` | `ca76177782a0075624ef391c70e2292b91edada5` | `ca76177` |
| Report | `Record Lane 2 chunk_2018 execution report` | (this commit; SHA recorded post-stage) | — |

Each guard-flip commit touched exactly one file (`scripts/run_lane2_gdelt1_full_daily_count_build.py:95`) with numstat `1\t1` (enable `False → True`; restore `True → False`). Runner byte-identical to `389747e` post-restore (`git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py` returns 0). Lineage extends `b8d0b2f → eb83ffa → ca76177 → (report SHA)`.

## Live command

`LANE2_FULL_BUILD_AUTHORIZED=1 python3 scripts/run_lane2_gdelt1_full_daily_count_build.py --authorize-full-build-run --chunk-id chunk_2018`

- Method: same-session in-session background execution via Bash tool `run_in_background=true`. Same-session, NOT off-session. Inline env (no export). Mirrors the proven `bgzz8eqe5` / `blywiekhg` / `bnb2fqhzw` / `bikkl185t` / `b4fp4o3rn` patterns.
- Harness shell ID: `b5mt31qol`.
- Capture path: `/tmp/lane2_chunk_2018_run/` (`stdout.log`, `stderr.log`, `exit_code.txt`, `start_utc.txt`, `end_utc.txt`).
- **Live command was invoked exactly once.** Exactly-once fetch semantics preserved.
- Wrapper window UTC: `2026-05-25T02:56:23Z → 2026-05-25T03:13:05Z`.
- Runner-recorded UTC: `2026-05-25T02:56:41.948549+00:00 → 2026-05-25T03:13:05.220568+00:00`.
- Exit code: `0`. Stdout: one line pointing to the output dir. Stderr: empty.
- Subprocess state at end: `EXITED_SUCCESS` — runner exited cleanly via harness completion notification with known exit code `0`; no timeout / abort / interruption / ambiguity; guard restore performed only after exit code was read.
- No retries; no second run; no prior-chunk rerun; no next-chunk run; no off-session execution; no checkpoint/resume; no bounded parallelism; no raw GDELT payload preservation.

## Runtime

| Metric | Value |
|---|---|
| Wrapper runtime | ~16m 42s (`02:56:23 → 03:13:05`) |
| Runner-recorded runtime | ~16m 23.27s (`02:56:41.948549 → 03:13:05.220568`) |
| URLs | `365` |
| Per-URL rate (runner-recorded) | **~2.69 s/URL** (`983.27 s / 365 URLs`) |
| Per-URL rate (wrapper) | ~2.745 s/URL (`1,002 s / 365 URLs`) |
| Planning anchor projection | `365 URLs × 2.8 s/URL ≈ 1,022.0 s ≈ 17m 2.0s ≈ ~17m 2s` (URLs × s/URL = s) |
| Actual vs projection | ~983.27 s vs ~1,022.0 s ≈ **−3.8% under projection** |
| Comparison vs `chunk_2017` (~3.16 s/URL) | **−14.9%** (improvement) — the per-step trend reverses for the first time |
| Bump-trigger threshold | `≥ ~3.4 s/URL` (ASCII-equivalent: `>= ~3.4 s/URL`) |
| Branch classification | **Branch (b)** — flat/improved vs `chunk_2017` (~2.69 ≤ ~3.16) → **preserve `~2.8 s/URL` anchor as transient improvement**, watch remains active |
| Per-step slowdown trend extension | `+27% → +22% → +9.4% → +3.9% → -14.9%` — deceleration reversed; chunk_2018 actually faster than `chunk_2017` |

This calibration is record-only and does NOT weaken the no-retry / exactly-once / no-off-session / no-market-data / no-Step-2 / no-checkpoint-resume / no-bounded-parallelism rules.

## Expected target

- Expected count: **365 daily URLs**.
- Date range: **2018-01-01** through **2018-12-31** (runner `CHUNK_YEAR_RANGES["chunk_2018"] = (date(2018, 1, 1), date(2018, 12, 31))` at line 1546).

## Output artifacts

Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2018_20260525T025641Z/` — exactly one new chunk_2018 subdirectory. Untracked by default per `0065d10` Decision 3A + `5962c20` §8.2 + `chunk_2013_partial` `065d475` + `chunk_2014` `770f982` + `chunk_2015` `ed4e74c` + `chunk_2016` `e6874d6` + `chunk_2017` `0e5f3f1` precedent; not committed.

Harness capture path: `/tmp/lane2_chunk_2018_run/`.

| File | Size (B) | SHA-256 |
|---|---|---|
| `chunk_contributions.csv` | 36,419 | `87d637fc8ba699f9468c2ce86ad8a397966a537918c68bebe64fffeb0b5fce10` |
| `chunk_metadata.json` | 263,900 | `38b00e10f5e40f363c1dfa4c46f8e3ffa91ef709096a1cc68be43958ac21cd37` |
| `chunk_summary.md` | 420 | `656ee9ce7042e1fb9fda91b4cca76354a8aea854ed84c99ba9dda1eff5bccda4` |

**`chunk_manifest_digest`** = `d53798c99b8be65ca550dc07fd35bc2b5e3a44e5bbde86935be083afa3e4c820` (distinct from prior five: `6ac92439…bfc8b43`, `93f97096…994aba`, `a5c61b06…bf17bd67`, `e03e84ac…382c7a2`, `6aec5ad9…b492c258e`).

Chunk-summary / aggregate-metrics row counts:

- `total_in_window_rows = 61,529,216`
- `total_out_of_window_rows = 11,230`
- `total_parsed_rows = 61,540,446`
- `per_offset_total = {-3650: 11230, -365: 602815, -30: 362581, -7: 582075, -1: 294798, 0: 59686947, 1: 0}`

No `halt_diagnostic.json`. No raw payload bytes. No `.zip` files. No extracted CSV rows. No merge artifacts. Exactly three files in the output directory (matching the per-chunk allow-list).

## Validation

| Field | Value | Status |
|---|---|---|
| `chunk_id` | `chunk_2018` | ✓ |
| `expected_file_count` | `365` | ✓ |
| `actual_completed_file_count` | `365` | ✓ |
| `actual == expected` | `365 == 365` | ✓ |
| `chunk_manifest_digest` | `d53798c99b8be65ca550dc07fd35bc2b5e3a44e5bbde86935be083afa3e4c820` | ✓ recorded |
| `source_recognized_list_sha256` | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` | ✓ matches recognized-list authority |
| `no_retry_confirmation` | `True` | ✓ |
| `boundary_declarations` (all 9 True) | `no_2023plus_access`, `no_asset_or_return_logic`, `no_category_theme_actor_filtering`, `no_market_calendar_alignment`, `no_market_data`, `no_negative_control`, `no_payload_preservation_after_parsing`, `no_spike_threshold_tuning`, `no_step_2` | ✓ all True |
| Substrate-gap diagnostic both surfaces | `["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]` on both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` | ✓ canonical post-`f4590eb` shape (NOT `[]` / `[]`) — **fourth empirical confirmation** after chunk_2015 (`ed4e74c`), chunk_2016 (`e6874d6`), chunk_2017 (`0e5f3f1`) |
| Halt diagnostic | absent | ✓ |
| Raw payloads | absent | ✓ |
| `.zip` files | absent | ✓ |
| Extracted CSV rows | absent | ✓ |
| Merge artifacts | absent | ✓ |
| Output dir untracked | yes | ✓ |
| Five guards `False` post-restore | yes (re-verified) | ✓ |
| `LANE2_*_AUTHORIZED` envs unset post-run | yes | ✓ |
| Runner byte-identical to `389747e` post-restore | yes (exit 0) | ✓ |
| Memory files unchanged | yes (re-verified) | ✓ |

## Substrate-gap diagnostic

Observed:

- `known_substrate_gap_dates = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]`
- `substrate_gap_dates_not_fetched = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]`

NOT `[]` / `[]`.

Semantic interpretation: `chunk_2018` has **zero in-range 2018 substrate gaps** — the runner's `KNOWN_SUBSTRATE_GAPS` constant at lines 125–130 contains only the four 2014 dates, none of which intersect chunk_2018's `2018-01-01..2018-12-31` range. The runner nevertheless surfaces the **global** `KNOWN_SUBSTRATE_GAPS` tuple unconditionally to both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` (runner lines 1349–1351 halt-path; 2011–2013 success-path). This is the canonical post-`f4590eb` shape.

**Fourth empirical validation status**: the observed diagnostic matches the canonical four-date / four-date shape exactly; the substrate-gap correction is now **fourth-empirically-validated** by chunk_2015 + chunk_2016 + chunk_2017 + chunk_2018 across four consecutive zero-in-range-gap chunks.

## Continuity envelope

Verified at all four checkpoints (preflight; post-run; after report creation; final post-push). All fifteen prior artifact SHAs, all five prior `chunk_manifest_digest` values, and all five tracked prior reports unchanged:

- `chunk_2013_partial` — report `065d4754f69e2c35eef1ebdb7e4bf960ca9e806b`; artifacts `9f07c801…cfa37247` (17,642 B) / `14a407a4…dc8a03c1` (214,857 B) / `9e88e95c…d5d15ed42` (440 B); digest `6ac92439455d3f59df64cfeca6256f54a319c0ac82d40886f11b26becbfc8b43`.
- `chunk_2014` — report `770f982afdf736575a8bdfdd1b8ef57c4fc6f578`; artifacts `2ffd56fb…7ce43660` (32,908 B) / `e0a944e3…80fd69d6` (265,975 B) / `93db53b0…c5c3459d` (424 B); digest `93f9709656cb30252e1a9e5a8167dadb17b4f63bbb58ac6e4f4405b593994aba`.
- `chunk_2015` — report `ed4e74cc1a7b19d425dd474371b936491d38a056`; artifacts `7f7307be…49301ea2` (36,820 B) / `a73d5a25…5158d4e2` (264,289 B) / `2de7dd35…35d5b2f9` (424 B); digest `a5c61b06dee77a9916db6725cabe3a41d74d47d5807dce6ca2be1709bf17bd67`.
- `chunk_2016` — report `e6874d61415d4fda24883ae6492f1090b8ce85a7`; artifacts `91d82561…3c2883` (36,820 B) / `b933d2f9…3070b371` (264,950 B) / `16570ed6…dc15326df` (420 B); digest `e03e84ac29045a46ba4d2f207227b6f8f6c1222ba24bafbeefc7e02bd382c7a2`.
- `chunk_2017` — report `0e5f3f11a77319dc0b9b9af906c89df2e585d12e` (tracked execution report SHA-256 `1bc474a184bb1482ca01196d669abcca81c130c8e2ed1bd05064eb75047db0c6`); artifacts `87ba1a90…3343db32` (36,565 B) / `56fece11…6ee24016` (264,066 B) / `b2f42542…9c171fdeffc` (420 B); digest `6aec5ad96f63721b5ce26831d3ebb38af05646fb64842e18fda14bba492c258e`.

Authority SHAs preserved (recognized-list `84ea721e…fff835fc`; F4 baselines `41c80c0…624c39d` and `00ce9b2…f5e37552c`). Memory files unchanged from preflight (`MEMORY.md` SHA `79dbacf52416ae4e7af1c3c6e4c506db828fb2be1652fc2e54743a0c7e321536`; `project_lane2_attention_spike.md` SHA `94b4a35d3e56bf09817d9318645222d4c3dd35dd0b96a765411d47c826d1d31f`).

## Guard state restored

All five guards confirmed `False` on disk after restore commit `ca76177`:

| Guard | File:line | Value |
|---|---|---|
| `REAL_RETRIEVAL_ENABLED` | `src/lane2_gdelt1_count_feasibility.py:647` | `False` |
| `COUNT_FEASIBILITY_AUTHORIZED` | `scripts/run_lane2_gdelt1_count_feasibility.py:49` | `False` |
| `EVENT_FILE_PROBE_AUTHORIZED` | `scripts/run_lane2_gdelt1_event_file_probe.py:52` | `False` |
| `ROW_DATE_CHARACTERIZATION_AUTHORIZED` | `scripts/run_lane2_gdelt1_row_date_characterization.py:57` | `False` |
| `FULL_BUILD_AUTHORIZED` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95` | `False` |

Shell envs `LANE2_*_AUTHORIZED` unset. Runner byte-identical to `389747e` (empty `git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py`).

## Boundary declarations (all 9 true)

| Key | Value |
|---|---|
| `no_retry_after_started_live_run` | `true` |
| `exactly_once_fetch` | `true` |
| `no_off_session_execution` | `true` |
| `no_market_data_access` | `true` |
| `no_step2` | `true` |
| `no_merge` | `true` |
| `no_checkpoint_resume` | `true` |
| `no_bounded_parallelism` | `true` |
| `no_raw_payload_preservation` | `true` |

The above report-level boundary declarations are distinct from (and complementary to) the runner-emitted `boundary_declarations` block in `chunk_metadata.json`, which separately records the nine runner-level invariants (`no_2023plus_access`, `no_asset_or_return_logic`, `no_category_theme_actor_filtering`, `no_market_calendar_alignment`, `no_market_data`, `no_negative_control`, `no_payload_preservation_after_parsing`, `no_spike_threshold_tuning`, `no_step_2`) — all also `True`.

## Boundaries preserved

No retry; no rerun of chunk_2018; no rerun of `chunk_2013_partial` / `chunk_2014` / `chunk_2015` / `chunk_2016` / `chunk_2017`; no next chunk (`chunk_2019+`) run; **chunk_2019+ was not touched**; no merge; no Step 2; no market data; no instrument construction; no output artifacts committed; no raw payload preservation; no `.zip` / extracted CSV preservation; no checkpoint/resume; no off-session execution (background was same-session); no bounded parallelism; no recognized-list mutation; no F4 mutation; **no memory edits during this execution cycle**; no other docs edits except this report; no code edits except the enable/restore guard flips; no test edits; no config edits; no tests run; no force / tag / other-branch push; no hook bypass; no signing override; no GDELT contact outside the single authorized live `chunk_2018` command (inline-env only, no `export`).

**Merge remains blocked until 10/10 chunks succeed** per `5962c20` §9.1.2. **Step 2 remains firewalled** until the no-market-data firewall is explicitly retired by a separately authorized memo.

## Progress

| Metric | Before chunk_2018 | After chunk_2018 |
|---|---|---|
| Chunks complete | 5 / 10 | **6 / 10** |
| Completed chunks | `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, `chunk_2016`, `chunk_2017` | + `chunk_2018` |
| Daily URLs complete | 1,732 / 3,558 | **2,097 / 3,558** (= 1,732 + 365) |
| Percent complete by URL count | ~48.7% | ~**58.9%** |
| Remaining daily URLs | 1,826 | **1,461** |
| Remaining chunks | 5 | **4** (`chunk_2019` through `chunk_2022`) |

## Next frontier

A separately authorized **chunk_2018 execution-closure memory update prompt** is the next step — recording the three-commit chain (`eb83ffa` → `ca76177` → report-SHA), the chunk_2018 output artifact SHAs / sizes, the new `chunk_manifest_digest = d53798c99b8be65ca550dc07fd35bc2b5e3a44e5bbde86935be083afa3e4c820`, the fourth empirical confirmation of the substrate-gap correction (now `chunk_2015` + `chunk_2016` + `chunk_2017` + `chunk_2018`), the runtime calibration update (`~2.69 s/URL` falls in branch (b) — preserve `~2.8 s/URL` anchor as transient improvement, keep watch active; per-step trend extends `+27% → +22% → +9.4% → +3.9% → -14.9%` with chunk_2018 reversing the trend), and advancing substrate progress to **6 of 10 chunks** (**2,097 of 3,558 URLs**, ~58.9%).

This is **not** chunk_2019 planning, **not** chunk_2019 execution, **not** merge, **not** Step 2, **not** market data. Merge remains blocked until 10/10 chunks succeed. Do not initiate the memory update prompt without explicit user authorization.
