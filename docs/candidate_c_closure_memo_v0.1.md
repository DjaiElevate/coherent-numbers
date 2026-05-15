# Candidate C Closure Memo — v0.1

**Version:** v0.1 (Closure)
**Date:** 2026-05-15
**Project:** Coherent Numbers
**Cell:** Candidate C — 12 vs 10 bucket-count comparison
**Status:** Closed
**Verdict:** 12-privileged

**Reference commits**

* Design memo (locked): `401ce45` — `docs/candidate_c_design_memo_v0.1.md`
* Lock-acceptance: `dc97576` — `docs/candidate_c_design_memo_v0.1_lock_acceptance.md`
* Freeze: `5225bfd` — `docs/pullback_population_freeze_manifest_v0.1.md`
* Implementation + tests: `4432591`
* Locked verdict run: `a19b2e9`

**Verdict artifacts**

* JSON: `results/candidate_c_results_20260515_051236_f3a6bf48.json` (SHA-256: `130235fef110cca141fa8873bfa3a6c630a44ac11dfcad953822f41f9cd3c7d4`)
* Markdown sidecar: `results/candidate_c_results_20260515_051236_f3a6bf48.md` (SHA-256: `baeba42d192faa22986b1666df1d63b67cab094136bd5f01782b1677191be8b1`)
* `rerun_verification_digest`: `f3a6bf48f7266c2d654dac36f79d38825f14f727d20aeead98e204463a39f762`

---

## 1. Executive summary

Candidate C found that the 12-bucket annual-sector partition is distinguished from the 10-bucket partition on the pooled Phase 3b 1,282-trade substrate under symmetrical 365-DOY anchor-surface rules. The directed comparison statistic clears the locked threshold (`beat_count_comparison_12 = 9973/10000`), and both bucket counts individually clear their own nulls at `10000/10000`. The locked verdict map (memo §12.2) classifies the result as 12-privileged (Class 1).

The bounded scope of this verdict is non-negotiable. Per the verbatim §12.2(b) and §12.4 disclosures recorded in the verdict log, the result does not establish 12 as uniquely privileged among all bucket counts (only 10 was tested), does not attribute the privilege to a duodecimal property as opposed to a substrate-specific feature at this temporal resolution, does not rescue Candidate B's equinox hypothesis, and does not generalize beyond the pre-registered substrate. The comparison is between two different temporal resolutions (≈30.4 days/bin for k=12 vs ≈36.5 days/bin for k=10), not a test of which resolution is "correct" in any absolute sense.

## 2. Locked protocol recap

* **Population.** Pooled Phase 3b 5-asset population — SPY/EFA/EEM/GLD/TLT — 1,282 trades, 2005–2022, frozen at `5225bfd` per `docs/pullback_population_freeze_manifest_v0.1.md`. Inherited from Candidate B unchanged (memo §3, §5; lock-acceptance §4.3).
* **Lens.** Parameterized annual-sector partition over k ∈ {12, 10} (memo §7). 365-DOY exhaustive anchor surface (memo §7.4). Civil-date March-20 anchor in §7.1; DOY-shifted anchors in §7.2. Inherited convention: DOY 60 in leap years coincides with Feb 29 (memo §7.3, §17, lock-acceptance §4.7).
* **PSS statistic.** η²/correlation-ratio `PSS_k = between_k / total_k` parameterized by k (memo §9.1). `total_k = 0` raises `DegenerateLongShareError` and aborts the run.
* **Primary statistic.** Median PSS over the 365-anchor surface, per bucket count: `median_12`, `median_10`. Directed comparison `diff = median_12 − median_10` (memo §9.2, §9.3).
* **Nulls.** Three coupled distributions derived from one shared pool of `N_PERM = 10,000` unstratified pooled `is_long` permutations (memo §10.1, §10.2). Seed `LABEL_PERM_SEED_C = 20260516`.
* **Beat counts.** Four (`beat_count_12_individual`, `beat_count_10_individual`, `beat_count_comparison_12`, `beat_count_comparison_10`), strict `<`, ties do not pass (memo §10.3).
* **Verdict map.** Four mutually exclusive and collectively exhaustive classes: 12-privileged, 10-privileged, Tied / both-structured, Non-confirmatory / unresolved (memo §12.2). Threshold `9500/10000` on all four beat counts.
* **Provenance check.** Memo §11.6: C's recomputed k=12 365-anchor surface must match Candidate B's stored `protocol_payload.n2_null_full` in `results/candidate_b_results_20260514_231323_c1982503.json` to ≤ 1e-12 per anchor.

## 3. Required verbatim disclosures (re-emitted from the verdict log)

The verdict log carries three required-verbatim disclosure paragraphs. They are re-emitted here in full because they are verdict-interpretation-critical and any reader of this closure memo must encounter them with the same wording the locked protocol commits to.

