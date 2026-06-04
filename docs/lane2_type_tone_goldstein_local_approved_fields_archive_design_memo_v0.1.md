# Lane 2 Type-Tone-Goldstein local approved-fields archive design memo v0.1

## 1. Status

`DRAFT-LOCKED DESIGN-ONLY — LOCAL APPROVED-FIELDS ARCHIVE PATH SELECTED; NO NETWORK, NO ARCHIVE EXECUTION, NO EXTRACTION, NO JOIN AUTHORIZED; NOT SETTLED PENDING FIDELITY REVIEW`

Design-only memo. It selects the route for resolving the local-only substrate blocker and specifies the design of a future, separately authorized local approved-fields archive. It authorizes **no network contact, no GDELT contact, no archive execution, no extraction, and no join**. It is committed (in a later, separate, explicitly authorized step) **pending a semantic/fidelity review** and must not be treated as settled merely because it is committed.

## 2. Current state

- Governing fidelity-passed anchor: `bc3b9c0` (outcome-side join-gate locks) — **DRAFT-LOCKED, NOT SETTLED**; fidelity-passed on design content + manifest pins.
- Manifest pins (carried forward, unchanged): governing `294494a + c6aeb2b + fb26424`; Phase 0.5 `8fdf233`; v2.1 base `3411db5`; basis/close-field `084c5bd`; join-design durable pin `df9089b`.
- Extraction remains **unauthorized**.
- Join remains **blocked**.
- 2023+ remains **sealed**.
- Push remains **deferred**.
- This memo does not change `bc3b9c0`'s status and adds no new governing scientific lock; it is a process/substrate-routing design memo.

## 3. Prior blocker and source-byte rationale

The prior extraction-authorization evidence turn produced:

`EXTRACTION BOUNDARIES NOT BYTE-CLEAR — LOCAL-ONLY SUBSTRATE NOT ESTABLISHED`

i.e. extraction authorization was **blocked because local-only substrate was not byte-clear**. The follow-up offline-substrate evidence turn produced:

`OFFLINE-SUBSTRATE EVIDENCE SHOWS NETWORK BOUNDARY — NO MEMO CREATED`

The offline-substrate evidence showed, from committed **source bytes**, that the proven count-build acquisition path (the path the v2.1 prompt `3411db5` instructs reuse of) **requires live network contact**, and that **raw event rows were discarded after parsing into counts** — so no retained local raw-event substrate exists for the Type-Tone-Goldstein (TTG) approved fields. Source-byte anchors:

- `src/lane2_gdelt1_count_feasibility.py` @ `7a9ca71`:
  - `:626` `DEFAULT_GDELT1_BASE_URL = "http://data.gdeltproject.org/events/"` (per-file download base for `<YYYYMMDD>.export.CSV.zip`).
  - `:714` `def download_one(...)`; `:726-728` "Does NOT perform a real download in this draft: requires BOTH `REAL_RETRIEVAL_ENABLED` and `network_authorized` AND an explicit `opener`."
  - `:647` `REAL_RETRIEVAL_ENABLED = False`.
  - `:1730-1735` "This is the wired retrieval/freeze/count flow. It performs a **REAL download** ONLY through the injected `opener` … the runner flips it transiently … no real network in tests." (The real path is a network download.)
- `scripts/run_lane2_gdelt1_full_daily_count_build.py` @ `fc98fc4`:
  - `:111` `EVENT_FILE_BASE_URL = "http://data.gdeltproject.org/events/"`.
  - `:1257` "Fetch one payload (with hash + parse + **discard**)"; `:1259` `def _fetch_one_payload(...)`; `:1267` network exception handling ("FetchFailure on HTTP non-200, urllib HTTPError/URLError, or any other network exception"); `:1270-1271` "The caller is responsible for **discarding the returned bytes after parsing** (payload-discard mechanism per memo §15.11)."
  - `:1618` "the full **3,558-URL fetch set**"; `:1620` "The **merge step (offline, no GDELT contact)** consumes the per-chunk derived artifacts" — i.e. "offline" scopes to the merge, not the row acquisition.
- `src/lane2_gdelt1_step2_features.py` @ `d0d82c0`:
  - `:1-18` "Step 2 daily-feature generator (**offline, GDELT-only**) … Reads the canonical **merged daily-count substrate** only … **NO GDELT fetch**, NO BigQuery, **NO row export** … Does NOT reuse `FULL_BUILD_AUTHORIZED` (live-fetch guard; Step 2 is offline)."

