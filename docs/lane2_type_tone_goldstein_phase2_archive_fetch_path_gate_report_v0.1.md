# Lane 2 / Type-Tone-Goldstein — Phase-2 archive-build fetch-path gate report v0.1

`PHASE-2 FETCH-PATH IMPLEMENTED (SYNTHETIC-PROVEN); NO REAL NETWORK CONTACT; NO REAL ARCHIVE BUILD; REAL-FETCH DISABLED BY A NON-RUNTIME SOURCE GATE; EXTRACTION STILL BLOCKED; NO PUSH`

This report records the implementation of the Phase-2 real fetch/archive-build
*path* (code + synthetic proof) for the Lane 2 / Type-Tone-Goldstein (TTG) local
approved-fields archive. It authorizes **no** real GDELT network contact, **no**
real archive build, **no** TTG extraction/feature/statistic, **no** join, **no**
outcome/market read, **no** V1/V2 execution, and touches **no** 2023+ data. The
real GDELT fetch is present in source but disabled by a source-level gate that
no runtime configuration can flip.

## 1. Preflight state

```
HEAD                         cd29b72
origin/main                  fb26424
origin/main...HEAD (L/R)     0    7   (local ahead by 7; no push)
status --short               two pre-existing untracked docs only:
  ?? docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md
  ?? docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md
```

Matches the expected state (HEAD `cd29b72`, origin/main `fb26424`, ahead 7, no
push, no unexpected tracked changes). Proceeded.

## 2. Governing artifacts read

- `docs/lane2_type_tone_goldstein_local_approved_fields_archive_design_memo_v0.1.md` (content SHA-256 `c97e5593…`, the value pinned by the module) — Path 1a (build a local approved-fields archive first), five approved fields (§7), forbidden set (§8), network-as-separate-boundary (§9), value-blind rule and irreversible-read accounting (§12), separate-authorization sequencing (§16).
- `docs/lane2_gdelt1_event_codebook_reference_v0.1.md` (content SHA-256 `3c5fa5bc054fbefaea2a26f9700ee827f2ff86a059d1625ffa127b10bf035a58`, 329 lines — verified equal to the value pinned in the availability amendment §14) — V1.03 codebook positional indices (§7/§8) and the corroborating daily-updates header (§3).
- `docs/lane2_type_tone_goldstein_availability_timing_amendment_v0.1.md` — `file_date <= SQLDATE + 1` eligibility (§6), fully-covered predictor-window rule and edge consequences (§7), file/update date as the availability instrument (§8), DATEADDED forbidden as instrument (§9), five-field schema preserved / per-row file-date not retained (§10), value-blind reporting (§11), Phase-2 implementation requirements and synthetic-proof-before-fetch (§15).
- `docs/lane2_type_tone_goldstein_local_archive_phase1_conformance_report_v0.1.md` — Phase-1 scaffold, the three-guard run gate, "network impossible by construction in Phase 1", and that Phase-2 network enablement requires a reviewed code change.
- `docs/lane2_type_tone_goldstein_outcome_side_join_gate_locks_v0.1.md` and `docs/lane2_type_tone_goldstein_outcome_basis_close_field_resolution_v0.1.md` — read-only, for the §5 outcome-convention inspection only (not edited).
- The document added by commit `084c5bd` = `docs/lane2_type_tone_goldstein_outcome_basis_close_field_resolution_v0.1.md` (same as above).
- `src/lane2_type_tone_goldstein_local_archive.py`, `scripts/run_lane2_type_tone_goldstein_local_archive_build.py`, `tests/test_lane2_type_tone_goldstein_local_archive.py`.

### Governing constraints extracted

- Retain exactly five approved fields; never retain/compute on any forbidden field; never compute any function over the four substantive fields during build.
- Network is a separate boundary from extraction; the archive build is the only step (later, separately) permitted any GDELT contact, and only to populate the approved-fields archive; TTG extraction is local-only thereafter.
- Predictor eligibility: `source_file_date <= SQLDATE + 1`; late-arriving lookback buckets excluded; edge-incomplete predictor days excluded from the primary or routed to a separately governed diagnostic set; 2023+ seal absolute; pre-window files never read.
- DATEADDED is forbidden as an availability instrument and as a retained field; row-level SOURCEURL is forbidden as a retained field; the per-row schema stays five fields; the file/update date is recorded only at per-file manifest/status level.
- Build output is structural/provenance only (value-blind); no value summaries, no sample rows.
- Each gate (real fetch, archive build, extraction, join) requires its own separate authorization; approving one does not authorize the next.

