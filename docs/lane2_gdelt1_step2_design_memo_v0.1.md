# Lane 2 GDELT1 — Step 2 Design Memo v0.1

Design-only memo. Governs how a future, separately authorized Step 2 may consume
the canonical merged daily-count substrate. It does **not** open Step 2.

Evidence legend: **[O]** observed git/fs · **[A]** artifact-derived (merged
`build_metadata.json` / `build_daily_counts.csv` / `build_summary.md`) ·
**[I]** design recommendation.

---

## 1. Purpose and non-authorization

This memo designs the Step 2 consumption path for the completed Lane 2 GDELT1
merged daily-count substrate and the firewalls that must hold before any Step 2
execution. It performs none of it.

- No Step 2 is opened or executed by this memo.
- No market data is accessed.
- No instrument is constructed.
- No code is changed; no result-output is written; no memory is written.
- No GDELT fetch, no BigQuery, no row export.
- Step 2 **implementation** and Step 2 **execution** each remain separately
  authorized future actions.

Distinct phases, not to be collapsed: **design (this memo) → Step 2
implementation design → implementation → pre-execution conformance gate →
execution authorization → execution**.

## 2. Canonical input substrate

The single canonical input is the merged daily-count substrate produced by the
authorized offline merge (HEAD = origin/main =
`fc98fc4617ecc10fc62489f75a53522c87a62daf`) [O][A]:

- directory: `results/lane2_gdelt1_full_daily_count_build/merged_20260529T175416Z/`
  (uncommitted result-output).
- `build_daily_counts.csv` SHA-256
  `84b6ac9f47888fea4bd5c9d448058db0e5c568e3aa194a0fc7d4d5c95704045e`
- `build_metadata.json` SHA-256
  `31ad8085d9df839f833d6af83cb4fdb24ad47c3ecef0bd44b4d730de682a08cf`
- `build_summary.md` SHA-256
  `7677bbaf3d84923209a8b0be64dd9d3f64ffe752ac56f4eb5ad65169bae86e97`
- `build_manifest_digest`
  `4b312183d9bb126169fc82c5b76008359778df18ee803527c567f7ade3a89650`

Substrate shape [A]: **3562 civil days** over `2013-04-01`..`2022-12-31`;
`build_daily_counts.csv` columns = `civil_date, total_row_count,
rows_from_offset_0, rows_from_offset_minus_1, rows_from_offset_minus_7,
rows_from_offset_minus_30, rows_from_offset_minus_365, rows_from_offset_minus_3650,
rows_from_offset_plus_1, t0_file_status, expected_contributing_files_count,
available_contributing_files_count, coverage_quality_flag, coverage_completeness,
represented_only, documented_exception_label`. `build_metadata.json` carries
`per_chunk`, `aggregate`, `documented_exceptions`, `retained_halt_history`,
`input_chunk_manifest_digests`, `build_manifest_digest`, `boundary_declarations`,
`merge_implementation_version`, `output_artifact_sha256s`, `merge_authorization`.

Substrate state: **10/10 terminal-status = 9 raw-complete + 1 labeled-complete
documented-exception** (chunk_2022). Aggregate partition closes
`3557 raw_processed + 1 documented_unavailable_data_confirmed + 0 recovered +
4 known_no_data_gap = 3562 terminal_status`. This substrate is **not raw-complete
10/10** and Step 2 must never describe it as such.

## 3. What Step 2 is allowed to design but not execute

Step 2's eventual purpose is to map the daily-count substrate toward
market/instrument analysis (e.g., attention-spike features conditioned on prior
market nervous state). In this design memo, Step 2 may be **designed** to:

- read the merged CSV + metadata as **read-only inputs** (by path + verified
  SHA-256 / `build_manifest_digest`);
- define a feature/representation layer over the per-civil-date counts;
- define how the documented-exception and KSG day classes are carried into any
  Step 2 feature rows.

Step 2 may **not**, in any turn until separately authorized: access market data,
construct an instrument, join price/return series, perform a market-calendar
alignment, fetch GDELT, query BigQuery, export rows, mutate result-output, or
declare any market finding.

## 4. Required propagation of documented-exception metadata

