"""Spec-conformance tests for the trade-level field-modulated identity study.

Synthetic in-memory fixtures only. No real-data contact. Maps to the locked
memo docs/influential_numbers_field_modulated_identity_trade_level_scoping_study_v0.1.md
(committed 8d4bd1d). Each test names the memo section it pins.
"""

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

import field_modulated_identity_trade_level as fmi  # noqa: E402
import synthetic_conformance_field_modulated_identity_trade_level as harness  # noqa: E402


@pytest.fixture(scope="module")
def synth():
    return harness.make_synthetic_trades(n=1282, seed=999)


# ── Schema / canonical pooled ordering (§G) ──────────────────────────────────

def test_missing_columns_rejected():
    bad = pd.DataFrame({"asset": ["SPY"], "entry_date": ["2005-01-03"]})
    with pytest.raises(ValueError):
        fmi.canonical_pooled_frame(bad)


def test_unknown_asset_rejected(synth):
    df = synth.copy()
    df.loc[0, "asset"] = "QQQ"
    with pytest.raises(ValueError):
        fmi.canonical_pooled_frame(df)


def test_pooled_stream_ordered_by_entry_date_deterministic(synth):
    a = fmi.canonical_pooled_frame(synth)
    b = fmi.canonical_pooled_frame(synth.sample(frac=1, random_state=7))
    assert a["entry_date"].is_monotonic_increasing
    # tie-break makes ordering a pure function of input content
    pd.testing.assert_frame_equal(
        a.drop(columns=["_input_order", "_asset_rank"]),
        b.drop(columns=["_input_order", "_asset_rank"]))


# ── Warmup exclusions (§G / §P-9) ────────────────────────────────────────────

@pytest.mark.parametrize("n,expect_drop", [(20, 20), (10, 10), (40, 40)])
def test_warmup_exclusion(synth, n, expect_drop):
    r = fmi.run_protocol(synth, n_window=n)
    assert r["n_warmup_dropped"] == expect_drop
    assert r["n_modeling_rows"] == len(synth) - expect_drop \
        - r["n_undefined_window_dropped"]


def test_primary_is_N20(synth):
    full = fmi.run_full_study(synth)
    assert full["primary_N20"]["n_window"] == 20
    assert full["primary_N20"]["is_primary"] is True
    assert set(full["supplementary_non_primary"]) == {"N=10", "N=40"}
    for k in ("N=10", "N=40"):
        assert full["supplementary_non_primary"][k]["is_primary"] is False


# ── Model set + 21 interactions + feature-matrix shapes (§H / §P-5) ──────────

def test_model_set_exact(synth):
    r = fmi.run_protocol(synth)
    assert tuple(r["models"]) == ("M0", "M1", "M1L", "M2", "M3a", "M3b")


def test_interaction_count_is_21(synth):
    assert fmi.N_INTERACTIONS == 21
    assert fmi.run_protocol(synth)["n_interactions"] == 21


def test_feature_matrix_widths(synth):
    frame = fmi.canonical_pooled_frame(synth).iloc[20:].reset_index(drop=True)
    ctx = fmi.build_context_block(
        fmi.canonical_pooled_frame(synth), 20).iloc[20:].reset_index(drop=True)
    base = fmi.base_feature_frame(frame)
    tr = np.arange(0, 400)
    va = np.arange(400, 520)
    widths = {}
    for m in ("M1", "M1L", "M2", "M3a", "M3b"):
        mats = fmi._assemble(frame, base, ctx, tr, va, m, fmi.MASTER_SEED)
        assert mats["tr"].shape[1] == mats["va"].shape[1]
        widths[m] = mats["tr"].shape[1]
    assert widths["M1"] == 3                       # direction, init_risk, logEP
    assert widths["M1L"] > widths["M1"]            # + asset/dow/month dummies
    assert widths["M2"] == widths["M1L"] + 7 + 21  # context + interactions
    # equal-structure control rule: M2/M3a/M3b identical width (§H)
    assert widths["M2"] == widths["M3a"] == widths["M3b"]


