# Gate 3: real CI failure and correction — 2026-10-22

## Observed execution
GitHub Actions run https://github.com/Arithmetic-Power-Geometry/Self-Healing-Energy-Systems/actions/runs/39795417527 completed with **failure**. Job 119881434951 completed setup, Python compilation, parser tests, pinned DSS-Python installation, upstream IEEE123 feeder fetch, and Linux line-code filename repair successfully. The static simulation step failed before a solve.

## Exact failure
At evidence/run_ieee123_baseline.py line 24: `d.Text.Command("clear")` raised `TypeError: 'str' object is not callable`. In the pinned DSS-Python API, `Text.Command` is a settable property, not a callable function.

## Correction
Changed all three invocation locations to property assignments: `d.Text.Command = "clear"`, `d.Text.Command = f'compile ...'`, and `d.Text.Command = cmd` for scenario commands.

## Evidence status
The run's own log was committed to evidence/ieee123_baseline_log.txt by GitHub Actions bot. The expected evidence/ieee123_baseline_result.json was absent because the solve did not occur. No power-flow convergence or protection/GFM/EMT validation established. Re-run the updated code via its push-triggered workflow and inspect actual results.

## Bibliography audit
reference/master.bib contains **16 BibTeX entries**: 13 article, 2 inproceedings, 1 misc; 14 have DOI fields and 2 do not. This counts records only; no claim that all DOI metadata or novelty coverage has been independently verified. No unverified references added.

## Manuscript gate
Gate 3 open, Gate 4 and Gate 5 outstanding. Write manuscript only after all validation passes and explicit user authorization.
