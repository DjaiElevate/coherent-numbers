#!/usr/bin/env python3
"""
Compression Lane — PRE-GATE COLLINEARITY DIAGNOSTIC (feature-side only).

Authorized by docs/compression_collinearity_diagnostic_authorization_v0_1.md
(authorization commit 8793efc28bd97f8b5ff4098850c615c5d5ac2ae7).

THIS IS NOT A GATE. NOT AN EPISODE-COUNT AUDIT. NOT A SYNTHETIC-NULL CHECK.
It is a one-way reject-only feature-space absorption check: does the Compression
metric CI_21 = -log(CR_21) lie inside the subspace spanned by a frozen set of
boring baselines? Absorption can KILL the lane. Survival only PERMITS the next
separately-authorized step (distinct-episode feasibility/count audit). Survival
proves no predictive value, authorizes no gate, spends no alpha.

================================================================================
STRUCTURAL FIREWALL (read before editing)
================================================================================
The diagnostic constructs ONLY feature-side fields, all computed from adjusted
closes up to and including the current row t (trailing windows only). It:
  * defines NO forward-window functions;
  * creates NO wake/outcome/target columns;
  * computes NO post-t value and merges NO future-return table;
  * uses NO negative shifts (a runtime self-scan rejects negative-shift usage);
  * asserts input columns are exactly {date, adj_close};
  * self-scans its own source so that no user-defined function name and no
    constructed dataframe column name contains a forbidden forward/wake token.
Wake/outcome construction is therefore unreachable from the diagnostic data
structures: there are no forward arrays, no forward-window functions, and no
forward indices to read.
================================================================================
"""

import hashlib
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Frozen constants (authorization spec)
# ----------------------------------------------------------------------------
REPO_ROOT_EXPECTED = "/Users/jay/Documents/GitHub/coherent-numbers"
HEAD_EXPECTED = "8793efc28bd97f8b5ff4098850c615c5d5ac2ae7"
AUTH_MEMO = "docs/compression_collinearity_diagnostic_authorization_v0_1.md"
AUTH_MEMO_SHA = "d4fc494d5b435798f0906d528333f793da7e34a53f930926ce8509885aca5628"
STAGE1_MEMO = "docs/compression_stage1_design_memo_v0_1.md"
STAGE1_MEMO_SHA = "66c54688374c439594546b715d65211340b8680cbe055fca6736c208cea7d420"
CSV_PATH = "data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv"
CSV_SHA = "5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901"
REPORT_PATH = "docs/compression_collinearity_diagnostic_report_v0_1.md"

DATE_MIN = "2005-01-01"
DATE_MAX = "2022-12-31"
SEALED_BOUNDARY = "2023-01-01"

ALLOWED_INPUT_COLUMNS = {"date", "adj_close"}

CR_WINDOW = 21          # primary Compression window
CR10_WINDOW = 10        # descriptive-only
RV_WINDOW = 21
PCTILE_WINDOW = 252
AC1_SHORT = 21
AC1_LONG = 63
VR_K = 5
VR_N = 252
N_FOLDS = 5

ABSORBED_HI = 0.85      # R^2 >= 0.85 -> ABSORBED
SURVIVE_LO = 0.75       # R^2 < 0.75 -> SURVIVES; [0.75,0.85) -> BORDERLINE-ABSORBED

# Feature-side columns the diagnostic is permitted to construct.
ALLOWED_FEATURE_COLUMNS = {
    "date", "adj_close", "logret", "absdiff",
    "range_21", "path_21", "CR_21", "CI_21",
    "range_10", "path_10", "CR_10", "CI_10",
    "RV_21", "log_RV_21", "RV_21_pctile_252",
    "AC1_21", "AC1_63", "VR5_252",
    "net_disp_21", "ER_21",
}

