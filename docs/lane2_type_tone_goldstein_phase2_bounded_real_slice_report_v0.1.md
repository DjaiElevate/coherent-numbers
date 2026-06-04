# Lane 2 / Type-Tone-Goldstein — Phase-2 bounded real-slice archive-build report v0.1

`BOUNDED REAL-SLICE COMPLETED (2013-04-01…2013-04-30); SOURCE GATE TRANSIENTLY ENABLED THEN REVERTED TO False; REPO NOT NETWORK-ARMED; FETCH MODULE BYTE-IDENTICAL TO effe853; VALUE-BLIND; EXTRACTION STILL BLOCKED; NO PUSH`

First authorized real GDELT 1.0 Event-data contact for the TTG archive path. A
bounded value-blind smoke test over `2013-04-01…2013-04-30` only. No full-window
build, no extraction, no features/statistics, no join/outcome/market, no V1/V2,
no 2023+. Generated raw zips / archive / cache are gitignored and untracked. The
only tracked change is this report.

## 1. Preflight state

```
HEAD                       effe853
HEAD^                      68505a2
origin/main                fb26424
origin/main...HEAD (L/R)   0   11   (local ahead by 11; no push)
status --short             two pre-existing untracked docs only
```
Matched expected state. Proceeded.

## 2. Governing artifacts read & constraints
Read the fetch-path gate, real-run hardening, bounded-run wiring, and manifest-acquisition wiring reports, plus both source modules and both test files. Constraints: five approved fields only; never compute over the four substantive fields; source gate edit-only; eligibility `F <= SQLDATE+1`; window `2013-04-01…2022-12-31`; 2023+ sealed; pre-window never read; exact 58-column daily layout; value-blind structural-only outputs; single real/default fetch entrypoint (`run_bounded_integrity_build`); manifests + daily zips through the gated `_open_url`; slice-aware coverage routes slice edges out.

### Reviewed base
This run used the reviewed manifest-acquisition base **`effe853`**. The fetch module `src/lane2_type_tone_goldstein_archive_fetch_path.py` was byte-unchanged before and after the run (SHA-256 `c656614a160571be56305e87ed717e048a04066c3ade044411075ae4d3123d8d`), apart from the transient one-line gate flip that was reverted.

## 3. Pre-run no-network tests
```
python3 -m pytest -q tests/test_lane2_type_tone_goldstein_fetch_path.py tests/test_lane2_type_tone_goldstein_local_archive.py
100 passed in 0.32s
```
Environment: Python 3.8.2, pytest 8.3.5.

## 4. Transient source-gate enablement
A single-line source edit flipped `REAL_FETCH_SOURCE_GATE_ENABLED = False` → `True` (L51); `git diff` showed exactly that one-line change and no other source change. The run was invoked via `run_bounded_integrity_build` with **no injected seams** (no `md5sums_bytes` / `filesizes_bytes` / `manifest_fetch_callable` / `fetch_callable`), `is_zip=True`, `cache_dir` under the gitignored TTG raw-cache, `out_dir` under gitignored `results/`.
- Transient gate-enable patch: `/tmp/ttg_bounded_real_slice_transient_gate_enable.patch`, SHA-256 `6c35f536cb715b6212289a6081e4e0bc773d86f110153a87b996559c782d93c0` (13 lines).

## 5. Gate reverted / repo disarmed
Immediately after the run, the gate literal was reverted to `False`. Confirmed:
- `REAL_FETCH_SOURCE_GATE_ENABLED = False` (L51); **no `= True`** anywhere.
- `git diff` on the fetch module is **empty** (back to committed `effe853`); working-tree SHA-256 = `c656614a…` (byte-identical to reviewed `effe853`).
- `_open_url` defense-in-depth gate present (L164). The final committed state is **not network-armed**.

## 6. Official integrity manifests
Fetched once each, through the gated `_open_url` (default real path; `manifest_source_mode = gated_open_url_default`):
- `md5sums`  — `http://data.gdeltproject.org/events/md5sums`  — byte size **282966**, SHA-256 `40e56da0b7c07761495601ca3159840bd1b798db5b44aeb244fe4800b651a2fb`.
- `filesizes` — `http://data.gdeltproject.org/events/filesizes` — byte size **157375**, SHA-256 `95bf8712f62186805e999fb33c7ae0d6f6b7f78e539f47ce9cbae78a5e062e04`.

**Known bounded-smoke-test limitation:** the GDELT endpoint is plain `http://` and the integrity manifests are not cryptographically signed. Official MD5 + byte size are used as the authoritative integrity check; SHA-256 is additional local provenance. The acquisition path was **not** redesigned in this run.

## 7. Manifest reconciliation status (scoped to the 30 authorized files only)
- expected authorized source-file count: **30**
- present in `md5sums`: **30**
- present in `filesizes`: **30**
- missing from `md5sums`: **0**
- missing from `filesizes`: **0**
- parse/reconcile error status: **none** (`reconciled_ok = true`); real manifest format **accepted**.

The official manifests list many non-authorized filenames (other dates/years); these are metadata-only, were **not** enumerated, summarized, or fetched, and no non-authorized manifest contents are reproduced here.

## 8. Bounded network contact
Authorized window `2013-04-01…2013-04-30` (inclusive). Contacted exactly: the two manifests above + the 30 daily Event zips `20130401.export.CSV.zip … 20130430.export.CSV.zip`. **No** `2013-03-31`, **no** `2013-05-01`, **no** pre-window/post-window/2023+ event file, **no** market/outcome/join data, **no** prior `results/`/`archive/`/unrelated `data/raw/` were enumerated, fetched, or opened. `fetched_dates` = `2013-04-01 … 2013-04-30` only.

