# Lane 2 — GDELT 1.0 Phase B Substep 1 Documentation-Fetch Authorization

**Version:** v0.1 (Phase B Substep 1 authorization memo; documentation-only)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Authorizes — once committed and
separately initiated — a **narrow, read-only documentation investigation**
only. Authorizes no GDELT event-archive contact, no live index read, no event
retrieval, no rerun, no code change, no source pivot, and no Phase B
Substep 2.

**Governing / source context (committed):**
- Count-only feasibility protocol — `147c0d40568636ba0cf24ca00cc39c330e77ea03` (**binding**)
- Source-selection + count-feasibility authorization — `8fef80db0e103d2c22e36d589fe041abd1fb4c78`
- Run-authorization memo (consumed) — `60ec1521106e6a980f6450cb21a1ef510b4c37d5`
- Retrieval-wiring path — `9528fe51519211af17206538ed1bb5b2f9a299ec`
- Run-enablement (consumed) — `fe742555cd240150d17dd1ea255453993e34d239`
- Inert-restore safety reset — `9e329c2a80e43f17eead7836729c719b444f2823`
- Layout-feasibility diagnostic memo (**binding for this investigation**) —
  `5e0ed4bd70658767c74654db20d748794a237548`
- Phase A offline diagnostic authorization — `c06ded434722d61b5707e46c4474e6f3ae9047ea`
- Phase A diagnostic report (provisional **D0**; this Substep resolves **D2**)
  — `38011be07c21c5f0455bff719867697d4ef1925f`

---

## 1. Status

- Phase B Substep 1 authorization memo only. It authorizes a bounded future
  documentation-fetch investigation; it is not the investigation and contacts
  nothing itself.
- No data accessed in drafting. No GDELT contacted. No documentation fetched.
  No API called. No tests run. No code implemented. No market data. No 2023+
  touched/referenced/sampled/counted/consumed. No Step 2. No source pivot.
- The single authorized count-only feasibility run remains **consumed**
  (`60ec1521` / `fe742555` spent); this memo does **not** re-authorize it.
- This memo is subordinate to and bounded by diagnostic memo `5e0ed4b` and the
  Phase A authorization `c06ded4`. It is the §4 "Phase B substep 1" the Phase A
  report `38011be` recommended; it grants **only** that substep.
- **Phase B Substep 2** (a single live index-metadata read) remains
  **ungranted** and is explicitly **not** authorized here.

## 2. Purpose

Authorize, once committed and separately initiated, a narrow **read-only
documentation investigation** to resolve **D2** (documented archive-layout
mismatch) from the Phase A report.

**Research question.** What is the actually-documented GDELT 1.0 Event
Database archive layout for **2005-01-01 through 2022-12-31**, specifically:
- file naming convention;
- archive / index structure;
- pre-2013 storage / history (whether 2005–2013-03 is exposed at this product
  at all, and at what granularity);
- post-2013 daily-file regime;
- date-unit meaning before and after **2013-04-01** (event date vs date found
  in news media);
- index / listing response format (HTML directory page vs plain file list vs a
  master file-list resource);
- whether the **committed Lane 2 layout assumptions**
  (`DEFAULT_GDELT1_BASE_URL`, `DEFAULT_GDELT1_FILENAME_TEMPLATES`,
  `REGIME_DAILY_START`, `PRE_REGIME_YEARLY_THROUGH_YEAR`) are **wrong,
  incomplete, or still plausible**.

## 3. Scope

This memo authorizes **only a future documentation-fetch step**, not the fetch
itself yet, and not any event-archive contact. The investigation begins only
after this memo is committed **and** a separate explicit go-ahead is given.

### 3a. Allowed later (only post-commit and post-initiation)

- Read-only fetches of GDELT **documentation pages** (e.g. the GDELT 1.0 Event
  database / Events codebook documentation and equivalent published
  documentation references).
- Read-only fetches of **documentation-like references** that describe the
  archive layout/coverage (published codebooks, data-format/file-naming
  documentation, official descriptions). Documentation only — never an event
  data resource.
- Read-only inspection of the already-committed Lane 2 memos, `src`, runner,
  tests, and the Phase A report.
