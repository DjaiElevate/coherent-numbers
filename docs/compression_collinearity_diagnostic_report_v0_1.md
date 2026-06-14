# Compression Lane — Collinearity Diagnostic Report v0.1

**Status: SURVIVES FEATURE-SPACE ABSORPTION** — pre-gate feature-space absorption diagnostic (reject-only). NOT a gate, NOT an episode-count audit, NOT a synthetic-null check. No wake/outcome/target was computed. No alpha was spent. No sealed data was accessed.

Authorized by `docs/compression_collinearity_diagnostic_authorization_v0_1.md` (commit `8793efc28bd97f8b5ff4098850c615c5d5ac2ae7`).

## 1. Title and status
Compression pre-gate collinearity diagnostic v0.1. Final status: **SURVIVES FEATURE-SPACE ABSORPTION**.

## 2. Commit / HEAD / origin verification
- repo root: `/Users/jay/Documents/GitHub/coherent-numbers`
- branch: `main`
- HEAD: `8793efc28bd97f8b5ff4098850c615c5d5ac2ae7`
- origin/main: `8793efc28bd97f8b5ff4098850c615c5d5ac2ae7`

## 3. Authorization memo SHA verification
- `docs/compression_collinearity_diagnostic_authorization_v0_1.md` = `d4fc494d5b435798f0906d528333f793da7e34a53f930926ce8509885aca5628` (matches frozen spec)

## 4. Compression Stage-1 memo SHA verification
- `docs/compression_stage1_design_memo_v0_1.md` = `66c54688374c439594546b715d65211340b8680cbe055fca6736c208cea7d420` (matches)

## 5. Sandbox CSV SHA verification
- `data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv` = `5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901` (verified before reading rows)

## 6. Loaded date range and row count
- loaded `2005-01-03` .. `2022-12-30`; input rows = 4531

## 7. Allowed columns only
- input columns asserted to be exactly {`date`, `adj_close`}.

## 8. No rows >= 2023-01-01
- confirmed: zero rows on/after the sealed boundary `2023-01-01`.

## 9. Structural firewall proof
The firewall is structural: the diagnostic constructs only feature-side fields, defines no forward-window functions, creates no wake/outcome/target columns, and makes wake/outcome construction unreachable from the diagnostic data structures.
- no forward-window functions defined;
- no wake/outcome/target columns created (constructed columns checked against an allow-list);
- no future-indexing: source rejected if it contains a negative (future) shift call;
- self-scan result: PASS (no offenders);
- feature-side data structures only (all features use trailing windows ending at t).

## 10. Feature definitions
- **CR_21** = (trailing 21-close range) / (trailing 21-close absolute path length); range = max−min over 21 closes ending at t; path = sum |Δclose| over the 20 increments spanning those 21 closes; invalid if path <= 0.
- **CI_21 = -log(CR_21)** — primary response (frozen transform).
- **CR_10 / CI_10** — descriptive only (not in any decision).
- **log_RV_21** = log of RMS of trailing 21 daily log returns.
- **RV_21_pctile_252** = trailing percentile of RV_21 within its trailing 252-day history ending at t.
- **AC1_21 / AC1_63** = lag-1 autocorrelation of daily log returns over trailing 21 / 63 days.
- **VR5_252** = Lo–MacKinlay (1988) overlap-bias-corrected variance ratio (see §11).
- **ER_21** = |net 21-close displacement| / (trailing 21-close absolute path length); same path denominator family as CR_21.

## 11. VR5_252 exact formula (Lo–MacKinlay 1988 overlap-bias-corrected)
Over a trailing window of `N = 252` daily log returns ending at t, with horizon `k = 5`:
- `mu = mean(r)`
- `var_a = (1/(N-1)) * sum((r - mu)^2)`  (1-period variance)
- overlapping k-sums `ksum_j = r_{j-k+1} + ... + r_j`, for j = k..N  (N-k+1 sums)
- `m = k*(N-k+1)*(1 - k/N)`  (Lo–MacKinlay overlap bias-correction denominator)
- `var_c = (1/m) * sum((ksum - k*mu)^2)`
- `VR5_252 = var_c / var_a`  (→ 1 under a random walk)

