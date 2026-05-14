# Coherent Numbers v0.2 — Candidate B Design Memo (Pullback × Harmonic Calendar)

**Version:** v0.1 (draft for review — final tightening pass)
**Date:** 2026-05-14
**Project:** Coherent Numbers
**Cell:** Candidate B — pullback × harmonic-calendar modulation
**Status:** Pre-registration draft. Protocol not yet locked. No harmonic-calendar features have been computed against pullback `entry_date`. No phase-conditional statistics on Phase 3b data exist.

---

## 1. Purpose

This memo locks the protocol for Candidate B, the v0.2 Microscope Program cell selected in the v0.2 Cell-Selection Decision Memo (`docs/cell_selection_decision_memo_v0.2.md`, commit `5c30f5d`). Candidate B tests whether a 12-phase March-20-anchored annual-sector calendar lens explains heterogeneity inside a frozen, audit-locked pullback-event population produced by the separate pullback research program.

Candidate B is **not** a re-discovery of the pullback signal. The pullback signal is the substrate; the question is whether the harmonic-calendar lens reveals additional within-population structure.

## 2. Inheritance from v0.2 cell-selection memo

The following decisions are inherited and not re-opened here:

- The pullback substrate is treated as frozen raw data inside Coherent Numbers. The pullback repo is not touched.
- OOS 2023+ remains sealed in both repos and is out of scope for B.
- The prior data-contact disclosure language is load-bearing (§13).
- Candidate B is a design-and-freeze sequence; no harmonic-calendar features may be joined to `entry_date` before this memo is locked.

The freeze itself has occurred. The candidate-relevant pullback populations are present in Coherent Numbers under their frozen CSV hashes per commit `5225bfd`. The frozen CSV hashes — not the pullback repo HEAD — are the run substrate (see §15).

## 3. Population scope

**Primary (confirmatory):** the pooled Phase 3b 5-asset population — SPY, EFA, EEM, GLD, TLT — 1,282 trades total, produced under identical `BacktestParams` at pullback commit `7806a6d` over the common window 2005-01-01 – 2022-12-31.

**Secondary (diagnostic, non-confirmatory):**

- SPY 301-trade base population (canonical: `runs/20260505_152451/trades.csv`) — used only for diagnostic continuity with prior SPY/GLD harmonic-calendar cells. Cannot rescue the primary verdict.
- Per-asset breakdowns over the Phase 3b 5-asset universe — diagnostic only.

The primary verdict is computed exclusively on the pooled Phase 3b 1,282-trade population.

## 4. Primary outcome

`PSS_B1` — phase-conditional long-share dispersion across the 12 annual phases on the pooled Phase 3b 1,282-trade population, expressed as the η²/correlation-ratio form for a binary outcome. Defined formally in §9.1 / Appendix B.1.

Choice rationale: pullback Phase 3b's reported edge appeared at the long/short allocation level versus a 50/50 random baseline, not at within-direction timing. The primary lens-modulation outcome inherits that structural finding rather than fighting it.

## 5. Reduced analytical row schema

Each analytical row corresponds to one frozen pullback trade. Per-row fields:

- `trade_id` — stable identifier within the frozen artifact.
- `asset` — one of `{SPY, EFA, EEM, GLD, TLT}`.
- `entry_date` — primary phase-assignment date (calendar-day granularity, exchange tz of the frozen artifact).
- `exit_date`.
- `is_long` — boolean direction label.
- `r_multiple` — signed trade outcome as recorded in the frozen artifact (see B.2).
- `frozen_artifact_id` — pointer to the manifest entry for this trade's source CSV.

`source_sha256` is **dataset-level provenance**, recorded once per frozen CSV in the freeze manifest. It is not a per-row analytical field. The manifest is loaded for provenance verification at run start, not joined into the analytical row set.

## 6. Frozen-data provenance

