# Lane 2 GDELT1 Step 2 Implementation-Design Memo v0.1

Draft. Untracked. Pre-registers Step 2 feature derivation and pre-execution
conformance requirements **before any implementation**. Required by the
committed Step 2 design memo
(`docs/lane2_gdelt1_step2_design_memo_v0.1.md`, SHA-256
`3f63d0d02b68d46821f498a524065fceac4104e9a3283eaee9cee4d0aaa9632d`), whose §12
recommendation is `STEP 2 IMPLEMENTATION DESIGN REQUIRED NEXT`.

Evidence legend: **[O]** observed git/fs · **[A]** artifact-derived (committed
`build_metadata.json` / `build_daily_counts.csv` / `build_summary.md`) ·
**[I]** design recommendation.

---

## 1. Non-authorization statement

- This memo does **not** authorize Step 2 implementation.
- This memo does **not** authorize Step 2 execution.
- This memo does **not** authorize market-data access.
- This memo does **not** authorize instrument construction.
- This memo does **not** authorize GDELT access, BigQuery use, row export, or
  any substrate mutation.
- It only **designs** the future implementation.

Distinct phases, not to be collapsed: **Step 2 design (already committed) →
Step 2 implementation design (this memo) → implementation → pre-execution
conformance gate → execution authorization → execution**. Any later
market-data join and any instrument construction are **further, separately
authorized** phases beyond Step 2 execution.

## 2. Canonical inputs and pins

**Step 2 design memo (committed)** [O]:
- path: `docs/lane2_gdelt1_step2_design_memo_v0.1.md`
- SHA-256: `3f63d0d02b68d46821f498a524065fceac4104e9a3283eaee9cee4d0aaa9632d`
- 222 lines / 12500 bytes

**Canonical merged substrate (committed)** [O][A]:
- directory: `results/lane2_gdelt1_full_daily_count_build/merged_20260529T175416Z/`
- `build_daily_counts.csv` — 274903 B, SHA-256
  `84b6ac9f47888fea4bd5c9d448058db0e5c568e3aa194a0fc7d4d5c95704045e`
- `build_metadata.json` — 12406 B, SHA-256
  `31ad8085d9df839f833d6af83cb4fdb24ad47c3ecef0bd44b4d730de682a08cf`
- `build_summary.md` — 2620 B, SHA-256
  `7677bbaf3d84923209a8b0be64dd9d3f64ffe752ac56f4eb5ad65169bae86e97`
- `build_manifest_digest`:
  `4b312183d9bb126169fc82c5b76008359778df18ee803527c567f7ade3a89650`

**Repo / runner / guard pins** [O]:
- HEAD = origin/main = `b51abf3a861c8df15fa85f694306dd4d991cb2e6`
- runner blob = `aa1dcd31dfefe9621c2b3b2a8a3288d9c212aa9d`
- `FULL_BUILD_AUTHORIZED = False` at line 95
- `KNOWN_SUBSTRATE_GAPS` at line 163 = exactly the four 2014 dates
  `2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`

## 3. Step 2 purpose

Step 2 is **narrowly defined** here [I]: convert the committed merged daily-count
substrate into a per-civil-date **feature table**. The feature table is derived
**only from GDELT substrate fields** materialized in the merged CSV/metadata.

Explicitly excluded at this stage:
- no market-conditioned feature;
- no outcome, market return, market direction, market volatility, or instrument
  series;
- no instrument construction, signal generation, or backtest;
- no future market/outcome variable.

Step 2 feature derivation is **deterministic, offline, and GDELT-only**.

## 4. Allowed input columns

The feature derivation universe is **strictly restricted** to the following
columns from the merged substrate [A][I]; no other input is permitted:

- `civil_date`
- the seven offset row-count fields: `rows_from_offset_0`, `rows_from_offset_minus_1`,
  `rows_from_offset_minus_7`, `rows_from_offset_minus_30`, `rows_from_offset_minus_365`,
  `rows_from_offset_minus_3650`, `rows_from_offset_plus_1`
- `total_row_count`
- coverage / status fields: `t0_file_status`,
  `expected_contributing_files_count`, `available_contributing_files_count`,
  `coverage_quality_flag`, `coverage_completeness`
