# Lane 2 / Type-Tone-Goldstein — Availability-Timing Amendment

DRAFT-LOCKED DESIGN-ONLY — AVAILABILITY-TIMING AMENDMENT FOR NO-LOOKAHEAD TTG PREDICTORS; FILE-DATE <= SQLDATE+1 RULE SELECTED; NO NETWORK, NO ARCHIVE EXECUTION, NO EXTRACTION, NO JOIN AUTHORIZED

---

## 1. Status

- **Version:** v0.1 (design-only amendment; uncommitted at drafting).
- **Type:** Predictor-side availability-eligibility amendment. It resolves the Phase 2 blocker
  `PHASE 2 AVAILABILITY DESIGN BLOCKED — DESIGN AMENDMENT NEEDED BEFORE PHASE 2`.
- **DRAFT-LOCKED, DESIGN-ONLY.** It amends only the predictor-side information-availability
  eligibility rule. It **authorizes no network, no archive execution, no TTG extraction, no
  join**, and changes no outcome-side convention. Phase 2 remains unauthorized.

## 2. Purpose

Define a no-lookahead predictor-side availability rule for the Type-Tone-Goldstein (TTG) local
archive so that a daily predictor attributed to information-date `t` is built **only** from
source-file contributions that were available by `t + 1`. This replaces the prior implicit
assumption that aggregating all rows by `SQLDATE` yields a day-`t` value available at `t + 1`.

## 3. Prior blocker

- The prior default assumed `SQLDATE` day-`t` rows were available by `t + 1`.
- `c6aeb2b` §5 (line 47) **asserted** the `≤ +1` availability lag using `rows_from_offset_plus_1`
  — an assertion ("characterization correction"), **not** proof.
- `8fdf233` §F (lines 117–121) explicitly **parked availability-timing validation for Phase 2**:
  at Phase 2 the gate must either confirm day-`t` SQLDATE rows were available by `t + 1`, or use
  the GDELT update-file date as the availability stamp, else **BLOCK / route to design review**.
  It forbids any earlier empirical no-lookahead claim.
- Committed row-date characterization (`858b501` execution report, `0065d10` post-characterization
  decision memo; 21-file sample) shows the **exhaustive offset taxonomy**
  `{0, −1, −7, −30, −365, −3650, +1}` of `offset = SQLDATE − file_nominal_date`.
- Post-characterization **Decision 1 = Option B** ("keep all rows, re-key every row to `SQLDATE`")
  folds **all** buckets — including the late-arriving lookback buckets — into the day-`t` aggregate.
- Outcome-side `civil_date + 1` / R1 anchoring (`df9089b` §4.3, `bc3b9c0`) protects the **outcome**
  side only; it does **not** remove predictor-side lookahead.

## 4. Evidence summary

| Source | What it says | Supports old `≤+1`? | Contradicts old `≤+1`? | Implies amendment? |
|---|---|:--:|:--:|:--:|
| `8fdf233` §F (117–121) | Availability timing is **unvalidated**; Phase 2 must confirm-by-`t+1` **or** use file/update date as availability stamp, else BLOCK | No (defers) | Neutral (says unproven) | **Yes** |
| `c6aeb2b` §5 (47) | Asserts `availability lags ≤ +1 day (rows_from_offset_plus_1)`; "Predictor-only extraction has no lookahead" | Asserts only | — | Assertion needs enforcement |
| `df9089b` §4.3 (169–205) | Default `max-info-date = civil_date + 1`; `rows_from_offset_plus_1` is a **forward +1** internal reference | Outcome-side only | — | Outcome-side, not predictor-side |
| `bc3b9c0` (R1) | Outcome anchored strictly after `m = civil_date + 1` | Outcome-side only | — | No (outcome side) |
| codebook ref §10 | SQLDATE (idx 1) = **event-occurrence** date ≠ DATEADDED (idx 56); availability explicitly unresolved | — | — | Confirms gap |
| `858b501` / `0065d10` | Offset taxonomy `{0,−1,−7,−30,−365,−3650,+1}`; **Option B re-keys all rows to SQLDATE** | — | **Yes** — SQLDATE-`t` rows appear in files dated `t+7 / t+30 / t+365 / t+3650` (and pre-2015 `t−1`), so day-`t` aggregate includes contributions **not available by `t+1`** | **Yes** |

