# Candidate C Design Memo v0.1 Lock Acceptance

**Artifact type:** Lock-acceptance ratification
**Date:** 2026-05-15
**Project:** Coherent Numbers
**Cell:** Candidate C — 12 vs 10 bucket-count comparison

---

## 1. Title

Lock-acceptance ratification of the Candidate C design memo at commit `401ce45e14e02ddc2440fc9cbc7b5e8d01b0696f` as the locked Candidate C protocol under the Coherent Numbers Microscope Program.

## 2. Status

This artifact ratifies the design memo at commit `401ce45e14e02ddc2440fc9cbc7b5e8d01b0696f` as the locked Candidate C protocol. Prior to this artifact, the design memo at `docs/candidate_c_design_memo_v0.1.md` was a pre-registration draft. As of the commit that records this artifact, the design surface specified in that memo — the bucket-count pair {12, 10}, the symmetrical exhaustive 365-DOY anchor surface, the median-PSS-over-the-surface primary statistic per bucket count, the three coupled shared-permutation nulls (`matched_null_12`, `matched_null_10`, `comparison_null`), the four-class verdict map (12-privileged, 10-privileged, Tied / both-structured, Non-confirmatory / unresolved), the 9,500-of-10,000 beat-count thresholds with strict-`<` and ties-do-not-pass, the locked seeds `LABEL_PERM_SEED_C = 20260516` and `ASSET_STRAT_DIAG_SEED_C = 20260517` with `N_PERM = 10,000`, the substrate clause in §15 naming frozen-CSV digests as the run substrate, the §11.6 provenance check against Candidate B's stored `protocol_payload.n2_null_full`, the §12.4 granularity caveat covering all four verdict classes, the §12.5 compound-verdict disclosure, and the §13 inherited-contact disclosure — is closed to revision without a separate, dated amendment artifact.

The wording "Status: Pre-registration draft. Protocol not yet locked. No analysis authorized. No harmonic-calendar features have been computed against pullback `entry_date` under this design." inside the memo file itself is preserved as the historical state at commit `401ce45`. The locked status is conferred by this artifact and the commit that records it, not by retroactive edits to the memo file.

## 3. References

* Design memo file: `docs/candidate_c_design_memo_v0.1.md`
* Design memo commit: `401ce45e14e02ddc2440fc9cbc7b5e8d01b0696f` — `Add Candidate C design memo draft (v0.1, lock-candidate)`
* Design memo SHA-256: `30f716d309af25817ebc2031a4d77d6cc4fce34b82ddbed6084d8c8fe2e92d39`
* Freeze commit (run substrate): `5225bfd` — `Freeze imported pullback trade populations`
* Freeze manifest: `docs/pullback_population_freeze_manifest_v0.1.md`
* Framework memo: `docs/candidate_c_framework_memo_v0.1.md` at commit `03bf9b9` — `Add Candidate C framework memo (v0.1)`
* Cell-Selection Decision Memo (v0.2) — select Candidate B (subsequently closed Split-null): commit `5c30f5d`
* Pullback repo HEAD at inventory: `eac925c` (historical only, not a run-substrate input per §15 of the design memo)

## 4. Verification of pre-lock checklist (§17 of the design memo)

### 4.1 Working tree clean of non-ignored modified/untracked files

> Working tree is clean of non-ignored modified or untracked files. Files covered by .gitignore may exist locally but are not part of the audit state.

**Verified.**

Evidence: `git status --short` returned empty at three audit-relevant points bracketing the lock-acceptance verification work — immediately after the design memo commit `401ce45` landed (post-commit final state), at the start of the frozen-CSV substrate verification run (initial state of that run), and at the end of that run (final state of that run). No staged, modified, or untracked files outside `.gitignore` are present in the working tree.

### 4.2 Frozen-CSV manifest present and intact

> Frozen-CSV manifest from commit 5225bfd is intact; all referenced CSVs are present and digests match.

**Verified.**

