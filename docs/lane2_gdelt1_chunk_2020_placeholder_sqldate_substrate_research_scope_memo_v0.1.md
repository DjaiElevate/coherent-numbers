# Lane 2 — GDELT1 chunk_2020 Placeholder-SQLDATE Substrate Research — Scope-Design Memo (v0.1)

## 1. Status / scope

This memo is a **scope-design memo only**. It does not authorize, initiate,
or perform any research. It does not contact GDELT, read any payload, run
the production runner, amend `SENTINEL_SQLDATES`, edit any test, archive any
halt diagnostic, or modify memory. It is explicitly:

- **not** data contact / no GDELT fetch
- **not** payload inspection
- **not** runner invocation
- **not** runner amendment
- **not** a `SENTINEL_SQLDATES` extension
- **not** a test edit
- **not** an archive write
- **not** a chunk_2020 retry / second attempt
- **not** a commit / push (commit/push is a separate sub-cycle)
- **not** a memory update
- **not** merge / Step 2 / market-data / instrument-construction work

No live retrieval, no GDELT contact, no runner invocation, no
output-directory creation, no archive write, and no memory edit has occurred
or is authorized by the act of writing this memo. The memo's sole purpose is
to **decide the scope of the next substrate research cycle** before any data
contact or runner amendment.

## 2. Current canonical state

HEAD = origin/main = `649ada3f7cf8165dd123a0045ea1594fd1369af3` (short
`649ada3`). Ahead/behind versus `origin/main` is 0 0. Tracked tree clean
(working tree contains only untracked artifacts including the chunk_2020
halted output directory, paper LaTeX intermediates, build outputs under
`results/`, archive/, and one each untracked draft / report; none of these
are repo state).

Lineage tail through `649ada3`:

- `c89625385103872c4b2a774bec51767ca62d143d` (short `c896253`) — chunk_2020
  execution-authorization planning memo committed (memo file SHA-256
  `cb9e51c3ee0b63ac7f986af357a9eb2e45089c10ea661572ec5ebd51291001f3`)
- `dd7cb06785d18d6c00b3e87749bdec66e4256f35` (short `dd7cb06`) — chunk_2020
  halted first-attempt enable commit (one-line `FULL_BUILD_AUTHORIZED = False
  → True` at line 95)
- `649ada3f7cf8165dd123a0045ea1594fd1369af3` (short `649ada3`) — chunk_2020
  halted first-attempt restore commit (one-line `FULL_BUILD_AUTHORIZED = True
  → False` at line 95); runner blob restored to
  `a1a10994d183b70bb4dfdcec9a981013a5857e10`

The chunk_2020 halt diagnostic remains in the live output location:

- `results/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/halt_diagnostic.json`
  SHA-256 **`a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`**

All five program guards remain false; all `LANE2_*_AUTHORIZED` shell
environment variables remain unset:

- `src/lane2_gdelt1_count_feasibility.py:647`
  `REAL_RETRIEVAL_ENABLED = False`
- `scripts/run_lane2_gdelt1_count_feasibility.py:49`
  `COUNT_FEASIBILITY_AUTHORIZED = False`
- `scripts/run_lane2_gdelt1_event_file_probe.py:52`
  `EVENT_FILE_PROBE_AUTHORIZED = False`
- `scripts/run_lane2_gdelt1_row_date_characterization.py:57`
  `ROW_DATE_CHARACTERIZATION_AUTHORIZED = False`
- `scripts/run_lane2_gdelt1_full_daily_count_build.py:95`
  `FULL_BUILD_AUTHORIZED = False`

Path (b) cycle counter at the chunk_2020 halted-lineage memory-update
boundary is **68** and is unchanged by this memo (memo creation is not a
memory-update boundary).

## 3. Halt evidence summary

The chunk_2020 first-attempt fresh execution under the post-amendment runner
regime HALTED on the very first daily file (`2020-01-01`) at runner-recorded
UTC `2026-05-26T16:47:48.524952+00:00`, after ~1.24 s of wall-clock activity:

- chunk_id: `chunk_2020`
- halted on: `2020-01-01` daily file (first scheduled URL)
- `actual_completed_file_count`: **0 / 366**
- halt class: `FullBuildBoundaryBreach`
- halt message: *"unexpected offset -36524 in payload nominally dated
  2020-01-01: SQLDATE 1920-01-02"*
