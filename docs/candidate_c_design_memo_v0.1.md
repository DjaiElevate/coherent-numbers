# Coherent Numbers v0.3 — Candidate C Design Memo (Bucket-Count Comparison: 12 vs 10)

Version: v0.1 (lock-candidate draft; expanded from chat-review draft v0.3)
Date: 2026-05-15
Project: Coherent Numbers
Cell: Candidate C — 12 vs 10 bucket-count comparison
Status: Pre-registration draft. Protocol not yet locked. No analysis authorized. No harmonic-calendar features have been computed against pullback `entry_date` under this design.

---

## 1. Purpose

This memo proposes the locked protocol for Candidate C, a v0.3 Microscope Program cell whose primary question is:

> Does a 12-phase annual-sector partition organize the pooled Phase 3b pullback-event population better than a 10-phase annual-sector partition under symmetrical anchor-surface rules?

The question is framed as a bucket-count comparison of two specific resolutions (`k = 12` versus `k = 10`), not as a test of duodecimal nesting, neighbor-influence, or "Influential Numbers" structure. The cell stays narrow on purpose.

This memo locks five framework-memo narrowing decisions (§3 of `docs/candidate_c_framework_memo_v0.1.md`):

1. **Question alignment (decision 1):** Q2 — bucket-count privilege — is selected, narrowed further to 12 vs 10 only. The broader §9.2 set `{6, 8, 10, 12, 18, 24}` is explicitly out of scope for this cell.
2. **Substrate (decision 2):** the same pooled Phase 3b 1,282-trade frozen population used by Candidate B. The inherited-contact disclosure (§13) is load-bearing.
3. **Anchor-control surface (decision 3):** a symmetrical exhaustive 365-DOY anchor surface for both bucket counts. The surface is absorbed into the primary statistic (median PSS over the surface), not a separate anchor-control null.
4. **Primary statistic normalization (decision 4):** three coupled nulls — two matched and one comparison — all computed from the same shared 10,000-element pool of pooled-population `is_long` permutations.
5. **Diagnostic tier discipline (decision 5):** the primary is the 12-vs-10 comparison plus individual significance for each bucket count; nested-duodecimal, neighbor-influence, Influential Numbers, and other lens-family extensions are out of scope for this cell and are not eligible to upgrade the verdict.

The framework memo's §5 originally sketched a nested-duodecimal design. This design memo deliberately diverges from that sketch in favor of the bucket-count-comparison framing, for the reasons given in framework §10 (the nested approach inherits Candidate B's anchor problem and faces a 144-cell sample-mass issue). The nested-duodecimal question is not abandoned; it is reserved for a possible future cell contingent on Candidate C's findings.

## 2. Inheritance from Candidate B and the framework memo

The following decisions and conventions are inherited unchanged and not re-opened here:

* The pullback substrate is treated as frozen raw data inside Coherent Numbers. The pullback repo is not touched.
* OOS 2023+ remains sealed in both repos and is out of scope for C.
* The data-contact disclosure pattern from B §13 is extended and strengthened in §13 of this memo to acknowledge B's prior application of 12-phase machinery to the same population.
* The frozen-CSV freeze at commit `5225bfd` is the run substrate. No new freeze is required.
* The reduced row schema, η²/correlation-ratio PSS form, exhaustive-enumeration discipline (no sampling-based anchor control), assertion-and-abort phase-range check, deterministic-reproducibility requirement, and three-strikes hash-verification pattern are all carried forward from Candidate B's locked design memo at commit `1e9a3e6`.

## 3. Population scope

Primary (confirmatory): the pooled Phase 3b 5-asset population — SPY, EFA, EEM, GLD, TLT — 1,282 trades total, produced under identical pullback `BacktestParams` at pullback commit `7806a6d` over the common window 2005-01-01 – 2022-12-31. Source manifest: `docs/pullback_population_freeze_manifest_v0.1.md` at commit `5225bfd`. This is the same population analyzed by Candidate B.

No secondary population is in scope for this cell. The SPY 301-trade base population is not used.

The primary verdict is computed exclusively on this pooled population. Inherited data contact is acknowledged in §13.

## 4. Primary outcome

The primary observed outcome is a three-quantity vector: `median_12_observed`, `median_10_observed`, and `diff_observed_12_minus_10`. The final verdict is determined by four beat counts derived from the coupled permutation nulls.

* `median_12_observed` — median over 365 anchor-shifted `PSS_k=12` values on the real `is_long` vector.
* `median_10_observed` — median over 365 anchor-shifted `PSS_k=10` values on the real `is_long` vector.
* `diff_observed_12_minus_10 = median_12_observed - median_10_observed` — directed comparison statistic.

