# SHES Prompt 3 — compatible joint certificate audit (2026-10-23)

## Committed artifacts
- `shes/joint_certificate.tex`: complete standalone LaTeX section with a joint model-relative sufficiency theorem, proof, and full-reset pickup proposition.
- `shes/test_joint_certificate.py`: 6 adversarial tests including 10,000 deterministic randomized comparison-oracle cases.
- This report.

## Locally compiled package
`SHES_Prompt_03_Joint_Certificate.zip` contains a revised `main.tex` that includes the new section via `\\input{joint_certificate.tex}`, `references.bib`, four PDF figures, `test_theory.py`, `test_joint_certificate.py`, and a compiled `main.pdf`. pdflatex -halt-on-error completed (11 pages); full BibTeX resolution was unavailable.

## Verified tests
12 tests passed (6 previous frequency/relay theory tests plus 6 joint-certificate tests); randomized joint comparison checked 10,000 scenarios. These are deterministic model tests, not electrical validation.

## Theorem scope and new gap fixed
- Same action, fault set, uncertainty domain, relay model and horizon must be used.
- Primary breaker opening delay is included in primary clearing.
- Earliest backup *assertion* must follow primary *clearing* by margin; comparing relay assertion times alone is insufficient.
- Backup clearing deadline is separately bounded in sustained-fault counterfactual.
- Full-reset definite-time timer semantics cannot be inferred from static inverse-time trip formula.
- The theorem composes sufficient model predicates and does not establish physical field safety.

## Outstanding transfer and verification
The complete main.tex, references.bib and binary figures are NOT yet on GitHub under shes. Connector can write UTF-8 text but not binary figures, and local git remote cannot resolve github.com. Do not mistake the GitHub shes/main.tex placeholder for a compilable manuscript. Existing root evidence and references were not overwritten.
The compiled local PDF is provisional: BibTeX is missing, and no independent feeder/EMT tests have succeeded.