## 3. Blind codebook / index extraction

Indices were re-extracted **independently from the committed codebook reference**
(this prompt supplied no expected values). Method: read the V1.03 codebook
record-order table (primary) and the daily-updates header tab-split (corroborating)
in `docs/lane2_gdelt1_event_codebook_reference_v0.1.md`, and read the 1-based
ordinal → Python 0-based conversion (`idx = ordinal − 1`).

| Field | Primary source (V1.03 table) | Corroborating source (daily-updates header) | Python idx |
|---|---|---|---:|
| SQLDATE | line 128 (ord. 2) | line 66 (`py-idx 1`) | **1** |
| QuadClass | line 156 (ord. 30) | line 67 (`py-idx 29`) | **29** |
| GoldsteinScale | line 157 (ord. 31) | line 68 (`py-idx 30`) | **30** |
| NumMentions | line 158 (ord. 32) | line 68 (`py-idx 31`) | **31** |
| AvgTone | line 161 (ord. 35) | line 69 (`py-idx 34`) | **34** |
| DATEADDED | line 171 (ord. 57) | line 225 (idx 56) | **56** |
| SOURCEURL | line 172 (ord. 58) | line 69 (`py-idx 57`) | **57** |

The two committed sources **agree**; no cross-source conflict was found, so no
stop condition fired. The approved retained schema is exactly `{sqldate:1,
quadclass:29, goldsteinscale:30, nummentions:31, avgtone:34}`; DATEADDED (56) and
SOURCEURL (57) are forbidden and excluded. The build verifies the module
constants against this independently-derived map and **fails closed** on mismatch
(`archive.assert_codebook_indices`; test `test_codebook_index_mismatch_fails_closed`).

## 4. Predictor-internal `+1` seam handling

A single `source_file_date` rule is implemented and documented:

- `source_file_date` (`F`) is parsed from the source filename / download-URL
  leading `YYYYMMDD` token (`archive.parse_source_file_date`);
- it is treated as the GDELT update-file civil date;
- it is **not** derived from DATEADDED, **not** from download time, and **not**
  shifted again by local timezone or by an extra `civil_date + 1` transform.

The `+1` appears **exactly once**, in the eligibility inequality
`F <= SQLDATE + ELIGIBILITY_DELTA_DAYS` with `ELIGIBILITY_DELTA_DAYS == 1`
(`archive.row_is_eligible`). The predictor archive is keyed by the raw SQLDATE;
no second bucket shift / `civil_date+1` re-key is applied. The double-shift hazard
is guarded by test `test_no_double_shift_of_eligibility`: a `SQLDATE = t` row
arriving in file `F = t+1` is eligible and retained **keyed at `t`** (not `t+1`),
and `F = t+2` is ineligible (a second `+1` would wrongly admit it).

**`source_file_date <= SQLDATE + 1` is provisional for archive build** and
remains subject to extraction-gate reconciliation against: GDELT 1.0 daily-update
publish time-of-day; the committed outcome return-measurement convention; and
whether the outcome is `close(t+1)→close(t+2)`, `close(t)→close(t+1)`, or
open-anchored. This prompt resolved only the predictor-internal double-shift
hazard for archive-build code.

## 5. Predictor-vs-outcome seam status

**Still open until the extraction gate.** The predictor-side eligibility rule does
not settle predictor↔outcome temporal alignment. The committed outcome docs (see
§7) define the outcome relative to a market anchor session `s` with `t ≡ s = d+1`
(where `d = civil_date = SQLDATE`), whereas the archive's `t` is the SQLDATE `d`
itself. Reconciling which session is labeled `t` — and the publish-time-of-day
basis for `F <= SQLDATE + 1` — is an extraction-gate question, not resolved here.

## 6. Outcome-convention paper inspection (read-only)

Inspection used committed docs and git metadata only; **no** outcome/market/join
data, result files, or generated datasets were opened (enforced/witnessed by
`test_no_outcome_market_join_reads_in_modules` — the modules contain no
`adj_close` / `pct_change` / `join_gdelt_spy` / `market_daily` / outcome-file
read).

