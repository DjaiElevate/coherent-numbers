"""Unit tests for src/spy_loader.py.

All tests use synthetic DataFrames — no network calls, no SPY data downloaded.
Tests marked with @pytest.mark.integration require a live internet connection
and are skipped by default.

Verifications locked here:
  - required columns and their types
  - dates sorted ascending, no duplicates, no NaN / inf after cleaning
  - date range: all dates within [START_DATE, CUTOFF_DATE]
  - holdout starts after training ends (no temporal overlap)
  - holdout covers exactly the final 10 calendar years
  - canonical loader reads frozen local CSV only (no live network calls)
  - acquisition function is separate and not called by canonical loader
  - spy_loader does not compute PSS or run the protocol
  - RUN_ANALYSIS = False in harmonic_calendar and spy_loader
"""

import math
import datetime
import inspect
import random
import pytest
import pandas as pd

import spy_loader
from spy_loader import (
    clean_spy_df,
    load_spy,
    acquire_spy_from_yahoo,
    make_train_holdout_split,
    START_DATE,
    CUTOFF_DATE,
    HOLDOUT_START,
    FILL_LIMIT,
    TICKER,
    PRICE_FIELD,
    REQUIRED_COLUMNS,
    FROZEN_CSV_STEM_FORMAT,
    ACQUISITION_SOURCE,
    RUNTIME_SOURCE,
    RUN_ANALYSIS as SPY_RUN_ANALYSIS,
)
from harmonic_calendar import RUN_ANALYSIS as HC_RUN_ANALYSIS


# ── Synthetic data helpers ────────────────────────────────────────────────────

def _make_raw_df(start: str = "2005-01-03", end: str = "2024-12-31") -> pd.DataFrame:
    """Build a minimal raw DataFrame matching the frozen-CSV input schema for clean_spy_df."""
    dates = pd.date_range(start=start, end=end, freq="B")  # business days
    rng = random.Random(42)
    prices = [200.0]
    for _ in range(len(dates) - 1):
        prices.append(max(1.0, prices[-1] * (1.0 + rng.gauss(0.0003, 0.008))))
    df = pd.DataFrame({"adj_close": prices}, index=dates)
    df.index.name = "date"
    return df


def _make_clean_df(start: str = "2005-01-03", end: str = "2024-12-31") -> pd.DataFrame:
    """Return a clean DataFrame (output of clean_spy_df) for use in tests."""
    return clean_spy_df(_make_raw_df(start=start, end=end))


# ── Provenance constants ──────────────────────────────────────────────────────

def test_ticker_is_spy():
    assert TICKER == "SPY"


def test_price_field_is_adjclose():
    assert PRICE_FIELD == "adjclose"


def test_start_date_is_spy_first_trading_day():
    assert START_DATE == datetime.date(1993, 1, 29)


def test_cutoff_date_is_end_of_2024():
    assert CUTOFF_DATE == datetime.date(2024, 12, 31)


def test_holdout_start_is_2015_01_01():
    assert HOLDOUT_START == datetime.date(2015, 1, 1)


def test_holdout_spans_exactly_10_calendar_years():
    # Holdout covers years [HOLDOUT_START.year, CUTOFF_DATE.year] inclusive.
    years = CUTOFF_DATE.year - HOLDOUT_START.year + 1
    assert years == 10, "Holdout must cover exactly 10 calendar years, got {}".format(years)


def test_fill_limit_is_positive_integer():
    assert isinstance(FILL_LIMIT, int) and FILL_LIMIT > 0


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
    # Inject a duplicate at a middle date (not the first row, which clean_spy_df
    # drops because it has no prior price for log_return computation).
    # Do NOT pre-sort the concat: clean_spy_df applies a stable sort internally,
    # so the original row (appearing first in the concat) is preserved.
    raw = _make_raw_df()
    mid_idx = raw.index[100]  # well inside the range, not the first row
    original_price = raw.at[mid_idx, "adj_close"]
    extra_row = pd.DataFrame({"adj_close": [999999.0]}, index=[mid_idx])
    raw_with_dup = pd.concat([raw, extra_row])  # original row comes first
    clean = clean_spy_df(raw_with_dup)
    assert clean["date"].nunique() == len(clean), "Duplicate dates remain after cleaning"
    # First occurrence (original price) should be kept, not the 999999.0 duplicate.
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
    clean = clean_spy_df(raw)
    assert not clean["adj_close"].isna().any()


