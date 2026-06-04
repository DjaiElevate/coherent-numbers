# Lane 2 TTG local approved-fields archive — Phase 1 conformance report v0.1

## Status

**Phase 1 implementation / conformance only — SYNTHETIC TESTS ONLY.**
No network contact. No GDELT contact. No real archive build. No TTG
extraction. No join. This report records the creation of the Phase-1
scaffold and the adversarial synthetic tests required *before* any future,
separately-authorized real GDELT fetch can be considered.

Governing design memo:
`docs/lane2_type_tone_goldstein_local_approved_fields_archive_design_memo_v0.1.md`
(content SHA-256 `c97e5593f5fa607f91ab8fb4a3a7e07c13efd6e385219f87431caedfd36abc99`,
DRAFT-LOCKED, NOT SETTLED). The memo authorizes no network, no archive
execution, no extraction, and no join; this Phase-1 turn authorizes none
of those either.

## Files created

- `src/lane2_type_tone_goldstein_local_archive.py` — pure parse / filter /
  structural-manifest logic + the by-construction network boundary.
- `scripts/run_lane2_type_tone_goldstein_local_archive_build.py` — guarded
  thin CLI runner (no network code).
- `tests/test_lane2_type_tone_goldstein_local_archive.py` — 19 adversarial
  synthetic-fixture tests.
- `docs/lane2_type_tone_goldstein_local_archive_phase1_conformance_report_v0.1.md`
  — this report.

## Test command and result

```
python3 -m pytest -q tests/test_lane2_type_tone_goldstein_local_archive.py
...................                                                      [100%]
19 passed in 0.11s
```

Environment: Python 3.8.2, pytest 8.3.5.

## Guard name

`TYPE_TONE_GOLDSTEIN_LOCAL_ARCHIVE_BUILD_AUTHORIZED = False` (ships False,
in `src/lane2_type_tone_goldstein_local_archive.py`). The conceptual
three-part run gate is: module constant True **AND** CLI flag
`--authorize-local-archive-build` **AND** env
`LANE2_TTG_LOCAL_ARCHIVE_BUILD_AUTHORIZED=1`.

## Network impossible by construction in Phase 1

The module imports **no** network library (`urllib`, `requests`, `socket`,
`http.client`). There is no opener, URL fetch, or HTTP helper anywhere in
the module or runner. The sole acquisition entrypoint is a bare hard-error
stub, `_phase1_fetch_disabled`, which raises `Phase1NetworkNotAuthorized`
with the exact message:

`NETWORK NOT AUTHORIZED IN PHASE 1`

**Even with all three guards flipped** (module constant monkeypatched True,
CLI flag passed, env var set), `run_local_archive_build` still hard-errors
at the acquisition step with that exact message, and a spy confirms no
opener / socket / fetch object is constructed
(`test_all_guards_flipped_still_network_hard_error`). Therefore **Phase 2
network enablement requires a reviewed code change** that adds a network
path — not a flag, env, or constant flip.

## Value-blind guarantees tested

- The structural manifest carries structural metadata only: approved
  schema (names/types), source date universe, per-file status, row counts,
  SHA-256 hashes, output artifact paths, code version/commit placeholder,
  boundary declarations.
- No value-level summary is computed or emitted: no distribution,
  histogram, mean, median, min, max, correlation, z-score, per-date
  aggregate, sample row, or example. Asserted by
  `test_manifest_has_no_value_summary_keys` and
  `test_manifest_is_structural_only`.
- **Adversarial extreme / value-rich fixture**: approved-field values
  `goldsteinscale=-9.8765`, `avgtone=-87.654321`, `nummentions=987654`
  appear **only** inside the approved-field archive rows (the archive
  itself), and **never** in the manifest or emitted text
  (`test_extreme_values_not_in_manifest`).
- SHA-256 hashes are explicitly allowed as structural integrity addresses,
  not value summaries, and are not misclassified as leaks
  (`test_sha256_is_structural_and_present`).

## 2023+ enumeration-before-open tested

`enumerate_source_universe` hard-errors (`Post2022SealBreach`) on any
candidate date `> 2022-12-31` **before any payload is opened or parsed**.
A spy proves no file/opener is touched after a 2023+ seal breach
(`test_2023plus_enumeration_hard_errors`, `test_spy_no_post2022_file_opened`).
Content-row 2023+ SQLDATE is rejected as defense-in-depth.

## Forbidden-field drop tested

GDELT rows may transiently contain forbidden columns (EventCode /
EventBaseCode / EventRootCode, actor, location, SOURCEURL, market /
outcome / `next_session_return` sentinels). Only the five approved fields
(date/SQLDATE, QuadClass, GoldsteinScale, AvgTone, NumMentions) are
retained; forbidden sentinels never appear in the parsed rows, the archive
output, or the manifest. Asserted across the plain-TSV and ZIP payload
paths (`test_forbidden_fields_dropped_from_parsed_rows`,
`test_archive_output_contains_no_forbidden_fields`,
`test_zip_payload_path_also_drops_forbidden`).

## No value-summary artifacts / logs emitted

The module emits no value-summary artifact and no value-summary log line.
Only structural metadata and the approved-fields archive (which is the
archive, not a summary) are produced. Tests write only under pytest
`tmp_path`; no real `results/` artifact is created
(`test_writes_only_under_tmp_path`).

## GDELT 1.0 positional schema note (V2 deferred to Phase 2)

The approved-field column indices used to read synthetic fixtures
(SQLDATE=1, QuadClass=29, GoldsteinScale=30, NumMentions=31, AvgTone=34)
reflect the documented GDELT 1.0 Event layout. Phase 2's V2 schema
verification must confirm these positions — and the exact
date / information-date field locked by `294494a` — against a committed
codebook reference **before** any real fetch.

## Boundaries that remain in force

- Future **real archive-build authorization is still required** (separate
  prompt): this Phase-1 turn authorizes no network, no archive execution,
  no extraction, no join.
- **Phase 2 network enablement requires a reviewed code change**, not just
  flag/env/constant changes.
- Join remains blocked. 2023+ remains sealed. TTG extraction remains
  unauthorized.
