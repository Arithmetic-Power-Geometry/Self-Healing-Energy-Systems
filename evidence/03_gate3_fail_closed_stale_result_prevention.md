# Gate 3 fail-closed result integrity — 2026-10-22

## Risk
An earlier evidence/ieee123_baseline_result.json indicating PASS could survive a later failed run if the program only wrote JSON after success. A researcher could then mistake a stale result for current validation. The program also examined voltage arrays before explicitly rejecting nonconvergence.

## Changes
- At start of run(), create the output directory and delete the requested output JSON if present, before importing or invoking DSS-Python. On any later failure, no stale PASS result remains.
- Immediately reject Solution.Converged=False before assessing per-unit voltage values.
- Added AST/source regression tests for stale-output deletion order and convergence-check order to evidence/test_ieee123_api_contract.py.

## Scope and caveats
These are software integrity checks, not a successful electrical simulation. Existing archived CI failure is still the last inspected run. A new workflow run and independent reference comparison remain necessary. Gate 3 open, manuscript locked; no new references in this increment.
