# Compression Lane — Collinearity Diagnostic Authorization v0.1 (DRAFT; no run)

**DRAFT ONLY. This memo does not itself authorize data contact until owner review and explicit acceptance. No diagnostic may be written or run until this authorization is accepted. No gate, episode-count audit, wake/outcome computation, alpha spend, or sealed access is authorized by this draft.**

---

## 1. Anchors and current state

- **Current HEAD:** `8dbbaf72aff6a5bfe1f2179652ac4425425454db`
- **Compression Stage-1 memo:** `docs/compression_stage1_design_memo_v0_1.md`
- **Compression Stage-1 memo SHA-256:** `66c54688374c439594546b715d65211340b8680cbe055fca6736c208cea7d420`
- **Compression decision memo SHA-256:** `389798b8ce7cdcb7533645fb190fa3270a46fe4f84149d09d834c3bc3c530660`
- **Atlas SHA-256:** `c44c3b3f1bed648fdc5c02192b6ea62cbae4d8439267d17b34d50ca58fd8bd31`
- **Current state:** accepted draft only, **not frozen.**
- **Active lane count:** **zero.**
- **No data contact has yet been authorized for Compression.**

---

## 2. Authorization boundary

- This draft **does not run anything.**
- This draft **does not write code.**
- This draft **does not open market data.**
- If later accepted and committed, this memo would authorize writing and running **only the pre-gate collinearity diagnostic to the frozen spec.**
- It would **not** authorize an episode-count audit.
- It would **not** authorize a sandbox gate.
- It would **not** authorize wake/outcome computation.
- It would **not** authorize alpha spend.
- It would **not** authorize sealed data.
- The diagnostic output would be a **separate artifact** and must be reviewed separately.

> Committing this authorization freezes the diagnostic specification. It authorizes implementing and running the diagnostic to that frozen spec only. The diagnostic result is a separate artifact. Survival of the diagnostic does not authorize a gate.

---

## 3. Purpose of the diagnostic

- The diagnostic is a **feature-side / event-side collinearity check.**
- It asks whether the Compression metric, CR, is **empirically absorbed by the boring baseline set.**
- It does **not** ask whether CR predicts expansion.
- It does **not** inspect future wake.
- It does **not** compute any forward target.
- It is a **pre-gate rejection filter.**

> The collinearity diagnostic is a one-way reject-only filter. Feature-space absorption can kill CR. Survival only permits the next pre-gate step, the distinct-episode feasibility/count audit. Survival does not prove predictive information, force behavior, or market relevance.

---

## 4. Five frozen diagnostic rules

The following five rules are frozen at the draft-spec level (they become binding on acceptance/commit).

### A. Joint / incremental absorption
- Absorption must be judged **jointly** over the full baseline set.
- Pairwise correlations are **descriptive only.**
- A metric can have modest pairwise correlations with each baseline and still be absorbed by the joint baseline model.
- The diagnostic must use **joint / incremental absorption** as the decision criterion.

> Pairwise correlation is not the absorption test. The B6 lesson applies here: a construct can look only modestly related to each baseline individually and still contribute no incremental structure over the full baseline set.

### B. Frozen strong baselines
- Baseline specifications must be **frozen before data contact.**
- Baselines must be the **strongest reasonable boring explanations, not weak strawmen.**
- Do **not** choose baselines after seeing whether CR survives.
- Do **not** weaken the baseline set to let CR through.

### C. Pre-registered absorption threshold and conservative borderline rule
- The absorbed-vs-survives threshold must be declared **before computing CR residuals.**
- Do **not** choose the threshold after seeing the diagnostic result.
- The threshold is a **diagnostic bar, not an alpha threshold.**
- Because `ER_21` is a near-neighbor of CR, the threshold may be verdict-sensitive. Therefore, this memo includes a conservative borderline rule:
  - if blocked-CV joint-baseline `R² >= 0.85`, status is **`ABSORBED`**;
  - if blocked-CV joint-baseline `R² < 0.75`, status is **`SURVIVES FEATURE-SPACE ABSORPTION`**;
  - if blocked-CV joint-baseline `R²` is in `[0.75, 0.85)`, status is **`BORDERLINE-ABSORBED`**, treated operationally as `ABSORBED` for lane progression.
