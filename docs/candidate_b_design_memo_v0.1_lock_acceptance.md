# Candidate B Design Memo v0.1 Lock Acceptance

**Artifact type:** Lock-acceptance ratification
**Date:** 2026-05-15
**Project:** Coherent Numbers
**Cell:** Candidate B — pullback × harmonic-calendar modulation

---

## 1. Title

Candidate B Design Memo v0.1 Lock Acceptance.

## 2. Status

This artifact ratifies the design memo at commit `1e9a3e6` as the **locked Candidate B protocol**. Prior to this artifact, the design memo at `docs/candidate_b_design_memo_v0.1.md` was a pre-registration draft. As of the commit that records this artifact, the design surface specified in that memo — population scope, schema, calendar lens, primary outcome, nulls, controls, verdict map, disclosure wording, seeds, and substrate clause — is closed to revision without a separate, dated amendment artifact.

The wording "draft for review — final tightening pass" and "Pre-registration draft. Protocol not yet locked." inside the memo file itself is preserved as the historical state at commit `1e9a3e6`. The locked status is conferred by **this artifact** and the commit that records it, not by retroactive edits to the memo file.

## 3. References

- **Design memo file:** `docs/candidate_b_design_memo_v0.1.md`
- **Design memo commit:** `1e9a3e6` ("Add Candidate B design memo draft (v0.1): pullback × harmonic-calendar modulation")
- **Freeze commit:** `5225bfd` ("Freeze imported pullback trade populations")
- **Freeze manifest:** `docs/pullback_population_freeze_manifest_v0.1.md`
- **v0.2 selection memo commit:** `5c30f5d` ("Add Cell-Selection Decision Memo (v0.2): select Candidate B (pullback × harmonic calendar)")
- **Pullback repo HEAD at inventory/freeze time** (historical, not run-substrate): `eac925c`

## 4. Verification of pre-lock checklist (§17 of the design memo)

Each §17 item is quoted verbatim from `docs/candidate_b_design_memo_v0.1.md` at commit `1e9a3e6`, marked verified, and supported by named evidence.

### 4.1 Working tree clean of non-ignored modified/untracked files

> **Working tree is clean of non-ignored modified or untracked files.** Files covered by `.gitignore` may exist locally but are not part of the audit state.

**Verified.** Evidence: `git status --short --untracked-files=all` at lock-acceptance time produced empty output. The design memo file at `docs/candidate_b_design_memo_v0.1.md` matches the HEAD commit `1e9a3e6` exactly (`git diff --quiet HEAD` returned clean; `git log -n 1 --format='%H %s' -- docs/candidate_b_design_memo_v0.1.md` returned `1e9a3e64ef8be8e70fc5f5abbf703882a78d976d`).

### 4.2 Frozen-CSV manifest present and intact

> Frozen-CSV manifest from commit `5225bfd` is intact; all referenced CSVs are present and digests match.

**Verified.** Evidence:

- The manifest `docs/pullback_population_freeze_manifest_v0.1.md` is present and readable, with six population rows and all source/destination SHA256 columns marked `✓`.
- `shasum -a 256` was recomputed on each destination CSV. Each computed digest matches the manifest:

| Destination CSV | Manifest SHA256 | Recomputed SHA256 | Match |
|---|---|---|---|
| `data/raw/pullback_spy_base_301_trades_2000_2022.csv` | `b7817e0e7a02dad44923eae462c1454ab67b8fbc73539b36b81e043d8dcc2d06` | `b7817e0e7a02dad44923eae462c1454ab67b8fbc73539b36b81e043d8dcc2d06` | ✓ |
| `data/raw/pullback_phase3b_spy_trades_2005_2022.csv` | `1d8a7b77389835a7231d6ca0742e39d963cf4dc03f822b0111039b5c19383621` | `1d8a7b77389835a7231d6ca0742e39d963cf4dc03f822b0111039b5c19383621` | ✓ |
| `data/raw/pullback_phase3b_efa_trades_2005_2022.csv` | `275af7e00f28a2a72d948228964c7a4658444f0030ac048e8a2851bc3313de82` | `275af7e00f28a2a72d948228964c7a4658444f0030ac048e8a2851bc3313de82` | ✓ |
| `data/raw/pullback_phase3b_eem_trades_2005_2022.csv` | `56cf8e5fe88f5230ebb8e2881f4df1e0ff633819d588764d9e9e57bbdebb6916` | `56cf8e5fe88f5230ebb8e2881f4df1e0ff633819d588764d9e9e57bbdebb6916` | ✓ |
| `data/raw/pullback_phase3b_gld_trades_2005_2022.csv` | `0de7bf6dd981be8d8091a382a6dc0af594a59fa8d87f459305ad25f9dc21d1e3` | `0de7bf6dd981be8d8091a382a6dc0af594a59fa8d87f459305ad25f9dc21d1e3` | ✓ |
| `data/raw/pullback_phase3b_tlt_trades_2005_2022.csv` | `037ea4178bd071e426d7cce30eeaffb554ae31d7998c8d00d5e2ba36a7388abc` | `037ea4178bd071e426d7cce30eeaffb554ae31d7998c8d00d5e2ba36a7388abc` | ✓ |

