"""Lane 2 GDELT1 Step 2 daily-feature generator (offline, GDELT-only).

Implements the locked design in
`docs/lane2_gdelt1_step2_implementation_design_memo_v0.1.md`
(SHA-256 `fea70ede10982a140d57b9534a9ce08eb7bb946c4dc6ba1e410b45777c8ed164`).

Scope and firewalls (per memo):
  - Reads the canonical merged daily-count substrate only.
  - Produces an in-memory per-civil-date feature table over GDELT substrate fields.
  - NO market data, NO instrument construction, NO outcome variable, NO trading
    signal, NO GDELT fetch, NO BigQuery, NO row export.
  - NO post-2022-12-31 data.
  - Default behavior is dry-run / in-memory only. Writing the three Step 2 output
    artifacts requires a dedicated `--write-step2-output` CLI flag and a
    separate execution-authorization prompt; this module does not invoke that
    path on import or in conformance-gate mode.
  - Does NOT reuse `FULL_BUILD_AUTHORIZED` (live-fetch guard; Step 2 is offline)
    and does NOT reuse `--write-merge-output` (merge-writer scoped).

The module is deterministic: given the same pinned merged substrate input, the
in-memory feature table is byte-identical across runs and the rendered
`step2_summary.md` / `step2_metadata.json` are identical across runs.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import statistics
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

STEP2_IMPLEMENTATION_VERSION = "v0.1"

# ----------------------------------------------------------------------------
# Pins (§2 of the implementation-design memo)
# ----------------------------------------------------------------------------

CANONICAL_MERGED_DIR_BASENAME = "merged_20260529T175416Z"

INPUT_ARTIFACT_SHA256: Mapping[str, str] = {
    "build_daily_counts.csv":
        "84b6ac9f47888fea4bd5c9d448058db0e5c568e3aa194a0fc7d4d5c95704045e",
    "build_metadata.json":
        "31ad8085d9df839f833d6af83cb4fdb24ad47c3ecef0bd44b4d730de682a08cf",
    "build_summary.md":
        "7677bbaf3d84923209a8b0be64dd9d3f64ffe752ac56f4eb5ad65169bae86e97",
}

EXPECTED_BUILD_MANIFEST_DIGEST = (
    "4b312183d9bb126169fc82c5b76008359778df18ee803527c567f7ade3a89650"
)

DESIGN_MEMO_SHA256 = (
    "fea70ede10982a140d57b9534a9ce08eb7bb946c4dc6ba1e410b45777c8ed164"
)

# ----------------------------------------------------------------------------
# Substrate constants (§§4, 8, 9, 10, 11)
# ----------------------------------------------------------------------------

DOMAIN_START = "2013-04-01"
DOMAIN_END = "2022-12-31"
EXPECTED_ROW_COUNT = 3562

DOCUMENTED_EXCEPTION_DATE = "2022-11-10"
DOCUMENTED_EXCEPTION_LABEL = (
    "UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY"
)
DOCUMENTED_EXCEPTION_TOTAL = 1267
DOCUMENTED_EXCEPTION_NEIGHBOR_PARTS = (91, 849, 327)
DOCUMENTED_EXCEPTION_NEIGHBOR_COLUMNS = (
    "rows_from_offset_minus_1",
    "rows_from_offset_minus_7",
    "rows_from_offset_minus_30",
)

KNOWN_SUBSTRATE_GAPS: Tuple[str, ...] = (
    "2014-01-23",
    "2014-01-24",
    "2014-01-25",
    "2014-03-19",
)

EXPECTED_INPUT_COLUMNS: Tuple[str, ...] = (
    "civil_date",
    "total_row_count",
    "rows_from_offset_0",
    "rows_from_offset_minus_1",
    "rows_from_offset_minus_7",
    "rows_from_offset_minus_30",
    "rows_from_offset_minus_365",
    "rows_from_offset_minus_3650",
    "rows_from_offset_plus_1",
    "t0_file_status",
    "expected_contributing_files_count",
    "available_contributing_files_count",
    "coverage_quality_flag",
    "coverage_completeness",
    "represented_only",
    "documented_exception_label",
)

OFFSET_COLUMNS: Tuple[str, ...] = (
    "rows_from_offset_0",
    "rows_from_offset_minus_1",
    "rows_from_offset_minus_7",
    "rows_from_offset_minus_30",
    "rows_from_offset_minus_365",
    "rows_from_offset_minus_3650",
    "rows_from_offset_plus_1",
)

NEIGHBOR_OFFSET_COLUMNS: Tuple[str, ...] = (
    "rows_from_offset_minus_1",
    "rows_from_offset_minus_7",
    "rows_from_offset_minus_30",
    "rows_from_offset_minus_365",
    "rows_from_offset_minus_3650",
    "rows_from_offset_plus_1",
)

# Terminal-status enum (§§6.1, 9)
TERMINAL_STATUS_RAW = "raw_t0_present"
TERMINAL_STATUS_DOC_EXC = "represented_only_documented_exception"
TERMINAL_STATUS_KSG = "known_no_data_gap"
TERMINAL_STATUS_ENUM: Tuple[str, ...] = (
    TERMINAL_STATUS_RAW,
    TERMINAL_STATUS_DOC_EXC,
    TERMINAL_STATUS_KSG,
)

# Locked rolling-window lengths (§6.6)
ROLLING_WINDOWS_MEAN_STD = (7, 14, 30)
ROLLING_WINDOW_OFFSET_0_SHARE = 30
ROLLING_WINDOWS_PERCENTILE = (30, 90, 365)
WARMUP_WINDOW = 365  # the broad warmup is keyed off the longest locked feature

SPIKE_THRESHOLD_LOW = 2.0
SPIKE_THRESHOLD_HIGH = 3.0

# F1-F6 forbidden literals (§13)
FORBIDDEN_F1_F6_LITERALS: Tuple[str, ...] = (
    "raw 365/365",
    "ordinary completion",
    "no-data gap",
    "recovered day",
    "raw-processed day",
    "exact runner-output gate from BigQuery count 105041",
)

# Boundary declarations (§11/§12) — all true in step2_metadata.json
BOUNDARY_DECLARATIONS_KEYS: Tuple[str, ...] = (
    "no_step_2_market_join",
    "no_market_data",
    "no_instrument",
    "no_gdelt_fetch",
    "no_bigquery",
    "no_row_export",
    "no_known_substrate_gaps_amendment",
)

# Documented-exception provenance fields that must be present per §10
DOC_EXCEPTION_PROVENANCE_FIELDS: Tuple[str, ...] = (
    "chunk_id",
    "date",
    "raw_filename",
    "label",
    "catalog_md5",
    "catalog_filesize_bytes",
    "http_status",
    "raw_object_parsed",
    "rows_recovered",
    "no_data_gap",
    "recovered",
    "known_substrate_gap_amended",
    "representation_artifact",
    "representation_artifact_sha256",
    "contract",
    "contract_sha256",
    "source_chunk_output_dir",
    "source_chunk_metadata_sha256",
)


# ----------------------------------------------------------------------------
# Locked output feature schema (§6) — order is part of the contract
# ----------------------------------------------------------------------------

def _build_feature_schema() -> Tuple[str, ...]:
    cols: List[str] = []
    # §6.1 identity / passthrough
    cols += [
        "civil_date",
        "represented_only",
        "documented_exception_label",
        "is_known_substrate_gap",
        "terminal_status",
        "coverage_quality_flag",
    ]
    # §6.2 raw counts (seven offsets, then total)
    cols += list(OFFSET_COLUMNS) + ["total_row_count"]
    # §6.3 scale transforms
    cols += ["log1p_total_row_count"] + [
        "log1p_" + name for name in OFFSET_COLUMNS
    ]
    # §6.4 coverage / completeness
    cols += [
        "offset_count_present_count",
        "offset_count_zero_count",
        "has_any_missing_offset_count",
        "coverage_completeness",
    ]
    # §6.5 cross-offset structure
    cols += [
        "offset_0_share_of_total",
        "share_offset_minus_1",
        "share_offset_minus_7",
        "share_offset_minus_30",
        "share_offset_minus_365",
        "share_offset_minus_3650",
        "share_offset_plus_1",
        "neighbor_offset_sum",
        "neighbor_offset_share_of_total",
        "nonzero_offset_count",
    ]
    # §6.6 temporal — raw-count descriptives (NOT z-denominator)
    for w in ROLLING_WINDOWS_MEAN_STD:
        cols.append(f"roll_mean_total_w{w}")
    for w in ROLLING_WINDOWS_MEAN_STD:
        cols.append(f"roll_std_total_w{w}")
    # §6.6 temporal — log1p z-score reference columns
    for w in ROLLING_WINDOWS_MEAN_STD:
        cols.append(f"roll_mean_log1p_total_w{w}")
    for w in ROLLING_WINDOWS_MEAN_STD:
        cols.append(f"roll_std_log1p_total_w{w}")
    # §6.6 z-scores (log1p / log1p reference)
    for w in ROLLING_WINDOWS_MEAN_STD:
        cols.append(f"roll_z_log1p_total_w{w}")
    # §6.6 percentile ranks
    for w in ROLLING_WINDOWS_PERCENTILE:
        cols.append(f"roll_pct_log1p_total_w{w}")
    # §6.6 day-over-day
    cols.append("delta_log1p_total_dod")
    # §6.6 offset_0 share rolling family
    cols += [
        f"roll_mean_offset_0_share_w{ROLLING_WINDOW_OFFSET_0_SHARE}",
        f"roll_std_offset_0_share_w{ROLLING_WINDOW_OFFSET_0_SHARE}",
        f"roll_z_offset_0_share_w{ROLLING_WINDOW_OFFSET_0_SHARE}",
    ]
    # §6.7 spike flags
    for w in ROLLING_WINDOWS_MEAN_STD:
        cols.append(f"spike_w{w}_z_ge_2")
        cols.append(f"spike_w{w}_z_ge_3")
    # §6.8 edge / domain flags
    cols += [
        "is_domain_start_edge",
        "is_rolling_window_warmup",
        "has_full_7d_history",
        "has_full_30d_history",
        "has_full_365d_history",
    ]
    return tuple(cols)


FEATURE_SCHEMA: Tuple[str, ...] = _build_feature_schema()


# ----------------------------------------------------------------------------
# Error types
# ----------------------------------------------------------------------------

class Step2InputError(Exception):
    """Raised when the merged substrate inputs fail pinning/schema checks."""


class Step2ConformanceError(Exception):
    """Raised when the §§9-11 conformance gate fails closed."""


class Step2BoundaryError(Exception):
    """Raised when an execution / write-output boundary is crossed."""


# ----------------------------------------------------------------------------
# Utility: file SHA-256
# ----------------------------------------------------------------------------

def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ----------------------------------------------------------------------------
# Input loading and pin verification
# ----------------------------------------------------------------------------

def verify_input_pins(merged_dir: Path) -> Dict[str, str]:
    """Verify the three input artifact SHA-256s and the build_manifest_digest
    match the pinned values in §2 of the design memo. Fail closed otherwise.

    Returns the dict of observed SHA-256s on success.
    """
    merged_dir = Path(merged_dir)
    if not merged_dir.is_dir():
        raise Step2InputError(f"merged substrate directory missing: {merged_dir}")

    observed: Dict[str, str] = {}
    for basename, expected_sha in INPUT_ARTIFACT_SHA256.items():
        artifact = merged_dir / basename
        if not artifact.is_file():
            raise Step2InputError(
                f"required merged artifact missing: {artifact}"
            )
        got = sha256_of_file(artifact)
        observed[basename] = got
        if got != expected_sha:
            raise Step2InputError(
                f"SHA-256 mismatch for {basename}: "
                f"expected {expected_sha}, got {got}"
            )

    meta_path = merged_dir / "build_metadata.json"
    with open(meta_path, encoding="utf-8") as fh:
        metadata = json.load(fh)
    got_digest = metadata.get("build_manifest_digest")
    if got_digest != EXPECTED_BUILD_MANIFEST_DIGEST:
        raise Step2InputError(
            "build_manifest_digest mismatch: "
            f"expected {EXPECTED_BUILD_MANIFEST_DIGEST}, got {got_digest!r}"
        )
    return observed


def _parse_bool(text: str) -> bool:
    cleaned = text.strip().lower()
    if cleaned == "true":
        return True
    if cleaned == "false" or cleaned == "":
        return False
    raise Step2InputError(f"unparseable boolean column value: {text!r}")


def _parse_int(text: str, *, column: str) -> int:
    try:
        return int(text)
    except ValueError as exc:
        raise Step2InputError(
            f"unparseable integer in column {column!r}: {text!r}"
        ) from exc


def _parse_float(text: str, *, column: str) -> float:
    try:
        return float(text)
    except ValueError as exc:
        raise Step2InputError(
            f"unparseable float in column {column!r}: {text!r}"
        ) from exc


def load_merged_csv(csv_path: Path) -> List[Dict[str, Any]]:
    """Parse the merged daily-count CSV into typed dicts and validate header."""
    csv_path = Path(csv_path)
    with open(csv_path, encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        if tuple(header) != EXPECTED_INPUT_COLUMNS:
            raise Step2InputError(
                "merged CSV header mismatch. expected="
                f"{EXPECTED_INPUT_COLUMNS}, got={tuple(header)}"
            )
        rows: List[Dict[str, Any]] = []
        for raw in reader:
            if len(raw) != len(EXPECTED_INPUT_COLUMNS):
                raise Step2InputError(
                    f"row has {len(raw)} cells, expected "
                    f"{len(EXPECTED_INPUT_COLUMNS)}: {raw!r}"
                )
            d: Dict[str, Any] = {}
            for col, val in zip(EXPECTED_INPUT_COLUMNS, raw):
                if col == "civil_date":
                    d[col] = val
                elif col in OFFSET_COLUMNS or col == "total_row_count":
                    d[col] = _parse_int(val, column=col)
                elif col in (
                    "expected_contributing_files_count",
                    "available_contributing_files_count",
                ):
                    d[col] = _parse_int(val, column=col)
                elif col == "coverage_completeness":
                    d[col] = _parse_float(val, column=col)
                elif col == "represented_only":
                    d[col] = _parse_bool(val)
                else:
                    d[col] = val
            rows.append(d)
    return rows


def load_inputs(
    merged_dir: Path,
    *,
    verify_pins: bool = True,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Load the merged substrate CSV + metadata.

    When `verify_pins` is True (default), the three input artifact SHA-256s and
    the embedded build_manifest_digest are checked against the §2 pins.
    """
    merged_dir = Path(merged_dir)
    if verify_pins:
        verify_input_pins(merged_dir)
    rows = load_merged_csv(merged_dir / "build_daily_counts.csv")
    with open(merged_dir / "build_metadata.json", encoding="utf-8") as fh:
        metadata = json.load(fh)
    return rows, metadata


