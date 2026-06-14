# COMPRESSION — CR EPISODE-COUNT AUDIT AUTHORIZATION v0.1

## Records

Base commit:

`cdf78f136d5930d8bd5b68a7b3c7a6dbcd75040d`

This is the current `HEAD = origin/main` state after the CR distinctness closure decision.

Compression / CR distinctness arc status:

`CLOSED`

Atlas status:

`CR — DISTINCT RANGE-EXTENT FEATURE`

This memo authorizes a future feature-side episode-count audit design and freezes its rules before any audit data contact.

This memo itself does not run the audit.

## Purpose

Count distinct feature-side CR compression episodes in the 2005–2022 sandbox.

The purpose is to gauge whether episode density could even support a separately designed future wake / predictive study.

This audit is feature-side only.

It counts occurrence.

It does not look forward.

It does not test whether compression resolves into expansion.

## Input boundary

Authorized future audit input file:

`data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv`

Expected SHA-256:

`5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901`

Allowed columns exactly:

```text
date
adj_close
```

Allowed date range:

```text
2005-01-01 through 2022-12-31 inclusive
```

Reject immediately if:

- the file hash does not match;
- columns are not exactly `{date, adj_close}`;
- any row is `>= 2023-01-01`;
- any sealed-period value is present.

No OHLC, volume, news, macro, options, cross-asset, or sealed-period inputs are authorized.

## Feature construction

The future audit must import the committed CR construction from:

`scripts/run_compression_second_distinctness_diagnostic_v0_1.py`

Reviewed script SHA-256:

`d7e365dc9412c86680896ea3688c9d9f73c3d66ccd46feae7583388449312380`

Do not reimplement the CR formula inline in the future audit script.

Use trailing 21-close windows ending at `t`.

Definitions:

```text
path_21 = sum(abs(adj_close_i - adj_close_{i-1})) across the 20 intervals in trailing [t-20..t]
range_21 = max(adj_close_i) - min(adj_close_i) over trailing [t-20..t]
CR_21 = range_21 / path_21
CI_21 = -log(CR_21) = log(path_21 / range_21)
```

No wake, outcome, target, future return, future range, future volatility, drawdown, recovery, expansion, or forward-window columns are authorized.

No forward windows are authorized.

## Valid-CI base

A row is CI-valid only if all of the following hold:

- full trailing 21-close window exists;
- `path_21 > 0`;
- `range_21 > 0`;
- `CI_21` is finite.

Expected valid-CI row count is approximately `4511`.

Reason:

- 4531 sandbox input rows were seen in the reviewed diagnostic context;
- 20 warmup rows lack full trailing 21-close windows;
- unlike Diagnostic 2, this audit does not use endpoint displacement, so the two `net_disp_21 == 0` rows that were dropped there should remain CI-valid here, assuming CR itself is valid.

The future audit report must report dropped rows by reason.

## Thresholds frozen now

Primary eligible-compression threshold:

```text
CI_21 >= empirical 90th percentile of CI-valid CI_21 rows
```

Percentile method:

```text
numpy percentile method = "linear"
```

Frozen sensitivity grid:

```text
85th percentile
90th percentile
95th percentile
```

The 90th percentile is primary.

The 85th and 95th percentiles are descriptive sensitivity checks only.

The thresholds may be computed during the future audit because the rules are frozen here.

Thresholds must not be tuned after seeing counts.

## Eligibility, runs, and episodes

Eligible day:

```text
CI_21 >= frozen threshold
```

The inequality is inclusive.

Raw eligible run:

A maximal consecutive run of eligible trading days.

Gaps are measured on the contiguous trading-day index.

Dropped rows occupy a session but are never eligible.

Merge rule:

Raw eligible runs separated by `<= 20` trading sessions are merged into one episode.

Rationale:

The CR window length is 21 closes. Days within 20 sessions have overlapping CR windows and are therefore window-dependent.

The 20-session merge gap is fixed and principled.

