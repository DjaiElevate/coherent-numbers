"""
Cusp Geometry Lane - frozen reference implementation v0.3
Status: DRAFT FOR FREEZE. Pure functions only. No data loaders by design:
this file must never acquire market data I/O; the loader lives in a separate
module under its own commit and may only feed `closes` into make_records().

v0.2 changes (external review, pre-data, k=0):
  - B6 linearized-curvature baseline: mean |z_{i+1}-z_i| over the feature window.
  - make_records(closes) -> rows: frozen row construction (alignment, stride,
    target timing are part of the instrument, not the later plumbing).
  - Self-test is a reduced SMOKE TEST verifying the calibration regime within
    broad tolerances. The archived calibration of record is: per-vertex cusp
    rates by EXACT quadrature (exact_cusp_rate), window statistics by
    null_calibration(100_000, 30_000, seed=SEED_CALIB).
  - Lookahead perturbation test: proves features/baselines of a row depend only
    on closes up to its anchor, and y only on the forward span.

v0.3 changes (pre-freeze hardening, k=0):
  - make_records takes nothing but closes; stride is NOT a parameter.
  - purged_blocked_folds(n_records) frozen in code: the evaluator may only
    consume its output, never re-decide split logic.
  - Version bumped so every circulated artifact has a unique (name, hash).

Geometry imported unchanged from living-line v0.3:
  THETA_CUSP = 2.5 rad; kappa = |dtheta| / mean adjacent step length.
Embedding (Isometry Convention): step_i = (1, z_i), z_i = r_i / sigma_lagged.
"""
import math, random

THETA_CUSP = 2.5      # imported from living-line v0.3, unchanged
W_SIGMA    = 63       # trailing RMS window for standardization (lagged)
W_FEAT     = 63       # feature window: 63 standardized steps -> 62 vertices
STRIDE     = 21       # sampling stride in bars (records every 21st step)
H_TARGET   = 21       # forward realized-vol horizon
MIN_REG    = 30       # minimum regular vertices for a valid window
PURGE      = 3        # CV purge width in records each side (W_FEAT/STRIDE)
N_FOLDS    = 10       # contiguous CV blocks
MIN_RECORDS= 40       # minimum records for a valid fold plan
SEED_CALIB = 20260612 # pinned seed for null calibration (full and smoke)

# ---------- core transforms ----------

def log_returns(closes):
    """r[j] = ln closes[j+1] - ln closes[j].  Step j runs close j -> close j+1."""
    return [math.log(closes[j+1] / closes[j]) for j in range(len(closes) - 1)]

def lagged_sigma(r, i, w=W_SIGMA):
    """RMS of r[i-w : i] (strictly excludes step i). None if short or zero."""
    if i < w: return None
    s = sum(x * x for x in r[i-w:i])
    if s <= 0: return None
    return math.sqrt(s / w)

def standardize(r):
    """z[i] = r[i] / sigma_lagged(i); None where sigma unavailable (i < W_SIGMA)."""
    return [ (r[i] / s) if (s := lagged_sigma(r, i)) else None
             for i in range(len(r)) ]

# ---------- vertex geometry (v0.3, unchanged) ----------

def vertex(z1, z2):
    """('cusp', None) or ('reg', kappa). Speed >= 1 always in this embedding."""
    dth = abs(math.atan(z2) - math.atan(z1))
    if dth >= THETA_CUSP:
        return ('cusp', None)
    m = (math.sqrt(1 + z1*z1) + math.sqrt(1 + z2*z2)) / 2.0
    return ('reg', dth / m)

def cusp_boundary(z1):
    """Required opposite z2 for a cusp given z1 (None if impossible)."""
    a = math.atan(z1) - THETA_CUSP
    return math.tan(a) if a > -math.pi/2 else None

# ---------- window statistics ----------

