# SHES Prompt 14 — phase-indexed energized-topology evidence audit

## Scope
Upstream OpenDSS feeder commit: 5005c668a72d20775f4c2d060feebb2866ba1d38
dss-python pinned: 0.15.7
P8 source: shes/ieee123_topology_result.json

## Verified pre-existing element-level candidate paths
Bus 60: 12 element edges; terminal primary candidate Line.l58; backup candidate Line.l55.
Bus 83: 23 element edges; terminal primary candidate Line.l84; backup candidate Line.l82.
The bus 83 path includes the one-phase Transformer.reg4a, despite an element-level phase-3-looking path. Therefore graph adjacency alone is insufficient to establish phase-specific electrical continuity.

## New P14 methods
- Extract line/transformer terminal bus-node strings, conductor counts, element enablement and conductor-open flags directly from OpenDSS.
- Construct line-only phase-indexed candidate edges by conductor position with strict rejection of invalid or open conductors.
- Do not silently infer transformer/regulator winding transfer.
- Adversarial unit tests for phase permutation, conductor opening, disabled lines, mismatched node lists, neutral-only conductors and false bus-level transformer paths.
- Pinned GitHub Actions workflow reruns extraction and fails closed on evidence invariants.

## Limitations and unfinished requirements
- Phase-indexed line graph is NOT a complete energized graph until transformer/regulator transfer is independently resolved.
- A positive bus voltage does not alone prove a closed fault-current path.
- The P8 magnitude-only terminal-current data do not establish CT orientation, signed current direction or installed relay zones.
- P14 does not establish the actual switching-state feasibility of a restoration action; that is the purpose of P15.
- No physical protection or restoration authorization is issued.
- The manuscript section is committed separately; full manuscript build remains blocked by missing complete source package from P12.

## Next prompt
P15: simulate documented pre/post-switch restoration actions, independently validate phase continuity, electrical feasibility, protection-zone changes and fault current direction with explicit transformer mapping, and refuse physical safety claims absent calibrated protection and inverter models.
