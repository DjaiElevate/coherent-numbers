# Lane 2 GDELT1 chunk_2022 — 2022-11-10 Recovery / Consistency Implementation Design Memo v0.1

> **Design / decision memo only.** Decides the recovery/consistency architecture for the `2022-11-10` data-bearing-but-raw-object-unavailable case and the merge-gate consequence. It does **not** implement recovery, modify runner code, run BigQuery, amend any constant, authorize a fresh chunk_2022 run, or open the merge gate.

---

## 1. Purpose

- Decide the recovery / consistency architecture for the `2022-11-10` data-bearing-but-raw-object-unavailable case.
- Make the **recover-vs-represent** decision explicit.
- Define the **merge-gate consequence**.
- Do **not** implement recovery, modify runner code, authorize fresh chunk_2022 execution, or open the merge gate.

## 2. Baseline

- HEAD/origin baseline `854a60698c1a186096de2a518b996e3c1ecf7807`.
- chunk_2022 remains **313/365**; substrate progress remains **9/10**.
- on-disk Path (b) remains **93**; user-side counter **retired** (not used).
- carry-forward ordinal **before** this memo report = **103**.

## 3. Evidence summary

- **A. Original halt:** chunk_2022 halted after 313/365 at `20221110.export.CSV.zip`; `FetchFailure` / HTTP 404; guard restored; no retry/skip/rescue/silent amendment. Sanctioned halted-attempt commits: enable `322e34c339f5596aef677e8f5225ec6a3b09bcc8`, restore `b10bd04b86cad484eb04d5ea9e3b6e7bc82dbd8d`.
- **B. Raw catalog evidence:** index/md5sums/filesizes consistently list `20221110.export.CSV.zip` (md5 `91e15516016f986e5b8a08712e1de95a`, size `6,714,105`); canonical raw endpoint unserved across four probes (~3 h): HEAD 404, range 416/404; neighbors `20221109`/`20221111` healthy and size-compatible.
- **C. Official BigQuery evidence (user-run):** `gdelt-bq.full.events` counts `20221109 = 117,008`, **`20221110 = 105,041`**, `20221111 = 40,588` → the date is data-bearing. `105,041` is a raw-`COUNT(*)` coverage reference, **not** an automatic exact runner-output gate.
- **D. Final raw-object check:** `RAW OBJECT STILL UNAVAILABLE DESPITE OFFICIAL DATA CONFIRMATION`; no self-heal across the tested horizon (self-heal remains a free fallback but must not be assumed).
- **E. Alternate official raw-object diagnostic:** `ONLY OFFICIAL TABLE / BIGQUERY EVIDENCE FOUND, NO RAW OBJECT`; HTTPS canonical = same object identity, env-TLS-inconclusive; GDELT 2.0 masterfilelist = different dataset (the `20221110` hit was a false substring of v2 timestamp `20220221110000`); v1 master-file-list analogues 404; no `2022.zip` annual archive; **path C ruled out under current evidence**; paths B/D remain.
- **Core classification:** `2022-11-10` is data-bearing; canonical v1 raw object unavailable; no official alternate raw object; BigQuery-derived semantic recovery is the only currently-evidenced data source; `KNOWN_SUBSTRATE_GAPS` amendment rejected.

## 4. Decision question

This memo must answer: (a) Should the project **recover** a semantic 2022-11-10 day from official BigQuery data, or only **represent** the day as upstream-object-unavailable? (b) Does a semantically recovered day count as **substrate-equivalent** enough to satisfy chunk_2022 completion / the merge gate? (c) If yes, what provenance/audit markings are required? (d) If no, what does "10/10" mean with 364 raw days + 1 documented unavailable-but-data-bearing day?

## 5. Candidate design outcomes

**A. Recover-admissible** — use official BigQuery rows for SQLDATE 20221110 as a semantic recovery source; treat the recovered day as data-bearing and admissible for completion only with explicit asterisked provenance; raw zip md5/byte layout cannot be matched unless the raw object self-heals; requires a dedicated recovery artifact + manifest + runner-count reconciliation; potentially permits asterisked 365/365 and 10/10 closure if all audit conditions are met.

**B. Represent-only** — do not recover rows; represent 2022-11-10 as official-data-confirmed but raw-object-unavailable; chunk_2022 = 364 raw days + 1 documented unavailable/data-bearing day; requires an explicit merge-eligibility decision; avoids semantic reconstruction but may block or redefine the merge gate.

