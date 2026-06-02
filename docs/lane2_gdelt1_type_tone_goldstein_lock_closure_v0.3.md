# Lane 2 — Type / Tone / Goldstein Lock-Closure v0.3 Amendment (DRAFT FOR REVIEW, rev 7)

## 1. Status and purpose

- **DRAFT FOR REVIEW. DESIGN-ONLY.**
- **DOES NOT AUTHORIZE EXTRACTION / GDELT CONTACT / MARKET JOIN / OUTCOME ACCESS / 2023+ / V1·V2 / EXECUTION.**
- Additive amendment to `294494a` (v0.2 remains baseline); changes only where labeled `CLARIFIES`/`AMENDS`. **"Locked"** = quotable to implementation exactness without inference.

**Purpose:** repair the Phase 0.5 canary BLOCK from prompt `3411db5`. **rev 7** applies two non-blocking micro-polishes on top of rev 6: a **sidedness caveat** on the §12 approximate confidence-bound diagnostic (two-sided §10 MDE floor vs one-sided directional-fragility CB), and an explicit **no-leave-two-sign-flip** condition in the Clean PASS terminal state (making hard-FAIL precedence explicit). **rev 6** applied ratified **Option B-with-teeth** to the §12 influence gate: deletion-subset floors recomputed **per subset** (LOYO and per-pair) with **seam-safe φ**; LOYO binds on sign + its own floor; leave-two binds on sign only, with a same-sign-below-own-pair-floor crossing as a **load-bearing routed warning** (blocks positive interpretation; mandates a future trailing-realized-volatility-control join-gate precondition); an approximate Fisher-z one-sided lower-confidence-bound **diagnostic** (not binding); and explicit **clean PASS / routed-warning / hard FAIL** terminal states. 50% magnitude retention stays diagnostic-only; the §11 planted-signal fidelity ratio stays distinct. (rev 5 demoted 50% magnitude retention to diagnostic and made the influence binding rule sign + realized MDE floor; rev 4 ratified alpha/power/φ, made the MDE floor a deterministic rule output, separated `φ_synth` from injected-signal character, and added exhaustive one-/two-year pairwise deletion. rev 6 also absorbed the prior stale footer "rev 4" → rev 6 lineage correction.)

---

## 2. Anchors

| Anchor | Commit |
|---|---|
| v0.1 design memo | `0295406` |
| v0.2 governing spec (baseline) | `294494a` |
| extraction gate memo | `ea891e0` |
| durable execution prompt v2.1 | `3411db5` |
| dry-run result | `BLOCKED — planted-signal diagnostic under-specified in governing spec` |

---

## 3. The BLOCK finding (preserved as fact)

v0.2 item 11 could not be quoted to implementation exactness (injection point ambiguous; ordered sequence inconsistent; retention metric/denominator undefined); in-scope (§6) and date (v0.1 §10) were by-reference only. Everything from §4 onward is this memo's analysis.

---

## 4. In-scope row/source definition — tied to the volume/coverage-control universe

**Committed-code trace (no data read):** count-build runner Decision **C** "Raw event rows, no dedup, **no filters**, no weights," docstring "filtering by category/theme/actor/geography/tone … **forbidden here**," Decision **D** "Aggregate by **SQLDATE** only," Decision **E** out-of-window + sentinel exclusion; Step 2 derives `total_row_count`/`log1p_total_row_count`/`coverage_completeness`/`roll_mean_log1p_total_w30` from `build_daily_counts.csv`.

**LOCK v0.3-IS:** feature universe **row-identical to the count-build universe** (all GDELT 1.0 Event rows, no filter, SQLDATE-attributed, same exclusions, 2013–2022, 2023+ hard-fail). Controls weight by **row counts**; the new extraction weights the **identical rows** by **`NumMentions`**. Universe drift ⇒ **BLOCKED**.

**Interpretation guard (LOCKED):** a null means *"global daily negativity/intensity pressure did not pass the locked association test,"* not *"news does not matter,"* not *"all news filters were tested."*

