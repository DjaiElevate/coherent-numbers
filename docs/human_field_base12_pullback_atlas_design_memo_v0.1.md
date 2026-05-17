# Human Field × Base-12 Pullback Atlas — Design Memo v0.1

**Version:** v0.1 (Exploratory atlas design memo — revised 2026-05-17: three design decisions accepted; realized-volatility arousal proxy replaces VIX)
**Date:** 2026-05-17
**Project:** Coherent Numbers
**Artifact type:** Atlas design memo (Lane 1 only)
**Status:** Draft. No analysis authorized. No data run. No implementation created. No OOS contact. Awaiting review.

**Accepted design decisions (locked into this revision):**

- **Decision 1 — single-anchor labels.** The atlas uses Candidate C's single civil-date March-20 anchor for deterministic base-12 and base-10 phase labels. It does **not** use Candidate C's 365-DOY anchor surface, permutation nulls, median-over-surface statistic, or verdict apparatus — those belonged to Candidate C's confirmatory comparison. Atlas v0.1 needs one deterministic phase label per trade per base. (Reflected in §5, §6, §9 Grid 4, §16.)
- **Decision 2 — `r_multiple` outcome.** The atlas uses `r_multiple` as the v0.1 outcome because the frozen Phase 3b compact schema carries `r_multiple` and contains no `fixed_horizon_outcome` and no post-entry price path. No fixed-horizon outcome is added in v0.1. A future fixed-horizon-Y study is a separate design decision requiring full price-path data. (Reflected in §7.)
- **Decision 3 — `indeterminate-state` rule.** Missing or insufficient nervous-system data receives a reserved `indeterminate-state` label, is retained in the full grids and the sparsity report, and is excluded from candidate-hypothesis formation on the same footing as low-data cells. This rule is fixed before any atlas generation. (Reflected in §8.4, §10.)

**Reference commits (context only — not subject to revision here):**

- Candidate C design memo (locked): `401ce45` — `docs/candidate_c_design_memo_v0.1.md`
- Candidate C lock-acceptance: `dc97576` — `docs/candidate_c_design_memo_v0.1_lock_acceptance.md`
- Candidate C verdict log: `a19b2e9` — `results/candidate_c_results_20260515_051236_f3a6bf48.{json,md}`
- Candidate C closure: `1659819` — `docs/candidate_c_closure_memo_v0.1.md`
- Pullback population freeze manifest: `5225bfd` — `docs/pullback_population_freeze_manifest_v0.1.md`

---

## 1. Title, date, status

**Title.** Human Field × Base-12 Pullback Atlas v0.1.

**Date.** 2026-05-17.

**Status.** This is an **exploratory atlas design memo**, not a confirmatory cell design memo. It does not follow the locked-protocol / verdict-map template of Candidate B or Candidate C. It has:

- no success criterion;
- no verdict language;
- no p-value as final evidence;
- no OOS access;
- no confirmation claim;
- no rescue framing;
- no profitability framing.

The only output of the work this memo describes is a **structured atlas** (full descriptive grids) plus a list of **candidate hypotheses** for possible future testing on data not used here. The full grid is always reported; interesting cells are never curated in isolation. 2023+ remains sealed. Any future confirmation of any atlas-seeded hypothesis requires data not used in the atlas.

> **The atlas does not validate any hypothesis. It describes joint structure in a discovery set and generates candidate hypotheses for future testing on fresh data.**

## 2. Purpose

Two structures in this program have already spoken, independently, under their own locked or frozen disciplines:

1. The **pullback population** — the frozen Phase 3b pooled 1,282-trade substrate (SPY/EFA/EEM/GLD/TLT, 2005–2022). Its directional/allocation behavior was characterized during pullback research and re-used under Candidate B and Candidate C.
2. **Candidate C's base-12 vs base-10 phase structure** — Candidate C closed **12-privileged (Class 1)** under its locked protocol: the 12-bucket annual-sector partition organized long/short allocation on this substrate better than the 10-bucket partition (`beat_count_comparison_12 = 9973/10000`, both individual nulls `10000/10000`), bounded by its §12.2(b) and §12.4 disclosures.

