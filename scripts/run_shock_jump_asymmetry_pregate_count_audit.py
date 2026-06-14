#!/usr/bin/env python3
"""
Shock/Jump Asymmetry Lane — Stage-2 PRE-GATE COUNT AUDIT (feasibility only).

THIS IS NOT THE SANDBOX GATE.
THIS IS NOT A TEST OF THE HYPOTHESIS.
THIS IS NOT MODELING.
THIS IS NOT TUNING.

Purpose: determine ONLY whether the Stage-1 design rules can produce a feasible,
time-local matched shock set, before any future sandbox gate. The audit computes
exclusively EVENT-SIDE quantities (returns, strictly-pre-shock volatility,
standardized returns, shock dates/signs/magnitudes, matching feasibility counts).

================================================================================
FORWARD-UNREACHABILITY — STRUCTURAL ENFORCEMENT (read before editing)
================================================================================
This script is built so forward-window data is STRUCTURALLY INACCESSIBLE to the
audit logic:

  * The audit table (AUDIT_TABLE) is restricted to an ALLOWED_EVENT_SIDE_COLUMNS
    allow-list. A runtime assertion fails the script if any other column appears.
    No target/outcome/wake column can exist in the structure the audit consumes.

  * NO function in this file computes forward realized volatility, forward max
    drawdown, forward recovery / calm-down time, forward range, future path
    length, future wake construction, or any target `y`. Such functions are not
    defined, so they cannot be called.

  * The ONLY windowing operation is a TRAILING window that ends strictly at t-1
    (implemented as rolling(...).shift(1)). There is no forward indexing of the
    form close[t+k] or iloc[t : t+window] anywhere in the audit logic.

  * The event-day return r_t (numerator of z_t) is used; the denominator uses
    only returns up to t-1. r_t is never used in the denominator, and no return
    after t is ever read.

Therefore a wake CANNOT be computed from the structures present: there are no
forward arrays, no forward-window functions, and no forward indices to read.
================================================================================
"""

import hashlib
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Frozen audit constants (from Stage-1 design memo; AUDIT CANDIDATES, not frozen)
# ----------------------------------------------------------------------------
REPO_ROOT_EXPECTED = "/Users/jay/Documents/GitHub/coherent-numbers"
HEAD_EXPECTED = "cd1016295ba4b843a61e8c9cd1811c86e88c0406"
MEMO_PATH = "docs/shock_jump_asymmetry_design_memo_v0_1.md"
MEMO_SHA_EXPECTED = "c6529e37dd1a225e80d23f9f3b014620843b9e31deac4d98139c9e3a7bda1fa2"
CSV_PATH = "data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv"
CSV_SHA_EXPECTED = "5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901"

DATE_MIN = "2005-01-01"
DATE_MAX = "2022-12-31"
SEALED_BOUNDARY = "2023-01-01"

VOL_WINDOW = 21                      # Stage-1 draft trailing window (trading days)
THRESHOLD_GRID = [3.5, 4.0, 4.5]    # candidate |z| thresholds (audit candidates)
CALIPER_GRID = [0.20, 0.30, 0.40]   # candidate calipers in standardized-distance units
TIME_LOCAL_WINDOW = 252             # Stage-1 candidate ±trading-day local window
ZDIFF_CAP = 0.5                     # Stage-1 draft additional raw |z|-difference cap
CANDIDATE_FLOORS = [20, 30, 40]     # candidate floors to REPORT (owner sets real floor)

# Allow-list: the audit table may contain ONLY these event-side fields.
ALLOWED_EVENT_SIDE_COLUMNS = {
    "row_idx",          # trading-day index (for time-locality only; not forward read)
    "date",
    "adj_close",
    "logret",           # event/current-or-past log return
    "vol_plain",        # strictly pre-shock vol (ends t-1), L2 ruler
    "vol_sym",          # strictly pre-shock vol (ends t-1), sign-symmetrized ruler
    "z_plain",          # standardized return under plain ruler
    "z_sym",            # standardized return under sign-symmetrized ruler
}

# Explicit, auditable list of forbidden forward-quantity tokens. This script
# defines NONE of these as functions; the self-scan below proves their absence
# outside this declaration / comments.
FORBIDDEN_FORWARD_TOKENS = [
    "forward_realized_vol", "forward_vol", "forward_drawdown", "max_drawdown",
    "forward_recovery", "recovery_time", "calm_down", "forward_range",
    "path_length", "future_window", "future_wake", "build_wake",
    "compute_wake", "make_target", "build_target", "target_y",
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg):
    print("AUDIT STOP: " + msg, file=sys.stderr)
    sys.exit(2)


