Claude Code prompt — Lane 2 type/tone/Goldstein extraction execution authorization v2.1

Working directory:
/Users/jay/Documents/GitHub/coherent-numbers

Mode:
Bounded execution-authorization prompt for type/tone/Goldstein in-sample extraction and outcome-free pre-join diagnostics only.

Design-only status:
This document is a reviewed execution prompt template, not an execution event. Making this document durable does not by itself authorize data contact. Actual extraction requires a later, separate, explicit execution turn that invokes this prompt from its durable commit.

This is the first data-contact step for the type/tone/Goldstein branch. Treat it as irreversible.

Core governing rule:
294494a1badf2d02866def75e985fb2dd0dc99c9 (294494a) is the only authoritative governing spec for formulas, thresholds, in-scope definition, date logic, diagnostics, and gates.

Any formula/threshold wording in this prompt is a subordinate cross-check only. Do not implement from this prompt alone. First extract the relevant governing rules verbatim from 294494a into a conformance report. Then implement from that conformance report.

If this prompt and 294494a disagree in any way, or if 294494a does not define a required formula/threshold/gate clearly enough to implement without inference, HALT before implementation and report BLOCKED. Do not silently choose one source. Do not improvise thresholds.

Hard boundaries:

* No 2023+ read.
* No 2023+ source-file enumeration into manifests.
* No market-data join.
* No next_session_return.
* No abs(next_session_return).
* No market outcome access.
* No outcome computation.
* No result computation against real market returns.
* No EventCode/EventBaseCode/EventRootCode extraction.
* No actor fields.
* No location fields.
* No article text.
* No “just in case” fields.
* No tuning after diagnostics.
* No inline redesign if a gate fails.
* No patch-and-rerun after diagnostic gate failure.
* No push of extraction code, run artifacts, result directories, or anything produced by executing this prompt. This run-time prohibition does not govern the separate design-only commit that makes this prompt document durable, which is committed and pushed in its own turn, not during an execution run.
* No force push under any circumstance.
* No branch/tag creation.
* No .gitignore modification.
* No changes outside files required for this authorized extraction/diagnostic pass.
* No outcome join under any circumstance.
* No fresh GDELT reads during diagnostics.
* No source-header read for V2. GDELT 1.0 files are headerless; V2 must be verified from committed parser/codebook/schema references, not from a source file header.

Current required state and pinned historical anchors:

* Current branch must be main.
* HEAD must equal origin/main at execution time.
* The working tree must be clean except for explicitly acknowledged pre-existing/unrelated untracked files.
* The governing extraction formula/spec commit remains pinned as:
  294494a1badf2d02866def75e985fb2dd0dc99c9 (294494a)
* The extraction authorization gate memo remains pinned as:
  ea891e0675f47bf736b7dab550191d72993ee9c1 (ea891e0)
* Required design-chain ancestors of execution-time HEAD:
  * 219f37c — divergence record;
  * 0295406 — type/tone/Goldstein extraction design memo v0.1;
  * 294494a — lock-closed v0.2 governing formula/spec commit;
  * ea891e0 — extraction authorization gate memo.
* Do not require execution-time HEAD to equal ea891e0. History is allowed to advance after ea891e0, including by this v2.1 design-only prompt commit, as long as the pinned spec/gate commits remain ancestors of HEAD and HEAD == origin/main.
* Future run manifests should pin all three:
  * governing spec commit: 294494a;
  * extraction gate memo commit: ea891e0;
  * execution prompt commit: the durable commit that contains this v2.1 prompt.

Primary objective:
Implement and run exactly one bounded in-sample type/tone/Goldstein extraction and outcome-free diagnostic pass, governed by 294494a, using the proven GDELT count-build discovery path.

Critical discovery-path requirement:
Reuse the proven file-discovery/acquisition path from the successful full daily count build / merged substrate path around merged_20260529, rather than creating a new independent discovery method.

The extraction must read the same 2013–2022 GDELT source-file universe proven by the count-build path, but only for the allowed fields and only as governed by 294494a.

If the proven discovery path cannot be identified or reused, stop before data contact and report BLOCKED.

