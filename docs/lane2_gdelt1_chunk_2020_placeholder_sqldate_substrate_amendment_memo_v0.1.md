# Lane 2 — GDELT1 chunk_2020 Placeholder-SQLDATE Substrate Amendment Memo (v0.1)

## 1. Status / scope

This is a **substrate amendment memo draft only**. It records the
amendment decision for the chunk_2020 placeholder-SQLDATE finding,
specifies the recommended `SENTINEL_SQLDATES` extension, and prepares
the downstream runner amendment commit — **without** implementing the
runner change itself.

This memo is explicitly:

- **not** a runner edit
- **not** a `SENTINEL_SQLDATES` change (the runner's tuple at line 136
  remains `(date(1920, 1, 1),)` throughout this memo turn)
- **not** an `EXPECTED_OFFSETS` change
- **not** a chunk_2020 retry or second attempt
- **not** an archive move (the chunk_2020 halt diagnostic remains
  live in its output location)
- **not** a memory update
- **not** a commit / push (commit/push is a separate sub-cycle)
- **not** an execution prompt
- **not** a GDELT fetch
- **not** a payload re-inspection
- **not** a test edit
- **not** merge / Step 2 / market-data / instrument-construction work

The memo is the chunk_2020 analogue of the chunk_2019 substrate
amendment memo at commit `7206e30` — it **records the design**; the
**runner amendment** (analogue of `d99a210`) is a separately scoped
downstream commit that this memo does not perform.

## 2. Precedent and lineage

Authority and lineage anchors for this memo:

- **chunk_2019 substrate amendment memo** at commit
  **`7206e30d865b379c16b3655d7a908114dbb99a16`** (short `7206e30`);
  established the R3 + Option α framework (sentinel-SQLDATE recognition
  + per-sentinel diagnostics + halt-on-other-unexpected preservation +
  `EXPECTED_OFFSETS` invariance under sentinel-set extension); single
  sentinel value `date(1920, 1, 1)` recommended at that cycle.
- **chunk_2019 runner amendment commit**
  **`d99a2100f20f2bd87984a6ea1627a98576a6ed9f`** (short `d99a210`);
  implemented `SENTINEL_SQLDATES: Tuple[date, ...] = (date(1920, 1, 1),)`
  at runner line 136 and the R3 + Option α parse-loop branch; produced
  the current canonical post-amendment runner blob
  `a1a10994d183b70bb4dfdcec9a981013a5857e10` (unchanged throughout this
  research cycle).
- **chunk_2020 scope-design memo** at commit
  **`a34d1ffcc2d4cfecb447ba45911f13b89a755656`** (short `a34d1ff`);
  pre-registered the Option B bounded-envelope research design + the
  `D3 ⪼ D2 ⪼ D1` precedence; file SHA-256
  `842e558840cee0177885f2c81eaac6a1c504a09405ad57d94a9cc7baa58427c2`.
- **chunk_2020 D2 research output memo** at commit
  **`dc48f55ae06af3e5cc439b92d3245974933edb09`** (short `dc48f55`);
  recorded the D2 — narrow early-January-1920 family classification +
  the amendment direction (§10) that this memo now formalizes; file
  SHA-256 `1b2e76d8bd4bba62764c06d675c6ffb870a76636498a6f202f371d61a7f9719a`.
- **chunk_2020 halt diagnostic** (forensic evidence; remains live, not
  archived):
  `results/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/halt_diagnostic.json`
  SHA-256 **`a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`**;
  halt class `FullBuildBoundaryBreach`; halt message *"unexpected
  offset -36524 in payload nominally dated 2020-01-01: SQLDATE
  1920-01-02"*.
- **chunk_2020 halted lineage** on `origin/main`: enable
  `dd7cb06785d18d6c00b3e87749bdec66e4256f35` → restore
  `649ada3f7cf8165dd123a0045ea1594fd1369af3` (canonically closed).

Lineage relationship: this memo is the **chunk_2020 substrate amendment
memo** drafted **before** the chunk_2020 runner amendment commit.
Mirroring the chunk_2019 sequence:

```
chunk_2019: 7206e30 (substrate amendment memo) → d99a210 (runner amendment commit)
chunk_2020: <this memo, when committed>         → <future runner amendment commit, analogue of d99a210>
```

