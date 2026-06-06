# Lane 2 / TTG → SPY v1 — Zero-Return Handling Amendment v0.1

Status: superseding overlay to prereg v1.1 §A/§F exact-zero tripwire, for the pinned SPY source only. Prereg v1.1 remains FROZEN and unedited at SHA-256 `860f33b632d23005b4365893c3ab19fee26de8ba0879a951d77f37b0f72bce3f`.

Value-blind: no prices, returns, feature values, row data, tie dates, or SOURCEURL appear herein.

## Anchored artifacts

- Prereg v1.1 doc SHA-256: `860f33b632d23005b4365893c3ab19fee26de8ba0879a951d77f37b0f72bce3f`
- SPY source pin doc SHA-256: `f9b05e856b224e59ea2e77b93377b09548445e9e159858a4743be2a8d6da4b18`
- Execution environment note SHA-256: `402440e2581a48408e819427231199c26946ce60abef15a5ede032b62ae433bc`
- Pinned SPY CSV SHA-256: `2842647c318c95bd02bc888ee70361d8242ddf8223281e49a8231ea3d91aa055`
- Exact-zero diagnostic byte-review bundle SHA-256: `b3cb5ef37a8ded92c889f5b82a2b732b26b9ca19c9bc22a469cde9a065d74715`
- Tie-characterization byte-review bundle SHA-256: `b0d5a38bec29bf97bd8c20d5085a07eeffa36893db087097ae76784e036dd9f2`

## 1. Background

v1 execution stopped fail-closed at label construction because the exact-zero return count was 7, exceeding the preregistered `exact-zero count > 3 ⇒ STOP` tripwire.

Two byte-reviewed diagnostics established:

1. No label-construction defect:
   - the runner selects `Adj Close`, not `Close`;
   - applies no rounding, int-cast, fill, shift, or resampling;
   - pairs row `i` with row `i+1`;
   - drops only the final row;
   - numeric equality, Decimal equality on the raw tokens, float-ratio equality, and the `Close` comparator all yield exact-zero count 7.
   - `BUG_SUSPECTED` is excluded.

2. The seven exact-zero ties are genuine rare flat closes in the pinned source:
   - Close/Adj Close exact-zero overlap is 7/7;
   - raw `Close` and adjustment factor are unchanged across every tied pair;
   - no tied session shows row-degeneracy markers: no `High == Low`, no zero volume, no volume equal to the prior row;
   - tied values are seven distinct, non-repeated values, with max multiplicity 1;
   - all ties are temporally isolated;
   - classification from the byte-reviewed tie-characterization diagnostic: `LIKELY_RARE_FLAT_TO_PENNY_CLOSES`.

These diagnostics identify the tripwire event as a real source/label property, not a code bug, stale-provider signal, or adjustment artifact.

## 2. Ratification of the label rule

The prereg §A label rule is ratified unchanged.

For label date `T`, on the recorded pinned `Adj Close` series:

`r(T) = adjclose(T+1) / adjclose(T) - 1`

- class 1 iff `r(T) > 0`;
- class 0 otherwise;
- exact-zero returns remain class 0.

Rationale: a recorded no-change day is not an up day. The conservative pre-registered mapping stands. The study uses the recorded pinned adjusted-close series and does not go behind the recorded source values.

## 3. Finding: no study-design change warranted

The seven exact-zero labels are not a defect, not a stale-provider signal, and not an adjustment artifact.

They provide no basis to change any feature, fold/partition, estimator, metric, bootstrap, threshold, read, join, evaluation, or V1/V2 choice.

Prereg §B, §C, §D, §E, and the non-zero portions of §F are unaffected.

## 4. Superseding the tripwire for this pinned source only

The preregistered `exact-zero count > 3 ⇒ STOP` tripwire is superseded for — and only for — the SPY source pinned at SHA-256 `2842647c318c95bd02bc888ee70361d8242ddf8223281e49a8231ea3d91aa055`.

It is replaced, not relaxed, by the source-bound exact-zero integrity gate in §5.

This superseding is void if the SPY source is re-pinned to any other SHA. A different source requires its own reviewed provenance amendment.

## 5. Source-bound exact-zero integrity gate

At execution, before the single archive feature read is spent, label construction must assert:

1. the pinned SPY CSV re-verifies as SHA-256 `2842647c318c95bd02bc888ee70361d8242ddf8223281e49a8231ea3d91aa055`;
2. the exact-zero return count, recomputed by the locked label code under the pinned source and pinned execution environment, equals 7;
3. all exact-zero ties are assigned class 0 per §2.

Stop conditions:

- If the SPY SHA re-verification fails, STOP because the source changed.
- If the exact-zero count departs from 7 while the SPY SHA still matches, STOP for a new reviewed amendment because label construction or environment behavior no longer reproduces the characterized source property.
- If any exact-zero tie is not assigned class 0, STOP because the ratified label rule is violated.

The blanket `exact-zero count > 3` STOP is retired for this pinned source and replaced by this exact, characterized integrity gate.

## 6. Scope confinement

This amendment touches only label-construction zero-handling and the source-bound exact-zero integrity gate.

It does not modify:

- §B feature specification;
- §C join;
- §D folds, partition, or embargo;
- §E estimator, hyperparameters, or scaler;
- §F metric, bootstrap, seed, flags, or thresholds, except for replacing the exact-zero tripwire as specified above;
- the single-non-adaptive-read rule;
- the holdout-touched-once rule;
- leakage invariants I1–I6;
- the V1/V2 boundary.

All remain locked at prereg v1.1 SHA-256 `860f33b632d23005b4365893c3ab19fee26de8ba0879a951d77f37b0f72bce3f`.

## 7. No execution authorized

This amendment is design/provenance only.

It does not spend the read or authorize archive reading, feature building, joining, training, holdout touching, or any execution.

A fresh execution dispatch is required. That dispatch must re-verify all pinned SHAs, including:

- archive SHA-256 `06dcbc2530deb9fb25dc87b651f3012fe7de21474235c0f85c7ddd53b604383b`;
- SPY CSV SHA-256 `2842647c318c95bd02bc888ee70361d8242ddf8223281e49a8231ea3d91aa055`;
- prereg SHA-256 `860f33b632d23005b4365893c3ab19fee26de8ba0879a951d77f37b0f72bce3f`;
- environment note SHA-256 `402440e2581a48408e819427231199c26946ce60abef15a5ede032b62ae433bc`.

The fresh execution dispatch must implement the §5 gate in place of the prior `exact-zero count > 3` STOP, spend the single read once non-adaptively, and touch the holdout once.

A null result remains a valid terminal outcome.
