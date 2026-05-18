# Lane 2 — GDELT 1.0 Layout-Diagnostic Investigation Authorization (Phase A)

**Version:** v0.1 (Phase A authorization memo; offline diagnostics only)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Authorizes — once committed — a
**narrow, offline-only Phase A diagnostic investigation** under the committed
diagnostic memo `5e0ed4b`. Authorizes nothing else. Authorizes no GDELT
contact, no live index read, no retrieval, no rerun, no code remediation, no
source pivot.

**Governing / source context (committed):**
- Count-only feasibility protocol — `147c0d40568636ba0cf24ca00cc39c330e77ea03` (**binding**)
- Source-selection + count-feasibility authorization — `8fef80db0e103d2c22e36d589fe041abd1fb4c78`
- Run-authorization memo (consumed) — `60ec1521106e6a980f6450cb21a1ef510b4c37d5`
- Retrieval-wiring path — `9528fe51519211af17206538ed1bb5b2f9a299ec`
- Run-enablement (consumed) — `fe742555cd240150d17dd1ea255453993e34d239`
- Inert-restore safety reset — `9e329c2a80e43f17eead7836729c719b444f2823`
- Layout-feasibility diagnostic memo (**binding for this investigation**) —
  `5e0ed4bd70658767c74654db20d748794a237548`

---

## 1. Status

- Phase A authorization memo only. Authorizes a bounded offline investigation;
  it is not the investigation and produces no diagnostic finding itself.
- No data accessed in drafting. No GDELT contacted. No API called. No tests
  run. No code implemented. No market data. No 2023+ touched/referenced/
  sampled/counted/consumed. No Step 2. No source pivot.
- The single authorized count-only feasibility run remains **consumed**
  (`60ec1521` / `fe742555` spent); this memo does **not** re-authorize it.
- This memo is subordinate to and bounded by diagnostic memo `5e0ed4b`
  (its §4 prohibitions, §5 inspection envelope, §6 D0–D5 vocabulary, §7
  re-authorization requirements, §8 preservation clause).

## 2. Purpose

Authorize **Phase A only**: an offline, read-only diagnostic to provisionally
classify the consumed F4-missing result into exactly one of the diagnostic
memo's classes (D0–D5), with explicit D1-vs-D2-vs-D3 disambiguation, and to
determine whether Phase A alone is sufficient or whether a separate **Phase B
live index-metadata micro-authorization** would be required.

This memo does **not** authorize Phase B. Phase B (a single, explicitly
human-authorized index-metadata read per diagnostic memo §5.2) remains
ungranted and requires its own separate micro-authorization.

## 3. What this memo does NOT authorize (hard prohibitions)

- No GDELT contact of any kind.
- No live index read / directory-listing fetch.
- No event-file request.
- No event-file download.
- No count-only feasibility rerun (the inert-restore `9e329c2` stands;
  `COUNT_FEASIBILITY_AUTHORIZED` stays False; `REAL_RETRIEVAL_ENABLED` stays
  False).
- No real opener, no `urllib`, no `requests`, no `socket`, no HTTP/HTTPS, no
  DNS, no network path of any kind.
- No market data; no returns / CAR / abnormal returns / volatility / VIX /
  any market outcome; no model fits; no p-values; no feature importance; no
  attention-response or state-response relationships.
- No 2023+ resource request, reference, sample, count, or inspection.
- No Step 2 draft; no hypothesis verdicts.
- No source pivot; no normalization / parameter / threshold / event-definition
  / output-allow-list change.
- No production-code remediation patch.
- No source/test/runner code changes. (Any remediation, or any new *tracked*
  test, requires a **separate explicit patch prompt** — it is out of scope
  here.)
- No modification, relocation, deletion, regeneration, or overwrite of the
  consumed F4 outputs.

## 4. Phase A allowed scope (offline, read-only)

Strictly the following, and only outside any guarded runner path:

1. **Read-only inspection of the consumed F4 outputs** —
   `results/lane2_gdelt1_count_feasibility/20260518T163302Z/`
   (`count_feasibility_metadata.json`, `feasibility_summary.md`). Read only;
   no modification, copy-back, or regeneration.
2. **Read-only inspection of committed Lane 2 artifacts** — `src/
   lane2_gdelt1_count_feasibility.py`, `scripts/run_lane2_gdelt1_count_
   feasibility.py`, `tests/test_lane2_gdelt1_count_feasibility.py`, and the
   committed Lane 2 memos (incl. `5e0ed4b`). Reading only.
3. **Offline synthetic parser/layout tests using fabricated listings only** —
   exercise the `fetch_archive_index` / `verify_archive_layout` code paths
   through **injected fake openers or in-memory fixtures only**. Permitted
   forms:
   - running the **existing committed** synthetic Lane 2 tests
     (`pytest tests/test_lane2_gdelt1_count_feasibility.py`), and
   - **ephemeral, uncommitted** in-memory exploration (e.g. a fake opener
     returning a fabricated known-good GDELT 1.0 directory listing) that is
     not written into any tracked source/test/runner file.
   No real opener, `urllib`, `requests`, `socket`, or network path may be
   constructed or called. No fabricated listing may contain a 2023+ entry;
   any such entry must abort per the existing seal guards.
