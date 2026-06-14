# Compression Lane — Second Distinctness Diagnostic Report v0.1

**Status: SURVIVES NON-TAUTOLOGICAL PATH-ROUGHNESS DISTINCTNESS TEST** — second feature-side distinctness diagnostic (non-tautological path-roughness family; reject-only). NOT a gate, NOT an episode-count audit, NOT a synthetic-null check. No wake/outcome/target was computed. No alpha was spent. No sealed data was accessed.

Authorized by `docs/compression_second_distinctness_diagnostic_authorization_v0_1.md` (commit `7f1a7d00060469d91c3e24a487a58bf4d4608056`).

## 1. Title and status
Compression second distinctness diagnostic v0.1. Final status: **SURVIVES NON-TAUTOLOGICAL PATH-ROUGHNESS DISTINCTNESS TEST**.

## 2. Commit / HEAD / origin verification
- repo root: `/Users/jay/Documents/GitHub/coherent-numbers`
- branch: `main`
- HEAD: `7f1a7d00060469d91c3e24a487a58bf4d4608056`
- origin/main: `7f1a7d00060469d91c3e24a487a58bf4d4608056`

## 3. Authorization memo SHA verification
- `docs/compression_second_distinctness_diagnostic_authorization_v0_1.md` = `4fc606b4c7f6de58c5dbb02ab46f8aa54bd28d44244052d462ba9b412b87c00d` (matches frozen spec)

## 4. Prior diagnostic report SHA verification
- `docs/compression_collinearity_diagnostic_report_v0_1.md` = `b2189ae590a582706b4e60f61082f8525bf02ee3426dcf8b4d8f0d113c1ff9d4` (matches)

## 5. CR distinctness memo SHA verification
- `docs/compression_cr_distinctness_reclassification_memo_v0_1.md` = `a53c75ace9f2f695c25c0e6e3f11db0bec65015c87f0990e5c51cc403457946c` (matches)

## 6. Sandbox CSV SHA verification
- `data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv` = `5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901` (verified before reading rows)

## 7. Loaded date range and row count
- loaded `2005-01-03` .. `2022-12-30`; input rows = 4531

## 8. Allowed columns only
- input columns asserted to be exactly {`date`, `adj_close`}.

## 9. No rows >= 2023-01-01
- confirmed: zero rows on/after the sealed boundary `2023-01-01`.

## 10. Structural firewall proof
The firewall is structural: the diagnostic constructs only feature-side fields, defines no forward-window functions, creates no wake/outcome/target columns, and makes wake/outcome construction unreachable from the diagnostic data structures.
- no forward-window functions defined;
- no wake/outcome/target columns created (constructed columns checked against an allow-list);
- no future-indexing: source rejected if it contains a negative (future) shift call;
- self-scan result: PASS (no offenders);
- feature-side data structures only (all features use trailing windows ending at t).

## 11. Feature definitions
- **CR_21** = (trailing 21-close range) / (trailing 21-close absolute path length); **CI_21 = -log(CR_21)** (response).
- **ER_21** = |close_t − close_start| / path_21 (endpoint-displacement extent).
- **LOG_TORT_21** = log(path_21 / |close_t − close_start|) = −log(ER_21) where defined (same endpoint-displacement axis, log form).
- **KATZ_FD_FIRST_21** = log(20) / (log(20) + log(d_first / path_21)), d_first = max|close_i − close_start| over the window (first-point-distance extent).

## 12. Analytical identity disclosure (deterministic response transforms)
- `RANGE_PATH_ROUGHNESS_21 = path_21 / range_21 = exp(CI_21)` — numerically verified: max abs deviation from exp(CI_21) = 8.882e-16
- `KATZ_FD_RANGE_21 = log(20) / (log(20) - CI_21)` — numerically verified: max abs deviation from the formula = 0.000e+00

> A deterministic transform of the response is not a predictive discovery. It is an identification result.

## 13. Both response transforms excluded from Level-1
`RANGE_PATH_ROUGHNESS_21` and `KATZ_FD_RANGE_21` are deterministic response transforms and are **excluded** from the Level-1 decision model. A self-scan asserts neither appears in the Level-1 predictor set.

