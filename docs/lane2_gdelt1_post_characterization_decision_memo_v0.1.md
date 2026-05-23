# Lane 2 GDELT1 post-characterization decision memo v0.1

## 1. Title and status

This memo is **memo-only**. It authorizes no new GDELT contact, no re-run, no characterization run, no full daily-count build, no market data, no Step 2, no spike/burst threshold tuning, no guard flip, no source/test/config edit, no locked-memo edit, no output-artifact mutation, and no staging / commit / push of this memo or any other artifact unless separately authorized after review.

The memo's authorization scope is the persistence of one tracked file at `docs/lane2_gdelt1_post_characterization_decision_memo_v0.1.md`. Its purpose is to translate the row-date characterization execution outcome (`TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY`) into three locked decisions that bridge between substrate characterization and a future full daily-count build design memo, without entering the full-build design itself.

| Anchor | Value |
|---|---|
| Current `HEAD = origin/main` | `858b501b3b259cd30fc7d4079f58c321a05cc8ef` |
| Ahead count | `0` |
| Tracked tree status | clean |
| Characterization outcome | `TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY` |
| First-probe execution report | `9319d30` |
| Substrate-validation memo (`REKEY-BY-SQLDATE-CANDIDATE`) | `a8a9dd2` |
| Characterization plan lock | `a2a8fd5` |
| Runner implementation | `e9f8781` |
| Exact-integer corrective | `487dadb` |
| Characterization enable | `3537a62` |
| Characterization restore | `73a7911` |
| Characterization execution report | `858b501` |
| First-probe output dir (untracked) | `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` |
| Characterization output dir (untracked) | `results/lane2_gdelt1_row_date_characterization/20260523T033234Z/` |

## 2. Scope and non-scope

**In scope:**

- Decision 1: T+1 row handling for the future full daily-count build.
- Decision 2: whether to authorize a finer-grained T+1 boundary characterization.
- Decision 3: artifact disposition for both output dirs.
- Explicit closure of `a8a9dd2`'s `REKEY-BY-SQLDATE-CANDIDATE` premise.
- Boundary-constraint statement for the next workstream.

**Out of scope (explicit, binding):**

- No full daily-count build design (a separate design memo follows this one).
- No full daily-count build execution.
- No market data of any kind.
- No Step 2 of any kind.
- No spike / burst threshold tuning.
- No return-window logic.
- No signal-design choice.
- No category / theme / actor / geography / tone filtering.
- No claim about market predictiveness.
- No claim about GDELT-side cause for the T+1 boundary disappearance.
- No GDELT contact.
- No output-artifact mutation.
- No guard flip.
- No source / test / config edit.
- No locked-memo edit.
- No 2023+ pre-filter authorization.
- No frozen-snapshot execution.
- No `python3` canonicalization change.
- No negative-control payload allow-list change.

## 3. Source anchors

In commit-chain order:

| # | Anchor | Description |
|---|---|---|
| 1 | `9319d30` | First event-file probe execution report; empirical origin of the `ROW-DATE-MISMATCH` finding |
| 2 | `a8a9dd2` | Substrate-validation memo; primary decision `REKEY-BY-SQLDATE-CANDIDATE` (conditional) |
| 3 | `a2a8fd5` | Characterization plan lock |
| 4 | `e9f8781` | Row-date characterization runner implementation |
| 5 | `487dadb` | Exact-integer offset taxonomy corrective patch (removed leap-year tolerance window) |
| 6 | `3537a62` | Characterization guard enable (one-line `ROW_DATE_CHARACTERIZATION_AUTHORIZED = False → True`) |
| 7 | live run | Single invocation over 16 locked URLs at output-dir timestamp `20260523T033234Z` |
| 8 | `73a7911` | Characterization guard restore (one-line back to False; runner byte-identical to `487dadb`) |
| 9 | `858b501` | Row-date characterization execution report (this memo's source of truth) |

This memo treats the committed execution report at `858b501` as the source of truth where memory and repo disagree.

## 4. Characterization result summary

From `858b501`:

- **Outcome**: `TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY` (per `a2a8fd5` §10 outcome B).
- All 16 locked URLs returned HTTP `200` / `200_OK`. Zero redirects, zero connection errors, zero non-200 responses, zero parser anomalies, zero malformed-short rows, zero unparseable SQLDATE rows, zero 2023+ rows, zero unexpected offsets.
- `all_files_conform_to_expected_taxonomy = True`; `any_unexpected_offset_observed = False`; `files_with_unexpected_offsets = []`.
- Exact taxonomy validated across all 16 files: `{0, −1, −7, −30, −365, −3650, +1}` — every observed offset is exactly one of the seven integers; nothing outside.
- `−3650` lands on the exact integer offset in every one of the 16 files — **no leap-year drift**. GDELT 1.0's lookback offsets are constant-day-count, not calendar-date arithmetic. The `487dadb` exact-integer corrective patch is empirically validated.
- `+1` is present in 4 of 16 files (`2013-09-07`, `2014-02-16`, `2014-07-26`, `2014-12-31`) and absent in the other 12 (`2015-10-02` through `2022-12-30`).
- **Latest sampled date with T+1**: `2014-12-31`.
- **Earliest sampled date without T+1**: `2015-10-02`.
- **T+1 disappearance window (sampling-bounded)**: half-open interval `(2014-12-31, 2015-10-02]`, approximately 9 months wide. Monotonic transition: no file after `2015-10-02` has T+1; no file before `2015-01-01` lacks it (within this sample).
- Total event rows across all 16 files: **1,892,438**.
- Offset row totals: `−3650: 315 / −365: 15,012 / −30: 9,745 / −7: 16,230 / −1: 10,162 / 0: 1,840,353 / +1: 621`.
- Mismatch-rate distribution: min `1.93 %` (`2017-12-31`), max `3.76 %` (`2014-02-16`), mean `2.69 %`, median `2.66 %`.
- Lookback-bucket row counts are roughly stable in absolute terms across files (T−365 totals 15,012 ≈ 939/file mean) while nominal-day row counts vary ~4.5× (48,853 to 221,966). The mismatch-rate decline first observed in `a8a9dd2` §5 is confirmed as a denominator effect, not a substrate-property trend.

## 5. Closure of `a8a9dd2` `REKEY-BY-SQLDATE-CANDIDATE`

**Verdict: UPGRADE TO LOCKED PREMISE.**

The substrate-validation memo `a8a9dd2` §6 selected `REKEY-BY-SQLDATE-CANDIDATE` as the primary decision, **conditional on a bounded characterization plan**, because (paraphrasing `a8a9dd2` §6, third paragraph): the offset taxonomy was consistent across 5 files but not proven exhaustive, and a bounded characterization plan was needed before locking the re-key rule.

The characterization at `858b501` discharges that conditionality:

1. The offset taxonomy `{0, −1, −7, −30, −365, −3650, +1}` is exhaustive across the 16-date characterization sample spanning `2013-09-07` to `2022-12-30` (covering the daily-regime in-window date range and all interior years).
2. `any_unexpected_offset_observed = False` across 16 files; no new offset buckets surfaced beyond what the 5-file initial probe identified.
3. The `−3650` bucket is exact-integer with no leap-year drift; the taxonomy is constant-day-count.
4. No pipeline-behavior boundaries other than the `T+1` disappearance were observed.
5. Five (initial probe) + sixteen (characterization) = **21 distinct daily files** inspected, all consistent with the locked taxonomy modulo the T+1 disappearance boundary.

**Locked premise** for the future full daily-count build:

> Each event row in a GDELT 1.0 daily publishing file contributes attention to its `SQLDATE` (the actual event date), not to the file's nominal publishing-window date. The full daily-count build aggregates rows across publishing files by `SQLDATE`. The offset taxonomy of lookback buckets relative to each publishing file's nominal date is the seven-element exact-integer set `{0, −1, −7, −30, −365, −3650, +1}`, with the `+1` bucket present only in files whose nominal date is on or before `2014-12-31` (sampling-bounded; see §7 for the exact-boundary question).

This premise replaces the strict §6 nominal-date contract from the original probe design note (`e55e09a`) and supersedes any earlier narrative shorthand that treated the row-date mismatch as a noise floor.

**What is NOT locked by this verdict** (and thus remains for other memos / decisions):

- The exact `T+1` disappearance date (only bracketed to `(2014-12-31, 2015-10-02]`; see Decision 2).
- The GDELT-side cause of the T+1 disappearance.
- The full-build aggregation arithmetic, edge handling, runner design, and output schema (deferred to a future full-build design memo).
- Any market-data, Step-2, spike-threshold, return-window, or signal-design choice.
- Any decision about how T+1 rows are handled in the build (that is **Decision 1**, immediately below).
- Artifact disposition for the existing output dirs (that is **Decision 3**, in §8).

## 6. Decision 1: T+1 row handling

**Decision: Option B — keep T+1 rows and re-key them to their `SQLDATE` like all other lookback-bucket rows.**

### 6.1 Options evaluated

**A. Drop T+1 rows from the future full daily-count build.**

- Pro: eliminates the pre-2015 / post-2015 publishing-pipeline asymmetry from the input row set; uniform "publishing-window-only" interpretation.
- Con: discards 621 real event-keyed rows (≈0.03 % of total) whose `SQLDATE` already places them at their actual event date; treats T+1 as a defect rather than a substrate property; introduces a special case that distinguishes T+1 from the other six lookback buckets without a substrate-side justification (the six other buckets all reference dates *prior to* the publishing date, but the publishing-pipeline machinery that emitted T+1 is the same machinery that emitted T=0).
- Reject as primary.

**B. Keep T+1 rows and re-key them to `SQLDATE` like all other rows. (SELECTED)**

- Pro: uniform treatment of all seven lookback buckets — every row's contribution flows to its actual event date regardless of which publishing file it came from; closes `a8a9dd2`'s `REKEY-BY-SQLDATE-CANDIDATE` premise uniformly across the locked offset taxonomy; preserves all 621 T+1 event-keyed rows; no special case in the build's re-keying logic; the pre / post-2015 publishing-pipeline asymmetry is documented but does not require a code-level branch (any analysis that wants to identify T+1-origin rows can derive them from `SQLDATE = publishing_file_date + 1`).
- Con: pre-2015 target dates can in principle receive contributions from one more publishing file (the next-day file's T+1 bucket) than post-2015 target dates; this is a substrate-level asymmetry the build cannot remove without dropping data.
- **Select.**

**C. Flag T+1 rows separately while still retaining them in the SQLDATE-keyed build.**

- Pro: preserves downstream-analysis flexibility (a future analysis can include or exclude T+1 by reading the flag).
- Con: the T+1-origin property is **already derivable** from `(SQLDATE − publishing_file_date) == +1`; an explicit flag column would duplicate information and bloat the build's row / column schema; the locked offset taxonomy already provides exhaustive coverage so any analysis that wants to filter by lookback bucket can do so on the derived offset itself.
- Reject as redundant relative to B (information is preserved either way; B carries less schema cost).

**D. Other explicitly justified rule.**

No substrate-side evidence supports a fourth rule. The 16-file characterization shows T+1 is part of the same lookback-ladder substrate (HTTP retrieval identical, parser identical, header anomaly flag identical, SQLDATE column identical), not a boundary-era artifact distinct in kind. A "drop T+1 only from post-2015 files" rule is incoherent since post-2015 files have no T+1 rows to drop. A "drop T+1 only from pre-2015 files" rule would re-introduce the publishing-pipeline asymmetry without substrate-side justification. Reject.

### 6.2 How Decision 1 closes / upgrades / revises / conditions `a8a9dd2`'s `REKEY-BY-SQLDATE-CANDIDATE`

Decision 1B **closes** the conditionality (per §5, upgraded to locked premise) and **operationalizes** the premise uniformly across all seven buckets of the locked offset taxonomy. The premise's "re-key by `SQLDATE`" rule is now exhaustive: every row, including T+1 rows, lands on its `SQLDATE` in the daily-count build. No bucket is exempted; no bucket is treated as a special case; no bucket is dropped.

### 6.3 Consistency with the no-market-data firewall

Decision 1B uses only:

- The offset taxonomy validated by `858b501` (locked).
- The semantic meaning of the `SQLDATE` column (column index 1 of GDELT 1.0 daily event files; documented in `e55e09a`).
- The 16-file sample's row-keyed evidence.

No market data, asset return, threshold, signal-design choice, or category / theme / actor filter enters the decision. The no-market-data firewall is not approached, not touched, not relaxed.

### 6.4 Comparability across pre-2015 and post-2015 files

Comparability is preserved **at the event-keyed level**: every event row lands on its actual `SQLDATE` regardless of which publishing file emitted it. Comparability is **not** preserved at the publishing-file level: pre-2015 publishing files contribute to a 7-bucket cone (the six lookback offsets plus T+1), post-2015 publishing files to a 6-bucket cone (the six lookback offsets only). This is a substrate property the build cannot eliminate without dropping data; Decision 1B documents the asymmetry and preserves all evidence rather than discarding rows in order to manufacture symmetry the substrate does not exhibit. This asymmetry is accepted as a documented substrate-level property of GDELT 1.0 under Decision 1B — not corrected in code, not normalized away by any build-side adjustment, and not used as a basis for introducing market-data, Step 2, spike / burst threshold, or any other downstream adjustment logic.

### 6.5 T+1 status — substrate property or boundary-era artifact?

**T+1 rows are part of the lookback-ladder substrate, not a boundary-era artifact.** Justifications:

- T+1 rows pass through the same HTTP retrieval (HTTP `200` / `200_OK`), the same parser (`header_anomaly_detected = False`), the same SQLDATE column, and the same row-shape as T=0 / T−1 / T−7 / T−30 / T−365 / T−3650 rows. No probe-side, parser-side, or transport-side anomaly distinguishes them.
- Their `SQLDATE` values are valid, parseable, integer-day-offset `+1` from the publishing date — identical in form to other lookback offsets.
- The T+1 bucket disappears after `2015-10-02` due to a publishing-pipeline change at GDELT (specific cause out of scope per §2); the pre-2015 substrate emitted T+1 rows because GDELT's publishing pipeline tagged some publication-window event rows with the next calendar day's date; the post-2015 substrate does not. The disappearance is a change of pipeline behavior, not a change of row-quality.
- "Boundary-era artifact" would imply the rows are noise, parsing artifacts, or substrate defects. None of these characterizations apply: the rows are valid event-keyed records.

### 6.6 How the future full-build design memo must implement Decision 1B (NOT executed here)

For each daily target date `d` in the build's recognized universe:

```
count[d] = number of rows R drawn from any publishing file f
           such that R.SQLDATE == d
           and f's nominal date is in {d, d+1, d+7, d+30, d+365, d+3650, d-1}
```

Equivalently, the build iterates over all publishing files in the recognized universe and routes each row to the daily bucket identified by its `SQLDATE`, with no per-row branching on T+1 origin. The seven-bucket `{0, −1, −7, −30, −365, −3650, +1}` taxonomy from §5 enumerates the lookback offsets the build pipeline must support.

For pre-2015 target dates, the `f` at nominal date `d-1` contributes its T+1 bucket (non-empty before the boundary); for post-2015 target dates, the same `f` at nominal date `d-1` contributes zero T+1 rows (because no T+1 rows are emitted in post-boundary files). The build code does **not** condition on the boundary; the `SQLDATE`-equality filter handles the asymmetry uniformly.

Edge handling at the boundaries of the recognized universe (e.g., a target date `d` near `2013-04-01` may have no `f` at nominal `d+3650` if no 2023+ file is allowed under the no-2023+ posture at `0ddbd51`; a target date `d` near `2022-12-31` may have no `f` at nominal `d+1` for the same reason; the T−3650 row in the `2013-04-01` file with SQLDATE `2003-04-04` lies outside the daily-regime window) is a design choice for the full-build design memo, **not** for this memo.

### 6.7 What must NOT be inferred from Decision 1

- **No market-data permission.** Decision 1 is purely substrate-treatment; it grants no permission to introduce asset returns, prices, volumes, volatility, indices, ETF data, or any other market measure into Lane 2.
- **No Step-2 permission.** No precursor work on attention-to-return mappings, signal extraction, or any downstream analytical step is authorized.
- **No spike / burst threshold permission.** No threshold on the daily count series, no spike detection, no burst characterization is authorized.
- **No return-window logic.** No event-windowing relative to market returns, no T-stat construction, no IR computation.
- **No full daily-count build execution.** This memo is design-level only; no script is run, no daily-count series is produced.
- **No claim about market predictiveness.** Decision 1 says nothing about whether the resulting daily attention series predicts, correlates with, or relates in any way to any market measure.

## 7. Decision 2: finer T+1 boundary characterization

**Decision: Option A — no finer characterization is authorized by this memo; the 9-month bracket `(2014-12-31, 2015-10-02]` is accepted as sufficient for the full-build design.**

### 7.1 Options evaluated

**A. No finer characterization; accept the 9-month bracket as sufficient. (SELECTED)**

- Pro: under Decision 1B's uniform SQLDATE re-keying the build is independent of the exact T+1 transition date; preserves the no-additional-GDELT-contact discipline; minimizes the surface area of the full-build design memo; produces a clean closure here rather than an open dependency.
- Con: the documentary record retains a 9-month uncertainty about the exact transition date.
- **Select.**

**B. Authorize (later) a bounded successor characterization over `2015-01-01` through `2015-09-30`.**

- Would narrow the bracket via deterministic sampling (e.g., bisection at 2015-04, 2015-05, 2015-07, then convergence).
- Pro: tighter documentary record; potentially identifies the exact GDELT publishing-pipeline change date.
- Con: requires a separate bounded characterization-plan lock memo analogous to `a2a8fd5`, plus a separate execution-authorization prompt analogous to the chain `3537a62 → 73a7911 → 858b501`; requires additional GDELT contact; the result is documentary rather than build-critical.
- Reject as premature (does not preclude a future explicit prompt; see §7.5).

**C. Defer the decision until the full-build design memo.**

- Pro: keeps the option live in case the full-build design surfaces a specific reason to need the exact transition date.
- Con: creates an unresolved dependency between this memo and the full-build design memo; under Decision 1B the build is independent of the exact transition date, so deferral creates an awkward conditional that does not affect the design.
- Reject in favor of A (cleaner closure).

**D. Forbid further boundary characterization.**

- Too strong. A future analytical need may legitimately motivate finer precision. Selecting D would foreclose a future bounded prompt for no substrate-side reason.
- Reject.

### 7.2 Is the 9-month bracket sufficient for a daily-count build design?

**Yes.** Under Decision 1B, the build re-keys all rows by `SQLDATE` uniformly. The build code does not branch on "is this publishing file pre-boundary or post-boundary"; it iterates over all publishing files in the recognized universe and routes each row by `SQLDATE`. The exact transition date is irrelevant to the build's correctness.

Under Decision 1A (which was not chosen), the answer would also be yes: a uniform "drop rows whose SQLDATE > publishing_file_date" rule applies regardless of the publishing file's relative position to the boundary, since post-2015 files have no T+1 rows to drop in the first place.

The 9-month bracket is therefore sufficient for the full-build design.

### 7.3 Would finer characterization change the build rule or merely improve documentation?

**Merely improve documentation.** No substantive build-rule change is contingent on the exact transition date. Documentary precision is a real value but not a build-critical value at this stage.

### 7.4 Is additional GDELT contact scientifically worth the cost?

**No — not for this purpose.** The cost includes:

- A bounded characterization-plan lock memo (analogous to `a2a8fd5`).
- A characterization-execution-authorization prompt (analogous to the prompt leading to `3537a62 → 73a7911 → 858b501`).
- An enable-then-inert-restore commit cycle on a runner (the existing runner's hardcoded `CHARACTERIZATION_DATES` constant would need to be replaced for a new locked date list, or a successor runner introduced).
- Additional GDELT GETs (≈4–10 additional URLs depending on the bisection strategy).
- A new post-run report and a new untracked output dir.

The benefit (documentary precision on a transition date that does not affect build correctness) does not justify the cost at this stage. A future analysis that surfaces a specific need can revisit.

### 7.5 How Decision 1 affects Decision 2

Decision 1B (keep + re-key uniformly) makes Decision 2 **documentary rather than build-critical**, as stated above. If Decision 1A (drop T+1) had been chosen, Decision 2 would still be documentary because the drop rule applies uniformly regardless of publishing-file position. If Decision 1C (flag T+1) had been chosen, the flag itself is a per-row property derivable from `SQLDATE − publishing_file_date == +1` without needing the exact transition date.

In all three cases (A, B, C for Decision 1), finer boundary precision is documentary, not build-critical. The choice across A / B / C for Decision 1 does not change Decision 2's verdict.

### 7.6 Future workstream framing (if revisited)

If a future explicit prompt requests finer-grained T+1 boundary characterization for the 2015-01 through 2015-09 region, it must be structured as a **separate future workstream**, not as execution authorized by this memo:

1. A successor bounded characterization-plan lock memo (analogous to `a2a8fd5`) pre-registering exact deterministic dates, metrics, output report path, and stop conditions.
2. A successor characterization-execution-authorization prompt (analogous to the prompt leading to `3537a62 → 73a7911 → 858b501`) authorizing a guard-flip-and-restore cycle on the existing characterization runner (or a successor runner if the existing one's hardcoded `CHARACTERIZATION_DATES` constant cannot be re-used).
3. A successor execution report (analogous to `858b501`).
4. A successor consolidated memory update.

This memo does **not** authorize any of the above. It also does not preclude them: a future explicit user prompt remains the gating authority.

## 8. Decision 3: artifact disposition

**Decision: Option A — keep both output dirs untracked indefinitely, with SHA-256 references in committed reports. This decision is temporary; a future explicit prompt may revisit either or both dirs.**

### 8.1 Output dirs in scope

- `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` — 7 files; first-probe at `9319d30`; ≈ 27 MiB total payload; SHA-256 per file recorded in `a8a9dd2` §10 and in the original probe report.
- `results/lane2_gdelt1_row_date_characterization/20260523T033234Z/` — 18 files; characterization at `858b501`; ≈ 119.4 MiB total payload; SHA-256 per file recorded in `858b501` §8.

### 8.2 Options evaluated

**A. Keep both output dirs untracked indefinitely, with SHA references in reports. (SELECTED)**

- Probe precedent: clean line of authority from `9319d30` (first probe), `a8a9dd2` §10–§11 (substrate-validation reaffirmed untracked), and `858b501` §16 (characterization explicitly extended the precedent).
- Repo size: avoids inflating the tracked tree by ≈146 MiB (≈4–5× the current paper / source / docs size, depending on revision).
- Auditability: committed reports preserve all analytical findings (per-file metrics, aggregate metrics, taxonomy conformance, T+1 boundary, mismatch rates) and SHA-256 for every output file in committed form.
- Re-validation: a future re-validation can re-run the runner against the same locked URL list (subject to GDELT-side payload mutability, documented at `858b501` §13) and verify SHAs; or request the local artifact bytes from the original author; or rely on the committed reports' SHA tables and analytical tables alone.
- **Select.**

**B. Commit selected lightweight metadata only.**

- Lightweight candidates: `characterization_metadata.json` (52,289 B; SHA `52fc25bd…dc2ed6f`) and `characterization_summary.md` (1,894 B; SHA `dafb3e1d…57910ca`) from the characterization dir; `probe_metadata.json` (4,422 B; SHA `4ee1f2b5…063d57c08`) and `probe_summary.md` (825 B; SHA `72b1a344…733500ef91`) from the probe dir.
- Total tracked addition: ≈ 60 KiB.
- Pro: preserves machine-readable per-row metrics in the repo for any future replay tooling; finer-grained than the report's prose tables.
- Con: diverges from the probe precedent; introduces a new repo discipline ("summary metadata is committed, raw payload is not") that adds surface area; the metadata is already summarized in the committed reports' tables (§10 and §11 of `858b501`; corresponding tables of the original probe report); a re-run of the runner regenerates the metadata deterministically given the same network state.
- Reject in favor of A unless a downstream analysis specifically requires the machine-readable form (no such need is identified by this memo).

**C. Commit all payload artifacts as audit evidence.**

- Total tracked addition: ≈ 146 MiB across 25 files.
- Pro: bytes-on-disk audit evidence independent of GDELT-side mutability.
- Con: severely inflates repo and clone size; violates the probe precedent; the SHA records in committed reports already serve the bytes-witness function as long as the SHAs are honored.
- Reject.

**D. Add / update gitignore discipline.**

- Status quo: `results/` is not committed by convention; no `.gitignore` rule explicitly excludes it.
- Pro: makes the convention explicit; protects against accidental staging.
- Con: a source / test / config edit (per §2 non-scope) that this memo does not authorize.
- Reject as out of scope for this memo (could be revisited in a separate small prompt if desired; not required for Decision 3A to operate).

**E. Defer artifact disposition.**

- Pro: keeps options open.
- Con: leaves an unresolved next-frontier item indefinitely; the probe precedent already provides a default ("untracked with SHA references in reports"); explicit acceptance of that default is cleaner than ongoing deferral.
- Reject in favor of A (which formalizes the default).

### 8.3 Probe precedent

The first-probe output dir at `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` has remained untracked since `9319d30` was committed. The substrate-validation memo `a8a9dd2` §10 and §11 reaffirmed the untracked status. The characterization output dir at `results/lane2_gdelt1_row_date_characterization/20260523T033234Z/` followed the same precedent (`858b501` §16). Decision 3A continues this discipline.

### 8.4 Repo-size implications

- Current paper / source / docs / test footprint: on the order of tens of MiB.
- Committing both payload dirs (option C): adds ≈ 146 MiB (≈ 4–5× the current tracked size, depending on revision).
- Committing only lightweight metadata (option B): adds ≈ 60 KiB.
- Option A: adds 0 bytes to the tracked tree.

### 8.5 Auditability implications

Committed reports (`9319d30`, `a8a9dd2`, `858b501`) preserve:

- Per-file HTTP outcomes.
- Per-file output-file SHA-256.
- Per-file row counts, distinct SQLDATE counts, offset-bucket counts, malformed / unparseable counts, header-anomaly flags, 2023+ flags.
- Aggregate metrics (offset totals, mismatch-rate distribution).
- Run command, environment, exit code.

The SHAs in the reports are sufficient to verify any future restored or re-fetched copy. The runner code is committed at `e9f8781` / `487dadb`; a future replay against the same locked URL list deterministically reproduces output structure modulo GDELT-side payload mutability.

### 8.6 Future re-validation reliance on reports + SHA tables

Yes — future re-validation can rely on:

- The committed reports' SHA tables for the bytes-witness function.
- The committed runner (`e9f8781` / `487dadb`) for the execution-procedure witness function.
- The committed locked URL lists (16 dates in `858b501` §6; 5 positive + 1 negative-control date in `9319d30`) for the input-set witness function.

A re-validation that requires byte-level inspection of the original output zips would either re-fetch from GDELT (subject to GDELT-side mutability) or request a copy of the original bytes from the original author. The committed reports remain the canonical record of what was observed when.

### 8.7 Temporary vs permanent

**Temporary.** The decision can be revisited by a future explicit prompt if:

- A downstream analysis requires bytes-on-disk audit evidence in the repo.
- A repo-wide artifact-tracking discipline change is proposed.
- The probe or characterization output dirs are about to be relocated, deleted, replaced, or otherwise mutated.

Until such a prompt is issued, both output dirs remain untracked, with SHA references in their respective committed reports.

## 9. Interaction among decisions

- **Decision 1B → Decision 2A**: under uniform SQLDATE re-keying, the build is independent of the exact T+1 transition date. The bracket `(2014-12-31, 2015-10-02]` is documentary-grade; finer precision would not improve build correctness. Decision 2A formalizes this.
- **Decision 1B → Decision 3A**: the build rule is fully captured by Decision 1B and the locked taxonomy at `858b501`; the output payload bytes are not load-bearing for build correctness given the committed reports and SHA tables. Decision 3A's untracked default is consistent.
- **Decision 2A → Decision 3A**: since no successor characterization is authorized by this memo, no additional output dir is anticipated. Decision 3A's scope remains the existing two dirs.
- **Decision 3A → Decisions 1B / 2A**: artifact disposition has no upstream effect on the build rule or the boundary-characterization decision; it is downstream from both.
- **All three → no-market-data firewall**: none of the three decisions approaches, touches, or relaxes the no-market-data firewall. All three are substrate-treatment and artifact-handling decisions only.

## 10. Consequences for the future full daily-count build design memo

The next eligible workstream after this memo is a **full daily-count build design memo** — design-level only, NOT execution. The full-build design memo must:

1. **Cite and adopt the locked premise from §5** as its starting point: re-key by `SQLDATE` uniformly across all seven lookback buckets `{0, −1, −7, −30, −365, −3650, +1}`.
2. **Implement Decision 1B exactly**: keep T+1 rows; re-key by `SQLDATE`; no special case in the re-keying logic; no per-row T+1-origin flag (the property is derivable from `(SQLDATE − publishing_file_date) == +1`); document the pre / post-2015 publishing-pipeline asymmetry without code-level branching.
3. **Cite Decision 2A**: build correctness does not depend on the exact T+1 boundary date; the 9-month bracket is documentary-grade.
4. **Cite Decision 3A**: payload bytes for probe and characterization remain untracked; SHA references in committed reports are the audit record.
5. **Specify build inputs**: the §10 recognized-list capture (SHA `84ea721e…fff835fc`), the locked `2013-04-01` to `2022-12-31` daily-regime window, the no-2023+ pre-filter posture at `0ddbd51`, and the F4 baselines (`41c80c0…624c39d` / `00ce9b2…f5e37552c`). No new GDELT contact for the design memo itself; execution would require a separate execution-authorization prompt.
6. **Specify build outputs**: a deterministic daily attention-count series keyed by event-date (`SQLDATE`) over the recognized universe; output schema TBD by the design memo.
7. **Specify aggregation arithmetic**: the SQLDATE-equality filter described in §6.6 of this memo. Edge handling at the recognized universe's boundaries (e.g., `2013-04-01` has no `f` at nominal date `d+3650 = 2023-04-01` because that file is excluded by the no-2023+ posture; `2022-12-31` has no `f` at nominal `d+1 = 2023-01-01` for the same reason; the T−3650 row in the `2013-04-01` file with SQLDATE `2003-04-04` falls outside the daily-regime window and must be handled by an explicit boundary rule).
8. **Specify what the build does NOT do**: no market data, no Step 2, no spike threshold, no signal extraction, no return-window logic, no category / theme / actor filtering. Build is substrate-side construction only.
9. **Specify three-guard discipline** for the build runner once it is implemented (mirroring the count-feasibility, event-file-probe, and characterization runners' three-guard pattern: module constant + CLI flag + env var).
10. **Specify enable-then-inert-restore commit-cycle expectations** for the build run (mirroring `60ec1521 → fe74255 → 9e329c2` / `e81208d → 7c85e3f → 9319d30` / `3537a62 → 73a7911 → 858b501`).
11. **Specify output-artifact disposition** for the build run's output dir up-front (consistent with Decision 3A's precedent: untracked indefinitely with SHA references in the build's post-run report).

The full-build design memo does **NOT** introduce market data, **NOT** Step 2, **NOT** spike / burst tuning, **NOT** execution. A subsequent **build-execution-authorization prompt** would then authorize the actual full-build run against the locked design memo, mirroring the structure of `3537a62 → 73a7911 → 858b501`.

## 11. Boundaries that remain in force

Until both the full-build design memo and the subsequent build-execution-authorization prompt have closed cleanly (including any post-run report and consolidated memory update), the following remain **blocked**:

- **Full daily-count build execution.**
- **Market data of any kind.**
- **Step 2 of any kind.**
- **Spike / burst threshold tuning.**
- **Return-window logic.**
- **Signal-design choices.**
- **Category / theme / actor / geography / tone filtering.**
- **Additional GDELT contact** beyond what a future explicitly-authorized successor characterization prompt or build-execution-authorization prompt may approve.
- **Event-file probe re-run** under the existing implementation.
- **Row-date characterization re-run** under the existing implementation.
- **Output-artifact disposition change** for `results/lane2_gdelt1_event_file_probe/20260522T221241Z/` or `results/lane2_gdelt1_row_date_characterization/20260523T033234Z/` beyond Decision 3A's "untracked indefinitely with SHA references in committed reports."
- **F4 modification** (baselines `41c80c0…624c39d` / `00ce9b2…f5e37552c` preserved).
- **Recognized-list capture modification** (SHA `84ea721e…fff835fc` preserved).
- **Guard flips on any runner.**
- **Source / test / config edits.**
- **Locked-memo edits** to any of `9319d30` / `a8a9dd2` / `a2a8fd5` / `e9f8781` / `487dadb` / `3537a62` / `73a7911` / `858b501` / `e55e09a` / `0b341b4` / `845c51c`.
- **Design-note edits** to the existing probe design note (`e55e09a`).
- **Post-§10 diagnostic report staging / commit / edit / delete.**
- **2023+ pre-filter authorization** (no-2023+ posture at `0ddbd51` is in force).
- **Frozen-snapshot execution** (no frozen-snapshot retrieval authorized).
- **`python3` canonicalization** changes.
- **Negative-control payload allow-list change.**
- **Staging / commit / push of this memo or any other artifact** unless separately authorized after review.

**Market data and Step 2 remain blocked unconditionally until the no-market-data firewall is explicitly retired by a future, separately authorized memo.** This memo does not authorize any such retirement.

## 12. Final verdict / next frontier

**Final verdict**: `PROCEED TO FULL-BUILD DESIGN MEMO AFTER LOCKING THESE DECISIONS.`

The three decisions in this memo —

- **Decision 1B**: keep T+1 rows and re-key them to `SQLDATE` uniformly with the other six buckets.
- **Decision 2A**: accept the 9-month bracket `(2014-12-31, 2015-10-02]` as sufficient; no finer T+1 boundary characterization authorized by this memo.
- **Decision 3A**: keep both output dirs (`results/lane2_gdelt1_event_file_probe/20260522T221241Z/` and `results/lane2_gdelt1_row_date_characterization/20260523T033234Z/`) untracked indefinitely with SHA references in committed reports; temporary, revisitable by a future explicit prompt.

— are sufficient to bridge from the characterization outcome `TAXONOMY-STABLE-WITH-TPLUS1-BOUNDARY` to a full daily-count build design memo without introducing market data, Step 2, spike / burst tuning, or any execution.

**Next frontier (NOT next; awaits explicit user initiation)**: full daily-count build design memo. Design-level only. No execution.

After the design memo closes, the next eligible workstream is a build-execution-authorization prompt that mirrors the structure of `3537a62 → 73a7911 → 858b501` against the locked build design.

Until both the design memo and the build-execution-authorization prompt close cleanly (including any post-run report and consolidated memory update), all blocks in §11 remain in force. The no-market-data firewall remains in force unconditionally.

This memo's authorization scope is complete upon persistence of `docs/lane2_gdelt1_post_characterization_decision_memo_v0.1.md`. No staging, commit, or push is authorized by this memo.
