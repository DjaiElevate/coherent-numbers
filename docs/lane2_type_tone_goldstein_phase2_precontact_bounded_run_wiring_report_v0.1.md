# Lane 2 / Type-Tone-Goldstein — Phase-2 pre-contact bounded-run wiring report v0.1

`WIRED ORCHESTRATION IMPLEMENTED (SYNTHETIC-PROVEN); SOURCE GATE REMAINS DISABLED; NO REAL NETWORK CONTACT; NO MANIFESTS FETCHED; NO ZIPS DOWNLOADED; NO BOUNDED/FULL BUILD RAN; ONE REAL/DEFAULT FETCH ENTRYPOINT; NO BARE REAL-FETCH ORCHESTRATOR; EXTRACTION STILL BLOCKED; NO PUSH`

This report records the wiring of the already-reviewed integrity/cache/exact-58/
slice primitives into a single integrity-checked bounded-run orchestration entry-
point (`run_bounded_integrity_build`), and the closure of the two-orchestrator
footgun by neutering the bare `run_phase2_archive_build` so it can never reach the
real fetch. Everything is proven on synthetic/local fixture bytes and injected
non-network fetchers. The committed source gate remains `False`.

## 1. Preflight state

```
HEAD                       a953d4d
HEAD^                      805122d
origin/main                fb26424
origin/main...HEAD (L/R)   0   9   (local ahead by 9; no push)
status --short             two pre-existing untracked docs only:
  ?? docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md
  ?? docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md
```

Matched expected state. Proceeded.

## 2. Governing artifacts read

- `docs/lane2_type_tone_goldstein_local_approved_fields_archive_design_memo_v0.1.md`; `docs/lane2_gdelt1_event_codebook_reference_v0.1.md` (content SHA-256 `3c5fa5bc…`, 58-field daily layout); `docs/lane2_type_tone_goldstein_availability_timing_amendment_v0.1.md` (`file_date <= SQLDATE+1`; fully-covered-window rule); `docs/lane2_type_tone_goldstein_local_archive_phase1_conformance_report_v0.1.md`; `docs/lane2_type_tone_goldstein_phase2_archive_fetch_path_gate_report_v0.1.md`; `docs/lane2_type_tone_goldstein_phase2_precontact_real_run_hardening_report_v0.1.md`; both source modules and both test files.

### Governing constraints extracted
Five approved fields only; never compute over the four substantive fields; source gate edit-only and not runtime-flippable; eligibility `F <= SQLDATE+1`; window `2013-04-01…2022-12-31`; 2023+ sealed; pre-window never read; exact 58-column daily layout; value-blind structural-only output; DATEADDED never an availability instrument/retained field; file-download URL ≠ row-level SOURCEURL; each gate separately authorized.

### Confirmed from committed bytes before editing
- `REAL_FETCH_SOURCE_GATE_ENABLED = False` committed (single source literal).
- `_open_url` has its own gate before the lazy `urllib` import / network open.
- Official MD5/size integrity primitives exist (`parse_md5sums`, `parse_filesizes`, `reconcile_universe_against_manifests`, `verify_file_integrity`).
- Cache verification primitive exists (`verify_cached_zip`).
- Exact 58-column validation exists (`EXPECTED_DAILY_COLUMN_COUNT`, `is_exact_daily_layout`, `classify_payload_rows(enforce_exact_columns=...)`).
- Slice-aware `fetched_set_fully_covers` exists.
- The prior runnable orchestrator (`run_phase2_archive_build`) did NOT wire these together — it was a bare `fetch -> classify` path whose default fetcher was the real gated fetch (the two-orchestrator footgun). This dispatch closes that.

## 3. Confirmations
- **Source gate remains disabled:** `REAL_FETCH_SOURCE_GATE_ENABLED = False` (fetch module L51, single assignment; no `= True` anywhere).
- **No real network contact occurred;** **no official manifests fetched;** **no daily GDELT zips downloaded;** **no bounded real build ran;** **no full-window build ran.** All tests use synthetic manifest bytes, in-memory fixture payloads, injected non-network fetchers, and pytest temp cache dirs; the shipped gate keeps the real default inert.

## 4. Wired orchestration path

New entrypoint `run_bounded_integrity_build(start_date, end_date, out_dir, *, md5sums_bytes, filesizes_bytes, …)` in `src/lane2_type_tone_goldstein_archive_fetch_path.py` (def L628). Fixed order:

1. `assert_codebook_indices` — fail closed.
2. Three-guard run gate (`guards_satisfied`).
3. Build bounded universe from start/end and `enumerate_source_universe` → rejects any out-of-window or 2023+ date **before any fetch/open**.
4. `manifest_provenance` (SHA-256 + byte size of supplied manifest bytes) + `parse_md5sums` + `parse_filesizes`.
5. `reconcile_universe_against_manifests` (fail closed) — **before** any daily fetch.
6. Per source date: cache-check first → if present `verify_cached_zip` (official MD5/size, `CacheIntegrityError` on failure, no silent re-download); else `fetch_stable` (retry stability) → `verify_file_integrity` (official MD5/size; SHA-256 recorded as local provenance) → write verified bytes to cache (after verification only) → `classify_payload_rows(enforce_exact_columns=True, route_edge_incomplete=True)`.
7. Slice-aware coverage: re-filter classify survivors with `fetched_set_fully_covers` against the **actual fetched date set**; slice-edge SQLDATEs routed out of the primary archive.
8. Write approved-fields archive (primary, slice-covered rows only) + value-agnostic provenance manifest.

**Exact call order (manifest reconciliation → cache verify → stable fetch → integrity verify → cache write → exact-58 classify → slice-aware coverage):** reconcile L703 (once, up front); then per file `verify_cached_zip` L721 (cache branch) **or** `fetch_stable` L727 → `verify_file_integrity` L730 → cache write L733-737; then `classify_payload_rows(enforce_exact_columns=True)` L742/747; then slice-aware `fetched_set_fully_covers` L780 after the per-file loop.

## 5. Single real-network entrypoint design

The two-orchestrator footgun is closed:

- **`run_phase2_archive_build` is neutered to a synthetic/legacy harness** (def L184). It (a) raises `SyntheticOrchestratorViolation` if `fetch_callable is None` (no fall-back to the real fetch, L221) and (b) raises if the injected fetcher is one of the real-network entrypoints `{fetch_one_source_file, fetch_stable, _open_url}` (L227). It therefore **cannot reach `_open_url` for real bytes**.
- **`run_bounded_integrity_build` is the only orchestrator whose default per-file byte source is the real gated fetch** (via `fetch_stable` → `fetch_one_source_file` → `_open_url`, all behind the source gate), and it applies manifest reconciliation + official MD5/size verification + exact-58 + slice-aware coverage **unconditionally** around the fetch. An injected fetcher only supplies bytes; it cannot skip the integrity steps, because they run on whatever bytes are returned (proven by `test_wired_injected_fetcher_cannot_bypass_integrity`).
- **No bare real-fetch-capable orchestrator remains.** There is exactly one real/default fetch entrypoint for future real runs.

## 6. Integrity-manifest call path
`run_bounded_integrity_build` calls `manifest_provenance` (L702), `parse_md5sums`/`parse_filesizes` (L704-705), and `reconcile_universe_against_manifests` (L703) before any daily processing; per file it calls `verify_file_integrity` (L730). Confirmed actually called (not prose): see `/tmp/ttg_bounded_wiring_callsite_scan.txt`.

## 7. Cache call path
`verify_cached_zip` is called for cached files (L721); cache is checked before fetch; cache cannot bypass reconciliation (reconcile runs first, L703) or integrity (`verify_cached_zip` re-verifies official MD5/size); cache integrity failure raises `CacheIntegrityError` with no silent re-download. Verified bytes are written to cache only after `verify_file_integrity` succeeds (L733-737).

## 8. Stable-fetch call path
For uncached bytes, `fetch_stable` is called (L727) with the injected fetcher (default = real gated fetch); an unstable retry raises `UnstableDownloadError` before archive write.

## 9. Exact 58-column call path
`classify_payload_rows(..., enforce_exact_columns=True)` is called by the wired orchestrator (L742/747); 35/45/59-column rows fail closed via `column_count_mismatch` inside the run path, distinct from the `_MAX_APPROVED_INDEX` short-row guard (`test_wired_exact58_enforced_in_orchestration[35/45/59]`).

## 10. Slice-aware coverage call path
`fetched_set_fully_covers` is called by the wired orchestrator (L780) against the actual fetched date set. For a synthetic `2013-04-01…2013-04-30` bounded set: `2013-04-01` is routed out (window-edge: needs pre-window `2013-03-31`); `2013-04-30` is routed out (slice-edge: needs unfetched `2013-05-01`); primary covered SQLDATEs are exactly `2013-04-02…2013-04-29`; neither `2013-03-31` nor `2013-05-01` is fetched/opened (`test_wired_happy_path_slice_coverage`, `test_wired_no_out_of_slice_fetch`).

