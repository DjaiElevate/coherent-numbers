# Lane 2 Type-Tone-Goldstein outcome-side join-gate locks v0.1

## 1. Status

`DRAFT-LOCKED — OUTCOME-SIDE JOIN-GATE CONVENTIONS COMMITTED PENDING FIDELITY CHECK; EXECUTION STILL NOT AUTHORIZED`

Design-only outcome-side join-gate lock memo. It locks the outcome convention for Lane 2 / Type-Tone-Goldstein: the temporal anchor, the news→session mapping, the return basis, RV/outcome coherence, overnight/gap handling, missing/degenerate handling, and the reaction-timing/treatment-buffer posture. It authorizes no data contact, no extraction, and no join. It is committed **pending a semantic/fidelity review** and must not be treated as settled merely because it is committed.

Anchors (active manifest): governing `294494a + c6aeb2b + fb26424`; Phase 0.5 `8fdf233`; v2.1 base `3411db5`. Active HAR-RV leg = `fb26424c92ad30a52f579ec4a1dd8a2b069c2cb0`; stale/superseded HAR-RV leg = `3b32129256562562...` (`3b32129`). Basis/close-field resolution = `084c5bd234a3de8e338fb258800b4b0de51181a9` (SHA-256 of memo blob `95bb9596a99cf87269d6115947f42542b9bfe2e4ccb87bc22b11b6a47ccfa7f9`).

This memo resolves the two blocker families that previously stopped the outcome-side lock:

1. **Basis / close-field** — resolved by `084c5bd` (return basis = close-to-close log return; close field = raw `close`; RV and outcome use the identical raw `close`; arithmetic / `pct_change()` / `adj_close` exploratory scripts superseded for governing use).
2. **Mapping / no-lookahead** — resolved by argument after the §4.3 read: §4.3's max-info boundary stays governing and is **not** amended; the old `s = civil_date` mapping is invalid for ordinary weekdays because its outcome realization lands on the boundary; the governing convention adopts **R1** (anchor at the max-info boundary `m = civil_date + 1`; the boundary/anchor close may serve as the close-to-close baseline; the realized return completes strictly after the boundary). R2 is not required for the primary; no extra treatment buffer is added to the primary.

## 2. Inputs inspected

Committed source/docs and git metadata only — read-only; no data/result/raw/market/outcome/joined files opened; exploratory scripts read, not executed.

- `docs/lane2_type_tone_goldstein_outcome_basis_close_field_resolution_v0.1.md` (`084c5bd`, blob SHA-256 `95bb9596…`) — governing basis/close-field input (§7 log basis, §8 raw `close`, §12 conformance, §9 exploratory supersession, §14 firewall).
- `docs/lane2_market_data_join_design_memo_v0.1.md` (`HEAD`) — §4.3 no-lookahead invariant (lines 158–205): `civil_date` UTC publishing-date semantics (160–162), `gdelt_max_information_date`/`feature_max_information_date` (163–168), default `max-info-date = civil_date + 1 day (locked)` (169–175), outcome must begin strictly after the boundary / no market field on-or-before the boundary aligned as an outcome (176–184), forward-window/`t+1:t+5` CAR example treated as leakage-safe after the max-info-date (191–192).
- `docs/lane2_type_tone_goldstein_v0.3_har_rv_control_scope_amendment_v0.1.md` (`fb26424`) — §9 estimator `r_s = ln(close_s/close_{s-1})` (105); §10 temporal alignment: RV ends ≤ `t−1`, excludes day `t`, excludes outcome `t+1` (112–119); §13 line 188 explicitly defers the `civil_date`-to-session mapping and outcome-side exactness ("These are **not** resolved here").
- `docs/lane2_market_data_acquisition_design_memo_v0.1.md` — single-asset SPY (`:88`), `close` = raw session close (`:150`), `adj_close` = verbatim vendor field (`:151`), adjustment/dividend/split ambiguity deferred (`:299`,`:302`).
- `docs/lane2_divergence_record_4f31bcb_6a75ec7.md` — caps `4f31bcb`/`6a75ec7` SPY-acquisition + next-session-return scripts EXPLORATORY-ONLY.
- `scripts/build_next_session_return.py`, `scripts/join_gdelt_spy_nextday.py` — read as source only. **Superseded for basis/close-field by `084c5bd`** (arithmetic return on `adj_close`: `build_next_session_return.py:87`; `RETURN_PRICE_COL="adj_close"` / `pct_change()`: `join_gdelt_spy_nextday.py:40,:111`). Their **timing** is R1-consistent for the ordinary-weekday anchor (`feature_info_date = civil_date + 1`; realization session strictly after that boundary; baseline/entry close "knowable on/before that boundary" — `build_next_session_return.py:4-11`, `join_gdelt_spy_nextday.py:8-15`). Cited as **timing-consistent only**, never as governing for basis or close field; their weekend baseline convention is not adopted — this memo's anchor rule (§5, §12) governs.

