# Compression Second Distinctness Diagnostic Authorization v0.1 (Non-Tautological Path-Roughness Baselines)

**SPECIFICATION / AUTHORIZATION MEMO ONLY. This memo freezes the second feature-side distinctness diagnostic design. It does not run the diagnostic, does not open market data, does not authorize a gate, does not authorize an episode-count audit, does not spend alpha, and does not compute wake/outcome.**

---

## 1. Anchors and current state

- **Current HEAD:** `2e276ef15dbde18a33d143abb1194569940d35ba`
- **Prior diagnostic result commit:** `b3ee41e6c73c2fc5008758bff729bef6ad762f02`
- **CR distinctness memo commit:** `2e276ef15dbde18a33d143abb1194569940d35ba`
- **CR distinctness memo SHA-256:** `a53c75ace9f2f695c25c0e6e3f11db0bec65015c87f0990e5c51cc403457946c`
- **Prior diagnostic report SHA-256:** `b2189ae590a582706b4e60f61082f8525bf02ee3426dcf8b4d8f0d113c1ff9d4`
- **Prior diagnostic script SHA-256:** `272330c5de51e0769049e50ee032efb692e926f79c9dc021ca9e982166c5c142`
- **First authorization memo SHA-256:** `d4fc494d5b435798f0906d528333f793da7e34a53f930926ce8509885aca5628`
- **Compression Stage-1 memo SHA-256:** `66c54688374c439594546b715d65211340b8680cbe055fca6736c208cea7d420`
- **Active lane count:** zero. No gate, episode-count audit, or alpha spend is authorized.

---

## 2. What is already established

- CR **survived** Diagnostic 1.
- Diagnostic 1 was **feature-side only.**
- Diagnostic 1 computed **no wake/outcome/target.**
- Diagnostic 1 ran **no gate.**
- Diagnostic 1 spent **no alpha.**
- Diagnostic 1 used a genuine **Lo–MacKinlay VR5_252** baseline.
- CR-vs-ER localization showed:
  - ER-alone R²: `0.6311`
  - joint R²: `0.659541`
  - drop-ER joint R²: `0.0262`
  - corr(CI_21, ER_21): `-0.796`
- Survival is real but **does not settle whether CR is merely range-based path roughness.**

---

## 3. Why this second diagnostic is needed

- Diagnostic 1 tested **volatility / autocorrelation / displacement-efficiency** baselines.
- It did **not** include explicit **non-tautological path-roughness / Katz-FD / tortuosity** baselines.
- The CR distinctness memo found CR **close to, but not analytically identical with,** these measures.
- Direct range/path roughness is now analytically identified as a **response transform, not a valid empirical predictor.**
- Therefore, reasoning alone should **not** reclassify CR as fully absorbed by the broader path-roughness family.
- But the episode-count audit should **not** proceed before CR is tested against its nearest non-tautological cousins.

> The first diagnostic showed that CR is not absorbed by the baselines it tested. It did not test the non-tautological path-roughness family. The second diagnostic tests that omitted nearest-family door before any episode-count audit.

---

## 4. Analytical identification already established — no data needed

Since:

`CR_21 = range_21 / path_21`

and:

`CI_21 = -log(CR_21)`

then:

`CI_21 = log(path_21 / range_21)`

Therefore:

`RANGE_PATH_ROUGHNESS_21 = path_21 / range_21 = exp(CI_21)`

This is an **exact deterministic transform of the response.**

Also, with fixed `n_steps = 20`:

`KATZ_FD_RANGE_21 = log(n_steps) / (log(n_steps) + log(range_21 / path_21))`

Since:

`range_21 / path_21 = CR_21`

then:

`KATZ_FD_RANGE_21 = log(20) / (log(20) - CI_21)`

This is also an **exact deterministic function of `CI_21`.**

> RANGE_PATH_ROUGHNESS_21 and KATZ_FD_RANGE_21 are not empirical baselines. They are deterministic response transforms. Including either in the predictor set would contaminate the decision model with identity.

**Interpretation.**

- This proves CR is, **by definition, the range-based path-roughness skeleton.**
- This is **identification evidence, not predictive evidence.**
- A deterministic transform of the response is **not a discovery from data.**
- These features may be **disclosed** in the future report, but they must **not enter the Level-1 decision model.**

> A deterministic transform of the response is not a predictive discovery. It is an identification result.

---

## 5. Stated prior

A clear prior, stated without making it a verdict:

- Absorption by non-tautological path-roughness relatives is **expected.**
- Reason: CR's incremental joint R² over ER_21 was thin:
  - joint R² `0.659541`
  - ER-alone R² `0.6311`
  - incremental difference ≈ `0.0284`
- CR has surprised once, so the prior must **not** decide the result.

> Expected outcome: absorption or borderline absorption by the non-tautological path-roughness family. This is a prior, not a verdict.

---

## 6. Data boundary for future implementation

Frozen for the future implementation; **no data is read now.**

