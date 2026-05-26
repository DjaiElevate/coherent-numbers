# Lane 2 GDELT1 sentinel-SQLDATE substrate amendment memo v0.1

**Status:** draft memo. Memo-only. Authorizes no runner edit, no chunk rerun, no
chunk_2019 retry, no merge, no memory update, no Step 2, no market-data work,
no instrument construction. The recommended remediation design is named and
explained here so a separately authorized implementation prompt can act on it;
this memo itself is not such an authorization.

| Anchor | Value |
|---|---|
| Current HEAD | `3595466a1934b20c85c264451824e42bf1e374ad` |
| origin/main | `3595466a1934b20c85c264451824e42bf1e374ad` |
| ahead/behind | 0 0 |
| Predecessor memo | `a8a9dd2` — `docs/lane2_gdelt1_row_date_mismatch_substrate_validation_memo_v0.1.md` (the F4 memo) |
| Locked runner reference | `389747e` — `scripts/run_lane2_gdelt1_full_daily_count_build.py` (byte-identical, all 5 guards `False`) |
| Halted-attempt archive | `archive/halted_attempts/lane2_gdelt1_full_daily_count_build/chunk_2019_20260525T192552Z/halt_diagnostic.json` (322 B, SHA `3b2b43708d0a7a9410d59a7bfd4deec7fef84f8a6543472f25942e67e1058005`) |
| Substrate research chain | Prompt A (in-session, no commit) → Prompt B (in-session, no commit) → Prompt C (in-session, no commit) |

## 1. Purpose and scope

This memo formalizes the substrate-level interpretation of the chunk_2019
live-execution halt event of 2026-05-25 (`HALTED — CHUNK_2019 LIVE RUN FAILED
AFTER START WITH GUARD RESTORED`) and consolidates the Prompt A / Prompt B /
Prompt C substrate-research findings into a locked substrate interpretation
plus a remediation-design rationale.

**In scope:** substrate taxonomy refinement; recognition of a new
sentinel-SQLDATE subclass; rationale for selecting remediation family R3
(hybrid: `EXPECTED_OFFSETS` retained for non-sentinel rows, explicit
`SENTINEL_SQLDATES` for placeholder dates, halt preserved for other unexpected
offsets); attribution-policy lock recommendation (Option α); formalization of
the inspection-contact discipline used in the research chain.

**Out of scope:** runner code amendment, runner code edits, line-level patch
guidance, implementation sequencing, chunk_2019 retry, chunks 2020-2022,
merge, Step 2, market-data work, instrument construction, environment-variable
authorization, guard flips, and any production GDELT contact through the
locked runner path.

## 2. Historical lineage from F4

The F4 memo (`a8a9dd2`,
`docs/lane2_gdelt1_row_date_mismatch_substrate_validation_memo_v0.1.md`)
established the offset-bucket convention for GDELT 1.0 daily-export files —
that rows in a `YYYYMMDD.export.CSV.zip` file are not single-date row
collections but a structured set of lookback offsets relative to the file's
nominal date — and recorded the **REKEY-BY-SQLDATE-CANDIDATE** primary
decision.

The F4 memo §5 limitation list explicitly noted that the offset taxonomy
`{−3650, −365, −30, −7, −1, 0, (+1)}` was **consistent across 5 inspected
files but not proven exhaustive**, and §6 explicitly chose
`REKEY-BY-SQLDATE-CANDIDATE` (not `LOCKED`) for that reason. The full-build
runner committed under reference SHA `389747e` enforces the
`EXPECTED_OFFSETS` taxonomy in `parse_payload` and raises
`FullBuildBoundaryBreach` on any row whose offset is not in that set. This
strict guard is the load-bearing implementation of the F4 "not-locked"
caveat: any future row that violates the taxonomy halts the build rather than
being silently incorporated.

This memo updates that posture in light of the chunk_2019 halt — the **first
observed exercise of that guard against real substrate data across all six
completed prior chunks** (2013_partial / 2014 / 2015 / 2016 / 2017 / 2018) and
into chunk_2019 (364 of 365 files processed before halt).

