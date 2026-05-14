# Coherent Numbers v0.2 Cell-Selection Decision Memo

**Status:** draft for review
**Scope:** selects the next v0.2 Microscope Program cell; does **not** design any selected cell.
**Repos referenced:** Coherent Numbers (this repo), pullback research (`/Users/jay/pullback_research`, separate audit chain).

---

## 1. Title

Coherent Numbers v0.2 Cell-Selection Decision Memo.

## 2. Decision question

Which v0.2 Microscope Program cell should be selected next?

- **Option A** — BTC continuous-return harmonic-calendar cell.
- **Option B** — pullback × harmonic-calendar modulation.
- **Option C** — pause; no new cell.

This memo selects among A, B, and C. It does not specify the internal design of any selected cell.

## 3. Prior uncertainty

Before today, Candidate B was not selectable, not because it was substantively weak, but because its substrate lived outside this repo in a separate audit chain. The following were unresolved:

- where the pullback research repo physically lived;
- whether that repo's audit chain was intact and linear;
- which pullback trade population was canonical, and where the file lived;
- whether the locked instrument parameters had drifted across later phases;
- whether the OOS 2023+ seal was still intact;
- whether a Coherent Numbers cell could ingest a pullback population as frozen raw data without requiring any re-run, modification, or coupling to the pullback repo.

Because those questions were open, B was held back as ineligible and the v0.2 selection had defaulted toward A or C.

## 4. New information from pullback inventory

A read-only inventory of the pullback repo has been completed. Relevant findings:

- **Pullback repo path:** `/Users/jay/pullback_research`.
- **Pullback repo HEAD:** `eac925c` (Phase 8 continuation memo).
- **Pullback repo working tree:** clean at time of inventory.
- **Locked BacktestParams:** `src/backtest.py:37–66`, locked at commit `50ee2d1` ("Phase 2 close"), unchanged across all later phases.
- **Canonical SPY 301-trade population:** `runs/20260505_152451/trades.csv` (declared canonical by the pullback `research_log.md`; a hash twin exists at `runs/20260505_151635/trades.csv` from an earlier in-memory-yfinance representation and is documented in the research log).
- **Phase 3b 5-asset populations** are present for SPY, EFA, EEM, GLD, and TLT, produced under identical `BacktestParams` defaults at commit `7806a6d` over a common 2005-01-01 – 2022-12-31 window.
- **Phase 3b summary commit `665a557` exists** in the pullback audit chain and contains the directional/allocation finding.
- **OOS 2023+ remains sealed.** Every Phase 1–3b data file ends at or before 2022-12-30. Later phases install loaders that hard-error on post-2022 rows.
- **The pullback repo and Coherent Numbers are separate audit chains.** Importing a pullback population into Coherent Numbers does not require any modification to the pullback repo.
- **No new pullback run is required** to obtain the population that Candidate B would test against.

The auditability uncertainty that previously made B ineligible is resolved.

## 5. Evaluation of Option A — BTC continuous-return harmonic-calendar cell

Option A is structurally valid. BTC continuous-return data is accessible, and the harmonic-calendar lens has already been applied at the cell level to SPY and GLD in this repo. A BTC cell would extend the same lens to a third underlying.

However, the marginal information value of A at this moment is lower than B for two reasons:

- A is another continuous-return harmonic-calendar test, of the same lens family already covered by SPY and GLD. It mostly broadens the existing lens-on-returns axis.
- A does not engage the cross-program opportunity that the pullback inventory has just opened. Until the pullback inventory had been completed, that opportunity was unavailable; now it is.

A is not dismissed. It remains a defensible later cell. It is simply not the highest-value next cell given the current state of the program.

## 6. Evaluation of Option B — pullback × harmonic-calendar modulation

Option B is now structurally feasible. Specifically:

- The pullback substrate exists as a frozen artifact in `/Users/jay/pullback_research`.
- The canonical pullback population can be ingested into Coherent Numbers as frozen raw data without re-running any pullback research.
- The pullback audit chain is intact and unchanged across Phases 1–3b.
- The pullback repo can remain untouched; the Coherent Numbers freeze is a one-direction import.
- Phase 3b provides a substantive constraint that B's design memo must weigh: the pullback project's directional random-baseline tests did not pass on any asset, while the primary Phase 3b edge appeared at the long/short allocation level versus a 50/50 random baseline.

