# Pullback Population Freeze Manifest v0.1

**Freeze date:** 2026-05-14
**Destination repo:** `/Users/jay/Documents/GitHub/coherent-numbers`
**Source repo:** `/Users/jay/pullback_research`
**Source repo HEAD at freeze time:** `eac925cf71cd6c4978c19e6a0d76c3966d6cc7e2` (`eac925c`, "Add Phase 8 continuation decision memo (A vs B vs C, no option selected)", 2026-05-11)
**Source repo working tree at freeze time:** clean (verified both before and after copy).

## Source commit references

| Commit | Role |
|---|---|
| `50ee2d1` | Phase 2 close — introduces `src/backtest.py` and `run_base.py`; locks `BacktestParams`; unchanged in all subsequent pullback phases |
| `7806a6d` | Run Phase 3b base system on all five assets — produces the five Phase 3b populations under identical `BacktestParams` defaults on the common 2005-01-01 – 2022-12-31 window |
| `665a557` | Add Phase 3b summary to research log — records the directional / long-short allocation finding (directional random baselines did not pass on any asset; the primary edge appeared at the long/short allocation level vs a 50/50 random baseline) |
| `eac925c` | Pullback repo HEAD observed during inventory and at freeze time |

## Statements of scope

- **The pullback repo was not modified.** No commits, edits, runs, or exports were written back into `/Users/jay/pullback_research`. Source `git status --short` was empty before and after the copy; source HEAD did not change.
- **This is a frozen imported data substrate**, not an analysis result. The CSVs in `data/raw/` are byte-identical copies of the existing pullback `trades.csv` artifacts referenced by the pullback research log and metadata.
- **No harmonic-calendar features were computed.** No phase mapping, no anchor, no boundary calculation, no leap-year adjustment, no time-zone normalization.
- **No `entry_date` to calendar-phase join was performed.** The imported CSVs contain only the columns already present in the source files.
- **No derived columns were added.** No row was filtered, sorted, renamed, or recoded.
- **OOS 2023+ remains untouched.** Every imported row's `entry_date` and `exit_date` is on or before 2022-12-30. The pullback repo's hard-erroring OOS loaders were not invoked. No 2023+ data was created, copied, or accessed.

## Imported populations

Six CSVs imported. All hashes computed via `shasum -a 256`. Source/destination hashes match exactly for all six files (byte-preserving `cp`).

| Label | Source path (relative to source repo root) | Destination path (relative to this repo root) | Rows (excl. header) | First entry_date | Last entry_date | Source SHA256 | Destination SHA256 | Match |
|---|---|---|---:|---|---|---|---|---|
| SPY base (Phase 1/2/3a, 2000–2022) | `runs/20260505_152451/trades.csv` | `data/raw/pullback_spy_base_301_trades_2000_2022.csv` | 301 | 2000-03-21 | 2022-10-19 | `b7817e0e7a02dad44923eae462c1454ab67b8fbc73539b36b81e043d8dcc2d06` | `b7817e0e7a02dad44923eae462c1454ab67b8fbc73539b36b81e043d8dcc2d06` | ✓ |
| Phase 3b SPY (2005–2022) | `runs/phase3b_SPY_20260506_200016/trades.csv` | `data/raw/pullback_phase3b_spy_trades_2005_2022.csv` | 243 | 2005-03-11 | 2022-10-19 | `1d8a7b77389835a7231d6ca0742e39d963cf4dc03f822b0111039b5c19383621` | `1d8a7b77389835a7231d6ca0742e39d963cf4dc03f822b0111039b5c19383621` | ✓ |
| Phase 3b EFA (2005–2022) | `runs/phase3b_EFA_20260506_200307/trades.csv` | `data/raw/pullback_phase3b_efa_trades_2005_2022.csv` | 283 | 2005-02-17 | 2022-12-08 | `275af7e00f28a2a72d948228964c7a4658444f0030ac048e8a2851bc3313de82` | `275af7e00f28a2a72d948228964c7a4658444f0030ac048e8a2851bc3313de82` | ✓ |
| Phase 3b EEM (2005–2022) | `runs/phase3b_EEM_20260506_200622/trades.csv` | `data/raw/pullback_phase3b_eem_trades_2005_2022.csv` | 261 | 2005-03-21 | 2022-12-08 | `56cf8e5fe88f5230ebb8e2881f4df1e0ff633819d588764d9e9e57bbdebb6916` | `56cf8e5fe88f5230ebb8e2881f4df1e0ff633819d588764d9e9e57bbdebb6916` | ✓ |
| Phase 3b GLD (2005–2022) | `runs/phase3b_GLD_20260506_200921/trades.csv` | `data/raw/pullback_phase3b_gld_trades_2005_2022.csv` | 253 | 2005-02-25 | 2022-12-16 | `0de7bf6dd981be8d8091a382a6dc0af594a59fa8d87f459305ad25f9dc21d1e3` | `0de7bf6dd981be8d8091a382a6dc0af594a59fa8d87f459305ad25f9dc21d1e3` | ✓ |
| Phase 3b TLT (2005–2022) | `runs/phase3b_TLT_20260506_201216/trades.csv` | `data/raw/pullback_phase3b_tlt_trades_2005_2022.csv` | 242 | 2005-02-04 | 2022-12-15 | `037ea4178bd071e426d7cce30eeaffb554ae31d7998c8d00d5e2ba36a7388abc` | `037ea4178bd071e426d7cce30eeaffb554ae31d7998c8d00d5e2ba36a7388abc` | ✓ |

