# Lane 2 / TTG — Streaming April real-contact equivalence run — report v0.1

`PASS — STREAMING APRIL EQUIVALENCE REPRODUCED`

Ran the value-blind `run_bounded_integrity_build` over `2013-04-01 … 2013-04-30`
using the new streaming writer committed at `053bfa9` (protected fetch-module
identity `1d069087…`), and proved the streamed real-byte archive reproduces the
prior April archive bytes from the cleared pre-streaming runs **byte-for-byte**
(archive SHA-256 `c077edc6…`, full match). Real-contact run; gate transiently
armed only during the run, reverted before analysis/commit; source bytes left
byte-identical; gate disarmed in committed bytes.

## 1. Preflight anchor
- HEAD `053bfa96ad760d98590ed2ceb608a58f0cba497c` (`053bfa9`); parent `9b10a9d…`; `origin/main` `fb26424…`; ahead/behind `15 0`; no push.
- Protected fetch-module SHA-256 before run: `1d069087f65fc604f976aea81fe3f2f7f3f65e44e6de2cbc94bc2afbb8f807e4`.
- `local_archive.py` (`src/lane2_type_tone_goldstein_local_archive.py`, single resolved path) SHA-256: `6a3d715e078c796391a930270c1f34a086e6ef9df2d663752d1922241ee5f40d`.
- Gate: one definition `REAL_FETCH_SOURCE_GATE_ENABLED = False`; zero `= True`. Both cache/out paths gitignored. Clean except two pre-existing untracked docs (not opened/staged).

## 2. Arm / revert evidence
- Transient gate arm: exactly one line `REAL_FETCH_SOURCE_GATE_ENABLED = False` → `True` (L54); `git diff --numstat` = `1 1`; only `-...= False` / `+...= True` at the gate line.
- Run executed armed (`gate_at_import = true`). Revert ran immediately on return via an in-process `finally` AND an unconditional outer `git checkout`, before any analysis/report/stage/commit.
- Post-revert: gate `= False` (L54), zero `= True`; worktree fetch-module SHA-256 `1d069087…`; committed fetch-module SHA-256 `1d069087…`; committed `local_archive.py` SHA-256 `6a3d715e…`; `git diff` on both files empty.

## 3. Run-authorization guard evidence (§4)
- `gate_at_import = true` (armed real run).
- Synthetic seams absent: `md5sums_bytes is None`, `filesizes_bytes is None`, `manifest_fetch_callable is None`, `fetch_callable is None` (call made with all four omitted/None).
- Three-guard run authorization satisfied: module-authorized=True, CLI flag=True, env `LANE2_TTG_LOCAL_ARCHIVE_BUILD_AUTHORIZED=1` (same as the cleared `1698e86`/`9b10a9d` runs; these are the run gate, not seams).
- Requested window: `2013-04-01 … 2013-04-30`.
- Authorized contact scope: official GDELT 1.0 Event manifests via `fetch_manifest_bytes → gated _open_url`; daily zips `20130401.export.CSV.zip … 20130430.export.CSV.zip` only (all served from verified cache this run).
- Forbidden boundary/source contacts: no `2013-03-31`, no `2013-05-01`, no `2023+` (fetched_dates = 04-01…04-30 only).
- Protected fetch-module SHA before/after: `1d069087…`. `local_archive.py` SHA: `6a3d715e…`.
- Source gate reverted before analysis/report/stage/commit.

## 4. Manifest provenance (this run)
- `md5sums`  — `http://data.gdeltproject.org/events/md5sums`  — byte size **282966**, SHA-256 `40e56da0b7c07761495601ca3159840bd1b798db5b44aeb244fe4800b651a2fb`.
- `filesizes` — `http://data.gdeltproject.org/events/filesizes` — byte size **157375**, SHA-256 `95bf8712f62186805e999fb33c7ae0d6f6b7f78e539f47ce9cbae78a5e062e04`.
- Manifests fetched fresh through the gated `_open_url`; all 30 daily zips served from the existing verified cache (`verify_cached_zip`, source = `cache`), so the only network this run was the two manifest fetches.

