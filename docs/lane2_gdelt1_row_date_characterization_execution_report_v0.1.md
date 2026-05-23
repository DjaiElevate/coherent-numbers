# Lane 2 GDELT1 row-date characterization execution report v0.1

## 1. Preflight state

| Item | Value |
|---|---|
| `HEAD = origin/main` (before enable) | `487dadb39957e2575ce4c6a9ff278459dc318055` |
| Ahead count before enable | `0` |
| Tracked tree status before enable | clean (zero M/A/D/R) |
| `REAL_RETRIEVAL_ENABLED` | `False` (line 647 of `src/lane2_gdelt1_count_feasibility.py`) |
| `COUNT_FEASIBILITY_AUTHORIZED` | `False` (line 49 of `scripts/run_lane2_gdelt1_count_feasibility.py`) |
| `EVENT_FILE_PROBE_AUTHORIZED` | `False` (line 52 of `scripts/run_lane2_gdelt1_event_file_probe.py`) |
| `ROW_DATE_CHARACTERIZATION_AUTHORIZED` | `False` (line 57 of `scripts/run_lane2_gdelt1_row_date_characterization.py`) |
| Shell envs | `LANE2_COUNT_FEASIBILITY_AUTHORIZED=UNSET`, `LANE2_EVENT_FILE_PROBE_AUTHORIZED=UNSET`, `LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED=UNSET` |
| Plan-lock memo anchor | `a2a8fd5` |
| Substrate-validation memo anchor | `a8a9dd2` |
| Event-file probe execution report anchor | `9319d30` |
| Design-note anchor | `e55e09a` |
| Probe implementation anchor | `0b341b4` |
| Parser-coverage anchor | `845c51c` |
| Characterization implementation anchor | `e9f8781` |
| Corrective (exact-offset) anchor | `487dadb` |
| Recognized-list capture SHA | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` (preserved) |
| First-probe output dir | `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` (preserved, untracked) |
| May-22 count-feasibility empty dir | preserved (empty, mtime `May 22 15:37`) |

## 2. Enable commit SHA

**`3537a625a00cc5508b1fea3e4d13156f31f3f29c`** (short `3537a62`); subject `Enable Lane 2 row-date characterization run`; 1 file changed / 1 insertion(+) / 1 deletion(−). `git diff HEAD~ HEAD --numstat` returned `1	1	scripts/run_lane2_gdelt1_row_date_characterization.py`.

## 3. Restore commit SHA

**`73a7911efa0995d7fe4080dff0b91dc6bab2b246`** (short `73a7911`); subject `Restore Lane 2 row-date characterization guard`; 1 file changed / 1 insertion(+) / 1 deletion(−). `git diff HEAD~ HEAD --numstat` returned `1	1	scripts/run_lane2_gdelt1_row_date_characterization.py`. `git diff 487dadb HEAD -- scripts/run_lane2_gdelt1_row_date_characterization.py` returned empty — runner is **byte-identical to `487dadb`** after restore.

## 4. Run command

```
LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED=1 python3 scripts/run_lane2_gdelt1_row_date_characterization.py --authorize-row-date-characterization-run
```

Inline env var (not `export`); single invocation; exit code `0`; stdout: `Row-date characterization outputs written under: /Users/jay/Documents/GitHub/coherent-numbers/results/lane2_gdelt1_row_date_characterization/20260523T033234Z`; stderr empty. `LANE2_ROW_DATE_CHARACTERIZATION_AUTHORIZED` was `UNSET` immediately after the run.

## 5. Output directory path

`results/lane2_gdelt1_row_date_characterization/20260523T033234Z/` — created by `_fresh_output_dir` immediately before the network loop via `os.makedirs(..., exist_ok=False)`.

## 6. 16 URLs actually fetched

All in ascending date order; one GET per URL; no retries; no index/listing URL; no negative control:

```
http://data.gdeltproject.org/events/20130907.export.CSV.zip
http://data.gdeltproject.org/events/20140216.export.CSV.zip
http://data.gdeltproject.org/events/20140726.export.CSV.zip
http://data.gdeltproject.org/events/20141231.export.CSV.zip
http://data.gdeltproject.org/events/20151002.export.CSV.zip
http://data.gdeltproject.org/events/20160702.export.CSV.zip
http://data.gdeltproject.org/events/20170402.export.CSV.zip
http://data.gdeltproject.org/events/20171231.export.CSV.zip
http://data.gdeltproject.org/events/20181002.export.CSV.zip
http://data.gdeltproject.org/events/20190703.export.CSV.zip
http://data.gdeltproject.org/events/20200402.export.CSV.zip
http://data.gdeltproject.org/events/20201231.export.CSV.zip
http://data.gdeltproject.org/events/20210702.export.CSV.zip
http://data.gdeltproject.org/events/20220101.export.CSV.zip
http://data.gdeltproject.org/events/20220702.export.CSV.zip
http://data.gdeltproject.org/events/20221230.export.CSV.zip
```

## 7. HTTP outcomes

| # | Nominal date | HTTP status | Outcome class |
|---|---|---:|---|
| 1 | 2013-09-07 | 200 | `200_OK` |
| 2 | 2014-02-16 | 200 | `200_OK` |
| 3 | 2014-07-26 | 200 | `200_OK` |
| 4 | 2014-12-31 | 200 | `200_OK` |
| 5 | 2015-10-02 | 200 | `200_OK` |
| 6 | 2016-07-02 | 200 | `200_OK` |
| 7 | 2017-04-02 | 200 | `200_OK` |
| 8 | 2017-12-31 | 200 | `200_OK` |
| 9 | 2018-10-02 | 200 | `200_OK` |
| 10 | 2019-07-03 | 200 | `200_OK` |
| 11 | 2020-04-02 | 200 | `200_OK` |
| 12 | 2020-12-31 | 200 | `200_OK` |
| 13 | 2021-07-02 | 200 | `200_OK` |
| 14 | 2022-01-01 | 200 | `200_OK` |
| 15 | 2022-07-02 | 200 | `200_OK` |
| 16 | 2022-12-30 | 200 | `200_OK` |

All 16 returned HTTP `200`. Zero redirects (no 301/302/303/307/308). Zero connection errors. Zero non-200 responses.

## 8. Payload files written + SHA-256s

All 18 output files (16 payload zips + `characterization_metadata.json` + `characterization_summary.md`) under the fresh output dir, listed by SHA-256:

| Path | Size (bytes) | SHA-256 |
|---|---:|---|
| `characterization_metadata.json` | 52,289 | `52fc25bdaddc5ea46f07ae4042b4309a4c4c05114d300b14aecc85f04dc2ed6f` |
| `characterization_summary.md` | 1,894 | `dafb3e1de903dc27ed80e8dcc0db185ea234fdf3d4b1e1e2824b6f3cf57910ca` |
| `payload_20130907.zip` | 6,897,193 | `dfbd650c38e94dc5910980a27026a2de01333724846a0a9fff03070ffc91a139` |
| `payload_20140216.zip` | 5,317,303 | `1d7ba5eae70abfc1cc56c893db061df8907f7f5a93629ac2eb71acfca491bf05` |
| `payload_20140726.zip` | 6,910,506 | `f944fdc08626965d739ec213a10f213ce0f019fee216389f0944367203dc2f1b` |
| `payload_20141231.zip` | 8,176,525 | `628a774f9f0785245fd658264ef3b05af38cb4d4691bea3fc2812674cbc9ac49` |
| `payload_20151002.zip` | 15,092,345 | `190c35adc5145619a0579cfb414aa870e1db27587261659e80b4404aec4662f8` |
| `payload_20160702.zip` | 8,996,505 | `fc0905407ba7b84e31e4f57db47ca9aab7d40f61db2a894c22b4effce0b40b19` |
| `payload_20170402.zip` | 7,323,562 | `e50d08d54a77ab6e1060adeaef2a42e91a63f5bab0571a8eb6fab53cf76c5271` |
| `payload_20171231.zip` | 5,369,540 | `6b546c51c989775c86c54f64de67a1fcefec752e42d1b6b4a6108ead650a7aa1` |
| `payload_20181002.zip` | 12,646,369 | `4b09334729c6723dbcd3e4cade0e1b01f43200e1555b29d8dd69a2bc4287f38b` |
| `payload_20190703.zip` | 12,000,973 | `cfcbc041350b324d4342a708697da16e152354f8069caafa095ff9bce06eba60` |
| `payload_20200402.zip` | 10,553,980 | `353c7f02f53d89ea94e9f3df11c149b9f1031701b44e4ea1e46c86da8f619ecb` |
| `payload_20201231.zip` | 6,575,326 | `39c100a1fcf8b213dc5744874fa569b4a4ff6b8009e0b2d0011f6e716d0f4817` |
| `payload_20210702.zip` | 7,534,543 | `bed1ce7f9da15adbe4106a5f4f468a4b35ae1e7dad18d9d19d11b863d2a25bb6` |
| `payload_20220101.zip` | 3,019,713 | `9a46c488e9660fb01f50577e6bc9921771593c52df19105853d1ccebdc208511` |
| `payload_20220702.zip` | 4,109,433 | `e85661551fc905a6c41efc49e341b0a3a7a4808b4ad02110b7fe5cca05b93000` |
| `payload_20221230.zip` | 4,712,089 | `649c90f22f9c1ab66a2cc04951a434945f7b03bbae9a994b221ee8b9af84d29e` |

Total payload bytes preserved: 125,235,905 (≈ 119.4 MiB). All 18 names within `ALLOWED_CHARACTERIZATION_OUTPUTS` ∪ `^payload_<locked-YYYYMMDD>\.zip$`. No extracted CSV. No bytecode pollution. No file outside the timestamp directory. Post-hoc tripwire (`_assert_characterization_outputs_allowed`) returned cleanly.

## 9. Final classification outcome

**`TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY`** (per `a2a8fd5` §10 outcome B).

## 10. Per-file metrics

| Nominal date | HTTP | Bytes | Rows | Distinct SQLDATEs | Nominal rows | Nominal % | Mismatch rows | Mismatch % | Malformed-short | Unparseable | Header anom | Unexpected offsets | 2023+ flag |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 2013-09-07 | 200 | 6,897,193 | 103,712 | 7 | 100,147 | 96.562596 % | 3,565 | 3.437404 % | 0 | 0 | False | 0 | False |
| 2014-02-16 | 200 | 5,317,303 | 77,877 | 7 | 74,947 | 96.237657 % | 2,930 | 3.762343 % | 0 | 0 | False | 0 | False |
| 2014-07-26 | 200 | 6,910,506 | 104,054 | 7 | 100,994 | 97.059219 % | 3,060 | 2.940781 % | 0 | 0 | False | 0 | False |
| 2014-12-31 | 200 | 8,176,525 | 119,196 | 7 | 116,483 | 97.723917 % | 2,713 | 2.276083 % | 0 | 0 | False | 0 | False |
| 2015-10-02 | 200 | 15,092,345 | 228,453 | 6 | 221,966 | 97.160466 % | 6,487 | 2.839534 % | 0 | 0 | False | 0 | False |
| 2016-07-02 | 200 | 8,996,505 | 139,186 | 6 | 135,444 | 97.311511 % | 3,742 | 2.688489 % | 0 | 0 | False | 0 | False |
| 2017-04-02 | 200 | 7,323,562 | 115,267 | 6 | 111,795 | 96.987863 % | 3,472 | 3.012137 % | 0 | 0 | False | 0 | False |
| 2017-12-31 | 200 | 5,369,540 | 84,997 | 6 | 83,357 | 98.07052 % | 1,640 | 1.92948 % | 0 | 0 | False | 0 | False |
| 2018-10-02 | 200 | 12,646,369 | 186,125 | 6 | 180,179 | 96.805373 % | 5,946 | 3.194627 % | 0 | 0 | False | 0 | False |
| 2019-07-03 | 200 | 12,000,973 | 176,753 | 6 | 171,592 | 97.080106 % | 5,161 | 2.919894 % | 0 | 0 | False | 0 | False |
| 2020-04-02 | 200 | 10,553,980 | 150,991 | 6 | 147,011 | 97.364081 % | 3,980 | 2.635919 % | 0 | 0 | False | 0 | False |
| 2020-12-31 | 200 | 6,575,326 | 100,226 | 6 | 97,934 | 97.713168 % | 2,292 | 2.286832 % | 0 | 0 | False | 0 | False |
| 2021-07-02 | 200 | 7,534,543 | 112,291 | 6 | 109,448 | 97.468185 % | 2,843 | 2.531815 % | 0 | 0 | False | 0 | False |
| 2022-01-01 | 200 | 3,019,713 | 49,903 | 6 | 48,853 | 97.895918 % | 1,050 | 2.104082 % | 0 | 0 | False | 0 | False |
| 2022-07-02 | 200 | 4,109,433 | 66,539 | 6 | 65,072 | 97.795278 % | 1,467 | 2.204722 % | 0 | 0 | False | 0 | False |
| 2022-12-30 | 200 | 4,712,089 | 76,868 | 6 | 75,131 | 97.740282 % | 1,737 | 2.259718 % | 0 | 0 | False | 0 | False |

**Expected-offset presence flags per file** (each entry is `0 / −1 / −7 / −30 / −365 / −3650 / +1` presence):

| Nominal date | 0 | −1 | −7 | −30 | −365 | −3650 | +1 |
|---|---|---|---|---|---|---|---|
| 2013-09-07 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** |
| 2014-02-16 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** |
| 2014-07-26 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** |
| 2014-12-31 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** |
| 2015-10-02 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 2016-07-02 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 2017-04-02 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 2017-12-31 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 2018-10-02 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 2019-07-03 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 2020-04-02 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 2020-12-31 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 2021-07-02 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 2022-01-01 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 2022-07-02 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 2022-12-30 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |

`distinct_sqldates = 7` for 2013-09-07 / 2014-02-16 / 2014-07-26 / 2014-12-31 (the four files with T+1 present); `distinct_sqldates = 6` for the other twelve files. Full per-SQLDATE distribution with exact row counts and offsets is in the tracked `characterization_metadata.json` artifact at `52fc25bd…dc2ed6f`.

## 11. Aggregate metrics

**Offset file count** (how many of 16 files contain each offset):

| Offset | Files |
|---:|---:|
| −3650 | 16 |
| −365 | 16 |
| −30 | 16 |
| −7 | 16 |
| −1 | 16 |
| 0 | 16 |
| +1 | 4 |

**Offset row totals** (across all 16 files):

| Offset | Rows |
|---:|---:|
| −3650 | 315 |
| −365 | 15,012 |
| −30 | 9,745 |
| −7 | 16,230 |
| −1 | 10,162 |
| 0 | 1,840,353 |
| +1 | 621 |

Total event rows across all 16 files: **1,892,438** (sum of all bucket totals).

**Mismatch-rate distribution** (across 16 files):

- files: 16
- min: 1.92948 % (2017-12-31)
- max: 3.762343 % (2014-02-16)
- mean: 2.68899125 %
- median: 2.662204 %

Range: 1.93 % – 3.76 % — roughly a 2× ratio, materially tighter than the original 5-file sample's 2.5× range (1.70 % – 4.25 %). The 5-file extremes (2013-04-01 at 4.25 %, 2022-12-31 at 1.70 %) were boundary picks; the 16-file sample's interior measurements bracket the distribution more representatively.

**Denominator evidence**:

- Per-file nominal rows: 100147, 74947, 100994, 116483, 221966, 135444, 111795, 83357, 180179, 171592, 147011, 97934, 109448, 48853, 65072, 75131 (mean ≈ 115,034).
- Per-file lookback (mismatch) rows: 3565, 2930, 3060, 2713, 6487, 3742, 3472, 1640, 5946, 5161, 3980, 2292, 2843, 1050, 1467, 1737 (mean ≈ 3,257).
- Ratio: nominal ≈ 35× lookback on average. The lookback row counts vary much less than nominal counts in absolute terms, supporting the substrate-validation memo `a8a9dd2` §5 denominator-effect hypothesis: variation in mismatch rate is dominated by the nominal-day row count.

**T+1 presence by date**:

| Nominal date | T+1 present |
|---|:---:|
| 2013-09-07 | ✓ |
| 2014-02-16 | ✓ |
| 2014-07-26 | ✓ |
| 2014-12-31 | ✓ |
| 2015-10-02 | ✗ |
| 2016-07-02 | ✗ |
| 2017-04-02 | ✗ |
| 2017-12-31 | ✗ |
| 2018-10-02 | ✗ |
| 2019-07-03 | ✗ |
| 2020-04-02 | ✗ |
| 2020-12-31 | ✗ |
| 2021-07-02 | ✗ |
| 2022-01-01 | ✗ |
| 2022-07-02 | ✗ |
| 2022-12-30 | ✗ |

- **Latest sampled date with T+1**: `2014-12-31`
- **Earliest sampled date without T+1**: `2015-10-02`
- T+1 disappearance window (sampling-bounded): `(2014-12-31, 2015-10-02]` — approximately 9 months, monotonic transition (all 4 subwindow A files have T+1; all 12 later files do not).

**Taxonomy conformance**:

- `all_files_conform_to_expected_taxonomy`: **True**
- `any_unexpected_offset_observed`: **False**
- `files_with_unexpected_offsets`: **[]**

All 16 files exhibit a subset of `{0, −1, −7, −30, −365, −3650, +1}` and **nothing outside** it. Notably, the `−3650` bucket lands on the **exact** integer offset in every one of the 16 files — no leap-year drift from this sample (which contradicts the first-probe annotation of `≈T−3650` for the 2013-04-01 nominal date and suggests GDELT's lookback offsets are constant-day-count rather than calendar-date-arithmetic; the 2013-04-01 first-probe observation of `2003-04-04` was a special case attributable to the very-early publishing-pipeline behavior at GDELT's earliest daily-regime date, not a general substrate property).

## 12. Denominator note

`nominal_percentage` and `mismatch_percentage` in each per-file `parse` block use **total parsed file rows** (i.e., `row_count = len(non-empty lines)`) as the denominator. The formula:

```
nominal_pct  = nominal_row_count  / row_count * 100
mismatch_pct = mismatch_row_count / row_count * 100
```

Where `mismatch_row_count = sum(row_count_at_offset for offset != 0)` and `nominal_row_count = row_count_at_offset_0`.

By construction, if `malformed_short_rows > 0` or `unparseable_sqldate_rows > 0`, then `nominal_pct + mismatch_pct < 100 %` because malformed/unparseable rows are counted in `row_count` (the total) but not in either `nominal_row_count` or `mismatch_row_count` (which are computed from `offset_counts`, populated only from successfully-parsed SQLDATE rows). **In this run, all 16 files have `malformed_short_rows = 0` and `unparseable_sqldate_rows = 0`, so `nominal_pct + mismatch_pct = 100 %` exactly in every per-file row.**

## 13. Interpretation (substrate characterization only)

The characterization confirms the substrate-validation memo's primary hypothesis: GDELT 1.0 daily event files are publishing-window snapshots whose rows are tagged with a fixed integer-day-count lookback taxonomy.

**Findings within the locked plan's scope:**

1. **Offset taxonomy is exact** across all 16 sampled files. Every observed offset is exactly one of `{0, −1, −7, −30, −365, −3650, +1}`. No taxonomy drift; no unexpected offsets. The pre-registered taxonomy from `a8a9dd2` §5 holds at the 16-file scale (5+16 = 21 distinct daily files sampled in total across the first probe and this characterization).
2. **`T+1` has a clean disappearance boundary**. All 4 files in the 2013–2014 subwindow contain `+1`; all 12 files from 2015 onward do not. The boundary lies in the half-open interval `(2014-12-31, 2015-10-02]` — a ~9-month window. The pattern is **monotonic**: no file after 2015-10-02 has T+1, and no file before 2015-01-01 lacks it (within this sample). This satisfies the §10 outcome B clean-boundary criterion.
3. **`-3650` lands exact**. The first-probe annotation `≈T−3650` for nominal `2013-04-01` (observed SQLDATE `2003-04-04`) was a special case at the very first daily-regime publishing date. Across all 16 characterization dates, the 10-year lookback bucket lands on the exact `−3650` integer-day offset. GDELT's lookback offsets are therefore constant-day-count, not calendar-date arithmetic. The corrective patch at `487dadb` (exact-integer pinning, no tolerance window) is validated by this finding: the substrate matches the locked taxonomy exactly.
4. **Mismatch-rate range is narrower than first-probe**: 1.93 % – 3.76 % (16-file mean 2.69 %, median 2.66 %) vs. the original first-probe 5-file range 1.70 % – 4.25 %. The first-probe extremes were subwindow boundary observations; the 16-file interior measurements give a more representative band. Consistent with the substrate-validation memo's denominator-effect hypothesis (nominal-day row counts grow faster than fixed-offset lookback buckets).
5. **Substrate is clean**: zero parser anomalies, zero unparseable SQLDATE rows, zero malformed-short rows, zero 2023+ SQLDATE rows, zero redirects, zero connection errors across all 16 files.

**Consequence per `a2a8fd5` §10 outcome B**: `SQLDATE` re-keying advances; the full-build design memo (which is *not* drafted by this report) must explicitly account for the `T+1` boundary at approximately the 2014/2015 transition. Options for the full-build design include: (a) keep T+1 rows in the early-window subset and treat them as same-day publishing-pipeline carryover; (b) drop T+1 rows uniformly; (c) flag T+1 rows in the daily index without dropping. The choice is not made here.

**Out of scope:**
- No interpretation of the `T+1` boundary's cause is offered (publishing-pipeline change at GDELT, ingestion-window adjustment, etc.).
- No interpretation of the lookback-bucket counts in absolute terms is offered.
- No full daily-count build design is entered.

## 14. No-market-data / no-Step-2 confirmation

- ✅ `no_market_data: true`, `no_step_2: true`, `no_asset_or_return_logic: true`, `no_category_theme_actor_filtering: true`, `no_spike_threshold_tuning: true`, `no_negative_control: true` — all explicitly emitted in `characterization_metadata.json`.
- ✅ No market data was read, written, or referenced during the run.
- ✅ No Step 2 lock or precursor drafting occurred.
- ✅ No spike/burst threshold tuning entered.
- ✅ No category / theme / actor / geography / tone filtering applied.

## 15. Boundary confirmations

- ✅ **No event-file probe re-run**: `scripts/run_lane2_gdelt1_event_file_probe.py` was not invoked.
- ✅ **No count-feasibility run**: `scripts/run_lane2_gdelt1_count_feasibility.py` was not invoked.
- ✅ **No F4 modification**: baselines `41c80c0…624c39d` / `00ce9b2…f5e37552c` preserved.
- ✅ **No recognized-list capture modification**: SHA `84ea721e…fff835fc` preserved (capture opened read-only by `_load_recognized_units` during pre-run substrate validation).
- ✅ **No locked-memo edit**: `a2a8fd5` plan memo unchanged; `a8a9dd2` substrate-validation memo unchanged; `9319d30` execution report unchanged; `e55e09a` design note unchanged; `0b341b4` probe runner unchanged; `845c51c` parser tests unchanged; `e9f8781` characterization implementation unchanged; `487dadb` corrective commit unchanged.
- ✅ **Source/test/config edits limited to one-line enable + one-line restore**: the only commits in this turn that touch source are `3537a62` (enable) and `73a7911` (restore); both modify exactly `scripts/run_lane2_gdelt1_row_date_characterization.py` line 57 (`ROW_DATE_CHARACTERIZATION_AUTHORIZED`); both have `numstat` `1	1`; net diff of the runner across both commits is zero (`git diff 487dadb 73a7911 -- scripts/run_lane2_gdelt1_row_date_characterization.py` is empty).
- ✅ **No 2023+ access**: no URL constructed for 2023+ dates (`_date_to_url` semantics in the runner refuse 2023+ by raising `CharacterizationBoundaryBreach`; none of the 16 locked dates is 2023+); no 2023+ SQLDATE row encountered in any payload.
- ✅ **No extracted CSV files**: `find` over the output dir for `*.csv` / `*.CSV` returned no entries; the runner saves only compressed raw `.zip` bytes.
- ✅ **No redirects**: 0 of 16 responses had a 30x status.
- ✅ **No manual GET**: no `curl` / `wget` / `requests` / browser tools used; all 16 requests originated from `_build_row_date_redirect_disabled_opener` inside the runner.

## 16. Output artifact disposition

Following the **first-probe precedent** (`9319d30`-era output dir `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` remained untracked indefinitely, pending a separate explicit artifact-disposition prompt), the 18 characterization output artifacts at

`results/lane2_gdelt1_event_file_probe/` … wait, `results/lane2_gdelt1_row_date_characterization/20260523T033234Z/`

are **left untracked / unstaged**. This memo / report commits only this `.md` file under `docs/`. The output artifacts persist on local disk only, byte-identical to their post-run state.

The 18 untracked output paths (each with SHA-256 listed in §8 above):

```
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/characterization_metadata.json
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/characterization_summary.md
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20130907.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20140216.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20140726.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20141231.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20151002.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20160702.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20170402.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20171231.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20181002.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20190703.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20200402.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20201231.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20210702.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20220101.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20220702.zip
results/lane2_gdelt1_row_date_characterization/20260523T033234Z/payload_20221230.zip
```

Inspection did **not** reveal characterization-specific repo rules that differ from the probe precedent; the locked plan memo `a2a8fd5` §12 explicitly defers artifact-disposition to "a separate artifact-disposition prompt." Default discipline applies: artifacts remain untracked.

A future artifact-disposition prompt may revisit this decision for either or both output dirs (`results/lane2_gdelt1_event_file_probe/20260522T221241Z/` and `results/lane2_gdelt1_row_date_characterization/20260523T033234Z/`).

## 17. Post-restore tests

- Narrow characterization suite (`tests/test_lane2_gdelt1_row_date_characterization.py`): **62 passed in 0.54s**.
- Paired non-regression suite (characterization + event-file probe): **117 passed in 0.82s**.
- Neither suite drifted from the expected counts (62 / 117).

## 18. Final repo state (after report commit + push)

To be filled by the commit/push step. Expected: `HEAD = origin/main = <report commit SHA>` (the report commit on top of restore commit `73a7911` on top of enable commit `3537a62` on top of pre-cycle anchor `487dadb`).
