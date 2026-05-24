# Lane 2 GDELT1 chunk_2016 execution-authorization plan v0.1

## Title

`Lane 2 GDELT1 chunk_2016 execution-authorization plan v0.1`

This memo is **planning-only**. It does not by itself execute `chunk_2016`, enable any guard, authorize GDELT contact, authorize merge, authorize Step 2, touch market data, or retire the no-market-data firewall. A separate review of this plan, a separate commit, a separate memory-update prompt for the planning closure, and a separate live-execution-authorization prompt are all still required before any `chunk_2016` execution. Its persistence scope is one tracked file at `docs/lane2_gdelt1_full_build_chunk_2016_execution_authorization_plan_v0.1.md`.

## Current canonical state

| Item | Value |
|---|---|
| `HEAD = origin/main` at planning creation | `ed4e74cc1a7b19d425dd474371b936491d38a056` |
| Short SHA | `ed4e74c` |
| Ahead / behind | `0 / 0` |
| Latest execution-cycle commit chain (closing `chunk_2015`) | enable `14c2f6b` → restore `083649b` → report `ed4e74c` |
| Planning-memo commit chain so far | `chunk_2013_partial` plan `447656d` → `chunk_2014` plan `4276b30` → `chunk_2015` plan `f4590eb` |
| Substrate progress before `chunk_2016` | **3 / 10 chunks complete**; 1,001 / 3,558 daily URLs complete (≈ 28.1%); 2,557 daily URLs + 7 chunks remaining |
| Completed chunks | `chunk_2013_partial`, `chunk_2014`, `chunk_2015` |
| Recognized-list authority SHA-256 | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` |
| F4 baseline SHAs (preserved) | `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d` / `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c` |
| Locked offset taxonomy | `{0, −1, −7, −30, −365, −3650, +1}` (exact-integer; `487dadb`) |
| Locked output window | `[2013-04-01, 2022-12-31]` (`7780a97` §6.8 / no-2023+ posture at `0ddbd51`) |
| Merge gate | blocked until 10/10 chunks succeed per `5962c20` §9.1.2 |
| Step 2 / market-data firewall | active and not retired |

## Purpose

This memo prepares the **future live execution envelope** for `chunk_2016` only — the fourth of 10 yearly fetch-file chunks per the chunk-design memo `5962c20`. It defines the enable / single live run / restore / post-chunk-report sequence in design-level detail, the stop conditions, the expected successful output, the halt output, the boundary statement, the prior-chunk continuity protections for **all three** completed chunks, and the runtime calibration. It is a **planning artifact for review**, not an execution authorization.

Explicitly:

- This memo does **not** execute `chunk_2016`.
- This memo does **not** enable any guard.
- This memo does **not** authorize GDELT contact by itself.
- This memo does **not** authorize merge.
- This memo does **not** authorize Step 2 or market-data logic.
- This memo does **not** touch market data.
- This memo does **not** retire the no-market-data firewall.
- This memo does **not** authorize retries, checkpoint/resume, off-session execution, or bounded parallelism.
- This memo does **not** authorize re-running `chunk_2013_partial`, `chunk_2014`, or `chunk_2015`.
- This memo does **not** authorize bundling chunks 2017 through 2022.

A separate review, separate commit, separate memory update, and separate live-execution-authorization prompt are still required before any `chunk_2016` execution.

## Target chunk facts

Verified from the runner at HEAD `ed4e74c` (runner byte-identical to `389747e`'s committed version; verified empty `git diff 389747e HEAD -- scripts/run_lane2_gdelt1_full_daily_count_build.py`):

| Item | Value | Source |
|---|---|---|
| Target chunk | `chunk_2016` | runner canonical chunk list |
| Date range | `2016-01-01` through `2016-12-31` (inclusive) | `CHUNK_DATE_RANGES["chunk_2016"]` at runner line 1544: `(date(2016, 1, 1), date(2016, 12, 31))` |
| Calendar days in range | `366` (**2016 IS a leap year** — one more day than chunk_2015) | calendar arithmetic |
| Known 2016 substrate gaps | **none** (`KNOWN_SUBSTRATE_GAPS` at runner lines 126–129 contains only the four 2014 dates `2014-01-23` / `2014-01-24` / `2014-01-25` / `2014-03-19`; none intersect the 2016 range) | runner lines 125–130 |
| Count arithmetic | `366 calendar days − 0 known 2016 substrate gaps = 366` | derived |
| Global `KNOWN_SUBSTRATE_GAPS` (full tuple) | `("2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19")` | runner lines 126–129 |
| Runner-recorded expected count | `EXPECTED_CHUNK_COUNTS["chunk_2016"] = 366` | runner line 1531 |
| Cross-check | calculated `366` matches runner-recorded `366` — agree | derived |

`chunk_2016` is therefore a **zero-2016-gap, full-calendar-year (leap), 366-URL chunk**. It is the second consecutive zero-in-range-gap chunk after `chunk_2015` and the first leap-year chunk in the execution sequence.

## Runner anchor verification

Exact current line numbers discovered in this turn (HEAD `ed4e74c`; runner byte-identical to `389747e`):

| Anchor | File:line | Current content |
|---|---|---|
| Chunk-runner module guard | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95` | `FULL_BUILD_AUTHORIZED = False` |
| Era-cutoff constant | `scripts/run_lane2_gdelt1_full_daily_count_build.py:116` | `SEAL_START = date(2023, 1, 1)` |
| Substrate-gap tuple opening line | `scripts/run_lane2_gdelt1_full_daily_count_build.py:125` | `KNOWN_SUBSTRATE_GAPS: Tuple[str, ...] = (` (4-element tuple at lines 126–129, closing `)` at line 130) |
| Substrate-gap tuple date entries | `scripts/run_lane2_gdelt1_full_daily_count_build.py:126–129` | `"2014-01-23"`, `"2014-01-24"`, `"2014-01-25"`, `"2014-03-19"` (in order) |
| Canonical chunk-list entry for `chunk_2016` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1518` | `"chunk_2016",` |
| `EXPECTED_CHUNK_COUNTS["chunk_2016"]` | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1531` | `"chunk_2016": 366,` |
| `chunk_2016` date-range tuple | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1544` | `"chunk_2016": (date(2016, 1, 1), date(2016, 12, 31)),` |
| `ALLOWED_CHUNK_OUTPUT_BASENAMES` opening line | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1554` | `ALLOWED_CHUNK_OUTPUT_BASENAMES: Tuple[str, ...] = (` — contains `chunk_contributions.csv`, `chunk_metadata.json`, `chunk_summary.md`, `halt_diagnostic.json` |
| `chunk_manifest_digest` function | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1609` | `def chunk_manifest_digest(chunk_iso_dates: List[str]) -> str:` |
| `substrate_gap_diagnostic` halt-path construction | `scripts/run_lane2_gdelt1_full_daily_count_build.py:1349–1351` | dict opener at 1349; `"known_substrate_gap_dates": list(KNOWN_SUBSTRATE_GAPS)` at 1350; `"substrate_gap_dates_not_fetched": list(KNOWN_SUBSTRATE_GAPS)` at 1351 |
| `substrate_gap_diagnostic` success-path construction | `scripts/run_lane2_gdelt1_full_daily_count_build.py:2011–2013` | dict opener at 2011; same two keys at 2012–2013 |

Line numbers `1518`, `1531`, `1544` are one greater than the corresponding `chunk_2015` line numbers (`1517`, `1530`, `1543`) — chunk_2016 follows chunk_2015 in the canonical list, counts dict, and date-range dict. All other anchors are unchanged across the chunk_2013_partial / chunk_2014 / chunk_2015 cycles.

## Substrate-gap diagnostic shape for `chunk_2016`

This is the load-bearing item established by the `f4590eb` planning correction and empirically validated by the live `chunk_2015` run.

The runner constructs `substrate_gap_diagnostic` by writing the **global** `KNOWN_SUBSTRATE_GAPS` list to both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` unconditionally, regardless of the chunk's own date range (runner lines 1349–1351 halt-path, lines 2011–2013 success-path). It is **not** a per-chunk intersection. **Empirically validated in the live `chunk_2015` run at `ed4e74c`**: both surfaces matched the global four-2014-date tuple exactly, not `[]`.

