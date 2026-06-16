# Group 9 — Trading-Calendar (Expected-Session) Reference Freeze — Design & Authorization Memo (v0.1)

**Status:** Design / authorization only. Authorizes no creation, no materialization, no data acquisition, and no missing-days run.

## 1. Purpose & scope

This memo defines and authorizes the *design posture* for constructing and freezing an independent expected-trading-session reference over the observed extent of the SPY adjusted-close sandbox date index. It is the design step that a later, separately authorized creation step must satisfy.

Scope is strictly calendar-reference freezing / materialization. It does not cover, design, or authorize the missing-days / calendar-handling integrity run, which remains gated behind its own separate run authorization.

This memo authorizes nothing operational. No source is selected-and-committed here, no list is materialized here, no SHA is pinned here.

## 2. Background & non-circularity rationale

The committed missing-days / calendar-handling integrity design memo is blocked behind the absence of an independent, frozen expected-session reference. The only committed calendar policy (Lane 2 acquisition memo §7) makes the snapshot's own date index the primary calendar; that index cannot serve as the *expected* side of a missing-days comparison, because comparing the observed index against itself is tautological and detects nothing. Atlas §6.9 records that there is no dedicated calendar dataset. An independent reference must therefore be constructed or identified.

"Near-zero contact ≠ no input": even though the integrity check reads only the date column, the expected-session reference is a load-bearing dependency of that check, and its construction is a deliberate data-construction step in its own right.

## 3. Target artifact (what is to be frozen)

The later creation step, once separately authorized, is to produce:

- A materialized list of expected NYSE / ARCA regular trading sessions, expressed as exchange-local calendar dates, covering the observed extent **2005-01-03 … 2022-12-30 inclusive**.
- One canonical field: the session date, ISO 8601 (`YYYY-MM-DD`). No price values, no OHLCV, no intraday times beyond what is internally required to determine that a date is a session. Date-level only.
- Sorted strictly ascending, unique, no duplicates.
- Stored durably (committed file in the repo, or an equivalently durable pinned location) and **SHA-256-pinned over the materialized output bytes** — not over a package name + version.

## 4. Calendar identity & session rules

- **Exchange / calendar identity:** NYSE Group U.S. cash-equity session calendar applicable to SPY / NYSE Arca equities, exchange-local (America/New_York). If an XNYS library calendar is used, the later creation step must document that its date-level session presence is equivalent for SPY / NYSE Arca equities over 2005-01-03 … 2022-12-30. It must be unambiguously this calendar — not a generic "US holidays" list and not a futures or other-venue calendar.
- **Sessions included:** every scheduled regular trading session that is not an exchange holiday.
- **Half-days count as sessions.** Early-close days (e.g., the day after Thanksgiving, and certain Christmas-Eve / July-3 eves) are sessions, because SPY trades and has a close on those days. The reference is a session-presence calendar; it does not distinguish full from half. A half-day is a session.
- **Excluded:** weekends and scheduled exchange holidays.
- **Unscheduled full-market closures must be handled by the reference as non-sessions.** A naive "weekdays minus fixed holidays" calendar is insufficient — the source must reflect actual market closures.

Cross-check (illustrative, secondhand, NOT authoritative — to verify against the chosen source at creation time): within 2005-01-03 … 2022-12-30 the unscheduled / extra closures I am aware of are the Gerald Ford national day of mourning (Jan 2, 2007), Hurricane Sandy (Oct 29–30, 2012), and the George H. W. Bush national day of mourning (Dec 5, 2018). This list is offered only to catch a source that silently misses unscheduled closures; it is not the reference, and the source — not this list — is authoritative on what the sessions are.

Endpoint sanity (also to verify against the source, not to assert from memory): both 2005-01-03 and 2022-12-30 are expected to be real sessions and to bound the list inclusively.

## 5. Independence & non-circularity constraints (binding)

