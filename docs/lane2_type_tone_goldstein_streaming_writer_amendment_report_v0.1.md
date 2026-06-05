# Lane 2 / TTG — No-network streaming archive-writer amendment report v0.1

`CODE-ONLY, NO-NETWORK, VALUE-BLIND, GATE-CLOSED — bounded streaming archive write; byte-identical output; local_archive.py unchanged; no run; no extraction; no push`

Replaces the whole-window in-memory row accumulation in `run_bounded_integrity_build`
with a bounded sliding-window file-block stream to a temp archive that is promoted
atomically on success, so the future 2013–2022 decade build can run without holding
the decade's retained rows in memory. No classification / coverage / integrity / gap /
exact-58 behavior changed; archive output bytes are preserved. No network, no real
build, gate left disarmed.

## Preflight anchor
- HEAD `9b10a9d6b7af829c627d3554291f9ce27204d860` (`9b10a9d`); parent `4f4708a…` (`4f4708a`); `origin/main` `fb26424…`; ahead/behind `14 0`; no push.
- Old fetch-module SHA-256: `c0dfda3745b1254854d6118c1375a5d960bc13cbd9d54f13b140990bf5a7f439`.
- `local_archive.py` SHA-256 (before): `6a3d715e078c796391a930270c1f34a086e6ef9df2d663752d1922241ee5f40d`.
- Gate: exactly one definition `REAL_FETCH_SOURCE_GATE_ENABLED = False`; zero `= True`.
- Pre-existing untracked docs (not opened/staged): `docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md`, `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`.

## Identity movement
- NEW committed fetch-module SHA-256: `1d069087f65fc604f976aea81fe3f2f7f3f65e44e6de2cbc94bc2afbb8f807e4`.
- `local_archive.py` SHA-256 (after): `6a3d715e078c796391a930270c1f34a086e6ef9df2d663752d1922241ee5f40d` — **unchanged** (`git diff` empty).
- Gate after amendment: single definition `= False` (now line 54 after three added stdlib imports); zero `= True`.

## No-network / gate-closed statement
No network/GDELT/manifest/zip contact; no real build; no April/decade run; no extraction/feature/value statistics; no outcome/join/market reads; no V1/V2; no 2023+ contact. All tests use synthetic fixtures, injected seams, temp dirs, and committed code, under a suite-wide autouse no-network backstop (`_open_url` patched to raise; gate asserted `False`).

## Files changed
- `src/lane2_type_tone_goldstein_archive_fetch_path.py` (streaming writer + orchestrator rewrite; added `csv`/`hashlib`/`io` imports).
- `tests/test_lane2_type_tone_goldstein_streaming_writer.py` (new focused streaming suite).
- `docs/lane2_type_tone_goldstein_streaming_writer_amendment_report_v0.1.md` (this report).
- `local_archive.py` is **not** changed (byte-identical), reusing its public serialization convention.

