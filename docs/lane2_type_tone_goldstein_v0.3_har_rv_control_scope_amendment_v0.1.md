# Lane 2 Type/Tone/Goldstein — v0.3 HAR-RV Control-Scope Amendment v0.1

*Design-only governing-spec amendment. Decided-by-argument inputs (RV/DAG decision, RV-control architecture decision) are cited as judgment sources, not byte-certified. This amendment artifact is what enters the byte-checkable correction → canary → external-byte-review cycle.*

## 1. Title and proposed path

**Title:** Lane 2 Type/Tone/Goldstein v0.3 HAR-RV at-join control-scope amendment (v0.1).
**Path:** `docs/lane2_type_tone_goldstein_v0.3_har_rv_control_scope_amendment_v0.1.md`

## 2. Scope

- **Design-only.** Amends the **at-join** primary controlled-association statistic; authorizes no data contact.
- Amends **at-join §7** primary statistic (adds two RV controls → k=6 at join).
- Amends **at-join §12** influence-gate control count / DOF references (inherits the 6-control at-join statistic).
- Updates **§10** control-count-dependent **at-join** references (Fisher-z SE, computability threshold, k).
- **Explicitly preserves §11 planted-signal fidelity as pre-join, outcome-free, and RV-free (k=4).**
- Does **not** authorize execution, extraction, the join, tests, V1/V2, market data, outcomes, `next_session_return` / `abs(next_session_return)`, real-data trailing RV, GDELT contact, or 2023+.
- Does **not** modify the five-field GDELT extraction allow-list (RV is price-derived at join, not a GDELT field).

**Load-bearing scope statement:** RV controls are **join-time, price-derived** quantities. They propagate to §7 / §12 / §10 *only where those sections operate at the join on real outcomes*. They do **not** propagate to §11, which is pre-join and outcome-free. Allowing RV into §11 would create an internal contradiction; this amendment forbids it.

## 3. Anchor references

| Role | Anchor |
|---|---|
| Governing v0.3 (lock-closure) | `c6aeb2b` |
| Phase 0.5 corrected amendment | `8fdf233` (supersedes `4fe1f0c`) |
| Phase 0.5 canary manifest | `294494a` + `c6aeb2b` + `3411db5` + `8fdf233` |
| RV/DAG decision memo | causal-judgment source (Decision A: RV is a pre-treatment volatility-state confounder / proxy) — argument-reviewed, not byte-certified |
| RV-control architecture decision memo | HAR-primary + horizon-set rationale source — argument-reviewed, not byte-certified |

## 4. Governing-source repoint (MANDATORY, load-bearing)

- This document is a **governing-spec amendment** to the v0.3 governing chain.
- For the **amended at-join §7 / §10 / §12 clauses**, the **source of truth** is repointed from `c6aeb2b` alone to:

  **`c6aeb2b` + this HAR-RV amendment commit.**

- Reading `c6aeb2b` **alone** for the amended at-join §7 / §10 / §12 clauses is **stale** and must be treated as **`STALE-SOURCE BLOCKED`** — not as a scientific or design BLOCK. (Without this repoint, a re-canary reads the old `c6aeb2b` 4-control at-join statistic and would mis-grade the k=6 structure — a stale-source false negative, not a real design gap.)
- This HAR-RV amendment **controls on conflict** for the amended at-join clauses:
  - the **at-join §7** primary statistic;
  - the **§10 at-join** control-count / Fisher-z / MDE-floor references;
  - the **§12 at-join** influence-gate control count / Fisher-z / computability references.
- `c6aeb2b` **remains the governing baseline everywhere else.**
- In particular, `c6aeb2b` **remains baseline for §11**, which this amendment explicitly leaves **pre-join, outcome-free, RV-free, k=4, `N_eff − 7`**.
- This repoint **does not replace `8fdf233`.** `8fdf233` **remains the Phase 0.5 corrected-amendment pin**; the new HAR-RV amendment commit becomes an **additional governing-spec amendment leg**, not a substitute for the Phase 0.5 leg.
- Consequence for the next canary manifest: it must be the **five-commit set** — governing chain `294494a` + `c6aeb2b` + this HAR-RV commit; Phase 0.5 corrected amendment `8fdf233`; v2.1 base `3411db5`.

