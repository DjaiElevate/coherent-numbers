# Influential Numbers Program — Cell 1 Design Memo (Neighborhood Influence Test)

Version: v0.1 (lock-candidate draft; expanded from the Cell 1 framework memo at commit `8ff619c`)
Date: 2026-05-15
Project: Coherent Numbers
Program: Influential Numbers
Cell: Cell 1 — Neighborhood Influence Test
Status: Pre-registration draft. Protocol not yet locked. No analysis authorized. No neighborhood-surface features have been computed against pullback `entry_date` under this design. This memo is a clean review draft only; the repo file is not created and nothing is lock-accepted.

---

## 1. Title and version

Influential Numbers Program — Cell 1: Neighborhood Influence Test. Design memo v0.1, lock-candidate draft. This memo formalizes the seven resolved locks named in the request into a single pre-registration design surface. It does not lock them; lock-acceptance is a separate, later artifact.

Possible eventual repo path: `docs/influential_numbers_cell_1_design_memo_v0.1.md`. Provisional only.

## 2. Purpose

This memo proposes the locked protocol for Cell 1 of the Influential Numbers program, whose primary question is:

> On the frozen pullback × pooled Phase 3b substrate, does the bucket-count `k = 12` sit inside a structured local neighborhood — a focal-centered attenuation of phase-allocation structure as `|k − 12|` increases — that is distinguished both from chance and from the analogous local structure around control focals `10`, `14`, and `16`?

This is a neighborhood-structure question, not a winner question. Candidate C already asked and answered "does 12 beat 10?" under its own locked binary rules. Cell 1 asks the orthogonal question "is 12 a structured local peak rather than an isolated point?" The cell stays narrow on purpose: it tests Layer 1 (linear-neighborhood influence) only, the single operationalization the Kryon source directly supports.

This memo formalizes the framework memo's narrowing (commit `8ff619c`) into seven locks:

1. **Substrate** — frozen pullback × pooled Phase 3b, 1,282 trades, 2005–2022 (§5).
2. **Focal structure** — multi-focal `F = {10, 12, 14, 16}`, primary `12`, controls `10, 14, 16` (§8).
3. **Window** — `±3` linear-integer window per focal; bucket-count universe `K = {7, …, 19}` (§8).
4. **Structure definition** — focal-centered continuous attenuation, with a required focal-elevation gate (§10, §11).
5. **Control / comparison design** — `max_gap` contrast against control focals, 10,000 shared label permutations (§12, §13).
6. **Implementation/statistic specifics** — hard-binary Class 4, seeds, asset-stratified diagnostic, provenance check, verdict map (§14–§18).
7. **Infrastructure** — result-defining surface/lens/PSS code forked into a Cell 1 namespace; generic loaders inherited (§19).

## 3. Source boundary and relationship to framework memo

The framework memo (commit `8ff619c`, `docs/influential_numbers_cell_1_framework_memo_v0.1.md`) is the controlling conceptual document. Its boundaries are inherited verbatim and are not re-opened here:

* The Kryon source ("Needed Science for the Times," *"The New Math is coming"*; "four is not a four," with five and three as the named linear neighbors of four) supports **linear-neighborhood influence only**. This is Layer 1.
* The Kryon source does **not** predict 12, does not single out any focal number, does not state divisor/multiple influence, and does not state 12-family, harmonic-family, recursive-field, or weighted-neighbor structure. Those are Layer 2 and are out of scope for this cell.
* The choice of 12 as the primary focal is inherited from Candidate C's result, not from the source. This memo names that explicitly and never lets Candidate C's outcome become a source claim.
* Layer 2 cannot rescue Layer 1. If Cell 1 returns no neighborhood evidence, Layer 2 is not authorized by this cell; any Layer 2 follow-up requires its own separate decision memo, argued on its own grounds.

The framework memo left substrate, focal structure, window, the definition of "structure," the control design, the statistic/null/threshold, and the verdict map open as design-memo locks. This memo closes exactly those, and nothing else.

## 4. Relationship to Candidate C and Candidate B

**Candidate C.** Candidate C closed `12-privileged` (closure commit `1659819`): under its locked binary rules, `k = 12` out-organized `k = 10` on this substrate (`beat_count_comparison_12 = 9973/10000`, both individual nulls `10000/10000`). Cell 1's relationship to that result is strictly additive and strictly independent:

* A Cell 1 *no-neighborhood-evidence* verdict does **not** weaken Candidate C. Candidate C's claim is fully contained in its own locked binary comparison.
* A Cell 1 *12-centered neighborhood structure* verdict does **not** retroactively reinterpret Candidate C. It does not convert "12 beat 10" into "12 is the centre of a base-12 structure," and it does not establish duodecimal mathematics.
* Candidate C remains exactly: *12 beat 10 under its locked decision rules.* Cell 1 adds a separate atlas tile about the *shape of the surface around 12*, not a re-litigation of C.

Candidate C also serves three concrete roles here: (i) the motivation for selecting 12 as the primary focal (named as researcher-side, not source-side); (ii) the mathematical family Cell 1 inherits (η²-form PSS, 365-DOY anchor surface, median-over-surface primary statistic); and (iii) the **provenance anchor** for the §17 validity gate, via Candidate C's stored `k = 10` and `k = 12` 365-anchor surfaces.