No result/raw/market/outcome/joined data or generated dataset was opened.

## 3. Basis/close-field resolution carried forward

Carried forward verbatim in force from `084c5bd`:

- Return basis = **close-to-close log return**.
- Close field = **raw `close`** for BOTH HAR-RV and the outcome (same-series coherence without reopening the settled HAR-RV `fb26424` leg).
- `next_session_return_s = ln(close_{s+1} / close_s)`; primary outcome `abs(next_session_return_s)`.
- Arithmetic / `pct_change()` returns are **not** governing; `adj_close` is **not** the governing primary close field.
- The two exploratory scripts are superseded for governing basis/close-field use.
- SPY raw-close split-suitability / discontinuity remains an **implementation-time conformance requirement** (§16), not a post-hoc rescue; no committed byte shows splits or unsuitability, so the raw-`close` lock stands conditionally.

This memo does not reopen `084c5bd`.

## 4. §4.3 max-info-date / R1 mapping carried forward

§4.3 of the join design memo is **governing for no-lookahead / max-info-date semantics and is conformed to, not amended**, by this memo.

- The no-lookahead invariant is anchored on each feature row's **maximal information-availability date** `m` (`gdelt_max_information_date` / `feature_max_information_date`), default `m = civil_date + 1 day` (locked default; relaxable only by a future design memo proving a stricter/earlier availability convention under §4.3).
- **R1 interpretation (governing for the primary):** a close-to-close forward return may use the boundary/anchor close `close_s` as the **baseline** provided the **realized return completes strictly after the boundary** (`close_{s+1}`, with `s+1` strictly after `m`). The *market outcome aligned to the feature row* is the realized forward return `s → s+1`, not the baseline close alone.
- R1 is consistent with §4.3's own forward-window / CAR example (join memo §4.3 lines 191–192): a `t+1:t+5` CAR candidate is treated as a leakage-safe forward window after the max-info-date while using the boundary close as its reference baseline.
- §4.3's field-level prohibition ("No market field observed on or before that boundary may be aligned as an *outcome*") is read as: no on-or-before-boundary market field may itself be the **realized outcome**. It does **not** forbid using the known boundary close as the **baseline** of a strictly-forward return.
- **R2 is not adopted for the primary.** R2 (baseline itself strictly after the boundary) is stricter than §4.3 requires, pushes the outcome one extra session later, and can pull the likely boundary/treatment-day return into the RV window. R2 is permitted **only** as report-only robustness / future design extension, never as the primary governing convention, and cannot rescue/overturn/replace the R1 primary.

## 5. Estimand and temporal anchor

The estimand is locked on the **max-info boundary**, not raw `civil_date`.

- `d` = GDELT `civil_date` (UTC publishing-date label).
- `m` = `gdelt_max_information_date` / `feature_max_information_date`; default `m = d + 1 day` unless a future design proves a stricter/earlier availability convention under §4.3.
- `s` = anchor / event session = the **first valid SPY market session on or after `m`**.
- For ordinary weekday dates where `m` is itself a valid trading session, `s = m = d + 1`.
- HAR-RV day `t` is identified with the anchor session: **`t ≡ s`**.
- Contemporaneous anchor-session return: `r_s = ln(close_s / close_{s-1})`.
  - `r_s` is **excluded from the primary outcome**.
  - `r_s` is **excluded from the HAR-RV window** because HAR-RV ends at or before `s − 1` (`t − 1`).
