# Influential Numbers Program — Cell 1 Closure Memo v0.1

**Version:** v0.1 (Closure)
**Date:** 2026-05-15
**Project:** Coherent Numbers
**Program:** Influential Numbers
**Cell:** Cell 1 — Neighborhood Influence Test
**Status:** Closed
**Verdict:** No neighborhood evidence (Class 3)

**Reference commits**

* Framework memo: `8ff619c` — `docs/influential_numbers_cell_1_framework_memo_v0.1.md`
* Design memo (locked): `a765098` — `docs/influential_numbers_cell_1_design_memo_v0.1.md`
* Lock-acceptance: `3d44e9e` — `docs/influential_numbers_cell_1_design_memo_v0.1_lock_acceptance.md`
* Implementation + tests: `067a43d`
* Verdict log landed (locked run): `5f2d5f2`

**Verdict artifacts**

* JSON: `results/influential_numbers_cell_1_results_20260515_213436_50f2357d.json` (SHA-256: `731cd0e4a518d765262d5cbeadff67f7bbf8e6517b5829a32b92e5aa0d887c0c`)
* Markdown sidecar: `results/influential_numbers_cell_1_results_20260515_213436_50f2357d.md` (SHA-256: `1f00c9541f9e1af3dfcbbe06991eaf11c19c30c2c01296b457d6b7245841a7a8`)
* `rerun_verification_digest`: `50f2357dd3f70f818f6353c1b7d1c3053ff1cd303d6a0ee31dc8aadc68478b02`

---

## 1. Executive summary

Cell 1 — the Neighborhood Influence Test — closes as **Class 3, No neighborhood evidence** on the frozen pullback × pooled Phase 3b 1,282-trade substrate. Under the locked decision rules (design memo `a765098`, §15.3), the verdict is determined by two independent failures: the focal-elevation gate for `k = 12` **fails** (`median_12 = 0.034445901350758625` does not exceed its non-focal window-neighbor mean `0.03467440484746646`; `focal_excess = -0.00022850349670783254`, `ambiguous = False`), **and** `beat_count_12_structure = 5979 < 9500`. Either condition alone routes to Class 3 (design memo §15.3); both hold here. `pathology = None`: this is a clean Class 3, not a Class 4 design-validity failure.

The bounded scope of this verdict is non-negotiable. Cell 1 asked whether `k = 12` sits inside a structured local neighborhood — a different question from Candidate C's "does 12 beat 10?". A no-neighborhood result leaves Candidate C's `12-privileged` verdict exactly intact, does not say the substrate is structureless, does not motivate or authorize Layer 2, and does not bear on Candidate B. The §17 provenance gate passed at floating-point equality (`max_abs_diff_10 = 0.0`, `max_abs_diff_12 = 0.0`), so this null is a property of the locked neighborhood operationalization on this substrate, not implementation drift relative to Candidate C's stored surfaces.

## 2. Locked protocol recap

