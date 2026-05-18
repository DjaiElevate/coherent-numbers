# Lane 2 — GDELT 1.0 Gate 4 Body-Access / R1 Firewall Decision Memo

**Version:** v0.1 (Gate 4 decision memo; adjudication only)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. **Authorizes nothing.** Decides
*policy* for R1 and live body access; implements no code, authorizes no
GET/HEAD, contacts no GDELT, runs no retrieval, authorizes no count-only run,
drafts no Step 2.

**Governing / chain (committed):**
- Count-only feasibility protocol — `147c0d4` (**binding**)
- Diagnostic memo — `5e0ed4b` (**binding**) · Design memo — `12ae078`
  (**binding**)
- Phase A `38011be` (D0) · Substep 1 `10b80c7` (D2 ruled out) · Substep 2A
  `9a8fb7b` (D1-supported)
- Gate 1 patch authorization — `be2a7df` · Gate 2 offline remediation —
  `6834814` · Gate 3 conformance review (PASS) — `f564b77`
- Consumed run-enablement (spent) — `fe742555`; inert-restore — `9e329c2`

---

## 0. Canonical state (frozen)

- F4 count-only run consumed under `fe742555`: 3,650 planned units, 0
  parseable available units, no downloads, no counts, no market data, no
  2023+, no Step 2. Runner restored inert at `9e329c2`.
- Diagnosis: D0 (`38011be`) → D2 ruled out (`10b80c7`) → D1-supported
  (`9a8fb7b`, documented `…/events/index.html` exists, `200`,
  `Content-Length 556438`, `text/html`, no redirect).
- Offline parser remediation (R2/R4/R5/R6) committed `6834814`; Gate 3
  conformance PASS `f564b77`. **Gates 0–3 closed.**
- **Gate 4 not yet entered. Gate 5 (fresh count-only run authorization) not
  drafted or authorized.** No rerun or live access is authorized by anything
  to date.

## 1. Sub-decision A — R1 request-target change

**Question.** May a future patch change the listing target from
`http://data.gdeltproject.org/events/` to
`http://data.gdeltproject.org/events/index.html`?

**Evidence.** `10b80c7` documents the listing resource explicitly as
`…/events/index.html`; `9a8fb7b` confirmed by HEAD that that exact resource
returns `200`, non-empty, `text/html`. The wiring currently targets the bare
directory path. R1 corrects the *request target* to the documented resource.

**Adjudication (decision, not authorization).**
- **R1 is a sound, evidence-supported change** and **may be decided here**
  *without* any live body access — the decision rests entirely on committed
  documentation (`10b80c7`) and HEAD metadata (`9a8fb7b`), neither of which
  required a body read.
- **R1 implementation remains a separate offline patch gate (Gate 4A)** —
  this memo does not implement it. An R1 patch is a one-line constant change
  plus tests; it is **offline** (changes which URL string is passed to the
  injected opener; performs no request itself).
- **R1 authorizes no retrieval and no count-feasibility run.** Changing the
  target string does not, by itself, fetch anything; the runner guards
  (`COUNT_FEASIBILITY_AUTHORIZED=False`, `REAL_RETRIEVAL_ENABLED=False`)
  remain in force and untouched by R1.

**Recommended:** approve R1 *in principle*; defer implementation to a separate
Gate 4A offline patch authorization. R1 alone does not require, and must not
be bundled with, body access.

## 2. Sub-decision B — live body-access decision

**Question.** May any future GET/body read of the index be authorized at all
under the 2023+ firewall? A current full index **will** contain post-2022
filenames (GDELT 1.0 daily files continue past 2022-12-31), so any body read
confronts the firewall.

| Option | Firewall cost | Diagnostic / audit value | Real 2023+ filenames enter Lane 2 address space? | R4 instrumentation possible? | Can support a later fresh count-only authorization? |
|---|---|---|---|---|---|
| **A. Forbid body access entirely; require alternative/historical source** | **Zero** — no body ever read | Low — cannot confirm the corrected parser recovers in-window units from the real index; relies on E or stays offline-only | No | Yes (offline/synthetic only) | Weakly — a fresh run would still face an unverified live discovery path |
| **B. One live GET, streaming firewall scan, immediate abort on first 2023+ token** | **Low** — bytes transit memory transiently; never materializes the full post-2022 listing; first 2023+ token aborts | High — verifies real recovery of 2005–2022 units up to the abort point | Transiently in memory only; **never stored/printed** if rule §4 holds | Yes — recognized/ignored/unrecognized counts up to abort | Yes — strongest practical basis, if ordering yields pre-2023 before 2023+ (not guaranteed; see note) |
| **C. One live GET, full scan, aggregate counts only (no real post-2022 filenames emitted)** | **Medium** — full body (incl. post-2022 entries) transits memory; only aggregates emitted | High — full recognized/ignored/rejected counts | Transiently in memory (full listing parsed); **aggregates only** emitted | Yes — full R4 instrumentation | Yes |
| **D. One live GET, rejected real examples preserved for audit** | **High** — real post-2022 filenames persisted in exception/artifact | Highest transparency | **Yes — persisted** | Yes | Yes, but at firewall cost most inconsistent with the no-2023+ rule |
| **E. Require a pre-2023-only / historical snapshot source before any body read** | **Zero–Low** — depends on whether such a source exists | High if a clean pre-2023 snapshot exists; otherwise blocked | No (by construction) | Yes | Yes, cleanest — but contingent on a real pre-2023-bounded source existing |

