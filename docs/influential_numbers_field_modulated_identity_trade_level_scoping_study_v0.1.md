# Pre-registered trade-level scoping study — different abstraction-level proxy for field-modulated identity

**Version:** v0.1
**Date:** 2026-05-16
**Project:** Coherent Numbers
**Program:** Influential Numbers (umbrella)
**Artifact type:** Pre-registered **scoping study** (CV-only). **Not** a full registered cell. **Not** the original coordinate-axis Influential-Numbers cell.
**Status:** **LOCK-ACCEPTED 2026-05-16 — DESIGN IMMUTABLE.** All §P pre-run locks resolved; lock-accepted by explicit user statement (see `…_lock_acceptance.md`). No post-hoc feature additions, threshold changes, prior-cell reinterpretation, or rescue framing; a near-miss remains a fail under §I. No data contacted. No analysis run. **Not committed, not staged.** Implementation/run/data-contact remain separately gated and are NOT authorized by this acceptance.

---

## A. Status label and scope

This is a **pre-registered trade-level scoping study — a different abstraction-level proxy for field-modulated identity**, conducted on the existing frozen trade-level substrate.

It is explicitly **not**:

- the original coordinate-axis Influential-Numbers cell (that cell is blocked on substrate-primitive definitions per `docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md`, which is retained as a failed-lock / substrate-mismatch memo, **not** a runnable pre-registration);
- a full registered (lens, asset, outcome) charter cell — it defines no sealed train/holdout path and is therefore CV-only and labelled a scoping study, not a cell (charter "Registry"; constraint 7);
- a Layer-2 rescue of any prior null.

This study is sequenced as **Step 1** of an Option-3 plan: a trade-level scoping study first; investing in the bar-level coordinate-axis substrate (define primitives, freeze a new dataset, hash it, register a separate cell) is **Step 2 and is considered only if Step 1 shows useful structure** per the §M graduation criterion. Drafting this memo does **not** commit the program to Step 2.

## B. Honest abstraction warning (load-bearing)

**This trade-level study cannot confirm or falsify the original coordinate-axis influential-numbers hypothesis.** The coordinate-axis hypothesis is about field modulation of *cluster-point identity on a price-coordinate lattice*; this study has no coordinate axis, no cluster points, and no bar-level field. It tests only whether the **broader principle of field-modulated identity has any detectable expression at the trade-event level** in the existing substrate. A positive result is a scoping signal that *may* justify building the coordinate-axis substrate; it is not evidence for the coordinate-axis hypothesis itself. A null result does not falsify the coordinate-axis hypothesis.

This study **stands on its own grounds.** Its justification is the §D research question, not any prior cell's outcome. Per the governance constraints:

- It does **not** reinterpret, rescue, reopen, or re-run Cell 1 (closed Class 3, `5745722`), Candidate B (not-confirmed split-null), or Candidate C (`12-privileged`). Those verdicts are independent and unaffected by any outcome here, in either direction.
- It does **not** borrow Kryon-source authority. The Kryon source authorizes linear-integer neighborhood influence only; a continuous trade-event context vector with interactions is a researcher-side construct and is labelled as such. No source text is cited as evidence anywhere in this study.
- It uses neutral construct language only: **response magnitude**, **outcome variation**, **trade-event context**, **recent-window state**. The body-model vocabulary is not used and is not adopted as a construct descriptor.

## C. Purpose and research question

**Purpose:** test whether the field/context around a trade-event modulates the relationship between trade identity and trade response.

**Research question:** does trade-event context improve out-of-sample explanation of trade response **beyond identity-only and expanded-identity controls**?

**Important distinction (the three competing readings):**

- **Identity-only effect:** intrinsic trade/event features explain response.
- **Expanded-identity effect:** additional non-context descriptors (asset identity, calendar identity) explain response.
- **Field-modulated identity effect:** recent-window trade-event context changes how identity expresses, producing improved out-of-sample prediction **beyond both** identity-only and expanded-identity controls.

