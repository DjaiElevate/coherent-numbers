# Candidate C Framework Memo — v0.1

**Working title:** Candidate C — Second-Digit Duodecimal Annual Structure
**Version:** v0.1 (Framework / cell-selection starter)
**Date:** 2026-05-15
**Project:** Coherent Numbers
**Status:** Framework only. No protocol locked. No data contact authorized.

**Reference commits (Candidate B audit chain, for inheritance only — not subject to revision here):**
- Design memo (locked): `1e9a3e6`
- Lock-acceptance: `159cccd`
- Freeze: `5225bfd`
- Implementation + tests: `e9961dd`
- Verdict log: `7a88833`
- Closure memo: `df09aa8`

---

## 1. What this memo is, and what it is not

This memo is the **first Candidate C artifact** in the audit chain. Its role is to scope a candidate research question, surface design problems, compare alternatives, and recommend whether Candidate C should be developed into a full design memo later.

It is explicitly **not**:

- A locked design memo. No protocol parameters, thresholds, seeds, anchors, or run rules are decided here.
- An authorization for any data contact. No frozen CSVs, no `entry_date` joins, no preview joins.
- A commitment to nested-duodecimal as the eventual primary design. The framing is open until a design memo, if one is later drafted, locks it.
- A rescue, reframe, or amendment of Candidate B. Candidate B closed as Split-null per `docs/candidate_b_closure_memo_v0.1.md`; that verdict stands.

If Candidate C is selected after this memo, the next artifact would be a separate locked design memo analogous to `docs/candidate_b_design_memo_v0.1.md`, with its own lock-acceptance and its own audit chain.

## 2. Starting question

> Does the second duodecimal digit of annual position carry additional long/short allocation information beyond the first duodecimal digit already tested in Candidate B?

Operationally: if every trade's `entry_date` is mapped to a pair (outer phase, inner subphase) where outer is the first duodecimal digit of annual position and inner is the second, does inner subphase carry information about `is_long` after the outer-phase information is preserved?

The question is statistical and neutral. It does not assume that any anchor in particular is privileged, that the duodecimal grid is uniquely correct, or that any observed pattern reflects a calendar-causal mechanism.

## 3. Why this follows from Candidate B

Candidate B's locked verdict is **Split-null**:

- **N.1 (unstratified label-permutation null) passed maximally** (10,000/10,000). Under the locked March-20 12-sector partition, the pooled Phase 3b 1,282-trade population's long-share is far from what unconditional random labeling would produce.
- **N.2 (exhaustive 365-DOY anchor-control null) failed** (107/365, strict percentile 0.2932 against threshold 0.95). The locked March-20 anchor is not specially distinguished against the integer-DOY anchor population; many other anchors produce comparable or higher `PSS_B1` on the same data.

The N.2 texture in `docs/candidate_b_closure_memo_v0.1.md` §5.5 shows the strongest anchors scattered across all four quarters of the year, with no clustering near DOY 79. This is consistent with **broad-band annual structure** rather than anchor-specific structure.

Two open questions follow naturally:

- **Q1.** Is the broad-band annual structure entirely captured by a coarse ≈ 30-day outer partition, or does finer within-outer-phase structure also exist?
- **Q2.** If finer structure exists, is it duodecimal (12 within 12) — or is the choice of 12 within 12 itself just one of many compatible bucket counts?

Candidate C as framed targets Q1, specifically under the duodecimal framing. Q2 is closer to the bucket-count-comparison alternative in §9.2 below.

## 4. What Candidate C is not

- **Not a rescue of Candidate B.** Candidate B's Split-null verdict is final and is not amended by anything in this memo or anything Candidate C eventually produces. A Confirmatory Candidate C verdict would not retroactively upgrade Candidate B.
- **Not a rerun of Candidate B** with a different lens. The primary question is structurally distinct — inner-given-outer dispersion is not what N.1 measured.
- **Not proof that 12 is sacred.** Selecting 12 × 12 as a candidate primary design is a research-program choice, not an empirical entailment. The bucket-count alternative (§9.2) is the right check on that choice.
- **Not a flat 144-bucket fishing scan.** A naïve 144-way ANOVA on the 1,282-trade pool would average ≈ 9 trades per cell and would be statistically untrustworthy under either null.
- **Not a neighbor-influence / "Influential Numbers" primary test.** See §8.
- **Not a trading-edge, profit, or allocation-optimization study.** Outcomes here would be statistical descriptions of a frozen historical event population, not signals for future use.
- **Not an OOS 2023+ contact.** The OOS seal in both repos continues to hold.

## 5. Candidate primary design shape (sketch only — not locked)

The design space currently under consideration is a **nested variance-decomposition / second-digit test**, sketched below. Concrete parameter values are deliberately omitted; the design memo, if one is later drafted, is where they would be locked.