- `BORDERLINE-ABSORBED` does **not** allow progression to episode counting.
- Do **not** turn a near-miss into survival.

> The 0.80 center point is a diagnostic convention, not an alpha threshold. Because CR and ER_21 are adjacent efficiency-type quantities, results near the bar are treated conservatively: the [0.75, 0.85) band is BORDERLINE-ABSORBED and does not permit progression. CR must clear the absorption diagnostic decisively to proceed.

### D. One-way reject-only framing
- Absorption **kills** CR.
- Survival permits **only** the episode-count audit.
- Survival does **not** mean CR predicts anything.
- Survival does **not** authorize a gate.
- Survival does **not** spend alpha.

### E. Structural firewall enforcement

> The diagnostic must be structurally unable to compute wake, expansion outcome, or forward target; this must be demonstrated by the code structure, not asserted as an instruction.

---

## 5. Future data scope

Specified without opening data now:
- **SPY adjusted close only.**
- **Existing sandbox file only:** `data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv`
- **Expected sandbox SHA-256 for future verification:** `5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901`
- **Allowed columns:** `date`, `adj_close`.
- **Allowed date range:** 2005-01-01 through 2022-12-31 inclusive.
- **No** rows ≥ 2023-01-01.
- **No** OHLC; **no** volume; **no** news; **no** macro; **no** options; **no** cross-asset inputs; **no** sealed-period values.

---

## 6. Future path and data guards

The future diagnostic implementation must verify, **before reading rows**:
- repo root,
- branch,
- HEAD,
- origin/main,
- Compression Stage-1 memo SHA,
- authorization memo SHA,
- sandbox CSV SHA,
- allowed columns only,
- no 2023+ rows.

> No wake does not mean no data-contact rigor. This is the first Compression code that touches real SPY returns, so it inherits full repo, hash, column, and date-range guards.

---

## 7. Primary Compression metric

Frozen for the draft spec.

**Primary feature:**
`CR_21 = rolling close range over 21 trading days / rolling absolute path length over the same 21 trading days`

**Compression intensity for regression/absorption:**
`CI_21 = -log(CR_21)`

**Justification of the transform.**
- CR is bounded in `(0, 1]`.
- Low CR represents stronger containment/compression.
- `-log(CR_21)` maps stronger containment into larger positive values.
- The log transform expands the low-CR region where the Compression construct lives.
- The absorption threshold is defined **relative to this transform.**
- Do **not** switch to raw CR, `1 - CR`, or `logit(CR)` after seeing results.

> CI_21 = -log(CR_21) is frozen as the diagnostic response transform. Because R² is transform-dependent, the absorption threshold is defined relative to CI_21, not raw CR or any later alternative transform.

**Construction constraints.**
- CR uses only adjusted closes **up to and including day `t`.**
- No future data.
- No forward window.
- No threshold.
- No episode definition.
- No outcome.
- The 21-day window is chosen as the primary draft spec because it is a standard one-trading-month path window and aligns with the prior design memo's candidate list.
- Any alternative CR window is **not authorized** by this memo unless explicitly listed as descriptive-only.

**Descriptive-only optional feature.**
- `CR_10` (and its `CI_10 = -log(CR_10)`) may be reported **`DESCRIPTIVE ONLY — not a survival criterion`**. It must not be used to decide survival.

---

## 8. Frozen strong baseline set

Frozen for the future diagnostic draft spec. At minimum:

**A. Volatility level / mean-reversion baseline**
- `log_RV_21`: log trailing realized volatility over 21 trading days, using returns up to `t`.

**B. Bounded-floor / low-vol mechanics baseline**
- `RV_21_trailing_percentile_252`: trailing percentile/rank of `RV_21` over a 252-trading-day history ending at `t`. Captures how close the current volatility state is to the low-vol floor / recent distribution.

