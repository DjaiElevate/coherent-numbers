# Result memo — trade-level field-modulated identity scoping study v0.1 (Gate 3, one-time verdict)

**Version:** v0.1 (result)
**Date:** 2026-05-16
**Project:** Coherent Numbers · Program: Influential Numbers (umbrella)
**Artifact type:** Pre-registered trade-level **scoping study** (CV-only). Not the coordinate-axis cell; not a full registered charter cell.
**Verdict:** **PRIMARY N=20 — FAIL.** Interpretation cell **(ii) expanded-identity-only**. `primary_success = False`.

This is the single authorized one-time real-data verdict run. No locked design or implementation file was modified before or after seeing results (verified byte-identical to commit `c086bec`).

---

## A. Run identity

| Field | Value |
|---|---|
| Run ID | `fmi_trade_level_gate3_20260516_172655` |
| Timestamp | `2026-05-16T17:26:56` |
| Code commit | `c086bec1750d460c86dffbaa9f11e93563b9ca29` |
| Design commit | `8d4bd1dcaf39100882c165583c7bfd805c42b401` |
| Machine-readable artifact | `results/field_modulated_identity_trade_level_gate3_20260516_172655.json` |
| Substrate | frozen pullback × pooled Phase 3b — SPY/EFA/EEM/GLD/TLT, freeze manifest `5225bfd` |
| Substrate files (SHA-256 verified vs manifest) | SPY `1d8a7b77…`, EFA `275af7e0…`, EEM `56cf8e5f…`, GLD `0de7bf6d…`, TLT `037ea417…` (all matched byte-identically; run aborts on mismatch) |
| Combined substrate SHA-256 | `53cb19a4e87b11dcc93de7ae1dc002d557d0265fad7d391323b76813a0b3a4ba` |
| Substrate row count | 1,282 (SPY 243, EFA 283, EEM 261, GLD 253, TLT 242) |
| entry_date range | 2005-02-04 … 2022-12-16 |
| exit_date range | 2005-02-17 … 2022-12-30 |
| OOS 2023+ | **Zero 2023+ rows** (entry and exit). OOS 2023+ remained **sealed** by construction; in-code seal re-asserted (run aborts if any 2023+ row). |

## B. Primary N=20 sample accounting

| Quantity | Value |
|---|---|
| Raw input rows | 1,282 |
| Warmup exclusions (locked: drop first 20) | 20 |
| Undefined-window drops | 0 |
| Final modeling rows | **1,262** |
| Purge (train trades with exit_date ≥ first val entry_date), per fold | F1 210→205, F2 420→418, F3 630→628, F4 840→839, F5 1050→1046 |
| Validation block sizes | F1–F4: 210, F5: 212 (all ≥ 50) |
| Degeneracy flag | **False** (clean run; not routed to cell iv) |

## C. Primary N=20 model performance

**Aggregate pooled-residual OOS R² (baseline = train-fold M0; M0 ≡ 0 by construction):**

| Model | Aggregate OOS R² |
|---|---|
| M0 | 0.000000 |
| M1 | −0.007047 |
| M1L | −0.006411 |
| **M2** | **−0.031177** |
| M3a | −0.033051 |
| M3b | −0.019453 |

**Fold-level OOS R²:**

| Model | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|
| M0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| M1 | −0.001712 | 0.003369 | 0.002250 | 0.007510 | −0.043676 |
| M1L | −0.001568 | 0.003689 | 0.003001 | 0.013591 | −0.048076 |
| M2 | −0.107451 | −0.013664 | 0.014248 | 0.017181 | −0.081681 |
| M3a | −0.064492 | −0.004635 | −0.031715 | −0.000706 | −0.065966 |
| M3b | −0.025583 | −0.027983 | 0.000326 | 0.000508 | −0.048182 |

**M2 fold wins (M2 fold-R² strictly > comparator, §I-B2):** vs M1L **2/5** · vs M3a **2/5** · vs M3b **3/5**.

Texture (faithful reporting, not reinterpretation): every model's aggregate OOS R² is ≤ 0 — no model, including M1L, beats the marginal-mean baseline out-of-sample. M2 is the **second-worst** model. This does not soften the verdict; it is reported because §C/§K require honest performance context.

## D. Locked §I verdict (primary N=20)

For each comparator the required margin is `max(0.01 absolute, 0.20·comp_R²)` with the relative term applying only when `comp_R² > 0` (confirmed reading). All three comparators have `comp_R² < 0`, so the **absolute 0.01 floor binds** for each.

| Comparator | Required margin | Actual M2 − comp | Aggregate margin passed? | ≥4/5 fold-win passed? |
|---|---|---|---|---|
| M1L | +0.010000 | **−0.024766** | **No** | No (2/5) |
| M3a | +0.010000 | **+0.001874** | **No** (0.0019 < 0.01) | No (2/5) |
| M3b | +0.010000 | **−0.011724** | **No** | No (3/5) |

