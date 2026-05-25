# Lane 2 GDELT1 full-build chunk_2018 execution-authorization plan v0.1

## 1. Purpose and decision

This memo plans and authorizes a **later, separately initiated** chunk_2018 live execution prompt. It is the sixth per-chunk planning memo in the Lane 2 GDELT1 full-build sequence (after `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, `chunk_2016`, and `chunk_2017`).

Decision: **AUTHORIZE LATER**.

This memo itself does NOT authorize and does NOT initiate:

- guard flip (the `FULL_BUILD_AUTHORIZED` module constant or any other guard)
- live runner invocation
- GDELT contact
- chunk_2018 execution
- chunk_2019+ work
- merge
- Step 2
- market-data access
- instrument construction
- commit/push of any artifact (including this memo)
- memory edits

The commit/push of this memo and all subsequent steps require explicit user initiation under separately scoped prompts.

## 2. Current state

The canonical state at memo creation is recorded here as a contiguous prose string for future grep verification (per the HEAD-literal discipline carried forward from the chunk_2017 closure): HEAD = origin/main = 0e5f3f11a77319dc0b9b9af906c89df2e585d12e (short `0e5f3f1`; ahead/behind = 0 0; tracked tree clean).

| Field | Value |
|---|---|
| Short SHA | `0e5f3f1` |
| Latest report subject | *"Record Lane 2 chunk_2017 execution report"* |
| Latest report path | `docs/lane2_gdelt1_full_build_chunk_2017_execution_report_v0.1.md` |
| Latest report stats | `1 file changed, 142 insertions(+)` |
| Latest report file SHA-256 | `1bc474a184bb1482ca01196d669abcca81c130c8e2ed1bd05064eb75047db0c6` |
| Runner | byte-identical to `389747e` (verified by empty `git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py`) |
| Guards | all five `False` on disk (see §10) |
| Shell envs | `LANE2_*_AUTHORIZED` unset |

Substrate progress at memo creation:

- **5 of 10 chunks complete** (`chunk_2013_partial`, `chunk_2014`, `chunk_2015`, `chunk_2016`, `chunk_2017`)
- **1,732 of 3,558 daily URLs complete** (`275 + 361 + 365 + 366 + 365 = 1,732`, ≈ **48.7%**)
- 5 chunks remain
- **1,826 URLs** remain
- next chunk is `chunk_2018`

Remaining chunks (canonical from runner `EXPECTED_CHUNK_COUNTS`, lines 1527–1538):

| Chunk | Expected URLs |
|---|---|
| `chunk_2018` | 365 |
| `chunk_2019` | 365 |
| `chunk_2020` | 366 |
| `chunk_2021` | 365 |
| `chunk_2022` | 365 |

## 3. Target chunk

| Field | Value |
|---|---|
| chunk ID | `chunk_2018` |
| Expected daily URLs | **365 URLs** |
| Date range | **2018-01-01** through **2018-12-31** |
| Date-range tuple in runner (line 1546) | `(date(2018, 1, 1), date(2018, 12, 31))` |
| Future output directory pattern | `results/lane2_gdelt1_full_daily_count_build/chunk_2018_<UTC>/` |
| Future harness capture path | `/tmp/lane2_chunk_2018_run/` |
| Future tracked execution report | `docs/lane2_gdelt1_full_build_chunk_2018_execution_report_v0.1.md` |

## 4. Runner anchors verified read-only

Verified against `scripts/run_lane2_gdelt1_full_daily_count_build.py` at HEAD `0e5f3f1` (observed line numbers, not assumed):

| Anchor | File:line | Observed value |
|---|---|---|
| Guard module constant (ships False) | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95` | `FULL_BUILD_AUTHORIZED = False` |
| `SEAL_START` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:116` | `date(2023, 1, 1)` |
| `KNOWN_SUBSTRATE_GAPS` tuple | `scripts/run_lane2_gdelt1_full_daily_count_build.py:125–130` | `("2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19")` |
| `chunk_2018` listed in canonical chunk order tuple | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1520` | `"chunk_2018",` |
| `EXPECTED_CHUNK_COUNTS["chunk_2018"]` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1533` | `"chunk_2018": 365,` |
| `CHUNK_YEAR_RANGES["chunk_2018"]` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1546` | `"chunk_2018": (date(2018, 1, 1), date(2018, 12, 31)),` |
| `chunk_manifest_digest` function | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1609` | function exists |
| Halt-path `substrate_gap_diagnostic` construction | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1349–1351` | builds both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` from global `KNOWN_SUBSTRATE_GAPS` |
| Success-path `substrate_gap_diagnostic` construction | `scripts/run_lane2_gdelt1_full_daily_count_build.py:2011–2013` | builds both surfaces from global `KNOWN_SUBSTRATE_GAPS` |

Runner byte-identity to `389747e` re-verified post-`0e5f3f1`: `git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py` returns 0.

## 5. Runtime projection and three-branch watch-item

### 5.1 Canonical strict-anchor projection

Use the explicit URLs-form runtime projection, which is the going-forward canonical strict-anchor form (carried forward from the chunk_2016 closure URL/no-URL canonicalization decision):

365 URLs × 2.8 s/URL ≈ 1,022.0 s ≈ 17m 2.0s ≈ ~17m 2s

Dimensional note: URLs × s/URL = s. The no-URLs form is substantively equivalent but not preferred.

### 5.2 Anchor preservation

- The conservative `~2.8 s/URL` anchor is preserved from the chunk_2017 closure (branch (c) verdict: `chunk_2017` ran at ~3.16 s/URL, which is below the `≥~3.4 s/URL` bump-trigger).
- Anchor was not bumped after `chunk_2014`, `chunk_2015`, `chunk_2016`, or `chunk_2017`; bump-trigger has never fired.

### 5.3 Step-slowdown trend (kept separate from anchor-relative comparison)

Per-step slowdown trend across closed chunks:

+27% (2013→2014) → +22% (2014→2015) → +9.4% (2015→2016) → +3.9% (2016→2017)

Trend: **+27% → +22% → +9.4% → +3.9%** — deceleration continues.

### 5.4 Anchor-relative chunk_2017 comparison (kept separate from the step-slowdown trend)

`chunk_2017` was **+12.9%** relative to the `2.8 s/URL` planning anchor (~1,152.66 s observed vs ~1,022.0 s projected). This anchor-relative figure is recorded distinctly from the step-slowdown trend and must NOT be folded into the step-slowdown trend line.

### 5.5 Three-branch runtime watch-item

The actual chunk_2018 execution may still be slower than projection; the watch remains active. Three branches are explicitly labeled for the future execution-closure memory update:

- **branch (a)**: observed `≥ ~3.4 s/URL` → **bump** the planning anchor in the execution-closure memory update.
- **branch (b)**: observed flat or improved vs `chunk_2017` (`≤ ~3.16 s/URL`) → treat slowdown as transient and **preserve** the `~2.8 s/URL` anchor.
- **branch (c)**: observed continued slowdown but **below** the `≥ ~3.4 s/URL` bump-trigger → **preserve** the `~2.8 s/URL` anchor and **keep the watch active** for `chunk_2019`.

The bump-trigger `≥ ~3.4 s/URL` (ASCII-equivalent: `>= ~3.4 s/URL`) is held constant from the chunk_2016 closure decision.

## 6. Substrate-gap diagnostic expectation

With the runner unchanged (byte-identical to `389747e`), the future chunk_2018 execution-time substrate-gap diagnostic is expected to surface the canonical post-`f4590eb` shape on **both surfaces**:

- `known_substrate_gap_dates = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]`
- `substrate_gap_dates_not_fetched = ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]`

NOT `[]` / `[]`.

Semantic interpretation:

- `chunk_2018` has **zero in-range 2018 substrate gaps** — the runner's `KNOWN_SUBSTRATE_GAPS` constant at lines 125–130 contains only the four 2014 dates, none of which intersect chunk_2018's `2018-01-01..2018-12-31` range.
- The runner nevertheless surfaces the **global** `KNOWN_SUBSTRATE_GAPS` tuple unconditionally to both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` (runner lines 1349–1351 halt-path; 2011–2013 success-path). This is the canonical post-`f4590eb` shape.

