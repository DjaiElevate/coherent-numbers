# Lane 2 — Phase 0.5 `y_synth` Contradiction Design-Review Memo v0.1

## 1. Status and non-authorization

**Design-review memo DRAFT only.** It records and analyzes a confirmed source contradiction. It fixes nothing and authorizes nothing.

This memo does **not** authorize and **does not perform**: execution; a canary rerun; GDELT contact; source-file enumeration/read (beyond committed `docs/` markdown + git metadata); extraction; extraction code; synthetic tests; guard flips; V1/V2; market data; outcomes; `next_session_return` / `abs(next_session_return)`; 2023+; `.gitignore` edits; result-output writes; staging, commit, or push by this prompt. The only repo write is the creation of this memo draft.

---

## 2. Trigger

The completed external byte-review verdict is:

`PHASE 0.5 BYTE-REVIEW VERDICT: INFERENCE-OVERREACH BLOCKED — EXECUTION NOT AUTHORIZED`

The in-session re-canary (`/tmp/lane2_type_tone_goldstein_phase0.5_recanary_report.md`, final line `PHASE 0.5 RE-CANARY VERDICT: CLEANLY LOCKED — EXECUTION STILL NOT AUTHORIZED`) returned `CLEANLY LOCKED`, but **external byte-review overturned that verdict** because **item 8 (`y_synth` construction) contains a contradiction between pinned source documents.**

Explicitly:
- **Transport / source completeness is no longer the blocker** (all four governing artifacts + the gate memo were exported and byte-verified; see §3).
- **The blocker is a real contradiction in committed design/checklist bytes** (§4).
- **Execution remains unauthorized.**

---

## 3. Source integrity basis

Identity facts (from the external byte-review bundle and its manifest):
- bundle SHA-256: `8a081195d6381244ee342ed6ec9c1b7196995f178b4beaa073fae3cbcdbe68d2`
- `3411db5` v2.1 prompt SHA: `cce945b0119075aaae85a36087bd433d6e4f2e25d91769e68e980b3f269cccab`
- `4fe1f0c` amendment SHA: `3d2ffd9b3b4611b7aaba4e8af478af1020e6ebf4a2e8f093e2fb457f9fc9f447`
- `c6aeb2b` v0.3 SHA: `714509656a9414f9b6c0858a919f08d524e9fd59549ec74441c0aed00582f2f7`
- `294494a` v0.2 SHA: `10ba64b24dfb36a6dd45eaa5477f6563ec03f77fe20290af347109abd3bbe038`
- `ea891e0` gate memo SHA: `cc7edb9ff1544a61f5b674431c163fcb1dd2401338d671198041a4c511437124`
- re-canary report SHA: `3694c60b60c2a416c67399820eab848a3e6fae8fa8b3ae931ae33f9564017f9e`

**Source transport is no longer the blocker; the blocker is a real source contradiction** grounded in the committed bytes quoted in §4 (not in any prompt paraphrase).

---

## 4. Exact contradiction (grounded in committed bytes)

All quotes below are pulled directly from committed bytes via:
`git show <commit>:<path> | nl -ba | sed -n '<start>,<end>p'`.

### 4.1 `4fe1f0c` §D — `git show 4fe1f0cdc15c5481a758cd5fdd7248a83a6aac72:docs/lane2_gdelt1_type_tone_goldstein_v2.1_phase0.5_amendment_v0.1.md | nl -ba | sed -n '73,84p'`

> L73 `**[Phase 0.5 — NEW ITEM] Planted-signal surrogate `y_synth` locked to implementation exactness.** Phase 0.5 must extract and confirm, against v0.3 (`c6aeb2b`):`
> L74 `- `y_synth` is an **i.i.d.-by-day synthetic surrogate** (no autocorrelation in the *injected signal* path);`
> L80 `  - `φ_synth` is **surrogate-target persistence / effective-N planning** for the planted-signal MDE floor;`
> L81 `  - the **injected signal remains daily / high-frequency** lead-lag;`
> L82 `- **binding planted-signal case remains `φ_synth = 0.50`** (conservative; lower-φ reported but cannot rescue).`