- `primary_success = **False**`.
- Interpretation cell: **(ii) expanded-identity-only** — routed because `M1L (−0.006411) > M1 (−0.007047)` while M2 fails the criterion vs M1L. Per locked §F the licensed conclusion is **"expanded identity may matter," not "field-modulated identity."** Note the "M1L > M1" relation here is marginal and both are below the M0 baseline; the cell-(ii) label is the locked classifier output and is reported as such, with no upward reinterpretation.
- **A near-miss is a fail under the locked §I criterion. This is not even a near-miss:** M2 is clearly worse than M1L (−0.0248 below it) and fails every aggregate and fold-win gate against all three comparators.

## E. Interaction / attribution reporting (descriptive, read-only)

Computed per §J/§E by reusing the locked feature assembly and locked alpha selection on the primary N=20 folds (descriptive only; it does not and cannot enter the verdict, which comes solely from the locked `run_full_study`).

- 21 identity×context interaction terms (locked).
- Mean |ridge coefficient| concentration across the 21 terms: **top-1 share 0.098, top-3 share 0.263, top-5 share 0.405 → diffuse** (no small set of interaction terms dominates).
- Highest-magnitude terms (descriptive ordering): `initial_risk × recent_win_rate`, `initial_risk × recent_mean_R`, `direction × recent_win_rate`, `log_entry_price × recent_mean_R`, `log_entry_price × recent_longshort_imbalance`.
- **Structural read:** the M2 interaction signal is **diffuse and structurally murky** — and moot for support, since M2 underperforms M1L out-of-sample. There is no concentrated, interpretable interaction structure to carry forward.
- Calendar identity controls enter M1L only as expanded-identity controls and are **excluded from the interaction block**; they are **not** reinterpreted as field-modulated evidence.

## F. Supplementary robustness (non-primary; context only)

These cannot rescue, soften, reverse, or reinterpret the primary verdict.

| Run | Modeling rows | M2 | M1L | M3a | M3b | M2−M1L / −M3a / −M3b | Fold wins (M1L/M3a/M3b) | Would pass §I? | Direction vs primary |
|---|---|---|---|---|---|---|---|---|---|
| N=10 | 1,272 | −0.046023 | −0.006223 | −0.021608 | −0.026850 | −0.0398 / −0.0244 / −0.0192 | 2 / 2 / 3 | **No** (cell iii) | Agrees: no field support |
| N=40 | 1,242 | −0.013608 | −0.017846 | −0.012605 | −0.029203 | +0.0042 / −0.0010 / +0.0156 | 3 / 2 / 4 | **No** (cell iii) | Agrees: no field support |

Both supplementary windows independently fail the same criterion and **directionally agree** with the primary: no field-modulated support. (N=40's single aggregate "beat" of M3b, +0.0156, is incomplete — it fails vs M1L and M3a and fails fold-wins — and is non-primary regardless.)

## G. Output artifacts

1. **Machine-readable run output:** `results/field_modulated_identity_trade_level_gate3_20260516_172655.json`
2. **Human-readable result memo:** this file, `docs/field_modulated_identity_trade_level_result_memo_v0.1.md`

### Required explicit statements

- **No locked design changes were made.** The design memo (`8d4bd1d`) and its lock-acceptance are byte-identical and untouched.
- **No implementation changes were made after seeing results.** `src/field_modulated_identity_trade_level.py`, the tests, the synthetic harness, and the conformance review are byte-identical to commit `c086bec` (verified `git diff HEAD` empty before and after the run).
- **The primary N=20 verdict FAILED:** `primary_success = False`; M2 did not beat M1L, M3a, or M3b on the locked aggregate margin and did not reach ≥4/5 fold wins against any of them; interpretation cell **(ii) expanded-identity-only**.
- **Near-miss = fail.** This result is a clear fail, not a near-miss; the rule is applied without softening.
- **Supplementary robustness cannot rescue the primary result.** N=10 and N=40 are context only; both independently fail and agree directionally. The primary fail stands.
- **Does the result justify later cell registration under the locked §M graduation criteria?** **No.** §M requires *all five* conditions; condition 1 ("M2 passes the §I primary success criterion") is **not met**, so graduation fails at the first gate. Conditions 2–5 are moot. Per §N the trade-level field-modulated identity hypothesis **is not supported as operationalized**; no post-hoc feature additions, no rescue, no reinterpretation of Cell 1 / Candidate B / Candidate C. Any future reframe must explicitly name what this failed operationalization conceded (trade-level abstraction in place of the coordinate-axis substrate, the specific 7-feature context set, the ~noise-floor threshold at N≈1,262, and the substrate overlap with prior cells per §L).

### Scope reminder (per locked §B)

This trade-level scoping study **cannot confirm or falsify the original coordinate-axis influential-numbers hypothesis**. A null here is not a falsification of the coordinate-axis hypothesis; it removes the scoping motivation that would have justified investing in the Option-1 bar-level coordinate-axis substrate. It does not reinterpret or rescue any prior cell, and it does not bear on Cell 1 (Class 3), Candidate B (not-confirmed split-null), or Candidate C (12-privileged), which remain independent and unchanged.

— end of result memo (NOT staged, NOT committed) —
