# Lane 2 — GDELT1 Post-4C Live-Execution Authorization Memo (v0.1)

**Status:** DRAFT FOR REVIEW. NOT COMMITTED. NOT EXECUTED.
**Scope:** Authorization decision only — whether a single live GET of the GDELT1 index body may be authorized *in a later, separately initiated step*, after Gate 4C closed at `e572c76`.
**This memo does not execute the GET, does not contact GDELT, does not perform retrieval, does not run count-feasibility, does not draft Gate 5, and does not touch market data.**
**This memo does not flip `REAL_RETRIEVAL_ENABLED` or `COUNT_FEASIBILITY_AUTHORIZED` and does not create a run-enablement commit.**

Drafted 2026-05-19. Subordinate to `bf4ef79` §4, `159c392`, `54fb16a` (§3/§4/§5), `e572c76`.

---

## 1. Preflight Provenance Result

Verified locally on 2026-05-19 before drafting:

- `pwd` = `/Users/jay/Documents/GitHub/coherent-numbers`
- `git rev-parse --show-toplevel` = `/Users/jay/Documents/GitHub/coherent-numbers`
- `git branch --show-current` = `main`
- `git log -1 --oneline` = `e572c76 Record Lane 2 GDELT1 Gate 4C conformance review`
- `git status --short` = only untracked, non-Lane-2-state artifacts (paper build outputs, an unrelated design memo draft, and the canonical untracked F4 results directory `results/lane2_gdelt1_count_feasibility/`); **no tracked modifications**
- local `main` = `e572c769f579b693a8a105682250cc8e1107af2f`
- `origin/main` = `e572c769f579b693a8a105682250cc8e1107af2f`
- **HEAD == origin/main: YES** (iMac clone aligned with origin and MacBook clone; prior cross-clone "phantom" divergence reconciled via push `5745722..e572c76`, 35 commits, + ff-merge)

Commit existence (all present, subjects match expected roles):

| Commit | Role |
|---|---|
| `60ec152` | GDELT1 count-feasibility run authorization |
| `fe74255` | Enable Lane 2 GDELT1 count-feasibility run (consumed/spent) |
| `9e329c2` | Restore count-feasibility runner to inert state after F4 run |
| `38011be` | Phase A diagnostic report → D0 |
| `10b80c7` | Phase B Substep 1 doc-fetch report → D2 ruled out |
| `9a8fb7b` | Phase B Substep 2A HEAD probe report → D1-supported |
| `12ae078` | Discovery-defect remediation design memo (Gate 0) |
| `be2a7df` | Remediation-patch authorization memo (Gate 1) |
| `6834814` | Offline parser remediation (Gate 2) |
| `f564b77` | Gate 3 remediation conformance review PASS |
| `bf4ef79` | Gate 4 body-access firewall decision memo |
| `befbb94` | Gate 4A R1 offline patch implementation |
| `bced9e1` | Gate 4A R1 conformance review |
| `159c392` | Gate 4B body-access decision memo |
| `54fb16a` | Gate 4C firewall/redaction authorization memo |
| `ec1c3ec` | Gate 4C firewall/redaction implementation |
| `e572c76` | Gate 4C conformance review PASS (= HEAD = origin/main) |

**Result: PASS.** Local `main`, `origin/main`, and the verified commit chain fully support the canonical state in §2. No mismatch, no staleness, no unverifiable precondition. Drafting proceeds.

---

## 2. Canonical State

- Count-feasibility run authorization committed at `60ec152`.
- The original count-only run under `fe74255` is **consumed and closed F4-missing**: 3,650 planned units, **0 parseable available units**, no downloads, no counts, no market data, no 2023+, no Step 2. Consumed F4 record at `results/lane2_gdelt1_count_feasibility/20260518T163302Z/` is canonical, untracked, and non-overwritten.
- Runner restored **inert** at `9e329c2` (`COUNT_FEASIBILITY_AUTHORIZED = False`).
- Phase A **D0** committed at `38011be`.
- Substep 1 **D2 ruled out** at `10b80c7`.
- Substep 2A **D1-supported** committed at `9a8fb7b`.
- Gate 0 design memo committed at `12ae078`.
- Gate 1 remediation authorization committed at `be2a7df`.
- Gate 2 offline parser remediation committed at `6834814`.
- Gate 3 conformance **PASS** committed at `f564b77`.
- Gate 4 decision memo committed at `bf4ef79`.
- Gate 4A R1 implementation and conformance closed at `befbb94` / `bced9e1`.
- Gate 4B body-access decision memo committed at `159c392` (chose **Strategy II** = CONDITIONALLY ALLOW after Gate 4C closed, FORBID fallback).
- Gate 4C authorization, implementation, and conformance closed at `54fb16a` / `ec1c3ec` / `e572c76`.
- Gate 4C added `LiveSafeExtraction`, `extract_index_units_live_safe`, and `fetch_archive_index_live_safe`.
- Gate 4C conformance **PASS** recorded (no required fixes; Strategy II non-disguise proved via T1/T2).
- **No live GET has been authorized or executed.**
- **Gate 5 has not been drafted.**