The affirmative claim is licensed **only** by the field-modulated reading as operationalized by the §I success criterion against the expanded-identity control M1L and the two negative controls M3a/M3b. An identity-only or expanded-identity-only signal is explicitly not this study's hypothesis (§F, §N).

## D. Outcome (Y) — selection criterion and lock

**Selection criterion (stated before choosing Y).** The primary Y must have: (1) continuous variation; (2) a plausible identity relationship that context could modulate; (3) no target leakage from features; (4) enough variance to model; (5) availability in the existing trade-level substrate.

**Candidate Y discussion.**

| Candidate | Assessment |
|---|---|
| absolute R-multiple magnitude | Continuous, directionless, outcome-variation oriented; the closest trade-level analog to "response magnitude." Meets all five criteria. |
| signed R-multiple | Mixes direction and magnitude; would test directional prediction, a different question, not chosen as primary (no justification offered to combine direction and magnitude here). |
| `first_target_hit` (binary) | Binary collapses information; not primary. Retained only as an optional binary **secondary** descriptor, not a predictive target, not verdict-bearing. |
| `bars_held` / time-stop behavior | Outcome-side timing; supplementary only, never primary, never an identity feature. |

**Locked primary Y:** `Y = log1p(abs(r_multiple))`, the trade-level response-magnitude proxy. Directionless, continuous, outcome-variation oriented. `r_multiple` is read directly from the frozen Phase 3b artifact (it is a realized trade outcome; see §L data-contact disclosure).

**Secondary (non-verdict, descriptive only):** `first_target_hit` as a binary descriptor; `bars_held` as a supplementary continuous descriptor. Neither can rescue, upgrade, or alter the primary verdict.

## E. Identity features (M1)

Only features intrinsic to the trade/setup and available **at or before entry**:

- `direction` (long/short).
- `initial_risk`.
- `log(entry_price)`, standardized **within asset** using **training-fold statistics only** — see entry-price lock below.
- Calendar descriptors of `entry_date`: day-of-week, month-of-year (calendar identity; their assignment to M1 vs M1L is fixed in §F — calendar identity is an *expanded-identity* control, so the M1 calendar content is empty and these enter at M1L).

`entry_date` is the trade's calendar-assignment date because it is the latest pre-outcome decision/observation timestamp for the trade. `setup_date` is not used as the assignment date (it precedes entry and adds no pre-entry information beyond `entry_date`).

**Leakage exclusions (locked):** `exit_reason`, `exit_date`, `exit_price`, `bars_held`, `first_target_hit`, and `r_multiple` itself are **outcome-side** and are **never** identity or context features. `exit_reason` may appear only later as descriptive segmentation, never as a predictive feature.

**Entry-price normalization lock:** if entry price is used, it enters as `log(entry_price)`, standardized within asset using training-fold mean/std only; validation rows are transformed with the corresponding train-fold scaler. **No tunable rolling normalization window** is introduced; any such window would be a separate pre-run lock and is not adopted here.

## F. Expanded-identity control (M1L analog)

M1L preserves its structural role from the coordinate-axis design: it tests whether a **broader identity description wins without context**.

**Trade-level M1L = M1 + asset fixed effects + calendar identity controls**, where:

- asset fixed effects = indicator contrasts over `{SPY, EFA, EEM, GLD, TLT}` (multi-asset substrate);
- calendar identity controls = **day-of-week and month-of-year of `entry_date` only (LOCKED).** Quarter is **excluded** because it is redundant with month-of-year and adds rank/collinearity risk for no incremental identity content.

Calendar identity controls enter M1L only as expanded-identity controls and are deliberately excluded from the interaction block; therefore this scoping study tests whether recent-window context modulates substantive trade identity features, not whether it modulates calendar identity.

**mod-7 / mod-10 (or any modular-lattice) identity are NOT forced in.** Lattice identity is a coordinate-axis-level construct; at trade level it is not part of the hypothesis and is not justified pre-results, so it is excluded. Adopting it later would require separate pre-run justification.

