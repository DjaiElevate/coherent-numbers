"""Frozen-CSV hash verification and reduced-row schema loader for Candidate B.

Implements sections 5 (reduced row schema) and 6 (frozen-data provenance) of
the locked design memo (1e9a3e6). The freeze manifest at
docs/pullback_population_freeze_manifest_v0.1.md (commit 5225bfd) declares
the six pullback CSVs and their SHA-256 digests. This module re-verifies the
on-disk digests at each invocation and aborts on any mismatch.

No row-level pullback trade content is materialized to disk. The reduced row
schema is constructed in memory and returned as an immutable dataclass.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, Mapping, Optional, Sequence

import numpy as np
import pandas as pd

FREEZE_MANIFEST_PATH: str = "docs/pullback_population_freeze_manifest_v0.1.md"

FROZEN_DATASETS: Dict[str, str] = {
    "data/raw/pullback_spy_base_301_trades_2000_2022.csv":
        "b7817e0e7a02dad44923eae462c1454ab67b8fbc73539b36b81e043d8dcc2d06",
    "data/raw/pullback_phase3b_spy_trades_2005_2022.csv":
        "1d8a7b77389835a7231d6ca0742e39d963cf4dc03f822b0111039b5c19383621",
    "data/raw/pullback_phase3b_efa_trades_2005_2022.csv":
        "275af7e00f28a2a72d948228964c7a4658444f0030ac048e8a2851bc3313de82",
    "data/raw/pullback_phase3b_eem_trades_2005_2022.csv":
        "56cf8e5fe88f5230ebb8e2881f4df1e0ff633819d588764d9e9e57bbdebb6916",
    "data/raw/pullback_phase3b_gld_trades_2005_2022.csv":
        "0de7bf6dd981be8d8091a382a6dc0af594a59fa8d87f459305ad25f9dc21d1e3",
    "data/raw/pullback_phase3b_tlt_trades_2005_2022.csv":
        "037ea4178bd071e426d7cce30eeaffb554ae31d7998c8d00d5e2ba36a7388abc",
}

PHASE3B_DATASETS: Dict[str, str] = {
    "SPY": "data/raw/pullback_phase3b_spy_trades_2005_2022.csv",
    "EFA": "data/raw/pullback_phase3b_efa_trades_2005_2022.csv",
    "EEM": "data/raw/pullback_phase3b_eem_trades_2005_2022.csv",
    "GLD": "data/raw/pullback_phase3b_gld_trades_2005_2022.csv",
    "TLT": "data/raw/pullback_phase3b_tlt_trades_2005_2022.csv",
}

SPY_BASE_PATH: str = "data/raw/pullback_spy_base_301_trades_2000_2022.csv"
SPY_BASE_ASSET: str = "SPY"

OOS_CUTOFF: date = date(2022, 12, 31)
REQUIRED_COLUMNS = ("entry_date", "exit_date", "direction", "r_multiple")


class FrozenCsvHashMismatch(RuntimeError):
    """Raised when an on-disk frozen CSV digest does not match the manifest."""


class OosRowDetected(RuntimeError):
    """Raised when any loaded row has entry_date or exit_date past 2022-12-31."""


@dataclass(frozen=True, eq=False)
class ReducedTrades:
    """Reduced analytical row schema (section 5 of the locked design memo)."""

    trade_id: np.ndarray
    asset: np.ndarray
    entry_date: np.ndarray
    exit_date: np.ndarray
    is_long: np.ndarray
    r_multiple: np.ndarray
    frozen_artifact_id: np.ndarray

    def __len__(self) -> int:
        return int(self.trade_id.shape[0])


def _file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_frozen_inputs(
    repo_root: str,
    dataset_hashes: Optional[Mapping[str, str]] = None,
) -> Dict[str, str]:
    """Recompute SHA-256 of every frozen CSV and verify against the manifest.

    Returns a {relpath: observed_sha256} mapping on success.
    Raises FrozenCsvHashMismatch on the first mismatch.
    """
    if dataset_hashes is None:
        dataset_hashes = FROZEN_DATASETS
    observed: Dict[str, str] = {}
    for rel_path, expected in dataset_hashes.items():
        full_path = os.path.join(repo_root, rel_path)
        if not os.path.isfile(full_path):
            raise FrozenCsvHashMismatch(
                "frozen CSV missing: {} (expected sha256 {})".format(rel_path, expected)
            )
        got = _file_sha256(full_path)
        if got != expected:
            raise FrozenCsvHashMismatch(
                "frozen CSV digest mismatch at {}: expected {}, got {}".format(
                    rel_path, expected, got
                )
            )
        observed[rel_path] = got
    return observed


def _normalize_is_long(value) -> bool:
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        if v == "long":
            return True
        if v == "short":
            return False
        raise ValueError("unrecognized direction string: {!r}".format(value))
    if isinstance(value, (int, np.integer)):
        if value == 1:
            return True
        if value in (-1, 0):
            return False
        raise ValueError("unrecognized integer direction: {}".format(value))
    raise TypeError("unsupported direction type: {}".format(type(value).__name__))


def _check_required_columns(df: pd.DataFrame, path: str) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            "missing required columns {} in {}".format(missing, path)
        )


def _coerce_date(value) -> date:
    if isinstance(value, pd.Timestamp):
        return value.date()
    if isinstance(value, date):
        return value
    return pd.Timestamp(value).date()


def _check_no_oos_rows(entry_dates, exit_dates, path: str) -> None:
    for col, arr in (("entry_date", entry_dates), ("exit_date", exit_dates)):
        for v in arr:
            if v > OOS_CUTOFF:
                raise OosRowDetected(
                    "{} contains OOS row in {}: {}".format(col, path, v)
                )


def _load_one_csv(
    repo_root: str,
    rel_path: str,
    asset_label: str,
) -> pd.DataFrame:
    full_path = os.path.join(repo_root, rel_path)
    df = pd.read_csv(full_path)
    _check_required_columns(df, rel_path)
    df = df.copy()
    df["entry_date"] = df["entry_date"].apply(_coerce_date)
    df["exit_date"] = df["exit_date"].apply(_coerce_date)
    _check_no_oos_rows(df["entry_date"].tolist(), df["exit_date"].tolist(), rel_path)
    df["is_long"] = df["direction"].apply(_normalize_is_long).astype(bool)
    df["asset"] = asset_label
    df["frozen_artifact_id"] = rel_path
    return df[
        ["entry_date", "exit_date", "is_long", "r_multiple", "asset", "frozen_artifact_id"]
    ]


def _to_reduced(df: pd.DataFrame) -> ReducedTrades:
    n = len(df)
    return ReducedTrades(
        trade_id=np.arange(n, dtype=np.int64),
        asset=df["asset"].to_numpy(dtype=object),
        entry_date=np.asarray(df["entry_date"].tolist(), dtype=object),
        exit_date=np.asarray(df["exit_date"].tolist(), dtype=object),
        is_long=df["is_long"].to_numpy(dtype=bool),
        r_multiple=df["r_multiple"].to_numpy(dtype=np.float64),
        frozen_artifact_id=df["frozen_artifact_id"].to_numpy(dtype=object),
    )


def load_reduced_phase3b_pool(
    repo_root: str,
    dataset_hashes: Optional[Mapping[str, str]] = None,
    phase3b_paths: Optional[Mapping[str, str]] = None,
) -> ReducedTrades:
    """Load and verify the five Phase 3b CSVs and return the pooled reduced view.

    Verifies SHA-256 of every frozen input first; aborts on mismatch or any
    OOS 2023+ row.
    """
    verify_frozen_inputs(repo_root, dataset_hashes)
    paths = dict(phase3b_paths) if phase3b_paths is not None else dict(PHASE3B_DATASETS)
    frames = []
    for asset, rel_path in paths.items():
        frames.append(_load_one_csv(repo_root, rel_path, asset))
    pooled = pd.concat(frames, ignore_index=True)
    return _to_reduced(pooled)


def load_reduced_spy_base(
    repo_root: str,
    dataset_hashes: Optional[Mapping[str, str]] = None,
    spy_base_path: Optional[str] = None,
) -> ReducedTrades:
    """Load and verify the SPY 301-trade base population (secondary diagnostic)."""
    verify_frozen_inputs(repo_root, dataset_hashes)
    rel_path = spy_base_path if spy_base_path is not None else SPY_BASE_PATH
    df = _load_one_csv(repo_root, rel_path, SPY_BASE_ASSET)
    return _to_reduced(df)
