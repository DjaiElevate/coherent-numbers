# Lane 2 GDELT1 Recognized-List Remediation Decision Memo v0.1

## 1. Artifact status

**Decision memo v0.1. Records path selection only; does NOT authorize any execution.**

Drafted 2026-05-20. File at `docs/lane2_gdelt1_recognized_list_remediation_decision_memo_v0.1.md`. This memo records the remediation path selected after the Lane 2 pre-run diagnostic halted at the recognized-list precondition gap recorded in the halt report at commit `d334ad5`. It does **not** by itself authorize byte-capture, a second GET, a diagnostic rerun, Gate 5 execution, count-feasibility, market-data access, or Step 2. The next required artifact is a separate Gate 4C re-review / Turn B byte-capture authorization memo v0.1.

The memo evaluates exactly one decision: which remediation path the chain follows. §4 records the three options surfaced by the halt report (A / B / C). §5 records the selection. §6 records non-authorization boundaries. §7 records the recommended next artifact. §8 records the commit posture for this memo itself.

## 2. Current reference frame

- **Local HEAD** = `d334ad54898c20c7e82db2012b292751b253de49` (short: `d334ad5`).
- **`origin/main`** = `d221e8fa7361b31b15fbc9f649dfffafce5d8fb5` (short: `d221e8f`).
- At this memo's drafting time, local `main` was one commit ahead of origin (the halt-report commit `d334ad5` had not been pushed). Push posture is a separate later decision per §8 and the chain's standing discipline.
- **Halt report at `d334ad5` is citation-stable**: tracked, committed, and reachable via `git log -1 --oneline d334ad5`. Commit message verbatim: `Record Lane 2 pre-run diagnostic precondition gap`. The 213-line report at `docs/lane2_gdelt1_gate5_prerun_diagnostic_report_v0.1.md` is the canonical evidence base for this decision memo.
- **F4 SHA-256 baseline preserved** at the §13.1 values recorded in the halt report's §4.3:
  - `count_feasibility_metadata.json` (75,303 B, mtime 2026-05-18 18:33) = `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d`
  - `feasibility_summary.md` (393 B, mtime 2026-05-18 18:33) = `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c`
- **Runner guards remain inert**: `REAL_RETRIEVAL_ENABLED = False` at `src/lane2_gdelt1_count_feasibility.py:647`; `COUNT_FEASIBILITY_AUTHORIZED = False` at `scripts/run_lane2_gdelt1_count_feasibility.py:44`.
- **Lane 2 chain anchors carried forward**: post-4C `f8345c8`, Gate 4D memo `a2851f4`, Gate 4D implementation `7f5caee`, Gate 4D conformance `9dea17c` (PASS), Turn A approval `991321d`, Gate 5 decision `c2717a6` (AUTHORIZE LATER), Gate 5 run-enablement `175e939` (DEFER FOR DIAGNOSTIC), pre-run diagnostic authorization `d221e8f` (AUTHORIZE DIAGNOSTIC LATER), pre-run diagnostic halt report `d334ad5` (precondition-failure note). All prior chain artifacts through `d334ad5` were committed as of this memo's drafting; push posture for `d334ad5` is a separate later decision (see §8).

## 3. Discovered gap (brief restatement from the halt report)

- The `d221e8f` §13.1 mandatory F4-integrity precondition **PASSED** in full (10/10 checks; SHA-256 baseline recorded — see §2 above).
- The diagnostic **halted before** any set-difference operation, before any missing-unit enumeration, and before any clustering check.
- The cause: the **recognized 3647-unit list was not available offline**. The `175e939` §12.1 envelope assumed the list was "already-captured" from Turn B's stdout, but Turn B's stdout was transient and was not persisted to any reachable artifact (filesystem search in the halt report §6.1 confirmed: 0 hits across the repository and `/Users/jay` for `"recognized_in_window": 3647` as a structured value, 0 hits for `LiveSafeExtraction` serializations, 0 hits for filename patterns like `*turn_b*` or `*recognized*`).
- The arithmetic identity `3650 − 3647 = 3` is known from Turn B's recorded summary counts, but **was not promoted to set-difference evidence**. Set-difference evidence requires the *identities* of the 3 missing units; clustering checks (by month / weekday / archive-format transition) require those identities too. Neither was producible offline.
- The gap is therefore at the **evidence-capture layer** (Turn B did not write its `LiveSafeExtraction` to disk under the Gate 4C firewall), not at the **diagnostic-design layer** (`175e939` §§12–15 + `d221e8f` §13.1 are sound; the diagnostic ran exactly as specified up to the halt).

