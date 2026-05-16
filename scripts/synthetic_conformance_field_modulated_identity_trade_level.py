"""Synthetic conformance harness — trade-level field-modulated identity study.

SYNTHETIC ONLY. This script never reads the frozen substrate, never reads any
file, and never touches the network. It fabricates an in-memory DataFrame with
the *same column structure* as the frozen Phase 3b trade table, runs the locked
protocol, and prints structural conformance evidence (shapes, interaction
count, model set, fold structure, warmup exclusions, determinism).

It produces NO observed real-data result and NO verdict on the real substrate.
Running the one-time real-data verdict is a separately gated step and is NOT
implemented anywhere in this codebase.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

import field_modulated_identity_trade_level as fmi  # noqa: E402

SYNTHETIC_SEED = 12345  # harness-only; unrelated to the locked MASTER_SEED


def make_synthetic_trades(n: int = 1282, seed: int = SYNTHETIC_SEED
                          ) -> pd.DataFrame:
    """Fabricate trades with the exact frozen-substrate column structure.

    Column set and dtypes mirror data/raw/pullback_phase3b_*_trades_2005_2022.csv
    plus the pooled-stream ``asset`` tag. Values are random; there is no signal
    designed in and no real data involved.
    """
    rs = np.random.RandomState(seed)
    assets = np.array(fmi.ASSET_LEVELS)
    asset = rs.choice(assets, size=n)
    start = np.datetime64("2005-01-03")
    # entry dates: cumulative business-ish gaps over ~2005-2022
    gaps = rs.randint(1, 9, size=n)
    entry = start + np.cumsum(gaps).astype("timedelta64[D]")
    setup = entry - rs.randint(1, 6, size=n).astype("timedelta64[D]")
    bars_held = rs.randint(1, 30, size=n)
    exit_dt = entry + bars_held.astype("timedelta64[D]")
    direction = rs.choice(["long", "short"], size=n)
    entry_price = np.round(rs.uniform(20, 400, size=n), 4)
    r_multiple = rs.normal(0.0, 1.2, size=n)
    exit_price = entry_price * (1.0 + rs.normal(0, 0.05, size=n))
    return pd.DataFrame({
        "asset": asset,
        "entry_date": entry,
        "setup_date": setup,
        "direction": direction,
        "entry_price": entry_price,
        "exit_price": np.round(exit_price, 4),
        "exit_date": exit_dt,
        "exit_reason": rs.choice(["stop", "time_stop", "target"], size=n),
        "bars_held": bars_held,
        "r_multiple": r_multiple,
        "first_target_hit": rs.choice([True, False], size=n),
        "initial_risk": np.round(rs.uniform(0.5, 5.0, size=n), 6),
    })


def main() -> None:
    print("=== SYNTHETIC conformance harness (NO real data) ===")
    df = make_synthetic_trades()
    print("synthetic frame: %d rows, columns=%s"
          % (len(df), list(df.columns)))

    res = fmi.run_full_study(df)
    p = res["primary_N20"]

    print("\n-- primary N=20 structural evidence --")
    print("input rows:            ", p["n_input_rows"])
    print("warmup dropped:        ", p["n_warmup_dropped"], "(expect 20)")
    print("undefined-window drop: ", p["n_undefined_window_dropped"])
    print("modeling rows:         ", p["n_modeling_rows"])
    print("n_interactions:        ", p["n_interactions"], "(expect 21)")
    print("context cols (%d):     " % len(p["context_cols"]),
          p["context_cols"])
    print("models:                ", p["models"])
    print("folds:                 ", len(p["fold_meta"]),
          "(expect 5 forward-chaining)")
    for fm in p["fold_meta"]:
        print("   fold %d: train_pre=%d train_post_purge=%d val=%d"
              % (fm["fold"], fm["n_train_pre_purge"],
                 fm["n_train_post_purge"], fm["n_val"]))
    print("degenerate:            ", p["degenerate"])
    print("aggregate OOS R²:      ",
          {k: round(v, 6) for k, v in p["aggregate_oos_r2"].items()}
          if not p["degenerate"] else "n/a (degenerate)")
    print("verdict:               ", p["verdict"])

    print("\n-- supplementary (non-primary) --")
    for k, sup in res["supplementary_non_primary"].items():
        print("  %s: warmup=%d modeling=%d interp=%s"
              % (k, sup["n_warmup_dropped"], sup["n_modeling_rows"],
                 sup["verdict"]["interpretation"]))

    print("\n-- determinism check (same input+seed -> identical output) --")
    res_b = fmi.run_full_study(make_synthetic_trades())
    same = (res["primary_N20"]["aggregate_oos_r2"]
            == res_b["primary_N20"]["aggregate_oos_r2"]
            and res["primary_N20"]["fold_oos_r2"]
            == res_b["primary_N20"]["fold_oos_r2"])
    print("deterministic:         ", same)

    print("\n=== NO real substrate contacted. NO verdict produced on real "
          "data. Code is ready for review only. ===")


if __name__ == "__main__":
    main()
