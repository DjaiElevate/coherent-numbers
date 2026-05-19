# Lane 2 — GDELT1 Gate 4D: Live-Opener Implementation Authorization Memo (v0.1)

DRAFT FOR REVIEW. NOT COMMITTED. NOT IMPLEMENTED. NO NETWORK REQUEST AUTHORIZED BY THIS MEMO DRAFT.

Drafted 2026-05-19. Subordinate to `bf4ef79` §4, `159c392`, `54fb16a` §3/§4, `e572c76`, `f8345c8`, and the Turn A L0 finding.

---

## 1. Title

Gate 4D — Live-Opener Implementation Authorization Memo. Scope: authorize (later, separately initiated) the construction of a redirect-disabled HTTP opener and a minimal one-call driver into the existing `fetch_archive_index_live_safe`, plus tests proving redirects are not followed and a conformance review against the Gate 4C firewall. This memo closes the implementation-path gap identified by Turn A L0; it does **not** authorize any live GET.

## 2. Top-of-File Disclaimer

DRAFT FOR REVIEW. NOT COMMITTED. NOT IMPLEMENTED. NO NETWORK REQUEST AUTHORIZED BY THIS MEMO DRAFT.

This memo authorizes only a *later, separately initiated* implementation step. It performs no implementation, no network access, no GDELT contact, no count-feasibility run, no Gate 5 entry, no guard flip, no F4 modification, and no commit/push.

## 3. Current Canonical State

Verified read-only on 2026-05-19 before drafting:

- Repo: `/Users/jay/Documents/GitHub/coherent-numbers`; branch `main`.
- `HEAD` = `f8345c8a4382f67686211de0ae27f89e72988c7f`.
- `origin/main` = `f8345c8a4382f67686211de0ae27f89e72988c7f` (local = origin; in sync).
- Tracked-modification count = `0` (only untracked artifacts present, including this draft once written).
- `REAL_RETRIEVAL_ENABLED = False` — `src/lane2_gdelt1_count_feasibility.py:647`.
- `COUNT_FEASIBILITY_AUTHORIZED = False` — `scripts/run_lane2_gdelt1_count_feasibility.py:44`.
- F4 record `results/lane2_gdelt1_count_feasibility/20260518T163302Z/` exists with exactly the two original files (`count_feasibility_metadata.json`, `feasibility_summary.md`), mtime 2026-05-18 18:33 — canonical, consumed, untracked, untouched.
- Post-4C live-execution authorization memo (`f8345c8`, `docs/lane2_gdelt1_post4C_live_execution_authorization_memo_v0.1.md`) committed and pushed; decision **AUTHORIZE LATER EXECUTION** stands and is not invalidated.

## 4. Turn A L0 Finding

Turn A (read-only, 2026-05-19) classified the would-be live execution **L0 — execution preflight passed; implementation path not yet executable**. Preflight was green, but the existing Strategy II live-safe path is not mechanically executable as a single existing call:

- **Criterion 1 fail** — no script/command invokes `fetch_archive_index_live_safe` with a real opener.
- **Criterion 2 fail** — no single existing function call/command without new driver code.
- **Criterion 4 fail** — redirect-following is not disabled or verifiable in the existing real-network path; the only real opener (`scripts/run_lane2_gdelt1_count_feasibility.py` `_real_opener`, `urllib.request.urlopen`) follows redirects by default and is wired to the count-feasibility flow.
- **Criterion 7 fail** — firing the GET would require new opener/driver code, which Turn A held out of scope.

L0 is an **implementation-path gap, not canonical-state drift**. No live GET fired; no GDELT contact; no network request; no count-feasibility run; no Gate 5; no event-file request/download; F4 unmodified; guards not flipped; nothing staged/committed/pushed. Gate 4D exists to close exactly this gap, narrowly.

## 5. Decision: AUTHORIZE LATER IMPLEMENTATION / DEFER / FORBID

The three possible decisions:

- **AUTHORIZE LATER IMPLEMENTATION** — permit, in a *later separately initiated and separately reviewed* step, the narrow implementation in §6, under all §8–§12 constraints. No network, no live GET, no commit without later explicit approval.
- **DEFER** — decline to authorize now; require an additional precondition, clarification, or review before the implementation may be scoped. Appropriate only if a precondition were unclear, stale, or unverifiable.
- **FORBID** — rule that the live-opener/driver must not be built under the current Lane 2 GDELT1 protocol. Appropriate only if a protocol-level reason existed that this implementation should never occur.

### Decision: **AUTHORIZE LATER IMPLEMENTATION**

**Why this is appropriate.** The canonical state is fully verified and unambiguous (§3); the post-4C authorization (`f8345c8`) already decided AUTHORIZE LATER EXECUTION and explicitly contemplated a Strategy II live-safe single GET with redirect-following disabled. Turn A demonstrated the *only* obstacle is a missing redirect-disabled opener + one-call driver — a bounded, well-specified implementation that does not touch extraction/redaction, guards, or F4. DEFER is not warranted: no precondition is unclear, stale, or unverifiable. FORBID is not warranted: there is no protocol-level reason the redirect-disabled opener should never exist; the firewall design already anticipates it. AUTHORIZE LATER IMPLEMENTATION, bound by §6–§12, is therefore the correct and minimal decision. This memo does not itself implement anything.

## 6. Authorized Narrow Scope

Gate 4D authorizes a later implementation strictly limited to these four items and nothing else:

1. **Redirect-disabled opener** — a small HTTP opener that performs at most one request and does not follow HTTP redirects (no automatic `Location` follow).
2. **Minimal one-call driver** — a thin driver that injects the redirect-disabled opener into the existing `fetch_archive_index_live_safe` and makes exactly one call, returning/recording only the existing `LiveSafeExtraction` aggregate result form. No new extraction, no new redaction, no result-file creation.
3. **Tests proving redirects are not followed** — deterministic tests using fake openers / in-memory fixtures / local synthetic responses that assert a redirect response yields a controlled non-follow outcome (no second request, no `Location` fetch).
4. **Conformance review against Gate 4C** — a later Gate 4D conformance review verifying the no-surfacing / firewall guarantees of `54fb16a` §3/§4 and `e572c76` are preserved.

Anything outside these four items is out of scope for Gate 4D.

## 7. Explicit Non-Authorizations

Gate 4D does **NOT** authorize any of the following:

- live GET
- GDELT contact
- HEAD request
- curl/wget/manual browser request
- event-file request
- event-file download
- count-feasibility run
- market data
- Step 2
- Gate 5
- F4 modification
- guard flip (`REAL_RETRIEVAL_ENABLED` / `COUNT_FEASIBILITY_AUTHORIZED` stay `False`)
- source pivot
- extraction/redaction rewrite
- post-2022 filename surfacing
- commit without later explicit approval

## 8. Future Implementation Constraints

The later implementation step (separately initiated, separately reviewed) is bound to:

- **No network access during implementation.** No socket, no DNS, no HTTP, no GDELT contact at any point in implementation or its tests.
- **Tests use fake openers, in-memory fixtures, or local synthetic responses only.** No real GDELT traffic in tests.
- **No real post-2022 filename literals** in tests, stdout, logs, reports, markdown, JSON, exceptions, `.rejected_examples`, or persisted artifacts.
- Synthetic boundary fixtures explicitly inherited from Gate 4C may be referenced in tests **only**; what remains forbidden is the *unredacted appearance of real fetched post-2022 filenames* in stdout, logs, reports, markdown, JSON, exceptions, `.rejected_examples`, or persisted artifacts.
- The **canonical 9-channel no-surfacing list from `54fb16a` §3** remains authoritative (enumerated in §12).
- **No changes to existing extraction/redaction behavior** unless explicitly justified and separately reviewed.
- Do **not** weaken or bypass: `extract_index_units`, `extract_index_units_live_safe`, `fetch_archive_index_live_safe`, `LiveSafeExtraction`.
- **Redirect-disabled behavior must be enforced by construction**, not by a fragile runtime convention (see §9).
- **Redirect attempts must produce a controlled failure/outcome, not an automatic follow.**
- The one-call driver must **not** create result files, JSON, markdown, or logs during implementation tests.
- **Runner guards must remain inert** unless a later memo explicitly authorizes otherwise.

