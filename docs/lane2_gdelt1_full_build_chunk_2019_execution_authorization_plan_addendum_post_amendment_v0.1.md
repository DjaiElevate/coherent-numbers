# Lane 2 — GDELT1 Full Daily Count Build — chunk_2019 Execution-Authorization Plan — Post-Amendment Addendum (v0.1)

## 1. Status preamble

This is a **narrow governance-layer addendum** to the chunk_2019 planning
memo committed at `6c17850a065965acda8eacc014012f3721e407b4` (the original
memo, `docs/lane2_gdelt1_full_build_chunk_2019_execution_authorization_plan_v0.1.md`,
content SHA-256 `a091621418dac211567cd375d21dde9f2573aa99b8f237b98affcb02cd4c58d2`,
10,719 B, 284 lines). The original memo **remains valid** except where this
addendum introduces post-amendment clarifications.

This addendum **supersedes nothing** in the original memo. It exists solely
to formalize, for the upcoming chunk_2019 fresh attempt under the amended
runner regime: (i) the canonical-state advance since the original memo was
written, (ii) the runner-regime transition introduced by the runner
amendment at commit `d99a2100f20f2bd87984a6ea1627a98576a6ed9f`, (iii) the
R3 + Option α sentinel-handling semantics added by that amendment, (iv) the
updated row-arithmetic identity, (v) the new line anchors in the runner,
(vi) the terminology distinction between the canonically-closed first
chunk_2019 attempt and the upcoming fresh attempt, and (vii) the
unchanged carry-forward backlog plus the next eligible action.

**No retrospective reinterpretation** of prior completed chunks is implied
by anything in this addendum. Chunks `chunk_2013_partial` / `chunk_2014` /
`chunk_2015` / `chunk_2016` / `chunk_2017` / `chunk_2018` remain canonically
closed under the pre-amendment runner regime, with their existing
`chunk_metadata.json` aggregates valid under that runner.

This addendum is **memo-only**. It authorizes no runner edit, no chunk
execution, no chunk_2019 retry, no merge, no Step 2, no market-data work,
no instrument construction, no memory edit, no commit, and no push by
itself.

## 2. Updated canonical state and lineage

HEAD = origin/main = `d99a2100f20f2bd87984a6ea1627a98576a6ed9f` (short
`d99a210`). Ahead/behind versus `origin/main` is 0 0. Tracked tree clean.

Lineage extension since the original chunk_2019 planning memo at
`6c17850`:

`6c17850 → da68003 → 3595466 → 7206e30 → d99a210`

- `6c17850` — Add Lane 2 chunk_2019 execution-authorization plan (original memo, locked)
- `da68003` — Enable Lane 2 full-build chunk_2019 run (first-attempt enable; line-95 `False → True`)
- `3595466` — Restore Lane 2 full-build guard after chunk_2019 (first-attempt restore; line-95 `True → False`)
- `7206e30` — Record Lane 2 sentinel SQLDATE substrate amendment memo
- `d99a210` — Add Lane 2 sentinel SQLDATE recognition (R3 + Option α) (runner amendment)

**Runner-regime references:**

- Pre-amendment runner: commit `389747e`; runner blob SHA `0c022e36986891753507cc28fdba83d612a61390`; canonical for `chunk_2013_partial` through `chunk_2018` only.
- Post-amendment runner: commit `d99a2100f20f2bd87984a6ea1627a98576a6ed9f`; runner blob SHA `a1a10994d183b70bb4dfdcec9a981013a5857e10`; canonical for `chunk_2019` onward only.

## 3. Runner-regime transition

The runner amendment at `d99a210` introduced R3 + Option α sentinel
handling. This creates a hard transition in canonical scope:

| Chunk scope | Canonical runner commit | Canonical runner blob SHA |
|---|---|---|
| `chunk_2013_partial`, `chunk_2014`, `chunk_2015`, `chunk_2016`, `chunk_2017`, `chunk_2018` | `389747e` | `0c022e36986891753507cc28fdba83d612a61390` |
| `chunk_2019` (upcoming fresh attempt), `chunk_2020`, `chunk_2021`, `chunk_2022` | `d99a2100f20f2bd87984a6ea1627a98576a6ed9f` | `a1a10994d183b70bb4dfdcec9a981013a5857e10` |

