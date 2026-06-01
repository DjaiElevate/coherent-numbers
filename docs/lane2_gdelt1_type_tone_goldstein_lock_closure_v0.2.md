# Lane 2 — Type / Tone / Goldstein Lock-Closure Design Memo (v0.2, LOCK-CLOSED)

## 1. Title and status

**Document type:** **Lock-closed v0.2 design memo.** It fixes, to single values, the type/tone/Goldstein extraction design locks left open by the v0.1 design memo (`0295406`, §23 decisions 1–4) and their dependent formula/method locks. It is **design-only**.

**THIS IS NOT AN EXECUTION AUTHORIZATION.**
**NO DATA CONTACT IS AUTHORIZED.**
**NO EXTRACTION IS AUTHORIZED.**

This memo authorizes nothing: no GDELT contact, no raw event-file read, no extraction, no feature build, no 2023+ read, no market-data join, no outcome computation, no result generation, no implementation, no staging, no commit, no push. It records fixed lock values, an algebraic (formula-only) pre-check, and the specification of empirical checks to be run later under their own gates. All locked values remain inert design text until a later, separately-initiated execution-authorization prompt adopts them and V1/V2 (§20) pass.

| Field | Value |
|---|---|
| Date of draft | 2026-06-01 |
| Canonical HEAD at drafting | `02954069e1e2b0491aba533dda7dee798d6e26c8` (`0295406`) == `origin/main` |
| Design baseline | `0295406` (type/tone/Goldstein extraction design memo v0.1) |
| Governing divergence record | `219f37c` |
| Status | **LOCK-CLOSED (design-only)** — not authorizing |
| 2023+ OOS seal | Sealed; this memo keeps it sealed |
| Locks addressed | v0.1 §23 decisions 1–4 + dependent formula/method locks |

---

## 2. Lineage

- **`219f37c` — divergence record.** Caps the post-`cb1122a` ungated market-data acquisition + next-session-return join arc (`4f31bcb`, `6a75ec7`) as EXPLORATORY-ONLY; records the governance gap (no execution guard, no conformance artifacts) and the intact 2023+ seal.
- **`0295406` — design baseline (v0.1).** Locks the mechanism (intensity/valence pressure, not amount), the primary outcome (`abs(next_session_return)`), the single composite (`intensity_valence_pressure`), the incremental-over-volume requirement, the negativity-only assumption, the no-rescue rule, frozen-from-in-sample standardization, strict 2023+ seal, and the §18 guard / §19 conformance-artifact requirements. Leaves §23 decisions 1–4 open and flagged LOCKS REQUIRED BEFORE THE EXTRACTION GATE.
- **v0.2 is a tracked diff against the committed v0.1 design baseline.** It does not restate or revise v0.1's locked mechanism, outcome, or sealing posture; it closes the four open locks to single values plus their dependent formula/method locks. Where this memo and v0.1 conflict, v0.1 governs until v0.2 is itself committed.

---

## 3. Scope

This memo closes decisions 1–4 from v0.1 §23 and their dependents:

1. coverage-denominator definition (§5);
2. material-conflict share/intensity formula (§7);
3. standardization scaler + warmup thresholds (§12);
4. drift-control recipe + planted-signal strength/threshold (§13).

It additionally closes the two non-`§23`-listed component formulas (negative structural-impact §8, negative-tone §9), the single in-scope event universe (§6), the share-of-total interpretation (§10), the degenerate-case / missing-value policy (§16), and the minimum-denominator floor (§17); specifies the algebraic pre-check (§4A) and the empirical costume check (§4B); and fixes the reporting specs for component-collinearity (§15) and excluded-mention diagnostics (§20 R1/R2).

**Out of scope / not authorized here:** extraction, execution, outcome join, OOS unsealing, implementation, and any data contact.

### 3.1 High-frequency scope limit (what this design can and cannot conclude)

- **This design targets a daily lead-lag effect:** whether high intensity/valence pressure **on the feature date** predicts higher **next-session** magnitude. It is a high-frequency, day-to-day test.
- **The expanding past-only scaler (§12) and the drift controls (§13) intentionally remove or suppress slow, low-frequency / regime-level variation.** This is deliberate: the volume-only null was driven by exactly such slow structure.
- **Consequence:** a **null under this design does not rule out a regime-level relationship** such as "high-conflict *periods* run hotter." Such an effect lives at a frequency this design deliberately filters out.
- **This is a scope limit, not a flaw.** A regime-level / low-frequency conflict→volatility question is a *distinct* hypothesis requiring its own separately-gated design; it must not be back-read into, or rescued from, this daily-lead-lag null.