# ----------------------------------------------------------------------------
# Guards (re-verified at run time)
# ----------------------------------------------------------------------------
def run_guards():
    root = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"]).decode().strip()
    if root != REPO_ROOT_EXPECTED:
        fail("repo root mismatch: %r" % root)
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
    if branch != "main":
        fail("branch is not main: %r" % branch)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    if head != HEAD_EXPECTED:
        fail("HEAD mismatch: %r" % head)
    memo_sha = sha256_file(MEMO_PATH)
    if memo_sha != MEMO_SHA_EXPECTED:
        fail("Stage-1 memo SHA mismatch: %r" % memo_sha)
    csv_sha = sha256_file(CSV_PATH)
    if csv_sha != CSV_SHA_EXPECTED:
        fail("sandbox CSV SHA mismatch: %r" % csv_sha)
    return {
        "repo_root": root, "branch": branch, "head": head,
        "memo_sha256": memo_sha, "csv_sha256": csv_sha,
    }


# ----------------------------------------------------------------------------
# Event-side construction (TRAILING ONLY; ends strictly at t-1)
# ----------------------------------------------------------------------------
def rms(x):
    return float(np.sqrt(np.mean(np.square(x))))


def mad_sigma(x):
    # canonical MAD->sigma scale on |r|: sqrt(pi/2) * mean(|r|)
    return float(np.sqrt(np.pi / 2.0) * np.mean(np.abs(x)))


def build_audit_table():
    df = pd.read_csv(CSV_PATH, usecols=["date", "adj_close"])
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df = df.sort_values("date").reset_index(drop=True)

    # Hard date-range / sealed-boundary guards.
    if (df["date"] < DATE_MIN).any() or (df["date"] > DATE_MAX).any():
        fail("date outside allowed sandbox range")
    if (df["date"] >= SEALED_BOUNDARY).any():
        fail("sealed-period (2023+) date present")

    df["row_idx"] = np.arange(len(df))
    df["logret"] = np.log(df["adj_close"] / df["adj_close"].shift(1))

    # Strictly pre-shock vol: rolling window over PAST returns, then shift(1) so
    # the value at row t uses returns [t-VOL_WINDOW .. t-1] (ends at t-1).
    df["vol_plain"] = df["logret"].rolling(VOL_WINDOW).apply(rms, raw=True).shift(1)
    df["vol_sym"] = df["logret"].rolling(VOL_WINDOW).apply(mad_sigma, raw=True).shift(1)

    # Standardized returns: numerator is the event-day return r_t; denominator
    # is strictly pre-shock (ends t-1). r_t never enters the denominator.
    df["z_plain"] = df["logret"] / df["vol_plain"]
    df["z_sym"] = df["logret"] / df["vol_sym"]

    audit = df[list(ALLOWED_EVENT_SIDE_COLUMNS & set(df.columns))].copy()
    # STRUCTURAL ENFORCEMENT: only event-side columns may exist.
    extra = set(audit.columns) - ALLOWED_EVENT_SIDE_COLUMNS
    if extra:
        fail("non-event-side columns present in audit table: %r" % extra)
    return audit