- exit code: 1
- stderr: single line above; stdout empty
- output directory:
  `results/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/`
- output artifacts: only `halt_diagnostic.json` (320 B; SHA-256
  `a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`); **no**
  `chunk_contributions.csv`, **no** `chunk_metadata.json`, **no**
  `chunk_summary.md` were produced because halt occurred before any aggregate
  computation or metadata generation

Empirical implications of the halt's structural shape:

- The halt was triggered by a **single row** in the `2020-01-01` daily file
  whose `SQLDATE` parsed to `1920-01-02`. The runner correctly computed the
  offset as `(date(1920, 1, 2) - date(2020, 1, 1)).days = -36524 days`.
- `-36524` is outside `EXPECTED_OFFSETS = (-3650, -365, -30, -7, -1, 0, 1)`.
- `1920-01-02` is **NOT** in the current `SENTINEL_SQLDATES = (date(1920, 1,
  1),)`. Per the runner's R3 + Option α logic, only sentinel-set values are
  routed to per-sentinel diagnostics and excluded from primary aggregates;
  all other values whose offset falls outside `EXPECTED_OFFSETS` halt the
  run.
- The halt fired on the **first encounter** of the unexpected offset; the
  runner did not attempt to continue, did not silently expand the sentinel
  set, and did not silently widen `EXPECTED_OFFSETS`. This is exactly the
  §9.A failure rule of the committed chunk_2020 planning memo
  (`cb9e51c3…001f3`).

Because no `chunk_metadata.json` was produced before the halt:

- chunk_2020's **6th fetch-gap empirical-validation surface remains
  DEFERRED**. The fields `known_substrate_gap_dates` and
  `substrate_gap_dates_not_fetched` are not observable from this aborted
  run, and the 4 / 4 pattern confirmation remains pending a future
  successful chunk_2020 fresh-attempt under a further-amended runner regime.
