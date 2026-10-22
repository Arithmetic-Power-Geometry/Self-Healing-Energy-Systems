# Gate 3: 2592-case scalar surrogate robustness sweep

Executed locally using SciPy on 2026-10-22. Source: evidence/gate3_2592_case_parameter_robustness.py.

Observed stdout: `{"baseline_safe": 486, "certified": 396, "conservative": 90, "false_accept": 0, "total": 2592}`.

Cartesian grid: CLPU (3), current cap (3), relay pickup (3), trip delay (2), frequency limit (2), CLPU decay (3), damping (2), voltage sensitivity (2), inertia (2). Total 2592.

Method: 3-second solve_ivp scalar ODE, rtol 1e-9, atol 1e-11, max_step 0.02, trajectory sampling every 0.02 seconds. Numerical sampling cannot establish continuous-time safety. Simplified algebraic voltage/current and idealized relay conditions are not physical inverter, EMT, or independent feeder validation. No general soundness claim. Gate 3 remains open.
