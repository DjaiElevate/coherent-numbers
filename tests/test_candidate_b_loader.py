"""Tests for the frozen-CSV hash verification and reduced-row loader.

All tests use synthetic CSVs in tmp_path. The real frozen pullback CSVs in
data/raw/ are never loaded by any test in this module.
"""

import hashlib
import os
from datetime import date

import numpy as np
import pandas as pd
import pytest

from candidate_b_loader import (
    FROZEN_DATASETS,
    FrozenCsvHashMismatch,
    OosRowDetected,
    ReducedTrades,
    _file_sha256,
    load_reduced_phase3b_pool,
    load_reduced_spy_base,
    verify_frozen_inputs,
)


PHASE3B_HEADER = (
    "entry_date,setup_date,direction,entry_price,exit_price,exit_date,"
    "exit_reason,bars_held,r_multiple,first_target_hit,initial_risk"
)


def _phase3b_row(entry, exit_, direction, r_multiple=1.0):
    return (
        "{entry},{entry},{dir},100,110,{exit},target,5,{r},True,1.0".format(
            entry=entry, dir=direction, exit=exit_, r=r_multiple
        )
    )


def _write_phase3b_csv(path, rows):
    content_lines = [PHASE3B_HEADER]
    content_lines.extend(rows)
    text = "\n".join(content_lines) + "\n"
    path.write_text(text)
    return text


def _sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _setup_tmp_repo_with_csvs(tmp_path):
    """Create a synthetic repo layout with three Phase 3b CSVs of two trades each."""
    raw = tmp_path / "data" / "raw"
    raw.mkdir(parents=True)

    files = {
        "SYN1": ("data/raw/syn1.csv", raw / "syn1.csv"),
        "SYN2": ("data/raw/syn2.csv", raw / "syn2.csv"),
        "SYN3": ("data/raw/syn3.csv", raw / "syn3.csv"),
    }
    hashes = {}
    paths = {}
    rows_per_file = {
        "SYN1": [
            _phase3b_row("2010-03-21", "2010-03-25", "long", 1.5),
            _phase3b_row("2011-06-15", "2011-06-20", "short", -0.5),
        ],
        "SYN2": [
            _phase3b_row("2012-09-10", "2012-09-12", "long", 0.8),
            _phase3b_row("2013-01-05", "2013-01-10", "short", -1.2),
        ],
        "SYN3": [
            _phase3b_row("2014-12-30", "2014-12-31", "long", 2.0),
            _phase3b_row("2015-02-14", "2015-02-20", "short", 0.3),
        ],
    }
    for asset, (rel, full) in files.items():
        text = _write_phase3b_csv(full, rows_per_file[asset])
        hashes[rel] = _sha256_text(text)
        paths[asset] = rel
    return str(tmp_path), hashes, paths


def test_file_sha256_matches_python_hashlib(tmp_path):
    f = tmp_path / "x.bin"
    payload = b"hello\nworld\n"
    f.write_bytes(payload)
    expected = hashlib.sha256(payload).hexdigest()
    assert _file_sha256(str(f)) == expected


def test_verify_frozen_inputs_succeeds_on_match(tmp_path):
    repo_root, hashes, _ = _setup_tmp_repo_with_csvs(tmp_path)
    observed = verify_frozen_inputs(repo_root, dataset_hashes=hashes)
    assert observed == hashes


def test_verify_frozen_inputs_raises_on_mismatch(tmp_path):
    repo_root, hashes, _ = _setup_tmp_repo_with_csvs(tmp_path)
    tampered = dict(hashes)
    first_key = next(iter(tampered))
    tampered[first_key] = "0" * 64
    with pytest.raises(FrozenCsvHashMismatch):
        verify_frozen_inputs(repo_root, dataset_hashes=tampered)


def test_verify_frozen_inputs_raises_on_missing_file(tmp_path):
    hashes = {"data/raw/does_not_exist.csv": "0" * 64}
    with pytest.raises(FrozenCsvHashMismatch):
        verify_frozen_inputs(str(tmp_path), dataset_hashes=hashes)


