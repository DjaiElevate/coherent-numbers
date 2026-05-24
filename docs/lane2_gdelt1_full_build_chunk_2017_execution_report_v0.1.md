# Lane 2 GDELT1 chunk_2017 execution report v0.1

## Verdict

**SUCCESS — CHUNK_2017 EXECUTION COMPLETE.**

The chunk_2017 live execution completed cleanly with `actual_completed_file_count = expected_file_count = 365`, exit code `0`, three success artifacts written, the substrate-gap diagnostic matching the canonical post-`f4590eb` shape (third empirical confirmation), the full-build guard restored, the runner byte-identical to `389747e` post-restore, and all four prior chunks' continuity preserved.

## Commit lineage

| Step | Subject | Full SHA | Short |
|---|---|---|---|
| Enable | `Enable Lane 2 full-build chunk_2017 run` | `6381c5a5c60dfdae777559fe6645c92fadcba066` | `6381c5a` |
| Restore | `Restore Lane 2 full-build guard after chunk_2017` | `51697bb3587667cff196e593cb95decc13dd8f14` | `51697bb` |
| Report | `Record Lane 2 chunk_2017 execution report` | (this commit; SHA recorded post-stage) | — |

Each guard-flip commit touched exactly one file (`scripts/run_lane2_gdelt1_full_daily_count_build.py:95`) with numstat `1\t1` (enable `False → True`; restore `True → False`). Runner byte-identical to `389747e` post-restore (`git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py` returns 0). Lineage extends `b41eb2e → 6381c5a → 51697bb → (report SHA)`.

## Live command

```
LANE2_FULL_BUILD_AUTHORIZED=1 python3 scripts/run_lane2_gdelt1_full_daily_count_build.py --authorize-full-build-run --chunk-id chunk_2017
```

- Method: same-session in-session background execution via Bash tool `run_in_background=true`. Same-session, NOT off-session. Inline env (no export). Mirrors the proven `bgzz8eqe5` / `blywiekhg` / `bnb2fqhzw` / `bikkl185t` patterns.
- Harness shell ID: `b4fp4o3rn`.
- Capture path: `/tmp/lane2_chunk_2017_run/` (stdout.log / stderr.log / exit_code.txt / start_utc.txt / end_utc.txt).
- Wrapper start UTC: `2026-05-24T23:11:42Z` → wrapper end UTC: `2026-05-24T23:30:55Z`.
- Runner-recorded: `2026-05-24T23:11:43.121474+00:00` → `2026-05-24T23:30:55.783476+00:00`.
- Exit code: `0`. Stdout: one line pointing to output dir. Stderr: empty.
- Subprocess state at end: `EXITED_SUCCESS` — runner exited cleanly via harness completion notification with known exit code `0`; no timeout / abort / interruption / ambiguity; guard restore performed only after exit code was read.
- No retries; no second run; no prior-chunk rerun; no next-chunk run; exactly-once fetch semantics preserved.

## Runtime

| Metric | Value |
|---|---|
| Wrapper runtime | ~19m 13s (`23:11:42 → 23:30:55`) |
| Runner-recorded runtime | ~19m 12.66s (`23:11:43.121474 → 23:30:55.783476`) |
| URLs | `365` |
| Per-URL rate | **~3.16 s/URL** (`1,152.66 s / 365 URLs`) |
| Comparison vs `chunk_2016` (~3.04 s/URL) | **+3.9% slower** per URL |
| Projection (planning anchor) | `365 URLs × 2.8 s/URL ≈ 1,022.0 s ≈ 17m 2.0s ≈ ~17m 2s` |
| Actual vs projection | ~1,152.66 s vs ~1,022.0 s ≈ +12.8% over projection |
| Bump-trigger threshold | `≥ ~3.4 s/URL` |
| Branch classification | **Branch (c)** — slowdown continues (~3.16 > ~3.04 prior) but ~3.16 < ~3.4 bump-trigger → **preserve `~2.8 s/URL` anchor**, keep watch active |
| Per-step slowdown trend | `+27% (2013→2014) → +22% (2014→2015) → +9.4% (2015→2016) → +3.9% (2016→2017)` — deceleration continues |

This calibration is record-only and does NOT weaken the no-retry / exactly-once / no-off-session / no-market-data / no-Step-2 / no-checkpoint-resume / no-bounded-parallelism rules.