Repo state at memo creation: HEAD = origin/main =
`dc48f55ae06af3e5cc439b92d3245974933edb09`; ahead/behind = 0 0; tracked
tree clean; runner blob `a1a10994d183b70bb4dfdcec9a981013a5857e10`; all
five guards `False`; `LANE2_*_AUTHORIZED` envs unset;
`SENTINEL_SQLDATES = (date(1920, 1, 1),)` at runner line 136;
`EXPECTED_OFFSETS = (-3650, -365, -30, -7, -1, 0, 1)` at runner
line 120.

## 3. Empirical evidence basis

This amendment is grounded entirely in **direct substrate evidence**
from the Option B bounded-envelope substrate research executed under
the scope-design memo `a34d1ff` and recorded in the research output
memo `dc48f55`. No prediction, no theoretical extension, no
speculative envelope.

Research execution summary (committed at `dc48f55`; full per-file
detail in committed memo and uncommitted research output directory):

- Bounded-envelope size: **23** pre-registered nominal file dates
- Inspected: **23 / 23** (zero target failures)
- Wall-clock window UTC: `2026-05-26T21:04:31.299014+00:00 →
  2026-05-26T21:05:19.918737+00:00`
- Total runtime: ~48.6 s (~2.1 s/URL)
- Production runner **not** invoked
- Guards not flipped; `LANE2_*_AUTHORIZED` envs not set
- `SENTINEL_SQLDATES` not modified during research
- `EXPECTED_OFFSETS` not modified during research
- Raw payloads not preserved
- URL authority: recognized-list capture at SHA
  `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`

Cross-envelope aggregate counts:

| metric | count |
|---|---:|
| `total_rows_parsed` | **3,245,764** |
| `total_expected_offset_rows` | **2,709,690** (83.5%) |
| `total_canonical_sentinel_rows` (`1920-01-01`) | **87,765** |
| `total_placeholder_candidate_rows` | **448,309** |
| `total_malformed_rows` | **0** |
| `total_unparseable_sqldate_rows` | **0** |

Affected nominal file dates: **6** — `2019-12-31`, `2020-01-01`,
`2020-01-02`, `2020-01-03`, `2020-01-04`, `2020-01-05` (canonical
sentinel ∪ placeholder candidate union; the prior research execution
report's "7 affected file dates" was an off-by-one text error and is
resolved by §4 of the committed D2 research output memo at line 132 +
correction-instruction at line 158; this amendment memo uses 6, not 7,
as the canonical count and does not propagate the "7" claim).

Distinct placeholder/sentinel SQLDATE values: **6** — `1920-01-01`
(canonical sentinel, 87,765 rows) + `1920-01-02`..`1920-01-06`
(placeholder candidates):

| SQLDATE | classification | total rows | n affected file dates |
|---|---|---:|---:|
| `1920-01-01` | canonical sentinel | 87,765 | 3 |
| `1920-01-02` | placeholder candidate | 121,054 | 3 |
| `1920-01-03` | placeholder candidate | 153,580 | 3 |
| `1920-01-04` | placeholder candidate | 110,228 | 3 |
| `1920-01-05` | placeholder candidate | 63,362 | 2 |
| `1920-01-06` | placeholder candidate | 85 | 1 |

D2 classification (final): **D2 — narrow early-January-1920 family**
under committed precedence `D3 ⪼ D2 ⪼ D1`. D3 NO (no value outside
`1920-01-01..1920-01-16`); D2 YES (contiguous range across multiple
file dates); D1 NO (set larger than isolated adjacency); D4 NO (D2
individually conclusive).

Parser cross-check: the 2019-12-31 canonical sentinel count observed
in this research (**120 rows**) exactly reproduces the chunk_2019
fresh-attempt closure observation
(`sentinel_sqldate_distribution = {'1920-01-01': {'2019-12-31': 120}}`).
This validates the standalone research parser's parse-path
correctness against the production runner's parse path for the known
sentinel surface — a load-bearing cross-check for any downstream
amendment decision because the runner amendment must operate on the
same parse path that produced the observed evidence.

Research artifact SHA-256 forensic anchors (all uncommitted; the
research output directory remains the canonical evidence substrate):

