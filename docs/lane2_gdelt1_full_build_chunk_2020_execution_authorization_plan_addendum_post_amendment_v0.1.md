# Lane 2 — GDELT1 chunk_2020 Execution-Authorization Plan — Post-Amendment Addendum (v0.1)

## 1. Status / scope

This is a **narrow, governance-only addendum** to the committed
chunk_2020 execution-authorization planning memo. It updates planning
anchors that were rendered stale by the chunk_2020 substrate research
and runner amendment cycle. It does **not** authorize execution.

This addendum is explicitly:

- **not** an execution authorization
- **not** a runner edit
- **not** a test update
- **not** a substrate amendment memo
- **not** an archival of the chunk_2020 halt diagnostic
- **not** a memory update
- **not** a commit / push (commit/push is a separate sub-cycle)
- **not** a chunk_2020 retry
- **not** a `SENTINEL_SQLDATES` change beyond what runner amendment
  commit `8b7d42f` already shipped
- **not** merge / Step 2 / market-data / instrument-construction work

The addendum is the **chunk_2020 analogue of chunk_2019's post-amendment
planning addendum at commit `437e7e9`** — it consolidates the
governance chain between the original chunk_2020 planning memo
(`c896253`) and any future chunk_2020 fresh-attempt execution
authorization. The original planning memo remains valid as written;
this addendum supersedes only the specific anchors made stale by the
runner amendment.

## 2. Why this addendum is required

Three load-bearing reasons motivate this addendum:

### 2.1 Planning memo self-prescription (§8 item 4)

The original chunk_2020 planning memo (`c896253`) §8 item 4 explicitly
prescribes that "*a fresh planning addendum is required prior to
execution*" if a runner amendment has changed the runner blob between
the planning memo's authorship and execution. Verbatim from §8 item 4:

> "Runner blob SHA equal to `a1a10994d183b70bb4dfdcec9a981013a5857e10`
> (or to whatever the then-canonical post-amendment runner blob is, if
> a further amendment has occurred — in which case a fresh planning
> addendum is required prior to execution)."

The runner blob has changed (see §2.2 below). Honoring the planning
memo's own discipline requires this addendum.

### 2.2 Runner blob transition

The chunk_2020 runner amendment commit `8b7d42f` changed the runner
blob:

- **Old (historical-only)**: `a1a10994d183b70bb4dfdcec9a981013a5857e10`
- **New (canonical)**: `dec8e09283de9357b2b2aa65af13e21b21fe85cc`