**Candidate B.** Candidate B closed `Split-null` on its pre-registered equinox question on the same substrate. That verdict stands on its own. Cell 1 tests a different question and **does not confirm, rescue, or reinterpret** Candidate B. A positive Cell 1 verdict does not convert Candidate B's split-null into a confirmed equinox result. This is a required-verbatim anti-rescue clause (§21.4).

## 5. Population / substrate

Primary (confirmatory): the pooled Phase 3b 5-asset population — SPY, EFA, EEM, GLD, TLT — 1,282 trades total, produced under identical pullback `BacktestParams` at pullback commit `7806a6d` over the common window 2005-01-01 – 2022-12-31. Source manifest: `docs/pullback_population_freeze_manifest_v0.1.md` at freeze commit `5225bfd`. This is the identical population analyzed by Candidate B and Candidate C; no new freeze is required and none is authorized.

Per-asset Phase 3b row counts inherited from the freeze manifest: SPY 243, EFA 283, EEM 261, GLD 253, TLT 242 (sum = 1,282).

No secondary population is in scope. The SPY 301-trade base population is not used. OOS 2023+ remains sealed in both repos and is out of scope for Cell 1. The pullback repo is not touched at design, lock, or run time. Inherited data contact is disclosed in §20 (required-verbatim).

This substrate is the framework memo's named conservative default: already frozen, already audited, already characterised (including its known phase-allocation structure under both `k = 12` and `k = 10` from Candidate C). Selecting it avoids introducing a new substrate before the neighborhood concept is operationalized. The selection is a deliberate framework-level decision, now locked here.

## 6. Reduced row schema

The reduced analytical row schema is inherited verbatim from Candidate B §5 / Candidate C §5. Each analytical row corresponds to one frozen pullback trade with:

* `trade_id` — stable identifier within the frozen artifact.
* `asset` — one of `{SPY, EFA, EEM, GLD, TLT}`.
* `entry_date` — primary phase-assignment date (calendar-day granularity, exchange tz of the frozen artifact).
* `exit_date`.
* `is_long` — boolean direction label (the only permuted quantity in all nulls).
* `r_multiple` — signed trade outcome as recorded in the frozen artifact; not used in Cell 1's primary outcome.
* `frozen_artifact_id` — pointer to the manifest entry for this trade's source CSV.

No new columns are added by Cell 1. `source_sha256` remains dataset-level provenance from the freeze manifest, not a per-row analytical field. Schema reconciliation across the SPY 21-column long-form and the Phase 3b 11-column compact schemas is inherited from Candidate B unchanged and not re-opened.

## 7. Calendar / bucket-count lens

Cell 1 inherits Candidate C's parameterized annual-sector lens family, generalized over a wider bucket-count set. For a trade with `entry_date` and bucket count `k`:

### 7.1 Parameterized phase assignment (civil-date anchor)

1. Locate the annual cycle (candidate anchor: March 20, i.e. `anchor_month = 3`, `anchor_day = 20`, inherited from Candidate C `locked_parameters`).
   * If `entry_date >= date(entry_date.year, 3, 20)`: `cycle_start = date(entry_date.year, 3, 20)`; else `cycle_start = date(entry_date.year - 1, 3, 20)`.
   * `cycle_end = date(cycle_start.year + 1, 3, 20)`.
2. `cycle_length_days = (cycle_end - cycle_start).days` (365 or 366); `days_since_start = (entry_date - cycle_start).days`.
3. `phase = floor(days_since_start * k / cycle_length_days)`. Assert `phase ∈ {0, …, k-1}`; abort on assertion failure. No silent clamp. No `%` operator anywhere in Cell 1 lens code (grep gate test required, parallel to Candidate B/C).

### 7.2 Anchor-shifted form (365-DOY surface)

For integer DOY anchor `d ∈ 1..365` and bucket count `k`: `anchor_in_year(y) = date(y,1,1) + timedelta(d-1)`; cycle structure as §7.1 with March 20 replaced by `anchor_in_year(·)` consistently; `phase_d = floor(days_since_start_d * k / cycle_length_days_d)`; assert `phase_d ∈ {0, …, k-1}`; abort on failure.

### 7.3 Inherited conventions

Anchor enumeration covers integer DOYs `1..365` exhaustively, no sampling, no seed consumed (inherits the v0.3.3 finite-control discipline). In leap years, DOY 60 coincides with Feb 29 and DOY 79 lands on March 19 (civil March 20 = DOY 80 in leap years). These are the inherited Candidate B/C conventions, retained unchanged for the §17 provenance check to be exact. The lens is deterministic given (`entry_date`, `k`, `d`). `entry_date` is the only phase-assignment date; `exit_date` is not used.

## 8. Focal centers and windows

**Lock 2 — focal structure (multi-focal).**

* Focal centers: `F = {10, 12, 14, 16}`.
* Primary focal: `12`.
* Control focals: `10, 14, 16`.

The design is deliberately multi-focal. A single-focal "12 looks structured" result is uninterpretable without knowing whether *every* focal on this substrate looks locally structured. The control focals exist to separate a 12-specific neighborhood effect from generic substrate smoothness. The choice of 12 as primary is the Candidate-C-inherited, researcher-side selection of §3/§4, not a source claim.