| Artifact | SHA-256 |
|---|---|
| `inspection_script.py` | `41e7fef8ffec3a11fafc08348a64bbee66398edac6618413353250e22b16f86e` |
| `inspection_log.txt` | `f819538540d280db4032d18bf1191ead30861388fea175f612cab793f9883642` |
| `research_metadata.json` | `6d9eba5a158cacb84d4c319ecaf2cc528adfdd4b461554339503657c7656a54a` |
| `target_dates_manifest.json` | `fc4cdb340f2cf4c99b0ea847d27a7781133b1a4c3acd9a4bb907eb9c8096a259` |
| `placeholder_sqldate_observations.csv` | `627c7979808a202999f205d4acb5612074a537d9c89ea5af87acf43aae6ba7d2` |
| `placeholder_sqldate_summary.json` | `e639117e9048cf8b6c8049790daef1349a5cf66401eb246e002581fcaa40289e` |
| `placeholder_sqldate_summary.md` | `184d472d883f87c08703a3d04b1b3fdafbde2d9d08b2cfe3872a9c31e10e0dab` |

## 4. Assumption status update

The chunk_2019 substrate amendment memo (`7206e30`) recorded two
pre-execution assumptions about the placeholder-row phenomenon. The
chunk_2020 D2 research conclusively resolves them.

| Assumption | Pre-research status | Post-research status |
|---|---|---|
| **T1** — one-off isolated anomaly (single affected nominal file date) | recorded under chunk_2019 closure; "disputed" after chunk_2020 halt | **decisively disputed**: **6** affected nominal file dates (canonical sentinel ∪ placeholder candidate union) |
| **S1** — single sentinel SQLDATE value (`1920-01-01` only) | recorded under chunk_2019 closure; "disputed" after chunk_2020 halt | **decisively disputed**: **6** distinct `1920-01-XX` values, contiguous |

Validated by the structural behavior of the chunk_2020 halt and the
Option B research:

- **Halt-on-other-unexpected** fired correctly on the first
  encountered non-sentinel non-`EXPECTED_OFFSETS` row at chunk_2020
  production-runner execution. This is the discovery-preservation
  mechanism that surfaced the new placeholder values; it must remain
  load-bearing after the amendment.
- **No silent `SENTINEL_SQLDATES` expansion**: the runner did not
  silently add `1920-01-02..1920-01-06` at runtime; the sentinel set
  remained exactly `(date(1920, 1, 1),)` throughout the halt and the
  research cycle.
- **No silent `EXPECTED_OFFSETS` widening**: the canonical tuple
  remained `(-3650, -365, -30, -7, -1, 0, 1)` throughout.
- **R3 + Option α discovery-preservation property** held verbatim:
  newly-encountered values produced an explicit halt and forensic
  diagnostic, not a silent extension of the recognized envelope.
- **`EXPECTED_OFFSETS` invariance under sentinel-set extension** is
  preserved by this amendment design: the recommended amendment
  (§5) modifies `SENTINEL_SQLDATES` only.

The R3 + Option α framework established at the chunk_2019 cycle
(`7206e30 → d99a210`) is **not weakened** by this amendment; it is
**applied with an updated sentinel-set** that reflects the additional
direct substrate evidence.

## 5. Amendment decision

**Recommended amendment: discrete-tuple extension of `SENTINEL_SQLDATES`
to the six directly-observed values.**

Proposed final tuple at runner line 136:

```python
SENTINEL_SQLDATES: Tuple[date, ...] = (
    date(1920, 1, 1),
    date(1920, 1, 2),
    date(1920, 1, 3),
    date(1920, 1, 4),
    date(1920, 1, 5),
    date(1920, 1, 6),
)
```

Properties of the recommendation:

- **6-value set**: one existing canonical sentinel + five new
  directly-observed placeholder values
- **5-value extension** beyond the current singleton
  `(date(1920, 1, 1),)`
- **Discrete tuple**: preserves the existing
  `SENTINEL_SQLDATES: Tuple[date, ...]` data shape; no
  runner-data-shape change
- **Evidence-bounded**: every added value has been directly observed
  in the substrate (`placeholder_sqldate_observations.csv` records
  row-level observations for all five new values across affected file
  dates `2020-01-01..2020-01-05`)
- **No predicate**: the recommendation does **not** introduce a
  predicate-shaped recognizer (no year-shift, no
  `*-01-*`-shaped rule, no offset-based recognizer)
- **No date range**: the recommendation does **not** introduce a
  range-shaped representation (no `(start_date, end_date)` form, no
  `SENTINEL_SQLDATE_RANGES` parallel structure)
- **Future placeholder values are NOT pre-included**: `date(1920, 1, 7)`
  is **not** in the recommended tuple because `1920-01-07` was not
  directly observed in the bounded research envelope; any future
  encounter with `1920-01-07` (or any other not-yet-observed
  placeholder value) must still trigger halt-on-other-unexpected and
  motivate a separately scoped substrate amendment

