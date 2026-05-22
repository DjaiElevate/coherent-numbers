# Lane 2 GDELT1 Gate 5 Run-Enablement Memo v0.2

## 1. Status

This is v0.2 of the Lane 2 GDELT1 Gate 5 Run-Enablement Memo. It succeeds v0.1 (committed at `175e939`, verdict `DEFER FOR DIAGNOSTIC`) on the same chain, now that the diagnostic v0.1 demanded has been executed (post-§10 v0.7 → `SPURIOUS-RECOGNIZED`) and the Gate 4C recognized-list integrity re-review has closed with the tracked, citable audit verdict `RECOGNIZED-LIST-USABLE-WITH-CAVEAT` (committed at `3176652`).

This memo is on disk as an **untracked working-tree file** following the disk-write turn that produced it. It is **not committed by this turn**. It is **not** an authorization of execution. Commit-authorization requires a separate explicit user prompt and a content-fidelity review under `[[feedback-disk-write-formatting-boundary]]` discipline; count-feasibility execution requires its own separate explicit execution prompt **after** v0.2 is committed and pushed.

## 2. Scope and non-authorization boundary

The memo addresses one decision: whether the Lane 2 GDELT1 program should authorize, defer, or forbid a future Gate 5 count-only feasibility run *given* the now-resolved substrate-coverage question.

This memo does **not** authorize, by itself: a Gate 5 count-only feasibility run; flipping `REAL_RETRIEVAL_ENABLED` or `COUNT_FEASIBILITY_AUTHORIZED`; a new live index GET; a second GET; an event-file request; market-data access; Step 2 entry; any mutation of F4; any mutation of the recognized-list artifact; any mutation of the historical v0.1 report; any staging, commit, edit, or deletion of the post-§10 diagnostic report; source/test/config edits; or memory edits.

The memo's verdict, even if `AUTHORIZE COUNT-FEASIBILITY LATER`, does not fire any request. A separate explicit execution prompt is still required after this memo is content-fidelity-reviewed, committed, and pushed.

## 3. Current canonical state

- Repo: `/Users/jay/Documents/GitHub/coherent-numbers`.
- `HEAD = origin/main = 3176652b663d96079151b2b87b4543e0b2bec2e1`; local ahead count = 0; tracked working tree clean (zero `M`/`A`/`D`/`R`).
- 9 untracked entries (the 8 known prior items + the post-§10 diagnostic report `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`) at the start of the disk-write turn that produced this memo; no duplicate untracked paths (verified by `git status --short | grep '^??' | sort | uniq -d` returning empty). After the disk-write turn lands this file, the untracked count is 10 (this file plus the prior 9).
- Guards inert: `REAL_RETRIEVAL_ENABLED = False` at `src/lane2_gdelt1_count_feasibility.py:647`; `COUNT_FEASIBILITY_AUTHORIZED = False` at `scripts/run_lane2_gdelt1_count_feasibility.py:44`.
- F4 baselines: `count_feasibility_metadata.json` SHA `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d` (75,303 B, mtime 2026-05-18 18:33); `feasibility_summary.md` SHA `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c` (393 B, mtime 2026-05-18 18:33). Layout status `missing`; `stopped_before_count_computation = True`; `files_available` empty.
- Recognized-list artifact at `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json` SHA `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`; sidecar `recognized_list.json: OK`; tracked at `4015b97`.
- Historical v0.1 report at `docs/lane2_gdelt1_gate5_prerun_diagnostic_report_v0.1.md` SHA `633960dd36d076d091cd58ca94a88ad0ae28ee936af939624a3fb5dcc63e07f3`; both `git diff` and `git diff --cached` empty; adding commit `d334ad5`.
- §10 chain anchors load-bearing: `d334ad5 → f10c1bc → cfede1b → 7a9ca71 → 4bff042 → 4015b97`.

## 4. Evidence anchors

Primary anchor (the tracked audit artifact this v0.2 inherits from):

- **`3176652b663d96079151b2b87b4543e0b2bec2e1`** — *Persist Gate 4C recognized-list integrity re-review report v0.1*; report at `docs/lane2_gdelt1_gate4c_recognized_list_integrity_re_review_report_v0.1.md` (SHA `992a395c4a23cbe6270e88b7352b1fe20b59e2eccc08d0864be59aad2d7a0de4`, 184 lines). This is the tracked, citable audit artifact for the substrate-coverage question.