- The known-substrate-gap dates (the canonical 2014 four-date list) are
  **not** under question at this halt; the fetch-gap mechanism and the
  in-file sentinel/placeholder mechanism are two distinct mechanisms (Section
  9 of the chunk_2020 planning memo's locked taxonomy) and must continue to
  be reported separately.

## 4. Prior R3 + Option α assumption status

Distinguish two classes of prior assertions: assumptions that are now
empirically disputed by the chunk_2020 halt, and design properties that are
validated by the way the halt actually fired.

### 4.1 Now empirically disputed

- **T1 — one-off isolated anomaly** (the assumption that the placeholder-row
  phenomenon affected only a single nominal file date). Now **disputed**:
  the affected nominal file dates include at least:
  - `2019-12-31` (chunk_2019 fresh-attempt closure: 120 rows with SQLDATE
    `1920-01-01`)
  - `2020-01-01` (this chunk_2020 halt: at least 1 row with SQLDATE
    `1920-01-02`)
- **S1 — single sentinel SQLDATE value** (the assumption that
  `SENTINEL_SQLDATES = (date(1920, 1, 1),)` was sufficient). Now
  **disputed**: the placeholder-dated SQLDATE values include at least:
  - `1920-01-01` (chunk_2019 closure; confined to `2019-12-31`)
  - `1920-01-02` (this chunk_2020 halt; observed in `2020-01-01`)

These disputed properties do **not** by themselves authorize any runner
amendment, any extension of `SENTINEL_SQLDATES`, or any chunk_2020 retry.
They only define what the next substrate research cycle must clarify.

### 4.2 Validated by the halt's structural behavior

- **Halt-on-other-unexpected** behavior fired correctly on the first
  encountered non-sentinel non-`EXPECTED_OFFSETS` row.
- **No silent `SENTINEL_SQLDATES` expansion**: the runner did not add
  `1920-01-02` to the sentinel set at runtime; the sentinel set remained
  exactly `(date(1920, 1, 1),)`.
- **No silent `EXPECTED_OFFSETS` widening**: the canonical tuple
  `(-3650, -365, -30, -7, -1, 0, 1)` was not modified at runtime.
- **R3 + Option α discovery-preservation property held verbatim**: a
  newly-encountered structural anomaly produced an explicit halt and a
  forensic diagnostic, not a silent extension of the recognized envelope.

These validated properties are load-bearing for the next research cycle:
the runner's behavior is **trustworthy as a probe-by-halting mechanism** for
detecting further placeholder-dated values, but the runner cannot be the
research tool itself because each new value will halt it before producing
metadata. Research must use a separate read-only path that does not invoke
the production runner.

## 5. Candidate research scopes

The substrate research must distinguish three hypotheses:

- **H1 — isolated adjacency**: `1920-01-02` is a second isolated
  placeholder value adjacent to `1920-01-01`, with no broader family. Under
  H1 the future `SENTINEL_SQLDATES` extension would add exactly one value
  (`date(1920, 1, 2)`) and no more.
- **H2 — narrow family**: placeholder values cluster in early 1920, e.g.
  `1920-01-XX` through part or all of January 1920, or a small `1920-01-*`
  range. Under H2 the future `SENTINEL_SQLDATES` extension would add a
  bounded date range (e.g. all `1920-01-01..1920-01-31` or a verified subset).
- **H3 — broader envelope**: placeholder values span a wider structural
  envelope, such as the full year `1920`, other `*-01-*` calendar months,
  year-boundary files, or a structural placeholder mechanism keyed to file
  boundaries / publication-cycle metadata rather than to specific dates.
  Under H3 the future `SENTINEL_SQLDATES` mechanism may need a different
  shape (e.g. a date-range tuple, a callable predicate, or a structural
  classifier) rather than a discrete `Tuple[date, ...]`.

### Option A — tight scope

- Inspect only the `2020-01-01` daily file (if and when later authorized).
- Characterize **all** placeholder-dated SQLDATEs within that single file:
  unique values, per-value row counts, distribution of offsets vs the
  nominal file date.
- Determine whether `1920-01-02` is the only non-canonical SQLDATE inside
  that file, or whether there are additional placeholder values clustered
  within the same file.
- Lowest research budget.
- **Strength**: minimal data contact; cheap; fastest to schedule.
- **Weakness**: tests H1 only at the level of the single halted file;
  cannot distinguish whether `1920-01-02` is isolated *across files* or
  part of a cross-file family. Cannot reach H2 or H3 directly. If H1 is
  rejected (i.e. additional placeholder values found inside the single
  file), the result still does not characterize H2 / H3.

### Option B — bounded early-1920 family scope

- Inspect the `2020-01-01` daily file **plus** a bounded set of additional
  daily files designed to test the H2 hypothesis.
- Proposed bounded inspection envelope (to be confirmed in the later
  substrate research prompt, not authorized here):
  - the `2020-01-01` halted file itself
  - a bounded set of cross-chunk daily files most likely to surface
    `1920-01-XX` placeholder rows — candidates include the `2019-12-31`
    file (chunk_2019 sentinel surface), year-boundary files (`*-12-31`,
    `*-01-01`) across the daily window, and a small sample of mid-month
    files inside chunks 2020 / 2021 / 2022 to act as control negatives
- For each file inspected, characterize:
  - unique non-canonical SQLDATE values
  - per-value row counts
  - whether the placeholder-set differs by file or is uniform
- **Strength**: distinguishes H1 vs H2 directly; gives signal on whether
  the placeholder family is narrow (H1/H2) or broader (early H3 indicators).
  Higher signal-per-budget than Option A.
- **Weakness**: bounded; will not by itself rule out H3 in its strongest
  forms (e.g. structural placeholder mechanism keyed to non-date metadata).
  Requires a careful pre-registered envelope to avoid scope creep.

### Option C — broader envelope scope

- Inspect a wider envelope sufficient to test H3 directly. Candidates
  include the full 1920 calendar across all daily files, all year-boundary
  files across the full daily window, or a structural enumeration of all
  files whose recognized-list metadata indicates atypical structure.
- For each file, compute the same placeholder distribution as Option B.
- **Strength**: strongest against H3; produces the most comprehensive
  empirical picture in a single pass.
- **Weakness**: highest budget; highest scope-creep risk; likely
  over-fetches relative to the evidence needed for a runner amendment;
  risks conflating sentinel-handling with fetch-gap diagnostics across many
  files at once; risks contaminating future chunk_2020-onwards fresh-attempt
  outputs if the inspection mechanism is later mis-attributed as
  exploratory data preservation.

## 6. Recommended scope

**Recommendation: Option B — bounded early-1920 family scope**, with a
strict pre-registered envelope and an explicit deferral of H3 expansion
unless evidence from the bounded stage justifies it.

Rationale (consistent with the chunk_2019 substrate-amendment cycle
discipline `7206e30 → d99a210`):

- Option A is **insufficient** because the chunk_2020 halt has already
  demonstrated that the phenomenon spans at least two distinct nominal
  file dates (`2019-12-31` and `2020-01-01`). The minimum research question
  is now cross-file, not within-file.
- Option C is **premature**. The discovery-preservation property combined
  with the runner's halt-by-default behavior means that any future
  placeholder-value discovery will surface naturally at the next fresh
  chunk_2020 fresh-attempt run. Pre-emptively running a broad sweep before
  the bounded stage's evidence is in hand inverts the discipline.
- Option B is **sized to the disputed properties**: T1 is disputed across
  ≥2 file dates, and S1 is disputed across ≥2 values. The bounded envelope
  is sized to characterize the immediate-neighborhood cluster (the `1920-XX`
  vicinity, including year-boundary files plausibly carrying the same
  publication-cycle placeholder mechanism) without committing to the full
  H3 envelope.

The bounded envelope's **sufficiency criteria**:

- if Option B's inspection finds that all placeholder values across the
  bounded set fall within `1920-01-01..1920-01-02` only, H1 is supported
  (isolated adjacency confirmed across the bounded envelope)
- if Option B's inspection finds that placeholder values span a continuous
  early-January-1920 range (e.g. `1920-01-01..1920-01-31` or any
  contiguous subset thereof) on multiple nominal file dates, H2 is
  supported
- if Option B's inspection finds placeholder values that fall outside
  early January 1920 (e.g. `1920-02-XX`, `1920-XX-XX`, or non-1920
  placeholder values), **H3 expansion is triggered** and a separately
  scoped Option-C research prompt becomes the next eligible step

The bounded envelope's **insufficiency criteria**:

- the placeholder distribution within the bounded envelope is
  structurally ambiguous (e.g. mixed signal that cannot distinguish H2
  from H3); a second-stage research prompt would be required before any
  amendment memo can be drafted

## 7. Future research prompt shape

The future substrate research prompt — separately authorized, **not**
authorized by this memo — must specify:

- **Allowed data sources**: the daily event-file payloads at the bounded
  envelope of dates specified by the research prompt. The recognized-list
  capture at `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json`
  (SHA-256 `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`)
  remains the canonical recognized-list authority; the research prompt
  must not modify this artifact or its sidecar.
- **Exact file/date envelope**: the bounded set of daily file dates to
  inspect, enumerated explicitly (no ambiguous "etc."). The envelope must
  include the `2020-01-01` halted file and the `2019-12-31` chunk_2019
  sentinel-surface file at minimum; additional bounded year-boundary
  files and a small in-month control set must be pre-registered before
  any data contact.
- **Exact fields to extract from each row**: SQLDATE, file-nominal date,
  computed offset. No other GDELT fields should be extracted; the research
  scope is sentinel-placeholder characterization only, not topical
  inspection.
- **Counts to report per file**:
  - total parsed rows
  - per-SQLDATE row counts (full distribution)
  - per-offset row counts
  - identified placeholder-SQLDATE rows (those whose offset is outside
    `EXPECTED_OFFSETS` and whose SQLDATE is not already in
    `SENTINEL_SQLDATES`)
  - identified canonical sentinel rows (those whose SQLDATE is in
    `SENTINEL_SQLDATES`)
- **Cross-file placeholder distribution**:
  - unique placeholder SQLDATE values across the bounded envelope
  - per-value row count totals
  - affected nominal file dates per placeholder value
  - first / last file-nominal date on which each placeholder value
    appears
- **Family-classification question to answer**:
  - is the placeholder set isolated (H1), narrow (H2), or broader (H3)
  - if H3-triggering values appear, name them explicitly
- **Production runner non-invocation**: the research must use a separate
  read-only inspection path. The production runner
  `scripts/run_lane2_gdelt1_full_daily_count_build.py` must **not** be
  invoked, because the halt-on-other-unexpected behavior will block it on
  any non-sentinel placeholder row before metadata can be written. The
  research path may be a separate one-off script, a notebook, or a
  manually-driven inspection — but it must **not** flip
  `FULL_BUILD_AUTHORIZED`, set any `LANE2_*_AUTHORIZED` env var, or modify
  the production runner.
- **No runner amendment during research**: the research prompt must not
  edit the runner, the tests, or the canonical config.
- **No silent `SENTINEL_SQLDATES` extension**: the research prompt must
  not modify the sentinel set; any extension is a separate downstream
  amendment cycle.
- **No archive write during research**: the chunk_2020 halt diagnostic
  remains in the live output location until the separately scoped
  archival sub-cycle.
- **No memory update during research execution**: research findings are
  recorded in a research-output memo and committed in a separate sub-cycle.
- **Boundary preservations**: 7-item non-weakening canon (no-retry /
  exactly-once / no-off-session / no-market-data / no-Step-2 /
  no-checkpoint-resume / no-bounded-parallelism); no merge; no 2023+
  access; no instrument construction; no Step 2; no market-data work.

## 8. Decision boundaries

The bounded research stage will produce one of four classified outcomes:

| Outcome | Evidence supports | Next sub-cycle |
|---|---|---|
| **D1 — isolated second value** | H1: only `1920-01-01` and `1920-01-02` appear across the bounded envelope | Draft substrate amendment memo proposing `SENTINEL_SQLDATES` extension to include `(date(1920, 1, 1), date(1920, 1, 2))` only |
| **D2 — narrow January-1920 family** | H2: placeholder values fall within a contiguous early-January-1920 range across multiple file dates | Draft substrate amendment memo proposing `SENTINEL_SQLDATES` extension to include the verified date range; consider whether tuple-of-discrete-dates remains the appropriate runner data shape or whether a range/predicate representation is needed |
| **D3 — broader placeholder envelope** | H3: placeholder values fall outside early January 1920 | **Do not** draft a substrate amendment memo yet; instead schedule a separately scoped Option-C broader-envelope research prompt; the runner-data-shape question (discrete tuple vs range vs predicate vs structural classifier) becomes load-bearing and must be answered before amendment |
| **D4 — insufficient evidence** | bounded envelope produces structurally ambiguous signal | Schedule a second-stage bounded research prompt with a refined envelope; no amendment memo yet |

**Default precedence (set here at the scope-design layer)**: `D3 ⪼ D2 ⪼ D1`;
`D4` applies only when `D1`, `D2`, and `D3` are each individually
inconclusive. That is: `D3` overrides `D2` and `D1` whenever any
broader-envelope evidence (values outside early January 1920) appears,
even if a narrow early-January-1920 cluster is also present in the data;
`D2` overrides `D1` whenever a contiguous early-January-1920 family is
present without broader-envelope evidence; `D1` applies only to the
strict isolated-adjacency case (exactly `1920-01-01` and `1920-01-02`,
no other placeholder values anywhere in the bounded envelope); `D4`
applies only when the bounded envelope produces structurally ambiguous
signal that cannot resolve `D1`, `D2`, or `D3` individually. This
default precedence handles the mixed-signal edge case where a
continuous early-January-1920 cluster co-occurs with one or more values
outside the early-January-1920 range (literally satisfies both `D2` and
`D3` under their isolated readings) — under this rule the mixed case
classifies as `D3`, triggering Option-C expansion rather than a
premature narrow-family amendment.

The research prompt **must pre-register** these four outcomes and the
deterministic precedence among them, per Discipline (diagnostic outcome
precedence) — when multiple outcomes could fire simultaneously, the
research prompt must declare which outcome takes precedence. The
research prompt may refine the precedence above, but it may not weaken
it: any refinement must continue to enforce `D3 ⪼ D2 ⪼ D1` and the
restriction of `D4` to genuinely inconclusive cases.

## 9. Amendment boundary

Runner amendment is **not** authorized by this scope memo and is **not**
authorized by the future substrate research prompt itself.

A separate **substrate amendment memo** must be drafted after research
results are in hand, analogous to the chunk_2019 substrate amendment cycle
which produced:

- `7206e30` — Lane 2 sentinel SQLDATE substrate amendment memo (recorded)
- `d99a210` — Lane 2 sentinel SQLDATE recognition (R3 + Option α) runner
  amendment commit

The post-chunk_2020-halt amendment cycle must follow the same lifecycle:

1. ⏸️ Substrate research (this memo's downstream) — bounded inspection
   under Option B
2. ⏸️ Substrate amendment memo (analogue of `7206e30`) — records empirical
   findings, proposes runner-data-shape decisions if needed, classifies
   outcome D1 / D2 / D3 / D4
3. ⏸️ Runner amendment commit (analogue of `d99a210`) — implements the
   `SENTINEL_SQLDATES` extension (or structural reshaping) per the
   amendment memo with direct-substrate-evidence justification
4. ⏸️ Post-amendment memory update
5. ⏸️ chunk_2020 post-amendment planning addendum (if planning gaps
   surface; analogue of `437e7e9`)
6. ⏸️ chunk_2020 fresh-attempt execution authorization (treated as
   **fresh attempt under a further-amended runner regime**, NOT a retry of
   the now-canonically-closed halted first attempt at enable `dd7cb06` /
   restore `649ada3`)

The non-retry canon is preserved: the chunk_2020 halted first attempt is
canonically closed and any future chunk_2020 execution will be a fresh
attempt under a further-amended runner regime, not a retry of the halted
run.

## 10. Archive boundary

The chunk_2020 halt diagnostic at
`results/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/halt_diagnostic.json`
(SHA-256 `a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`)
**remains in the live output location** during this scope-design memo
draft and during the future substrate research cycle. Archival to
`archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/`
is a **separately scoped future sub-cycle**, mirroring the chunk_2019
halted first attempt arc where the halt diagnostic at
`archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2019_20260525T192552Z/halt_diagnostic.json`
(SHA-256 `3b2b43708d0a7a9410d59a7bfd4deec7fef84f8a6543472f25942e67e1058005`)
was archived as a separate operation after the substrate-amendment cycle
had progressed.

The live halt diagnostic must remain untouched during scope design and
during the bounded research cycle: it is forensic evidence of the
original halt and its byte-identity must be preserved for cross-check
against the future research's findings.

## 11. Next frontier

After this scope-design memo draft, the next eligible sub-cycle is **not**
research execution. The chunk-level planning-and-execution discipline
established through chunks 2013_partial → 2019 prescribes the following
sequence:

1. ✅ **Scope-design memo creation** — completed by this turn's draft
2. ⏸️ **Scope-design memo content review / sanity-check** (separately
   scoped; awaits explicit user initiation)
3. ⏸️ Scope-design memo commit + push (separately scoped; not authorized
   by this memo's creation)
4. ⏸️ *(optional)* Scope-design-closure memory update (separately scoped)
5. ⏸️ Substrate research prompt under the recommended Option B bounded
   envelope (separately scoped; uses read-only inspection path, not the
   production runner; pre-registers D1 / D2 / D3 / D4 outcomes per
   Section 8)
6. ⏸️ Substrate research execution
7. ⏸️ Substrate research output memo (records D1 / D2 / D3 / D4
   classification with full placeholder distribution)
8. ⏸️ Substrate amendment memo (analogue of `7206e30`)
9. ⏸️ Runner amendment commit (analogue of `d99a210`)
10. ⏸️ Post-amendment memory update
11. ⏸️ chunk_2020 post-amendment planning addendum (if needed)
12. ⏸️ chunk_2020 fresh-attempt execution authorization
13. ⏸️ chunk_2020 enable/restore lineage push
14. ⏸️ chunk_2020 execution-closure memory update
15. ⏸️ Halt diagnostic archival to `archive/halted_attempts/...`
    (separately scoped, at the user's choice of timing within the cycle)

No live execution, no runner amendment, no `SENTINEL_SQLDATES` change, no
archive write, no commit, no push, and no memory update is authorized by
this scope-design memo creation. The memo is a planning artifact only.
Pause: await explicit next prompt.