### 5.1 Phase grid

- **Outer phase** `p ∈ {0..11}` — first duodecimal digit of annual position. A natural starting choice is the same March-20-anchored annual-sector formula used in Candidate B §7.1, but the anchor question is open (§6.3).
- **Inner subphase** `q ∈ {0..11}` — second duodecimal digit, indexing the sub-position of the trade within its outer phase. Natural starting choice: each outer phase has length ≈ `cycle_length_days / 12`; inner subphase divides that span into 12 sub-sectors. The exact formula is a design-memo decision.

### 5.2 Decomposition idiom

Total phase-conditional long-share variance can be decomposed as:

```
total_variance_of_is_long ≈ between_outer + within_outer
within_outer              ≈ between_inner_given_outer + within_inner_given_outer
```

Candidate B's `PSS_B1` is broadly the `between_outer / total` ratio under the η² family. Candidate C's primary statistic candidate is the **conditional component** `between_inner_given_outer / something`, specifically isolating information added by the second digit after the first is fixed.

A starting sketch (illustrative, not locked):

```
between_inner_given_outer
  = Σ_p (N_p / N_total)
    × Σ_q (N_{p,q} / N_p) × (share_{p,q} − share_p)²
```

with a `total_within_outer` denominator that normalizes appropriately for the within-outer marginal. The framework memo does not pre-decide whether the normalization is the within-outer Bernoulli variance (a per-outer-phase analog of `total_B1`), the pooled `share_pooled × (1 − share_pooled)`, or another η²-family choice. That choice is a design-memo decision.

### 5.3 Null shape

The natural primary null under this idiom is **label permutation within each outer phase** — for each `p`, shuffle `is_long` only among trades in outer phase `p`, holding outer-phase membership and `share_p` fixed. This breaks inner structure while preserving outer structure. An aggregated statistic across outer phases yields a single primary test rather than 12 separate per-outer-phase primaries.

The anchor-control analog is open. See §6.3.

### 5.4 Why aggregation is important

Running 12 independent per-outer-phase tests creates a multiple-comparisons problem (§6.2). An aggregated statistic over all outer phases collapses 12 tests into one and matches the §10.1-style discipline of B's primary null. If per-outer-phase results are also reported, they live in the diagnostics tier and cannot enter the verdict.

## 6. Main methodological problems

Six problems must be surfaced and resolved before any design memo is drafted. None are fatal; all need explicit handling.

### 6.1 Sample mass / sparse 144 cells

On the pooled Phase 3b 1,282-trade population, 144 cells average ≈ 8.9 trades per cell. The actual distribution will be heavier-tailed because outer-phase occupancy already ranges 84..145 (B closure §5.4); inner cells with very few trades will be common, some may be empty, and per-cell long-share estimates will be high-variance.

The aggregated statistic of §5.4 mitigates this on the verdict path. Per-cell diagnostics will need explicit minimum-N gates and explicit non-rescue language.

### 6.2 Multiple comparisons

A naïve "test each of 12 outer phases independently" approach triggers a 12-way multiple-comparisons problem. The aggregated statistic is the principled response. Any per-outer-phase tests should be in the diagnostics tier with explicit non-rescue handling, analogous to Candidate B's secondary outcomes under §12.3.

### 6.3 Anchor-control complexity

In Candidate B, anchor enumeration was one-dimensional (365 integer DOYs for the outer anchor). In a nested design, the anchor-control surface has at least two dimensions:

- **Outer anchor:** the first-digit anchor — 365 integer DOYs, analogous to B's N.2.
- **Inner anchor:** the phase of the inner partition relative to the outer phase boundary — a starting choice is "inner phase 0 begins at the outer phase boundary", but the design could in principle vary this offset.

This raises three design questions that must be settled before lock:

1. Whether the inner anchor varies at all in the control, or is fixed to "aligned with outer".
2. If inner anchor varies, whether the joint outer × inner anchor space is enumerated exhaustively (e.g., 365 × 12 = 4,380 controls) or only along a marginal axis.
3. Whether the §10.2 v0.3.3 exhaustive-enumeration discipline can be preserved as the control population size grows, or whether a different finite-control framing is required.

This is the most genuinely difficult design problem and the one most likely to delay or prevent a clean lock.

### 6.4 Same-population vs fresh-population trade-off

Two substrate options exist:

