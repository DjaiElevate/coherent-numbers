# Lane 2 TTG Magnitude-Pressure — Pre-Data Benchmark + Limitation Memo v0.1

## Status

External-input decision memo. Supplies the pre-data effect-size benchmark that the prior viability memo flagged as `RHO_MIN_MEANINGFUL_REQUIRES_EXTERNAL_INPUT`, then runs the committed §8a kill test against it.

No data contact, no execution, no 2023+ contact, no acquisition, no prereg lock. Content is literature plus design-only arithmetic. Does not amend the TTG→SPY directional null. Does not authorize execution, feature extraction, outcome construction, model fitting, 2023+ acquisition, or any seal contact.

## Provenance / governing anchors

- Current repo state at creation: HEAD = origin/main = `2003fc855bd0583f137e8814c173485981540270`; branch `main`; upstream `origin/main`.
- **Outcome/control/statistic anchors:**
  - Return basis / close-field (log return, raw `close`): `084c5bd` — `docs/lane2_type_tone_goldstein_outcome_basis_close_field_resolution_v0.1.md`.
  - Primary outcome `abs(next_session_return_s)` + HAR-RV/outcome coherence (RV window ends ≤ `s−1`, anchor return excluded, no `t`/`t+1` leakage): `bc3b9c0` — `docs/lane2_type_tone_goldstein_outcome_side_join_gate_locks_v0.1.md`.
  - At-join primary statistic (simultaneous Spearman partial vs `abs(next_session_return_s)`, k=6 = rank-date + 3 volume/coverage controls + `trailing_rv_5` + `trailing_rv_22`; `SE_z = 1/√(N_eff−9)`; `trailing_rv_60`/single-window robustness-only): `fb26424` — `docs/lane2_type_tone_goldstein_v0.3_har_rv_control_scope_amendment_v0.1.md`.
  - §8a/§10 MDE machinery + §12 LOYO/leave-two influence gate + two-sided §10 detectability floor / Fisher-z convention: `c6aeb2b` — `docs/lane2_gdelt1_type_tone_goldstein_lock_closure_v0.3.md`.
  - At-join §7/§10/§12 governing manifest = `c6aeb2b + fb26424` (reading `c6aeb2b` alone for the at-join clauses is stale-source); base lock-closure = `294494a`.
- **Pressure-feature anchors:**
  - Mechanism (intensity/valence pressure, not amount), single composite `intensity_valence_pressure`, primary outcome pairing, incremental-over-volume requirement, negativity-only, frozen-from-in-sample standardization, 2023+ seal: `0295406` — `docs/lane2_gdelt1_type_tone_goldstein_extraction_design_memo_v0.1.md`.
  - F1/F2/F3 formulas locked to single values (S1 common daily `NumMentions` denominator §5; F1 = `QuadClass=4` mention-share §7; F2 = share-of-total `max(0,−GoldsteinScale)` §8; F3 = share-of-total `max(0,−AvgTone)` §9; expanding past-only z-scaler §12; equal-weight composite; per-day Kish floor `N_eff_mentions = (ΣNumMentions)²/Σ(NumMentions²) ≥ 100` §17/M1; §4B volume-costume check): `294494a` — `docs/lane2_gdelt1_type_tone_goldstein_lock_closure_v0.2.md`.
  - Extraction authorization gate (separate gate before any data contact): `ea891e0` — `docs/lane2_gdelt1_type_tone_goldstein_extraction_authorization_gate_v0.1.md`.
- **Directional TTG→SPY result anchor:** prereg `8406878` — `docs/lane2_ttg_spy_prereg_v1.1.md` (directional Class-1-iff-`r>0`); result `2003fc8` — `docs/lane2_ttg_spy_v1_results_v0.1.md` (terminal weak/null, single read spent, no V2).
- **Prior viability memo / benchmark gap:** conversation-derived design state (TTG magnitude-pressure prereg v0.1 draft + pre-data benchmark + 2023+ extent memo v0.3 draft), which established: 2023+ extent not committed; `rho_min_meaningful` unresolved; `N_raw_ceiling` unresolved; Kish/effective-N unresolved; Option C blocked pending external benchmark. Those drafts were review-only and were not committed; this memo is the committed external-input resolution of the benchmark gap they flagged.
- **Benchmark source status:** external literature translated into design benchmarks; no repo data used.