## 3. Prompt A findings

The halt diagnostic recorded:

```
{
  "actual_completed_file_count": 364,
  "chunk_id": "chunk_2019",
  "halt_class": "FullBuildBoundaryBreach",
  "halted_at_utc": "2026-05-25T19:40:50.998922+00:00",
  "message": "unexpected offset -36524 in payload nominally dated 2019-12-31: SQLDATE 1920-01-01",
  "started_at_utc": "2026-05-25T19:25:52.538065+00:00"
}
```

Prompt A performed a read-only inspection fetch of
`http://data.gdeltproject.org/events/20191231.export.CSV.zip` (HTTP 200,
8,108,775 B, outer-zip SHA-256
`8017ad3872fc0b137384a2c6f92bd8367372c1b4530407dd6627fbb2baa67056`) into a
`/tmp` scratch location, decompressed in memory, and observed:

- **120 rows** in the 2019-12-31 file (`125,858` total non-empty rows) have
  `SQLDATE = 1920-01-01`, giving the offset `(1920-01-01) − (2019-12-31) =
  −36524` days. The arithmetic is correct (100 years − 1 day = 36,524 days).
- Each affected row has the canonical GDELT 1.0 column count (58 columns).
- For each affected row, the four date-related columns (`SQLDATE`,
  `MonthYear`, `Year`, `FractionDate`) are **internally self-consistent at
  1920-01-01**.
- `GLOBALEVENTID` values for the 120 affected rows fall in the same
  ~895-million range as all other rows in the 2019-12-31 file
  (offending range `895,866,098 – 895,939,206`; sample non-offending GEIDs at
  indices 0/100/1k/10k/100k: `895,862,728`/`895,862,828`/`895,863,728`
  /`895,875,384`/`896,011,914`).
- `SOURCEURL` values for the 120 affected rows are uniformly **modern 2019
  articles** (samples include articles about Greta Thunberg, the Carlos Ghosn
  Lebanon escape, John McIntire library events, Tanzania's Yanga signing a
  player, etc.).
- Rows immediately surrounding each affected row are structurally normal
  (58-column GDELT rows with in-taxonomy SQLDATEs and modern URLs).
- `unparseable_sqldate_rows = 0`; `malformed_short_rows = 0` for the full
  2019-12-31 file.

**Parser corruption was ruled out** because: (i) the column count is correct,
(ii) the four date-related columns are internally consistent at 1920-01-01
(not consistent with a one-column shift or one-byte slice misalignment),
(iii) the actor codes are valid GDELT codes, (iv) the source URLs and
GEIDs are clearly modern, and (v) surrounding rows are unaffected.

The interpretation supported by this evidence is that **the substrate (the
GDELT 1.0 daily-export file content itself) contained 120 rows with the
SQLDATE field populated with the value `19200101`**, irrespective of how the
runner read them. The rows are well-formed GDELT 1.0 rows with a deep-past
SQLDATE.

## 4. Prompt B findings

Prompt B did a zero-fetch scan of all 6 Prompt A cached files plus a 6-fetch
within-2019 sample (`2019-01-31` / `2019-03-31` / `2019-06-30` / `2019-09-30`
/ `2019-11-30` / `2019-12-30`).

- Across all 6 prior year-end files (2014-12-31 through 2018-12-31) the SQLDATE
  `1920-01-01` does not appear; out-of-taxonomy offset count is 0; no other
  named-sentinel candidates appear; `malformed_short = malformed_sqldate =
  blank_sqldate = 0`.
- Across the 6 within-2019 sampled dates the SQLDATE `1920-01-01` does not
  appear; out-of-taxonomy offset count is 0; in-taxonomy distributions are
  canonical (T=0 dominant; T−1/T−7/T−30/T−365/T−3650 present in usual
  magnitudes; T+1 absent throughout — consistent with the F4 memo's
  observation that T+1 disappeared from GDELT 1.0 sometime between
  2014-01-26 and 2018-02-14).
