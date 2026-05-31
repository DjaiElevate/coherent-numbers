# Lane 2 GDELT1 — Market-Data Join Design Memo v0.1

Design-only memo. Pre-registers how a future, **separately authorized**
market-data join may consume the canonical Lane 2 GDELT1 Step 2 daily-feature
substrate and align it to a market trading-day index. It does **not** open the
join, does **not** access market data, and does **not** construct an instrument.

Evidence legend: **[O]** observed git/fs · **[A]** artifact-derived (Step 2
output `step2_daily_features.csv` / `step2_metadata.json` / `step2_summary.md`) ·
**[I]** design recommendation.

---

## 1. Purpose and non-authorization

This memo designs the **market-data join** consumption path for the completed
Lane 2 GDELT1 Step 2 daily-feature substrate, and the firewalls that must hold
before any market data is accessed or any join is executed. It performs none of
it.

This turn explicitly does **not**:

- access, fetch, download, sample, or read any market data (prices, returns,
  volumes, volatility, calendars, instrument series, index levels);
- call `yfinance`, BigQuery, GDELT, or any market or data API;
- read any local market-data file;
- execute, implement, or stage any join;
- construct, parameterize, tune, or backtest any instrument;
- create any return, CAR, volatility, target, label, signal, or PnL field;
- export rows, mutate any result-output, edit source / tests / configs /
  representations, write memory, stage, commit, or push.

Distinct phases, **not** to be collapsed, each a separately authorized future
action [I]:

**design (this memo) → market-data acquisition design + authorization →
market-data acquisition / freeze (SHA-pinned snapshot) → join implementation
design → join implementation → join pre-execution conformance gate → join
execution authorization → join execution → (separately) instrument-construction
design → …**

No later phase is authorized, implied, or pre-approved by this memo. In
particular, market-data acquisition, the join run, and instrument construction
are three **independent** gates, each with its own preflight, design memo, and
conformance gate.

## 2. Canonical join inputs

### 2.1 Input A — GDELT Step 2 daily-feature substrate (pinned, present) [O][A]

The single canonical GDELT-side input is the committed Step 2 output at
`HEAD = origin/main = cb1122aa1ab5c040a5b42cb4a69296649fa5fbd5` (ahead/behind
`0 0`):

- directory:
  `results/lane2_gdelt1_step2_daily_features/20260531T020244Z/`
- `step2_daily_features.csv` SHA-256
  `48a64e1cfbcffc4b1e89ef65cb91fa07d928b31a2cb1ffdedcdb2a75cd2aef4d`
  (3563 lines = 1 header + 3562 data rows; 2,924,972 bytes)
- `step2_metadata.json` SHA-256
  `67436f9412eac29e7876bfb661c23040759b6a78b1ed72f7c9da4f41be640b11`
  (133 lines; 5,076 bytes)
- `step2_summary.md` SHA-256
  `80211a0626a4fb466db6ad4c7fe12b1d486e4b1d9d3a54e48a8c4740ad335d53`
  (37 lines; 1,516 bytes)

Substrate shape [A]: **3562 data rows**, one per `civil_date`, domain
`2013-04-01`..`2022-12-31` (3562 unique civil dates, no duplicates), **69
GDELT-only columns**, no market/outcome/return/target/price/ticker/volatility/
instrument/pnl header token. Day-class partition (sums to 3562):
**3557 `raw_t0_present` + 1 `represented_only_documented_exception` (2022-11-10)
+ 4 `known_no_data_gap` (KSG: 2014-01-23 / 2014-01-24 / 2014-01-25 /
2014-03-19)**. The substrate is **10/10 terminal-status** — *not* raw-complete
10/10 — and the join must never describe it as raw-complete 10/10.

The Step 2 output is itself pinned to the merged substrate via
`step2_metadata.json.input_substrate` (`build_manifest_digest`
`4b312183…`, csv `84b6ac9f…`, metadata `31ad8085…`, summary `7677bbaf…`) [A].
The join inherits this provenance chain by reference; it does not re-derive it.

### 2.2 Input B — market-data series (deferred, absent, NOT chosen here) [I]

The market-side input is a **future, separately authorized, SHA-pinned frozen
market-data snapshot**. This memo:

- does **not** select the instrument, vendor, product, or field set;
- does **not** fetch, download, or read it;
- pre-registers only the **discipline** the snapshot must satisfy *before* it can
  be a join input.

Required discipline for Input B before any join consumes it [I]:

- the exact instrument / series, adjustment method, and field set are chosen and
  pre-registered in the **market-data acquisition design memo**, not here;
- the snapshot is frozen under SHA-pinned manifest discipline (mirroring the
  existing pullback / SPY / GLD frozen-artifact convention) **before** use;
- the snapshot domain is **truncated at `2022-12-31`** — 2023+ remains sealed
  (§5);
- the snapshot is read **read-only**, by path + verified SHA-256 / manifest
  digest, and the join fails closed if the pin does not match.

Until that separate authorization, Input B does not exist for this lane and no
market field may be named with a concrete observed value anywhere downstream.

## 3. What the join is allowed to design but not execute

The join's eventual purpose [I] is a **purely structural temporal alignment**:
place the GDELT Step 2 per-civil-date feature rows alongside a market
trading-day index, producing a joined panel keyed by date, so that a *later,
separately authorized* instrument-construction step can attach market outcomes.

In this memo the join may be **designed** to:

- read Input A (GDELT features) and Input B (frozen market snapshot) as
  **read-only**, both pinned by SHA / manifest digest;
- define a **date-keyed temporal alignment** between GDELT `civil_date` and the
  market trading calendar (§4);
- carry the GDELT 69-column schema and the day-class flags
  (`represented_only`, `documented_exception_label`, `is_known_substrate_gap`,
  `terminal_status`, `coverage_quality_flag`) verbatim into the joined panel;
- attach a **minimal, pre-registered, non-derived** market-side field set and a
  `market_trading_day` flag (§6) — with derived market outcomes firewalled to
  the separate instrument step.

The join may **not**, in any turn until the relevant separate authorization:
fetch or read market data; compute any return / CAR / abnormal return /
volatility / target / label / signal / PnL; tune a spike threshold or event
window; select a negative control; consume 2023+; export rows; mutate
result-output; or declare any market finding.

## 4. Temporal alignment rule (pre-registered)

The join is keyed on calendar date with explicit, pre-registered handling of the
GDELT↔market calendar mismatch and of information-timing (leakage) semantics. No
alignment branch may be chosen ad hoc at execution time.

### 4.1 Key and direction [I]

- The join key is the civil date. GDELT emits a feature row for **every** civil
  day in `2013-04-01`..`2022-12-31` (incl. weekends / holidays); the market
  series has rows only on **trading sessions**.
- Pre-registered direction: **left join from the GDELT 3562-row substrate** —
  every GDELT civil_date is retained; the market side contributes where a
  trading session exists. No GDELT row is dropped by the join.
- Each retained row carries a boolean `market_trading_day` flag distinguishing
  civil dates that are / are not market trading sessions.

### 4.2 Non-trading-day handling [I]

- GDELT civil dates that are **not** market trading days are retained with
  `market_trading_day = false` and **null** (not imputed, not back-filled,
  not forward-filled) market-side fields.
- Any mapping of a non-trading GDELT date onto an adjacent session (e.g.
  next-session attribution) is a **downstream instrument-construction decision**,
  not a join responsibility; the join records the raw calendar relationship only.
- The join must **not** silently collapse, drop, or impute non-trading-day rows.

### 4.3 Information-timing / leakage semantics — the no-lookahead invariant anchored on the maximal information-availability date [I]

- GDELT `civil_date` carries **UTC publishing-date** daily-count semantics: the
  content attributed to civil day *d* is only fully observed after day *d*'s
  publishing window closes.
- **Maximal information-availability boundary (locked).** The no-lookahead
  invariant is anchored on each feature row's **maximal information-availability
  date**, *not* on `civil_date = d` alone. For each GDELT feature row with
  `civil_date = d`, the future join must **compute and carry a field** — e.g.
  `gdelt_max_information_date` (equivalently `feature_max_information_date`) —
  equal to the **latest civil date referenced by any GDELT feature in that row**.
- **Default max-info-date = `civil_date + 1 day` (locked).** Because the locked
  Step 2 feature schema includes `rows_from_offset_plus_1` and its derivatives
  (`log1p_rows_from_offset_plus_1`, `share_offset_plus_1`, `neighbor_offset_sum`,
  and `neighbor_offset_share_of_total`), the default max-info-date for the
  canonical 69-column feature row **must be treated as `civil_date + 1 day`**
  unless a future design memo proves a stricter / earlier availability
  convention.