# Forbidden tokens for function names and constructed column names.
FORBIDDEN_TOKENS = [
    "forward", "future", "wake", "outcome", "target", "drawdown",
    "recovery", "expansion", "lookahead", "_fwd", "fwd_", "lead_", "_ahead",
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def halt(msg):
    print("DIAGNOSTIC INVALID / HALTED: " + msg, file=sys.stderr)
    sys.exit(2)


# ----------------------------------------------------------------------------
# Guards
# ----------------------------------------------------------------------------
def run_guards():
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip()
    if root != REPO_ROOT_EXPECTED:
        halt("repo root mismatch: %r" % root)
    branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
    if branch != "main":
        halt("branch not main: %r" % branch)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    if head != HEAD_EXPECTED:
        halt("HEAD mismatch: %r" % head)
    origin = subprocess.check_output(["git", "rev-parse", "origin/main"]).decode().strip()
    if origin != HEAD_EXPECTED:
        halt("origin/main mismatch: %r" % origin)
    if sha256_file(AUTH_MEMO) != AUTH_MEMO_SHA:
        halt("authorization memo SHA mismatch")
    if sha256_file(STAGE1_MEMO) != STAGE1_MEMO_SHA:
        halt("Stage-1 memo SHA mismatch")
    if sha256_file(CSV_PATH) != CSV_SHA:
        halt("sandbox CSV SHA mismatch")
    return {"repo_root": root, "branch": branch, "head": head, "origin_main": origin,
            "auth_memo_sha256": AUTH_MEMO_SHA, "stage1_memo_sha256": STAGE1_MEMO_SHA,
            "csv_sha256": CSV_SHA}


def self_scan():
    """Prove no forbidden forward/wake function name exists and no negative shift."""
    with open(__file__, "r") as f:
        src = f.read()
    offenders = []
    for name in re.findall(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)", src, flags=re.MULTILINE):
        for tok in FORBIDDEN_TOKENS:
            if tok in name.lower():
                offenders.append(("func", name, tok))
    # reject negative shifts (future indexing). The search pattern is assembled
    # from pieces so this guard line never matches itself (false positive).
    neg_shift = ".shift(" + chr(45)
    if neg_shift in src:
        offenders.append(("pattern", "negative-shift", "negative-shift"))
    # forbidden tokens may not appear in the allowed-feature-column set
    for col in ALLOWED_FEATURE_COLUMNS:
        for tok in FORBIDDEN_TOKENS:
            if tok in col.lower():
                offenders.append(("col", col, tok))
    return offenders


# ----------------------------------------------------------------------------
# Trailing-only rolling helpers (window arrays end at current row t)
# ----------------------------------------------------------------------------
def _ac1(window):
    if np.any(~np.isfinite(window)) or len(window) < 3:
        return np.nan
    a = window[:-1]
    b = window[1:]
    if np.std(a) == 0 or np.std(b) == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def _pctile_last(window):
    if np.any(~np.isfinite(window)):
        return np.nan
    return float(np.mean(window <= window[-1]))


def _lomackinlay_vr(window):
    """Lo & MacKinlay (1988) overlapping bias-corrected variance ratio, k vs 1.

    window = N one-period (daily) log returns ending at t.
      mu      = mean(returns)
      var_a   = (1/(N-1)) * sum((r - mu)^2)                      # 1-period var
      ksum_j  = sum of k consecutive returns ending at j         # overlapping
      var_c   = (1/m) * sum((ksum - k*mu)^2),  j = k..N          # k-period var
      m       = k*(N-k+1)*(1 - k/N)                              # overlap bias corr.
      VR(k)   = var_c / var_a                                    # -> 1 under RW
    """
    if np.any(~np.isfinite(window)):
        return np.nan
    N = len(window)
    k = VR_K
    if N != VR_N:
        return np.nan
    mu = np.mean(window)
    var_a = np.sum((window - mu) ** 2) / (N - 1)
    if var_a <= 0:
        return np.nan
    csum = np.cumsum(window)
    # overlapping k-sums ending at indices k-1 .. N-1 (0-indexed) -> N-k+1 sums
    ksums = csum[k - 1:].copy()
    ksums[1:] = ksums[1:] - csum[:N - k]
    m = k * (N - k + 1) * (1.0 - float(k) / N)
    var_c = np.sum((ksums - k * mu) ** 2) / m
    return float(var_c / var_a)


def build_features():
    df = pd.read_csv(CSV_PATH)
    if set(df.columns) != ALLOWED_INPUT_COLUMNS:
        halt("unexpected input columns: %r" % list(df.columns))
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df = df.sort_values("date").reset_index(drop=True)
    if (df["date"] < DATE_MIN).any() or (df["date"] > DATE_MAX).any():
        halt("date outside allowed sandbox range")
    if (df["date"] >= SEALED_BOUNDARY).any():
        halt("sealed-period (2023+) row present")

    close = df["adj_close"].astype(float)
    df["logret"] = np.log(close / close.shift(1))           # uses t and t-1 only
    df["absdiff"] = close.diff().abs()

    # CR_21 (primary): trailing 21-close range / 21-close path
    df["range_21"] = close.rolling(CR_WINDOW).max() - close.rolling(CR_WINDOW).min()
    df["path_21"] = df["absdiff"].rolling(CR_WINDOW - 1).sum()
    cr21 = df["range_21"] / df["path_21"]
    cr21 = cr21.where(df["path_21"] > 0)
    df["CR_21"] = cr21
    df["CI_21"] = -np.log(df["CR_21"])

    # CR_10 (descriptive only)
    df["range_10"] = close.rolling(CR10_WINDOW).max() - close.rolling(CR10_WINDOW).min()
    df["path_10"] = df["absdiff"].rolling(CR10_WINDOW - 1).sum()
    cr10 = (df["range_10"] / df["path_10"]).where(df["path_10"] > 0)
    df["CR_10"] = cr10
    df["CI_10"] = -np.log(df["CR_10"])

    # A. log realized volatility (RMS of trailing 21 daily log returns), then log
    rv21 = np.sqrt((df["logret"] ** 2).rolling(RV_WINDOW).mean())
    df["RV_21"] = rv21.where(rv21 > 0)
    df["log_RV_21"] = np.log(df["RV_21"])

    # B. trailing percentile of RV_21 over 252-day history ending at t
    df["RV_21_pctile_252"] = df["RV_21"].rolling(PCTILE_WINDOW).apply(_pctile_last, raw=True)

    # C. lag-1 autocorrelation of daily log returns (trailing 21 / 63)
    df["AC1_21"] = df["logret"].rolling(AC1_SHORT).apply(_ac1, raw=True)
    df["AC1_63"] = df["logret"].rolling(AC1_LONG).apply(_ac1, raw=True)

    # D. Lo-MacKinlay (1988) overlap-bias-corrected variance ratio, k=5, n=252
    df["VR5_252"] = df["logret"].rolling(VR_N).apply(_lomackinlay_vr, raw=True)

    # E. efficiency ratio ER_21: |net 21-close displacement| / 21-close path
    df["net_disp_21"] = (close - close.shift(CR_WINDOW - 1)).abs()
    df["ER_21"] = (df["net_disp_21"] / df["path_21"]).where(df["path_21"] > 0)

    extra = set(df.columns) - ALLOWED_FEATURE_COLUMNS
    if extra:
        halt("non-allowed feature columns constructed: %r" % extra)
    return df


# ----------------------------------------------------------------------------
# Modeling (blocked chronological CV; train-fold standardization; OLS)
# ----------------------------------------------------------------------------
FEATURES = ["log_RV_21", "RV_21_pctile_252", "AC1_21", "AC1_63", "VR5_252", "ER_21"]
RESPONSE = "CI_21"


def _ols_fit_predict(Xtr, ytr, Xte):
    mu = Xtr.mean(axis=0)
    sd = Xtr.std(axis=0)
    sd[sd == 0] = 1.0
    Xtr_s = (Xtr - mu) / sd
    Xte_s = (Xte - mu) / sd
    Atr = np.column_stack([np.ones(len(Xtr_s)), Xtr_s])
    Ate = np.column_stack([np.ones(len(Xte_s)), Xte_s])
    beta, _, _, _ = np.linalg.lstsq(Atr, ytr, rcond=None)
    return Ate @ beta


def blocked_cv_r2(data, feature_cols):
    n = len(data)
    if n < N_FOLDS:
        halt("insufficient feature rows for %d folds: n=%d" % (N_FOLDS, n))
    bounds = np.linspace(0, n, N_FOLDS + 1).astype(int)
    folds = [(bounds[i], bounds[i + 1]) for i in range(N_FOLDS)]
    if any(b - a < 1 for a, b in folds):
        halt("fewer than %d feasible folds" % N_FOLDS)
    X = data[feature_cols].to_numpy(float)
    y = data[RESPONSE].to_numpy(float)
    oof_true, oof_pred = [], []
    fold_info = []
    for (a, b) in folds:
        te = np.zeros(n, dtype=bool)
        te[a:b] = True
        tr = ~te
        pred = _ols_fit_predict(X[tr], y[tr], X[te])
        oof_true.append(y[te])
        oof_pred.append(pred)
        fold_info.append({"test_start_date": data.iloc[a]["date"],
                          "test_end_date": data.iloc[b - 1]["date"],
                          "test_rows": int(b - a)})
    yt = np.concatenate(oof_true)
    yp = np.concatenate(oof_pred)
    ss_res = float(np.sum((yt - yp) ** 2))
    ss_tot = float(np.sum((yt - np.mean(yt)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return r2, fold_info


def insample_r2(data, feature_cols):
    X = data[feature_cols].to_numpy(float)
    y = data[RESPONSE].to_numpy(float)
    mu = X.mean(axis=0); sd = X.std(axis=0); sd[sd == 0] = 1.0
    Xs = (X - mu) / sd
    A = np.column_stack([np.ones(len(Xs)), Xs])
    beta, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    pred = A @ beta
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def classify(r2):
    if r2 >= ABSORBED_HI:
        return "ABSORBED"
    if r2 < SURVIVE_LO:
        return "SURVIVES FEATURE-SPACE ABSORPTION"
    return "BORDERLINE-ABSORBED"


def main():
    guards = run_guards()
    offenders = self_scan()
    if offenders:
        halt("firewall self-scan failed: %r" % offenders)

    df = build_features()
    input_rows = int(len(df))
    date_min, date_max = df["date"].min(), df["date"].max()

    valid = df.dropna(subset=FEATURES + [RESPONSE]).reset_index(drop=True)
    valid_rows = int(len(valid))
    if valid_rows < N_FOLDS:
        halt("insufficient valid diagnostic rows: %d" % valid_rows)

    cv_r2, fold_info = blocked_cv_r2(valid, FEATURES)
    status = classify(cv_r2)

    # ---- descriptive only (do NOT affect decision) ----
    is_r2 = insample_r2(valid, FEATURES)
    pairwise = {f: float(np.corrcoef(valid[RESPONSE], valid[f])[0, 1]) for f in FEATURES}
    ablations = {}
    for f in FEATURES:
        reduced = [c for c in FEATURES if c != f]
        ab_r2, _ = blocked_cv_r2(valid, reduced)
        ablations["drop_" + f] = ab_r2
    er_alone_r2, _ = blocked_cv_r2(valid, ["ER_21"])
    er_residual_share = 1.0 - er_alone_r2

    summary = {
        "guards": guards,
        "input_rows": input_rows, "date_min": date_min, "date_max": date_max,
        "valid_rows": valid_rows,
        "self_scan_offenders": offenders,
        "cv_joint_r2": cv_r2, "status": status,
        "folds": fold_info,
        "descriptive": {
            "insample_joint_r2": is_r2,
            "pairwise_corr_CI21": pairwise,
            "ablation_cv_r2_drop_one": ablations,
            "er_alone_cv_r2": er_alone_r2,
            "er_residual_share": er_residual_share,
        },
    }
    print("===DIAG_JSON_BEGIN===")
    print(json.dumps(summary, indent=2))
    print("===DIAG_JSON_END===")

    write_report(summary)


def write_report(s):
    g = s["guards"]
    d = s["descriptive"]
    fold_lines = "\n".join(
        "| %d | %s | %s | %d |" % (i + 1, f["test_start_date"], f["test_end_date"], f["test_rows"])
        for i, f in enumerate(s["folds"]))
    pair_lines = "\n".join("| `%s` | %.4f |" % (k, v) for k, v in d["pairwise_corr_CI21"].items())
    abl_lines = "\n".join("| %s | %.4f |" % (k, v) for k, v in d["ablation_cv_r2_drop_one"].items())
    status = s["status"]
    if status == "SURVIVES FEATURE-SPACE ABSORPTION":
        next_step = ("Status is `SURVIVES FEATURE-SPACE ABSORPTION`. This permits ONLY the next "
                     "separately-authorized artifact: the distinct-episode feasibility/count audit. "
                     "It does NOT authorize a gate, does NOT prove predictive information, and spends no alpha.")
    else:
        next_step = ("Status is `%s`. The lane STOPS before the episode-count audit unless a future "
                     "owner creates a separate decision memo. No alpha spent; not a hypothesis null; "
                     "not a gate fail." % status)
    report = """# Compression Lane — Collinearity Diagnostic Report v0.1

**Status: %(status)s** — pre-gate feature-space absorption diagnostic (reject-only). NOT a gate, NOT an episode-count audit, NOT a synthetic-null check. No wake/outcome/target was computed. No alpha was spent. No sealed data was accessed.

Authorized by `docs/compression_collinearity_diagnostic_authorization_v0_1.md` (commit `8793efc28bd97f8b5ff4098850c615c5d5ac2ae7`).

## 1. Title and status
Compression pre-gate collinearity diagnostic v0.1. Final status: **%(status)s**.

## 2. Commit / HEAD / origin verification
- repo root: `%(repo_root)s`
- branch: `%(branch)s`
- HEAD: `%(head)s`
- origin/main: `%(origin_main)s`

## 3. Authorization memo SHA verification
- `docs/compression_collinearity_diagnostic_authorization_v0_1.md` = `%(auth_sha)s` (matches frozen spec)

## 4. Compression Stage-1 memo SHA verification
- `docs/compression_stage1_design_memo_v0_1.md` = `%(stage1_sha)s` (matches)

## 5. Sandbox CSV SHA verification
- `%(csv_path)s` = `%(csv_sha)s` (verified before reading rows)

## 6. Loaded date range and row count
- loaded `%(date_min)s` .. `%(date_max)s`; input rows = %(input_rows)d

## 7. Allowed columns only
- input columns asserted to be exactly {`date`, `adj_close`}.

## 8. No rows >= 2023-01-01
- confirmed: zero rows on/after the sealed boundary `2023-01-01`.

## 9. Structural firewall proof
The firewall is structural: the diagnostic constructs only feature-side fields, defines no forward-window functions, creates no wake/outcome/target columns, and makes wake/outcome construction unreachable from the diagnostic data structures.
- no forward-window functions defined;
- no wake/outcome/target columns created (constructed columns checked against an allow-list);
- no future-indexing: source rejected if it contains a negative (future) shift call;
- self-scan result: %(selfscan)s;
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
- valid rows (all primary features + response finite) = %(valid_rows)d

## 13. Fold date ranges and row counts (blocked chronological 5-fold)
| fold | test_start | test_end | test_rows |
|------|------------|----------|-----------|
%(fold_lines)s

## 14. Blocked cross-validated joint-baseline R²
- **blocked-CV joint-baseline R² = %(cv_r2).6f**
- model: `CI_21 ~ log_RV_21 + RV_21_pctile_252 + AC1_21 + AC1_63 + VR5_252 + ER_21`
- standardization used training-fold statistics only; OLS with intercept; pooled out-of-fold R².

## 15. Final diagnostic status
**%(status)s** (decision rule: R² ≥ 0.85 → ABSORBED; R² < 0.75 → SURVIVES; [0.75, 0.85) → BORDERLINE-ABSORBED).

## 16. Descriptive in-sample joint R² (descriptive only)
- in-sample joint R² = %(is_r2).6f

## 17. Descriptive pairwise correlations (descriptive only)
| baseline | corr(CI_21, baseline) |
|----------|------------------------|
%(pair_lines)s

## 18. Descriptive baseline ablations — blocked-CV joint R² dropping one baseline (descriptive only)
| ablation | blocked-CV joint R² |
|----------|---------------------|
%(abl_lines)s

## 19. Descriptive ER-alone absorption (descriptive only)
- `CI_21 ~ ER_21` blocked-CV R² = %(er_r2).6f
- residual share over ER alone (1 − ER-alone R²) = %(er_resid).6f

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
%(next_step)s
""" % {
        "status": status,
        "repo_root": g["repo_root"], "branch": g["branch"], "head": g["head"],
        "origin_main": g["origin_main"], "auth_sha": g["auth_memo_sha256"],
        "stage1_sha": g["stage1_memo_sha256"], "csv_path": CSV_PATH, "csv_sha": g["csv_sha256"],
        "date_min": s["date_min"], "date_max": s["date_max"], "input_rows": s["input_rows"],
        "selfscan": "PASS (no offenders)" if not s["self_scan_offenders"] else repr(s["self_scan_offenders"]),
        "valid_rows": s["valid_rows"], "fold_lines": fold_lines,
        "cv_r2": s["cv_joint_r2"], "is_r2": d["insample_joint_r2"],
        "pair_lines": pair_lines, "abl_lines": abl_lines,
        "er_r2": d["er_alone_cv_r2"], "er_resid": d["er_residual_share"],
        "next_step": next_step,
    }
    with open(REPORT_PATH, "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()