- **Same Phase 3b 1,282-trade pool** (already frozen at `5225bfd`). Pro: zero new freeze work, audit-friendly. Con: inherited data contact from Candidate B and from pullback Phases 1–3b. B's N.1 specifically characterized the pooled outer-phase long-share dispersion under the locked outer partition; any test that conditions on outer phase therefore inherits that contact and must be interpreted accordingly.
- **Fresh population.** Could be a different audit-frozen pullback population (no such artifact currently exists in Coherent Numbers), a fresh event population on different assets or windows, or an OOS extension (sealed in both repos and out of scope here). Pro: cleaner inferential standing. Con: substantial new freeze and design work; OOS contact requires its own protocol design and is not authorized.

The framework memo does not pick. The design memo, if one is drafted, must.

### 6.5 Inherited data contact

Beyond §6.4, two layers of contact already apply to the Phase 3b pool:

- The pullback research program contacted these series during Phases 1–3b for direction/allocation estimation (`docs/cell_selection_decision_memo_v0.2.md` §4; B design memo §13).
- Candidate B contacted the pooled population under the March-20 outer partition during its N.1 (B closure §3).

A nested-duodecimal test that conditions on outer-phase under the same anchor on the same data is not an independent test of within-outer structure. The design memo must carry a Candidate-C-specific data-contact disclosure and must reason carefully about what "conditional on outer" means inferentially when the outer marginal has already been characterized.

### 6.6 Duodecimal nesting vs arbitrary multi-scale partitioning

Choosing 12 × 12 = 144 is a program-aesthetic choice as much as a statistical one. Other nestings exist — 6 × 12, 12 × 6, 4 × 12, 12 × 4, 24 × 6, and non-nested alternatives such as continuous frequency decomposition. The framework should be honest that the duodecimal nesting is a specific candidate framing, not the unique one. The bucket-count-comparison alternative in §9.2 is the natural check on this choice; the design memo, if drafted, should engage with why 12 × 12 is the preferred starting framing despite alternatives.

## 7. Possible outcome map

Pre-registered for inclusion in a future design memo, but illustrative here.

| Outcome | Interpretation (under a properly locked Candidate C) |
|---|---|
| **Inner-given-outer Confirmatory** | Evidence for nested/multi-scale annual structure within the outer-phase partition. Does not retroactively confirm Candidate B's equinox-anchor hypothesis. Does not establish duodecimal nesting as uniquely correct; alternative bucket-count nestings would need their own tests. |
| **Inner-given-outer Split-null** | Informative texture under whichever null partially rejects. Per the locked verdict-map idiom (analogous to B §12.3), not Confirmatory, not a rescue, not a redesign trigger. |
| **Inner-given-outer Non-confirmatory** | B's broad-band annual structure is plausibly explained by the outer (≈ 30-day) partition alone, with no detectable additional inner structure at the duodecimal scale. A constraint, not a rescue invitation. |
| **Diagnostic neighbor smoothness appears** | Texture that adjacent inner sub-phases may show related behavior. Not primary evidence here; in a later, separately scoped cell, could motivate an "Influential Numbers" diagnostic test (§8). |
| **Everything disappears** | All four outcomes above null. A useful constraint on the duodecimal-nesting hypothesis on this substrate; no rescue. |

Every entry in this table assumes the design memo, if drafted, carries forward Candidate B's no-rescue clauses, the §10.2 exhaustive-enumeration discipline, the §13 data-contact disclosure pattern, and the §14 deterministic-reproducibility requirement.

## 8. Relation to Influential Numbers

The "Influential Numbers" intuition — that numbers/positions may be relational, that neighbouring positions may interact — is a useful **motivation** for asking the second-digit question. It is **not** offered as a metaphysical premise and is **not** primary evidence here.

The empirical translation that is permissible to test is narrow:

> "Adjacent or nested phase positions may show related long/short allocation behavior under a locked duodecimal phase-space model."

The framework memo treats this translation as:

- **Permitted as motivation in the design memo's background section.**
- **Permitted as a diagnostic in a future cell**, separately scoped and locked, if Candidate C's primary verdict warrants it. A neighbor-smoothness diagnostic (e.g., expected difference between `share_{p, q}` and `share_{p, q ± 1}` under a permutation null) is a candidate, but its statistical machinery is genuinely different from the second-digit test sketched in §5.
- **Not permitted as a co-primary outcome in Candidate C** unless a future design memo separately justifies that elevation. The locked design must have one primary lens family per cell, consistent with prior-cell discipline.

Statistics on phase-position neighbour behavior do not warrant metaphysical conclusions. The closure memo for any cell that addresses this must carry that disclaimer explicitly.

## 9. Candidate C versus alternatives

Five alternative continuations are on the table. They answer different questions; the framework memo does not pick.

### 9.1 Direct anchor-space investigation

Aim: characterize the broad-band anchor structure Candidate B uncovered — why does the N.2 anchor distribution have mean `0.035`, stdev `0.006`, and a 273-day-spanning top-10? Are the strongest anchors associated with any external regularity (volatility seasonality, calendar reporting, payroll, options expirations)?

