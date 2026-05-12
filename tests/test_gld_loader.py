"""Unit tests for src/gld_loader.py.

All tests use synthetic DataFrames except the canonical-file group, which
reads the frozen GLD CSV from data/raw/ to verify file existence, SHA256
integrity, row count, and loaded date range.

Verifications locked here:
  - required columns and their types
  - dates sorted ascending, no duplicates, no NaN / inf after cleaning
  - date range: all dates within [START_DATE, CUTOFF_DATE]
  - holdout starts after training ends (no temporal overlap)
  - holdout covers exactly the final 10 calendar years (2015–2024)
  - canonical loader reads frozen local CSV only (no live network calls)
  - acquisition function is separate and not called by canonical loader
  - gld_loader does not compute PSS or run the protocol
  - RUN_ANALYSIS = False in gld_loader
  - canonical frozen GLD CSV exists, SHA256 matches, loaded row count = 5,062
  - loaded first date = 2004-11-19 (2004-11-18 raw row dropped for log-return)
  - loaded last date = 2024-12-31
"""

import hashlib
import math
import datetime
import inspect
import os
import random
import shutil
import pytest
import pandas as pd

import gld_loader
from gld_loader import (
    clean_gld_df,
    load_gld,
    acquire_gld_from_yahoo,
    make_train_holdout_split,
    START_DATE,
    CUTOFF_DATE,
    HOLDOUT_START,
    FILL_LIMIT,
    TICKER,
    PRICE_FIELD,
    REQUIRED_COLUMNS,
    FROZEN_CSV_STEM_FORMAT,
    FROZEN_CSV_SHA256,
    FROZEN_CSV_FILENAME,
    ACQUISITION_SOURCE,
    RUNTIME_SOURCE,
    RUN_ANALYSIS as GLD_RUN_ANALYSIS,
)

_REPO_ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_FROZEN_GLD_CSV = os.path.join(_REPO_ROOT, "data", "raw", FROZEN_CSV_FILENAME)

GLD_EXPECTED_RAW_ROWS    = 5_063
GLD_EXPECTED_LOADED_ROWS = 5_062   # 5,063 raw rows minus first-row log-return drop
GLD_EXPECTED_FIRST_DATE  = datetime.date(2004, 11, 19)  # row 2 of raw; row 1 is dropped
GLD_EXPECTED_LAST_DATE   = datetime.date(2024, 12, 31)


# ── Synthetic data helpers ────────────────────────────────────────────────────

def _make_raw_df(start: str = "2004-11-18", end: str = "2024-12-31") -> pd.DataFrame:
    """Build a minimal raw DataFrame matching the frozen-CSV input schema for clean_gld_df."""
    dates = pd.date_range(start=start, end=end, freq="B")  # business days
    rng = random.Random(42)
    prices = [45.0]
    for _ in range(len(dates) - 1):
        prices.append(max(1.0, prices[-1] * (1.0 + rng.gauss(0.0003, 0.008))))
    df = pd.DataFrame({"adj_close": prices}, index=dates)
    df.index.name = "date"
    return df


def _make_clean_df(start: str = "2004-11-18", end: str = "2024-12-31") -> pd.DataFrame:
    """Return a clean DataFrame (output of clean_gld_df) for use in tests."""
    return clean_gld_df(_make_raw_df(start=start, end=end))


# ── Provenance constants ──────────────────────────────────────────────────────

def test_ticker_is_gld():
    assert TICKER == "GLD"


def test_price_field_is_adjclose():
    assert PRICE_FIELD == "adjclose"


def test_start_date_is_gld_inception():
    assert START_DATE == datetime.date(2004, 11, 18)


def test_cutoff_date_is_end_of_2024():
    assert CUTOFF_DATE == datetime.date(2024, 12, 31)


def test_holdout_start_is_2015_01_01():
    assert HOLDOUT_START == datetime.date(2015, 1, 1)


def test_holdout_spans_exactly_10_calendar_years():
    years = CUTOFF_DATE.year - HOLDOUT_START.year + 1
    assert years == 10, "Holdout must cover exactly 10 calendar years, got {}".format(years)


def test_fill_limit_is_positive_integer():
    assert isinstance(FILL_LIMIT, int) and FILL_LIMIT > 0


def test_frozen_csv_sha256_is_64_hex_chars():
    assert len(FROZEN_CSV_SHA256) == 64
    assert all(c in "0123456789abcdef" for c in FROZEN_CSV_SHA256)


def test_frozen_csv_filename_embeds_sha256():
    assert FROZEN_CSV_SHA256 in FROZEN_CSV_FILENAME