* **Population.** Pooled Phase 3b 5-asset population — SPY/EFA/EEM/GLD/TLT — 1,282 trades, 2005–2022, frozen at `5225bfd` per `docs/pullback_population_freeze_manifest_v0.1.md`. Inherited unchanged (design memo §5, §6).
* **Lens / PSS.** Parameterized annual-sector lens over `k ∈ K = {7, …, 19}`, civil-March-20 / 365-DOY anchor surface; η²/correlation-ratio `PSS_k = between_k / total_k`; per-bucket-count statistic `median_k` = median over the 365-anchor surface (design memo §7, §9). The PSS arithmetic is a bit-identical fork of Candidate C's `pss_long_share`.
* **Focal structure.** Multi-focal `F = {10, 12, 14, 16}`; primary focal `12`; control focals `10, 14, 16`; `±3` linear-integer window `W(f) = {f−3, …, f+3}` (design memo §8).
* **Structure statistic.** Focal-centered continuous attenuation `attenuation_score_f = −slope(median_k ~ |k − f|)` over the seven window points (distance multiset `{0,1,1,2,2,3,3}`, focal included); strict-`>` focal-elevation gate for 12; contrast `max_gap = attenuation_score_12 − max(attenuation_score_10, attenuation_score_14, attenuation_score_16)` (design memo §10–§12).
* **Nulls.** One shared `N_PERM = 10,000` unstratified pooled `is_long` permutation pool, seed `LABEL_PERM_SEED_CELL1 = 20260518`; two coupled primary beat counts (design memo §13–§14). Threshold `9,500 / 10,000`, strict `<`, ties do not pass.
* **Verdict map.** Four mutually exclusive classes with display names and `class_1..class_4` machine labels; hard-binary Class 4 reserved for pathology only (design memo §15).
* **Provenance gate (§17).** Cell 1's recomputed `k = 10` and `k = 12` 365-anchor surfaces must match Candidate C's stored `protocol_payload.pss_surface_10` / `pss_surface_12` in `results/candidate_c_results_20260515_051236_f3a6bf48.json` at `≤ 1e-12` per anchor; failure routes to Class 4. This is a validity gate, not a diagnostic.

## 3. Required verbatim disclosures (re-emitted from the locked design memo)

The locked design memo `a765098` §22 carries a Required-verbatim block register. The blocks operative for this Class 3 closure, plus the closure-critical caveat / disclosure / anti-rescue blocks, are re-emitted here character-exactly. Any reader of this closure memo must encounter them with the same wording the locked protocol commits to.

### 3.1 Class 3 — what it supports (verbatim, design memo §15.3a)

> **(a) What it supports** *(REQUIRED-VERBATIM, §15.3a):* Under the locked decision rules, there is no evidence that 12 sits inside a structured local neighborhood on this substrate: either 12's median PSS does not exceed its non-focal window neighbors, or the 12-neighborhood attenuation is not distinguished from chance. 12, on the neighborhood operationalization, behaves as an isolated point rather than a structured local peak.

### 3.2 Class 3 — what it does not support (verbatim, design memo §15.3b)

> **(b) What it does not support** *(REQUIRED-VERBATIM, §15.3b):* This null does not weaken Candidate C's `12-privileged` verdict — Cell 1 asks a different question and a no-neighborhood result leaves "12 beat 10 under C's locked rules" untouched. It does not say the substrate is structureless. It does not motivate or authorize Layer 2 (divisor, multiple, harmonic, 12-family, recursive, weighted) as a rescue; per §3 and §21, Layer 2 on a Layer 1 null requires a separate decision memo argued on its own grounds. It does not bear on Candidate B.

### 3.3 Granularity / neighborhood-window caveat (verbatim, design memo §15.5)

> *(REQUIRED-VERBATIM, §15.5):* Every Cell 1 verdict is scope-bounded by the locked neighborhood operationalization. "Neighborhood" here means a `±3` linear-integer window of bucket counts evaluated as the median of each bucket count's 365-anchor PSS surface; different bucket counts correspond to different temporal resolutions (e.g. `k = 12` ≈ 30.4 days/phase, `k = 16` ≈ 22.8 days/phase, `k = 7` ≈ 52 days/phase). A neighborhood verdict reflects how phase-allocation structure varies with bucket-count resolution near the focal, not a claim that any bucket count is structurally "correct," and not a test of divisor/multiple/harmonic/12-family structure. This caveat applies to all four verdict classes.

### 3.4 Compound-verdict / coupled-null disclosure (verbatim, design memo §15.6)

> *(REQUIRED-VERBATIM, §15.6):* The two primary beat counts (`beat_count_12_structure`, `beat_count_max_gap`) are coupled: both are derived from the same shared pool of 10,000 pooled-population `is_long` permutations, and the per-permutation attenuation scores entering both are functions of the same recomputed `K`-wide median-PSS map. The verdict classes are pre-registered decision rules under that joint distribution, not independent p-value claims. The false-positive interpretation of a class assignment is not identical to the false-positive rate of a single independent test at the 95th percentile, and the four classes do not partition probability mass uniformly under the null.

