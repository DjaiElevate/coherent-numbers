# Lane 2 — TTG → SPY Estimator & Evaluation Pre-Registration — v1.1 FINAL

> Status: FINAL lockable design document. This commit is design-doc-only; no archive bytes were read, no extraction
> was run, no features were computed, no outcome/market data were read, no statistics were computed, no join was
> performed, and no V1/V2 execution was touched. The single in-sample read remains unspent.
> All design decisions are resolved. The only open execution-blocker is the outcome-data
> `[TO-PIN-BEFORE-EXECUTION]`. A separately-vetted dispatch is required before any read or execution.

---

## LOCKED — frozen inputs

- Archive SHA-256 `06dcbc2530deb9fb25dc87b651f3012fe7de21474235c0f85c7ddd53b604383b`; 505,818,607 rows.
- Coverage-ledger dates 3549; distinct-written 3546 — legitimate Jan-2020 zero-eligible-row nuance:
  `2020-01-03` proven from the per-file table; `2020-01-01/02` corroborated and bug-modes excluded by the per-year match.
- Row eligibility already enforced: `source_file_date ≤ SQLDATE + 1`.
- `2013-03-31` and all `2023-01-01+` are sealed/never-contacted.
- No extraction authorized.

## LOCKED — leakage / timing invariants

- **I1** Feature decision time τ uses archive rows only for event-days `d ≤ τ − 1`.
- **I2** One non-adaptive read; all feature columns enumerated below before the read.
- **I3** Outcome never informs feature selection; all scaling/imputation parameters fit on training folds only.
- **I4** Train/holdout embargo strictly exceeds feature lookback + label horizon + the 1-day halo.
- **I5** Final holdout touched once.
- **I6** Archive SHA re-checked before any read; mismatch = hard fail.

---

## A. Outcome / target definition

- **Instrument:** SPY — confirmed primary instrument.
- **Outcome source/method:** daily SPY **adjusted close** from a later **separately authorized, frozen market-data snapshot**.
  Not fetched or inspected in this design-doc commit.
- **Outcome provenance:** `[TO-PIN-BEFORE-EXECUTION]` — the actual outcome-file SHA/provenance is intentionally
  unpinned; computing it requires a market read not authorized by this design-doc commit. The future dispatch **must first
  freeze and hash the outcome file before any label construction**, recording the SHA here.
- **Label:** `r(T) = adjclose(T+1)/adjclose(T) − 1`. **Class 1** iff `r(T) > 0`; **Class 0** otherwise.
  Exact-zero returns are kept as class 0, not dropped. The exact-zero count is reported; **if it exceeds 3 over the full
  locked sample, stop for reviewed amendment before evaluation.**
- **Cadence:** daily, non-overlapping.
- **Timing:** for label date `T`, features use only TTG event-days `d ≤ T − 1`; no same-day-`T` rows enter the `T→T+1` label.
- **Right edge:** a label exists for trading day `T` only if `T+1` is an available in-sample SPY trading day; consequently
  the final holdout's last label date is the **penultimate** available SPY trading day in the holdout span, so label
  construction never requires 2023 SPY data. **No 2023+ contact is authorized.**

## B. Feature specification

- **Fields:** `sqldate` as time key only; `quadclass` as category; `goldsteinscale`, `nummentions`, and `avgtone` as numeric fields.
- **Strata:** `Q1`, `Q2`, `Q3`, `Q4` separately plus `ALL`.
- **Fixed lookbacks:** 7 and 28 calendar days, relative to the `d ≤ T−1` cutoff.
- **Weighted mean:** `mean_wt(x) = Σ(x · nummentions) / Σ(nummentions)` over eligible written event-rows in the window for the stratum.
- **Irregular-date rule:** skip-and-renormalize. Only valid written days enter sums/denominators; zero-row covered days,
  coverage-loss days, and one-sided/absent days are excluded and counted in the flags. `2020-01-01/02/03` use this same rule;
  the 11 coverage-loss SQLDATEs are never imputed. **No patching, synthesis, or carry-forward.**
- **Empty-window guard:** any undefined continuous feature from a zero denominator, including weighted means and shares, is
  imputed using the **training-fold mean only**, applied forward. Counts and availability flags remain **literal**. No
  validation/holdout information enters imputation or scaling.
- **Left edge:** all labels are included, with **no minimum-fill filter**. Early partial windows are handled by
  skip-and-renormalize, the availability flags, and train-fold-only imputation. Early-window incompleteness is reported via
  the flags, never used for adaptive dropping.

### Feature manifest — exact column list

Naming: `{family}__{stratum}__{window}d`; flags `{flag}__{window}d`. For each `w ∈ {7, 28}`:

- `event_count__{Q1,Q2,Q3,Q4,ALL}__{w}d` (5)
- `total_nummentions__{Q1,Q2,Q3,Q4,ALL}__{w}d` (5)
- `mean_avgtone_wt__{Q1,Q2,Q3,Q4,ALL}__{w}d` (5)
- `mean_goldstein_wt__{Q1,Q2,Q3,Q4,ALL}__{w}d` (5)
- `share_events__{Q1,Q2,Q3,Q4}__{w}d` = stratum event_count / ALL event_count (4)
- `share_nummentions__{Q1,Q2,Q3,Q4}__{w}d` = stratum total_nummentions / ALL total_nummentions (4)
- `flag_valid_written_days__{w}d` (1)
- `flag_zero_row_covered_days__{w}d` (1)
- `flag_coverage_loss_days__{w}d` (1)

This gives 31 columns per window × 2 windows = **62 columns**. `ALL` shares are trivially 1 and are excluded.