For `chunk_2016` (zero in-range 2016 gaps, but the runner is byte-identical to `389747e` and the global `KNOWN_SUBSTRATE_GAPS` tuple is unchanged), the expected `substrate_gap_diagnostic` in `chunk_metadata.json` is:

```
substrate_gap_diagnostic = {
    "known_substrate_gap_dates":         ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"],
    "substrate_gap_dates_not_fetched":   ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]
}
```

**Not** `[]` / `[]`. The future `chunk_2016` execution prompt and post-chunk report must validate this exact list in the exact expected order on both surfaces. If the runner implementation has changed between this planning memo and the live execution, the change must be explicitly reviewed and documented before execution; otherwise this is the canonical expected shape.

Semantic interpretation: the four 2014 dates have no daily URL in the recognized list, so they are not fetched by **any** chunk. For `chunk_2014` they fell within the chunk's date range and were correctly excluded from the manifest. For `chunk_2015` and `chunk_2016` they fall outside the chunk's date range entirely, but the runner still records them in the diagnostic as the global substrate-gap set. This applies for `chunk_2016` through `chunk_2022` unless the runner implementation itself changes.

## Inherited locked rules

The future execution prompt and the live run it authorizes will inherit all of the following locked premises without re-litigation:

- **Recognized-list authority** (`84ea721e…fff835fc`): only daily URLs derived from the §10 capture, filtered to `chunk_2016`'s year range, may be fetched.
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
- **Merge remains blocked until all 10 chunks succeed** (`5962c20` §9.1.2): a successful `chunk_2016` would advance progress to 4 of 10, not unblock merge.
- **`c10ae74` coverage-domain amendment**: 7-entry closed `coverage_quality_flag` domain including `t_minus_n_neighbor_substrate_gap`; `+`-joined multi-cause representation (`bc7b66b`).