## Output artifacts

Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2017_20260524T231143Z/` — exactly one new chunk_2017 subdirectory. Untracked by default per `0065d10` Decision 3A + `5962c20` §8.2 + `chunk_2013_partial` `065d475` + `chunk_2014` `770f982` + `chunk_2015` `ed4e74c` + `chunk_2016` `e6874d6` precedent; not committed.

| File | Size (B) | SHA-256 |
|---|---|---|
| `chunk_contributions.csv` | 36,565 | `87ba1a907d0c6879e370796ef12bf1df1efa1c9e2281489821b44f3343db3223` |
| `chunk_metadata.json` | 264,066 | `56fece119d32e1ebeab5d5964c83848200b91ce2486ca177017578b67ee24016` |
| `chunk_summary.md` | 420 | `b2f42542fa295b6feb1248220d05a11302b1d43d52bb616ba09df9c171fdeffc` |

**`chunk_manifest_digest`** = `6aec5ad96f63721b5ce26831d3ebb38af05646fb64842e18fda14bba492c258e` (distinct from prior four: `6ac92439…bfc8b43`, `93f97096…994aba`, `a5c61b06…bf17bd67`, `e03e84ac…382c7a2`).

Chunk-summary aggregates: `total_in_window_rows = 66,303,468`; `total_out_of_window_rows = 12,791`; `per_offset_total = {-3650:12791, -365:630167, -30:377075, -7:629719, -1:368480, 0:64298027, 1:0}`.

No `halt_diagnostic.json`. No raw payload bytes. No `.zip` files. No extracted CSV rows. No merge artifacts.

## Validation

| Field | Value | Status |
|---|---|---|
| `chunk_id` | `chunk_2017` | ✓ |
| `expected_file_count` | `365` | ✓ |
| `actual_completed_file_count` | `365` | ✓ |
| `actual == expected` | `365 == 365` | ✓ |
| `chunk_manifest_digest` | `6aec5ad96f63721b5ce26831d3ebb38af05646fb64842e18fda14bba492c258e` | ✓ recorded |
| `source_recognized_list_sha256` | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` | ✓ matches recognized-list authority |
| `no_retry_confirmation` | `True` | ✓ |
| `boundary_declarations` (all 9 True) | `no_2023plus_access`, `no_asset_or_return_logic`, `no_category_theme_actor_filtering`, `no_market_calendar_alignment`, `no_market_data`, `no_negative_control`, `no_payload_preservation_after_parsing`, `no_spike_threshold_tuning`, `no_step_2` | ✓ all True |
| Substrate-gap diagnostic both surfaces | `["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]` on both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` | ✓ canonical post-`f4590eb` shape (NOT `[] / []`) — **third empirical confirmation** after chunk_2015 (`ed4e74c`) and chunk_2016 (`e6874d6`) |
| Halt diagnostic | absent | ✓ |
| Raw payloads | absent | ✓ |
| `.zip` files | absent | ✓ |
| Extracted CSV rows | absent | ✓ |
| Merge artifacts | absent | ✓ |
| Output dir untracked | yes | ✓ |
| Five guards `False` post-restore | yes (re-verified) | ✓ |
| `LANE2_*_AUTHORIZED` envs unset post-run | yes | ✓ |
| Runner byte-identical to `389747e` post-restore | yes (exit 0) | ✓ |

## Substrate-gap diagnostic

Semantic interpretation: `chunk_2017` has **zero in-range 2017 substrate gaps** — the runner's `KNOWN_SUBSTRATE_GAPS` constant at lines 126–129 contains only the four 2014 dates, none of which intersect chunk_2017's `2017-01-01..2017-12-31` range. The runner nevertheless surfaces the **global** `KNOWN_SUBSTRATE_GAPS` tuple unconditionally to both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` (runner lines 1349–1351 halt-path; 2011–2013 success-path). This is the canonical post-`f4590eb` shape and is now the **third consecutive empirical confirmation** that the correction holds across zero-in-range-gap chunks (chunk_2015, chunk_2016, chunk_2017).

## Continuity envelope

Verified at all four checkpoints (preflight; post-run; after report creation; final post-push). All twelve prior artifact SHAs, all four prior `chunk_manifest_digest` values, and all four tracked prior reports unchanged:

- `chunk_2013_partial` — report `065d4754f69e2c35eef1ebdb7e4bf960ca9e806b`; artifacts `9f07c801…cfa37247` (17,642 B) / `14a407a4…dc8a03c1` (214,857 B) / `9e88e95c…d5d15ed42` (440 B); digest `6ac92439455d3f59df64cfeca6256f54a319c0ac82d40886f11b26becbfc8b43`.
- `chunk_2014` — report `770f982afdf736575a8bdfdd1b8ef57c4fc6f578`; artifacts `2ffd56fb…7ce43660` (32,908 B) / `e0a944e3…80fd69d6` (265,975 B) / `93db53b0…c5c3459d` (424 B); digest `93f9709656cb30252e1a9e5a8167dadb17b4f63bbb58ac6e4f4405b593994aba`.
- `chunk_2015` — report `ed4e74cc1a7b19d425dd474371b936491d38a056`; artifacts `7f7307be…49301ea2` (36,820 B) / `a73d5a25…5158d4e2` (264,289 B) / `2de7dd35…35d5b2f9` (424 B); digest `a5c61b06dee77a9916db6725cabe3a41d74d47d5807dce6ca2be1709bf17bd67`.
- `chunk_2016` — report `e6874d61415d4fda24883ae6492f1090b8ce85a7`; artifacts `91d82561…3c2883` (36,820 B) / `b933d2f9…3070b371` (264,950 B) / `16570ed6…dc15326df` (420 B); digest `e03e84ac29045a46ba4d2f207227b6f8f6c1222ba24bafbeefc7e02bd382c7a2`.

