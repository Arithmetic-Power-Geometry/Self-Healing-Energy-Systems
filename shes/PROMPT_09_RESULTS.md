# SHES Prompt 9 — independently verified feeder-derived proxy relay screens

## Reproducible execution
GitHub Actions run https://github.com/Arithmetic-Power-Geometry/Self-Healing-Energy-Systems/actions/runs/39958562769: SUCCESS.
- Five adversarial/unit tests passed.
- 1,200 seeded hypothetical relay configurations derived from six IEEE123 terminal-current fault cases (buses 60 and 83, three fault resistances, 200 draws per case).
- Independent fail-closed JSON validator passed, then JSON archived at `shes/ieee123_p9_screens.json`.
- Source and tests: `shes/feeder_certificate_p9.py`, `shes/test_feeder_certificate_p9.py`, `shes/validate_p9.py`.

## Complete confusion matrices
Order TP/FP/FN/TN; population 1200 for every row.
Against independent-corner constant-current oracle:
- Nominal: 24/189/0/987.
- Common derating: 24/7/0/1169.
- Independent box: 24/0/0/1176.
- Full-reset trace: 16/25/8/1151.
Against distinct full-reset trace oracle:
- Nominal: 41/172/0/987.
- Common derating: 16/15/25/1144.
- Independent box: 16/8/25/1151.
- Full-reset trace: 41/0/0/1159.
Zero box-vs-corner errors is a model-relative mathematical consistency property; zero self-oracle errors are tautological.

## Sensitivity
At gmin=.6: nominal/common/box/full-reset approvals 74/5/3/9.
At gmin=.7: 72/11/9/17.
At gmin=.8: 67/15/12/15.
Five counterexamples in the result JSON demonstrate box approvals that fail the separate full-reset time-domain trace, including bus 60 Rf=.1 ohm, gmin=.8, breaker delay=.08 s.

## Physical validity and scope
This experiment uses the terminal-1 conductor-1 magnitudes from Prompt 8, not measured CT currents. Topology path phase continuity, current orientation, actual switching feasibility, breaker operation, relay inventory/settings and restoration frequency certificate are unverified. Relay pickup, TDS, margins, deadlines, derating and delays are hypothetical, seeded sensitivity settings. No restoration action is certified safe. The constant-current and full-reset trace oracles do not share identical model assumptions.

## Manuscript and packaging
Committed `shes/ieee123_p9_section.tex` with full confusion tables and limits. A complete local 17-page PDF and bibliography-resolved source package was compiled with pdflatex, bibtex8, pdflatex twice; no undefined citation/reference warnings. The complete `main.tex`, figures and PDF have not been transferred to GitHub, so the GitHub shes directory is not yet a standalone manuscript build.

## Prompt 10
Develop and verify phase-aware energized connectivity and switch-state semantics, calibrate or explicitly bound relay settings from external documentation, and evaluate joint frequency and protection certificates with counterfactual backup operation; distinguish proved model-relative guarantees from physical validation.
