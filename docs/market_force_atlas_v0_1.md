# Market Force Atlas v0.1 — DRAFT (memo-before-test)

**Status: DRAFT FOR OWNER REVIEW. Not committed. Not a test plan for immediate execution.**
**Class: exploratory-design (atlas). Writing/revising cards consumes no trials.**
**Repo: /Users/jay/Documents/GitHub/coherent-numbers**
**Drafted: 2026-06-12 · Revised: 2026-06-13 (bounded revision pass)**
**Value-safety: no raw data, no row-level values, no prices/returns/sentiment/macro values, no sealed-period (≥ 2023-01-01) values inspected. Headers + first/last date metadata + SHA-256 only. GDELT zip cache audited by filename only (no zip opened/unzipped/read).**

---

## 1. Purpose and non-goals

**Purpose (explanatory).** The Market Force Atlas maps the *forces* that may shape SPY price paths and, for each, defines **in advance** how it could be measured later: its proxy, dataset, canonical outcome, null hypothesis, confounds, and the boring baseline it must beat. It is a map of the forest, not a hunt for an edge.

**This artifact is explanatory, not an edge system.** It is not a trading system, not a prediction-for-profit project, and not a parameter search. Nothing in it authorizes a test.

**A null result is valid.** A force that turns out to add nothing beyond its cluster's boring baseline is a *finding*, recorded as such, not a failure to be optimized around. The Cusp Geometry Lane v0.3 null (§2) is the template: tested honestly, did not survive, closed.

**A force may be another force wearing a mask.** Many named "forces" are the same underlying axis seen from a different angle (trend / momentum / mean-reversion are one autocorrelation axis; zigzag / path-length / range are facets of volatility). The atlas forces every card to declare its cluster and to eventually beat that cluster's canonical representative before it may claim distinctness.

**No force is tested until it is fully specified.** A force may not be promoted to a tested lane until its **proxy, dataset, canonical outcome, null, confounds, and cluster baseline** are all defined ahead of time, in a frozen design memo.

**Cards are free; promoted lanes are rationed.** Writing or revising a card costs nothing. Testing a force consumes governance attention and a shared sealed-alpha budget, so promotions are limited (§3).

**Non-goals.**
- Not an edge-finding or alpha-generation program.
- Not a directional or magnitude prediction-for-profit system.
- Not a parameter / window / threshold search.
- Not a re-opening of any closed lane (see §2).
- Not a sibling project that can collide with existing lanes — **the atlas is the program's master index** over forces, sitting above lanes, not beside them.

---

## 2. Relationship to prior lanes

The atlas is the **master index**; existing lanes are its already-spent or reserved entries. It does not duplicate, fork, or compete with them.

| Prior work | Repo trace (filename/header only) | Atlas consequence |
| --- | --- | --- |
| **Cusp Geometry Lane v0.3** | `docs/cusp_geometry_lane_design_memo_v0_3.md`; `docs/cusp_geometry_lane_v0_3_sandbox_gate_report.md`; freeze `4536be27f6955be72bdb7abad4b4cb38ac1278ad`; closure `ac098b660cabdc04aafff54aec7356ab55b143f4` | **Curvature CLOSED** — exploratory null; pooled incremental R² `-0.0256`, `0/10` folds; `F2_kappa_mean` not separable from B6 / zigzag for SPY 2005–2022. **Do not reopen.** No alternate windows, thresholds, mirrored features, or sealed test. |
| **Lane 2 TTG → SPY directional v1.1** | `docs/lane2_ttg_spy_prereg_v1.1.md`; `docs/lane2_ttg_spy_v1_results_v0.1.md` | **News direction CLOSED** — weak/null (AUC≈0.5266, p≈0.166, `statistical_confirmed=False`). Treat as closed unless owner provides new scope. |
| **TTG magnitude-pressure arc** | `docs/lane2_ttg_magnitude_pressure_weekly_spend_decision_v0.1.md` and siblings | No-spend terminal across daily/weekly/monthly horizons on the achievable seal. Informs **News magnitude** card (OPEN but governed by MDE realism). |
| **GDELT attention / volume work** | `docs/lane2_attention_spike_*`; `results/lane2_gdelt1_full_daily_count_build/...`; `docs/lane2_divergence_record_4f31bcb_6a75ec7.md` | **GDELT raw-count/coverage proxy → `CLOSED`** (Q8): exploratory null, drift-confounded — raw Spearman ≈ −0.15 to −0.18, dissolved under drift control (owner-confirmed; divergence record cited). Read-only prior art / drift-confounded artifact only; **not** a promotable representative. Coverage-normalized/drift-controlled attention remains the cluster representative. |
| **Calendar studies (Harmonic Calendar)** | `docs/harmonic_calendar_*` (SPY MVT null, GLD null) | Prior-art for **Calendar** group; both cells closed null. |
| **Pullback program** | `docs/pullback_population_freeze_manifest_v0.1.md`; `data/raw/pullback_*` | Prior-art for path-geometry / event-date forces; frozen 2005–2022 trade substrate. |
| **Human Field Base-12 Pullback Atlas v0.1** | `docs/human_field_base12_pullback_atlas_*` | Prior exploratory atlas, closed (resolution-limit). Precedent for atlas-class artifacts; not a force to re-run. |
| **Live dispersion lane** | **No doc found by filename in `docs/`.** Owner-confirmed; design memo not yet committed (pending §6a.6/§7 whitelist fix). | **Cross-asset dispersion**, **Correlation regime**, and **Fundamental dispersion** are **RESERVED** to it. Provisional written grounding in **§3.1**; superseded by the real dispersion memo when committed. See §11 Q1. |
| **Microscope instrument program charter** | `docs/microscope_instrument_program_charter_v0.1.md` | Program-level governance precedent; atlas governance (§3) is designed to nest under it, not collide. |

---

## 3. Atlas governance

**The atlas is exploratory-design class.** Writing or revising force cards **consumes no trials** and touches no data.

**Testing a force consumes governance attention** and requires **promotion to a lane**. A force moves from card → lane **only through a frozen design memo**.

**The frozen design memo must follow the Cusp-lane pattern:**
- statistic / proxy,
- target / canonical outcome,
- baselines,
- the cluster's canonical representative (the boring baseline it must beat),
- sandbox gate (in-window only, pre-registered PASS/FAIL),
- sealed rule (no sealed contact before a sandbox PASS + explicit owner authorization),
- multiple-testing ledger entry.

**Promotions are rationed.** Frozen draft governance literals for v0.1:
```
MAX_ACTIVE_ATLAS_LANES        = 1
ATLAS_FAMILY_ALPHA            = 0.05
MAX_SEALED_ATTEMPTS_ATLAS_V0X = 5
PER_ATTEMPT_ALPHA             = 0.01   # unless amended on the record
```

**Rationale.**
- The program currently operates best with **one** active promoted atlas lane at a time.
- Parallel promoted lanes increase audit complexity and family-level forking-path risk.
- The atlas family receives **one shared sealed-test budget**, not a fresh 0.05 per lane.
- If the owner later wants more active lanes or more sealed attempts, that requires a **formal amendment on the record before further data contact** — the `unless amended on the record` clause on `PER_ATTEMPT_ALPHA` is the only sanctioned path to change these literals.

**The four governing facts of this regime:**
- **Cards are free.** Writing or revising a card costs nothing and touches no data.
- **Lanes are rationed.** `MAX_ACTIVE_ATLAS_LANES = 1`; promotion is the scarce act.
- **Sealed alpha is shared across the atlas family.** `ATLAS_FAMILY_ALPHA = 0.05` is one budget for the whole family; `MAX_SEALED_ATTEMPTS_ATLAS_V0X = 5` attempts at `PER_ATTEMPT_ALPHA = 0.01` each.
- **No future lane gets a fresh sealed-alpha budget just because it is individually clean.** Cleanliness earns a lane the right to *spend* from the shared budget, not a new budget of its own.

**Shared alpha.** Every promoted lane joins **one atlas-level trial ledger**. Sealed-test alpha is **shared across the whole atlas family and never reset per lane**. Each promotion spends from the same budget; a lane cannot buy itself a fresh α by being renamed, re-scoped, or by being individually clean.

