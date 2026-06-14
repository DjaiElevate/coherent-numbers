# Shock/Jump Asymmetry Lane — Stage-2 Pre-Gate Count Audit Report v0.1

**Status:** DRAFT — feasibility audit result, for owner review. Not a freeze, not a Stage-2 re-hash.

**This is NOT the sandbox gate. NOT a test of the hypothesis. NOT modeling. NOT tuning. No wake/outcome was computed. No sealed data was accessed.**

This report records the first controlled price-series contact for the Shock/Jump Asymmetry lane. Its sole purpose is to determine whether the Stage-1 design rules can produce a feasible, time-local matched shock set before any future sandbox gate.

---

## 1. Repo root verification

- Repo root: `/Users/jay/Documents/GitHub/coherent-numbers` ✓ (matches expected)

## 2. HEAD verification

- Branch: `main` ✓
- HEAD: `cd1016295ba4b843a61e8c9cd1811c86e88c0406` ✓ (matches expected)
- `origin/main`: `cd1016295ba4b843a61e8c9cd1811c86e88c0406` ✓ (matches expected)

## 3. Stage-1 memo SHA verification

- `docs/shock_jump_asymmetry_design_memo_v0_1.md`
- SHA-256: `c6529e37dd1a225e80d23f9f3b014620843b9e31deac4d98139c9e3a7bda1fa2` ✓ (matches expected)
- Confirmed in memo: no sandbox gate may run from Stage-1; deferred literals require the pre-gate count audit; Stage-2 re-hash required before any sandbox gate.

## 4. Sandbox CSV SHA verification

- `data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv`
- SHA-256: `5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901` ✓ (matches expected)

## 5. Date range loaded

- Loaded `2005-01-03` through `2022-12-30` (inclusive), within the allowed `2005-01-01 … 2022-12-31` sandbox window.
- Zero rows on/after the sealed boundary `2023-01-01`. No sealed data read.

## 6. Number of closes

- 4531 adjusted closes (columns read: `date`, `adj_close` only).

## 7. Volatility estimator used

Strictly pre-shock trailing realized volatility over a **21-trading-day** window ending strictly at `t-1` (implemented as `rolling(21).shift(1)`), computed for two rulers:

- **Plain ruler:** `σ = sqrt(mean(r²))` over the trailing 21 log returns ending `t-1` (the Stage-1 §7-B draft estimator; unambiguous).
- **Sign-symmetrized ruler (audit operationalization of §8):** `σ = sqrt(π/2)·mean(|r|)` over the same trailing window — the canonical MAD→σ scale on `|r|`, robust to leverage-driven tail clustering. The only difference from the plain ruler is L2-vs-L1 sensitivity, isolating exactly the magnitude-scale-contamination concern §8 raises.

Standardized return: `z_t = r_t / σ̂_{t-1}` for each ruler. The event-day return `r_t` is the numerator only; it never enters the denominator, and no return after `t` is read.

> **OPEN ITEM (owner, Stage-2):** §8 gives the sign-symmetrized ruler only as an example ("e.g., volatility estimated on `|r|`"), not a frozen formula. The MAD→σ form above is an **audit-time operationalization**, documented here so the cross-ruler feasibility comparison is reproducible. The exact frozen sign-symmetrized definition remains an owner decision before any Stage-2 freeze. This audit's verdict does not depend on the choice (see §18).

## 8. Threshold / caliper grid

- Candidate thresholds (|z|): `{3.5, 4.0, 4.5}` — audit candidates, not frozen, not chosen from performance.
- Caliper grid (standardized-distance units): `{0.20, 0.30, 0.40}`.
- Additional Stage-1 draft constraint applied: raw `|z|`-difference cap `≤ 0.5`.

## 9. Caliper covariate scales by threshold

Matching covariates `(|z|, pre-shock vol)` are scaled to unit variance **over the shock set**, which changes with threshold; therefore caliper units are threshold-dependent and ruler-dependent. Scales used (population std over the shock set):

**Plain ruler**

| Threshold | n shocks (scale basis) | scale(|z|) | scale(pre-shock vol) |
|-----------|------------------------|------------|----------------------|
| 3.5 | 46 | 1.41096 | 0.0062938 |
| 4.0 | 21 | 1.61291 | 0.0033290 |
| 4.5 | 16 | 1.65502 | 0.0030604 |

**Sign-symmetrized ruler**

| Threshold | n shocks (scale basis) | scale(|z|) | scale(pre-shock vol) |
|-----------|------------------------|------------|----------------------|
| 3.5 | 52 | 1.46365 | 0.0059532 |
| 4.0 | 31 | 1.61125 | 0.0037811 |
| 4.5 | 18 | 1.68622 | 0.0027331 |

A caliper of `0.20` therefore does **not** denote the same physical distance across thresholds or rulers; the scales above make the caliper counts interpretable.

## 10. Dual-ruler feasibility summary

Both rulers were computed and compared. See §13 (event counts) and §14 (matched-pair feasibility).