def test_interactions_are_identity_times_context(synth):
    frame = fmi.canonical_pooled_frame(synth).iloc[20:].reset_index(drop=True)
    ctx = fmi.build_context_block(
        fmi.canonical_pooled_frame(synth), 20).iloc[20:].reset_index(drop=True)
    base = fmi.base_feature_frame(frame)
    tr = np.arange(0, 400)
    va = np.arange(400, 520)
    m2 = fmi._assemble(frame, base, ctx, tr, va, "M2", fmi.MASTER_SEED)
    w_m1l = fmi._assemble(frame, base, ctx, tr, va, "M1L",
                          fmi.MASTER_SEED)["tr"].shape[1]
    ident = m2["tr"][:, [0, 1, 2]]                 # direction, init_risk, logEP
    ctx_z = m2["tr"][:, w_m1l:w_m1l + 7]
    inter = m2["tr"][:, w_m1l + 7:w_m1l + 7 + 21]
    expected = fmi._interactions(ident, ctx_z)
    np.testing.assert_allclose(inter, expected, rtol=0, atol=0)


# ── Leakage guards (§E / §G window leakage lock) ─────────────────────────────

def test_leakage_columns_never_features():
    # the locked leakage set is explicit and not in any feature name list
    for c in fmi.LEAKAGE_COLUMNS:
        assert c not in fmi.CONTEXT_COLS
        assert c not in fmi.IDENTITY_INTERACTION_COLS
    base_cols = set(fmi.base_feature_frame(
        fmi.canonical_pooled_frame(harness.make_synthetic_trades(60))
    ).columns)
    # only identity + private helper cols; no outcome-side leakage column
    assert base_cols.isdisjoint(set(fmi.LEAKAGE_COLUMNS))


def test_resolved_before_entry_constraint():
    # focal trade index 3 entry 2005-02-01. Prior trades:
    #  0: exit 2005-01-10 (resolved, R=+2) -> counts
    #  1: exit 2005-01-20 (resolved, R=-1) -> counts
    #  2: exit 2005-03-01 (NOT resolved before focal entry) -> excluded
    df = pd.DataFrame({
        "asset": ["SPY"] * 5,
        "entry_date": pd.to_datetime(
            ["2005-01-02", "2005-01-05", "2005-01-09",
             "2005-02-01", "2005-02-10"]),
        "setup_date": pd.to_datetime(
            ["2005-01-01"] * 5),
        "direction": ["long", "short", "long", "long", "short"],
        "entry_price": [100.0] * 5,
        "exit_price": [101.0] * 5,
        "exit_date": pd.to_datetime(
            ["2005-01-10", "2005-01-20", "2005-03-01",
             "2005-02-05", "2005-02-15"]),
        "exit_reason": ["stop"] * 5,
        "bars_held": [5] * 5,
        "r_multiple": [2.0, -1.0, 9.0, 0.5, 0.5],
        "first_target_hit": [True] * 5,
        "initial_risk": [1.0] * 5,
    })
    frame = fmi.canonical_pooled_frame(df)
    ctx = fmi.build_context_block(frame, n_window=20)
    # focal index 3: resolved priors are rows 0 and 1 only (row 2 exits later)
    assert ctx["ctx_recent_mean_R"].iloc[3] == pytest.approx((2.0 + -1.0) / 2)
    assert ctx["ctx_recent_win_rate"].iloc[3] == pytest.approx(0.5)
    # the unresolved big-R trade (R=9) must NOT leak in
    assert ctx["ctx_recent_mean_R"].iloc[3] != pytest.approx(
        (2.0 - 1.0 + 9.0) / 3)


# ── Forward-chaining CV + purge (§I) ─────────────────────────────────────────