## Chunk manifest expectation

The future live run for `chunk_2016` will fetch:

- **Only daily publishing-file URLs** with nominal date in `[2016-01-01, 2016-12-31]` inclusive.
- **Exactly `366` URLs** (verified by `EXPECTED_CHUNK_COUNTS["chunk_2016"] = 366` in the runner; `build_chunk_manifest` will hard-fail if the actual count differs).
- **Zero yearly recognized units** (the 2-element yearly subset of the recognized list is excluded by the daily-only regex filter).
- **Zero monthly recognized units** (the 87-element `YYYY-MM` subset is excluded by the same filter).
- **Zero 2023+ URLs** (the year range stops at `2016-12-31`; `date_to_daily_url` enforces a redundant `SEAL_START` precondition check).
- **Zero substrate-gap exclusions inside the chunk's own date range** (no 2016 dates appear in `KNOWN_SUBSTRATE_GAPS`).
- **One leap day** (`2016-02-29` is part of the 366-URL manifest).

The runner will compute the chunk manifest **digest** at execution time as `chunk_manifest_digest(chunk_iso_dates)` (`scripts/run_lane2_gdelt1_full_daily_count_build.py:1609`): sorted ASCII-encoded URLs joined by `\n`, then SHA-256. The digest is recorded in `chunk_metadata.json` for later cross-check by the merge step. The `chunk_2016` digest is **not** computable in advance from this planning memo and will be a new value distinct from `chunk_2013_partial`'s `6ac92439…bfc8b43`, `chunk_2014`'s `93f97096…994aba`, and `chunk_2015`'s `a5c61b06…bf17bd67`.

Chunk output must contain **derived-only** artifacts (per `5962c20` §8 and `c10ae74` Decision 2A):

- `chunk_contributions.csv` — per-SQLDATE per-offset in-window contributions for this chunk only.
- `chunk_metadata.json` — provenance (chunk_id, source recognized-list SHA, chunk manifest digest, `expected_file_count = 366`, `actual_completed_file_count`, script anchor, guard state, started/finished UTC, `no_retry_confirmation`, boundary_declarations, per-URL manifest, substrate-gap diagnostic, out-of-window SQLDATE diagnostic, parser-anomaly diagnostic, output allow-list).
- `chunk_summary.md` — human-readable summary.
- `halt_diagnostic.json` — only on hard-fail paths; derived metadata only.

**No raw payload bytes** in any artifact. **No extracted CSV rows** in any artifact. **No SQLDATE values per individual event row** — only per-SQLDATE per-offset aggregate counts.

## Prior-chunk continuity envelope

The future `chunk_2016` live execution must protect **all three** completed chunks. The envelope below must be re-verified by the live execution prompt at four checkpoints: before enabling the guard (preflight), after the live run (post-run), after report creation, and after push (final).

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

### `chunk_2015`

