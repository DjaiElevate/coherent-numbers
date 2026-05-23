# Lane 2 GDELT1 row-date mismatch characterization plan v0.1

## 1. Title and state

This memo is a **plan-lock memo only**. It does not authorize GDELT contact, characterization execution, event-file probe re-run, full daily-count build, market data, or Step 2.

| Anchor | Value |
|---|---|
| Current `HEAD` | `a8a9dd261a4d2a26c3b92becca5a51927714232b` |
| Substrate-validation memo | `a8a9dd2` — `docs/lane2_gdelt1_row_date_mismatch_substrate_validation_memo_v0.1.md` (SHA `d12531d…00d5ceb5`) |
| Execution report | `9319d30` — `docs/lane2_gdelt1_event_file_probe_execution_report_v0.1.md` |
| Design-note anchor | `e55e09a` — `docs/lane2_gdelt1_event_file_probe_design_note_v0.1.md` |
| Implementation anchor | `0b341b4` — `scripts/run_lane2_gdelt1_event_file_probe.py` |
| Parser-coverage anchor | `845c51c` — `tests/test_lane2_gdelt1_event_file_probe.py` |
| Recognized-list capture | `4015b97` — `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json` (SHA `84ea721e…fff835fc`) |
| Probe execution chain | `e81208d` (enable) → run → `7c85e3f` (restore) → `9319d30` (report) |
| Count-feasibility precedent | `60ec152 → fe74255 → 9e329c2` |
| First probe output (untracked) | `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` |

Authorization scope of this memo: persistence of one tracked memo file at `docs/lane2_gdelt1_row_date_mismatch_characterization_plan_v0.1.md`. Nothing else.

## 2. Scientific purpose

Characterize whether the observed GDELT 1.0 row-date offset taxonomy

> `T = {0, −1, −7, −30, −365, −3650, (+1)}`

holds across a bounded deterministic sample of additional daily files, and determine whether `REKEY-BY-SQLDATE-CANDIDATE` (substrate-validation memo `a8a9dd2` §6) can advance toward a full daily-count build design.

The characterization must answer:

- **Is the offset taxonomy stable across the 2013–2022 daily universe?** — i.e., do all sampled files exhibit a subset of `{0, −1, −7, −30, −365, −3650, +1}` and no offsets outside it.
- **Is `T+1` present only in early files, and where does it disappear?** — the first probe found `T+1` in 2013–2014 files and absent in 2018-02-14 / 2022-12-31; the disappearance boundary lies somewhere in the unsampled interval.
- **Are there any additional offsets beyond `{0, −1, −7, −30, −365, −3650, (+1)}`?** — a new bucket would force taxonomy revision before `SQLDATE` re-keying can proceed.
- **Are mismatch rates mainly denominator-driven?** — the first-probe pattern (4.25% → 1.70%, 2.5× range) was attributed in `a8a9dd2` §5 to nominal-day row counts growing faster than lookback-bucket counts; broader sampling tests this.
- **Are there file-specific anomalies that would block `SQLDATE` re-keying?** — e.g., a file where the SQLDATE column carries non-event-date semantics, or where the lookback set differs in kind.
- **Does the characterization support proceeding to a full-build design memo, or require recursion?** — see §10 for the pre-registered outcome map.

## 3. Scope

This characterization is **still substrate-only**.

- No market data.
- No asset returns.
- No Step 2.
- No spike-threshold tuning.
- No profitability interpretation.
- No full daily-count build.
- No execution authorized by this memo.

## 4. Input universe

The **§10 recognized-list capture** at

`results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json` (SHA `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`, tracked at `4015b97`)

is the **only source** of eligible dates for this characterization.

**Eligibility filter:**

- daily units only — match `^\d{4}-\d{2}-\d{2}$`, not yearly (`2005`) or monthly (`2006-01`) identifiers;
- within `2013-04-01` through `2022-12-31` (the daily-regime window of the original substrate);
- must be present in `recognized_in_window_units`;
- excluded — known substrate gaps from the §6 caveat (v0.2 memo `57f42cc`):
  - `2014-01-23`
  - `2014-01-24`
  - `2014-01-25`
  - `2014-03-19`