Provenance is the freeze manifest (committed under `5225bfd`). Each frozen pullback CSV is identified by its filesystem path inside Coherent Numbers and its SHA-256 digest. At run start, the analysis script:

1. Reads the manifest.
2. Recomputes SHA-256 of each referenced CSV.
3. Aborts if any digest mismatches.

This is the run substrate. The pullback repo's HEAD is not consulted at run time (§15).

## 7. Calendar lens — 12-phase March-20 annual-sector partition

Candidate B uses **12 annual sectors** of an annual cycle anchored at **March 20**. This shares the March-20 anchor with the prior SPY and GLD harmonic-calendar cells, but uses a different **annual-sector 12-phase lens** rather than the 108-phase ≈ 3.38-day-bucket lens of those cells. The adaptation is deliberate and is justified in §8.

### 7.1 Phase assignment formula

For a given trade with `entry_date`:

1. **Locate the relevant annual cycle.**
   - If `entry_date >= date(entry_date.year, 3, 20)`:
     `cycle_start = date(entry_date.year, 3, 20)`
   - Otherwise:
     `cycle_start = date(entry_date.year - 1, 3, 20)`
   - `cycle_end = date(cycle_start.year + 1, 3, 20)`

2. **Compute the within-cycle position.**
   - `cycle_length_days = (cycle_end - cycle_start).days`  *(365 or 366)*
   - `days_since_start  = (entry_date - cycle_start).days`

3. **Assign phase.**
   - `phase = floor( days_since_start * 12 / cycle_length_days )`
   - **Assert** `phase ∈ {0, 1, ..., 11}`. If the assertion fails, the run **aborts**. There is no silent clamp.

   An out-of-range `phase` indicates a bug in cycle arithmetic or in the input data (e.g., `entry_date` outside its located cycle). Such conditions must fail loudly. For all valid `entry_date` values inside `[cycle_start, cycle_end)`, the assertion holds by construction.

4. **Labels.** Integer `0..11`. Phase 0 begins on March 20 of `cycle_start.year`.

### 7.2 Properties

- Each phase is an **annual sector** of approximately `cycle_length_days / 12 ≈ 30.42–30.50` days. There is no `% 12` day-of-year residue. The lens does **not** create a 12-day modular repeating cycle.
- Leap years are handled automatically: a leap cycle yields `cycle_length_days = 366` and sector width ≈ 30.5 days; a non-leap cycle yields 365 and ≈ 30.42 days. No leap-day excision, no leap-day reassignment.
- The lens is fully determined by `entry_date` alone. No exit-date, holding-period, or trade-internal information enters phase assignment.
- The lens is deterministic. Given `(entry_date, anchor_month, anchor_day, bucket_count)`, `phase` is exact.

### 7.3 Anchor

`anchor_month = 3`, `anchor_day = 20`. Fixed civil-date proxy for the vernal equinox, consistent with the SPY and GLD cells. No alternative anchor is considered after data contact except via the §10 exhaustive 365-DOY anchor-control null.

### 7.4 Primary assignment date

`entry_date`. `exit_date` is not used for phase assignment. Holding-period effects are absorbed into the per-trade `r_multiple` outcome (B.2) and are not lens-relevant.

## 8. 12-phase vs 108-phase — bucket-count adaptation

The prior SPY and GLD harmonic-calendar cells used a 108-phase lens (≈ 3.38-day buckets) against ~30 years of daily-bar data. Candidate B uses a **12-phase annual-sector** lens against the 1,282-trade event population.

Two points must be clear:

1. **Sample-mass argument.** With 1,282 event-level observations spread over an annual cycle, a 108-bucket partition would average ≈ 12 trades per bucket — too few for a stable per-phase statistic, especially under the asset and direction stratifications used as diagnostics. A 12-bucket partition averages ≈ 107 trades per phase, sufficient for the long-share statistic that drives the primary verdict.