Evidence: `docs/pullback_population_freeze_manifest_v0.1.md` is unchanged since its freeze at commit `5225bfd`. The six destination paths recorded under the manifest's "Imported populations" table each resolve to a present file in the working tree. `shasum -a 256` recomputed on file bytes (no parser, no row inspection) at each manifest destination path matches the manifest's recorded digest in all six rows.

| # | Filename                                     | Manifest path                                         | Recorded SHA-256                                                   | Recomputed SHA-256                                                 | Match |
| - | -------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ | ----- |
| 1 | `pullback_spy_base_301_trades_2000_2022.csv` | `data/raw/pullback_spy_base_301_trades_2000_2022.csv` | `b7817e0e7a02dad44923eae462c1454ab67b8fbc73539b36b81e043d8dcc2d06` | `b7817e0e7a02dad44923eae462c1454ab67b8fbc73539b36b81e043d8dcc2d06` | ✓     |
| 2 | `pullback_phase3b_spy_trades_2005_2022.csv`  | `data/raw/pullback_phase3b_spy_trades_2005_2022.csv`  | `1d8a7b77389835a7231d6ca0742e39d963cf4dc03f822b0111039b5c19383621` | `1d8a7b77389835a7231d6ca0742e39d963cf4dc03f822b0111039b5c19383621` | ✓     |
| 3 | `pullback_phase3b_efa_trades_2005_2022.csv`  | `data/raw/pullback_phase3b_efa_trades_2005_2022.csv`  | `275af7e00f28a2a72d948228964c7a4658444f0030ac048e8a2851bc3313de82` | `275af7e00f28a2a72d948228964c7a4658444f0030ac048e8a2851bc3313de82` | ✓     |
| 4 | `pullback_phase3b_eem_trades_2005_2022.csv`  | `data/raw/pullback_phase3b_eem_trades_2005_2022.csv`  | `56cf8e5fe88f5230ebb8e2881f4df1e0ff633819d588764d9e9e57bbdebb6916` | `56cf8e5fe88f5230ebb8e2881f4df1e0ff633819d588764d9e9e57bbdebb6916` | ✓     |
| 5 | `pullback_phase3b_gld_trades_2005_2022.csv`  | `data/raw/pullback_phase3b_gld_trades_2005_2022.csv`  | `0de7bf6dd981be8d8091a382a6dc0af594a59fa8d87f459305ad25f9dc21d1e3` | `0de7bf6dd981be8d8091a382a6dc0af594a59fa8d87f459305ad25f9dc21d1e3` | ✓     |
| 6 | `pullback_phase3b_tlt_trades_2005_2022.csv`  | `data/raw/pullback_phase3b_tlt_trades_2005_2022.csv`  | `037ea4178bd071e426d7cce30eeaffb554ae31d7998c8d00d5e2ba36a7388abc` | `037ea4178bd071e426d7cce30eeaffb554ae31d7998c8d00d5e2ba36a7388abc` | ✓     |

All six matches confirmed. No CSV row was loaded, parsed, or inspected; only file bytes were hashed.

### 4.3 Reduced row schema inherited from Candidate B unchanged

> Reduced row schema (§5) is inherited from Candidate B unchanged.

**Verified.**

Evidence: §5 of the design memo at `30f716d3...` reproduces the per-row field set from Candidate B §5 verbatim — `trade_id`, `asset`, `entry_date`, `exit_date`, `is_long`, `r_multiple`, `frozen_artifact_id`. The design memo states explicitly: "No new columns are added by Candidate C. `source_sha256` remains dataset-level provenance from the freeze manifest, not a per-row analytical field."

### 4.4 Phase formula parameterized; assertion-and-abort; no `%`; grep gate

> Phase formula (§7.1, §7.2) is the parameterized annual-sector formula with bucket_count = k argument and the assertion-and-abort range check on phase ∈ {0..k-1}. No % residue logic appears anywhere in C's lens code (grep gate test required in C's lens tests, parallel to B's).

