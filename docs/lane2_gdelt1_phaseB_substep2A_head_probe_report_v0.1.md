# Lane 2 — GDELT 1.0 Phase B Substep 2A HEAD-Only Probe Report

**Version:** v0.1 (Phase B Substep 2A HEAD-only probe report; uncommitted)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft. Not committed. Reports one HEAD-only metadata classification.
Authorizes nothing.

**Governing / bounding (committed):**
- Layout-feasibility diagnostic memo — `5e0ed4b` (**binding**)
- Phase A report (prov. **D0**) — `38011be`
- Phase B Substep 1 doc-fetch report (**D2 ruled out**; 2023+ firewall note
  binding) — `10b80c7`
- Phase B Substep 2A HEAD-only authorization — `1ccb99c` (this report
  executes Substep 2A under it)
- Consumed run-enablement (spent) — `fe742555`; inert-restore — `9e329c2`

---

## 1. Classification

**D1-supported — request-construction / discovery defect likely.**

A single HEAD request to the documented GDELT 1.0 index resource returned
**HTTP 200 OK** with a positive **`Content-Length: 556438`** and
`Content-Type: text/html`, with **no redirect**. Existence and non-empty
status were established **from response headers only** (no body retrieved).
The documented index resource therefore plainly **exists and is substantial
(~556 KB)** — it is not absent, blocked, or transport-empty. This **rules
against D3** (access/environment) and **supports D1**: the consumed
F4-missing result (0 available, all 3650 planned units missing, zero
unexpected/naming/date-unit residue) is most consistent with a
request-construction / discovery-layer defect rather than the resource being
unavailable. (D2 remains ruled out per `10b80c7`.)

**Supporting rationale (observation only, not a patch authorization):** the
committed wiring fetches the *directory path* `DEFAULT_GDELT1_BASE_URL =
http://data.gdeltproject.org/events/`, whereas the resource that exists and is
non-empty is the documented `…/events/index.html`; and `fetch_archive_index`
tokenizes via whitespace-split + outer-char strip, which would not extract
filenames from a ~556 KB **text/html** index page. Either or both would yield
`available = 0` → all-missing → F4 with exactly the observed zero-residue
signature. This is a D1-family request-construction/discovery defect; it is
**recorded as an observation only** and authorizes no remediation.

## 2. Exact recorded metadata (single HEAD response)

| Field | Value |
|---|---|
| Method | HEAD (exactly one request; `--max-redirs 0`, redirect-following disabled) |
| Requested URL | `http://data.gdeltproject.org/events/index.html` |
| HTTP status code | `200 OK` |
| Redirect? | No — not a 3xx; **no `Location` header returned** |
| `Location` header | (none) |
| `Content-Length` | `556438` (also `x-goog-stored-content-length: 556438`) |
| `Content-Type` | `text/html` (transport metadata only; listing content NOT inspected) |
| `Last-Modified` | `Mon, 18 May 2026 07:00:16 GMT` |
| `ETag` | `"00c896abd1326a6e09c098cddea21562"` |
| HEAD refused / unsupported? | No — HEAD supported; full response headers returned, no body required |
| Existence/non-empty established without body retrieval? | **Yes** — `200` + `Content-Length 556438` (> 0) establish a non-empty resource from headers alone |

## 3. No redirect was followed

The response was `200 OK` with **no `Location` header**, i.e. not a redirect;
there was nothing to follow. Automatic redirect-following was disabled
(`--max-redirs 0`, no `-L`). **No redirect was followed**, no follow-up
request to any `Location` URL was made, no GET fallback occurred, and **no
second HEAD request** was issued.

## 4. No response body retrieved

**No response body was retrieved, read, printed, parsed, or stored.** The
request used the HTTP HEAD method (no entity body by definition); only the
status line and response headers were observed.

## 5. No listing content or filenames inspected

**No listing content, HTML, or filenames were inspected, parsed, extracted,
counted, stored, or printed.** Only non-content transport metadata
(status, headers) was recorded; `Content-Type: text/html` and
`Content-Length: 556438` are aggregate transport facts, not listing entries.

## 6. No 2023+ filenames/resources inspected

**No 2023+ filenames or resources were inspected, extracted, counted, stored,
or printed.** A HEAD response carries no body, so no archive entries — pre-2023
or post-2022 — were transferred or observed. The 2023+ firewall (`10b80c7`
§3) was preserved by construction; the HEAD-only narrow exception in `1ccb99c`
§3 held.

## 7. Canonical-preservation confirmation

The consumed F4 run record
`results/lane2_gdelt1_count_feasibility/20260518T163302Z/`
(`count_feasibility_metadata.json`, `feasibility_summary.md`) was **not
touched** during Substep 2A. It remains **canonical, unmodified,
non-overwritten, and uncommitted** — not moved, deleted, regenerated, or
copied back. Original mtimes intact (`2026-05-18 18:33:03`).

## 8. No-authorization confirmation

This Substep 2A report authorizes **no** count-only feasibility rerun, **no**
parser/layout code patch, **no** GET / body read / listing parse, **no**
source pivot, and **no** Step 2. The D1-supported finding and the
discovery-layer observation in §1 *describe* the likely defect locus; they
**do not** authorize a fix. Any remediation remains a separately reviewed
change with no rerun authority (diagnostic memo `5e0ed4b` §7), and any future
body-level access requires its own separately reviewed authorization that
re-adjudicates the 2023+ firewall.

— end of Phase B Substep 2A HEAD-only probe report (draft v0.1) —
