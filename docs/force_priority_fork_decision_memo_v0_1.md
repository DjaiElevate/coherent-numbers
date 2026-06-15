# FORCE-PRIORITY FORK DECISION MEMO v0.1

## Records

Base commit: `91401b192a9cf63592a216e4526d410a8373210f` (HEAD = origin/main).

This memo records a project-orientation decision following the read-only retrieval of
the committed Market Force Atlas (`docs/market_force_atlas_v0_1.md`). It contacts no
data and authorizes no test.

## Ground truth from the Atlas retrieval

- The Atlas is explanatory, not an edge ranking. Its own charter: "a map of the forest,
  not a hunt for an edge"; explicitly not a trading / prediction-for-profit / alpha
  system. It organizes forces by group (1-10), cluster, and governance status — not by
  impact, tradability, or forecastable edge.
- The current sandbox (adjusted-close SPY 2005-2022; volume partial 2013-2022) supports
  testing of price-shape (Group 1), calendar (Group 8), and data-construction (Group 9)
  forces only. Macro (Group 3), fundamentals (Group 4), liquidity / market structure incl.
  options hedging, dealer positioning, flows (Group 5), and cross-asset (Group 7) are
  STUB / vintage-gated / unavailable. The largest forces are unreachable by data
  availability, not by deprioritization.
- Compression is a coherent Atlas force: FULL / OPEN, VOLATILITY cluster, canonical
  representative = trailing realized volatility; card bar = "beat 'vol is simply low.'"
- CR (range / path) is recorded (closure memo, cdf78f1) as DISTINCT RANGE-EXTENT FEATURE
  — distinct from displacement- and first-point-based path roughness; thin margin; linear
  scope.
- The wake claim ("contained traversal resolves into expansion") remains SEALED.

## The three paths

- A  — continue mapping testable Atlas forces (price-shape / calendar); nulls as findings;
  episode-count audit optional.
- A' — open the compression wake question (does compression precede expansion):
  edge-flavored but price-feasible, because both the feature and the outcome are
  price-derived; gated and ritual-bound.
- B  — a separate new-data edge project (options / flows / macro / positioning): costlier,
  more leakage-prone, requires more strictness, low base rate.

## Decision — chosen orientation

A', as a FEASIBILITY ORIENTATION only. This memo records intent to pursue the compression
wake question through its gates. It is NOT an edge claim, NOT a wake authorization, and
does NOT open the seal.

Rationale (on record): A' is the only path that faces the original compression intuition
directly while staying inside available data. The prior is skeptical — it fights
volatility persistence (quiet tends to stay quiet) — and a clean null would be a real
finding, not a loss.

## Seal status — INTACT

This memo opens nothing. The wake seal remains in force. Two gates stand between this
orientation and any forward / outcome computation:

- Gate 1 — Episode-count audit RUN. Feature-side only; counts compression episodes;
  computes no forward / outcome values. Separate run authorization, against the frozen
  design committed at 91401b1. Does not open the seal.
- Gate 2 — Wake-design authorization. Only if Gate 1 clears with adequate episode density.
  Full freeze-before-data ritual. The wake seal may be opened deliberately here, and only
  here, if separately authorized.

## Pre-frozen design constraint for any future A' wake design

A compression wake design must test compression's predictive content INCREMENTAL to
trailing realized volatility (and a volatility-persistence baseline) — per the Atlas
card's "beat 'vol is simply low'" bar. A raw compression-to-expansion test that omits the
vol baseline would rediscover volatility clustering and misattribute it to compression.
This bar is frozen now so it cannot be dropped later in pursuit of a positive result.

## Next eligible action

Episode-count audit RUN authorization (separate prompt), implementing the frozen design
committed at 91401b1, with run-time guards and the boundary-run clarification (a run still
above threshold at the sample's first or last session counts as one episode).

## This memo does NOT authorize

running the audit; computing any wake / outcome / target / future-return / future-range /
future-volatility / expansion values; the wake test; any predictive claim; gate; alpha
spend; sealed 2023+ access; the Option-B new-data project; any change to the CR closure
decision or the Atlas.
