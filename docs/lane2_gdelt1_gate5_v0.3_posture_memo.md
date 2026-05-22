# Lane 2 GDELT1 Gate 5 v0.3 Posture Memo — Frozen Recognized Universe Direction

## 1. Status

This is a **posture memo, not a run-enablement memo**. It defines Lane 2's preferred substrate path going forward and the relationship between the live GDELT 1.0 archive and the already-tracked §10 recognized-list capture. It does not authorize a count-feasibility run, code changes, a live GET, a second GET, a capture, market data ingest, Step 2, or Gate 5 execution. Each of those remains gated on its own future authorization.

Successor relationship: v0.2 (`57f42cc`, verdict `AUTHORIZE COUNT-FEASIBILITY LATER`) was satisfied at the run-attempt layer; the post-run report at `b1dfd00` records the actual outcome. v0.3 takes the v0.2 §6 caveat and the v0.2 post-run report as its starting facts and resolves only the **default substrate question**.

## 2. What v0.2 established

- The v0.2 run was executed exactly once under authorization `57f42cc`, with enablement `89a5bcb` → run → inert-restore `a6e5ebb`, and persisted in the tracked post-run report `b1dfd00` (`docs/lane2_gdelt1_gate5_post_run_report_v0.2.md`).
- Verdict: `RUN-HALTED-BOUNDARY` — `Protocol2023PlusBreach` with `rejected_2023plus = 1219` raised inside `extract_index_units` (`src/lane2_gdelt1_count_feasibility.py:1131`), upstream of `run_count_only_feasibility` and upstream of `verify_archive_layout`.
- The breach was driven by the **listing itself**, not by anything inside the in-window 2005–2022 subset: current GDELT 1.0 dailies (`20260519`–`20260521.export.CSV.zip` and ≥1,216 others) are now advertised in `events/index.html` by construction, because the upstream archive is current as of 2026-05-22.
- The §6 caveat (`'2013'` dropped at universe-construction; the four 2014 dailies — `2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19` — as known substrate gaps) was **not exercised** by the run; the run aborted before any planned-vs-recognized comparison ran.
- The §10 capture (`results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json`, SHA-256 `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`, tracked at `4015b97`) remains the only live, on-disk evidence about which in-window units the upstream actually advertises (`recognized_in_window_count=3647`).

## 3. Why the live archive path is no longer the default

Three properties of the v0.2 outcome converge:

1. **Structural, not transient.** The 2023+ tokens in the upstream listing are not noise; they are correctly published current-date dailies. The listing is cumulative, and the upstream's protocol does not provide a date-restricted listing endpoint. Any future live GET to `events/index.html` will, by construction, present `extract_index_units` with seal-breaching tokens and trip the same guard.
2. **Upstream of the in-window contract.** The breach occurs before any in-window key is returned; `verify_archive_layout`, `files_missing`, and `files_in_archive_not_planned` are never reached. The §6 caveat — which is the v0.2 design lock for the in-window substrate — cannot be exercised at all while the live path is in use, regardless of whether the in-window subset is in fact clean.
3. **The seal guard is doing its job.** `Protocol2023PlusBreach` is the protocol-correct response to a listing that contains 2023+ tokens. The fault is not in the guard; the fault is that the live listing no longer matches the pre-2023 protocol Lane 2 was designed for.

These three together imply: keeping the live archive as Lane 2's default substrate path means accepting that every future run will be RUN-HALTED-BOUNDARY at the same layer, on every invocation, until a code-level transform is added.

## 4. Frozen recognized universe decision

Lane 2's **default substrate path is the §10 frozen recognized-list capture**:

- Path: `results/lane2_gdelt1_turn_b_recognized_list_capture/20260521T124853Z/recognized_list.json` (tracked at `4015b97`).
- SHA-256: `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`.
- Sidecar: `recognized_list.sha256` verifies `OK` via `shasum -a 256 -c`.
- Captured payload (verified at §10.5 post-verify and §10.6 review): `schema_version=v0.1`, `single_get_confirmation=True`, `recognized_in_window_count=3647`, `len(recognized_in_window_units)=3647`, `l5_regex_matches_in_artifact_body=0`, `provenance.turn_b_outcome=L1`, `provenance.byte_capture_authorization_memo_commit=cfede1b`, `provenance.recognized_list_remediation_decision_commit=f10c1bc`.

