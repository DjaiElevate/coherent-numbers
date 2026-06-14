# Compression Lane — Stage-1 Design Memo v0.1 (DRAFT; no data contact)

**DRAFT ONLY. No design rules are frozen until owner review and explicit acceptance. No data contact, audit, gate, sandbox run, sealed access, or alpha spend is authorized by this memo.**

---

## 1. Anchors and current state

- **Current HEAD:** `0a006844e37d0bb5da3227884638ecce13adfcea`
- **Compression decision memo:** `docs/market_force_atlas_second_promotion_decision_compression_v0_1.md`
- **Compression decision SHA-256:** `389798b8ce7cdcb7533645fb190fa3270a46fe4f84149d09d834c3bc3c530660`
- **Atlas amendment / current atlas SHA-256:** `c44c3b3f1bed648fdc5c02192b6ea62cbae4d8439267d17b34d50ca58fd8bd31`
- **Shock status:** `INFEASIBLE — matched design, SPY 2005–2022`
- **Active lane count:** **zero** until this Stage-1 design is explicitly accepted.

**Prior-art note.** The Market Force Atlas carries a Compression *concept card* (VOLATILITY cluster, rep = trailing realized vol; null = "adds nothing beyond low trailing vol"; confound = "definitionally the inverse of vol level"). That card is a **concept stub, not a result**. It is treated here as prior-art framing requiring fresh review — its draft choices are **not inherited as evidence and authorize nothing.**

---

## 2. Decision boundary

- Compression has been selected as the **next Stage-1 design candidate** (second-promotion decision, pushed at `0a00684`).
- **This memo is not a Shock rescue.**
- A distributional / regression-based Shock-wake lane **remains possible in the future, but is not selected here.**
- **No test, audit, gate, data contact, sealed access, or alpha spend is authorized.**
- This memo **drafts a possible instrument only.**

---

## 3. Research question

> Does a pre-declared compression state have a measurable relation to later **directionless path expansion** beyond ordinary volatility mean-reversion, bounded-floor mechanics, and autocorrelation / variance-ratio structure?

- The question is about **path behavior / force behavior.**
- It is **not** about entries, exits, breakouts, directional profit, or trading edge.

---

## 4. Primary burden (stated before any metaphor)

> The first burden of a Compression lane is not to sound like pressure-at-rest; it is to prove it is not merely ordinary volatility mean-reversion, bounded-floor mechanics, or autocorrelation / variance-ratio structure wearing a more poetic name.

The boring baselines this lane must beat:

**A. Volatility mean-reversion.**
- Low realized volatility may later normalize.
- That alone is **not** a new Compression force.

**B. Bounded-floor mechanics.**
- Volatility is autocorrelated.
- Volatility is bounded below by zero.
- Very low volatility readings are **mechanically more likely** to be followed by increases than decreases.
- That apparent expansion can be a **floor artifact, not a force.**

**C. Autocorrelation / variance-ratio structure.**
- A containment-like path measure may not be a volatility-level proxy, but it may instead be a **choppiness / mean-reversion proxy.**
- The containment-ratio candidate (rolling range ÷ rolling path length) is **adjacent to efficiency-ratio / variance-ratio / trending-vs-choppiness** measures.
- A construct distinct from trailing RV but **collinear with autocorrelation / variance-ratio is not a new Compression force.** It is a known force in a path-shape costume.

---

## 5. Definition kill-switch — two canonical baselines

Compression may **not** be defined as:
- silence / low volatility; or
- mere choppiness / mean-reversion.

The memo must argue that any proposed construct is distinct from **BOTH**:
1. trailing realized volatility / volatility level;
2. within-window return autocorrelation / variance-ratio / mean-reversion structure.

The **containment-ratio candidate** (rolling close range ÷ rolling path length) is treated carefully:
- it likely escapes being a monotone transform of trailing realized volatility;
- but it is **adjacent to** efficiency-ratio / variance-ratio / trending-vs-choppiness measures;
- therefore it may **dissolve into the AUTOCORRELATION cluster** instead of the VOLATILITY cluster.

> Compression is not silence, and it is not mere choppiness. If containment cannot be defined as something both quietness and within-window autocorrelation miss, the lane is infeasible by definition.

**If no proposed Compression construct can be argued as distinct from both baselines at the definitional level, this memo must declare the lane `INFEASIBLE-BY-DEFINITION` and stop.** The definition must not be left unresolved pending data.

