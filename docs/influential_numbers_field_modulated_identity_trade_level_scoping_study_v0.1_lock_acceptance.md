# Lock-acceptance — Pre-registered trade-level scoping study (field-modulated identity, trade-level proxy) v0.1

**Version:** v0.1 (lock-acceptance)
**Date:** 2026-05-16
**Project:** Coherent Numbers
**Program:** Influential Numbers (umbrella)
**Governs:** `docs/influential_numbers_field_modulated_identity_trade_level_scoping_study_v0.1.md`
**Status:** **LOCK-ACCEPTED 2026-05-16 by explicit user statement.** Design is immutable for this pre-registered trade-level scoping study. **Not committed. Not staged.** No data contacted. No analysis run. Acceptance locks the design **only**; it is **not** approval to implement, run analysis, contact data, stage, or commit — each remains separately gated.

---

## 1. What this memo is

This is the lock-acceptance checklist for the trade-level scoping study, parallel in role to `docs/influential_numbers_cell_1_design_memo_v0.1_lock_acceptance.md`. It exists so that lock-acceptance is a deliberate, separately-reviewable act, not an implicit consequence of editing the design memo. Acceptance of this memo (by explicit user statement) is the single remaining gate before any computation against the substrate.

It is **not** approval to implement, run, analyze, or commit. Those remain separately gated.

## 2. Scope and label confirmation

- The governed artifact is a **pre-registered trade-level scoping study — a different abstraction-level proxy for field-modulated identity.** It is **not** the original coordinate-axis Influential-Numbers cell and **not** a full registered charter cell (it defines no sealed train/holdout path; it is CV-only).
- The coordinate-axis substrate-mismatch memo (`docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md`) remains a failed-lock record and is **not** runnable.
- Option-3 sequencing holds: this is Step 1. Step 2 (build/freeze/hash a bar-level coordinate-axis substrate and register a separate cell) is gated on the §M graduation criterion and is **not** authorized by this acceptance.

## 3. Governance attestations (must all hold for acceptance)

| # | Attestation | State |
|---|---|---|
| G1 | Does not reinterpret, rescue, reopen, or re-run Cell 1, Candidate B, or Candidate C; verdicts independent in both directions. | Satisfied in memo §B, §N |
| G2 | Not framed as rescuing any prior null. | Satisfied in memo §A, §B |
| G3 | Study stands on its own grounds (justified by §C research question, not prior outcomes). | Satisfied in memo §B |
| G4 | No Kryon-source authority cited as evidence anywhere. | Satisfied in memo §B |
| G5 | Terms "exhaustion"/"pressure" do not appear; neutral construct language only. | Satisfied (absent throughout) |
| G6 | OOS 2023+ sealed; no holdout into sealed data; CV-only ⇒ labelled scoping study, not cell. | Satisfied in memo §A, §I, §L |
| G7 | Overlap/independence disclosed explicitly, not implicit. | Satisfied in memo §L |
| G8 | Failure rule binding; no post-hoc additions / rescue / prior-cell reinterpretation. | Satisfied in memo §N |

## 4. Locked-parameter register (snapshot for audit)

| Item | Locked value |
|---|---|
| Primary Y | `log1p(abs(r_multiple))` |
| Secondary (descriptive, non-verdict) | `first_target_hit` (binary), `bars_held` (continuous) |
| Substrate | frozen pullback × pooled Phase 3b, SPY/EFA/EEM/GLD/TLT, 1,282 trades, 2005–2022, freeze manifest commit `5225bfd` |
| Identity (M1) | `direction`, `initial_risk`, `log(entry_price)` (within-asset, train-fold-only standardized) |
| Leakage exclusions | `exit_reason`, `exit_date`, `exit_price`, `bars_held`, `first_target_hit`, `r_multiple` never used as features |
| M1L expanded identity | M1 + asset fixed effects + day-of-week + month-of-year (no quarter; no mod-7/mod-10) |
| Context block | 7 features (all of §G), LOCKED IN |
| Prior-trade sequence | single pooled stream by `entry_date`, resolved-before-entry constraint |
| Interaction block | {`direction`, `initial_risk`, `log(entry_price)`} × 7 context = **21** terms; same structure in M2/M3a/M3b |
| Calendar/asset in interactions | excluded by design |
| Models | M0, M1, M1L, M2, M3a (shuffled context), M3b (Gaussian context); ridge |
| CV | 5-fold forward-chaining expanding-window, pooled by `entry_date` |
| Embargo | trade-interval-overlap purge (train trade purged if `exit_date` ≥ first validation `entry_date`); no extra horizon embargo (Y realized at exit) |
| Ridge penalty | `np.logspace(-3, 3, 13)`, inner forward-chaining 5-fold, train-only |
| OOS R² aggregation (B1) | pooled-residual vs train-fold M0 baseline (M0 ≡ 0) |
| Fold-level "beat" (B2) | any strictly positive improvement; magnitude margin only at aggregate |
| M3a (B4) | joint within-fold context row-permutation; interactions recomputed; master seed 20260516 |
| M3b (B5) | 7 i.i.d. N(0,1) columns; interactions recomputed; master seed 20260516 |
| Master seed | `20260516` (per-fold offsets documented) |
| Degeneracy guard | abort→map(iv) if any validation block < 50 rows post-exclusion/purge, or unsafe rank-degeneracy |
| Warmup exclusion | drop first 20 (N=20 primary), 40 (N=40), 10 (N=10); each N own sample |
| Primary success | M2 beats M1L, M3a, M3b by `max(0.01 abs OOS R², 20% rel)` aggregate **and** beats each in ≥4/5 folds |
| Robustness | N=10, N=40 supplementary only; cannot rescue/reinterpret a failed N=20 |
| Graduation | all 5 §M conditions required; never automatic; itself a separate pre-registered decision |

## 5. Post-lock immutability

On acceptance, none of the §4 register may be re-opened: not Y, identity set, M1L composition, context set, sequence, interaction column list/count (21), model set, CV/embargo, ridge grid/inner-CV, R²/beat conventions, seeds, degeneracy guard, warmup rule, success threshold, or robustness scope. A protocol-internal contradiction surfaced *before* any real-data computation is the only amendable case, and only via a separate pre-data amendment record stating no outcomes have been observed (charter "Registry"; Cell 1 lock-acceptance discipline).

## 6. Acceptance block (unsigned)

> Lock-acceptance **granted by explicit user statement, 2026-05-16.** The §4 register is locked and the §3 attestations (G1–G8) hold. The design of the governed scoping-study memo is now **immutable**: no post-hoc feature additions, no threshold changes, no reinterpretation of Cell 1 / Candidate B / Candidate C, no rescue framing. A near-miss remains a fail under the locked §I criterion. This acceptance freezes the design **only**; it does **not** authorize implementation, a verdict run, data contact, staging, or commit — each is separately gated and the verdict run, if later authorized, occurs exactly once.

**Acceptance status:** ☑ ACCEPTED 2026-05-16 (explicit user statement). Design immutable. Implementation NOT authorized by this acceptance.

— end of lock-acceptance memo (ACCEPTED 2026-05-16; NOT COMMITTED, NOT STAGED) —