Before chunk_2022 (or any 2022-11-10-bearing row) is consumed, Step 2 must carry
the documented-exception metadata forward, sourced from
`build_metadata.json.documented_exceptions[0]` [A] (which already carries the full
§8 provenance): `chunk_id`, `date`, `raw_filename`, `label`
(`UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY`), `catalog_md5`,
`catalog_filesize_bytes`, `http_status`, `raw_object_parsed`, `rows_recovered`,
`no_data_gap`, `recovered`, `known_substrate_gap_amended`, `representation_artifact`
+ `representation_artifact_sha256`, `contract` + `contract_sha256`,
`source_chunk_output_dir`, `source_chunk_metadata_sha256`.

Rules [I]:
- Any Step 2 output that includes or derives from 2022-11-10 must inherit/inspect
  the label and must **fail closed** if the label is absent or altered.
- Step 2 must not collapse the documented exception into raw-processed, recovered,
  a KSG no-data gap, ordinary completion, or invisible/missing status.
- The label must propagate to every Step 2 artifact and aggregate that touches the
  date, mirroring the merge-gate firewall established for the substrate.

## 5. Handling of the `2022-11-10` represented-only row

In the merged substrate, the `2022-11-10` row has `rows_from_offset_0 = 0`,
`total_row_count = 1267` (represented purely via neighbor offsets;
1267 = 91 + 849 + 327), `represented_only = True`, and the documented-exception
label set [A]. Step 2 design rules [I]:

- treat `2022-11-10` as **represented-only**, not as an ordinary raw t0 day;
- do **not** synthesize/back-fill an offset-0 value for it;
- if Step 2 features depend on own-day (offset_0) counts, `2022-11-10` must be
  handled by an explicit, documented branch (e.g., flagged-missing-t0 /
  represented-only), never silently imputed;
- `represented_only` is **label-derived** — Step 2 must key represented-only
  status on the documented-exception label, not on `rows_from_offset_0 == 0`
  alone (KSG and ordinary low-volume days could also have small offset_0);
- the decision on whether represented-only days are included, excluded, or
  separately bucketed in any Step 2 feature must be **pre-registered** in the
  Step 2 implementation design, not made ad hoc.

## 6. Market-data firewall

No market data (prices, returns, volumes, calendars, instrument series) is read,
joined, or referenced in this memo or in any subsequent turn until a separate
explicit Step 2 market-data authorization. The merged substrate is GDELT
daily-count-only; it contains no market data. Any future market-data join is a
distinct, separately authorized step with its own preflight and conformance gate.
OOS / 2023+ sealing remains in force (the substrate domain ends `2022-12-31`).

## 7. Instrument-construction firewall

No instrument is constructed, parameterized, or backtested by this memo or any
subsequent turn until separate explicit authorization. Step 2 design may name the
*intended* analysis target abstractly, but must not specify, tune, or execute an
instrument, threshold, signal, or trading rule. Spike-threshold tuning,
negative-control selection, and any return/PnL logic remain firewalled.

## 8. Proposed Step 2 artifact set

A future Step 2 implementation should produce **read-derived, offline** artifacts
[I], under a fresh `results/lane2_gdelt1_step2_*/<UTC-ts>Z/` directory
(untracked result-output, mirroring the chunk/merge convention):

| # | artifact | role |
|---|---|---|
| 1 | `step2_daily_features.csv` | per-civil-date Step 2 feature rows derived from the merged counts, carrying `civil_date`, the chosen feature columns, plus `represented_only` and `documented_exception_label` passthrough |
| 2 | `step2_metadata.json` | provenance: input merged-substrate path + `build_manifest_digest` + the three input SHA-256s; documented-exception block (inherited from `build_metadata.json.documented_exceptions`); per-day-class counts; boundary declarations; Step 2 implementation version |
| 3 | `step2_summary.md` | positive-status summary: substrate = 10/10 terminal-status (not raw-complete 10/10); day-class table; documented-exception note; explicit "no market data / no instrument" boundary statement |

Each artifact is checksummed; `step2_metadata.json` must reference the input
`build_manifest_digest` so Step 2 outputs are pinned to the exact merged substrate.

