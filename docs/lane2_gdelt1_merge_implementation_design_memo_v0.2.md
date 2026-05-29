# Lane 2 GDELT1 — Merge-Implementation Design Memo v0.2

Ordinal 122. Design memo only. Governs a later, separately authorized
merge-implementation prompt. Required by the committed merge-authorization design
memo (`docs/lane2_gdelt1_merge_authorization_design_memo_v0.1.md`, SHA-256
`9a580a3cd8773e7b44c3cbbf293f1dca5dde1afb4abdb63d783347634e93d145`), which
concluded `MERGE IMPLEMENTATION DESIGN REQUIRED BEFORE AUTHORIZATION`.

**v0.2 cleanup (this revision):** narrow corrections from the independent
`PASS WITH NARROW CLEANUP` review — (A) `represented_only` is now label-derived and
explicitly excludes KSG dates (§6); (B) `total_row_count` is formula-pinned as the
seven-offset sum with a hard-stop (§6); (C) all ten expected terminal-status chunk
counts and the aggregate partition are pinned (§9). No design change beyond these
three; all firewalls preserved. (File path retains the `v0.1` slug; the artifact is
uncommitted and unreferenced, so an in-place title bump is mechanically safest.)

Evidence legend: **[O]** observed git/fs · **[S]** static source inspection
(runner `scripts/run_lane2_gdelt1_full_daily_count_build.py`, blob
`799b6d85b29be1ebe2df47db288e4f9eac6b038f`) · **[A]** artifact-derived
(chunk metadata / contract / representation) · **[I]** design recommendation.

---

## 1. Purpose and non-authorization statement

This memo designs the future offline merge implementation. It does not implement,
authorize, or execute the merge.

- No code is changed by this memo.
- No merge occurs.
- No Step 2 (instrument construction / market-data join) opens.
- No market data is touched.
- Merge **implementation** remains separately authorized (a future prompt).
- Merge **execution** remains separately authorized **after** implementation and
  a conformance gate pass.

Distinct phases, not to be collapsed: **design (this memo) → implementation →
conformance gate → execution authorization → execution**.

## 2. Inputs and canonical substrate state

The merge implementation must consume the ordinal-116 canonical substrate [A]:

- **10/10 terminal-status chunks**; **9 raw-complete** (2013_partial, 2014–2021)
  + **1 labeled-complete documented-exception** (chunk_2022).
- chunk_2022 is **not raw-complete**: 365 terminal-status days = 364 raw_processed
  + 1 documented-unavailable/data-confirmed/represented-only day (`2022-11-10`).
- chunk_2013 is the partial regime-start year (window 2013-04-01..12-31):
  275 expected = 275 actual.
- chunk_2014: 4 known-no-data-gap days from the global `KNOWN_SUBSTRATE_GAPS`
  constant (the four 2014 dates); expected_file_count 361 = 365 − 4.
- chunk_2022 `known_no_data_gap_days` = 0.
- All chunk result inputs are **uncommitted result-output artifacts** at this
  stage (the `results/lane2_gdelt1_full_daily_count_build/` tree is untracked).

Canonical input directories (one per chunk; halted/forensic dirs excluded):
`chunk_2013_partial_20260524T135157Z`, `chunk_2014_20260524T150055Z`,
`chunk_2015_20260524T163556Z`, `chunk_2016_20260524T194435Z`,
`chunk_2017_20260524T231143Z`, `chunk_2018_20260525T025641Z`,
`chunk_2019_20260526T130910Z`, `chunk_2020_20260528T080812Z`,
`chunk_2021_20260528T110740Z`, `chunk_2022_20260528T234738Z`.

## 3. Existing merge machinery inventory

Static inspection of the runner (blob `799b6d85b29be1ebe2df47db288e4f9eac6b038f`) [S]:

- **`merge_chunks(chunk_dirs, repo_root)`** — lines ~2470–2610. Offline; no GDELT
  contact. Verifies chunk set against `CHUNK_IDS`; loads the recognized-list
  capture; verifies per-chunk `chunk_manifest_digest` against
  `build_all_chunk_manifests`; checks cross-chunk URL uniqueness; asserts
  union == recognized-list fetch set; sums per-(civil_date, offset) contributions;
  builds per-civil-date rows with coverage flags recomputed from
  `daily_set`/`gaps_set`; returns a dict `{daily_count_rows, aggregate_metrics,
  per_chunk_summary}`.
