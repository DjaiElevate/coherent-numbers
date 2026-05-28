# Lane 2 GDELT1 chunk_2022 — 2022-11-10 Catalog-Object Conflict Remediation Design Memo v0.1

> **Design / decision memo only.** This memo documents the persistent catalog-object conflict for `2022-11-10` and selects the next *decision path* at the design level. It does **not** implement remediation, amend any constant, authorize a fresh chunk_2022 run, perform network probes, or open the merge gate.

---

## 1. Purpose

- Document the **persistent catalog-object conflict** affecting `2022-11-10` / `20221110.export.CSV.zip`.
- Decide the next remediation **decision path** at the design level.
- Do **not** implement remediation; do **not** amend constants (`KNOWN_SUBSTRATE_GAPS` or any other); do **not** authorize a fresh chunk_2022 run; do **not** open the merge gate.

## 2. Baseline

- local HEAD before memo: `b10bd04b86cad484eb04d5ea9e3b6e7bc82dbd8d`
- origin/main before memo: `cb145d11d56d19d496c57a0c55bd0bb6cda6f2c5`
- local branch ahead by two **sanctioned** guard-toggle commits (from the authorized halted attempt):
  - `322e34c339f5596aef677e8f5225ec6a3b09bcc8` — halted-attempt **enable** commit
  - `b10bd04b86cad484eb04d5ea9e3b6e7bc82dbd8d` — halted-attempt **restore** commit
- chunk_2022 progress remains **313/365**; substrate progress remains **9/10**.
- on-disk Path (b) remains **93**; user-side counter track is **retired** (not used).

## 3. Halt summary

- chunk_2022 execution halted at `20221110.export.CSV.zip`; class `FetchFailure`; HTTP 404; **313** files completed before halt.
- enable commit: `322e34c339f5596aef677e8f5225ec6a3b09bcc8`
- restore commit: `b10bd04b86cad484eb04d5ea9e3b6e7bc82dbd8d`
- guard restored to `FULL_BUILD_AUTHORIZED = False`; runner blob round-tripped to `dec8e09283de9357b2b2aa65af13e21b21fe85cc`.
- **No retry / no skip / no rescue / no silent amendment.**
- This halted enable/restore pair is **sanctioned history from an authorized attempt** and belongs on origin together with this explanatory memo. (This is unlike the discarded out-of-band chunk_2020 no-op pair `8ca0b12`/`d8d9794`, which was reset out of history; that pair was a non-executing accidental toggle, whereas this pair bracketed a real, authorized run that fetched 313 files before the upstream 404.)
- Halt diagnostic: `results/lane2_gdelt1_full_daily_count_build/chunk_2022_20260528T121150Z/halt_diagnostic.json`, SHA-256 `009720576b0e3dc3f11d67dbd811e36bbfd5a385df55567e1191ad30441057b7`.

## 4. Diagnostic evidence

**First diagnostic** — `DIAGNOSIS — INCONCLUSIVE UPSTREAM AVAILABILITY`:
- catalog (index / md5sums / filesizes) listed `20221110.export.CSV.zip`; md5 `91e15516016f986e5b8a08712e1de95a`; filesize `6,714,105`.
- direct object: HEAD **404**, range-GET **416**.
- neighbors `20221109` / `20221111` available and matched catalog.

**Second diagnostic (~16 min later)** — `DIAGNOSIS — PERSISTENT CATALOG-OBJECT CONFLICT`:
- catalog still listed `20221110.export.CSV.zip`; md5 **unchanged** `91e15516016f986e5b8a08712e1de95a`; filesize **unchanged** `6,714,105`.
- direct object still unserved: HEAD **404** (both probes); range-GET **404** (second probe; **416** in the first) — both indicate the object is not served.
- neighbors `20221109` / `20221111` still available (catalog-listed, HEAD 200, range 206, content-lengths matching `filesizes`).
- **HTTPS** checks failed with curl exit 60 for all dates due to the local TLS/certificate environment — **not** date-specific evidence.
- **BigQuery / alternate official-source check skipped**: `bq`, `gcloud`, `gsutil` absent from PATH; installing/authenticating forbidden.
- No zip payload downloaded; no unzip; no remediation decision made during diagnostics.

## 5. Classification

- **persistent catalog-object conflict** ✅
- NOT a `known substrate gap`
- NOT an ordinary `transient 404`
- NOT a `structural offset anomaly`
- NOT a `sentinel anomaly`
- NOT a `runner failure` (the runner correctly halted on an unexpected fetch failure)

## 6. Why `KNOWN_SUBSTRATE_GAPS` amendment is disfavored

- Current evidence says the file **exists** in GDELT's own catalog (index + md5 `91e1551…` + size `6,714,105`).
- **No official evidence** says the date has no data.
- Adding `2022-11-10` to global `KNOWN_SUBSTRATE_GAPS` would likely **record a falsehood**.
- It would **globally alter** the gap constant that populates `substrate_gap_dates_not_fetched` (and `known_substrate_gap_dates`) in **every** chunk.
- It would **stale** the prior four-date field semantics already recorded for the nine completed chunks (2013-partial, 2014–2021).
- It would **reduce expected chunk_2022 count from 365 to 364** without proving the date has no data.
- Therefore `KNOWN_SUBSTRATE_GAPS` amendment is **not** the default path; it is admissible only if later official evidence shows the date genuinely has no data or the catalog evidence is withdrawn/contradicted.