The atlas asks one **descriptive discovery question**:

> When we lay the already-spoken pullback structure and the already-spoken Candidate C base-12 structure side by side against a simple market nervous-system state, how do they co-express?

This is discovery mode. The atlas produces a map and candidate hypotheses. It does not produce proof, a verdict, or confirmation. It does not test anything. It describes what the discovery set looks like when these three already-independent structures are cross-tabulated, and it records — with equal status — the possibility that no joint structure appears.

## 3. Atlas vs rescue distinction

This atlas is explicitly **not** any of the following:

- **Not a rescue of any prior null.** It does not attempt to recover, reinterpret, or upgrade Candidate B's Split-null, the SPY MVT null, the GLD null, or the trade-level field-modulated identity null.
- **Not the later trade-level field-modulated identity study.** That study has its own design memo, lock-acceptance, scoping study, and verdict (`docs/influential_numbers_field_modulated_identity_*`, `docs/field_modulated_identity_trade_level_*`). The atlas is not a continuation, reinterpretation, or rescue of it.
- **Not a confirmatory retest** of Candidate C or anything else. There is no locked statistic, no null, no threshold, no verdict map.
- **Not an OOS replication.** No 2023+ data is read, joined, previewed, or computed against.
- **Not the Attention-Spike Market Response study.** See §4 (Lane separation). That is a different substrate and a different design and is out of scope here.

The atlas is an **exploratory map of structures that have already spoken independently**. Its inferential standing is therefore strictly that of a discovery set: anything visible in it is a candidate hypothesis, never a result.

## 4. Lane separation

This memo authorizes **Lane 1 only**.

**Lane 1 — this atlas (in scope):**

- Pullback events/trades from the frozen Phase 3b pooled population.
- Candidate C base-12 / base-10 annual phase structure (the locked Candidate C lens, re-used descriptively).
- A simple market nervous-system state (§8).
- The existing frozen 2005–2022 discovery substrate only.

**Lane 2 — separate future study (explicitly out of scope here):**

- Attention-spike market response.
- GDELT / news-flow / collective-attention event series.
- S&P 500 event-window response design.
- Prior fear/greed state as an event-window conditioner.
- A different substrate and a different design from Lane 1.

Lane 2 **is not derived from this atlas** and must not be merged into Atlas v0.1. Nothing in the atlas seeds, justifies, or pre-shapes Lane 2. Lane 2 may be considered later, entirely on its own merits, in its own framework/design artifacts. If Lane 1 and Lane 2 are ever related in future work, that relationship must be argued explicitly in a separate memo and may not be assumed by proximity in this program.

## 5. Substrate

The atlas uses the **frozen Candidate C / Phase 3b pullback population**, unchanged:

- **1,282 trades** — pooled across SPY/EFA/EEM/GLD/TLT.
- Per-asset frozen row counts (from the freeze manifest at `5225bfd`): SPY 243, EFA 283, EEM 261, GLD 253, TLT 242. Sum = 1,282.
- **Window:** 2005–2022 (earliest frozen `entry_date` 2005-02-04, latest 2022-12-21; all `entry_date`/`exit_date` ≤ 2022-12-31 per the freeze manifest OOS sanity check).
- **Universe:** SPY, EFA, EEM, GLD, TLT.
- **Phase definitions:** the **same base-12 and base-10 annual phase definitions as Candidate C** — the parameterized March-20-anchored annual-sector formula of Candidate C design memo §7.1 (`phase = floor(days_since_start × k / cycle_length_days)`, `k ∈ {10, 12}`, civil-date March-20 anchor, assertion-and-abort range check). The atlas uses the **single civil-date March-20 anchor only** (Candidate C §7.1). It does **not** run Candidate C's 365-DOY anchor surface, its permutation nulls, or its median-over-surface statistic. The atlas needs only a single deterministic phase label per trade per base; the anchor-surface machinery is confirmatory apparatus and is not part of an atlas.
- **2023+ untouched and sealed** in both this repo and the pullback repo. The pullback repo's HEAD is not consulted. Only the frozen CSV substrate at manifest `5225bfd` is read.

