# Lane 2 / Type-Tone-Goldstein — Phase-2 pre-contact manifest-acquisition wiring report v0.1

`MANIFEST ACQUISITION WIRED THROUGH THE GATED _open_url (SYNTHETIC-PROVEN); SOURCE GATE REMAINS DISABLED; NO REAL NETWORK CONTACT; NO MANIFESTS FETCHED; NO ZIPS DOWNLOADED; NO BOUNDED/FULL BUILD RAN; SINGLE REAL/DEFAULT ENTRYPOINT; EXTRACTION STILL BLOCKED; NO PUSH`

This amendment closes the last no-network gap before bounded real contact: official
GDELT `md5sums` and `filesizes` acquisition is now routed through the **same
reviewed gated `_open_url`** path as daily zips, inside the single wired
orchestrator. Proven on synthetic/local fixtures only. The committed source gate
remains `False`.

## 1. Preflight state

```
HEAD                       68505a2
HEAD^                      a953d4d
origin/main                fb26424
origin/main...HEAD (L/R)   0   10   (local ahead by 10; no push)
status --short             two pre-existing untracked docs only:
  ?? docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md
  ?? docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md
```

Matched expected state. Proceeded.

## 2. Governing artifacts read

- `docs/lane2_type_tone_goldstein_phase2_archive_fetch_path_gate_report_v0.1.md`; `docs/lane2_type_tone_goldstein_phase2_precontact_real_run_hardening_report_v0.1.md`; `docs/lane2_type_tone_goldstein_phase2_precontact_bounded_run_wiring_report_v0.1.md`; `src/lane2_type_tone_goldstein_archive_fetch_path.py`; `src/lane2_type_tone_goldstein_local_archive.py`; `tests/test_lane2_type_tone_goldstein_fetch_path.py`.

### Governing constraints extracted
Five approved fields only; never compute over the four substantive fields; source gate edit-only, not runtime-flippable; eligibility `F <= SQLDATE+1`; window `2013-04-01…2022-12-31`; 2023+ sealed; pre-window never read; exact 58-column layout; value-blind structural-only output; single real/default fetch entrypoint; integrity/cache/exact-58/slice behaviour from `68505a2` must not be loosened.

### Confirmed from committed bytes before editing (at `68505a2`)
- `REAL_FETCH_SOURCE_GATE_ENABLED = False` committed (single source literal).
- `_open_url` has its own gate before the lazy `urllib` import / open.
- `run_bounded_integrity_build` wired daily zip bytes through integrity/cache/stable-fetch/exact-58/slice-aware coverage.
- `run_phase2_archive_build` neutered (refuses None/default and real-network entrypoints) — cannot reach `_open_url` for real bytes.
- Manifest acquisition was NOT yet wired into the real/default path; it required caller-supplied `md5sums_bytes` / `filesizes_bytes` (the gap this amendment closes).

## 3. Confirmations
- **Source gate remains disabled:** `REAL_FETCH_SOURCE_GATE_ENABLED = False` (fetch module L51, single source assignment; no `= True`).
- **No real network contact occurred;** **no official manifests fetched;** **no daily GDELT zips downloaded;** **no bounded real build ran;** **no full-window build ran.** All tests use synthetic manifest bytes / an injected manifest-fetch callable / in-memory daily payloads / pytest temp cache dirs; the shipped gate keeps the real default inert.

## 4. Manifest-acquisition wiring

New helper `fetch_manifest_bytes(url, *, manifest_fetch_callable=None)` (L176):
- DEFAULT (real) path: `return _open_url(url)` (L196) — the **same gated `_open_url`** used for daily zips. With the gate `False` it hard-errors before any `urllib` import or open.
- `manifest_fetch_callable(url) -> bytes` is a synthetic/test-only seam for in-memory manifest bytes.

`run_bounded_integrity_build` now takes `md5sums_bytes` / `filesizes_bytes` as **Optional** (default `None`) plus an optional `manifest_fetch_callable`. When manifest bytes are not supplied (future real/default mode), it acquires both manifests via `fetch_manifest_bytes(GDELT1_MD5SUMS_URL …)` / `(GDELT1_FILESIZES_URL …)` (L761/765) → the gated `_open_url`. A `manifest_source_mode` marker (`"gated_open_url_default"` vs `"synthetic_injected"`) is recorded in the structural manifest.

