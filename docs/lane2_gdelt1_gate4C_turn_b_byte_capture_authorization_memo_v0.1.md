# Lane 2 Gate 4C Re-review / Turn B Byte-capture Authorization Memo v0.1

## 1. Title and artifact status

**Title:** Lane 2 Gate 4C Re-review / Turn B Byte-capture Authorization Memo v0.1.

**Status:** Authorization-decision memo v0.1. Records a verdict on byte-capture authorization only.

This memo by itself does **not** execute byte-capture, perform a second GET, contact GDELT, fetch any external URL, request or download any event file, run any diagnostic, enter Gate 5, run count-feasibility, access market data, enter Step 2, flip any runner guard, modify F4, modify any source/test/config file, stage, commit, push, tag, amend, or edit memory. It records a verdict on whether to authorize, defer, or forbid a bounded byte-capture mechanism whose later execution would itself require a separate explicit prompt.

The memo evaluates one decision: should Lane 2 authorize a later separately initiated byte-capture step that persists Turn B-equivalent `LiveSafeExtraction` recognized-in-window unit identifiers to disk under the Gate 4C firewall, so that the offline pre-run diagnostic can read the recognized 3647-unit list it requires for the set difference `planned 3650 ∖ recognized 3647`.

## 2. Current reference frame

- **HEAD** = `f10c1bca8e9d25b63f57f6b0b927344760451904` (short: `f10c1bc`).
- **`origin/main`** = `d221e8fa7361b31b15fbc9f649dfffafce5d8fb5` (short: `d221e8f`).
- At this memo's drafting time, local `main` was **2 commits ahead** of origin (unpushed):
  - `d334ad5` — Record Lane 2 pre-run diagnostic precondition gap (halt report).
  - `f10c1bc` — Record Lane 2 recognized-list remediation decision (Option A).
- 8 pre-existing untracked items present (1 FMI design draft + 6 paper build artifacts + 1 results dir). 0 `M`/`A` on tracked files.
- **F4 SHA-256 baseline preserved** at the `d221e8f` §13.1 values:
  - `count_feasibility_metadata.json` (75,303 B, mtime 2026-05-18 18:33) = `41c80c095b1129cda0141dbe2d4cf1c9527cabc305118770e93b964c5624c39d`
  - `feasibility_summary.md` (393 B, mtime 2026-05-18 18:33) = `00ce9b24c7218041758694d84cac2ec17c240ece07b320d58363bccf5e37552c`
- **Runner guards inert**: `REAL_RETRIEVAL_ENABLED = False` at `src/lane2_gdelt1_count_feasibility.py:647`; `COUNT_FEASIBILITY_AUTHORIZED = False` at `scripts/run_lane2_gdelt1_count_feasibility.py:44`.
- **Lane 2 chain anchors carried forward**: Gate 4A `745af67`/`befbb94`/`bced9e1`; Gate 4B `159c392`; Gate 4C `54fb16a` (auth) / `ec1c3ec` (impl) / `e572c76` (conformance PASS); post-4C `f8345c8` (AUTHORIZE LATER EXECUTION; spent by Turn B); Gate 4D `a2851f4` (auth) / `7f5caee` (impl) / `9dea17c` (conformance PASS); Turn A approval `991321d`; Gate 5 decision `c2717a6` (AUTHORIZE LATER); Gate 5 run-enablement `175e939` (DEFER FOR DIAGNOSTIC); pre-run diagnostic authorization `d221e8f` (AUTHORIZE DIAGNOSTIC LATER); pre-run diagnostic halt report `d334ad5` (precondition-failure note); recognized-list remediation decision `f10c1bc` (Option A selected).

## 3. Chain context

- **`d221e8f` authorized the pre-run diagnostic later.** The diagnostic envelope was specified at `175e939` §§12–15 plus the `d221e8f` §13.1 mandatory F4-integrity precondition. Second-GET replication was explicitly excluded by `d221e8f` §12.
- **`d334ad5` recorded the diagnostic precondition gap.** The diagnostic halted before any set-difference, missing-unit enumeration, or clustering operation because the recognized 3647-unit list was not available offline. The §13.1 F4-integrity precondition itself PASSED 10/10 (recorded SHA-256 baseline in §2 above); the halt was at the *next* precondition: a data-availability one. Turn B's stdout / in-memory `LiveSafeExtraction` was transient and was not persisted to any reachable artifact.
- **`f10c1bc` selected Option A.** The recognized-list remediation decision memo argued three options (A: Gate 4C re-review / Turn B byte-capture; B: bundle byte-capture into a diagnostic-authorization v0.2; C: DEFER the broader Lane 2 path). It selected A on the principle that the defect is at the **evidence-capture layer** — the Gate 4C / Turn B path did not persist the bytes the offline diagnostic needs — not at the diagnostic-design layer. Remediating at the same layer as the defect preserves the chain's artifact-layer discipline.
- This memo is the artifact `f10c1bc` §7 named as the next active step.

## 4. Problem statement

The offline pre-run diagnostic, as designed by `175e939` §§12.1–12.2 and authorized for later separate execution by `d221e8f`, requires the set difference:

> **planned 3650 ∖ recognized 3647**

