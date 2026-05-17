# Lane 2 — Source-Selection + Count-Only Feasibility Authorization

**Version:** v0.1 (combined source-selection + count-only run authorization)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Documentation-only at this stage.

**Governing / source context (committed):**
- Lane 2 Step 1 framework — `357fba585965818da853a6ba560a7ea2b3213c0b`
- Lane 2 Step 2 readiness memo — `af64ee2f5e12d867bc7b70a1afe7d3c41a7c03fa`
- Lane 2 count-only feasibility protocol — `147c0d40568636ba0cf24ca00cc39c330e77ea03` (**binding**)

---

## 1. Status

- Source-selection + count-only feasibility authorization memo.
- Documentation-only at drafting stage.
- No data accessed.
- No GDELT queried.
- No API called.
- No market data loaded.
- No 2023+ touched, referenced, sampled, counted, or consumed.
- No Step 2 lock drafted.
- No implementation created.
- No model run.
- No outcome computed.

All source/coverage statements below are **documentation-level expectations**,
to be **verified at freeze time** by the future run; none is a data-derived
fact and none is asserted as observed.

## 2. Reason for the compressed gate

The Lane 2 chain already has a Step 1 framework (`357fba5`), a Step 2
readiness memo (`af64ee2`), and a count-only feasibility protocol
(`147c0d4`). A separate source-selection memo plus a separate
run-authorization memo would add gate density without proportional audit
value. This memo preserves the audit value by (a) documenting the
source/product choice and its rationale, and (b) authorizing **only** a
tightly constrained count-only feasibility implementation and one run, fully
governed by protocol `147c0d4`.

## 3. Protocol inheritance (binding)

Protocol `147c0d4` governs this memo. Nothing here may widen it.

**The future run may compute only:** candidate source availability; pre-2023
daily attention-volume series; missingness summaries; raw spike counts;
clustered spike counts; non-trading-day event counts; event-window overlap
counts; per-fold count feasibility; state-count feasibility **only if** the
state-source data is also frozen and pre-2023.

**The future run may not compute:** S&P returns; SPY returns; CAR; abnormal
returns; volatility response; VIX response; any market outcome; model fits;
M0/M1/M2/M3 comparisons; p-values; feature importance; attention–response
relationships; state–response relationships; any 2023+ counts or observations.

## 4. Candidate source/product comparison (documentation only)

No event counts or data-derived facts are used. Coverage figures are
documentation-level expectations to be verified at freeze.

| # | Candidate | Doc-level history | Daily global attention volume? | Pre-2023 restriction possible? | 2005–2022 possible? | Freeze/SHA feasible? | Reproducibility risk | API/vendor risk | Missingness risk | Volume-norm risk | Protocol compatible? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | GDELT 2.0 GKG | ~2015→ (GKG 2.1) | Yes (rich themes/tone) | Yes (file date filter) | **No** (starts ~2015) | Yes (static 15-min files) | Low–med | Low (static files) | Med | High (coverage growth) | Partial — fails 2005–2022 |
| B | GDELT 2.0 Event DB | ~2015→ | Yes (event volume) | Yes | **No** (starts ~2015) | Yes | Low–med | Low | Med | High | Partial — fails 2005–2022 |
| C | GDELT DOC / API | ~2017→ | Partial (article API) | Query-dependent | **No** | Weak (API, non-static) | High | Med–high | Med | High | Poor — API non-reproducible |
| D | **GDELT 1.0 Event DB** | **~1979→** | Yes (aggregate event volume) | **Yes** (restrict frozen file set to pre-2023) | **Yes**, but **non-uniform file/dating regime** (monthly/yearly by event date through 2013-03-31; daily files by media-discovery date from 2013-04-01 — see §5) | **Yes** (static historical archive, per-file hashable) | Low | Low (static archive) | Med (early-year sparsity + 2013 regime boundary) | **High but count-mitigable** via trailing baseline / GDELT normalization files | **Yes** |
| E | Google Trends | ~2004→ | Proxy (search interest) | Yes by query window | Yes (nominal) | Weak (re-sampled, rescaled) | **High** (non-deterministic) | Med | Med | Built-in relative scaling | Poor — reproducibility weak |
| F | Wikipedia pageviews | ~2007/2015→ | Proxy (pageviews) | Yes | **Partial** (no clean 2005) | Yes (dumps) | Low–med | Low | Med | Med | Partial — 2005 gap, weaker "global attention" |
| G | Other market-news proxy | varies | varies | varies | varies | varies | varies | varies | varies | varies | unknown without doc review |
| H | No source yet | — | — | — | — | — | — | — | — | — | — |

