# Human Field × Base-12 Pullback Atlas v0.1 — Run Provenance (20260517_201553)

**Artifact type:** Run provenance memo (exploratory atlas record)
**Status:** Records a completed exploratory atlas run. No rerun, no
reinterpretation, no candidate hypotheses, no memory update.

---

## 1. Run identity

- **Atlas:** Human Field × Base-12 Pullback Atlas v0.1
- **Run timestamp (UTC):** 20260517_201553
- **Design/implementation commit before run:** `8493c951b877b266c937bd498c11a9a1fc572794`
- **Output locations:**
  - `results/human_field_base12_pullback_atlas_tables_20260517_201553/`
  - `results/human_field_base12_pullback_atlas_heatmaps_20260517_201553/`
  - `results/human_field_base12_pullback_atlas_metadata_20260517_201553.json`
  - `results/human_field_base12_pullback_atlas_summary_20260517_201553.md`
  - `docs/human_field_base12_pullback_atlas_closure_memo_v0.1.md`

## 2. Run status

- `methodological_status = ok`
- `row_count = 1,282`
- Asset counts: SPY 243, EFA 283, EEM 261, GLD 253, TLT 242
- `indeterminate_count = 0`
- `post_2022_rows_used_in_computation = false`
- No p-values, permutations, beat counts, or verdicts were produced.
- `candidate_hypotheses_generated = []`
- Lane 2 Attention-Spike Market Response study not included.
- Memory not updated.
- No result commit occurred before this provenance step.

## 3. Runner provenance

- The computation module `src/human_field_base12_pullback_atlas.py` was
  **byte-identical** to commit `8493c951b877b266c937bd498c11a9a1fc572794`
  at run time (`git diff --stat` against that commit was empty).
- The runner `scripts/run_human_field_base12_pullback_atlas.py` was **not
  byte-identical** to that commit at run time.
- The runner carried an **authorized emission-gate / output-writing
  extension** (the explicitly authorized "next gate"): guard flip
  (`CANONICAL_RUN_AUTHORIZED True`), `--authorize-canonical-run` mechanism,
  and descriptive artifact writers (CSV tables, heatmaps, metadata JSON,
  summary, closure memo).
- The runner diff was classified **A — emission/authorization/output-writing
  only, with computation unchanged**.
- **Every computed value originated from functions in the byte-identical
  committed computation module** (`atlas.build_spy_frame`,
  `atlas.build_events`, `atlas.preflight`, `atlas.grid1..grid8`,
  `atlas.grid7_sparsity_report`, `atlas.build_metadata`).
- The runner diff **did not change** any of: input files, row filtering,
  phase labels, base-12/base-10 logic, valence construction,
  realized-volatility construction, nervous-system state assignment,
  PSS/η² calculation, grid construction, sparsity logic, low-data handling,
  candidate-hypothesis formation, p-values/permutations/verdict machinery,
  or Lane 2 inclusion.

## 4. Known audit gaps / fidelity gaps

**Gap 1 — Runner not committed before run.** The runner used for artifact
emission was uncommitted at run time. This is addressed by committing it with
the run artifacts in this provenance step.

**Gap 2 — Runner SystemExit behavior changed.** The committed pre-run runner
would abort before emission if `methodological_status != ok`. The run-time
runner emits artifacts while recording status. This had **no effect on this
run** because `methodological_status = ok`, but it is a behavioral deviation
and is recorded here.

**Gap 3 — Metadata JSON omissions.** The metadata JSON lacks a commit-hash
field and does not record the uncommitted runner extension. The commit hash
appears in the summary and closure memo, not in the JSON.

**Gap 4 — Sparsity report coverage.** The sparsity report covers six grid
surfaces rather than the full planned Grids 1–6 and 8 coverage. Grid6
long/short splits and grid8 `median_r` / `state_pss` are absent from the
sparsity report. This is a plan-fidelity gap, not a computation-affecting
error.

**Gap 5 — Redundant grid8 state PSS file.** `grid8_base10_state_pss.csv`
duplicates `grid4_state_pss.csv` (the base-10 view reuses the combined
state-PSS table, which already carries PSS_12 and PSS_10). This is a cosmetic
redundancy, not a computation or discipline error.

## 5. Boundary status

None of the five gaps are computation-affecting, and none are
boundary-language violations. The computed atlas values are exactly those
produced by the byte-identical committed computation module.

## 6. Sparsity reality

- Grid1/2/3: 60 cells, 41 low-data, 23.5% of events in low-data cells.
- Grid5: 300 cells, 296 low-data, 93.4% of events in low-data cells.
- Grid8 base-10 count / long%: 50 cells, 29 low-data, 15.4% of events in
  low-data cells.
- Candidate-hypothesis formation was deliberately deferred.
- Low-data cells (n < 20) remain excluded from candidate-hypothesis formation.

## 7. Interpretation boundary

- This atlas is **exploratory only**.
- It validates **no hypothesis**.
- It produces **no verdict**.
- It confirms **no** base-12, influential-numbers, consciousness, or
  market-field claim.
- It does **not** rescue or reinterpret any prior null.
- Candidate H0 / no coherent joint structure remains an **equal-weight**
  outcome.
- Any future candidate hypothesis requires a **separate review step and
  fresh-data confirmation**.

— end of run provenance memo —