**Lock 3 — window (`±3` linear-integer).**

`W(f) = {f−3, f−2, f−1, f, f+1, f+2, f+3}` (seven integer bucket counts per focal):

* `W(10) = {7, 8, 9, 10, 11, 12, 13}`
* `W(12) = {9, 10, 11, 12, 13, 14, 15}`
* `W(14) = {11, 12, 13, 14, 15, 16, 17}`
* `W(16) = {13, 14, 15, 16, 17, 18, 19}`

Total bucket-count universe: `K = {7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}` (13 distinct bucket counts). Every PSS surface used anywhere in Cell 1 is computed over `K`.

"Neighborhood" means a linear-integer window only. No divisor, multiple, factor, harmonic, or duodecimal-family relation enters Cell 1; those are Layer 2 and forbidden here (§21). Non-focal neighbors used by the focal-elevation gate (§11) are all `k ∈ W(f)` except `f` itself, **even when those `k` are focal centers in their own windows** (e.g. `k = 12 ∈ W(10)` counts as a non-focal neighbor of focal `10`). The focal `k = f` is included in the slope regression (§10).

## 9. PSS surface definition

Cell 1 inherits Candidate C's η²/correlation-ratio PSS, parameterized by `k`, generalized over `K = {7, …, 19}`.

### 9.1 Per-bucket-count PSS at a single anchor

For bucket count `k` and a fixed anchor configuration, let `N_p`, `L_p` be per-phase trade and long counts, `N_total = Σ_p N_p`, `share_pooled = (Σ_p L_p)/N_total`, `share_p = L_p/N_p` for `N_p > 0`; phases with `N_p = 0` contribute 0 to `between_k`.

```text
between_k = Σ_p (N_p / N_total) × (share_p − share_pooled)^2
total_k   = share_pooled × (1 − share_pooled)
PSS_k     = between_k / total_k
```

η²-form, bounded `[0,1]` when `total_k > 0`. If `total_k = 0` (all-long or all-short pool), raise `DegenerateLongShareError` and abort. No fallback.

### 9.2 Per-bucket-count surface and median statistic

For each `k ∈ K`, the 365-anchor surface is `PSS_surface_k = { PSS_k(d) : d ∈ 1..365 }` using the §7.2 anchor-shifted formula. The per-bucket-count primary statistic is the anchor-neutral median:

```text
median_k = median(PSS_surface_k)
```

(odd `N = 365`, the 183rd order statistic; no interpolation ambiguity). `median_k` is the single number used as "the PSS of bucket count `k`" everywhere downstream (the attenuation regression of §10, the gate of §11, the contrast of §12, and every permutation draw of §13). This makes the entire cell anchor-neutral, exactly as Candidate C's median absorbed the anchor surface.

## 10. Neighborhood structure statistic

**Lock 4 — primary structure measure: focal-centered continuous attenuation.**

For each focal `f ∈ F`:

1. Compute `median_k` (§9.2) for every `k ∈ W(f)` — seven values.
2. Define per-point distance `distance_k = |k − f|`. Over the seven window points the distance multiset is exactly `{0, 1, 1, 2, 2, 3, 3}` (the focal contributes the single `0`).
3. Ordinary-least-squares regression of `median_k` on `distance_k` using all seven points:
   `slope_f = OLS_slope( median_k ~ |k − f| )`.
4. Define the attenuation score:
   `attenuation_score_f = − slope_f`.

A higher positive `attenuation_score_f` means PSS attenuates more steeply as bucket count moves away from the focal — i.e. the focal sits on a structured local peak. The focal `k = f` is included as the `distance = 0` point in the regression (per Lock 3).

Strict monotonic attenuation (a check that `median_k` is non-increasing in `|k − f|` step by step on each side) is a **secondary diagnostic only** (§16). It cannot drive, alter, upgrade, or rescue any verdict.

## 11. Focal-elevation gate

A required gate, evaluated for the primary focal `12` only, prior to verdict assignment:

```text
focal_elevation_gate_12 :=  median_12  >  mean({ median_k : k ∈ W(12), k ≠ 12 })
```

i.e. the focal's own median PSS must strictly exceed the arithmetic mean of its six non-focal window neighbors `{9, 10, 11, 13, 14, 15}`. The gate is strict `>`. The gate ensures attenuation is measured around an actual local elevation, not around a focal that is itself a trough with a coincidentally negative slope.

Exact numerical ambiguity in the gate (a tie at floating-point equality, or a non-finite `median_k` entering the gate) is a Class 4 design-validity pathology (§14), not a pass and not a fail-by-default-to-Class-3 — it is explicitly routed to Class 4 per §15.

## 12. Control contrast: max-gap

**Lock 5 — primary contrast.**

```text
max_gap_observed = attenuation_score_12
                 − max( attenuation_score_10, attenuation_score_14, attenuation_score_16 )
```

`max_gap` asks whether 12's neighborhood attenuation exceeds the *strongest* attenuation found at any control focal. Using `max(·)` over the three controls (rather than a mean) is the conservative choice: 12 must beat the best-looking control, not merely the average control, before any 12-specific structure is claimed. This is the design's guard against generic substrate smoothness — if the substrate produces smooth local peaks around many bucket counts, some control focal will exhibit comparable attenuation and `max_gap` will not separate.