| Item | Value |
|---|---|
| Tracked report | `docs/lane2_gdelt1_full_build_chunk_2015_execution_report_v0.1.md` (commit `ed4e74cc1a7b19d425dd474371b936491d38a056` / short `ed4e74c`) |
| Output directory | `results/lane2_gdelt1_full_daily_count_build/chunk_2015_20260524T163556Z/` (untracked by default; not committed) |
| `chunk_contributions.csv` | `36,820 B` / SHA-256 `7f7307be58e450190db5925cbc69861b95a827bbf279598a9eccecf549301ea2` |
| `chunk_metadata.json` | `264,289 B` / SHA-256 `a73d5a252610c8610d22d579cbef18e8a58338a7985dac56d9f4d1fe5158d4e2` |
| `chunk_summary.md` | `424 B` / SHA-256 `2de7dd3595d340d31c27993e416204050c1734dfd4d6ebd137f21c7135d5b2f9` |
| `chunk_manifest_digest` | `a5c61b06dee77a9916db6725cabe3a41d74d47d5807dce6ca2be1709bf17bd67` |

### Continuity-check requirements

The future `chunk_2016` execution prompt must verify **all nine** prior artifact SHA-256 values, **all three** output directory paths (and the absence of any rename / move / deletion), and the byte-identicality of **all three** tracked reports against their committed states (`065d475`, `770f982`, `ed4e74c`) at four checkpoints:

- **preflight** (before enabling the guard);
- **post-run** (immediately after guard restore, before output verification mutates state);
- **after report creation** (post-write, pre-stage);
- **after push** (final).