- By negative inference from the halt diagnostic's
  `actual_completed_file_count = 364`, the chunk_2019 runner processed all
  364 chunk_2019 days preceding 2019-12-31 without raising
  `FullBuildBoundaryBreach`, which implies **none of those 364 days contained
  any out-of-taxonomy offset**. This is independent of which 6 specific
  within-2019 days Prompt B sampled.

Prompt B classified the observed evidence as **S1 — single sentinel value
only**, with high confidence that within 2019 the pattern is **sharply
localized to 2019-12-31**. Prompt B identified R3 (hybrid) as the strongest
remediation family but flagged that the absence of a forward-window sample
(2020-2022) left R4 (more research first) as a defensible alternative.

## 5. Prompt C findings

Prompt C addressed the forward-window question and re-tested 2019-12-31
reproducibility.

- **2019-12-31 reproducibility:** Re-fetching
  `http://data.gdeltproject.org/events/20191231.export.CSV.zip` returned an
  outer ZIP with SHA-256
  `8017ad3872fc0b137384a2c6f92bd8367372c1b4530407dd6627fbb2baa67056` — byte-
  for-byte identical to Prompt A. The 2019-12-31 file is stable on the GDELT
  server across the inter-prompt interval. Row-level findings therefore hold
  without re-decompression.
- **2020-12-31 / 2021-12-31 / 2022-12-31 year-end fetches:** all HTTP 200; all
  three files clean — `total_rows` 100,226 / 74,765 / 56,040; `OOT total = 0`
  for each; `SQLDATE 1920-01-01 = 0` for each; no other named sentinel
  candidates; `malformed_short = malformed_sqldate = blank_sqldate = 0`;
  in-taxonomy distributions canonical with T+1 absent throughout.
- Task D optional-extension trigger conditions did **not** fire on any of
  the 3 year-end files; no within-year 2020/2021/2022 dates were sampled in
  Prompt C.

Prompt C classified the temporal pattern as **T1 — one-off isolated
anomaly. 2019-12-31 uniquely affected.** The forward-window absence
strongly contradicts T3 (expanding/leading-edge process) — a leading-edge
process would have intensified in 2020/2021/2022 rather than disappearing
entirely.

Aggregate evidence after Prompts A/B/C: 15 distinct GDELT 1.0 daily-export
files inspected (6 Prompt A year-ends + 6 Prompt B within-2019 + 4 Prompt C
of which 1 is the 2019-12-31 reproducibility re-fetch, deduplicating to 3
new files; net 15 distinct). **One file contains the pattern; 14 do not.**
Plus the 364 non-halting in-run chunk_2019 days inferred from the halt
diagnostic.

## 6. Substrate anomaly taxonomy refinement

The substrate exhibits three conceptually distinct anomaly classes. The F4
memo named one class (fetch-gap) and implicitly handled a second
(lookback retrocoding) through `EXPECTED_OFFSETS`. The chunk_2019 evidence
forces explicit recognition of a third class.

| Class | Description | F4 status | Locked-runner status | Prompt A/B/C status |
|---|---|---|---|---|
| Fetch-gap anomalies | A GDELT daily-export file does not exist on the server for a given date (HTTP 404 / absent). Currently four known dates: 2014-01-23, 2014-01-24, 2014-01-25, 2014-03-19. | Named and characterized | `KNOWN_SUBSTRATE_GAPS` constant; excluded from `fetch_set`; fourth-empirically-validated across closed chunks 2015/16/17/18 | Reaffirmed; no change |
| Lookback retrocoding | A row's SQLDATE is an earlier real event date than the file's nominal date, at one of the structured lookback offsets `{−3650, −365, −30, −7, −1, 0, (+1)}`. | Named and characterized (5-file sample); offset set noted as not-yet-exhaustive | `EXPECTED_OFFSETS` constant; `FullBuildBoundaryBreach` on offsets outside the set | Reaffirmed; the 7-element offset set holds across 15 inspected files for **non-sentinel** rows |
| **Sentinel-placeholder rows** | A row's SQLDATE is set to a fixed sentinel-like value (`1920-01-01` in the observed evidence) that is not the row's actual event date. Surrounding row content (URL, GEID, actor codes) indicates a modern event. | Not anticipated by name | Currently halts (caught as out-of-taxonomy offset) | Newly named here |

