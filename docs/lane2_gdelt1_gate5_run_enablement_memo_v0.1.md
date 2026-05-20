# Lane 2 GDELT1 Gate 5 Run-Enablement Memo v0.1

## 1. Artifact status

**Run-enablement memo v0.1. Final verdict: DEFER FOR DIAGNOSTIC. Does NOT authorize Gate 5 execution; the diagnostic and any future count-only run each require separate authorization.**

Drafted 2026-05-20. Committed file at `docs/lane2_gdelt1_gate5_run_enablement_memo_v0.1.md`. This memo is the run-enablement artifact mandated by the Gate 5 decision memo at `c2717a6` §14. Its job is to **classify the 3647 vs 3650 substrate-coverage discrepancy** and select one of three verdicts that follows from that classification. It does **not** by itself fire any network request, run any protocol, modify any source / test / config / result file, stage, commit, push, flip any runner guard, or authorize Step 2, market data, or event-file requests.

The memo evaluates exactly one classification question. It does not pre-bake the answer; §7–§9 argue all three classifications on their strongest grounds before §10 selects one. §11 maps the chosen classification to a verdict label, §12–§15 specify the consequences of the chosen verdict, and §16–§19 carry forward the binding boundaries and future-run constraints from the Gate 5 decision memo so that no later artifact silently weakens them.

## 2. Current canonical state

- HEAD = origin/main = `c2717a6128738f526e9c0c4b5749f6cda18b7b7a`.
- Gate 5 decision memo v0.1 = **committed and pushed** at `c2717a6` (`docs/lane2_gdelt1_gate5_decision_memo_v0.1.md`); local amend predecessor `91a05ff` never reached origin and is unreachable from `main`.
- Gate 5 decision = **AUTHORIZE LATER**.
- Gate 5 execution = **NOT authorized.**
- Count-feasibility = **NOT run.**
- Runner guards inert: `REAL_RETRIEVAL_ENABLED = False` (`src/lane2_gdelt1_count_feasibility.py:647`); `COUNT_FEASIBILITY_AUTHORIZED = False` (`scripts/run_lane2_gdelt1_count_feasibility.py:44`).
- F4 = canonical / consumed / untracked / untouched at `results/lane2_gdelt1_count_feasibility/20260518T163302Z/` (`count_feasibility_metadata.json` 75,303 B + `feasibility_summary.md` 393 B; both mtime 2026-05-18 18:33; untracked-by-design).
- `60ec1521` / `fe742555` count-feasibility authorizations remain **spent**; no reuse.
- Tracked working tree clean (pre-existing untracked artifacts unrelated to this memo: `paper/main.*` LaTeX build outputs; `docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md` (DRAFT — NOT LOCKED, unrelated to Lane 2); `results/lane2_gdelt1_count_feasibility/` directory).
- Anchors carried forward from the decision memo: post-4C `f8345c8`, Gate 4D memo `a2851f4`, Gate 4D implementation `7f5caee`, Gate 4D conformance `9dea17c` (PASS), Turn A approval `991321d`, Gate 5 decision `c2717a6`. All real, committed, and pushed.

## 3. Mandate — decision-memo dependency

This memo is mandated by the Gate 5 decision memo v0.1 at `c2717a6`, specifically §14 (binding on any future run-enablement memo):

> The future Gate 5 run-enablement memo must explicitly address the 3647 vs 3650 discrepancy before any count-only run is authorized. It must decide whether the missing-unit structure can be handled inside the Gate 5 run/report design, or whether a separate pre-run enumeration diagnostic is required before locking that design.

and:

> The later run-enablement memo must not treat the 3-unit discrepancy as already resolved. It may classify the discrepancy as tolerable, blocking, or requiring a pre-run diagnostic, but it must make that classification explicitly before any run.

The Gate 5 decision memo also recorded (§13) that DEFER's strongest argument — timing — was acknowledged but routed here: *"if the run-enablement memo concludes a pre-run diagnostic is required, it will say so and pause for that diagnostic before locking the run; DEFER is therefore not foreclosed, it is positioned at the artifact where the design lock actually occurs."* This memo is that artifact. The classification choice here resolves where DEFER's timing argument lands.

## 4. Decision question