- `represented_only`
- `documented_exception_label`
- KSG / terminal-status provenance from `build_metadata.json`
  (`per_chunk[].known_no_data_gap_days`, `per_chunk[].terminal_status_complete`,
  `aggregate.*`, `documented_exceptions[]`) — for per-chunk class derivation and
  for the per-row `is_known_substrate_gap` flag, derived against the pinned
  `KNOWN_SUBSTRATE_GAPS` list

Explicitly forbidden as input:
- any field from market data (prices, returns, volumes, calendars, instrument
  series);
- any future market/outcome variable;
- any post-`2022-12-31` data;
- any GDELT field not materialized in the committed merged substrate (no fresh
  GDELT fetch / BigQuery query / payload download).

## 5. Proposed output artifacts

Future Step 2 implementation will write **three** untracked result-output
artifacts (mirroring the chunk/merge convention) [I]; this memo does **not**
create them:

- `results/lane2_gdelt1_step2_daily_features/<UTC-ts>Z/step2_daily_features.csv`
- `results/lane2_gdelt1_step2_daily_features/<UTC-ts>Z/step2_metadata.json`
- `results/lane2_gdelt1_step2_daily_features/<UTC-ts>Z/step2_summary.md`

These outputs:
- remain **untracked result-output** unless a separately authorized commit turn
  later tracks them;
- must be **pinned to the merged substrate** by including, in
  `step2_metadata.json`, the input directory path, the input
  `build_manifest_digest`, and the three input artifact SHA-256s exactly as
  pinned in §2;
- must record the locked feature schema (§6), the represented-only policy (§8),
  the KSG policy (§9), and the boundary declarations (§12/§13).

## 6. Proposed feature schema

All features below are **pre-registered here**. Adding/removing/changing any
feature requires a new design memo. All thresholds and window lengths listed
below are **locked**; they may not be tuned after seeing the data.

### 6.1 Identity / passthrough

- `civil_date` (ISO)
- `represented_only` (bool)
- `documented_exception_label` (string; empty for non-documented-exception rows)
- `is_known_substrate_gap` (bool) — true iff `civil_date` ∈ pinned
  `KNOWN_SUBSTRATE_GAPS`; never inferred from offset counts
- `terminal_status` (string) — one of
  `raw_t0_present` / `represented_only_documented_exception` / `known_no_data_gap`
  derived deterministically from `documented_exception_label` and
  `is_known_substrate_gap`
- `coverage_quality_flag` (passthrough)

### 6.2 Raw count features

- the seven offset count columns as passthrough
- `total_row_count` (passthrough)

### 6.3 Scale transforms

- `log1p_total_row_count` = `log1p(total_row_count)`
- `log1p_rows_from_offset_0`, `log1p_rows_from_offset_minus_1`,
  `log1p_rows_from_offset_minus_7`, `log1p_rows_from_offset_minus_30`,
  `log1p_rows_from_offset_minus_365`, `log1p_rows_from_offset_minus_3650`,
  `log1p_rows_from_offset_plus_1`

### 6.4 Coverage / completeness

- `offset_count_present_count` — number of the seven offsets with value > 0
- `offset_count_zero_count` — 7 − `offset_count_present_count`
- `has_any_missing_offset_count` — bool, true iff `offset_count_zero_count > 0`
- `coverage_completeness` (passthrough)

### 6.5 Cross-offset structure

- `offset_0_share_of_total` = `rows_from_offset_0 / total_row_count` (NaN-safe:
  emit 0.0 when `total_row_count == 0`)
- each offset's share of total: `share_offset_minus_1`, `share_offset_minus_7`,
  `share_offset_minus_30`, `share_offset_minus_365`,
  `share_offset_minus_3650`, `share_offset_plus_1` (same NaN-safe rule)
- `neighbor_offset_sum` = `rows_from_offset_minus_1 + rows_from_offset_minus_7
  + rows_from_offset_minus_30 + rows_from_offset_minus_365
  + rows_from_offset_minus_3650 + rows_from_offset_plus_1`
- `neighbor_offset_share_of_total` = `neighbor_offset_sum / total_row_count`
  (same NaN-safe rule)
- `nonzero_offset_count` — alias of `offset_count_present_count`, retained for
  readability

### 6.6 Temporal features (past/current GDELT only)