Discovery-date firewall:
If the proven discovery path covers dates outside 2013–2022, apply the 2013–2022 in-sample filter at discovery/enumeration time before writing manifests or logs. Do not enumerate or manifest 2023+ source paths. Any source file/date > 2022-12-31 must hard-error before reading content rows.

Allowed source fields only:

* date / information-date field as locked by 294494a;
* QuadClass;
* GoldsteinScale;
* AvgTone;
* NumMentions.

Forbidden fields unless future design authorizes them:

* EventCode;
* EventBaseCode;
* EventRootCode;
* any actor fields;
* any location fields;
* any article text;
* any market data/outcome field;
* any price-derived field, including trailing realized volatility.

Forward note only:
The volatility-regime confound is not part of this extraction pass. If a future join-gate spec adds a trailing-realized-volatility control, planted-signal sensitivity must be re-run at that future join gate including that covariate. Do not implement or test that here.

Required output directory:
Create a fresh timestamped run directory under a clearly named path such as:
results/lane2_gdelt1_type_tone_goldstein_extraction/<TIMESTAMP_Z>/

Do not overwrite any existing result directory.

Required implementation artifacts:
Create or update only files necessary for this bounded extraction and diagnostic pass, for example:

* extraction code;
* guarded runner script;
* tests/checks using synthetic fixtures;
* generated extraction artifacts in the fresh run directory.

Do not modify unrelated docs, unrelated result directories, or .gitignore.

Do not preserve raw GDELT payload rows beyond the derived extraction artifacts and audit summaries required here.

Verdict semantics:

Use these meanings exactly:

* SUCCESS — the authorized pass ran to completion without boundary violation. This may still produce future_outcome_join_status = BLOCKED if sample sufficiency, planted-signal, or costume diagnostics fail.
* BLOCKED — a preflight, conformance, V1/V2, discovery-path, schema, guard, or synthetic-test requirement failed before authorized extraction could safely run.
* FAILED — the pass itself errored unexpectedly, or boundary status became uncertain.

A planted-signal FAIL, costume-check FAIL, or sample-sufficiency failure after successful extraction is not FAILED. It is a successful authorized pass whose result is: outcome join remains unauthorized and blocked pending design review / new gate.

Phase 0 — preflight, before any data contact:

No GDELT source-file content may be read in Phase 0. No source header/schema line may be read, because GDELT 1.0 files are headerless.

1. Print:
    * git rev-parse HEAD
    * git rev-parse origin/main
    * git status --branch --short
    * git status --short
    * recent commit log showing execution-time HEAD, the durable v2.1 prompt commit if present, ea891e0, 294494a, 0295406, and 219f37c.
2. Confirm:
    * current branch is main;
    * HEAD == origin/main;
    * no staged files;
    * no modified tracked files;
    * existing untracked files are pre-existing/unrelated;
    * git merge-base --is-ancestor 219f37c HEAD passes;
    * git merge-base --is-ancestor 0295406 HEAD passes;
    * git merge-base --is-ancestor 294494a HEAD passes;
    * git merge-base --is-ancestor ea891e0 HEAD passes;
    * execution-time HEAD is allowed to be later than ea891e0; do not BLOCK merely because HEAD != ea891e0.
3. Verify governing spec chain (ancestor-style):
    * 219f37c divergence record exists and is an ancestor of HEAD;
    * 0295406 v0.1 design exists and is an ancestor of HEAD;
    * 294494a lock-closed v0.2 exists and is an ancestor of HEAD;
    * ea891e0 extraction gate exists and is an ancestor of HEAD.
4. Read the committed gate memo and lock memo only as specifications. Prefer reading them from their pinned commits rather than from mutable working-tree assumptions:
    * governing lock/spec from 294494a;
    * extraction gate memo from ea891e0.
    If exact paths must be resolved, locate them from those commit trees and report the paths used. Do not contact GDELT yet.
5. Verify that the future extraction manifest will declare exactly:
    governing_spec_commit = 294494a1badf2d02866def75e985fb2dd0dc99c9
6. Verify V1:
    Re-check the committed Step 2 table/schema or committed metadata has the volume/coverage-quality control columns:
    * log1p_total_row_count
    * roll_mean_log1p_total_w30
    * coverage_completeness
    V1 must not expose or load market outcome values. If the only available source of these columns is a market-joined table that cannot be safely schema-projected without reading outcome columns, stop and report BLOCKED.
    If V1 fails, stop before extraction.
