# Spec-conformance review — trade-level field-modulated identity scoping study v0.1

**Version:** v0.1 (conformance review)
**Date:** 2026-05-16
**Project:** Coherent Numbers
**Governs:** implementation of the LOCKED memo
`docs/influential_numbers_field_modulated_identity_trade_level_scoping_study_v0.1.md`
(committed `8d4bd1d`) and its lock-acceptance memo.
**Status:** Implementation-only deliverable for **review**. **No real-data analysis run. No real substrate contacted. No verdict produced. Not staged, not committed.**

---

## 1. No-real-data attestations (explicit)

- **No observed real-data analysis was run.** The only execution performed was the synthetic conformance harness on a fabricated random frame.
- **No real substrate was contacted.** `src/field_modulated_identity_trade_level.py` contains **no file read, no path constant, no loader, and no network call**. Every entry point (`run_protocol`, `run_full_study`) takes an in-memory `pandas.DataFrame` supplied by the caller. The frozen Phase 3b CSVs under `data/raw/` are never opened by any code added in this gate. A real-data loader/runner is **intentionally not implemented** — wiring it is the separately-gated one-time verdict step.
- **No verdict was produced** on the real substrate. The verdict logic exists and is exercised only on synthetic/fixture inputs.
- **Code is ready for review only.** Gate 3 (one-time real-data verdict run) remains separately gated and is not authorized by this artifact.
- Determinism: identical input + identical `MASTER_SEED` ⇒ byte-identical aggregate and fold OOS R² (harness "deterministic: True"; `test_full_study_deterministic`).

## 2. Files added (working tree only; not staged)

| Path | Role |
|---|---|
| `src/field_modulated_identity_trade_level.py` | Result-defining locked protocol (features, models, CV, verdict). No real-data path. |
| `scripts/synthetic_conformance_field_modulated_identity_trade_level.py` | Synthetic-only harness; fabricates a same-structure frame, prints structural evidence. |
| `tests/test_field_modulated_identity_trade_level.py` | 29 conformance tests pinned to memo sections (incl. a synthetic positive control). |
| `docs/field_modulated_identity_trade_level_conformance_review_v0.1.md` | This artifact. |

## 3. Requirement → code → test → synthetic evidence map

Citations are `src/field_modulated_identity_trade_level.py:<line>` unless noted.

