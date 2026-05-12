# Harmonic Calendar × GLD — Design Memo

**Version:** v0.1  
**Date:** May 12, 2026  
**Project:** Coherent Numbers  
**Cell:** Harmonic Calendar × GLD continuous returns  
**Status:** Pre-registered. No GLD data has been loaded, fetched, or inspected. Protocol locked.  
**Parent decisions:** Cell-Selection Decision Memo v0.1 (commit `f6dac6e`); Microscope/Instrument Program Charter v0.1 (commit `2dcf340`); SPY v0.3.3 protocol (commit `9ea89ae`).

---

## Purpose

This memo specifies the design of the first cross-asset extension of the harmonic calendar test under the Microscope/Instrument Program Charter. It inherits the v0.3.3 protocol structure intact and adds one new matrix dimension: asset.

The cell asks: does the v0.3.3 harmonic calendar lens resolve structure in GLD daily continuous returns over the asset's full available history? The verdict is interpreted under the same per-outcome, three-state summary structure used for SPY: positive, partial/mixed, or null per outcome.

This memo is a design memo only. No data is loaded. No PSS is computed. No phase assignments are made against real GLD data. The frozen GLD CSV is acquired in a separate audit-chain commit after this memo lands.

---

## Inheritance from v0.3.3

The following elements are inherited from `docs/harmonic_calendar_design_memo_v0.3.3.md` without modification:

- **Lens:** 108-phase harmonic calendar, anchored at civil-date March 20 each year, computed as `solar_phase = floor((days_since_most_recent_march_20 / 365.2422) × 108)`, integer range 0-107.
- **Outcomes:** Daily log return; daily squared log return (volatility proxy).
- **Controls:** January-anchored 108-phase calendar; Gregorian month; exhaustive enumeration of all 365 integer-DOY anchor 108-phase calendars.
- **Anchor-control method:** Exhaustive enumeration, `enumerate_anchor_doys()` returning `list(range(1, 366))`.
- **Anchor-control population size:** 365.
- **Strict-rank convention:** Pass/fail via integer rank counts, ties do not help March20 pass.
- **Training rank threshold:** strictly_below ≥ 347 (= ceil(0.95 × 365)).
- **Holdout rank threshold:** strictly_below ≥ 329 (= ceil(0.90 × 365)).
- **Holdout primary subgates:** PSS_oos rank pass AND PSS_oos > 0 in absolute terms.
- **Auxiliary criterion:** March20 PSS_oos > January-anchored-108 PSS_oos AND March20 PSS_oos > Gregorian-month PSS_oos.
- **Three-threshold success criterion (per outcome):** Training screen pass AND holdout primary pass AND auxiliary pass.
- **Per-outcome verdict structure:** Each outcome receives an independent verdict; the three-state summary (positive/partial-mixed/null) is reported per the SPY memo.
- **Holdout-transparency clause:** A training-screen pass that does not survive holdout is reported descriptively but does not constitute a positive verdict.
- **Secondary diagnostics gate:** Per-phase means with FDR correction computed only for outcomes whose primary criterion passes.
- **`RANDOM_ANCHOR_SEED = 20260512`:** Preserved as audit-traceability constant; not consumed by the exhaustive anchor-control null.

The lens, controls, thresholds, percentile convention, success criterion, and verdict structure are referenced from v0.3.3 rather than restated. Any future amendment to v0.3.3 does not retroactively modify this cell's locked spec; this cell uses the v0.3.3 elements as they exist at the commit hash referenced above.

---

## Asset specification

**Asset:** SPDR Gold Shares ETF, NYSE Arca symbol GLD.

**Why GLD over alternatives.** GLD is structurally closer to SPY than other plausible cross-asset extensions (BTC, individual gold futures contracts, other gold-tracking instruments). It is an exchange-traded fund with standard trading-day structure, dividend/split adjustments handled by the data source, single primary listing, and continuous-return semantics compatible with the SPY analysis pipeline. The asset-agnostic orchestration code authored for the SPY protocol runs on GLD with no semantic changes; the only required additions are data acquisition and a new memo.