So within the same §D item: **L74 calls the named object `y_synth` "i.i.d.-by-day"** (which implies the surrogate target has zero autocorrelation), while **L80/L82 assert `φ_synth` is the surrogate-target persistence and is binding at `0.50`**. §D is therefore **internally inconsistent**: the parenthetical on L74 ("no autocorrelation in the *injected signal* path") tries to scope i.i.d. to the injected signal, but the sentence subject is `y_synth` (the surrogate **target**), so the wording labels `y_synth` itself i.i.d.

### 4.2 `c6aeb2b` §8 — `git show c6aeb2b84279e3d8955b94ae31778f95e3d1fa14:docs/lane2_gdelt1_type_tone_goldstein_lock_closure_v0.3.md | nl -ba | sed -n '76,79p'`

> L76 `- **Surrogate target `y_synth` (the outcome stand-in):** an **AR(1)-style series with persistence `φ_synth`** (binding `φ_synth = 0.50`, §10), deterministic seed **`1729`**. Its persistence exists **only to power-match / stress the effective-N environment** of the diagnostic.`
> L77 `- **Injected signal (separate object):** a **daily / high-frequency lead-lag** additive term … The **injected signal remains daily/high-frequency** — it is **not** trend-shaped or regime-shaped …`
> L79 `**Separation (LOCKED):** *"The surrogate target may carry AR(1)-style persistence (`φ_synth`) for power-matching, but the planted relation injected into the raw component remains a daily/high-frequency lead-lag signal. The φ grid varies surrogate-target persistence, not the temporal character of the injected signal."* Target persistence and injected-signal character are **separate design objects**.`

v0.3 §8 is unambiguous: **`y_synth` (the surrogate target) is AR(1)-style with persistence `φ_synth`, binding `0.50`**; the **injected signal** is the *separate* daily/high-frequency object; **target persistence and injected-signal character are separate design objects.**

### 4.3 `c6aeb2b` §10 — `git show c6aeb2b84279e3d8955b94ae31778f95e3d1fa14:docs/lane2_gdelt1_type_tone_goldstein_lock_closure_v0.3.md | nl -ba | sed -n '106,106p'`

> L106 `**Binding planted-signal case: `φ_synth = 0.50`** ⇒ binding planted floor = the MDE-rule output at the diagnostic's effective-N under `φ_synth=0.50` (planning example ≈ **0.093** pooled). Lower-φ cases are **reported as sensitivity / planning context only**; **passing lower-φ cannot rescue failure at the binding `φ_synth=0.50` floor.** Rationale: `φ_synth=0.50` is conservative — it avoids certifying fidelity only under an easy low-autocorrelation surrogate. It does **not** claim the real outcome has φ=0.50.`

### 4.4 The contradiction

- **i.i.d.-by-day** (`4fe1f0c` §D L74 applied to `y_synth`) ⇒ **φ = 0**.
- **AR(1) with `φ_synth = 0.50`** (`c6aeb2b` §8 L76 / §10 L106) ⇒ **φ = 0.50**.
- **The same named object, `y_synth`, cannot be both** φ = 0 and φ = 0.50. This is a direct contradiction between the pinned Phase 0.5 amendment and the pinned v0.3 governing amendment — and `4fe1f0c` §D is additionally internally inconsistent (§4.1).

---

## 5. Why this blocks Phase 0.5

`4fe1f0c` itself makes the unresolved `y_synth` construction a hard `BLOCKED`:

`git show 4fe1f0cdc15c5481a758cd5fdd7248a83a6aac72:docs/lane2_gdelt1_type_tone_goldstein_v2.1_phase0.5_amendment_v0.1.md | nl -ba | sed -n '84p;167p'`

> L84 `**Failure to lock `y_synth` construction ⇒ `BLOCKED`**, because the §11 retention numerator/denominator (and the §12 floor calibration) **cannot be reproduced to exactness** without the exact surrogate construction.`
> L167 `- If it cannot resolve **`y_synth` construction** to implementation exactness, it must return **`BLOCKED`**.`