def test_load_reduced_phase3b_pool_returns_reduced_trades(tmp_path):
    repo_root, hashes, paths = _setup_tmp_repo_with_csvs(tmp_path)
    reduced = load_reduced_phase3b_pool(
        repo_root,
        dataset_hashes=hashes,
        phase3b_paths=paths,
    )
    assert isinstance(reduced, ReducedTrades)
    assert len(reduced) == 6
    for field in ("trade_id", "asset", "entry_date", "exit_date",
                   "is_long", "r_multiple", "frozen_artifact_id"):
        assert getattr(reduced, field).shape[0] == 6
    assert reduced.is_long.dtype == np.bool_
    assert reduced.r_multiple.dtype == np.float64
    # Asset labels are SYN1/SYN2/SYN3
    assert set(reduced.asset.tolist()) == {"SYN1", "SYN2", "SYN3"}


def test_load_reduced_phase3b_dates_are_python_date(tmp_path):
    repo_root, hashes, paths = _setup_tmp_repo_with_csvs(tmp_path)
    reduced = load_reduced_phase3b_pool(repo_root, dataset_hashes=hashes, phase3b_paths=paths)
    for d in reduced.entry_date:
        assert isinstance(d, date)


def test_load_aborts_on_oos_2023_row(tmp_path):
    raw = tmp_path / "data" / "raw"
    raw.mkdir(parents=True)
    csv_path = raw / "with_oos.csv"
    rows = [
        _phase3b_row("2022-12-15", "2022-12-20", "long", 1.0),
        _phase3b_row("2023-01-15", "2023-01-20", "long", 1.0),  # OOS
    ]
    text = _write_phase3b_csv(csv_path, rows)
    sha = _sha256_text(text)
    hashes = {"data/raw/with_oos.csv": sha}
    paths = {"OOS": "data/raw/with_oos.csv"}
    with pytest.raises(OosRowDetected):
        load_reduced_phase3b_pool(str(tmp_path), dataset_hashes=hashes, phase3b_paths=paths)


def test_load_aborts_on_missing_required_column(tmp_path):
    raw = tmp_path / "data" / "raw"
    raw.mkdir(parents=True)
    csv_path = raw / "broken.csv"
    # Missing 'direction' column
    text = "entry_date,exit_date,r_multiple\n2010-03-21,2010-03-25,1.0\n"
    csv_path.write_text(text)
    sha = _sha256_text(text)
    hashes = {"data/raw/broken.csv": sha}
    paths = {"BAD": "data/raw/broken.csv"}
    with pytest.raises(ValueError):
        load_reduced_phase3b_pool(str(tmp_path), dataset_hashes=hashes, phase3b_paths=paths)


def test_load_handles_short_string_direction(tmp_path):
    raw = tmp_path / "data" / "raw"
    raw.mkdir(parents=True)
    csv_path = raw / "syn.csv"
    rows = [
        _phase3b_row("2010-03-21", "2010-03-25", "long", 1.0),
        _phase3b_row("2010-04-21", "2010-04-25", "short", -0.5),
    ]
    text = _write_phase3b_csv(csv_path, rows)
    sha = _sha256_text(text)
    reduced = load_reduced_phase3b_pool(
        str(tmp_path),
        dataset_hashes={"data/raw/syn.csv": sha},
        phase3b_paths={"X": "data/raw/syn.csv"},
    )
    assert reduced.is_long.tolist() == [True, False]


def test_frozen_datasets_constant_has_six_entries():
    assert len(FROZEN_DATASETS) == 6
    for sha in FROZEN_DATASETS.values():
        assert len(sha) == 64
        int(sha, 16)  # must be valid hex


def test_load_reduced_spy_base_uses_synthetic_repo(tmp_path):
    raw = tmp_path / "data" / "raw"
    raw.mkdir(parents=True)
    csv_path = raw / "spy_base.csv"
    rows = [
        _phase3b_row("2005-03-21", "2005-03-25", "long", 1.0),
        _phase3b_row("2006-05-15", "2006-05-18", "short", -0.5),
    ]
    text = _write_phase3b_csv(csv_path, rows)
    sha = _sha256_text(text)
    reduced = load_reduced_spy_base(
        str(tmp_path),
        dataset_hashes={"data/raw/spy_base.csv": sha},
        spy_base_path="data/raw/spy_base.csv",
    )
    assert len(reduced) == 2
    assert set(reduced.asset.tolist()) == {"SPY"}