## 5. Manifest ordering

Inside `run_bounded_integrity_build`, the fixed order is:
1. `assert_codebook_indices` (L741).
2. three-guard run gate (L748-ish).
3. seam-mode guard (L754): in a gate-enabled session, any injected seam fails closed.
4. bounded universe + `enumerate_source_universe` (L747) — rejects out-of-window / 2023+ **before** any fetch.
5. **manifest acquisition** `fetch_manifest_bytes` (L761/765) — AFTER codebook/run-gate/window/2023+/enumeration.
6. `manifest_provenance` + `parse_md5sums` + `parse_filesizes` (L770-772).
7. `reconcile_universe_against_manifests` (L775) — before the daily loop.
8. per-file daily processing (L786+).

A failure at codebook/index, run gate, bounded window, 2023+ rejection, or enumeration raises **before** the manifest-acquisition line, so it can never reach the network for manifests. Proven by `test_codebook_failure_does_not_reach_manifest_acquisition`, `test_run_gate_failure_does_not_reach_manifest_acquisition`, `test_2023plus_enumeration_does_not_reach_manifest_acquisition` (the manifest fetcher records zero URLs in each).

## 6. Manifest network route
The only network primitive in the module is `_open_url`'s lazy `import urllib.request` (single site, L169) and single `opener.open(...)` (L172). `fetch_manifest_bytes` routes through `_open_url` (L196). There is no `import requests` / `subprocess` / `os.system` / `os.popen` / `urlopen(` / second opener. Manifest URL constants `GDELT1_MD5SUMS_URL` (L333) / `GDELT1_FILESIZES_URL` (L334) are passed to `fetch_manifest_bytes` and referenced as provenance strings in `manifest_provenance`; they are never opened by any other route. With the gate `False`, both manifest and daily acquisition hard-error before network import/open (`test_manifest_default_routes_through_gated_open_url`, `test_single_real_entrypoint_default_manifest_and_daily_gated`, `test_no_separate_manifest_network_route`).

## 7. Single real/default entrypoint status
`run_bounded_integrity_build` remains the only orchestrator whose default byte source (manifests AND daily zips) is the gated real fetch. With no seams supplied, default manifest acquisition reaches `_open_url` first and hard-errors (`test_single_real_entrypoint_default_manifest_and_daily_gated`). Injected seams (`md5sums_bytes` / `filesizes_bytes` / `manifest_fetch_callable` / `fetch_callable`) are synthetic/test-only and are rejected in a gate-enabled session by the §3 seam-mode guard (`test_wired_seam_mode_guard_blocks_injected_seams_when_gate_enabled`), so they cannot be used as a real-run bypass. Integrity / exact-58 / slice are applied unconditionally to whatever bytes are obtained.

## 8. Old/synthetic harness status
`run_phase2_archive_build` remains neutered (refuses `None`/default and the real-network entrypoints) AND now additionally fails closed at entry if `REAL_FETCH_SOURCE_GATE_ENABLED` is `True` (belt-and-suspenders §5 guard), so it cannot be used during a future gate-enabled session (`test_bare_harness_blocked_when_gate_enabled`). It still cannot reach `_open_url` for real bytes.

## 9. Integrity/cache/exact-58/slice preservation
Unchanged from `68505a2` and re-proven through the callable-manifest seam: `verify_cached_zip` for cache hits, `fetch_stable` for uncached bytes, `verify_file_integrity` (MD5/size) before archive write, cache write only after verification, `classify_payload_rows(enforce_exact_columns=True)`, and `fetched_set_fully_covers` slice routing (`test_injected_manifest_callable_flows_through_pipeline`, `test_manifest_callable_full_path_with_cache`). Missing manifest entries still fail closed (`test_manifest_missing_entry_via_callable_fails_closed`); the prior wired/hardening tests remain green.

## 10. Value-blindness
The amendment branches only on URLs, filenames, dates, bytes, sizes, MD5/SHA hashes, cache/integrity status, source-file coverage, and column counts. No aggregation, no branch on `quadclass/goldsteinscale/nummentions/avgtone` values; the generated manifest (incl. the new `manifest_source_mode` string + boundary declaration) is structural-only — no value summaries, no sample rows, no value-conditioned buckets (`test_manifest_acquisition_output_value_agnostic`).