**Interpretive rule (binding):** if M1L beats M1 but M2 does **not** meaningfully beat M1L (per §I), the licensed conclusion is **"expanded identity may matter," not "field-modulated identity."**

## G. Context features (recent-window state)

Recent-window summaries from the **trade sequence**, not any price-axis neighborhood. Every context feature uses **only information available before the focal trade's entry**.

**Window leakage lock.** A prior trade's outcome (`r_multiple`, win/loss) is only known at that trade's `exit_date`. Any context feature that summarizes prior *outcomes* is computed over the most recent N prior trades **whose `exit_date` is strictly before the focal trade's `entry_date`** (resolved-before-entry constraint). Context features that use only prior *entry-time* information (timing, direction, frequency) use the most recent N prior trades by `entry_date` with `entry_date` strictly before the focal `entry_date`.

**Primary recent-window:** `N = 20` prior trades. **Supplementary (non-primary):** `N = 10` and `N = 40`. The primary result is **not** rescued or reinterpreted by N=10 or N=40 if N=20 fails.

**Context features (all 7 LOCKED IN):**

- time since prior trade (entry-time info; no outcome leakage)
- recent mean R over previous N resolved trades (resolved-before-entry)
- recent win rate over previous N resolved trades (resolved-before-entry)
- recent volatility / std of R over previous N resolved trades (resolved-before-entry)
- recent long/short imbalance over previous N prior trades (direction known at entry)
- recent trade frequency / clustering in calendar time over the prior window (entry-time info)
- recent mean absolute R over previous N resolved trades (resolved-before-entry)
- asset/regime indicators are **not** added as context (they duplicate the §F expanded-identity controls)

*Rationale for locking all 7:* ridge absorbs the expected multicollinearity among the recent-window summaries; the scoping purpose is to test whether trade-level recent-window state has **any** detectable field-modulation expression, not to optimize interpretability at this stage. This fixes the context block at **7 columns**.

**Prior-trade sequence (LOCKED): a single pooled stream ordered by `entry_date`** with the resolved-before-entry constraint, so "context" is genuine cross-asset recent-window state. *Rationale:* per-asset sequencing may be conceptually cleaner later, but running both now creates a rescue path. If pooled is positive, per-asset is a legitimate follow-up; if pooled is null, per-asset is a separate future hypothesis, **not** a rescue of this study.

**Warmup exclusion (LOCKED):** the primary N=20 sample **drops the first 20 trades** of the pooled stream; the N=40 robustness sample drops the first 40; the N=10 robustness sample drops the first 10. Each N runs on its own warmup-excluded sample.

## H. Models

| Model | Definition |
|---|---|
| `M0` | marginal mean (train-fold mean of Y, broadcast to validation) |
| `M1` | identity only (§E) |
| `M1L` | expanded identity only = M1 + asset fixed effects + calendar identity controls (§F) |
| `M2` | M1L + context + (primary-identity × context) interactions |
| `M3a` | M1L + **shuffled** context + same interaction structure |
| `M3b` | M1L + **random Gaussian** context + same interaction structure |

- **Estimator:** ridge regression.
- **Standardization:** all continuous features standardized using **training-fold statistics only**; validation transformed with the train-fold scaler. Indicator/dummy columns are not standardized. No validation/test leakage.
- **Interactions (LOCKED):** the interaction block crosses **3 identity columns — `direction`, `initial_risk`, `log(entry_price)` — with the 7 context features = 21 identity × context interaction terms.** This 21-term count is recorded at lock and is **not** "corrected" afterward. Interactions are included in M2, M3a, and M3b with the **same 21-term dimensional structure** across all three, so "field improves prediction" cannot be an artifact of added column count or interaction flexibility. Calendar and asset identity (M1L expanded-identity controls) are **not** in the interaction block.

  Calendar identity controls enter M1L only as expanded-identity controls and are deliberately excluded from the interaction block; therefore this scoping study tests whether recent-window context modulates substantive trade identity features, not whether it modulates calendar identity.

