# Market Force Atlas — Second-Promotion Decision: Compression v0.1

**Status:** Owner decision recorded. **Decision memo only.**

**This memo does NOT freeze a design. It does NOT authorize data contact. It does NOT authorize any audit, gate, sandbox run, or sealed access.**

---

## 1. Decision

- **Compression is selected as the next candidate force for Stage-1 design work.**
- This choice is made after the Shock/Jump matched design closed as **`INFEASIBLE — matched design, SPY 2005–2022`** (closure commit `526b12de8cf2fb6b7a1f680ac7818274c6e1cd50`; atlas amendment commit `a761085a84ad626e80116f0a6b82aa45d18eb70f`).
- Compression is chosen partly because it is a **genuinely different force**, not a Shock rescue.
- A distributional / regression-based Shock-wake lane **remains possible in the future, but is NOT selected here.**
- Any future Shock variant would require a **fresh Stage-1 design memo and a separate promotion decision.**
- **No next test is authorized by this memo.**
- **No data contact is authorized by this memo.**

---

## 2. Rationale (disciplined, not aesthetic)

Compression is chosen for disciplined reasons, not mainly aesthetic ones.

> Compression is not selected because "pressure at rest" is a beautiful metaphor. It is selected because it is the named fallback, it is not a continuation or rescue of Shock, and it asks a different force question.

### Honest prior

> The honest prior is that Compression may null or prove infeasible by dissolving into ordinary volatility behavior, floor mechanics, or insufficient independent episodes. That would be an acceptable result, not a disappointment.

---

## 3. Primary hazard: volatility mean-reversion, bounded-floor mechanics, and breakout-edge drift

- Compression is at **high risk of dissolving into ordinary volatility behavior.**
- Compression is usually defined by low range, low realized volatility, narrow movement, or containment.
- Therefore the future Stage-1 design must ask whether Compression **adds anything beyond boring volatility explanations.**
- Compression must clear **two boring baselines**:
  1. **volatility mean-reversion;**
  2. **bounded-below / floor mechanics.**
- The canonical baseline must include **trailing realized volatility / volatility mean-reversion.**
- The **bounded-floor confound** must be named explicitly:
  - volatility is autocorrelated;
  - volatility is bounded below by zero;
  - any low-volatility reading is mechanically more likely to be followed by an **increase** than a decrease;
  - that apparent asymmetry can be a **statistical artifact of the floor, not a force.**
- The future Stage-1 design must show Compression adds something **beyond both**:
  1. volatility mean-reversion;
  2. bounded-below-floor mechanics.
- A **null or infeasibility would be an acceptable result.**

> The first burden of a Compression lane is not to sound like pressure-at-rest; it is to prove it is not merely ordinary volatility mean-reversion or bounded-floor mechanics wearing a more poetic name.

---

## 4. No breakout-strategy drift

- Compression must **not** become a hidden breakout trading strategy.
- The future design must **not** be framed as "find quiet ranges and trade the breakout."
- Directional profit, entry/exit logic, and trading edge are **not** the purpose of this lane.
- The purpose is **explanatory**: determine whether a compression state has a measurable relation to later expansion **beyond baseline volatility behavior and floor mechanics.**
- Any future outcome must be framed as **force behavior / path behavior, not profitability.**

---

## 5. Metaphor is generative, not evidentiary

- The forest / pressure metaphor is useful for **generating** the question.
- The metaphor must **step back at the gate.**
- Once Stage-1 begins, Compression must be judged against **frozen definitions and boring baselines.**
- **Beautiful language is not evidence.**
- The project remains valuable **because its words can fail.**

> The metaphor may nominate a force, but it may not testify for that force. Compression must earn its meaning against the volatility baseline and bounded-floor mechanics.

---

## 6. Prior-art guard

If any prior Compression work exists elsewhere in the repo or project history, it is treated **only as historical prior art.** (No committed Compression design/result artifact was found in `docs/` at this decision; the atlas Compression card is a `STUB`/`FULL` concept entry, not a result.)

- **No prior Compression result is inherited as evidence in this atlas lane.**
- **No prior result authorizes a new test.**
- Any future Stage-1 Compression design must stand on its **own frozen rules.**
- Any future data contact requires **explicit authorization.**

---

## 7. Future Stage-1 requirements (recorded, NOT designed here)

The future Compression Stage-1 design memo must, at minimum, address:

1. Exact compression definition **before data contact.**
2. Canonical volatility baseline, including **trailing realized volatility / volatility mean-reversion.**
3. **Bounded-below / floor-mechanics baseline.**
4. How "expansion" is defined **without becoming a trading signal.**
5. Whether expansion is **magnitude-only, directionless, or directional.**
6. How to **avoid breakout-profit framing.**
7. How to prevent **post-hoc threshold selection.**
8. Whether multiple compression definitions are **one family or separate lanes.**
9. How **alpha / attempt budget** would be handled if any future gate is authorized.
10. **Sealed-data firewall and 2023+ protection.**
11. **No rescue** by swapping compression definitions after results.
12. **Pre-gate feasibility/count audit** before any gate design.

### Required future feasibility/count audit

- Before any Compression gate is designed or run, a **pre-gate feasibility/count audit** must establish how many **distinct, independent compression episodes** exist in SPY 2005–2022.
- Compression regimes can persist for weeks or months, so **calendar-day counts may overstate independent observations.**
- The audit must count **distinct episodes, not just days.**
- The audit must assess **episode independence / clustering.**
- The audit must **not** compute wake/outcome.
- The audit must **not** inspect expansion results.
- If independent episodes are too few, the lane may be **`INFEASIBLE`** in the same sense as Shock's matched design.
- This infeasibility must be **discoverable cheaply before any gate design or alpha-spending step.**
- **This memo records the future requirement only; it does not authorize the audit now.**

---

## 8. Status

- **Active lane count remains zero** until a Stage-1 design memo is explicitly drafted and accepted.
- This decision memo **promotes Compression as the next design candidate only.**
- It does **not** itself open a sandbox gate.
- It does **not** authorize a pre-gate feasibility audit yet.
- It does **not** spend alpha.
- It does **not** authorize sealed data.
- It does **not** promote any Shock variant.

---

## 9. References

- Current atlas amendment commit: `a761085a84ad626e80116f0a6b82aa45d18eb70f`
- Shock closure commit: `526b12de8cf2fb6b7a1f680ac7818274c6e1cd50`
- Shock status: `INFEASIBLE — matched design, SPY 2005–2022`
- Atlas status vocabulary now includes `INFEASIBLE`

---

## 10. Boundary confirmations

- No tests were run.
- No modeling was run.
- No market data was opened.
- No gate was run.
- No synthetic-null check was run.
- No wake/outcome was computed.
- No sealed data was accessed.
- No alpha was spent.
- No Compression design detail is frozen by this memo.
