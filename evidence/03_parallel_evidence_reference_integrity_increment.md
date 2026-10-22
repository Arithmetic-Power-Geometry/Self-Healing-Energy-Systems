# Parallel evidence and bibliography increment — 2026-10-22

## Electrical evidence track
The OpenDSS driver now checks d.Error.Number immediately after feeder compilation and after every DSS command. It raises with d.Error.Description rather than trusting circuit existence or a later solve to reveal command failure. This is a fail-closed *software* change; no new feeder results were executed or inspected during this increment.

## Bibliography track
Added reference/audit_master.py: reports entry counts by BibTeX type, DOI field count, duplicate keys, duplicate normalized DOIs, and malformed DOI identifiers. It exits nonzero for duplicate keys/DOIs or malformed DOI fields. This is an offline metadata integrity screen, **not** publisher verification, a complete BibTeX grammar parser, or a full-text literature study. It does not generate or invent citations. Current register remains 21 records pending live audit execution.

## CI
The IEEE123 workflow now runs the bibliography audit as well as the existing API, parser, simulator and independent output checks. Both streams are saved and committed. Successful CI execution has **not** been independently verified here.

## Paper gate
Gate 3 remains OPEN, manuscript LOCKED. Next inspect live Actions run and simulation log, then verify physical benchmarks and expand verified references toward 60.
