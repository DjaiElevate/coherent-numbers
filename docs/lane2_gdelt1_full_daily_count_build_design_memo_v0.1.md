# Lane 2 GDELT1 full daily-count build design memo v0.1

## 1. Title and status

This memo is **memo-only**. It authorizes no new GDELT contact, no runner implementation, no full daily-count build execution, no event-file probe re-run, no row-date characterization re-run, no market data, no Step 2, no spike / burst threshold tuning, no return-window logic, no asset selection, no signal extraction, no category / theme / actor / geography / tone filtering, no claim about market predictiveness, no guard flip, no source / test / config edit, no locked-memo edit, no output-artifact mutation, and no staging / commit / push of this memo or any other artifact unless separately authorized after review.

The memo's authorization scope is the persistence of one tracked file at `docs/lane2_gdelt1_full_daily_count_build_design_memo_v0.1.md`. Its purpose is to translate the three locked decisions in the post-characterization decision memo (`0065d10`) into a complete design for the future full daily-count build — covering build inputs, output date domain, row-count semantics, SQLDATE aggregation, edge handling, retrieval policy, parser validation, output artifact schema, and future implementation / test requirements — **without implementing the runner and without executing the build**.

| Anchor | Value |
|---|---|
| Current `HEAD = origin/main` | `0065d10107848ff528db94c19e4feec5ad932d16` |
| Ahead count | `0` |
| Tracked tree status | clean |
| Post-characterization decision memo | `0065d10` |
| Characterization execution report | `858b501` |
| Characterization plan lock | `a2a8fd5` |
| Substrate-validation memo (closed by `0065d10` §5) | `a8a9dd2` |
| First-probe execution report | `9319d30` |
| No-2023+ posture (v0.3) | `0ddbd51` |
| §10 recognized-list capture SHA-256 | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` |
| F4 baselines (preserved) | `41c80c0…624c39d` / `00ce9b2…f5e37552c` |

## 2. Scope and non-scope

**In scope:**

- Decision A: build input universe.
- Decision B: output date domain.
- Decision C: row-count semantics.
- Decision D: SQLDATE aggregation rule.
- Decision E: backward edge handling (out-of-window SQLDATEs).
- Decision F: forward edge / 2022-seal coverage gaps.
- Decision G: substrate gaps and missing publishing files.
- Decision H: retrieval policy and run authorization design (design-only).
- Decision I: parser validation and stop conditions.
- Decision J: output artifact design.
- Decision K: future implementation and test requirements.
- Consequences for future build-runner implementation.
- Boundary-constraint statement for the next workstream.

**Out of scope (explicit, binding):**

- No runner implementation (a separate implementation prompt follows this one).
- No full daily-count build execution.
- No market data of any kind.
- No Step 2 of any kind.
- No spike / burst threshold tuning.
- No return-window logic.
- No asset selection.
- No signal-design choice.
- No category / theme / actor / geography / tone filtering.
- No claim about market predictiveness.
- No GDELT contact.
- No output-artifact mutation.
- No guard flip.
- No source / test / config edit other than this memo file.
- No locked-memo edit.
- No 2023+ pre-filter authorization.
- No frozen-snapshot execution.
- No `python3` canonicalization change.
- No negative-control payload allow-list change.
- No re-litigation of the three locked decisions in `0065d10` (Decisions 1B / 2A / 3A).

## 3. Source anchors

In commit-chain order:

| # | Anchor | Description |
|---|---|---|
| 1 | `9319d30` | First event-file probe execution report; empirical origin of `ROW-DATE-MISMATCH` |
| 2 | `a8a9dd2` | Substrate-validation memo; `REKEY-BY-SQLDATE-CANDIDATE` (conditional; closed by `0065d10`) |
| 3 | `a2a8fd5` | Row-date characterization plan lock |
| 4 | `e9f8781` | Row-date characterization runner implementation |
| 5 | `487dadb` | Exact-integer offset taxonomy corrective patch |
| 6 | `3537a62` | Characterization guard enable |
| 7 | `73a7911` | Characterization guard restore |
| 8 | `858b501` | Row-date characterization execution report (outcome `TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY`) |
| 9 | `0065d10` | Post-characterization decision memo (three locked decisions; this memo's primary source of truth) |

Supporting anchors: probe design note `e55e09a`; probe implementation `0b341b4`; parser coverage `845c51c`; no-2023+ posture `0ddbd51`; §10 recognized-list capture (SHA `84ea721e…fff835fc`); F4 baselines `41c80c0…624c39d` / `00ce9b2…f5e37552c`; count-feasibility precedent `60ec1521 → fe74255 → 9e329c2`; event-file probe precedent `e81208d → 7c85e3f → 9319d30`; row-date characterization precedent `3537a62 → 73a7911 → 858b501`.

This memo treats the committed decision memo at `0065d10` as the primary source of truth where memory and repo disagree; secondary source of truth is the characterization execution report at `858b501`.

## 4. Locked premises inherited from `0065d10`

The full-build design memo **inherits without re-litigation** the following items locked in `0065d10`:

### 4.1 `a8a9dd2`'s `REKEY-BY-SQLDATE-CANDIDATE` upgraded to a locked full-build premise (`0065d10` §5)

> Each event row in a GDELT 1.0 daily publishing file contributes attention to its `SQLDATE` (the actual event date), not to the file's nominal publishing-window date. The full daily-count build aggregates rows across publishing files by `SQLDATE`. The offset taxonomy of lookback buckets relative to each publishing file's nominal date is the seven-element exact-integer set `{0, −1, −7, −30, −365, −3650, +1}`, with the `+1` bucket present only in files whose nominal date is on or before `2014-12-31` (sampling-bounded).

### 4.2 Exact offset taxonomy

`{0, −1, −7, −30, −365, −3650, +1}` — exact-integer offsets only; no tolerance windows; `−3650` lands on the exact integer with no leap-year drift; GDELT's lookback offsets are constant-day-count, not calendar-date arithmetic.

### 4.3 Decision 1B — T+1 row handling

Keep T+1 rows and re-key them uniformly to `SQLDATE` like all other lookback-bucket rows. T+1 rows are **not** dropped, **not** specially corrected, **not** normalized away, and **not** used as a basis for introducing market-data / Step 2 / spike-burst threshold / any other downstream adjustment logic (`0065d10` §6.4 explicit sentence). The pre / post-2015 T+1 publishing-pipeline asymmetry is **documented as a substrate-level property** and **uncoded** in the build pipeline.

### 4.4 Decision 2A — T+1 boundary precision

No finer-grained T+1 boundary characterization is authorized at this stage. The 9-month bracket `(2014-12-31, 2015-10-02]` is accepted as sufficient for build design. Build correctness does not depend on the exact transition date under Decision 1B. Any future finer characterization is a separate explicit workstream (not authorized here).

### 4.5 Decision 3A — artifact disposition (existing dirs)

Both pre-existing output dirs — `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` and `results/lane2_gdelt1_row_date_characterization/20260523T033234Z/` — remain **untracked indefinitely** with SHA-256 references in the committed reports at `9319d30` and `858b501`. Temporary, revisitable by future explicit memo. The full-build design memo extends D3A's principle to the future build's output artifacts in §15 below.

### 4.6 No-market-data firewall

The no-market-data firewall remains in force unconditionally. This memo does not approach, touch, or relax it.

## 5. Design objective

Produce a **deterministic daily attention-count series** keyed by event-date (`SQLDATE`) over the Lane 2 daily-regime window `2013-04-01` through `2022-12-31`, by aggregating rows across publishing files in the recognized-list capture per the locked SQLDATE re-key premise (§4.1). The instrument is **substrate-side only**: counts measure GDELT-published event rows by their tagged event date, no more and no less. The instrument introduces **no market data, no Step 2, no spike thresholds, no return-window logic, no asset selection, and no market-predictiveness claim**.

The build's correctness is judged by:

1. **Determinism**: given the same recognized-list capture and the same fetched bytes, two runs produce byte-identical metadata + daily-count outputs (modulo timestamps).
2. **Substrate fidelity**: every parsed row is routed by its `SQLDATE` to the daily bucket; no row is silently dropped, normalized, or special-cased.
3. **Boundary safety**: no 2023+ contact; no market data; no Step 2; no spike threshold; no signal logic.
4. **Coverage transparency**: each output row carries diagnostics indicating which contributing files were present vs absent, so downstream systems can reason about right-truncation, left-truncation, and substrate-gap effects without inference.

## 6. Decision A — build input universe

**Decision: the future full daily-count build consumes exactly the §10 recognized-list capture at SHA `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` as its canonical input universe; no other URL is constructed; no index / listing fetch occurs during build execution.**

### Options evaluated

| Option | Verdict | Rationale |
|---|---|---|
| A. Use the §10 recognized-list capture (SHA `84ea721e…fff835fc`) as the sole input-universe authority, with deterministic preflight classification per §6.8 and no guessed files | **SELECTED** | The §10 capture is the canonical, repo-tracked, hash-verifiable artifact enumerating in-window publishing files; locked at `4015b97` under the Gate 4C / turn-b live-execution chain. Reusing it gives determinism, single-source-of-truth, and zero new GDELT contact in the build. |
| B. Re-fetch / re-list the GDELT index URLs at build execution time | Rejected (not for this design; available via future explicit re-capture authorization memo) | Duplicates work already locked in the §10 capture; introduces reproducibility risk if the GDELT index changes between capture and build; a new live listing would itself require a Gate 4C / turn-b-equivalent authorization, not approvable as a side decision of this design memo. |
| C. Infer or guess missing dates from a civil-calendar enumeration | Rejected (permanently forbidden by design) | Construction of URLs not present in the §10 capture violates the locked input-universe authority and would silently fetch non-recognized files; per §6.6 and §6.7 such construction is a hard-fail. The substrate-pinned discipline established by the Gate 4C / turn-b chain cannot be bypassed by calendar inference. |
| D. Use a manually curated date list independent of the §10 capture | Rejected (not for this design; available via future explicit revision memo if a substrate-side reason emerges) | Would introduce an unauditable curation layer divorced from the canonical capture and defeat the substrate-pinned discipline of `4015b97`. A future memo could define a curated subset for a special-purpose run with explicit authorization. |

### 6.1 Input set definition

- The tracked §10 recognized-list capture artifact (committed at `4015b97` per memory; SHA-256 `84ea721e…fff835fc`) is the **sole authority** for which GDELT 1.0 daily event files the build may fetch.
- The build reads the capture from its tracked on-repo location at parse time, asserts the SHA-256 against the locked value, and enumerates the in-window recognized units listed in the capture.
- Each enumerated unit corresponds to one daily publishing file URL of the form `http://data.gdeltproject.org/events/<YYYYMMDD>.export.CSV.zip`.
- The build attempts each enumerated URL **exactly once** per run. No retries unless separately authorized.

### 6.2 No guessed files

- The build does **not** construct URLs from a date enumeration (e.g., "every civil day in `[2013-04-01, 2022-12-31]`").
- The build does **not** construct URLs from a regex extrapolation of the recognized list.
- The build does **not** infer file existence from the existence of neighboring files.
- Any URL not listed in the recognized-list capture is treated as a hard-fail attempt and never issued.

### 6.3 No index / listing fetch during build execution

- The build does **not** issue any HTTP request to the GDELT index, listing, raw-data root, or any URL other than the enumerated daily file URLs from §6.1.
- The recognized-list capture is **the** listing-equivalent for the build; the listing operation itself is locked into the on-repo capture artifact, not re-performed during the build.
- Any future re-capture of the recognized list (e.g., to support a future 2023+ window expansion or new ingest cycle) is a **separate explicit workstream** under the same three-guard discipline that produced the existing capture (Gate 4C turn-b lineage); not authorized here.

### 6.4 Known substrate gaps

- The substrate-validation memo `a8a9dd2` §2 / §10 lists four known publishing-file gap dates: `2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`. These dates are **not in the recognized-list capture** (excluded at the capture stage).
- The build does **not** issue HTTP requests for these dates. Each is recorded in the per-file manifest as `status = expected_absent_per_recognized_list` for documentation completeness, with `http_status = none / not_requested`.
- Substrate-gap SQLDATEs can still receive contributions from other publishing files: e.g., `2014-01-23` may appear as a T−1 row in `f_(2014-01-24)`, as a T−7 row in `f_(2014-01-30)`, etc. — though for these specific dates, several neighbor files are also absent, and the resulting daily-count value for the gap date will be the sum of contributions from whichever neighbor publishing files are present. This is a substrate property to surface via coverage diagnostics, not an instrument-side correction.

### 6.5 All recognized in-window files attempted exactly once