# ----------------------------------------------------------------------------
# Helpers: NaN-safe share, rolling window math
# ----------------------------------------------------------------------------

def _safe_share(num: float, den: float) -> float:
    """NaN-safe share computation: return 0.0 when the denominator is zero."""
    if den == 0:
        return 0.0
    return num / den


def _trailing_slice(
    values: Sequence[Any],
    idx: int,
    window: int,
) -> Sequence[Any]:
    """Return the current-row-inclusive trailing slice of length `window`.

    The slice covers `values[idx-window+1 : idx+1]` clipped to a non-negative
    start. Used by §6.6 rolling statistics.
    """
    if window <= 0:
        raise ValueError(f"window must be positive, got {window}")
    start = max(0, idx - window + 1)
    return values[start : idx + 1]


def _trailing_mean(
    values: Sequence[float],
    idx: int,
    window: int,
) -> Optional[float]:
    """Mean over the trailing window; None when fewer than `window` rows."""
    if (idx + 1) < window:
        return None
    sliced = _trailing_slice(values, idx, window)
    return sum(sliced) / len(sliced)


def _trailing_std(
    values: Sequence[float],
    idx: int,
    window: int,
) -> Optional[float]:
    """Sample standard deviation (ddof=1) over the trailing window; None when
    fewer than `window` rows are available."""
    if (idx + 1) < window:
        return None
    sliced = list(_trailing_slice(values, idx, window))
    if len(sliced) < 2:
        return None
    return statistics.stdev(sliced)


