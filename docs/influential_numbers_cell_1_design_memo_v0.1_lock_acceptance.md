# Influential Numbers Program — Cell 1 Design Memo v0.1 Lock Acceptance

**Artifact type:** Lock-acceptance ratification
**Date:** 2026-05-15
**Project:** Coherent Numbers
**Program:** Influential Numbers
**Cell:** Cell 1 — Neighborhood Influence Test

---

## 1. Title

Lock-acceptance ratification of the Influential Numbers Cell 1 design memo at commit `a765098aa58472fda7080ea08416a4ccf312e16a` as the locked Cell 1 protocol under the Coherent Numbers Influential Numbers program.

## 2. Status

This artifact ratifies the design memo at commit `a765098aa58472fda7080ea08416a4ccf312e16a` as the locked Cell 1 protocol. Prior to this artifact, the design memo at `docs/influential_numbers_cell_1_design_memo_v0.1.md` was a pre-registration lock-candidate draft. As of the commit that records this artifact, the design surface specified in that memo — the frozen pullback × pooled Phase 3b 1,282-trade substrate; the multi-focal set `F = {10, 12, 14, 16}` with primary focal `12` and control focals `10, 14, 16`; the `±3` linear-integer window and bucket-count universe `K = {7, …, 19}`; the median-PSS-over-the-365-anchor-surface per-bucket-count statistic; the focal-centered continuous-attenuation statistic `attenuation_score_f = −slope(median_k ~ |k − f|)`; the strict-`>` focal-elevation gate for 12; the `max_gap` contrast against the maximum control attenuation; the single shared `N_PERM = 10,000` unstratified pooled `is_long` permutation null; the locked seeds `LABEL_PERM_SEED_CELL1 = 20260518` and `ASSET_STRAT_DIAG_SEED_CELL1 = 20260519`; the two primary beat counts with the `9,500/10,000` strict-`<` ties-do-not-pass threshold; the hard-binary Class 4 with no marginal band; the four-class verdict map with its display names and `class_1..class_4` machine labels; the Required-verbatim block register; the asset-stratified diagnostic as a non-verdict diagnostic; the §17 provenance gate against Candidate C's stored `protocol_payload.pss_surface_10` and `protocol_payload.pss_surface_12`; and the §19 infrastructure boundary — is closed to revision without a separate, dated amendment artifact.

The wording "Status: Pre-registration draft. Protocol not yet locked. No analysis authorized. No neighborhood-surface features have been computed against pullback `entry_date` under this design. This memo is a clean review draft only; the repo file is not created and nothing is lock-accepted." inside the memo file itself is preserved as the historical state at commit `a765098aa58472fda7080ea08416a4ccf312e16a`. The locked status is conferred by this artifact and the commit that records it, not by retroactive edits to the memo file.

## 3. References

* Design memo file: `docs/influential_numbers_cell_1_design_memo_v0.1.md`
* Design memo commit: `a765098aa58472fda7080ea08416a4ccf312e16a` — `Influential Numbers Cell 1 design memo (lock-candidate)`
* Design memo SHA-256: `90e56a5318afcc25c5444fcc5cee911927c86afb41a71b2f3948b8335e28df84`
* Framework memo file: `docs/influential_numbers_cell_1_framework_memo_v0.1.md`
* Framework memo commit: `8ff619c` — `Influential Numbers Cell 1 framework memo`
* Freeze commit (run substrate): `5225bfd` — `Freeze imported pullback trade populations`
* Freeze manifest: `docs/pullback_population_freeze_manifest_v0.1.md`
* Candidate C verdict-log provenance target: `results/candidate_c_results_20260515_051236_f3a6bf48.json`
* Candidate C verdict-log commit: `a19b2e9` — `Land Candidate C v0.1 verdict log (locked run)`
* Candidate C verdict-log JSON SHA-256: `130235fef110cca141fa8873bfa3a6c630a44ac11dfcad953822f41f9cd3c7d4`
* Candidate C closure commit: `1659819` — `Close Candidate C v0.1: 12-privileged`
* Candidate C lock-acceptance template: `docs/candidate_c_design_memo_v0.1_lock_acceptance.md` at commit `dc97576`
* Candidate C design memo (provenance/inheritance context): `docs/candidate_c_design_memo_v0.1.md` at commit `401ce45`
* Pullback repo HEAD at inventory: `eac925c` (historical note inherited from the freeze manifest only; not a run-substrate input per §17 of the design memo)