Key documentation-level observation: only **D (GDELT 1.0 Event database)**
appears to combine (i) history compatible with 2005–2022, (ii) a static
historical archive that can be SHA-pinned per file (subject to the non-uniform
file/dating regime detailed in §5), and (iii) tractable pre-2023 enforcement
by restricting the frozen file set to pre-2023. GKG/DOC products (A/B/C) carry
richer attention semantics but do not reach 2005. E/F have reproducibility or
coverage weaknesses.

## 5. Source/product selection

**Selected: D — GDELT 1.0 Event database.**

Rationale (documentation-level, count-only feasibility purpose only):

GDELT 1.0 is selected as the first source to attempt because it is the only
reviewed candidate with documented coverage compatible with 2005–2022.
However, its storage and dating regime is not uniform across the full window:
through March 31, 2013, records are stored in monthly/yearly files by event
date; beginning April 1, 2013, files are created daily and records are stored
by the date the event was found in the news media. Therefore, the count-only
feasibility implementation must handle the pre-April-2013 and post-April-2013
regimes explicitly and report whether the boundary creates coverage,
missingness, or spike-rate discontinuity.

Additional rationale (unchanged in substance):

- Pre-2023 restriction is **tractable and verifiable**: only files in the
  frozen set dated before 2023 are retained; no query needs to "ask for"
  2023+, so the §6/§8 seal is enforced by construction, with an abort path if
  the frozen file set cannot be date-restricted.
- An aggregate **event-volume** series (count of records / coverage volume) is
  a defensible count-only attention-intensity proxy without any content
  interpretation, satisfying the protocol's "no content interpretation"
  requirement.
- This remains a source selection for **count-only feasibility only**, not a
  Step 2 source lock; Step 2 may revisit the source/product on its own merits.

**Source-regime risk / implementation requirement.** The future feasibility
run must report attention-observation counts and spike counts by year, and
must explicitly flag whether spike candidates are disproportionately
concentrated after April 1, 2013 or in later years. Secular news-volume drift
and the 2013 file/dating-regime boundary are **feasibility issues, not
hypothesis evidence**.

**Source-normalization choice.** GDELT 1.0 normalization files exist to
compensate for growth in available global news material over time. The
feasibility implementation should record whether those normalization files
are **used, not used, or deferred**, and should treat this as a documented
source-normalization choice (not an outcome or hypothesis decision).

**This is a source selection for count-only feasibility only — not a Step 2
source lock.** Step 2 may revisit the source/product (e.g., a GKG-based
attention measure on a shorter window) on its own merits.

## 6. Recommended coverage window for feasibility

Candidate pre-2023 window: **2005-01-01 → 2022-12-31** (documentation-level;
GDELT 1.0 Event DB is expected to support it). If freeze-time verification
shows the daily archive does not cleanly support 2005, the run must fall back
to the **longest contiguous pre-2023 window the frozen archive actually
supports**, record that window in the manifest, and proceed at count level
only. **No 2023+ under any circumstance.**

## 7. Freeze and manifest requirements

Before any count computation, the future implementation/run must freeze the
selected source. The freeze manifest must record:

- source/product (GDELT 1.0 Event database);
- source URL/query or retrieval method (masterfile/list + per-day files);
- access date;
- coverage window actually frozen;
- the explicit date restriction used to exclude 2023+;
- row/file count;
- SHA-256 (or equivalent) content hash per file (and an aggregate);
- whether any endpoint/listing attempted to return 2023+ entries;
- confirmation that 2023+ rows were **not** downloaded, stored, sampled,
  counted, or inspected.

If the retrieval mechanism cannot enforce a pre-2023 restriction, the run
must **abort** unless separately approved.

## 8. 2023+ seal

