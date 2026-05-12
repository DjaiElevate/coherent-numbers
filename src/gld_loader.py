"""GLD daily data loader for the harmonic calendar pre-registered study.

Design memo:     docs/harmonic_calendar_gld_v0.1.md (commit 11b00d6)
SPY loader anchor: commit 30faabb
Data freeze:     commit 4dc56c4

RUNTIME DATA SOURCE
===================
The canonical runtime loader (load_gld) reads from a FROZEN LOCAL CSV FILE,
not from a live network request. Yahoo Finance is the acquisition source only.
The frozen CSV was produced once (commit 4dc56c4) and is thereafter treated as
immutable. Its SHA256 hash is embedded in the filename so any subsequent
modification is immediately detectable at load time.

DATA PROVENANCE (locked before any analysis)
============================================
Acquisition source:   Yahoo Finance v8 chart API (direct HTTP)
                      Field: indicators.adjclose[0].adjclose
Ticker:               GLD (SPDR Gold Shares ETF)
Adjusted price field: Adjusted close — adjusted for all splits and dividends.
Start date:           2004-11-18 (GLD ETF inception; earliest available)
End / cutoff:         2024-12-31 — matches the SPY freeze terminus, preserving
                      cross-cell calendar comparability. Data from 2025-01-01
                      onward is excluded unconditionally.
Frozen CSV location:  data/raw/gld_yahoo_v8_20041118_20241231_{sha256}.csv
                      The SHA256 is computed over the full CSV byte contents
                      and embedded in the filename. load_gld() verifies the
                      hash against the file contents on every load.
Missing data policy:  Rows where adj_close is NaN (source returned a date but
                      no price) are forward-filled up to FILL_LIMIT = 5
                      consecutive rows. Dates absent from the source entirely
                      are not inserted. Rows with remaining NaN after the fill
                      window are dropped.
NaN / inf policy:     After gap-fill and log computation, any row where
                      adj_close, log_return, or log_return_sq is NaN or ±inf
                      is dropped. Rows where adj_close ≤ 0 (log undefined) are
                      dropped before log computation.
Partial year:         Only complete trading days through 2024-12-31 are
                      included. Partial 2025 / 2026 data is excluded.

TRAIN / HOLDOUT SPLIT (locked in docs/harmonic_calendar_gld_v0.1.md,
section "Train/holdout split — Decision": Option 1 selected)
===============================================================================
Training:  dates in [START_DATE, HOLDOUT_START)   — 2004-11-18 to 2014-12-31 (~10.1 years)
Holdout:   dates in [HOLDOUT_START, CUTOFF_DATE]  — 2015-01-01 to 2024-12-31 (10 years)
           The holdout is UNTOUCHED until after the training-phase PSS is computed.
           Interpretation caveat (pre-registered): GLD training window (~10.1 years)
           is shorter than SPY (~22 years); per-anchor PSS estimates in training have
           wider uncertainty. This is accepted as a limitation of the GLD cell.

WHAT THIS MODULE DOES NOT DO
=============================
- Does not compute PSS (Phase Structure Score)
- Does not run the analysis protocol
- Does not assign calendar phases
- Does not make live network requests during canonical loading
- RUN_ANALYSIS remains False
"""

import hashlib
import math
import os
import re
import datetime
import pandas as pd
from typing import Tuple

# ── Provenance constants (locked before any analysis) ─────────────────────────

TICKER             = "GLD"
ACQUISITION_SOURCE = "Yahoo Finance v8 chart API"
RUNTIME_SOURCE     = "frozen local CSV"
PRICE_FIELD        = "adjclose"                   # indicators.adjclose[0].adjclose
START_DATE         = datetime.date(2004, 11, 18)  # GLD ETF inception
CUTOFF_DATE        = datetime.date(2024, 12, 31)  # matches SPY freeze terminus
HOLDOUT_START      = datetime.date(2015, 1, 1)    # final 10 calendar years: 2015–2024
FILL_LIMIT         = 5                            # max consecutive NaN to forward-fill

# Canonical frozen CSV SHA256 — locked at data-freeze commit 4dc56c4.
FROZEN_CSV_SHA256 = "368fe45094eafa277c81accd2c71b2b593ddcf917c29c7b269de088a31fd1b2c"

