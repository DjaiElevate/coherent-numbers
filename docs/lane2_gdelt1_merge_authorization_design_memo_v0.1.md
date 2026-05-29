# Lane 2 GDELT1 — Merge-Authorization Design Memo v0.1

Ordinal 117. Design memo only. Drafted after ordinal 116's cross-chunk
disclosure + pre-merge conformance diagnostic
(`SUCCESS WITH NON-BLOCKING DISCLOSURE OBSERVATIONS — PRE-MERGE CONFORMANCE PASSED`).

Evidence legend: **[O]** observed git/fs · **[A]** artifact-derived (chunk
metadata / contributions / representation / contract) · **[S]** static source
inspection (runner) · **[I]** inference / design recommendation.

---

## 1. Purpose and non-authorization statement

This memo designs the path by which a future, separately authorized prompt may
authorize and execute the offline merge of the Lane 2 GDELT1 full-build
substrate. It governs that later step; it does not perform it.

This memo, in this turn:

- does **not** execute or authorize any merge;
- does **not** open Step 2 (instrument construction / market-data join);
- does **not** touch market data;
- does **not** amend `KNOWN_SUBSTRATE_GAPS`;
- leaves merge a **separately authorized** future action.

Merge remains gated. Nothing here flips a guard, writes a merged artifact, or
declares the substrate merged.

## 2. Canonical substrate state

From ordinal 116 [A]:

- **10/10 terminal-status chunks** — not 10/10 raw-complete.
- **9 raw-complete chunks** (2013_partial, 2014–2021).
- **1 labeled-complete documented-exception chunk** (chunk_2022).
- chunk_2022 is **not raw-complete**.
- chunk_2022 has **365 terminal-status days = 364 raw_processed + 1 documented
  exception** (`recovered_days`=0, `known_no_data_gap_days`=0).
- chunk_2013 is the **partial regime-start year** (window 2013-04-01..12-31):
  275 expected = 275 actual; complete. The `_partial` tag is descriptive, not
  an incompleteness flag.
- chunk_2014 carries **4 known-no-data-gap days** drawn from the global
  `KNOWN_SUBSTRATE_GAPS` constant (the four 2014 dates); these are a distinct
  category from any documented exception.
- chunk_2022 `known_no_data_gap_days` = **0**.

## 3. Canonical chunk table summary

Reproduced from the ordinal-116 disclosure table [A]. Per-artifact SHA-256s and
manifest digests were collected and passed disclosure in ordinal 116 and are not
re-listed here (see that report); they must be re-verified at merge preflight
(§8).

| chunk_id | canonical_output_dir | status_class | exp_cal | raw | doc_exc | ksg | terminal | complete |
|---|---|---|---|---|---|---|---|---|
| chunk_2013_partial | chunk_2013_partial_20260524T135157Z | raw_complete | 275 | 275 | 0 | 0 | 275 | true |
| chunk_2014 | chunk_2014_20260524T150055Z | raw_complete | 365 | 361 | 0 | 4 | 365 | true |
| chunk_2015 | chunk_2015_20260524T163556Z | raw_complete | 365 | 365 | 0 | 0 | 365 | true |
| chunk_2016 | chunk_2016_20260524T194435Z | raw_complete | 366 | 366 | 0 | 0 | 366 | true |
| chunk_2017 | chunk_2017_20260524T231143Z | raw_complete | 365 | 365 | 0 | 0 | 365 | true |
| chunk_2018 | chunk_2018_20260525T025641Z | raw_complete | 365 | 365 | 0 | 0 | 365 | true |
| chunk_2019 | chunk_2019_20260526T130910Z | raw_complete | 365 | 365 | 0 | 0 | 365 | true |
| chunk_2020 | chunk_2020_20260528T080812Z | raw_complete | 366 | 366 | 0 | 0 | 366 | true |
| chunk_2021 | chunk_2021_20260528T110740Z | raw_complete | 365 | 365 | 0 | 0 | 365 | true |
| chunk_2022 | chunk_2022_20260528T234738Z | labeled_complete_documented_exception | 365 | 364 | 1 | 0 | 365 | true |