| Locked requirement (memo §) | Code location | Test | Synthetic-run evidence |
|---|---|---|---|
| Y = `log1p(abs(r_multiple))` (§D) | `run_protocol` L463 (`np.log1p(np.abs(...))`) | exercised by all `run_*` tests | harness runs end-to-end with this Y |
| Identity M1 = direction, initial_risk, log(entry_price); calendar empty in M1 (§E) | `base_feature_frame` L187; `_assemble` ident block L320–329 | `test_feature_matrix_widths` (M1 width = 3) | `widths["M1"]==3` |
| log(entry_price) standardized **within asset**, train-fold only (§E) | `_fit_within_asset_logep` L223; applied L312–319 | covered by widths/leakage tests | n/a (numeric) |
| Leakage exclusions never features (§E/§D) | `LEAKAGE_COLUMNS` L61; never referenced as a feature | `test_leakage_columns_never_features` | base cols disjoint from leakage set |
| Resolved-before-entry window leakage lock (§G) | `_resolved_prior_mask` L109; `build_context_block` L116 | `test_resolved_before_entry_constraint` | unresolved high-R prior excluded |
| 7 locked context features (§G/§P-1) | `CONTEXT_COLS` L43; `build_context_block` L116 | `test_interaction_count_is_21`, widths | `context cols (7): [...]` |
| Pooled stream ordered by entry_date, deterministic (§G/§P-2) | `canonical_pooled_frame` L80 | `test_pooled_stream_ordered_by_entry_date_deterministic` | monotonic entry_date |
| Warmup exclusion: drop first N (20/10/40) (§G/§P-9) | `run_protocol` L460–462 | `test_warmup_exclusion`, `test_primary_is_N20` | warmup dropped 20/10/40; modeling 1262/1272/1242 |
| N=20 primary; N=10/40 supplementary, non-rescue (§G/§N) | `run_full_study` L533 | `test_primary_is_N20` | supplementary marked `is_primary False` |
| Model set M0/M1/M1L/M2/M3a/M3b (§H) | `MODELS` L66; `_assemble` L292 | `test_model_set_exact` | `models: [...6...]` |
| 21 identity×context interactions, fixed (§H/§P-5) | `N_INTERACTIONS` L53; `_interactions` L284 | `test_interaction_count_is_21`, `test_interactions_are_identity_times_context` | `n_interactions: 21` |
| Same interaction structure across M2/M3a/M3b (§H) | `_assemble` M2/M3a/M3b branches L344–374 | `test_feature_matrix_widths` (equal widths) | widths M2==M3a==M3b |
| Calendar/asset excluded from interactions (§H/§P-5) | interaction uses `ident_*` only (3 cols) L353 | `test_interactions_are_identity_times_context` | n/a |
| Standardization train-fold only; dummies unstandardized (§E/§H/§I) | `Scaler` L209; `_standardise_continuous` L269; dummies via `_dummy_matrix` L168 | widths/interaction tests | n/a |
| M1L = M1 + asset FE + dow + month; quarter excluded (§F/§P-4) | `_assemble` expanded block L331–342; `DOW_LEVELS`/`MONTH_LEVELS` L36–37 | `test_feature_matrix_widths` (M1L>M1) | widths M1L>M1 |
| mod-7/mod-10 NOT included (§F) | absent from code (no modular feature) | grep-evident; widths test | n/a |
| 5-fold forward-chaining expanding-window (§I/§P-8) | `_forward_chaining_splits` L250; `run_protocol` L470 | `test_split_helper_shapes`, `test_forward_chaining_expanding_and_purge` | 5 folds, train 210→1050 expanding |
| Purge: train exit_date ≥ first val entry_date (§I) | `_purge_train` L392; applied L478 | `test_forward_chaining_expanding_and_purge` | post_purge ≤ pre each fold |
| No extra embargo (Y realized at exit) (§I) | documented in `_purge_train` docstring L392 | — | rationale recorded |
| Pooled-residual OOS R² vs train-fold M0 (§I-B1) | `_pooled_r2` L404; M0 broadcast L491; aggregate L510 | `test_m0_oos_r2_is_zero` | `M0` aggregate R² == 0.0 |
| Ridge, closed form, intercept unpenalized (§H/§I) | `ridge_fit_predict` L235 | indirectly all run tests | runs without sklearn |
| Alpha grid logspace(-3,3,13), inner 5-fold nested CV, train-only (§I-B3/§P-3) | `ALPHA_GRID` L29; `_select_alpha` L376 | exercised by run tests | `alpha_grid` len 13 in result |
| Fold-level "beat" = any positive improvement (§I-B2) | `_classify` fold_wins L431 (`M2>comp`) | `test_fold_win_threshold_requires_4_of_5` | n/a |
| Aggregate margin max(0.01 abs, 20% rel) (§I) | `_beats_aggregate` L411 | `test_beats_aggregate_absolute_floor`, `..._relative_margin` | n/a |
| Success = aggregate vs all 3 AND ≥4/5 folds each (§I) | `_classify` L424 | `test_classify_success_path`, `..._fold_win_threshold` | n/a |
| Interpretation map i/ii/iii/iv (§I) | `_classify` L424 | 4 `test_classify_*` tests | harness prints verdict cell |
| M3a: joint context row-permutation, train & val independent, interactions recomputed, master-seed offsets (§I-B4/§P-7) | `_assemble` M3a L345–350 | `test_m3a_permutes_context_but_keeps_structure` | structure preserved, rows permuted |
| M3b: 7 i.i.d. N(0,1), interactions recomputed, seeded (§I-B5/§P-7) | `_assemble` M3b L351–362 | `test_m3b_gaussian_context_shape_and_seed` | mean≈0, sd≈1, seed-stable |
| Master seed 20260516 + per-fold offsets (§P-7) | `MASTER_SEED` L28; offset `seed=master_seed+fi` L494; sub-offsets L346–356 | determinism tests | deterministic: True |
| Degeneracy guard: val block <50 or unsafe rank ⇒ cell (iv) (§I/§P-6) | `MIN_VAL_BLOCK_ROWS` L34; guard L483–489; `_classify` L427 | `test_degeneracy_guard_small_sample`, `..._small_val_block` | tiny/short samples → degenerate iv |
| Reporting fields (§J) | `run_protocol` return dict L516–540 (aggregate, fold, fold_wins, verdict, interaction count) | structure asserted across tests | harness prints all fields |
| Failure rule binding; supplementary cannot rescue (§G/§N) | `run_full_study` `note` L543 | `test_primary_is_N20` | supplementary tagged non-primary |

