# Lane 2 GDELT1 Gate 4C Recognized-List Integrity Re-Review Authorization Memo v0.1

## 1. Title and status line

- **Memo:** Lane 2 GDELT1 Gate 4C Recognized-List Integrity Re-Review Authorization Memo v0.1.
- **On-disk path:** `docs/lane2_gdelt1_gate4c_recognized_list_integrity_re_review_authorization_memo_v0.1.md`.
- **Status:** authorization memo (not an execution report).
- This memo does **not** execute the Gate 4C re-review.
- This memo does **not** authorize Gate 5 execution or count-feasibility.
- This memo does **not** authorize a second GET (excluded by `d221e8f` §12 and not re-opened here).
- A separately initiated re-review prompt is still required after this memo is accepted; the re-review prompt is the artifact that fires the actual read-only investigation.

## 2. Background

### 2.1 §10 chain closure

The §10 evidence-capture envelope closed on 2026-05-21 at `origin/main = 4015b97`. The committed §10.6 closure memo bundled the §10.5 capture artifact (`recognized_list.json` + `.sha256` sidecar) under Option C disposition. The artifact is tracked and self-verifying on repo, with payload provenance commits `cfede1b` / `f10c1bc` and `turn_b_outcome=L1` embedded inside the JSON.

### 2.2 v0.7 post-§10 diagnostic execution

On 2026-05-22 the pre-run diagnostic was executed under prompt v0.7 (prompt chain v0.4 → v0.5 → v0.6 → v0.7, all chat-only — never persisted to disk). The diagnostic ran read-only against the tracked recognized list and the canonical F4 metadata; §3 / §5.5 / §6 / §8 / §9 all PASS.

### 2.3 Outcome — SPURIOUS-RECOGNIZED

- **§7.2 SPURIOUS-RECOGNIZED** (no-commit / commit-prohibited) classified after §6 set-difference: `extras = ['2013']`, a year-form identifier in `recognized_in_window_units` that is not in the planned partition.
- **§7.3 EXCESS-MISSING co-fired** on its independent criterion (`|missing| = 4 > 3`); the no-commit branch was chosen on a conservative judgment that was **not** pre-registered in v0.7 — codification of this rule is folded in at §11 below.
- Missing units: `2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`. The Turn B `3650 − 3647 = 3` arithmetic gap decomposes as `+1` extra (year `2013`) and `−4` missing dailies — net `−3`, **not** a clean 3-unit deficit.
- Clustering observations descriptive only (small-sample caveat binding at `|missing| = 4`): January 2014 three-consecutive-day cluster plus isolated 2014-03-19; **0 of 4** missing dailies fall inside the fixed ±14-day transition window `[2013-03-18, 2013-04-15]`; archive-format-transition hypothesis **not supported** at this evidence level.

### 2.4 Why Gate 5 remains blocked

The recognized-list artifact's **form-compatibility with the planned universe** is a precondition for any Gate 5 v0.2 design lock. Until the SPURIOUS-RECOGNIZED finding is mechanism-explained — i.e., until the re-review determines whether the year-form `'2013'` reflects a parser/classifier bug, a planned-universe gap, a transition-semantics mismatch, or a broader artifact invalidation — the universe of "what to count" cannot be pinned. Therefore Gate 5 v0.2 run-enablement drafting remains blocked.

## 3. Evidence basis

### 3.1 Post-§10 diagnostic report

- Path: `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`.
- Disk status: **exists on disk**.
- Verification status: **clean** after read-only verification — placeholder/leakage grep hit count = 0; §9 fully substituted; no Python-source / template-fragment leakage.
- Tracking status: **untracked**.
- Authorization status: **commit-prohibited under §7.2 SPURIOUS-RECOGNIZED**. Usable as evidence for this authorization discussion only. **Not** a tracked canonical repo artifact. **Not** to be staged, committed, pushed, edited, deleted, or treated as a committed reference without separate explicit authorization. This memo cites the post10 report under this explicit framing.

### 3.2 Recognized-list capture artifact

- Path: `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json`.
- SHA-256: `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`.
- Sidecar `.sha256` verifies `recognized_list.json: OK`.
- Tracked at commit `4015b97`.

Canonical provenance block (sorted keys), verified read-only against the tracked JSON before this memo was written:

```json
{
  "byte_capture_authorization_memo_commit": "cfede1b",
  "gate_4c_authorization_commit": "54fb16a",
  "gate_4c_conformance_commit": "e572c76",
  "gate_4c_implementation_commit": "ec1c3ec",
  "gate_4d_authorization_commit": "a2851f4",
  "gate_4d_conformance_commit": "9dea17c",
  "gate_4d_implementation_commit": "7f5caee",
  "post_4c_live_execution_authorization_commit": "f8345c8",
  "recognized_list_remediation_decision_commit": "f10c1bc",
  "turn_a_approval_commit": "991321d",
  "turn_b_outcome": "L1"
}
```

Field-by-field narrative form (same values, same scope):

- `provenance.byte_capture_authorization_memo_commit = "cfede1b"`
- `provenance.recognized_list_remediation_decision_commit = "f10c1bc"`
- `provenance.turn_b_outcome = "L1"`
- `provenance.gate_4c_authorization_commit = "54fb16a"`
- `provenance.gate_4c_implementation_commit = "ec1c3ec"`
- `provenance.gate_4c_conformance_commit = "e572c76"`
- `provenance.gate_4d_authorization_commit = "a2851f4"`
- `provenance.gate_4d_implementation_commit = "7f5caee"`
- `provenance.gate_4d_conformance_commit = "9dea17c"`
- `provenance.post_4c_live_execution_authorization_commit = "f8345c8"`
- `provenance.turn_a_approval_commit = "991321d"`

### 3.3 Historical v0.1 preservation

- Path: `docs/lane2_gdelt1_gate5_prerun_diagnostic_report_v0.1.md`.
- SHA-256: `633960dd36d076d091cd58ca94a88ad0ae28ee936af939624a3fb5dcc63e07f3`.
- `git diff` and `git diff --cached` both empty.
- Adding commit: `d334ad5 Record Lane 2 pre-run diagnostic precondition gap`.
- Must remain unchanged throughout the future re-review.

### 3.4 F4 preservation

- Directory: `results/lane2_gdelt1_count_feasibility/20260518T163302Z/`.
- `count_feasibility_metadata.json` SHA-256: `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d` (75,303 B, mtime 2026-05-18 18:33).
- `feasibility_summary.md` SHA-256: `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c` (393 B, mtime 2026-05-18 18:33).
- Must remain unchanged throughout the future re-review.

### 3.5 Guards inert

- `REAL_RETRIEVAL_ENABLED = False` at `src/lane2_gdelt1_count_feasibility.py:647`.
- `COUNT_FEASIBILITY_AUTHORIZED = False` at `scripts/run_lane2_gdelt1_count_feasibility.py:44`.
- Must remain `False` throughout the future re-review.

### 3.6 §10 chain (authorization lineage)

`d334ad5 → f10c1bc → cfede1b → 7a9ca71 → 4bff042 → 4015b97`.

## 4. Problem statement

The recognized-list capture artifact at §3.2 contains exactly one year-form identifier `'2013'` inside `recognized_in_window_units`. The planned partition (recovered offline from F4 metadata `layout_report.files_missing`) uses **monthly** identifiers `2013-01..2013-03` plus **daily** identifiers from `2013-04-01`; there is **no yearly aggregate** in the planned partition for 2013. The single planned yearly identifier is `2005`.

Consequently:

- The recognized-list artifact may not be form-compatible with the planned universe.
- The Turn B `3650 − 3647 = 3` arithmetic gap was **not** a clean 3-unit deficit. It decomposed as `+1` extra year-form `2013` and `−4` missing daily identifiers (`2014-01-23/24/25` + `2014-03-19`), netting `−3`.
- The post-§10 diagnostic report supporting this finding is **untracked** and **commit-prohibited**, but **clean** on disk and usable as evidence for this authorization discussion. No further authorization is granted by this memo to mutate or stage that report.

The substantive question this memo authorizes a future re-review to investigate is **mechanism**: how did a year-form `2013` identifier come to be present in `recognized_in_window_units`, and what does that imply for the artifact's validity, the planned partition's completeness, and the next steps in the Lane 2 chain.

## 5. Candidate hypotheses

These are starting hypotheses for the future re-review. They are **not** conclusions; the re-review must distinguish among them on read-only evidence and assign one of the §10 verdict classes accordingly.

