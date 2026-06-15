# Compression Lane — CR Episode-Count Audit Report v0.1

**Gate 1 — feature-side only.** Counts compression (high-CI) episodes under the frozen design. **NOT a wake test, NOT a predictive test, NOT a gate.** No wake/outcome/target was computed; no forward window was used; no alpha was spent; no sealed (>= 2023-01-01) data was accessed; no predictive claim is made. **This audit does not authorize Gate 2.**

Authorized by `docs/compression_cr_episode_count_audit_authorization_v0_1.md` (SHA-256 `07db8c2ec4ad08fcff1a88d75f94c4e550bcbc3c03934cb1b62c2eb80e4e1299`) and the orientation memo `docs/force_priority_fork_decision_memo_v0_1.md` (SHA-256 `4630b329b499c95782370c67b3554bf6ab1b22083b0d6d29f71a89e85891cd10`).

## 1. Commit / HEAD / origin verification
- repo root: `/Users/jay/Documents/GitHub/coherent-numbers`
- branch: `main`
- HEAD: `9d482ba477b0475f7a5dcb59b2806484517e7bae`
- origin/main: `9d482ba477b0475f7a5dcb59b2806484517e7bae`

## 2. Governing-record SHA verification
- authorization memo `docs/compression_cr_episode_count_audit_authorization_v0_1.md` = `07db8c2ec4ad08fcff1a88d75f94c4e550bcbc3c03934cb1b62c2eb80e4e1299` (matches frozen spec)
- orientation memo `docs/force_priority_fork_decision_memo_v0_1.md` = `4630b329b499c95782370c67b3554bf6ab1b22083b0d6d29f71a89e85891cd10` (matches frozen spec)
- Diagnostic-2 construction script `scripts/run_compression_second_distinctness_diagnostic_v0_1.py` = `d7e365dc9412c86680896ea3688c9d9f73c3d66ccd46feae7583388449312380` (matches frozen spec)
- sandbox input (direct hash) `data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv` = `5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901` (verified before reading rows)

## 3. Imported CR construction (not retyped)
- imported module path: `/Users/jay/Documents/GitHub/coherent-numbers/scripts/run_compression_second_distinctness_diagnostic_v0_1.py`
- imported function object: `build_features`
- imported module `CSV_PATH`: `data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv`
- resolved imported module `CSV_PATH`: `/Users/jay/Documents/GitHub/coherent-numbers/data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv`
- SHA-256 of resolved imported `CSV_PATH`: `5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901`
- resolved imported `CSV_PATH` hash equals the authorized sandbox SHA: **True**

CR/CI are constructed by the imported function object `build_features` exactly as committed:
`path_21 = sum |adj_close_i - adj_close_{i-1}|` over the 20 trailing intervals;
`range_21 = max(adj_close) - min(adj_close)` over trailing [t-20..t];
`CR_21 = range_21 / path_21`; `CI_21 = -log(CR_21) = log(path_21 / range_21)`.
This audit uses only `CI_21` for counting.

## 4. Input
- input rows: 4531
- input date range: `2005-01-03` .. `2022-12-30`
- allowed columns exactly {`date`, `adj_close`}: **True**
- no rows on/after `2023-01-01`: **True**

## 5. Valid-CI rows and dropped-row decomposition
- valid-CI rows (full trailing 21-close window, `path_21 > 0`, `range_21 > 0`, finite `CI_21`): **4511**
- dropped — warmup / no full trailing 21-close window: 20
- dropped — `path_21 <= 0`: 0
- dropped — `range_21 <= 0`: 0
- dropped — nonfinite `CI_21`: 0
- dropped — other: 0

This audit is CI-only: rows are NOT dropped because `ER_21`, `LOG_TORT_21`, `KATZ_FD_FIRST_21`, or endpoint displacement are invalid. The two `net_disp_21 == 0` rows dropped in Diagnostic 2 remain CI-valid here.

## 6. Thresholds
- numpy percentile method: `linear`
- 85th percentile CI_21 = 1.310883
- 90th percentile CI_21 = 1.378064  **(primary)**
- 95th percentile CI_21 = 1.475100

Thresholds were not tuned after seeing counts.

## 7. Eligibility / raw runs / merged episodes (per threshold)
Eligible day: `CI_21 >= threshold` (inclusive). Eligible runs separated by `<= 20` trading sessions (`gap_sessions = next_start_idx - prev_end_idx - 1`) merge into one episode (window length 21 ⇒ days within 20 sessions have overlapping CR windows). Boundary-truncated runs are retained.