**Note on B (ordering — strong firewall safety, order-dependent
completeness).** Stream-abort-on-first-2023+ has **strong surface-level
firewall safety regardless of listing order**, but its **completeness is
order-dependent**:

- **Chronological, oldest-first:** stream-abort may capture *all* 2005–2022
  entries before the first 2023+ token (complete).
- **Alphabetically sorted by YYYYMMDD-prefixed filenames:** lexical order of
  zero-padded date-prefixed names effectively behaves like chronological
  ordering (≈ complete).
- **Reverse-chronological, newest-first:** stream-abort may hit a 2023+ token
  immediately and capture **zero** pre-2023 entries (empty result).
- **Random / unstable order:** completeness is **indeterminate**.

Firewall *safety* under B holds in all four cases; *completeness* does **not**
and must never be assumed. **Gate 4B must define, in advance, how a
zero-pre-2023 or incomplete one-live-GET result is treated** under the
one-GET rule — exactly one of: (i) accept the incomplete/empty result as a
substrate limitation; (ii) classify the source as not usable under that
firewall strategy; or (iii) stop without proceeding to Gate 5. **No automatic
second GET and no retry** is permitted under any of these.

**Adjudication (decision, not authorization).** Option **D is rejected**
(directly inconsistent with the binding no-2023+ rule). Option **A** is the
safe floor. Option **E** is preferred *iff* a genuine pre-2023-bounded source
is identified (open question; not established). Absent E, the recommended
posture is a **B+C hybrid**: one live GET, streaming scan, **abort on first
2023+ token**, emitting **aggregate counts only** and **never** real
post-2022 filenames — i.e. B's low-exposure transport with C's
aggregate-only emission discipline. This is a *policy recommendation only*;
the actual body-access authorization (Gate 4B) is separate and not granted
here.

**Gate 4B design-comparison requirement.** Before authorizing *any* body
access, Gate 4B must **explicitly compare at least the following two
live-body firewall strategies**, and must **re-adjudicate the 2023+ firewall**
in doing so:

- **Strategy I — Pure stream-abort-on-first-2023+:** strongest surface-level
  firewall; may lose completeness depending on listing order (per the
  ordering note above); minimizes exposure of real post-2022 strings (scan
  halts at the first 2023+ token).
- **Strategy II — Segregated streaming scan:** streams the response once;
  emits/stores only pre-2023 recognized filenames and aggregate counters;
  drops/redacts real 2023+ tokens immediately; never stores, logs, prints, or
  surfaces real post-2022 filenames; preserves more R4 instrumentation and can
  be order-robust; carries a **higher firewall cost** because real 2023+
  strings briefly enter classifier memory before being dropped.

This memo does **not** choose between Strategy I and Strategy II (the §6
recommendation's "B+C hybrid" wording is unchanged and is a posture, not a
Gate 4B selection). The binding requirement is that **Gate 4B must make this
choice explicitly**, with the 2023+ firewall (§3 redaction precondition, §4
rule) adjudicated again at that gate.

## 3. Sub-decision C — 2023+ breach-example handling

**Question (Gate 3 forward note).** The Gate 2 extractor's
`Protocol2023PlusBreach` currently carries up to 3 example filenames in its
message and up to 10 in `.rejected_examples`. Synthetic examples were safe in
Gate 2; **real** post-2022 examples require a firewall decision.

**Adjudication (decision, not authorization).** For any future *live/body*
context:
- **Exact real post-2022 filenames are FORBIDDEN** in exception messages,
  `.rejected_examples`, logs, JSON, markdown, stdout, or tests.