# Filename pattern. {sha256} is the lowercase hexadecimal SHA256 of the CSV file contents.
FROZEN_CSV_STEM_FORMAT = "gld_yahoo_v8_20041118_20241231_{sha256}.csv"
FROZEN_CSV_FILENAME    = FROZEN_CSV_STEM_FORMAT.format(sha256=FROZEN_CSV_SHA256)

RUN_ANALYSIS = False  # Protocol execution guard — never set True in this module

REQUIRED_COLUMNS = ("date", "adj_close", "log_return", "log_return_sq")

_YF_URL     = "https://query1.finance.yahoo.com/v8/finance/chart/GLD"
_YF_HEADERS = {"User-Agent": "Mozilla/5.0 (harmonic-calendar-research/0.1-gld)"}


# ── Cleaning ──────────────────────────────────────────────────────────────────

def clean_gld_df(df: pd.DataFrame) -> pd.DataFrame:
    """Apply provenance policies and compute log-return outcomes.

    Input:  DataFrame with a DatetimeIndex (or datetime-convertible index) and
            an [adj_close] column. Accepted from load_gld (reads frozen CSV) or
            from synthetic DataFrames in tests.
    Output: DataFrame with columns [date, adj_close, log_return, log_return_sq],
            where date is datetime.date, rows sorted ascending, no duplicates,
            no NaN or ±inf in any column.

    Cleaning steps (applied in order):
      1. Normalise index to date-only (drops intra-day time component).
      2. Filter to provenance window: START_DATE .. CUTOFF_DATE (inclusive).
      3. Drop rows where adj_close is NaN or ≤ 0.
      4. Forward-fill up to FILL_LIMIT consecutive NaN in adj_close (defensive).
      5. Stable sort ascending; keep first occurrence of any duplicate date.
      6. Drop remaining NaN / invalid adj_close rows.
      7. Compute log_return = ln(adj_close_t / adj_close_{t-1}).
      8. Compute log_return_sq = log_return ** 2.
      9. Drop the first row (no prior price to form log return).
     10. Drop rows where any column contains NaN or ±inf.
    """
    work = df.copy()

    # Step 1 – normalise index
    work.index = pd.to_datetime(work.index).normalize()
    work.index.name = "date"

    # Step 2 – provenance date window
    start_ts  = pd.Timestamp(START_DATE)
    cutoff_ts = pd.Timestamp(CUTOFF_DATE)
    work = work.loc[(work.index >= start_ts) & (work.index <= cutoff_ts)]

    # Step 3 – drop invalid adj_close before fill
    work = work[work["adj_close"].notna() & (work["adj_close"] > 0)]

    # Step 4 – forward-fill short NaN gaps (see module docstring for policy)
    work["adj_close"] = work["adj_close"].ffill(limit=FILL_LIMIT)

    # Step 5 – stable sort (preserves first-occurrence order), then deduplicate
    work = work.sort_index(kind="stable")
    work = work[~work.index.duplicated(keep="first")]

    # Step 6 – drop still-missing rows
    work = work[work["adj_close"].notna() & (work["adj_close"] > 0)]

    # Steps 7-8 – log return and squared log return
    prev  = work["adj_close"].shift(1)
    ratio = work["adj_close"] / prev
    work["log_return"] = ratio.apply(
        lambda r: math.log(r) if (pd.notna(r) and math.isfinite(r) and r > 0) else float("nan")
    )
    work["log_return_sq"] = work["log_return"] ** 2

    # Step 9 – drop first row (NaN log_return; no prior price)
    work = work.iloc[1:]

    # Step 10 – drop any remaining NaN / inf in any column
    for col in ("adj_close", "log_return", "log_return_sq"):
        work = work[work[col].notna()]
        work = work[work[col].apply(math.isfinite)]

    work = work.reset_index()
    work["date"] = pd.to_datetime(work["date"]).dt.date
    return work[list(REQUIRED_COLUMNS)].reset_index(drop=True)


# ── Train / Holdout split ─────────────────────────────────────────────────────