---

## 4. Volume / coverage-quality costume control — two distinct checks

The volume-costume concern is split into **two distinct checks at two distinct gates.** The earlier draft incorrectly framed the *empirical* check as a precondition for lock closure; that is corrected here.

### 4A. Algebraic volume-costume pre-check — gates LOCK CLOSURE (design-only)

- This is **design-only and uses formulas only.** It **does not** compute a composite from extracted data, **does not** read GDELT content fields, **does not** require extraction, and **does not** use market outcomes or 2023+.
- It confirms, **by formula inspection**, that the proposed composite is not algebraically identical to raw volume nor a direct monotone transform of volume.
- It must explicitly state: **share-of-total formulas reduce raw-volume dependence but do not prove empirical independence from volume; therefore the empirical check (§4B) remains required later.**

**Algebraic pre-check record — VERDICT: PASS.**
Reasoning:
- F1, F2, and F3 (§7–§9) are **ratios of negative/conflict mention-mass to a common total in-scope mention denominator** (§5/§6);
- the components are therefore **scale-free shares/intensities, not raw volume counts**;
- the **equal-weight composite of standardized components is not algebraically identical to total volume** nor a direct monotone transform of volume;
- **however**, the formulas can still **empirically covary** with volume/coverage-quality, so the **empirical costume check (§4B) remains required** after extraction and **before any outcome join.**

Because §4A is design-only and records PASS, it **does not block** lock closure; the locks below are closed on the strength of the algebraic argument, with the empirical check deferred to §4B.

### 4B. Empirical volume / coverage-quality costume check — gates OUTCOME JOIN, not lock closure

- Occurs **only after** a properly gated extraction has produced an **in-sample extracted composite**, and **before any market outcome join.**
- **Must NOT use:** `next_session_return`; `abs(next_session_return)`; any market outcome; any 2023+ data.
- Uses **only** the extracted in-sample composite/components and the locked volume/coverage-quality controls (§14).
- **Reports:** linear composite-on-volume **R²**, and **Spearman/rank** monotone association (catches monotone-nonlinear costumes).
- **C1 — LOCKED thresholds:**
  - Linear R²: **PASS** R² < 0.25; **CAUTION** 0.25 ≤ R² < 0.50; **FAIL** R² ≥ 0.50.
  - Spearman/rank (|ρ|): **PASS** |ρ| < 0.50; **CAUTION** 0.50 ≤ |ρ| < 0.70; **FAIL** |ρ| ≥ 0.70.
- **On FAIL:** **stop**; do **not** revise formulas inline; do **not** tune the same extraction; **require a new design-review memo and a new gate.** A fail must **not** trigger "revise-and-re-extract" inside the same gate (that would be a tuning loop).
- **On CAUTION:** explicit caution labeling is required before any outcome join proceeds.

---

## 5. Lock 1 — coverage denominator (S1, LOCKED)

**LOCKED:** the common daily-normalization denominator for all three primary components is **total daily `NumMentions` summed over the single in-scope event universe (§6)** for that information date.

- The denominator must be the **whole in-scope daily attention field, not a component-specific valid subset.**
- **Why this matches the v0.1 mechanism:** `NumMentions` is the v0.1-locked coverage weight; normalizing each pressure numerator by the same daily `NumMentions` total expresses every component as a *share of the day's mention-weighted attention* — "what fraction of today's attention is conflict / negative-impact / negative-tone," holding amount fixed.
- **Why it is not a raw-volume proxy:** dividing by total daily `NumMentions` removes the day's overall scale; a mention-share is scale-free by construction (see §4A PASS).
- **Small-denominator caveat:** share-of-total is high-variance when the denominator is small; the minimum effective-sample floor (§17, M1) and degenerate-case policy (§16, F4) govern this.

---

## 6. In-scope event universe (single definition, applied identically)

The **in-scope event universe** is the set of GDELT Event records, attributed to an information date by the project's locked row-date rule (v0.1 §10), eligible to contribute to the daily aggregates. Defined **once** and applied **identically** to every numerator and denominator.

