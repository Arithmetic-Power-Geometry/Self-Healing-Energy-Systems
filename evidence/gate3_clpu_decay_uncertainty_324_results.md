# Executed CLPU uncertainty sweep

Date: 2026-10-22. Local Python and SciPy execution of `evidence/gate3_clpu_decay_uncertainty_sweep.py`.

Parameter grid: CLPU {0.05, 0.2, 0.4}, current cap {0.7, 1.0, 1.4}, pickup {0.6, 1.0, 1.3}, delay {0.08, 0.2}, frequency limit {0.12, 0.25}, decay tau {0.15, 0.4, 1.2}. Total 324.

Observed output: `{'total': 324, 'certified': 60, 'baseline_safe': 66, 'false_accept': 0, 'conservative': 6}`.

Earlier 108-case tau=0.4 baseline: 20 certified, 22 safe, 0 observed unsafe, 2 conservative. Certificate does not use tau, so triple certified count is expected. Scalar surrogate with sampled 3-second ODE trajectory; not IEEE123 electrical simulation, EMT, physical relay evidence, or mathematical soundness proof. Gate 3 OPEN.