- 2023+ **remains sealed**.
- The authorized count-only run may not access, download, query, inspect,
  sample, count, or reference 2023+.
- If a listing/endpoint returns 2023+ entries by default, the run must
  **abort** or require separate explicit approval — never accept silently.
- Any later use of 2023+ requires a **separate** OOS / seal-consumption
  decision. **This memo does not make that decision.**

## 9. Authorized count-only event definitions

Count-level evaluation only, if compatible with the selected source:

- **Option A:** spike = daily attention-volume percentile ≥ 95% vs a trailing
  60 valid pre-2023-day baseline.
- **Option B:** spike = z-score ≥ 2.5 vs a trailing 60 valid pre-2023-day
  baseline.
- **Option C:** spike = attention acceleration / rate-of-change above a
  pre-declared threshold.

Counts may be compared across A/B/C. The final Step 2 event definition may
**not** be chosen on market outcomes (there are none in this gate).

## 10. Authorized clustering / overlap counts

Count-only evaluation of: raw spike days; clustered spike events under
candidate separation windows of **5, 10, 20** trading or calendar days (per
the frozen source calendar); non-trading-day event counts; event-window
overlap counts for hypothetical windows `t+1:t+5` and `t+1:t+20` as
**date-overlap counting only**. **No market returns may be computed.**

## 11. State-axis count feasibility

Authorized **only if** the state source is also pre-2023 and frozen under the
same §7 rule. Families counted as availability / cell-count checks only:
price-derived; implied-vol or stress; external/news-derived; hybrid. **No
market response may be computed.**

If state-axis data is not available under the same no-2023 / freeze
constraints, the run reports **attention-event feasibility only** and marks
**state-count feasibility unresolved** (consistent with a possible F2/F4).

## 12. Implementation authorization

Because a source (D) is selected, this memo **authorizes implementation** of a
count-only feasibility script governed by this memo and protocol `147c0d4`.

The implementation **may**: retrieve/freeze GDELT 1.0 Event DB **only** under
the pre-2023 restriction; compute availability and count-only feasibility
outputs; generate count tables and missingness summaries; write metadata and
manifest artifacts.

The implementation **may not**: load returns; compute outcomes; compute
models; touch 2023+; draft Step 2; make hypothesis claims.

The implementation itself must pass a separate review before any run (§13).

## 13. Run authorization

Because a source is selected, this memo **authorizes one future count-only
feasibility run** — **after** the implementation passes review. The run must
terminate with exactly one feasibility class **F0–F5** from protocol
`147c0d4` and may **not** produce any hypothesis verdict. A second run, or any
scope change, requires fresh authorization.

(If selection had been **H**, neither implementation nor run would be
authorized. Selection is D, so both are authorized under the constraints
above.)

## 14. Feasibility result classes (feasibility only)

- **F0** — no suitable source found.
- **F1** — source available but event counts too low.
- **F2** — source available, event counts adequate, state counts inadequate.
- **F3** — source and counts adequate enough for Step 2 lock drafting.
- **F4** — feasibility inconclusive (coverage / missingness / reproducibility).
- **F5** — methodological failure / protocol breach.

**F3 does not confirm the Lane 2 hypothesis. It only means Step 2 may be
draftable.** F0/F1/F2/F4/F5 do not disprove the hypothesis; they mean the
proposed operationalization is not ready.

## 15. Output artifacts for the future run

- source freeze manifest;
- count-only feasibility metadata JSON;
- count tables CSV;
- missingness tables;
- readiness summary markdown;
- **no** outcome plots; **no** market-response plots (count/missingness plots
  only, if any).

## 16. Boundary statement

This memo does not authorize Step 2 locking, market-outcome computation,
return computation, OOS use, or hypothesis testing. It authorizes only a
count-only, pre-2023, frozen-source feasibility implementation and one run
under protocol `147c0d4`.

## 17. Stop condition

This source-selection and count-feasibility authorization memo does not itself
access data, implement code, run the feasibility check, touch 2023+, or draft
Step 2. If a source/product is selected, the next step is count-only
implementation under this memo and protocol `147c0d4`. If no source/product is
selected, the next step is pause or further documentation review.

— end of source-selection + count-only feasibility authorization memo —