## 1. Quantity being benchmarked

The benchmark applies to the committed primary statistic only: the simultaneous Spearman partial correlation of the F1/F2/F3 pressure composite against `abs(next_session_return_s)`, with the k=6 control set (rank-date + 3 volume/coverage controls + trailing_rv_5 + trailing_rv_22).

This is the incremental effect of news pressure on next-session magnitude after HAR-RV and coverage controls — not the marginal news→volatility association. HAR-RV controls deliberately remove volatility persistence; coverage normalization removes the volume/attention channel. The target is the residual news-pressure signal that survives both.

The prior viability memo established that no committed benchmark exists, that the committed 0.054–0.093 figures are N-derived detection floors rather than meaningful-effect thresholds, and that the only in-window magnitude anchor — the volume association ρ ≈ −0.15 to −0.18, dissolved under drift control — is in-window observed and therefore forbidden as a benchmark basis. The benchmark below is set on external/literature grounds, pre-data, with no reference to any in-window quantity.

## 2. Literature basis

The directly relevant strand augments HAR-RV / realized-volatility models with news or sentiment and reports the incremental contribution after realized-volatility controls.

- Bodilsen et al. (2025), Journal of Applied Econometrics — "Exploiting News Analytics for Volatility Forecasting." Augments realized-volatility models for the S&P 500 and individual stocks with macroeconomic and firm-specific news sentiment. A favorable aggregate/macro news signal is reported at roughly the ρ ≈ 0.10 order of magnitude with next-day realized measures after volatility persistence is accounted for, while firm-specific sentiment contributes far less once past realized volatility is included. Gains are stronger at longer weekly/monthly horizons than at the daily horizon.
- Mamaysky & Glasserman (2016), OFR WP — "Does Unusual News Forecast Market Stress?" Unusual negative news predicts future volatility/stress, but once lagged implied/realized volatility and return controls are included, the incremental contribution of news measures falls sharply and is economically small.
- GDELT-specific corroboration is directional/plausibility support, not a clean magnitude estimate. Studies using GDELT tone/Goldstein/coverage measures report statistically significant relationships with returns or volatility, but do not isolate a clean after-HAR-RV partial correlation matching the present design.
- Methodological corroboration: applied GDELT work indicates that Goldstein/tone aggregates must be normalized by total event coverage to avoid spurious drift from changing news volume. This is exactly why the F1/F2/F3 common denominator and §4B volume-costume gate are part of the design.

Two regularities are load-bearing:
1. incremental news effects after volatility controls are modest;
2. effects are weakest at the daily horizon and stronger at weekly/monthly horizons.

## 3. Pre-data benchmark

These values are not directly reported estimates from any single study. They are conservative design benchmarks, derived by translating the literature's favorable after-RV anchor (ρ ≈ 0.10) into the present design and discounting marginal news→volatility effects for the HAR-RV and coverage controls and for the daily horizon. They are adopted as pre-data planning targets for the viability decision, not as empirical findings imported from the cited papers.

Discount logic:

- Composition discount: the favorable anchor is a curated macroeconomic-news index; the F1/F2/F3 composite is a broad GDELT conflict/tone/Goldstein aggregate and is noisier.
- Horizon discount: the committed outcome is next-session magnitude, the horizon where the literature finds the news effect weakest.
- Partial offset: the pressure composite is aggregate/geopolitical rather than firm-specific, so it is not in the near-zero firm-specific bucket.

Benchmark:

| Quantity | Value | Basis |
|---|---:|---|
| `rho_expected` | ≈ 0.07 | central order-of-magnitude estimate; plausible band 0.05–0.10; 0.10 optimistic ceiling |
| `rho_min_meaningful` | ≈ 0.05 | smallest incremental partial correlation worth confirmatory spend |
| Constraint | `rho_min_meaningful <= rho_expected` | satisfied |

