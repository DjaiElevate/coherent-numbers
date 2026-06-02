# Lane 2 — v2.1 Phase 0.5 Conformance-Checklist Amendment (DRAFT v0.1, DESIGN-ONLY)

## A. Status / non-authorization

- **Design-only prompt-amendment DRAFT.** It amends the durable v2.1 execution prompt's **Phase 0.5 governing-spec conformance** stage. It changes no logic outside Phase 0.5's source-of-truth and checklist.
- **NOT committed. NOT executed.**
- This draft **does not authorize**, and nothing in it permits:
  - running Phase 0;
  - running Phase 0.5;
  - running the response-only conformance canary (not yet — see §I sequence);
  - GDELT contact;
  - source-file enumeration/read;
  - extraction;
  - extraction code;
  - synthetic tests;
  - guard flips;
  - V1/V2;
  - market data;
  - outcomes;
  - `next_session_return` / `abs(next_session_return)`;
  - 2023+ read.

This is a documentation/prompt-amendment draft only. It is reviewed, then (if approved) committed/pushed in a **separate** durability turn, after which a fresh contact-free response-only Phase 0.5 canary may be run against the amended prompt + manifest.

---

## B. Anchor manifest

| Role | Commit | Status |
|---|---|---|
| v0.2 baseline governing spec | `294494a` | baseline |
| extraction-authorization gate | `ea891e0` | unchanged |
| durable v2.1 prompt being amended | `3411db5` | amended by this document |
| v0.3 additive lock-closure amendment | `c6aeb2b84279e3d8955b94ae31778f95e3d1fa14` | additive governing amendment |
| this v2.1 amendment | `TBD after commit` | future durable amendment |

**Resolved file paths:**
- v2.1 prompt being amended: `docs/lane2_gdelt1_type_tone_goldstein_extraction_execution_prompt_v2.1.md` (committed at `3411db5`).
- v0.3 lock-closure amendment: `docs/lane2_gdelt1_type_tone_goldstein_lock_closure_v0.3.md` (committed at `c6aeb2b`, rev 7, 256 lines).

---

## C. Amendment part (a) — add the missing primary-statistic / control-mechanism / outcome-treatment checklist item

Insert into v2.1 **Phase 0.5** a new **required** conformance item:

**[Phase 0.5 — NEW ITEM] Primary controlled-association statistic locked to implementation exactness.** Phase 0.5 must extract and confirm, against the v0.3 amendment (`c6aeb2b`), that the primary controlled-association statistic is:
- **full-rank simultaneous Spearman partial correlation**;
- **rank-transform** predictor/composite, outcome, **and all three** volume/coverage controls (`log1p_total_row_count`, `roll_mean_log1p_total_w30`, `coverage_completeness`);
- **date enters as rank of `civil_date`** (ascending over the association sample);
- **average ranks for ties**;
- statistic = **Pearson correlation of residuals** from **two symmetric OLS regressions**:
  - ranked predictor/composite ~ rank-date + three ranked controls;
  - ranked outcome ~ rank-date + three ranked controls;
- **identical rows** used for both regressions;
- **missing values excluded**;
- **no separate outcome residualization** outside the statistic;
- **no hybrid numeric-control** approach (controls are fully ranked, not numeric-linear);
- **no sequential residualization**;
- **no per-year averaging / no revival of the demoted Y1 mechanism.**

**Outcome treatment (must be explicit in the item):**
- For the **real join-time outcome**, the outcome (`abs(next_session_return)`) is **ranked and included inside the same simultaneous partial statistic** (not pre-residualized outside it).
- For the **planted-signal / synthetic conformance path**, `y_synth` substitutes for the outcome **only where v0.3 says so** (the §11 fidelity diagnostic / §9 numerator).
- Phase 0.5 must **distinguish the real-outcome statistic definition from the synthetic planted-signal fidelity diagnostic** — they share the statistic form but differ in the substituted target and in pre-join vs at-join status.

---

## D. Amendment part (a2) — lock `y_synth` construction for planted-signal conformance

Insert into v2.1 **Phase 0.5** a new **required** conformance item:

**[Phase 0.5 — NEW ITEM] Planted-signal surrogate `y_synth` locked to implementation exactness.** Phase 0.5 must extract and confirm, against v0.3 (`c6aeb2b`):
- `y_synth` is an **AR(1)-style synthetic surrogate target / outcome stand-in with persistence `φ_synth`** (binding `φ_synth = 0.50`; the persistence exists only to power-match / stress the effective-N environment — per v0.3 §8/§10). `y_synth` is **not** a zero-autocorrelation / φ=0 surrogate;
- the **no-autocorrelation, daily / high-frequency lead-lag** character belongs to the **injected signal (a separate object)**, **not** to `y_synth`; the injected signal is **not** trend-shaped or regime-shaped;
- **seed = `1729`** (deterministic);
- **gain calibrated to the realized pre-stack association** (calibration uses `y_synth` only, never an outcome);
- the synthetic surrogate substitutes for the outcome **only** in the planted-signal / fidelity-diagnostic path;
- **do not** use trend-shaped, regime-shaped, or outcome-derived surrogate structure;
- **do not confuse `φ_synth` with the injected signal's character**:
  - `φ_synth` is **surrogate-target persistence / effective-N planning** for the planted-signal MDE floor;
  - the **injected signal remains daily / high-frequency** lead-lag;
