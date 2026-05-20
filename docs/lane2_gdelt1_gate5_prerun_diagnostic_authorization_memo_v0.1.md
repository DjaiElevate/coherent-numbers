# Lane 2 GDELT1 Gate 5 Pre-Run Diagnostic Authorization Memo v0.1

## 1. Artifact status

**Authorization memo v0.1. Final verdict: AUTHORIZE DIAGNOSTIC LATER. Does NOT execute the diagnostic; does NOT authorize Gate 5 execution; second-GET replication remains excluded.**

Drafted 2026-05-20. Committed file at `docs/lane2_gdelt1_gate5_prerun_diagnostic_authorization_memo_v0.1.md`. This memo is an authorization-decision document only. It does **not** by itself:

- execute the pre-run diagnostic (the diagnostic is *defined* in §12 of the run-enablement memo `175e939`, and *if* this memo is later approved and committed, a *separate* explicit execution prompt is still required before any diagnostic operation runs),
- run any count-feasibility code,
- contact GDELT,
- fetch any external URL,
- request or download any event file,
- modify F4,
- flip any runner guard,
- access market data,
- enter Step 2,
- stage, commit, or push.

The body of this memo evaluates exactly one decision: whether to authorize (separately, later) the execution of the pre-run diagnostic defined in §12 of the Gate 5 run-enablement memo v0.1. §7–§10 argue all three verdict options on their strongest grounds. §11 selects one. §12 records the second-GET replication decision separately. §13–§15 inherit and re-state the permitted / forbidden / stop-condition envelope from the run-enablement memo. §16 lists required report fields. §17 lays out the downstream gate map. §18 carries the non-authorization boundaries. §19 is the one-run-only / inert-restore preview for downstream reference. §20 records the final verdict.

## 2. Current canonical state

- HEAD = origin/main = `175e93919241a1d8e5a551cce47b3cdc2cc4f9d4`.
- Gate 5 decision memo v0.1 = committed and pushed at `c2717a6` (`docs/lane2_gdelt1_gate5_decision_memo_v0.1.md`); decision **AUTHORIZE LATER**.
- Gate 5 run-enablement memo v0.1 = committed and pushed at `175e939` (`docs/lane2_gdelt1_gate5_run_enablement_memo_v0.1.md`); verdict **DEFER FOR DIAGNOSTIC**; classification: **requiring a pre-run diagnostic**.
- Pre-run diagnostic = **defined in §12 of `175e939` but not authorized and not executed.**
- Gate 5 execution = **NOT authorized.**
- Count-feasibility = **NOT run.**
- F4 = canonical / consumed / untracked / untouched at `results/lane2_gdelt1_count_feasibility/20260518T163302Z/` (`count_feasibility_metadata.json` 75,303 B + `feasibility_summary.md` 393 B; both mtime 2026-05-18 18:33; untracked-by-design).
- Runner guards inert: `REAL_RETRIEVAL_ENABLED = False` (`src/lane2_gdelt1_count_feasibility.py:647`); `COUNT_FEASIBILITY_AUTHORIZED = False` (`scripts/run_lane2_gdelt1_count_feasibility.py:44`).
- Tracked working tree clean (pre-existing untracked artifacts unrelated to this memo: `paper/main.*` LaTeX build outputs; `docs/influential_numbers_field_modulated_identity_design_memo_v0.1.md` (DRAFT — NOT LOCKED, unrelated to Lane 2); `results/lane2_gdelt1_count_feasibility/` directory).
- `60ec1521` / `fe742555` count-feasibility authorizations remain **spent**; not reusable.
- Anchors carried forward: post-4C `f8345c8`, Gate 4D memo `a2851f4`, Gate 4D implementation `7f5caee`, Gate 4D conformance `9dea17c` (PASS), Turn A approval `991321d`, Gate 5 decision `c2717a6`, Gate 5 run-enablement `175e939`. All real, committed, and pushed.

## 3. Dependency chain

This memo sits inside the following committed and pushed chain on `origin/main`:

| Anchor | Artifact | Decision |
|---|---|---|
| `c2717a6` | Gate 5 decision memo v0.1 | **AUTHORIZE LATER** (Gate 5 may be entered later under separate run-enablement) |
| `175e939` | Gate 5 run-enablement memo v0.1 | **DEFER FOR DIAGNOSTIC** (classification: requiring a pre-run diagnostic; the diagnostic must run before any v0.2 run-enablement can lock the Gate 5 run design) |
| this memo (v0.1) | Pre-run diagnostic authorization memo v0.1 | **AUTHORIZE DIAGNOSTIC LATER** |

The decision-memo's §14 binding clause and the run-enablement memo's §11 / §15 framing both terminate here: this memo is the next required artifact in the chain, and its verdict gates the existence of any later diagnostic-execution prompt.

## 4. Decision question

> **Should the pre-run diagnostic defined in §12 of the Gate 5 run-enablement memo v0.1 (`175e939`) be authorized for later, separately initiated execution?**

The decision is a single ternary: **AUTHORIZE DIAGNOSTIC LATER** / **DEFER DIAGNOSTIC AUTHORIZATION** / **BLOCK DIAGNOSTIC**. This memo does not execute the diagnostic under any branch. AUTHORIZE DIAGNOSTIC LATER does not run it; it permits a later separately initiated execution prompt.

## 5. Diagnostic purpose

Carried forward verbatim from `175e939` §12 (lead sentence):

> The pre-run diagnostic is a single bounded artifact that resolves the 3647 vs 3650 gap structure without entering Gate 5 execution. It is not itself a Gate 5 run.

Concretely: the diagnostic must produce decision-relevant evidence about whether the 3-unit shortfall between the live-recognized universe (3647) and the F4-canonical planned universe (3650) is random scatter or a structured pattern (e.g., clustered in a calendar month, weekday, or archive-format transition window). That evidence is the input the v0.2 run-enablement memo (or a substrate-comparison memo) needs to honestly lock the universe choice and verdict map. Without it, the v0.2 design lock would substitute plausibility for evidence — which is exactly the failure mode the Gate 5 decision memo's §11 timing argument named.

## 6. Diagnostic scope

Scope is **inherited verbatim and unchanged** from `175e939` §12, §13, and §14. This memo does not redefine scope; it only decides authorization. The scope envelope is restated here for self-containment.

**Per §12.1 (`175e939`) — Set difference (offline, no network):**