def test_forward_chaining_expanding_and_purge(synth):
    r = fmi.run_protocol(synth)
    fm = r["fold_meta"]
    assert len(fm) == 5
    pre = [f["n_train_pre_purge"] for f in fm]
    assert pre == sorted(pre) and len(set(pre)) == 5      # strictly expanding
    for f in fm:
        assert f["n_train_post_purge"] <= f["n_train_pre_purge"]  # purge only
        assert f["n_val"] >= fmi.MIN_VAL_BLOCK_ROWS


def test_split_helper_shapes():
    sp = fmi._forward_chaining_splits(120, 5)
    assert len(sp) == 5
    for k in range(1, len(sp)):
        assert len(sp[k][0]) > len(sp[k - 1][0])          # expanding train
        assert sp[k][0][0] == 0                             # always from start
    assert sp[-1][1][-1] == 119                             # remainder absorbed
    assert fmi._forward_chaining_splits(3, 5) == []         # too small


# ── M0 baseline / pooled-residual R² (§I-B1) ─────────────────────────────────

def test_m0_oos_r2_is_zero(synth):
    r = fmi.run_protocol(synth)
    assert not r["degenerate"]
    assert r["aggregate_oos_r2"]["M0"] == pytest.approx(0.0, abs=1e-12)


# ── Success/failure logic (§I) ───────────────────────────────────────────────

def test_beats_aggregate_absolute_floor():
    # comp <= 0 -> relative term undefined, absolute 0.01 governs
    assert fmi._beats_aggregate(0.011, 0.0) is True
    assert fmi._beats_aggregate(0.009, 0.0) is False
    # comp<0: relative term -> 0, absolute floor governs the required margin
    assert fmi._beats_aggregate(0.005, -0.01) is True      # +0.015 >= 0.01
    assert fmi._beats_aggregate(-0.004, -0.01) is False    # +0.006 < 0.01


def test_beats_aggregate_relative_margin():
    # comp=0.10 -> required=max(0.01, 0.20*0.10=0.02)=0.02
    assert fmi._beats_aggregate(0.119, 0.10) is False      # +0.019 < 0.02
    assert fmi._beats_aggregate(0.121, 0.10) is True       # +0.021 >= 0.02


def test_classify_success_path():
    agg = {"M0": 0.0, "M1": 0.0, "M1L": 0.05,
           "M2": 0.10, "M3a": 0.05, "M3b": 0.05}
    fold = {"M0": [0] * 5, "M1": [0] * 5, "M1L": [0.04] * 5,
            "M2": [0.09] * 5, "M3a": [0.04] * 5, "M3b": [0.04] * 5}
    v = fmi._classify(agg, fold, degenerate=False)
    assert v["primary_success"] is True
    assert v["interpretation"] == "i_field_modulated_supported"


def test_classify_expanded_identity_only():
    agg = {"M0": 0.0, "M1": 0.0, "M1L": 0.05,
           "M2": 0.051, "M3a": 0.05, "M3b": 0.05}
    fold = {m: [0.0] * 5 for m in fmi.MODELS}
    v = fmi._classify(agg, fold, degenerate=False)
    assert v["primary_success"] is False
    assert v["interpretation"] == "ii_expanded_identity_only"


def test_classify_no_field_evidence():
    agg = {"M0": 0.0, "M1": 0.02, "M1L": 0.01,
           "M2": 0.011, "M3a": 0.01, "M3b": 0.01}
    fold = {m: [0.0] * 5 for m in fmi.MODELS}
    v = fmi._classify(agg, fold, degenerate=False)
    assert v["interpretation"] == "iii_no_field_evidence"


def test_classify_degenerate_routes_iv():
    v = fmi._classify({}, {}, degenerate=True)
    assert v["interpretation"] == "iv_non_confirmatory_degenerate"
    assert v["primary_success"] is False


