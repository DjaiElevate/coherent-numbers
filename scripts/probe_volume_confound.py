#!/usr/bin/env python3
"""
Lane 2 - EXPLORATORY probe: is the GDELT-volume vs |return| correlation a
slow trend / regime confound, or a genuine higher-frequency relationship?

The wide scan found that |next_session_return| correlates (rho ~ -0.15..-0.18)
with a family of GDELT activity-volume / coverage features. Those features trend
over 2013-2022 and co-move with volatility regimes, so a pooled correlation can
be driven entirely by shared slow structure rather than any day-to-day link.

For each top magnitude feature this prints, side by side:

  rho_pooled       : plain Spearman(feature, |ret|)            -- the headline number
  rho_partial_time : Spearman partial-correlation controlling for ordinal date
                     (removes any monotone time trend shared by both series)
  rho_detrend_w    : Spearman of rolling-residuals, window W   -- removes slow
                     components with timescale longer than ~W sessions
  year_rho_mean    : mean of the per-calendar-year Spearman values
  year_rho_range   : [min, max] across years (sign flips => regime-dependent)

Also reports each feature's own trend (Spearman vs ordinal date) and the trend
of |ret| itself, to show the confound mechanism.

If rho collapses toward 0 under partial-time AND detrending, and the within-year
values are small/inconsistent, the pooled correlation is mostly a trend/regime
confound. If it survives, there is a higher-frequency component worth a look.

Exploratory only. No targets/signals/PnL, no trading claim, no 2023+ data.

Usage:
    python3 scripts/probe_volume_confound.py \
        --join results/lane2_join/gdelt_spy_nextday.csv --window 60
"""

from __future__ import annotations

import argparse
import sys

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, rankdata, spearmanr

NON_FEATURE_COLS = {
    "civil_date",
    "feature_info_date",
    "outcome_session_date",
    "next_session_return",
}


def partial_spearman(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> float:
    """Spearman partial correlation of x,y controlling for z (rank-residual)."""
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)

    def resid(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        slope, intercept = np.polyfit(b, a, 1)
        return a - (slope * b + intercept)

    ex, ey = resid(rx, rz), resid(ry, rz)
    if np.std(ex) == 0 or np.std(ey) == 0:
        return float("nan")
    return float(pearsonr(ex, ey)[0])


def rolling_detrend_spearman(x: pd.Series, y: pd.Series, w: int) -> float:
    """Spearman after removing a centered rolling mean (timescale ~ w) from both."""
    minp = max(2, w // 2)
    xr = x - x.rolling(w, center=True, min_periods=minp).mean()
    yr = y - y.rolling(w, center=True, min_periods=minp).mean()
    mask = xr.notna() & yr.notna()
    if mask.sum() < 3 or xr[mask].nunique() < 2:
        return float("nan")
    return float(spearmanr(xr[mask], yr[mask])[0])


def within_year_spearman(df: pd.DataFrame, col: str, target: pd.Series) -> list[float]:
    years = pd.to_datetime(df["civil_date"]).dt.year
    vals = []
    for _, idx in df.groupby(years).groups.items():
        x = df.loc[idx, col]
        t = target.loc[idx]
        mask = x.notna() & t.notna()
        if mask.sum() >= 20 and x[mask].nunique() >= 2:
            vals.append(float(spearmanr(x[mask], t[mask])[0]))
    return vals


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--join", required=True, help="path to gdelt_spy_nextday.csv")
    parser.add_argument("--window", type=int, default=60, help="detrend window (sessions)")
    parser.add_argument("--top", type=int, default=12, help="how many features to probe")
    args = parser.parse_args()

    df = pd.read_csv(args.join)
    df = df[df["next_session_return"].notna()].copy()
    df = df.sort_values("civil_date").reset_index(drop=True)

    target = df["next_session_return"].abs()           # magnitude
    ord_time = np.arange(len(df), dtype=float)          # ordinal date (sorted)

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    feature_cols = [c for c in numeric_cols if c not in NON_FEATURE_COLS]

    # Rank features by pooled |Spearman| with |ret|, then probe the strongest.
    ranked = []
    for col in feature_cols:
        m = df[col].notna() & target.notna()
        if m.sum() < 3 or df[col][m].nunique() < 2:
            continue
        ranked.append((col, abs(spearmanr(df[col][m], target[m])[0])))
    ranked.sort(key=lambda kv: kv[1], reverse=True)
    probe_cols = [c for c, _ in ranked[: args.top]]

    target_trend = spearmanr(ord_time, target)[0]

    rows = []
    for col in probe_cols:
        m = df[col].notna() & target.notna()
        x, y, z = df[col][m].to_numpy(), target[m].to_numpy(), ord_time[m.to_numpy()]
        rho_pooled = spearmanr(x, y)[0]
        rho_partial = partial_spearman(x, y, z)
        rho_detrend = rolling_detrend_spearman(df[col], target, args.window)
        feat_trend = spearmanr(z, x)[0]
        yr = within_year_spearman(df, col, target)
        rows.append({
            "feature": col,
            "rho_pooled": rho_pooled,
            "rho_partial_time": rho_partial,
            f"rho_detrend_w{args.window}": rho_detrend,
            "feat_vs_time": feat_trend,
            "year_rho_mean": np.mean(yr) if yr else float("nan"),
            "year_rho_min": np.min(yr) if yr else float("nan"),
            "year_rho_max": np.max(yr) if yr else float("nan"),
        })

    res = pd.DataFrame(rows)
    fmt = {c: (lambda v: f"{v:+.4f}") for c in res.columns if c != "feature"}

    print(f"join file              : {args.join}")
    print(f"rows used (with outcome): {len(df)}")
    print(f"detrend window          : {args.window} sessions")
    print(f"features probed         : {len(probe_cols)} (strongest |return| correlations)")
    print(f"|return| vs ordinal time: rho = {target_trend:+.4f}  "
          f"(if non-trivial, |ret| itself has slow/regime structure)")
    print("\n=== confound probe (magnitude target = |next_session_return|) ===")
    print(res.to_string(index=False, formatters=fmt))

    print(
        "\nHOW TO READ: rho_pooled is the headline. If rho_partial_time and "
        f"rho_detrend_w{args.window} both shrink toward 0 vs rho_pooled, the signal "
        "lives in the slow trend/regime that feat_vs_time exposes -> confound. "
        "If they hold up and year_rho stays same-signed and non-trivial, there is "
        "a higher-frequency component. Exploratory only; no claim either way yet."
    )


if __name__ == "__main__":
    main()
