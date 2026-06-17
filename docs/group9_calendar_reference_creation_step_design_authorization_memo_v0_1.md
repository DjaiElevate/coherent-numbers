# Group 9 — Trading-Calendar (Expected-Session) Reference — Creation-Step Design & Authorization Memo (v0.1)

**Status:** Design / authorization only. This memo specifies and authorizes the posture and acceptance criteria for a later, separately authorized creation step. It does not select-and-commit a source, does not materialize the session list, does not pin any SHA, and does not run the missing-days check.

## 1. Records & base state

- Base origin/main: ab85a6128e76017e6bb99ac3a3e550484d0cdb5f
- Parent: 6327745765ff15c711060f560d4dceb64fb27023
- Governing freeze design memo: docs/group9_calendar_reference_freeze_design_authorization_memo_v0_1.md, committed blob SHA-256 f8bc8f5ee46abb4a46766cda5ffd6a9ad1fd535dfa6e2825958f50a5f27df74f.
- Class: Group 9 creation-step design / authorization memo.
- This memo is downstream of and bounded by the freeze design memo (ab85a61). Where the freeze memo defined what must be frozen and why it must be independent, this memo defines how the creation step must be conducted and judged — without conducting it.

## 2. Purpose & scope

Define the criteria a later creation step must satisfy to produce and freeze the independent expected-trading-session reference required by the committed missing-days / calendar-handling integrity design memo.

In scope: source-selection criteria; identity-confirmation requirements; half-day handling; unscheduled-closure handling; the fixed observed extent; the target artifact specification; proposed durable paths; SHA-pin discipline; STOP conditions.

Out of scope (not authorized here): selecting-and-committing a specific source; acquiring or materializing the list; pinning a SHA over any list; running the missing-days check; any price-value, OHLCV, CI/CR, feature, wake/outcome/target, or Gate 2 work; alpha spend; sealed-data access; any change to atlas status, CR closure, or Gate 1.

## 3. Source-selection criteria (independent expected-session source)

The creation step must select exactly one source that meets all of the following:

1. Independence. The source must be independent of the SPY sandbox date index. It must not be derived from, seeded by, joined to, or validated against the sandbox's own dates — that is the circularity the reference exists to break (freeze memo §2, §5).
2. Applicable identity. It must represent the NYSE Group U.S. cash-equity regular session calendar applicable to SPY / NYSE Arca equities (the XNYS regular session calendar), expressed exchange-local (America/New_York). Not a generic "US holidays" list; not a futures or other-venue calendar.
3. Full-window coverage. It must produce every regular session over the fixed observed extent 2005-01-03 … 2022-12-30 inclusive (§7 below).
4. Closure fidelity. It must reflect actual market closures, including unscheduled full-market closures (§6), not a naive "weekdays minus fixed holidays" rule.
5. Materializable & reproducible. It must be capable of producing a concrete, date-level session list that can be written to durable bytes and reproduced, with a recordable provenance identity (e.g., library name + version, or the exchange schedule's publication identity).

Candidate sources to evaluate (informational, not a selection): an established exchange-calendar library that materializes the XNYS regular session calendar, or the exchange's own published holiday/early-close schedule reconciled into a session list. Whichever is evaluated, §4 identity confirmation and §5/§6 handling checks gate its acceptance.

## 4. Identity-confirmation requirements

Before any output from the chosen source is trusted, the creation step must confirm and record:

- that the source is unambiguously the NYSE / XNYS regular equities session calendar (vs. a generic holiday list, a futures calendar, or a different venue/instrument);
- if an XNYS library calendar is used, that its date-level session presence is equivalent for SPY / NYSE Arca equities over 2005-01-03 … 2022-12-30 (the wording fixed in freeze memo §4);
- the exchange-local timezone basis (America/New_York), so that session dates are calendar dates, not UTC-shifted timestamps.

Identity that cannot be confirmed is a fatal STOP (§11), not a thing to paper over.

## 5. Half-day-as-session handling

- Half-days are sessions. Early-close days (e.g., the day after Thanksgiving; certain Christmas-Eve / July-3 eves) are included, because SPY trades and has a close on those days.
- The reference is a session-presence calendar: it records whether a date is a trading session at date-level. It does not distinguish full from half sessions, and must not drop a date merely because it is an early close.
- The creation step must report (provenance note, §9) the half-day handling actually applied by the chosen source.

## 6. Unscheduled full-market closure handling

- Unscheduled full-market closures must be represented as non-sessions by the source.
- A naive "weekdays minus fixed holidays" list is insufficient and is grounds for rejecting a source.
- Cross-check (illustrative, secondhand, NOT authoritative): within the window, the unscheduled / extra closures to watch for are the Gerald Ford national day of mourning (2007-01-02), Hurricane Sandy (2012-10-29 and 2012-10-30), and the George H. W. Bush national day of mourning (2018-12-05). This list exists only to catch a source that silently misses unscheduled closures; the chosen source — not this list — is authoritative on the actual sessions. The creation step records which unscheduled-closure dates the source included/excluded and on what basis.

## 7. Observed extent (fixed)

- The materialized expected-session list covers the observed sandbox extent 2005-01-03 … 2022-12-30 inclusive, matching the committed sandbox inventory (Atlas §6.1; freeze memo §3). The narrower observed extent — not the filename's nominal 20050101_20221231 — is the boundary, to avoid false boundary anomalies in the downstream check.
- Both endpoints 2005-01-03 and 2022-12-30 are expected to be genuine sessions bounding the list inclusively; this must be verified against the source, not asserted.
- Any expected date outside this window is a fatal STOP (§11). A broader span is permitted only under an explicit, separately justified amendment.

## 8. Target artifact specification

The creation step, once separately authorized, produces:

- a materialized list of expected sessions, one canonical field — the session date in ISO 8601 YYYY-MM-DD, exchange-local;
- date-level only: no price values, no OHLCV, no intraday times beyond what is internally required to decide that a date is a session;
- sorted strictly ascending, unique, no duplicates;
- stored durably as committed bytes in the repo (§9);
- accompanied by a provenance / SHA-pin note (§9).

## 9. Proposed durable paths

Proposed, pending confirmation at execution time that the chosen location is tracked (not gitignored) — this matters because data/raw/ is gitignored, which is exactly why the sandbox CSV is not a tracked file:

- Materialized session list (proposed): data/reference/nyse_xnys_expected_sessions_20050103_20221230.csv
  - The creation step must verify this path is not under a gitignore rule; if it is, choose a tracked location (e.g., a reference/ tree) so the list is durably committed, mirroring the repo's name-stamped-SHA filename convention if desired (e.g., appending the content SHA to the filename after materialization).
- Provenance / SHA-pin note (proposed): docs/group9_calendar_reference_provenance_note_v0_1.md
  - Records: chosen source and its identity/version; the exact selection rule; timezone basis; half-day handling applied; the unscheduled-closure dates included/excluded and the basis; endpoint inclusivity at both bounds; and the SHA-256 of the materialized list bytes (the pin of record).

Both files are committed in the same single-purpose creation commit at execution time.

## 10. SHA-pin discipline (binding)

- The pin of record is the SHA-256 over the materialized date-list bytes — the actual file of session dates.
- A package name + version is provenance only, never the pin. Library calendar data can change across versions and updates; recording only "library X vX.Y" would not freeze anything. The frozen bytes are the reference; the package/schedule identity is recorded as how those bytes were produced.

## 11. Fatal STOP conditions before / at creation (in order)

STOP means STOP — no silent substitution, regeneration, or "find another source" without separate authorization:

1. Source unavailable — the chosen NYSE / XNYS source cannot be obtained or reached.
2. Ambiguous calendar identity — cannot confirm the source is the NYSE / XNYS regular equities session calendar (§4).
3. Extent violation — any expected date falls outside 2005-01-03 … 2022-12-30 (broader span only under explicit separate justification).
4. Duplicate expected dates in the materialized output.
5. Unsorted expected dates in the materialized output.
6. Malformed date format — non-ISO, unparseable, mixed formats, or timezone-ambiguous entries.
7. Untracked storage path — the chosen list path is gitignored / not durably committable (would defeat the freeze).
8. Failure to SHA-pin the materialized output bytes — no recorded SHA-256 over the frozen list.

Survey-and-report (not fatal, but must appear in the provenance note, never silently resolved): the half-day handling actually applied; the specific unscheduled-closure dates the source included/excluded and its basis; endpoint inclusivity at both bounds.

## 12. What the creation step produces vs. does not

Produces (only when separately authorized): a frozen, SHA-pinned, sorted, unique, in-window expected-session date list, plus the provenance / SHA-pin note (§9).

Does not: read any price value cell; read OHLCV; compute CI / CR; compute features; compute wake / outcome / target; open Gate 2; spend alpha; access sealed data; run the missing-days check; or modify atlas status, CR closure, or Gate 1.

## 13. Dependency clearance & gating

- On successful creation against this design, the missing-days / calendar-handling memo's open prerequisites #1 (no frozen expected-session reference), #2 (circularity), and #6 (package-version insufficiency) are cleared, and the freeze design memo's §10 items #1–#5 are resolved.
- Prerequisites #3 (sandbox is gitignored — must be present and SHA-matching 5cd92502… at run time), #4 (observed-span scoping), and #5 (schema-freeze decision) remain independent and are not addressed here.
- The missing-days check becomes runnable only after the reference is frozen and a separate run-authorization turn is issued. This memo does not authorize that run.

## 14. Explicit non-authorizations

This memo authorizes nothing operational. It does not authorize: selecting-and-committing a source; acquiring data; materializing or committing the calendar list; pinning a SHA over any list; running the missing-days check; any price-value, OHLCV, feature, CI / CR, wake / outcome / target, or Gate 2 work; alpha spend; sealed-data access; or any change to atlas status, CR closure, or Gate 1.

## 15. Open items to confirm at execution-authorization time

1. The specific source selected and its confirmed XNYS regular-session identity (§3, §4).
2. The source's half-day and unscheduled-closure handling, verified against §5/§6 (cross-check list is a tripwire, not the authority).
3. The final tracked storage path for the materialized list (gitignore-verified) and the provenance-note path (§9).
4. Endpoint inclusivity at 2005-01-03 and 2022-12-30 per the source (§7).
5. The recorded SHA-256 over the materialized bytes as the pin of record (§10).
