# Lane 2 — GDELT1 chunk_2020 Placeholder-SQLDATE Research Output Memo (v0.1)

## 1. Status / scope

This is a **research output memo only**. It records the empirical findings
of the Option B bounded-envelope substrate research executed under the
committed scope-design memo, applies the pre-registered D1 / D2 / D3 / D4
classification under the committed `D3 ⪼ D2 ⪼ D1` precedence, and
prepares the downstream amendment direction without authorizing any
amendment.

This memo is explicitly:

- **not** a runner amendment
- **not** a `SENTINEL_SQLDATES` extension
- **not** an `EXPECTED_OFFSETS` widening
- **not** a chunk_2020 retry / second attempt
- **not** an archive move (the chunk_2020 halt diagnostic remains live in
  its output location)
- **not** a memory update
- **not** a commit / push (commit/push is a separate sub-cycle)
- **not** an execution prompt
- **not** a GDELT fetch
- **not** a payload re-inspection
- **not** merge / Step 2 / market-data / instrument-construction work

The memo is a planning artifact recording what was observed and what the
appropriate next sub-cycle should do.

## 2. Governance basis

Authority artifacts and lineage anchors for this memo:

- **Scope-design memo** at commit **`a34d1ffcc2d4cfecb447ba45911f13b89a755656`**
  (short `a34d1ff`); file path
  `docs/lane2_gdelt1_chunk_2020_placeholder_sqldate_substrate_research_scope_memo_v0.1.md`;
  SHA-256 **`842e558840cee0177885f2c81eaac6a1c504a09405ad57d94a9cc7baa58427c2`**
- **Committed precedence rule** (Section 8 of the scope-design memo):
  `D3 ⪼ D2 ⪼ D1`; `D4` applies only when `D1`, `D2`, and `D3` are each
  individually inconclusive. The research prompt may refine this
  precedence but may not weaken it.
- **chunk_2020 halt diagnostic** (forensic evidence; remains live, not
  archived):
  `results/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/halt_diagnostic.json`
  SHA-256 **`a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`**
- **Recognized-list authority** (URL-resolution authority used by the
  research script): `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json`
  SHA-256 `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`
- **chunk_2020 planning memo** at commit
  `c89625385103872c4b2a774bec51767ca62d143d` / SHA
  `cb9e51c3ee0b63ac7f986af357a9eb2e45089c10ea661572ec5ebd51291001f3`
  (recorded as the governance basis for the chunk_2020 execution
  lifecycle; its §9.A failure-rule discipline is the basis under which
  the halt fired correctly)
- **chunk_2020 halted lineage** on `origin/main`: enable
  `dd7cb06785d18d6c00b3e87749bdec66e4256f35` → restore
  `649ada3f7cf8165dd123a0045ea1594fd1369af3` (canonically closed)
- **Substrate amendment precedent** from chunk_2019 cycle: amendment memo
  `7206e30` → runner amendment commit
  `d99a2100f20f2bd87984a6ea1627a98576a6ed9f` (post-amendment runner blob
  `a1a10994d183b70bb4dfdcec9a981013a5857e10` — unchanged across this
  research cycle)

Research output directory:
`results/lane2_gdelt1_placeholder_sqldate_research/chunk_2020_option_b_20260526T210247Z/`

The seven research output artifacts and their SHA-256 values are:

| Artifact | SHA-256 |
|---|---|
| `inspection_script.py` | `41e7fef8ffec3a11fafc08348a64bbee66398edac6618413353250e22b16f86e` |
| `inspection_log.txt` | `f819538540d280db4032d18bf1191ead30861388fea175f612cab793f9883642` |
| `research_metadata.json` | `6d9eba5a158cacb84d4c319ecaf2cc528adfdd4b461554339503657c7656a54a` |
| `target_dates_manifest.json` | `fc4cdb340f2cf4c99b0ea847d27a7781133b1a4c3acd9a4bb907eb9c8096a259` |
| `placeholder_sqldate_observations.csv` | `627c7979808a202999f205d4acb5612074a537d9c89ea5af87acf43aae6ba7d2` |
| `placeholder_sqldate_summary.json` | `e639117e9048cf8b6c8049790daef1349a5cf66401eb246e002581fcaa40289e` |
| `placeholder_sqldate_summary.md` | `184d472d883f87c08703a3d04b1b3fdafbde2d9d08b2cfe3872a9c31e10e0dab` |

