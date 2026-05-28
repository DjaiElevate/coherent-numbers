# Lane 2 GDELT1 Full Daily Count Build — chunk_2021 Execution-Authorization Plan v0.1

> **Planning / authorization-memo only.** This memo authorizes a *later, separate* chunk_2021 live-execution prompt. It does **not** execute chunk_2021, does **not** flip any guard, and does **not** contact GDELT.

---

## 1. Purpose

- Authorize a later, separately-prompted chunk_2021 live production execution under the further-amended runner regime.
- This memo **does not** execute chunk_2021, **does not** flip `FULL_BUILD_AUTHORIZED`, **does not** set any `LANE2_*_AUTHORIZED` env var, and **does not** contact GDELT.
- The future chunk_2021 live-execution prompt is **not** authorized by this memo alone; it must be issued explicitly.

## 2. Baseline

- HEAD = origin/main = `e1b605f73d83109a4da6403f8d06166eee7e214d` (short `e1b605f`).
- chunk_2020 fresh-attempt execution is **complete, pushed, and recorded in memory**.
- Substrate progress = **8 / 10** chunks complete.
- On-disk Path (b) counter = **90** (sole canonical/gating counter; see §12).
- Active frontier = chunk_2021 planning / execution-authorization cycle.
- chunk_2022 remains downstream; merge remains blocked until 10/10.

## 3. Chunk target

- `chunk_id = chunk_2021`
- date range: `2021-01-01` through `2021-12-31`
- expected file count: **365**
- **non-leap-year** chunk
- chunk_2022 is **out of scope** for the future chunk_2021 execution prompt.

## 4. Required production locks for the future live execution

All three must be satisfied — missing any one **blocks** live execution (`_guards_ok` in runner source):

1. **Source guard enable commit**: `FULL_BUILD_AUTHORIZED = True`.
2. **CLI flag**: `--authorize-full-build-run`.
3. **Env var (single run command only)**: `LANE2_FULL_BUILD_AUTHORIZED=1`.

The env var must be set inline for the single production command only and must not persist in the session.

## 5. Required live-execution lifecycle for the future prompt

1. Preflight (repo state, blob, anchors, guards, env, output-dir state).
2. Enable commit (`FULL_BUILD_AUTHORIZED = False → True`, runner file only, one line).
3. **Exactly one** chunk_2021 production run (CLI flag + env var).
4. Restore commit (`True → False`) **regardless of execution outcome**.
5. Post-run continuity verification.
6. **No push** during the live-execution turn unless separately authorized.
7. Memory update **only after** a successful push/closure, separately authorized.

## 6. Non-weakening canon

1. no-retry
2. exactly-once
3. no-off-session
4. no-market-data
5. no-Step-2
6. no-checkpoint-resume
7. no-bounded-parallelism

## 7. Active boundaries

- no chunk_2022
- no merge
- no Step 2
- no market data
- no instrument construction
- no 2023+ access
- no halt-diagnostic archival
- no output commit unless separately authorized
- no memory update during live execution
- no source edits other than the future `FULL_BUILD_AUTHORIZED` guard toggles

## 8. Runner anchors (live at this memo's authoring; **must be re-verified before live execution**)

- Runner file: `scripts/run_lane2_gdelt1_full_daily_count_build.py`
- Canonical post-restore runner blob: `dec8e09283de9357b2b2aa65af13e21b21fe85cc`
- `FULL_BUILD_AUTHORIZED = False` — **line 95**
- `RECOGNIZED_LIST_SHA256` value `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` — value literal **line 108** (line 107 is the `RECOGNIZED_LIST_SHA256 = (` opener)
- `EXPECTED_OFFSETS = (-3650, -365, -30, -7, -1, 0, 1)` — **line 120**
- `SENTINEL_SQLDATES` six-value tuple — opener **line 151** (values lines 152–157)
- `KNOWN_SUBSTRATE_GAPS` four global 2014 dates — opener **line 163**
- chunk_2021 live anchors:
  - `CHUNK_IDS` entry `"chunk_2021"` — **line 1625**
  - `EXPECTED_CHUNK_COUNTS["chunk_2021"] = 365` — **line 1638**
  - `CHUNK_YEAR_RANGES["chunk_2021"] = (date(2021, 1, 1), date(2021, 12, 31))` — **line 1651**
- (For reference only — out of scope: chunk_2022 at lines 1626 / 1639 / 1652.)
- **These line numbers must be live-re-verified against the then-current runner before the live execution; do not reuse them as predictions.**

## 9. Sentinel handling

- Six-value `SENTINEL_SQLDATES` only: `1920-01-01`, `1920-01-02`, `1920-01-03`, `1920-01-04`, `1920-01-05`, `1920-01-06`.
- `date(1920, 1, 7)` remains **excluded** and is not authorized.
- The future run must **halt** on any non-sentinel unexpected offset (offset outside `EXPECTED_OFFSETS`).
- The future run must **not** silently amend the sentinel tuple; any amendment requires a separately scoped substrate-evidence memo.

