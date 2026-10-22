# Gate 3 IEEE123 voltage plausibility validation — 2026-10-22

## Change
The static IEEE123 runner now refuses to report PASS if any per-unit bus voltage is NaN/Inf or if any value is outside [0.5,1.5] pu. These are intentionally broad numerical plausibility checks, **not** operational voltage-code limits or proof of a correct power-flow solution. Previously only nonpositive voltage was rejected.

## Why
A solver can mark convergence while results are physically implausible, and a min/max-only check could conceal nonfinite values. Both scenarios (control mode off and static controls) must independently pass.

## Provenance
Source: evidence/run_ieee123_baseline.py. No new reference was required; reference/master.bib remains unchanged.

## Still not validated
No verified GitHub Actions job logs, feeder voltages, regulator tap benchmark, current-limited GFM transient model, relay coordination, independent EMT/DAE comparison, or H2 soundness theorem. Manuscript locked; Gate 3 open.

## Next
Execute GitHub Actions, inspect run logs and upload artifact, compare computed feeder voltages against an independent reference, then integrate verified dynamic models.