### 3.5 Inherited data-contact disclosure (verbatim, design memo §20)

> *(REQUIRED-VERBATIM, §20):* Cell 1's verdict is conditional on a previously contacted, audit-frozen pullback-event population. The pullback Phase 1–3b series for SPY and the Phase 3b 2005–2022 series for SPY/EFA/EEM/GLD/TLT were inspected, partitioned, and used to estimate within-population statistics during pullback research before Coherent Numbers contacted them. The pullback BacktestParams were locked early at pullback commit 50ee2d1 and not re-tuned, which limits but does not eliminate that prior exposure. Candidate B previously applied 12-phase March-20-anchored machinery to this same population (a 10,000-element unstratified label-permutation null and an exhaustive 365-DOY anchor-control null) and reported a split-null verdict. Candidate C subsequently applied parallel 12-phase and 10-phase machinery to the same population under symmetrical 365-DOY anchor-surface rules and reported a 12-privileged verdict. Cell 1 applies a multi-focal neighborhood operationalization over bucket counts K = {7,…,19} to the same population. Cell 1's verdict is therefore conditional on (i) the pullback program's prior contact with the underlying series, (ii) Candidate B's prior 12-phase contact, and (iii) Candidate C's prior 12-and-10-phase contact, including the k=10 and k=12 365-anchor surfaces Cell 1 reuses as a provenance check. OOS 2023+ remains sealed in both repos and is out of scope for Cell 1. This disclosure is required wording; a hash citation alone does not satisfy it.

### 3.6 Layer 1 / Layer 2 anti-rescue (verbatim, design memo §21.3)

> **21.3 (REQUIRED-VERBATIM anti-rescue — Layer 1 / Layer 2):** Layer 2 (divisor, multiple, 12-family/duodecimal, harmonic-family, recursive-field, or weighted-neighbor influence) is out of scope for Cell 1 and may not be added as a "diagnostic," may not be used to rescue a Class 2/3/4 verdict, and may not borrow authority from the Kryon source. If a Layer 1 null (Class 3) or non-confirmatory result (Class 4) is followed by any Layer 2 consideration, it requires a separate decision memo explaining why Layer 2 remains scientifically justified on its own grounds; it is never an escape hatch from a Layer 1 null.

### 3.7 Cross-cell anti-rescue (verbatim, design memo §21.4)

> **21.4 (REQUIRED-VERBATIM anti-rescue — cross-cell):** Candidate C's `12-privileged` verdict remains independent and is not retroactively reinterpreted by any Cell 1 outcome. Candidate B's split-null equinox result remains **not confirmed** and is not rescued, confirmed, or reinterpreted by any Cell 1 outcome. "12 beat 10 under Candidate C's locked rules" and "Cell 1's neighborhood verdict" are distinct claims that do not transfer authority in either direction.

### 3.8 Non-operative — Class 1 (verbatim, design memo §15.1a / §15.1b)

The following Class 1 blocks are **non-operative** for this closure: Cell 1 did not return Class 1. They are re-emitted here solely to satisfy the locked design memo §22 register; their language describes a `12-centered neighborhood structure` verdict that Cell 1 did **not** reach and must not be read as applying to this Class 3 result.

> **(a) What it supports** *(REQUIRED-VERBATIM, §15.1a):* Under the locked decision rules, the bucket count `k = 12` sits on a focal-centered local elevation whose attenuation away from 12 is distinguished from chance, and that attenuation exceeds the strongest attenuation at any of the control focals `10`, `14`, `16` on this substrate. The 12-neighborhood behaves as a structured local peak rather than an isolated point under the locked protocol.