The four integer beat counts that determine the primary verdict (§12) are defined in §10 as comparisons of these three observed quantities against three coupled null distributions.

Choice rationale: by absorbing the 365-anchor surface into the primary statistic via the median, the comparison becomes anchor-neutral — the question is not "is the candidate March-20 anchor specially good at resolution `k`?" but "regardless of anchor, is resolution 12 typically better at organizing the data than resolution 10?". This is a different question from Candidate B's anchor-specific question.

## 5. Reduced analytical row schema

The reduced row schema is inherited verbatim from Candidate B §5. Each analytical row corresponds to one frozen pullback trade with the following per-row fields:

* `trade_id` — stable identifier within the frozen artifact.
* `asset` — one of `{SPY, EFA, EEM, GLD, TLT}`.
* `entry_date` — primary phase-assignment date (calendar-day granularity, exchange tz of the frozen artifact).
* `exit_date`.
* `is_long` — boolean direction label.
* `r_multiple` — signed trade outcome as recorded in the frozen artifact.
* `frozen_artifact_id` — pointer to the manifest entry for this trade's source CSV.

No new columns are added by Candidate C. `source_sha256` remains dataset-level provenance from the freeze manifest, not a per-row analytical field.

## 6. Frozen-data provenance

Provenance is the freeze manifest at commit `5225bfd`. At run start, the analysis script:

1. Reads the manifest.
2. Recomputes SHA-256 of each referenced CSV.
3. Aborts if any digest mismatches.
4. Re-verifies after the reduced view is constructed.
5. Re-verifies a third time between the two protocol invocations inside the rerun gate.

Same triple-check pattern as Candidate B §6. The pullback repo's HEAD is not consulted at run time (§15).

## 7. Calendar lens — parameterized 12 and 10 annual-sector partitions

Candidate C uses two annual-sector lenses in parallel: a 12-phase March-20-anchored partition and a 10-phase March-20-anchored partition. Both are evaluated across the same exhaustive 365-DOY anchor surface.

### 7.1 Parameterized phase assignment formula (candidate civil-date anchor)

For a given trade with `entry_date` and bucket count `k ∈ {10, 12}`:

1. Locate the relevant annual cycle (candidate anchor: March 20).

   * If `entry_date >= date(entry_date.year, 3, 20)`:

     * `cycle_start = date(entry_date.year, 3, 20)`
   * Otherwise:

     * `cycle_start = date(entry_date.year - 1, 3, 20)`
   * `cycle_end = date(cycle_start.year + 1, 3, 20)`
2. Compute the within-cycle position.

   * `cycle_length_days = (cycle_end - cycle_start).days` (365 or 366)
   * `days_since_start = (entry_date - cycle_start).days`
3. Assign phase.

   * `phase = floor(days_since_start * k / cycle_length_days)`
   * Assert `phase ∈ {0, 1, ..., k - 1}`. If the assertion fails, the run aborts. There is no silent clamp.

### 7.2 Anchor-shifted form (for the 365-DOY anchor sweep)

For a given trade with `entry_date`, integer DOY anchor `d ∈ 1..365`, and bucket count `k ∈ {10, 12}`:

1. `anchor_in_year(y) = date(y, 1, 1) + timedelta(d - 1)`
2. Cycle structure as in §7.1 with March 20 replaced by `anchor_in_year(.)` consistently.
3. `cycle_length_days_d`, `days_since_start_d` as in §7.1.
4. `phase_d = floor(days_since_start_d * k / cycle_length_days_d)`
5. Assert `phase_d ∈ {0, 1, ..., k - 1}`; abort on assertion failure.

### 7.3 Properties

* Each `k = 12` sector is ≈ `cycle_length_days / 12` ≈ 30.42 – 30.50 days. Each `k = 10` sector is ≈ `cycle_length_days / 10` ≈ 36.50 – 36.60 days. These different bin widths are intentional and motivate the granularity caveat in §12.4.
* No `%` operator appears in any C lens code. The same grep gate as Candidate B's `tests/test_candidate_b_lens.py` is required in C's lens test module.
* Leap-year effects enter only through `cycle_length_days_d`, which is 365 or 366 depending on whether the cycle traverses a leap day. No separate Feb-29 or DOY-366 anchor is enumerated outside the `1..365` integer-DOY scheme. In leap years, the integer DOY 60 anchor coincides with Feb 29 as a direct consequence of the §7.2 enumeration `anchor_in_year(y) = date(y, 1, 1) + timedelta(d - 1)`; this is the inherited Candidate B convention and is retained for direct comparability under the §11.6 provenance check.
* The lens is deterministic given (`entry_date`, `k`, `d`).

### 7.4 Anchor population