Upstream chain anchors (read-only references, all committed):

- **`94a574b`** — Gate 4C recognized-list integrity re-review authorization memo v0.1 (SHA `26b0c0222a2e6cb359448196a21378f66b3239b0066d5e13746bff53b8df02b0`). Defines the re-review envelope (read-only inputs, hard forbids, allowed operations, required outputs, six verdict classes, §11 precedence semantics).
- **`175e939`** — Gate 5 run-enablement memo v0.1 (this v0.2's predecessor on the same chain). Verdict `DEFER FOR DIAGNOSTIC`; v0.1 §11 explicitly anticipates v0.2 carrying "its own ternary, distinct from this memo's verdict" when re-entering with diagnostic evidence.
- **`c2717a6`** — Gate 5 decision memo v0.1 (AUTHORIZE LATER at the decision level; §13 timing argument; §14 future-run constraints).
- **`d221e8f`** — Pre-run diagnostic authorization memo v0.1 (verdict AUTHORIZE DIAGNOSTIC LATER; §12 second-GET exclusion; §13.1 F4-integrity precondition).
- **`4015b97`** — §10.6 closure memo + Option C disposition (the recognized-list capture artifact is tracked here).
- §10 envelope: `cfede1b` (envelope memo) / `7a9ca71` (wrapper) / `4bff042` (capture approval).
- Post-§10 diagnostic report at `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`: **untracked, commit-prohibited under §7.2 SPURIOUS-RECOGNIZED**, usable for this memo as evidence only, not as a tracked canonical artifact. Its content is independently re-derived and audited by the tracked `3176652` report.
- F4 metadata at `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json`: read-only, baselines must remain unchanged.
- Recognized-list artifact at `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json`: read-only, SHA must remain unchanged.
- Historical pre-§10 report at `docs/lane2_gdelt1_gate5_prerun_diagnostic_report_v0.1.md`: read-only context only; SHA must remain `633960dd…07f3`.

## 5. Gate 4C re-review finding

The tracked re-review report at `3176652` records:

- **Final verdict:** `RECOGNIZED-LIST-USABLE-WITH-CAVEAT`.
- **Mechanism interpretation:** a definitional mismatch between the planner (`plan_gdelt1_files`, gated by `PRE_REGIME_YEARLY_THROUGH_YEAR = 2005`) and the classifier (`parse_gdelt1_unit_key`, shape-only, accepts any 4-digit string as yearly). The dominant §11 trigger `SPURIOUS-RECOGNIZED` resolves as a definitional mismatch, **not** capture-artifact corruption. Subordinate trigger `EXCESS-MISSING` recorded as a co-extensive observation.
- **Substantive numbers** (independently re-derived; reproduces post-§10 exactly): `|planned| = 3650` `{yearly: 1, monthly: 87, daily: 3562}`; `|recognized| = 3647` `{yearly: 2, monthly: 87, daily: 3558}`; `extras = ['2013']`; `missing = ['2014-01-23','2014-01-24','2014-01-25','2014-03-19']`; arithmetic `+1 extra year-form 2013 − 4 missing daily units = net −3` (not a clean 3-unit deficit).
- **Hypothesis slate:** H1 (capture/parser mismatch) **refuted**; H2 (planned partition incomplete because GDELT 1.0 publishes a `2013` yearly aggregate) **supported but not directly confirmed** (direct confirmation requires re-reading the live archive page, which is envelope-forbidden, or recovering raw Turn B HTML, which was not persisted); H3 (planner/classifier semantic mismatch) **supported** at code level; H4 (localized issue, artifact still usable) **supported**; H5 (broader systemic invalidation) **refuted**; H6 (four missing dailies as independent substrate gaps) **supported** by adjacency-probe evidence (`2014-01-22` and `2014-01-26` recognized; `2014-03-18` and `2014-03-20` recognized).
- **Cluster status:** 0 of 4 missing dailies fall inside the fixed ±14-day archive-format-transition window `[2013-03-18, 2013-04-15]`; archive-format-transition hypothesis not supported.

## 6. Binding caveat for v0.2

The following caveat from `3176652` §12 is **binding** on this v0.2 memo and on any count-feasibility run that proceeds from it:

> `'2013' yearly identifier is dropped at universe-construction time; the four 2014 dailies (2014-01-23, 2014-01-24, 2014-01-25, 2014-03-19) are recorded as known substrate gaps.`

This caveat is binding for v0.2 and must be **pre-registered** in this memo (here) **before any count run** — not negotiated, weakened, or rewritten after the fact. Pre-registration means the caveat is the universe-construction rule v0.2 commits to in advance; the count run cannot retroactively expand it (e.g., dropping additional identifiers) or contract it (e.g., re-admitting `'2013'`).

Implementation choices for the caveat (per the re-review report §11 / §12):

- **Memo-level pre-registration** (this option): the caveat is written into v0.2 as the binding precondition; the count-feasibility runner reads v0.2 (or v0.2's design lock fields) and applies the caveat at universe-construction time. No source-code edit required.
- **Code-level deterministic transform** (alternative option): a small reviewed patch lands the caveat as a code-level filter in the planned-universe or recognized-universe construction path (e.g., `usable_universe = recognized ∩ planned` plus a documented exception list for the four 2014 dailies). Would require a separate transform-implementation memo, patch, and conformance review before count-feasibility.

This v0.2 selects **memo-level pre-registration** by default, with code-level transform left as a permitted upgrade path if a future review prefers it. Either way, the **caveat content** is binding.

## 7. Treatment of recognized-list artifact

- The tracked artifact at `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json` (SHA `84ea721e…fff835fc`) is **reused without modification**. Its bytes are not edited, its sidecar is not regenerated, and no replacement capture is performed.
- The §6 caveat is applied **downstream** of the artifact at universe-construction time: the universe handed to the count-feasibility design is `recognized ∩ planned` (3,646 in-planned recognized identifiers), with the four 2014 dailies explicitly documented as substrate gaps and `'2013'` explicitly excluded as a planner/classifier-mismatch artifact. The artifact itself remains bit-for-bit unchanged.
- No second GET, no re-capture, no fetch invocation, no calls to `capture_recognized_list_once`, `fetch_index_live_once`, or `fetch_archive_index_live_safe`. The recognized-list artifact is treated as a frozen historical snapshot anchored to its `4015b97` commit and `cfede1b` provenance.

## 8. Treatment of post-§10 diagnostic report

- The post-§10 diagnostic report at `docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md` **remains untracked** in working tree and **remains commit-prohibited under §7.2 SPURIOUS-RECOGNIZED**. Its commit-prohibited status survives the `3176652` re-review-report commit unchanged, because only the re-review report was committed at `3176652`, not the post-§10 report.
- v0.2 cites the post-§10 report only via the tracked `3176652` re-review report (which independently re-derives the same numbers under the audit-artifact framing). v0.2 does **not** stage, commit, edit, rename, delete, move, or otherwise mutate the post-§10 report. v0.2 does **not** treat the post-§10 report as a tracked canonical reference for downstream artifacts — when downstream artifacts need the substrate-coverage evidence, they reference the tracked re-review report at `3176652`, not the untracked post-§10 file.
- The post-§10 report continues to exist on disk as historical evidence of the v0.7 diagnostic execution; v0.2 does not require it to be committed for its own evidence chain.

## 9. Count-feasibility eligibility analysis

The Gate 5 decision memo (`c2717a6`) authorized count-feasibility at the decision level (AUTHORIZE LATER) but conditioned it on a v0.2-style run-enablement memo locking the universe-and-verdict-map design. v0.1 (`175e939`) deferred that lock to a pre-run diagnostic, which has now completed via v0.7 → SPURIOUS-RECOGNIZED → Gate 4C re-review → `RECOGNIZED-LIST-USABLE-WITH-CAVEAT`.

**Where the §11 timing argument from v0.1 stood:** "discovering the structure during or after the run is too late if the structure was load-bearing for the lock." v0.1 deferred precisely because it could not lock without knowing whether the gap was random scatter or structural shortfall.

**Where the evidence now stands:**

- The 1-extra-yearly + 4-missing-daily structure is **known and audited** (tracked at `3176652`).
- The 1 extra is a **definitional planner/classifier mismatch**, not a substrate corruption. The caveat-driven universe `recognized ∩ planned` is well-defined and deterministic.
- The 4 missing dailies are **independent substrate gaps** with no clustering signal at the ±14-day transition boundary; H6 supported.
- The artifact is structurally sound for the 3,646 in-planned recognized identifiers (zero unparseable; monthly count matches planned exactly; all expected 2013 monthlies and dailies present).

**Sufficiency of the §6 caveat:**

- **Sufficient** for the v0.1 §11 timing concern: the gap structure is no longer "unknown" — it is enumerated, classified, and resolved.
- **Sufficient** for the universe-construction lock: `recognized ∩ planned` is a deterministic, reproducible universe of size 3,646; the four 2014 dailies are recorded as substrate gaps that the count-feasibility verdict map can anticipate.
- **Sufficient** for downstream design: the count-feasibility design can lock its verdict-map under the caveat without further substrate-coverage investigation.
- **Insufficient** only in one residual sense: H2 (the upstream `2013.zip`-or-equivalent existence) is supported but not directly confirmed; if a future memo directly confirms upstream presence of a 2013 yearly aggregate, the caveat's "drop `'2013'`" treatment becomes a deliberate scope choice rather than a defect repair. The conservative caveat handles both interpretations identically (the count run ignores `'2013'` either way), so this residual is non-blocking.

**Conclusion on eligibility:** count-feasibility design lock is eligible under the §6 caveat; count-feasibility execution remains gated on a separate explicit execution prompt after v0.2 is committed.

## 10. Diagnostic re-run question

The tracked re-review report at `3176652` §13 states: *"A new diagnostic is optional, not required. The v0.2 design may incorporate the §12 caveat without re-running the diagnostic, because the mechanism is now resolved and the universe-construction rule under the caveat is deterministic. If v0.2 design prefers a clean `CLEAN` outcome from a fresh diagnostic before proceeding to count-feasibility, a future `v0.8+` diagnostic (with codified §11 precedence per the committed memo's `feedback_diagnostic_outcome_precedence.md` reference) against the caveat-transformed recognized list could be run as a design choice, but it is not a precondition."*

This v0.2 memo treats the re-diagnostic as **optional, not required**:

- **In favor of running it (as a design choice):** a fresh `v0.8+` diagnostic against the caveat-transformed universe (`recognized ∩ planned`, the four 2014 dailies pre-registered as substrate gaps) would, on the evidence here, return `CLEAN` — providing direct empirical confirmation rather than inferred consistency. It would also be a natural occasion to codify the §11 precedence semantics (the open methodological item per `[[feedback-diagnostic-outcome-precedence]]`) in the prompt itself before any future analogous diagnostic.
- **Against running it:** the mechanism is resolved; the universe under the caveat is deterministic; running another diagnostic without new evidence to find is process-for-process's-sake. The Lane 2 chain has already absorbed multiple diagnostic and audit cycles; adding another adds latency without proportionate evidence return.

**v0.2 stance:** the re-diagnostic is **not required** by this memo. v0.2 does not block count-feasibility on a re-diagnostic, and does not request one. If a future review prefers a clean `v0.8+` outcome before count-feasibility execution, that decision can be made at the count-feasibility execution-prompt step (which is separate from this memo); the §11 precedence codification can be folded into either that diagnostic or a standalone precedence-prompt memo, as preferred at that later step.

## 11. Gate 5 v0.2 decision

**Verdict: `AUTHORIZE COUNT-FEASIBILITY LATER`.**

Three-way label set used by this memo: **`AUTHORIZE COUNT-FEASIBILITY LATER`** / `DEFER FOR CLEAN DIAGNOSTIC` / `FORBID COUNT-FEASIBILITY`.

Reasoning, against each rival:

- **Not `DEFER FOR CLEAN DIAGNOSTIC`:** v0.1's `DEFER FOR DIAGNOSTIC` was justified by the unresolved gap structure; that structural question has now been resolved by the tracked Gate 4C re-review report at `3176652` (`RECOGNIZED-LIST-USABLE-WITH-CAVEAT`). A second DEFER, this time for a "cleaner" diagnostic, would require treating "consistent with H4+H6, mechanism resolved at code level, audit verdict committed and cross-linked from feedback memory" as **insufficient** evidence — which inverts the chain's evidence threshold. A re-diagnostic is permitted by `3176652` §13 as a design choice but is not a precondition; demanding it here would be process-for-process's-sake. (If a future review wants the clean-diagnostic confidence boost, the request can be made at the count-feasibility execution-prompt step, separately from this memo, without re-opening v0.2.)
- **Not `FORBID COUNT-FEASIBILITY`:** FORBID would require treating the SPURIOUS-RECOGNIZED finding as evidence of broader substrate problems, which `3176652` §9 explicitly refuted (H5 refuted by absence of any other classification anomaly; H1 refuted by all-expected-2013-monthlies-and-dailies-present). FORBID would also override the Gate 5 decision memo's (`c2717a6` §13) substrate-pivot rejection, which §13 grounded on the reasoning that the 3-unit gap does not rise to substrate-veto and that FORBID requires affirmative new evidence rather than absence of new positive evidence — evidence that has not materialized. FORBID overshoots the available evidence.
- **`AUTHORIZE COUNT-FEASIBILITY LATER`** is justified because: (i) the diagnostic precondition v0.1 demanded has been satisfied; (ii) the §6 caveat provides a deterministic, pre-registerable universe-construction rule; (iii) the recognized-list artifact is reused without modification, preserving all upstream chain integrity; (iv) `c2717a6`'s AUTHORIZE LATER at the decision level remains active; (v) the memo itself does not execute count-feasibility — a separate execution prompt is still required.

**What `AUTHORIZE COUNT-FEASIBILITY LATER` permits:** a separately drafted count-feasibility execution prompt, bounded by `c2717a6` / `175e939` / `d221e8f` / `3176652` envelope plus this v0.2's §6 caveat and §13–§14 hard forbids, may fire the one count-only feasibility run at a later turn.

**What `AUTHORIZE COUNT-FEASIBILITY LATER` does NOT do:** it does not execute the run; it does not flip guards; it does not touch F4; it does not authorize a fresh GET; it does not authorize a second GET; it does not authorize Step 2 or market-data access.

## 12. Consequence chain

Under the v0.2 verdict `AUTHORIZE COUNT-FEASIBILITY LATER`:

- **Eligible (under separate explicit initiation):**
  - A count-feasibility execution prompt, parameterized by this v0.2's §6 caveat and binding boundaries, after v0.2 is content-fidelity-reviewed, committed, and pushed.
  - Optional: a fresh `v0.8+` diagnostic against the caveat-transformed universe, if a future review prefers direct empirical CLEAN confirmation before count-feasibility execution.
  - Optional: a code-level deterministic transform implementing the §6 caveat in source (with its own implementation memo + conformance review), if a future review prefers code-level over memo-level pre-registration.
- **Remains blocked (none of these become eligible from this verdict):**
  - Gate 5 execution itself (requires its own separately authorized run-enablement-fire step after count-feasibility).
  - Market data access; Step 2 entry; second-GET replication (`d221e8f` §12 exclusion); live GET (would need a fresh post-4C-style authorization analogous to `f8345c8`); capture invocation; F4 modification; guard flips.
  - Source / test / config edits except as specifically authorized for the optional code-level transform (which is itself a separate memo + patch step, not initiated here).
  - Any staging / commit / push of the post-§10 diagnostic report.
- **Recognized-list artifact reuse:** allowed without modifying the artifact. SHA `84ea721e…fff835fc` preserved.
- **Caveat status:** the §6 caveat is **binding** on any count-feasibility run that proceeds from v0.2; it must be pre-registered in the execution prompt and cannot be retroactively weakened or expanded.

## 13. Hard forbids after this memo

The following constraints bind any later step in the Lane 2 GDELT1 chain that proceeds from this v0.2 memo. They hold whether v0.2 is at draft, on disk, committed, or referenced by a successor:

- **Gate 5 execution remains blocked.** Even after count-feasibility runs and produces a verdict, Gate 5 execution itself requires its own separately authorized fire step.
- **Count-feasibility run remains blocked** in this memo's drafting turn, this disk-write turn, any subsequent v0.2 content-fidelity-review turn, and any v0.2 commit/push turn. Count-feasibility execution requires a separate explicit execution prompt **after** v0.2 is written, reviewed, and committed.
- **Market data remains blocked.**
- **Step 2 remains blocked.**
- **Live GET remains blocked.** Any new live GET requires a fresh authorization analogous to `f8345c8`.
- **Second GET remains blocked.** `d221e8f` §12 exclusion still in force; would require a separately authorized future post-4C-style memo.
- **Capture remains blocked.** No call to `capture_recognized_list_once`, `fetch_index_live_once`, or `fetch_archive_index_live_safe`.
- **F4 modification remains blocked.** F4 baselines (`41c80c0…624c39d` / `00ce9b2…f5e37552c`) must hold throughout.
- **Recognized-list mutation remains blocked.** SHA `84ea721e…fff835fc` and sidecar `recognized_list.json: OK` must hold.
- **Historical-v0.1 mutation remains blocked.** SHA `633960dd…07f3` must hold; `git diff` and `git diff --cached` must remain empty.
- **Post-§10 diagnostic report staging / commit / edit / delete remains blocked.** The report remains untracked and commit-prohibited under §7.2 SPURIOUS-RECOGNIZED indefinitely, absent a separately authorized future step.
- **Guard flips remain blocked.** `REAL_RETRIEVAL_ENABLED` and `COUNT_FEASIBILITY_AUTHORIZED` both stay `False` until and unless a separately authorized count-feasibility execution prompt initiates the one-run-only / inert-restore cycle described by the Gate 5 decision memo §14 and v0.1 §18.
- **Source / test / config edits remain blocked.** Except as specifically authorized by a future code-level-transform implementation memo (which is itself a separate step).
- **Memory edits remain blocked unless separately authorized.** This v0.2 disk-write turn does not edit memory; later content-fidelity-review and commit turns must each carry their own memory-edit authorization.
- **Any eventual count-feasibility run requires a separate explicit execution prompt after v0.2 is written, reviewed, and committed.** v0.2's existence — even fully committed and pushed — does not by itself authorize firing the run.

## 14. Future execution requirements

For a count-feasibility run to actually fire under v0.2, the following sequence is required:

1. v0.2 is **written to disk** under a separately authorized disk-write turn. The disk-write turn must invoke `[[feedback-disk-write-formatting-boundary]]` discipline: verbatim of the approved draft except for strictly bounded formatting (whitespace / Markdown syntax / fences / list markers / wrapping / write mechanics only). Any silent content adaptation is forbidden.
2. v0.2 is **content-fidelity-reviewed** before commit. The review must verify section-by-section that every required claim, caveat, boundary, and verdict is preserved exactly, that the §6 caveat appears verbatim, that the §13 hard-forbids list is complete, that the §11 verdict is exactly `AUTHORIZE COUNT-FEASIBILITY LATER` (or whatever the approved draft commits to), and that no drift has been introduced.
3. v0.2 is **committed and pushed** under a separately authorized commit-and-push turn, staging exactly the one v0.2 file, with the exact commit subject the user authorizes (e.g., *"Lock Gate 5 v0.2 run-enablement under §6 caveat"* or equivalent). No other files staged or committed.
4. After v0.2 is on `origin/main`, a **count-feasibility execution prompt** is separately initiated by the user. The execution prompt must:
   - Cite v0.2's commit hash as authorization anchor.
   - Pre-register the §6 caveat verbatim.
   - Pre-register the one-run-only and inert-restore discipline.
   - Define the count-feasibility verdict-map under the caveat-transformed universe.
   - Confirm guards are inert at start of run.
   - Authorize the single transient flip of `REAL_RETRIEVAL_ENABLED` and `COUNT_FEASIBILITY_AUTHORIZED` for the duration of the one run.
   - Authorize the immediate inert-restore after the run completes (mirroring `9e329c2`).
5. The count-feasibility run executes **exactly once** under the prompt. F4 may or may not be touched depending on the new run's `archive_layout_status`; the existing F4 baselines `41c80c0…624c39d` / `00ce9b2…f5e37552c` are the historical record of the prior F4 run and remain untouched by the v0.2 run unless the v0.2 design explicitly directs otherwise (which would require its own pre-registration in v0.2).
6. After the run, a **post-run report + memory update + Gate 5 v0.3 (or successor) drafting decision** are separate turns.

This v0.2 memo authorizes step (4) eligibility under the §13 hard forbids; it does not authorize steps (5) or (6) directly, and it does not authorize anything in steps (2)–(3) by itself (those each need their own separate authorization turns).

## 15. Open audit risks and mitigations

- **Risk A — H2 not directly confirmed.** The Gate 4C re-review marked H2 (planned partition incomplete because GDELT 1.0 publishes a `2013` yearly aggregate) as *supported but not directly confirmed*. If H2 is in fact true and a future direct-confirmation step recovers the upstream `2013.zip`-or-equivalent existence, the §6 caveat's "drop `'2013'`" treatment becomes a scope choice rather than a defect repair.
  - **Mitigation:** the §6 caveat handles both H2-true and H2-false interpretations identically — the count run ignores `'2013'` either way. v0.2 does not depend on H2's resolution. A future direct-confirmation step (which would itself require separate authorization, since it implies re-reading the live archive page) can re-open `PLANNED-UNIVERSE-MISMATCH` if desired, but it does not invalidate the count-feasibility run under v0.2's caveat.

- **Risk B — the four 2014 dailies might cluster on retest.** The current evidence (0 of 4 in the fixed ±14-day archive-format-transition window; adjacent calendar days recognized; small-sample caveat binding at |missing|=4) does not support a clustering claim, but the sample is small.
  - **Mitigation:** the §6 caveat pre-registers the four dailies as substrate gaps regardless of any future clustering observation. The count-feasibility verdict map can include a verdict line for "substrate-attributable shortfall" that absorbs these four dailies without re-opening the universe lock. If a future Gate 5 v0.3 (after v0.2's count run) wishes to revisit the substrate-gap interpretation under richer data, it may do so in its own memo without retrospectively touching v0.2.

- **Risk C — §11 precedence semantics not codified in a fresh `v0.8+` prompt.** The dominance ordering (`F4-CONTAMINATION > FIREWALL-BREACH > SPURIOUS-RECOGNIZED > EXCESS-MISSING > INSUFFICIENT-MISSING > STRUCTURAL-CLUSTERING > CLEAN`) is recorded in the tracked authorization memo at `94a574b` §11 and is cross-linked from `[[feedback-diagnostic-outcome-precedence]]`. v0.2 itself does not run a diagnostic and therefore does not need to pre-register the ordering inside its own text, but any future `v0.8+` diagnostic (if a future review elects to run one) must.
  - **Mitigation:** v0.2 explicitly references `[[feedback-diagnostic-outcome-precedence]]` and `94a574b` §11 as the binding precedence source for any future diagnostic. The §11 codification work itself remains an open methodological item per the feedback memory; v0.2 does not close it but does not depend on it.

- **Risk D — v0.1 commit `175e939` remains the prior on the chain.** v0.2 is a successor, not a supersession; v0.1 stays on disk as historical context. There is no risk of confusion if v0.2's title and status line make the relationship explicit, which they do (§1).
  - **Mitigation:** v0.2's §1 status line and §4 evidence anchors both name v0.1 explicitly and locate it on the chain. v0.1 is never edited.

- **Risk E — disk-write silent-edit recurrence.** The Gate 4C authorization memo's disk-write (at `94a574b`) silently adapted §1 / §3.1 / §12 / §13.3 / §14, requiring a follow-up §12 restoration patch at the same commit. That incident codified `[[feedback-disk-write-formatting-boundary]]`.
  - **Mitigation:** v0.2's eventual disk-write turn must invoke [[feedback-disk-write-formatting-boundary]] discipline explicitly, treating any content-level adaptation as a separate explicit content-edit step. The content-fidelity review before commit must verify section-by-section against this approved chat draft.

## 16. Final drafting notes

This memo is now on disk as an untracked artifact following the disk-write turn that produced it. It is **not committed by this turn**; it does not authorize execution; it does not by itself flip any guard, modify any artifact, or commit any change.

Disk-write authorization was the explicit separate user prompt that produced this file. Commit authorization is a separate user prompt **after** content-fidelity review. Count-feasibility execution authorization is a separate user prompt **after** v0.2 is committed. Each step in this chain holds the boundary of the previous one and adds no new authority beyond what is explicitly granted in its turn.

The draft is suitable for review. Specific design choices a reviewer may wish to revisit before disk-write:

- §10 stance on diagnostic re-run (currently "not required"; could be revised to "recommended" or "required" if a reviewer prefers tighter empirical confirmation).
- §6 caveat implementation choice (currently memo-level pre-registration; could be revised to code-level deterministic transform).
- §11 verdict (currently `AUTHORIZE COUNT-FEASIBILITY LATER`; the strongest rival on the available evidence is `DEFER FOR CLEAN DIAGNOSTIC`, which would re-open §10 with a "required" stance).

If any of these are revised, the revisions belong here in the chat draft, not at disk-write time. Disk-write must transcribe the approved draft verbatim.

*End of Lane 2 GDELT1 Gate 5 Run-Enablement Memo v0.2.*