No row-level inspection was performed; only filesystem-level SHA256 was computed.

### 4.3 Reduced row schema is final

> Reduced row schema (§5) is final; `source_sha256` is dataset-level only.

**Verified.** Evidence: §5 of the design memo lists exactly seven per-row fields — `trade_id, asset, entry_date, exit_date, is_long, r_multiple, frozen_artifact_id` — and explicitly states "`source_sha256` is **dataset-level provenance**, recorded once per frozen CSV in the freeze manifest. It is not a per-row analytical field." The freeze manifest carries `source_sha256` at the dataset row, not at trade level.

### 4.4 §7 annual-sector formula present; no `% 12` day-residue logic for Candidate B's lens

> §7 phase formula is the **annual-sector** formula; no `% 12` day-residue logic appears anywhere in the memo or in code.

**Verified, within the corrected verification scope.** Evidence:

- §7.1 specifies the annual-sector formula: locate `cycle_start` as March 20 of the relevant year, compute `cycle_length_days`, `days_since_start`, then `phase = floor(days_since_start * 12 / cycle_length_days)`. No `%` operator appears in the assignment.
- The memo's only three occurrences of `% 12` (lines 98, 188, 316) are **explicit negations**: "There is no `% 12` day-of-year residue" (§7.2), "No `% 12` residue logic appears anywhere" (§10.2), and the §17 checklist line itself.
- Scope correction acknowledged: this verification covers the Candidate B design memo only. Existing source files belonging to prior cells (`src/harmonic_calendar.py`, `src/harmonic_calendar_protocol.py`, `src/spy_loader.py`, `src/gld_loader.py`) are not Candidate B implementation and are not subject to Candidate B's lens-arithmetic constraints.
- No Candidate-B-specific implementation file exists yet (see §4.6 below), so there is no code surface on which a Candidate-B `% 12` rule could be violated at this stage.

### 4.5 Phase-range check is assertion-and-abort, not silent clamp

> The §7.1 step-3 phase-range check is implemented as an **assertion that aborts the run** on failure, not as a silent clamp.

**Verified.** Evidence: §7.1 step 3 reads "**Assert** `phase ∈ {0, 1, ..., 11}`. If the assertion fails, the run **aborts**. There is no silent clamp." (line 90). §10.2 step 3 inherits the same discipline for `phase_d`: "Assert `phase_d ∈ {0..11}`; abort on assertion failure (same discipline as §7.1 step 3)." (line 184).

### 4.6 No Candidate-B-specific implementation/output files exist yet

**Verified.** Evidence:

- `find . -type f -iname "*candidate_b*"` returned a single hit: `./docs/candidate_b_design_memo_v0.1.md` (the memo itself).
- `grep -l -iE "candidate[_ -]?b|PSS_B1|LABEL_PERM_SEED|ASSET_STRAT_DIAG_SEED"` across `src/`, `tests/`, `scripts/`, `notebooks/`, `results/` returned no matches.
- No `candidate_b_*.py`, no Candidate-B-specific test files, no Candidate-B output logs, no Candidate-B derived data, no Candidate-B notebooks exist.

The lock-acceptance commit therefore precedes any Candidate B implementation.

### 4.7 §9.1 PSS_B1 η²/correlation-ratio form with `total_B1 = 0` abort rule

> §9.1 `PSS_B1` is the η²/correlation-ratio form `between_B1 / total_B1`, with the `total_B1 = 0` abort rule in force.