- The expected-session list must be derived from a source independent of the SPY sandbox date index.
- It must not be generated from, seeded by, or validated against the sandbox's own dates. Doing so would reintroduce the tautology the reference exists to break.
- Package name + version is insufficient. Library calendar data can change across versions and updates, so the *materialized session list itself* must be frozen and SHA-pinned. The frozen bytes are the reference of record; the package is merely how they were produced, and its identity/version is recorded as provenance, not as the pin.

## 6. Fatal STOP conditions for the later (separately authorized) creation step

In order. STOP means STOP — no silent substitution, regeneration, or "find another source" without separate authorization:

1. **Source / reference unavailable** — the chosen NYSE / ARCA source cannot be obtained or reached.
2. **Ambiguous calendar identity** — cannot confirm the source is the NYSE / XNYS regular equities session calendar (vs. a generic holiday list, a futures calendar, or a different venue/instrument).
3. **Extent violation** — any expected date falls outside 2005-01-03 … 2022-12-30 (a broader span is permitted only under explicit separate justification).
4. **Duplicate expected dates** in the materialized output.
5. **Unsorted expected dates** in the materialized output.
6. **Malformed date format** — non-ISO, unparseable, mixed formats, or timezone-ambiguous entries.
7. **Failure to SHA-pin** the materialized output — no recorded SHA-256 over the frozen bytes.

Survey-and-report (not fatal, but must be reported in the creation step's provenance note, never silently resolved): the half-day handling actually applied; the specific unscheduled-closure dates the source included or excluded and its basis; and endpoint inclusivity at both bounds.

## 7. What the creation step produces vs. does not

**Produces (only when separately authorized):** a frozen, SHA-pinned, sorted, unique, in-window expected-session date list, plus a short provenance note recording the source, its identity/version, the exact selection rule, the unscheduled-closure dates handled, and the SHA-256 of the frozen bytes.

**Does not:** read any price value cell; read OHLCV; compute CI / CR; compute features; compute wake / outcome / target; open Gate 2; spend alpha; access sealed data; run the missing-days check; or modify atlas status, CR closure, or Gate 1.

## 8. Relationship to the missing-days memo (dependency clearance)

On successful creation against this design, prerequisites #1 (no frozen expected-session reference), #2 (circularity constraint), and #6 (package-version insufficiency) of the missing-days / calendar-handling memo are cleared. Prerequisites #3 (sandbox gitignored; must be present and SHA-matching at run time), #4 (observed-span scoping), and #5 (schema-freeze decision) are independent and are not addressed here. The missing-days check becomes runnable only after the reference is frozen **and** a separate run-authorization turn is issued.

## 9. Explicit non-authorizations

This memo authorizes nothing operational. It does not authorize: creating or materializing the calendar list; acquiring data; selecting-and-committing a source; running the missing-days check; any price-value, OHLCV, feature, CI / CR, wake / outcome / target, or Gate 2 work; alpha spend; sealed-data access; or any change to atlas status, CR closure, or Gate 1.

## 10. Open prerequisites before the creation step can be authorized

1. Select the specific external NYSE / ARCA source and confirm its calendar identity (XNYS regular session).
2. Confirm the source's handling of half-days (as sessions) and of unscheduled closures across the window.
3. Decide the durable storage location and file format for the materialized list, and the committed path.
4. Define where the SHA-256 of the materialized bytes is recorded (the pin of record).
5. Confirm endpoint inclusivity (2005-01-03 and 2022-12-30 both genuine sessions per the source).

## 11. Non-authorized implementation notes (informational; authorizes nothing)

Offered only to inform the eventual, separately authorized creation step; nothing here is an instruction to execute, and no commands are provided. Candidate independent sources to evaluate at that step include an established exchange-calendar library that materializes the XNYS regular session calendar, or the exchange's own published holiday/early-close schedule reconciled into a session list. Whichever is chosen, the materialized output — the actual list of session dates — is what must be frozen and SHA-pinned; the library or schedule is recorded as provenance only. The chosen source must be checked against the half-day rule and the unscheduled-closure handling in §4 before its output is trusted, and that check is the creation step's responsibility, not this memo's.
