# Lane 2 / GDELT 1.0 Event — Codebook Reference (TTG Field-Index Verification)

DRAFT-LOCKED REFERENCE-ONLY — GDELT 1.0 EVENT CODEBOOK PINNED FOR TTG FIELD-INDEX VERIFICATION; NO DATA FETCH, NO ARCHIVE EXECUTION, NO EXTRACTION, NO JOIN AUTHORIZED

---

## 1. Status

- **Version:** v0.1 (reference-only documentation artifact; uncommitted at drafting).
- **Type:** External-spec pin. This artifact resolves the Phase 2 blocker
  `PHASE 2 AUTHORIZATION BLOCKED — COMMITTED PROVENANCE-TRACEABLE CODEBOOK REFERENCE MISSING`
  by pinning the official GDELT 1.0 Event Data Format Codebook as a provenance-traceable,
  module-independent source of truth for the approved-field positional indices and the
  retained date field.
- **Authorizes nothing.** No data fetch, no network contact with event data, no archive
  execution, no TTG extraction, no join. Phase 2 remains unauthorized.

## 2. Purpose

The Phase 1 archive module (`src/lane2_type_tone_goldstein_local_archive.py`, untracked)
declares 0-based positional indices for the approved GDELT 1.0 Event fields. Synthetic
tests prove the filtering/firewall logic but **cannot** prove the real GDELT index→field
mapping (synthetic fixtures write values at the module's own declared indices — circular).
This memo establishes the column order and positional indices **from the official published
GDELT 1.0 Event Data Format Codebook**, independent of the module constants, so that a future
Phase 2 gate can verify the indices against committed, provenance-traceable evidence before
any network contact or content-row parsing.

## 3. Source provenance

| Attribute | Value |
|---|---|
| Document title | **GDELT — DATA FORMAT CODEBOOK** |
| Version | **V 1.03** |
| Document date | **8/25/2013** |
| Publisher | The GDELT Project (`http://gdeltproject.org/`) |
| Source URL (documentation path) | `http://data.gdeltproject.org/documentation/GDELT-Data_Format_Codebook.pdf` |
| Retrieved file type | PDF (PDF 1.4, 7 pages) |
| Retrieved byte size | 316838 bytes |
| Retrieved SHA-256 | `ed82ce6f4c55b3442e7996568570bceb96cf1ddd9fa031c36bc98d7537d8af95` |
| Temporary copy location | `/tmp/GDELT-Data_Format_Codebook.pdf` (inspection only; not committed; not under `results/` or any data path) |
| Independence | Document dated 2013-08-25, published by GDELT, predates the entire Lane 2 project; **not** derived from or a transcription of the Phase 1 module constants. |

This artifact is the **source of truth** for column order. The untracked Phase 1 module is
**not** used as evidence; it is only checked *against* this reference (§11).

**Transport-authentication note (provenance clarification).** The codebook PDF was retrieved
over the documented **`http://`** URL above. An **HTTPS** upgrade was attempted but was
**unavailable due to a TLS/certificate failure** on the `data.gdeltproject.org` host
(`ERR_TLS_CERT_ALTNAME_INVALID`), so the transport was **unauthenticated HTTP**. This weakens
**transport authentication** (the channel was not TLS-verified) but does **not** change the
**byte identity** of the inspected artifact: the exact PDF that was read is pinned by its
official source URL, title, version `V 1.03`, date `8/25/2013`, byte size `316838`, and
**SHA-256 `ed82ce6f4c55b3442e7996568570bceb96cf1ddd9fa031c36bc98d7537d8af95`**. Any future
re-verification must re-download the documentation PDF and **compare its SHA-256 to that value
before trusting it**; a mismatch invalidates this reference until re-reviewed.

**Second official documentation cross-check (corroborating, not primary).** The five approved
field positions were independently cross-checked against a **second** official GDELT
documentation reference — the published column-header label file
`http://gdeltproject.org/data/lookups/CSV.header.dailyupdates.txt` (effective
`https://www.gdeltproject.org/data/lookups/CSV.header.dailyupdates.txt`; `text/plain`,
893 bytes, SHA-256 `5c7382b118398a11042e9146e5a2f1bba16b580a00cff358f3a13f019a4361f0`). It is
official GDELT documentation/reference only (no event-data endpoint contacted), and is the
**GDELT 1.0 Event daily-updates** header (58 tab-separated labels, `SOURCEURL` present — not
GKG, not GDELT 2.0). Tab-split positional read corroborates, byte-exactly: `SQLDATE` py-idx 1;
`EventCode`/`EventBaseCode`/`EventRootCode` py-idx 26/27/28; `QuadClass` py-idx 29;
`GoldsteinScale` py-idx 30; `NumMentions` py-idx 31; `NumSources` py-idx 32; `NumArticles`
py-idx 33; `AvgTone` py-idx 34; `SOURCEURL` py-idx 57. This **corroborates** the V1.03 codebook
mapping in §7; it does **not** replace the V1.03 codebook as the primary source of truth.

## 4. Retrieval / documentation-contact boundary

- **Documentation-only retrieval.** The only network resources contacted were the two
  official GDELT **documentation** references named in §3: the codebook PDF under
  `data.gdeltproject.org/documentation/`, and the column-header label file under
  `gdeltproject.org/data/lookups/`. No other endpoint was contacted.
- **No event-data contact.** No request to `data.gdeltproject.org/events/`, no
  `YYYYMMDD.export.CSV.zip`, no event index/listing page, no raw event payload, no
  market/outcome/join data source.
- **No data saved.** No event data, no event payloads, no result files were written. The
  only file produced by this turn is this reference memo.

## 5. Source identity: GDELT 1.0 Event, not 2.0 or GKG

Confirmed directly from the codebook text:

- It is the **GDELT generation 1.0 / original** "DATA FORMAT CODEBOOK V 1.03" — **not** the
  GDELT 2.0 Event codebook (`GDELT-Event_Codebook-V2.0.pdf`, V2.0 2/19/2015) and **not** any
  GKG codebook.
- It describes the **Event Database** `.export.CSV` layout: *"GDELT event records are stored
  in an expanded version of the dyadic CAMEO format, capturing two actors and the action
  performed by Actor1 upon Actor2."*
- Width / orientation cross-check (internal, not the source of truth): *"The Historical
  Backfile collection, which runs January 1, 1979 through March 31, 2013 contains **57
  fields** for each record. The Daily Updates collection, which begins April 1, 2013 …
  contains an additional field at the end … for a total of **58 fields** for each record."*
  *"Records are stored one per line, separated by a newline (\n) … are actually
  tab-delimited."* The 58-column daily layout is consistent with the reconstructed mapping
  in §7 (the Lane 2 in-sample window 2013-04-01 … 2022-12-31 uses the 58-field daily files).

## 6. Position convention and 1-based → 0-based conversion

- The V1.03 codebook **lists the fields in sequential record order** and describes each in
  prose; it does **not** print an explicit numeric column index next to each field. The
  **column position is therefore determined by the field order in the document** (the order
  in which fields appear in the record), cross-checked against the document's own stated
  total field counts (57 backfile / 58 daily).
- This memo assigns each field its **1-based ordinal position** in that document order
  (1 = the first field, GLOBALEVENTID) and converts to the **Python 0-based index** used by
  the Phase 1 module:

  **Python 0-based index = (1-based ordinal position in record order) − 1.**

- The codebook describes the **Actor1** attribute sub-fields in full, then states *"The
  fields above are repeated for Actor2"*; likewise the **EVENT GEOGRAPHY** section defines
  one georeferencing group of sub-fields applied to **Actor1, Actor2, and Action** (three
  groups). These mirrored blocks are expanded in §7 to recover true positions.

## 7. Relevant field mapping (reconstructed from codebook record order)

Tab-delimited record, daily (Apr 1 2013+) 58-field layout. `Approved` = retained by the TTG
local archive; `Forbidden` = must not be retained.

| 1-based ord. | Python idx | Field | Codebook description (paraphrased) | TTG status |
|---:|---:|---|---|---|
| 1 | 0 | GLOBALEVENTID | Globally unique event record id (orientation only). | Forbidden (orientation) |
| 2 | **1** | **SQLDATE** (`Day`) | **Date the event took place, YYYYMMDD (integer).** | **Approved (date field)** |
| 3 | 2 | MonthYear | Alt. date format YYYYMM. | Forbidden |
| 4 | 3 | Year | Alt. date format YYYY. | Forbidden |
| 5 | 4 | FractionDate | Alt. date format YYYY.FFFF. | Forbidden |
| 6 | 5 | Actor1Code | Raw CAMEO code for Actor1. | Forbidden (actor) |
| 7 | 6 | Actor1Name | Actor1 proper name. | Forbidden (actor) |
| 8 | 7 | Actor1CountryCode | Actor1 country code. | Forbidden (actor) |
| 9 | 8 | Actor1KnownGroupCode | Actor1 known-group code. | Forbidden (actor) |
| 10 | 9 | Actor1EthnicCode | Actor1 ethnic code. | Forbidden (actor) |
| 11 | 10 | Actor1Religion1Code | Actor1 religion 1. | Forbidden (actor) |
| 12 | 11 | Actor1Religion2Code | Actor1 religion 2. | Forbidden (actor) |
| 13 | 12 | Actor1Type1Code | Actor1 type/role 1. | Forbidden (actor) |
| 14 | 13 | Actor1Type2Code | Actor1 type/role 2. | Forbidden (actor) |
| 15 | 14 | Actor1Type3Code | Actor1 type/role 3. | Forbidden (actor) |
| 16 | 15 | Actor2Code | (mirror of Actor1 block) | Forbidden (actor) |
| 17 | 16 | Actor2Name | (mirror) | Forbidden (actor) |
| 18 | 17 | Actor2CountryCode | (mirror) | Forbidden (actor) |
| 19 | 18 | Actor2KnownGroupCode | (mirror) | Forbidden (actor) |
| 20 | 19 | Actor2EthnicCode | (mirror) | Forbidden (actor) |
| 21 | 20 | Actor2Religion1Code | (mirror) | Forbidden (actor) |
| 22 | 21 | Actor2Religion2Code | (mirror) | Forbidden (actor) |
| 23 | 22 | Actor2Type1Code | (mirror) | Forbidden (actor) |
| 24 | 23 | Actor2Type2Code | (mirror) | Forbidden (actor) |
| 25 | 24 | Actor2Type3Code | (mirror) | Forbidden (actor) |
| 26 | 25 | IsRootEvent | Event found in lead paragraph flag. | Forbidden |
| 27 | 26 | EventCode | Raw CAMEO action code. | **Forbidden (collision-trap)** |
| 28 | 27 | EventBaseCode | CAMEO base action code. | **Forbidden (collision-trap)** |
| 29 | 28 | EventRootCode | CAMEO root action code. | **Forbidden (collision-trap)** |
| 30 | **29** | **QuadClass** | Primary classification 1=VerbalCoop, 2=MaterialCoop, 3=VerbalConflict, 4=MaterialConflict (integer). | **Approved** |
| 31 | **30** | **GoldsteinScale** | Event-type impact score −10..+10 (numeric). | **Approved** |
| 32 | **31** | **NumMentions** | Total mentions of the event across all source documents (integer). | **Approved** |
| 33 | 32 | NumSources | Total information sources mentioning the event (integer). | **Forbidden (gap field)** |
| 34 | 33 | NumArticles | Total source documents mentioning the event (integer). | **Forbidden (gap field)** |
| 35 | **34** | **AvgTone** | Average tone of documents mentioning the event, −100..+100 (numeric). | **Approved** |
| 36 | 35 | Actor1Geo_Type | Geo match resolution. | Forbidden (geo) |
| 37 | 36 | Actor1Geo_Fullname | Geo full name. | Forbidden (geo) |
| 38 | 37 | Actor1Geo_CountryCode | Geo FIPS country. | Forbidden (geo) |
| 39 | 38 | Actor1Geo_ADM1Code | Geo ADM1 code. | Forbidden (geo) |
| 40 | 39 | Actor1Geo_Lat | Geo latitude. | Forbidden (geo) |
| 41 | 40 | Actor1Geo_Long | Geo longitude. | Forbidden (geo) |
| 42 | 41 | Actor1Geo_FeatureID | Geo GNS/GNIS feature id. | Forbidden (geo) |
| 43–49 | 42–48 | Actor2Geo_* (7 sub-fields) | (mirror of Actor1Geo block) | Forbidden (geo) |
| 50–56 | 49–55 | ActionGeo_* (7 sub-fields) | (mirror, action location) | Forbidden (geo) |
| 57 | 56 | DATEADDED | Date the event was added to the master DB (integer). | Forbidden (mgmt) |
| 58 | 57 | SOURCEURL | URL of source article (daily files only, Apr 1 2013+). | **Forbidden (article/source URL)** |

Backfile (pre-2013-04-01) has 57 fields (no SOURCEURL, ending at DATEADDED, idx 56); the
daily files used by Lane 2 (2013-04-01 onward) have 58 fields (idx 0–57). Total field count
check: 5 (id/date) + 10 (Actor1) + 10 (Actor2) + 10 (IsRootEvent…AvgTone) + 21 (3×7 geo) + 2
(DATEADDED, SOURCEURL) = **58**. ✓ matches the codebook's stated daily total.

## 8. Approved TTG archive fields — field-by-field conversion arithmetic

The codebook lists, in record order: … `EventCode`, `EventBaseCode`, `EventRootCode`,
`QuadClass`, `GoldsteinScale`, `NumMentions`, `NumSources`, `NumArticles`, `AvgTone`, … . The
1-based ordinal → Python 0-based conversion for each approved field:

- **SQLDATE** — 2nd field in record order → Python index = 2 − 1 = **1**.
- **QuadClass** — 30th field → Python index = 30 − 1 = **29**.
  - *Collision-trap check:* QuadClass is verified to sit **after** `EventCode` (idx 26),
    `EventBaseCode` (idx 27), and `EventRootCode` (idx 28), which occupy the three positions
    immediately before it. QuadClass ≠ any EventCode-family index.
- **GoldsteinScale** — 31st field → Python index = 31 − 1 = **30**.
- **NumMentions** — 32nd field → Python index = 32 − 1 = **31**.
- **AvgTone** — 35th field → Python index = 35 − 1 = **34**.
  - *Gap-trap check (explicit):* AvgTone does **not** immediately follow NumMentions. The
    codebook places **`NumSources`** (idx 32) and **`NumArticles`** (idx 33) **between**
    `NumMentions` (idx 31) and `AvgTone` (idx 34). Therefore:
    - NumMentions → Python index **31**;
    - NumSources occupies index **32** (intervening, forbidden);
    - NumArticles occupies index **33** (intervening, forbidden);
    - AvgTone → Python index **34**.

Approved retained output schema (5 fields): `sqldate` (idx 1), `quadclass` (idx 29),
`goldsteinscale` (idx 30), `nummentions` (idx 31), `avgtone` (idx 34). This matches the
5-field allow-list locked by the active Phase 0.5 `8fdf233` §F and the v2.1 prompt `3411db5`.

## 9. Forbidden-field collision check

The approved index set is **{1, 29, 30, 31, 34}**. Verified against the §7 layout:

- **EventCode / EventBaseCode / EventRootCode** = idx {26, 27, 28}. No overlap with the
  approved set. ✓ (QuadClass at 29 is the first index *after* this CAMEO action-code family.)
- **Actor1/Actor2 fields** = idx {5…24}. No overlap. ✓
- **Geo fields** (Actor1Geo / Actor2Geo / ActionGeo) = idx {35…55}. No overlap. ✓
- **Article/source URL** (`SOURCEURL`) = idx 57; **DATEADDED** = idx 56. No overlap. ✓
- **NumSources / NumArticles** (the AvgTone-gap fields) = idx {32, 33}. No overlap with the
  approved set — correctly excluded. ✓
- **Market / outcome / joined / price-derived fields** do not exist in the GDELT 1.0 Event
  schema at all (they are not GDELT columns), so no approved index can point to one. ✓

No approved index collides with any forbidden field.

## 10. Date-field reconciliation

**Codebook (external pin):** `SQLDATE` (`Day`) is the **2nd field (Python index 1)** = *"Date
the event took place, YYYYMMDD."* It is the **event/record-occurrence date**. The codebook
distinguishes this from `DATEADDED` (idx 56) = the date the event was added to the database
(*"the SQLDATE and other event date fields contain[] the date the event actually took place,
while the DATEADDED field … will ca[pture the date added]"*).

**Active Lane 2 governing bytes:**
- `294494a` (lock-closure v0.2, the commit changed exactly this file): locks the **information
  date** concept — daily aggregates *"on the information date,"* strictly-prior expanding-window
  standardization *"{x_s : s < t} … no current or future day"* — and delegates the concrete
  field to *"the project's locked row-date rule (v0.1 §10)"* (§6 line 101). It does **not**
  itself byte-name SQLDATE or a column index.
- `0295406` (design memo v0.1, latest touch = `0295406`): §151 locks the **date-attribution
  premise** — *"aggregate event content to the event's already-established daily information
  date using the project's previously locked row-date / SQLDATE logic … a locked premise, not
  … redesign[ed]."* §59 names *"`SQLDATE` or the project's established event-date field."*
- `c6aeb2b` (lock-closure **v0.3**, latest touch = `c6aeb2b`; **active** amendment): §5 lines
  45–47 — *"`SQLDATE_COLUMN_INDEX = 1` (memo §9 / `e55e09a`); Decision D aggregates by SQLDATE
  → per-`civil_date`. **Date key = `civil_date` = SQLDATE-aggregated date.**"* and the
  characterization correction: *"`civil_date` = SQLDATE = GDELT **event/record date**;
  availability lags ≤ +1 day (`rows_from_offset_plus_1`), handled by the join memo's
  `civil_date+1` no-lookahead anchor. Predictor-only extraction has no lookahead."*
- `8fdf233` (active Phase 0.5): §F lines 109–113 — Phase 0.5 MAY verify *"`civil_date = SQLDATE`
  … `SQLDATE_COLUMN_INDEX = 1`"*, no event-occurrence backdating, the +1 availability-lag rule
  specified, no-lookahead intended.
- Outcome-side (`084c5bd`, `bc3b9c0`, `df9089b`): the no-lookahead invariant is anchored on the
  **maximal information-availability date** `m = civil_date + 1 day` (locked default); the
  outcome realizes strictly **after** that boundary.

**Reconciliation result.** The module's `DATE_FIELD_COLUMN_INDEX = 1 (# SQLDATE)` reconciles
with all of: (a) the codebook position — SQLDATE = Python index 1, event-occurrence date
YYYYMMDD; (b) `294494a`'s information-date concept — resolved by the locked row-date rule;
(c) the active row-date rule — `0295406` §151 locked premise and `c6aeb2b` §5 `civil_date =
SQLDATE` at index 1; (d) the outcome-side `civil_date + 1` no-lookahead anchor — which manages
the event-date-vs-availability lag the codebook flags. **SQLDATE at Python index 1 is the
correct retained archive date field.**

**Carried-forward caveat (not resolved by this reference; remains a Phase 2 precondition).**
The codebook confirms SQLDATE is the *event-occurrence* date, which is precisely why
`8fdf233` §F parks a **Phase 2 availability-timing validation** requirement: before extracted
day-`t` rows may be treated as available at `civil_date + 1`, the Phase 2 execution gate must
either confirm day-`t` SQLDATE rows were ingested/available by `t+1` or use the GDELT
update-file date as the availability stamp, else BLOCK / route to design review. This memo
resolves only the **positional / field-identity** verification, not availability timing.

## 11. Phase 1 module index verification

Module under check: `src/lane2_type_tone_goldstein_local_archive.py` (untracked; 0-based
constants, lines 93–97). Compared **against this codebook reference** (not the reverse):

| Module constant | Module value | Codebook-derived Python index | Match |
|---|---:|---:|:--:|
| `DATE_FIELD_COLUMN_INDEX` (SQLDATE) | 1 | 1 | ✅ |
| `QUADCLASS_COLUMN_INDEX` | 29 | 29 | ✅ |
| `GOLDSTEINSCALE_COLUMN_INDEX` | 30 | 30 | ✅ |
| `NUMMENTIONS_COLUMN_INDEX` | 31 | 31 | ✅ |
| `AVGTONE_COLUMN_INDEX` | 34 | 34 | ✅ |

**All five Phase 1 module indices match the official GDELT 1.0 Event Data Format Codebook
V1.03.** The module's own `_MAX_APPROVED_INDEX` (max = 34) is consistent: any record with ≤ 34
columns is malformed for these reads, and the 58-field daily layout amply satisfies it.

## 12. Phase 2 precondition

This reference satisfies the codebook prerequisite that previously blocked Phase 2:

- A committed, provenance-traceable GDELT 1.0 Event codebook reference now exists (this memo,
  once committed), tracing to the official published V1.03 codebook with source URL, version,
  date, byte size, and SHA-256, and independent of the module constants.
- The approved-field indices {1, 29, 30, 31, 34} and the retained date field (SQLDATE = idx 1)
  are byte-clear and match the Phase 1 module.

**Before any Phase 2 network contact or content-row parsing**, the Phase 2 authorization gate
must (i) re-verify the Phase 1 indices against this reference, (ii) re-confirm the date-field
reconciliation in §10, and (iii) additionally satisfy the **separate** availability-timing
validation parked by `8fdf233` §F (see §10 caveat). This memo does **not** waive (iii).

## 13. Boundaries not authorized

This artifact authorizes **none** of the following, all of which remain firewalled behind
their own separate, explicitly-authorized gates:

- GDELT network/event-data fetch; contact with `data.gdeltproject.org/events/`; any
  `.export.CSV.zip` or event index/listing;
- Phase 2 local archive build / execution;
- TTG extraction (design, execution, or authorization);
- outcome-side join (authorization or execution);
- any read of raw event data, result-file contents, market data, outcomes, joined data,
  `next_session_return`, or `abs(next_session_return)`;
- unsealing or reading 2023+ data.

## 14. Superseded-source exclusion

`4fe1f0c` (v2.1 Phase 0.5 conformance amendment) is **superseded by `8fdf233`** (Phase 0.5
Option A `y_synth` correction) and was **not** used as active evidence in this reference. All
Phase 0.5 date-rule evidence here is read from `8fdf233`'s own changed file
(`docs/lane2_gdelt1_type_tone_goldstein_v2.1_phase0.5_amendment_v0.1.md` at `8fdf233`).

## 15. Boundary confirmation

Documentation-only GDELT retrieval (the V1.03 codebook PDF under
`data.gdeltproject.org/documentation/`); no event-data contact; no event index contact; no
`.export.CSV.zip` contact; no raw-event data read; no result-file content read; no archive
execution; no archive authorization; no TTG extraction authorization; no TTG extraction
execution; no join authorization; no join execution; no market-data read; no outcome read; no
joined-data read; no `next_session_return` read; no `abs(next_session_return)` read; no tests;
no V1/V2 execution; no 2023+ real data. This memo is reference-only and authorizes nothing.