# ── Schema: required columns ──────────────────────────────────────────────────

def test_clean_df_has_required_columns():
    df = _make_clean_df()
    for col in REQUIRED_COLUMNS:
        assert col in df.columns, "Missing column: {}".format(col)


def test_clean_df_date_column_is_python_date():
    df = _make_clean_df()
    for val in df["date"].head(5):
        assert isinstance(val, datetime.date), "date must be datetime.date, got {}".format(type(val))


def test_clean_df_numeric_columns_are_float():
    df = _make_clean_df()
    for col in ("adj_close", "log_return", "log_return_sq"):
        assert pd.api.types.is_float_dtype(df[col]), "{} must be float dtype".format(col)


# ── Sorted ascending dates ────────────────────────────────────────────────────

def test_dates_sorted_ascending():
    df = _make_clean_df()
    dates = list(df["date"])
    assert dates == sorted(dates), "Dates are not sorted ascending"


# ── No duplicate dates ────────────────────────────────────────────────────────

def test_no_duplicate_dates():
    df = _make_clean_df()
    assert df["date"].nunique() == len(df), "Duplicate dates found"


def test_duplicate_dates_in_raw_are_deduped():
    raw = _make_raw_df()
    mid_idx = raw.index[100]  # well inside the range, not the first row
    original_price = raw.at[mid_idx, "adj_close"]
    extra_row = pd.DataFrame({"adj_close": [999999.0]}, index=[mid_idx])
    raw_with_dup = pd.concat([raw, extra_row])  # original row comes first
    clean = clean_gld_df(raw_with_dup)
    assert clean["date"].nunique() == len(clean), "Duplicate dates remain after cleaning"
    kept_price = clean.loc[clean["date"] == mid_idx.date(), "adj_close"].values[0]
    assert kept_price != 999999.0, "Duplicate resolution should keep first occurrence"
    assert abs(kept_price - original_price) < 0.01


# ── No NaN or ±inf after cleaning ─────────────────────────────────────────────

def test_no_nan_in_any_column():
    df = _make_clean_df()
    for col in ("adj_close", "log_return", "log_return_sq"):
        assert not df[col].isna().any(), "NaN found in column {}".format(col)


def test_no_inf_in_log_return():
    df = _make_clean_df()
    assert df["log_return"].apply(math.isfinite).all(), "±inf found in log_return"


def test_no_inf_in_log_return_sq():
    df = _make_clean_df()
    assert df["log_return_sq"].apply(math.isfinite).all(), "±inf found in log_return_sq"


def test_nan_adj_close_in_raw_is_dropped():
    raw = _make_raw_df()
    raw.iloc[5, raw.columns.get_loc("adj_close")] = float("nan")
    clean = clean_gld_df(raw)
    assert not clean["adj_close"].isna().any()


def test_non_positive_adj_close_in_raw_is_dropped():
    raw = _make_raw_df()
    raw.iloc[10, raw.columns.get_loc("adj_close")] = -5.0
    clean = clean_gld_df(raw)
    assert (clean["adj_close"] > 0).all()


def test_infinite_adj_close_in_raw_does_not_survive_cleaning():
    raw = _make_raw_df()
    raw.iloc[20, raw.columns.get_loc("adj_close")] = float("inf")
    clean = clean_gld_df(raw)
    assert clean["adj_close"].apply(math.isfinite).all()
    assert clean["log_return"].apply(math.isfinite).all()


# ── log_return_sq == log_return^2 ─────────────────────────────────────────────

def test_log_return_sq_equals_log_return_squared():
    df = _make_clean_df()
    expected = df["log_return"] ** 2
    pd.testing.assert_series_equal(df["log_return_sq"], expected, check_names=False)


# ── Date range ────────────────────────────────────────────────────────────────

def test_all_dates_within_provenance_window():
    df = _make_clean_df()
    assert (df["date"] >= START_DATE).all(), "Dates before START_DATE present"
    assert (df["date"] <= CUTOFF_DATE).all(), "Dates after CUTOFF_DATE present"


def test_dates_beyond_cutoff_are_excluded():
    raw = _make_raw_df(end="2025-06-30")
    clean = clean_gld_df(raw)
    assert (clean["date"] <= CUTOFF_DATE).all(), "Post-cutoff dates not excluded"


def test_dates_before_start_are_excluded():
    raw = _make_raw_df(start="2003-01-02")
    clean = clean_gld_df(raw)
    assert (clean["date"] >= START_DATE).all(), "Pre-start dates not excluded"


# ── Train / holdout split ─────────────────────────────────────────────────────

