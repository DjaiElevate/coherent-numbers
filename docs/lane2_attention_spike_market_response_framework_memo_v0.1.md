# Lane 2 — Attention-Spike Market Response, Conditioned on Prior Market Nervous State

**Framework memo — Step 1 only**
**Working title:** Attention-Spike Market Response, Conditioned on Prior Market Nervous State
**Version:** v0.1 (Step 1 framework / scoping starter)
**Date:** 2026-05-17
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Not locked.

---

## 1. Status and scope

This is a **Step 1 framework memo only**. Explicitly:

- Not a locked preregistration.
- Not an implementation.
- Not an analysis.
- Not an OOS validation.
- Not a verdict run.
- No data accessed (no source queried, no file loaded, no preview).
- No 2023+ data consumed; the sealed window is untouched.
- No confirmation claim of any kind.

Its only role is to scope a candidate research question, surface design
burdens, and recommend whether a Step 2 lock should later be attempted. No
parameters, thresholds, sources, windows, models, or seeds are decided here.

**Core research question.** Does the S&P 500 response to a major spike in
global collective attention depend on the prior market nervous-system state?

## 2. Relationship to prior work

### A. Relationship to Atlas v0.1

Atlas v0.1 (Human Field × Base-12 Pullback Atlas) is **closed** as a committed
exploratory record. It found that a joint base-12 × nervous-state structure
**could not be formed from well-populated cells** on its substrate (a
resolution-limit result, not a failure). Lane 2 is **not a continuation** of
the atlas. Lane 2 inherits nothing from it except **methodological
discipline**:

- Avoid overbuilt grids before sample adequacy is known.
- Avoid state-axis construction-coupling with the response variable.
- Treat H0 / no coherent structure as a real, equal-weight possible outcome.
- Preserve sealed data unless a candidate is strong enough to justify
  consuming it.

Lane 2 is **not Atlas v0.2** and must not be merged with Atlas v0.1.

### B. Relationship to Candidate C

Candidate C remains a **scoped base-12 vs base-10 allocation-structure
result** under its locked protocol. Lane 2 **does not test Candidate C**,
does not reinterpret it, and **does not use base-12** at all.

### C. Relationship to the field-modulated identity null

The trade-level field-modulated identity study remains **closed (null)**.
Lane 2 uses a **different substrate** (attention-spike events, not pullback
trades), a **different Y** (S&P index response, not trade-level identity), a
**different identity/treatment feature** (attention spike), and a **different
context feature** (prior market nervous state on a non-coupled basis). Lane 2
is **not a rescue** of that null and makes no claim about it.

## 3. Conceptual translation

> **Mystical / intuitive language:** "Big changes in human consciousness
> change the energy of humanity, and that energy affects markets."

> **Research language:** "Major spikes in collective attention may alter or
> reveal market response patterns, and those responses may be conditioned by
> prior market state."

Explicit boundaries on the translation:

- The study **does not measure consciousness directly**.
- It measures **proxies**: collective-attention intensity and market
  nervous-system state.
- It **does not validate** Hawkins levels, Orlando cosmology, Kryon, Spiral
  Dynamics, Integral theory, or influential numbers.
- The **only** extracted idea is **context-dependent expression**: the same
  attention event may express differently under different prior market states.
  This motivates *looking*; it is not a premise, mechanism, or conclusion.

## 4. Candidate substrate (draft, not locked)

**Event substrate.** Daily global attention spikes. Candidate source: a
reproducible global news-flow / collective-attention proxy (e.g., GDELT
event/volume series or an equivalent that can be audit-frozen under the same
SHA-pinned discipline used elsewhere in this repo). Event day `t` is defined
by attention intensity crossing a threshold relative to a trailing baseline.

**Market substrate.** S&P 500 / SPY as the MVP response asset. **No geography
in v0.1.** A geographic "consciousness map" is explicitly deferred.

**Development window.** 2005–2022 as the candidate development window. **2023+
remains sealed** unless a separate, explicit, later OOS decision authorizes
consuming part of the seal for a specific pre-registered question.

No source, threshold, or window is locked here; Step 2 must do that.

## 5. Event-definition candidates (none selected)

- **Option A — percentile:** attention day if global news-flow volume exceeds
  the 95th percentile of a trailing 60-day baseline.
- **Option B — z-score:** attention day if a standardized score exceeds a
  pre-specified threshold.
- **Option C — acceleration:** attention day if attention rate-of-change /
  acceleration exceeds a threshold.

Step 2 must lock exactly one.

**Clustering / de-duplication is a required Step 2 issue.** If multiple
attention spikes occur within a short window, Step 2 must define whether to
keep the first, combine the cluster into one event, or exclude overlaps. **No
event-window overlap may be allowed without a locked rule.** Overlap handling
materially affects both event count and the independence assumptions of any
validation scheme.

## 6. Response-variable candidates (none locked)

- **Primary candidate:** cumulative abnormal return (CAR) from `t+1` to `t+5`,
  to reduce same-day leakage and event-timestamp ambiguity.
- **Alternatives:** CAR from `t` to `t+5` (only if event timestamping is good
  enough); 1-day response; 20-day response; realized-volatility response;
  VIX response.