Retained halt-history dirs (non-canonical, excluded from merge):
`chunk_2022_20260528T121150Z`, `chunk_2020_20260526T164747Z`, and
`archive/halted_attempts/.../chunk_2019_20260525T192552Z`.

## 4. Documented-exception handling requirement

The merge must carry chunk_2022's documented exception verbatim [A]
(from `configs/lane2_gdelt1_documented_exceptions.json` and the representation
artifact):

- label: `UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY`
- date: `2022-11-10`
- file: `20221110.export.CSV.zip`
- catalog md5: `91e15516016f986e5b8a08712e1de95a`
- catalog filesize: `6714105`
- `raw_object_parsed` = False
- `rows_recovered` = False
- `http_status` = 404
- `no_data_gap` = False
- `recovered` = False
- `known_substrate_gap_amended` = False

The merge **must not** collapse 2022-11-10 into: raw-processed, recovered, a
`KNOWN_SUBSTRATE_GAPS` no-data gap, ordinary raw completion, or a
missing/invisible status. The day is **represented-only**: in
`chunk_contributions.csv` it has `rows_from_offset_0 = 0` and is represented
solely via neighbor offsets (−1, −7, −30) [A]. The merged artifact must preserve
this exact distinction.

## 5. Canonical F1–F6 mapping for merge-time audit

**Source of truth (settled):** the canonical F1–F6 forbidden-claim set for any
future merge-time audit is the **artifact-level** `forbidden_claims` array in
`representations/lane2_gdelt1/chunk_2022_documented_exception_20221110/representation.json`
[A], reinforced by the documented-exception contract `forbidden_uses` and the
merge-gate representation design memo §8/§12 lineage:

- **F1** = `raw 365/365`
- **F2** = `ordinary completion`
- **F3** = `no-data gap`
- **F4** = `recovered day`
- **F5** = `raw-processed day`
- **F6** = `exact runner-output gate from BigQuery count 105041`

The earlier **discipline-level "F1–F6" mnemonic** used informally during
ordinals 108–115 is **historical shorthand only** and is **not** the canonical
merge-time audit source. Where the two ever diverge, the artifact-level set
above governs.

Merge-time audit must apply this artifact-level set — especially to the
chunk_2022 documented-exception pathway and to **any merged-output text** that
describes that day or the substrate as a whole.

## 6. Legacy raw-complete wording scope

Ordinal-116 result [A][O]:

- all ten canonical `chunk_summary.md` files had **F1–F6 count = 0** under the
  artifact-level set;
- the ordinal-116 §E.1 "legacy raw-complete wording" carve-out was **unused**
  (the raw-complete summaries carry no `365/365`-style or "raw days processed"
  phrasing at all).

Rule for future audits:

- **Blocking** iff a forbidden claim is used to describe the chunk_2022
  documented-exception pathway (or the merged substrate as raw-complete).
- **Non-blocking** iff a legacy raw-complete chunk truthfully describes its own
  raw-complete state and does not touch chunk_2022 / documented-exception
  semantics.

## 7. Non-blocking disclosure observations carried forward

From ordinal 116 [A]:

1. chunk_2013 carries `_partial` naming because it is the partial regime-start
   year (275 expected = 275 actual). Not an incompleteness flag.
2. chunk_2014 has `expected_file_count` = 361 after four KSG exclusions; the four
   2014 KSG dates are handled through the global `KNOWN_SUBSTRATE_GAPS` constant
   / `substrate_gap_diagnostic`. Distinct from a documented exception.
3. the global `substrate_gap_diagnostic` echoes the four 2014 KSG dates in every
   chunk's metadata, including chunks where those dates are out of window; a
   harmless constant echo whenever in-window `known_no_data_gap_days` = 0.
4. ordinal 116 did not verify the contract SHA because it searched the wrong
   scope (`docs/`, `representations/`). **Resolved this turn:** the contract is
   at `configs/lane2_gdelt1_documented_exceptions.json` and its SHA-256 verifies
   (§8). Merge preflight must verify the contract **directly at that path**.