def test_fold_win_threshold_requires_4_of_5():
    agg = {"M0": 0.0, "M1": 0.0, "M1L": 0.05,
           "M2": 0.10, "M3a": 0.05, "M3b": 0.05}
    # M2 beats M1L in only 3/5 folds -> fails fold-win gate despite aggregate
    fold = {"M0": [0] * 5, "M1": [0] * 5,
            "M1L": [0.0, 0.0, 0.2, 0.2, 0.0],
            "M2": [0.09, 0.09, 0.09, 0.09, 0.09],
            "M3a": [0.0] * 5, "M3b": [0.0] * 5}
    v = fmi._classify(agg, fold, degenerate=False)
    assert v["fold_wins"]["M1L"] == 3
    assert v["primary_success"] is False


# ── M3a / M3b construction (§I-B4 / §I-B5) ───────────────────────────────────

def test_m3a_permutes_context_but_keeps_structure(synth):
    frame = fmi.canonical_pooled_frame(synth).iloc[20:].reset_index(drop=True)
    ctx = fmi.build_context_block(
        fmi.canonical_pooled_frame(synth), 20).iloc[20:].reset_index(drop=True)
    base = fmi.base_feature_frame(frame)
    tr = np.arange(0, 400)
    va = np.arange(400, 520)
    m2 = fmi._assemble(frame, base, ctx, tr, va, "M2", fmi.MASTER_SEED)
    m3a = fmi._assemble(frame, base, ctx, tr, va, "M3a", fmi.MASTER_SEED)
    assert m2["tr"].shape == m3a["tr"].shape          # identical structure
    # identity columns unchanged; context block permuted -> differs
    np.testing.assert_allclose(m2["tr"][:, :3], m3a["tr"][:, :3])
    w_m1l = fmi._assemble(frame, base, ctx, tr, va, "M1L",
                          fmi.MASTER_SEED)["tr"].shape[1]
    assert not np.allclose(m2["tr"][:, w_m1l:w_m1l + 7],
                           m3a["tr"][:, w_m1l:w_m1l + 7])
    # M3a context is a row permutation of M2 context (same multiset of rows)
    a = np.sort(m2["tr"][:, w_m1l:w_m1l + 7], axis=0)
    b = np.sort(m3a["tr"][:, w_m1l:w_m1l + 7], axis=0)
    np.testing.assert_allclose(a, b, rtol=1e-9, atol=1e-9)


def test_m3b_gaussian_context_shape_and_seed(synth):
    frame = fmi.canonical_pooled_frame(synth).iloc[20:].reset_index(drop=True)
    ctx = fmi.build_context_block(
        fmi.canonical_pooled_frame(synth), 20).iloc[20:].reset_index(drop=True)
    base = fmi.base_feature_frame(frame)
    tr = np.arange(0, 400)
    va = np.arange(400, 520)
    b1 = fmi._assemble(frame, base, ctx, tr, va, "M3b", fmi.MASTER_SEED)
    b2 = fmi._assemble(frame, base, ctx, tr, va, "M3b", fmi.MASTER_SEED)
    m2 = fmi._assemble(frame, base, ctx, tr, va, "M2", fmi.MASTER_SEED)
    assert b1["tr"].shape == m2["tr"].shape
    np.testing.assert_allclose(b1["tr"], b2["tr"])        # seed-deterministic
    w_m1l = fmi._assemble(frame, base, ctx, tr, va, "M1L",
                          fmi.MASTER_SEED)["tr"].shape[1]
    gauss = b1["tr"][:, w_m1l:w_m1l + 7]
    assert abs(gauss.mean()) < 0.25                        # ~N(0,1)
    assert 0.7 < gauss.std() < 1.3


# ── Determinism + degeneracy guard (§I / §P-6) ───────────────────────────────

def test_full_study_deterministic(synth):
    a = fmi.run_full_study(synth)
    b = fmi.run_full_study(synth.copy())
    assert (a["primary_N20"]["aggregate_oos_r2"]
            == b["primary_N20"]["aggregate_oos_r2"])
    assert (a["primary_N20"]["fold_oos_r2"]
            == b["primary_N20"]["fold_oos_r2"])


