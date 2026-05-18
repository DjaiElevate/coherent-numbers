# Lane 2 — GDELT 1.0 Gate 4A R1 Offline Patch Authorization Memo

**Version:** v0.1 (Gate 4A authorization memo; offline URL-target only)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Authorizes — once committed and
separately initiated — only a **narrow, offline-only R1 URL-target patch**.
Authorizes no live access, no body access, no GET/HEAD, no retrieval, no
count-only rerun, no run-enablement, no Step 2, no source pivot.

**Governing / chain (committed):**
- Count-only feasibility protocol — `147c0d4` (**binding**)
- Diagnostic memo — `5e0ed4b` (**binding**) · Design memo — `12ae078`
  (**binding**)
- Phase A `38011be` (D0) · Substep 1 `10b80c7` (D2 ruled out) · Substep 2A
  `9a8fb7b` (D1-supported)
- Gate 1 patch authorization — `be2a7df` · Gate 2 offline remediation —
  `6834814` · Gate 3 conformance review (PASS) — `f564b77`
- Gate 4 body-access / R1 firewall **decision memo** — `bf4ef79`
  (**binding**; §1 approved R1 *in principle*, deferred implementation to
  this Gate 4A)
- Consumed run-enablement (spent) — `fe742555`; inert-restore — `9e329c2`

---

## 1. Canonical state (frozen, through `bf4ef79`)

- F4 count-only run consumed under `fe742555`: 3,650 planned units, 0
  parseable available units, no downloads, no counts, no market data, no
  2023+, no Step 2. Runner restored inert at `9e329c2`.
- Phase A **D0** (`38011be`) → Substep 1 **D2 ruled out** (`10b80c7`) →
  Substep 2A **D1-supported** (`9a8fb7b`: documented `…/events/index.html`
  exists, `200`, non-empty, `text/html`).
- Gate 0 design memo `12ae078`; Gate 1 authorization `be2a7df`; Gate 2
  offline parser remediation `6834814`; Gate 3 conformance PASS `f564b77`;
  Gate 4 decision memo `bf4ef79`.
- **Gate 4A not entered.** Gate 4B / 4C / 5 remain **unentered and
  unauthorized**. No rerun or live access is authorized by anything to date.

## 2. R1 authorization boundary

- Once committed **and** separately initiated, this memo authorizes **only an
  offline R1 URL-target patch** — changing the GDELT 1.0 listing target from
  the directory path `http://data.gdeltproject.org/events/` to the documented
  index resource `http://data.gdeltproject.org/events/index.html` — plus
  synthetic URL-construction/regression tests.
- **No live access or retrieval authority.** Changing the target *string*
  does not fetch anything; no request is performed by this patch. The patch
  is pure offline URL-construction logic + tests.
- **No run authority.** Runner guards remain in force and untouched
  (`COUNT_FEASIBILITY_AUTHORIZED=False`, `REAL_RETRIEVAL_ENABLED=False`).
- **No body-access strategy selection.** Strategy I vs Strategy II
  (`bf4ef79` §2) and the 2023+ live-path firewall are **not** decided here;
  they remain Gate 4B/4C.
- **Out of scope (not authorized):** any GET; any HEAD; any GDELT contact;
  any documentation fetch; any event archive/index body access; any
  event-file request/download; any count-only feasibility rerun; any
  run-enablement commit; any body-access strategy selection; any Gate 4B/4C
  implementation; any market data; any real 2023+ filename/resource touch;
  any Step 2; any source pivot; any modification of the consumed F4 outputs.

## 3. Required implementation constraints (binding on the Gate 4A patch)

- **URL construction must target `events/index.html`.** The constructed
  listing URL used by `fetch_archive_index` (via its `index_url` default /
  the relevant target constant) must resolve to
  `http://data.gdeltproject.org/events/index.html`, not the bare
  `…/events/` directory path.
- **Gate 2 parser/extractor behavior must remain intact.**
  `extract_index_units` (R2/R4/R5/R6), `_classify_gdelt1_filename`,
  `IndexExtraction`, the 2023+ hard-fail-before-downstream behavior, and the
  legacy-regression helper are **unchanged** by R1. R1 changes only *which
  URL string* is targeted, not *how listing text is parsed*.
- **Guards remain inert:** `REAL_RETRIEVAL_ENABLED=False` (src) and
  `COUNT_FEASIBILITY_AUTHORIZED=False` (runner) — unchanged. R1 flips no
  guard and wires no live path.