2. **Lens-family clarification.** B's 12 phases are **annual sectors** — each phase is a contiguous ≈30-day window of the solar year, anchored at March 20. They are **not** a 12-day modular residue cycle. The lens family is the same family as the 108-phase cell (annual harmonic partition anchored at March 20); only the bucket count differs.

The 12-phase bucket count is a deliberate, pre-registered lens adaptation to the event-population sample size. It is not a free parameter to be tuned, and is not changed after data contact.

## 9. Primary outcome definitions

### 9.1 PSS_B1 — phase-conditional long-share dispersion (primary, η²-form)

Let `N_p` be the count of trades in phase `p` (`p ∈ 0..11`) on the pooled Phase 3b 1,282-trade population, and let `L_p` be the count of long trades in phase `p`. Let `N_total = Σ_p N_p` and `share_pooled = (Σ_p L_p) / N_total`. Define `share_p = L_p / N_p` for phases with `N_p > 0` (phases with `N_p = 0` contribute zero to the between-sum).

Then:

```
between_B1 = Σ_p ( N_p / N_total ) × ( share_p − share_pooled )²
total_B1   = share_pooled × ( 1 − share_pooled )
PSS_B1     = between_B1 / total_B1
```

Properties:

- `PSS_B1` is the **η² / correlation-ratio** form of phase-conditional dispersion for a binary outcome. It is the same family as the η² used by the prior SPY/GLD cells, specialized to a binary outcome (`is_long`).
- `PSS_B1` is bounded in `[0, 1]` whenever `total_B1 > 0`.
- If `total_B1 = 0` — i.e., the pooled population contains only longs or only shorts — allocation heterogeneity is undefined. In that case the run **aborts** and reports the degenerate-population condition. No fallback estimand is substituted.
- Because `total_B1` is fixed for the frozen population (the `is_long` marginal is invariant under both N.1 unstratified permutation and the N.2 anchor-shifted phase assignment), the normalized form `PSS_B1` and the unnormalized `between_B1` produce identical rank orderings of the observed value against either null. The normalized form is adopted to preserve continuity with the η²/PSS conventions of prior cells.

### 9.2 Secondary outcome: signed r-multiple dispersion (diagnostic only)

`PSS_B2` is defined on per-phase mean `r_multiple` in the conventional η² form (see B.2). Diagnostic only. Cannot drive the primary verdict.

## 10. Null hypotheses and finite controls

Two nulls are pre-registered. **N.1 is the primary label-permutation null and N.2 is the primary anchor-control null. Together they drive the confirmatory verdict.**

### 10.1 N.1 — Unstratified label-permutation null (primary)

Procedure:

1. Take the pooled Phase 3b 1,282-trade population with its assigned phases (from §7).
2. Independently and uniformly shuffle the `is_long` label across **all 1,282 trades, ignoring asset**. Phase labels and asset labels are held fixed; only the `is_long` vector is permuted.
3. Recompute `PSS_B1` on the permuted labels.
4. Repeat for `N_PERM = 10,000` permutations with a pre-registered seed `LABEL_PERM_SEED = 20260514`.

This tests whether the observed phase-conditional long-share dispersion is more extreme than expected if direction labels were assigned randomly across the pooled frozen event population, with no respect for asset.