The correction is currently **thrice-empirically-validated** by `chunk_2015` (`ed4e74c`) + `chunk_2016` (`e6874d6`) + `chunk_2017` (`0e5f3f1`) across three consecutive zero-in-range-gap chunks. If `chunk_2018` succeeds with the same shape, it will become fourth-validated — but that is future-only and is NOT pre-recorded as a fact by this memo.

## 7. Prior continuity envelope

The following five completed chunks must remain byte-identical across the future chunk_2018 execution cycle. Re-verify SHAs at all four checkpoints (preflight, post-run, after-report-creation, final-post-push) per the chunk_2017 precedent.

### 7.1 chunk_2013_partial

- Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2013_partial_20260524T135157Z/`
- Tracked report commit: `065d4754f69e2c35eef1ebdb7e4bf960ca9e806b`
- Artifacts:
  - `chunk_contributions.csv` — `17,642 B` / `9f07c8018c322027841dbf6484f19c2218d2945731e775b9ced03099cfa37247`
  - `chunk_metadata.json` — `214,857 B` / `14a407a49e53f660a581bcdc7cee224e3228046aa1ea51eaae5e7eb5dc8a03c1`
  - `chunk_summary.md` — `440 B` / `9e88e95cc33e4f99ddc3a810db23cd076ac51928d7504b7bab35780d5d15ed42`
- `chunk_manifest_digest`: `6ac92439455d3f59df64cfeca6256f54a319c0ac82d40886f11b26becbfc8b43`

### 7.2 chunk_2014

- Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2014_20260524T150055Z/`
- Tracked report commit: `770f982afdf736575a8bdfdd1b8ef57c4fc6f578`
- Artifacts:
  - `chunk_contributions.csv` — `32,908 B` / `2ffd56fbd039ef5e7825c048358d7dc0a0b1e6f24d3d8614902de6217ce43660`
  - `chunk_metadata.json` — `265,975 B` / `e0a944e38204d3fa6deb904d1b71b1a465a284c8203d75c025df372c80fd69d6`
  - `chunk_summary.md` — `424 B` / `93db53b075e0e15bf1e91d5a4b41a75eb03695925aa5ff0e8a7ceae5c5c3459d`
