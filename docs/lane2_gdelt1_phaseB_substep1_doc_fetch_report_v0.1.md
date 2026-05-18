# Lane 2 — GDELT 1.0 Phase B Substep 1 Documentation-Fetch Report

**Version:** v0.1 (Phase B Substep 1 documentation-fetch report; uncommitted)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft. Not committed. Reports a documentation-only D2 finding.
Authorizes nothing.

**Governing / bounding (committed):**
- Layout-feasibility diagnostic memo — `5e0ed4b` (**binding**)
- Phase A authorization — `c06ded4`; Phase A report (prov. **D0**) —
  `38011be`
- Phase B Substep 1 doc-fetch authorization — `b982e7c` (this report
  executes Substep 1 under it)
- Consumed run-enablement (spent) — `fe742555`; inert-restore — `9e329c2`

---

## 1. D2 finding

**D2 — RULED OUT.**

The documented GDELT 1.0 Event Database archive layout (per the GDELT
documentation page `gdeltproject.org/data.html`) is **consistent** with the
committed Lane 2 layout assumptions on every load-bearing point: base
URL/path, daily filename convention, the 2013-04-01 daily-regime boundary, the
pre-2013 monthly/yearly storage, and the pre/post date-unit semantics. The
committed assumptions are **not wrong and not contradicted** by documentation;
therefore the consumed F4-missing result is **not** explained by a documented
archive-layout mismatch. (D2 is the *documented-layout* class; ruling it out
does not resolve D1 vs D3 — see §3.)

One discovery-layer **observation** (not a D2 mismatch, not a patch
authorization): the committed wiring fetches the *directory path*
`http://data.gdeltproject.org/events/`, whereas the documentation names the
listing resource explicitly as `…/events/index.html`. This is a parser/
discovery-layer question (D1 family), not a documented archive-layout error.

## 2. Evidence table

| Committed Lane 2 assumption | Documentation statement (gdeltproject.org/data.html) | Implication for 2005–2022 coverage | Implication for 2013-04-01 regime boundary | Implication for consumed F4-missing |
|---|---|---|---|---|
| `DEFAULT_GDELT1_BASE_URL = "http://data.gdeltproject.org/events/"` | Download location referenced as `http://data.gdeltproject.org/events/index.html` | Same host/path family → base path **consistent** | n/a | Base path is correct; but wiring requests the *directory*, doc names *index.html* as the listing → a **D1-family discovery** question, not a layout mismatch |
| Daily template `"{yyyy}{mm}{dd}.export.CSV.zip"` | "YYYYMMDD.export.CSV.zip"; example "20130523.export.CSV.zip" | Post-2013 daily naming **matches exactly** | Daily files begin at the boundary — consistent | Daily naming is **not** the F4 cause |
| `REGIME_DAILY_START = date(2013, 4, 1)` | "Beginning with April 1, 2013, files are created daily" | Regime split date **matches** | 2013-04-01 boundary **verbatim-confirmed** | Boundary handling correct (consumed `boundary_2013_04_01_handled = true`) — not the F4 cause |
| Pre-boundary monthly/yearly, by **event date**; `PRE_REGIME_YEARLY_THROUGH_YEAR = 2005` (yearly ≤2005, monthly 2006-01..2013-03) | "Through March 31, 2013 records are stored in monthly and yearly files by the date the event took place" | Existence of pre-2013 **monthly + yearly by event date confirmed**; the exact yearly(≤2005)/monthly(2006+) cutover year is **plausible but not verbatim** on this page (not contradicted) | Pre-boundary = monthly/yearly — consistent | Even a wrong yearly/monthly cutover would yield *partial* unexpected/naming residue, **not** the observed 0-available / 0-residue all-3650-missing signature → does **not** explain F4 |
| Pre-boundary by event date; post-boundary by date found in news media (`src` regime docstring) | "records are stored by the date the event was found in the world's news media rather than the date it occurred" (post 2013-04-01) | Date-unit semantics **match exactly** | Consistent across the boundary | Not the F4 cause |
| (Index/listing format — committed code assumes a whitespace-tokenizable listing) | Doc references `…/events/index.html` but **does not describe its format** (HTML page vs plain list) | — | — | The **live index response format** is the unresolved variable → D1 (format not parseable by the tokenizer) vs D3 (empty/blocked access) |

## 3. Is Phase B Substep 2 still needed?

**Yes.** Substep 1 conclusively rules out **D2** but, by design, cannot
resolve the **D1-vs-D3** question carried over from the Phase A report
(`38011be` §2): the consumed all-3650-missing / zero-residue F4 signature is
offline-indistinguishable between a non-empty-but-unrecognized index response
(D1 discovery-robustness) and an empty/blocked response in the run environment
(D3 access). Documentation states the index format but does not reveal what
the endpoint actually returned during the consumed run, and the wiring fetched
the directory path rather than the documented `index.html`. Resolving this
requires observing the live index resource — Phase B Substep 2.

**2023+ firewall note (binding on any future Substep 2 authorization).**
Although Substep 2's unresolved question is now precise — whether the
documented `.../events/index.html` listing is non-empty/recognizable versus
empty/blocked — any future live index-metadata authorization must explicitly
adjudicate the 2023+ firewall. A current archive index may expose post-2022
filenames or metadata. This Substep 1 report does **not** authorize that
contact, does **not** decide whether such exposure is permissible, and does
**not** weaken the existing no-2023+ rule. If a live index read cannot be
performed without post-2022 metadata exposure, the Substep 2 authorization
memo must either (a) forbid the read and leave D1/D3 unresolved, or (b) create
a separately reviewed firewall exception before any contact.

## 4. Exact remaining question for Substep 2

> *"Does a single read of the documented GDELT 1.0 index resource
> (`http://data.gdeltproject.org/events/index.html`) — and, for parity, the
> directory path the committed wiring actually requests
> (`http://data.gdeltproject.org/events/`) — return a non-empty listing, and
> in what format (HTML directory/index page vs plain whitespace-tokenizable
> file list)? Specifically: does the live response contain recognizable
> 2005–2022 GDELT 1.0 unit filenames that the committed `fetch_archive_index`
> whitespace/strip tokenizer fails to extract (⇒ **D1** discovery-robustness
> defect), or does it return empty / blocked / non-listing content in the run
> environment (⇒ **D3** access issue)?"*

Substep 2 remains a single, separately-authorized live index-metadata read
(no event-file listing-by-listing, no event download); it is **not**
authorized by this report and requires its own micro-authorization memo.

## 5. Canonical-preservation confirmation

The consumed F4 run record
`results/lane2_gdelt1_count_feasibility/20260518T163302Z/`
(`count_feasibility_metadata.json`, `feasibility_summary.md`) was **not
touched** during Substep 1 (no read needed beyond the already-recorded Phase A
extract). It remains **canonical, unmodified, non-overwritten** — not moved,
deleted, regenerated, or copied back. Original mtimes intact
(`2026-05-18 18:33:03`).

## 6. No-authorization confirmation

This Substep 1 report authorizes **no** count-only feasibility rerun, **no**
parser/layout code patch, **no** live index-metadata read (Substep 2), **no**
source pivot, and **no** Step 2. The "D2 ruled out" finding and the
discovery-layer observation in §1 *describe* where the open question lies;
they **do not** authorize any remediation or access. All such steps remain
gated by diagnostic memo `5e0ed4b` §7 and/or a separate explicit
micro-authorization (Substep 2 in particular requires its own memo).

— end of Phase B Substep 1 documentation-fetch report (draft v0.1) —