- **H1: Capture-wrapper / classification mismatch.** The §10.1 wrapper `capture_recognized_list_once(...)` or the upstream classification logic in `extract_index_units` / `extract_index_units_live_safe` / `LiveSafeExtraction` may have routed a 2013 monthly or daily aggregate into yearly form by a localized parser or regex defect. Under H1 the recognized-list artifact contains a single classification error; the rest of the artifact is sound.

- **H2: Faithful capture; planned-universe gap.** Turn B's live-safe extraction faithfully recognized a 2013 yearly aggregate that actually exists in the GDELT 1.0 archive but was not modeled in the planned partition. Under H2 the recognized-list artifact is correct and the planned partition (derived from F4 metadata `layout_report.files_missing`) is incomplete or stale.

- **H3: Different form-class semantics around the 2013 monthly→daily transition.** The planned-universe construction and the recognized-universe construction may use different form-class boundary rules around the documented GDELT 1.0 transition at `2013-04-01`. Under H3 the discrepancy is a definitional mismatch between two construction paths, not a parser bug.

- **H4: Localized issue, artifact still usable.** If the only anomaly is the single yearly `'2013'` and the four missing 2014 dailies, and the recognized list is otherwise structurally sound, then the artifact may be usable for Gate 5 under a deterministic transform (e.g., drop `'2013'` at universe-construction time; treat the four 2014 dailies as documented substrate gaps).

- **H5: Broader invalidation.** If the year-form `'2013'` indicates a systemic form-class assignment failure, other identifiers in `recognized_in_window_units` may be misclassified at lower visibility (e.g., a 2014-05 monthly identifier where daily was expected). Under H5 the recognized-list artifact is invalid for Gate 5 purposes and must be recaptured under a new bounded second-GET authorization.

- **H6: Confounded missing dailies.** The four missing daily identifiers (`2014-01-23/24/25` + `2014-03-19`) may be independent substrate gaps with no causal connection to the form-class `'2013'` anomaly. The re-review should test whether the missing dailies and the extra yearly are causally linked or independent — the answer affects whether a deterministic transform under H4 is well-defined.

The re-review may add hypotheses but must not convert hypotheses into conclusions without evidence; an inability to distinguish among H1–H6 on read-only evidence routes to the `REVIEW-INCONCLUSIVE` verdict class (§10).

## 6. Future re-review allowed inputs (read-only only)

- **Tracked recognized-list artifact** at `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json` and its `.sha256` sidecar (read-only).
- **Capture-wrapper source code:** `capture_recognized_list_once(...)` and supporting helpers in `src/lane2_gdelt1_count_feasibility.py` (added at `7a9ca71`).
- **Parsing / classification source code:** `extract_index_units`, `extract_index_units_live_safe`, `fetch_archive_index_live_safe`, `LiveSafeExtraction`, and helpers. Live-safe / redirect-disabled Gate 4D path components (`build_redirect_disabled_opener`, `_NoFollowRedirectHandler`, `fetch_index_live_once`) may be inspected.
- **Relevant tests:** `tests/test_lane2_gdelt1_count_feasibility.py` (including the §10.1 wrapper tests, Gate 4C tests, Gate 4D tests; full Lane 2 test suite). Cache-disabled re-runs allowed if needed for diagnosis (read-only — no source/test edits).
- **§10 chain memos** (read-only): `f10c1bc`, `cfede1b`, `4bff042`, `4015b97` (closure memo + Option C disposition). Earlier chain memos for context: `c2717a6` Gate 5 decision, `175e939` Gate 5 run-enablement, `d221e8f` pre-run diagnostic authorization.
- **Post-§10 diagnostic report** at `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`, **explicitly marked as untracked and commit-prohibited evidence**. The re-review may read it but must not stage, commit, edit, delete, rename, or otherwise alter its on-disk state, and must not treat it as a committed reference in any downstream artifact.
- **F4 metadata** at `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json` (read-only; F4 baseline hashes must remain unchanged).
- **Historical v0.1 report** at `docs/lane2_gdelt1_gate5_prerun_diagnostic_report_v0.1.md` for context only (read-only; SHA-256 must remain `633960dd…07f3`).

## 7. Future re-review hard forbids

