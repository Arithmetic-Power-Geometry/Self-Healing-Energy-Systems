# Gate 3 critical Python syntax fix — 2026-10-22

Repository inspection identified literal backslash-n tokens embedded outside Python strings in evidence/run_ieee123_baseline.py voltage validation. Those tokens would cause a SyntaxError before feeder simulation.

Corrected those tokens to real line breaks. Added an early Python py_compile step to .github/workflows/ieee123-baseline.yml, and fixed double-escaped CI metadata newlines.

This is a source-level fix, not proof of a successful OpenDSS simulation. No independent feeder, GFM, relay or EMT result was verified in this increment. reference/master.bib was not changed because no new source was verified.

Next: inspect actual GitHub Actions logs and committed evidence; require compilation, preflight, and both static feeder modes to pass. Gate 3 remains open and manuscript locked.
