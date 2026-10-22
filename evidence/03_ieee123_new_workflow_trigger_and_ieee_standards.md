# Parallel increment: workflow trigger and IEEE standards — 2026-10-22

## Evidence track
Changed .github/workflows/ieee123-baseline.yml to print GITHUB_SHA and GITHUB_REF_NAME at the start of the job. Because the workflow listens to pushes touching its own path, this commit should request a fresh CI run; **workflow success is NOT inferred from the commit**. Last directly inspected archived run remains 39795417527, failed. Inspect actual newly generated run ID, steps, logs, output JSON and hashes before claiming any electrical evidence.

## Reference track
Two authoritative standards added to master.bib:
- IEEE Std 1547-2018, *IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces*, DOI 10.1109/IEEESTD.2018.8332112.
- IEEE Std 2800-2022, *IEEE Standard for Interconnection and Interoperability of Inverter-Based Resources (IBRs) Interconnecting with Associated Transmission Electric Power Systems*, DOI 10.1109/IEEESTD.2022.9762253.
These are standards, not journal articles. IEEE 2800 concerns transmission-level IBR interconnection; its requirements must not be falsely presented as distribution-relay rules.

## Counts and gate
Master bibliography 30 records total (including standards, reports and repository records). 60 remains a coverage target, not a count of reviewed full-text journal articles. Gate 3 open; manuscript locked.
