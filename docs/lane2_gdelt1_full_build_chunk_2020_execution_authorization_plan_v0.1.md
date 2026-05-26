# Lane 2 — GDELT1 Full Daily Count Build — chunk_2020 Execution-Authorization Plan (v0.1)

## 1. Status / scope

This memo creates the **chunk_2020 planning frontier only**. It is a
planning/authorization-plan document. It does not by itself authorize live
execution of the chunk_2020 build.

This memo is explicitly:

- **not** live execution
- **not** merge
- **not** Step 2
- **not** market-data access
- **not** instrument construction
- **not** a guard flip
- **not** a runner invocation
- **not** authorization for chunk_2021 / chunk_2022

No live retrieval, no GDELT contact, no runner invocation, and no
output-directory creation has occurred or is authorized by the act of writing
this memo. No commit and no push has occurred or is authorized by the act of
writing this memo (commit/push are a separate sub-cycle).

## 2. Current canonical state and lineage

HEAD = origin/main = `366d43f0358d29691582194fdfce4c7bfba2d003` (short
`366d43f`). Ahead/behind versus `origin/main` is 0 0. Tracked tree clean
(working tree contains only untracked artifacts: build outputs under
`results/`, paper LaTeX intermediates, and one untracked draft / one untracked
report; none of these are repo state). Path (b) cycle counter at the
chunk_2019 fresh-attempt execution-closure memory-update boundary is **61**
and is unchanged by this memo (memo creation is not a memory-update boundary).

Lineage through `366d43f`:

- `7206e30` — Lane 2 sentinel SQLDATE substrate amendment memo (recorded)
- `d99a2100f20f2bd87984a6ea1627a98576a6ed9f` (short `d99a210`) — Lane 2
  sentinel SQLDATE recognition (R3 + Option α) runner amendment commit; this
  is the **post-amendment runner regime anchor** for chunk_2019-onward chunks
- `6c17850` — chunk_2019 execution-authorization planning memo (original)
- `437e7e972ce8e82f72608df64f28ba6988ceb9e2` (short `437e7e9`) — chunk_2019
  execution-authorization plan post-amendment addendum
- `a69b32310acc484233b59debdd7a1edae0a477d8` (short `a69b323`) — chunk_2019
  fresh-attempt enable commit (one-line `FULL_BUILD_AUTHORIZED = False → True`
  at line 95)
- `366d43f0358d29691582194fdfce4c7bfba2d003` (short `366d43f`) — chunk_2019
  fresh-attempt restore commit (one-line `FULL_BUILD_AUTHORIZED = True →
  False` at line 95); runner blob restored to
  `a1a10994d183b70bb4dfdcec9a981013a5857e10`

chunk_2019 cycle is fully closed under the amended runner regime
(fresh-attempt execution + lineage push complete; halted first attempt at
`archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2019_20260525T192552Z/halt_diagnostic.json`
SHA `3b2b43708d0a7a9410d59a7bfd4deec7fef84f8a6543472f25942e67e1058005`
remains canonically closed and untouched as audit evidence only).

Substrate progress prior to chunk_2020:

- 7 of 10 chunks complete (chunk_2013_partial, chunk_2014, chunk_2015,
  chunk_2016, chunk_2017, chunk_2018, chunk_2019)
- 2,462 of 3,558 daily URLs complete (~69.2%)
- 3 chunks remain: chunk_2020, chunk_2021, chunk_2022
- 1,096 URLs remain
- merge blocked until 10/10 chunks succeed
- Step 2 remains firewalled

## 3. Memory preflight anchors

The two memory files in scope were verified at preflight immediately before
this memo was written. These anchors must continue to match exactly after
this memo is created. Memo creation does not edit memory files.

`MEMORY.md`

- size: 243,376 B
- SHA-256: `12889717940f0aa6445983026f505ea76658131d7dd05ec4efd6eddf612a6d67`
- mtime: May 26 16:04:04 2026

`project_lane2_attention_spike.md`

- size: 421,120 B
- SHA-256: `f1b3276d104aff4179e66adc816ede2a56ee73a58393bb24ac4d8ab591bf8234`
- mtime: May 26 16:03:34 2026

## 4. Authority artifacts

The following authority artifacts were SHA-256-verified at preflight and were
not modified by this memo creation. They remain canonical anchors for the
program and must be re-verified at any future chunk_2020 execution preflight.

