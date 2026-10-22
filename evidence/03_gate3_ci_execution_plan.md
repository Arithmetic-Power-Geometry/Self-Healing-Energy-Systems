# Q1 Gate 3 — remote CI execution protocol (2026-10-22)
A GitHub Actions workflow has been committed to attempt an actual IEEE123 load flow using a network-enabled runner. It installs dss-python==0.15.7, checks out upstream tshort/OpenDSS at pinned revision 5005c668a72d20775f4c2d060feebb2866ba1d38, and executes evidence/run_ieee123_baseline.py. If a dependency is missing or convergence fails, the job must fail. The workflow uploads output only if produced.

**This commit does not establish a successful run.** GitHub workflow execution and its logs/artifact must be inspected before claiming electrical results. No inverter dynamics or relay coordination are modeled in this workflow.

Potential known failure: the exact-path IEEELinecodes.DSS file was not available from earlier GitHub connector fetch; source tree may use a different case or location. Resolve from actual checkout rather than fabricate line impedance data.

Manual trigger: GitHub repository > Actions > IEEE123 static baseline (Gate 3) > Run workflow.
Success criterion: green job plus JSON with converged=true, nonempty voltage nodes, SHA256 source provenance and solver version. Next stage is cross-check published feeder voltages, then add validated GFM/relay dynamics and independent EMT comparison.