**Class:** all-global = **`AMENDS`**; universe-identity = **`CLARIFIES`**.

---

## 5. Date / information-date logic — traced to committed code

`SQLDATE_COLUMN_INDEX = 1` (memo §9 / `e55e09a`); Decision D aggregates by SQLDATE → per-`civil_date` `build_daily_counts.csv`. **Date key = `civil_date` = SQLDATE-aggregated date used by Step 2.** 2013–2022 only; 2023+ hard-fail.

**Characterization correction (overrides v0.1 §10 wording):** `civil_date` = SQLDATE = GDELT **event/record date**; availability lags ≤ +1 day (`rows_from_offset_plus_1`), handled by the join memo's `civil_date+1` no-lookahead anchor. Predictor-only extraction has no lookahead.

**Class:** field citation = **`CLARIFIES`**; rewording = **`AMENDS`**. **Date RESOLVED.**

---

## 6. Planted-signal diagnostic purpose fork

**Intent A (recommended):** retention certifies a known synthetic signal survives raw-component → standardization → compositing → simultaneous date/volume control (§7/§9/§11). Single-year dominance is tested by **exhaustive one-year + two-year pairwise deletion (§12)**, not per-year same-sign. The floor is the **MDE rule output (§10)** under binding `φ_synth = 0.50`. Intent B not recommended.

---

## 7. Primary controlled-association statistic — LOCKED (LOCK v0.3-STAT)

Full-rank **simultaneous Spearman partial correlation**:
- **Association type:** Spearman partial.
- **Control mechanism:** simultaneous partial (predictor and outcome adjusted for the same covariates symmetrically; no separate outcome residualization outside the statistic).
- **Outcome treatment:** `abs(next_session_return)` is the outcome variable **inside** the statistic; not pre-residualized outside it.
- **Covariates (all rank-transformed):** ordinal/rank date; ranked `log1p_total_row_count`; ranked `roll_mean_log1p_total_w30`; ranked `coverage_completeness`.

**Implementation-exact convention:** (1) rank-transform predictor/composite, outcome, and **all three** controls, **average ranks for ties**; (2) **date = rank of `civil_date` ascending** over the association sample; (3) statistic = **Pearson correlation of residuals** from two symmetric OLS regressions [ranked predictor ~ rank-date + 3 ranked controls] and [ranked outcome ~ rank-date + 3 ranked controls]; (4) **identical rows**, **missing → exclude**; (5) **no additional outcome residualization** outside the statistic.

**Rationale:** rank-based for heavy tails; full-rank control prevents monotone-nonlinear volume leakage; no splines (avoids df/forking); simultaneous over sequential (rank "residualize then re-rank" is ambiguous). **Class: `AMENDS`** (statistic + full-rank controls).

---

## 8. Injection point and surrogate target (LOCK v0.3-INJ)

- **Single injection point:** raw F1/F2/F3 components, before expanding-z. "Pre-standardization composite" removed.
- **Surrogate target `y_synth` (the outcome stand-in):** an **AR(1)-style series with persistence `φ_synth`** (binding `φ_synth = 0.50`, §10), deterministic seed **`1729`**. Its persistence exists **only to power-match / stress the effective-N environment** of the diagnostic.
- **Injected signal (separate object):** a **daily / high-frequency lead-lag** additive term placed into each raw component (equal standardized-dispersion share) so the daily composite tracks `y_synth` at the targeted floor strength. The **injected signal remains daily/high-frequency** — it is **not** trend-shaped or regime-shaped. Gain calibrated so the realized **pre-stack plain Spearman** of composite vs `y_synth` equals the targeted MDE floor (§10/§11). Calibration uses `y_synth` only.

**Separation (LOCKED):** *"The surrogate target may carry AR(1)-style persistence (`φ_synth`) for power-matching, but the planted relation injected into the raw component remains a daily/high-frequency lead-lag signal. The φ grid varies surrogate-target persistence, not the temporal character of the injected signal."* Target persistence and injected-signal character are **separate design objects**.

- Valid days = post-warmup, `N_eff_mentions ≥ 100`, valid `y_synth`; invalids excluded.

