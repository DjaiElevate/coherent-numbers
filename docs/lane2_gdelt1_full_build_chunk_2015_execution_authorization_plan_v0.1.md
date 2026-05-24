# Lane 2 GDELT1 chunk_2015 execution-authorization plan v0.1

## Title

`Lane 2 GDELT1 chunk_2015 execution-authorization plan v0.1`

This memo is **planning-only**. It does not by itself execute `chunk_2015`, enable any guard, authorize GDELT contact, authorize merge, authorize Step 2, touch market data, or retire the no-market-data firewall. A separate review of this plan, a separate commit, a separate memory-update prompt for the planning closure, and a separate live-execution-authorization prompt are all still required before any `chunk_2015` execution. Its persistence scope is one tracked file at `docs/lane2_gdelt1_full_build_chunk_2015_execution_authorization_plan_v0.1.md`.

## Current canonical state

| Item | Value |
|---|---|
| `HEAD = origin/main` at planning creation | `770f982afdf736575a8bdfdd1b8ef57c4fc6f578` |
| Short SHA | `770f982` |
| Ahead / behind | `0 / 0` |
| Latest execution-cycle commit chain (closing `chunk_2014`) | enable `574ce77` → restore `13f14ba` → report `770f982` |
| Planning-memo commit chain so far | `chunk_2013_partial` plan `447656d` → `chunk_2014` plan `4276b30` |
| Substrate progress before `chunk_2015` | **2 / 10 chunks complete**; 636 / 3,558 daily URLs complete; 2,922 daily URLs + 8 chunks remaining |
| Completed chunks | `chunk_2013_partial`, `chunk_2014` |
| Recognized-list authority SHA-256 | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` |
| F4 baseline SHAs (preserved) | `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d` / `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c` |
| Locked offset taxonomy | `{0, −1, −7, −30, −365, −3650, +1}` (exact-integer; `487dadb`) |
| Locked output window | `[2013-04-01, 2022-12-31]` (`7780a97` §6.8 / no-2023+ posture at `0ddbd51`) |
| Merge gate | blocked until 10/10 chunks succeed per `5962c20` §9.1.2 |
| Step 2 / market-data firewall | active and not retired |

## Purpose

This memo prepares the **future live execution envelope** for `chunk_2015` only — the third of 10 yearly fetch-file chunks per the chunk-design memo `5962c20`. It defines the enable / single live run / restore / post-chunk-report sequence in design-level detail, the stop conditions, the expected successful output, the halt output, the boundary statement, the prior-chunk continuity protections for **both** completed chunks, and the runtime calibration. It is a **planning artifact for review**, not an execution authorization.

Explicitly:

- This memo does **not** execute `chunk_2015`.
- This memo does **not** enable any guard.
- This memo does **not** authorize GDELT contact by itself.
- This memo does **not** authorize merge.
- This memo does **not** authorize Step 2 or market-data logic.
- This memo does **not** touch market data.
- This memo does **not** retire the no-market-data firewall.
- This memo does **not** authorize retries, checkpoint/resume, off-session execution, or bounded parallelism.
- This memo does **not** authorize re-running `chunk_2013_partial` or `chunk_2014`.
- This memo does **not** authorize bundling chunks 2016 through 2022.

A separate review, separate commit, separate memory update, and separate live-execution-authorization prompt are still required before any `chunk_2015` execution.

## Target chunk facts

Verified from the runner at HEAD `770f982` (runner byte-identical to `389747e`'s committed version; verified empty `git diff 389747e HEAD -- scripts/run_lane2_gdelt1_full_daily_count_build.py`):

| Item | Value | Source |
|---|---|---|
| Target chunk | `chunk_2015` | runner canonical chunk list |
| Date range | `2015-01-01` through `2015-12-31` (inclusive) | `CHUNK_DATE_RANGES["chunk_2015"]` runner line 1543: `(date(2015, 1, 1), date(2015, 12, 31))` |
| Calendar days in range | `365` (2015 is not a leap year) | calendar arithmetic |
| Known 2015 substrate gaps | **none** (`KNOWN_SUBSTRATE_GAPS` contains only the four 2014 dates `2014-01-23` / `2014-01-24` / `2014-01-25` / `2014-03-19`; none intersect the 2015 range) | runner lines 125–130 |
| Count arithmetic | `365 calendar days − 0 known 2015 substrate gaps = 365` | derived |
| Runner-recorded expected count | `EXPECTED_CHUNK_COUNTS["chunk_2015"] = 365` | runner line 1530 |
| Cross-check | calculated `365` matches runner-recorded `365` — agree | derived |

`chunk_2015` is therefore a **zero-2015-gap, full-calendar-year, 365-URL chunk** — the first chunk in the execution sequence where no substrate-gap exclusions apply to the chunk's own date range.

## Runner anchor verification

Exact current line numbers discovered in this turn (HEAD `770f982`):

| Anchor | File:line | Current content |
|---|---|---|
| Chunk-runner module guard | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95` | `FULL_BUILD_AUTHORIZED = False` |
| Era-cutoff constant | `scripts/run_lane2_gdelt1_full_daily_count_build.py:116` | `SEAL_START = date(2023, 1, 1)` |
| Substrate-gap tuple opening line | `scripts/run_lane2_gdelt1_full_daily_count_build.py:125` | `KNOWN_SUBSTRATE_GAPS: Tuple[str, ...] = (` (4-element tuple at lines 126–129, closing `)` at line 130) |
| Canonical chunk-list entry for `chunk_2015` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1517` | `"chunk_2015",` |
| `EXPECTED_CHUNK_COUNTS["chunk_2015"]` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1530` | `"chunk_2015": 365,` |
| `chunk_2015` date-range tuple | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1543` | `"chunk_2015": (date(2015, 1, 1), date(2015, 12, 31)),` |
| `ALLOWED_CHUNK_OUTPUT_BASENAMES` opening line | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1554` | `ALLOWED_CHUNK_OUTPUT_BASENAMES: Tuple[str, ...] = (` — contains `chunk_contributions.csv`, `chunk_metadata.json`, `chunk_summary.md`, `halt_diagnostic.json` |
| `chunk_manifest_digest` function | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1609` | `def chunk_manifest_digest(chunk_iso_dates: List[str]) -> str:` |
| `substrate_gap_diagnostic` construction (twice: halt-path and success-path) | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1349–1351` (halt-path) and `2011–2013` (success-path) | Both surface the **global** `KNOWN_SUBSTRATE_GAPS` list unconditionally — see the "Substrate-gap diagnostic" note below |

