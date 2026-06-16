# GROUP 9 MISSING-DAYS / CALENDAR-HANDLING INTEGRITY DESIGN AUTHORIZATION MEMO v0.1

## 1. Records

* Base commit: `23f916e739dc6290372d20e6aa256f28f3657b29`
* Class: `Group 9 design authorization memo`
* Target: missing-days / calendar-handling integrity check on the SPY adjusted-close sandbox date index.
* Design only. This memo specifies a future check; it authorizes no run.
* No run is authorized unless a later, separate authorization explicitly states it.
* No price value cells are authorized at the design stage.
* No wake / outcome / target.
* No Gate 2.
* No alpha.
* No sealed data.

## 2. Purpose

This is not an edge lane.

This is not a predictive test.

This is a data-construction integrity check.

Purpose:

* Determine whether the SPY adjusted-close sandbox date index has missing, duplicate, unexpected, unsorted, or calendar-misaligned session dates.
* Protect compression / CR, volatility, trend, path-length, and calendar interpretations from date-index artifacts.
* Protect future wake designs from feature/outcome misalignment.
* Check the map before interpreting the forest, per the committed Group 9 hygiene rule that data-construction forces must be checked before behavioral interpretation.

## 3. Why this check is first

* It covers the full 2005–2022 adjusted-close sandbox, including the pre-2013 portion.
* It is the lowest-contact Group 9 check.
* In a future run, it reads the date index only, not price value cells.
* It protects every 21-close window used by path-shape lanes.
* A missing expected trading session inside a 21-close window can distort window spacing, path interpretation, and feature/outcome alignment.
* It reaches the pre-2013 period, 2005–2012, that the adjusted-close-vs-raw check cannot validate, because raw Close / OHLCV is committed as 2013–2022 only.

## 4. Frozen primary data source

Confirmed from committed docs, specifically Atlas §6.1 line 230, corroborated by the compression and cusp gate reports, not copied from any external instruction:

    File:    data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv
    SHA-256: 5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901
    Columns: date, adj_close
    Observed first / last date: 2005-01-03 / 2022-12-30
    Window class: sandbox-only, no sealed dates

Two confirmed nuances that the future design must carry:

* The committed inventory records the observed first / last dates as `2005-01-03 / 2022-12-30`, not `2005-01-01 / 2022-12-31`. The filename encodes the nominal span `20050101_20221231`; the observed extent is narrower. The design must not assume rows exist on `2005-01-01` or `2022-12-31`.
* Per `research_memory.md:70`, this derived sandbox CSV is SHA-pinned but not committed / tracked, because `data/raw/` is gitignored. A future run reads it from the working-tree location and verifies the SHA against `5cd92502…` before reading anything. The reproducibility guarantee is SHA-pinned source plus committed loader, not a tracked file. Because the file is not tracked, its absence at the expected path is a real and expected failure mode and is a fatal STOP below.

The future run may read only the `date` column from this file unless separately authorized.

It must verify the file’s presence and SHA before reading anything.

Fatal pre-read / read-time STOP conditions:

* source file absent at the expected path;
* source SHA mismatch, meaning not equal to `5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901`;
* missing `date` column;
* unexpected schema if the schema is frozen as exactly `{date, adj_close}`;
* unreadable date column;
* any observed date outside `2005-01-01` through `2022-12-31`;
* any sealed observed date `>= 2023-01-01`.

Intended STOP logic:

If the file is absent, STOP.

If the file is present but the SHA mismatches, STOP.

Do not proceed by regenerating, substituting, or silently finding another file unless a separate authorization explicitly permits that.

Survey-and-report anomalies, not immediate STOP conditions:

* duplicate observed dates;
* unsorted observed dates;
* missing expected sessions;
* unexpected observed sessions that are still inside 2005–2022.

The future run must preserve enough information to count and report duplicate / unsorted rows.

For set comparisons, it may use the unique observed session-date set, while separately reporting duplicate counts and row locations.

It must not silently repair or drop anomalies without reporting them.

## 5. Calendar reference dependency

Near-zero contact does not mean no input.

To know which dates are missing, the design needs a canonical trading-calendar reference giving the expected SPY trading sessions, to compare against the observed sandbox date index.

The reference must represent:

* NYSE / ARCA-style SPY trading sessions;
* exchange-local session dates;
* weekends excluded;
* market holidays excluded;
* scheduled early closes / half-days counted as sessions when SPY has a close;
* unscheduled market closures handled by the reference, not guessed.

Extent of the expected-session reference:

* The expected-session reference for this check should be materialized over the observed sandbox extent, `2005-01-03` through `2022-12-30`, not the filename’s nominal `2005-01-01` through `2022-12-31`.
* This avoids false missing-session reports at the boundaries.
* `2005-01-03` is the observed first session and `2022-12-30` is the observed last session; using this observed extent aligns the comparison to the committed sandbox inventory.
* Any decision to use a broader nominal span must be explicit and justified.

State of the repo, confirmed not inferred:

* No committed canonical expected-session calendar reference exists. Atlas §6.9 says there is no dedicated calendar dataset.
* The only committed calendar policy, Lane 2 acquisition memo §7, makes the snapshot’s own `market_date` index the primary calendar and requires any external trading calendar to be separately pinned or versioned in its own metadata, not assumed.
* Circularity warning: because the committed policy’s “primary calendar” is the price file’s own date index, it cannot be used as the expected side of a missing-days comparison against that same file. That would be tautological and would detect nothing. This check specifically requires an independent expected-session source.
* Therefore the design must specify, freeze, and verify a canonical expected-session source before any run. Do not invent one inline.
* The reference must be versioned and SHA-pinned, or the generated expected-session CSV must be committed / SHA-pinned. A package name plus version alone is insufficient unless the materialized expected-session list is itself frozen, because exchange-calendar packages can change holiday rules across versions.

