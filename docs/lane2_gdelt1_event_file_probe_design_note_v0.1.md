# Lane 2 GDELT1 Event-File Probe Design Note v0.1

## 1. Purpose

Lane 2 is trying to understand the market/attention relationship by first testing whether a frozen, audit-safe GDELT event-count substrate can support a valid attention-signal instrument before any market data is touched.

The next practical question is not yet market comparison. It is:

**Can we retrieve and count a tiny sample of daily GDELT event files from the frozen daily-resolution universe, in a way that could later support a daily aggregate attention-count series?**

This note defines the first small feasibility test. It does not authorize execution, network calls, source additions, guard flips, code changes, market data, Step 2, or signal testing.

## 2. First attention-count object

The first target attention object is:

**Daily aggregate GDELT event count over the frozen daily-resolution substrate.**

The relevant frozen daily universe is:

- `3,562` planned daily units;
- `3,558` observable daily files in the §10 recognized universe;
- `4` known substrate gaps:
  - `2014-01-23`
  - `2014-01-24`
  - `2014-01-25`
  - `2014-03-19`

The first full signal would eventually be a daily time series of raw event counts. No categories, themes, actors, geography filters, spike thresholds, market windows, assets, or returns enter at this stage.

## 3. Sample selection rule

The first feasibility test uses a **5 + 1 deterministic sentinel design**.

The `K = 5` positive sample contains observable daily files only. These are intended to test normal retrieval, boundary behavior, and broad date coverage.

Positive sample candidates:

1. `2013-04-01` — first daily-regime unit.
2. `2014-01-22` — recognized day immediately before the known `2014-01-23/24/25` substrate gap.
3. `2014-01-26` — recognized day immediately after the known substrate gap.
4. `2018-02-14` — lower median planned daily date.
5. `2022-12-31` — final in-window daily unit.

Negative-control probe:

- `2014-01-23` — known substrate gap; not part of the positive `K = 5` attention-count input.

## 4. Sample-date preflight rule

Before any fetch authorization, all five positive sample dates must be verified against the §10 capture's `recognized_in_window_units`.

If any of the four structurally pinned dates is absent, the test halts before fetch authorization:

- `2013-04-01`
- `2014-01-22`
- `2014-01-26`
- `2022-12-31`

The mid-window date has a special rule because the planned daily partition has an even number of dates, so the median has two equally valid candidates:

- use lower median `2018-02-14` if present;
- if absent, use upper median `2018-02-15`;
- if both are absent, halt and revise the sample design.

The mid-window point exists only to probe a typical ordinary in-window daily file with no special boundary properties. That is why it has a median fallback while the boundary-defined dates do not.

The negative-control date `2014-01-23` must be confirmed absent from `recognized_in_window_units` before fetch authorization.

## 5. Fetch contract sketch

The feasibility test requires exactly `6` attempted per-file GETs:

- `5` positive observable daily files;
- `1` negative-control substrate-gap probe.

The negative-control attempt counts as a GET.

No retries are assumed in this design note. Retry rules, spacing between GETs, exact URL construction, storage policy, and guard handling must be specified later in a separate fetch-authorization prompt.

Expected URL pattern is likely one daily event-file URL per date, for example:

`http://data.gdeltproject.org/events/YYYYMMDD.export.CSV.zip`

The final authorization prompt must verify the exact URL pattern from the repository or GDELT file convention before executing.

## 6. Parser and row-count contract

A clean positive retrieval requires more than HTTP success.

For each positive sample file, the test must verify:

- file can be retrieved;
- file can be opened/decompressed if zipped;
- rows can be parsed;
- raw event-row count can be computed;
- rows correspond to the file's nominal date.

GDELT 1.0 `export.CSV` event files are treated as **headerless positional files** for this test. Therefore:

- the event count is the number of parsed data rows;
- no header row is subtracted by default;
- if a header-like first row is detected, that is a parser anomaly and must be reported rather than silently handled;
- the test must not switch between "count all rows" and "count rows minus header" after seeing file contents.

Date validation is required. If a file named for `2014-01-22` returns rows that do not correspond to `2014-01-22`, the retrieval is not clean.

For the first feasibility test, count **all event rows**. Do not filter by theme, actor, geography, tone, category, or market relevance.

## 7. Negative-control contract

The negative-control probe is diagnostic, not part of the attention-count input.

Probe:

`2014-01-23`

Expected interpretation:

- A clean substrate-gap result means no usable event file for `2014-01-23` is retrieved.
- Acceptable controlled failure shapes may include HTTP `404` or another clear non-success response showing the file is absent.
- HTTP `200` with valid rows for `2014-01-23` means `GAP-MODEL-FAILED`.
- Redirect/substitution to another date is not clean.
- Connection-level failures such as DNS failure, timeout, TCP reset, or local network failure are not acceptable evidence for the substrate-gap model, because they do not distinguish "file absent" from "network broken."

## 8. Expected outcomes and consequence chain

A clean feasibility result requires:

- all five positive sample files retrieve successfully;
- all five parse successfully;
- all five produce positive row counts;
- all five pass date validation;
- no header anomaly is detected;
- the negative-control gap probe fails in a controlled, interpretable way;
- no market data, Step 2, category filtering, spike thresholding, or market-facing logic is touched.

Outcome classes:

### `FEASIBLE`

Definition:

- all five positive files retrieve, parse, count, and date-validate cleanly;
- the negative-control gap behaves as a controlled absence;
- no firewall or boundary rule is violated.

Consequence:

- unlocks design of the full daily-count build over the `3,558` observable daily files;
- does not unlock market data;
- does not unlock Step 2;
- does not unlock spike/burst thresholding;
- next workstream is a full daily-count build design or authorization memo.

### `INFEASIBLE-RETRIEVAL`