The two sides have asymmetric availability:

- **Planned 3650 (left-hand side)** is **available offline**. The F4-canonical metadata at `results/lane2_gdelt1_count_feasibility/20260518T163302Z/count_feasibility_metadata.json` contains the planned unit list at `layout_report.files_missing` (3,650 entries; 88 pre-2013 yearly+monthly + 3,562 post-2013 daily). The halt report at `d334ad5` confirmed this list, partition counts, and SHA-256 baseline.
- **Recognized 3647 (right-hand side)** is **not available offline**. Turn B's `LiveSafeExtraction` produced this list in transient memory, surfaced its counts to stdout under Gate 4C non-disguise discipline, and exited without writing the unit identifiers to disk. The halt report at `d334ad5` §6.1 confirmed the recognized-list source is absent from every reachable artifact (0 hits in repository and `/Users/jay` for `"recognized_in_window": 3647` as a structured value; 0 hits for `LiveSafeExtraction` serializations; 0 hits for `*turn_b*` / `*recognized*` filename patterns).

The arithmetic identity `3650 − 3647 = 3` is known by subtraction from Turn B's recorded summary counts, but it does **not** constitute set-difference evidence. Set-difference evidence requires the *identities* of the 3 missing units; clustering checks (by month / weekday / archive-format transition) require those identities too. Neither was producible offline at the halt report.

Therefore, **recognized-list byte-capture must be explicitly authorized before the diagnostic can be retried.** The diagnostic envelope (`175e939` §§12.1–12.2, `d221e8f` §13.1) is sound and does not need redesign. The missing piece is an offline-readable recognized 3647-unit list, which can only be produced by reopening the Gate 4C / Turn B evidence-capture layer.

## 5. Scope and mechanism of proposed byte-capture

### 5.1 Code path proposed for augmentation

The byte-capture would be a **new wrapper function** layered over the existing committed Gate 4C / Gate 4D live-safe path. No existing function is modified. Concretely:

- **Existing functions (not modified):**
  - `LiveSafeExtraction` (class) at `src/lane2_gdelt1_count_feasibility.py:1157`
  - `extract_index_units_live_safe(...)` at `src/lane2_gdelt1_count_feasibility.py:1172`
  - `fetch_archive_index_live_safe(...)` at `src/lane2_gdelt1_count_feasibility.py:1251`
  - `RedirectBlocked` (exception) at `src/lane2_gdelt1_count_feasibility.py:1294`
  - `_NoFollowRedirectHandler` at `src/lane2_gdelt1_count_feasibility.py:1301`
  - `build_redirect_disabled_opener(timeout: float = 30.0)` at `src/lane2_gdelt1_count_feasibility.py:1321`
  - `fetch_index_live_once(...)` at `src/lane2_gdelt1_count_feasibility.py:1344`
