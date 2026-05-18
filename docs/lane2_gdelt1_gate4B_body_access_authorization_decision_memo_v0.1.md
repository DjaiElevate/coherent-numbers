# Lane 2 — GDELT 1.0 Gate 4B Body-Access Authorization / Forbid Decision Memo

**Version:** v0.1 (Gate 4B decision memo; adjudication only)
**Date:** 2026-05-19
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. **Authorizes nothing.** Decides
*policy* on live index-body access and (if allowed) the firewall strategy.
Performs no body access, implements no code, contacts no GDELT, runs no
retrieval, authorizes no count-only run, drafts no Step 2.

**Governing / chain (committed):**
- Count-only feasibility protocol — `147c0d4` (**binding**)
- Diagnostic memo — `5e0ed4b` (**binding**) · Design memo — `12ae078`
  (**binding**)
- Phase A `38011be` (D0) · Substep 1 `10b80c7` (D2 ruled out) · Substep 2A
  `9a8fb7b` (D1-supported)
- Gate 1 `be2a7df` · Gate 2 `6834814` · Gate 3 PASS `f564b77`
- Gate 4 decision memo — `bf4ef79` (**binding**; mandates this Strategy I vs
  II comparison + firewall re-adjudication)
- Gate 4A: authorization `745af67` · R1 implementation `befbb94` ·
  conformance PASS `bced9e1`
- Consumed run-enablement (spent) — `fe742555`; inert-restore — `9e329c2`

---

## 0. Canonical state (frozen, through `bced9e1`)

- Original count-only run under `fe742555` consumed → **F4-missing**: 3,650
  planned units, 0 parseable available, no downloads, no counts, no market
  data, no 2023+, no Step 2; inert-restored `9e329c2`.
- Diagnosis: D0 (`38011be`) → D2 ruled out (`10b80c7`) → **D1-supported**
  (`9a8fb7b`).
- Offline parser remediated (Gate 2 `6834814`, Gate 3 PASS `f564b77`); R1
  request-target corrected to `…/events/index.html` (Gate 4A `befbb94`,
  conformance `bced9e1`); per-file base unchanged; guards inert.
- **Gate 4B not entered. Gate 4C and Gate 5 unentered and unauthorized.**
  Nothing to date authorizes any live access.
- **Open question Gate 4B gates:** the offline fixes (Gate 2 parser + Gate 4A
  target) are unverified against the *real* live index, because that
  verification requires a body read — which confronts the 2023+ firewall (a
  current `index.html` contains post-2022 filenames).

## 1. Decision — is live index-body access permitted?

Options: (a) forbid entirely; (b) defer pending a pre-2023-only / historical
source; (c) conditionally allow later under a separately implemented firewall
path.

- **(b) is not actionable:** Substep 1 (`10b80c7`) documentation review found
  the listing is a single live `…/events/index.html`; **no pre-2023-only or
  historical snapshot source has been identified.** Deferring "pending" a
  source that does not demonstrably exist is indefinite stall, not a plan.
- **(a) forbid** keeps zero firewall cost but leaves the corrected discovery
  path permanently unverified against reality — the consumed F4 would stand
  as the terminal Lane 2 result on a *known-and-fixed* defect, which is a
  weak place to stop given D1 is supported and the fix is offline-proven.
- **(c) conditionally allow** — a single, tightly firewalled live GET —
  resolves the open question with bounded, reviewable exposure.

**Decision:** **conditionally allow later body access** (option c), **only
after Gate 4C**, under exactly one of the strategies in §2, with the §3–§5
constraints binding. This memo grants no access; it sets the policy a future
Gate 4C/4B-execution authorization must satisfy.

## 2. Strategy I vs Strategy II (mandated by `bf4ef79`)

