# Lane 2 / Type-Tone-Goldstein — Phase-2 pre-contact real-run hardening report v0.1

`HARDENING IMPLEMENTED (SYNTHETIC-PROVEN); SOURCE GATE REMAINS DISABLED; NO REAL NETWORK CONTACT; NO OFFICIAL MANIFESTS FETCHED; NO GDELT ZIPS DOWNLOADED; NO BOUNDED/FULL BUILD RAN; EXTRACTION STILL BLOCKED; NO PUSH`

This report records defense-in-depth hardening of the Phase-2 fetch/archive-build
path: a belt-and-suspenders `_open_url` source gate, official `md5sums`/`filesizes`
integrity-manifest parsing + verification, raw-cache integrity verification,
retry-stability checking, and an exact 58-column real-byte layout validator — all
implemented and proven on synthetic/local fixture bytes only. It authorizes **no**
real GDELT network contact, **no** manifest fetch, **no** zip download, **no**
bounded or full archive build, **no** TTG extraction/feature/statistic, **no**
join/outcome/market/V1/V2/2023+ access. The committed source gate remains `False`.

## 1. Preflight state

```
HEAD                       805122d
HEAD^                      cd29b72
origin/main                fb26424
origin/main...HEAD (L/R)   0   8   (local ahead by 8; no push)
status --short             two pre-existing untracked docs only:
  ?? docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md
  ?? docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md
```

Matched expected state. Proceeded.

## 2. Governing artifacts read

- `docs/lane2_type_tone_goldstein_local_approved_fields_archive_design_memo_v0.1.md` — five approved fields, forbidden set, network-as-separate-boundary, value-blind rule, separate-authorization sequencing.
- `docs/lane2_gdelt1_event_codebook_reference_v0.1.md` (content SHA-256 `3c5fa5bc…`) — V1.03 indices (SQLDATE 1, QuadClass 29, GoldsteinScale 30, NumMentions 31, AvgTone 34; DATEADDED 56 / SOURCEURL 57 forbidden) and the **58-field** daily layout (§5/§7).
- `docs/lane2_type_tone_goldstein_availability_timing_amendment_v0.1.md` — `file_date <= SQLDATE + 1` eligibility, fully-covered-window rule, DATEADDED forbidden as instrument/field, five-field schema, value-blind reporting.
- `docs/lane2_type_tone_goldstein_local_archive_phase1_conformance_report_v0.1.md` — Phase-1 by-construction network boundary; Phase-2 needs a reviewed code change.
- `docs/lane2_type_tone_goldstein_phase2_archive_fetch_path_gate_report_v0.1.md` — the Phase-2 fetch-path gate this dispatch hardens.
- `src/lane2_type_tone_goldstein_archive_fetch_path.py`, `src/lane2_type_tone_goldstein_local_archive.py`, `tests/test_lane2_type_tone_goldstein_fetch_path.py`, `tests/test_lane2_type_tone_goldstein_local_archive.py`.

### Governing constraints extracted
Five approved fields only; never compute over the four substantive fields; source gate is edit-only and not runtime-flippable; eligibility `F <= SQLDATE+1` (single +1); window `2013-04-01…2022-12-31`; 2023+ sealed; pre-window never read; daily layout is exactly 58 columns; build output structural/provenance only; DATEADDED never an availability instrument or retained field; file-download URL ≠ row-level SOURCEURL.

## 3. Source-gate hardening summary

A belt-and-suspenders gate check was added as the **first statement of `_open_url`**:
```
if not REAL_FETCH_SOURCE_GATE_ENABLED:
    raise RealFetchNotAuthorized(REAL_FETCH_BLOCK_MESSAGE + " [_open_url defense-in-depth gate]")
import urllib.request  # lazy: only after the source gate passes
```
This runs **before** the lazy `urllib` import and **before** any socket open, so even a direct call to `_open_url` (bypassing `fetch_one_source_file`) cannot import a network library or open a connection while the gate is `False`. The pre-existing higher-level gate in `fetch_one_source_file` is unchanged; this is additional, not a replacement.

## 4. Confirmation: source gate remains disabled
`REAL_FETCH_SOURCE_GATE_ENABLED = False` — a single source literal (one assignment, line 51), unchanged by this dispatch. Verified by scan and by `test_source_gate_remains_disabled_in_committed_code`.

## 5. Confirmation: `_open_url` gated before network import/open
`_open_url` (def L138) checks the gate at L156 **before** `import urllib.request` (L161) and before `opener.open(...)`. Proven by `test_open_url_itself_gated_before_urllib_import` (direct call hard-errors; injected opener spy records zero calls; source-order assertion confirms the gate precedes the import).