Definition:

- one or more positive sample files cannot be retrieved cleanly.

Consequence:

- blocks the daily aggregate attention-count build;
- requires diagnosis of whether failure is URL construction, archive availability, permissions, network, or substrate drift;
- may point toward a revised fetch model, frozen-file snapshot strategy, or 2023+ pre-filter path;
- does not update the market/attention hypothesis.

### `INFEASIBLE-PARSER`

Definition:

- files retrieve but cannot be decompressed, parsed, row-counted, or interpreted under the headerless positional-file contract.

Consequence:

- blocks the attention-count build until parser contract is revised and tested;
- any parser revision must be locked before market data enters;
- no market data or signal derivation becomes eligible.

### `ROW-DATE-MISMATCH`

Definition:

- a positive sample file retrieves and parses, but rows do not correspond to the nominal file date.

Consequence:

- raises a substrate-integrity question;
- blocks the daily aggregate signal until investigated;
- may require a new substrate-validation memo before any larger fetch.

### `GAP-MODEL-FAILED`

Definition:

- the negative-control date `2014-01-23` returns a valid event file with rows corresponding to `2014-01-23`.

Consequence:

- re-opens the known-substrate-gap model from the Gate 4C / §6 caveat chain;
- requires revisiting the four-gap interpretation before full daily-count build;
- does not invalidate the five positive retrievals by itself, but blocks using the gap model as locked.

### `GAP-MODEL-AMBIGUOUS`

Definition:

- the negative-control probe fails in a way that does not distinguish "file absent" from "network or infrastructure problem," such as DNS failure, timeout, TCP reset, or local connectivity failure.

Consequence:

- does not confirm or refute the substrate-gap model;
- may justify a separately authorized retry or diagnostic probe;
- does not unlock full daily-count build on its own.

### `BOUNDARY-FAILURE`

Definition:

- the test attempts to cross a prohibited boundary: market data, Step 2, second GET beyond the authorized per-file attempts, capture wrapper, unapproved retry, guard violation, or unapproved file mutation.

Consequence:

- halt;
- no downstream work becomes eligible;
- requires a boundary report or corrective memo before continuing.

### `FIREWALL-BREACH`

Definition:

- market data, asset labels, returns, market windows, or market-facing comparison logic enters the test.

Consequence:

- invalidates the test for Lane 2 instrument-building purposes;
- requires halt and separate remediation;
- no attention signal can be considered locked from that run.

A clean result only proves that the daily aggregate attention-count object is technically feasible to build from a small sample. It does not yet prove that the full attention series is built, that spike logic is valid, or that any market relationship exists.

## 9. Probe implementation strategy

The feasibility probe should use a small standalone probe script, not the existing count-feasibility runner.

The existing count-feasibility runner is designed around GDELT index-listing feasibility. The `5 + 1` test is different: it fetches specific event-file URLs from the already frozen daily-resolution universe. Reusing the index-listing runner would blur two scopes that the Lane 2 chain has kept separate.

The implementation should therefore be a standalone probe script under `scripts/`.

Preferred path:

`scripts/run_lane2_gdelt1_event_file_probe.py`

The script should:

- construct exactly the six authorized per-file URLs;
- use a redirect-disabled opener built locally inside the probe script;
- not reuse Gate 4D's index-listing opener unless separately justified;
- apply a per-GET timeout, default `30` seconds;
- make no index/listing GET;
- make no event-file GET outside the six authorized dates;
- write only into a fresh timestamped directory under:
  `results/lane2_gdelt1_event_file_probe/<timestamp>/`
- write only:
  - `probe_metadata.json`
  - `probe_summary.md`
  - compressed raw payloads for HTTP `200` positive sample responses
- not write extracted CSV files;
- not touch the count-feasibility runner;
- not modify F4;
- not touch market data;
- not touch Step 2.

The redirect policy is:

- no redirects are followed;
- `301`, `302`, `307`, and `308` responses are recorded with status and `Location`;
- redirected responses are not considered clean retrievals;
- redirect classification is handled in the probe result.

The output discipline should be enforced by the standalone script itself. The script should define an inline output allow-list, for example `ALLOWED_PROBE_OUTPUTS`, and should check every intended output path against that allow-list before writing. This mirrors the count-feasibility runner's output-discipline pattern without modifying the existing runner or its `ALLOWED_OUTPUT_BASENAMES`.

## 10. Authorization sequence

This design note authorizes no execution and no source addition.

The sequence after this note is:

1. Track this design note as a small artifact.
2. Separately authorize a probe-script implementation step:
   - add the standalone script;
   - include the local redirect-disabled opener;
   - include the output allow-list;
   - add tests or conformance checks if needed;
   - commit the script.
3. Separately authorize execution of the committed script.
4. After execution, decide whether a full daily-count build design is eligible.

None of those steps is entered by this design note.

## 11. Firewall

The no-market-data firewall remains the central rule.

This feasibility test must not include:

- market data;
- asset selection;
- return windows;
- Step 2;
- market comparison;
- predictive labels;
- spike/burst threshold tuning;
- category/theme/actor filtering.

Any later burst/spike rule must be specified in a tracked memo before market data enters. No threshold may be tuned after seeing market correlations.

## 12. Final design stance

The first event-file feasibility test should be a **5 + 1 deterministic sentinel test**:

- `5` observable daily files to test retrieval, parsing, row counting, and date validation;
- `1` known substrate-gap probe to test the gap model;
- zero market data;
- zero signal-threshold tuning;
- zero category filtering.

The implementation should use a standalone probe script at `scripts/run_lane2_gdelt1_event_file_probe.py`, with its own redirect-disabled opener and output allow-list. The next workstream is not execution yet; it is the probe-script implementation/authorization step. This design note authorizes neither source addition nor execution.