def _trailing_z(
    value: float,
    mean: Optional[float],
    std: Optional[float],
) -> Optional[float]:
    """NaN-safe z-score; returns None on warmup or zero/undefined std."""
    if mean is None or std is None:
        return None
    if std == 0:
        return None
    return (value - mean) / std


def _trailing_percentile_rank(
    values: Sequence[float],
    idx: int,
    window: int,
) -> Optional[float]:
    """Average-rank percentile of `values[idx]` within the trailing window.

    Ties are broken by average rank (memo §6.6). Returns None when fewer than
    `window` rows are available.
    """
    if (idx + 1) < window:
        return None
    sliced = _trailing_slice(values, idx, window)
    current = values[idx]
    n = len(sliced)
    less = sum(1 for v in sliced if v < current)
    equal = sum(1 for v in sliced if v == current)
    average_rank = less + (equal + 1) / 2.0
    return average_rank / n


# ----------------------------------------------------------------------------
# Terminal-status derivation (§§6.1, 9)
# ----------------------------------------------------------------------------

def derive_terminal_status(
    civil_date_str: str,
    documented_exception_label: str,
    is_known_substrate_gap: bool,
) -> str:
    """Deterministic terminal-status mapping per §§6.1 and 9."""
    if documented_exception_label == DOCUMENTED_EXCEPTION_LABEL:
        return TERMINAL_STATUS_DOC_EXC
    if is_known_substrate_gap:
        # Defense-in-depth: never label the documented-exception date as KSG
        # even if upstream metadata is corrupted, the label check above wins.
        if civil_date_str == DOCUMENTED_EXCEPTION_DATE:
            raise Step2ConformanceError(
                f"{DOCUMENTED_EXCEPTION_DATE} must never be labeled "
                f"{TERMINAL_STATUS_KSG}"
            )
        return TERMINAL_STATUS_KSG
    return TERMINAL_STATUS_RAW


# ----------------------------------------------------------------------------
# Per-row feature construction
# ----------------------------------------------------------------------------

