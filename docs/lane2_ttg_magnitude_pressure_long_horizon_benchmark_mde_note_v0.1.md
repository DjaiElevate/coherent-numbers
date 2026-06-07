# Lane 2 TTG Magnitude-Pressure — Long-Horizon Benchmark + Per-Horizon Confirmation-Viability Note v0.1

## Status

- **Status:** DRAFT / pre-execution / companion to Option A screen memo v0.3.
- **Value-safety:** external-literature characterization + design arithmetic + structural calendar trading-day counts only.
- **Provenance:** drafted pre-execution; no data contact; no execution; no 2023+ contact.
- This note **scopes the decision and authorizes nothing**: no 2023+ acquisition, no seal contact, no feature extraction, no outcome construction, no model fitting, no execution.
- This note is a **record of viability arithmetic, not a preregistration**. It locks no benchmark, no threshold, and no run.

## 0. Purpose and structure

This note decides, **before** any screen is locked, which next-session-magnitude horizons could in principle support a *confirmable* long-horizon preregistration on the **achievable 2023+ seal**, and which cannot. The companion Option A screen memo v0.3 inherits this scoping.

Structure:
- **Part A** supplies a *soft external prior* for the expected incremental effect size. It is translated/approximate and **does not carry the go/no-go**.
- **Part B** computes the *per-horizon confirmation MDE* on the achievable 2023+ seal. **Part B carries the decision**, because the minimum detectable effect (MDE) — not the soft prior — dominates the horizon-viability question: a horizon whose best-case MDE exceeds any plausible effect cannot host a confirmable prereg regardless of the prior.

## Part A — External benchmark (soft prior; not locked)

The external literature is characterized here only at **source-description level**. Exact effect sizes are **not** imported; native units of these studies do not convert directly to the present design's incremental-over-HAR-RV partial-Spearman ρ. These are anchors for plausibility, not locked numbers.

- **Tetlock (media pessimism):** foundational work linking daily media pessimism to price pressure and trading volume. It is a daily-frequency, price-pressure/volume result and is **not** a clean long-horizon magnitude benchmark; it does not provide an after-HAR-RV partial ρ.
- **Kräussl & Mirgorodskaya:** relevant to long-run media pessimism, market performance, and volatility. Its native units (returns/volatility associations in its own framing) **do not convert directly** to an incremental-over-HAR-RV partial Spearman ρ.
- **Hsu (news-sentiment volatility modeling):** relevant because news sentiment enters volatility models; its native units are **model coefficients / forecast-improvement metrics**, not a partial ρ.

From these, the soft prior for a small-to-moderate incremental effect is taken as a **band**, not a point:

> `rho ≈ 0.10–0.15` is a **soft prior / plausible small-to-moderate band, not a locked threshold.**

Any future prereg that needs a **hard** benchmark must **re-derive it explicitly** with proper unit-translation from source text; this note does **not** lock that derivation.

## Part B — Per-horizon confirmation MDE on the achievable 2023+ seal (hard gate)

MDE is computed via the Fisher-z convention used throughout the magnitude design:

```
rho_MDE = tanh[ (z_0.95 + z_0.80) / sqrt(N_eff - k - 3) ],   with z_0.95 + z_0.80 ≈ 2.487
```

- The arithmetic is **optimistic** wherever it uses **one-sided α** and **non-overlap / favorable-overlap** assumptions. Realistic overlap and per-day eligibility deflation only **enlarge** the MDE.
- Trading-day counts below are **structural planning approximations**, not data reads or coverage probes. The achievable out-of-sample (2023+) seal is taken as **~800 raw trading days** for planning purposes (~3+ years of 2023+ availability), which is itself uncommitted and would require a separate source-freeze/acquisition decision.
- `k` is the control count for the horizon's ratified partial set (HAR-RV + non-RV controls); the `N_eff − k − 3` denominator follows the committed Fisher-z form.

### Daily h=1
- **Closed by the prior §8a viability gate** (benchmark-limitation memo). The daily next-session confirmation is nonviable; it is **not reopened** here.

