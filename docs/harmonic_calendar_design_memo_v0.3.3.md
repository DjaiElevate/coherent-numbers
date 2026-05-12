# Harmonic Calendar / Time Geometry Framework

**Version:** v0.3.3 (Design Memo — Anchor-Control Amendment)
**Date:** May 12, 2026
**Project:** Coherent Numbers
**Status:** Pre-registered. No real-data PSS values, no real SPY phase assignments, and no Commit 4 verdict outputs have been computed. Protocol locked.

---

## Changes from v0.3.2

This is an **anchor-control amendment**, not a redesign of the outcomes, anchors, or success criteria. One pre-registration defect carried forward from v0.3.1 / v0.3.2 is resolved here.

1. **Anchor-control null replaced with exhaustive enumeration.** v0.3.2 (carried from v0.3.1) specified "1,000 calendars with integer day-of-year start dates sampled uniformly from 1..365." The committed implementation used `random.sample` without replacement, which cannot draw 1,000 distinct integers from a population of 365. Drawing 1,000 *with replacement* would have been mechanically possible but would (a) produce ~89% duplicate calendars on average and (b) add Monte Carlo noise to an exactly computable finite quantity. v0.3.3 replaces the random-sample control with **exhaustive enumeration of all 365 integer day-of-year anchors, 1..365, each evaluated exactly once**. This is the full finite anchor-control population.
2. **March 20 (DOY 79 in non-leap years) is retained in the 365-anchor null.** The candidate-anchor calendar uses `date(year, 3, 20)` directly (a fixed civil-date proxy), while the 365 DOY-anchored calendars use `date(year, 1, 1) + timedelta(doy - 1)` per the v0.3.1 implementation. These coincide in non-leap years for DOY 79 and differ by one day in leap years. DOY 79 is therefore the *closest* but **not identical** twin of the candidate; it is not manually excluded from the control population. This is consistent with the original v0.3.1/v0.3.2 intent that the candidate anchor was sampled from, not excluded from, the integer-DOY population.
3. **Finite-population rank/percentile convention locked.** With the null distribution now a finite, exhaustively enumerated population of 365 values, the pass/fail comparison is rank-based and deterministic — not based on interpolated percentile functions. The exact convention is locked in the Success Criterion section below.
4. **Seed preserved for audit traceability only.** `RANDOM_ANCHOR_SEED = 20260512` (locked in v0.3.2) is preserved unchanged in `src/harmonic_calendar.py` for audit traceability from v0.3.2, but it is **not used** by the v0.3.3 exhaustive anchor-control null. The v0.3.3 control involves no random sampling and consumes no random seed.

All other content carries forward unchanged from v0.3.2.

### v0.3.3 amendment note (verbatim, for citation)

> The v0.3.2 random-anchor control contained an implementation/protocol contradiction: 1,000 without-replacement draws from 365 possible integer DOY anchors is impossible. Because this contradiction surfaced before any real-data PSS values, real SPY phase assignments, or Commit 4 verdict outputs were computed, the control is amended to exhaustive enumeration of all 365 integer DOY anchors. This removes Monte Carlo sampling noise and evaluates the full finite anchor population.

> RANDOM_ANCHOR_SEED = 20260512 is preserved in code for audit traceability from v0.3.2 but is not used by the v0.3.3 exhaustive anchor-control null.

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

**Out-of-sample (holdout):**

```
PSS_oos = 1 − (SS_residual_oos / SS_total_oos)
```

For each holdout day, the prediction is the **training** mean of that day's phase bucket. PSS_oos can be negative if the training pattern fails to generalize, which is the intended diagnostic.

PSS_oos comparisons across calendars with different bucket counts are valid because out-of-sample prediction punishes overfitting. PSS_in comparisons across different bucket counts are not statistically valid.

### Controls

1. **Anchor-control 108-phase calendars (exhaustive enumeration, v0.3.3).** The null distribution is the **full finite population of 365 integer day-of-year anchored 108-phase calendars**, with anchor DOYs taking each integer value in 1..365 exactly once. Anchor date in year *Y* is `date(Y, 1, 1) + timedelta(doy - 1)`. The DOY corresponding to ≈ March 20 (DOY 79 in non-leap years) is retained in this population; it is not the same as the candidate's `date(Y, 3, 20)` anchor due to one-day leap-year shifts. No random sampling is used; `RANDOM_ANCHOR_SEED` is not consumed by this control.
2. **Gregorian month bucketing** (12 buckets). Auxiliary control. Comparison meaningful on **PSS_oos only**; PSS_in comparison is not statistically valid due to differing bucket counts.
3. **January-anchored 108-phase subdivision.** Auxiliary control with matched bucket count. Both PSS_in and PSS_oos comparisons are valid.