- excluded — already-sampled positive probe dates (first probe at `9319d30`):
  - `2013-04-01`
  - `2014-01-22`
  - `2014-01-26`
  - `2018-02-14`
  - `2022-12-31`

**Total eligible daily units after filter**: 3,558 daily identifiers in the recognized list − 5 already-sampled − 0 gap dates that survived the daily filter (the four 2014 gap dates were absent from `recognized_in_window_units` already and so do not appear in the 3,558 daily units; the eligibility filter still names them so the exclusion is explicit). Net eligible universe ≈ 3,553 daily identifiers.

## 5. Sample design

Pre-register **exactly 16 additional daily files** — bounded enough to remain a characterization, not a full build; large enough to identify per-subwindow behavior beyond the five-file sentinel probe.

Four subwindows × four dates per subwindow:

| Subwindow | Date range (inclusive) | Purpose |
|---|---|---|
| **A** | `2013-04-02` → `2014-12-31` | Test whether `T+1` exists beyond early files and help bracket disappearance |
| **B** | `2015-01-01` → `2017-12-31` | Post-early behavior before the 2018 sentinel |
| **C** | `2018-01-01` → `2020-12-31` | Whether 2018-era behavior generalizes into later pre-2021 files |
| **D** | `2021-01-01` → `2022-12-31` | Late-window behavior near the 2022 sentinel |

**Selection rule within each subwindow:**

1. Filter eligible recognized daily units to the subwindow.
2. Sort ascending by date.
3. Select four deterministic quartile positions by integer floor:
   - pick #1 = index `⌊N · 1/4⌋` (first-quartile lower index)
   - pick #2 = index `⌊N · 2/4⌋` (second-quartile lower index)
   - pick #3 = index `⌊N · 3/4⌋` (third-quartile lower index)
   - pick #4 = index `N − 1` (final available date in subwindow)
4. If a selected date collides with an excluded date, move forward to the next eligible date.
5. If moving forward would cross the subwindow boundary or collisions repeat, move backward to the nearest eligible date in the subwindow.
6. If a pick within a quartet collides with an already-picked date in the same subwindow, apply rule 4 / 5 to the duplicate.

### Computed selection (deterministic, against `recognized_list.json` SHA `84ea721e…fff835fc`)

**Subwindow A** (`2013-04-02` → `2014-12-31`; `N = 635`):

| Pick | Raw index | Date |
|---|---:|---|
| #1 | 158 | `2013-09-07` |
| #2 | 317 | `2014-02-16` |
| #3 | 476 | `2014-07-26` |
| #4 | 634 | `2014-12-31` |

**Subwindow B** (`2015-01-01` → `2017-12-31`; `N = 1096`):

| Pick | Raw index | Date |
|---|---:|---|
| #1 | 274 | `2015-10-02` |
| #2 | 548 | `2016-07-02` |
| #3 | 822 | `2017-04-02` |
| #4 | 1095 | `2017-12-31` |

**Subwindow C** (`2018-01-01` → `2020-12-31`; `N = 1096`):

| Pick | Raw index | Date |
|---|---:|---|
| #1 | 274 | `2018-10-02` |
| #2 | 548 | `2019-07-03` |
| #3 | 822 | `2020-04-02` |
| #4 | 1095 | `2020-12-31` |

**Subwindow D** (`2021-01-01` → `2022-12-31`; `N = 730`):

| Pick | Raw index | Date | Adjustment |
|---|---:|---|---|
| #1 | 182 | `2021-07-02` | — |
| #2 | 365 | `2022-01-01` | — |
| #3 | 547 | `2022-07-02` | — |
| #4 | 729 | `2022-12-30` | **collision adjustment**: raw idx 729 was `2022-12-31` (already-sampled positive probe date); forward exited the subwindow; moved backward to idx 728 → `2022-12-30`. |

### Final 16 dates (sorted)

