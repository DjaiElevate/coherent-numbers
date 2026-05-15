# Candidate C v0.1 — Verdict

**Active memo:** `docs/candidate_c_design_memo_v0.1.md` (v0.1)
**Design memo commit:** `401ce45`
**Lock-acceptance commit:** `dc97576`
**Freeze commit:** `5225bfd`
**Run timestamp (UTC):** 2026-05-15T05:12:36Z
**Repo commit before run:** `4432591fc4afa189a37d5cd054e5e6b0cbebaafd`
**Rerun verification digest:** `f3a6bf48f7266c2d654dac36f79d38825f14f727d20aeead98e204463a39f762`

## Verdict

- **Verdict class:** **12-privileged**
- **Observed median PSS (k=12):** 0.03444590
- **Observed median PSS (k=10):** 0.02985119
- **diff_observed (12 - 10):** 0.00459471

### Beat counts (threshold 9500 of 10000)

- `beat_count_12_individual` = 10000  (pass=True)
- `beat_count_10_individual` = 10000  (pass=True)
- `beat_count_comparison_12` = 9973  (pass=True)
- `beat_count_comparison_10` = 27  (pass=False)

## Verbalization (verbatim §12.2 block for the assigned class)

(a) What it supports: under the locked decision rules, the 12-bucket partition is distinguished from the 10-bucket partition on this substrate and the 12-bucket partition is itself non-random against its own null. The comparison and individual evidence are jointly consistent with 12 carrying structure that 10 does not capture under the locked protocol.

(b) What it does not support: the verdict does not establish that 12 is uniquely privileged among all bucket counts (the locked design tests only 12 vs 10); it does not establish that 12 is privileged because of a duodecimal property as opposed to a feature of this substrate at this resolution; it does not confirm or rescue Candidate B's equinox hypothesis; and it does not generalize to other populations, windows, or anchor configurations not pre-registered here.

## §12.4 Granularity caveat (verbatim)

The four-class verdict map compares the median PSS across the 365-anchor surface at two different temporal resolutions: ≈ 30.4 days per phase for k = 12 and ≈ 36.5 days per phase for k = 10. Median PSS is interpretable as "typical phase-structure for this bucket count" rather than "phase-structure at a specific anchor configuration." The locked decision rules are methodologically valid as pre-registered, but the interpretation of every verdict class must acknowledge that the comparison is between two different temporal resolutions, not a test of which resolution is "correct" in any absolute sense:

* A 12-privileged or 10-privileged verdict reflects which resolution better organizes long/short allocation on this substrate under the anchor surface, not which bucket count is structurally correct in any absolute sense.
* A Tied / both-structured verdict reflects that both resolutions are individually non-random and cannot be distinguished from each other under the comparison threshold, not that the underlying signal is resolution-independent.
* A Non-confirmatory / unresolved verdict does not adjudicate the resolution question at all; it states that the pre-registered decision rules do not separate the alternatives under the locked threshold structure.

This caveat applies to all four verdict classes.

## §12.5 Compound-verdict disclosure (verbatim)

The four beat counts that drive the verdict are coupled. They are derived from the same shared pool of 10,000 pooled-population is_long permutations. The verdict classes are pre-registered decision rules under that joint distribution, not independent p-value claims. The false-positive interpretation of a class assignment is therefore not identical to the false-positive rate of a single independent test at the 95th percentile, and the four classes do not partition probability mass uniformly under the null.

## §13 Data-contact disclosure (verbatim)

Candidate C's verdict is conditional on a previously contacted, audit-frozen pullback-event population. The pullback Phase 1–3b series for SPY and the Phase 3b 2005–2022 series for SPY/EFA/EEM/GLD/TLT were inspected, partitioned, and used to estimate within-population statistics during pullback research before Coherent Numbers contacted them. The pullback BacktestParams were locked early at pullback commit 50ee2d1 and not re-tuned, which limits but does not eliminate that prior exposure. Candidate B previously applied 12-phase March-20-anchored machinery to this same population — specifically a 10,000-element unstratified label-permutation null (§10.1 of docs/candidate_b_design_memo_v0.1.md) and an exhaustive 365-DOY anchor-control null (§10.2) — and reported the resulting verdict in results/candidate_b_results_20260514_231323_c1982503.json. Candidate C applies parallel 12-phase and 10-phase machinery to the same population under symmetrical anchor-surface rules. Candidate C's verdict is therefore conditional on (i) the pullback program's prior contact with the underlying series, and (ii) Candidate B's prior contact with the pooled Phase 3b population under 12-phase machinery. OOS 2023+ remains sealed in both repos and is out of scope for Candidate C. This disclosure is required wording; a hash citation alone does not satisfy it.
