# Market Force Atlas — First-Promotion Decision Memo v0.1 — DRAFT

**Status: DRAFT FOR OWNER REVIEW. Not committed. Not staged. Not pushed.**
**Class: exploratory-design (atlas decision). Writing/revising this memo consumes no trials and touches no data.**
**Repo: /Users/jay/Documents/GitHub/coherent-numbers**
**Drafted: 2026-06-14**
**Authority: this memo discharges Market Force Atlas v0.1 §11 Q9 ("First force to promote — intentionally deferred to a separate future session").**

**Value-safety:** no raw data read, no row-level values, no prices/returns/sentiment/macro values, **no sealed-period (≥ 2023-01-01) values inspected, no sealed data opened for analysis.** This memo was written from the committed atlas text and filename/header/SHA metadata only.

> **This decision memo does not authorize testing.** It only recommends which force should be considered *first* for a future design memo. It does not design a lane, does not run a sandbox gate, does not open sealed data, and does not spend any sealed alpha. No force is promoted by this memo. Promotion happens only through a separately reviewed, hash-pinned, frozen design memo (atlas §3, §10).

---

## 0. Anchors and known state

- **Market Force Atlas v0.1** is committed at `dba9b9e08c8b705fe925fa141231b26a0b0e367b` (`docs/market_force_atlas_v0_1.md`).
- **Cusp Geometry Lane v0.3** is **CLOSED** as exploratory null (curvature absorbed by zigzag/B6; `0/10` folds; incremental R² `-0.0256`). Closure commit `ac098b66…`.
- **Curvature** and **Cusp/reversal** remain **CLOSED**. Do not reopen.
- **News direction** is **CLOSED** (Lane 2 TTG → SPY v1.1 null).
- **GDELT raw-count/coverage proxy** is **CLOSED** (drift-confounded exploratory null).
- **Cross-asset dispersion, correlation regime, fundamental dispersion** remain **RESERVED** to the live dispersion lane (§3.1 of the atlas).
- **No force is currently promoted.** `MAX_ACTIVE_ATLAS_LANES = 1` is fully available.

### 0.1 Governance literals in force (atlas §3)

```
MAX_ACTIVE_ATLAS_LANES        = 1
ATLAS_FAMILY_ALPHA            = 0.05
MAX_SEALED_ATTEMPTS_ATLAS_V0X = 5
PER_ATTEMPT_ALPHA             = 0.01   # unless amended on the record
```

The four governing facts (atlas §3) that frame this decision:

1. **Cards are free; lanes are rationed.** Writing this memo costs nothing; promotion is the scarce act.
2. **Sealed alpha is shared across the atlas family.** `0.05` total, **not** `0.05` per lane. Five attempts at `0.01` each.
3. **No promoted lane gets a fresh independent sealed-alpha budget.** Cleanliness earns the right to *spend* from the shared budget, not a new budget.
4. **Sealed alpha is spent only at the moment of sealed-data contact.** **Sandbox-gate failures debit nothing.** A sandbox FAIL closes a lane as exploratory null without touching the family budget.

**Consequence for this memo:** the first promotion is the most likely first claim on a five-deep, non-renewable shared budget. The question is therefore not only *"which force is most interesting?"* but *"which force is worth the family's first potential `0.01` sealed attempt ahead of the other seven?"* — a budget-allocation question, not just an interest ranking.

### 0.2 Closed/reserved lanes stay closed/reserved

This memo may not promote, reopen, redefine, or explore any CLOSED force (curvature, cusp/reversal, news direction, GDELT raw-count) or any RESERVED force (cross-asset dispersion, correlation regime, fundamental dispersion). Candidates that drift toward closed/reserved territory are penalized accordingly below.

### 0.3 The two-window rule (atlas §6A)

No candidate may silently mix windows. Where a force has more than one version in different data windows, this memo names the **specific version and specific window** it recommends:

- **Adjusted-close SPY price-shape forces:** sandbox window **2005–2022** (`spy_yahoo_adjclose_..._sandbox_from_v8.csv`, `5cd92502…`).
- **OHLC / volume-dependent forces:** **2013–2022 only** (OHLCV snapshot `2842647c…`).
- **News / GDELT-derived forces:** **2013–2022 only**.

A longer window means more independent sandbox events and more statistical power per `0.01` attempt. All else equal, a **2005–2022 price-only version is budget-preferred over a 2013–2022 version** of comparable scientific value.