Repo state at memo creation: HEAD = origin/main =
`a34d1ffcc2d4cfecb447ba45911f13b89a755656`; ahead/behind = 0 0; tracked
tree clean; runner blob `a1a10994d183b70bb4dfdcec9a981013a5857e10`; all
five guards `False`; `LANE2_*_AUTHORIZED` envs unset;
`SENTINEL_SQLDATES = (date(1920, 1, 1),)` at runner line 136;
`EXPECTED_OFFSETS = (-3650, -365, -30, -7, -1, 0, 1)` at runner line 120.

## 3. Research execution summary

- Bounded-envelope size: **23** pre-registered nominal file dates
- Inspected: **23 / 23** (zero failures)
- Wall-clock window UTC: `2026-05-26T21:04:31.299014+00:00 →
  2026-05-26T21:05:19.918737+00:00`
- Total runtime: **~48.6 s** (~2.1 s/URL average)
- Standalone read-only inspection script:
  `results/lane2_gdelt1_placeholder_sqldate_research/chunk_2020_option_b_20260526T210247Z/inspection_script.py`
  (SHA-256 `41e7fef8ffec3a11fafc08348a64bbee66398edac6618413353250e22b16f86e`)
- Production runner **not** invoked at any point (verified via
  `research_metadata.production_runner_invoked = False`)
- Guard flips: **none** (`guards_flipped = False`)
- `LANE2_*` env vars: **unset** (`lane2_env_set = False`)
- `SENTINEL_SQLDATES` modifications: **none** (`sentinel_sqldates_modified
  = False`)
- `EXPECTED_OFFSETS` modifications: **none**
  (`expected_offsets_modified = False`)
- Raw payload preservation: **none**
  (`raw_payloads_preserved = False`); 23 GDELT daily event-file ZIPs
  were held in memory only during parse and freed before the next
  iteration; no `*.zip`, `*.gz`, or `*.export.CSV*` files exist under
  the output directory
- URL authority: all 23 target nominal file dates resolved through the
  recognized-list authority at SHA
  `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`
- No GDELT contact outside the pre-registered 23-date envelope
- No 2023+ files fetched
- No `chunk_2021` / `chunk_2022` files fetched

Cross-envelope aggregate counts (from
`placeholder_sqldate_summary.json` totals):

| metric | count |
|---|---:|
| `total_rows_parsed` | **3,245,764** |
| `total_expected_offset_rows` | **2,709,690** (83.5%) |
| `total_canonical_sentinel_rows` (`1920-01-01`) | **87,765** |
| `total_placeholder_candidate_rows` | **448,309** |
| `total_malformed_rows` | **0** |
| `total_unparseable_sqldate_rows` | **0** |
| `header_anomaly_detected` (any file) | **none** |

## 4. Corrected affected-file-date count

The research-execution report text contained an off-by-one error: it
stated "7 affected file dates" in two locations. The **correct
canonical count is 6**, computed as the union of nominal file dates
across the canonical_sentinel and placeholder_candidate distributions
in `placeholder_sqldate_summary.json`.