- `chunk_manifest_digest`: `93f9709656cb30252e1a9e5a8167dadb17b4f63bbb58ac6e4f4405b593994aba`

### 7.3 chunk_2015

- Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2015_20260524T163556Z/`
- Tracked report commit: `ed4e74cc1a7b19d425dd474371b936491d38a056`
- Artifacts:
  - `chunk_contributions.csv` — `36,820 B` / `7f7307be58e450190db5925cbc69861b95a827bbf279598a9eccecf549301ea2`
  - `chunk_metadata.json` — `264,289 B` / `a73d5a252610c8610d22d579cbef18e8a58338a7985dac56d9f4d1fe5158d4e2`
  - `chunk_summary.md` — `424 B` / `2de7dd3595d340d31c27993e416204050c1734dfd4d6ebd137f21c7135d5b2f9`
- `chunk_manifest_digest`: `a5c61b06dee77a9916db6725cabe3a41d74d47d5807dce6ca2be1709bf17bd67`

### 7.4 chunk_2016

- Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2016_20260524T194435Z/`
- Tracked report commit: `e6874d61415d4fda24883ae6492f1090b8ce85a7`
- Artifacts:
  - `chunk_contributions.csv` — `36,820 B` / `91d82561f7296d08e8e134adf59729fb6c82fc2d4d3f11e02112b1a8393c2883`
  - `chunk_metadata.json` — `264,950 B` / `b933d2f920716684a71a6ec1db7cce482519546c571f3572a53b08c03070b371`
  - `chunk_summary.md` — `420 B` / `16570ed6a234045f3dc7892d6b5f5c9250220838ba94fdcaf79d402dc15326df`