**Class:** raw-component injection = **`CLARIFIES`**; remove pre-std composite = **`AMENDS`**; φ_synth = surrogate-target (not injected-signal) autocorrelation, injected signal stays high-frequency = **`CLARIFIES`**.

---

## 9. Ordered transformation sequence (LOCK v0.3-SEQ)

1. construct raw F1/F2/F3; 2. **inject** calibrated daily signal (∝ alignment with `y_synth`) into each raw component; 3. expanding past-only z per component, 365-day warmup; 4. **composite construction** → `intensity_valence_pressure`; 5. **[DENOMINATOR]** plain Spearman of composite vs `y_synth`, **no covariates** (§11); 6. **[NUMERATOR]** **full-rank simultaneous Spearman partial** of composite vs `y_synth`, controls simultaneous (rank-date + 3 ranked controls), per §7 (§11).

**Reconciliation:** the v0.2 separate "drift/time control" then "volume control" are operationalized as **one simultaneous partial statistic**, not two sequential stages. Per-year is not in the stack. **Class:** compositing step = **`CLARIFIES`**; sequential→simultaneous collapse = **`AMENDS`**.

---

## 10. Detectable-effect (MDE) floor + ratified conventions (LOCK v0.3-FLOOR)

**Ratified conventions (LOCKED):**
- **alpha = 0.05, two-sided.**
- **target power = 0.80.**
- **effective-N method = AR(1)-style deflation `N_eff ≈ N·(1−φ)/(1+φ)`.**
- **φ reporting grid = {0.0, 0.1, 0.25, 0.5}.**
- MDE via Fisher-z: `atanh(ρ_MDE) = (z_{1−α/2}+z_{1−β})/√(N_eff−k−3)`, k=4 (rank-partial approximation; simulation may replace if exactness needed).

**The binding floor is the deterministic OUTPUT of the locked MDE rule given the applicable effective-N inputs.** Planning values **0.054, 0.060, 0.070, 0.093** (pooled, N_nom≈2700, φ=0/0.1/0.25/0.5) are **examples from φ sensitivity, not fixed locked floors.**

**Binding planted-signal case: `φ_synth = 0.50`** ⇒ binding planted floor = the MDE-rule output at the diagnostic's effective-N under `φ_synth=0.50` (planning example ≈ **0.093** pooled). Lower-φ cases are **reported as sensitivity / planning context only**; **passing lower-φ cannot rescue failure at the binding `φ_synth=0.50` floor.** Rationale: `φ_synth=0.50` is conservative — it avoids certifying fidelity only under an easy low-autocorrelation surrogate. It does **not** claim the real outcome has φ=0.50.

**Interpretive real-outcome floor (later):** computed from the locked MDE rule using the **realized paired/outcome context after authorized outcome join**. A real null is interpreted **only relative to that realized interpretive MDE floor**; effects below it are **below-resolution, not strong evidence of absence**.

**Floor scope for §12 deletions (LOCKED).** The **full-sample** realized interpretive MDE floor governs only the **full-sample** interpretation at the separately authorized outcome join. For the §12 influence-gate deletions, the floor is **recomputed per deletion subset**: each LOYO subset uses **its own** realized `N_eff` and `φ`; each leave-two pair-deleted subset uses **its own** pair-specific realized `N_eff` and `φ`. These §12 floors are **at-join, outcome-dependent interpretive floors** and **must not be confused with the §11 pre-join, outcome-free planted-signal floor / fidelity ratio**.

**Deletion-subset φ seam pin (LOCKED).** For deletion-subset floor computations, realized `φ` is estimated from lag-1 autocorrelation using **only within-contiguous-retained-block lag pairs**; lag pairs spanning a deleted calendar year / deletion seam are **excluded**, so the last retained observation before a deleted year is **not** paired with the first retained observation after that deleted year as if adjacent.

**Legacy 0.05:** **reference-only / superseded** unless the MDE-rule output is ≤ 0.05; reported for continuity; cannot be the binding floor when underpowered; cannot rescue the binding floor.