7. Verify V2 without reading a GDELT source file:
    Confirm GDELT 1.0 field positions and value ranges for:
    * date / information-date field;
    * QuadClass;
    * GoldsteinScale;
    * AvgTone;
    * NumMentions.
    Use only repository code/docs, committed parser code, committed known schema references, or committed codebook references. Do not read a source “header” line. GDELT 1.0 event files are headerless tab-delimited data rows.
    Required V2 confirmations:
    * QuadClass expected value range must be confirmed, including {1,2,3,4} if that is what the committed schema/reference says.
    * GoldsteinScale expected value range must be confirmed, including [-10, 10] if that is what the committed schema/reference says.
    * NumMentions numeric/count expectation must be confirmed.
    * AvgTone numeric expectation must be confirmed.
    * The exact date/information-date field must be identified.
    If field positions or value ranges cannot be confirmed safely without data contact, stop before extraction.
8. Verify the proven count-build discovery path:
    Identify the exact code/path used by the successful full daily count build / merged substrate path around merged_20260529.
    Confirm this extraction will reuse that path rather than re-derive discovery.
    If not identifiable, stop before data contact.
9. Verify 2023+ firewall:
    extraction window must be in-sample only, 2013–2022 as governed by the existing Lane 2 substrate and by 294494a.
    2023+ source paths must not be enumerated into the run manifest. Any source file/date > 2022-12-31 must hard-error before reading content rows.
10. Verify there is a default-false execution guard.
    If it does not exist yet, implement it before extraction.
    Use a guard analogous to STEP2_EXECUTION_AUTHORIZED, named clearly for this extraction, for example:
    TYPE_TONE_GOLDSTEIN_EXTRACTION_AUTHORIZED.
    It must be false by default and restored in finally.

If any Phase 0 preflight fails, stop and report BLOCKED. Do not perform extraction.

Phase 0.5 — governing-spec conformance before implementation:

Before implementing extraction logic, create the governing-spec conformance report. This is one evolving artifact that begins in Phase 0.5 as the pre-implementation conformance artifact and is finalized into the Phase 2 run artifacts. Do not create separate conformance reports that can disagree.

The conformance report must quote or precisely extract from 294494a the governing rules for all of the following:

1. In-scope row/source definition:
    Quote the exact 294494a definition of “in-scope.”
    Do not infer whether “in-scope” means global, US-only, economic-only, all rows, or anything else. If 294494a does not define it clearly, HALT before implementation and report BLOCKED.
2. Date / information-date logic:
    Quote the exact date field to be used.
    State whether it is an information-availability / record/publication / file date rather than an event-occurrence date.
    Affirm no backdating/lookahead is introduced.
    If this cannot be affirmed from 294494a and committed schema/parser evidence, HALT before implementation and report BLOCKED.
3. F1/F2/F3 formulas:
    Quote the governing definitions from 294494a.
4. Missing Goldstein/tone behavior:
    Quote how missing/non-numeric values affect numerator and denominator.
5. Denominator rule:
    Quote the common denominator definition.
6. M1/Kish effective mention count:
    Quote the formula and validity threshold.
7. Zero-denominator / zero-event handling:
    Quote the NaN/exclusion behavior.
8. Z1 standardization:
    Quote the expanding-window, past-only, warmup, and valid-day rules.
9. Composite:
    Quote the equal-weight standardized component rule or whatever 294494a locks.
10. Output schema:
    Quote or extract required output columns/fields from 294494a and ea891e0.
11. Planted-signal full-stack sensitivity:
    Quote the complete locked planted-signal diagnostic specification from 294494a, including all of the following:
    * the exact injection point;
    * the exact ordered transformation sequence the injected synthetic signal must traverse;
    * the locked rho_plant grid;
    * the exact retention metric;
    * the same-sign rule;
    * the 0.05 binding gate;
    * the rescue prohibition for 0.10 and 0.20;
    * any drift/time-control and volume-control requirements.
    Constraints:
    * The expected subordinate cross-check is that injection occurs at the raw-component / pre-standardization level, then passes through the locked predictor-side stack.
    * Do not use or invent a “pre-standardization composite” unless 294494a explicitly defines such an object.
    * Under the expected locked order, compositing occurs after expanding-z standardization.
    * Do not include a per-year synthetic-target check unless 294494a explicitly locks one for the planted-signal diagnostic.
    * Per-year stability belongs to the later outcome-dependent Y1 join gate unless the governing spec says otherwise.
    * If the injection point, ordered transformation sequence, retention metric, or gate thresholds cannot be extracted clearly from 294494a, stop before running diagnostics and report BLOCKED.
