"""Fetch SPY daily OHLCV from Yahoo Finance (via yfinance) and save a CSV.

Scope: 2013-04-01 through 2022-12-31, SPY only. This is a plain data-pull so
we can look at the market data directly. It does NOT compute returns, forward
returns, targets, signals, labels, CAR, volatility, PnL, or instruments, and it
does NOT touch GDELT or the Step 2 feature outputs.

Guardrails kept (the ones that protect the research):
  - the date window ends at 2022-12-31; 2023+ rows are dropped, never saved;
  - the saved schema is exactly 12 columns, market-data-only.

By default it writes to a fresh UTC-timestamped subdirectory under
results/lane2_market_data_acquisition/, e.g.
results/lane2_market_data_acquisition/20260601T000000Z/market_daily_spy.csv

Usage:
    python3 scripts/acquire_spy_daily.py
    python3 scripts/acquire_spy_daily.py --out some/other/path.csv
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf

REPO_ROOT = Path(__file__).resolve().parents[1]

SYMBOL = "SPY"
START = "2013-04-01"
END = "2022-12-31"  # inclusive; no 2023+ rows are saved

SOURCE_VENDOR = "yahoo_finance_via_yfinance"
SOURCE_TIMEZONE = "America/New_York"
SOURCE_CALENDAR = "XNYS"

# The exact 12-column schema we save, in order.
COLUMNS = [
    "market_date",
    "symbol",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
    "source_vendor",
    "source_retrieved_at_utc",
    "source_timezone",
    "source_calendar",
]

ACQUISITION_PARENT = REPO_ROOT / "results" / "lane2_market_data_acquisition"
OUTPUT_FILENAME = "market_daily_spy.csv"


def default_out() -> Path:
    """A fresh UTC-timestamped output path under the acquisition parent dir."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return ACQUISITION_PARENT / stamp / OUTPUT_FILENAME

# Columns we never want to appear (returns/outcomes/targets/signals/PnL, etc.).
FORBIDDEN_TOKENS = [
    "return",
    "forward",
    "target",
    "signal",
    "label",
    "car",
    "abnormal",
    "volatility",
    "pnl",
    "instrument",
]


def fetch_spy() -> pd.DataFrame:
    """Download raw SPY daily bars and shape them into the 12-column table."""
    retrieved_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # yfinance's `end` is exclusive, so add a day to include 2022-12-31.
    raw = yf.download(
        SYMBOL,
        start=START,
        end="2023-01-01",
        interval="1d",
        auto_adjust=False,
        actions=False,
        progress=False,
    )
    if raw.empty:
        raise SystemExit("yfinance returned no rows for SPY — check connectivity.")

    # yfinance can return a MultiIndex on columns when given a ticker; flatten it.
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    raw = raw.reset_index()

    df = pd.DataFrame()
    df["market_date"] = pd.to_datetime(raw["Date"]).dt.strftime("%Y-%m-%d")
    df["symbol"] = SYMBOL
    df["open"] = raw["Open"]
    df["high"] = raw["High"]
    df["low"] = raw["Low"]
    df["close"] = raw["Close"]
    df["adj_close"] = raw["Adj Close"]
    df["volume"] = raw["Volume"].astype("int64")
    df["source_vendor"] = SOURCE_VENDOR
    df["source_retrieved_at_utc"] = retrieved_at
    df["source_timezone"] = SOURCE_TIMEZONE
    df["source_calendar"] = SOURCE_CALENDAR

    # Belt-and-suspenders: drop anything outside the window before we go further.
    df = df[(df["market_date"] >= START) & (df["market_date"] <= END)]
    df = df.sort_values("market_date").reset_index(drop=True)

    return df[COLUMNS]


def sanity_checks(df: pd.DataFrame) -> None:
    """Plain assertions so a bad pull fails loudly instead of being saved."""
    assert set(df["symbol"].unique()) == {SYMBOL}, "symbol column is not all SPY"
    assert df["market_date"].max() <= END, f"found a row after {END}"
    assert not df["market_date"].duplicated().any(), "duplicate market_date rows"
    assert df["market_date"].is_monotonic_increasing, "dates are not sorted ascending"
    assert list(df.columns) == COLUMNS, "schema is not the exact 12 columns"

    lowered = [c.lower() for c in df.columns]
    leaked = [c for c in lowered if any(tok in c for tok in FORBIDDEN_TOKENS)]
    assert not leaked, f"forbidden return/outcome column(s) present: {leaked}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch SPY daily data to CSV.")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="output CSV path (default: a fresh timestamped dir under "
        f"{ACQUISITION_PARENT})",
    )
    args = parser.parse_args()
    out_path = args.out if args.out is not None else default_out()

    df = fetch_spy()
    sanity_checks(df)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    print(f"Saved {len(df)} rows to {out_path}")
    print(f"Date range: {df['market_date'].min()} .. {df['market_date'].max()}")
    print(f"Columns: {', '.join(df.columns)}")


if __name__ == "__main__":
    sys.exit(main())