Conclusion: `step2_daily_features.csv` is byte-confirmed offline **count/volume** feature output (derived from merged daily counts), **not** TTG per-row extraction output; and local-only TTG extraction is impossible unless a local approved-fields archive is built first, or live network/GDELT contact is separately authorized.

## 4. Decision

We select **Path 1a — build and pin a local approved-fields archive first.**

1. We will **not** silently fold live GDELT contact into "extraction."
2. We will **not** authorize TTG extraction yet.
3. We will **not** authorize archive execution yet.
4. We will **not** authorize join.
5. We will **not** touch 2023+.
6. We **separate** the network/archive step from the irreversible TTG feature/statistical-read step.
7. The next future execution frontier, if later authorized, is a **local approved-fields archive build**, **not** TTG extraction.
8. That archive build may contact GDELT **only if separately authorized** in a future execution prompt.
9. That archive build must retain **only** the approved fields needed for TTG (§7).
10. The local archive must later be the **sole** read source for TTG extraction (§13); TTG extraction must not read GDELT/network.

## 5. Governing artifacts

- `294494a` — lock-closed v0.2 governing formula/spec; sole authority for the date/information-date field, formulas, thresholds, in-scope definition, diagnostics, gates.
- `c6aeb2b` — additive v0.3 lock-closure amendment (co-governing with `294494a`).
- `3411db5` — TTG extraction execution prompt v2.1 (design-only); names the count-build acquisition path and the approved/forbidden field sets.
- `fb26424` — active HAR-RV control-scope leg.
- `8fdf233` — Phase 0.5 Option A y_synth correction.
- `084c5bd` — outcome basis/close-field resolution.
- `bc3b9c0` — outcome-side join-gate locks (fidelity-passed, DRAFT-LOCKED).
- `df9089b` — durable join-design memo pin (§4.3 no-lookahead invariant).
- Source-byte evidence commits: `7a9ca71`, `fc98fc4`, `d0d82c0` (see §3).

## 6. Authorized future archive scope, if separately executed later

If — and only if — a future, separate execution-authorization prompt authorizes it, the archive build would:

- contact GDELT over the network **once** to fetch the 2013–2022 source-file universe (the same 3,558-URL fetch-file-date universe proven by the count-build path), under its own default-false guard;
- apply the 2013–2022 in-sample filter at discovery/enumeration time; any source file/date `> 2022-12-31` must hard-error before reading content rows;
- stream/parse each fetched file, **retain only the approved fields** (§7), and write a pinned local approved-fields archive plus structural manifest (§10, §11);
- be **value-blind** (§12): it may parse approved-field values only to filter and write the archive, and may report **structural metadata only**.

This memo does **not** authorize that build. It specifies its design constraints only.

## 7. Approved fields

The archive may retain **only**:

- date / information-date field **as locked by `294494a`**;
- `QuadClass`;
- `GoldsteinScale`;
- `AvgTone`;
- `NumMentions`.

No other field may be retained, written, or carried forward.

## 8. Forbidden fields and boundaries

GDELT export rows may **transiently** contain forbidden columns during parsing, but the archive build must **never retain, write, compute on, summarize, surface, log, or expose** any of:

- `EventCode` / `EventBaseCode` / `EventRootCode`;
- actor fields;
- location fields;
- article text;
- market data;
- outcome data;
- price-derived fields;
- trailing realized volatility (RV);
- joined data;
- any 2023+ data.

No "just in case" fields. The forbidden-field set is identical to the v2.1 (`3411db5`) forbidden set; this memo does not relax it.

## 9. Network boundary handling

- Live GDELT/network contact is a **separate boundary** from "extraction" and must be **explicitly authorized or rejected** in its own future prompt; it must not be folded into TTG extraction.
- This memo authorizes **no network contact** and **no GDELT contact**.
- The current acquisition path requires network (§3); therefore the archive build is the **only** step permitted (later, separately) to perform that contact, and only to populate the local approved-fields archive.
- After the archive is pinned, **no further network/GDELT contact** is required or permitted for TTG extraction.

## 10. Local archive requirements

The future local archive must:

- write only to a **fresh timestamped run directory** (e.g. `results/lane2_gdelt1_type_tone_goldstein_local_archive/<TIMESTAMP_Z>/`), never overwriting an existing directory;
- contain **only approved-field** rows/columns (§7), keyed by the locked date/information-date field;
- exclude every forbidden field and every 2023+ row (§8);
- be the **sole** later read source for TTG extraction (§13);
- carry a structural manifest sufficient to pin its identity and reproduce its provenance (§11).

## 11. Reproducibility / manifest requirements

The archive must be pinned by **structural metadata only**:

- run directory;
- manifest;
- source URL / date universe (the enumerated 2013–2022 fetch-file-date set);
- per-file / per-source-file status (fetched / parsed / skipped / hard-errored);
- approved-field schema (column names + types, no values);
- row counts (per file and total);
- SHA-256s (per archive artifact and manifest);
- deterministic code version / commit;
- explicit **no-join / no-outcome / no-market** declaration;
- explicit **no-2023+** proof.

## 12. Value-blind rule and irreversible-read accounting

The archive build must be **value-blind**:

- It may **stream/parse approved-field values only** to filter rows and write the approved-fields archive.
- It may report **structural metadata only** (§11).
- It must **not** compute, print, save, or expose value-level summaries of the approved fields.
- It must **not** compute distributions, histograms, means, medians, min/max values, correlations, z-scores, examples, sample rows, per-date field aggregates, or any other value-dependent function of `QuadClass`, `GoldsteinScale`, `AvgTone`, or `NumMentions`.
- **No human** should inspect archived field values during the archive-build step.

Irreversible-read accounting:

- The irreversible in-sample TTG read is **not spent** by this design memo.
- The irreversible in-sample TTG read is **not spent** by a future archive-build step **only if** that step is strictly value-blind and reports structural metadata only.
- The irreversible in-sample TTG read **is spent** by any value-level read, inspection, summary, diagnostic, feature computation, or statistic over the 2013–2022 approved-field values — **even if it is not formally labeled a "TTG feature."** Row counts and structural metadata are not value-level reads; any function of the field *values* is.

## 13. Relationship to future TTG extraction

- A future TTG extraction, if separately authorized **after** the archive is pinned, must read **only this pinned local archive**, not GDELT/network.
- That extraction would be the step that **spends** the irreversible in-sample read (it computes value-level features/statistics).
- The archive build and the TTG extraction each require **separate** authorization prompts; neither is authorized here.
- The v2.1 prompt's "reuse the count-build acquisition path" instruction is, under this route, satisfied **once** by the archive build's network fetch; TTG extraction thereafter is local-only.

## 14. Relationship to join

- Join remains **blocked**.
- The archive retains no market/outcome/joined data and computes no outcome.
- No `next_session_return`, no `abs(next_session_return)`, no market field may be retained, read, or aligned.
- Outcome join remains a separate, later, still-blocked gate governed by `bc3b9c0` / `df9089b`; this memo does not advance it.

## 15. 2023+ / V1 / V2 firewall

- **2023+ remains sealed.** No 2023+ read, no 2023+ source-path enumeration into any manifest; any date `> 2022-12-31` must hard-error before content-row reads.
- **V1 / V2** remain gate-time schema verifications owned by the future archive-build and TTG-extraction authorizations; this memo neither runs nor satisfies them.

## 16. Future authorization sequence

1. Fidelity-review this memo (external); only then may it be recorded as settled.
2. Separately author and authorize a **local approved-fields archive build** execution prompt, with explicit value-blind and forbidden-field-retention guards (§12, §18-equivalent), a default-false network guard, and the 2023+ firewall.
3. Run that archive build once (separate execution turn), producing the pinned local archive + structural manifest.
4. Separately author and authorize a **TTG extraction** execution prompt that reads only the pinned local archive.
5. Only after a clean extraction + diagnostics pass would the still-separate, still-blocked outcome-join gate be considered.

Each step is its own prompt; approval of one does not authorize the next.

## 17. Stop conditions

- If the target memo path already existed, stop before editing (reported separately).
- The future archive-build authorization **must include an explicit value-blind guard** and a forbidden-field-retention guard; absent either, the archive build must not run.
- If the archive build cannot retain approved-only fields without exposing forbidden fields or value-level summaries, it must hard-error and report BLOCKED rather than proceed.
- If the proven discovery/fetch path cannot be reused without ambiguity, stop before data contact and report BLOCKED.
- No inline redesign, no tuning, no patch-and-rerun across an authorization boundary.

## 18. Boundary confirmation

This memo, as written:

- authorizes **no** network contact;
- authorizes **no** GDELT contact;
- authorizes **no** archive execution;
- authorizes **no** TTG extraction;
- authorizes **no** join;
- touches **no** 2023+ data;
- reads **no** raw-event, market, outcome, joined, `next_session_return`, or `abs(next_session_return)` data;
- runs **no** tests and exercises **no** V1/V2;
- is **DRAFT-LOCKED design-only**, **NOT SETTLED pending fidelity review**.

`2023+ remains sealed.` `join remains blocked.`