## 7. Candidate remediation paths

**A. Wait-and-reprobe** — repeated read-only probes over a longer horizon. Lowest invasiveness; appropriate because storage/CDN/object-store repairs may self-heal (the catalog asserts a real 6.7 MB object). Does not resolve if the conflict persists indefinitely.

**B. Alternate official-source existence check** — in an environment with already-configured official-source access (BigQuery/GCS/public official dataset), verify whether SQLDATE `20221110` has rows/data (no export, no recovery). Provides stronger evidence before any recovery design.

**C. Alternate official-source recovery design** — only after official existence is confirmed (B). Would need a design memo for how to reconstruct/import the missing daily file consistently (provenance, md5/size compatibility if possible, schema compatibility, audit trail). Not implemented here.

**D. Dedicated upstream-object-unavailable mechanism** — separate from `KNOWN_SUBSTRATE_GAPS`; models *cataloged-but-unserved* objects. Could let expected-count / fetch logic account for inaccessible-but-catalogued files without false no-data claims. Requires careful global-field design.

**E. `KNOWN_SUBSTRATE_GAPS` amendment** — currently disfavored (see §6); admissible only if later official evidence shows genuine no-data or the catalog is contradicted; requires explicit global-field-consequence discussion.

## 8. Selected decision path (conservative)

1. **First: wait-and-reprobe** over a longer horizon, separately authorized.
2. **Second: if the conflict persists**, seek **alternate official-source existence confirmation** (path B) in an already-configured environment, separately authorized.
3. **Third: only after** those steps, open a remediation **implementation** design memo (path C or D, as the evidence dictates).
- Do **not** select `KNOWN_SUBSTRATE_GAPS` amendment (E) as default.
- Do **not** authorize a fresh chunk_2022 attempt yet.

## 9. Required future wait-and-reprobe design

A future read-only diagnostic prompt should: run the same repo preflight; no runner execution; no source edits; no memory update unless separately chosen; check catalog/md5/filesizes; check the direct object endpoint; check neighbors; compare to **both** prior diagnostics; and classify as one of:
- raw object available now,
- persistent catalog-object conflict remains,
- official sources now contradict the catalog,
- inconclusive.
If the raw object becomes available, a future **fresh** chunk_2022 attempt may be considered separately. If the conflict persists, the alternate official-source existence check (§10) becomes the next recommended branch.

## 10. Required future alternate-source existence check design

Must be **read-only**; official source only; no install/auth/config changes unless separately authorized outside this workflow; query only existence/count for `SQLDATE=20221110`; no export of rows; no market data; no Step 2. The result informs recovery design only — it does not by itself authorize recovery.

## 11. Fresh-attempt rule

- The halted chunk_2022 attempt must **not** be retried or resumed.
- If the raw object becomes available or remediation is designed, a later chunk_2022 run must be a **separately-authorized fresh attempt**, still satisfying all **three production locks** (`FULL_BUILD_AUTHORIZED=True` + CLI `--authorize-full-build-run` + env `LANE2_FULL_BUILD_AUTHORIZED=1`), and must **not** reuse the halted directory.
- Future fresh-attempt enable/restore commits **may reuse the same commit subjects**, so this halted pair must be **disambiguated by SHA** in future handoffs: enable `322e34c339f5596aef677e8f5225ec6a3b09bcc8`, restore `b10bd04b86cad484eb04d5ea9e3b6e7bc82dbd8d`.

## 12. Merge-gate boundary

chunk_2022 remains incomplete; substrate progress remains **9/10**; the **merge gate remains closed**. Merge may open only after successful chunk_2022 completion and a separate closure. The output-commit question remains separately scoped.

## 13. Counter discipline

- On-disk **Path (b) remains 93** in this non-memory turn; the user-side counter is retired; do not use user-side arithmetic.
- The next memory-write boundary must count sanctioned Claude Code reports since Path (b)=93 per the established on-disk rule. **Intervening ordinal carry-forward since 93:**
  - chunk_2022 plan-memo report → 94
  - chunk_2022 halted execution report → 95
  - read-only diagnostic 1 report → 96
  - read-only diagnostic 2 report → 97
  - this remediation design memo report → 98
- Because this is **not** a memory-write turn, Path (b) stays **93** on disk. The eventual memory-write boundary may therefore produce a larger jump (e.g., to 98+ depending on intervening reports) than the recent +3 closures — that is **expected, not a discrepancy**.

## 14. Boundaries preserved

No runner execution; no retry; no resume; no source edit; no constants amended; no memory update; no merge; no Step 2; no market data; no instrument construction; no archive; no payload download; no unzip; no network probes this turn.

## 15. Next frontier

A **separately-authorized wait-and-reprobe diagnostic over a longer horizon** (§9). Not a rerun, not an amendment, not a merge. If/when that diagnostic shows the raw object available, a separately-authorized fresh chunk_2022 attempt may follow; if the conflict persists, the alternate official-source existence check (§10) is next.

---

*End of memo v0.1 — design/decision only; no remediation implemented, no constant amended, no run authorized, no merge.*
