# Lane 2 — GDELT 1.0 Discovery-Defect Remediation Design Memo

**Version:** v0.1 (design-and-constraints memo; not an implementation or run
authorization)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. **Authorizes nothing.** Documents
the discovery-layer defect and defines the design space for a *future*
remediation patch. Does **not** authorize implementation, event-archive body
access, parser changes, a count-feasibility rerun, Step 2, or a source pivot.

**Governing / diagnostic chain (committed):**
- Count-only feasibility protocol — `147c0d4` (**binding**)
- Retrieval-wiring path — `9528fe5`
- Run-enablement (**consumed/spent**) — `fe742555`; inert-restore —
  `9e329c2`
- Layout-feasibility diagnostic memo — `5e0ed4b` (**binding**)
- Phase A authorization — `c06ded4`; Phase A report (**D0**) — `38011be`
- Phase B Substep 1 doc-fetch authorization — `b982e7c`; report
  (**D2 ruled out**) — `10b80c7`
- Phase B Substep 2A HEAD authorization — `1ccb99c`; report
  (**D1-supported**) — `9a8fb7b`

---

## 0. Canonical diagnostic state (frozen)

- The single authorized count-only run under `fe742555` produced **F4-missing**:
  3,650 planned units, **0 parseable available units**, no GDELT files
  downloaded, no counts computed; `9e329c2` restored runner inert state.
- `38011be` closed **D0** (offline inspection could not distinguish D1/D2/D3).
- `10b80c7` **ruled out D2** (documentation matched load-bearing GDELT 1.0
  layout assumptions).
- `9a8fb7b` **supported D1** (documented `.../events/index.html` exists and is
  non-empty by HEAD metadata: `200`, `Content-Length 556438`, `text/html`,
  no redirect; **D3 ruled against** for that resource).
- **No rerun is authorized. No patch is authorized.**

## 1. Defect statement

The consumed F4-missing result is best explained as a **Lane 2
discovery-layer defect, not a substrate veto** of GDELT 1.0 for the
2005–2022 count-only feasibility question. (D2 ruled out; D3 ruled against
for the documented index; the resource demonstrably exists and is
substantial.)

Candidate defect components (not all independently proven; see §2):

- **(a) Request-target defect.** The wiring fetches the directory path
  `DEFAULT_GDELT1_BASE_URL = http://data.gdeltproject.org/events/`, whereas
  the documented, demonstrably-existing listing resource is
  `.../events/index.html`. The request may not be hitting the listing
  resource at all.
- **(b) Discovery/parser defect.** `fetch_archive_index` extracts via
  whitespace-split + outer-character strip, which would not extract filenames
  from an HTML index listing (`Content-Type: text/html`, ~556 KB). A correct
  listing could be received yet yield zero recognized units.
- **(c) Instrumentation defect.** The original F4 path preserved neither
  raw-response metadata (size/content-type/status) nor an unparsed-token /
  unrecognized-link count, making offline D1/D3 disambiguation impossible
  until the Substep 2A HEAD probe.

## 2. Evidence basis

| Component | Supporting committed artifact(s) | Strength of claim |
|---|---|---|
| (a) Request-target defect | `9a8fb7b` (documented `index.html` exists, 200/non-empty; wiring constant targets `.../events/`); `10b80c7` (documentation names `.../events/index.html` as the listing resource) | **D1-supported**, not a confirmed mechanism — Substep 2A probed only `index.html` via HEAD; it did not observe what the wiring's actual directory-path request returns |
| (b) Discovery/parser defect | `9a8fb7b` (`Content-Type: text/html`, ~556 KB — an HTML page the whitespace tokenizer would not parse); `38011be` (offline reasoning that an HTML index would be silently discarded → `available=0`) | **D1-supported / plausible**, not confirmed — no body was ever parsed; the failure to extract from a real HTML body has not been directly observed, only inferred |
| (c) Instrumentation defect | `38011be` (offline D1-vs-D3 indistinguishable because raw response / unparsed-token count not persisted); F4 metadata in the consumed `20260518T163302Z` record (no raw-response fields) | **Established** — this is a property of the committed code/outputs, directly verifiable, not probabilistic |

Language discipline: components (a) and (b) remain **"D1-supported"**
(consistent with all evidence, best explanation) — **not** "confirmed
mechanism" — because no listing body was ever retrieved or parsed under any
authorization. Component (c) is **established** as a code/output property.

## 3. Remediation design space (discussion only — nothing chosen or authorized)

Possible future patch components, for design consideration only:

- **R1.** Change the source listing target to the documented `index.html`
  (or otherwise make the listing resource explicit and verifiable) rather
  than the bare directory path.
- **R2.** Replace whitespace tokenization with a robust HTML/listing filename
  extractor (e.g. anchor-href / link extraction) tolerant of the documented
  index format, without inferring beyond extracted filenames.
- **R3.** Preserve **bounded** raw-response audit metadata (status,
  content-type, content-length, byte count, hash) **without storing event
  data or listing bodies** — an audit artifact, not a data cache.
- **R4.** Record unparsed-token / unrecognized-link counts so a future F4 is
  self-diagnosing (D1 vs D3 distinguishable from the artifact alone).
- **R5.** Enforce the **2005–2022 extraction filter at the moment of filename
  extraction** — filter to the pinned window before any persistence or
  counting.
- **R6.** **Hard-fail on any 2023+ filename/resource** encountered before
  counting or persistence (extend existing `Protocol2023PlusBreach`/seal
  guards into the discovery layer).