**Verified.** Evidence: §9.1 defines `between_B1 = Σ_p (N_p/N_total) (share_p − share_pooled)²`, `total_B1 = share_pooled (1 − share_pooled)`, `PSS_B1 = between_B1 / total_B1`. The degenerate-population abort rule is at line 141: "If `total_B1 = 0` — i.e., the pooled population contains only longs or only shorts — allocation heterogeneity is undefined. In that case the run **aborts** … No fallback estimand is substituted."

### 4.8 N.1 unstratified label permutation across pooled 1,282 Phase 3b trades

> N.1 is **unstratified** label permutation across the pooled 1,282-trade Phase 3b population (§10.1).

**Verified.** Evidence: §10.1 step 2: "Independently and uniformly shuffle the `is_long` label across **all 1,282 trades, ignoring asset**." `N_PERM = 10,000` and `LABEL_PERM_SEED = 20260514` are stated. Asset-stratified permutation is explicitly demoted to a §11.3 diagnostic.

### 4.9 N.2 exhaustive 365-DOY anchor control under the annual-sector formula

> N.2 uses the §7 annual-sector formula with anchor swapped to integer DOY `d ∈ 1..365`, exhaustively enumerated, with no sampling permitted (§10.2).

**Verified.** Evidence: §10.2 enumerates `d ∈ 1..365` and applies the annual-sector formula with anchor swap. The opening line: "B adopts the v0.3.3 exhaustive-enumeration discipline as its initial standard, not via amendment. No sampling-based anchor control is permitted at any phase of B's lifecycle." The closing paragraph confirms "No random sampling. No seed is consumed." DOY 79 is retained; February 29 is not a separate anchor; leap-year effects enter via `cycle_length_days_d`.

### 4.10 Three-class verdict map with integer beat-count thresholds

> Verdict map is exactly the three-class map in §12.2 with `beat_count_perm ≥ 9500` and `beat_count_anchor ≥ 347`.

**Verified.** Evidence: §12.1 specifies `beat_count_perm ≥ 9500` (out of 10,000) and `beat_count_anchor ≥ 347` (out of 365 DOY anchors; `347 = ceil(0.95 × 365)`). §12.2 names exactly three verdicts: Confirmatory (both pass), Split-null (exactly one passes), Non-confirmatory (neither passes). §12.3 rules out any quintile band or 95th-percentile prose not tied to the integer beat counts.

### 4.11 Pooled-vs-within-asset interpretation rule (§12.4)

> Pooled-vs-within-asset interpretation rule (§12.4) is present and binds the verdict text.

**Verified.** Evidence: §12.4 is present and binds verdict verbalization (not the verdict bit): a Confirmatory primary with a weak asset-stratified diagnostic must be described as **pooled-population modulation**, not within-asset modulation.

### 4.12 Gregorian-month independence caveat (§11.1)

> `PSS_GREG_MONTH` independence caveat present (§11.1).

**Verified.** Evidence: §11.1 reads "`PSS_GREG_MONTH` is not independent evidence beyond the §10.2 anchor-control family — it is one civil-calendar point within that family's neighborhood. It is best understood as a familiar civil-calendar benchmark for human readability, not as independent confirmatory evidence."

### 4.13 Data-contact disclosure wording (§13)

> Data-contact disclosure wording present verbatim (§13).

**Verified.** Evidence: §13 carries the required wording verbatim from `docs/cell_selection_decision_memo_v0.2.md` §11, naming the pullback Phase 1–3b SPY and Phase 3b 5-asset 2005–2022 contact history, the early lock of `BacktestParams` at `50ee2d1`, and the OOS 2023+ seal. The memo states "This disclosure is required wording. A hash citation alone does not satisfy it."

### 4.14 Seeds and permutation count locked

> `LABEL_PERM_SEED = 20260514` and `ASSET_STRAT_DIAG_SEED = 20260515` locked, with `N_PERM = 10,000` (§14).

**Verified.** Evidence: §14 enumerates `LABEL_PERM_SEED = 20260514` for N.1 (unstratified pooled permutation), `ASSET_STRAT_DIAG_SEED = 20260515` for the §11.3 asset-stratified diagnostic, and `N_PERM = 10,000`. The two seeds are stated to be distinct by design so that the diagnostic's permutation sequence is not a sub-sample of the primary null's.

### 4.15 Substrate clause: frozen CSV hashes, not pullback HEAD