- **Question answered:** "What is the structure of the broad-band annual signal, irrespective of duodecimal framing?"
- **Strength:** directly engages B's finding.
- **Cost:** moves away from the duodecimal program aesthetic; risks becoming open-ended.

### 9.2 Bucket-count comparison

Aim: parallel locked tests across multiple outer-partition bucket counts — e.g., 6, 8, 10, 12, 18, 24 — under matched protocol discipline.

- **Question answered:** "Is 12 privileged at all?"
- **Strength:** directly tests the duodecimal-program assumption that 12 is special.
- **Cost:** requires N comparable lock-acceptance runs; multiple-comparisons discipline at the cell level; inferential framing of "which bucket count wins" must be pre-registered.

**This is a genuinely different question from Candidate C's nested-duodecimal framing.** Nested-duodecimal tests whether 12 repeats inside itself as multi-scale structure. Bucket-count comparison tests whether 12 is privileged at all. The framework memo does not assume the answer to "is 12 privileged?" by selecting nested-duodecimal as the next cell — it merely chooses to engage one question at a time, and the program's stated aesthetic is duodecimal. If we want neutrality on bucket count, this alternative is the right next cell. If we want depth on the duodecimal aesthetic, Candidate C as sketched is the right one. The two are not substitutes.

### 9.3 Fresh population replication

Aim: re-run B's locked protocol (or a comparable locked protocol) on a fresh, audit-frozen event population that has not been contacted by the pullback research program.

- **Question answered:** "Does B's finding hold under data-contact-clean conditions?"
- **Strength:** addresses the §6.5 inherited-contact concern more cleanly than any conditional analysis can.
- **Cost:** depends on whether a suitable fresh population exists, can be acquired, and can be audit-frozen under Coherent Numbers' discipline.

### 9.4 Continuous-frequency / spectral approach

Aim: replace the bucket lens with a Fourier/wavelet/Lomb-Scargle decomposition of phase-conditional long-share over the year.

- **Question answered:** "What annual frequencies, if any, carry the long-share signal? Is the signal concentrated at one or a few periods, or broadband?"
- **Strength:** lens-family-neutral; engages the broad-band anchor finding without committing to any bucket count or anchor.
- **Cost:** entirely new statistical machinery, distinct from the PSS/η² family; a new protocol-lock template would be needed.

### 9.5 Pause / integration

Aim: hold position. Document Candidate B's findings publicly, integrate the SPY MVT and GLD closures alongside, and let the next-cell selection wait until external constraints (calendar, attention, data availability) settle.

- **Question answered:** "What does the atlas-so-far say, and what do we want to learn next?"
- **Strength:** matches the cell-selection memo's posture that pause is a defensible option.
- **Cost:** opportunity cost only; nothing closes.

## 10. Recommendation

The framework memo's recommendation is:

> **Candidate C as sketched is worth developing into a design memo, but only after five narrowing decisions are made explicitly. Until those decisions are recorded in writing — either in a follow-on framework artifact or in the design memo's preamble — Candidate C remains at framework-only status and no implementation, freeze, or run is authorized.**

The five narrowing decisions:

1. **Question alignment.** Whether the goal is "does the duodecimal framing nest inside itself?" (Candidate C as sketched) or "is the bucket count of 12 privileged at all?" (bucket-count alternative in §9.2). These are different questions, and the design memo must commit to one.
2. **Substrate.** Whether to reuse the Phase 3b 1,282-trade frozen pool (inherited data contact) or to scope a fresh population (§6.4 / §9.3). If reuse, the data-contact disclosure must be explicitly carried forward and strengthened to acknowledge B's outer-phase contact in addition to pullback's series contact.
3. **Anchor-control surface.** Whether outer anchor varies, inner anchor varies, or both — and whether the exhaustive-enumeration discipline can be preserved at the resulting control-population size (§6.3). This is the design problem most likely to gate progress.
4. **Primary statistic normalization.** Which `total_within_outer`-style denominator is locked for the conditional η² (§5.2). The choice has rank-invariance implications under the chosen null and must be pre-registered.
5. **Diagnostic tier discipline.** Whether per-outer-phase tests and the "Influential Numbers" neighbor-smoothness diagnostic appear at all, and if so under what non-rescue clauses (§7, §8).

If, after addressing these five, the design memo can be drafted with the same audit cleanliness as Candidate B's, Candidate C is a defensible next cell. If any of the five cannot be cleanly resolved — particularly §6.3 — the right move is to pivot to one of the §9 alternatives or to pause (§9.5) rather than lock a protocol that papers over a methodological hole.

The framework memo does not commit. The next decision belongs to a separate selection step.

— end of framework memo —
