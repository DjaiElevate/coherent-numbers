# Harmonic Calendar / Time Geometry Framework

**Version:** v0.3.1 (Design Memo — Clarification Patch)
**Date:** May 11, 2026
**Project:** Coherent Numbers
**Status:** Pre-registered. No data has been touched. Protocol locked.

---

## Changes from v0.3

This is a **clarification patch**, not a redesign. No success criteria, controls, or constants change. Three precisions are tightened to align the memo with the analytic implementation and to prevent avoidable critiques.

1. **Equinox anchor honestly named.** The implementation uses March 20 as a fixed civil-date proxy for the vernal equinox. The memo now states this explicitly rather than referring to astronomical equinox timing. The 108-phase resolution is ~3.38 days, so the proxy lies within one phase bucket of the true equinox for all years 1900–2100. Exact astronomical equinox dates (via Meeus's formula or an ephemeris library) are **reserved for a future robustness test** and may not be substituted post-hoc.
2. **Null distribution precision aligned with primary.** Random-anchor calendars use integer day-of-year anchors (1..365), matching the day-level precision of the primary calendar. No sub-day or continuous anchors at v0.
3. **Volatility outcome renamed.** What v0.3 called "daily realized volatility" is more precisely **squared daily log return**, a daily volatility proxy. The label avoids confusion with microstructure-literature usage of "realized volatility," which implies intraday or multi-period aggregation.
4. **PSS_in comparability clarified.** PSS_in (η²) comparisons across calendars with **different bucket counts** (e.g., harmonic 108 vs. Gregorian 12) are not statistically valid — 108 buckets has more degrees of freedom and inflates in-sample η² mechanically. PSS_oos (R²_oos) comparisons across different bucket counts **are** valid because out-of-sample prediction punishes overfitting. The Gregorian comparison is therefore meaningful on PSS_oos only.

All other content carries forward unchanged from v0.3.

---

## Core Motto

> The signal is not hidden in price alone. It may be hidden by the calendar we use to measure time.

---

## Claim Being Tested

The Gregorian calendar is well-calibrated to the tropical year at the macro scale — it tracks Earth's orbit around the Sun to within roughly one day per 3,000 years. However, its internal subdivisions are decoupled from natural cycles:

- Months no longer track lunar phase
- The seven-day week has no cosmic basis
- Year-start (January 1) is misaligned with vernal equinox and winter solstice
- Day boundary (midnight) is misaligned with solar events

**The question this memo proposes to test:** Do harmonic time coordinates (phase-based, anchored to natural cycles) reveal structure in market behavior that civil time coordinates cannot detect?

This is not a claim that the Gregorian calendar is wrong. It is a test of whether it is the right *coordinate system* for cyclic phenomena in market data.

---

## Connection to the Two-Layer Model

The existing Coherent Numbers framework holds:

- **Layer 1 (universal):** Pressure dynamics — log-space clustering and measurable exhaustion pressure — appear across assets.
- **Layer 2 (structural):** Asset-specific characteristics govern the direction of response.

This memo extends the framework with one additional principle, not a new layer:

> The coordinate system through which structure is observed is part of the structural layer. The observation frame and the receiving structure are co-determining. Different time coordinates may make the same underlying dynamics visible or invisible.

In short: *pressure is universal, release is structural, and structure includes the lens.*

---

## Minimum Viable Test (MVT)

### Asset

SPY (S&P 500 ETF). 30+ years of daily data. Single asset chosen deliberately to prevent multi-asset cherry-picking at v0 stage.

### Phase Definition (Fixed Before Any Analysis)

The primary calendar uses a **fixed March 20 civil-date proxy** for the vernal equinox:

```
solar_phase = floor( ((days_since_most_recent_march_20) / 365.2422) × 108 )
```

- Phase 0 begins on March 20.
- Range: integer 0 to 107.
- Phase resolution = 365.2422 / 108 ≈ 3.38 days. March 20 lies within one phase bucket of the true astronomical vernal equinox for all years 1900–2100.
- No alternative phase definition (different anchor, different bucket count, astronomical equinox timing) will be tried after data is observed. Astronomical equinox timing is reserved for a future robustness test that, if conducted, will be pre-registered separately.

### Outcomes (Pre-Registered)

Two outcomes computed in parallel:

1. **Daily log return** (`ln(close_t / close_{t-1})`)
2. **Daily volatility proxy** (squared daily log return)

Each outcome receives an independent primary test and verdict.

### Primary Metric: Phase Structure Score (PSS)

For each candidate calendar, we compute how much of the outcome's variance is explained by phase labels.

**In-sample (training only):**

```
PSS_in = η² = SS_between / SS_total
```

`SS_between` = sum of squared deviations of phase-bucket means from the grand mean, weighted by bucket size. `SS_total` = sum of squared deviations of all observations from the grand mean. PSS_in is biased upward by category count and is **only comparable across calendars with the same number of buckets**.

**Out-of-sample (holdout):**

```
PSS_oos = 1 − (SS_residual_oos / SS_total_oos)
```

For each holdout day, the prediction is the **training** mean of that day's phase bucket. `SS_residual_oos` = sum of squared (actual − predicted) on holdout. `SS_total_oos` = sum of squared (actual − training grand mean) on holdout. PSS_oos can be negative if the training pattern fails to generalize, which is the intended diagnostic.

PSS_oos comparisons across calendars with different bucket counts are valid because out-of-sample prediction punishes overfitting.

### Controls

1. **Random-anchor 108-phase calendars** (primary null distribution). 1,000 calendars identical in structure but with **integer day-of-year start dates** sampled uniformly from 1..365. Fixed random seed for reproducibility. Anchors near March 20 are explicitly allowed — the null represents "any possible day-of-year anchor."
2. **Gregorian month bucketing** (12 buckets). Auxiliary control. Comparison meaningful on **PSS_oos only**; PSS_in comparison is not statistically valid due to differing bucket counts.
3. **January-anchored 108-phase subdivision.** Auxiliary control with matched bucket count. Both PSS_in and PSS_oos comparisons are valid.

### Train / Holdout Split

- **Training:** All years except the final 10.
- **Holdout:** Final 10 years. Untouched until training phase is complete.

### Success Criterion (Pre-Registered)

A finding requires the March-20-anchored 108-phase calendar to clear all three thresholds for at least one of the two outcomes:

1. **Training screen:** PSS_in must exceed the 95th percentile of the random-anchor null distribution. If not, the primary verdict is null.
2. **Holdout primary verdict:** PSS_oos must exceed the 90th percentile of the random-anchor null distribution on holdout, **and** PSS_oos must be positive in absolute terms (PSS_oos > 0).
3. **Holdout auxiliary check:** PSS_oos must exceed both the Gregorian-month PSS_oos and the January-anchored 108-phase PSS_oos.

### Holdout Transparency Clause

If the training screen fails, the primary verdict is **null**. Holdout results may still be computed and reported descriptively for transparency, but they cannot reverse or rescue the null verdict. This prevents both data hiding and post-hoc rescue attempts.

Failing the success criterion on both returns and volatility → null result. Null results are reported with equal rigor as positive findings.

If returns pass and volatility fails (or vice versa), the result is reported as a partial / mixed signal and interpreted with caution.

### Secondary Diagnostics (Descriptive Only)

- Per-phase mean returns and volatilities, with Benjamini-Hochberg FDR correction at q = 0.05.
- Visualizations: phase heat map, training-vs-holdout consistency plot.
- These describe *which* phases (if any) carry observed structure. They do **not** determine the primary verdict. They are interpretable only if the primary test passes.

---

## Hypothesis (Pre-Registered)

**H1:** The March-20-anchored 108-phase calendar produces a higher Phase Structure Score on SPY daily log returns and/or squared daily log returns than the random-anchor null distribution and the auxiliary civil-time controls, with the effect surviving the train/holdout split.

**H0:** PSS for the March-20-anchored calendar is statistically indistinguishable from the random-anchor null and from civil-time controls.

Direction is not predicted in advance. Effect size threshold is not specified at v0 because no prior literature provides a sensible prior. Both PSS values and percentile ranks will be reported regardless of outcome.

---

## What This Test Cannot Settle

Even if H1 is supported, MVT cannot distinguish among:

- Markets responding to natural solar cycles (via biology, sentiment, daylight, seasonal economic activity, etc.)
- Confounding effects of Gregorian-anchored behaviors that happen to correlate with day-of-year (e.g., fiscal-year boundaries, tax-year effects)
- Coincidence that survives the percentile threshold by chance

A positive result is *not* proof of harmonic structure in markets. It is a flag that the harmonic coordinate system reveals patterns worth investigating further.

---

## Next Steps if MVT Returns a Signal

1. Robustness test: re-run with **astronomical vernal equinox dates** (Meeus formula or ephemeris) replacing the March 20 proxy. Pre-register separately.
2. Replicate on additional assets (BTC, GLD, TLT, EWZ, foreign indices) using the same protocol.
3. Compare solar phase against lunar-phase coordinates (~29.5 day cycle).
4. Compare 108-phase vs. 12-phase vs. 27-phase vs. 4-phase subdivisions to test whether granularity matters.
5. Investigate causal pathways — decompose by economic regime, sentiment indicators, volatility regime, etc.

## Next Steps if MVT Returns a Null

1. Report null cleanly. Update framework documentation: time geometry does not detectably influence SPY at 108-phase resolution under March-20-proxy anchor.
2. Consider whether different anchors (winter solstice, true astronomical equinox) or different cycles (lunar rather than solar) deserve a separate, equally pre-registered test.
3. The two-layer model itself is unaffected by a null here. Time geometry is a proposed extension; if it does not hold, the core model stands.

---

## Methodological Posture

This is a reverent investigator test.

The classical tradition encoded the year in 12-phase, 108-subdivision harmonic structure. We are not assuming this encoding is empirically meaningful in markets. We are testing whether it is.

> Reverence without falsifiability becomes belief. Falsifiability without reverence becomes reduction. The path is to bring both together.

The reverence lies in taking the traditional claim seriously enough to design a rigorous test. The investigator part lies in reporting the result truthfully, whatever it shows. The discipline of testing geometry rather than buckets is what keeps the test honest. The discipline of computing holdout regardless of training screen outcome is what keeps the test transparent. The discipline of naming the March 20 proxy honestly is what keeps the test defensible.

---

*End of design memo. Pre-registration timestamp: 2026-05-11. Protocol locked at v0.3.1. No data has been touched.*
