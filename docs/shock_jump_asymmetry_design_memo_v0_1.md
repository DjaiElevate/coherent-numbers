# Shock/Jump Asymmetry Lane — Design Memo v0.1 (Stage-1 rules-frozen)

**STATUS: Stage-1 rules-frozen on owner approval. Design rules and the most-selective-feasible selection rule are frozen at this SHA. Threshold, caliper, time-locality, replacement rule, and minimum matched-pair floor remain DEFERRED to the pre-gate count audit (§7A) and are NOT frozen until the Stage-2 re-hash (§7B). No sandbox gate may run from this Stage-1 version.**

**Lane:** Shock/jump — adjusted-close-only, SPY 2005–2022, sign-conditional asymmetry framed.

**Position in program:** First design-memo candidate following the committed *Market Force Atlas v0.1* and the committed *first-promotion decision*.

**This memo proposes a full design. It does not freeze it, does not authorize any data contact, and does not authorize any test.**

---

## 0. Core framing (read first)

This lane is **not** asking:

> "Do large moves lead to more large moves?"

That is volatility clustering and belongs to the **VOLATILITY** cluster.

This lane **is** asking:

> "Do large down-shocks leave a different future wake than large up-shocks of comparable standardized magnitude, after accounting for ordinary volatility clustering and ordinary sign-aware leverage asymmetry?"

The real hypothesis is **sign-conditional asymmetry**, not generic aftershock behavior.

### Governance constants (inherited from the Atlas, not amended here)

- `MAX_ACTIVE_ATLAS_LANES = 1`
- `ATLAS_FAMILY_ALPHA = 0.05`
- `MAX_SEALED_ATTEMPTS_ATLAS_V0X = 5`
- `PER_ATTEMPT_ALPHA = 0.01` unless amended on the record
- Sandbox failure debits nothing.
- Sealed-data contact is the moment family alpha is spent.

### Lane state (inherited, not decided here)

- Market Force Atlas v0.1 is committed.
- First-promotion decision is committed.
- Recommended force: **Shock/jump asymmetry**.
- Exact version/window: **adjusted-close-only SPY 2005–2022**.
- Volume-confirmed shock is **deferred**.
- Compression is **named fallback only, not authorized**.
- Curvature, cusp/reversal, and news direction are **CLOSED**.
- Cross-asset dispersion, correlation regime, and fundamental dispersion are **RESERVED**.
- No sealed data may be opened.

---

## 1. Purpose and non-goals

This is **explanatory research, not a trading system.**

- No direction prediction.
- No edge claim.
- No trade rule.
- No optimization.
- No sealed data until sandbox PASS **and** explicit owner authorization.
- A null is valid and expected.
- A sandbox FAIL closes the lane as an exploratory null and **debits no sealed alpha**.

The output of this lane, at most, is a statement of the form: *holding the frozen big-force baselines fixed, large down-shocks do / do not leave an incrementally different wake than comparable up-shocks.* It is never a statement about how to trade shocks, nor a claim that shocks "work."

---

## 2. Force definition

**Force:** `Shock/jump`

**Forest metaphor.** A stone is thrown at the walker. But the design must distinguish:

- stone from the **left**,
- stone from the **right**,
- of the **same size**,
- under **similar ground/weather**.

**Market translation.**

- An **up-shock** and a **down-shock** are large standardized return impulses.
- The central comparison is **down-shocks vs up-shocks of comparable magnitude and comparable prior volatility context.**

The distinctness of this lane does not come from "shocks are followed by turbulence." It comes from the *difference between the two sides* once size and weather are held fixed.

> The distinctness claim lives on the sign-conditional asymmetry axis. Without that asymmetry framing, Shock is not suitable as a promoted lane because symmetric aftershock behavior belongs to volatility clustering.

---

## 3. Force Visibility Protocol — one-layer application only

Do **not** build a general six-layer residualization engine. Apply the Force Visibility Protocol **only once, inside this Shock lane.**

### Force Visibility Protocol, restricted form

- Big forces can drown small forces.
- The big force here is **volatility regime / volatility clustering.**
- The design must make that force **visible** before testing Shock.
- **Subtraction order is a researcher degree of freedom and must be frozen before data contact.**
- Residualizing **after** seeing data would be a forking path.
- This lane measures **incremental** shock asymmetry after specified baselines, not total market reaction to shocks.