## 4. Verification of pre-lock checklist (§22 of the design memo)

### 4.1 Working tree clean of non-ignored modified/untracked files

> Working tree clean of non-ignored modified/untracked files.

**Verified.**

Evidence: `git status --short` returned empty at the audit-relevant points bracketing this lock-acceptance verification work — at the start of the verification run and at its end. No staged, modified, or untracked files outside `.gitignore` are present in the working tree. The design memo itself is committed at `a765098aa58472fda7080ea08416a4ccf312e16a` with a clean tree thereafter.

### 4.2 Frozen-CSV manifest present and intact

> Frozen-CSV manifest from `5225bfd` intact; all six referenced CSVs present and digests match.

**Verified.**

Evidence: `docs/pullback_population_freeze_manifest_v0.1.md` is unchanged since its freeze at commit `5225bfd`. The six destination paths recorded under the manifest's "Imported populations" table each resolve to a present file in the working tree. `shasum -a 256` recomputed on file bytes (no parser, no row inspection) at each manifest destination path matches the manifest's recorded digest in all six rows.

| # | Filename | Manifest path | Recorded SHA-256 | Recomputed SHA-256 | Match |
| - | -------- | ------------- | ---------------- | ------------------ | ----- |
| 1 | `pullback_spy_base_301_trades_2000_2022.csv` | `data/raw/pullback_spy_base_301_trades_2000_2022.csv` | `b7817e0e7a02dad44923eae462c1454ab67b8fbc73539b36b81e043d8dcc2d06` | `b7817e0e7a02dad44923eae462c1454ab67b8fbc73539b36b81e043d8dcc2d06` | ✓ |
| 2 | `pullback_phase3b_spy_trades_2005_2022.csv` | `data/raw/pullback_phase3b_spy_trades_2005_2022.csv` | `1d8a7b77389835a7231d6ca0742e39d963cf4dc03f822b0111039b5c19383621` | `1d8a7b77389835a7231d6ca0742e39d963cf4dc03f822b0111039b5c19383621` | ✓ |
| 3 | `pullback_phase3b_efa_trades_2005_2022.csv` | `data/raw/pullback_phase3b_efa_trades_2005_2022.csv` | `275af7e00f28a2a72d948228964c7a4658444f0030ac048e8a2851bc3313de82` | `275af7e00f28a2a72d948228964c7a4658444f0030ac048e8a2851bc3313de82` | ✓ |
| 4 | `pullback_phase3b_eem_trades_2005_2022.csv` | `data/raw/pullback_phase3b_eem_trades_2005_2022.csv` | `56cf8e5fe88f5230ebb8e2881f4df1e0ff633819d588764d9e9e57bbdebb6916` | `56cf8e5fe88f5230ebb8e2881f4df1e0ff633819d588764d9e9e57bbdebb6916` | ✓ |
| 5 | `pullback_phase3b_gld_trades_2005_2022.csv` | `data/raw/pullback_phase3b_gld_trades_2005_2022.csv` | `0de7bf6dd981be8d8091a382a6dc0af594a59fa8d87f459305ad25f9dc21d1e3` | `0de7bf6dd981be8d8091a382a6dc0af594a59fa8d87f459305ad25f9dc21d1e3` | ✓ |
| 6 | `pullback_phase3b_tlt_trades_2005_2022.csv` | `data/raw/pullback_phase3b_tlt_trades_2005_2022.csv` | `037ea4178bd071e426d7cce30eeaffb554ae31d7998c8d00d5e2ba36a7388abc` | `037ea4178bd071e426d7cce30eeaffb554ae31d7998c8d00d5e2ba36a7388abc` | ✓ |

All six matches confirmed. No CSV row was loaded, parsed, or inspected; only file bytes were hashed.

### 4.3 Reduced row schema inherited from Candidate B/C unchanged

> Reduced row schema (§6) inherited from Candidate B/C unchanged.

**Verified.**

Evidence: §6 of the design memo at SHA-256 `90e56a5318afcc25c5444fcc5cee911927c86afb41a71b2f3948b8335e28df84` reproduces the per-row field set from Candidate B §5 / Candidate C §5 verbatim — `trade_id`, `asset`, `entry_date`, `exit_date`, `is_long`, `r_multiple`, `frozen_artifact_id`. The design memo states: "No new columns are added by Cell 1. `source_sha256` remains dataset-level provenance from the freeze manifest, not a per-row analytical field." Schema reconciliation across the SPY 21-column long-form and the Phase 3b 11-column compact schemas is inherited from Candidate B unchanged and not re-opened.