- **No-lookahead invariant (pre-registered).** Any market outcome or market
  measurement window attached later must begin **strictly after** this
  max-info-date / feature-availability boundary (i.e. strictly after
  `gdelt_max_information_date`, not merely strictly after *d*). No market field
  observed on or before that boundary may be aligned as an *outcome* of the
  feature row. The join must **pin and record** both sides' timestamp semantics
  (GDELT publishing-date **and the computed max-info-date** vs market session
  date, including any after-close / next-open convention) in `join_metadata.json`
  so the invariant is mechanically checkable.
- **Conformance coupling.** The future conformance gate must **fail closed** if
  the `gdelt_max_information_date` / `feature_max_information_date` field is
  missing, inconsistent (e.g. earlier than `civil_date + 1 day` without a proven
  convention), or ignored by downstream alignment (§8).
- The join itself computes **no outcome**, so it introduces no lookahead by
  construction; the invariant and the max-info-date field are recorded, not
  consumed, here. The leakage-safe forward-window choice (e.g. a window strictly
  after the max-info-date, such as the `t+1:t+5` CAR candidate) is an
  **instrument-construction decision** and is firewalled (§7).
- **Forward-offset GDELT columns caution.** `rows_from_offset_plus_1` (and its
  derivatives `log1p_rows_from_offset_plus_1`, `share_offset_plus_1`, and any
  neighbor-offset aggregate that includes the `+1` term, i.e. `neighbor_offset_sum`
  and `neighbor_offset_share_of_total`) reference rows whose internal row-date is
  the civil day **after** the publishing day. These remain GDELT-internal
  **predictor** features carried verbatim — **not** market outcomes — but their
  publication-lag / availability implication is exactly what makes the default
  max-info-date `civil_date + 1 day` and therefore **mechanically constrains**
  downstream market-outcome alignment. The join must not treat
  `rows_from_offset_plus_1` as, or convert it into, a market outcome; and the
  instrument step must **inherit** the carried `gdelt_max_information_date` field
  rather than re-derive or guess the timing boundary.

### 4.4 Day-class propagation through the join [I]

- The `2022-11-10` documented-exception row (`represented_only = true`,
  `terminal_status = represented_only_documented_exception`, label
  `UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY`,
  `total_row_count = 1267`, `rows_from_offset_0 = 0`) **propagates verbatim**
  through the join: its label and flags carry into the joined panel, it is never
  reclassified as raw-processed / recovered / a KSG no-data gap / ordinary
  completion, and the join fails closed if the label is absent or altered.
- The four KSG dates (`2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`,
  `terminal_status = known_no_data_gap`, empty documented-exception label)
  remain a **distinct class** from the documented exception and are never
  reclassified or merged with it.
- The join performs **no imputation** for any day class; it propagates Step 2's
  existing flags rather than recomputing coverage or status.

## 5. Market-data firewall and 2023+ seal

- This memo and every turn until a **separate explicit market-data
  authorization** access **no** market data. The Step 2 substrate is GDELT
  daily-count-only and contains no market data; the join introduces market data
  only at a future, separately authorized acquisition gate.
- The **2023+ seal remains in force**. Input B must be truncated at
  `2022-12-31`; the joined domain is `2013-04-01`..`2022-12-31` (3562 civil
  days). No 2023+ observation, outcome, level, or count may be accessed,
  sampled, referenced for a design choice, or consumed. Any future use of 2023+
  is a separate, explicitly justified seal-consumption decision and is **not**
  authorized, implied, or pre-approved here.
- Market-data acquisition is a distinct gate from the join run: freezing /
  pinning the snapshot does **not** authorize executing the join, and executing
  the join does **not** authorize constructing an instrument.

## 6. Proposed joined-output artifact set and schema

A future, separately authorized join implementation should produce
**read-derived, offline** artifacts [I] under a fresh
`results/lane2_gdelt1_join_*/<UTC-ts>Z/` directory (untracked result-output,
mirroring the chunk / merge / Step 2 convention):

| # | artifact | role |
|---|----------|------|
| 1 | `join_panel.csv` | per-civil-date joined rows: the GDELT 69-column Step 2 schema verbatim, plus `market_trading_day`, plus a **pre-registered minimal raw market-side field set (deferred to the acquisition design memo)**, plus day-class passthrough |
| 2 | `join_metadata.json` | provenance: Input A path + SHA-256s (the three Step 2 identities of §2.1) and inherited `build_manifest_digest`; Input B frozen-snapshot path + manifest SHA; temporal-alignment + timestamp-semantics pins (§4); documented-exception block (inherited); per-day-class counts reconciling to 3562; boundary declarations; join implementation version |
| 3 | `join_summary.md` | positive-status summary: substrate = 10/10 terminal-status (not raw-complete 10/10); day-class table; documented-exception note; explicit "no derived market outcome / no instrument / 2023+ sealed" boundary statement |

