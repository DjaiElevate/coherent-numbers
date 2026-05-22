# Lane 2 GDELT1 Event-File Probe Execution Report v0.1

## 1. Title and state

- **Run date / time (UTC)**: 2026-05-22 22:12:41Z (output-dir timestamp; the calendar date in the executing shell's local timezone is 2026-05-23).
- **Design-note anchor**: `e55e09a` — `docs/lane2_gdelt1_event_file_probe_design_note_v0.1.md` (SHA-256 `150c315594a09381214f5af4533d245f93f91e007d849c4a12368a1d38398fba`).
- **Implementation anchor**: `0b341b4` — `scripts/run_lane2_gdelt1_event_file_probe.py` + `tests/test_lane2_gdelt1_event_file_probe.py`.
- **Parser-coverage anchor**: `845c51c` — `tests/test_lane2_gdelt1_event_file_probe.py` (added `_load_recognized_units` direct coverage).
- **Enable commit SHA**: `e81208d6aee36865e2c0f621cb6b8e23e07d7e2e` (subject *"Enable Lane 2 event-file probe run"*; 1 file +1/−1).
- **Restore commit SHA**: `7c85e3fd949cd1909c5901d2a68d70adf3a7eca9` (subject *"Restore Lane 2 event-file probe guard after run"*; 1 file +1/−1).
- **HEAD before this report commit**: `7c85e3fd949cd1909c5901d2a68d70adf3a7eca9`.

## 2. Preflight

| Item | Value |
|---|---|
| `HEAD = origin/main` before enable | `845c51c079c46b53473166b1f08e74d3b731d2ec` |
| Ahead count before enable | `0` |
| Tracked tree status before enable | clean (zero M/A/D/R) |
| Guard state before enable | `REAL_RETRIEVAL_ENABLED=False`, `COUNT_FEASIBILITY_AUTHORIZED=False`, `EVENT_FILE_PROBE_AUTHORIZED=False` |
| Shell env before enable | `LANE2_COUNT_FEASIBILITY_AUTHORIZED=UNSET`, `LANE2_EVENT_FILE_PROBE_AUTHORIZED=UNSET` |
| Recognized-list SHA-256 | `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc` (tracked at `4015b97`) |
| F4 metadata SHA-256 | `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d` (mtime preserved 2026-05-18 18:33:03) |
| F4 summary SHA-256 | `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c` (mtime preserved 2026-05-18 18:33:03) |
| May-22 count-feasibility empty dir preserved | yes — `results/lane2_gdelt1_count_feasibility/20260522T133715Z/` still empty and untracked |
| Event-file probe output parent before run | did not exist (clean slate) |
| Pre-run no-network test result | **55 passed in 0.33s** including `test_load_recognized_units_against_real_committed_capture` |

## 3. Authorization

- This prompt authorized exactly one run.
- Three-guard gate (all three required by `_guards_ok`):
  - module constant `EVENT_FILE_PROBE_AUTHORIZED = True` (flipped via the enable commit `e81208d` at line 52 of `scripts/run_lane2_gdelt1_event_file_probe.py`);
  - CLI flag `--authorize-event-file-probe-run`;
  - env var `LANE2_EVENT_FILE_PROBE_AUTHORIZED=1`.
- `PYTHONDONTWRITEBYTECODE=1` was set for the run.
- The count-feasibility runner (`scripts/run_lane2_gdelt1_count_feasibility.py`) was not invoked.
- No manual `curl` / `wget` / `requests` / browser fetches occurred at any point.

## 4. Deterministic sample

- **Positive sample dates (5)**: `2013-04-01`, `2014-01-22`, `2014-01-26`, `2018-02-14`, `2022-12-31`.
- **Negative control (1)**: `2014-01-23`.
- **Exact six URLs constructed** (event-file pattern only; no index/listing URL):
  - `http://data.gdeltproject.org/events/20130401.export.CSV.zip`
  - `http://data.gdeltproject.org/events/20140122.export.CSV.zip`
  - `http://data.gdeltproject.org/events/20140126.export.CSV.zip`
  - `http://data.gdeltproject.org/events/20180214.export.CSV.zip`
  - `http://data.gdeltproject.org/events/20221231.export.CSV.zip`
  - `http://data.gdeltproject.org/events/20140123.export.CSV.zip`
- **Sample-presence / negative-absence verification**: satisfied by `test_load_recognized_units_against_real_committed_capture` in the `55 passed` pre-run suite — the real committed capture has `len == 3647`; positives `2013-04-01` / `2014-01-22` / `2014-01-26` / `2022-12-31` present; `2018-02-14` selected (preferred over fallback `2018-02-15`); `2014-01-23` absent. The probe script's internal `select_sample` then re-derived the same selection at runtime and would have hard-failed loud if substrate had drifted between test run and execution.

## 5. Run command

```
PYTHONDONTWRITEBYTECODE=1 LANE2_EVENT_FILE_PROBE_AUTHORIZED=1 \
  python3 scripts/run_lane2_gdelt1_event_file_probe.py \
  --authorize-event-file-probe-run
```

- **stdout**: `Event-file probe outputs written under: /Users/jay/Documents/GitHub/coherent-numbers/results/lane2_gdelt1_event_file_probe/20260522T221241Z`.
- **stderr**: empty.
- **Exit code**: `0`.
- `LANE2_EVENT_FILE_PROBE_AUTHORIZED` was unset immediately after.

## 6. Output artifact inventory

- **Output dir**: `results/lane2_gdelt1_event_file_probe/20260522T221241Z/`.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| `probe_metadata.json` | 4,422 | `4ee1f2b524c811545afc0c38f085dc140949d98935950055f5b91c4063d57c08` |
| `probe_summary.md` | 825 | `72b1a34415173413e68e2749989ea3805f7793f614c8b9ac403509733500ef91` |
| `payload_20130401.zip` | 1,729,307 | `73afa42c059be917f457af43c5c3ebbcf7ee985c2d71dc38f3671331f8be24a1` |
| `payload_20140122.zip` | 2,452,590 | `a93beee53a70e0a975cfbf539f4cb263ebc3e6e78b7dcaf8c14c5cc46132a4d3` |
| `payload_20140126.zip` | 5,608,181 | `221207eab29649f527aace7d04eb5af4107bd7cbc9b17aab95f2eb294e588a78` |
| `payload_20180214.zip` | 13,965,452 | `a9bf89e827cbf1a5c6f0f71e55bab5f09e0863806c4b8b71fde707da9998d718` |
| `payload_20221231.zip` | 3,307,531 | `7606fb41365b5efb5cc333dbd0b1563a0dc2a19bdb81c2bcd0e8b88154d585d6` |

- **Allow-list validation**: all 7 filenames are within `ALLOWED_PROBE_OUTPUTS` ∪ `^payload_(\d{8})\.zip$` restricted to the five positive `YYYYMMDD` values. `_assert_probe_outputs_allowed` returned cleanly (no `ProbeBoundaryBreach`).
- **Raw payload disposition**: HTTP 200 positive-sample bodies preserved on disk as compressed `.zip`; total payload bytes 27,063,061 (≈ 25.8 MiB). Bytes received in metadata match file sizes exactly for each positive sample.
- **No extracted CSV**: `find … -name "*.csv" -o -name "*.CSV"` returned no matches.
- **Negative-control body NOT preserved on disk** (design-conformant per §9 of the design note): `payload_20140123.zip` is absent.
- **All output artifacts remain untracked and unstaged**: only the entire `results/lane2_gdelt1_event_file_probe/` directory appears as a single `??` entry in `git status --short`; no individual file was staged or committed.
- **No `__pycache__/` or `.pyc` files created**: `find . -name "__pycache__"` and `find . -name "*.pyc"` returned no entries newer than the script — `PYTHONDONTWRITEBYTECODE=1` held.

## 7. Result summary

**Per-file table:**

| Date | Role | Status | Outcome | Bytes | row_count | match | mismatch | mismatch % | unparseable | header_anomaly | date_validation_pass |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| 2013-04-01 | positive | 200 | `200_OK` | 1,729,307 | 27,758 | 26,577 | 1,181 | 4.25 % | 0 | False | False |
| 2014-01-22 | positive | 200 | `200_OK` | 2,452,590 | 39,737 | 38,241 | 1,496 | 3.76 % | 0 | False | False |
| 2014-01-26 | positive | 200 | `200_OK` | 5,608,181 | 84,672 | 81,569 | 3,103 | 3.66 % | 0 | False | False |
| 2018-02-14 | positive | 200 | `200_OK` | 13,965,452 | 204,859 | 198,467 | 6,392 | 3.12 % | 0 | False | False |
| 2022-12-31 | positive | 200 | `200_OK` | 3,307,531 | 56,040 | 55,087 | 953 | 1.70 % | 0 | False | False |
| 2014-01-23 | negative-control | 404 | `HTTP_NON_200` | 0 | — | — | — | — | — | — | — |

- **Row-count totals (positives only)**: 27,758 + 39,737 + 84,672 + 204,859 + 56,040 = **413,066** event rows across the 5 positive files; of which **399,941** match the nominal file date and **13,125** mismatch.
- **Negative-control status**: HTTP `404` clean substrate-gap response (no `Location` header recorded; no follow). Body not preserved by design.
- **Redirects**: zero. No 301/302/303/307/308 across any of the six attempts; no `Location` header logged on the negative-control.
- **Connection errors**: zero (no DNS/timeout/TCP reset/URLError).
- **Parser anomalies**: zero — `header_anomaly_detected` is `False` for all 5 positive samples; no unparseable SQLDATE rows on any positive sample.
- **Date mismatches**: present on all 5 positive samples at the **1.70%–4.25%** range — the substrate-integrity property that drives the verdict.
- **2023+ boundary status**: clean. No 2023+ URL constructed, no 2023+ SQLDATE row encountered. `Protocol2023PlusBreach` never raised. `SEAL_START = 2023-01-01` guard held both at URL construction (`_date_to_url` not called with any 2023+ date) and at parse-time (zero 2023+ rows in any payload — note that mismatching rows have parseable pre-2023 dates, not 2023+ dates, otherwise the parser would have raised `ProbeBoundaryBreach`).
- **No filtering / market / Step 2 leakage**: metadata explicitly declares `no_market_data: true`, `no_step_2: true`, `no_asset_or_return_logic: true`, `no_category_theme_actor_filtering: true`, `no_spike_threshold_tuning: true`.

## 8. Verdict classification

**`ROW-DATE-MISMATCH`** — verdict assigned by `_compute_verdict` because all 5 positive samples have `rows_mismatching_nominal_date > 0` (non-zero in every case, between 1.70% and 4.25%).

This is one of the design-note §8 verdict tokens, defined as:

> A positive sample file retrieves and parses, but rows do not correspond to the nominal file date.

The five positive samples did retrieve cleanly (HTTP 200, zero parser anomalies, zero unparseable rows, zero connection errors) and the negative control produced a controlled HTTP 404 — but a small consistent fraction of rows in each daily file carries a SQLDATE that differs from the nominal file date. The verdict map's positive-side check fires before the negative-side check, so the negative-control 404 (which would otherwise have produced `FEASIBLE`) is not reached.

Other verdict tokens **NOT** assigned (and why):
- `FEASIBLE` — would have required all 5 positives to have `date_validation_pass=True`; failed because of the mismatching rows.
- `INFEASIBLE-RETRIEVAL` — would have required at least one positive with `REDIRECT_BLOCKED` / `HTTP_NON_200` / `CONNECTION_ERROR`; none occurred.
- `INFEASIBLE-PARSER` — would have required at least one positive with `header_anomaly_detected` or unparseable rows in non-header positions; none occurred.
- `GAP-MODEL-FAILED` — would have required the negative control to return HTTP 200; it returned 404.
- `GAP-MODEL-AMBIGUOUS` — would have required the negative control to return redirect or connection error; it returned a clean 404.
- `BOUNDARY-FAILURE` — would have required a `ProbeBoundaryBreach` exception or a guard-violation pathway; none occurred.
- `FIREWALL-BREACH` — structurally impossible (no market-data surface in the probe).

## 9. Interpretation

The probe surfaced a real substrate-integrity property of GDELT 1.0 daily event files: a small but consistent fraction of rows (~2% on a recent file like 2022-12-31, rising to ~4% on earlier daily files) carry a `SQLDATE` that does not match the nominal date of the file in which they appear. This is consistent with documented GDELT 1.0 behavior whereby published-date and event-date can diverge; the script's strict §6 contract ("rows correspond to the file's nominal date") treats any divergence as failing date-validation.

Under the design note's verdict-map semantics (§8), `ROW-DATE-MISMATCH`:

- **raises a substrate-integrity question** that must be resolved before any larger daily-count build;
- **blocks the daily aggregate signal** under the current parser contract until investigated;
- **may require a new substrate-validation memo** before any larger fetch — the resolution path could be (a) accept the mismatch and define a stricter aggregation rule (e.g., index events by their actual `SQLDATE`, not by the file name); (b) accept the mismatch and define a tolerance threshold; (c) treat per-file mismatch rates as a substrate property to characterize across the full universe before deciding;
- **does not update the market/attention hypothesis** in any direction.

The probe surfaced no other issue: no retrieval failure, no parser anomaly, no 2023+ leak, no redirect, no connection error, no firewall breach. The substrate-integrity finding is the sole load-bearing outcome.

No design step beyond classification is taken here. No market data is introduced. No threshold is tuned. No reinterpretation of the verdict to "rescue" the result is attempted.

## 10. Audit-thinness disclosure

Per design note §9, the negative-control payload is **not preserved on disk by design** even if HTTP 200 is returned (which did not occur here — the actual negative-control status was 404).

For this run, `GAP-MODEL-FAILED` did **not** fire (the negative control returned a clean HTTP 404, not 200), so the audit-thinness path is not exercised. The disclosure remains relevant for future runs: if `GAP-MODEL-FAILED` ever fires, body-level evidence would require a separate diagnostic authorization; the allow-list must not be broadened during the execution-authorization flow.

## 11. Guard restoration

- **Restore commit SHA**: `7c85e3fd949cd1909c5901d2a68d70adf3a7eca9` (subject *"Restore Lane 2 event-file probe guard after run"*; single one-line change to `scripts/run_lane2_gdelt1_event_file_probe.py` reverting `EVENT_FILE_PROBE_AUTHORIZED = True → False`).
- **Final on-disk guard state**: `EVENT_FILE_PROBE_AUTHORIZED = False` (line 52), `REAL_RETRIEVAL_ENABLED = False` (`src/lane2_gdelt1_count_feasibility.py:647`), `COUNT_FEASIBILITY_AUTHORIZED = False` (`scripts/run_lane2_gdelt1_count_feasibility.py:49`).
- **Shell env unset**: `LANE2_EVENT_FILE_PROBE_AUTHORIZED=UNSET`, `LANE2_COUNT_FEASIBILITY_AUTHORIZED=UNSET`.
- **Push policy held**: no `git push` was executed while `EVENT_FILE_PROBE_AUTHORIZED = True`. Both the enable commit and the run completed locally before the restore commit; the final push happens only after this report commit.
- **Post-restore no-network test**: **55 passed in 0.33s** (re-run of the full probe test suite confirms restoration is clean and the test surface still parses the real capture).

## 12. Boundary confirmation

- ✅ No Gate 5 execution.
- ✅ No count-feasibility execution (`scripts/run_lane2_gdelt1_count_feasibility.py` not invoked).
- ✅ No market data read, written, or referenced.
- ✅ No Step 2 lock or precursor drafting.
- ✅ No F4 modification — F4 baseline SHAs `41c80c0…624c39d` / `00ce9b2…f5e37552c` match exactly; mtimes preserved at 2026-05-18 18:33:03.
- ✅ No recognized-list capture modification — SHA `84ea721e…fff835fc` preserved.
- ✅ No design-note / source / test / config edits except the two one-line guard commits (`e81208d` enable, `7c85e3f` restore). Net diff of the script across both commits = `0` lines (back to baseline).
- ✅ No `ALLOWED_PROBE_OUTPUTS` / negative-control payload allow-list change.
- ✅ No post-§10 diagnostic report (`docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`) edit, stage, or commit.
- ✅ No memory edit — `MEMORY.md` and `project_lane2_attention_spike.md` mtimes preserved at 2026-05-22 22:30.
- ✅ No manual GET — no `curl`, `wget`, `requests`, browser tools, or ad hoc network commands.
- ✅ No index/listing GET — `_date_to_url` only constructs event-file URLs; `index.html` not contacted.
- ✅ Zero retries — exactly six GET attempts, one per pre-registered URL. The script does not retry, and none was invoked manually.
- ✅ No output artifact staged or committed — `git status --short` shows `?? results/lane2_gdelt1_event_file_probe/` as a single untracked entry; no file under that path is in `git diff --cached`.
- ✅ No push while `EVENT_FILE_PROBE_AUTHORIZED = True`.
- ✅ No bytecode pollution — `PYTHONDONTWRITEBYTECODE=1` set for the run; no new `__pycache__/` directories or `.pyc` files were created (`find` returned no matches newer than the script).
- ✅ May-22 count-feasibility empty dir (`results/lane2_gdelt1_count_feasibility/20260522T133715Z/`) still present, empty, untracked.

## 13. Next frontier

The verdict is `ROW-DATE-MISMATCH` — not `FEASIBLE`. Per design note §8 the next-eligible workstream is a **separate substrate-validation memo / decision** that resolves the row-date-mismatch finding before any larger daily-count build. This memo would need to:

- characterize whether the ~1.7%–4.25% mismatch rate is consistent across the full 3,558-daily universe or varies by date / regime;
- decide how the full daily-count build should treat mismatching rows (re-key by `SQLDATE`, accept a tolerance, or reject the parser contract as written);
- specify whether the design note §6 strict "rows correspond to the file's nominal date" contract is preserved, relaxed, or replaced;
- pre-register the resolution in a tracked memo **before** any larger fetch or any market data is introduced.

It does **not**:
- introduce market data;
- enter Step 2;
- tune spike/burst thresholds;
- broaden the `ALLOWED_PROBE_OUTPUTS` allow-list;
- modify F4 / the recognized-list capture / the post-§10 diagnostic report;
- automatically unlock a full daily-count build.

Probe execution itself is **closed** by this report. The output artifact directory `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` and its 7 files remain untracked pending a separate **artifact-disposition prompt** (if you want the payloads tracked alongside the F4 / §10 baselines as audit evidence of this run, that would be a separate explicit authorization).

Pending blocked items not unlocked by this run: event-file probe re-run; Gate 5 execution; count-feasibility re-run; market data; Step 2; second GET; capture; F4 modification; guard flips; source/test/config edits beyond the two one-line guards; design-note edits; recognized-list capture modification; post-§10 diagnostic report staging/commit/edit/delete; 2023+ pre-filter authorization; frozen-snapshot execution; `python3` canonicalization; spike/burst threshold tuning; negative-control payload allow-list change.