- Permitted: **aggregate counts only** (e.g. `rejected_2023plus = N`), and at
  most a **non-identifying** characterization (e.g. "first rejected token at
  scan offset k", or "rejected span: daily-form, year>=2023") with **no
  filename, no date digits beyond the year-class boundary**.
- Therefore a future live-access patch (Gate 4B/4C) **must modify the Gate 2
  extractor's example-carrying behavior** so that, in any live path, real
  rejected filenames are aggregated/redacted before they can reach any
  surface. (Under synthetic Gate 2 tests the current behavior remains
  acceptable; the change is a live-path firewall requirement, scoped to
  Gate 4C, not done here.)
- Until that redaction change is implemented and reviewed, **no live body
  read may occur** — the example-carrying behavior is itself a blocking
  precondition.

## 4. Sub-decision D — binding firewall preservation rule

Any future live body-access patch (Gate 4B/4C) is bound by:

- **May be read:** the index/listing body, transiently, in process memory
  only, solely to extract 2005–2022 unit keys.
- **May be stored:** only (i) the in-window (2005–2022) recognized unit keys
  and slot map, (ii) aggregate instrumentation counts
  (`recognized_in_window`, `ignored_out_of_window`, `rejected_2023plus`,
  `unrecognized_tokens`, `malformed_gdelt_tokens`), (iii) non-content
  transport metadata (status, content-type, content-length, hash). **No raw
  listing body, no post-2022 filename, no post-2022 date.**
- **May be printed/emitted:** in-window keys and aggregate counts only.
- **Must be redacted / aggregated:** every post-2022 token — never a
  filename, never a post-2022 date; only the integer `rejected_2023plus`.
- **Full-scan-then-fail-closed:** **not permitted on a live body** (it
  materializes the full post-2022 listing in memory). Permitted only on
  synthetic fixtures (Gate 2 status quo).
- **Stream-abort-on-first-2023+:** **required** for any live body read — the
  scan must stop at the first 2023+ token and must not continue enumerating
  post-2022 entries.
- **Post-2022 filenames may NEVER appear** in logs, exceptions,
  `.rejected_examples`, JSON, markdown, stdout, CSV, or tests in any live
  path. Synthetic tests must use only fabricated `2023…`/`2024…` strings.

This rule is binding on Gate 4B/4C; it does not itself authorize them.

## 5. Future gate sequence (defined; none entered or authorized here)

- **Gate 4A — R1 patch authorization (offline).** Authorize the
  request-target change to `…/events/index.html` + tests; no retrieval, no
  run. Separate memo.
- **Gate 4B — body-access authorization.** Decide and authorize (or forbid)
  one live index-body GET under §2 (recommended B+C hybrid) and the §4
  firewall rule; or adopt A/E. Separate memo; must re-state §3/§4.
- **Gate 4C — body-access implementation + review.** Implement the §4
  firewall (incl. §3 redaction of rejected examples on the live path) and
  the stream-abort scanner; offline-tested first; reviewed before any live
  read. Separate gate.
- **Gate 5 — fresh count-only feasibility run authorization** *(only if still
  warranted after 4A–4C)*: a brand-new run-authorization memo + separate
  run-enablement commit + one-run-only + inert-restore (diagnostic memo
  `5e0ed4b` §7 unchanged). The consumed `60ec1521`/`fe742555` remain spent.

Each gate is separate and individually reviewed. This memo enters none of
them.

## 6. Recommended decision (recommendation only — authorizes nothing)

1. **R1: approve in principle**, implement at a separate **offline Gate 4A**
   (target → `…/events/index.html`, with tests); R1 carries no retrieval/run
   authority.
2. **Body access: do not forbid outright, but do not authorize yet.** Prefer
   **Option E** if a genuine pre-2023-bounded source is identified;
   otherwise authorize, at a separate **Gate 4B**, a single **B+C hybrid**
   live GET (streaming scan, abort on first 2023+, aggregate-only emission),
   strictly bound by §4.
3. **2023+ examples: forbid real post-2022 filenames** anywhere on any live
   path; require the §3 redaction change as a **blocking precondition**
   (Gate 4C) before any live read.
4. **Firewall rule §4 is binding** on all of Gate 4B/4C.
5. **Gate 5 remains gated** and is not warranted until 4A–4C close.

This draft authorizes nothing. R1 implementation, body access, the redaction
change, and any future run each require their own separate, explicitly-
reviewed authorization.

## 7. Stop condition

This memo implements no code, edits no tests, contacts no GDELT endpoint,
fetches no documentation, performs no GET/HEAD, inspects no event
archive/index body, runs no retrieval, loads no market data, touches no real
2023+ resource, drafts no Step 2, authorizes no run, modifies no consumed F4
output, and updates no memory. It records adjudications and a recommended
decision only; every downstream step remains separately gated.

— end of Gate 4 body-access / R1 firewall decision memo (draft v0.1) —