## I. Validation and success/failure threshold

**Cross-validation (LOCKED).** Time-respecting **5-fold forward-chaining (expanding-window)** CV on the pooled stream ordered by `entry_date` (each fold trains on the past, validates on the next contiguous block; no future data predicts past data). *Disclosure:* Fold 1 will likely carry the highest variance because it has the least training data; this is expected and is not grounds for post-hoc fold reweighting. All feature engineering, standardization, within-asset entry-price scaling, ridge-penalty selection, and shuffle/Gaussian generation are fitted **inside train folds only**.

**Embargo / purge.** `Y = log1p(abs(r_multiple))` is fully realized at the trade's `exit_date`; there is no forward horizon beyond trade exit. The only leakage channel is **trade-interval overlap** across a fold boundary. Locked rule: a training trade is **purged** if its `exit_date` is on or after the first `entry_date` of its validation block (its outcome was not resolved when the validation period began). No additional bar/day embargo is required because Y encodes no information past `exit_date`; this rationale is recorded as the explicit embargo justification.

**Threshold (locked candidate).** M2 must beat M1L, M3a, and M3b by:

> `max(0.01 absolute OOS R², 20% relative improvement)` on aggregate,

**and** M2 must beat each comparator in at least **4 of 5** folds.

**B1 — OOS R² aggregation (recommended, justified pre-results):** **pooled-residual method.** Concatenate each model's out-of-fold predictions across all 5 validation blocks into one OOS prediction vector, then compute a single R² as `R²_OOS = 1 − Σ(y − ŷ_model)² / Σ(y − ŷ_M0)²`, where `ŷ_M0` is the train-fold marginal mean broadcast to each validation block. *Justification:* with ~1,282 trades / 5 folds (~250 validation rows each), per-fold R² is high-variance and the denominator differs across folds; the pooled estimator gives one stable number with a single, well-defined baseline, makes `M0`'s OOS R² identically 0, and makes "beat" unambiguous and baseline-consistent across all models. (Mean-of-fold R² is reported as supplementary texture only.)

**B2 — fold-level "beat" (recommended, justified pre-results):** fold-level "beat" = **any strictly positive improvement** in that fold's pooled-baseline OOS R² (M2 > comparator in that fold). *Justification:* the magnitude gate (`max(0.01, 20%)`) is enforced once, at aggregate, where the estimate is stable; the per-fold ≥4/5 requirement is a **sign-consistency / robustness** check, not a second magnitude test. Re-applying the magnitude margin at fold level would double-penalize against per-fold sampling variance at ~250 rows/fold and is not adopted.

**B3 — ridge penalty selection (LOCKED):** **nested CV inside each training fold.** Within each outer training set, an inner forward-chaining 5-fold CV selects `alpha` from the locked grid `np.logspace(-3, 3, 13)`; the selected `alpha` is refit on the full outer training set and applied to the outer validation block. The inner procedure never sees the outer validation rows. *Justification:* a single preselected `alpha` is fragile to fold-specific standardized-feature scaling; nested CV keeps penalty selection strictly train-only and avoids a tuned-on-test artifact.

