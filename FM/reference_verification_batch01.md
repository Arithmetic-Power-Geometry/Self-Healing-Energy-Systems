# FM — Reference verification batch 01/05

**Source of truth:** uploaded `SHES_Revised_Editorial_Audit_Package(1).zip`, `SHES_Prompt_20_Final/references.bib`. Entries are in original bibliography order, with original BibTeX keys unchanged. Only the first **15 of 63** are in `FM/references.bib`. Do **not** substitute this partial file for the manuscript's complete 63-entry bibliography until the remaining batches are completed.

**Verification method:** compare original title/DOI with the publisher or official institutional source, transcribe the author list, venue, year, volume, issue and pages/article number where supported, and preserve uncertainty for unavailable fields. Article numbers are stored in `pages` for compatibility with standard BibTeX styles. No fictitious metadata added.

| # | Original key | Verification source | Result / caveat |
|---|---|---|---|
| 1 | Sun2025TopologyReconstruction | https://www.nature.com/articles/s41598-025-15440-8 | Publisher: six authors; Scientific Reports 15, 30661 (2025). |
| 2 | Wang2025IncompleteFault | https://www.mdpi.com/2227-9717/13/10/3075 | Publisher: six authors; Processes 13(10), 3075 (2025). |
| 3 | Liu2025GraphEnhanced | https://www.mdpi.com/2075-1702/13/7/543 | Publisher: three authors; Machines 13(7), 543 (2025). |
| 4 | Asadi2026IGDT | https://www.sciencedirect.com/science/article/pii/S0378779625009381 | Publisher: three authors; Electric Power Systems Research 252, 112351 (2026). |
| 5 | Shi2026Blackstart | https://www.nature.com/articles/s41467-026-76692-0 | Publisher: three authors; Nature Communications 17, 8498 (2026). |
| 6 | Eisenkraemer2026Coordinated | https://dblp.org/rec/journals/access/EisenkraemerSBAAMCB26.html and https://www.pnnl.gov/publications/systematic-review-coordinated-restoration-strategies-power-distribution-grids | DBLP + PNNL: eight authors; IEEE Access 14, 30702–30725 (2026). |
| 7 | GridAPPSDModels2024 | https://github.com/GRIDAPPSD/Powergrid-Models | Official software repository verified; original 2024 year retained but **fixed release date unverified**. No DOI established; cite a pinned commit in final manuscript if reproducibility requires one. |
| 8 | Ghoreishi2026DigitalTwin | https://www.sciencedirect.com/science/article/pii/S0142061526003133 | Publisher: seven author initials/surnames; IJEPES 177, 111871 (2026). **Full given-name expansions not verified**; initials retained. |
| 9 | Liang2025BayesianDistribution | https://www.sciencedirect.com/science/article/pii/S014206152500434X | Publisher: six authors; IJEPES 170, 110886 (2025). |
| 10 | Islam2026MeasurementRecovery | https://research-hub.nlr.gov/en/publications/risk-aware-measurement-synchronization-and-recovery-for-dsse-with/ | National laboratory: five authors; IEEE TIM 75, 9006215 (2026). |
| 11 | Baeckeland2024CurrentLimiting | https://doi.org/10.1109/TPEL.2024.3430316 and https://www.scivora.io/articles/overcurrent-limiting-in-grid-forming-inverters-a-comprehensive-review-and-discus-2024 | Five authors; IEEE TPEL 39(11), 14493–14517 (2024). |
| 12 | Mohiuddin2025TwoStage | https://doi.org/10.1109/TIA.2025.3544164 and https://www.minicod.com/papers/a-two-stage-current-limiting-control-strategy-for-direct-droop-controlled-grid-forming-inverters-f49282c8 | Scholarly indexing: five authors; IEEE TIA 61, 6472–6483 (2025). **Issue number not confirmed**; omit. |
| 13 | Pal2025FaultInduced | https://www.sciencedirect.com/science/article/pii/S0378779625000641 | Publisher: three authors; Electric Power Systems Research 242, 111471 (2025). |
| 14 | Du2019GridFormingGridLABD | https://www.pnnl.gov/publications/modeling-grid-forming-inverters-transient-stability-simulations-all-inverter-based | PNNL: five authors; IEEE ISGT 2019, pp. 1–5. |
| 15 | Kenyon2021OpenPSCAD | https://vivo.colorado.edu/display/pubid_319847 and https://research-hub.nlr.gov/en/publications/open-source-pscad-grid-following-and-grid-forming-inverters-and-a-4/ | University + laboratory: four authors; KPEC 2021; DOI 10.1109/KPEC51835.2021.9446243; original bibliography incorrectly omitted DOI. |

## Status
- Batch 01: 15/15 checked against traceable sources; 13 have complete core publication metadata, while #7 has unverified software release date and #12 has unverified optional issue number. #8 given names are retained as publisher initials.
- Remaining: 48 entries, in four batches (15, 15, 15, 3).
- Do not mark the manuscript as 100% reference-verified yet.
- After each batch, append entries to `FM/references.bib` while retaining keys and cite provenance in a new batch report.