- No live GET.
- No GDELT contact of any form.
- No second GET (excluded by `d221e8f` §12; a second GET would require a separate future post-4C-style authorization memo analogous to `f8345c8`, which this memo does **not** draft and does **not** anticipate).
- No capture invocation. No call to `capture_recognized_list_once`. No call to `fetch_index_live_once`. No call to `fetch_archive_index_live_safe`.
- No event-file URL construction or request.
- No F4 modification of any kind. F4 SHA-256 baselines (§3.4) must hold throughout.
- No flipping of `REAL_RETRIEVAL_ENABLED` or `COUNT_FEASIBILITY_AUTHORIZED`. Both stay `False`.
- No Gate 5 entry. No count-feasibility run.
- No market-data access. No Step 2 entry.
- No modification of the tracked recognized-list artifact (`recognized_list.json` / `.sha256`).
- No modification of the historical v0.1 report (`d334ad5`).
- No modification, staging, commit, push, deletion, rename, or overwrite of the post-§10 diagnostic report at `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md` (remains untracked and commit-prohibited).
- No staging, commit, or push of any file inside the future re-review unless separately authorized after the re-review's verdict is reviewed.
- No memory update inside the re-review execution turn (memory updates require a separate explicit turn).
- No source / test / config file edits during the re-review. The re-review may construct ephemeral synthetic test fixtures in `tmp_path` for diagnostic purposes but must not commit them, and must not edit existing source or test files.
- No source pivot to a different substrate (e.g., GDELT 2.0, ICEWS) inside the re-review; substrate selection is out of scope.

## 8. Future re-review allowed operations (read-only)

- Inspect capture-wrapper source code, parsing/classification source, live-safe path components, and Gate 4C / Gate 4D test fixtures.
- Inspect the recognized-list payload at the JSON level (form-class distribution; per-identifier classification; comparison with planned partition).
- Inspect F4 planned-list metadata at the JSON level (`layout_report.files_missing` partition; form-class distribution).
- Inspect the untracked, commit-prohibited post-§10 diagnostic report as evidence (read-only).
- Compute offline comparisons (set difference, form-class enumeration, missing-unit calendar analysis, weekday/month/quarter aggregations) on already-on-disk artifacts only.
- Run cache-disabled `python3 -m pytest tests/test_lane2_gdelt1_count_feasibility.py` (or scoped subsets) read-only to confirm test invariants are unchanged after diagnosis.
- Construct synthetic test fixtures locally (`tmp_path` / fake openers / `_Resp` synthetic responses) to test classification behavior on **synthetic** inputs — no real network, no real GDELT data, no real post-2022 filenames.
- Apply L5 regex scan (`\b\d{8,14}\.(?:export|gkg|mentions)\.(?:CSV|csv)\.zip\b`) to the re-review report body before writing.
- No mutation. No network. No GDELT contact. No live capture.

## 9. Required future re-review outputs

The re-review must produce a report at a future path (proposed): `docs/lane2_gdelt1_gate4c_recognized_list_integrity_re_review_report_v0.1.md` (separate artifact from this authorization memo). The report must include, at minimum:

- **§1 Title + artifact status line** identifying the report as the Gate 4C recognized-list integrity re-review report v0.1, with explicit disposition (commit-eligible / commit-prohibited per verdict).
- **§2 Current canonical state** including HEAD = origin/main, F4 hashes, recognized-list SHA, historical-v0.1 preservation status, guard inertness.
- **§3 Dependency chain** including all §10 anchors plus this authorization memo's commit hash (once it is written).
- **§4 Evidence basis** mirroring §3 of this memo, including the explicit untracked-and-commit-prohibited framing of the post-§10 diagnostic report.
- **§5 Mechanism analysis** answering:
  - The exact mechanism (or candidate mechanisms) that produced or admitted year-form `'2013'` in `recognized_in_window_units`, if identifiable.
  - Whether the recognized-list artifact is **valid**, **invalid**, or **conditionally usable**.
  - Whether the issue is **local to `'2013'`** or **structurally broader** (with explicit enumeration of any other suspect identifiers found during inspection).
  - Whether the four missing dailies (`2014-01-23/24/25` + `2014-03-19`) are **true substrate-level missing units** or **downstream effects of form-class mismatch** (with read-only evidence).
