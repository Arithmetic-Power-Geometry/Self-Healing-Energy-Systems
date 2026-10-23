# SHES Prompt 8 — expanded feeder topology and hypothetical relay boundaries

## Independently successful CI
Run https://github.com/Arithmetic-Power-Geometry/Self-Healing-Energy-Systems/actions/runs/39956981716 completed SUCCESS.
- 5 adversarial unit tests passed.
- Pinned OpenDSS feeder compiled using DSS-Python 0.15.7.
- 9 fault-case terminal-current probes converged.
- Independent result validator passed, then GitHub Actions committed `shes/ieee123_topology_result.json`.
- The result includes SHA256 hashes of feeder dependencies and the pinned upstream commit.

## Corrected Prompt 7 null path
The earlier line-only graph omitted transformer/regulator adjacency. Expanded enabled-element graph: 126 lines, 8 transformers. Source bus 150.
- Bus 60: 12-edge candidate path, terminal candidate Line.l58, upstream candidate Line.l55.
- Bus 83: 23-edge candidate path, terminal candidate Line.l84, upstream candidate Line.l82.
- No actual installed relay inventory or protection settings. Paths are element adjacency, not proven phase-specific energized connectivity or verified protection zones.

## Feeder-derived terminal current example
Bus 60, single-phase fault on phase 1, Rf=0.1 ohm:
- candidate primary Line.l58, terminal 1, conductor 1: 3366.8246897065187 A.
- candidate backup Line.l55, terminal 1, conductor 1: 3366.8243247749147 A.
- bus 60 per-unit voltage magnitudes: [0.13718527966860486,1.2355282609163067,1.135914126119503].
Conductor identity is NOT independently mapped to physical CT phase; do not call these verified relay inputs. Large fault-related voltages/currents are model outputs, not measured safety limits.

## Uncertainty treatment
`shes/terminal_current_model.py` defines explicit independent-box and common-derating intervals and hypothetical breaker delays, all flagged `calibrated_to_equipment=false`. There are no field measurements for parameter calibration; actual breaker delay, pickup, reset and inverse-time settings remain unverified.

## Scientific limitations
Topology shortest paths do not guarantee energized phase continuity or radial protection paths; regulator and transformer winding behavior requires further examination. Open/closed switch states are not yet exhaustively reconstructed. Current magnitudes are steady-state DSS snapshot fault results, not time-domain inverter-limited current trajectories. The source bus is 150, so no upstream primary/backup exists for fault at source bus 150 in the selected graph. No field reliability or restoration safety claim.

## Manuscript and remaining packaging
`shes/ieee123_topology_section.tex` committed, with verified tables and example. The full `shes/main.tex`, references and binary figures remain an outstanding transfer task. The current work does not establish a newly compiled full bibliography-resolved manuscript PDF; do not describe it as such unless separately verified.
