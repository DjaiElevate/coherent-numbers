# Lane 2 — Type / Tone / Goldstein Extraction-Authorization Gate Memo (v0.1, DRAFT)

## 1. Title and status

**Document type:** Extraction-authorization **gate memo draft**. It prepares the authorization *structure* for a future type/tone/Goldstein extraction — the preflight, guard, conformance, artifact, and post-extraction-diagnostic requirements — so that a later, explicit execution prompt can be evaluated against a fixed gate.

**THIS IS NOT AN EXECUTION.**
**This memo draft itself does not contact data** — no GDELT contact, no raw event-file read, no fetch, no extraction, no feature build, no 2023+ read.
**This memo authorizes no extraction.** No extraction may occur until a **separate, explicit execution prompt** is issued and passes this gate. Drafting or committing this memo does not open the extraction gate.

| Field | Value |
|---|---|
| Date of draft | 2026-06-01 |
| Canonical HEAD at drafting | `294494a1badf2d02866def75e985fb2dd0dc99c9` (`294494a`) == `origin/main` |
| Governing spec commit | `294494a1badf2d02866def75e985fb2dd0dc99c9` (lock-closed v0.2) |
| Status | DRAFT GATE MEMO — not authorizing, not executing |
| 2023+ OOS seal | Sealed; this memo keeps it sealed |
| Extraction gate | UNOPENED (this memo prepares it; it does not open it) |

---

## 2. Governing lineage

- **`219f37c` — divergence record.** Caps the ungated market-data acquisition + next-session-return join arc as EXPLORATORY-ONLY; records the governance gap (no guard, no conformance artifacts) this gate is designed to prevent recurring.
- **`0295406` — design baseline (v0.1).** Mechanism (intensity/valence pressure, not amount), primary outcome `abs(next_session_return)`, single composite `intensity_valence_pressure`, negativity-only, no-rescue, frozen-from-in-sample standardization, strict 2023+ seal, §18 guard / §19 conformance requirements.
- **`294494a` — lock-closed v0.2.** All scientific/formula/method locks closed to single values (S1, S2, F1–F4, M1, Z1, Z2, P1, P2, Y1, C1); V1/V2 kept as gate-time verifications; R1/R2 as reporting specs; §4 split into algebraic pre-check (gates lock closure, PASS) vs empirical costume check (gates outcome join).

**Any future extraction implementation MUST declare:**

```
governing_spec_commit = 294494a1badf2d02866def75e985fb2dd0dc99c9
```

---

## 3. Design-to-execution provenance link

- **Every future extraction manifest MUST pin the governing spec commit `294494a`** (`governing_spec_commit = 294494a1badf2d02866def75e985fb2dd0dc99c9`).
- A **conformance check MUST verify the implementation against `294494a` before any data contact.** The check confirms that the formulas, denominator, validity rules, floor, scaler, and stack the implementation will apply match the locked values in `294494a`.
- **Failure to verify against `294494a` blocks extraction.** No data contact may proceed on an unverified or drifted implementation.
- **Why:** this directly prevents the prior failure mode (recorded in `219f37c`) where execution drifted from committed design and ran with no guard and no conformance artifacts. Pinning + pre-contact conformance makes design-to-execution drift a hard stop, not a silent slip.

---

## 4. Gate preflight — V1 / V2

Both must pass **before** any extraction execution. They are **gate-time schema verifications, not scientific degrees of freedom** — they confirm the substrate matches the locked design; they do not re-open any locked choice.

- **V1 — re-verify Step 2 volume-control column names** against the committed Step 2 table (`results/lane2_gdelt1_step2_daily_features/20260531T020244Z/step2_daily_features.csv`, schema as of `cb1122a`):
  - `log1p_total_row_count`
  - `roll_mean_log1p_total_w30`
  - `coverage_completeness`
- **V2 — confirm GDELT 1.0 field positions / value ranges** for:
  - date field / information-date field
  - `QuadClass`
  - `GoldsteinScale`
  - `AvgTone`
  - `NumMentions`
