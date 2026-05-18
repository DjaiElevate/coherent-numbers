# Lane 2 — GDELT 1.0 Remediation-Patch Authorization Memo (Gate 1)

**Version:** v0.1 (remediation-patch authorization memo; offline-only)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Authorizes — once committed and
separately initiated — only a **narrow, offline-only discovery/parser
remediation patch**. Authorizes no live contact, no body access, no GET/HEAD,
no count-feasibility rerun, no run-enablement, no Step 2, no source pivot.

**Governing / chain (committed):**
- Count-only feasibility protocol — `147c0d4` (**binding**)
- Retrieval-wiring path — `9528fe5`
- Run-enablement (**consumed/spent**) — `fe742555`; inert-restore —
  `9e329c2`
- Layout-feasibility diagnostic memo — `5e0ed4b` (**binding**)
- Phase A report (**D0**) — `38011be`
- Phase B Substep 1 report (**D2 ruled out**) — `10b80c7`
- Phase B Substep 2A report (**D1-supported**) — `9a8fb7b`
- Discovery-defect remediation **design memo** — `12ae078` (**binding**;
  this memo is its Gate 1)

---

## 1. Canonical state (frozen)

- The single authorized count-only run under `fe742555` produced
  **F4-missing**: 3,650 planned units, **0 parseable available units**, no
  GDELT files downloaded, no counts computed.
- Inert-restore committed at `9e329c2` (`COUNT_FEASIBILITY_AUTHORIZED=False`,
  `REAL_RETRIEVAL_ENABLED=False`).
- Phase A closed **D0** at `38011be`.
- Substep 1 **ruled out D2** at `10b80c7`.
- Substep 2A **D1-supported** at `9a8fb7b` (documented
  `.../events/index.html` exists, non-empty, `text/html`).
- Discovery-defect remediation **design memo** committed at `12ae078`.
- **No rerun and no patch is currently authorized.** This memo, once
  committed, authorizes **only** the Gate 1 offline patch defined below.

## 2. Patch authorization boundary

- Once committed **and** separately initiated, this memo authorizes **only an
  offline parser/discovery remediation patch** — implementation plus
  synthetic/local tests, exercised through in-memory fake openers and
  fabricated fixtures only.
- **No live contact or body-level access** of any kind.
- **R1 (request-target change `.../events/` → `.../events/index.html`)
  remains OUT OF SCOPE** — it is a server/environment-side fact (per `12ae078`
  §3 testability asymmetry) and is deferred to a later, separately-adjudicated
  body-access decision (Gate 4).
- Authorized remediation components (offline-testable only):
  - **R2** — robust HTML/listing filename extractor for synthetic
    representative HTML fixtures.
  - **R4** — unparsed-token / unrecognized-link count instrumentation.
  - **R5** — immediate 2005–2022 extraction filter.
  - **R6** — hard-fail on any 2023+ filename/resource token in synthetic
    fixtures.
  - Preserve the existing output allow-list and prohibited-output tripwires
    (`ALLOWED_OUTPUT_BASENAMES`, `_checked_path`, `_assert_outputs_allowed`)
    — unchanged in spirit; any new audit artifact must be added to the
    allow-list explicitly and reviewed.
  - Add or update **synthetic/local tests only**; in-memory fake openers /
    fabricated HTML/listing fixtures only.
- **Explicitly deferred / NOT authorized:** R1; any live body access; any GET;
  any HEAD; any event archive/index contact; any event-file request or
  download; any count-only feasibility rerun; any run-enablement commit; any
  Step 2 lock; any source pivot.

## 3. Required implementation constraints (binding on the Gate 2 patch)

- Synthetic fixtures **must** include: representative **HTML index listings**;
  valid **2005–2022** filenames; **invalid/unrecognized** tokens; **2023+**
  filenames/resources used solely to verify hard-fail behavior.
- The parser **must not silently drop unrecognized tokens** without
  instrumentation.
- The parser **must report counts**: recognized, ignored (out-of-window),
  rejected (2023+), and unparsed/unrecognized.
- The parser **must fail closed on 2023+** (raise the existing
  `Protocol2023PlusBreach` / seal behavior) **before any downstream
  planning/count logic**.
- The 2005–2022 extraction filter (R5) must apply **at extraction time**,
  before any persistence or counting.