- `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json`
  SHA-256: `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`
  (matches `RECOGNIZED_LIST_SHA256` constant in runner)
- `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json`
  (F4 baseline) SHA-256:
  `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d`
- `results/lane2_gdelt1_count_feasibility/20260518T163302Z/feasibility_summary.md`
  (F4 baseline) SHA-256:
  `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c`

These are preserved authority anchors; they were verified before memo creation
and are not modified by memo creation.

## 5. Post-amendment runner regime anchoring

chunk_2020 is anchored to the post-amendment runner regime — the same regime
under which chunk_2019 was successfully executed as a fresh attempt. The
post-amendment anchors are:

- **runner blob SHA**: `a1a10994d183b70bb4dfdcec9a981013a5857e10`
- **amendment commit**: `d99a2100f20f2bd87984a6ea1627a98576a6ed9f` (short
  `d99a210`); subject *"Add Lane 2 sentinel SQLDATE recognition (R3 + Option
  α)"*
- **byte-identity check at preflight**: `git diff --exit-code d99a210 --
  scripts/run_lane2_gdelt1_full_daily_count_build.py` returned exit code 0 at
  the time of this memo's creation; the runner is byte-identical to the
  amendment commit

Pre-amendment-anchored chunks (`chunk_2013_partial` through `chunk_2018`) were
executed under the prior runner regime anchored to commit `389747e` / blob
`0c022e36986891753507cc28fdba83d612a61390`. chunk_2019 and chunk_2020 onward
are anchored to the post-amendment regime above. This distinction is
load-bearing for byte-identity verification at any future execution preflight.

The post-amendment regime introduces the sentinel SQLDATE recognition
mechanism (R3 + Option α) and is documented in:

- substrate amendment memo at commit `7206e30`
- chunk_2019 post-amendment planning addendum at commit `437e7e9` (file SHA
  `0c65be07327e5dbaa21a682ece40d087489dd3152ebdddb1876dcc6651a1f158`)
- chunk_2019 fresh-attempt execution-closure record in
  `project_lane2_attention_spike.md` at the 2026-05-26 memory update

## 6. chunk_2020 target definition

- chunk name: `chunk_2020`
- year: 2020 (**leap year** — 366 calendar days)
- expected URL count: **366** (one more than the non-leap years)
- prior progress before chunk_2020: 7 of 10 chunks complete; 2,462 of 3,558
  URLs complete (~69.2%)
- expected progress after a future successful chunk_2020 execution: 8 of 10
  chunks complete; 2,828 of 3,558 URLs complete (~79.5%)
- remaining after a future successful chunk_2020 execution: chunk_2021,
  chunk_2022; 730 URLs remain
- merge still blocked until 10/10 chunks succeed
- Step 2 still firewalled
- **no chunk_2021 / chunk_2022 authorization** by this memo; chunk_2021 and
  chunk_2022 require their own separately scoped planning prompts in turn

Arithmetic check: 2,462 + 366 = 2,828; 3,558 − 2,828 = 730; 730 = 365 + 365 =
chunk_2021 (365) + chunk_2022 (365).

## 7. Runner anchors (verified directly from current runner)

The runner anchors for `chunk_2020` were re-verified **directly** in
`scripts/run_lane2_gdelt1_full_daily_count_build.py` against the current
runner blob at preflight. They were **not reused from prediction**; the
predicted line numbers (1602 / 1615 / 1628) were treated as predictions only
and re-verified against the runner at the time of this memo's creation. The
verified line numbers match the prediction exactly.

| Anchor                                                                          | Verified line |
| ------------------------------------------------------------------------------- | ------------- |
| Canonical chunk-list entry `"chunk_2020",` in `CHUNK_IDS`                       | 1602          |
| `EXPECTED_CHUNK_COUNTS` entry `"chunk_2020": 366,`                              | 1615          |
| `CHUNK_YEAR_RANGES` entry `"chunk_2020": (date(2020, 1, 1), date(2020, 12, 31)),` | 1628          |

Additional preflight invariants verified at this memo's preflight:

- `FULL_BUILD_AUTHORIZED = False` at
  `scripts/run_lane2_gdelt1_full_daily_count_build.py:95`
