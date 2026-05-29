# Lane 2 GDELT1 merged daily-count build summary

- substrate status: 10/10 terminal-status (9 raw-complete + 1 labeled-complete documented-exception)
- aggregate terminal-status days: 3562
- aggregate partition: 3557 raw_processed + 1 documented_unavailable_data_confirmed + 0 recovered + 4 known_no_data_gap = 3562 terminal_status
- documented exception: 2022-11-10 carries label UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY (date-confirmed, represented-only; its daily-count row has rows_from_offset_0 = 0, represented via neighbor offsets)

## Per-chunk category counts

| chunk_id | status_class | expected_calendar_days | raw_processed_days | documented_unavailable_data_confirmed_days | recovered_days | known_no_data_gap_days | terminal_status_days | terminal_status_complete |
|---|---|---|---|---|---|---|---|---|
| chunk_2013_partial | raw_complete | 275 | 275 | 0 | 0 | 0 | 275 | True |
| chunk_2014 | raw_complete | 365 | 361 | 0 | 0 | 4 | 365 | True |
| chunk_2015 | raw_complete | 365 | 365 | 0 | 0 | 0 | 365 | True |
| chunk_2016 | raw_complete | 366 | 366 | 0 | 0 | 0 | 366 | True |
| chunk_2017 | raw_complete | 365 | 365 | 0 | 0 | 0 | 365 | True |
| chunk_2018 | raw_complete | 365 | 365 | 0 | 0 | 0 | 365 | True |
| chunk_2019 | raw_complete | 365 | 365 | 0 | 0 | 0 | 365 | True |
| chunk_2020 | raw_complete | 366 | 366 | 0 | 0 | 0 | 366 | True |
| chunk_2021 | raw_complete | 365 | 365 | 0 | 0 | 0 | 365 | True |
| chunk_2022 | labeled_complete_documented_exception | 365 | 364 | 1 | 0 | 0 | 365 | True |
| aggregate | - | - | 3557 | 1 | 0 | 4 | 3562 | - |

## Retained halt-history (informational provenance; not merge inputs)

- results/lane2_gdelt1_full_daily_count_build/chunk_2022_20260528T121150Z/halt_diagnostic.json (halt_diagnostic sha256 009720576b0e3dc3f11d67dbd811e36bbfd5a385df55567e1191ad30441057b7)
- results/lane2_gdelt1_full_daily_count_build/chunk_2020_20260526T164747Z/halt_diagnostic.json (halt_diagnostic sha256 a6c9060a8798ad1392b2be1f3daf810b997ebada2c6d5f3bf1d879ddd170992f)
- archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2019_20260525T192552Z/halt_diagnostic.json (halt_diagnostic sha256 3b2b43708d0a7a9410d59a7bfd4deec7fef84f8a6543472f25942e67e1058005)

## Boundaries

- This merged substrate opens no Step 2, accesses no market data, performs no GDELT fetch, performs no BigQuery recovery, and amends no KNOWN_SUBSTRATE_GAPS entry.
- Self-heal: if a future separately authorized rebuild replaces the documented-exception state, raw-path processing supersedes it; until then the merged substrate carries the documented-exception label.