**Verified at the design surface.**

Evidence: §7.1 specifies `phase = floor(days_since_start * k / cycle_length_days)` followed by the explicit assertion: "Assert phase ∈ {0, 1, ..., k - 1}. If the assertion fails, the run aborts. There is no silent clamp." §7.2 reproduces the same form parameterized over DOY anchor d, with the parallel `assert phase_d ∈ {0, 1, ..., k - 1}` and abort. §7.3 third bullet states "No % operator appears in any C lens code. The same grep gate as Candidate B's `tests/test_candidate_b_lens.py` is required in C's lens test module." The grep-gate test does not yet exist as no Candidate-C implementation files are present at lock-acceptance; its absence at the first implementation commit would violate this clause and that commit would be rejected. The design surface is ratified here.

### 4.5 §9.1 PSS_k η²/correlation-ratio form with `total_k = 0` abort

> §9.1 PSS_k is the η²/correlation-ratio form between_k / total_k, with the total_k = 0 abort rule in force.

**Verified.**

Evidence: §9.1 specifies `between_k = Σ_p (N_p / N_total) × (share_p − share_pooled)²`, `total_k = share_pooled × (1 − share_pooled)`, and `PSS_k = between_k / total_k`. The `total_k = 0` degenerate case is explicitly handled: "If total_k = 0 (pooled population all-longs or all-shorts), raise `DegenerateLongShareError` and abort the run. No fallback." Same η²/correlation-ratio family as Candidate B §9.1, generalized over k.

### 4.6 Bucket counts in scope exactly k = 12 and k = 10

> Bucket counts in scope are exactly k = 12 and k = 10.

**Verified.**

Evidence: §1 narrowing decision 1 names "Q2 — bucket-count privilege — is selected, narrowed further to 12 vs 10 only. The broader §9.2 set {6, 8, 10, 12, 18, 24} is explicitly out of scope for this cell." §7 references k ∈ {10, 12} throughout. §8 supplies the rationale for the binary 12-vs-10 contrast. §16 ninth guardrail states "No additional bucket counts beyond k = 12 and k = 10 may be tested under this cell's verdict map."

### 4.7 Anchor sweep enumerates 365 integer-DOY anchors exhaustively; no separate Feb-29 / DOY-366 anchor

> Anchor sweep enumerates 365 integer-DOY anchors exhaustively; no sampling. No separate Feb-29 / DOY-366 anchor is enumerated; DOY 60 in leap years coincides with Feb 29 as inherited from B.

**Verified.**

Evidence: §7.4 of the design memo states "Anchor enumeration covers integer DOYs 1..365 exhaustively, no sampling, no seed consumed." §7.3 states leap-year effects enter only through `cycle_length_days_d` (which is 365 or 366 per cycle); no separate Feb-29 or DOY-366 anchor is enumerated outside the 1..365 scheme; in leap years the integer DOY 60 anchor coincides with Feb 29 as a direct consequence of `anchor_in_year(y) = date(y, 1, 1) + timedelta(d - 1)`. The inherited Candidate B convention is retained for direct comparability under the §11.6 provenance check.

### 4.8 Primary statistic per bucket count is median PSS over 365-anchor surface

> Primary statistic per bucket count is the median PSS over the 365-anchor surface (§9.2).

**Verified.**

Evidence: §9.2 defines `PSS_surface_k = { PSS_k(d) : d ∈ 1..365 }` and `median_k = median(PSS_surface_k)`. §9.3 defines `diff_observed = median_12_observed − median_10_observed`. §4 names the three observed quantities (`median_12_observed`, `median_10_observed`, `diff_observed_12_minus_10`) as the primary observed outcome, with the four beat counts derived from the coupled permutation nulls.

### 4.9 Three nulls from shared 10,000-element permutation pool

> Three nulls are derived from the same shared 10,000-element permutation pool (§10.1, §10.2).