### Candidate constructs to evaluate without data contact
- **containment ratio:** rolling close range ÷ rolling path length;
- **movement-without-escape:** substantial internal path movement with limited net escape;
- **serial structure of small moves:** sign alternation / mean-reverting movement inside a contained window;
- **relative range compression:** short-window range relative to a longer-horizon range, only if it can be argued not to collapse into a volatility-level proxy;
- **within-window shape measures**, only if they are not just variance or autocorrelation in disguise.

> Compression is not silence. Compression is movement without escape. If the lane cannot define containment separately from low volatility and mere choppiness, it is infeasible by definition.

### Three-level distinctness hierarchy (the bar CR must be judged against)

Distinctness is not one test but three nested levels, weakest to strongest. A construct may not be carried forward merely because it clears the weakest level.

1. **Logical non-identity (weakest).** The construct is not exactly equal to the baseline. A toy path can always demonstrate this; it proves almost nothing on its own.
2. **Analytical non-reducibility (stronger).** The construct is built from **different path functionals** and is **not reducible to the baseline by definition** — there is no definitional rewrite turning one into the other.
3. **Empirical residual survival (strongest).** The construct retains **non-trivial residual information on real SPY paths** after **joint** baseline absorption. This is the only level that licenses promotion, and it is **not** addressed at the draft stage.

**Where CR stands at this draft stage:** CR clears **levels 1 and 2** by the analytical arguments below. CR does **NOT** claim **level 3**. Empirical residual survival remains **unproven** and must be tested later by the future collinearity diagnostic (§14). Therefore CR is **not infeasible-by-definition on analytical grounds**, but it remains **high-risk for empirical absorption.**

### Why CR is analytically non-reducible (levels 1–2 argument)

The containment ratio `R = (max(close) − min(close)) over window ÷ Σ|Δclose| over window` is **bounded in (0, 1]** (net range traversal can never exceed total path length).

**Against the trailing-RV / volatility-level baseline.** Both ingredients of CR are *volatility-flavored*: the rolling **range** is scale-sensitive, and the rolling **total variation** `Σ|Δclose|` is an **L1 analog of realized volatility** (range is itself bounded by total variation). So CR does **not** escape RV because its ingredients ignore volatility — they don't.

> Both ingredients of CR are volatility-flavored: range is scale-sensitive and total variation is an L1 analog of realized volatility. CR escapes the trailing-RV baseline not because its ingredients ignore volatility, but because the ratio cancels the common volatility scale and leaves a dimensionless containment-geometry measure.

Concretely: the common volatility scale appears in both numerator and denominator and **partly cancels** in the ratio; what remains is a **dimensionless containment / path-efficiency geometry** measure, not a volatility level.

**Against the autocorrelation / variance-ratio baseline.** CR is built from **extrema and total variation** (spatial range; absolute path length; movement-without-escape). Variance-ratio / autocorrelation is built from **signed second-moment structure** (summed-return variance; autocovariances; trend / mean-reversion sign structure). These are different functionals of the path, so CR is **analytically non-reducible** to a variance ratio at the definitional level.

> Containment Ratio is more than a toy-path non-identity claim: it is built from extrema and total variation, while variance-ratio is built from signed second-moment / autocovariance structure. That gives CR a defensible analytical non-reducibility argument against the AUTOCORRELATION baseline.

**No overclaim.**

> Analytical non-reducibility is not evidence that the CR residual is large, stable, or useful on SPY. The Stage-1 draft does not claim that CR has market relevance. It claims only that CR is not infeasible-by-definition on analytical grounds. The lane may still die at the future collinearity diagnostic if CR is empirically absorbed by trailing RV, bounded-floor mechanics, variance-ratio, efficiency-ratio, or the joint baseline set.

CR remains *adjacent* to the **efficiency ratio** (directional travel ÷ path length), which is exactly where empirical absorption (level 3 failure) is most likely. That adjacency is the open question for §14, not a definitional defect.

---

## 6. Synthetic illustration boundary — non-identity is not orthogonality

Synthetic toy paths, if used, may establish **only logical non-identity**. They may show a proposed construct is not definitionally identical to (i) trailing realized volatility or (ii) within-window autocorrelation / variance-ratio. They may **NOT** be treated as evidence that the construct carries generic orthogonal information on realistic return structure.

Distinguish:
- **logical non-identity:** the construct is not mathematically identical to the baseline;
- **generic orthogonality:** the construct is expected to carry non-trivial information beyond the baseline on broad realistic path structures.

