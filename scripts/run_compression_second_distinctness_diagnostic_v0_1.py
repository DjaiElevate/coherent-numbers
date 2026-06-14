#!/usr/bin/env python3
"""
Compression Lane — SECOND DISTINCTNESS DIAGNOSTIC (feature-side only).

Authorized by docs/compression_second_distinctness_diagnostic_authorization_v0_1.md
(authorization commit 7f1a7d00060469d91c3e24a487a58bf4d4608056).

Tests whether CI_21 = -log(CR_21) is absorbed by NON-TAUTOLOGICAL path-roughness
relatives that use different extent definitions (endpoint-displacement and
first-point-distance). The range-extent path-roughness skeleton is EXCLUDED
because it is an exact deterministic transform of the response (see disclosure).

THIS IS NOT A GATE. NOT AN EPISODE-COUNT AUDIT. NOT A SYNTHETIC-NULL CHECK.
Reject-only: absorption can kill / reclassify the lane; survival only permits
considering a separately-authorized episode-count audit. No wake/outcome/target
is computed; no alpha is spent; no sealed data is read.

================================================================================
STRUCTURAL FIREWALL (read before editing)
================================================================================
The diagnostic constructs ONLY feature-side fields, all from adjusted closes up
to and including the current row t (trailing windows only). It: defines no
forward-window functions; creates no wake/outcome/target columns; computes no
post-t value and merges no future-return table; uses no negative shifts (a
self-scan rejects the negative-shift call pattern, assembled dynamically so this
guard never matches its own text); asserts input columns are exactly
{date, adj_close}; and self-scans its own source so no user-defined function
name and no constructed dataframe column name contains a forbidden token. The
two response-transform identities are computed for DISCLOSURE ONLY and are
asserted to be absent from the Level-1 predictor set.
================================================================================
"""

import hashlib
import json
import re
import subprocess
import sys

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Frozen constants (authorization spec)
# ----------------------------------------------------------------------------
REPO_ROOT_EXPECTED = "/Users/jay/Documents/GitHub/coherent-numbers"
HEAD_EXPECTED = "7f1a7d00060469d91c3e24a487a58bf4d4608056"
AUTH_MEMO = "docs/compression_second_distinctness_diagnostic_authorization_v0_1.md"
AUTH_MEMO_SHA = "4fc606b4c7f6de58c5dbb02ab46f8aa54bd28d44244052d462ba9b412b87c00d"
PRIOR_REPORT = "docs/compression_collinearity_diagnostic_report_v0_1.md"
PRIOR_REPORT_SHA = "b2189ae590a582706b4e60f61082f8525bf02ee3426dcf8b4d8f0d113c1ff9d4"
CR_MEMO = "docs/compression_cr_distinctness_reclassification_memo_v0_1.md"
CR_MEMO_SHA = "a53c75ace9f2f695c25c0e6e3f11db0bec65015c87f0990e5c51cc403457946c"
CSV_PATH = "data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv"
CSV_SHA = "5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901"
REPORT_PATH = "docs/compression_second_distinctness_diagnostic_report_v0_1.md"

DATE_MIN = "2005-01-01"
DATE_MAX = "2022-12-31"
SEALED_BOUNDARY = "2023-01-01"

ALLOWED_INPUT_COLUMNS = {"date", "adj_close"}
W = 21
N_STEPS = 20
LOG_N = np.log(N_STEPS)
N_FOLDS = 5
ABSORBED_HI = 0.85
SURVIVE_LO = 0.75

ALLOWED_FEATURE_COLUMNS = {
    "date", "adj_close", "logret_unused_placeholder",
    "absdiff", "range_21", "path_21", "CR_21", "CI_21",
    "net_disp_21", "ER_21", "LOG_TORT_21", "d_first_21", "KATZ_FD_FIRST_21",
    # disclosure-only response transforms (NOT Level-1 predictors):
    "RANGE_PATH_ROUGHNESS_21", "KATZ_FD_RANGE_21",
}

FORBIDDEN_TOKENS = [
    "forward", "future", "wake", "outcome", "target", "drawdown",
    "recovery", "expansion", "lookahead", "_fwd", "fwd_", "lead_", "_ahead",
]

