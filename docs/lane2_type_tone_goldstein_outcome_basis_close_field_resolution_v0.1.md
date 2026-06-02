# Lane 2 Type-Tone-Goldstein outcome basis and close-field resolution v0.1

## 1. Status

`DRAFT-LOCKED — OUTCOME BASIS/CLOSE-FIELD RESOLUTION COMMITTED PENDING FIDELITY CHECK; EXECUTION STILL NOT AUTHORIZED`

Design-only resolution memo. It decides the canonical **return basis** and **close series** for Lane 2 / Type-Tone-Goldstein so the outcome-side join-gate lock memo can be re-run coherently with the settled HAR-RV leg. It authorizes no data contact, no extraction, and no join. It is committed **pending a light fidelity check** and must not be treated as settled merely because it is committed.

Anchors (active manifest): governing `294494a + c6aeb2b + fb26424`; Phase 0.5 `8fdf233` (stale `4fe1f0c` superseded); v2.1 base `3411db5`. Active HAR-RV leg = `fb26424c92ad30a52f579ec4a1dd8a2b069c2cb0`; stale/superseded HAR-RV leg = `3b32129256562feeb1d879fad6c6a42bb2689bd5`.

## 2. Conflict surfaced by the outcome-side join-gate attempt

The outcome-side join-gate lock attempt was correctly **BLOCKED** by a committed-source conflict on two axes:

- **Conflict A (return basis):** committed exploratory scripts compute `next_session_return` as an **arithmetic** return — `scripts/build_next_session_return.py:87` `ret = ac_outcome / ac_prev - 1.0`; `scripts/join_gdelt_spy_nextday.py:111` `pct_change()` — while the settled HAR-RV basis is a **log** return.
- **Conflict B (close field):** those exploratory scripts use **`adj_close`** (`scripts/join_gdelt_spy_nextday.py:40` `RETURN_PRICE_COL = "adj_close"`), while settled HAR-RV §9 uses raw **`close`**. RV/outcome same-series coherence requires one identical close series.

This memo resolves both axes.

## 3. Inputs inspected (committed source/docs only — read-only; no data opened)

- `scripts/build_next_session_return.py` — arithmetic return on `adj_close` (`:87`); reads `adj_close` only.
- `scripts/join_gdelt_spy_nextday.py` — `RETURN_PRICE_COL = "adj_close"` (`:40`), `pct_change()` (`:111`), "adj_close, close-to-close" (`:9,:160`).
- `docs/lane2_type_tone_goldstein_v0.3_har_rv_control_scope_amendment_v0.1.md` (`fb26424`) — §9 estimator (`:105`).
- `docs/lane2_market_data_acquisition_design_memo_v0.1.md` — field table (`:150-151`), adjustment ambiguity (`:299`), dividend/split deferred (`:302`), single-instrument SPY (`:88`).
- `docs/lane2_market_data_join_design_memo_v0.1.md` — no return-basis / close-field lock present.
- `docs/lane2_divergence_record_4f31bcb_6a75ec7.md` — arc cap (`:9`, `:12`).

No result/raw/market/outcome/joined data or generated dataset was opened; the exploratory scripts were read, not executed.

## 4. HAR-RV close-field fact

Confirmed from committed HAR-RV bytes (`fb26424` §9, line 105):

```
trailing_rv_h = sqrt( (1/h) * sum_s r_s^2 ),   r_s = ln(close_s / close_{s-1})
```

The estimator is written on **`close`** (raw close), a **log** return. The committed HAR-RV amendment contains **zero** `adj_close` occurrences. HAR-RV's basis is therefore raw-`close` close-to-close log returns.

## 5. Acquisition close-field facts

Confirmed from `docs/lane2_market_data_acquisition_design_memo_v0.1.md`:

- `close` is **column 6 — "raw session close"** (`:150`).
- `adj_close` is **column 7 — "raw vendor adjusted close (verbatim source field)"** (`:151`).
- `adj_close` adjustment semantics are explicitly flagged as ambiguous/open: **"Adjustment ambiguity: vendor `adj_close` semantics (dividend/split …)"** (`:299`) and **"Dividend/split handling: deferred — any total-return reconstruction is an [out-of-scope step]"** (`:302`).
- Acquisition freezes **raw OHLCV plus verbatim `adj_close`**, "captured verbatim, not transformed" (`:123,:126,:357`); it computes **no returns/outcomes/signals** and leaves the close-field choice open for a downstream step.

## 6. Scope and SPY split-suitability facts

- **Single-asset SPY scope: CONFIRMED.** `docs/lane2_market_data_acquisition_design_memo_v0.1.md:88` — "**v0.1 Input B is exactly one instrument: `SPY`.**" (EFA/EEM/GLD/TLT are named future-only, not acquired.) The asset universe is not broadened here.
- **SPY split-history / raw-close split-adjustment suitability:** `SPY split-history / raw-close split-adjustment suitability is not confirmed from committed repo bytes.` No committed doc/source states SPY's split history; the only committed "split" references are unrelated train/holdout *data* splits. No committed evidence shows SPY had splits or that raw close is unsuitable.
- **Decision-rule application:** single-asset SPY scope is confirmed but split history is not confirmable from committed bytes ⇒ this memo **draft-locks raw `close` conditional on an implementation-time conformance proof** that the in-scope SPY/session series has no split discontinuity (or that the raw close field is otherwise valid for the in-scope series). This condition is recorded as an **implementation conformance requirement (§12), not a post-hoc rescue**. Because committed bytes show neither splits nor unsuitability, this does **not** block the raw-`close` lock.

## 7. Resolution: return basis

**Canonical return basis = close-to-close log return.** The canonical outcome is:

```
next_session_return_s = ln(close_{s+1} / close_s)
```

and the primary Lane 2 / Type-Tone-Goldstein outcome is:

```
abs(next_session_return_s)
```

Arithmetic / `pct_change()` returns are **not** the governing convention. This mirrors and coheres with the settled HAR-RV log basis (`r_s = ln(close_s / close_{s-1})`), so RV and outcome share one return algebra.

## 8. Resolution: close field

**Canonical close field = raw `close`, used for BOTH HAR-RV and the outcome.** Rationale:

- Settled HAR-RV §9 already uses `close`; choosing `close` for the outcome preserves RV/outcome **same-series coherence without reopening the settled HAR-RV governing leg**.
- `adj_close` would (a) require reopening HAR-RV §9 (a governing-spec amendment with its own correction/canary/external-byte-review cycle) and (b) require resolving the acquisition memo's flagged vendor-adjustment (dividend/split) ambiguity — both avoided here.
- For the locked single-asset SPY scope, raw `close` is preferred **provided** split-discontinuity risk is absent or shown non-load-bearing by the implementation-time conformance check (§6, §12).
- Dividend / ex-dividend effects remain embedded in raw close-to-close returns and are treated as scheduled, plausibly news-orthogonal noise, disclosed by robustness diagnostics, **not** removed from the primary (§11).

## 9. Exploratory-script supersession

- `scripts/build_next_session_return.py` and `scripts/join_gdelt_spy_nextday.py` are **legacy / exploratory** for the governing outcome convention. They sit within the arc capped **EXPLORATORY-ONLY** by `docs/lane2_divergence_record_4f31bcb_6a75ec7.md` (`:9` covers commits `4f31bcb` "SPY acquisition + next-session-return join" and `6a75ec7`; `:12` "Resulting status: EXPLORATORY-ONLY").
- Their **arithmetic `adj_close`** logic must **not** be used as the canonical Lane 2 / Type-Tone-Goldstein outcome convention.
- Future implementation must update/replace outcome construction to conform to the **log-return raw-`close`** convention before any join.
- **No existing script is authorized for the join merely because this design memo is committed.**

## 10. No HAR-RV governing reopen

- This resolution **avoids reopening the settled HAR-RV `fb26424` leg** by choosing the same `close` series already used by HAR-RV §9.
- **No HAR-RV governing-spec amendment is created in this turn.**
- If implementation-time conformance later shows raw `close` is unsuitable for the in-scope series (e.g. a split discontinuity is found), then a **separate governing design decision is required before extraction/join** — it would not be patched silently here.

## 11. Dividend / ex-dividend handling

- Raw `close` includes scheduled dividend / ex-dividend price effects if present; these are **not** removed from the primary return.
- They are considered scheduled and plausibly **orthogonal to GDELT/news features** at the primary design level.
- Future robustness **may** (report-only): drop known ex-dividend dates if such a calendar is available without violating the firewall; and compare `adj_close` as a report-only sensitivity arm.
- Such robustness **cannot rescue, overturn, or replace** the raw-`close` log-return primary.

## 12. Implementation conformance requirements

Future implementation must prove, before any join:

- the outcome formula is a **log** return `ln(close_{s+1}/close_s)`, **not** arithmetic;
- RV and outcome use the **identical raw `close`** field;
- **same asset and same session calendar** for RV and outcome;
- `close_s` and `close_{s+1}` are **positive and non-missing**;
- session order is strictly increasing and **deterministic**;
- **no arithmetic `pct_change()`** outcome is used for the governing convention;
- **no `adj_close`** outcome is used for the governing primary;
- legacy/exploratory scripts **cannot be invoked as governing join inputs**;
- because raw-close split suitability was **not** confirmed from committed bytes (§6), implementation **must include a split-discontinuity / raw-close-suitability conformance check** for the in-scope SPY series before join;
- any ex-dividend / `adj_close` diagnostic is **report-only** and cannot rescue/overturn.

## 13. Remaining conditions and blockers

- **Conditional item (not a blocker):** raw-`close` split-suitability for SPY over the in-scope period is unconfirmed from committed bytes; it becomes the §12 implementation conformance check. No committed evidence contradicts raw `close`, so the lock stands conditionally.
- **No outstanding committed-source conflict** prevents this resolution: HAR-RV (raw `close`, log) and this resolution (raw `close`, log) agree; the only conflicting artifacts are the EXPLORATORY-ONLY-capped scripts, which §9 supersedes for governing use.
- If a future turn broadens the asset universe beyond SPY or admits assets with material splits/corporate actions making raw close discontinuous, the close-field decision (§8) must be **revisited before join** (§6 scope condition).

## 14. Firewall and sequencing

- This is **design-only**; no data read, no extraction, no join occurred.
- **Extraction remains unblocked but unauthorized; the join remains blocked.**
- The outcome convention basis/close-field is resolved here so the **outcome-side join-gate lock memo can be re-run** with the `(log-return, raw `close`)` pair settled — that re-run is a separate turn, **not** performed here.
- This memo is **pending a light fidelity check** before being treated as settled.
- Any future implementation must prove conformance (§12) to this memo before join; no extraction or join authorization is granted by committing this memo.

## 15. Boundary confirmation

No execution; no extraction; no GDELT contact; no raw-event read; no market-data read; no outcome read; no `next_session_return` data access; no `abs(next_session_return)` data access; no real-data RV; no tests; no V1/V2; no 2023+; no join; no extraction authorization; no join authorization; no memory edits; no push. Only committed source/docs and git metadata were inspected (read-only); the exploratory scripts were read, not executed, and no data they reference was opened.