- **binding planted-signal case remains `φ_synth = 0.50`** (conservative; lower-φ reported but cannot rescue).

**Failure to lock `y_synth` construction ⇒ `BLOCKED`**, because the §11 retention numerator/denominator (and the §12 floor calibration) **cannot be reproduced to exactness** without the exact surrogate construction.

---

## E. Amendment part (b) — governing-spec repoint (MANDATORY, load-bearing)

**Phase 0.5's governing source of truth is repointed** from `294494a` alone to the **amended governing-spec chain**:
- `294494a` = v0.2 baseline;
- `c6aeb2b84279e3d8955b94ae31778f95e3d1fa14` = additive v0.3 amendment.

**Phase 0.5 must NOT read `294494a` alone.** Any canary / conformance run that extracts requirements only from `294494a` must be treated as **invalid / `STALE-SOURCE BLOCKED`**, not as a scientific or design BLOCK. (Without this repoint, a re-canary reads the old `294494a` item 11, which is under-specified, and correctly BLOCKs again — a stale-source false negative, not a real design gap.)

Composition rules (to be stated in Phase 0.5):
- **v0.3 amends and clarifies v0.2 only where labeled `AMENDS` / `CLARIFIES`;**
- **v0.2 remains baseline where not amended;**
- **in conflicts, v0.3 controls for the amended clauses;**
- the **governing-spec manifest must pin BOTH commits** (`294494a` **and** `c6aeb2b`) before any response-only canary is run.

---

## F. Date / lookahead boundary clarification (refinement 4)

Phase 0.5 can verify **date-spec exactness**, but **cannot validate actual ingestion availability** in a contact-free pass.