## 4. Alternatives considered

The halt report §12 surfaced three principled remediation paths. They are restated here with their strongest grounds and the rationale for selection/rejection.

### Option A — Gate 4C re-review / Turn B byte-capture authorization memo *(selected)*

**Substance:** A small new authorization memo (drafted as v0.1 in a separate step after this decision memo is committed) that revisits the Gate 4C / Gate 4D path to add a **bounded byte-capture mechanism**. The mechanism would authorize a single bounded augmentation to the Turn B-equivalent extraction path so that the `LiveSafeExtraction` result (form-class only for post-2022; real identifiers for 2005–2022 in-window) is written to disk under the firewall. The captured artifact would then serve as the offline-readable recognized list for any future diagnostic re-attempt.

**Strongest grounds (selection rationale):** The defect is at the evidence-capture layer, not the diagnostic-design layer. The diagnostic ran exactly as specified up to the halt; what failed was the standing assumption that Turn B's stdout had been captured to disk. Remediating at the same layer as the defect — Gate 4C's firewall + Turn B's extraction-and-output path — places the fix where the problem is. Option A also lets every other artifact in the chain (`c2717a6`, `175e939`, `d221e8f`, `d334ad5`) stand unchanged as citation-stable history; no prior memo is amended or superseded.

### Option B — diagnostic-authorization v0.2 folding byte-capture in *(rejected)*

**Substance:** An amendment to `d221e8f` (drafted as v0.2) that bundles a single bounded Turn B-equivalent live GET *with* on-disk capture into the diagnostic authorization itself, scoped tightly enough that it would not be the same as the §12-excluded second-GET replication for stability-of-gap.