**Alpha debit mechanism (Q3).**
- **Prior closed lanes do not retroactively debit `ATLAS_FAMILY_ALPHA`** — including **Cusp Geometry Lane v0.3** and **Lane 2 news-direction** — because they **predate the Market Force Atlas** and were governed under their own preregistrations.
- From the moment **Market Force Atlas v0.1 is committed**, **every promoted atlas lane joins the atlas-level trial ledger**.
- A **sealed attempt debits the atlas family budget only at the moment of sealed-data contact.**
- **Sandbox-gate failures debit nothing** — sealed data remains unopened.
- Each sealed attempt under Atlas v0.x **debits `PER_ATTEMPT_ALPHA = 0.01`** from the family cap of **`ATLAS_FAMILY_ALPHA = 0.05`**, **unless amended on the record before further data contact.**
- **Every debit must be logged** with:
  - date,
  - lane name,
  - frozen design memo SHA / commit,
  - sealed boundary,
  - alpha debited,
  - result,
  - whether the sealed attempt count remains within `MAX_SEALED_ATTEMPTS_ATLAS_V0X = 5`.
- **No promoted atlas lane receives a fresh independent sealed alpha budget.**

This preserves the Cusp-lane logic: **sandbox failure closes a lane without spending the seal; sealed contact is the moment the family budget is actually consumed.**

**Sealed discipline.**
- No lane may open sealed data (≥ `2023-01-01`) without **explicit owner authorization after a sandbox PASS**.
- A **sandbox FAIL closes the promoted lane as exploratory null** unless a **new version is explicitly designed and logged before any further data contact**.

**Card status values.** Every card carries exactly one of these four primary statuses:
- `OPEN` — available and not closed/reserved (fully specifiable; eligible for promotion).
- `STUB` — concept exists but the required data is not currently available or not usable; cannot be fully specified yet.
- `RESERVED` — owned by another live lane; do not promote here until that lane resolves.
- `CLOSED` — a prior lane closed it, or the force cannot be reopened under current protocol; do not reopen.

`PARTIAL` is an **optional availability label** (not a fifth status) for forces with partial data — the card must still carry one of the four primary statuses (typically `OPEN`) and **state exactly what is partial** (e.g. "OHLC available 2013–2022 only").

**Pre-set statuses (owner-fixed for v0.1):**
- **Curvature → `CLOSED`** — Cusp Geometry Lane v0.3; not separable from zigzag/B6 for SPY 2005–2022; do not reopen.
- **News direction → `CLOSED`** — prior Lane 2 v1.1 null; not open unless owner provides new scope.
- **GDELT raw-count/coverage proxy → `CLOSED`** — prior exploratory null / drift-confounded (raw Spearman ≈ −0.15 to −0.18, dissolved under drift control; `docs/lane2_divergence_record_4f31bcb_6a75ec7.md`). Raw count is **not a promotable canonical representative**; it may appear only as read-only prior art or as an explicitly drift-confounded artifact.
- **News magnitude → `OPEN`** — intensity/valence → next-session absolute move or volatility; untested here; requires its own locked design if promoted.
- **Cross-asset dispersion → `RESERVED`** — belongs to the live dispersion lane until it resolves.
- **Correlation regime → `RESERVED`** — belongs to the live dispersion lane until it resolves.
- **Fundamental dispersion → `RESERVED`** — belongs to the live dispersion lane until it resolves.

### 3.1 Reservation grounding — live dispersion lane

The previous draft marked these forces RESERVED, but **no committed dispersion/correlation design memo was found in `docs/` by filename**. This subsection supplies the written grounding for that status:

- The owner **confirms a live dispersion lane exists outside the committed docs.**
- Its design memo **has not yet been committed** because it is still pending a **load-bearing fix involving the §6a.6/§7 whitelist inconsistency**.
- Until that lane resolves or is formally abandoned, the atlas marks these forces **RESERVED**:
  - **cross-asset dispersion**,
  - **correlation regime**,
  - **fundamental dispersion**.
- The atlas **may index** these forces but **may not explore, test, promote, or redefine** them.
- This reservation is **provisional written grounding** and **should be superseded by the real dispersion memo when committed**.
- The in-memo reservation stub grounds the RESERVED status *for now*, but it **does not retire the separate debt** to fix and commit the live dispersion memo.
- The pending dispersion memo fix **remains its own future single-purpose task** — specifically the **§6a.6/§7 whitelist inconsistency** — and is not discharged by this stub.

---

## 4. Cluster system

A force is **not distinct merely because it has a new name.** To count as its own force it must eventually **beat its cluster's boring canonical representative**.

| Cluster | Canonical representative | Members |
| --- | --- | --- |
| **VOLATILITY** | trailing realized volatility | volatility, zigzag, range expansion, compression, shock/jump, path length, volatility-of-volatility, drawdown, recovery (curvature/cusp belong here but are **CLOSED**) |
| **AUTOCORRELATION** | lag-k autocorrelation / simple continuation–reversal statistic | trend, momentum, mean reversion — **one axis, different signs/horizons**, not three forces |
| **NEWS/ATTENTION** | **coverage-normalized / drift-controlled** news or attention count (**not** raw count) | attention, narratives, news velocity, news decay, sentiment disagreement, news magnitude (news direction CLOSED) |
| **MACRO WEATHER** | simple macro variable or event flag | all Group 3 macro forces |
| **LIQUIDITY** | volume or spread proxy | all Group 5 structure forces |
| **CALENDAR** | simple calendar dummy | all Group 8 calendar forces |
| **DATA CONSTRUCTION** | source / adjustment-policy check | all Group 9 forces |

**Distinctness rule (general).** A card may claim distinctness from its cluster only by **incrementally beating the cluster's canonical representative** on a canonical outcome, out-of-fold, under the same sandbox gate that closed Curvature. Curvature is the worked example of failing this rule (absorbed by B6).

**DERIVED (composite) forces.** A force built from other forces is marked `DERIVED` and **cannot be promoted before its components are defined** (each component must itself be a defined FULL card or canonical representative). Worked examples:
- **Euphoria** = low volatility + strong trend + positive sentiment
- **Panic** = high volatility + downside shock + volume/stress
- **Uncertainty** = volatility + disagreement/news dispersion
- **Exhaustion** = extended trend + high activity + weakening continuation

### 4.1 Per-cluster rules

Every FULL card **must** declare its **cluster**, its **canonical representative**, and its **distinctness rule** (the explicit thing it must beat). The clusters below fix those representatives.

**VOLATILITY cluster.**
- Canonical representative: **trailing realized volatility**.
- Members include volatility, zigzag, range expansion, compression, shock/jump, path length, volatility-of-volatility (drawdown and recovery also sit here; curvature/cusp belong here but are **CLOSED**).
- Any member must **beat trailing realized volatility** (or the relevant canonical representative — e.g. roughness forces must additionally beat **zigzag/B6**, which already beat curvature) to count as distinct.

**AUTOCORRELATION cluster.**
- Canonical representative: **simple lag-k autocorrelation / return continuation–reversal statistic**.
- Trend, momentum, and mean reversion are **one axis with different signs/horizons, not three unrelated forces**. A member claiming separateness must beat the single representative *and* show it is not that same axis at another horizon.

**NEWS/ATTENTION cluster (amended rule).**
- Canonical representative: **coverage-normalized / drift-controlled news or attention count — not raw count.**
- **Rationale:** program prior art (the GDELT volume/coverage exploratory null, drift-confounded — see §6/§7 prior-art) showed **raw counts carried a collection-drift artifact that dissolved under drift control**. Therefore **raw news count is the known artifact, not the boring representative.**
- **The GDELT raw-count/coverage proxy is `CLOSED`** (Q8): an official closed record on the strength of that exploratory null. **Raw count is not a promotable canonical representative** — it may appear only as **read-only prior art or as an explicitly drift-confounded artifact**, never as the thing a new card beats.
- **Every card in the NEWS/ATTENTION cluster must list `collection drift` as a standing confound.**
- The **coverage-normalized / drift-controlled** count remains the canonical representative for this cluster.
- **News direction remains `CLOSED`** under prior Lane 2 v1.1.
- **News magnitude / intensity remains `OPEN` but unpromoted** and requires its own locked design if ever promoted.