**Verified.**

Evidence: §10.1 specifies one shared pool of `N_PERM = 10,000` pooled-population permutations of `is_long`, with each permutation producing a paired `(median_12_perm, median_10_perm, diff_perm)` triple. §10.2 names the three derived null distributions: `matched_null_12`, `matched_null_10`, `comparison_null`. §10.4 explicitly notes the coupling: "All four beat counts are derived from the same 10,000 permutation draws. They are not statistically independent."

### 4.10 All four beat-count thresholds exactly 9,500

> All four beat-count thresholds are exactly 9,500.

**Verified.**

Evidence: §12.1 states "All four beat-count thresholds are exactly 9,500 out of 10,000. Strict `<` comparison; ties do not contribute to a pass." §12.2 reproduces "≥ 9500" in each Class 1, 2, and 3 decision rule, with Class 4 as the residual.

### 4.11 Verdict map exactly four classes

> Verdict map is exactly four classes: 12-privileged, 10-privileged, Tied / both-structured, Non-confirmatory / unresolved.

**Verified.**

Evidence: §12.2 defines exactly four mutually exclusive and collectively exhaustive classes with the names above. Class 4 is named "Non-confirmatory / unresolved"; the prior chat-review name "neither-structured" is not present anywhere in the file (Claude Code's read-only compliance check on `grep -niF "neither-structured"` returned exit 1 with zero matches).

### 4.12 Verdict-class interpretive language verbatim

> Verdict-class interpretive language in §12.2 is the locked wording above, used verbatim in the verdict log.

**Verified at the design surface.**

Evidence: §12.2 provides the verbatim two-part `(a) what-it-supports / (b) what-it-does-not-support` language for each of the four classes. The verdict-log emission machinery does not yet exist as no Candidate-C implementation files are present at lock-acceptance; the verbatim-emission requirement is gated by the implementation-test step. The design surface is ratified.

### 4.13 Granularity caveat verbatim with coverage of all four classes

> Granularity caveat (§12.4) is present verbatim in the verdict log, with coverage of all four verdict classes.

**Verified at the design surface.**

Evidence: §12.4 provides the required-verbatim caveat in a single quoted block. The block enumerates per-class implications for 12-privileged, 10-privileged, Tied / both-structured, and Non-confirmatory / unresolved, and closes with "This caveat applies to all four verdict classes." Verdict-log emission is implementation-gated; the design surface is ratified.

### 4.14 Compound-verdict disclosure verbatim

> Compound-verdict disclosure (§12.5) is present verbatim in the verdict log.

**Verified at the design surface.**

Evidence: §12.5 provides the required-verbatim disclosure in a single quoted block framing the four beat counts as coupled pre-registered decision rules under a single shared permutation pool rather than independent p-value claims. Verdict-log emission is implementation-gated; the design surface is ratified.

### 4.15 Inherited data-contact disclosure verbatim

> Inherited data-contact disclosure (§13) is present verbatim, naming both pullback Phase 1–3b contact and Candidate B's prior 12-phase contact.

**Verified.**

Evidence: §13 provides the required-verbatim disclosure in a single quoted block. The block names: (i) pullback Phases 1–3b inspection, partitioning, and within-population statistics estimation during pullback research; (ii) the early lock of pullback `BacktestParams` at pullback commit `50ee2d1` and no re-tuning thereafter; (iii) Candidate B's prior application of 12-phase March-20-anchored machinery — both the §10.1 unstratified label-permutation null and the §10.2 exhaustive 365-DOY anchor-control null in Candidate B's design memo — to the same pooled Phase 3b population; (iv) Candidate B's verdict log path `results/candidate_b_results_20260514_231323_c1982503.json`; (v) the OOS 2023+ seal in both repos and its out-of-scope status for Candidate C; (vi) the closing clause "This disclosure is required wording; a hash citation alone does not satisfy it."

### 4.16 Seeds and permutation count locked

> LABEL_PERM_SEED_C = 20260516 and ASSET_STRAT_DIAG_SEED_C = 20260517 locked, with N_PERM = 10,000 (§14).

**Verified.**

Evidence: §14 specifies `LABEL_PERM_SEED_C = 20260516` is used for §10.1 (primary unstratified pooled permutation) and seeds a single `numpy.random.Generator(numpy.random.PCG64(LABEL_PERM_SEED_C))` instance, and `ASSET_STRAT_DIAG_SEED_C = 20260517` is used for §11.3 (asset-stratified diagnostic) under an independent PCG64 instance. `N_PERM = 10,000` is named in §10.1, §11.3, §14, and Appendix A. C's seeds are explicitly distinct from Candidate B's `LABEL_PERM_SEED = 20260514` and `ASSET_STRAT_DIAG_SEED = 20260515` by design so that C's permutation sequences are not sub-samples of B's; the B-seed values are independently verified in §4.19 below.

### 4.17 Substrate clause: frozen-CSV hashes, not pullback HEAD

> Substrate clause (§15) names frozen-CSV hashes (not pullback HEAD) as run substrate.

**Verified.**

Evidence: §15 states "Following the freeze commit 5225bfd, Candidate C's run substrate is the set of frozen CSV SHA-256 digests recorded in the Coherent Numbers freeze manifest. The pullback research repo's HEAD is not part of the run substrate." The pullback repo HEAD at inventory time (`eac925c`) is recorded as a historical note only, explicitly not a run-time precondition. Manifest digest mismatch aborts the run regardless of pullback HEAD state.

### 4.18 §11.6 provenance check against B's stored k = 12 surface

> Provenance check (§11.6) against Candidate B's stored k = 12 365-anchor surface is enabled and enforces a ≤ 1e-12 per-anchor tolerance. The stored Candidate B surface is read from protocol_payload.n2_null_full in results/candidate_b_results_20260514_231323_c1982503.json, using stringified integer DOY keys "1" through "365"; implementation compares Candidate C anchor d to Candidate B key str(d).

**Verified at the design surface.**

Evidence: §11.6 specifies that Candidate C's recomputed k = 12 365-anchor PSS surface must match Candidate B's stored `protocol_payload.n2_null_full` (string-typed integer DOY keys `"1"` through `"365"`) in `results/candidate_b_results_20260514_231323_c1982503.json` to ≤ 1e-12 absolute difference per anchor, with mismatch aborting the run. The Candidate B back-reference identifying that field by name and JSON path is independently verified in §4.19. The runtime check is implementation-gated; the design surface is ratified.

### 4.19 Candidate B back-references verified

> Candidate B back-references verified by direct inspection of B's artifacts in the Coherent Numbers repo at commit 03bf9b9 or later: (i) Candidate B primary label-permutation seed equals 20260514 as asserted in C §10.1; (ii) Candidate B asset-stratified diagnostic seed equals 20260515 as asserted in C §10.1; (iii) the stored k = 12 365-anchor PSS surface in `results/candidate_b_results_20260514_231323_c1982503.json` is named `n2_null_full` as referenced in C §11.6, or — if differently named — §11.6 is updated to the actual field name prior to lock; (iv) the Candidate B design memo `docs/candidate_b_design_memo_v0.1.md` has its unstratified pooled label-permutation null in §10.1 and its exhaustive 365-DOY anchor-control null in §10.2, as cited in C §13. If the section numbers differ, §13 is updated to the actual section numbers prior to lock. Verification is a read-only inspection in Claude Code. No analysis, computation, or write operation is permitted under this item.

**Verified.**

Evidence: read-only inspection of Candidate B's artifacts in the Coherent Numbers repo confirmed all four back-references prior to this lock-acceptance:

* Candidate B primary label-permutation seed `LABEL_PERM_SEED = 20260514` — present at `docs/candidate_b_design_memo_v0.1.md` line 159 (§10.1), line 281 (§14), line 324 (§17 checklist), line 341 (Appendix A); and at `results/candidate_b_results_20260514_231323_c1982503.json` paths `header.seeds.LABEL_PERM_SEED` and `protocol_payload.seeds.LABEL_PERM_SEED`. Match.
* Candidate B asset-stratified diagnostic seed `ASSET_STRAT_DIAG_SEED = 20260515` — present at `docs/candidate_b_design_memo_v0.1.md` line 219 (§11.3), line 282 (§14), line 324 (§17 checklist), line 341 (Appendix A), line 361 (Appendix C.3); and at the same JSON paths under `header.seeds` and `protocol_payload.seeds`. Match.
* Candidate B stored k = 12 365-anchor PSS surface JSON field — present at `protocol_payload.n2_null_full` in `results/candidate_b_results_20260514_231323_c1982503.json`, with stringified-integer DOY keys `"1"` through `"365"` (length 365). The field name `n2_null_full` referenced in C §11.6 is correct; the path-spec wording in C §11.6 / §17 / Appendix C.6 reflects the full nested path and key-type convention.
* Candidate B design memo null-section references — present at `docs/candidate_b_design_memo_v0.1.md` line 148 (`## 10. Null hypotheses and finite controls`), line 152 (`### 10.1 N.1 — Unstratified label-permutation null (primary)`), line 165 (`### 10.2 N.2 — Exhaustive 365-DOY anchor-control null (primary)`). The §10.1 / §10.2 citations in C §13 are correct as written.

No corrective rewrite of any C-memo section is required as a result of this verification.

## 5. No-data-contact statement

The following negative claims hold as of this lock-acceptance:

* No harmonic-calendar features have been computed against pullback `entry_date` under the Candidate C design.
* No `entry_date` joins, phase-distribution histograms, or sanity-check "previews" have been performed under the Candidate C design.
* No `PSS_k` statistics have been computed for k ∈ {10, 12} or any other k under the Candidate C design.
* No row-level inspection of any frozen pullback CSV has been performed under Candidate C. The substrate verification in §4.2 hashed file bytes only via `shasum -a 256`; no CSV parser was invoked and no row was loaded.
* No modification, staging, or commit has been performed on the pullback research repository at `/Users/jay/pullback_research`. Pullback HEAD has not been re-inspected since the inventory note (`eac925c`).
* OOS 2023+ has not been accessed in either repo.
* No Candidate C implementation files, test files, or analysis output files exist in the repository as of the lock-acceptance commit.
* No null-distribution sampling, anchor enumeration, or median computation has been executed against any data under the Candidate C design.

## 6. Lock statement

The Candidate C design memo at commit `401ce45e14e02ddc2440fc9cbc7b5e8d01b0696f` is accepted as the locked protocol for Candidate C. From this point forward, implementation may proceed only under the terms specified in that memo. No design field — the bucket-count pair {12, 10}; the symmetrical exhaustive 365-DOY anchor surface enumerated 1..365 with the inherited Candidate B convention that DOY 60 in leap years coincides with Feb 29; the median-PSS-over-the-surface primary statistic per bucket count; the three coupled shared-permutation nulls `matched_null_12`, `matched_null_10`, `comparison_null` drawn from one shared `N_PERM = 10,000` pool; the four-class verdict map with classes 12-privileged, 10-privileged, Tied / both-structured, Non-confirmatory / unresolved; the 9,500-of-10,000 beat-count thresholds with strict-`<` and ties-do-not-pass; the granularity caveat in §12.4 with coverage of all four verdict classes; the compound-verdict disclosure in §12.5; the inherited data-contact disclosure in §13; the locked seeds `LABEL_PERM_SEED_C = 20260516` and `ASSET_STRAT_DIAG_SEED_C = 20260517`; the substrate clause in §15 naming the frozen-CSV digests recorded at freeze commit `5225bfd` as the run substrate; the §11.6 provenance check against Candidate B's stored `protocol_payload.n2_null_full` for k = 12 at ≤ 1e-12 absolute per-anchor tolerance — may be changed without a new amendment artifact and its own audit trail. Analysis is authorized only after this lock-acceptance artifact is committed.

## 7. Post-lock authorization boundary

From the commit that records this artifact, the following actions become authorized within the locked terms:

* Implementation modules for the Candidate C lens (parameterized §7.1 / §7.2 phase formula with assertion-and-abort range check on `phase ∈ {0..k-1}`) and the §9.1 `PSS_k` statistic (η²-form with `total_k = 0` `DegenerateLongShareError` abort) may be written, including a `tests/test_candidate_c_lens.py` no-`%` grep gate test parallel to Candidate B's.
* Frozen pullback CSV files at the manifest's recorded destination paths may be loaded under the §6 three-strikes hash-verification pattern.
* `entry_date` may be mapped to `(k, d, phase)` triples via §7.2 for k ∈ {10, 12} and d ∈ 1..365.
* The §10.1 shared-permutation pool (`N_PERM = 10,000`, `LABEL_PERM_SEED_C = 20260516`) may be drawn, and the three derived null distributions plus the four beat counts may be computed.
* The §11 diagnostics — best-anchor PSS per bucket count, anchor-distribution shape, asset-stratified label-permutation diagnostic seeded by `ASSET_STRAT_DIAG_SEED_C = 20260517`, per-asset PSS at the civil-date March-20 anchor (via §7.1) and at each bucket count's peak anchor (from the §7.2 surface), top-10 anchors per bucket count, and the §11.6 provenance check against Candidate B's stored `protocol_payload.n2_null_full` — may be computed.
* The verdict log may be generated containing the four beat counts unconditionally, the verdict class per §12.2 decision rules, and the verbatim §12.4 granularity caveat, §12.5 compound-verdict disclosure, and §13 inherited-contact disclosure.
* The §11.6 provenance check against Candidate B's stored k = 12 365-anchor surface is enforced at run time and aborts on any per-anchor absolute difference exceeding 1e-12.

The following remain prohibited:

* No design field may be changed after observing results. The locked field list is enumerated in §6 above.
* OOS 2023+ remains sealed in both repos and may not be accessed.
* The pullback research repository at `/Users/jay/pullback_research` may not be modified. Re-inspection is permitted as a provenance note only; drift does not block a Candidate C run whose frozen-CSV digests match the manifest, and the matching frozen-CSV digests are the authoritative run substrate per §15.
* No additional verdict heads beyond the four classes in §12.2 may be registered. The verdict class is determined exclusively by the four beat counts applied to the §12.2 rules; no diagnostic may upgrade the class.
* No diagnostic in §11 may rescue a Non-confirmatory / unresolved verdict per §12.6. The no-rescue rule is absolute.
* No sampling-based anchor control may be introduced; the v0.3.3 exhaustive-enumeration discipline is inherited.
* No nested 12×12, neighbor-influence, or "Influential Numbers" tests may be added as "diagnostics" or anywhere else in Candidate C's run. These remain explicitly out of scope for this cell and are reserved for possible future cells contingent on Candidate C's findings.
* No additional bucket counts beyond k = 12 and k = 10 may be tested under this cell's verdict map.

## 8. Final state

* Design memo locked at commit `401ce45e14e02ddc2440fc9cbc7b5e8d01b0696f`. File SHA-256: `30f716d309af25817ebc2031a4d77d6cc4fce34b82ddbed6084d8c8fe2e92d39`.
* Frozen-CSV substrate verified at the freeze manifest from commit `5225bfd`; all six recorded digests match recomputed digests at the manifest's destination paths.
* No Candidate C implementation, tests, or output files exist in the repository.
* No Candidate C analysis has been executed.
* The next artifact in the audit chain is implementation + tests, not a design revision. Any revision to the locked design surface requires a dated amendment artifact and its own commit.