- `SENTINEL_SQLDATES: Tuple[date, ...] = (date(1920, 1, 1),)` at
  `scripts/run_lane2_gdelt1_full_daily_count_build.py:136`
- `EXPECTED_OFFSETS: Tuple[int, ...] = (-3650, -365, -30, -7, -1, 0, 1)` at
  `scripts/run_lane2_gdelt1_full_daily_count_build.py:120`
- `KNOWN_SUBSTRATE_GAPS` defined at
  `scripts/run_lane2_gdelt1_full_daily_count_build.py:141`
- runner byte-identical to amendment commit `d99a210` (`git diff --exit-code
  d99a210 -- scripts/run_lane2_gdelt1_full_daily_count_build.py` exit code 0)
- runner blob SHA = `a1a10994d183b70bb4dfdcec9a981013a5857e10`
- no `LANE2_*_AUTHORIZED` shell environment variable is set

All five program guards remain false:

- `src/lane2_gdelt1_count_feasibility.py:647`
  `REAL_RETRIEVAL_ENABLED = False`
- `scripts/run_lane2_gdelt1_count_feasibility.py:49`
  `COUNT_FEASIBILITY_AUTHORIZED = False`
- `scripts/run_lane2_gdelt1_event_file_probe.py:52`
  `EVENT_FILE_PROBE_AUTHORIZED = False`
- `scripts/run_lane2_gdelt1_row_date_characterization.py:57`
  `ROW_DATE_CHARACTERIZATION_AUTHORIZED = False`
- `scripts/run_lane2_gdelt1_full_daily_count_build.py:95`
  `FULL_BUILD_AUTHORIZED = False`

**Re-verification discipline**: at any future chunk_2020 execution-preflight,
the line-number anchors (1602 / 1615 / 1628) MUST be re-verified directly
against the current runner — they MUST NOT be reused from this memo as
predictions. If any of those lines have drifted, the execution prompt must
treat that as a preflight failure and stop before any enable commit. This is
the same re-verification discipline applied at chunk_2019's preflight.

## 8. Required pre-execution checks for a future chunk_2020 execution prompt

A future chunk_2020 execution-authorization prompt must perform, at minimum,
the following preflight checks before flipping any guard:

1. HEAD / origin/main alignment to the then-current canonical state.
2. Ahead/behind against `origin/main` is 0 0.
3. Tracked tree clean (no staged files; no tracked modifications).
4. Runner blob SHA equal to `a1a10994d183b70bb4dfdcec9a981013a5857e10` (or to
   whatever the then-canonical post-amendment runner blob is, if a further
   amendment has occurred — in which case a fresh planning addendum is
   required prior to execution).
5. `FULL_BUILD_AUTHORIZED = False` at
   `scripts/run_lane2_gdelt1_full_daily_count_build.py:95`.
6. `SENTINEL_SQLDATES = (date(1920, 1, 1),)` still defined at
   `scripts/run_lane2_gdelt1_full_daily_count_build.py:136`.
7. All five program guards `False`.
8. All `LANE2_*_AUTHORIZED` shell environment variables unset.
9. No `chunk_2020` execution-output directory exists under
   `results/lane2_gdelt1_full_daily_count_build/`.
10. `chunk_2020` line-number anchors (1602 / 1615 / 1628) **directly
    re-verified** against the current runner, **not reused from this memo**.
11. Authority artifact SHAs (Section 4) re-verified.
12. Memory files not modified during preflight.
13. `chunk_2021` / `chunk_2022` anchors not touched, reused, or verified for
    execution purposes (Section 6 negative confirmation).

If any preflight item fails, the execution prompt must stop before the enable
commit and report the most specific BLOCKED verdict.

## 9. Locked substrate-anomaly taxonomy — two distinct mechanisms

chunk_2019's fresh-attempt empirical-validation closure surfaced two distinct
substrate-anomaly streams that must continue to be reported as **separate
mechanisms** in chunk_2020 (and onward). They are not to be conflated, even
though both surface in `chunk_metadata.json`. This is the locked taxonomy
carried forward from the chunk_2019 closure.

### 9.A — In-file SQLDATE sentinel-placeholder stream (R3 + Option α)