## 6. Confirmation: enablement is source-edit-only, not runtime-flippable
The gate is a bare module literal, never read from env/CLI/config/settings/parameter. Setting `REAL_FETCH_SOURCE_GATE_ENABLED`/`ENABLE_REAL_FETCH` env vars does not flip it (`test_open_url_gate_not_runtime_flippable`, `test_gate_not_reachable_via_runtime_config`). Enabling real fetch requires a reviewed edit of the source line plus a separate execution authorization.

## 7. Official `md5sums` / `filesizes` parsing and verification design

Implemented in the fetch module (synthetic/local bytes only here):
- `GDELT1_MD5SUMS_URL` / `GDELT1_FILESIZES_URL` are **defined** as provenance constants; **never opened** in this dispatch.
- `parse_md5sums(text) -> {filename: md5hex}` and `parse_filesizes(text) -> {filename: int}` — token-order-tolerant, retain only daily `*.export.CSV.zip` entries; filenames + hex/integer tokens only (value-blind).
- `expected_source_filenames(dates)` builds the deterministic expected bounded universe.
- `reconcile_universe_against_manifests(expected, md5map, sizemap)` — **fails closed** (`IntegrityManifestError`) if any expected file is missing from md5sums or filesizes; returns a value-agnostic reconciliation status otherwise.
- `verify_file_integrity(filename, file_bytes, md5map, sizemap)` — **fails closed** on a missing entry (`IntegrityManifestError`), MD5 mismatch, or byte-size mismatch (`IntegrityVerificationError`); records SHA-256 as **additional local provenance** (not a substitute for official MD5/size).
- `fetch_stable(date, fetch_callable, attempts>=2)` — retried download must return byte-identical results; otherwise **fails closed** (`UnstableDownloadError`).
- `manifest_provenance(md5sums_bytes, filesizes_bytes)` records SHA-256 + byte size of supplied manifest bytes.
- Authority model: official MD5 + byte size are authoritative; SHA-256 is local provenance only.

## 8. Confirmation: no official manifests were fetched
No request to `md5sums`, `filesizes`, or any GDELT endpoint occurred. All parsing/verification ran on synthetic fixture bytes built inside tests. The URL constants are defined but never opened.

## 9. Raw-cache verification design
- Real runs will cache raw zips under the gitignored `data/raw/lane2_ttg_gdelt1_event_zip_cache` tree (`RAW_CACHE_DIR`); this dispatch creates nothing there.
- `verify_cached_zip(cache_path, filename, md5map, sizemap)` reads the local cached bytes and re-runs `verify_file_integrity` **before use**. Cache presence **never** bypasses official integrity. On failure it **fails closed** (`CacheIntegrityError`); re-download requires a separate future authorization and is not performed here. Returns a value-agnostic status (cache path, byte size, MD5, SHA-256, integrity status).

## 10. Confirmation: no real cache was created from network
No cache directory was created and no zip was written from any network source. Synthetic cache tests wrote fixture bytes only under pytest `tmp_path`. No existing `data/raw/` was read or attached.

## 11. Exact 58-column validation design
- `EXPECTED_DAILY_COLUMN_COUNT = 58` (from the committed codebook/header reference, §5/§7).
- `is_exact_daily_layout(n)` and `exact_daily_layout_status(line)` provide a structural exact-count check, **distinct** from the approved-index short-row guard (`_MAX_APPROVED_INDEX = 34`).
- `classify_payload_rows(..., enforce_exact_columns=...)`: when enforced (the real build orchestration passes `True`), any row not exactly 58 columns is dropped via the closed reason `column_count_mismatch` **before** approved-field extraction. A 45-column row that contains the max approved index — which slips past the short-row guard — fails the exact-58 guard. Columns are never inferred, shifted, repaired, or reinterpreted from values. Proven by `test_exact_58_layout_passes`, `test_wrong_width_rows_fail_exact_layout[35/45/59]`, and `test_exact_layout_enforced_in_classify_distinct_from_short_guard`.

## 12. Synthetic tests run and results

```
python3 -m pytest -q \
  tests/test_lane2_type_tone_goldstein_local_archive.py \
  tests/test_lane2_type_tone_goldstein_fetch_path.py
................................................................         [100%]
64 passed in 0.22s
```

Broader regression (no collateral breakage):

```
python3 -m pytest -q tests/ -k "lane2"
609 passed, 596 deselected in 54.14s
```