**Reading of the offset taxonomy (decisive).** With `offset = SQLDATE − file_date`, a fixed event
date `t` is emitted across files dated `t` (offset 0), `t+1` (offset −1), `t+7` (offset −7),
`t+30` (offset −30), `t+365` (offset −365), `t+3650` (offset −3650), and pre-2015 `t−1`
(offset +1). Only the `{0, −1, +1}` buckets satisfy file date `F ≤ t + 1`; the `{−7, −30, −365,
−3650}` lookback buckets arrive **later** than `t + 1`. Under Option-B re-keying these
late-arriving rows are folded into the day-`t` aggregate — a predictor-side seal-risk.

## 5. Decision

1. The blanket rule "aggregate all rows by `SQLDATE` and treat day-`t` as available by `t + 1`"
   (Option-B re-keying) is **unsafe for no-lookahead predictors**.
2. `c6aeb2b` §5 remains active **except** the implicit predictor-availability claim amended here.
3. `SQLDATE` remains the GDELT **event/record-occurrence date** and remains the retained archive
   date field (Python index 1; codebook reference §7/§10).
4. **Amended information-availability eligibility rule (governing):** for a predictor for
   `SQLDATE / civil_date = t`, include **only** source-file contributions whose file/update date
   `F` satisfies **`F <= t + 1`**.
5. Rows with `SQLDATE = t` appearing in source files dated **later than `t + 1`** are
   **late-arriving lookback contributions** (offset `−7 / −30 / −365 / −3650`) and **must not**
   contribute to the day-`t` no-lookahead predictor.
6. Late-arriving rows **may** be (a) **excluded** from the no-lookahead predictor archive, or
   (b) routed to a **separately governed late-arrival / restatement archive** — but they **must
   not** be folded into day-`t` predictors used at `t + 1`.

## 6. Amended availability rule

- **Governing eligibility:** a retained predictor row for information-date `t` is eligible **iff**
  its source file/update date `F` satisfies **`F <= SQLDATE + 1`** (equivalently `offset =
  SQLDATE − F >= −1`, i.e. only the `{0, −1, +1}` buckets).
- The `{−7, −30, −365, −3650}` lookback buckets are **ineligible** for the day-`t` no-lookahead
  predictor.
- The pre-2015 `+1` forward bucket (`SQLDATE = F + 1`, file dated `t − 1`) satisfies `F = t − 1 ≤
  t + 1` and is therefore eligible by this rule; it is the same mechanism that fixes the
  `max-info-date = civil_date + 1` boundary and is consistent with the outcome-side anchor.
- This is a **predictor-eligibility** rule. It does not alter `SQLDATE` semantics, the row-date
  key, or any outcome-side timing.

## 7. Window-boundary handling (fully covered predictor window)

The amended `file_date <= SQLDATE + 1` rule (§6) defines *eligibility per contribution*; it does
**not** guarantee that an edge SQLDATE day has complete eligible-file coverage inside the
**authorized source-file window**. These are two distinct, non-contradictory layers:

- **Eligibility layer (§6):** whether a contribution is allowed by `file_date <= SQLDATE + 1`
  (eligible offset buckets `{0, −1, +1}`).
- **Window-coverage layer (this section):** whether the SQLDATE day's eligible file dates all fall
  **inside the authorized source-file window**. A bucket that is eligible by rule but whose file
  date lies **outside** the window does **not** permit reading outside the window.

**Authorized source-file window (locked):** `2013-04-01` through `2022-12-31` (the Lane 2 in-sample
GDELT 1.0 daily-regime window). No file outside this window may be fetched, enumerated, opened, or
read for any purpose, including edge completion.

**Fully covered predictor window (governing).** A SQLDATE day `t` belongs to the **primary
no-lookahead predictor archive only if every potentially eligible source-file date under the §6
rule lies inside the authorized source-file window.** Edge SQLDATE days whose eligible file-date
coverage would require a file **outside** the window are **not** fully covered and must **not**
silently enter the primary archive as if comparable to interior days. (This sits cleanly alongside
§6: a bucket may be *eligible by rule* yet *unavailable for an edge day* because the required file
is outside the authorized window.)

**2023+ seal is absolute.**
- Never fetch / enumerate / open / read `2023-01-01` or any later file to complete any `t`.
- The 2023+ seal is **never** relaxed for edge coverage.

**Pre-window files are not read.**
- Never fetch / enumerate / open / read `2013-03-31` or any earlier file to complete the start
  boundary of the primary in-sample archive.

**End-boundary consequence.** `SQLDATE = 2022-12-31` is **not fully covered** for the primary
no-lookahead predictor archive, because its eligible `offset −1` contribution would require file
`F = 2023-01-01`, which is **sealed**. It must therefore be **excluded from the primary
no-lookahead predictor archive** — or routed to a separately governed edge-incomplete diagnostic
set — never silently included as comparable to interior days, and never completed by reading the
sealed `2023-01-01` file.