def test_split_produces_non_empty_partitions():
    df = _make_clean_df()
    train, holdout = make_train_holdout_split(df)
    assert len(train) > 0
    assert len(holdout) > 0


def test_holdout_starts_after_training_ends():
    df = _make_clean_df()
    train, holdout = make_train_holdout_split(df)
    assert max(train["date"]) < min(holdout["date"]), (
        "Temporal overlap: max train date {} >= min holdout date {}".format(
            max(train["date"]), min(holdout["date"])
        )
    )


def test_no_temporal_overlap_between_split_partitions():
    df = _make_clean_df()
    train, holdout = make_train_holdout_split(df)
    assert set(train["date"]).isdisjoint(set(holdout["date"])), "Train and holdout share dates"


def test_training_dates_all_before_holdout_start():
    df = _make_clean_df()
    train, _ = make_train_holdout_split(df)
    assert (train["date"] < HOLDOUT_START).all()


def test_holdout_dates_all_at_or_after_holdout_start():
    df = _make_clean_df()
    _, holdout = make_train_holdout_split(df)
    assert (holdout["date"] >= HOLDOUT_START).all()


def test_holdout_dates_all_at_or_before_cutoff():
    df = _make_clean_df()
    _, holdout = make_train_holdout_split(df)
    assert (holdout["date"] <= CUTOFF_DATE).all()


def test_final_10_calendar_years_are_in_holdout():
    df = _make_clean_df()
    _, holdout = make_train_holdout_split(df)
    holdout_years = sorted(set(d.year for d in holdout["date"]))
    for year in range(2015, 2025):
        assert year in holdout_years, "Year {} missing from holdout".format(year)


def test_split_requires_date_column():
    df_bad = pd.DataFrame({"adj_close": [1.0, 2.0]})
    with pytest.raises(ValueError, match="'date' column"):
        make_train_holdout_split(df_bad)


def test_split_raises_on_empty_train_partition():
    # DataFrame entirely within holdout window: no training rows.
    df = _make_clean_df(start="2020-01-02", end="2024-12-31")
    with pytest.raises(ValueError, match="Training partition is empty"):
        make_train_holdout_split(df)


def test_split_raises_on_empty_holdout_partition():
    # DataFrame entirely within training window: no holdout rows.
    df = _make_clean_df(start="2004-11-18", end="2013-12-31")
    with pytest.raises(ValueError, match="Holdout partition is empty"):
        make_train_holdout_split(df)


# ── Protocol guard: no PSS / no analysis ─────────────────────────────────────

def test_gld_loader_does_not_compute_pss():
    src = inspect.getsource(gld_loader)
    for symbol in ("pss_in_sample", "pss_out_of_sample", "SS_between", "SS_residual"):
        assert symbol not in src, (
            "gld_loader.py must not reference '{}' (no PSS computation)".format(symbol)
        )


def test_gld_loader_does_not_assign_phases():
    src = inspect.getsource(gld_loader)
    for symbol in ("assign_march20_phase", "assign_january_anchored_phase",
                   "assign_random_anchor_phase", "PHASE_CYCLE"):
        assert symbol not in src, (
            "gld_loader.py must not reference '{}' (phase assignment is separate)".format(symbol)
        )


def test_gld_loader_run_analysis_is_false():
    assert GLD_RUN_ANALYSIS is False, "RUN_ANALYSIS in gld_loader must be False"


# ── Frozen CSV design: constants ──────────────────────────────────────────────

def test_frozen_csv_stem_format_contains_sha256_placeholder():
    assert "{sha256}" in FROZEN_CSV_STEM_FORMAT


def test_frozen_csv_stem_format_ends_with_csv():
    filled = FROZEN_CSV_STEM_FORMAT.format(sha256="a" * 64)
    assert filled.endswith(".csv")


def test_acquisition_source_constant():
    assert "Yahoo" in ACQUISITION_SOURCE


def test_runtime_source_constant():
    assert "frozen" in RUNTIME_SOURCE.lower() or "local" in RUNTIME_SOURCE.lower()


# ── Frozen CSV design: canonical loader ──────────────────────────────────────

def test_load_gld_raises_file_not_found_for_missing_csv():
    with pytest.raises(FileNotFoundError):
        load_gld("/nonexistent/path/gld_yahoo_v8_20041118_20241231_{}.csv".format("a" * 64))


def test_load_gld_source_has_no_live_requests():
    src = inspect.getsource(load_gld)
    assert "requests" not in src, (
        "load_gld must not contain 'requests' — canonical loader makes no live network calls"
    )
    assert "_download_yahoo_adjclose" not in src, (
        "load_gld must not call _download_yahoo_adjclose — acquisition is separate"
    )