def test_non_positive_adj_close_in_raw_is_dropped():
    raw = _make_raw_df()
    raw.iloc[10, raw.columns.get_loc("adj_close")] = -5.0
    clean = clean_spy_df(raw)
    assert (clean["adj_close"] > 0).all()


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
    # Inject rows past CUTOFF_DATE; they must not appear in output.
    raw = _make_raw_df(end="2025-06-30")
    clean = clean_spy_df(raw)
    assert (clean["date"] <= CUTOFF_DATE).all(), "Post-cutoff dates not excluded"


def test_dates_before_start_are_excluded():
    # Inject rows before START_DATE.
    raw = _make_raw_df(start="1990-01-02")
    clean = clean_spy_df(raw)
    assert (clean["date"] >= START_DATE).all(), "Pre-start dates not excluded"


# ── Train / holdout split ─────────────────────────────────────────────────────

def test_split_produces_non_empty_partitions():
    df = _make_clean_df(start="2005-01-03", end="2024-12-31")
    train, holdout = make_train_holdout_split(df)
    assert len(train) > 0
    assert len(holdout) > 0


def test_holdout_starts_after_training_ends():
    df = _make_clean_df(start="2005-01-03", end="2024-12-31")
    train, holdout = make_train_holdout_split(df)
    assert max(train["date"]) < min(holdout["date"]), (
        "Temporal overlap: max train date {} >= min holdout date {}".format(
            max(train["date"]), min(holdout["date"])
        )
    )


def test_no_temporal_overlap_between_split_partitions():
    df = _make_clean_df(start="2005-01-03", end="2024-12-31")
    train, holdout = make_train_holdout_split(df)
    train_dates   = set(train["date"])
    holdout_dates = set(holdout["date"])
    assert train_dates.isdisjoint(holdout_dates), "Train and holdout share dates"


def test_training_dates_all_before_holdout_start():
    df = _make_clean_df(start="2005-01-03", end="2024-12-31")
    train, _ = make_train_holdout_split(df)
    assert (train["date"] < HOLDOUT_START).all()


def test_holdout_dates_all_at_or_after_holdout_start():
    df = _make_clean_df(start="2005-01-03", end="2024-12-31")
    _, holdout = make_train_holdout_split(df)
    assert (holdout["date"] >= HOLDOUT_START).all()


def test_holdout_dates_all_at_or_before_cutoff():
    df = _make_clean_df(start="2005-01-03", end="2024-12-31")
    _, holdout = make_train_holdout_split(df)
    assert (holdout["date"] <= CUTOFF_DATE).all()


def test_final_10_calendar_years_are_in_holdout():
    df = _make_clean_df(start="2005-01-03", end="2024-12-31")
    _, holdout = make_train_holdout_split(df)
    holdout_years = sorted(set(d.year for d in holdout["date"]))
    # Must include at minimum all years from 2015 through 2024.
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
    df = _make_clean_df(start="2005-01-03", end="2013-12-31")
    with pytest.raises(ValueError, match="Holdout partition is empty"):
        make_train_holdout_split(df)


# ── Protocol guard: no PSS / no analysis ─────────────────────────────────────

def test_spy_loader_does_not_compute_pss():
    import spy_loader
    src = inspect.getsource(spy_loader)
    for symbol in ("pss_in_sample", "pss_out_of_sample", "SS_between", "SS_residual"):
        assert symbol not in src, (
            "spy_loader.py must not reference '{}' (no PSS computation)".format(symbol)
        )


def test_spy_loader_does_not_assign_phases():
    import spy_loader
    src = inspect.getsource(spy_loader)
    for symbol in ("assign_march20_phase", "assign_january_anchored_phase",
                   "assign_random_anchor_phase", "PHASE_CYCLE"):
        assert symbol not in src, (
            "spy_loader.py must not reference '{}' (phase assignment is separate)".format(symbol)
        )