Anchor enumeration covers integer DOYs `1..365` exhaustively, no sampling, no seed consumed. This inherits the v0.3.3 finite-control discipline of `docs/harmonic_calendar_design_memo_v0.3.3.md`.

The candidate civil-date March-20 anchor used in §7.1 corresponds to DOY 79 in non-leap years and DOY 80 in leap years (March 20 of a leap year is calendar day 80, not 79). The DOY-79 anchor in the §7.2 365-DOY sweep is therefore not identical to the civil-date March-20 anchor: DOY 79 lands on March 20 in non-leap years and March 19 in leap years. This distinction is load-bearing for the §11.4 diagnostic.

DOY 79 is retained in the 365-DOY sweep and is not given any special status in the primary statistic.

### 7.5 Primary assignment date

`entry_date`. `exit_date` is not used for phase assignment. Holding-period effects are absorbed into `r_multiple` (not used in the primary outcome).

## 8. Bucket-count adaptation rationale

### 8.1 Why 12 vs 10 only

The locked design tests exactly two bucket counts, paired as a single binary contrast. Reasons:

* A clean test of "is 12 privileged at all?" is best framed as a comparison against one well-chosen alternative, not against a broad set. A broad set introduces a multi-class adjudication problem and degrades the inferential clarity of the result.
* 10 is the most informative single contrast to 12. It is the closest non-duodecimal annual integer that has its own historical/structural use (base-10 calendar groupings, decimal time, decadal patterning) but no duodecimal connection. 6 and 24 are duodecimal multiples; 8 and 18 lack a clearly distinct cultural reference; 12 vs 13/14 would test marginal arithmetic rather than a meaningful contrast.
* Bin widths. `k = 12` yields ≈ 30-day bins; `k = 10` yields ≈ 36-day bins. Both are within the same order of magnitude as the substrate's natural event rate (≈ 100 trades per outer phase at either bucket count on a 1,282-trade pool), so neither suffers a fatal sample-mass collapse.

### 8.2 Why not a broader bucket-count set

A broader set (e.g., `{6, 8, 10, 12, 18, 24}`) is the §9.2 framework alternative. It is not chosen for this cell because:

* The locked verdict map and the four beat-count thresholds become combinatorially harder to interpret over a 6-way comparison.
* Multiple-comparisons discipline would dominate the design.
* A future cell can do the broader sweep; Candidate C deliberately stays narrow.

### 8.3 Why "duodecimal vs decimal" is the right narrowed question

The candidate question for Candidate C is resolution privilege, not anchor specificity (that was B) or nested multi-scale structure (that is reserved for a possible future cell). The 12-vs-10 contrast directly probes whether the program's duodecimal aesthetic carries empirical weight against a non-duodecimal alternative at comparable temporal resolution.

## 9. Primary outcome definitions

### 9.1 Per-bucket-count PSS at a single anchor (η²-form)

For bucket count `k` and a fixed anchor configuration (either candidate March 20 or DOY anchor `d`), let `N_p` be the trade count in phase `p ∈ {0..k-1}` and `L_p` be the long-trade count in phase `p`. Let `N_total = Σ_p N_p` and `share_pooled = (Σ_p L_p) / N_total`. Define `share_p = L_p / N_p` for phases with `N_p > 0`; phases with `N_p = 0` contribute 0 to `between_k`.

Then:

```text
between_k = Σ_p (N_p / N_total) × (share_p − share_pooled)^2
total_k   = share_pooled × (1 − share_pooled)
PSS_k     = between_k / total_k
```

Properties:

* η²/correlation-ratio form, identical family to Candidate B §9.1 but parameterized by `k`.
* Bounded in `[0, 1]` when `total_k > 0`.
* If `total_k = 0` (pooled population all-longs or all-shorts), raise `DegenerateLongShareError` and abort the run. No fallback.

### 9.2 Per-bucket-count surface and primary statistic (median PSS)

For each bucket count `k`, the 365-anchor surface is:

```text
PSS_surface_k = { PSS_k(d) : d ∈ 1..365 }
```

where `PSS_k(d)` uses the anchor-shifted phase formula of §7.2 at DOY `d`.

The per-bucket-count primary statistic is:

```text
median_k = median(PSS_surface_k)
```

Two observed values are reported: `median_12_observed` and `median_10_observed`.

### 9.3 Comparison statistic

```text
diff_observed = median_12_observed - median_10_observed
```

Sign convention: positive `diff_observed` means `k = 12` produces a higher typical PSS than `k = 10` across the anchor surface; negative means `k = 10` dominates.

## 10. Null hypotheses and finite controls — three coupled shared-permutation nulls