**CALENDAR cluster.**
- Canonical representative: **simple calendar dummy**.
- Prior calendar nulls must be listed where found (Harmonic Calendar: SPY MVT null, GLD null — see Group 8 / prior-art).

**DATA CONSTRUCTION cluster.**
- Canonical representative: **source / adjustment / calendar policy check**.
- **"Group 9 protects us from studying the map instead of the forest."** These checks must be considered *before* any behavioral interpretation (hygiene rule §8.6).

---

## 5. Canonical outcomes

To prevent test-multiplication by outcome-shopping, the atlas fixes a small canonical outcome family.

**Canonical outcomes:**
1. **forward realized volatility** — magnitude outcome.
2. **forward max drawdown** — tail / risk-path outcome.
3. **regime indicator** — structure / change-state outcome.

**Derived outcomes** (may be *described*, may **not** be used to casually multiply tests): future zigzag, future range, future path length, shock count, reversal count, recovery time, compression time.

A future lane that wants a derived outcome as its **primary** must justify, in its frozen memo, why it is **not just another mask** of the canonical outcome family (e.g., why "future zigzag" is not forward realized volatility relabeled).

---

## 6. Dataset inventory summary

Inventory is **metadata-only**: path, SHA-256, header/columns, first/last date. **No prices, returns, sentiment, macro, or value cells were read.** For files spanning ≥ 2023-01-01, only the first/last *date* cells were read (allowed metadata); their values were not inspected. **No decision to use any dataset is made here.**

### 6.1 Price-only data

| Path | SHA-256 | Columns | First | Last | Sealed dates? | Class |
| --- | --- | --- | --- | --- | --- | --- |
| `data/raw/spy_yahoo_v8_19930129_20241231_e8fc0357…aaaa56.csv` | `e8fc0357410ce499da8f67e09b4c9908232e18a55445f38969e77fa712aaaa56` | `date, adj_close` | 1993-01-29 | 2024-12-31 | **YES (→2024)** | **MIXED** |
| `data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv` | `5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901` | `date, adj_close` | 2005-01-03 | 2022-12-30 | No | **sandbox-only** |
| `data/raw/market/spy_yahoo_adjclose_20130402_20221230_snapshot_20260606.csv` | `2842647c318c95bd02bc888ee70361d8242ddf8223281e49a8231ea3d91aa055` | `Date, Open, High, Low, Close, Adj Close, Volume` | 2013-04-02 | 2022-12-30 | No | **sandbox-only** |

### 6.2 Volume / liquidity data

| Path | SHA-256 | Columns | First | Last | Sealed? | Class |
| --- | --- | --- | --- | --- | --- | --- |
| `data/raw/market/spy_yahoo_adjclose_20130402_20221230_snapshot_20260606.csv` | (as above `2842647c…`) | OHLCV (incl. `Volume`) | 2013-04-02 | 2022-12-30 | No | sandbox-only |
| `results/lane2_market_data_acquisition/20260531T224518Z/market_daily_spy.csv` | `8a87fc0536b24d013272f1ae841d9d8881fe203e16bf84a96b2ae6ce2f6cd5a1` | `market_date, symbol, open, high, low, close, adj_close, volume, source_vendor, source_retrieved_at_utc, source_timezone, source_calendar` | 2013-04-01 | 2022-12-30 | No | sandbox-only (Lane 2 provenance-stamped) |

### 6.3 Market psychology / sentiment data

No dedicated sentiment dataset. Closest proxy is **GDELT `avgtone`** in the TTG event archives (§6.4) and the daily count/feature builds — these are news-derived, not market-sentiment indices. **No VIX / put-call / survey sentiment present.**

### 6.4 News / event data

| Path | SHA-256 | Columns (count) | First | Last | Sealed? | Class |
| --- | --- | --- | --- | --- | --- | --- |
| `results/lane2_gdelt1_full_daily_count_build/merged_20260529T175416Z/build_daily_counts.csv` | `84b6ac9f47888fea4bd5c9d448058db0e5c568e3aa194a0fc7d4d5c95704045e` | 16 cols (`civil_date, total_row_count, rows_from_offset_*, coverage_*, …`) | 2013-04-01 | 2022-12-31 | No | sandbox-only |
| `results/lane2_gdelt1_step2_daily_features/20260531T020244Z/step2_daily_features.csv` | `48a64e1cfbcffc4b1e89ef65cb91fa07d928b31a2cb1ffdedcdb2a75cd2aef4d` | 69 cols (`civil_date, …, log1p_*`) | 2013-04-01 | 2022-12-31 | No | sandbox-only (GDELT-only, no market cols) |
| `results/lane2_ttg_gdelt1_bounded_real_slice/20260604T210758Z/ttg_approved_fields_archive.csv` | `c077edc6d4e0214797d001fdd8b1601a791868bf05fe84732dbd48cdfc716238` | `sqldate, quadclass, goldsteinscale, avgtone, nummentions` | 2013-04-02 | 2013-04-29 | No | sandbox-only (April-2013 bounded slice) |
| `results/lane2_type_tone_goldstein_full_window_real_archive_build/ttg_approved_fields_archive.csv` | `06dcbc2530deb9fb25dc87b651f3012fe7de21474235c0f85c7ddd53b604383b` | `sqldate, quadclass, goldsteinscale, avgtone, nummentions` | 2013-04-02 | 2022-12-30 | No | sandbox-only (event-level; ~5.06e8 rows — very large) |
| `data/raw/lane2_ttg_gdelt1_event_zip_cache/` | (3557 daily `YYYYMMDD.export.CSV.zip` files; not hashed individually) | raw GDELT 1.0 event export | **2013-04-01** | **2022-12-31** | **No (filename audit)** | sandbox-only by filename. **Filename-only audit (2026-06-13): 3557 zip files, all match `YYYYMMDD.export.CSV.zip` (0 non-parseable); earliest encoded date 2013-04-01, latest 2022-12-31; 0 filenames on/after 2023-01-01.** No zip opened, unzipped, or read — date bound from filenames only. Raw vendor cache; in-window by filename. |

### 6.5 Macro data
**None present** in repo inventory. All Group 3 forces are `STUB` pending external, **point-in-time (vintage-safe)** sourcing.

### 6.6 Company / fundamental data
**None present.** All Group 4 forces are `STUB`; vintage flag required when sourced.

### 6.7 Market-structure / options data
**None present** (no options, order-book, dealer-positioning, or short-interest data). All Group 5 forces are `STUB`.

### 6.8 Cross-asset data

| Path | SHA-256 | Columns | First | Last | Sealed? | Class |
| --- | --- | --- | --- | --- | --- | --- |
| `data/raw/gld_yahoo_v8_20041118_20241231_368fe450…1fd1b2c.csv` | `368fe45094eafa277c81accd2c71b2b593ddcf917c29c7b269de088a31fd1b2c` | `date, adj_close` | 2004-11-18 | 2024-12-31 | **YES (→2024)** | **MIXED** (gold) |
| `data/raw/pullback_phase3b_{eem,efa,gld,tlt}_trades_2005_2022.csv` | eem `56cf8e5f…`, efa `275af7e0…`, gld `0de7bf6d…`, tlt `037ea417…` | trade-list (`entry_date,…,r_multiple`) | 2005-02 | 2022-12 | No | sandbox-only **(derived strategy trades, not price series)** |

No bond-yield, VIX, dollar, oil, credit, global-equity, or crypto price series present. Those cross-asset cards are `STUB`.

### 6.9 Calendar / event-date data
**No dedicated calendar dataset.** Calendar forces (Group 8) are derivable from the **date index of any inventoried price file** (no market values needed), so they are full-card-eligible on the in-window SPY index.

### 6.10 Data-construction / metadata