**Classification: SETTLED as a close-to-close log return (not open-anchored), but
expressed in an anchor-session frame that differs from the predictor SQLDATE
frame.**

- `docs/lane2_type_tone_goldstein_outcome_basis_close_field_resolution_v0.1.md`
  (`084c5bd`) §7: `next_session_return_s = ln(close_{s+1} / close_s)`; primary
  outcome `abs(next_session_return_s)`; arithmetic / `pct_change()` not governing.
  §8: close field = raw `close`.
- `docs/lane2_type_tone_goldstein_outcome_side_join_gate_locks_v0.1.md` §5
  (governing worked mapping): `m = d+1`; anchor `s = d+1`; `t ≡ s`; the
  contemporaneous anchor-session return `r_s` is **excluded**; **primary outcome
  `r_{d+2} = ln(close_{d+2}/close_{d+1})`**, primary absolute `abs(r_{d+2})`.

So, in the doc's anchor-session frame (`t ≡ s`), the outcome is
`close(t)→close(t+1)`; equivalently, in the predictor SQLDATE/civil_date frame
(`t = d`), it is **`close(t+1)→close(t+2)`** (= `close(d+1)→close(d+2)`). It is
**not** open-anchored and **not** substantively ambiguous; the only ambiguity is
which session carries the label `t`, which is exactly the §5 predictor-vs-outcome
seam that the extraction gate must reconcile.

Paths/anchors supporting this: `084c5bd` §7/§8 (lines 58–70, 73–80); join-gate
locks §4–§5 (lines 42–76); HAR-RV `fb26424` §9 (raw-`close` log RV) as referenced
in those memos.

**Outcome-doc defect found (report-only, governing doc left untouched):** the
join-gate locks memo §1 (line 14) and Anchors line (line 9) abbreviate the stale
HAR-RV leg as `3b32129256562562...`, which is not the full 40-hex SHA recorded
elsewhere for `3b32129` (`3b32129256562ef1b879fad6c6a42bb2689bd5` family). This is
a cosmetic truncation/typo in a superseded-leg citation; it does not affect the
active `fb26424` leg or the outcome convention. **Reported only; not edited.**

## 7. File-date provenance / source-file universe (build input)

Pinned as a build input (manifest `source_file_window` + module constants):

- **Source-file date range:** `2013-04-01` … `2022-12-31` (Lane 2 in-sample GDELT
  1.0 daily-regime window; `archive.WINDOW_START`/`WINDOW_END`).
- **URL / date-token template:** download URL = `<base>` + `{yyyymmdd}.export.CSV.zip`
  (`fetch_path.build_source_file_url`, base `GDELT1_EVENT_BASE_URL`); the
  filename token is the `YYYYMMDD` source/update date.
- **Universe is generated deterministically** per in-window civil day from the
  `YYYYMMDD` template (no listing-page scrape required); `enumerate_source_universe`
  sorts/de-dups and hard-errors on any 2023+ or pre-window date **before** any open.
- **No 2023-01-01-or-later files** are enumerated/opened (`Post2022SealBreach` at
  enumeration; defense-in-depth at content-row parse).
- **No pre-window files** (`2013-03-31` or earlier) are enumerated/opened, including
  to complete first-day coverage (`enumerate_source_universe` rejects pre-window).
- **Missing/unavailable files in a future real run** would be recorded per-file as
  `attempted`/`opened`/`error_status` provenance; the build does not fabricate
  rows for an unavailable file (fail-closed accounting).
- **Source file date parsing:** leading 8-digit token of the filename/URL, never
  DATEADDED / download time / tz-shifted.
- **Future manifest records each attempted source file** via
  `build_per_file_provenance_entry`: `source_file_date`, `source_file_url`,
  `attempted`, `opened`, `byte_sha256`/`byte_size` (real run only), `raw_row_count`,
  `retained_row_count`, `dropped_by_reason{closed set}`, `coverage_status`,
  `error_status`.

**File-download URL vs row-level SOURCEURL:** the **file-download URL**
(`source_file_url`, built from base + filename) is provenance metadata and is
allowed in the manifest. The **row-level GDELT `SOURCEURL`** field (codebook idx
57) is forbidden and never retained as a row column. The two namespaces are kept
separate in code, manifest, and tests
(`test_download_url_provenance_allowed_distinct_from_sourceurl`,
`test_sourceurl_and_dateadded_not_retained`).

