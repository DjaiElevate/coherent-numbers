# Lane 2 / TTG — Full-window real archive build — FAIL-CLOSED report v0.1

## A. Verdict

`FAIL-CLOSED — FULL-WINDOW REAL ARCHIVE BUILD NOT ACCEPTED`

The value-blind streaming build over `2013-04-01 … 2022-12-31` ran far (3506 / 3558
present-in-both source files acquired+verified, ~32 GB cache, 18.4 GB partial
archive, bounded memory) but **aborted hard-closed** on a real upstream GDELT
data-availability condition: the daily file for **`2022-11-10`** is listed in BOTH
official manifests yet returns **HTTP 404** on the server. A present-in-both file
that fails to fetch is a **hard FAIL** under the committed contract (not a
tolerable mutual-absence gap, never silently skipped or backfilled). No final
archive or provenance manifest was promoted. The source gate was reverted; source
modules are byte-identical to their protected identities. No push.

This is a clean firewall outcome: the streaming/memory/disk machinery proved out
at near-decade scale; the blocker is upstream data availability, which the build
correctly refused to paper over.

## B. Preflight anchor

- HEAD: `69fe00c624e2753023068d9b8a11f67aba5bfacf` (`69fe00c`)
- parent: `053bfa96ad760d98590ed2ceb608a58f0cba497c`
- origin/main: `fb26424c92ad30a52f579ec4a1dd8a2b069c2cb0`
- ahead/behind: `0 16` (no push)
- allowed untracked docs (not opened/staged): `docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md`, `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`
- fetch module: `src/lane2_type_tone_goldstein_archive_fetch_path.py` — SHA before/after `1d069087f65fc604f976aea81fe3f2f7f3f65e44e6de2cbc94bc2afbb8f807e4` (committed + worktree, byte-identical)
- local archive: `src/lane2_type_tone_goldstein_local_archive.py` — SHA before/after `6a3d715e078c796391a930270c1f34a086e6ef9df2d663752d1922241ee5f40d` (committed + worktree, byte-identical)
- gate before/after: exactly one active `REAL_FETCH_SOURCE_GATE_ENABLED = False`; zero active `= True` (committed + worktree)
- cache path: `data/raw/lane2_ttg_gdelt1_event_zip_cache` (gitignored: `.gitignore:10 data/raw/`)
- output path: `results/lane2_type_tone_goldstein_full_window_real_archive_build` (gitignored: `.gitignore:8 results/`)
- generated archive/cache/partial outputs remain untracked + uncommitted
- no push

### Disk-feasibility (PASS — not the blocker)
- Pre-arm conservative basis: 15 MB/file upper bound → remaining footprint ~81 GB; 1.5× ≤ free (PASS) with §5 manifest refinement as the binding gate.
- Manifest-refined (exact `filesizes`): remaining footprint **61.11 GB** (remaining zips 34.63 GB + archive est 17.99 GB + overhead 8.5 GB); free **134.27 GB** (125.06 GiB); 1.5× required **91.67 GB** → PASS; after-run free **68.14 GiB** ≥ 25 GiB → PASS.
- No disk/write/IO error occurred. Free disk after the run: ~74 GiB (32 GB cache + 18.4 GB partial archive written). Disk was never the limiter.

## C. Run-authorization block

- `gate_at_import = true` (armed real run, both attempts).
- Synthetic seams absent/None: `md5sums_bytes=None`, `filesizes_bytes=None`, `manifest_fetch_callable=None`, `fetch_callable=None`.
- Three-guard authorization: module-authorized=True, CLI flag=True, `LANE2_TTG_LOCAL_ARCHIVE_BUILD_AUTHORIZED=1`.
- Requested source window: `2013-04-01 … 2022-12-31`.
- Authorized contact scope: official GDELT 1.0 Event manifests (`md5sums`, `filesizes`) via `fetch_manifest_bytes → gated _open_url`; daily zips inside the window only.
- Forbidden contact confirmation: no `2013-03-31`; no `2023-01-01`; no `2023+` (window enumeration rejects them before any fetch; not in `fetched_dates`).
- Source gate reverted (in-process `finally` + unconditional outer `git checkout`) before this analysis/report/stage/commit, on both attempts.

## D. Manifest provenance, reconciliation, transport caveat