## 6. Future run design

Design only; do not run.

A future authorized run should:

1. verify repo HEAD and origin;
2. verify primary sandbox CSV presence and SHA against `5cd92502…`;
3. verify the frozen expected-session calendar source SHA;
4. read only the sandbox `date` column;
5. parse dates as exchange-local session dates, not UTC timestamps;
6. apply the bounds and comparison-extent split:

   * Fatal observed-date bounds:

     * reject observed dates outside `2005-01-01` through `2022-12-31`;
     * reject sealed observed dates `>= 2023-01-01`.
   * Expected-session comparison extent:

     * expected sessions are generated over `2005-01-03` through `2022-12-30` unless explicitly authorized otherwise.
7. build the observed session set from sandbox dates, preserving duplicate and row-order diagnostics separately;
8. build the expected session set from the frozen calendar source over the comparison extent;
9. compute:

   * missing expected sessions = expected minus observed;
   * unexpected observed dates = observed minus expected;
   * duplicate observed dates;
   * unsorted observed dates;
   * consecutive missing-expected-session runs in the observed data;
   * per-year counts of missing / unexpected / duplicate issues;
   * 21-close-window exposure counts: how many rolling 21-close windows would contain or border a date-index anomaly;
10. produce a report with counts and affected date ranges only.

No price values read.

No CI / CR computed.

No wake / outcome / target computed.

No trading or predictive conclusion drawn.

Note on consecutive-run accounting:

The expected NYSE / ARCA calendar legitimately contains gaps from weekends, holidays, and unscheduled closures; those expected-calendar gaps are context, not anomalies.

The integrity-relevant metric is whether the observed data is missing one or more consecutive expected sessions.

Multi-session missing runs suggest a dropped chunk and must be distinguished from scattered one-offs.

## 7. Interpretation rules

If zero missing / unexpected / duplicate / unsorted dates:

* record date-index integrity as clean for the `2005-01-03` through `2022-12-30` observed extent under the chosen calendar reference, scope-bounded to that reference;
* do not claim edge;
* do not change CR closure;
* do not change Gate 1;
* do not open Gate 2.

If anomalies exist:

* report them as data-construction issues;
* identify which years and rolling windows are affected, and report consecutive missing-session run lengths;
* do not repair silently;
* do not rerun any prior lane without separate authorization;
* do not make behavioral interpretation until the anomaly is adjudicated.

If the expected-calendar reference is unavailable or not frozen:

* stop before run;
* the design remains authorized-in-principle only;
* no data check is executed.

## 8. Deliverables for future run

When / if a run is later authorized, deliverables should include:

* script path, if later authorized;
* report path, if later authorized;
* exact input SHAs, sandbox CSV plus expected-calendar reference;
* expected-calendar reference SHA;
* count table:

  * observed sessions;
  * expected sessions;
  * missing sessions;
  * unexpected sessions;
  * duplicates;
  * unsorted flags;
  * consecutive missing-session run lengths;
  * per-year issue counts;
  * 21-close-window exposure counts;
* explicit statement that no price value cells were read;
* explicit statement that no wake / outcome / target was computed;
* explicit statement that no alpha or sealed data was used.

## 9. Non-authorizations

This design memo does not authorize:

* execution of the missing-days check;
* reading price value cells;
* reading OHLCV rows;
* computing CI / CR;
* computing features;
* computing wake / outcome / target;
* predictive testing;
* Gate 2;
* alpha spend;
* sealed data access;
* new data acquisition;
* OHLCV inventory;
* atlas promotion;
* changing CR closure;
* changing Gate 1.

## 10. Recommended next step

Because no frozen canonical trading-calendar reference currently exists in the repo, and the only committed calendar policy would create a circular comparison:

Create or identify a frozen canonical trading-calendar reference before authorizing a run.

Concretely: select an external NYSE / ARCA exchange-calendar source, materialize the expected-session list over the observed sandbox extent `2005-01-03` through `2022-12-30`, and commit / SHA-pin that list, meaning the materialized output, not just a package name plus version.

Any decision to use the broader nominal span `2005-01-01` through `2022-12-31` must be explicit and justified.

This memo may be committed after review as the design record, but the missing-days run stays unauthorized until the expected-session reference is frozen and a separate run-authorization turn is issued.

## 11. Open prerequisites binding before any run

1. Frozen expected-session calendar reference does not exist. It must be created / identified and SHA-pinned as a materialized session list over the observed extent `2005-01-03` through `2022-12-30`, broader nominal span only if explicitly justified. Confirmed: Atlas §6.9 says there is no dedicated calendar dataset; Lane 2 acquisition §7 requires external calendars to be separately pinned.
2. Circularity constraint. The committed “primary calendar = snapshot’s own date index” cannot be the expected reference; an independent source is required, or the check detects nothing.
3. Sandbox CSV is gitignored / not tracked, per `research_memory.md:70`. The run depends on the working-tree file being present and matching SHA `5cd92502…`; absence or mismatch is a fatal STOP. No regeneration or substitution without separate authorization.
4. Observed span is `2005-01-03` through `2022-12-30`, narrower than the filename’s nominal `20050101_20221231`. The expected-session comparison must be scoped to the observed extent unless a broader span is explicitly justified, to avoid false missing-day reports at the boundaries.
5. Schema-freeze decision pending: whether `{date, adj_close}` is frozen as an exact schema. This affects whether an extra or renamed column is a fatal STOP.
6. Package-version insufficiency: an exchange-calendar package name plus version alone does not satisfy prerequisite 1; the materialized expected-session list must itself be frozen / SHA-pinned.