Asset-stratified label permutation is **not** the primary null. It is moved to controls/diagnostics (§11.3) and asks a different question (does any pooled effect persist if each asset's long/short mix is preserved?). The primary verdict is unstratified.

### 10.2 N.2 — Exhaustive 365-DOY anchor-control null (primary)

**B adopts the v0.3.3 exhaustive-enumeration discipline as its initial standard, not via amendment. No sampling-based anchor control is permitted at any phase of B's lifecycle.**

For each integer day-of-year anchor `d ∈ 1..365`, define the anchor-shifted lens:

For a given trade with `entry_date`:

1. Compute the candidate cycle start as if the anchor were DOY `d`:
   - `anchor_in_year(y) = date(y, 1, 1) + timedelta(d - 1)`
   - If `entry_date >= anchor_in_year(entry_date.year)`:
     `cycle_start_d = anchor_in_year(entry_date.year)`
   - Otherwise:
     `cycle_start_d = anchor_in_year(entry_date.year - 1)`
   - `cycle_end_d = anchor_in_year(cycle_start_d.year + 1)`

2. `cycle_length_days_d = (cycle_end_d - cycle_start_d).days`
   `days_since_start_d  = (entry_date - cycle_start_d).days`

3. `phase_d = floor( days_since_start_d × 12 / cycle_length_days_d )`. Assert `phase_d ∈ {0..11}`; abort on assertion failure (same discipline as §7.1 step 3).

4. Compute `PSS_B1_d` on the unpermuted `is_long` labels using `phase_d`, in the η²-form of §9.1.

The null distribution is the exhaustively enumerated population of 365 `PSS_B1_d` values, one per integer DOY anchor `d ∈ 1..365`. No `% 12` residue logic appears anywhere. No random sampling. No seed is consumed.

DOY 79 (the closest integer-DOY twin of March 20 in non-leap years) is **retained** in this 365-anchor population, following the v0.3.3 finite-control discipline. The candidate's `date(y, 3, 20)` anchor and the DOY-79 anchor differ by one day in leap years and are not identical.

**Leap-year / 365-anchor note.** The control intentionally enumerates integer DOY anchors `d ∈ 1..365`. **February 29 is not a separate anchor.** This follows the prior-cell finite-control convention (v0.3.1 / v0.3.3) of using a 365-element DOY axis. Leap years still affect `cycle_length_days_d` through the annual-sector formula in step 2 of §10.2; the leap-day's effect enters via cycle length, not via an additional anchor.

### 10.3 Beat-count statistics

Both nulls are summarized as **strict beat counts** against the observed `PSS_B1`:

- `beat_count_perm   = #{ N.1 permutation PSS_B1 values strictly less than observed PSS_B1 }`
- `beat_count_anchor = #{ N.2 anchor-control PSS_B1_d values strictly less than observed PSS_B1 }`

Ties are not counted toward beat counts. Reported percentiles (`beat_count / N_total_null`) are descriptive only; verdict thresholds (§12) are integer beat counts.

## 11. Controls and diagnostics (non-confirmatory)

The following are reported but do **not** affect the primary verdict.

### 11.1 Gregorian civil-month control

`PSS_GREG_MONTH` is `PSS_B1` recomputed using calendar month of `entry_date` as the phase label (12 buckets).

**Independence caveat.** A 12-phase March-20 annual-sector partition and a Gregorian-month partition are both approximately monthly partitions, offset by roughly 19 days. `PSS_GREG_MONTH` is not independent evidence beyond the §10.2 anchor-control family — it is one civil-calendar point within that family's neighborhood. It is best understood as a **familiar civil-calendar benchmark for human readability, not as independent confirmatory evidence**. Its diagnostic value is interpretive, not confirmatory.

### 11.2 January-anchored 12-sector control (auxiliary)

`PSS_JAN` is `PSS_B1` recomputed with `anchor_month = 1, anchor_day = 1` using the §7 annual-sector formula. Same family as N.2, kept for readability continuity with prior cells.

### 11.3 Asset-stratified label-permutation diagnostic

Re-runs the N.1 procedure with `is_long` shuffled **within each asset's trades** rather than pooled. The number of permutations is `N_PERM = 10,000`, seeded by a separate pre-registered seed `ASSET_STRAT_DIAG_SEED = 20260515` (see §14). Asks: does any pooled phase-conditional long-share effect persist when each asset's long/short mix is preserved?

Reported alongside N.1; does not enter the verdict. Used in the post-verdict interpretation rule of §12.4.

### 11.4 Per-asset PSS_B1

Reported for each of `{SPY, EFA, EEM, GLD, TLT}` individually. Diagnostic only.

### 11.5 Phase-cell occupancy

Per-phase trade counts `N_p` and longs counts `L_p` reported as descriptive texture. Not a screen.

## 12. Verdict map

### 12.1 Thresholds

The verdict is determined exclusively by the two integer beat-count thresholds:

- **Permutation threshold (N.1):** `beat_count_perm ≥ 9500` (observed `PSS_B1` strictly beats at least 9,500 of 10,000 permuted PSS values).
- **Anchor-control threshold (N.2):** `beat_count_anchor ≥ 347` (observed `PSS_B1` strictly beats at least 347 of 365 DOY anchors; `347 = ceil(0.95 × 365)`).

### 12.2 Three-class verdict map

| Verdict | Condition |
|---|---|
| **Confirmatory** | `beat_count_perm ≥ 9500` **and** `beat_count_anchor ≥ 347` |
| **Split-null**   | exactly one of the two thresholds passes |
| **Non-confirmatory** | neither threshold passes |

### 12.3 Interpretation of Split-null

Split-null is *informative texture*. It is **not** a confirmatory result, **not** a partial pass, and **not** an invitation to amend the design, add hypotheses, or re-tune the lens. It is reported with the same rigor as the other two classes and interpreted as a flag that the two nulls disagreed about the same observed value — descriptively useful, evidentially inconclusive.

No "top quintile" or "near-miss informative-fail" band exists. There is no 95th-percentile language outside the explicit integer beat-count thresholds above.

Secondary outcomes (`PSS_B2`, per-asset, civil-month, January-anchor, asset-stratified permutation) cannot rescue or upgrade the verdict. A Non-confirmatory primary outcome stays Non-confirmatory regardless of secondary patterns.

### 12.4 Pooled estimand: required interpretation rule

The primary confirmatory verdict tests **pooled phase-conditional allocation structure** on the 1,282-trade Phase 3b population. The unstratified N.1 null and the unstratified pooled outcome together define a pooled estimand.

The following interpretation rule is binding on the verdict text:

- A Confirmatory primary result does **not** by itself establish that the same phase-conditional allocation structure holds within each asset.
- A Confirmatory primary result may, in principle, reflect **asset-composition-mediated structure**: phase-to-asset-mix variation combined with cross-asset differences in long/short mix can generate pooled phase-conditional long-share dispersion without any within-asset modulation.
- The asset-stratified permutation diagnostic (§11.3) is the interpretive instrument for this distinction. It asks whether the pooled effect persists when each asset's long/short mix is preserved.
- **If the primary is Confirmatory but the asset-stratified diagnostic is weak** (i.e., observed `PSS_B1` is not unusual against the asset-stratified permutation null at the same beat-count discipline as N.1), the verdict text **must** describe the finding as **pooled-population modulation**, not as within-asset modulation. The Confirmatory label is preserved (the diagnostic cannot demote the verdict), but the verdict's plain-language description is constrained.
- If the primary is Confirmatory and the asset-stratified diagnostic is also strong, the verdict text may describe the finding as pooled-population modulation that persists under per-asset mix conditioning, while remaining careful not to over-claim per-asset modulation without per-asset confirmatory tests.

This rule shapes verbalization, not the verdict bit. The verdict bit is determined solely by §12.1–12.2.

## 13. Data-contact disclosure (required wording)

Verbatim wording carried from `docs/cell_selection_decision_memo_v0.2.md` §11, and required in B's verdict:

> Candidate B's verdict is conditional on a previously contacted, audit-frozen pullback-event population. The pullback Phase 1–3b series for SPY and the Phase 3b 2005–2022 series for SPY/EFA/EEM/GLD/TLT were inspected, partitioned, and used to estimate within-population statistics during pullback research before Coherent Numbers contacted them. The pullback `BacktestParams` were locked early at pullback commit `50ee2d1` and not re-tuned, which limits but does not eliminate this exposure. OOS 2023+ remains sealed and is out of scope for B.

This disclosure is required wording. A hash citation alone does not satisfy it.

## 14. Reproducibility requirements and seeds

- All randomness in this protocol resides in N.1 and the §11.3 asset-stratified diagnostic. Both use `N_PERM = 10,000`.
- **`LABEL_PERM_SEED = 20260514`** is used for N.1 (unstratified pooled permutation).
- **`ASSET_STRAT_DIAG_SEED = 20260515`** is used for the §11.3 asset-stratified permutation diagnostic.
- The two seeds are distinct by design so that the diagnostic's permutation sequence is not a sub-sample of the primary null's permutation sequence. Both are locked at this memo's adoption.
- N.2 is deterministic and exhaustive over `d ∈ 1..365`. No seed is consumed.
- §7 phase assignment is deterministic given `(entry_date, anchor_month=3, anchor_day=20, bucket_count=12)`.
- The frozen-CSV provenance verification (§6) is performed at run start. Mismatch aborts the run.

A clean run from a clean checkout of Coherent Numbers at the memo-lock commit must reproduce `PSS_B1`, both beat counts, and the verdict bit-for-bit.

## 15. Substrate: frozen CSV hashes, not pullback HEAD

Following the freeze commit `5225bfd`, the Candidate B run substrate is the set of **frozen CSV SHA-256 digests** recorded in the Coherent Numbers freeze manifest. The pullback research repo's HEAD is **not** part of the run substrate.

- The pullback HEAD at inventory time was `eac925c`. This is a historical fact recorded in `docs/cell_selection_decision_memo_v0.2.md` §4. It is not a run-time precondition for Candidate B.
- If the pullback repo is ever re-inspected and drift from `eac925c` is detected, that drift is recorded as a provenance note but does **not** block a Candidate B run whose frozen-CSV digests match the manifest.
- Conversely, if the frozen-CSV digests do **not** match the manifest, the run aborts regardless of pullback HEAD state.

This decouples Candidate B from any future activity in the separate pullback audit chain.

## 16. Guardrails (pre-lock and through run)

- No harmonic-calendar features may be computed against pullback `entry_date` before this memo is locked.
- No phase-distribution sanity checks, histograms, or "preview" joins before lock. A preview is a computation.
- No re-opening of population scope, lens family, anchor, bucket count, primary outcome, null definitions, or beat-count thresholds after lock.
- No OOS 2023+ access. No modifications to the pullback repo.
- Secondary outcomes are reported but cannot rescue the primary verdict.
- No sampling-based anchor control may be reintroduced at any point in B's lifecycle (§10.2).

## 17. Pre-lock checklist

The following must hold at the moment of design-lock commit:

- [ ] **Working tree is clean of non-ignored modified or untracked files.** Files covered by `.gitignore` may exist locally but are not part of the audit state.
- [ ] Frozen-CSV manifest from commit `5225bfd` is intact; all referenced CSVs are present and digests match.
- [ ] Reduced row schema (§5) is final; `source_sha256` is dataset-level only.
- [ ] §7 phase formula is the **annual-sector** formula; no `% 12` day-residue logic appears anywhere in the memo or in code. The §7.1 step-3 phase-range check is implemented as an **assertion that aborts the run** on failure, not as a silent clamp.
- [ ] §9.1 `PSS_B1` is the η²/correlation-ratio form `between_B1 / total_B1`, with the `total_B1 = 0` abort rule in force.
- [ ] N.1 is **unstratified** label permutation across the pooled 1,282-trade Phase 3b population (§10.1).
- [ ] N.2 uses the §7 annual-sector formula with anchor swapped to integer DOY `d ∈ 1..365`, exhaustively enumerated, with no sampling permitted (§10.2).
- [ ] Verdict map is exactly the three-class map in §12.2 with `beat_count_perm ≥ 9500` and `beat_count_anchor ≥ 347`. No quintile band, no 95th-percentile prose untied to integer beat counts.
- [ ] Pooled-vs-within-asset interpretation rule (§12.4) is present and binds the verdict text.
- [ ] `PSS_GREG_MONTH` independence caveat present (§11.1).
- [ ] Data-contact disclosure wording present verbatim (§13).
- [ ] `LABEL_PERM_SEED = 20260514` and `ASSET_STRAT_DIAG_SEED = 20260515` locked, with `N_PERM = 10,000` (§14).
- [ ] Substrate clause names frozen-CSV hashes (not pullback HEAD) as run substrate (§15).

The previously-listed checklist item requiring the pullback repo HEAD to equal `eac925c` at run time is **removed**. It is replaced by the frozen-CSV digest check above, consistent with §15.

---

## Appendix A — Variable glossary

- `entry_date` — calendar date a pullback trade entered the market, as recorded in the frozen CSV.
- `is_long` — boolean direction label as recorded in the frozen CSV.
- `r_multiple` — signed trade outcome as recorded in the frozen CSV (see B.2).
- `phase` — integer `0..11` produced by §7.
- `N_p`, `L_p` — per-phase trade count and per-phase long-trade count on the pooled Phase 3b population.
- `N_total`, `share_pooled` — pooled total trade count and pooled long share.
- `between_B1`, `total_B1`, `PSS_B1` — η²-form primary outcome components (§9.1).
- `beat_count_perm`, `beat_count_anchor` — strict beat counts defined in §10.3.
- `LABEL_PERM_SEED = 20260514`, `ASSET_STRAT_DIAG_SEED = 20260515`, `N_PERM = 10,000` — seeds and permutation count (§14).

## Appendix B — Outcome conventions

### B.1 Long-share, η²-form

Per-phase long-share `share_p = L_p / N_p` on the pooled 1,282-trade Phase 3b population (phases with `N_p = 0` contribute zero to `between_B1`). Pooled mean `share_pooled = Σ L_p / N_total`. Between-sum, total, and ratio are defined in §9.1. `PSS_B1` is the η²/correlation-ratio of phase against the binary `is_long` outcome and is bounded in `[0, 1]` when `total_B1 > 0`. The run aborts when `total_B1 = 0`.

### B.2 Signed `r_multiple` (single convention)

`r_multiple` is used **exactly as recorded in the frozen pullback CSV**. The recorded `r_multiple` is the already-signed trade outcome — positive for favorable trade resolution, negative for adverse — relative to each trade's directional intent. It is **not** multiplied by `is_long`, **not** re-signed, and **not** transformed.

There is one convention only. Long trades and short trades both contribute their recorded signed `r_multiple` directly to any `r_multiple`-based diagnostic. Any future convention change requires a new design memo.

## Appendix C — Diagnostics

C.1 — Per-phase trade counts `N_p` and longs `L_p`. Descriptive only.

C.2 — Per-asset `PSS_B1` (§11.4). Diagnostic only.

C.3 — Asset-stratified label-permutation null (§11.3), seeded by `ASSET_STRAT_DIAG_SEED = 20260515`. Diagnostic only; feeds the §12.4 interpretation rule but not the verdict bit.

C.4 — Direction-aware diagnostics. Reported as **either** (a) per-phase directional counts `(L_p, N_p − L_p)` for descriptive long/short occupancy, **or** (b) within-direction `r_multiple` diagnostics computed separately on the long sub-population and the short sub-population (per-phase mean `r_multiple` among longs; per-phase mean `r_multiple` among shorts). C.4 cannot rescue the primary verdict; it exists to describe whether any observed structure is concentrated on one side of the direction split. Long-share as a directional ratio is not meaningful within a direction-restricted sub-population and is not used in C.4.

— end of tightened draft —