def test_spy_loader_run_analysis_is_false():
    assert SPY_RUN_ANALYSIS is False, "RUN_ANALYSIS in spy_loader must be False"


def test_harmonic_calendar_run_analysis_is_false():
    assert HC_RUN_ANALYSIS is False, "RUN_ANALYSIS in harmonic_calendar must be False"


# ── Frozen CSV design: constants ──────────────────────────────────────────────

def test_frozen_csv_stem_format_contains_sha256_placeholder():
    assert "{sha256}" in FROZEN_CSV_STEM_FORMAT, (
        "FROZEN_CSV_STEM_FORMAT must contain '{sha256}' placeholder"
    )


def test_frozen_csv_stem_format_ends_with_csv():
    filled = FROZEN_CSV_STEM_FORMAT.format(sha256="a" * 64)
    assert filled.endswith(".csv"), "FROZEN_CSV_STEM_FORMAT must produce a .csv filename"


def test_acquisition_source_constant():
    assert "Yahoo" in ACQUISITION_SOURCE, (
        "ACQUISITION_SOURCE must reference Yahoo Finance"
    )


def test_runtime_source_constant():
    assert "frozen" in RUNTIME_SOURCE.lower() or "local" in RUNTIME_SOURCE.lower(), (
        "RUNTIME_SOURCE must reference frozen local CSV"
    )


# ── Frozen CSV design: canonical loader ──────────────────────────────────────

def test_load_spy_raises_file_not_found_for_missing_csv():
    with pytest.raises(FileNotFoundError):
        load_spy("/nonexistent/path/spy_yahoo_v8_19930129_20241231_{}.csv".format("a" * 64))


def test_load_spy_source_has_no_live_requests():
    src = inspect.getsource(load_spy)
    assert "requests" not in src, (
        "load_spy must not contain 'requests' — canonical loader makes no live network calls"
    )
    assert "_download_yahoo_adjclose" not in src, (
        "load_spy must not call _download_yahoo_adjclose — acquisition is separate"
    )


def test_load_spy_reads_from_csv_path_argument():
    src = inspect.getsource(load_spy)
    assert "csv_path" in src, "load_spy must accept and use a csv_path argument"


# ── Frozen CSV design: acquisition function ───────────────────────────────────

def test_acquisition_function_docstring_has_run_once_label():
    doc = acquire_spy_from_yahoo.__doc__ or ""
    assert "ACQUISITION FUNCTION" in doc, (
        "acquire_spy_from_yahoo docstring must contain 'ACQUISITION FUNCTION'"
    )
    assert "RUN ONCE" in doc, (
        "acquire_spy_from_yahoo docstring must contain 'RUN ONCE'"
    )


def test_acquisition_function_docstring_not_canonical_loader():
    doc = acquire_spy_from_yahoo.__doc__ or ""
    assert "NOT the canonical runtime loader" in doc or "NOT" in doc, (
        "acquire_spy_from_yahoo docstring must clarify it is NOT the canonical loader"
    )


def test_acquisition_function_not_called_by_load_spy():
    # The canonical loader must not invoke the download helper.
    # (load_spy docstring may mention acquire_spy_from_yahoo; we check for
    # the private download helper that would actually trigger a network call.)
    src = inspect.getsource(load_spy)
    assert "_download_yahoo_adjclose" not in src, (
        "load_spy must not call _download_yahoo_adjclose — no live network calls in canonical loader"
    )


def test_acquisition_function_imports_requests_locally():
    # The requests import lives in _download_yahoo_adjclose (the private helper
    # called by acquire_spy_from_yahoo) so the canonical loader has no network dependency.
    src = inspect.getsource(spy_loader._download_yahoo_adjclose)
    assert "import requests" in src, (
        "_download_yahoo_adjclose must import requests locally (not at module level)"
    )


def test_module_level_imports_do_not_include_requests():
    src = inspect.getsource(spy_loader)
    # 'import requests' must only appear inside a function, not at module top level.
    for line in src.splitlines():
        stripped = line.strip()
        if stripped == "import requests":
            # Must be indented (inside a function), not a top-level import.
            assert line.startswith(" ") or line.startswith("\t"), (
                "'import requests' must be inside a function, not at module level"
            )
