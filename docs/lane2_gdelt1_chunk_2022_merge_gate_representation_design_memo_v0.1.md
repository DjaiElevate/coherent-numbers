# Lane 2 GDELT1 chunk_2022 — Merge-Gate Definition and Representation Design Memo v0.1

> **Design / decision memo only.** Defines the merge-gate consequence of the represent-only decision for `2022-11-10` and the disclosure machinery. It does **not** merge, execute chunk_2022, modify runner code, run BigQuery, amend any constant, update memory, or open Step 2.

---

## 1. Purpose

- Define the merge-gate consequence of the **represent-only** decision for `2022-11-10`.
- Decide whether **labeled completion** is admissible or whether **strict raw-purity** blocks the merge gate.
- Define machine-readable and human-readable disclosure requirements for the selected outcome.
- Do **not** merge, execute chunk_2022, modify runner code, update memory, or open Step 2.

## 2. Baseline

- HEAD/origin baseline `36202b955ac5e467aaf8afbddab386d89627b30b`.
- chunk_2022 = **313/365 raw-runner processed before halt**; target year has **365** expected calendar days.
- represent-only decision selected in the prior implementation design memo (`36202b9`).
- substrate progress remains **9/10** before this memo; on-disk Path (b) remains **93**; user-side counter **retired**.
- carry-forward ordinal **before** this memo report = **104**.

## 3. Evidence summary

- Original chunk_2022 halt: 313/365, `20221110.export.CSV.zip`, `FetchFailure` / HTTP 404; guard restored; sanctioned commits enable `322e34c339f5596aef677e8f5225ec6a3b09bcc8` / restore `b10bd04b86cad484eb04d5ea9e3b6e7bc82dbd8d`.
- Data-bearing status confirmed: catalog lists the file (md5 `91e15516016f986e5b8a08712e1de95a`, size `6,714,105`); user-run BigQuery `gdelt-bq.full.events` counts `20221109 = 117,008`, `20221110 = 105,041`, `20221111 = 40,588`.
- Raw object unavailable across four probes (HEAD 404, range 416/404); no official md5-compatible alternate raw object; GDELT 2.0 correctly rejected (different dataset; `20221110` was a timestamp-substring false match); path C ruled out.
- Represent-only selected; `KNOWN_SUBSTRATE_GAPS` amendment rejected; no semantic recovery artifact produced.

## 4. Decision question

Does a represent-only, data-confirmed-but-raw-object-unavailable day **satisfy the Lane 2 full-build merge gate** if explicitly labeled and carried through all artifacts? Or does the merge gate require **strict raw-object completion of every expected day**, such that chunk_2022 remains incomplete until self-heal?

## 5. Candidate gate definitions

**A. Labeled completion / documented-exception gate** — chunk_2022 becomes merge-eligible as `364 raw days + 1 documented official-data-confirmed raw-object-unavailable day`; **not** a raw 365/365; the merge label discloses the documented exception; merge artifacts include a raw-vs-documented cross-chunk table; Step 2 must carry the documented status and cannot silently treat the day as raw-processed. Preserves raw purity for the counted raw days while allowing build closure with an explicit exception.

**B. Strict raw-purity block** — the merge gate requires raw-object-processed completion for every expected day; chunk_2022 remains incomplete until `20221110.export.CSV.zip` self-heals or a true md5-compatible official raw object appears; no labeled completion, no merge eligibility. Avoids redefining the gate but may block indefinitely despite official data-bearing evidence.

## 6. Required selection

**`SELECTED — LABELED COMPLETION / DOCUMENTED EXCEPTION GATE`.**

Justification (from merge-gate semantics, §7): the merge gate exists to certify that the substrate has been **built to the project's standard and that the terminal status of every expected day is known and truthfully recorded** — not narrowly that every day is raw-processed regardless of external reality. For `2022-11-10` the terminal status is fully known: official data exists (BigQuery 105,041; catalog md5/size), the raw object is unavailable due to an **external upstream object-availability fault** outside the project's control, no md5-compatible alternate exists, and no substitute was fabricated. A gate that admits this **single, explicitly-labeled, fully-disclosed, non-recoverable-as-raw** day — with airtight machinery preventing any silent promotion to raw — certifies the substrate more honestly than either fabricating a substitute or stalling the entire program indefinitely on an external fault. Self-heal remains a free fallback (§13) that would later restore true raw 365/365, so labeled completion is an honest, reversible interim terminal state, not a permanent compromise.