- **If V1 or V2 fails: stop and require a new design / gate path.** Do not "adapt" the locked design to the schema inline; a mismatch is a design-review trigger, not a tuning opportunity.

---

## 5. Guard requirement

- A **`STEP2_EXECUTION_AUTHORIZED`-style guard** is required for this extraction (analogue of the Step 2 execution wrapper).
- The guard must be **false by default**.
- It must be **explicitly enabled only for the single authorized extraction command**.
- It must be **restored in a `finally`** block so the default-inert state is guaranteed even on error.
- **Post-run proof must show the guard restored to false** (e.g. source-line value, committed-blob SHA match, clean `git diff`).
- **No extraction may run without the guard.** A run that bypasses or hard-codes the guard is non-conformant and its outputs are void.

---

## 6. Authorized future extraction scope

If — and only if — a later explicit execution prompt authorizes it, the extraction scope is:

- **in-sample only;**
- **no 2023+;**
- **no market outcomes;**
- **no outcome join;**
- **no `next_session_return`;**
- **no `abs(next_session_return)`;**
- **no result computation.**

It may **only** extract the **locked feature table** needed for the type/tone/Goldstein composite (the daily F1/F2/F3 components and the inputs they require), nothing else.

---

## 7. Fields allowed

Only the fields required by `294494a`:

- date / information-date field;
- `QuadClass`;
- `GoldsteinScale`;
- `AvgTone`;
- `NumMentions`.

- **No `EventCode`, `EventBaseCode`, or `EventRootCode`** unless a future, separately committed design authorizes them.
- **No "just in case" field extraction.** Retaining unlisted fields is non-conformant.

---

## 8. Locked formulas to implement — NON-AUTHORITATIVE convenience summary

> **This section is a convenience summary only. The governing source of truth is commit `294494a1badf2d02866def75e985fb2dd0dc99c9`. If this summary and `294494a` differ, `294494a` governs.**

- **Common denominator:** total daily in-scope `NumMentions` (the whole in-scope daily attention field, not a per-component valid subset).
- **F1 — material-conflict pressure:** mention-weighted `QuadClass = 4` share = `Σ NumMentions[QuadClass=4] / total in-scope NumMentions`.
- **F2 — negative structural-impact pressure:** `Σ NumMentions × max(0, −GoldsteinScale) / total in-scope NumMentions`.
- **F3 — negative-tone pressure:** `Σ NumMentions × max(0, −AvgTone) / total in-scope NumMentions`.
- **Missing/non-numeric Goldstein or tone** contributes **0 to that component's numerator** but **does not shrink the common denominator**.
- **M1 — effective-sample floor:** `N_eff_mentions = (Σ NumMentions)² / Σ(NumMentions²) ≥ 100` (Kish effective event count); below-floor days excluded from the primary composite.
- **Z1 — scaler:** expanding past-only z-score per component, 365 prior valid in-scope days warmup, sub-warmup → NaN/exclude.
- **Composite:** equal-weight of standardized F1/F2/F3 = `intensity_valence_pressure`.

(Degenerate-case policy F4, drift/volume controls Z2, planted-signal P1/P2, per-year Y1, costume thresholds C1 — all per `294494a`.)

---

## 9. Required output artifacts

A future authorized extraction must produce, at minimum:

- extracted feature table (the locked daily F1/F2/F3 + composite-input table);
- extraction manifest (pinning `governing_spec_commit = 294494a`);
- metadata JSON;
- boundary declaration;
- source schema verification report (V2 result);
- governing-spec conformance report against `294494a`;
- SHA-256 hashes (of every produced artifact);
- row / date coverage summary;
- no-2023+ proof;
- guard restoration proof (guard back to false);
- `git status` proof (clean / expected tree).

---

## 10. Outcome-free diagnostics after extraction, before any outcome join

These are allowed **only after a separately authorized extraction run** and **before any market outcome join**. They run in this **required order:**

1. **Sample sufficiency report** (§11 — must be first).
2. **Planted-signal full-stack sensitivity check** (gate detail below).
3. **§4B empirical volume / coverage-quality costume check** (C1 thresholds in `294494a`).
4. **R1 component collinearity matrix.**
5. **R2 missing-field / excluded-field mention-fraction diagnostics.**

