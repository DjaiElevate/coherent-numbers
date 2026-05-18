# Lane 2 — GDELT 1.0 Phase B Substep 2A HEAD-Only Index-Existence Probe Authorization

**Version:** v0.1 (Phase B Substep 2A authorization memo; HEAD-only)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Authorizes — once committed and
separately initiated — exactly **one HEAD-only metadata probe**. Authorizes no
GET, no body read, no parsing, no event retrieval, no rerun, no code change,
no source pivot.

**Governing / source context (committed):**
- Count-only feasibility protocol — `147c0d40568636ba0cf24ca00cc39c330e77ea03` (**binding**)
- Layout-feasibility diagnostic memo — `5e0ed4bd70658767c74654db20d748794a237548` (**binding**)
- Phase A authorization — `c06ded434722d61b5707e46c4474e6f3ae9047ea`
- Phase A report (provisional **D0**) — `38011be07c21c5f0455bff719867697d4ef1925f`
- Phase B Substep 1 doc-fetch authorization — `b982e7cd0c2d51b410d8b5e36d56506cf26bfaca`
- Phase B Substep 1 doc-fetch report (**D2 ruled out**; 2023+ firewall note
  binding) — `10b80c7a7adbabf579ada5c56ac480710004acae`
- Consumed run-enablement (spent) — `fe742555cd240150d17dd1ea255453993e34d239`;
  inert-restore — `9e329c2a80e43f17eead7836729c719b444f2823`

---

## 1. Status

- Substep 2A authorization memo only. Authorizes a bounded future HEAD-only
  probe; it is not the probe and contacts nothing itself.
- No data accessed in drafting. No GDELT contacted. No HEAD/GET issued. No API
  called. No tests run. No code implemented. No market data. No 2023+
  touched/referenced/sampled/counted/consumed. No Step 2. No source pivot.
- The single authorized count-only feasibility run remains **consumed**
  (`60ec1521` / `fe742555` spent); this memo does **not** re-authorize it.
- This memo is subordinate to and bounded by diagnostic memo `5e0ed4b`. It is
  a deliberately narrowed alternative to a full "Substep 2 live
  index-metadata read": **Substep 2A** authorizes only an HTTP **HEAD**
  existence/non-empty probe — no listing content is ever transferred or read.
- **D2 remains ruled out** per `10b80c7`. This memo addresses only the
  remaining **D1-vs-D3** question.

## 2. Purpose

Resolve the D1-vs-D3 ambiguity as narrowly as possible: determine whether the
documented GDELT 1.0 index resource **exists and is non-empty** *without
reading any listing body*, so that:
- a successful, non-empty HEAD → the resource exists and the consumed
  F4-missing result is most consistent with a **request-construction /
  discovery defect (D1)** (e.g. the wiring fetched the directory path, or its
  tokenizer cannot parse the real listing format); vs
- a 404 / blocked / transport-empty-like HEAD → most consistent with an
  **access/environment issue (D3)**.

## 3. 2023+ firewall adjudication (per `10b80c7` §3 binding note)

The Substep 1 report requires any live index-metadata authorization to
explicitly adjudicate the 2023+ firewall. Adjudication for Substep 2A:

- A **HEAD request returns no entity body**. No filenames — pre-2023 or
  post-2022 — are transferred, read, parsed, extracted, counted, stored, or
  printed. The probe therefore **cannot** expose 2023+ archive contents.
- Only **non-content transport metadata** is recorded (status code, final
  URL, the `Location` header if a redirect is returned, presence/value of
  `Content-Length`, redirect status, HEAD-refusal; no redirect is followed).
  `Content-Length` is an aggregate byte count of a listing page, **not** a
  2023+ filename or resource; recording it does not inspect, enumerate, or
  reveal any 2023+ event resource.
- This satisfies `10b80c7` option **(a)/(b) hybrid**: rather than forbidding
  the read outright or opening a broad firewall exception, Substep 2A defines
  a **HEAD-only narrow exception** that structurally cannot expose post-2022
  metadata. The existing no-2023+ rule is **not weakened**; it is preserved by
  construction.
- If, in execution, existence/non-empty status cannot be established without
  retrieving a body, the correct outcome is **D0-still-unresolved** (see §6) —
  **no escalation to GET is authorized**.

## 4. Target

- Exactly **one** HTTP **HEAD** request, with **automatic redirect-following
  disabled**, to the documented GDELT 1.0 index resource:
  `http://data.gdeltproject.org/events/index.html`.
- No other URL. In particular, no request to the directory path
  `http://data.gdeltproject.org/events/`, and no event file. The target is the
  documented index/listing resource, but Substep 2A authorizes no
  listing-body retrieval, no listing-content inspection, no HTML parsing, and
  no filename extraction.

## 5. Scope

Authorizes **only a future HEAD-only probe step**, not the probe itself yet,
and only after this memo is committed **and** a separate explicit go-ahead is
given.

### 5a. Allowed later (post-commit and post-initiation)