**Why not Strict raw-purity block:** it would hold the entire program hostage **indefinitely** to a third party's object-store repair that may never occur, for **one** confirmed-data-bearing day among ~3,650 — disproportionate, and it yields no additional scientific integrity over labeled completion since labeled completion never overclaims (it explicitly is not "raw 365/365," not "recovered," not "no-data gap"). Strict-block is preserved only as the posture that would apply if disclosure machinery could not be guaranteed — which it can (§9–§12). (Strict-block also remains the *automatic* state until the labeled-completion machinery of §9–§11 is actually implemented and conformance-verified in a future authorized turn; this memo selects the target gate, it does not declare chunk_2022 complete.)

## 7. Evidentiary burden for gate selection

Labeled completion is **not** selected for operational convenience; strict-block is **not** rejected merely for being stricter. The decision rests on what "merge-eligible / complete" *means*:

- **Labeled-completion burden (met):** a documented, data-confirmed, raw-object-unavailable day can satisfy the gate **without** corrupting raw-substrate claims **iff** (a) it is never counted as a raw day, (b) the disclosure label propagates to every artifact and aggregate, (c) downstream/Step 2 is firewalled and must inherit/inspect the label, and (d) the forbidden claims (§12) are enforced. §8–§12 define exactly this machinery, so the burden is met. What is claimed: "raw substrate complete with one documented upstream-object-unavailable, data-confirmed, represented-only exception." What is **not** claimed: raw 365/365, recovery, or a no-data gap.
- **Strict-block burden (not met for permanence):** it would need to justify why confirmed official data-bearing evidence **plus** explicit, machine-enforced representation are insufficient for merge eligibility. The only thing strict-block buys over labeled completion is the literal "every day raw-processed" phrasing — which labeled completion never falsely claims anyway — at the cost of an indefinite external-fault stall. Future evidence that would unblock strict-block: canonical self-heal or a true md5-compatible official raw object.

The selected outcome follows from merge-gate semantics, not convenience.

## 8. Expected-file-count semantics

Under the selected **labeled completion** gate, chunk_2022 must be represented with **distinct fields**, never a bare raw ratio:

- `expected_calendar_days = 365`
- `raw_processed_days = 364`
- `documented_unavailable_data_confirmed_days = 1` (`2022-11-10`)
- `recovered_days = 0`
- `known_no_data_gap_days = 0` (for chunk_2022; the four 2014 `KNOWN_SUBSTRATE_GAPS` dates are out of the 2022 range and unrelated)
- `merge_gate_status = labeled_complete`

**Explicitly forbidden phrasings** for chunk_2022: raw `365/365`; "ordinary completion"; "no caveat"; "gap day"; "no-data day". (Permitted phrasing example: `365 expected = 364 raw_processed + 1 documented_unavailable_data_confirmed`.)

(For the record, the rejected strict-block representation would have been: `expected_raw_days = 365`, `raw_processed_days = 364`, `documented_unavailable_data_confirmed_days = 1`, `merge_gate_status = blocked_pending_raw_object`.)

## 9. Machine-readable disclosure label

Mandatory machine-readable label string:

```
UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY
```

Requirements:
- **Where it must appear:** the chunk_2022 representation artifact (§10); the cross-chunk disclosure table (§11) row for chunk_2022; the chunk_2022 `chunk_metadata.json` / `chunk_summary.md` if/when a future completion artifact is produced; and any merge manifest.
- **How it must propagate:** it must travel with chunk_2022 into the merge artifact and **must not be erased, collapsed, or summarized away** in any aggregate or roll-up.
- **Step 2 obligation:** Step 2 (and any downstream consumer) must inspect or inherit this label **before** any downstream analysis and must not begin until it has demonstrably done so.
- It is keyed to the single date `2022-11-10`; it must never be applied to any other date and must never substitute for a real raw day elsewhere.

(The rejected strict-block label would have been `MERGE_BLOCKED_RAW_OBJECT_UNAVAILABLE_DATA_CONFIRMED`.)

## 10. Required representation artifact

