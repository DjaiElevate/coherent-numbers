# Lane 2 Trajectory Note v0.1

Lane 2 is trying to understand the market/attention relationship by first testing whether a frozen, audit-safe GDELT event-count substrate can support a valid attention-signal instrument before any market data is touched.

The central rule is the **no-market-data firewall**. The attention instrument must be defined, retrieved, counted, and locked before any market data, asset selection, return window, or Step 2 logic enters the analysis.

The frozen recognized universe is now the substrate. The live index is no longer the default. The §10 capture, with the §6 caveat applied, is the canonical recognized universe.

## First attention object

The first attention object should be:

**Daily aggregate GDELT event count across the daily-resolution portion of the frozen recognized universe.**

The known universe counts are:

- recognized in-window total: `3,647`
- recognized partition: `2 yearly`, `87 monthly`, `3,558 daily`
- after dropping extra yearly `2013`: `3,646` total in-planned recognized identifiers
- daily-resolution recognized units: `3,558`

The first signal should use daily-resolution units only. Monthly and yearly files should not be allocated across days, because that would introduce researcher choice before the instrument is locked.

## Treatment of the four missing 2014 dailies

The target daily partition is:

**3,562 planned daily units**, of which:

- `3,558` are present in the frozen recognized universe;
- `4` are pre-registered known substrate gaps:
  - `2014-01-23`
  - `2014-01-24`
  - `2014-01-25`
  - `2014-03-19`

So the first attention series should be understood as a daily-resolution substrate with **3,558 observable daily files** and **4 known missing daily substrate gaps**. Those four dates are not silently ignored; they are documented absences.

## Direct answer to the four attention-object options

### (a) Per-unit attention level over time

Not the final first signal, but necessary as a small feasibility mechanism.

We do not need full per-unit time series first. But a small sample of per-unit event files is needed to test whether the aggregate daily signal can be built.

### (b) Aggregate attention indexed by date

Yes. This is the first target signal.

More precisely:

**daily aggregate event count over the 3,562 planned daily partition, with 3,558 observable daily files and 4 known substrate gaps.**

### (c) Per-category attention

Not first.

Themes, actors, geography, and categories add extra degrees of freedom. They should only enter after the raw daily attention count instrument is proven feasible and locked.

### (d) Burst/spike-based attention

Derived later from the daily aggregate series.

Any burst/spike rule requires a threshold. That threshold must be specified in a tracked memo **before** any market data enters, and the same threshold must be used later without re-tuning after seeing market correlations.

## Shortest defensible next path

1. Lock the first attention-count object: daily aggregate event counts over the daily-resolution frozen substrate.
2. Run a tiny feasibility test: fetch and count `K = 3–5` sample daily event files from the `3,558` observable daily units.
3. Confirm whether raw event rows can be counted cleanly.
4. If feasible, design the full daily-count build.
5. Only after the daily attention series is built and locked, define any spike/burst transformation.
6. Only after the raw and/or derived attention instrument is locked, introduce market data.

## Load-bearing gates

These remain strict:

- no market data;
- no Step 2;
- no asset/return/window logic;
- frozen universe stays fixed;
- §6 caveat stays fixed;
- daily substrate gaps stay explicitly recorded;
- event-file GETs require explicit authorization;
- spike/burst thresholds must be pre-registered before market data.

## Procedural inertia to avoid

Avoid:

- more live-index diagnostics;
- relitigating H2;
- preserving the old F-class taxonomy by default;
- broad sanity-check cycles for simple trajectory artifacts;
- writing large memos before the first attention-count object is clear.

## Final trajectory

Lane 2 should next test whether a daily aggregate attention-count series can be built from the frozen daily-resolution GDELT substrate: `3,562` planned daily units, `3,558` observable daily files, and `4` pre-registered substrate gaps. The first feasibility test should be a tiny `K = 3–5` event-file fetch/count test with no market data, no Step 2, and no signal-threshold tuning.
