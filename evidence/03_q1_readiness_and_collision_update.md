# Q1 readiness gate — 2026-10-22
Status: BLOCKED; no manuscript.

## New high-impact prior-art collision
Shi, Bai and Wang (2026), Nature Communications DOI 10.1038/s41467-026-76692-0 explicitly screen frequency nadir/RoCoF, cold-load pickup and switching feasibility on a modified three-phase IEEE 123-node feeder. Generic fast transient restoration screening is therefore NOT a novel claim.
IEEE Access 2026 DOI 10.1109/ACCESS.2026.3716094 already performs current-proxy feasibility screening in GFM siting; its own limitations highlight missing controller saturation, EMT and relay dynamics.
PNNL 2019 DOI 10.1109/ISGT.2019.8791620 and PNNL IEEE TPWRD 2021 develop/validate GFM dynamic models in three-phase distribution simulators.
IEEE TPWRS 2025/2026 critical-clearing-time results with circular current limiting and virtual impedance are further collision risks.

## Novelty threshold
Only proceed if a switching-action-specific, **joint** transient-and-protection certificate is proven sound for a clearly identified physically credible hybrid inverter-and-network model, and demonstrably outperforms established dynamic-screening or reachability baselines on both coverage and computation, without unsafe approval. Even this is a hypothesis, not novelty certification.

## Execution attempt
2026-10-22 local Python import dss -> ModuleNotFoundError.
pip install dss-python -> failed with DNS name resolution; no package downloaded. Hence IEEE123 OpenDSS execution cannot be claimed.
No complete official feeder files, no executable dynamic model, no independent EMT simulation, no relay selectivity validation, no physical-grid certificate.

## Priority execution sequence
1. Obtain complete, provenance-verified IEEE123 or OEDI feeder (OEDI DOI 10.25984/2228282) with documented source files, licenses, and model revision.
2. Install and validate DSS-Extensions OpenDSS; compare baseline voltages/losses with reference.
3. Obtain independently validated open GFM model from PNNL/NREL, with current limiter and fault ride-through. Freeze controller parameters and assumptions.
4. Establish protection model with actual relay time-current curves and selectivity; test inverter-limited fault currents.
5. Implement rigorous sufficient safety certificate for specific hybrid model; derive proof and report abstentions.
6. Compare to high-fidelity dynamic simulator, conservative reachability, quasi-steady nadir/RoCoF screens, and no-certificate full simulation.
7. Report soundness counterexamples, coverage, run time, conservatism, parameter robustness and confidence intervals.
8. Re-audit literature and only then choose journal / draft.

## Decision
H2 conditional, Gate 4 blocked, paper locked. Aiming at Q1 is not evidence of publishability.