All temporal features are **strictly trailing**: each window covers **the
current row and the prior W−1 rows** (the **current-row-inclusive trailing
convention** is intentional and **locked here**), ordered by `civil_date`
ascending, **with no look-ahead and no market data**. Spike flags (§6.7)
must therefore be interpreted as "large relative to the **current-inclusive
trailing GDELT distribution**," not as a strictly-prior-only surprise
measure; changing to strictly-prior windows would require a new design memo.
The **represented-only / KSG rolling-inclusion policy is locked in §7**
(their recorded `total_row_count` and offset values feed the rolling
statistics verbatim, with no imputation, masking, or exclusion). Locked
window lengths and features:

- trailing rolling mean of `total_row_count` (raw-count descriptive;
  **not** the z-score denominator below): `roll_mean_total_w7`,
  `roll_mean_total_w14`, `roll_mean_total_w30`
- trailing rolling standard deviation of `total_row_count` (raw-count
  descriptive; **not** the z-score denominator below): `roll_std_total_w7`,
  `roll_std_total_w14`, `roll_std_total_w30`
- **trailing rolling mean of `log1p_total_row_count`** (z-score reference):
  `roll_mean_log1p_total_w7`, `roll_mean_log1p_total_w14`,
  `roll_mean_log1p_total_w30`
- **trailing rolling standard deviation of `log1p_total_row_count`**
  (z-score reference): `roll_std_log1p_total_w7`,
  `roll_std_log1p_total_w14`, `roll_std_log1p_total_w30`
- trailing rolling **z-score of `log1p_total_row_count`** —
  `roll_z_log1p_total_w7`, `roll_z_log1p_total_w14`, `roll_z_log1p_total_w30`,
  computed as `(log1p_total_row_count − roll_mean_log1p_total_wN) /
  roll_std_log1p_total_wN` for the **same `W`** (so the reference
  distribution is the trailing rolling mean/std **of
  `log1p_total_row_count`**, **not** of raw `total_row_count`); NaN-safe
  (emit NaN where the trailing std is 0 or undefined; flag via
  `is_rolling_window_warmup`)
- trailing rolling percentile/rank of `log1p_total_row_count`:
  `roll_pct_log1p_total_w30`, `roll_pct_log1p_total_w90`,
  `roll_pct_log1p_total_w365` (rank within trailing window; ties broken by
  average rank)
- day-over-day change in `log1p_total_row_count`:
  `delta_log1p_total_dod`
- trailing mean of offset_0 share: `roll_mean_offset_0_share_w30`
- trailing standard deviation of offset_0 share:
  `roll_std_offset_0_share_w30`
- trailing **z-score of offset_0 share**: `roll_z_offset_0_share_w30` =
  `(offset_0_share_of_total − roll_mean_offset_0_share_w30) /
  roll_std_offset_0_share_w30`, NaN-safe (emit NaN where the trailing std
  is 0 or undefined; flag via `is_rolling_window_warmup`)

### 6.7 Spike features (thresholds locked)

Binary spike flags keyed off the pre-registered rolling z-score of
`log1p_total_row_count`. **Thresholds are LOCKED HERE and may not be tuned
after seeing data**:

- `spike_w7_z_ge_2` = `roll_z_log1p_total_w7 ≥ 2.0`
- `spike_w7_z_ge_3` = `roll_z_log1p_total_w7 ≥ 3.0`
- `spike_w14_z_ge_2` = `roll_z_log1p_total_w14 ≥ 2.0`
- `spike_w14_z_ge_3` = `roll_z_log1p_total_w14 ≥ 3.0`
- `spike_w30_z_ge_2` = `roll_z_log1p_total_w30 ≥ 2.0`
- `spike_w30_z_ge_3` = `roll_z_log1p_total_w30 ≥ 3.0`

All spike flags emit `False` (not NaN) during warmup and where the rolling std
is 0 or undefined; the row is additionally flagged via `is_rolling_window_warmup`
so consumers can exclude warmup rows from spike-tabulation if desired.

### 6.8 Edge / domain flags

- `is_domain_start_edge` — true for the first 7 civil dates in the domain
  (`2013-04-01` … `2013-04-07`)
