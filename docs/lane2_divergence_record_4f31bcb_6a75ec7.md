# Lane 2 — Divergence Record: Ungated Market-Data Acquisition and Next-Session-Return Join

**Document type:** Divergence record (incident documentation).
**This is NOT a conformance certification.** It documents a gate that was skipped, records what was nonetheless verified after the fact, and fixes the resulting evidentiary status. It does not retroactively certify that the §10 gate passed, because the §10 gate did not run.

| Field | Value |
|---|---|
| Date of record | 2026-06-01 |
| Commits covered | `4f31bcb` (SPY acquisition + next-session-return join), `6a75ec7` (exploration scripts, current HEAD) |
| Governing design memos | `df9089b` (market-data join design memo), `21c87c1` (market-data acquisition design memo) |
| Prior recorded HEAD | `cb1122a` (Step 2 daily feature tracking) |
| Resulting status | **EXPLORATORY-ONLY** |
| 2023+ OOS seal | Intact — never read |

---

## 1. Scope

This record covers the post-`cb1122a` arc that executed, in two commits of "plain scripts," three steps that the prior project record tracked as unopened gates: (a) market-data acquisition execution, (b) join implementation/execution, and (c) instrument/outcome construction (the next-session-return join).

Artifacts in scope:
- `results/lane2_market_data_acquisition/20260531T224518Z/market_daily_spy.csv` (committed in `4f31bcb`)
- `results/lane2_join/gdelt_spy_nextday.csv` (present on disk, **untracked**)
- Exploration scripts committed in `6a75ec7` (raw scan → confound probe → detrended confirmation; print-only, no committed result artifacts)

> **Confirm against repo before committing this record:** all short hashes above, the acquisition row count (audit reported 2458 data rows), the date range (2013-04-01 → 2022-12-30), and the exploration ρ range (audit reported ≈ −0.15 to −0.18). Replace any value this memo cannot independently anchor.

## 2. The divergence — design vs. execution

The design memos `df9089b` and `21c87c1` specified a §10 gate and a set of per-execution conformance deliverables. The execution produced none of them and ran with no authorization guard.

| Required by design memo | Produced by execution |
|---|---|
| §10 conformance gate (review-then-execute) | Not run |
| Pre-execution conformance verdict | Absent |
| Boundary-declaration block | Absent |
| Per-execution manifest / `metadata.json` | Absent |
| Frozen-SHA record of acquired data | Absent |
| Execution-authorization guard (cf. `STEP2_EXECUTION_AUTHORIZED`, restored in `finally`) | None present in any of the 6 scripts (grep-confirmed) |

Plain statement: **the design was gated; the execution was not.** The acquisition step — previously characterized as the first irreversible market-data step requiring its own review — went straight to a committed CSV.

## 3. Post-hoc verification (what was checked after the fact)

These checks were performed during the read-only audit on 2026-06-01. They are recorded as post-hoc verification. They are **not** a substitute for the gate that should have preceded execution, and they do not change the status in §5.

Acquisition (`market_daily_spy.csv`):
- Window 2013-04-01 → 2022-12-30, SPY only, exact 12-column frozen schema.
- 2023+ seal honored: `END="2022-12-31"` inclusive; yfinance end is exclusive; `assert market_date.max() <= END`.
- Defensive asserts present: all-SPY, no duplicates, sorted, exact 12 columns, no forbidden return/outcome columns.
- Note: the audit's initial `grep 2023` hit was a red herring — every row carries `source_retrieved_at_utc = 2026-05-31…`, which is acquisition metadata, not a data date.

Join (`gdelt_spy_nextday.csv`):
- 72 columns = 69 GDELT features + `feature_info_date` + `outcome_session_date` + `next_session_return` (the market-derived outcome).
- No-lookahead: outcome session strictly after `feature_info_date` (= `civil_date` + 1, honoring `rows_from_offset_plus_1`), enforced by a hard `sys.exit` leakage check.
- Seal honored in the join: SPY 2023+ rows refused; the sealed December-2022 tail (`civil_date` 2022-12-30 / 2022-12-31) correctly yields an empty `next_session_return` because the outcome session would land in 2023.
- Independent `searchsorted` cross-check matched to 0.0 max absolute difference.

Conclusion of §3: the data boundaries that would have been fatal were honored. The 2023+ holdout was never read. The breach is governance, not contamination.

## 4. Substantive result (recorded as exploratory)

The exploration arc (`6a75ec7`) ran a wide Spearman scan, then a confound probe (partial-time + detrend + per-year), then a detrended scan.

- Raw scan: `|next_session_return|` correlates with GDELT volume/coverage features at ρ ≈ −0.15 to −0.18 (confirm range against repo).
- Confound control: the association dissolves under drift removal; attributed to slow trend/regime drift.
- Result: **clean exploratory NULL** — no clear next-session SPY direction or magnitude relationship after removing drift.

