# Lane 2 TTG Magnitude-Pressure — Option A In-Window Multi-Horizon Screen — Design Memo v0.3

## Status

- **Status:** DRAFT for review/lock; supersedes the v0.1/v0.2 drafts.
- Design + methodology only; **no data contact; no execution.**
- **Not lockable** until the §1.1 prerequisites are met.
- **v0.3 change:** the prereg trigger is **weekly-centered (h=5)**; monthly (h=21) is **demoted to exploratory context / contradiction-veto**; daily (h=1) remains **closed / left anchor only**.
- **Value-safety:** design text, structural trading-day counts, and the calendar `2023+ seal` concept only — no data, no row content, no coverage results.
- **Provenance:** drafted pre-execution; no 2023+ contact; inherits the companion long-horizon benchmark/MDE note.
- The committed bytes are **generated from this specification** and **still require a post-commit byte-review for wording fidelity**; value-safety and anchor checks are necessary but not sufficient for wording fidelity.

## 1. Purpose and standing

A **bounded exploratory in-window screen**. Its only output is **binary**: whether the weekly pressure→magnitude association comes back **strong enough in-window** to justify writing a *separate* weekly preregistration. It is **non-confirmatory**. The daily confirmatory question remains **closed**. It runs only on **2013-01-01 … 2022-12-31**; the **2023+ seal is untouched and unspent**.

### 1.1 Prerequisites to lock

- The companion benchmark/MDE note exists and establishes: **monthly nonviable**, **daily closed**, **weekly nonviable under floor assumptions and borderline only under stacked optimism**.
- If **no horizon clears confirmation viability** under accepted assumptions, the screen **does not lock as prereg-triggering** and may run **only as pure exploration**.
- The weekly threshold `T_weekly` is **finalized against the companion note's weekly MDE**, not against the soft external band.

### 1.2 Horizon roles after the companion note

| Horizon      | Role                                               |
| ------------ | -------------------------------------------------- |
| h=1 daily    | closed / left anchor only                          |
| h=5 weekly   | sole conceivable prereg-trigger horizon            |
| h=21 monthly | exploratory context only; cannot trigger; may veto |

## 2. What this screen may and may not do

- **May:** compute in-window partial-Spearman point estimates of the F1/F2/F3 pressure composite vs absolute multi-horizon magnitude, and emit one binary trigger read for the weekly horizon.
- **May not:** confirm anything; reopen the daily confirmatory question; contact 2023+; acquire or spend the seal; retune features; treat its own parameters as prereg locks.

## 3. Frozen inheritances

Inherited unchanged from the committed feature design; **no retuning**:
- F1/F2/F3 pressure composite unchanged;
- common daily `NumMentions` denominator;
- equal-weight standardized composite;
- expanding past-only z-scaler;
- coverage-normalized (not raw-volume-driven).

## 4. Outcomes per horizon

Absolute log-return magnitude over the forward window:
- h=1: `abs( ln(close_{s+1} / close_s) )`
- h=5: `abs( ln(close_{s+5} / close_s) )`
- h=21: `abs( ln(close_{s+21} / close_s) )`

## 5. Leakage timing

- Feature z-score uses information **through day s only**;
- controls use information **≤ s**;
- HAR-RV trailing windows **end ≤ s−1**;
- the outcome spans **s+1 … s+h**;
- **no part of the forward outcome enters any feature or control.**

## 6. Controls — RATIFIED

Per horizon, HAR-RV trailing controls:
- h=1: `trailing_rv_5`, `trailing_rv_22`
- h=5: `trailing_rv_5`, `trailing_rv_22`
- h=21: `trailing_rv_22`, `trailing_rv_60`

Plus the standard non-RV partial set in all cases: **rank-date + volume/coverage terms.**

## 7. Statistic

- **One-sided positive partial Spearman**, Fisher-z transform.
- **Overlap-aware effective N** (forward-overlapping multi-horizon windows reduce effective N).
- Primary read is **ρ point estimates and the daily→weekly gradient**, **not p-values**.
- Fisher-z SE = `1 / sqrt(N_eff - k - 3)`.
- In-window resolving power (2013–2022): weekly ≈ **500 non-overlap** observations, monthly ≈ **120**; monthly is **context only**.

## 8. Pre-committed decision rule (weekly-centered)

### 8.1 Trigger rule