**Inception:** 2004-11-18. This is GLD's first trading date and the earliest possible observation in the dataset.

**Continuous returns, not pullback events.** This cell tests the harmonic calendar lens on daily continuous log returns, not on the pullback-trade population that includes GLD in the Phase 3b universe expansion. The pullback-universe GLD work is a different analytical context (pullback-trade outcomes conditioned on a specific entry trigger) and is not the data underlying this cell.

---

## Data source and frozen-data procedure

**Source:** Yahoo Finance v8 chart API, matching the SPY precedent. Field: `indicators.adjclose[0].adjclose`, adjusted close prices.

**Why Yahoo v8.** The SPY frozen CSV was acquired via Yahoo v8 (commit `ed199bd`). Using the same source for GLD preserves source-comparability across cells and avoids introducing a new vendor selection as an additional degree of freedom. If a future cell requires a different source (e.g., for an asset Yahoo does not cover), that's a per-cell decision documented in that cell's design memo.

**Date range to be frozen:** 2004-11-18 (GLD inception) through 2024-12-31. The terminus matches the SPY frozen-data terminus, preserving cross-cell calendar comparability of the data span. Total expected trading days: approximately 5,063 (20.1 calendar years × ~252 trading days per year, with one day dropped for first-row log-return computation matching the SPY loader convention).

**Acquisition procedure.** Mirrors the SPY pattern from commits `30faabb` and `ed199bd`:

1. The acquisition function (`acquire_gld_from_yahoo` or equivalent) is authored as part of the GLD orchestration code, marked `ACQUISITION FUNCTION / RUN ONCE / NOT the canonical loader`, and not invoked from analysis code. It exists in the repo as historical/utility code only.
2. The canonical loader (`load_gld` or equivalent) reads from disk only and is the only function invoked from the protocol runner.
3. Data acquisition is a separate audit-chain commit, performed after this design memo is committed and before any protocol orchestration tests are run. The frozen CSV's SHA256 is recorded in that commit's message and is the canonical reference for all subsequent cell work.
4. The frozen CSV filename includes the source identifier, date range, and SHA256, following the SPY precedent: `gld_yahoo_v8_<start>_<end>_<sha256>.csv`.

**No GLD data is loaded prior to this design memo's commit.** This rule is operational, not aspirational. Any GLD data inspection, network fetch, or analysis prior to this memo's commit voids the pre-registration discipline for this cell.

---

## Train/holdout split

### The choice

GLD's first traded date is 2004-11-18 (ETF inception). The frozen GLD dataset for this cell ends at 2024-12-31, matching the SPY freeze terminus. The total available history is therefore approximately 20.1 years.

The SPY v0.3.3 protocol used a train/holdout split of 1993-01-29 through 2014-12-31 (training, ~22 years) and 2015-01-01 through 2024-12-31 (holdout, 10 years), a roughly 69/31 ratio. Applying that split rule to GLD admits three pre-registered options.

**Option 1 — Inherit the "final 10 calendar years as holdout" rule.** Training: GLD inception (2004-11-18) through 2014-12-31, approximately 10.1 years. Holdout: 2015-01-01 through 2024-12-31, 10 years. Train/holdout ratio: approximately 50/50.

**Option 2 — Proportional split matched to SPY's ~69/31 ratio.** Training: GLD inception through approximately 2018-09, roughly 13.9 years. Holdout: approximately 2018-09 through 2024-12-31, roughly 6.2 years. Train/holdout ratio: ~69/31.

**Option 3 — Another pre-registered split rule with explicit justification before GLD data contact.** Reserved for the case that a specific structural feature of GLD's history makes neither Option 1 nor Option 2 defensible. No such feature is identified.

### Trade-off

The choice trades two kinds of comparability against each other.

