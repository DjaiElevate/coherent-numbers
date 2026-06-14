# COMPRESSION — CR DISTINCTNESS CLOSURE DECISION MEMO v0.1

## Records

Base commit: `781b20ba528d2e8eee88ec34389bd663f9a973da`.

Parent commit: `7f1a7d00060469d91c3e24a487a58bf4d4608056`.

This memo records the program decision following the second distinctness diagnostic committed at `781b20ba528d2e8eee88ec34389bd663f9a973da`.

## Result being closed

Second distinctness diagnostic script:

`scripts/run_compression_second_distinctness_diagnostic_v0_1.py`

SHA-256:

`d7e365dc9412c86680896ea3688c9d9f73c3d66ccd46feae7583388449312380`

Second distinctness diagnostic report:

`docs/compression_second_distinctness_diagnostic_report_v0_1.md`

SHA-256:

`ddfda94c7241f991cb2c3a451f1643b7cdc77cfb94623ae300da10881d8bab41`

Frozen Level-1 model:

`CI_21 ~ ER_21 + LOG_TORT_21 + KATZ_FD_FIRST_21`

Primary result:

`blocked-CV Level-1 joint R² = 0.736339`

Frozen decision band:

```text
R² >= 0.85       → ABSORBED BY NON-TAUTOLOGICAL PATH-ROUGHNESS FAMILY
R² < 0.75        → SURVIVES NON-TAUTOLOGICAL PATH-ROUGHNESS DISTINCTNESS TEST
[0.75, 0.85)     → BORDERLINE-ABSORBED BY NON-TAUTOLOGICAL PATH-ROUGHNESS FAMILY
```

Since `0.736339 < 0.75`, the diagnostic status is:

`SURVIVES NON-TAUTOLOGICAL PATH-ROUGHNESS DISTINCTNESS TEST`

This is a thin survival, but it is below the frozen absorption/borderline boundary and therefore not borderline under the frozen rule.

## Decision — atlas status

CR is recorded for the Market Force Atlas as:

`CR — DISTINCT RANGE-EXTENT FEATURE`

Definitions:

```text
CR_21 = range_21 / path_21
CI_21 = -log(CR_21) = log(path_21 / range_21)
```

This is not `RECLASSIFIED — known construct`, because CR was not absorbed.

This is not `CLOSED — null`.

This is not `INFEASIBLE`.

## Characterization

CR is range-normalized path roughness: traversal length relative to the 21-day close-to-close extreme spread.

Equivalently:

```text
CI_21 = log(path_21 / range_21)
```

Interpretive label:

`excursion confined within extremes`

Across the two feature-side diagnostics:

1. CR was largely co-extensive with endpoint efficiency. ER carried most of the absorbable structure in the first diagnostic.

2. CR was not linearly reducible to displacement-based roughness, represented by `ER_21` and `LOG_TORT_21`.

3. CR was not linearly reducible to first-point-distance roughness, represented by `KATZ_FD_FIRST_21`.

4. The full non-tautological Level-1 model reached only `R² = 0.736339`, leaving approximately `0.263661` of `CI_21` unexplained by those two non-tautological extent axes.

By the algebra frozen in the second-diagnostic authorization:

```text
RANGE_PATH_ROUGHNESS_21 = path_21 / range_21 = exp(CI_21)
KATZ_FD_RANGE_21 = log(20) / (log(20) - CI_21)
```

Therefore, range/diameter-based path roughness is CR by identity. It is not a separable competitor.

CR is therefore specifically a range-extent roughness construct:

`excursion from extremes`

This is distinct from:

- `excursion from endpoint`, represented by displacement / ER-style constructs;
- `excursion from origin`, represented by first-point-distance / Katz-first constructs.

## Stopping rule for the reclassification search — CLOSED AS EXHAUSTED

The reclassification search is closed on a bounded-family argument, not fatigue.

A Katz-style / efficiency-ratio-style path-roughness measure normalizes traversed path length by a characteristic distance.

For a one-dimensional close series, the recognized reference distances in this family are:

1. endpoint displacement:

```text
abs(close_t - close_start)
```

2. maximum distance from the first point:

```text
max(abs(close_i - close_start))
```

3. global extreme spread / diameter:

```text
max(close_i) - min(close_i)
```

The status of those three references is now adjudicated:

- Endpoint-displacement axis: tested through `ER_21` and `LOG_TORT_21`; CR survived.
- First-point-distance axis: tested through `KATZ_FD_FIRST_21`; CR survived.
- Range/diameter axis: CR itself by identity; response transforms excluded as tautological.

Range-based volatility estimators are outside this reclassification family. They normalize range by time, square-root time, or constants rather than by traversed path. CR’s path normalization is what makes it a roughness / efficiency construct rather than a volatility estimator.

No further named constructs are pursued ad hoc under this reclassification arc.

## Logged limitations

### 1. Thin margin

The survival margin is thin:

```text
0.75 - 0.736339 = 0.013661
```

The result is a clean `SURVIVES` under the frozen rule, but it is close to the absorption/borderline boundary.

CR is distinct, not strongly separated.

This memo does not promote CR as a star feature on this margin.

### 2. Linear-absorption scope

Both distinctness diagnostics test linear absorption using OLS joint R².

Survival does not prove that no nonlinear function of `ER_21`, `LOG_TORT_21`, and `KATZ_FD_FIRST_21` could absorb CR.

A nonlinear-absorption diagnostic would be a separate question under separate authorization. It is not a continuation of this closed reclassification search and is not authorized here.

## Episode-count audit

An episode-count audit is now considerable, but only under separate authorization.

This memo does not authorize an episode-count audit.

Any future episode-count authorization must freeze in advance:

- episode definition;
- refractory rule;
- count unit;
- inclusion / exclusion rules;
- treatment of overlapping or clustered episodes;
- whether counts are days or distinct independent episodes.

The audit must not be feasibility-tuned after seeing counts.

## Wake seal reaffirmed

This entire arc is feature-side only.

It includes:

- the first collinearity diagnostic;
- the CR distinctness / reclassification memo;
- the second distinctness diagnostic;
- this closure decision memo.

None of these computes or licenses:

- wake;
- outcome;
- target;
- future return;
- future range;
- future volatility;
- expansion;
- drawdown;
- recovery;
- predictive gate;
- alpha spend;
- sealed-period access.

The Compression claim proper remains sealed:

`contained traversal resolves into expansion`

That is a predictive / wake claim and requires a separate future wake-authorized design.

Nothing in this closure memo tests or authorizes that claim.

## This memo does NOT authorize

This memo does not authorize:

- episode-count audit;
- predictive / wake test;
- gate;
- alpha spend;
- sealed-data access;
- atlas promotion beyond `CR — DISTINCT RANGE-EXTENT FEATURE`;
- nonlinear-absorption retest;
- any change to prior diagnostic results.

Each requires separate authorization.