- Primary predictive outcome (post-anchor): `next_session_return_s = r_{s+1} = ln(close_{s+1} / close_s)`.
- Primary Lane 2 / Type-Tone-Goldstein outcome: **`abs(next_session_return_s)`**.

Prohibitions: do not use raw `civil_date` as the anchor; do not use `r_s` as the primary outcome; do not use the contemporaneous anchor-session return as a fallback, rescue, or post-hoc alternative.

**Worked ordinary-weekday mapping (governing).** For `civil_date = d` with `d`, `d+1`, `d+2` valid trading sessions:

- `m = d + 1`; anchor `s = d + 1`; HAR-RV day `t = s = d + 1`;
- RV windows end at or before `d`;
- anchor-session return `r_{d+1} = ln(close_{d+1} / close_d)` is **excluded** from both the RV window and the primary outcome;
- primary outcome `r_{d+2} = ln(close_{d+2} / close_{d+1})`;
- primary absolute outcome `abs(r_{d+2})`.

## 6. Return-basis lock

Carried forward from `084c5bd`:

- `next_session_return_s = ln(close_{s+1} / close_s)`.
- Primary outcome = `abs(next_session_return_s)`.
- Arithmetic returns are **not** governing.
- `pct_change()` is **not** governing.
- Old arithmetic / `adj_close` exploratory scripts are **superseded for governing use** by `084c5bd`.

## 7. RV/outcome coherence lock

HAR-RV and the outcome use the same close-to-close log-return basis **and the same temporal anchor**.

- HAR-RV day `t` equals the anchor session `s` (`t ≡ s`).
- RV uses prior close-to-close log returns ending at or before `s − 1` / `t − 1`: `r_u = ln(close_u / close_{u-1})`.
- Outcome uses the next close-to-close log return: `r_{s+1} = ln(close_{s+1} / close_s)`.
- Primary outcome uses the absolute value of the next-session log return.
- The contemporaneous anchor-session return `r_s` is used by **neither** the RV-control window **nor** the primary outcome.
- Do **not** key the RV window and the outcome to different session anchors.

## 8. Same-series coherence lock

From `084c5bd`: the RV close series and the outcome close series are identical.

- Same **raw `close` field** for HAR-RV and `next_session_return`.
- Same asset.
- Same session calendar.
- Same session ordering.
- Same close-price definition.
- Same handling of missing sessions and duplicate sessions.
- Same raw-close split-suitability / discontinuity conformance requirement.
- Do **not** compute RV from one series and the outcome from another.
- Do **not** compute the outcome from `adj_close` as the governing primary.
- Do **not** compute the outcome using arithmetic `pct_change()` as the governing primary.

## 9. Civil-date timezone/date-basis lock

- GDELT `civil_date` carries **UTC publishing-date** daily-count semantics per §4.3; the content attributed to civil day `d` is only fully observed after day `d`'s publishing window closes.
- `civil_date` is **not** treated as an intraday timestamp.
- The per-row **max-info date `m`** is the governing observability boundary.
- Default `m = civil_date + 1 day` unless a future design proves a stricter/earlier availability convention under §4.3.
- The mapping from `m` to a SPY session is **date-level, deterministic**, and uses the **SPY US-equity market session calendar** and its session-date convention.
- A timezone/date-basis mismatch can shift the news→session mapping by one session and is therefore a **join-gate risk** that implementation must prove conforming (§16).

## 10. Max-info date to trading-session mapping lock

- Compute or carry `gdelt_max_information_date` / `feature_max_information_date`; default `= civil_date + 1 day`.
- Map `m` to the **first valid SPY trading session on or after `m`**; call it anchor/event session `s`.
- Identify HAR-RV day `t` with that same mapped session: **`t ≡ s`**.
- Define `next_session_return_s = ln(close_{s+1} / close_s)`.
- If no valid `s` or `s+1` close exists, the outcome is **missing**; the row/cell is **excluded deterministically with counts reported**.
- Do **not** impute missing closes.
- Do **not** substitute another asset.
- Do **not** use calendar-day returns.
- Do **not** use partial sessions unless the committed market dataset defines them as valid sessions.