def window_features(zs):
    """F1..F4 over one window of standardized steps. None if invalid."""
    if any(z is None for z in zs): return None
    cusps, regs, plen = 0, [], 0.0
    for z in zs: plen += math.sqrt(1 + z*z)
    for i in range(len(zs) - 1):
        kind, k = vertex(zs[i], zs[i+1])
        if kind == 'cusp': cusps += 1
        else: regs.append(k)
    if len(regs) < MIN_REG: return None
    return {
        'F1_cusp_count': cusps,
        'F2_kappa_mean': sum(regs) / len(regs),     # PRIMARY
        'F3_kappa_max':  max(regs),                  # descriptive (ceiling ~1.13)
        'F4_pathlen':    plen / len(zs),
    }

def linearized_b6(zs):
    """B6 = mean |z_{i+1} - z_i| over the window: F2's small-z approximation."""
    n = len(zs) - 1
    return sum(abs(zs[i+1] - zs[i]) for i in range(n)) / n

def forward_log_rv(r, t, h=H_TARGET):
    """ln RMS of r[t+1 : t+1+h]; strictly future. None if insufficient."""
    seg = r[t+1 : t+1+h]
    if len(seg) < h: return None
    s = sum(x * x for x in seg)
    if s <= 0: return None
    return math.log(math.sqrt(s / h))

def baselines(r, logp, t):
    """B1..B5 at step t. Trailing windows INCLUDE step t (causal). None if invalid."""
    if t < 63: return None
    rv63 = lagged_sigma(r, t+1, 63); rv21 = lagged_sigma(r, t+1, 21)
    if not rv63 or not rv21: return None
    seg63 = r[t-62:t+1]; seg21 = r[t-20:t+1]
    mu = sum(seg63) / 63
    var = sum((x-mu)**2 for x in seg63) / 63
    if var <= 0: return None
    ac1 = sum((seg63[i]-mu)*(seg63[i+1]-mu) for i in range(62)) / 62 / var
    win_logp = logp[t-62:t+2]
    return {
        'B1_ln_rv63': math.log(rv63),
        'B2_ln_rv21': math.log(rv21),
        'B3_abs_ret21': abs(sum(seg21)),
        'B4_range63': max(win_logp) - min(win_logp),
        'B5_ac1_63': ac1,
    }

# ---------- frozen row construction ----------

def make_records(closes):
    """closes -> modeling rows. THIS IS PART OF THE FROZEN INSTRUMENT.
    Takes nothing but closes; stride is frozen at STRIDE and is not a parameter.
    Row anchor t is a step index: feature window = z[t-62 ... t]; baselines at t;
    target = ln RMS of r[t+1 ... t+21]. First valid anchor t = W_SIGMA + W_FEAT - 1
    = 125; anchors advance by `stride`. Rows with any invalid component are skipped
    (never imputed)."""
    r = log_returns(closes)
    logp = [math.log(c) for c in closes]
    z = standardize(r)
    stride = STRIDE
    rows = []
    t = W_SIGMA + W_FEAT - 1
    while t < len(r):
        zs = z[t - (W_FEAT - 1): t + 1]
        f = window_features(zs) if len(zs) == W_FEAT else None
        b = baselines(r, logp, t)
        y = forward_log_rv(r, t)
        if f is not None and b is not None and y is not None:
            row = {'t': t}
            row.update(f); row.update(b)
            row['B6_mean_abs_dz'] = linearized_b6(zs)
            row['y_ln_fwd_rv21'] = y
            rows.append(row)
        t += stride
    return rows

def purged_blocked_folds(n_records):
    """Frozen CV split. N_FOLDS contiguous blocks; block b = [floor(b*n/10),
    floor((b+1)*n/10)). Training excludes every index within PURGE records of
    either test-block boundary. THIS IS PART OF THE FROZEN INSTRUMENT: the
    evaluator may only consume this output."""
    n = n_records
    if n < MIN_RECORDS:
        raise ValueError(f"need >= {MIN_RECORDS} records, got {n}")
    folds = []
    for b in range(N_FOLDS):
        lo, hi = (b * n) // N_FOLDS, ((b + 1) * n) // N_FOLDS
        test = list(range(lo, hi))
        train = [i for i in range(n) if i < lo - PURGE or i >= hi + PURGE]
        folds.append((train, test))
    return folds