### Weekly h=5
- ~800 trading days → **non-overlap floor ≈ 160 weekly observations** (800 / 5).
- **Floor MDE ≈ `rho ≈ 0.20`** (non-overlap, even with one-sided α).
- **Best-case / favorable-overlap MDE may approach `rho ≈ 0.14–0.15`** (treating overlapping weekly windows as adding effective information up to a favorable efficiency ceiling).
- **Verdict:** `weekly is nonviable under floor assumptions; borderline only under stacked optimism`.
- **Stacked optimism** = **top-of-band expected effect (≈0.15) plus favorable overlap efficiency** simultaneously. Only when *both* optimistic assumptions hold does the weekly MDE approach the top of the soft band.

### Monthly h=21
- ~800 trading days → **non-overlap floor ≈ 38 monthly observations** (800 / 21).
- **MDE ≈ `rho ≈ 0.43–0.45`**; even generous overlap/efficiency assumptions remain **far above** the soft band `0.10–0.15`.
- **Monthly is nonviable and exploratory-only.** Monthly is **not a prereg target.**

## Verdict table

| Horizon      | Expected effect status     | Seal N_eff logic   | Approx MDE                                        | Verdict                                                                   |
| ------------ | -------------------------- | ------------------ | ------------------------------------------------- | ------------------------------------------------------------------------- |
| h=1 daily    | already nonviable / closed | daily seal         | prior §8a                                         | closed                                                                    |
| h=5 weekly   | soft plausible band        | ~800/5 ≈ 160 floor | ~0.20 floor; ~0.14–0.15 best case                 | nonviable under floor assumptions; borderline only under stacked optimism |
| h=21 monthly | soft plausible band        | ~800/21 ≈ 38 floor | ~0.43–0.45; still high under generous assumptions | nonviable / exploratory-only                                              |

## Conclusion and routing

- **Monthly (h=21):** nonviable / exploratory-only. Not a prereg target.
- **Daily (h=1):** closed (prior §8a). Not reopened.
- **Weekly (h=5):** the **sole conceivable** prereg target, but **not accepted** under the project's floor-assumption discipline — under floor assumptions the weekly MDE (~0.20) exceeds the soft band, so a normally-sized weekly effect could not be confirmed.
- **Default decision:** **no-spend / pure exploration.** No 2023+ seal is acquired or spent on this evidence.
- A **prereg-triggering screen** would require a **separate explicit future decision** that affirmatively accepts **optimistic overlap efficiency plus a top-of-band expected effect** — i.e. it must consciously adopt the stacked-optimism regime.
- This note does **not** authorize 2023+ acquisition, seal contact, feature extraction, outcome construction, model fitting, or execution.

## Governing anchors

**Hard SHA-pinned (the only pin in this note):**
- Benchmark-limitation memo — `docs/lane2_ttg_magnitude_pressure_predata_benchmark_limitation_memo_v0.1.md` @ `c841f3c37762156038996460a420e537aa7cb8bb`. Supplies the §8a daily-horizon nonviability that closes h=1 and the kill-test convention reused here.

**Descriptive / unpinned (NOT SHA-pinned in this draft; require SHA-pin / re-verification before any future lock):**
- F1/F2/F3 pressure-feature lock (mention-share composite, common `NumMentions` denominator, equal-weight, expanding past-only z, per-day Kish floor) — *unpinned in this draft.*
- §8a / §10 MDE machinery (Fisher-z, k, power, two-sided detectability floor) — *unpinned in this draft.*
- HAR-RV control-scope amendment (trailing-RV controls; `N_eff − 9` at-join form) — *unpinned in this draft.*
- Extraction authorization gate memo — *unpinned in this draft.*
- Directional TTG→SPY prereg v1.1 and directional null-result anchor — *unpinned in this draft.*

These descriptive references are intentionally left unpinned; any move from draft to lock must SHA-pin and re-verify them.

## Boundary attestation

No data contact; no 2023+ contact; no acquisition; no seal contact; no raw market data; no row-level data; no feature matrix / labels / predictions; no SOURCEURLs; no raw prices / returns / OHLC; no GDELT/source contact; no model fitting; no feature extraction; no outcome construction; no execution. All effect-size figures are external/literature characterizations and design-only arithmetic; all trading-day counts are structural planning approximations, not data reads or coverage probes. This note authorizes nothing.