**Calendar comparability** (Option 1's strength): both SPY and GLD have identical holdout windows (2015-2024). Cross-asset comparisons can ask "what did this lens see in the same calendar decade across two assets?" with no ambiguity about test windows differing.

**Structural comparability** (Option 2's strength): training power is matched in proportion. The PSS_in null distribution's width and the underlying per-anchor PSS estimates scale with the training population size; a ~10-year GLD training window produces noisier per-anchor estimates than a ~22-year SPY training window. Option 2 preserves the inferential profile by giving GLD a proportionally similar training window relative to its history.

The two comparabilities cannot both be preserved on a shorter-history asset.

### Decision

**Option 1 is selected.** Training: GLD inception (2004-11-18) through 2014-12-31. Holdout: 2015-01-01 through 2024-12-31.

### Justification

Three considerations support Option 1.

First, protocol continuity is the cleanest charter posture. The charter treats each cell as standing on its own pre-registered terms; this is more disciplined when the protocol structure is inherited intact across cells rather than tuned per-asset. Custom split rules per asset would, over time, accumulate into a per-asset protocol family harder to compare than a single inherited rule with documented asymmetries.

Second, the holdout-transparency clause from the SPY protocol carries forward: a training-screen pass that does not survive holdout is not a finding. The 10-year GLD holdout provides the same holdout window length as SPY (2015-2024), which is the part of the protocol most directly load-bearing for the verdict. A shorter holdout under Option 2 would weaken the test where it matters most.

Third, the training-power asymmetry that Option 2 would correct is real but addressable through pre-registered disclosure rather than through a new split rule. The interpretation caveat below states the asymmetry explicitly and locks it before data contact.

### Interpretation caveat (pre-registered)

The training period for the GLD cell is approximately 10.1 years, versus approximately 22 years for SPY. This is a property of GLD's shorter available history, not a design choice. The strict-rank convention remains fixed — March20 must still beat 347 of 365 anchors in training and 329 of 365 in holdout — but the shorter GLD training window means each anchor's PSS estimate is based on fewer observations than in SPY. Therefore, the GLD training screen has different power characteristics from the SPY training screen even though the rank rule is identical. This is accepted as a limitation of the GLD cell and must be considered when comparing GLD to SPY.

A null verdict on GLD carries less power than a null verdict on SPY in the way that any shorter time series carries less evidence than a longer one. A positive verdict on GLD would be interpretable against the holdout window directly and would not be discounted for the training-window asymmetry, because the holdout window length is matched to SPY's.

---

## Operational rules

The following rules are inherited from the SPY protocol pattern and apply to this cell:

- No GLD data is loaded into any analysis path before the data-acquisition commit lands as a separate audit-chain entry.
- The protocol runner is executed exactly once against the frozen GLD CSV. Re-runs are permitted only for report-label fixes (matching the SPY precedent where the v0.3.2/v0.3.3 H1 label was corrected) and must produce byte-identical numerical results.
- Results artifacts are persisted in `results/` under the naming convention `harmonic_calendar_gld_results_<YYYYMMDD>_<datahashprefix>.{json,md}`.
- No exploratory follow-ups, no rescue analysis, no parameter changes, no additional anchors, no additional outcomes, no additional controls, no energy-conditioning, no time-energy coupling.
- The frozen GLD CSV is not modified after acquisition.

## Expected audit chain after cell completion

Expected order after the GLD cell is complete:

- `[results commit]` — Run locked harmonic calendar protocol on GLD
- `[acquisition]` — Freeze GLD Yahoo v8 raw data
- `[this memo]` — Add harmonic calendar GLD design memo (v0.1)
- `f6dac6e` — Add Cell-Selection Decision Memo (v0.1): select Harmonic Calendar × GLD
- `2dcf340` — Add Microscope Instrument Program charter (v0.1)
- `371ca9c` — Add Harmonic Calendar MVT closure memo
- `...` — SPY chain continues

Three commits are anticipated for this cell: this design memo (locked spec), the data acquisition commit (frozen CSV), and the protocol-run commit (results artifacts).

## Status of this memo

v0.1. The protocol is locked. No data has been loaded. The expected next artifact is the GLD data-acquisition commit, which freezes the GLD CSV and records its SHA256. No protocol orchestration is implemented or run prior to that commit.