The upcoming chunk_2019 fresh attempt will execute under the
**post-amendment runner blob** `a1a10994d183b70bb4dfdcec9a981013a5857e10`,
not the pre-amendment blob `0c022e36986891753507cc28fdba83d612a61390`.

The prior six chunks remain canonically closed under the pre-amendment
regime. Their `chunk_metadata.json` files were generated under the
pre-amendment runner and their `aggregate_metrics` semantics are bound to
that runner. The runner amendment does not invalidate them; the new
sentinel diagnostic counters would have been zero in the pre-amendment
fixture set (no sentinel SQLDATEs were observed in any of those six
chunks, per Prompt B's zero-fetch sentinel scan of all six prior year-end
files and per `actual_completed_file_count == expected_file_count` for
each completed chunk).

The upcoming chunk_2019 fresh attempt's enable-commit / restore-commit
byte-identity reference is the post-amendment blob, **not** `389747e`.

## 4. R3 + Option α integration

The runner amendment locked the following new semantics (substrate
amendment memo at commit `7206e30`, content SHA-256
`7aa96b73001623731849acd91981565828c4be63c4afb83d17b49dbf515161a5`):

- **New module-level constant** in the runner:
  `SENTINEL_SQLDATES: Tuple[date, ...] = (date(1920, 1, 1),)` (narrow seed, extensible shape).
- **Option α attribution**: rows whose parsed SQLDATE is in `SENTINEL_SQLDATES` are routed into per-sentinel diagnostics only; they are **excluded** from `total_in_window_rows` and `total_out_of_window_rows`.
- **Sentinel rows remain diagnostically visible** via three new fields surfaced in `aggregate_metrics`:
  - `total_sentinel_rows`
  - `per_sentinel_total: Dict[str, int]` (sentinel-ISO-date string → cumulative count across files)
  - `sentinel_sqldate_distribution: Dict[str, Dict[str, int]]` (sentinel-ISO-date → nominal-file-date-ISO → count)
- **Halt-on-other-unexpected behavior preserved**: any non-sentinel SQLDATE whose offset is outside `EXPECTED_OFFSETS = (-3650, -365, -30, -7, -1, 0, 1)` continues to raise `FullBuildBoundaryBreach`. `EXPECTED_OFFSETS` is unchanged. The discovery-preservation property is retained verbatim.

**Empirical expectation for the upcoming chunk_2019 fresh attempt.** The
2019-12-31 daily-export file is expected to contribute approximately
**120 sentinel-attributed rows** at `SQLDATE = 1920-01-01`, grounded in
the substrate-research chain:

- Prompt A: 120 rows observed in the 2019-12-31 file with SQLDATE 1920-01-01; structurally well-formed; modern URLs/GEIDs/actors; parser corruption ruled out.
- Prompt B: 1920-01-01 sentinel not observed in any of the 6 sampled within-2019 dates or in any of the 5 pre-2019 year-ends (S1: single sentinel value).
- Prompt C: outer-ZIP SHA `8017ad3872fc0b137384a2c6f92bd8367372c1b4530407dd6627fbb2baa67056` byte-stable across the Prompt A → Prompt C re-fetch interval; sentinel not observed in 2020/2021/2022 year-end files (T1: one-off isolated anomaly).

This expectation is **observational, not a hard pass/fail criterion**.
The fresh attempt's execution-closure stage should record the actual
observed `total_sentinel_rows`, `per_sentinel_total["1920-01-01"]`, and
`sentinel_sqldate_distribution["1920-01-01"]["2019-12-31"]` and note any
deviation from the expectation as a substrate-research signal (e.g., if
the GDELT source has changed in the inter-research interval, the count
may differ; if zero sentinel rows surface, that itself is a substrate
event worth recording). A deviation does **not** constitute a halt
condition; the runner amendment is correct regardless of the observed
count.