## Substrate-gap diagnostic shape for `chunk_2015`

**Important finding from runner inspection** (not in the prior `chunk_2014` planning memo because both 2014 surfaces happened to agree on the full global list):

The runner constructs `substrate_gap_diagnostic` by writing the **global** `KNOWN_SUBSTRATE_GAPS` list to both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` unconditionally, regardless of the chunk's own date range (runner lines 1349–1351 halt-path, lines 2011–2013 success-path). It is **not** a per-chunk intersection.

Therefore, for `chunk_2015`, the expected `substrate_gap_diagnostic` in `chunk_metadata.json` is:

```
substrate_gap_diagnostic = {
    "known_substrate_gap_dates":         ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"],
    "substrate_gap_dates_not_fetched":   ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
}
```

**Not** `[]` / `[]`. This is the correct expected shape for the `chunk_2015` success path. The future execution prompt and post-chunk report must use this exact expected list, not an empty baseline.

Semantic interpretation: the four 2014 dates have no daily URL in the recognized list, so they are not fetched by **any** chunk. For `chunk_2014` they fell within the chunk's date range and were correctly excluded from the manifest. For `chunk_2015` they fall outside the chunk's date range entirely, but the runner still records them in the diagnostic as the global substrate-gap set. The forward-note shape recorded in the prior memory update — "for a future zero-known-gap chunk both surfaces should be empty" — was anticipated but **does not hold for `chunk_2015` under the current runner implementation**, because the runner surfaces the global list rather than a per-chunk intersection. This memo records the correct expected shape so the chunk_2015 cycle does not flag a false anomaly.

## Inherited locked rules

The future execution prompt and the live run it authorizes will inherit all of the following locked premises without re-litigation:

- **Recognized-list authority** (`84ea721e…fff835fc`): only daily URLs derived from the §10 capture, filtered to `chunk_2015`'s year range, may be fetched.
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
- **Per-chunk output is NOT the final canonical `daily_count.csv`**: the merge step is the only producer of `daily_count.csv` + `build_metadata.json` + `build_summary.md` + manifests, separately authorized later (`5962c20` §14 step 6).
- **Merge remains blocked until all 10 chunks succeed** (`5962c20` §9.1.2): a successful `chunk_2015` would advance progress to 3 of 10, not unblock merge.
- **`c10ae74` coverage-domain amendment**: 7-entry closed `coverage_quality_flag` domain including `t_minus_n_neighbor_substrate_gap`; `+`-joined multi-cause representation (`bc7b66b`).

## Chunk manifest expectation

The future live run for `chunk_2015` will fetch:

- **Only daily publishing-file URLs** with nominal date in `[2015-01-01, 2015-12-31]` inclusive.
- **Exactly `365` URLs** (verified by `EXPECTED_CHUNK_COUNTS["chunk_2015"] = 365` in the runner; `build_chunk_manifest` will hard-fail if the actual count differs).
- **Zero yearly recognized units** (the 2-element yearly subset of the recognized list is excluded by the daily-only regex filter).
- **Zero monthly recognized units** (the 87-element `YYYY-MM` subset is excluded by the same filter).
- **Zero 2023+ URLs** (the year range stops at `2015-12-31`; `date_to_daily_url` enforces a redundant `SEAL_START` precondition check).
- **Zero substrate-gap exclusions inside the chunk's own date range** (no 2015 dates appear in `KNOWN_SUBSTRATE_GAPS`).

The runner will compute the chunk manifest **digest** at execution time as `chunk_manifest_digest(chunk_iso_dates)` (`scripts/run_lane2_gdelt1_full_daily_count_build.py:1609`): sorted ASCII-encoded URLs joined by `\n`, then SHA-256. The digest is recorded in `chunk_metadata.json` for later cross-check by the merge step. The `chunk_2015` digest is **not** computable in advance from this planning memo and will be a new value distinct from `chunk_2013_partial`'s `6ac92439…bfc8b43` and `chunk_2014`'s `93f97096…994aba`.

Chunk output must contain **derived-only** artifacts (per `5962c20` §8 and `c10ae74` Decision 2A):

- `chunk_contributions.csv` — per-SQLDATE per-offset in-window contributions for this chunk only.
- `chunk_metadata.json` — provenance (chunk_id, source recognized-list SHA, chunk manifest digest, `expected_file_count = 365`, `actual_completed_file_count`, script anchor, guard state, started/finished UTC, `no_retry_confirmation`, boundary_declarations, per-URL manifest, substrate-gap diagnostic, out-of-window SQLDATE diagnostic, parser-anomaly diagnostic, output allow-list).
- `chunk_summary.md` — human-readable summary.
- `halt_diagnostic.json` — only on hard-fail paths; derived metadata only.

**No raw payload bytes** in any artifact. **No extracted CSV rows** in any artifact. **No SQLDATE values per individual event row** — only per-SQLDATE per-offset aggregate counts.

## Prior-chunk continuity envelope

The future `chunk_2015` live execution must protect **both** completed chunks. The envelope below must be re-verified by the live execution prompt at four checkpoints: before enabling the guard (preflight), after the live run (post-run), after report creation, and after push (final).

### `chunk_2013_partial`

| Item | Value |
|---|---|
| Tracked report | `docs/lane2_gdelt1_full_build_chunk_2013_partial_execution_report_v0.1.md` (commit `065d4754f69e2c35eef1ebdb7e4bf960ca9e806b` / short `065d475`) |
| Output directory | `results/lane2_gdelt1_full_daily_count_build/chunk_2013_partial_20260524T135157Z/` (untracked by default; not committed) |
| `chunk_contributions.csv` | `17,642 B` / SHA-256 `9f07c8018c322027841dbf6484f19c2218d2945731e775b9ced03099cfa37247` |
| `chunk_metadata.json` | `214,857 B` / SHA-256 `14a407a49e53f660a581bcdc7cee224e3228046aa1ea51eaae5e7eb5dc8a03c1` |
| `chunk_summary.md` | `440 B` / SHA-256 `9e88e95cc33e4f99ddc3a810db23cd076ac51928d7504b7bab35780d5d15ed42` |
| `chunk_manifest_digest` | `6ac92439455d3f59df64cfeca6256f54a319c0ac82d40886f11b26becbfc8b43` |

### `chunk_2014`

| Item | Value |
|---|---|
| Tracked report | `docs/lane2_gdelt1_full_build_chunk_2014_execution_report_v0.1.md` (commit `770f982afdf736575a8bdfdd1b8ef57c4fc6f578` / short `770f982`) |
| Output directory | `results/lane2_gdelt1_full_daily_count_build/chunk_2014_20260524T150055Z/` (untracked by default; not committed) |
| `chunk_contributions.csv` | `32,908 B` / SHA-256 `2ffd56fbd039ef5e7825c048358d7dc0a0b1e6f24d3d8614902de6217ce43660` |
| `chunk_metadata.json` | `265,975 B` / SHA-256 `e0a944e38204d3fa6deb904d1b71b1a465a284c8203d75c025df372c80fd69d6` |
| `chunk_summary.md` | `424 B` / SHA-256 `93db53b075e0e15bf1e91d5a4b41a75eb03695925aa5ff0e8a7ceae5c5c3459d` |
| `chunk_manifest_digest` | `93f9709656cb30252e1a9e5a8167dadb17b4f63bbb58ac6e4f4405b593994aba` |

### Continuity-check requirements

The future `chunk_2015` execution prompt must verify all six prior artifact SHA-256 values, both output directory paths (and the absence of any rename / move / deletion), and the byte-identicality of both tracked reports against their committed states (`065d475` and `770f982`) at four checkpoints:

- **preflight** (before enabling the guard);
- **post-run** (immediately after guard restore, before output verification mutates state);
- **after report creation** (post-write, pre-stage);
- **after push** (final).

No `chunk_2015_*` subdirectory may pre-exist inside `results/lane2_gdelt1_full_daily_count_build/` before the live run (the runner's `os.makedirs(..., exist_ok=False)` would hard-fail on collision). The `chunk_2015` execution must not touch either prior output directory in any way (read-only continuity preservation is sufficient and required).

## Runtime calibration

Observed runtimes:

| Chunk | URLs | Wall-clock runtime | Per-URL rate |
|---|---|---|---|
| `chunk_2013_partial` | 275 | ~8m 20s | ~1.8 s/URL |
| `chunk_2014` | 361 | ~13m 44s | ~2.28 s/URL |

`chunk_2014` was ~27% slower per URL than `chunk_2013_partial`. Use **~2.3 s/URL as the conservative planning anchor** unless later evidence supersedes it.

**Projected `chunk_2015` runtime**: `365 URLs × 2.3 s/URL ≈ 839.5 s ≈ 13m 59.5s ≈ ~14m`. This sits comfortably above the 10-minute Bash foreground tool ceiling, so **same-session background execution via Bash tool `run_in_background=true` with harness completion capture remains the default and is reinforced** for the future live execution prompt.

Explicit non-weakening declarations (this calibration is record-only):

- This calibration does NOT weaken the **no-retry** rule.
- This calibration does NOT weaken **exactly-once fetch semantics**.
- This calibration does NOT weaken **no-off-session** execution.
- This calibration does NOT weaken **no-market-data** firewall.
- This calibration does NOT weaken **no-Step-2**.
- This calibration does NOT weaken **no-checkpoint/resume**.
- This calibration does NOT weaken **no-bounded-parallelism**.

## Future execution sequence

The future `chunk_2015` execution prompt (separately initiated; **NOT** authorized by this plan) will perform the following steps in order:

1. **Preflight read-only verification**. Confirm: `HEAD = origin/main = 770f982` (or its accepted successor if intervening memory updates / planning memos have landed); ahead = `0`; tracked tree clean; all five guards `False` on disk; production `results/lane2_gdelt1_full_daily_count_build/` exists (contains the prior `chunk_2013_partial_20260524T135157Z/` and `chunk_2014_20260524T150055Z/` subdirectories) but does not contain a colliding `chunk_2015_<UTC_TIMESTAMP>/` subdirectory; recognized-list SHA `84ea721e…fff835fc` intact; F4 baselines intact; chunk-runner source byte-identical to its current committed state (and to `389747e`); both prior chunks' six artifact SHAs and both tracked reports unmodified; memory mtimes pinned per the most recent memory update.
2. **Enable commit**: flip `FULL_BUILD_AUTHORIZED = False → True` on **line 95** of `scripts/run_lane2_gdelt1_full_daily_count_build.py` via a single one-line edit. Subject: **`Enable Lane 2 full-build chunk_2015 run`**. Numstat `1\t1`. Mirrors `c6b313c` and `574ce77` enable precedent.
3. **Single live run** of exactly one shell command (inline env var only, no `export`):
   ```
   LANE2_FULL_BUILD_AUTHORIZED=1 python3 scripts/run_lane2_gdelt1_full_daily_count_build.py \
     --authorize-full-build-run --chunk-id chunk_2015
   ```
   Capture stdout, stderr, exit code, start UTC, end UTC, output directory path. The runner is expected to create `results/lane2_gdelt1_full_daily_count_build/chunk_2015_<UTC_TIMESTAMP>/` and write `chunk_contributions.csv` + `chunk_metadata.json` + `chunk_summary.md` (success path) or `halt_diagnostic.json` (halt path) + the partial allowable artifacts. The env var `LANE2_FULL_BUILD_AUTHORIZED` must be `UNSET` after the run command's process exits.
   **Execution mode**: same-session in-session background execution via Bash tool `run_in_background=true` with harness completion capture (mirroring the proven `chunk_2013_partial` `bgzz8eqe5` and `chunk_2014` `blywiekhg` patterns). Same-session, **not** off-session. Justification: the runtime calibration above projects ~14 min for 365 URLs at ~2.3 s/URL, above the 10-min Bash foreground tool ceiling, so background-in-session avoids tool-layer-kill orphaning while preserving deterministic exit-status reporting.
4. **Restore commit**: flip line-95 back to `False`. Subject: **`Restore Lane 2 full-build guard after chunk_2015`**. Same `1\t1` numstat. Runner byte-identical to `389747e` post-restore (verify via empty `git diff 389747e HEAD -- scripts/run_lane2_gdelt1_full_daily_count_build.py`). Restore happens **regardless of success or halt** of the live run.
5. **Verify all five guards `False` after restore** via `grep -nE "^(REAL_RETRIEVAL_ENABLED|COUNT_FEASIBILITY_AUTHORIZED|EVENT_FILE_PROBE_AUTHORIZED|ROW_DATE_CHARACTERIZATION_AUTHORIZED|FULL_BUILD_AUTHORIZED) = "`; all four `LANE2_*_AUTHORIZED` shell envs `UNSET`.
6. **Verify output-artifact allow-list**: only files from `ALLOWED_CHUNK_OUTPUT_BASENAMES` (runner line 1554) — `{chunk_contributions.csv, chunk_metadata.json, chunk_summary.md, halt_diagnostic.json}`. No `.zip` / `.CSV` / `tmp_*` / subdirectories.
7. **Verify prior-chunk continuity post-run**: re-compute all six SHA-256 values for the two prior chunks' artifacts and confirm both tracked reports unchanged.
8. **Write a tracked post-chunk execution report** at `docs/lane2_gdelt1_full_build_chunk_2015_execution_report_v0.1.md`, mirroring the `chunk_2014` report at `770f982`. The report records: preflight state; enable-commit SHA; live-run command verbatim + timeout/background strategy + start/end UTC + exit code + stdout/stderr summary + harness shell ID; output directory path; chunk manifest digest; URL count (expected 365 / actual N); per-URL summary (HTTP status, SHA-256, row count, offset distribution); aggregate in-window/out-of-window row counts; per-offset totals; parser anomalies; substrate-gap diagnostic (expected `["2014-01-23","2014-01-24","2014-01-25","2014-03-19"]` in both surfaces, per the runner-implementation note above); halt class + diagnostic SHA if halted; restore-commit SHA; post-restore guard state; output artifact SHA-256 manifest; boundary confirmations; prior-chunk continuity confirmation for **both** `chunk_2013_partial` and `chunk_2014`.
9. **Commit cycle**: three commits in order — `Enable Lane 2 full-build chunk_2015 run` → `Restore Lane 2 full-build guard after chunk_2015` → `Record Lane 2 chunk_2015 execution report`. Push only after the restore commit and report commit both exist and all guards are `False` on disk. Mirrors the `chunk_2013_partial` and `chunk_2014` cycles exactly.

## Future commit subjects and report path

| Step | Subject | Future file |
|---|---|---|
| Enable | `Enable Lane 2 full-build chunk_2015 run` | (no new file) |
| Restore | `Restore Lane 2 full-build guard after chunk_2015` | (no new file) |
| Report | `Record Lane 2 chunk_2015 execution report` | **`docs/lane2_gdelt1_full_build_chunk_2015_execution_report_v0.1.md`** |

## Future output policy

- Successful per-chunk outputs remain **untracked by default** (Decision 3A `0065d10` + §8.2 `5962c20` + `chunk_2013_partial` `065d475` + `chunk_2014` `770f982` precedent).
- Output artifacts must **not** be committed.
- The tracked report records output directory path, artifact sizes, SHA-256 hashes, validation facts, runtime, gap diagnostics, and boundary checks.
- **No raw payload preservation.**
- **No `.zip` / extracted CSV preservation.**
- **No merge artifacts.**

## Expected future validation checks

The future `chunk_2015` execution prompt must verify:

- `actual_completed_file_count == expected_file_count == 365`.
- `chunk_manifest_digest` is recorded (new value, distinct from `6ac92439…bfc8b43` and `93f97096…994aba`).
- `source_recognized_list_sha256 == 84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`.
- `no_retry_confirmation == True`.
- `substrate_gap_diagnostic` matches the 2015-specific expected shape per the "Substrate-gap diagnostic shape for `chunk_2015`" section above: both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` equal `["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]` (the global `KNOWN_SUBSTRATE_GAPS` list, surfaced unconditionally by the runner). Do **not** expect `[]`.
- `boundary_declarations` all `True` (`no_2023plus_access`, `no_asset_or_return_logic`, `no_category_theme_actor_filtering`, `no_market_calendar_alignment`, `no_market_data`, `no_negative_control`, `no_payload_preservation_after_parsing`, `no_spike_threshold_tuning`, `no_step_2`).
- No `halt_diagnostic.json` on success.
- No raw payloads.
- No `.zip` / extracted CSV.
- No merge artifacts.
- All five guards `False` after restore (with explicit file:line citations).
- `LANE2_*_AUTHORIZED` shell envs unset after run.
- `chunk_2013_partial` and `chunk_2014` continuity preserved (all six prior artifact SHAs unchanged, both tracked reports byte-identical to their committed copies).