- `chunk_manifest_digest`: `e03e84ac29045a46ba4d2f207227b6f8f6c1222ba24bafbeefc7e02bd382c7a2`

### 7.5 chunk_2017

- Output directory: `results/lane2_gdelt1_full_daily_count_build/chunk_2017_20260524T231143Z/`
- Tracked report commit: `0e5f3f11a77319dc0b9b9af906c89df2e585d12e`
- Tracked execution report SHA-256: `1bc474a184bb1482ca01196d669abcca81c130c8e2ed1bd05064eb75047db0c6`
- Artifacts:
  - `chunk_contributions.csv` — **`36,565 B`** / `87ba1a907d0c6879e370796ef12bf1df1efa1c9e2281489821b44f3343db3223`
  - `chunk_metadata.json` — **`264,066 B`** / `56fece119d32e1ebeab5d5964c83848200b91ce2486ca177017578b67ee24016`
  - `chunk_summary.md` — **`420 B`** / `b2f42542fa295b6feb1248220d05a11302b1d43d52bb616ba09df9c171fdeffc`
- `chunk_manifest_digest`: `6aec5ad96f63721b5ce26831d3ebb38af05646fb64842e18fda14bba492c258e`

### 7.6 Byte-count-not-identity caution

The five prior `chunk_manifest_digest` values are all distinct. However, byte-count coincidences exist across chunks (e.g., `chunk_2015` and `chunk_2016` both have `chunk_contributions.csv = 36,820 B` but differ in SHA-256). **Do not rely on byte-count-only eyeballing** — always cross-check SHA-256 (byte-count-not-identity caution).

## 8. Future live execution shape

The future, separately initiated chunk_2018 live execution prompt should follow this exact shape. Nothing in this section authorizes execution now.

### 8.1 Guard-enable commit

- Subject: `Enable Lane 2 full-build chunk_2018 run`
- Only expected source change: `scripts/run_lane2_gdelt1_full_daily_count_build.py:95` — `FULL_BUILD_AUTHORIZED = False → True` (numstat `1\t1`).
- No other file edited. No staged or untracked changes outside this single one-line flip.

### 8.2 Exactly one live runner invocation

Live command (verbatim, **inline-env only, no `export`**):

`LANE2_FULL_BUILD_AUTHORIZED=1 python3 scripts/run_lane2_gdelt1_full_daily_count_build.py --authorize-full-build-run --chunk-id chunk_2018`

- **Exactly-once fetch semantics**: exactly one live runner invocation; no retry after a started live run; no second run; no prior-chunk rerun; no next-chunk run.
- **Same-session in-session background execution** via Bash tool `run_in_background=true` (NOT off-session). Mirrors the proven `chunk_2013_partial` `bgzz8eqe5`, `chunk_2014` `blywiekhg`, `chunk_2015` `bnb2fqhzw`, `chunk_2016` `bikkl185t`, and `chunk_2017` `b4fp4o3rn` patterns.
- Capture path: `/tmp/lane2_chunk_2018_run/` (`stdout.log`, `stderr.log`, `exit_code.txt`, `start_utc.txt`, `end_utc.txt`).
- Subprocess state must reach normal clean-exit path with known exit code `0`; guard restore performed only after the exit code is read.
- No raw payload preservation. No `.zip`. No extracted CSV. No checkpoint/resume. No bounded parallelism. No GDELT contact outside this single authorized command.

### 8.3 Guard-restore commit