### 3.1 Granularity caveat (verbatim, design memo §12.4)

> The four-class verdict map compares the median PSS across the 365-anchor surface at two different temporal resolutions: ≈ 30.4 days per phase for k = 12 and ≈ 36.5 days per phase for k = 10. Median PSS is interpretable as "typical phase-structure for this bucket count" rather than "phase-structure at a specific anchor configuration." The locked decision rules are methodologically valid as pre-registered, but the interpretation of every verdict class must acknowledge that the comparison is between two different temporal resolutions, not a test of which resolution is "correct" in any absolute sense:
>
> * A 12-privileged or 10-privileged verdict reflects which resolution better organizes long/short allocation on this substrate under the anchor surface, not which bucket count is structurally correct in any absolute sense.
> * A Tied / both-structured verdict reflects that both resolutions are individually non-random and cannot be distinguished from each other under the comparison threshold, not that the underlying signal is resolution-independent.
> * A Non-confirmatory / unresolved verdict does not adjudicate the resolution question at all; it states that the pre-registered decision rules do not separate the alternatives under the locked threshold structure.
>
> This caveat applies to all four verdict classes.

### 3.2 Compound-verdict disclosure (verbatim, design memo §12.5)

> The four beat counts that drive the verdict are coupled. They are derived from the same shared pool of 10,000 pooled-population is_long permutations. The verdict classes are pre-registered decision rules under that joint distribution, not independent p-value claims. The false-positive interpretation of a class assignment is therefore not identical to the false-positive rate of a single independent test at the 95th percentile, and the four classes do not partition probability mass uniformly under the null.

### 3.3 Inherited data-contact disclosure (verbatim, design memo §13)

> Candidate C's verdict is conditional on a previously contacted, audit-frozen pullback-event population. The pullback Phase 1–3b series for SPY and the Phase 3b 2005–2022 series for SPY/EFA/EEM/GLD/TLT were inspected, partitioned, and used to estimate within-population statistics during pullback research before Coherent Numbers contacted them. The pullback BacktestParams were locked early at pullback commit 50ee2d1 and not re-tuned, which limits but does not eliminate that prior exposure. Candidate B previously applied 12-phase March-20-anchored machinery to this same population — specifically a 10,000-element unstratified label-permutation null (§10.1 of docs/candidate_b_design_memo_v0.1.md) and an exhaustive 365-DOY anchor-control null (§10.2) — and reported the resulting verdict in results/candidate_b_results_20260514_231323_c1982503.json. Candidate C applies parallel 12-phase and 10-phase machinery to the same population under symmetrical anchor-surface rules. Candidate C's verdict is therefore conditional on (i) the pullback program's prior contact with the underlying series, and (ii) Candidate B's prior contact with the pooled Phase 3b population under 12-phase machinery. OOS 2023+ remains sealed in both repos and is out of scope for Candidate C. This disclosure is required wording; a hash citation alone does not satisfy it.

## 4. Primary result

| Quantity                                    | Value                   |
| ------------------------------------------- | ----------------------- |
| `median_12_observed`                        | `0.034445901350758625`  |
| `median_10_observed`                        | `0.0298511936535751`    |
| `diff_observed` (= `median_12 − median_10`) | `+0.004594707697183526` |

| Beat count                 | Value | Threshold (9,500/10,000) | Pass |
| -------------------------- | ----- | ------------------------ | ---- |
| `beat_count_12_individual` | 10000 | ≥ 9500                   | ✓    |
| `beat_count_10_individual` | 10000 | ≥ 9500                   | ✓    |
| `beat_count_comparison_12` | 9973  | ≥ 9500                   | ✓    |
| `beat_count_comparison_10` | 27    | ≥ 9500                   | ✗    |

Verdict class: **12-privileged** (Class 1).

Decision rule satisfied (memo §12.2 Class 1):
`beat_count_comparison_12 ≥ 9500 AND beat_count_12_individual ≥ 9500` → `9973 ≥ 9500 AND 10000 ≥ 9500`.

### 4.1 Precise interpretation

What the four beat counts jointly say, scoped to the locked decision rules:

* Both bucket counts produce phase-allocation structure that is non-random against pooled permutation of `is_long`. Both individual nulls cleared at the floor (10000/10000). The pooled Phase 3b population has phase-allocation structure at both k = 12 and k = 10 resolutions, when each is evaluated as the median of its own 365-anchor PSS surface.
* The directed comparison favors k = 12 strongly. The diff distribution under the shared null is heavily skewed: 9973 of 10,000 permuted diffs fall below the observed diff (where the observed diff is positive at `+0.004594707697183526`), and only 27 fall above. The shared-permutation coupling means the four beat counts are pre-registered decision rules under one joint distribution, not independent p-value claims (per §3.2 above).
* Per Class 1's verbatim §12.2(a) language:

  > (a) What it supports: under the locked decision rules, the 12-bucket partition is distinguished from the 10-bucket partition on this substrate and the 12-bucket partition is itself non-random against its own null. The comparison and individual evidence are jointly consistent with 12 carrying structure that 10 does not capture under the locked protocol.