All Gate 4C preconditions for considering a live body read are therefore satisfied and committed: the firewall rule is binding (`bf4ef79` §4), Strategy II is chosen (`159c392`), the redaction blocking-precondition is authorized (`54fb16a`) and implemented (`ec1c3ec`) and conformance-passed (`e572c76`).

---

## 3. Memo Question and Decision

**Question:** Should the project authorize, in a later separately initiated step, **exactly one** live GET of

`http://data.gdeltproject.org/events/index.html`

using the Gate 4C Strategy II live-safe path (`fetch_archive_index_live_safe` → `extract_index_units_live_safe` → `LiveSafeExtraction`)?

### Decision: **AUTHORIZE LATER EXECUTION**

Conditionally authorize **exactly one** live GET, **but only after** (a) this memo is committed, and (b) a separate, explicit go-ahead is given in a later separately initiated step.

**Rationale.** Every committed precondition is satisfied and independently verified (§1, §2). The redaction firewall — the explicit blocking precondition stated in `bf4ef79` and Gate 4B `159c392` — is closed: authorized (`54fb16a`), implemented (`ec1c3ec`), conformance-PASS (`e572c76`). The Substep 2A HEAD probe (`9a8fb7b`) already established the documented target exists at `200 OK`, `Content-Length 556438`, `Content-Type: text/html`, **no redirect**, so a single live GET is a bounded, well-characterized transport action with a known-good baseline. No protocol-level reason exists to FORBID under the current Lane 2 GDELT1 design: the design explicitly contemplates a Strategy II conditional-allow path post-4C. DEFER is not warranted because no precondition is unclear, stale, or unverifiable. AUTHORIZE LATER EXECUTION is therefore the correct decision, with the binding constraints in §3.1.

### 3.1 Binding constraints on the future execution

If and when later separately initiated, the authorized execution is bound to **all** of the following. Violation of any one is an L5 protocol breach:

- exactly **one** GET request;
- **no** retry;
- **no** second GET;
- **no** fallback URL;
- **no** event-file request;
- **no** event-file download;
- **no** count-only feasibility run;
- **no** Gate 5;
- **no** market data;
- **no** Step 2;
- **no** source pivot;
- **no** modification of the consumed F4 outputs.

### 3.2 What this decision is NOT

This decision does **not** execute the GET, does **not** flip any runner guard, does **not** create a run-enablement commit, and does **not** authorize any action outside this memo's text. Any future execution requires a separate, explicitly initiated, separately reviewed (and if applicable committed) run-enablement step.

---

## 4. Target and Redirect Policy

- **Target URL must be exactly:** `http://data.gdeltproject.org/events/index.html`
- Automatic redirect-following is **disabled**. This memo does **not** decide otherwise.
- If a redirect occurs at execution time and redirect-following is not authorized, execution **must stop and report unresolved** (outcome class **L4**, see §8) — it must not be treated as permission to follow.
- **No** automatic follow-up to a `Location` header.
- **No** fallback to `.../events/` or any other URL.

**Empirical baseline.** Substep 2A (`9a8fb7b`) HEAD probe returned `200 OK` for the exact target, `Content-Length = 556438`, `Content-Type: text/html`, and **no redirect**. The documented target was already observed to exist without redirect under HEAD. This baseline supports the no-redirect-following policy but does **not** relax it: any execution-time redirect remains a distinct outcome class (L4), never implicit permission to follow.

---

## 5. Runner Guard Preservation

Both runner guards remain **inert** after this memo is drafted and, if later committed:

- `REAL_RETRIEVAL_ENABLED = False`
- `COUNT_FEASIBILITY_AUTHORIZED = False`

This memo authorizes a future single GET **only as a later, separately initiated step**. It does **not** flip these flags, does **not** create a run-enablement commit, and does **not** permit any guard flip in the current turn or by virtue of being committed. Any future execution/run-enablement step must be separately drafted, reviewed, committed if applicable, and explicitly initiated. The single authorized live GET, when later enabled, runs via the Gate 4C live-safe path and is not a count-feasibility run; `COUNT_FEASIBILITY_AUTHORIZED` stays `False` throughout.

---

## 6. Firewall Execution Requirements

- Use the **Gate 4C live-safe Strategy II path only**: `fetch_archive_index_live_safe` → `extract_index_units_live_safe` → `LiveSafeExtraction`. Gate 2 `extract_index_units` remains unmodified and is not used for the live path.
- Real **post-2022** filenames may **not** appear in any of:
  1. exception messages
  2. `.rejected_examples`
  3. logs
  4. JSON
  5. markdown
  6. stdout
  7. tests
  8. reports
  9. any persisted artifact
- Exact real post-2022 filenames are **forbidden everywhere**.
- Only **aggregate** post-2022 counts and **non-identifying** classes may be emitted.
- Pre-2023 recognized filenames may be retained **only** if they fall within the authorized window **2005-01-01 through 2022-12-31**.
  - `20221231.export.CSV.zip` is **in-window** (retainable).
  - `20230101.export.CSV.zip` is **post-2022** and must be **redacted/aggregated**.