### 4.4 Lens parameterized over k; assertion-and-abort; no-`%`; grep gate

> Lens (§7) parameterized over `k` with the assertion-and-abort range check and the no-`%` grep gate test.

**Verified at the design surface.**

Evidence: §7.1 specifies `phase = floor(days_since_start * k / cycle_length_days)` followed by "Assert `phase ∈ {0, …, k-1}`; abort on assertion failure. No silent clamp." §7.2 reproduces the same form parameterized over DOY anchor `d` with the parallel `assert phase_d ∈ {0, …, k-1}` and abort. §7.1 states "No `%` operator anywhere in Cell 1 lens code (grep gate test required, parallel to Candidate B/C)." The grep-gate test does not yet exist as no Cell 1 implementation files are present at lock-acceptance; its absence at the first implementation commit would violate this clause and that commit would be rejected. The design surface is ratified here.

### 4.5 PSS §9.1 η²-form `between_k/total_k` with `total_k = 0` abort

> PSS (§9.1) is the η²-form `between_k/total_k` with the `total_k = 0` abort.

**Verified.**

Evidence: §9.1 specifies `between_k = Σ_p (N_p / N_total) × (share_p − share_pooled)^2`, `total_k = share_pooled × (1 − share_pooled)`, and `PSS_k = between_k / total_k`. The `total_k = 0` degenerate case is explicitly handled: "If `total_k = 0` (all-long or all-short pool), raise `DegenerateLongShareError` and abort. No fallback." Same η²/correlation-ratio family as Candidate C §9.1, generalized over `k ∈ K = {7, …, 19}`.

### 4.6 Focal set, primary, controls, window, K

> Focal set exactly `F = {10, 12, 14, 16}`, primary `12`, controls `10, 14, 16`; window exactly `±3`; `K = {7, …, 19}`.

**Verified.**

Evidence: §8 ("Focal centers and windows") states Lock 2 — focal centers `F = {10, 12, 14, 16}`, primary focal `12`, control focals `10, 14, 16`; and Lock 3 — `W(f) = {f−3, …, f+3}` with the four explicit windows `W(10) = {7,8,9,10,11,12,13}`, `W(12) = {9,10,11,12,13,14,15}`, `W(14) = {11,12,13,14,15,16,17}`, `W(16) = {13,14,15,16,17,18,19}`, and total universe `K = {7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}` (13 distinct bucket counts). Guardrail §21.8 forbids any focal centers, bucket counts, or window other than these.

### 4.7 Structure statistic — focal-centered OLS attenuation

> Structure statistic exactly the §10 OLS attenuation `−slope(median_k ~ |k−f|)` over the seven window points with distance multiset `{0,1,1,2,2,3,3}`, focal included.

**Verified.**

Evidence: §10 ("Neighborhood structure statistic", Lock 4) specifies, per focal `f`: compute `median_k` for every `k ∈ W(f)` (seven values); define `distance_k = |k − f|` with the seven-point distance multiset exactly `{0, 1, 1, 2, 2, 3, 3}` (the focal contributes the single `0`); `slope_f = OLS_slope(median_k ~ |k − f|)` over all seven points; `attenuation_score_f = − slope_f`. The focal `k = f` is included as the `distance = 0` point in the regression. Strict monotonic attenuation is a secondary diagnostic only and cannot drive, alter, upgrade, or rescue any verdict.

### 4.8 Focal-elevation gate strict `>`

> Focal-elevation gate (§11) is strict `>` against the mean of the six non-focal window neighbors of 12.

**Verified.**

Evidence: §11 ("Focal-elevation gate") specifies `focal_elevation_gate_12 := median_12 > mean({ median_k : k ∈ W(12), k ≠ 12 })`, i.e. the focal's own median PSS must strictly exceed the arithmetic mean of its six non-focal window neighbors `{9, 10, 11, 13, 14, 15}`; the gate is strict `>`. Exact numerical ambiguity in the gate (a floating-point tie, or a non-finite `median_k` entering it) is explicitly routed to Class 4 per §15.4, not a pass and not a default to Class 3.

### 4.9 `max_gap` uses `max(·)` over the three control focals

> `max_gap` (§12) uses `max(·)` over the three control focals.