**Why this is substantive, not cosmetic** (causal chain):
1. `y_synth` persistence drives **`N_eff`** (v0.3 §10 L100: `N_eff ≈ N·(1−φ)/(1+φ)`);
2. `N_eff` drives the **MDE floor** (v0.3 §10 L104/L106, deterministic rule output);
3. the MDE floor drives the **injected-signal gain calibration** (v0.3 §8 L77: "Gain calibrated so the realized pre-stack plain Spearman of composite vs `y_synth` equals the targeted MDE floor");
4. that calibrated quantity feeds the **§11 retention denominator** (pre-control plain Spearman of composite vs `y_synth`);
5. therefore the **§11 fidelity ratio cannot be reproduced to exactness** until the φ of `y_synth` is unambiguous.

**Quantitative implication** (from v0.3 §10 L104 planning values):
- Under **φ = 0** (i.i.d.): `N_eff ≈ N`; planning floor ≈ **0.054**.
- Under **φ = 0.50** (AR(1)): `N_eff ≈ N·(1−0.50)/(1+0.50) ≈ N/3`; planning floor ≈ **0.093**.
- This is **not cosmetic wording** — it changes the effective-N-deflated fidelity bar and the calibration target by roughly a factor (floor ≈ 0.054 vs ≈ 0.093; `N_eff` ≈ N vs ≈ N/3).

---

## 6. Non-item-8 findings

The external byte-review found the other **fifteen** items byte-faithful to the amended source chain (`294494a` + `c6aeb2b`; `3411db5` + `4fe1f0c`):
- governing-spec repoint to `294494a + c6aeb2b` (not `294494a` alone);
- row-universe / field-selection separation (incl. EventCode dual-use, 5-field allow-list, no price-derived incl. trailing realized volatility);
- date logic + Phase-2 no-lookahead / ingestion-availability deferral;
- primary controlled-association statistic + outcome treatment;
- injection point / transformation sequence / retention numerator and denominator;
- §11 (planted-signal fidelity ratio) / §12 (at-join influence-gate floors) separation;
- MDE floor as deterministic rule output;
- §12 non-executability at extraction;
- non-authorization preserved.

**This memo is narrowly about item 8 (`y_synth` construction) only.**

---

## 7. Reconciliation options

### Option A — conformance repair preserving v0.3's AR(1) regime

Treat `4fe1f0c` §D L74 as a **checklist restatement error**. Correction direction:
- `y_synth` is **AR(1)-style with `φ_synth = 0.50`**;
- the **injected signal** is daily/high-frequency and **not** trend/regime-shaped;
- `φ_synth` belongs to **surrogate-target persistence / effective-N planning**;
- **injected-signal character remains separate** from target persistence.

**Structural case for Option A** (not merely "smallest correction"):
1. `4fe1f0c` is a **Phase 0.5 checklist amendment** that explicitly says (L73) Phase 0.5 must "**extract and confirm, against v0.3 (`c6aeb2b`)**." Its role is to **restate/check v0.3**, not to introduce a new `y_synth` design.
2. The `i.i.d.-by-day y_synth` phrase contradicts **three v0.3 anchors**:
   - v0.3 §8 (L76): `y_synth` is AR(1)-style with `φ_synth`;
   - v0.3 §10 (L106): binding `φ_synth = 0.50` is the conservative case;
   - the v0.3 MDE / effective-N / binding-floor machinery (§10 L100/L104/L106) depends on `φ_synth = 0.50`.
3. v0.3 does **not merely mention** `φ_synth = 0.50`; it gives a **rationale** (§10 L106): "avoid certifying fidelity only under an easy low-autocorrelation surrogate."

**Consequence of Option A (stated plainly):**
- Option A **knowingly ratifies the harder, effective-N-deflated fidelity bar** (floor ≈ 0.093, `N_eff ≈ N/3`).
- Option A is **not "free" or purely cosmetic.**
- It **preserves the v0.3 conservative `φ_synth = 0.50` regime and the higher binding floor.**

### Option B — larger redesign making `y_synth` i.i.d.

