#!/usr/bin/env python3
"""
Lane 2 - EXPLORATORY detrended scan (the last clean first-pass check).

For each numeric feature:
    prior_mean/std = trailing window of size --window, shifted by 1 (today excluded)
    residual (surge) = (x_today - prior_mean) / prior_std
    abs_residual     = |residual|

Three Spearman scans against the next-session outcome:
    (1) residual       vs  next_session_return         (direction)
    (2) residual       vs  |next_session_return|        (monotone magnitude)
    (3) abs_residual   vs  |next_session_return|        (non-monotone surprise magnitude)

Exploratory only. No 2023+ (join already excludes it). No targets/signals/PnL. Print-only.
"""

import argparse
import sys

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

DATE_COL = "civil_date"
RET_COL = "next_session_return"
EXCLUDE = {
    DATE_COL, RET_COL, "feature_info_date", "outcome_session_date",
    "outcome_available", "year", "abs_ret",
}
VOLUME_TOKENS = ("roll", "total", "count", "rows_from_offset", "coverage",
                 "neighbor_offset_sum", "volume", "num_", "_n_", "freq")


def is_volume_like(name):
    n = name.lower()
    return any(tok in n for tok in VOLUME_TOKENS)


SKIP_TOKENS = ("has_full", "warmup", "available")

def numeric_features(df):
    out = []
    for c in df.columns:
        if c in EXCLUDE:
            continue
        if any(tok in c.lower() for tok in SKIP_TOKENS):
            continue
        if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique(dropna=True) > 1:
            out.append(c)
    return out


def spear(a, b):
    m = a.notna() & b.notna()
    if m.sum() < 250:
        return np.nan, np.nan
    rho, p = spearmanr(a[m], b[m])
    return rho, p


def top_block(title, res, rho_col, p_col, bonf, floor):
    print(f"=== {title} ===")
    sub = res.reindex(res[rho_col].abs().sort_values(ascending=False).index).head(15)
    for _, r in sub.iterrows():
        sig = "*" if (not np.isnan(r[p_col]) and r[p_col] < bonf) else " "
        vol = "vol?" if is_volume_like(r["feature"]) else "    "
        print(f"  {sig} {vol} {r['feature']:<34} rho={r[rho_col]:>7.3f}  p={r[p_col]:.1e}")
    print()


def survivors(res, rho_col, p_col, bonf, floor):
    mask = (res[p_col] < bonf) & (res[rho_col].abs() >= floor)
    return res.loc[mask, "feature"].tolist()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--join", required=True)
    ap.add_argument("--window", type=int, default=60)
    ap.add_argument("--min-periods", type=int, default=20)
    ap.add_argument("--rho-floor", type=float, default=0.10,
                    help="practical effect-size floor for calling something a candidate")
    args = ap.parse_args()

    df = pd.read_csv(args.join)
    for need in (DATE_COL, RET_COL):
        if need not in df.columns:
            sys.exit(f"ERROR: join file missing '{need}'")

    df[DATE_COL] = pd.to_datetime(df[DATE_COL])
    df = df.sort_values(DATE_COL).reset_index(drop=True)
    df["abs_ret"] = df[RET_COL].abs()
    have = df[RET_COL].notna()

    feats = numeric_features(df)

    resid = pd.DataFrame(index=df.index)
    for c in feats:
        roll = df[c].rolling(args.window, min_periods=args.min_periods)
        mean = roll.mean().shift(1)
        std = roll.std().shift(1).replace(0, np.nan)
        resid[c] = (df[c] - mean) / std
    absresid = resid.abs()

    recs = []
    for c in feats:
        r_sgn, p_sgn = spear(resid.loc[have, c], df.loc[have, RET_COL])
        r_mag, p_mag = spear(resid.loc[have, c], df.loc[have, "abs_ret"])
        r_abs, p_abs = spear(absresid.loc[have, c], df.loc[have, "abs_ret"])
        r_lvl, p_lvl = spear(df.loc[have, c], df.loc[have, "abs_ret"])
        recs.append((c, r_sgn, p_sgn, r_mag, p_mag, r_abs, p_abs, r_lvl, p_lvl))
    res = pd.DataFrame(recs, columns=[
        "feature", "resid_signed", "p_signed", "resid_mag", "p_mag",
        "absresid_mag", "p_abs", "level_mag", "p_lvl",
    ])

    n_tests = len(feats)
    bonf = 0.05 / max(n_tests, 1)
    floor = args.rho_floor

    print(f"join file               : {args.join}")
    print(f"rows used (with outcome): {int(have.sum())}")
    print(f"numeric features scanned: {n_tests}")
    print(f"window / min_periods    : {args.window} / {args.min_periods}")
    print(f"bonferroni ref (p<)     : {bonf:.2e}  [EXPLORATORY; volume feats are collinear,")
    print(f"                          so these are NOT independent tests - read loosely]")
    print(f"candidate rule          : p < bonferroni AND |rho| >= {floor}")
    print()

    top_block("(1) residual vs SIGNED next_session_return  (direction)",
              res, "resid_signed", "p_signed", bonf, floor)
    top_block("(2) residual vs |next_session_return|  (monotone magnitude)",
              res, "resid_mag", "p_mag", bonf, floor)
    top_block("(3) |residual| vs |next_session_return|  (non-monotone surprise magnitude)",
              res, "absresid_mag", "p_abs", bonf, floor)

    dir_c = survivors(res, "resid_signed", "p_signed", bonf, floor)
    mag_resid_c = survivors(res, "resid_mag", "p_mag", bonf, floor)
    absres_c = survivors(res, "absresid_mag", "p_abs", bonf, floor)
    level_c = survivors(res, "level_mag", "p_lvl", bonf, floor)

    if level_c:
        survived = [f for f in level_c if f in mag_resid_c or f in absres_c]
        mag_level_read = "candidate (level effect survives detrend)" if survived \
            else "confounded (level effect collapses on detrend)"
    else:
        mag_level_read = "no material level effect found"

    nonvol_survivors = [f for f in absres_c if not is_volume_like(f)]

    print("=== FINAL READ (heuristic; exploratory only) ===")
    print(f"direction                     : {'candidate' if dir_c else 'null'}"
          + (f"  {dir_c}" if dir_c else ""))
    print(f"magnitude level               : {mag_level_read}")
    print(f"magnitude residual            : {'candidate' if mag_resid_c else 'null'}"
          + (f"  {mag_resid_c}" if mag_resid_c else ""))
    print(f"non-monotone absolute-residual: {'candidate' if absres_c else 'null'}"
          + (f"  {absres_c}" if absres_c else ""))
    if absres_c:
        print(f"  -> non-volume survivors in (3): {nonvol_survivors or 'NONE (all volume-like)'}")
    print()
    if not (dir_c or mag_resid_c or absres_c):
        print("=> Clean exploratory NULL: no clear next-session SPY direction or magnitude")
        print("   relationship from this GDELT daily attention feature set after removing drift.")
    else:
        print("=> Something cleared the candidate bar - inspect survivors above (esp. any")
        print("   NON-volume feature in scan 3) before reading into it. Still exploratory.")


if __name__ == "__main__":
    main()