- **§6 Implication map** answering:
  - Whether **Gate 5 v0.2 run-enablement drafting** can become eligible after remediation, and under exactly what conditions.
  - Whether **a new diagnostic prompt** is required (and if so, what it must codify — at minimum the precedence semantics in §11 below).
  - Whether **the recognized-list artifact** can be reused, must be deterministically transformed, or must be retired and recaptured.
- **§7 Verdict class** assigned (exactly one of the §10 classes below).
- **§8 Mandatory L5 regex scan result** (pattern verbatim; matches = 0 to write).
- **§9 Self-status footer** confirming F4 untouched, guards inert, historical v0.1 unchanged (SHA still `633960dd…07f3`), post-§10 report unchanged and still untracked / commit-prohibited, recognized-list artifact unchanged (SHA still `84ea721e…fff835fc`), no live GET / no GDELT contact / no capture / no Gate 5 / no count-feasibility / no market data / no Step 2 / no second-GET replication / no F4 modification / no guard flip / no staging / no commit / no push, memory not updated in the re-review execution turn.

The re-review report must contain **no real post-2022 GDELT filenames**.

## 10. Verdict classes for the future re-review

The re-review must classify into **exactly one** of the following six verdict classes. Each class has a consequence chain stating what becomes eligible, what remains blocked, whether Gate 5 v0.2 can be drafted, whether a new diagnostic is required, and whether the recognized-list artifact may be reused.

### 10.1 LOCAL-PARSE-MISMATCH

- **Mechanism:** Specific localized bug in the capture wrapper or classifier admitted `'2013'` as yearly; the rest of the artifact is sound.
- **Eligible (later, separately authorized):** A deterministic-transform memo specifying the exact transform (e.g., "drop `'2013'`; document the four 2014 dailies as substrate gaps under a named hypothesis"); then Gate 5 v0.2 drafting under explicit remediation.
- **Blocked:** Gate 5 execution until a fresh v0.2 run-enablement memo locks the transformed universe.
- **Recognized-list artifact:** reused with deterministic transform; the on-disk artifact is **not** edited.
- **New diagnostic:** not strictly required, but recommended to confirm the transformed universe yields a clean §7.7 CLEAN outcome before Gate 5.

### 10.2 CAPTURE-ARTIFACT-INVALID

- **Mechanism:** The recognized-list artifact contains structural classification failures beyond `'2013'`; the artifact is not usable for Gate 5.
- **Eligible (later, separately authorized):** A new capture authorization memo analogous to `cfede1b`, plus a new bounded second-GET (which requires its own post-4C-style authorization separate from this memo).
- **Blocked:** Gate 5 v0.2 drafting until the new capture lands; the existing artifact is retired (kept as historical evidence, not deleted).
- **Recognized-list artifact:** retired.
- **New diagnostic:** required, against the new capture; a fresh `v0.8+` diagnostic prompt with codified precedence (§11) is mandatory.

### 10.3 PLANNED-UNIVERSE-MISMATCH

- **Mechanism:** The recognized-list artifact is faithful; the planned partition is incomplete or stale (the `2013` yearly aggregate exists in GDELT 1.0 and was overlooked at F4-derived universe construction).
- **Eligible (later, separately authorized):** A planned-universe revision memo updating F4-derived expectations to include the yearly `'2013'`; revised universe = 3651 planned (or whatever the revision finds).
- **Blocked:** Gate 5 v0.2 until the revision lands.
- **Recognized-list artifact:** reused as-is.
- **New diagnostic:** required against the revised planned universe; a fresh `v0.8+` diagnostic prompt with codified precedence (§11) is mandatory.

### 10.4 RECOGNIZED-LIST-USABLE-WITH-CAVEAT

- **Mechanism:** Diagnosed but documented as a known anomaly that does not invalidate the artifact for Gate 5 purposes.
- **Eligible (later, separately authorized):** Gate 5 v0.2 drafting under a pre-registered caveat in the v0.2 run-enablement memo (e.g., "`'2013'` yearly identifier is dropped at universe-construction time; the four 2014 dailies are recorded as known substrate gaps").
- **Blocked:** nothing additional, but the caveat must be pre-registered in v0.2 before any count run.
- **Recognized-list artifact:** reused with caveat; not edited on disk.
- **New diagnostic:** optional; the v0.2 design may incorporate the caveat without re-running the diagnostic.