Provenance and discipline:
Both values are external/literature-derived, pre-data, and set without reference to the 2013–2022 in-window effect, the TTG→SPY directional null, the available 2023+ N, or any desire to make Option C viable. `rho_min_meaningful` is not raised to clear the MDE. These are order-of-magnitude reads from heterogeneous literature, not precise priors.

## 4. §8a kill test against the benchmark

Committed convention: `rho_MDE = tanh(z_required / sqrt(N_eff - 9))`, k=6, power 0.80. One-sided α=0.05 gives `z_required = 2.48647`; two-sided sensitivity gives `z_required ≈ 2.80158`, which only enlarges the MDE.

Design-arithmetic sensitivity, not data:

| N_eff | 100 | 150 | 250 | 500 | 800 |
|---|---:|---:|---:|---:|---:|
| ρ_MDE, one-sided k=6 | 0.255 | 0.206 | 0.159 | 0.112 | 0.088 |

Maximum achievable 2023+ window:
As of mid-2026, the largest acquirable out-of-sample window is roughly 2023-01-01 to current availability, approximately 750–850 raw trading days at best. This is a real-world planning assumption for benchmark-limitation purposes, not a committed repo source-freeze; exact 2023+ extent remains uncommitted and would require a separate source-freeze/acquisition decision.

- Best case, no deflation, N_eff ≈ 750–850: `rho_MDE ≈ 0.088–0.092`.
- Realistic case after per-day Kish eligibility losses and AR(1) volatility-persistence deflation, N_eff plausibly ≈ 350–550: `rho_MDE ≈ 0.11–0.14`.

Comparison:
`rho_expected ≈ 0.07` is below the no-deflation best-case MDE, and `rho_min_meaningful ≈ 0.05` is below every achievable MDE considered here. The detectable floor exceeds the effect this design expects to detect, even before realistic Kish/AR deflation.

## 5. Verdict

`OPTION_C_NONVIABLE_BEST_CASE_FAIL` at the daily next-session horizon.

Even a full 2023+ acquisition is unlikely to detect an effect of the size the literature leads us to expect. A null from such a confirmation would be uninformative: it could not separate "no effect" from "a real effect near 0.05–0.07 that the sample was too small to see." Spending or acquiring the 2023+ seal for this daily confirmation would be theater. This is the failure mode the §8a viability gate was built to catch.

## 6. Routing

Two disciplined paths remain. This memo does not choose between them; it records the daily-horizon nonviability so the choice is made knowingly.

### Option A — daily question, in-window only

Run the 2013–2022 screen as explicitly non-pristine, exploratory, and non-confirmatory. The 2023+ seal is neither acquired nor spent. No confirmatory magnitude claim is made for the next-session horizon. Terminal for the confirmatory daily question.

### Separate long-horizon design

The literature points more strongly to weekly/monthly volatility effects, where a full 2023+ window could plausibly be powered. Re-posing the magnitude question at a multi-session horizon would require a new design: new outcome definition, re-derived controls and leakage timing, fresh benchmark, and its own lock. It is a fork, not a rescue of the committed daily outcome.

## 7. What this memo does and does not do

Does:
- supplies the external pre-data benchmark the prior memo lacked;
- runs the §8a kill test;
- records `OPTION_C_NONVIABLE_BEST_CASE_FAIL` for the daily next-session horizon.

Does not:
- authorize a full prereg lock;
- authorize 2023+ acquisition or seal contact;
- authorize outcome-free coverage probe;
- amend the committed daily outcome;
- commit the project to the long-horizon fork.

## 8. Next gate

`OPTION_C_NONVIABLE_DAILY_HORIZON — CHOOSE OPTION_A_OR_LONG_HORIZON_DESIGN`.

The next decision is a fork:
1. accept Option A for the daily next-session question; or
2. open a separate long-horizon magnitude-pressure design memo.

No full prereg lock and no 2023+ acquisition are justified for the daily next-session outcome on this benchmark.

## Boundary attestation

No data contact; no 2023+ contact; no acquisition; no raw market data; no row-level artifacts; no feature extraction; no outcome construction; no model fitting; no metric computation from data. All effect-size figures are external/literature reads and design-only arithmetic using committed conventions. This memo itself authorizes nothing.
