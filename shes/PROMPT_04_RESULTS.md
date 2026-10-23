# SHES Prompt 4 — advanced time-domain relay integration

## New model
- Strict pickup `I > I_pk`, inverse-time integrator progress `dx/dt = 1/T(I)` with T(I)=0.14 s*TDS/((I/I_pk)^0.02-1).
- Three declared dropout rules: full reset, hold, linear partial reset with rate rho [s^-1].
- Definite-time progress `dx/dt=1/dwell` above pickup.
- Exact piecewise-constant segment updates, first threshold-crossing time, and nonzero initial progress.
- Primary/backup coordination uses backup assertion minus primary assertion-plus-breaker-opening, plus independent clearing deadlines.
- Not a vendor-specific relay, EMT model, or field validation.

## Formal result
Constant-current consistency and piecewise-constant exactness proved for the stated integrator. Time-domain relay behavior cannot generally be replaced with one static current multiplier.

## Verified GitHub CI
SHES relay time-domain tests workflow run 39952987778: SUCCESS.
Workflow executes Python compilation and 10 unittest methods, including 10,000 randomized piecewise constant-current oracle checks and 1,000 reset-order checks. No physical validation is inferred.

## Artifacts
- `shes/relay_time_domain.py`
- `shes/test_relay_time_domain.py`
- `shes/relay_time_domain_section.tex`
- `.github/workflows/shes-relay-tests.yml`
- This results report.
The complete revised LaTeX main.tex, bibliography and figures remain in the local downloadable archive, not in GitHub; the existing GitHub shes/main.tex remains a placeholder. The revised local PDF compiled with pdflatex (11 pages); bibliography unresolved because BibTeX unavailable.

## Remaining limitations
- Integration and reset laws are stipulated idealizations, not manufacturer relay characteristics.
- Current trace must be contiguous, piecewise constant, nonnegative and cover the requested horizon.
- No measurement-derived current trace, breaker failure, CT saturation, directionality, filtering or communication delay.
- Static IEEE123 workflow remains failing; no feeder-derived fault-current validation.
- Full source and binary figure GitHub transfer unresolved.