## 9. Proposed schema for any future Step 2 outputs

`step2_daily_features.csv` [I]: `civil_date` (3562 rows, `2013-04-01`..`2022-12-31`,
no duplicates); a small, pre-registered set of feature columns derived only from
the seven offset counts / `total_row_count` / coverage fields (e.g., normalized
attention level, coverage-adjusted count) — **the specific features are deferred
to the Step 2 implementation design, not fixed here**; passthrough `t0_file_status`,
`coverage_quality_flag`, `coverage_completeness`, `represented_only`,
`documented_exception_label`.

`step2_metadata.json` [I]: `input_substrate` `{dir, build_manifest_digest,
build_daily_counts_sha256, build_metadata_sha256, build_summary_sha256}`;
`documented_exceptions` (inherited verbatim); `day_class_counts`
`{raw_t0_present, represented_only, ksg, ...}` that must reconcile to 3562;
`boundary_declarations` `{no_step_2_market_join, no_market_data, no_instrument,
no_gdelt_fetch, no_bigquery, no_row_export, no_known_substrate_gaps_amendment}`
all true at the design/implementation stage; `step2_implementation_version`.

## 10. Validation / conformance gates before any Step 2 execution

A future Step 2 pre-execution conformance gate must verify [I]:
- input pinning: the merged substrate SHAs + `build_manifest_digest` match the
  canonical values in §2 (fail closed otherwise);
- row domain: 3562 civil days, `2013-04-01`..`2022-12-31`, no duplicates;
- documented-exception propagation: the label + §8 provenance are carried into
  Step 2 outputs; `2022-11-10` is flagged represented-only and not imputed;
- KSG distinctness: the four 2014 KSG dates remain a separate class from the
  documented exception, never reclassified;
- day-class reconciliation: per-class counts sum to 3562;
- no raw-complete-10/10 claim anywhere in Step 2 prose/metadata;
- F1–F6 artifact-level forbidden-claim audit (canonical mapping from
  `representations/lane2_gdelt1/chunk_2022_documented_exception_20221110/representation.json`):
  no affirmative forbidden claim in Step 2 summary/metadata prose;
- firewall declarations: no market data, no instrument, no GDELT/BigQuery/row
  export, no `KNOWN_SUBSTRATE_GAPS` amendment.

## 11. Risks and ambiguity list

- **Feature selection is unspecified** [I]: the exact Step 2 feature set is a
  deliberate downstream decision; this memo fixes the consumption discipline, not
  the features. Not a blocker for design; must be pre-registered before
  implementation.
- **Represented-only inclusion policy** must be pre-registered (include / exclude
  / separate bucket); silent inclusion or exclusion is a risk.
- **Coverage-edge days**: the lookback/lookahead offset structure means early-2013
  and year-boundary days have partial coverage flags; Step 2 must use the existing
  `coverage_quality_flag` / `coverage_completeness`, not recompute coverage.
- **Uncommitted input**: the merged substrate is uncommitted result-output; a
  future Step 2 run must pin it by SHA/digest, and ideally follow (or wait for) a
  merged-output disclosure/commit so the input is durably referenceable.
- **Market-data boundary** is the highest-risk firewall: market join must be its
  own separately authorized step, never folded into Step 2 feature derivation.

No design point is impossible or materially ambiguous to the degree that blocks
*designing* Step 2 consumption; the open items are downstream pre-registration
decisions, not missing inputs.

## 12. Recommendation and next frontier

**`STEP 2 IMPLEMENTATION DESIGN REQUIRED NEXT`**

Justification [I]: the canonical merged substrate is complete, conformant, and
fully provenanced (incl. the documented-exception §8 metadata and the
represented-only `2022-11-10` row), so Step 2 consumption is well-defined at the
design level. The next prompt should be a **separately-authorized Step 2
implementation design** that pre-registers the concrete feature set, the
represented-only inclusion policy, and the §8/§10 propagation + conformance gate —
**before** any implementation, and long before any market-data join or instrument
construction. Step 2 is not opened; no market data is touched; the substrate is
10/10 terminal-status (9 raw-complete + 1 labeled-complete documented-exception),
not raw-complete 10/10.
