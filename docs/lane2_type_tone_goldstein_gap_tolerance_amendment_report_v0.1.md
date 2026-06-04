# Lane 2 / Type-Tone-Goldstein — no-network gap-tolerance amendment report v0.1

`CODE-ONLY, NO-NETWORK, VALUE-BLIND, GATE-CLOSED AMENDMENT — gap-tolerant manifest reconciliation + unified support-aware coverage; source gate remains False; no extraction; no push`

This amendment makes the GDELT 1.0 archive fetch/build path tolerate
**mutual manifest-attested source absence** as a coverage gap (rather than aborting
the whole window), while keeping all integrity/format failures hard fail-closed. It
is a code change only — no network, no GDELT contact, no full-window build, no
extraction. The source gate is left disarmed.

## Preflight anchor
- HEAD before: `1698e868294e3423e9fba0aba735de44894d9337` (`1698e86`)
- parent: `effe8533…` (`effe853`)
- `origin/main`: `fb26424c…` (`fb26424`); ahead by 12, behind 0; no push.
- Source gate at HEAD: exactly one definition `REAL_FETCH_SOURCE_GATE_ENABLED = False` (L51); zero `= True`.
- Pre-existing untracked files (not part of this task, not opened, not staged): `docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md`, `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`.

## No-network / gate-closed statement
This amendment performed **no** network contact, **no** GDELT contact, **no** manifest/zip fetch, **no** real raw/cache/archive/result reads, **no** outcome/market/join reads, **no** V1/V2, **no** 2023+ contact, **no** extraction, and **no** feature/value computation. All tests use synthetic fixtures, injected seams, and committed code only, under a suite-wide no-network backstop. The source gate is and remains `False`.

## Fetch-module identity
- Old (bounded-run) fetch-module SHA-256: `c656614a160571be56305e87ed717e048a04066c3ade044411075ae4d3123d8d`
- New committed fetch-module SHA-256: `c0dfda3745b1254854d6118c1375a5d960bc13cbd9d54f13b140990bf5a7f439`

The new SHA is the protected fetch-module identity for the eventual decade run.

## Changed files
- `src/lane2_type_tone_goldstein_archive_fetch_path.py` (amendment logic)
- `tests/test_lane2_type_tone_goldstein_fetch_path.py` (exact-58 orchestration test re-pointed to the new terminal hard-fail)
- `tests/test_lane2_type_tone_goldstein_gap_tolerance.py` (new focused amendment suite)
- `docs/lane2_type_tone_goldstein_gap_tolerance_amendment_report_v0.1.md` (this report)

## Scope finding
`reconcile_universe_against_manifests` and `run_bounded_integrity_build` already live in `src/lane2_type_tone_goldstein_archive_fetch_path.py` (in scope). The **support/coverage convention** (`fetched_set_fully_covers`, `is_sqldate_fully_covered`, `row_is_eligible`, `ELIGIBILITY_DELTA_DAYS`, `WINDOW_START/END`) lives in the companion `src/lane2_type_tone_goldstein_local_archive.py`. Because the staging allow-list excludes `local_archive.py`, that module was **not** modified. The amendment implements the gap-fan-out ledger entirely in `archive_fetch_path.py`, reusing `local_archive.py`'s existing public primitives as the authoritative coverage oracle, and pins its support-set derivation to the production oracle by test (`test_support_set_pinned_to_production_oracle`) so it cannot drift. No production module beyond `archive_fetch_path.py` was edited.

## Manifest classification semantics (§4.1)
New pure helper `classify_manifest_presence(expected_filenames, md5sums, filesizes)` splits the authorized universe into:
- `present_in_both` — in `md5sums` AND `filesizes` → mandatory; full download/stable-retry/MD5/byte-size/cache verification still hard fail-closed.
- `absent_in_both` — in NEITHER → tolerated source gap; **not fetched**; dependent SQLDATEs ledgered `gap-uncovered` and excluded from the primary archive.
- `single_manifest_only` — in exactly one → manifest inconsistency/corruption → `IntegrityManifestError` **before** daily processing (NOT a tolerated gap).

Manifest parse/malformed manifests remain fail-closed (a truncated/garbage manifest yields no daily entries → dependent dates become single-manifest-only or absent, and any present-in-one inconsistency aborts).

