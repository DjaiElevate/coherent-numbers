# Lane 2 Market-Data Acquisition Design Memo v0.1

Design-only memo. Pre-registers **Input B** — the market-data source, instrument,
field set, adjustment discipline, trading calendar, 2023+ seal, freeze/pin
discipline, and conformance gate — for the future Lane 2 market-data join. It
selects and justifies the acquisition **before any market data is accessed**. It
fetches nothing, reads nothing, joins nothing, and constructs nothing.

Evidence legend: **[O]** observed git/fs · **[A]** artifact-derived (committed
Step 2 / join-memo blobs) · **[I]** design recommendation.

---

## 1. Non-authorization statement

This memo is design-only and **non-authorizing**. Explicitly, it does **not**
authorize:

- market-data access of any kind;
- fetching or downloading prices, bars, or any market series;
- reading local market-data files;
- calling `yfinance`, any market/data API, BigQuery, or any data provider;
- market-data acquisition execution (the freeze run);
- market-data join implementation;
- market-data join execution;
- instrument construction;
- return / outcome / target / signal / CAR / abnormal-return / volatility /
  PnL / label construction;
- GDELT access or row export.

It **only designs** the future market-data acquisition freeze. Each of
acquisition, join implementation, join execution, and instrument construction
remains a separate, independently authorized future gate with its own preflight,
design memo, and conformance gate.

Distinct phases, **not** to be collapsed [I]:

**design (this memo) → market-data acquisition implementation design + auth →
acquisition / freeze (SHA-pinned snapshot) → join implementation design → join
implementation → join pre-execution conformance gate → join execution → (separately)
instrument-construction design → …**

## 2. Canonical upstream inputs (pinned)

- repo HEAD = origin/main = `df9089bccd219758a523e7724230fbbb46439603` (0/0,
  tree clean) [O].
- Market-data **join** design memo (the consumer of Input B) [O][A]:
  - `docs/lane2_market_data_join_design_memo_v0.1.md`
  - SHA-256 `3a11945c8f04372365d09b2ed23a6c6da1e3581f79b9faeec58fecb355263b21`
  - 406 lines, 23,662 bytes
- **Input A** (the GDELT side the join aligns to), committed Step 2 output [O][A]:
  - directory: `results/lane2_gdelt1_step2_daily_features/20260531T020244Z/`
  - `step2_daily_features.csv` SHA-256
    `48a64e1cfbcffc4b1e89ef65cb91fa07d928b31a2cb1ffdedcdb2a75cd2aef4d`
    (3563 lines = 1 header + 3562 data rows; 2,924,972 bytes)
  - `step2_metadata.json` SHA-256
    `67436f9412eac29e7876bfb661c23040759b6a78b1ed72f7c9da4f41be640b11`
    (133 lines; 5,076 bytes)
  - `step2_summary.md` SHA-256
    `80211a0626a4fb466db6ad4c7fe12b1d486e4b1d9d3a54e48a8c4740ad335d53`
    (37 lines; 1,516 bytes)
- Step 2 domain [A]: `2013-04-01` through `2022-12-31` (3562 unique civil days).
- Step 2 schema [A]: **69 GDELT-only columns**; no market / outcome / return /
  target / price / ticker / volatility / instrument / PnL column; `2022-11-10`
  documented-exception row preserved; four KSG rows preserved.
- Guards [O]: `STEP2_EXECUTION_AUTHORIZED = False @ line 53`;
  `FULL_BUILD_AUTHORIZED = False @ line 95`; `KNOWN_SUBSTRATE_GAPS @ line 163` =
  `2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`.

Input B must be aligned to Input A's domain (§8) and consumed only under the
join memo's §4 alignment rule and §8 conformance gate; this memo defines the
source that produces Input B, not the join.

## 3. Input B selection — market instrument (LOCKED)

**Primary instrument (v0.1 Input B): `SPY`** — the SPDR S&P 500 ETF [I].

- **Role:** broad U.S. equity-market proxy for the first Lane 2 market-response
  join (the S&P 500 response axis named in the Step 2 readiness memo §6).
- **Rationale [I]:**
  - highly liquid, continuously traded over the full `2013-2022` window;
  - long, complete daily history covering `2013-04-01`..`2022-12-31`;
  - compatible with prior project context using SPY / ETF daily series
    (SPY adjusted-close frozen artifacts elsewhere in the program);
  - suitable as the first market-response substrate before any broader-universe
    expansion.