**Verified.**

Evidence: §12 ("Control contrast: max-gap", Lock 5) specifies `max_gap_observed = attenuation_score_12 − max(attenuation_score_10, attenuation_score_14, attenuation_score_16)`. The memo states the use of `max(·)` over the three controls (rather than a mean) is the conservative choice: 12 must beat the best-looking control before any 12-specific structure is claimed, as the design's guard against generic substrate smoothness.

### 4.10 Primary shared label-permutation null and seed

> Primary null is one shared 10,000-element unstratified pooled `is_long` permutation pool; `LABEL_PERM_SEED_CELL1 = 20260518`.

**Verified.**

Evidence: §13 ("Null hypotheses and finite controls") specifies a single shared pool of `N_PERM = 10,000` pooled-population permutations of `is_long`, phase and asset labels held fixed, only `is_long` permuted, no asset stratification in the primary pool. Locked seed `LABEL_PERM_SEED_CELL1 = 20260518`, a single `numpy.random.Generator(numpy.random.PCG64(LABEL_PERM_SEED_CELL1))` instance. The seed is explicitly distinct from Candidate B's `20260514`/`20260515` and Candidate C's `20260516`/`20260517`, so Cell 1's permutation sequence is not a sub-sample of any prior cell's; the B/C seed values are independently confirmed in §4.17.

### 4.11 Two primary beat counts, strict `<`, threshold `9500/10000`

> Two primary beat counts, strict `<`, threshold exactly `9500/10000`.

**Verified.**

Evidence: §14 ("Beat counts and thresholds") specifies exactly two primary beat counts — `beat_count_12_structure = #{ i : attenuation_score_12_perm[i] < attenuation_score_12_observed }` and `beat_count_max_gap = #{ i : max_gap_perm[i] < max_gap_observed }` — both strict `<`, ties do not pass. Locked threshold `9500 / 10000`, strict: `beat_count ≥ 9500` = pass; `beat_count < 9500` = fail. All beat counts are emitted to the verdict log unconditionally.

### 4.12 Verdict map exactly four classes; display names; machine labels

> Verdict map exactly four classes with the §15 display names and `class_1..class_4` machine labels; per-class (a)/(b) wording present verbatim in the verdict log.

**Verified at the design surface.**

Evidence: §15 ("Verdict map and interpretations") defines exactly four mutually exclusive, collectively exhaustive classes with display names `12-centered neighborhood structure` (`class_1`), `Generic substrate smoothness` (`class_2`), `No neighborhood evidence` (`class_3`), `Non-confirmatory / unresolved` (`class_4`), and provides the verbatim two-part `(a) what-it-supports / (b) what-it-does-not-support` language for each, each tagged `REQUIRED-VERBATIM, §15.x{a,b}` in the memo body (verified present at design-memo lines 237, 239, 245, 247, 253, 255, 268, 270). The verdict-log emission machinery does not yet exist as no Cell 1 implementation files are present at lock-acceptance; the verbatim-emission requirement is implementation-gated. The design surface is ratified.

### 4.13 Verbatim caveat / disclosure / anti-rescue clauses

> §15.5 granularity caveat, §15.6 compound/coupled-null disclosure, §20 data-contact disclosure, §21.3 and §21.4 anti-rescue clauses present verbatim in the verdict log.

**Verified at the design surface.**

Evidence: §15.5 (granularity / neighborhood-window caveat, tagged `REQUIRED-VERBATIM, §15.5`, design-memo line 274) closes "This caveat applies to all four verdict classes."; §15.6 (compound-verdict / coupled-null disclosure, tagged `REQUIRED-VERBATIM, §15.6`, line 278); §20 (inherited data-contact disclosure, tagged `REQUIRED-VERBATIM, §20`, line 331, closing "This disclosure is required wording; a hash citation alone does not satisfy it."); §21.3 (Layer 1 / Layer 2 anti-rescue, tagged `REQUIRED-VERBATIM anti-rescue — Layer 1 / Layer 2`, line 337); §21.4 (cross-cell anti-rescue, tagged `REQUIRED-VERBATIM anti-rescue — cross-cell`, line 338). All five blocks are present as single quoted/identified blocks in the memo body. Verdict-log emission is implementation-gated; the design surface is ratified.

### 4.14 Asset-stratified diagnostic seed and permutation count

> Asset-stratified diagnostic (§16) seeded `ASSET_STRAT_DIAG_SEED_CELL1 = 20260519`, `N_PERM = 10000`.

