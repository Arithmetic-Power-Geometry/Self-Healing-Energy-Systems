# Gate 3 automatic CI evidence archival — 2026-10-22

## Change committed
IEEE123 GitHub Actions workflow now has contents:write and an always-run archival step that:
1. writes evidence/ieee123_ci_run_metadata.txt with run URL, triggering commit and workflow name;
2. stages only evidence/ieee123_* files that actually exist;
3. commits and pushes evidence to the same branch as the run when changes exist;
4. retains upload-artifact diagnostics as a separate fallback.

This makes the research requirement to **save and commit actual run outputs** executable rather than dependent on manually downloading an artifact. The workflow only triggers on code/test/workflow paths, so its evidence-only commit should not cause a run loop.

## Caveats
A workflow commit is NOT proof that GitHub Actions executed or that the feeder converged. Branch protections, disabled Actions, restricted GITHUB_TOKEN permissions, upstream network errors, or an invalid pinned feeder revision may prevent the archival step. If the run fails before simulation, metadata may be committed without a solver result; interpret it as an attempted run, not PASS.

## Required inspection
Check GitHub Actions latest run, its job logs and evidence/ieee123_baseline_result.json. Only mark static convergence validated if the solver reports converged=true in both control modes and benchmark comparison is independently performed. Do not start manuscript. No new literature source validated in this increment; reference/master.bib intentionally unchanged.