- **Helpers**: `load_chunk_contributions` (~2419–2455, reads `chunk_contributions.csv`
  into `(iso, offset)->count`); `load_chunk_metadata` (~2458–2467, reads
  `chunk_metadata.json`); `build_all_chunk_manifests` (~1717); `chunk_manifest_digest`
  (~1722); `assert_chunk_manifests_partition` (~1738); `CHUNK_IDS` (~1627),
  `EXPECTED_CHUNK_COUNTS` (~1640).
- **CLI**: `--merge` (~2662) and repeatable `--merge-input CHUNK_ID=DIR` (~2671),
  parsed by `_parse_merge_inputs` (~2683); dispatched in `main` (~2702). Mutually
  exclusive with `--chunk-id`.
- **Does it write canonical output?** **No.** `main` prints *"Merge complete
  (in-memory only; CLI does not write canonical artifacts in this implementation
  turn)."* `merge_chunks` returns a dict and the caller discards it.
- **Does it read documented-exception metadata?** **No.** `merge_chunks` reads only
  `chunk_manifest_digest`, `expected_file_count`, `actual_completed_file_count`
  from each chunk's metadata. It never reads `documented_exception_diagnostic` or
  `per_file_manifest`.
- **Does it understand `documented_exception_diagnostic`?** **No.**
- **Does it propagate documented-exception labels?** **No.** `per_chunk_summary`
  carries only counts + digest; rows recompute coverage generically, so 2022-11-10
  would surface as a generic coverage shortfall (offset_0 = 0) without the label.
- **Structural guards present**: `ChunkManifestError` (class ~1675) on missing
  chunk / digest mismatch / duplicate URL / union mismatch; `FullBuildBoundaryBreach`
  (class ~262) on invalid coverage flag. No merge-specific *authorization* guard;
  merge is offline ("no guard flip required").
- **Limitations blocking merge authorization**: (a) writes no canonical artifact;
  (b) documented-exception-blind. Both must be closed before merge execution.

This **confirms** the prior memo's finding (present-but-blind, writes nothing).
No contradiction found.

## 4. Implementation objective

Extend the offline merge machinery so it produces canonical merged Lane 2 GDELT1
daily-count artifacts from the 10 terminal-status chunk outputs while preserving
documented-exception metadata and per-category distinctions.

Explicitly, the merge implementation:
- is **offline**; must **not** fetch GDELT; must **not** use BigQuery; must **not**
  access market data; must **not** open Step 2; must **not** amend
  `KNOWN_SUBSTRATE_GAPS`.
- separates **compute** (`merge_chunks`, already present) from **write** (new) and
  **documented-exception carry-through** (new).

## 5. Proposed canonical merge output artifact set

Output directory convention [I]: `results/lane2_gdelt1_full_daily_count_build/merged_<UTC-ISO-compact>Z/`
(mirrors the per-chunk `chunk_<id>_<ts>Z/` convention). **Untracked result-output**
(like the chunk outputs), surfaced by checksum in the run report; **not committed**
by the merge run itself (a later, separately authorized step may commit/disclose).

| # | artifact | filename | tracked? | committed? |
|---|---|---|---|---|
| 1 | merged daily-count CSV | `build_daily_counts.csv` | untracked | result-output |
| 2 | build metadata JSON | `build_metadata.json` | untracked | result-output |
| 3 | build summary Markdown | `build_summary.md` | untracked | result-output |
| 4 | manifest / digest | **embedded** `build_manifest` section inside `build_metadata.json` (a `build_manifest_digest` field over the ordered 10 input `chunk_manifest_digest`s + the three output-artifact SHA-256s) | untracked | result-output |

Each artifact: required fields per §6/§7/§11; SHA-256 of each output captured in the
run report and cross-listed in `build_metadata.json`. All four reference the 10 input
chunk directories by path + each chunk's `chunk_metadata.json` SHA-256 +
`chunk_manifest_digest`. Filenames are chosen to avoid collision with per-chunk
names (`chunk_*`) and to read as build-level (`build_*`); justification: keeps a
clean grep boundary between chunk-step and merge-step artifacts.