This is the Lo–MacKinlay (1988) overlapping bias-corrected variance-ratio estimator, not a simple/uncorrected ratio and not a homebrewed correction.

## 12. Valid diagnostic row count
- valid rows (all primary features + response finite) = 4259

## 13. Fold date ranges and row counts (blocked chronological 5-fold)
| fold | test_start | test_end | test_rows |
|------|------------|----------|-----------|
| 1 | 2006-02-01 | 2009-06-18 | 851 |
| 2 | 2009-06-19 | 2012-11-05 | 852 |
| 3 | 2012-11-06 | 2016-03-28 | 852 |
| 4 | 2016-03-29 | 2019-08-14 | 852 |
| 5 | 2019-08-15 | 2022-12-30 | 852 |

## 14. Blocked cross-validated joint-baseline R²
- **blocked-CV joint-baseline R² = 0.659541**
- model: `CI_21 ~ log_RV_21 + RV_21_pctile_252 + AC1_21 + AC1_63 + VR5_252 + ER_21`
- standardization used training-fold statistics only; OLS with intercept; pooled out-of-fold R².

## 15. Final diagnostic status
**SURVIVES FEATURE-SPACE ABSORPTION** (decision rule: R² ≥ 0.85 → ABSORBED; R² < 0.75 → SURVIVES; [0.75, 0.85) → BORDERLINE-ABSORBED).

## 16. Descriptive in-sample joint R² (descriptive only)
- in-sample joint R² = 0.669801

## 17. Descriptive pairwise correlations (descriptive only)
| baseline | corr(CI_21, baseline) |
|----------|------------------------|
| `log_RV_21` | 0.2139 |
| `RV_21_pctile_252` | 0.2251 |
| `AC1_21` | -0.1448 |
| `AC1_63` | -0.1609 |
| `VR5_252` | -0.0762 |
| `ER_21` | -0.7956 |

## 18. Descriptive baseline ablations — blocked-CV joint R² dropping one baseline (descriptive only)
| ablation | blocked-CV joint R² |
|----------|---------------------|
| drop_log_RV_21 | 0.6605 |
| drop_RV_21_pctile_252 | 0.6613 |
| drop_AC1_21 | 0.6353 |
| drop_AC1_63 | 0.6621 |
| drop_VR5_252 | 0.6615 |
| drop_ER_21 | 0.0262 |

## 19. Descriptive ER-alone absorption (descriptive only)
- `CI_21 ~ ER_21` blocked-CV R² = 0.631063
- residual share over ER alone (1 − ER-alone R²) = 0.368937

## 20. Descriptive outputs did not affect the decision
The decision used ONLY the blocked cross-validated joint-baseline R² (§14) against the frozen threshold band. Pairwise correlations, ablations, in-sample R², and ER-alone results are descriptive only and did not affect the survival/absorption decision.

## 21. Joint R² is a subspace-absorption measure
The joint R² measures whether CI_21 lies within the feature subspace collectively spanned by the frozen baselines. It is not single-baseline attribution; ER-alone reporting only helps localize whether the efficiency-ratio twin does most of the absorption.

## 22. No wake/outcome/target computed
No forward realized volatility, future range, future drawdown, recovery, expansion, or any target `y` was computed.

## 23. No gate run
No sandbox gate was run.

## 24. No episode-count audit run
No distinct-episode feasibility/count audit was run.

## 25. No alpha spent
No sealed attempt occurred; the atlas family alpha budget is untouched.

## 26. No sealed data accessed
No data on/after 2023-01-01 was read or used.

## 27 / 28. Next-step constraint
Status is `SURVIVES FEATURE-SPACE ABSORPTION`. This permits ONLY the next separately-authorized artifact: the distinct-episode feasibility/count audit. It does NOT authorize a gate, does NOT prove predictive information, and spends no alpha.
