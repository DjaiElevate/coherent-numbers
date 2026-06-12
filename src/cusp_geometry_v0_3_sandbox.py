"""
Cusp Geometry Lane v0.3 - sandbox loader + evaluator (SEPARATE from the frozen
instrument). This module performs NO data acquisition beyond reading one local,
SHA-pinned sandbox CSV. It MUST NOT:
  - touch any date on/after SEALED_BOUNDARY_DATE (2023-01-01),
  - reimplement row construction, fold splitting, stride, windows, target,
    baselines, features, purge, or model formulas.
Row construction and fold splitting come ONLY from the frozen instrument via
make_records() and purged_blocked_folds(). The only modeling added here is the
pre-registered M0/M1 OLS comparison and the pooled out-of-fold incremental R^2
gate, which are evaluation, not instrument logic.
"""
import os, sys, csv, hashlib
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(REPO, "src") not in sys.path:
    sys.path.insert(0, os.path.join(REPO, "src"))
from cusp_geometry_v0_3 import make_records, purged_blocked_folds  # frozen instrument

SEALED_BOUNDARY_DATE = "2023-01-01"   # owner-confirmed; nothing >= this is read
SANDBOX_LO = "2005-01-01"
SANDBOX_HI = "2022-12-31"
FROZEN_CLOSE_COLUMN = "adj_close"
BOOTSTRAP_SEED = 2026061201           # pinned for reproducibility (gate is deterministic)

M0_FEATURES = ["B1_ln_rv63", "B2_ln_rv21", "B3_abs_ret21",
               "B4_range63", "B5_ac1_63", "B6_mean_abs_dz"]
M1_EXTRA = "F2_kappa_mean"
TARGET = "y_ln_fwd_rv21"


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def load_sandbox_closes(path, expected_sha256):
    """Read ONLY the pinned sandbox file; verify hash; enforce date window;
    return (dates, closes). Never reads/returns any row >= SEALED_BOUNDARY_DATE."""
    actual = sha256_file(path)
    if actual != expected_sha256:
        raise SystemExit(f"SANDBOX HASH MISMATCH: expected {expected_sha256}, got {actual}")
    dates, closes = [], []
    with open(path, newline="") as f:
        r = csv.reader(f)
        header = next(r)
        if header != ["date", "adj_close"]:
            raise SystemExit(f"unexpected header: {header!r}")
        for rec in r:
            d, v = rec[0], rec[1]
            if d >= SEALED_BOUNDARY_DATE:
                raise SystemExit(f"sealed-boundary violation: date {d} >= {SEALED_BOUNDARY_DATE}")
            if not (SANDBOX_LO <= d <= SANDBOX_HI):
                raise SystemExit(f"out-of-window date in sandbox file: {d}")
            dates.append(d)
            closes.append(float(v))
    return header, dates, closes


def _design(rows, feature_names):
    """const + named features, in fixed order. Returns (X, y)."""
    X = np.column_stack([np.ones(len(rows))] +
                        [np.array([row[f] for row in rows]) for f in feature_names])
    y = np.array([row[TARGET] for row in rows])
    return X, y


def _ols_fit(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def evaluate(rows, folds):
    """Run the pre-registered M0/M1 OLS gate over the frozen folds.
    Returns a dict of all reportable quantities. No tuning, no alternatives."""
    m0_cols = M0_FEATURES
    m1_cols = M0_FEATURES + [M1_EXTRA]
    f2_idx_in_m1 = 1 + len(M0_FEATURES)   # const is col 0, F2 appended last

    per_fold = []
    sse_m0 = 0.0
    sse_m1 = 0.0
    improving = 0
    for fi, (train_idx, test_idx) in enumerate(folds):
        train = [rows[i] for i in train_idx]
        test = [rows[i] for i in test_idx]

        X0_tr, y_tr = _design(train, m0_cols)
        X1_tr, _    = _design(train, m1_cols)
        X0_te, y_te = _design(test, m0_cols)
        X1_te, _    = _design(test, m1_cols)

        b0 = _ols_fit(X0_tr, y_tr)
        b1 = _ols_fit(X1_tr, y_tr)

        e0 = y_te - X0_te @ b0
        e1 = y_te - X1_te @ b1
        mse0 = float(np.mean(e0 ** 2))
        mse1 = float(np.mean(e1 ** 2))
        sse_m0 += float(np.sum(e0 ** 2))
        sse_m1 += float(np.sum(e1 ** 2))

        f2_coef = float(b1[f2_idx_in_m1])
        f2_sign = "+" if f2_coef > 0 else ("-" if f2_coef < 0 else "0")
        improved = mse1 < mse0
        if improved:
            improving += 1
        per_fold.append({
            "fold": fi,
            "n_train": len(train_idx),
            "n_test": len(test_idx),
            "mse_m0": mse0,
            "mse_m1": mse1,
            "improved": improved,
            "f2_coef": f2_coef,
            "f2_sign": f2_sign,
        })

    incremental_r2 = (sse_m0 - sse_m1) / sse_m0 if sse_m0 > 0 else float("nan")
    passed = (incremental_r2 > 0) and (improving >= 7)
    return {
        "per_fold": per_fold,
        "sse_m0": sse_m0,
        "sse_m1": sse_m1,
        "incremental_r2": incremental_r2,
        "n_improving": improving,
        "passed": passed,
    }


def full_sandbox_coeffs(rows):
    """Refit M0 and M1 on ALL sandbox rows. Only call after a PASS."""
    X0, y = _design(rows, M0_FEATURES)
    X1, _ = _design(rows, M0_FEATURES + [M1_EXTRA])
    b0 = _ols_fit(X0, y)
    b1 = _ols_fit(X1, y)
    m0 = dict(zip(["const"] + M0_FEATURES, [float(x) for x in b0]))
    m1 = dict(zip(["const"] + M0_FEATURES + [M1_EXTRA], [float(x) for x in b1]))
    return m0, m1
