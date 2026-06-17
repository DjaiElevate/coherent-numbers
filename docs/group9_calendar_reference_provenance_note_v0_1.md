# Group 9 — Calendar-Reference Provenance / SHA-Pin Note (v0.1)

This note records the provenance and the pin of record for the independent
NYSE/XNYS expected-session reference materialized under the Group 9
calendar-reference creation step.

## Governing records

- Governing commit: `1e0c0eb6126dea69bfb33db421973fb745f2dbec`
- Governing creation-step memo: `docs/group9_calendar_reference_creation_step_design_authorization_memo_v0_1.md`
- Governing memo SHA-256: `a1a3922a24ac0a7c8f3250ff3769916ebb84e02fb3be42ca7180ecdd6f19f749`

## Materialized reference (pin of record)

- Materialized CSV path: `data/reference/nyse_xnys_expected_sessions_20050103_20221230.csv`
- **Materialized CSV SHA-256 (pin of record): `77c3c46d014c5fc1b1d2311bca97b384aa59cacdea5671e09515f68a9cf68b58`**
- Row count (data rows): `4531`
- Total line count (including header): `4532`
- First session date: `2005-01-03`
- Last session date: `2022-12-30`

## Source environment (provenance only)

- Source package: `exchange_calendars==4.2.8`
- Python version: `3.8.2`
- pandas version: `2.0.3`
- numpy version: `1.24.4`
- venv path: `/Users/jay/.venvs/coherent_numbers_group9_xnys_py38`

## Generation rule

- Calendar: `XNYS` (NYSE/XNYS regular equities session calendar) — identity confirmed.
- Timezone basis: `America/New_York`.
- Explicit start/end bounds used (defaults not relied upon): instantiated with
  `start="2004-06-01"`, `end="2023-06-30"`, which fully cover the target window.
- Scope: `sessions_in_range("2005-01-03", "2022-12-30")`, inclusive.
- Output: date-level sessions only, as exchange-local (America/New_York) session
  dates, ISO `YYYY-MM-DD`, sorted strictly ascending, unique.
- No SPY sandbox read, no price cells, no OHLCV.

## CSV serialization

- UTF-8; LF (`\n`) line endings only (zero CR bytes).
- Single column; header line exactly `session_date`.
- One ISO `YYYY-MM-DD` date per line; no index column; no quoting; no blank lines;
  no trailing spaces; exactly one final newline.
- Built deterministically (explicit byte construction); reproducible byte-for-byte.

## Half-day handling

Half-days are retained as full sessions; only the close time differs (early close,
exposed by the source via the session schedule close time).

- `2022-11-25` — session, early close `13:00` America/New_York.
- `2012-12-24` — session, early close `13:00` America/New_York.

## Unscheduled full-market closure tripwire results (non-sessions)

- `2007-01-02` — **Gerald Ford** national day of mourning only (not "Ford/Carter";
  Carter's day of mourning, 2025-01-09, is outside this 2005–2022 window) — non-session.
- `2012-10-29` — Hurricane Sandy — non-session.
- `2012-10-30` — Hurricane Sandy — non-session.
- `2018-12-05` — George H. W. Bush national day of mourning — non-session.

## Offline-query check

The calendar was instantiated and all spot-checks / materialization were performed
with bogus proxy environment variables set (`HTTP(S)_PROXY` / `ALL_PROXY` =
`http://127.0.0.1:9`), forcing any outbound network call to fail. Queries succeeded.
The package answers XNYS calendar queries fully offline; no network access at query time.

## Pin / provenance statements

- The package name, package version, Python version, pandas version, numpy version,
  and venv path recorded above are **provenance only — not the pin**.
- The **materialized CSV bytes SHA-256
  (`77c3c46d014c5fc1b1d2311bca97b384aa59cacdea5671e09515f68a9cf68b58`) is the pin of
  record.** The CSV SHA-256 is computed over the CSV bytes alone and is independent of
  this note (no self-reference).

## Data-boundary statement

No SPY sandbox CSV, price cells, OHLCV, CI/CR, features, wake/outcome/target data,
Gate 2 data, alpha, or sealed data were read, computed, or touched in producing this
reference. The missing-days check was not run and is not authorized by this step.
