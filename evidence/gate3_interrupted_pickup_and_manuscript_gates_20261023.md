# Gate 3 interrupted pickup, literature audit, and manuscript decision (2026-10-23)

## Executed experiment
Python locally executed, seed 20261023, 20,000 synthetic two-pulse fault-current traces. Definite-time relay pickup resets completely when current falls below threshold. Static certificate requires high current above pickup and required dwell <= deadline, but ignores dropout. Outcomes: static approved 19,135; static false approvals 6,457; persistence-aware approved 12,678; persistence-aware false approvals 0. This is a **model counterexample**, not a hardware validation or inverse-time curve. In this toy model, the persistence-aware rule is exact by construction. No feeder impedance, OpenDSS short-circuit, GFM control, or EMT simulation involved.

## Three verified references
1. Gross, Ramasubramanian and Paz, *Universal Input-Output Model of GFM Functions and Data-Driven Verification Methods*, NREL/TP-5D00-88646 (2024), DOI 10.2172/2318960. Verified OSTI record.
2. Muenz et al., *Protection of 100% Inverter-dominated Power Systems with Grid-Forming Inverters and Protection Relays: Gap Analysis and Expert Interviews*, Sandia SAND2024-04848 (2024), public report cover. No DOI asserted.
3. Rauf, Batool and Madni, *Comprehensive Review of Fault Detection and Protection Strategies for Medium-Voltage Networks Supplied by Grid-Forming Inverter Sources*, Energies 19(9):2175 (2026), DOI 10.3390/en19092175. Verified publisher record.

Bibliography now 58 entries, including reports and standards, **not** 58 journal papers. Metadata screening does not imply full-text critical review.

## Manuscript start decision
A full submission-ready manuscript should NOT be written now. Prepare a provisional outline only. Release manuscript lock after (i) successful independent IEEE123 power-flow/short-circuit execution with archived solver outputs; (ii) protection curves and primary/backup fault-location tests based on electrical feeder currents; (iii) independent dynamic/EMT tests of GFM current limit, CLPU and relay behavior; (iv) novelty comparison to Bassey 2020, Sandia 2024, Maharjan 2025 and recent GFM protection papers; (v) independent reproduction of certificate tests and negative cases. The proposed novelty is a **joint action-specific sufficient safety certificate**, not protection-aware restoration or fault-current limitation by themselves. If no defensible gap survives, stop or pivot instead of claiming novelty. Gate 3 OPEN; manuscript LOCKED.
