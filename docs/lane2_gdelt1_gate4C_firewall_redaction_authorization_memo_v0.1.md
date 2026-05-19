# Lane 2 — GDELT 1.0 Gate 4C Firewall / Redaction Implementation Authorization Memo

**Version:** v0.1 (Gate 4C authorization memo; synthetic/offline only)
**Date:** 2026-05-19
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Authorizes — once committed and
separately initiated — only a **synthetic/offline-only live-path firewall /
redaction implementation patch**. Authorizes no live body access, no
GET/HEAD, no GDELT contact, no retrieval, no count-only run, no Step 2, no
source pivot.

**Governing / chain (committed):**
- Count-only feasibility protocol — `147c0d4` (**binding**)
- Diagnostic memo — `5e0ed4b` (**binding**) · Design memo — `12ae078`
  (**binding**)
- Phase A `38011be` (D0) · Substep 1 `10b80c7` (D2 ruled out) · Substep 2A
  `9a8fb7b` (D1-supported)
- Gate 1 `be2a7df` · Gate 2 `6834814` · Gate 3 PASS `f564b77`
- Gate 4 decision `bf4ef79` · Gate 4A: auth `745af67`, impl `befbb94`,
  conformance PASS `bced9e1`
- Gate 4B body-access decision — `159c392` (**binding**; this memo is its
  Gate 4C)
- Consumed run-enablement (spent) — `fe742555`; inert-restore — `9e329c2`

---

## 1. Canonical state (frozen, through `159c392`)

- Original count-only run under `fe742555` consumed → **F4-missing**: 3,650
  planned units, 0 parseable available, no downloads, no counts, no market
  data, no 2023+, no Step 2; inert-restored `9e329c2`.
- D0 (`38011be`) → D2 ruled out (`10b80c7`) → **D1-supported** (`9a8fb7b`).
- Offline parser remediated (Gate 2 `6834814`, Gate 3 PASS `f564b77`); R1
  index-target corrected to `…/events/index.html` (Gate 4A `befbb94`,
  conformance `bced9e1`); per-file base unchanged; guards inert.
- Gate 4B (`159c392`): **CONDITIONALLY ALLOW later body access under
  Strategy II after Gate 4C; FORBID fallback.**
- **Gate 4C not entered.** Post-4C live-execution authorization and Gate 5
  remain **unentered and unauthorized**. Nothing to date authorizes any live
  access.

## 2. Gate 4C authorization boundary

- Once committed **and** separately initiated, this memo authorizes **only a
  synthetic/offline implementation patch** of the Strategy II live-path
  firewall (segregated streaming / redaction / aggregation) plus synthetic
  adversarial tests.
- **No live body access, no GET, no HEAD, no GDELT contact, no retrieval, no
  network** of any kind — implemented and tested entirely against fabricated
  in-memory fixtures.
- **Passing Gate 4C does NOT authorize the live read.** A subsequent,
  separate post-4C live-execution authorization (one GET) is still required;
  Gate 5 remains separate thereafter.
- The firewall code may be *present and tested* but must be **inert by
  construction**: exercised only via fake openers / synthetic strings; no
  code path it adds may itself initiate a request, flip a guard, or enable a
  run.

## 3. Binding canonical no-surfacing channel list (from Gate 4B `159c392`)

Under any future live Strategy II path, **real post-2022 filenames may NOT
appear** in any of these channels — this is the **canonical, binding design
specification** for Gate 4C:

1. exception messages,
2. `.rejected_examples`,
3. logs,
4. JSON,
5. markdown,
6. stdout,
7. tests,
8. reports,
9. or any persisted artifact.

**Exact post-2022 filenames are forbidden on the live path.** Only aggregate
counts (e.g. `rejected_2023plus = N`) and a non-identifying class
characterization (form-class + year-class boundary; no filename, no post-2022
date digits) may be emitted. The Gate 2 `Protocol2023PlusBreach`
example-carrying behavior remains acceptable for **synthetic/offline Gate 2
fixtures only** (examples fabricated) and **must be segregated from** any
live-path behavior.

## 4. Layering rule — full design constraint vs test-observable subset

The §3 canonical channel list is the **binding design specification** for the
Gate 4C implementation; it is **not** narrowed or replaced by what tests can
observe.

- The synthetic test matrix (§6) verifies the **subset of §3 channels
  observable from the synthetic/local test path** (e.g. exception messages,
  `.rejected_examples`, returned/aggregated payloads, captured stdout,
  test-path-persisted artifacts). Channels not directly observable in
  synthetic execution (e.g. a future production log sink, an external report
  surface) are still **bound by design** even though a synthetic test cannot
  exercise them.
- **Gate 4C conformance review must evaluate BOTH:**
  1. whether the implementation **design** satisfies the **full canonical §3
     no-surfacing channel list** (by inspection/argument, not only by test);
     and
  2. whether **tests adequately cover the observable subset** available in
     synthetic/local execution.
- A passing test subset is **necessary but not sufficient**; the design-level
  guarantee against the full §3 list is the controlling criterion. Tests must
  never be read as redefining or shrinking §3.

## 5. Allowed implementation design space

Gate 4C must implement **exactly one** of the following (per Gate 4B §5),
demonstrated safe under comprehensive synthetic adversarial testing **and**
argued safe against the full §3 list (per §4):

- **(i)** redaction/aggregation layered over the existing Gate 2 extractor so
  no real post-2022 filename is ever constructed into any §3 channel;
- **(ii)** a pre-classifier streaming filter that drops/redacts post-2022
  tokens before they reach any §3 channel;