The value of B is not to re-discover the pullback signal. Phase 1–3b already characterized the pullback population on its own audit chain. The value of B is **testing whether a harmonic-calendar lens explains heterogeneity inside an already-existing, audit-frozen pullback-event population.** That is a question Coherent Numbers is positioned to ask and the pullback project is not.

Candidate B is now eligible for selection. **It is not yet authorized for analysis.** Eligibility means: the substrate is reachable and the audit conditions for a future cell are satisfiable. Authorization for analysis would require a separate, locked Candidate B design memo.

## 7. Evaluation of Option C — pause / no new cell

Option C remains defensible. The pullback inventory itself created a natural pause and resolved the largest open uncertainty without committing to a new cell. A researcher who wants to consolidate before opening another cell is not acting incorrectly.

However, the specific reason C was load-bearing — namely, that B was structurally blocked — no longer applies. C is now a preference, not a default. If the project elects C, it is electing a deliberate pause, not deferring an undecidable selection.

## 8. Decision

**Selected: Option B**, as the next v0.2 Microscope Program cell.

The selection is bounded:

- **B is selected for preparation and design, not for immediate analysis.**
- The selection authorizes a freeze / preparation step (importing the pullback population into Coherent Numbers as frozen raw data). It does **not** authorize computing harmonic-calendar features against pullback entry dates.
- The design memo for B must lock the protocol — population scope, schema, lens, comparator, success criterion, disclosure language — **before** any calendar-feature join is performed.

Central sentence:

> Candidate B is selected as the next v0.2 cell, but only as a design-and-freeze sequence; no harmonic-calendar features may be computed against pullback entry dates until the Candidate B design memo is locked.

## 9. Immediate next artifact after decision

The next artifact is either the pullback-population freeze inside Coherent Numbers, or a freeze plan, depending on which sequencing the project prefers. Two defensible sequencings exist:

- **Sequence 1: Freeze-then-design.**
  v0.2 decision memo → freeze all candidate-relevant pullback populations into Coherent Numbers (six populations total: SPY 301 base, plus Phase 3b SPY/EFA/EEM/GLD/TLT) → Candidate B design memo, which then selects from already-frozen artifacts.
  *Strength:* the design memo operates against hashes that already exist in this repo; population scope is a selection from a known set.
  *Cost:* may freeze data that the eventual design memo does not use.

- **Sequence 2: Design-then-freeze-only-what-is-needed.**
  v0.2 decision memo → Candidate B design memo locks scope (population, schema, lens, comparator) → freeze only the populations the locked design requires.
  *Strength:* freeze commit is minimal and exactly aligned to the locked design.
  *Cost:* the design memo locks scope without the corresponding artifacts yet present in this repo; reproducibility hashes are referenced rather than committed at design-lock time.

This memo does not choose between Sequence 1 and Sequence 2. The choice is a practical sequencing question for the Candidate B design memo or its immediately preceding planning note, not a v0.2 selection question.

Whichever sequencing is chosen, the following preconditions apply:

- **The pullback repo remains untouched.** No commits, no edits, no re-runs, no exports written back into `/Users/jay/pullback_research`.
- **The freeze commit, when it happens, must be clean.** It must contain only the imported pullback artifacts and a provenance manifest. It must not contain unrelated README revisions, exploratory notebooks, oscillator images, `.DS_Store` files, or root-level legacy oscillator CSVs that may exist in the current Coherent Numbers working tree.
- **The Coherent Numbers working tree must be cleaned or quarantined before any freeze commit.** Working-tree hygiene is a precondition for the freeze, not a step inside it.

## 10. Open design questions to be resolved in the Candidate B design memo

The following are explicitly **not** decided here. They are the design surface of Candidate B and belong in B's own design memo:

- **Population scope:** SPY 301 base only; Phase 3b 5-asset universe only; both; or a defined subset.
- **Canonical SPY artifact:** use `runs/20260505_152451/trades.csv` as the SPY 301 canonical (consistent with the pullback `research_log.md`), while documenting the existence of the hash twin `runs/20260505_151635/trades.csv`.
- **Schema reconciliation:** the SPY 301 base population uses a 21-column long-form trade schema; the five Phase 3b populations use an 11-column compact schema. A reconciled common schema must be defined before any join.
- **Calendar lens definition:** the harmonic-calendar lens used in B must be specified at design lock — base (e.g., 12-phase), anchor date, phase boundaries, leap-year handling, time-zone convention — and must be the same lens family already deployed in the SPY and GLD harmonic-calendar cells unless the design memo justifies a deviation.
- **Timing of the calendar join:** the design memo must lock the join specification **before** `entry_date` is mapped to any harmonic-calendar phase. No probing joins.
- **Primary outcome:** the design memo must explicitly decide whether the primary outcome is allocation-flavored, timing-flavored, or another pre-specified construct, while accounting for Phase 3b's finding that the observed edge appeared primarily at the allocation level rather than within-direction timing. The exact primary outcome (e.g., per-phase long-share, per-phase signed r-multiple, per-phase allocation expectancy) is for the design memo.
- **Pooling decision:** if multi-asset, whether results are pooled, asset-stratified, or both — and which is primary versus diagnostic.
- **Comparator / null construction:** how the calendar-conditional distribution is compared against an appropriate null. This must be matched (same population, same selection, same friction model) — not against an external benchmark.
- **Controls:** what is held fixed (e.g., regime, direction, asset) when reading the calendar conditional.
- **Success criterion / verdict map:** what threshold under what statistic counts as a confirmatory, informative-fail, or non-confirmatory verdict, pre-registered before any computation.
- **Data-contact disclosure language:** the exact language inherited into B's verdict (see §11).

The list is non-exhaustive; the design memo is responsible for completeness.

## 11. Required data-contact disclosure precondition

Candidate B inherits prior data contact from the pullback research program. This is a load-bearing precondition for B and must be explicitly named in B's design memo and carried through to B's verdict.

The pullback event population was **not pristine** at the time Coherent Numbers contacts it. It was produced through Phases 1–3b of pullback research, during which the underlying SPY 2000–2022 series, and the Phase 3b 2005–2022 series for SPY/EFA/EEM/GLD/TLT, were repeatedly inspected, partitioned, and used to estimate within-population statistics. The pullback `BacktestParams` were locked early (`50ee2d1`) and were not re-tuned, which limits but does not eliminate this exposure.

Candidate B can still be a valid cell. Its verdict must be interpreted as **conditional on a previously contacted, audit-frozen population**. The disclosure is required wording in B's design memo and in B's verdict; it is not optional and is not satisfied by a hash citation alone.

OOS 2023+ remains sealed in the pullback repo. B may not breach that seal. If B wants to make any OOS claim, it must define its own OOS protocol and acquire its own data outside the pullback repo; that decision belongs in B's design memo and is not authorized here.

## 12. Guardrails

The following guardrails apply from the moment this memo is adopted until B's design memo is locked:

- No modifications to the pullback repo, in any form.
- No re-running of pullback research, partial or full.
- No OOS 2023+ access in either repo.
- No freeze commit in Coherent Numbers until the working-tree hygiene issue is handled (unrelated modified and untracked files must be addressed first).
- No inclusion of unrelated files in the freeze commit — README revisions, exploratory notebooks, oscillator imagery, `.DS_Store`, or root-level legacy oscillator CSVs must be excluded.
- No harmonic-calendar features computed against pullback `entry_date` before design lock.
- No phase-distribution sanity checks, histograms, or "preview" joins before design lock. A preview is a computation.
- No interpretation of B's eventual results as an independent discovery or re-discovery of the pullback signal. B tests **conditional modulation** of a pre-existing, audit-frozen pullback-event population by a harmonic-calendar lens. The pullback signal is the substrate, not the finding.

## 13. Final state

- **v0.2 selects Option B.**
- The auditability uncertainty that previously blocked B has been resolved by the pullback inventory.
- Candidate B is structurally feasible.
- Candidate B is not yet designed.
- Candidate B is not yet authorized for analysis.
- The pullback repo is untouched and will remain untouched.
- OOS 2023+ remains sealed in both repos.
- The next concrete step is a clean preparation/freeze sequence inside Coherent Numbers, with working-tree hygiene handled first, and either Sequence 1 (freeze-then-design) or Sequence 2 (design-then-freeze-only-what-is-needed) chosen as a practical sequencing decision adjacent to — not inside — this memo.

— end of memo —
