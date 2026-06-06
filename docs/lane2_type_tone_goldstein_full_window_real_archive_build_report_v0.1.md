# Lane 2 — TTG Full-Window Real Archive Build Report v0.1

## Verdict

**FULL-WINDOW ARCHIVE BUILD COMPLETED** (real, value-blind, gate-closed after run).
The separately-authorized full-window real archive rerun over `2013-04-01 …
2022-12-31` ran to completion under the reviewed missing-source retry/allowlist
amendment, using the streaming `run_bounded_integrity_build` path with the explicit
operator allowlist `{"2022-11-10"}`. The isolated April-2013 reproduction matched
`c077edc6…` exactly. The gate was armed for exactly one window and reverted; module
identities are restored. **This authorizes nothing beyond the archive build — no
extraction, features, statistics, joins, outcomes, market data, V1/V2, or
pre-registration-gated work. Not pushed.**

A count nuance (distinct-written SQLDATEs 3546 vs coverage-ledger 3549) is
**legitimate and fully explained** in §Coverage below; it is not a fail-closed
condition.

## Preflight anchor (verified before arming)

| Field | Value |
|---|---|
| HEAD | `5c25ca2911feb234e4c48643bf16caa3a3883ce5` |
| Parent | `91c9f2bd23241370939d3ce199643a66b1827568` |
| origin/main | `fb26424c92ad30a52f579ec4a1dd8a2b069c2cb0` |
| ahead/behind | `0 18` |
| fetch module (committed==worktree) | `98bc35ac8dd26824db1e8786ad7bff093fb562f9cedbadeecc1995252194b006` |
| local archive (committed==worktree) | `6a3d715e078c796391a930270c1f34a086e6ef9df2d663752d1922241ee5f40d` |
| gate before | `REAL_FETCH_SOURCE_GATE_ENABLED = False`; zero active `= True` in source |
| tracked diff before | none |
| cache/output paths | gitignored |

## Run authorization

- **Gate one-line arm proof:** `git diff --numstat` of the fetch module showed
  exactly `1 1` (line 54 `REAL_FETCH_SOURCE_GATE_ENABLED = False` → `True`); no
  other line changed.
- **One armed window:** full-window build → isolated April reproduction → single
  gate revert, all inside one armed window (no revert-then-rearm).
- **In-process revert proof:** the run harness `finally` rewrote line 54
  `True`→`False` (`in_process_revert_applied = true`).
- **Outer checkout proof:** unconditional `git checkout -- src/lane2_type_tone_goldstein_archive_fetch_path.py`
  after the run; post-revert `git diff --stat` empty.
- **Run guards:** module_authorized=True, cli_flag=True, env
  `LANE2_TTG_LOCAL_ARCHIVE_BUILD_AUTHORIZED=1`.
- **Explicit allowlist:** `fetch_absent_allowlist=["2022-11-10"]` passed at runtime
  (not a committed default; source unchanged — no baked-in date).
- **Real mode (no synthetic seams):** `md5sums_bytes=None`, `filesizes_bytes=None`,
  `manifest_fetch_callable=None`, `fetch_callable=None`; manifests acquired via the
  gated `_open_url` (`manifest_source_mode = gated_open_url_default`); daily zips via
  the gated fetch. No fake fetchers/manifests.

## Disk / resource record

- Free before: 79.07 GB (~73.6 GiB). Stale prior-run `.partial` (18.41 GB) removed
  from the pinned ignored output dir (path + byte size recorded; content not read).
  Note: APFS snapshot/purgeable accounting did not immediately reflect the freed
  18.41 GB, so feasibility was evaluated against raw free (73.6 GiB), which already
  satisfied 1.5× of the ~19.5 GB remaining footprint and the ≥25 GiB-after floor.
- Free after run: 60.17 GB (~56.0 GiB) — ≥ 25 GiB. PASS.
- Cache after: 3557 verified daily zips.
- No final promoted archive/manifest existed before the rerun (confirmed).

## Coverage

### Source manifest reconciliation
- Source window dates: 3562
- Present-in-both: 3558; absent-in-both (mutual gaps): 4; single-manifest-only: 0
  (`reconciled_ok = true`).

### Fetched source files
- Real daily zips verified after rerun: **3557** (= 3558 present-in-both − 1
  allowlisted fetch-absent `2022-11-10`; cache holds 3557). No synthetic substitute
  for `2022-11-10`.

### Tolerated mutual-absence source gaps (4)
`2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`.

