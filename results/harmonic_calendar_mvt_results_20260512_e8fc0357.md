# Harmonic Calendar MVT — v0.3.3 Verdict

**Project:** Coherent Numbers
**Active memo:** `docs/harmonic_calendar_design_memo_v0.3.3.md` (v0.3.3)
**Repo commit before run:** `9ea89ae9109185e7a8f0a0cdc888a19ec3e38cdd`
**Run timestamp (UTC):** 2026-05-12T16:10:27+00:00
**Frozen CSV:** `data/raw/spy_yahoo_v8_19930129_20241231_e8fc0357410ce499da8f67e09b4c9908232e18a55445f38969e77fa712aaaa56.csv`
**Frozen CSV SHA256:** `e8fc0357410ce499da8f67e09b4c9908232e18a55445f38969e77fa712aaaa56`
**Loader:** `spy_loader.load_spy`
**Anchor-control:** exhaustive enumeration, 365 integer-DOY anchors (1..365)
**Rank thresholds:** training strictly_below ≥ 347 (= ceil(0.95 × 365)); holdout strictly_below ≥ 329 (= ceil(0.90 × 365))
**Seed (preserved, not consumed):** RANDOM_ANCHOR_SEED = 20260512

## Data ranges

- Loaded rows: 8037
- Training: 5521 rows, 1993-02-01 → 2014-12-31
- Holdout: 2516 rows, 2015-01-02 → 2024-12-31

## Per-outcome verdicts

### Outcome: `log_return`

- **Verdict: `null`**

Calendar PSS values:

| Calendar | PSS_in | PSS_oos |
|---|---:|---:|
| march20_108 | 1.689898e-02 | -2.104214e-02 |
| january_108 | 2.435772e-02 | -3.244094e-02 |
| gregorian_month | 1.009139e-03 | 5.534569e-04 |

Anchor-control null distribution (n = 365, exhaustive):

- PSS_in:  mean=2.266199e-02, median=2.288680e-02, min=1.951359e-02, max=2.461078e-02
- PSS_oos: mean=-2.969785e-02, median=-2.939356e-02, min=-3.803591e-02, max=-2.325984e-02

- March20 PSS_in:  strictly_below 0 of 365 (strict_percentile 0.0000)
- March20 PSS_oos: strictly_below 365 of 365 (strict_percentile 1.0000)

Threshold gates (per memo v0.3.3 success criteria):

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
| march20_108 | 1.966718e-02 | -1.643497e-02 |
| january_108 | 1.976427e-02 | -7.227361e-03 |
| gregorian_month | 1.037125e-02 | -1.099381e-02 |

Anchor-control null distribution (n = 365, exhaustive):

- PSS_in:  mean=1.667214e-02, median=1.656438e-02, min=1.434879e-02, max=1.987530e-02
- PSS_oos: mean=-1.053427e-02, median=-1.197972e-02, min=-1.792378e-02, max=-3.049187e-03

- March20 PSS_in:  strictly_below 351 of 365 (strict_percentile 0.9616)
- March20 PSS_oos: strictly_below 27 of 365 (strict_percentile 0.0740)

Threshold gates (per memo v0.3.3 success criteria):

- Training screen (strictly_below ≥ 347 of 365): **PASS**
- Holdout primary (strictly_below ≥ 329 of 365 AND PSS_oos > 0): **fail**
  - rank gate: False ; PSS_oos > 0: False
- Holdout auxiliary (PSS_oos > Gregorian AND PSS_oos > January-108): **fail**
  - vs Gregorian: False ; vs January-108: False

Secondary diagnostics: **not computed** (not computed because primary gate failed).

## Final summary

**Overall:** `null` — Neither outcome clears the success criterion. Per memo v0.3.3, this is a **null** result.

Per-outcome verdicts:

- `log_return`: **null**
- `log_return_sq`: **null**

_No exploratory follow-up, post-hoc rescue, energy-conditioning, or time-energy-coupling analysis was performed. The locked memo v0.3.3 and frozen CSV were not modified during this run._