## 5. Existing at-join §7 (summary of current locked state)

Current locked at-join primary = full-rank **simultaneous Spearman partial** of the news feature against `|return|_{t+1}` controlling **k=4**:
- rank-date,
- `log1p_total_row_count`,
- `roll_mean_log1p_total_w30`,
- `coverage_completeness`.

**No RV control currently included.**

## 6. Amended at-join §7 primary statistic

Same full-rank **simultaneous Spearman partial** structure; **add two simultaneous primary RV controls** → **k=6 at join**:
1. rank-date,
2. `log1p_total_row_count`,
3. `roll_mean_log1p_total_w30`,
4. `coverage_completeness`,
5. **`trailing_rv_5`**,
6. **`trailing_rv_22`**.

All six are conditioned **simultaneously** (no stepwise / sequential entry). `trailing_rv_60` and single-window variants are **not** primary (robustness only — see §13).

## 7. §10 / §12 control-count and DOF updates (at-join only)

Generic form: `SE_z = 1 / sqrt(N_eff − k − 3)`.

| Quantity | Old (k=4) | New at-join (k=6) |
|---|---|---|
| Control count `k` | 4 | **6** |
| Fisher-z SE | `1 / sqrt(N_eff − 7)` | **`1 / sqrt(N_eff − 9)`** |
| Computability threshold | `N_eff > 7` | **`N_eff > 9`** |

- **§10 MDE / effective-sample / Fisher-z quantities for the at-join primary** use k=6 (`N_eff − 9`); any at-join MDE floor that consumed `k=4` is recomputed at `k=6`. No old 4-control constants may remain in at-join logic.
- **§12 LOYO / leave-two influence gate** re-runs the at-join §7 statistic, so it **inherits the 6-control at-join structure**: each deletion subset recomputes its own realized `N_eff`, seam-safe `φ`, and per-subset MDE floor at **k=6**, and the approximate one-sided Fisher-z confidence-bound diagnostic uses **`SE_z = 1 / sqrt(N_eff − 9)`**.
- **Acknowledgement (stricter computability):** the `+2` controls raise the computability floor from `N_eff > 7` to `N_eff > 9`. Some §12 deletion subsets (especially leave-two on the smallest retained samples) may become **non-computable / BLOCKED** that were computable under k=4. This is expected and is handled by the existing degenerate → BLOCKED convention, not by silently reverting to k=4.

## 8. §11 planted-signal fidelity preservation (RV-free, pre-join, k=4)

- **§11 remains pre-join, outcome-free, and RV-free.** It keeps **k=4**: rank-date + the three volume/coverage controls only. It does **not** include `trailing_rv_5` or `trailing_rv_22`.
- **§11 retains its own constants:** the §11 fidelity statistic uses `k=4` and therefore does **not** inherit the at-join `N_eff − 9` / `N_eff > 9` rule; any §11 computability / SE quantity stays at the `k=4` form (`N_eff − 7`).
- **Rationale:** RV is computed *at the join* from the price series; §11 (planted-signal / fidelity diagnostic) executes *before* the join, where no price series and no outcome are available. Injecting RV into §11 is therefore impossible and forbidden.
- **This is not a contradiction:** the k=4 (§11) vs k=6 (§7 / §12 / §10 at-join) split is a **deliberate stage-specific control distinction** (pre-join vs at-join), not an inconsistency. The amendment states this explicitly so a canary does not flag the two control counts as conflicting.

## 9. Exact RV definitions

Primary controls: **`trailing_rv_5`**, **`trailing_rv_22`**.

**Estimator** (each horizon `h`): realized-volatility proxy = RMS of daily close-to-close log returns over the `h` most recent trading sessions:

```
trailing_rv_h = sqrt( (1/h) * sum_s r_s^2 ),   r_s = ln(close_s / close_{s-1})
```

using daily close-to-close returns from the market price series **at the join**. These are **daily-return realized-volatility proxies, not intraday realized volatility** (the price series is daily OHLCV) — stated explicitly, since it bounds how finely short-horizon volatility is resolved.