| Path | SHA-256 | Note |
| --- | --- | --- |
| `results/lane2_market_data_acquisition/.../market_daily_spy.csv` | `8a87fc05…` | carries `source_vendor, source_retrieved_at_utc, source_timezone, source_calendar` — adjustment/provenance fields |
| `results/.../ttg_archive_provenance_manifest.json` (multiple) | not hashed here | provenance manifests for TTG archives |
| `data/raw/market/spy_yahoo_adjclose_20130402_20221230_snapshot_20260606.csv` | `2842647c…` | **carries both `Close` and `Adj Close`** — the adjustment-policy fork is live here |
| filename-embedded SHA convention | — | source files name-stamp their content hash (e.g. `…_e8fc0357….csv`) — a data-construction hygiene control already in use |

**Inventory-level hygiene notes.**
- The two `…_20241231_…` files (`spy_yahoo_v8`, `gld_yahoo_v8`) **span sealed dates (2023–2024)**; only first/last date metadata was read. Any in-window use must truncate before 2023 exactly as the cusp sandbox derivation did.
- `results/lane2_join/gdelt_spy_nextday.csv` (`e9e76ea3ca19f1bbbcaa39ea223fe3c877757b30139530c959edebeea228f32a`, 72 cols, 2013-04-01→2022-12-31) and `results/lane2_next_session_return/20260531T225725Z/next_session_return.csv` (`b2773b3f627f28cd9b3eefa0ad8cd7b6b3ac7962425e6319686111560baed566`, 2013-04-01→2022-12-31) **contain an outcome column (`next_session_return`)** and originate from the Lane 2 join arc flagged in `docs/lane2_divergence_record_4f31bcb_6a75ec7.md` as ungated/exploratory. **Governance-flagged: outcome-bearing, do not treat as a neutral feature source.**
- `step2_daily_features.csv` is documented (Lane 2 records) as GDELT-only with **no market/outcome columns** — the cleaner news-feature substrate.

---

## 6A. Window discipline (the two-window rule)

The atlas spans datasets with **different date coverage**. A lane may not silently mix them.

- **Adjusted-close SPY price-shape forces** may use the frozen SPY sandbox window **2005–2022** if later promoted (`spy_yahoo_adjclose_..._sandbox_from_v8.csv`, `5cd92502…`).
- **OHLC / volume-dependent forces** are only available from the **2013–2022 OHLCV snapshot** (`2842647c…`) unless a broader vetted dataset is added.
- **News / GDELT-derived forces** are only available for their inventoried **2013–2022 window** unless a broader vetted dataset is added.
- **No lane may silently blend windows.**
- If a force requires a shorter window, **that window limitation must appear on the force card and in any future frozen lane design.**
- A future lane **may not compare a 2005–2022 price-only result against a 2013–2022 OHLC/news result without making that window mismatch explicit.**

**OHLC short-window treatment (Q5, owner-fixed).** Keep OHLC/volume-dependent cards **usable where inventoried**, but **window-flag them**:
- OHLC/volume-supported forces may be marked **`OPEN` or `FULL` only for the available 2013–2022 window.**
- They **may not be silently compared** with 2005–2022 price-only cards.
- **Any future promoted lane using OHLC/volume must declare the shorter 2013–2022 window in its frozen design.**
- If a **broader vetted OHLCV dataset** is later added, that requires **inventory update and SHA pinning before use.**

**Applied to the relevant cards:**
- **Gap force:** 2013–2022 only unless broader OHLC exists.
- **Range expansion / Compression (OHLC-range face):** 2013–2022 only unless broader OHLC exists.
- **Volume / liquidity proxies:** 2013–2022 only unless broader volume exists.
- **GDELT / news proxies:** 2013–2022 only.
- **Gold / cross-asset files that span sealed dates:** not promotable until a **sandbox-only derived file is created and SHA-pinned**, just like SPY.

**GLD specifically.**
- The raw GLD file (`gld_yahoo_v8`, `368fe450…`) **spans sealed dates (2004–2024).**
- Before any GLD-related card is promotable, a **derived sandbox-only GLD file must be created and SHA-pinned** (mirroring the SPY sandbox derivation that truncated before 2023).
- Until then, **GLD is inventory-only / not promotable.**

---

## 6B. Spent-trial artifacts and quarantine

The following are **read-only history, never atlas inputs:**

- `results/lane2_join/gdelt_spy_nextday.csv`
- any `next_session_return` outcome-bearing file from the prior Lane 2 / GDELT arc (e.g. `results/lane2_next_session_return/.../next_session_return.csv`).

> These files carry outcomes from a spent or governance-flagged prior trial. They may be cited as prior-art records, but they may not be used as atlas inputs. Future promoted atlas lanes must rebuild outcomes from primary closes through their own frozen row-construction function.

**Principle.** The atlas **may inventory** outcome-bearing joins, but it **may not reuse them as modeling inputs** unless a future frozen design explicitly justifies their provenance **and the owner approves**. (These specific files originate from the governance-flagged arc documented in `docs/lane2_divergence_record_4f31bcb_6a75ec7.md`, EXPLORATORY-ONLY.)

---

## 7. Force Dictionary

Field legend (FULL card): force name · status · group · cluster · canonical representative · derived? · forest metaphor · simple explanation · possible data proxy · required dataset · current availability · expected path-shape effects · canonical outcome family · measurable outcomes · null hypothesis · distinctness rule · risks/confounds · prior-art. STUB cards carry the reduced field set per §0 rules.

### Group 1 — Price-shape forces

#### Volatility — FULL
- **Status:** OPEN · **Group:** 1 · **Cluster:** VOLATILITY · **Canonical rep:** trailing realized volatility · **Derived?** No (it *is* the cluster anchor).
- **Forest metaphor:** the wind — how hard the trees are shaking right now.
- **Explanation:** dispersion of recent returns; the dominant, most-absorbing baseline in the program.
- **Proxy:** trailing RMS of log returns over a fixed window (e.g. the B1/B2 `ln_rv` family already used in the cusp instrument).
- **Required dataset:** daily adj_close. **Availability:** ✅ SPY sandbox 2005–2022 (`5cd92502…`).
- **Expected path-shape effects:** scales amplitude of all path geometry; persists (vol clustering).
- **Canonical outcome family:** forward realized volatility (1).
- **Measurable outcomes:** forward realized vol; vol persistence.
- **Null hypothesis:** trailing realized vol carries no predictive content for forward realized vol beyond a constant. (Practically expected to be the *strong* baseline, not the null.)
- **Distinctness rule:** N/A — it is the canonical representative every VOLATILITY card must beat.
- **Risks/confounds:** absorbs most path-shape proxies (this is exactly what killed Curvature).
- **Prior-art:** Cusp Geometry Lane v0.3 (B-baselines B1–B6).

#### Trend / Momentum / Mean reversion — FULL (one axis)
- **Status:** OPEN · **Group:** 1 · **Cluster:** AUTOCORRELATION · **Canonical rep:** lag-k autocorrelation / continuation–reversal statistic · **Derived?** No.
- **Forest metaphor:** the slope and lean of the ground — does a step tend to be followed by another in the same direction (trend/momentum) or a step back (mean reversion)?
- **Explanation:** **one autocorrelation axis at different signs and horizons.** Trend/momentum = positive continuation; mean reversion = negative continuation. They must **not** become three independent lanes.
- **Proxy:** lag-k autocorrelation of returns; sign and horizon parameterize the same statistic (e.g. B5-style `ac1`).
- **Required dataset:** daily adj_close. **Availability:** ✅ SPY sandbox 2005–2022.
- **Expected path-shape effects:** directional persistence vs reversal; path straightness vs zigzag.
- **Canonical outcome family:** forward realized vol (1); regime indicator (3).
- **Measurable outcomes:** sign/strength of continuation; horizon at which it flips.
- **Null hypothesis:** return autocorrelation at the chosen lag(s) adds nothing beyond a constant for the canonical outcome.
- **Distinctness rule:** any of trend/momentum/mean-reversion claiming separateness must beat the single autocorrelation representative AND show it is not the same axis at another horizon.
- **Risks/confounds:** horizon-shopping; sign flips by regime (see Mirror modifier, §9).
- **Prior-art:** pullback program (continuation/reversal setups); `prior-art: possible; requires owner confirmation`.