**Class: `AMENDS`** (ratified alpha/power; floor as deterministic rule output; binding `φ_synth=0.50`; 0.05 superseded).

---

## 11. Retention metric and denominator — explicit asymmetry (LOCK v0.3-RET)

The retention ratio is **a post-control partial association divided by a pre-control plain association** — not the same statistic twice.

- **Denominator** (SEQ stage 5): **plain Spearman rank correlation** of the injected composite vs `y_synth`, **no covariates** — *not* "partial with zero covariates"; average-rank ties; same valid-date sample as numerator where possible.
- **Numerator** (SEQ stage 6): the **full-rank simultaneous Spearman partial** of §7 with **`y_synth` substituted for the outcome**; controls simultaneous (rank-date + 3 ranked controls).
- **Retention = numerator / denominator, sign-preserving.** **PASS** iff same sign AND **|retention| ≥ 0.50** at the binding MDE floor (§10). **Degenerate / near-zero denominator ⇒ BLOCKED** (not FAIL). Report-only grid (legacy 0.05, 0.10, 0.20, lower-φ) **cannot rescue** the floor point.

**Interpretive rationale (LOCKED):** the synthetic surrogate is constructed to be independent of real date/volume structure, so date/volume controls should not materially attenuate a clean high-frequency injected signal; low retention indicates the predictor/control stack is destroying daily signal rather than legitimately absorbing a date/volume channel.

**Class: `CLARIFIES`** (asymmetry, plain-Spearman denominator, full-rank-partial numerator — inheriting §7).

---

## 12. Influence gate: exhaustive one-year + two-year pairwise deletion (LOCK v0.3-INFL)

**Replaces the v0.2 per-year same-sign blocking mechanism and any "top-two individually influential years" shortcut.** Purpose preserved: test directly whether the pooled association is **carried by one or two years**.

- **Per-year same-sign counts: DESCRIPTIVE only, NOT blocking** (sharding into noisy yearly chunks discards magnitude and has low power; a sign count does not test single/pair dominance).

**"Pooled primary statistic" (clarifier).** Throughout §12, "pooled" means the **single-sample full-rank simultaneous Spearman partial (§7) recomputed on the retained rows**; it is **not** per-year averaging and does **not** revive the demoted Y1 per-year mechanism.

**One-year deletion (exhaustive) — binding rule:** for **each** valid calendar year, drop it and recompute the pooled primary statistic on the retained rows (§7 convention). **PASS** requires **every** LOYO estimate to (i) keep the **full-sample sign** AND (ii) remain above **that LOYO subset's own recomputed realized interpretive MDE floor** — recomputed on the LOYO subset's own realized `N_eff` and **seam-safe `φ`** (§10). **FAIL** if any LOYO **flips sign** or **falls below its own LOYO floor**. For any near-floor / flagged LOYO subset, report: the LOYO estimate, the LOYO floor, the magnitude-retention diagnostic, and the **approximate one-sided lower confidence-bound diagnostic relative to that LOYO floor** (method below).