- **One HEAD request only** to the §4 target, with automatic
  redirect-following **disabled** — a single response only; **no follow-up
  request** to any `Location` URL, **no GET fallback**, **no second HEAD
  request**.
- Record only:
  - HTTP status code (including a 3xx redirect status, if returned);
  - the requested URL, and the `Location` header if a redirect response is
    returned (the `Location` URL is recorded but **not** requested);
  - headers necessary to determine existence / non-empty status — in
    particular `Content-Length` if present;
  - whether the server refused HEAD.
- If the single response is a redirect and existence/non-empty status cannot
  be established from that one response, classify **D0-still-unresolved**
  (no follow-up request, no GET fallback).
- Read-only inspection of committed Lane 2 memos / source / runner / tests /
  prior Phase reports for write-up context.

### 5b. Strict prohibitions

- No GET request.
- No response-body retrieval, read, print, parse, or store.
- No listing-body retrieval; no listing-content inspection; no HTML parsing;
  no filename extraction.
- No event-file request/download.
- No count-only feasibility rerun (inert-restore `9e329c2` stands;
  `COUNT_FEASIBILITY_AUTHORIZED` / `REAL_RETRIEVAL_ENABLED` stay False).
- No parser patch; no production-code change; no source/test/runner change.
- No market data; no returns / CAR / abnormal returns / volatility / VIX /
  any market outcome; no model fits; no p-values; no feature importance; no
  attention-response or state-response relationships.
- No 2023+ filename/resource inspection, extraction, counting, storage, or
  printing.
- No Step 2; no hypothesis verdicts.
- No source pivot; no normalization / parameter / threshold / event-definition
  / output-allow-list change.
- No modification, relocation, deletion, regeneration, or overwrite of the
  consumed F4 outputs.
- **No automatic escalation to GET** if HEAD is unsupported or ambiguous —
  stop and classify D0-still-unresolved instead.

## 6. Decision rule

The later Substep 2A investigation must assign exactly one class:

- **D1-supported / request-construction-discovery defect likely** — HEAD
  returns 200 (or equivalent success) and indicates a **non-empty** resource
  (e.g. positive `Content-Length`) **without** reading the body.
- **D3-supported** — HEAD returns 404, is blocked/unavailable, or yields a
  transport-empty-like response (e.g. success with zero/absent length
  indicating no resource), in the run environment.
- **D0-still-unresolved** — HEAD is unsupported, `Content-Length` is absent,
  the single response is a redirect from which existence/non-empty status
  cannot be established (no follow-up to `Location`), or existence/non-empty
  status otherwise cannot be established without body retrieval. **No
  redirect-follow, no GET escalation, no second HEAD.**
- **D2** — remains **ruled out** per `10b80c7`; not re-litigated here.
- **D5** — any protocol breach (a GET issued, a body read, 2023+ inspected,
  F4 outputs altered, scope exceeded). Halt; escalate to human review.

## 7. Required output for the later Substep 2A investigation

An uncommitted report containing exactly:

1. The assigned class — **D1-supported**, **D3-supported**,
   **D0-still-unresolved**, or **D5**.
2. The exact metadata recorded from the HEAD response (status code, the
   requested URL, the `Location` header if a redirect is returned,
   `Content-Length` if present, redirect status, HEAD-refusal flag), with an
   explicit note that **no redirect was followed**.
3. Explicit statement that **no response body was retrieved, read, printed,
   parsed, or stored**.
4. Explicit statement that **no 2023+ filenames/resources were inspected,
   extracted, counted, stored, or printed**.
5. Canonical-preservation confirmation for the consumed F4 outputs
   (`results/lane2_gdelt1_count_feasibility/20260518T163302Z/`).
6. Explicit statement that the report authorizes **no** rerun, **no** code
   patch, **no** GET, **no** source pivot, and **no** Step 2.

## 8. Authorizes-no-further-step clause

Nothing in this memo, and nothing the Substep 2A probe produces, authorizes a
count-only feasibility run, a GET / body read / listing parse, any
parser/layout remediation patch, or any source pivot. A "D1-supported"
finding *describes* a likely request-construction/discovery defect; it does
**not** authorize a fix — that remains a separately reviewed change with no
rerun authority (diagnostic memo `5e0ed4b` §7). A "D3-supported" finding
points toward independent access verification or source rejection as a
separate decision. Any body-level inspection requires its own, separately
reviewed authorization that must itself re-adjudicate the 2023+ firewall.

## 9. Stop condition

This memo does not contact GDELT, issue any HEAD or GET, read any body, parse
any listing, request or download any event file, rerun the feasibility check,
implement or change any code, run any test, modify the consumed F4 outputs, or
pivot the source. It authorizes — only once committed and only then — the
single bounded HEAD-only probe defined in §4–§5, to produce the §7 outputs.
The Substep 2A probe is **not** initiated until this memo is committed and a
separate explicit go-ahead is given.

— end of Phase B Substep 2A HEAD-only probe authorization memo (draft v0.1) —