Step 2 should lock **exactly one primary Y** (others, if retained, are
diagnostic only). Not locked here.

## 7. Prior market nervous-state candidates (construction-coupling is the central burden)

A valence / arousal framing is the natural starting point, but it must avoid
construction-coupling with the response.

- **Candidate valence options:** prior 30-day S&P return; broader market
  breadth; an external sentiment index; news sentiment.
- **Candidate arousal options:** VIX percentile; realized-volatility
  percentile; credit-spread stress; cross-asset volatility stress.

**Required warning.** Because the Lane 2 response is an S&P CAR, defining the
prior state from prior S&P return and S&P realized volatility risks
**construction-coupling and autoregressive confounding** — exactly the C1
caution from Atlas v0.1, where a state axis built from SPY trend/vol was
plausibly mechanically coupled to a regime-tracking response. Step 2 must
explicitly address this. Candidate mitigations to evaluate (not chosen here):

- Use VIX / cross-asset stress rather than only realized SPY volatility.
- Include prior returns as **controls** rather than state-defining variables.
- Define state from **exogenous** attention/news variables rather than market
  price variables.
- Run both a price-derived-state and an external-state version and compare.

This memo names construction-coupling as a **design burden**, not a solved
problem, and does not choose a state definition.

## 8. Model candidates (discussed, not locked)

- **M0:** baseline mean response.
- **M1:** attention magnitude only.
- **M2:** attention magnitude + prior state.
- **M3:** attention magnitude × prior state interaction.

The **primary conceptual test** is **M3 vs M2** — does attention express
differently by prior state?

**Warning.** M3 must not be overparameterized relative to the event count.
Step 2 must compute event count and per-cell adequacy **before** locking any
interaction model. An interaction that the data cannot support is forbidden.

## 9. Validation candidates (discussed, not locked)

- Time-respecting forward-chaining cross-validation on 2005–2022.
- Purge / embargo around event windows to prevent leakage across folds.
- **No random shuffling across time** for primary validation.
- 2023+ sealed OOS only as a **separate later decision**, never automatic.
- Shuffled-state and random-feature controls as possible negative baselines.

## 10. Confounding and reflexivity (required)

- Attention, sentiment, volatility, and prices often move together.
- Market movement can **cause** attention, not only the reverse.
- A single external event can drive **both** attention and price.
- Lead/lag identification is the core challenge of this study.
- A `t+1:t+5` Y reduces same-day feedback but **does not solve causality**.
- Lane 2 should initially make **predictive / conditional-response** claims,
  not causal claims. Causal language is out of scope at Step 1 and would
  require a separate, much stronger identification design.

## 11. Sample adequacy (Step 2 must compute before locking)

Step 2 must compute, before any model lock:

- number of attention spikes;
- number after clustering/de-duplication;
- number per prior-state cell;
- number per validation fold;
- event-window overlap rate;
- whether the M3 interaction model is feasible at that event count.

**Atlas v0.1 lesson, applied:** do not build a large grid or an interaction
model before confirming sample adequacy. If the adequacy floor is not met,
the correct move is to simplify the model or pause — not to proceed.

## 12. Potential verdict classes (scaffolding only)

Not locked. Candidate classes for a future Step 2 verdict map:

- **L0** — no support for state-modulated attention response.
- **L1** — state-modulated attention response supported under the locked
  design.
- **L2** — direct attention effect or direct state effect only; no
  interaction.
- **L3** — unstable / fold-local pattern.
- **L5** — methodologically inadequate (e.g., sample-adequacy floor not met).

These are scaffolding to be re-derived and locked at Step 2, not commitments.

## 13. What Lane 2 would support if positive

Only:

> "Under the locked design, attention-spike market response is conditioned by
> prior market state."

It would **not** support: "human consciousness was measured"; "energy moved
the market"; "influential numbers are validated"; "base-12 is confirmed"; or
"a trading edge exists."

## 14. What Lane 2 does not test (out of scope)

- Geography of consciousness.
- Hawkins / Spiral Dynamics / Integral levels.
- Base-12.
- Pullback signals.
- Candidate C.
- Riemannian / correlation-manifold methods.
- Trade-level field-modulated identity.
- Direct causal proof.

## 15. Step 2 requirements (what a future lock must specify)

A future Step 2 lock, if approved, must specify exactly:

1. data source (audit-frozen, SHA-pinned);
2. event threshold (one of Options A/B/C, fully specified);
3. clustering / de-duplication rule;
4. time window;
5. primary Y (exactly one);
6. state variables (with the construction-coupling decision resolved);
7. confound controls;
8. model class (with M3 feasibility justified by event count);
9. validation split (time-respecting, with purge/embargo);
10. sample-adequacy floor (and the action if unmet);
11. OOS decision (whether/when any 2023+ seal is spent, and on what question);
12. success criterion;
13. failure rule;
14. no-rescue framing;
15. forbidden anchors;
16. exact output artifacts.

## 16. Stop condition

This Step 1 framework does not authorize implementation, data access, OOS
use, or a preregistered run. The next step, if approved, is a Step 2 lock
decision or a decision to pause.

— end of Step 1 framework memo —