- `md5sums`  — `http://data.gdeltproject.org/events/md5sums`  — byte size **282966**, SHA-256 `40e56da0b7c07761495601ca3159840bd1b798db5b44aeb244fe4800b651a2fb`.
- `filesizes` — `http://data.gdeltproject.org/events/filesizes` — byte size **157375**, SHA-256 `95bf8712f62186805e999fb33c7ae0d6f6b7f78e539f47ce9cbae78a5e062e04`.
- Reconciliation over the requested window (3562 calendar days): present-in-both **3558**; absent-in-both (tolerated mutual-absence gaps) **4**; single-manifest-only **0** (no manifest-inconsistency abort).
- Tolerated gap dates (absent from BOTH manifests, correctly skipped/not fetched): **`2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`** (all in 2014).
- Verification source summary: of the 3506 acquired present-in-both files, all were MD5+byte-size verified against the manifests; April 2013 (30) reused from prior verified cache, the remainder fetched this run.
- At-scale transport caveat: this was the first at-scale real fetch over plain `http://`; manifests are unsigned / trust-on-first-use; per-file MD5 + byte-size verification against the manifests is the accepted integrity backstop; any integrity failure hard-fails. This caveat is carried forward and is a limitation, not a license to cross the firewall or redesign mid-run.

## E. Abort condition (load-bearing)

Two armed attempts of the single authorized build:

1. **Attempt 1** (`bnhkuec5z`): aborted with `http.client.IncompleteRead` (10,612,997 bytes read, 679,758 more expected) — a **transient** daily-zip download truncation over plain HTTP inside `fetch_stable → fetch_one_source_file → _open_url`. ~525 files cached at abort. Atomic discipline held (no promote); gate reverted.
2. **Attempt 2 (resume from verified cache)** (`bywjcd86d`): re-verified the cache and continued, reaching **3506 / 3558** present-in-both files (last cached source date **`2022-11-09`**), then aborted with `urllib.error.HTTPError: HTTP Error 404: Not Found` on the next present-in-both daily file.

Abort point: **`2022-11-10`** — the next source date after the last cached `2022-11-09`; the uncached tail is exactly `2022-11-10 … 2022-12-31` (52 dates = 3558 − 3506). `2022-11-10` is listed in BOTH manifests (so it is fetched, not a mutual-absence gap) yet returns HTTP 404 — a manifest-listed-but-upstream-unavailable file. This matches the previously documented `2022-11-10` upstream-unavailable condition in the Lane 2 count-build trail.

Classification: a **present-in-both file failing to fetch is a hard FAIL** (§3). The reviewed path raised the error without silent retry-around, conversion to a gap, or backfill — the firewall-correct behavior. Because the 404 is persistent (the file is not served upstream), further resume-from-cache attempts re-hit the same condition; the build is **not completable under the current reviewed fetch path / gap-tolerance contract**.

## F. Coverage / per-year (partial — build aborted before emitting the provenance manifest)

The aborted run did not produce the structural coverage/row ledger (it raised inside the fetch loop). The value-safe structural evidence available is the per-year **acquired+verified source-file** breakdown (from cache filenames; dates only — no row/field data):

| Year | cached present-in-both source files | note |
|---|---:|---|
| 2013 | 275 | full `2013-04-01 … 2013-12-31` |
| 2014 | 361 | 365 − 4 tolerated gaps (`01-23/24/25`, `03-19`) |
| 2015 | 365 | full |
| 2016 | 366 | full (leap) |
| 2017 | 365 | full |
| 2018 | 365 | full |
| 2019 | 365 | full |
| 2020 | 366 | full (leap) |
| 2021 | 365 | full |
| 2022 | 313 | `2022-01-01 … 2022-11-09`; aborted at `2022-11-10` (404); `2022-11-10 … 2022-12-31` (52) unacquired |
| **total** | **3506** | / 3558 present-in-both |

Per-year row counts, date-eligibility failures, edge-window exclusions, classify-retained, primary-archive rows, and the per-SQLDATE coverage ledger are **unavailable** because the build aborted before completing and before emitting the value-blind provenance manifest. Nominal primary window would have been `2013-04-02 … 2022-12-30`; edge-excluded endpoints `2013-04-01` (needs pre-window `2013-03-31`) and `2022-12-31` (needs sealed `2023-01-01`); neither was contacted. Expected April-2013 decade-internal primary would extend to `2013-04-30` (interior `2013-05-01` present), but no completed coverage ledger was produced.