## 6. Merged daily-count CSV schema

`build_daily_counts.csv`, one row per civil date in `[2013-04-01, 2022-12-31]`
(reusing `civil_date_domain()`), columns [I]:

- `civil_date` (ISO);
- `total_row_count` = `rows_from_offset_0 + rows_from_offset_minus_1 +
  rows_from_offset_minus_7 + rows_from_offset_minus_30 + rows_from_offset_minus_365
  + rows_from_offset_minus_3650 + rows_from_offset_plus_1` (the seven-offset sum;
  it is **not** offset_0-only). For `2022-11-10`, `rows_from_offset_0 = 0` but
  `total_row_count` includes the neighbor-offset contributions. The merge must
  **hard-stop** if `total_row_count` does not equal the sum of the seven offset
  columns for every row;
- per-offset columns `rows_from_offset_0`, `_minus_1`, `_minus_7`, `_minus_30`,
  `_minus_365`, `_minus_3650`, `_plus_1` (retain the existing offset taxonomy);
- `t0_file_status` (reuse runner's `t0_file_status`);
- `expected_contributing_files_count`, `available_contributing_files_count`,
  `coverage_quality_flag`, `coverage_completeness` (reuse merge-time coverage);
- **new** `represented_only` (bool): true **iff** `documented_exception_label` is
  non-empty for that civil date. It is **not** a generic "own t0 absent + neighbor
  contributions" classifier and **not** keyed on absence of offset_0 alone. KSG
  dates — including the four 2014 `KNOWN_SUBSTRATE_GAPS` dates — must have
  `represented_only = false` even if neighbor-offset contributions exist; KSG days
  remain KSG only and are never reclassified as represented-only. The
  `documented_exception_label` is the **sole** row-level discriminator for
  represented-only status; `represented_only` is a convenience flag derived from
  that label, not a generic coverage-gap classifier. True only for `2022-11-10`
  (label non-empty; `rows_from_offset_0 = 0`, neighbors > 0);
- **new** `documented_exception_label` (string, empty unless the civil date is a
  documented-exception date) = `UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY`
  for `2022-11-10`.

Rules: **preserve** rows with zero own-day raw count but nonzero neighbor
contributions (do not drop `2022-11-10`); do **not** synthesize/back-fill an
offset_0 value. **No deduplication** is required at chunk boundaries — chunks
partition the daily fetch set by nominal file date (`merge_chunks` already asserts
disjoint URL partition + union == fetch set), so each (civil_date, offset)
contribution has exactly one source chunk; cross-year neighbor offsets summing into
one civil_date is expected and additive, validated by the union/partition asserts.
chunk_2013 partial-year days (pre-2013-04-01 simply absent from the domain start)
and the four 2014 KSG days are handled by the existing `coverage_for_date(d,
daily_set, gaps_set)` (KSG ∈ `gaps_set`; not raw-processed, not documented
exception). Source-chunk provenance need not be a per-row column (it is derivable
from the manifest partition); if added, it is informational only.

## 7. Build metadata JSON schema

`build_metadata.json` must preserve [I]:

- `per_chunk[]`: `chunk_id`, `status_class`
  (`raw_complete` | `labeled_complete_documented_exception`), `canonical_output_dir`,
  `chunk_metadata_sha256`, `chunk_summary_sha256`, `chunk_contributions_sha256`,
  `chunk_manifest_digest`, `expected_calendar_days`, `raw_processed_days`,
  `documented_unavailable_data_confirmed_days`, `recovered_days`,
  `known_no_data_gap_days`, `terminal_status_days`, `terminal_status_complete`;
- `aggregate`: summed `raw_processed_days`, `documented_unavailable_data_confirmed_days`,
  `recovered_days`, `known_no_data_gap_days`, `terminal_status_days`,
  `total_in_window_rows`, `civil_days_in_output_domain`, `chunks_merged`;
- `documented_exceptions[]`: the §8 entry/entries;
- `retained_halt_history[]`: the non-canonical halted dirs
  (`chunk_2022_20260528T121150Z`, `chunk_2020_20260526T164747Z`, and
  `archive/halted_attempts/.../chunk_2019_20260525T192552Z`) with their
  `halt_diagnostic.json` SHA-256s — recorded, excluded from inputs;
- `input_chunk_manifest_digests` (ordered);
- `build_manifest_digest` (§5 item 4);
- `merge_implementation_version` (e.g. `v0.1`);
- `merge_authorization` (mechanism + that execution was separately authorized;
  §12);
- `boundary_declarations`: `no_step_2`, `no_market_data`, `no_gdelt_fetch`,
  `no_bigquery`, `no_row_export`, `no_known_substrate_gaps_amendment` — all true.

For the 9 raw-complete chunks the category counts are derived
(`expected_calendar_days = expected_file_count + in-window KSG`;
`raw_processed_days = actual_completed_file_count`; documented/recovered = 0); for
chunk_2022 they are read directly from its `documented_exception_diagnostic` [A].

## 8. Documented-exception representation in merged metadata

`documented_exceptions[0]` must carry exactly [A]:

- `label` = `UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY`
- `date` = `2022-11-10`
- `raw_filename` = `20221110.export.CSV.zip`
- `catalog_md5` = `91e15516016f986e5b8a08712e1de95a`
- `catalog_filesize_bytes` = `6714105`
- `raw_object_parsed` = False; `rows_recovered` = False; `http_status` = 404;
  `no_data_gap` = False; `recovered` = False; `known_substrate_gap_amended` = False
- `representation_artifact` = `representations/lane2_gdelt1/chunk_2022_documented_exception_20221110/representation.json`
  + its SHA-256 `91276597f4f3882d15133e32ec2d845badd244f7c89e706d06482a9d729c4ee3`
- `contract` = `configs/lane2_gdelt1_documented_exceptions.json` + its SHA-256
  `afee1c0d1e0e1d73fbe1ef45161deba4d174a4903e4b90093d00ac00472dda97`
- `source_chunk_output_dir` = `chunk_2022_20260528T234738Z` + its
  `chunk_metadata.json` SHA-256 `e986e217d1906aa3e7fbe3bf412add975738bf10fba8334b704440b9d3184de1`

This entry must **not** be collapsed into raw-processed, recovered, a
`KNOWN_SUBSTRATE_GAPS` no-data gap, ordinary raw completion, or an
invisible/missing status. The implementation must read it from chunk_2022's
`documented_exception_diagnostic` / `per_file_manifest` and the contract, and
**fail closed** if the chunk_2022 label/date/md5/size do not match the contract's
exact scope quintuple.

## 9. Category-count coherence rules

Hard-stop checks (raise `ChunkManifestError`-class on failure) [I]:

- per chunk: `raw_processed + documented_unavailable + recovered + known_no_data_gap
  = terminal_status_days`;
- per chunk: `terminal_status_days = expected_calendar_days` (documented-exception
  and KSG handling shift raw-vs-terminal categories but never terminal
  completeness);
- **pinned per-chunk expected terminal-status counts (all ten):**
  - chunk_2013_partial: **275** terminal-status days (partial regime-start year);
  - chunk_2014: **361 raw + 4 KSG = 365** terminal-status days;
  - chunk_2015: **365** terminal-status days;
  - chunk_2016: **366** terminal-status days (leap year);
  - chunk_2017: **365** terminal-status days;
  - chunk_2018: **365** terminal-status days;
  - chunk_2019: **365** terminal-status days;
  - chunk_2020: **366** terminal-status days (leap year);
  - chunk_2021: **365** terminal-status days;
  - chunk_2022: **364 raw + 1 documented = 365** terminal-status days;
- **pinned aggregate:** aggregate terminal-status days = **3562**; aggregate
  category partition = **3557 raw + 1 documented + 0 recovered + 4 KSG = 3562**; the
  merged per-category sums across the 10 chunks must equal this partition;
- exactly **one** documented exception across all chunks, and it is
  chunk_2022 / `2022-11-10`.

Any coherence failure, any deviation from the pinned per-chunk or aggregate counts,
any second documented exception, or any documented-exception label on chunks
2013–2021 must **hard-stop** implementation/execution.

## 10. Artifact-level F1–F6 audit design

Canonical source: the `forbidden_claims` array in
`representations/lane2_gdelt1/chunk_2022_documented_exception_20221110/representation.json`
[A]. The prior discipline-level F1–F6 mnemonic is **historical shorthand**, not the
audit source. Canonical mapping (this is the designated literal zone):
**F1** = `raw 365/365` · **F2** = `ordinary completion` · **F3** = `no-data gap`
· **F4** = `recovered day` · **F5** = `raw-processed day` ·
**F6** = `exact runner-output gate from BigQuery count 105041`.

Merge-output audit [I]: scan `build_summary.md` and every prose/string field in
`build_metadata.json` (esp. documented-exception-pathway descriptions). **Block**
any affirmative claim matching the forbidden set; **allow** meta-linguistic
references only inside a clearly-marked canonical-mapping/documentation field if one
exists in the output. Output prose must use **positive-status** wording
("10/10 terminal-status", "labeled-complete documented-exception",
"represented-only", category-count equation `365 = 364 + 1`). Future tests must
assert F1–F6 cleanliness of the generated `build_summary.md` and metadata prose
(count-zero of each forbidden literal outside any documentation field).

## 11. Build summary Markdown requirements

`build_summary.md` must include [I]: substrate status = **10/10 terminal-status**;
**9 raw-complete + 1 labeled-complete documented-exception**; **no raw-complete
10/10 claim**; chunk_2022 documented-exception label; a category-count table
(per chunk + aggregate); a retained-halt-history note; no merge-authorization claim
beyond the executed merge itself; no Step 2 opening; no market-data access; no
BigQuery recovery; no `KNOWN_SUBSTRATE_GAPS` amendment.

Approved positive-status self-heal phrasing: "if a future separately authorized
rebuild replaces the documented-exception state, raw-path processing supersedes it;
until then the merged substrate carries the documented-exception label." Do not use
slash-count phrasing outside the §10 canonical-mapping zone.

## 12. Authorization posture for merge implementation and merge execution

Design [I]:

- **Do not** reuse `FULL_BUILD_AUTHORIZED` — it is the live-fetch guard; merge is
  offline. Conflating them is a category error.
- The binding risk for merge is **writing a canonical artifact**, not network
  access. Recommended posture: **(a)** implement the merge writer behind a single
  explicit **write-authorization CLI flag**, e.g. `--write-merge-output`
  (compute via `merge_chunks` stays unguarded and side-effect-free; only the
  *write* requires the flag); **(b)** keep the existing structural
  `ChunkManifestError`/`FullBuildBoundaryBreach` integrity guards; **(c)** gate
  execution behind a separately-authorized merge-execution prompt + the §15
  conformance gate. A full source+CLI+env triple-guard is **not** warranted for an
  offline writer; a single write flag + scoped prompt + conformance gate is
  proportionate.
- If a stronger posture is later desired, add a distinct module constant (e.g.
  `MERGE_BUILD_AUTHORIZED`, default False) — **never** the live-fetch guard — with
  its own enable/restore lifecycle and tests. This memo recommends the lighter
  single-flag posture and records the constant option as a fallback.

## 13. Implementation file-scope proposal

Least-invasive, runner-local extension [I]:

- `scripts/run_lane2_gdelt1_full_daily_count_build.py`: extend `merge_chunks` (or
  add a thin `merge_chunks_with_documented_exceptions`) to read each chunk's
  `documented_exception_diagnostic` and derive §7 per-chunk records; add a
  `write_merge_artifacts(result, out_dir)` writer; extend the `--merge` CLI branch
  to create the output dir and write the three artifacts when `--write-merge-output`
  is passed (otherwise retain the current in-memory-only behavior).
- `tests/test_lane2_gdelt1_full_daily_count_build.py` (and possibly a new
  `tests/test_lane2_gdelt1_merge_build.py`): add the §14 tests.
- No config/representation/docs change required for implementation.

A separate module is **not** justified: the merge already lives in the runner, the
helpers are there, and the offset/coverage/manifest logic is shared. Prefer a
localized extension over a refactor. Revisit only if the runner exceeds a
maintainability threshold.

## 14. Test plan

Future tests [I]: merge consumes all 10 canonical chunk outputs; rejects a missing
chunk; rejects an unexpected/ambiguous chunk id; rejects a halted-only directory as
canonical input; rejects an undocumented documented-exception label (and a
documented-exception label on chunks 2013–2021); carries chunk_2022's
documented-exception metadata exactly (label/date/md5/size/flags); fails closed on
contract-mismatch; preserves the 2014 KSG handling (361 raw + 4 KSG = 365);
preserves chunk_2013 partial-year classification (275); per-chunk and aggregate
category-count coherence; artifact-level F1–F6 audit on the generated
`build_summary.md`/metadata prose; raw-complete-10/10 claim absent; Step 2 remains
closed; no market-data access; no BigQuery recovery; deterministic output artifact
hashes / `build_manifest_digest` (independent of `--merge-input` order). Reuse the
existing merge tests (missing/unexpected/digest/canonical/clip/order/coverage/
parse-inputs) as the structural base; add the documented-exception + writer +
coherence + F1–F6 layers.

## 15. Merge-output conformance gate

Post-implementation, pre-execution-authorization gate [I] verifies: implementation
diff scope (runner + tests only, guard untouched); test coverage (§14 all pass);
canonical output schema (§5–§7); category-count coherence (§9); documented-exception
label propagation (§8); artifact-level F1–F6 cleanliness (§10); no Step 2 / market
data / BigQuery / GDELT fetch; no `KNOWN_SUBSTRATE_GAPS` amendment; the
write-authorization flag behaves (no write without it; clean write with it). Verdict
gates whether a merge-execution-authorization prompt may follow.

## 16. Execution lifecycle for future merge run

Future merge run [I]: **preflight** (HEAD/guard/runner-blob/contract/representation
SHAs; all 10 canonical dirs present + hashes match; halted dirs excluded);
**authorization** via the §12 write flag (and, if adopted, the
`MERGE_BUILD_AUTHORIZED` enable→run→restore lifecycle, mirroring the chunk-run
guard discipline); **exactly one** merge write to a fresh `merged_<ts>Z/` dir;
**no production fetch**; **artifact checksum capture** (the three output SHAs +
`build_manifest_digest`); **post-run conformance** (§15 re-run on the produced
artifacts); **no Step 2**; **no memory write until run closure** (a separate
closure turn records it).

## 17. Self-heal fallback

If the `2022-11-10` raw object becomes available in a future separately authorized
rebuild, raw-path processing may supersede the documented-exception state for that
date. Until such a rebuild replaces it, the merge implementation must carry the
documented-exception label from the completed chunk_2022 output.

## 18. Non-goals and firewalls

No merge in this memo; no Step 2; no market data; no GDELT fetch; no BigQuery
recovery; no manual row export; no `KNOWN_SUBSTRATE_GAPS` amendment; no OOS /
market-data boundary; no claim of raw-complete 10/10. Design only.

## 19. Recommendation and next frontier

**`MERGE IMPLEMENTATION PROMPT READY NEXT`**

Justification [I]: the existing merge machinery, helpers, CLI, structural guards,
canonical inputs, contract, and representation are all present and inspectable; the
two gaps (no canonical-artifact write; documented-exception-blind) are well-scoped
and closable by a localized runner extension + tests (§13–§14) under a single
write-authorization flag (§12), validated by the §15 conformance gate. After the
v0.2 cleanup, the prior schema ambiguities are resolved: represented-only is
label-derived and excludes KSG dates (§6); `total_row_count` is the seven-offset sum
with a hard-stop (§6); and all ten expected terminal-status chunk counts plus the
3562 aggregate partition are pinned (§9) — so no missing information blocks
implementation, and no sub-split is needed. The next prompt
should be a **separately-authorized merge-implementation prompt** (code + tests),
followed by the conformance gate, then — only after both pass — a separately
authorized merge-execution prompt. Merge is not authorized; merge has not executed;
Step 2 is not open; the substrate is 10/10 terminal-status, not raw-complete 10/10.