Operational implications:

- The §10 capture is now framed as the **canonical recognized universe** for Lane 2, not as a one-off evidence artifact for H2.
- Lane 2's contract with the upstream becomes a **snapshot contract anchored to `20260521T124853Z`**, not a live-archive contract. Any future "what does the upstream advertise" question must be answered with reference to this snapshot, not by re-running a live GET.
- The §10 capture is byte-stable on disk (SHA-pinned, sidecar-verified, tracked at `4015b97`); the snapshot contract is auditable in the same way the F4 baseline is.

This decision does **not** retire the live-archive path entirely — it demotes it from default to backup. A future re-snapshot taken under a separate explicit authorization (mirroring the §10 capture chain) is permitted, but it would replace the snapshot anchor, not the contract type.

## 5. Treatment of the §6 caveat

The §6 caveat from `57f42cc` is **inherited verbatim** by v0.3:

> `'2013'` yearly identifier is dropped at universe-construction time; the four 2014 dailies (`2014-01-23`, `2014-01-24`, `2014-01-25`, `2014-03-19`) are recorded as known substrate gaps.

Under the frozen-recognized-universe path, the §6 caveat resolves arithmetically against the captured payload:

- `recognized_in_window_count = 3647` (from the §10 capture).
- `'2013'` excluded → `3647 − 1 = 3646` in-planned recognized identifiers.
- The four 2014 dailies are not present in the recognized universe; they are pre-registered as known substrate gaps, not treated as missing units pending a re-run.
- The effective run universe under v0.3 is therefore **3,646 units**, identical to the v0.2 §6-caveat universe.

The caveat must still be **pre-registered** in any future count-feasibility execution prompt before any guard flip, as v0.2 required. Memo-level pre-registration remains the chosen mechanism; a code-level deterministic transform is still a permitted future upgrade but is not selected here.

## 6. Treatment of H2

H2 — *"the upstream GDELT 1.0 index advertises a `'2013'` yearly aggregate"* — is **supported but not confirmed** and is **non-blocking** under v0.3.

- The Gate 4C re-review report at `3176652` (SHA-256 `992a395c4a23cbe6270e88b7352b1fe20b59e2eccc08d0864be59aad2d7a0de4`, verdict `RECOGNIZED-LIST-USABLE-WITH-CAVEAT`) supports H2 at the code/semantic level: `plan_gdelt1_files` (gated by `PRE_REGIME_YEARLY_THROUGH_YEAR=2005`) does not produce a yearly `'2013'`, while `parse_gdelt1_unit_key` accepts any 4-digit yearly token by shape — the recognized-list `extras=['2013']` is a planner/classifier definitional mismatch, not capture-artifact corruption.
- Direct live confirmation would require re-reading the live `events/index.html` and inspecting the parse of `'2013'` — under v0.3 this is not done, and the live-archive path is not the default mechanism for such checks.
- A future fresh §10-style capture, taken under a separate explicit authorization, could in principle either confirm or refute the persistence of `'2013'` in the live listing; v0.3 does not require this, and the question is non-blocking for Lane 2's downstream work.
- Lane 2 will not condition any downstream design decision on H2's resolution. The §6 caveat already binds the universe-construction behavior, and the caveat is itself indifferent to whether `'2013'` is or is not in the live listing on any given day.

## 7. What this memo does not authorize

- No count-feasibility execution (under any guard configuration).
- No guard flip of `REAL_RETRIEVAL_ENABLED` or `COUNT_FEASIBILITY_AUTHORIZED`.
- No source, test, or config edits in the repo.
- No live GET; no second GET; no capture wrapper invocation; no `capture_recognized_list_once`, `fetch_index_live_once`, or `fetch_archive_index_live_safe` call.
- No event-file download.
- No market data ingest, read, or join.
- No Step 2 lock or precursor drafting.
- No Gate 5 execution.
- No modification of the F4 baseline at `20260518T163302Z`.
- No modification of the §10 recognized-list capture or its sidecar.
- No staging, committing, editing, or deleting of the post-§10 diagnostic report (`docs/lane2_gdelt1_gate5_prerun_diagnostic_post10_report_v0.1.md`, untracked and commit-prohibited under §7.2 SPURIOUS-RECOGNIZED).
- No new authorization for the 2023+ pre-filter transform (see §9 below).
- No `python3` canonicalization change (see §9 below).