## 11. Overnight and gap handling lock

- Because the outcome is close-to-close, overnight and gap moves between `close_s` and `close_{s+1}` are **included** in the primary outcome.
- The contemporaneous pre-anchor-to-anchor gap `close_{s-1} → close_s` is `r_s` and is **excluded** from the primary outcome because `s` is the anchor/event session.
- Because `t ≡ s`, this same `r_s` is also **excluded** from the HAR-RV prior-control window, which ends at or before `s − 1`.
- Overnight and gap moves are **not** separately removed, winsorized, decomposed, or adjusted.
- If a future robustness wants open-to-close, close-to-open, R2, or extra-buffer decomposition, that is **not** primary and **cannot** rescue, overturn, or replace the primary.

## 12. Non-trading news dates

- Weekend/holiday news dates use the **same max-info-date rule**.
- If `m = civil_date + 1` is **not** a valid trading session, map forward to the first valid SPY session on or after `m`; that mapped session is `s`.
- The outcome is the next trading-session close-to-close return `s → s+1`.
- **Worked weekend example.** For weekend/holiday `civil_date = d` where `m = d + 1` is not a trading session and the next valid sessions are Monday `M`, Tuesday `M+1`:
  - `m = d + 1`; anchor `s = M` (first valid SPY session on or after `m`); HAR-RV day `t = s = M`;
  - RV windows end at or before the last valid session before `M`;
  - the anchor-session return into `close_M` is **excluded** from the RV window and from the primary outcome;
  - primary outcome `ln(close_{M+1} / close_M)`; primary absolute outcome `abs(ln(close_{M+1} / close_M))`.
  - This is why weekend/holiday cases often produce **Monday→Tuesday** as the primary outcome.
- The row is excluded **only** if required close data are missing or the mapping is non-computable.

## 13. Reaction timing and treatment-buffer posture

Observability is separated from market-reaction timing.

- §4.3 governs **observability / no-lookahead**, not actual market-reaction timing.
- **No committed memo pins exactly when the market prices GDELT day-`d` news.** HAR-RV `fb26424` line 188 explicitly defers the `civil_date`-to-session mapping and outcome-side exactness; its "pre-treatment / excludes day `t`" framing uses an abstract `t` and pins no calendar relationship to `civil_date`.
- The **primary design does NOT add an extra treatment buffer** beyond the R1 anchor. Rationale:
  - R1 already **excludes the anchor-session return `r_s`** — the session most likely to contain post-publishing or next-open reaction.
  - RV windows end at or before `s − 1`, so `r_s` is **not** included in RV.
  - For ordinary weekday `d`, RV ends at or before `d`; the return `r_d` ending at `close_d` is **retained** in the RV window by default. This is acceptable for primary design because §4.3's observability rationale holds that day-`d` content is only fully observed after day `d`'s publishing window closes, while the US market close on day `d` occurs **before** that full publishing window closes.
  - A stricter buffer excluding `r_d` from RV (e.g. RV ending at or before `d − 1`) would be more conservative but would reduce power and is **not** required by committed bytes.
- Future robustness / design extension **may** test or adopt a stricter treatment-window buffer (e.g. RV ending at or before `d − 1`, or R2 baseline), but that is **not** the primary and **cannot** rescue, overturn, or replace the R1 primary unless separately governed before join.

## 14. Asset/session scope

- Current outcome asset scope is **single-asset SPY**.
- Do **not** broaden the asset universe in this turn.
- For SPY, RV and outcome must use the **identical raw `close` series** and the **identical SPY session calendar**.
- If the asset universe broadens beyond SPY, or admits split-bearing assets, the raw-close decision from `084c5bd` must be **revisited before join**.

## 15. Missing and degenerate handling

Deterministic, fail-closed exclusion with counts reported, for:

- missing `gdelt_max_information_date` / `feature_max_information_date`;
- missing `close_s`;
- missing `close_{s+1}`;
- duplicated session dates;
- non-monotonic session order;
- non-positive close;
- insufficient future session;
- `m` cannot map to a valid session;
- asset/session calendar conflict;
- timezone/date-basis cannot be resolved;
- close-field mismatch between RV and outcome;
- raw-close split-suitability / discontinuity conformance fails;
- HAR-RV day `t` and mapped anchor session `s` cannot be shown identical.