The new class is conceptually distinct from lookback retrocoding because the
substrate does not encode an earlier-but-real event date — it encodes a
**placeholder** that happens to parse as a deep-past date. Treating sentinel
rows as if they were a deeper-lookback retrocoding bucket would misattribute
modern events to a fictional 100-year-back event date.

## 7. Sentinel SQLDATE subclass definition

A row is in the **sentinel-SQLDATE subclass** when:

- the row is structurally well-formed (canonical column count; the four
  date-related columns parse internally consistent values),
- the parsed SQLDATE equals a value in a designated `SENTINEL_SQLDATES` set,
- and no other anomaly is present (no column shift, no encoding drift, no
  surrounding-row corruption).

Based on the Prompts A/B/C evidence, the `SENTINEL_SQLDATES` set is
recommended to be seeded as exactly:

```
SENTINEL_SQLDATES = (date(1920, 1, 1),)
```

— **narrow now** (only the observed value), **extensible in shape** (a tuple
that can be extended to additional sentinel values if observed in future
substrate research), and **not over-generalized** (no speculative inclusion
of unobserved candidates such as `1900-01-01`, `1970-01-01`, `9999-12-31`,
etc., which would re-introduce the over-tolerance failure mode discussed
below).

**Wording discipline applied:** the substrate evidence is consistent with a
sentinel-placeholder interpretation. The memo does not assert as fact that
the GDELT publishing pipeline definitively uses `1920-01-01` for any
specific upstream cause (e.g., undateable articles, malformed parser input,
missing date metadata, batch-default insertion, or any other GDELT-internal
mechanism). The cause is treated as inferred but not directly documented.

## 8. Discovery-property rationale

The `FullBuildBoundaryBreach` halt on any unexpected offset is the
runner's discovery-preservation property: it ensures that **any future
substrate pattern not previously observed and characterized halts the build
rather than being silently incorporated**.

This property is load-bearing for the following reasons:

- It correctly caught the 2019-12-31 sentinel pattern that had not been
  observed in F4's 5-file sample or in any of the 6 prior completed chunks.
- Without it, the 120 affected rows would have been silently attributed to
  either the nominal file date (under publish-date attribution) or the
  SQLDATE `1920-01-01` (under `REKEY-BY-SQLDATE`), and the substrate property
  change would not have been surfaced.
- The downstream attention-count series and any later interpretive layer
  would inherit unflagged misattribution.

Any remediation that loses this property — e.g., blind widening of
`EXPECTED_OFFSETS` to include `−36524` — would compromise the runner's
ability to surface the *next* novel substrate pattern. The recommended
remediation preserves the property.

## 9. Remediation-family comparison (R1 / R2 / R3 / R4)

