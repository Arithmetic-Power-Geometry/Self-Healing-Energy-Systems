# Gate 3 extension — official feeder and GFM reference acquisition (2026-10-22)

## Successfully accessed original GitHub file contents through connector
Upstream: https://github.com/tshort/OpenDSS/tree/master/Distrib/IEEETestCases/123Bus
- IEEE123Master.dss — Git blob SHA 2f4775e5f564cbc9ad348b4d7b00a5b9ae247c7a, 15574 UTF-8 characters
- Run_IEEE123Bus.DSS — SHA f678d579f596b9343be61772d117876563e551b2, 4764 characters
- IEEE123Regulators.DSS — SHA f695011c017946feadcd0f5280f833d8d9680ac4, 1861 characters
- IEEE123Loads.DSS — SHA 452974187c8dcc05e387e1d83cf798db373ed1d7, 8289 characters
- IEEELinecodes.DSS — referenced by master but exact-path fetch returned 404. CASE/PATH/REVISION UNRESOLVED. Therefore no complete, executable feeder snapshot.
The source repo is a community OpenDSS mirror, NOT demonstrated to be EPRI's canonical current distribution. Official EPRI catalog: https://opendss.epri.com/ExamplesDocsandTestCases.html and specifically its IBRDynamics_Cases GFM/GFL IEEE123 examples.
Do not redistribute upstream content until license and attribution are verified. No local OpenDSS engine available.

## Open GFM models and independent simulation candidates
- https://github.com/NatLabRockies/PyPSCAD (README SHA d49df04bf3f64098c14a379ae9e21d1df5b7446f); source GFM/GFL PSCAD averaged-switching models and 9-bus benchmark. PSCAD runtime availability/license unverified.
- https://www.nrel.gov/docs/fy21osti/78402.pdf Kenyon, Sajadi, Hoke & Hodge open-source PSCAD models.
- https://www.osti.gov/biblio/1909842 PNNL IEEE TPWRD 2020 validated 3-phase inverter dynamics with GridLAB-D against EMT and CERTS/AEP field data.
- https://www.pnnl.gov/publications/modeling-grid-forming-inverters-transient-stability-simulations-all-inverter-based PNNL IEEE123 modified GFM distribution model in GridLAB-D, DOI 10.1109/ISGT.2019.8791620.
- https://opendss.epri.com/Dynamics.html OpenDSS supports basic electromechanical dynamics, not a general substitute for EMT.
- https://ieee-pes-data-sharing.org/codes/detail/f0cd8e35-f97e-484d-9565-3a78464a3ced ParaEMT Python open-source BSD-3-Clause, candidate independent EMT baseline.
- https://www.pscad.com/knowledge-base/article/894 EPRI/UIUC/UW/UM grid-forming PSCAD v5 model.

## Required validation chain (NOT completed)
1. Resolve upstream model revision and missing IEEELinecodes.DSS; acquire complete licensed feeder snapshot with SHA256 hashes.
2. Reproduce published steady-state voltages/line currents on IEEE123 using OpenDSS/DSS C-API and record numerical tolerances.
3. Import/construct GFM inverter controls with explicit state-space, current limiter, DC source, droop, fault ride-through, relay curves and cold-load motor inrush; distinguish calibrated parameters from hypothetical.
4. Validate dynamic waveforms against independently implemented EMT/PHIL/field-backed reference; report discrepancy and timestep convergence.
5. Implement a mathematically sound interval/reachability or barrier-based sufficient certificate for explicitly bounded hybrid DAE; compare soundness and coverage with EMT, standard security filter and brute-force dynamic screening.
6. Repeat across switching actions, fault locations, topology variants, protection miscoordination, inverter saturation, uncertainty and out-of-distribution settings.
7. Never infer real-grid safety from a numerical simulator alone.

## Present verdict
OFFICIAL BENCHMARK DISCOVERED; PARTIAL SOURCE CONTENT ACCESSED; EXECUTABLE FEEDER NOT ASSEMBLED; NO ELECTRICAL SIMULATION. Gate 4 remains blocked.