| Dimension | **Strategy I — pure stream-abort-on-first-2023+** | **Strategy II — segregated streaming scan, aggregate-only 2023+** |
|---|---|---|
| Firewall cost | **Lowest.** Scan halts at the first 2023+ token; the bulk of post-2022 entries is never read. | **Low–medium.** Whole body streamed once; every post-2022 token transiently classified then dropped. |
| Real post-2022 strings enter classifier memory? | Only up to the first 2023+ token (then abort). | **Yes — every** post-2022 token transits classifier memory (transiently, then discarded). |
| Real post-2022 filenames ever stored/printed/logged? | **Never** (forbidden by §4; abort precludes most). | **Never** (forbidden by §4; redaction/aggregation enforced by Gate 4C). |
| Completeness risk under listing order | **High & fatal.** Oldest-first/lexical-by-YYYYMMDD → complete; **reverse-chronological → zero pre-2023 captured**; random → indeterminate. Completeness hinges on uncontrolled server order. | **Order-robust.** A full single pass collects all pre-2023 in-window units regardless of order; only 2023+ tokens are dropped. |
| R4 instrumentation quality | **Degraded.** Counts only reflect what was seen before abort; `rejected_2023plus`, `ignored_out_of_window`, `unrecognized` are truncated/unreliable. | **Full.** Complete recognized/ignored/rejected/unrecognized/malformed counts over the entire listing. |
| Can support a later fresh count-only run? | Only if order happens to cooperate; an order-unlucky GET yields an uninformative/empty result that cannot ground a Gate 5 authorization. | Yes — an order-robust complete in-window key set + full instrumentation is the strongest basis a one-GET can give a later Gate 5 decision. |
| If zero pre-2023 entries captured | Likely (reverse-chronological). Result is uninformative; per §3 → classify source unusable under Strategy I / stop. No retry. | Unlikely from ordering alone; a genuine zero would be a real substrate signal, not an artifact. |

**Adjudication.** Strategy I's surface-level firewall is marginally tighter,
but its completeness is **hostage to uncontrolled server listing order**;
GDELT directory indices are commonly not guaranteed oldest-first, so a single
GET under Strategy I has a material chance of capturing **zero** pre-2023
units and burning the one-GET allowance on an uninformative result. Strategy
II is **order-robust**, preserves **full R4 instrumentation** (the diagnostic
value that the whole Gate chain exists to obtain), and its higher firewall
cost is **bounded and fully mitigable**: post-2022 strings transit memory
transiently and are **never** stored/printed/logged provided the Gate 4C
redaction/aggregation path is implemented and reviewed first. The incremental
firewall cost of II over I is acceptable **only** under a strict, reviewed
Gate 4C; absent Gate 4C, **forbid** is the fallback.

## 3. One-live-GET rule — incomplete / zero-pre-2023 handling

- **Exactly one** live GET. **No automatic second GET, no retry, no
  fallback fetch** under any outcome.
- **Strategy I, zero/short capture:** **classify the source unusable under
  Strategy I and stop** — do not proceed to Gate 5, do not retry, do not
  silently treat truncated counts as a feasibility signal.
- **Strategy II, complete pass but zero in-window units:** treat as a **real
  substrate limitation** (recorded as such), not an artifact — still **no
  retry**; a Gate 5 decision would then be "source not usable for 2005–2022
  count-only feasibility", not a rerun.
- **Either strategy, technical failure (network error, truncation, ambiguous
  response):** **stop and report**; no retry; no Gate 5.
- In all cases the consumed F4 record remains canonical; any future run
  writes a new timestamped directory.

## 4. Real post-2022 rejected-example handling

Addresses the Gate 3/Gate 4 forward note (`Protocol2023PlusBreach` currently
carries example filenames in its message and `.rejected_examples`; synthetic
was safe, real is not):

- **Exact real post-2022 filenames are FORBIDDEN** in exception messages,
  `.rejected_examples`, logs, JSON, markdown, stdout, CSV, tests, or reports.
- **Permitted on the live path: aggregate counts only** (e.g.
  `rejected_2023plus = N`) plus a **non-identifying** characterization (form
  class + year-class boundary only; **no filename, no post-2022 date
  digits**).
- The current Gate 2 example-carrying behavior remains acceptable **only**
  for synthetic fixtures; it **must be replaced on any live path** by the
  redaction/aggregation behavior — this is the Gate 4C blocking precondition
  (§5). Until implemented and reviewed, **no live body read may occur**.

## 5. Mandatory Gate 4C precondition (if body access is conditionally allowed)

Before any live body read:

- Redaction/aggregation behavior **implemented and reviewed**: on the live
  path, `Protocol2023PlusBreach` and any artifact carry **only** aggregate
  `rejected_2023plus` (+ non-identifying class), **never** a real post-2022
  filename or date.