**C. Autocorrelation baseline**
- `AC1_21`: lag-1 autocorrelation of daily log returns over the trailing 21-day window.
- `AC1_63`: lag-1 autocorrelation of daily log returns over the trailing 63-day window.

**D. Variance-ratio baseline**
- `VR5_252`: overlap-bias-corrected variance ratio using 5-day overlapping summed returns over a trailing 252-trading-day window, compared to 1-day return variance.
- Why this is stronger:
  - it keeps the 5-day variance-ratio horizon;
  - it uses a 252-day estimation window to give a more stable estimate;
  - it uses an overlap-bias-corrected estimator for overlapping observations;
  - it is included as a strong mean-reversion / variance-ratio baseline, not a weak strawman.
- The variance-ratio baseline is specified with a 252-day estimation window and overlap-bias correction to make it a strong boring baseline rather than a noisy strawman, because variance-ratio / efficiency-ratio absorption is the load-bearing risk identified in the Compression Stage-1 memo.

**E. Efficiency-ratio baseline**
- `ER_21`: absolute net close displacement over 21 trading days divided by 21-day absolute path length.

### ER_21 as load-bearing baseline
- `ER_21` is the **most CR-adjacent baseline.**
- It is the **§5-predicted absorption risk** (Compression Stage-1 memo §5).
- `CR_21` and `ER_21` are both **efficiency-type ratios over the same 21-day window with the same denominator** (21-day absolute path length).
- The **joint model remains the decision criterion.**
- The diagnostic must also report **descriptive ER-alone absorption**:
  - `CI_21 ~ ER_21`;
  - incremental residual share over `ER_21` alone.
- ER-alone reporting is **descriptive only** and does **not** change the joint decision rule.
- Purpose: make a kill legible as either absorption by the efficiency-ratio twin or absorption by the broader joint baseline combination.

**Baseline discipline.**
- These baselines are chosen **before data contact.**
- They are intended to be **strong boring explanations.**
- Baseline ablations may be reported **descriptively**, but survival must be judged against the **full frozen baseline set.**
- **No survival by dropping an inconvenient baseline.**

---

## 9. Absorption model

Frozen at the spec level.

**Primary response:** `CI_21`

**Primary baseline model:**
`CI_21 ~ log_RV_21 + RV_21_trailing_percentile_252 + AC1_21 + AC1_63 + VR5_252 + ER_21`

**Modeling rules.**
- Use only rows where **all features are defined.**
- Standardize features using **training-fold statistics only.**
- Use **blocked chronological cross-validation.**
- Use **5 contiguous chronological folds** unless the future implementation finds fewer than 5 feasible folds; if fewer, **stop and report** rather than changing the fold rule.
- **Primary metric:** blocked cross-validated `R²` of the joint baseline model predicting `CI_21`.
- Also report **in-sample `R²`** as descriptive only.
- **Pairwise correlations** may be reported descriptive only.
- **Baseline ablations** may be reported descriptive only.
- **ER-alone absorption** must be reported descriptive only.
- The survival/absorption decision must use the **full joint baseline model** and the **pre-registered threshold/borderline rule.**

---

## 10. Pre-registered absorption threshold and borderline band

**Primary absorption rule.**
- If blocked cross-validated joint-baseline `R² >= 0.85`, CR is **`ABSORBED`**.
- If blocked cross-validated joint-baseline `R² < 0.75`, CR **`SURVIVES FEATURE-SPACE ABSORPTION`**.
- If blocked cross-validated joint-baseline `R²` is in `[0.75, 0.85)`, CR is **`BORDERLINE-ABSORBED`**.

**Operational rule.**
- `BORDERLINE-ABSORBED` is treated as **absorbed for progression.**
- It does **not** permit progression to episode-count audit.
- It spends **no alpha.**
- It is **not** a hypothesis null.
- It is a **conservative diagnostic stop.**