### Train / Holdout Split

- **Training:** All years except the final 10.
- **Holdout:** Final 10 years. Untouched until training phase is complete.

### Success Criterion (Pre-Registered)

A finding requires the March-20-anchored 108-phase calendar to clear all three thresholds for at least one of the two outcomes:

1. **Training screen:** March20 PSS_in must strictly exceed the PSS_in of **at least 347 of the 365** anchor-control calendars. Equivalently, `strictly_below_count(march20_PSS_in, anchor_control_PSS_in_population) ≥ ceil(0.95 × 365) = 347`.
2. **Holdout primary verdict:** March20 PSS_oos must strictly exceed the PSS_oos of **at least 329 of the 365** anchor-control calendars (`strictly_below_count ≥ ceil(0.90 × 365) = 329`), **and** March20 PSS_oos must be positive in absolute terms (`PSS_oos > 0`).
3. **Holdout auxiliary check:** March20 PSS_oos must strictly exceed both the Gregorian-month PSS_oos and the January-anchored 108-phase PSS_oos.

**Finite-population rank/percentile convention (locked):**

- The anchor-control null is exhaustively enumerated, so all comparisons are deterministic.
- For a given PSS metric, define:
  - `strictly_below = number of anchor calendars with PSS strictly less than March20's PSS`
  - `equal_to       = number of anchor calendars with PSS exactly equal to March20's PSS`
- Pass/fail uses **strict beating only.** Ties are not counted as strictly below March20 and therefore do not help March20 clear a threshold.
- `strict_percentile = strictly_below / 365` is reported for human readability. **Pass/fail is determined by the integer rank thresholds (347, 329), not by the reported percentile.**
- No interpolated percentile function (e.g., `numpy.percentile` linear interpolation) is used to determine pass/fail.

### Holdout Transparency Clause

If the training screen fails, the primary verdict is **null**. Holdout results may still be computed and reported descriptively for transparency, but they cannot reverse or rescue the null verdict.

Failing the success criterion on both outcomes → null result. Null results are reported with equal rigor as positive findings. If returns pass and volatility fails (or vice versa), the result is reported as a partial / mixed signal and interpreted with caution.

### Secondary Diagnostics (Descriptive Only)

- Per-phase mean returns and volatilities, with Benjamini-Hochberg FDR correction at q = 0.05.
- These describe *which* phases (if any) carry observed structure. They do **not** determine the primary verdict. They are interpretable only if the primary test passes.

---

## Hypothesis (Pre-Registered)

**H1:** The March-20-anchored 108-phase calendar produces a higher Phase Structure Score on SPY daily log returns and/or squared daily log returns than the exhaustive 365-anchor null and the auxiliary civil-time controls, with the effect surviving the train/holdout split.

**H0:** PSS for the March-20-anchored calendar is statistically indistinguishable from the 365-anchor null and from civil-time controls.

Direction is not predicted in advance. Both PSS values and strict ranks (with reported percentiles) will be reported regardless of outcome.

---

## What This Test Cannot Settle

Even if H1 is supported, MVT cannot distinguish among:

- Markets responding to natural solar cycles
- Confounding effects of Gregorian-anchored behaviors that happen to correlate with day-of-year
- Coincidence that survives the threshold by chance

A positive result is *not* proof of harmonic structure in markets. It is a flag that the harmonic coordinate system reveals patterns worth investigating further.

---

## Methodological Posture

This is a reverent investigator test.

> Reverence without falsifiability becomes belief. Falsifiability without reverence becomes reduction. The path is to bring both together.

The discipline of testing geometry rather than buckets is what keeps the test honest. The discipline of computing holdout regardless of training screen outcome is what keeps the test transparent. The discipline of naming the March 20 proxy honestly is what keeps the test defensible. The discipline of locking the random-anchor seed before computing any real-data PSS is what keeps the null distribution honest. The discipline of resolving the v0.3.2 random-sample contradiction *before* any real-data PSS was computed — and resolving it via the exact, deterministic, finite-population enumeration that the original control space implied — is what keeps the null distribution defensible.

---

*End of design memo. v0.3.3 anchor-control amendment timestamp: 2026-05-12. Protocol locked at v0.3.3. No real-data PSS values, no real SPY phase assignments, and no Commit 4 verdict outputs have been computed.*