**v0.1 Input B is exactly one instrument: `SPY`.** The instrument is **not**
left ambiguous.

**Possible future extensions (named, NOT acquired here):** `EFA`, `EEM`, `GLD`,
`TLT`. These are mentioned only to scope the roadmap. They are:

- **not** acquired by this memo;
- **not** part of v0.1 Input B;
- admissible only via a later design memo (or an explicit, separately approved
  multi-instrument section added to this memo) that locks the full list and
  justifies each addition. No multi-instrument expansion is chosen here.

## 4. Vendor / source selection — design only

- **Source / vendor [I]:** Yahoo Finance data, accessed via the `yfinance`
  Python package in a **future, separately authorized** acquisition turn.
- **Source object:** daily historical market bars for `SPY`.
- **No API call or fetch occurs in this memo.** No `yfinance` import or
  invocation is performed here; this memo only names the intended source.

State [I]:

- this memo does **not** verify live availability of Yahoo Finance / `yfinance`
  or of the `SPY` series;
- the future acquisition must **fail closed** if the source is unavailable, the
  schema differs from §6, rate-limited, or the data cannot be frozen
  reproducibly (SHA-pinned manifest);
- any **replacement source** (different vendor/package/object) requires a design
  **amendment** to this memo before acquisition execution — the source may not
  be swapped silently or after seeing data.

## 5. Price-adjustment method

Pre-registered adjustment discipline [I]:

- freeze **raw OHLCV plus adjusted close** (where the source provides it):
  `date`, `open`, `high`, `low`, `close`, `adj_close`, `volume`;
- treat `adj_close` strictly as a **raw source field** at the
  acquisition / join stage — it is captured verbatim, not transformed;
- do **not** compute returns here;
- do **not** compute outcomes here;
- do **not** compute trading signals here.

State [I]:

- a future **instrument-construction** step may use `adj_close` or
  adjusted/total returns **only after** a separate instrument design memo;
- market acquisition itself is **source freezing, not analysis** — it persists
  raw vendor fields under SHA-pinned discipline and nothing derived.

## 6. Exact field set to freeze (LOCKED schema)

The future acquisition must persist **exactly** these columns in
`market_daily_spy.csv` (the frozen market snapshot), no more, no fewer [I]:

| # | column | meaning |
|---|--------|---------|
| 1 | `market_date` | trading-session calendar date (ISO `YYYY-MM-DD`) |
| 2 | `symbol` | instrument symbol (literal `SPY` for v0.1) |
| 3 | `open` | raw session open |
| 4 | `high` | raw session high |
| 5 | `low` | raw session low |
| 6 | `close` | raw session close |
| 7 | `adj_close` | raw vendor adjusted close (verbatim source field) |
| 8 | `volume` | raw session volume |
| 9 | `source_vendor` | vendor identifier (e.g. `yahoo_finance_via_yfinance`) |
| 10 | `source_retrieved_at_utc` | UTC retrieval timestamp of the freeze |
| 11 | `source_timezone` | declared source/exchange timezone |
| 12 | `source_calendar` | declared exchange/calendar interpretation |

State [I] — the frozen snapshot contains:

- **no** return column;
- **no** forward return;
- **no** CAR;
- **no** abnormal return;
- **no** volatility outcome;
- **no** target;
- **no** label;
- **no** signal;
- **no** PnL;
- **no** instrument output;
- **no** post-2022 row.

Any column not in the twelve-row locked schema above triggers a fail-closed in
the §10 conformance gate.

## 7. Trading-calendar source

Pre-registered calendar discipline [I]:

- the **primary calendar** is the trading-date index actually present in the
  frozen `SPY` market snapshot (the `market_date` values the source returns);
- the acquisition **metadata must record** the exchange / calendar
  interpretation, the expected timezone, and the source calendar assumptions
  (`source_calendar`, `source_timezone`);
- if an **external** trading calendar (e.g. an exchange-holiday calendar package)
  is used later, it must be **separately pinned or versioned** in its own
  metadata — not assumed;