All five references to the old blob in the original planning memo
(lines 50, 111, 181, 212, 424 of `c896253`'s file) are stale as
canonical anchors. Future chunk_2020-onward preflights MUST use the
new blob.

### 2.3 chunk_2019 precedent

The chunk_2019 substrate amendment cycle followed exactly this
pattern: original planning memo `6c17850` (committed pre-amendment) →
narrow post-amendment addendum `437e7e9` → chunk_2019 fresh-attempt
execution authorization → enable/restore lineage. The chunk_2020 cycle
is structurally identical and the same addendum discipline applies.

## 3. Governance chain

This addendum consolidates the following committed governance artifacts
for future chunk_2020 execution-authorization-prompt drafters:

| Artifact | Commit | File SHA-256 |
|---|---|---|
| Original chunk_2020 planning memo | `c89625385103872c4b2a774bec51767ca62d143d` | `cb9e51c3ee0b63ac7f986af357a9eb2e45089c10ea661572ec5ebd51291001f3` |
| Scope-design memo (Option B; `D3 ⪼ D2 ⪼ D1` precedence) | `a34d1ffcc2d4cfecb447ba45911f13b89a755656` | `842e558840cee0177885f2c81eaac6a1c504a09405ad57d94a9cc7baa58427c2` |
| D2 research output memo | `dc48f55ae06af3e5cc439b92d3245974933edb09` | `1b2e76d8bd4bba62764c06d675c6ffb870a76636498a6f202f371d61a7f9719a` |
| Substrate amendment memo | `a1f2c4c7d76df02bedc42cbc12ee4051e1b0cd42` | `9774bbd7156d1546060240f453beb7fed198c08e81455afdfa9e82468fc1b43b` |
| Runner amendment commit | `8b7d42f4b7e0fef9bd888042af0f7a3f18a529e5` | (runner blob `dec8e09283de9357b2b2aa65af13e21b21fe85cc`) |

Precedent for this addendum's shape: chunk_2019 post-amendment
planning addendum at commit `437e7e9` (file SHA-256
`0c65be07327e5dbaa21a682ece40d087489dd3152ebdddb1876dcc6651a1f158`).

This addendum is the consolidated governance bridge between the
committed planning memo `c896253` and any future chunk_2020
fresh-attempt execution authorization prompt.

## 4. Runner blob and sentinel-state update

### 4.1 Runner blob transition

- **Old active runner blob**:
  `a1a10994d183b70bb4dfdcec9a981013a5857e10` — used since chunk_2019
  runner amendment `d99a210` through the chunk_2020 halted first
  attempt. **Now historical-only.** Must not be used as the active
  byte-identity anchor for any future chunk_2020-onward execution
  preflight.
- **New active runner blob**:
  **`dec8e09283de9357b2b2aa65af13e21b21fe85cc`** — produced by
  runner amendment commit `8b7d42f`. **All future
  chunk_2020-onward execution preflights MUST use this blob.**

### 4.2 `SENTINEL_SQLDATES` extension

- **Old**: `SENTINEL_SQLDATES: Tuple[date, ...] = (date(1920, 1, 1),)`
  at runner **line 136**
- **New**: 6-value tuple at runner **line 151**:

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

`len(SENTINEL_SQLDATES) = 6`. Every member is directly observed in
substrate evidence per the D2 research output memo (`dc48f55`); zero
predicted values; no row-count threshold (`date(1920, 1, 6)` is
included despite being marginal evidence at 85 rows in 1 file,
because it is directly observed).

### 4.3 `date(1920, 1, 7)` halt discipline

`date(1920, 1, 7)` is **NOT** in the recommended (and now committed)
sentinel tuple. Any future encounter with `1920-01-07`, or any other
not-yet-observed placeholder-like value, MUST still trigger
halt-on-other-unexpected and motivate a separately scoped substrate
amendment cycle — not silent expansion. This discipline is
implemented in runner amendment `8b7d42f` and verified by test
`test_parser_halts_on_date_1920_01_07_unobserved_placeholder` (part
of the 186-test lane2 full-build pytest suite that passed at
`8b7d42f`).

## 5. Updated runner anchor table (post-amendment, verified directly)

The narrative comment block in the runner expanded by ~22 lines during
the amendment (now lines 122-150). All anchors at or after that block
shifted by +22 lines. Anchors before the block are unchanged.

| Anchor | Current line | Pre-amendment (original planning memo §7) | Shift |
|---|---:|---:|---:|
| `FULL_BUILD_AUTHORIZED = False` | **95** | 95 | 0 (unchanged) |
| `RECOGNIZED_LIST_SHA256 = (...)` | **107** | 107 | 0 (unchanged) |
| `EXPECTED_OFFSETS: Tuple[int, ...] = (-3650, -365, -30, -7, -1, 0, 1)` | **120** | 120 | 0 (unchanged) |
| `SENTINEL_SQLDATES: Tuple[date, ...] = (` (declaration line) | **151** | 136 | **+15** |
| `KNOWN_SUBSTRATE_GAPS: Tuple[str, ...] = (` | **163** | 141 | +22 |
| `CHUNK_IDS: Tuple[str, ...] = (` (block start) | **1616** | 1594 | +22 |
| `"chunk_2020",` entry in `CHUNK_IDS` | **1624** | 1602 | +22 |
| `EXPECTED_CHUNK_COUNTS: Dict[str, int] = {` (block start) | **1629** | 1607 | +22 |
| `"chunk_2020": 366,` entry | **1637** | 1615 | +22 |
| `CHUNK_YEAR_RANGES: Dict[str, Tuple[date, date]] = {` (block start) | **1642** | 1620 | +22 |
| `"chunk_2020": (date(2020, 1, 1), date(2020, 12, 31)),` entry | **1650** | 1628 | +22 |

**Re-verification discipline (load-bearing)**: the line numbers above
record the post-amendment state at the time of this addendum's
creation. The future chunk_2020 fresh-attempt execution-authorization
prompt MUST **directly re-verify these line anchors against the
then-current runner**, NOT blindly reuse them from this addendum. If
any line has drifted further (e.g., a later unrelated runner edit),
that drift must be detected at execution preflight and either
re-anchored or escalated as a preflight failure. This discipline
mirrors the original planning memo's §8 item 10 and the chunk_2019
addendum's discipline at `437e7e9`.

## 6. Substrate / amendment state now governing execution

The chunk_2020 substrate research and amendment cycle established the
following post-amendment state (recorded across the governance chain
in §3):

- **Final classification**: **D2 — narrow early-January-1920 family**
  under committed precedence **`D3 ⪼ D2 ⪼ D1`** (D4 only if D1/D2/D3
  individually inconclusive); D3 NO, D2 YES, D1 NO, D4 NO.
- **Corrected affected nominal file-date count: 6** (`2019-12-31`,
  `2020-01-01`, `2020-01-02`, `2020-01-03`, `2020-01-04`,
  `2020-01-05`). The original research execution report's
  "7 affected file dates" was an off-by-one text error; canonical
  count is **6**, resolved at §4 of the D2 research output memo and
  carried forward by the substrate amendment memo `a1f2c4c`.
- **Six distinct directly-observed `1920-01-XX` SQLDATE values**:
  `1920-01-01` (canonical sentinel; 87,765 rows across 3 files) +
  `1920-01-02..1920-01-06` (placeholder candidates; 448,309 total
  rows). Set is contiguous within early-January-1920 envelope
  `1920-01-01..1920-01-16`; no value outside that envelope.
- **Discrete-tuple amendment direction**: implemented by runner
  amendment `8b7d42f` exactly per §5 of the substrate amendment
  memo. The committed sentinel tuple is the 6-value list in §4.2.
- **Year-shift predicate not recommended / not implemented**: a
  year-shift predicate ("any SQLDATE whose year is 1920 while the
  nominal file year is 2020 is a sentinel") would overgeneralize
  beyond direct substrate evidence — it would silently recognize
  never-observed values like `1920-07-15` in `2020-07-15`, and
  would erase the discovery-preservation signal that the
  halt-on-other-unexpected mechanism provides. The substrate
  amendment memo `a1f2c4c` §6.4 / §6.5 explicitly disqualifies
  this direction; the runner amendment did not implement it.
- **`EXPECTED_OFFSETS` unchanged**: `(-3650, -365, -30, -7, -1, 0, 1)`
  at runner line 120 — load-bearing for discovery preservation;
  preserved by the amendment.
- **Discovery-preservation tests passed**: the runner amendment
  commit `8b7d42f` ships 4 new pytest tests covering (i) all 6
  sentinels recognized, (ii) `date(1920, 1, 7)` still halts, (iii)
  `1920-02-15` (out-of-cluster placeholder-like) still halts, (iv)
  chunk_2020 anchors unchanged after the amendment. Targeted file:
  **186 passed**. Lane 2 subset (4 files): **430 passed**. Full
  project suite: **1024 passed, 2 skipped, 0 failures**.
- **R3 + Option α framework**: preserved verbatim; the amendment
  extends the sentinel set but does not weaken the R3 routing
  semantics or the Option α exclusion of sentinel rows from primary
  aggregates.

## 7. Future execution preflight — corrections to the committed planning memo

The future chunk_2020 fresh-attempt execution-authorization prompt's
preflight checklist MUST **supersede** the following items in the
original planning memo's §8:

### 7.1 Item 4 supersession (runner blob)

- **Original**: `Runner blob SHA equal to a1a10994d183b70bb4dfdcec9a981013a5857e10`
- **Superseded**: `Runner blob SHA equal to dec8e09283de9357b2b2aa65af13e21b21fe85cc`

The old `a1a10994…57e10` anchor is now historical-only. Asserting
equality against the old blob would fail post-amendment.

### 7.2 Item 6 supersession (`SENTINEL_SQLDATES`)

- **Original**: `SENTINEL_SQLDATES = (date(1920, 1, 1),) still defined
  at scripts/run_lane2_gdelt1_full_daily_count_build.py:136`
- **Superseded**: `SENTINEL_SQLDATES = (date(1920, 1, 1), date(1920,
  1, 2), date(1920, 1, 3), date(1920, 1, 4), date(1920, 1, 5),
  date(1920, 1, 6)) still defined at
  scripts/run_lane2_gdelt1_full_daily_count_build.py:151`

Asserting the singleton value or the line-136 anchor would fail
post-amendment. The future preflight must additionally assert
`date(1920, 1, 7) not in SENTINEL_SQLDATES`.

### 7.3 Item 9 nuance (execution-output directory)

- **Original**: `No chunk_2020 execution-output directory exists
  under results/lane2_gdelt1_full_daily_count_build/`
- **Nuance**: the halted first-attempt output directory
  `results/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/`
  **now exists** as forensic evidence (containing only
  `halt_diagnostic.json` at SHA
  `a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`).
  The future preflight must:
  - Permit the halted-attempt output directory to exist (forensic
    evidence only; not a checkpoint, not a resume anchor)
  - Assert **no new** chunk_2020 production-output directory exists
    beyond the halted-attempt one (i.e., no second
    `chunk_2020_<UTC>/` directory with `chunk_metadata.json` /
    `chunk_contributions.csv` / `chunk_summary.md` content)
  - Verify the halted-attempt halt diagnostic SHA is byte-identical
    to `a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`
    at preflight start and at completion

### 7.4 Item 10 supersession (line-number anchors)

- **Original**: `chunk_2020 line-number anchors (1602 / 1615 / 1628)
  directly re-verified against the current runner, not reused from
  this memo`
- **Superseded**: `chunk_2020 line-number anchors (**1624 / 1637 /
  1650** at the time of this addendum) directly re-verified against
  the current runner, not reused from this addendum`

The re-verification discipline itself is preserved — only the cited
expected line numbers are updated.

### 7.5 Items unaffected by the amendment (no supersession needed)

The following original planning memo §8 items remain valid as
written:

- Item 1 (HEAD / origin/main alignment)
- Item 2 (ahead/behind = 0 0)
- Item 3 (tracked tree clean — with the nuance that the halted-attempt
  output directory and research output directory are allowed untracked
  state)
- Item 5 (`FULL_BUILD_AUTHORIZED = False` at line 95) — line 95
  unchanged
- Item 7 (all five guards `False`)
- Item 8 (all `LANE2_*_AUTHORIZED` envs unset)
- Item 11 (authority artifact SHAs re-verified) — recognized-list and
  F4 baseline SHAs unchanged
- Item 12 (memory files not modified during preflight)
- Item 13 (chunk_2021 / chunk_2022 anchors untouched)

### 7.6 Additional preflight items for the fresh-attempt prompt

In addition to the original planning memo's items (with the
supersessions above), the future fresh-attempt execution-authorization
prompt's preflight MUST also include:

- Re-verify this addendum's file SHA-256 matches the committed
  addendum's recorded SHA-256 (to be recorded in the
  post-addendum memory update once committed)
