# Lane 2 — GDELT 1.0 Gate 2 Offline Remediation Implementation Report

**Version:** v0.1 (Gate 2 implementation report; uncommitted)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft. Not committed. Reports an offline parser/discovery
remediation implementation. Authorizes nothing further.

**Governing / chain (committed):**
- Discovery-defect remediation **design memo** — `12ae078` (**binding**)
- Remediation-patch **authorization** (Gate 1) — `be2a7df` (**binding**;
  this is its Gate 2)
- Phase A `38011be` (D0) · Substep 1 `10b80c7` (D2 ruled out) · Substep 2A
  `9a8fb7b` (D1-supported)
- Consumed run-enablement (spent) — `fe742555`; inert-restore — `9e329c2`

---

## 1. Files changed

- **`src/lane2_gdelt1_count_feasibility.py`** — added `import re`; added
  `IndexExtraction` dataclass, `_legacy_whitespace_index_tokens` (regression
  helper), `_classify_gdelt1_filename`, `extract_index_units` (R2/R4/R5/R6);
  refactored `fetch_archive_index` to fetch text via the **injected opener**
  (unchanged) and delegate parsing to `extract_index_units` (added optional
  `return_detail`). **No constant/guard changed**:
  `DEFAULT_GDELT1_BASE_URL` (R1) untouched; `REAL_RETRIEVAL_ENABLED=False`
  and runner `COUNT_FEASIBILITY_AUTHORIZED=False` unchanged; output
  allow-list / tripwires unchanged.
- **`tests/test_lane2_gdelt1_count_feasibility.py`** — appended 9 synthetic
  Gate 2 tests (fabricated HTML/listing fixtures, in-memory fake openers
  only).

## 2. Tests run and results

- `pytest tests/test_lane2_gdelt1_count_feasibility.py` → **66 passed, 0
  failed** (57 prior + 9 new). Existing count-only safety tests
  (seal guards, allow-list, runner-guard, F-class, orchestrator) **remain
  passing**.
- New tests: legacy-whitespace failure-mode regression; R2 HTML-form
  recognition; R5 2005–2022 filter; R4 instrumentation (no silent drops);
  R6 hard-fail on 2023+ before returning keys; R6 hard-fail blocks
  `fetch_archive_index` downstream; robust extractor via fake opener
  (+ `return_detail`); malformed-token counting; no-network-symbols static
  check on the extractor path.
- One mid-implementation failure (instrumentation double-counted a filename
  appearing in both `href` and link text) was fixed by deduping all
  categories by distinct filename; re-run green.

## 3. R1 deferral confirmation

**R1 (request-target change `.../events/` → `.../events/index.html`) remains
deferred and was NOT implemented.** `DEFAULT_GDELT1_BASE_URL` is unchanged;
`fetch_archive_index` still requests whatever URL it is given via the injected
opener. R1 belongs to the later, separately-adjudicated Gate 4 body-access
decision (per `12ae078` §3 testability asymmetry and `be2a7df` §2).

## 4. Boundary confirmations

No live contact; no GET; no HEAD; no event archive/index body access; no
event-file request/download; no count-only feasibility rerun; no
run-enablement / guard flip; no market data; no real 2023+ resource touch
(only fabricated `2023…`/`2024…` fixture strings to verify hard-fail); no
Step 2; no source pivot. Tests use only in-memory fake openers and string
fixtures — no real opener / `urllib` / `requests` / `socket` / network path
(asserted by `test_no_network_symbols_in_extractor_path`).

## 5. How R2/R4/R5/R6 were implemented

- **R2 (robust extractor).** `_GDELT1_FILE_RE` matches the documented GDELT
  1.0 forms — yearly `YYYY.zip`, monthly `YYYYMM.zip`, daily
  `YYYYMMDD.export.CSV.zip` — anywhere in arbitrary text, surviving HTML
  anchor tags, quotes, attributes, and angle brackets. `_classify_gdelt1_
  filename` maps `(stem, is_export)` to a PlannedUnit-style key + rep date,
  returning `None` for ambiguous forms (8-digit without `.export.CSV`,
  6-digit with it) so they are counted, not silently accepted.
- **R4 (instrumentation).** `IndexExtraction.instrumentation` reports
  `recognized_in_window`, `ignored_out_of_window`, `rejected_2023plus`,
  `unrecognized_tokens`, `malformed_gdelt_tokens` — all deduped by distinct
  filename so href/link-text duplication does not inflate counts. Non-GDELT
  file-like tokens (e.g. `index.html`, `masterfilelist.txt`) are surfaced as
  `unrecognized_tokens`, never silently dropped.
- **R5 (immediate 2005–2022 filter).** Applied at extraction time: a
  recognized GDELT-form file whose rep date is `< 2005-01-01` (and pre-2023)
  is counted as `ignored_out_of_window` and excluded from `keys` — before any
  key list is built or returned.
- **R6 (hard-fail on 2023+).** Any recognized GDELT-form filename with rep
  date `>= 2023-01-01` is collected as `rejected`; after counting completes,
  `Protocol2023PlusBreach` is raised (with `.instrumentation` and
  `.rejected_examples` attached) **before** `keys`/`slot_actual_keys` are
  constructed or returned.

## 6. How 2023+ hard-fail occurs before downstream logic

`extract_index_units` computes full instrumentation, then — if any 2023+
GDELT-form filename was seen — raises `Protocol2023PlusBreach` **before**
building or returning `IndexExtraction.keys`. `fetch_archive_index` calls
`extract_index_units` immediately after reading the listing text and **before
returning** any `(keys, slots)` tuple. Therefore a 2023+ listing aborts at the
discovery layer: no keys reach `build_retrieval_plan`,
`verify_archive_layout`, downloading, parsing, counting, or any planning
logic. Verified by `test_r6_hard_fail_on_2023plus_before_returning_keys`
(extractor level) and `test_r6_hardfail_blocks_downstream_via_fetch_archive_
index` (fetch level). The pre-existing seal guards
(`assert_no_2023plus`, parser/aggregate/plan) remain in force as defense in
depth.

## 7. Canonical-preservation confirmation

The consumed F4 run record
`results/lane2_gdelt1_count_feasibility/20260518T163302Z/`
(`count_feasibility_metadata.json`, `feasibility_summary.md`) was **not
touched** by Gate 2 — not read, modified, moved, deleted, regenerated, or
overwritten. It remains **canonical and uncommitted**, original mtimes intact
(`2026-05-18 18:33:03`).

## 8. No-authorization confirmation

This Gate 2 implementation authorizes **no** count-only feasibility rerun,
**no** live/body access, **no** R1 change, **no** run-enablement, **no**
source pivot, and **no** Step 2. The patch is offline parser/discovery logic
+ synthetic tests only. Gate 3 (conformance review), Gate 4 (body-access / R1
with 2023+ firewall re-adjudicated), and Gate 5 (fresh count-only run
authorization) each remain separate and require their own explicit review.

— end of Gate 2 offline remediation implementation report (draft v0.1) —
