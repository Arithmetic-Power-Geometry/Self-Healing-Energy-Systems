# SHES Prompt 5 — synthetic reproducibility audit (2026-10-23)

## CI execution
Latest clean successful run: https://github.com/Arithmetic-Power-Geometry/Self-Healing-Energy-Systems/actions/runs/39954105766
Five Python unittest methods passed; source experiments, refined scalar RK4 check, shared-population sensitivity and time-domain comparison executed. JSON archived in this repository at `shes/results/synthetic_audit.json` and `shes/results/time_domain_comparison.json`. Earlier interim failed CI runs occurred while updating tests for the added RK4 dependency; the final run succeeded.

## Source count reproduction
- Three-location independent-current, 20,000: nominal 5796 approvals / 4739 false; common 1533 / 476 false; box 1057 / 0 false.
- Interrupted definite-time, 20,000: static 19135 approvals / 6457 false; persistence 12678 / 0 false.
- Finite backup, 20,000: nominal 6634 / 3530 false; common derating 3233 / 0 false against exact stipulated scenario.
- Finite backup contingency: both 3104; nominal-only 3530; derating-only 129; neither 13237.
- Scalar analytic refined certificate: 402/2592, NOT 396. Independent finite-step RK4 check: 486 model-safe; 84 conservatively rejected; 0 refined approvals sampled unsafe. Old looser certificate had 396 approvals / 90 conservative rejections and should not be conflated with refined values.
- Other source runs: inverse-time script nominal 10695, nominal unsafe 3208, robust 7656; relay pickup uncertainty 10000 nominal 5202 / 3047 missed, robust 2155 / 0 missed.
- CRITICAL: original `evidence/gate3_inverse_time_relay_20000.py` sets `robust_unsafe += 0` unconditionally, so that zero is NOT an independent validation.

## Shared-population independent-corner sensitivity (5,000 each)
- gamma_min .60: oracle-safe 98, nominal false 1322, common false 76, box false 0.
- gamma_min .70: oracle-safe 271, nominal false 1149, common false 103, box false 0.
- gamma_min .80: oracle-safe 540, nominal false 880, common false 109, box false 0.
- Box approvals equal oracle-safe counts by mathematical monotonicity and the common uncertainty domain; zero is expected and NOT empirical device reliability.

## Time-varying full-reset relay experiment (4,000 synthetic two-pulse traces)
- Nominal constant-current: approved 2222, false approvals 1035, safe rejected 15.
- Common derating: approved 1110, false approvals 189, safe rejected 281.
- Independent constant-current box: approved 940, false approvals 118, safe rejected 380.
- Time-domain full-reset oracle: approved 1202, self-comparison false approvals 0, safe rejected 0.
- The 118 box-screen false approvals are outside the *constant-current* box theorem's assumptions, not a mathematical contradiction. No field or manufacturer relay data used.

## Manuscript integration
- Committed `shes/synthetic_audit_section.tex` with full results tables and caveats.
- Local Prompt 5 LaTeX package includes this section and changes the refined scalar table to 402/84. pdflatex compiled 12 pages twice; bibliography remains unresolved (no BibTeX installed).
- GitHub `shes/main.tex` remains a placeholder; complete LaTeX/figure transfer remains open. Do not treat this GitHub folder as a compilable manuscript archive yet.

## Remaining limitations
Synthetic self-oracles do not measure field failure probabilities. No feeder-derived fault currents, manufacturer relay calibration, time-domain EMT inverter model, or independently successful IEEE123 workflow. The test sample distributions are not calibrated to an actual feeder. Compare each screen only within the clearly specified shared population and oracle.