| Family | Description | Verdict | Reason |
|---|---|---|---|
| **R1** — blind widening | Add `−36524` (or a broader long-range neighbor offset) to `EXPECTED_OFFSETS`; no sentinel concept. | **Rejected.** | Attributes sentinel-placeholder rows to a fictional "100-year lookback" semantic; loses discovery property; re-creates the over-tolerance failure mode that the F4 "not-locked" caveat was designed to prevent. |
| **R2** — sentinel-only, narrow | Add `SENTINEL_SQLDATES = (date(1920,1,1),)`; remove the halt on `−36524` only; no broader retention of halt-on-other-unexpected. | **Defensible but dominated by R3.** | Solves the immediate 2019-12-31 case but, if interpreted as removing the halt-on-other-unexpected behavior, would silently lose the discovery property for future novel patterns. |
| **R3** — hybrid (recommended) | Retain `EXPECTED_OFFSETS` for non-sentinel rows; add explicit `SENTINEL_SQLDATES` for placeholder dates; preserve halt-on-other-unexpected for any non-sentinel offset outside `EXPECTED_OFFSETS`. | **Recommended.** | Solves the 2019-12-31 case with the narrowest tolerance change; preserves discovery property; cleanly separates conceptually distinct row classes (sentinel placeholders ≠ lookback retrocoding); compatible with the F4 `REKEY-BY-SQLDATE-CANDIDATE` principle for non-sentinel rows. |
| **R4** — more research first | Defer remediation pending wider substrate sampling. | **Lower-priority after Prompt C.** | The two specific gaps R4 was designed to close — (i) within-2019 distribution (Prompt B) and (ii) 2020-2022 forward extension (Prompt C) — are now addressed at the year-end granularity. Diminishing returns from further sampling before locking R3. R4 remains a valid alternative if additional confidence is desired (e.g., within-year sampling for 2020/21/22). |

## 10. Attribution-policy analysis (Option α / β / γ)

For rows recognized as `SENTINEL_SQLDATES` members, three attribution
policies are conceptually available:

| Option | Policy | Numerical impact on chunk_2019 (estimate based on observed 120 sentinel rows out of expected ~60-70M in-window rows) | Semantic property |
|---|---|---|---|
| **α** | Exclude from primary `total_in_window_rows` and `total_out_of_window_rows`; record only in a separate per-sentinel diagnostic counter. | ≈ 2 ppm impact on aggregate row totals; sentinel rows do not enter the attention-count series | Aligns with the F4 `REKEY-BY-SQLDATE-CANDIDATE` principle: a sentinel SQLDATE is not a meaningful event date, so it should not flow into the SQLDATE-attributed attention-count series. |
| β | Attribute sentinel rows to the nominal file date (publish-date attribution). | Same ≈ 2 ppm impact, contributing to the T=0 / nominal-day count | Pragmatically preserves aggregate row totals exactly; loses the SQLDATE-rekey principle for this row class. |
| γ | Attribute to the sentinel SQLDATE itself (here, 1920-01-01) and treat as a separate diagnostic time series. | Produces a tiny 1920-01-01 spike with no real-world interpretation | Technically faithful to the on-disk SQLDATE value; but creates a diagnostic time series that is downstream-meaningless because the SQLDATE has no event-time semantic. |

**Recommendation: Option α** (exclude from primary aggregates; record only in
per-sentinel diagnostic counter). Rationale: cleanest semantic given the
F4 `REKEY-BY-SQLDATE-CANDIDATE` principle; numerically negligible
contribution either way given the 0.0954% within-affected-file prevalence
and the 2 ppm chunk-level prevalence; preserves the meaningfulness of the
attention-count series.

**Attribution policy is a memo-level semantic choice, not a parser fix.**
The runner's parser correctly extracts the SQLDATE in all options; the
choice is about how to attribute the row to the downstream aggregates and
diagnostics. Locking this choice is a memo decision and should not be
deferred to implementation.

## 11. Recommended substrate interpretation

The interpretation locked by this memo:

1. The 2019-12-31 GDELT 1.0 daily-export file contains 120 rows whose
   SQLDATE field equals `1920-01-01`.
2. Those 120 rows are structurally well-formed GDELT 1.0 rows whose other
   columns (URLs, GEIDs, actor codes, internally consistent date columns)
   indicate modern (2019) events.
3. The observed pattern is **consistent with a sentinel-placeholder
   interpretation** of the SQLDATE field for those specific rows. The
   upstream cause inside the GDELT publishing pipeline is inferred but not
   directly documented in this memo's evidence base.
4. The pattern is **one-off isolated** within the inspected window
   (2014-12-31 through 2022-12-31 at year-end granularity, plus 6
   within-2019 dates plus the 364 in-run chunk_2019 days from negative
   inference): 1 of 15 inspected files contains the pattern; 14 do not. No
   recurrence after 2019-12-31 was observed at year-end granularity through
   2022.
