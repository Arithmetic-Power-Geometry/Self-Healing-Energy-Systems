# Gate 3 independent result-integrity gate — 2026-10-22

Added evidence/validate_ieee123_result.py as a separate parser and checker for the JSON produced by evidence/run_ieee123_baseline.py. GitHub Actions now requires this independent check after the simulation and before treating the workflow as successful.

Checks: PASS_STATIC_ONLY and IEEE123 identification; all dynamic/protection/EMT claims explicitly false; source hashes present with 64 lowercase hexadecimal digits; exactly two distinct scenarios (static_off, static_controls); explicit convergence; at least 100 voltage nodes; finite ordered voltage extrema within broad [0.5,1.5] pu diagnostic bounds; finite two-component total power.

These are **schema and numerical consistency checks**, not a second electrical solver, an independent feeder benchmark, proof of protection selectivity, or verification of the underlying physical model. The minimum node count is only a broad corruption check, not a benchmark node-count assertion. Workflow execution of this new revision has not been confirmed in this increment.

Next: inspect newly triggered workflow and logs, compare feeder results to independent published values, then test GFM/protection transients. No new reference added. Gate 3 open, manuscript locked.