Verification (recomputed at this memo's preflight from artifacts):

- canonical-sentinel-affected dates:
  `2019-12-31`, `2020-01-01`, `2020-01-02` (3 dates)
- placeholder-candidate-affected dates:
  `2020-01-01`, `2020-01-02`, `2020-01-03`, `2020-01-04`, `2020-01-05`
  (5 dates)
- **union** = 6 dates: `2019-12-31`, `2020-01-01`, `2020-01-02`,
  `2020-01-03`, `2020-01-04`, `2020-01-05`

The six canonical affected nominal file dates are:

1. `2019-12-31`
2. `2020-01-01`
3. `2020-01-02`
4. `2020-01-03`
5. `2020-01-04`
6. `2020-01-05`

All downstream artifacts (this memo, any future amendment memo, any
future planning addendum, any future execution prompt, and any future
memory update) **must use 6, not 7**, as the canonical
affected-file-date count.

Note on terminology: the
`placeholder_sqldate_summary.json` field
`affected_nominal_dates_for_any_placeholder` is the
**placeholder-only** affected set (5 dates) and is not the union; the
canonical count for T1-dispute purposes is the union (6).

## 5. Per-file findings

Full per-file detail is available in
`placeholder_sqldate_summary.json` (`per_file` array) and
`placeholder_sqldate_observations.csv` (row-level observations for
all `canonical_sentinel`, `placeholder_candidate`, `malformed`, and
`unparseable_sqldate` rows; `expected_offset` rows are aggregated
only, not recorded row-by-row). The 23-file table is summarized below.
Files with zero non-expected rows are listed compactly.

Files containing canonical-sentinel and/or placeholder-candidate rows:

| nominal file date | rows | expected | canonical sentinel `1920-01-01` | placeholder candidates |
|---|---:|---:|---:|---|
| `2019-12-31` | 125,858 | 125,738 | **120** | 0 |
| `2020-01-01` | 89,215 | 1,876 | **87,241** | **98** (`1920-01-02`: 98) |
| `2020-01-02` | 123,425 | 2,597 | **404** | **120,424** (`1920-01-02`: 120,281; `1920-01-03`: 143) |
| `2020-01-03` | 157,403 | 3,542 | 0 | **153,861** (`1920-01-02`: 675; `1920-01-03`: 153,043; `1920-01-04`: 143) |
| `2020-01-04` | 112,518 | 2,140 | 0 | **110,378** (`1920-01-03`: 394; `1920-01-04`: 109,895; `1920-01-05`: 89) |
| `2020-01-05` | 112,046 | 48,498 | 0 | **63,548** (`1920-01-04`: 190; `1920-01-05`: 63,273; `1920-01-06`: 85) |

Files containing zero canonical-sentinel and zero placeholder-candidate
rows (clean):

- `2019-12-30` (118,132 rows; all `expected_offset`)
- `2020-01-06`..`2020-01-15` (10 mid-January continuity files; all
  `expected_offset`)
- `2020-01-31` (179,524; clean)
- `2020-02-01` (113,580; clean)
- `2020-03-01` (106,304; clean)
- `2020-06-15` (136,420; clean)
- `2020-09-01` (149,211; clean)
- `2020-12-31` (100,226; clean)

Total clean files: **17 / 23**. Total files with at least one
non-expected row: **6 / 23**.

## 6. Cross-file placeholder distribution

Unique `1920-01-XX` SQLDATE values observed across the bounded
envelope: **6** — one canonical sentinel (`1920-01-01`) and five
placeholder candidates (`1920-01-02` through `1920-01-06`).

| SQLDATE | classification | total rows | n affected file dates | affected file dates |
|---|---|---:|---:|---|
| `1920-01-01` | canonical sentinel | **87,765** | 3 | `2019-12-31`, `2020-01-01`, `2020-01-02` |
| `1920-01-02` | placeholder candidate | **121,054** | 3 | `2020-01-01`, `2020-01-02`, `2020-01-03` |
| `1920-01-03` | placeholder candidate | **153,580** | 3 | `2020-01-02`, `2020-01-03`, `2020-01-04` |
| `1920-01-04` | placeholder candidate | **110,228** | 3 | `2020-01-03`, `2020-01-04`, `2020-01-05` |
| `1920-01-05` | placeholder candidate | **63,362** | 2 | `2020-01-04`, `2020-01-05` |
| `1920-01-06` | placeholder candidate | **85** | 1 | `2020-01-05` |

Contiguity: the six-value `1920-01-XX` set is **contiguous** — every
integer day from `1920-01-01` through `1920-01-06` is represented; no
gaps. The set is fully contained within the pre-registered
early-January-1920 envelope `1920-01-01..1920-01-16`.

No placeholder candidate appears **outside** `1920-01-01..1920-01-16`
across any of the 23 files. The bounded broader-envelope controls
(`2020-01-31`, `2020-02-01`, `2020-03-01`, `2020-06-15`, `2020-09-01`,
`2020-12-31`) all show zero placeholder/sentinel rows. The mid-January
continuity files (`2020-01-06`..`2020-01-15`) also all show zero
placeholder/sentinel rows. The phenomenon is bounded both in
SQLDATE-space (within `1920-01-01..1920-01-06`) and in nominal-file
space (within `2019-12-31..2020-01-05`).

## 7. D1 / D2 / D3 / D4 classification

Applied under the committed precedence `D3 ⪼ D2 ⪼ D1`; `D4` only if
`D1`, `D2`, and `D3` are each individually inconclusive.

| Outcome | Criteria | Observed | Fires? |
|---|---|---|---|
| **D3** — broader envelope | any placeholder candidate outside `1920-01-01..1920-01-16` | all 6 values (`1920-01-01..1920-01-06`) fall inside the envelope; no value outside | **NO** |
| **D2** — narrow early-January-1920 family | canonical sentinel + placeholder candidates form a contiguous early-January-1920 range; no D3 evidence | contiguous `1920-01-01..1920-01-06`; 6 affected file dates; D3 negative | **YES** |
| **D1** — isolated adjacency | placeholder set limited to exactly `1920-01-02` | placeholder set is `{1920-01-02, 1920-01-03, 1920-01-04, 1920-01-05, 1920-01-06}` — larger than isolated adjacency | NO (D2 overrides) |
| **D4** — insufficient / inconclusive | D1, D2, D3 each individually inconclusive | D2 is individually conclusive | NO |

**Final decision: D2 — narrow early-January-1920 family.**

## 8. T1 / S1 status update

The chunk_2019 fresh-attempt closure recorded two pre-execution
assumptions about the placeholder-row phenomenon. Both are now
empirically resolved.

| Assumption | Prior status | Updated status |
|---|---|---|
| **T1** — one-off isolated anomaly (single affected nominal file date) | "disputed" after chunk_2020 halt | **decisively disputed**: **6** affected nominal file dates (canonical sentinel ∪ placeholder candidate union) |
| **S1** — single sentinel SQLDATE value (`1920-01-01` only) | "disputed" after chunk_2020 halt | **decisively disputed**: **6** distinct `1920-01-XX` values, contiguous |

Validated by the way the halt fired and by this research run:

- **Halt-on-other-unexpected** behavior fired correctly on the first
  non-sentinel non-`EXPECTED_OFFSETS` row at chunk_2020 production-runner
  execution; this remains a load-bearing discovery-preservation
  mechanism for future fresh-attempt runs
- **No silent `SENTINEL_SQLDATES` expansion**: the sentinel set
  remained `(date(1920, 1, 1),)` throughout both the chunk_2020 halt
  and this research cycle
- **No silent `EXPECTED_OFFSETS` widening**: the canonical tuple
  remained `(-3650, -365, -30, -7, -1, 0, 1)` throughout
- **R3 + Option α discovery-preservation property** held verbatim
- **Cross-check against chunk_2019 closure**: the 2019-12-31 canonical
  sentinel count observed in this research (120 rows) exactly
  reproduces the chunk_2019 fresh-attempt closure observation
  (`sentinel_sqldate_distribution = {'1920-01-01': {'2019-12-31': 120}}`).
  This validates the standalone parser's correctness against the
  production runner's parsing path for the known sentinel surface.

## 9. Structural observation (hypothesis-level; NOT classification)

The placeholder distribution shows a striking structural pattern:
each placeholder SQLDATE `1920-01-N` peaks in the nominal file dated
`2020-01-N`, with smaller tails on adjacent days. Peak counts:

| placeholder SQLDATE | peak count | peak file | tail files |
|---|---:|---|---|
| `1920-01-01` (canonical sentinel) | 87,241 | `2020-01-01` | `2019-12-31` (120), `2020-01-02` (404) |
| `1920-01-02` | 120,281 | `2020-01-02` | `2020-01-01` (98), `2020-01-03` (675) |
| `1920-01-03` | 153,043 | `2020-01-03` | `2020-01-02` (143), `2020-01-04` (394) |
| `1920-01-04` | 109,895 | `2020-01-04` | `2020-01-03` (143), `2020-01-05` (190) |
| `1920-01-05` | 63,273 | `2020-01-05` | `2020-01-04` (89) |
| `1920-01-06` | 85 | `2020-01-05` (tail-only) | — |

This pattern is consistent with a **year-shift mechanism** in which a
subset of rows inside a `2020-01-N` daily event file has its SQLDATE
year miscoded as `1920` rather than `2020`. Under this hypothesis the
miscoded rows would otherwise have been ordinary same-day rows
(offset `0`), and the placeholder distribution would be a structural
mirror of the underlying same-day-event distribution. The cluster's
sharp start at the `2019-12-31 / 2020-01-01` year boundary and sharp
end at `2020-01-05/06` is consistent with this interpretation.

**This is a hypothesis, not the D2 classification.** Two cautions
apply:

1. **The D2 classification is grounded in observed SQLDATE values
   only** (`1920-01-01..1920-01-06`, contiguous, inside the
   early-January-1920 envelope). The year-shift hypothesis is an
   *explanation* for those values, not the classification basis. The
   classification stands or falls on the observed distribution
   regardless of mechanism.
2. **A year-shift predicate amendment would overgeneralize beyond
   direct substrate evidence.** A predicate of the form "any SQLDATE
   whose year is 1920 while the nominal file year is 2020 is a
   sentinel" would silently extend the recognized envelope to include
   values that have not been empirically observed (e.g.
   `1920-07-15` in a `2020-07-15` file). The discipline established
   at the chunk_2019 substrate amendment cycle (commit `7206e30`)
   explicitly required direct substrate evidence for sentinel-set
   extension — not theoretical predicates. The same discipline must
   apply here.

## 10. Amendment direction

This memo does **not authorize** any runner amendment, any
`SENTINEL_SQLDATES` extension, or any `EXPECTED_OFFSETS` change. The
appropriate amendment direction, to be drafted in a separately
authorized **substrate amendment memo** (analogue of chunk_2019's
`7206e30`), is recorded below as a preparatory recommendation only.

### 10.1 Recommended direction (evidence-bounded)

**Discrete-tuple expansion to the six observed values**, following the
existing `SENTINEL_SQLDATES: Tuple[date, ...]` data shape:

```
SENTINEL_SQLDATES: Tuple[date, ...] = (
    date(1920, 1, 1),
    date(1920, 1, 2),
    date(1920, 1, 3),
    date(1920, 1, 4),
    date(1920, 1, 5),
    date(1920, 1, 6),
)
```

Properties of this recommendation:

- **Evidence-bounded**: every added value has been directly observed
  in the substrate; no value is added on prediction
- **Conservative**: adds exactly five values (`1920-01-02..1920-01-06`),
  matching the empirically-observed placeholder set
- **Lower-risk**: preserves the discrete-tuple data shape; minimal
  code change vs. the chunk_2019 amendment commit (`d99a210`); the
  runner's R3 + Option α logic continues to operate verbatim
- **Preserves discovery-preservation**: any future row whose SQLDATE
  is outside the (now extended) sentinel set AND whose offset is
  outside `EXPECTED_OFFSETS` will still trigger halt-on-other-unexpected
  per §9.A of the chunk_2020 planning memo
- **Forward-compatible**: if future fresh-attempt runs surface
  additional placeholder values, the discipline of evidence-bounded
  discrete-tuple extension can be applied again incrementally

### 10.2 Alternative directions (recorded for completeness; NOT recommended as default)

- **Date-range representation** (e.g.
  `SENTINEL_SQLDATE_RANGES = ((date(1920, 1, 1), date(1920, 1, 6)),)`):
  Defensible if the substrate amendment memo finds that the
  contiguous-range property is a stable structural invariant. This is
  a less conservative choice than discrete-tuple expansion because it
  pre-includes any future-observed `1920-01-N` for N in the range
  without requiring re-observation; however the range is still
  bounded and explicitly enumerated by date. **Not recommended as
  default** because (i) it requires a runner-data-shape change and
  (ii) it pre-includes any `1920-01-N` value not yet directly
  observed (e.g. `1920-01-04` would have already been "included" by a
  hypothetical range amendment after only `1920-01-02` and
  `1920-01-06` had been observed — this is the kind of silent
  inclusion the no-silent-expansion discipline is designed to prevent).
- **Year-shift predicate** (e.g. "any SQLDATE whose year is 1920
  while the nominal file year is 2020 is a sentinel" or, more
  generally, "any SQLDATE whose year differs from the nominal file
  year by exactly 100 in a placeholder-mechanism direction"):
  **NOT recommended as the amendment default.** A predicate
  overgeneralizes beyond direct substrate evidence; it would silently
  extend the recognized envelope to placeholder values that have
  never been observed; and it cannot itself be verified empirically
  without a separate broader-envelope research cycle (Option C). If
  the substrate amendment memo wishes to pursue the year-shift
  hypothesis, the appropriate path is **first** a separately scoped
  research cycle to test the predicate's structural properties on a
  broader envelope, **then** an amendment memo that decides between
  discrete-tuple extension and predicate based on that evidence.

### 10.3 Open amendment-design questions for the substrate amendment memo

- Whether the chunk_2019 substrate amendment memo's existing
  one-line-comment narrative pattern continues to apply or whether a
  longer rationale block is justified given the 5-value extension vs.
  the original 1-value substrate amendment
- Whether the runner's parse-loop comment at line 122 ("Sentinel
  SQLDATE subclass") needs to be updated to reflect the multi-value
  empirical basis
- Whether the empirical-validation surface count (currently
  fifth-surface confirmation for sentinel-remediation at chunk_2019
  closure) should be updated in the post-amendment memory record

These are noted as questions for the amendment memo to resolve; this
output memo does not pre-empt them.

## 11. Boundary preservation

Across the entire research cycle (scope-design memo → content review →
narrow §8 precedence cleanup → commit + push → research execution →
this output memo draft) the following boundaries were preserved:

- HEAD = origin/main = `a34d1ffcc2d4cfecb447ba45911f13b89a755656`
  unchanged across this draft turn; ahead/behind = 0 0; tracked tree
  clean
- Runner blob `a1a10994d183b70bb4dfdcec9a981013a5857e10` unchanged
  throughout
- `SENTINEL_SQLDATES = (date(1920, 1, 1),)` at runner line 136
  unchanged throughout
- `EXPECTED_OFFSETS = (-3650, -365, -30, -7, -1, 0, 1)` at runner
  line 120 unchanged throughout
- All five program guards `False` throughout
- `LANE2_*_AUTHORIZED` envs unset throughout
- Halt diagnostic byte-identical at SHA
  `a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`;
  remains in **live output location** at
  `results/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/halt_diagnostic.json`
- No archive copy of the halt diagnostic created (archival remains a
  separately scoped future sub-cycle)
- Memory files unchanged: `MEMORY.md` and
  `project_lane2_attention_spike.md` SHAs preserved across this draft
  turn
- No production runner invocation
- No production chunk_2020 output directory created beyond the
  pre-existing halted dir
- No raw payload preservation
- No test edits
- No planning-memo / addendum / scope-memo edits beyond pre-existing
  state
- chunk_2019 closure remains canonically closed and untouched
- chunk_2020 halted lineage (`dd7cb06 → 649ada3`) remains canonically
  closed and untouched
- No merge, no Step 2, no market-data work, no instrument
  construction
- chunk_2021 / chunk_2022 anchors untouched
- No tags, no branches, no force-push, no hook bypass

## 12. Next frontier

After this research output memo draft, the next eligible sub-cycle is
**not** runner amendment. The sub-cycle sequence is:

1. ✅ **Research output memo creation** — completed by this turn's
   draft
2. ⏸️ **Research output memo content review / sanity-check**
   (separately scoped; awaits explicit user initiation)
3. ⏸️ Research output memo commit + push (separately scoped; not
   authorized by this memo's creation)
4. ⏸️ *(optional)* Research-output-closure memory update (separately
   scoped)
5. ⏸️ **Substrate amendment memo** (analogue of `7206e30`) — drafts
   the amendment direction recorded in §10 above, decides
   discrete-tuple vs. date-range vs. predicate based on the §10
   analysis, and records the empirical evidence basis
6. ⏸️ Substrate amendment memo content review
7. ⏸️ Substrate amendment memo commit + push
8. ⏸️ Post-substrate-amendment-memo memory update
9. ⏸️ **Runner amendment commit** (analogue of `d99a210`) implementing
   the chosen `SENTINEL_SQLDATES` extension with direct-substrate-
   evidence justification per the amendment memo
10. ⏸️ Post-amendment memory update (updates runner-blob SHA anchor)
11. ⏸️ chunk_2020 post-amendment planning addendum (if planning gaps
    surface; analogue of `437e7e9`)
12. ⏸️ chunk_2020 fresh-attempt execution authorization (treated as a
    **fresh attempt under a further-amended runner regime**, NOT a
    retry of the now-canonically-closed halted first attempt at
    enable `dd7cb06` / restore `649ada3`)
13. ⏸️ chunk_2020 enable/restore lineage push
14. ⏸️ chunk_2020 execution-closure memory update
15. ⏸️ Halt diagnostic archival to
    `archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/`
    (separately scoped, at the user's choice of timing)

No live execution, no runner amendment, no `SENTINEL_SQLDATES` change,
no archive write, no commit, no push, and no memory update is
authorized by this research output memo creation. The memo is a
planning / record artifact only. Pause: await explicit next prompt.