- **Minimal, documented constant change.** `DEFAULT_GDELT1_BASE_URL` /
  target constant(s) may be changed **only as needed for R1** and must be
  clearly documented in-code (comment citing this Gate 4A authorization and
  the `9a8fb7b` / `10b80c7` evidence). No unrelated constant, parameter,
  threshold, event-definition, normalization, or allow-list change.
- **Preserve output allow-list & tripwires.** `ALLOWED_OUTPUT_BASENAMES`,
  `_checked_path`, `_assert_outputs_allowed`, `_PROHIBITED_OUTPUT_MARKERS`
  unchanged in spirit; any new artifact name (none expected for R1) would
  require explicit allow-list review.
- **No body-access or 2023+ firewall strategy is selected here** — that is
  Gate 4B/4C and must re-adjudicate the firewall (`bf4ef79` §2–§4).

## 4. Required tests (binding on the Gate 4A patch)

- A synthetic **URL-construction test** asserting the constructed listing URL
  is exactly `http://data.gdeltproject.org/events/index.html`.
- A **regression test** asserting the bare directory path
  `http://data.gdeltproject.org/events/` is **not** used as the index
  listing target.
- Tests use **fake openers / local synthetic URL-construction only** — no
  real opener, no `urllib`/`requests`/`socket`, no network, no GET, no HEAD.
- The **existing 66 Lane 2 tests remain passing** (Gate 2 parser/extractor,
  seal guards, allow-list, runner-guard, F-class, orchestrator).

## 5. Future gates (defined; none entered or authorized here)

- **Gate 4A — implementation patch** (offline R1 URL-target + tests), under
  this authorization, only on commit + separate initiation.
- **Gate 4A — conformance review** (offline; verifies §3/§4; no live access).
- **Gate 4B — body-access authorization decision**: explicitly compare
  **Strategy I** (pure stream-abort-on-first-2023+) vs **Strategy II**
  (segregated streaming scan) per `bf4ef79` §2, with the 2023+ firewall
  **re-adjudicated**; may forbid body access (Option A) or require a
  pre-2023 source (Option E). Separate memo.
- **Gate 4C — redaction/aggregation implementation** (the `bf4ef79` §3
  blocking precondition: real post-2022 examples must never surface), if
  body access is ever authorized. Separate gate.
- **Gate 5 — fresh count-only feasibility run authorization** *(only if
  still warranted after 4A–4C)*: brand-new run-authorization memo + separate
  run-enablement commit + one-run-only + inert-restore (`5e0ed4b` §7
  unchanged); `60ec1521`/`fe742555` remain spent.

Each gate is separate and individually reviewed. This memo enters none of
them.

## 6. Strict prohibitions

No GET; no HEAD; no GDELT contact; no documentation fetch; no event
archive/index body access; no event-file request/download; no count-only
feasibility rerun; no run-enablement commit / guard flip; no body-access
strategy selection; no Gate 4B/4C implementation; no market data; no
returns/outcomes/models/p-values; no real 2023+ filename/resource touch
(synthetic fixture strings only, where tests need them); no Step 2; no
source pivot; no normalization/parameter/threshold/event-definition change;
no weakening of the output allow-list/tripwires; no modification, relocation,
deletion, regeneration, or overwrite of the consumed F4 outputs.

## 7. Authorizes-no-further-step clause

Nothing in this memo, and nothing the Gate 4A patch produces, authorizes any
live access, body read, GET/HEAD, retrieval, count-only run, run-enablement,
body-access strategy selection, Gate 4B/4C step, source pivot, or Step 2. A
correctly targeted listing URL *describes* the corrected request target; it
does **not** authorize sending the request. Gate 4B (body-access decision,
firewall re-adjudicated) and Gate 5 (fresh run authorization) each require
their own separate, explicitly-reviewed memos.

## 8. Stop condition

This memo implements no code, edits no tests, contacts no GDELT endpoint,
fetches no documentation, performs no GET/HEAD, inspects no event
archive/index body, runs no retrieval, loads no market data, touches no real
2023+ resource, drafts no Step 2, authorizes no run, modifies no consumed F4
output, and updates no memory. **It authorizes nothing until it is committed
and separately initiated**, and even then authorizes only the bounded
offline R1 URL-target patch defined in §2–§4. Every downstream step
(Gate 4B / 4C / 5) remains separately gated and unauthorized.

— end of Gate 4A R1 offline patch authorization memo (draft v0.1) —