def test_load_gld_reads_from_csv_path_argument():
    src = inspect.getsource(load_gld)
    assert "csv_path" in src, "load_gld must accept and use a csv_path argument"


# ── Frozen CSV design: acquisition function ───────────────────────────────────

def test_acquisition_function_docstring_has_run_once_label():
    doc = acquire_gld_from_yahoo.__doc__ or ""
    assert "ACQUISITION FUNCTION" in doc
    assert "RUN ONCE" in doc


def test_acquisition_function_docstring_not_canonical_loader():
    doc = acquire_gld_from_yahoo.__doc__ or ""
    assert "NOT" in doc


def test_acquisition_function_not_called_by_load_gld():
    src = inspect.getsource(load_gld)
    assert "_download_yahoo_adjclose" not in src


def test_acquisition_function_imports_requests_locally():
    src = inspect.getsource(gld_loader._download_yahoo_adjclose)
    assert "import requests" in src, (
        "_download_yahoo_adjclose must import requests locally (not at module level)"
    )


def test_module_level_imports_do_not_include_requests():
    src = inspect.getsource(gld_loader)
    for line in src.splitlines():
        stripped = line.strip()
        if stripped == "import requests":
            assert line.startswith(" ") or line.startswith("\t"), (
                "'import requests' must be inside a function, not at module level"
            )


# ── Canonical frozen file checks ──────────────────────────────────────────────

def test_canonical_gld_file_exists():
    assert os.path.exists(_FROZEN_GLD_CSV), (
        "Frozen GLD CSV not found at {!r}. "
        "Expected after data-freeze commit 4dc56c4.".format(_FROZEN_GLD_CSV)
    )


def test_canonical_gld_sha256_matches():
    with open(_FROZEN_GLD_CSV, "rb") as fh:
        actual = hashlib.sha256(fh.read()).hexdigest()
    assert actual == FROZEN_CSV_SHA256, (
        "SHA256 mismatch.\n  Expected: {}\n  Actual:   {}".format(FROZEN_CSV_SHA256, actual)
    )


def test_load_gld_returns_expected_row_count():
    df = load_gld(_FROZEN_GLD_CSV)
    assert len(df) == GLD_EXPECTED_LOADED_ROWS, (
        "Expected {} loaded rows ({} raw minus first-row log-return drop), got {}".format(
            GLD_EXPECTED_LOADED_ROWS, GLD_EXPECTED_RAW_ROWS, len(df)
        )
    )


def test_load_gld_first_date_is_second_raw_date():
    df = load_gld(_FROZEN_GLD_CSV)
    assert df["date"].iloc[0] == GLD_EXPECTED_FIRST_DATE, (
        "Expected loaded first date {} (raw row 2004-11-18 dropped for log-return), got {}".format(
            GLD_EXPECTED_FIRST_DATE, df["date"].iloc[0]
        )
    )


def test_load_gld_last_date_is_2024_12_31():
    df = load_gld(_FROZEN_GLD_CSV)
    assert df["date"].iloc[-1] == GLD_EXPECTED_LAST_DATE, (
        "Expected loaded last date {}, got {}".format(
            GLD_EXPECTED_LAST_DATE, df["date"].iloc[-1]
        )
    )


def test_load_gld_adj_close_all_positive_and_finite():
    df = load_gld(_FROZEN_GLD_CSV)
    assert (df["adj_close"] > 0).all(), "Non-positive adj_close found"
    assert df["adj_close"].apply(math.isfinite).all(), "Infinite adj_close found"


def test_load_gld_log_return_all_finite():
    df = load_gld(_FROZEN_GLD_CSV)
    assert df["log_return"].apply(math.isfinite).all(), "Non-finite log_return found"


def test_load_gld_no_duplicate_dates():
    df = load_gld(_FROZEN_GLD_CSV)
    assert df["date"].nunique() == len(df), "Duplicate dates found in loaded GLD data"


def test_load_gld_dates_sorted_ascending():
    df = load_gld(_FROZEN_GLD_CSV)
    dates = list(df["date"])
    assert dates == sorted(dates), "Loaded GLD dates are not sorted ascending"


def test_load_gld_wrong_hash_raises_value_error(tmp_path):
    bad_hash = "b" * 64
    bad_name = "gld_yahoo_v8_20041118_20241231_{}.csv".format(bad_hash)
    bad_path = str(tmp_path / bad_name)
    shutil.copy2(_FROZEN_GLD_CSV, bad_path)
    with pytest.raises(ValueError, match="SHA256 integrity check failed"):
        load_gld(bad_path)