## 5. Metric-by-metric equivalence (recorded pre-streaming / this streaming run / result)
| Metric | recorded pre-streaming | this run | result |
|---|---|---|---|
| source files | `20130401…20130430.export.CSV.zip` | same | PASS |
| source file count | 30 | 30 | PASS |
| `2013-03-31` fetched | no | no | PASS |
| `2013-05-01` fetched | no | no | PASS |
| `2023+` event-data contact | no | no | PASS |
| tolerated gaps | 0 / none | 0 / none | PASS |
| primary covered SQLDATEs | 2013-04-02 … 2013-04-29 | 2013-04-02 … 2013-04-29 | PASS |
| exact-58 conformance | all 30 conformant | all 30 conformant | PASS |
| total `column_count_mismatch` | 0 | 0 | PASS |
| raw rows | 990702 | 990702 | PASS |
| date eligibility failures | 30961 | 30961 | PASS |
| edge window exclusions | 26926 | 26926 | PASS |
| classify survivors | 932815 | 932815 | PASS |
| primary archive rows | 895932 | 895932 | PASS |
| drop arithmetic | 990702 − 30961 − 26926 = 932815 | 990702 − 30961 − 26926 = 932815 | PASS |
| archive byte size | 31166630 | 31166630 | PASS |
| archive SHA-256 | `c077edc6d4e0214797d001fdd8b1601a791868bf05fe84732dbd48cdfc716238` | `c077edc6d4e0214797d001fdd8b1601a791868bf05fe84732dbd48cdfc716238` | PASS (FULL) |
| manifest `md5sums` SHA-256 | `40e56da0…` | `40e56da0b7c07761495601ca3159840bd1b798db5b44aeb244fe4800b651a2fb` | PASS |
| manifest `md5sums` size | 282966 | 282966 | PASS |
| manifest `filesizes` SHA-256 | `95bf8712…` | `95bf8712f62186805e999fb33c7ae0d6f6b7f78e539f47ce9cbae78a5e062e04` | PASS |
| manifest `filesizes` size | 157375 | 157375 | PASS |

The load-bearing acceptance criterion (streamed archive SHA-256) reproduces the recorded April archive SHA in **full** — the full prior SHA `c077edc6d4e0214797d001fdd8b1601a791868bf05fe84732dbd48cdfc716238` is recorded in committed docs (`…phase2_bounded_real_slice_report_v0.1.md`, `…amended_bounded_slice_equivalence_report_v0.1.md`), and this run's archive SHA equals it exactly. Per-file drop-reason aggregates cross-checked: returned aggregates equal the per-file sums (raw 990702; date-elig 30961; edge 26926; classify 932815).

## 6. Streaming machinery (§6)
| Field | expected | this run | result |
|---|---|---|---|
| `ELIGIBILITY_DELTA_DAYS` | 1 | 1 | PASS |
| `streaming_release_depth` | 2 | 2 | PASS |
| `max_buffered_source_file_blocks` | 3 | 3 | PASS |
| retained-offset hard-fail count | 0 | 0 (run completed; no `RetainedOffsetHardFail`) | PASS |
| terminal buffered blocks flushed | yes | yes (final boundary `2013-04-30` edge-excluded; `2013-04-02` covered) | PASS |
| atomic archive temp→final promote | yes | yes (`.partial` → final on success) | PASS |
| atomic provenance temp→final promote | yes | yes (manifest `.partial` → final after archive) | PASS |
| final archive published only on success | yes | yes | PASS |
| final provenance published only on success | yes | yes | PASS |
| no production whole-window accumulator | yes | yes (`boundary_declarations.streaming_archive_write = true`) | PASS |
| public return/provenance keys present | yes | yes (all prior keys + agg counters surfaced) | PASS |

## 7. Final verdict
`PASS — STREAMING APRIL EQUIVALENCE REPRODUCED`. Every required metric matches the cleared pre-streaming April result exactly; the streamed archive is byte-identical (full SHA `c077edc6…`), and the streaming machinery fields are satisfied. The new streaming writer (`1d069087…`) produces output byte-identical to the pre-streaming path on this real bounded slice.

## 8. Firewall confirmations
- No extraction; no TTG feature computation; no value statistics/buckets/correlations/regressions/scores/model metrics.
- No outcome reads; no join reads; no market reads; no V1/V2.
- No `2013-03-31` fetch; no `2013-05-01` fetch; no `2023+` event-data contact.
- No full-window decade build.
- Gate `False` in committed bytes and in worktree; fetch module byte-identical to `1d069087…` before and after; `local_archive.py` byte-identical to `6a3d715e…`.
- Generated raw/cache/archive/result artifacts are gitignored, untracked, and not staged or committed (daily zips served from verified cache; archive + provenance manifest written under the gitignored out_dir).
- No memory update; no push.