## 8. Merge preflight requirements

A future merge-authorization prompt must verify, before any merge execution:

- HEAD / origin/main at the then-current expected baseline; `0 0` ahead/behind;
  tracked tree clean.
- runner blob = `799b6d85b29be1ebe2df47db288e4f9eac6b038f`; guard
  `FULL_BUILD_AUTHORIZED = False` @ line 95.
- contract SHA-256 at `configs/lane2_gdelt1_documented_exceptions.json` =
  `afee1c0d1e0e1d73fbe1ef45161deba4d174a4903e4b90093d00ac00472dda97`
  (verified this turn [O]).
- representation JSON SHA-256 =
  `91276597f4f3882d15133e32ec2d845badd244f7c89e706d06482a9d729c4ee3`
  (verified this turn [O]); representation summary SHA-256 =
  `635bbc983d877b9996b05e25c0497d551be8fb7eb2e52a7461a75270d3525150`.
- memory SHA-256 state re-verified if the then-current prompt makes it
  load-bearing.
- all 10 canonical output dirs present (§3); halted dirs retained but **excluded**
  from `--merge-input`.
- chunk_2022 output hashes match ordinal 114/116:
  csv `45405bf9cc59776578a2081f55d86617453d1ece6ef5b9d1b1f4c3363e66004a`,
  json `e986e217d1906aa3e7fbe3bf412add975738bf10fba8334b704440b9d3184de1`,
  md `d92e22b4b72d4da556a9878d777b6ef577102c88b2fbf5f9689cdf8e6aef0da0`.
- Path (b) = 114 until the next memory-write boundary.
- no merge already performed; no merged artifact present.
- no Step 2 open; no market data touched.

## 9. Merge execution design questions

Read-only inspection of `scripts/run_lane2_gdelt1_full_daily_count_build.py` [S]:

- **Is there an existing merge script / command?** **Yes.** `merge_chunks()`
  (~line 2470) plus a `--merge` / `--merge-input CHUNK_ID=DIR` CLI mode
  (mutually exclusive with `--chunk-id`). Helpers: `load_chunk_contributions`,
  `load_chunk_metadata`, `build_all_chunk_manifests`.
- **Does it have an authorization guard?** **No merge-specific guard.** Merge is
  offline ("No GDELT contact; no guard flip required"). The
  `--authorize-full-build-run` / `FULL_BUILD_AUTHORIZED` /
  `LANE2_FULL_BUILD_AUTHORIZED` three-guard applies **only to live fetch** and
  must **not** be conflated with merge. There is a structural **integrity**
  guard: `ChunkManifestError` on missing chunk, manifest-digest mismatch,
  cross-chunk duplicate URL, or union ≠ recognized-list fetch set; and
  `FullBuildBoundaryBreach` on an invalid coverage flag.
- **Does it assume all chunks are raw-complete?** **No, but it is
  documented-exception-blind.** Manifest digests are computed over **expected**
  fetch-set URLs, so chunk_2022's unfetched 2022-11-10 does **not** cause a
  digest halt. It checks `expected_file_count` / `actual_completed_file_count`
  for record-keeping only; it does not assert raw-completeness.
- **Does it consume chunk metadata or only contributions CSVs?** **Both.**
  metadata for digest + expected/actual counts; CSVs for the SQLDATE counts.
- **Can it carry documented-exception metadata into the merged artifact?**
  **Not currently.** `merge_chunks` never reads `documented_exception_diagnostic`;
  `per_chunk_summary` carries only `expected_file_count`,
  `actual_completed_file_count`, `chunk_manifest_digest`. Coverage flags for each
  civil date are **recomputed generically** from the recognized-list fetch set +
  `KNOWN_SUBSTRATE_GAPS`, so 2022-11-10 would surface as a generic coverage
  shortfall (offset_0 = 0) **without** the documented-exception label, md5,
  filesize, or `status_class`.
- **Does it produce a manifest / metadata / summary?** **Not yet.** The CLI
  handler computes `merge_chunks` in memory and prints "Merge complete
  (in-memory only; CLI does not write canonical artifacts in this implementation
  turn)." No merged CSV / metadata / summary is written.