- **Mechanism**: a non-`(0..86)`-offset SQLDATE value inside an otherwise
  well-formed daily event-file is recognized as a placeholder-dated row
  rather than lookback-retrocoded; routed into per-sentinel diagnostics;
  excluded from `total_in_window_rows` / `total_out_of_window_rows` under
  Option α; **not** subject to the `EXPECTED_OFFSETS` halt.
- **Current sentinel set**: `SENTINEL_SQLDATES = (date(1920, 1, 1),)` (line
  136 of the runner). The set is narrow now and extensible in shape; it is
  extended only on **direct substrate evidence**, not on prediction.
- **Empirical record so far**: chunk_2019's `2019-12-31` daily file contained
  120 rows with SQLDATE `1920-01-01`; the runner correctly recognized and
  routed them under R3 + Option α. T1 (single affected file) and S1 (single
  sentinel value) properties were both confirmed at chunk_2019 closure.
- **`EXPECTED_OFFSETS` invariance**: the canonical tuple
  `(-3650, -365, -30, -7, -1, 0, 1)` MUST remain unchanged for non-sentinel
  rows; halt-on-other-unexpected behavior MUST remain active.
- **Diagnostic-vs-fail rule for chunk_2020**: any sentinel-routed rows
  observed in chunk_2020 are **diagnostic** so long as the structural
  invariants hold (`EXPECTED_OFFSETS` unchanged; halt-on-other-unexpected
  preserved; 5-term row-arithmetic identity holds:
  `in_window + out_of_window + sentinel + malformed + unparseable = parsed`).
- **Failure rule**: any **non-sentinel** SQLDATE that produces an offset
  outside `EXPECTED_OFFSETS` MUST halt the run via the existing
  halt-on-other-unexpected behavior. No silent expansion of the sentinel set
  is permitted during execution.
- **Distinctness**: this mechanism is distinct from the fetch-gap diagnostic
  mechanism (Section 9.B) per the locked taxonomy. Reporting must keep them
  separate.

### 9.B — Fetch-gap diagnostic stream

- **Mechanism**: the runner unconditionally surfaces the global
  `KNOWN_SUBSTRATE_GAPS` tuple via two fields in `chunk_metadata.json`:
  `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched`. These
  capture **publishing-file substrate gaps** (dates on which no daily event
  file is published), which is a fundamentally different phenomenon from
  the sentinel-placeholder stream (which is about rows *inside* a file).
- **Canonical shape**: both `known_substrate_gap_dates` and
  `substrate_gap_dates_not_fetched` MUST be the four-date list
  `['2014-01-23', '2014-01-24', '2014-01-25', '2014-03-19']` for chunk_2020,
  not `[]` / `[]`. The runner emits the global tuple, not a per-chunk subset.
- **Empirical validation history**: fourth-empirically-validated across
  chunks 2015 / 2016 / 2017 / 2018; **fifth-empirically-validated** at
  chunk_2019 fresh-attempt closure (4 / 4 pattern confirmed in
  `chunk_2019_20260526T130910Z/chunk_metadata.json`). chunk_2020 is the
  **sixth empirical-validation surface** for this diagnostic.
- **Expected semantic interpretation for chunk_2020**: there are zero
  in-range 2020 substrate gaps (the canonical gap dates are all 2014, fully
  outside the chunk_2020 date range `(2020-01-01, 2020-12-31)`), while the
  runner unconditionally surfaces the global `KNOWN_SUBSTRATE_GAPS` tuple.
  A future chunk_2020 live-execution report must therefore continue to
  record both fields with the canonical four-date / four-date shape, and
  **must not silently treat `[]` / `[]` as equivalent** to that canonical
  shape. Any future deviation from the canonical four-date / four-date
  shape on chunk_2020 must be treated as a diagnostic event, not as routine.
- **Distinctness**: this mechanism is distinct from the in-file sentinel
  stream (Section 9.A) per the locked taxonomy. Reporting MUST keep them
  separate; conflating them is a discipline regression.

## 10. Runtime planning anchor and watch

Canonical planning anchor: 366 URLs × 2.8 s/URL ≈ 1,024.8 s ≈ 17m 4.8s
(dimensional check: URLs × s/URL = s). One additional URL versus a 365-URL
chunk (leap-year extra day) implies the planning anchor is ~2.8 s longer
than the chunk_2019 anchor under the same per-URL rate.

Recent history (carry-forward):

