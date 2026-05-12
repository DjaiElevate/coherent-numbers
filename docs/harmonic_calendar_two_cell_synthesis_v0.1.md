# Harmonic Calendar Two-Cell Synthesis

**Version:** v0.1  
**Date:** May 12, 2026  
**Project:** Coherent Numbers  
**Status:** Program-posture synthesis. Consolidates the closed SPY and GLD harmonic-calendar cells. Not a protocol. Not a cell-selection memo.

---

## What was jointly tested

Both cells applied the same registered lens: a 108-phase harmonic calendar anchored on the civil-date proxy of March 20 for the vernal equinox, as locked in `docs/harmonic_calendar_design_memo_v0.3.3.md`. Both cells tested two outcomes: daily continuous log returns and daily squared log returns.

Assets and date ranges:

- **SPY:** 1993-01-29 to 2024-12-31. Verdict run at commit `35eab04`; closure memo at commit `371ca9c` (`harmonic_calendar_mvt_closure_memo_v0.1.md`).
- **GLD:** 2004-11-19 to 2024-12-31. Verdict run at commit `5cc8c6e`; closure memo at commit `2e2c974` (`harmonic_calendar_gld_closure_memo_v0.1.md`).

Both cells shared the same inherited v0.3.3 control structure: January-anchored 108-phase calendar, Gregorian month, exhaustive enumeration of all 365 integer-DOY anchor calendars as the null, strict-rank thresholds (347/365 for training, 329/365 for holdout), and a holdout-transparency clause requiring both training-screen pass and positive holdout PSS to constitute a finding.

---

## Joint verdict

Four registered outcome verdicts. Four nulls.

- **SPY log_return:** null.
- **SPY squared_log_return:** null.
- **GLD log_return:** null.
- **GLD log_return_sq:** null.

The registered March20-anchored 108-phase harmonic-calendar lens did not pass the pre-registered success criterion on either outcome for either asset. There is no finding.

---

## Cross-cell texture

The following observations are drawn directly from the two closure memos. No new analysis is introduced here.

**1. Below-minimum log_return PSS_in on both assets.**

On both SPY and GLD, March-20's in-sample PSS for log_return fell strictly below the minimum of all 365 fixed-DOY anchor calendars. On SPY the null range was 0.01951 to 0.02461 and March-20 scored 0.01690. On GLD the null range was 0.04249 to 0.05329 and March-20 scored 0.03711. In both cases every pure integer-DOY anchor outperformed the civil-date March-20 anchor in-sample. The closure memos frame the most plausible explanation as leap-year jitter: civil-date March 20 alternates between DOY 79 and DOY 80 across leap years, diluting phase identity relative to fixed-DOY anchors that maintain exact 365-day periodicity and preserve any year-aligned structure.

This pattern repeated across two structurally similar assets. It is a property of the audit record.

**2. Squared-return training rank differed between assets.**

SPY's squared-return outcome reached a training-screen rank of 351/365 (strict_percentile 0.9616) before failing holdout. GLD's squared-return outcome reached only 287/365 (0.7863) and did not clear the training threshold. The GLD closure memo frames this difference through the pre-registered training-power caveat: GLD's training window (~10.1 years, 2,546 trading days) is roughly half that of SPY (~22 years, 5,545 trading days), producing noisier per-anchor PSS_in estimates and making any underlying rank signal harder to detect. This asymmetry was accepted as a limitation before GLD data contact; it applies here without adjustment and does not constitute a new hypothesis.

---

## What this jointly licenses

The registered March20-anchored 108-phase harmonic-calendar lens has not resolved daily continuous-return structure in the two ETF contexts tested — SPY and GLD — under their locked protocols, controls, thresholds, and holdout requirements.

The two cells jointly lower the program's expectation that further standalone continuous-return tests of the same harmonic-calendar lens on closely similar ETF assets will have high information value per cost. This is a program-posture update, not a program-level verdict.

---

## What this does not license

The two-cell synthesis does not establish or refute claims about:

- Assets other than SPY and GLD.
- Structurally different assets such as BTC, futures, or individual equities.
- Other lenses, including lunar cycle, memory/autocorrelation, or regime structure.
- Other outcomes, including higher moments, intraday returns, or regime-conditional outcomes.
- Calendar modulation of an already-existing signal.
- Pullback-trade populations.
- The broader Microscope / Instrument Program.
- The broader two-layer pressure/release framework.
- Phase 2.
- The Time-Energy Coupling Note.

Two null cells are two null cells. They are not a program-level null. Future cells may differ.

---

## Program-posture implication

The two closed cells lower the priority of additional standalone harmonic-calendar continuous-return tests using the same March20-108 lens, especially on structurally similar ETF assets. They do not rule out future standalone tests, but any future decision memo should treat the SPY + GLD pair as prior evidence that the standalone version of this lens has so far failed under audit-controlled conditions.

The selection of any next cell, if a next cell is selected, belongs to a separate decision memo and is not determined here.
