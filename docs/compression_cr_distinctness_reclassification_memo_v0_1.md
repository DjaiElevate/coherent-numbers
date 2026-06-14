# Compression CR Distinctness / Reclassification Memo v0.1 (DRAFT; no data contact)

**DRAFT ONLY. This memo is analytical and interpretive. It does not authorize an episode-count audit, gate, wake/outcome computation, alpha spend, sealed access, or any new data contact.**

---

## 1. Anchors and current state

- **Current HEAD:** `b3ee41e6c73c2fc5008758bff729bef6ad762f02`
- **Diagnostic result commit:** `b3ee41e6c73c2fc5008758bff729bef6ad762f02`
- **Diagnostic status:** `SURVIVES FEATURE-SPACE ABSORPTION`
- **Blocked-CV joint-baseline R²:** `0.659541`
- **Script SHA-256:** `272330c5de51e0769049e50ee032efb692e926f79c9dc021ca9e982166c5c142`
- **Report SHA-256:** `b2189ae590a582706b4e60f61082f8525bf02ee3426dcf8b4d8f0d113c1ff9d4`
- **Authorization memo SHA-256:** `d4fc494d5b435798f0906d528333f793da7e34a53f930926ce8509885aca5628`
- **Stage-1 memo SHA-256:** `66c54688374c439594546b715d65211340b8680cbe055fca6736c208cea7d420`
- **Active lane count:** zero. **No episode-count audit, gate, or alpha spend is authorized.**

---

## 2. What the diagnostic established

- CR **survived** the frozen joint baseline absorption test.
- The diagnostic used **feature-side data only.**
- It computed **no wake/outcome/target.**
- It did **not** run a gate.
- It did **not** spend alpha.
- Survival does **not** prove predictive value.
- Survival permits **only a next separately-authorized artifact, not a gate.**

Key result:

`Blocked-CV joint-baseline R² = 0.659541 < 0.75`

This is a decisive survival under the frozen rule (below the `[0.75, 0.85)` borderline band), against the frozen baseline set: trailing realized volatility, the low-vol floor percentile, lag-1 autocorrelation (21/63), the Lo–MacKinlay (1988) VR5_252, and the efficiency-ratio twin ER_21.

---

## 3. What the diagnostic localized

Descriptive results (from the committed diagnostic report; descriptive only, did not change the decision):

- **ER_21 alone R²:** `0.6311`
- **Joint R²:** `0.659541`
- **Drop ER_21 joint R²:** `0.0262`
- **Pairwise corr(CI_21, ER_21):** `-0.796`

Interpretation:

- **Almost all absorbable structure comes from ER_21.** Removing ER_21 collapses the joint model to R² ≈ 0.026; the other five baselines add almost nothing beyond the efficiency-ratio twin.
- CR's survival is therefore **localized to the CR-vs-ER residual** — the part of CR not captured by net-displacement/path-length.
- This residual is **not a vague new signal; it has a specific geometry.**

> The surviving feature-space content is range/path-length in excess of net-displacement/path-length. In plain terms: full-path traversal trapped inside a finite range.

CR_21 = range/path and ER_21 = |net displacement|/path share the **same path-length denominator**; they differ only in the numerator — **spatial range (max−min)** vs **net endpoint displacement**. The surviving residual is exactly the gap between "how far the price wandered across its high-low band" and "how far it ended up from where it started," both normalized by total traversal.

---

## 4. The favorable interpretation

- CR is **not just low volatility** (it survived trailing RV and the low-vol floor percentile).
- CR is **not absorbed** by the frozen joint baseline set.
- CR survived **trailing RV, low-vol floor mechanics, autocorrelation (21/63), the strong Lo–MacKinlay VR5_252, and ER_21** under the frozen diagnostic.
- CR **sees full-path traversal** (it uses total absolute path length).
- **Range-based volatility estimators mainly see extremes** (high–low), not interior traversal.
- Therefore CR **may capture interior traversal that high-low / range-only estimators miss.**

**Illustrative example (logical, not evidentiary):**

- `Path 1: 100 → 110 → 100`
- `Path 2: 100 → 105 → 100 → 106 → 101 → 110 → 100`