def _row_static_features(row: Mapping[str, Any]) -> Dict[str, Any]:
    """Build the identity/passthrough, raw-count, scale-transform, coverage,
    and cross-offset feature subset for a single row (no rolling features).
    """
    civil_date_str = row["civil_date"]
    is_ksg = civil_date_str in KNOWN_SUBSTRATE_GAPS
    doc_label = row.get("documented_exception_label", "") or ""
    terminal_status = derive_terminal_status(civil_date_str, doc_label, is_ksg)

    total = int(row["total_row_count"])
    offsets: Dict[str, int] = {col: int(row[col]) for col in OFFSET_COLUMNS}

    out: Dict[str, Any] = {
        "civil_date": civil_date_str,
        "represented_only": bool(row["represented_only"]),
        "documented_exception_label": doc_label,
        "is_known_substrate_gap": is_ksg,
        "terminal_status": terminal_status,
        "coverage_quality_flag": row["coverage_quality_flag"],
    }
    for col in OFFSET_COLUMNS:
        out[col] = offsets[col]
    out["total_row_count"] = total

    # §6.3 scale transforms
    out["log1p_total_row_count"] = math.log1p(total)
    for col in OFFSET_COLUMNS:
        out["log1p_" + col] = math.log1p(offsets[col])

    # §6.4 coverage / completeness
    present = sum(1 for col in OFFSET_COLUMNS if offsets[col] > 0)
    zeros = len(OFFSET_COLUMNS) - present
    out["offset_count_present_count"] = present
    out["offset_count_zero_count"] = zeros
    out["has_any_missing_offset_count"] = zeros > 0
    out["coverage_completeness"] = float(row["coverage_completeness"])

    # §6.5 cross-offset structure
    out["offset_0_share_of_total"] = _safe_share(
        offsets["rows_from_offset_0"], total
    )
    out["share_offset_minus_1"] = _safe_share(
        offsets["rows_from_offset_minus_1"], total
    )
    out["share_offset_minus_7"] = _safe_share(
        offsets["rows_from_offset_minus_7"], total
    )
    out["share_offset_minus_30"] = _safe_share(
        offsets["rows_from_offset_minus_30"], total
    )
    out["share_offset_minus_365"] = _safe_share(
        offsets["rows_from_offset_minus_365"], total
    )
    out["share_offset_minus_3650"] = _safe_share(
        offsets["rows_from_offset_minus_3650"], total
    )
    out["share_offset_plus_1"] = _safe_share(
        offsets["rows_from_offset_plus_1"], total
    )
    neighbor_sum = sum(offsets[c] for c in NEIGHBOR_OFFSET_COLUMNS)
    out["neighbor_offset_sum"] = neighbor_sum
    out["neighbor_offset_share_of_total"] = _safe_share(neighbor_sum, total)
    out["nonzero_offset_count"] = present
    return out


def _attach_rolling_features(
    static_rows: List[Dict[str, Any]],
    domain_start_str: str,
) -> None:
    """Attach §§6.6, 6.7, 6.8 rolling/percentile/spike/warmup features in
    place. Rolling features use current-row-inclusive trailing windows over the
    full row sequence in civil-date ascending order. Represented-only and KSG
    rows are INCLUDED VERBATIM in rolling computations (§7).
    """
    totals: List[float] = [float(r["total_row_count"]) for r in static_rows]
    log1p_totals: List[float] = [r["log1p_total_row_count"] for r in static_rows]
    offset_0_shares: List[float] = [r["offset_0_share_of_total"] for r in static_rows]

    domain_start_date = date.fromisoformat(domain_start_str)
    domain_start_edge_dates = {
        (domain_start_date + timedelta(days=k)).isoformat() for k in range(7)
    }

    for i, r in enumerate(static_rows):
        # raw-count descriptives (NOT z denominator)
        for w in ROLLING_WINDOWS_MEAN_STD:
            r[f"roll_mean_total_w{w}"] = _trailing_mean(totals, i, w)
            r[f"roll_std_total_w{w}"] = _trailing_std(totals, i, w)

        # log1p z-score reference columns
        log1p_means: Dict[int, Optional[float]] = {}
        log1p_stds: Dict[int, Optional[float]] = {}
        for w in ROLLING_WINDOWS_MEAN_STD:
            m = _trailing_mean(log1p_totals, i, w)
            s = _trailing_std(log1p_totals, i, w)
            log1p_means[w] = m
            log1p_stds[w] = s
            r[f"roll_mean_log1p_total_w{w}"] = m
            r[f"roll_std_log1p_total_w{w}"] = s

        # z-scores of log1p (NOT raw-count mean/std)
        z_by_w: Dict[int, Optional[float]] = {}
        for w in ROLLING_WINDOWS_MEAN_STD:
            z = _trailing_z(log1p_totals[i], log1p_means[w], log1p_stds[w])
            z_by_w[w] = z
            r[f"roll_z_log1p_total_w{w}"] = z

        # percentiles
        for w in ROLLING_WINDOWS_PERCENTILE:
            r[f"roll_pct_log1p_total_w{w}"] = _trailing_percentile_rank(
                log1p_totals, i, w
            )

        # day-over-day delta in log1p
        if i == 0:
            r["delta_log1p_total_dod"] = None
        else:
            r["delta_log1p_total_dod"] = log1p_totals[i] - log1p_totals[i - 1]

        # offset_0 share rolling family
        w0 = ROLLING_WINDOW_OFFSET_0_SHARE
        share_mean = _trailing_mean(offset_0_shares, i, w0)
        share_std = _trailing_std(offset_0_shares, i, w0)
        r[f"roll_mean_offset_0_share_w{w0}"] = share_mean
        r[f"roll_std_offset_0_share_w{w0}"] = share_std
        r[f"roll_z_offset_0_share_w{w0}"] = _trailing_z(
            offset_0_shares[i], share_mean, share_std
        )

        # spike flags (False on warmup / NaN / zero-std)
        for w in ROLLING_WINDOWS_MEAN_STD:
            z = z_by_w[w]
            if z is None:
                ge_2 = False
                ge_3 = False
            else:
                ge_2 = z >= SPIKE_THRESHOLD_LOW
                ge_3 = z >= SPIKE_THRESHOLD_HIGH
            r[f"spike_w{w}_z_ge_2"] = ge_2
            r[f"spike_w{w}_z_ge_3"] = ge_3

        # edge / domain flags
        r["is_domain_start_edge"] = r["civil_date"] in domain_start_edge_dates
        history_len = i + 1
        has_full_7 = history_len >= 7
        has_full_30 = history_len >= 30
        has_full_365 = history_len >= WARMUP_WINDOW
        r["has_full_7d_history"] = has_full_7
        r["has_full_30d_history"] = has_full_30
        r["has_full_365d_history"] = has_full_365
        # broad warmup: equivalent to has_full_365d_history == False
        r["is_rolling_window_warmup"] = not has_full_365


