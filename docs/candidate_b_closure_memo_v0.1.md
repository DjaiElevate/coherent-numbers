# Candidate B Closure Memo — v0.1

**Version:** v0.1 (Closure)
**Date:** 2026-05-15
**Project:** Coherent Numbers
**Cell:** Candidate B — pullback × harmonic-calendar modulation
**Status:** Closed
**Verdict:** Split-null

**Reference commits**
- Design memo (locked): `1e9a3e6` — `docs/candidate_b_design_memo_v0.1.md`
- Lock-acceptance: `159cccd` — `docs/candidate_b_design_memo_v0.1_lock_acceptance.md`
- Freeze: `5225bfd` — `docs/pullback_population_freeze_manifest_v0.1.md`
- Locked verdict run: `7a88833`

**Verdict artifacts**
- `results/candidate_b_results_20260514_231323_c1982503.json`
- `results/candidate_b_results_20260514_231323_c1982503.md`
- `rerun_verification_digest = c1982503a2ae31946ae56c8c74530d97408391ccb326768340d389f581ceef19`

---

## 1. Executive summary

Candidate B found a strong pooled phase-allocation irregularity under the locked March-20 12-sector partition, but failed the anchor-specific control. Therefore the equinox-anchored harmonic-calendar modulation hypothesis is not confirmed. The locked verdict map (memo §12.2) classifies the result as **Split-null**: exactly one of the two pre-registered nulls is rejected, and per §12.3 Split-null is informative texture, not a confirmatory result and not an invitation to amend the design.

## 2. Locked protocol recap

- **Primary population:** pooled Phase 3b 5-asset trade population from the pullback research program — SPY, EFA, EEM, GLD, TLT — 1,282 trades total over a common 2005-01-01 – 2022-12-31 window, produced under identical `BacktestParams` at pullback commit `7806a6d`. The substrate at run time is the set of frozen CSV SHA-256 digests recorded in the freeze manifest at commit `5225bfd`; all six digests verified match at run start.
- **Lens:** 12-phase March-20-anchored annual-sector calendar (§7.1). For each trade's `entry_date`, the relevant March-20 → next-March-20 cycle is located, `cycle_length_days` and `days_since_start` are computed, and the phase is `floor(days_since_start * 12 / cycle_length_days)`. Phase ∈ {0..11}, asserted at runtime.
- **Primary statistic:** `PSS_B1` (§9.1) — η²/correlation-ratio form of phase-conditional long-share dispersion, `between_B1 / total_B1`. Bounded in [0, 1]; degenerate `total_B1 = 0` aborts the run.
- **N.1 — Unstratified label-permutation null (primary):** `is_long` shuffled uniformly across all 1,282 trades (asset and phase labels held fixed). 10,000 permutations with seed `LABEL_PERM_SEED = 20260514`. Reports `beat_count_perm`.
- **N.2 — Exhaustive 365-DOY anchor-control null (primary):** the §7 annual-sector formula reapplied with the anchor swapped to each integer DOY `d ∈ 1..365`, exhaustively, no random sampling. Reports `beat_count_anchor`.
- **Verdict rule (§12.1–12.2):** Confirmatory requires `beat_count_perm ≥ 9500` and `beat_count_anchor ≥ 347` simultaneously. Exactly one pass and one fail is Split-null. Neither passes is Non-confirmatory.

## 3. Data-contact disclosure (verbatim, §13)

> Candidate B's verdict is conditional on a previously contacted, audit-frozen pullback-event population. The pullback Phase 1–3b series for SPY and the Phase 3b 2005–2022 series for SPY/EFA/EEM/GLD/TLT were inspected, partitioned, and used to estimate within-population statistics during pullback research before Coherent Numbers contacted them. The pullback `BacktestParams` were locked early at pullback commit `50ee2d1` and not re-tuned, which limits but does not eliminate this exposure. OOS 2023+ remains sealed and is out of scope for B.

## 4. Primary result

| Quantity | Value |
|---|---|
| `observed_pss_b1` | `0.03013694720290423` |
| `beat_count_perm` (out of 10,000) | **10,000** (strict pct `1.0000`; locked threshold `≥ 9500`) → **N.1 passes** |
| `beat_count_anchor` (out of 365) | **107** (strict pct `0.2932`; locked threshold `≥ 347`) → **N.2 fails** |
| Verdict | **Split-null** |
| Verbalization class | `n/a-split-null` |

**N.1 null distribution (n = 10,000 permutations):** mean `0.008575`, stdev `0.003625`, min `0.000741`, max `0.029743`. The observed value `0.030137` lies above every permuted value; z ≈ **+5.95** relative to the N.1 null mean.

**N.2 null distribution (n = 365 anchor-shifted PSS values):** mean `0.035170`, stdev `0.006035`, min `0.024680`, max `0.045457`. The observed value lies slightly below the N.2 mean; z ≈ **−0.83** relative to the N.2 null mean.

### 4.1 Precise interpretation