- Both can have **similar high/low range** (≈100–110) and **similar net displacement** (≈0).
- **Path 2 has more internal traversal** (longer total path length).
- **CR can distinguish them** through path length (Path 2 has lower CR — more movement trapped in the same range).
- A **pure range-based estimator cannot distinguish them** if it only uses extremes.

This is the favorable reading: CR may be a genuine *interior-traversal-within-a-bounded-range* construct that the tested baselines do not span.

---

## 5. The skeptical interpretation

- CR is **range divided by path length.**
- This is **close to range-normalized tortuosity / path roughness** (the reciprocal-family of straightness/efficiency, but using spatial range as the extent term).
- **Katz fractal-dimension-style measures** also combine **path length and spatial extent / diameter.**
- CR **may be a known geometric path-complexity quantity under a new name.**
- If so, "Compression" is a **rebranding of path roughness / tortuosity, not a new force.**

> The diagnostic showed that CR is not absorbed by the volatility/autocorrelation baselines that were tested. It did not test whether CR is already a known path-roughness / tortuosity construct.

This is the crux: the first diagnostic's baseline set contained **no explicit path-roughness / fractal-dimension / tortuosity feature.** ER_21 (displacement/path) is the *closest* such feature it contained, and ER_21 already absorbed the large majority of CR's structure (R² 0.631 alone). The residual CR carries beyond ER is precisely the territory a path-roughness baseline would target — and that territory was never tested.

---

## 6. Two-sided reclassification burden

This memo must **not over-reclassify by resemblance.**

- **Do not treat resemblance as identity.**
- **Do not claim CR is Katz FD** merely because both use path length and extent.
- CR and Katz FD are **not literally identical without proof.**
- Katz FD uses a **log-wrapper** and an **`n` term** (step count).
- CR is a **direct range/path ratio** (no log, no `n`).
- The memo must distinguish:
  - **exact identity,**
  - **monotone transform,**
  - **close family resemblance,**
  - **empirical collinearity,**
  - **conceptual analogy.**

> At §8, non-identity was not enough to admit CR. Here, resemblance is not enough to reclassify CR. Reclassification must be earned, not assumed.