12. Costume-check diagnostics:
    Quote the exact linear R² and Spearman/rank bands, CAUTION/FAIL thresholds, and what object is tested.
    The costume check must be on the pre-control extracted composite/components versus volume/coverage controls, not after controlling for volume in a circular way.
13. R1/R2 diagnostics:
    Quote the locked component-collinearity and missing-field/coverage requirements.
14. Verdict/gate meaning:
    Quote or state the governing rule that outcome join remains unauthorized and requires a separate future gate.

Implementation may begin only after this conformance report is produced and shows no unresolved discrepancy.

If any item above cannot be extracted from 294494a or the gate memo, stop and report BLOCKED. Do not fill gaps with assumptions.

Phase 1 — implementation, still before extraction:

Implement the minimal extraction code required by the Phase 0.5 conformance report.

The following expected formula shape is a subordinate cross-check only. It is not authoritative over 294494a.

Subordinate cross-check expectations:

1. Common denominator:
    total daily in-scope NumMentions.
2. F1 material-conflict pressure:
    Σ NumMentions[QuadClass = 4] / total daily in-scope NumMentions
3. F2 negative structural-impact pressure:
    Σ NumMentions * max(0, -GoldsteinScale) / total daily in-scope NumMentions
4. F3 negative-tone pressure:
    Σ NumMentions * max(0, -AvgTone) / total daily in-scope NumMentions
5. Missing/non-numeric Goldstein or tone:
    contributes 0 to that component numerator and does not shrink the denominator.
6. M1:
    N_eff_mentions = (Σ NumMentions)^2 / Σ(NumMentions^2)
    primary valid day requires N_eff_mentions >= 100.
7. All-cooperative / no-negative-pressure day with valid denominator:
    component = 0, not NaN.
8. Denominator-zero or zero-event day:
    NaN / excluded from primary composite.
9. Z1:
    expanding-window past-only z-score per component, using 365 prior valid in-scope days.
10. Composite:
    equal-weight standardized F1/F2/F3 into intensity_valence_pressure.

If any subordinate cross-check conflicts with the Phase 0.5 conformance report, HALT and report BLOCKED. Do not choose one.

Implement output schema with clear columns for:

* civil_date / information date;
* raw component values F1/F2/F3;
* validity flags;
* denominator totals;
* N_eff_mentions;
* warmup eligibility;
* standardized components;
* intensity_valence_pressure;
* missing-field mention fractions for Goldstein and AvgTone;
* any coverage/substrate flags reused.

Do not include market outcomes.

Phase 1 tests/checks:
Before running full extraction, run targeted tests/checks using synthetic fixtures only. Do not use real GDELT rows for these tests.

Required checks:

* common denominator is not shrunk for missing Goldstein/tone;
* missing Goldstein/tone contributes 0 numerator;
* all-cooperative valid day gives 0 component;
* zero denominator gives NaN/exclude;
* Kish effective N behaves correctly under equal weights and concentrated weights;
* expanding z-score uses prior days only;
* no 2023+ rows allowed;
* forbidden fields are not extracted;
* date/firewall logic rejects >2022-12-31 before content-row reading;
* output schema scanner shows no market outcome columns;
* forbidden field scanner shows no EventCode/EventBaseCode/EventRootCode, actor, location, article text, or market fields.

If tests/checks fail, stop before extraction.

Phase 2 — authorized extraction run:

Only after Phase 0, Phase 0.5, and Phase 1 pass:

1. Explicitly enable the extraction guard for exactly one run.
2. Run the in-sample extraction once using the proven discovery path.
3. Use the discovery-time 2013–2022 filter before manifesting source paths.
4. Restore the guard in finally.
5. Prove guard restored to false after run.
6. Write artifacts only to the fresh timestamped run directory.