No `EXPECTED_OFFSETS` change is recommended. No chunk-definition
change is recommended. No market-data / Step 2 / merge boundary
change is recommended.

**This memo does not implement the runner change.** The amendment
decision is recorded here; the runner edit is a separately scoped
downstream commit (analogue of `d99a210`).

## 6. Why discrete tuple, not range/predicate

The recommendation rests on five evidence-bounded properties that
discrete-tuple extension satisfies and that range/predicate
alternatives do not.

### 6.1 Discrete tuple is most evidence-bounded

Every added value (`1920-01-02`, `1920-01-03`, `1920-01-04`,
`1920-01-05`, `1920-01-06`) has been directly observed in the
substrate with row-level evidence in
`placeholder_sqldate_observations.csv`. The recommendation contains
**zero predicted values** and **zero values added on theory alone**.

### 6.2 It preserves the current data shape

The runner's `SENTINEL_SQLDATES: Tuple[date, ...]` declaration at
line 136 is unchanged in shape. The runner's R3 + Option α parse-loop
branch at the equivalent of chunk_2019 amendment commit `d99a210`'s
sentinel-routing code (currently `if d in SENTINEL_SQLDATES:`) is
unchanged in shape; the `in` membership check works verbatim for a
6-value tuple.

### 6.3 It minimizes runner-code change

The downstream runner amendment commit (analogue of `d99a210`) will
modify exactly one tuple literal at runner line 136. Comments
referencing the sentinel-set narrative (e.g. runner lines 122-135)
may need updating to reflect the multi-value empirical basis; the
parse-loop semantics need no change.

### 6.4 It avoids silently recognizing unobserved values

A date-range representation would silently pre-include any
`1920-01-N` value not yet directly observed (e.g. `1920-01-07`). The
no-silent-expansion discipline established at chunk_2019
(`7206e30` §6 substrate anomaly taxonomy refinement; §11 recommended
substrate interpretation) explicitly requires direct substrate
evidence for sentinel-set inclusion. A range would violate this
discipline by construction.

A year-shift predicate would silently recognize any SQLDATE whose
year is `1920` while the nominal file year is `2020` — including
values such as `1920-07-15` in a `2020-07-15` file, which have
**never been observed** in the substrate. The bounded broader-envelope
controls in the Option B research (`2020-01-31`, `2020-02-01`,
`2020-03-01`, `2020-06-15`, `2020-09-01`, `2020-12-31`) all show
**zero placeholder/sentinel rows**, so the predicate has zero direct
substrate support beyond the early-January-1920 cluster.

### 6.5 It preserves future halt/discovery behavior

After the discrete-tuple extension, the halt-on-other-unexpected
behavior continues to fire on any SQLDATE outside `SENTINEL_SQLDATES`
whose offset is outside `EXPECTED_OFFSETS`. In particular:

- `date(1920, 1, 7)` in any future fetched file → halt (good;
  surfaces a new substrate question that would motivate a separately
  scoped research cycle and a fresh amendment memo)
- any `1920-02-*` / `1920-07-*` / non-1920 placeholder-like value →
  halt (good; same discipline)
- any genuinely unexpected SQLDATE → halt (good; the
  discovery-preservation property is the load-bearing mechanism that
  surfaced the present amendment)

A range or predicate would silently absorb these cases and **erase
the discovery-preservation signal** that the chunk_2019 cycle
explicitly preserved.

### 6.6 Range and predicate are deferred, not refuted

If a future broader-envelope research cycle (Option C) directly
observes substrate evidence that:

- placeholder values form a stable contiguous range with empirically
  bounded endpoints (e.g. all of `1920-01-01..1920-01-31` observed
  across an envelope wider than the present one), **or**
- placeholder values follow a year-shift structural rule with direct
  evidence in non-January files (e.g. observed `1920-07-15` in
  `2020-07-15`),

then a future substrate amendment memo could revisit the data-shape
question with evidence in hand. This memo does **not** rule out those
designs in principle; it rules them out **as the default amendment**
given current evidence.

## 7. Runner amendment implications

The downstream **runner amendment commit** (separately scoped;
analogue of `d99a210`) implementing this memo's decision should:

### 7.1 Required edits

- Update `SENTINEL_SQLDATES` at
  `scripts/run_lane2_gdelt1_full_daily_count_build.py:136` to the
  6-value tuple specified in §5