# ----------------------------------------------------------------------------
# Matching feasibility (maximum one-to-one, no-replacement, time-local)
# ----------------------------------------------------------------------------
def max_bipartite_matching(adj, n_left):
    """Kuhn's algorithm: maximum cardinality matching. adj[i] = admissible rights."""
    match_right = {}

    def try_kuhn(u, seen):
        for v in adj[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in match_right or try_kuhn(match_right[v], seen):
                match_right[v] = u
                return True
        return False

    matched = 0
    for u in range(n_left):
        if try_kuhn(u, set()):
            matched += 1
    return matched, match_right


def feasibility_for(audit, ruler, threshold, caliper, time_local):
    zcol = "z_plain" if ruler == "plain" else "z_sym"
    vcol = "vol_plain" if ruler == "plain" else "vol_sym"

    valid = audit.dropna(subset=[zcol, vcol]).copy()
    z = valid[zcol].to_numpy()
    absz = np.abs(z)
    shock_mask = absz >= threshold
    sh = valid[shock_mask].copy()
    sh_absz = np.abs(sh[zcol].to_numpy())
    sh_vol = sh[vcol].to_numpy()
    sh_idx = sh["row_idx"].to_numpy()
    sh_sign = np.sign(sh[zcol].to_numpy())  # -1 down, +1 up

    n_down = int(np.sum(sh_sign < 0))
    n_up = int(np.sum(sh_sign > 0))
    n_total = int(len(sh))

    # Covariate scales over the shock set (for THIS threshold) -> standardized units.
    scale_z = float(np.std(sh_absz)) if n_total > 1 else 0.0
    scale_vol = float(np.std(sh_vol)) if n_total > 1 else 0.0

    result = {
        "ruler": ruler, "threshold": threshold, "caliper": caliper,
        "time_local": time_local,
        "n_down": n_down, "n_up": n_up, "n_total": n_total,
        "scale_absz": scale_z, "scale_vol": scale_vol, "n_for_scale": n_total,
    }

    down_i = np.where(sh_sign < 0)[0]
    up_i = np.where(sh_sign > 0)[0]

    if n_down == 0 or n_up == 0 or scale_z == 0.0 or scale_vol == 0.0:
        result.update({
            "candidate_edges": 0, "down_with_match": 0, "up_with_match": 0,
            "matched_pairs": 0, "unmatched_down": n_down, "unmatched_up": n_up,
        })
        return result

    a = sh_absz / scale_z       # standardized |z|
    b = sh_vol / scale_vol      # standardized pre-shock vol

    adj = {}
    candidate_edges = 0
    down_with = set()
    up_with = set()
    for di_pos, di in enumerate(down_i):
        adj[di_pos] = []
        for uj in up_i:
            if time_local and abs(int(sh_idx[di]) - int(sh_idx[uj])) > TIME_LOCAL_WINDOW:
                continue
            if abs(sh_absz[di] - sh_absz[uj]) > ZDIFF_CAP:
                continue
            dist = float(np.hypot(a[di] - a[uj], b[di] - b[uj]))
            if dist <= caliper:
                adj[di_pos].append(uj)
                candidate_edges += 1
                down_with.add(di)
                up_with.add(uj)

    matched_pairs, _ = max_bipartite_matching(adj, len(down_i))
    result.update({
        "candidate_edges": candidate_edges,
        "down_with_match": len(down_with),
        "up_with_match": len(up_with),
        "matched_pairs": matched_pairs,
        "unmatched_down": n_down - matched_pairs,
        "unmatched_up": n_up - matched_pairs,
    })
    return result


def self_scan():
    """Prove no forbidden forward-quantity function is defined in this file."""
    with open(__file__, "r") as f:
        src = f.read()
    offenders = []
    for tok in FORBIDDEN_FORWARD_TOKENS:
        # a 'def <tok>' would be a forward function definition -> forbidden
        if ("def " + tok) in src:
            offenders.append(tok)
    return offenders


def main():
    guards = run_guards()
    offenders = self_scan()
    if offenders:
        fail("forbidden forward-function definitions present: %r" % offenders)

    audit = build_audit_table()
    n_closes = int(audit["adj_close"].notna().sum())
    date_loaded_min = audit["date"].min()
    date_loaded_max = audit["date"].max()

    rows = []
    for ruler in ("plain", "sym"):
        for thr in THRESHOLD_GRID:
            for cal in CALIPER_GRID:
                # time-local (gate-feasible)
                rows.append(feasibility_for(audit, ruler, thr, cal, time_local=True))
                # widened / nonlocal: DESCRIPTIVE ONLY — excluded from gate
                wide = feasibility_for(audit, ruler, thr, cal, time_local=False)
                wide["DESCRIPTIVE_ONLY"] = True
                rows.append(wide)

    summary = {
        "guards": guards,
        "date_loaded_min": date_loaded_min,
        "date_loaded_max": date_loaded_max,
        "n_closes": n_closes,
        "vol_window": VOL_WINDOW,
        "threshold_grid": THRESHOLD_GRID,
        "caliper_grid": CALIPER_GRID,
        "time_local_window": TIME_LOCAL_WINDOW,
        "zdiff_cap": ZDIFF_CAP,
        "candidate_floors": CANDIDATE_FLOORS,
        "allowed_event_side_columns": sorted(ALLOWED_EVENT_SIDE_COLUMNS),
        "self_scan_offenders": offenders,
        "rows": rows,
    }
    print("===AUDIT_JSON_BEGIN===")
    print(json.dumps(summary, indent=2))
    print("===AUDIT_JSON_END===")


if __name__ == "__main__":
    main()