> Substrate clause names frozen-CSV hashes (not pullback HEAD) as run substrate (§15).

**Verified.** Evidence: §15 reads "the Candidate B run substrate is the set of **frozen CSV SHA-256 digests** recorded in the Coherent Numbers freeze manifest. The pullback research repo's HEAD is **not** part of the run substrate." Drift in the pullback repo does not block a Candidate B run; manifest digest mismatch aborts the run regardless of pullback HEAD state.

## 5. No-data-contact statement

During this lock-acceptance preparation:

- **No harmonic-calendar features were computed.** No phase mapping, no anchor arithmetic, no boundary calculation.
- **No `entry_date` values were joined to phases.** §7.4's "no preview is a computation" rule was honored.
- **No PSS statistics were computed.** Neither `PSS_B1` nor `PSS_B2` nor any beat count was evaluated.
- **No row-level pullback trade data was inspected.** Verification touched only filesystem-level SHA256 of the frozen CSVs and the memo/manifest text. The CSV contents were not opened, parsed, sliced, or summarized.
- **The pullback repo was not touched.** No commits, edits, runs, or exports in `/Users/jay/pullback_research`.
- **OOS 2023+ data was not accessed** in either repo.
- **No Candidate B implementation was started.** No `candidate_b_*.py`, no test, no notebook, no script, no output file exists.

## 6. Lock statement

The Candidate B design memo at commit `1e9a3e6` is accepted as the **locked protocol** for Candidate B. From this point forward, implementation may proceed only under the terms specified in that memo. No design field — population scope, schema, calendar lens (anchor, bucket count, annual-sector formula, phase-range assertion), primary outcome (`PSS_B1` η²-form, `total_B1 = 0` abort), null definitions (N.1 unstratified label permutation, N.2 exhaustive 365-DOY anchor control), beat-count thresholds, three-class verdict map, §12.4 interpretation rule, §13 disclosure wording, §14 seeds (`LABEL_PERM_SEED = 20260514`, `ASSET_STRAT_DIAG_SEED = 20260515`, `N_PERM = 10,000`), or §15 substrate clause — may be changed without a new amendment artifact and its own audit trail. Analysis is authorized only after this lock-acceptance artifact is committed.

## 7. Post-lock authorization boundary

After this lock-acceptance artifact is committed, the following actions become authorized within the locked terms:

- Candidate B **implementation** may be written.
- Frozen CSVs may be **loaded under hash verification** against the manifest (§6 of the memo).
- `entry_date` may be **mapped to the locked 12-phase annual-sector calendar** per §7.1, with the phase-range assertion enforced.
- **Nulls and statistics** may be computed exactly as specified — N.1 with `LABEL_PERM_SEED = 20260514`, N.2 exhaustive enumeration over `d ∈ 1..365`, plus the §11 diagnostics with `ASSET_STRAT_DIAG_SEED = 20260515`.
- A **verdict log** may be generated reporting `PSS_B1`, `beat_count_perm`, `beat_count_anchor`, the three-class verdict per §12.2, the §12.4 verbalization rule, and the §13 disclosure.

The following remain prohibited:

- **No design changes** are allowed after observing results. Lens, anchor, bucket count, primary outcome, nulls, thresholds, and verdict map are frozen.
- **No OOS 2023+ access** in either repo.
- **No pullback repo modifications.** The pullback audit chain remains untouched.
- **No unregistered additional verdict heads.** Secondary outcomes (`PSS_B2`, per-asset, civil-month, January-anchor, asset-stratified permutation) cannot rescue or upgrade the verdict.
- **No design rescue based on secondary diagnostics.** A Non-confirmatory primary stays Non-confirmatory regardless of secondary patterns.
- **No sampling-based anchor control** may be reintroduced (§10.2 / §16).

## 8. Final state

- **Design memo locked** at commit `1e9a3e6`.
- **Substrate frozen** at commit `5225bfd`; all six frozen-CSV SHA256 digests verified against `docs/pullback_population_freeze_manifest_v0.1.md` at lock-acceptance time.
- **Implementation not yet started.** No Candidate-B-specific source, test, script, notebook, or output file exists.
- **Analysis not yet run.** No phase mapping, no `PSS_B1`, no beat counts, no verdict.
- **Next artifact is implementation, not design revision.**

— end of proposed lock-acceptance artifact —