- `is_rolling_window_warmup` — true for any civil date that does not have a
  fully populated trailing window of the **longest locked rolling feature**
  (which is the 365-day percentile feature `roll_pct_log1p_total_w365`).
  Operationally `is_rolling_window_warmup ⇔ has_full_365d_history = False`.
  This is the **broad** warmup flag: it is `True` whenever **any** locked
  rolling feature lacks a full window. Granular per-window flags
  (`has_full_7d_history`, `has_full_30d_history`, `has_full_365d_history`)
  remain available for consumers that need finer-grained warmup logic per
  feature family.
- `has_full_7d_history` — true iff at least 7 trailing civil dates are
  available (inclusive of current)
- `has_full_30d_history` — true iff at least 30 trailing civil dates are
  available (inclusive of current)
- `has_full_365d_history` — true iff at least 365 trailing civil dates are
  available (inclusive of current)

## 7. Rolling-window discipline

- All rolling features use **past/current GDELT rows only**; no future rows.
- No market data is read or referenced.
- Rows are ordered **deterministically by `civil_date` ascending** before any
  rolling computation.
- **Current-row-inclusive trailing convention (locked):** every locked rolling
  window covers the **current row and the prior W−1 rows** (window of length
  `W` over civil-date ascending). This convention is intentional and locked
  here; changing to strictly-prior windows would require a new design memo.
  Spike flags (§6.7) are therefore "large relative to the **current-inclusive
  trailing GDELT distribution**," not a strictly-prior-only surprise measure.
- Warmup rows (those with `is_rolling_window_warmup = True`) are **flagged, not
  silently dropped**. A separately pre-registered exclusion policy is required
  before dropping warmup rows downstream.
- **Represented-only and KSG rolling-inclusion policy (LOCKED, no future
  tuning in Step 2):** represented-only rows (§8) and KSG rows (§9) **remain
  present** in the feature table **and** their recorded `total_row_count`
  and offset values are **included verbatim** in rolling-window computations
  for all affected dates. **No imputation, no dropping, no masking, and no
  exclusion** is applied inside Step 2 rolling statistics. This choice is
  deliberate, in service of **deterministic substrate-faithful feature
  generation**: the rolling features describe the actual recorded substrate
  exactly. The status flags (`represented_only`, `is_known_substrate_gap`,
  `terminal_status`, `coverage_quality_flag`, `coverage_completeness`,
  `documented_exception_label`, `is_rolling_window_warmup`,
  `has_full_7d_history`, `has_full_30d_history`, `has_full_365d_history`)
  are preserved on every row so any later analysis may pre-register an
  exclusion or sensitivity treatment. **Any future exclusion** of
  represented-only or KSG rows from rolling-window reference distributions
  requires a **separate design memo** before implementation; ad-hoc
  exclusion inside Step 2 is forbidden.
- **`offset_plus_1` non-look-ahead clarification:** the seven offset columns
  in the merged substrate — including `rows_from_offset_plus_1` — are
  treated here as **components of the finalized per-`civil_date` substrate
  row** (the merge writer already assembled them across nominal-file
  boundaries). Their use in Step 2 features computed for that same
  `civil_date` does **not** constitute look-ahead in the Step 2
  `civil_date` ordering used by the rolling-window discipline above; they
  are not "future rows" — they are columns of the current row.
  **Publication-lag / causal availability** of `offset_plus_1` (and of the
  represented-only-supporting neighbor offsets in §8) is a **later
  market-data-join design issue** and must be **separately pre-registered**
  before any market-conditioned analysis. This memo does not authorize a
  market-conditioning decision either way; it only fixes the Step 2 feature
  semantics relative to the GDELT-only civil-date axis.

## 8. Represented-only inclusion policy

**Locked policy (no future tuning):**

- **Include** the `2022-11-10` represented-only row in `step2_daily_features.csv`.
- Preserve `represented_only = True` exactly as in the merged substrate.
- Preserve the documented-exception label
  `UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY` exactly.
- **Do not** impute `rows_from_offset_0` (it must remain `0`).
- Use the recorded `total_row_count = 1267` exactly; the neighbor-offset
  cross-check `1267 = 91 + 849 + 327` must reconcile.
- Keep the row available for downstream sensitivity analysis.
- Any future market-data join must either include this row with the
  represented-only flag preserved, or **separately pre-register** a sensitivity
  analysis. Silent dropping in the market-data step is forbidden.