All 29 conformance tests pass. Full repo suite: **574 passed, 2 skipped** (the 2 skips are pre-existing gated integration tests unrelated to this module) — no regressions introduced.

### 3a. Positive control (false-negative guard)

`test_positive_control_field_modulated_signal_detected` (+ helper `_make_field_modulated_signal`) is a **synthetic-only** end-to-end positive control. It fabricates a 1,500-row frame in which `Y = log1p(abs(r))` is driven **only** by the interaction of an identity feature (`initial_risk`) with a context feature (`ctx_time_since_prior_trade`, a clean 60-trade-block 1d/8d alternation), with **no main effects** — `eta = mu + beta·(IR−IR̄)·(gap−gap̄)`, `abs(r)=expm1(eta)`. This is a genuine field-modulated identity effect that no identity/expanded-identity column can reconstruct, that the M3a/M3b broken/random context destroys, and that only M2's context + identity×context interaction block can fit.

The test asserts M2 clears the locked §I aggregate margin vs **each** of M1L/M3a/M3b, wins **≥4/5** folds vs each, `primary_success is True`, and routes to interpretation cell **(i)**. Observed separation (synthetic, not a finding): aggregate OOS R² `M2≈0.998` vs `M1≈M1L≈0`, `M3a≈M3b<0`; fold-wins 5/5/5. This confirms the M2 assembly, interaction construction, and verdict path are free of a false-negative bug — the null-on-noise harness and this positive-on-signal control together bracket the implementation. No implementation bug was found; no code change was required.

## 4. Operationalisation notes flagged for reviewer attention

These resolve text that the locked memo left to faithful implementation; none changes a locked parameter. Raised here for transparency, not as amendments:

1. **Aggregate "beat by max(0.01, 20% relative)" (§I).** Implemented as: required margin `= max(0.01, 0.20·comp_R²)` when `comp_R² > 0`, else the absolute `0.01` floor (relative term undefined for non-positive baseline). `_beats_aggregate` L411. This is the natural reading of the locked phrase; flagged for explicit confirmation.
2. **Pooled-stream tie-break (§G).** "Ordered by entry_date" with ties broken deterministically by `(entry_date, asset_rank, input_order)` so the stream is a pure function of input content. Ordering only; does not alter the locked design. `canonical_pooled_frame` L80.
3. **Undefined-window rows.** After the locked first-N warmup drop, any focal row whose context window is still empty (no resolved prior) is dropped as a well-definedness exclusion (count reported as `n_undefined_window_dropped`), analogous to the spec's "exclude if unavailable" pattern. Not a new lock; surfaced in the result dict. `run_protocol` L465–470. On the synthetic frame this count was 0.
4. **Forward-chaining block sizing (§I).** Block size `= n // (n_splits+1)`; the final validation block absorbs the remainder so no time-ordered rows are wasted. `_forward_chaining_splits` L250.
5. **`std==0 → 1.0`** in the scaler to keep standardisation deterministic on constant train columns. `Scaler.fit` L215.
6. **Ridge closed-form** (centre-then-solve, intercept unpenalised) substitutes for an sklearn estimator, which is unavailable in the environment; this is more deterministic and dependency-free, consistent with the repo's numpy-only result-defining convention.

These six are implementation operationalisations of locked text, recorded for review. If any reading is not what was intended, that is a pre-data correction to make **now**, before Gate 3 — not after.

## 5. Synthetic-run evidence (verbatim structural lines)

From `python3 scripts/synthetic_conformance_field_modulated_identity_trade_level.py` (fabricated 1,282-row frame, no real data):

```
input rows:             1282
warmup dropped:         20 (expect 20)
undefined-window drop:  0
modeling rows:          1262
n_interactions:         21 (expect 21)
context cols (7):       [7 locked names]
models:                 ['M0','M1','M1L','M2','M3a','M3b']
folds:                  5 (forward-chaining; train 210→1050 expanding; purge applied)
M0 aggregate OOS R²:    0.0   (pooled-residual baseline ≡ 0 by construction)
deterministic:          True
```

The numeric R² values on synthetic noise are not reported as findings and carry no interpretive weight — they only demonstrate the pipeline executes and the verdict logic routes (synthetic frame routed to `iii_no_field_evidence`, as expected for unstructured noise).

## 6. Posture

Implementation is complete and conformant to the locked design under review. The one-time real-data verdict run (Gate 3) is **not** performed, **not** wired, and remains separately gated. No staging or commit performed.

— end of conformance review (REVIEW-ONLY; NO REAL DATA; NOT COMMITTED) —