### Schema note

- **SPY base** uses the 21-column long-form trade schema: `direction, entry_date, entry_price, initial_stop, initial_risk, shares_total, shares_remaining, first_target, current_stop, setup_date, is_free_bar_trigger, first_target_hit, highest_high, lowest_low, bars_held, realized_pnl, exit_date, exit_price_final, exit_reason, r_multiple, is_closed`.
- **All five Phase 3b populations** use the 11-column compact schema: `entry_date, setup_date, direction, entry_price, exit_price, exit_date, exit_reason, bars_held, r_multiple, first_target_hit, initial_risk`.

A reconciled common schema is **not** defined here. Schema reconciliation is an open question for the Candidate B design memo.

### OOS sanity check (per-file max date across `entry_date` and `exit_date`)

| Label | Max observed date | Bound |
|---|---|---|
| SPY base | 2022-11-01 | ≤ 2022-12-31 ✓ |
| Phase 3b SPY | 2022-11-01 | ≤ 2022-12-31 ✓ |
| Phase 3b EFA | 2022-12-21 | ≤ 2022-12-31 ✓ |
| Phase 3b EEM | 2022-12-21 | ≤ 2022-12-31 ✓ |
| Phase 3b GLD | 2022-12-30 | ≤ 2022-12-31 ✓ |
| Phase 3b TLT | 2022-12-21 | ≤ 2022-12-31 ✓ |

## Twin-hash advisory (SPY base population)

A second pullback run at `runs/20260505_151635/trades.csv` produces the same 301-trade SPY population but writes a different file SHA256 (different in-memory representation of the same underlying data). The pullback `research_log.md` declares `runs/20260505_152451/` canonical (with underlying CSV `data_hash` `d170f6752cd1d8be`). This freeze imports the canonical artifact only; the twin is **not** imported. The Candidate B design memo may document the twin's existence as a footnote if needed.

## Data-contact disclosure

The imported pullback populations were produced by prior pullback research Phases 1–3b. They are **audit-frozen** but **not pristine**. The underlying SPY 2000–2022 series and the Phase 3b 2005–2022 series for SPY/EFA/EEM/GLD/TLT were inspected, partitioned, and used to estimate within-population statistics during pullback research. The pullback `BacktestParams` were locked early at `50ee2d1` and were not re-tuned, which limits but does not eliminate this exposure. Any future Candidate B verdict must be interpreted as conditional on this previously contacted pullback-event population. This disclosure is a required precondition that must be carried forward into the Candidate B design memo and into B's verdict.

## What this commit does NOT do

- It does not authorize Candidate B analysis.
- It does not lock Candidate B's design (population scope, schema reconciliation, calendar lens, pooling, comparator, success criterion, controls remain open).
- It does not compute or join any harmonic-calendar feature against `entry_date`.
- It does not modify or push to the pullback repo.
- It does not breach the OOS 2023+ seal in either repo.