Forward implication (motivation only, not authorization): the volume-only attention signal is null once regime drift is controlled. If discriminating information exists, it is more likely to live in *what kind* of news rather than *how much* — i.e. in the event-type, tone, and impact fields of the Event Database (`EventCode` / `QuadClass` / `GoldsteinScale` / `AvgTone`) rather than in raw volume/coverage counts. This is the first empirical motivation for a type/tone/impact-weighted extraction, to be pursued only as a future, separately-gated design.

## 5. Resulting status and consequences

- **Status: EXPLORATORY-ONLY.** The analytic path (raw scan → confound probe → detrended confirmation) was not pre-registered. With no pre-commitment of features, test, drift-removal method, or null threshold, this cannot be elevated above first-pass exploration regardless of the clean boundaries in §3.
- **In-sample window 2013–2022 is exploration-spent.** It has been looked at; any later in-sample "confirmation" of this relationship would be circular.
- **OOS 2023+ — closed but openable.** The 2013–2022 volume-only result is exploratory-spent. A confirmatory 2023+ test remains theoretically available because the seal held, but it should only be opened if a future pre-registration gives a strong reason to spend the holdout on this exact question.

This record does not retire the volume-only question permanently. It does decline to spend the holdout on it casually. In practice the better-motivated future direction is type/tone/Goldstein-weighted news (see §4), but that judgment is recorded as a direction, not as a prohibition on ever revisiting the raw-volume question under a properly gated pre-registration.

## 6. Remediation (bounded — no re-runs, no reverts)

**Commit scope for this step is narrow and evidentiary: this divergence record only.** No `.gitignore` edit, no re-run, no revert, and no other file change is part of this commit unless separately and explicitly authorized.

1. Compute and record the SHA-256 of `market_daily_spy.csv`. Record it as computed post-hoc on 2026-06-01 — explicitly **not** backdated and **not** representing a pre-execution freeze. `8a87fc0536b24d013272f1ae841d9d8881fe203e16bf84a96b2ae6ce2f6cd5a1`
2. Commit this divergence record to the repo evidentiary chain (suggested: alongside the other Lane 2 memos), not only to agent memory. A divergence of this weight belongs in the committed record.
3. **Untracked-artifact policy (decided).**
   - `gdelt_spy_nextday.csv` remains untracked by policy as a regenerable derived outcome table. Its existence, path, schema, and post-hoc SHA may be recorded here for transparency, but it is not elevated into a canonical committed result artifact. Future derived outcome tables follow the same rule unless a future pre-registered gate explicitly authorizes commit-with-SHA treatment.
   - The F4 feasibility output and other historical/intermediate dirs are **not** retro-committed. Committed canonical artifacts stay committed; untracked historical/intermediate artifacts stay untracked. This record pins their paths, status, and post-hoc hashes where material (ledger below).
   - Making this non-accidental — i.e. adding explicit `.gitignore` patterns so the untracked state is by policy rather than by omission — is a **separate, later step**, not part of this commit.

   Artifact ledger (Claude Code to populate during read-only verification; record post-hoc SHA only where material):

   | Path | Tracked? | Status | Post-hoc SHA-256 (2026-06-01) |
   |---|---|---|---|
   | `results/lane2_market_data_acquisition/20260531T224518Z/market_daily_spy.csv` | committed (`4f31bcb`) | canonical input | `8a87fc0536b24d013272f1ae841d9d8881fe203e16bf84a96b2ae6ce2f6cd5a1` |
   | `results/lane2_join/gdelt_spy_nextday.csv` | untracked (by policy) | regenerable derived outcome | n/a (untracked; SHA not computed this pass — step 5 verified tracking status only) |
   | `results/lane2_gdelt1_count_feasibility/20260518T163302Z/` | untracked | historical (F4-missing) | hashes run-metadata, not data: `count_feasibility_metadata.json` = `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d`; `feasibility_summary.md` = `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c` |
   | other intermediate dirs | untracked | historical/intermediate | n/a (not hashed this pass) |

4. Restore an execution-authorization guard (analogue of `STEP2_EXECUTION_AUTHORIZED`, set explicitly and restored in `finally`) as a precondition for the next irreversible step. This arc avoided harm by luck, not by control.

## 7. What this record does NOT authorize

- No in-sample confirmatory reinterpretation of the §4 NULL.
- No unsealing of, or read against, 2023+ data.
- No fresh acquisition, build, or type/tone/impact-weighted extraction without a new design memo and its own gate.
- No backdating of the SHA or any artifact to imply pre-execution conformance.

---

*Filed as a divergence record. The next forward artifact is the narrow evidentiary commit of this record (per §6), not a re-run, a revert, or a `.gitignore` change.*