- **Event counts:** the sign-symmetrized ruler yields modestly **more** shocks at every threshold (e.g., 3.5: 52 vs 46; 4.0: 31 vs 21; 4.5: 18 vs 16), and at 4.0 it yields 4 up-shocks vs 2 under plain.
- **Down/up balance:** strongly down-skewed under both rulers at every threshold (e.g., 3.5: 36↓/10↑ plain, 42↓/10↑ sym; 4.0: 19↓/2↑ plain, 27↓/4↑ sym; 4.5: 14↓/2↑ plain, 16↓/2↑ sym).
- **Matched-pair feasibility:** materially the same verdict under both rulers — see §14. The maximum time-local one-to-one no-replacement matched-pair count under **either** ruler is **6** (threshold 3.5).
- **Highest feasible threshold for candidate floors {20,30,40}:** **none**, under either ruler (see §16).

**Ruler agreement:** the two rulers **agree** on the feasibility verdict — infeasible at all candidate floors. The minor count differences do not flip any floor. No threshold is feasible under one ruler while infeasible under the other relative to the floors (both are infeasible across the board). Per §8, ruler disagreement would be a design/feasibility finding, not success; here there is no disagreement to flag, and no "better-looking" ruler was selected.

## 11. Time-local window

- `±252 trading days` (Stage-1 candidate), measured on trading-day index. Time-local results are the gate-feasible figures; widened/nonlocal results are descriptive only.

## 12. Matching rule used for the count audit