**Start-boundary consequence.** Analogously, start-of-window SQLDATE days whose eligible `offset +1`
coverage would require a pre-window file — e.g. `SQLDATE = 2013-04-01`, whose `offset +1`
contribution would sit in file `F = 2013-03-31` — are **not fully covered** and must likewise be
**excluded** from the primary no-lookahead predictor archive (or flagged/routed as edge-incomplete),
never completed by reading a pre-window file. (The rule is stated structurally so it holds for any
edge day regardless of which eligible buckets it actually has.)

**Scale note.** This trims only the window edges: the end-trim bites at `2022-12-31`
(`t+1 = 2023-01-01`, sealed) and the start-trim bites where an eligible `+1` contribution would
require a pre-window file (e.g. `2013-04-01`). The intent is not to lose many days, but to prevent
silently retaining edge days built under a different coverage rule than interior days.

**Reporting (value-blind).** Edge exclusions may be reported as **structural counts/status only**
(e.g. number of edge-incomplete SQLDATE days excluded or routed); **no** value summaries of
`QuadClass` / `GoldsteinScale` / `AvgTone` / `NumMentions`; **no** sample rows.

**Predictor-side only.** This section constrains predictor-side window coverage only. Outcome-side
R1 / `civil_date + 1` anchoring is **unchanged**; the GDELT 1.0 codebook/index reference is
**unchanged**; the core `file_date <= SQLDATE + 1` rule (§6) and the five-field retained schema are
**unchanged**.

**Phase 2 implementation/tests must prove (on synthetic fixtures, before any real fetch):**
- no `2023-01-01`-or-later file is opened to complete an edge day;
- no pre-window (`2013-03-31`-or-earlier) file is opened to complete an edge day;
- edge-incomplete days are **not** silently written into the primary no-lookahead predictor archive;
- edge counts/status are **structural-only** (no value summaries, no sample rows).

**Non-authorization preserved.** This section authorizes **no network, no archive execution, no
extraction, no join, and no data read**; it only constrains predictor-side window coverage.

## 8. Preferred availability instrument: file/update date

- The **preferred and selected** availability instrument is the **file/update date derived from
  the source filename / source URL** (e.g. `YYYYMMDD.export.CSV`), per `8fdf233` §F's
  "use the GDELT update-file date as the availability stamp."
- It is **structural provenance metadata already known** from the source URL / enumeration
  universe — known per file **before** any content-row parse.
- It is per-file; the eligibility check `F <= SQLDATE + 1` is computed per row using the
  already-known `F` and the parsed `SQLDATE`.

## 9. DATEADDED handling

- `DATEADDED` (codebook reference Python index 56) is **not** used as the availability instrument
  here. It remains classified **forbidden / management metadata**.
- `DATEADDED` is **not retained** in the Phase 2 archive and is **not** parsed for retention.
- Adopting or retaining `DATEADDED` (transiently or persistently) would require a **separate,
  explicit design amendment**, because it reopens the locked five-field approved set; it is **not**
  authorized by this memo.

## 10. Archive schema implication

- The Phase 2 archive's **retained row schema remains the five approved fields**: `sqldate`,
  `quadclass`, `goldsteinscale`, `nummentions`, `avgtone`.
- File/update date may be recorded **at per-file manifest / status level** as structural
  provenance metadata (it is already known from the source URL).
- **Per-row retention** of file/update date is **not authorized** by this memo. If a future design
  needs a per-row availability stamp (e.g. to support the separately governed late-arrival
  archive), it requires a **later schema/design amendment** with its own justification; it must
  not be added under this amendment.
- The eligibility rule itself needs **no additional retained field**: `F` is used as a build-time
  gate, not written into the row.

## 11. Value-blind reporting

Availability validation and build-time reporting must be **value-blind**:
- report structural counts/status only: number of **eligible** rows, number of **excluded
  late-arriving** rows;
- **counts by offset bucket** are permitted **only** as structural availability metadata;
- **no** value summaries of `QuadClass` / `GoldsteinScale` / `AvgTone` / `NumMentions`;
- **no** sample rows.

## 12. Existing substrate / Step-2 implication

- The existing **Option-B count substrate** (`build_daily_counts.csv`) and the **Step-2 daily
  features** derived from it **are not valid no-lookahead predictors**, because they fold
  late-arriving lookback contributions into each day-`t` aggregate.