- **All three primary components (§7–§9) use the same in-scope event universe.**
- **Numerator and denominator are drawn from the same daily universe.** The Lock 1 denominator (§5) is total `NumMentions` over exactly this universe; each component numerator is a sub-sum over the same universe.
- **No component may use a narrower denominator than another.** Per-component field-validity (missing `GoldsteinScale`/`AvgTone`) affects only that component's **numerator**, never the **common denominator** (§8/§9/§16); excluded-field mention fractions are reported (R2).
- **If future schema verification (V1/V2) forces exclusions**, they must be **declared before extraction** and applied **consistently** across all components.

---

## 7. Lock 2 — material-conflict pressure (F1, LOCKED)

**LOCKED:** mention-weighted **`QuadClass = 4` share**.
- numerator = Σ `NumMentions` for in-scope events with `QuadClass = 4` (material conflict) on the information date;
- denominator = total daily `NumMentions` over the **same in-scope event universe** (§5/§6);
- component = numerator / denominator (dimensionless share ∈ [0, 1]).

- **Fixity:** no alternative material-conflict formula (raw count, intensity sum, multi-`QuadClass` grouping, event-rate) may be selected after seeing any outcome result; alternatives are non-primary sensitivities requiring their own pre-registration (v0.1 §6/§7/§12).
- **Degenerate handling:** zero / sub-floor denominator days → §16 + §17.

---

## 8. Negative structural-impact pressure (F2, LOCKED)

**LOCKED — share-of-total negative structural pressure:**
- numerator = Σ `NumMentions × max(0, −GoldsteinScale)` over the in-scope universe on the information date (negative structural-impact **mention-mass**);
- denominator = total daily `NumMentions` over the **same in-scope event universe** (§5/§6);
- component = numerator / denominator (see §10).

- **Missing/non-numeric `GoldsteinScale` does NOT shrink the denominator.** Such a row contributes **0 to the Goldstein numerator** while its `NumMentions` **remains in the common denominator.**
- Positive-Goldstein (cooperative) events contribute 0 to the numerator (negativity-only, v0.1) but remain in the denominator.
- **Value range:** `GoldsteinScale` nominally [−10, +10]; `max(0, −GoldsteinScale)` ∈ [0, 10].
- **Report** the Goldstein missing/excluded-field mention fraction as an **R2** coverage-quality diagnostic.

---

## 9. Negative-tone pressure (F3, LOCKED)

**LOCKED — share-of-total negative-tone pressure:**
- numerator = Σ `NumMentions × max(0, −AvgTone)` over the in-scope universe on the information date (negative-tone **mention-mass**);
- denominator = total daily `NumMentions` over the **same in-scope event universe** (§5/§6);
- component = numerator / denominator (see §10).

- **Missing/non-numeric `AvgTone` does NOT shrink the denominator.** Such a row contributes **0 to the tone numerator** while its `NumMentions` **remains in the common denominator.**
- Positive-tone events contribute 0 to the numerator but remain in the denominator.
- **Value range:** `AvgTone` nominally ~[−100, +100] (commonly [−15, +15]); `max(0, −AvgTone)` ≥ 0.
- **Report** the AvgTone missing/excluded-field mention fraction as an **R2** coverage-quality diagnostic.

---

## 10. Share-of-total denominator interpretation (S2, LOCKED)

**LOCKED — share-of-total negative pressure.**
- Each component's **numerator is the negative-pressure mention-mass**; the **denominator is total daily `NumMentions` over the same in-scope universe** (§5/§6).
- **Interpretation:** *"How much of the whole daily attention field is negative / conflictual / impactful?"* — not "how negative *only the negative subset* was."
- **Negative-subset-normalized alternatives** (dividing by the mention-mass of only the negative/eligible subset) are **non-primary sensitivities or future hypotheses only.** They are **not co-primary.**

---

## 11. Composite construction

- **Composite:** `intensity_valence_pressure` (v0.1).
- **Construction:** (1) compute the three daily components (§7–§9); (2) standardize each with the locked scaler (§12); (3) combine with **equal weights** (1/3 each).
- **Fixed weighting:** weights are fixed and **not optimized** against any outcome or in-sample fit.
- **No-rescue (v0.1 §13):** no single component can rescue or overturn a null composite; a strong component under a null composite is exploratory only and may motivate a *future* pre-registration, never a salvage.

---

## 12. Lock 3 — scaler and warmup (Z1, LOCKED)

