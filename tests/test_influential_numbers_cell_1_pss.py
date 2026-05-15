"""Tests for the Influential Numbers Cell 1 PSS.

Mirrors tests/test_candidate_c_pss.py (commit 4432591). Includes a strict
source-text parity test asserting the pss_long_share arithmetic body is
byte-identical to src/candidate_c_pss.py (only the module docstring may
differ), because the design memo section 17 provenance gate depends on
reproducing Candidate C's k=10 / k=12 surfaces at max_abs_diff <= 1e-12.
"""

import os
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

import influential_numbers_cell_1_pss as pss

CELL1_PSS_FILE = os.path.join(
    REPO_ROOT, "src", "influential_numbers_cell_1_pss.py"
)
CANDIDATE_C_PSS_FILE = os.path.join(
    REPO_ROOT, "src", "candidate_c_pss.py"
)


# ── Public surface ───────────────────────────────────────────────────────────

def test_public_surface_present():
    assert issubclass(pss.DegenerateLongShareError, RuntimeError)
    assert callable(pss.pss_long_share)
    assert callable(pss._coerce_bool_array)
    assert callable(pss._coerce_phase_array)


def test_no_r_multiple_pss_function():
    bad = [n for n in dir(pss) if "r_multiple" in n or "rmultiple" in n]
    assert bad == []


def test_n_phases_required_no_default():
    with pytest.raises(TypeError):
        pss.pss_long_share([True, False], [0, 1])  # noqa


# ── Behaviour ────────────────────────────────────────────────────────────────

def test_max_separation_returns_one():
    # phase fully predicts is_long -> eta-squared == 1.0
    is_long = np.array([True, True, False, False])
    phase = np.array([0, 0, 1, 1])
    assert pss.pss_long_share(is_long, phase, 2) == pytest.approx(1.0)


def test_no_separation_returns_zero():
    # Genuine no-separation: every phase has the same long share (0.5), so
    # eta-squared is exactly 0.0. (The previous [0,1,0,1] fixture made phase
    # perfectly predict direction -> that is maximum separation, not none.)
    is_long = np.array([True, False, True, False])
    phase = np.array([0, 0, 1, 1])
    assert pss.pss_long_share(is_long, phase, 2) == pytest.approx(0.0)


def test_all_long_aborts():
    with pytest.raises(pss.DegenerateLongShareError):
        pss.pss_long_share(np.array([True, True, True]), np.array([0, 1, 2]), 3)


def test_all_short_aborts():
    with pytest.raises(pss.DegenerateLongShareError):
        pss.pss_long_share(
            np.array([False, False, False]), np.array([0, 1, 2]), 3
        )


def test_empty_phase_contributes_zero():
    # phase 2 has no trades; must not raise, must not contribute.
    is_long = np.array([True, True, False, False])
    phase = np.array([0, 0, 1, 1])
    val = pss.pss_long_share(is_long, phase, 3)  # n_phases 3, phase 2 empty
    assert val == pytest.approx(1.0)


@pytest.mark.parametrize("seed", [1, 2, 3, 7])
def test_bounds_in_unit_interval(seed):
    rng = np.random.Generator(np.random.PCG64(seed))
    is_long = rng.integers(0, 2, size=120).astype(bool)
    is_long[0], is_long[1] = True, False
    phase = rng.integers(0, 12, size=120)
    v = pss.pss_long_share(is_long, phase, 12)
    assert 0.0 <= v <= 1.0


def test_hand_micro_fixture():
    # 4 trades, 2 phases. share_pooled = 2/4 = 0.5; total_k = 0.25
    # phase0: longs 2/2 = 1.0 ; phase1: longs 0/2 = 0.0
    # between = 0.5*(1-0.5)^2 + 0.5*(0-0.5)^2 = 0.25 ; pss = 0.25/0.25 = 1.0
    is_long = np.array([True, True, False, False])
    phase = np.array([0, 0, 1, 1])
    assert pss.pss_long_share(is_long, phase, 2) == pytest.approx(1.0)


def test_shape_mismatch_rejected():
    with pytest.raises(ValueError):
        pss.pss_long_share(np.array([True, False, True]), np.array([0, 1]), 2)


def test_empty_input_rejected():
    with pytest.raises(ValueError):
        pss.pss_long_share(np.array([], dtype=bool),
                           np.array([], dtype=np.int64), 2)


def test_phase_out_of_range_rejected():
    with pytest.raises(ValueError):
        pss.pss_long_share(np.array([True, False]), np.array([0, 5]), 2)


def test_rank_invariance_under_phase_preserving_relabel():
    rng = np.random.Generator(np.random.PCG64(99))
    is_long = rng.integers(0, 2, size=90).astype(bool)
    is_long[0], is_long[1] = True, False
    phase = rng.integers(0, 6, size=90)
    base = pss.pss_long_share(is_long, phase, 6)
    relabel = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1, 5: 0}
    phase2 = np.array([relabel[p] for p in phase])
    assert pss.pss_long_share(is_long, phase2, 6) == pytest.approx(base)


# ── Strict source-text parity with Candidate C ───────────────────────────────

def _code_after_module_docstring(path):
    txt = open(path, encoding="utf-8").read().split("\n")
    assert txt[0].startswith('"""'), path
    for i in range(1, len(txt)):
        if txt[i].rstrip() == '"""':
            return "\n".join(txt[i + 1:])
    raise AssertionError("no closing module docstring in " + path)


def test_pss_body_bit_identical_to_candidate_c():
    cell1 = _code_after_module_docstring(CELL1_PSS_FILE)
    cand_c = _code_after_module_docstring(CANDIDATE_C_PSS_FILE)
    assert cell1 == cand_c, (
        "pss_long_share arithmetic body must be byte-identical to "
        "src/candidate_c_pss.py (only the module docstring may differ); "
        "the section 17 provenance gate depends on this parity"
    )


def test_cell1_pss_module_has_no_percent_character():
    # Same discipline as the lens; keeps the surface comparison clean.
    assert "%" not in open(CELL1_PSS_FILE, encoding="utf-8").read()
