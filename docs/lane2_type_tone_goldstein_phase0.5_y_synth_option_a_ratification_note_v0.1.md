# Lane 2 — Phase 0.5 `y_synth` Option A Ratification Note v0.1

## 1. Status

- **Design-only.** Records researcher ratification of **Option A** (the conformance-repair path from the `y_synth` contradiction design-review memo).
- Authorizes **no** execution, **no** canary, **no** data contact, **no** extraction, and performs **no** commit/push by itself.

## 2. Ratification

- The researcher **ratifies Option A**.
- `4fe1f0c` §D's "**i.i.d.-by-day `y_synth`**" language is treated as a **Phase 0.5 checklist restatement error** (it imported the injected signal's no-autocorrelation property onto the wrong named object).
- **v0.3's AR(1) `y_synth` regime is preserved**: `y_synth` is an AR(1)-style surrogate target with persistence `φ_synth`, binding `φ_synth = 0.50`; the injected signal is the separate daily/high-frequency, no-autocorrelation lead-lag object; target persistence and injected-signal character remain separate design objects (v0.3 §8 L76/L77/L79, §10 L106).

## 3. Consequence

- This **knowingly preserves the harder conservative binding planted-signal regime**: `φ_synth = 0.50`.
- `N_eff` is **deflated** relative to φ=0 (`N_eff ≈ N·(1−0.50)/(1+0.50) ≈ N/3`).
- The planning floor remains **around `0.093`**, **not** the easier i.i.d. / φ=0 floor **around `0.054`** (v0.3 §10 L104/L106 planning values).
- Option A is therefore **not cosmetic** — it ratifies the higher, effective-N-deflated fidelity bar.

## 4. Residual question (examined, not closed)

- A persistent `y_synth` may contain **lower-frequency structure that rank-date control can legitimately absorb**, attenuating the measured §11 fidelity ratio for reasons unrelated to predictor-pipeline failure.
- This is **examined-not-closed**.
- It **does not block Option A** as a conformance repair.
- It may be **revisited at the diagnostic / join-gate design stage** if needed.

## 5. Validity boundary

- This is **conformance repair only**.
- It **does not prove causal validity**.
- The **trailing-RV / causal-DAG issue remains parked-open** for the future join gate.

## 6. Durability strategy note

- This draft uses an **in-place working-tree correction only** to make the diff reviewable against the committed base (`4fe1f0c` amendment SHA `3d2ffd9b…`).
- The **later commit turn must explicitly decide and record the durability strategy**, one of:
  - **in-place correction commit** that **supersedes `4fe1f0c` §D**, or
  - **additive correction artifact** that **composes over `4fe1f0c`**.
- If **in-place correction** is chosen, the correction commit **must explicitly state that it supersedes the old `4fe1f0c` §D wording**.
- If **additive correction** is chosen, the manifest / composition rule **must explicitly state that the additive correction controls over `4fe1f0c` for `y_synth` construction**.
- **No durability strategy is finalized by this draft-only prompt.**

## 7. Future anchor discipline

- The correction commit **will move HEAD and change the amendment SHA**.
- The next fresh **contact-free canary must pin the corrected amendment commit and the updated manifest**.
- Any **stale `4fe1f0c` pin after the correction would be invalid for Phase 0.5**, mirroring the **stale-`294494a` failure mode** this amendment was designed to avoid.

## 8. Final status

`OPTION A RATIFIED FOR CONFORMANCE REPAIR — EXECUTION STILL NOT AUTHORIZED`