- Every URL enumerated from the §10 recognized-list capture's in-window unit list is attempted exactly once.
- No URL is skipped, deferred, sampled, or batched.
- No URL is fetched twice (no retries).
- An unexpected absence (HTTP non-200 for a URL listed as in-window) is a hard-fail stop condition per Decision I (§14).

### 6.6 Non-recognized dates forbidden

- Any URL not enumerated by the §10 capture is forbidden from construction, fetch, allow-list, manifest, or output artifact.
- Construction of a non-recognized URL inside the build runner is a hard-fail per Decision I.

### 6.7 No 2023+ URL construction

- The no-2023+ posture at `0ddbd51` is in force.
- Even if the §10 capture were to enumerate a 2023+ unit (it does not, by construction; the capture was acquired with the no-2023+ posture), the runner enforces a redundant 2023+ refusal at URL-construction time via a precondition check (`year(date) <= 2022`).
- A 2023+ URL construction attempt by the runner is a hard-fail.

### 6.8 Build input count reconciliation (verification deferred to implementation preflight)

Three counts are involved in defining the build's input universe:

| Quantity | Documented value | Source |
|---|---|---|
| §10 recognized-list capture units | `3,647` (per `recognized_in_window_count` and `len(recognized_in_window_units)` fields in the capture artifact) | Capture artifact at SHA `84ea721e…fff835fc` |
| Civil days in output date domain | `3,562` | Computed from locked window `[2013-04-01, 2022-12-31]` inclusive (275 days in 2013 + 365 + 365 + 366 + 365 + 365 + 365 + 366 + 365 + 365 = 3,562) |
| Known publishing-file substrate gaps | `4` (`2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`) | Substrate-validation memo `a8a9dd2` §2 / §10 |

A naive expectation that the recognized-list capture would enumerate one daily-event-file URL per non-gap civil day yields `3,562 − 4 = 3,558` expected daily URLs to fetch. The capture's documented count of `3,647` is **89 units higher** than this naive expectation.

**The exact reconciliation cannot be derived from this memo without inspecting the capture's content, which requires code execution and is therefore out of scope for this memo.** Candidate explanations for the 89-unit difference include (without commitment):

- post-2022 daily-event-file entries that survived the no-2023+ filter at capture acquisition time (would need to be excluded by the runner via the precondition check at §6.7);
- non-daily aggregate identifiers (weekly, monthly, quarterly, yearly aggregates) enumerated by the capture but not consumed by a daily-count build;
- yearly or other identifier types embedded in the capture as a single row per aggregate;
- schema header rows or metadata entries enumerated alongside the unit rows;
- pre-`2013-04-01` daily-regime entries (if any) that the capture included but the locked window excludes;
- duplicate entries (unexpected; would itself be a finding).

**Required reconciliation step at implementation preflight (binding on the implementation prompt that follows this memo):** the runner's preflight must inspect the capture, classify each enumerated unit by type (daily-event-file vs other), and emit an explicit reconciliation report. The reconciliation report must show: total capture units; per-unit-type counts; subset of capture units that are daily-event-file URLs within the locked window `[2013-04-01, 2022-12-31]`; and the expected fetch count. If the daily-event-file in-window count differs from `civil_days_in_window − known_substrate_gaps = 3,558`, the discrepancy must be enumerated date-by-date and surfaced as a build-design finding (potentially blocking execution authorization until adjudicated by a separate revision memo).

This memo does **not** invent a specific URL count. The runner must compute the fetch set deterministically from the capture per Decision A; the count is whatever the capture's daily-event-file unit subset enumerates, **not** a fixed number assumed here. The numbers `3,647`, `3,562`, `4`, and `3,558` above are documented values and naive-expectation arithmetic, not asserted equalities.

### 6.9 What Decision A does NOT authorize

- No new recognized-list capture run.
- No GDELT contact for any URL not in the §10 capture.
- No index / listing / search / browse query against GDELT.
- No frozen-snapshot retrieval.
- No archive re-fetch of any previously-fetched file in the probe or characterization output dirs.

## 7. Decision B — output date domain

**Decision: the canonical output date domain is the full civil calendar from `2013-04-01` through `2022-12-31` inclusive (every civil day in the locked Lane 2 daily-regime window), with one daily-count row per civil day. Zero-row days are represented as `total_row_count = 0` with explicit coverage diagnostics; the absence or presence of a publishing file at a civil day does not change the domain's shape.**

### 7.1 Options evaluated

| # | Option | Verdict |
|---|---|---|
| 1 | Full civil calendar over the daily-regime window | **SELECTED** |
| 2 | Only recognized publishing-file dates | Reject |
| 3 | Only SQLDATEs observed in parsed rows | Reject |
| 4 | Extended SQLDATE range including out-of-window lookback dates | Reject |

**Option 1 — Full civil calendar `2013-04-01` to `2022-12-31` (SELECTED).**

- Pro: the output domain is stable, deterministic, and downstream-friendly; every civil day in the locked window has exactly one row; the domain shape is independent of which publishing files are present or absent; substrate gaps (e.g., `2014-01-23`) still appear as civil days with `total_row_count` reflecting whatever contributions are aggregated from non-gap neighbor publishing files; the domain matches the SQLDATE re-keying premise (which assigns rows to event-dates, not to publishing-file-dates).
- Con: zero-row days exist in the output and must be distinguished from missing-observation days via coverage diagnostics.
- **Select.**

**Option 2 — Only recognized publishing-file dates.**

- Con: conflates input universe (which publishing files exist) with output universe (which SQLDATEs are valid). Under SQLDATE re-keying, the output domain is the SQLDATE domain, not the publishing-file-date domain. Selecting Option 2 would silently exclude substrate-gap civil days from the output even though those days legitimately have SQLDATE contributions from neighbor publishing files. Reject as incoherent with the locked premise.

**Option 3 — Only SQLDATEs observed in parsed rows.**

- Con: makes the output domain data-dependent. Two runs over the same input could produce different domains if even one row's SQLDATE differs (e.g., a malformed-short row at a unique date that would otherwise have zero rows would change the domain). Disables stable downstream comparison across runs. Reject as non-deterministic at the domain level.

**Option 4 — Extended SQLDATE range including out-of-window lookback dates.**

- Con: extends the instrument's domain into territory outside the locked Lane 2 daily-regime window. For example, T−3650 rows in the `2013-04-01` file have SQLDATEs around `2003-04-04`, which is outside the locked window. Including these would create asymmetric coverage (only T−3650 contributions on pre-2013 dates; no T=0, T−1, T−7, T−30, T−365 contributions because those require pre-2013 publishing files that are not in the universe), produce a meaningless tail of the series, and violate the locked daily-regime window. Reject as out-of-window scope creep.

### 7.2 Why the chosen date domain fits SQLDATE re-keying

Under Decision 1B (`0065d10` §6), every row's contribution flows to its `SQLDATE`. The natural output keying is therefore by civil date — specifically, by the civil date space that the build is **scoped to measure**. The locked daily-regime window `2013-04-01` to `2022-12-31` (substrate-validation memo `a8a9dd2` §1; no-2023+ posture `0ddbd51`) defines that scope. The full civil calendar across the scope produces one row per civil day; the instrument's coverage and contribution structure for each day is then surfaced via diagnostics.

### 7.3 How publishing-file gaps are represented

- A civil day `d` whose publishing file `f_d` is in the substrate-gap list (e.g., `2014-01-23`) appears as a row in the output domain with `t0_file_status = expected_absent_per_recognized_list`, `t0_rows = 0` (no T=0 contribution), and possibly non-zero contributions from `f_(d+1)`'s T−1 bucket, `f_(d+7)`'s T−7 bucket, etc., wherever those neighbor files are present in the recognized list.
- A civil day `d` whose publishing file is in the recognized list but fails retrieval at run time triggers a hard-fail per Decision I (the build does not silently skip and produce a partial daily-count row).
- A civil day's `coverage_quality_flag` summarizes which of the seven expected contributing files (per §10 below) were present, absent-by-design, or unavailable.

### 7.4 Why this does not use market calendars or trading days

- The instrument is a substrate-side row-count over GDELT event-dates. Event-date occurrence is not constrained to trading days, business days, or any market-calendar concept.
- Using a market calendar would (a) impose a downstream-system semantic onto a substrate-side instrument, (b) require integration with a market data source (forbidden by the no-market-data firewall), and (c) silently align the daily-count series with a specific asset's trading day, which would prematurely commit the instrument to one downstream application.
- Per `0065d10` §11 boundaries, **no market data**. Selecting any market-calendar variant of Option 1 would violate the no-market-data firewall.

### 7.5 Zero-row vs missing-observation days

- **Zero-row day**: every contributing publishing file in the seven-offset cone is either present-and-fetched-with-zero-SQLDATE-=-d rows, or absent-by-design (substrate gap), or absent-by-policy (no-2023+ at the right edge), or absent-by-window-boundary (at the left edge). The `total_row_count` is `0`. The `coverage_quality_flag` documents which contributions are absent.
- **Missing observation**: there are no missing observations in the output domain by construction — every civil day in `[2013-04-01, 2022-12-31]` gets a row. The runner halts (Decision I) before producing a partial output if any in-universe publishing file fails to retrieve.

### 7.6 What future downstream systems may and may not infer

- **May infer**: per-day counts, per-day per-offset counts, per-day coverage quality, the position of substrate gaps in the output series, the right-truncation effects at the 2022 seal.
- **May not infer**: anything about market activity, trading-day alignment, asset-specific behavior, predictive value, spike timing relative to market events, or any other downstream-specific interpretation. The instrument is a substrate measurement, not a signal.
- **Must not silently impute**: downstream systems that filter zero-row days should do so explicitly via the `coverage_quality_flag`, not by removing rows from the domain.

## 8. Decision C — row-count semantics

**Decision: count raw event rows. Each parsed row contributes exactly one unit to the total count of its `SQLDATE` bucket and exactly one unit to the per-offset count of its `(SQLDATE, offset_from_publishing_file_nominal_date)` cell. No deduplication. No filtering. Malformed-short and unparseable-SQLDATE rows are excluded from counts but surfaced in diagnostics.**

### Options evaluated

| Option | Verdict | Rationale |
|---|---|---|
| A. Raw event rows, counted once per parsed occurrence; no deduplication, no filters, no weights | **SELECTED** | Substrate-fidelity — each row that GDELT publishes contributes one unit to its `SQLDATE` bucket exactly, per the locked premise (`0065d10` §5). Avoids prematurely committing this instrument to any downstream signal-design choice; mirrors the row-count framing of the characterization at `858b501`. |
| B. Deduplicated event rows (by `GLOBALEVENTID` or row-hash) | Rejected (not for this design; available via future explicit revision memo) | A deduplicated event-count instrument is a different downstream construct that can be derived from this build's per-row data by a downstream tool. Forbidding dedup here preserves the substrate's publishing-window emission structure exactly. |
| C. Filtered subset by category / theme / actor / geography / tone | Rejected (not for this design; available only through a future explicit revision memo that retires the no-market-data firewall and explicitly authorizes Step 2 / instrument-construction logic) | Filtering by category / theme / actor / geography / tone is **not merely** a generic future revision; it is **Step 2 / instrument-construction territory**. Selecting a category, theme, actor, geography, or tone filter is a signal-design choice that converts this substrate-side row-count instrument into a downstream feature-construction step. Such a conversion requires both (a) retirement of the no-market-data firewall (currently locked unconditionally by `0065d10` §11 boundaries and §11.1 of this memo) by a separately authorized memo, and (b) explicit authorization of Step 2-style instrument-construction logic. Neither is provided by this design memo, and neither may be inferred from any decision herein. |
| D. Weighted rows (per-row weights driven by source, tone, mentions, etc.) | Rejected (not for this design; available via future explicit revision memo) | Weighting requires a downstream rationale this memo does not provide and would tie the build to a specific analytical use. Substrate-side counts remain unweighted; downstream tools may weight as needed. |

### 8.1 Raw event rows, not unique event IDs

- The instrument is a **row-count instrument**, consistent with `0065d10` §5's locked premise ("contributes attention to its `SQLDATE`").
- No de-duplication by `GLOBALEVENTID` (the GDELT 1.0 event ID column) or any other column. A row that appears in two publishing files (e.g., once at T=0 in `f_d` and again at T−1 in `f_(d+1)` with the same `GLOBALEVENTID`) contributes **twice** to the count for SQLDATE = d — once per publishing-file occurrence. The substrate's publishing-window snapshot mechanism is the reason these rows exist in multiple files, and treating each occurrence as a separate count unit preserves the substrate's emission structure exactly.
- This is consistent with the row-count framing in the characterization plan `a2a8fd5` and the characterization report `858b501` (which counts rows, not unique event IDs).