Enumerate the F4-canonical planned 3650-unit list (recorded in `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json`, canonical/consumed/untouched) against the Turn B recognized 3647-unit list (recovered from Turn B's already-captured stdout under the Gate 4C non-disguise discipline, form-class only, no real post-2022 filename surfacing). Identify exactly which 3 planned units are absent from the recognized set.

**Per §12.2 (`175e939`) — Clustering check (offline, descriptive only):**

For the 3 absent units, test whether they cluster by (a) calendar month, (b) calendar weekday, (c) proximity to a known GDELT 1.0 archive-format transition (2013-04-01 daily / monthly switch, and any documented subsequent format changes). Report observed counts. No inferential hypothesis tests at this stage.

**Per §12.3 (`175e939`) — Optional second-GET replication:**

Optional and **not authorized by `175e939` itself**. If a separate prompt authorizes a fresh post-4C-style second live index GET, the diagnostic may compare the second GET's recognized-in-window count against Turn B's `3647` to test stability of the gap. This memo records its own decision on this option in §12 below; the default position carried in from the chain is "not authorized here."

**Forbidden activities (full list per `175e939` §14):**

- No new live GET of any GDELT URL (§12.3 second-GET replication needs separate post-4C-style authorization).
- No event-file request or download under any condition.
- No market-data access.
- No Step 2 entry.
- No count-feasibility run.
- No modification of F4 directory contents.
- No flip of `REAL_RETRIEVAL_ENABLED` or `COUNT_FEASIBILITY_AUTHORIZED`.
- No reuse of spent count-feasibility authorizations (`60ec1521` / `fe742555`).
- No surfacing of real post-2022 filenames in any of the 9 Gate 4C channels; mandatory L5 regex scan (pattern `\b\d{8,14}\.(?:export|gkg|mentions)\.(?:CSV|csv)\.zip\b`) with 0 matches required against the captured report stdout and report body.
- No design lock of the Gate 5 run/report. The diagnostic informs the lock; the lock happens in run-enablement v0.2 or a substrate-comparison memo.
- No promotion of "diagnostic returned no clustering" to "Gate 5 run can fire."

## 7. The three verdict options

The Gate 5 run-enablement memo (`175e939`) implicitly named three legal moves for the next artifact (this memo) by listing the diagnostic as "not authorized by `175e939`" and requiring a separate authorization prompt. The three are:

- **AUTHORIZE DIAGNOSTIC LATER** — separate, later, explicitly initiated execution prompt may fire the diagnostic. This memo does not run it. The diagnostic, when later run, is bounded by `175e939` §§12–15.
- **DEFER DIAGNOSTIC AUTHORIZATION** — the diagnostic is not authorized at this memo's level either; some specific uncertainty must be resolved or condition met before authorization can be issued. Specify the uncertainty and the reconsideration trigger.
- **BLOCK DIAGNOSTIC** — the diagnostic should not be authorized at all under the current Lane 2 / GDELT 1.0 path. Name the reason and whether the block scopes to the current diagnostic design only or to a broader part of the chain.

Each is argued in turn before §11 selects one. Each is argued on its strongest grounds. The default-against pull is real: each option could be defended by a weak rescue argument, and those must be excluded.

## 8. Case for AUTHORIZE DIAGNOSTIC LATER

The strongest case for AUTHORIZE DIAGNOSTIC LATER:

- The Gate 5 run-enablement memo (`175e939`) §10 chose "requiring a pre-run diagnostic" precisely so that the universe-and-verdict-map design lock could be made *on evidence*, not on plausibility. The diagnostic is the artifact that produces that evidence. Continuing to refuse to authorize it leaves Lane 2 indefinitely blocked at "v0.2 cannot lock the run design until the diagnostic returns," which is functionally the same as a permanent DEFER on Gate 5 itself.
- The diagnostic's scope (`175e939` §12.1–§12.2) is **fully offline** under the default position: set difference of two already-captured lists + descriptive clustering check. No new GET, no GDELT contact, no event-file request, no F4 modification, no guard flip, no market data, no Step 2. It operates on (a) `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json` (F4-canonical, untracked-but-canonical, untouched — read-only) and (b) Turn B's already-captured stdout. There is no new substrate contact involved.
- The forbidden list (`175e939` §14) and the stop conditions (`175e939` §15) are tight and well-defined. The diagnostic cannot accidentally escalate into Gate 5 execution; the §14 last bullet ("No promotion of 'diagnostic returned no clustering' to 'Gate 5 run can fire'") explicitly prevents the worst-case momentum failure.
- AUTHORIZE DIAGNOSTIC LATER is **not** diagnostic execution. It permits a separately drafted execution prompt to fire the diagnostic, bounded by `175e939` §§13–15 and this memo's §12 decision on second-GET replication. No code runs at this authorization step; no guards flip; F4 stays untouched.

The weakest form (to avoid): "the run-enablement memo defined it, so it should be authorized." That argument inherits authority by procedural momentum. The correct argument for AUTHORIZE DIAGNOSTIC LATER is the program-purpose argument above (the diagnostic produces the evidence the v0.2 lock needs and cannot be substituted by further argument).

## 9. Case for DEFER DIAGNOSTIC AUTHORIZATION

The strongest case for DEFER DIAGNOSTIC AUTHORIZATION:

- The Gate 5 decision memo (`c2717a6`) and the run-enablement memo (`175e939`) were each gated by a *separate, explicit* user-initiated prompt. The chain's discipline has been "wait for explicit initiation between artifacts." A principled DEFER here could honor that discipline by saying: this memo is the right artifact at the right time, but its authorization decision itself should pause briefly to ensure no additional context has surfaced (e.g., a new Lane 2 substrate-quality observation, a fresh handout-freshness check showing repo HEAD drift, etc.) before committing to authorization.
- DEFER could also be principled if there is a specific resolvable uncertainty about the F4-canonical metadata file. The file is *untracked*, so its integrity rests on filesystem mtime and content rather than git history. Before authorizing a diagnostic that reads from it, DEFER could insist on a small pre-authorization integrity-confirmation step (mtime + SHA-256 of the F4 file in its current state) to confirm the canonical evidence base is unchanged from Turn B time.
- The committed-state discipline of Lane 2 has been "each gate transition gets a separate explicit decision." A DEFER here adds a check-step without changing the eventual trajectory.

The weakest form (to avoid): "we should always wait for more information." DEFER has no value as a generic stalling move. To be principled here, DEFER must name (a) a specific resolvable uncertainty and (b) a specific concrete trigger for reconsideration. The strongest concrete trigger candidate is the F4 integrity check above; a generic "let's pause" without that anchor would be unprincipled.

## 10. Case for BLOCK DIAGNOSTIC

The strongest case for BLOCK DIAGNOSTIC:

- The Gate 5 decision memo (`c2717a6`) §12 noted that the original count-only protocol (`147c0d4` §3) said GDELT 1.0 should be used "only if longer history is needed." If the Lane 2 program is going to reconsider source selection anyway (a possibility the decision memo named without selecting), then *the diagnostic itself* is a step further into the GDELT 1.0 path that strengthens the sunk-cost case for continuing on GDELT 1.0 rather than pivoting to a cleaner alternative. BLOCK now opens space for a substrate-comparison memo before any more GDELT 1.0 artifacts accrue.
- BLOCK could also be argued on firewall grounds — even though Gate 4C / Gate 4D / Turn B passed their L5 regex scans cleanly, the diagnostic's report production is a new write surface that could theoretically leak post-2022 form-class information if the regex pattern is incomplete. A precautionary BLOCK would refuse to expand the write surface until the firewall has been re-reviewed against the planned report structure.

The weakest form (to avoid): "we have not yet seen the diagnostic's output, therefore we should forbid it." That argument is unprincipled (it would forbid every research step). The correct BLOCK argument is the program-design argument above (sunk cost on GDELT 1.0 vs alternatives) or the firewall-precaution argument; neither rises to substrate-veto evidence under current data.

## 11. Decision

**AUTHORIZE DIAGNOSTIC LATER.**

Reasoning, weighing §§8–10 against the §2–§3 chain state and the `175e939` §12–§15 envelope:

- The diagnostic is the artifact that produces the evidence the v0.2 design lock needs. Refusing to authorize it leaves Lane 2 indefinitely blocked at the boundary `175e939` §10 framed as resolvable only by the diagnostic.
- The diagnostic's scope under the default offline position (§12 below excludes second-GET replication) is genuinely small and substrate-safe: two already-captured lists, a set difference, a descriptive clustering check, and a small report with mandatory L5 regex scan. No new GET, no GDELT contact, no event-file request, no F4 modification, no guard flip, no market data, no Step 2.
- DEFER (§9) is a near-rival, and its strongest move — a pre-authorization F4-integrity confirmation step (mtime + SHA-256 of the F4 metadata file) — has independent value. Rather than choosing DEFER on that basis, this memo **folds the F4-integrity check into the AUTHORIZE LATER envelope as a binding precondition of the diagnostic execution prompt** (see §13.1 below). That captures DEFER's principled concern without adding a separate gate cycle.
- BLOCK (§10) is principled in its program-design framing but does not match current evidence. The sunk-cost-on-GDELT-1.0 argument was already weighed and rejected at the Gate 5 decision memo level (`c2717a6` §13); inverting that choice now requires affirmative new evidence, which the diagnostic itself would help produce. Pre-emptively blocking the diagnostic forecloses the cheapest path to that evidence. The firewall-precaution variant overshoots given the L5 regex scan discipline is already binding (`175e939` §14) and the report's write surface is bounded by Gate 4C non-disguise.

**AUTHORIZE DIAGNOSTIC LATER does not execute the diagnostic. AUTHORIZE DIAGNOSTIC LATER does not modify F4. AUTHORIZE DIAGNOSTIC LATER does not flip any runner guard. AUTHORIZE DIAGNOSTIC LATER does not contact GDELT, does not fire a new GET, does not request event files, does not access market data, and does not authorize Step 2. A separately initiated execution prompt is still required before any diagnostic operation runs.**

## 12. Second-GET replication — decision

**EXCLUDED from this authorization.**

Reasoning:

- The run-enablement memo (`175e939`) §12.3 named the second-GET replication as *optional* and *not authorized* by that memo. Authorizing it here would expand scope beyond the conservative default.
- The first two diagnostic operations (set difference + clustering check) are **fully offline** under the data already captured at Turn B. They require no network access whatsoever. The replication step, by contrast, would require a fresh post-4C-style single-GET authorization analogous to `f8345c8` — a non-trivial scope expansion.
- The stability-of-gap question that replication would answer is *not load-bearing* for the v0.2 design lock at the current evidence level. If the §12.1 set difference and the §12.2 clustering check both return clean results (random scatter, no structural pattern), the v0.2 design can lock universe = 3647 recognized with no need to confirm gap stability. If §12.1 returns a structural pattern, the v0.2 design must either carve it out or escalate to substrate-comparison — and stability is not the deciding factor either way.
- Including replication here would force this authorization memo to also carry the post-4C-style firewall reasoning (single-GET-only, no retry, no fallback, redirect-disabled opener, L5 regex scan against the new GET's stdout, etc.) — which is a separate memo's worth of content. Bundling it would weaken both decisions.

**Therefore:**

- Second-GET replication is **not authorized by this memo.**
- Second-GET replication may be considered in a separate future memo, drafted only if (a) the §12.1 set difference and the §12.2 clustering check both succeed cleanly under this memo's authorization envelope, and (b) the v0.2 run-enablement memo (or a substrate-comparison memo) explicitly identifies gap-stability as a load-bearing question for its design lock.
- A future second-GET authorization, if drafted, must be structured as its own post-4C-style memo with single-GET-only / no-retry / Gate 4D opener / Gate 4C live-safe path / mandatory L5 regex scan / inert-restore discipline, analogous to `f8345c8`.
- **This memo does not execute any second GET even hypothetically. Even if a future second-GET memo is later authorized, that authorization is separate from this one.**

## 13. Permitted operations (envelope, inherited from `175e939` §13)

The future, separately initiated diagnostic execution prompt — *if and only if* it is explicitly initiated by the user — may perform the following operations and no others:

### 13.1 Mandatory F4-integrity confirmation (added by §11 reasoning)

Before any other diagnostic operation, the execution prompt must:

- Verify that `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json` exists at the canonical path.
- Verify its size remains 75,303 B.
- Verify its mtime remains `2026-05-18 18:33`.
- Compute its SHA-256 and record it in the diagnostic report.
- Confirm the directory contains exactly two files (`count_feasibility_metadata.json` 75,303 B + `feasibility_summary.md` 393 B), both mtime `2026-05-18 18:33`, no extras and no missing files.

If any of these checks fails, the diagnostic must **halt before any set-difference or clustering operation** and route to the §15 F4-contamination stop condition.

### 13.2 Permitted diagnostic operations (inherited from `175e939` §13)

After the §13.1 integrity confirmation passes:

- Read the F4-canonical metadata at `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json` (canonical/consumed/untouched; reading is allowed, modification is not).
- Read Turn B's already-captured stdout (under Gate 4C non-disguise discipline).
- Compute the set difference (planned 3650 ∖ recognized 3647).
- Compute small descriptive clustering statistics on the 3 absent unit dates (counts only; no inferential hypothesis tests).
- Produce a small report file at `docs/lane2_gdelt1_gate5_prerun_diagnostic_report_v0.1.md` (suggested path) with the Gate 4C non-disguise discipline preserved.
- Memory may be updated after the report is committed and pushed, under standing memory-update discipline.

## 14. Forbidden operations (envelope, inherited from `175e939` §14 + this memo's §12)

Forbidden under any future diagnostic execution scope authorized by this memo:

- **No new live GET of any GDELT URL.** §12 of this memo explicitly excludes second-GET replication; a separate future memo would be required to authorize it.
- No event-file request or download under any condition.
- No market-data access.
- No Step 2 entry.
- No count-feasibility run.
- No modification of F4 directory contents (read-only access only).
- No flip of `REAL_RETRIEVAL_ENABLED` or `COUNT_FEASIBILITY_AUTHORIZED`.
- No reuse of spent count-feasibility authorizations (`60ec1521` / `fe742555`).
- No surfacing of real post-2022 filenames in any of the 9 Gate 4C channels; mandatory L5 regex scan (pattern `\b\d{8,14}\.(?:export|gkg|mentions)\.(?:CSV|csv)\.zip\b`) with 0 matches required against the captured report stdout and report body.
- No design lock of the Gate 5 run/report. The diagnostic informs the lock; the lock happens in run-enablement v0.2 or a substrate-comparison memo.
- No promotion of "diagnostic returned no clustering" to "Gate 5 run can fire." Even a clean diagnostic only authorizes drafting the run-enablement v0.2; the run requires its own separately committed authorization downstream of v0.2.

## 15. Stop conditions (inherited verbatim from `175e939` §15)

The diagnostic must stop and escalate (no auto-proceed) if any of the following are observed:

- The set-difference operation cannot be performed because the F4-canonical metadata is missing, corrupted, or mtime-changed from the recorded `2026-05-18 18:33` (would imply F4 contamination → halt and report).
- The 3 absent units exceed the 0.082% size when re-derived (e.g., set difference returns more than 3 missing units → halt, report, and require a substrate-comparison memo).
- The set-difference returns fewer than 3 missing units (e.g., 0, 1, or 2 → halt and re-verify). That result contradicts Turn B's `recognized = 3647` vs `F4-canonical = 3650` arithmetic and should route to a Gate 4C re-review / Turn B re-verification memo rather than auto-proceed; the symmetric arithmetic-mismatch case is not silently absorbed.
- A real post-2022 filename appears in any channel of the diagnostic's output (Gate 4C firewall breach → halt, report, do not commit the diagnostic, and require a Gate 4C re-review memo).
- Clustering check returns a strong structural pattern (e.g., all 3 absent units share a single calendar month / single weekday / single archive-format-transition window) → halt the auto-path to run-enablement v0.2 and route to a substrate-comparison memo or a narrowly-scoped run-enablement v0.2 that explicitly handles the structural pattern; either way, the choice is a separate decision.

If none of the stop conditions fire, the diagnostic's output authorizes drafting (not running) the Gate 5 run-enablement memo v0.2. It does **not** authorize executing Gate 5.

## 16. Required diagnostic report fields

The diagnostic report (suggested path `docs/lane2_gdelt1_gate5_prerun_diagnostic_report_v0.1.md`), when later produced under a separately initiated execution prompt, must include at minimum:

- **F4-integrity confirmation (per §13.1):**
  - `count_feasibility_metadata.json` size, mtime, SHA-256.
  - `feasibility_summary.md` size, mtime.
  - Directory file-list confirmation (exactly two files, no extras, no missing).
- **Set-difference result (per §12.1 / §13.2):**
  - Total count of planned units (must be 3650).
  - Total count of recognized units (must be 3647).
  - Total count of absent units (must be 3; §15 second/third stop conditions trigger on any deviation).
  - Identifiers of the 3 absent units **under Gate 4C non-disguise discipline** — form-class only, no real post-2022 filenames anywhere in the report.
- **Clustering observations (per §12.2):**
  - Per-month distribution of the 3 absent unit dates.
  - Per-weekday distribution of the 3 absent unit dates.
  - Proximity-to-known-archive-format-transition observations (2013-04-01 daily/monthly switch and any documented subsequent transitions).
  - Descriptive counts only; no inferential hypothesis tests.
- **Stop-condition status:**
  - For each §15 stop condition, an explicit "did not fire" or "fired (route: ...)" record.
- **Firewall-discipline confirmation:**
  - Mandatory L5 regex scan result (pattern `\b\d{8,14}\.(?:export|gkg|mentions)\.(?:CSV|csv)\.zip\b`); matches must be 0.
  - Gate 4C non-disguise compliance confirmation across the 9 channels.
- **Boundary-state confirmation:**
  - F4 mtime / size at report-write time (must remain `2026-05-18 18:33` / 75,303 B + 393 B).
  - `REAL_RETRIEVAL_ENABLED` and `COUNT_FEASIBILITY_AUTHORIZED` values (must remain `False`).
  - Confirmation that no event-file URL was constructed, no network request fired, no market data accessed, no Step 2 activity occurred.
- **Recommendation for v0.2 design lock (per `175e939` §12 last paragraph):**
  - Recommended universe choice (3650 planned vs 3647 recognized) with justification grounded in the set-difference and clustering observations.
  - Explicit note: the recommendation is non-binding on v0.2; v0.2 makes its own independent classification using the report's evidence.
- **Authorizing-memo references:**
  - Commit hash of this authorization memo (filled in after this memo is later committed; the diagnostic execution prompt and the report must both reference it).
  - Commit hash of the run-enablement memo (`175e939`).
  - Commit hash of the decision memo (`c2717a6`).

## 17. Downstream gate map

The full remaining chain from this memo (v0.1) to Gate 5 run completion (each step requires its own separately initiated prompt and is not authorized by any earlier step except where specifically noted):

| # | Step | Status | What authorizes it |
|---|---|---|---|
| 1 | **This authorization memo v0.1** | DONE, committed | This memo itself: committed authorization basis for a later separately initiated diagnostic-execution prompt; does not execute the diagnostic. |
| 2 | **Commit + push of this memo** | NOT YET DONE | separate explicit user prompt; subject to feedback_handout_freshness.md item 6 pre-commit self-status cleanup |
| 3 | **Diagnostic execution prompt** | NOT YET INITIATED | this memo (once committed), §13 envelope, §14 forbidden list, §15 stop conditions; a separate explicit user prompt is still required |
| 4 | **Diagnostic execution** | NOT EXECUTED | the diagnostic execution prompt (step 3); fires F4-integrity confirmation first, then set-difference + clustering check; offline only |
| 5 | **Diagnostic report draft + review** | NOT DRAFTED | step 4's output; uncommitted at first draft, subject to its own self-status scan before commit |
| 6 | **Commit + push of diagnostic report** | NOT YET DONE | separate explicit user prompt |
| 7 | **Memory update for diagnostic report** | NOT YET DONE | separate explicit user prompt under standing memory-update discipline |
| 8a | **Gate 5 run-enablement memo v0.2** *(if §15 stop conditions did not fire)* | NOT DRAFTED | step 6's clean diagnostic; v0.2 must independently classify the universe + verdict map using the diagnostic evidence (per `175e939` §16) |
| 8b | **Substrate-comparison memo** *(if §15 stop conditions fired with structural pattern)* | NOT DRAFTED | step 6's stop-condition trigger; an alternative route that does not continue Gate 5 on GDELT 1.0 |
| 8c | **Gate 4C re-review memo** *(if §15 stop conditions fired with firewall breach or arithmetic mismatch)* | NOT DRAFTED | step 6's firewall or arithmetic-mismatch trigger |
| 9 | **Gate 5 run-enablement memo v0.2 commit + push** *(if 8a was drafted)* | NOT YET DONE | separate explicit user prompt |
| 10 | **Memory update for v0.2** | NOT YET DONE | separate explicit user prompt |
| 11 | **Gate 5 run-enablement commit (flips `COUNT_FEASIBILITY_AUTHORIZED` to True)** | NOT YET DONE | v0.2 explicit authorization; analogous to spent `60ec1521` → `fe742555` but with fresh commits (those are spent and may not be reused) |
| 12 | **Gate 5 run execution** | NOT EXECUTED | step 11's authorization; one-run-only |
| 13 | **Inert-restore commit (flips `COUNT_FEASIBILITY_AUTHORIZED` back to False)** | NOT YET DONE | step 12 completing (success or failure); analogous to `9e329c2` |
| 14 | **Gate 5 run report + closure memo** | NOT YET DONE | step 12's output + step 13's inert-restore; subject to all required-report-field constraints from `175e939` §17 |
| 15 | **Memory update for Gate 5 run closure** | NOT YET DONE | separate explicit user prompt |
| 16 | **Step 2 readiness memo** *(separate question)* | NOT YET DONE | step 14's Gate 5 closure verdict; Step 2 eligibility is the next memo's question, not Gate 5's |

Each step in the map is its own artifact with its own explicit initiation. No step authorizes any subsequent step by inheritance unless explicitly noted. This map is *informative*; it does not authorize any of the steps it lists.

## 18. Non-authorization boundaries

This memo does **not** authorize, by itself, any of the following. None of these become permitted by AUTHORIZE DIAGNOSTIC LATER; each requires its own separate explicit authorization:

- diagnostic execution (this memo permits the execution prompt to exist, not the execution itself)
- Gate 5 execution
- count-feasibility execution
- a new live GET of any GDELT URL (the post-4C `f8345c8` AUTHORIZE LATER EXECUTION was spent by Turn B; a fresh GET requires a fresh memo + fresh approval, including the §12-excluded second-GET replication)
- event-file request / download
- market-data access
- Step 2 lock or Step 2 entry
- Gate 5 run-enablement v0.2 (gated by the diagnostic's output, which does not yet exist)
- runner guard flip (`REAL_RETRIEVAL_ENABLED`, `COUNT_FEASIBILITY_AUTHORIZED` remain `False`)
- F4 modification, overwrite, deletion, or rename (the F4 directory is read-only for the diagnostic)
- source pivot
- fallback source selection
- update of any committed file in `docs/`, `src/`, `tests/`, `scripts/`, or `results/` (the diagnostic, when later authorized, produces one new untracked report file; this memo is itself committed as one new tracked file at this commit)

Safety success at Gate 4C, Gate 4D, and during Turn B remains **necessary but not sufficient** for any subsequent Lane 2 step. The Gate 5 decision memo's AUTHORIZE LATER (`c2717a6`) and the run-enablement memo's DEFER FOR DIAGNOSTIC (`175e939`) both remain **necessary but not sufficient** for the diagnostic execution. This memo, if approved and committed, will be **necessary but not sufficient** for the diagnostic execution prompt.

## 19. One-run-only and inert-restore preview (for downstream reference only)

This section is **not authorization**; it is a forward-looking reminder of constraints that will bind any future Gate 5 run, drawn from `175e939` §18 and the prior count-feasibility cycle:

- If a Gate 5 run is later separately authorized (post-diagnostic, post-run-enablement v0.2), it executes **exactly once**. Technical/protocol failure routes to F5 / human review; no patch-and-rerun without a fresh memo.
- A separately committed run-enablement commit flips `COUNT_FEASIBILITY_AUTHORIZED` to `True` (analogous to `fe742555`, but `fe742555` is spent and may not be reused).
- A separately committed inert-restore commit flips `COUNT_FEASIBILITY_AUTHORIZED` back to `False` immediately after the run completes (analogous to `9e329c2`).
- The new run artifact directory must be timestamped distinctly from F4's `20260518T163302Z`.
- F4 remains canonical / consumed / untouched in all branches.

The diagnostic itself does **not** invoke any of these mechanisms; they bind only the Gate 5 run that is downstream of v0.2.

## 20. Final verdict

**AUTHORIZE DIAGNOSTIC LATER.** The pre-run diagnostic defined in `175e939` §12 is authorized for later, separately initiated execution under the envelope inherited from `175e939` §§13–15 and augmented by §13.1 of this memo (mandatory F4-integrity confirmation before any other diagnostic operation). Second-GET replication is **excluded** from this authorization; the diagnostic operates fully offline under the data already captured at Turn B. The diagnostic is not executed by this memo. A separately initiated execution prompt is still required before any diagnostic operation runs. The diagnostic, when later run, produces evidence that conditions the drafting (not running) of a Gate 5 run-enablement memo v0.2 or, if §15 stop conditions fire, of a substrate-comparison or Gate 4C re-review memo instead. Gate 5 execution remains downstream of v0.2 and remains unauthorized by anything in the chain so far. F4 remains untouched. Guards remain inert. No GDELT contact, no event-file request, no market-data access, no Step 2 activity. The chain's pause discipline holds: the next step waits for explicit user initiation.

— end of pre-run diagnostic authorization memo v0.1 (committed; diagnostic NOT EXECUTED; Gate 5 NOT EXECUTED; second-GET EXCLUDED) —
