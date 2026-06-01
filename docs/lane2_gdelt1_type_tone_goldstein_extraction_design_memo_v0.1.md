# Lane 2 — Type / Tone / Goldstein Extraction Design Memo (v0.1)

## 1. Title and status

**Document type:** Design memo / **lock-candidate**. Pre-registration draft for a future, separately-gated GDELT Event-field extraction and analysis.

**THIS IS NOT AN EXECUTION AUTHORIZATION.** This memo defines a mechanism, a primary feature composite, a primary outcome, and the methodological guards that a future analysis must obey. It authorizes **nothing**: no GDELT contact, no extraction, no feature build, no join, no outcome computation, no result generation, no implementation, no staging, no commit, no push. A later, **separately initiated execution-authorization prompt** is required before any data contact or any irreversible step. Until that prompt is issued and its own conformance gate passes, this memo is inert design text.

| Field | Value |
|---|---|
| Date of draft | 2026-06-01 |
| Lane 2 source-of-truth HEAD at drafting | `219f37c` (divergence record memo) |
| Governing prior records | `219f37c` (divergence record), `cb1122a` (Step 2 daily feature tracking), prior SQLDATE / row-date characterization decision |
| Status | DESIGN-ONLY / LOCK-CANDIDATE — not authorizing |
| 2023+ OOS seal | Sealed; this memo keeps it sealed |
| Mechanism locked | Intensity / valence pressure (NOT amount) |
| Primary outcome | `abs(next_session_return)` |

---

## 2. Background

- **`219f37c` (divergence record).** The post-`cb1122a` arc executed, in two commits of "plain scripts" (`4f31bcb`, `6a75ec7`), three steps the prior project record tracked as unopened gates: market-data acquisition execution, join implementation/execution, and instrument/outcome construction (the next-session-return join). That arc ran with **no execution-authorization guard** and produced **none** of the per-execution conformance deliverables the design memos (`df9089b`, `21c87c1`) required. It is capped **EXPLORATORY-ONLY**. The breach was governance, not contamination: the data boundaries that would have been fatal (2023+ seal, no-lookahead, exact schema) were honored.
- **Volume-only first-pass result.** The exploration arc (`6a75ec7`) ran a wide Spearman scan → confound probe (partial-time + detrend + per-year) → detrended confirmation. `|next_session_return|` correlated with GDELT volume/coverage features at ρ ≈ −0.15 to −0.18, but the association **dissolved under drift removal**. Recorded as a **clean exploratory NULL**: no clear next-session SPY direction or magnitude relationship after removing drift.
- **2023+ seal intact.** The 2013–2022 window is the only window ever read; 2023+ was never fetched, read, or sampled. The seal remains recorded as intact.
- **Step 2 inventory (2026-06-01, read-only).** The 69-column Step 2 table `results/lane2_gdelt1_step2_daily_features/20260531T020244Z/step2_daily_features.csv` is **volume/coverage only**: 54 volume-or-coverage columns, 14 structural/status columns, 1 date/key column, and **0** EventCode/QuadClass-derived, **0** GoldsteinScale-derived, **0** AvgTone-derived columns. The Step 2 generator source (`src/lane2_gdelt1_step2_features.py`) contains **zero** references to `EventCode`, `QuadClass`, `GoldsteinScale`, `AvgTone`, `Actor`, `NumMentions`, `NumSources`, `NumArticles`, `tone`, `sentiment`, or `impact`.
- **No re-analysis path.** The prior exploration consumed essentially the full informative surface of the volume substrate — all 51 numeric volume/coverage features. There is **no "missed volume feature" path** and **no re-analysis path** for type/tone/Goldstein. The type/tone/Goldstein branch is **scientifically distinct** and requires a **fresh extraction from GDELT Event fields**, which must be separately gated.

---

## 3. Scientific mechanism

**Locked mechanism: intensity / valence pressure, not amount.**

The volume-only hypothesis ("more news → market movement") is exhausted in-sample as far as exploration can exhaust it. This memo locks a different mechanism: at **equal total news volume**, the market may respond to the **kind of collective news pressure** present — specifically material conflict, negative structural impact, and negative tone — rather than to raw coverage amount.