> **Is the 3647 vs 3650 substrate-coverage discrepancy tolerable, blocking, or requiring a pre-run diagnostic before any Gate 5 count-only run is authorized?**

The classification is a single ternary. Each branch maps to one verdict label in §11.

## 5. Evidence inherited from Turn B L1

Carried forward verbatim from the Gate 5 decision memo §5 (Turn B was executed 2026-05-20 under the Gate 4D redirect-disabled opener into the unchanged Gate 4C live-safe path at `DEFAULT_GDELT1_INDEX_URL` with `timeout = 30.0`; fired exactly once; no retry, no fallback, no second GET, no base `/events/` fallback, no event-file request/download, no source pivot, no count-feasibility run, no Gate 5 entry; no new commit produced by Turn B itself):

| Field | Value |
|---|---|
| Outcome class | **L1** |
| `recognized_in_window` (2005–2022) | **3647** |
| F4-canonical planned units | **3650** |
| Arithmetic difference | **−3 units** (≈0.082% of planned) |
| `ignored_out_of_window` | 26 |
| `rejected_2023plus` | 1216 (aggregated to non-identifying form-class label `daily_export`; zero filename retention) |
| `post2022_form_classes` | `['daily_export']` |
| `unrecognized_tokens` | 1 |
| `malformed_gdelt_tokens` | 0 |
| Mandatory L5 regex scan (post-2022 filename leakage) | **0 matches** |

Turn B did **not** enumerate which 3 planned units are missing, did **not** test whether the missing trio clusters in time, and did **not** check whether the gap is stable across calls. The single `unrecognized_tokens = 1` may or may not be one of the 3 missing units; Turn B's output does not resolve that linkage.

## 6. The three classification options

The Gate 5 decision memo §14 names the three legal classifications. They are repeated here as the legal moves available to this memo:

- **Tolerable** — the 3-unit gap can be handled inside the Gate 5 run/report design as it currently stands, given the universe choice (3650 planned vs 3647 recognized) and verdict-map design surfaced in the decision memo §8. No pre-run diagnostic is required. The run-enablement memo may proceed to lock the run design at v0.2 (or successor).
- **Blocking** — the 3-unit gap is severe enough that count-only feasibility cannot proceed under the current GDELT 1.0 source / path. Gate 5 is blocked; a separate substrate-comparison or source-pivot memo is required before any run-enablement memo can be drafted. Note: the Gate 5 decision memo §13 already rejected FORBID at the decision-memo level, so "blocking" here would be a *narrower* finding scoped to "the run-enablement memo cannot lock the run design under this gap," not a full FORBID at the source level.
- **Requiring a pre-run diagnostic** — the 3-unit gap is not severe enough to forbid Gate 5, but is unexplained enough that locking the Gate 5 run/report design *without first knowing the gap structure* would substitute plausibility for evidence. A small, bounded pre-run diagnostic is needed before the run-enablement memo can lock the run design. Crucially, the diagnostic itself is **not** a Gate 5 run.

Each is argued on its strongest grounds in §7–§9.

## 7. Case for "tolerable"

Strongest grounds:

- A 3-unit gap on 3650 (0.082%) is small in absolute terms; it is well within the publishing-cadence noise expected from a documented archival source. The GDELT 1.0 daily archive is known to have publishing irregularities; treating a sub-0.1% live-vs-planned drift as a hard pre-run blocker would functionally require a perfect publishing cadence that no real-world archival source provides.
- The Gate 5 decision memo §8 already identified two legitimate universe choices: 3650 planned (with `unit_absent` accounting in metadata and a "tolerable absentee count" verdict-map threshold) and 3647 recognized (with the 3 missing documented separately and outside the verdict map). Either is defensible without knowing which specific 3 dates are missing. Choosing "tolerable" at this memo lets the future run-enablement memo v0.2 lock one of those two universe choices and proceed.
- A Gate 5 run that includes missing-unit accounting (per the decision memo §17 required report fields) will produce the same enumeration the pre-run diagnostic would, plus the actual per-unit count data. The diagnostic, on this view, adds an artifact without producing decision-relevant evidence the run wouldn't also produce, while delaying the substrate-adequacy question Lane 2 has been blocked on since the Step 2 readiness memo named it as B+D.
- "Tolerable" preserves the Gate 5 decision memo's AUTHORIZE LATER spirit most directly: the per-unit-count half of the substrate adequacy question is the half Gate 5 is for, and "tolerable" lets it proceed.