**Verified at the design surface.**

Evidence: §16 ("Diagnostics") specifies the asset-stratified label-permutation diagnostic — permute `is_long` within each asset's index slice, recompute the full `K`-wide median-PSS map, the four focal attenuation scores, and `max_gap` — under locked seed `ASSET_STRAT_DIAG_SEED_CELL1 = 20260519`, `N_PERM = 10000` (explicitly the same count as the primary pool; a smaller diagnostic permutation count is not permitted unless pre-registered, and it is not). Produces `asset_stratified_beat_count_12_structure` and `asset_stratified_beat_count_max_gap`. The diagnostic is non-confirmatory and cannot rescue, upgrade, alter, or convert generic smoothness into 12-centered structure (§16, §21.5). The diagnostic run is implementation-gated; the constants are ratified at the design surface.

### 4.15 Provenance gate against Candidate C `pss_surface_10` / `pss_surface_12`

> Provenance gate (§17) compares recomputed `k=10`/`k=12` 365-anchor surfaces to `protocol_payload.pss_surface_10`/`pss_surface_12` in `results/candidate_c_results_20260515_051236_f3a6bf48.json` at `≤ 1e-12`; failure aborts to Class 4.

**Verified at the design surface.**

Evidence: §17 ("Provenance checks") specifies that Cell 1 recomputes the 365-anchor PSS surfaces for every `k ∈ K = {7, …, 19}`, and because `k = 10` and `k = 12` are members of `K`, Cell 1's recomputed `pss_surface_10` and `pss_surface_12` must reproduce Candidate C's stored surfaces at `max_abs_diff ≤ 1e-12` per anchor, for each of `k = 10` and `k = 12` independently across all 365 anchors. Cell 1 differs from Candidate C here: Candidate C's §11.6 provenance check aborted the run outright on mismatch; Cell 1's §17 specifies that provenance-gate failure is a design-validity failure that routes to Class 4 / `Non-confirmatory / unresolved` (the run aborts and the verdict is Class 4 per §15.4). It is a validity gate, not a diagnostic.

Read-only back-reference confirmation (no row inspection, no PSS recomputation): the stored reference `results/candidate_c_results_20260515_051236_f3a6bf48.json` has SHA-256 `130235fef110cca141fa8873bfa3a6c630a44ac11dfcad953822f41f9cd3c7d4` (matches §17 / §3 citation); JSON path `protocol_payload.pss_surface_10` exists as a 365-entry object with stringified integer DOY keys `"1"`…`"365"`; JSON path `protocol_payload.pss_surface_12` exists as a 365-entry object with stringified integer DOY keys `"1"`…`"365"`. The runtime gate is implementation-gated; the design surface and the static back-references are ratified.

### 4.16 Infrastructure boundary

> Infrastructure boundary (§19): result-defining code in Cell 1 namespace; only `candidate_b_loader` and `candidate_b_rerun_gate` imported as generic utilities.

**Verified at the design surface.**

Evidence: §19 ("Infrastructure and implementation boundary") specifies that all result-defining surface / lens / PSS / attenuation computation must live exclusively in the Cell 1 namespace (`src/influential_numbers_cell_1_lens.py`, `src/influential_numbers_cell_1_pss.py`, `src/influential_numbers_cell_1_protocol.py`, `scripts/run_influential_numbers_cell_1_protocol.py`, with tests `tests/test_influential_numbers_cell_1_{lens,pss,protocol}.py`), must not be imported from Candidate B or Candidate C modules, and that only the generic non-result-defining utilities `candidate_b_loader` (frozen-CSV load + manifest verification) and `candidate_b_rerun_gate` (deterministic double-invocation gate) are imported unchanged. Candidate C's stored `k = 10` / `k = 12` surfaces are an audit-chain provenance check, not a live runtime dependency. No Cell 1 implementation files exist at lock-acceptance; the design surface is ratified.

### 4.17 Candidate C back-references verified by read-only inspection

> Candidate C back-references verified by read-only inspection of C's artifacts in the Coherent Numbers repo: stored surface field names `pss_surface_10` / `pss_surface_12`, verdict-log path, and JSON SHA-256 as cited in §17 — or §17 updated to actual values prior to lock. Read-only inspection only; no analysis, computation, or write.

**Verified.**

Evidence: read-only inspection of Candidate C's artifacts in the Coherent Numbers repo confirmed all back-references prior to this lock-acceptance:

* Verdict-log path `results/candidate_c_results_20260515_051236_f3a6bf48.json` is present at the cited path, committed at `a19b2e9`.
* Verdict-log JSON SHA-256 recomputed as `130235fef110cca141fa8873bfa3a6c630a44ac11dfcad953822f41f9cd3c7d4` — matches the value cited in design-memo §17 and §3 of this artifact.
* Stored surface field `protocol_payload.pss_surface_10` is present, a 365-entry object, all stringified integer DOY keys `"1"`…`"365"` contiguous.
* Stored surface field `protocol_payload.pss_surface_12` is present, a 365-entry object, all stringified integer DOY keys `"1"`…`"365"` contiguous.

The field names `pss_surface_10` / `pss_surface_12`, the verdict-log path, and the JSON SHA-256 cited in design-memo §17 are correct as written; no corrective rewrite of any Cell 1 design-memo section is required as a result of this verification. Verification was a read-only inspection in Claude Code; no analysis, computation, or write operation was performed under this item.

### 4.18 Required-verbatim block register verification

> The eventual closure memo must quote the following blocks character-exactly, each named by its section reference, so closure cannot paraphrase verdict-interpretation-critical language. **All of the following are required-verbatim:**
>
> Per-class support / non-support text: §15.1a, §15.1b, §15.2a, §15.2b, §15.3a, §15.3b, §15.4a, §15.4b.
> Granularity / neighborhood-window caveat: §15.5.
> Compound-verdict / coupled-null disclosure: §15.6.
> Inherited data-contact disclosure: §20.
> Layer 1 / Layer 2 anti-rescue disclosure: §21.3 (treated as closure-critical).
> Cross-cell anti-rescue disclosure (Candidate C independence, Candidate B not-confirmed): §21.4 (treated as closure-critical).
>
> The closure memo must re-emit each of these by section reference; inference or paraphrase is not permitted.

**Verified.**

Evidence: the Required-verbatim block register is present in design-memo §22. Read-only inspection confirms each referenced section anchor exists in the design-memo body, tagged with an explicit `REQUIRED-VERBATIM` marker:

* §15.1a — design-memo line 237; §15.1b — line 239 (Class 1 (a)/(b)).
* §15.2a — line 245; §15.2b — line 247 (Class 2 (a)/(b)).
* §15.3a — line 253; §15.3b — line 255 (Class 3 (a)/(b)).
* §15.4a — line 268; §15.4b — line 270 (Class 4 (a)/(b)).
* §15.5 — line 274 (granularity / neighborhood-window caveat).
* §15.6 — line 278 (compound-verdict / coupled-null disclosure).
* §20 — line 331 (inherited data-contact disclosure).
* §21.3 — line 337 (Layer 1 / Layer 2 anti-rescue, treated as closure-critical).
* §21.4 — line 338 (cross-cell anti-rescue: Candidate C independence, Candidate B not-confirmed, treated as closure-critical).

Thirteen referenced blocks total. The §22 register states explicitly "**All of the following are required-verbatim:**" and "The closure memo must re-emit each of these by section reference; inference or paraphrase is not permitted." The register is internally consistent with the tagged anchors in the body; no corrective rewrite is required. The closure-memo re-emission obligation is gated to the eventual Cell 1 closure artifact; the register itself is ratified here.

## 5. No-data-contact statement

The following negative claims hold as of this lock-acceptance:

* No Cell 1 neighborhood-surface features have been computed against pullback `entry_date`.
* No Cell 1 PSS surfaces (`PSS_k`, `PSS_surface_k`, `median_k`) have been computed for any `k ∈ K = {7, …, 19}`.
* No Cell 1 focal attenuation scores (`slope_f`, `attenuation_score_f`) have been computed for any focal.
* No `max_gap` has been computed.
* No `focal_elevation_gate_12` evaluation has been performed.
* No label permutations have been drawn (neither the primary `LABEL_PERM_SEED_CELL1 = 20260518` pool nor any other).
* No asset-stratified diagnostic (`ASSET_STRAT_DIAG_SEED_CELL1 = 20260519`) has been run.
* No `entry_date` joins, phase-distribution histograms, or sanity-check "previews" have been performed under the Cell 1 design.
* No Cell 1 implementation files or test files exist in the repository as of the lock-acceptance commit.
* No Cell 1 output, verdict-log, or result files exist in the repository.
* No modification, staging, or commit has been performed on the pullback research repository at `/Users/jay/pullback_research`. Pullback HEAD has not been re-inspected since the inventory note (`eac925c`).
* OOS 2023+ has not been accessed in either repo.
* No row-level inspection of any frozen pullback CSV has been performed under Cell 1. The substrate verification in §4.2 hashed file bytes only via `shasum -a 256`; no CSV parser was invoked and no row was loaded. The read-only inspection of Candidate C's verdict-log JSON (§4.15, §4.17) read only `protocol_payload` metadata and surface-key structure; it did not recompute any PSS value and did not inspect any pullback CSV row.