**C. Blocked pending additional evidence** — defer until a future raw-object self-heal, official alternate object, or additional official-source evidence appears; maximal purity but leaves the build incomplete and the decision unmade.

## 6. Required selection

**`SELECTED — REPRESENT-ONLY / NO SEMANTIC RECOVERY`.**

Rationale (from the substrate-admissibility analysis in §7): the Lane 2 full daily-count substrate is defined by parsing the **raw GDELT 1.0 daily `.export.CSV.zip` objects** under the runner's exact offset/sentinel/recognized-list semantics. A BigQuery-derived day is **not substrate-equivalent**: it cannot reproduce the catalog raw md5 (`91e1551…`) or byte layout, and the official table's shape/ordering/typing differs from the raw file, so reconstructing a runner-equivalent day would require re-deriving the runner's daily-count semantics against a different schema — a fidelity risk introduced for a single date among ~3,650. The truthful, purity-preserving action is to **represent** 2022-11-10 exactly as it is (official data exists; raw object unavailable) rather than manufacture a substitute and count it as substrate.

**Why not Recover-admissible:** it injects a non-raw, non-md5-matching artifact into an otherwise raw-pure substrate and asterisks everything downstream, for one day — the integrity cost outweighs the convenience of a "365/365" label, especially since represent-only can still reach a labeled completion (§11) without fabricating substrate. BigQuery confirming data exists does **not** make recovery the default (§7).

**Why not Blocked:** the evidence is already sufficient to decide *substrate admissibility* — what was missing (self-heal, alternate object) has been actively searched and ruled out. The remaining question is a design judgment, not absent evidence; deferring again would be avoidant. (Self-heal nonetheless remains a free fallback at execution time per §13.)

## 7. Evidentiary burden / substrate-admissibility analysis

Recovery is **not** treated as default merely because BigQuery confirms data exists. The first-order question is **substrate admissibility**: is an official BigQuery-derived semantic day substrate-equivalent enough for Lane 2's raw-file daily-count build, or does the build require **raw-object substrate purity** such that recovery can only be *represented*, not *counted as completion*?

- **Recover-admissible burden (not met):** it would need to justify that BigQuery-derived data — despite non-matching raw zip md5/byte layout and a different table schema/ordering — can satisfy the chunk_2022 completion and merge-gate standard with asterisked provenance. It cannot meet the raw-substrate-equivalence bar; at best it yields a *semantically similar* day, not the raw object the other 364 days (and all prior chunks) are built from.
- **Represent-only burden (met):** confirmed official data should not be *fabricated into substrate* simply because it exists; representing the day truthfully (data-bearing, raw-object-unavailable) is both honest and consistent with the already-made decision to reject a no-data `KNOWN_SUBSTRATE_GAPS` amendment. It tells the literal truth on both axes — neither "no data" nor "raw day recovered."
- **Blocked burden:** would require that *new* evidence could change the admissibility call; but admissibility is a standards question the project can answer now.

The selected outcome (represent-only) follows from this analysis — raw-object substrate purity is the operative standard — **not** from a default preference.

## 8. B/D architecture (not selected — for completeness only)

Recover-admissible is **not** selected, so the B+D stacked design is **not** adopted. Recorded only so a future reversal would be explicit: were recovery ever selected, path B (official BigQuery rows for `SQLDATE=20221110`) would supply the data and path D (a dedicated upstream-object-unavailable hook, **distinct from `KNOWN_SUBSTRATE_GAPS`**, never reducing expected count 365→364, with a separate recovered-day provenance flag) would supply the mechanism, with no claim of raw-zip md5/byte equivalence unless self-heal occurs. This memo does **not** authorize that path.

## 9. BigQuery recovery semantics

Not applicable under the selected represent-only outcome (no recovery artifact is produced). For the record: had recovery been selected, the future implementation design would have had to specify the exact official table/query, columns, GDELT 1.0 schema mapping, deterministic ordering, encoding/delimiter/null handling, the use of `105,041` strictly as a coverage reference, an explicit reconciliation between BigQuery raw `COUNT(*)` and runner daily-count semantics, count-mismatch handling, and an explicit no-raw-md5-equivalence statement. None of this is undertaken now.

## 10. Runner / artifact design requirements