4. **Documentation/URL-pattern reasoning on paper** — comparing the wiring's
   `DEFAULT_GDELT1_BASE_URL` / `DEFAULT_GDELT1_FILENAME_TEMPLATES` / regime
   split against documented GDELT 1.0 conventions *from already-known
   references*, without contacting GDELT. (No new documentation fetch is
   authorized here; if documentation retrieval is later deemed necessary it is
   a separate authorization.)

Anything not in this list is out of Phase A scope. Phase A authorizes **no
new documentation fetches** and **no live index read**.

### 4a. Phase A class-assignment limits (offline-only envelope)

Phase A may not be able to conclusively assign D2 or D3. Class assignment is
bounded as follows:

- **D1** — a Phase A D1 finding **may** be supported by offline synthetic
  parser/layout tests showing that valid 2005–2022 GDELT 1.0 unit patterns are
  **not recognized** by the Lane 2 parser/layout code (`fetch_archive_index` /
  `verify_archive_layout`) under fabricated known-good listings. This is the
  only class Phase A can affirmatively *confirm* within the offline envelope.
- **D2** — a Phase A D2 finding **may only** be assigned if **committed
  artifacts or already-known references already show** that the documented/
  template layout assumption is wrong or incomplete **and** that an
  alternative stable 2005–2022 layout is identifiable. Phase A may **not**
  fetch documentation to establish this.
- **D3** — a Phase A D3 finding **may only** be assigned as a **provisional
  access/index-consistency diagnosis** inferred from the consumed F4 signature
  and committed artifacts. Confirmation of D3 through live access **requires
  separate Phase B authorization**; Phase A cannot confirm D3.
- **D0 fallback** — if D2 or D3 cannot be resolved under the offline-only
  envelope, the correct Phase A output is **D0**, with an explicit
  recommendation for a **separately authorized Phase B**.
- **Phase B may be split** into separately authorized substeps — e.g. a
  read-only documentation fetch first, then **at most one** live
  index-metadata read only if still needed. Phase B and each of its substeps
  remain ungranted; none is authorized by this memo.

## 5. Required Phase A diagnostic outputs

The Phase A investigation (when separately initiated) must produce a
**diagnostic report** containing exactly:

1. **One provisional diagnostic class** — D0, D1, D2, D3, D4, or D5 (per
   diagnostic memo §6), labelled *provisional* and Phase-A-scoped. D5
   overrides all others.
2. **Explicit D1-vs-D2-vs-D3 evidence table** — a table with one row per
   class {D1, D2, D3} and columns:
   - *Supporting evidence found (Phase A)*,
   - *Ruling-out evidence found (Phase A)*,
   - *Provisional lean / undetermined*,
   - *Phase A sufficient to decide this class? (yes/no)*.
3. **Phase A sufficiency statement** — an explicit declaration, consistent
   with the §4a class-assignment limits, of whether Phase A is sufficient to
   assign a stable class, or whether a separate **Phase B** is required.
   Per §4a: D1 may be confirmed offline; D2 only if committed artifacts/
   already-known references already establish it; D3 only provisionally from
   the F4 signature + committed artifacts; if D2 or D3 is unresolved offline
   the output must be **D0** with a Phase B recommendation. The statement must
   name the precise question a Phase B substep (read-only documentation fetch,
   and/or at most one live index-metadata read per diagnostic memo §5.2) would
   answer.
4. **Canonical-preservation confirmation** — explicit confirmation that the
   consumed F4 result (`20260518T163302Z`) was inspected read-only and
   remains canonical, unmodified, non-overwritten.
5. **No-authorization confirmation** — explicit statement that the diagnostic
   report itself authorizes **no** future count-only run, no parser/layout
   remediation patch, no Phase B, and no source pivot; any such step requires
   the fresh chains in diagnostic memo §7 and/or a separate explicit
   authorization.

## 6. Preservation clause

The consumed F4 run record
(`results/lane2_gdelt1_count_feasibility/20260518T163302Z/`) is **canonical**.
Phase A treats it strictly read-only; it must never be modified, moved,
deleted, regenerated, or overwritten. Any future run writes to a new
timestamped directory and leaves this one intact (diagnostic memo §8).

## 7. Authorizes-no-future-run clause

Nothing in this memo, and nothing the Phase A investigation produces,
authorizes any count-only feasibility run, any retrieval, any Phase B live
index read, any parser/layout remediation patch, or any source pivot. All of
those remain gated by diagnostic memo `5e0ed4b` §7 (fresh run-authorization
memo + separate run-enablement commit + three guards + separate inert-restore
commit + new output directory) and/or a separate explicit micro-authorization.
A provisional D1/D2 finding *describes* a possible remediation path; it does
**not** authorize one.

## 8. Stop condition

This memo does not perform the investigation, run any test, inspect live
GDELT, contact any endpoint, request any 2023+ resource, download or query any
file, implement or change any code, rerun the feasibility check, modify the
consumed F4 outputs, or pivot the source. It authorizes — only once committed
and only then — the bounded offline Phase A diagnostic defined in §4, to
produce the §5 outputs. The Phase A investigation is **not** initiated until
this memo is committed and a separate explicit go-ahead to begin Phase A is
given.

— end of Phase A layout-diagnostic authorization memo (draft v0.1) —