**This is a discovery substrate, not a confirmatory one.** It has already been contacted: by pullback research Phases 1–3b (series inspected, partitioned, used to estimate within-population statistics; `BacktestParams` locked at pullback `50ee2d1`), by Candidate B (12-phase March-20 machinery + nulls), and by Candidate C (parallel 12-/10-phase machinery + nulls). Every structure the atlas can see in this substrate is therefore discovery-set structure by construction. No amount of atlas detail changes that standing.

### 5.1 Substrate-extension note (auxiliary context series)

The frozen Phase 3b CSVs use the 11-column compact schema (`entry_date, setup_date, direction, entry_price, exit_price, exit_date, exit_reason, bars_held, r_multiple, first_target_hit, initial_risk`). They contain **no market index level series and no volatility series**. The nervous-system state (§8) requires one auxiliary daily series: a frozen SPY adjusted-close series, from which **both** axes are derived — the 30-trading-day return (valence) and the 20-day realized volatility percentile (arousal). This is an **auxiliary context feature**, not a modification to the frozen pullback substrate:

- The frozen pullback CSVs are read-only and unchanged. No column is added to them, no row filtered, recoded, or re-signed.
- The auxiliary SPY series is joined **only by date**, using values available strictly at or before `t-1` relative to the event date (§8), to attach a context label to each trade.
- **The required auxiliary series is already frozen in the repo.** The artifact is `data/raw/spy_yahoo_v8_19930129_20241231_e8fc0357410ce499da8f67e09b4c9908232e18a55445f38969e77fa712aaaa56.csv` (frozen at commit `ed199bd`, frozen-CSV loader architecture at `30faabb`), schema `date,adj_close`, spanning **1993-01-29 → 2024-12-31**. This span covers 2005–2022 with ample trailing history for both the 30-trading-day return window and the 252-trading-day realized-volatility percentile window. The atlas re-uses this frozen artifact **read-only**. No new external data freeze is introduced for Atlas v0.1.
- **OOS guard.** The frozen SPY artifact extends to 2024-12-31, into the sealed 2023+ window. The atlas consults this series **only** at sessions on or before `t-1` for each trade, and every trade's `entry_date` is ≤ 2022-12-21 (freeze manifest OOS sanity check). All trailing-window computations therefore terminate on sessions ≤ 2022, and **no 2023+ row of the SPY artifact is ever read, joined, or computed against**. This is a hard read boundary in the design, not a runtime check.

**Arousal-proxy substitution (required wording).**

> Atlas v0.1 uses realized volatility from frozen SPY data as the arousal proxy instead of VIX. This is appropriate for exploratory atlas use because the goal is to classify prior market activation/calm using already-frozen data without introducing a new external data freeze. VIX or another implied-volatility series would be the preferred arousal proxy for any later confirmatory study if the candidate hypothesis specifically requires forward-looking fear/volatility pricing.

No claim is made here about the numerical relationship between realized volatility and VIX. None is needed for an exploratory atlas, and none is asserted. If a later confirmatory study requires implied-volatility pricing, acquiring and freezing a VIX-style series under the standard SHA-256-pinned manifest discipline is that study's prerequisite, not this atlas's.

## 6. Candidate C provenance

Verified by direct read of the Candidate C artifacts:

- **What Candidate C compared.** A 12-bucket annual-sector partition vs a 10-bucket annual-sector partition, both via the March-20-anchored parameterized formula (Candidate C design memo §7), over an exhaustive 365-DOY anchor surface absorbed into a median PSS statistic.
- **Substrate.** The frozen pooled Phase 3b 1,282-trade population (manifest `5225bfd`) — the same substrate this atlas uses.
- **Metric.** PSS = η²/correlation ratio `between_k / total_k` measuring how much of long/short allocation (`is_long`) is explained by phase labels (Candidate C §9.1).
- **Result.** **12-privileged (Class 1).** `median_12_observed ≈ 0.03444590`, `median_10_observed ≈ 0.02985119`, `diff_observed ≈ +0.00459471`. Beat counts: `beat_count_12_individual = 10000`, `beat_count_10_individual = 10000`, `beat_count_comparison_12 = 9973`, `beat_count_comparison_10 = 27`.
- **Scope.** Candidate C's §12.2(b) and §12.4 disclosures are load-bearing: the result does **not** establish 12 as uniquely privileged among all bucket counts (only 10 was tested), does **not** attribute the edge to a duodecimal property vs a substrate feature at this temporal resolution, does **not** rescue Candidate B, and does **not** generalize beyond the pre-registered substrate. The comparison is between two temporal resolutions (≈30.4 vs ≈36.5 days/bin), not a claim about which resolution is "correct."

