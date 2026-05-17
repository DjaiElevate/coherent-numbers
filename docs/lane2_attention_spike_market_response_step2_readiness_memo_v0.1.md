# Lane 2 — Step 2 Readiness / Data-Source Feasibility Memo

**Version:** v0.1 (readiness assessment only)
**Date:** 2026-05-17
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Not a lock.

**Source context (committed):** `docs/lane2_attention_spike_market_response_framework_memo_v0.1.md` @ `357fba585965818da853a6ba560a7ea2b3213c0b` (Step 1 framework; review passed; already committed — no further Step 1 commit needed).

---

## 1. Status

This is a **Step 2 readiness memo only**. Explicitly:

- No data accessed.
- No GDELT data queried.
- No market data loaded.
- No 2023+ accessed, referenced for design choices, sampled, or consumed.
- No Step 2 lock drafted.
- No implementation created.
- No OOS decision made.

It assesses whether the committed Step 1 framework is ready to become a Step 2
lock, and enumerates the decisions that must be resolved first. It contains no
data-derived facts.

## 2. Current committed state

- Lane 2 Step 1 framework committed at `357fba5`.
- Review passed.
- No overcommitment violations.
- Boundary scan clean.
- Seal-preservation scan clean.
- Soft notes only (non-blocking):
  - §8 phrases "M3 vs M2" as the primary conceptual test, but §8/§12/§15
    keep it unlocked.
  - No verbatim "2023+ not referenced for design choices" sentence, but seal
    preservation is substantively covered by §1 + §4 + §9 of the framework
    memo plus the "no data accessed" stance.

## 3. Purpose of Lane 2

**Research question.** Does the S&P 500 response to a major spike in global
collective attention depend on the prior market nervous-system state?

**Translation.**
- Intuitive language: large human-attention / "consciousness" events may
  affect markets.
- Research language: collective-attention spikes may condition market
  response patterns.
- No direct measurement of consciousness.
- No validation of Hawkins / Orlando / Kryon / influential numbers.
- No base-12.
- No pullback trades.
- No Candidate C extension.
- No rescue of the field-modulated identity null.

## 4. Data-source feasibility questions (to verify before Step 2; not answered from data)

For **each** candidate attention source, Step 2 prerequisites must verify, from
documentation only at this stage:

- historical coverage (start date; continuity);
- access mechanism (bulk download vs API; auth; rate limits);
- reproducibility / freeze requirements (can a fixed snapshot be pinned?);
- volume-normalization problem (raw coverage volume drifts over time);
- missingness / vendor / API-stability risk (schema changes, deprecation);
- whether it supports a **daily global attention-intensity** series;
- whether it supports 2005–2022 or requires a shorter window;
- whether it can be frozen under SHA-pinned manifest discipline (as with the
  existing pullback / SPY / GLD frozen artifacts).

Candidate sources to evaluate at memo level (none chosen here):

- **GDELT 2.0** (GKG / DOC / Event volume).
- **GDELT 1.0** (only if longer history is required).
- **Google Trends** (if considered).
- **Wikipedia pageview / trending volume** (if considered).
- **A simpler market-news proxy** (if considered).

No source is selected. None is documented here as obviously dominant or
obviously infeasible; that determination itself requires the documentation
review named in §15, not data access.

## 5. GDELT-specific readiness issues (discussed without querying data)

- GDELT **product choice matters**: Event database vs GKG vs DOC API are
  distinct products with different variables, cadence, and history.
- GDELT 2.0 vs 1.0, and Event vs GKG vs DOC, may differ in coverage,
  variables, update cadence, and historical availability.
- The historical window may differ across products; the chosen product may
  not reach back to 2005.
- If the chosen GDELT product cannot support 2005–2022, Step 2 must either
  **shorten the development window** or **use a different source** — and that
  choice must be made on documentation, not on observed event counts.
- Attention volume requires **normalization** because total news-coverage
  volume changes substantially over time.
- A trailing-percentile / rolling-baseline transform may partly normalize
  volume but may **not** fully address historical coverage drift.
- Product choice must be **locked before any event count is observed**, to
  avoid choosing the product that yields a convenient event count.

## 6. Market substrate feasibility (no data loaded)

Candidate response sources:

- SPY adjusted close;
- S&P 500 index;
- futures / ETF alternatives.

Issues Step 2 must lock:

- exact instrument;
- adjustment method (total-return / adjusted close vs raw);
- trading calendar;
- abnormal-return baseline (market model vs simple mean);
- event-window alignment to trading days;
- handling of missing trading days around attention events;
- treatment of attention spikes that fall on non-trading days.

## 7. 2023+ seal decision (required)

- 2023+ **remains sealed**.
- Step 1 did **not** authorize OOS use.
- This readiness memo does **not** authorize OOS use.
- Step 2 must **explicitly choose** whether 2023+ remains sealed, is used as a
  final holdout, or is excluded from this study.