## 11. Value-blindness
The wired path branches only on filenames, dates, bytes, sizes, MD5/SHA hashes, cache/integrity status, and column counts. No `.mean/.sum/.median/groupby/value_counts/Counter/np/pd/quantile/corr/histogram`; no branch on `quadclass/goldsteinscale/nummentions/avgtone` values; approved fields are copied verbatim by the existing classify logic. Generated manifest is structural/provenance only — no value summaries, no sample rows, no value-conditioned buckets (`test_wired_manifest_structural_and_value_agnostic`).

## 12. Synthetic tests

```
python3 -m pytest -q \
  tests/test_lane2_type_tone_goldstein_local_archive.py \
  tests/test_lane2_type_tone_goldstein_fetch_path.py
86 passed in 0.34s
```

Broader regression:

```
python3 -m pytest -q tests/ -k "lane2"
631 passed, 596 deselected in 54.00s
```

Environment: Python 3.8.2, pytest 8.3.5. §10 requirement → wired test map (highlights):
1 `test_wired_source_gate_remains_disabled`;
2/9 `test_wired_reconciliation_before_fetch`, `test_wired_cache_cannot_bypass_reconciliation`;
3/4 `test_wired_missing_md5_entry_fails_closed`, `test_wired_missing_filesizes_entry_fails_closed`;
5/6 `test_wired_md5_mismatch_fails_closed`, `test_wired_size_mismatch_fails_closed`;
7 `test_wired_unstable_retry_fails_closed`;
8/11 `test_wired_all_from_verified_cache`, `test_wired_mixed_cache_and_fetch_records_provenance`;
10 `test_wired_cache_integrity_failure_no_silent_redownload`;
12-15 `test_wired_exact58_enforced_in_orchestration[35/45/59]`;
16-19 `test_wired_happy_path_slice_coverage`;
20 `test_wired_no_out_of_slice_fetch`;
21-23 `test_wired_manifest_structural_and_value_agnostic`;
24 `test_wired_no_2023plus_enumeration`;
25 `test_wired_default_fetch_is_real_gated`;
26/27 `test_bare_harness_refuses_default_and_real_fetch`, `test_bare_harness_synthetic_fetcher_never_opens_url`;
28 `test_wired_injected_fetcher_cannot_bypass_integrity`.

## 13. No-network confirmation
No socket/URL opened; `urllib` is imported only lazily inside the gated `_open_url`, never reached with the shipped gate. The wired path's default per-file source is the real gated fetch — proven to hard-error (`test_wired_default_fetch_is_real_gated`) — so no test performs real contact. No official manifests fetched, no daily zips downloaded, no real cache created from network, no bounded/full build ran.

## 14. Generated `/tmp` artifacts (evidence only; not committed)
- `/tmp/ttg_bounded_wiring_callsite_scan.txt` — call sites for the integrity/cache/exact-58/slice primitives, `_open_url`, and both orchestrators.
- `/tmp/ttg_bounded_wiring_source_gate_scan.txt` — gate `= False` present, no `= True`.

## 15. Changed paths
- `src/lane2_type_tone_goldstein_archive_fetch_path.py` (modified — `SyntheticOrchestratorViolation`, neutered `run_phase2_archive_build`, new wired `run_bounded_integrity_build`, `_date_range_inclusive`, `timedelta` import)
- `tests/test_lane2_type_tone_goldstein_fetch_path.py` (modified — 22 wired end-to-end tests)
- `docs/lane2_type_tone_goldstein_phase2_precontact_bounded_run_wiring_report_v0.1.md` (new — this report)

The archive module (`src/lane2_type_tone_goldstein_local_archive.py`) was **not** changed in this dispatch (its primitives sufficed). No generated/cache outputs under `data/raw/`, `archive/`, or `results/` were created or staged.

## 16. Remaining blocked work
- **Real GDELT network contact / manifest fetch / zip download** — blocked; require editing the source gate **and** a separate execution authorization after byte review of this commit, then connecting `run_bounded_integrity_build` to the real default.
- **Bounded real-slice build** — separately unauthorized.
- **Full-window archive build** — separately unauthorized.
- **TTG extraction** — still BLOCKED; requires a locked estimator-and-evaluation pre-registration before any value-level read.
- **Predictor-vs-outcome alignment seam** — still open (extraction-gate question).
- **Outcome-side join** — still blocked.
- **No push** performed.