#### Zigzag — FULL
- **Status:** OPEN · **Group:** 1 · **Cluster:** VOLATILITY · **Canonical rep:** trailing realized vol · **Derived?** No.
- **Forest metaphor:** how crooked the path between two clearings is.
- **Explanation:** mean absolute step / path roughness. **This is the canonical killer baseline for curvature-like geometry** — the linearized `B6_mean_abs_dz` that absorbed F2.
- **Proxy:** mean |Δz| over the window (B6).
- **Required dataset:** daily adj_close. **Availability:** ✅ SPY sandbox 2005–2022.
- **Expected path-shape effects:** measures roughness without invoking curvature.
- **Canonical outcome family:** forward realized vol (1).
- **Measurable outcomes:** forward roughness; forward realized vol.
- **Null hypothesis:** zigzag adds nothing beyond trailing realized vol.
- **Distinctness rule:** must beat trailing realized vol; note zigzag is itself the baseline that beat curvature, so any *new* roughness force must beat zigzag too.
- **Risks/confounds:** near-collinear with realized vol.
- **Prior-art:** Cusp Geometry Lane v0.3 (B6 is the killer baseline).

#### Range expansion — FULL (OHLC window)
- **Status:** OPEN · **Group:** 1 · **Cluster:** VOLATILITY · **Canonical rep:** trailing realized vol · **Derived?** No.
- **Forest metaphor:** how wide the clearing got today vs yesterday.
- **Explanation:** high–low range growth; intraday amplitude.
- **Proxy:** rolling high–low range; range ratio. **Requires OHLC.**
- **Required dataset:** OHLC daily. **Availability:** ✅ but **2013–2022 only** (OHLCV snapshot `2842647c…`); ❌ pre-2013 (adj_close-only files have no OHLC).
- **Expected path-shape effects:** expansion precedes/accompanies vol bursts.
- **Canonical outcome family:** forward realized vol (1).
- **Measurable outcomes:** forward range; forward realized vol.
- **Null hypothesis:** range expansion adds nothing beyond trailing realized vol.
- **Distinctness rule:** beat realized vol; show range ≠ vol relabeled.
- **Risks/confounds:** window shortened to 2013–2022 reduces power; overlaps Gap force.
- **Prior-art:** none specific.

#### Compression — FULL
- Mirror of range expansion (low range / coiling). **Cluster:** VOLATILITY · rep trailing realized vol · OPEN. **Availability:** ✅ adj_close (vol-compression) 2005–2022; OHLC-range-compression 2013–2022. **Null:** compression adds nothing beyond low trailing vol. **Distinctness:** must beat "vol is simply low." **Confound:** definitionally the inverse of vol level. **Metaphor:** the unnatural stillness before wind. **Prior-art:** none specific.

#### Shock / jump — FULL
- **Status:** OPEN · **Cluster:** VOLATILITY · rep trailing realized vol · Group 1. **Metaphor:** a branch suddenly snapping. **Proxy:** standardized return exceedance / jump indicator on adj_close. **Availability:** ✅ 2005–2022. **Outcome family:** forward realized vol (1); forward max drawdown (2). **Null:** jump count adds nothing beyond trailing realized vol for forward vol/drawdown. **Distinctness:** beat realized vol; show jumps ≠ high-vol tail. **Confound:** jumps inflate realized vol itself (mechanical overlap). **Prior-art:** none specific.

#### Cusp / reversal — CLOSED
- **Status:** `CLOSED` · **Group:** 1 · **Cluster:** VOLATILITY · rep trailing realized vol / zigzag.
- **Reason:** Cusp Geometry Lane v0.3 — the cusp/reversal vertex geometry (and its κ curvature statistic) was tested and **did not survive B6/zigzag** for SPY 2005–2022 (incremental R² `-0.0256`, `0/10` folds). **Do not reopen.** No alternate windows/thresholds/mirrors/sealed test.
- **Prior-art:** `cusp_geometry_lane_design_memo_v0_3.md`; closure `ac098b66…`.

#### Curvature — CLOSED
- **Status:** `CLOSED` · **Group:** 1 · **Cluster:** VOLATILITY · rep zigzag/B6.
- **Reason:** same lane; `F2_kappa_mean` not separable from zigzag/B6 for SPY 2005–2022. **Do not reopen.**
- **Prior-art:** Cusp Geometry Lane v0.3.