Required extraction artifacts:

* extracted feature table;
* extraction manifest pinning governing spec commit 294494a;
* metadata JSON;
* boundary declaration;
* source schema verification report from committed parser/codebook references, not source headers;
* finalized governing-spec conformance report against 294494a, continuing the same Phase 0.5 conformance artifact rather than creating a second independent report;
* SHA-256 hashes for generated artifacts;
* row/date coverage summary;
* no-2023+ proof;
* guard restoration proof;
* git status proof;
* forbidden-field absence proof.

Phase 3 — outcome-free diagnostics only:

Run only outcome-free diagnostics. Do not join market data.

Phase 3 precondition:
Diagnostics must operate solely on the Phase 2 on-disk extracted artifacts and any explicitly outcome-free committed control artifacts needed for volume/coverage controls.

The extraction guard must remain false during diagnostics.

No fresh GDELT enumeration, discovery, or read is allowed in Phase 3.

No market-data files may be read.

No market-joined table may be read unless safe column projection can prove only outcome-free volume/coverage columns are loaded. If that cannot be guaranteed, report the costume diagnostic as blocked and state that outcome join remains blocked pending design review/new gate.

Required diagnostic order:

1. Sample sufficiency first:
    Report before interpreting anything else:
    * total extracted days;
    * valid composite days after N_eff_mentions >= 100;
    * valid composite days after 365-day warmup;
    * valid composite years before outcome join;
    * number of years with at least 100 valid composite days.
    State that this is a pre-join lower bound, not final Y1 paired-observation sufficiency.
    If sample sufficiency fails:
    * stop before interpreting later diagnostics;
    * report Verdict: SUCCESS;
    * report future_outcome_join_status: BLOCKED — sample sufficiency failure;
    * do not tune, patch, or rerun.
    If 294494a appears to contradict the sufficiency-first-stop rule from the extraction gate memo, treat that as a spec/gate discrepancy and report BLOCKED. Do not proceed by choosing one.
2. Planted-signal full-stack sensitivity:
    Use synthetic target only.
    Never use:
    * next_session_return;
    * abs(next_session_return);
    * any market outcome;
    * 2023+;
    * market data;
    * price-derived volatility.
    This diagnostic must follow the complete planted-signal specification quoted in the Phase 0.5 conformance report.
    Subordinate cross-check only (not authoritative over 294494a):
    The expected locked shape is injection at the raw-component / pre-standardization level, followed by the full ordered predictor-side transformation stack from 294494a, including expanding-z standardization, composite construction, drift/time control, and incremental-over-volume control if those are confirmed by the governing spec.
    Prohibitions:
    * Do not inject into a “pre-standardization composite” unless 294494a explicitly defines that object.
    * Do not run or report a synthetic-target per-year check unless 294494a explicitly makes it part of the planted-signal diagnostic.
    Use the locked grid quoted from 294494a, expected subordinate cross-check:
    rho_plant = {0.05, 0.10, 0.20}
    Binding gate:
    rho_plant = 0.05 must retain same sign and at least the locked retention threshold quoted from 294494a.
    If 294494a defines retention as ≥50%, use that. If not defined clearly, report BLOCKED before running this diagnostic.
    Failure at 0.05 blocks outcome join and requires design-review/new gate.
    0.10 and 0.20 cannot rescue failure at 0.05.
    If planted-signal gate fails:
    * report Verdict: SUCCESS;
    * report future_outcome_join_status: BLOCKED — planted-signal gate failure;
    * do not tune, patch, or rerun.