## 5. Updated row arithmetic identity

The original memo §10 stated the row arithmetic identity as:

> `total_in_window_rows + total_out_of_window_rows = total_parsed_rows`

This two-term identity is **superseded** under the amended runner regime
by the five-term identity that the amended runner's chunk-level
counting-invariant check now enforces:

```
total_in_window_rows
+ total_out_of_window_rows
+ total_sentinel_rows
+ total_malformed_short
+ total_unparseable_sqldate
= total_parsed_rows
```

This five-term identity applies **only under the amended runner regime**
(chunk_2019 onward). The pre-amendment chunk artifacts
(`chunk_2013_partial` through `chunk_2018`) remain valid under their
original two-term accounting semantics — their `chunk_metadata.json`
`aggregate_metrics` did not include `total_sentinel_rows` and were
generated under a runner where the term did not exist. **No retrospective
reinterpretation of those aggregates is implied.**

For the upcoming chunk_2019 fresh attempt, the execution-closure stage
must record all five terms explicitly and verify the identity holds.

## 6. Updated runner anchors

Verified positions in
`scripts/run_lane2_gdelt1_full_daily_count_build.py` under the
post-amendment runner blob `a1a10994d183b70bb4dfdcec9a981013a5857e10`:

| Anchor | Line | Status vs original memo |
|---|---|---|
| `FULL_BUILD_AUTHORIZED = False` | 95 | unchanged |
| `EXPECTED_OFFSETS: Tuple[int, ...] = (-3650, -365, -30, -7, -1, 0, 1)` | 120 | unchanged (value unchanged; line unchanged) |
| `SENTINEL_SQLDATES: Tuple[date, ...] = (date(1920, 1, 1),)` | 136 | **new** (introduced by the runner amendment) |
| `"chunk_2019",` (canonical chunk-list entry) | 1601 | content unchanged; shifted from line 1521 |
| `"chunk_2019": 365,` (`EXPECTED_CHUNK_COUNTS` entry) | 1614 | content unchanged; shifted from line 1534 |
| `"chunk_2019": (date(2019, 1, 1), date(2019, 12, 31)),` (`CHUNK_YEAR_RANGES` entry) | 1627 | content unchanged; shifted from line 1547 |

Predicted chunk_2020 anchor positions (informational, not yet executed):
**1602 / 1615 / 1628**. These predictions are derived from the +80-line
offset introduced by the SENTINEL_SQLDATES constant + parse_payload
sentinel branch and from the prior pre-amendment positions
1522/1535/1548. They are predictions and **must always be re-verified at
chunk_2020 planning preflight before reuse** — line numbers can shift
under any subsequent runner edit.

Line numbers in this addendum are accurate at the post-amendment runner
blob `a1a10994d183b70bb4dfdcec9a981013a5857e10`. They **must always be
re-verified before reuse in future prompts**; any future runner amendment
shifts them again.

## 7. Retry-vs-first-attempt terminology clarification

The chunk_2019 first attempt under the pre-amendment runner is
**canonically closed**:

- enable commit `da68003baf53bc663dfad5652836adb770de7a76`
- restore commit `3595466a1934b20c85c264451824e42bf1e374ad`
- both commits pushed to `origin/main` via fast-forward `6c17850..3595466 main -> main`
- halt diagnostic archived at `archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2019_20260525T192552Z/halt_diagnostic.json` (322 B; SHA-256 `3b2b43708d0a7a9410d59a7bfd4deec7fef84f8a6543472f25942e67e1058005`; `halt_class = FullBuildBoundaryBreach`; `actual_completed_file_count = 364 of 365`; halted on the 2019-12-31 file at offset −36524 / SQLDATE 1920-01-01)

The upcoming run is a **fresh attempt under the amended runner regime**,
not a retry of the first attempt:

- the first attempt is closed; its byte-identity reference was the
  pre-amendment blob `0c022e36…`; its outcome is canonically recorded as
  HALTED with the substrate-boundary-breach diagnostic preserved
