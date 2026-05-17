# Lane 2 — GDELT 1.0 Count-Only Feasibility Run Authorization

**Version:** v0.1 (run-authorization memo; not the run)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Authorizes nothing until committed and the retrieval wiring separately passes review.

**Governing / source context (committed):**
- Step 1 framework — `357fba585965818da853a6ba560a7ea2b3213c0b`
- Step 2 readiness memo — `af64ee2f5e12d867bc7b70a1afe7d3c41a7c03fa`
- Count-only feasibility protocol — `147c0d40568636ba0cf24ca00cc39c330e77ea03` (**binding**)
- Source-selection + count-feasibility authorization — `8fef80db0e103d2c22e36d589fe041abd1fb4c78`
- Count-only scaffold — `ba457a892a3f47c339a32db3f8ba45bba2bf9f14`
- Metadata-gap closure — `925b74aedbedcbf14c4f5d657612f10c57dfcfb4`
- Retrieval-freeze scaffolding — `656dc3043e87aa80e9134cdc1c0dea261932eac4`
- Archive-layout mismatch detection — `57847d439ea454f8fc7eab013c35fad615697236`

---

## 1. Status

- Run-authorization memo only.
- No data accessed in drafting.
- No GDELT queried in drafting.
- No API called in drafting.
- No market data loaded.
- No 2023+ touched, referenced, sampled, counted, or consumed.
- No Step 2 lock drafted.
- No model run.
- No hypothesis test.
- No outcome computation.

This memo pins the remaining run parameters and the allowed retrieval/count
behavior. It does not itself run anything.

## 2. Purpose

Authorize **one** future count-only feasibility run, **after** the retrieval
wiring patch separately passes review.

The run may answer **only**:
- Can GDELT 1.0 be frozen reproducibly over the pre-2023 window?
- Can a daily count-only attention series be built?
- Are raw/clustered spike counts plausibly sufficient for future Step 2
  drafting?
- Does the 2013 GDELT regime boundary or secular volume drift make the source
  infeasible or inconclusive?

The run may **not** answer: whether attention predicts market response;
whether prior state modulates response; whether the Lane 2 hypothesis is true;
whether any trading edge exists.

## 3. Source/product

- **Source/product: GDELT 1.0 Event database.**
- This is **still not a Step 2 source lock**.
- It is only the source for this count-only feasibility run.

## 4. Coverage window

- **2005-01-01 through 2022-12-31 inclusive.**
- No 2023+ access.
- If retrieval cannot enforce the pre-2023 restriction, the run must
  **abort** (no fallback that touches 2023+).

## 5. Normalization choice

- **`gdelt_normalization_files_status = "not_used"`** (pinned).

Rationale: the first feasibility run uses raw GDELT 1.0 row/event-volume
counts only — simple and transparent. By-year counts and late-window
concentration flags (§12) will reveal whether raw volume drift makes the
source infeasible or inconclusive. Not using normalization is **not** a
hypothesis choice. If drift is severe, a later, separately authorized
normalized feasibility run may be considered.

## 6. Event definitions authorized

Authorize **only Options A and B**:

- **Option A:** attention spike = daily event-volume percentile ≥ 95%
  relative to a trailing 60 valid pre-2023-day baseline.
- **Option B:** attention spike = z-score ≥ 2.5 relative to a trailing 60
  valid pre-2023-day baseline.

**Option C is disabled for this run:** `option_c_threshold = null`;
acceleration / rate-of-change is not evaluated; no silent default threshold
is allowed (the implementation already raises if Option C is called without an
explicit threshold).

## 7. Clustering windows

Authorize count-only clustering for **5, 10, and 20 calendar days**. The
**primary feasibility floor** (§8) is evaluated on **10-day clustered events**
under **either Option A or Option B**.

## 8. min_event_floor

- **`min_event_floor = 100` clustered events** (pinned).

Rationale: a minimum practical sample-size floor for later simple event-study
feasibility. It is **not** a hypothesis success criterion, **not** a market
result, and does **not** by itself imply Step 2 is ready. If no authorized
event definition reaches 100 clustered events under the 10-day clustering
rule, classify source event-count feasibility as **F1**.

## 9. State-axis feasibility

- No state source is selected for this run.
- No SPY, VIX, returns, CAR, or market data may be loaded.
- State-count feasibility remains **unresolved** in this run.
- Because state feasibility is unresolved, **F3 may not be reachable** from
  this run unless source-count feasibility *and* state-count feasibility can
  both be established without market outcomes and without violating protocol
  (not expected here).
- The run reports `state_count_feasibility_status = "unresolved"`.

## 10. Feasibility classification rules