- On-paper comparison of documented layouts against the committed Lane 2
  layout assumptions.

### 3b. Strict prohibitions

- No GDELT event-archive index read.
- No request to `data.gdeltproject.org/events/` or any event-file listing
  endpoint.
- No event-file request.
- No event-file download.
- No count-only feasibility rerun (inert-restore `9e329c2` stands;
  `COUNT_FEASIBILITY_AUTHORIZED` and `REAL_RETRIEVAL_ENABLED` stay False).
- No parser patch; no production-code change; no source/test/runner change.
- No market data; no returns / CAR / abnormal returns / volatility / VIX /
  any market outcome; no model fits; no p-values; no feature importance; no
  attention-response or state-response relationships.
- No 2023+ data touch, reference, sample, count, consume, or storage —
  **except** quoted documentation statements that describe coverage in general
  terms without inspecting any 2023+ event resource.
- No Step 2; no hypothesis verdicts.
- No source pivot; no normalization / parameter / threshold / event-definition
  / output-allow-list change.
- No Phase B Substep 2 live index-metadata read.
- No modification, relocation, deletion, regeneration, or overwrite of the
  consumed F4 outputs.

The dividing line: **documentation describing the archive is in scope; the
event archive, its index/listing endpoint, and any event file are not.**

## 4. Required outputs for the later Substep 1 investigation

When separately initiated, the investigation must produce an uncommitted
report containing exactly:

1. **One D2 determination:**
   - **D2 supported** — documentation shows the committed layout assumption is
     wrong or incomplete **and** an alternative stable 2005–2022 layout is
     identifiable; or
   - **D2 ruled out** — documentation shows the committed layout assumption is
     consistent with the published GDELT 1.0 layout for 2005–2022; or
   - **D2 unresolved** — documentation is insufficient/ambiguous to decide.
2. **Evidence table** with columns:
   - committed Lane 2 layout assumption,
   - documentation statement (quoted/cited),
   - implication for 2005–2022 coverage,
   - implication for the 2013-04-01 regime boundary,
   - implication for the consumed F4-missing result.
3. **Explicit statement** of whether **Phase B Substep 2** (a single live
   index-metadata read) is still needed, and if so the precise question it
   would answer (the D1-vs-D3 disambiguation carried over from the Phase A
   report).
4. **Explicit statement** that the report authorizes **no** rerun, **no** code
   patch, **no** live index read, **no** source pivot, and **no** Step 2.
5. **Canonical-preservation confirmation** that the consumed F4 outputs
   (`results/lane2_gdelt1_count_feasibility/20260518T163302Z/`) remain
   untouched and non-overwritten.

## 5. Preservation clause

The consumed F4 run record
(`results/lane2_gdelt1_count_feasibility/20260518T163302Z/`) is **canonical**.
Substep 1 treats it strictly read-only; it must never be modified, moved,
deleted, regenerated, or overwritten. Any future run writes to a new
timestamped directory and leaves this one intact (diagnostic memo §8).

## 6. Authorizes-no-further-step clause

Nothing in this memo, and nothing the Substep 1 investigation produces,
authorizes any count-only feasibility run, any event-archive contact, any
live index-metadata read (Substep 2), any parser/layout remediation patch, or
any source pivot. A "D2 supported" finding *describes* a possible
revised-layout-memo + patch path; it does **not** authorize one. All such
steps remain gated by diagnostic memo `5e0ed4b` §7 and/or separate explicit
micro-authorizations (Substep 2 in particular requires its own memo).

## 7. Stop condition

This memo does not fetch documentation, browse, contact GDELT, inspect the
live event archive or its index, request or download any event file, rerun the
feasibility check, implement or change any code, run any test, modify the
consumed F4 outputs, or pivot the source. It authorizes — only once committed
and only then — the bounded read-only documentation investigation defined in
§3a, to produce the §4 outputs. The Substep 1 investigation is **not**
initiated until this memo is committed and a separate explicit go-ahead is
given.

— end of Phase B Substep 1 documentation-fetch authorization memo (draft v0.1) —