def test_degeneracy_guard_small_sample():
    tiny = harness.make_synthetic_trades(n=30, seed=1)
    r = fmi.run_protocol(tiny, n_window=20)
    assert r["degenerate"] is True
    assert r["verdict"]["interpretation"] == "iv_non_confirmatory_degenerate"
    assert r["verdict"]["primary_success"] is False


def _make_field_modulated_signal(n=1500, seed=4242):
    """SYNTHETIC positive control. Baked-in field-modulated identity effect:
    Y is driven ONLY by the interaction of an identity feature (initial_risk)
    with a context feature (time-since-prior-trade), with no main effects.

    Construction: stream gaps alternate in 60-trade blocks between 1 and 8
    days, so ``ctx_time_since_prior_trade`` is a clean 2-level block signal
    that no identity / asset / calendar column can reconstruct. r_multiple is
    set so that log1p(abs(r)) == eta == mu + beta*(IR-IRbar)*(gap-gapbar).
    Pure interaction => M1/M1L (no context) and M3a/M3b (broken/random
    context) cannot fit it; only M2 can. No real data.
    """
    rs = np.random.RandomState(seed)
    block = 60
    gap = np.where(((np.arange(n) // block) % 2) == 0, 1, 8).astype(int)
    entry = np.datetime64("2005-01-03") + np.cumsum(gap).astype(
        "timedelta64[D]")
    initial_risk = rs.uniform(0.5, 5.0, size=n)
    ir_bar = initial_risk.mean()
    gap_bar = gap.mean()
    mu, beta = 1.0, 0.05
    eta = mu + beta * (initial_risk - ir_bar) * (gap - gap_bar) \
        + rs.normal(0.0, 0.01, size=n)
    eta = np.maximum(eta, 1e-6)
    r_multiple = np.expm1(eta)  # => log1p(abs(r)) == eta exactly
    bars_held = rs.randint(1, 10, size=n)
    return pd.DataFrame({
        "asset": rs.choice(list(fmi.ASSET_LEVELS), size=n),
        "entry_date": entry,
        "setup_date": entry - np.timedelta64(1, "D"),
        "direction": rs.choice(["long", "short"], size=n),
        "entry_price": np.round(rs.uniform(20, 400, size=n), 4),
        "exit_price": np.round(rs.uniform(20, 400, size=n), 4),
        "exit_date": entry + bars_held.astype("timedelta64[D]"),
        "exit_reason": rs.choice(["stop", "target"], size=n),
        "bars_held": bars_held,
        "r_multiple": r_multiple,
        "first_target_hit": rs.choice([True, False], size=n),
        "initial_risk": initial_risk,
    })


def test_positive_control_field_modulated_signal_detected():
    """Guards against false-negative implementation bugs: with a real
    identity×context effect baked in, M2 must beat M1L/M3a/M3b under the
    locked §I criterion and route to interpretation cell (i)."""
    df = _make_field_modulated_signal()
    r = fmi.run_protocol(df, n_window=20)
    assert r["degenerate"] is False
    agg = r["aggregate_oos_r2"]
    # M2 must clear the locked aggregate margin vs each comparator
    for c in fmi.COMPARATORS:
        assert fmi._beats_aggregate(agg["M2"], agg[c]), \
            "M2 (%.4f) failed locked margin vs %s (%.4f)" % (
                agg["M2"], c, agg[c])
    v = r["verdict"]
    assert all(v["fold_wins"][c] >= fmi.FOLD_WIN_MIN
               for c in fmi.COMPARATORS), v["fold_wins"]
    assert v["primary_success"] is True
    assert v["interpretation"] == "i_field_modulated_supported"


def test_degeneracy_guard_small_val_block():
    # ~360 rows -> 5-split block ~60 > 50 ok; shrink so val block < 50
    small = harness.make_synthetic_trades(n=290, seed=2)
    r = fmi.run_protocol(small, n_window=20)
    # modeling ~270, block ~ 270//6 = 45 < 50 -> degeneracy guard trips
    assert r["degenerate"] is True
    assert r["verdict"]["primary_success"] is False