Weakest form (to avoid): "the gap is 3 units, so it doesn't matter." That phrasing would bury the gap; the §10 chosen path here, if "tolerable" were selected, would still require explicit missing-unit accounting in the run and verdict-map design (§16–§17 carry that forward regardless of classification).

## 8. Case for "blocking"

Strongest grounds:

- The 3-unit gap is small but **unexplained**. If the 3 missing units are not random — for example, if they cluster in a specific GDELT 1.0 transition month, or all fall on a particular weekday, or correspond to a known archive-format change — that pattern itself is evidence the substrate has a structured availability defect that a count-only feasibility report cannot honestly summarize without naming it. Locking the run/report design without that information builds the count substrate on a foundation we have not actually verified.
- The Gate 5 decision memo §12 was explicit that GDELT 1.0 has documented publishing-cadence irregularities, and the original count-only protocol (`147c0d4` §3) said GDELT 1.0 should be used "only if longer history is needed." If the 3 missing units turn out to be evidence of a *systematic* shortfall (not just random gaps), the right move could be a substrate-comparison memo rather than continuing to build on GDELT 1.0.
- "Blocking" here is **narrower** than full FORBID. The Gate 5 decision memo's AUTHORIZE LATER stands; this memo would only be saying that the run-enablement step itself cannot be locked under the current gap evidence, and a different (substrate-comparison) memo is required before this memo's v0.2 can exist. That is consistent with the decision memo §13's framing of FORBID as requiring "affirmative new evidence, not absence of new positive evidence" — but blocking here would be making the narrower claim that the absence of explanation is itself the affirmative-evidence requirement.

Weakest form (to avoid): "0.08% is unacceptable on principle." That argument inflates a sub-0.1% gap to substrate veto and would also forbid most real-world archival sources. The correct "blocking" argument is the structured-defect-could-be-hiding-here argument, not the gap-size argument.

## 9. Case for "requiring a pre-run diagnostic"

Strongest grounds:

- The Gate 5 decision memo §11 framed DEFER's strongest argument as **timing**: *"if the 3647 vs 3650 gap changes the design of the count-only feasibility report or the interpretation of missingness, then the gap structure might need to be diagnosed before any Gate 5 run-enablement memo locks the run design."* That timing argument lands here, at this memo. The honest question is: can the run-enablement memo v0.2 design the run/report and verdict map *without first knowing whether the 3 missing units are random or systematic*? If the answer is "the design would meaningfully differ depending on that answer," then the diagnostic must come first.
- The diagnostic step that resolves this is **small, cheap, and substrate-safe**: it is a set-difference between the F4-canonical planned 3650-unit list and the Turn B recognized 3647-unit list, plus a check on whether the 3 missing dates cluster (by month, by weekday, by archive-format transition). It does *not* require event-file retrieval. It does *not* require a count run. It does *not* require a new live GET (it can operate on Turn B's already-captured output, or, if a second live index GET is later authorized through a fresh post-4C-style memo, on that output). It produces a small (~1-page) report and a recommendation for the universe choice.
- This option *preserves* the Gate 5 decision memo's AUTHORIZE LATER (Gate 5 remains decidable and on the path), it *honors* the decision memo's §11 timing concern (the gap is diagnosed before the lock, not during the run), and it *defers* only the lock of the run design — not the run itself — by one small artifact cycle. The diagnostic plays the same role here that Substep 1 and Substep 2A played at Phase B (small, bounded, decision-informing).
- "Requiring a pre-run diagnostic" also has a cleaner stop condition than "tolerable": if the diagnostic returns "the 3 missing units are random gaps with no clustering," the run-enablement memo v0.2 can proceed with confidence; if it returns "the 3 missing units cluster in [a specific structured pattern]," the v0.2 memo can design the run/verdict map to handle that pattern explicitly, or escalate to a substrate-comparison memo if the pattern is severe enough.

Weakest form (to avoid): "we should always wait for more information." That argument has no stopping rule. The "diagnostic" here is a specific bounded artifact with a specific termination condition (the diagnostic returns within one bounded step and either clears v0.2 or escalates).

## 10. Classification

**Requiring a pre-run diagnostic.**

Reasoning, weighing §7–§9 against the §3 mandate and the Gate 5 decision memo's §11 timing argument:

- The honest test is: would the run-enablement memo v0.2's design of the universe-and-verdict-map differ depending on whether the 3 missing units cluster systematically or scatter randomly? The answer is yes. If the 3 missing units are random scatter, universe=3647-recognized is the clean choice and the verdict map needs no special threshold. If the 3 missing units cluster (e.g., one specific archive-format transition), the run-enablement memo must either (a) define a "structural absentee" carve-out separate from the count-adequacy threshold, or (b) escalate to substrate-comparison. The right design genuinely depends on the diagnostic.
- "Tolerable" (§7) is the strongest *cost-minimization* argument and is not unreasonable, but it requires the run-enablement memo v0.2 to lock a universe choice now under unknown gap structure. The §11 timing argument from the decision memo specifically guarded against that: "discovering the structure during or after the run is too late if the structure was load-bearing for the lock."
- "Blocking" (§8) is principled in its narrower form but overshoots given current evidence. A 3-unit gap is consistent with random GDELT 1.0 publishing gaps; we have not yet seen evidence of structural defect. Blocking now would require treating "unknown" as "structurally defective," which substitutes pessimism for evidence in the same way "tolerable" can substitute optimism for evidence. The right path is to *find out*.
- A pre-run diagnostic is small (one set-difference, one clustering check), bounded (one artifact), and produces decision-relevant evidence that neither "tolerable" nor "blocking" can produce by argument alone. It is the move that *resolves* the §11 timing concern rather than papering over it.

The choice does not retroactively touch the Gate 5 decision memo's AUTHORIZE LATER. Gate 5 remains the authorized direction; this memo only refines the *order* of remaining steps: pre-run diagnostic first, then run-enablement memo v0.2 (or a substrate-comparison memo if the diagnostic finds a structural defect).

## 11. Final verdict label

**DEFER FOR DIAGNOSTIC.**

Three-way label set used by this memo: **AUTHORIZE RUN LATER** (tolerable) / **DEFER FOR DIAGNOSTIC** (requiring a pre-run diagnostic) / **BLOCK GATE 5** (blocking).

DEFER FOR DIAGNOSTIC means:

- This memo does **not** authorize a Gate 5 count-only feasibility run.
- This memo does **not** authorize a new live index GET, an event-file request, a market-data load, or a Step 2 entry.
- This memo does **not** flip `REAL_RETRIEVAL_ENABLED` or `COUNT_FEASIBILITY_AUTHORIZED`.
- This memo does **not** modify F4.
- This memo **defines** a small bounded pre-run diagnostic (§12) that may be authorized in a future *separate* prompt.
- The pre-run diagnostic, if later authorized, is bounded by §13 (what is permitted) and §14 (what is forbidden). It is not Gate 5 execution; it is an enumeration artifact.
- After the pre-run diagnostic returns, this memo's v0.2 (or a clearly-named successor) re-enters with the diagnostic evidence in hand and either locks the Gate 5 run design (AUTHORIZE RUN LATER — v0.2's own ternary, distinct from this memo's verdict) or escalates (BLOCK GATE 5 / substrate-comparison memo).

## 12. Definition and scope of the pre-run diagnostic

The pre-run diagnostic is a **single bounded artifact** that resolves the 3647 vs 3650 gap structure without entering Gate 5 execution. It is *not* itself a Gate 5 run. Its scope is exactly:

1. **Set difference.** Enumerate the F4-canonical planned 3650-unit list (already recorded in `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json`, which is untracked-but-canonical) against the Turn B recognized 3647-unit list (recovered from Turn B's already-captured stdout under the Gate 4C non-disguise discipline, with form-class only and no real post-2022 filename surfacing). Identify exactly which 3 planned units are absent from the recognized set.
2. **Clustering check.** For the 3 absent units, test whether they cluster by: (a) calendar month, (b) calendar weekday, (c) proximity to a known GDELT 1.0 archive-format transition (the 2013-04-01 daily / monthly switch and any documented subsequent format changes). Report observed counts; do not run hypothesis tests at this stage; this is a small descriptive check, not an inferential one.
3. **Replication hint, if a future second live GET is separately authorized.** *Optional and not authorized by this memo.* If a future separate prompt authorizes a second live index GET under a fresh post-4C-style authorization, the diagnostic may compare the second GET's recognized-in-window count against Turn B's `3647` to test stability of the gap. This optional step requires its own authorization and is **not** authorized here.

The diagnostic produces a small report at `docs/lane2_gdelt1_gate5_prerun_diagnostic_report_v0.1.md` (suggested path; uncommitted at first draft, as this memo was at its first draft). The report contains: (a) the 3 absent unit identifiers under Gate 4C non-disguise discipline (form-class only; no identifying real post-2022 filenames anywhere, including for in-window units the report's regex scan must still pass with 0 matches against the standard pattern); (b) the clustering observations; (c) a recommendation for the universe choice in run-enablement v0.2.

## 13. What the diagnostic is permitted to do

Permitted, if and only if separately authorized in a future prompt:

- Read the F4-canonical metadata at `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json` (canonical/consumed/untouched; reading is allowed, modification is not).
- Read Turn B's already-captured stdout (under Gate 4C non-disguise discipline).
- Compute the set difference (planned 3650 ∖ recognized 3647).
- Compute small descriptive clustering statistics on the 3 absent unit dates.
- Produce a small report file under `docs/` with the Gate 4C non-disguise discipline preserved.
- Memory may be updated after the report is committed and pushed, under standing memory-update discipline.

## 14. What the diagnostic is forbidden from doing

Forbidden under any future authorization scope:

- No new live GET of any GDELT URL (optional Section 12.3 replication requires its own separate authorization analogous to post-4C `f8345c8`).
- No event-file request or download under any condition.
- No market-data access.
- No Step 2 entry.
- No count-feasibility run (the diagnostic is enumeration only; it does not compute per-unit event counts).
- No modification of F4 directory contents.
- No flip of `REAL_RETRIEVAL_ENABLED` or `COUNT_FEASIBILITY_AUTHORIZED`.
- No reuse of spent count-feasibility authorizations (`60ec1521` / `fe742555`).
- No surfacing of real post-2022 filenames in any of the 9 Gate 4C channels; the report must include a mandatory L5 regex scan (pattern `\b\d{8,14}\.(?:export|gkg|mentions)\.(?:CSV|csv)\.zip\b`) with 0 matches against the captured report stdout and report body.
- No design lock of the Gate 5 run/report. The diagnostic informs the lock; the lock happens in run-enablement v0.2 or successor.
- No promotion of "diagnostic returned no clustering" to "Gate 5 run can fire." Even a clean diagnostic only authorizes drafting the run-enablement v0.2; the run requires its own separately committed authorization downstream of v0.2.

## 15. Stop conditions

The pre-run diagnostic must stop and escalate (no auto-proceed) if any of the following are observed:

- The set-difference operation cannot be performed because the F4-canonical metadata is missing, corrupted, or mtime-changed from the recorded `2026-05-18 18:33` (would imply F4 contamination → halt and report).
- The 3 absent units exceed the 0.082% size when re-derived (e.g., set difference returns more than 3 missing units → halt, report, and require a substrate-comparison memo).
- The set-difference returns fewer than 3 missing units (e.g., 0, 1, or 2 → halt and re-verify). That result contradicts Turn B's `recognized = 3647` vs `F4-canonical = 3650` arithmetic and should route to a Gate 4C re-review / Turn B re-verification memo rather than auto-proceed; the symmetric arithmetic-mismatch case is not silently absorbed.
- A real post-2022 filename appears in any channel of the diagnostic's output (Gate 4C firewall breach → halt, report, do not commit the diagnostic, and require a Gate 4C re-review memo).
- Clustering check returns a strong structural pattern (e.g., all 3 absent units share a single calendar month / single weekday / single archive-format-transition window) → halt the auto-path to run-enablement v0.2 and route to a substrate-comparison memo or a narrowly-scoped run-enablement v0.2 that explicitly handles the structural pattern; either way, the choice is a separate decision.

If none of the stop conditions fire, the diagnostic's output authorizes drafting (not running) the Gate 5 run-enablement memo v0.2.

## 16. Future Gate 5 run constraints (carried forward from decision memo §14)

These constraints bind any later run-enablement memo v0.2 and any Gate 5 run that follows it. They are inherited unchanged from the Gate 5 decision memo §14 and are repeated here so this memo is self-contained:

- The Gate 5 run is **one-run-only.** A technical/protocol failure at the run does not authorize a patch-and-rerun; it routes to a fresh, separately authorized memo.
- `COUNT_FEASIBILITY_AUTHORIZED` remains `False` until separately flipped by an explicit committed run-enablement step (analogous to `60ec152` → `fe74255` → `9e329c2` inert-restore pattern; `60ec152` and `fe74255` are spent and may not be reused).
- `REAL_RETRIEVAL_ENABLED` is **not flipped** by this memo, and any decision to flip it lives in run-enablement v0.2 (or a successor enabling memo) plus a separately committed run-enablement commit, not here.
- **No event-file download** outside the future locked Gate 5 run path. Gate 5 is index-and-count-only against units already exposed by the index, not event-file retrieval; even within the future locked run, event-file URL requests are forbidden unless explicitly re-authorized in a separate step.
- **No market data.** Lane 2 market-data contact remains out of scope.
- **No Step 2 lock.** Step 2 remains blocked behind a separate Step 2 readiness step that can only run after Gate 5 produces interpretable counts.
- **No F4 overwrite.** F4 at `results/lane2_gdelt1_count_feasibility/20260518T163302Z/` is canonical/consumed/untouched. The new run artifact must be timestamped **separately** from F4 and must not write to the F4 directory.
- The new run artifact directory name must follow the established pattern (`results/lane2_gdelt1_count_feasibility/<NEW_TIMESTAMP>Z/`) with a timestamp distinct from `20260518T163302Z`.
- The run-enablement v0.2 memo must explicitly resolve the §8 universe question (3650 planned vs 3647 recognized) **using the diagnostic evidence**, and must explicitly state the verdict map for partial coverage, including thresholds for "tolerable absentee count" if the universe is 3650.
- The run-enablement v0.2 memo must not treat the 3-unit discrepancy as already resolved by this memo; it inherits the diagnostic's evidence and must classify on that evidence.
- Old F4 record remains consumed and untouched. Any reuse, overwrite, or "merge with F4" is forbidden.

## 17. Required future report fields if Gate 5 is later authorized

Carried forward from the Gate 5 decision memo §17 and **augmented** with diagnostic-derived fields. Any future Gate 5 run report must include, at minimum:

- **Recognized unit universe used** — explicitly state whether the universe was 3650 planned, 3647 recognized, or some other documented choice; cite the authorizing memo (run-enablement v0.2) and the pre-run diagnostic report for the choice.
- **Pre-run diagnostic reference** — commit hash and path of the pre-run diagnostic report that informed the universe choice and verdict map.
- **Expected vs actual count** per unit — `unit_id`, `expected`, `actual`, `delta`.
- **Missing-unit accounting** — explicit enumeration of any planned units absent from the live index *at run time*, with form-class only (no identifying filenames), the same firewall discipline as Turn B; report whether each is one of the 3 originally absent units, a new absentee, or a returned unit.
- **Whether the 3-unit discrepancy persists** — yes/no relative to the diagnostic-time absentee set, with explicit identity comparison.
- **Diagnostic-flagged structural pattern carryover** — if the pre-run diagnostic flagged a structural pattern in the 3 absentees, the run report must explicitly say whether the run honored the pattern-aware design or violated it.
- **Event-file request count** — must be `0` unless the run-enablement v0.2 memo explicitly authorized event-file retrieval (it should not).
- **Event-file success / failure counts** — `0/0` if no event-file requests fired; otherwise explicit pass/fail count.
- **No post-2022 leakage confirmation** — mandatory L5 regex scan result against the captured run stdout / logs; pattern at least `\b\d{8,14}\.(?:export|gkg|mentions)\.(?:CSV|csv)\.zip\b`; matches must be 0.
- **F4 untouched confirmation** — `count_feasibility_metadata.json` and `feasibility_summary.md` at `results/lane2_gdelt1_count_feasibility/20260518T163302Z/` unmodified (size, mtime, and SHA-256 if available).
- **Guards state** at run start, during run, and at run end — `REAL_RETRIEVAL_ENABLED`, `COUNT_FEASIBILITY_AUTHORIZED`, and any other guard introduced by the run-enablement step.
- **Whether Step 2 remains blocked or becomes eligible** — explicit yes/no based on the Gate 5 verdict map; Step 2 eligibility decision is the next memo's question, not Gate 5's, but Gate 5's output must say whether the *feasibility precondition* is satisfied.

The report must use the Gate 4C non-disguise discipline (no identifying real post-2022 filenames in any channel) and must be timestamped distinctly from F4.

## 18. One-run-only and inert-restore discipline

If a future Gate 5 run is separately authorized (post-diagnostic, post-run-enablement v0.2), the run honors the inert-restore pattern established at the prior count-feasibility cycle (`60ec152` → `fe74255` → `9e329c2`):

- A separately committed run-enablement commit flips `COUNT_FEASIBILITY_AUTHORIZED` to `True` (analogous to `fe74255`).
- The run executes **exactly once**.
- A separately committed inert-restore commit flips `COUNT_FEASIBILITY_AUTHORIZED` back to `False` (analogous to `9e329c2`) immediately after the run completes (success or failure).
- If the run fails technically/protocol-wise, the failure routes to F5 / human review; no patch-and-rerun without a fresh memo.
- `REAL_RETRIEVAL_ENABLED` is handled analogously by the run-enablement v0.2 / inert-restore pair; this memo does not pre-resolve which sequence applies.

## 19. Non-authorization boundaries

This memo does **not** authorize, by itself, any of the following. None of these become permitted by `DEFER FOR DIAGNOSTIC`; each requires its own separate explicit authorization:

- the pre-run diagnostic execution (the diagnostic is *defined* here, not run here)
- count-feasibility execution
- event-file request / download
- market-data access
- Step 2 lock or Step 2 entry
- Gate 5 run-enablement v0.2 (the diagnostic comes first; v0.2 cannot be drafted under §15 stop conditions)
- runner guard flip (`REAL_RETRIEVAL_ENABLED`, `COUNT_FEASIBILITY_AUTHORIZED` remain `False`)
- F4 modification, overwrite, deletion, or rename
- source pivot
- fallback source selection
- a new live GET of any GDELT URL (the post-4C `f8345c8` AUTHORIZE LATER EXECUTION was spent by Turn B; any future GET requires a fresh memo + fresh approval, including an optional second-GET replication step under §12.3)

Safety success at Gate 4C, Gate 4D, and during Turn B is **necessary but not sufficient** for Gate 5 warrant. The Gate 5 decision memo's AUTHORIZE LATER is **necessary but not sufficient** for the pre-run diagnostic or the Gate 5 run. This memo treats both accordingly.

## 20. Final verdict

**DEFER FOR DIAGNOSTIC.** The 3647 vs 3650 substrate-coverage discrepancy is classified as **requiring a pre-run diagnostic** before any Gate 5 run-enablement memo can lock the Gate 5 run design. A 3-unit gap on 3650 (0.082%) is too small to forbid Gate 5 and too unexplained to absorb into a v0.2 design lock without first knowing whether the missing trio is random scatter or structured shortfall. The diagnostic that resolves this — a bounded set-difference and clustering check against Turn B's already-captured output, with no event-file contact, no count run, no market data, and no F4 touch — is defined in §12, scoped by §13–§14, and gated by the §15 stop conditions. The diagnostic itself is not authorized by this memo; a separate prompt is required to authorize its execution. The diagnostic's report, once committed, conditions the drafting (not running) of Gate 5 run-enablement v0.2; the Gate 5 run itself remains downstream of v0.2 and its own separately committed run-enablement / inert-restore cycle (§18). The Gate 5 decision memo's AUTHORIZE LATER stands; this memo refines the order of the remaining steps without weakening any of its constraints (§16–§19 inherit them all unchanged). Gate 5 remains decidable; the route to deciding it now passes through one small diagnostic artifact.

— end of Gate 5 run-enablement memo v0.1 (committed; Gate 5 NOT EXECUTED; diagnostic NOT EXECUTED) —
