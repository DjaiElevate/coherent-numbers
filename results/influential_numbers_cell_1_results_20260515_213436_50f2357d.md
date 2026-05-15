# Influential Numbers Cell 1 v0.1 — Verdict

**Active memo:** `docs/influential_numbers_cell_1_design_memo_v0.1.md` (v0.1)
**Framework memo commit:** `8ff619c`
**Design memo commit:** `a765098`
**Lock-acceptance commit:** `3d44e9e`
**Freeze commit:** `5225bfd`
**Run timestamp (UTC):** 2026-05-15T21:34:36Z
**Repo commit before run:** `067a43dcd481a9a1adfc752236a0df205dd40b33`
**Rerun verification digest:** `50f2357dd3f70f818f6353c1b7d1c3053ff1cd303d6a0ee31dc8aadc68478b02`

## Verdict

- **Verdict class:** **No neighborhood evidence**
- **Machine label:** `class_3`
- **Pathology:** n/a

### Focal-elevation gate (k = 12)

- `pass` = False
- `median_12` = 0.0344459014
- `neighbor_mean` = 0.0346744048
- `focal_excess` = -0.0002285035
- `ambiguous` = False
- `ambiguity_reason` = n/a

### Attenuation scores (per focal)

- focal `10` : attenuation_score = 0.0001588265
- focal `12` : attenuation_score = 0.0000322310
- focal `14` : attenuation_score = 0.0005209146
- focal `16` : attenuation_score = 0.0001156763

### max_gap contrast

- `max_gap` = -0.0004886836
- `score_12` = 0.0000322310
- `strongest_control_focal` = 14
- `strongest_control_score` = 0.0005209146

### Beat counts (threshold 9500 of 10000)

- `beat_count_12_structure` = 5979  (pass=False)
- `beat_count_max_gap` = 704  (pass=False)

### Provenance gate vs Candidate C surfaces (validity gate, not a diagnostic)

- `pass` = True
- `max_abs_diff_10` = 0.0
- `max_abs_diff_12` = 0.0
- `n_anchors_checked_10` = 365
- `n_anchors_checked_12` = 365
- `tolerance` = 1e-12
- `candidate_c_json_sha256` = 130235fef110cca141fa8873bfa3a6c630a44ac11dfcad953822f41f9cd3c7d4
- `failure_reason` = n/a

### Asset-stratified diagnostic (non-verdict)

- `asset_stratified_beat_count_12_structure` = 6018
- `asset_stratified_beat_count_max_gap` = 739

## Verbalization (verbatim §15.x (a)/(b) block for the assigned class)

**(a) What it supports** *(REQUIRED-VERBATIM, §15.3a):* Under the locked decision rules, there is no evidence that 12 sits inside a structured local neighborhood on this substrate: either 12's median PSS does not exceed its non-focal window neighbors, or the 12-neighborhood attenuation is not distinguished from chance. 12, on the neighborhood operationalization, behaves as an isolated point rather than a structured local peak.

**(b) What it does not support** *(REQUIRED-VERBATIM, §15.3b):* This null does not weaken Candidate C's `12-privileged` verdict — Cell 1 asks a different question and a no-neighborhood result leaves "12 beat 10 under C's locked rules" untouched. It does not say the substrate is structureless. It does not motivate or authorize Layer 2 (divisor, multiple, harmonic, 12-family, recursive, weighted) as a rescue; per §3 and §21, Layer 2 on a Layer 1 null requires a separate decision memo argued on its own grounds. It does not bear on Candidate B.

## §15.5 Granularity / neighborhood-window caveat (verbatim)

*(REQUIRED-VERBATIM, §15.5):* Every Cell 1 verdict is scope-bounded by the locked neighborhood operationalization. "Neighborhood" here means a `±3` linear-integer window of bucket counts evaluated as the median of each bucket count's 365-anchor PSS surface; different bucket counts correspond to different temporal resolutions (e.g. `k = 12` ≈ 30.4 days/phase, `k = 16` ≈ 22.8 days/phase, `k = 7` ≈ 52 days/phase). A neighborhood verdict reflects how phase-allocation structure varies with bucket-count resolution near the focal, not a claim that any bucket count is structurally "correct," and not a test of divisor/multiple/harmonic/12-family structure. This caveat applies to all four verdict classes.

## §15.6 Compound-verdict / coupled-null disclosure (verbatim)

*(REQUIRED-VERBATIM, §15.6):* The two primary beat counts (`beat_count_12_structure`, `beat_count_max_gap`) are coupled: both are derived from the same shared pool of 10,000 pooled-population `is_long` permutations, and the per-permutation attenuation scores entering both are functions of the same recomputed `K`-wide median-PSS map. The verdict classes are pre-registered decision rules under that joint distribution, not independent p-value claims. The false-positive interpretation of a class assignment is not identical to the false-positive rate of a single independent test at the 95th percentile, and the four classes do not partition probability mass uniformly under the null.

## §20 Data-contact disclosure (verbatim)

*(REQUIRED-VERBATIM, §20):* Cell 1's verdict is conditional on a previously contacted, audit-frozen pullback-event population. The pullback Phase 1–3b series for SPY and the Phase 3b 2005–2022 series for SPY/EFA/EEM/GLD/TLT were inspected, partitioned, and used to estimate within-population statistics during pullback research before Coherent Numbers contacted them. The pullback BacktestParams were locked early at pullback commit 50ee2d1 and not re-tuned, which limits but does not eliminate that prior exposure. Candidate B previously applied 12-phase March-20-anchored machinery to this same population (a 10,000-element unstratified label-permutation null and an exhaustive 365-DOY anchor-control null) and reported a split-null verdict. Candidate C subsequently applied parallel 12-phase and 10-phase machinery to the same population under symmetrical 365-DOY anchor-surface rules and reported a 12-privileged verdict. Cell 1 applies a multi-focal neighborhood operationalization over bucket counts K = {7,…,19} to the same population. Cell 1's verdict is therefore conditional on (i) the pullback program's prior contact with the underlying series, (ii) Candidate B's prior 12-phase contact, and (iii) Candidate C's prior 12-and-10-phase contact, including the k=10 and k=12 365-anchor surfaces Cell 1 reuses as a provenance check. OOS 2023+ remains sealed in both repos and is out of scope for Cell 1. This disclosure is required wording; a hash citation alone does not satisfy it.

## §21.3 Layer 1 / Layer 2 anti-rescue (verbatim)

**21.3 (REQUIRED-VERBATIM anti-rescue — Layer 1 / Layer 2):** Layer 2 (divisor, multiple, 12-family/duodecimal, harmonic-family, recursive-field, or weighted-neighbor influence) is out of scope for Cell 1 and may not be added as a "diagnostic," may not be used to rescue a Class 2/3/4 verdict, and may not borrow authority from the Kryon source. If a Layer 1 null (Class 3) or non-confirmatory result (Class 4) is followed by any Layer 2 consideration, it requires a separate decision memo explaining why Layer 2 remains scientifically justified on its own grounds; it is never an escape hatch from a Layer 1 null.

## §21.4 Cross-cell anti-rescue (verbatim)

**21.4 (REQUIRED-VERBATIM anti-rescue — cross-cell):** Candidate C's `12-privileged` verdict remains independent and is not retroactively reinterpreted by any Cell 1 outcome. Candidate B's split-null equinox result remains **not confirmed** and is not rescued, confirmed, or reinterpreted by any Cell 1 outcome. "12 beat 10 under Candidate C's locked rules" and "Cell 1's neighborhood verdict" are distinct claims that do not transfer authority in either direction.
