# SHES Prompt 10 — joint frequency and protection model audit (2026-10-23)

## CI result
Run https://github.com/Arithmetic-Power-Geometry/Self-Healing-Energy-Systems/actions/runs/39959323013 completed SUCCESS. Six adversarial/unit tests passed, 1,440 seeded joint model configurations executed, independent validator passed, JSON was committed to `shes/ieee123_p10_joint_model.json`, and the workflow artifact was archived.

## Model and evidence scope
Six feeder-derived terminal-current proxy cases from P8 (buses 60 and 83, three fault resistances), crossed with 80 seeded hypothetical settings and three inverse-time reset semantics: full, hold, linear. Each setting uses the sign-aware scalar frequency envelope and the finite-time primary and counterfactual backup assertion model, with independent current-derating and breaker-delay corners. A sustained-fault backup counterfactual is evaluated even when primary clearing would prevent a physical backup operation. Frequency inertia, damping, power intervals and limits are hypothetical; inverter current limiting is NOT calibrated.

## Complete model-relative confusion matrices (TP/FP/FN/TN, 480 per reset)
- Full: nominal 5/65/0/410; common 5/2/0/473; independent corners 5/0/0/475.
- Hold: nominal 4/104/0/372; common 4/5/0/471; independent corners 4/0/0/476.
- Linear: nominal 9/64/0/407; common 9/3/0/468; independent corners 9/0/0/471.
- 1,097 of 1,440 pass the hypothetical frequency bound; 18 pass the joint corner model; 233 nominal and ten common-derating false approvals against the stipulated joint corner model.
- Eight nominal false-approval witness records archived.
- Zero independent-corner errors are tautological here because the box method directly uses the exact enumerated corner oracle; not an independent empirical safety verification.

## Physical verification gates
All six prerequisites remain FALSE in the source evidence: energized phase continuity, switching feasibility, CT/relay current orientation, actual installed relay settings, calibrated inverter current limits and calibrated breaker delays. Thus ZERO physical restoration certificates issued. P8 topology adjacency and current magnitudes cannot resolve CT orientation or actual protection installation.

## Deliverables
- `shes/joint_certificate_p10.py`
- `shes/test_joint_certificate_p10.py`
- `shes/validate_joint_p10.py`
- `.github/workflows/shes-p10-joint.yml`
- `shes/ieee123_p10_joint_model.json`
- `shes/ieee123_p10_joint_section.tex`
- Local 18-page manuscript assembled with full bibliography, figures, corrected outdated static-CI discussion, revised abstract and conclusion; compiled with pdflatex/bibtex8/pdflatex/pdflatex with no unresolved citations.
- IMPORTANT: full manuscript main.tex, references.bib and binary figures remain available in the downloadable local package but have not been uploaded to GitHub; GitHub shes/ is not a standalone manuscript build.

## Open science limitations
No phase-by-phase switch status and energized path audit, no CT polarity/directional measurements, no installed protective device inventory, no manufacturer relay curve calibration, no EMT/grid-forming inverter current limiter, no validated cold-load pickup, and no physical restoration authorization. The result is conditional mathematics and reproducible model comparisons only.