Environment: Python 3.8.2, pytest 8.3.5. §8 requirement → test map:
1 `test_open_url_itself_gated_before_urllib_import`;
2 `test_open_url_gate_not_runtime_flippable` (+ `test_gate_not_reachable_via_runtime_config`);
3 `test_source_gate_remains_disabled_in_committed_code`;
4/12 `test_universe_reconciliation_ok_and_required`;
5 `test_missing_md5sums_entry_fails_closed`;
6 `test_missing_filesizes_entry_fails_closed`;
7 `test_md5_mismatch_fails_closed`;
8 `test_byte_size_mismatch_fails_closed`;
9 `test_unstable_retry_fails_closed` (+ `test_stable_retry_returns_bytes`);
10 `test_cached_zip_reverified_before_use`;
11 `test_cache_is_not_a_bypass_around_integrity`;
13 `test_exact_58_layout_passes`;
14/15/16 `test_wrong_width_rows_fail_exact_layout[35/45/59]` + `test_exact_layout_enforced_in_classify_distinct_from_short_guard`;
17/18 `test_integrity_status_value_agnostic`;
19 `test_no_2023plus_enumeration_or_open_path`;
20 `test_no_real_network_contact_possible_in_tests`;
slice-aware (§10) `test_slice_aware_coverage_for_bounded_april_2013`.

## 13. Confirmation: no real network contact occurred
No socket was opened, no URL fetched. `urllib` is imported only lazily inside `_open_url`, which is gated; with the shipped gate `False` it is never reached. All tests inject synthetic fetchers or hit the gate (`test_no_real_network_contact_possible_in_tests`).

## 14. Confirmation: no GDELT files downloaded; no bounded/full build ran
No daily `*.export.CSV.zip` was downloaded; no bounded real-slice build and no full-window build ran. The only orchestration exercised (`run_phase2_archive_build`) ran against injected synthetic payloads, writing only under pytest `tmp_path`.

## 15. Confirmation: no extraction/join/outcome/market/V1/V2/2023+; no governing-doc edits
No TTG feature/statistic/value-summary/sample-row was computed; no join, outcome read, market read, V1/V2, or 2023+ contact occurred. No outcome/join-gate governing doc was edited (their SHA pins remain asserted by `test_outcome_join_gate_docs_unmodified`). Integrity/report outputs are value-agnostic (`test_integrity_status_value_agnostic`); no logic branches on `quadclass`/`goldsteinscale`/`nummentions`/`avgtone` values.

## 16. Future bounded-run requirement (report only — not run here)
For a future bounded slice such as `2013-04-01…2013-04-30`, **slice-aware** coverage must be enforced: a SQLDATE is build-complete only if all eligible contributing source-file dates `{t-1, t, t+1}` are inside the fetched source-file set (and in-window). For a `2013-04-01…2013-04-30` fetched set:
- `2013-04-01` is start-edge incomplete (needs pre-window `2013-03-31`, not fetched);
- `2013-04-30` must be routed as slice-edge incomplete unless `2013-05-01` is explicitly inside the fetched set;
- fully covered smoke-test SQLDATEs are `2013-04-02…2013-04-29`.
`2013-05-01` is **not** fetched in this dispatch. The structural helper `fetched_set_fully_covers(sqldate, fetched_dates)` encodes this and is synthetic-tested (`test_slice_aware_coverage_for_bounded_april_2013`); no bounded slice was executed.

## 17. Changed paths
- `src/lane2_type_tone_goldstein_local_archive.py` (modified — `md5_hex`, exact-58 constant/helpers, `column_count_mismatch` reason, `enforce_exact_columns` param, slice-aware coverage helper)
- `src/lane2_type_tone_goldstein_archive_fetch_path.py` (modified — `_open_url` defense-in-depth gate, integrity-manifest/cache/retry logic, exact-58 threading)
- `tests/test_lane2_type_tone_goldstein_fetch_path.py` (modified — hardening test suite)
- `docs/lane2_type_tone_goldstein_phase2_precontact_real_run_hardening_report_v0.1.md` (new — this report)

No generated/cache outputs under `data/raw/`, `archive/`, or `results/` were created or staged.

## 18. Remaining blocked work
- **Real GDELT network contact / manifest fetch / zip download** — blocked; require editing the source gate **and** a separate execution authorization after byte review of this commit.
- **Bounded real-slice build** — separately unauthorized.
- **Full-window archive build** — separately unauthorized.
- **TTG extraction** — still BLOCKED; requires a locked estimator-and-evaluation pre-registration before any value-level read.
- **Predictor-vs-outcome alignment seam** — still open (extraction-gate question).
- **Outcome-side join** — still blocked.
- **No push** performed.
