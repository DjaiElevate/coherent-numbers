# Cusp Geometry Lane v0.3 - Sandbox Gate Report

instrument_commit_sha: 4536be27f6955be72bdb7abad4b4cb38ac1278ad
sandbox_file: data/raw/market/spy_yahoo_adjclose_20050101_20221231_sandbox_from_v8.csv
sandbox_sha256: 5cd925026d37c1825363db525483ecc454e680ea21d1addfe1c83cb134ea5901
close_column_used: adj_close
bootstrap_seed_pinned: 2026061201
first_loaded_date: 2005-01-03
last_loaded_date: 2022-12-30
num_closes_loaded: 4531
num_records_make_records: 209

## Folds
fold | n_test (fold size) | n_train (after purge)
   0 |   20 |   186
   1 |   21 |   182
   2 |   21 |   182
   3 |   21 |   182
   4 |   21 |   182
   5 |   21 |   182
   6 |   21 |   182
   7 |   21 |   182
   8 |   21 |   182
   9 |   21 |   185

## Per-fold model comparison
fold | MSE_M0 | MSE_M1 | improved | F2_sign | F2_coef
   0 | 1.0038195331e-01 | 1.0475361507e-01 | False | - | -6.204001e-01
   1 | 2.3741364231e-01 | 2.4357654396e-01 | False | - | -5.364242e-01
   2 | 1.4519637436e-01 | 1.5182674345e-01 | False | + | +3.838415e-01
   3 | 1.5001774892e-01 | 1.5564463126e-01 | False | + | +5.699899e-01
   4 | 1.1613909911e-01 | 1.1704929001e-01 | False | + | +2.593287e-01
   5 | 1.9880695383e-01 | 1.9894763992e-01 | False | + | +1.102121e-01
   6 | 2.2105388844e-01 | 2.2605788581e-01 | False | + | +3.713320e-01
   7 | 2.1171831976e-01 | 2.2348708132e-01 | False | - | -7.831614e-01
   8 | 2.2703166779e-01 | 2.2986066170e-01 | False | - | -3.659459e-01
   9 | 9.9178314282e-02 | 9.9593831170e-02 | False | - | -1.193441e-01

## Pooled out-of-fold
pooled_SSE_M0: 3.5745315251e+01
pooled_SSE_M1: 3.6662002782e+01
pooled_incremental_R2: -2.5644969815e-02
num_improving_folds: 0 / 10
PASS_condition: incremental_R2 > 0 AND improving >= 7
RESULT: FAIL

No sealed data was accessed.
