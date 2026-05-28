# chunk_2022 — 2022-11-10 documented-exception representation (summary)

**Label:** `UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY`

**What this is:** a committed *disclosure* record (not runtime behavior) for the single date `2022-11-10` whose GDELT 1.0 raw daily object `20221110.export.CSV.zip` is **officially data-confirmed but unavailable** from the raw-events endpoint.

## Facts
- Raw object: `20221110.export.CSV.zip` — catalog md5 `91e15516016f986e5b8a08712e1de95a`, catalog size `6,714,105` B. Endpoint persistently unserved (HEAD 404 / range 416–404 across four probes); neighbors `20221109`/`20221111` healthy; no official alternate raw object (path C ruled out).
- Data-bearing confirmed via official BigQuery `gdelt-bq.full.events`: `20221109=117,008`, `20221110=105,041`, `20221111=40,588`. **`105,041` is a coverage reference, not an exact runner-output gate.**
- Original halt: chunk_2022 `FetchFailure` at 313/365; halt diagnostic SHA `009720576b0e3dc3f11d67dbd811e36bbfd5a385df55567e1191ad30441057b7`.

## What is explicitly NOT claimed
- NOT raw `365/365`; NOT ordinary completion.
- NOT a no-data gap (`KNOWN_SUBSTRATE_GAPS` unchanged; `2022-11-10` not added).
- NOT recovered; no rows recovered; no semantic recovery artifact; no raw zip md5/byte equivalence.
- NOT raw-processed.

## Status
- `merge_gate_status = pending_labeled_completion_implementation`; chunk_2022 is **not** complete; the merge gate is **not** open.
- Production runner blob unchanged: `dec8e09283de9357b2b2aa65af13e21b21fe85cc`; **no runtime documented-exception path exists yet** — arbitrary 404s still halt as before.
- Target labeled-completion state (`expected_calendar_days=365`, `raw_processed_days=364`, `documented_unavailable_data_confirmed_days=1`, `recovered_days=0`, `known_no_data_gap_days=0`) requires a separately-authorized runner-support turn and a fresh chunk_2022 run.

## Self-heal fallback
If the canonical raw object becomes available, the normal raw-object path is preferred and would supersede this representation for the date (after a separately-authorized fresh attempt, all three production locks, no reuse of the halted directory).

Governance: design memos `e60a88a` → `854a606` → `36202b9` → `50dda46`. Contract: `configs/lane2_gdelt1_documented_exceptions.json`.