The locked design uses three null distributions, all derived from one shared pool of `N_PERM = 10,000` pooled-population permutations of `is_long`. There is no separate anchor-control null because the anchor surface is absorbed into the primary statistic via the median (§9.2). The 365-anchor exhaustive enumeration appears inside both the observed statistic and every permutation draw.

### 10.1 Shared permutation procedure

Locked seed: `LABEL_PERM_SEED_C = 20260516` (distinct from Candidate B's `LABEL_PERM_SEED = 20260514` and `ASSET_STRAT_DIAG_SEED = 20260515`). Procedure:

For each `i ∈ 1..10000`:

1. Draw a uniform, unstratified pooled shuffle of `is_long` across all 1,282 trades. Phase labels and asset labels held fixed; only `is_long` is permuted. No asset stratification.
2. Compute `median_12_perm[i]` — median over the 365-anchor PSS surface for `k = 12` using the permuted `is_long_i`.
3. Compute `median_10_perm[i]` — median over the 365-anchor PSS surface for `k = 10` using the same permuted `is_long_i`.
4. Compute `diff_perm[i] = median_12_perm[i] - median_10_perm[i]`.

### 10.2 The three derived null distributions

From the 10,000 paired draws above:

* `matched_null_12 = { median_12_perm[i] : i ∈ 1..10000 }` — tests whether `k = 12` individually organizes structure beyond chance.
* `matched_null_10 = { median_10_perm[i] : i ∈ 1..10000 }` — tests whether `k = 10` individually organizes structure beyond chance.
* `comparison_null = { diff_perm[i] : i ∈ 1..10000 }` — tests whether the observed direction and magnitude of `median_12 − median_10` is distinguishable from chance.

### 10.3 Beat counts (strict <; ties do not pass)

```text
beat_count_12_individual = #{ i : median_12_perm[i] < median_12_observed }
beat_count_10_individual = #{ i : median_10_perm[i] < median_10_observed }
beat_count_comparison_12 = #{ i : (median_12_perm[i] − median_10_perm[i]) < diff_observed }
beat_count_comparison_10 = #{ i : (median_10_perm[i] − median_12_perm[i]) < (−diff_observed) }
                         = #{ i : diff_perm[i] > diff_observed }
```

Note: `beat_count_comparison_12 + beat_count_comparison_10 + ties = N_PERM`. The two comparison beat counts encode the two tail directions of the same diff distribution; both are reported because the verdict map treats them as distinct rules (§12).

### 10.4 Coupling

All four beat counts are derived from the same 10,000 permutation draws. They are not statistically independent. The joint dependence under the null is non-trivial and is treated by the verdict map as a pre-registered decision rule, not as four independent p-values. See §12.5 for the compound-verdict disclosure.

## 11. Controls and diagnostics (non-confirmatory)

The following diagnostics are reported but do not affect the verdict. They cannot rescue, upgrade, or alter the four-class verdict assignment.

### 11.1 Best-anchor PSS per bucket count

For each `k`, report the peak of the 365-anchor surface — `argmax_d PSS_k(d)` and the corresponding `PSS_k(d*)`. Diagnostic only.

### 11.2 Anchor-distribution shape

For each `k`, report mean, standard deviation, min, max of `PSS_surface_k`, plus the full 365-element surface. Used to characterize the texture; not a verdict input.

### 11.3 Asset-stratified label-permutation diagnostic

Parallel to Candidate B §11.3, repeated for both bucket counts. Procedure: re-run §10.1 with `is_long` shuffled within each asset's index slice rather than pooled. Locked seed: `ASSET_STRAT_DIAG_SEED_C = 20260517` (distinct from both C's primary seed and B's two seeds). `N_PERM = 10,000`. Produces parallel matched and comparison null distributions, reported as diagnostic.

### 11.4 Per-asset PSS at civil-date March-20 and peak anchors

For each `k`, report per-asset `PSS_k` at:

* the candidate civil-date March-20 anchor, applied via the §7.1 formula. This anchor always lands on March 20 of the relevant year regardless of leap status (DOY 79 in non-leap years, DOY 80 in leap years). It is not in general equal to any single value `PSS_k(d)` from the §7.2 365-DOY surface, because the surface uses fixed-integer DOY anchors that diverge from civil March 20 in leap years (DOY 79 = March 19 in leap years). The per-asset `PSS_k` at civil-date March-20 reported here is therefore not in general equal to `PSS_k(d = 79)` or `PSS_k(d = 80)` from `PSS_surface_k`.
* the bucket count's peak anchor `d*` (§11.1), drawn from the §7.2 365-DOY surface.

This diagnostic is reported for direct comparability with Candidate B's per-asset civil-March-20 results, not as a slice of `PSS_surface_k`. Diagnostic only; no per-asset confirmatory tests are part of this cell.

### 11.5 Top-10 anchors per bucket count

For each `k`, list the 10 DOY anchors with highest `PSS_k(d)` and report their values. Diagnostic only.

### 11.6 Provenance check against Candidate B

Candidate C's recomputed `k = 12` 365-anchor PSS surface must match Candidate B's stored `n2_null_full` for `k = 12` to numerical precision (≤ `1e-12` absolute difference per anchor). The stored Candidate B surface lives at `protocol_payload.n2_null_full` in `results/candidate_b_results_20260514_231323_c1982503.json`, with stringified integer DOY keys `"1"` through `"365"`. Candidate C implementation must compare Candidate C anchor `d` to Candidate B key `str(d)`.

Mismatch indicates implementation inconsistency between the two cells and aborts the run. This is an audit-chain consistency check, not a verdict input. The Candidate B verdict log path used for comparison: `results/candidate_b_results_20260514_231323_c1982503.json`.

## 12. Verdict map

### 12.1 Locked thresholds

All four beat-count thresholds are exactly 9,500 out of 10,000. Strict `<` comparison; ties do not contribute to a pass.

### 12.2 Four-class verdict map

The verdict classes are mutually exclusive and collectively exhaustive over the four beat-count vector. The four classes are:

### Class 1 — 12-privileged

Decision rule:

```text
beat_count_comparison_12 ≥ 9500 AND beat_count_12_individual ≥ 9500.
```

(a) What it supports: under the locked decision rules, the 12-bucket partition is distinguished from the 10-bucket partition on this substrate and the 12-bucket partition is itself non-random against its own null. The comparison and individual evidence are jointly consistent with 12 carrying structure that 10 does not capture under the locked protocol.

(b) What it does not support: the verdict does not establish that 12 is uniquely privileged among all bucket counts (the locked design tests only 12 vs 10); it does not establish that 12 is privileged because of a duodecimal property as opposed to a feature of this substrate at this resolution; it does not confirm or rescue Candidate B's equinox hypothesis; and it does not generalize to other populations, windows, or anchor configurations not pre-registered here.

### Class 2 — 10-privileged

Decision rule:

```text
beat_count_comparison_10 ≥ 9500 AND beat_count_10_individual ≥ 9500.
```

(a) What it supports: under the locked decision rules, the 10-bucket partition is distinguished from the 12-bucket partition on this substrate and the 10-bucket partition is itself non-random against its own null. Comparison and individual evidence are jointly consistent with 10 carrying structure that 12 does not capture under the locked protocol.

(b) What it does not support: the verdict does not falsify the duodecimal program in general; it does not establish 10 as uniquely privileged among all bucket counts; it does not show that 10 is structurally meaningful (the result might reflect a base-rate periodicity unrelated to "10-ness"); and it does not generalize to other populations or anchors.

### Class 3 — Tied / both-structured

Decision rule:

```text
neither comparison threshold is met AND both individual thresholds ≥ 9500.
```

(a) What it supports: under the locked decision rules, both 12-bucket and 10-bucket partitions are individually non-random on this substrate, but neither is distinguished from the other in direct comparison. The phase-conditional long-share signal is present at a resolution scale that the comparison cannot tell apart at the 9500-threshold level. This is informative texture about the structural scale: the signal is unlikely to be specific to either bucket count.

(b) What it does not support: the verdict does not adjudicate whether 12 or 10 is the "correct" frame; it does not establish that the underlying signal is continuous, multi-scale, or anchor-related; it does not rescue Candidate B; and it does not motivate selecting either bucket count for downstream work.

### Class 4 — Non-confirmatory / unresolved

Decision rule: everything else.

(a) What it supports: under the locked decision rules, the result does not support 12-privileged, 10-privileged, or Tied / both-structured. The individual and comparison beat counts are reported as diagnostic texture but they do not upgrade the verdict. This class may include cases where one bucket count shows individual structure without a decisive 12-vs-10 comparison — e.g., 12 individually passes but the comparison threshold is not met; or where comparison favours one direction without the individual structure threshold being cleared on either side.

(b) What it does not support: the verdict does not say the substrate is structureless; it does not adjudicate the broader duodecimal framing question; it does not rescue Candidate B's equinox hypothesis; it does not motivate amending the locked design after the fact; and it does not constrain future cells that might test different bucket-count pairs, different substrates, or different lens families.

### 12.3 All four beat counts are reported regardless of verdict

The verdict log emits `beat_count_12_individual`, `beat_count_10_individual`, `beat_count_comparison_12`, and `beat_count_comparison_10` unconditionally. The verdict class is determined by the §12.2 rules applied to those four integers.

### 12.4 Required granularity caveat (verbatim in the verdict log)

The following wording is required in the verdict log's verdict section and may not be paraphrased:

> The four-class verdict map compares the median PSS across the 365-anchor surface at two different temporal resolutions: ≈ 30.4 days per phase for k = 12 and ≈ 36.5 days per phase for k = 10. Median PSS is interpretable as "typical phase-structure for this bucket count" rather than "phase-structure at a specific anchor configuration." The locked decision rules are methodologically valid as pre-registered, but the interpretation of every verdict class must acknowledge that the comparison is between two different temporal resolutions, not a test of which resolution is "correct" in any absolute sense:
>
> * A 12-privileged or 10-privileged verdict reflects which resolution better organizes long/short allocation on this substrate under the anchor surface, not which bucket count is structurally correct in any absolute sense.
> * A Tied / both-structured verdict reflects that both resolutions are individually non-random and cannot be distinguished from each other under the comparison threshold, not that the underlying signal is resolution-independent.
> * A Non-confirmatory / unresolved verdict does not adjudicate the resolution question at all; it states that the pre-registered decision rules do not separate the alternatives under the locked threshold structure.
>
> This caveat applies to all four verdict classes.

### 12.5 Compound-verdict disclosure (verbatim in the verdict log)

The following wording is required in the verdict log's verdict section and may not be paraphrased:

> The four beat counts that drive the verdict are coupled. They are derived from the same shared pool of 10,000 pooled-population is_long permutations. The verdict classes are pre-registered decision rules under that joint distribution, not independent p-value claims. The false-positive interpretation of a class assignment is therefore not identical to the false-positive rate of a single independent test at the 95th percentile, and the four classes do not partition probability mass uniformly under the null.

### 12.6 No-rescue rule

Secondary diagnostics in §11 (best-anchor PSS, anchor-distribution shape, asset-stratified diagnostic, per-asset PSS, top-10 anchors, provenance check) cannot rescue or upgrade the verdict. A Non-confirmatory / unresolved verdict remains so regardless of diagnostic patterns.

## 13. Data-contact disclosure (required wording, verbatim)

The following wording is required in the verdict log and in any closure memo:

> Candidate C's verdict is conditional on a previously contacted, audit-frozen pullback-event population. The pullback Phase 1–3b series for SPY and the Phase 3b 2005–2022 series for SPY/EFA/EEM/GLD/TLT were inspected, partitioned, and used to estimate within-population statistics during pullback research before Coherent Numbers contacted them. The pullback BacktestParams were locked early at pullback commit 50ee2d1 and not re-tuned, which limits but does not eliminate that prior exposure. Candidate B previously applied 12-phase March-20-anchored machinery to this same population — specifically a 10,000-element unstratified label-permutation null (§10.1 of docs/candidate_b_design_memo_v0.1.md) and an exhaustive 365-DOY anchor-control null (§10.2) — and reported the resulting verdict in results/candidate_b_results_20260514_231323_c1982503.json. Candidate C applies parallel 12-phase and 10-phase machinery to the same population under symmetrical anchor-surface rules. Candidate C's verdict is therefore conditional on (i) the pullback program's prior contact with the underlying series, and (ii) Candidate B's prior contact with the pooled Phase 3b population under 12-phase machinery. OOS 2023+ remains sealed in both repos and is out of scope for Candidate C. This disclosure is required wording; a hash citation alone does not satisfy it.

## 14. Reproducibility requirements and seeds

* All randomness in this protocol resides in §10.1 (primary) and §11.3 (diagnostic). Both use `N_PERM = 10,000`.
* `LABEL_PERM_SEED_C = 20260516` is used for §10.1 (primary unstratified pooled permutation). It seeds a single `numpy.random.Generator(numpy.random.PCG64(LABEL_PERM_SEED_C))` instance.
* `ASSET_STRAT_DIAG_SEED_C = 20260517` is used for §11.3 (asset-stratified diagnostic). Independent PCG64 instance.
* C's seeds are distinct from B's `LABEL_PERM_SEED = 20260514` and `ASSET_STRAT_DIAG_SEED = 20260515` by design, so C's permutation sequences are not sub-samples of B's.
* The 365-DOY anchor sweep is deterministic and exhaustive; no seed is consumed.
* §7.1 / §7.2 phase assignment is deterministic given the parameters.
* The frozen-CSV provenance verification (§6) is performed three times per run as in B.
* The deterministic rerun gate (analogous to B's) invokes `protocol.run` twice, canonicalizes the protocol payload (numeric results, beat counts, verdict, verbalization class — header metadata excluded), SHA-256-compares, and aborts on mismatch. The matched digest becomes `rerun_verification_digest` in the verdict-log header.
* A clean run from a clean checkout of Coherent Numbers at the memo-lock commit must reproduce the four beat counts, the verdict class, and the rerun digest bit-for-bit.

## 15. Substrate clause — frozen CSV hashes, not pullback HEAD

Following the freeze commit `5225bfd`, Candidate C's run substrate is the set of frozen CSV SHA-256 digests recorded in the Coherent Numbers freeze manifest. The pullback research repo's HEAD is not part of the run substrate.

* Pullback HEAD at inventory time was `eac925c` (historical note from `docs/cell_selection_decision_memo_v0.2.md` §4). This is not a Candidate C run-time precondition.
* If the pullback repo is re-inspected and drift is observed, it is recorded as a provenance note but does not block a Candidate C run whose frozen-CSV digests match the manifest.
* If the frozen-CSV digests do not match the manifest, the run aborts regardless of pullback HEAD state.

## 16. Guardrails (pre-lock and through run)

* No harmonic-calendar features may be computed against pullback `entry_date` before this memo is locked.
* No phase-distribution sanity checks, histograms, or "preview" joins before lock. A preview is a computation.
* No re-opening of bucket-count set, anchor surface, primary statistic, null structure, beat-count thresholds, verdict map, or seeds after lock.
* No OOS 2023+ access. No modifications to the pullback repo.
* Secondary diagnostics (§11) cannot rescue, upgrade, or alter the primary verdict.
* No sampling-based anchor control may be introduced (the v0.3.3 exhaustive-enumeration discipline is inherited).
* No nested-duodecimal or neighbor-influence tests are part of this cell. Those are explicitly out of scope and may not be silently included as "diagnostics."
* No additional bucket counts beyond `k = 12` and `k = 10` may be tested under this cell's verdict map.

## 17. Pre-lock checklist

The following must hold at the moment of design-lock commit:

* Working tree is clean of non-ignored modified or untracked files. Files covered by `.gitignore` may exist locally but are not part of the audit state.
* Frozen-CSV manifest from commit `5225bfd` is intact; all referenced CSVs are present and digests match.
* Reduced row schema (§5) is inherited from Candidate B unchanged.
* Phase formula (§7.1, §7.2) is the parameterized annual-sector formula with `bucket_count = k` argument and the assertion-and-abort range check on `phase ∈ {0..k-1}`. No `%` residue logic appears anywhere in C's lens code (grep gate test required in C's lens tests, parallel to B's).
* §9.1 `PSS_k` is the η²/correlation-ratio form `between_k / total_k`, with the `total_k = 0` abort rule in force.
* Bucket counts in scope are exactly `k = 12` and `k = 10`.
* Anchor sweep enumerates 365 integer-DOY anchors exhaustively; no sampling. No separate Feb-29 / DOY-366 anchor is enumerated; DOY 60 in leap years coincides with Feb 29 as inherited from B.
* Primary statistic per bucket count is the median PSS over the 365-anchor surface (§9.2).
* Three nulls are derived from the same shared 10,000-element permutation pool (§10.1, §10.2).
* All four beat-count thresholds are exactly 9,500.
* Verdict map is exactly four classes: 12-privileged, 10-privileged, Tied / both-structured, Non-confirmatory / unresolved.
* Verdict-class interpretive language in §12.2 is the locked wording above, used verbatim in the verdict log.
* Granularity caveat (§12.4) is present verbatim in the verdict log, with coverage of all four verdict classes.
* Compound-verdict disclosure (§12.5) is present verbatim in the verdict log.
* Inherited data-contact disclosure (§13) is present verbatim, naming both pullback Phase 1–3b contact and Candidate B's prior 12-phase contact.
* `LABEL_PERM_SEED_C = 20260516` and `ASSET_STRAT_DIAG_SEED_C = 20260517` locked, with `N_PERM = 10,000` (§14).
* Substrate clause (§15) names frozen-CSV hashes (not pullback HEAD) as run substrate.
* Provenance check (§11.6) against Candidate B's stored `k = 12` 365-anchor surface is enabled and enforces a ≤ `1e-12` per-anchor tolerance. The stored Candidate B surface is read from `protocol_payload.n2_null_full` in `results/candidate_b_results_20260514_231323_c1982503.json`, using stringified integer DOY keys `"1"` through `"365"`; implementation compares Candidate C anchor `d` to Candidate B key `str(d)`.
* Candidate B back-references verified by direct inspection of B's artifacts in the Coherent Numbers repo at commit `03bf9b9` or later:

  * Candidate B primary label-permutation seed equals `20260514` as asserted in C §10.1.
  * Candidate B asset-stratified diagnostic seed equals `20260515` as asserted in C §10.1.
  * The stored `k = 12` 365-anchor PSS surface in `results/candidate_b_results_20260514_231323_c1982503.json` is named `n2_null_full` as referenced in C §11.6, or — if differently named — §11.6 is updated to the actual field name prior to lock.
  * The Candidate B design memo `docs/candidate_b_design_memo_v0.1.md` has its unstratified pooled label-permutation null in §10.1 and its exhaustive 365-DOY anchor-control null in §10.2, as cited in C §13. If the section numbers differ, §13 is updated to the actual section numbers prior to lock.
  * Verification is a read-only inspection in Claude Code. No analysis, computation, or write operation is permitted under this item.

---

## Appendix A — Variable glossary

* `entry_date` — calendar date a pullback trade entered the market, as recorded in the frozen CSV.
* `is_long` — boolean direction label as recorded in the frozen CSV.
* `r_multiple` — signed trade outcome (not used in C's primary outcome).
* `k` — bucket count, `k ∈ {10, 12}`.
* `d` — integer day-of-year anchor, `d ∈ 1..365`.
* `phase` — integer in `{0..k-1}` produced by §7.1 / §7.2.
* `N_p`, `L_p` — per-phase trade count and per-phase long-trade count.
* `N_total`, `share_pooled` — pooled trade count and pooled long share.
* `between_k`, `total_k`, `PSS_k` — η²-form components per bucket count (§9.1).
* `PSS_k(d)` — `PSS_k` computed at anchor DOY `d` via §7.2.
* `PSS_surface_k` — `{ PSS_k(d) : d ∈ 1..365 }`.
* `median_k_observed` — observed median over `PSS_surface_k`.
* `median_k_perm[i]` — i-th permutation's median.
* `diff_observed` — `median_12_observed - median_10_observed`.
* `diff_perm[i]` — `median_12_perm[i] - median_10_perm[i]`.
* `beat_count_12_individual`, `beat_count_10_individual`, `beat_count_comparison_12`, `beat_count_comparison_10` — strict beat counts (§10.3).
* `LABEL_PERM_SEED_C = 20260516`, `ASSET_STRAT_DIAG_SEED_C = 20260517`, `N_PERM = 10000`.

## Appendix B — Outcome conventions

### B.1 Per-bucket-count PSS (η²-form)

Computed per §9.1. Identical functional family to Candidate B §9.1 generalized over `k`. Phases with `N_p = 0` contribute 0 to `between_k`. `total_k = 0` aborts the run.

### B.2 Median over anchor surface

`median_k = median(PSS_surface_k)` where the median is computed over the 365 values via the standard rank-50% definition. With an odd `N = 365`, the median is the 183rd order statistic (no interpolation ambiguity).

### B.3 Comparison statistic

`diff = median_12 - median_10`. Sign convention: positive favors `k = 12`.

### B.4 Beat-count strictness

All four beat counts use strict `<`. Ties (permutation value equal to observed value) do not contribute to a pass. Reported strict percentiles `beat_count / N_PERM` are descriptive only; verdict thresholds are integer beat counts.

### B.5 r_multiple convention

`r_multiple` is not part of Candidate C's primary outcome. If reported in any diagnostic, it is used exactly as recorded in the frozen CSV — already signed by trade outcome — with no multiplication by `is_long`, no re-signing, and no transformation. Same convention as Candidate B Appendix B.2.

## Appendix C — Diagnostics

**C.1** — Per-bucket-count best-anchor PSS and DOY (§11.1). Diagnostic only.

**C.2** — Anchor-distribution shape: mean, std, min, max, and full 365-value surface per bucket count (§11.2). Diagnostic only.

**C.3** — Asset-stratified label-permutation diagnostic for both bucket counts (§11.3), seeded by `ASSET_STRAT_DIAG_SEED_C = 20260517`. Produces parallel matched and comparison nulls. Diagnostic only; cannot upgrade the verdict.

**C.4** — Per-asset `PSS_k` at the candidate civil-date March-20 anchor (applied via §7.1) and at each bucket count's peak anchor `d*` from the §7.2 365-DOY surface (§11.4). The civil-date March-20 diagnostic is not in general equal to any single `PSS_k(d)` from `PSS_surface_k`, because civil March 20 falls on DOY 80 in leap years while DOY 79 in the surface lands on March 19 in leap years. Diagnostic only.

**C.5** — Top-10 DOY anchors per bucket count (§11.5). Diagnostic only.

**C.6** — Provenance check against Candidate B's stored `k = 12` 365-anchor surface (§11.6). Recomputed `PSS_k=12(d)` for `d ∈ 1..365` must match B's `protocol_payload.n2_null_full` entries within ≤ `1e-12` absolute per-anchor difference, reading Candidate B's stringified integer DOY keys `"1"` through `"365"` and comparing Candidate C anchor `d` to Candidate B key `str(d)`. Mismatch aborts the run. This is an audit-chain consistency check, not a verdict input.
