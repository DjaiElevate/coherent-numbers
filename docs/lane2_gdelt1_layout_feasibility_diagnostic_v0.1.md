# Lane 2 — GDELT 1.0 Layout-Feasibility Diagnostic Memo

**Version:** v0.1 (diagnostic-gate memo; not a rerun authorization)
**Date:** 2026-05-18
**Project:** Coherent Numbers — Lane 2 (separate from the Atlas lane)
**Status:** Draft for review. Not committed. Authorizes nothing. Defines a
diagnostic gate only. Does **not** authorize any GDELT contact, any retrieval,
any count-only rerun, or any source pivot.

**Governing / source context (committed):**
- Count-only feasibility protocol — `147c0d40568636ba0cf24ca00cc39c330e77ea03` (**binding**)
- Source-selection + count-feasibility authorization — `8fef80db0e103d2c22e36d589fe041abd1fb4c78`
- Run-authorization memo — `60ec1521106e6a980f6450cb21a1ef510b4c37d5`
- Retrieval-wiring path — `9528fe51519211af17206538ed1bb5b2f9a299ec`
- Run-enablement (consumed) — `fe742555cd240150d17dd1ea255453993e34d239`
- Inert-restore safety reset — `9e329c2a80e43f17eead7836729c719b444f2823`

---

## 1. Status

- Diagnostic-gate memo only.
- No data accessed in drafting.
- No GDELT contacted in drafting.
- No API called in drafting.
- No market data loaded.
- No 2023+ touched, referenced, sampled, counted, or consumed.
- No Step 2 lock drafted.
- No count-only rerun.
- No source pivot.
- The single authorized count-only feasibility run is **consumed** and is
  **not** re-authorized by this memo.

This memo defines *what may be safely inspected* to classify the cause of the
F4-missing result, the diagnostic class vocabulary, the decision rule, and the
re-authorization requirements that any future run would still face. It does
not itself investigate, conclude, or run anything.

## 2. Canonical consumed F4 result (frozen, non-overwritten)

The one authorized count-only feasibility run executed exactly once under
run-enablement commit `fe742555` and terminated at **F4** before any GDELT
file download or count computation. Its outputs are **canonical and must not
be modified, moved, deleted, regenerated, or overwritten**:

- Run output directory: `results/lane2_gdelt1_count_feasibility/20260518T163302Z/`
  - `count_feasibility_metadata.json`
  - `feasibility_summary.md`
- `feasibility_class = "F4"`
- `archive_layout_status = "missing"`
- `layout_report`: `files_missing = 3650`, `files_available = 0`,
  `files_in_archive_not_planned = 0`, `files_unexpected_naming = 0`,
  `files_date_unit_mismatch = 0`, `pre_2013_regime_coverage = 88`,
  `post_2013_daily_coverage = 3562`, `boundary_2013_04_01_handled = true`,
  `actual_layout_differs_from_documented = true`
- `stopped_before_count_computation = true`;
  `by_year_counts_status = "not_computed"`;
  `regime_boundary_status = "not_evaluated"`
- No `raw/` directory was created; zero GDELT event files were downloaded,
  queried, sampled, counted, stored, or inspected.

**Mechanistic record (count-only, no hypothesis content):** the authorized
retrieval path's first step (`fetch_archive_index`) contacted the GDELT 1.0
base index URL once via the injected real opener; the response yielded **zero
parseable available unit keys**, so all 3,650 planned pre-2023 units were
classified `missing` and the orchestrator routed to F4 and returned before the
download loop. This memo treats that mechanism as an observation to be
diagnosed, **not** as a conclusion.

F4 is a coverage/layout-feasibility result. Per the binding protocol it is
**not** evidence for or against the Lane 2 hypothesis, and it does **not**
authorize patch-and-rerun.

## 3. Purpose

Classify which of the following the F4-missing result reflects:

- **A.** Environment / index-access issue (the index endpoint was
  unreachable, blocked, empty, or returned non-listing content in the run
  environment).
