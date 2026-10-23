# SHES Prompt 7 — IEEE123 feeder-derived fault probe audit (2026-10-23)

## Status
PASS for limited phase-aware fault-element snapshot study; NOT PASS for verified relay-zone assignments or restoration safety.

## CI evidence
- Successful original fault run: https://github.com/Arithmetic-Power-Geometry/Self-Healing-Energy-Systems/actions/runs/39956030167
- Latest successful workflow including topology candidates: https://github.com/Arithmetic-Power-Geometry/Self-Healing-Energy-Systems/actions/runs/39956358400
- Earlier runs 39955893544 (Python import path) and 39955958159 (incorrect DSS-Python Lines API) failed and were repaired.
- 5 unit tests pass; independent JSON validator passes.
- Source and result: `shes/run_ieee123_fault_probes.py`, `shes/validate_fault_probes.py`, `shes/test_fault_probes.py`, `shes/ieee123_fault_probe_result.json`.

## Pinned provenance
Upstream tshort/OpenDSS commit `5005c668a72d20775f4c2d060feebb2866ba1d38`, dss-python==0.15.7, Ubuntu 24.04, Python 3.11.
Four DSS dependency SHA256s stored in result JSON. The linecode case alias is a byte-identical copy.

## Observed values
54 converged fault-element snapshot solves: 3 named buses (150,60,83), 3 phases each, 3 resistances (0.01,0.1,1.0 ohm), 2 configurations (published, Line.l1 disabled). The selected Line.l1 connects bus 1 to bus 2. The fault-element current range is 1206.9838652226485 to 240164.2417173114 A.
For bus 150, phase 1, published state: 0.01 ohm -> 240163.19576229007 A; 0.1 ohm -> 24017.51323733001 A; 1.0 ohm -> 2401.752561675008 A.
The large currents reflect the idealized source/fault model and are not measured relay currents or device ratings.

## Protection-zone mapping: IMPORTANT NEGATIVE RESULT
`shes/candidate_protection_paths.py` constructs candidate upstream line paths and marks all inferred assignments unverified. In the actual feeder, the line-only graph from bus 150 to buses 60 and 83 returned no paths. Consequently the JSON correctly contains null candidate primary and backup boundaries for both targets. This is a topology-model limitation, likely requiring transformer/regulator connectivity and energized switching state. Do not invent primary/backup relay identities or claim verified protection zones.
No real installed relay inventory, CT ratios, breaker delays, directionality, feeder fault duty validation or inverter current limiting were established.

## Manuscript
Committed `shes/ieee123_fault_probe_section.tex` documenting only verified phase-aware fault observations. Local manuscript assembly includes the new section and a 16-page bibliography-resolved PDF. Full `main.tex` and binary figures remain in local package rather than GitHub.

## Next work
Build electrically connected multigraph including transformer/regulator terminals and switch states; distinguish reachable buses and de-energized island effects; extract line/transformer terminal currents; assign explicitly hypothetical relays to physical protective devices only with grounded inventory; then test primary/backup inequalities under calibrated uncertainty.