## 9. Redirect-Disabled Opener Requirements

- The opener must disable redirect-following **by construction** — e.g., a URL-opener built with a redirect handler whose redirect methods do not follow (raise/return a controlled non-follow), so that "no redirect follow" is a structural property of the object, not an after-the-fact check or a convention a caller could forget.
- On encountering a 3xx / `Location` response, the opener must surface a **controlled, classifiable outcome** (mapping to the post-4C memo's L4 "request fired; transport/substrate failure / redirected" class) and must **not** issue any follow-up request, must **not** fetch the `Location` target, and must **not** fall back to the base `/events/` or any other URL.
- Exactly one request per invocation. No retry. No second GET. No fallback URL.
- The opener constructs no hidden default network client beyond the single explicit request it is asked to perform, and is itself only ever exercised in tests via fakes/fixtures during Gate 4D implementation (no real network).
- The opener does not parse, extract, redact, or persist anything; it returns a response object consumed by the existing live-safe path only.

## 10. Minimal One-Call Driver Requirements

- A thin driver that: builds/accepts the redirect-disabled opener, injects it into `fetch_archive_index_live_safe` (default `index_url = http://data.gdeltproject.org/events/index.html`, the existing `DEFAULT_GDELT1_INDEX_URL`), performs exactly one call, and returns/records only the existing `LiveSafeExtraction` aggregate form.
- The driver must **not**: modify or replace `extract_index_units_live_safe` / `fetch_archive_index_live_safe` / `LiveSafeExtraction`; call the base `/events/` URL; request any event-file URL; perform any fallback; flip any guard; create result files / JSON / markdown / logs during implementation tests; trigger any count-feasibility run; enter Gate 5.
- The driver itself does not fire a live request during Gate 4D implementation — it is exercised only with fake openers / synthetic responses. A real live GET remains gated behind the separately-blocked live-execution step (§16).
- The driver carries forward, unchanged, the post-4C single-GET / no-retry / no-fallback / no-event-file / no-redirect-follow constraints so that a future Turn B can use it without re-deriving them.

## 11. Test Requirements

- All tests run with **no network access**; use fake openers, in-memory fixtures, or local synthetic responses only.
- **Redirect-not-followed evidence:** at least one test feeds a synthetic 3xx/`Location` response and asserts (a) no second request is made, (b) the `Location` target is not fetched, (c) the outcome is the controlled non-follow class, (d) no base `/events/` fallback occurs.
- **Single-call evidence:** a test asserts exactly one opener invocation per driver call (no retry, no second GET).
- **Firewall preservation:** existing Gate 4C extraction/redaction tests (e.g. the `test_gate4c_*` suite, including the no-network and fake-opener live-safe tests) must continue to pass unchanged.
- **No-surfacing evidence:** tests assert no real post-2022 filename appears in any of the 9 channels (§12); only aggregate counts / non-identifying form-class labels appear. Synthetic Gate 4C boundary fixtures may be referenced by constant/test name only.
- **No-artifact evidence:** tests assert the driver creates no result files / JSON / markdown / logs.
- Tests must be deterministic and hermetic (no reliance on external hosts, time, or network).

## 12. Gate 4C Firewall / No-Surfacing Preservation

The canonical 9-channel no-surfacing list from `54fb16a` §3 remains authoritative. No real post-2022 filename may appear in:

1. exception messages
2. `.rejected_examples`
3. logs
4. JSON
5. markdown
6. stdout
7. tests
8. reports
9. any persisted artifact

`54fb16a` §4 (design-spec vs observable-test layering) and the Gate 4C conformance PASS (`e572c76`, T1/T2 non-disguise) remain binding. The Gate 4D opener/driver is layered *around* the existing live-safe path and must not alter its redaction/aggregation semantics; only aggregate post-2022 counts and non-identifying form-class labels may ever be emitted.

## 13. Binding Citation Anchors

The later implementation, its tests, and its conformance review must cite and remain subordinate to:

1. **This Gate 4D memo (v0.1)** — narrow live-opener/driver authorization; defines scope and constraints.
2. **`bf4ef79` §4** — Gate 4 live body-access firewall rule; binding on any live body-access path.
3. **`159c392`** — Gate 4B Strategy II decision (CONDITIONALLY ALLOW after Gate 4C closed, FORBID fallback).
4. **`54fb16a` §3/§4** — canonical 9-channel no-surfacing list and design-vs-observable-test layering.
5. **`e572c76`** — Gate 4C conformance PASS (firewall proven non-disguising via T1/T2).
6. **`f8345c8`** — post-4C live-execution authorization memo (AUTHORIZE LATER EXECUTION; single GET / no retry / no fallback / no redirect-follow; L0–L5 classes).
7. **Turn A L0 finding** — execution preflight passed; implementation path not yet executable; Gate 4D is the narrow remediation.

## 14. Future Implementation-Report Requirements

A future (uncommitted) Gate 4D implementation report must include:

- exact files changed
- summary of code changes
- confirmation no network / GDELT contact occurred
- confirmation no live GET occurred
- confirmation no event-file request/download occurred
- confirmation F4 untouched
- confirmation guards inert (`REAL_RETRIEVAL_ENABLED=False`, `COUNT_FEASIBILITY_AUTHORIZED=False`)
- test command(s) run
- test results
- redirect-not-followed test evidence
- confirmation existing Gate 4C firewall tests still pass
- confirmation no real post-2022 filename surfaced (any of the 9 channels)
- confirmation no staging/commit/push occurred unless separately authorized
- binding citation anchors carried forward (§13)

## 15. Conformance-Review Requirements

A later Gate 4D conformance review must verify:

- only the authorized opener/driver/test files changed
- no network request occurred during implementation
- no GDELT contact occurred during implementation
- no F4 files were touched
- guards remained inert
- existing Gate 4C extraction/redaction tests still pass
- new redirect tests prove redirects are not followed
- no new surfacing channel for real post-2022 filenames was introduced
- the live-safe firewall cannot be bypassed by the new driver
- no event-file URL is requested
- no base `/events/` fallback is introduced
- no source pivot is introduced
- no count-feasibility run is triggered
- no Gate 5 is entered

## 16. What Remains Blocked After This Memo

Even if this memo is approved and committed:

- **No live GET** is authorized. The separately initiated live execution remains **BLOCKED** until Gate 4D is implemented *and* conformance-reviewed clean *and* a separate explicit live-execution approval step is given.
- Runner guards stay inert (`REAL_RETRIEVAL_ENABLED=False`, `COUNT_FEASIBILITY_AUTHORIZED=False`).
- No Gate 5, no count-feasibility run, no market data, no Step 2, no source pivot.
- F4 stays canonical/consumed/untracked/untouched.
- Implementation itself is a *later separately initiated* step; this memo does not perform it and grants no commit/push.
- Sequence ahead: Gate 4D approve → (later) Gate 4D implementation → Gate 4D conformance review PASS → (then, separately) post-4C Turn B live-execution approval → only then a single live GET.

## 17. Final Verdict

**AUTHORIZE LATER IMPLEMENTATION** of the narrow Gate 4D scope (§6) — redirect-disabled opener, minimal one-call driver into `fetch_archive_index_live_safe`, redirect-not-followed tests, and a Gate 4C-firewall conformance review — bound by §7 non-authorizations, §8 implementation constraints, §9–§11 opener/driver/test requirements, §12 firewall preservation, §13 anchors, §14–§15 report/review requirements, and §16 blocked items. Contingent on (a) this memo being committed and (b) a separate explicit go-ahead to begin implementation. This memo does not implement code, performs no network request, flips no guard, touches no F4, and grants no commit/push.

*End of draft v0.1. Not committed. Not implemented. No network request authorized by this memo draft.*