Future implementation may use only:

`data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv`

Expected sandbox SHA-256:

`5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901`

Allowed input columns:
- `date`
- `adj_close`

Allowed date range:
- 2005-01-01 through 2022-12-31 inclusive
- No rows ≥ 2023-01-01.

No OHLC. No volume. No news. No macro. No options. No cross-asset inputs. No sealed-period values.

---

## 7. Structural firewall for future implementation

The future implementation must be **structurally unable** to compute wake, expansion outcome, or forward target. It must:

- construct only feature-side tables;
- contain no forward-window functions;
- contain no wake/outcome/target construction;
- create no future-return, future-range, future-volatility, drawdown, recovery, expansion, target, or `y` columns;
- not compute any post-`t` value;
- not merge any future-return table;
- not read any 2023+ data;
- assert input columns exactly `{date, adj_close}`;
- self-scan user-defined function names and constructed dataframe columns for forbidden tokens;
- reject negative future shifts such as `.shift(-...)`.

> The firewall must be structural: wake/outcome construction must be unreachable from the diagnostic data structures, not merely prohibited by instruction.

---

## 8. Frozen response

Response remains:

`CI_21 = -log(CR_21)`

with:

`CR_21 = rolling close range over 21 trading days / rolling absolute path length over the same 21 trading days`

Definitions:
- `range_21 = max(adj_close) - min(adj_close)` over the trailing 21 trading-day window ending at `t`;
- `path_21 = sum(abs(adj_close_i - adj_close_{i-1}))` over that same trailing 21-day window;
- `CR_21 = range_21 / path_21`;
- `CI_21 = -log(CR_21)`;
- invalid if `path_21 <= 0`, `range_21 <= 0`, or non-finite.

Do **not** use raw CR, `1 - CR`, or `logit(CR)` as the decision response.

---

## 9. Frozen non-tautological path-roughness baseline family

A family-spanning baseline set with **no response transforms**. The point is not to test a strawman single variant; it is to test whether CR is absorbed by **non-tautological path-roughness relatives that use different extent definitions.**

**Required Level-1 baseline features:**

**A. `ER_21`**
- `ER_21 = abs(adj_close_t - adj_close_start) / path_21`
- same 21-trading-day window as CR;
- carried forward because it is the closest displacement-efficiency twin.

**B. `LOG_TORT_21`**
- `LOG_TORT_21 = log(path_21 / abs(adj_close_t - adj_close_start))`
- invalid if endpoint displacement is `<= 0`;
- a tortuosity/sinuosity-style path-length-over-displacement measure;
- related to ER but uses the log tortuosity form.

**Note on extent independence.** `ER_21` and `LOG_TORT_21` are the same extent concept — endpoint-displacement-over-path — in two algebraic forms (`LOG_TORT_21 = -log(ER_21)`, where defined). They are one independent axis, not two. The Level-1 set therefore spans two independent non-range extent definitions: (i) endpoint-displacement, represented by `ER_21` / `LOG_TORT_21`, and (ii) first-point-distance, represented by `KATZ_FD_FIRST_21`. The range extent is excluded as tautological by §4. Accordingly, `ABSORBED` means CR is absorbed by displacement-based and first-point-based roughness; `SURVIVES` means CR is distinct from both and is specifically a range-extent construct — “excursion from extremes” distinct from “excursion from endpoint.” The test spans two independent extent concepts, not three; any survival should be read against that span, not oversold as distinctness from three independent baselines.

**C. `KATZ_FD_FIRST_21`** — first-point Katz-style fractal dimension.
Use the trailing 21-close window ending at `t`. Let:
- `n_steps = 20`
- `L = path_21`
- `d_first = max(abs(adj_close_i - adj_close_start))` over the window

Then:

`KATZ_FD_FIRST_21 = log(n_steps) / (log(n_steps) + log(d_first / L))`

Invalid if:
- `L <= 0`
- `d_first <= 0`
- `d_first / L <= 0`
- denominator non-finite or zero.

**Explicit exclusions from the Level-1 model.** Do **NOT** include:
- `RANGE_PATH_ROUGHNESS_21`
- `KATZ_FD_RANGE_21`

Reason:
- `RANGE_PATH_ROUGHNESS_21 = exp(CI_21)`
- `KATZ_FD_RANGE_21 = log(20) / (log(20) - CI_21)`
- These are deterministic response transforms, not empirical baselines.

---

## 10. Decision model

Primary response: `CI_21`

Primary Level-1 non-tautological path-roughness model:

`CI_21 ~ ER_21 + LOG_TORT_21 + KATZ_FD_FIRST_21`

The decision must be based **only** on this Level-1 model.

Also report, **separately and descriptively**:
- the analytical identity between `CI_21` and `RANGE_PATH_ROUGHNESS_21`;
- the analytical identity between `CI_21` and `KATZ_FD_RANGE_21`;
- pairwise relationship of `CI_21` to each non-tautological baseline;
- ablations of Level-1 features;
- in-sample Level-1 R² (descriptive only).

