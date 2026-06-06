# Lane 2 — TTG → SPY Outcome-Source Pin (provenance amendment) — v0.1

> Status: provenance-only amendment. This commit is doc-only. No market-data fetch, no network, no returns, no
> labels, no target construction, no join, no statistics, no evaluation, and no TTG archive read were performed.
> The single in-sample read remains unspent. No price values are recorded in this document or its byte-review bundle.

## Purpose

This amendment **resolves the `[TO-PIN-BEFORE-EXECUTION]` outcome-data blocker** named in the locked
pre-registration `docs/lane2_ttg_spy_prereg_v1.1.md` (prereg commit
`84068784a195d1f7a8966d57dcba52a725413e29`). It does so **by separate amendment** — it does **not** edit the
locked prereg text. The prereg `§A. Outcome / target definition` requirement that "the future dispatch must first
freeze and hash the outcome file before any label construction, recording the SHA here" is satisfied by this pin.

Label construction, returns, joins, and evaluation remain **unauthorized** and **not performed**; they are deferred
to a separate, separately-vetted execution dispatch.

## Pinned outcome source

| Field | Value |
|---|---|
| Instrument | SPY |
| Source / provider | Yahoo Finance — historical daily data |
| Retrieval method | Operator manual download from Yahoo Finance historical data (no network or fetch performed by this commit) |
| Snapshot date (from filename) | 2026-06-06 |
| Pin / as-of timestamp (UTC) | 2026-06-06T05:22:19Z |
| Raw file path | `data/raw/market/spy_yahoo_adjclose_20130402_20221230_snapshot_20260606.csv` |
| Raw file gitignored | Yes — `git check-ignore` matches `.gitignore:10 data/raw/`; the raw CSV is **not committed** |

## Frozen file identity

| Field | Value |
|---|---|
| SHA-256 | `2842647c318c95bd02bc888ee70361d8242ddf8223281e49a8231ea3d91aa055` |
| Byte size | 185,162 bytes |
| Physical lines | 2,458 (1 header + 2,457 data rows; no trailing newline — structural property recorded, file not modified) |
| Data row count | 2,457 |

## Structural / schema checks (no price values read)

| Check | Result |
|---|---|
| Column count | 7 |
| Column headers (verbatim) | `Date,Open,High,Low,Close,Adj Close,Volume` |
| Adjusted-close header (verbatim) | `Adj Close` |
| Adjusted-close column identity | column index 6 (1-based), header `Adj Close` |
| Date column identity | column index 1 (1-based), header `Date` |
| First data date | `2013-04-02` |
| Last data date | `2022-12-30` |
| Date span covers required `2013-04-02 … 2022-12-30` | Yes (exact span) |
| Ordering (as stored) | ascending |
| Monotonicity | strictly increasing on the `Date` column |
| Duplicate dates | 0 |
| Pre-window rows (`< 2013-04-02`) | 0 |
| `2023-01-01+` rows | 0 (no 2023+ data present; no 2023+ contact) |
| Structural-gap / trading-day sanity | 2,457 daily rows over `2013-04-02 … 2022-12-30` is consistent with the US equity trading-day count for that span (weekends/market holidays absent by construction; no calendar reconstruction performed) |

The raw file is **not reordered or modified**; the ascending ordering is recorded as a structural property only.

## Notes (documentation, not value-derived claims)

- **Corporate-action adjustment:** the provider's `Adj Close` column is intended as a split- and dividend-adjusted
  (adjusted total-return-style) close. The file itself does not state its adjustment methodology; this is recorded
  as a **provider-documentation note**, not a value-derived or computed claim.
- **Timezone / calendar:** US equity trading-day daily bars, on the provider's (Yahoo Finance) supplied calendar,
  as delivered. No timezone or calendar transformation was applied.
- **Used-span bound:** the prereg consumes `2013-04-02 … 2022-12-30`; under the prereg right-edge rule the final
  label uses `T+1`, so the last usable label date is the penultimate available trading day and label construction
  never requires 2023 SPY data.

## Boundary declaration

- No price values, returns, labels, targets, joins, plots, statistics, or evaluations are recorded here or were
  computed.
- No market-data fetch and no network were used; the file was inspected in place as an existing local artifact.
- No TTG archive bytes were read; no features were extracted; no V1/V2 execution was touched; no `2023+` data was
  contacted.
- The raw SPY CSV remains gitignored and is **not committed**; only this provenance amendment doc is committed.
- This pin authorizes nothing further on its own. A subsequent separately-vetted execution dispatch must, per the
  locked prereg, re-verify the archive SHA, use this pinned outcome SHA, execute the single non-adaptive feature
  read, and touch the holdout once. Until then the read remains unspent and the archive remains value-blind.