def derive_features(
    rows: Sequence[Mapping[str, Any]],
    *,
    domain_start: str = DOMAIN_START,
) -> List[Dict[str, Any]]:
    """Build the full Step 2 feature table (in-memory list of dicts).

    Rows are first sorted deterministically by civil_date ascending, then the
    static per-row features are computed, then rolling features are attached
    over the full ordered sequence.
    """
    sorted_rows = sorted(rows, key=lambda r: r["civil_date"])
    static_rows = [_row_static_features(r) for r in sorted_rows]
    _attach_rolling_features(static_rows, domain_start)
    # Lock the column order to FEATURE_SCHEMA without dropping or adding keys.
    out: List[Dict[str, Any]] = []
    for r in static_rows:
        missing = [c for c in FEATURE_SCHEMA if c not in r]
        if missing:
            raise Step2ConformanceError(
                f"feature row is missing locked columns: {missing}"
            )
        extras = [k for k in r if k not in FEATURE_SCHEMA]
        if extras:
            raise Step2ConformanceError(
                f"feature row carries non-schema columns: {extras}"
            )
        out.append({col: r[col] for col in FEATURE_SCHEMA})
    return out


# ----------------------------------------------------------------------------
# Conformance gate (§§10, 11)
# ----------------------------------------------------------------------------

def assert_seven_offset_sum_invariant(
    rows: Iterable[Mapping[str, Any]],
) -> None:
    for r in rows:
        total = int(r["total_row_count"])
        offsets_sum = sum(int(r[c]) for c in OFFSET_COLUMNS)
        if total != offsets_sum:
            raise Step2ConformanceError(
                f"seven-offset-sum invariant failed at "
                f"{r['civil_date']}: total_row_count={total} != sum={offsets_sum}"
            )


def assert_documented_exception_invariants(
    rows: Sequence[Mapping[str, Any]],
    metadata: Mapping[str, Any],
) -> None:
    """§10 hard-stop set on the documented-exception row and metadata."""
    matches = [r for r in rows if r["civil_date"] == DOCUMENTED_EXCEPTION_DATE]
    if len(matches) == 0:
        raise Step2ConformanceError(
            f"documented-exception row {DOCUMENTED_EXCEPTION_DATE} missing"
        )
    if len(matches) > 1:
        raise Step2ConformanceError(
            f"documented-exception row {DOCUMENTED_EXCEPTION_DATE} appears "
            f"{len(matches)} times (>1)"
        )
    r = matches[0]

    label = r.get("documented_exception_label", "")
    if label != DOCUMENTED_EXCEPTION_LABEL:
        raise Step2ConformanceError(
            f"documented-exception label mismatch on {DOCUMENTED_EXCEPTION_DATE}: "
            f"expected {DOCUMENTED_EXCEPTION_LABEL!r}, got {label!r}"
        )
    if not bool(r.get("represented_only", False)):
        raise Step2ConformanceError(
            f"represented_only must be True on {DOCUMENTED_EXCEPTION_DATE}"
        )
    if int(r["total_row_count"]) != DOCUMENTED_EXCEPTION_TOTAL:
        raise Step2ConformanceError(
            f"total_row_count must be {DOCUMENTED_EXCEPTION_TOTAL} on "
            f"{DOCUMENTED_EXCEPTION_DATE}, got {r['total_row_count']!r}"
        )
    if int(r["rows_from_offset_0"]) != 0:
        raise Step2ConformanceError(
            "rows_from_offset_0 must be 0 on "
            f"{DOCUMENTED_EXCEPTION_DATE}, got {r['rows_from_offset_0']!r}"
        )

    # Neighbor cross-check: 1267 = 91 + 849 + 327
    parts = tuple(
        int(r[c]) for c in DOCUMENTED_EXCEPTION_NEIGHBOR_COLUMNS
    )
    if parts != DOCUMENTED_EXCEPTION_NEIGHBOR_PARTS:
        raise Step2ConformanceError(
            f"documented-exception neighbor parts on "
            f"{DOCUMENTED_EXCEPTION_DATE} must equal "
            f"{DOCUMENTED_EXCEPTION_NEIGHBOR_PARTS}, got {parts}"
        )
    if sum(parts) != DOCUMENTED_EXCEPTION_TOTAL:
        raise Step2ConformanceError(
            f"neighbor parts sum {sum(parts)} != "
            f"documented-exception total {DOCUMENTED_EXCEPTION_TOTAL}"
        )

    # Reclassification protection
    ts = r.get("terminal_status")
    if ts is not None and ts != TERMINAL_STATUS_DOC_EXC:
        raise Step2ConformanceError(
            f"documented-exception row reclassified to {ts!r}"
        )

    # §10 metadata propagation: documented_exceptions[0] must exist with the
    # full provenance field set.
    doc_exc_list = metadata.get("documented_exceptions") or []
    if len(doc_exc_list) != 1:
        raise Step2ConformanceError(
            f"metadata.documented_exceptions must have exactly one entry, got "
            f"{len(doc_exc_list)}"
        )
    entry = doc_exc_list[0]
    if entry.get("label") != DOCUMENTED_EXCEPTION_LABEL:
        raise Step2ConformanceError(
            "metadata documented-exception label mismatch: "
            f"expected {DOCUMENTED_EXCEPTION_LABEL!r}, "
            f"got {entry.get('label')!r}"
        )
    if entry.get("date") != DOCUMENTED_EXCEPTION_DATE:
        raise Step2ConformanceError(
            "metadata documented-exception date mismatch: "
            f"expected {DOCUMENTED_EXCEPTION_DATE!r}, "
            f"got {entry.get('date')!r}"
        )
    missing_prov = [
        f for f in DOC_EXCEPTION_PROVENANCE_FIELDS if f not in entry
    ]
    if missing_prov:
        raise Step2ConformanceError(
            "documented-exception provenance missing fields: "
            f"{missing_prov}"
        )