> **(b) What it does not support** *(REQUIRED-VERBATIM, §15.1b):* The verdict does not establish that 12 is uniquely neighborhood-structured among all bucket counts (only `10, 14, 16` were used as controls); it does not attribute the structure to a duodecimal, divisor, multiple, harmonic, or 12-family property (those are Layer 2 and untested here); it does not establish base-12 mathematics; it does not retroactively reinterpret Candidate C's `12-privileged` verdict, which remains exactly "12 beat 10 under its locked rules"; it does not confirm or rescue Candidate B's split-null equinox result; and it does not generalize beyond the pre-registered substrate, window, or focal set.

### 3.9 Non-operative — Class 2 (verbatim, design memo §15.2a / §15.2b)

The following Class 2 blocks are **non-operative** for this closure: Cell 1 did not return Class 2. They are re-emitted here solely to satisfy the locked design memo §22 register; their language describes a `Generic substrate smoothness` verdict that Cell 1 did **not** reach and must not be read as applying to this Class 3 result.

> **(a) What it supports** *(REQUIRED-VERBATIM, §15.2a):* Under the locked decision rules, the 12-neighborhood shows attenuation distinguished from chance, but that attenuation is **not** distinguished from the attenuation at the strongest control focal. The substrate appears to produce locally smooth neighborhoods around multiple bucket centers; 12's local structure is consistent with that generic smoothness rather than being 12-specific.

