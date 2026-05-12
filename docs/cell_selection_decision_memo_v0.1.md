# Cell-Selection Decision Memo

**Version:** v0.1  
**Date:** May 12, 2026  
**Project:** Coherent Numbers  
**Status:** Decision artifact for selecting the next cell in the Microscope / Instrument Program. Not a protocol. Not a data run.

---

## Purpose

This memo selects the next cell to be designed under the Microscope / Instrument Program (charter at commit `2dcf340`). The charter governs the structure of any cell test; this memo does not redefine those rules.

Selection criteria, evaluated for each candidate: cost, information value, design risk, charter compliance, data-contact history, OOS posture, multiple-comparison burden.

Two candidates are evaluated. Other candidates exist (lunar cycle on SPY, memory/autocorrelation, foundational tests of the two-layer framework) but are not evaluated in this memo.

---

## Candidate A — Cross-Asset Harmonic Calendar Extension

**Cell shape.** Lens: v0.3.3 harmonic calendar (108-phase, vernal equinox civil-date anchored). Asset: gold (GLD continuous returns) or BTC (continuous returns). Outcomes: log return, squared log return. Controls: same three as v0.3.3 (January-anchored 108-phase, Gregorian month, 365-anchor exhaustive null). Train/holdout split: to be locked in the design memo.

- **Cost:** Low. Orchestration code from v0.3.3 is asset-agnostic by design. Required work: acquire and hash-freeze new asset data, author a design memo referencing the v0.3.3 lens, execute the locked protocol. Estimated total: ~2 days.
- **Information value:** Moderate. A second null strengthens the case that the lens itself doesn't resolve return structure (rather than SPY being anomalous). A pass would be the most surprising outcome and would directly motivate further cross-asset extension.
- **Design risk:** Low. Lens and protocol already locked; the open design choices are asset selection, data span, and train/holdout split rule.
- **Charter compliance:** Clean. New asset, new memo authored before data contact, no inheritance of data-contact history.
- **Data-contact history:** No harmonic-calendar analysis on GLD or BTC continuous returns. GLD appears in prior pullback-universe work, but not as a continuous-return harmonic-calendar cell.
- **OOS posture:** Pre-registered train/holdout split locked in the design memo before data contact.
- **Multiple-comparison burden:** Light. One new cell; the charter's standalone-reporting posture applies cleanly.

---

## Candidate B — Pullback × 12-Base Calendar Modulation

