# Human Field × Base-12 Pullback Atlas — Implementation Plan v0.1

**Version:** v0.1 (Implementation plan — draft for the next planning gate)
**Date:** 2026-05-17
**Project:** Coherent Numbers
**Artifact type:** Implementation plan (Lane 1 only)
**Status:** Draft. No code authorized. No data loaded for analysis. No atlas generated. No tables computed. No heatmaps generated. No OOS access. No commit. Awaiting explicit authorization to implement.

**Governing design memo:** `docs/human_field_base12_pullback_atlas_design_memo_v0.1.md` (v0.1, revised 2026-05-17, accepted as a draft for this planning gate).

**Audit-language note (OOS framing).** No OOS analysis was performed. The existing SPY artifact's date coverage was inspected only to verify availability; Atlas v0.1 remains designed to read no rows beyond each event's permitted `t-1` lookback boundary, and no post-2022 rows are used in any atlas computation.

---

## 0. Scope of this document

This plan specifies *how* Atlas v0.1 would be built if authorized. It writes no code, loads no population for analysis, computes no tables, and generates no figures. It exists so the build can be reviewed before any execution. All design constraints are inherited from the governing design memo; this plan adds only construction detail and does not re-open any design decision (single-anchor labels, `r_multiple` outcome, `indeterminate-state` rule, realized-volatility arousal proxy, exploratory/no-verdict posture).

## 1. Input files

All inputs are already present in the repo and frozen. No external data acquisition is required.

### 1.1 Frozen Phase 3b / Candidate C pullback population (the 1,282-trade substrate)

| Asset | Frozen path | Rows (excl. header) |
|---|---|---:|
| SPY | `data/raw/pullback_phase3b_spy_trades_2005_2022.csv` | 243 |
| EFA | `data/raw/pullback_phase3b_efa_trades_2005_2022.csv` | 283 |
| EEM | `data/raw/pullback_phase3b_eem_trades_2005_2022.csv` | 261 |
| GLD | `data/raw/pullback_phase3b_gld_trades_2005_2022.csv` | 253 |
| TLT | `data/raw/pullback_phase3b_tlt_trades_2005_2022.csv` | 242 |
| **Pooled** | — | **1,282** |

Compact 11-column schema: `entry_date, setup_date, direction, entry_price, exit_price, exit_date, exit_reason, bars_held, r_multiple, first_target_hit, initial_risk`. The SPY base 301-trade file (`pullback_spy_base_301_trades_2000_2022.csv`) is **not** an input — Candidate C uses only the pooled Phase 3b population.

### 1.2 Manifest for substrate verification

- `docs/pullback_population_freeze_manifest_v0.1.md` (freeze commit `5225bfd`) — supplies the per-file SHA-256 digests and row counts the loader verifies against.

### 1.3 Candidate C phase-label logic source

- `src/candidate_c_lens.py` → `assign_annual_sector_phase(entry_date, bucket_count)` — the single civil-date March-20 anchor formula (Candidate C design memo §7.1): `cycle_bounds_for` locates the March-20 cycle, `phase = (days_since_start * bucket_count) // cycle_length_days`, with `PhaseRangeError` on out-of-range (no silent clamp).
- **Excluded by Decision 1:** `assign_anchor_shifted_phase` (§7.2, 365-DOY surface), `candidate_c_pss.py`, `candidate_c_protocol.py`, and all permutation / median-over-surface / verdict machinery. The atlas imports the §7.1 function only and computes nothing from the Candidate C protocol layer.

### 1.4 Frozen SPY auxiliary series (valence + realized-volatility arousal)