Schema rules for `join_panel.csv` [I]:

- the 69 GDELT columns are carried **verbatim** (same names, same values);
  Step 2 features are not recomputed by the join;
- `civil_date` remains the 3562-row, no-duplicate key over
  `2013-04-01`..`2022-12-31`;
- the market-side carry is a **minimal, pre-registered, non-derived** field set
  (raw session date / raw price/calendar fields only) — the **exact** field list
  is deferred to the market-data acquisition design memo and is **not** fixed
  here;
- **raw market field clarification.** Any raw market fields carried by the join,
  if any, are **calendar-aligned market records only**. They are **not**
  outcomes, targets, trading signals, instruments, CARs, abnormal returns,
  volatility outcomes, PnL, or model labels; outcome construction remains a
  separate instrument-construction phase (§7). Any future raw market fields must
  be **namespaced** (e.g. a `mkt_` / `market_` prefix), **pinned** to the frozen
  Input-B snapshot, and **documented as read-only source fields**. Derived
  outcome columns remain **forbidden** in the join unless separately
  pre-registered in a later phase;
- **no** column may be a return / CAR / abnormal return / volatility / target /
  label / signal / PnL — those are firewalled to instrument construction (§7);
- `market_trading_day` and the day-class passthrough columns
  (`represented_only`, `documented_exception_label`, `is_known_substrate_gap`,
  `terminal_status`, `coverage_quality_flag`) are present and unmodified.

Each artifact is checksummed; `join_metadata.json` must reference both input
pins so the joined output is reproducibly bound to the exact Step 2 substrate
and the exact frozen market snapshot.

## 7. Instrument-construction firewall

No instrument is constructed, parameterized, tuned, evaluated, or backtested by
this memo, by the acquisition step, or by the join step. The join produces a
**structurally aligned panel only**. Specifically firewalled to a later,
separately authorized instrument-construction phase [I]:

- any return, cumulative abnormal return (CAR), abnormal-return baseline
  (market-model vs simple-mean), realized-volatility response, or target
  variable;
- the primary response window (e.g. the `t+1:t+5` CAR candidate named in the
  readiness memo) and any same-day / 1-day / 20-day alternative;
- attention-spike threshold tuning, event clustering / separation rules,
  event-window overlap handling, and non-trading-day **event** attribution;
- state-axis definition (and the Atlas C1 construction-coupling burden);
- negative-control / shuffled-state / random-feature selection;
- any signal, allocation, or PnL logic, and any market finding or claim.

Naming these abstractly here does **not** select or pre-register any of them; it
fixes the boundary the join must not cross.

## 8. Pre-execution conformance gate (before any join execution)

A future join pre-execution conformance gate must verify [I], failing closed on
any breach:

- **input-A pinning**: `step2_daily_features.csv` / `step2_metadata.json` /
  `step2_summary.md` SHA-256s match the canonical §2.1 values; inherited
  `build_manifest_digest` matches;
- **input-B pinning**: the frozen market snapshot matches its pre-registered
  manifest SHA; domain truncated at `2022-12-31`;
- **row domain**: 3562 GDELT civil days, `2013-04-01`..`2022-12-31`, no
  duplicates; left-join retains all 3562 GDELT rows;
- **temporal-alignment conformance**: the join key, direction, non-trading-day
  handling, and timestamp semantics match §4 exactly; no ad-hoc branch;
- **max-info-date conformance**: a `gdelt_max_information_date` /
  `feature_max_information_date` field is present, equals the latest civil date
  referenced by the row (default `civil_date + 1 day` for the canonical
  69-column schema, absent a proven stricter convention), and is carried into
  `join_metadata.json`; **fail closed** if the field is missing, inconsistent,
  or ignored by downstream alignment (§4.3);
- **day-class propagation**: the documented-exception label + §2.1 provenance
  carry into the joined panel; `2022-11-10` flagged represented-only and not
  imputed; the four KSG dates remain a distinct, unreclassified class;
- **day-class reconciliation**: per-class counts sum to 3562
  (3557 + 1 + 4);
- **no-imputation audit**: non-trading-day and any-missing market fields are
  null, never back/forward-filled;