- Subject: `Restore Lane 2 full-build guard after chunk_2018`
- Only expected source change: `scripts/run_lane2_gdelt1_full_daily_count_build.py:95` — `FULL_BUILD_AUTHORIZED = True → False` (numstat `1\t1`).
- Runner must return **byte-identical to `389747e`** after restore (`git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py` returns 0).

### 8.4 Execution report commit

- Expected report path: `docs/lane2_gdelt1_full_build_chunk_2018_execution_report_v0.1.md`
- Subject: `Record Lane 2 chunk_2018 execution report`
- Exactly one new tracked file under `docs/`; `create mode 100644`; no source / test / config / memory / result / F4 / recognized-list changes in the report commit.

### 8.5 Push

One fast-forward push to `origin/main`. No force. No tag push. No other-branch push. No hook bypass. No signing override.

### 8.6 Stop boundary

After the push completes, the live execution sub-cycle stops. The next eligible action is the separately authorized chunk_2018 execution-closure memory update — invoked by an explicit successor prompt, not by this memo or the live-execution prompt.

## 9. Future live execution validation requirements

The future chunk_2018 execution report must verify and record:

- exit code `0`
- exactly one new `chunk_2018_<UTC>/` output directory under `results/lane2_gdelt1_full_daily_count_build/`
- `actual_completed_file_count = expected_file_count = 365`
- `chunk_id = chunk_2018`
- `chunk_manifest_digest` recorded
- `source_recognized_list_sha256 = 84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` (matches recognized-list authority)
- `no_retry_confirmation = True`
- **all 9 boundary_declarations True**: `no_2023plus_access`, `no_asset_or_return_logic`, `no_category_theme_actor_filtering`, `no_market_calendar_alignment`, `no_market_data`, `no_negative_control`, `no_payload_preservation_after_parsing`, `no_spike_threshold_tuning`, `no_step_2`.
- Corrected substrate-gap diagnostic shape equals the four 2014 dates `["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]` on **both surfaces**, NOT `[]` / `[]`.
- Zero in-range 2018 gaps **interpreted semantically** (the runner unconditionally surfaces global `KNOWN_SUBSTRATE_GAPS`; in-range gap count is a separate semantic interpretation, not a diagnostic field).
- `total_in_window_rows` and `total_out_of_window_rows` recorded if surfaced by runner metadata/report (per the execution-closure recording discipline; chunk_2017 surfaced `66,303,468` / `12,791`).
- No `halt_diagnostic.json` on success.
- No raw payloads. No `.zip`. No extracted CSV. No merge artifacts. No final `daily_count.csv` / `build_metadata.json` / `build_summary.md`. No market data. No Step 2. No instrument construction.
- All five guards `False` post-restore (verified explicitly by file:line, not by transitive inference alone): `REAL_RETRIEVAL_ENABLED`, `COUNT_FEASIBILITY_AUTHORIZED`, `EVENT_FILE_PROBE_AUTHORIZED`, `ROW_DATE_CHARACTERIZATION_AUTHORIZED`, `FULL_BUILD_AUTHORIZED`.
- Shell envs `LANE2_*_AUTHORIZED` unset.
- Runner byte-identical to `389747e`.
- Continuity envelope preserved for all five prior chunks (§7 above) — re-verify all **fifteen** artifact SHAs, all **five** tracked report SHAs, and all **five** prior `chunk_manifest_digest` values at four checkpoints.

## 10. Locked boundaries

The following are locked for this planning sub-cycle and all subsequent sub-cycles until explicitly retired by a separately authorized memo:

- no live execution now
- no GDELT contact now
- no guard flip now
- no `chunk_2019+` work
- no merge
- no Step 2
- no market data
- no instrument construction
- **exactly-once fetch semantics** (when the live execution prompt is eventually invoked)
- no raw payload preservation
- no checkpoint/resume
- no bounded parallelism
- no off-session execution
- no retry after a started live run
- no output artifact tracking
- no F4 modification
- no recognized-list mutation
- no memory edit in this planning sub-cycle