- **B.** Documented GDELT 1.0 archive-layout mismatch (the real archive
  exposes files under a different path / filename / regime convention than the
  documented-overridable templates in the wiring).
- **C.** Parser / layout-discovery bug (the index *was* retrievable but
  `fetch_archive_index` / `verify_archive_layout` failed to recognize valid
  entries).
- **D.** Source not suitable for 2005–2022 count-only feasibility (the
  GDELT 1.0 Event archive does not provide the assumed coverage at all).
- **E.** Unresolved substrate ambiguity (evidence within the §5
  safe-inspection envelope, classified per §6, cannot distinguish A–D).

This is a **new diagnostic gate**, not a rerun authorization.

## 4. Scope and prohibitions

**Prohibited under this memo (hard):**
- No GDELT event-file download.
- No count-only feasibility rerun (no execution of the runner with guards
  satisfied; the inert-restore at `9e329c2` stands).
- No contact with GDELT endpoints for *event data*.
- No market data; no returns / CAR / abnormal returns / volatility / VIX /
  any market outcome; no model fits; no p-values; no feature importance; no
  attention-response or state-response relationships.
- No Step 2 lock; no hypothesis verdicts.
- No 2023+ resource request, reference, sample, count, or inspection.
- No modification, relocation, deletion, or regeneration of the consumed F4
  run outputs (§2).
- No patch-and-rerun of the consumed run.
- No source pivot, normalization change, parameter change, threshold change,
  event-definition change, or output-allow-list change.
- `REAL_RETRIEVAL_ENABLED` stays False in source; `COUNT_FEASIBILITY_
  AUTHORIZED` stays False in the runner.

## 5. What may be safely inspected (read-only, no event retrieval)

The diagnostic may use **only** the following, and only outside any guarded
runner path:

1. **GDELT 1.0 public documentation pages** — to record the *documented*
   archive base path, filename templates, regime boundary (pre/post
   2013-04-01), and sub-granularity conventions, as text references. Capturing
   documentation is not event retrieval; it must not fetch, parse, or store
   any event data file.
2. **Archive index / listing metadata** — at most a single, explicitly
   human-authorized read of the directory-index page (the same base index the
   consumed run contacted), treated as *layout metadata only*. This is
   permitted only if separately and explicitly authorized at execution time;
   this memo does **not** itself authorize it. No event `.zip`/`.CSV` file may
   be opened. Any 2023+ entry is ignored and never recorded.
3. **URL-pattern examples** — documented example URLs/filenames quoted from
   GDELT documentation, compared on paper to the wiring's
   `DEFAULT_GDELT1_BASE_URL` and `DEFAULT_GDELT1_FILENAME_TEMPLATES`.
4. **Synthetic / parser tests** — offline unit tests with fabricated index
   text and fabricated filename listings (no network), to determine whether
   `fetch_archive_index` / `verify_archive_layout` correctly recognize a
   *known-good synthetic* GDELT 1.0 listing and correctly reject 2023+.
5. **The consumed F4 metadata** — read-only inspection of the existing
   `count_feasibility_metadata.json` / `layout_report` (no modification).

Everything else is out of scope for this gate.

## 6. Diagnostic classes

Exactly one diagnostic class is to be assigned by the (separately authorized)
investigation that this memo gates. For each class: **(1) supporting
evidence**, **(2) ruling-out evidence**, **(3) re-authorization disposition**.
All §4 prohibitions hold throughout: no GDELT contact, no index-read
authorization (this memo grants none), no event-file download, no count-only
rerun, no remediation/patch or production-code change (offline read-only
synthetic parser tests per §5.4 are the only code execution permitted, and
only within the separately authorized investigation), no market data, no
2023+, no Step 2, no source pivot.
None of D0–D4 *by itself* authorizes any run; every future run still requires
the full fresh chain in §7. D5 overrides every other class.

### D0 — Investigation cannot resolve the ambiguity
- **(1) Supports:** the §5 inspections actually performable in scope are
  insufficient to distinguish D1/D2/D3/D4 (e.g. documentation inaccessible
  *and* no index-metadata read authorized *and* synthetic parser tests alone
  cannot adjudicate between a real-listing recognition failure and an
  empty-response environment).
