# Lane 2 — Count-Only Data-Source Feasibility Protocol

**Version:** v0.1 (protocol for a future feasibility gate; not the run)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Not authorized to execute.

**Source context (committed):**
- Lane 2 Step 1 framework — `357fba585965818da853a6ba560a7ea2b3213c0b`
- Lane 2 Step 2 readiness memo — `af64ee2f5e12d867bc7b70a1afe7d3c41a7c03fa` (concluded **B + D**: data-source feasibility must be resolved first; sample adequacy unknown; next gate is a separately authorized count-only feasibility check)

---

## 1. Status

This document is a **count-only feasibility protocol only**. Explicitly:

- No data access is authorized by this document.
- No GDELT query.
- No market data load.
- No 2023+ access.
- No outcomes.
- No returns.
- No model fitting.
- No Step 2 lock.
- No OOS decision.
- No verdict.

It defines exactly what a **future**, separately authorized count-only
feasibility run may and may not do. It is not that run.

## 2. Purpose

The future feasibility gate may answer **only**:

> Can a reproducible attention-spike event substrate be constructed for
> Lane 2, with enough event counts to make a later Step 2 lock plausible?

It may **not** answer:

- whether markets respond;
- whether attention predicts returns;
- whether prior state modulates response;
- whether the Lane 2 hypothesis is supported.

## 3. Candidate attention sources for feasibility

To be evaluated at documentation / protocol level (none chosen here):

- GDELT 2.0 GKG
- GDELT 2.0 Event database
- GDELT DOC / API-style products
- GDELT 1.0 (only if longer history is needed)
- Google Trends (only if reproducibility is defensible)
- Wikipedia pageviews (only if it can plausibly represent global attention)
- other market-news attention proxies (only if reproducible and freezable)

No source is selected. The protocol does not assert a first-choice source;
selection is itself an output of the future documentation review + feasibility
check, not a decision made here.

## 4. Source-selection criteria

The future feasibility check must evaluate each candidate source against:

- historical coverage;
- daily global attention-intensity availability;
- 2005–2022 feasibility or the required shorter window;
- access mechanism (bulk vs API; auth; rate limits);
- reproducibility;
- freeze / SHA-manifest feasibility;
- vendor / API stability;
- missingness risk;
- volume-normalization risk;
- whether count-only event detection is possible **without content
  interpretation**;
- whether the source risks becoming unavailable or non-reproducible.

## 5. External-data freeze rule

If actual external data is used in any future feasibility run:

- the source must be **frozen before** any count computation;
- file(s) must be **SHA-pinned**;
- a manifest must record source URL/query, access date, coverage window, row
  counts, and content hash;
- **no 2023+ data** may be downloaded, queried, stored, sampled, or counted
  unless separately authorized;
- if a source endpoint cannot restrict to pre-2023, the feasibility run must
  **abort** or require separate approval before proceeding.

## 6. 2023+ seal rule

- 2023+ **remains sealed**.
- The count-only feasibility gate must not access, download, query, inspect,
  sample, count, or reference 2023+.
- If an API returns 2023+ rows by default, they must **not** be accepted
  silently.
- The run must enforce either a hard query/date restriction **or** an abort
  condition.
- Any later use of 2023+ requires a **separate** OOS / seal-consumption
  decision, not granted here.

## 7. What the future feasibility run may compute

Only:

- candidate source availability;
- daily attention-volume series for **pre-2023 only**;
- missingness summaries;
- candidate event counts under pre-declared simple event definitions (§9);
- clustered event counts;
- non-trading-day event counts;
- event-window overlap counts;
- counts by candidate prior-state labels **only if** those state labels are
  computed without any market outcome;
- feasibility of per-fold event counts for a future validation design.

## 8. What the future feasibility run may not compute

It may **not** compute:

- S&P returns; SPY returns; CAR; abnormal returns;
- volatility response; VIX response; any market outcome;
- model fits; M0/M1/M2/M3 comparisons;
- p-values; feature importance;
- success / failure claims;
- attention–response relationships; state–response relationships;
- any 2023+ counts or observations.

## 9. Candidate event definitions for count-only feasibility

Simple definitions to **count, not test**:

- **Option A:** attention spike = daily volume percentile ≥ 95% relative to a
  trailing 60 valid-day baseline.
- **Option B:** attention spike = z-score ≥ 2.5 relative to a trailing 60
  valid-day baseline.
- **Option C:** attention spike = daily attention acceleration /
  rate-of-change above a pre-declared threshold.

The run may compare **event counts** across A/B/C. It may **not** choose the
final Step 2 definition based on market outcomes (there are none in this gate).

## 10. Clustering / overlap feasibility

The future run should count:

- raw spike days;
- clustered spike events under candidate separation windows (e.g., 5, 10, 20
  trading days);
- event-window overlap rate for candidate response windows (e.g., `t+1:t+5`,
  `t+1:t+20`) — **as date-overlap counting only**, no returns computed;
- non-trading-day attention spikes, if the attention data includes
  weekends/holidays.

It must **not** compute market returns for any of those windows.

## 11. Candidate state-axis count feasibility

Because the readiness memo flagged construction-coupling, state-axis families
are kept separate:

- **A. price-derived states** — risky (coupling), but countable;
- **B. implied-vol / stress states** — possible if the source is available
  and pre-2023 only;
- **C. external / news-derived states** — preferred if reproducible;
- **D. hybrid states** — possible but likely too complex for a first Step 2.

For count-only feasibility, state labels may be counted **only if** their data
source is also frozen and pre-2023. **No response outcome may be computed.**

Required reporting: events per state; events per fold; minimum state cell
count; whether an interaction model would be numerically plausible (a
count-feasibility statement only, not a model).

## 12. Sample-adequacy reporting

The future feasibility report should include:

- total daily observations;
- valid daily attention observations;
- raw spike count;
- clustered spike count;
- spike count by year;
- spike count by candidate state;
- spike count by validation fold;
- non-trading-day event count;
- overlap count / overlap percentage;
- missingness by period;
- whether minimum sample adequacy is **plausible** for a later Step 2 lock.

No pass/fail hypothesis verdict — readiness notes only.

## 13. Output artifacts for the future feasibility run

- frozen source manifest;
- count-only feasibility metadata JSON;
- count tables CSV;
- readiness summary markdown;
- plots **only** if purely count / missingness plots;
- **no** market-response plots.

## 14. Feasibility result classes (feasibility only, not hypothesis verdicts)

- **F0** — no suitable source found.
- **F1** — source available but event counts too low.
- **F2** — source available, event counts adequate, state counts inadequate.
- **F3** — source and counts adequate enough for Step 2 lock drafting.
- **F4** — feasibility inconclusive (coverage / missingness / reproducibility).
- **F5** — methodological failure / protocol breach.

These are feasibility classes only. None is a statement about the Lane 2
hypothesis.

## 15. Relationship to Step 2

- A future **F3**-style result would **not** confirm the hypothesis. It would
  only mean Lane 2 is lockable enough to **draft** Step 2.
- A future **F0/F1/F2/F4/F5** result would **not** disprove the hypothesis. It
  would only mean the proposed Lane 2 operationalization is not ready.

## 16. Stop condition

This count-only feasibility protocol does not authorize data access,
implementation, Step 2 locking, OOS use, or any model run. A future
feasibility run requires separate explicit authorization.

— end of count-only feasibility protocol —