- The chosen §2 strategy (I or II) **implemented and reviewed** with the
  one-GET / no-retry rule (§3) enforced in code.
- **No real post-2022 filename** may appear in exception messages, logs,
  JSON, markdown, stdout, tests, or reports — unless explicitly permitted by
  this Gate 4B memo (it is **not** permitted).
- **Gate 4C uses synthetic fixtures only** — no GDELT contact, no live read,
  no network during Gate 4C implementation/review.
- Gate 4C is itself separately authorized and reviewed; passing Gate 4C does
  **not** authorize the live read — a subsequent explicit Gate 4B-execution
  authorization (one GET) is still required.

**Strategy II composition note.** Strategy II is acceptable only if its
parser / 2023+-handling composition is demonstrated safe under comprehensive
synthetic adversarial testing. The current Gate 2 `Protocol2023PlusBreach`
behavior may carry example filenames in exception messages and
`.rejected_examples`; this is acceptable for synthetic/offline Gate 2
fixtures because the examples are fabricated. It is not automatically
acceptable for any future live path. Under any future live Strategy II path,
real post-2022 filenames may not appear in the following channels: exception
messages, `.rejected_examples`, logs, JSON, markdown, stdout, tests, reports,
or any persisted artifact. Gate 4C must implement exactly one of:

- **(i)** redaction/aggregation layered over the existing Gate 2 extractor so
  no real post-2022 filename is ever constructed into any of the channels
  enumerated above;
- **(ii)** a pre-classifier streaming filter that drops/redacts post-2022
  tokens before they reach any of the channels enumerated above;
- **(iii)** a different Gate 4C design that is separately justified and
  demonstrably satisfies the same no-real-filename-surfacing constraint
  across the channels enumerated above under comprehensive synthetic
  adversarial testing.

If none of these designs can be implemented and reviewed cleanly, Strategy II
is unavailable and Gate 4B must fall back to FORBID unless a new, separately
reviewed Gate 4B amendment is drafted and committed.

## 6. Gate 4B authorizes NOTHING operational

This memo does **not** authorize: GET; HEAD; GDELT contact; live index/body
access; event-file request/download; retrieval; a count-only run;
run-enablement / guard flip; market data; Step 2; source pivot; or any
modification of the consumed F4 outputs. Runner stays inert
(`COUNT_FEASIBILITY_AUTHORIZED=False`, `REAL_RETRIEVAL_ENABLED=False`). It
records a *policy decision and a recommended strategy* only.

## 7. Recommended decision

**CONDITIONALLY ALLOW later body access under Strategy II (segregated
streaming scan, aggregate-only 2023+) after Gate 4C** — with **FORBID as the
explicit fallback** if Gate 4C cannot deliver a reviewed, synthetic-tested
redaction/aggregation + one-GET/no-retry path.

Rationale: Strategy I is rejected as the primary path because its
completeness is hostage to uncontrolled server listing order (material risk
of a zero-capture, one-GET-wasting result) and it degrades the very R4
instrumentation the diagnostic chain exists to obtain. Strategy II is
order-robust and preserves full instrumentation; its only material downside
— transient in-memory post-2022 strings — is bounded and **fully neutralized
by the Gate 4C redaction/aggregation precondition** (§4–§5), with exact
post-2022 filenames forbidden everywhere (D rejected). Option (b)
defer-pending-source is not actionable (no pre-2023 source exists); option
(a) forbid remains the disciplined fallback if Gate 4C cannot be satisfied.

Next step is **Gate 4C** (synthetic-only redaction/aggregation + Strategy II
+ one-GET/no-retry implementation and review). The actual single live GET
remains gated behind a *separate* post-4C execution authorization, and Gate 5
(fresh count-only run authorization) remains separate and unwarranted until
4C closes. This memo authorizes none of them.

## 8. Stop condition

This memo implements no code, edits no tests, contacts no GDELT endpoint,
fetches no documentation, performs no GET/HEAD, inspects no event
archive/index body, runs no retrieval, loads no market data, touches no real
2023+ resource, drafts no Step 2, authorizes no run, modifies no consumed F4
output, and updates no memory. It records adjudications and a recommended
decision only; every downstream step (Gate 4C, the live GET, Gate 5) remains
separately gated and unauthorized.

— end of Gate 4B body-access authorization / forbid decision memo (draft
v0.1) —