### Predeclared layer order (DRAFT-FOR-REVIEW, not frozen until owner approval)

1. **Data construction** — adjusted-close return construction.
2. **Prior volatility** — trailing realized volatility.
3. **Shock magnitude.**
4. **Ordinary sign-aware leverage asymmetry.**
5. **Shock-conditional asymmetry.**

> Shared variance is attributed to earlier layers by design. Therefore a null means "no incremental shock-conditional asymmetry beyond the frozen baselines," not "shocks do not matter."

---

## 4. Total effect vs incremental effect

### Total vs incremental interpretation

- **Total effect:** what happens after shocks **before** controlling for anything.
- **Incremental effect:** what remains **after** accounting for prior volatility, magnitude, and ordinary sign-aware leverage asymmetry.

**The gated claim, if any, can only be incremental.**

A null in this lane must never be read as "shocks have no total effect." By the layer-order construction in §3, total effect is largely pre-assigned to earlier layers.

> A future null would mean that Shock/jump asymmetry did not add explanatory value beyond the frozen big-force baselines, not that shock events are irrelevant to markets.

---

## 5. Impulse-vs-reversal firewall

(Imported from the first-promotion decision memo.)

- A **Shock** event is a **single-step impulse-magnitude exceedance.**
- A **Cusp/reversal** event was a **two-vertex reversal geometry** and is **CLOSED** through *Cusp Geometry Lane v0.3*.
- These are different objects, but they **overlap** when a shock is immediately reversed.
- The design must test **all qualifying shocks**, not filter down to shocks-that-reverse.
- Filtering to shocks-that-reverse would be **Cusp/reversal re-entry through the side door.**
- If a signal survives **only** inside shocks-that-reverse, that is **contamination / closed-lane overlap**, not a positive Shock finding.

> If the surviving signal lives only in shocks-that-reverse, it is not a Shock finding; it is Cusp/reversal re-entry, and the lane must report contamination rather than success.

See §10 (J) for the contamination tripwire that operationalizes this firewall.

---

## 6. Data scope

Use **only** the adjusted-close SPY sandbox window:

- **instrument:** SPY
- **column:** adjusted close / `adj_close`
- **sandbox period:** 2005–2022
- **sealed boundary:** 2023-01-01
- **no** volume confirmation
- **no** OHLC
- **no** news
- **no** macro
- **no** external data
- **no** cross-asset data

Volume-confirmed Shock remains **deferred** because it shortens the usable window to 2013–2022 and would require a separate future design.

**The data is not read in this memo. This section is design-only.**

---

## 7. Design objects to propose

All literals below are **DRAFT-FOR-REVIEW, not frozen until owner approval.** No object is left as a hidden choice point.

| ID | Object | Draft proposal (not frozen) |
|----|--------|------------------------------|
| A | **Shock threshold** | Standardized-return exceedance on the §C standardized series. **Candidate thresholds: `{3.5, 4.0, 4.5}`** — no single standalone literal is frozen here. Symmetric threshold for both sides (the *threshold* is sign-blind; the *outcome comparison* is sign-conditional). The final threshold is selected **only after the pre-gate count audit (§7A)**, by the predeclared most-selective-feasible rule, and frozen **jointly** with the volatility estimator (B), caliper (§8), replacement rule (§8), time-local matching policy (§8), and matched-pair floor (§8). Selection is made **before any wake/outcome inspection**; it may **not** be chosen to maximize matched-pair count or by predictive performance. |
| B | **Volatility estimator** | Trailing realized volatility from adjusted-close log returns over a trailing window ending strictly before the shock day (`t-1` and earlier). Draft window: 21 trading days, EWMA optionally considered as a diagnostic only. Strictly pre-shock (see §8 magnitude-scale contamination). |
| C | **Standardized return definition** | `z_t = r_t / σ̂_{t-1}` where `r_t` is the adjusted-close log return and `σ̂_{t-1}` is the §B pre-shock estimator. No use of `r_t` itself in the denominator. |
| D | **Matching rule** | See §8 (keystone). Draft: caliper matching on (standardized magnitude, pre-shock volatility), with a named cross-time policy. |
| E | **Sign-aware leverage baseline** | An explicit ordinary down-day/negative-return volatility-asymmetry baseline that Shock-asymmetry must beat. See §10. |
| F | **Symmetric magnitude clustering baseline** | "Large move followed by large moves" regardless of sign. See §10. |
| G | **Wake / outcome statistic** | Primary: forward realized volatility over a fixed forward window. See §13. |
| H | **Gate** | Concordance gate (matched + residual must agree and both clear minimum condition). See §9 and §14. |
| I | **Synthetic-null check** | Sign-randomized magnitudes PRIMARY, plus three symmetric generators. See §12. |
| J | **Contamination tripwire** | Shocks-that-reverse overlap check; signal that lives only in reversed shocks is reported as contamination, not success. See §5 and §14. |
| K | **Multiple-testing / alpha debit rule** | One primary gate, one sandbox attempt per frozen design; sealed attempts debit `PER_ATTEMPT_ALPHA = 0.01`. See §14. |

