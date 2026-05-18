# Lane 2 — GDELT 1.0 Gate 4A R1 Offline Patch Implementation Report

**Version:** v0.1 (Gate 4A implementation report; uncommitted)
**Date:** 2026-05-19
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft. Not committed. Reports the offline R1 URL-target patch.
Authorizes nothing further.

**Governing / chain (committed):**
- Gate 4 body-access/R1 firewall **decision memo** — `bf4ef79` (**binding**)
- Gate 4A R1 offline-patch **authorization** — `745af67` (**binding**; this
  is its implementation)
- Gate 2 offline parser remediation — `6834814` · Gate 3 conformance PASS —
  `f564b77`
- Consumed run-enablement (spent) — `fe742555`; inert-restore — `9e329c2`

---

## 1. Files changed

- **`src/lane2_gdelt1_count_feasibility.py`** — added
  `DEFAULT_GDELT1_INDEX_URL = "http://data.gdeltproject.org/events/index.html"`
  (dedicated index/listing target, documented with the Gate 4A / `9a8fb7b` /
  `10b80c7` rationale); changed `fetch_archive_index`'s default `index_url`
  from `DEFAULT_GDELT1_BASE_URL` to `DEFAULT_GDELT1_INDEX_URL`; updated its
  docstring. **No other code changed.**
- **`tests/test_lane2_gdelt1_count_feasibility.py`** — broadened
  `_make_fake_opener`'s index-detection (now also accepts `…/index.html`,
  still accepts the `…/events` sentinel) so the runner integration test
  exercises the corrected default; appended 4 synthetic R1 tests.

## 2. Tests run and results

- `pytest tests/test_lane2_gdelt1_count_feasibility.py` → **70 passed, 0
  failed** (66 prior + 4 new R1). **Existing 66 tests remain passing.**
- New R1 tests: default index target = `…/events/index.html`; regression
  that the bare `…/events/` directory path is not the listing target (and
  per-file base unchanged); explicit `index_url` override still honored;
  guards inert + no network symbols in `fetch_archive_index`.

## 3. R1 URL-target change explained

The diagnostic chain (Substep 1 `10b80c7`, Substep 2A `9a8fb7b`) established
that the documented listing resource is `…/events/index.html` and that it
exists/non-empty, while the wiring requested the bare directory path
`…/events/`. R1 corrects the **index/listing request target only**:

- `DEFAULT_GDELT1_BASE_URL` (`…/events/`) is **unchanged** — it remains the
  per-FILE download base (`base + "<YYYYMMDD>.export.CSV.zip"`); changing it
  would have corrupted per-file URLs.
- A **separate** constant `DEFAULT_GDELT1_INDEX_URL`
  (`…/events/index.html`) was introduced and is now the default `index_url`
  for `fetch_archive_index`. This is the minimal change that targets the
  documented listing resource without disturbing file-download URL
  construction.
- No request is performed by this patch; the injected `opener` remains the
  sole request path. An explicit `index_url=` argument still overrides the
  default (back-compat for Gate 2 tests and future use).

## 4. Gate 2 parser/extractor intact

`extract_index_units` (R2/R4/R5/R6), `_classify_gdelt1_filename`,
`IndexExtraction`, the 2023+ hard-fail-before-downstream behavior, the
distinct-filename instrumentation, and `_legacy_whitespace_index_tokens`
(regression helper) are **unchanged**. R1 alters only which URL string is the
default listing target; the parsing of returned listing text is identical.
Verified: `test_r1_default_index_target_is_index_html` asserts the Gate 2
parser still yields the expected in-window keys; the full Gate 2 test set
(legacy regression, R2/R4/R5/R6, malformed, no-network) still passes.

## 5. Boundary confirmations

No live contact; no GET; no HEAD; no GDELT contact; no documentation fetch;
no event archive/index body access; no event-file request/download; no
count-only feasibility rerun; no run-enablement / guard flip; no Gate 4B
body-access decision; no Gate 4C redaction/body-access implementation; no
market data; no real 2023+ filename/resource touch (only fabricated fixture
strings); no Step 2; no source pivot. `REAL_RETRIEVAL_ENABLED=False` (src),
`COUNT_FEASIBILITY_AUTHORIZED=False` (runner) — both unchanged. Tests use
only in-memory fake openers — no real opener / `urllib` / `requests` /
`socket` / network (statically asserted by
`test_r1_guards_remain_inert_and_no_network_in_patch`).

## 6. Consumed F4 outputs

`results/lane2_gdelt1_count_feasibility/20260518T163302Z/` was **not
touched** — not read, modified, moved, deleted, regenerated, or overwritten.
It remains **canonical, untracked, and uncommitted**, original mtimes intact
(`2026-05-18 18:33:03`).

## 7. Gate 4B / 4C / 5 status

**Unentered and unauthorized.** R1 does not select a body-access strategy
(Strategy I vs Strategy II), does not authorize any live read, does not
implement the `bf4ef79` §3 redaction precondition, and does not authorize a
fresh count-only run. Gate 4A conformance review, Gate 4B (body-access
decision, 2023+ firewall re-adjudicated), Gate 4C (redaction implementation),
and Gate 5 (fresh run authorization, only if warranted) each remain separate
and require their own explicit authorization. `60ec1521`/`fe742555` remain
spent.

## 8. No-authorization confirmation

This Gate 4A implementation authorizes nothing further. A correctly targeted
listing URL *describes* the corrected request target; it does not authorize
sending the request.

— end of Gate 4A R1 offline patch implementation report (draft v0.1) —
