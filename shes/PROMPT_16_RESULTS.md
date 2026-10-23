# SHES Prompt 16 — winding and fault-current model audit

## Verified execution
GitHub Actions run https://github.com/Arithmetic-Power-Geometry/Self-Healing-Energy-Systems/actions/runs/39966863934 SUCCESS. Twelve regression tests passed, independent structural evidence validation passed, archived artifact 12507705512.
Pinned upstream IEEE 123-bus OpenDSS revision: 5005c668a72d20775f4c2d060feebb2866ba1d38.
Pinned dss-python version: 0.15.7.

## Extracted model evidence
Eight transformer records with per-winding OpenDSS connection code, nominal voltage, nominal kVA, tap and terminal bus labels. These are metadata, not verified winding phase-transfer matrices or grounding impedance.
Four converged phase-1 0.1-ohm single-line-to-ground faults: published bus 60 fault-voltage 0.13718527966860486 pu, bus 83 0.07545516959818346 pu; Line.sw1-disabled bus 60 and bus 83 both 0 pu. Signed complex terminal currents recorded for Line.l58, Line.l55, Line.l84 and Line.l82, in OpenDSS terminal-into-element convention.
The zero-voltage cases are not valid evidence of energized post-switch protection. No physical restoration certificates issued.

## Open scientific gaps
- No independent transformer/regulator phase-transfer matrix or neutral grounding audit completed.
- No independent source-reachable energized phase graph proved.
- No thermal or voltage adequacy certificate; numerical convergence is not operational feasibility.
- No installed CT orientation, protection zones, relay settings or inverter transient calibration.
- No meaningful positive pre/post restoration fault-current comparison because selected disabled state loses voltage at both monitored buses.
- The separate LaTeX section has not been integrated into the full manuscript and full clean manuscript GitHub CI is not yet verified.

## Prompt 17
Develop a unified controlled benchmark comparing nominal, common-derating, independent rectangular endpoint and explicit time-domain relay screens on the SAME scenario set, with reset semantics, uncertainty correlations and frequency criteria specified. Include independent ground truth and a robust adversarial suite, wall-clock timings, approval/false-approval/conservative-rejection tables and ablations. Distinguish synthetic protection model evidence from physical feeder restoration and do not label a finite-corner oracle a continuum proof.
