# Microscope / Instrument Program Charter

**Version:** v0.1  
**Date:** May 12, 2026  
**Project:** Coherent Numbers  
**Status:** Initial charter. Governs the instrument-testing program inaugurated after the Harmonic Calendar MVT closed at commit `371ca9c`.

---

## Preamble

The Coherent Numbers two-layer finding holds that pressure dynamics are universal across assets while the structural response is asset-specific. This implies that any instrument that resolves market structure must be asset-tuned, and an asset-tuned instrument requires a library of independently validated lenses.

This charter governs the program that builds that library. The Harmonic Calendar MVT (closed `371ca9c`, verdict null on both registered outcomes for SPY 1993-2024) demonstrated that a single lens can fail cleanly under pre-registered discipline. The broader question is not whether any one lens resolves structure on any one asset; it is whether a library of independently-tested lenses, evaluated against multiple assets and outcomes, eventually supports a combined adaptive instrument.

The program's working object is a matrix of cells. Each cell is a (lens, asset, outcome) triple. Each cell is a separate pre-registered test with its own verdict. The pattern of verdicts across cells is the finding. No single cell is the program.

This charter does not select which cell is tested next, and does not endorse any specific lens or asset as a priority. It defines the rules under which any cell test is conducted and reported.

## Registry

Each test in the program is a pre-registered artifact authored before data contact.

A registered test consists of: a named lens (formal definition, not a label), a named asset (with frozen-data reference and hash), a registered outcome set, a registered control set, registered thresholds, a registered train/holdout split, and a results artifact path. A test that lacks any of these is not registered and cannot produce a program verdict.

The pre-registration discipline that governed the Harmonic Calendar MVT extends to every cell: design memo committed before any data is loaded into the cell's analysis path. No quiet data contact during memo drafting. Frozen data is acquired and hash-recorded in its own commit, separate from analysis code. Verdict runs occur exactly once per registered test.

The future repository structure for housing cell tests is targeted as: `protocols/<lens>_<asset>_<version>/` containing memo, frozen data reference, orchestration, tests, and results, with the existing `docs/`, `src/`, `tests/`, `data/`, and `results/` directories either reorganized or wrapped. The charter targets this structure; it does not execute reorganization. Reorganization, if undertaken, is a separate audit-chain commit handled outside any active cell test.

Amendments to a registered protocol mid-test are permitted only when a protocol-internal contradiction is surfaced before real-data computation, as occurred between v0.3.1 and v0.3.3 of the Harmonic Calendar MVT. Amendments require their own commit, their own justification, and the explicit confirmation that no real-data outcomes have been observed at the time of amendment.

## Independence and multiple-comparisons posture

Each cell verdict is reported standalone, in its own results artifact, against its own pre-registered thresholds.

One cell passing does not constitute a program-level finding. Phrases of the form "the instrument works" or "the lens is validated" are not licensed by any single pass. One cell failing does not refute the program or the lens; it is data about that specific cell.

Cross-cell replication is the meaningful unit of program-level evidence. A lens that passes its registered thresholds on multiple assets, or a lens that passes on multiple outcomes within an asset, is stronger evidence than any single pass. The program uses cross-cell replication as its primary defense against multiple-comparisons inflation: results from individual cells are reported but not combined into a global claim until replication patterns are themselves analyzed under a separately registered standard.

The program does not adopt a fixed family-wise correction (Bonferroni, Holm, or equivalent) at the charter level, because the family of tests is open-ended. Instead, the discipline is: no cross-cell combined claim without its own pre-registered analysis protocol.

A null verdict on any cell remains a permanent part of the program's record. Nulls are not retired or rerun under different parameters as a matter of routine. A new version of a lens or a new asset is a new cell, not a re-attempt of an existing cell.

## Combination rule

The program does not construct or evaluate an adaptive multi-lens instrument until each lens proposed for inclusion has passed its own pre-registered success criteria on more than one cell.

When that threshold is met, any combination logic — including which lens applies under which asset, regime, or condition — is itself a registered protocol with its own design memo, frozen data, train/holdout split, and verdict. Combination logic is not tuned on observed cell verdicts; it is specified before its evaluation data is seen.

Combined-instrument tests use data that is either entirely untouched by the constituent lens tests, or is held out under a pre-registered split that the constituent tests did not observe. Combination logic that is built by selecting lenses post-hoc on observed performance is outside the program's discipline.

The program's central rule: lenses earn entry before they are combined. The charter exists to make that rule operational.

## Status of this charter

This is v0.1. Amendments are tracked by version. No real-data analysis is governed by versions earlier than v0.1, because v0.1 is the first version.
