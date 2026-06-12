"""
Runner for the Cusp Geometry Lane v0.3 sandbox gate. Loads ONLY the pinned
sandbox SPY file (2005-2022, adj_close), feeds closes into the frozen
make_records(), splits with frozen purged_blocked_folds(), runs the
pre-registered M0/M1 OLS comparison, and prints a metadata-only report.
Prints NO raw data rows. Touches NO sealed (2023+) data.
"""
import os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))
from cusp_geometry_v0_3_sandbox import (
    load_sandbox_closes, evaluate, full_sandbox_coeffs, sha256_file,
    FROZEN_CLOSE_COLUMN, BOOTSTRAP_SEED,
)
from cusp_geometry_v0_3 import make_records, purged_blocked_folds

INSTRUMENT_COMMIT = "4536be27f6955be72bdb7abad4b4cb38ac1278ad"
SANDBOX_FILE = os.path.join(REPO, "data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv")
SANDBOX_SHA256 = "5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901"


def main():
    header, dates, closes = load_sandbox_closes(SANDBOX_FILE, SANDBOX_SHA256)

    rows = make_records(closes)
    folds = purged_blocked_folds(len(rows))
    res = evaluate(rows, folds)

    L = []
    L.append("# Cusp Geometry Lane v0.3 - Sandbox Gate Report")
    L.append("")
    L.append(f"instrument_commit_sha: {INSTRUMENT_COMMIT}")
    L.append(f"sandbox_file: {os.path.relpath(SANDBOX_FILE, REPO)}")
    L.append(f"sandbox_sha256: {sha256_file(SANDBOX_FILE)}")
    L.append(f"close_column_used: {FROZEN_CLOSE_COLUMN}")
    L.append(f"bootstrap_seed_pinned: {BOOTSTRAP_SEED}")
    L.append(f"first_loaded_date: {dates[0]}")
    L.append(f"last_loaded_date: {dates[-1]}")
    L.append(f"num_closes_loaded: {len(closes)}")
    L.append(f"num_records_make_records: {len(rows)}")
    L.append("")
    L.append("## Folds")
    L.append("fold | n_test (fold size) | n_train (after purge)")
    for pf in res["per_fold"]:
        L.append(f"{pf['fold']:>4} | {pf['n_test']:>4} | {pf['n_train']:>5}")
    L.append("")
    L.append("## Per-fold model comparison")
    L.append("fold | MSE_M0 | MSE_M1 | improved | F2_sign | F2_coef")
    for pf in res["per_fold"]:
        L.append(f"{pf['fold']:>4} | {pf['mse_m0']:.10e} | {pf['mse_m1']:.10e} | "
                 f"{str(pf['improved']):>5} | {pf['f2_sign']:>1} | {pf['f2_coef']:+.6e}")
    L.append("")
    L.append("## Pooled out-of-fold")
    L.append(f"pooled_SSE_M0: {res['sse_m0']:.10e}")
    L.append(f"pooled_SSE_M1: {res['sse_m1']:.10e}")
    L.append(f"pooled_incremental_R2: {res['incremental_r2']:.10e}")
    L.append(f"num_improving_folds: {res['n_improving']} / {len(res['per_fold'])}")
    L.append(f"PASS_condition: incremental_R2 > 0 AND improving >= 7")
    L.append(f"RESULT: {'PASS' if res['passed'] else 'FAIL'}")
    L.append("")
    if res["passed"]:
        m0, m1 = full_sandbox_coeffs(rows)
        L.append("## Full-sandbox coefficients (PASS only)")
        L.append("M0:")
        for k, v in m0.items():
            L.append(f"  {k}: {v:+.8e}")
        L.append("M1:")
        for k, v in m1.items():
            L.append(f"  {k}: {v:+.8e}")
        L.append("")
    L.append("No sealed data was accessed.")
    print("\n".join(L))


if __name__ == "__main__":
    main()
