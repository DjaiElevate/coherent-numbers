# Lane 2 — GDELT1 Full Daily Count Build — chunk_2019 Execution-Authorization Plan (v0.1)

## 1. Status / scope

This memo creates the **chunk_2019 planning frontier only**. It is a
planning/authorization-plan document. It does not by itself authorize live
execution of the chunk_2019 build.

This memo is explicitly:

- **not** live execution
- **not** merge
- **not** Step 2
- **not** market-data access
- **not** instrument construction
- **not** a guard flip
- **not** a runner invocation

No live retrieval, no GDELT contact, no runner invocation, and no
output-directory creation has occurred or is authorized by the act of writing
this memo.

## 2. Current canonical state

HEAD = origin/main = 6e9b6faebe47cf39545435f265be9a60c1f868fd (short 6e9b6fa).
Ahead/behind versus `origin/main` is 0 0. Path (b) counter at the chunk_2018
execution-closure boundary is 37 and is unchanged by this memo (memo creation
is not a memory-update boundary). chunk_2018 cycle is fully closed (sub-cycle
6 closure confirmed; discipline (f) aggregate row totals confirmed on disk by
the narrow Flag 1 disambiguation grep; no row-total fix was required; counter
remains 37; guards remain false; merge remains blocked; Step 2 remains
firewalled).

Substrate progress prior to chunk_2019:

- 6 of 10 chunks complete (chunk_2013_partial, chunk_2014, chunk_2015,
  chunk_2016, chunk_2017, chunk_2018)
- 2,097 of 3,558 daily URLs complete (≈58.9%)
- 4 chunks remain: chunk_2019, chunk_2020, chunk_2021, chunk_2022
- 1,461 URLs remain
- merge blocked until 10/10 chunks succeed
- Step 2 remains firewalled

## 3. Memory preflight anchors

The two memory files in scope were verified byte-for-byte against the
chunk_2018 sub-cycle 6 closure anchors immediately before this memo was
written.

`MEMORY.md`

- size: 202,376 B
- SHA-256: e249c941cb47bccd4ac5d440af118054ac2f7c4b9840bf651975694e3fb2ac8c
- mtime: May 25 06:43:55

`project_lane2_attention_spike.md`

- size: 370,413 B
- SHA-256: 846f5e5dabb4de4108858b2a64318f1ab557a30b78be5e7a1a656118e218a0a7
- mtime: May 25 06:48:56

These anchors must continue to match exactly after this memo is created. Memo
creation does not edit memory files.

## 4. Authority artifacts

The following authority artifacts were SHA-256-verified at preflight and were
not modified by this memo creation. They remain canonical anchors for the
program.

- `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json`
  SHA-256: 84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc
- `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json`
  (F4 baseline) SHA-256:
  41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d
- `results/lane2_gdelt1_count_feasibility/20260518T163302Z/feasibility_summary.md`
  (F4 baseline) SHA-256:
  00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c

These are preserved authority anchors; they were verified before memo creation
and are not modified by memo creation.

## 5. chunk_2019 target definition

- chunk name: `chunk_2019`
- year: 2019
- expected URL count: 365
- prior progress before chunk_2019: 6 of 10 chunks complete; 2,097 of 3,558
  URLs complete
- expected progress after a future successful chunk_2019 execution: 7 of 10
  chunks complete; 2,462 of 3,558 URLs complete
- remaining after a future successful chunk_2019 execution: chunk_2020,
  chunk_2021, chunk_2022; 1,096 URLs remain
- merge still blocked until 10/10 chunks succeed
- Step 2 still firewalled

Arithmetic check: 2,097 + 365 = 2,462; 3,558 − 2,462 = 1,096.

## 6. Runner anchors (verified)

The runner anchors for `chunk_2019` were verified in
`scripts/run_lane2_gdelt1_full_daily_count_build.py` at the lines predicted
from prior state. Predicted lines were 1521 / 1534 / 1547; the actual verified
line numbers match the prediction exactly.

| Anchor                                       | Verified line |
| -------------------------------------------- | ------------- |
| Canonical chunk-list entry `"chunk_2019",`   | 1521          |
| `EXPECTED_CHUNK_COUNTS` entry `"chunk_2019": 365,`   | 1534          |
| `CHUNK_YEAR_RANGES` entry `"chunk_2019": (date(2019, 1, 1), date(2019, 12, 31)),` | 1547 |

Additional preflight invariants verified:

- `FULL_BUILD_AUTHORIZED = False` at
  `scripts/run_lane2_gdelt1_full_daily_count_build.py:95`
- runner byte-identical to commit `389747e`
  (`git diff --exit-code 389747e -- scripts/run_lane2_gdelt1_full_daily_count_build.py`
  returned exit code 0)
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

## 7. Runtime planning anchor and watch

Canonical planning anchor: 365 URLs × 2.8 s/URL ≈ 1,022.0 s ≈ 17m 2.0s
(≈ ~17m 2s).

Recent history (carry-forward):

- chunk_2018 was branch (b) at execution closure (flat/improved vs the prior
  anchor; preserved as transient improvement; watch kept active)
