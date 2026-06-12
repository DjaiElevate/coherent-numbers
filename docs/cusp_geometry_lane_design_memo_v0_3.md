# Cusp Geometry Lane — Design Memo v0.3

**Status: DRAFT FOR FREEZE.** Written before any market-data contact. Becomes FROZEN on repo
commit; the SHA of `cusp_geometry_v0_3.py` is pinned at that commit. Any post-freeze change
requires a version bump and a ledger entry. Data-contact trial counter at issue: **k = 0**.

---

## 0. Revision history

- **v0.2 → v0.3** (pre-freeze hardening, external review, k unchanged at 0):
  1. `make_records` takes nothing but `closes`; stride is no longer a parameter — the
     hidden forking path is closed in the signature itself.
  2. `purged_blocked_folds(n_records)` frozen in code (N_FOLDS = 10; contiguous blocks by
     `floor(b·n/10)`; purge 3 records/side; minimum 40 records). The evaluator may only
     consume its output, never re-decide split logic.
  3. Version bumped so every circulated artifact carries a unique (name, hash) pair; only
     the committed pair becomes canonical.

- **v0.1 → v0.2** (external review, pre-data, k unchanged at 0):
  1. Added **B6**, the linearized-curvature killer baseline (mean |Δz|).
  2. Froze **row construction** in code: `make_records(closes) → rows`; alignment, stride,
     and target timing are part of the instrument, not later plumbing.
  3. Corrected calibration wording: the module self-test is a reduced **smoke test**; the
     table of record comes from the archived calibration run defined in §5.
  4. Added **purge/embargo** to the blocked CV (3 records each side; W/stride = 63/21 = 3).
  5. (Found during implementation) Smoke-test tolerance for corr(F2, B6) corrected from a
     guessed >0.8 to the measured regime ≈0.74 (Gaussian) / ≈0.56 (t4); recorded in §5/§7.
  6. Cusp rates of record upgraded from Monte Carlo to **exact quadrature**
     (`exact_cusp_rate`), with MC retained as cross-check.

---

## 1. Question and non-goals

**Question.** Does the path geometry of volatility-standardized daily price paths carry
information about future realized volatility beyond standard trailing statistics?

**Framing (frozen):** this is not a trading rule. It is a frozen test of whether living-line
curvature geometry contains incremental information about future realized volatility beyond
simpler baselines — including its own linearization.

**Non-goals.** No direction prediction. No trading rule. No parameter search against market
data. The expected outcome is the null; a clean null closes the lane respectably.

**Provenance.** The geometry convention (cusp threshold, curvature formula) is imported
verbatim from living-line v0.3, whose literals were chosen for a 2-D navigation model with no
market intent — frozen blind with respect to this domain. All remaining choices were made in
this memo, before data contact, with synthetic-null calibration only.

---

## 2. Path embedding (the Isometry Convention)

Let `P_i` be daily closes, `r_i = ln P_i − ln P_{i−1}`.

- Lagged volatility: `σ̂_i = RMS(r_{i−63} … r_{i−1})` (63 bars, no mean subtraction,
  strictly lagged). Windows containing any undefined or zero `σ̂` are invalid.
- Standardized step: `z_i = r_i / σ̂_i`.
- Path step: `s_i = (1, z_i)`. Heading `θ_i = atan(z_i)`. Step length `|s_i| = √(1 + z_i²)`.

**Frozen aspect statement:** one bar of time has the same length as one trailing sigma of
move. Heading is a pure function of the z-score; the chart-scaling artifact dissolves.

**Deviation from the proposed cumulative form** `(t/W, (ln P_t − ln P_{t−W})/σ_W)`:
rejected — it couples vertex geometry to within-window drift and to W twice. The per-step
form makes vertex geometry local, stationary, and scale-free.

**Auto-satisfied v0.3 guards:** speed ≥ 1 always; `|Δθ| < π` by construction. Only
`θ_cusp` is active.

---

## 3. Vertex geometry (imported v0.3, unchanged)

At interior vertex i: `Δθ_i = atan(z_{i+1}) − atan(z_i)`.

- **Cusp:** `|Δθ_i| ≥ θ_cusp = 2.5` rad.
- **Regular curvature:** `κ_i = |Δθ_i| / ((|s_i| + |s_{i+1}|)/2)`.

**Market meaning of a cusp** (boundary, exact): a cusp requires the opposite step
`z₂ ≤ tan(atan(z₁) − 2.5)`:

| z₁ | required opposite z₂ |
|---|---|
| 1.4 | ≤ −46.8 |
| 2.0 | ≤ −5.56 |
| 3.0 | ≤ −3.02 |
| 5.0 | ≤ −2.10 |