- chunk_2018 ~2.69 s/URL
- chunk_2019 halted partial ~2.469 s/URL (364 / 365 URLs before halt; not a
  closure observation)
- chunk_2019 fresh-attempt **~2.39 s/URL** (365 / 365 URLs; closure
  observation under the amended runner regime)
- the ~2.8 s/URL anchor is preserved as a **transient improvement**, not
  promoted to a new structural baseline
- bump-down threshold review is **deferred until chunk_2020 observed runtime
  is in hand**

Three-branch interpretation for the future chunk_2020 execution-closure stage:

- **(a)** if chunk_2020 observed s/URL is ≥ ~3.4 s/URL, bump the anchor
  upward at execution closure (slowdown reversion).
- **(b)** if chunk_2020 is flat or improved versus chunk_2019 fresh-attempt
  (≤ ~2.39 s/URL ± noise), preserve the current ~2.8 s/URL anchor as a
  transient improvement and **revisit the bump-down threshold** at
  execution closure: if the trend is robust across chunk_2018 → chunk_2019
  fresh → chunk_2020, a separately authorized anchor-bump-down memo may be
  drafted to lower the structural baseline. The bump-down memo is not
  authorized by this memo; only the review is scheduled.
- **(c)** if a slowdown resumes but remains below the bump-up trigger,
  preserve the anchor and keep the watch active.

The watch remains active for chunk_2020. The bump-down review is a separately
scoped sub-cycle, not part of chunk_2020 execution.

## 11. Boundary conditions for future live execution

Future chunk_2020 live execution is **not** authorized by this memo. Future
live execution requires a separate user initiation and a separate
live-execution authorization prompt.

The future live-execution prompt must preserve all of the following, none
weakened — the **7-item non-weakening canon** carried forward verbatim from
the project-memory canonical variant (chunk_2019 closure boundary):

1. **no-retry**
2. **exactly-once**
3. **no-off-session**
4. **no-market-data**
5. **no-Step-2**
6. **no-checkpoint-resume**
7. **no-bounded-parallelism**

Broader boundary conditions carried forward (separate from, and not part of,
the 7-item canon above; none weakened):

- **no merge** — merge remains blocked until 10/10 chunks succeed per
  chunk-design memo `5962c20` §9.1.2
- **no `chunk_2021` / `chunk_2022` authorization** within a chunk_2020
  execution prompt
- **no raw payload preservation**
- **no prior-chunk rerun**
- **no 2023+ access** — preserve no-2023+ posture
- **no instrument construction**
- **no memory edit during live execution**
- **no commit / no push by this memo**
- **no execution by this memo**
- preserve halt-on-other-unexpected behavior
- preserve `KNOWN_SUBSTRATE_GAPS`
- preserve `SENTINEL_SQLDATES`
- preserve `EXPECTED_OFFSETS`
- preserve recognized-list authority (`RECOGNIZED_LIST_SHA256` matched)
- preserve the locked substrate-anomaly taxonomy (Section 9: two distinct
  mechanisms)

## 12. Expected future output shape (for future live execution only)

The following is the **expected** shape for a future chunk_2020 live
execution. Nothing in this section authorizes such execution; it is recorded
here so the future live-execution preflight and execution-closure stages can
cross-check against this memo.

Expected output directory pattern:

`results/lane2_gdelt1_full_daily_count_build/chunk_2020_<UTC>/`

Expected files inside that directory:

- `chunk_contributions.csv`
- `chunk_metadata.json`
- `chunk_summary.md`

Expected absences:

- no raw payloads
- no `halt_diagnostic.json` on success

The future chunk_2020 execution report must record (at minimum):

- output directory
- artifact sizes
- artifact SHA-256s
- chunk manifest digest
- `total_in_window_rows`
- `total_out_of_window_rows`
- `total_sentinel_rows` and `per_sentinel_total` / `sentinel_sqldate_distribution`
  (Section 9.A taxonomy)
- `parser_anomaly_diagnostic.total_malformed_short_rows` and
  `total_unparseable_sqldate_rows`
- `total_parsed_rows`
- **5-term row arithmetic check**: `in_window + out_of_window + sentinel +
  malformed + unparseable = parsed` (per R3 + Option α)
- `known_substrate_gap_dates` and `substrate_gap_dates_not_fetched`
  (Section 9.B taxonomy — must remain four-date / four-date shape)