## 14. Level-1 formula
`CI_21 ~ ER_21 + LOG_TORT_21 + KATZ_FD_FIRST_21`

## 15. Extent-span interpretation
The Level-1 set spans two independent extent concepts, not three. `ER_21` and `LOG_TORT_21` are endpoint-displacement-over-path in two algebraic forms (one axis); `KATZ_FD_FIRST_21` is the first-point-distance extent. The range extent is excluded as tautological (it is the response skeleton). A `SURVIVES` result means CR is distinct from displacement-based and first-point-based roughness, not from three independent path-roughness axes.

## 16. Valid diagnostic row count
- valid rows (all Level-1 features + response finite) = 4509

## 17. Fold date ranges and row counts (blocked chronological 5-fold)
| fold | test_start | test_end | test_rows |
|------|------------|----------|-----------|
| 1 | 2005-02-01 | 2008-08-29 | 901 |
| 2 | 2008-09-02 | 2012-03-30 | 902 |
| 3 | 2012-04-02 | 2015-10-30 | 902 |
| 4 | 2015-11-02 | 2019-06-04 | 902 |
| 5 | 2019-06-05 | 2022-12-30 | 902 |

## 18. Blocked cross-validated Level-1 joint R²
- **blocked-CV Level-1 joint R² = 0.736339**
- standardization used training-fold statistics only; OLS with intercept; pooled out-of-fold R².

## 19. Final diagnostic status
**SURVIVES NON-TAUTOLOGICAL PATH-ROUGHNESS DISTINCTNESS TEST** (rule: R² ≥ 0.85 → ABSORBED; R² < 0.75 → SURVIVES; [0.75, 0.85) → BORDERLINE-ABSORBED).

## 20. Descriptive in-sample Level-1 R² (descriptive only)
- in-sample Level-1 R² = 0.737921

## 21. Descriptive pairwise correlations (descriptive only)
| baseline | corr(CI_21, baseline) |
|----------|------------------------|
| `ER_21` | -0.7970 |
| `LOG_TORT_21` | 0.6447 |
| `KATZ_FD_FIRST_21` | 0.7829 |

## 22. Descriptive baseline ablations — blocked-CV Level-1 R² dropping one feature (descriptive only)
| ablation | blocked-CV R² |
|----------|---------------|
| drop_ER_21 | 0.6549 |
| drop_LOG_TORT_21 | 0.7326 |
| drop_KATZ_FD_FIRST_21 | 0.6353 |

## 23. Descriptive outputs did not affect the decision
The decision used ONLY the blocked cross-validated Level-1 joint R² (§18) against the frozen threshold band. In-sample R², pairwise correlations, and ablations are descriptive only.

## 24. Analytical identities did not enter the Level-1 model
The two deterministic response transforms were disclosed (§12) but were not predictors in the Level-1 model (§13/§14).

## 25. No wake/outcome/target computed
No forward realized volatility, future range, future drawdown, recovery, expansion, or any target `y` was computed.

## 26. No gate run
No sandbox gate was run.

## 27. No episode-count audit run
No distinct-episode feasibility/count audit was run.

## 28. No alpha spent
No sealed attempt occurred; the atlas family alpha budget is untouched.

## 29. No sealed data accessed
No data on/after 2023-01-01 was read or used.

## 30 / 31. Next-step constraint
Status is `SURVIVES NON-TAUTOLOGICAL PATH-ROUGHNESS DISTINCTNESS TEST`. This only permits considering an episode-count audit by SEPARATE authorization; it does NOT authorize a gate, does not prove predictive value, and spends no alpha. CR may be considered specifically range-based path roughness distinct from displacement/first-point relatives.

## Stated prior (recorded before interpretation)
Expected outcome before running: absorption or borderline absorption by the non-tautological path-roughness family. This is a prior, not a verdict. (Reason: Diagnostic 1 joint R² 0.659541; ER-alone R² 0.6311; incremental difference ≈ 0.0284.) CR has surprised once, so the prior does not decide the result.