- **(iii)** a different, separately-justified design (live-path-safe wrapper,
  segregated classifier, or equivalent) that demonstrably satisfies the same
  no-real-filename-surfacing constraint across all §3 channels.

Implementation requirements:
- Add a **live-path-safe mode / wrapper / segregated classifier** (or
  equivalent) ensuring post-2022 tokens cannot surface in any §3 channel;
  pre-2023 in-window recognized filenames still retained; aggregate counts +
  non-identifying classes retained.
- **Separate** synthetic/offline example-carrying behavior (Gate 2) from any
  live-path behavior — Gate 2's synthetic hard-fail/example behavior is
  preserved where it applies to fabricated fixtures; the live-path behavior
  is the redacting one.
- **Preserve** Gate 2 parser/extractor behavior (`extract_index_units`
  R2/R4/R5/R6, 2023+ hard-fail-before-downstream, distinct-filename
  instrumentation) and Gate 4A index-target behavior
  (`DEFAULT_GDELT1_INDEX_URL`); preserve the output allow-list and
  prohibited-output tripwires.
- Guards remain inert: `REAL_RETRIEVAL_ENABLED=False` (src),
  `COUNT_FEASIBILITY_AUTHORIZED=False` (runner) — unchanged. No run-enablement
  path, no live path is wired by Gate 4C.
- No real GDELT contact; no GET; no HEAD; no body access; no event
  archive/index inspection; no event-file request/download; no count-only
  rerun; no market data; no real 2023+ resource touch; no Step 2; no source
  pivot. Consumed F4 outputs remain untouched and uncommitted.

## 6. Required synthetic adversarial test matrix

All fixtures fabricated; all openers fake; no network. Tests must prove:

| # | Test class | Assertion |
|---|---|---|
| T1 | Fabricated 2023+ / 2024+ filenames in a synthetic listing | live-path-safe mode does not surface any exact fabricated post-2022 filename in any **observable** §3 channel |
| T2 | Exact-filename redaction/drop | each fabricated post-2022 token is redacted/dropped **before** reaching exception message, `.rejected_examples`, returned/aggregated payloads, captured stdout, or any test-path-persisted artifact |
| T3 | **Year-boundary** | `20221231` (and a `20221231.export.CSV.zip` daily form) is **allowed/retained** as in-window; `20230101` (and `20230101.export.CSV.zip`) is treated as **post-2022** and redacted/aggregated — cutoff is exact at the 2022-12-31 / 2023-01-01 boundary |
| T4 | Aggregate retention | `rejected_2023plus` count + non-identifying class retained with **no** exact filename / post-2022 date digits |
| T5 | Pre-2023 retention | pre-2023 in-window recognized filenames still recognized/retained under live-path-safe mode |
| T6 | Instrumentation intact | unrecognized/malformed tokens remain counted (R4) under live-path-safe mode |
| T7 | Gate 2 segregation | Gate 2 synthetic/offline path unchanged where it applies to fabricated fixtures |
| T8 | No-network static check | no real opener / `urllib` / `requests` / `socket` / network / GET / HEAD path in the firewall code or its tests |
| T9 | Guards / F4 invariants | `REAL_RETRIEVAL_ENABLED is False`; runner `COUNT_FEASIBILITY_AUTHORIZED is False`; consumed F4 record untouched |
| T10 | Full suite | entire `tests/test_lane2_gdelt1_count_feasibility.py` remains passing |

Adversarial coverage must include: post-2022 tokens in href vs link text,
mixed case, multiple post-2022 entries, post-2022 interleaved with pre-2023,
a post-2022-only listing (zero pre-2023), and the exact `20221231` vs
`20230101` boundary pair. Per §4, passing this observable matrix is necessary
but not sufficient — the design must also be argued safe against the full §3
list.

## 7. Future gates (defined; none entered or authorized here)

1. **Gate 4C implementation patch** — synthetic/offline firewall + tests,
   under this authorization, only on commit + separate initiation.
2. **Gate 4C conformance review** — offline; evaluates BOTH the full-§3
   design guarantee (§4.1) and the observable-subset test coverage (§4.2); no
   live access.
3. **Post-4C live-execution authorization** — a *separate* memo authorizing
   exactly one live GET under Strategy II (one-GET / no-retry per Gate 4B
   §3), **only if still warranted**; re-states the firewall.
4. **Gate 5** — fresh count-only feasibility run authorization, **only if
   warranted after the live-execution result**: brand-new memo + separate
   run-enablement + one-run-only + inert-restore (`5e0ed4b` §7);
   `60ec1521`/`fe742555` remain spent.

Each gate is separate and individually reviewed. This memo enters none of
them.

## 8. Authorizes-no-live-step clause

This memo authorizes **no live GET, no HEAD, no GDELT contact, no body/index
access, no retrieval, no count-only run, no run-enablement, no Step 2, and no
source pivot.** A passing Gate 4C firewall *describes* a live-path-safe
design; it does **not** authorize running it against the real index. The
post-4C live-execution authorization and Gate 5 each require their own
separate, explicitly-reviewed memos.

## 9. Stop condition

This memo implements no code, edits no tests, contacts no GDELT endpoint,
fetches no documentation, performs no GET/HEAD, inspects no event
archive/index body, runs no retrieval, loads no market data, touches no real
2023+ resource, drafts no Step 2, authorizes no run, modifies no consumed F4
output, and updates no memory. **It authorizes nothing until it is committed
and separately initiated, and even then only the synthetic/offline Gate 4C
implementation defined in §2–§6.** Every downstream step (Gate 4C conformance
review, the post-4C live GET, Gate 5) remains separately gated and
unauthorized.

— end of Gate 4C firewall / redaction implementation authorization memo
(draft v0.1) —