- **R7.** Maintain the existing output allow-list and prohibited-output
  tripwires (`ALLOWED_OUTPUT_BASENAMES`, `_checked_path`,
  `_assert_outputs_allowed`) unchanged in spirit; any new audit artifact must
  be added to the allow-list explicitly and reviewed.

These are **candidate components**, not a chosen design and not authorized.
Their interactions (e.g. R2 + R5 + R6 ordering) are noted as design questions
for the future remediation-patch authorization memo.

**Testability asymmetry (design consideration, not an authorization).** The
candidate components do not share the same verification surface. The
discovery/parser/tokenizer behavior (R2, R4, R5, R6) is **fully testable
offline** using synthetic, representative HTML index fixtures and in-memory
fake openers — no GDELT contact is needed to prove an HTML-aware extractor
correctly recognizes documented-form filenames, filters to 2005–2022, and
hard-fails on 2023+. The request-target behavior (R1) **cannot be fully
resolved offline**: whether `.../events/` versus `.../events/index.html`
actually returns a listing (and in what form, with what redirect/status) is a
**server/environment-side fact** not determinable from committed artifacts or
synthetic fixtures alone. Consequently, a future remediation-patch
authorization should **separate the two**: (i) offline parser-fixture
validation of R2/R4/R5/R6 against synthetic HTML, gated and reviewable with no
network; and (ii) any R1 request-target confirmation, which belongs to a
**later, separately-adjudicated live/body-access decision** (subject to the §4
2023+ firewall) and is **not** bundled into the offline patch step. This memo
neither authorizes nor sequences those steps beyond noting the asymmetry.

## 4. 2023+ firewall design requirement

A current, full GDELT 1.0 index almost certainly contains **post-2022
filenames** (daily files continue past 2022-12-31). Any future parser **must
not silently ingest** such an index. This memo defines the firewall design
requirement but **does not choose or authorize** a body-access strategy.

Firewall-safe extraction strategy must be defined **before any body-level GET
is ever authorized**. Options compared (none authorized):

- **(A) Fetch-then-reject.** Retrieve the listing body, then immediately
  filter/abort on any 2023+ filename **before** storing or counting any
  parsed listing. Risk: a 2023+ filename transits process memory before
  rejection; mitigation must ensure no 2023+ token is persisted, counted, or
  printed.
- **(B) Streaming scan with immediate abort.** Stream the listing and abort
  on the first 2023+ token, never materializing the full post-2022 listing.
  Lower exposure than (A) but still touches 2023+ tokens transiently.
- **(C) Pre-2023-only listing source.** Use only a historical / explicitly
  pre-2023-bounded listing source (if one is identified), so no 2023+
  filename is ever transferred. Lowest exposure; contingent on such a source
  existing.

**This design memo explicitly does not choose or authorize any body-access
strategy.** Selection among (A)/(B)/(C), and whether any body-level access is
permitted at all, is deferred to a separate, explicitly-reviewed
authorization that must re-adjudicate the 2023+ firewall (per `10b80c7` §3
and `1ccb99c` §8).

## 5. Anti-rescue / anti-tuning constraints (binding on any future work)

- **No parser tuning to produce a desired event count.** Remediation targets
  *correct discovery of the listing*, never a target count, threshold, or
  feasibility class.
- **No market data or market outcomes** of any kind.
- **No Step 2 drafting**; no hypothesis verdicts.
- **No count-feasibility rerun under the spent authorization** `60ec1521` /
  `fe742555` (consumed; one-run-only already used).
- Any future remediation patch must be **reviewed before any data-touching
  run**.
- Any future count-only run requires a **fresh authorization memo**, a
  **separate run-enablement commit**, **one-run-only** execution, and a
  **separate inert-restore commit** (diagnostic memo `5e0ed4b` §7 unchanged).
- The consumed F4 record (`results/lane2_gdelt1_count_feasibility/
  20260518T163302Z/`) remains **canonical, non-overwritten**; any future run
  writes to a new timestamped directory.

## 6. Required future gates (sequence; none entered by this memo)

1. **Commit this design memo only** (no code, no run).
2. Draft a **remediation-patch authorization memo** (defines exact patch
   scope, fixtures-only test plan, conformance spec; authorizes no run).
3. **Implement the patch using synthetic/local fixtures only** (no GDELT
   contact, no body access) under that authorization.
4. **Review** tests / spec conformance (offline; fake openers / in-memory
   fixtures only).
5. **Separately decide** whether to authorize any body-level index access,
   **explicitly adjudicating the 2023+ firewall** (choose among §4 (A)/(B)/(C)
   or forbid).
6. **Only after that**, draft a **fresh count-only feasibility run
   authorization** (new memo + separate run-enablement + one-run-only +
   inert-restore).

Each gate is separate and individually reviewed. This memo enters **only**
gate 0 (drafting); it does not enter gate 1+ and authorizes none of them.

## 7. Stop condition

This memo implements no code, runs no test, contacts no GDELT endpoint,
fetches no documentation, performs no GET or HEAD, inspects no event
archive/index body, modifies no consumed F4 output, and updates no memory. It
records the discovery-defect analysis and the constrained design space only.
No remediation, body access, rerun, Step 2, or source pivot is authorized;
each remains gated by a separate, explicitly-reviewed authorization.

— end of discovery-defect remediation design memo (draft v0.1) —