5. The pattern is **reproducible** (byte-for-byte outer-ZIP SHA match across
   the Prompt A → Prompt C re-fetch interval).
6. The pattern is treated as **bounded, isolated, reproducible,
   non-expanding (within the inspected forward window at year-end
   granularity), and non-generalized (no other sentinel values observed)**.

The chunk_2019 halt is interpreted as a correct runner-side surfacing of a
new substrate subclass that the F4 taxonomy did not anticipate by name, not
as a runner defect, not as a parser bug, and not as a transient delivery
hiccup.

## 12. Recommended runner-side conceptual changes

The conceptual changes needed to implement R3 are described here at the
type-signature and functional-description level only. Implementation
specifics (line numbers, diff-level instructions, exact parse_payload
modification details, code-edit sequencing) are deferred to a separately
authorized runner-amendment prompt.

- **New module-level constant** of type
  `SENTINEL_SQLDATES: Tuple[date, ...] = (date(1920, 1, 1),)` placed near
  `EXPECTED_OFFSETS`, with comment-level documentation pointing to this
  memo and to the chunk_2019 halt diagnostic as the empirical basis.
- **Parser-level distinction**: in the parsing routine that currently
  computes `offset = (d − nominal_date).days` and raises
  `FullBuildBoundaryBreach` on offsets outside `EXPECTED_OFFSETS`, the
  parsed SQLDATE `d` should first be checked for membership in
  `SENTINEL_SQLDATES`; sentinel rows are routed into a separate
  per-sentinel diagnostic counter and do not enter the offset computation.
- **Halt behavior preserved**: non-sentinel rows whose offset is outside
  `EXPECTED_OFFSETS` continue to raise `FullBuildBoundaryBreach`, preserving
  the discovery-preservation property.
- **New diagnostics surfaced**: a `per_sentinel_count` mapping (sentinel
  ISO-date → count) and a `sentinel_sqldate_distribution` mapping (sentinel
  ISO-date → per-nominal-file-date count) reported alongside the existing
  `out_of_window_sqldate_distribution`, `per_offset_total`,
  `total_in_window_rows`, `total_out_of_window_rows`, `total_parsed_rows`
  aggregate metrics.