**All diagnostics must remain:** outcome-free; no-2023+; no `next_session_return`; no `abs(next_session_return)`; no market-data join.

### Planted-signal gate

- **Synthetic target only.** Must **never** use `next_session_return`, `abs(next_session_return)`, any market outcome, or 2023+.
- Runs **after extraction**, on the extracted composite/components.
- Injects a **daily / high-frequency synthetic signal at the raw-component or pre-standardization composite level**.
- Pushes the planted signal through the **full locked stack:** standardization → drift/time control → per-year check → incremental-over-volume control.
- **Locked grid:** `rho_plant = {0.05, 0.10, 0.20}`.
- **Binding criterion:**
  - the **`rho_plant = 0.05` floor must retain the same sign and ≥ 50% retention** after the full stack;
  - **failure at `rho_plant = 0.05` blocks the outcome join;**
  - `rho_plant = 0.10` and `0.20` are reported as detection-floor diagnostics but **cannot rescue failure at 0.05**.
- **If the planted-signal check fails: stop before outcome join.** A real-outcome null would be uninterpretable, because the pipeline has not shown it can preserve the smallest signal the design cares about. (Deterministic seed `1729` per `294494a`.)

---

## 11. Sample sufficiency must be first

The **first** post-extraction report must lead with **pre-join sample sufficiency**.

**Pre-join computable sufficiency:**
- valid composite days after `N_eff_mentions ≥ 100`;
- valid composite days after the 365-day warmup;
- valid composite years available before any outcome join;
- number of years with at least 100 valid composite days.

**Important distinction (pre-join lower bound, not the final Y1 count):**
- Y1's binding per-year threshold is based on **valid paired observations**.
- Paired observations require an **outcome join**, which does **not** exist at this stage.
- Therefore pre-join valid composite days/years are a **necessary lower bound, not the final Y1 paired-observation count**.
- A year with **fewer than 100 valid composite days cannot possibly reach 100 paired observations** after join (pairing can only preserve or reduce the count).
- The **binding paired-observation count must be confirmed later**, after a separately authorized outcome join.

**If pre-join sample sufficiency fails: stop before interpreting** the planted-signal, costume, collinearity, or missingness diagnostics.

---

## 12. Outcome join firewall

- **No outcome join is authorized by this memo.**
- An outcome join requires a **separate future authorization**, granted only after **all** of:
  - extraction artifacts are pinned;
  - sample sufficiency is known and sufficient as a pre-join lower bound (§11);
  - planted-signal `rho_plant = 0.05` floor retention passes (§10);
  - empirical costume check passes or is caution-labeled (§4B / C1);
  - R1 component collinearity matrix is reported;
  - R2 missing-field / excluded-field mention-fraction diagnostics are reported;
  - no-2023+ proof is confirmed;
  - guard restoration proof is confirmed.
- **If planted-signal, sample sufficiency, or empirical costume diagnostics fail, the next step is a design-review memo / new gate — not an inline tuning loop.** Revising formulas and re-extracting inside the same gate is prohibited (it would become a tuning loop, the exact anti-pattern `294494a` §4B forbids).

---

## 13. Non-authorizations

This memo explicitly does **NOT** authorize, and nothing in it permits:

- no GDELT contact now;
- no raw event-file read now;
- no extraction now;
- no feature build now;
- no 2023+ read;
- no market join;
- no outcome computation;
- no result generation;
- no implementation;
- no staging;
- no commit;
- no push.

---

*Filed as a draft extraction-authorization gate memo. It pins the governing spec `294494a`, requires V1/V2 preflight + a default-false guard + governing-spec conformance, fixes the required output artifacts, and orders the post-extraction outcome-free diagnostics (sample sufficiency first → planted-signal full-stack → empirical costume → R1 → R2) behind an outcome-join firewall. It contacts no data and authorizes no extraction; a separate explicit execution prompt is required. The 2023+ seal remains intact.*