def assert_ksg_invariants(rows: Sequence[Mapping[str, Any]]) -> None:
    """§9 hard-stop set: four KSG rows present with the correct flags; the
    documented-exception date must never be a KSG."""
    by_date: Dict[str, Mapping[str, Any]] = {r["civil_date"]: r for r in rows}
    for ksg in KNOWN_SUBSTRATE_GAPS:
        if ksg not in by_date:
            raise Step2ConformanceError(f"KSG row missing: {ksg}")
        r = by_date[ksg]
        if not bool(r.get("is_known_substrate_gap", False)):
            raise Step2ConformanceError(
                f"KSG row {ksg} has is_known_substrate_gap != True"
            )
        if r.get("terminal_status") not in (None, TERMINAL_STATUS_KSG):
            raise Step2ConformanceError(
                f"KSG row {ksg} terminal_status={r['terminal_status']!r} "
                f"!= {TERMINAL_STATUS_KSG!r}"
            )
        if bool(r.get("represented_only", False)):
            raise Step2ConformanceError(
                f"KSG row {ksg} must have represented_only=False"
            )
        if r.get("documented_exception_label", "") != "":
            raise Step2ConformanceError(
                f"KSG row {ksg} must have empty documented_exception_label"
            )
    # Reverse direction: no non-KSG date carries is_known_substrate_gap=True
    # and the documented-exception date is never KSG.
    for r in rows:
        d = r["civil_date"]
        if d == DOCUMENTED_EXCEPTION_DATE:
            if bool(r.get("is_known_substrate_gap", False)):
                raise Step2ConformanceError(
                    f"{DOCUMENTED_EXCEPTION_DATE} must never be a KSG"
                )
            if r.get("terminal_status") == TERMINAL_STATUS_KSG:
                raise Step2ConformanceError(
                    f"{DOCUMENTED_EXCEPTION_DATE} must never have "
                    f"terminal_status={TERMINAL_STATUS_KSG!r}"
                )
        elif d not in KNOWN_SUBSTRATE_GAPS:
            if bool(r.get("is_known_substrate_gap", False)):
                raise Step2ConformanceError(
                    f"non-KSG row {d} has is_known_substrate_gap=True"
                )
            if r.get("terminal_status") == TERMINAL_STATUS_KSG:
                raise Step2ConformanceError(
                    f"non-KSG row {d} has terminal_status="
                    f"{TERMINAL_STATUS_KSG!r}"
                )


def assert_date_domain(rows: Sequence[Mapping[str, Any]]) -> None:
    if len(rows) != EXPECTED_ROW_COUNT:
        raise Step2ConformanceError(
            f"row count {len(rows)} != expected {EXPECTED_ROW_COUNT}"
        )
    dates = [r["civil_date"] for r in rows]
    if dates[0] != DOMAIN_START:
        raise Step2ConformanceError(
            f"first civil_date {dates[0]!r} != {DOMAIN_START!r}"
        )
    if dates[-1] != DOMAIN_END:
        raise Step2ConformanceError(
            f"last civil_date {dates[-1]!r} != {DOMAIN_END!r}"
        )
    if len(set(dates)) != len(dates):
        # find the duplicates for the error message
        seen: Dict[str, int] = {}
        for d in dates:
            seen[d] = seen.get(d, 0) + 1
        dups = sorted([d for d, c in seen.items() if c > 1])
        raise Step2ConformanceError(
            f"duplicate civil_date values: {dups[:10]}{'...' if len(dups) > 10 else ''}"
        )
    end_date = date.fromisoformat(DOMAIN_END)
    for d in dates:
        if date.fromisoformat(d) > end_date:
            raise Step2ConformanceError(
                f"post-{DOMAIN_END} row present: {d}"
            )


def assert_feature_schema_exact(
    feature_rows: Sequence[Mapping[str, Any]],
) -> None:
    """Every row must have keys exactly equal to FEATURE_SCHEMA in the same
    order. Enforces no extra columns (e.g., market / outcome smuggling)."""
    schema = FEATURE_SCHEMA
    for r in feature_rows:
        keys = tuple(r.keys())
        if keys != schema:
            extras = [k for k in keys if k not in schema]
            missing = [k for k in schema if k not in keys]
            raise Step2ConformanceError(
                "feature schema mismatch on "
                f"{r.get('civil_date', '?')}: extras={extras}, missing={missing}"
            )


def audit_f1_f6(text: str) -> List[str]:
    """Return the list of forbidden literals (§13) that appear in `text`.

    This is a strict substring detector: any occurrence is flagged. The Step 2
    summary and metadata-prose generators produced by this module deliberately
    avoid all six literals so that the audit returns an empty list. The memo
    permits these literals only in meta-linguistic prohibition contexts; this
    module enforces the stricter rule of complete absence in generated prose.
    """
    return [lit for lit in FORBIDDEN_F1_F6_LITERALS if lit in text]


def run_conformance_gate(
    merged_dir: Path,
    *,
    verify_pins: bool = True,
) -> Dict[str, Any]:
    """End-to-end pre-execution conformance gate. Never writes any artifact.

    Returns a structured report dict and raises Step2ConformanceError on any
    fail-closed condition.
    """
    merged_dir = Path(merged_dir)
    report: Dict[str, Any] = {
        "merged_dir": str(merged_dir),
        "step2_implementation_version": STEP2_IMPLEMENTATION_VERSION,
        "design_memo_sha256": DESIGN_MEMO_SHA256,
        "input_artifact_sha256s_expected": dict(INPUT_ARTIFACT_SHA256),
        "build_manifest_digest_expected": EXPECTED_BUILD_MANIFEST_DIGEST,
        "verify_pins": verify_pins,
        "boundary_declarations": {k: True for k in BOUNDARY_DECLARATIONS_KEYS},
    }

    if verify_pins:
        report["input_artifact_sha256s_observed"] = verify_input_pins(merged_dir)

    rows, metadata = load_inputs(merged_dir, verify_pins=False)
    report["input_row_count"] = len(rows)

    assert_date_domain(rows)
    assert_seven_offset_sum_invariant(rows)
    assert_documented_exception_invariants(rows, metadata)

    feature_rows = derive_features(rows)
    report["feature_row_count"] = len(feature_rows)
    report["feature_schema"] = list(FEATURE_SCHEMA)

    assert_feature_schema_exact(feature_rows)
    assert_ksg_invariants(feature_rows)
    # The documented-exception invariants must also pass on the feature table.
    assert_documented_exception_invariants(feature_rows, metadata)

    summary = render_step2_summary(feature_rows, metadata, merged_dir)
    forbidden_hits = audit_f1_f6(summary)
    if forbidden_hits:
        raise Step2ConformanceError(
            f"F1-F6 audit failed on summary: hits={forbidden_hits}"
        )
    report["summary_audit_hits"] = forbidden_hits
    report["summary_byte_count"] = len(summary.encode("utf-8"))

    step2_metadata = render_step2_metadata(feature_rows, metadata, merged_dir)
    forbidden_hits_meta = audit_f1_f6(json.dumps(step2_metadata, indent=2))
    if forbidden_hits_meta:
        raise Step2ConformanceError(
            f"F1-F6 audit failed on metadata prose: hits={forbidden_hits_meta}"
        )
    report["metadata_audit_hits"] = forbidden_hits_meta

    # Verdict (per §15 of the design memo)
    report["verdict"] = "PASS — STEP 2 IMPLEMENTATION CONFORMS TO DESIGN MEMO"
    return report


