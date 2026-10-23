# SHES Prompt 6 — verified IEEE123 static feeder baseline (2026-10-23)

## Root causes, fixed
1. OpenDSS compilation changes the process working directory; `evidence/run_ieee123_baseline.py` previously wrote a relative result path into the feeder directory, so the independent validator could not find it. Fix: resolve output to an absolute path before compilation.
2. Workflow tried to push generated evidence from a stale checkout to main, causing non-fast-forward rejection. Fix: read-only workflow permissions, remove automatic repository pushes, retain diagnostics through upload-artifact.
3. Add explicit nonempty JSON existence check and regression test simulating a compile-triggered cwd change.
4. Keep original Linux filename case alias with identical electrical bytes.

## Successful GitHub Actions runs
- 39954993392: SUCCESS, all tests, DSS-Python install, feeder checkout, static solves, output JSON existence, independent validator and artifact upload passed.
- 39955020375: SUCCESS, same validated pipeline including new output-path regression test.
- 39955020375 artifact `ieee123-gate3-diagnostics`, ID 12501574009, SHA256 of ZIP `082287e42498e4ef83aa0bfb6ff780802a273070efcccb5a1b8cd1591866583a`.
- Earlier 39926762697 failed independent validation due to missing JSON and archival push conflict, not nonconvergent static load flow.

## Reproducible environment
Ubuntu 24.04; Python 3.11; dss-python==0.15.7; upstream tshort/OpenDSS pinned commit 5005c668a72d20775f4c2d060feebb2866ba1d38. DSS C-API 0.14.5 revision 87d85c2622c8281b92255335bc7c09b11191b21d (reported by successful run).
Linux alias IEEELineCodes.DSS -> IEEELinecodes.DSS was created by copying, without changing electrical data.

## Verified static observations
- controls off: converged, 278 voltage nodes, 3 iterations, 1 control iteration, min 0.9265380197575005 p.u., max 0.9999938776441388 p.u., power [-3482.6846852337558,-1358.0693921089373].
- static controls: converged, 278 voltage nodes, 19 iterations, 6 control iterations, min 0.9792109289804353 p.u., max 1.0499610277736173 p.u., power [-3615.2419223985175,-1311.5149870128353].
- JSON validator passed. `278` is a voltage-node count, not the number of physical buses.

## Source and manuscript
- Committed: corrected driver, workflow, regression test and `shes/ieee123_static_verified_section.tex`.
- Local Prompt 6 package includes revised main.tex, bibliography, figures and the verified static section. pdflatex + bibtex8 + pdflatex (three passes) compiled a 16-page PDF with no unresolved citation/reference warnings in final log.
- Full main.tex and binary figures are still not uploaded under GitHub shes/; the local downloadable package is the authoritative revised assembly for now.

## Remaining limitations
Static load flow only. No feeder-derived fault currents, protection relay settings, short-circuit studies, switching transients, GFM frequency dynamics or EMT validation. Pinned upstream commit exists and was checked out successfully, but upstream authenticity beyond Git provenance was not independently audited. Artifact retention is limited by GitHub Actions policy; it is not an indefinite archival repository.