- **New wrapper (to be implemented under a separate explicit step if this memo's verdict is AUTHORIZE LATER):**
  - Suggested name: `capture_recognized_list_once(capture_dir: str, authorization_commit: str, timeout: float = 30.0)`
  - Suggested location: `src/lane2_gdelt1_count_feasibility.py` (appended below `fetch_index_live_once`; no edit of existing functions)
  - Behavior: invokes `fetch_index_live_once(timeout=...)` exactly once → receives the `LiveSafeExtraction` object → serializes the recognized-in-window field and minimal provenance to a JSON file at the capture path → computes SHA-256 of the serialized JSON bytes → performs the mandatory L5 regex scan on the JSON body → aborts (raises) if the L5 scan finds any match.
- **Tests (to be added under the same separate step):** synthetic-opener tests in `tests/test_lane2_gdelt1_count_feasibility.py` parallel to the Gate 4D test pattern. No network. No real GDELT post-2022 filenames in fixtures.

The wrapper is a thin serialization layer. It does not change extraction semantics; it does not alter the Gate 4C live-safe firewall or the Gate 4D redirect-disabled opener; it does not add a fallback URL; it does not retry; it does not call `DEFAULT_GDELT1_BASE_URL` or any event-file URL.

### 5.2 Fields written to disk

The captured artifact is a JSON object with exactly these fields:

- `recognized_in_window_units` — array of in-window 2005–2022 unit identifiers (strings, format matching the F4-canonical `files_missing` style, e.g. `"2005"`, `"2006-01"`, …, `"2022-12-31"`). Expected length: **3647** (matching Turn B's recorded count).
- `recognized_in_window_count` — integer, must equal `len(recognized_in_window_units)`.
- `ignored_out_of_window_count` — integer (Turn B recorded 26; the capture re-records whatever the live extraction yields).
- `rejected_2023plus_count` — integer (Turn B recorded 1216).
- `post2022_form_classes` — array of non-identifying form-class labels (e.g., `["daily_export"]`; per Gate 4C aggregation discipline; **no real post-2022 filenames** under any condition).
- `unrecognized_tokens_count` — integer (Turn B recorded 1).
- `malformed_gdelt_tokens_count` — integer (Turn B recorded 0).
- `l5_regex_pattern` — string, the exact pattern: `\b\d{8,14}\.(?:export|gkg|mentions)\.(?:CSV|csv)\.zip\b`.
- `l5_regex_matches_in_artifact_body` — integer, must be **0**; non-zero halts and aborts the capture without writing.
- `provenance` — object with sub-fields:
  - `gate_4c_authorization_commit` = `"54fb16a"`
  - `gate_4c_implementation_commit` = `"ec1c3ec"`
  - `gate_4c_conformance_commit` = `"e572c76"`
  - `gate_4d_authorization_commit` = `"a2851f4"`
  - `gate_4d_implementation_commit` = `"7f5caee"`
  - `gate_4d_conformance_commit` = `"9dea17c"`
  - `post_4c_live_execution_authorization_commit` = `"f8345c8"` (historical reference; not re-used as live authorization)
  - `turn_a_approval_commit` = `"991321d"` (historical reference)
  - `turn_b_outcome` = `"L1"` (historical reference to Turn B's recorded outcome class)
  - `recognized_list_remediation_decision_commit` = `"f10c1bc"` (Option A selected)
  - `byte_capture_authorization_memo_commit` = **filled in at execution time** with this memo's eventual commit hash (the future execution step must record it).
- `capture_timestamp_iso8601_utc` — string, ISO-8601 UTC timestamp when the capture executed.
- `index_url` — string, must equal `DEFAULT_GDELT1_INDEX_URL` (the same URL Turn B used; no event-file URL, no base URL).
- `single_get_confirmation` — bool, must be `true`; the capture asserts exactly one live GET was performed.

The JSON is canonicalized (sorted keys, UTF-8, deterministic float formatting if any floats appear) so the SHA-256 is stable for re-verification.

### 5.3 Filename and directory

- **Directory:** `results/lane2_gdelt1_turn_b_recognized_list_capture/<YYYYMMDDTHHMMSSZ>/` (new top-level results subdirectory; **not** a child of the F4 directory `results/lane2_gdelt1_count_feasibility/20260518T163302Z/`, to preserve F4's canonical/consumed/untouched state).
- **Filename:** `recognized_list.json` (the JSON artifact described in §5.2).
- **Companion file:** `recognized_list.sha256` (a one-line text file containing the SHA-256 of `recognized_list.json` followed by two spaces and the filename, in `shasum -a 256` format). This allows independent verification without re-reading the JSON.

Both files are written once at capture time. Neither is later mutated. The directory is one-shot.

### 5.4 Format and accompanying metadata

- **Format:** JSON (per §5.2). JSON is chosen over CSV/TXT because the artifact carries mixed structured data (array of identifiers + counts + provenance object + nested fields) and because future readers will need stable field-name access for the set-difference operation. CSV would force a single-table flat layout that doesn't fit the provenance/metadata; TXT would lose structure and prevent automated verification.
- **Accompanying metadata:**
  - SHA-256 of the JSON in the companion `.sha256` file (§5.3).
  - L5 regex scan result inside the JSON (§5.2).
  - Provenance commit hashes inside the JSON (§5.2).
  - Captured-at timestamp inside the JSON (§5.2).
- **No additional sidecar files** beyond the two named above. The capture is two-file: the data + the SHA-256 sidecar.

### 5.5 How the artifact serves the offline set-difference

A future diagnostic re-attempt (under its own separately initiated step) would:

1. Verify F4 SHA-256 baseline per `d221e8f` §13.1 (unchanged).
2. Verify the captured artifact's SHA-256 against the `.sha256` sidecar.
3. Read `recognized_list.json` and extract `recognized_in_window_units` (the 3647-element array).
4. Read F4 metadata's `layout_report.files_missing` (the 3650-element planned array).
5. Compute the set difference `planned 3650 ∖ recognized 3647` — the result must be exactly 3 unit identifiers.
6. Apply `175e939` §15 stop conditions to the result (gap > 3, gap < 3, structural clustering, firewall breach).
7. Produce a diagnostic report v0.2 that supersedes the precondition-failure note at `d334ad5`.

The artifact does not need to be re-read or mutated after step 1's SHA-256 verification; it is consume-once-read-many-times.

### 5.6 Explicit out-of-scope clauses

This memo's authorization (if granted) covers byte-capture only. Explicitly **not in scope**:

- **No real post-2022 filename surfacing.** Post-2022 tokens remain aggregated to form-class labels (e.g., `daily_export`) with zero filename retention, per the Gate 4C non-disguise discipline.
- **No event-file requests or downloads.** The capture's single GET is the live index URL only, identical to Turn B.
- **No market data.** Lane 2 market-data contact remains out of scope.
- **No count-feasibility run.** The capture writes a unit-list artifact, not per-unit event counts.
- **No Gate 5 entry.** Gate 5 remains downstream of (i) a successful byte-capture, (ii) a successful diagnostic re-attempt, (iii) a Gate 5 run-enablement memo v0.2.
- **No diagnostic rerun in the same memo.** Diagnostic re-attempt is a separate later step gated by this memo's verdict + a separate diagnostic execution prompt.
- **No source pivot.** GDELT 1.0 remains the source; no fallback / alternative source is invoked.
- **No fallback path.** Single GET only; no retry, no second URL, no event-file fallback.

## 6. Gate 4C firewall preservation

The byte-capture must preserve every Gate 4C firewall property already proved by the conformance review at `e572c76`:

- **No real post-2022 filenames surfaced** in any of the 9 Gate 4C channels (stdout, stderr, logs, exception messages, traceback frames, return values, structured fields, artifact bodies, sidecar files). The capture path is a new write surface and must inherit this discipline by construction.
- **Post-2022 tokens remain aggregated** only as non-identifying form-class labels (e.g., `daily_export`). The capture's `post2022_form_classes` field is a small string list (Turn B saw `["daily_export"]`); the capture must not include any per-token filename data.
- **Mandatory L5 regex scan** before any report or artifact is accepted. The pattern is `\b\d{8,14}\.(?:export|gkg|mentions)\.(?:CSV|csv)\.zip\b`. The scan runs against the entire captured JSON body and the SHA-256 sidecar. **0 matches required; any positive match halts capture and aborts the write.** The scan result is itself written into the JSON (§5.2) for later verification.
- **No source pivot / fallback.** GDELT 1.0 only. No GDELT 2.0 GKG, no GDELT Event database alternative, no DOC API, no Google Trends, no Wikipedia pageviews, no other proxy.
- **No event-file request or download.** The capture's single GET targets `DEFAULT_GDELT1_INDEX_URL` only. No `DEFAULT_GDELT1_BASE_URL`. No constructed event-file URLs. The Gate 4C live-safe path `fetch_archive_index_live_safe` is invoked without modification.
- **No reuse of spent authorizations as live authorization.** `60ec1521` (the prior count-feasibility run authorization) and `fe742555` (the prior run-enablement that flipped `COUNT_FEASIBILITY_AUTHORIZED` to True before the F4 attempt) remain spent. The post-4C `f8345c8` AUTHORIZE LATER EXECUTION was spent by Turn B; a new bounded authorization analogous to `f8345c8` would be required for the capture's second GET (see §7).

The byte-capture's structural firewall preservation is achievable because the existing committed Gate 4C live-safe path already enforces these properties; the wrapper adds only a write step, and the write step is gated by the L5 scan + the SHA-256-recorded JSON body, both of which can be validated *before* the file is finalized on disk.

## 7. Second-GET question

**A second live GET is required.** This is an honest and non-negotiable consequence of the chain state:

- Turn B's in-memory `LiveSafeExtraction` is gone.
- The recognized list was not persisted at Turn B time.
- No equivalent offline artifact exists anywhere reachable (per `d334ad5` §6.1 search).
- Therefore, the recognized list can only be reconstructed by performing another live GET that produces an equivalent `LiveSafeExtraction` and then capturing its bytes to disk.

The second GET must be **separately bounded under post-4C-style discipline** analogous to `f8345c8`:

- Exactly **one** live GET; no retry; no fallback; no second GET (the capture's GET is itself the "single" GET — not a second one *within* the capture).
- Target URL: `DEFAULT_GDELT1_INDEX_URL` only. No event-file URL. No base URL.
- Through the unchanged **Gate 4D redirect-disabled opener** (`build_redirect_disabled_opener`, `_NoFollowRedirectHandler` blocks 301/302/303/307/308).
- Through the unchanged **Gate 4C live-safe path** (`fetch_archive_index_live_safe`, `LiveSafeExtraction`).
- **Inert-restore discipline:** if any runner guard is opened to enable the capture (it should not need to be — the capture's wrapper operates above the guards, not below them — but if for any reason guard state must be temporarily changed, the same inert-restore pattern as `60ec152 → fe74255 → 9e329c2` applies, with new commits, not reuse of spent ones).
- **One-run-only:** technical/protocol failure routes to a fresh memo, not a patch-and-rerun.

**The memo itself does NOT perform that second GET.** This memo is an authorization-decision artifact, not an execution step. The memo argues whether to authorize a later separately initiated capture step (which would, if and only if separately initiated, perform the second GET inside the capture wrapper). The capture's second GET is downstream of this memo's verdict, the capture step's separate explicit initiation prompt, and the capture wrapper's implementation.

If this memo's verdict is **AUTHORIZE LATER** (see §8–§9), four further separately initiated steps would be required before any second GET fires:

1. A wrapper-implementation step (write `capture_recognized_list_once` + its synthetic-opener tests; no network).
2. A wrapper-conformance review (analogous to Gate 4D conformance at `9dea17c`; read-only audit; no network).
3. A separate live-execution approval memo (analogous to Turn A approval at `991321d`).
4. A separate live-execution readiness prompt (analogous to the Turn A readiness preflight).

The fifth separately initiated step (analogous to Turn B itself) IS the capture's second GET, not a precondition for it. Each of those steps would be its own artifact under standing chain discipline.

## 8. Verdict options

The memo evaluates a ternary:

- **AUTHORIZE LATER.** Authorize a later separately initiated byte-capture execution prompt under the strict constraints of §6, §7, §10, and §11. The memo itself does not execute anything; the wrapper is not implemented by this memo; the second GET is not fired by this memo.
- **DEFER.** Do not authorize yet. Specify what additional design work, firewall analysis, or chain alignment is needed before authorization is appropriate. DEFER must name a specific resolvable uncertainty and a concrete trigger for reconsideration.
- **FORBID.** Reject byte-capture on the grounds that it cannot be made compatible with the Gate 4C firewall, the Gate 4D redirect-disabled opener, the L5 scan discipline, the no-source-pivot rule, the no-event-file rule, the one-run-only rule, or the no-spent-authorization-reuse rule. FORBID would close the Option A path entirely and route the chain back to a substrate-comparison memo or to a broader DEFER on Lane 2.

Each option is argued in turn before §9 selects one. Each is argued on its strongest grounds.

### 8.1 Case for AUTHORIZE LATER

- The mechanism in §5 is precisely specifiable. The wrapper layers over committed Gate 4C / Gate 4D functions without modifying them; the captured artifact is a small structured JSON with explicit fields; the firewall properties are preserved by the L5 scan + form-class aggregation rule.
- The defect that triggered this branch (recognized list not captured offline) is at the evidence-capture layer, and the proposed remediation is at the same layer. Per `f10c1bc` Option A reasoning, this is the principled artifact layer for the fix.
- The capture's scope is **strictly narrower** than the prior Turn B scope: Turn B retrieved the live index *and* did extraction; the capture does the same plus a single bounded JSON write. No event-file fetch, no extra HTTP request, no source pivot.
- The cost of *not* authorizing is that Lane 2 remains stuck at the diagnostic halt indefinitely: the diagnostic envelope is sound but the input it requires cannot be produced without this capture (or an equivalent).
- AUTHORIZE LATER is **not execution.** It permits a later separately initiated capture step, gated by additional artifacts (wrapper implementation, conformance review, live-execution approval memo, live-execution readiness prompt).

The weakest form (to avoid): "byte-capture is small, so it should be authorized." That argument inherits authority by minimization. The correct argument is the mechanism-specifiable + layer-discipline argument above.

### 8.2 Case for DEFER

- The wrapper-implementation step is not yet drafted; the field schema in §5.2 is the memo's best specification but has not been reviewed by a separate implementation memo.
- The L5 regex scan's coverage across all 9 Gate 4C channels for a new write surface has been argued in principle but not conformance-reviewed for the specific case of writing a JSON file containing 3,647 in-window identifiers. A specific Gate 4C re-review note could close that gap before authorization.
- The captured JSON's exact provenance fields could be debated: should they include the SHA-256 of the F4 metadata at capture time, to bind the capture to the planned-list baseline? (The §5.2 schema does not currently require this.) A DEFER could insist on resolving such design questions before authorization.

The weakest form (to avoid): "we should always wait for more design review." DEFER must name a specific resolvable design question and a concrete trigger. The strongest concrete trigger candidate is: "Gate 4C re-review note specifically scoped to the JSON write surface, validating that the 9-channel firewall coverage extends to the capture artifact's body and sidecar."

### 8.3 Case for FORBID

- The byte-capture introduces a new write surface that did not exist when the Gate 4C conformance review at `e572c76` PASSed. The conformance review's binding §3 list of 9 non-surfacing channels was scoped to the existing extraction path, not to a new on-disk artifact. A precautionary FORBID would argue that Gate 4C's firewall guarantee cannot be extended to a new artifact body by argument alone — it needs its own conformance review, and until then byte-capture should be refused.
- The byte-capture requires a second live GET. Even with post-4C-style discipline, every additional GDELT contact carries marginal substrate exposure risk. The original count-only protocol (`147c0d4` §3) said GDELT 1.0 should be used "only if longer history is needed"; FORBIDding the capture forces the chain to reconsider whether GDELT 1.0 is the right source at all, before more retrievals accumulate.
- The captured artifact would itself become a new piece of standing state in the repository. If it ever leaked a post-2022 identifier, the leak would be in a tracked-and-committed file, harder to remove than a transient stdout. FORBID avoids that risk class entirely.

The weakest form (to avoid): "we haven't seen the capture work, therefore forbid." That argument would forbid every research step. The correct FORBID argument is the new-write-surface / firewall-not-yet-reviewed argument above; if that argument is decisive, the chain pivots to substrate-comparison instead.

## 9. Recommended verdict

**AUTHORIZE LATER.**

Reasoning, weighing §§8.1–8.3 against the §5 mechanism specification and the §6/§7 firewall + second-GET constraints:

- The mechanism in §5 is positively specified to the field level. The wrapper is a thin serialization layer over committed and conformance-passed Gate 4C / Gate 4D functions. The captured artifact is a bounded JSON object. The firewall preservation argument in §6 is structural, not promissory: the L5 scan runs over the JSON body *before* the file is finalized; the form-class aggregation rule remains binding; no real post-2022 filenames can pass through.
- The DEFER concerns (§8.2) are about additional review *of an already-specified mechanism*, not about an underspecified mechanism. Those concerns are appropriately addressed by **gating the future wrapper-implementation step on its own conformance review** (analogous to Gate 4D's `9dea17c` PASS gate before Turn A approval). That gate is built into the §10 execution envelope below. DEFER would add a separate "pre-authorization review" cycle that effectively duplicates the existing conformance-review gate; the proposed envelope already provides that gate via the wrapper-conformance step.
- The FORBID concerns (§8.3) are principled but do not match the current evidence. The Gate 4C 9-channel firewall is structural and inheritable by a new write surface *if* the L5 scan + form-class aggregation rules are preserved over the new surface — which §5/§6 specify. The second-GET concern is real but bounded: a single GET under post-4C-style discipline is the same shape Turn B already executed cleanly. The standing-state-leak concern is mitigated by the mandatory L5 scan + the JSON's content discipline + the abort-before-write rule on any positive scan.
- The cost of FORBID is that the Lane 2 chain stops at the diagnostic halt indefinitely without a substrate-comparison memo path opening. The cost of DEFER is one extra cycle for no additional decision-relevant evidence beyond what AUTHORIZE LATER's downstream gates already deliver. AUTHORIZE LATER preserves chain motion while keeping every subsequent step explicit and bounded.

**AUTHORIZE LATER does not execute byte-capture. AUTHORIZE LATER does not perform a second GET. AUTHORIZE LATER does not modify F4. AUTHORIZE LATER does not flip any runner guard. AUTHORIZE LATER does not contact GDELT, does not request event files, does not access market data, and does not authorize Step 2. A separately initiated wrapper-implementation step, a separately initiated wrapper-conformance review, a separately initiated live-execution approval memo, and a separately initiated live-execution readiness prompt are each still required before any second GET fires; the live-execution prompt itself IS the second GET, not a precondition for it.** Diagnostic re-attempt remains separately gated after byte-capture exists.

If this verdict is approved at memo-commit time, the chain advances by exactly one artifact (this memo). Every subsequent step remains under standing chain discipline.

## 10. Allowed future execution envelope

If AUTHORIZE LATER is selected at this memo's commit time, the future execution envelope is precisely:

### 10.1 Wrapper implementation step (separate future prompt)

- New function `capture_recognized_list_once(capture_dir: str, authorization_commit: str, timeout: float = 30.0)` appended to `src/lane2_gdelt1_count_feasibility.py`; **no edits to existing functions**.
- Synthetic-opener tests in `tests/test_lane2_gdelt1_count_feasibility.py` covering: redirect-disabled property is preserved; L5 scan triggers an abort on a post-2022-pattern-leaking fixture; SHA-256 sidecar matches the JSON body byte-for-byte; structured-field shape per §5.2; **no real network**; **no real GDELT post-2022 filenames** in any fixture.
- Implementation commit lands under standing position-1 discipline (write → review → pre-commit cleanup → commit). **No live GET in this step.** Guards remain inert (`REAL_RETRIEVAL_ENABLED = False`, `COUNT_FEASIBILITY_AUTHORIZED = False`).

### 10.2 Wrapper conformance-review step (separate future prompt)

- Analogous to Gate 4D conformance at `9dea17c`: read-only audit; no network; cache-disabled test re-run; structured 9-channel firewall coverage check; verdict PASS / NEEDS FIX / FAIL.
- Only on PASS does the chain proceed to §10.3.

### 10.3 Capture live-execution approval memo (separate future prompt)

- Analogous to Turn A approval at `991321d`: an authorization memo that authorizes **only the next separately initiated capture live-execution readiness prompt**, not the capture's GET itself. Decision verdict: AUTHORIZE / DEFER / DENY.
- Anchors: this memo's commit, §10.1's implementation commit, §10.2's conformance-PASS commit, plus the prior Gate 4C / Gate 4D / post-4C chain.
- Memo fires no request; no guard flip; no F4 touch.

### 10.4 Capture live-execution readiness prompt (separate future prompt)

- Analogous to Turn A's readiness check: read-only preflight against `f10c1bc`, this memo, §10.1, §10.2, §10.3; no network; structured 10-criteria check; verdict READY / NOT READY.
- Only on READY does the chain proceed to §10.5.

### 10.5 Capture live-execution prompt (separate future prompt)

- Analogous to Turn B: a single user-initiated live execution.
- Exactly **one** live GET via `capture_recognized_list_once(...)` → `fetch_index_live_once(...)` → `fetch_archive_index_live_safe(opener=<Gate 4D redirect-disabled>, ...)`.
- No retry. No fallback. No second GET. No base `/events/` fallback. No event-file request. No source pivot.
- Writes exactly two files: `recognized_list.json` and `recognized_list.sha256` at the new directory `results/lane2_gdelt1_turn_b_recognized_list_capture/<NEW_TIMESTAMP>Z/` (timestamp distinct from F4's `20260518T163302Z`).
- **F4 untouched.** SHA-256 recheck before and after the capture against the `d221e8f` §13.1 baseline.
- **Guard discipline:** if any guard must be temporarily flipped (it should not be; the capture wrapper is layered above the count-feasibility runner and does not need `COUNT_FEASIBILITY_AUTHORIZED` to be True), then the analogous `60ec152 → fe74255 → 9e329c2` inert-restore pattern applies with **fresh commits** — `60ec1521` and `fe742555` are spent and may not be reused.
- One-run-only. Technical / protocol failure routes to a fresh memo.
- **No Gate 5. No count-feasibility. No market data. No Step 2. No diagnostic rerun** in the same prompt (diagnostic rerun is gated by its own separately initiated step after the capture artifact lands and is committed).

### 10.6 Capture report / closure (separate future prompt)

- A small report draft analogous to the diagnostic halt report at `d334ad5`: SHA-256 of the new artifact, recognized count = 3647 (must match), L5 scan = 0 matches (must match), F4 SHA-256 recheck (must match baseline), guards post-state (must match pre-state unless §10.5's inert-restore logged a temporary flip).
- Standard position-1 discipline + pre-commit self-status cleanup.

### 10.7 Memory update (separate future prompt)

Memory update under standing memory-update discipline after the capture-report commit. No memory edit by any earlier step.

## 11. Stop conditions

The capture (when later authorized and run under §10.5) must halt and escalate (no auto-proceed) if any of the following are observed:

- **F4 mismatch.** Any of the F4 baseline SHA-256s, sizes, or mtimes deviate from `d221e8f` §13.1 + §2 above. Halt before any capture write. Route to F4-integrity / Gate 4C re-review memo.
- **Guard mismatch.** `REAL_RETRIEVAL_ENABLED` or `COUNT_FEASIBILITY_AUTHORIZED` is not `False` at capture-start (other than a temporary flip explicitly authorized by §10's inert-restore pattern); or any guard restore fails post-capture. Halt; route to guard-integrity memo.
- **Unexpected tracked modifications.** `git status --short` shows any `M` or `A` on tracked files at capture-start. Halt; route to working-tree integrity review.
- **Target capture artifact already exists unexpectedly.** `recognized_list.json` or `recognized_list.sha256` at the chosen timestamped path already exists before the capture writes. Halt; route to artifact-namespace review (the timestamp directory should be unique).
- **Any post-2022 real filename would be surfaced.** The capture wrapper's pre-write checks find a real post-2022 filename in the JSON body, sidecar, stdout, stderr, log, exception text, traceback, return value, or structured field. Halt before write; route to Gate 4C firewall re-review.
- **L5 regex scan positive.** The mandatory L5 scan on the JSON body or sidecar finds ≥1 match. Halt before finalizing the write; route to Gate 4C firewall re-review.
- **More than one live GET would be needed.** Network failure, redirect attempt blocked, timeout, or any condition that would require a retry. Halt; route to a fresh memo (no retry without new authorization).
- **Source pivot or fallback required.** Any code path attempts `DEFAULT_GDELT1_BASE_URL`, an event-file URL, or any URL other than `DEFAULT_GDELT1_INDEX_URL`. Halt; route to source-selection re-review.
- **Event-file download required.** Any code path attempts an event-file request. Halt; route to Gate 4 body-access re-review.
- **Byte-capture cannot produce a recognized 3647-unit list.** The extraction returns a count that is not exactly 3647 — see the two sub-cases below.
- **Output count > 3647.** The captured list contains more than 3647 in-window units (would contradict Turn B's recorded recognized count by an unexpected positive margin). Halt; route to substrate-comparison memo. The captured artifact remains uncommitted pending review.
- **Output count < 3647.** The captured list contains fewer than 3647 in-window units (would contradict Turn B's recorded recognized count by a negative margin). Halt; route to Gate 4C re-review / Turn B re-verification memo. Could indicate substrate drift between Turn B and the capture-time GET.
- **Output count = 3647 but identity mismatch.** (Diagnostic-time stop condition, not capture-time.) The captured list has 3647 elements but the set difference against the planned 3650 yields fewer or more than 3 missing units — handled at diagnostic re-attempt time by `175e939` §15 stop conditions; not this memo's concern.
- **Any F4 mutation observed during the capture.** Halt; route to F4-integrity memo. F4 must be byte-identical pre/post.
- **Any guard restore failure.** Halt; route to guard-integrity memo. Guards must be inert at capture-end (unless explicitly temporarily flipped per §10's inert-restore pattern, in which case they must be re-flipped to inert by a committed inert-restore commit).
- **Capture wrapper crash.** Any unhandled exception. Halt; route to wrapper-implementation re-review.

In all stop cases: **no auto-proceed to diagnostic rerun, no auto-proceed to Gate 5, no auto-retry of the capture.**

## 12. Non-authorization statement

This memo does **NOT** authorize, by itself or by inference:

- **Byte-capture execution now.** The capture wrapper does not yet exist; the wrapper-implementation step (§10.1) is gated by this memo's commit; the wrapper-conformance step (§10.2), the live-execution approval (§10.3), the live-execution readiness prompt (§10.4), and the live-execution prompt (§10.5) are each gated by their predecessors.
- **Second GET now.** No live GET fires from this memo. The capture's second GET, if and when it occurs, is downstream of §10.5 and not before.
- **Diagnostic rerun.** Diagnostic re-attempt is downstream of the capture-report commit (§10.6) and requires its own separate authorization and execution prompts.
- **Gate 5.** Gate 5 remains downstream of (i) successful byte-capture, (ii) successful diagnostic re-attempt, (iii) a Gate 5 run-enablement memo v0.2, (iv) a Gate 5 run-enablement commit, (v) the Gate 5 run.
- **Count-feasibility.** Runner guards remain `False`. The capture wrapper does not require `COUNT_FEASIBILITY_AUTHORIZED = True`.
- **Market data.** Lane 2 market-data contact remains out of scope.
- **Step 2.** Step 2 lock and entry remain blocked behind Gate 5 closure.
- **F4 modification.** F4 SHA-256 baseline (per §2) must be preserved across the entire downstream chain. Any deviation halts.
- **Guard flip now.** Guards remain inert. Any future guard flip requires its own separately committed run-enablement step with inert-restore discipline.
- **Push.** No push of any commit is authorized by this memo. Push posture is per §13.
- **Commit.** No commit beyond this memo's own commit is authorized.

Safety success at Gate 4C, Gate 4D, and during Turn B remains **necessary but not sufficient** for any subsequent Lane 2 step. The Gate 5 decision memo's AUTHORIZE LATER (`c2717a6`), the run-enablement memo's DEFER FOR DIAGNOSTIC (`175e939`), the pre-run diagnostic authorization memo's AUTHORIZE DIAGNOSTIC LATER (`d221e8f`), the halt report (`d334ad5`), and the recognized-list remediation Option A selection (`f10c1bc`) are each **necessary but not sufficient** for byte-capture authorization. This memo, if approved and committed, will be **necessary but not sufficient** for the wrapper-implementation step; and so on down the §10 chain.

## 13. Commit and push posture

### 13.1 Commit posture

Position 1 for the memo itself: write → review → pre-commit self-status cleanup if needed → commit standalone with a verbatim message specified at commit time. Suggested message form: `Add Lane 2 Gate 4C re-review / Turn B byte-capture authorization memo v0.1`.

### 13.2 Push posture

Push posture is a separate later decision and is not authorized by this memo. Current planning lean inherits `f10c1bc` §8's posture-2 lean: push after this memo is also committed, so origin/main advances with the decision-plus-authorization pair (decision = `f10c1bc`, authorization = this memo's eventual commit) rather than the decision alone. This is a planning lean only, not a push authorization; the push posture may still be revised in a separate later decision.

The prior two unpushed commits on local `main` (`d334ad5` halt report + `f10c1bc` decision) would, under posture 2, be pushed together with this memo's commit — three commits in one push. Whether that grouping is the right unit is itself a separate decision at push time, not now.

## 14. Cross-references

- **`d221e8f`** — pre-run diagnostic authorization memo v0.1 (verdict AUTHORIZE DIAGNOSTIC LATER; second-GET excluded; §13.1 mandatory F4-integrity precondition).
- **`d334ad5`** — pre-run diagnostic halt report (commit message: `Record Lane 2 pre-run diagnostic precondition gap`; documents that the recognized 3647-unit list was not available offline; recorded F4 SHA-256 baseline).
- **`f10c1bc`** — recognized-list remediation decision memo v0.1 (commit message: `Record Lane 2 recognized-list remediation decision (Option A)`; selected Option A — Gate 4C re-review / Turn B byte-capture; this memo is the §7-named next artifact).
- **Gate 4C anchors:** `54fb16a` (authorization), `ec1c3ec` (implementation), `e572c76` (conformance review PASS, binding §3 = 9-channel non-surfacing list).
- **Gate 4D anchors:** `a2851f4` (authorization), `7f5caee` (implementation), `9dea17c` (conformance review PASS).
- **post-4C live-execution authorization:** `f8345c8` (AUTHORIZE LATER EXECUTION; spent by Turn B).
- **Turn A approval:** `991321d`.
- **Gate 5 anchors:** `c2717a6` (decision memo, AUTHORIZE LATER), `175e939` (run-enablement memo, DEFER FOR DIAGNOSTIC).
- **F4 substrate:** `results/lane2_gdelt1_count_feasibility/20260518T163302Z/` (canonical, consumed, untouched; SHA-256 baseline preserved in this memo §2 and `d221e8f` §13.1).
- **Source functions referenced (no edits in this memo):**
  - `LiveSafeExtraction` at `src/lane2_gdelt1_count_feasibility.py:1157`
  - `extract_index_units_live_safe` at `src/lane2_gdelt1_count_feasibility.py:1172`
  - `fetch_archive_index_live_safe` at `src/lane2_gdelt1_count_feasibility.py:1251`
  - `RedirectBlocked` at `src/lane2_gdelt1_count_feasibility.py:1294`
  - `_NoFollowRedirectHandler` at `src/lane2_gdelt1_count_feasibility.py:1301`
  - `build_redirect_disabled_opener` at `src/lane2_gdelt1_count_feasibility.py:1321`
  - `fetch_index_live_once` at `src/lane2_gdelt1_count_feasibility.py:1344`
- **Handout-freshness discipline:** `feedback_handout_freshness.md` item 6 — to be applied to this memo's body before any future commit per §13.1.

— end of Gate 4C re-review / Turn B byte-capture authorization memo v0.1 (verdict AUTHORIZE LATER under §10 envelope; byte-capture NOT EXECUTED; second GET NOT EXECUTED; diagnostic rerun NOT AUTHORIZED; Gate 5 NOT EXECUTED; F4 untouched; guards inert) —