Treat `4fe1f0c` §D L74 as **intentional**. Then **v0.3 §8/§10 must be revised**, because the AR(1) `φ_synth = 0.50` machinery conflicts with an i.i.d. target. This would affect: the MDE floor; effective-N assumptions; injected-signal gain calibration; the §11 retention denominator; the canary checklist; and likely later diagnostic design.

**Option B is a larger redesign, not a local checklist fix.**

---

## 8. Provisional recommendation and researcher-ratification requirement

`Provisional recommendation pending researcher ratification: Option A.`

(Option A is **not** presented as already decided.)

Reasons:
- v0.3 (`c6aeb2b`) is the document the checklist amendment **explicitly points to** (`4fe1f0c` §D L73);
- v0.3's AR(1) `y_synth` regime is **reasoned** and **structurally tied** to the MDE/fidelity machinery;
- `4fe1f0c` §D appears to have **imported "i.i.d." into the wrong named object** (the parenthetical on L74 scopes it to the injected signal, but the subject is `y_synth`);
- Option A rests on the **structural fact** that the checklist amendment (`4fe1f0c` §D L73) points to v0.3 and that v0.3's AR(1) regime is documented across **§8 (L76) and §10 (L106)**; the recommendation does **not** rely on the re-canary caveat as an authority. *(The re-canary caveat — which noted "i.i.d.-by-day applies to the injected signal; `y_synth` target carries `φ_synth` persistence" — is **evidence of the self-grading miss**, i.e. the contradiction was silently resolved by inference, **not** an authority for Option A.)*
- Option A is the **smallest conformance repair that preserves the ratified v0.3 regime**.

Explicitly:
- **The agent ecosystem may recommend, but the researcher must ratify the A/B choice on the record.**
- **This memo itself does not authorize the correction.**
- A later prompt must record the ratification and implement the correction **if Option A is approved.**

---

## 9. Residual methodological question not closed by Option A

Limitations / residual question (examined, **not closed**):
- Option A repairs **conformance** by aligning the checklist with v0.3.
- It **does not by itself prove** that a persistent `y_synth` is the **ideal** planted-signal diagnostic design.
- A persistent AR(1) `y_synth` contains **lower-frequency structure that rank-date control may legitimately absorb**, which could attenuate the measured fidelity ratio for reasons unrelated to predictor-pipeline failure.
- An **i.i.d. `y_synth`** would keep the diagnostic **cleaner with respect to date-control absorption**.
- The injected signal being **daily/high-frequency partly offsets** this concern, but the **net implication for what the §11 fidelity ratio measures is non-obvious**.
- This residual diagnostic-design question is recorded as **examined-not-closed** and may be revisited at a later diagnostic / join-gate design stage if needed.
- It **does not automatically block Option A** as the conformance repair, but it **must not be erased by calling Option A a mere typo fix.**

---

## 10. Required next artifacts if Option A is ratified later

A later, **separate** prompt should:
1. record **researcher ratification** of Option A;
2. create a correction artifact **or** amend the existing tracked Phase 0.5 amendment in a **new commit**, explicitly replacing the i.i.d.-by-day `y_synth` wording with v0.3-consistent (AR(1), `φ_synth = 0.50`) wording;
3. **commit and push** that correction;
4. run a **fresh contact-free response-only Phase 0.5 canary**;
5. only after a clean canary **and** any needed external byte-review, consider a **separate execution-authorization turn**.

**None of these are done in this prompt.**

---

## 11. Validity boundary

- This is a **conformance failure, not a validity adjudication.**
- Resolving item 8 **does not prove the method is causally valid.**
- The **trailing realized-volatility / causal-DAG issue remains parked-open** for the future join gate.
- The **persistent-`y_synth` diagnostic-design question (§9) is separate** from the trailing-RV causal-validity question.
- A future clean canary would mean **only that the report faithfully represents the spec**, **not** that the method is scientifically valid.

---

## 12. Final status

`DESIGN REVIEW STATUS: ITEM-8 Y_SYNTH CONTRADICTION CONFIRMED — OPTION A PROVISIONALLY RECOMMENDED PENDING RESEARCHER RATIFICATION — EXECUTION STILL NOT AUTHORIZED`
