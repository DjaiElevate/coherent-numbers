# Lane 2 GDELT1 full-build chunk-design memo v0.1

## 1. Title

`Lane 2 GDELT1 full-build chunk-design memo v0.1`

This memo is **memo-only**. It authorizes no runner patch, no chunk-runner implementation, no test edit, no chunk execution, no full-build execution, no merge execution, no GDELT contact, no guard flip, no memory edit, no market data, no Step 2, no spike/burst threshold tuning, no return-window logic, no asset selection, no signal extraction, no 2023+ access, no raw payload preservation, no retry, no checkpoint/resume implementation, no off-session execution, no output-artifact mutation, no F4 modification, no recognized-list modification, and no staging/commit/push of this memo or any other artifact unless separately authorized after review.

## 2. Current anchor

| Item | Value |
|---|---|
| `HEAD = origin/main` | `fbc605bf0589268a8a635c3a6a1c68ceb533bd25` |
| Short SHA | `fbc605b` |
| Ahead count | `0` |
| Tracked tree | clean |
| Authoritative `FULL_BUILD_AUTHORIZED` line | `scripts/run_lane2_gdelt1_full_daily_count_build.py:95:FULL_BUILD_AUTHORIZED = False` |
| §10 recognized-list capture SHA-256 | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` |
| Authoritative Option D reserve-tier reference | `fbc605b` reconciliation memo (canonical: Option D = Plan-C reserve only) |

This memo is opened after `fbc605b`, which reconciled the Option D reserve-tier labeling inconsistency in the prior runtime-feasibility adjudication memo at `d7c8775`. The current artifact is **design-only**.

## 3. Purpose

This memo designs the **chunked execution path** selected by `d7c8775` Decision 2C after single-session sequential execution of the full-build runner was rejected (Decision 1B) as operationally unsuitable. The chunked path splits the 3,558-URL fetch set into ~10 yearly fetch-file chunks, each independently authorized, executed, and reported, with a separately authorized merge step that produces the final canonical full-build artifacts.

This memo is explicitly **NOT**:

- A runner patch (no edits to `scripts/run_lane2_gdelt1_full_daily_count_build.py` or `tests/test_lane2_gdelt1_full_daily_count_build.py`).
- An execution authorization for any chunk, the merge step, or the runner under any guard configuration.
- A GDELT-contact event (no URL constructed; no network call other than `git push` for any future commit step).
- A Step 2 authorization.
- A market-data authorization.
- A guard flip on any runner.

## 4. Inherited locked premises

The following premises are carried forward verbatim from prior locked memos (`7780a97`, `c10ae74`, `d7c8775`, `fbc605b`) and bind every chunk's per-URL behavior and the merge step's aggregation behavior:

1. **Recognized-list capture is the sole input authority** (SHA-256 `84ea721e…fff835fc`). No guessed dates; no index/listing fetch; no non-recognized URL construction.
2. **Output domain remains the full civil calendar `2013-04-01` through `2022-12-31`** (3,562 civil days). The final canonical `daily_count.csv` has one row per civil date over this domain — chunking does not change the output domain.
3. **SQLDATE aggregation is the primary key**: each event row contributes to its `SQLDATE`, not to the nominal publishing-file date. The merge step's per-SQLDATE summation across chunks is the operational expression of this premise.
4. **T+1 rows are kept and re-keyed uniformly to `SQLDATE`** (per `0065d10` Decision 1B). Not dropped, not specially corrected, not normalized away, not used as a basis for any downstream adjustment.
5. **Exact offset taxonomy** `{0, −1, −7, −30, −365, −3650, +1}` — exact-integer offsets only; no tolerance windows; any observed offset outside the set is hard-fail per the parser.
6. **Structural T−3650 zero**: T−3650 contributes structurally zero to every in-window primary-series date under the no-2023+ posture (per `7780a97` §10.2 explicit acceptance). Chunking does not change this; the merge step preserves it (every T−3650 row observed in any chunk's parsed file has a pre-2013 SQLDATE and routes to the out-of-window diagnostic).
7. **Known substrate gaps** (`2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`) remain `expected_absent_per_recognized_list` diagnostics; their SQLDATEs remain eligible in the output domain via neighbor contributions. Chunking does not imputation these.
8. **No filters, no weights, no category/theme/actor/geography/tone logic** (per `7780a97` §8 Decision C and `c10ae74` Decision C-Option-C firewall framing — filtering is Step 2 territory and forbidden in this design surface).
9. **No raw payload preservation** (per `7780a97` §15.11 mechanism: hash + parse + discard each payload before the next URL). Chunks inherit this verbatim.
10. **No retry** (per `7780a97` §13.4 / Decision I). Chunking does NOT introduce retries.
11. **No 2023+ URL construction or 2023+ SQLDATE acceptance in primary logic** (no-2023+ posture at `0ddbd51` + `7780a97` §11.1). Chunks inherit this verbatim.
12. **No-market-data firewall remains in force** unconditionally.
13. **Option D / off-session execution is Plan-C reserve only** (per `fbc605b` reconciliation memo §5.1). Not primary, not Plan-B. Plan-B reserve is Option A (checkpoint/resume). Neither A nor D is authorized by this memo.
14. **`c10ae74` adjudication amendments** remain binding per-chunk: 7-entry `coverage_quality_flag` closed domain including `t_minus_n_neighbor_substrate_gap`; `halt_diagnostic.json` allow-listed for halt-only derived-metadata emission.

## 5. Problem statement

The full-build runner at `bc7b66b` is **sequential-only** (zero concurrency primitives). The expected daily fetch count is **3,558**, with a sequential wall-clock estimated by `d7c8775` §4.3 at ~3.0 hours optimistic / ~4.9 hours realistic / ~7.9 hours conservative / ~14.8 hours pessimistic. The no-retry rule (Decision I) means any single transient HTTP failure aborts the run; at realistic per-URL success rate `p ≈ 0.999`, the probability of zero failures across 3,558 sequential URLs is `0.999^3558 ≈ 2.8%`, making first-pass completion in one uninterrupted session very unlikely.

`d7c8775` Decision 1B **rejected** single-session sequential execution as operationally unsuitable. `d7c8775` Decision 2C **selected** chunked execution as the next strategy. This memo designs that strategy.

**Important calibrations** (this memo does NOT claim chunking solves problems it does not solve):

- **Chunking does not magically remove the cumulative no-retry failure risk** across all 3,558 URLs. Across the entire build, the probability of at least one chunk's run halting on a transient HTTP/network failure remains roughly the same as before chunking, because the per-URL no-retry rule applies identically inside each chunk.
- **What chunking does provide**: (a) per-chunk wall-clock estimates (~30 min per chunk at 5 s/URL × ~356 URLs/chunk) fit within a normal Claude Code session; (b) failure-location isolation — a hard-fail in chunk_2018 does not invalidate the already-completed chunk_2013_partial / chunk_2014 / chunk_2015 / chunk_2016 / chunk_2017; (c) independent SHA-able per-chunk audit trail; (d) deterministic merge of successful chunks into the final canonical artifacts.
- **Any chunk failure remains a stop / adjudication event**, not an automatic retry trigger. A failed chunk requires a separately authorized memo (a checkpoint/resume design memo if Plan-B reserve is invoked, or a chain-of-custody memo if Plan-C reserve is invoked, or a different adjudication if neither).

## 6. Chunking basis

**Decision: use yearly fetch-file chunks, not output-SQLDATE chunks.**

### 6.1 Rationale for fetch-file-date chunks (not output-SQLDATE chunks)

- The live contact unit is the **publishing file URL**, not the output SQLDATE.
- Exactly-once fetch semantics apply at the URL level. Output-SQLDATE chunks would risk requiring the same publishing file to be fetched by multiple output chunks (because a publishing file emits rows that contribute to multiple output dates spanning multiple offsets).
- Fetch-file chunks allow each URL to belong to **exactly one chunk** — preserving exactness-of-fetch trivially.
- SQLDATE-keyed aggregation happens at merge time, where per-SQLDATE row contributions sum across chunks. This is consistent with the locked re-key premise from `0065d10` §5 and the merge-time coverage recomputation discussed in §10 below.

### 6.2 Primary chunk set (yearly fetch-file chunks)

| Chunk ID | Fetch-date start | Fetch-date end | Expected daily file count |
|---|---|---|---|
| `chunk_2013_partial` | `2013-04-01` | `2013-12-31` | **275** |
| `chunk_2014` | `2014-01-01` | `2014-12-31` | **361** (= 365 − 4 known substrate gaps) |
| `chunk_2015` | `2015-01-01` | `2015-12-31` | **365** |
| `chunk_2016` | `2016-01-01` | `2016-12-31` | **366** (leap year) |
| `chunk_2017` | `2017-01-01` | `2017-12-31` | **365** |
| `chunk_2018` | `2018-01-01` | `2018-12-31` | **365** |
| `chunk_2019` | `2019-01-01` | `2019-12-31` | **365** |
| `chunk_2020` | `2020-01-01` | `2020-12-31` | **366** (leap year) |
| `chunk_2021` | `2021-01-01` | `2021-12-31` | **365** |
| `chunk_2022` | `2022-01-01` | `2022-12-31` | **365** |
| **Total** | | | **3,558** |

Counts were derived by read-only Python inspection of the recognized-list capture at `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json` (SHA-256 `84ea721e…fff835fc`). The per-year counts equal civil-year days minus 0 (no gap dates in any year except 2014's 4 gaps). The sum equals the locked `3,558` expected daily fetches from `7780a97` §6.8 / `c10ae74` §4 / `d7c8775` §4.2.

Note: the chunk boundaries align with publishing-file calendar years. They do **not** align with output-SQLDATE calendar years; coverage flag computation must account for cross-chunk contributors at year boundaries (see §10).

## 7. Per-chunk execution unit

Each chunk is:

- A **named, non-overlapping** set of recognized daily publishing-file URLs (the per-chunk **manifest**).
- A **separately authorized execution unit** (one enable / single live run / restore / post-chunk report cycle per chunk, mirroring `3537a62 → 73a7911 → 858b501` discipline).
- **Not allowed** to fetch files outside its chunk manifest.
- **Not allowed** to fetch yearly recognized units (`"2005"`, `"2013"`) or monthly recognized units (`"2006-01"`, …, `"2013-03"`) — the 89 non-daily residual units from the recognized-list capture (per `bc7b66b`'s deterministic classification).
- **Not allowed** to fetch 2023+ URLs.
- **Not allowed** to retry failed URLs inside the chunk.

Each chunk must be defined with the following metadata fields (the chunk-runner patch will derive these from the recognized-list capture at runtime):

| Field | Description |
|---|---|
| `chunk_id` | e.g., `chunk_2013_partial`, `chunk_2014`, … |
| `fetch_date_start` | inclusive lower bound on publishing-file nominal date |
| `fetch_date_end` | inclusive upper bound on publishing-file nominal date |
| `expected_recognized_daily_file_count` | derived from §6.2 (e.g., 275 for `chunk_2013_partial`) |
| `chunk_manifest_digest` | SHA-256 of the sorted ASCII-encoded list of in-chunk URL strings (or equivalent deterministic digest) |
| `output_directory` | `results/lane2_gdelt1_full_daily_count_build/<chunk_id>_<UTC_TIMESTAMP>/` |
| `per_chunk_metadata` | `chunk_metadata.json` (see §8) |
| `per_chunk_summary` | `chunk_summary.md` (see §8) |
| `per_chunk_derived_contribution_table` | `chunk_contributions.csv` (see §8) |

## 8. Per-chunk artifacts

Each chunk's output directory contains **derived-only** artifacts. No raw compressed payloads, no extracted CSV rows.

### 8.1 Required per-chunk artifacts

- **`chunk_contributions.csv`** — SQLDATE-level count contributions observed from publishing files in that chunk only.
  - Columns: `civil_date`, `chunk_id`, `rows_from_offset_0`, `rows_from_offset_minus_1`, `rows_from_offset_minus_7`, `rows_from_offset_minus_30`, `rows_from_offset_minus_365`, `rows_from_offset_minus_3650` (structurally always zero in-window per `7780a97` §10.2), `rows_from_offset_plus_1`, `total_rows`.
  - May include SQLDATEs outside the final output window only for diagnostic completeness; the merge step will exclude such rows from the final primary series per §9.
  - Must NOT contain raw payload bytes, extracted CSV row text, or any non-derived data.
- **`chunk_metadata.json`** — derived metadata only:
  - `chunk_id`
  - `source_recognized_list_sha256` (= `84ea721e…fff835fc`)
  - `expected_file_count`
  - `actual_completed_file_count`
  - `chunk_manifest_digest`
  - `script_commit` (the chunk-runner's commit SHA)
  - `guard_state` (post-restore, must be `FULL_BUILD_AUTHORIZED = False`)
  - `started_at_utc`, `finished_at_utc`
  - `no_retry_confirmation: true`
  - `boundary_declarations` (mirroring `bc7b66b`'s `_boundary_declarations()`)
  - per-URL manifest with HTTP status, SHA-256 of fetched payload, per-offset row count, anomaly counts
- **`chunk_summary.md`** — human-readable summary (concise; mirrors the structure of `bc7b66b`'s `build_summary.md` but scoped to one chunk).
- **`halt_diagnostic.json`** — allowed only on hard-fail / halt paths, following `c10ae74` Decision 2A. Derived metadata only (`halt_class`, `message`, `started_at_utc`, `halted_at_utc`). NOT emitted on successful completion. NOT containing raw payload bytes or extracted CSV rows.

### 8.2 What per-chunk artifacts are NOT

- **Per-chunk successful output is NOT the final canonical `daily_count.csv`.** The final canonical `daily_count.csv` is produced **only** by the separately authorized merge step (§9), and only after all required chunks have produced successful per-chunk derived artifacts.
- Per-chunk `coverage_quality_flag` and `coverage_completeness`, if emitted at all, are **diagnostic only**. The merge step recomputes these flags using the full recognized-list-derived contributing-file cone (§10).
- Per-chunk artifacts remain **untracked by default** under the `7780a97` §15.10 Decision J (as amended by `c10ae74` Decision 2A for `halt_diagnostic.json` on hard-fail paths) and `0065d10` Decision 3A precedent. The final post-merge execution report is the only tracked artifact (drafted and committed by a separately authorized post-merge reporting step, not by the merge step itself; see §9.1 item 11 and §14 step 7).

## 9. Deterministic merge rules

The merge step is a **separate future authorization step**. It consumes only the per-chunk derived artifacts and produces the final canonical full-build artifacts.

### 9.1 Merge-step invariants

The merge step **must**:

1. **Read only successful per-chunk derived artifacts** from each chunk's output directory. The merge step does not perform any GDELT contact, fetch, or HTTP request.
2. **Refuse to merge if any required chunk is missing** (`chunk_2013_partial` through `chunk_2022`). All 10 chunks must be present and successful before merge proceeds.
3. **Refuse to merge if any chunk manifest digest mismatches** the recognized-list-derived expected manifest. The merge step recomputes the expected per-chunk manifest digest from the recognized-list capture (SHA `84ea721e…fff835fc`) and compares each chunk's recorded `chunk_manifest_digest` against the expected value.
4. **Refuse to merge if any publishing-file URL appears in more than one chunk's per-file manifest** (`DUPLICATE-FETCH-DETECTED` halt class). Chunk manifests are designed to partition the fetch set; cross-chunk duplicates are a structural failure.
5. **Refuse to merge if the union of chunk manifests does not equal the recognized-list-derived full daily fetch set** (3,558 URLs from the recognized-list capture minus the 4 known substrate gaps, equivalent to the union of the 10 chunks' expected manifests). Missing URLs (other than the 4 known gaps already excluded by recognized-list authority) are a hard failure.
6. **Sum SQLDATE count contributions across chunks**. For each civil date `d` in the output domain, `total_row_count[d] = Σ_chunks chunk_contributions[chunk_id][d]`. Per-offset diagnostic columns sum analogously.
7. **Restrict the final primary series to `2013-04-01` through `2022-12-31`**. Any out-of-window SQLDATE contributions from any chunk are routed to the merged `out_of_window_sqldate_diagnostic` rather than to the primary series.
8. **Sort by SQLDATE ascending** in the final `daily_count.csv`.
9. **Produce the canonical final artifacts** expected by the full-build design (per `7780a97` §15 / Decision J as amended by `c10ae74` Decision 2A):
   - `daily_count.csv` (one row per civil day in the output domain)
   - `build_metadata.json` (full provenance: chunk roll-up, per-file manifest union, SHA-256 manifest, boundary declarations, reconciliation, aggregation invariants, coverage distribution)
   - `build_summary.md`
   - Embedded or referenced per-chunk / per-file manifest
   - Embedded or referenced SHA-256 manifest
10. **Preserve deterministic output independent of chunk execution order**: a merge run in chunk_2013-first order must produce byte-identical `daily_count.csv` to a merge run in chunk_2022-first order. This is the deterministic-equivalence invariant.
11. **The final tracked execution report is a SEPARATELY AUTHORIZED post-merge step, NOT a merge-step output.** The merge step's canonical output set is items 1–10 above: derived artifacts (CSV / JSON / MD / manifests) written to an untracked timestamped output directory. The tracked execution report at `docs/lane2_gdelt1_full_daily_count_build_execution_report_v0.1.md` (mirrors `858b501` discipline; the only tracked artifact of the full build) is drafted and committed AFTER the merge step's untracked derived artifacts land, via a separately authorized post-merge reporting prompt. The merge step itself does NOT write or commit this tracked report.

### 9.2 What the merge step does NOT do

- **No GDELT contact.** The merge step is purely derived: it reads chunks' already-fetched-and-discarded provenance and aggregates.
- **No retry of any chunk.** A failed chunk requires a separately authorized memo before the merge step proceeds.
- **No payload preservation.** The merge step does not access raw payload bytes (none preserved per `7780a97` §15.11).
- **No imputation of missing chunks.** If a chunk is missing, the merge step halts with `MERGE-HALT — AWAIT ADJUDICATION`.
- **No market-data ingestion**, **no Step 2 logic**, **no signal extraction**.

## 10. Cross-chunk coverage computation

**Critical**: coverage for an output SQLDATE may depend on contributing publishing files in **neighboring chunks**. Per-chunk coverage flags computed in isolation would produce incorrect results at year boundaries.

### 10.1 Boundary example

For output `d = 2015-01-01`:

- T=0 contributor is `f_(2015-01-01)` → in `chunk_2015`.
- T−1 contributor is `f_(2015-01-02)` → in `chunk_2015`.
- T−7 contributor is `f_(2015-01-08)` → in `chunk_2015`.
- T−30 contributor is `f_(2015-01-31)` → in `chunk_2015`.
- T−365 contributor is `f_(2016-01-01)` → in **`chunk_2016`** (different chunk!).
- T+1 contributor (in pre-2015 era) is `f_(2014-12-31)` → in **`chunk_2014`** (different chunk!). The era cutoff at `2015-01-01` (per `c10ae74` Decision 1A) places this date in the pre-2015 T+1 era, so T+1 is in its expected cone.

Computing coverage for `d = 2015-01-01` using only `chunk_2015`'s available files would incorrectly mark T−365 and T+1 contributions as absent. The merge step must use the **union of all chunks' fetch sets** as `daily_set` when computing the per-civil-date coverage flag.

### 10.2 Merge-time coverage requirements

- **Per-chunk coverage flags are diagnostic only.** If emitted, they reflect the per-chunk view of the daily_set and are not authoritative.
- **Final `coverage_quality_flag` and `coverage_completeness` are computed at merge time** using the full recognized-list-derived contributing-file cone, not inferred solely from any single chunk.
- The merge step preserves the **`c10ae74` Decision 1A amendment**: the closed `coverage_quality_flag` value domain is the 7-entry set `{full, t0_absent_substrate_gap, right_truncated_2022_seal, left_truncated_2013_edge, t_plus_1_neighbor_substrate_gap, t_minus_n_neighbor_substrate_gap, multiple}`, with the era cutoff at `T_PLUS_1_ERA_CUTOFF = date(2015, 1, 1)`.
- The merge step recomputes coverage by invoking the same `coverage_for_date(d, daily_set, gaps_set)` logic as the existing runner at `bc7b66b`, with `daily_set` = the union of all chunks' fetch_set = the full recognized-list-derived in-window daily set minus substrate gaps.

### 10.3 Multi-cause flag representation (carried forward implementation reality)

The `c10ae74` adjudication memo's closed domain table lists `multiple` as the categorical name for multi-cause coverage states. The `bc7b66b` runner implements multi-cause states as `+`-joined ordered concatenations of single-cause flag names (e.g., `t0_absent_substrate_gap+t_plus_1_neighbor_substrate_gap`), with the validator `is_valid_coverage_flag` accepting either a single-flag value from the 6-entry `COVERAGE_SINGLE_FLAGS` tuple OR a `+`-joined ordered concatenation of two or more single-cause flags. This is consistent with `c10ae74` §11.3's wording but uses the concatenation form as the runtime representation.

**Decision for this memo**: carry forward this implementation reality verbatim. The merge step inherits `bc7b66b`'s `coverage_for_date` and `is_valid_coverage_flag` semantics without modification. A future clarification of `multiple`-literal-vs-`+`-joined representation, if any, is a non-blocker for chunk-design and may be addressed in a future small revision memo or in the chunk-runner-patch implementation review. No patch is authorized here.

## 11. Chunk-level halt semantics

A failed chunk is a **stop / adjudication event**, not an automatic retry trigger.

### 11.1 Halt-class behavior

When a chunk's runner encounters any hard-fail condition (any Decision I class from `7780a97` §14: HTTP non-200, redirect, connection error, timeout, unexpected offset, 2023+ SQLDATE, output allow-list violation, recognized-list mismatch, 2023+ URL construction, header anomaly):

- The chunk's runner halts.
- The chunk's `halt_diagnostic.json` is written under the chunk's output directory (allow-list gated; derived metadata only per `c10ae74` Decision 2A).
- The chunk's restore commit still proceeds (the enable→run→restore commit cycle is completed for the chunk).
- **No automatic retry.**
- **No automatic fallback to checkpoint/resume.** (Option A remains Plan-B reserve per `fbc605b` and is not activated by chunk-level halt alone.)
- **No automatic fallback to off-session execution.** (Option D remains Plan-C reserve per `fbc605b` and is not activated by chunk-level halt alone.)
- **No merge may occur** while any required chunk is failed or incomplete (per §9.1.2).
- **Re-fetching already-contacted URLs is not authorized** by this memo. A future memo deciding how to recover the failed chunk must explicitly address re-fetch / no-second-GET semantics; the default posture is "no re-fetch within the same execution-authorization scope".
- Any decision to continue after a failed chunk (re-execute the chunk in a new authorization, invoke Plan-B reserve, invoke Plan-C reserve, or abandon the build) requires a **separately authorized memo**.

### 11.2 Recovery framing (out of scope for this memo)

- If recovery from a failed mid-chunk run would require avoiding second GETs on already-fetched URLs, that belongs to a **checkpoint/resume design** (Plan-B reserve per `fbc605b`) and is **not part of this chunk-design memo**.
- If recovery requires off-session execution (e.g., to side-step session-lifetime constraints entirely), that is **Plan-C reserve** per `fbc605b` and is **not authorized here**.
- This chunk-design memo's halt semantics treat each chunk as an atomic execution unit: it either completes cleanly or halts with derived diagnostics, with no in-place mid-chunk recovery.

## 12. Duplicate-prevention and exact-once discipline

The chunked design must preserve exact-once fetch semantics at the URL level.

### 12.1 Invariants

- **No overlapping chunk manifests.** Each daily publishing-file URL appears in exactly one chunk's manifest.
- **No URL appears in more than one chunk's per-file manifest.** Any duplicate is a hard failure at merge time (`DUPLICATE-FETCH-DETECTED` halt class).
- **No chunk may be executed twice** without separate adjudication. Re-execution of an already-successful chunk requires a separately authorized memo explaining the substrate-side reason.
- **No successful chunk may be overwritten.** The chunk-runner's output directory creation uses `os.makedirs(..., exist_ok=False)` per `bc7b66b` precedent (`_fresh_output_dir`). A pre-existing output directory at the chunk's intended path is a hard failure.
- **Chunk output directories must be pre-existence guarded.** A failed chunk's partial output directory must NOT be overwritten by a subsequent re-execution authorization; the partial directory must be moved/archived (or the re-execution must use a different timestamp) per separately authorized recovery memo.
- **The merge step must check chunk-manifest union equality** against the full expected daily fetch set (3,558 URLs). Any duplicate URL across chunks is a hard failure. Any missing expected URL is a hard failure **unless** it is one of the 4 known substrate gaps already excluded by recognized-list authority.

### 12.2 Manifest digest contract

Each chunk's `chunk_manifest_digest` is computed by the chunk-runner as the SHA-256 of the sorted ASCII-encoded list of in-chunk URL strings (each terminated by `\n`). The merge step recomputes the same digest from the recognized-list capture and compares. Mismatch = hard failure (`MANIFEST-DIGEST-MISMATCH` halt class).

## 13. Future implementation requirements

The chunk-runner patch (separately authorized; **NOT** part of this memo) must implement the following.

### 13.1 Runner-patch surface

- **Deterministic chunk manifest construction** from the recognized-list capture: given a `--chunk-id <chunk_id>` (or equivalent) CLI flag, the runner derives the chunk's daily fetch URL list by filtering the recognized-list capture's daily-in-window units to the chunk's `[fetch_date_start, fetch_date_end]` interval and removing the 4 substrate gaps. The result is sorted lexicographically.
- **Chunk ID validation**: accepted values are the 10 chunk IDs from §6.2. Any other value is hard-fail.
- **Per-chunk expected count validation**: the runner verifies that the constructed chunk manifest has exactly the expected file count from §6.2 before any fetch. Mismatch = hard-fail.
- **Output pre-existence guard**: `os.makedirs(<output_dir>, exist_ok=False)` on the chunk's timestamped output directory; hard-fail on collision.
- **Redirect-disabled opener**: reuse `bc7b66b`'s `_FullBuildNoFollowRedirectHandler` pattern (or an equivalent script-local opener). No following of 3xx responses.
- **No retry**: per-URL fetch is exact-once; any failure halts.
- **Hard-fail classes inherited from full-build design**: every Decision I hard-fail class from `7780a97` §14 / `c10ae74` applies verbatim per-chunk.
- **Per-chunk derived artifacts** as defined in §8.1.
- **Merge command or separate merge script**: the chunk-runner patch may either expose a `--merge` CLI subcommand or be paired with a separate `scripts/merge_lane2_gdelt1_full_daily_count_build_chunks.py` script. Either choice must be specified in the chunk-runner-patch design memo (the patch itself, not this chunk-design memo).

### 13.2 Required paired tests (offline-only, mocked HTTP)

The chunk-runner patch must include paired tests at `tests/test_lane2_gdelt1_full_daily_count_build.py` (extending the existing file) covering at minimum:

- **Chunk manifest partitioning correctness** — verify each chunk's expected count from §6.2; verify the union of all 10 chunks' manifests equals the recognized-list-derived full fetch set.
- **Duplicate prevention** — verify no URL appears in more than one chunk's manifest.
- **Cross-chunk coverage computation** — verify the merge step's `coverage_for_date(d, union_daily_set, gaps_set)` produces identical results to a hypothetical non-chunked run over the same input.
- **Merge determinism** — verify two merge invocations over the same chunk outputs produce byte-identical final `daily_count.csv` and `build_metadata.json` (modulo timestamps).
- **Guard enforcement** — chunk-runner three-guard discipline (`FULL_BUILD_AUTHORIZED` + `--authorize-full-build-run` + `LANE2_FULL_BUILD_AUTHORIZED=1`) preserved per-chunk; chunk-runner refuses to execute on any guard absence; refusal fires before any fetch / output dir creation.
- **No-2023+ firewall** — chunk-runner refuses to construct any 2023+ URL; refuses to accept any 2023+ SQLDATE in parsed rows; refuses to accept a chunk manifest containing 2023+ dates.
- **Halt semantics** — chunk-runner halts on first Decision I condition; emits `halt_diagnostic.json`; restore commit proceeds.

## 14. Future workstream sequence

The complete future chain (each step separately authorized; no step bundled into a prior step):

1. **Commit this chunk-design memo** after review (a separately authorized commit prompt, not authorized by this memo).
2. **Separately authorize the chunk-runner patch + paired tests** prompt. The patch implements §13 requirements; tests verify §13.2 categories; runner ships inert (`FULL_BUILD_AUTHORIZED = False` preserved).
3. **Review the chunk-runner implementation** (read-only review pass mirroring the `c10ae74`-era implementation-review discipline).
4. **Separately authorize each chunk execution** — one execution-authorization prompt per chunk (10 prompts total), each prompting enable / single live run / restore / post-chunk report mirroring `3537a62 → 73a7911 → 858b501`. Each chunk's run must complete within a normal Claude Code session (per-chunk wall-clock ≈ 30 min at 5 s/URL).
5. **Write per-chunk post-run reports** at `docs/lane2_gdelt1_full_daily_count_build_chunk_<chunk_id>_execution_report_v0.1.md` (one per chunk; each tracked).
6. **Separately authorize the merge step** — one merge-authorization prompt that runs the merge command (offline, no GDELT contact) and produces the canonical derived artifacts (`daily_count.csv` + `build_metadata.json` + `build_summary.md` + embedded/referenced per-file/per-chunk manifest + SHA-256 manifest) under a fresh untracked timestamped output directory. The merge step does NOT write or commit the tracked execution report.
7. **Separately authorize the post-merge reporting step** — one report-authorization prompt that drafts the tracked execution report at `docs/lane2_gdelt1_full_daily_count_build_execution_report_v0.1.md` (mirrors `858b501` discipline; the only tracked artifact of the full build) summarizing the chunked-build outcome plus SHAs of the merge step's derived outputs, and commits it via a separate report-commit step. This is a distinct workstream from the merge step itself.
8. **Consolidated memory update** recording the full chunked-execution closure.
9. **No instrument-construction or market-data logic may begin until a separate firewall-retirement memo and a separate Step 2 authorization are produced.** The chunked full-build artifacts are substrate-side only.

This memo authorizes none of steps 1–9 except its own persistence. Each subsequent step requires its own separate user-initiated prompt.

## 15. Boundary statement

This memo authorizes **none** of the following:

- **Chunk-runner implementation.** No code edit to any file in `scripts/`, `src/`, `tests/`, or any other directory.
- **Code edits.**
- **Test edits.**
- **Configuration edits.**
- **Chunk execution.**
- **Full-build execution.**
- **Merge execution.**
- **GDELT contact** (no URL construction; no fetch; no `curl`/`wget`/browser/requests/manual).
- **Guard flips on any runner.** All five guards remain `False` on disk: `REAL_RETRIEVAL_ENABLED` (`src/lane2_gdelt1_count_feasibility.py:647`); `COUNT_FEASIBILITY_AUTHORIZED` (`scripts/run_lane2_gdelt1_count_feasibility.py:49`); `EVENT_FILE_PROBE_AUTHORIZED` (`scripts/run_lane2_gdelt1_event_file_probe.py:52`); `ROW_DATE_CHARACTERIZATION_AUTHORIZED` (`scripts/run_lane2_gdelt1_row_date_characterization.py:57`); `FULL_BUILD_AUTHORIZED` (`scripts/run_lane2_gdelt1_full_daily_count_build.py:95`). Shell envs `LANE2_*_AUTHORIZED` all `UNSET`.
- **Memory file edits.**
- **Market data of any kind.**
- **Step 2 of any kind.**
- **Spike / burst threshold tuning.**
- **Return-window logic.**
- **Asset selection.**
- **Signal extraction.**
- **2023+ access** (no-2023+ posture at `0ddbd51` / `7780a97` §11.1 remains in force).
- **Raw payload preservation.**
- **Retries.**
- **Checkpoint/resume implementation** (Plan-B reserve per `fbc605b`; not activated by this memo).
- **Off-session execution** (Plan-C reserve per `fbc605b`; not activated by this memo).
- **Output-artifact mutation** of existing dirs (`results/lane2_gdelt1_event_file_probe/20260522T221241Z/`, `results/lane2_gdelt1_row_date_characterization/20260523T033234Z/`, `results/lane2_gdelt1_count_feasibility/20260518T163302Z/` F4 baseline all byte-identical).
- **F4 modification** (baselines `41c80c0…624c39d` / `00ce9b2…f5e37552c` preserved).
- **Recognized-list capture modification** (SHA `84ea721e…fff835fc` preserved).
- **Locked-memo / locked-commit edits** to any of `9319d30` / `a8a9dd2` / `a2a8fd5` / `e9f8781` / `487dadb` / `3537a62` / `73a7911` / `858b501` / `0065d10` / `7780a97` / `bc7b66b` / `c10ae74` / `d7c8775` / `fbc605b` / `e55e09a` / `0b341b4` / `845c51c` / `e81208d` / `7c85e3f` (event-file probe enable/restore, added for inventory completeness to mirror the characterization cycle's `3537a62` / `73a7911`).
- **Staging / commit / push** of this memo or any other artifact unless separately authorized after review.

## 16. Open questions / known non-blockers

The following items are noted for completeness but do **not** block the chunk-design memo's adoption:

1. **Pre-existing untracked files are not adjudicated by this memo.** The untracked items `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`, `docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md`, `paper/main.*`, and the three pre-existing `results/` directories (`lane2_gdelt1_event_file_probe`, `lane2_gdelt1_row_date_characterization`, `lane2_gdelt1_count_feasibility`) remain in their pre-existing untracked state. This memo does not interpret, adjudicate, stage, commit, or modify them.
2. **`docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md` is not interpreted here.** Its disposition (track / commit / discard / supersede) is a separate workstream not initiated by this memo.
3. **Coverage-domain representation issue** (`multiple` literal vs `+`-joined multi-cause flags): per §10.3 above, the implementation reality from `bc7b66b` (validator accepts either a 6-entry single-flag tuple member OR a `+`-joined ordered concatenation) is **carried forward verbatim** by this memo's design. A future revision of `c10ae74` Decision 1A could clarify the categorical-name-vs-runtime-representation distinction, but this is not a chunk-design blocker. The merge step inherits `bc7b66b`'s coverage validator unchanged.
4. **Chunking solves session/runtime exposure, not the full cumulative no-retry probability problem across all 3,558 URLs.** Across the entire build, the probability of at least one chunk's run halting on a transient HTTP/network failure remains roughly the same as the un-chunked first-pass probability (P(zero failures) ≈ `0.999^3558 ≈ 2.8%`). What chunking provides is per-chunk failure-location isolation, per-chunk session-fit, and independent audit trails — not magic elimination of cumulative network risk. If chunked execution encounters a halt, recovery proceeds via separately authorized memos (Plan-B reserve = checkpoint/resume, or Plan-C reserve = off-session execution, or a different adjudication).
5. **The chunk-runner patch is a separate workstream** and must NOT be bundled into this chunk-design memo. The design memo is design-only; the patch is implementation. The two must be separately authorized prompts.

This memo's authorization scope is complete upon persistence of `docs/lane2_gdelt1_full_build_chunk_design_memo_v0.1.md`. No staging, commit, or push is authorized by this memo's content.