## G. Drop arithmetic / archive identity

No completed archive. Aggregate row/drop counters were not emitted (abort before the provenance manifest). The on-disk artifact is a non-promoted partial only:

- `results/lane2_type_tone_goldstein_full_window_real_archive_build/ttg_approved_fields_archive.csv.partial` — 18,411,313,115 bytes (gitignored, untracked, **not** promoted to a final archive; not committed; contents not inspected).
- No final `ttg_approved_fields_archive.csv` and no final `ttg_archive_provenance_manifest.json` exist (atomic temp→promote only on success).

## H. Streaming machinery (proved out up to the abort)

- `ELIGIBILITY_DELTA_DAYS = 1`; `streaming_release_depth = 2` (= 2·EDD, derived).
- The streaming writer + bounded sliding file-block buffer + atomic temp write operated at near-decade scale (3506 files, 18.4 GB partial archive) within bounded memory — the memory limitation that blocked the earlier non-streaming attempt did not recur.
- Atomic discipline confirmed: a hard fail mid-stream published **no** final archive and **no** final provenance manifest; only the gitignored `.partial` remains.
- `max_buffered_source_file_blocks` for the completed run is not in a result manifest (build aborted), but the build streamed 18.4 GB to the partial with no memory failure, consistent with the bounded `2·EDD+1 = 3` design and the prior April real-slice proof; high-water did not scale with window length (no OOM across 3506 files).
- `boundary_declarations.streaming_archive_write` is set by the build path on success; no success manifest was emitted here.

## I. Disk / resource record

- pre-arm conservative estimate: ~81 GB remaining footprint (15 MB/file basis) → 1.5× PASS.
- manifest-refined estimate: footprint **61.11 GB**; free **134.27 GB**; 1.5× req **91.67 GB** (PASS); after-run free **68.14 GiB** (PASS).
- cache before run: 30 files / ~0.06 GB; cache after: **3506 files / ~32 GB**.
- output dir after: 18.4 GB (`.partial` only).
- free disk before: ~134.27 GB (125.06 GiB); after: ~74 GiB.
- disk/write/IO errors: **none**. Disk was not the limiter; the abort was a network/data-availability `HTTP 404` on a manifest-listed file.

## J. Firewall confirmations

- No extraction; no TTG features; no statistics; no buckets/correlations/regressions/scores/model metrics.
- No outcome reads; no market reads; no joins; no V1/V2.
- No `2013-03-31`; no `2023-01-01`; no `2023+` contact.
- No source-code commit; generated archive/cache/raw/results untracked and gitignored.
- Gate `False` in committed bytes and worktree; zero active `= True`.
- Fetch module unchanged at `1d069087…`; `local_archive.py` unchanged at `6a3d715e…`.
- No push.

## K. Why not accepted, and what would unblock it

The decade build is blocked on a real upstream condition: at least one present-in-both manifest-listed daily file (`2022-11-10`) returns HTTP 404. The committed contract correctly treats this as a hard FAIL (it is not mutual-absence; tolerating it would mean silently skipping a file the manifests claim exists). Completing the full window would require a **separately-authorized** decision/amendment (out of scope for this value-blind run; no code change made here), e.g.:

1. A governance + code amendment defining a new tolerated class **"manifest-listed-but-upstream-404 / confirmed-unavailable"**, distinct from mutual-absence, with its own gap ledger and coverage semantics (so `2022-11-10`'s dependent SQLDATEs become gap-uncovered rather than aborting), re-deriving coverage under the support rule; and/or
2. A transport-robustness amendment adding bounded retry/backoff to `_open_url`/`fetch_stable` for transient `IncompleteRead` truncations (which also occurred once), so a single transient truncation does not abort a multi-thousand-file run.

Both are code/governance changes requiring their own reviewed dispatch and byte-review; neither was performed here. The ~32 GB verified cache (3506 files) is preserved for any future authorized resumed/amended run.

Pre-registration remains the gate before any extraction, feature work, statistics, outcome-side join, or market-side work. Read-spend remains unspent.