A cusp is a double shock with reversal — roughly consecutive opposite ±3σ standardized moves.

**Analytic ceiling:** regular κ is maximized near symmetric z ≈ ±1.2 at κ ≈ 1.13; κ_max
pins against this ceiling in almost every window and is descriptive only.

---

## 4. Features (window W = 63 steps → 62 vertices; stride 21 bars)

For each valid window ending at step t:

- `F1_cusp_count` — number of cusp vertices. **Secondary, rare-event counter.**
- `F2_kappa_mean` — mean regular κ. **PRIMARY.**
- `F3_kappa_max` — max regular κ. Descriptive only (ceiling-limited).
- `F4_pathlen` — `Σ|s_i| / 63`. Secondary.

Validity: all z defined; at least 30 regular vertices. Invalid rows are skipped, never
imputed.

---

## 5. Null calibration of record (synthetic only; no market data)

**Rates of record — exact quadrature** (`exact_cusp_rate`; deterministic):
`P = 2 ∫_{z₁>L} f(z₁)·F(tan(atan(z₁) − 2.5)) dz₁`, `L = tan(2.5 − π/2)`; Gaussian via erf;
t(4) via the closed-form CDF `F₄(t) = 1/2 + (3/4)u − (1/4)u³`, `u = t/√(t²+4)`, unit-variance
scaled.

- iid N(0,1): **1.2312e−5** per vertex (≈ 1 per 81,000)
- iid t(4): **2.8007e−4** per vertex (≈ 1 per 3,600)

**Window statistics of record — archived run** `null_calibration(100_000, 30_000,
seed = 20260612)` (canonical generator in the module; MC vertex stream retained only as a
cross-check of the quadrature):

| quantity | iid N(0,1) | iid t(4) |
|---|---|---|
| P(window has ≥1 cusp) | 0.00067 | 0.01797 |
| F2 mean ± sd | 0.5587 ± 0.0448 | 0.5217 ± 0.0433 |
| F2 q05 / q95 | 0.4851 / 0.6328 | 0.4507 / 0.5933 |
| F3 median / q95 | 1.1136 / 1.1216 | 1.1058 / 1.1210 |
| F4 mean ± sd | 1.3546 ± 0.0510 | 1.3108 ± 0.0662 |
| B6 mean ± sd | 1.1287 ± 0.1294 | 1.0408 ± 0.1569 |
| **corr(F2, B6)** | **0.7380** | **0.5603** |

Sanity anchors: B6 Gaussian mean matches the analytic `2/√π = 1.1284`; P(window cusp) is
consistent with `62 ×` the exact rate. The **module self-test is a reduced smoke test**
(200,000 / 5,000) verifying this regime within broad tolerances; it is not the table of
record.

**Design consequences (decided pre-data):** F1 too rare for a windowed primary → rare-event
counter with the secondary descriptive hypothesis that cusps cluster at volatility-regime
breaks. F3 ceiling-pinned → descriptive. **F2 primary.** Heavier tails *lower* F2 — the
feature is not a monotone proxy for tail weight. And the corr(F2, B6) values quantify the
a-priori room for nonlinearity: under the nulls, roughly half (Gaussian) to two-thirds (t4)
of F2's variance is not linearly explained by its own linearization.

---

## 6. Target

`y_t = ln RMS(r_{t+1} … r_{t+21})` — log forward realized volatility, horizon H = 21 bars.
Stride 21 ⇒ target windows tile without overlap.

---

## 7. Baselines (B1–B5 trailing at t; B6 from the feature window)

- B1 `ln RV63`, B2 `ln RV21`
- B3 `|21-bar net log return|`
- B4 `max − min of ln P over trailing 63 bars`
- B5 `lag-1 autocorrelation of r over trailing 63 bars`
- **B6 `mean |z_{i+1} − z_i|` over the feature window — the linearized-curvature killer.**

**Pre-registered humility (updated).** For small z, `κ_i ≈ |z_{i+1} − z_i|`: F2's linear
content **is** B6. F2 counts as novel only if it adds value beyond B1–B6 — beyond its own
small-z approximation. The incremental content can live only in the tail nonlinearity (atan
compression, step-length weighting, cusp cut). Collinearity between F2 and B6 is handled by
design: evaluation is prediction-based (ΔMSE), not coefficient-significance-based, so
correlated regressors degrade nothing the protocol gates on. (Alternative B6 form — lag-1
autocorrelation of z — considered and never run; see ledger.)

---

## 8. Frozen row construction

`make_records(closes) → rows` is **part of the instrument** (module, pure, no I/O).
It takes nothing but `closes`: stride is frozen inside the function, not exposed.