- **N.1 tests whether the observed long/short allocation is random given the locked March-20 12-sector partition.** N.1 passed maximally: not one of 10,000 label permutations produced a PSS_B1 as large as the observed value. The pooled population's phase-conditional long-share dispersion under the locked partition is far from what unconditional random labeling would produce.
- **N.2 tests whether March-20 is distinguished against alternative integer-DOY anchors.** N.2 failed: the observed `PSS_B1` is in fact slightly below the average PSS_B1 produced by the 365 alternative integer-DOY anchors, and only 107/365 anchors yield a strictly lower PSS_B1. The locked March-20 anchor is not specially distinguished against the anchor-control population.
- This is **not** "almost Confirmatory". By the locked verdict map, exactly one of the two pre-registered nulls is rejected and the other is not. The result is Split-null by §12.2 and informative texture by §12.3.

## 5. Diagnostic texture

The following diagnostics are reported but do **not** affect the verdict. They are not Confirmatory evidence and cannot upgrade Split-null.

### 5.1 Asset-stratified label-permutation diagnostic (§11.3)

- `asset_stratified_beat_count` = **9,999 / 10,000** (strict percentile `0.9999`).
- The observed `PSS_B1` exceeds essentially every permutation in which each asset's long/short mix is preserved within asset (only phase-to-direction associations within each asset are scrambled).
- The §12.4 verbalization rule only fires for Confirmatory verdicts and so the verdict log records `verbalization_class = n/a-split-null`. The diagnostic is texture.

### 5.2 Per-asset `PSS_B1` (§11.4)

| Asset | `PSS_B1` |
|---|---|
| GLD | 0.112314 |
| TLT | 0.084931 |
| SPY | 0.072661 |
| EFA | 0.062184 |
| EEM | 0.061144 |

Per-asset values are uniformly higher than the pooled value (smaller sub-populations have larger sampling variance under fixed bucket count). No per-asset anchor-control nulls were computed; per-asset values are descriptive only.

### 5.3 Calendar-civil controls (§11.1, §11.2)

| Control | `PSS_B1` | Δ vs. observed March-20 (0.030137) |
|---|---|---|
| `PSS_GREG_MONTH` (Gregorian civil month) | 0.041001 | +0.010864 |
| `PSS_JAN` (January-1 annual-sector) | 0.044304 | +0.014168 |

Both civil-calendar partitions produce a higher `PSS_B1` on the same data than the locked equinox-anchored partition. Per §11.1's independence caveat, these partitions are in the same family as the §10.2 anchor-control population (both are approximately monthly partitions offset by about 19 days from the locked anchor) and are not independent evidence beyond N.2. They are reported here as familiar civil-calendar benchmarks for human readability.

### 5.4 Phase-cell occupancy (§11.5)

| Phase | `N_p` | `L_p` | long-share |
|--:|--:|--:|--:|
| 0 | 109 | 70 | 0.642 |
| 1 | 115 | 63 | 0.548 |
| 2 | 113 | 45 | 0.398 |
| 3 | 109 | 59 | 0.541 |
| 4 |  88 | 56 | 0.636 |
| 5 |  96 | 52 | 0.542 |
| 6 | 145 | 68 | 0.469 |
| 7 | 116 | 72 | 0.621 |
| 8 |  84 | 54 | 0.643 |
| 9 |  92 | 62 | 0.674 |
| 10 | 115 | 79 | 0.687 |
| 11 | 100 | 53 | 0.530 |

`N_p` min = 84, max = 145, mean ≈ 106.83. Spread `max/min` ≈ 1.73, structurally uneven; no phase is empty.

### 5.5 N.2 anchor-control texture

**Top 10 DOY anchors by `PSS_B1`** (highest first):

| DOY | `PSS_B1` |
|--:|--:|
| 309 | 0.045457 |
| 219 | 0.045339 |
|  97 | 0.045279 |
|  36 | 0.045048 |
| 248 | 0.045031 |
| 280 | 0.044644 |
| 158 | 0.044569 |
| 276 | 0.044518 |
| 305 | 0.044473 |
| 215 | 0.044382 |

**Bottom 10 DOY anchors by `PSS_B1`** (lowest first):

| DOY | `PSS_B1` |
|--:|--:|
|  48 | 0.024680 |
| 109 | 0.024680 |
| 199 | 0.025068 |
| 170 | 0.025134 |
|  12 | 0.025464 |
|  73 | 0.025464 |
| 346 | 0.025464 |
| 351 | 0.025469 |
|  47 | 0.025560 |
| 134 | 0.025670 |

**March-20 anchor rank against the integer-DOY control:** the locked civil-date March-20 anchor produces the observed `PSS_B1 = 0.030137`. Against the 365 integer-DOY-anchored PSS values, only 107 are strictly lower; the locked anchor sits at strict percentile `0.2932`, well below the locked threshold of `0.95`.

