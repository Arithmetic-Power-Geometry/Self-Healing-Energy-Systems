# Parallel evidence and literature increment — 2026-10-22

## Literature (metadata verified, full text not claimed)
1. Ding, Kar, Miao, Fan, *A Novel Design for Switchable Grid-Following and Grid-Forming Control*, IEEE TSTE 16(2), DOI 10.1109/TSTE.2024.3520989, OSTI https://www.osti.gov/pages/biblio/2562882 . Journal year 2025, DOI online 2024. Direct baseline for mode-switching claims; cannot claim switching itself is novel.
2. Muenz et al., *Protection of 100% Inverter-dominated Power Systems with Grid-Forming Inverters and Protection Relays: Gap Analysis and Expert Interviews*, SAND2024-04848, report cover https://www.osti.gov/servlets/purl/2429968 . Protection research gap map and modeling/coordination context; not a peer-reviewed journal article. No DOI invented.
Bibliography now 27 records (previous 25 plus 2). Counts include reports and repository items; journal-only count is lower.

## Evidence: actual code artifacts, NOT physical results
Created eight adversarial unittest cases for the independent IEEE123 output validator, including nonconvergence, false protection-validated claim, nonfinite voltage, duplicate scenarios, invalid SHA256, implausible node count, nonfinite power, and one synthetic valid control fixture. Synthetic numbers are test fixtures and must NEVER be described as measured feeder results. GitHub Actions updated to execute these tests and trigger when references change. Execution result of new CI revision has not been verified.

## Critical next gates
Inspect new GitHub Actions job logs and archived result, independently compare static IEEE123 feeder results, then GFM/relay/CLPU EMT testing and mathematical proof. Gate 3 open; manuscript locked.