| percentile | threshold CI_21 | eligible days | raw runs | merged episodes | tier |
|------------|-----------------|---------------|----------|-----------------|------|
| 85th | 1.310883 | 677 | 136 | 68 | COUNT-DENSITY ADEQUATE TO REVISIT, NOT AN AUTHORIZATION |
| 90th | 1.378064 | 452 | 111 | 64 | COUNT-DENSITY ADEQUATE TO REVISIT, NOT AN AUTHORIZATION |
| 95th | 1.475100 | 226 | 73 | 52 | SPARSE; FUTURE WAKE DESIGN NOT RECOMMENDED WITHOUT EXTRA JUSTIFICATION |

## 8. Primary (90th-percentile) episodes
Episode anchor = date of maximum `CI_21` inside the merged cluster (tie-break: earliest date). Duration = sessions from cluster start through end inclusive.

| # | anchor date | anchor CI_21 | duration (sessions) | anchor session idx | boundary-truncated |
|---|-------------|--------------|---------------------|--------------------|--------------------|
| 1 | 2005-03-02 | 1.480651 | 21 | 40 | no |
| 2 | 2005-05-11 | 1.540457 | 6 | 89 | no |
| 3 | 2005-07-08 | 1.448238 | 1 | 129 | no |
| 4 | 2005-08-16 | 1.578668 | 20 | 156 | no |
| 5 | 2005-11-01 | 1.568488 | 2 | 210 | no |
| 6 | 2006-01-03 | 1.395325 | 1 | 252 | no |
| 7 | 2006-02-14 | 1.559859 | 5 | 281 | no |
| 8 | 2006-04-18 | 1.506446 | 2 | 324 | no |
| 9 | 2006-07-24 | 1.431748 | 2 | 391 | no |
| 10 | 2007-01-11 | 1.607898 | 8 | 509 | no |
| 11 | 2007-07-03 | 1.554830 | 14 | 628 | no |
| 12 | 2007-09-17 | 1.442076 | 13 | 680 | no |
| 13 | 2008-03-31 | 1.527662 | 29 | 814 | no |
| 14 | 2008-09-03 | 1.859309 | 28 | 923 | no |
| 15 | 2008-11-05 | 1.551468 | 40 | 968 | no |
| 16 | 2009-02-11 | 1.544940 | 5 | 1034 | no |
| 17 | 2009-05-29 | 1.543655 | 6 | 1108 | no |
| 18 | 2009-08-20 | 1.394558 | 1 | 1166 | no |
| 19 | 2009-12-10 | 1.840886 | 12 | 1244 | no |
| 20 | 2010-05-03 | 1.652557 | 4 | 1341 | no |
| 21 | 2010-06-17 | 1.551552 | 7 | 1373 | no |
| 22 | 2010-12-02 | 1.504568 | 2 | 1490 | no |
| 23 | 2011-03-08 | 1.596572 | 8 | 1555 | no |
| 24 | 2011-06-01 | 1.535790 | 49 | 1614 | no |
| 25 | 2011-09-21 | 1.668731 | 21 | 1692 | no |
| 26 | 2011-11-17 | 1.745012 | 10 | 1733 | no |
| 27 | 2012-03-09 | 1.404678 | 2 | 1809 | no |
| 28 | 2012-05-04 | 1.515487 | 3 | 1848 | no |
| 29 | 2012-06-14 | 1.453617 | 2 | 1876 | no |
| 30 | 2012-07-26 | 1.390337 | 1 | 1905 | no |
| 31 | 2012-10-19 | 1.594211 | 9 | 1965 | no |
| 32 | 2013-04-08 | 1.793621 | 47 | 2078 | no |
| 33 | 2013-06-19 | 1.476221 | 8 | 2129 | no |
| 34 | 2014-01-23 | 1.606768 | 28 | 2279 | no |
| 35 | 2014-03-31 | 1.644050 | 14 | 2325 | no |
| 36 | 2014-05-22 | 1.506813 | 5 | 2362 | no |
| 37 | 2014-07-29 | 1.709702 | 10 | 2408 | no |
| 38 | 2014-09-24 | 1.545726 | 7 | 2448 | no |
| 39 | 2015-02-02 | 1.717253 | 10 | 2537 | no |
| 40 | 2015-05-12 | 1.849099 | 63 | 2606 | no |
| 41 | 2015-08-19 | 1.573413 | 2 | 2675 | no |
| 42 | 2015-09-24 | 1.601259 | 5 | 2700 | no |
| 43 | 2016-02-08 | 1.703645 | 38 | 2793 | no |
| 44 | 2016-04-15 | 1.414541 | 1 | 2840 | no |
| 45 | 2016-05-25 | 1.592199 | 8 | 2868 | no |
| 46 | 2016-09-06 | 1.780563 | 40 | 2939 | no |
| 47 | 2017-01-09 | 1.538867 | 5 | 3025 | no |
| 48 | 2017-07-13 | 1.527891 | 10 | 3153 | no |
| 49 | 2017-09-07 | 1.439442 | 3 | 3192 | no |
| 50 | 2017-11-16 | 1.398631 | 1 | 3242 | no |
| 51 | 2018-04-19 | 1.602002 | 17 | 3346 | no |
| 52 | 2018-08-20 | 1.503679 | 4 | 3431 | no |
| 53 | 2019-08-30 | 1.937561 | 27 | 3690 | no |
| 54 | 2020-05-22 | 1.543929 | 33 | 3873 | no |
| 55 | 2020-07-09 | 1.477022 | 2 | 3905 | no |
| 56 | 2020-10-06 | 1.457154 | 3 | 3967 | no |
| 57 | 2021-02-03 | 1.459656 | 28 | 4049 | no |
| 58 | 2021-05-11 | 1.521730 | 3 | 4116 | no |
| 59 | 2021-10-14 | 1.454847 | 2 | 4225 | no |
| 60 | 2021-12-22 | 1.668772 | 19 | 4273 | no |
| 61 | 2022-03-17 | 1.402716 | 23 | 4331 | no |
| 62 | 2022-06-10 | 1.469554 | 6 | 4390 | no |
| 63 | 2022-10-21 | 1.664588 | 7 | 4482 | no |
| 64 | 2022-12-12 | 1.543105 | 5 | 4517 | no |

