# Coherent-Numbers Research Memory — Anchored State Index

**Status: LIVING STATE INDEX**
**Repo: /Users/jay/Documents/GitHub/coherent-numbers**
**Branch at creation: main**
**Last updated: 2026-06-12**
**Last reconciled against commit: ac098b660cabdc04aafff54aec7356ab55b143f4**
**Purpose: map to authoritative committed records (Lane 2 / TTG closure); not a replacement for preregs, result docs, decision memos, research logs, result reports, or closure memos**
**Value-safety: no raw data, no row-level data, no OHLC rows, no returns rows, no source URLs, no secrets, no 2023+ data filenames/rows, no execution authorization, no OOS authorization**
**Bootstrap rule: future sessions must read this file first, then verify every cited commit/path against git before relying on it**

---

## 0. How to use this file

- This file is an **index, not the source of truth**. The source of truth is the **committed record cited by each entry** (preregs, result docs, decision memos, closure memos).
- Future sessions **must read this file first, then verify anchors against git** (see §1) before trusting any statement here.
- If this file conflicts with a cited committed memo/doc, **the committed record controls and this file is stale**. Reconcile by updating this file, never by overriding the committed record.
- Full 40-character commit hashes only; no short hashes.

## 1. Reconciliation protocol

Run at the start of any session that intends to rely on this file:

1. Verify repo path and branch (`pwd`; `git branch --show-current`) against the status block.
2. Verify the last-reconciled commit resolves (`git cat-file -t 4ce9bf3df4ff2ed1847cebf74b185a10bd859944`).
3. For every anchor in §10: `git cat-file -t <sha>` resolves to a commit.
4. For every cited path: confirm it exists at the cited commit (`git cat-file -e <sha>:<path>`).
5. For every "introduced" claim: verify with `git show --name-status --diff-filter=A <sha> -- <path>` showing `A`.
6. Check whether `HEAD` is newer than the last-reconciled commit (`git log --oneline 4ce9bf3df4ff2ed1847cebf74b185a10bd859944..HEAD`).
7. Inspect any commits after the last-reconciled anchor. If **substantive research commits** exist beyond it, **mark this file stale** and reconcile against the committed records before relying on the "current state" sections.
8. **Exception:** the ledger's own creation commit being exactly one commit beyond the reconciled anchor is **not** stale drift **if** that commit adds only `docs/research_memory.md`.
9. If any anchor or path fails verification, mark this file stale and fall back to git history + the cited committed docs as the authority.

## 2. Current canonical state

- `coherent-numbers` on `main`.
- **TTG (Type/Tone/Goldstein) Lane 2 is closed on origin/main at `4ce9bf3df4ff2ed1847cebf74b185a10bd859944`** (`Lane 2: close TTG magnitude-pressure spend decision`).
- **No active TTG continuation** is open (no screen run, no prereg, no V2).
- **2023+ seal untouched.**
- **No V2 authorized.**
- **No base-12 conclusion drawn from TTG.**
- Local creation of this ledger will make `main` **one commit ahead of `origin/main`** until pushed. **Do not push.** A remote (`origin`) is configured; the ahead state is expected and local-only.

> The stable anchors in this file are the introducing/governing commits in §10, not the moving HEAD pointer.

## 3. Closed / terminal lanes

### TTG → SPY directional v1 — closed weak/null

- **Status:** closed; terminal scientific outcome **weak / null**.
- **Holdout AUC ≈ `0.5266`** (primary metric); **primary block-bootstrap p ≈ `0.166`** (one-sided AUC > 0.5).
- `statistical_confirmed` (AUC > 0.5 AND p ≤ 0.05) = **False**.
- Holdout **accuracy below majority baseline** (~0.4960 vs ~0.5079).
- **Negative sign-rule Sharpe** (annualized ≈ −0.10).
- **Single in-sample read spent** (holdout touched once); recorded as-is, no adjustment.
- **No V2 authorized.**
- **No base-12 inference** from TTG→SPY.
- **No "negative news makes price go down" conclusion** is supported or drawn.
- Anchor: `docs/lane2_ttg_spy_v1_results_v0.1.md` @ `2003fc855bd0583f137e8814c173485981540270`. Full row in §10.

### Cusp Geometry Lane v0.3 — closed exploratory null

