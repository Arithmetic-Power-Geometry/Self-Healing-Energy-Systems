# SHES Prompt 17 — unified controlled benchmark

## Reproducibility
GitHub Actions SUCCESS: https://github.com/Arithmetic-Power-Geometry/Self-Healing-Energy-Systems/actions/runs/39967261791
Evidence artifact ID: 12506923720
10 regression/theorem tests passed; independent JSON invariants passed.
Synthetic deterministic seed 1717, 90 shared cases, 30 each full/hold/linear reset.

## Independent rectangular model reference (exact only under P13 assumptions)
method | approved | false approvals | conservative rejections | elapsed seconds
nominal | 41 | 19 | 0 | 0.000400259
common endpoints | 25 | 3 | 0 | 0.000535992
rectangle | 22 | 0 | 0 | 0.000558355
time-domain 3x3x2x2 grid | 22 | 0 | 0 | 0.004714324
The finite grid matched the theorem-backed rectangular criterion in these cases but is not itself a continuum proof.

## Correlated common-derating finite three-point diagonal reference
method | false approvals | conservative rejections
nominal | 16 | 0
common endpoints | 0 | 0
rectangle | 0 | 3
time-domain grid | 0 | 3
This is a FINITE grid, not a correlated continuum oracle. P13's analytic interior counterexample shows common endpoints can miss a violation.

## Limitations
- Synthetic piecewise-current traces, stipulated frequency envelopes, fixed relay settings; no physical relay or feeder restoration validation.
- Wall-clock times are one hosted CI-run sample, not repeat measurements.
- No separately instrumented statistical uncertainty intervals or power analysis.
- The common-endpoints screen is not a robust correlated-continuum certificate.
- No full factorial component ablation beyond the four screen methods. Dedicated ablation remains for Prompt 18.
- Full manuscript integration and clean GitHub LaTeX build remain pending.

## Novelty assessment
Most defensible contribution is a rigorously qualified exact rectangular certificate and a counterexample to correlated endpoint sufficiency, paired with an auditable comparative model benchmark. The benchmark itself does not establish a new physical restoration controller.

## Prompt 18
Execute a controlled component ablation and adversarial stress-test study. Hold scenario data fixed while omitting frequency, primary deadline, backup deadline, coordination, timer memory, independent derating and breaker delay. Compute independent confusion matrices against the theorem-backed full joint model and, separately, finite correlated reference; include minimal failing witnesses and attribution overlap. Add uncertainty sensitivity and repeated runtime measurements, independently validate, commit and run successful GitHub CI. Do not invent field or continuum results.