- chunk_2018 was the first reversal of the slowdown trend, at −14.9% vs
  chunk_2017
- the ~2.8 s/URL anchor is preserved as a transient improvement, not promoted
  to a new structural baseline
- watch remains active for chunk_2019

Three-branch interpretation for the future chunk_2019 execution-closure stage:

- (a) if chunk_2019 observed s/URL is ≥ ~3.4 s/URL, bump the anchor at
  execution closure
- (b) if chunk_2019 is flat or improved versus chunk_2018, preserve the
  current ~2.8 s/URL anchor as a transient improvement and keep the watch
  active
- (c) if a slowdown resumes but remains below the bump trigger, preserve the
  anchor and keep the watch active

## 8. Substrate-gap diagnostic expectation

Carry-forward state (unchanged by this memo):

- `KNOWN_SUBSTRATE_GAPS` canonical dates surfaced by the runner:
  `["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]`
- known_substrate_gap_dates = `["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]`
- substrate_gap_dates_not_fetched = `["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"]`
- not `[]` / `[]`
- fourth-empirically-validated across chunks 2015, 2016, 2017, and 2018

For chunk_2019, the expected semantic interpretation is: there are zero
in-range 2019 substrate gaps (the canonical gap dates are all 2014, fully
outside the chunk_2019 date range), while the runner unconditionally surfaces
the global `KNOWN_SUBSTRATE_GAPS` tuple. A future chunk_2019 live-execution
report must therefore continue to record both fields with the canonical
four-date / four-date shape, and **must not silently treat `[]` / `[]` as
equivalent** to that canonical shape. Any future deviation from the canonical
four-date / four-date shape on chunk_2019 must be treated as a diagnostic
event, not as routine.

## 9. Boundary conditions for future live execution

Future chunk_2019 live execution is **not** authorized by this memo. Future
live execution requires a separate user initiation and a separate
live-execution authorization prompt.

The future live-execution prompt must preserve all of the following, none
weakened:

- no retry
- exactly-once
- no off-session execution
- no checkpoint / no resume
- no bounded parallelism
- no raw payload preservation
- no prior-chunk rerun
- no merge
- no Step 2
- no market-data access
- no instrument construction
- no memory edit during live execution

## 10. Expected future output shape (for future live execution only)

The following is the **expected** shape for a future chunk_2019 live
execution. Nothing in this section authorizes such execution; it is recorded
here so the future live-execution preflight and execution-closure stages can
cross-check against this memo.

Expected output directory pattern:

`results/lane2_gdelt1_full_daily_count_build/chunk_2019_<UTC>/`

Expected files inside that directory:

- `chunk_contributions.csv`
- `chunk_metadata.json`
- `chunk_summary.md`

Expected absences:

- no raw payloads
- no `halt_diagnostic.json` on success

The future chunk_2019 execution report must record (at minimum):

- output directory
- artifact sizes
- artifact SHA-256s
- chunk manifest digest
- `total_in_window_rows`
- `total_out_of_window_rows`
- `total_parsed_rows`
- row arithmetic check (`total_in_window_rows + total_out_of_window_rows = total_parsed_rows`)
- runtime
- substrate-gap diagnostic (per Section 8)
- boundary preservation
- guards restored false after run
- runner byte-identity restored after run
- push state (if/when applicable)
- on-disk execution report SHA-256, computed at execution-closure preflight,
  per chunk_2018-established discipline; this gap was originally identified
  at chunk_2017 closure and closed at chunk_2018 closure

## 11. Carry-forward discipline

Unresolved items: 1 (Section 9 / commit-report cosmetic observation, now 4
cycles unresolved; non-load-bearing).

Established disciplines carried forward (8 items, (a)–(h)):

- (a) literal-anchor cross-check against actual memo/report text
- (b) digest hit counts are structural/context-dependent;
  byte-count-not-identity caution reinforced
- (c) URL / no-URL canonicalization: the URLs form is the canonical strict
  anchor form
- (d) planning-closure memory updates record planning memo file SHA-256 from
  chunk_2017 forward
- (e) execution-closure memory updates record artifact sizes + SHAs
- (f) execution-closure memory updates record `total_in_window_rows` and
  `total_out_of_window_rows` when surfaced by the runner
- (g) HEAD / origin/main / SHA literals appear as contiguous prose strings
  (never split across table columns)
- (h) prompt-transport integrity: avoid nested fence delivery-truncation risk

7-item non-weakening canon (carry-forward, none weakened):

1. no-retry
2. exactly-once
3. no-off-session
4. no-market-data
5. no-Step-2
6. no-checkpoint-resume
7. no-bounded-parallelism

## 12. Next frontier after this planning memo creation

After this planning memo is created, the next eligible action is **not**
automatic execution. The next sub-cycle is:

> chunk_2019 planning memo content review / sanity-check

Only after content review, and a subsequent commit/push plus the
planning-closure memory update, would chunk_2019 live-execution authorization
become eligible. No live execution is authorized by this memo creation.