def make_train_holdout_split(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split a clean GLD DataFrame into training and holdout partitions.

    Training:  date in [START_DATE, HOLDOUT_START)   — 2004-11-18 to 2014-12-31
    Holdout:   date in [HOLDOUT_START, CUTOFF_DATE]  — 2015-01-01 to 2024-12-31

    Option 1 (design memo): "final 10 calendar years as holdout", matching SPY.
    Pre-registered interpretation caveat: GLD training window is ~10.1 years
    vs ~22 years for SPY; per-anchor PSS estimates are noisier in training.

    Raises ValueError if the DataFrame has no 'date' column, or if either
    partition is empty.
    """
    if "date" not in df.columns:
        raise ValueError("DataFrame must have a 'date' column (output of clean_gld_df)")

    train   = df[df["date"] < HOLDOUT_START].copy().reset_index(drop=True)
    holdout = df[
        (df["date"] >= HOLDOUT_START) & (df["date"] <= CUTOFF_DATE)
    ].copy().reset_index(drop=True)

    if train.empty:
        raise ValueError(
            "Training partition is empty — DataFrame may not span [START_DATE, HOLDOUT_START)"
        )
    if holdout.empty:
        raise ValueError(
            "Holdout partition is empty — DataFrame may not span [HOLDOUT_START, CUTOFF_DATE]"
        )

    return train, holdout


# ── Canonical runtime loader (frozen CSV only) ────────────────────────────────

def _verify_csv_hash_from_filename(csv_path: str) -> None:
    """If csv_path encodes a SHA256 hash in its filename, verify the file contents.

    Filename pattern: ..._<64-hex-chars>.csv
    If no hash is found in the filename, this function is a no-op.
    Raises ValueError if the actual file hash does not match the filename hash.
    """
    m = re.search(r"_([0-9a-f]{64})\.csv$", os.path.basename(csv_path))
    if not m:
        return
    expected = m.group(1)
    with open(csv_path, "rb") as fh:
        actual = hashlib.sha256(fh.read()).hexdigest()
    if actual != expected:
        raise ValueError(
            "SHA256 integrity check failed for {!r}.\n"
            "Expected (from filename): {}\n"
            "Actual   (file contents): {}".format(csv_path, expected, actual)
        )


def load_gld(csv_path: str) -> pd.DataFrame:
    """Canonical runtime loader: read the frozen GLD CSV and return a clean DataFrame.

    Reads from a local frozen CSV file only. Does NOT fetch live data from
    Yahoo Finance or any other network source.

    If the filename encodes a SHA256 hash (pattern: ..._<64-hex>.csv), the hash
    is verified against the file contents before loading. Any modification to
    the frozen CSV will raise ValueError here.

    Args:
        csv_path: Absolute or relative path to the frozen GLD CSV file produced
                  at data-freeze commit 4dc56c4. Expected filename format:
                  gld_yahoo_v8_20041118_20241231_{sha256}.csv

    Returns:
        Clean DataFrame with columns [date, adj_close, log_return, log_return_sq].
        Row count: 5,062 (5,063 raw rows minus the first-row log-return drop).

    Raises:
        FileNotFoundError if csv_path does not exist.
        ValueError if the SHA256 hash in the filename does not match the file.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            "Frozen GLD CSV not found at {!r}.\n"
            "The frozen CSV was produced at data-freeze commit 4dc56c4.\n"
            "Pass the correct path to load_gld().".format(csv_path)
        )
    _verify_csv_hash_from_filename(csv_path)
    raw = pd.read_csv(csv_path, parse_dates=["date"], index_col="date")
    return clean_gld_df(raw)


# ── Acquisition (run ONCE, explicitly, never from analysis code) ──────────────