The future report must clearly separate:
- **analytical identification;**
- **empirical collinearity;**
- **descriptive correlations;**
- **operational decision.**

---

## 11. Cross-validation and standardization

For future implementation:
- use only rows where all primary Level-1 features are finite;
- standardize features using **training-fold statistics only;**
- use **5 contiguous chronological folds;**
- if fewer than 5 feasible folds exist, **stop and report;**
- for each fold, train on the other folds and test on the held-out fold;
- use OLS with intercept;
- compute **pooled out-of-fold R²** across all held-out predictions;
- report fold ranges and row counts.

---

## 12. Decision rule

Primary decision metric:

`blocked cross-validated joint-baseline R² of the Level-1 non-tautological path-roughness family model`

Frozen threshold:
- `R² >= 0.85` → `ABSORBED BY NON-TAUTOLOGICAL PATH-ROUGHNESS FAMILY`
- `R² < 0.75` → `SURVIVES NON-TAUTOLOGICAL PATH-ROUGHNESS DISTINCTNESS TEST`
- `[0.75, 0.85)` → `BORDERLINE-ABSORBED BY NON-TAUTOLOGICAL PATH-ROUGHNESS FAMILY`

Operational meaning:
- `ABSORBED BY NON-TAUTOLOGICAL PATH-ROUGHNESS FAMILY` supports the future closure decision status candidate `RECLASSIFIED — known construct`.
- `BORDERLINE-ABSORBED BY NON-TAUTOLOGICAL PATH-ROUGHNESS FAMILY` is treated operationally as **absorbed for progression** and also supports reclassification, unless a later closure decision memo says otherwise.
- `SURVIVES NON-TAUTOLOGICAL PATH-ROUGHNESS DISTINCTNESS TEST` does **not** authorize a gate. It only means CR may be considered specifically **range-based path roughness distinct from displacement/first-point path-roughness relatives**, and may proceed, **by separate authorization**, to an episode-count audit.
- **No outcome authorizes wake/gate/alpha directly.**

---

## 13. Baseline-intercorrelation note

> The non-tautological path-roughness baselines are expected to be intercorrelated. This is not a flaw. The diagnostic asks whether CR lies in the subspace spanned by path-roughness relatives with different extent definitions, not whether any single member uniquely explains CR.

---

## 14. Tautology / known-transform guard

The future report must explicitly state that:
- `RANGE_PATH_ROUGHNESS_21` is an **exact deterministic transform** of `CI_21`;
- `KATZ_FD_RANGE_21` is an **exact deterministic function** of `CI_21` under fixed `n_steps = 20`;
- **neither is included** in the Level-1 decision model;
- **neither is used** to produce the empirical R² decision.

> A deterministic transform of the response is not a predictive discovery. It is an identification result.

---

## 15. Outputs required from future diagnostic report

The future diagnostic report must include:
- guard verification;
- sandbox hash verification;
- input date range and row count;
- confirmation no 2023+ rows;
- allowed columns confirmation;
- structural firewall proof;
- feature definitions;
- valid diagnostic row count;
- fold ranges and row counts;
- Level-1 blocked-CV joint R²;
- in-sample Level-1 R² (descriptive only);
- pairwise correlations (descriptive only);
- ablations (descriptive only);
- analytical identity disclosure for `RANGE_PATH_ROUGHNESS_21`;
- analytical identity disclosure for `KATZ_FD_RANGE_21`;
- tautology / known-transform disclosure;
- final status:
  - `ABSORBED BY NON-TAUTOLOGICAL PATH-ROUGHNESS FAMILY`,
  - `BORDERLINE-ABSORBED BY NON-TAUTOLOGICAL PATH-ROUGHNESS FAMILY`,
  - or `SURVIVES NON-TAUTOLOGICAL PATH-ROUGHNESS DISTINCTNESS TEST`;
- statement that no wake/outcome/target was computed;
- statement that no gate was run;
- statement that no episode-count audit was run;
- statement that no alpha was spent;
- statement that no sealed data was accessed.

---

## 16. Non-authorizations

- This authorization memo **does not run the diagnostic.**
- It **does not** authorize an episode-count audit.
- It **does not** authorize a gate.
- It **does not** authorize alpha spend.
- It **does not** authorize sealed access.
- It **does not** authorize wake/outcome computation.
- It **does not** change the atlas status.
- It **does not** reclassify CR by itself.
- It **only freezes the second diagnostic design.**

---

## 17. Boundary confirmations (this drafting turn)

- No code was written.
- No code/diagnostic was run.
- No tests were run.
- No market data was opened.
- No sealed data was accessed.
- No gate, audit, or wake/outcome computation occurred.
- This memo authorizes implementing/running the second diagnostic to this frozen spec only **after** owner review and acceptance/commit — and even then authorizes nothing beyond that diagnostic.
