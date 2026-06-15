#!/usr/bin/env python3
"""
Gate 1 — CR EPISODE-COUNT AUDIT (feature-side only).

Authorized by docs/compression_cr_episode_count_audit_authorization_v0_1.md
(SHA-256 07db8c2ec4ad08fcff1a88d75f94c4e550bcbc3c03934cb1b62c2eb80e4e1299) and the
orientation memo docs/force_priority_fork_decision_memo_v0_1.md
(SHA-256 4630b329b499c95782370c67b3554bf6ab1b22083b0d6d29f71a89e85891cd10),
at HEAD = origin/main = 9d482ba477b0475f7a5dcb59b2806484517e7bae.

THIS IS NOT A WAKE TEST. NOT A PREDICTIVE TEST. NOT A GATE. It counts compression
(high-CI) episodes only. No wake/outcome/target is computed; no forward window is
used; no alpha is spent; no sealed (>= 2023-01-01) data is read.

================================================================================
STRUCTURAL FIREWALL (read before editing)
================================================================================
This audit constructs only feature-side fields, all from adjusted closes up to and
including row t (trailing windows only). The CR/CI construction is IMPORTED from the
reviewed Diagnostic-2 script (not retyped). It: defines no forward-window functions;
creates no wake/outcome/target columns; uses no negative shifts (a self-scan rejects
the negative-shift call pattern, assembled dynamically so the guard never self-matches);
asserts input columns are exactly {date, adj_close}; rejects any row >= 2023-01-01
(inherited from the imported construction); and self-scans its own source so no
function name and no constructed column name contains a forbidden token.
================================================================================
"""

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from collections import Counter

import numpy as np

# ----------------------------------------------------------------------------
# Frozen constants (authorization spec)
# ----------------------------------------------------------------------------
REPO_ROOT_EXPECTED = "/Users/jay/Documents/GitHub/coherent-numbers"
HEAD_EXPECTED = "9d482ba477b0475f7a5dcb59b2806484517e7bae"

AUTH_MEMO = "docs/compression_cr_episode_count_audit_authorization_v0_1.md"
AUTH_MEMO_SHA = "07db8c2ec4ad08fcff1a88d75f94c4e550bcbc3c03934cb1b62c2eb80e4e1299"
ORIENT_MEMO = "docs/force_priority_fork_decision_memo_v0_1.md"
ORIENT_MEMO_SHA = "4630b329b499c95782370c67b3554bf6ab1b22083b0d6d29f71a89e85891cd10"
DIAG2_SCRIPT = "scripts/run_compression_second_distinctness_diagnostic_v0_1.py"
DIAG2_SCRIPT_SHA = "d7e365dc9412c86680896ea3688c9d9f73c3d66ccd46feae7583388449312380"
CSV_PATH = "data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv"
CSV_SHA = "5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901"

REPORT_PATH = "docs/compression_cr_episode_count_audit_report_v0_1.md"

SEALED_BOUNDARY = "2023-01-01"
ALLOWED_INPUT_COLUMNS = {"date", "adj_close"}

W = 21                       # CR window length (closes)
MERGE_GAP = 20               # raw runs separated by <= 20 sessions merge into one episode
PERCENTILES = [85, 90, 95]
PRIMARY = 90
PCTL_METHOD = "linear"

FORBIDDEN_TOKENS = [
    "forward", "future", "wake", "outcome", "target", "drawdown",
    "recovery", "expansion", "lookahead", "_fwd", "fwd_", "lead_", "_ahead",
]

# This audit constructs NO new dataframe columns of its own; it reads only
# {date, adj_close, range_21, path_21, CI_21} from the imported construction.
CREATED_COLUMNS = []


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def halt(msg):
    print("AUDIT INVALID / HALTED: " + msg, file=sys.stderr)
    sys.exit(2)