- primary merged episode count: **64**
- boundary-truncated episodes: 0
- anchor spacing (primary): min 25 / median 60.0 / max 259 sessions

### Per-year episode counts (primary 90th)
| year | episodes |
|------|----------|
| 2005 | 5 |
| 2006 | 4 |
| 2007 | 3 |
| 2008 | 3 |
| 2009 | 4 |
| 2010 | 3 |
| 2011 | 4 |
| 2012 | 5 |
| 2013 | 2 |
| 2014 | 5 |
| 2015 | 4 |
| 2016 | 4 |
| 2017 | 4 |
| 2018 | 2 |
| 2019 | 1 |
| 2020 | 3 |
| 2021 | 4 |
| 2022 | 4 |

## 9. Derived invariant
- final episode anchors at least 21 trading sessions apart: **PASS — all final episode anchors are >= 21 trading sessions apart.**

## 10. Count-density tier (primary 90th only)
- primary merged episode count = 64
- **count-density tier: COUNT-DENSITY ADEQUATE TO REVISIT, NOT AN AUTHORIZATION**
- **FRAGILE / BORDERLINE** — the count-density tier differs across the 85/90/95 grid.

Frozen tier labels: `N_episodes < 30` → COUNT-INFEASIBLE FOR A FUTURE WAKE DESIGN; `30 <= N < 60` → SPARSE; FUTURE WAKE DESIGN NOT RECOMMENDED WITHOUT EXTRA JUSTIFICATION; `N >= 60` → COUNT-DENSITY ADEQUATE TO REVISIT, NOT AN AUTHORIZATION. Even the top tier does not authorize wake, prediction, gate, alpha, sealed data, or atlas promotion.

## 11. Structural firewall proof
- CR/CI construction IMPORTED from the reviewed Diagnostic-2 script (actual function object), not retyped;
- imported module `CSV_PATH` re-resolved and re-hashed to the authorized sandbox SHA before any row read;
- input columns asserted exactly {`date`, `adj_close`} (inherited from the imported construction);
- zero rows on/after `2023-01-01` (inherited sealed-boundary guard + re-checked here);
- no forward-window function defined; no wake/outcome/target column constructed (constructed columns checked against an allow-list and a forbidden-token scan);
- no negative (future) shift call present in source; no forward merge present;
- self-scan over this script's own function names and constructed column names: **PASS (no offenders)**.

## 12. Self-scan result
- PASS (no offenders)

## 13. Explicit boundary statements
- No wake/outcome/target was computed.
- No forward window was used (anchors are not used to index any post-t value).
- No gate was run.
- No alpha was spent.
- No sealed (>= 2023-01-01) data was accessed.
- No predictive claim was made.
- This audit does NOT authorize Gate 2 (wake-design authorization), which requires Gate 1 clearing with adequate episode density AND separate authorization.