3. Empirical volume/coverage-quality costume check:
    Outcome-free.
    No market outcomes.
    No 2023+.
    No fresh GDELT reads.
    No market-data files.
    Use extracted in-sample composite/components and locked controls:
    * log1p_total_row_count
    * roll_mean_log1p_total_w30
    * coverage_completeness
    If the volume/coverage controls are read from a table that spans beyond 2013–2022, perform an inner join restricted to the extracted composite’s in-sample dates only. No 2023+ control row may enter diagnostics through the join key, schema projection, or artifact metadata.
    If the controls cannot be safely projected and date-restricted without exposing market outcome columns or 2023+ rows, report the costume diagnostic as blocked and state that outcome join remains blocked pending design review/new gate.
    Confirm the diagnostic object is the pre-control extracted composite/components versus volume/coverage controls, not a post-control residual/composite in a circular check.
    Report the bands locked in 294494a for:
    * linear R²;
    * Spearman/rank relationship.
    If exact CAUTION/FAIL bands cannot be extracted from 294494a, report BLOCKED and do not improvise.
    FAIL blocks outcome join and requires design-review/new gate.
    CAUTION must be labeled.
    If costume diagnostic fails:
    * report Verdict: SUCCESS;
    * report future_outcome_join_status: BLOCKED — costume diagnostic failure;
    * do not tune, patch, or rerun.
4. R1 component collinearity:
    Outcome-free.
    Report Pearson and Spearman if feasible, minimum Spearman.
    If high collinearity, interpret composite as a single negativity-share index, not three independent signals.
    Cannot rescue or overturn primary test.
5. R2 missing-field / coverage-quality diagnostics:
    Outcome-free.
    No fresh GDELT reads.
    Report Goldstein and AvgTone missing-field mention fractions.
    Report excluded / invalid / below-floor day counts.
    Report coverage-quality diagnostics.

Phase 4 — post-run verification:

1. Print final git status --short.
2. Confirm no market outcome fields exist in generated artifacts.
3. Confirm no 2023+ rows read or written.
4. Confirm no 2023+ source paths were enumerated into the run manifest.
5. Confirm no outcome join occurred.
6. Confirm no market-data files were read.
7. Confirm no EventCode/EventBaseCode/EventRootCode extracted.
8. Confirm no actor/location/article-text fields extracted.
9. Confirm guard restored to false before diagnostics and remained false during diagnostics.
10. Confirm diagnostics used only Phase 2 artifacts and explicitly outcome-free controls.
11. Confirm artifacts include manifest, metadata, SHA-256s, boundary declaration, no-2023+ proof, conformance report, schema verification report, guard restoration proof, forbidden-field proof, and diagnostics.
12. State clearly whether outcome join remains unauthorized.
13. State clearly whether future outcome join is:
    * unauthorized but not blocked by these diagnostics;
    * unauthorized and blocked by sample sufficiency;
    * unauthorized and blocked by planted-signal gate;
    * unauthorized and blocked by costume diagnostic;
    * unauthorized and blocked because diagnostic prerequisites were unavailable.

Commit policy:

For this prompt:

* You may create implementation files and result artifacts needed for the authorized extraction.
* Do not commit.
* Do not push.
* Leave created/modified files unstaged.
* Report the exact files created/modified.

Report format:

* Verdict: SUCCESS, BLOCKED, or FAILED.
* If SUCCESS, future_outcome_join_status:
    * UNAUTHORIZED — future gate still required;
    * BLOCKED — sample sufficiency;
    * BLOCKED — planted-signal gate;
    * BLOCKED — costume diagnostic;
    * BLOCKED — missing/unsafe diagnostic prerequisite.
* Governing spec commit pinned.
* Phase 0.5 conformance status.
* Any prompt-vs-294494a discrepancy: yes/no.
* In-scope definition quoted from 294494a.
* Date/information-date field quoted from 294494a.
* Date availability/no-lookahead assertion.
* V1 status.
* V2 status, with source of schema confirmation.
* Proven discovery path reused: yes/no, with exact path/code reference.
* Discovery-time 2013–2022 filter proof.
* Guard name and restoration proof.
* Run directory.
* Artifact list.
* Sample sufficiency summary first.
* Planted-signal gate result.
* Costume diagnostic result.
* R1/R2 summary.
* No-2023+ proof.
* Confirmation:
    * no outcome join;
    * no market outcomes;
    * no 2023+;
    * no 2023+ manifest paths;
    * no EventCode/EventBaseCode/EventRootCode;
    * no actor/location/article-text fields;
    * no market-data files read;
    * no fresh GDELT reads during diagnostics.
* Files created/modified.
* Final git status --short.

One detail to notice:
This prompt still does not authorize any market outcome join. It authorizes only in-sample type/tone/Goldstein extraction plus outcome-free gates needed to decide whether a future join gate is even worth opening.