- **(2) Rules out:** any single §5 inspection cleanly satisfies a D1, D2, D3,
  or D4 supporting criterion below ⇒ that class instead of D0.
- **(3) Disposition:** **unresolved.** Remain at the canonical consumed F4. No
  parser patch, no layout memo, no run authorization, no source rejection. A
  new decision (possibly authorizing a single index-metadata read, or an
  independent-environment access check) is required to leave D0.

### D1 — Parser / layout-discovery bug
- **(1) Supports:** evidence that the archive/index **exposes valid 2005–2022
  GDELT 1.0 units** (established via documentation example URLs/filenames
  and/or a *synthetic* reconstruction of a known-good GDELT 1.0 listing) **but
  Lane 2 code fails to recognize them** — i.e. offline tests feeding a
  known-good synthetic listing to `fetch_archive_index` /
  `verify_archive_layout` reproduce `files_available = 0` (or systematic
  non-recognition) with no 2023+ involvement.
- **(2) Rules out:** synthetic known-good listings *are* correctly parsed and
  mapped to planned unit keys in offline tests (defect not in the parser); or
  the documented layout itself cannot be shown to expose valid units (points
  to D2/D4); or the only failure observed is an empty/blocked transport
  response with no listing to parse (points to D3).
- **(3) Disposition:** **may justify a parser patch** (separately reviewed,
  no rerun authority on its own) **followed by a fresh run-authorization
  chain (§7)**. Does not, by itself, reject the source.

### D2 — Documented archive-layout mismatch
- **(1) Supports:** evidence that the documentation/template assumption
  (`DEFAULT_GDELT1_BASE_URL` / `DEFAULT_GDELT1_FILENAME_TEMPLATES` / regime
  split) is **wrong or incomplete**, **and** an **alternative stable archive
  layout for 2005–2022 can be identified** from documentation/URL-pattern
  examples, such that a correct listing under the alternative layout *would*
  map to the planned units.
- **(2) Rules out:** the documented layout matches example URLs/filenames and
  a synthetic listing built to it parses correctly (points to D1 or D3); or no
  alternative stable 2005–2022 layout can be identified at all (points to D4);
  or the failure is purely transport-empty (points to D3).
- **(3) Disposition:** **may justify a revised layout memo + implementation
  patch (separately reviewed) + a fresh run-authorization chain (§7)**. Does
  not, by itself, reject the source or authorize a run.

### D3 — Endpoint / environment / index-access issue
- **(1) Supports:** evidence that the expected archive **may exist** (the
  documented layout is internally consistent and a synthetic listing parses
  correctly) **but the index read in this environment returned empty /
  blocked / incomplete / non-listing content** — consistent with the consumed
  signature `files_available = 0` **and** `files_in_archive_not_planned = 0`
  **and** `files_unexpected_naming = 0` **and** `files_date_unit_mismatch =
  0` (an empty/blocked-transport signature, *not* a divergent-listing
  signature).
- **(2) Rules out:** a listing *was* obtained but its entries diverge from the
  documented layout (points to D2) or are valid yet unrecognized by the parser
  (points to D1); or documentation shows the source does not provide 2005–2022
  at all (points to D4).
- **(3) Disposition:** **does NOT automatically justify a parser patch.** It
  points to **independent access verification** (e.g. a network-capable,
  explicitly authorized environment under a new memo) **or, if access cannot
  be established, toward source rejection**. No code change is warranted from
  D3 alone; any future run still requires the full §7 chain *and* a
  demonstrably access-capable environment.

### D4 — GDELT 1.0 unsuitable for the Lane 2 2005–2022 count-only substrate
- **(1) Supports:** documentation/URL-pattern evidence that the GDELT 1.0
  Event archive does **not** provide the assumed 2005–2022 coverage in any
  stable documented form (no identifiable layout yields the required pre-2023
  units), independent of parser and environment.
- **(2) Rules out:** any identifiable stable 2005–2022 layout exists (points
  to D2), or the parser/environment is the only failing element (points to
  D1/D3).