## 8. Implementation summary

Two source files changed plus one new test file; no generated outputs.

- `src/lane2_type_tone_goldstein_local_archive.py` — added **network-free** Phase-2
  pure logic: `parse_source_file_date`, `row_is_eligible` (`F <= SQLDATE+1`),
  `is_sqldate_fully_covered` (window-coverage), forbidden index constants
  (DATEADDED 56 / SOURCEURL 57), the closed drop-reason set `CLOSED_DROP_REASONS`,
  `classify_payload_rows` (retained rows + value-agnostic drop counts),
  `build_per_file_provenance_entry`, `build_phase2_provenance_manifest`, and
  `assert_codebook_indices` (fail-closed). The module still imports no network
  library and contains no URL literal (verified: token scan CLEAN); all 19 Phase-1
  tests still pass unchanged.
- `src/lane2_type_tone_goldstein_archive_fetch_path.py` (new) — the reviewed
  network module: source gate, `RealFetchNotAuthorized`, `build_source_file_url`,
  the gated `fetch_one_source_file`, `_open_url` (lazy `urllib` only after the
  gate), and `run_phase2_archive_build` orchestration (codebook-verify → three-guard
  run gate → enumerate → per-file fetch via an **injected** fetcher → classify →
  write archive + value-agnostic provenance manifest). The default fetcher is the
  gated real fetch, which hard-errors.
- `tests/test_lane2_type_tone_goldstein_fetch_path.py` (new) — synthetic tests
  covering all 21 §11 requirements (24 test items; `test_late_rows_dropped` is
  parametrized over four late offsets).

**Build pipeline (synthetic only here):** all end-to-end pipeline tests inject an
in-memory synthetic fetcher; the real fetcher is never invoked with the gate
enabled, so no URL is ever opened.

## 9. Non-runtime real-fetch source gate

`REAL_FETCH_SOURCE_GATE_ENABLED = False` is a hard-coded boolean literal in the
fetch module. Properties (all tested):

- The real fetch entrypoint checks the gate **first** and raises
  `RealFetchNotAuthorized` before building any URL, importing any network library,
  or opening any connection (`test_real_fetch_hard_errors_before_url_open`, with a
  spy on `_open_url` that records zero calls).
- The gate is **not** reachable via runtime configuration: setting
  `REAL_FETCH_SOURCE_GATE_ENABLED`, `LANE2_TTG_LOCAL_ARCHIVE_BUILD_AUTHORIZED`,
  `TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED`, `ENABLE_REAL_FETCH` in the
  environment, and passing arbitrary parameters, still hard-errors; the assignment
  is a single literal `= False` with no env/CLI/config/`bool(...)`/`open(...)`
  derivation (`test_gate_not_reachable_via_runtime_config`).
- Even with the three runtime build-run guards all satisfied and the default
  (real) fetcher, the build aborts at the gate before any network contact
  (covered by `test_2023plus_rejected_at_enumeration` /
  `test_pre_window_files_not_opened`, which use a fetch spy showing zero calls, and
  by the gate-first ordering above).
- `urllib` is imported **lazily inside `_open_url`** (line 145), which is reached
  only after the gate passes; with the shipped gate, no network library is imported
  at all (`test_source_gate_ships_false_and_no_network_lib_imported`).

Enabling real fetch therefore requires editing the source gate line **and** a
separate execution authorization; it cannot be flipped by env var, CLI flag,
config file, settings file, or parameter.

## 10. Manifest value-agnostic contract

The provenance manifest carries structural/provenance fields only: source-file
window pin, eligibility rule string, per-file provenance (date, download URL,
attempted/opened, byte hash/size, raw & retained counts, dropped-by-closed-reason,
coverage status, error status), archive artifact hashes, the approved schema
(names/types), and boundary declarations. Closed drop reasons:
`malformed_row`, `short_row`, `field_parse_failure`, `date_eligibility_failure`,
`source_file_outside_authorized_universe`, `edge_window_exclusion`,
`forbidden_field_retention_violation`, `duplicate_provenance_integrity_failure`.