- do **not** silently backfill missing market sessions;
- do **not** silently forward-fill non-trading days;
- do **not** infer sessions from the GDELT civil-date calendar alone (GDELT
  emits every civil day; the market series only trading sessions — that
  mismatch is handled at join time per the join memo §4, not by fabricating
  market rows here).

## 8. Domain and 2023+ seal (LOCKED)

- the acquisition domain must cover **only** dates needed up to `2022-12-31`,
  aligned to Input A's `2013-04-01`..`2022-12-31` domain;
- **no 2023+ market data** may be fetched, read, sampled, or stored — the
  2023+ seal in force across the program remains in force here;
- because a future outcome window near the 2022 boundary (e.g. a `t+1:t+5`
  window seeded on late-December-2022 GDELT rows) **may** require post-2022
  prices, those rows must be **marked unavailable** or handled by a **later,
  separately pre-registered rule** — the acquisition must **not** break the
  2023+ seal to satisfy a future outcome window;
- if the future market source returns post-2022 rows, the acquisition must
  **fail closed or truncate before persistence**, and the truncation must be
  **recorded in metadata** (count of rows dropped, max retained `market_date`).
  No 2023+ row may reach disk.

## 9. Future acquisition output artifacts (proposed, NOT created now)

A future, separately authorized acquisition should write **only** these three
artifacts under a fresh timestamped directory [I] (none created by this memo):

- `results/lane2_market_data_acquisition/<timestamp>/market_daily_spy.csv`
- `results/lane2_market_data_acquisition/<timestamp>/market_data_metadata.json`
- `results/lane2_market_data_acquisition/<timestamp>/market_data_summary.md`

State [I]:

- these outputs are **untracked result-output** unless a separate turn
  authorizes tracking them;
- `market_data_metadata.json` must record: **source/vendor**, **symbol**,
  **retrieval method**, **retrieval timestamp (UTC)**, **field set** (the §6
  locked schema), **date domain**, **row count**, the **SHA-256(s)** of the
  frozen CSV (and of the metadata/summary, non-self-referentially), **calendar
  assumptions**, **adjustment method**, and the §11 **boundary declarations**;
- `market_data_summary.md` must be **F1–F6 safe** and must **not** claim any
  market-response result, signal, or outcome — it is a freeze receipt, not
  analysis.

## 10. Future acquisition conformance gate (before any join consumes Input B)

A future acquisition conformance gate must verify [I], failing closed on any
breach:

- **source/vendor** matches §4 (Yahoo Finance via `yfinance`);
- **symbol/instrument** matches §3 (`SPY`);
- **field set** **exactly** matches the §6 locked twelve-column schema (no
  extra, missing, or renamed column);
- **domain** within `2013-04-01`..`2022-12-31`;
- **no 2023+ rows** (max `market_date` ≤ `2022-12-31`);
- **no duplicate** `market_date`;
- dates **sorted ascending**;
- required fields **non-missing where applicable** (OHLC/adj_close/volume on
  trading sessions; missingness explicitly flagged, never imputed);
- **no** return / outcome / target / signal / PnL column;
- **no** instrument-construction column;
- **row count and date bounds recorded** in metadata;
- a **SHA-256 manifest** generated over the frozen artifact(s);
- **source retrieval metadata present** (vendor, method, UTC timestamp);
- **calendar / timezone assumptions present**;
- **boundary declarations** (§11) all true.

## 11. Boundary declarations (future acquisition metadata must declare)

All true at acquisition time [I]:

- `no_market_data_before_authorization`
- `no_2023_plus_access`
- `no_join_execution`
- `no_instrument_construction`
- `no_return_or_outcome_construction`
- `no_target_or_label_construction`
- `no_gdelt_fetch`
- `no_bigquery`
- `no_row_export`
- `no_step2_mutation`
- `source_snapshot_pinned`

## 12. Forbidden actions

Forbidden [I]:

- fetching data in this design turn;
- reading local market files in this design turn;
- choosing fields **after** seeing data;
- changing the source **after** seeing data without a design amendment;
- including 2023+ rows;
- computing returns;
- computing forward returns;
- computing CARs;
- computing abnormal returns;
- computing volatility outcomes;
- computing labels / signals / targets / PnL;
- joining to GDELT features;
- constructing instruments;
- backfilling or forward-filling silently;
- using market data to mutate the 69 GDELT feature columns (the join memo §8
  projection-hash / no-feature-mutation gate enforces the immutable 69-column
  GDELT projection; acquisition must never touch it).