Logical non-identity is **necessary but far from sufficient.** In terms of the §5 three-level hierarchy, **toy paths reach only level 1 (logical non-identity).** They do **not** by themselves establish **level 2 (analytical non-reducibility)** — that requires the functional-form argument in §5 (extrema / total variation vs signed autocovariance; ratio-cancellation of the common volatility scale) — and they do **not** establish **level 3 (empirical residual survival)**, which only the future collinearity diagnostic on real SPY paths can address.

> A toy path proving non-identity is always available and proves almost nothing. It shows the construct is not definitionally dead; it does not show the residual survives against the baselines on real return structure. Curvature was non-identical to zigzag and still died against B6. Non-identity is the floor of the argument, not the pass.

**If the analytical argument cannot give a reason to expect generic non-trivial residual information beyond both baselines, the lane should be marked `INFEASIBLE-BY-DEFINITION` and stop.**

### Allowed synthetic use (strict limits)
- hand-specified toy paths only; no market data; no SPY data; no 2023+ data;
- no random search; no parameter sweep; no optimization; no generated-until-it-works examples;
- no outcome / wake / expansion measurement; no claim about real markets.

**Purpose:** show whether containment can be conceptually decoupled from trailing RV and variance-ratio / autocorrelation.

> Synthetic toy paths are not evidence about markets. They are only definitional counterexamples or existence checks showing whether the proposed construct is mathematically distinct enough to deserve a Stage-1 design. If the analytical argument fails, synthetic examples may not rescue the lane.

If a synthetic illustration is used, the memo must state: the toy paths explicitly; the quantities compared; what the example proves; what it does **not** prove; and why it does **not** authorize data contact, audit, gate, or alpha spend.

> Synthetic distinctness is necessary but not sufficient. It can show that a Compression construct is not definitionally identical to RV or variance-ratio, but it cannot show that the construct matters in SPY or predicts expansion.

*(This draft offers the §5 analytical non-identity reasoning in lieu of a worked toy path. Any toy path added later must obey the limits above and remains illustration, not evidence.)*

---

## 7. Definition / outcome coupling

Compression definition and expansion outcome are **coupled, not independent.** Before any data, the memo must say why the proposed definition → expansion relationship is **not mechanically guaranteed** by:
- volatility mean-reversion;
- bounded-floor mechanics;
- autocorrelation / variance-ratio structure.

- If the definition is low-volatility-like and the outcome is high-future-volatility-like, the lane reduces to: **`low volatility precedes higher volatility`** (an artifact, not a force).
- If the definition is choppiness-like and the outcome is expansion-like, the lane may reduce to a **known autocorrelation / variance-ratio relationship.**

> A Compression definition that is just low volatility paired with an expansion outcome that is just higher future volatility measures an artifact, not a force. A Compression definition that is just choppiness paired with later expansion risks measuring the AUTOCORRELATION cluster under a new name.

**Coupling hazard for the containment ratio `R`:** because `R` is low when a window oscillates without escaping, and "expansion" outcomes often coincide with later directional escape, a naive `R → escape` pairing could be partly mechanical via the same autocorrelation structure. The future design must pick an expansion outcome that is **not** the arithmetic complement of the compression definition over overlapping windows.

---

## 8. Metaphor boundary

> The metaphor may nominate a force, but it may not testify for that force. Compression must earn its meaning against the volatility baseline, bounded-floor mechanics, and autocorrelation / variance-ratio structure.

- "Pressure at rest" is a **generative metaphor only.**
- **Beautiful language is not evidence.**
- Once Stage-1 is accepted, **frozen definitions and boring baselines govern.**

---

## 9. No breakout-strategy drift

- Compression must **not** become "find quiet ranges and trade the breakout."
- Directional profit, entry/exit rules, position logic, and trading edge are **not objectives.**
- Any future outcome must be **directionless path expansion** unless a later memo explicitly justifies otherwise.
- If directional expansion is ever considered, it must be **secondary and cannot rescue the primary.**

---

## 10. Data scope for future work

Specified without opening any data:
- **SPY adjusted close only.**
- **2005–2022 sandbox only.**
- **2023+ sealed and untouched.**
- Allowed future columns: `date`, `adj_close`.
- **No** OHLC, volume, news, macro, options, or cross-asset inputs in this lane unless a future amendment explicitly reopens scope.

---

## 11. Candidate compression definition — draft, not frozen

A draft primary definition is proposed because the §5 two-sided kill-switch is **not failed at the definitional level**: per the §5 three-level hierarchy, the containment ratio clears **level 1 (logical non-identity)** and **level 2 (analytical non-reducibility)** against both baselines. The **analytical non-reducibility question is provisionally answered in favor of carrying CR forward.** The **empirical absorption / residual-size question (level 3)** is **deferred** to the future §14 collinearity diagnostic. CR is therefore carried forward strictly as **`not infeasible-by-definition`**, **not as proven useful**; it is **not** frozen and may yet be declared infeasible if it is empirically absorbed.

