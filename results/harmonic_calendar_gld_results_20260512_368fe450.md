# Harmonic Calendar × GLD — v0.1 Verdict

**Project:** Coherent Numbers
**Asset:** GLD
**Active cell memo:** `docs/harmonic_calendar_gld_v0.1.md` (v0.1)
**Inherited lens version:** v0.3.3 (harmonic_calendar_protocol)
**Repo commit before run:** `87e5578a661ac42011024b7359fc42e36440852d`
**Run timestamp (UTC):** 2026-05-12T18:58:16+00:00
**Frozen CSV:** `data/raw/gld_yahoo_v8_20041118_20241231_368fe45094eafa277c81accd2c71b2b593ddcf917c29c7b269de088a31fd1b2c.csv`
**Frozen CSV SHA256:** `368fe45094eafa277c81accd2c71b2b593ddcf917c29c7b269de088a31fd1b2c`
**Loader:** `gld_loader.load_gld`
**Anchor-control:** exhaustive enumeration, 365 integer-DOY anchors (1..365)
**Rank thresholds:** training strictly_below ≥ 347 (= ceil(0.95 × 365)); holdout strictly_below ≥ 329 (= ceil(0.90 × 365))
**Seed (preserved, not consumed):** RANDOM_ANCHOR_SEED = 20260512

## Data ranges

- Raw/design data range: 2004-11-18 through 2024-12-31 (2004-11-18 = GLD inception; 2024-12-31 = freeze terminus, matching SPY cell)
- Design training rule: GLD inception through 2014-12-31 (first-row log-return drop means effective loaded first return = 2004-11-19)
- Effective loaded training date range used for PSS: 2004-11-19 through 2014-12-31
- Effective loaded holdout date range used for PSS: 2015-01-02 through 2024-12-31
- Loaded rows: 5062 (training: 2546, holdout: 2516)

## Training-power caveat (pre-registered)

Training-power caveat (pre-registered in design memo v0.1): The GLD training window is approximately 10.1 years (effective loaded first return: 2004-11-19, through 2014-12-31), versus approximately 22 years for the SPY cell (effective loaded first return: 1993-02-01, through 2014-12-31). The strict-rank convention is identical across cells (March20 must beat 347 of 365 anchors in training, 329 of 365 in holdout). Per-anchor PSS estimates are noisier on GLD's shorter training window. This asymmetry is accepted as a limitation of the GLD cell and must be considered when comparing GLD verdicts to SPY verdicts. A null verdict on GLD carries less power than a null verdict on SPY. A positive verdict on GLD would be directly interpretable against the holdout window, which is matched in length to SPY's holdout (2015-2024).

## Per-outcome verdicts

### Outcome: `log_return`

- **Verdict: `null`**

Calendar PSS values:

| Calendar | PSS_in | PSS_oos |
|---|---:|---:|
| march20_108 | 3.711052e-02 | -9.173413e-02 |
| january_108 | 5.091969e-02 | -1.163461e-01 |
| gregorian_month | 3.117328e-03 | -7.789153e-03 |

Anchor-control null distribution (n = 365, exhaustive):

- PSS_in:  mean=4.728989e-02, median=4.639170e-02, min=4.249011e-02, max=5.328661e-02
- PSS_oos: mean=-1.108049e-01, median=-1.087485e-01, min=-1.311288e-01, max=-9.422467e-02

- March20 PSS_in:  strictly_below 0 of 365 (strict_percentile 0.0000)
- March20 PSS_oos: strictly_below 365 of 365 (strict_percentile 1.0000)

Threshold gates (per v0.3.3 success criteria, inherited by GLD v0.1):

- Training screen (strictly_below ≥ 347 of 365): **fail**
- Holdout primary (strictly_below ≥ 329 of 365 AND PSS_oos > 0): **fail**
  - rank gate: True ; PSS_oos > 0: False
- Holdout auxiliary (PSS_oos > Gregorian AND PSS_oos > January-108): **fail**
  - vs Gregorian: False ; vs January-108: True

Secondary diagnostics: **not computed** (not computed because primary gate failed).

### Outcome: `log_return_sq`

- **Verdict: `null`**

Calendar PSS values:

| Calendar | PSS_in | PSS_oos |
|---|---:|---:|
| march20_108 | 4.136535e-02 | -2.108497e-01 |
| january_108 | 4.232804e-02 | -2.064150e-01 |
| gregorian_month | 7.374264e-03 | -5.375531e-02 |

Anchor-control null distribution (n = 365, exhaustive):

- PSS_in:  mean=3.812378e-02, median=3.755188e-02, min=3.119251e-02, max=4.352095e-02
- PSS_oos: mean=-2.031964e-01, median=-2.002614e-01, min=-2.520139e-01, max=-1.647187e-01

- March20 PSS_in:  strictly_below 287 of 365 (strict_percentile 0.7863)
- March20 PSS_oos: strictly_below 99 of 365 (strict_percentile 0.2712)

Threshold gates (per v0.3.3 success criteria, inherited by GLD v0.1):

- Training screen (strictly_below ≥ 347 of 365): **fail**
- Holdout primary (strictly_below ≥ 329 of 365 AND PSS_oos > 0): **fail**
  - rank gate: False ; PSS_oos > 0: False
- Holdout auxiliary (PSS_oos > Gregorian AND PSS_oos > January-108): **fail**
  - vs Gregorian: False ; vs January-108: False

Secondary diagnostics: **not computed** (not computed because primary gate failed).

## Final summary

**Overall:** `null` — Neither outcome clears the success criterion. Per design memo v0.1 (inheriting v0.3.3 criteria), this is a **null** result.

Per-outcome verdicts:

- `log_return`: **null**
- `log_return_sq`: **null**

_No exploratory follow-up, post-hoc rescue, energy-conditioning, or time-energy-coupling analysis was performed. The locked design memo v0.1 and frozen GLD CSV were not modified during this run. The training-power caveat above applies when comparing this result to SPY._
