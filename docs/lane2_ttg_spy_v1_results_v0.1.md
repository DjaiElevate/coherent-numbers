# Lane 2 — TTG → SPY v1.1 Execution Results v0.1 (value-safe)

> Status: results of the single non-adaptive in-sample read, executed under the locked prereg v1.1 plus the
> zero-return handling amendment §5 gate. Aggregate metrics/counts and structural fingerprints only — no
> prices, returns, feature values, per-row labels, per-row predictions, or SOURCEURL. Run ID `20260606T075348Z`.
> **Outcome reported as-is: the primary criterion is NOT confirmed (a weak/null result). No adjustment,
> re-read, or re-run was performed.** This report is uncommitted, for byte-review.

## Reproducibility anchors (all re-verified at runtime)

| Artifact | SHA-256 |
|---|---|
| archive (`ttg_approved_fields_archive.csv`) | `06dcbc2530deb9fb25dc87b651f3012fe7de21474235c0f85c7ddd53b604383b` |
| pinned SPY CSV | `2842647c318c95bd02bc888ee70361d8242ddf8223281e49a8231ea3d91aa055` |
| prereg v1.1 | `860f33b632d23005b4365893c3ab19fee26de8ba0879a951d77f37b0f72bce3f` |
| SPY pin doc | `f9b05e856b224e59ea2e77b93377b09548445e9e159858a4743be2a8d6da4b18` |
| environment note | `402440e2581a48408e819427231199c26946ce60abef15a5ede032b62ae433bc` |
| zero-return amendment | `f7aeda338604187fb28c8d081fe46c61ed3596f32e49716b37b0eb25635d5a22` |

Package versions: python 3.8.2, numpy 1.24.4, pandas 2.0.3, scipy 1.10.1, scikit-learn 1.3.2, joblib 1.4.2, threadpoolctl 3.5.0.

## Labels and §5 source-bound exact-zero gate

- SPY trading days 2457; labels 2456 (first `2013-04-02`, last `2022-12-29` — penultimate trading day per right edge; no 2023 contact).
- Class balance (all labels): class1 1343, class0 1113.
- **Exact-zero count = 7**, equals the amendment-required value; **all 7 exact-zero ties assigned class 0** ✓. The amendment §5 gate replaced the retired `exact-zero > 3` tripwire and passed.

## Single non-adaptive archive feature read

- Rows read: **505,818,607** in **127** streamed chunks; `streaming_chunked_used = true`, `whole_archive_in_memory_load = false`.
- QuadClass values seen: {1, 2, 3, 4}. Distinct written days: 3546; zero-row-covered days: 3.
- Feature matrix: **2456 rows × 62 columns** (exact locked 62-column manifest).
- NaN/imputation: `nan_total = 36` — confined to **1 row** (the earliest label date, whose 7d/28d windows precede the archive start) across the 36 imputable mean/share columns; imputed with **training-fold means only**. Counts and availability flags are literal.
- Join: joined rows 2456; one-sided drops 0; `d <= T-1` enforced (no same-day-T rows enter the T→T+1 label); 2023+ absent; 2013-03-31 absent.

## I4 embargo / runtime margin (days; strictly > 0 required)

| Split | margin (days) |
|---|---|
| Fold 1 | 8 |
| Fold 2 | 8 |
| Fold 3 | 8 |
| Fold 4 | 8 |
| Holdout | 10 |

All margins > 0: the earliest event-day entering each validation/holdout feature window is strictly after the latest training outcome day for that split. (Runtime assertion only; not used for tuning.)

## Fold definitions and counts

| Fold | train rows | val rows | validation AUC (diagnostic) |
|---|---|---|---|
| 1 (val 2017) | 923 | 251 | 0.4811 |
| 2 (val 2018) | 1174 | 251 | 0.4479 |
| 3 (val 2019) | 1426 | 252 | 0.5529 |
| 4 (val 2020) | 1678 | 253 | 0.5577 |

Validation AUC is diagnostic only and was not inspected before holdout evaluation.

## Final holdout (touched once)

- Final training rows 1930; holdout rows **502** (class1 255, class0 247; both classes present).
- **Final holdout AUC = 0.5266** (primary metric).
- Stationary block bootstrap — primary (mean block **21** trading days, **10,000** resamples, seed **20260606**, one-sided AUC > 0.5):
  - **primary p-value = 0.1662** (10,000 valid resamples, 0 single-class); bootstrap AUC mean 0.5252, [p05 0.4794, p95 0.5667].
- Diagnostic bootstraps (cannot replace primary): block 10 → p = 0.1740; block 42 → p = 0.1601.

### Result flags (locked)

- `statistical_confirmed = (AUC > 0.5 AND primary p ≤ 0.05)` → **False** (p = 0.1662).
- `practical_material = (AUC ≥ 0.52)` → **True** (AUC = 0.5266).
- Reported separately and not merged.

### Secondary diagnostics (diagnostic only, never tuned)

- Holdout accuracy 0.4960 vs majority-baseline accuracy 0.5079 (model **below** majority baseline).
- Brier score 0.2554.
- Economic sign-rule (long/short by predicted class): mean daily ≈ −7.85e-5; annualized Sharpe ≈ −0.10.

## Bootstrap implementation

Local stationary block bootstrap (Politis & Romano 1994): iid Geometric(p = 1/mean_block) block lengths via
`numpy.random.Generator.geometric` (≥1, mean = mean_block); uniform start index; circular wrap preserving
within-block time order; blocks concatenated to length n then truncated; resample paired (y_true, y_score);
AUC via `sklearn.metrics.roc_auc_score`; one-sided p = (1 + #{AUC* ≤ 0.5}) / (valid + 1); single-class
resamples excluded and counted; RNG `numpy.random.default_rng(20260606)` per block length.

## Deviations log

- None. No locked choice (model, hyperparameters, scaler, features, folds, embargo, metric, bootstrap, seed,
  thresholds, single-read, holdout-once, I1–I6, V1/V2 boundary) was changed. The only change versus the prior
  attempt is the amendment-specified replacement of the `exact-zero > 3` tripwire by the §5 source-bound gate.

## Interpretation (reported as-is)

The locked primary criterion `statistical_confirmed` is **False**: holdout AUC 0.5266 is not significantly above
0.5 (primary one-sided block-bootstrap p = 0.166; bootstrap 5th percentile below 0.5), and the diagnostic 10/42
block lengths agree (p ≈ 0.16–0.17). Although the AUC point estimate is marginally above the 0.52 materiality
mark (`practical_material = True`), the secondary diagnostics are unfavorable (holdout accuracy below the majority
baseline; slightly negative sign-rule Sharpe) and validation AUC is mixed across folds. **This is a weak / null
result and is recorded as the terminal scientific outcome.** Per the prereg and amendment, a null/weak result is
valid and is NOT a basis to adjust the model, features, folds, metric, thresholds, source, or bootstrap, nor to
re-read or re-run. The single in-sample read is now spent. V2 remains unauthorized.