A weekly prereg is **worth writing only if all** hold:
1. `rho_5 > 0`
2. `rho_5 >= T_weekly`
3. `rho_5 >= rho_1 + 0.05`
4. monthly veto does **not** fire

### 8.2 Weekly threshold T_weekly

- **Proposed lock: `T_weekly = 0.20`.**
- `T_weekly` is tied to the **weekly confirmation MDE floor** (companion note), **not** to the soft external band.
- `T_weekly = 0.15` is **not acceptable** unless a separate explicit decision accepts **favorable overlap efficiency**.
- `0.20` sits **above** the whole soft band `0.10–0.15`, so a **normal expected weekly effect does not trigger**; **only an unexpectedly large weekly effect triggers**.
- Such a trigger is a **scrutiny flag, not a green light**.

### 8.3 Asymmetric interpretation

- If the trigger **passes**: `CANDIDATE_WEEKLY_PREREG_WORTH_WRITING` — **with an explicit warning** that the in-window weekly effect **exceeded external expectations** and **needs artifact scrutiny before any seal spend** (a too-large in-window effect is more likely an artifact/leakage/coverage signature than a real after-HAR-RV effect).
- If the trigger **fails**: `NO_WEEKLY_PREREG_TRIGGER_FROM_THIS_SCREEN`.
- A failed screen is **non-triggering / inconclusive, not disconfirmation.**

### 8.4 Monthly veto

- Monthly **cannot be a positive trigger.**
- If `rho_21 <= -0.05`, the screen **does not trigger** (a clearly negative monthly association contradicts the weekly-positive hypothesis).

### 8.5 Daily-horizon firewall

- h=1 is **left anchor only** (used only to compute the `rho_5 ≥ rho_1 + 0.05` gradient).
- **No rescue of the daily confirmatory question**; **no reopening of Option C.**

### 8.6 Per-horizon confirmation-viability gate

- **Monthly:** not confirmation-viable; **exploratory / veto only.**
- **Weekly:** confirmation MDE ≈ **0.20 floor / ≈0.15 best case**. Under **floor assumptions weekly fails the viability inequality**; weekly is **borderline only under stacked optimism**.
- A horizon that **fails confirmation viability cannot be a prereg target regardless of its in-window estimate** — a strong in-window ρ on an unconfirmable horizon does not make it confirmable.

## 9. Data scope and seal discipline

- In-window **2013-01-01 … 2022-12-31 only.**
- **2023+ seal untouched.**
- **No 2023+ contact, probe, or coverage check** of any kind.

## 10. What a passing screen does and does not authorize

A passing (triggering) screen authorizes **only**:
- writing a **separate** weekly preregistration; and
- **prior-artifact scrutiny** of the surprisingly large in-window effect.

It does **not** authorize:
- 2023+ spend or acquisition;
- a monthly prereg;
- any confirmation;
- reuse of the screen's parameters (threshold, controls, composite) as prereg locks **without fresh derivation**.

## 11. Governing anchors

**Hard SHA-pinned:**
1. Benchmark-limitation memo — `docs/lane2_ttg_magnitude_pressure_predata_benchmark_limitation_memo_v0.1.md` @ `c841f3c37762156038996460a420e537aa7cb8bb`.
2. Companion long-horizon benchmark/MDE note — `docs/lane2_ttg_magnitude_pressure_long_horizon_benchmark_mde_note_v0.1.md` @ `abffe6eb7015e621f20aa0cc6d4779da8ed03865`.

**Descriptive / unpinned (NOT SHA-pinned in this draft; require later SHA-pin / re-verification before any future lock; no SHA tokens included for these):**
- F1/F2/F3 feature-design lock;
- mechanism / extraction-design memo;
- §8a / §10 MDE machinery + §12 influence gate + two-sided detectability floor;
- HAR-RV control-scope amendment;
- extraction authorization gate memo;
- directional TTG→SPY prereg v1.1 and directional null-result anchor.

These descriptive references are intentionally left unpinned; moving this memo from draft to lock requires SHA-pinning and re-verifying each.

## 12. Boundary attestation

No repo data read; no row-level data; no feature matrix / labels / predictions; no SOURCEURLs; no raw prices / returns / OHLC; no GDELT/source contact; no 2023+ contact; no model fitting; no execution. This memo **does not authorize execution or seal contact**; running the screen requires a **separate explicit go decision after lock**, and the default lean is **no-trigger / no-spend absent a surprisingly strong weekly in-window signal**.