- **Status:** closed; terminal scientific outcome **FAIL — exploratory null**.
- **Pre-registered sandbox gate** (SPY in-window sandbox 2005-01-01…2022-12-31, `adj_close`): does adding the living-line curvature statistic `F2_kappa_mean` to the M0 baseline (`const + B1_ln_rv63 + B2_ln_rv21 + B3_abs_ret21 + B4_range63 + B5_ac1_63 + B6_mean_abs_dz`) improve out-of-fold prediction of forward log realized vol? OLS over the frozen `purged_blocked_folds` (N_FOLDS=10, PURGE=3); 209 records from frozen `make_records`.
- **Pooled out-of-fold incremental R² = `-0.0256` (< 0)**; **improving folds = `0/10`**. PASS condition (incremental R² > 0 AND ≥7/10 improve) failed on both clauses.
- **Interpretation:** B6 (F2's linearized small-z shadow) and the standard volatility baselines absorb the curvature statistic; F2 adds nothing and degrades OOF prediction (fold-wise F2 coefficient sign unstable, 5 positive / 5 negative).
- **Protocol consequence:** lane closed per the **pre-registered FAIL branch**. **No tuning, no alternatives, no full-sandbox refit** were run. **2023+ sealed data remains unopened** (only the 2005–2022 in-window sandbox was read).
- **Instrument freeze commit:** `4536be27f6955be72bdb7abad4b4cb38ac1278ad` (memo SHA-256 `7d47f9a8a840984bc12a95933f377a73a853d59ad223403a095bc3a0b3d6d8e8`; code SHA-256 `bd2a9d46e7637fc2eede7ecd1584cedd9d7859cbca82d1e867ca84af90568014`). **Closure commit:** `ac098b660cabdc04aafff54aec7356ab55b143f4`.
- **Report:** `docs/cusp_geometry_lane_v0_3_sandbox_gate_report.md` SHA-256 `28d97171f902ec50b0ac945160fe7489ef06398e3c8d21a21ea7f289f28849a6`. **Derived sandbox CSV** SHA-256 `5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901` — **not committed** because `data/raw/` is gitignored (the gate is reproducible from the SHA-pinned source + committed loader).
- **Local branch:** `main` is **two commits ahead this session** (freeze → closure) and **unpushed**. Two unrelated untracked docs (`docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md`, `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`) were left untracked and untouched. Full rows in §10.

## 4. TTG magnitude-pressure closure

The magnitude-pressure question concerned **magnitude (size of price response), not direction.** Closed as a **no-spend terminal judgment** on the currently achievable 2023+ seal, dominated by MDE arithmetic (the external benchmark band is a soft prior, not locked). Per-horizon, as verified in the committed records:

- **Daily horizon (h=1): closed / nonviable.** Settled `OPTION_C_NONVIABLE_BEST_CASE_FAIL`; the confirmation MDE exceeds the expected effect (`rho_MDE ≥ ~0.088` vs `rho_expected ≈ 0.07`). The daily question remains closed.
- **Monthly horizon (h=21): nonviable / exploratory-only.** Confirmation MDE ≈ `0.43–0.45` with only ~38 monthly observations on the achievable seal; **not a prereg target.**
- **Weekly horizon (h=5): too marginal.** Confirmation MDE ≈ `0.20` under floor assumptions; **fails the viability inequality under floor discipline** (`rho_MDE >= rho_expected`); **borderline only under stacked optimism** (top-of-band expected effect **plus** favorable overlap efficiency).

Decision and disciplines (verified):

- **No 2023+ seal spend** for confirmation at **any** horizon.
- **No weekly prereg written.**
- **No screen lock** as a prereg-triggering design; screen memo v0.3 remains a **DRAFT**, unlocked, non-prereg-triggering.
- **2023+ seal remains untouched and unspent.**
- The **in-window screen (2013-01-01 … 2022-12-31)** is preserved only as **pure exploration, runnable only under separate explicit authorization** — no prereg pathway, no 2023+ contact. It is **not an active next step.**

Anchors: weekly spend decision (closure) `4ce9bf3df4ff2ed1847cebf74b185a10bd859944`; long-horizon benchmark/MDE note `abffe6eb7015e621f20aa0cc6d4779da8ed03865`; daily-horizon benchmark-limitation memo `c841f3c37762156038996460a420e537aa7cb8bb`; screen memo v0.3 (draft) `ddc5c92ed2588219b4c7a8700b611022b967cf35`. Full rows in §10.

## 5. Paused / preserved / gated items

- **TTG in-window exploratory screen** (2013-01-01 … 2022-12-31): **not authorized now.** May only run under **separate explicit authorization**; **must not trigger a prereg by itself**; no 2023+ contact.
- **Gate 5 diagnostic doc: not authorized to commit.**
- **Known local/untracked docs at creation** (not authoritative committed records; must remain untracked/unstaged):
  - `docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md`
  - `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`
  - These are recorded here as **local/untracked state only**, not as committed anchors.

## 6. 2023+ / OOS seal-state

- **2023+ / OOS remains sealed.**
- **No 2023+ acquisition / contact / probe is authorized.**
- **No outcome-free 2023+ coverage probe is authorized.**
- **No seal-spend, unsealing memo, or OOS-opening action exists** in this handoff or in the current committed state.
- 2023+ may be referenced **only as a sealed governance concept.**

## 7. Forbidden actions

- Do not reopen TTG.
- Do not run the TTG in-window exploratory screen without separate explicit authorization.
- Do not run TTG directional V2.
- Do not touch / acquire / contact / probe 2023+ without an explicit unsealing memo / authorization.
- Do not perform an outcome-free 2023+ coverage probe.
- Do not infer base-12 from TTG→SPY.
- Do not commit the Gate 5 diagnostic doc without explicit authorization.
- Do not read raw data.
- Do not execute project code / scripts / tests / notebooks / feature builders / archive readers / market loaders.
- Do not stage unrelated docs.
- Do not push.

## 8. Next safe moves

**Nothing here is automatically authorized.** Each move requires explicit initiation and a fresh git preflight.

- The next safe move after creation is a **read-only byte-review of `docs/research_memory.md`**.
- **No scientific continuation, screen, prereg, run, data read, or OOS action is automatically authorized** by this ledger.
- Any future action requires **explicit authorization** and a **fresh git preflight**.

## 9. (Reserved — see §10 for the authoritative-records table)

## 10. Authoritative records

All commits/paths below were resolved and confirmed against git at the last-reconciled commit; each "introduced" claim was verified with `git show --name-status --diff-filter=A`. Provenance: *committed-doc claim* = status/verdict asserted by the cited committed document (this index does not independently re-derive each verdict).

| Topic | Status | Provenance type | Path | Commit | Verification note |
| ----- | ------ | --------------- | ---- | ------ | ----------------- |
| TTG magnitude-pressure weekly spend decision (lane closure) | closed / no-spend terminal | committed-doc claim | `docs/lane2_ttg_magnitude_pressure_weekly_spend_decision_v0.1.md` | `4ce9bf3df4ff2ed1847cebf74b185a10bd859944` | introduced (A) verified; equals origin/main and last-reconciled anchor |
| TTG long-horizon benchmark / MDE note | committed | committed-doc claim | `docs/lane2_ttg_magnitude_pressure_long_horizon_benchmark_mde_note_v0.1.md` | `abffe6eb7015e621f20aa0cc6d4779da8ed03865` | introduced (A) verified; per-horizon confirmation-viability arithmetic |
| TTG magnitude-pressure benchmark-limitation memo (daily horizon) | committed | committed-doc claim | `docs/lane2_ttg_magnitude_pressure_predata_benchmark_limitation_memo_v0.1.md` | `c841f3c37762156038996460a420e537aa7cb8bb` | introduced (A) verified; daily settled OPTION_C_NONVIABLE_BEST_CASE_FAIL |
| TTG multi-horizon screen design v0.3 (DRAFT, weekly-centered) | committed; draft, not locked | committed-doc claim | `docs/lane2_ttg_magnitude_pressure_option_a_multi_horizon_screen_design_v0.3.md` | `ddc5c92ed2588219b4c7a8700b611022b967cf35` | introduced (A) verified; not a prereg-triggering artifact |
| TTG → SPY directional v1 results | closed weak/null | committed-doc claim | `docs/lane2_ttg_spy_v1_results_v0.1.md` | `2003fc855bd0583f137e8814c173485981540270` | introduced (A) verified; AUC≈0.5266, primary p≈0.166, statistical_confirmed=False |
| Cusp Geometry Lane v0.3 instrument freeze | frozen | committed-doc claim | `docs/cusp_geometry_lane_design_memo_v0_3.md` + `src/cusp_geometry_v0_3.py` | `4536be27f6955be72bdb7abad4b4cb38ac1278ad` | introduced (A) verified; memo SHA-256 `7d47f9a8…b3d6d8e8`, code SHA-256 `bd2a9d46…90568014`; smoke test PASS |
| Cusp Geometry Lane v0.3 sandbox null (closure) | closed / FAIL exploratory null | committed-doc claim | `docs/cusp_geometry_lane_v0_3_sandbox_gate_report.md` | `ac098b660cabdc04aafff54aec7356ab55b143f4` | introduced (A) verified; pooled incremental R²=`-0.0256`, 0/10 folds improve; report SHA-256 `28d97171…f28849a6`; derived sandbox CSV SHA-256 `5cd92502…ea5901` (not committed, `data/raw/` ignored); FAIL branch — no tuning/alternatives/refit; sealed data unopened |

Additional committed TTG→SPY directional v1 scaffolding exists in earlier commits (outcome-source pin, execution-environment note, zero-return amendment) and is reachable through git history; it is supporting, not load-bearing for this closure index, and is intentionally not enumerated as separate anchor rows. Verify directly from git if needed.

## 11. Update rules

- Update this file whenever a **verdict, closure, or major decision lands**.
- Update it in the **same commit as the decision when possible**.
- Keep it **terse, anchored, and value-safe**; cite full-hash introducing/governing commit + path, not live HEAD.
- **Nulls and methodological failures are first-class findings** (e.g., TTG directional v1 weak/null; magnitude-pressure no-spend closure) and must be recorded as such.
- Distinguish **"permitted if explicitly authorized"** from **"automatically do this."**
- If the ledger becomes stale, **mark it stale and reconcile against the committed records before relying on it**; then refresh `Last updated` and `Last reconciled against commit`.

## 12. Value-safety boundary

This file contains and authorizes none of the following:

- no raw data;
- no row-level data;
- no OHLC rows;
- no returns rows;
- no secrets;
- no source URLs;
- no 2023+ data filenames or rows;
- no execution authorization;
- no OOS authorization language.

2023+ / OOS is referenced in this file **only as a sealed governance concept.**

End of state index.