### 10.5 RECOGNIZED-LIST-USABLE-AFTER-DETERMINISTIC-TRANSFORM

- **Mechanism:** A deterministic, reproducible code-level transform applied to the existing artifact yields a Gate-5-usable universe.
- **Eligible (later, separately authorized):** A transform-implementation memo and patch (small, reviewed, conformance-checked) that lands the deterministic transform in code; then Gate 5 v0.2 drafting under the transform spec.
- **Blocked:** Gate 5 v0.2 until the transform lands and conformance review passes.
- **Recognized-list artifact:** reused via transform; original artifact unchanged.
- **New diagnostic:** required against the transformed universe to confirm a clean §7.7 CLEAN outcome.

### 10.6 REVIEW-INCONCLUSIVE

- **Mechanism:** The re-review cannot determine the mechanism from the available read-only on-disk evidence.
- **Eligible (later, separately authorized):** one of three downstream routes — (i) a new capture authorization (`CAPTURE-ARTIFACT-INVALID` route), (ii) a substrate-comparison memo (out of GDELT 1.0), or (iii) a new diagnostic prompt with broader scope. Selection of which route is itself a separate later memo.
- **Blocked:** Gate 5 v0.2 drafting until further evidence is obtained.
- **Recognized-list artifact:** status undetermined.
- **New diagnostic:** likely required; precedence semantics (§11) must be codified in any new prompt regardless.

## 11. Deterministic precedence semantics (folded in from `feedback_diagnostic_outcome_precedence.md`)

The motivating example is the 2026-05-22 v0.7 execution, where §7.2 SPURIOUS-RECOGNIZED and §7.3 EXCESS-MISSING both fired and the execution turn applied a conservative no-commit-dominates rule as a judgment call that was **not** pre-registered. This memo formalizes that rule for the future Gate 4C re-review and for any `v0.8+` diagnostic that follows.

### 11.1 Pre-registration requirement

Future diagnostics and re-reviews must **pre-register** what happens when ≥2 mutually-exclusive outcome triggers fire simultaneously. Simultaneous-trigger handling must **not** be decided at execution time.

### 11.2 Default dominance rule

If ≥2 outcome triggers fire simultaneously, the **no-commit / integrity-threatening outcome dominates** the commit-eligible arithmetic-only outcome by default. The dominance ordering applies to the seven Lane-2 outcome classes as follows (highest priority first):

1. `F4-CONTAMINATION` (no-commit; substrate-integrity)
2. `FIREWALL-BREACH` (no-commit; firewall/L5 integrity)
3. `SPURIOUS-RECOGNIZED` (no-commit; capture-artifact integrity)
4. `EXCESS-MISSING` (commit-eligible; arithmetic disagreement)
5. `INSUFFICIENT-MISSING` (commit-eligible; arithmetic disagreement)
6. `STRUCTURAL-CLUSTERING` (commit-eligible; descriptive structural signal)
7. `CLEAN` (commit-eligible; baseline)

If two outcomes from the same dominance tier fire simultaneously (e.g., `F4-CONTAMINATION` + `FIREWALL-BREACH`), the prompt must specify how to halt for adjudication rather than auto-routing.

### 11.3 Override discipline

The default dominance rule may be overridden **only** if a later memo explicitly defines an alternative ordering or an explicit `DUAL-OUTCOME` halt class **before** data contact / diagnostic execution. Overrides written or proposed after seeing diagnostic results are forbidden.

### 11.4 Subordinate-trigger recording

When the dominant outcome routes the diagnostic, the subordinate trigger must be **recorded as a co-extensive observation** inside the dominant outcome's report (current v0.7 behavior). This preserves the full evidence without changing the routing.

### 11.5 Application to the future re-review

The future Gate 4C re-review and any `v0.8+` diagnostic prompt that follows must pre-register §11.1–§11.4 verbatim or by explicit reference to this memo.

## 12. Non-authorization boundaries

This memo authorizes only a future separately initiated Gate 4C re-review prompt under the envelope in §6 / §7 / §8 / §9 / §10 / §11. It does **not** authorize:

- Gate 5 execution.
- Count-feasibility run.
- Market-data access.
- Step 2 entry.
- A new live GET of any GDELT URL.
- A second GET (excluded by `d221e8f` §12).
- Any capture invocation.
- Any mutation of F4.
- Any mutation of the tracked recognized-list artifact.
- Any mutation of the historical v0.1 report.
- Committing the post-§10 diagnostic report.
- Editing or deleting the post-§10 diagnostic report.
- Committing or pushing this memo without a separate explicit commit authorization.
- Triggering the re-review automatically when this memo is committed; a separate explicit re-review prompt is still required.
- Drafting any downstream artifact (re-review report, v0.2 run-enablement, substrate-comparison memo, transform implementation memo, new diagnostic prompt) in any turn that does not separately authorize the drafting.

Memo-itself-fires-no-request: even after this memo is committed, **no GDELT contact, no live GET, no capture, no count run, no Gate 5 entry, no F4 touch, no guard flip occurs by virtue of the commit itself**.

## 13. Recommended decision

**AUTHORIZE RE-REVIEW LATER.**

### 13.1 Justification

- **Necessity:** The SPURIOUS-RECOGNIZED finding blocks Gate 5 v0.2 drafting. The form-compatibility of the recognized-list artifact with the planned universe is a precondition for any v0.2 design lock, and that precondition is currently unverified. Without mechanism-level explanation, the chain stalls indefinitely.
- **Substrate-safety:** Under the §6 / §7 / §8 envelope, the re-review is genuinely small and substrate-safe — read-only inspection of already-on-disk artifacts plus offline comparison and synthetic-fixture tests. No new GET, no GDELT contact, no event-file request, no F4 modification, no guard flip, no market data, no Step 2.
- **Substrate-comparison rejected as primary route:** the Gate 5 decision memo (`c2717a6` §13) already weighed and rejected the substrate-pivot path on artifact-boundary grounds; inverting that choice now requires affirmative new evidence, which the re-review may help produce but which `c2717a6` did not request preemptively.
- **DEFER's principled concern absorbed:** the strongest DEFER consideration (the v0.7 precedence-judgment gap) is folded into §11 as a binding precondition of the re-review and any `v0.8+` diagnostic. That captures DEFER's value without adding a separate gate cycle.
- **FORBID misaligned with chain state:** the existing chain (`c2717a6` AUTHORIZE LATER) is still active; FORBID would require a substrate-program-level pivot decision that has not been initiated and is out of scope for this memo.

### 13.2 What AUTHORIZE RE-REVIEW LATER does and does not do

AUTHORIZE RE-REVIEW LATER permits a separately drafted re-review execution prompt to fire the read-only re-review, bounded by §6 / §7 / §8 / §9 / §10 / §11. **No code runs at this authorization step. No guards flip. F4 stays untouched. The post-§10 report stays untracked and unchanged. The historical v0.1 stays at SHA `633960dd…07f3`. The recognized-list artifact stays at SHA `84ea721e…fff835fc`.**

### 13.3 Pause discipline

Per `feedback_phase6_to_7_pause`-style discipline, after this memo is accepted, the chain pauses. The next step (a separately initiated re-review execution prompt) waits for explicit user initiation.

## 14. Closing checklist

- Authorization memo only — does not execute the re-review.
- Recommended decision: AUTHORIZE RE-REVIEW LATER.
- Does not authorize Gate 5.
- Does not authorize count-feasibility.
- Does not authorize live GET / second GET / capture.
- Post-§10 diagnostic report preserved as untracked / commit-prohibited evidence per §3.1 and §6.
- Historical v0.1 preservation (SHA `633960dd…07f3`) carried forward as a binding boundary.
- F4 baselines (`41c80c0…624c39d` / `00ce9b2…f5e37552c`) carried forward as binding boundaries.
- Recognized-list artifact (SHA `84ea721e…fff835fc`, sidecar OK) carried forward as a binding boundary.
- Guards `REAL_RETRIEVAL_ENABLED=False` / `COUNT_FEASIBILITY_AUTHORIZED=False` carried forward as binding boundaries.
- Deterministic precedence semantics (§11) folded in from `feedback_diagnostic_outcome_precedence.md`.
- Non-authorization boundaries (§12) intact.
- Memo path: `docs/lane2_gdelt1_gate4c_recognized_list_integrity_re_review_authorization_memo_v0.1.md`.

*End of Lane 2 GDELT1 Gate 4C Recognized-List Integrity Re-Review Authorization Memo v0.1.*