- the upcoming attempt's byte-identity reference will be the
  post-amendment blob `a1a10994…`; its runner has different semantics
  (R3 + Option α sentinel handling); it cannot fail at the same
  substrate boundary because the amended runner now recognizes the
  1920-01-01 sentinel and routes it into diagnostics rather than raising
  `FullBuildBoundaryBreach`

**The 7-item non-weakening canon applies to the upcoming fresh attempt as
a single fresh attempt**:

1. **no-retry** — the upcoming run is the single attempt under the amended runner regime; it is not "retrying" the closed first attempt's output. There is no resume from the first attempt's partial state; the new attempt starts from a clean recognized-list manifest and processes all 365 chunk_2019 URLs.
2. **exactly-once** — exactly one live execution of the upcoming attempt; no second invocation.
3. **no-off-session execution** — the upcoming attempt's live command must be invoked in the authorized session.
4. **no-market-data** — preserved.
5. **no-Step-2** — preserved.
6. **no-checkpoint-resume** — the first attempt's archived halt diagnostic is for audit, not a checkpoint to resume from. The fresh attempt re-fetches the full chunk_2019 manifest from scratch.
7. **no-bounded-parallelism** — preserved.

These reaffirmations are not relaxations. The terminology distinction is
load-bearing because "retry under amended runner regime" is functionally
a different execution under a different byte-identity reference, not a
weakening of the no-retry rule that governs within-attempt behavior.

## 8. Carry-forward backlog and next frontier

**Carry-forward backlog (unchanged at this addendum):**

- Section 9 commit-report cosmetic observation — **5 cycles** unresolved, non-blocking.
- Substrate amendment memo Observation 1 — §9 R2 framing symmetry candidate (explicit "R3 strictly dominates R2 at zero implementation cost" sentence); current text is content-correct; carry-forward only.
- Substrate amendment memo Observation 2 — chunk_2018 in-window-row anchor `61,529,216` should be verified from `results/lane2_gdelt1_full_daily_count_build/chunk_2018_20260525T025641Z/chunk_metadata.json` `aggregate_metrics.total_in_window_rows` before reuse in any later decision-bearing artifact (e.g., the chunk_2019 fresh-attempt execution-closure memo).

No new carry-forward observations are introduced by this addendum.

**Next eligible action** after the addendum lifecycle (draft → content
review → commit/push → memory update) completes:

A separately authorized **chunk_2019 fresh-attempt authorization prompt
under the amended runner regime**. The authorization prompt must:

- reference the post-amendment runner commit `d99a2100f20f2bd87984a6ea1627a98576a6ed9f` and runner blob SHA `a1a10994d183b70bb4dfdcec9a981013a5857e10` as the new canonical byte-identity reference
- explicitly distinguish pre-amendment-anchored chunks (`chunk_2013_partial` through `chunk_2018`, anchored to commit `389747e` / blob `0c022e36986891753507cc28fdba83d612a61390`) from post-amendment-anchored chunks (`chunk_2019` onward, anchored to commit `d99a210` / blob `a1a10994d183b70bb4dfdcec9a981013a5857e10`)
- mirror the established **enable-commit / run / restore-commit lifecycle** (line-95 boolean flip `False → True` enable commit; live invocation under three-guard discipline; line-95 boolean flip `True → False` restore commit; both commits pushed as fast-forward)
- use the post-amendment blob as the byte-identity reference (`git diff --exit-code d99a210 -- scripts/run_lane2_gdelt1_full_daily_count_build.py` should exit 0 at sub-cycle entry and after the restore commit)
- preserve every item of the 7-item non-weakening canon and the full §9 boundary preservation list from the original memo
- **NOT** authorize `chunk_2020`, `chunk_2021`, `chunk_2022`, merge, Step 2, market-data work, or instrument construction

This addendum authorizes none of the above. It only formalizes the
governance layer that the chunk_2019 fresh-attempt authorization prompt
will draw on.
