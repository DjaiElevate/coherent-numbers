#!/usr/bin/env python3
"""
Lane 2 - join GDELT daily features to the NEXT SPY trading session's return.

For each GDELT feature row (civil_date t), attach:

* feature_info_date     : the latest date the feature row may depend on
* outcome_session_date  : the first SPY trading session STRICTLY AFTER feature_info_date
* next_session_return   : that session's adj_close close-to-close return

Why feature_info_date defaults to civil_date + 1:
The Step 2 GDELT feature table includes plus-one / neighbor-style features such as
rows_from_offset_plus_1. That means a row labeled civil_date=t may contain
information from t+1. To avoid lookahead, the market outcome must be strictly
after t+1, not merely after t.

If you later create a feature set that excludes all plus-one/future-offset fields,
you can run with:
    --feature-info-lag-days 0

GDELT rows whose next outcome session would fall outside the sealed SPY file
(for example into 2023+) get NaN outcomes. They are left empty on purpose.

Usage:
    python join_gdelt_spy_nextday.py \
        --gdelt results/lane2_gdelt1_step2_daily_features/<ts>/step2_daily_features.csv \
        --spy   results/lane2_market_data_acquisition/<ts>/market_daily_spy.csv \
        --out   results/lane2_join/gdelt_spy_nextday.csv
"""

from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

GDELT_DATE_CANDIDATES = ["civil_date", "date", "gdelt_date", "day"]
RETURN_PRICE_COL = "adj_close"


def find_gdelt_date_col(df: pd.DataFrame, explicit: str | None = None) -> str:
    if explicit:
        if explicit not in df.columns:
            sys.exit(f"ERROR: --gdelt-date-col '{explicit}' not in GDELT columns")
        return explicit

    for col in GDELT_DATE_CANDIDATES:
        if col in df.columns:
            return col

    sys.exit(
        "ERROR: no GDELT date column found. "
        f"Tried {GDELT_DATE_CANDIDATES}; first columns are {list(df.columns)[:20]}"
    )


def require_columns(df: pd.DataFrame, cols: list[str], label: str) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        sys.exit(f"ERROR: {label} missing required columns: {missing}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gdelt", required=True, help="Path to Step 2 GDELT feature CSV")
    parser.add_argument("--spy", required=True, help="Path to SPY daily market CSV")
    parser.add_argument("--out", default="results/lane2_join/gdelt_spy_nextday.csv")
    parser.add_argument("--gdelt-date-col", default=None)
    parser.add_argument(
        "--feature-info-lag-days",
        type=int,
        default=1,
        help=(
            "Days added to GDELT civil_date to define feature_info_date. "
            "Default 1 protects against plus-one GDELT features."
        ),
    )
    args = parser.parse_args()

    gdelt = pd.read_csv(args.gdelt)
    spy = pd.read_csv(args.spy)

    gdate = find_gdelt_date_col(gdelt, args.gdelt_date_col)

    require_columns(spy, ["market_date", RETURN_PRICE_COL], "SPY CSV")

    # --- SPY sanity and return construction ---
    spy = spy.copy()
    spy["market_date"] = pd.to_datetime(spy["market_date"], errors="raise")
    spy[RETURN_PRICE_COL] = pd.to_numeric(spy[RETURN_PRICE_COL], errors="raise")

    spy = spy.sort_values("market_date").reset_index(drop=True)

    if spy["market_date"].duplicated().any():
        dupes = spy.loc[spy["market_date"].duplicated(), "market_date"].head().tolist()
        sys.exit(f"ERROR: duplicate SPY market_date values, examples: {dupes}")

    if not spy["market_date"].is_monotonic_increasing:
        sys.exit("ERROR: SPY market_date is not sorted ascending")

    if (spy["market_date"] >= pd.Timestamp("2023-01-01")).any():
        sys.exit("ERROR: SPY file contains 2023+ rows; refusing to join")

    if spy["market_date"].max() > pd.Timestamp("2022-12-31"):
        sys.exit("ERROR: SPY max market_date is after 2022-12-31")

    # Return for each SPY session: current adj_close / prior session adj_close - 1.
    # This is safe as an outcome only when the session date is strictly after feature_info_date.
    spy["next_session_return"] = spy[RETURN_PRICE_COL].pct_change()

    spy_keys = spy[["market_date", "next_session_return"]].rename(
        columns={"market_date": "outcome_session_date"}
    )

    # --- GDELT feature information date ---
    g = gdelt.copy()
    g[gdate] = pd.to_datetime(g[gdate], errors="raise")
    g["feature_info_date"] = g[gdate] + pd.to_timedelta(args.feature_info_lag_days, unit="D")
    g = g.sort_values("feature_info_date").reset_index(drop=True)

    # --- Map each feature row to the first SPY session STRICTLY AFTER feature_info_date ---
    joined = pd.merge_asof(
        g,
        spy_keys,
        left_on="feature_info_date",
        right_on="outcome_session_date",
        direction="forward",
        allow_exact_matches=False,
    )

    # --- Explicit leakage guard ---
    have = joined["outcome_session_date"].notna()
    if not (joined.loc[have, "outcome_session_date"] > joined.loc[have, "feature_info_date"]).all():
        bad = joined.loc[
            have & ~(joined["outcome_session_date"] > joined["feature_info_date"]),
            [gdate, "feature_info_date", "outcome_session_date"],
        ].head()
        sys.exit(f"LEAKAGE ERROR: outcome session not strictly after feature_info_date:\n{bad}")

    n_total = len(joined)
    n_out = int(have.sum())

    # Format date columns for CSV.
    joined[gdate] = joined[gdate].dt.strftime("%Y-%m-%d")
    joined["feature_info_date"] = joined["feature_info_date"].dt.strftime("%Y-%m-%d")
    joined["outcome_session_date"] = joined["outcome_session_date"].dt.strftime("%Y-%m-%d")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    joined.to_csv(args.out, index=False)

    print(f"gdelt file             : {args.gdelt}")
    print(f"spy file               : {args.spy}")
    print(f"gdelt date column      : {gdate}")
    print(f"feature info lag days  : {args.feature_info_lag_days}")
    print(f"gdelt rows             : {n_total}")
    print(f"rows with outcome      : {n_out}")
    print(f"rows without outcome   : {n_total - n_out}")
    print(f"return basis           : {RETURN_PRICE_COL}, close-to-close")
    print("leakage check          : PASS (outcome strictly after feature_info_date)")
    print(f"saved                  : {args.out}")


if __name__ == "__main__":
    main()