- If 2023+ is used, that is a deliberate **seal-consumption decision** and
  must be justified for the specific pre-registered question.
- No Step 2 lock may imply 2023+ consumption by momentum or default.
- This readiness memo references **no** 2023+ observations, outcomes, market
  behavior, event counts, or any data-derived design facts.

## 8. Event-definition readiness

Step 2 must lock:

- attention metric (which series/field);
- rolling-baseline window length;
- threshold form (percentile vs z-score vs acceleration);
- event clustering rule;
- overlapping event-window handling;
- non-trading-day event handling;
- minimum event separation;
- whether attention magnitude is retained as continuous after spike selection;
- whether event class / content is ignored or included.

**Warning.** Sample adequacy must be computed **before** locking any complex
interaction model (carried from framework §8/§11).

## 9. State-axis readiness (Atlas C1 lesson applied)

Step 2 must avoid, or explicitly account for, **construction-coupling**.

Candidate state-variable paths (none chosen):

- price-derived state: prior return / realized vol;
- implied-vol state: VIX percentile;
- cross-asset stress state;
- external / news-derived state;
- hybrid state;
- prior returns as **controls** rather than state labels.

**The state axis must not be mechanically coupled to the response variable in
a way that makes the interaction nearly tautological.**

Carried-forward Atlas v0.1 lesson (a design lesson, **not** a Lane 2
finding): Atlas v0.1 found a weak state-level allocation contrast, but it was
likely construction-coupled because the state axis used prior SPY trend and
prior SPY realized volatility while pullback long/short directionality
plausibly tracked regime by construction. Lane 2 must not repeat that coupling
with an S&P CAR response.

## 10. Response-variable readiness

- `t+1:t+5` CAR is the **primary candidate**.
- Alternatives: same-day-included CAR, 1-day, 20-day, realized-vol response.
- Leakage problem if the event day is defined after market close (timestamp
  semantics must be pinned).
- Abnormal-return baseline choices: market model vs simple mean.
- Exactly **one primary Y** must be locked at Step 2. Not locked here.

## 11. Model readiness

- M0 / M1 / M2 / M3 are **scaffolding only**.
- "M3 vs M2" remains **conceptual, not locked**.
- Step 2 must compute event count and per-state / per-fold adequacy **before**
  locking M3.
- If event counts are low, a simpler descriptive / event-study model may be
  required instead of an interaction model.
- Shuffled-state and random-feature controls remain **candidates, not locks**.

## 12. Sample-adequacy preconditions

Step 2 cannot be locked until feasibility can answer:

- total candidate attention spikes;
- clustered event count;
- events by state;
- events by fold;
- event-window overlap rate;
- number of non-trading-day events;
- minimum cell count under the proposed state definition;
- whether the M3 interaction model is feasible at that count.

These are **count-only** quantities. The first future technical step, **if
any**, should be a separately authorized **count-only feasibility check** that
computes availability and event counts only — not outcomes, not models, not
2023+ (see §15).

## 13. Confounding and reflexivity burden

- Attention can move markets.
- Markets can generate attention.
- Both can be caused by a third external event.
- **Predictive / conditional-response language only.**
- No causal claims without a stronger identification design.

## 14. Step 2 lock readiness rating

**B + D — Not ready. Data-source feasibility must be resolved first (B), and
sample adequacy is unknown until then (D).**

Rationale (no data used): the framework is internally disciplined and
review-passed, but two gating unknowns block a Step 2 lock and **cannot** be
resolved from documentation reasoning alone in a way that fixes the design:
(1) which attention source/product actually supports a reproducible,
freezable daily global attention series over the intended window (§4–§5); and
(2) whether the resulting event count supports any interaction model (§12).
The state-axis construction-coupling burden (C) is also unresolved but is a
**design-decision** burden Step 2 can resolve in the lock itself, given the
framework already names mitigations; it is therefore secondary to B/D as a
*readiness gate*. Rating is not A (not ready to draft a lock) and not E (no
basis yet to recommend abandoning the line).

## 15. Recommended next gate

**One gate: a separately authorized, count-only data-source feasibility
check**, preceded by (or combined with) a documentation review of candidate
sources.

If that count-only feasibility check is later authorized, it **must**:

- be **separately authorized** (this memo does not authorize it);
- **not** access 2023+;
- **not** compute outcomes or returns;
- **not** fit or evaluate any model;
- **only** assess source availability and event counts;
- **freeze** any external data source under SHA-pinned manifest discipline
  **before** use if it touches actual data;
- report counts only (per §12), with no design parameter chosen from the
  observed counts beyond what the lock will later pre-register.

Step 2 lock drafting is **not** recommended yet; pause remains acceptable if
the feasibility gate is not pursued.

## 16. Stop condition

This readiness memo does not authorize Step 2 locking, implementation, data
access, OOS use, or any model run. The next action requires a separate
explicit decision.

— end of Step 2 readiness memo —