Required rule: **fail closed / exclude deterministically with counts reported.** Do **not** impute, regularize, fall back to arithmetic return, fall back to `adj_close`, fall back to open-to-close, fall back to the contemporaneous anchor-session return `r_s`, substitute assets, key RV and outcome to different sessions, or silently change the mapping.

## 16. Implementation conformance requirements

Future implementation must prove, before any join:

- `gdelt_max_information_date` / `feature_max_information_date` exists;
- default max-info date is at least `civil_date + 1` unless a future design proves a stricter/earlier availability convention;
- `s` is the first valid SPY trading session on or after the max-info date;
- `next_session_return_s = ln(close_{s+1} / close_s)`;
- `abs(next_session_return_s)` is the absolute value of that log return;
- HAR-RV day `t` equals the mapped anchor session `s` (`t ≡ s`);
- RV windows end at or before `s − 1` / `t − 1`;
- the contemporaneous anchor return `r_s` is excluded from **both** the RV window and the primary outcome;
- RV and outcome use the **identical raw `close`**;
- same asset and same session calendar are used for RV and outcome;
- session ordering is strictly increasing and deterministic;
- `civil_date` / max-info-date mapping is deterministic;
- weekend/holiday mapping follows the same anchor rule;
- missing/degenerate cases are excluded with counts;
- **no** arithmetic `pct_change()` outcome is used for the governing convention;
- **no** `adj_close` outcome is used for the governing primary;
- exploratory scripts capped by `docs/lane2_divergence_record_4f31bcb_6a75ec7.md` are **not** invoked as governing join inputs;
- the raw-close split-suitability / discontinuity conformance check passes for the in-scope SPY series;
- no outcome data are inspected before the authorized join stage;
- no 2023+ is touched unless explicitly authorized in a later stage.

## 17. Firewall and sequencing

- This is **design-only**; no data read occurred.
- No extraction occurred.
- No join occurred.
- **Extraction remains unblocked but unauthorized; the join remains blocked.**
- The outcome convention is drafted/committed **before** extraction/join.
- The memo itself is **pending a semantic/fidelity review** before being treated as settled.
- Any future implementation must prove conformance to this memo (§16) before join.
- Committing this memo does **not** push `084c5bd` or this new memo commit.

## 18. Open conflicts or blockers

- **No non-superseded committed-source/design conflict** prevents this lock. §4.3 (observability, max-info-date) and `084c5bd` (log basis, raw `close`) and HAR-RV `fb26424` (raw-`close` close-to-close log RV, RV ends ≤ `t−1`) are mutually coherent under the R1 anchoring (`t ≡ s`, anchor at `m = civil_date + 1`, `r_s` excluded from both RV and outcome).
- The two exploratory scripts conflict with `084c5bd` only on **basis/close-field** (arithmetic / `adj_close`); they are **superseded** for governing use, not blockers. Their **weekday timing** is R1-consistent (baseline = boundary session `d+1`, realization strictly after at `d+2`) and is cited as timing-consistent only; their weekend baseline convention is not adopted (this memo's §5/§12 anchor rule governs).
- **Conditional (not a blocker):** SPY raw-close split-suitability over the in-scope period is unconfirmed from committed bytes; it is carried as the §16 implementation conformance check. No committed evidence contradicts raw `close`.
- **Reaction-timing residual (not a blocker):** market-reaction timing is not pinned by any committed memo; the primary adopts the no-extra-buffer R1 posture (§13), with a stricter buffer reserved as separately-governed future robustness.

## 19. Boundary confirmation

No execution; no extraction; no GDELT contact; no raw-event read; no market-data read; no outcome read; no `next_session_return` data access; no `abs(next_session_return)` data access; no real-data RV; no tests; no V1/V2; no 2023+; no join; no extraction authorization; no join authorization; no memory edits; no push. Only committed source/docs and git metadata were inspected (read-only); the exploratory scripts were read, not executed, and no data they reference was opened.