Forbidden content is absent and tested: no counts bucketed by QuadClass /
GoldsteinScale / NumMentions / AvgTone, no sign or tone or Goldstein buckets, no
value distributions, no sample/preview/retained-row examples, no statistic over
substantive values (`test_manifest_structural_only_no_value_summaries`,
`test_manifest_counts_value_agnostic`). Per-file retained row count is a single
structural integer (volume/provenance), never partitioned by field value. The
manifest is deterministic from the pinned universe regardless of candidate
ordering (`test_provenance_manifest_deterministic`).

## 11. Synthetic tests

Command and result:

```
python3 -m pytest -q \
  tests/test_lane2_type_tone_goldstein_local_archive.py \
  tests/test_lane2_type_tone_goldstein_fetch_path.py
...........................................                              [100%]
43 passed in 0.18s
```

Broader regression (no collateral breakage):

```
python3 -m pytest -q tests/ -k "lane2"
588 passed, 596 deselected in 67.32s
```

Environment: Python 3.8.2, pytest 8.3.5. Requirement → test map (all 21):
1 `test_source_gate_ships_false_and_no_network_lib_imported`;
2 `test_real_fetch_hard_errors_before_url_open`;
3 `test_gate_not_reachable_via_runtime_config`;
4 `test_2023plus_rejected_at_enumeration`;
5/7 `test_eligibility_same_day_and_plus_one`;
6 `test_late_rows_dropped` (+ `test_far_late_file_outside_window_fails_closed`);
8 `test_no_double_shift_of_eligibility`;
9 `test_edge_incomplete_excluded_and_routable`;
10 `test_pre_window_files_not_opened`;
11 `test_dateadded_not_used_for_availability`;
12 `test_sourceurl_and_dateadded_not_retained`;
13 `test_download_url_provenance_allowed_distinct_from_sourceurl`;
14 `test_forbidden_fields_dropped_from_archive`;
15 `test_manifest_structural_only_no_value_summaries`;
16 `test_manifest_counts_value_agnostic`;
17 `test_short_and_malformed_rows_fail_closed`;
18 `test_codebook_index_mismatch_fails_closed`;
19 `test_provenance_manifest_deterministic`;
20 `test_no_outcome_market_join_reads_in_modules`;
21 `test_outcome_join_gate_docs_unmodified`.

## 12. Real fetch / build status and confirmations

- **No real fetch/build ran.** All pipeline tests inject a synthetic in-memory
  fetcher; the real fetcher is never invoked with the gate enabled.
- **No network contact occurred.** No GDELT event-data endpoint, no
  `.export.CSV.zip`, no index/listing page, no market/outcome/join source was
  contacted. `urllib` is imported only lazily inside `_open_url`, never reached.
- **Real-fetch enablement is not runtime-flippable** (see §9).
- **No outcome/join-gate governing doc was edited** — verified by content-SHA pins
  in `test_outcome_join_gate_docs_unmodified` (`95bb9596…`, `4cacb0b6…`). The §6
  defect was reported only.
- **No extraction / statistics / join / outcome / market / V1 / V2 / 2023+
  occurred.** The build computes no function over the four substantive fields; it
  copies approved values into the (not-built) archive and emits structural status
  only.

## 13. Final git status and files changed

Final `git status --short` and the explicit file list are recorded with the commit
(see the commit body). Files changed by this dispatch:

- `src/lane2_type_tone_goldstein_local_archive.py` (modified — network-free Phase-2 pure logic)
- `src/lane2_type_tone_goldstein_archive_fetch_path.py` (new — gated real fetch + orchestration)
- `tests/test_lane2_type_tone_goldstein_fetch_path.py` (new — synthetic tests, 24 items)
- `docs/lane2_type_tone_goldstein_phase2_archive_fetch_path_gate_report_v0.1.md` (new — this report)

No generated archive/results/data/raw output was created or staged.

## 14. Remaining blocked work

- **Real GDELT network contact** — blocked; requires editing the source gate
  **and** a separate execution-authorization prompt after byte review of this
  commit.
- **Real Phase-2 archive build** — not run; separate minimal dispatch.
- **TTG extraction** — still BLOCKED; requires a locked estimator-and-evaluation
  pre-registration before any value-level read.
- **Predictor-vs-outcome alignment seam** — still open (see §5/§4); extraction-gate
  reconciliation required (publish time-of-day + the settled outcome convention).
- **Outcome-side join** — still blocked.
- **No push** performed; local branch remains ahead of `origin/main` (now ahead 8
  after this commit).