# ---------- synthetic null calibration (canonical generator) ----------

def _draw(dist, rng):
    if dist == 'gauss': return rng.gauss(0, 1)
    zg = rng.gauss(0, 1); c = sum(rng.gauss(0, 1)**2 for _ in range(4))
    return (zg / math.sqrt(c/4)) / math.sqrt(2.0)   # t(4), unit variance

def exact_cusp_rate(dist):
    """Deterministic per-vertex cusp probability for iid unit-variance steps.
    P = 2 * Int_{z1>L} f(z1) * F(tan(atan(z1) - THETA_CUSP)) dz1,
    L = tan(THETA_CUSP - pi/2). Gaussian via erf; t(4) via closed-form CDF
    F_4(t) = 1/2 + (3/4)u - (1/4)u^3, u = t/sqrt(t^2+4), scaled to unit variance."""
    if dist == 'gauss':
        f = lambda x: math.exp(-x*x/2) / math.sqrt(2*math.pi)
        F = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    else:
        f = lambda x: (3*math.sqrt(2)/8) * (1 + x*x/2) ** -2.5
        def F(x):
            t = math.sqrt(2) * x; u = t / math.sqrt(t*t + 4)
            return 0.5 + 0.75*u - 0.25*u**3
    L = math.tan(THETA_CUSP - math.pi/2)
    a, b, n = L + 1e-9, 50.0, 200_000   # Simpson, even n
    h = (b - a) / n
    def g(z1): return f(z1) * F(math.tan(math.atan(z1) - THETA_CUSP))
    s = g(a) + g(b)
    for i in range(1, n):
        s += g(a + i*h) * (4 if i % 2 else 2)
    return 2 * s * h / 3

def null_calibration(n_vertices, n_windows, seed=SEED_CALIB):
    """Synthetic null table. No market data. Deterministic given (sizes, seed).
    Archived run of record: null_calibration(100_000, 30_000); cusp rates of
    record come from exact_cusp_rate (quadrature), with MC as cross-check."""
    rng = random.Random(seed); out = {}
    for dist in ('gauss', 't4'):
        z1 = _draw(dist, rng); c = 0
        for _ in range(n_vertices):
            z2 = _draw(dist, rng)
            if abs(math.atan(z2) - math.atan(z1)) >= THETA_CUSP: c += 1
            z1 = z2
        f2, f3, f4, b6, anycusp = [], [], [], [], 0
        for _ in range(n_windows):
            zs = [_draw(dist, rng) for _ in range(W_FEAT)]
            f = window_features(zs)
            f2.append(f['F2_kappa_mean']); f3.append(f['F3_kappa_max'])
            f4.append(f['F4_pathlen']);    b6.append(linearized_b6(zs))
            if f['F1_cusp_count'] > 0: anycusp += 1
        m  = lambda a: sum(a)/len(a)
        sd = lambda a: (sum((x-m(a))**2 for x in a)/len(a))**0.5
        sf2, sf3 = sorted(f2), sorted(f3)
        q = lambda a, p: a[int(p*len(a))]
        mf2, mb6 = m(f2), m(b6)
        cov = sum((f2[i]-mf2)*(b6[i]-mb6) for i in range(len(f2))) / len(f2)
        corr = cov / (sd(f2)*sd(b6))
        out[dist] = {'cusp_rate': c/n_vertices, 'p_window_cusp': anycusp/n_windows,
                     'F2_mean': mf2, 'F2_sd': sd(f2),
                     'F2_q05': q(sf2, 0.05), 'F2_q95': q(sf2, 0.95),
                     'F3_med': q(sf3, 0.50), 'F3_q95': q(sf3, 0.95),
                     'F4_mean': m(f4), 'F4_sd': sd(f4),
                     'B6_mean': mb6, 'B6_sd': sd(b6),
                     'corr_F2_B6': corr}
    return out