No `chunk_2016_*` subdirectory may pre-exist inside `results/lane2_gdelt1_full_daily_count_build/` before the live run (the runner's `os.makedirs(..., exist_ok=False)` would hard-fail on collision). The `chunk_2016` execution must not touch any of the three prior output directories in any way (read-only continuity preservation is sufficient and required).

## Runtime calibration

Observed runtimes:

| Chunk | URLs | Wall-clock runtime | Per-URL rate | Slowdown vs prior |
|---|---|---|---|---|
| `chunk_2013_partial` | 275 | ~8m 20s | ~1.8 s/URL | — |
| `chunk_2014` | 361 | ~13m 44s | ~2.28 s/URL | ~27% slower vs chunk_2013_partial |
| `chunk_2015` | 365 | ~16m 54s | ~2.78 s/URL | ~22% slower vs chunk_2014; ~54% slower vs chunk_2013_partial |

A monotonic slowdown trend is now visible across three chunks. Use **`~2.8 s/URL` as the conservative planning anchor** unless later evidence supersedes it.

**Projected `chunk_2016` runtime**: `366 URLs × 2.8 s/URL ≈ 1,024.8 s ≈ 17m 4.8s ≈ ~17m 5s`. This sits ~70% above the 10-minute Bash foreground tool ceiling, so **same-session background execution via Bash tool `run_in_background=true` with harness completion capture remains the default and is further reinforced** for the future live execution prompt.

**Watch-item**: if `chunk_2016` lands around `~3.4 s/URL` (or higher), the slowdown pattern continues and the conservative anchor should be bumped again in the post-`chunk_2016` planning closure for `chunk_2017`. If the rate flattens or improves, document that the slowdown was transient and the `~2.8 s/URL` anchor remains adequate.

Explicit non-weakening declarations (this calibration is record-only):

- This calibration does NOT weaken the **no-retry** rule.
- This calibration does NOT weaken **exactly-once fetch semantics**.
- This calibration does NOT weaken **no-off-session** execution.
- This calibration does NOT weaken **no-market-data** firewall.
- This calibration does NOT weaken **no-Step-2**.
- This calibration does NOT weaken **no-checkpoint/resume**.
- This calibration does NOT weaken **no-bounded-parallelism**.

## Future execution sequence

The future `chunk_2016` execution prompt (separately initiated; **NOT** authorized by this plan) will perform the following steps in order:

1. **Preflight read-only verification**. Confirm: `HEAD = origin/main = ed4e74c` (or its accepted successor if intervening memory updates / planning memos have landed); ahead = `0`; tracked tree clean; all five guards `False` on disk; production `results/lane2_gdelt1_full_daily_count_build/` exists (contains the prior `chunk_2013_partial_20260524T135157Z/`, `chunk_2014_20260524T150055Z/`, and `chunk_2015_20260524T163556Z/` subdirectories) but does not contain a colliding `chunk_2016_<UTC_TIMESTAMP>/` subdirectory; recognized-list SHA `84ea721e…fff835fc` intact; F4 baselines intact; chunk-runner source byte-identical to its current committed state (and to `389747e`); all three prior chunks' nine artifact SHAs and three tracked reports unmodified; memory mtimes pinned per the most recent memory update.
2. **Enable commit**: flip `FULL_BUILD_AUTHORIZED = False → True` on **line 95** of `scripts/run_lane2_gdelt1_full_daily_count_build.py` via a single one-line edit. Subject: **`Enable Lane 2 full-build chunk_2016 run`**. Numstat `1\t1`. Mirrors `c6b313c`, `574ce77`, and `14c2f6b` enable precedent.
3. **Single live run** of exactly one shell command (inline env var only, no `export`):
   ```
   LANE2_FULL_BUILD_AUTHORIZED=1 python3 scripts/run_lane2_gdelt1_full_daily_count_build.py \
     --authorize-full-build-run --chunk-id chunk_2016
   ```
   Capture stdout, stderr, exit code, start UTC, end UTC, output directory path. The runner is expected to create `results/lane2_gdelt1_full_daily_count_build/chunk_2016_<UTC_TIMESTAMP>/` and write `chunk_contributions.csv` + `chunk_metadata.json` + `chunk_summary.md` (success path) or `halt_diagnostic.json` (halt path) + the partial allowable artifacts. The env var `LANE2_FULL_BUILD_AUTHORIZED` must be `UNSET` after the run command's process exits.
   **Execution mode**: same-session in-session background execution via Bash tool `run_in_background=true` with harness completion capture (mirroring the proven `chunk_2013_partial` `bgzz8eqe5`, `chunk_2014` `blywiekhg`, and `chunk_2015` `bnb2fqhzw` patterns). Same-session, **not** off-session. Justification: the runtime calibration above projects ~17m 5s for 366 URLs at ~2.8 s/URL, ~70% above the 10-min Bash foreground tool ceiling.
4. **Restore commit**: flip line-95 back to `False`. Subject: **`Restore Lane 2 full-build guard after chunk_2016`**. Same `1\t1` numstat. Runner byte-identical to `389747e` post-restore (verify via empty `git diff 389747e HEAD -- scripts/run_lane2_gdelt1_full_daily_count_build.py`). Restore happens **regardless of success or halt** of the live run.
5. **Verify all five guards `False` after restore** via `grep -nE "^(REAL_RETRIEVAL_ENABLED|COUNT_FEASIBILITY_AUTHORIZED|EVENT_FILE_PROBE_AUTHORIZED|ROW_DATE_CHARACTERIZATION_AUTHORIZED|FULL_BUILD_AUTHORIZED) = "`; all four `LANE2_*_AUTHORIZED` shell envs `UNSET`.
6. **Verify output-artifact allow-list**: only files from `ALLOWED_CHUNK_OUTPUT_BASENAMES` (runner line 1554) — `{chunk_contributions.csv, chunk_metadata.json, chunk_summary.md, halt_diagnostic.json}`. No `.zip` / `.CSV` / `tmp_*` / subdirectories.
7. **Verify prior-chunk continuity post-run**: re-compute all **nine** SHA-256 values for the three prior chunks' artifacts and confirm all **three** tracked reports unchanged.
8. **Write a tracked post-chunk execution report** at `docs/lane2_gdelt1_full_build_chunk_2016_execution_report_v0.1.md`, mirroring the `chunk_2015` report at `ed4e74c`. The report records: preflight state; enable-commit SHA; live-run command verbatim + timeout/background strategy + start/end UTC + exit code + stdout/stderr summary + harness shell ID; output directory path; chunk manifest digest; URL count (expected 366 / actual N); per-URL summary (HTTP status, SHA-256, row count, offset distribution); aggregate in-window/out-of-window row counts; per-offset totals; parser anomalies; substrate-gap diagnostic (expected `["2014-01-23","2014-01-24","2014-01-25","2014-03-19"]` in both surfaces, per the canonical shape above); halt class + diagnostic SHA if halted; restore-commit SHA; post-restore guard state; output artifact SHA-256 manifest; boundary confirmations; prior-chunk continuity confirmation for **all three** completed chunks; new runtime calibration data point.
9. **Commit cycle**: three commits in order — `Enable Lane 2 full-build chunk_2016 run` → `Restore Lane 2 full-build guard after chunk_2016` → `Record Lane 2 chunk_2016 execution report`. Push only after the restore commit and report commit both exist and all guards are `False` on disk. Mirrors the `chunk_2013_partial`, `chunk_2014`, and `chunk_2015` cycles exactly.

## Future commit subjects and report path

| Step | Subject | Future file |
|---|---|---|
| Enable | `Enable Lane 2 full-build chunk_2016 run` | (no new file) |
| Restore | `Restore Lane 2 full-build guard after chunk_2016` | (no new file) |
| Report | `Record Lane 2 chunk_2016 execution report` | **`docs/lane2_gdelt1_full_build_chunk_2016_execution_report_v0.1.md`** |

## Future output policy

- Successful per-chunk outputs remain **untracked by default** (Decision 3A `0065d10` + §8.2 `5962c20` + `chunk_2013_partial` `065d475` + `chunk_2014` `770f982` + `chunk_2015` `ed4e74c` precedent).
- Output artifacts must **not** be committed.
- The tracked report records output directory path, artifact sizes, SHA-256 hashes, validation facts, runtime, gap diagnostics, and boundary checks.
- **No raw payload preservation.**
- **No `.zip` / extracted CSV preservation.**
- **No merge artifacts.**

## Expected future validation checks

The future `chunk_2016` execution prompt must verify:

- `actual_completed_file_count == expected_file_count == 366`.
- `chunk_manifest_digest` is recorded (new value, distinct from `6ac92439…bfc8b43`, `93f97096…994aba`, and `a5c61b06…bf17bd67`).
- `source_recognized_list_sha256 == 84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`.
- `no_retry_confirmation == True`.
- `boundary_declarations` all `True` if present (`no_2023plus_access`, `no_asset_or_return_logic`, `no_category_theme_actor_filtering`, `no_market_calendar_alignment`, `no_market_data`, `no_negative_control`, `no_payload_preservation_after_parsing`, `no_spike_threshold_tuning`, `no_step_2`).
- `substrate_gap_diagnostic` matches the corrected expected global-list shape per the "Substrate-gap diagnostic shape for `chunk_2016`" section above: both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` equal `["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]` (the global `KNOWN_SUBSTRATE_GAPS` list, surfaced unconditionally by the runner). Do **not** expect `[]`.
- No `halt_diagnostic.json` on success.
- No raw payloads.
- No `.zip` / extracted CSV.
- No merge artifacts.
- All five guards `False` after restore (with explicit file:line citations).
- `LANE2_*_AUTHORIZED` shell envs unset after run.
- `chunk_2013_partial`, `chunk_2014`, and `chunk_2015` continuity preserved (all nine prior artifact SHAs unchanged, all three tracked reports byte-identical to their committed copies).

## Stop conditions

Hard stop conditions the future `chunk_2016` execution prompt must enforce. Any single one halts the cycle.

### Preflight / procedurally enforced (execution does not begin)

- HEAD ≠ accepted ancestor (e.g., not `ed4e74c` or a successor reviewed and recorded in memory).
- `origin/main` mismatch with HEAD.
- Tracked tree dirty (any `M`/`A`/`D`/`R` entries from `git status --porcelain`, ignoring pre-existing untracked items).
- Any staged files pre-enable.
- Any of the five guards is already `True` on disk pre-enable.
- Any `LANE2_*_AUTHORIZED` shell env is set pre-enable.
- Recognized-list SHA mismatch with `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`.
- F4 baseline SHA mismatch with `41c80c0…624c39d` or `00ce9b2…f5e37552c`.
- Memory mtime drift if the future prompt pins memory mtimes.
- Target post-chunk report `docs/lane2_gdelt1_full_build_chunk_2016_execution_report_v0.1.md` already exists pre-write.
- Existing `chunk_2016_<UTC_TIMESTAMP>/` subdirectory inside `results/lane2_gdelt1_full_daily_count_build/` (runner's `os.makedirs(..., exist_ok=False)` would hard-fail on collision).
- Any prior chunk (`chunk_2013_partial`, `chunk_2014`, `chunk_2015`) output directory, any of its three artifacts, or its tracked report missing, renamed, or SHA-256-mutated.
- Chunk-runner source file diverges from `389747e`'s committed state pre-enable.
- Inability to run the live command via same-session background execution with captured exit status / stdout / stderr / start UTC / end UTC.

### Runner-internal / machine-enforced (during the live run; `run_chunk_build` raises and `_write_chunk_halt_diagnostic` writes the halt artifact, then `raise` re-raises)

- Chunk manifest actual count ≠ `366` (`ChunkManifestError` from `build_chunk_manifest`).
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
- Any raw payload bytes (`.zip`) present in the `chunk_2016` output directory.
- Any extracted CSV rows (`.CSV`) present in the `chunk_2016` output directory.
- Any output outside `ALLOWED_CHUNK_OUTPUT_BASENAMES`.
- Any retry attempt observed in the runner's per-URL manifest.
- Any second-GET attempt for the same URL.
- Any accidental market-data / Step 2 / spike-burst / return-window logic.
- Any modification to any prior chunk's output (SHA-256 mismatch on any of the nine prior artifacts) or report (byte-divergence from committed copy).
- Any accidental next-chunk run (e.g., a `chunk_2017` directory appearing).
- Any accidental merge run (e.g., top-level `daily_count.csv` / `build_metadata.json` / `build_summary.md` appearing).
- `substrate_gap_diagnostic` does not match the runner-implementation-expected shape `["2014-01-23","2014-01-24","2014-01-25","2014-03-19"]` in both surfaces (this would indicate a runtime change to the runner or a change to `KNOWN_SUBSTRATE_GAPS`, not a chunk-data anomaly).

Any halt condition triggers the **session-interruption recovery rule**: restore the guard, preserve partial output as-is, emit verdict `FULL-BUILD CHUNK_2016 RUN HALTED — AWAIT ADJUDICATION`.

## Outcome classes for future live execution

The future execution prompt must classify its outcome as exactly one of:

- **SUCCESS** — runner exits with code 0; three success artifacts present; `actual = expected = 366`; substrate-gap diagnostic matches expected; all three prior chunks' continuity preserved.
- **BLOCKED BEFORE ENABLE** — a preflight check failed; no guard flip occurred.
- **LIVE RUN FAILURE** — runner exit non-zero, halt class identified, `halt_diagnostic.json` may exist.
- **OUTPUT VERIFICATION FAILURE** — runner exited cleanly but the produced output set / SHAs / metadata do not match the success contract.
- **OUTPUT VERIFICATION FAILURE / SUBSTRATE GAP DIAGNOSTIC MISMATCH** — substrate-gap diagnostic deviates from the canonical four-2014-date global shape.
- **PRIOR CHUNK CONTINUITY FAILURE** — `chunk_2013_partial`, `chunk_2014`, or `chunk_2015` artifacts / reports changed during the cycle.
- **GUARD RESTORE FAILURE** — line-95 could not be restored to `False`.
- **INFRASTRUCTURE FAILURE / SUBPROCESS STATE AMBIGUOUS** — tool-layer timeout / abort / interruption; subprocess may have been running when guard restore proceeded.
- **INFRASTRUCTURE FAILURE / SUBPROCESS STATE UNKNOWN** — subprocess state could not be reliably established.

**Guard restoration must be prioritized after any enable commit, regardless of live-run success or failure, unless the repo state itself prevents restoration.** Push must not proceed while the guard remains enabled.

## Substrate progress projection

If `chunk_2016` succeeds with `actual_completed_file_count = 366`:

| Metric | Before `chunk_2016` | Projected after `chunk_2016` |
|---|---|---|
| Chunks complete | 3 / 10 | **4 / 10** |
| Completed chunks list | `chunk_2013_partial`, `chunk_2014`, `chunk_2015` | `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, `chunk_2016` |
| Daily URLs complete | 1,001 / 3,558 | **1,367 / 3,558** (= 1,001 + 366) |
| Percent complete by URL count | ~28.1% | ~**38.4%** |
| Remaining daily URLs | 2,557 | **2,191** |
| Remaining chunks | 7 | **6** (`chunk_2017` through `chunk_2022`) |

Merge remains blocked until 10/10 chunks succeed per `5962c20` §9.1.2. Chunks `chunk_2017` through `chunk_2022` each require their own separately authorized execution prompt; this cycle does not authorize them.

## Boundary statement

This plan authorizes **none** of the following:

- Live execution of `chunk_2016` or any other chunk.
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
- Output-artifact mutation (all three prior chunks' output directories remain untouched read-only; the pre-existing `results/lane2_gdelt1_event_file_probe/`, `results/lane2_gdelt1_row_date_characterization/`, `results/lane2_gdelt1_count_feasibility/` directories also untouched).
- Recognized-list mutation (`84ea721e…fff835fc` preserved).
- F4 mutation (baselines preserved).
- Memory edit.
- Code edit (`scripts/`, `src/`, `tests/` byte-identical to `ed4e74c`).
- Test edit.
- Re-running `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, or any other chunk.
- Running any chunk other than `chunk_2016`.
- Locked-commit edits to prior memo / execution-cycle commits in the lifecycle chain `a8a9dd2` / `a2a8fd5` / `e9f8781` / `487dadb` / `3537a62` / `73a7911` / `858b501` / `0065d10` / `7780a97` / `bc7b66b` / `c10ae74` / `d7c8775` / `fbc605b` / `5962c20` / `389747e` / `447656d` / `c6b313c` / `167a08a` / `065d475` / `4276b30` / `574ce77` / `13f14ba` / `770f982` / `f4590eb` / `14c2f6b` / `083649b` / `ed4e74c` / `e55e09a` / `0b341b4` / `845c51c` / `e81208d` / `7c85e3f` / `9319d30`.
- Staging / commit / push of this plan or any other artifact (the plan's commit is a separately authorized follow-up step, NOT part of this planning turn).

The no-market-data firewall, no-2023+ posture, no-retry rule, exactly-once fetch semantics, no-merge-until-10/10 rule, recognized-list authority, SQLDATE re-keying, and the locked design contract from `7780a97` as amended by `c10ae74` + the chunk-design contract from `5962c20` all remain in force.

## Decision points before live execution

All decision points from prior cycles are resolved by precedent for `chunk_2016`:

| Decision point | Resolution by precedent |
|---|---|
| Chunk-output artifact disposition | **Untracked by default** per `0065d10` Decision 3A + `5962c20` §8.2; reaffirmed by `chunk_2013_partial` (`065d475`), `chunk_2014` (`770f982`), and `chunk_2015` (`ed4e74c`) cycles. |
| Commit sequence | **Three commits: Enable → Restore → Report.** Reaffirmed by all three prior cycles. |
| Post-chunk report commit timing | **Report committed standalone** (output untracked); resolves automatically. |
| Timeout / subprocess strategy | **In-session background execution via Bash `run_in_background=true`** with harness completion capture; mirrors `bgzz8eqe5`, `blywiekhg`, and `bnb2fqhzw`; same-session, **not** off-session; justified by the ~17m 5s runtime projection ~70% above the 10-min Bash foreground ceiling. |
| Output-directory timestamping | Runner-controlled via `chunk_2016_<UTC_TIMESTAMP>/`; collision handled by `os.makedirs(..., exist_ok=False)`. |
| Substrate-gap diagnostic surfacing | Runner surfaces the **global** `KNOWN_SUBSTRATE_GAPS` list in both `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched` unconditionally (lines 1349–1351, 2011–2013); the expected `chunk_2016` shape is the four 2014 dates in both fields, not `[]`. Empirically validated in the live `chunk_2015` run at `ed4e74c`. |
| Conservative runtime anchor | `~2.8 s/URL` (from the post-`chunk_2015` calibration update). The future `chunk_2016` execution-closure memory update should bump this anchor again if the observed rate exceeds ~3.4 s/URL. |

Precedent citations:

- `0065d10 Decision 3A` — untracked-by-default for per-cycle output artifacts.
- `5962c20 §8.2` — chunk-design memo's untracked-by-default codification.
- `chunk_2013_partial` execution at `065d475` (chain `c6b313c → 167a08a → 065d475`).
- `chunk_2014` execution at `770f982` (chain `574ce77 → 13f14ba → 770f982`).
- `chunk_2015` execution at `ed4e74c` (chain `14c2f6b → 083649b → ed4e74c`) — includes the empirical validation of the corrected substrate-gap diagnostic shape and the `~2.8 s/URL` calibration anchor.

## Next steps after this memo

The next procedural steps after this planning memo's creation are, in order:

- **Sanity-check review** of the planning memo (read-only, by the user or a separately invoked review-only prompt). If review surfaces issues, a corrective revision of this plan precedes the commit prompt.
- **Separate explicit commit prompt** (no commit is authorized by this planning-memo-creation turn).
- **Separate memory-update prompt for the planning closure** (after commit/push lands).
- **Only then**, a separate live `chunk_2016` execution-authorization prompt (which performs the steps in §"Future execution sequence" above).

**No execution is authorized by this planning memo creation turn.** Its persistence scope is complete upon writing the single file at `docs/lane2_gdelt1_full_build_chunk_2016_execution_authorization_plan_v0.1.md`. No review, no staging, no commit, no push, no memory update, no live execution, no guard flip, no GDELT contact, no merge, no market data, and no Step 2 work is authorized by this turn.