Why this is distinct from volume-only attention: two days can carry the same number of GDELT rows yet differ entirely in character. A deadly-virus emergence, a war escalation, or a wave of material-conflict events is not equivalent to an equal-volume day of low-impact procedural or payment-dispute coverage. Volume counts treat those days as interchangeable; an intensity/valence measure does not. The mechanism asserts that *what* the news pressure is — its conflict content, its structural-impact sign, its tone sign — carries information that raw amount cannot, **conditional on amount being held fixed**.

The expected market response is **pressure/magnitude**, not signed direction. Negative-valence collective pressure is hypothesized to enlarge next-session realized movement (in either direction), not to predict its sign.

---

## 4. Primary hypothesis

**Operational primary hypothesis:**

> Higher intensity/valence pressure predicts higher next-session market magnitude after controlling for volume/coverage amount and for drift.

- **Primary target:** `abs(next_session_return)` (next-session magnitude / pressure).
- **Signed direction is NOT the primary hypothesis.** `next_session_return` (signed) is excluded from the primary confirmatory target. It may appear only as a non-primary descriptive check; it must not become a co-primary target.
- The hypothesis is explicitly an **incremental-over-volume** claim: the composite must add information **beyond** the amount of news, after drift control (see §9). A relationship that survives only without volume control does not satisfy the primary hypothesis.

---

## 5. Source fields required

The primary extraction must consume **only** the fields the locked composite needs:

1. **Event date / daily attribution field** required by the project's locked row-date rule (e.g. `SQLDATE` or the project's established event-date field — see §10/date-attribution premise).
2. `QuadClass`
3. `GoldsteinScale`
4. `AvgTone`
5. `NumMentions`

**Exact source schema availability (column presence, types, value ranges, units, GDELT 1.0 field positions) must be verified in a later, gated pre-execution step.** This memo does not assert the schema; it specifies the minimal field set conditional on schema confirmation.

**Explicitly out of scope for the primary design:** `EventCode`, `EventBaseCode`, `EventRootCode`. These create a large scannable surface and must **not** be extracted or retained "just in case." They may enter only via a future named extension that pre-registers their exact use.

`NumArticles` and `NumSources` are **not** primary fields. They may be named only as non-primary sensitivity candidates or future extensions (see §6 coverage-weight note).

---

## 6. Feature set

### Coverage weight (locked)

**Primary coverage weight: `NumMentions`.** Rationale: `NumMentions` represents mention intensity attached to event records — closer to "how much attention this event received" than a simple row count. `NumArticles` (article breadth) and `NumSources` (source breadth) measure related but different concepts and are listed only as **non-primary** sensitivities / future extensions, never as co-primary coverage weights.

### Three primary components (mechanism-derived, not scanned)

All three are computed **daily**, aggregated to the event's established daily information date (§10), and **coverage-normalized** by a daily coverage denominator (the daily total of the chosen coverage weight) so that none collapses back into raw volume:

1. **Material-conflict pressure** — based on `QuadClass = 4` (material conflict). A coverage-normalized daily **share/intensity** measure (e.g. `NumMentions`-weighted share of material-conflict events in the day's total `NumMentions`), **not** a raw count.
2. **Negative structural-impact pressure** — based on `GoldsteinScale`. Use negative magnitude `max(0, -GoldsteinScale)`, weighted by the chosen coverage weight (`NumMentions`), and **normalized by the daily coverage denominator** so it does not reduce to raw volume.
3. **Negative-tone pressure** — based on `AvgTone`. Use negative-tone magnitude `max(0, -AvgTone)`, weighted by `NumMentions`, and **normalized by the daily coverage denominator**.

### Single primary composite

- `intensity_valence_pressure` — the single primary statistic: compute the three normalized pressure components daily, standardize each by a pre-specified leakage-safe method (§8/§16), and **combine with equal weights** into one composite.

### Explicitly excluded (no open-ended scanning)

The design **forbids** scanning across:
- all `EventCode` values;
- all `EventRootCode` / `EventBaseCode` values;
- arbitrary tone thresholds;
- arbitrary `GoldsteinScale` bins;
- arbitrary `QuadClass` groupings/combinations;
- arbitrary rolling windows;
- arbitrary coverage weightings.

One composite is the primary evidence. The three components are secondary/descriptive (§12, §13, §14).

---

## 7. Negative-pressure assumption

The primary composite is, by construction, a **negative-pressure composite**: material conflict (`QuadClass = 4`), negative Goldstein magnitude (`max(0, -GoldsteinScale)`), and negative tone (`max(0, -AvgTone)`).

This **pre-excludes positive-valence / euphoria pressure** from the primary hypothesis. The primary claim is about negative collective pressure only.

Symmetric or absolute-pressure alternatives — e.g. `abs(GoldsteinScale)`, tone extremity / `abs(AvgTone)`, or a two-sided intensity measure — are named **only as non-primary sensitivities or future hypotheses**. They must **not** become co-primary tests in this memo. A finding under a symmetric/absolute alternative is exploratory and would require its own pre-registration.

---

## 8. Normalization discipline

- **Why raw sums are dangerous:** raw daily sums of mentions, conflict events, or negative-magnitude pressure scale with the **amount** of news and with the secular GDELT coverage growth across 2013–2022. Using raw sums would **reintroduce the very volume/regime drift** that produced the volume-only null. The components must therefore be **coverage-normalized** (share-style / intensity-style), dividing by the daily coverage denominator.
- **Leakage-safe standardization required:** any standardization (centering/scaling) must use only information available strictly before the outcome and, where rolling, only trailing history (no use of the current or future days in the statistic that is then correlated with the current day's outcome). See §16 for the OOS-frozen-parameter rule.
- **Warmup / history rule:** if rolling normalization is used, a clear warmup/history rule must be pre-specified (e.g. require a minimum trailing window before a normalized value is considered valid), mirroring the Step 2 warmup discipline.
- **Normalization is necessary but not sufficient:** coverage-normalization alone does **not** prove independence from volume. The **incremental-over-volume test (§9)** is a separate, required step.

---

## 9. Incremental-over-volume test (primary methodological requirement)

This test is **required** and is part of the primary evidence.

- The future primary statistic must test whether `intensity_valence_pressure` explains `abs(next_session_return)` **after controlling for a small, pre-specified volume/coverage control set** — i.e. it must show **incremental** information beyond the amount of news, not merely a marginal association.
- **Drift control vs. volume control are separate confounds and both must be addressed:**
  - **Drift control** removes time / regime trend (§11).
  - **Volume control** removes "amount of news."
  - Satisfying one does not satisfy the other; the primary analysis must address **both**.

### Pre-specified volume-control set (narrow)

Use a **small** control set — **not** all 54 volume/coverage features — to avoid overfitting and to avoid stripping real signal. Proposed narrow set:

- `log1p_total_row_count` — overall daily amount;
- `roll_mean_log1p_total_w30` — one local/regime volume baseline term;
- `coverage_completeness` — one coverage-quality term.

These three column names were observed present in the Step 2 table during the 2026-06-01 read-only inventory, **but must be re-verified at the future execution/analysis gate before use** (exact names, semantics, and availability). The control set must **not** be expanded into a broad scan, and **volume controls must not be selected post-hoc based on result strength** (§9 prohibition, restated in §12).

---

## 10. Outcome and timing

- **Primary outcome:** `abs(next_session_return)`.
- **No look-ahead:** the feature date must strictly precede the outcome session, consistent with the prior no-lookahead invariant (outcome session strictly after the feature information date).
- **Date-attribution premise (locked, not redesigned here):** the extraction must aggregate event content to the event's **already-established daily information date** using the project's previously locked row-date / SQLDATE logic. This memo references that decision as a **locked premise**, not as something to redesign. Introducing a new date definition is out of scope.
- **No 2023+ read** unless a later OOS gate explicitly authorizes unsealing (§15, §16).
- **Firewall the steps:** content extraction and outcome join must be kept **separate**. The content extraction must be **completed and pinned** before any future outcome join. The analysis pre-registration must be **committed** before any future outcome join (§20).

---

## 11. Drift-control plan

- **Carry forward the volume-null lesson:** raw pooled correlations are insufficient; the volume-only ρ ≈ −0.15…−0.18 vanished under drift control. The type/tone/Goldstein analysis must assume the same trap exists.
- **Pre-specify the drift-control method before any result computation.** Use the now-known detrend / partial-time / per-year logic as a **fixed** method, written as a locked procedure — **not** an exploratory choice made after seeing results.
- **Planted-signal sensitivity check (required):** before trusting any null, run a synthetic / planted-signal check — inject a known signal of reasonable strength into a surrogate and confirm the drift-control procedure **recovers** it. This guards against an over-aggressive drift control that erases real structure.
- **Disambiguation requirement:** a future null must **not** be ambiguous between "no signal" and "drift control too aggressive." The planted-signal check is what resolves that ambiguity; it must be specified and run as part of the gate.

---

## 12. Multiple-comparisons discipline

- The type/tone/Goldstein branch has **higher forking-path risk** than the volume branch (more candidate fields, thresholds, weightings, windows).
- **One primary composite statistic** (`intensity_valence_pressure`) is the main test.
- The three component features are **secondary / descriptive** unless a **named correction method is chosen in advance**.
- A **broad feature scan must not become the primary evidence.** Post-hoc selection of volume controls or components based on result strength is prohibited.

---

## 13. No-rescue rule

- If the **primary composite is null** but one **component appears strong**, that component result is **exploratory only**.
- A strong component under a null composite may **motivate a future pre-registration**, but it does **not** rescue or overturn the primary null.
- **No post-hoc reinterpretation** of a component as the "real" primary test. The primary test is the composite, fixed in advance.

---

## 14. Component collinearity reporting

- Require a **descriptive component correlation matrix** among:
  - material-conflict pressure;
  - negative structural-impact pressure;
  - negative-tone pressure.
- This matrix is **interpretive only**, not a primary result.
- **Purpose:** determine whether the composite is genuinely multidimensional or is mostly a single negativity/conflict dimension (which would change how the composite should be read, but not the primary verdict).

---

## 15. OOS / in-sample posture

- **2013–2022 is exploration-spent for the volume-only question.** It has been looked at; in-sample "confirmation" of the volume-only relationship would be circular.
- The **type/tone/Goldstein feature family is scientifically distinct** (new fields, never extracted) but requires careful gating because it shares the same in-sample window.
- **This memo keeps 2023+ sealed.**
- **Frozen standardization for any future OOS:** all scaler / threshold / normalization-denominator parameters must be learned from the in-sample (pre-OOS) window only and frozen, never re-fit on 2023+ (see §16).
- A future **2023+ confirmatory test remains closed-but-openable only after** all of:
  - feature definitions are locked;
  - analysis is pre-registered (and committed);
  - an execution guard exists (§18);
  - conformance artifacts are specified (§19);
  - an explicit **unsealing authorization is committed**.

---

## 16. Frozen standardization for future OOS

- If any future OOS confirmation is authorized, **all standardization parameters must be learned from the pre-OOS / training window only and frozen**: means, standard deviations, scalers, thresholds, normalization denominators/parameters.
- **Do not refit** any of these on 2023+ data.
- Carry the **frozen parameters into the holdout unchanged**.
- Rationale: refitting on OOS would **leak holdout distribution information** into the test and invalidate it.

---

## 17. Magnitude sensitivity candidates

- **Primary target remains `abs(next_session_return)`.**
- Realized range, squared return, or similar magnitude/volatility proxies are named **only as non-primary sensitivity candidates or future extensions**.
- They must **not** become co-primary targets in this memo.

---

## 18. Execution boundary and guard

- Any future type/tone/Goldstein extraction is a **fresh data-contact step** (the first irreversible step for this branch).
- It requires an **execution-authorization guard** analogous to `STEP2_EXECUTION_AUTHORIZED`:
  - the guard must **exist before** extraction execution;
  - it must be set **explicitly only for the authorized run**;
  - it must be **restored in a `finally`** block so the default state is inert.
- This directly addresses the governance gap documented in `219f37c` (the prior arc ran with no guard and avoided harm by luck, not by control).

---

## 19. Required future conformance artifacts

A future execution gate must require, at minimum:

- pre-execution conformance verdict;
- boundary declaration;
- source-field schema confirmation (the §5 fields verified against the actual source);
- extraction manifest;
- metadata JSON;
- artifact SHA-256(s);
- row-count / date-range summary;
- a **no-2023+ proof** (or, only if explicitly authorized, an explicit **2023+ unsealing proof**) appropriate to the authorized scope;
- post-run **guard-restoration proof** (guard back to inert);
- `git status` proof (clean / expected tree).

---

## 20. Firewall ordering

1. **Content extraction first** — must **not** touch any outcome / market data.
2. The extracted type/tone/Goldstein **feature table must be pinned** (SHA-pinned) before any outcome join.
3. **Outcome join comes only after** the analysis design is committed (pre-registered).
4. **Analysis computation comes only after** the joined design is authorized.
5. **Do not repeat the prior build-and-join fusion** that `219f37c` documents (the ungated acquisition+join arc).

---

## 21. Artifact policy (recommendation only)

- A future, properly-gated **type/tone/Goldstein extracted feature table** should be **committed with SHA** — it becomes a canonical analysis input.
- A future **outcome-joined table** should remain **untracked-by-policy** as a regenerable derived artifact, unless a separate gate authorizes commit-with-SHA treatment (consistent with the `gdelt_spy_nextday.csv` policy in `219f37c`).
- **Do not modify `.gitignore` in this step.**
- This artifact policy is a **recommendation only** until separately committed.

---

## 22. Non-authorizations

This memo explicitly does **NOT** authorize, and nothing in it permits:

- no GDELT contact;
- no raw event-file read;
- no extraction;
- no feature build;
- no 2023+ read;
- no market-data join;
- no outcome computation;
- no result scan;
- no re-run of the volume-only analysis;
- no implementation;
- no execution;
- no staging;
- no commit;
- no push.

---

## 23. Open decisions / next gate

**Open design decisions left for the next review (not resolved here).** Decisions 1–4 are **LOCKS REQUIRED BEFORE THE EXTRACTION GATE** — each must be resolved to a single fixed choice and committed before any execution-authorization prompt may open; an extraction gate must not proceed while any of them is open. Decisions 5–6 are gate-time verifications. Decision 7 is resolved below.

1. **[LOCK REQUIRED BEFORE EXTRACTION GATE]** **Exact coverage-denominator definition** — whether the daily normalization denominator is total daily `NumMentions`, total daily event rows, or another fixed quantity. To be locked before extraction (one fixed choice, no scan).
2. **[LOCK REQUIRED BEFORE EXTRACTION GATE]** **Exact daily share/intensity formula** for material-conflict pressure (mention-weighted share vs. mention-weighted intensity) — pick one, fix it.
3. **[LOCK REQUIRED BEFORE EXTRACTION GATE]** **Standardization method specifics** — exact leakage-safe scaler and rolling-warmup thresholds (§8/§16) to be pinned as a fixed procedure.
4. **[LOCK REQUIRED BEFORE EXTRACTION GATE]** **Drift-control method specifics** — the fixed detrend / partial-time / per-year recipe and the planted-signal strength/threshold for the §11 sensitivity check.
5. **Volume-control column names** — re-verify `log1p_total_row_count`, `roll_mean_log1p_total_w30`, `coverage_completeness` against the Step 2 table at the gate (§9).
6. **GDELT 1.0 field positions / schema** — confirm `QuadClass`, `GoldsteinScale`, `AvgTone`, `NumMentions`, and the date field positions and value ranges (§5).
7. **OOS scope — RESOLVED:** 2023+ is **strictly sealed in v0.1**. OOS unsealing is **not** decided here; it is a **separate, separately-authorized decision, out of scope for this memo**, and may be taken only after the §15 preconditions are met and an explicit unsealing authorization is committed.

**Next required step after review of this memo:** either

- **commit this memo as design-only** (no implementation, no execution), or
- **revise it before commit**.

**Do not proceed to implementation or execution.** The next substantive gate beyond committing this memo is a **separately initiated execution-authorization prompt** with its own preflight, guard, and conformance artifacts (§18, §19).

---

*Filed as a design-only lock-candidate. It defines a mechanism (intensity/valence pressure, not amount), one primary composite (`intensity_valence_pressure`), one primary outcome (`abs(next_session_return)`), and an incremental-over-volume + drift-control discipline. It authorizes no data contact. The 2023+ seal remains intact.*