**The threshold is not a free literal. It is part of the feasibility bundle.**

**The final threshold is selected by the most-selective-feasible rule after the count audit: the highest candidate threshold that satisfies the predeclared time-local matched-pair floor.**

---

## 7A. Pre-gate count audit — threshold/floor feasibility

The shock threshold, caliper, replacement rule, time-locality rule, and minimum matched-pair floor **jointly** determine whether the lane can run at all. Freezing `|z| ≥ 4.0`, caliper `0.20`, no replacement, time-local matching, and `30` matched pairs **independently** may make the lane arithmetically unable to run.

**Threshold, caliper, replacement rule, time-locality rule, and minimum matched-pair floor are one coupled design object. They may not be frozen independently.**

An insufficient matched-pair count is **not a null**. It is an **infeasible design / non-result**.

Before any sandbox gate or final freeze, the lane requires a **pre-gate count audit on the standardized return series only**.

- The count audit **may** count event dates, signs, standardized magnitudes, pre-shock volatility, and possible matched-pair feasibility.
- The count audit **must not** inspect forward wake/outcome values.
- The count audit **must not** compute future realized volatility, future drawdown, recovery, or any target outcome.
- The count audit is **instrument-feasibility, not a test.**
- It **does not** debit sealed alpha.
- It **does not** authorize tuning against outcomes.
- It exists only to choose threshold/floor/caliper feasibility **jointly** before the gate is frozen.

### Candidate audit grid (DRAFT-FOR-REVIEW)

- **Shock thresholds:** `{3.5, 4.0, 4.5}`.
- **Caliper candidates:** include the current `0.20` **and at least one wider candidate** for feasibility review (e.g., `0.35`) — all marked `DRAFT-FOR-REVIEW`.
- **Replacement options:** no replacement is preferred, but feasibility **must be audited** (i.e., the without-replacement count is the binding feasibility figure; a with-replacement count may be audited for context only).
- **Minimum pair floor:** to be chosen **jointly after the audit**, not independently — subject to the power/noise pre-condition below.

> If the pre-gate count audit shows the proposed literals cannot produce a valid matched set, the design must be revised before freeze. That is not a sandbox FAIL and not a null result.

### Selection rule must be mechanical, not discretionary

- The minimum matched-pair floor **must be set from a stated power/noise consideration before the audit runs**.
- The floor must represent the **minimum number of matched pairs below which the matched estimator is too noisy to mean anything**.
- The floor **may not** be chosen afterward to fit whatever count appears.
- The threshold is then selected by a **frozen rule**:

  > Choose the highest, most selective candidate threshold in `{3.5, 4.0, 4.5}` that yields at least the predeclared floor of time-local matched pairs.

- **Rationale:** shock distinctness from the ordinary leverage baseline increases with threshold, so feasibility is the **constraint**, not the objective.
- The rule must bias toward **extremity**, never toward whichever threshold is most convenient.
- Choosing the threshold to maximize pair count is a soft form of **fitting on event structure**, and event structure can correlate with outcome structure.
- The most-selective-feasible rule blocks that backdoor optimization.
- If **no** candidate threshold yields the floor at time-local scope, the design is **infeasible** and must be revised before freeze.
- In that case, **do not** rescue the design by widening into other epochs or by lowering the floor after seeing the counts.

**The threshold is selected by the most-selective-feasible rule: use the highest candidate threshold that meets the predeclared time-local matched-pair floor. Feasibility is the constraint, not the objective.**