- Anchor t is a step index; feature window = `z[t−62 … t]`; baselines at t; target =
  `ln RMS(r[t+1 … t+21])`. First valid anchor `t = W_SIGMA + W_FEAT − 1 = 125`; anchors
  advance by stride 21. Row = `(t, F1–F4, B1–B6, y)`. Invalid rows skipped, never imputed.
- The later loader/evaluator commit may only feed `closes` into this function; it may not
  re-decide alignment, indexing, missing-value handling, stride, or target timing.
- **Causality is tested, not assumed:** the module's lookahead perturbation test bumps a
  close inside one row's target span and asserts that the row's features and baselines are
  bit-identical while only its y changes, and that earlier rows are untouched.

---

## 9. Models, gate, and confirmation protocol

**Models.** M0: OLS `y ~ const + B1…B6`. M1: M0 + F2. Estimated on sandbox.

**Sandbox (exploratory only): SPY daily closes, 2005-01-01 … 2022-12-31** (exact frozen file
and SHA: confirm-before-freeze item). Expected usable points ≈ 208.

**Go/no-go gate (sandbox, pre-registered).** The split is **frozen in code**:
`purged_blocked_folds(n_records)` — 10 contiguous blocks (`floor(b·n/10)` boundaries);
training excludes all records within 3 records of either boundary of the test block
(rationale: W/stride = 3; the target spans 1 stride, covered); minimum 40 records. The
evaluator may only consume this output. PASS iff pooled
out-of-fold incremental R²(M1 vs M0) > 0 AND ≥ 7/10 folds improve. FAIL ⇒ lane closes with
an exploratory-null record; the seal is never opened; zero fresh-data spend.

**Confirmation (one shot).** On PASS: refit M0 and M1 on the full sandbox; freeze all
coefficients; score both frozen models on **sealed data: 2023-01-01 onward** (boundary date:
confirm item). SUCCESS iff MSE(M1) < MSE(M0) on sealed points with one-sided moving-block
bootstrap p ≤ 0.05 (block = 3 consecutive points, 10,000 resamples, seed assigned and pinned
at freeze). **Sealed attempts for this lane: hard cap 1.**

**Sign registration.** Two-sided. No theory-committed direction exists for F2; the sign is
itself a finding.

**Replication panel (secondary, descriptive, not gated).** EFA / EEM / GLD / TLT: identical
frozen pipeline, coefficients refit per asset on that asset's sandbox; report sign
consistency with SPY.

---

## 10. Multiple-testing ledger (initialized)

**Data-contact trials k = 0.** Synthetic-null calibration and quadrature are not trials.

Frozen design choices (made blind, this memo): W_σ = 63 · W = 63 · stride = 21 · H = 21 ·
θ_cusp = 2.5 (imported) · κ convention (imported) · MIN_REG = 30 · baselines B1–B6 ·
**B6 = mean |Δz|** · log-OLS spec · CV = 10 contiguous blocks · **purge = 3 records/side** ·
gate 7/10 · block bootstrap (3, 10,000) · α = 0.05 one-sided on ΔMSE · two-sided coefficient
stance · row construction per §8 (stride non-parametric) · fold plan frozen in code (N_FOLDS = 10,
`floor(b·n/10)` partition, purge 3/side, minimum 40 records) · rates of record by
quadrature; windows of record by (100,000 / 30,000, seed 20260612).

Considered and never run: W ∈ {21, 126}; H ∈ {5, 63}; rescaled θ_cusp; cumulative embedding;
direction targets; per-feature search; **B6 as lag-1 autocorrelation of z**; alternative
purge widths. Any future sandbox evaluation of a configuration not in this memo increments
k, is logged with date and motivation, and tightens the sealed α by Bonferroni across lane
versions.

---

## 11. Power note and conclusion grades

Sealed window 2023-01 … present ≈ 39 points: only large effects are detectable. A sealed
null is therefore weak evidence of absence — pre-committed B-grade language applies. A
sandbox-gate failure is an honest exploratory null and the expected outcome: **the likely
ending is that B6 (or B5) kills F2 and the lane closes cleanly.** If it survives, the sealed
test gets exactly one shot.

## 12. Divergence protocol

Any deviation from this memo — code, data handling, evaluation — is logged in a divergence
record with date and reason **before** work continues.

---

## Confirm before freeze (owner)

1. Sealed boundary date — proposed 2023-01-01 to match the program's existing seal.
2. Exact sandbox data file(s) + SHA for SPY 2005–2022 closes (and replication panel files).
3. Repo path / memo naming per program convention; then commit memo + module, pin SHA,
   assign the bootstrap seed.