- **no-derived-outcome audit**: the joined panel contains **no** return / CAR /
  volatility / target / label / signal / PnL column (header-token scan, mirroring
  the Step 2 GDELT-only token audit);
- **projection-hash / no-feature-mutation**: the joined artifact must carry the
  69 GDELT feature columns **unchanged and in the same canonical order**. The
  gate must **project** `join_panel.csv` back to exactly those 69 GDELT feature
  columns, in canonical order, and verify the projection is **byte-identical /
  SHA-identical** to the pinned `step2_daily_features.csv` (SHA-256 `48a64e1c…`,
  §2.1). Where exact byte identity is obstructed by CSV formatting, a
  **deterministic canonical serialization** must be applied before hashing. Any
  mutation, reordering, dropping, rounding, type conversion, or value change in
  the 69 GDELT feature columns **fails closed**. Market columns must live **only
  outside** that immutable 69-column projection;
- **2023+ seal audit**: no row, field, or reference beyond `2022-12-31`;
- **no raw-complete-10/10 claim** anywhere in join prose / metadata;
- **F1–F6 forbidden-claim audit** (canonical mapping from
  `representations/lane2_gdelt1/chunk_2022_documented_exception_20221110/representation.json`):
  no affirmative forbidden claim in the join summary / metadata prose;
- **firewall declarations** all true: `no_market_outcome`, `no_instrument`,
  `no_gdelt_fetch`, `no_bigquery`, `no_row_export`,
  `no_known_substrate_gaps_amendment`, `no_2023_plus_access`,
  `no_step2_substrate_mutation`.

## 9. Risks and ambiguity list

- **Market-side field set is unspecified** [I]: deliberately deferred to the
  market-data acquisition design memo; this memo fixes the join discipline and
  firewalls, not the chosen instrument or fields. Not a blocker for designing
  the join.
- **Calendar mismatch**: GDELT emits every civil day; the market series only
  trading days. The pre-registered left-join + `market_trading_day` flag + null
  (no-impute) rule (§4) is the mitigation; any session-attribution mapping is
  explicitly an instrument-step decision, not a join decision.
- **Timestamp / leakage semantics**: the highest-care item. The join computes no
  outcome and therefore introduces no look-ahead, but must **record** both
  sides' timestamp semantics so the later instrument step cannot leak; failing
  to pin these semantics is the principal latent risk.
- **Day-class carry**: the documented-exception row and the four KSG dates must
  survive the join as distinct, labeled classes; a left join that drops or
  reclassifies them would be a firewall breach.
- **Uncommitted vs committed inputs**: Input A is committed and SHA-pinned
  (durable); Input B will be uncommitted frozen result-output at acquisition
  time and must be pinned by manifest SHA before the join consumes it.
- **Market-data boundary** is the top firewall: market acquisition, the join
  run, and instrument construction are three separate gates, none folded into
  another.

No design point is impossible or materially ambiguous to the degree that blocks
*designing* the join; the open items are downstream pre-registration decisions
(chiefly the Input B instrument / field selection), not missing inputs.

## 10. Recommendation and next frontier

**`RECOMMENDATION: REVIEW MARKET-DATA JOIN DESIGN MEMO BEFORE ANY MARKET-DATA ACCESS OR JOIN IMPLEMENTATION`**

**`MARKET-DATA ACQUISITION DESIGN + AUTHORIZATION REQUIRED NEXT`**

Justification [I]: the GDELT Step 2 substrate is complete, conformant, committed,
and fully provenanced (incl. the documented-exception §2.1/§4.4 metadata and the
represented-only `2022-11-10` row), so the **structural** join is well-defined at
the design level. The binding unknown is **Input B** — which market series /
product / field set supports a reproducible, freezable, 2023+-sealed daily series
over `2013-04-01`..`2022-12-31`. The next prompt should therefore be a
**separately authorized market-data acquisition design memo** that pre-registers
the instrument, adjustment method, field set, calendar source, and SHA-pinned
freeze discipline — **before** any market data is fetched, **before** any join is
implemented or executed, and long **before** any instrument construction.

**The next substantive gate is the market-data acquisition design / authorization
memo — not market-data access, and not join execution**, both of which remain
unauthorized until their own separate, explicitly authorized gates.

This memo opens nothing: no market data is accessed, no join is executed, no
instrument is constructed, the 2023+ seal holds, and the substrate remains 10/10
terminal-status (9 raw-complete + 1 labeled-complete documented-exception), not
raw-complete 10/10.

— end of market-data join design memo (design-only; non-authorizing) —