`2013-09-07`, `2014-02-16`, `2014-07-26`, `2014-12-31`, `2015-10-02`, `2016-07-02`, `2017-04-02`, `2017-12-31`, `2018-10-02`, `2019-07-03`, `2020-04-02`, `2020-12-31`, `2021-07-02`, `2022-01-01`, `2022-07-02`, `2022-12-30`.

All 16 are unique, all are within their subwindow ranges, all are in `recognized_in_window_units`, none collide with the four known substrate-gap dates, none collide with the five already-sampled probe dates.

### Collision adjustments

**One** collision adjustment was needed:

- **Subwindow D pick #4**: raw index 729 (final available date in subwindow) was `2022-12-31` — excluded as an already-sampled positive probe date. Forward move would have exited the subwindow (no dates exist between `2022-12-31` and `2022-12-31`). Per rule 5, moved backward one index to `2022-12-30`, which is eligible (in `recognized_in_window_units`, not in any exclusion set). Recorded.

No other collisions, no duplicate-within-quartet adjustments.

## 6. Future execution URL set

For the future characterization-execution-authorization prompt, each of the 16 selected dates maps to exactly one URL via the event-file pattern:

`http://data.gdeltproject.org/events/YYYYMMDD.export.CSV.zip`

The exact 16 URLs the future execution must produce, in ascending date order:

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

The future execution must use **exactly these 16 URLs and no others**:

- No index/listing URL (`events/index.html`) — out of scope.
- No manual GET via `curl` / `wget` / `requests` / browser tools.
- No second GET for any of the 16 URLs.
- No retries unless explicitly implemented and pre-authorized in the future execution prompt — default is no retries, matching the first-probe discipline.
- **No negative controls** for this characterization — default is none, because the prior probe's negative control (`2014-01-23`) passed cleanly with HTTP `404` and the substrate-gap model is settled. Adding negative controls here would mix concerns; gap-model questions are out of scope of this characterization.

## 7. Metrics to collect in future characterization

The future characterization execution must record, **for each of the 16 files**:

- nominal date (`YYYY-MM-DD`);
- HTTP status code;
- outcome class (one of: `200_OK`, `HTTP_NON_200`, `REDIRECT_BLOCKED`, `CONNECTION_ERROR`);
- compressed payload byte size;
- total parsed rows;
- number of distinct `SQLDATE` values appearing in the file;
- per-`SQLDATE` table:
  - `SQLDATE` (parsed as `YYYY-MM-DD`);
  - row count;
  - offset in integer days relative to nominal date;
  - percentage of total file rows;
- offset-bucket distribution (per-bucket row count and percentage);
- nominal-date row count and percentage;
- mismatch row count and percentage;
- presence/absence of each expected offset: `0`, `−1`, `−7`, `−30`, `−365`, `−3650`, `+1`;
- any unexpected offsets (offsets observed outside the pre-registered taxonomy);
- parser anomalies (`header_anomaly_detected`);
- unparseable SQLDATE rows;
- date-boundary breaches (any `SQLDATE ≥ 2023-01-01` row);
- redirects (with `Location` header if any);
- connection errors (with exception class and message).

**Aggregate metrics across all 16 files:**