**LOCKED — leakage-safe expanding-window, past-only z-score per component:**
- at information date *t*, standardize component *x* using `mean`/`std` over `{x_s : s < t, s a valid in-sample day}` (strictly prior valid days only — no current or future day);
- **Warmup:** **365 prior valid in-scope days** required before a standardized value is valid;
- **Sub-warmup days → NaN / excluded**, not imputed;
- **OOS freezing (v0.1 §16):** for any future OOS confirmation, scaler `mean`/`std` (and any threshold/denominator parameters) are **learned on the pre-OOS training window only and frozen**, then carried into 2023+ unchanged. **No refit on OOS.**
- **Scope-limit note:** this scaler is, by design, a high-frequency filter (§3.1) — it suppresses slow/regime-level level shifts.

---

## 13. Lock 4 — drift / volume-control + planted-signal (Z2, P1, P2, Y1, LOCKED)

### 13.1 Z2 — fixed controlled-association sequence (LOCKED)

The primary controlled association uses this **fixed sequence**:
1. construct raw daily components (§7–§9);
2. apply expanding past-only z-score (§12);
3. equal-weight the three standardized components into `intensity_valence_pressure` (§11);
4. control for time/drift (partial-time / monotone-trend control);
5. control for the small locked volume/coverage-quality control set (§14);
6. evaluate the primary association with `abs(next_session_return)` **only after a separately authorized outcome join.**

**Locked volume/coverage-quality controls:** `log1p_total_row_count`; `roll_mean_log1p_total_w30`; `coverage_completeness`.
- **`coverage_completeness` is a coverage-quality / substrate-quality control, not pure volume.**
- **Do not** expand to all 54 volume/coverage features; **do not** choose controls post-hoc.

### 13.2 Y1 — per-year stability criterion (LOCKED)

- **Report** the controlled association **per calendar year** for every year with **at least 100 valid paired observations**; report sign and magnitude per valid year.
- **PASS:** at least **70%** of valid years share the same sign as the pooled controlled association **and** no 1–2 years solely carry the pooled result.
- **CAUTION:** **50% to <70%** of valid years agree in sign, **or** evidence appears materially concentrated in 1–2 years.
- **FAIL / UNINTERPRETABLE:** **<50%** of valid years agree in sign, **or** fewer than **5** valid years exist, **or** the pooled association is clearly carried by 1–2 years.
- **Per-year FAIL can block interpretation.** The per-year check is **not a rescue mechanism.**

### 13.3 P1 — planted-signal construction (LOCKED)

- Uses a **synthetic surrogate target only**; **never** uses `next_session_return`, `abs(next_session_return)`, any market outcome, or 2023+ data.
- Injects the planted signal at the **raw-component or pre-standardization composite level**.
- Runs through the **full stack:** standardization (§12) → drift/time control → per-year check (§13.2) → incremental-over-volume control (§14).
- Signal character must be **daily / high-frequency lead-lag**, **not** trend-shaped or regime-shaped. A **trend-shaped planted signal should be killed by this design and therefore must not be used for this diagnostic** (using one would falsely label the pipeline "too aggressive").
- **Deterministic fixed seed = `1729`** for any synthetic noise.

### 13.4 P2 — planted-signal retention grid + binding criterion (LOCKED)

- **Grid:** `rho_plant = {0.05, 0.10, 0.20}`; **report retention across the full grid** (fraction of the planted partial correlation retained after the full stack, with sign).
- **Binding criterion is at the floor:**
  - **PASS only if `rho_plant = 0.05` is retained with the same sign and ≥ 50% retention** after the full stack;
  - **FAIL if the 0.05 plant falls below 50% retention or flips sign.**
- The **0.10 and 0.20** plants are reported as detection-floor diagnostics but **cannot rescue failure at 0.05.**
- This makes the diagnostic answer whether the pipeline preserves the **smallest signal the design cares about.** A FAIL means a subsequent real null is uninterpretable (cannot distinguish "no signal" from "signal erased"); the recipe must be revised through a new gate (v0.1 §11 anti-ambiguity requirement).

---

## 14. Incremental-over-volume control

- **Volume control ≠ drift control.** Drift control removes time/regime trend; volume control removes "amount of news / coverage quality." Both are required (§13.1 steps 4 vs 5).
- **Locked control set:** `log1p_total_row_count` (direct volume); `roll_mean_log1p_total_w30` (local/regime baseline); `coverage_completeness` (coverage-quality, not pure volume).
- **Re-verification (V1):** all three names must be re-verified against the committed Step 2 table (`results/lane2_gdelt1_step2_daily_features/20260531T020244Z/step2_daily_features.csv`, schema as of `cb1122a`) at gate time.
- **Prohibitions:** no expansion to all 54 features; no post-hoc control selection.