**Phase 0.5 MAY verify (spec-level):**
- `civil_date = SQLDATE` (committed count-build Decision D; `SQLDATE_COLUMN_INDEX = 1`; memo §9 / `e55e09a`);
- **no event-occurrence backdating** in the spec;
- the **+1 availability-lag rule is specified** (`rows_from_offset_plus_1`; join memo's `civil_date+1` anchor);
- **no lookahead is intended** in the design.

**Phase 0.5 MUST NOT claim** it has **empirically validated no-lookahead**. A contact-free spec-conformance pass proves the *intended rule is exact*, not that ingestion timing holds.

**Future extraction-time validation requirement (parked for Phase 2):**
- At **Phase 2**, before interpreting extracted daily rows as available at `civil_date + 1`, the execution gate **must validate availability timing**;
- either **confirm day-`t` SQLDATE rows were ingested / available by `t+1`**, or **use the GDELT update-file date as the availability stamp**;
- if availability timing **cannot be verified to exactness**, the extraction / join path must **BLOCK or route to design review**;
- this is a **seal-risk item parked for extraction-time validation** — **not** a Phase 0.5 conformance failure if the spec is exact about the intended rule.

---

## F2. Field-selection scope clarification

Phase 0.5 must distinguish **row-universe / no-filter conformance** from **extraction field selection** — two different axes (row inclusion vs column reading).

- The v0.3 **in-scope rule (row universe)** verifies the row universe is **all global GDELT 1.0 Event rows with no geo/actor/EventCode/text/market *row* filters**. That does **not** imply unrestricted **field** reads.
- **EventCode is deliberately dual-use here:**
  - **no EventCode *row filter*** means rows are **not subset** by EventCode — **every EventCode's rows remain in the universe**;
  - **separately, no EventCode *family / field read*** means the **EventCode column/family is not extracted**;
  - these are **not contradictory**: one governs **row inclusion**, the other governs **column selection**.
- **Field selection remains a v2.1 / extraction-stage invariant** (not a new v0.3 governing-spec amendment). The durable v2.1 prompt (`3411db5`, `docs/lane2_gdelt1_type_tone_goldstein_extraction_execution_prompt_v2.1.md`) and the gate memo (`ea891e0`) **already lock the field allow-list to implementation exactness**: the extraction path reads **only** these five fields — **date / information-date (`civil_date`/SQLDATE), `QuadClass`, `GoldsteinScale`, `AvgTone`, `NumMentions`** — with **no `EventCode` / `EventBaseCode` / `EventRootCode` family, no actor fields, no location fields, no article text, no market data/outcome fields, no price-derived fields (including trailing realized volatility), and no "just in case" fields** unless a future, separately-committed design authorizes them.
- **Trailing realized volatility is explicitly NOT an extraction field** (mirroring the durable v2.1 forbidden-field list: "any price-derived field, including trailing realized volatility"). It remains a **parked future join-gate control / confound issue** (the §12 routed-warning trailing-RV-control precondition is a *future join-gate* design item) — it is **not** read or extracted at this extraction stage, and Phase 0.5 must not treat the future-join-gate RV-control discussion as permission to read a price-derived field now.
- **Phase 0.5 may verify that this field-selection invariant is preserved** in the amended prompt, and **must not infer "no field restriction" from "no row filters."** This amendment **does not** create a new v0.3 field allow-list and **does not** authorize field reads or extraction.

---

## G. Amended Phase 0.5 checklist scope

The amended Phase 0.5 canary must verify **at least**:

1. **governing-spec manifest includes BOTH `294494a` and `c6aeb2b`** (else `STALE-SOURCE BLOCKED`);
2. in-scope universe = **all global GDELT 1.0 Event rows**, **no** geo/actor/EventCode/text/market *row* filters;
2b. **field-selection scope is consciously separated from row-universe scope** (§F2): *no row filters does not mean unrestricted field reads.* EventCode is the concrete dual-use example — **no EventCode row filter keeps all EventCode rows in the universe**, while **no EventCode family / no EventCode field read keeps the EventCode column/family out of the extraction payload**. Phase 0.5 must verify the durable v2.1 / extraction-stage **field allow-list invariant is preserved** (only `civil_date`/SQLDATE, `QuadClass`, `GoldsteinScale`, `AvgTone`, `NumMentions`), and **must not** treat v0.3's all-row universe as permission to read **EventCode family, actor, location, article text, market data/outcome fields, price-derived fields (including trailing realized volatility), or other non-allow-listed fields**;
3. date logic spec-locked as **`civil_date = SQLDATE`**, no event-occurrence backdating, intended **+1 availability lag**, with **empirical no-lookahead / ingestion-availability validation explicitly deferred to Phase 2** extraction-time validation (§F);
4. **primary controlled-association statistic = full-rank simultaneous Spearman partial** (§C);
5. **planted-signal `y_synth` construction locked**: AR(1)-style surrogate target with binding `φ_synth = 0.50`, seed `1729`, gain calibrated to realized pre-stack association (§D);
6. planted-signal **injection point = raw-component / pre-standardization only**;
7. **"pre-standardization composite" removed** as invalid;
8. transformation sequence **includes the compositing step and the simultaneous partial**;
9. **retention denominator = pre-control plain Spearman**;
10. **retention numerator = post-control full-rank simultaneous Spearman partial with `y_synth` substituted for outcome**;
11. **`|retention| ≥ 0.50` is the §11 planted-signal fidelity ratio** and is **distinct from §12 influence-gate magnitude retention**;
12. **MDE floor = deterministic rule output**, not fixed `0.05` or fixed `0.07`;
13. **`φ_synth = 0.50` = binding planted-signal conservative case**;
14. **§12 influence gate = at-join future-rule specification only**; must **not** be executed or treated as extraction-stage work;
15. v2.1 (as amended) **does not authorize** execution, extraction, V1/V2, market data, outcome join, or 2023+.

---

## H. Canary outcome logic after amendment

- If amended Phase 0.5 can extract **all** required locks from **`294494a` + `c6aeb2b`**, it may return **`CLEANLY LOCKED`**.
- If it can only extract from **`294494a`** (manifest missing `c6aeb2b`), it must return **`STALE-SOURCE BLOCKED`**, **not** `CLEANLY LOCKED`.
- If it cannot resolve the **primary statistic / control mechanism / outcome treatment** to implementation exactness, it must return **`BLOCKED`**.
- If it cannot resolve **`y_synth` construction** to implementation exactness, it must return **`BLOCKED`**.
- If it **conflates §11 planted-signal retention ratio with §12 influence-gate magnitude retention**, it must return **`BLOCKED`**.
- If it **treats §12 as executable at extraction**, it must return **`BLOCKED`**.
- If it **claims empirical no-lookahead validation** from a contact-free spec-conformance pass, it must return **`BLOCKED`** or **revise the claim to "extraction-time validation deferred"** (§F).
- If it **conflates row-universe / no-filter logic with unrestricted field selection** — including conflating **"no EventCode row filter" with "permission to read the EventCode field/family"** — or treats the v0.3 all-row universe as permission to read **non-allow-listed fields**, it must return **`BLOCKED`** or **revise the claim to preserve the v2.1 / extraction-stage field-selection invariant** (§F2).

---

## I. Sequence after this amendment

1. **review** this draft amendment;
2. **commit/push** it in a **separate** durability turn if approved;
3. run a **fresh contact-free response-only Phase 0.5 canary** against the amended v2.1 + the two-commit manifest;
4. **only if** the canary returns **`CLEANLY LOCKED`**, consider a **separate execution-authorization turn**;
5. **execution remains UNOPENED** until then.

---

*Filed as a design-only v2.1 Phase 0.5 conformance-checklist amendment DRAFT (v0.1). It does BOTH load-bearing parts — (a) adds the missing primary-statistic / control-mechanism / outcome-treatment checklist item (plus the (a2) `y_synth` construction lock), and (b) repoints Phase 0.5's governing source from `294494a` alone to the `294494a` + `c6aeb2b` chain with a manifest pinning both — and folds in the `y_synth`-exactness and date/lookahead extraction-time-validation refinements. It authorizes no canary run, no execution, and no data contact. The 2023+ seal remains intact.*