Not applicable under represent-only — **no runner code change, no recovery artifact, no recovered-day metadata field is designed or authorized here.** The runner stays at blob `dec8e09…` with `expected_file_count` for chunk_2022 unchanged at 365. The *representation* (how 2022-11-10's documented-unavailable status is recorded and surfaced) is delegated to the separately-authorized merge-gate definition / representation design memo (§17), which must decide artifact/label wording without amending `KNOWN_SUBSTRATE_GAPS`.

## 11. Merge-gate consequence

Under **represent-only**, 2022-11-10 is documented as official-data-confirmed-but-raw-object-unavailable; it is **not** semantically recovered and **not** recorded as a no-data gap. The merge-gate consequence (to be finalized in the separate merge-gate definition memo, not here) is one of:

- **(i) Labeled completion (recommended):** redefine the gate so "10/10 chunks processed to completion" admits explicitly-labeled upstream-object-unavailable-but-official-data-confirmed dates; chunk_2022 then counts as **364 raw days + 1 documented represented day**, and the merge must carry a disclosure label (e.g., "10/10 with 1 documented upstream-object-unavailable date: 2022-11-10") plus a cross-chunk table separating raw vs documented-unavailable days. This unblocks the program honestly without fabricating substrate.
- **(ii) Strict raw-purity (block):** if the gate requires all 365 raw objects, merge stays **blocked** for chunk_2022 until canonical self-heal (or a future official alternate raw object) appears.

This memo **recommends (i)** as consistent with the project's truth-over-convenience posture, but **defers the binding merge-gate decision** to the merge-gate definition memo. It does **not** open the merge gate.

## 12. Substrate-purity / scientific-use boundary

- An official BigQuery-derived day is **not** substrate-equivalent to a raw-object day for Lane 2; under represent-only no such day is created, so the substrate stays raw-pure for all counted days.
- Downstream may state: "2022-11-10 is official-data-confirmed (105,041 BigQuery rows) but its raw GDELT 1.0 daily object was unavailable; it is documented, not raw-counted."
- Downstream must **not** state or imply that 2022-11-10 was raw-processed, nor silently treat it as an ordinary raw day, nor hide its documented-unavailable status inside aggregate-only artifacts.
- **Step 2 / market data / instrument construction remain firewalled** and must explicitly carry the documented-unavailable status of 2022-11-10 if/when they consume chunk_2022; no silent promotion of the represented day to raw status.

## 13. Self-heal fallback

If the canonical raw object becomes available before any fresh execution, the **normal raw-object runner path is preferred** — it would supersede this representation for the date and restore full raw-substrate purity (365 raw days). This is a free fallback that requires no design change. Any fresh chunk_2022 attempt still requires separate authorization and all three production locks, and must not reuse the halted directory.

## 14. Future implementation memo requirements

Because the selected outcome is **represent-only**, no *recovery* implementation is required. The next memo is a **merge-gate definition / representation design memo** that must specify: the exact wording/label for the documented-unavailable date; where it is recorded (e.g., a representation note, not `KNOWN_SUBSTRATE_GAPS`); how chunk_2022 "completion" is phrased (option (i) vs (ii) of §11); the cross-chunk raw-vs-documented disclosure table; whether any runner/metadata change is needed to *surface* (not recover) the status; conformance/unit tests for that surfacing if code is touched; and the explicit downstream-claim boundary. No live run, no Step 2, no market data, no `KNOWN_SUBSTRATE_GAPS` amendment.

## 15. Counter discipline

- On-disk **Path (b) remains 93** in this non-memory turn; user-side counter retired and not used.
- Carry-forward ordinal through the prior alt-object diagnostic = **103**.
- This memo report should be treated as carry-forward ordinal **104** if completed.
- The eventual memory-write boundary must reconcile the larger jump from 93 — that is **expected, not a discrepancy**.

## 16. Boundaries preserved

No runner execution; no retry; no resume; no source edit; no constants amended; no memory update; no merge; no Step 2; no market data; no instrument construction; no archive; no payload download; no row export; no BigQuery run; no recovery implementation; no network probes this turn.

## 17. Next frontier

Per the selected **represent-only** outcome: a **separately-authorized merge-gate definition / representation design memo** (§14) that decides whether labeled completion (§11(i)) or strict-raw-purity block (§11(ii)) governs, defines the disclosure label and cross-chunk table, and surfaces 2022-11-10's documented-unavailable status without amending `KNOWN_SUBSTRATE_GAPS`. Self-heal remains a free fallback (§13). Never an immediate rerun; never an amendment under current evidence; never a merge in this turn.

---

*End of memo v0.1 — design/decision only; represent-only selected; no recovery implemented, no constant amended, no run authorized, no merge.*
