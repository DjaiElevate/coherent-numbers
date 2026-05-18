# Lane 2 — GDELT 1.0 Layout-Diagnostic Phase A Report

**Version:** v0.1 (Phase A offline diagnostic report; uncommitted)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft. Not committed. Reports a **provisional** Phase A finding
only. Authorizes nothing.

**Governing / bounding (committed):**
- Count-only feasibility protocol — `147c0d4` (**binding**)
- Layout-feasibility diagnostic memo — `5e0ed4b` (**binding for this
  investigation**)
- Phase A offline diagnostic authorization — `c06ded4` (this report executes
  Phase A under it)
- Consumed run-enablement (spent) — `fe742555`; inert-restore — `9e329c2`

---

## 1. Provisional Phase A class

**Provisional class: D0 — investigation cannot resolve the ambiguity within
the offline-only envelope.**

Rationale (per `c06ded4` §4a): D1 is **not affirmatively confirmable** (offline
synthetic tests show the parser *correctly* recognizes a fabricated known-good
listing in the documented-template form); D2 is **not assignable** (committed
artifacts explicitly mark the layout assumption as unverified/overridable —
they do not show it wrong, and identify no alternative stable layout); D3 is
**only provisional** (the F4 signature is consistent with an access/index
issue but cannot be confirmed without live access, which Phase A prohibits).
Per the §4a D0-fallback rule, when D2/D3 cannot be resolved offline the correct
Phase A output is **D0 with a Phase B recommendation**.

No D5: only authorized read-only inspection and the existing committed
synthetic tests were used; no breach occurred.

## 2. D1 vs D2 vs D3 evidence table

| Class | Supporting evidence (Phase A) | Ruling-out / non-confirming evidence (Phase A) | Phase A lean | Phase A sufficient? |
|---|---|---|---|---|
| **D1** parser/layout-discovery bug | `fetch_archive_index` tokenizer is `text.split()` + outer-char `strip('"\'<>')` only (src ~1000–1006); a realistic HTML directory index (`<a href="YYYYMMDD.export.CSV.zip">`) would split into tokens whose `name.split(".")[0]` is non-digit (e.g. `href="20150312`) and be silently discarded → `available=0` → all-3650-missing → exactly the observed all-zero-residue F4 signature. So a parser/discovery-robustness limitation *could* produce this result. | Committed synthetic tests pass: a fabricated **known-good** whitespace-separated bare-filename listing (`2005.zip`, `200601.zip`, `20130401.export.CSV.zip`) **is** correctly recognized into unit keys, and 2023+ correctly aborts (`test_fetch_archive_index_parses_and_blocks_2023plus`, layout/url tests — 13/13 passed). No parser defect is demonstrated for the documented-template form. Whether the live endpoint actually returns HTML (vs a bare list) is **unknowable offline** (no doc fetch, no live read). | Possible but **unconfirmed** | **No** |
| **D2** documented archive-layout mismatch | None established offline. | Committed artifacts (`src` docstring ~lines 44–54) explicitly label the GDELT 1.0 filename/dating regime "documentation-level … to be verified at freeze; overridable — not asserted as a data-derived fact." Per `c06ded4` §4a, D2 may be assigned **only** if committed artifacts/already-known references **already show** the assumption wrong **and** an alternative stable 2005–2022 layout is identifiable. They show it *unverified*, not *wrong*, and identify no alternative. | **Not assignable offline** | **No** |
| **D3** endpoint/environment/index-access issue | Consumed F4 signature: `files_available=0`, `files_in_archive_not_planned=0`, `files_unexpected_naming=0`, `files_date_unit_mismatch=0`, `files_missing=3650` — the empty/non-listing-transport signature (per diagnostic memo §6 preliminary note), not a divergent-listing signature. Consumed run used `_real_opener` (urllib) against `DEFAULT_GDELT1_BASE_URL` in a sandboxed environment. | The same all-zero signature is **also** consistent with a non-empty-but-format-unrecognized response (D1-flavored) because `fetch_archive_index` *discards* unparsed tokens and the consumed run persisted **neither** the raw response **nor** an unparsed-token count. Empty-transport vs unrecognized-format **cannot be distinguished offline**; confirming D3 requires observing the live index response (Phase B). | **Provisional only** | **No** |

**Disambiguation summary:** the three classes collapse to a single unresolved
question that Phase A is structurally unable to answer offline — *what did the
live `events/` index endpoint actually return (empty/blocked vs non-empty),
and in what format?* The instrumentation gap (`fetch_archive_index` does not
record raw-response size or unparsed-token count) makes the consumed F4
intrinsically ambiguous between D1 and D3 from artifacts alone.

## 3. Phase A sufficiency

**Phase A is NOT sufficient.** It can rule *in* none of D1/D2/D3
conclusively: D1 is unconfirmed (parser handles the documented form
correctly), D2 is not assignable from committed artifacts, D3 is only a
provisional access reading. **A separately authorized Phase B is required.**

## 4. Phase B recommendation (NOT authorized here; questions only)

Phase B should be split into separately authorized substeps; each remains
ungranted:

- **Phase B substep 1 — read-only documentation fetch.** Precise question:
  *"What is the actually-published GDELT 1.0 `events` archive layout for
  2005–2022 — the real base URL, the real file-naming/granularity convention
  (in particular whether pre-2013-04-01 history is exposed as yearly/monthly
  files at this endpoint or whether GDELT 1.0 daily `export` files begin only
  at 2013-04-01), and the index/listing response format (HTML directory page
  vs plain file list vs a master file-list resource)?"* — resolves **D2**
  (is the documented/template assumption wrong, and is an alternative stable
  2005–2022 layout identifiable?).
- **Phase B substep 2 — at most one live index-metadata read, only if still
  needed after substep 1.** Precise question: *"Does a single read of the
  actual index endpoint return a non-empty listing, and if so in what format —
  does it contain recognizable 2005–2022 unit filenames that the current
  `fetch_archive_index` tokenizer fails to extract (⇒ a D1
  discovery-robustness defect), or does it return empty/blocked/non-listing
  content (⇒ a D3 access issue)?"* — disambiguates **D1 vs D3**.

Substep 2 is gated behind substep 1 and is justified only if documentation
alone does not resolve the class. Either substep, and any remediation it might
imply, requires its own explicit authorization.

## 5. Canonical-preservation confirmation

The consumed F4 run record
`results/lane2_gdelt1_count_feasibility/20260518T163302Z/`
(`count_feasibility_metadata.json`, `feasibility_summary.md`) was inspected
**read-only** and remains **canonical, unmodified, non-overwritten** — not
moved, deleted, regenerated, or copied back. Original mtimes intact
(`2026-05-18 18:33:03`).

## 6. No-authorization confirmation

This Phase A report authorizes **no** future count-only run, **no**
parser/layout remediation patch, **no** Phase B (nor either Phase B substep),
**no** source pivot, and **no** Step 2. The provisional D0 finding and the
D1-flavored instrumentation observation in §2 *describe* possible paths; they
**do not** authorize any. All such steps remain gated by diagnostic memo
`5e0ed4b` §7 and/or a separate explicit micro-authorization.

— end of Phase A layout-diagnostic report (draft v0.1) —