This atlas inherits Candidate C's phase **labels** as a descriptive lens. It does **not** inherit, re-run, or reinterpret Candidate C's statistic, nulls, anchor surface, or verdict map. See §16 for the full relationship statement.

## 7. Core variables

For each pullback trade in the frozen pooled Phase 3b population, the atlas attaches or computes the following row attributes. No new bases are introduced; base-10 is present **only** as Candidate C's comparator.

| Variable | Definition / source |
|---|---|
| `trade_id` | Stable identifier within the frozen artifact (asset + frozen row index). |
| `date` | `entry_date` as recorded in the frozen CSV (the Candidate C primary phase-assignment date). |
| `asset` | One of {SPY, EFA, EEM, GLD, TLT}. |
| `direction` | long / short, derived from the frozen `direction` column with no re-signing. |
| `phase_12` | Base-12 annual phase ∈ {0..11}, via Candidate C §7.1 civil-date March-20 formula. |
| `phase_10` | Base-10 annual phase ∈ {0..9}, via the same formula with `k = 10`. Comparator only. |
| `r_multiple` | Signed trade outcome **as recorded** in the frozen CSV. Used exactly as stored — no multiplication by direction, no re-signing, no transformation (Candidate C Appendix B.5 convention). |
| `fixed_horizon_outcome` | **Not used in v0.1 (Decision 2, accepted).** The compact 11-column schema carries no fixed-horizon column and the frozen CSVs carry no post-entry price path, so v0.1 has no fixed-horizon outcome; `r_multiple` is the sole outcome measure. A future fixed-horizon-Y study is a separate design decision requiring full price-path data, never an v0.1 default. |
| `prior_30d_spy_return` | Trailing 30-trading-day simple return of the frozen SPY adjusted-close series, over the window **ending at `t-1`** (the last SPY session strictly before `entry_date`), never including the event day (§8). |
| `prior_rvol_pctile_252` | Percentile rank of 20-trading-day SPY realized volatility (rolling standard deviation of daily SPY log returns over the prior 20 trading days ending at `t-1`, not including the event day) within its trailing 252-trading-day window, also ending at `t-1` (§8). Replaces the earlier VIX-percentile variable. |
| `ns_state` | Nervous-system state label ∈ {calm bull, manic/unstable rally, panic/crisis, quiet bearish/exhaustion, `indeterminate-state`} (§8). |

**No additional bases in v0.1.** Base-10 is included only because Candidate C used it as the comparator. The atlas does **not** add base-7, base-8, base-9, base-11, base-13, or any other bucket count. Adding bases is out of scope for v0.1 and would require a separate memo.

## 8. Nervous-system state definition

A deliberately **simple, pre-committed, 2-axis** state. No tuning. No optimization. No post-hoc threshold adjustment.

All signals derive from the single frozen SPY adjusted-close artifact (§5.1). Let `t` = `entry_date` and `t-1` = the last SPY session strictly before `t`.

### 8.1 Valence axis

- Signal: prior 30-trading-day SPY simple return over the window **ending at `t-1`** (not including the event day).
- **Positive valence** if prior 30-trading-day return `> 0`.
- **Negative valence** otherwise (≤ 0).

### 8.2 Arousal axis (realized volatility from frozen SPY — replaces VIX)