## 11. Manifest retry-stability (not implemented) — why corruption still fails closed
`fetch_stable` retry-stability is applied to **daily zips** but not to manifests. This is acceptable because malformed / truncated / corrupt manifests fail closed downstream before any archive write:
- a truncated or garbage `md5sums` / `filesizes` yields parsed maps that omit expected daily filenames, so `reconcile_universe_against_manifests` raises `IntegrityManifestError` before the daily loop;
- even if reconciliation somehow passed, a wrong per-file MD5 or size raises `IntegrityVerificationError` at `verify_file_integrity` before the row write.
Proven by `test_manifest_truncation_fails_closed_via_reconcile` (truncated and garbage manifests both raise `IntegrityManifestError`). A future real-run dispatch may add manifest retry-stability if desired; it is not required for fail-closed safety.

## 12. Synthetic tests

```
python3 -m pytest -q \
  tests/test_lane2_type_tone_goldstein_local_archive.py \
  tests/test_lane2_type_tone_goldstein_fetch_path.py
100 passed in 0.39s
```

Broader regression:

```
python3 -m pytest -q tests/ -k "lane2"
645 passed, 596 deselected in 54.14s
```

Environment: Python 3.8.2, pytest 8.3.5. §8 requirement → test map:
1 `test_manifest_source_gate_remains_disabled`;
2/3/17 `test_manifest_default_routes_through_gated_open_url`;
4/5 `test_no_separate_manifest_network_route`;
6-10 `test_injected_manifest_callable_flows_through_pipeline`;
11/12 `test_manifest_missing_entry_via_callable_fails_closed`;
13/14 `test_codebook_failure_does_not_reach_manifest_acquisition`;
15 `test_run_gate_failure_does_not_reach_manifest_acquisition`;
16 `test_2023plus_enumeration_does_not_reach_manifest_acquisition`;
18-20 `test_manifest_callable_full_path_with_cache` (+ retained `68505a2` wired tests);
21 `test_single_real_entrypoint_default_manifest_and_daily_gated`;
22 `test_bare_harness_blocked_when_gate_enabled` + `test_wired_seam_mode_guard_blocks_injected_seams_when_gate_enabled`;
23 (all tests synthetic / gate False);
24 `test_manifest_acquisition_output_value_agnostic`;
25 `test_manifest_truncation_fails_closed_via_reconcile`.

## 13. No-network confirmation
No socket/URL opened; `urllib` imported only lazily inside the gated `_open_url`, never reached. Default manifest + daily acquisition both proven to hard-error at the gate. No official manifests fetched, no daily zips downloaded, no real cache from network, no bounded/full build.

## 14. Generated `/tmp` artifacts (evidence only; not committed)
- `/tmp/ttg_manifest_acquisition_callsite_scan.txt`
- `/tmp/ttg_manifest_acquisition_source_gate_scan.txt`
Plus the post-commit byte-review bundle under `/tmp/ttg_<new_head>_byte_review/`.

## 15. Changed paths
- `src/lane2_type_tone_goldstein_archive_fetch_path.py` (modified — `fetch_manifest_bytes`, optional manifest bytes + `manifest_fetch_callable`, seam-mode guard, gate-enabled harness guard, manifest-acquisition wiring + structural markers)
- `tests/test_lane2_type_tone_goldstein_fetch_path.py` (modified — 14 manifest-acquisition tests)
- `docs/lane2_type_tone_goldstein_phase2_precontact_manifest_acquisition_wiring_report_v0.1.md` (new — this report)

The archive module (`src/lane2_type_tone_goldstein_local_archive.py`) was **not** changed. No generated/cache outputs under `data/raw/`, `archive/`, or `results/` were created or staged.

## 16. Remaining blocked work
- **Real GDELT network contact / manifest fetch / zip download** — blocked; require editing the source gate **and** a separate execution authorization after byte review of this commit. With the gate enabled, `run_bounded_integrity_build` (no seams) is the single entrypoint that fetches manifests + daily zips through `_open_url`.
- **Bounded real-slice build** — separately unauthorized.
- **Full-window archive build** — separately unauthorized.
- **TTG extraction** — still BLOCKED; requires a locked estimator-and-evaluation pre-registration before any value-level read.
- **Predictor-vs-outcome alignment seam** — still open (extraction-gate question).
- **Outcome-side join** — still blocked.
- **No push** performed.