**Choosing the threshold to maximize matched-pair count would be event-structure fitting. The design therefore uses a mechanical most-selective-feasible rule, declared before the count audit.**

*The pre-gate count audit is specified here only; it is not run by this memo.*

---

## 7B. Two-stage freeze structure

This design memo freezes the design rules, not the final audit-derived literals. Approval of this memo creates a Stage-1 rules freeze: the force definition, baselines, matching logic, synthetic-null requirements, gate logic, contamination tripwire, and the most-selective-feasible selection rule are fixed at this memo SHA. The threshold, caliper, time-locality, replacement rule, and minimum matched-pair floor remain deliberately deferred to the pre-gate count audit because they cannot be honestly pinned without event-count feasibility information. The count audit may inspect only event-side standardized returns and matching feasibility, never forward wake/outcome values. After the audit, the selected literals must be appended to this memo according to the frozen selection rule and the memo must be re-hashed. Only that Stage-2, audit-completed, fully pinned version may be used for any sandbox gate. A sandbox run may not execute from the Stage-1 rules-only memo.

---

## 8. Matching rule

**The word "comparable" is load-bearing.**

A down-shock must be compared to up-shocks of comparable:

- **standardized magnitude,**
- **prior volatility,**
- and **timing context if specified.**

### Proposed matching rule (DRAFT-FOR-REVIEW, not frozen until owner approval)

- **What is matched:** each down-shock to one or more up-shocks, on the pair (standardized magnitude `|z|`, pre-shock trailing volatility `σ̂_{t-1}`).
- **Distance metric:** standardized Euclidean distance on the two matching covariates (each scaled to unit variance over the shock set), draft.
- **Caliper / tolerance:** matches only admitted within caliper `0.20` standardized-distance units (draft); `|z|` difference additionally capped at `0.5` (draft).
- **One-to-one or many-to-one:** draft = **one-to-one optimal matching** to avoid one extreme event dominating; many-to-one considered only as a diagnostic.
- **Replacement:** draft = **no replacement** for the primary matched form (so no event reuse inflates the matched count).
- **Tie handling:** deterministic tie-break by smallest `|z|` difference, then earliest date; fully specified before contact.
- **No-match behavior:** unmatched shocks are **dropped from the matched estimator** and **counted/reported**; they are never silently discarded.
- **Cross-time-regime matching:** see the named tension below — draft = **time-local only for the gate** (widened/nonlocal matches are descriptive context, excluded from every PASS condition).
- **Event reuse:** disallowed in primary (see no-replacement).
- **Minimum matched-pair count for a valid sandbox evaluation:** draft = **30 matched pairs** minimum; below this the sandbox is reported as **inconclusive / insufficient sample**, not as a pass or fail.

**Do not let the design choose matching after seeing data.**

> The matching rule is the primary forking-path risk in this lane. It must be frozen before sandbox contact.

### Addition — magnitude-scale contamination

The volatility estimate used to standardize shock magnitude must be **strictly pre-shock** (uses only information up to `t-1`, never `r_t`, never `t+`).

The memo must address whether that volatility estimate is itself **sign-contaminated**, because the leverage effect can elevate volatility ahead of down-moves. If the trailing window straddles a recent down-move, the denominator for a down-shock can be systematically larger than for an up-shock, making them look "comparable" only because the ruler already absorbed part of the asymmetry.

**Draft mitigation (not frozen):** (i) the volatility estimator is computed from a trailing window ending at `t-1`; (ii) as a frozen design choice, a sensitivity arm computes the standardized magnitude with a **sign-symmetrized volatility estimator** (e.g., volatility estimated on `|r|` without conditioning on sign of recent returns) so that the ruler's sign-contamination can be measured, not assumed away. The matched comparison must hold under both the plain and the symmetrized ruler for a clean PASS; divergence is reported as ruler-driven, not as a Shock finding.

> The pre-shock volatility scale is part of the ruler. If the ruler already contains sign-contamination, apparent comparability may be false comparability. The design must specify the ruler before data contact and accept its consequences.

### Addition — cross-time matching tension (named design tension)