Guard state at memo creation (verified explicitly by file:line):

- `src/lane2_gdelt1_count_feasibility.py:647: REAL_RETRIEVAL_ENABLED = False`
- `scripts/run_lane2_gdelt1_count_feasibility.py:49: COUNT_FEASIBILITY_AUTHORIZED = False`
- `scripts/run_lane2_gdelt1_event_file_probe.py:52: EVENT_FILE_PROBE_AUTHORIZED = False`
- `scripts/run_lane2_gdelt1_row_date_characterization.py:57: ROW_DATE_CHARACTERIZATION_AUTHORIZED = False`
- `scripts/run_lane2_gdelt1_full_daily_count_build.py:95: FULL_BUILD_AUTHORIZED = False`

Authority preserved:

- recognized-list SHA: `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`
- F4 baselines: `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d` and `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c`

## 11. Locked-commit edits terminology

Future correction language must use **Locked-commit edits**, not the older "locked-memo edit" phrasing. This memo uses **Locked-commit edits** throughout. The terminology supersedes the older phrasing project-wide for the Lane 2 GDELT1 full-build sequence.

## 12. Carry-forward items

### 12.1 Unresolved (non-blocking)

- `Section 9 / commit-report cosmetic observation` remains unresolved and non-blocking (carried forward unchanged from the chunk_2016 closure; the specific anchor was not located in current memory text and cannot be safely reconstructed without fabricating content).

### 12.2 Established disciplines to propagate

These disciplines are carried forward as defaults for the chunk_2018 sub-cycle and all later chunks until explicitly changed:

1. **Calibration #7 literal-anchor cross-check**: future prompt sanity checks must cross-reference actual memo/report text and on-disk content, not only memory or prompt-internal wording.
2. **Digest-hit count discipline**: digest hit counts in memory are structural/context-dependent and should not be assumed to follow a strict monotonic formula.
3. **URL/no-URL canonicalization**: future strict runtime anchors should use the explicit URLs form; no-URLs form is substantively equivalent (URLs × s/URL = s) but not preferred.
4. **Planning memo file-SHA discipline**: planning-closure memory updates should record committed planning memo file SHA-256 from `chunk_2017` forward unless later changed.
5. **Execution artifact recording discipline**: execution-closure memory updates should record artifact sizes and SHA-256 values for each chunk.
6. **Runner row-count recording discipline**: execution-closure memory updates should record `total_in_window_rows` and `total_out_of_window_rows` when surfaced by runner metadata/report, unless later changed.
7. **HEAD-literal grep discipline**: HEAD / origin/main / SHA literals used for future grep verification should appear as **contiguous prose strings**, not split across Markdown table columns. (This memo's §2 honors the discipline: HEAD = origin/main = 0e5f3f11a77319dc0b9b9af906c89df2e585d12e is written as a contiguous prose string.)
8. **prompt-transport integrity**: when sanity-checking prompts containing nested code fences, assess whether the outer wrapper could be terminated prematurely by an inner fence at delivery. Prefer no nested fenced code blocks or otherwise make transport robust. (This memo deliberately avoids nested fenced code blocks for the live command and other long literal strings, instead using single-backtick inline code so that future planning-memo / live-execution prompts can quote this memo without nested-fence transport failures.)

## 13. Next frontier after this memo

After this memo is created and reviewed, the next eligible sub-cycle is:

- **chunk_2018 planning memo on-disk content review** (separately authorized, awaits explicit user initiation).

This is **not** chunk_2018 live execution. This is **not** merge. This is **not** Step 2. **Merge remains blocked until 10/10 chunks succeed** per `5962c20` §9.1.2.

Frontier coda: not chunk_2018 live execution; not merge; not Step 2; merge remains blocked until 10/10 chunks succeed. Pause: await explicit next prompt.