**Cell shape.** Lens: 12-phase harmonic calendar (vernal equinox civil-date anchored, equal-width buckets). Asset: the existing Phase 3b 5-asset pullback universe (SPY, EFA, EEM, GLD, TLT), in-sample 2005-2022. Primary outcome: per-phase long/short allocation effect (mean signed expectancy per phase given the system's directional decisions). Secondary outcome (gated on primary pass): per-phase within-direction selection effect. Controls: 12-phase January-anchored, Gregorian month, 365-anchor exhaustive 12-phase null.

- **Cost:** Higher. Required work: design memo addressing the data-contact history of the conditioning population, locking the allocation-vs-selection framing, specifying the pooling choice, and locking all thresholds; orchestration that consumes the existing pullback trade population as input (new code, can reuse calendar utilities); phase assignment and heterogeneity metric computation; protocol execution. Estimated total: ~7-10 days.
- **Information value:** Potentially high. A pass would establish that calendar phase modulates an already-detected market signal — substantively different from "the calendar lens resolves return structure standalone." A null would close a third partition vocabulary on the pullback population, informative about the limits of the base instrument's residual variance.
- **Design risk:** High. (a) The allocation-vs-selection framing must be locked correctly given Phase 3b's narrowing — allocation primary, selection gated. (b) The pooling choice (pooled across 5 assets vs. per-asset) determines the power profile and must be pre-registered. (c) Per-phase sample sizes are at the lower edge of robust inference even pooled (~125 trades per phase pooled, ~25 per asset-phase cell). (d) Phase 2 and Phase 3a both failed to find partition structure on this population; this would be the third partition vocabulary tested.
- **Charter compliance:** Defensible but requires explicit handling. The base pullback population has been heavily data-contacted across Phases 1-3b. The design memo must state explicitly what is known about the population and ensure the calendar test doesn't covertly tune to that knowledge. The Phase 1-3b work predates the charter, so this isn't a violation, but the memo must address it head-on.
- **Data-contact history:** Substantial. 301-trade SPY base population and 5-asset universe used across Phases 1-3b. Three prior partition vocabularies tested (Grimes filters, Grimes partitions, Phase 3b directional decomposition). The calendar lens would be a fourth vocabulary on the same population.
- **OOS posture:** OOS (2023+) sealed and remains so. Test is in-sample only on 2005-2022 Phase 3b window. The design memo must explicitly state OOS is not opened.
- **Multiple-comparison burden:** Heavy. Fourth partition test on the same population. Cross-cell replication via 5-asset pooling provides some within-test replication, but cumulative degrees of freedom consumed across Phases 1-3b plus this test is real.

---

## Comparison

| Criterion | A (Cross-Asset) | B (Pullback × Calendar) |
|---|---|---|
| Cost | Low (~2 days) | Higher (~7-10 days) |
| Information value | Moderate | Potentially high |
| Design risk | Low | High |
| Charter compliance | Clean | Defensible with explicit handling |
| Data-contact history | No harmonic-calendar analysis on continuous returns | Substantial (4 prior phases) |
| OOS posture | Pre-registered split | In-sample only; OOS sealed |
| Multiple-comparison burden | Light | Heavy |

## Discussion

The candidates are not strictly comparable. Candidate A is a low-cost extension of an already-closed test, most likely producing another null but contributing to a cleanly comparable cross-asset matrix. Candidate B asks a different and more interesting question — calendar as modulator of an existing signal rather than calendar as standalone resolver — but carries substantially more design risk and an elevated prior probability of producing a null given the Phase 2/3a wall pattern (the base pullback system's mechanics absorb the structural variance that partition vocabularies would otherwise carve).

The trade-off is between matrix-building economy and conceptual synthesis. A favors economy: cheap, fast, charter-clean, fills out the cross-asset axis of the matrix, and produces a result that is directly interpretable against the SPY null. B favors synthesis: more expensive, more design-heavy, but connects two previously separate lines of work and asks a question that no prior phase has addressed.

A consideration not captured in the criteria: choosing A does not foreclose B. Running cross-asset extension first does not commit the program to never running the pullback × calendar test. Choosing B first, however, consumes substantial design time and may delay any cross-asset work for weeks. The asymmetry favors A as a near-term move if both tests are eventually wanted.

A null verdict on either candidate is a legitimate and program-compatible outcome. The decision is not "which test is more likely to succeed" but "which test's verdict, in either direction, is more valuable to have."

GLD is selected over BTC within Candidate A because GLD is structurally closer to SPY: ETF with trading-day structure, adjusted-close handling, single primary listing. BTC introduces design complications (24/7 trading, exchange-source choice, calendar-day definitions, shorter reliable history depending on data source) that are best addressed in a later cell once one ETF-to-ETF extension has been completed.

---

## Decision

**Selected cell:** Candidate A — Cross-Asset Harmonic Calendar Extension on GLD continuous returns.

**Justification:** Candidate A is selected as the first post-charter cell because it is the cleanest continuation of the closed Harmonic Calendar MVT while adding one new matrix dimension: asset. The SPY test closed with a null under memo v0.3.3; running the same lens structure on GLD asks whether that null reflects weakness of the harmonic calendar lens generally, or whether SPY specifically failed to express the structure. GLD is preferred over BTC because it is an ETF with trading-day structure and adjusted-close handling closer to SPY, reducing design complications around 24/7 markets, exchange selection, and calendar-day definitions.

This selection is not a rescue of the SPY null. It is a cross-asset replication test under the charter's matrix structure (lens, asset, outcome), with no parameter changes to the lens. The SPY null stands; the GLD test asks an adjacent question, not the same one.

Candidate B is deferred to a future decision memo; deferral is not rejection. Candidate B carries higher design risk, substantial data-contact history, heavier multiple-comparison burden, and unresolved choices about allocation-vs-selection framing and pooled-vs-asset-level inference. Deferring B preserves it for a later design memo once the program has established one clean cross-asset extension.

**Expected next artifact:** Design memo for `harmonic_calendar_gld_v0.1`, authored before any GLD data contact for this test, committed as its own audit-chain entry. The design memo must explicitly resolve the train/holdout split before data contact, choosing between:

1. Inheriting v0.3.3's "final 10 calendar years as holdout" rule (preserves calendar-matched holdout window with SPY; produces ~10/10 train/holdout split given GLD's November 2004 inception, accepting reduced training power relative to SPY's ~22/10 split).
2. Using a proportional split matched to SPY's ~69/31 ratio (preserves structural comparability of training power; produces a non-calendar-matched holdout window).
3. Another pre-registered split rule with explicit justification before GLD data contact.

No GLD data is to be loaded prior to the design memo's commit. The split rule must be locked in the design memo, not amended afterward.

---

## Status of this memo

v0.1. The decision is recorded above. No subsequent cell design begins until the GLD design memo is committed.