#### Drawdown — FULL
- **Status:** OPEN · **Group:** 1 · **Cluster:** VOLATILITY · rep trailing realized vol · **Derived?** No (but **doubles as canonical outcome #2**).
- **Metaphor:** how deep the valley got before the next ridge.
- **Proxy:** rolling peak-to-trough on adj_close. **Availability:** ✅ 2005–2022.
- **Outcome family:** forward max drawdown (2).
- **Null:** trailing drawdown adds nothing beyond trailing realized vol for forward max drawdown.
- **Distinctness:** as a *force*, must beat realized vol; as an *outcome*, see §5 (tail outcome).
- **Confound:** drawdown is largely vol × horizon; risk of restating vol.
- **Prior-art:** none specific.

#### Recovery — FULL
- **Status:** OPEN · **Group:** 1 · **Cluster:** VOLATILITY (recovery-time face; autocorr-adjacent) · rep trailing realized vol · **Derived?** partially (depends on drawdown). **Metaphor:** how fast the forest regrows after a fire. **Proxy:** time/þ to reclaim prior peak post-drawdown. **Availability:** ✅ 2005–2022. **Outcome family:** regime indicator (3); derived: recovery time. **Null:** recovery speed adds nothing beyond vol + drawdown. **Distinctness:** must beat "low vol recovers faster." **Confound:** mechanically tied to drawdown depth and vol. **Prior-art:** none specific.

#### Path length — FULL
- **Status:** OPEN · **Group:** 1 · **Cluster:** VOLATILITY · rep trailing realized vol · **Derived?** No. **Metaphor:** total distance walked, not straight-line displacement. **Proxy:** sum of step lengths over window (F4-style pathlen in cusp instrument). **Availability:** ✅ 2005–2022. **Outcome family:** forward realized vol (1). **Null:** path length adds nothing beyond realized vol. **Distinctness:** beat realized vol; note path length is near-collinear with vol×n. **Confound:** strong collinearity with vol (a sibling of what absorbed curvature). **Prior-art:** Cusp Geometry Lane v0.3 (F4 descriptive).

#### Volatility-of-volatility — FULL
- **Status:** OPEN · **Group:** 1 · **Cluster:** VOLATILITY · rep trailing realized vol · **Derived?** Yes (second moment of vol). **Metaphor:** how gusty the wind itself is. **Proxy:** dispersion of rolling realized vol. **Availability:** ✅ 2005–2022. **Outcome family:** forward realized vol (1); regime indicator (3). **Null:** vol-of-vol adds nothing beyond vol level. **Distinctness:** beat vol level; show it is not just high-vol regions. **Confound:** estimation noise; overlaps regime. **Prior-art:** none specific.

#### Gap force — FULL (OHLC window)
- **Status:** OPEN · **Group:** 1 · **Cluster:** VOLATILITY · rep trailing realized vol · **Derived?** No. **Metaphor:** waking to find the trail moved overnight. **Proxy:** open-vs-prior-close gap. **Requires OHLC.** **Availability:** ✅ **2013–2022 only** (OHLCV snapshot `2842647c…`); ❌ pre-2013. **Outcome family:** forward realized vol (1). **Null:** overnight gap magnitude adds nothing beyond trailing realized vol. **Distinctness:** beat realized vol; show gap ≠ vol. **Confound:** short window; adjustment/dividend effects in close-to-open. **Prior-art:** none specific.

### Group 2 — Market psychology forces

#### Attention — FULL (window-limited)
- **Status:** OPEN (drift-controlled representative only) · **Group:** 2 · **Cluster:** NEWS/ATTENTION · **Canonical rep:** **coverage-normalized / drift-controlled** news/attention count (**not** raw count) · **Derived?** No. **Metaphor:** how many eyes are on the same clearing. **Proxy:** a **coverage-normalized / drift-controlled** GDELT attention measure. **The GDELT raw-count/coverage proxy is `CLOSED` (Q8)** — raw `total_row_count` / step2 log1p raw count may appear only as **read-only prior art or an explicitly drift-confounded artifact**, never as the representative this card beats. **Availability:** ✅ **2013–2022 only** (`84b6ac9f…`, `48a64e1c…`; see §6A window discipline). **Outcome family:** forward realized vol (1). **Measurable outcomes:** forward vol; activity. **Null:** the drift-controlled attention measure adds nothing beyond trailing realized vol for forward vol. **Distinctness:** must beat realized vol AND survive drift control (a drift-controlled / coverage-normalized count, not the raw count). **Confound:** **`collection drift` (standing confound for this cluster)**; attention spikes co-occur with vol (endogeneity); overlaps closed news lanes.
- **Prior-art (owner-confirmed program record):** the **GDELT count/coverage → SPY exploratory null** — raw Spearman ≈ **−0.15 to −0.18**, effect **dissolved under drift control**, documented with a formal divergence record at **`docs/lane2_divergence_record_4f31bcb_6a75ec7.md`** (EXPLORATORY-ONLY; ungated arc). Consequence: **GDELT raw-count/coverage proxy = `CLOSED`** (drift-confounded null). **Volume-based attention proxies: untested** unless separately inventoried and promoted.

#### Uncertainty — DERIVED
- **Status:** OPEN (DERIVED) · **Group:** 2 · **Cluster:** VOLATILITY × NEWS/ATTENTION · rep trailing realized vol · **Derived?** Yes (= volatility + disagreement/news dispersion). **Metaphor:** fog over the canopy. **Components:** volatility (✅ 2005–2022) + news dispersion (partial, GDELT 2013–2022). **Cannot be promoted before components defined.** **Outcome family:** forward realized vol (1); regime (3). **Null:** the composite adds nothing beyond realized vol. **Confound:** mostly a vol restatement. **Prior-art:** TTG dispersion threads.

#### Panic — DERIVED
- **Status:** OPEN (DERIVED) · **Group:** 2 · **Cluster:** VOLATILITY × LIQUIDITY · rep trailing realized vol · **Derived?** Yes (= high vol + downside shock + volume/stress). **Components:** vol (✅), shock (✅), volume (✅ 2013–2022). **Metaphor:** the whole herd bolting at once. **Outcome family:** forward max drawdown (2). **Null:** composite adds nothing beyond vol+shock. **Confound:** mechanical overlap with vol tail. **Prior-art:** none specific.

#### Euphoria — DERIVED (STUB on sentiment)
- **Status:** STUB (DERIVED) · **Group:** 2 · **Cluster:** AUTOCORRELATION × VOLATILITY × NEWS/ATTENTION · rep trailing realized vol / autocorr. **= low vol + strong trend + positive sentiment.** **Required dataset:** a positive-sentiment series (none clean in inventory; GDELT tone is a weak proxy). **Why not full:** sentiment component unavailable. **Metaphor:** the false summer before the frost.

#### Exhaustion — DERIVED
- **Status:** OPEN (DERIVED) · **Group:** 2 · **Cluster:** AUTOCORRELATION × VOLATILITY · rep autocorr statistic. **= extended trend + high activity + weakening continuation.** **Components:** trend/autocorr (✅), activity/vol (✅), continuation-decay (✅, all from adj_close). **Metaphor:** a runner whose strides shorten near the finish. **Outcome family:** regime (3). **Null:** composite adds nothing beyond the autocorrelation representative. **Confound:** horizon-shopping. **Prior-art:** pullback exhaustion setups (`prior-art: possible; requires owner confirmation`).

#### Fear / Greed / Herding / Narratives / Technical levels / Self-fulfilling belief / Anchoring — STUB
- **Status:** STUB · **Group:** 2 · **Cluster:** mostly NEWS/ATTENTION or VOLATILITY (Technical levels: price-derived; Self-fulfilling belief: residual-adjacent). **Required dataset:** market-sentiment indices (VIX, put/call, surveys), positioning, or news-sentiment — **none clean in inventory**. **Why not full:** no sentiment/positioning data. **Metaphors:** Fear = animals fleeing; Greed = overgrazing; Herding = single trampled trail; Narratives = the story the forest tells itself; Technical levels = remembered waterlines; Anchoring = staring at an old high-water mark. *(**Technical levels → `STUB` (Q4, owner-fixed).** An honest test needs **watched-level data or a carefully defined level proxy**. A price-only prior-high/prior-low proxy risks becoming **anchoring or range behavior wearing a technical-level mask**. Technical-levels stay STUB until the required data/proxy **and** their cluster distinctness rule are defined — not promotable on price alone.)*

### Group 3 — Macro weather forces — ALL STUB (vintage-gated)

All of: interest rates, Fed policy, inflation, economic growth, recession risk, unemployment/jobs, yield curve, credit spreads, dollar strength, oil/energy, fiscal policy, liquidity regime, policy uncertainty.

- **Status:** `STUB` (each) · **Group:** 3 · **Cluster:** MACRO WEATHER · **Canonical rep:** simple macro variable or event flag.
- **Required dataset:** macro series — **none present in repo inventory.**
- **Vintage flag:** **`unknown` → must be `vintage-safe` (point-in-time) when sourced.** Revised series (CPI, GDP, payrolls) are **leakage-contaminated unless point-in-time vintages are sourced**; if a revised series is later added, mark availability **`present but vintage-unsafe`**.
- **Why not full:** no data + vintage hazard.
- **Metaphor (cluster):** the season and the climate — slow background weather over the forest.
- **Prior-art:** none in-repo.

### Group 4 — Company / fundamental forces — ALL STUB (vintage-gated)

Earnings, revenue growth, margins, valuation multiples, buybacks, dividends, guidance, sector rotation, mega-cap concentration, index composition changes, market breadth, **dispersion**.

- **Status:** `STUB` (each), **except (fundamental) dispersion → `RESERVED`** to the live dispersion lane (§2, §3.1, §11 Q1). The atlas may index it but may not explore, test, promote, or redefine it.
- **Group:** 4 · **Cluster:** MACRO WEATHER (fundamentals) / cross-asset for breadth & dispersion · **rep:** simple fundamental variable.
- **Required dataset:** fundamentals / constituent data — **none present.**
- **Vintage flag:** **required; `unknown` until point-in-time sourced.**
- **Metaphor:** the soil chemistry under individual trees.
- **Prior-art:** dispersion → live dispersion lane (`prior-art: possible; requires owner confirmation`).

### Group 5 — Liquidity and market-structure forces — ALL STUB

Liquidity, bid-ask spread, order flow, market makers, options hedging, futures arbitrage, ETF creation/redemption, closing-auction flows, rebalancing flows, vol-targeting funds, risk-parity funds, CTAs/trend-followers, margin calls/liquidations, short interest, dealer positioning.

- **Status:** `STUB` (each) · **Group:** 5 · **Cluster:** LIQUIDITY · **rep:** volume or spread proxy.
- **Partial availability:** only **volume** exists (OHLCV snapshot + `market_daily_spy.csv`, 2013–2022). A **bare volume/liquidity** card could be promoted to FULL on volume alone; everything requiring order-book/options/positioning data stays STUB.
- **Required dataset:** order flow, quotes/spreads, options, positioning — **none present** (volume only).
- **Metaphor:** the width and mud of the trails — how easily the herd can move.
- **Prior-art:** none in-repo.

### Group 6 — News and event forces

- **News direction — `CLOSED`.** Prior Lane 2 v1.1 null (`lane2_ttg_spy_prereg_v1.1.md`, `lane2_ttg_spy_v1_results_v0.1.md`). Do not treat as open unless owner provides new scope.
- **News magnitude / intensity — `OPEN`** (DERIVED-eligible). **Cluster:** NEWS/ATTENTION · rep simple count. **Proxy:** GDELT `nummentions` / `avgtone` intensity → next-session **absolute** move or volatility. **Availability:** ✅ 2013–2022 (count/feature builds; TTG event archives). **Outcome family:** forward realized vol (1). **Null:** news intensity adds nothing beyond trailing realized vol + plain news count for forward absolute move/vol. **Requires its own locked design if promoted** (the TTG magnitude-pressure MDE arithmetic governs realism). **Prior-art:** TTG magnitude-pressure arc (no-spend terminal on achievable seal).
- **STUB** (each): economic data releases, Fed meetings, earnings season, geopolitical events, banking stress, pandemic/health shocks, regulation/legal shocks, unexpected announcements — **require event-date datasets not present** (some derivable from GDELT event codes, but not cleanly inventoried as event-flags). **News velocity, news decay, sentiment disagreement** — partially derivable from GDELT counts/tone 2013–2022, marked STUB pending a precise proxy + their own design (they live under the NEWS/ATTENTION cluster and must beat the plain count).
- **Standing confound (whole cluster):** `collection drift` — every NEWS/ATTENTION card must list it; raw counts are drift-confounded unless normalized/controlled (§4.1).
- **Metaphor:** sudden storms and lightning strikes.
- **Prior-art for the group:**
  - **News direction:** `CLOSED` null under prior **Lane 2 TTG → SPY v1.1** (`lane2_ttg_spy_prereg_v1.1.md`, `lane2_ttg_spy_v1_results_v0.1.md`).
  - **News magnitude / intensity:** OPEN but **untested here**; requires its own frozen design if promoted (TTG magnitude-pressure arc was a **no-spend terminal**, `lane2_ttg_magnitude_pressure_weekly_spend_decision_v0.1.md`).
  - **GDELT raw-count/coverage proxy:** **`CLOSED`** (Q8) — exploratory null, drift-confounded; raw Spearman ≈ −0.15 to −0.18, dissolved under drift control; divergence record `docs/lane2_divergence_record_4f31bcb_6a75ec7.md` (owner-confirmed program record). Not a promotable representative; read-only prior art / drift-confounded artifact only.

### Group 7 — Cross-asset forces

- **Gold — `STUB` / inventory-only (not promotable yet).** **Cluster:** cross-asset · rep cross-asset price proxy · **Canonical rep:** cross-asset price proxy · **Distinctness rule:** gold co-movement must beat SPY's own trailing vol/autocorr. **Proxy:** GLD adj_close co-movement / lead-lag with SPY. **Availability:** ⚠️ `gld_yahoo_v8` (`368fe450…`) spans **2004–2024** — **contains sealed dates.** Per §6A: the **raw GLD file spans sealed dates**, so **before any GLD-related card is promotable a derived sandbox-only GLD file must be created and SHA-pinned** (mirroring the SPY sandbox derivation that truncated before 2023). **Until then, GLD is inventory-only / not promotable.** **Outcome family:** regime (3); forward realized vol (1). **Null:** gold co-movement adds nothing beyond SPY's own trailing vol/autocorr. **Confound:** macro-driven joint moves. **Prior-art:** Harmonic Calendar GLD (closed null); GC/ES state-map work.
- **Cross-asset dispersion — `RESERVED`** (live dispersion lane; §3.1). Do not promote here.
- **Correlation regime — `RESERVED`** (live dispersion lane; §3.1). Do not promote here.
- **STUB** (each): bond yields, VIX/implied volatility, dollar, oil, credit markets, global equities, crypto/risk appetite, commodity basket — **no price series present** for these in inventory.
- **Metaphor:** weather blowing in from neighboring forests.

### Group 8 — Calendar / time forces — FULL-eligible (no market values needed)

Day of week, month-end, quarter-end, options expiration, tax season, holiday liquidity, earnings calendar, Fed calendar, turn-of-month, year-end.

- **Status:** OPEN (each; FULL-eligible) · **Group:** 8 · **Cluster:** CALENDAR · **Canonical rep:** simple calendar dummy · **Derived?** No.
- **Forest metaphor:** the clock of seasons and market-hours rituals.
- **Proxy:** deterministic calendar dummies built from the **date index** of any in-window price file — **no market value read**.
- **Required dataset:** a trading-date index. **Availability:** ✅ SPY sandbox index 2005–2022 (dates only). *(Options-expiration / Fed / earnings calendars need an external event-date list → those specific cards are STUB until such a list is sourced; pure date-arithmetic dummies are FULL.)*
- **Canonical outcome family:** forward realized vol (1); regime (3).
- **Measurable outcomes:** mean forward vol by calendar bucket.
- **Null hypothesis:** the calendar dummy adds nothing beyond a constant / trailing realized vol for the canonical outcome.
- **Distinctness rule:** a calendar effect must beat the plain dummy and not be a vol-seasonality restatement.
- **Risks/confounds:** multiple-comparison across many calendar cuts (shared α applies); overlap with known seasonality.
- **Prior-art:** **Harmonic Calendar** studies — SPY MVT **null** and GLD **null** (`docs/harmonic_calendar_*`). Calendar effects already have an in-program null record; do not re-run those exact cells.

### Group 9 — Data-construction forces — FULL-eligible (essential)

Adjusted-close choice, raw close vs adjusted close, vendor methodology, missing days, rounding, bad ticks/errors, survivorship/composition, time-zone/calendar handling, revision force, adjustment lag.

> **"Group 9 protects us from studying the map instead of the forest."**

- **Status:** OPEN (each; FULL-eligible) · **Group:** 9 · **Cluster:** DATA CONSTRUCTION · **Canonical rep:** source / adjustment-policy check · **Derived?** No.
- **Forest metaphor:** the cartographer's pen — distortions in the map mistaken for features of the land.
- **Proxy:** compare `Close` vs `Adj Close` paths; vendor/provenance fields; missing-day calendars; rounding granularity; adjustment timing.
- **Required dataset:** the inventoried price files themselves. **Availability:** ✅ — the OHLCV snapshot (`2842647c…`) carries **both `Close` and `Adj Close`** (adjustment fork live); `market_daily_spy.csv` (`8a87fc05…`) carries `source_vendor/retrieved_at/timezone/calendar`; source files name-stamp their content SHA.
- **Canonical outcome family:** regime (3) / data-quality flags (these forces gate *interpretation* more than predict outcomes).
- **Measurable outcomes:** divergence between adjusted/raw paths; count/placement of missing days; sensitivity of any force to adjustment choice.
- **Null hypothesis:** the construction choice does not materially change the path statistic under study.
- **Distinctness rule:** must be checked **before** any behavioral interpretation (hygiene rule §8.6).
- **Risks/confounds:** dividend/split adjustment lag; vendor revision; survivorship in any constituent extension.
- **Prior-art:** the cusp lane fixed on `adj_close`; the `Close`/`Adj Close` stop-and-ask in the cusp sandbox is the precedent.

### Group 10 — Hidden / noise forces

Group 10 is **not** a set of ordinary testable cards. See **§9A (Residual doctrine)** and **§9B (Modifiers vocabulary)** for the restructure — residual explanations have no null hypotheses; modifiers describe *how* other cards behave, they are not standalone forces.

---

## 8. Data hygiene and leakage rules

1. **No sealed data may be opened for atlas drafting.** (≥ `2023-01-01`.)
2. **Inventory may read headers and first/last date metadata only** — never value cells, never sealed-period values.
3. **Dataset SHA-256 must be recorded** for any dataset inventoried (done in §6).
4. **Files spanning 2023+ must be marked as containing sealed-period dates** — here `spy_yahoo_v8` (`e8fc0357…`) and `gld_yahoo_v8` (`368fe450…`). The GDELT raw zip cache upper bound was verified **by filename only** (2026-06-13): latest encoded date `2022-12-31`, **no sealed-period filenames** — no zip was opened (§6.4).
5. **Revised macro/fundamental series are vintage-unsafe** unless point-in-time vintages are sourced; mark `present but vintage-unsafe` where applicable.
6. **Data-construction forces (Group 9) must be considered before behavioral interpretation.**
7. **No force is promoted to a lane without a frozen design memo** (§3 pattern).
8. **No promoted lane receives a fresh sealed-alpha budget; alpha is shared across the atlas family.**
9. **Null results are valid records.**
10. **Closed lanes stay closed** (Curvature, Cusp/reversal, News direction; calendar cells already null).
11. **Raw news/attention counts are not canonical unless drift-controlled or coverage-normalized** (§4.1; raw count is the known drift artifact, not the boring representative).
12. **Spent-trial outcome joins are read-only history and cannot be atlas inputs** (§6B; `gdelt_spy_nextday.csv`, `next_session_return.csv`).

Additional standing flags from inventory: the join/outcome files (`gdelt_spy_nextday.csv`, `next_session_return.csv`) are **outcome-bearing and from a governance-flagged arc** — not neutral feature sources; the two `…_20241231_…` adj_close files must be truncated before 2023 (as the cusp sandbox was) for any in-window use.

---

## 9. Group 10 — Residual doctrine and modifiers

Group 10 is **not** a set of ordinary force cards with null hypotheses. It splits into two parts.

### A. Residual doctrine

These are **residual explanations, not clean cards with null hypotheses**:

- Unknown trader motives
- Hidden positioning
- Private information
- Randomness
- Force cancellation
- Projection / shadow error

**Doctrine.** Unexplained variance is discussed as a *residual*, not promoted as a measurable force. After the cluster baselines and any promoted force are fit, what remains is attributed to this residual pool **without pretending each unknown is directly measurable**. We may *characterize* the residual (its size, its time-clustering, whether it concentrates in shocks) but we do **not** write a null hypothesis for "private information" as if it were an observable series. "Force cancellation" and "projection/shadow error" warn that the observed price path is a *shadow* of latent forces: two real forces may net to nothing, or the price-shadow may misrepresent the underlying force — so a measured null does not prove a force is absent, only that it left no separable trace in this projection.

### B. Modifiers vocabulary

These **modify other force cards; they are not standalone forces:**

- **Delayed force** — an effect may appear later, not immediately; its effect on the path shows up days after its driver.
- **Threshold force** — a force may matter only after crossing a certain level (small moves do nothing; large ones do).
- **Mirror / inversion force** — a force may appear with **opposite sign in different regimes**, or the observed price-shadow may **invert** the real underlying force.
- **Regime force** — the same force may behave differently in **calm vs crisis** conditions (present in some states, absent in others).
- **Interaction force** — **mud plus wolf is not the same as mud alone plus wolf alone**; two forces combine non-additively.
- **Saturation force** — more of the same force may **stop adding effect after a cap** (the effect flattens past a point).

**Anti-rescue principle (exact).**

> Mirror/inversion is not a license to rescue a failed lane after the fact. It must be specified before promotion, with a reason and a frozen test design.

When a promoted lane invokes any modifier, the modifier must be specified in its frozen memo *before promotion* (e.g. the exact threshold, the regime definition, the inversion sign and its reason) — modifiers must **not** become a back-door for post-hoc tuning or for resurrecting a closed lane.

---

## 10. Promotion protocol

A force becomes a tested lane only by this path:

1. **Card complete** — proxy, dataset, canonical outcome, null, confounds, cluster baseline all defined (FULL card, not STUB).
2. **Not pre-closed/reserved** — status is `OPEN`.
3. **Budget available** — `MAX_ACTIVE_ATLAS_LANES = 1` not exceeded, and the **shared** sealed budget (`ATLAS_FAMILY_ALPHA = 0.05`, `MAX_SEALED_ATTEMPTS_ATLAS_V0X = 5` at `PER_ATTEMPT_ALPHA = 0.01`) has room; an entry is opened in the **single atlas trial ledger**.
4. **Frozen design memo** — authored in the Cusp-lane pattern (statistic/proxy · target/canonical outcome · baselines · cluster canonical representative · sandbox gate · sealed rule · multiple-testing ledger). Hash-pinned and committed before any data contact.
5. **Sandbox gate (in-window only)** — pre-registered PASS/FAIL on 2005–2022 (or the force's available in-window span). A **FAIL closes the lane as exploratory null** unless a new version is explicitly designed and logged before further data contact.
6. **Sealed authorization** — only after a sandbox **PASS** AND **explicit owner authorization** may sealed (≥ 2023-01-01) data be opened, spending from the **shared** sealed-α budget.
7. **Record** — PASS or FAIL is written to the trial ledger and the research memory index; closed lanes stay closed.

**First promotion (Q9, owner-fixed): intentionally deferred.** No first force/lane is chosen in this memo. The atlas enters the repo as a **neutral map**, not reorganized around a favorite next lane. Any promotion decision must happen in a **separate future session** and **require its own frozen design memo**.

### Modifiers and the anti-rescue rule

The **modifiers vocabulary** (delayed / threshold / mirror-inversion / regime / interaction / saturation) lives in **§9B**. Any modifier a promoted lane invokes **must be specified in its frozen memo before promotion** — including the **mirror/inversion anti-rescue rule** (§9B): *mirror/inversion is not a license to rescue a failed lane after the fact; it must be specified before promotion, with a reason and a frozen test design.* Modifiers must not become a back-door for post-hoc tuning.

---

## 11. Open questions / owner decisions required

Most v0.1 decisions are now **RESOLVED** (below). The single substantive item still pending is the dispersion-memo commit (Q1).

1. **Live dispersion lane provenance — STILL OPEN.** Owner-confirmed but its design memo is **not yet committed** (pending the §6a.6/§7 whitelist fix). **Cross-asset dispersion / correlation regime / fundamental dispersion** are RESERVED with provisional grounding in §3.1. → *When the dispersion memo is committed, it supersedes the §3.1 stub; the §6a.6/§7 fix remains a separate future task and is not retired by this memo.*
2. ~~`MAX_ACTIVE_ATLAS_LANES`~~ — **RESOLVED (draft literal): `= 1`** (§3). Amend on the record to change.
3. ~~Shared sealed-α budget + debit mechanism~~ — **RESOLVED (§3):** literals `ATLAS_FAMILY_ALPHA = 0.05`, `MAX_SEALED_ATTEMPTS_ATLAS_V0X = 5`, `PER_ATTEMPT_ALPHA = 0.01`; **debit mechanism fixed** — prior closed lanes (Cusp v0.3, Lane 2 news-direction) **do not** retroactively debit (they predate the atlas); a sealed attempt debits 0.01 **only at sealed-data contact**; sandbox failures debit nothing; every debit logged (date · lane · memo SHA · sealed boundary · α · result · within-5 check); no fresh per-lane budget.
4. ~~Technical levels~~ — **RESOLVED: `STUB`** (Group 2 card). Not promotable on a price-only prior-high/low proxy (risks anchoring/range in disguise); needs watched-level data or a defined level proxy **and** its cluster distinctness rule first.
5. ~~OHLC window mismatch~~ — **RESOLVED (§6A, Q5):** OHLC/volume cards usable where inventoried but **window-flagged to 2013–2022 only**, never silently compared to 2005–2022 price-only cards; any promoted OHLC/volume lane must declare the short window in its frozen design; a broader OHLCV dataset requires inventory update + SHA pinning before use.
6. ~~GDELT raw zip cache upper bound~~ — **RESOLVED by filename audit (2026-06-13): latest encoded date `2022-12-31`, no sealed-period filenames (§6.4).** GDELT-derived news cards are restricted to 2013–2022 only (§6A).
7. **Outcome-bearing join files** — quarantined in §6B (read-only history, governance-flagged arc). Confirmed: no future lane reuses them without an explicit frozen-provenance justification + owner approval. *(Standing rule; no further decision needed unless a future lane requests an exception.)*
8. ~~GDELT attention/volume null~~ — **RESOLVED: GDELT raw-count/coverage proxy → `CLOSED`** (Q8). Official closed record (drift-confounded exploratory null, ρ ≈ −0.15 to −0.18; `lane2_divergence_record_4f31bcb_6a75ec7.md`). Raw count is read-only prior art / drift-confounded artifact only; the Attention card stays OPEN **only** under a coverage-normalized / drift-controlled representative.
9. ~~First force to promote~~ — **RESOLVED: intentionally deferred** (Q9). No first force is chosen in this memo. The atlas enters the repo as a **neutral map**, not reorganized around a favorite next lane. Any promotion decision must happen in a **separate future session and require its own frozen design memo** (within the `MAX_ACTIVE_ATLAS_LANES = 1` cap).

---

*Draft ends. No tests run, no modeling, no tuning, no sealed values inspected, no sealed data accessed for analysis, nothing staged/committed/pushed. Awaiting owner review.*