- Return series: daily SPY log returns from the frozen adjusted-close artifact.
- Realized volatility: rolling **20-trading-day** standard deviation of daily SPY log returns.
- **Standard-deviation convention (locked, not an open question).** Atlas v0.1 computes realized volatility as the 20-trading-day sample standard deviation of SPY daily log returns, `ddof=1`. Because the window length is fixed at 20 sessions, changing `ddof` would multiply every rolling volatility value by a constant factor and therefore would not change percentile ranks under complete fixed-length windows. `ddof=1` is retained as the documented sample-volatility convention.
- Timing: use the prior **20 trading days ending at `t-1`**, not including the event day (no event-day leakage).
- Percentile: realized-volatility percentile within a trailing **252-trading-day** window also **ending at `t-1`**.
- **High arousal** if percentile `≥ 75%`.
- **Low arousal** if percentile `< 75%`.

### 8.3 Five states (fixed display order)

1. **calm bull** — positive valence + low arousal.
2. **manic / unstable rally** — positive valence + high arousal.
3. **panic / crisis** — negative valence + high arousal.
4. **quiet bearish / exhaustion** — negative valence + low arousal.
5. **`indeterminate-state`** — insufficient or missing state data (§8.4). Retained in the full grids and the sparsity report; **excluded from candidate-hypothesis formation** on the same footing as low-data cells. Displayed last and visually distinct (§11).

### 8.4 No-leakage and missing-data rules (design-level, pre-committed)