**Justification.**
- The original 0.80 center point represents a 20% residual feature-variance intuition.
- Because CR is adjacent to `ER_21`, a result close to 0.80 may be sensitive to threshold choice.
- The diagnostic must **not** allow a knife-edge near a round number to decide survival.
- Therefore, survival requires a **decisive** residual share: joint baseline `R² < 0.75`.
- Absorption is decisive at `R² >= 0.85`.
- The middle band is conservatively stopped as **borderline-absorbed.**

> CR survival requires a decisive residual feature share after the frozen joint baseline set. Results near the 0.80 center point are not treated as survival. If blocked-CV joint-baseline R² is in [0.75, 0.85), CR is BORDERLINE-ABSORBED and the lane does not proceed to episode counting.

---

## 11. Structural firewall / forward-unreachability

The future diagnostic script must:
- construct **only feature-side tables**;
- contain **no forward window functions**;
- contain **no wake/outcome/target construction**;
- create **no columns** for future realized volatility, future range, future drawdown, recovery, expansion, target, or `y`;
- **not compute any post-`t` value**;
- **not merge any future-return table**;
- **not read any 2023+ data**;
- include runtime assertions that allowed columns are only `date`, `adj_close`;
- include a **self-scan or equivalent check** that no forbidden forward/wake functions or columns are defined.

> The firewall is a property of the implementation, not a promise about researcher behavior. The diagnostic must make wake/outcome construction structurally unreachable.

---

## 12. Outcome of the future diagnostic

### A. `ABSORBED`
- CR is feature-space absorbed by the joint baseline model.
- Lane **stops before episode-count audit.**
- No alpha spent.
- No wake computed.
- **Not** a hypothesis null.
- **Not** a gate fail.
- Status may become `INFEASIBLE — feature-space absorbed` or similar, subject to future owner decision / atlas vocabulary.

### B. `BORDERLINE-ABSORBED`
- CR lands in the pre-registered borderline band `[0.75, 0.85)`.
- Treat operationally as **absorbed for progression.**
- Lane **stops before episode-count audit.**
- No alpha spent.
- No wake computed.
- **Not** a hypothesis null.
- **Not** a gate fail.
- Record as a **conservative diagnostic stop**, not as evidence about wake or expansion.

### C. `SURVIVES FEATURE-SPACE ABSORPTION`
- CR is not feature-space absorbed under the pre-registered threshold and borderline rule.
- This does **not** prove predictive value.
- This authorizes only the next **separately authorized** artifact: the **distinct-episode feasibility/count audit.**
- **No gate** is authorized by survival.

### D. `DIAGNOSTIC INVALID / HALTED`
- Guard failure, missing data, insufficient feature rows, fold infeasibility, or firewall violation.
- **Stop and report.**
- **No rescue** by changing specs after seeing partial output.

---

## 13. Staging

1. **Draft authorization memo** — this file.
2. **Owner review and acceptance / commit** of authorization.
3. **Implement and run diagnostic** to frozen spec.
4. **Record diagnostic report** as a separate artifact.
5. **If absorbed or borderline-absorbed, stop lane** before episode counting.
6. **If survives, owner may separately authorize** the distinct-episode feasibility/count audit.
7. **Literal freeze** only after diagnostics are adequate.
8. **Sandbox gate** only after literal freeze and explicit authorization.
9. **Sealed data** only under separate atlas authorization.

---

## 14. Non-authorizations

- This draft does **not** authorize data contact.
- This draft does **not** authorize code.
- This draft does **not** authorize running the diagnostic.
- This draft does **not** authorize an episode-count audit.
- This draft does **not** authorize a gate.
- This draft does **not** authorize alpha spend.
- This draft does **not** authorize sealed data.
- This draft does **not** authorize wake/outcome computation.
- **Active lane count remains zero.**

---

## 15. Boundary confirmations

- No tests were run.
- No code was written.
- No modeling was run.
- No market data was opened.
- No gate was run.
- No audit was run.
- No synthetic-null check was run.
- No wake/outcome was computed.
- No sealed data was accessed.
- No diagnostic spec is binding until owner acceptance/commit.