(The §8 reference is to the Compression Stage-1 design memo's two-sided definition kill-switch: there, *logical non-identity* was the floor, not the pass; here, by symmetry, *resemblance* to a known construct is a flag, not a verdict.)

---

## 7. CR vs Katz FD / tortuosity / path roughness

Question: is CR (A) analytically identical to a known measure; (B) a monotone transform of one; (C) close but not identical; (D) empirically likely collinear but not analytically reducible; or (E) genuinely distinct?

**Ingredient comparison.**

| Construct | Numerator / extent term | Denominator / scale term | step-count `n`? | log-wrapper? |
|---|---|---|---|---|
| **CR (this lane)** | range = max − min | total path length `Σ|Δ|` | no | no |
| **Katz FD (path)** | path length `L` | max distance / diameter `d` | yes (in normalization) | yes (`log` of ratios) |
| **Tortuosity / sinuosity** | path length `L` | net endpoint displacement | no | no |
| **Range-based volatility (e.g. Parkinson)** | high − low extremes | (window scaling) | no | (sometimes) |
| **ER_21 (efficiency ratio)** | net endpoint displacement | total path length `Σ|Δ|` | no | no |

**What CR adds or removes relative to each:**

- **vs Katz FD:** CR removes the `log`-wrapper and the explicit `n` (step-count) term, and uses **range** as the extent rather than max-distance-from-origin `d`. CR is therefore **not** an exact identity and **not** an obvious monotone transform of Katz FD (the log-wrapper and `n` break monotone-equivalence in general). → at most **(C) close** / **(D) empirically collinear**.
- **vs tortuosity/sinuosity:** tortuosity uses **net displacement** in its ratio; CR uses **range (max−min)**. Range ≥ |net displacement| always, so CR and the tortuosity/ER family are **related but not identical** — CR's numerator is the larger, extremes-based extent. → **(C)/(D)**, not (A)/(B).
- **vs range-based volatility:** those estimators use **only extremes** and **no interior path length**; CR explicitly divides by interior path length. → CR is **not** a range-volatility relabel (consistent with surviving RV in the diagnostic). → tends toward **(E) distinct from range-vol specifically.**
- **vs ER_21:** ER uses **net displacement / path**; CR uses **range / path**. Same denominator, different numerator. The diagnostic already showed ER absorbs most of CR but **not all** (joint 0.660 vs ER-alone 0.631; CR carries ~0.029 incremental over ER and survives the 0.75 bar). → **(C)/(D)** relative to the *displacement-based* efficiency family.

**Conclusion of the comparison.** CR is **not analytically identical** to Katz FD or tortuosity (it lacks the log-wrapper/`n`, and uses range not displacement), so **(A) is not established**. But CR is **clearly in the path-roughness / efficiency / fractal-dimension family by construction** (extent ÷ path length), and the most CR-adjacent member the diagnostic actually tested (ER_21) already absorbed the bulk of CR. This is exactly the **(C) close-but-not-reducible / (D) empirically-likely-collinear** zone — and it was **not tested** against an explicit path-roughness / Katz-FD / tortuosity baseline.

Per the §7 decision logic:
- **not** "analytically a monotone transform of a known path-roughness measure" → do **not** `RECLASSIFY NOW`;
- **is** "close but not analytically reducible" → **recommend a second feature-side collinearity diagnostic using explicit path-roughness / Katz-FD / tortuosity baselines**;
- "genuinely distinct even from path-roughness baselines" is **not yet shown** → episode-count audit is **not** the next step.

---

## 8. Wake-seal / precursor-framing boundary

- "Containment that resolves into expansion" is a **predictive/wake claim.**
- The current diagnostic **did not compute expansion.**
- This distinctness memo **must not validate the precursor framing by rhetoric.**
- Whether tortuosity / CR predicts later expansion is a **separate future hypothesis.**
- That future hypothesis would require **full ritual and explicit wake-authorized design.**
- It is **not authorized here.**

> Feature-side survival cannot prove the Compression story. It can only show that CR is not absorbed by the tested feature baselines. The claim that contained traversal later resolves into expansion is a wake question, and it remains unasked.

---

## 9. Recommended next step

**Recommendation: `SECOND DISTINCTNESS DIAGNOSTIC`.**

**Why this recommendation follows.** The first diagnostic established that CR is not absorbed by volatility-level, low-vol-floor, autocorrelation, variance-ratio, and displacement-efficiency (ER) baselines. But §3 localized CR's surviving content to the CR-vs-ER residual — *interior traversal in excess of net displacement, normalized by path length* — which is precisely **path-roughness / tortuosity / fractal-dimension territory**, and §7 found CR is **close to but not analytically identical** to those constructs (no log-wrapper, no `n`, range-not-displacement extent). Reclassifying now (A) would be **over-reclassification by resemblance** — forbidden by §6. Proceeding to the episode-count audit (C) would **skip the most likely absorber that was never tested** — the same mistake in reverse, admitting CR on the strength of a baseline set that omitted its nearest cousin. The disciplined middle path is to **test CR against an explicit path-roughness / Katz-FD / tortuosity baseline**, feature-side, no wake, no alpha, before any episode counting.

**Meaning of this recommendation:**
- Recommend a **second feature-side, no-wake, no-alpha collinearity diagnostic** using **explicit path-roughness / Katz-FD / tortuosity baselines** (in addition to, or alongside, the already-frozen baseline set).
- **No episode-count audit until this is resolved.**
- The second diagnostic would be **separately authorized** (its own authorization memo, frozen spec, structural firewall, pre-registered absorption threshold/borderline rule).
- Outcomes of that second diagnostic would map back to: `RECLASSIFIED — known construct` (if absorbed by path-roughness), or genuine-distinctness (which would *then* permit considering an episode-count audit, still only via separate authorization).

This memo does **not** author or authorize that second diagnostic; it recommends it.

---

## 10. Non-authorizations

- **No data contact.**
- **No code.**
- **No diagnostic.**
- **No episode-count audit.**
- **No gate.**
- **No alpha.**
- **No sealed data.**
- **No wake/outcome computation.**
- **No atlas status change yet.**

---

## 11. Boundary confirmations

- No tests were run.
- No code was written.
- No market data was opened.
- No modeling/tuning was run.
- No gate, audit, or synthetic-null check was run.
- No wake/outcome/target was computed.
- No sealed data was accessed.
- This memo is analytical/interpretive only; it freezes nothing and authorizes nothing.