### 8.2 Deduplication forbidden

- The build does **not** deduplicate rows by `GLOBALEVENTID`, by any column combination, by row hash, or by any other key.
- A future analysis that wants a deduplicated event series can derive it as a downstream operation; the build instrument exposes the underlying row-count data.
- Forbidding dedup at the build stage preserves substrate fidelity and avoids prematurely committing the instrument to a downstream-specific semantic.

### 8.3 Once per parsed occurrence

- Each row that parses successfully contributes exactly one count to its `(SQLDATE, offset)` cell.
- If the same row text appeared twice in a single file (which is not expected per the substrate characterization, but is documented here for completeness), both occurrences would count.
- Rows in different files with the same `GLOBALEVENTID` count separately (see §8.1).

### 8.4 Category / theme / actor / geography / tone filters forbidden

- The build does **not** apply any filter on `Actor1Type1Code`, `Actor2Type1Code`, `EventCode`, `EventBaseCode`, `EventRootCode`, `GoldsteinScale`, `NumMentions`, `NumSources`, `NumArticles`, `AvgTone`, country codes, geography fields, theme tags, or any other GDELT 1.0 column.
- The build does **not** apply any filter on URLs, sources, languages, or any other contextual metadata.
- The instrument is a pure substrate-side row count; downstream filtering is a downstream concern.
- Forbidding filtering at the build stage is consistent with the no-market-data firewall (any filter would prematurely couple the instrument to a downstream signal-design choice).

### 8.5 Per-offset diagnostic counts retained alongside total count

For each civil date `d` in the output domain:

- `total_row_count[d]`: sum of all contributing rows with SQLDATE = d.
- `rows_from_offset[d][0]`: T=0 contribution (from `f_d`, if present).
- `rows_from_offset[d][-1]`: T−1 contribution (from `f_(d+1)`, if present).
- `rows_from_offset[d][-7]`: T−7 contribution (from `f_(d+7)`, if present).
- `rows_from_offset[d][-30]`: T−30 contribution (from `f_(d+30)`, if present).
- `rows_from_offset[d][-365]`: T−365 contribution (from `f_(d+365)`, if present).
- `rows_from_offset[d][-3650]`: T−3650 contribution (from `f_(d+3650)`, if present; see §10 for the structural observation that this is always 0 within the locked window).
- `rows_from_offset[d][+1]`: T+1 contribution (from `f_(d-1)`, if present and in the pre-2015 T+1 era).

Total: 1 row in the primary daily-count output + 7 per-offset diagnostic columns + coverage diagnostics (per §15).

### 8.6 Malformed-short and unparseable-SQLDATE rows

- A **malformed-short row** is a CSV row whose comma-separated field count is less than the minimum expected by the GDELT 1.0 schema (i.e., the row does not contain a parseable `SQLDATE` column at index 1).
- An **unparseable-SQLDATE row** is a row that has a value at column index 1 but that value cannot be parsed as a `YYYYMMDD` integer (e.g., empty string, non-numeric characters).
- Both classes are **excluded from total counts and per-offset counts**.
- Both classes are **surfaced in diagnostics**: per-file counts (`malformed_short_rows`, `unparseable_sqldate_rows`) recorded in the metadata JSON; the characterization (§10 of `858b501`) observed zero such rows across all 16 files, so any nonzero observation in the full build is a substrate anomaly worth surfacing.
- Note: these counts are **diagnostic, not hard-fail**. The runner records them, prints them in the summary, but does not halt. Hard-fail conditions are in Decision I.

### 8.7 What this is and what this is not

- **This is**: a substrate-side row-count instrument over GDELT 1.0 daily event files, keyed by event date (`SQLDATE`).
- **This is not**: a unique-event instrument; a category-filtered instrument; a theme-filtered instrument; an actor-filtered instrument; a sentiment instrument; a market-aligned instrument; a deduplicated-event instrument; a Step-2 signal.

## 9. Decision D — SQLDATE aggregation rule

**Decision: for each parsed row R from each allowed publishing file f, parse `R.SQLDATE` (column index 1), compute `offset = sqldate_as_date(R.SQLDATE) − f.nominal_date`, and route R to the daily-count bucket for `R.SQLDATE` if `offset ∈ {0, −1, −7, −30, −365, −3650, +1}` and `R.SQLDATE ∈ [2013-04-01, 2022-12-31]`. Aggregate counts across all allowed publishing files uniformly. Retain `f.nominal_date` and `offset` as per-row diagnostic columns within the aggregation pipeline. Do not aggregate by `f.nominal_date`. Do not normalize T+1 contributions. Do not special-case T+1 in any way.**

### Options evaluated

