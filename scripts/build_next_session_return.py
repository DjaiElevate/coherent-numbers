"""Build the next-session SPY return outcome for each GDELT civil_date.

For each GDELT civil_date:
    feature_info_date   = civil_date + 1 day        (max info-availability date)
    outcome_session_date = first SPY trading session strictly after info_date
    prev_session_date    = the SPY session immediately before the outcome session
                           (== last session on/before info_date)
    next_session_return  = adj_close[outcome] / adj_close[prev] - 1

No-lookahead: the outcome session is strictly after the information boundary,
and the entry price (prev session close) is knowable on/before that boundary.

This reads only the `civil_date` column from the Step 2 feature file and the
acquired SPY CSV. It does NOT modify the Step 2 features, and it does NOT fetch
or read any 2023+ market data. Tail civil_dates whose outcome session would fall
into the sealed 2023 region get a null return with outcome_available=False.

Usage:
    python3 scripts/build_next_session_return.py
    python3 scripts/build_next_session_return.py --spy <path> --features <path>
"""

from __future__ import annotations

import argparse
import glob
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]

SEAL = "2022-12-31"  # no outcome may use a session after this date

FEATURES_GLOB = "results/lane2_gdelt1_step2_daily_features/*/step2_daily_features.csv"
SPY_GLOB = "results/lane2_market_data_acquisition/*/market_daily_spy.csv"

OUTPUT_PARENT = REPO_ROOT / "results" / "lane2_next_session_return"
OUTPUT_FILENAME = "next_session_return.csv"

OUT_COLUMNS = [
    "civil_date",
    "feature_info_date",
    "prev_session_date",
    "outcome_session_date",
    "adj_close_prev",
    "adj_close_outcome",
    "next_session_return",
    "outcome_available",
]


def _latest(pattern: str) -> Path:
    matches = sorted(glob.glob(str(REPO_ROOT / pattern)))
    if not matches:
        raise SystemExit(f"no file matches {pattern}")
    return Path(matches[-1])


def build(spy_path: Path, features_path: Path) -> pd.DataFrame:
    # Trading sessions, sorted, with adj_close lookup. Sealed at 2022-12-31.
    spy = pd.read_csv(spy_path, usecols=["market_date", "adj_close"])
    spy = spy[spy["market_date"] <= SEAL].sort_values("market_date")
    sessions = spy["market_date"].to_numpy()  # 'YYYY-MM-DD' strings, ascending
    adj_close = dict(zip(spy["market_date"], spy["adj_close"]))

    civil_dates = pd.read_csv(features_path, usecols=["civil_date"])["civil_date"]

    rows = []
    for civil_date in civil_dates:
        info_date = (
            datetime.strptime(civil_date, "%Y-%m-%d") + timedelta(days=1)
        ).strftime("%Y-%m-%d")

        # First session strictly after info_date (searchsorted on the right).
        idx = int(np.searchsorted(sessions, info_date, side="right"))
        available = idx < len(sessions) and idx >= 1

        if available:
            outcome_date = sessions[idx]
            prev_date = sessions[idx - 1]
            ac_prev = adj_close[prev_date]
            ac_outcome = adj_close[outcome_date]
            ret = ac_outcome / ac_prev - 1.0
        else:
            # Outcome session would fall past the seal (or no prior session).
            outcome_date = prev_date = ""
            ac_prev = ac_outcome = ret = np.nan

        rows.append(
            {
                "civil_date": civil_date,
                "feature_info_date": info_date,
                "prev_session_date": prev_date,
                "outcome_session_date": outcome_date,
                "adj_close_prev": ac_prev,
                "adj_close_outcome": ac_outcome,
                "next_session_return": ret,
                "outcome_available": available,
            }
        )

    return pd.DataFrame(rows)[OUT_COLUMNS]


def sanity_checks(df: pd.DataFrame) -> None:
    avail = df[df["outcome_available"]]

    # Outcome session strictly after the information boundary.
    assert (avail["outcome_session_date"] > avail["feature_info_date"]).all(), \
        "an outcome session is not strictly after feature_info_date"
    # Entry session strictly before the outcome session.
    assert (avail["prev_session_date"] < avail["outcome_session_date"]).all(), \
        "prev_session is not before outcome_session"
    # Entry price knowable on/before the info boundary (no lookahead).
    assert (avail["prev_session_date"] <= avail["feature_info_date"]).all(), \
        "prev_session is after feature_info_date (lookahead)"
    # Seal: nothing references a session past 2022-12-31.
    assert (avail["outcome_session_date"] <= SEAL).all(), "outcome session past seal"
    # Available rows have a return; unavailable rows do not.
    assert avail["next_session_return"].notna().all(), "available row missing return"
    assert df.loc[~df["outcome_available"], "next_session_return"].isna().all(), \
        "unavailable row has a return"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spy", type=Path, default=None, help="SPY daily CSV")
    parser.add_argument("--features", type=Path, default=None,
                        help="Step 2 feature CSV (civil_date column read only)")
    parser.add_argument("--out", type=Path, default=None, help="output CSV path")
    args = parser.parse_args()

    spy_path = args.spy or _latest(SPY_GLOB)
    features_path = args.features or _latest(FEATURES_GLOB)

    df = build(spy_path, features_path)
    sanity_checks(df)

    if args.out is not None:
        out_path = args.out
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_path = OUTPUT_PARENT / stamp / OUTPUT_FILENAME
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    n_avail = int(df["outcome_available"].sum())
    n_unavail = len(df) - n_avail
    print(f"SPY:      {spy_path}")
    print(f"features: {features_path}")
    print(f"Saved {len(df)} rows to {out_path}")
    print(f"  outcome available: {n_avail}")
    print(f"  unavailable (outcome session past {SEAL} seal): {n_unavail}")
    if n_unavail:
        tail = df.loc[~df["outcome_available"], "civil_date"]
        print(f"  unavailable civil_dates: {tail.min()} .. {tail.max()}")


if __name__ == "__main__":
    sys.exit(main())