---

## 15. Component collinearity reporting (R1 spec, LOCKED; output later, outcome-free)

- **Required outcome-free descriptive report** at the analysis gate: the **inter-component correlation matrix** among material-conflict (§7), negative structural-impact (§8), and negative-tone (§9) pressure.
- **Pearson + Spearman if feasible; at minimum Spearman** (rank-robust default).
- **Must not use any market outcome and must not use 2023+.**
- **Purpose:** determine whether the equal-weight composite is genuinely multidimensional or **effectively a single daily-negativity / conflict-share index.**
- **Interpretive rule:** if component collinearity is **high**, interpret the composite as a **single negativity-share index**; the three-component framing is then **scaffolding, not three independent signals.**
- **Status:** descriptive / interpretive only; **cannot rescue or overturn** the primary test (bound by §11 / v0.1 §13).

---

## 16. Degenerate cases & missing-value policy (F4, LOCKED)

- **Denominator-zero days → NaN / exclude** from primary component/composite.
- **Zero-event days → NaN / exclude** from primary component/composite.
- **Rows with missing/non-numeric `GoldsteinScale` or `AvgTone`** → contribute **0 to that component's numerator** but **remain in the common denominator** (§8/§9); never shrink the denominator.
- **All-cooperative / no-negative-pressure days with a valid denominator** → negative-pressure numerator = 0, **component = 0, not NaN** (a genuine "no negative pressure today," distinct from a missing day).
- **Reuse existing coverage / substrate-gap flags** (Step 2 lineage) rather than inventing a parallel gap system.
- **Missing-field mention fractions must be reported** (R2).
- **Small-but-nonzero denominator days** → governed by the §17 effective-sample floor.

---

## 17. Minimum-denominator / effective-sample floor (M1, LOCKED)

**LOCKED — minimum mention-effective-sample-size floor using the Kish effective event count based on `NumMentions` weights.**

- **Formula:** `N_eff_mentions = (Σ NumMentions)² / Σ(NumMentions²)` over the day's in-scope event universe.
- **Valid primary-composite day requires:** `N_eff_mentions ≥ 100`.
- **Rationale:**
  - the floor is chosen by **share-stability principle, not by data**;
  - simple event count alone is insufficient for mention-weighted shares because **one heavily covered event can dominate the denominator** even if many low-mention events exist;
  - minimum `NumMentions` alone is also insufficient because one heavily covered event can satisfy it;
  - the **Kish effective event count binds on mention concentration** and better matches the variance problem introduced by mention-weighted shares;
  - when mention weights are equal, `N_eff_mentions` **reduces to ordinary event count**, so the earlier `p(1−p)/N` intuition applies only in that equal-weight limiting case;
  - with concentrated mention weights, `N_eff_mentions` **falls, correctly flagging the failure case.**
- **Below-floor days:** **excluded** from the primary composite calculation; **reported** as below-effective-N days; **not tuned** after seeing composite behavior or market outcomes.
- The floor is chosen **without market outcomes and before extraction.** It is distinct from the warmup threshold (§12): warmup is *history length*; the floor is *same-day denominator adequacy*.

---

## 18. Gate consequences

- **All scientific / formula / method locks are now CLOSED** (S1, S2, F1–F4, M1, Z1, Z2, P1, P2, Y1, C1). **No scientific/formula/method degree of freedom remains open** before the extraction gate.
- **The §4A algebraic pre-check records PASS**, so lock closure proceeds; the **§4B empirical costume check gates the outcome join, not lock closure.**
- **The extraction gate still cannot open** until **(a)** a separate execution-authorization prompt exists (with a v0.1-§18 `STEP2_EXECUTION_AUTHORIZED`-style guard and v0.1-§19 conformance artifacts) **and (b)** the gate-time verifications **V1/V2 pass.**
- **Closure of these locks authorizes no data contact by itself.**

---

## 19. Non-authorizations

This memo explicitly does **NOT** authorize, and nothing in it permits:

- no GDELT contact;
- no raw event-file read;
- no extraction;
- no feature build;
- no 2023+ read;
- no market-data join;
- no outcome computation;
- no result generation;
- no implementation;
- no staging by the memo itself;
- no commit by the memo itself;
- no push by the memo itself.

---

## 20. Lock register

**All scientific / formula / method locks are CLOSED to single values. No such lock remains open before the extraction gate.** V1/V2 remain gate-time verifications; R1/R2 are required reporting specs (locked now, outputs produced later).