- Down-shocks and up-shocks may **not be equinumerous**.
- Down-shocks may **cluster in crises**.
- Up-shocks may **cluster in rebounds**.
- **Free** cross-time matching may compare crisis down-shocks with rebound up-shocks.
- That risks measuring **epoch/regime** rather than **sign**.
- **Time-local** matching may reduce contamination but can **starve** the matched sample.
- **Pre-committed resolution (DRAFT-FOR-REVIEW) — time-local only for the gate:**
  - The **primary matched gate reads only the time-local matched set.**
  - The time-local window remains `DRAFT-FOR-REVIEW`, with current candidate **±252 trading days**.
  - **Widened/nonlocal matches may be reported only as descriptive context.**
  - **Widened/nonlocal matches are explicitly excluded from all PASS conditions.** A PASS cannot depend on widened matches.
  - If the time-local matched set cannot meet the pair floor, the lane reports **infeasible design / insufficient sample** unless the pre-gate count audit (§7A) leads to a revised threshold/floor **before freeze**.
  - **Do not widen into other epochs to rescue feasibility after the literals are frozen.**
- The rationale above is stated **before data contact** and is frozen at approval.

**The concordance gate reads the time-local matched set only. Widened matches are descriptive context and are excluded from every pass condition.**

**If the time-local pool cannot support the matched-pair floor, the solution is not to widen into other epochs after the fact. The solution is to resolve threshold, caliper, time-locality, and pair floor jointly during the pre-gate count audit before freeze.**

> If the matcher pairs down-shocks from one historical regime with up-shocks from a different historical regime, the lane may be measuring epoch rather than sign. The design must decide this before sandbox contact.

---

## 9. Residual form and matched form

Residualizing and matching are two ways of asking the **same** question:

> Holding big forces fixed, does the small force still move the path?

Both forms are included, **but they must not become two independent chances to pass.**

### Decision structures considered

- **Option A:** matched form primary, residual form diagnostic only.
- **Option B:** residual form primary, matched form diagnostic only.
- **Option C:** **concordance gate** — both must agree in direction **and** both must clear a pre-specified minimum condition.

### Recommendation: **Option C — concordance gate**

**Reason.** This is more conservative. It prevents matching and residualization from becoming two shots at success. Agreement is robustness. Disagreement is a structural finding, not a nuisance.

### Local-only matched gate

- **Matched-form PASS is evaluated on the time-local matched set only** (§8).
- **Residual-form PASS remains separate.**
- Option C concordance still requires **both** matched and residual forms to agree in direction **and** clear their pre-specified minimum condition.
- If residual passes but the **time-local matched form fails**, this is **structural ambiguity, not a pass**.
- If **widened matches pass but time-local matches fail**, this is **not a pass**.

**Nonlocal/widened matched results cannot rescue a failed local matched gate.**

### Interpretation table (frozen with the gate)

| Matched | Residual | Interpretation |
|---------|----------|----------------|
| pass, same direction | pass, same direction | **Possible incremental asymmetry** — eligible for the next protocol step (still no sealed data without owner authorization). |
| pass | fail | **Structural ambiguity / regime-dependence candidate** — not a clean positive. |
| fail | pass | **Structural ambiguity / regime-dependence candidate** — not a clean positive. |
| fail | fail | **Exploratory null.** |

Disagreement is never a pass. It is a structural-ambiguity / regime-dependence flag.

---

## 10. Baselines

The design must include **at least** these baselines:

1. **Sign-blind trailing realized volatility baseline.** Captures ordinary volatility clustering. (Layer 2.)
2. **Symmetric magnitude clustering baseline.** Captures "large move followed by large moves" regardless of sign. (Layer 3.)
3. **Sign-aware leverage baseline.** Captures ordinary down-day / negative-return volatility asymmetry. (Layer 4.)

**Down/up asymmetry is not virgin territory.** The leverage effect is a known regularity. Therefore Shock-asymmetry must **beat ordinary sign-aware leverage behavior.**

> Do large down-shocks leave a qualitatively different wake than ordinary down-day leverage asymmetry already predicts?

**Proposed specification of the sign-aware baseline (DRAFT-FOR-REVIEW, for the future frozen design).** Estimate the ordinary relationship between the **sign** of a day's return and forward realized volatility across **all** days (not only shock days) — i.e., the routine asymmetry by which negative returns precede higher forward volatility. The Shock-conditional asymmetry (Layer 5) is then evaluated as the **increment** of the down-vs-up wake difference *among matched shocks* over what this all-days sign-aware leverage relationship already predicts at the same magnitude/volatility context. The exact functional form (e.g., a frozen leverage coefficient applied at the shock's covariates) is to be fixed at approval and never re-chosen after sandbox contact.