**Draft primary candidate — Containment Ratio (CR).**
- **Plain-English math.** Over a trailing window of `W` trading days ending at day `t` (using only adjusted closes up to `t`): let `range = max(adj_close) − min(adj_close)` over the window, and `path = Σ |adj_close_i − adj_close_{i-1}|` over the same window. Define `CR_t = range / path` (bounded in (0, 1]). A **compression state** is a low `CR` (much internal movement, little net range escape). The exact threshold is **deferred** (no post-hoc threshold selection; see §16).
- **Required rolling lookback.** One trailing window `W` (draft candidates to review: 10 / 21 trading days), strictly ending at `t`. No future data; window uses closes `≤ t` only.
- **How it avoids future data.** `CR_t` is computed from closes up to and including `t`; the expansion outcome (future window) is strictly after `t` and is never used in the definition.
- **Why not identical to trailing-RV baseline.** `CR` can be identical across windows with very different realized volatility, and very different across windows with identical realized volatility; it is a **shape** measure, not a **level** measure.
- **Why not identical to autocorrelation / variance-ratio baseline.** `CR` uses absolute path length and net range, not signed serial correlation; it is non-identical to a variance ratio. **However**, it is *adjacent* to the efficiency ratio and is therefore at **high risk** of being empirically collinear with variance-ratio structure — this is the open question for §14, not something this draft asserts is resolved.
- **Why its residual might be generically non-trivial (claim, not proof).** Containment captures "movement without escape," which can occur both in mean-reverting chop *and* in low-drift accumulation that is not strongly serially anticorrelated; if these decouple on real paths, `CR` could carry information beyond a pure variance ratio. The **analytical** non-reducibility of CR from both baselines is provisionally settled (§5, levels 1–2); what remains open is strictly the **empirical** question — whether the CR residual is large/stable enough to survive joint baseline absorption (level 3). **That empirical-residual question, not the analytical question, is what the future §14 collinearity diagnostic must answer; it is not a Stage-1 conclusion.**
- **Future-diagnostic note (do not design it now).** When the future collinearity diagnostic is designed, **absorption must mean joint / incremental absorption over the full baseline set, not merely low pairwise correlation with each baseline.** A metric can have modest pairwise correlations with each baseline individually and still be absorbed by the joint baseline model.
- **Draft pending review.** window `W`; compression threshold; whether `CR` or `1 − CR` is the natural "compression" orientation; whether to standardize `CR` cross-sectionally over time.

**Secondary/descriptive candidates (only if necessary; multiplicity warning).** "relative range compression" (short-window range ÷ long-window range) and "serial-alternation count." These are **not** promoted here; listing them creates **family/multiplicity risk** (§16) and they must not become rescue options.

*(If, on owner review, no defensible primary definition survives reasoning alone, the correct outcome is to declare `INFEASIBLE-BY-DEFINITION` rather than leave the definition unresolved.)*

---

## 12. Expansion outcome — draft, not frozen

Draft only; chosen to avoid becoming a trading signal.
- **Prefer directionless expansion.** No profit, no entry/exit, no trade P&L.
- **Candidate outcomes:** future realized volatility; future close-to-close range; future absolute path movement — all over a forward window strictly after `t`.
- Any future **primary** outcome must be chosen **before data contact or gate.**
- **Multiple horizons/outcomes are one family** with multiplicity control, not rescue options.
- **Non-mechanical-pairing requirement.** The chosen pairing must not be guaranteed by the same bounded / autocorrelated quantity: e.g., do not pair a `CR`-based compression definition with an expansion outcome computed on an overlapping window or that is `CR`'s arithmetic complement. Forward window must not overlap the definition window.

---

## 13. Canonical baselines

The future design must include **at least**:
- trailing realized volatility / volatility mean-reversion baseline;
- bounded-floor mechanics baseline;
- naive low-volatility state baseline;
- within-window return autocorrelation baseline;
- variance-ratio / efficiency-ratio style baseline;
- persistence / clustering baseline (if compression episodes persist).

**Compression only earns meaning if it adds something beyond all of these.**

---

## 14. Required future collinearity diagnostic (before the episode-count audit)

Named as a required future artifact only; **not designed in detail here.**

