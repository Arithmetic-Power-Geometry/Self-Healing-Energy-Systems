# Q1 manuscript go/no-go decision matrix — 2026-10-22

## Decision
Do not start the full manuscript yet. The scientific result must be established before writing, not inferred from toy-model screening.

## Research dimensions and thresholds
| Dimension | Required independently reproducible result | Current status |
|---|---|---|
| Feeder data provenance | Complete pinned IEEE123 model, hashes, licensing, all redirects | Partial; Linux linecode filename mismatch diagnosed and workflow patched |
| AC convergence | Unbalanced 3-phase power flow with and without regulator controls; stable node voltages, control iterations, power balance | NOT VERIFIED |
| Reference consistency | Voltages/taps/losses checked against trusted feeder reference | NOT DONE |
| GFM model | Published validated current-limited GFM control equations and parameter calibration | NOT DONE |
| Transient numerical stability | Time-step convergence, stiff-solver tolerance tests, fault and cold-load scenarios | NOT DONE |
| Protection | Time-current coordination, pickup, selectivity, clearing times under inverter-limited faults | NOT DONE |
| Mathematical theorem | Precisely bounded sufficient certificate with full proof and falsification | Toy bounds only; NO H2 theorem established |
| Independent dynamic baseline | Reproducible EMT/DAE model and paired trajectories | NOT DONE |
| Baseline comparison | Same feeder/scenarios against prior screening, reachable-set or barrier baselines and brute-force simulation | NOT DONE |
| Statistical and deployment robustness | Parameter sweeps, adversarial cases, zero-unsafe-accept reporting with uncertainty, runtime | NOT DONE |
| Novelty | Closest-work claim-by-claim matrix, verified source metadata and no prior collision | CONDITIONAL |
| Evidence integrity | Scripts, raw results, hashes, failures and log URLs in evidence/; DOI records in reference/master.bib | PARTIAL; CI run not verified |

## Writing decision
Stage A: Draft only a private outline/claim table after converged feeder and validated inverter+protection model.
Stage B: Start actual manuscript when a rigorously proved nontrivial H2 certificate and independent dynamic evidence both exist, with closest prior art comparison and Gate 4 review approval.
Stage C: Freeze manuscript after supplementary robustness and reproducibility audit.

## Anti-overclaim rules
No fabricated run statuses, no unsafe approval-rate claims extrapolated beyond sampled cases, no Q1 acceptance prediction, no article writing merely to create progress.
