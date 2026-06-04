# Lane 2 / TTG — Amended bounded-slice equivalence run, April 2013 — report v0.1

`PASS — BOUNDED-SLICE EQUIVALENCE REPRODUCED`

Re-ran the value-blind `run_bounded_integrity_build` over `2013-04-01 … 2013-04-30`
at the amended protected fetch-module identity `4f4708a` and verified its
structural output reproduces the already-cleared `1698e86` April real-byte result
**exactly**. Real-contact run (gate transiently armed only during the run, then
reverted). Not a full-window build, not extraction, not a code change. Source
bytes left byte-identical; gate disarmed in committed bytes.

## 1. Preflight anchor
- HEAD: `4f4708affffc54cdb923150a870c16640e4de516` (`4f4708a`)
- parent: `1698e868294e3423e9fba0aba735de44894d9337` (`1698e86`)
- `origin/main`: `fb26424c92ad30a52f579ec4a1dd8a2b069c2cb0` (`fb26424`)
- ahead/behind: `13 0`; no push.
- Protected fetch-module SHA-256 before run: `c0dfda3745b1254854d6118c1375a5d960bc13cbd9d54f13b140990bf5a7f439`.
- Gate before run: exactly one definition `REAL_FETCH_SOURCE_GATE_ENABLED = False` (L51); zero `= True`.
- `data/raw/lane2_ttg_gdelt1_event_zip_cache` and `results/lane2_ttg_gdelt1_amended_bounded_slice_equivalence` both gitignored.
- Pre-existing untracked docs (not opened, not staged): `docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md`, `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`.

## 2. Arm / revert evidence
- Transient gate arm: exactly one line `REAL_FETCH_SOURCE_GATE_ENABLED = False` → `True` at L51 (`git diff --numstat` = `1 1`; only `-...= False` / `+...= True` at the gate line; no other change).
- The build ran armed (`gate_at_import = true`). Revert executed immediately on return via an in-process `finally` AND an unconditional outer `git checkout -- src/lane2_type_tone_goldstein_archive_fetch_path.py`, before any analysis/report/stage/commit.
- Post-revert gate grep: `51:REAL_FETCH_SOURCE_GATE_ENABLED = False`; zero `= True`.
- Post-revert worktree fetch-module SHA-256: `c0dfda3745b1254854d6118c1375a5d960bc13cbd9d54f13b140990bf5a7f439`.
- Committed fetch-module SHA-256: `c0dfda3745b1254854d6118c1375a5d960bc13cbd9d54f13b140990bf5a7f439`.
- `git diff -- src/lane2_type_tone_goldstein_archive_fetch_path.py`: empty.

(Note: an initial armed invocation refused at the three-guard run gate — `ArchiveBuildRefused`, raised before manifest acquisition, so **no network contact and no outputs**; the gate was reverted, the run-authorization guards added [`cli_flag/module_authorized/env`, the same as the cleared `1698e86` run — these are the run gate, not seams], and the single real-contact build was then run.)

## 3. Manifest provenance (this run)
- `md5sums`  — `http://data.gdeltproject.org/events/md5sums`  — byte size **282966**, SHA-256 `40e56da0b7c07761495601ca3159840bd1b798db5b44aeb244fe4800b651a2fb`.
- `filesizes` — `http://data.gdeltproject.org/events/filesizes` — byte size **157375**, SHA-256 `95bf8712f62186805e999fb33c7ae0d6f6b7f78e539f47ce9cbae78a5e062e04`.
- Both identical to the cleared `1698e86` manifest provenance. Manifests fetched fresh through `fetch_manifest_bytes → gated _open_url`; all 30 daily zips served from the existing verified cache (`verify_cached_zip`, source = `cache`), so the only network this run was the two manifest fetches.

## 4. Source-file set
- `20130401.export.CSV.zip` … `20130430.export.CSV.zip` (count **30**).
- `2013-03-31` fetched: **no**. `2013-05-01` fetched: **no**. `2023+` contact: **none**.
- Reconciliation (scoped to the 30 authorized files): present-in-both **30**, absent-in-both **0**, single-manifest-only **0**, tolerated gaps **0**, reconciled_ok.

## 5. Metric-by-metric equivalence table
Format: metric — recorded `1698e86` / this-run / PASS|FAIL.

| Metric | recorded 1698e86 | this run | result |
|---|---|---|---|
| source files | `20130401…20130430.export.CSV.zip` | `20130401…20130430.export.CSV.zip` | PASS |
| source file count | 30 | 30 | PASS |
| `2013-03-31` fetched | no | no | PASS |
| `2013-05-01` fetched | no | no | PASS |
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

Bonus byte-level corroboration (structural hashes, not values):
- archive output SHA-256 `c077edc6d4e0214797d001fdd8b1601a791868bf05fe84732dbd48cdfc716238` (byte size 31166630) — **identical** to the cleared `1698e86` archive.
- Coverage ledger: covered = 2013-04-02…2013-04-29 (28); edge-excluded = {2013-04-01, 2013-04-30}; gap-uncovered = none.

## 6. Final verdict
`PASS — BOUNDED-SLICE EQUIVALENCE REPRODUCED`. Every required metric matches the cleared `1698e86` bounded-slice result exactly; the archive output and manifest provenance are byte-identical. The amended `4f4708a` orchestrator is structurally equivalent to the cleared `1698e86` orchestrator on this bounded slice. The amended gap-tolerance logic does not change the no-gap April result: with all 30 files present-in-both, the new classification yields zero gaps and the same covered/edge-excluded ledger.

## 7. Firewall confirmations
- No extraction; no TTG feature computation; no value statistics/buckets/correlations/regressions/scores/model metrics.
- No outcome reads; no join reads; no market reads; no V1/V2.
- No `2013-03-31` fetch; no `2013-05-01` fetch; no `2023+` event-data contact.
- No full-window build.
- Gate `False` in committed bytes and in worktree; fetch module byte-identical to `c0dfda37…` before and after the run.
- Generated raw/cache/archive/result artifacts are gitignored, untracked, and not staged or committed.
- No memory update; no push.