## Streaming design (4.1–4.12)
- **Flush unit = whole source-file row-block** (§4.2). Each present file's classified retained rows are buffered as one ordered unit and released whole, in source-file order; coverage filtering is applied at release; never per-SQLDATE.
- **Release depth derived from `ELIGIBILITY_DELTA_DAYS`** (§4.3): `streaming_release_depth() = 2 * ELIGIBILITY_DELTA_DAYS` (not a hard-coded `2`). Current computed depth = **2** (EDD=1). A file `f` can carry retained rows up to SQLDATE `f+EDD`; coverage of `s` needs support through `s+EDD`, so block `b` is final once source dates through `b+2*EDD` are final (i.e., current present file `g >= b + 2*EDD`). Blocks also release at the terminal flush when forward support is out-of-window/sealed.
- **Retained-offset guard** (§4.4): any retained row with `SQLDATE - source_file_date > ELIGIBILITY_DELTA_DAYS` raises `RetainedOffsetHardFail` (terminal; offending file/date/offset named; not streamed, not dropped, not a gap, no completed archive). Lower-bound eligibility is unchanged (`date_eligibility_failure`). Byte-equivalence is required only on the valid domain (retained offsets `<= EDD`); the guard is a hard-fail improvement for the previously-inconsistent `> EDD` domain.
- **Bounded memory** (§4.5): only the rolling file-block buffer streams; high-water = `2*EDD + 1 = 3` blocks, recorded as `max_buffered_source_file_blocks` and asserted independent of window length (30-day and 120-day fixtures both = 3). The whole-window `classify_retained` / `primary_rows` lists are removed from the real path.
- **Terminal post-loop flush** (§4.6): remaining held blocks released in order; the final boundary's forward support is out-of-window/sealed (e.g., decade `2022-12-30` covered, `2022-12-31` edge-excluded; April `…-30` edge-excluded). No final buffered file dropped.
- **Coverage / gap / integrity / exact-58 unchanged** (§4.7–4.9): states `covered`/`edge-excluded`/`gap-uncovered` via the production oracle `archive.fetched_set_fully_covers`; `hard-fail finding` is terminal abort only; mutual-absence-only tolerated gaps; single-manifest-only → `IntegrityManifestError`; listed fetch/verify/cache failures stay hard fail-closed and are never reclassified as gaps; exact-58 zero-tolerance `ColumnLayoutHardFail` fires per file before that file's block is buffered/released.
- **Atomic output** (§4.10): rows stream to `…ttg_approved_fields_archive.csv.partial`; promoted via `os.replace` to the final path only after the build completes; the provenance manifest is written to `…json.partial` and promoted only after the archive is promoted. Any hard-fail/interrupt (`except BaseException`) closes the writer and publishes NO final archive/manifest; the un-promoted partial temp stays gitignored/untracked. Empty/all-gap build matches the existing serializer's header-only bytes exactly.
- **Byte-identical order** (§4.11): file-block order = source-file processing order; within-block order = classifier order; coverage filtering does not reorder; no per-SQLDATE grouping. Proven byte-for-byte vs a test-local accumulate reference. (The real `c077edc6…` April reproduction is a later real-contact run, after this clears.)
- **Public shape preserved** (§4.12): the return dict and provenance manifest keep all prior keys (`primary_covered_sqldates`, `fetched_dates`, `tolerated_source_gaps`, `ledger_covered_sqldates`, `ledger_edge_excluded_sqldates`, `ledger_gap_uncovered_sqldates`, `coverage_ledger`, `slice_edge_incomplete_sqldates`, `window_edge_incomplete_days`, `reconcile_status`, `archive_artifact`, `manifest`/`manifest_path`, `boundary_declarations`, …), computed from incremental counters/streamed-write counters/date-indexed ledger/source-date state — not from whole-window lists. Aggregate counters are now surfaced explicitly (`agg_raw_rows`, `agg_date_eligibility_failure`, `agg_edge_window_exclusion`, `agg_classify_retained`, `primary_archive_rows`, `archive_sha256`) plus `max_buffered_source_file_blocks` and `streaming_release_depth` (additive — no existing key changed).
- The synthetic/legacy harness `run_phase2_archive_build` (not real-fetch capable; small synthetic inputs only) is out of scope and unchanged; the streaming fix targets the real build path `run_bounded_integrity_build`.

## Tests (synthetic only; suite-wide no-network backstop active)
```
python3 -m pytest -q tests/test_lane2_type_tone_goldstein_streaming_writer.py   -> 18 passed
python3 -m pytest -q tests/ -k "streaming or gap_tolerance or type_tone_goldstein" -> 130 passed, 1141 deselected
python3 -m pytest -q tests/ -k lane2                                            -> 675 passed, 596 deselected
```
Environment: Python 3.8.2, pytest 8.3.5. Coverage of §5: byte/order equivalence over offsets {-1,0,+1} (§5.1); release depth derived from EDD (§5.2); offset `> EDD` hard-fail (§5.3); bounded buffer high-water = 3, length-independent (§5.4); terminal flush (§5.5); interior gap fan-out `{2017-05-04..06}` named (§5.6); edge exclusions same mechanism (§5.7); all-gap header-only byte identity vs `write_approved_archive_csv([])` (§5.8); hard-fail mid-stream → no final archive/manifest (§5.9); listed integrity failure hard fail (§5.10); single-manifest-only abort (§5.11); exact-58 hard fail [35/45/59] (§5.12); per-row short-row guard distinct (§5.13); public return/provenance shape incl. no-gap `04-02…04-29` happy path (§5.14); `local_archive.py` unchanged SHA (§5.15); no production whole-window accumulator in the real path; no-network backstop (§5.16).

## Firewall confirmations
No push; gate `False` in worktree and committed bytes (never armed); no network/GDELT contact; no real archive build / April run / decade run; no extraction/feature/statistics; no outcome/join/market reads; no V1/V2; no 2023+ contact; no value artifacts staged or committed; `local_archive.py` byte-identical; no memory update.