The run must assign exactly one F0–F5 class:

- **F0** — no suitable source found, or no source could be frozen.
- **F1** — source available/frozen but no authorized event definition reaches
  `min_event_floor = 100` under 10-day clustering.
- **F2** — source available and event counts adequate, but state-count
  feasibility unresolved or inadequate.
- **F3** — only if source counts *and* state counts are both adequate enough
  for Step 2 lock drafting. With no state source selected, F3 is expected to
  be **unreachable** unless state feasibility can be established without market
  outcomes and without protocol violation.
- **F4** — feasibility inconclusive: coverage, missingness, archive-layout
  mismatch, 2013 regime-boundary discontinuity, severe volume drift, or
  reproducibility problem.
- **F5** — methodological failure or protocol breach, including any 2023+
  breach or any prohibited computation.

**F3 does not confirm the hypothesis. F0/F1/F2/F4/F5 do not disprove it.**

## 11. Archive-layout verification rule

Before any count computation, the run must: verify archive layout against the
planned file list; verify the 2013-04-01 regime boundary; report missing
files, unexpected files, naming issues, and **file/date-unit mismatches**
(dedicated category). If actual layout differs from the documented-overridable
assumptions, classify as **F4** or abort pending separate approval.

**No count computation may proceed if:** 2023+ files/rows appear; date
restrictions fail; a file/date-unit mismatch touches 2023+; or the archive
layout cannot be reconciled without a new decision.

## 12. Drift / concentration flags

The run must report: daily observation counts by year; raw spike counts by
year; clustered spike counts by year; whether spike candidates are
disproportionately concentrated after 2013-04-01; whether they are
disproportionately concentrated in later years.

These are **feasibility flags, not hypothesis evidence** — descriptive only;
no market outcomes computed.

## 13. Retrieval enablement mechanism

After this memo is committed and reviewed, a **future implementation patch**
(separately reviewed) may enable the one count-only run by:

- setting `REAL_RETRIEVAL_ENABLED = True` only for the run
  implementation/commit;
- wiring the runner to use the real retrieval path **only after all runner
  guards pass**;
- requiring `--authorize-count-feasibility-run`;
- requiring env `LANE2_COUNT_FEASIBILITY_AUTHORIZED=1`;
- preserving the code-constant guard;
- preserving the no-2023 hard guards;
- preserving the injected/controlled retrieval path (no hidden default
  network client);
- writing outputs only to a fresh timestamped directory;
- restoring the inert default after the run in a **separate safety commit**
  if the runner or module is left permissive.

**No run is authorized without all guards.**

## 14. One-run-only scope

Authorize **exactly one** count-only feasibility run after the implementation
wiring passes review. **No rerun** if counts are surprising, the source is
messy, the F-class is disappointing, or threshold choices feel wrong. If the
run fails due to a technical/protocol issue, record **F5** or stop for human
review; do not patch and rerun without a new authorization.

## 15. Outputs authorized

Source freeze manifest; count-only feasibility metadata JSON; daily count
table CSV; missingness table CSV; by-year count summary CSV; spike-count
tables for Options A/B; clustering-count tables for 5/10/20 days; overlap-count
table; feasibility summary markdown. **No** market-response plots; **no**
outcome plots; **no** return data; **no** model outputs; **no** p-values.

## 16. Prohibited outputs

S&P/SPY returns; CAR; abnormal returns; market-outcome variables; VIX
response; model fits; p-values; feature importance; attention–response
relationships; state–response relationships; Step 2 lock; hypothesis verdicts;
any 2023+ counts or observations.

## 17. Metadata requirements

Run metadata must include: governing commits; selected source/product;
coverage window; `gdelt_normalization_files_status = "not_used"`;
`min_event_floor = 100`; `option_c_threshold = null`; `option_c_enabled =
false` (if supported); `no_2023plus = true`; `outcomes_computed = false`;
`returns_computed = false`; `models_fit = false`; `p_values_computed = false`;
`step2_lock_drafted = false`; `feasibility_only = true`; `hypothesis_verdict =
false`; `feasibility_class` ∈ {F0…F5}; `state_count_feasibility_status`;
`gdelt_2013_regime_boundary_handled`; `archive_layout_status`;
`by_year_counts_reported = true`; `run_authorization_memo` path
(`docs/lane2_gdelt1_count_feasibility_run_authorization_v0.1.md`).

## 18. Stop condition

This run-authorization memo does not itself download data, query GDELT, call
APIs, touch 2023+, compute counts, or run the feasibility check. It authorizes
exactly one future count-only feasibility run only after retrieval wiring
passes review. The run may compute counts and availability only, under the
constraints above.

— end of run-authorization memo —