**Closed locks**
| # | Lock | Value (closed) | Section |
|---|---|---|---|
| S1 | Coverage denominator | total daily `NumMentions` over the single in-scope universe (whole field, not a subset) | §5, §6 |
| S2 | Interpretation | share-of-total negative pressure (subset-normalized = non-primary only) | §10 |
| F1 | Material-conflict pressure | mention-weighted `QuadClass=4` share over common denominator | §7 |
| F2 | Negative structural-impact | `Σ NumMentions·max(0,−GoldsteinScale) / Σ NumMentions`; missing Goldstein → 0 num, stays in denom | §8 |
| F3 | Negative-tone | `Σ NumMentions·max(0,−AvgTone) / Σ NumMentions`; missing tone → 0 num, stays in denom | §9 |
| F4 | Validity / degenerate policy | denom-0 & zero-event → NaN/exclude; missing-field → 0 num, denom intact; all-cooperative valid day → 0 not NaN; reuse gap flags; report missing-field fractions | §16 |
| M1 | Effective-sample floor | Kish `N_eff_mentions = (ΣNumMentions)²/Σ(NumMentions²) ≥ 100`; below-floor excluded | §17 |
| Z1 | Scaler / warmup | expanding past-only z; 365 prior valid days; sub-warmup NaN/exclude; OOS frozen-from-in-sample | §12 |
| Z2 | Drift / volume controls | fixed 6-step sequence; controls = `log1p_total_row_count`, `roll_mean_log1p_total_w30`, `coverage_completeness`; no expansion/post-hoc | §13.1, §14 |
| P1 | Planted-signal construction | synthetic target only; inject pre-standardization; full stack; daily/high-freq; seed `1729` | §13.3 |
| P2 | Planted-signal retention | grid `{0.05,0.10,0.20}`; PASS iff 0.05 retained same-sign ≥50%; 0.10/0.20 cannot rescue | §13.4 |
| Y1 | Per-year stability | per valid year (≥100 paired obs); PASS ≥70% sign-agree & not carried by 1–2 yrs; CAUTION 50–<70%; FAIL <50% or <5 valid yrs | §13.2 |
| C1 | Empirical costume thresholds | linear R²: PASS<0.25/CAUTION/ FAIL≥0.50; Spearman \|ρ\|: PASS<0.50/CAUTION/FAIL≥0.70; FAIL ⇒ new gate, no inline tuning | §4B |

**Gate-time verifications (NOT locks — must pass before extraction execution; do not fake-close now)**
| # | Verification | Section |
|---|---|---|
| V1 | Re-verify the three volume-control column names against the committed Step 2 table | §14 |
| V2 | Confirm GDELT 1.0 field positions / value ranges for `QuadClass`/`GoldsteinScale`/`AvgTone`/`NumMentions`/date | §5–§9 (v0.1 §5) |

V1/V2 are **gate-time schema / preflight verifications, not scientific degrees of freedom.** They must pass before extraction execution; if either fails, **stop and revise through a new design/gate path.**

**Required reporting specs (locked now; outputs produced later, outcome-free, no 2023+; descriptive — cannot rescue/overturn the primary test)**
| # | Reporting spec | Section |
|---|---|---|
| R1 | Component collinearity matrix (Pearson + Spearman if feasible, min. Spearman) | §15 |
| R2 | Missing-field / excluded-field mention-fraction & coverage-quality diagnostics | §6, §8, §9, §16 |

**Status of the four v0.1 §23 locks:** Lock 1 **CLOSED** (S1); Lock 2 **CLOSED** (F1 + F2/F3/F4/M1); Lock 3 **CLOSED** (Z1); Lock 4 **CLOSED** (Z2/P1/P2/Y1). **v0.2 is LOCK-CLOSED.**

**Next required step after review:** a **separate execution-authorization prompt** (its own guard + conformance artifacts) that, with V1/V2 passing, opens the extraction gate. Do not proceed to extraction, implementation, or execution on this memo.

---

*Filed as a lock-closed, design-only memo. It closes the type/tone/Goldstein extraction locks (denominator, formulas, effective-sample floor, scaler/warmup, drift/volume controls, planted-signal diagnostic, per-year stability, costume thresholds), records the algebraic pre-check PASS, defers the empirical costume check to the outcome-join gate, and keeps V1/V2 as gate-time verifications and R1/R2 as reporting specs. It authorizes no data contact. The 2023+ seal remains intact.*