**Two-year deletion (exhaustive pairwise) — binding rule:** for **every pair** of valid calendar years, drop **both jointly** and recompute the pooled primary statistic on the retained rows (§7 convention); evaluate **all pairs** (~36 for 9 years — cheap, so **no shortcut**; the top-two-individually-influential shortcut is **prohibited**). **A sign flip in any pair FAILs** the influence gate. A pair-deleted estimate that **keeps the full-sample sign** but **falls below its own pair-specific recomputed realized interpretive MDE floor** (recomputed on the pair-deleted subset's own realized `N_eff` and **seam-safe `φ`**, §10) does **NOT** automatically FAIL; it is a **severe load-bearing routed warning** that **(i)** blocks interpreting the full-sample result as a positive finding, **(ii)** routes to the future join-gate design as a **mandatory precondition**, and **(iii)** requires the future join-gate spec to **pre-register a trailing realized-volatility control and re-examine the flagged pair(s) with that control** before any positive interpretation. Report, per flagged pair: the pair-specific estimate, the pair-specific floor, the magnitude-retention diagnostic, and the **approximate one-sided lower confidence-bound diagnostic relative to that pair floor** (method below).

**Approximate confidence-bound diagnostic (method, diagnostic-only — NOT binding).** For flagged / near-floor subsets, report a one-sided lower confidence-bound diagnostic relative to that subset's **own** floor. Let `s = sign(full-sample estimate)` and `r_dir = s × r_subset`, so same-sign retained estimates are positive on the directional scale. Use a **Fisher-z analytic approximation** with the **same subset `N_eff`** used for that subset's MDE floor and **four controlled variables** (rank date + three ranked volume/coverage controls): `SE_z = 1 / sqrt(N_eff − 7)`, one-sided `α = 0.05`, and `LCB_dir = tanh( atanh(r_dir) − z_(1−α) × SE_z )`. Report `LCB_dir`, the subset floor, and `LCB_dir − floor`. **This diagnostic is approximate** because the primary statistic is a **Pearson partial on rank-residuals, not a simple bivariate-normal Pearson r** (Fisher-z is exact only for bivariate-normal Pearson correlation); autocorrelation is handled through `N_eff`, while the rank-residual approximation remains analytic. **It is diagnostic only; `LCB_dir` clearing the floor is NOT a v0.3 binding criterion.** If `N_eff ≤ 7` or the statistic is degenerate / not computable to exactness, report the confidence-bound diagnostic as **BLOCKED / non-computable** and disclose it; this non-computability does **not** by itself change the binding gate result. **Sidedness convention:** the §10 MDE floor remains a **two-sided detectability floor**, while this lower-confidence-bound diagnostic is **one-sided** because it measures directional fragility of a same-sign retained estimate; this diagnostic is **not** a binding floor test. If a future design proposes promoting confidence-bound clearance toward a binding criterion, the sidedness convention **must be re-ratified** in the join-gate / bootstrap design. **Upgrade path:** if a future design proposes promoting this diagnostic toward a binding criterion, the upgrade is a **block bootstrap that respects both the rank structure and the autocorrelation** (not the analytic Fisher-z form).

**Magnitude retention is a DIAGNOSTIC, not a binding threshold.** *"Magnitude retention is reported to expose concentration risk, but it is not a separate blocking threshold. The blocking influence rule is sign stability plus remaining above the (subset-own) realized interpretive MDE floor."* Report descriptively: **max one-year magnitude retention**, **worst-pair two-year magnitude retention**, and **max one-year / max pairwise LOYO deviation**. A retained magnitude **below 50%** raises a **labeled concentration warning only** — it does **not** by itself FAIL the gate and does **not** rescue a FAIL. **The leave-two pair-floor crossing is stronger than the ordinary 50% diagnostic:** still not an automatic FAIL, but it **blocks positive interpretation**, **forces the future join-gate trailing-RV-control precondition**, and **must be carried into any later join-gate memo / interpretation**.

**Terminal states (LOCKED — exactly three).**
- **Clean PASS:** **no LOYO sign flip, no LOYO floor breach, no leave-two sign flip, and no leave-two pair-floor crossing** (the no-sign-flip conditions make hard-FAIL precedence explicit). Positive full-sample interpretation is permitted **by this influence gate**, still pending all separate join authorization / interpretation constraints.
- **Routed-warning:** no hard FAIL, but **at least one same-sign leave-two pair falls below its own pair-specific floor**. Positive full-sample interpretation is **not permitted**; the future join-gate spec **must pre-register trailing realized-volatility control and re-examine the flagged pair(s)** before any positive interpretation. *Routed-warning is **not** a hard FAIL and is **not** a clean PASS.*
- **Hard FAIL:** any LOYO sign flip, any LOYO below its own LOYO floor, **or** any leave-two sign flip. Outcome interpretation is **blocked pending design review**.

The **50% magnitude diagnostic** cannot create or rescue a FAIL; the **confidence-bound diagnostic** cannot create or rescue a FAIL. **BLOCKED** = the exhaustive deletion test cannot be computed to exactness ⇒ outcome interpretation blocked pending design review.

**Gate location (LOCKED).** §12 is an **at-join future-rule specification**: both the predictor↔outcome partial and the realized interpretive floor are **outcome-dependent**. §12 **does not authorize** outcome join, market-data access, running the influence gate, or extraction. It writes the future join-gate rulebook only.

**Power note:** each deletion retains ~7–8 of 9 years (large `N_eff`), so the gate tests influence/robustness, well-powered; weak-signal detection is governed by the per-subset §10 floor.

**Class: `AMENDS`** (per-year demoted to descriptive; exhaustive one-year + two-year pairwise deletion; **LOYO binds on sign + own subset floor; leave-two binds on sign, with same-sign-below-own-pair-floor a routed warning**; seam-safe per-subset φ; approximate confidence-bound diagnostic; explicit terminal states; 50% magnitude retention diagnostic-only). Replacing the top-two shortcut with exhaustive pairwise = **`CLARIFIES`** of the "not carried by 1–2 years" intent.

---

## 13. Gate consequences (consolidated)

- **Retention (§11):** PASS = same-sign & |retention| ≥ 0.50 at the binding MDE floor; FAIL ⇒ blocks outcome join; degenerate denominator ⇒ BLOCKED. No CAUTION; report-only grid cannot rescue. No tuning/patch-rerun.
- **MDE floor (§10):** deterministic rule output; binding `φ_synth=0.50`.
- **Influence gate (§12, at-join future rule — three terminal states):**
  - **Hard FAIL** = any LOYO **sign flip**, any LOYO **below its own LOYO floor**, or any **leave-two sign flip** ⇒ outcome interpretation **blocked pending design review**.
  - **Routed-warning** = a **same-sign leave-two pair below its own pair-specific floor**: **not** an automatic FAIL, **not** a clean PASS; **no positive full-sample interpretation**; the future join-gate spec **must pre-register trailing-RV control and re-examine the flagged pair(s)**.
  - **Clean PASS** = no LOYO sign flip, no LOYO floor breach, no leave-two sign flip, no pair-floor crossing.
  - **BLOCKED** = deletion test not computable to exactness ⇒ blocked pending design review. Floors are **per-subset** (LOYO / per-pair), recomputed on subset `N_eff` + seam-safe `φ`. Outcome-dependent; specified here, **run only under separate future authorization**.
- **50% magnitude-retention diagnostic (§12):** concentration transparency only; **cannot create a FAIL** and **cannot rescue a FAIL**; `< 50%` raises a labeled concentration warning.
- **Confidence-bound diagnostic (§12):** approximate Fisher-z, diagnostic-only; **cannot create or rescue a FAIL**.
- **Per-year same-sign:** descriptive only; never blocks.

---

## 14. Prompt compatibility — does v0.3 let `3411db5` pass Phase 0.5 item 11?

| Question | v0.3 answer |
|---|---|
| Pre-standardization composite ambiguity removed? | Yes (§8). |
| Ordered synthetic sequence defined? | Yes — 6 steps, single simultaneous partial (§9). |
| Retention metric/denominator (asymmetry) defined? | Yes (§11). |
| Covariate set defined? | Yes — rank-date + 3 ranked controls (§7/§11). |
| Primary statistic implementation-exact? | Yes — full-rank simultaneous Spearman partial (§7). |
| Per-year/Y1 adjudicated? | Yes — descriptive; replaced by exhaustive 1-yr + 2-yr deletion (§12). |
| Floor adjudicated? | Yes — MDE rule output, alpha/power/φ ratified, binding `φ_synth=0.50` (§10). |
| `φ_synth` vs injected-signal character separated? | Yes (§8/§10). |
| In-scope + universe identity? | Yes (§4). Date? Yes (§5). |
| Item-11 repairs labeled CLARIFIES/AMENDS? | Yes (§16). |

**Net:** all item-11 mechanics, the primary statistic, the floor convention, the influence gate, in-scope, and date are closed to implementation exactness. The only remaining pre-execution item is the v2.1 checklist amendment (§15), which is a prompt change, not a v0.3 spec gap.

---

## 15. Deferred v2.1 prompt amendment note

v2.1 (`3411db5`) Phase 0.5 does not require extracting/locking the **primary controlled-association statistic / control mechanism / outcome treatment** (nor the §12 influence gate / §10 MDE floor). v0.3 locks them; **v2.1 Phase 0.5 must later be amended** to require their explicit conformance extraction. Prompt/checklist amendment, **not** a v0.3 spec change; **v2.1 NOT modified here**; open a separate small design-only prompt-amendment turn before any execution. **This does not block v0.3 review-readiness** (§17).

---

## 16. Clarify-vs-amend table

| Item | Class | Rationale |
|---|---|---|
| Full-rank simultaneous Spearman partial primary statistic | **AMENDS** | v0.2 did not operationalize the statistic |
| Rank-transform volume/coverage controls | **AMENDS** | closes monotone-nonlinear volume leakage |
| Retention numerator/denominator asymmetry; plain-Spearman denominator; full-rank-partial numerator | **CLARIFIES** | resolves §13.4 ambiguity, inherits §7 |
| Raw-component injection / remove pre-std composite | **CLARIFIES** / **AMENDS** | select branch / remove impossible object |
| Sequential control stages → one simultaneous partial | **AMENDS** | overrides §13.1/§13.3 sequencing |
| Per-year same-sign demoted to descriptive | **AMENDS** | v0.2 treated Y1 as blocking |
| Exhaustive one-year deletion gate | **AMENDS** | new blocking robustness gate |
| Exhaustive two-year pairwise deletion gate | **AMENDS** | new blocking robustness gate |
| Replace top-two-individual shortcut with exhaustive pairwise | **CLARIFIES** | tests "not carried by 1–2 years" directly, no weaker proxy |
| `φ_synth` = surrogate-target autocorrelation, not injected-signal autocorrelation | **CLARIFIES** | separates two design objects |
| Injected signal remains daily/high-frequency | **CLARIFIES** | preserves diagnostic character |
| Binding `φ_synth = 0.50` | **AMENDS** | conservative effective-N case |
| alpha = 0.05 two-sided, power = 0.80 (newly locked) | **AMENDS** | not locked by v0.2 |
| LOYO binds on sign + own subset floor; 50% magnitude retention diagnostic-only | **AMENDS** | ties influence to detectability, not an arbitrary magnitude fraction; concentration risk preserved via reported retention ratios + warnings |
| Influence-deletion floor = subset-specific recomputed realized interpretive MDE floor (per-LOYO; per-pair for leave-two) | **AMENDS** | detectability updates after information removal; avoids reusing the full-sample floor on reduced-information subsets; keeps LOYO the clean single-year concentration catch |
| Deletion-subset φ estimation excludes deletion seams | **CLARIFIES** | prevents inferred lag-1 autocorrelation across deleted-year seams; does not pair non-adjacent retained blocks as if adjacent |
| Leave-two pair-floor crossing = routed-warning terminal state / join-gate routing precondition, not auto-FAIL and not clean PASS | **AMENDS** | avoids Option-A hostage-to-noisiest-pair behavior while preventing crisis-pair artifacts from being over-claimed; routes flagged pair(s) to the future trailing-RV-control join-gate design where the real confound belongs |
| Approximate confidence-bound fragility diagnostic (Fisher-z at subset `N_eff − 7`, one-sided α=0.05) | **AMENDS** | reproducible approximate analytic fragility/resolvability diagnostic relative to each subset's own floor, without adopting confidence-bound clearance as a binding v0.3 gate; block bootstrap respecting rank structure + autocorrelation is the upgrade path if ever promoted toward binding |
| §12 terminal states = clean PASS / routed-warning / hard FAIL | **CLARIFIES** | removes downstream ambiguity about what a warning permits; routed-warning blocks positive interpretation and routes to join-gate RV-control design, hard FAIL blocks outcome interpretation pending design review |
| MDE floor as deterministic rule output (no fixed number) | **AMENDS** | replaces asserted floor |
| Legacy 0.05 reference-only / superseded | **AMENDS** | below pooled MDE for φ>0 |
| In-scope all-global / universe identity | **AMENDS** / **CLARIFIES** | gap-fill / confirmed from committed code |
| Date field citation / characterization correction | **CLARIFIES** / **AMENDS** | pin to committed source / correct v0.1 §10 |
| Deferred v2.1 checklist amendment | N/A (prompt note) | not a v0.2 spec change |

---

## 17. Commit-readiness status

**`REVIEW-READY — v0.3 draft clean after artifact review and final influence-gate revision, pending user approval`** (not committed, not executed).

All substantive v0.3 spec blockers are resolved: primary statistic implementation-exact (§7); retention asymmetry explicit (§11); **§12 Option B-with-teeth** — exhaustive LOYO + leave-two pairwise; LOYO binds on sign + its **own per-subset** recomputed realized interpretive MDE floor; leave-two binds on sign, with a same-sign-below-own-pair-floor crossing a **routed warning** (blocks positive interpretation; mandatory future trailing-RV-control join-gate precondition); **seam-safe per-subset φ**; approximate Fisher-z confidence-bound **diagnostic** (not binding); explicit **clean PASS / routed-warning / hard FAIL** terminal states; 50% magnitude retention diagnostic-only; MDE floor = deterministic rule output with **alpha=0.05 / power=0.80 / φ grid ratified** and binding `φ_synth=0.50` (§10); `φ_synth`/injected-signal separation (§8); date (§5) and in-scope/universe identity (§4) resolved. §12 is an **at-join future-rule specification** and authorizes no outcome join / market-data access / gate run / extraction.

**Distinction (LOCKED):**
- **v0.3 spec status:** **REVIEW-READY** — no known implementation-lock blockers; pending user approval of the ratified conventions and the binding `φ_synth=0.50` case.
- **Pre-execution v2.1 checklist status:** a **separate** v2.1 Phase 0.5 amendment (§15) is still required **before any execution turn** — this is a prompt-checklist task, **not** a v0.3 spec blocker, and does **not** prevent v0.3 review-readiness or commit.

---

## 18. Non-authorization statement

Does **not** authorize execution, GDELT contact, V1/V2, extraction code, synthetic tests, market-data/outcome access, or 2023+.

**Future sequence:** (1) approve the v0.3 conventions/thresholds; (2) commit/push v0.3; (3) **separately amend the v2.1 Phase 0.5 checklist (§15)**; (4) rerun the response-only Phase 0.5 dry run; (5) only if CLEANLY LOCKED, consider a separate execution authorization.

---

*Filed as a design-only v0.3 amendment DRAFT (rev 7). Additive to `294494a`. Locks: full-rank simultaneous Spearman partial primary statistic; asymmetric (post-control-partial / pre-control-plain) retention; **§12 Option B-with-teeth at-join influence gate** — exhaustive LOYO + leave-two pairwise with **per-subset recomputed realized interpretive MDE floors** (seam-safe φ), LOYO binding on sign + own floor, leave-two binding on sign with a same-sign-below-own-pair-floor **routed warning** (blocks positive interpretation; mandatory future trailing-RV-control join-gate precondition), an approximate Fisher-z confidence-bound diagnostic (not binding; block-bootstrap upgrade path named), explicit **clean PASS / routed-warning / hard FAIL** terminal states, and 50% magnitude retention diagnostic-only; an MDE floor as the deterministic output of a ratified alpha=0.05 / power=0.80 / AR(1)-φ rule with binding `φ_synth=0.50` (legacy 0.05 superseded); and a clean separation of surrogate-target persistence from injected-signal character. The §11 pre-join planted-signal fidelity ratio (`|retention| ≥ 0.50`) remains distinct from the §12 at-join interpretive floors. REVIEW-READY pending user approval; the v2.1 checklist amendment remains a separate pre-execution task. Authorizes no data contact; 2023+ seal intact.*