**Required future order:**
1. Stage-1 draft design memo *(this file)*.
2. Stage-1 owner review / acceptance.
3. Pre-gate **collinearity diagnostic** against canonical baselines.
4. Pre-gate **distinct-episode feasibility/count audit.**
5. Stage-2 literal freeze **if diagnostics are adequate.**
6. Sandbox gate **only after** Stage-2 freeze and explicit authorization.
7. Sealed data **only under separate atlas authorization.**

The collinearity diagnostic is **future explicit authorization only.** It must be **event-side / feature-side only**: no wake; no expansion outcome; no forward realized volatility; no future target; no gate; no alpha spend; no sealed data.

**Purpose:** determine whether the proposed Compression metric is **empirically absorbed** by trailing realized volatility; bounded-floor / low-vol mechanics; within-window autocorrelation; variance-ratio / efficiency-ratio measures. If too collinear, the lane **stops before episode counting.**

> Episode counting is only meaningful after the Compression metric survives a pre-gate collinearity diagnostic. Counting episodes for a metric already absorbed by its baselines is wasted motion.

---

## 15. Required future feasibility/count audit (after collinearity; before any gate design)

- A pre-gate feasibility/count audit must happen **before any Compression gate is designed or run.**
- It must count **distinct independent compression episodes, not just calendar days.**
- Compression regimes can persist for **weeks or months.**
- **Calendar-day counts may overstate independent observations.**
- The audit must assess **clustering / persistence / episode independence.**
- The audit must **not** compute wake/outcome.
- The audit must **not** inspect expansion results.
- If independent episodes are too few, the lane may become **`INFEASIBLE`**, like Shock's matched design.
- **This memo does not authorize that audit yet.**

### Draft episode-counting concept (not frozen)
- contiguous compression days should likely **collapse into one episode**;
- a **cooldown / refractory rule** may be needed between episodes;
- **minimum independent-episode floors must be owner-set before any audit**;
- **do not let observed episode counts suggest the floor.**

### Episode-independence parameters must be pre-justified, not feasibility-tuned
The future episode-count audit must pre-justify: the episode-collapsing rule; the cooldown / refractory window; the independence criterion; the minimum independent-episode floor. These must be justified **before** counting and must **not** be tuned to make the lane feasible.

> Episode-definition parameters are not feasibility knobs. They must be justified before counting, not adjusted until enough episodes appear.

---

## 16. Family / multiplicity guard

- Multiple compression definitions, lookbacks, thresholds, and horizons are **one family** unless a future memo explicitly separates them.
- **No rescue** by swapping definitions after results.
- **No rescue** by changing expansion horizon after results.
- **No rescue** by choosing the threshold that produces the nicest result.
- Any future alpha attempt must be **budgeted under atlas family rules.**

---

## 17. Stage structure (draft, not authorized)

- **Stage-1 design memo draft:** this file.
- **Stage-1 acceptance/freeze:** future owner review and commit only.
- **Pre-gate collinearity diagnostic:** future explicit authorization only.
- **Pre-gate feasibility/count audit:** future explicit authorization only, and only **after** the collinearity diagnostic.
- **Stage-2 literal freeze:** if diagnostics are adequate.
- **Sandbox gate:** only after Stage-2 freeze and explicit authorization.
- **Sealed data:** none until separately authorized under atlas rules.

---

## 18. Failure modes

- infeasible-by-definition;
- dissolves into volatility mean-reversion;
- dissolves into bounded-floor mechanics;
- dissolves into autocorrelation / variance-ratio structure;
- logical non-identity mistaken for generic orthogonality;
- too few independent compression episodes;
- hidden breakout strategy;
- threshold fishing;
- horizon fishing;
- overlapping episodes / serial dependence;
- metaphor overreach;
- prior-art inheritance error.

---

## 19. Expected result / honest prior

- **Honest prior:** Compression probably **nulls**, proves **infeasible-by-definition**, proves **empirically collinear** with its baselines, or proves **infeasible by insufficient independent episodes.**
- **That is an acceptable result.**
- The project's integrity depends on **allowing that outcome.**

---

## 20. Non-authorizations

- **No data contact authorized.**
- **No collinearity diagnostic authorized.**
- **No episode-count audit authorized.**
- **No test/gate authorized.**
- **No code authorized.**
- **No alpha spend.**
- **No sealed data.**
- **No Stage-1 freeze until explicit acceptance.**

---

## 21. Boundary confirmations

- No tests were run.
- No modeling was run.
- No market data was opened.
- No gate was run.
- No audit was run.
- No synthetic-null check was run.
- No wake/outcome was computed.
- No sealed data was accessed.
- No design rule is frozen by this memo.