**Rejection rationale:** This option treats the symptom (the diagnostic couldn't read the list) as a diagnostic-envelope problem and bundles a Gate 4C/4D-equivalent live action into the diagnostic authorization. But the missing input *originated* in Gate 4C / Turn B evidence capture, not in the diagnostic envelope. Bundling the byte-capture into a v0.2 diagnostic-authorization memo would muddy the artifact-layer boundary that has held cleanly across the chain: the diagnostic-authorization memo authorizes *the diagnostic*, not new live retrievals or firewall augmentations. Option B would also expand `d221e8f`'s scope substantially after the fact, in a way that the original §12 second-GET-exclusion clause was specifically written to forbid. Rejecting B preserves the chain's layer discipline.

### Option C — DEFER pending broader discussion *(rejected as the active remediation path)*

**Substance:** Pause Lane 2's diagnostic loop without remediating. Step 2 readiness remains blocked behind the loop; all boundaries (no GDELT, no F4 touch, etc.) remain in place; revisit the data-availability assumptions broadly at a later date.

**Rejection rationale (as the active path):** DEFER does not remediate the recognized-list capture gap. It only pauses Lane 2, leaving the chain stuck at the same halt state indefinitely. The halt report at `d334ad5` already records the pause-equivalent posture; selecting DEFER here would add no new artifact value. DEFER is **acceptable as a broader program pause** if separately invoked (e.g., if the user decides Lane 2 should be paused for unrelated reasons), but it is not the active remediation path because it does not produce a route to a captured recognized list. If DEFER is later invoked for broader reasons, this memo's Option A selection does not block that pause — Option A only authorizes drafting the next memo, not running anything.

## 5. Decision

**OPTION A — Gate 4C re-review / Turn B byte-capture authorization memo.**

The defect is at the evidence-capture layer; the remediation lives at the same layer. This selection:

- Preserves the artifact-layer boundary between Gate 4C/4D (live-retrieval discipline + firewall) and the diagnostic envelope (`175e939` §§12–15 + `d221e8f` §13.1).
- Leaves all prior chain artifacts (`c2717a6`, `175e939`, `d221e8f`, `d334ad5`) citation-stable and unmodified.
- Routes the next active artifact to a separately drafted Gate 4C re-review / Turn B byte-capture authorization memo, which will itself argue its own AUTHORIZE LATER / DEFER / FORBID ternary under post-4C-style discipline (single bounded write, no event-file contact, mandatory L5 regex scan, inert-restore).
- Does **not** by itself authorize anything beyond drafting the next memo. The next memo, in turn, will not by itself execute byte-capture; it will only authorize a later, separately initiated byte-capture step.

## 6. Non-authorization statement

This decision memo records the chosen remediation path. It does **not** authorize, by itself or by inference:

- **byte-capture execution.** A future Gate 4C re-review / Turn B byte-capture authorization memo is required; that memo, in turn, will only authorize a later separately initiated byte-capture step.
- **a second GET** of any GDELT URL. The `d221e8f` §12 exclusion stands; any future GET requires a fresh post-4C-style authorization memo of its own.
- **diagnostic rerun.** A future re-attempt of the pre-run diagnostic requires (a) successful byte-capture under the new memo, (b) a fresh diagnostic-execution prompt, and (c) re-confirmation of `d221e8f` §13.1 against the F4 baseline preserved in §2.
- **Gate 5 execution.** Gate 5 remains downstream of (i) a successful pre-run diagnostic re-attempt, (ii) a Gate 5 run-enablement memo v0.2, and (iii) a separate run-enablement / inert-restore cycle.
- **Count-feasibility run.** Runner guards remain `False`; no new run-enablement commit is issued by this memo.
- **Step 2 lock or Step 2 entry.** Step 2 remains blocked behind a separate Step 2 readiness step downstream of Gate 5 closure.
- **Market-data access.** Lane 2 market-data contact remains out of scope.
- **F4 modification, overwrite, deletion, or rename.** F4 at `results/lane2_gdelt1_count_feasibility/20260518T163302Z/` is canonical/consumed/untouched. The SHA-256 baseline in §2 must be re-verified by any successor diagnostic memo.
- **Runner guard flip.** `REAL_RETRIEVAL_ENABLED` and `COUNT_FEASIBILITY_AUTHORIZED` remain `False`.
- **Source pivot** or **fallback source selection.** GDELT 1.0 remains the Lane 2 source under the Gate 5 chain; a substrate-comparison memo (which would be one of the §15 stop-condition routes from `175e939`) is not invoked here.

Safety success at Gate 4C, Gate 4D, and during Turn B remains **necessary but not sufficient** for any subsequent Lane 2 step. The selection of Option A is **necessary but not sufficient** for the byte-capture authorization memo; that memo, when drafted, will be **necessary but not sufficient** for the byte-capture execution; and so on down the chain.

## 7. Recommended next artifact

**Gate 4C re-review / Turn B byte-capture authorization memo v0.1.** Suggested untracked path:

```
docs/lane2_gdelt1_gate4C_turn_b_byte_capture_authorization_memo_v0.1.md
```

(Exact path is a drafting decision; the suggestion above mirrors the naming convention used for the Gate 4C-family memos: `lane2_gdelt1_gate4C_*`.)

The next memo, when drafted, must at minimum:

- Argue its own ternary verdict (AUTHORIZE LATER / DEFER / FORBID) on its own grounds, not on this memo's Option A selection.
- Specify the byte-capture mechanism precisely: which extraction-path function would be augmented, what fields would be written to disk, what filename and directory the captured artifact would live at, and how the Gate 4C firewall guarantees (no real post-2022 filename surfacing; mandatory L5 regex scan) are preserved across the write path.
- Specify whether a second live GET is required, or whether the byte-capture mechanism can be exercised via a re-execution of an already-extracted in-memory artifact (the latter is impossible since Turn B's in-memory state is gone, so a second GET is likely required — and would require its own post-4C-style single-GET / no-retry / Gate 4D opener / inert-restore discipline analogous to `f8345c8`).
- Treat the F4 SHA-256 baseline in §2 as the canonical reference for any future diagnostic re-attempt.
- Inherit all anti-rescue clauses from the prior chain (no source pivot, no event-file fetch, no count-feasibility run, no Gate 5 entry).
- Carry its own self-status discipline per `feedback_handout_freshness.md` item 6.

## 8. Commit and push posture for this memo

**Commit posture.** Position 1 applies to the decision memo itself: write, review, pre-commit self-status cleanup if needed, then commit standalone as a citation-stable artifact before opening the next memo. The intended sequence is:

1. **Draft** — write the memo as a standalone decision artifact, no edits to any other file, no commit.
2. **Review** — read-only audit of this memo for clarity, scope discipline, non-authorization completeness, push-posture neutrality, and self-status wording.
3. **Pre-commit self-status cleanup** — apply `feedback_handout_freshness.md` item 6 to clean any stale self-status wording before commit.
4. **Commit** — stage exactly this file and commit it with a verbatim message to be specified at commit time. Suggested message form: `Record Lane 2 recognized-list remediation decision (Option A)`.

Then, and only then, the next memo (Gate 4C re-review / Turn B byte-capture authorization v0.1) may be drafted in a fresh separately initiated step. The reason for position 1 is the standard chain discipline: each artifact stands alone, is citation-stable on its own, and is reviewed in isolation before the next one opens.

**Push posture.** Push posture is a separate later decision and is not authorized by this memo. Current planning lean is posture 2: push after the subsequent Gate 4C re-review / Turn B byte-capture authorization memo is committed, so origin/main advances with the decision-plus-authorization pair rather than the decision alone. This is a planning lean only, not a push authorization; the push posture may still be revised in a separate later decision.

## 9. Cross-references

- Halt report: commit `d334ad5` (`docs/lane2_gdelt1_gate5_prerun_diagnostic_report_v0.1.md`), 213 lines, message `Record Lane 2 pre-run diagnostic precondition gap`.
- Pre-run diagnostic authorization memo: commit `d221e8f` (`docs/lane2_gdelt1_gate5_prerun_diagnostic_authorization_memo_v0.1.md`), verdict AUTHORIZE DIAGNOSTIC LATER, second-GET excluded.
- Gate 5 run-enablement memo: commit `175e939` (`docs/lane2_gdelt1_gate5_run_enablement_memo_v0.1.md`), verdict DEFER FOR DIAGNOSTIC, classification "requiring a pre-run diagnostic"; §§12–15 define the diagnostic envelope this remediation aims to feed.
- Gate 5 decision memo: commit `c2717a6` (`docs/lane2_gdelt1_gate5_decision_memo_v0.1.md`), verdict AUTHORIZE LATER.
- Gate 4C chain anchors (the layer this remediation targets): `54fb16a` authorization, `ec1c3ec` implementation, `e572c76` conformance review (PASS), Gate 4D `a2851f4` memo + `7f5caee` implementation + `9dea17c` conformance (PASS), post-4C `f8345c8` AUTHORIZE LATER EXECUTION.
- Turn B execution record (no committed artifact; transient stdout only): project memory `project_lane2_attention_spike.md` (no `M`/`A` on any tracked file; no new untracked entries; `LiveSafeExtraction` not serialized).
- F4 substrate: `results/lane2_gdelt1_count_feasibility/20260518T163302Z/` (canonical, consumed, untouched, SHA-256 baseline in §2).
- Handout-freshness discipline: `feedback_handout_freshness.md` item 6 — pre-commit self-status cleanup was applied to this memo's body per §8 step 3 before staging.

— end of recognized-list remediation decision memo v0.1 (Option A selected; byte-capture NOT AUTHORIZED; second-GET NOT AUTHORIZED; diagnostic-rerun NOT AUTHORIZED; Gate 5 NOT EXECUTED; F4 untouched; guards inert) —
