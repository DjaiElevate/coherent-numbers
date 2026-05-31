#!/usr/bin/env python3
"""
Lane 2 - EXPLORATORY scan: GDELT features vs next-session SPY return.

For every numeric GDELT feature, compute two Spearman rank correlations against
the joined outcome:

  * signed:    feature  vs  next_session_return        (direction)
  * magnitude: feature  vs  abs(next_session_return)    (volatility-ish size)

Then print the strongest of each. This is HYPOTHESIS GENERATION ONLY. Spearman
is rank-based so it is robust to outliers and monotone-but-nonlinear shapes, but
scanning many features inflates the chance that some correlation looks large by
luck. No multiple-comparison correction is applied to the ranking itself; a
Bonferroni reference threshold is printed alongside so the nominal p-values can
be read with appropriate skepticism.

Reads the deterministic join output (gdelt_spy_nextday.csv). Uses only rows that
have an outcome (the sealed Dec-2022 tail rows are dropped). No 2023+ data, no
targets/signals/PnL, no trading strategy.

Usage:
    python3 scripts/explore_feature_return_scan.py
    python3 scripts/explore_feature_return_scan.py --join results/lane2_join/gdelt_spy_nextday.csv
"""

from __future__ import annotations

import argparse
import glob
import sys

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

# Columns that are keys/outcomes, not GDELT features to scan.
NON_FEATURE_COLS = {
    "civil_date",
    "feature_info_date",
    "outcome_session_date",
    "next_session_return",
}

TOP_N = 15


def latest_join() -> str:
    matches = sorted(glob.glob("results/lane2_join/gdelt_spy_nextday.csv")) or \
        sorted(glob.glob("results/lane2_join/*/gdelt_spy_nextday.csv"))
    if not matches:
        sys.exit("ERROR: no join file found under results/lane2_join/")
    return matches[-1]


def scan(df: pd.DataFrame, target: pd.Series, feature_cols: list[str]) -> pd.DataFrame:
    """Spearman rho + nominal p for each feature against `target`."""
    out = []
    for col in feature_cols:
        x = df[col]
        mask = x.notna() & target.notna()
        if mask.sum() < 3 or x[mask].nunique() < 2:
            continue  # not enough variation to correlate
        rho, p = spearmanr(x[mask], target[mask])
        out.append({"feature": col, "spearman_rho": rho, "p_value": p, "n": int(mask.sum())})
    res = pd.DataFrame(out)
    res["abs_rho"] = res["spearman_rho"].abs()
    return res.sort_values("abs_rho", ascending=False).reset_index(drop=True)


def show(title: str, res: pd.DataFrame, n: int) -> None:
    print(f"\n=== {title} (top {n} by |rho|) ===")
    view = res.head(n)[["feature", "spearman_rho", "p_value", "n"]].copy()
    view["spearman_rho"] = view["spearman_rho"].map(lambda v: f"{v:+.4f}")
    view["p_value"] = view["p_value"].map(lambda v: f"{v:.2e}")
    print(view.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--join", default=None, help="path to gdelt_spy_nextday.csv")
    args = parser.parse_args()

    path = args.join or latest_join()
    df = pd.read_csv(path)

    # Keep only rows with a realized outcome (drops the sealed Dec-2022 tail).
    df = df[df["next_session_return"].notna()].copy()

    # Numeric GDELT features = numeric columns that aren't keys/outcomes.
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    feature_cols = [c for c in numeric_cols if c not in NON_FEATURE_COLS]

    signed_target = df["next_session_return"]
    magnitude_target = df["next_session_return"].abs()

    signed = scan(df, signed_target, feature_cols)
    magnitude = scan(df, magnitude_target, feature_cols)

    n_features = len(feature_cols)
    n_rows = len(df)
    n_tests = 2 * n_features
    bonferroni = 0.05 / n_tests if n_tests else float("nan")

    print(f"join file              : {path}")
    print(f"rows used (with outcome): {n_rows}")
    print(f"numeric features scanned: {n_features}")
    print(f"tests run (2 per feature): {n_tests}")
    print(f"Bonferroni 0.05 threshold: p < {bonferroni:.2e} (reference only)")

    show("SIGNED-RETURN correlations", signed, TOP_N)
    show("ABSOLUTE-RETURN (magnitude) correlations", magnitude, TOP_N)

    print(
        "\nNOTE: Exploratory only. These are uncorrected Spearman correlations from "
        "a wide scan; treat the rankings as candidates for follow-up, not findings. "
        "No causal/predictive claim, no trading interpretation."
    )


if __name__ == "__main__":
    main()