A future (separately-authorized) **representation artifact** is required, containing at minimum:
- date `2022-11-10`; raw filename `20221110.export.CSV.zip`;
- catalog md5 `91e15516016f986e5b8a08712e1de95a`; catalog size `6,714,105`;
- BigQuery evidence counts (`20221109 = 117,008`, `20221110 = 105,041`, `20221111 = 40,588`) with the user-run query provenance;
- raw-object probe history (HEAD 404 / range 416–404 across four probes; HTTPS env-TLS note; alternate-object and GDELT-2.0-rejection findings);
- status label `UPSTREAM_OBJECT_UNAVAILABLE_DATA_CONFIRMED_REPRESENTED_ONLY`;
- explicit statements: **no rows were recovered**, **no raw object was parsed**, **`KNOWN_SUBSTRATE_GAPS` was not amended**;
- hashes/manifests for the representation artifact itself.

This artifact is **designed, not created** here; its implementation is a separately-authorized future turn.

## 11. Cross-chunk disclosure table

The future merge / pre-merge artifact must include a cross-chunk table with at least: `chunk_id`, `expected_calendar_days`, `raw_processed_days`, `documented_unavailable_data_confirmed_days`, `recovered_days`, `known_no_data_gap_days`, `merge_gate_status`, `status_label`, `artifact_references`. It must make visible that chunks **2013(partial)–2021 are raw-complete under their respective definitions** while **chunk_2022 carries one documented data-confirmed raw-object-unavailable day**. (Note: chunk_2013 is partial by its own prior definition; chunk_2014 expected 361 due to the four 2014 `KNOWN_SUBSTRATE_GAPS`; these are distinct from the 2022 documented-exception and must be shown distinctly.)

## 12. Step 2 firewall / downstream-claim boundary

**Allowed downstream claims:** "Lane 2 GDELT1 raw substrate is complete with one documented upstream-object-unavailable, data-confirmed exception (`2022-11-10`)"; "`2022-11-10` was not raw-processed and was not recovered"; "the merge carries a documented exception label."

**Forbidden:** "raw 365/365"; "all days raw-processed"; "`2022-11-10` was a no-data gap"; "`2022-11-10` was recovered"; hiding the exception in aggregate-only artifacts; Step 2 treating the day as ordinary raw substrate. **Step 2 / market data / instrument construction remain firewalled** and must explicitly carry/inherit the §9 label before consuming chunk_2022; no silent promotion of the represented day to raw status.

## 13. Self-heal fallback

If the canonical raw object becomes available before a merge-gate representation artifact is finalized, the **normal raw-object processing path is preferred**. Self-heal supersedes represent-only status for this date **only after a separately-authorized fresh execution** (all three production locks; no reuse of the halted directory), which would restore true raw 365/365 and retire the §9 label for `2022-11-10`.

## 14. Future implementation requirements

Under the selected **labeled completion** outcome, the next required steps (separately authorized) are: a **representation artifact design/implementation** (the §10 artifact); **machine-readable label implementation** (§9); **cross-chunk disclosure-table generation** (§11); **pre-merge conformance checks** verifying label presence/propagation and forbidden-phrasing absence; and **no Step 2 until label propagation is verified**. No merge until the representation artifact + cross-chunk table + conformance checks are committed and pass. No live run, no Step 2, no market data in those steps either, beyond what each is scoped for.

## 15. Counter discipline

- On-disk **Path (b) remains 93** in this non-memory turn; user-side counter retired and not used.
- Carry-forward ordinal through the prior implementation design memo = **104**.
- This memo report should be treated as carry-forward ordinal **105** if completed.
- The eventual memory-write boundary must reconcile the larger jump from 93 — expected, not a discrepancy.

## 16. Boundaries preserved

No runner execution; no retry; no resume; no source edit; no constants amended; no memory update; no merge; no Step 2; no market data; no instrument construction; no archive; no payload download; no row export; no recovery implementation; no network probes; no BigQuery run this turn.

## 17. Next frontier

Per the selected **labeled completion** outcome: a **separately-authorized representation-artifact + pre-merge disclosure implementation** (§10–§11, §14) — building the `2022-11-10` representation artifact, the machine-readable label propagation, the cross-chunk disclosure table, and pre-merge conformance checks — followed (only after those pass and are committed) by a separately-authorized merge step that carries the documented-exception label. Self-heal remains a free fallback (§13). Never an immediate rerun; never a `KNOWN_SUBSTRATE_GAPS` amendment under current evidence; never a merge in this turn. chunk_2022 is **not** declared complete by this memo — it defines the gate the future implementation must satisfy.

---

*End of memo v0.1 — design/decision only; labeled-completion gate selected; no merge, no completion declared, no recovery, no constant amended, no run authorized.*