## 8. Candidate next downstream question

With the substrate path resolved, the next eligible question is **what kind of count-feasibility run, if any, is meaningful against the frozen recognized universe**. Sub-questions a future v0.3-successor memo might address:

- Is the count-feasibility design (Options A/B, 10-day clustering, F-class taxonomy) still well-defined when the recognized universe is a frozen snapshot rather than a live listing? Most of it ports across unchanged because the design has always been count-only and the planner is local; the layout check becomes a snapshot-vs-planner comparison rather than a live-vs-planner comparison.
- Does the snapshot-contract framing change the F4 taxonomy? Under v0.2's design, F4 was triggered by the live layout differing from the documented plan. Under the snapshot contract, the layout difference is already known and pre-registered via the §6 caveat — the layout-check would deterministically be either "matches caveat" or "differs beyond caveat," which is a binary that may not need the full F-class machinery.
- What event-file path is implied? The frozen recognized universe identifies *which* in-window units the upstream advertises, but actually fetching event files (per planned unit) would still require live GETs to per-file URLs, not to the listing. Those live GETs are out of scope of v0.3 and would need their own authorization.

These are framing questions for a successor memo, not authorizations.

## 9. Alternatives retained but not selected

- **Option A — 2023+ pre-filter transform**: a code-level transform that strips 2023+ tokens from the listing string before `extract_index_units` parses it, with auditable in-window byte-preservation, conformance tests, and its own Gate-4-style authorization memo. Retained as the **backup path if live-archive continuity ever becomes necessary** (e.g., Lane 2 outgrows the snapshot contract, or a successor research question requires a fresh listing on demand). Not selected under v0.3 because the snapshot contract is sufficient for current Lane 2 scope and is strictly lower-risk than introducing a new code transform on the live path.
- **Option B — accept that the live path is blocked, take no action**: rejected here only insofar as v0.3 *does* take action — it selects the frozen-snapshot contract. The "accept and do nothing" framing collapses into v0.3's default-substrate selection.
- **Option C — different upstream data source**: out of scope for v0.3; would require revisiting Lane 2's source-selection lineage (`8fef80d` and predecessors) and is not motivated by the v0.2 outcome.
- **`python3` canonicalization hygiene**: framed as **orthogonal hygiene, not strategic**. The Attempt 1 / Attempt 2 interpreter-substitution observation in the v0.2 post-run report is a small workflow concern (either pin `python3` in the runner's shebang, or normalize all execution prompts to specify `python3` explicitly). It can land at any time under a separate trivial authorization and has no bearing on the substrate-path decision recorded in §4.

## 10. Final posture

**`SELECT FROZEN RECOGNIZED UNIVERSE AS DEFAULT LANE 2 SUBSTRATE`**

- The §10 capture at `4015b97` (`recognized_list.json`, SHA-256 `84ea721e14bd0ac11ad60d7657143d38b3c2b0db0c26383abb0e38dafff835fc`) is the canonical recognized-universe anchor for all future Lane 2 work.
- The §6 caveat from `57f42cc` is inherited verbatim; the effective run universe under v0.3 is the 3,646 in-planned recognized identifiers (3,647 captured minus `'2013'`), with the four 2014 dailies pre-registered as known substrate gaps.
- H2 remains supported-but-not-confirmed and is non-blocking.
- The live-archive path is demoted from default to backup; Option A (2023+ pre-filter transform) is the retained fallback if live-archive continuity ever becomes necessary, under its own future authorization.
- No execution, no code change, no GET, no guard flip, no memory edit, no downstream design step is authorized by this memo.
- The next eligible workstream is the successor memo that defines what, if any, count-feasibility design is meaningful against the frozen recognized universe — separately initiated.

Until that successor memo and its eventual run-enablement memo close, the following remain blocked: Gate 5 execution, count-feasibility re-run, market data, Step 2, live GET, second GET, capture, F4 modification, guard flips, source/test/config edits, post-§10 diagnostic report staging/commit/edit/delete.