- Re-verify the substrate amendment memo at `a1f2c4c` exists with file
  SHA-256 `9774bbd7156d1546060240f453beb7fed198c08e81455afdfa9e82468fc1b43b`
- Re-verify the D2 research output memo at `dc48f55` exists with file
  SHA-256 `1b2e76d8bd4bba62764c06d675c6ffb870a76636498a6f202f371d61a7f9719a`
- Re-verify the runner amendment commit `8b7d42f` is part of the
  current HEAD lineage
- Assert `date(1920, 1, 7) not in SENTINEL_SQLDATES`

## 8. Fresh-attempt framing

A future chunk_2020 execution under the post-runner-amendment regime
must be **a fresh attempt under a further-amended runner regime** —
**not** a retry of the now-canonically-closed halted first attempt
(enable `dd7cb06785d18d6c00b3e87749bdec66e4256f35` → restore
`649ada3f7cf8165dd123a0045ea1594fd1369af3`).

The fresh-attempt execution must preserve the following, none weakened
(7-item non-weakening canon, identical to the canon recorded at the
substrate amendment memo `a1f2c4c` §8 and at the runner amendment
commit `8b7d42f`'s test scope):

1. **no-retry**
2. **exactly-once**
3. **no-off-session**
4. **no-market-data**
5. **no-Step-2**
6. **no-checkpoint-resume**
7. **no-bounded-parallelism**

Additional fresh-attempt boundary conditions:

- **No checkpoint resume**: there is no partial state to resume from;
  the halted-attempt output directory contains only the halt
  diagnostic (no `chunk_metadata.json`, no `chunk_contributions.csv`,
  no `chunk_summary.md` were produced before halt)
- **No reuse of halted output**: the halt diagnostic at
  `chunk_2020_20260526T164747Z/halt_diagnostic.json` is **forensic
  evidence only** — not a resume anchor, not a recovery state
- **Same-session execution** (same-session in-session, no
  `export` of `LANE2_*_AUTHORIZED`)
- **No 2023+ access**
- **No instrument construction**
- **No prior-chunk rerun**
- **No `chunk_2021` / `chunk_2022` authorization** within the
  chunk_2020 execution prompt
- **No raw payload preservation**
- **No memory edit during live execution**
- **`EXPECTED_OFFSETS` unchanged at runtime**
- **`SENTINEL_SQLDATES` unchanged at runtime** (the 6-value tuple is
  source-side; the fresh-attempt execution must not silently extend
  it during the run)
- **Halt diagnostic byte-identity preserved**: the halt diagnostic at
  SHA `a6c9060a…992f` must remain byte-identical throughout the
  fresh-attempt execution; the fresh-attempt run creates a **new**
  output directory and does not write to the halted-attempt
  directory

## 9. Archive and boundary preservation

- **Halt diagnostic remains live and unarchived**: the chunk_2020
  halt diagnostic at
  `results/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/halt_diagnostic.json`
  (SHA-256
  `a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f`)
  remains in its live output location throughout this addendum turn,
  any future addendum content-review turn, any future commit + push
  turn, any future post-addendum memory update, and any future
  chunk_2020 fresh-attempt execution sub-cycle. Archival to
  `archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/`
  is a **separately scoped future sub-cycle**, mirroring the
  chunk_2019 halted first-attempt arc (archived halt diagnostic at
  `archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2019_20260525T192552Z/halt_diagnostic.json`,
  SHA `3b2b43708d0a7a9410d59a7bfd4deec7fef84f8a6543472f25942e67e1058005`).
- **No execution authorization by this addendum**: this addendum
  does NOT authorize the chunk_2020 fresh-attempt execution prompt.
  Execution authorization is a separately scoped downstream prompt
  that cites this addendum as governance.
- **Merge blocked**: merge remains blocked until 10 / 10 chunks
  succeed per chunk-design memo `5962c20` §9.1.2. Current progress
  is 7 / 10; chunk_2020 remains 0 / 366 pending fresh-attempt
  execution.
- **Step 2 firewalled**: Step 2 remains firewalled until a
  separately authorized memo retires the no-market-data firewall.
- **No `chunk_2021` / `chunk_2022` authorization**: this addendum
  governs only chunk_2020.
- **No runner edits in this addendum turn**: the runner amendment
  was already committed at `8b7d42f`; no further runner edits are
  authorized by this addendum.
- **No tests in this addendum turn**: the runner amendment commit
  already added the required tests; no further test edits are
  authorized.
- **No memory update in this addendum turn**: the post-addendum
  memory update is a separately scoped sub-cycle.
- **No commit / no push by this addendum**: commit/push is a
  separately scoped sub-cycle.

## 10. Next frontier

After this addendum draft is created, the next eligible sub-cycle is
**not** chunk_2020 fresh-attempt execution. The sub-cycle sequence
is:

1. ✅ **Post-amendment planning addendum creation** — completed by
   this turn's draft
2. ⏸️ **Addendum content review / sanity-check** (separately scoped;
   awaits explicit user initiation)
3. ⏸️ Addendum commit + push (separately scoped; not authorized by
   this addendum's creation)
4. ⏸️ Post-addendum memory update (separately scoped) — records the
   committed addendum's commit SHA and file SHA-256 for future
   citation by the execution-authorization prompt
5. ⏸️ chunk_2020 fresh-attempt execution authorization (separately
   scoped; cites this addendum as governance; uses new runner blob
   `dec8e09283de9357b2b2aa65af13e21b21fe85cc`; re-verifies line
   anchors `1624 / 1637 / 1650` directly against the then-current
   runner)
6. ⏸️ chunk_2020 enable/restore lineage push
7. ⏸️ chunk_2020 execution-closure memory update
8. ⏸️ Halt diagnostic archival to
   `archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/`
   (separately scoped, at the user's choice of timing)

No live execution, no runner amendment, no `SENTINEL_SQLDATES`
change, no archive write, no commit, no push, and no memory update is
authorized by this addendum creation. The addendum is a planning /
governance-bridge artifact only. Pause: await explicit next prompt.
