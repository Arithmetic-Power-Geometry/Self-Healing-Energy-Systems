# SHES Prompt 15: named-switch pre/post OpenDSS sensitivity

## Reproducibility
Pinned upstream OpenDSS revision: 5005c668a72d20775f4c2d060feebb2866ba1d38.
Pinned dss-python version: 0.15.7.
Workflow run: https://github.com/Arithmetic-Power-Geometry/Self-Healing-Energy-Systems/actions/runs/39966371417 (SUCCESS).
Evidence artifact: 12506244690.
Nine adversarial tests passed and independent evidence invariants passed.

## Experiment and observed values
Eight enabled named Line.sw elements were found. The first, Line.sw1, was selected for an outage sensitivity (not a permitted restoration operation). Two freshly compiled snapshots with controls off both converged.
- Published feeder: bus 60 voltages [0.9424651734, 0.9797944305, 0.9602442077] pu; bus 83 [0.9458531088, 0.9830881792, 0.9611122490] pu.
- Line.sw1 disabled: bus 60 [0,0,0] pu; bus 83 [0,0,0] pu.
- Numerical convergence is NOT restoration feasibility. Zero voltages suggest loss of modeled supply but do not independently prove every phase-specific energized path.

## Scientific limitations (fail closed)
- Transformer/regulator terminal buses, conductor and phase counts are extracted, but winding phase transfer is NOT verified.
- Signed element-terminal current data, where available, are simulator convention, not installed CT polarity or a validated relay direction.
- No validated thermal ratings or ampacity screen; no demonstrated energized source reachability.
- No completed pre/post fault-current magnitude and direction comparison; no installed protection-zone changes verified.
- The selected case is a documented named-switch outage sensitivity, not an admissible restoration action. Physical restoration authorization: zero.
- New manuscript section shes/p15_switch_sensitivity_section.tex is separate; full clean manuscript integration/build not established.

## Prompt 16
Build a documented phase-transfer and winding-connection audit for transformers/regulators; verify source-reachable phases and identify any published switch restoration ties with modeled constraints. Independently compare pre/post switching fault-current phasors and protective candidate paths, while refusing physical relay claims absent settings and CT orientation. Reproduce and commit with successful CI.