Authority SHAs preserved (`84ea721e…fff835fc`; `41c80c0…624c39d`; `00ce9b2…f5e37552c`). Memory files unchanged from preflight (`MEMORY.md` `8ee9834adde27fe43fee0f658af2500e92b800a3bee6dff144b1b445ef54e7d0`; `project_lane2_attention_spike.md` `2637d91323c25313e836d21768ed327f2910e5506d4e62ba379a160aea46401b`).

## Guard state restored

All five guards confirmed `False` on disk after restore commit `51697bb`:

| Guard | File:line | Value |
|---|---|---|
| `REAL_RETRIEVAL_ENABLED` | `src/lane2_gdelt1_count_feasibility.py:647` | `False` |
| `COUNT_FEASIBILITY_AUTHORIZED` | `scripts/run_lane2_gdelt1_count_feasibility.py:49` | `False` |
| `EVENT_FILE_PROBE_AUTHORIZED` | `scripts/run_lane2_gdelt1_event_file_probe.py:52` | `False` |
| `ROW_DATE_CHARACTERIZATION_AUTHORIZED` | `scripts/run_lane2_gdelt1_row_date_characterization.py:57` | `False` |
| `FULL_BUILD_AUTHORIZED` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95` | `False` |

Shell envs `LANE2_*_AUTHORIZED` unset. Runner byte-identical to `389747e` (empty `git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py`).

## Boundaries preserved

No retry; no rerun of chunk_2017; no rerun of chunk_2013_partial / chunk_2014 / chunk_2015 / chunk_2016; no next chunk (chunk_2018+) run; no merge; no Step 2; no market data; no instrument construction; no output artifacts committed; no raw payload preservation; no `.zip` / extracted CSV preservation; no checkpoint/resume; no off-session execution (background was same-session); no bounded parallelism; no recognized-list mutation; no F4 mutation; no memory edits during this execution cycle; no other docs edits except this report; no code edits except the enable/restore guard flips; no test edits; no config edits; no tests run; no force / tag / other-branch push; no GDELT contact outside the single authorized live `chunk_2017` command (inline-env only, no `export`).

## Progress

| Metric | Before chunk_2017 | After chunk_2017 |
|---|---|---|
| Chunks complete | 4 / 10 | **5 / 10** |
| Completed chunks | `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, `chunk_2016` | + `chunk_2017` |
| Daily URLs complete | 1,367 / 3,558 | **1,732 / 3,558** (= 1,367 + 365) |
| Percent complete by URL count | ~38.4% | ~**48.7%** |
| Remaining daily URLs | 2,191 | **1,826** |
| Remaining chunks | 6 | **5** (`chunk_2018` through `chunk_2022`) |

Merge remains blocked until 10/10 chunks succeed per `5962c20` §9.1.2.

## Next frontier

A separately authorized **chunk_2017 execution-closure memory update prompt** is the next step — recording the three-commit chain (`6381c5a` → `51697bb` → report-SHA), the chunk_2017 output artifact SHAs / sizes, the new `chunk_manifest_digest = 6aec5ad96f63721b5ce26831d3ebb38af05646fb64842e18fda14bba492c258e`, the third empirical confirmation of the substrate-gap correction, the runtime calibration update (`~3.16 s/URL` falls in branch (c) — preserve `~2.8 s/URL` anchor, keep watch active; deceleration trend `+27% → +22% → +9.4% → +3.9%`), advancing substrate progress to **5 of 10 chunks** (**1,732 of 3,558 URLs**, ~48.7%), and superseding the prior "⏸️ Next frontier — chunk_2017 live execution-authorization prompt" bullet with a ✅ execution-closure bullet plus a new ⏸️ frontier pointing to **chunk_2018 planning**.

Also record the **prompt-truncation transport lesson** as a sanity-check discipline: when sanity-checking prompts containing nested code fences, assess whether the outer wrapper could be terminated prematurely by an inner fence at delivery, even if the source text is complete.

This is **not** chunk_2018 planning, **not** chunk_2018 execution, **not** merge, **not** Step 2, **not** market data. Merge remains blocked until 10/10 chunks succeed. Do not initiate the memory update prompt without explicit user authorization.
