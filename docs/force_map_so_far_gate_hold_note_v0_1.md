# Force Map So Far / Gate Hold Note (v0.1)

Anchor: `origin/main = 8f70f18038a285158cb39cf20f28022f3c3fcb3f`

## Force Map free side

The freely explorable price surface currently reduces to:

`drift + volatility clustering + weak short-horizon reversal`

On the full 2005–2022 adjusted-close sandbox:

- drift / trend is the large base context;
- volatility clustering is the master price-shape force;
- compression / expansion is mostly volatility persistence wearing another hat;
- calendar rhythm is weak / dead;
- shock and pullback overlap heavily;
- pullback survived as a weak short-horizon loser-bounce, interesting but not proof-mode-worthy and not an edge claim.

## Volume / liquidity

The volume/liquidity scan used a partial 2013–2022 OHLCV window, not the full 2005–2022 sandbox.

On that partial window, no independent volume force was found. Standalone volume mostly proxies volatility; dollar-volume liquidity is dead / weak for SPY; and the apparent volume × pullback interaction mostly dissolved after the vol-held-fixed / residual-volume probe.

Conclusion: volume is at most a weak conditioner and mostly volatility wearing a volume hat.

## Attention substrate and Gate Hold

A usable attention substrate exists:

`results/lane2_gdelt1_step2_daily_features/20260531T020244Z/step2_daily_features.csv`

It is tracked, SHA-pinned (`48a64e1c…`), raw market-wide counts, date-only, and contains no 2023+ sealed data. No tone / salience / Goldstein / sentiment features are used here.

The GDELT → SPY forward-return join remains held. Gate 2 remains unopened. Existing untracked join files are not to be used.

Reason: news/attention is the highest-prior domain. Looking at the in-sample attention → return relationship, even in map-mode, would contaminate the eventual clean Gate 2 test. Once attention features are inspected against returns, the researcher cannot un-see which features looked alive.

## Mapping correction: STRICT_AFTER_OPEN

Mapping-Seam Reconciliation v0.1 resolved the no-lookahead rule as:

`STRICT_AFTER_OPEN`

For GDELT `civil_date = D`:

- availability date `A = D + 1`;
- `gdelt_max_information_date = A`;
- any outcome window must begin strictly after `A`;
- the earliest defensible outcome anchor is no earlier than the open of the first XNYS session whose date is strictly greater than `A`;
- do not use `first XNYS session >= A`.

Because the GDELT substrate is date-only and does not retain intraday visibility timestamps, event-day reactions and the `D+1` session reaction are not cleanly testable from this substrate without additional timestamp evidence.

Predictor-side endpoints `2013-04-01` and `2022-12-31` are edge-incomplete / excluded, so the usable predictor window is narrower than the nominal substrate range.

## Non-authorizations

This note authorizes nothing:

- no GDELT → SPY join;
- no forward returns;
- no Gate 2;
- no alpha;
- no sealed data;
- no promotion;
- no edge claim;
- no tradable claim.
