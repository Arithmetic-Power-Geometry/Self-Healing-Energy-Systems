# Prompt 1 — repository baseline audit (2026-10-23)

## Verified repository structure
- `.github/workflows/ieee123-baseline.yml`
- `evidence/`: research protocols, synthetic Python experiments, OpenDSS driver, validators and regression tests
- `reference/`: master bibliography and audit code
- `paper/`: README only at inspection
- `shes/`: working revision plan and source placeholder

## Source archive
The conversation attachment `shes_revision_stage1.zip` contains `main.tex`, `references.bib`, four PDF figures, `citation_registry.tsv`, `audit.json`, `README.md`, and `REVISION_PLAN.md`. Full source transfer into GitHub is **not yet complete**. Do not use `shes/main.tex` as a finished manuscript until replaced.

## Verified script design
- `gate3_independent_relay_uncertainty_20000.py`: deterministic RNG seed 20261022, 20,000 cases, 3 locations each, 3x3 current multipliers and 2x2 delay corners, compares nominal/common/independent-box.
- `gate3_interrupted_pickup_20000.py`: deterministic seed 20261023, 20,000 two-pulse synthetic full-reset definite-time traces. Not EMT or manufacturer relay model.
- `gate3_finite_backup_trip_20000.py`: deterministic seed 20261022, 20,000 synthetic current/settings cases, 30% common derating plus 40 ms delay.
- An independent local reproduction of the three named scripts' computational logic (Python 3, same seeds and parameter draws) matched the reported counts exactly. This is not an end-to-end execution of the GitHub workflow or proof of physical validity.

## CI status
Latest inspected run 39926762697 (2026-10-23): FAILURE.
Earlier inspected runs 39816117460, 39815140607, 39814693255 and 39813703558: FAILURE.
Workflow has a pinned dss-python 0.15.7 dependency, pinned upstream OpenDSS revision 5005c668a72d20775f4c2d060feebb2866ba1d38, and static JSON validation.
Workflow's `if: always()` archival push can fail when the repository branch advances concurrently; artifacts are uploaded even on failure. No clean successful end-to-end run is established.

## Open issues / blockers
1. Full `shes/` LaTeX and figure transfer not complete.
2. Binary figures cannot be uploaded by the current GitHub text-file connector.
3. Three core synthetic experiments reproduced locally; remaining scripts and full clean-environment reproducibility remain unverified.
4. No successful independently validated feeder workflow in inspected runs.
5. No feeder-derived fault-current/relay certificate or dynamic EMT validation.
6. Table 4 set accounting independently reproduced: 3,104 nominal-and-robust approvals, 129 robust-only approvals, 3,530 nominal-only approvals. Thus 3,104 + 129 = 3,233 robust approvals; 3,104 + 3,530 = 6,634 nominal approvals. Explain this explicitly in the manuscript.
7. Verify incomplete bibliography author fields and possible duplicate Muenz entries.
8. Preserve the distinction between model-relative mathematical soundness and physically demonstrated safety.

## Preservation policy
Existing evidence, workflows and reference files were not overwritten. No fabricated data, simulation result, or successful validation status was added.

## Local reproduction results (2026-10-23)
- Independent-current study: nominal 5796, nominal false 4739, common 1533, common false 476, box 1057, box false 0.
- Interrupted-pickup study: static 19135, static false 6457, persistence 12678, persistence false 0.
- Finite-backup study: nominal 6634, false 3530, robust 3233, robust false 0, infinite-backup loophole 32; overlap 3104, robust-only 129.
- Reproduction independently reimplemented the same deterministic loops from inspected repository scripts; it does not independently validate the assumed electrical model.
