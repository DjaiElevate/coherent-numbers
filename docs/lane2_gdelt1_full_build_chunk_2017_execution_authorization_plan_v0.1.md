# Lane 2 GDELT1 chunk_2017 execution-authorization plan v0.1

## Title

`Lane 2 GDELT1 chunk_2017 execution-authorization plan v0.1`

This memo is **planning-only**. It does not by itself execute `chunk_2017`, enable any guard, authorize GDELT contact, authorize merge, authorize Step 2, touch market data, or retire the no-market-data firewall. A separate review of this plan, a separate commit, a separate memory-update prompt for the planning closure, and a separate live-execution-authorization prompt are all still required before any `chunk_2017` execution. Its persistence scope is one tracked file at `docs/lane2_gdelt1_full_build_chunk_2017_execution_authorization_plan_v0.1.md`.

## Purpose / decision

This memo prepares the **future live execution envelope** for `chunk_2017` only — the fifth of 10 yearly fetch-file chunks per the chunk-design memo `5962c20`. It defines the enable / single live run / restore / post-chunk-report sequence in design-level detail, the stop conditions, the expected successful output, the halt output, the boundary statement, the prior-chunk continuity protections for **all four** completed chunks, the runtime calibration, and the substrate-gap diagnostic expectation. It is a **planning artifact for review**, not an execution authorization.

**Decision: `AUTHORIZE LATER`.**

Explicitly, this memo does **not** authorize:

- guard flip on any runner
- live runner invocation
- GDELT contact (no network calls)
- chunk_2017 execution
- chunk_2018+ work (no bundling of subsequent chunks)
- merge
- Step 2
- market-data access
- instrument construction
- commit/push of this plan or any other artifact in this planning-creation turn (the plan's commit is a separately authorized follow-up step)
- retries, checkpoint/resume, off-session execution, bounded parallelism
- re-running `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, or `chunk_2016`

## Current state

**Canonical state at planning creation**: `HEAD = origin/main = e6874d61415d4fda24883ae6492f1090b8ce85a7` (short `e6874d6`); ahead/behind `0 0`; tracked tree clean; four chunks complete; chunk_2017 is next.

| Item | Value |
|---|---|
| `HEAD = origin/main` at planning creation | `e6874d61415d4fda24883ae6492f1090b8ce85a7` |
| Short SHA | `e6874d6` |
| Ahead / behind | `0 / 0` |
| Latest execution-cycle commit chain (closing `chunk_2016`) | enable `1481820` → restore `3fe1b58` → report `e6874d6` |
| Planning-memo commit chain so far | `chunk_2013_partial` plan `447656d` → `chunk_2014` plan `4276b30` → `chunk_2015` plan `f4590eb` → `chunk_2016` plan `edef491` |
| Substrate progress | **4 of 10 chunks complete**; **1,367 of 3,558** daily URLs complete (~**38.4%**); **6** chunks + **2,191 URLs** remaining |
| Completed chunks | `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, `chunk_2016` |
| Next chunk | `chunk_2017` |
| Remaining chunks | `chunk_2017` (365 URLs), `chunk_2018` (365 URLs), `chunk_2019` (365 URLs), `chunk_2020` (366 URLs), `chunk_2021` (365 URLs), `chunk_2022` (365 URLs) |
| Recognized-list authority SHA-256 | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` |
| F4 baselines (preserved) | `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d` / `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c` |
| Locked output window | `[2013-04-01, 2022-12-31]` (`7780a97` §6.8 / no-2023+ posture at `0ddbd51`) |
| Merge gate | blocked until 10/10 chunks succeed per `5962c20` §9.1.2 |
| Step 2 / market-data firewall | active and not retired |

## Target chunk

Verified from the runner at HEAD `e6874d6` (runner byte-identical to `389747e`'s committed version; verified empty `git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py`):

| Item | Value | Source |
|---|---|---|
| Chunk ID | `chunk_2017` | runner canonical chunk list |
| Date range | `2017-01-01` through `2017-12-31` (inclusive) | `CHUNK_DATE_RANGES["chunk_2017"]` at runner line 1545: `(date(2017, 1, 1), date(2017, 12, 31))` |
| Calendar days in range | `365` (2017 is not a leap year) | calendar arithmetic |
| Known 2017 substrate gaps | **none** (`KNOWN_SUBSTRATE_GAPS` at runner lines 125–130 contains only the four 2014 dates `2014-01-23` / `2014-01-24` / `2014-01-25` / `2014-03-19`; none intersect the 2017 range) | runner lines 125–130 |
| Count arithmetic | `365 calendar days − 0 known 2017 substrate gaps = 365` | derived |
| Runner-recorded expected count | `EXPECTED_CHUNK_COUNTS["chunk_2017"] = 365` | runner line 1532 |
| Cross-check | calculated `365` matches runner-recorded `365` — agree | derived |
| Future output directory pattern | `results/lane2_gdelt1_full_daily_count_build/chunk_2017_<UTC>/` | runner convention |
| Future harness capture path | `/tmp/lane2_chunk_2017_run/` | execution convention |

`chunk_2017` is therefore a **zero-2017-gap, full-calendar-year (non-leap), 365-URL chunk** — the third consecutive zero-in-range-gap chunk after `chunk_2015` and `chunk_2016`.

## Runner anchor verification

Exact current line numbers discovered in this turn (HEAD `e6874d6`; runner byte-identical to `389747e`):

| Anchor | File:line | Current content |
|---|---|---|
| Chunk-runner module guard | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95` | `FULL_BUILD_AUTHORIZED = False` |
| Era-cutoff constant | `scripts/run_lane2_gdelt1_full_daily_count_build.py:116` | `SEAL_START = date(2023, 1, 1)` |
| Substrate-gap tuple opening | `scripts/run_lane2_gdelt1_full_daily_count_build.py:125` | `KNOWN_SUBSTRATE_GAPS: Tuple[str, ...] = (` (4-element tuple at lines 126–129, closing `)` at line 130) |
| Substrate-gap tuple date entries | `scripts/run_lane2_gdelt1_full_daily_count_build.py:126–129` | `"2014-01-23"`, `"2014-01-24"`, `"2014-01-25"`, `"2014-03-19"` (in order) |
| Canonical chunk-list entry for `chunk_2017` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1519` | `"chunk_2017",` |
| `EXPECTED_CHUNK_COUNTS["chunk_2017"]` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1532` | `"chunk_2017": 365,` |
| `chunk_2017` date-range tuple | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1545` | `"chunk_2017": (date(2017, 1, 1), date(2017, 12, 31)),` |
| `ALLOWED_CHUNK_OUTPUT_BASENAMES` opening | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1554` | tuple of `chunk_contributions.csv`, `chunk_metadata.json`, `chunk_summary.md`, `halt_diagnostic.json` |
| `chunk_manifest_digest` function | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1609` | `def chunk_manifest_digest(chunk_iso_dates: List[str]) -> str:` |
| `substrate_gap_diagnostic` halt-path | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1349–1351` | dict opener at 1349; both keys = `list(KNOWN_SUBSTRATE_GAPS)` |
| `substrate_gap_diagnostic` success-path | `scripts/run_lane2_gdelt1_full_daily_count_build.py:2011–2013` | dict opener at 2011; both keys = `list(KNOWN_SUBSTRATE_GAPS)` |

Chunk-specific lines `1519`, `1532`, `1545` are exactly one greater than the corresponding `chunk_2016` line numbers (`1518`, `1531`, `1544`) — `chunk_2017` follows `chunk_2016` in the canonical list, counts dict, and date-range dict. All other anchors are unchanged across all four prior chunk cycles.

## Runtime projection and watch-item

**Projected `chunk_2017` runtime** (using the canonical URLs-form strict anchor established in the chunk_2016 closure):

```
365 URLs × 2.8 s/URL ≈ 1,022.0 s ≈ 17m 2.0s ≈ ~17m 2s
```

Dimensional note: `URLs × s/URL = s`. The URLs-form is the canonical future strict grep anchor per the chunk_2016 closure decision; the no-URLs form `365 × 2.8 s/URL ≈ 1,022.0 s ≈ 17m 2.0s ≈ ~17m 2s` is substantively equivalent but should not be the preferred future strict anchor.

**Conservative `~2.8 s/URL` anchor is preserved from the chunk_2016 closure.** Observed per-URL rates across completed chunks:

| Chunk | URLs | Runtime | s/URL | Slowdown vs prior |
|---|---|---|---|---|
| `chunk_2013_partial` | 275 | ~8m 20s | ~1.8 | — |
| `chunk_2014` | 361 | ~13m 44s | ~2.28 | +27% |
| `chunk_2015` | 365 | ~16m 54s | ~2.78 | +22% |
| `chunk_2016` | 366 | ~18m 34s | ~3.04 | +9.4% |

**Per-step slowdown deceleration `+27% → +22% → +9.4%`** supports preserving the `~2.8 s/URL` anchor for chunk_2017 planning. The chunk_2016 closure recorded that the slowdown trend continues but at a decelerating per-step magnitude, and that `chunk_2016` fell below the `~3.4 s/URL` bump-trigger.

**Three-branch runtime watch-item (explicit):**

- (a) `>= ~3.4 s/URL` → bump the planning anchor in the post-chunk execution-closure memory update.
- (b) flat or improved vs prior chunk → treat slowdown as transient and preserve the `~2.8 s/URL` anchor.
- (c) slowdown continues but remains below the `~3.4 s/URL` bump-trigger → preserve `~2.8 s/URL` anchor and keep the watch active.

The watch remains active for `chunk_2017`. The chunk_2016 observed `~3.04 s/URL` would, if reproduced for `chunk_2017`, give a wall-clock of `365 × 3.04 = 1,109.6 s ≈ ~18m 30s` — still safely above the 10-min Bash foreground tool ceiling, so same-session background execution remains the default.

This runtime calibration is record-only and does NOT weaken the no-retry / exactly-once / no-off-session / no-market-data / no-Step-2 / no-checkpoint-resume / no-bounded-parallelism rules.

## Substrate-gap diagnostic expectation

This is the load-bearing item established by the `f4590eb` planning correction and now **twice empirically validated** (chunk_2015 at `ed4e74c` and chunk_2016 at `e6874d6`).

The runner constructs `substrate_gap_diagnostic` by writing the **global** `KNOWN_SUBSTRATE_GAPS` list to both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` unconditionally, regardless of the chunk's own date range (runner lines 1349–1351 halt-path, lines 2011–2013 success-path). It is **not** a per-chunk intersection.

For `chunk_2017` (zero in-range 2017 gaps, but the runner is byte-identical to `389747e` and the global `KNOWN_SUBSTRATE_GAPS` tuple is unchanged), the expected `substrate_gap_diagnostic` in `chunk_metadata.json` is:

```
known_substrate_gap_dates       = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
substrate_gap_dates_not_fetched = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
```

**Not** `[] / []`. The future `chunk_2017` execution prompt and post-chunk report must validate this exact list in the exact expected order on both surfaces.

Semantic clarification:

- `chunk_2017` has **zero in-range 2017 substrate gaps**.
- The runner diagnostics still surface the **global** `KNOWN_SUBSTRATE_GAPS` unconditionally.
- The correction was **empirically validated by chunk_2015 and chunk_2016**; the third consecutive zero-in-range-gap chunk (chunk_2017) is expected to produce the same diagnostic shape unless the runner implementation changes.

## Inherited locked rules

The future execution prompt and the live run it authorizes will inherit all of the following locked premises without re-litigation:

- **Recognized-list authority** (`84ea721e…fff835fc`): only daily URLs derived from the §10 capture, filtered to `chunk_2017`'s year range, may be fetched.
- **SQLDATE re-keying** (`0065d10` §5).
- **No-market-data firewall** unconditionally.
- **No-2023+ posture** (`0ddbd51` / `7780a97` §11.1).
- **No-retry rule** (`7780a97` §13.4 / Decision I).
- **Exactly-once fetch semantics** (`7780a97` §13.3).
- **No raw payload preservation** (`7780a97` §15.11).
- **No category/theme/actor/geography/tone filtering** (`7780a97` §8 + `c10ae74` §8).
- **No instrument construction / no Step 2** — gated behind a separately authorized firewall-retirement memo + Step 2 authorization.
- **No off-session execution** (`fbc605b` Plan-C reserve only; not authorized).
- **No checkpoint/resume** (`fbc605b` Plan-B reserve only; not implemented).
- **No bounded parallelism** (`d7c8775` Decision 2B rejected).
- **Per-chunk output is NOT the final canonical `daily_count.csv`**: merge step is separately authorized (`5962c20` §14 step 6).
- **Merge remains blocked until all 10 chunks succeed** (`5962c20` §9.1.2): a successful `chunk_2017` would advance progress to 5 of 10, not unblock merge.

## Prior continuity envelope

The future `chunk_2017` live execution must protect **all four** completed chunks at four checkpoints (preflight; post-run; after report creation; final post-push).

### `chunk_2013_partial`

| Item | Value |
|---|---|
| Tracked report | `docs/lane2_gdelt1_full_build_chunk_2013_partial_execution_report_v0.1.md` (commit `065d4754f69e2c35eef1ebdb7e4bf960ca9e806b`) |
| Output directory | `results/lane2_gdelt1_full_daily_count_build/chunk_2013_partial_20260524T135157Z/` |
| `chunk_contributions.csv` | 17,642 B / SHA-256 `9f07c8018c322027841dbf6484f19c2218d2945731e775b9ced03099cfa37247` |
| `chunk_metadata.json` | 214,857 B / SHA-256 `14a407a49e53f660a581bcdc7cee224e3228046aa1ea51eaae5e7eb5dc8a03c1` |
| `chunk_summary.md` | 440 B / SHA-256 `9e88e95cc33e4f99ddc3a810db23cd076ac51928d7504b7bab35780d5d15ed42` |
| `chunk_manifest_digest` | `6ac92439455d3f59df64cfeca6256f54a319c0ac82d40886f11b26becbfc8b43` |

### `chunk_2014`

| Item | Value |
|---|---|
| Tracked report | `docs/lane2_gdelt1_full_build_chunk_2014_execution_report_v0.1.md` (commit `770f982afdf736575a8bdfdd1b8ef57c4fc6f578`) |
| Output directory | `results/lane2_gdelt1_full_daily_count_build/chunk_2014_20260524T150055Z/` |
| `chunk_contributions.csv` | 32,908 B / SHA-256 `2ffd56fbd039ef5e7825c048358d7dc0a0b1e6f24d3d8614902de6217ce43660` |
| `chunk_metadata.json` | 265,975 B / SHA-256 `e0a944e38204d3fa6deb904d1b71b1a465a284c8203d75c025df372c80fd69d6` |
| `chunk_summary.md` | 424 B / SHA-256 `93db53b075e0e15bf1e91d5a4b41a75eb03695925aa5ff0e8a7ceae5c5c3459d` |
| `chunk_manifest_digest` | `93f9709656cb30252e1a9e5a8167dadb17b4f63bbb58ac6e4f4405b593994aba` |

### `chunk_2015`

| Item | Value |
|---|---|
| Tracked report | `docs/lane2_gdelt1_full_build_chunk_2015_execution_report_v0.1.md` (commit `ed4e74cc1a7b19d425dd474371b936491d38a056`) |
| Output directory | `results/lane2_gdelt1_full_daily_count_build/chunk_2015_20260524T163556Z/` |
| `chunk_contributions.csv` | 36,820 B / SHA-256 `7f7307be58e450190db5925cbc69861b95a827bbf279598a9eccecf549301ea2` |
| `chunk_metadata.json` | 264,289 B / SHA-256 `a73d5a252610c8610d22d579cbef18e8a58338a7985dac56d9f4d1fe5158d4e2` |
| `chunk_summary.md` | 424 B / SHA-256 `2de7dd3595d340d31c27993e416204050c1734dfd4d6ebd137f21c7135d5b2f9` |
| `chunk_manifest_digest` | `a5c61b06dee77a9916db6725cabe3a41d74d47d5807dce6ca2be1709bf17bd67` |

### `chunk_2016`

| Item | Value |
|---|---|
| Tracked report | `docs/lane2_gdelt1_full_build_chunk_2016_execution_report_v0.1.md` (commit `e6874d61415d4fda24883ae6492f1090b8ce85a7`) |
| Output directory | `results/lane2_gdelt1_full_daily_count_build/chunk_2016_20260524T194435Z/` |
| `chunk_contributions.csv` | 36,820 B / SHA-256 `91d82561f7296d08e8e134adf59729fb6c82fc2d4d3f11e02112b1a8393c2883` |
| `chunk_metadata.json` | 264,950 B / SHA-256 `b933d2f920716684a71a6ec1db7cce482519546c571f3572a53b08c03070b371` |
| `chunk_summary.md` | 420 B / SHA-256 `16570ed6a234045f3dc7892d6b5f5c9250220838ba94fdcaf79d402dc15326df` |
| `chunk_manifest_digest` | `e03e84ac29045a46ba4d2f207227b6f8f6c1222ba24bafbeefc7e02bd382c7a2` |

### Byte-count caution

`chunk_2015` `chunk_contributions.csv` and `chunk_2016` `chunk_contributions.csv` are both `36,820 B` — but SHA-256 values differ (`7f7307be…01ea2` vs `91d82561…3c2883`). Treat byte counts as non-identity checks only: SHA-256 is the authoritative content identifier. Do not rely on byte-count-only eyeballing for chunk_2017 continuity verification.

### Continuity-check requirements

The future `chunk_2017` execution prompt must verify all **twelve** prior artifact SHA-256 values, all **four** output directory paths (and the absence of any rename / move / deletion), all **four** prior `chunk_manifest_digest` values, and the byte-identicality of all **four** tracked reports against their committed states (`065d475`, `770f982`, `ed4e74c`, `e6874d6`) at four checkpoints: preflight, post-run (immediately after guard restore), after report creation, and after push (final).

No `chunk_2017_*` subdirectory may pre-exist inside `results/lane2_gdelt1_full_daily_count_build/` before the live run (the runner's `os.makedirs(..., exist_ok=False)` would hard-fail on collision). The `chunk_2017` execution must not touch any of the four prior output directories in any way.

## Future live execution shape

The future `chunk_2017` execution prompt (separately initiated; **NOT** authorized by this plan) will perform the following steps in order:

1. **Preflight read-only verification**. Confirm: `HEAD = origin/main = e6874d6` (or its accepted successor if intervening memory updates / planning memos have landed); ahead = `0`; tracked tree clean; all five guards `False` on disk; production `results/lane2_gdelt1_full_daily_count_build/` exists with the four prior chunk subdirectories but no `chunk_2017_<UTC>/` collision; recognized-list SHA + F4 baselines intact; chunk-runner source byte-identical to `389747e`; all four prior chunks' twelve artifact SHAs + four digests + four tracked reports unmodified.

2. **Enable commit**: flip `FULL_BUILD_AUTHORIZED = False → True` on **line 95** of `scripts/run_lane2_gdelt1_full_daily_count_build.py` via a single one-line edit. Subject: **`Enable Lane 2 full-build chunk_2017 run`**. Numstat `1\t1`.

3. **Single live runner invocation** of exactly one shell command (inline env var only, no `export`):
   ```
   LANE2_FULL_BUILD_AUTHORIZED=1 python3 scripts/run_lane2_gdelt1_full_daily_count_build.py --authorize-full-build-run --chunk-id chunk_2017
   ```
   **Exactly-once fetch semantics.** **Same-session in-session background execution** via Bash tool `run_in_background=true` with harness completion capture (mirroring the proven `bgzz8eqe5` / `blywiekhg` / `bnb2fqhzw` / `bikkl185t` patterns). **Not** off-session. Capture path: `/tmp/lane2_chunk_2017_run/`. No retry. No second run. No prior-chunk rerun. No next-chunk run. The env var `LANE2_FULL_BUILD_AUTHORIZED` must be `UNSET` after the run command's process exits.

4. **Restore commit**: flip line-95 back to `False`. Subject: **`Restore Lane 2 full-build guard after chunk_2017`**. Same `1\t1` numstat. Runner must return byte-identical to `389747e` post-restore (`git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py` returns 0). Restore happens **regardless of success or halt** of the live run.

5. **Verify** all five guards `False` after restore; `LANE2_*_AUTHORIZED` shell envs unset; output-artifact allow-list adherence; all four prior chunks' continuity SHAs and digests unchanged; tracked reports byte-identical to committed states.

6. **Write a tracked post-chunk execution report** at `docs/lane2_gdelt1_full_build_chunk_2017_execution_report_v0.1.md`, mirroring the `chunk_2016` report at `e6874d6`. Subject: **`Record Lane 2 chunk_2017 execution report`**. The report records: preflight state; enable-commit SHA; live-run command verbatim + timeout/background strategy + start/end UTC + exit code + stdout/stderr summary + harness shell ID; output directory path; chunk manifest digest; URL count (expected 365 / actual N); per-URL summary; aggregate row counts; per-offset totals; substrate-gap diagnostic (expected `["2014-01-23","2014-01-24","2014-01-25","2014-03-19"]` in both surfaces); halt class + diagnostic SHA if halted; restore-commit SHA; post-restore guard state; output artifact SHA-256 manifest; boundary confirmations; prior-chunk continuity confirmation for **all four** completed chunks; new runtime calibration data point.

7. **Commit cycle**: three commits in order — `Enable Lane 2 full-build chunk_2017 run` → `Restore Lane 2 full-build guard after chunk_2017` → `Record Lane 2 chunk_2017 execution report`. **One fast-forward push to `origin/main`** only after the restore commit and report commit both exist and all guards are `False` on disk.

8. **Stop for the separately authorized chunk_2017 execution-closure memory update.** Do not initiate `chunk_2018` work, merge, or Step 2.

## Future live execution validation requirements

The future live execution report must verify:

- exit code `0`
- exactly one new `chunk_2017_<UTC>/` output directory
- `actual_completed_file_count = expected_file_count = 365`
- `chunk_id = chunk_2017`
- `chunk_manifest_digest` is recorded (new value, distinct from `6ac92439…bfc8b43`, `93f97096…994aba`, `a5c61b06…bf17bd67`, and `e03e84ac…382c7a2`)
- `source_recognized_list_sha256 = 84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` (matches recognized-list authority)
- `no_retry_confirmation = True`
- **all 9 boundary_declarations True** (`no_2023plus_access`, `no_asset_or_return_logic`, `no_category_theme_actor_filtering`, `no_market_calendar_alignment`, `no_market_data`, `no_negative_control`, `no_payload_preservation_after_parsing`, `no_spike_threshold_tuning`, `no_step_2`)
- corrected substrate-gap diagnostic shape equals the four 2014 dates `["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]` on both surfaces, **not** `[] / []`
- zero in-range 2017 gaps interpreted semantically (KNOWN_SUBSTRATE_GAPS contains only 2014 dates that fall outside chunk_2017's range)
- no `halt_diagnostic.json` on success
- no raw payloads
- no `.zip`
- no extracted CSV
- no merge artifacts
- no market data
- no Step 2
- no instrument construction
- all five guards `False` post-restore (with explicit file:line citations)
- shell envs `LANE2_*_AUTHORIZED` unset
- runner byte-identical to `389747e`
- continuity envelope preserved for all prior chunks (`chunk_2013_partial`, `chunk_2014`, `chunk_2015`, `chunk_2016`): twelve artifact SHAs + four digests + four tracked reports unchanged at all four checkpoints

## Stop conditions

Hard stop conditions the future `chunk_2017` execution prompt must enforce. Any single one halts the cycle.

### Preflight (execution does not begin)

- HEAD ≠ accepted ancestor (e.g., not `e6874d6` or a reviewed successor).
- `origin/main` mismatch with HEAD.
- Tracked tree dirty.
- Any staged files pre-enable.
- Any of the five guards already `True` on disk pre-enable.
- Any `LANE2_*_AUTHORIZED` shell env set pre-enable.
- Recognized-list SHA mismatch.
- F4 baseline SHA mismatch.
- Target post-chunk report already exists pre-write.
- Existing `chunk_2017_<UTC>/` subdirectory pre-run.
- Any prior chunk (chunk_2013_partial / chunk_2014 / chunk_2015 / chunk_2016) output directory, any of its three artifacts, its digest, or its tracked report missing, renamed, or SHA-256-mutated.
- Chunk-runner source file diverges from `389747e` pre-enable.
- Inability to run the live command via same-session background execution with captured exit status / stdout / stderr / start UTC / end UTC.

### Runner-internal (during the live run)

- Chunk manifest actual count ≠ `365`.
- Recognized-list SHA mismatch at runtime.
- Reconciliation contradiction.
- HTTP non-200 / redirect / connection error / timeout for any in-chunk URL.
- Unexpected offset outside `{0, −1, −7, −30, −365, −3650, +1}` for any parsed row.
- 2023+ SQLDATE in any parsed row.
- 2023+ URL construction attempt.
- Output allow-list violation.
- Counting-invariant violation.

### Post-run (block report commit / push)

- Inability to restore `FULL_BUILD_AUTHORIZED = False`. Guard restoration is the highest priority.
- Any guard `True` on disk after the restore commit.
- Any raw payload bytes / `.zip` / extracted CSV in the chunk_2017 output directory.
- Output outside `ALLOWED_CHUNK_OUTPUT_BASENAMES`.
- Retry / second-GET attempts in the manifest.
- Accidental market-data / Step 2 / spike-burst / return-window logic.
- Any modification to any prior chunk's output (SHA-256 mismatch on any of the twelve prior artifacts) or report (byte-divergence from committed copy) or digest.
- Accidental next-chunk run (e.g., a `chunk_2018` directory appearing).
- Accidental merge run.
- `substrate_gap_diagnostic` does not match `["2014-01-23","2014-01-24","2014-01-25","2014-03-19"]` in both surfaces.

Any halt condition triggers the **session-interruption recovery rule**: restore the guard, preserve partial output as-is, emit verdict `FULL-BUILD CHUNK_2017 RUN HALTED — AWAIT ADJUDICATION`.

## Locked boundaries

This plan authorizes **none** of the following:

- no live execution now
- no GDELT contact now
- no guard flip now
- no chunk_2018+ work
- no merge
- no Step 2
- no market data
- no instrument construction
- **exactly-once fetch semantics** (preserved, no retry after a started live run)
- no raw payload preservation
- no checkpoint/resume
- no bounded parallelism
- no off-session execution
- no output artifact tracking
- no F4 modification
- no recognized-list mutation
- no memory edit in this planning sub-cycle
- no source / test / config / prior docs / prior reports / existing result-artifact edit (this plan only writes the single new memo file)

The no-market-data firewall, no-2023+ posture, no-retry rule, exactly-once fetch semantics, no-merge-until-10/10 rule, recognized-list authority, and SQLDATE re-keying all remain in force.

## Locked-commit edits terminology

The corrected terminology adopted at the `chunk_2016` planning memo (`edef491`) and recorded in memory is **`Locked-commit edits`** (NOT `locked-memo edit`). Future planning memos for `chunk_2018`, `chunk_2019`, `chunk_2020`, `chunk_2021`, and `chunk_2022` must carry forward `Locked-commit edits` terminology and must not regress to `locked-memo edit` phrasing.

`Locked-commit edits` to prior memo / execution-cycle commits in the lifecycle chain `a8a9dd2` / `a2a8fd5` / `e9f8781` / `487dadb` / `3537a62` / `73a7911` / `858b501` / `0065d10` / `7780a97` / `bc7b66b` / `c10ae74` / `d7c8775` / `fbc605b` / `5962c20` / `389747e` / `447656d` / `c6b313c` / `167a08a` / `065d475` / `4276b30` / `574ce77` / `13f14ba` / `770f982` / `f4590eb` / `14c2f6b` / `083649b` / `ed4e74c` / `edef491` / `1481820` / `3fe1b58` / `e6874d6` / `e55e09a` / `0b341b4` / `845c51c` / `e81208d` / `7c85e3f` / `9319d30` are **not** authorized.

## Outcome classes for future live execution

The future execution prompt must classify its outcome as exactly one of:

- **SUCCESS** — runner exits with code 0; three success artifacts present; `actual = expected = 365`; substrate-gap diagnostic matches expected; all four prior chunks' continuity preserved.
- **BLOCKED BEFORE ENABLE** — a preflight check failed; no guard flip occurred.
- **LIVE RUN FAILURE** — runner exit non-zero, halt class identified, `halt_diagnostic.json` may exist.
- **OUTPUT VERIFICATION FAILURE** — runner exited cleanly but the produced output set / SHAs / metadata do not match the success contract.
- **OUTPUT VERIFICATION FAILURE / SUBSTRATE GAP DIAGNOSTIC MISMATCH** — substrate-gap diagnostic deviates from the canonical four-2014-date global shape.
- **PRIOR CHUNK CONTINUITY FAILURE** — any of chunk_2013_partial, chunk_2014, chunk_2015, chunk_2016 artifacts / reports / digests changed during the cycle.
- **GUARD RESTORE FAILURE** — line-95 could not be restored to `False`.
- **INFRASTRUCTURE FAILURE / SUBPROCESS STATE AMBIGUOUS** — tool-layer timeout / abort / interruption.
- **INFRASTRUCTURE FAILURE / SUBPROCESS STATE UNKNOWN** — subprocess state could not be reliably established.

**Guard restoration must be prioritized after any enable commit, regardless of live-run success or failure, unless the repo state itself prevents restoration.** Push must not proceed while the guard remains enabled.

## Substrate progress projection

If `chunk_2017` succeeds with `actual_completed_file_count = 365`:

| Metric | Before `chunk_2017` | Projected after `chunk_2017` |
|---|---|---|
| Chunks complete | 4 / 10 | **5 / 10** |
| Completed chunks list | `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, `chunk_2016` | `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, `chunk_2016`, `chunk_2017` |
| Daily URLs complete | 1,367 / 3,558 | **1,732 / 3,558** (= 1,367 + 365) |
| Percent complete by URL count | ~38.4% | ~**48.7%** |
| Remaining daily URLs | 2,191 | **1,826** |
| Remaining chunks | 6 | **5** (`chunk_2018` through `chunk_2022`) |

`merge remains blocked until 10/10 chunks succeed`. Chunks `chunk_2018` through `chunk_2022` each require their own separately authorized execution prompt; this cycle does not authorize them.

## Carry-forward items

- **Section 9 / commit-report cosmetic observation** remains **unresolved** from the chunk_2016 execution-closure memory update. The specific anchor is not found in current memory and the intended wording cannot be safely reconstructed without fabrication. It should not block chunk_2017 planning or live execution.
- **Calibration #7 / sanity-check blind-spot lesson** (recorded in the chunk_2016 execution-closure memory update): future prompt sanity-checks involving literal strings, SHAs, line numbers, or file paths must cross-reference the anchor against the actual memo/report text from prior chat reports, not only against memory or the prompt's own statements. Future review prompts for the chunk_2017 memo and execution report should apply this lesson.
- **Digest hit counts in memory** are structural / context-dependent and should not be assumed to follow a strict monotonic formula. The asymmetry observed in `project_lane2_attention_spike.md` (chunk_2013_partial: 3 hits, chunk_2014: 2, chunk_2015: 2, chunk_2016: 0 → after chunk_2016 closure update: counts grew) reflects intentional structural repetition — each new continuity-envelope citation re-cites earlier chunks. This is benign.
- **URL/no-URL canonicalization**: the canonical strict-anchor form is the URLs form `365 URLs × 2.8 s/URL ≈ 1,022.0 s ≈ 17m 2.0s ≈ ~17m 2s` (used by this memo). The no-URLs form `365 × 2.8 s/URL ≈ 1,022.0 s ≈ 17m 2.0s ≈ ~17m 2s` is substantively equivalent (`URLs × s/URL = s`) but should not be the preferred future strict grep anchor.

## Decision points before live execution

All decision points from prior cycles are resolved by precedent for `chunk_2017`:

| Decision point | Resolution by precedent |
|---|---|
| Chunk-output artifact disposition | **Untracked by default** per `0065d10` Decision 3A + `5962c20` §8.2; reaffirmed by `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, and `chunk_2016` cycles. |
| Commit sequence | **Three commits: Enable → Restore → Report.** Reaffirmed by all four prior cycles. |
| Post-chunk report commit timing | **Report committed standalone** (output untracked). |
| Timeout / subprocess strategy | **In-session background execution via Bash `run_in_background=true`** with harness completion capture; mirrors `bgzz8eqe5`, `blywiekhg`, `bnb2fqhzw`, `bikkl185t`; same-session, **not** off-session. |
| Output-directory timestamping | Runner-controlled via `chunk_2017_<UTC>/`; collision handled by `os.makedirs(..., exist_ok=False)`. |
| Substrate-gap diagnostic surfacing | Runner surfaces the global `KNOWN_SUBSTRATE_GAPS` list unconditionally; expected chunk_2017 shape is the four 2014 dates in both fields, not `[]`. Twice empirically validated. |
| Conservative runtime anchor | `~2.8 s/URL` preserved from `chunk_2016` closure. Three-branch watch-item explicit. |
| Locked-commit terminology | Adopted `Locked-commit edits` (NOT `locked-memo edit`); carry forward to all subsequent planning memos. |

## Next steps after this memo

The next procedural steps after this planning memo's creation are, in order:

- **Sanity-check review** of the planning memo (read-only, by the user or a separately invoked review-only prompt). Apply calibration #7: cross-reference all literal strings, SHAs, line numbers, and file paths against the actual memo text rather than only against memory or prompt-internal wording.
- **Separate explicit commit prompt** (no commit is authorized by this planning-memo-creation turn).
- **Separate memory-update prompt for the planning closure** (after commit/push lands).
- **Only then**, a separate live `chunk_2017` execution-authorization prompt (which performs the steps in §"Future live execution shape" above).

**No execution is authorized by this planning memo creation turn.** Its persistence scope is complete upon writing the single file at `docs/lane2_gdelt1_full_build_chunk_2017_execution_authorization_plan_v0.1.md`. No review, no staging, no commit, no push, no memory update, no live execution, no guard flip, no GDELT contact, no merge, no market data, and no Step 2 work is authorized by this turn. The next eligible action after this memo is created is **chunk_2017 planning memo on-disk content review** — **not chunk_2017 live execution**, **not merge**, **not Step 2**. **`merge remains blocked until 10/10 chunks succeed`.**