- Artifact: `data/raw/spy_yahoo_v8_19930129_20241231_e8fc0357410ce499da8f67e09b4c9908232e18a55445f38969e77fa712aaaa56.csv` (frozen at commit `ed199bd`; loader architecture `30faabb`).
- Loader: `src/spy_loader.py` → `load_spy()` returns `date, adj_close, log_return, log_return_sq` (sorted ascending, de-duplicated, NaN/≤0 dropped per the loader's documented policy). The atlas re-uses this loader read-only; `log_return` is taken as provided rather than recomputed.
- Span 1993-01-29 → 2024-12-31 — covers 2005–2022 with full trailing history for the 30-day and 252-day windows.

## 2. Loader rules

- **Pullback events.** Only the five frozen Phase 3b CSVs (§1.1) are read for events. Each file's SHA-256 is recomputed and checked against the freeze manifest before any row is used; a mismatch aborts before feature construction. Per-file row counts are checked against §1.1. No filtering, sorting, recoding, or re-signing of the frozen rows; the atlas reads them as stored.
- **SPY auxiliary series — hard OOS read boundary.** Immediately after `load_spy()`, the SPY frame is **truncated to `date ≤ 2022-12-21`** (the maximum permitted event `entry_date` per the freeze manifest OOS sanity check) **before any feature construction**. All trailing windows are computed from this truncated frame only. Because every trailing window ends at `t-1 < entry_date ≤ 2022-12-21`, no post-2022 SPY row can enter any computation. This is a structural guard (filter-then-compute), not a runtime assertion sprinkled through the code: the post-2022 rows are physically removed from the working frame at load time. A post-truncation assertion `max(spy.date) ≤ 2022-12-21` is added as a belt-and-braces check that aborts on violation.
- **No 2023+ contact anywhere.** No pullback OOS file is opened. The pullback repo HEAD is not consulted. No 2023+ SPY row survives the §2 truncation. Nothing in the atlas reads, joins, previews, or computes against any row dated after 2022-12-21.
- **Determinism.** All loads are deterministic; the atlas consumes no random seed (it has no permutation, no null, no resampling).

## 3. Feature construction

Per trade in the pooled 1,282-row substrate, in this order:

1. **`asset`** — from the source file identity.
2. **`entry_date` (`t`)** — parsed from the frozen `entry_date` column (date granularity).
3. **`direction`** — mapped from the frozen `direction` column to `long` / `short` with no re-signing; `is_long` boolean derived for the long-share computations only.
4. **`r_multiple`** — taken exactly as stored (Candidate C Appendix B.5 convention: no multiplication by direction, no transformation).
5. **`phase_12`** — `assign_annual_sector_phase(entry_date, 12)` → integer 0–11.
6. **`phase_10`** — `assign_annual_sector_phase(entry_date, 10)` → integer 0–9 (comparator only; same deterministic March-20 anchor).
7. **`t-1`** — the last SPY session in the truncated frame strictly before `entry_date`. Weekends/holidays resolve to the last available prior session; a true data gap that prevents window population yields `indeterminate-state` (§3 step 10).
8. **`prior_30d_spy_return`** — simple return of `adj_close` over the 30-trading-day window ending at `t-1` (i.e. `adj_close[t-1] / adj_close[t-1 minus 30 sessions] − 1`), never including `t`.
9. **`prior_rvol_pctile_252`** —
   - daily SPY `log_return` (from the loader);
   - realized volatility = rolling **20-trading-day** standard deviation of `log_return`, evaluated over the prior 20 trading days ending at `t-1`. **`ddof=1` (locked, sample standard deviation).** Atlas v0.1 computes realized volatility as the 20-trading-day sample standard deviation of SPY daily log returns, `ddof=1`. Because the window length is fixed at 20 sessions, changing `ddof` would multiply every rolling volatility value by a constant factor and therefore would not change percentile ranks under complete fixed-length windows. `ddof=1` is retained as the documented sample-volatility convention. This is not an open implementation question;
   - percentile rank of that realized-vol value within the trailing **252-trading-day** window of realized-vol values ending at `t-1` (window of the daily realized-vol series, not of returns).
10. **`ns_state`** — from valence × arousal:
    - valence = positive if `prior_30d_spy_return > 0` else negative;
    - arousal = high if `prior_rvol_pctile_252 ≥ 0.75` else low;
    - state map: (pos, low) → **calm bull**; (pos, high) → **manic / unstable rally**; (neg, high) → **panic / crisis**; (neg, low) → **quiet bearish / exhaustion**;
    - if any required window (30-day, 20-day, 252-day) cannot be fully populated from sessions ≤ `t-1`, or a true SPY gap prevents it → **`indeterminate-state`** (retained in all grids, excluded from narrative/hypothesis formation; counted in the sparsity report).

No tuning, no optimization, no post-hoc threshold change at any step. Thresholds (`> 0`, `≥ 75%`), windows (30/20/252), and the state map are fixed by the design memo and are not parameters here.

## 4. Grid construction

Exactly the design memo §9 grids. All cells reported; nothing curated. `indeterminate-state` is a first-class state column (displayed last).

- **Grid 1** — base-12 phase (0–11) × ns-state → event count.
- **Grid 2** — base-12 phase × ns-state → long percentage (`mean(is_long)` ×100).
- **Grid 3** — base-12 phase × ns-state → median `r_multiple`. (No fixed-horizon outcome — Decision 2.)
- **Grid 4** — state-level **PSS_12 vs PSS_10**: within each ns-state, the descriptive η² correlation ratio `between / total` of `is_long` on `phase_12` and on `phase_10`, reported side by side as plain numbers. **No null, no permutation, no threshold, no beat count, no verdict** — the η² *form* only (`between = Σ_p (N_p/N)·(share_p − share_pooled)²`, `total = share_pooled·(1 − share_pooled)`; degenerate `total = 0` in a state cell is reported as `NA`, never as a result).
- **Grid 5** — asset × base-12 phase × ns-state → event count and long percentage. Flagged as diagnostic; expected predominantly low-data (~5 trades/cell over 240 cells).
- **Grid 6** — long-only and short-only re-renders of Grids 1–3.
- **Grid 7** — sparsity report (§5).
- **Grid 8** — base-10 comparator views matching Grids 1–4 view-for-view, presented only as Candidate C's comparator, never as an additional search surface.

Each grid is emitted with companion per-cell `n` and a `low_data` boolean.

## 5. Sparsity handling

- Any cell with `n < 20` → `low_data = True`.
- Low-data cells are **still reported** in every grid (full grid always emitted).
- Low-data cells (and `indeterminate-state` cells) are **excluded from the descriptive narrative and from candidate-hypothesis formation**.
- **Table marker.** In CSV/table form, each cell carries columns `value`, `n`, `low_data` (boolean), plus a `marker` column whose value is `LOW_DATA` when `n < 20` and empty otherwise. `indeterminate-state` rows additionally carry `state = indeterminate-state`.
- **Heatmap marker.** Low-data cells are overlaid with a hatch pattern and the cell's `n` printed in-cell; `indeterminate-state` column is rendered with a distinct neutral border and labeled. A legend entry documents the hatch as "n < 20, excluded from narrative".
- **Sparsity report (Grid 7).** Per grid: total cells, count of cells with `n < 20`, fraction of total events in below-threshold cells, and the `indeterminate-state` trade count. Reported for Grids 1–6 and 8.

## 6. Visualization rules (fixed before generation)

- Base-12 phase axis ordered chronologically 1→12 (0→11). No clustering, no similarity reordering.
- Nervous-state order, always: **calm bull, manic / unstable rally, panic / crisis, quiet bearish / exhaustion, indeterminate** (indeterminate last, visually distinct).
- Asset order, always: **SPY, EFA, EEM, GLD, TLT**.
- Single shared color scale with consistent bounds across comparable heatmaps (one bound for all long-% maps; one for all η² maps; one for all median-`r_multiple` maps). No scale tuned to emphasize a pattern.
- Neutral/default plotting style; no emphasis annotation beyond the mandated low-data hatch and counts.
- Every heatmap either prints per-cell counts or ships paired with a per-cell count table.
- Low-data and `indeterminate-state` cells visually marked on every figure.

## 7. Output artifacts (paths proposed; not created yet)

```
results/human_field_base12_pullback_atlas_tables_<timestamp>/        # one CSV per grid (Grids 1–8 + sparsity)
results/human_field_base12_pullback_atlas_heatmaps_<timestamp>/      # one figure per heatmap grid
results/human_field_base12_pullback_atlas_summary_<timestamp>.md     # descriptive summary (permitted language only)
results/human_field_base12_pullback_atlas_metadata_<timestamp>.json  # provenance + mode metadata (§8)
docs/human_field_base12_pullback_atlas_closure_memo_v0.1.md          # closure memo draft (carries §15 sealed-data statements)
```

`<timestamp>` is the run start in UTC, format `YYYYMMDD_HHMMSS`. Nothing in this list is created until a run is explicitly authorized.

## 8. Metadata (recorded in the metadata JSON)

- `design_memo_path`: `docs/human_field_base12_pullback_atlas_design_memo_v0.1.md`
- `candidate_c_references`: design memo `401ce45`, lock-acceptance `dc97576`, verdict log `a19b2e9` (`results/candidate_c_results_20260515_051236_f3a6bf48.{json,md}`), closure `1659819`; phase-label source `src/candidate_c_lens.py::assign_annual_sector_phase`
- `freeze_manifest`: `docs/pullback_population_freeze_manifest_v0.1.md` @ `5225bfd`, with the five per-file SHA-256 digests verified at load
- `spy_artifact`: `data/raw/spy_yahoo_v8_19930129_20241231_e8fc0357…csv` @ `ed199bd`
- `date_range_used`: pullback events `entry_date` ∈ [2005-02-04, 2022-12-21]; SPY series truncated to `date ≤ 2022-12-21`
- `no_post_2022_rows_used`: `true` — explicit statement that no row dated after 2022-12-21 entered any calculation
- `atlas_mode`: `"exploratory / no-verdict"`
- `oos`: `"no OOS analysis performed; coverage inspected only to verify availability"`
- `confirmation_claim`: `"none"`
- `seeds`: `none (no permutation/null/resampling)`
- per-grid digests (SHA-256 of each emitted CSV) for reproducibility

## 9. Tests / checks before any run

All checks below must pass; any failure aborts before output is written.

1. **Substrate row count** — pooled loaded rows == 1,282.
2. **Per-asset counts** — SPY 243, EFA 283, EEM 261, GLD 253, TLT 242, matching the freeze manifest.
3. **Manifest digests** — each Phase 3b CSV SHA-256 matches `5225bfd` manifest.
4. **No event beyond bound** — `max(entry_date) ≤ 2022-12-21` across all loaded trades.
5. **SPY OOS guard** — after truncation, `max(spy.date) ≤ 2022-12-21`; assertion aborts on violation.
6. **No future SPY row used** — for every trade, every window's last session ≤ `t-1 < entry_date`; spot-invariant asserted in the feature builder.
7. **Phase completeness** — every trade has integer `phase_12 ∈ 0..11` and `phase_10 ∈ 0..9`; no missing/NaN; no `PhaseRangeError`.
8. **State completeness** — every trade has a state in {calm bull, manic/unstable rally, panic/crisis, quiet bearish/exhaustion, indeterminate-state}; no nulls.
9. **All grids generated** — Grids 1–8 plus sparsity report all present.
10. **Cell annotation** — every cell in every grid carries `n` and a `low_data` flag.
11. **Full grid, not subset** — emitted cell count per grid equals the full cartesian cell count for that grid's axes (including empty and low-data cells); no curation.
12. **SPY loader contract** — `load_spy()` returns the documented columns and the artifact SHA-256 matches the frozen stem.

## 10. Stop condition

This implementation plan does not authorize code, data loading, atlas generation, or OOS access. The next gate is explicit authorization to implement the plan.

---

## Appendix — Implementation questions (all resolved)

**Resolution status:** Q1–Q8 below were reviewed and accepted as documented at
the implementation-draft gate. The realized-volatility standard-deviation
convention is locked to `ddof=1` (see §3 step 9 and design memo §8.2). No
implementation question for Atlas v0.1 remains open. The text below is retained
for the audit trail with each item's accepted resolution.

These were surfaced for the planning gate and are now resolved:

1. **Realized-vol percentile reference window definition.** The plan computes a daily realized-vol series, then takes the percentile of today's realized-vol within the trailing 252 *daily realized-vol values* ending at `t-1`. An alternative reading is "percentile within 252 returns." The plan commits to the realized-vol-series reading; confirm this matches intent before implementation.
2. **Percentile estimator convention.** Rank method (e.g., `≤`-rank fraction vs interpolated percentile) at the 75% cut is unspecified in the design memo. Propose: fraction of trailing-window values strictly `<` current value (a deterministic, tie-stable rule), fixed before run. Confirm.
3. **Trading-day vs calendar-day windows.** Windows are specified in *trading days* and will be counted as sessions present in the truncated SPY frame (not calendar days). This is the assumed reading; confirm.
4. **`direction` encoding in the frozen CSVs.** Exact string domain of the `direction` column (e.g., `long`/`short` vs `1`/`-1`) is not verified in this plan (no data loaded for analysis). The loader will assert the observed domain against an expected set and abort on anything unexpected, rather than silently coercing.
5. **Empty / degenerate η² state cells (Grid 4).** A state with all-long or all-short trades makes `total = 0`. The plan reports such cells as `NA` (not 0, not a result). Confirm `NA` over alternatives.
6. **Median `r_multiple` tie/even-n convention.** Standard median (mean of two central values for even `n`). Confirm acceptable, or specify a no-interpolation order-statistic rule.
7. **Closure-memo timing.** The closure memo draft is listed as an output of the run, but the design memo requires the four sealed-data statements be fixed before generation. Proposal: author the closure memo's fixed boilerplate (the §15 statements) at implementation time and populate only descriptive, non-verdict observations post-run. Confirm.
8. **`<timestamp>` source.** UTC run-start; confirm format `YYYYMMDD_HHMMSS` and that a single timestamp is shared across all artifacts of one run.

— end of implementation plan —