def preflight_guards():
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip()
    if root != REPO_ROOT_EXPECTED:
        halt("repo root mismatch: %r" % root)
    branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
    if branch != "main":
        halt("branch not main: %r" % branch)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    if head != HEAD_EXPECTED:
        halt("HEAD mismatch: %r" % head)
    origin = subprocess.check_output(["git", "rev-parse", "origin/main"]).decode().strip()
    if origin != HEAD_EXPECTED:
        halt("origin/main mismatch: %r" % origin)
    if sha256_file(AUTH_MEMO) != AUTH_MEMO_SHA:
        halt("authorization memo SHA mismatch")
    if sha256_file(ORIENT_MEMO) != ORIENT_MEMO_SHA:
        halt("orientation memo SHA mismatch")
    if sha256_file(DIAG2_SCRIPT) != DIAG2_SCRIPT_SHA:
        halt("Diagnostic-2 script SHA mismatch")
    if sha256_file(CSV_PATH) != CSV_SHA:
        halt("sandbox CSV SHA mismatch")
    return {"repo_root": root, "branch": branch, "head": head, "origin_main": origin,
            "auth_memo_sha256": AUTH_MEMO_SHA, "orient_memo_sha256": ORIENT_MEMO_SHA,
            "diag2_script_sha256": DIAG2_SCRIPT_SHA, "csv_sha256": CSV_SHA}


def self_scan():
    with open(__file__, "r") as f:
        src = f.read()
    offenders = []
    for name in re.findall(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)", src, flags=re.MULTILINE):
        for tok in FORBIDDEN_TOKENS:
            if tok in name.lower():
                offenders.append(("func", name, tok))
    for col in CREATED_COLUMNS:
        for tok in FORBIDDEN_TOKENS:
            if tok in col.lower():
                offenders.append(("column", col, tok))
    neg_shift = ".shift(" + chr(45)          # assembled so this guard never self-matches
    if neg_shift in src:
        offenders.append(("pattern", "negative-shift", "negative-shift"))
    merge_needle = "mer" + "ge("             # assembled so this guard never self-matches
    how_needle = "ho" + "w="
    if merge_needle in src and how_needle in src:   # no forward merge in this audit
        offenders.append(("pattern", "merge", "merge"))
    return offenders