This section is **design logic, not literature review.** No external literature or web search is used.

---

## 11. Regime stratification guardrail

- Regime buckets can **multiply tests.**
- Volatility regime labels may be useful for **diagnostics**, but **subgroup gates are dangerous.**
- **Any regime split must be frozen before data contact.**
- If volatility buckets are proposed, the **exact** bucket rules and their status (descriptive vs gated) must be specified.
- **Default: no gated subgroup claims in v0.1.**
- Regime analysis, if included, is **descriptive only** unless explicitly added to the gate with alpha/multiplicity accounting.

**Draft for v0.1:** regime labels (if any) are **descriptive only**; there are **no gated subgroup claims.** The single gate operates on the pooled matched/residual comparison.

> The weather map is useful for thinking, but dangerous as a testing surface unless its cells are frozen before data contact.

---

## 12. Synthetic-null check

**Do not run the check yet unless separately authorized.** This section specifies a future check.

The check verifies that the **matching rule does not manufacture asymmetry under symmetric data.**

The synthetic-null check must test at least:

1. **Primary synthetic null: sign-randomized magnitudes.**
   - Take real SPY-shaped return **magnitudes**.
   - Preserve every magnitude **exactly**.
   - Randomly **flip signs**.
   - This destroys true sign asymmetry while preserving magnitude distribution, clustering, and fat tails.
   - **If the matching pipeline reports down/up asymmetry on this sign-randomized data, the pipeline is broken.**
2. Symmetric **iid** returns.
3. Symmetric returns with **volatility clustering**.
4. Symmetric **fat-tailed** returns.

**The sign-randomized magnitudes check is PRIMARY, not optional.**

In addition, the synthetic-null check must evaluate:

- the **time-local matched gate**,
- the **widened descriptive matches separately**, and
- whether **widening creates false asymmetry** under sign-randomized magnitudes.

**If widened matches produce apparent asymmetry under a synthetic null while time-local matches do not, widening is treated as an artifact, not robustness.**

**The synthetic-null check must report matched-pair counts at each candidate threshold/caliper combination before any market wake/outcome is inspected.**

The check must answer:

- Does the matching rule **create fake** down/up asymmetry under symmetric signs?
- Does the matched-pair construction **bias one side**?
- Is the required matched-pair count **plausible** before market data contact?
- Does the pre-shock standardization scale create **false comparability**?

This synthetic check must occur **before** sandbox data contact **if the owner approves.** Passing the synthetic-null check is a **precondition** for the lane being allowed to touch sandbox data; it is a check on the *instrument*, and it touches **no** market data and **no** sealed data.

---

## 13. Wake statistic

The memo proposes candidate wake outcomes; it does not choose too many.

**Candidate outcome families.**

- forward realized volatility,
- forward max drawdown,
- recovery / calm-down time.

**Recommendation.**

- **Primary gate outcome (canonical):** **forward realized volatility** over a fixed forward window (draft: 21 trading days, ending strictly after the shock day; no overlap into sealed period). This aligns with the atlas canonical outcomes and is symmetric to both up- and down-shocks, so it does not pre-bake a sign preference into the outcome.
- **Secondary descriptive outcome (one only):** **forward max drawdown** — descriptive only.
- **Deferred / rejected:** recovery / calm-down time (deferred; outcome-multiplicity risk, definition sensitivity).

Outcome labels are explicit: forward realized volatility = **primary gate**; forward max drawdown = **secondary descriptive**; recovery/calm-down time = **deferred**.

> The secondary outcome is not part of the sandbox PASS rule and may not be used to rescue a failed primary gate.

---

## 14. Gate and closure

### Sandbox gate (DRAFT-FOR-REVIEW)

**Passes when, on the PRIMARY outcome (forward realized volatility):**

- the **matched form** shows a down-vs-up wake difference in a consistent direction and clears the pre-specified minimum condition, **and**
- the **residual form** agrees in direction and clears its pre-specified minimum condition, **and**
- the result holds under **both** the plain and sign-symmetrized ruler (§8 magnitude-scale contamination), **and**
- matched-pair count meets the minimum-pair floor fixed by the §7A feasibility bundle: the floor is set by a power/noise rationale before the pre-gate count audit, and no standalone numeric floor is frozen in §14, **and**
- the contamination tripwire (§5/below) is **not** triggered.