It is not tunable.

Episode:

One merged cluster after applying the merge rule.

Episode anchor:

The date inside the merged cluster with maximum `CI_21`.

Tie-break:

Earliest date among tied maximum-`CI_21` rows.

Episode anchors are counted only.

Episode anchors are not retained or used for any forward, predictive, or alignment purpose under this authorization.

Derived invariant:

Final episode anchors should be at least 21 trading sessions apart.

This is a sanity check derived from the merge rule, not a separate tunable rule.

## Independence caveat

In this audit, "independent" means window-non-overlapping.

It does not mean statistically independent or iid.

Compression episodes may cluster in calendar time through volatility clustering.

Therefore, the per-year episode distribution is as load-bearing as the total episode count.

The episode count is a density indicator, not a count of iid observations.

## Required future audit report outputs

If the audit is later run under separate run authorization, the report must include:

- authorization hash;
- sandbox hash;
- input row count;
- input date range;
- CI-valid row count;
- percentile method;
- numeric thresholds at 85th, 90th, and 95th percentiles;
- eligible-day count at 85th, 90th, and 95th percentiles;
- raw eligible-run count at 85th, 90th, and 95th percentiles;
- merged episode count at 85th, 90th, and 95th percentiles;
- primary 90th-percentile episode anchor dates;
- per-episode duration in sessions;
- per-year episode counts;
- min / median / max spacing between episode anchors;
- dropped-row decomposition by reason;
- confirmation no wake/outcome/target was computed;
- confirmation no forward window was used;
- confirmation no gate was run;
- confirmation no alpha was spent;
- confirmation no sealed data was accessed;
- confirmation no predictive claim was made.

## Count-density tiers

The count-density tier is assigned using the primary 90th-percentile threshold only.

The tier is not predictive validity.

The tier is not authorization for a future wake design.

The tier is a pre-frozen density read.

Rationale:

A future predictive design would likely use blocked chronological folds, consistent with this program's prior diagnostic pattern. As a rule of thumb, a 5-fold blocked design needs several independent episodes per fold to be worth designing.

Frozen labels:

```text
N_episodes < 30       → COUNT-INFEASIBLE FOR A FUTURE WAKE DESIGN
30 <= N_episodes < 60 → SPARSE; FUTURE WAKE DESIGN NOT RECOMMENDED WITHOUT EXTRA JUSTIFICATION
N_episodes >= 60      → COUNT-DENSITY ADEQUATE TO REVISIT, NOT AN AUTHORIZATION
```

Approximate fold-density intuition:

```text
N_episodes < 30       → fewer than about 6 episodes per fold
30 <= N_episodes < 60 → about 6 to 12 episodes per fold
N_episodes >= 60      → at least about 12 episodes per fold
```

If the tier differs across the frozen 85th / 90th / 95th grid, the feasibility read is fragile and must be labeled borderline.

Even the top tier defers real feasibility judgment to the future wake design's own power analysis and per-year distribution.

## Wake seal

The future audit authorized by this memo is feature-side `CI_21` only.

It has no forward window.

It has no outcome.

It does not breach the wake seal.

It is still data contact, which is why the rules are frozen here before the audit run.

The Compression claim proper remains sealed:

```text
contained traversal resolves into expansion
```

That is a predictive / wake claim.

This memo does not test or authorize that claim.

## This memo does NOT authorize

This memo does not authorize:

- running the audit;
- writing the audit script;
- reading the raw market data now;
- any data contact beyond a separately relayed future run prompt;
- wake computation;
- outcome computation;
- target computation;
- future-return computation;
- future-range computation;
- future-volatility computation;
- expansion computation;
- drawdown computation;
- recovery computation;
- any forward-window use of episode anchors;
- predictive testing;
- gate;
- alpha spend;
- sealed 2023+ access;
- nonlinear-absorption retest;
- atlas promotion;
- any change to the CR distinctness closure decision.

Each requires separate authorization.