**Source:** computed at the join from the price series. **Not a GDELT field** — RV is not extracted and does **not** modify the five-field GDELT allow-list (`civil_date` / SQLDATE, `QuadClass`, `GoldsteinScale`, `AvgTone`, `NumMentions`).

## 10. Temporal alignment (binding)

For news day `t`, each RV control is computed from market sessions **strictly before day `t`**:
- every window **ends at the last market session on or before `t−1`**;
- **excludes day `t`** (pre-treatment relative to day-`t` news features);
- **excludes outcome day `t+1`** (pre-outcome relative to `|return|_{t+1}`);
- RV is **pre-treatment** relative to day-`t` news features;
- RV is **pre-outcome** relative to `|return|_{t+1}`.

## 11. Horizon-set rationale

- **Why 5:** ≈ one trading week; captures **acute short-lag volatility clustering**, the likely dominant next-day volatility-confounding channel. A monthly-only RV would smooth this short-lag structure away.
- **Why 22:** ≈ one trading month; captures the **medium-horizon volatility level / state**.
- **Why `{5,22}` together:** they jointly control the most relevant **short and medium** volatility-persistence channels for next-session absolute returns — the deconfounding that matters most — without the extra primary cost of the 60-session horizon.
- **Why not 60 in primary:** 60 is weaker on three axes at once — (1) least marginal next-day deconfounding beyond 5/22; (2) likely highly collinear with 22 (the 60-window contains the 22-window); (3) a 60-session warm-up drops ~3 months of early in-sample days vs ~1 month for `{5,22}`. Under the bounded-null / modest-association power frame these costs are real.
- This is an **explicit modeling choice, not a silent retreat from HAR**: 60 is retained and disclosed as robustness (§13), not discarded.

## 12. Estimand reinterpretation

- **Old headline:** "news ↔ `|return|_{t+1}`, net of rank-date and news volume/coverage controls."
- **New headline:** "**incremental news signal over a short/medium volatility-persistence baseline**, net of rank-date, news volume/coverage controls, and strictly-prior HAR-style realized-volatility controls (`trailing_rv_5`, `trailing_rv_22`)."

This is a more demanding and more honest estimand than the old volume-only-controlled statistic.

**Partial-deconfounder limitation.** HAR `{5,22}` is a **partial deconfounder, not complete control of latent volatility state.** It controls only the **short- and medium-horizon trailing-realized-volatility components** of the latent volatility state. It does **not** capture: implied / forward-looking volatility; intraday range volatility; jump risk; overnight-gap risk; volatility-of-volatility; quarterly / longer-horizon regime stress; or other unobserved market-stress dimensions. Adding `{5,22}` reduces the dominant short/medium realized-volatility persistence confound but does **not** eliminate all volatility-state confounding; **residual volatility-state confounding remains an interpretive limitation** and must not be written as if fully controlled.

## 13. Sensitivity / robustness plan (report-only; cannot rescue)

Pre-specified report-only arms:
- **no-RV old-spec diagnostic** (k=4 at-join), for reference only;
- **single-window arms:** `trailing_rv_5` alone, `trailing_rv_22` alone, `trailing_rv_60` alone;
- **primary** `{5,22}` (k=6);
- **long-horizon robustness:** full `{5,22,60}` HAR.

**Rules (binding):**
- Primary is `{5,22}`.
- Robustness **cannot rescue** a failed/null primary and **cannot overturn** the primary verdict.
- A **primary-null but robustness-positive** result is **not** a success.
- A **primary-positive but robustness-unstable** result must be **flagged as fragile**.
- If `{5,22}` and `{5,22,60}` **materially differ**, report it as **long-horizon sensitivity / regime-stress dependence**, not as a revised primary.

**Sample-attrition control — two reporting modes (binding):**
- **(A) Native-sample:** each arm on its own valid eligible sample; sample size + exclusions disclosed.
- **(B) Common-sample:** when *comparing* control sets, recompute all compared arms on the **common most-restrictive eligible subsample**. For any comparison involving `trailing_rv_60`, use the **60-eligible common subsample for all arms in that comparison**. This isolates control-set change from warm-up-driven attrition.
- Do not interpret cross-arm differences without identifying whether they arise from **control-set change**, **sample change**, or **both**.