def _download_yahoo_adjclose() -> pd.DataFrame:
    """Private helper: fetch GLD adjclose from Yahoo Finance v8 API.

    Returns a DataFrame with DatetimeIndex (tz-naive) and [adj_close] column.
    Only called from acquire_gld_from_yahoo(); never called by the canonical loader.
    """
    import requests  # imported here so the canonical loader has no requests dependency

    period1 = int(datetime.datetime(
        START_DATE.year, START_DATE.month, START_DATE.day
    ).timestamp()) - 86400
    period2 = int(datetime.datetime(
        CUTOFF_DATE.year, CUTOFF_DATE.month, CUTOFF_DATE.day
    ).timestamp()) + 2 * 86400

    resp = requests.get(
        _YF_URL,
        params={
            "period1":        period1,
            "period2":        period2,
            "interval":       "1d",
            "includePrePost": "false",
            "events":         "div,splits",
        },
        headers=_YF_HEADERS,
        timeout=30,
    )
    resp.raise_for_status()

    try:
        result     = resp.json()["chart"]["result"][0]
        timestamps = result["timestamp"]
        adj_close  = result["indicators"]["adjclose"][0]["adjclose"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(
            "Unexpected Yahoo Finance response structure: {}".format(exc)
        ) from exc

    index = pd.to_datetime(timestamps, unit="s", utc=True).normalize().tz_localize(None)
    df = pd.DataFrame({"adj_close": adj_close}, index=index)
    df.index.name = "date"
    return df


def acquire_gld_from_yahoo(output_dir: str = "data/raw") -> str:
    """ACQUISITION FUNCTION — RUN ONCE / NOT the canonical loader.

    This function fetches live data from Yahoo Finance and writes a frozen CSV
    with a SHA256 hash embedded in the filename. It is NOT the canonical runtime
    loader. The canonical loader (load_gld) reads from the local frozen CSV.
    Do not call this function from analysis code.

    The frozen GLD CSV was produced at data-freeze commit 4dc56c4. This function
    is preserved here as a historical audit reference and utility for re-acquisition
    if ever needed. It must not be called from the protocol runner or any analysis path.

    Steps performed:
      1. Fetch GLD daily adjusted close from Yahoo Finance v8 chart API.
      2. Filter to the provenance window [START_DATE, CUTOFF_DATE].
      3. Write raw adjusted-close data to CSV (no log-return computation here;
         clean_gld_df handles that at load time).
      4. Compute SHA256 of the CSV file contents.
      5. Rename the file to embed the hash: FROZEN_CSV_STEM_FORMAT.format(sha256=...).
      6. Print the path and hash for the audit trail.

    Args:
        output_dir: Directory where the frozen CSV will be written.
                    Created if it does not exist.

    Returns:
        Absolute path to the frozen CSV file.

    Raises:
        FileExistsError if a frozen CSV with the same hash already exists.
        requests.HTTPError on non-200 HTTP responses.
        ValueError if the Yahoo Finance response is malformed.
    """
    import io

    raw = _download_yahoo_adjclose()

    # Filter to provenance window before writing
    raw = raw.loc[
        (raw.index >= pd.Timestamp(START_DATE)) &
        (raw.index <= pd.Timestamp(CUTOFF_DATE))
    ]
    raw = raw[raw["adj_close"].notna() & (raw["adj_close"] > 0)]
    raw = raw.sort_index(kind="stable")
    raw = raw[~raw.index.duplicated(keep="first")]

    # Serialise to bytes so SHA256 is deterministic
    buf = io.StringIO()
    raw.to_csv(buf, index=True, date_format="%Y-%m-%d", float_format="%.8f")
    csv_bytes = buf.getvalue().encode("utf-8")
    sha256_hash = hashlib.sha256(csv_bytes).hexdigest()

    os.makedirs(output_dir, exist_ok=True)
    filename = FROZEN_CSV_STEM_FORMAT.format(sha256=sha256_hash)
    csv_path = os.path.join(output_dir, filename)

    if os.path.exists(csv_path):
        raise FileExistsError(
            "Frozen CSV already exists at {!r}. "
            "Delete it explicitly if you intend to re-acquire.".format(csv_path)
        )

    with open(csv_path, "wb") as fh:
        fh.write(csv_bytes)

    print("GLD acquisition complete.")
    print("  Path:   {}".format(os.path.abspath(csv_path)))
    print("  SHA256: {}".format(sha256_hash))
    print("  Rows:   {}".format(len(raw)))
    if len(raw):
        print("  Range:  {} to {}".format(raw.index[0].date(), raw.index[-1].date()))

    return os.path.abspath(csv_path)