# ----------------------------------------------------------------------------
# Output rendering (in-memory only; never written by this module)
# ----------------------------------------------------------------------------

def render_step2_summary(
    feature_rows: Sequence[Mapping[str, Any]],
    metadata: Mapping[str, Any],
    merged_dir: Path,
) -> str:
    """Build the step2_summary.md content. F1-F6 safe by construction."""
    n_rows = len(feature_rows)
    n_features = len(FEATURE_SCHEMA)
    agg = metadata.get("aggregate", {})
    doc_exc_list = metadata.get("documented_exceptions", []) or []
    doc_exc = doc_exc_list[0] if doc_exc_list else {}
    lines = [
        "# Lane 2 GDELT1 Step 2 Daily-Feature Summary",
        "",
        "Substrate is 10/10 terminal-status (9 raw-complete chunks + 1 "
        "labeled-complete documented-exception chunk).",
        "",
        f"- merged substrate directory: `{merged_dir}`",
        f"- input rows consumed: {n_rows}",
        f"- locked feature column count: {n_features}",
        f"- design memo SHA-256: `{DESIGN_MEMO_SHA256}`",
        f"- build_manifest_digest: `{EXPECTED_BUILD_MANIFEST_DIGEST}`",
        "",
        "## Day-class counts (from `build_metadata.json` aggregate)",
        "",
        f"- raw_processed_days: {agg.get('raw_processed_days')}",
        "- documented_unavailable_data_confirmed_days: "
        f"{agg.get('documented_unavailable_data_confirmed_days')}",
        f"- recovered_days: {agg.get('recovered_days')}",
        f"- known_substrate_gap_days: {agg.get('known_no_data_gap_days')}",
        f"- terminal_status_days: {agg.get('terminal_status_days')}",
        "",
        "## Documented-exception row",
        "",
        f"- date: {doc_exc.get('date')}",
        f"- label: {doc_exc.get('label')}",
        "- propagated represented-only: True",
        f"- total_row_count: {DOCUMENTED_EXCEPTION_TOTAL}",
        "- neighbor-offset cross-check: "
        f"{' + '.join(str(p) for p in DOCUMENTED_EXCEPTION_NEIGHBOR_PARTS)}"
        f" = {DOCUMENTED_EXCEPTION_TOTAL}",
        "",
        "## Boundary declarations",
        "",
    ]
    for k in BOUNDARY_DECLARATIONS_KEYS:
        lines.append(f"- {k}: true")
    lines += [
        "",
        "This summary describes the GDELT-only substrate and the deterministic "
        "feature derivation. No exogenous-series claims and no outcome-variable "
        "claims are asserted here. Step 2 implementation, Step 2 execution, "
        "and the later separately authorized join/construction phases remain "
        "firewalled until separately authorized.",
        "",
    ]
    return "\n".join(lines)


def render_step2_metadata(
    feature_rows: Sequence[Mapping[str, Any]],
    metadata: Mapping[str, Any],
    merged_dir: Path,
) -> Dict[str, Any]:
    """Build the step2_metadata.json structure. Inherits documented-exception
    provenance verbatim from the input metadata; never invents content."""
    doc_exc_list = metadata.get("documented_exceptions", []) or []
    by_terminal_status: Dict[str, int] = {k: 0 for k in TERMINAL_STATUS_ENUM}
    for r in feature_rows:
        ts = r.get("terminal_status")
        if ts in by_terminal_status:
            by_terminal_status[ts] += 1
    reconcile_sum = sum(by_terminal_status.values())
    out: Dict[str, Any] = {
        "step2_implementation_version": STEP2_IMPLEMENTATION_VERSION,
        "design_memo": {
            "path": "docs/lane2_gdelt1_step2_implementation_design_memo_v0.1.md",
            "sha256": DESIGN_MEMO_SHA256,
        },
        "input_substrate": {
            "dir": str(merged_dir),
            "build_manifest_digest": EXPECTED_BUILD_MANIFEST_DIGEST,
            "build_daily_counts_sha256":
                INPUT_ARTIFACT_SHA256["build_daily_counts.csv"],
            "build_metadata_sha256":
                INPUT_ARTIFACT_SHA256["build_metadata.json"],
            "build_summary_sha256":
                INPUT_ARTIFACT_SHA256["build_summary.md"],
        },
        "documented_exceptions": list(doc_exc_list),
        "feature_schema": list(FEATURE_SCHEMA),
        "feature_schema_locked": True,
        "represented_only_inclusion_policy": "include_label_derived_no_imputation",
        "ksg_inclusion_policy": "include_internal_terminal_status_enum_only",
        "rolling_window_inclusion_policy": "include_verbatim_no_imputation_no_exclusion",
        "rolling_window_convention": "current_row_inclusive_trailing",
        "warmup_policy": "is_rolling_window_warmup_iff_not_has_full_365d_history",
        "day_class_counts": dict(by_terminal_status),
        "day_class_total": reconcile_sum,
        "boundary_declarations": {k: True for k in BOUNDARY_DECLARATIONS_KEYS},
        "write_authorization_mechanism": "write_step2_output_cli_flag",
        "full_build_authorized_reused": False,
        "merge_write_flag_reused": False,
    }
    return out


# ----------------------------------------------------------------------------
# Output artifact constants (§5) and the write path (§§5, 11, 14)
# ----------------------------------------------------------------------------

OUTPUT_DAILY_FEATURES_BASENAME = "step2_daily_features.csv"
OUTPUT_METADATA_BASENAME = "step2_metadata.json"
OUTPUT_SUMMARY_BASENAME = "step2_summary.md"