FEATURES = ["ER_21", "LOG_TORT_21", "KATZ_FD_FIRST_21"]   # Level-1 only
RESPONSE = "CI_21"
EXCLUDED_TRANSFORMS = ["RANGE_PATH_ROUGHNESS_21", "KATZ_FD_RANGE_21"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def halt(msg):
    print("DIAGNOSTIC INVALID / HALTED: " + msg, file=sys.stderr)
    sys.exit(2)


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
    if sha256_file(PRIOR_REPORT) != PRIOR_REPORT_SHA:
        halt("prior diagnostic report SHA mismatch")
    if sha256_file(CR_MEMO) != CR_MEMO_SHA:
        halt("CR distinctness memo SHA mismatch")
    if sha256_file(CSV_PATH) != CSV_SHA:
        halt("sandbox CSV SHA mismatch")
    return {"repo_root": root, "branch": branch, "head": head, "origin_main": origin,
            "auth_memo_sha256": AUTH_MEMO_SHA, "prior_report_sha256": PRIOR_REPORT_SHA,
            "cr_memo_sha256": CR_MEMO_SHA, "csv_sha256": CSV_SHA}


def self_scan():
    with open(__file__, "r") as f:
        src = f.read()
    offenders = []
    for name in re.findall(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)", src, flags=re.MULTILINE):
        for tok in FORBIDDEN_TOKENS:
            if tok in name.lower():
                offenders.append(("func", name, tok))
    neg_shift = ".shift(" + chr(45)            # assembled so this guard never self-matches
    if neg_shift in src:
        offenders.append(("pattern", "negative-shift", "negative-shift"))
    # Level-1 predictor set must exclude the deterministic response transforms
    for t in EXCLUDED_TRANSFORMS:
        if t in FEATURES:
            offenders.append(("spec", t, "response-transform-in-level1"))
    return offenders


# ----------------------------------------------------------------------------
# Trailing-only window helpers
# ----------------------------------------------------------------------------
def _d_first(window):
    # max |x_i - x_0| over the trailing window (x_0 = first close in window)
    if np.any(~np.isfinite(window)):
        return np.nan
    return float(np.max(np.abs(window - window[0])))


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
    df["absdiff"] = close.diff().abs()

    df["range_21"] = close.rolling(W).max() - close.rolling(W).min()
    df["path_21"] = df["absdiff"].rolling(W - 1).sum()
    cr = (df["range_21"] / df["path_21"]).where((df["path_21"] > 0) & (df["range_21"] > 0))
    df["CR_21"] = cr
    df["CI_21"] = -np.log(df["CR_21"])

    # endpoint displacement = |close_t - close_start|, start = first close of window
    df["net_disp_21"] = (close - close.shift(W - 1)).abs()
    nd = df["net_disp_21"].where(df["net_disp_21"] > 0)

    # A. ER_21 (displacement / path)
    df["ER_21"] = (df["net_disp_21"] / df["path_21"]).where(df["path_21"] > 0)
    # B. LOG_TORT_21 = log(path / displacement) = -log(ER) where defined
    df["LOG_TORT_21"] = np.log(df["path_21"] / nd).where(df["path_21"] > 0)
    # C. KATZ_FD_FIRST_21 (first-point distance extent)
    df["d_first_21"] = close.rolling(W).apply(_d_first, raw=True)
    ratio = (df["d_first_21"] / df["path_21"]).where(
        (df["path_21"] > 0) & (df["d_first_21"] > 0))
    denom = LOG_N + np.log(ratio)
    df["KATZ_FD_FIRST_21"] = (LOG_N / denom).where(np.isfinite(denom) & (denom != 0))

    # disclosure-only deterministic response transforms (NOT Level-1 predictors)
    df["RANGE_PATH_ROUGHNESS_21"] = (df["path_21"] / df["range_21"]).where(
        (df["path_21"] > 0) & (df["range_21"] > 0))
    katz_range_denom = LOG_N - df["CI_21"]
    df["KATZ_FD_RANGE_21"] = (LOG_N / katz_range_denom).where(
        np.isfinite(katz_range_denom) & (katz_range_denom != 0))

    extra = set(df.columns) - ALLOWED_FEATURE_COLUMNS
    if extra:
        halt("non-allowed feature columns constructed: %r" % extra)
    return df


# ----------------------------------------------------------------------------
# Modeling
# ----------------------------------------------------------------------------
def _ols_fit_predict(Xtr, ytr, Xte):
    mu = Xtr.mean(axis=0); sd = Xtr.std(axis=0); sd[sd == 0] = 1.0
    Xtr_s = (Xtr - mu) / sd; Xte_s = (Xte - mu) / sd
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
    oof_true, oof_pred, info = [], [], []
    for (a, b) in folds:
        te = np.zeros(n, bool); te[a:b] = True; tr = ~te
        pred = _ols_fit_predict(X[tr], y[tr], X[te])
        oof_true.append(y[te]); oof_pred.append(pred)
        info.append({"test_start_date": data.iloc[a]["date"],
                     "test_end_date": data.iloc[b - 1]["date"], "test_rows": int(b - a)})
    yt = np.concatenate(oof_true); yp = np.concatenate(oof_pred)
    ss_res = float(np.sum((yt - yp) ** 2)); ss_tot = float(np.sum((yt - np.mean(yt)) ** 2))
    return (1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")), info


def insample_r2(data, feature_cols):
    X = data[feature_cols].to_numpy(float); y = data[RESPONSE].to_numpy(float)
    mu = X.mean(axis=0); sd = X.std(axis=0); sd[sd == 0] = 1.0
    A = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    beta, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    pred = A @ beta
    ss_res = float(np.sum((y - pred) ** 2)); ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def classify(r2):
    if r2 >= ABSORBED_HI:
        return "ABSORBED BY NON-TAUTOLOGICAL PATH-ROUGHNESS FAMILY"
    if r2 < SURVIVE_LO:
        return "SURVIVES NON-TAUTOLOGICAL PATH-ROUGHNESS DISTINCTNESS TEST"
    return "BORDERLINE-ABSORBED BY NON-TAUTOLOGICAL PATH-ROUGHNESS FAMILY"


def main():
    guards = run_guards()
    offenders = self_scan()
    if offenders:
        halt("firewall/spec self-scan failed: %r" % offenders)

    df = build_features()
    input_rows = int(len(df))
    date_min, date_max = df["date"].min(), df["date"].max()

    valid = df.dropna(subset=FEATURES + [RESPONSE]).reset_index(drop=True)
    valid_rows = int(len(valid))
    if valid_rows < N_FOLDS:
        halt("insufficient valid diagnostic rows: %d" % valid_rows)

    cv_r2, folds = blocked_cv_r2(valid, FEATURES)
    status = classify(cv_r2)

    # descriptive only
    is_r2 = insample_r2(valid, FEATURES)
    pairwise = {f: float(np.corrcoef(valid[RESPONSE], valid[f])[0, 1]) for f in FEATURES}
    ablations = {}
    for f in FEATURES:
        reduced = [c for c in FEATURES if c != f]
        ab, _ = blocked_cv_r2(valid, reduced)
        ablations["drop_" + f] = ab

    # analytical identity verification (disclosure only)
    vd = df.dropna(subset=["CI_21", "RANGE_PATH_ROUGHNESS_21"])
    id_rpr = float(np.max(np.abs(vd["RANGE_PATH_ROUGHNESS_21"] - np.exp(vd["CI_21"]))))
    vk = df.dropna(subset=["CI_21", "KATZ_FD_RANGE_21"])
    id_katz = float(np.max(np.abs(vk["KATZ_FD_RANGE_21"] - (LOG_N / (LOG_N - vk["CI_21"])))))

    summary = {
        "guards": guards, "input_rows": input_rows, "date_min": date_min,
        "date_max": date_max, "valid_rows": valid_rows,
        "self_scan_offenders": offenders, "level1_features": FEATURES,
        "excluded_transforms": EXCLUDED_TRANSFORMS,
        "cv_level1_r2": cv_r2, "status": status, "folds": folds,
        "descriptive": {"insample_level1_r2": is_r2, "pairwise_corr_CI21": pairwise,
                        "ablation_cv_r2_drop_one": ablations,
                        "identity_max_abs_dev_RANGE_PATH_ROUGHNESS_vs_expCI": id_rpr,
                        "identity_max_abs_dev_KATZ_FD_RANGE_vs_formula": id_katz},
    }
    print("===DIAG2_JSON_BEGIN===")
    print(json.dumps(summary, indent=2))
    print("===DIAG2_JSON_END===")
    write_report(summary)


def write_report(s):
    g = s["guards"]; d = s["descriptive"]
    fold_lines = "\n".join("| %d | %s | %s | %d |" % (
        i + 1, f["test_start_date"], f["test_end_date"], f["test_rows"])
        for i, f in enumerate(s["folds"]))
    pair_lines = "\n".join("| `%s` | %.4f |" % (k, v) for k, v in d["pairwise_corr_CI21"].items())
    abl_lines = "\n".join("| %s | %.4f |" % (k, v) for k, v in d["ablation_cv_r2_drop_one"].items())
    status = s["status"]
    if status.startswith("SURVIVES"):
        nxt = ("Status is `SURVIVES NON-TAUTOLOGICAL PATH-ROUGHNESS DISTINCTNESS TEST`. This only "
               "permits considering an episode-count audit by SEPARATE authorization; it does NOT "
               "authorize a gate, does not prove predictive value, and spends no alpha. CR may be "
               "considered specifically range-based path roughness distinct from displacement/first-point relatives.")
    else:
        nxt = ("Status is `%s`. This supports the future closure decision status candidate "
               "`RECLASSIFIED — known construct`, but does NOT itself change atlas status. No alpha "
               "spent; not a hypothesis null; not a gate fail." % status)
    report = """# Compression Lane — Second Distinctness Diagnostic Report v0.1

**Status: %(status)s** — second feature-side distinctness diagnostic (non-tautological path-roughness family; reject-only). NOT a gate, NOT an episode-count audit, NOT a synthetic-null check. No wake/outcome/target was computed. No alpha was spent. No sealed data was accessed.

Authorized by `docs/compression_second_distinctness_diagnostic_authorization_v0_1.md` (commit `7f1a7d00060469d91c3e24a487a58bf4d4608056`).

## 1. Title and status
Compression second distinctness diagnostic v0.1. Final status: **%(status)s**.

## 2. Commit / HEAD / origin verification
- repo root: `%(repo_root)s`
- branch: `%(branch)s`
- HEAD: `%(head)s`
- origin/main: `%(origin_main)s`

## 3. Authorization memo SHA verification
- `%(auth_memo)s` = `%(auth_sha)s` (matches frozen spec)

## 4. Prior diagnostic report SHA verification
- `%(prior_report)s` = `%(prior_sha)s` (matches)

## 5. CR distinctness memo SHA verification
- `%(cr_memo)s` = `%(cr_sha)s` (matches)

## 6. Sandbox CSV SHA verification
- `%(csv_path)s` = `%(csv_sha)s` (verified before reading rows)

## 7. Loaded date range and row count
- loaded `%(date_min)s` .. `%(date_max)s`; input rows = %(input_rows)d

## 8. Allowed columns only
- input columns asserted to be exactly {`date`, `adj_close`}.

## 9. No rows >= 2023-01-01
- confirmed: zero rows on/after the sealed boundary `2023-01-01`.

## 10. Structural firewall proof
The firewall is structural: the diagnostic constructs only feature-side fields, defines no forward-window functions, creates no wake/outcome/target columns, and makes wake/outcome construction unreachable from the diagnostic data structures.
- no forward-window functions defined;
- no wake/outcome/target columns created (constructed columns checked against an allow-list);
- no future-indexing: source rejected if it contains a negative (future) shift call;
- self-scan result: %(selfscan)s;
- feature-side data structures only (all features use trailing windows ending at t).

## 11. Feature definitions
- **CR_21** = (trailing 21-close range) / (trailing 21-close absolute path length); **CI_21 = -log(CR_21)** (response).
- **ER_21** = |close_t − close_start| / path_21 (endpoint-displacement extent).
- **LOG_TORT_21** = log(path_21 / |close_t − close_start|) = −log(ER_21) where defined (same endpoint-displacement axis, log form).
- **KATZ_FD_FIRST_21** = log(20) / (log(20) + log(d_first / path_21)), d_first = max|close_i − close_start| over the window (first-point-distance extent).

## 12. Analytical identity disclosure (deterministic response transforms)
- `RANGE_PATH_ROUGHNESS_21 = path_21 / range_21 = exp(CI_21)` — numerically verified: max abs deviation from exp(CI_21) = %(id_rpr).3e
- `KATZ_FD_RANGE_21 = log(20) / (log(20) - CI_21)` — numerically verified: max abs deviation from the formula = %(id_katz).3e

> A deterministic transform of the response is not a predictive discovery. It is an identification result.

## 13. Both response transforms excluded from Level-1
`RANGE_PATH_ROUGHNESS_21` and `KATZ_FD_RANGE_21` are deterministic response transforms and are **excluded** from the Level-1 decision model. A self-scan asserts neither appears in the Level-1 predictor set.

## 14. Level-1 formula
`CI_21 ~ ER_21 + LOG_TORT_21 + KATZ_FD_FIRST_21`

## 15. Extent-span interpretation
The Level-1 set spans two independent extent concepts, not three. `ER_21` and `LOG_TORT_21` are endpoint-displacement-over-path in two algebraic forms (one axis); `KATZ_FD_FIRST_21` is the first-point-distance extent. The range extent is excluded as tautological (it is the response skeleton). A `SURVIVES` result means CR is distinct from displacement-based and first-point-based roughness, not from three independent path-roughness axes.

## 16. Valid diagnostic row count
- valid rows (all Level-1 features + response finite) = %(valid_rows)d

## 17. Fold date ranges and row counts (blocked chronological 5-fold)
| fold | test_start | test_end | test_rows |
|------|------------|----------|-----------|
%(fold_lines)s

## 18. Blocked cross-validated Level-1 joint R²
- **blocked-CV Level-1 joint R² = %(cv_r2).6f**
- standardization used training-fold statistics only; OLS with intercept; pooled out-of-fold R².

## 19. Final diagnostic status
**%(status)s** (rule: R² ≥ 0.85 → ABSORBED; R² < 0.75 → SURVIVES; [0.75, 0.85) → BORDERLINE-ABSORBED).

## 20. Descriptive in-sample Level-1 R² (descriptive only)
- in-sample Level-1 R² = %(is_r2).6f

## 21. Descriptive pairwise correlations (descriptive only)
| baseline | corr(CI_21, baseline) |
|----------|------------------------|
%(pair_lines)s

## 22. Descriptive baseline ablations — blocked-CV Level-1 R² dropping one feature (descriptive only)
| ablation | blocked-CV R² |
|----------|---------------|
%(abl_lines)s

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
%(nxt)s

## Stated prior (recorded before interpretation)
Expected outcome before running: absorption or borderline absorption by the non-tautological path-roughness family. This is a prior, not a verdict. (Reason: Diagnostic 1 joint R² 0.659541; ER-alone R² 0.6311; incremental difference ≈ 0.0284.) CR has surprised once, so the prior does not decide the result.
""" % {
        "status": status, "repo_root": g["repo_root"], "branch": g["branch"],
        "head": g["head"], "origin_main": g["origin_main"],
        "auth_memo": AUTH_MEMO, "auth_sha": g["auth_memo_sha256"],
        "prior_report": PRIOR_REPORT, "prior_sha": g["prior_report_sha256"],
        "cr_memo": CR_MEMO, "cr_sha": g["cr_memo_sha256"],
        "csv_path": CSV_PATH, "csv_sha": g["csv_sha256"],
        "date_min": s["date_min"], "date_max": s["date_max"], "input_rows": s["input_rows"],
        "selfscan": "PASS (no offenders)" if not s["self_scan_offenders"] else repr(s["self_scan_offenders"]),
        "id_rpr": d["identity_max_abs_dev_RANGE_PATH_ROUGHNESS_vs_expCI"],
        "id_katz": d["identity_max_abs_dev_KATZ_FD_RANGE_vs_formula"],
        "valid_rows": s["valid_rows"], "fold_lines": fold_lines, "cv_r2": s["cv_level1_r2"],
        "is_r2": d["insample_level1_r2"], "pair_lines": pair_lines, "abl_lines": abl_lines,
        "nxt": nxt,
    }
    with open(REPORT_PATH, "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()