- The execution report must **not** print or store any exact post-2022 filename.
- The execution report must preserve the consumed F4 run as **canonical and non-overwritten**.

These requirements are inherited verbatim in force from `54fb16a` §3 (canonical 9-channel no-surfacing list), §4 (design-spec vs observable-test layering), and §5, and were proved non-disguising at Gate 4C conformance (`e572c76`, T1/T2).

---

## 7. Memo Inheritance and Binding Citations

This memo inherits and remains **subordinate to**:

- `bf4ef79` **§4** — the binding firewall rule for any future live body-access patch.
- `159c392` — Gate 4B Strategy II decision.
- `54fb16a` — Gate 4C firewall/redaction authorization, especially **§3 / §4 / §5**.
- `e572c76` — Gate 4C conformance PASS.

Any future execution report produced under this memo's authorization **must explicitly cite all five anchors**:

1. This post-4C live-execution authorization memo (v0.1).
2. `bf4ef79` §4.
3. `159c392` — Gate 4B Strategy II decision.
4. `54fb16a` — Gate 4C firewall/redaction authorization.
5. `e572c76` — Gate 4C conformance PASS.

A future execution report missing any of the five anchors is non-conformant.

---

## 8. One-GET Outcome Classes (L0–L5)

The later execution, if authorized, terminates in exactly one of:

- **L0 — Preflight held back; request never fired.** Execution did not occur because a preflight guard, precondition, or authorization check failed *before any request was made*. Protocol held back correctly; **zero transport activity**.
- **L1 — Live index retrieved; usable pre-2023 units found.** At least one valid 2005–2022 unit discovered, with **zero** post-2022 leakage.
- **L2 — Live index retrieved; no usable pre-2023 units.** Zero valid 2005–2022 units discovered, with **zero** post-2022 leakage.
- **L3 — Live index retrieved; only aggregate post-2022 presence.** Only aggregate post-2022 presence/counts detected before any usable pre-2023 recovery; reported as aggregate/non-identifying only.
- **L4 — Request fired; transport/substrate failure.** The authorized request was made but live access failed, was blocked, was redirected, was ambiguous, or was otherwise unusable as a substrate/transport outcome. **Distinct from L0: the request fired; the substrate or transport did not deliver as expected.**
- **L5 — Protocol breach / firewall breach; HALT.** Any violation of §3.1 constraints or §6 firewall requirements (including any exact post-2022 filename surfacing, any retry, any second GET, any fallback, any redirect-follow, any guard flip, any F4 modification). Immediate halt; human review.

Invariants preserved across any refinement of these classes:

- **no retry**;
- **no exact post-2022 filename surfacing**;
- **no automatic Gate 5**;
- **sharp L0 / L4 distinction** — L0 = preflight held back, request never fired; L4 = request fired, transport/substrate failure. These two are never conflated.

---

## 9. Required Future Execution Report Fields

If later authorized and executed, the (uncommitted) execution report must contain:

- HTTP status / high-level transport result;
- whether body access occurred;
- whether a redirect occurred;
- number of recognized in-window 2005–2022 units;
- aggregate count of post-2022 tokens, **without filenames**;
- aggregate count of unrecognized/malformed tokens;
- confirmation that **no exact post-2022 filename** surfaced in any of the 9 forbidden channels (§6);
- confirmation that **no event files** were requested or downloaded;
- confirmation that **no count-only feasibility run** occurred;
- confirmation that **no market data, Step 2, or Gate 5** action occurred;
- confirmation that the consumed **F4 outputs remain canonical and untouched**;
- the assigned outcome class **L0–L5**;
- explicit citation of **all five binding anchors** per §7.

---

## 10. Strict Non-Execution Statement

This memo:

- **does not execute the GET** (no GET, no HEAD, no body inspection, no GDELT contact, no documentation fetch);
- **does not flip** `REAL_RETRIEVAL_ENABLED` or `COUNT_FEASIBILITY_AUTHORIZED`;
- **does not create** a run-enablement commit;
- **does not draft Gate 5**, Step 2, or any source pivot;
- **does not modify** the consumed F4 outputs;
- **does not authorize** any action outside this memo's text.

It authorizes a later single live GET **only if** this memo is committed **and** a separate, explicit go-ahead is given in a later separately initiated step. Any such future step must be independently drafted, reviewed, committed if applicable, and explicitly initiated.

---

## 11. Final Recommendation

**AUTHORIZE LATER EXECUTION** of exactly one live GET of `http://data.gdeltproject.org/events/index.html` via the Gate 4C Strategy II live-safe path, bound by §3.1 constraints, §4 redirect policy, §5 guard preservation, §6 firewall requirements, §7 binding citations, and §8 outcome classes — contingent on (a) this memo being committed and (b) a separate explicit go-ahead in a later separately initiated step. No execution, no guard flip, no run-enablement, and no Gate 5 in this turn.

*End of draft v0.1. Not committed. Not executed.*