### Operator-allowlisted manifest-present fetch-absent source date (1)
`2022-11-10` — stable HTTP 404 during the run, classified as a deliberate
operator-allowlisted fetch-absent gap (explicitly supplied), build continued. No
new unknown manifest-listed-but-unavailable day occurred (none tolerated implicitly).

### Coverage-loss SQLDATEs (11)
- Mutual-absence `2014-01-23/24/25` → `2014-01-22 … 2014-01-26` (5)
- Mutual-absence `2014-03-19` → `2014-03-18`, `2014-03-19`, `2014-03-20` (3)
- Allowlisted fetch-absent `2022-11-10` → `2022-11-09`, `2022-11-10`, `2022-11-11` (3)

### Edge exclusions (2)
- `2013-04-01` excluded — would require pre-window `2013-03-31` (never contacted).
- `2022-12-31` excluded — would require sealed `2023-01-01` (never contacted).

### Primary counts — two metrics, reconciled
- **Nominal primary window:** `2013-04-02 … 2022-12-30` = 3560 SQLDATEs.
- **Coverage-ledger actual primary (date-based, the dispatch's metric):**
  `coverage_summary.covered_count = 3549` = 3560 − 11 coverage-loss. **This matches
  the dispatch's expected 3549 and the expected per-year table exactly**, including
  the leap-year **2020: 366**:

  | year | ledger-covered | dispatch expected |
  |---|---|---|
  | 2013 | 274 | 274 |
  | 2014 | 357 | 357 |
  | 2015 | 365 | 365 |
  | 2016 | 366 | 366 |
  | 2017 | 365 | 365 |
  | 2018 | 365 | 365 |
  | 2019 | 365 | 365 |
  | 2020 | 366 | 366 |
  | 2021 | 365 | 365 |
  | 2022 | 361 | 361 |
  | **total** | **3549** | **3549** |

- **Distinct-written SQLDATEs (row-presence):** 3546 (per-year identical to the
  table above except **2020: 363**). The 3-date difference is **legitimate**:
  SQLDATEs `2020-01-01`, `2020-01-02`, `2020-01-03` are coverage-covered (all of
  their `{t-1,t,t+1}` support files are present and verified) but have **zero
  eligible event rows**, so no rows are written for them.

#### Why `2020-01-01/02/03` have zero eligible rows (legitimate, not fail-closed)
The 2020 new-year boundary daily files are all present and **verified**
(`integrity_status = verified`, `column_count_mismatch = 0`) but contain
historically/stale-dated events (a known GDELT 1.0 early-January-2020
reprocessing/backfill) that fail the **pre-existing no-lookahead eligibility rule**
`source_file_date ≤ SQLDATE + 1`. Structural per-file drop counts:

| source file | raw rows | retained | date_eligibility_failure |
|---|---|---|---|
| 2019-12-31 | 125858 | 123418 | 2440 |
| 2020-01-01 | 89215 | 331 | 88884 |
| 2020-01-02 | 123425 | 0 | 123425 |
| 2020-01-03 | 157403 | 0 | 157403 |
| 2020-01-04 | 112518 | 0 | 112518 |
| 2020-01-05 | 112046 | 46528 | 65518 |
| 2020-01-06 | 158919 | 154815 | 4104 |

The rows were dropped by the locked eligibility rule (not by the amendment, not
silently, with **no patching/inference/synthesis/backfill** — which are forbidden).
The coverage ledger correctly counts these dates as covered (support files present);
the archive correctly contains no rows for them (no eligible data). Both metrics are
faithful: the date-based coverage matches the dispatch (3549); the row-presence
count is 3 lower for this documented real-data reason. **No other year has any
zero-eligible-row covered date.**

## Archive identity

- **Full-window archive SHA-256:** `06dcbc2530deb9fb25dc87b651f3012fe7de21474235c0f85c7ddd53b604383b`
- **Byte size:** 18,565,733,712
- **Row count:** 505,818,607
- **Provenance manifest file SHA-256:** `7f8daf4bd52f987427ec371ba21e5418c7d2cfe269e93171a1fca47935e0646a` (4,282,699 bytes)
- **Official manifest provenance (acquired via gated `_open_url`):**
  - `md5sums` SHA-256 `bbab009c3b8c9572daf7de43dfb6e84517525e5f301d4a1c0e83863e71cc87fc` (283,024 bytes)
  - `filesizes` SHA-256 `d4eba2e2a2a370f1a0ab1c3e3f7eb18eb1a8b0bcf5c1712946f1b9e578b4f5c6` (157,407 bytes)
- Archive + manifest written to the **gitignored** output dir
  `results/lane2_type_tone_goldstein_full_window_real_archive_build/`; atomic
  temp→final promote (final published only on success). Not committed.

### Isolated April `c077edc6…` reproduction
Run under the **standalone isolated April configuration** (source window
`2013-04-01 … 2013-04-30`; isolated-slice primary `2013-04-02 … 2013-04-29` = 28
SQLDATEs), cache reuse of the 30 April zips, no `2013-03-31`, no `2013-05-01`, no
`2023+`. Result:

| metric | value | expected |
|---|---|---|
| archive SHA-256 | `c077edc6d4e0214797d001fdd8b1601a791868bf05fe84732dbd48cdfc716238` | `c077edc6…716238` |
| byte size | 31,166,630 | 31,166,630 |
| row count | 895,932 | (prior cleared) |
| **match** | **PASS (full)** | |

**Explicitly checked using the standalone isolated April configuration, NOT the
full-decade build's internal April rows.** In the full-decade build `2013-05-01` is
an interior source date, so full-decade April-internal coverage correctly extends
through primary SQLDATE `2013-04-30`; that difference is expected and is not a
regression. The isolated April value-bearing output was written to a `/tmp` scratch
dir and deleted after capturing the SHA (never read, never included in any
report/bundle).

## Streaming / integrity

- `ELIGIBILITY_DELTA_DAYS (edd)` = 1
- `streaming_release_depth` = 2 (= 2·EDD)
- `max_buffered_source_file_blocks` = **3** (= 2·EDD+1; fixed bound, no growth with
  window length) — within bound.
- retained-offset hard-fail count = **0** (no `RetainedOffsetHardFail`).
- `agg_column_count_mismatch` = **0** (exact-58 conformance held for every file).
- `per_file_all_verified` = true; `per_file_exact58_ok` = true.
- Aggregate row accounting (structural): raw 520,155,060; date_eligibility_failure
  13,682,957; edge_window_exclusion 82,013; classify_retained 506,390,090;
  archive rows 505,818,607 (the 571,483 classify-retained-but-not-written rows
  belong to the coverage-loss / slice-edge SQLDATEs).
- Atomic temp→final promote for both archive and provenance manifest; final
  artifacts published only on success.
- `boundary_declarations.streaming_archive_write = true`; no production whole-window
  accumulator used (streaming buffer + writer only).

## Retry / 404 behavior observed

- Bounded retry/backoff config: `max_transient_retries=4`,
  `retry_backoff_base_seconds=2.0`, `stable_404_recheck_count=1`, `fetch_attempts=2`.
- The 51 uncached tail files (`2022-11-11 … 2022-12-31`) were fetched and verified;
  `2022-11-10` returned a stable HTTP 404 and — with the explicit allowlist — was
  classified as an operator-authorized fetch-absent gap and the build continued. No
  other present-in-both date 404'd; no unknown 404 tolerated; no transient exhaustion.

## Module identities (after run)

| Module | committed | worktree | match |
|---|---|---|---|
| fetch_path | `98bc35ac…194b006` | `98bc35ac…194b006` | ✓ |
| local_archive | `6a3d715e…1ee5f40d` | `6a3d715e…1ee5f40d` | ✓ |

Gate final: `REAL_FETCH_SOURCE_GATE_ENABLED = False`; zero active `= True` in source.

## Boundary confirmations

- No extraction; no TTG feature computation; no statistics/buckets/correlations/
  regressions/scores/model metrics/diagnostics beyond archive-build structural
  metadata.
- No outcome reads; no market reads; no joins; no V1/V2.
- No `2013-03-31` contact; no `2023-01-01`/`2023+` contact (both edges excluded by
  the coverage rule, never fetched).
- No patching/inference/synthesis/backfill of missing event data; the 4 mutual
  gaps and the 1 allowlisted fetch-absent date carry no synthetic substitute; the
  `2020-01-01/02/03` zero-eligible-row dates were not backfilled.
- Value-blind: structural/provenance metadata only; the report contains no event-row
  values, no `SOURCEURL`, no archive bytes.
- Report-doc-only commit; not pushed.

## Next step

External byte-review of the rerun bundle. Even though the archive build succeeded,
the next step is review only — extraction, feature work, statistics, joins,
outcomes, market reads, V1/V2, and any pre-registration-gated work remain
**unauthorized**.