## 9. Raw cache status
- daily zips fetched from network: **30**
- daily zips served from verified cache: **0** (cold cache for this first run)
- cache location `data/raw/lane2_ttg_gdelt1_event_zip_cache` (30 zips written, **gitignored**, untracked, unstaged).
- Cache path confirmed gitignored (`.gitignore:10 data/raw/`). Verified bytes are written to cache only after integrity verification succeeded.

## 10. Daily zip integrity status
- files verified (official MD5 + byte size): **30 / 30** (`integrity_status = verified`, `md5_ok = true`, `size_ok = true` for every file).
- MD5 mismatch count: **0**
- byte-size mismatch count: **0**
- unstable retry count: **0**
- SHA-256 recorded per file as additional local provenance (in the gitignored generated manifest, not here).

## 11. Exact 58-column enforcement
`enforce_exact_columns=True` through the reviewed path.
- per-file exact-58: **all 30 files passed**; per-file `column_count_mismatch` drop = 0 for every file.
- total `column_count_mismatch` drop count: **0**
- any file deviated from exact 58 columns: **No** (real 2013 GDELT 1.0 daily files are exactly 58 columns).

## 12. Slice-aware coverage result
- fully covered primary SQLDATE range: **`2013-04-02 … 2013-04-29`** (28 SQLDATEs) — exactly as expected.
- structurally excluded edge SQLDATEs (routed out of the primary archive):
  - `2013-04-01` — start-edge incomplete (would need pre-window `2013-03-31`, not fetched);
  - `2013-04-30` — slice-edge incomplete (would need `2013-05-01`, not fetched);
  - `2013-05-01` — these rows arrived as offset−1 (`SQLDATE = file_date+1`) contributions **inside the authorized `2013-04-30` file**; they were routed out by slice-aware coverage. **No `2013-05-01` file was fetched** to complete anything.
- The primary bounded archive contains **only** fully covered SQLDATEs; slice-incomplete SQLDATEs were not silently included.

## 13. Bounded archive build status (structural counts)
- total raw rows across 30 files: **990702**
- dropped — `date_eligibility_failure` (`source_file_date > SQLDATE + 1`): **30961**
- dropped — `edge_window_exclusion` (window/slice edge, classify stage): **26926**
- dropped — `column_count_mismatch`: **0**; all other closed drop reasons: **0**
- classify survivors (pre-slice-filter): **932815**
- primary archive retained rows (post slice-aware filter): **895932**
- approved retained schema exactly `sqldate, quadclass, goldsteinscale, nummentions, avgtone`; DATEADDED not used as instrument and not retained; row-level SOURCEURL not retained; archive keyed by raw SQLDATE.
- No sample rows, value summaries, event text, value-conditioned buckets, sums/means/quantiles/correlations/scores, extraction, or join/outcome/market access occurred.

## 14. Structural manifest/report status
The generated provenance manifest (gitignored) carries structural/provenance fields only (per-file source date, download URL, fetch-vs-cache source, official + observed MD5/size, observed SHA-256, integrity status, exact-column status, raw/retained/dropped-by-closed-reason counts, slice coverage, output path/SHA, boundary declarations). Boundary declarations recorded include `single_real_network_entrypoint`, `integrity_checked_before_archive_write`, `slice_aware_coverage_applied`, `manifest_acquired_via_gated_open_url_in_real_mode`, and the value-blind / no-2023+ / no-outcome / no-join set.

## 15. Generated local artifacts (all gitignored, untracked, unstaged)
- archive: `results/lane2_ttg_gdelt1_bounded_real_slice/20260604T210758Z/ttg_approved_fields_archive.csv` — SHA-256 `c077edc6d4e0214797d001fdd8b1601a791868bf05fe84732dbd48cdfc716238`, byte size 31166630, row_count 895932.
- generated provenance manifest: `…/ttg_archive_provenance_manifest.json` — SHA-256 `2d2195c83d5d44b4f0099bedc9e7e411affddfe2f303dbe3f911fcd265fd742a`, byte size 34373.
- raw zip cache: `data/raw/lane2_ttg_gdelt1_event_zip_cache/` (30 verified zips).
- transient gate-enable proof: `/tmp/ttg_bounded_real_slice_transient_gate_enable.patch`.
None of these are staged or committed; `results/`, `archive/`, `data/raw/` are gitignored.

## 16. Confirmations
- No extraction / feature computation / value statistics / model / join / outcome / market / V1 / V2 / 2023+ access occurred.
- Source gate transiently enabled only for the authorized run, then reverted to `False`; final committed repo is not network-armed.
- Fetch module at HEAD is byte-identical to reviewed `effe853` (`c656614a…`).
- Only tracked change is this report.

## 17. Final git status / changed paths
`git status --short` shows only this report (to be committed) plus the two pre-existing untracked docs. Changed tracked path staged: `docs/lane2_type_tone_goldstein_phase2_bounded_real_slice_report_v0.1.md` only.

## 18. Remaining blocked work
- **Full-window decade build** — separately unauthorized.
- **TTG extraction** — still BLOCKED; requires a locked estimator-and-evaluation pre-registration before any value-level read of the archived approved fields.
- **Predictor-vs-outcome alignment seam** — still open (extraction-gate question).
- **Outcome-side join / outcome / market reads / V1/V2 / 2023+** — still blocked.
- **No push** performed.