**B4 — M3a shuffle (locked):** the entire **context block is row-permuted jointly** (preserving each row's internal cross-context correlation, destroying only the trade↔context linkage), with an independent permutation generated **within the training fold** and a separate independent permutation **within each validation block** — the validation target is never used to construct any permutation. Interactions are **recomputed from the shuffled context** so M3a's column structure is identical to M2's (21 interaction terms). Permutation RNG is derived from the locked master seed **20260516** with documented per-fold offsets.

**B5 — M3b Gaussian context (locked):** replace the 7-column context block with **7** i.i.d. standard-normal columns drawn at the post-standardization scale (mean 0, sd 1) from a fixed-seed RNG (master seed **20260516**, per-fold offsets) with independent train and validation draws. Interactions are recomputed from the Gaussian draws so the column structure matches M2.

**Interpretation map (light, consistent with §F/§N):** (i) *field-modulated supported* — M2 clears the §I criterion against all of M1L/M3a/M3b; (ii) *expanded-identity-only* — M1L>M1 but M2 fails the criterion vs M1L → "expanded identity may matter," not field-modulated; (iii) *no field evidence* — M2 fails and M1L does not beat M1; (iv) *non-confirmatory / degenerate* — the **locked degeneracy guard** tripped (any validation block has fewer than 50 rows after all exclusions/purges, or the model design is rank-degenerate in a way ridge/encoding cannot safely handle); beat numbers reported as texture only, no upgrade.

## J. Reporting requirements

The results artifact must report: aggregate OOS R² for each model (pooled-residual, B1); fold-level OOS R² for each model; M2-vs-{M1L, M3a, M3b} fold-win counts; the primary success/failure verdict and which interpretation-map cell it lands in; ridge-coefficient summaries or ablation contributions for the interaction terms; an explicit statement of whether any positive result is **concentrated in a small number of interaction terms or diffuse across many**; and the supplementary N=10 and N=40 results clearly marked non-primary. Mean-of-fold R² reported as supplementary only.

## K. Power / noise-floor disclosure (required)

The raw frozen substrate is 1,282 trades; the locked §G warmup exclusion (drop first 20) makes the **primary N=20 modeling sample N≈1,262**. With 5-fold CV and identity + expanded-identity + context + interaction terms, feature dimensionality may reach 30+ columns (asset and calendar dummies plus context plus the identity×context interaction block). Ridge handles this mechanically, but effective signal-to-noise is low and a `0.01` absolute OOS R² threshold sits **near the practical noise floor** at this sample size.

**Low signal-to-noise at approximately N≈1,262 means a null result is not strongly informative on its own, but it remains a null per the pre-committed §I criterion.** This disclosure limits *interpretive strength only*; it does **not** change the threshold and does **not** weaken the locked success/failure rule. It changes interpretation:

- a positive result is a **scoping signal, not confirmation**;
- a null result is **not a definitive falsification** of the coordinate-axis hypothesis;
- the result is **one input** into whether a larger registered cell is worth building;
- a primary fail remains a fail under the locked §I criterion: a near-miss is a fail, not an ambiguous result, and low signal-to-noise is **not** grounds to rescue, soften, or re-interpret a result that does not clear §I.

## L. Independence / data-contact disclosure

**This study OVERLAPS prior work and independence is limited; the overlap is named here, not left implicit.**

- **Same rows.** This study uses the *identical* frozen pullback × pooled Phase 3b 1,282-trade substrate (SPY/EFA/EEM/GLD/TLT, 2005–2022; freeze manifest `docs/pullback_population_freeze_manifest_v0.1.md`, freeze commit `5225bfd`) previously analyzed by Candidate B, Candidate C, and Influential Numbers Cell 1. The rows are not independent of those analyses.
- **Different question / different target.** Candidate B/C and Cell 1 used a calendar-phase lens over `entry_date` with `is_long` as the only permuted quantity and never used `r_multiple` as an outcome. This study uses `Y = log1p(abs(r_multiple))` and trade-sequence recent-window context. The question and the response variable differ, but the substrate does not — so any "independence from prior cells" claim is limited to *question/target* independence, not *data* independence.
- **Prior contact with the target itself.** `r_multiple` is a realized pullback-trade outcome generated by the sealed pullback program under `BacktestParams` locked early at pullback commit `50ee2d1` (not re-tuned). The pullback Phase 1–3b series were inspected and partitioned during pullback research before Coherent Numbers contacted them. `Y` here is therefore a previously-contacted quantity, not a fresh outcome; this is disclosed, not hashed away.
- **OOS sealing.** The substrate ends 2022; OOS 2023+ remains sealed in both repos and is **not** accessed. This study defines no holdout into sealed data; it is CV-only by construction (hence "scoping study," not "registered cell").
- The pullback_research repo is **not** touched at design, lock, or run time.

## M. Scoping-to-cell graduation criterion (defined before results)

A scoping result justifies moving to a full registered cell (coordinate-axis Step 2, or a narrower trade-level cell) **only if all of**:

1. M2 passes the §I primary success criterion;
2. the improvement over M1L is **not solely driven by one obvious calendar/asset confound** (checked via the §J interaction-concentration report and an M1L-ablation read);
3. the interaction contribution is interpretable enough to **specify a narrower registered hypothesis**;
4. supplementary N=10 and N=40 **do not directly contradict** the primary result;
5. the memo for the next step can **name what would be frozen**: substrate, asset universe, train/holdout split, and feature definitions.

If these do not all hold, the scoping study may still be informative but does **not** justify immediate cell registration. Graduation is never automatic and is itself a separate pre-registered decision.

## N. Failure rule (binding)

If M2 does not pass the locked §I success criterion: **the trade-level field-modulated identity hypothesis is not supported as operationalized.** No post-hoc feature additions. No rescue. No reinterpretation of Cell 1, Candidate B, or Candidate C. Any reframe must explicitly name **what the failed operationalization conceded** (e.g., trade-level abstraction, the specific context set, the ~noise-floor threshold, the overlapping substrate).

## O. Pre-registration discipline

All §P items are resolved (locked 2026-05-16). No feature, model fit, fold split, permutation, Gaussian draw, or summary statistic is computed against the substrate until this memo is **lock-accepted** and that acceptance is explicitly granted. A preview is a computation. The verdict run occurs exactly once. No commit without explicit user approval.

## P. Resolved pre-run locks (all decided; LOCKED)

All §P items are resolved by explicit user decision dated 2026-05-16. No item remains open.

1. **Context feature set — LOCKED:** all 7 features (§G) in. Context block = 7 columns. Rationale: ridge absorbs multicollinearity; scoping tests *any* detectable expression, not interpretability optimization.
2. **Prior-trade sequence — LOCKED:** single pooled stream ordered by `entry_date` with the resolved-before-entry constraint. Rationale: running both pooled and per-asset now would create a rescue path; per-asset is a separate future hypothesis, not a rescue.
3. **Ridge penalty — LOCKED:** grid `np.logspace(-3, 3, 13)`, inner forward-chaining 5-fold CV inside each training fold.
4. **Calendar controls — LOCKED:** day-of-week + month-of-year only; quarter excluded (redundant with month, rank/collinearity risk).
5. **Interaction block — LOCKED:** identity columns `direction`, `initial_risk`, `log(entry_price)` × 7 context features = **21** identity × context interaction terms. Calendar/asset identity excluded from interactions (clarification sentence added to §F and §H).
6. **Degeneracy guard — LOCKED:** abort to interpretation-map cell (iv) if any validation block has < 50 rows after all exclusions/purges, or if the design is rank-degenerate in a way ridge/encoding cannot safely handle.
7. **Master seed — LOCKED:** `20260516`, with documented per-fold offsets, for M3a permutations and M3b Gaussian draws.
8. **Fold structure — LOCKED:** 5-fold forward-chaining expanding-window. Disclosed: Fold 1 carries the highest variance (least training data); not grounds for post-hoc reweighting.
9. **Warmup exclusion — LOCKED:** drop first 20 trades for the N=20 primary sample; first 40 for N=40; first 10 for N=10; each N on its own warmup-excluded sample.

With all §P items locked, the only remaining gate before a verdict run is explicit lock-acceptance (drafted separately in `docs/influential_numbers_field_modulated_identity_trade_level_scoping_study_v0.1_lock_acceptance.md`). Nothing has been implemented, run, committed, or contacted.

— end of draft scoping-study memo (NOT LOCKED) —