## 5. Diagnostic texture (non-verdict)

The following diagnostics are reported but do not affect the verdict. Per memo §12.6 and lock-acceptance §7, secondary diagnostics cannot alter or upgrade the verdict class. The §12.4 granularity caveat applies symmetrically: diagnostic texture consistent with the primary result does not extend the locked decision rules' scope.

### 5.1 Asset-stratified diagnostic

`run_asset_stratified_diagnostic` (memo §11.3) produces the three coupled nulls under within-asset `is_long` shuffles (`ASSET_STRAT_DIAG_SEED_C = 20260517`, `N_PERM = 10,000`). Diagnostic beat counts under this stratification:

| Asset-stratified beat count | Value |
| --------------------------- | ----- |
| `beat_count_12_individual`  | 10000 |
| `beat_count_10_individual`  | 10000 |
| `beat_count_comparison_12`  | 9979  |
| `beat_count_comparison_10`  | 21    |

The stratified pattern mirrors the primary closely (9979 vs 9973 in the favored direction; 21 vs 27 in the dispreferred direction). This is texture consistent with the primary finding being a property of the pooled phase-allocation structure rather than an artifact of asset-composition reshuffling under the unstratified pool. Per memo §12.6, this does not rescue, alter, or upgrade the verdict.

### 5.2 §11.6 provenance check

| Quantity            | Value |
| ------------------- | ----- |
| `max_abs_diff`      | `0.0` |
| `n_anchors_checked` | 365   |
| `pass`              | True  |

C's recomputed k = 12 365-anchor PSS surface is bit-identical to Candidate B's stored `protocol_payload.n2_null_full` in `results/candidate_b_results_20260514_231323_c1982503.json`. Maximum absolute per-anchor difference is exactly `0.0` — strictly within the ≤ 1e-12 tolerance, in fact at floating-point equality. Audit-chain consistency between Candidate B's locked k = 12 surface and Candidate C's parallel computation is confirmed.

### 5.3 Other diagnostics (recorded in the verdict log JSON, not reproduced numerically here)

* Best-anchor PSS for each bucket count (memo §11.1).
* Anchor-distribution shape: mean, std, min, max of each 365-anchor PSS surface (memo §11.2).
* Per-asset PSS at the civil-date March-20 anchor (via §7.1 lens) and at each bucket count's peak anchor d* (memo §11.4). The civil-date March-20 diagnostic is not in general equal to any single value in `PSS_surface_k` due to the leap-year DOY-79 vs DOY-80 distinction (memo §7.4); see lock-acceptance §4 commentary.
* Top-10 DOY anchors per bucket count (memo §11.5).

These quantities are diagnostic only and live in `protocol_payload.diagnostics` of the verdict log JSON.

## 6. What was found (within the locked scope)

Under the locked decision rules:

* Phase-allocation structure exists in the pooled Phase 3b 1,282-trade substrate at both k = 12 and k = 10 resolutions, when each is evaluated as the median of its own 365-anchor PSS surface. Both individual nulls cleared at 10000/10000.
* The k = 12 partition produces a higher typical PSS across the 365-anchor surface than the k = 10 partition. The directed comparison diff is `+0.004594707697183526` and falls in the upper tail of the shared null at 9973/10,000.
* The 12-vs-10 separation survives within-asset preservation (asset-stratified diagnostic: 9979 in the same direction). The separation is unlikely to be an artifact of asset-composition reshuffling under the unstratified pool.
* Candidate C's recomputed k = 12 365-anchor surface is bit-identical to Candidate B's stored surface, confirming audit-chain consistency between the two cells at floating-point equality.

The Class 1 result is the first non-null verdict in the Coherent Numbers harmonic-calendar lens family's audit chain.

## 7. What was not found

Per the verbatim Class 1 (b) wording in memo §12.2:

> (b) What it does not support: the verdict does not establish that 12 is uniquely privileged among all bucket counts (the locked design tests only 12 vs 10); it does not establish that 12 is privileged because of a duodecimal property as opposed to a feature of this substrate at this resolution; it does not confirm or rescue Candidate B's equinox hypothesis; and it does not generalize to other populations, windows, or anchor configurations not pre-registered here.

Additional negative scoping clauses, all derived from the locked design surface and not new claims:

* The broader framework §9.2 set {6, 8, 10, 12, 18, 24} remains untested. C's design narrowed to a single binary contrast (12 vs 10) as the most informative non-duodecimal alternative, not as a representative of all alternatives. The privilege of 12 against 6, 8, 18, or 24 is unanswered.
* The granularity caveat (§3.1 above) is load-bearing: 12-privileged on this substrate means k = 12 better organizes long/short allocation under the locked anchor surface, not that 12 is structurally "correct." The comparison is between two temporal resolutions of different bin widths.
* Candidate B's split-null verdict stands. C tests a different question (bucket-count privilege under symmetrical anchor surfaces) on the same substrate; C's verdict does not bear on B's pre-registered equinox question. The equinox-as-organizing-anchor hypothesis remains not confirmed per B's closure.
* The result does not establish that the underlying anchor-organizing structure in the pullback substrate is duodecimal as opposed to broadly annual; only that under the locked decision rules, the 12-bucket partition out-organizes the 10-bucket partition on this substrate.
* Secondary diagnostics (asset-stratified, per-asset, top-10 anchors, anchor-distribution shape) cannot rescue, alter, or upgrade the verdict class. Per memo §12.6 and lock-acceptance §7, no diagnostic may promote the verdict.

## 8. Program posture

Candidate C joins the Coherent Numbers harmonic-calendar lens family as the fourth closed cell overall in the program and the second closed cell on the pullback × pooled-Phase-3b substrate family:

* SPY MVT closure (commit `371ca9c`): null/null on continuous returns.
* GLD closure (commit `2e2c974`): null/null on continuous returns.
* Candidate B closure (commit `df09aa8`): Split-null on pullback × pooled Phase 3b under equinox-anchored 12-phase.
* Candidate C closure (this artifact): 12-privileged on pullback × pooled Phase 3b under symmetrical 12-vs-10 anchor surfaces.

Candidate C is the first non-null verdict in the audit chain. The 12-privileged classification, bounded by the §12.2(b) and §12.4 disclosures above, places another atlas tile in the program's map. The result provides one empirical contrast (12 over 10 on this substrate under the locked rules) where the binary test resolved in favor of 12; it does not establish duodecimal privilege as a confirmed property of either this substrate or the broader research program.

The posture is constrained curiosity, not rescue. The locked no-rescue clauses (memo §12.6) and the lock-acceptance §7 prohibitions apply through this closure. C's verdict does not authorize amendment of the locked design surface, does not authorize new bucket-count probes within this cell, and does not invite reinterpretation of Candidate B's verdict in light of C's result.

## 9. Open questions not answered by Candidate C

Each item below is explicitly out of scope for this cell and requires its own future audit chain if pursued:

* Is k = 12 privileged against bucket counts other than 10 — for example 6, 8, 18, 24? The broader §9.2 framework set is unanswered by this cell. The locked design narrowed to 12 vs 10 deliberately, on the rationale that a binary contrast yields cleaner inferential structure than a multi-class adjudication (memo §8.1).
* Is the 12-privileged result driven by duodecimal structure, by a substrate-specific feature at this temporal resolution, by an annual-rhythm artifact, or by some other dependency? The locked design does not adjudicate. The §12.4 granularity caveat explicitly constrains this question.
* Does the 12-vs-10 separation hold on different populations — other event-derived substrates, different time windows, OOS 2023+ data? Only the locked pooled Phase 3b 2005–2022 substrate has been tested. OOS 2023+ remains sealed and is out of scope.
* Does Candidate B's equinox-as-organizing-anchor question become tractable under different anchor controls? B's split-null verdict stands; C does not revisit.
* The nested 12 × 12 question (framework memo §5) remains reserved for a possible future cell contingent on this finding. The locked design memo §1 narrowing decision 5 explicitly defers it.
* Influential Numbers, neighbor-influence smoothness, and other lens-family extensions remain explicitly out of scope (memo §16; lock-acceptance §7 prohibitions).

## 10. Closure statement

Candidate C is closed as 12-privileged. The 12-bucket annual-sector partition is distinguished from the 10-bucket partition on the pooled Phase 3b 1,282-trade substrate under symmetrical 365-DOY anchor-surface rules: `beat_count_comparison_12 = 9973/10000` with `beat_count_12_individual = 10000/10000`. Per the verbatim §12.2(b) and §12.4 disclosures re-emitted in §3 of this memo and recorded in the verdict log, the verdict does not establish 12 as uniquely privileged among all bucket counts, does not attribute the privilege to a duodecimal property as opposed to a substrate feature at this temporal resolution, does not rescue Candidate B's equinox hypothesis, and does not generalize beyond the pre-registered substrate. The comparison is between two different temporal resolutions, not a test of which resolution is "correct" in any absolute sense.

— end of closure memo —