## 10. Corrected fetch-gap semantics

- `substrate_gap_dates_not_fetched` may list **all four global 2014 dates** (`2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`) even for chunk_2021. This is the runner's **consistent established semantics** (verified identical in chunk_2014, chunk_2018, chunk_2019, chunk_2020), **not** automatically an anomaly.
- **Do not** repeat the prior chunk_2020 prompt's incorrect prediction that this field would be empty for a non-2014 chunk. Do not infer field meaning from the chunk date range alone — verify runner behavior.
- For chunk_2021 the **anomaly criteria** are strictly:
  1. a chunk_2021 target date is missing unexpectedly;
  2. the known global gap constant (`KNOWN_SUBSTRATE_GAPS`) changes unexpectedly;
  3. non-sentinel unexpected offsets appear;
  4. sentinel handling deviates from the six-value tuple;
  5. any 2023+ access occurs.

## 11. Halted forensic output preservation

- The May-26 chunk_2020 halted forensic directory `results/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/` remains forensic evidence only.
- Halt diagnostic SHA-256 remains `a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f` and must stay byte-identical.
- **No archival is authorized** by this memo.

## 12. Counter discipline

- On-disk **Path (b) counter = 90** is the **sole canonical/gating counter**.
- The **user-side carry-forward counter track is RETIRED**: it is non-canonical, deprecated-not-live, and not a gating value.
- Historical user-side values such as **103 / 104** must **not** drive future prompts, reports, handoffs, or gate decisions.
- **Forward obligation:** because this is *not* a memory-write turn, memory is not updated now. The **next memory-write boundary must land this user-side-counter-retirement rule on disk** in both:
  - `/Users/jay/.claude/projects/-Users-jay/memory/MEMORY.md`
  - `/Users/jay/.claude/projects/-Users-jay/memory/project_lane2_attention_spike.md`
- Do not use user-side arithmetic in future prompts.

## 13. Expected future live-execution report requirements

The future chunk_2021 live-execution report must include:

- exact command echoed;
- confirmation the env var is unset after the command;
- runtime total and per-URL;
- URL count **365 / 365** if successful;
- output directory path;
- artifact sizes and SHA-256 values (`chunk_contributions.csv`, `chunk_metadata.json`, `chunk_summary.md`);
- runner-computed `chunk_manifest_digest`;
- row totals (in-window / out-of-window / sentinel / total parsed) with `per_offset_total`;
- sentinel diagnostics (six SENTINEL_SQLDATEs; no `1920-01-07`; parser-anomaly counts);
- fetch-gap diagnostics **under the corrected semantics** (§10);
- final runner-blob round-trip to `dec8e09283de9357b2b2aa65af13e21b21fe85cc`;
- halt-diagnostic byte-identity (`a6c9060…0992f`);
- negative confirmations (no push unless authorized, no memory update, no chunk_2022, no merge, no Step 2/market-data/instrument-construction, no 2023+, no retry/resume/parallelism/off-session, no archival).

## 14. Recommended future verdict set (for the chunk_2021 live-execution prompt)

- `SUCCESS — CHUNK_2021 FRESH-ATTEMPT EXECUTION COMPLETE`
- `SUCCESS — CHUNK_2021 FRESH-ATTEMPT EXECUTION COMPLETE WITH NON-BLOCKING OBSERVATIONS`
- `HALTED — EXECUTION FAILED AFTER START WITH GUARD RESTORED`
- `HALTED — STRUCTURAL OFFSET ANOMALY DETECTED`
- `HALTED — UNEXPECTED NON-SENTINEL OFFSET DETECTED`
- `BLOCKED — PREFLIGHT FAILED`
- `BLOCKED — PRODUCTION LOCKS NOT ALL SATISFIED`
- `BLOCKED — ENABLE COMMIT FAILED`
- `BLOCKED — RESTORE COMMIT FAILED`
- `BLOCKED — POST-RUN CONTINUITY ENVELOPE FAILED`
- `UNCLASSIFIED — STATE REQUIRES USER REVIEW`

## 15. Next frontier

- After this memo is committed and pushed, the next step is a **separate chunk_2021 live-execution authorization prompt**.
- That later prompt must **not** be treated as authorized by this memo alone.
- chunk_2022 and merge remain downstream; merge stays blocked until 10/10 chunks complete (chunk-design memo `5962c20` §9.1.2).
- Halt-diagnostic archival and the output-commit question (follow the 2014–2019 precedent) remain separately scoped.

---

*End of memo v0.1 — planning/authorization only; no execution, no guard flip, no GDELT contact.*