- `per_offset_total` keyed exactly by `EXPECTED_OFFSETS`
- runtime (wall-clock and runner-recorded UTC)
- per-URL runtime classification under the three-branch interpretation
  (Section 10)
- boundary preservation declarations (`boundary_declarations` all True)
- guards restored false after run
- runner byte-identity restored after run (blob SHA equal to
  `a1a10994d183b70bb4dfdcec9a981013a5857e10`)
- push state (if/when applicable; fast-forward only)
- on-disk execution report SHA-256, computed at execution-closure preflight,
  per chunk_2018-established discipline

## 13. Carry-forward discipline

Unresolved items (carry-forward, none load-bearing):

1. Section 9 commit-report cosmetic observation (still carrying forward;
   non-blocking).
2. Substrate amendment memo Observation 1 — §9 R2 framing symmetry
   candidate (carry-forward only).
3. Substrate amendment memo Observation 2 — chunk_2018 `61,529,216`
   in-window-row anchor verify-before-reuse note.
4. Four addendum-content-review non-blocking observations from the 2026-05-26
   chunk_2019 addendum cycle (R3-hybrid terminology cosmetic; addendum length
   239 vs 100–150 target; §8 next-step pointer tightness; §8 standalone
   non-authorization statement tightness).

The sentinel-remediation fifth-empirical-validation item and the
substrate-gap fifth-empirical-validation item were **closed** at the
chunk_2019 fresh-attempt closure memory update; they are no longer in the
carry-forward backlog.

Established disciplines **(a)–(l) carry forward verbatim** per
`project_lane2_attention_spike.md` at the 2026-05-26 chunk_2019-closure
boundary; the full text of each discipline is canonical there and is not
duplicated in this memo. Discipline (l) — counter-token regression check
for memory-write closure — **remains memory-update-boundary specific** and is
NOT generalized to all artifacts carrying Path (b) values; any future
generalization (e.g., extending (l) to non-memory artifacts) must be
separately codified at a future memory-update boundary, not by incidental
re-wording in a per-chunk planning memo. Most-recent application of (l):
chunk_2019 fresh-attempt closure memory update (active Path (b) value 61;
intermediate token 60 verified zero active occurrences).

Locked substrate-anomaly taxonomy (Section 9) carried forward: in-file
SQLDATE sentinel-placeholder stream (R3 + Option α) and fetch-gap diagnostic
stream are two distinct mechanisms; reporting MUST keep them separate.

## 14. Merge / Step 2 boundary

- **Merge remains blocked** until 10 / 10 chunks succeed per chunk-design
  memo `5962c20` §9.1.2. Current progress is 7 / 10; chunk_2020 (when later
  authorized and executed) would bring progress to 8 / 10; chunk_2021 and
  chunk_2022 remain after that. Merge is not authorized by this memo and is
  not authorized by any future chunk_2020 execution prompt.
- **Step 2 remains firewalled** until a separately authorized memo retires
  the no-market-data firewall. Step 2 is not authorized by this memo and is
  not authorized by any future chunk_2020 execution prompt.
- **Off-session execution / Option D remains not authorized** for chunk_2020
  by this memo (see Option D reserve-tier label-reconciliation memo
  `fbc605b`).

## 15. Next frontier after this planning memo creation

After this planning memo is created, the next eligible action is **not**
automatic execution. The next sub-cycle is:

> chunk_2020 planning memo content review / sanity-check

Following the chunk-level planning lifecycle established through chunks
2013_partial → 2019, the sub-cycle sequence is:

1. **planning memo creation** (this memo — completed by this turn's draft)
2. planning memo content review / sanity-check (separately scoped)
3. planning memo commit + push (separately scoped; not authorized by this
   memo's creation)
4. planning-closure memory update (separately scoped)
5. *(only after the above four are complete)* chunk_2020 execution-authorization
   prompt — separately initiated by the user
6. chunk_2020 execution (exactly-once, same-session, no retry, no resume,
   no bounded parallelism, no off-session)
7. chunk_2020 enable/restore lineage push
8. chunk_2020 execution-closure memory update

Only after sub-cycles 1–4 are complete would chunk_2020 live-execution
authorization become eligible. No live execution is authorized by this memo
creation. No commit, no push, and no memory update is authorized by this
memo creation. Pause: await explicit next prompt.
