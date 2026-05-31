# Lane 2 GDELT1 Step 2 Daily-Feature Summary

Substrate is 10/10 terminal-status (9 raw-complete chunks + 1 labeled-complete documented-exception chunk).

- merged substrate directory: `/Users/jay/Documents/GitHub/coherent-numbers/results/lane2_gdelt1_full_daily_count_build/merged_20260529T175416Z`
- input rows consumed: 3562
- locked feature column count: 69
- design memo SHA-256: `fea70ede10982a140d57b9534a9ce08eb7bb946c4dc6ba1e410b45777c8ed164`
- build_manifest_digest: `4b312183d9bb126169fc82c5b76008359778df18ee803527c567f7ade3a89650`

## Day-class counts (from `build_metadata.json` aggregate)

- raw_processed_days: 3557
- documented_unavailable_data_confirmed_days: 1
- recovered_days: 0
- known_substrate_gap_days: 4
- terminal_status_days: 3562

## Documented-exception row

- date: 2022-11-10
- label: UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY
- propagated represented-only: True
- total_row_count: 1267
- neighbor-offset cross-check: 91 + 849 + 327 = 1267

## Boundary declarations

- no_step_2_market_join: true
- no_market_data: true
- no_instrument: true
- no_gdelt_fetch: true
- no_bigquery: true
- no_row_export: true
- no_known_substrate_gaps_amendment: true

This summary describes the GDELT-only substrate and the deterministic feature derivation. No exogenous-series claims and no outcome-variable claims are asserted here. Step 2 implementation, Step 2 execution, and the later separately authorized join/construction phases remain firewalled until separately authorized.