- Update the sentinel-set narrative comments at the equivalent of
  runner lines 122-135 to reflect the multi-value empirical basis
  (cite this memo + the D2 research output memo + the research output
  directory as evidence anchors)
- Update inline references that describe the empirical basis of
  `SENTINEL_SQLDATES` (single-value → 6-value, with appropriate
  affected-file-date count = 6 and the corrected error-correction
  note)

### 7.2 Boundaries the runner amendment MUST preserve

- **`EXPECTED_OFFSETS` unchanged** (`(-3650, -365, -30, -7, -1, 0, 1)`
  at line 120 — load-bearing for discovery preservation)
- **`KNOWN_SUBSTRATE_GAPS` unchanged** (fetch-gap mechanism is
  structurally distinct from the in-file sentinel mechanism per the
  locked taxonomy)
- **`CHUNK_IDS` unchanged** (no chunk-definition change)
- **`EXPECTED_CHUNK_COUNTS` unchanged** (`chunk_2020 = 366` at
  line 1615; the amendment does not change URL-set semantics)
- **`CHUNK_YEAR_RANGES` unchanged**
- **`RECOGNIZED_LIST_SHA256` constant unchanged** (recognized-list
  authority preserved)
- **`FULL_BUILD_AUTHORIZED = False` at line 95** (the runner amendment
  commit is a recorded-state change; chunk_2020 retry is a separate
  fresh-attempt execution authorization)
- **No market-data access change**
- **No Step 2 retirement**
- **No merge change**
- **No 2023+ access change**
- **No instrument construction**

### 7.3 Tests the runner amendment should add

The runner amendment commit should include unit/integration tests
covering at least:

- All six sentinel SQLDATEs recognized: parse a synthetic payload
  containing exactly one row per each of `1920-01-01..1920-01-06`
  with offset values outside `EXPECTED_OFFSETS`; assert each row is
  routed to `per_sentinel_count` / `sentinel_sqldate_distribution`,
  excluded from primary aggregates, and does **not** trigger
  `FullBuildBoundaryBreach`
- Unexpected non-sentinel offsets still halt: parse a synthetic
  payload containing a row with SQLDATE `1920-01-07` (or any other
  `1920-01-*` value not in the extended tuple) and offset outside
  `EXPECTED_OFFSETS`; assert `FullBuildBoundaryBreach` is raised with
  the canonical halt message shape
- 2019-12-31 / 2020-01-01 / early-January cases behave as expected:
  parse synthetic payloads mirroring the per-file row counts from
  `placeholder_sqldate_summary.json` per_file entries; assert
  aggregate counts match per-file canonical-sentinel /
  placeholder-candidate totals (using the recommended 6-value tuple)
- `EXPECTED_OFFSETS` invariance: assert
  `EXPECTED_OFFSETS == (-3650, -365, -30, -7, -1, 0, 1)` at parse
  time and at completion

**This memo does not implement any of these tests.** Test
implementation is part of the downstream runner amendment commit and
is not authorized by this memo.

### 7.4 Forensic preservation under the runner amendment

The chunk_2020 halt diagnostic at SHA
`a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`
must remain byte-identical after the runner amendment commit. The
runner amendment does **not** rewrite, move, or modify the live halt
diagnostic. Archival is a separately scoped sub-cycle (§9).

## 8. Fresh-attempt framing

A future chunk_2020 execution under the post-runner-amendment regime
must be **a fresh attempt under a further-amended runner regime** —
**not** a retry of the now-canonically-closed halted first attempt
(enable `dd7cb06785d18d6c00b3e87749bdec66e4256f35` → restore
`649ada3f7cf8165dd123a0045ea1594fd1369af3`).

Specifically the fresh-attempt execution must preserve:

- **No retry**: the halted first attempt remains canonically closed;
  any future chunk_2020 run starts from a clean recognized-list
  manifest, not from partial halted state
- **No checkpoint resume**: there is no partial state to resume from;
  the halted attempt's output directory contains only the halt
  diagnostic (no `chunk_metadata.json`, no `chunk_contributions.csv`,
  no `chunk_summary.md` were produced)
- **No reuse of partial halted state**: the halt diagnostic at
  `chunk_2020_20260526T164747Z/halt_diagnostic.json` is **forensic
  evidence only** — not a resume anchor, not a recovery state
- **Exactly-once fetch semantics**
- **Same-session execution**
- **No off-session continuation**
- **No bounded parallelism**

