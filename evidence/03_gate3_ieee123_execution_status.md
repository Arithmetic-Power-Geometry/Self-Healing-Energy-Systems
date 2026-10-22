# Gate 3 — IEEE123 executable baseline handoff (2026-10-22)

## Completed
- Independently checked DSS-Python installation guidance and API: https://dss-extensions.org/DSS-Python/ and https://github.com/dss-extensions/DSS-Python.
- Inspected IEEE123Master.dss and Run_IEEE123Bus.DSS from https://github.com/tshort/OpenDSS/tree/master/Distrib/IEEETestCases/123Bus via connected GitHub.
- Created fail-closed executable driver evidence/run_ieee123_baseline.py. It checks recursive DSS dependencies, SHA256 hashes every source file, invokes an isolated DSS engine, requires convergence and writes voltage range, engine version, node count and provenance.
- Tested local environment: import dss failed (No module named 'dss'). Attempted pip install dss-python==0.15.7; pip failed because DNS resolution unavailable. Thus **NO electrical load flow was run**.
- Missing upstream IEEELinecodes.DSS remains unresolved; do not fabricate line impedances or substitute another feeder's linecodes.

## Reproduction steps on a network-enabled machine
1. Obtain the complete IEEE123 distribution feeder folder from an EPRI-authorized or properly attributed repository. Preserve exact revision, license and all dependencies.
2. Python 3.10–3.12 recommended, install pinned dss-python==0.15.7 in clean environment.
3. python evidence/run_ieee123_baseline.py --feeder /absolute/path/to/123Bus --output evidence/ieee123_baseline_result.json
4. Compare bus voltages, losses and line currents against official published reference before extending to inverter.
5. Build an independently validated GFM inverter dynamic/EMT model, fault model and relay time-current model; connect to feeder only after validating each component.
6. No manuscript or Gate 4 until credible independent electrical validation exists.

## Adversarial checks for next run
- Ensure no hidden unresolved DSS Redirect/Compile dependencies.
- Verify feeder provenance, numerical tolerances, solver convergence and actual voltage range.
- Validate unbalanced phases, regulator control and transformer taps against reference.
- Do not use a static load flow as an inverter transient safety benchmark.
- Treat failed dependency, missing engine, nonconvergence or invalid voltage as a HARD FAIL.

## Current outcome
**BLOCKED**: model source only partially available, DSS engine unavailable, no static feeder baseline, no dynamic GFM/protection baseline, no physical certificate. Script is reproducible preparation, not an executed result.