# Final-output basenames. Only these three may be written by the writer; any
# other basename trips a hard-fail. Mirrors the chunk/merge allow-list pattern.
ALLOWED_OUTPUT_BASENAMES: Tuple[str, ...] = (
    OUTPUT_DAILY_FEATURES_BASENAME,
    OUTPUT_METADATA_BASENAME,
    OUTPUT_SUMMARY_BASENAME,
)

# The canonical results parent for a real (separately authorized) execution.
# The writer itself takes an explicit `output_parent_dir`, so tests target a
# pytest `tmp_path` outside the repo and never touch this directory.
CANONICAL_STEP2_OUTPUT_PARENT_BASENAME = "lane2_gdelt1_step2_daily_features"

PASS_VERDICT = "PASS — STEP 2 IMPLEMENTATION CONFORMS TO DESIGN MEMO"


def utc_timestamp_compact() -> str:
    """Return a compact UTC timestamp `YYYYMMDDTHHMMSS` (no trailing `Z`).

    The caller appends the `Z` suffix to form the `<UTC-ts>Z` output-dir name
    per §5. The timestamp affects only the directory name, never any artifact
    file content, so the three written artifacts stay byte-deterministic.
    """
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


def _format_csv_cell(value: Any) -> str:
    """Deterministically format a feature value as a CSV cell string.

    Locked conventions (so output SHA-256s are reproducible across runs):
      - None        -> "" (empty cell; a warmup/undefined rolling value)
      - bool        -> "true" / "false" (checked before int: bool subclasses int)
      - int         -> str(int)
      - float       -> repr(float) (shortest round-trip form; stable in CPython)
      - str         -> the string unchanged
    """
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    return str(value)


def render_step2_daily_features_csv(
    feature_rows: Sequence[Mapping[str, Any]],
) -> str:
    """Render the locked-schema feature table as deterministic CSV text.

    Header row is exactly `FEATURE_SCHEMA`; data rows follow in the order given
    (the caller passes civil-date-ascending rows). Uses `\\n` line terminators
    and minimal quoting so the byte stream is platform-independent.
    """
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(list(FEATURE_SCHEMA))
    for r in feature_rows:
        writer.writerow([_format_csv_cell(r[col]) for col in FEATURE_SCHEMA])
    return buf.getvalue()


def write_step2_outputs(
    merged_dir: Path,
    output_parent_dir: Path,
    *,
    verify_pins: bool = True,
    timestamp_utc: Optional[str] = None,
) -> Dict[str, Any]:
    """Run the §11 conformance gate, then write the three Step 2 artifacts.

    This is the write path behind the dedicated `--write-step2-output` CLI flag.
    It is gate-agnostic at this level — the CLI script applies the separate
    `STEP2_EXECUTION_AUTHORIZED` execution gate before calling this. Tests call
    this directly with a `tmp_path` `output_parent_dir` outside the repo.

    Contract (memo §§5, 11, 14):
      - the §11 conformance gate must PASS before any byte is written (fail
        closed otherwise — no partial output);
      - exactly the three §5 artifacts are written, into a fresh
        `<output_parent_dir>/<UTC-ts>Z/` directory that must not pre-exist;
      - artifact contents are deterministic (no timestamp / output path is
        embedded in any artifact), so re-runs produce identical SHA-256s;
      - returns a manifest with the output dir, per-artifact SHA-256s, the
        verdict, and the row counts.
    """
    merged_dir = Path(merged_dir)
    output_parent_dir = Path(output_parent_dir)

    # 1. Re-PASS the pre-execution conformance gate (memo §11). Any failure
    #    raises (Step2InputError / Step2ConformanceError) before we touch disk.
    report = run_conformance_gate(merged_dir, verify_pins=verify_pins)
    if report.get("verdict") != PASS_VERDICT:
        raise Step2ConformanceError(
            f"refusing to write: conformance verdict={report.get('verdict')!r}"
        )

    # 2. Re-derive the artifacts deterministically from the pinned substrate.
    rows, metadata = load_inputs(merged_dir, verify_pins=False)
    feature_rows = derive_features(rows)

    csv_text = render_step2_daily_features_csv(feature_rows)
    summary_text = render_step2_summary(feature_rows, metadata, merged_dir)

    step2_metadata = dict(render_step2_metadata(feature_rows, metadata, merged_dir))
    step2_metadata["pre_execution_conformance_verdict"] = report["verdict"]
    step2_metadata["input_row_count"] = report["input_row_count"]
    step2_metadata["feature_row_count"] = report["feature_row_count"]
    metadata_text = json.dumps(step2_metadata, indent=2, sort_keys=True)

    # Defense-in-depth: re-run the F1-F6 audit on the exact rendered bytes.
    for label, text in (("summary", summary_text), ("metadata", metadata_text)):
        hits = audit_f1_f6(text)
        if hits:
            raise Step2ConformanceError(
                f"refusing to write: F1-F6 audit failed on {label}: {hits}"
            )

    artifacts: Dict[str, str] = {
        OUTPUT_DAILY_FEATURES_BASENAME: csv_text,
        OUTPUT_METADATA_BASENAME: metadata_text,
        OUTPUT_SUMMARY_BASENAME: summary_text,
    }
    for basename in artifacts:
        if basename not in ALLOWED_OUTPUT_BASENAMES:
            raise Step2BoundaryError(
                f"output basename not allow-listed: {basename!r}"
            )

    # 3. Fresh, unique `<UTC-ts>Z` output dir; never overwrite.
    if timestamp_utc is None:
        timestamp_utc = utc_timestamp_compact()
    output_dir = output_parent_dir / f"{timestamp_utc}Z"
    if output_dir.exists():
        raise Step2BoundaryError(
            f"refusing to overwrite existing output dir: {output_dir}"
        )
    output_dir.mkdir(parents=True, exist_ok=False)

    # 4. Write exactly the three allow-listed artifacts; hash each.
    artifacts_sha256: Dict[str, str] = {}
    for basename in ALLOWED_OUTPUT_BASENAMES:
        path = output_dir / basename
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(artifacts[basename])
        artifacts_sha256[basename] = sha256_of_file(path)

    return {
        "output_dir": str(output_dir),
        "artifacts_sha256": artifacts_sha256,
        "verdict": report["verdict"],
        "input_row_count": report["input_row_count"],
        "feature_row_count": report["feature_row_count"],
        "build_manifest_digest": EXPECTED_BUILD_MANIFEST_DIGEST,
        "step2_implementation_version": STEP2_IMPLEMENTATION_VERSION,
    }