- Match each **down-shock** to **up-shocks** on covariates `(|z|, pre-shock vol)`, each standardized to unit variance over the shock set.
- Distance: standardized Euclidean. Admission: distance ≤ caliper **and** raw `|z|`-difference ≤ 0.5 **and** (for the gate figure) trading-day index difference ≤ 252.
- **One-to-one, no replacement.** The reported matched-pair count is the maximum-cardinality one-to-one matching over admissible edges (Kuhn's algorithm), i.e., the most pairs the rule can form.
- No outcome/wake enters matching. Matching uses only event-side covariates.

## 13. Event count table (time-local; caliper-independent)

| Ruler | Threshold | n down | n up | n total |
|-------|-----------|--------|------|---------|
| plain | 3.5 | 36 | 10 | 46 |
| plain | 4.0 | 19 | 2 | 21 |
| plain | 4.5 | 14 | 2 | 16 |
| sym | 3.5 | 42 | 10 | 52 |
| sym | 4.0 | 27 | 4 | 31 |
| sym | 4.5 | 16 | 2 | 18 |

**Binding constraint:** up-shocks are scarce at every threshold (≤10, dropping to 2–4 at 4.0–4.5). One-to-one no-replacement matching is bounded above by `min(n_down, n_up) = n_up`, so the matched set cannot exceed the up-shock count regardless of caliper.

## 14. Matched-pair feasibility table (time-local, one-to-one, no-replacement)

| Ruler | Threshold | caliper 0.20 | caliper 0.30 | caliper 0.40 |
|-------|-----------|--------------|--------------|--------------|
| plain | 3.5 | 3 | 6 | 6 |
| plain | 4.0 | 0 | 1 | 1 |
| plain | 4.5 | 0 | 1 | 1 |
| sym | 3.5 | 4 | 6 | 6 |
| sym | 4.0 | 1 | 1 | 2 |
| sym | 4.5 | 0 | 0 | 1 |

Maximum across the whole grid (time-local): **6 matched pairs** (threshold 3.5, caliper ≥0.30, either ruler).

Supporting per-cell detail (candidate edges / down-with-match / up-with-match / unmatched-down / unmatched-up) is in the script's JSON output; the table above reports the gate-relevant matched-pair count.

## 15. Nonlocal / widened counts — DESCRIPTIVE ONLY — excluded from gate

These drop the `±252` time-local constraint. **DESCRIPTIVE ONLY — excluded from gate.** They are not used to choose feasibility.

| Ruler | Threshold | caliper 0.20 | caliper 0.30 | caliper 0.40 |
|-------|-----------|--------------|--------------|--------------|
| plain | 3.5 | 8 | 8 | 9 |
| plain | 4.0 | 0 | 2 | 2 |
| plain | 4.5 | 0 | 2 | 2 |
| sym | 3.5 | 8 | 9 | 9 |
| sym | 4.0 | 3 | 4 | 4 |
| sym | 4.5 | 1 | 1 | 2 |

Even widened, the maximum is **9 matched pairs** — still far below the lowest candidate floor (20). Widening does not rescue feasibility.

## 16. Most-selective-feasible interpretation for candidate floors {20, 30, 40}

Applying the Stage-1 mechanical interpretation (report only; no floor chosen here):

- **Candidate floor 20:** no threshold clears it under time-local one-to-one no-replacement matching (max time-local count = 6), under either ruler. Not cleared even by widened/nonlocal matches (max = 9).
- **Candidate floor 30:** not cleared by any threshold/caliper/ruler (time-local or widened).
- **Candidate floor 40:** not cleared by any threshold/caliper/ruler (time-local or widened).

**Highest threshold feasible for each candidate floor: NONE (20: none; 30: none; 40: none), under either ruler.**

> The audit reports which thresholds clear candidate floors {20,30,40}; it does not recommend a floor. The minimum floor must be justified independently from power/noise considerations before Stage-2 freeze.

This report does **not** recommend a floor and does **not** editorialize toward any achievable floor. (No candidate floor is achievable in any case.)

## 17. Does any candidate threshold appear feasible under time-local matching?

**No.** Under time-local one-to-one no-replacement matching, the maximum matched-pair count across all thresholds, calipers, and both rulers is **6**, below the lowest candidate floor of 20. A **feasibility null** appears to hold: the Stage-1 drafted literals (|z| ≥ 3.5/4.0/4.5; caliper 0.20–0.40; no replacement; ±252 time-local) cannot produce a matched set meeting any candidate floor.

Per Stage-1 §7A, an insufficient matched-pair count is **not a sandbox FAIL and not a hypothesis null** — it is an **infeasible design / non-result**. The root cause is structural: large up-shocks (≥3.5σ) are scarce relative to down-shocks (a frequency-side reflection of the same leverage asymmetry the lane studies), so symmetric-magnitude down-vs-up matching is starved on the up side. Widening into other epochs does not fix it and is excluded from the gate.

## 18. Does feasibility differ between plain and sign-symmetrized rulers?

**No — not at the verdict level.** Both rulers yield the same conclusion: infeasible at all candidate floors {20,30,40}, time-local and widened. The sym ruler produces slightly more shocks and marginally higher matched counts at threshold 4.0, but the maximum time-local matched-pair count is 6 under both. Because the verdict is identical, it does **not** depend on the (open) exact sign-symmetrized definition flagged in §7. No ruler was preferred for looking better.

## 19. No wake/outcome was computed

No forward realized volatility, forward max drawdown, forward recovery/calm-down time, forward range, future path length, or any target `y` was computed. The audit computed only event-side quantities (returns, strictly-pre-shock volatility, standardized returns, shock dates/signs/magnitudes, pre-shock volatility at event time, matching feasibility counts).

## 20. Forward-unreachability enforcement

`Forward-unreachability was enforced structurally: the audit table contains only event-side fields and no target/wake arrays or forward-window functions. The code cannot compute forward realized volatility, drawdown, recovery, or any future wake from the constructed audit structures.`

Enforcement mechanism (why a wake **cannot** be computed from the structures present, not merely that it was not):

1. **Column allow-list with runtime assertion.** The audit table is restricted to `ALLOWED_EVENT_SIDE_COLUMNS = {row_idx, date, adj_close, logret, vol_plain, vol_sym, z_plain, z_sym}`. The script asserts no other column exists and aborts otherwise. No target/outcome/wake array can be present in the structure the audit consumes.
2. **No forward-window functions defined.** The file defines no function for forward realized volatility, forward max drawdown, forward recovery, forward range, future path length, future wake construction, or target construction. Undefined functions cannot be called. A self-scan asserts none of the forbidden tokens appears as a `def` (result: no offenders).
3. **Trailing-only windowing.** The only windowing operation is `rolling(21).shift(1)`, which ends strictly at `t-1`. There is no forward indexing of the form `close[t+k]` or `iloc[t : t+window]` anywhere in the audit logic.
4. **Numerator/denominator separation.** `z_t = r_t / σ̂_{t-1}` uses the event-day return only in the numerator; the denominator uses returns up to `t-1`. No return after `t` is ever read.

Therefore there are no forward arrays, no forward-window functions, and no forward indices for any wake to be computed from.

## 21. This is not a sandbox gate

This audit is the Stage-2 pre-gate **feasibility count audit** only. No sandbox gate was run. No PASS/FAIL on the hypothesis was produced. No synthetic-null check was run.

## 22. No sealed data accessed

No data on/after `2023-01-01` was read, sampled, or stored. Only the 2005–2022 adjusted-close sandbox series (`date`, `adj_close`) was used.

---

## Bottom line (for owner review)

The Stage-1 drafted feasibility bundle is **infeasible** on the SPY 2005–2022 adjusted-close sandbox: the highest time-local one-to-one no-replacement matched-pair count is **6** (threshold 3.5), below the lowest candidate floor of 20, under both rulers. This is an **infeasible-design / non-result** finding (Stage-1 §7A), not a sandbox FAIL and not a hypothesis null. The binding constraint is the scarcity of large up-shocks relative to down-shocks. Any remedy (e.g., a different shock definition, a non-symmetric magnitude pairing, a different lane framing, or accepting the design as infeasible at adjusted-close-only resolution) is an owner design decision for a Stage-1 revision **before** any Stage-2 freeze — not a tuning step, and not to be resolved by widening into other epochs or by lowering a floor to fit these counts.