**Explicitly rejected** (any implementation that does any of these must
hard-stop):
- silently dropping it;
- treating it as raw / raw-processed;
- treating it as recovered;
- treating it as KSG / no-data gap;
- treating it as missing / invisible / ordinary completion;
- imputing/back-filling `rows_from_offset_0`.

## 9. KSG policy

**Locked policy:**

- **Keep** the four KSG rows (`2014-01-23`, `2014-01-24`, `2014-01-25`,
  `2014-03-19`) in `step2_daily_features.csv`.
- Preserve their KSG identity: `is_known_substrate_gap = True`,
  `terminal_status = known_no_data_gap`, `represented_only = False`,
  `documented_exception_label = ""`.
- The literal string `known_no_data_gap` is an **internal Step 2
  terminal-status enum value** carried per-row from the canonical mapping
  in §5, applied **only** to the four pinned KSG dates above. It is **not**
  an affirmative F1–F6 artifact claim about chunk_2022 or the
  documented-exception pathway, and it does not constitute documentation
  of an upstream "no-data gap" for any non-KSG date. **Do not** label
  `2022-11-10` (or any date outside the four pinned KSG dates) with
  `terminal_status = known_no_data_gap`, with `is_known_substrate_gap =
  True`, or as a "no-data gap" anywhere in Step 2 outputs or prose;
  `2022-11-10` is the labeled-complete documented exception, not a KSG.
- **Do not** collapse KSG into documented exception or any other class.
- **Do not** silently amend `KNOWN_SUBSTRATE_GAPS`.
- Any later exclusion or sensitivity treatment must be **separately
  pre-registered** in a follow-on design memo, not decided ad hoc.

## 10. Documented-exception propagation

The future implementation must **fail closed** if **any** of the following
holds [I]:

- `2022-11-10` is missing from `step2_daily_features.csv`;
- `2022-11-10` appears more than once;
- its `documented_exception_label` is missing or differs from
  `UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY`;
- `represented_only` is not `True` for that row;
- `total_row_count` is not exactly `1267`;
- `rows_from_offset_0` is not exactly `0`;
- `91 + 849 + 327 ≠ 1267` for the cross-check;
- it is reclassified as raw, recovered, KSG, missing, or ordinary completion;
- the documented-exception provenance is missing from `step2_metadata.json`
  (chunk_id, date, raw_filename, label, catalog_md5, catalog_filesize_bytes,
  http_status, raw_object_parsed, rows_recovered, no_data_gap, recovered,
  known_substrate_gap_amended, representation_artifact +
  representation_artifact_sha256, contract + contract_sha256,
  source_chunk_output_dir, source_chunk_metadata_sha256).

## 11. Pre-execution conformance gate

A pre-execution conformance gate must run before any Step 2 execution and
must verify [I]:

- **input pinning**: the three input artifact SHAs and the
  `build_manifest_digest` match the pinned values in §2; the directory path
  matches; fail closed otherwise;
- **row count**: `step2_daily_features.csv` has exactly `3562` data rows;
- **date domain**: first `civil_date` = `2013-04-01`; last `civil_date` =
  `2022-12-31`; no duplicate `civil_date`;
- **seven-offset-sum invariant**: every row satisfies
  `total_row_count = Σ seven offset columns`;
- **documented-exception exact checks**: the §10 hard-stop set;
- **KSG exact checks**: §9 hard-stop set (four KSG dates present, with the
  exact field values);
- **feature schema exact match**: the output column set matches the locked
  schema in §6 exactly — same names, same order, no extras, no omissions;
- **no market-data columns** present anywhere in `step2_daily_features.csv` or
  `step2_metadata.json`;
- **no outcome columns** present (no forward returns, no target labels, no
  PnL);
- **no post-2022 rows** anywhere (`civil_date > 2022-12-31` must be absent);
- **F1–F6 forbidden-claim audit** clean on `step2_summary.md` and on metadata
  prose fields (§13);
- **boundary declarations** in `step2_metadata.json` are all `true`:
  `no_step_2_market_join`, `no_market_data`, `no_instrument`,
  `no_gdelt_fetch`, `no_bigquery`, `no_row_export`,
  `no_known_substrate_gaps_amendment`.

A separate, pre-execution review report must explicitly state PASS for each
of the above before execution authorization is requested.