| Option | Verdict | Rationale |
|---|---|---|
| A. Aggregate by `SQLDATE` only (each row routed by its event date across all in-universe publishing files; per-file and per-offset diagnostics retained separately) | **SELECTED** | Operationalizes the locked SQLDATE re-key premise from `0065d10` §5; closes Decision 1B uniformly across all seven offset buckets (including T+1); matches the substrate's actual event-date semantics. Diagnostics preserve the publishing-file and offset information for audit without making them the primary key. |
| B. Aggregate by nominal publishing-file date (each file's row total → that file's nominal date) | Rejected (permanently forbidden by the `a8a9dd2` → `0065d10` §5 locked premise) | Would re-open the substrate-validation conclusion. Per `0065d10`, the strict §6 nominal-date contract from `e55e09a` is **replaced** by SQLDATE re-keying; reverting is out of scope. |
| C. Dual-publish a nominal-date series alongside the SQLDATE primary | Rejected (not for this design; available via future explicit revision memo) | Per-file row totals are already in the per-file manifest (§15.2 / §15.4); a second tracked primary artifact is redundant and dilutes the locked single-instrument design. A future memo could authorize a separate diagnostic-only nominal-date table if a use case emerges. |
| D. Normalize / rebalance by offset bucket (e.g., scale to manufacture pre/post-2015 symmetry) | Rejected (permanently forbidden by Decision 1B's no-normalization clause in `0065d10` §6.4) | Would inject a downstream-adjustment layer in violation of the locked Decision 1B sentence explicitly prohibiting use of the pre/post-2015 asymmetry as a basis for any adjustment. |

### 9.1 Per-row aggregation procedure

```
for each f in enumerated_in_window_publishing_files_from_§10_capture:
    response = http_get(f.url, redirect_disabled, timeout)
    if response.status != 200:
        halt_with_diagnostic(file_retrieval_failure, f.url, response.status)
    payload = response.bytes
    record_per_file_sha256(payload)
    csv_text = decompress_zip_to_csv_in_memory(payload)
    for each row R in csv_text.split_lines():
        if not has_sqldate_column(R):
            increment_diagnostic(f.malformed_short_rows)
            continue
        sqldate_str = R.column_at_index_1
        try:
            sqldate = parse_yyyymmdd(sqldate_str)
        except ValueError:
            increment_diagnostic(f.unparseable_sqldate_rows)
            continue
        offset = (sqldate - f.nominal_date).days
        if offset not in {0, -1, -7, -30, -365, -3650, +1}:
            halt_with_diagnostic(unexpected_offset, f.url, sqldate, offset)
        if sqldate >= 2023-01-01:
            halt_with_diagnostic(post_2022_sqldate, f.url, sqldate)
        if sqldate not in [2013-04-01, 2022-12-31]:
            increment_diagnostic(out_of_window_sqldate, sqldate, offset)
            continue        # excluded from primary series per Decision E
        increment(total_row_count[sqldate])
        increment(rows_from_offset[sqldate][offset])
```

The above is a **design-level pseudocode sketch**, not a runner implementation. The implementation prompt that follows this memo will produce a real runner with the above semantics.

### 9.2 Aggregation is across publishing files, not within

- Every parsed row from every in-universe publishing file contributes to the `SQLDATE` daily-count bucket corresponding to its event date.
- The build does **not** produce a per-publishing-file daily-count; it produces a per-event-date (per-SQLDATE) daily-count.
- The aggregation iterates over all publishing files in the capture (Decision A), inverting the per-file SQLDATE distribution into a per-SQLDATE file-and-offset distribution.

### 9.3 Per-file diagnostics retained alongside aggregation

- For each publishing file `f`, the per-file manifest records: HTTP status; bytes; row count; per-offset row count (mirroring `858b501` §10's per-file table); malformed-short count; unparseable-SQLDATE count; header anomaly flag; 2023+ SQLDATE row count (must be 0 by construction; nonzero is hard-fail).
- The aggregation pipeline keeps an in-memory per-file row tracker so the per-file metrics are emitted to the metadata JSON without re-reading the file.

### 9.4 Do not aggregate by nominal file date

- The publishing-file-date aggregation (i.e., `count[f.nominal_date] = sum_of_all_rows_in_f`) is the **wrong** instrument under the locked SQLDATE re-keying premise. It over-attributes to publishing-window dates and under-attributes to actual event dates.
- The build does **not** emit a per-publishing-file-date count column as a primary metric. Per-file row totals are diagnostic (recorded in the metadata JSON) but **not** part of the daily-count series schema.

### 9.5 Do not normalize counts to manufacture publishing-pipeline symmetry

- The pre / post-2015 T+1 publishing-pipeline asymmetry (Decision 1B; `0065d10` §6.4) is a substrate-level property.
- The build does **not** apply any normalization factor to balance T+1 contributions across the boundary.
- The build does **not** apply any per-era scaling, weighting, or correction to compensate for the differing number of contributing files between pre-2015 and post-2015 dates.
- All seven offset buckets are summed identically; the per-offset diagnostic columns document any asymmetry; downstream analysis can apply its own treatment if it chooses (but the build does not).

### 9.6 Do not use T+1 as a special-case adjustment

- The T+1 bucket is treated exactly like the other six offset buckets: rows in this bucket from `f_(d-1)` (for d in the pre-2015 era) increment `total_row_count[d]` and `rows_from_offset[d][+1]`.
- No T+1 flag column on per-row output.
- No T+1-aware filter at any aggregation step.
- No T+1-aware threshold in the primary series.

## 10. Decision E — backward edge handling

**Decision: rows whose `SQLDATE` falls before the canonical left edge (`< 2013-04-01`) are excluded from the primary daily-count output and reported in a structured `out_of_window_sqldate_diagnostic` table in the metadata JSON. The primary daily-count series remains scoped to `[2013-04-01, 2022-12-31]`. The runner emits explicit counts of excluded rows per source publishing file, never silently dropping.**

### 10.1 Options evaluated

| # | Option | Verdict |
|---|---|---|
| 1 | Exclude out-of-window SQLDATEs from primary daily-count; report in diagnostics | **SELECTED** |
| 2 | Extend output domain backward to include all observed SQLDATEs | Reject |
| 3 | Treat out-of-window SQLDATEs as hard failure | Reject |
| 4 | Keep them in a separate auxiliary table only | Reject |

**Option 1 (SELECTED).** Out-of-window rows are excluded from the primary series, but **the runner emits a structured diagnostic** showing: total out-of-window row count; per-source-file out-of-window row count; per-out-of-window-SQLDATE row count (so that the `2003-04-04` SQLDATE from the `2013-04-01` file's T−3650 bucket appears explicitly in the diagnostic). This preserves substrate fidelity (no rows lost from the audit record), preserves locked-window scope (no domain extension), and prevents silent dropping (every excluded row is enumerated).

**Option 2.** Would extend the output series backward to include SQLDATEs like `2003-04-04`. Rejected because (a) the resulting domain would be asymmetric — only T−3650 contributions reach pre-2013 dates, no T=0, T−1, T−7, T−30, T−365 — producing a non-comparable tail; (b) extends instrument scope beyond the locked daily-regime window without authorization; (c) the count values for pre-2013 dates would be tiny single-digit numbers from one offset bucket, providing no analytical value relative to the window-scope cost.

**Option 3.** Would hard-fail on encountering any out-of-window SQLDATE. Rejected because out-of-window SQLDATEs are an **expected substrate property** (validated by the characterization at `858b501` §10–§11: all 16 sampled files contain T−3650 rows, all of which fall in 2003–2012, outside the locked window). Hard-failing would prevent the build from ever completing.

**Option 4.** Auxiliary table. Functionally equivalent to Option 1 but more elaborate (requires a separate output artifact, separate schema, separate disposition decision). Rejected in favor of Option 1's diagnostic-section approach, which keeps the schema simpler.

### 10.2 Structural consequence — T−3650 within the locked window (explicit design acceptance)

A consequence of Decision 1B (uniform SQLDATE re-keying; `0065d10` §6 / §4.3 above), Decision 2A (no successor T+1 characterization; `0065d10` §7 / §4.4 above), Decision A (recognized-list capture as universe; §6 above), the no-2023+ posture (controlling authority at `0ddbd51`; see §11.1 for the explicit keep/lock decision), and the locked daily-regime window:

> For every target SQLDATE `d` in `[2013-04-01, 2022-12-31]`, the T−3650 contribution would have to come from a publishing file at nominal date `d + 3650 ∈ [2023-04-01, 2032-12-31]`. All such files are 2023+, all excluded by the no-2023+ posture. **Therefore the T−3650 contribution is structurally zero for every in-window date.**

Equivalently, every T−3650 row observed in every in-universe publishing file has SQLDATE outside the locked window (by construction), and is therefore routed to the `out_of_window_sqldate_diagnostic` table by Decision E.

**Explicit accepted design consequence (this is an adjudicated design choice, not merely a derived observation):**

> **Structural T−3650 zero is accepted under the current locked premises.** The design does **not** lift the no-2023+ posture, does **not** shift the output window earlier, and does **not** fetch post-2022 files to recover the 10-year lookback bucket. Future Step 2 logic may **not** treat T−3650 as an available in-window signal feature unless a later explicit revision memo changes the no-2023+ posture or the output window.

**Alternatives considered and rejected (each remains a non-authorized path; this memo does NOT turn either into an authorized workstream):**

- **Alt-1: lift the no-2023+ posture for backward fetches only** — i.e., authorize fetching a subset of 2023-era publishing files (e.g., a slice of `[2023-04-01, 2032-12-31]`) solely for the purpose of populating the T−3650 bucket on in-window dates. **Rejected** because (a) it would require retiring or selectively weakening the no-2023+ seal, which `0ddbd51` locks unconditionally and §11.1 reaffirms as immovable in this memo; (b) "backward fetches only" is not a substrate-side distinction — once any 2023+ file is fetched, all of its offset buckets (T=0, T−1, T−7, T−30, T−365, T−3650, and where applicable T+1) become available, expanding the build's domain and surface area; (c) a partial selective fetch would create an asymmetric instrument that is harder to audit than the current symmetric right-truncation.
- **Alt-2: shift the output window earlier so all in-window dates have `f_(d+3650) ≤ 2022-12-31`.** This would require `d_max ≤ 2022-12-31 − 3650 days = 2012-12-31`. Since the window's locked left edge is `2013-04-01` (first daily-regime date per `a8a9dd2`; substrate-side locked by GDELT 1.0's publishing history), `d_max ≤ 2012-12-31 < d_min = 2013-04-01` is incompatible — the resulting window would be empty. **Rejected as structurally infeasible** without lifting the locked left edge, which would require a separate substrate-side authorization that this memo does not provide.

Future implementation tests must assert `rows_from_offset[d][-3650] = 0` for every `d` in the output domain (this is a positive testable consequence of the accepted design choice; see §16 Decision K test category 10).

### 10.3 Diagnostics required

The metadata JSON must include an `out_of_window_sqldate_diagnostic` section structured as:

```
{
  "total_out_of_window_rows": <int>,
  "per_source_file_out_of_window_counts": [
    {"publishing_file_nominal_date": "YYYY-MM-DD", "out_of_window_row_count": <int>}
  ],
  "per_sqldate_out_of_window_counts": [
    {"sqldate": "YYYY-MM-DD", "row_count": <int>, "offset_breakdown": {"-3650": <int>, "-365": <int>, ...}}
  ],
  "out_of_window_rows_excluded_from_primary_series": true
}
```

### 10.4 Prevent silent dropping

- The runner increments `out_of_window_diagnostic[sqldate][offset]` for every row routed out of window.
- The metadata JSON's `out_of_window_sqldate_diagnostic` total must equal the sum of per-source-file counts AND the sum of per-SQLDATE counts (consistency invariant).
- The build's post-hoc tripwire asserts that the sum of `total_row_count[d]` for d in [2013-04-01, 2022-12-31] plus `total_out_of_window_rows` plus `total_malformed_short_rows` plus `total_unparseable_sqldate_rows` equals the sum of `parsed_row_count[f]` across all f in the capture (counting invariant).

### 10.5 What Decision E does NOT do

- Does not extend the instrument's domain beyond `[2013-04-01, 2022-12-31]`.
- Does not silently drop rows.
- Does not normalize for the structural T−3650 absence in the primary series.
- Does not introduce market data or any downstream-specific column.

## 11. Decision F — forward edge / 2022-seal coverage gaps

**Decision: at the 2022 right edge, rows for late-window SQLDATEs that would require contributions from 2023+ publishing files are simply absent — no imputation, no normalization, no extrapolation. Each daily-count row carries a `coverage_quality_flag` that records which expected contributing files were in-universe vs absent-by-no-2023+ posture. The 2023+ files are never fetched, never constructed, never represented.**

### Options evaluated

| Option | Verdict | Rationale |
|---|---|---|
| A. Observed-only right-truncated counts with explicit `coverage_quality_flag` and `coverage_completeness` per §11.3; no post-2022 fetches; no imputation; no normalization | **SELECTED** | Preserves substrate fidelity at the 2022 seal: every absence is documented per §11.3's closed-domain flag, downstream systems can reason about right-truncation explicitly, and the no-2023+ lock (§11.1) is respected. |
| B. Post-2022 fetches to complete future contributing files (T−1 / T−7 / T−30 / T−365 / T−3650 sources beyond `2022-12-31`) | Rejected (forbidden under current authorization; revisitable only via a separate explicit memo retiring the no-2023+ posture per §11.1) | Violates the explicit keep/lock decision in §11.1. Any retirement of the no-2023+ seal requires a separately authorized memo, not a side decision here. |
| C. Imputation / normalization for missing future contributions (model-fill, historical-rate extrapolation, neighbor-substitution) | Rejected (permanently forbidden by substrate-fidelity discipline and §11.4 / §11.5) | Would inject extrapolated or model-based data into a substrate-side instrument and risks a market-data leak if any imputation references market measures. §11.4 already prohibits imputation; §11.5 already prohibits market-data normalization. |
| D. Shorten the output window to dates with fuller offset coverage (e.g., compress the right edge to `2021-12-31` or earlier so all in-window dates have a complete T−365 cone) | Rejected (not for this design; available only through a future explicit revision memo that re-locks the output window) | Would change the locked output domain (Decision B Option 1) and the locked daily-regime window (`a8a9dd2` / `0ddbd51`). A window-shortening proposal must come as a separate explicit memo with its own substrate-side justification; this design memo does not adjudicate window changes. |

### 11.1 No-2023+ posture — explicit keep/lock decision

**Decision: the no-2023+ posture at `0ddbd51` remains LOCKED for the full daily-count build design. No part of this memo lifts, weakens, partial-relaxes, or conditions away the seal.**

Specifically, the build runner and the surrounding design:

- Issue **no 2023+ URL construction** (URL precondition refuses `year(date) ≥ 2023`; the §10 recognized-list capture also excludes 2023+ units by construction).
- Fetch **no post-2022 publishing files** (the recognized-list universe is in-window; no overflow URL is constructed; no neighbor or sibling 2023+ URL is constructed for any reason).
- Accept **no 2023+ SQLDATE in primary build logic** (any 2023+ SQLDATE observed in parsed rows is a hard-fail per Decision I; never routed to the primary daily-count series; never accepted in any metadata field or diagnostic).
- Permit **no lifting of the seal to fill coverage gaps** at the 2022 right edge (the structural absences enumerated in §11.2 are accepted as right-truncation with `coverage_quality_flag` per §11.3; no exception is carved for "just enough" 2023+ fetches to populate T−1 / T−7 / T−30 / T−365 / T−3650 buckets at late-2022 target dates).
- Permit **no post-2022 leakage** (no 2023+ date appears in the output domain, in any metadata field, in any per-file manifest, in any diagnostic, in any tracked or untracked artifact).
- Reject **any market-data, Step 2, signal-quality, or downstream-utility rationale** as a basis for weakening the seal — the no-2023+ posture is a substrate-side and authorization-side lock, and downstream-utility appeals do not constitute substrate-side or authorization-side grounds for retirement.

**Alternatives considered and rejected (each remains a non-authorized path; this memo does NOT turn any into an authorized workstream):**

- **Alt-a: lift the seal for the entire 2023+ horizon.** Rejected — `0ddbd51` is the controlling authority and locks the seal unconditionally; lifting requires a separately authorized memo, not a side decision in this design memo.
- **Alt-b: lift the seal partially for backward-fetch purposes only** (e.g., to populate the T−3650 bucket; see §10.2 Alt-1). Rejected — same rationale as §10.2 Alt-1 (no "backward-only" substrate-side distinction exists at the fetch layer).
- **Alt-c: lift the seal partially for forward-coverage purposes only** (e.g., to fetch `2023-01-01` so that `d = 2022-12-31` receives its T−1 contribution). Rejected — once any 2023+ URL is fetched, the seal is no longer intact; a "partial" framing is illusory at the substrate-fetch level.
- **Alt-d: keep the seal but allow 2023+ SQLDATE rows that arrive incidentally in 2022 publishing files** (i.e., accept post-2022 SQLDATEs as part of the substrate when they appear in pre-2023 files). Rejected — the characterization at `858b501` observed zero such rows across 16 files; if any are observed in the full build they represent a substrate property the locked premises do not anticipate, and treating them as acceptable would silently widen the instrument's domain beyond `[2013-04-01, 2022-12-31]`. Hard-fail per Decision I is the chosen treatment.

A future retirement of the no-2023+ posture (e.g., to extend the daily-regime window to a later seal date) requires a **separate explicit memo** that explicitly retires `0ddbd51`'s posture and re-locks a new seal; until such a memo lands, this design treats the seal as immovable.

Enforcement summary: the build runner refuses to construct 2023+ URLs at URL-construction time (precondition check); refuses to fetch 2023+ URLs (would not reach this layer because §10 capture excludes them); halts on any 2023+ SQLDATE observed in parsed rows (per Decision I).

### 11.2 Late-window SQLDATEs may lack future publishing-file contributions

For a target SQLDATE `d` in the late window, the contributing files are (per Decision D):

| Offset | Contributing file's nominal date |
|---|---|
| 0 | d (publishing-file at d itself) |
| −1 | d + 1 |
| −7 | d + 7 |
| −30 | d + 30 |
| −365 | d + 365 |
| −3650 | d + 3650 (always 2023+ for in-window d; absent by Decision F) |
| +1 (pre-2015 era only) | d − 1 |

For `d = 2022-12-31`, the contributing files would be at `{2022-12-31, 2023-01-01, 2023-01-07, 2023-01-30, 2023-12-31, 2032-12-31, 2022-12-30}`. Of these, only `{2022-12-31, 2022-12-30}` are in the recognized-list universe; the rest are 2023+ and excluded. The T+1 source `2022-12-30` is in-universe but is **post-2015 era**, so it contains no T+1 rows. **Net result: `d = 2022-12-31` receives contributions only from `f_(2022-12-31)`'s T=0 bucket.**

Right-edge coverage degrades by offset bucket:

| d range (late window) | T=0 | T−1 | T−7 | T−30 | T−365 | T−3650 | T+1 (era-dependent) |
|---|---|---|---|---|---|---|---|
| `[2022-01-01, 2022-11-30]` | ✓ | ✓ | ✓ | ✓ | ✗ (d+365 in 2023+) | ✗ | ✗ |
| `[2022-12-01, 2022-12-24]` | ✓ | ✓ | ✓ | ✗ (d+30 in 2023+) | ✗ | ✗ | ✗ |
| `[2022-12-25, 2022-12-30]` | ✓ | ✓ | ✗ (d+7 in 2023+) | ✗ | ✗ | ✗ | ✗ |
| `[2022-12-31, 2022-12-31]` | ✓ | ✗ (d+1 in 2023+) | ✗ | ✗ | ✗ | ✗ | ✗ |

(Symmetric left-edge degradation is documented in §10 for the backward case; see also §12 for substrate-gap-specific cases.)

### 11.3 Handling: observed-only counts with explicit right-truncation coverage flags

The build:

1. Computes `total_row_count[d]` as the sum of all available in-universe contributions (Decision D).
2. Records, for each civil date `d`, an `expected_contributing_files` list (per the **era-conditioned cone** defined below) and an `available_contributing_files` list (subset that are in-universe in the §10 recognized-list capture).
3. Computes a `coverage_quality_flag` per `d` from the **closed value domain** below.
4. Computes a `coverage_completeness` numeric score per the **exact formula** below.

**Era-conditioned expected cone (T−3650 excluded a priori per §10.2):**

| Era | Civil-date range | Expected offset buckets in the cone | Cone size |
|---|---|---|---|
| Pre-2015 T+1 era | `d ≤ 2015-01-01` | `{0, −1, −7, −30, −365, +1}` | 6 |
| Post-2015 era | `d ≥ 2015-01-02` | `{0, −1, −7, −30, −365}` | 5 |

The era cutoff at `2015-01-01` is a counter-design choice grounded in characterization evidence: the latest sampled publishing file confirmed to emit T+1 rows is `f_(2014-12-31)` (per `858b501`), whose T+1 rows have `SQLDATE = 2015-01-01`. Therefore `d = 2015-01-01` is the latest in-window date confirmed to receive a T+1 contribution; civil dates from `d = 2015-01-02` onward fall into the sampling-bounded uncertainty interval `(2014-12-31, 2015-10-02]` (Decision 2A) and are conservatively classified as post-2015 era for counter purposes. This is a counter-design choice only; it does not assert that no T+1 rows arrive for `d ∈ [2015-01-02, 2015-10-03]` (if any do, they will be counted in `total_row_count` and `rows_from_offset[d][+1]` but will not raise `available_contributing_files_count` above the post-2015 cone-size cap of 5).

**T−3650 omission:** T−3650 is excluded from the expected cone for every `d` in the locked window. T−3650 absence is universal per §10.2 and is surfaced by the `out_of_window_sqldate_diagnostic` (Decision E §10.3), not by the per-date `coverage_quality_flag`.

**`coverage_quality_flag` — closed value domain (any other value is a hard-fail per Decision I):**

| # | Flag value | Definition |
|---|---|---|
| 1 | `full` | `available_contributing_files_count[d] == expected_contributing_files_count[d]`: all era-conditioned cone members are in-universe and present (none is a substrate-gap, none is excluded by no-2023+, none is pre-window). |
| 2 | `t0_absent_substrate_gap` | `f_d` is in the known substrate-gap list (per Decision G); all other expected cone members are in-universe and present. |
| 3 | `right_truncated_2022_seal` | One or more of T−1 / T−7 / T−30 / T−365 contributions are absent because `d + n ≥ 2023-01-01` and the corresponding `f_(d+n)` is excluded by the no-2023+ posture (§11.1); T=0 is present; no other absences apply. |
| 4 | `left_truncated_2013_edge` | T+1 contribution absent because `f_(d−1)` is pre-window (`d − 1 < 2013-04-01`); applies to `d = 2013-04-01` only (in the pre-2015 T+1 era); T=0 is present; no other absences apply. |
| 5 | `t_plus_1_neighbor_substrate_gap` | `d` is in the pre-2015 T+1 era and `f_(d−1)` is a substrate-gap date (Decision G), so the expected T+1 contribution is unavailable; T=0 is present; no other absences apply. |
| 6 | `multiple` | Two or more of flags 2–5 apply to `d`. The flag value is then an ordered concatenation joined by `+` (e.g., `right_truncated_2022_seal+t0_absent_substrate_gap`), with components in the numeric order above (lowest `#` first). |

The runner emits **exactly one** `coverage_quality_flag` value per civil date drawn from the above six-value closed set. Any deviation is a hard-fail per Decision I.

**`coverage_completeness` — exact formula:**

```
coverage_completeness[d] = available_contributing_files_count[d] / expected_contributing_files_count[d]
```

Where:

- `expected_contributing_files_count[d]` is the era-conditioned cone size: `6` for `d ≤ 2015-01-01`; `5` for `d ≥ 2015-01-02`.
- `available_contributing_files_count[d]` is the number of distinct publishing-file nominal dates from `d`'s era-conditioned cone that are present in the §10 recognized-list capture (i.e., are in-universe). A file in-universe but with status `expected_absent_per_recognized_list` (a substrate-gap file per Decision G) counts as **not** available — substrate-gap files decrement `available_contributing_files_count`. A cone member whose nominal date maps to a 2023+ date (`d + n ≥ 2023-01-01`) is **not** in-universe per §11.1 and counts as not available. A cone member whose nominal date maps to a pre-window date (`d + n < 2013-04-01` or `d − 1 < 2013-04-01` for the T+1 case) is **not** in-universe and counts as not available.

The formula is **fraction of expected offset buckets observable for that SQLDATE under the locked fetch universe**, not fraction of row-count contribution observed (which is not knowable a priori without fetching) and not any other ratio. The runner must use exactly this formula; alternative formulas are forbidden and any deviation is a hard-fail per Decision I.

The numeric score is in `[0.0, 1.0]` inclusive. `coverage_quality_flag = full` corresponds to `coverage_completeness = 1.0`. All other flag values correspond to `coverage_completeness < 1.0`.

### 11.4 No imputation

- The build does **not** impute counts for missing contributions.
- The build does **not** project a "what would the T−365 count have been if 2023+ files were available" estimate.
- The build does **not** apply any historical-rate extrapolation, model-based fill, or substitution.
- A missing contribution is simply absent from the sum.

### 11.5 No normalization based on market outcomes

- The no-market-data firewall (§4.6) forbids any normalization driven by market measures.
- The build does **not** scale, weight, or transform counts based on trading volume, volatility, returns, indices, or any other market reference.

### 11.6 No post-2022 leakage

- The build does **not** fetch any 2023+ URL.
- The build does **not** accept any 2023+ SQLDATE in parsed rows (hard-fail per Decision I).
- The build does **not** allow any 2023+ date to appear in the output domain, in any metadata field, in any per-file manifest, in any diagnostic.
- A future window-extension (e.g., post-2022 daily-regime ingestion) requires a separate explicit authorization memo and is not authorized here.

### 11.7 What Decision F does NOT do

- Does not authorize any 2023+ access.
- Does not change the locked daily-regime window.
- Does not introduce any extrapolation, imputation, or model-based fill.
- Does not introduce market data.

## 12. Decision G — substrate gaps and missing publishing files

**Decision: known substrate-gap dates (`2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19` per `a8a9dd2` §2 and §10) are not fetched; their absence is recorded as `status = expected_absent_per_recognized_list` in the per-file manifest. SQLDATEs corresponding to gap dates still appear in the output domain (per Decision B) and may receive contributions from neighbor publishing files' T−1, T−7, T−30, T−365, or T+1 buckets. Unexpected retrieval failures (HTTP non-200 for any in-universe URL) are hard-fail stop conditions per Decision I, not "missing publishing files."**

### Options evaluated

| Option | Verdict | Rationale |
|---|---|---|
| A. Encode known gaps as `expected_absent_per_recognized_list` diagnostics; gap SQLDATEs remain eligible in the full civil output domain (Decision B); unexpected HTTP failures are hard-fail per Decision I | **SELECTED** | Matches the locked output-domain choice from Decision B (full civil calendar); preserves substrate-gap visibility in the per-file manifest; allows gap SQLDATEs to receive neighbor contributions (T−1, T−7, T−30, T−365, T+1) where neighbor files are present. |
| B. Drop gap SQLDATEs from the output domain | Rejected (permanently forbidden by Decision B's locked premise) | Decision B Option 1 commits to a full civil calendar; dropping gap dates would create a non-uniform domain dependent on the substrate-gap list and defeat downstream-system stability. |
| C. Hard-fail on encountering a known substrate gap | Rejected (permanently forbidden by substrate-fidelity discipline) | Substrate gaps are expected substrate properties (per `a8a9dd2` §2 / §10); halting on every gap would prevent the build from ever completing on the recognized universe. Hard-fail is reserved for **unexpected** retrieval failures per Decision I. |
| D. Fill gap dates by interpolation, model-fill, or substitution from nearby publishing files | Rejected (permanently forbidden by substrate-fidelity discipline and the no-imputation clause in §11.4) | Would silently inject extrapolated data into the primary series; equivalent in spirit to Decision F Option C, which is permanently rejected. |

### 12.1 Known substrate gaps from the recognized-list universe

The substrate-validation memo `a8a9dd2` §2 and the probe execution report `9319d30` (negative control) established four known publishing-file gap dates:

| Gap date | Source of knowledge |
|---|---|
| `2014-01-23` | Negative control HTTP 404 in `9319d30` |
| `2014-01-24` | `a8a9dd2` §10 (four-2014-dailies substrate-gap model) |
| `2014-01-25` | `a8a9dd2` §10 |
| `2014-03-19` | `a8a9dd2` §10 |

These dates are **not in the §10 recognized-list capture's in-window unit list** (the capture was acquired with the gap dates already excluded as the canonical input universe).

### 12.2 Distinction — expected absent vs unexpected retrieval failure

- **Expected absent**: a civil day whose publishing file is not in the §10 capture. No HTTP request is issued. Recorded in the per-file manifest as `status = expected_absent_per_recognized_list`, `http_status = none/not_requested`. The build proceeds normally.
- **Unexpected retrieval failure**: a civil day whose publishing file **is** in the §10 capture but fails to retrieve at run time (HTTP non-200, connection error, redirect, timeout). This is a **hard-fail stop condition** per Decision I. The build halts; no daily-count outputs are written; a diagnostic identifies the failing URL and class.

The distinction is crucial: it prevents the build from silently producing a partial daily-count series under retrieval flakiness.

### 12.3 Gap dates can still appear as SQLDATEs from other publishing files

Even though `f_(2014-01-23)` is absent, the SQLDATE `2014-01-23` can appear as:

- T−1 row in `f_(2014-01-24)`: ABSENT (also a gap date).
- T−7 row in `f_(2014-01-30)`: contributing (in-universe).
- T−30 row in `f_(2014-02-22)`: contributing.
- T−365 row in `f_(2015-01-23)`: contributing.
- T+1 row in `f_(2014-01-22)`: contributing (pre-2015 era, in-universe).

So the daily-count row for `2014-01-23` will be assembled from whichever neighbor contributions exist. The `coverage_quality_flag` documents the T=0 absence and the T−1 absence.

### 12.4 Output series includes gap SQLDATEs

Per Decision B (Option 1: full civil calendar), the output domain includes every civil day in `[2013-04-01, 2022-12-31]`. Gap days are not removed from the domain; they simply have `t0_file_status = expected_absent_per_recognized_list` and `coverage_quality_flag = t0_absent_substrate_gap` (or `multiple` if other contributing files are also absent).

### 12.5 Required gap diagnostics

The metadata JSON includes a `substrate_gap_diagnostic` section:

```
{
  "known_substrate_gap_dates": ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"],
  "substrate_gap_dates_not_fetched": ["2014-01-23", "2014-01-24", "2014-01-25", "2014-03-19"],
  "substrate_gap_dates_with_nonzero_count_via_neighbor_contributions": [
    {"sqldate": "2014-01-23", "neighbor_contributions": {...}},
    ...
  ]
}
```

### 12.6 What Decision G does NOT do

- Does not authorize fetching gap dates.
- Does not modify the §10 recognized-list capture.
- Does not silently treat unexpected HTTP failures as substrate gaps.
- Does not impute T=0 contributions for gap dates.

## 13. Decision H — retrieval policy and run authorization design (design-only)

**Decision: the future build runner ships inert by default under a three-guard discipline (module constant + CLI flag + env var); fetches each in-universe URL exactly once; uses a redirect-disabled opener; halts hard on any redirect / non-200 / timeout / connection error; writes outputs to `results/lane2_gdelt1_full_daily_count_build/<UTC-timestamp>/`; emits a post-run report at `docs/lane2_gdelt1_full_daily_count_build_execution_report_v0.1.md` for the first run; treats execution as a separately authorized enable-then-inert-restore cycle (this memo does NOT authorize it).**

### Options evaluated

| Option | Verdict | Rationale |
|---|---|---|
| A. Three-guard exact-once live retrieval (module constant `FULL_BUILD_AUTHORIZED` + CLI flag `--authorize-full-build-run` + env var `LANE2_FULL_BUILD_AUTHORIZED=1`); enable / run / restore commit cycle as a separately authorized future workstream | **SELECTED** | Mirrors the Lane 2 discipline established by count-feasibility (`60ec1521 → fe74255 → 9e329c2`), event-file probe (`e81208d → 7c85e3f → 9319d30`), and characterization (`3537a62 → 73a7911 → 858b501`) runners; operationalizes the no-market-data / no-Step-2 firewall procedurally. |
| B. Direct unguarded run (single-flag or no-flag execution) | Rejected (permanently forbidden by the Lane 2 procedural discipline) | The three-guard pattern is how the no-market-data / no-Step-2 firewall is operationalized; weakening it weakens the firewall. Any unguarded execution path would defeat the audit chain established across prior runners. |
| C. Retrying downloader (automatic retry on transient HTTP failure) | Rejected (not for this design; available via future explicit authorization if a substrate-side reason emerges) | Weakens the exactly-once fetch semantics and could mask substrate-side flakes (e.g., GDELT-side mutability) as recovered. A future memo could authorize a retry policy with explicit substrate-side justification. |
| D. Offline-only build from pre-preserved payloads (use already-fetched bytes only, no live retrieval) | Rejected (not for this design; available via future explicit payload-preserving authorization) | Requires payload-preservation runs to exist first, which §15.11 specifically excludes by default. A future memo could authorize a payload-preserving variant and a downstream offline-replay variant; both are out of scope here. |

### 13.1 Default inert

- Module constant `FULL_BUILD_AUTHORIZED = False` at the top of the runner.
- The runner refuses to execute the network loop unless all three guards (module constant + CLI flag + env var) are simultaneously set.
- The runner exits with a clear error message if any one of the three is missing.

### 13.2 Proposed three-guard names

Mirroring the pattern established by count-feasibility / event-file probe / characterization runners:

| Guard | Proposed name |
|---|---|
| Module constant | `FULL_BUILD_AUTHORIZED` (default `False`) |
| CLI flag | `--authorize-full-build-run` |
| Env var | `LANE2_FULL_BUILD_AUTHORIZED=1` |

Path placement in the runner mirrors prior runners:

| Constant location | Inferred line |
|---|---|
| Module constant location | top of file, ≈ line 50 |
| CLI flag location | argparse setup |
| Env var read | inside the `__main__` block before any network call |

The implementation prompt that follows this memo will finalize the exact names and locations.

### 13.3 Exact-once fetch policy

- Each in-universe URL is fetched **exactly once** per run.
- No retries on failure (failure → hard-fail per Decision I).
- No duplicate URL in the per-file manifest (`assert len(set(urls)) == len(urls)` precondition).
- No re-fetch within a single run.

### 13.4 No retries

- The build does **not** implement automatic retries.
- A retry policy would require a separate authorization (would touch network-load discipline and would change the exactly-once semantics).
- A future run that needs to recover from a transient failure runs as a separate enable-then-inert-restore cycle, not a retry.

### 13.5 Redirect handling

- The runner uses a redirect-disabled opener, mirroring `_RowDateNoFollowRedirectHandler` in the characterization runner (`e9f8781` / `487dadb`) and the equivalent in the event-file probe (`0b341b4`).
- Any 30x response (`301`, `302`, `303`, `307`, `308`) is a **hard-fail** stop condition.
- The runner does not follow redirects, does not retry against the `Location` header, does not cache the redirect target.

### 13.6 HTTP non-200 handling

- Any non-200 response (including 30x, 4xx, 5xx) is a **hard-fail** stop condition.
- The runner halts; no outputs are written; the diagnostic identifies the failing URL and HTTP status.
- Note: the recognized-list capture defines the "in-universe" set; a 404 for an in-universe URL is unexpected (since the capture was built to enumerate only present files). Such a 404 indicates GDELT-side mutability or capture-vs-reality drift, and must surface as hard-fail.

### 13.7 Timeout policy

- Connection timeout: proposed `30` seconds.
- Read timeout: proposed `60` seconds.
- Any timeout is a **hard-fail** stop condition.
- The exact values will be finalized in the implementation prompt.

### 13.8 Output directory convention

- Output dir path: `results/lane2_gdelt1_full_daily_count_build/<UTC-timestamp>/`.
- `<UTC-timestamp>` follows the existing convention: `YYYYMMDDTHHMMSSZ` (e.g., `20260524T123456Z`).
- The output dir is **untracked** per Decision 3A inheritance (and per §15 below).
- The runner creates the dir with `os.makedirs(..., exist_ok=False)` immediately before the network loop (mirroring `_fresh_output_dir` in the characterization runner).
- All output paths must pass a pre-write allow-list gate; a post-hoc tripwire (`_assert_full_build_outputs_allowed` or equivalent) re-verifies after the run.

### 13.9 Expected run report

- The first execution produces a post-run report at `docs/lane2_gdelt1_full_daily_count_build_execution_report_v0.1.md`.
- Report structure mirrors `858b501` (characterization execution report): preflight state; enable/restore commits; run command; output dir path; per-file metrics; aggregate metrics; final classification outcome; boundary-confirmation section.
- The report is committed under a `Record Lane 2 full daily-count build execution report` subject as a separate commit on top of the restore.

### 13.10 Enable / restore as separate future authorization step

- The runner's three-guard flip → run → guard-flip-back cycle is a **separately authorized future workstream**, not authorized by this memo and not authorized by the upcoming implementation prompt.
- The implementation prompt is design-mirror only: it implements the runner with `FULL_BUILD_AUTHORIZED = False` and tests; it does **not** flip the guard, does **not** invoke the network loop, does **not** contact GDELT.
- A subsequent **build-execution-authorization prompt** would authorize the enable commit; then the run; then the restore commit; then the post-run report; then a consolidated memory update. The chain mirrors `3537a62 → run → 73a7911 → 858b501`.

### 13.11 What Decision H does NOT do

- Does **not** implement the runner.
- Does **not** authorize any GDELT contact.
- Does **not** flip any guard.
- Does **not** create any output directory.
- Does **not** write any file.
- Does **not** assume the runner names or paths above are final; the implementation prompt may refine them within the constraints stated.

## 14. Decision I — parser validation and stop conditions

**Decision: nine classes of substrate-property violations are hard-fail stop conditions (halt run, emit diagnostic, write no daily-count outputs). Three classes of expected substrate-property anomalies are reportable diagnostics (recorded in metadata, do not halt). Silent repair is forbidden in all cases.**

### Options evaluated

| Option | Verdict | Rationale |
|---|---|---|
| A. Hard-fail on the nine structural contract violations enumerated in §14.1; reportable diagnostics for malformed-short, unparseable-SQLDATE, and out-of-window SQLDATE rows (§14.2); no silent repair (§14.4) | **SELECTED** | Distinguishes substrate-property violations (which invalidate the build's correctness invariants) from expected substrate-property anomalies (which affect only specific rows). Mirrors the diagnostic discipline of the characterization runner (`858b501` §13) and the event-file probe (`9319d30`). |
| B. Permissive repair / coercion (e.g., snap unexpected offsets to nearest known offset; truncate 2023+ SQLDATEs to the last in-window date) | Rejected (permanently forbidden by substrate-fidelity discipline and §14.4 "no silent repair") | Silent repair masks substrate-property changes; would prevent detection of substrate drift or parser bugs and would defeat the audit chain. |
| C. Soft-warn all anomalies and continue (no hard-fail) | Rejected (permanently forbidden by the locked premises of exact-integer offset taxonomy and the no-2023+ posture) | Would allow substrate-violating offsets and 2023+ rows to slip into the primary daily-count series, violating both the `487dadb` exact-integer taxonomy and the §11.1 no-2023+ lock. |
| D. Drop anomalous rows silently (no halt, no diagnostic) | Rejected (permanently forbidden by substrate-fidelity discipline and §14.4) | Would corrupt the primary series with no audit trail and prevent any recovery; the worst-case outcome for a substrate instrument. |

### 14.1 Hard-fail stop conditions (substrate-property violations)

A hard-fail condition halts the run before any daily-count output is written. The runner emits a structured diagnostic identifying the failing condition. No partial daily-count series is produced.

| # | Condition | Detection point | Diagnostic structure |
|---|---|---|---|
| 1 | **Unexpected offset** outside `{0, −1, −7, −30, −365, −3650, +1}` | Row aggregation | `{condition, file_url, sqldate, offset, observed_offset_set_so_far}` |
| 2 | **Recognized-list mismatch** (URL not in §10 capture) | URL construction | `{condition, attempted_url, capture_sha}` |
| 3 | **2023+ SQLDATE row** | Row parsing | `{condition, file_url, sqldate, offset}` |
| 4 | **2023+ URL construction attempt** | URL precondition check | `{condition, attempted_url, year, locked_window}` |
| 5 | **Output allow-list violation** | Pre-write gate or post-hoc tripwire | `{condition, attempted_path, allow_list_pattern}` |
| 6 | **HTTP non-200** | Network response | `{condition, file_url, http_status, response_size}` |
| 7 | **Redirect (30x)** | Network response | `{condition, file_url, http_status, location_header_present, location_value_redacted_or_listed}` |
| 8 | **Connection error / timeout** | Network exception | `{condition, file_url, exception_class, timeout_class}` |
| 9 | **Header anomaly** (per-file) | CSV header parsing | `{condition, file_url, observed_header, expected_header_fragment}` |

For all hard-fail conditions, the runner:

- Halts execution immediately.
- Does **not** write any primary daily-count output.
- Does **not** write any partial per-file payload.
- Emits a hard-fail diagnostic to stderr and to a `halt_diagnostic.json` artifact under the partial output dir.
- Exits with a non-zero status code.

### 14.2 Reportable diagnostics (expected substrate-property anomalies)

A reportable diagnostic is recorded in the per-file manifest and in the metadata JSON's diagnostic section. It does **not** halt the run.

| # | Condition | Reporting |
|---|---|---|
| A | **Malformed-short rows** (row missing SQLDATE column) | Per-file count in manifest; total in metadata |
| B | **Unparseable SQLDATE rows** (SQLDATE value not parseable as YYYYMMDD) | Per-file count in manifest; total in metadata |
| C | **Out-of-window SQLDATE rows** (SQLDATE < 2013-04-01) | Per Decision E §10.3 |

The characterization at `858b501` §10 observed **zero** of any of these anomalies across 16 sampled files. Any non-zero observation in the full build is a genuine substrate property worth surfacing — but is not, by itself, a stop condition. (A pattern of high anomalies might motivate a follow-up substrate-validation memo, but that is a future workstream, not built into this runner.)

### 14.3 Hard-fail vs diagnostic rationale

- **Hard-fail** applies when the substrate is observed to **violate** an invariant the locked premises depend on (taxonomy is exhaustive, no 2023+, no redirects, all URLs from capture, etc.). A violation invalidates the build's output.
- **Reportable diagnostic** applies when an anomaly is **observed but expected to occur at low rate** (malformed rows, unparseable SQLDATEs). These do not invalidate the build's output for other rows; the affected rows are excluded from counts but the rest of the build proceeds.

### 14.4 No silent repair

- The runner does **not** silently coerce an unexpected offset to the nearest known offset.
- The runner does **not** silently truncate a 2023+ SQLDATE to the last in-window date.
- The runner does **not** silently retry a failed HTTP.
- The runner does **not** silently impute a missing SQLDATE column.
- The runner does **not** silently rewrite output paths to fit the allow-list.
- The runner does **not** silently re-key a row whose offset is outside the taxonomy.

Every anomaly is **either** a hard-fail with diagnostic **or** a reportable diagnostic that affects only the specific row(s); never a silent transformation that hides the substrate's behavior.

### 14.5 What Decision I does NOT do

- Does not relax any of the hard-fail conditions.
- Does not introduce any retry policy.
- Does not authorize per-file overrides.
- Does not modify the locked offset taxonomy.

## 15. Decision J — output artifact design

**Decision: the future build produces five categories of output: (1) primary daily-count CSV/Parquet series; (2) metadata JSON with full provenance and diagnostics; (3) human-readable summary Markdown; (4) per-file manifest (embedded in metadata); (5) SHA-256 manifest of fetched bytes (embedded in metadata). Raw compressed payload zips are NOT preserved by default after parsing — only the SHA-256 of each fetched payload is recorded — to bound local disk usage; a future explicit prompt may authorize payload-preserving variants. All artifacts remain untracked indefinitely per Decision 3A precedent; the post-run report Markdown under `docs/` is the only tracked artifact.**

### Options evaluated

| Option | Verdict | Rationale |
|---|---|---|
| A. Write lightweight derived artifacts only (`daily_count.csv` / `build_metadata.json` / `build_summary.md` / per-file manifest embedded / SHA-256 manifest embedded); no raw payload preservation after parsing per §15.11; all future build artifacts untracked by default unless a later explicit artifact-disposition memo says otherwise | **SELECTED** | Bounds local disk pressure to a single payload at a time (§15.11); preserves bytes-witness provenance through the SHA-256 manifest; inherits Decision 3A's untracked-by-default discipline from `0065d10` §8 / §15.10. |
| B. Preserve all raw compressed payloads in the timestamp output directory | Rejected (not for this design; available via future explicit payload-preserving authorization memo) | Would impose ≈ tens of GiB local disk pressure per run (extrapolated from the characterization sample at §15.11 rationale). A future memo could authorize a one-time comprehensive audit run that preserves all payloads. |
| C. Preserve selected payloads only (e.g., a sample, a substrate-anomaly subset, or a year-boundary subset) | Rejected (not for this design; available only through a future explicit revision memo that defines the selection criterion) | Requires a downstream selection rule this design memo does not provide. A future memo could define `preserve_if_anomaly_observed=True` or a sampling-by-era criterion; out of scope here. |
| D. Write only the primary `daily_count.csv` without metadata, manifest, or summary | Rejected (permanently forbidden by audit / provenance discipline) | Defeats the bytes-witness function under the no-payload-preservation default (§15.11); breaks parity with the probe (`9319d30`) and characterization (`858b501`) audit precedent; leaves no path to verify what the build saw. |

### 15.1 Primary daily-count artifact

Path: `daily_count.csv` (and/or `daily_count.parquet`) under the timestamped output dir.

Columns:

| Column | Type | Description |
|---|---|---|
| `civil_date` | `YYYY-MM-DD` | Output date (one row per civil day in `[2013-04-01, 2022-12-31]`) |
| `total_row_count` | `int` | Sum of all in-universe rows with SQLDATE = civil_date |
| `rows_from_offset_0` | `int` | T=0 contribution (from `f_(civil_date)`) |
| `rows_from_offset_minus_1` | `int` | T−1 contribution |
| `rows_from_offset_minus_7` | `int` | T−7 contribution |
| `rows_from_offset_minus_30` | `int` | T−30 contribution |
| `rows_from_offset_minus_365` | `int` | T−365 contribution |
| `rows_from_offset_minus_3650` | `int` | T−3650 contribution (structurally zero per §10.2; column retained for schema regularity and to surface any future violation) |
| `rows_from_offset_plus_1` | `int` | T+1 contribution (pre-2015 era only) |
| `t0_file_status` | enum | `present` / `expected_absent_per_recognized_list` / `out_of_universe` |
| `expected_contributing_files_count` | `int` | Maximum (typically 7, less near boundaries) |
| `available_contributing_files_count` | `int` | Actual subset in-universe |
| `coverage_quality_flag` | enum/string | Per §11.3 closed value domain (`full` / `t0_absent_substrate_gap` / `right_truncated_2022_seal` / `left_truncated_2013_edge` / `t_plus_1_neighbor_substrate_gap` / `multiple`) |
| `coverage_completeness` | `float` | `available_contributing_files_count / expected_contributing_files_count` |

Format note: CSV is the canonical text format for portability and audit; Parquet is optional for downstream-system efficiency. The implementation prompt may emit both; only the CSV is required.

### 15.2 Metadata JSON

Path: `build_metadata.json` under the timestamped output dir.

Top-level sections:

- `run_anchors`: commit SHA at run time; runner SHA-256; capture SHA reference; `command_line`; environment variables (with sensitive values redacted, none are sensitive here); start UTC; end UTC; exit code; locked-window definition; no-2023+ posture commit reference.
- `recognized_list_capture`: SHA-256 reference, byte size, list of all enumerated in-universe URLs.
- `per_file_manifest`: array of `{url, nominal_date, http_status, http_status_class, bytes_fetched, sha256, row_count, malformed_short_rows, unparseable_sqldate_rows, header_anomaly_detected, post_2022_sqldate_rows_count (must be 0), offset_distribution, status (present / expected_absent_per_recognized_list / hard_fail_class), out_of_window_row_count_contributed}` — one entry per URL in the capture.
- `substrate_gap_diagnostic`: per §12.5.
- `out_of_window_sqldate_diagnostic`: per §10.3.
- `parser_anomaly_diagnostic`: per-file and aggregate `malformed_short_rows`, `unparseable_sqldate_rows`, header anomalies.
- `coverage_diagnostic`: per-civil-day `coverage_quality_flag` distribution; counts per flag class.
- `output_allow_list`: list of allowed output file patterns; verification result (pass / fail).
- `boundary_declarations`: explicit `no_market_data: true`, `no_step_2: true`, `no_asset_or_return_logic: true`, `no_category_theme_actor_filtering: true`, `no_spike_threshold_tuning: true`, `no_negative_control: true`, `no_2023plus_access: true`.
- `aggregation_invariants`: counting invariant from §10.4 (sum equality); deterministic-input-output assertion.

### 15.3 Human-readable summary

Path: `build_summary.md` under the timestamped output dir.

Structure mirrors `characterization_summary.md` from the characterization output (`858b501` §8): outcome class; per-class file counts; aggregate row totals; coverage distribution; key diagnostics; run command; output dir path; SHA-256 of `daily_count.csv` and `build_metadata.json`.

### 15.4 Per-file manifest

Embedded in metadata JSON as `per_file_manifest` (see §15.2). The per-file manifest is the audit substrate for the SHA-256 manifest in §15.5 and for the per-URL HTTP outcomes recorded in the post-run report.

### 15.5 SHA-256 manifest of fetched bytes

Embedded in metadata JSON as `per_file_manifest[*].sha256`. Every fetched zip's SHA-256 is recorded **before** any in-memory decompression to maintain bytes-witness provenance. The SHA-256 of every output file is also recorded in the metadata JSON. The build's post-run report enumerates these in a SHA table (mirroring `858b501` §8).

### 15.6 Per-date coverage diagnostics

Per §11.3 and §15.1's `coverage_quality_flag` / `coverage_completeness` columns. The metadata JSON's `coverage_diagnostic` section additionally summarizes:

- count of civil dates with `coverage_quality_flag = full`;
- count per other flag class;
- list of right-truncated dates with which offset buckets are absent;
- list of left-truncated dates;
- list of substrate-gap dates and their `coverage_quality_flag`.

### 15.7 Per-offset counts

Surfaced as columns in the primary daily-count CSV (§15.1) **and** as aggregate-level counts in the metadata JSON (mirroring `858b501` §11's offset-row-totals table for the characterization sample; the full build's totals will be substantially larger).

### 15.8 Parser-anomaly diagnostics

Per Decision I §14.2: malformed-short, unparseable-SQLDATE counts per file and in aggregate. Surfaced in the metadata JSON's `parser_anomaly_diagnostic` section.

### 15.9 Out-of-window SQLDATE diagnostics

Per Decision E §10.3. Surfaced in the metadata JSON's `out_of_window_sqldate_diagnostic` section.

### 15.10 Artifact disposition default — untracked

- The future full-build output dir `results/lane2_gdelt1_full_daily_count_build/<UTC-timestamp>/` is **untracked indefinitely** by default, mirroring Decision 3A from `0065d10`.
- The only artifact this build produces that becomes **tracked** is the post-run report at `docs/lane2_gdelt1_full_daily_count_build_execution_report_v0.1.md`, which records all SHAs and metrics necessary for audit. Tracking is by separate commit (mirroring `858b501`).
- A future explicit prompt may revisit artifact disposition (consistent with D3A's `temporary, revisitable by future explicit memo` framing).

### 15.11 Raw compressed payload preservation — DEFAULT: NOT PRESERVED

- The build's **default behavior** is to **NOT preserve raw payload zips after parsing**. Each fetched zip is hashed (SHA-256), decompressed, parsed, and the zip bytes are then discarded before the next URL is fetched.
- **Mechanism-level rule (binding on the implementation prompt):** the runner may stream or download each compressed payload into memory **or** into a per-file temporary file (e.g., under the OS temp directory or under a `tmp/` subdirectory of the run's timestamp output dir) only long enough to hash and parse it; **the payload bytes (memory buffer or temp file) must be discarded before proceeding to the next URL and must not be present in the final output directory at run completion.** The runner must **not** hold all payloads in memory simultaneously (memory-safety constraint at the universe scale enumerated in §6.8) and must **not** retain any temp file beyond the per-URL fetch-hash-parse cycle. The runner must **not** preserve raw compressed payloads in the final output directory unless a future explicit payload-preserving authorization overrides this design.
- **Temp-file specifics (if a temp-file path is chosen by the implementation):** any temp file created during a fetch-hash-parse cycle must be deleted before the runner moves on to the next URL. A successful run terminates with **no temp file remaining**. An aborted run (hard-fail per Decision I) may leave at most one temp file (the one in progress at halt time), which the runner must attempt to delete in its halt-cleanup path. Temp file paths are **not** part of the final artifact allow-list (§15.10 / §15.13); their post-hoc presence in the output directory is itself a hard-fail per Decision I's allow-list-violation class.
- **Rationale**: extrapolating from the characterization sample (16 files ≈ 119.4 MiB) to the full universe (likely ≈ thousands of files; estimated ≈ tens of GiB total) suggests that preserving every raw zip locally for every run would impose unacceptable disk pressure. Per-URL streaming + per-URL discard keeps peak disk pressure to a single payload's size (≈ low-tens of MiB) and bounds peak memory similarly. The SHA-256 manifest combined with the GDELT-side files (modulo GDELT mutability) preserves bytes-witness provenance.
- A future explicit prompt may authorize a **payload-preserving variant** of the runner (e.g., for a single comprehensive audit run, or for a frozen-snapshot capability under separate authorization). This memo does **not** authorize any payload-preserving execution; the implementation prompt that follows this design memo must implement only the default no-preservation behavior described above.
- Even under the default no-payload-preservation policy, the SHA-256 of every fetched zip is recorded in the metadata JSON; the manifest is the canonical bytes-witness record.

### 15.12 Distinction — payload preservation vs git tracking

- **Payload preservation** = "the raw zip exists on local disk after parsing." The full-build memo selects NOT to preserve as the default (§15.11).
- **Git tracking** = "the artifact is committed to the repo." The full-build memo extends D3A's "untracked indefinitely" to **all build output artifacts**, including the primary daily-count CSV, the metadata JSON, the summary Markdown, and any payload zips that future variants might preserve.
- The only **tracked** artifact of the full build is the post-run execution report under `docs/` (§15.10).
- A future prompt may separately revisit (a) whether to preserve payloads on local disk, and (b) whether to track any build output artifacts as audit evidence.

### 15.13 What Decision J does NOT do

- Does not produce any actual artifact (this memo writes only itself).
- Does not authorize preserving payload zips beyond the SHA-256 manifest.
- Does not authorize tracking build output artifacts in git.
- Does not commit the runner to a specific binary format (CSV vs Parquet vs both).

## 16. Decision K — future implementation / test requirements

**Decision: the future runner+test implementation prompt must produce a standalone runner at `scripts/run_lane2_gdelt1_full_daily_count_build.py` and a paired test file at `tests/test_lane2_gdelt1_full_daily_count_build.py`, covering twelve test categories enumerated below. The implementation prompt does NOT execute the build, does NOT contact GDELT, does NOT flip the guard. A separate build-execution-authorization prompt would follow.**

### 16.1 Implementation path candidates

| Candidate | Verdict |
|---|---|
| `scripts/run_lane2_gdelt1_full_daily_count_build.py` | **SELECTED** (mirrors prior runners) |
| `src/lane2_gdelt1_full_daily_count_build.py` + thin script wrapper | Alternative; rejected for now (prior runners are standalone) |

The implementation prompt may revise to the alternative if the runner exceeds, say, ~1,500 lines and a library split would aid testability; the design memo does not insist.

### 16.2 Test file path

`tests/test_lane2_gdelt1_full_daily_count_build.py` — mirrors the naming pattern of `tests/test_lane2_gdelt1_row_date_characterization.py` (`e9f8781`) and `tests/test_lane2_gdelt1_event_file_probe.py` (`0b341b4` / `845c51c`).

### 16.3 Required test categories

| # | Category | Description |
|---|---|---|
| 1 | **Date-domain handling** | Civil calendar enumeration over `[2013-04-01, 2022-12-31]`; correct day count (3,562); correct boundary handling at left and right edges; correct leap-year handling within the window |
| 2 | **SQLDATE re-keying** | Every parsed row routed by its SQLDATE; no row routed by nominal file date; uniform handling across all seven offset buckets; offset arithmetic is exact-integer-day |
| 3 | **T+1 uniform handling** | T+1 rows from a pre-2015 file at nominal `f.nominal_date` routed to `SQLDATE = f.nominal_date + 1` (so that file's contribution arrives at the next-day's daily count); no per-row T+1 flag; no era-conditional code path |
| 4 | **Backward edge** | Row in a 2013-era file with SQLDATE outside the window (e.g., `2003-04-04` from T−3650) excluded from primary series; recorded in `out_of_window_sqldate_diagnostic`; primary series row for `2003-04-04` does NOT exist |
| 5 | **Forward edge** | Civil day `2022-12-31` receives T=0 contribution; T−1, T−7, T−30, T−365, T−3650 contributions absent (right-truncated); `coverage_quality_flag = right_truncated_2022_seal` set; no 2023+ URL attempted in any test fixture |
| 6 | **Known substrate gaps** | `2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19` not in the in-universe URL list passed to the runner's test fixture; the runner does not issue HTTP requests for them; each is recorded as `expected_absent_per_recognized_list`; SQLDATEs for these dates still appear in the primary series via neighbor contributions when neighbor files are present |
| 7 | **No-2023+ posture** | Runner refuses to construct any URL with year ≥ 2023; runner halts on any 2023+ SQLDATE encountered in test-fixture rows; runner does not allow any 2023+ date in the output domain |
| 8 | **No-market-data leakage** | Runner does not import `pandas-datareader`, `yfinance`, market-data APIs, asset-data libraries, return-windowing libraries, or any other market-side dependency; output schema does not include any market-side column; metadata JSON declares `no_market_data: true`, `no_step_2: true`, `no_asset_or_return_logic: true`, `no_category_theme_actor_filtering: true`, `no_spike_threshold_tuning: true`, `no_negative_control: true`, `no_2023plus_access: true` |
| 9 | **Output allow-list** | Pre-write gate rejects any file path not matching `^(daily_count\.csv|daily_count\.parquet|build_metadata\.json|build_summary\.md|halt_diagnostic\.json)$` (and the SHA-256 manifest if a separate file); post-hoc tripwire re-asserts; both gates fire on any violation |
| 10 | **Exact offset taxonomy** | Runner halts hard on any observed offset outside `{0, −1, −7, −30, −365, −3650, +1}`; runner does not silently coerce to nearest known offset; runner's tests verify all seven specific offsets and several near-miss negatives (e.g., `−2`, `−6`, `−8`, `−29`, `−31`, `−364`, `−366`, `−3649`, `−3651`, `+2`) |
| 11 | **Deterministic manifests** | Two runs over the same fixture input produce byte-identical `build_metadata.json` modulo a small whitelist of timestamps; `daily_count.csv` is byte-identical; the SHA-256 manifest is deterministic given fixed input |
| 12 | **Paired regression** | After the full-build runner is added to the repo, all existing test suites still pass: characterization (62 tests in `tests/test_lane2_gdelt1_row_date_characterization.py`), event-file probe (`tests/test_lane2_gdelt1_event_file_probe.py`), count-feasibility, and any other repo-wide test discovery; no shared-module drift |

### 16.4 Test discipline notes

- Tests run **offline only**: no test issues a real HTTP request. All HTTP responses are mocked via in-process opener substitution (mirroring the characterization runner's test fixtures).
- Tests run with `PYTHONDONTWRITEBYTECODE=1` discipline (no `__pycache__/` or `.pyc` pollution).
- Tests **must** be invokable via `python3 -m pytest tests/test_lane2_gdelt1_full_daily_count_build.py -q` and via the broader `python3 -m pytest tests/` for paired regression.
- Tests **must not** flip the runner's `FULL_BUILD_AUTHORIZED` guard. Authorization gating is tested by setting the env var / CLI flag separately in fixtures, then exercising the precondition-check path (which is part of the runner's API surface, not the network loop).

### 16.5 What Decision K does NOT do

- Does not implement the runner.
- Does not implement the tests.
- Does not run any test.
- Does not contact GDELT.
- Does not authorize the enable/run/restore cycle (that is a separate, post-implementation workstream).

## 17. Consequences for future build-runner implementation

The implementation prompt that follows this memo must:

1. **Adopt the locked premises** (§4) verbatim, citing `0065d10` §5.
2. **Implement Decision A** (build input universe) by reading the §10 recognized-list capture from its on-repo path, asserting the SHA-256 against the locked value, and enumerating the in-universe URL list.
3. **Implement Decision B** (output date domain) by generating the full civil calendar `2013-04-01` to `2022-12-31` and producing one row per civil day in the primary daily-count CSV.
4. **Implement Decision C** (row-count semantics) by counting raw rows, no deduplication, no filtering, retaining per-offset diagnostic counts.
5. **Implement Decision D** (SQLDATE aggregation rule) per the pseudocode in §9.1.
6. **Implement Decision E** (backward edge handling) per §10.
7. **Implement Decision F** (forward edge / 2022-seal coverage) per §11.
8. **Implement Decision G** (substrate gaps) per §12.
9. **Implement Decision H** (retrieval policy) under three-guard discipline (`FULL_BUILD_AUTHORIZED` + `--authorize-full-build-run` + `LANE2_FULL_BUILD_AUTHORIZED=1`), redirect-disabled opener, exact-once fetch, no retries; runner ships inert.
10. **Implement Decision I** (parser validation) with the nine hard-fail classes and three reportable-diagnostic classes; no silent repair.
11. **Implement Decision J** (output artifact design) with the five categories, allow-list gating, pre-write + post-hoc tripwire, default no-payload-preservation, SHA-256 manifest.
12. **Implement Decision K** (test suite) with all twelve test categories before any execution authorization.
13. **Use** `PYTHONDONTWRITEBYTECODE=1` discipline throughout.
14. **Do not** flip the guard; **do not** execute the network loop; **do not** create the output directory under any non-test code path; **do not** contact GDELT.

The implementation prompt then closes with a single tracked commit adding the runner + tests; the runner is inert by default; the tests pass against mocked HTTP. A subsequent **build-execution-authorization prompt** would mirror the structure of `3537a62 → 73a7911 → 858b501`:

- Enable commit (flip `FULL_BUILD_AUTHORIZED` to `True`; one-line +1/−1).
- Single live run with inline env var + CLI flag.
- Restore commit (flip back to `False`; one-line +1/−1; runner byte-identical pre-/post-cycle).
- Post-run execution report at `docs/lane2_gdelt1_full_daily_count_build_execution_report_v0.1.md`.
- Consolidated memory update.

Neither the implementation prompt nor the execution-authorization prompt is authorized by this memo.

## 18. Boundaries that remain in force

Until both the runner implementation prompt and the subsequent build-execution-authorization prompt (plus any post-run report and consolidated memory update) have closed cleanly, the following remain **blocked**:

- **Full daily-count build execution.**
- **Runner implementation** (separate explicit prompt required).
- **Market data of any kind.**
- **Step 2 of any kind.**
- **Spike / burst threshold tuning.**
- **Return-window logic.**
- **Asset selection.**
- **Signal-design choices.**
- **Market-predictiveness claim.**
- **Category / theme / actor / geography / tone filtering.**
- **Additional GDELT contact** beyond what a future explicitly-authorized successor characterization, runner test fixture (offline only), or build-execution-authorization prompt may approve.
- **Event-file probe re-run** under the existing implementation.
- **Row-date characterization re-run** under the existing implementation.
- **Output-artifact disposition change** for `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` or `results/lane2_gdelt1_row_date_characterization/20260523T033234Z/` beyond Decision 3A's "untracked indefinitely with SHA references in committed reports."
- **F4 modification** (baselines `41c80c0…624c39d` / `00ce9b2…f5e37552c` preserved).
- **Recognized-list capture modification** (SHA `84ea721e…fff835fc` preserved).
- **Guard flips on any runner.**
- **Source / test / config edits** beyond this memo file.
- **Locked-memo edits** to any of `9319d30` / `a8a9dd2` / `a2a8fd5` / `e9f8781` / `487dadb` / `3537a62` / `73a7911` / `858b501` / `0065d10` / `e55e09a` / `0b341b4` / `845c51c`.
- **Design-note edits** to the existing probe design note (`e55e09a`).
- **Post-§10 diagnostic report staging / commit / edit / delete.**
- **2023+ pre-filter authorization** (no-2023+ posture at `0ddbd51` is in force).
- **Frozen-snapshot execution** (no frozen-snapshot retrieval authorized).
- **`python3` canonicalization** changes.
- **Negative-control payload allow-list change.**
- **Payload-preserving runner variant** (Default per §15.11 is NOT to preserve raw zips after parsing; a future explicit prompt may revisit).
- **Staging / commit / push of this memo or any other artifact** unless separately authorized after review.

**Market data and Step 2 remain blocked unconditionally until the no-market-data firewall is explicitly retired by a future, separately authorized memo.** This memo does not authorize any retirement.

## 19. Final verdict / next frontier

**Final verdict**: `PROCEED TO FULL-BUILD RUNNER IMPLEMENTATION PROMPT AFTER LOCKING THIS DESIGN MEMO.`

The eleven design decisions in this memo —

- **Decision A**: build input universe = §10 recognized-list capture (SHA `84ea721e…fff835fc`), each URL attempted exactly once, no guessed files, no index/listing fetch, no 2023+ URL construction.
- **Decision B**: output date domain = full civil calendar `2013-04-01` through `2022-12-31` (one row per civil day; zero-row days surfaced via coverage diagnostics).
- **Decision C**: row-count semantics = raw row count, no deduplication, no filtering, malformed/unparseable rows excluded from counts but surfaced in diagnostics.
- **Decision D**: SQLDATE aggregation rule = per-row routing by SQLDATE across all in-universe publishing files, uniform across all seven offset buckets including T+1, no nominal-date aggregation, no symmetry normalization, no T+1 special case.
- **Decision E**: backward edge handling = exclude out-of-window SQLDATEs from primary series, report in structured `out_of_window_sqldate_diagnostic` (with explicit per-source-file and per-SQLDATE breakdowns); structural consequence — T−3650 contribution is zero for every in-window date.
- **Decision F**: forward edge / 2022-seal = right-truncation with `coverage_quality_flag`, no imputation, no normalization, no post-2022 leakage; coverage degrades by offset bucket toward 2022-12-31.
- **Decision G**: substrate gaps = expected-absent vs unexpected-failure distinction; gap dates not fetched but their SQLDATEs still appear in the primary series via neighbor contributions; unexpected HTTP failures are hard-fail.
- **Decision H**: retrieval policy (design-only) = three-guard discipline `FULL_BUILD_AUTHORIZED` + `--authorize-full-build-run` + `LANE2_FULL_BUILD_AUTHORIZED=1`, redirect-disabled opener, exact-once fetch, no retries, output dir `results/lane2_gdelt1_full_daily_count_build/<UTC-timestamp>/`, post-run report at `docs/lane2_gdelt1_full_daily_count_build_execution_report_v0.1.md`; enable/restore as a separately authorized cycle.
- **Decision I**: parser validation = nine hard-fail conditions (unexpected offset, recognized-list mismatch, 2023+ SQLDATE, 2023+ URL construction, output allow-list violation, HTTP non-200, redirect, connection error/timeout, header anomaly); three reportable diagnostics (malformed-short, unparseable-SQLDATE, out-of-window SQLDATE); no silent repair.
- **Decision J**: output artifact design = five categories (daily_count CSV, metadata JSON, summary Markdown, per-file manifest embedded, SHA-256 manifest embedded); default no-payload-preservation; only the post-run report Markdown is tracked.
- **Decision K**: future implementation/test requirements = standalone runner at `scripts/run_lane2_gdelt1_full_daily_count_build.py`, tests at `tests/test_lane2_gdelt1_full_daily_count_build.py`, twelve test categories from date-domain handling through paired regression.

— are sufficient to specify a complete, deterministic, substrate-faithful, market-data-free daily attention-count build over the Lane 2 daily-regime window without re-litigating any locked decision from `0065d10` and without introducing any new authorization scope beyond memo persistence.

**Next frontier (NOT next; awaits explicit user initiation)**: full-build runner implementation prompt. The implementation prompt produces a tracked commit adding the runner + paired test file under the eleven design decisions above; the runner ships inert with `FULL_BUILD_AUTHORIZED = False`; the tests pass against mocked HTTP fixtures; **NO** GDELT contact occurs; **NO** guard flips occur.

After the implementation prompt closes, the next eligible workstream is a build-execution-authorization prompt mirroring `3537a62 → 73a7911 → 858b501`. After the execution cycle closes, the next eligible workstream is a consolidated memory update — and only then is the Lane 2 daily-count instrument substrate-side construction complete.

Until each of those three workstreams closes cleanly in order, all blocks in §18 remain in force. The no-market-data firewall remains in force unconditionally; no decision in this memo approaches its retirement.

This memo's authorization scope is complete upon persistence of `docs/lane2_gdelt1_full_daily_count_build_design_memo_v0.1.md`. No staging, commit, or push is authorized by this memo.