## 14. Warm-up / missing / degenerate handling

- **Primary warm-up (`{5,22}`):** a news day `t` is eligible for the primary RV-controlled statistic only if **both** `trailing_rv_5` and `trailing_rv_22` are computable — i.e. **≥ 22 valid prior trading sessions ending on or before `t−1`**. Days lacking this are **excluded from the RV-controlled primary**; the exclusion is **counted, reported, deterministic, not imputed, not post-hoc rescued**.
- **Robustness warm-up (`60`):** any arm using `trailing_rv_60` has its own **60-prior-session** eligibility and reports its **additional** sample loss separately. The 60-session warm-up **must not redefine the primary sample** except inside an explicit robustness / common-sample report.
- **Degenerate:** if `trailing_rv_5` or `trailing_rv_22` is constant, missing, undefined, or induces rank deficiency in a primary cell, follow the locked full-rank / fail-closed convention. If the expanded ranked control matrix is **rank-deficient or non-computable**, the affected estimate is **BLOCKED pending design review**. Do **not** silently regularize, drop RV controls, fall back to no-RV, or change windows post hoc.
- **Optional future fallback (explicitly NOT in this amendment):** because `{5,22}` overlap, collinearity is expected; if later diagnostics show severe destabilizing near-collinearity, a *separately authorized future* design turn may consider an orthogonalized parameterization (e.g. `trailing_rv_5` + a 6–22-session increment). Not built into this primary.

## 15. Full-rank / fail-closed implications

The expanded k=6 control matrix raises the rank / computability burden. The existing fail-closed conventions apply unchanged: non-computable-to-exactness ⇒ **BLOCKED**, never silent regularization or control-dropping. §12 subsets that fall below `N_eff > 9` become non-computable / BLOCKED rather than reverting to a smaller control set.

## 16. Reporting diagnostics (disclosure, not rescue)

Required, pre-specified, **cannot rescue / overturn** the primary verdict:
- rank correlation between each primary RV control and each primary news feature;
- rank correlation between each primary RV control and the outcome;
- **inter-horizon rank correlation `trailing_rv_5` ↔ `trailing_rv_22`**;
- retained sample after primary RV warm-up exclusions (and count lost);
- **additional** sample loss for 60-session robustness arms;
- rank / full-rank diagnostics for the expanded control matrix; cells lost to RV-induced rank deficiency;
- near-collinearity diagnostics on the ranked control matrix: **VIF** and **condition number** (both);
- robustness table comparing: no-RV old-spec / single-window arms / primary `{5,22}` / full `{5,22,60}`;
- **native-sample and common-sample** versions of the robustness comparisons.

## 17. Sequencing consequences

- This amendment is a **governing-spec change** and must pass its **own correction → canary → external-byte-review cycle before the join**.
- **Extraction remains unblocked** by this amendment (price-blind, outcome-blind) but **still unauthorized**.
- **Conservative sequencing recommendation:** complete this amendment gate cycle **before** spending the irreversible extraction read, so the at-join design is settled before any data contact.
- **Join remains blocked** until this amendment cycle is clean and the join is separately authorized.
- **Separate join-gate bookkeeping (not in this amendment):** outcome-side exactness remains a distinct join-gate item — confirm the `next_session_return` / `abs(next_session_return)` convention matches RV's close-to-close log-return convention; confirm the civil_date-to-trading-session mapping; confirm overnight / gap handling. These are not resolved here.

## 18. Boundary confirmation

Design-only draft. No execution, no extraction, no GDELT contact, no raw-event read, no market-data read, no outcome read, no `next_session_return` / `abs(next_session_return)` read, no real-data trailing RV computed or read, no tests, no V1/V2, no 2023+. The five-field GDELT allow-list is untouched. **Extraction remains unblocked but unauthorized; the join remains blocked; execution remains unauthorized.**