## 12. Forbidden features and firewalls

The future implementation **must not** include or reference any of the
following [I]:

- market returns (any horizon)
- market direction (up/down/sign labels)
- prices for SPY, GLD, TLT, EFA, EEM, or any other instrument
- volatility outcomes (realized, implied, or any market-based vol)
- trading signals or rules
- instrument labels or tickers
- forward returns (any horizon)
- future GDELT counts (no look-ahead within the GDELT substrate either)
- any target/outcome variable
- any post-`2022-12-31` data
- any data acquired by GDELT fetch, BigQuery query, or row export

Market-data join and instrument construction are **separate, later, separately
authorized** phases. They must not be folded into Step 2 implementation or
execution.

## 13. F1–F6 artifact audit

Future `step2_summary.md` and the prose/string fields of `step2_metadata.json`
must contain **no affirmative claim** matching any of the six artifact-level
forbidden literals (canonical source: the `forbidden_claims` array in
`representations/lane2_gdelt1/chunk_2022_documented_exception_20221110/representation.json`):

- `raw 365/365`
- `ordinary completion`
- `no-data gap`
- `recovered day`
- `raw-processed day`
- `exact runner-output gate from BigQuery count 105041`

These literals are allowed **only inside meta-linguistic prohibition contexts**
(e.g., a "must not collapse into …" clause) and **only inside a clearly-marked
documentation field**. Any affirmative use about the substrate, the
documented-exception pathway, or any feature is forbidden. Step 2 must never
make a raw-complete-10/10 claim; the substrate is 10/10 terminal-status (9
raw-complete + 1 labeled-complete documented-exception).

## 14. Future implementation requirements

Future Step 2 implementation must [I]:

- be **deterministic** — given the same pinned merged substrate input, the
  three output artifact SHA-256s must be identical across runs;
- be **localized** — the implementation should live in a new, narrowly-scoped
  module (preferably a separate script under `scripts/` or a focused function
  within an existing module), not bolted into the merge runner;
- **include tests before execution** — a focused test file (e.g.,
  `tests/test_lane2_gdelt1_step2_features.py`) must cover the feature schema,
  the represented-only and KSG policies, the documented-exception propagation,
  the seven-offset-sum invariant on synthetic fixtures, the rolling-window
  warmup flags, the spike-threshold lock, and the F1–F6 audit on a generated
  summary;
- **write metadata** that records all input pins (directory + three SHAs +
  `build_manifest_digest`), the exact locked feature schema, the
  represented-only inclusion policy (§8), the KSG policy (§9), the
  documented-exception provenance (inherited verbatim), the pre-execution
  conformance verdict, the implementation version, and the boundary
  declarations (§11/§12);
- **not execute automatically** during implementation — implementation
  produces code + tests + a default in-memory or dry-run path; an actual write
  requires a dedicated `--write-step2-output` CLI flag (analogous to the
  merge's `--write-merge-output`);
- **require separate execution authorization** — a future prompt must
  explicitly authorize the one-shot Step 2 execution, and the conformance gate
  in §11 must PASS before that authorization is requested.

The implementation must **not** reuse `FULL_BUILD_AUTHORIZED` (it is the
live-fetch guard; Step 2 is offline) and must **not** reuse the merge's
`--write-merge-output` flag (that flag is scoped to the merge writer).

## 15. Verdict map

A **future implementation conformance review** — i.e., a review of the future
Step 2 code + tests against this design memo (not a review of this memo
itself) — may produce one of these verdicts:

- `PASS — STEP 2 IMPLEMENTATION CONFORMS TO DESIGN MEMO`
- `BLOCKED — MARKET DATA SMUGGLED INTO FEATURE SET`
- `BLOCKED — DOCUMENTED-EXCEPTION PROPAGATION INCOMPLETE`
- `BLOCKED — REPRESENTED-ONLY POLICY NOT LOCKED`
- `BLOCKED — KSG POLICY NOT LOCKED`
- `BLOCKED — CONFORMANCE GATE INCOMPLETE`
- `BLOCKED — IMPLEMENTATION OR EXECUTION BOUNDARY CROSSED`

## 16. Recommendation

**RECOMMENDATION: REVIEW STEP 2 IMPLEMENTATION-DESIGN MEMO BEFORE ANY IMPLEMENTATION**