- **(3) Disposition:** **points to source rejection / pivot discussion.** This
  is a separate decision **out of scope of this memo** — D4 records the
  finding only; it neither performs nor authorizes a pivot, and authorizes no
  run.

### D5 — Protocol breach (overrides all other classes)
- **(1) Supports:** any 2023+ contact/reference/sample/count/inspection; any
  prohibited computation (returns/CAR/outcomes/models/p-values/etc.); any
  modification, relocation, deletion, or regeneration of the consumed F4
  outputs; any event-file download; any rerun; any out-of-scope action during
  the diagnostic.
- **(2) Rules out:** strictly only the §5 safe inspections were performed and
  none of the above occurred.
- **(3) Disposition:** **halt immediately; escalate to human review.** D5
  overrides D0–D4. No remediation, patch, memo, or run authorization may be
  derived from a breach-tainted investigation.

**Class → purpose mapping:** D3→A, D2→B, D1→C, D4→D, D0→E, D5→breach
(overrides).

**Consolidated disposition rule:** D1 → parser patch (new review) → fresh §7
chain. D2 → revised layout memo + patch (new review) → fresh §7 chain. D3 →
independent access verification or source rejection; no parser patch from D3
alone. D4 → source rejection / pivot is a separate out-of-scope decision. D0 →
unresolved; remain at consumed F4 pending a new decision. D5 → halt + human
review. No class authorizes a run; §7 is mandatory and unchanged.

**Preliminary signature note (non-binding, to be tested, not concluded):** the
consumed `layout_report` shows zero available, zero unexpected, zero naming,
and zero date-unit mismatches. A genuine documented-layout mismatch (D2) or a
partial parser failure (D1) would typically leave *some* unexpected/naming/
date-unit residue; an all-missing / all-zero-residue signature is more
consistent with an empty or non-listing index response (D3). This is recorded
as a hypothesis for the §6 diagnostic to confirm or refute under the §5
envelope — it is **not** a verdict and confers no rerun authority.

## 7. Re-authorization requirements (unchanged and reaffirmed)

Regardless of diagnostic class, **no count-only feasibility run may occur
again** without a complete, fresh authorization chain:

1. A **new run-authorization memo** (the consumed `60ec1521` authorized
   exactly one run, now spent), explicitly addressing the diagnostic finding
   and any code/template/environment remediation.
2. A **separate run-enablement commit** flipping `COUNT_FEASIBILITY_
   AUTHORIZED = True` (the prior one, `fe742555`, is consumed).
3. The three runtime guards (code constant, `--authorize-count-feasibility-
   run`, `LANE2_COUNT_FEASIBILITY_AUTHORIZED=1`).
4. A **separate inert-restore safety commit** after that run (mirroring
   `9e329c2`).
5. A fresh timestamped output directory; the consumed
   `20260518T163302Z` directory is never reused or overwritten.

Any code patch arising from D1, or any template/documentation correction
arising from D2, is itself a separately reviewed change and **does not** carry
rerun authority.

## 8. Preservation clause

The consumed F4 run record (`results/lane2_gdelt1_count_feasibility/
20260518T163302Z/`) is **canonical**. It is read-only for all diagnostic
purposes, must remain uncommitted-or-committed exactly as the human directs,
and must never be modified, moved, deleted, or regenerated by the diagnostic.
Any future run writes to a new directory and leaves this one intact.

## 9. Stop condition

This memo does not contact GDELT, request any 2023+ resource, download or
query any event file, run retrieval, rerun the feasibility check, modify the
consumed F4 outputs, implement code, or pivot the source. It defines a
diagnostic gate, a safe inspection envelope, a D0–D5 vocabulary, the
class→purpose mapping, the disposition rule, and the unchanged re-
authorization requirements. The diagnostic investigation it gates is itself
**not** authorized until this memo is reviewed and a separate explicit
go-ahead (including, if needed, an explicit single index-metadata read
authorization) is given.

— end of layout-feasibility diagnostic memo (draft v0.1) —
