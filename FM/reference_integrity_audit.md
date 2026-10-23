# FM — Bibliography integrity and metadata exception audit

Date: 2026-10-23. **Staging audit only; no manuscript changes.**

## Structural inspection of committed FM/references.bib

- Exactly **63 entries and 63 distinct original keys**.
- Entry brace depth balanced across all 63 BibTeX records.
- Required bibliographic fields: **63/63 title**, **63/63 year**, **63/63 URL**, **62/63 author**.
- DOI: **60/63**. The three absent DOIs are `GridAPPSDModels2024` (software repository), `IEEE1547_2018` and `IEEE2800_2022` (IEEE standards with official links); missing DOIs do not by themselves invalidate these records.
- Field parsing correctly accounts for both line-leading and comma-separated inline BibTeX assignments.
- **No successful BibTeX-to-PDF compilation is claimed.** Syntax checks and field coverage are not equivalent to successful BibTeX compilation or LaTeX reference resolution.

## Open blocking exceptions

1. **`CSEEFRT2026`: missing author list.** IEEE publisher record https://xplorestaging.ieee.org/document/11338153/ confirms title, CSEE Journal of Power and Energy Systems, early access 7 January 2026, pages 1–12, DOI 10.17775/CSEEJPES.2024.06620. The accessible page has an empty Authors heading. Do not invent authors. **Blocking for complete author verification.**
2. **`Luo2025ParallelGFMStability`:** IEEE https://ieeexplore.ieee.org/document/10892023/ confirms journal volume 16(3), pages 2015–2028 and DOI 10.1109/TSTE.2025.3543595; indexed author list https://eurekamag.com/research/100/113/100113207.php shows Luo C., Chen Y., Liao S., Xie Z., Lian Z., Wang Z., Liu X., Gao M., Xie J. Last five given names are not verified. Preserve initials.
3. **`Le2026FaultAnalysis`:** https://eurekamag.com/research/111/550/111550455.php gives Le G.-H., Wu Y.-K., Phan Q.-D., journal and DOI 10.1109/TIA.2026.3741058. Full given names and final volume/issue/pages not established.
4. **`VoltageSustaining2026`:** Earlier Batch 04 caveat about publisher author/issue confirmation was subsequently resolved in Batch 05 using Aalborg University and IEEE; record seven authors, JESTPE 14(3), 2914–2924.
5. Other optional fields flagged in individual batch reports should be retained as qualified rather than guessed.

## Next work gate

- Resolve CSEE author metadata using an accessible full publisher PDF or verified indexing export; if unavailable, retain explicit unresolved status and do not claim 100% verified.
- Independently cross-check all remaining incomplete author expansions.
- Run BibTeX and both author/anonymous LaTeX builds against a working copy; do not overwrite original 63-reference manuscript until the reference gate passes.
- Then complete narrative flow, claim-to-evidence, and clean CI audits in the order in `FM/README.md`.