> **(b) What it does not support** *(REQUIRED-VERBATIM, §15.2b):* The verdict does not say 12 is unstructured, and it does not say the substrate is structureless; it specifically does not support a 12-specific neighborhood claim; it does not weaken Candidate C (a generic-smoothness reading of the neighborhood is independent of C's binary 12-vs-10 result); and it does not motivate Layer 2 extension as a rescue.

### 3.10 Non-operative — Class 4 (verbatim, design memo §15.4a / §15.4b)

The following Class 4 blocks are **non-operative** for this closure: Cell 1 did not return Class 4 (`pathology = None`; the §17 provenance gate passed; the focal-elevation gate was not `ambiguous`). They are re-emitted here solely to satisfy the locked design memo §22 register; their language describes a `Non-confirmatory / unresolved` verdict that Cell 1 did **not** reach and must not be read as applying to this Class 3 result.

> **(a) What it supports** *(REQUIRED-VERBATIM, §15.4a):* Under the locked decision rules, the result does not support any of Class 1, 2, or 3. A design-validity or pathology condition prevented a valid neighborhood adjudication. Beat counts, if computed, are reported as diagnostic texture only and do not upgrade the verdict.

> **(b) What it does not support** *(REQUIRED-VERBATIM, §15.4b):* This class does not say the substrate is structureless, does not adjudicate the neighborhood question, does not rescue or weaken Candidate C or Candidate B, and does not authorize amending the locked design after the fact.

### 3.11 Full §22 register and operative-block scope

The design memo §22 Required-verbatim block register names thirteen blocks, **all required-verbatim in the locked design memo**, and **all thirteen are re-emitted character-exactly in this closure memo**:

* Per-class support / non-support text: §15.1a, §15.1b, §15.2a, §15.2b, §15.3a, §15.3b, §15.4a, §15.4b.
* Granularity / neighborhood-window caveat: §15.5.
* Compound-verdict / coupled-null disclosure: §15.6.
* Inherited data-contact disclosure: §20.
* Layer 1 / Layer 2 anti-rescue disclosure: §21.3 (treated as closure-critical).
* Cross-cell anti-rescue disclosure (Candidate C independence, Candidate B not-confirmed): §21.4 (treated as closure-critical).

Re-emission map: §15.3a → §3.1; §15.3b → §3.2; §15.5 → §3.3; §15.6 → §3.4; §20 → §3.5; §21.3 → §3.6; §21.4 → §3.7; §15.1a/b → §3.8; §15.2a/b → §3.9; §15.4a/b → §3.10.

The **operative verdict text for this closure is the Class 3 pair, §15.3a and §15.3b** (§3.1, §3.2): Cell 1 returned `class_3`, `No neighborhood evidence`. The closure-critical caveat / disclosure / anti-rescue blocks §15.5, §15.6, §20, §21.3, §21.4 (§3.3–§3.7) apply to this verdict as the locked protocol commits. The per-class blocks §15.1a/b (Class 1), §15.2a/b (Class 2), and §15.4a/b (Class 4) are **non-operative** for this verdict — Cell 1 did not reach those classes — and are re-emitted in §3.8–§3.10 **solely to satisfy the locked §22 register's character-exact re-emission obligation**, not because their language applies here. No non-operative class language describes or modifies the Class 3 result. This satisfies the §22 obligation in full: every one of the thirteen required-verbatim blocks is re-emitted by section reference, character-exactly, with no paraphrase, while the operative class remains unambiguously Class 3.

## 4. Primary result

| Quantity | Value |
| --- | --- |
| `verdict_class` | `No neighborhood evidence` |
| `verdict_class_machine` | `class_3` |
| `pathology` | `None` |

**Focal-elevation gate (k = 12), design memo §11**

| Field | Value |
| --- | --- |
| `pass` | `False` |
| `median_12` | `0.034445901350758625` |
| `neighbor_mean` | `0.03467440484746646` |
| `focal_excess` | `-0.00022850349670783254` |
| `ambiguous` | `False` |

**Attenuation scores (per focal), design memo §10**

| Focal | `attenuation_score` |
| --- | --- |
| 10 | `0.00015882650282547683` |
| 12 | `0.00003223099773091763` |
| 14 | `0.000520914577591333` |
| 16 | `0.0001156762544218018` |

**max_gap contrast, design memo §12**

| Field | Value |
| --- | --- |
| observed `max_gap` | `-0.0004886835798604154` |
| `strongest_control_focal` | `14` |
| `strongest_control_score` | `0.000520914577591333` |
| `score_12` | `0.00003223099773091763` |

**Primary beat counts (threshold 9,500 / 10,000, strict `<`), design memo §14**

| Beat count | Value | Threshold | Pass |
| --- | --- | --- | --- |
| `beat_count_12_structure` | 5979 | ≥ 9500 | ✗ |
| `beat_count_max_gap` | 704 | ≥ 9500 | ✗ |

`threshold_pass = { beat_count_12_structure: False, beat_count_max_gap: False }`.

Decision rule satisfied (design memo §15.3): `focal_elevation_gate_12` **fails** **OR** `beat_count_12_structure < 9500`. Both disjuncts hold: the gate fails (`focal_excess` is negative) and `beat_count_12_structure = 5979 < 9500`. Verdict class: **No neighborhood evidence (Class 3)**. Class 4 was not entered: `pathology = None`, the gate is not `ambiguous`, and the §17 provenance gate passed — a near-threshold beat count below 9,500 is a fail routed to Class 3, never the pathology class (design memo §15.4, §21.7).

### 4.1 Precise interpretation (scoped to the locked decision rules)

* The focal-elevation gate fails: `median_12` (`0.03444…`) is **below** the arithmetic mean of its six non-focal window neighbors `{9,10,11,13,14,15}` (`0.03467…`). 12 is not even a local elevation on this substrate under the locked operationalization, let alone a structured peak.
* `attenuation_score_12 = 3.22e-05` is the **weakest** of the four focal attenuation scores; focal 14 (`5.21e-04`) is the strongest. Consequently `max_gap = score_12 − max(score_10, score_14, score_16) = −4.89e-04` is negative: 12's neighborhood attenuation does not exceed, and is in fact below, the strongest control focal's.
* `beat_count_12_structure = 5979/10000`: the observed 12-neighborhood attenuation is not distinguished from the pooled-permutation null at the locked 9,500 threshold. `beat_count_max_gap = 704/10000` likewise fails. Per the §15.6 coupled-null disclosure re-emitted above, these are pre-registered decision rules under one joint distribution, not independent p-values.

## 5. Diagnostic texture (non-verdict)

Per design memo §16 and §21.5, the following are reported but cannot rescue, upgrade, alter, or convert anything into 12-centered structure. A Class 3 verdict remains Class 3 regardless of diagnostic pattern.

### 5.1 Asset-stratified diagnostic

`run_asset_stratified_diagnostic` (design memo §16) under within-asset `is_long` shuffles (`ASSET_STRAT_DIAG_SEED_CELL1 = 20260519`, `N_PERM = 10,000`):

| Asset-stratified beat count | Value |
| --- | --- |
| `asset_stratified_beat_count_12_structure` | 6018 |
| `asset_stratified_beat_count_max_gap` | 739 |

The stratified pattern mirrors the primary closely (6018 vs 5979 for the 12-structure beat count; 739 vs 704 for max_gap). This is texture consistent with the primary null being a property of the pooled phase-allocation structure rather than an artifact of asset-composition reshuffling. Per §16 / §21.5 it does not rescue, alter, or upgrade the Class 3 verdict.

### 5.2 §17 provenance check (validity gate)

| Quantity | Value |
| --- | --- |
| `pass` | `True` |
| `max_abs_diff_10` | `0.0` |
| `max_abs_diff_12` | `0.0` |
| `n_anchors_checked_10` | 365 |
| `n_anchors_checked_12` | 365 |
| `tolerance` | `1e-12` |

Cell 1's recomputed `k = 10` and `k = 12` 365-anchor PSS surfaces are bit-identical to Candidate C's stored `protocol_payload.pss_surface_10` / `pss_surface_12` — maximum absolute per-anchor difference exactly `0.0`, strictly within the `≤ 1e-12` tolerance, at floating-point equality. The Class 3 result is therefore **not** implementation drift relative to Candidate C's locked surfaces on the shared bucket counts; the lens/PSS fork is mathematically identical to Candidate C's locked computation. The rerun gate confirmed byte-identical double invocation (`rerun_verification_digest = 50f2357d…`, matching the verdict-log filename tag).

## 6. What was found (within the locked scope)

Under the locked decision rules, on the frozen pullback × pooled Phase 3b 1,282-trade substrate:

* `k = 12` does **not** sit on a local elevation: its median PSS is below the mean of its six non-focal `±3` window neighbors (`focal_excess = −0.00022850349670783254`).
* The 12-neighborhood attenuation is not distinguished from the pooled-permutation null (`beat_count_12_structure = 5979/10000`), and it is below the strongest control focal's attenuation (`max_gap = −0.0004886835798604154`, strongest control focal 14).
* The result is a clean Class 3 (`pathology = None`), survives within-asset stratification (asset-stratified diagnostic mirrors the primary), and rests on a computation bit-identical to Candidate C's stored k=10/k=12 surfaces (§17 provenance exact).

Per the verbatim §15.3a re-emitted above: 12, on the neighborhood operationalization, behaves as an isolated point rather than a structured local peak.

## 7. What was not found

Per the verbatim §15.3b and §21.4 re-emitted above, and the §15.5 granularity caveat:

* This null does **not** weaken Candidate C's `12-privileged` verdict. Cell 1 asked a different question; "12 beat 10 under Candidate C's locked rules" stands exactly as Candidate C closed it (`1659819`). Candidate C independence is preserved.
* This null does **not** say the substrate is structureless. It is scope-bounded to the locked `±3` linear-integer neighborhood operationalization evaluated as the median of each bucket count's 365-anchor PSS surface — a statement about how phase-allocation structure varies with bucket-count resolution near the focal, not about absolute structure or which bucket count is "correct."
* This null does **not** test, and says nothing about, divisor, multiple, 12-family/duodecimal, harmonic-family, recursive-field, or weighted-neighbor influence. Those are Layer 2, out of scope for Cell 1, and the Kryon source does not authorize them.
* This null does **not** bear on Candidate B. Candidate B's split-null equinox result remains **not confirmed** and is neither rescued, confirmed, nor reinterpreted by Cell 1.
* The source boundary holds: Kryon's direct framing ("four is not a four"; three and five as the linear neighbors of four) supports linear-neighborhood influence only. Cell 1 operationalized exactly that source-faithful Layer 1 and found no neighborhood structure around 12 on this substrate; the choice of 12 as primary focal was the Candidate-C-inherited, researcher-side selection, never a source claim.

## 8. Program posture

Influential Numbers Cell 1 joins the Coherent Numbers audit chain as a closed cell on the pullback × pooled-Phase-3b substrate family:

* SPY MVT closure (`371ca9c`): null/null.
* GLD closure: null/null.
* Candidate B closure (`df09aa8`): Split-null.
* Candidate C closure (`1659819`): 12-privileged.
* Influential Numbers Cell 1 closure (this artifact): No neighborhood evidence (Class 3).

The posture is constrained curiosity, not rescue. Cell 1 adds one atlas tile: under a source-faithful linear-neighborhood operationalization, 12 does not sit in a structured local neighborhood on this substrate. This is fully compatible with Candidate C's separate finding that 12 out-organized 10 under its own binary rules — the two are independent questions and the program treats them as such. A Layer 1 null does not make Layer 2 a follow-up by default; per the verbatim §21.3, any Layer 2 consideration requires a separate decision memo justified on its own scientific grounds, and is never an escape hatch from this Class 3 result. The locked no-rescue and anti-rescue clauses apply through this closure: no diagnostic promotes the verdict, and Cell 1 neither softens its own Class 3 nor reinterprets any prior cell.

## 9. Open questions not answered by Cell 1

Each item below is explicitly out of scope for this cell and would require its own separate decision memo and audit chain if pursued. None of these softens or reopens the Class 3 verdict.

* Whether any Layer 2 operationalization (divisor, multiple, 12-family/duodecimal, harmonic-family, recursive-field, weighted-neighbor) carries structure on this substrate. This is not motivated by Cell 1's null and, per the verbatim §21.3, requires a separate decision memo argued on its own grounds — not as a rescue of Layer 1.
* Whether a different focal structure, window width, substrate, or anchor scheme would behave differently. The locked design fixed these pre-outcome; any alternative is a new pre-registered cell, not a re-run or amendment of Cell 1.
* Whether the negative `focal_excess` and weak `attenuation_score_12` reflect a substrate property, an annual-rhythm artifact, or the bucket-count-resolution dependence flagged in the verbatim §15.5 caveat. The locked design does not adjudicate this.
* The broader Influential Numbers umbrella (the framework memo `8ff619c` reserved later cells) is neither answered nor foreclosed by Cell 1; any successor cell is a separate framework/design/lock/run/closure chain.

## 10. Closure statement

Influential Numbers Cell 1 — the Neighborhood Influence Test — is closed as **No neighborhood evidence (Class 3)**. On the frozen pullback × pooled Phase 3b 1,282-trade substrate, under the locked design memo `a765098`, the focal-elevation gate for `k = 12` fails (`median_12 = 0.034445901350758625` below neighbor mean `0.03467440484746646`; `focal_excess = -0.00022850349670783254`; `ambiguous = False`) and `beat_count_12_structure = 5979 < 9500`; `pathology = None`. Per the verbatim §15.3a/b, §15.5, §15.6, §20, §21.3, and §21.4 re-emitted in §3 of this memo and recorded in the verdict log, the verdict establishes that 12 behaves as an isolated point rather than a structured local peak under the source-faithful linear-neighborhood operationalization; it does not weaken Candidate C's `12-privileged` verdict, does not say the substrate is structureless, does not test or motivate any Layer 2 extension, does not rescue or reinterpret Candidate B's not-confirmed split-null, and is scope-bounded to the locked neighborhood operationalization. The §17 provenance gate passed at floating-point equality, confirming the result is not implementation drift relative to Candidate C's locked k=10/k=12 surfaces. The next artifact in the audit chain, if any successor cell is pursued, is a separate framework/design/lock chain — not an amendment, re-run, or Layer 2 rescue of Cell 1.

— end of closure memo —