## Fetch/verify/cache failures remain hard fail (§4.2)
For `present_in_both` dates the existing fail-closed exceptions are intact and never caught/converted to gaps: `IntegrityVerificationError` (MD5/byte-size), `UnstableDownloadError` (non-identical retry), `CacheIntegrityError` (cache re-verify). Test `test_listed_file_md5_failure_hard_fails_even_with_a_gap` proves a present-in-both integrity failure aborts even when another date in the same window is a tolerated gap.

## Unified support-aware coverage + gap fan-out (§4.3, §4.4)
ONE rule governs start-edge, slice-edge, and interior gaps. `classify_sqldate_coverage(sqldate, available, gaps)` delegates the covered/not decision to the production oracle `archive.fetched_set_fully_covers` and uses `sqldate_support_set(t) = {t-1, t, t+ELIGIBILITY_DELTA_DAYS}` (the production `source_file_date <= SQLDATE + 1` support set). A missing interior source file strands **every** SQLDATE whose support set includes it (fan-out), not just its own date.

Exact interior-gap fixture result (`test_interior_gap_fanout_exact_dependent_set`): with `2013-04-15` absent-in-both over the `2013-04-01…2013-04-30` window, the `gap-uncovered` set is exactly `{2013-04-14, 2013-04-15, 2013-04-16}` (derived from the production support function, asserted equal to the literal set), each excluded from primary with `20130415.export.CSV.zip` named as the cause; `2013-04-15` is never fetched.

Completed-build per-SQLDATE ledger vocabulary is exactly `covered` / `edge-excluded` / `gap-uncovered`.

Edge vs interior are the same mechanism (`test_edge_and_interior_gap_same_rule`): `2013-04-01`/`2013-04-30` resolve `edge-excluded`, `2013-04-15` resolves `gap-uncovered`, and the same oracle reports all three uncovered.

## `hard-fail finding` is terminal abort, not a per-SQLDATE label (§4.5)
A hard-fail finding (single-manifest-only, integrity failure, exact-58 file-level violation, manifest parse failure) raises before any archive/manifest write — no primary archive and no success manifest are produced, and the offending file/condition is named. It is never a fourth per-SQLDATE coverage label inside a produced archive.

## Exact-58 file-level hard fail (§4.6)
For every manifest-listed file processed under `enforce_exact_columns=True`, any column-count deviation raises `ColumnLayoutHardFail` (new), naming the offending source file and aborting before write — a non-58 file is never silently dropped and never becomes `gap-uncovered`. The pre-existing per-row approved-index / short-row guard remains a row-level structural drop reason (`short_row`) and is NOT a source-gap path (`test_per_row_short_row_guard_is_row_level_not_gap`).

## Degenerate all-gap window (§4.7)
A window entirely `absent-in-both` completes as a value-blind build with no primary rows, no fetch attempts, and every requested SQLDATE ledgered `gap-uncovered` (causing files named) — no abort solely because the archive is empty (`test_all_gap_window_completes_empty`).

## Suite-wide no-network backstop + production-logic testing (§6.1, §6.10)
The new amendment suite uses an autouse fixture that patches `_open_url` to raise and asserts the gate is `False`, so every amendment test runs with no network. Tests drive the **production** `classify_manifest_presence`, `classify_sqldate_coverage`, `sqldate_support_set`, and the full `run_bounded_integrity_build` build path — not copied/mock implementations; the support-set derivation is pinned to the production oracle.

## Test commands and outcomes
```
python3 -m pytest -q tests/test_lane2_type_tone_goldstein_gap_tolerance.py
12 passed

python3 -m pytest -q tests/test_lane2_type_tone_goldstein_fetch_path.py \
  tests/test_lane2_type_tone_goldstein_local_archive.py \
  tests/test_lane2_type_tone_goldstein_gap_tolerance.py
112 passed

python3 -m pytest -q tests/ -k "lane2"
657 passed, 596 deselected
```
Environment: Python 3.8.2, pytest 8.3.5.

## Gate grep evidence
Working tree and committed object both show exactly one definition `REAL_FETCH_SOURCE_GATE_ENABLED = False` (L51) and zero `REAL_FETCH_SOURCE_GATE_ENABLED = True`. (Other occurrences are docstring prose and `if`-checks, not definitions.) The committed-object grep is recorded in the post-commit section of the run and the byte-review bundle.

## Firewall confirmations
No extraction, no feature/value statistics, no outcome/join/market reads, no V1/V2, no 2023+ contact, no full-window build, no network/GDELT contact, no value artifacts staged or committed, no memory update, no push.