## 13. Risks and ambiguity list

- **Source availability drift** [I]: Yahoo Finance / `yfinance` is an
  unofficial, schema-unstable source; the freeze must fail closed and be
  reproducible (SHA-pinned) — a single frozen snapshot is the durable artifact,
  not live re-fetching.
- **Adjustment ambiguity**: vendor `adj_close` semantics (dividend/split
  treatment) vary; capture verbatim and record the vendor's adjustment basis in
  metadata; do not re-derive adjustment here.
- **Dividend/split handling**: deferred — any total-return reconstruction is an
  instrument-construction decision, not acquisition.
- **Calendar and timezone ambiguity**: NYSE-listed ETF on a U.S. session
  calendar; record `source_timezone` / `source_calendar` explicitly; do not
  assume.
- **Missing market sessions / non-trading days**: never fabricated or
  forward-filled; the GDELT↔market calendar mismatch is resolved at join time
  (join memo §4), not here.
- **2023+ seal pressure near the boundary**: late-2022 outcome windows may
  "want" 2023 prices; the seal still holds — those are marked unavailable and
  governed by a later pre-registered rule.
- **Future outcome-window truncation**: documented as a known limitation; the
  acquisition truncates at `2022-12-31` and records it.
- **Source-vendor reproducibility**: mitigated by SHA-pinned freeze + retrieval
  metadata; the snapshot, not the live source, is canonical once frozen.
- **Accidental outcome construction**: forbidden (§12); the freeze persists raw
  vendor fields only.
- **Accidental join execution**: forbidden; acquisition writes only the three
  §9 artifacts and never reads Input A.
- **Using market data to tune GDELT features**: forbidden; the 69-column GDELT
  projection is immutable (join memo §8).

## 14. Future implementation shape

A future acquisition implementation should [I]:

- be a **separate source / script / test unit** (e.g.
  `src/lane2_market_data_acquisition.py` + `scripts/run_…` + `tests/test_…`),
  distinct from all Step 2 / merge / build code;
- **default to dry-run / manifest-verification only**, performing no network
  fetch unless explicitly enabled;
- require a **dedicated authorization flag** (e.g.
  `MARKET_DATA_ACQUISITION_AUTHORIZED = False`, flipped only inside a
  separately authorized execution wrapper) for any real acquisition;
- write **only** the three §9 acquisition artifacts;
- **fail closed** on schema / source / domain / pin mismatch;
- **never mutate Step 2 outputs**;
- **never run the join**;
- **never construct instruments**.

## 15. Verdict map

- `PASS — MARKET-DATA ACQUISITION DESIGN READY FOR REVIEW`
- `BLOCKED — INPUT B INSTRUMENT UNSPECIFIED`
- `BLOCKED — MARKET SOURCE UNSPECIFIED`
- `BLOCKED — FIELD SET UNSPECIFIED`
- `BLOCKED — ADJUSTMENT METHOD UNSPECIFIED`
- `BLOCKED — CALENDAR SOURCE UNSPECIFIED`
- `BLOCKED — 2023+ SEAL NOT ENFORCED`
- `BLOCKED — FREEZE/PIN DISCIPLINE INCOMPLETE`
- `BLOCKED — MARKET DATA ACCESSED`
- `BLOCKED — JOIN OR INSTRUMENT BOUNDARY CROSSED`

Self-assessment for this draft [I]: instrument locked (`SPY`, §3), source locked
(Yahoo Finance via `yfinance`, §4), field set locked (§6 twelve columns),
adjustment method locked (raw OHLCV + verbatim `adj_close`, §5), calendar source
locked (frozen-snapshot trading index + recorded assumptions, §7), 2023+ seal
enforced (§8), freeze/pin discipline complete (§9–§10 SHA-pinned manifest +
conformance gate), no market data accessed, no join/instrument boundary crossed
→ **`PASS — MARKET-DATA ACQUISITION DESIGN READY FOR REVIEW`** (subject to
independent review).

## 16. Recommendation

`RECOMMENDATION: REVIEW MARKET-DATA ACQUISITION DESIGN MEMO BEFORE ANY MARKET-DATA ACCESS OR FETCH`

— end of market-data acquisition design memo (design-only; non-authorizing) —
