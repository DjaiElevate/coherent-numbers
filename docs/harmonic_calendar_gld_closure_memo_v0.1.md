# Harmonic Calendar × GLD — Closure Memo

**Version:** v0.1 (Closure)  
**Date:** May 12, 2026  
**Project:** Coherent Numbers  
**Cell:** Harmonic Calendar × GLD continuous returns  
**Status:** Closed. Verdict landed at commit `5cc8c6e`.

---

## What was tested

Whether a 108-phase harmonic calendar, anchored on the civil-date proxy of March 20 for the vernal equinox, resolves structure in daily GLD continuous log returns or daily squared GLD log returns over 2004-11-19 to 2024-12-31, beyond what civil-time controls (Gregorian month, January-anchored 108-phase) and an exhaustive 365-anchor integer-DOY null reveal.

The cell inherits the v0.3.3 lens intact. Lens, controls, rank thresholds, success criterion, and verdict structure are those locked in `docs/harmonic_calendar_design_memo_v0.3.3.md`. The GLD-specific design decisions — asset selection, data source, date range, train/holdout split, and interpretation caveat — are specified in `docs/harmonic_calendar_gld_v0.1.md`.

Training window (effective loaded): 2004-11-19 through 2014-12-31 (2,546 trading days, approximately 10.1 years). Holdout window (effective loaded): 2015-01-02 through 2024-12-31 (2,516 trading days, 10 calendar years). Total loaded rows: 5,062. Frozen GLD CSV SHA256: `368fe450…` (data-freeze commit `4dc56c4`).

GLD cell audit chain: `11b00d6 → 4dc56c4 → 87e5578 → 5cc8c6e`.

## Verdict

Null on both registered outcomes.

- **log_return:** March-20's PSS_in (0.03711) fell below the minimum of all 365 fixed-DOY anchor calendars (null PSS_in range: 0.04249 to 0.05329). Training screen failed (strictly_below = 0/365; threshold 347/365). Holdout PSS_oos was negative (−0.09173), despite March-20 ranking above all 365 anchor controls in holdout (strictly_below = 365/365). The PSS_oos > 0 gate failed. Verdict: null.

- **log_return_sq:** Training screen failed (strictly_below = 287/365, strict_percentile 0.7863; threshold 347/365). March-20's PSS_in (0.04137) was within the null PSS_in range (0.03119 to 0.04352) but did not clear the threshold. Holdout failed (strictly_below = 99/365, strict_percentile 0.2712; PSS_oos = −0.21085, negative). Verdict: null.

Overall memo-compatible summary: null.

## What this verdict licenses

The harmonic calendar lens as registered in memo v0.3.3 — civil-date March-20 anchor, 108-phase subdivision, applied to daily GLD log returns and daily squared log returns over 2004-2024, evaluated against the controls and thresholds specified — does not resolve structure in those outcomes for that asset over that span.

This is the second audit-controlled null result under the Microscope/Instrument Program. The first was SPY (closure memo `harmonic_calendar_mvt_closure_memo_v0.1.md`). The cross-asset pattern — null on both assets, null on both outcomes — can be noted as an observation: the registered v0.3.3 lens has not resolved structure in daily continuous-return outcomes on either of its first two applications. That observation belongs to the audit record.

## What this verdict does not license

This verdict does not establish or refute claims about:

- The harmonic calendar hypothesis for assets other than GLD under this lens.
- The harmonic calendar hypothesis applied to GLD under alternative anchorings, phase subdivisions, or outcomes.
- GLD pullback-trade outcomes. This cell tests the harmonic calendar lens on daily continuous log returns, not on the pullback-trade population that includes GLD in the Phase 3b universe expansion. Those are distinct analytical contexts; neither verdict speaks to the other.
- Any program-level conclusion about the harmonic calendar. Two null cells are two null cells; they are not a program-level null. Future cells may differ.
- The broader two-layer framework.
- Any Phase 2 framing, including the Time-Energy Coupling Note. The Note remains sealed off and cannot be invoked to reinterpret this cell's null verdict.

## Texture in the null

Two observations about how the null manifested. Neither is used here as follow-up justification; both are notes for the audit record.

**The below-minimum log_return pattern appeared on both assets.** On GLD, as on SPY, March-20's PSS_in for log_return fell strictly below the minimum of all 365 fixed-DOY anchor calendars. On SPY the PSS_in range was 0.01951 to 0.02461 and March-20 scored 0.01690. On GLD the range was 0.04249 to 0.05329 and March-20 scored 0.03711. In both cases, every pure integer-DOY anchor outperformed the civil-date March-20 anchor in-sample. The consistency of this pattern across two structurally similar assets (exchange-traded, dividend-adjusted, daily continuous returns) is a property of the audit record. The most plausible explanation remains the one noted in the SPY closure memo: leap-year jitter causes civil-date March 20 to alternate between DOY 79 and DOY 80, diluting phase identity relative to pure fixed-DOY anchors. GLD's below-minimum result is consistent with that account.

**The log_return_sq training rank difference is explained by the pre-registered training-power caveat, not used as new hypothesis.** SPY's squared-return outcome reached a training-screen rank of 351/365 (strict_percentile 0.9616) before failing holdout. GLD's squared-return outcome reached only 287/365 (0.7863) and did not clear the training threshold. The difference in training rank is consistent with the asymmetry documented before GLD data contact in design memo v0.1: GLD's training window (~10.1 years, 2,546 trading days) is roughly half that of SPY (~22 years, 5,545 trading days), producing noisier per-anchor PSS_in estimates. On a shorter window, any underlying rank signal — if present — is harder to detect; the underlying per-anchor PSS estimates are noisier, so the rank ordering is more sensitive to noise. This is a property of GLD's shorter available history, not a finding about the lens. The training-power asymmetry was accepted as a limitation of the GLD cell before data contact; it applies here without adjustment.

## Methodological notes

The GLD cell is the first application of the v0.3.3 protocol to a non-SPY asset. No protocol defects were encountered during this execution. The control spec used here (exhaustive enumeration of all 365 integer-DOY anchors; strict-rank thresholds 347/365 and 329/365) was already resolved and locked in v0.3.3 before the GLD cell was scoped. The seed-locking constant `RANDOM_ANCHOR_SEED = 20260512` is preserved as audit history; the exhaustive control does not consume it, consistent with SPY.

One provenance distinction specific to this cell: the GLD result artifacts distinguish the raw/design data range (2004-11-18 through 2024-12-31, GLD inception) from the effective loaded-return date range (first return date 2004-11-19, after first-row log-return drop). The SPY results did not carry this distinction explicitly; it has been added to the GLD artifacts as a clarity improvement in the audit trail.

The frozen GLD CSV was verified by SHA256 hash on load (hash embedded in filename; `gld_loader.load_gld()` verifies on every call). The SPY frozen CSV was not read or modified during the GLD cell. The protocol was executed exactly once against the frozen data.
