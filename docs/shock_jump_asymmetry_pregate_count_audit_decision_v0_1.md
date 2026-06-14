# Shock/Jump Asymmetry Lane — Pre-Gate Count Audit Decision v0.1

**Status:** Owner decision recorded after the Stage-2 pre-gate count audit.

**Lane status:** `INFEASIBLE — matched design, SPY 2005–2022`

**This is NOT a sandbox FAIL. NOT a hypothesis null. NOT a successful or failed hypothesis test. It is an instrument-feasibility result / non-result.**

---

## 1. Decision

After the pre-gate count audit, the owner records the following decision:

- The **Stage-1 matched Shock/Jump Asymmetry design is infeasible** on SPY 2005–2022 under the audited event structure.
- This is **not a sandbox FAIL.**
- This is **not a hypothesis null.**
- This is an **instrument-feasibility result / non-result.**
- **No sealed alpha is debited** (sealed-data contact never occurred).
- **No sandbox gate was run.**
- **No wake/outcome was computed.**
- **No sealed data was accessed.**
- The lane **does not proceed to Stage-2 literal freeze.**
- The lane is **closed on feasibility grounds** unless a future owner explicitly opens a **new version as a separate design**, not as a patch.

---

## 2. Status distinction

- This is **not** `CLOSED-as-null`.
- Lane status: **`INFEASIBLE — matched design, SPY 2005–2022`**.
- The wake-asymmetry question remains **`OPEN-BUT-UNASKABLE by this matched design on this sandbox`**.
- This is **not** marked as a successful or failed hypothesis test.

> **Atlas vocabulary flag:** if the Market Force Atlas status vocabulary lacks an `INFEASIBLE` state (distinct from PASS / FAIL / CLOSED-as-null / RESERVED), a future atlas amendment may be needed to carry this status cleanly. This memo records the status as `INFEASIBLE` pending any such amendment; it does not itself amend the atlas.

---

## 3. Key audit facts (provenance)

- Stage-1 memo commit: `cd1016295ba4b843a61e8c9cd1811c86e88c0406`
- Stage-1 memo SHA-256: `c6529e37dd1a225e80d23f9f3b014620843b9e31deac4d98139c9e3a7bda1fa2`
- Audit report file: `docs/shock_jump_asymmetry_pregate_count_audit_report_v0_1.md`
- Audit report SHA-256: `4e751c3a45efcf65b7dec2bedaa05fb9074102a69326f2433622e2d453f45c8b`
- Audit script file: `scripts/run_shock_jump_asymmetry_pregate_count_audit.py`
- Audit script SHA-256: `cb3c184cca53e879d30c8e702d51f6b6e8804557ba563aafda629d722b18b60c`
- Loaded date range: `2005-01-03` → `2022-12-30`
- Closes loaded: 4531
- No rows ≥ `2023-01-01`
- Max time-local one-to-one no-replacement matched pairs: **6** under either ruler
- Max widened / descriptive-only matched pairs: **9**
- Candidate floors 20 / 30 / 40: **NONE feasible** under either ruler
- Up-shocks are the binding constraint:
  - plain ruler at thresholds 3.5 / 4.0 / 4.5: up-shocks **10 / 2 / 2**
  - sym ruler at thresholds 3.5 / 4.0 / 4.5: up-shocks **10 / 4 / 2**

---

## 4. Interpretation

The matched sign-conditional Shock design cannot be run cleanly because the comparison arm is too sparse. Large down-shocks are much more common than large up-shocks, and fair time-local one-to-one matching cannot produce enough pairs. This scarcity is informative about event frequency, but not about future wake behavior.

The maximum time-local one-to-one no-replacement matched-pair count anywhere in the audited grid is 6 (threshold 3.5), below the lowest candidate floor of 20. Even widened/nonlocal (descriptive-only, excluded from gate) matching reaches only 9. The binding constraint is up-shock scarcity at every candidate threshold.

---

## 5. What was learned / what was not learned

### What the audit established

- Large up-shocks are far scarcer than large down-shocks at every candidate threshold.
- This is an event-frequency / negative-skew property of the return series.
- That scarcity makes the matched comparison arm too sparse to populate.

### What remains untested

- The lane's actual hypothesis — whether down-shocks and up-shocks leave **different future wakes** — was never tested, supported, or nulled.
- No wake/outcome was computed.
- No forward realized volatility, forward drawdown, recovery, or any target was inspected.

> Frequency asymmetry is not wake asymmetry. The pre-gate audit found that the matched design cannot ask the wake-asymmetry question cleanly on this sandbox; it did not answer the wake-asymmetry question.

---

## 6. Non-rescue rule

The result may not be rescued by:

- lowering the threshold,
- widening time matching,
- reusing scarce up-shocks,
- changing to many-to-one matching,
- switching to replacement matching,
- or changing the estimator inside this lane.

Any distributional / non-matched Shock version would be a **new lane** and must start from a **fresh Stage-1 design memo**. A distributional / regression-based Shock-asymmetry version, if desired, is a new lane, not a patch.

---

## 7. Program / atlas bookkeeping

- **Compression remains the named fallback, but is NOT authorized yet.**
- **No next lane is promoted by this memo.**
- Any future promotion requires a **separate decision**.
- A distributional / regression-based Shock-asymmetry version, if desired, is a **new lane, not a patch** to this one.

---

## 8. Audit script forward-unreachability enforcement (carried into the closure package)

The audit script structurally enforced forward-unreachability, so the audit remains permanently auditable:

- **Column allow-list:** the audit table is restricted to event-side fields `{row_idx, date, adj_close, logret, vol_plain, vol_sym, z_plain, z_sym}`.
- **Runtime assertion:** the script aborts if any column outside the allow-list appears in the audit table.
- **Event-side fields only:** no target/outcome/wake arrays are constructed.
- **Trailing-only pre-shock rolling volatility:** volatility uses `rolling(21).shift(1)`, ending strictly at `t-1`; the event-day return `r_t` appears only in the numerator of `z_t`, never in the denominator, and no return after `t` is read.
- **No forward-window functions:** no `iloc[t : t+window]` / `close[t+k]` forward indexing exists in the audit logic.
- **No forward realized volatility / forward drawdown / recovery / target construction** functions are defined.
- **Self-scan found zero forbidden forward-wake function definitions.**

`Forward-unreachability was enforced structurally: the audit table contains only event-side fields and no target/wake arrays or forward-window functions. The code cannot compute forward realized volatility, drawdown, recovery, or any future wake from the constructed audit structures.`

---

## 9. Boundary confirmations

- No wake/outcome was computed.
- No sandbox gate was run.
- No synthetic-null check was run.
- No modeling was run.
- No tuning was run.
- No sealed values were inspected.
- No sealed data was accessed.
- No sealed alpha was debited.

---

## 10. Relationship to prior artifacts

- **Market Force Atlas v0.1** (`dba9b9e`) — governance source; status-vocabulary amendment for `INFEASIBLE` may be required (see §2).
- **First-promotion decision memo** (`23591ba`) — promoted Shock/jump asymmetry; this memo records its matched design as infeasible at the pre-gate audit, without redesign.
- **Shock/Jump Stage-1 design memo** (`cd10162`, SHA `c6529e37…`) — the rules-frozen design audited here; not advanced to Stage-2.
- **Pre-gate count audit report** (SHA `4e751c3a…`) and **audit script** (SHA `cb3c184c…`) — the evidence base for this decision.

No closed lane is reopened by this memo. No new lane is promoted by this memo.