## 13. Null hypotheses and finite controls

The primary null is a single shared pool of `N_PERM = 10,000` pooled-population permutations of `is_long`. Phase labels and asset labels are held fixed; only `is_long` is permuted; no asset stratification in the primary pool.

Locked seed: `LABEL_PERM_SEED_CELL1 = 20260518` (distinct from Candidate B's `20260514`/`20260515` and Candidate C's `20260516`/`20260517`, so Cell 1's permutation sequence is not a sub-sample of any prior cell's). A single `numpy.random.Generator(numpy.random.PCG64(LABEL_PERM_SEED_CELL1))` instance.

For each permutation `i ∈ 1..10000`:

1. Draw a uniform unstratified pooled shuffle of `is_long` over all 1,282 trades.
2. Recompute the full median-PSS map `{ median_k : k ∈ K = {7,…,19} }` on the permuted labels (each `median_k` is itself the median of that bucket count's 365-anchor surface, §9.2).
3. Recompute `attenuation_score_f` (§10) for every focal `f ∈ {10, 12, 14, 16}`.
4. Compute `max_gap_perm[i] = attenuation_score_12_perm[i] − max(attenuation_score_10_perm[i], attenuation_score_14_perm[i], attenuation_score_16_perm[i])`.

This is exhaustive over the 365-DOY anchor surface inside every permutation draw (no anchor sampling); the only randomness is the `is_long` shuffle. The 365-anchor enumeration appears inside both the observed statistic and every permutation draw.

## 14. Beat counts and thresholds

Two primary beat counts, both strict `<`, ties do not pass:

```text
beat_count_12_structure = #{ i : attenuation_score_12_perm[i] < attenuation_score_12_observed }
beat_count_max_gap      = #{ i : max_gap_perm[i]               < max_gap_observed }
```

Locked threshold: `9500 / 10000`, strict. `beat_count ≥ 9500` = pass; `beat_count < 9500` = fail.

**Class 4 is a hard binary with no marginal band.** A near-threshold value below 9,500 (e.g. 9,499) is a **fail**, not "unresolved." Class 4 is reserved exclusively for pathology / design-validity failures enumerated in §15 — it is never a near-threshold escape hatch.

All beat counts (primary and the §16 diagnostic counterparts) are emitted to the verdict log unconditionally, regardless of verdict class.

## 15. Verdict map and interpretations

Four mutually exclusive, collectively exhaustive classes. Display names are exact and must appear character-identical in the verdict log; machine labels are as given.

| Class | Display name | Machine label |
|---|---|---|
| 1 | `12-centered neighborhood structure` | `class_1` |
| 2 | `Generic substrate smoothness` | `class_2` |
| 3 | `No neighborhood evidence` | `class_3` |
| 4 | `Non-confirmatory / unresolved` | `class_4` |

### 15.1 Class 1 — 12-centered neighborhood structure

Decision rule: `focal_elevation_gate_12` passes **AND** `beat_count_12_structure ≥ 9500` **AND** `beat_count_max_gap ≥ 9500`.

> **(a) What it supports** *(REQUIRED-VERBATIM, §15.1a):* Under the locked decision rules, the bucket count `k = 12` sits on a focal-centered local elevation whose attenuation away from 12 is distinguished from chance, and that attenuation exceeds the strongest attenuation at any of the control focals `10`, `14`, `16` on this substrate. The 12-neighborhood behaves as a structured local peak rather than an isolated point under the locked protocol.
>
> **(b) What it does not support** *(REQUIRED-VERBATIM, §15.1b):* The verdict does not establish that 12 is uniquely neighborhood-structured among all bucket counts (only `10, 14, 16` were used as controls); it does not attribute the structure to a duodecimal, divisor, multiple, harmonic, or 12-family property (those are Layer 2 and untested here); it does not establish base-12 mathematics; it does not retroactively reinterpret Candidate C's `12-privileged` verdict, which remains exactly "12 beat 10 under its locked rules"; it does not confirm or rescue Candidate B's split-null equinox result; and it does not generalize beyond the pre-registered substrate, window, or focal set.

### 15.2 Class 2 — Generic substrate smoothness

Decision rule: `focal_elevation_gate_12` passes **AND** `beat_count_12_structure ≥ 9500` **AND** `beat_count_max_gap < 9500`.

> **(a) What it supports** *(REQUIRED-VERBATIM, §15.2a):* Under the locked decision rules, the 12-neighborhood shows attenuation distinguished from chance, but that attenuation is **not** distinguished from the attenuation at the strongest control focal. The substrate appears to produce locally smooth neighborhoods around multiple bucket centers; 12's local structure is consistent with that generic smoothness rather than being 12-specific.
>
> **(b) What it does not support** *(REQUIRED-VERBATIM, §15.2b):* The verdict does not say 12 is unstructured, and it does not say the substrate is structureless; it specifically does not support a 12-specific neighborhood claim; it does not weaken Candidate C (a generic-smoothness reading of the neighborhood is independent of C's binary 12-vs-10 result); and it does not motivate Layer 2 extension as a rescue.

### 15.3 Class 3 — No neighborhood evidence

Decision rule: `focal_elevation_gate_12` **fails** **OR** `beat_count_12_structure < 9500`.

> **(a) What it supports** *(REQUIRED-VERBATIM, §15.3a):* Under the locked decision rules, there is no evidence that 12 sits inside a structured local neighborhood on this substrate: either 12's median PSS does not exceed its non-focal window neighbors, or the 12-neighborhood attenuation is not distinguished from chance. 12, on the neighborhood operationalization, behaves as an isolated point rather than a structured local peak.
>
> **(b) What it does not support** *(REQUIRED-VERBATIM, §15.3b):* This null does not weaken Candidate C's `12-privileged` verdict — Cell 1 asks a different question and a no-neighborhood result leaves "12 beat 10 under C's locked rules" untouched. It does not say the substrate is structureless. It does not motivate or authorize Layer 2 (divisor, multiple, harmonic, 12-family, recursive, weighted) as a rescue; per §3 and §21, Layer 2 on a Layer 1 null requires a separate decision memo argued on its own grounds. It does not bear on Candidate B.

### 15.4 Class 4 — Non-confirmatory / unresolved

Decision rule: pathology / design-validity failure only — never a near-threshold escape hatch. A `beat_count` below 9,500 (however close) is a fail routed to Class 3, not Class 4. Class 4 is entered **only** for:

* non-finite values anywhere in a `median_k`, slope, attenuation score, or `max_gap`;
* degenerate variance (`total_k = 0` → `DegenerateLongShareError`, or a zero-variance distance regressor — structurally impossible under a fixed `±3` window but checked);
* a missing focal surface (any `k ∈ K` whose 365-anchor surface cannot be computed);
* provenance-check failure (§17);
* implementation-validity failure (rerun-gate mismatch, §18);
* exact numerical ambiguity in the focal-elevation gate (a floating-point tie in §11, or a non-finite value entering the gate).

> **(a) What it supports** *(REQUIRED-VERBATIM, §15.4a):* Under the locked decision rules, the result does not support any of Class 1, 2, or 3. A design-validity or pathology condition prevented a valid neighborhood adjudication. Beat counts, if computed, are reported as diagnostic texture only and do not upgrade the verdict.
>
> **(b) What it does not support** *(REQUIRED-VERBATIM, §15.4b):* This class does not say the substrate is structureless, does not adjudicate the neighborhood question, does not rescue or weaken Candidate C or Candidate B, and does not authorize amending the locked design after the fact.

### 15.5 Required granularity / neighborhood-window caveat

> *(REQUIRED-VERBATIM, §15.5):* Every Cell 1 verdict is scope-bounded by the locked neighborhood operationalization. "Neighborhood" here means a `±3` linear-integer window of bucket counts evaluated as the median of each bucket count's 365-anchor PSS surface; different bucket counts correspond to different temporal resolutions (e.g. `k = 12` ≈ 30.4 days/phase, `k = 16` ≈ 22.8 days/phase, `k = 7` ≈ 52 days/phase). A neighborhood verdict reflects how phase-allocation structure varies with bucket-count resolution near the focal, not a claim that any bucket count is structurally "correct," and not a test of divisor/multiple/harmonic/12-family structure. This caveat applies to all four verdict classes.

### 15.6 Compound-verdict / coupled-null disclosure

> *(REQUIRED-VERBATIM, §15.6):* The two primary beat counts (`beat_count_12_structure`, `beat_count_max_gap`) are coupled: both are derived from the same shared pool of 10,000 pooled-population `is_long` permutations, and the per-permutation attenuation scores entering both are functions of the same recomputed `K`-wide median-PSS map. The verdict classes are pre-registered decision rules under that joint distribution, not independent p-value claims. The false-positive interpretation of a class assignment is not identical to the false-positive rate of a single independent test at the 95th percentile, and the four classes do not partition probability mass uniformly under the null.

## 16. Diagnostics

All diagnostics are non-confirmatory. They cannot rescue, upgrade, alter, or convert generic smoothness into 12-centered structure.

* **Asset-stratified label-permutation diagnostic.** Mirrors Candidate C §11.3. Permute `is_long` *within each asset's index slice*, recompute the full `K`-wide median-PSS map, the four focal attenuation scores, and `max_gap`. Locked seed `ASSET_STRAT_DIAG_SEED_CELL1 = 20260519`. `N_PERM = 10000` (the same count as the primary pool; a smaller diagnostic permutation count is **not** permitted unless explicitly pre-registered in this memo, and it is not). Produces `asset_stratified_beat_count_12_structure` and `asset_stratified_beat_count_max_gap`. Diagnostic only.
* **Strict monotonic attenuation** per focal (§10): per-side step-wise non-increase of `median_k` in `|k − f|`. Secondary diagnostic only.
* **Per-focal attenuation scores and window surfaces** for all four focals (`median_k` for every `k ∈ K`, the four slopes, the four scores, `max_gap`). Texture.
* **Control-focal beat counts** (`attenuation_score_10/14/16` vs their own permutation distributions) reported for interpretability of `max_gap`. Diagnostic only; not verdict inputs.

Per §21 no-rescue, a Class 3 or Class 4 verdict remains so regardless of diagnostic pattern, including a diagnostic that looks like clean 12-centered attenuation.

## 17. Provenance checks

Cell 1 recomputes the 365-anchor PSS surfaces for every `k ∈ K = {7, …, 19}`. Because `k = 10` and `k = 12` are members of `K`, Cell 1's recomputed `pss_surface_10` and `pss_surface_12` must reproduce Candidate C's stored surfaces to floating-point precision.

* Stored reference: `protocol_payload.pss_surface_10` and `protocol_payload.pss_surface_12` in `results/candidate_c_results_20260515_051236_f3a6bf48.json` (locked verdict run, commit `a19b2e9`; JSON SHA-256 `130235fef110cca141fa8873bfa3a6c630a44ac11dfcad953822f41f9cd3c7d4`). Keys are stringified integer DOYs `"1"`…`"365"`; Cell 1 compares its anchor `d` to Candidate C key `str(d)`.
* Tolerance: `max_abs_diff ≤ 1e-12` per anchor, for **each** of `k = 10` and `k = 12` independently across all 365 anchors.
* If either `k = 10` or `k = 12` exceeds tolerance, the run **aborts** and the verdict is Class 4. This is a **validity gate, not a diagnostic** — it gates whether Cell 1's lens/PSS fork is mathematically identical to Candidate C's locked computation on the shared bucket counts.

Frozen-data provenance is otherwise the freeze manifest at `5225bfd`, with the inherited triple SHA-256 re-verification of every referenced CSV (run start, after reduced-view construction, between the two rerun-gate protocol invocations). The pullback repo HEAD is not consulted at run time.

## 18. Reproducibility requirements and seeds

* All randomness resides in §13 (primary, `LABEL_PERM_SEED_CELL1 = 20260518`) and §16 (asset-stratified diagnostic, `ASSET_STRAT_DIAG_SEED_CELL1 = 20260519`). Independent PCG64 instances. Both pools use `N_PERM = 10000`.
* The 365-DOY anchor sweep is deterministic and exhaustive; no seed consumed.
* §7 phase assignment is deterministic given parameters.
* Frozen-CSV provenance verified three times per run (§17).
* A deterministic rerun gate invokes the protocol twice, canonicalizes the protocol payload (numeric results, beat counts, verdict class, verbalization — header metadata excluded), SHA-256-compares, and aborts on mismatch; the matched digest becomes `rerun_verification_digest` in the verdict-log header. Rerun-gate mismatch is a Class 4 implementation-validity failure (§15.4).
* A clean run from a clean checkout at the eventual lock commit must reproduce the two primary beat counts, the two diagnostic beat counts, the verdict class, and the rerun digest bit-for-bit.

## 19. Infrastructure and implementation boundary

Cell 1 inherits the *mathematical family* from Candidate C but freezes all *result-defining code* in Cell 1-specific modules. Candidate C's stored `k = 10` / `k = 12` surfaces are an audit-chain provenance check (§17), **not** a live runtime dependency.

Future implementation modules (not created by this memo):

* `src/influential_numbers_cell_1_lens.py`
* `src/influential_numbers_cell_1_pss.py`
* `src/influential_numbers_cell_1_protocol.py`
* `scripts/run_influential_numbers_cell_1_protocol.py`

Future tests (not created by this memo):

* `tests/test_influential_numbers_cell_1_lens.py`
* `tests/test_influential_numbers_cell_1_pss.py`
* `tests/test_influential_numbers_cell_1_protocol.py`

Generic locked infrastructure continues to be imported unchanged: `candidate_b_loader` (frozen-CSV load + manifest verification) and `candidate_b_rerun_gate` (deterministic double-invocation gate). Result-defining surface / lens / PSS / attenuation computation must live exclusively in the Cell 1 namespace above; it must not be imported from Candidate B or Candidate C modules. This keeps Cell 1's result-defining path forked and independently auditable while reusing only generic, non-result-defining loading and gating utilities.

## 20. Data-contact disclosure

> *(REQUIRED-VERBATIM, §20):* Cell 1's verdict is conditional on a previously contacted, audit-frozen pullback-event population. The pullback Phase 1–3b series for SPY and the Phase 3b 2005–2022 series for SPY/EFA/EEM/GLD/TLT were inspected, partitioned, and used to estimate within-population statistics during pullback research before Coherent Numbers contacted them. The pullback BacktestParams were locked early at pullback commit 50ee2d1 and not re-tuned, which limits but does not eliminate that prior exposure. Candidate B previously applied 12-phase March-20-anchored machinery to this same population (a 10,000-element unstratified label-permutation null and an exhaustive 365-DOY anchor-control null) and reported a split-null verdict. Candidate C subsequently applied parallel 12-phase and 10-phase machinery to the same population under symmetrical 365-DOY anchor-surface rules and reported a 12-privileged verdict. Cell 1 applies a multi-focal neighborhood operationalization over bucket counts K = {7,…,19} to the same population. Cell 1's verdict is therefore conditional on (i) the pullback program's prior contact with the underlying series, (ii) Candidate B's prior 12-phase contact, and (iii) Candidate C's prior 12-and-10-phase contact, including the k=10 and k=12 365-anchor surfaces Cell 1 reuses as a provenance check. OOS 2023+ remains sealed in both repos and is out of scope for Cell 1. This disclosure is required wording; a hash citation alone does not satisfy it.

## 21. Guardrails

* **21.1** No neighborhood-surface, lens, or PSS feature may be computed against pullback `entry_date` before this memo is lock-accepted. A preview is a computation.
* **21.2** No re-opening of substrate, focal set, primary focal, window width, `K`, structure statistic, focal-elevation gate, contrast, null structure, beat-count thresholds, verdict map, machine labels, display names, or seeds after lock.
* **21.3 (REQUIRED-VERBATIM anti-rescue — Layer 1 / Layer 2):** Layer 2 (divisor, multiple, 12-family/duodecimal, harmonic-family, recursive-field, or weighted-neighbor influence) is out of scope for Cell 1 and may not be added as a "diagnostic," may not be used to rescue a Class 2/3/4 verdict, and may not borrow authority from the Kryon source. If a Layer 1 null (Class 3) or non-confirmatory result (Class 4) is followed by any Layer 2 consideration, it requires a separate decision memo explaining why Layer 2 remains scientifically justified on its own grounds; it is never an escape hatch from a Layer 1 null.
* **21.4 (REQUIRED-VERBATIM anti-rescue — cross-cell):** Candidate C's `12-privileged` verdict remains independent and is not retroactively reinterpreted by any Cell 1 outcome. Candidate B's split-null equinox result remains **not confirmed** and is not rescued, confirmed, or reinterpreted by any Cell 1 outcome. "12 beat 10 under Candidate C's locked rules" and "Cell 1's neighborhood verdict" are distinct claims that do not transfer authority in either direction.
* **21.5** Secondary diagnostics (§16) cannot rescue, upgrade, alter, or convert generic smoothness into 12-centered structure.
* **21.6** No OOS 2023+ access. No modification of the pullback repo. No new freeze.
* **21.7** Class 4 is pathology-only. A near-threshold beat count below 9,500 is a fail (Class 3 via its decision rule), never Class 4.
* **21.8** No bucket counts outside `K = {7, …, 19}`, no focal centers outside `F = {10, 12, 14, 16}`, and no window other than `±3` may be introduced under this cell.

## 22. Pre-lock checklist

The following must hold at the moment of design-lock commit (lock-acceptance is a separate later artifact; this memo does not lock-accept):

* Working tree clean of non-ignored modified/untracked files.
* Frozen-CSV manifest from `5225bfd` intact; all six referenced CSVs present and digests match.
* Reduced row schema (§6) inherited from Candidate B/C unchanged.
* Lens (§7) parameterized over `k` with the assertion-and-abort range check and the no-`%` grep gate test.
* PSS (§9.1) is the η²-form `between_k/total_k` with the `total_k = 0` abort.
* Focal set exactly `F = {10, 12, 14, 16}`, primary `12`, controls `10, 14, 16`; window exactly `±3`; `K = {7, …, 19}`.
* Structure statistic exactly the §10 OLS attenuation `−slope(median_k ~ |k−f|)` over the seven window points with distance multiset `{0,1,1,2,2,3,3}`, focal included.
* Focal-elevation gate (§11) is strict `>` against the mean of the six non-focal window neighbors of 12.
* `max_gap` (§12) uses `max(·)` over the three control focals.
* Primary null is one shared 10,000-element unstratified pooled `is_long` permutation pool; `LABEL_PERM_SEED_CELL1 = 20260518`.
* Two primary beat counts, strict `<`, threshold exactly `9500/10000`.
* Verdict map exactly four classes with the §15 display names and `class_1..class_4` machine labels; per-class (a)/(b) wording present verbatim in the verdict log.
* §15.5 granularity caveat, §15.6 compound/coupled-null disclosure, §20 data-contact disclosure, §21.3 and §21.4 anti-rescue clauses present verbatim in the verdict log.
* Asset-stratified diagnostic (§16) seeded `ASSET_STRAT_DIAG_SEED_CELL1 = 20260519`, `N_PERM = 10000`.
* Provenance gate (§17) compares recomputed `k=10`/`k=12` 365-anchor surfaces to `protocol_payload.pss_surface_10`/`pss_surface_12` in `results/candidate_c_results_20260515_051236_f3a6bf48.json` at `≤ 1e-12`; failure aborts to Class 4.
* Infrastructure boundary (§19): result-defining code in Cell 1 namespace; only `candidate_b_loader` and `candidate_b_rerun_gate` imported as generic utilities.
* Candidate C back-references verified by read-only inspection of C's artifacts in the Coherent Numbers repo: stored surface field names `pss_surface_10` / `pss_surface_12`, verdict-log path, and JSON SHA-256 as cited in §17 — or §17 updated to actual values prior to lock. Read-only inspection only; no analysis, computation, or write.

### Required-verbatim block register

The eventual closure memo must quote the following blocks character-exactly, each named by its section reference, so closure cannot paraphrase verdict-interpretation-critical language. **All of the following are required-verbatim:**

* Per-class support / non-support text: §15.1a, §15.1b, §15.2a, §15.2b, §15.3a, §15.3b, §15.4a, §15.4b.
* Granularity / neighborhood-window caveat: §15.5.
* Compound-verdict / coupled-null disclosure: §15.6.
* Inherited data-contact disclosure: §20.
* Layer 1 / Layer 2 anti-rescue disclosure: §21.3 (treated as closure-critical).
* Cross-cell anti-rescue disclosure (Candidate C independence, Candidate B not-confirmed): §21.4 (treated as closure-critical).

The closure memo must re-emit each of these by section reference; inference or paraphrase is not permitted.

---

## Appendix A — Variable glossary

* `entry_date`, `is_long`, `r_multiple` — frozen-CSV fields; `is_long` is the only permuted quantity; `r_multiple` unused in the primary outcome.
* `k` — bucket count, `k ∈ K = {7, …, 19}`.
* `d` — integer day-of-year anchor, `d ∈ 1..365`.
* `f` — focal center, `f ∈ F = {10, 12, 14, 16}`; primary `f = 12`.
* `W(f)` — `{f−3, …, f+3}`, the seven-point linear-integer window.
* `PSS_k(d)` — η²-form PSS at bucket count `k`, anchor `d` (§9.1).
* `PSS_surface_k` — `{ PSS_k(d) : d ∈ 1..365 }`.
* `median_k` — median of `PSS_surface_k` (the anchor-neutral per-bucket-count statistic).
* `distance_k` — `|k − f|` for a point in `W(f)`; window distance multiset `{0,1,1,2,2,3,3}`.
* `slope_f` — OLS slope of `median_k` on `distance_k` over `W(f)`.
* `attenuation_score_f` — `− slope_f`.
* `max_gap` — `attenuation_score_12 − max(attenuation_score_10, attenuation_score_14, attenuation_score_16)`.
* `focal_elevation_gate_12` — `median_12 > mean({median_k : k ∈ W(12), k ≠ 12})` (strict).
* `beat_count_12_structure`, `beat_count_max_gap` — primary strict-`<` beat counts (§14).
* `asset_stratified_beat_count_12_structure`, `asset_stratified_beat_count_max_gap` — §16 diagnostic counterparts.
* `LABEL_PERM_SEED_CELL1 = 20260518`, `ASSET_STRAT_DIAG_SEED_CELL1 = 20260519`, `N_PERM = 10000`.

## Appendix B — Outcome conventions

* **B.1** PSS is the η²/correlation-ratio form (§9.1); phases with `N_p = 0` contribute 0 to `between_k`; `total_k = 0` aborts (`DegenerateLongShareError`).
* **B.2** `median_k` is the rank-50% median over 365 values; with odd `N = 365` it is the 183rd order statistic (no interpolation).
* **B.3** `slope_f` is ordinary least squares on the seven `(distance_k, median_k)` points; `attenuation_score_f = −slope_f`; positive score = attenuation away from focal.
* **B.4** All beat counts use strict `<`; ties (perm value equal to observed) do not pass. Reported percentiles `beat_count / N_PERM` are descriptive; verdict thresholds are integer beat counts at `9500`.
* **B.5** `r_multiple` is not part of the primary outcome; if surfaced in any diagnostic it is used exactly as recorded in the frozen CSV (already signed), with no re-signing or transformation. Same convention as Candidate B/C Appendix B.

## Appendix C — Diagnostics enumerated

* **C.1** Asset-stratified label-permutation diagnostic (§16): within-asset `is_long` shuffle, `ASSET_STRAT_DIAG_SEED_CELL1 = 20260519`, `N_PERM = 10000`; produces `asset_stratified_beat_count_12_structure`, `asset_stratified_beat_count_max_gap`. Diagnostic only.
* **C.2** Strict monotonic attenuation per focal (§10): per-side step-wise non-increase of `median_k` in `|k−f|`. Secondary diagnostic only.
* **C.3** Per-focal window surfaces, slopes, attenuation scores, and `max_gap` for all four focals. Texture.
* **C.4** Control-focal beat counts (`attenuation_score_10/14/16` vs their own permutation distributions). Diagnostic only; not verdict inputs.
* **C.5** Provenance check against Candidate C's stored `k=10`/`k=12` 365-anchor surfaces (§17). This is a *validity gate*, not a diagnostic: failure aborts the run to Class 4.

## Appendix D — Verdict class examples

Illustrative only; not data, not pre-judgements.

* **Class 1 (12-centered neighborhood structure).** Gate passes; `beat_count_12_structure = 9800 ≥ 9500`; `beat_count_max_gap = 9620 ≥ 9500`. 12 is a structured local peak distinguished from chance and from the best control focal.
* **Class 2 (Generic substrate smoothness).** Gate passes; `beat_count_12_structure = 9710 ≥ 9500`; `beat_count_max_gap = 8400 < 9500`. 12's attenuation is real vs chance but not distinguished from a control focal's — the substrate is locally smooth around many centers.
* **Class 3 (No neighborhood evidence).** Either `focal_elevation_gate_12` fails (`median_12` not above its non-focal window mean), or `beat_count_12_structure = 9100 < 9500`. 12 behaves as an isolated point on the neighborhood operationalization; Candidate C's binary verdict is untouched.
* **Class 4 (Non-confirmatory / unresolved).** Provenance gate fails (`k=12` surface diverges from Candidate C's stored surface beyond `1e-12`), or a non-finite `median_k` enters the gate. Pathology only — not a near-threshold beat count.

---

End of design memo draft v0.1 — clean review copy. No repo file written. Nothing lock-accepted. Awaiting review before any further artifact.