## C. Predictor ↔ outcome join

- Calendar-day TTG features mapped onto trading-day SPY labels.
- For label `T`, join features built only from event-days `d ≤ T − 1`.
- Weekends/holidays: windows carried forward only through the pre-`T` cutoff, never through `T` or `T+1`.
- Dates present on only one side are dropped after logging counts.
- No same-day-`T` TTG rows enter the target.
- Label existence is governed by the right-edge rule in §A.
- This section is defined here but executed only after a separate dispatch; it is blocked now.

## D. Sample partition

Expanding-window walk-forward for selection; one final touch-once holdout. Embargo = **35 calendar days** before each evaluated span. Use available SPY trading days only inside each span.

| Fold | Train labels | Embargo | Validation / holdout |
|---|---|---|---|
| 1 | 2013-04-02 … 2016-11-26 | 2016-11-27 … 2016-12-31 | 2017-01-01 … 2017-12-31 |
| 2 | 2013-04-02 … 2017-11-26 | 2017-11-27 … 2017-12-31 | 2018-01-01 … 2018-12-31 |
| 3 | 2013-04-02 … 2018-11-26 | 2018-11-27 … 2018-12-31 | 2019-01-01 … 2019-12-31 |
| 4 | 2013-04-02 … 2019-11-26 | 2019-11-27 … 2019-12-31 | 2020-01-01 … 2020-12-31 |
| Holdout | 2013-04-02 … 2020-11-26 | 2020-11-27 … 2020-12-31 | 2021-01-01 … 2022-12-30 |

- Scaler and model are refit at each expanding step using only data up to that step's train end.
- The final holdout is touched once.
- Embargo sufficiency: 35 days exceeds the 28-day max lookback plus 1 trading-day label horizon plus 1-day eligibility halo, with margin.

## E. Estimator

One locked primary model:

- **Model:** L2-regularized logistic regression.
- `penalty="l2"`
- `C=1.0`
- `solver="lbfgs"`
- `fit_intercept=True`
- `class_weight=None`
- `max_iter=10000`
- `tol=1e-8`
- **No hyperparameter search.**
- **Standardization:** `StandardScaler` fit on the training fold only, applied forward without refitting.
- Package versions are recorded at execution, not during this design-doc commit.
- No max-over-models headline. Optional diagnostics cannot change the primary model.

## F. Evaluation and success criteria

- **Primary metric:** out-of-sample **AUC vs 0.5** on the final holdout.
- **Significance:** stationary block bootstrap, Politis–Romano, as the primary variant.
  - primary expected/mean block length: **21 trading days**
  - bootstrap resamples: **10,000**
  - RNG seed: **20260606**
  - test: **one-sided** for `AUC > 0.5`
  - primary p-value comes only from the 21-trading-day stationary block bootstrap
  - diagnostic sensitivity block lengths: **10 and 42 trading days**; diagnostic only and cannot replace the primary p-value
- **`statistical_confirmed`** = (`AUC > 0.5` and primary bootstrap `p ≤ 0.05`).
- **`practical_material`** = (`AUC ≥ 0.52`).
- The two flags are reported separately and are not merged.
- **Secondary diagnostics:** accuracy vs majority baseline; Brier score / calibration; per-fold validation AUC; simple economic
  sign-rule return/Sharpe. These are diagnostic only, never primary, and never tuned.

## G. Reporting

Report unconditionally, regardless of outcome:

- feature manifest and exact 62-column list
- valid sample counts after join
- missing / zero-row / coverage-loss counts
- exact-zero label-day count
- fold definitions and 35-day embargo
- per-fold validation AUC
- final-holdout AUC
- primary 21-day stationary-block-bootstrap p-value
- 10/42-day bootstrap diagnostics
- baseline comparison
- secondary diagnostics
- both result flags
- deviations log

Any post-lock deviation requires a new reviewed amendment **before** execution.

## H. V1 / V2

- **V1** = the primary locked TTG→SPY directional-classification study above.
- **V2 is not authorized here.**
- Future V2 may be a separately reviewed robustness/amendment path, or explicitly locked same-read robustness later.
- V2 must not silently re-spend the V1 read and must not become a post-hoc second bite at the apple.

## Lock checklist

- [x] SPY confirmed primary.
- [ ] Outcome SHA `[TO-PIN-BEFORE-EXECUTION]`, to be frozen and hashed by the future dispatch.
- [x] Zero-return rule plus exact-zero amendment bound.
- [x] Train-fold-only imputation for means and shares; literal flags.
- [x] Stationary block bootstrap; mean block 21 trading days; diagnostics 10 and 42; 10,000 resamples; seed 20260606; one-sided AUC > 0.5; primary p from 21-day bootstrap only.
- [x] Separate result flags: `statistical_confirmed` and `practical_material`.
- [x] Right edge: penultimate-trading-day label; no 2023 contact.
- [x] Left edge: no minimum-fill filter.
- [x] Exact L2 hyperparameters.
- [x] Walk-forward fold boundaries.
- [ ] Reviewer vet and design-doc-only commit.
- [ ] Future separately vetted execution dispatch.

## Boundary declaration

Locking this design document authorizes nothing on its own. A subsequent separately vetted dispatch must:

1. re-verify the frozen archive SHA,
2. freeze and hash the outcome file and pin it here,
3. execute §B as a single non-adaptive read,
4. execute §C–§F under I1–I6,
5. touch the holdout once.

Until that dispatch, extraction, features, statistics, joins, outcomes, market reads, V1/V2, and 2023+ remain unauthorized. The read remains unspent and the archive remains value-blind. No push.