- frequency of each offset across files (how many of 16 files exhibit each pre-registered offset);
- total rows by offset across all 16 characterization files;
- mismatch-rate distribution across files (min / median / max / range);
- denominator relationship: nominal-day row count vs. lookback-bucket counts per file, and whether the mismatch-rate variation is driven mostly by nominal-day volume growth (as the first probe's denominator hypothesis predicts);
- `T+1` presence/absence by file date;
- earliest sampled date **without** `T+1` (upper bound on the disappearance window);
- latest sampled date **with** `T+1` (lower bound on the disappearance window);
- whether all 16 files conform to the observed taxonomy `{0, −1, −7, −30, −365, −3650, (+1)}`;
- whether any file contains offsets outside that taxonomy.

## 8. Expected output artifacts for future execution

The future characterization-execution-authorization prompt is expected to produce, at minimum:

- **Machine-readable characterization metadata**: `characterization_metadata.json` (or analogous; the future prompt will lock the exact name).
- **Human-readable characterization summary/report**: `characterization_summary.md` (or analogous).
- **Optionally**: compressed raw payloads for successful HTTP 200 responses, if the future execution prompt authorizes preservation under a §9-style allow-list (analogous to `ALLOWED_PROBE_OUTPUTS`).

This plan-lock memo does **not** authorize creating those artifacts now and does **not** lock the artifact names or allow-list — that is for the future execution-authorization prompt.

## 9. Stop conditions for future characterization execution

The future characterization execution must halt on:

- **2023+ URL construction** → boundary failure (`Protocol2023PlusBreach` semantics);
- **2023+ SQLDATE encountered** in any payload → boundary failure;
- **Any file returns non-200** → retrieval-issue classification (the future execution prompt must decide whether to abort the full sweep or proceed and flag);
- **Any parser anomaly** (`header_anomaly_detected = True`) or non-trivial unparseable-SQLDATE rows → parser-issue classification;
- **Any unexpected offset** outside the pre-observed taxonomy → taxonomy-deviation flag (does NOT auto-halt; recorded for post-run decision);
- **Missing expected offset in many files** → taxonomy-revision candidate flag (does NOT auto-halt; recorded for post-run decision);
- **Output allow-list violation** → boundary failure;
- **Any market-data touch** → firewall breach (must not occur);
- **Any Step 2 touch** → firewall breach (must not occur);
- **Any redirect followed** → firewall breach (the future execution must use a redirect-disabled opener, mirroring the probe script `0b341b4` `_ProbeNoFollowRedirectHandler`).

## 10. Post-characterization decision criteria

Pre-registered outcome map for the future post-characterization decision memo:

### A. `TAXONOMY-STABLE-REKEY-BY-SQLDATE`

- ≥ 15 of 16 sampled files conform to the expected taxonomy `{0, −1, −7, −30, −365, −3650, (+1)}`;
- No unexpected offsets that materially affect interpretation;
- Mismatch-rate variation is consistent with the denominator hypothesis from `a8a9dd2` §5;
- **Consequence**: `SQLDATE` re-keying can advance to a full-build design memo. **Market data and Step 2 remain blocked**; the next step is a *design memo*, not a build run.

### B. `TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY`

- Same conformance as outcome A;
- `T+1` appears in early-subwindow files only and disappears at a bounded transition date observable from the 16-file sample;
- **Consequence**: `SQLDATE` re-keying can still advance, but the full-build design memo must explicitly account for the `T+1` boundary (e.g., by recording the exact disappearance interval as a documented substrate property and deciding whether `T+1` rows are kept, dropped, or specially flagged in the full build). **Market data and Step 2 remain blocked.**

### C. `TAXONOMY-DEVIATION-REQUIRES-REVISION`

- One or more files exhibit an unexpected offset outside `{0, −1, −7, −30, −365, −3650, (+1)}`, OR
- Several files are missing expected lookback buckets in a non-random pattern;
- **Consequence**: the taxonomy must be revised before any full-build design. The post-characterization decision memo specifies the revision and, if needed, a further bounded characterization plan. **`SQLDATE` re-keying does not advance.** Market data and Step 2 remain blocked.

### D. `RETRIEVAL-OR-PARSER-BLOCK`

- One or more files cannot be retrieved cleanly (non-200, redirect, connection error), OR
- One or more files cannot be parsed cleanly (header anomaly, unparseable SQLDATE rows beyond a token count);
- **Consequence**: the retrieval/parser issue must be diagnosed before any further characterization or build. The post-characterization decision memo specifies remediation. Market data and Step 2 remain blocked.

### E. `INSUFFICIENT-CHARACTERIZATION`

- The 16-file plan returns clean results but reveals questions that require additional sampling (e.g., the `T+1` disappearance boundary is wider than expected and needs more samples to bracket);
- **Consequence**: a further bounded characterization plan with a different sample design, or a substrate-decision memo accepting the residual uncertainty. Market data and Step 2 remain blocked.

**No outcome introduces market data or Step 2.** The no-market-data firewall (substrate-validation memo `a8a9dd2` and event-file probe design note `e55e09a` §11) holds across all five outcomes.

## 11. Future authorization requirement

This memo **locks the plan only**. It does **not** authorize the characterization run.

The next step after this memo, if accepted, is a **separate characterization-execution-authorization prompt**. That future prompt must use:

- **Three-guard discipline** matching the count-feasibility runner's three-guard pattern: a module constant (analogous to `EVENT_FILE_PROBE_AUTHORIZED`), a CLI flag, and an environment variable, all required.
- **Enable-then-inert-restore commit cycle** mirroring the relevant precedents:
  - count-feasibility: `60ec152 → fe74255 → 9e329c2`
  - event-file probe: `e81208d → 7c85e3f → 9319d30`
- **Exact 16 selected dates and URLs from this memo** (§5 and §6). The future prompt must cite this memo by SHA (to be the SHA of `a8a9dd2`'s successor commit, recorded once this memo is committed) and pre-register the 16-date list verbatim.
- **No-market-data firewall** — verbatim re-statement.
- **Post-run report requirement** — a tracked execution report (analogous to `9319d30`) must be committed before any push that includes the run.
- **Substrate-pinned recognized-list path** — same as the probe: hardcoded `RECOGNIZED_LIST_PATH = "results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json"`; no override surface.

The future execution prompt may either (a) re-use the existing `scripts/run_lane2_gdelt1_event_file_probe.py` runner with a different `--authorize-…` flag or different `EVENT_FILE_PROBE_AUTHORIZED` semantics, or (b) add a separate `scripts/run_lane2_gdelt1_row_date_characterization.py` runner with its own three-guard discipline. Either path is acceptable; the future execution prompt locks the choice.

## 12. Artifact disposition

The 7 untracked files at `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` (from the first probe run at `9319d30`) **remain untracked** and **are not staged or committed by this memo**. They remain byte-identical to their post-run state.

Any future characterization execution will produce its own output artifacts under its own fresh timestamped directory (e.g., `results/lane2_gdelt1_row_date_characterization/<TIMESTAMP>/` or `results/lane2_gdelt1_event_file_probe/<TIMESTAMP>/`, depending on whether the future execution prompt routes through the existing probe runner or a new runner). Those future artifacts will need their own disposition decision (separate artifact-disposition prompt, mirroring the still-pending decision on the first-probe outputs).

**No output-artifact disposition is authorized here.**

## 13. Boundary confirmation

This memo's drafting and commit turn:

- ✅ No GDELT contact.
- ✅ No live GET.
- ✅ No characterization execution.
- ✅ No event-file probe re-run.
- ✅ No guard flip — `REAL_RETRIEVAL_ENABLED`, `COUNT_FEASIBILITY_AUTHORIZED`, `EVENT_FILE_PROBE_AUTHORIZED` all `False`; shell envs `UNSET`.
- ✅ No market data.
- ✅ No Step 2.
- ✅ No F4 modification.
- ✅ No recognized-list capture modification — the §10 capture was opened read-only via `json.load` during the date-selection computation (§5); the file was not written, mutated, renamed, or moved.
- ✅ No output-artifact modification, staging, or commit — `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` untouched.
- ✅ No design-note / source / test / config edits.
- ✅ No post-§10 diagnostic edit.
- ✅ No full daily-count build entered.

## 14. Next frontier

**Next frontier: characterization-execution-authorization prompt** for the 16-date sweep specified by this memo, **not** execution itself.

- Full daily-count build remains **blocked**.
- Market data remains **blocked**.
- Step 2 remains **blocked**.
- Spike/burst threshold tuning remains **blocked**.
- Output-artifact disposition (both for the first-probe artifacts and for future characterization artifacts) remains **blocked**.
- F4 modification, recognized-list capture modification, guard flips, source/test/config edits, design-note edits, post-§10 staging/commit/edit/delete, 2023+ pre-filter authorization, frozen-snapshot execution, `python3` canonicalization, negative-control payload allow-list change all remain **blocked**.

Market data and Step 2 remain unconditionally blocked until the no-market-data firewall is explicitly retired by a separately authorized memo. The lock memo does not retire it.

Plan locked. Execution awaits a separate explicit prompt.