def import_cr_construction():
    spec = importlib.util.spec_from_file_location("diag2_cr_construction", DIAG2_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # defines constants + functions; main() is guarded, not run
    return mod


def maximal_runs(bool_arr):
    """Maximal consecutive runs of True over the contiguous session index."""
    runs = []
    n = len(bool_arr)
    i = 0
    while i < n:
        if bool_arr[i]:
            j = i
            while j + 1 < n and bool_arr[j + 1]:
                j += 1
            runs.append((i, j))
            i = j + 1
        else:
            i += 1
    return runs


def merge_runs(runs, gap_max):
    """Merge raw runs whose gap_sessions = next_start - prev_end - 1 <= gap_max."""
    if not runs:
        return []
    eps = [list(runs[0])]
    for (s, e) in runs[1:]:
        ps, pe = eps[-1]
        gap_sessions = s - pe - 1
        if gap_sessions <= gap_max:
            eps[-1][1] = e
        else:
            eps.append([s, e])
    return [tuple(x) for x in eps]


def episode_anchor(df, s, e):
    """Date inside [s,e] with max CI_21; tie-break earliest date. Returns (idx, date, ci)."""
    sub = df.iloc[s:e + 1]
    ci = sub["CI_21"]
    mx = ci.max()                          # NaN-skipping
    cand = sub[ci == mx].sort_values("date")
    pos = int(cand.index[0])               # df index == contiguous session index
    return pos, df.loc[pos, "date"], float(mx)


def count_density_tier(n):
    if n < 30:
        return "COUNT-INFEASIBLE FOR A FUTURE WAKE DESIGN"
    if n < 60:
        return "SPARSE; FUTURE WAKE DESIGN NOT RECOMMENDED WITHOUT EXTRA JUSTIFICATION"
    return "COUNT-DENSITY ADEQUATE TO REVISIT, NOT AN AUTHORIZATION"


def main():
    guards = preflight_guards()
    offenders = self_scan()
    if offenders:
        halt("firewall/self-scan failed: %r" % offenders)

    mod = import_cr_construction()
    if not hasattr(mod, "CSV_PATH"):
        halt("imported module has no CSV_PATH")
    imported_csv_path = mod.CSV_PATH
    resolved_csv_path = os.path.abspath(imported_csv_path)
    if not os.path.exists(resolved_csv_path):
        halt("resolved imported CSV_PATH does not exist: %r" % resolved_csv_path)
    resolved_csv_sha = sha256_file(resolved_csv_path)
    print("imported module path : %s" % os.path.abspath(mod.__file__))
    print("imported function    : %s" % mod.build_features.__name__)
    print("imported CSV_PATH     : %s" % imported_csv_path)
    print("resolved CSV_PATH     : %s" % resolved_csv_path)
    print("resolved CSV_PATH sha : %s" % resolved_csv_sha)
    if resolved_csv_sha != CSV_SHA:
        halt("resolved imported CSV_PATH hash != authorized sandbox SHA")

    construction_fn = mod.build_features    # the actual imported function object
    df = construction_fn()                  # constructs CI_21, range_21, path_21 (trailing only)

    # firewall: no constructed column may carry a forbidden token
    bad_cols = [c for c in df.columns for t in FORBIDDEN_TOKENS if t in str(c).lower()]
    if bad_cols:
        halt("forbidden token in constructed columns: %r" % bad_cols)
    if set(df.columns) - {"date", "adj_close", "absdiff", "range_21", "path_21", "CR_21",
                          "CI_21", "net_disp_21", "ER_21", "LOG_TORT_21", "d_first_21",
                          "KATZ_FD_FIRST_21", "RANGE_PATH_ROUGHNESS_21", "KATZ_FD_RANGE_21"}:
        halt("unexpected constructed columns: %r" % list(df.columns))

    # df is date-sorted and reset_index(drop=True): its index IS the contiguous session index.
    input_rows = int(len(df))
    date_min, date_max = df["date"].min(), df["date"].max()
    cols_ok = (set(["date", "adj_close"]).issubset(set(df.columns)))
    no_2023 = bool((df["date"] < SEALED_BOUNDARY).all())
    if not no_2023:
        halt("sealed-period (2023+) row present in constructed table")

    rng = df["range_21"]
    pth = df["path_21"]
    ci = df["CI_21"]

    warmup_mask = rng.isna() | pth.isna()
    after_warmup = ~warmup_mask
    path_nonpos = after_warmup & (pth <= 0)
    range_nonpos = after_warmup & ~path_nonpos & (rng <= 0)
    ci_nonfinite = after_warmup & ~path_nonpos & ~range_nonpos & ~np.isfinite(ci)
    valid_mask = after_warmup & (pth > 0) & (rng > 0) & np.isfinite(ci)

    n_warmup = int(warmup_mask.sum())
    n_path = int(path_nonpos.sum())
    n_range = int(range_nonpos.sum())
    n_nonfin = int(ci_nonfinite.sum())
    n_valid = int(valid_mask.sum())
    n_other = input_rows - n_warmup - n_path - n_range - n_nonfin - n_valid

    valid_vals = ci[valid_mask].to_numpy(float)
    valid_idx = np.flatnonzero(valid_mask.to_numpy())
    first_valid_idx = int(valid_idx.min())
    last_valid_idx = int(valid_idx.max())

    thresholds = {p: float(np.percentile(valid_vals, p, method=PCTL_METHOD)) for p in PERCENTILES}

    valid_bool = valid_mask.to_numpy()
    ci_np = ci.to_numpy(float)

    grid = {}
    for p in PERCENTILES:
        thr = thresholds[p]
        eligible = valid_bool & (ci_np >= thr)
        raw_runs = maximal_runs(eligible)
        episodes = merge_runs(raw_runs, MERGE_GAP)
        grid[p] = {
            "threshold": thr,
            "eligible_days": int(eligible.sum()),
            "raw_runs": len(raw_runs),
            "episodes": len(episodes),
            "episode_spans": episodes,
        }

    # ----- primary (90th) detail -----
    prim = grid[PRIMARY]
    prim_eps = prim["episode_spans"]
    anchors = []
    for (s, e) in prim_eps:
        pos, adate, aci = episode_anchor(df, s, e)
        duration = e - s + 1
        boundary = (s <= first_valid_idx <= e) or (s <= last_valid_idx <= e)
        anchors.append({"start_idx": s, "end_idx": e, "anchor_idx": pos,
                        "anchor_date": adate, "anchor_ci": aci,
                        "duration_sessions": int(duration),
                        "boundary_truncated": bool(boundary)})

    anchor_idxs = [a["anchor_idx"] for a in anchors]
    anchor_dates = [a["anchor_date"] for a in anchors]
    durations = [a["duration_sessions"] for a in anchors]
    n_boundary = int(sum(1 for a in anchors if a["boundary_truncated"]))

    per_year = dict(sorted(Counter(d[:4] for d in anchor_dates).items()))

    spacings = [anchor_idxs[i + 1] - anchor_idxs[i] for i in range(len(anchor_idxs) - 1)]
    if spacings:
        sp_min, sp_med, sp_max = int(min(spacings)), float(np.median(spacings)), int(max(spacings))
    else:
        sp_min, sp_med, sp_max = None, None, None

    invariant_ok = True if not spacings else (min(spacings) >= 21)

    prim_tier = count_density_tier(prim["episodes"]) if invariant_ok else "N/A (invariant failed)"
    grid_tiers = {p: count_density_tier(grid[p]["episodes"]) for p in PERCENTILES}
    tiers_differ = len(set(grid_tiers.values())) > 1

    summary = {
        "guards": guards,
        "imported_module_path": os.path.abspath(mod.__file__),
        "imported_function": mod.build_features.__name__,
        "imported_csv_path": imported_csv_path,
        "resolved_csv_path": resolved_csv_path,
        "resolved_csv_sha256": resolved_csv_sha,
        "resolved_equals_authorized": resolved_csv_sha == CSV_SHA,
        "input_rows": input_rows, "date_min": date_min, "date_max": date_max,
        "allowed_columns_ok": cols_ok, "no_2023_rows": no_2023,
        "valid_ci_rows": n_valid,
        "dropped": {"warmup": n_warmup, "path_le_0": n_path, "range_le_0": n_range,
                    "ci_nonfinite": n_nonfin, "other": n_other},
        "percentile_method": PCTL_METHOD,
        "thresholds": thresholds,
        "grid": {p: {k: v for k, v in grid[p].items() if k != "episode_spans"} for p in PERCENTILES},
        "primary_percentile": PRIMARY,
        "primary_anchors": anchors,
        "per_year": per_year,
        "anchor_spacing": {"min": sp_min, "median": sp_med, "max": sp_max},
        "boundary_truncated_episodes": n_boundary,
        "invariant_anchors_ge_21": bool(invariant_ok),
        "first_valid_idx": first_valid_idx, "last_valid_idx": last_valid_idx,
        "primary_tier": prim_tier, "grid_tiers": grid_tiers, "tiers_differ": tiers_differ,
        "self_scan_offenders": offenders,
    }
    print("===CRAUDIT_JSON_BEGIN===")
    print(json.dumps(summary, indent=2))
    print("===CRAUDIT_JSON_END===")

    if not invariant_ok:
        # methodological failure: report and do NOT assign a count-density tier
        write_report(summary, invariant_failed=True)
        halt("derived invariant failed: final anchors not all >= 21 sessions apart")

    write_report(summary, invariant_failed=False)


def write_report(s, invariant_failed):
    g = s["guards"]
    thr = s["thresholds"]
    grid = s["grid"]

    grid_rows = "\n".join(
        "| %dth | %.6f | %d | %d | %d | %s |" % (
            p, grid[p]["threshold"], grid[p]["eligible_days"], grid[p]["raw_runs"],
            grid[p]["episodes"], s["grid_tiers"][p])
        for p in PERCENTILES)

    anchor_rows = "\n".join(
        "| %d | %s | %.6f | %d | %d | %s |" % (
            i + 1, a["anchor_date"], a["anchor_ci"], a["duration_sessions"],
            a["anchor_idx"], "yes" if a["boundary_truncated"] else "no")
        for i, a in enumerate(s["primary_anchors"]))

    year_rows = "\n".join("| %s | %d |" % (y, c) for y, c in s["per_year"].items())

    sp = s["anchor_spacing"]
    sp_line = ("min %s / median %s / max %s sessions" % (sp["min"], sp["median"], sp["max"])
               if sp["min"] is not None else "n/a (fewer than 2 episodes)")

    dr = s["dropped"]
    tier_line = s["primary_tier"]
    fragile = ("**FRAGILE / BORDERLINE** — the count-density tier differs across the 85/90/95 grid."
               if s["tiers_differ"] else
               "Not fragile — the count-density tier is consistent across the 85/90/95 grid.")
    inv_line = ("FAILED — final anchors are NOT all >= 21 sessions apart; "
                "methodological failure, no count-density tier assigned."
                if invariant_failed else
                "PASS — all final episode anchors are >= 21 trading sessions apart.")

    report = """# Compression Lane — CR Episode-Count Audit Report v0.1

**Gate 1 — feature-side only.** Counts compression (high-CI) episodes under the frozen design. **NOT a wake test, NOT a predictive test, NOT a gate.** No wake/outcome/target was computed; no forward window was used; no alpha was spent; no sealed (>= 2023-01-01) data was accessed; no predictive claim is made. **This audit does not authorize Gate 2.**

Authorized by `%(auth_memo)s` (SHA-256 `%(auth_sha)s`) and the orientation memo `%(orient_memo)s` (SHA-256 `%(orient_sha)s`).

## 1. Commit / HEAD / origin verification
- repo root: `%(repo_root)s`
- branch: `%(branch)s`
- HEAD: `%(head)s`
- origin/main: `%(origin)s`

## 2. Governing-record SHA verification
- authorization memo `%(auth_memo)s` = `%(auth_sha)s` (matches frozen spec)
- orientation memo `%(orient_memo)s` = `%(orient_sha)s` (matches frozen spec)
- Diagnostic-2 construction script `%(diag2_script)s` = `%(diag2_sha)s` (matches frozen spec)
- sandbox input (direct hash) `%(csv_path)s` = `%(csv_sha)s` (verified before reading rows)

## 3. Imported CR construction (not retyped)
- imported module path: `%(imp_path)s`
- imported function object: `%(imp_fn)s`
- imported module `CSV_PATH`: `%(imp_csv)s`
- resolved imported module `CSV_PATH`: `%(res_csv)s`
- SHA-256 of resolved imported `CSV_PATH`: `%(res_sha)s`
- resolved imported `CSV_PATH` hash equals the authorized sandbox SHA: **%(res_eq)s**

CR/CI are constructed by the imported function object `%(imp_fn)s` exactly as committed:
`path_21 = sum |adj_close_i - adj_close_{i-1}|` over the 20 trailing intervals;
`range_21 = max(adj_close) - min(adj_close)` over trailing [t-20..t];
`CR_21 = range_21 / path_21`; `CI_21 = -log(CR_21) = log(path_21 / range_21)`.
This audit uses only `CI_21` for counting.

## 4. Input
- input rows: %(input_rows)d
- input date range: `%(date_min)s` .. `%(date_max)s`
- allowed columns exactly {`date`, `adj_close`}: **%(cols_ok)s**
- no rows on/after `2023-01-01`: **%(no2023)s**

## 5. Valid-CI rows and dropped-row decomposition
- valid-CI rows (full trailing 21-close window, `path_21 > 0`, `range_21 > 0`, finite `CI_21`): **%(valid)d**
- dropped — warmup / no full trailing 21-close window: %(d_warm)d
- dropped — `path_21 <= 0`: %(d_path)d
- dropped — `range_21 <= 0`: %(d_range)d
- dropped — nonfinite `CI_21`: %(d_nonfin)d
- dropped — other: %(d_other)d

This audit is CI-only: rows are NOT dropped because `ER_21`, `LOG_TORT_21`, `KATZ_FD_FIRST_21`, or endpoint displacement are invalid. The two `net_disp_21 == 0` rows dropped in Diagnostic 2 remain CI-valid here.

## 6. Thresholds
- numpy percentile method: `%(pctl)s`
- 85th percentile CI_21 = %(t85).6f
- 90th percentile CI_21 = %(t90).6f  **(primary)**
- 95th percentile CI_21 = %(t95).6f

Thresholds were not tuned after seeing counts.

## 7. Eligibility / raw runs / merged episodes (per threshold)
Eligible day: `CI_21 >= threshold` (inclusive). Eligible runs separated by `<= 20` trading sessions (`gap_sessions = next_start_idx - prev_end_idx - 1`) merge into one episode (window length 21 ⇒ days within 20 sessions have overlapping CR windows). Boundary-truncated runs are retained.

| percentile | threshold CI_21 | eligible days | raw runs | merged episodes | tier |
|------------|-----------------|---------------|----------|-----------------|------|
%(grid_rows)s

## 8. Primary (90th-percentile) episodes
Episode anchor = date of maximum `CI_21` inside the merged cluster (tie-break: earliest date). Duration = sessions from cluster start through end inclusive.

| # | anchor date | anchor CI_21 | duration (sessions) | anchor session idx | boundary-truncated |
|---|-------------|--------------|---------------------|--------------------|--------------------|
%(anchor_rows)s

- primary merged episode count: **%(prim_eps)d**
- boundary-truncated episodes: %(n_boundary)d
- anchor spacing (primary): %(sp_line)s

### Per-year episode counts (primary 90th)
| year | episodes |
|------|----------|
%(year_rows)s

## 9. Derived invariant
- final episode anchors at least 21 trading sessions apart: **%(inv_line)s**

## 10. Count-density tier (primary 90th only)
- primary merged episode count = %(prim_eps)d
- **count-density tier: %(tier_line)s**
- %(fragile)s

Frozen tier labels: `N_episodes < 30` → COUNT-INFEASIBLE FOR A FUTURE WAKE DESIGN; `30 <= N < 60` → SPARSE; FUTURE WAKE DESIGN NOT RECOMMENDED WITHOUT EXTRA JUSTIFICATION; `N >= 60` → COUNT-DENSITY ADEQUATE TO REVISIT, NOT AN AUTHORIZATION. Even the top tier does not authorize wake, prediction, gate, alpha, sealed data, or atlas promotion.

## 11. Structural firewall proof
- CR/CI construction IMPORTED from the reviewed Diagnostic-2 script (actual function object), not retyped;
- imported module `CSV_PATH` re-resolved and re-hashed to the authorized sandbox SHA before any row read;
- input columns asserted exactly {`date`, `adj_close`} (inherited from the imported construction);
- zero rows on/after `2023-01-01` (inherited sealed-boundary guard + re-checked here);
- no forward-window function defined; no wake/outcome/target column constructed (constructed columns checked against an allow-list and a forbidden-token scan);
- no negative (future) shift call present in source; no forward merge present;
- self-scan over this script's own function names and constructed column names: **%(selfscan)s**.

## 12. Self-scan result
- %(selfscan)s

## 13. Explicit boundary statements
- No wake/outcome/target was computed.
- No forward window was used (anchors are not used to index any post-t value).
- No gate was run.
- No alpha was spent.
- No sealed (>= 2023-01-01) data was accessed.
- No predictive claim was made.
- This audit does NOT authorize Gate 2 (wake-design authorization), which requires Gate 1 clearing with adequate episode density AND separate authorization.
""" % {
        "auth_memo": AUTH_MEMO, "auth_sha": g["auth_memo_sha256"],
        "orient_memo": ORIENT_MEMO, "orient_sha": g["orient_memo_sha256"],
        "diag2_script": DIAG2_SCRIPT, "diag2_sha": g["diag2_script_sha256"],
        "csv_path": CSV_PATH, "csv_sha": g["csv_sha256"],
        "repo_root": g["repo_root"], "branch": g["branch"], "head": g["head"], "origin": g["origin_main"],
        "imp_path": s["imported_module_path"], "imp_fn": s["imported_function"],
        "imp_csv": s["imported_csv_path"], "res_csv": s["resolved_csv_path"],
        "res_sha": s["resolved_csv_sha256"], "res_eq": s["resolved_equals_authorized"],
        "input_rows": s["input_rows"], "date_min": s["date_min"], "date_max": s["date_max"],
        "cols_ok": s["allowed_columns_ok"], "no2023": s["no_2023_rows"],
        "valid": s["valid_ci_rows"], "d_warm": s["dropped"]["warmup"], "d_path": s["dropped"]["path_le_0"],
        "d_range": s["dropped"]["range_le_0"], "d_nonfin": s["dropped"]["ci_nonfinite"],
        "d_other": s["dropped"]["other"], "pctl": s["percentile_method"],
        "t85": thr[85], "t90": thr[90], "t95": thr[95],
        "grid_rows": grid_rows, "anchor_rows": anchor_rows,
        "prim_eps": grid[PRIMARY]["episodes"], "n_boundary": s["boundary_truncated_episodes"],
        "sp_line": sp_line, "year_rows": year_rows, "inv_line": inv_line,
        "tier_line": tier_line, "fragile": fragile,
        "selfscan": "PASS (no offenders)" if not s["self_scan_offenders"] else repr(s["self_scan_offenders"]),
    }
    with open(REPORT_PATH, "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()