- **Does it need implementation changes before merge authorization?** **Yes.**
  (a) implement the merge **writer** (canonical merged daily-count CSV +
  `build_metadata.json` + `build_summary.md`); (b) **propagate
  documented-exception semantics** (label, date/file/md5/filesize, `status_class`
  per chunk, the §10 category counts, retained halt-history references, F1–F6
  merge-time audit result, and an explicit "merge does not open Step 2"
  statement) into the merged metadata/summary.

**Conclusion [I]:** merge machinery is present and structurally guarded but
**incomplete** for a documented-exception-aware merge — it writes nothing and is
label-blind. Per §B.7 of the prompt, the next step is **merge-implementation
design**, not merge execution.

## 10. Merge output requirements

A future merged-substrate artifact (or accompanying metadata) must preserve [I]:

- per-chunk `status_class`;
- the `raw_complete` vs `labeled_complete_documented_exception` distinction;
- chunk_2022's documented-exception label;
- documented-exception date / file / md5 / filesize;
- category counts per chunk and in aggregate: raw_processed;
  documented_unavailable_data_confirmed; recovered; known_no_data_gap;
  terminal_status;
- the `terminal_status_complete` flag;
- retained halt-history references (the three non-canonical dirs in §3);
- the F1–F6 merge-time audit result (artifact-level set, §5);
- an explicit statement that the merge does **not** open Step 2.

The merged daily-count rows must keep 2022-11-10's `rows_from_offset_0 = 0`
(represented-only) and must not back-fill or synthesize an offset-0 value.

## 11. Authorization posture

Recommendation [I]:

- The merge is **offline** (no network, no market data) and already carries a
  structural integrity guard. It therefore does **not** require — and must not
  reuse — the live-fetch `FULL_BUILD_AUTHORIZED` three-guard. Conflating the two
  would be a category error.
- Because the merge **writer is unimplemented** and the merge is
  **label-blind**, a source/CLI authorization guard is not the binding
  constraint; **implementation** is. The recommended posture is:
  1. implement the documented-exception-aware merge writer (§9–§10) under a
     normal scoped implementation prompt (commit-scoped authorization, like the
     chunk runs);
  2. add a **merge-output conformance gate** that re-runs the ordinal-116-style
     checks (F1–F6 artifact-level audit + category-count coherence + label
     presence/propagation) against the **merged** artifact;
  3. only then a **tightly-scoped merge-authorization + execution prompt**.
- A dedicated boolean merge guard in source is **optional**; if added it must be
  a distinct constant (e.g. a `MERGE_*` flag), never the live-fetch guard. A
  tightly-scoped prompt + the existing integrity guard + the new conformance
  gate are sufficient for an offline merge.

## 12. Self-heal fallback

If the 2022-11-10 raw object becomes available again in a future **separately
authorized** rebuild, the normal raw-path processing supersedes the
documented-exception state for that date and retires the documented-exception
label for 2022-11-10.

Until such a separately authorized rebuild replaces it, the **current merge must
carry the documented-exception label** from the already-completed chunk_2022
output. Self-heal is a free fallback, never an obligation and never a reason to
delay the labeled merge.

## 13. Recommended next frontier

**`MERGE IMPLEMENTATION DESIGN REQUIRED BEFORE AUTHORIZATION`**

Justification [I]: the disclosure substrate is clean and merge preflight passes,
but the merge code path (a) **writes no canonical artifact** and (b) is
**documented-exception-blind** — it cannot satisfy the §10 merge-output
requirements (per-chunk status class, the chunk_2022 label and catalog fields,
the five category counts, retained halt-history, F1–F6 merge-time audit, and the
"no Step 2" statement). A merge executed today would silently flatten
2022-11-10 into a generic coverage shortfall. The next prompt should therefore
design (then, separately, implement) the documented-exception-aware merge writer
and its conformance gate — **before** any merge-authorization/execution prompt.
Merge is not authorized. Step 2 is not open. The substrate is 10/10
terminal-status, not 10/10 raw-complete.
