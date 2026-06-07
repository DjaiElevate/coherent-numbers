# Lane 2 TTG Magnitude-Pressure — Weekly Spend Decision (Lane Closure) v0.1

## Status

- **Status: DECISION RECORD.**
- Records a **no-spend terminal judgment** for the magnitude-pressure lane on the currently achievable 2023+ seal.
- **Value-safe:** design arithmetic + prior-record references only; no data contact; no execution.
- This record **authorizes nothing**; any future action requires separate explicit authorization.
- **Provenance:** drafted after byte-review of the companion note and screen memo; no data contact; no execution; no 2023+ contact.

## 0. Purpose

This memo records the **terminal decision** for the TTG magnitude-pressure question after the supporting records were committed and byte-reviewed. In plain terms, the decision is:

> **Do not spend the 2023+ seal on confirmation at any horizon.**

## 1. What this closes over

This closure rests on three hard-pinned committed records:

1. **Benchmark-limitation memo** — `docs/lane2_ttg_magnitude_pressure_predata_benchmark_limitation_memo_v0.1.md` @ `c841f3c37762156038996460a420e537aa7cb8bb`. Role: the **daily next-session horizon** was settled `OPTION_C_NONVIABLE_BEST_CASE_FAIL`.
2. **Companion benchmark/MDE note** — `docs/lane2_ttg_magnitude_pressure_long_horizon_benchmark_mde_note_v0.1.md` @ `abffe6eb7015e621f20aa0cc6d4779da8ed03865`. Role: **per-horizon confirmation-viability arithmetic** on the achievable seal; passed byte-review.
3. **Screen memo v0.3** — `docs/lane2_ttg_magnitude_pressure_option_a_multi_horizon_screen_design_v0.3.md` @ `ddc5c92ed2588219b4c7a8700b611022b967cf35`. Role: **weekly-centered exploratory design**; passed byte-review.

The two new local records (companion note, screen memo) were verified **clause-by-clause**; their load-bearing clauses were **present and unsoftened**.

## 2. §8.6 layout ratification

- The screen memo's §8 was generated with **six subsections** rather than the original spec's five.
- **"Monthly veto" was promoted to its own §8.4.**
- This shifted:
  - the **daily-horizon firewall to §8.5**;
  - the **per-horizon confirmation-viability gate to §8.6**.
- Byte-review confirmed the six-subsection structure is **substantively harmless**.
- **§8.6 carries the load-bearing weekly/no-spend logic and softens nothing.**
- The six-subsection layout is **ratified as draft-harmless**.
- Internal §8.x cross-reference numbering must be **rechecked only if** the screen memo ever moves from draft toward lock.

## 3. Viability summary

The decision rests on **MDE arithmetic, which dominates** the horizon-viability question. The external benchmark band remains a **soft prior, not locked**.

- **Achievable seal:** approximately **~800 trading days**; assumptions are **one-sided / optimistic** where noted.
- **Daily h=1:**
  - **closed by prior §8a**;
  - `rho_MDE ≥ ~0.088` vs `rho_expected ≈ 0.07`;
  - **not reopened.**
- **Weekly h=5:**
  - confirmation MDE ≈ **`0.20`** under floor assumptions;
  - may approach **`0.14–0.15`** only under favorable overlap;
  - expected band is a soft **`0.10–0.15`**;
  - under floor assumptions, **`rho_MDE >= rho_expected`**;
  - weekly **fails the viability inequality** under floor discipline;
  - weekly is **borderline only under stacked optimism** = top-of-band expected effect **plus** favorable overlap efficiency.
- **Monthly h=21:**
  - confirmation MDE ≈ **`0.43–0.45`**;
  - approximately **~38 monthly observations**;
  - **far above the soft band**;
  - **nonviable / exploratory-only**;
  - **not a prereg target**;
  - not band-confirmable for roughly **two decades** of additional post-2022 data.

## 4. Decision

- **No 2023+ seal spend** for confirmation of the magnitude-pressure hypothesis **at any horizon.**
- **No weekly prereg written.**
- **No screen lock** as a prereg-triggering design.
- **Screen memo v0.3 remains a DRAFT**, unlocked, and **not** a prereg-triggering artifact.
- The **seal remains untouched and unspent.**
- The **daily question remains closed.**

## 5. Preserved option

- The in-window screen over **2013-01-01 … 2022-12-31** may later be run as **pure exploration only if separately and explicitly authorized.**
- Such a run would carry:
  - **no prereg pathway;**
  - **no confirmatory claim;**
  - **no 2023+ contact.**
- **This record does not authorize that run.**

## 6. Conditions for revisiting

This closure is **terminal under the currently achievable seal and floor discipline**, **not** a permanent foreclosure. It could be revisited **only by separate explicit decision** and **only if** one of:

- the achievable seal grows enough to move the **weekly confirmation MDE below the expected band** under floor assumptions;
- an external benchmark is later **defended near/above the top of the band** via explicit unit-translated derivation;
- a deliberate **documented decision accepts stacked optimism** with eyes open.

**None of these conditions is met now.**

## 7. Governing anchors

**Hard-pinned anchors:**
1. Benchmark-limitation memo — `docs/lane2_ttg_magnitude_pressure_predata_benchmark_limitation_memo_v0.1.md` @ `c841f3c37762156038996460a420e537aa7cb8bb`.
2. Companion benchmark/MDE note — `docs/lane2_ttg_magnitude_pressure_long_horizon_benchmark_mde_note_v0.1.md` @ `abffe6eb7015e621f20aa0cc6d4779da8ed03865`.
3. Screen memo v0.3 — `docs/lane2_ttg_magnitude_pressure_option_a_multi_horizon_screen_design_v0.3.md` @ `ddc5c92ed2588219b4c7a8700b611022b967cf35`.

**Descriptive / unpinned references:**
- F1/F2/F3 feature-design lock;
- mechanism / extraction-design memo;
- §8a / §10 MDE machinery + §12 influence gate + two-sided floor;
- HAR-RV control-scope amendment;
- extraction authorization gate memo;
- directional TTG→SPY prereg v1.1 and directional null-result anchor.

No SHA tokens are included for the descriptive anchors; they require SHA-pin / re-verification **only if the lane is ever reopened toward a lock**.

## 8. Boundary attestation

- design arithmetic and prior-record references only;
- no repo data read;
- no row-level data;
- no feature matrix / labels / predictions;
- no SOURCEURLs;
- no raw prices / returns / OHLC;
- no GDELT/source contact;
- no 2023+ contact of any kind;
- no model fitting;
- no execution;
- this record **does not authorize** execution, feature extraction, outcome construction, 2023+ acquisition, seal contact, or any screen run;
- the preserved exploration option in §5 **requires separate explicit authorization.**