## 6. Lock statement

The Influential Numbers Cell 1 design memo at commit `a765098aa58472fda7080ea08416a4ccf312e16a` is accepted as the locked protocol for Cell 1 — Neighborhood Influence Test. From this point forward, implementation may proceed only under the terms specified in that memo. No design field — the frozen pullback × pooled Phase 3b 1,282-trade substrate (SPY/EFA/EEM/GLD/TLT, 2005–2022, freeze commit `5225bfd`); the multi-focal set `F = {10, 12, 14, 16}`; the primary focal `12`; the control focals `10, 14, 16`; the `±3` linear-integer window `W(f) = {f−3, …, f+3}`; the bucket-count universe `K = {7, …, 19}`; the median PSS over the 365-anchor surface per bucket count; the focal-centered continuous-attenuation statistic `attenuation_score_f = −slope(median_k ~ |k − f|)` over the seven window points with distance multiset `{0,1,1,2,2,3,3}`, focal included; the strict-`>` focal-elevation gate for 12 against the mean of its six non-focal window neighbors; the `max_gap = attenuation_score_12 − max(attenuation_score_10, attenuation_score_14, attenuation_score_16)` contrast; the single shared `N_PERM = 10,000` unstratified pooled `is_long` permutation null; the locked seed `LABEL_PERM_SEED_CELL1 = 20260518`; the asset-stratified diagnostic seed `ASSET_STRAT_DIAG_SEED_CELL1 = 20260519` with `N_PERM = 10,000`; the two primary beat counts `beat_count_12_structure` and `beat_count_max_gap` with the `9,500/10,000` strict-`<` ties-do-not-pass threshold; the hard-binary Class 4 with no marginal band (a near-threshold beat count below 9,500 is a fail routed to Class 3, never Class 4); the four-class verdict map with display names `12-centered neighborhood structure`, `Generic substrate smoothness`, `No neighborhood evidence`, `Non-confirmatory / unresolved` and machine labels `class_1..class_4`; the Required-verbatim block register (§15.1a, §15.1b, §15.2a, §15.2b, §15.3a, §15.3b, §15.4a, §15.4b, §15.5, §15.6, §20, §21.3, §21.4); the asset-stratified diagnostic as a non-verdict diagnostic that cannot rescue, upgrade, or alter the verdict; the §17 provenance gate against Candidate C's stored `protocol_payload.pss_surface_10` and `protocol_payload.pss_surface_12` in `results/candidate_c_results_20260515_051236_f3a6bf48.json` at `max_abs_diff ≤ 1e-12` per anchor for each of `k = 10` and `k = 12`, with failure as a design-validity failure routing to Class 4; and the §19 infrastructure boundary requiring result-defining code in the Cell 1 namespace with only the generic `candidate_b_loader` / `candidate_b_rerun_gate` imports — may be changed without a new amendment artifact and its own audit trail. Analysis is authorized only after this lock-acceptance artifact is committed.

## 7. Post-lock authorization boundary

From the commit that records this artifact, the following actions become authorized within the locked terms:

* Implementation modules for the Cell 1 lens (parameterized §7.1 / §7.2 phase formula with assertion-and-abort range check on `phase ∈ {0..k-1}`), the §9.1 `PSS_k` statistic (η²-form with `total_k = 0` `DegenerateLongShareError` abort), the §10 attenuation statistic, the §11 focal-elevation gate, and the §12 `max_gap` contrast may be written in the Cell 1 namespace, including a `tests/test_influential_numbers_cell_1_lens.py` no-`%` grep gate test parallel to Candidate B/C's.
* Frozen pullback CSV files at the manifest's recorded destination paths may be loaded under the §17 triple hash-verification pattern via the generic `candidate_b_loader`.
* `entry_date` may be mapped to `(k, d, phase)` triples via §7.2 for `k ∈ K = {7, …, 19}` and `d ∈ 1..365`, and the `K`-wide `median_k` map computed.
* The four focal attenuation scores, the `focal_elevation_gate_12`, and `max_gap` may be computed per §10–§12.
* The §13 primary shared-permutation pool (`N_PERM = 10,000`, `LABEL_PERM_SEED_CELL1 = 20260518`) and the §16 asset-stratified diagnostic pool (`N_PERM = 10,000`, `ASSET_STRAT_DIAG_SEED_CELL1 = 20260519`) may be drawn, and the two primary beat counts plus the two diagnostic beat counts computed.
* The §17 provenance gate against Candidate C's stored `protocol_payload.pss_surface_10` and `protocol_payload.pss_surface_12` is enforced at run time at `≤ 1e-12` per anchor for each of `k = 10` and `k = 12`; failure is a design-validity failure that routes the verdict to Class 4.
* The verdict log may eventually be generated — after the implementation commit and the locked run — containing the two primary beat counts unconditionally, the verdict class per §15 decision rules, and the verbatim §15.5 granularity caveat, §15.6 compound/coupled-null disclosure, §20 data-contact disclosure, and §21.3 / §21.4 anti-rescue clauses.

The following remain prohibited:

* No design field may be changed after observing results. The locked field list is enumerated in §6 above.
* OOS 2023+ remains sealed in both repos and may not be accessed.
* The pullback research repository at `/Users/jay/pullback_research` may not be modified. Re-inspection is permitted as a provenance note only; drift does not block a Cell 1 run whose frozen-CSV digests match the manifest, and the matching frozen-CSV digests are the authoritative run substrate per §17.
* Layer 2 (divisor, multiple, 12-family/duodecimal, harmonic-family, recursive-field, or weighted-neighbor influence) may not be added as a "diagnostic" or anywhere else, may not be used to rescue a Class 2/3/4 verdict, and may not borrow authority from the Kryon source. Any Layer 2 follow-up requires a separate decision memo argued on its own grounds (design-memo §21.3).
* Candidate C's `12-privileged` verdict may not be retroactively reinterpreted by any Cell 1 outcome. Candidate B's split-null equinox result remains not confirmed and may not be rescued, confirmed, or reinterpreted by any Cell 1 outcome (design-memo §21.4).
* No additional verdict heads beyond the four classes in §15 may be registered. The verdict class is determined exclusively by the focal-elevation gate and the two primary beat counts applied to the §15 rules; no diagnostic may upgrade or alter the class.
* No secondary diagnostic (§16) may rescue, upgrade, alter, or convert generic smoothness into 12-centered structure. The no-rescue rule is absolute; a Class 3 or Class 4 verdict remains so regardless of diagnostic pattern.
* No focal centers outside `F = {10, 12, 14, 16}`, no bucket counts outside `K = {7, …, 19}`, and no window other than `±3` may be introduced under this cell.
* No result-defining surface / lens / PSS / attenuation code may be imported from Candidate B or Candidate C modules; only the generic `candidate_b_loader` and `candidate_b_rerun_gate` utilities may be imported.

## 8. Final state

* Design memo locked at commit `a765098aa58472fda7080ea08416a4ccf312e16a`. File SHA-256: `90e56a5318afcc25c5444fcc5cee911927c86afb41a71b2f3948b8335e28df84`.
* Frozen-CSV substrate verified at the freeze manifest from commit `5225bfd`; all six recorded digests match recomputed digests at the manifest's destination paths (§4.2).
* Candidate C provenance back-references verified read-only: verdict-log path `results/candidate_c_results_20260515_051236_f3a6bf48.json`, JSON SHA-256 `130235fef110cca141fa8873bfa3a6c630a44ac11dfcad953822f41f9cd3c7d4`, and the present 365-entry `protocol_payload.pss_surface_10` / `protocol_payload.pss_surface_12` objects (§4.15, §4.17).
* No Cell 1 implementation, tests, or output files exist in the repository.
* No Cell 1 analysis has been executed; no PSS surface, attenuation score, gate, max-gap, or permutation has been computed against any data.
* The next artifact in the audit chain is implementation + tests, not a design revision. Any revision to the locked design surface requires a dated amendment artifact and its own commit.

— end of lock-acceptance draft v0.1 (clean review copy; no repo file written; nothing lock-accepted) —