- **Attribution policy under Option α** (this memo's recommendation):
  sentinel rows are excluded from `total_in_window_rows` and
  `total_out_of_window_rows`; they appear only in the new sentinel
  diagnostics.

No further implementation detail is given here. The runner amendment
prompt, when separately authorized, should derive line-level changes from
the locked runner source at SHA `389747e`, decide test scaffolding, and
sequence enable/restore commits per the established chunk lifecycle.

## 13. Boundaries preserved / invariants under amendment

The proposed R3 design **preserves** every load-bearing invariant currently
asserted by the locked runner and by the prior chunk lifecycle. The
following items must not be weakened by any subsequent implementation:

- **The 7-element `EXPECTED_OFFSETS` taxonomy** `(-3650, -365, -30, -7, -1,
  0, 1)` for non-sentinel rows. R3 does not widen `EXPECTED_OFFSETS`.
- **The halt-on-unknown-offset behavior** for all non-sentinel unexpected
  offsets. `FullBuildBoundaryBreach` continues to fire on any non-sentinel
  SQLDATE whose offset is not in `EXPECTED_OFFSETS`. The discovery-
  preservation property is retained verbatim.
- **The `REKEY-BY-SQLDATE-CANDIDATE` principle** for non-sentinel rows
  (per the F4 memo §6). Sentinel rows are explicitly excluded from the
  rekey because their SQLDATE is not an event date.
- **Runner reference SHA `389747e` remains canonical** for the six already-
  completed chunks (chunk_2013_partial through chunk_2018). The prior
  chunks' outputs and their `chunk_metadata.json` aggregates remain valid
  under the unchanged runner; nothing in this memo invalidates those
  closed cycles.
- **The 7-item non-weakening canon (full list, no weakening permitted)**:
  1. **no-retry**
  2. **exactly-once**
  3. **no-off-session**
  4. **no-market-data**
  5. **no-Step-2**
  6. **no-checkpoint-resume**
  7. **no-bounded-parallelism**
- **The no-2023+ posture**: `SEAL_START = date(2023, 1, 1)` continues to
  hard-fail any 2023+ nominal date or 2023+ SQLDATE row.
- **`KNOWN_SUBSTRATE_GAPS`** `("2014-01-23", "2014-01-24", "2014-01-25",
  "2014-03-19")` remains the canonical fetch-gap set; sentinel handling is
  conceptually separate from fetch-gap handling.
- **All five guards remain `False` in the locked runner** and flip only
  under the established enable-commit / restore-commit lifecycle for an
  explicit single-chunk run.
- **No category / theme / actor / geography / tone filtering** is added.
  Sentinel handling is purely a SQLDATE classification operation.
- **No raw payload preservation** beyond the runner's intended outputs.

## 14. Inspection-contact discipline formalization

The substrate-research chain (Prompts A/B/C) used a new type of GDELT
contact: **inspection contact**. This memo formalizes that discipline so
future substrate research can invoke it under explicit constraints.

**Definition.** Inspection contact is a read-only, scratch-bound,
fetch-budget-capped, prompt-authorized GDELT GET pattern used for
substrate diagnosis, distinct from the production GDELT contact path
(through the locked runner under the three-guard discipline).

**Required properties of an inspection-contact prompt:**

- **Scratch-only fetch destination**: fresh fetches go only to a
  `/tmp/lane2_*_substrate_inspection*/` scratch directory namespace.
  Inspection-contact prompts must not write to `results/`, must not write
  to `archive/`, must not overwrite any canonical artifact, must not write
  any new file under the repo tree.
- **Fetch-budget cap**: each inspection-contact prompt declares an explicit
  upper bound on fresh fetches (e.g., 10 in Prompt B, 8 in Prompt C);
  exceeding the budget triggers a HALT verdict.
- **Single-prompt authorization**: each inspection-contact prompt is
  separately user-initiated and scope-bounded. Inspection contact does not
  authorize itself; production contact through the runner cannot inherit
  inspection-contact authorization.
- **Cached-file reuse preferred**: prior scratch files from earlier
  inspection-contact prompts may be reused for zero-fetch analysis when
  appropriate. Re-fetching for SHA reproducibility verification is allowed
  and counts against the budget.
- **Retention-for-research-cycle-only**: files under
  `/tmp/lane2_*_substrate_inspection*/` may persist under normal ephemeral
  `/tmp` semantics for the duration of the research cycle. They must not
  be committed, must not be archived, and must not be treated as canonical
  artifacts.
- **HTTP-status logging**: every fresh fetch records URL, HTTP status,
  fetched byte size, and SHA-256. Non-200 responses do not trigger retry;
  they are recorded and the prompt continues within budget under a
  partial-completion verdict.
- **No production runner invocation**: inspection contact must not flip
  any guard, must not set any `LANE2_*_AUTHORIZED` env var, and must not
  invoke `scripts/run_lane2_gdelt1_full_daily_count_build.py` or any other
  production runner.

The distinction from production GDELT contact is load-bearing: production
contact through the locked runner produces canonical artifacts under
`results/` that flow into the chunk lifecycle and (eventually) the merge
step; inspection contact does not produce canonical artifacts and is
purely diagnostic.

## 15. Residual uncertainties

Honestly noted:

- **The within-year prevalence of the sentinel pattern in 2020 / 2021 / 2022
  has not been sampled.** Prompt C inspected only year-end files for those
  years. The forward-window evidence is consistent with T1 at year-end
  granularity but does not rule out a sentinel occurrence on some other
  date within 2020/21/22 that a future chunk_2020/21/22 build might surface.
  The runner's discovery-preservation property would catch any such
  occurrence by halting; R3 does not depend on this gap being closed.
- **The upstream cause** of the 2019-12-31 sentinel pattern within the GDELT
  publishing pipeline is not directly documented. The observed evidence is
  consistent with a sentinel-placeholder interpretation but the
  GDELT-internal mechanism (e.g., undateable-article fallback, batch-default
  insertion, parser-input malformation, or another pipeline-level cause) is
  inferred, not observed.
- **The within-2019 finer granularity** outside the 6 sampled dates plus the
  364 in-run chunk_2019 days inferred from `actual_completed_file_count =
  364` is not exhaustively characterized. The available evidence strongly
  supports localization to 2019-12-31 within 2019 but does not prove the
  pattern is exclusively on that date if a future re-run were to surface
  additional occurrences.
- **The offset taxonomy `EXPECTED_OFFSETS`** is reaffirmed for the non-
  sentinel row class across 15 inspected files, but the F4 "not-locked"
  caveat is preserved in spirit: the halt-on-unknown-offset behavior remains
  load-bearing precisely because future substrate evidence may surface
  additional offset cohorts, sentinel values, or other anomaly classes not
  yet observed.
- **The 2019-12-31 cross-clone stability** of the 120 affected rows has not
  been independently verified against an alternative GDELT 1.0 archive
  source (only the canonical `data.gdeltproject.org/events/` host has been
  inspected). The observed reproducibility is across the inter-prompt
  interval on the same source, not across mirrors.

## 16. Non-goals / forbidden inferences

This memo explicitly does **not**:

- Authorize any runner code edit.
- Authorize any chunk_2019 retry.
- Authorize any chunk_2020 / 2021 / 2022 execution or planning.
- Authorize any commit, push, merge, memory edit, archive edit, canonical-
  results edit, market-data work, instrument construction, Step 2 work, or
  guard flip.
- Declare the offset taxonomy "exhaustively proven". The F4 "not-locked"
  caveat is preserved in spirit; R3 adds an explicit sentinel subclass
  rather than declaring exhaustiveness.
- Assert as fact that GDELT definitively uses `1920-01-01` as a sentinel
  for any specific upstream cause. The interpretation is consistent with
  the evidence; the GDELT-internal mechanism is inferred, not documented.
- Generalize the sentinel set beyond the observed value. No other sentinel
  candidates (`1900-01-01`, `1970-01-01`, `9999-12-31`, etc.) are added
  speculatively.
- Modify the existing 7-item non-weakening canon.
- Modify the `KNOWN_SUBSTRATE_GAPS` fetch-gap set.
- Touch the runner reference SHA `389747e`.

## 17. Decision summary

| Item | Decision |
|---|---|
| Substrate model | **S1 — single sentinel value observed** (1920-01-01) |
| Temporal pattern | **T1 — one-off isolated anomaly, 2019-12-31 uniquely affected at year-end granularity** |
| Remediation family | **R3 — hybrid: `EXPECTED_OFFSETS` retained for non-sentinel rows + explicit `SENTINEL_SQLDATES` for placeholder dates + halt preserved for other unexpected offsets** |
| Sentinel set | `SENTINEL_SQLDATES = (date(1920, 1, 1),)` — narrow now, extensible in shape |
| Attribution policy | **Option α** — exclude sentinel rows from primary aggregates; record only in per-sentinel diagnostic counters |
| Runner reference SHA for completed chunks | `389747e` remains canonical and unchanged by this memo |
| Discovery-preservation property | Preserved verbatim |
| 7-item non-weakening canon | Preserved verbatim |
| `KNOWN_SUBSTRATE_GAPS` fetch-gap set | Unchanged |
| Next eligible action | Separately authorized runner-amendment prompt implementing R3 + Option α + new diagnostics, followed by a separately authorized chunk_2019 retry under the established enable / run / restore lifecycle, followed by the chunk_2019 execution-closure memory update |

This memo authorizes none of the above next actions. It only consolidates
the substrate interpretation that justifies them.