- **No future leakage.** Both axes use only SPY sessions **at or before `t-1`**. The 30-trading-day return window, the 20-trading-day realized-volatility window, and the 252-trading-day percentile window all **end at `t-1`** and never include the event day or later. (Decision 1's single-anchor phase labels are likewise deterministic from `entry_date` alone and contact no future data.)
- **Insufficient trailing history.** If fewer than the required trailing SPY sessions are available before `t` to populate the 30-day, 20-day, or 252-day window (the frozen SPY artifact starts 1993-01-29, so this is not expected on the 2005–2022 trades but the rule stands regardless), the trade's `ns_state` is set to the reserved label **`indeterminate-state`**. Such trades are **retained in the substrate and in the full grids** under `indeterminate-state` and are **excluded from candidate-hypothesis formation** exactly as low-data cells are (§10). The count of `indeterminate-state` trades is reported in the sparsity report (§10).
- **Missing SPY rows.** If the frozen SPY series has a true gap such that a required window cannot be populated from sessions on or before `t-1` (a genuine missing-data gap, not a weekend/holiday — for weekends/holidays the last available prior session is used), the trade is labeled `indeterminate-state` and handled as above.
- The decision rule for missing/short-history data is fixed **here, before any run**, and is **not** to be revisited by looking at how many trades fall into `indeterminate-state` or where they land.
- The decision rule for missing/short-history data is fixed **here, before any run**, and is **not** to be revisited by looking at how many trades fall into `indeterminate-state` or where they land.

## 9. Required atlas grids

All grids below are **pre-committed**. They are **descriptive**. They are **not a menu of success routes** and there is no rule by which any grid "passes." Every grid is reported in full, including all low-data and `indeterminate-state` cells.

- **Grid 1 — Event count:** base-12 phase (0–11) × nervous-system state → number of trades.
- **Grid 2 — Long percentage:** base-12 phase × nervous-system state → percent of trades that are long.
- **Grid 3 — Outcome:** base-12 phase × nervous-system state → median `r_multiple` (and median fixed-horizon outcome only if one exists per §7; in v0.1, `r_multiple` only).
- **Grid 4 — State-level PSS_12 vs PSS_10:** within each nervous-system state, the descriptive Candidate-C-style η² correlation ratio of `is_long` on `phase_12` and on `phase_10`, reported side by side as plain descriptive numbers. **No null, no permutation, no threshold, no beat count, no verdict.** This is a descriptive re-use of the η² *form* only, not Candidate C's statistic-with-null.
- **Grid 5 — Asset × phase × state:** asset × base-12 phase × nervous-system state → event count and long percentage. **Expected to be sparse** (5 assets × 12 phases × 4 states = 240 cells before any direction split; with 1,282 trades the average cell holds ≈ 5 trades). Grid 5 is a **diagnostic**, not a narrative source.
- **Grid 6 — Direction splits:** long-only and short-only breakdowns of Grids 1–3.
- **Grid 7 — Sparsity report:** per-grid cell-count / sparsity report (§10), including the `indeterminate-state` count.
- **Grid 8 — Base-10 comparator views:** base-10 versions of Grids 1–4 matched view-for-view, presented **only** as Candidate C's comparator, **not** as a new search surface. Base-10 is shown to mirror Candidate C's own contrast, never as an additional place to hunt for patterns.

These grids are descriptive cross-tabulations of a discovery set. They are not hypotheses, not tests, and not evidence.

## 10. Sparsity threshold and low-data handling

A single hard, descriptive threshold, fixed here:

- **Any cell with fewer than 20 events is flagged `low-data`.**
- Low-data cells are **still reported** in the full grid (full grid always shown).
- Low-data cells are **excluded from the descriptive narrative and from candidate-hypothesis formation**.
- If a visually interesting pattern depends mainly on cells with `n < 20`, it is labeled **"low-data visual noise candidate only"** and **cannot become a serious candidate hypothesis**.
- The **sparsity report (Grid 7)** must show, for each grid: total cells, number of cells below threshold, fraction of total events sitting in below-threshold cells, and the `indeterminate-state` trade count.
- `indeterminate-state` trades (§8.4) are reported in the full grids and the sparsity report and are excluded from candidate-hypothesis formation on the same footing as low-data cells.

**Grid 5 expectation, stated up front:** asset × 12 phases × 4 states = 240 cells before direction splits; ≈ 5 trades/cell average on 1,282 events. Grid 5 is therefore **expected to be predominantly low-data** and is to be used as a **diagnostic only**, never as a source of strong narrative or serious candidate hypotheses. Any apparent asset-specific structure that lives mostly in Grid 5 is, by this pre-commitment, a low-data visual-noise candidate at best.

## 11. Visualization rules

Visualization choices are degrees of freedom and are therefore **fixed before atlas generation**:

- Base-12 phases are ordered **chronologically 1→12** (equivalently 0→11). No clustering, no similarity reordering, no permutation of phases.
- Nervous-system states always appear in this order: **(1) calm bull, (2) manic/unstable rally, (3) panic/crisis, (4) quiet bearish/exhaustion**. `indeterminate-state`, when shown, appears last and is visually distinct.
- Assets always appear in this order: **SPY, EFA, EEM, GLD, TLT**.
- A **single color scale** is used across comparable heatmaps; **consistent scale bounds** across grids where the measure is comparable (e.g., all long-percentage heatmaps share one bound; all η² heatmaps share one bound).
- **Neutral/default plotting styles.** No color scale is tuned to make any pattern look stronger or weaker. No emphasis annotations beyond the mandated low-data marking.
- **Every heatmap** either includes per-cell counts or is paired with a per-cell count table.
- **Low-data cells are visually marked or annotated** (e.g., hatched / greyed / asterisked) on every heatmap, as are `indeterminate-state` cells.

If any visualization choice is found to be underspecified during implementation, it is resolved by a written addendum to this memo **before** generation, not by trying alternatives on the data.

## 12. Descriptive-language rules

The atlas summary and closure must use descriptive language only. Permitted forms (examples):

- "This cell contains X events."
- "The long percentage in this cell is Y."
- "PSS_12 is higher / lower than PSS_10 in this state."
- "This apparent pattern is concentrated in cells below the sparsity threshold."
- "This pattern is visible in the discovery set and requires fresh-data confirmation."

Forbidden language (examples — not exhaustive; the spirit governs):

- "This proves base-12 works in panic states."
- "This confirms consciousness affects markets."
- "This explains the pullback signal."
- "This validates influential numbers."
- "This rescues the failed scoping study."

No verdict words ("confirmatory", "privileged", "passes", "significant-therefore-true"), no causal claims, no profitability claims, no claim that the atlas settles any question.

## 13. Candidate hypothesis policy

After the full grids are generated, the atlas may record a list of **candidate hypotheses**. Policy:

- Candidate hypotheses are **discovery-set-only** observations phrased as questions for possible future testing on data not used in the atlas.
- They must be grounded in the **pre-committed grids** (§9), not in any post-hoc re-slicing.
- They must **not** rely on low-data or `indeterminate-state` cells as serious support; any candidate that does is downgraded to "low-data visual-noise candidate only."
- Every candidate is explicitly labeled **discovery-seeded, not confirmed**.
- The candidate list is bounded by what the fixed grids show; it is not an open-ended brainstorm and is not a route to a conclusion.
- The example candidates in §11-of-the-task (reproduced in §13.1 below and the null in §14) are **examples only**. The actual post-generation list must be re-derived from the grids and may differ.

### 13.1 Example candidate hypotheses (illustrative only)

- **Candidate H1:** Base-12 allocation structure appears strongest in high-arousal states.
- **Candidate H2:** The 12-over-10 advantage appears concentrated in negative-valence / high-arousal states.
- **Candidate H3:** The joint structure appears to live in long/short allocation rather than outcome magnitude.
- **Candidate H4:** The joint structure appears asset-specific rather than universe-wide.
- **Candidate H5:** The joint structure appears concentrated in one asset or one direction.
- **Candidate H0:** No coherent joint structure appears (see §14).

These are worded as examples to illustrate the *form* a candidate may take. They are not predictions, not preferred outcomes, and not a checklist. The atlas does not aim at any of them.

## 14. Equal-weight null / no-joint-structure candidate

The candidate-hypothesis section must carry, with **equal status** and no framing as disappointment or fallback:

> **Candidate H0.** No coherent joint structure appears. Candidate C remains a standalone base-12 vs base-10 structural result, and the pullback population remains independently interesting, but the atlas does not reveal a meaningful joint base-12 × nervous-system pattern.

> **No joint structure is a valid atlas outcome.**

H0 is listed first-class alongside any H1…Hn. An atlas that rediscovers Candidate C's base-12 structure but adds no joint nervous-system structure has succeeded as an atlas: it has mapped the discovery set faithfully. H0 is not a failure to be explained away and must not be treated as one in the summary or closure.

## 15. Sealed-data framing

The closure memo generated after the atlas (if and when one is written) **must** explicitly state all four of the following, and this requirement is fixed **before any atlas is generated**:

- **(a)** The atlas itself does not validate anything.
- **(b)** Hypotheses generated are discovery-seeded.
- **(c)** Confirmation requires data **not used in the atlas**.
- **(d)** Within the existing audit chain, the natural confirmatory set is the 2023+ sealed data, and using it for any atlas-generated hypothesis is a **deliberate decision that consumes part of the seal for that specific question** — one-shot, pre-registered, and not to be spent casually or implicitly. Spending the seal is a separate, explicit, future decision, never an automatic consequence of an atlas observation.

No atlas run is authorized until this framing is committed to in the design (it is, here) and carried into any closure.

## 16. Relationship to Candidate C

- Candidate C is the **reason base-12 is included** in this atlas.
- Candidate C's result remains **scoped to its locked protocol** (§12.2(b), §12.4 of the Candidate C design memo). Nothing here changes that scope.
- The atlas **does not strengthen or weaken Candidate C**. It computes no null, no anchor surface, no beat count, no verdict. Grid 4's η² numbers are descriptive re-uses of the η² *form* within nervous-system states; they are not Candidate C's statistic and carry none of its inferential weight.
- The atlas asks a **new descriptive question**: whether Candidate C's phase-allocation structure **co-expresses** with a simple market nervous-system state on the same discovery substrate.
- If the atlas **rediscovers Candidate C but adds no joint structure**, that is a **valid outcome** (Candidate H0).
- If the atlas **finds candidate joint structure**, that is **not confirmation**; it is a discovery-seeded hypothesis requiring data not used in the atlas.
- The atlas does not authorize amending Candidate C, does not re-open its locked surface, and does not reinterpret its verdict in light of anything seen here.

## 17. Relationship to later nulls

- The atlas **does not reinterpret** the later trade-level field-modulated identity null (`docs/field_modulated_identity_trade_level_result_memo_v0.1.md` and related artifacts).
- The atlas **does not rescue** that null.
- The atlas **is not a continuation** of that null study, and is not its successor design.
- The atlas is **exploratory and descriptive only**.
- Any future confirmatory study that draws on this atlas must **explicitly name** which prior results it is using as discovery context and which prior results it is **not** attempting to rescue. That naming is a required precondition of any such future study and may not be left implicit.

## 18. Conceptual motivation from context-dependent expression / influential numbers

The only extractable, usable idea from the Orlando / Kryon / "influential numbers" language is, narrowly, **context-dependent expression**: the broad intuition that a value may *express* differently depending on the field or context it sits in.

The atlas translates that intuition — and nothing more — into a descriptive market question:

> Does the expression of pullback / base-12 structure **vary across market nervous-system states**?

Explicit boundaries on this motivation:

- This does **not** claim numbers literally change.
- This does **not** claim consciousness is directly measured.
- This does **not** claim Orlando's cosmology is correct.
- This does **not** validate "influential numbers."
- It uses **only** the broad, content-free intuition that values may express differently depending on context, as a reason to *look*, never as a premise, a mechanism, or a conclusion.

The motivation justifies asking the descriptive question. It supplies no evidence and licenses no interpretation of any pattern the atlas may show.

## 19. What the atlas may output

The work this memo describes may, if approved and run, produce:

- A full set of descriptive grids (Grids 1–8), every cell reported, low-data and `indeterminate-state` cells marked.
- A sparsity report.
- Standardized heatmaps under the fixed visualization rules.
- A descriptive summary using only permitted language.
- A bounded list of **candidate hypotheses**, each labeled discovery-seeded, with **Candidate H0 (no joint structure) carried at equal status**.
- A closure memo carrying the four sealed-data statements of §15.

Proposed future artifact paths (created later only on explicit instruction, not now):

- `docs/human_field_base12_pullback_atlas_design_memo_v0.1.md` (this memo)
- `results/human_field_base12_pullback_atlas_tables_<timestamp>.csv`
- `results/human_field_base12_pullback_atlas_heatmaps_<timestamp>/`
- `results/human_field_base12_pullback_atlas_summary_<timestamp>.md`
- `docs/human_field_base12_pullback_atlas_closure_memo_v0.1.md`

## 20. What the atlas must not claim

- No verdict, no "privileged", no "confirmatory", no "significant therefore true".
- No proof, no validation, no confirmation of any hypothesis, including Candidate C.
- No rescue of any prior null (Candidate B, SPY MVT, GLD, trade-level field-modulated identity).
- No causal claim about consciousness, attention, fields, or markets.
- No profitability, edge, or allocation-recommendation claim.
- No claim that any pattern generalizes beyond the frozen 2005–2022 discovery substrate.
- No claim derived mainly from low-data or `indeterminate-state` cells.
- No implicit consumption of the 2023+ seal.
- No merger with Lane 2.

## 21. Stop condition

> This design memo does not authorize analysis. No data is run. No OOS is touched. No implementation is created. The next step, if approved, is an atlas implementation plan or a direct atlas run under the fixed descriptive grid.

## 22. Proposed next step after memo review

On review of this memo, the reasonable next steps (your choice, not assumed here) are one of:

1. **Revise this design memo** — adjust grids, state thresholds, variable list, missing-data handling, or scope before anything is built.
2. **Authorize an atlas implementation plan** — a separate document specifying the read-only loaders (frozen Phase 3b CSVs + the already-frozen SPY Yahoo v8 artifact, §5.1), the deterministic single-anchor phase labeling, the valence/realized-volatility state construction with the `t-1` no-leakage and OOS read boundaries, the deterministic grid-construction steps, and the visualization pipeline, still with no run.
3. **Authorize a direct atlas run** under the fixed descriptive grid in this memo. No external data freeze is a prerequisite: all required series (frozen Phase 3b populations + frozen SPY Yahoo v8) are already present in the repo.

No option is selected here. Pause is also a valid choice. Nothing proceeds without explicit instruction.

— end of design memo —