## Stop conditions

Hard stop conditions the future `chunk_2015` execution prompt must enforce. Any single one halts the cycle.

### Preflight / procedurally enforced (execution does not begin)

- HEAD ≠ accepted ancestor (e.g., not `770f982` or a successor reviewed and recorded in memory).
- `origin/main` mismatch with HEAD.
- Tracked tree dirty (any `M`/`A`/`D`/`R` entries from `git status --porcelain`, ignoring pre-existing untracked items).
- Any staged files pre-enable.
- Any of the five guards is already `True` on disk pre-enable.
- Any `LANE2_*_AUTHORIZED` shell env is set pre-enable.
- Recognized-list SHA mismatch with `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`.
- F4 baseline SHA mismatch with `41c80c0…624c39d` or `00ce9b2…f5e37552c`.
- Memory mtime drift if the future prompt pins memory mtimes.
- Target post-chunk report `docs/lane2_gdelt1_full_build_chunk_2015_execution_report_v0.1.md` already exists pre-write.
- Existing `chunk_2015_<UTC_TIMESTAMP>/` subdirectory inside `results/lane2_gdelt1_full_daily_count_build/` (runner's `os.makedirs(..., exist_ok=False)` would hard-fail on collision).
- `chunk_2013_partial` output directory, any of its three artifacts, or its tracked report missing, renamed, or SHA-256-mutated.
- `chunk_2014` output directory, any of its three artifacts, or its tracked report missing, renamed, or SHA-256-mutated.
- Chunk-runner source file diverges from `389747e`'s committed state pre-enable.
- Inability to run the live command via same-session background execution with captured exit status / stdout / stderr / start UTC / end UTC.

### Runner-internal / machine-enforced (during the live run; `run_chunk_build` raises and `_write_chunk_halt_diagnostic` writes the halt artifact, then `raise` re-raises)

- Chunk manifest actual count ≠ `365` (`ChunkManifestError` from `build_chunk_manifest`).
- Recognized-list SHA mismatch at runtime (`RecognizedListSchemaError`).
- Reconciliation contradiction (`ReconciliationContradiction`).
- HTTP non-200 for any in-chunk URL (`FetchFailure` via `_fetch_one_payload`).
- Redirect (any 3xx) for any in-chunk URL (`FullBuildRedirectBlocked` → translated to `FetchFailure`).
- Connection error / timeout for any in-chunk URL (`FetchFailure`).
- Unexpected offset outside `{0, −1, −7, −30, −365, −3650, +1}` for any parsed row (`FullBuildBoundaryBreach`).
- 2023+ SQLDATE in any parsed row (`FullBuildBoundaryBreach`).
- 2023+ URL construction attempt (`FullBuildBoundaryBreach` via `date_to_daily_url` precondition).
- Output allow-list violation (`FullBuildBoundaryBreach`).
- Counting-invariant violation (`FullBuildBoundaryBreach`).

### Post-run / defense-in-depth (block report commit / push)

- Inability to restore `FULL_BUILD_AUTHORIZED = False`. **Guard restoration on disk is the highest priority** if anything fails post-run, unless the repo state itself prevents restoration.
- Any guard `True` on disk after the restore commit.
- Any raw payload bytes (`.zip`) present in the `chunk_2015` output directory.
- Any extracted CSV rows (`.CSV`) present in the `chunk_2015` output directory.
- Any output outside `ALLOWED_CHUNK_OUTPUT_BASENAMES`.
- Any retry attempt observed in the runner's per-URL manifest.
- Any second-GET attempt for the same URL.
- Any accidental market-data / Step 2 / spike-burst / return-window logic.
- Any modification to either prior chunk's output (SHA-256 mismatch on any of the six prior artifacts) or report (byte-divergence from committed copy).
- Any accidental next-chunk run (e.g., a `chunk_2016` directory appearing).
- Any accidental merge run (e.g., top-level `daily_count.csv` / `build_metadata.json` / `build_summary.md` appearing).
- `substrate_gap_diagnostic` does not match the runner-implementation-expected shape `["2014-01-23","2014-01-24","2014-01-25","2014-03-19"]` in both surfaces (this would indicate a runtime change to the runner, not a chunk-data anomaly).

Any halt condition triggers the **session-interruption recovery rule**: restore the guard, preserve partial output as-is, emit verdict `FULL-BUILD CHUNK_2015 RUN HALTED — AWAIT ADJUDICATION`.

## Outcome classes for future live execution

The future execution prompt must classify its outcome as exactly one of:

- **SUCCESS** — runner exits with code 0; three success artifacts present; `actual = expected = 365`; substrate-gap diagnostic matches expected; both prior chunks' continuity preserved.
- **BLOCKED BEFORE ENABLE** — a preflight check failed; no guard flip occurred.
- **LIVE RUN FAILURE** — runner exit non-zero, halt class identified, `halt_diagnostic.json` may exist.
- **OUTPUT VERIFICATION FAILURE** — runner exited cleanly but the produced output set / SHAs / metadata do not match the success contract.
- **PRIOR CHUNK CONTINUITY FAILURE** — `chunk_2013_partial` or `chunk_2014` artifacts / reports changed during the cycle.
- **GUARD RESTORE FAILURE** — line-95 could not be restored to `False`.
- **INFRASTRUCTURE FAILURE / SUBPROCESS STATE AMBIGUOUS** — tool-layer timeout / abort / interruption; subprocess may have been running when guard restore proceeded.
- **INFRASTRUCTURE FAILURE / SUBPROCESS STATE UNKNOWN** — subprocess state could not be reliably established.

**Guard restoration must be prioritized after any enable commit, regardless of live-run success or failure, unless the repo state itself prevents restoration.** Push must not proceed while the guard remains enabled.

## Substrate progress projection

If `chunk_2015` succeeds with `actual_completed_file_count = 365`:

| Metric | Before `chunk_2015` | Projected after `chunk_2015` |
|---|---|---|
| Chunks complete | 2 / 10 | **3 / 10** |
| Completed chunks list | `chunk_2013_partial`, `chunk_2014` | `chunk_2013_partial`, `chunk_2014`, `chunk_2015` |
| Daily URLs complete | 636 / 3,558 | **1,001 / 3,558** (= 636 + 365) |
| Percent complete by URL count | ~17.9% | ~**28.1%** |
| Remaining daily URLs | 2,922 | **2,557** |
| Remaining chunks | 8 | **7** (`chunk_2016` through `chunk_2022`) |

Merge remains blocked until 10/10 chunks succeed per `5962c20` §9.1.2. Chunks `chunk_2016` through `chunk_2022` each require their own separately authorized execution prompt; this cycle does not authorize them.

## Boundary statement

This plan authorizes **none** of the following:

- Live execution of `chunk_2015` or any other chunk.
- GDELT contact.
- Guard flip on any runner (the five guards remain `False` on disk and the four `LANE2_*_AUTHORIZED` shell envs remain `UNSET` throughout the planning turn).
- Retry of any URL.
- Checkpoint/resume implementation.
- Off-session execution.
- Bounded parallelism.
- Merge execution.
- Market data of any kind.
- Step 2 of any kind.
- No-market-data firewall retirement.
- No-2023+ posture change.
- Output-artifact mutation (both prior chunks' output directories remain untouched read-only; the pre-existing `results/lane2_gdelt1_event_file_probe/`, `results/lane2_gdelt1_row_date_characterization/`, `results/lane2_gdelt1_count_feasibility/` directories also untouched).
- Recognized-list mutation (`84ea721e…fff835fc` preserved).
- F4 mutation (baselines preserved).
- Memory edit.
- Code edit (`scripts/`, `src/`, `tests/` byte-identical to `770f982`).
- Test edit.
- Re-running `chunk_2013_partial` or `chunk_2014` or any other chunk.
- Running any chunk other than `chunk_2015`.
- Locked-memo edit to `9319d30` / `a8a9dd2` / `a2a8fd5` / `e9f8781` / `487dadb` / `3537a62` / `73a7911` / `858b501` / `0065d10` / `7780a97` / `bc7b66b` / `c10ae74` / `d7c8775` / `fbc605b` / `5962c20` / `389747e` / `447656d` / `c6b313c` / `167a08a` / `065d475` / `4276b30` / `574ce77` / `13f14ba` / `770f982` / `e55e09a` / `0b341b4` / `845c51c` / `e81208d` / `7c85e3f`.
- Staging / commit / push of this plan or any other artifact (the plan's commit is a separately authorized follow-up step, NOT part of this planning turn).

The no-market-data firewall, no-2023+ posture, no-retry rule, exactly-once fetch semantics, no-merge-until-10/10 rule, recognized-list authority, SQLDATE re-keying, and the locked design contract from `7780a97` as amended by `c10ae74` + the chunk-design contract from `5962c20` all remain in force.

## Decision points before live execution

All decision points from prior cycles are resolved by precedent for `chunk_2015`:

| Decision point | Resolution by precedent |
|---|---|
| Chunk-output artifact disposition | **Untracked by default** per `0065d10` Decision 3A + `5962c20` §8.2; reaffirmed by `chunk_2013_partial` (`065d475`) and `chunk_2014` (`770f982`) cycles. |
| Commit sequence | **Three commits: Enable → Restore → Report.** Reaffirmed by both prior cycles. |
| Post-chunk report commit timing | **Report committed standalone** (output untracked); resolves automatically. |
| Timeout / subprocess strategy | **In-session background execution via Bash `run_in_background=true`** with harness completion capture; mirrors `bgzz8eqe5` and `blywiekhg`; same-session, **not** off-session; justified by the ~14 min runtime projection above the 10-min Bash foreground ceiling. |
| Output-directory timestamping | Runner-controlled via `chunk_2015_<UTC_TIMESTAMP>/`; collision handled by `os.makedirs(..., exist_ok=False)`. |
| Substrate-gap diagnostic surfacing | Runner surfaces the **global** `KNOWN_SUBSTRATE_GAPS` list in both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` unconditionally (lines 1349–1351, 2011–2013); the expected `chunk_2015` shape is the four 2014 dates in both fields, not `[]`. |

Precedent citations:

- `0065d10 Decision 3A` — untracked-by-default for per-cycle output artifacts.
- `5962c20 §8.2` — chunk-design memo's untracked-by-default codification.
- `chunk_2013_partial` execution at `065d475` (chain `c6b313c → 167a08a → 065d475`).
- `chunk_2014` execution at `770f982` (chain `574ce77 → 13f14ba → 770f982`).

## Next steps after this memo

The next procedural steps after this planning memo's creation are, in order:

- **Sanity-check review** of the planning memo (read-only, by the user or a separately invoked review-only prompt). If review surfaces issues, a corrective revision of this plan precedes the commit prompt.
- **Separate explicit commit prompt** (no commit is authorized by this planning-memo-creation turn).
- **Separate memory-update prompt for the planning closure** (after commit/push lands).
- **Only then**, a separate live `chunk_2015` execution-authorization prompt (which performs the steps in §"Future execution sequence" above).

**No execution is authorized by this planning memo creation turn.** Its persistence scope is complete upon writing the single file at `docs/lane2_gdelt1_full_build_chunk_2015_execution_authorization_plan_v0.1.md`. No review, no staging, no commit, no push, no memory update, no live execution, no guard flip, no GDELT contact, no merge, no market data, and no Step 2 work is authorized by this turn.