**Fails when:** both forms fail, or the primary outcome shows no consistent incremental asymmetry.

**Disagreement** (one form passes, one fails): **structural ambiguity / regime-dependence candidate** — **not** a pass (see §9 table).

**Contamination** (tripwire J): if the surviving signal lives **only** inside shocks-that-reverse, the lane reports **contamination**, not success — this is Cusp/reversal re-entry and is **not** a Shock finding (§5).

### Closure logic (required rules)

- Sandbox FAIL **closes the lane as exploratory null.**
- Sandbox FAIL **debits no sealed alpha.**
- Sandbox PASS **does not open sealed data automatically.**
- Sealed data may be opened **only after explicit owner authorization.**
- Any sealed test would debit **`PER_ATTEMPT_ALPHA = 0.01`** from the atlas family budget.
- **No tuning after sandbox result.**
- **No alternative thresholds or matching rules after sandbox result.**
- **No secondary descriptive outcome can rescue a failed primary gate.**

---

## 15. Expected result

**Expected result: null.**

**Reason.** Shock-asymmetry may dissolve into:

- volatility clustering,
- symmetric magnitude effects,
- ordinary leverage asymmetry,
- sign-contaminated scaling,
- epoch/regime mismatch,
- or closed Cusp/reversal overlap.

**A clean null is a valid outcome.**

---

## 16. Relationship to prior artifacts

- **Market Force Atlas v0.1** — committed; this lane is the first promotion under its governance.
- **First-promotion decision memo** — committed; recommended Shock/jump asymmetry at adjusted-close-only SPY 2005–2022; source of the impulse-vs-reversal firewall.
- **Cusp Geometry Lane v0.3 — CLOSED.** Not reopened. The firewall in §5 exists to prevent side-door re-entry.
- **Curvature — CLOSED.** Not reopened.
- **Cusp/reversal — CLOSED.** Not reopened.
- **B6/curvature lesson:** a beautiful feature can be absorbed by a boring representative. This is the motivation for the big-force baselines in §10 and the incremental-only framing in §4.
- **Atlas governance:** cards free, lanes rationed, sealed alpha shared.

**No closed lane is reopened by this memo.**

---

## 17. Open owner questions

1. **Feasibility bundle (A/B/§7A/§8) — single coupled choice:** Choose threshold-caliper-time-locality-pair-floor bundle **after the pre-gate count audit**, using the predeclared **most-selective-feasible rule**. (This replaces the previously separate threshold, caliper, cross-time-policy, and pair-floor questions.)
2. **Minimum matched-pair floor rationale (§7A/§8):** confirm the power/noise basis used to set the floor **before** the audit runs (the floor is the count below which the matched estimator is too noisy to mean anything; it may not be set after seeing counts).
3. **Volatility estimator / pre-shock ruler (B/§8):** 21-day trailing realized vol as drafted, or a different window / EWMA; and accept the plain + sign-symmetrized dual-ruler requirement, or treat the symmetrized ruler as diagnostic only?
4. **Sign-aware leverage baseline formula (§10):** accept all-days leverage relationship as the increment reference, or a different specification?
5. **Residual-form specification (§9):** confirm the residual form and that Option C (concordance gate) governs, evaluated on the **time-local matched set only**.
6. **Primary wake statistic confirmation (§13):** confirm forward realized volatility (21-day) as primary; confirm forward max drawdown as secondary-descriptive-only.
7. **Contamination tripwire operationalization (§5/§14):** confirm how the shocks-that-reverse overlap check is operationalized.
8. **Synthetic-null sequencing (§12):** confirm the synthetic-null suite must PASS before any sandbox contact is even requested, and that it reports matched-pair counts per threshold/caliper before any wake/outcome inspection.

---

## 18. Output / boundary confirmations

- This memo opened **no market data.**
- This memo ran **no tests.**
- This memo ran **no modeling.**
- This memo ran **no tuning.**
- This memo inspected **no sealed values.**
- This memo accessed **no sealed data.**
- This memo did **not** open the SPY sandbox file.
- Nothing was **staged.**
- Nothing was **committed.**
- Nothing was **pushed.**

**All literals in this memo are DRAFT-FOR-REVIEW and are not frozen until the owner explicitly approves.**
