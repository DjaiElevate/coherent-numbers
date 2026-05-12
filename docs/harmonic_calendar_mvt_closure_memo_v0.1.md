# Harmonic Calendar MVT — Closure Memo

**Version:** v0.1 (Closure)  
**Date:** May 12, 2026  
**Project:** Coherent Numbers  
**Status:** Phase 1 closed. Verdict landed at commit `35eab04`.

---

## What was tested

Whether a 108-phase harmonic calendar, anchored on the civil-date proxy of March 20 for the vernal equinox, resolves structure in daily SPY returns or daily squared SPY returns over 1993-01-29 to 2024-12-31, beyond what civil-time controls (Gregorian month, January-anchored 108-phase) and an exhaustive 365-anchor integer-DOY null reveal.

Full protocol locked in `docs/harmonic_calendar_design_memo_v0.3.3.md`. Audit chain: `0cc8e6a → 30faabb → ed199bd → 3b01233 → 9ea89ae → 35eab04`.

## Verdict

Null on both registered outcomes.

- **log_return:** The March-20 anchor's PSS_in fell below the minimum of all 365 fixed-DOY anchor calendars (strictly_below = 0/365). Training screen failed. Holdout PSS_oos was negative. Verdict: null.
- **squared_log_return:** Training screen passed (strict_percentile 0.9616, strictly_below 351/365, exceeding the locked threshold of 347). Holdout failed (strictly_below 27/365 against a threshold of 329; PSS_oos negative). Per the memo's holdout-transparency clause, training-screen pass alone does not constitute a finding. Verdict: null.

Overall memo-compatible summary: null.

## What this verdict licenses

The harmonic calendar lens as registered in memo v0.3.3 — civil-date March-20 anchor, 108-phase subdivision, applied to daily SPY returns and daily squared returns over 1993-2024, evaluated against the controls and thresholds specified — does not resolve structure in those outcomes for that asset over that span.

## What this verdict does not license

This verdict does not establish or refute claims about:

- The harmonic calendar hypothesis for assets other than SPY.
- The harmonic calendar hypothesis under alternative anchorings (astronomical equinox, fixed DOY, or other near-equinox civil dates).
- The harmonic calendar hypothesis at finer or coarser phase subdivisions, or on other outcomes (higher moments, regime-conditional returns, intraday data).
- The broader two-layer framework (pressure universal, release structural).
- Any Phase 2 framing, including the Time-Energy Coupling Note. The Note remains sealed off and cannot be invoked to reinterpret this Phase 1 verdict.

## Texture in the null

Two observations about how the null manifested. Neither is used here as follow-up justification; both are notes for the audit record.

The log_return result was structurally specific. March-20's PSS_in was strictly below the minimum of all 365 fixed-DOY anchor calendars (range 0.01951 to 0.02461; March-20 = 0.01690). The most plausible explanation is leap-year jitter: civil-date March 20 lands on DOY 79 in non-leap years and DOY 80 in leap years, which shifts phase boundaries across leap years and dilutes phase identity relative to fixed-DOY anchoring. Pure-DOY anchors maintain exact 365-day periodicity and so preserve any year-aligned structure (quarterly cycles, fiscal-year effects); the civil-date hybrid breaks that alignment. This is a property of the design choice (civil-date proxy vs. fixed DOY), not a flaw in the locked protocol.

The squared_log_return result showed the textbook signature of in-sample structure that did not generalize. March-20's rank moved from top 4% in training (351/365) to bottom 7% in holdout (27/365). The pre-registered holdout-transparency clause caught this directly: without the holdout, the training result would have looked like a finding worth pursuing. The pre-registration prevented that.

## Methodological notes

The protocol surfaced one defect during execution. The original v0.3.1 control specified 1,000 calendars sampled without replacement from a 365-element population, which is mathematically impossible. The defect was caught at orchestration setup, before any real-data PSS computation, by the firewall built into the protocol structure. It was resolved by amendment to v0.3.3 (exhaustive enumeration of all 365 integer-DOY anchors, strict-rank thresholds at 347/365 and 329/365) before the verdict run. The seed-locking commit (`3b01233`) preserved `RANDOM_ANCHOR_SEED = 20260512` as audit history; the v0.3.3 control does not consume it.

This closure memo is itself part of the audit record. The verdict, the protocol, and the observations above are the deliverable of Phase 1.
