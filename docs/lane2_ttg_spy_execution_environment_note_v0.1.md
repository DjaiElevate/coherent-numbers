# Lane 2 — TTG → SPY v1 Execution Environment Note — v0.1

> Status: environment-provisioning record only. No study data were read and no execution occurred. The single
> in-sample archive read remains unspent. This note is uncommitted pending explicit instruction.

## Purpose

Provision the missing locked dependency (`scikit-learn`) for the TTG→SPY v1 execution environment, so the locked
pre-registration `docs/lane2_ttg_spy_prereg_v1.1.md` (prereg commit `84068784…`) can be executed in a later,
separately-vetted dispatch. The prior execution dispatch stopped fail-closed solely because `scikit-learn` was
missing. This provisioning does not read or execute the study.

## Python environment

- Python executable: `/Library/Developer/CommandLineTools/usr/bin/python3`
- Python version: `3.8.2` (not upgraded)

## Install command used

```
python3 -m pip install --user "scikit-learn==1.3.2"
```

- pip default upgrade strategy (`only-if-needed`) was used; **numpy / pandas / scipy were NOT upgraded**
  (already satisfied scikit-learn 1.3.2's requirements). Only `scikit-learn`, `joblib`, and `threadpoolctl`
  were added.

## Resolved package versions

| package | version |
|---|---|
| python | 3.8.2 |
| numpy | 1.24.4 |
| pandas | 2.0.3 |
| scipy | 1.10.1 |
| scikit-learn | 1.3.2 |
| joblib | 1.4.2 |
| threadpoolctl | 3.5.0 |

## Synthetic smoke test (value-blind)

Tiny hard-coded synthetic toy arrays only — no repo data, no archive, no SPY CSV, no results/cache:

- imported `sklearn`, `LogisticRegression`, `StandardScaler`, `roc_auc_score`
- fit locked-style `LogisticRegression(penalty="l2", C=1.0, solver="lbfgs", fit_intercept=True,
  class_weight=None, max_iter=10000, tol=1e-8)` on an 8×2 toy array, with `StandardScaler` fit on the same toy array
- computed `roc_auc_score` on toy labels → AUC in [0, 1]
- **Result: PASS** (model fitted; AUC well-defined)

## Boundary declaration

- No TTG archive read; no SPY CSV read; no labels; no returns; no features; no joins; no study statistics; no
  evaluation; no holdout touch; no 2023+ contact; no V2.
- No source-code edits; no tracked files changed by the install.
- The single in-sample archive read remains unspent; the archive remains value-blind.
- Not pushed. This note is uncommitted.