The fresh-attempt execution authorization is a separately scoped
prompt that this memo does not authorize.

## 9. Archive boundary

The chunk_2020 halt diagnostic at
`results/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/halt_diagnostic.json`
(SHA-256
`a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`)
**remains live and unarchived** during this memo turn, the future
content-review turn, the future commit + push turn, the future
post-amendment-memo memory update, the future runner amendment commit,
the future post-runner-amendment memory update, and any subsequent
chunk_2020 fresh-attempt sub-cycle.

Archival to
`archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/`
is a **separately scoped future sub-cycle**, mirroring the chunk_2019
halted first-attempt arc where the halt diagnostic at
`archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2019_20260525T192552Z/halt_diagnostic.json`
(SHA-256
`3b2b43708d0a7a9410d59a7bfd4deec7fef84f8a6543472f25942e67e1058005`)
was archived as a separate operation after the substrate-amendment
cycle had progressed.

This memo does **not** authorize archive movement. The live halt
diagnostic must remain byte-identical throughout the amendment cycle.

## 10. Boundary preservation

This memo turn preserves all of the following:

- **No runner edit** — runner blob
  `a1a10994d183b70bb4dfdcec9a981013a5857e10` unchanged
- **No `SENTINEL_SQLDATES` change yet** — the runner's tuple at
  line 136 remains `(date(1920, 1, 1),)`
- **No `EXPECTED_OFFSETS` change** — the runner's tuple at line 120
  remains `(-3650, -365, -30, -7, -1, 0, 1)`
- **No chunk_2020 retry / second attempt**
- **No production runner invocation**
- **No GDELT fetch**
- **No archive write** — halt diagnostic byte-identical at SHA
  `a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`
- **No memory update** — `MEMORY.md` and
  `project_lane2_attention_spike.md` SHAs preserved across this
  memo-draft turn
- **No commit / no push**
- **No merge**
- **No Step 2 retirement / no market-data work / no instrument
  construction**
- **No `chunk_2021` / `chunk_2022` work**
- **No test edits**
- **No planning-memo / addendum / scope-memo / research-output-memo
  edits beyond pre-existing state**
- **No tags, no branches, no force-push, no hook bypass**
- chunk_2019 closure remains canonically closed and untouched
- chunk_2020 halted lineage (`dd7cb06 → 649ada3`) remains canonically
  closed and untouched

## 11. Next frontier

After this substrate amendment memo draft, the next eligible
sub-cycle is **not** runner amendment. The sub-cycle sequence is:

1. ✅ **Substrate amendment memo creation** — completed by this turn's
   draft
2. ⏸️ **Substrate amendment memo content review / sanity-check**
   (separately scoped; awaits explicit user initiation)
3. ⏸️ Substrate amendment memo commit + push (separately scoped; not
   authorized by this memo's creation)
4. ⏸️ Post-substrate-amendment-memo memory update (separately scoped)
5. ⏸️ **Runner amendment commit** (analogue of `d99a210`) implementing
   the discrete-tuple extension per §5 + the test additions per §7.3
   + the boundary preservations per §7.2
6. ⏸️ Post-runner-amendment memory update (updates the canonical
   runner-blob SHA anchor; current
   `a1a10994d183b70bb4dfdcec9a981013a5857e10` → new post-amendment
   blob SHA, which is **not** known until the runner amendment commit
   is performed)
7. ⏸️ chunk_2020 post-amendment planning addendum (if planning gaps
   surface relative to the chunk_2020 planning memo at `c896253` and
   its post-amendment addendum-precedent at `437e7e9`; analogue of
   the chunk_2019 `437e7e9` addendum)
8. ⏸️ chunk_2020 fresh-attempt execution authorization (treated as a
   **fresh attempt under a further-amended runner regime**, **NOT** a
   retry of the canonically-closed halted first attempt at enable
   `dd7cb06` / restore `649ada3`)
9. ⏸️ chunk_2020 enable/restore lineage push
10. ⏸️ chunk_2020 execution-closure memory update
11. ⏸️ Halt diagnostic archival to
    `archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/`
    (separately scoped, at the user's choice of timing)

No live execution, no runner amendment, no `SENTINEL_SQLDATES`
change, no archive write, no commit, no push, and no memory update is
authorized by this substrate amendment memo creation. The memo is a
planning / decision-record artifact only. Pause: await explicit next
prompt.
