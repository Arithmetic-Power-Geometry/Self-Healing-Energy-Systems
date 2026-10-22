# Gate 3 multidimensional convergence review — 2026-10-22

## Verified improvements committed
- IEEE123 diagnostic driver now runs two **static** scenarios: controls off and static regulator controls on.
- Each records convergence, solver iteration count, control iteration count, bus voltage range, total circuit power, solver version and SHA256 input provenance.
- Hard fail on missing dependency, failed circuit compilation, nonconvergence, invalid voltages or absent engine.
- CI sparse checkout order corrected; workflow uploads diagnostic log on failures; pipefail prevents masked failures.

## Dimensions to converge independently before Q1 claim
1. Provenance: official feeder, file revisions, licenses, SHA256.
2. Numerical: three-phase unbalanced load flow, regulator tap/control convergence, voltage range and losses vs benchmark.
3. Dynamic: validated GFM frequency/voltage controller, current saturation and limiter transitions, solver time-step convergence.
4. Protection: actual relay pickup and time-current curves, selectivity, inverter fault current and clearing deadlines.
5. Operational: switching sequence, cold-load pickup, restoration service, uncertainty and topology/fault location variation.
6. Mathematical: hybrid-state invariant, sound proof, abstention coverage and explicit validity domain.
7. Empirical: independent EMT/DAE benchmark, matched initial conditions, negative controls and adversarial counterexamples.
8. Statistical: repetitions/uncertainty sampling, false approvals, abstention, runtime and confidence intervals.
9. Novelty: contrast with Shi et al. 2026 restoration and Baeckeland et al. 2026 current limiter and reachability literature.
10. Reproducibility: environment lock, raw logs, model hashes, scripts, figures and append-only bibliography.

## Status
Static solver workflow was updated, NOT confirmed executed successfully. Local dss package unavailable. The full physical model and independent EMT benchmark remain outstanding. No new bibliographic reference was verified in this step, so master.bib was intentionally not changed. Gate 4 blocked, paper locked.