**Clustering observation:** the top 10 integer-DOY anchors span 273 days (DOY 36 to DOY 309) and distribute across all four quarters of the year (Q1: 1; Q2: 2; Q3: 4; Q4: 3 in the top 10; broader top-30 still spans all four quarters). The strongest anchors are scattered and do not cluster near DOY 79 (≈ March 20). The 12-sector annual-allocation structure is broadly present across the year; it is not anchored at the equinox.

## 6. What was found

- The pooled Phase 3b 1,282-trade population contains **non-random phase-conditional long-share structure under the locked March-20 12-sector partition**: under the unstratified label-permutation null (§10.1), the observed `PSS_B1` is more extreme than every one of 10,000 permutations.
- The §11.3 asset-stratified diagnostic **weakens the simplest between-asset mix explanation** for that structure: when each asset's long/short mix is preserved and only phase-to-direction associations within each asset are scrambled, the observed `PSS_B1` is still extreme (9,999/10,000). The pooled effect is not a simple artifact of asset-composition variation by phase combined with cross-asset direction-mix differences.
- The structure **survives within-asset label preservation** as diagnostic texture. Per the locked verdict map and the §12.4 verbalization rule, this diagnostic is texture only; it does not upgrade the Split-null verdict.

## 7. What was not found

- Candidate B **did not confirm the equinox-anchored harmonic-calendar modulation hypothesis** — N.2 failed decisively (107/365, strict percentile 0.2932, against a locked threshold of 0.95).
- **March 20 was not distinguished in anchor space.** The locked anchor sits in the lower-middle of the integer-DOY anchor-control distribution; many other anchors produce comparable or higher `PSS_B1` on the same data.
- **Secondary diagnostics do not rescue, upgrade, or change the Split-null verdict.** Per memo §12.3 and §16 guardrails, secondary outcomes (`PSS_B2`, per-asset, civil-month, January-anchor, asset-stratified permutation) cannot promote a non-Confirmatory verdict.
- The result **does not prove that another anchor would confirm** the modulation hypothesis — the broad-band character of the anchor-PSS distribution is consistent with structure that is not anchor-specific at all, and selecting any single one of the higher integer-DOY anchors as a post hoc replacement would be a design rescue that the locked protocol explicitly forbids (§16, §12.3).
- The result **does not prove the observed structure is a real calendar effect.** The structure is real in this population under the locked lens; its causal/structural source — calendar, annual-sector artifact, asset-time-population interaction, or population-construction-induced regularity — remains unresolved.
- The result **does not establish replication** on other populations, other windows, or any pristine OOS sample.
- The result **does not fully rule out subtler asset/time/population interactions.** The §11.3 diagnostic weakens the simplest between-asset mix explanation but does not exhaust the space of asset-by-time-by-population mechanisms.

## 8. Program posture

- Candidate B joins the prior closed harmonic-calendar cells (SPY MVT, GLD) as another atlas tile. Standalone continuous-return harmonic-calendar cells on ETF substrates did not confirm (`docs/harmonic_calendar_mvt_closure_memo_v0.1.md`, `docs/harmonic_calendar_gld_closure_memo_v0.1.md`); Candidate B, the event-population cell, returns Split-null.
- Candidate B shows phase-allocation structure under the locked March-20 partition on a pullback-event substrate, but that structure is **not specifically attributable to the equinox anchor** under the locked anchor-control test. Whether it is attributable to any anchor — or to a non-anchor mechanism — is outside the scope this cell pre-registered.
- The program posture is **constrained curiosity, not rescue.** Candidate B does not select or recommend a next phase. The locked protocol's no-rescue clauses (§12.3, §16) and the lock-acceptance §7 prohibitions (no design changes after observing results, no unregistered additional verdict heads, no sampling-based anchor control) apply through this closure.

## 9. Open questions not answered by Candidate B

These questions are surfaced for the program log; none are scoped or authorized here. Any future cell that addresses them must be selected, designed, locked, and ratified under its own audit chain.

- Whether the broad-band anchor-space structure can be explained by a pre-registered future design that targets a non-anchor mechanism (e.g., partition geometry, sub-population stratification, or a continuous time-of-year feature rather than an anchor-shifted partition).
- Whether continuous-feature or seasonal controls (day-of-year regression, seasonal-volatility conditioning, regime-state conditioning) would explain or absorb the observed pattern.
- Whether the structure persists by asset, window, or alternative pullback populations — and whether per-asset confirmatory tests would survive their own pre-registered anchor controls.
- Whether the pattern survives different population definitions, such as direction-restricted populations, differently conditioned pullback populations, or non-pullback event populations on the same assets.
- Whether the pattern is a calendar effect, an annual-sector geometric artifact (the 12-bucket partition is broadly compatible with a wide range of annual periodicities), or another temporal/population interaction that is best characterized outside the harmonic-calendar lens family.

## 10. Closure statement

Candidate B is closed as Split-null. The March-20/equinox hypothesis is not confirmed. The diagnostic resolves cleanly: the pullback-event population contains strong phase-allocation structure that survives within-asset preservation, but the locked protocol does not identify the equinox as its organizing anchor.

— end of closure memo —