- They remain **historical artifacts only**. They must **not** be used as governing no-lookahead
  predictors **without a rebuild** under the amended `F <= SQLDATE + 1` eligibility rule.
- Any future no-lookahead predictor must be (re)built under this rule; existing tracked/generated
  count outputs do not satisfy it.

## 13. Relationship to outcome-side R1

- Outcome-side **R1 / `civil_date + 1`** anchoring (`df9089b` §4.3, `bc3b9c0`) is **unchanged**.
- This amendment affects **predictor eligibility only**; it does not alter the outcome anchor,
  the `m = civil_date + 1` max-info boundary, the close-to-close basis, or RV alignment.
- The two are complementary: outcome-side R1 keeps the outcome strictly after `t + 1`; this
  amendment keeps the predictor built only from information available by `t + 1`.

## 14. Relationship to codebook/index reference

- The GDELT 1.0 Event **codebook reference** (`docs/lane2_gdelt1_event_codebook_reference_v0.1.md`,
  329 lines, SHA-256 `3c5fa5bc054fbefaea2a26f9700ee827f2ff86a059d1625ffa127b10bf035a58`) remains
  **valid and unaffected**.
- The **codebook/index prerequisite remains resolved**; this amendment resolves the **separate**
  availability-timing prerequisite the codebook reference explicitly carried forward (its §10
  caveat).

## 15. Phase 2 implementation requirements

A future Phase 2 archive-build authorization and implementation must:
1. Re-verify codebook indices against the codebook reference (SHA-256 above).
2. Enforce **`file_date <= SQLDATE + 1`** per retained row **before** writing the archive row.
3. Sequence per row: parse `SQLDATE`; obtain file/update date `F` (known from source); check
   `F <= SQLDATE + 1`; **only then** write the row to the no-lookahead archive.
4. Exclude (or route to a separately governed late-arrival archive) every ineligible
   late-arriving row; never fold it into the day-`t` predictor.
5. Keep the retained row schema to the five approved fields; record `F` only at per-file
   manifest/status level (no per-row retention without a later amendment).
6. Report structural counts/status only (eligible / excluded / per-offset-bucket counts);
   no value summaries; no sample rows.
7. Preserve the 2023+ seal before any content-row read.
8. **Prove this rule using synthetic fixtures before any real fetch** — Phase 2 code/tests must
   demonstrate, on synthetic data, that eligible rows are written, late-arriving rows are
   excluded/routed, and the build hard-errors or routes to design review when the rule cannot be
   satisfied — prior to any network/GDELT event-data contact.
9. Compute no TTG features/statistics during the archive-build phase.

## 16. Stop conditions

- If, during an authorized Phase 2 build, the file/update date for any file cannot be determined
  to exactness, **BLOCK / route to design review** (cannot evaluate eligibility).
- If a row's `SQLDATE = t` is present only in files dated later than `t + 1` and no separately
  governed late-arrival archive is authorized, **exclude it from the day-`t` predictor**; do not
  fold it in.
- If a per-row availability stamp turns out to be required, **BLOCK** and require a later
  schema/design amendment before retaining it.
- If `DATEADDED` use is proposed, **BLOCK** and require a separate amendment (forbidden/management
  metadata under the current lock).

## 17. Boundaries not authorized

This amendment authorizes **none** of the following, each firewalled behind its own separate gate:
- GDELT network / event-data fetch; contact with `data.gdeltproject.org/events/`; any
  `.export.CSV.zip` or event index/listing;
- Phase 2 local archive build / execution;
- TTG extraction (design, execution, or authorization);
- outcome-side join (authorization or execution);
- any read of raw event data, result-file contents, market data, outcomes, joined data,
  `next_session_return`, or `abs_next`;
- unsealing or reading 2023+ data;
- retaining `DATEADDED` or any per-row availability field;
- V1/V2 execution.

Phase 2 archive-build authorization remains **blocked** until this amendment is committed and then
**enforced in code/tests**.

## 18. Boundary confirmation

Design-only amendment produced from committed-doc/source bytes and git metadata. No network
contact; no GDELT contact; no event-data contact; no event index contact; no `.export.CSV.zip`
contact; no archive execution; no archive authorization; no TTG extraction authorization; no TTG
extraction execution; no join authorization; no join execution; no raw-event data read; no
result-file content read; no CSV content read; no market-data read; no outcome read; no
joined-data read; no `next_session_return` read; no `abs_next` read; no tests; no V1/V2 execution;
no 2023+ real data. This memo is design-only and authorizes nothing beyond recording the amended
predictor-availability rule.