---

## 1. The central question for first promotion: distinctness, not interest

Every VOLATILITY-cluster candidate (six of the eight below) must beat the cluster's canonical representative — **trailing realized volatility** — out-of-fold, under the same sandbox gate that closed Curvature (atlas §4, §4.1). Interest is cheap; **distinctness is the bar.** Curvature was *interesting* and still died because realized vol / zigzag absorbed it.

For each candidate this memo states explicitly **what it must beat to count as distinct**. A candidate whose only plausibly-distinct content is something trailing realized vol already owns is not worth the first sealed `0.01`, however intuitive its story.

---

## 2. Candidate evaluations

Each candidate carries: force name · atlas status · cluster · canonical representative · forest metaphor · why interesting · available data · recommended version/window if promoted · window limitations · governance risk · distinctness risk (**what it must beat**) · external-data risk · budget-allocation argument · overlaps with CLOSED/RESERVED · price-only studyable? · suitable as first promoted force?

---

### Candidate 1 — Shock / jump → "Aftershock Force"

- **Force name:** Shock / jump (owner working title: **Aftershock Force**).
- **Atlas status:** **OPEN** (atlas §7, Group 1, Shock/jump card).
- **Cluster:** VOLATILITY.
- **Canonical representative (must beat):** trailing realized volatility.
- **Forest metaphor:** a stone thrown at the walker / a branch suddenly snapping — a sudden external impulse strikes the path. The explanatory question: **after a sudden shock, what happens to the path?**
- **Why interesting:** price-only in its simplest form, intuitive, OPEN, not closed, not reserved, needs no macro/news/vintage/external data, and poses a clean *explanatory* (not edge-seeking) question. Maps to the canonical outcome family directly (forward realized vol #1; forward max drawdown #2).
- **Available data:** SPY adj_close sandbox **2005–2022** (`5cd92502…`) for the adjusted-close-only version. Volume-confirmed version needs OHLCV (`2842647c…`), **2013–2022 only**.
- **Recommended version/window if promoted:** **Shock/jump, adjusted-close-only version, 2005–2022 sandbox-capable** — and **framed around down-shock vs up-shock asymmetry** (see §3). The **volume-confirmed version (2013–2022 only) is explicitly deferred** because it shortens the window for no offsetting distinctness gain at first promotion.
- **Window limitations:** adjusted-close-only version has the **full 2005–2022 span** (no shortening) — a budget advantage. Volume confirmation would truncate to 2013–2022.
- **Governance risk:** **Low.** OPEN, price-only, not adjacent to any CLOSED/RESERVED lane, fits cleanly under `MAX_ACTIVE_ATLAS_LANES = 1`.
- **Distinctness risk:** **HIGH and central — this is the whole question (see §3).** Conditioning on a shock = conditioning on a large realized move, and *"large moves follow large moves"* is **already owned by trailing realized volatility** (vol clustering). The atlas Shock card already flags the mechanical overlap: *"jumps inflate realized vol itself."* Generic symmetric aftershock magnitude is **pre-conceded to the canonical representative.**
- **External-data risk:** **None** (price-only).
- **Budget-allocation argument:** Worth the family's first potential `0.01` **only in its sign-asymmetry framing** (§3). In that framing it offers a hypothesis trailing realized vol *cannot* trivially own — realized vol is sign-blind, so a sign-conditional post-shock path is a genuinely separable question — at the **longest available window (2005–2022)**, **price-only** (no external/vintage dependency), and with the **cleanest governance profile** of all eight. That combination — full window × zero external risk × low governance risk × a distinct hypothesis the representative is structurally blind to — is what earns it the first attempt ahead of the others.
- **Overlaps CLOSED/RESERVED?** No. (Distinct from cusp/reversal, which is a *vertex-geometry* force; shock is an *impulse-exceedance* force. But see §3.3 — the design memo must keep them separate.)
- **Price-only studyable?** **Yes** (adjusted-close-only version).
- **Suitable as first promoted force?** **Yes — recommended**, conditional on adopting the asymmetry framing in §3.

---

### Candidate 2 — Compression

- **Atlas status:** **OPEN** (atlas §7, Compression card).
- **Cluster:** VOLATILITY.
- **Canonical representative (must beat):** trailing realized volatility. Specifically must beat *"vol is simply low"* — the inverse-of-vol-level baseline.
- **Forest metaphor:** the unnatural stillness before the wind — a quiet, coiling path that may later expand.
- **Why interesting:** quiet/tight regimes plausibly precede expansion; a real "stored energy" story would be valuable.
- **Available data:** adj_close volatility-compression **2005–2022**; OHLC-range compression **2013–2022 only**.
- **Recommended version/window if promoted:** adjusted-close volatility-compression, **2005–2022** (the OHLC-range face would be 2013–2022 only and is not preferred at first promotion).
- **Window limitations:** OHLC-range face truncates to 2013–2022; adj_close face is full-span.
- **Governance risk:** **Medium-high — edge-hunting risk.** Compression's natural narrative ("quiet → breakout") slides easily into a **breakout trading strategy**, which violates the atlas's explanatory, non-edge-seeking charter (§1). Needs very careful null framing to stay explanatory.
- **Distinctness risk:** **HIGH.** Compression is **definitionally the inverse of vol level** (atlas: *"definitionally the inverse of vol level"*). To be distinct it must show that *low vol now* predicts forward path structure beyond what the *level* of trailing realized vol already predicts — a hard, narrow margin.
- **External-data risk:** None (price-only).
- **Budget-allocation argument:** Interesting but **not worth the first `0.01`.** The edge-hunting drift risk plus near-tautological relationship to the representative make it a poor first claim on a non-renewable budget. Better as a later attempt, after the framing discipline is proven on a cleaner first lane.
- **Overlaps CLOSED/RESERVED?** No, but is the literal mirror of Range expansion (also OPEN, not closed).
- **Price-only studyable?** Yes.
- **Suitable as first promoted force?** **No — defer.** Strong second-tier candidate; not the first pick.

---

### Candidate 3 — Drawdown / recovery

- **Atlas status:** **OPEN** (Drawdown card; Recovery card, partially DERIVED).
- **Cluster:** VOLATILITY (recovery has an autocorrelation-adjacent face).
- **Canonical representative (must beat):** trailing realized volatility. Drawdown must beat *"drawdown is largely vol × horizon"*; recovery must beat *"low vol recovers faster."*
- **Forest metaphor:** falling into a valley and climbing out — depth of the valley before the next ridge, and how fast the forest regrows.
- **Why interesting:** intuitive and tangible; mixes trend, volatility, and tail behavior into a path-shape story.
- **Available data:** adj_close **2005–2022**.
- **Recommended version/window if promoted:** adjusted-close drawdown depth, 2005–2022 — *but see suitability.*
- **Window limitations:** None beyond the standard 2005–2022 sandbox.
- **Governance risk:** **Medium — circularity hazard.** **Drawdown doubles as canonical outcome #2** (forward max drawdown). A drawdown *force* predicting a drawdown *outcome* risks restating the outcome family as a predictor; the design memo would have to firewall in-window trailing drawdown from the forward-drawdown target very carefully.
- **Distinctness risk:** **HIGH and compound.** Drawdown is *"largely vol × horizon"*; recovery is *"mechanically tied to drawdown depth and vol."* The force bundles three axes (trend + vol + tail), so isolating distinct content from the representative is harder than for a single-axis force.
- **External-data risk:** None (price-only).
- **Budget-allocation argument:** Potentially a good *later* lane, but **too complex for the first attempt.** First promotion should be the cleanest separable question available, not the one that bundles three axes plus an outcome-circularity hazard. Spending the family's first `0.01` here risks an uninterpretable result.
- **Overlaps CLOSED/RESERVED?** No.
- **Price-only studyable?** Yes.
- **Suitable as first promoted force?** **No — defer** (complexity + outcome-circularity).

---

### Candidate 4 — Zigzag

- **Atlas status:** **OPEN** (Zigzag card) — **but it is the killer baseline B6 that closed Curvature.**
- **Cluster:** VOLATILITY.
- **Canonical representative (must beat):** trailing realized volatility. **And** — because zigzag is *itself* the baseline that absorbed curvature — any *new* roughness force must beat **zigzag/B6 too**.
- **Forest metaphor:** how crooked the path between two clearings is.
- **Why interesting:** roughness/path-crookedness is intuitive; zigzag is the proven-strong roughness statistic.
- **Available data:** adj_close **2005–2022**.
- **Recommended version/window if promoted:** not recommended (see suitability).
- **Window limitations:** None beyond 2005–2022.
- **Governance risk:** **HIGH — closed-territory adjacency.** Zigzag/B6 is the exact statistic that killed the Cusp Geometry Lane. Promoting zigzag as a *force* (rather than a baseline) risks **functionally reopening the closed curvature/cusp territory** under a new name — which the atlas forbids (*"closed lanes stay closed"*). The anti-rescue principle (§9B) bars resurrecting a closed lane via relabeling.
- **Distinctness risk:** **HIGH.** Zigzag is *"near-collinear with realized vol"* and is itself a baseline; there is no obvious *new* distinct question it asks that isn't either (a) owned by realized vol or (b) the closed curvature question in disguise.
- **External-data risk:** None.
- **Budget-allocation argument:** **Not worth the first `0.01`,** and arguably not promotable at all without a genuinely new, distinct question that is provably not curvature/cusp re-entry. No such question is on the table.
- **Overlaps CLOSED/RESERVED?** **Yes — dangerously adjacent to CLOSED curvature/cusp.** This is the strongest single reason to defer.
- **Price-only studyable?** Yes.
- **Suitable as first promoted force?** **No — defer** unless a new, demonstrably-distinct question appears that is provably not closed-territory re-entry.

---

### Candidate 5 — Volatility-of-volatility

- **Atlas status:** **OPEN** (DERIVED — second moment of vol).
- **Cluster:** VOLATILITY.
- **Canonical representative (must beat):** trailing realized volatility (the **level**), plus simple volatility-change baselines.
- **Forest metaphor:** how gusty the wind itself is — not how hard it blows, but how erratically the gusts vary.
- **Why interesting:** a clean second-moment concept; potentially valuable for regime detection; scientifically tidy.
- **Available data:** adj_close **2005–2022**.
- **Recommended version/window if promoted:** adjusted-close vol-of-vol, 2005–2022 — *but see suitability.*
- **Window limitations:** None beyond 2005–2022.
- **Governance risk:** **Low-medium.** OPEN, price-only, not closed-adjacent. Mild DERIVED caveat (depends on the realized-vol definition being fixed first, which it is — vol is the cluster anchor).
- **Distinctness risk:** **HIGH.** Must beat vol level *and* show it is *"not just high-vol regions"* (atlas confound: estimation noise, overlaps regime). Second-moment estimates are noisy; separating vol-of-vol from vol level out-of-fold is demanding.
- **External-data risk:** None.
- **Budget-allocation argument:** Scientifically clean but **abstract and less intuitive** for a *first* promotion, and its distinctness margin against vol level is thin. A defensible *later* attempt; not the strongest first claim. Shock's sign-asymmetry framing offers a hypothesis the representative is *structurally blind to* (sign), whereas vol-of-vol competes with the representative on the same magnitude axis — a harder separation.
- **Overlaps CLOSED/RESERVED?** No.
- **Price-only studyable?** Yes.
- **Suitable as first promoted force?** **No — defer** (abstract; thin distinctness margin). Reasonable second or third later attempt.

---

### Candidate 6 — News magnitude / intensity

- **Atlas status:** **OPEN** (atlas Group 6) — but governed by hard NEWS/ATTENTION-cluster constraints.
- **Cluster:** NEWS/ATTENTION.
- **Canonical representative (must beat):** **coverage-normalized / drift-controlled** news/attention count (**not** raw count) — **and** trailing realized vol, **and** plain news count, for the forward absolute move / vol outcome.
- **Forest metaphor:** the intensity of sudden storms — not their direction, but how loud the thunder is.
- **Why interesting:** OPEN, and intensity/valence pressure is a plausibly real driver of absolute moves; the one non-price candidate with a clean OPEN status.
- **Available data:** GDELT count/feature builds and TTG event archives, **2013–2022 only**.
- **Recommended version/window if promoted:** would require a coverage-normalized / drift-controlled intensity measure, **2013–2022 only** — *not recommended first.*
- **Window limitations:** **Hard 2013–2022 ceiling** (shorter window → fewer sandbox events → less power per `0.01`).
- **Governance risk:** **HIGH.** News direction is **CLOSED**; GDELT raw-count/coverage is **CLOSED** (drift-confounded). Raw counts are **drift-confounded** and may appear only as read-only prior art, never as the baseline a new card beats. Any news-magnitude lane must build a coverage-normalized / drift-controlled attention measure *and* must not drift into closed news-direction territory.
- **Distinctness risk:** **HIGH** — must beat realized vol *and* plain count *and* survive drift control; the prior TTG magnitude-pressure arc was a **no-spend terminal** on the achievable seal.
- **External-data risk:** **HIGH** — the only candidate with a genuine external-data / collection-drift dependency. `collection drift` is a standing confound for the entire cluster.
- **Budget-allocation argument:** **Not worth the first `0.01`.** Shortest window, highest external-data and drift-control burden, closed-lane adjacency, and a prior no-spend terminal in the same family. A first promotion should minimize external dependencies, not maximize them.
- **Overlaps CLOSED/RESERVED?** Adjacent to **CLOSED** news direction and **CLOSED** GDELT raw-count.
- **Price-only studyable?** **No** — requires news/attention data.
- **Suitable as first promoted force?** **No — defer.**

---

### Candidate 7 — Calendar / time force

- **Atlas status:** **OPEN** (FULL-eligible for pure date-arithmetic dummies; specific event-calendar cells are STUB).
- **Cluster:** CALENDAR.
- **Canonical representative (must beat):** simple calendar dummy — and must not be a vol-seasonality restatement.
- **Forest metaphor:** the clock of seasons and market-hours rituals.
- **Why interesting:** trivially easy to define (date index only, no market values needed); FULL-eligible on the 2005–2022 index.
- **Available data:** trading-date index of any in-window price file, **2005–2022** (dates only; no values).
- **Recommended version/window if promoted:** not recommended (see suitability).
- **Window limitations:** None on dates; but event-calendars (OpEx/Fed/earnings) need external lists → those cells are STUB.
- **Governance risk:** **HIGH — pattern-mining risk + prior nulls.** The Harmonic Calendar studies already produced **SPY MVT null and GLD null**; the atlas instructs *"do not re-run those exact cells."* Many calendar cuts × shared family α = a multiple-comparison hazard explicitly flagged in the atlas card.
- **Distinctness risk:** **HIGH** — calendar effects must beat the plain dummy and not be vol-seasonality in disguise; and there is an in-program null record to clear.
- **External-data risk:** None for pure date-arithmetic dummies (external lists needed only for event-calendars).
- **Budget-allocation argument:** **Not worth the first `0.01`.** Prior nulls + high pattern-mining / multiple-comparison risk against a shared, non-renewable budget make calendar a poor first claim. Cheap to *define*, but expensive in family-α risk to *test*.
- **Overlaps CLOSED/RESERVED?** Not formally CLOSED, but the Harmonic Calendar cells are an in-program null record that constrains it.
- **Price-only studyable?** Yes (date index only).
- **Suitable as first promoted force?** **No — defer** (prior nulls + pattern-mining risk).

---

### Candidate 8 — Technical levels

- **Atlas status:** **STUB** (atlas §7 Group 2; owner-fixed Q4).
- **Cluster:** mostly VOLATILITY / price-derived (with an anchoring face).
- **Canonical representative (must beat):** would need both a defined level proxy *and* a cluster distinctness rule before it could even be specified.
- **Forest metaphor:** remembered waterlines / staring at an old high-water mark.
- **Why interesting:** watched levels (prior highs/lows, round numbers) are a folk-favorite driver.
- **Available data:** none clean — needs **watched-level data or a carefully defined level proxy**, neither inventoried.
- **Recommended version/window if promoted:** **N/A — not promotable.**
- **Window limitations:** N/A.
- **Governance risk:** **HIGH.** A price-only prior-high/prior-low proxy risks being **anchoring or range behavior wearing a technical-level mask** (atlas Q4). STUB status means it **cannot be fully specified**, and only FULL cards are promotion-eligible (atlas §10 step 1).
- **Distinctness risk:** **HIGH/undefined** — cannot be stated until the proxy and distinctness rule exist.
- **External-data risk:** **HIGH** — needs watched-level data not present.
- **Budget-allocation argument:** **Ineligible for the first `0.01`** — STUB forces are not promotable at all.
- **Overlaps CLOSED/RESERVED?** No, but risks masking range/anchoring behavior.
- **Price-only studyable?** **Not honestly** — a price-only proxy is the exact masking hazard the atlas warns against.
- **Suitable as first promoted force?** **No — ineligible (STUB).**

---

## 3. Shock distinctness — the decisive analysis (the user's preferred candidate, stress-tested)

The owner's preferred candidate is **Shock/jump → Aftershock Force**. This memo endorses it as the first pick **but only after relocating its distinctness claim**, because the generic-aftershock framing does not survive scrutiny. Distinctness is the central question for Shock, not a checkbox.

### 3.1 What Shock must beat

Conditioning on a shock means conditioning on a **large realized move**. **Three** baselines stand in the way:

1. **Sign-blind trailing realized volatility.** *"Large moves tend to be followed by large moves"* is **volatility clustering**, already owned by the cluster's canonical representative. The atlas Shock card concedes the mechanical overlap outright: *"jumps inflate realized vol itself."* So **generic symmetric aftershock magnitude is pre-conceded to trailing realized vol.** It cannot be the distinct content.

2. **Symmetric magnitude clustering.** A magnitude-only, sign-blind clustering baseline — the same content as (1) restated as a per-event clustering predictor. Generic symmetric "large move → large moves" belongs here and is conceded.

3. **A simple sign-aware volatility / leverage baseline.** Does the post-shock path differ for **down-shocks vs up-shocks** beyond what **magnitude alone** predicts? Trailing realized vol is **sign-blind** — it sees magnitude, not direction — so a *sign-conditional* difference is content the representative is structurally unable to capture. **But down/up asymmetry is not virgin territory:** leverage-effect-style asymmetry (down days raise forward volatility more than up days) is a **known market regularity**. So sign-conditional content is not automatically distinct either — it must also beat a **boring sign-aware baseline** (e.g. a signed-shock or negative-return volatility indicator). The exact sign-aware baseline formula is **not defined here**; it must be frozen in the future design memo before F1 (the Shock-asymmetry statistic) can count as distinct.

**The real narrow question** the future lane actually asks is therefore:

> *Do large down-shocks leave a qualitatively different wake than ordinary down-day leverage asymmetry already predicts?*

If they do not — if the apparent asymmetry is just the known leverage effect — then a future **null is respectable**, recorded as a finding.

### 3.2 The honest risk, named plainly

> **Shock may turn out to be volatility clustering plus down/up asymmetry — and the asymmetry may itself be nothing more than the known leverage effect.** If nothing survives beyond (1) sign-blind trailing realized vol, (2) symmetric magnitude clustering, and (3) a simple sign-aware leverage baseline — i.e. if even the asymmetry dissolves into ordinary down-day leverage asymmetry — then a future null would be **respectable**, recorded as a finding, not a failure. The atlas's Cusp v0.3 null is the template.

### 3.3 Reframed, not generic — adopted

This memo **adopts the asymmetry reframing** and **relocates the distinctness claim** rather than keeping a generic "aftershock" story:

- The recommended first promotion **remains `Shock/jump → Aftershock Force`.**
- **Generic symmetric "large move followed by large moves" is pre-conceded** to the VOLATILITY cluster and trailing realized volatility; it is *not* the hypothesis.
- **The promotable hypothesis is not generic aftershock magnitude.** It is **whether down-shocks and up-shocks of comparable standardized magnitude leave different future path shapes** — i.e. does the wake after a *down* shock differ from the wake after an *up* shock of comparable standardized magnitude, beyond what magnitude/vol and the known leverage effect already predict?

> **The distinctness claim lives on the sign-conditional asymmetry axis. Without that asymmetry framing, Shock is not a suitable first promotion because symmetric aftershock behavior belongs to volatility clustering.**

So the answer to *"reframed as asymmetry or kept as generic aftershock?"* is: **reframed — the force is promoted as Shock/jump, but its distinctness claim is explicitly moved onto down/up (sign-conditional) asymmetry**, which must itself clear the sign-aware leverage baseline (§3.1). Generic aftershock is retained only as the null-prone framing whose failure would be a respectable null.

### 3.3a Impulse-vs-reversal firewall

The future Shock design memo must pre-register the following firewall **before any data contact**:

- A **Shock event is a single-step impulse-magnitude exceedance** — one large standardized return.
- A **Cusp/reversal event was a two-vertex reversal geometry** and is **CLOSED** through the **Cusp Geometry Lane v0.3** (curvature absorbed by zigzag/B6; do not reopen).
- These are **different objects**, but they **overlap when a shock is immediately reversed** (a shock that is followed by a sharp move back is also, geometrically, a near-vertex/reversal).
- The future Shock design memo must **run the asymmetry test on all qualifying shocks**, not quietly filter down to the **shocks-that-reverse** subset.
- **Filtering to shocks-that-reverse would be Cusp/reversal re-entry through the side door** (anti-rescue principle, atlas §9B) — resurrecting a CLOSED lane under a new name.
- If any apparent signal **survives only inside the shocks-that-reverse subset**, the Shock lane must report this as **contamination / closed-lane overlap, not as a positive Shock finding.**

> **If the surviving signal lives only in shocks-that-reverse, it is not a Shock finding; it is Cusp/reversal re-entry, and the lane must report contamination rather than success.**

This tripwire must be **pre-registered in the future design memo before any data contact.**

### 3.3b Parameters belong in the design memo, not here

This decision memo **chooses the force and version only.** It does **not** authorize data contact or parameter selection. The following are **frozen in the future design memo, not here:**

- the **shock threshold** (what standardized-return magnitude qualifies as a shock),
- the **volatility estimator** used to standardize,
- the **matching rule** (how down-shocks and up-shocks of "comparable standardized magnitude" are paired),
- the **outcome target** (which canonical outcome / wake statistic),
- the **baselines**, including the **exact sign-aware leverage baseline** (§3.1).

No threshold, estimator, or baseline formula is selected, tuned, or implied by this memo.

### 3.4 Is the reframed force still the best first pick?

**Yes.** Even reduced to its sign-asymmetry core, the reframed Shock force is the strongest first claim because it uniquely combines:

- a distinct hypothesis the representative is **structurally blind to** (sign), unlike Compression / Vol-of-vol / Drawdown, which all compete with realized vol on the **same magnitude axis**;
- the **longest available window** (2005–2022, adjusted-close-only — full span, no truncation);
- **zero external-data / vintage / drift dependency** (price-only), unlike News magnitude;
- the **lowest governance risk** (OPEN, not closed-adjacent), unlike Zigzag (curvature re-entry), Calendar (prior nulls), News (closed-lane adjacency), Technical levels (STUB);
- no outcome-circularity hazard, unlike Drawdown (which doubles as canonical outcome #2).

### 3.5 Window resolution (no silent mixing) — confirmed

- **Recommended (confirmed):** *Shock/jump, **adjusted-close-only** version, **SPY 2005–2022** sandbox-capable.*
- **Deferred (confirmed):** *Shock with volume confirmation, 2013–2022 only — deferred because it **collapses the usable window to 2013–2022** without enough first-promotion benefit.*
- **No windows are mixed.** A 2005–2022 adjusted-close result may not be silently compared with or blended into a 2013–2022 volume-confirmed result (atlas §6A).
- Any future **volume-confirmed version** would require a **separate future design decision and its own frozen design memo** — it is not authorized, implied, or pre-approved by this memo.

---

## 4. Ranking of candidates as *first* promoted force

Ranked by suitability **as the first claim on the shared sealed budget** (interest is necessary but not sufficient; distinctness, window length, governance cleanliness, and external-data burden decide it):

1. **Shock / jump — adjusted-close-only, 2005–2022, asymmetry-framed.** **RECOMMENDED.** Distinct hypothesis the representative is sign-blind to; full window; price-only; cleanest governance.
2. **Compression — adj_close, 2005–2022.** Interesting, full window, price-only, but edge-hunting drift risk + near-tautological inverse-of-vol distinctness. Strong second-tier; not first.
3. **Volatility-of-volatility — adj_close, 2005–2022.** Clean and full-window but abstract; competes with realized vol on the same magnitude axis (thin margin).
4. **Drawdown / recovery — adj_close, 2005–2022.** Intuitive but bundles three axes and carries outcome-circularity (drawdown = canonical outcome #2). Too complex for first.
5. **Calendar / time — date index, 2005–2022.** Easy to define but prior Harmonic Calendar nulls + high pattern-mining / multiple-comparison risk against shared α.
6. **News magnitude / intensity — drift-controlled, 2013–2022.** OPEN but shortest window + highest external-data/drift burden + closed-lane adjacency + prior no-spend terminal.
7. **Zigzag — adj_close, 2005–2022.** Dangerously adjacent to CLOSED curvature/cusp (it *is* the B6 killer baseline); risks reopening closed territory; no new distinct question on the table.
8. **Technical levels.** **Ineligible** — STUB; not fully specifiable; not promotable on a price-only proxy (anchoring/range mask hazard).

---

## 5. Recommendation and fallback

**Recommended first promotion candidate:**

> **Shock/jump — adjusted-close-only, SPY 2005–2022, sign-conditional asymmetry framed.**

**Budget-allocation rationale (why this gets the family's first potential `0.01`):** of the eight, it is the only candidate that pairs a distinct hypothesis the canonical representative is *structurally blind to* (sign asymmetry) with the longest available window (2005–2022), zero external-data/vintage/drift dependency, the lowest governance risk, and no outcome-circularity. Every other candidate is weaker on at least one of those axes — and the first attempt on a five-deep, non-renewable shared budget should be the cleanest separable question available, not the most elaborate or the most externally-dependent one.

**Fallback candidate:**

> **Compression — named fallback only, not authorized.**

- Compression (adjusted-close volatility-compression, 2005–2022) is the **named fallback** should Shock's design memo fail to freeze cleanly.
- **Naming it as fallback does not authorize design, testing, or any parallel work.**
- `MAX_ACTIVE_ATLAS_LANES = 1`: **Compression cannot begin design while Shock is active.**
- Compression may be **reconsidered only after Shock resolves/closes or is formally abandoned.**

**Next step, if owner approves:**

> **Draft frozen design memo for Shock/jump asymmetry; no data contact until reviewed and frozen.**

The frozen design memo follows the Cusp-lane pattern (statistic/proxy · canonical outcome · baselines · the three distinctness baselines from §3.1 [sign-blind trailing realized vol + symmetric magnitude clustering + a frozen sign-aware leverage baseline] · the §3.3a impulse-vs-reversal firewall tripwire · sandbox gate · sealed rule · multiple-testing ledger entry). The shock threshold, volatility estimator, matching rule, outcome target, and baseline formulas are decided **there**, not here (§3.3b). A sandbox FAIL would close the lane as exploratory null and debit nothing; sealed contact (and the first `0.01` debit) would require a sandbox PASS plus explicit owner authorization.

---

## 6. Owner decisions and remaining open questions

**Resolved by owner this revision:**

1. ~~Adopt the asymmetry reframing?~~ — **RESOLVED: adopted** (§3.1, §3.3). Distinctness claim lives on the sign-conditional asymmetry axis; generic symmetric aftershock is pre-conceded to volatility clustering.
2. ~~Window confirmation?~~ — **RESOLVED: adjusted-close-only SPY 2005–2022 confirmed; volume-confirmed shock deferred** (collapses window to 2013–2022); any future volume-confirmed version needs its own separate design decision and frozen memo (§3.5).
3. ~~Threshold/estimator location?~~ — **RESOLVED: deferred to the future frozen design memo** (threshold, estimator, matching rule, outcome target, baselines). This decision memo chooses force/version only and authorizes no data contact or parameter selection (§3.3b).
4. ~~Cusp firewall?~~ — **RESOLVED: impulse-vs-reversal firewall added** (§3.3a). The design memo must run the asymmetry test on all qualifying shocks and pre-register the shocks-that-reverse tripwire before any data contact.
5. ~~Sign-aware leverage baseline?~~ — **RESOLVED: added to the distinctness bar** (§3.1). F1 must beat a frozen sign-aware leverage baseline, not only sign-blind vol + symmetric clustering. The exact formula is frozen in the design memo, not here.
6. ~~Named fallback?~~ — **RESOLVED: Compression named as fallback only, not authorized** (§5); cannot begin design while Shock is active (`MAX_ACTIVE_ATLAS_LANES = 1`).

**Still open (for the future design memo, not this memo):**

- **A.** Exact shock threshold and volatility estimator (frozen in the design memo).
- **B.** Exact sign-aware leverage baseline formula (frozen in the design memo).
- **C.** Exact down/up "comparable standardized magnitude" matching rule and the chosen wake/outcome statistic from the canonical family (frozen in the design memo).
- **D.** Exact pre-registered form of the §3.3a shocks-that-reverse contamination tripwire (frozen in the design memo, before any data contact).

---

## 7. Standing confirmations

- **This decision memo does not authorize testing.** It only recommends which force should be considered first for a future design memo.
- No force is promoted by this memo. Promotion requires a separate, reviewed, frozen, hash-pinned design memo (atlas §3, §10).
- Closed lanes stay closed; reserved lanes stay reserved; no promoted lane receives a fresh independent sealed-alpha budget.
- No tests run · no modeling run · no tuning run · no sealed values inspected · no sealed data accessed · nothing staged · nothing committed · nothing pushed.

*Draft ends. Awaiting owner review.*