# ---------- smoke test ----------

if __name__ == '__main__':
    # geometry boundary
    b = cusp_boundary(3.0)
    assert b is not None and abs(b + 3.019) < 0.01, b
    assert cusp_boundary(1.0) is None or cusp_boundary(1.0) < -100

    # reduced-sample calibration regime check (NOT the archived full table)
    tab = null_calibration(200_000, 5_000)
    g, t4 = tab['gauss'], tab['t4']
    for k in ('gauss', 't4'):
        d = tab[k]
        print(f"{k:5s}: cusp_rate={d['cusp_rate']:.2e} P(win cusp)={d['p_window_cusp']:.4f} "
              f"F2={d['F2_mean']:.4f}±{d['F2_sd']:.4f} B6={d['B6_mean']:.4f}±{d['B6_sd']:.4f} "
              f"corr(F2,B6)={d['corr_F2_B6']:.4f} F4={d['F4_mean']:.4f}")
    assert g['cusp_rate'] < 1e-4 and t4['cusp_rate'] > g['cusp_rate']
    eg, et = exact_cusp_rate('gauss'), exact_cusp_rate('t4')
    assert 5e-6 < eg < 2e-5 and 2e-4 < et < 4e-4, (eg, et)
    assert abs(t4['cusp_rate'] / et - 1) < 0.35   # MC consistent with quadrature
    assert 0.50 < g['F2_mean'] < 0.62 and 1.30 < g['F4_mean'] < 1.41
    assert 0.60 < g['corr_F2_B6'] < 0.85 and 0.40 < t4['corr_F2_B6'] < 0.70

    # frozen row construction: alignment, stride, causality
    rng = random.Random(7)
    closes = [100.0]
    for _ in range(420):
        closes.append(closes[-1] * math.exp(rng.gauss(0, 0.01)))
    rows = make_records(closes)
    assert rows and rows[0]['t'] == W_SIGMA + W_FEAT - 1 == 125
    assert all(rows[i+1]['t'] - rows[i]['t'] == STRIDE for i in range(len(rows)-1))
    expected = 1 + (len(closes) - 1 - 1 - H_TARGET - 125) // STRIDE
    assert len(rows) == expected, (len(rows), expected)

    # lookahead perturbation: bump a close inside row-1's TARGET span only
    t1 = rows[1]['t']
    closes2 = list(closes); closes2[t1 + 12] *= 1.05
    rows2 = make_records(closes2)
    keys_feat = [k for k in rows[1] if k not in ('y_ln_fwd_rv21',)]
    assert all(abs(rows2[1][k] - rows[1][k]) < 1e-12 for k in keys_feat if k != 't')
    assert abs(rows2[1]['y_ln_fwd_rv21'] - rows[1]['y_ln_fwd_rv21']) > 1e-9
    assert all(abs(rows2[0][k] - rows[0][k]) < 1e-12 for k in rows[0] if k != 't')
    # frozen fold plan: partition, purge, determinism
    for n in (208, 53):
        folds = purged_blocked_folds(n)
        allt = sorted(i for _, te in folds for i in te)
        assert allt == list(range(n)), "test blocks must partition the records"
        for tr, te in folds:
            lo, hi = te[0], te[-1] + 1
            assert te == list(range(lo, hi))
            assert all(i < lo - PURGE or i >= hi + PURGE for i in tr)
            assert tr, "every fold must keep nonempty training data"
        assert folds == purged_blocked_folds(n), "split must be deterministic"
    try:
        purged_blocked_folds(MIN_RECORDS - 1); assert False
    except ValueError:
        pass
    print(f"rows={len(rows)} first_t={rows[0]['t']} | causality, alignment, and fold plan verified.")
    print(f"exact cusp rates: gauss={exact_cusp_rate('gauss'):.3e} t4={exact_cusp_rate('t4'):.3e}")
    print("smoke test OK (reduced sample; rates of record = quadrature; windows of record = 100k/30k run).")