- No market data; no returns / CAR / abnormal returns / volatility / VIX /
  market outcomes; no model fits; no p-values; no feature importance; no
  attention-response or state-response relationships; **no Step 2 content**.
- `REAL_RETRIEVAL_ENABLED` stays **False** in source;
  `COUNT_FEASIBILITY_AUTHORIZED` stays **False** in the runner. The patch is
  pure offline discovery/parser logic + tests; it does **not** flip any
  guard, wire any live path, or enable any run.
- The consumed F4 record (`results/lane2_gdelt1_count_feasibility/
  20260518T163302Z/`) is **canonical, non-overwritten**; the patch must not
  touch it.

## 4. Required tests (binding on the Gate 2 patch)

- A synthetic HTML fixture **represents the current whitespace-tokenizer
  failure mode** (HTML index → 0 recognized under the old tokenizer).
- The new extractor **recognizes documented-form filenames** from synthetic
  HTML.
- The new extractor **filters to 2005–2022**.
- The new extractor **hard-fails on 2023+** (synthetic 2023+ token →
  `Protocol2023PlusBreach`, before any planning/count).
- **Unparsed/unrecognized-token counts are recorded** and asserted.
- **No real opener, `urllib`, `requests`, `socket`, or network path** is used
  anywhere in the new or existing tests.
- **Existing count-only safety tests remain passing** (the prior committed
  Lane 2 suite, incl. seal guards, allow-list, runner-guard, F-class tests).

## 5. Required future gates (sequence; none entered by this memo)

- **Gate 1 (this memo):** authorize the offline parser/discovery remediation
  scope. *(Entered only on commit + separate initiation.)*
- **Gate 2:** implement the patch using synthetic/local fixtures only (no
  GDELT contact, no body access, no guard flip).
- **Gate 3:** conformance review (offline; fake openers / fixtures only;
  spec/test conformance against §3–§4).
- **Gate 4:** a **separate** body-access / R1 decision, **explicitly
  re-adjudicating the 2023+ firewall** (per `12ae078` §4 and `10b80c7` §3);
  may forbid body access or choose a firewall-safe strategy.
- **Gate 5:** a **fresh** count-only feasibility run authorization (new memo +
  separate run-enablement commit + one-run-only + inert-restore), **only if
  still warranted** after Gate 4.

Each gate is separate and individually reviewed. This memo enters **only**
Gate 1 (and only on commit + separate initiation); it does not enter Gate 2+
and authorizes none of them.

## 6. Strict prohibitions

- No GDELT contact.
- No documentation fetch.
- No GET; no HEAD.
- No response-body access; no event archive/index inspection.
- No event-file request/download.
- No count-only feasibility rerun.
- No run-enablement commit; no guard flip
  (`COUNT_FEASIBILITY_AUTHORIZED`/`REAL_RETRIEVAL_ENABLED` stay False).
- No R1 request-target change (deferred to Gate 4).
- No market data; no returns/outcomes/models/p-values/feature-importance/
  attention- or state-response.
- No 2023+ **real** resource touch (synthetic 2023+ fixture strings for
  hard-fail tests only).
- No Step 2; no hypothesis verdicts.
- No source pivot; no normalization/parameter/threshold/event-definition
  change; no weakening of the output allow-list or tripwires.
- No modification, relocation, deletion, regeneration, or overwrite of the
  consumed F4 outputs.

## 7. Authorizes-no-further-step clause

Nothing in this memo, and nothing the Gate 2 patch produces, authorizes a
count-only feasibility run, any live/body access, any R1 change, any
run-enablement, any source pivot, or any Step 2. A passing offline patch
*describes* a corrected discovery/parser path; it does **not** authorize
running it against real data. Gate 4 (body-access / R1, firewall
re-adjudicated) and Gate 5 (fresh run authorization) each require their own
separate, explicitly-reviewed memos.

## 8. Stop condition

This memo implements no code, runs no test, contacts no GDELT endpoint,
fetches no documentation, performs no GET or HEAD, inspects no event
archive/index body, modifies no consumed F4 output, and updates no memory. It
authorizes — only once committed and only then — the bounded offline
parser/discovery remediation defined in §2–§4, to be implemented at Gate 2
under separate initiation. No live contact, body access, rerun, Step 2, or
source pivot is authorized; each remains gated by a separate, explicitly-
reviewed authorization.

— end of remediation-patch authorization memo (draft v0.1) —
