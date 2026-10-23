# FM — Final Manuscript research and submission work plan

Project: **Conditional Frequency and Protection Screens for Microgrid Restoration: Robust Bounds, Relay-Timer Counterexamples, and IEEE 123-Bus Model Evidence**

This folder is the staging area. **Do not modify the submitted/revised manuscript source or overwrite its 63-reference bibliography until all reference batches and subsequent editorial audits pass.** Preserve the citation keys used in the paper. Original authoritative source for this stage: uploaded `SHES_Revised_Editorial_Audit_Package(1).zip`.

## Ordered work plan (approved)
1. Independently verify and repair all **63** references (author list, exact title, venue, year, volume, issue, pages/article ID, DOI or official URL); process **15 per batch** and commit after each batch. Save all verified entries in `FM/references.bib` and verification provenance in `FM/reference_verification_batchNN.md`. Never invent metadata. Any missing DOI or non-journal software record must be explained, not manufactured.
2. Revise narrative flow: eliminate duplicated IEEE 123-bus static baseline across Sections 8.4 and 8.9; replace formulaic table introductions; retain all distinct results, caveats, labels and counts.
3. Independently audit every theorem and proof assumption, numerical count, source hash, unit, physical safety boundary, novelty claim, figure/table/algorithm citation and reproducibility statement. Treat correlated finite-grid evidence separately from Cartesian-continuum theorem.
4. Compile and inspect **author and anonymous** manuscripts from the exact committed sources, bibliography and figures. Check metadata, self-identification, missing/duplicate citation keys, unresolved references, and GitHub Actions CI. A passing source audit is not a passing PDF build.
5. Perform general journal-neutral final editorial review: abstract/conclusion alignment, academic flow, no author instructions or AI workflow phrases, bibliography metadata, ethics/declarations and anonymity. **No target journal selected; do not impose journal-specific formatting.**

## Batches
- Batch 01, references **1–15**: COMPLETE in `FM/references.bib`, documented in `FM/reference_verification_batch01.md`.
- Batch 02, references **16–30**: `Baeckeland2026UnifiedLimiter`, `Lyu2024LimiterRecoveryCriterion`, `Ordono2024CurrentLimitingLVRT`, `Li2022ColdLoadPickupEndogenous`, `Mannan2024FIDVRRestoration`, `Lyu2024NegativeSequenceProtectionReview`, `Lyu2025CriticalClearing`, `Yang2024SmallSignalGFM`, `Chatterjee2025UNIFIReference`, `Kroposki2024UNIFISpecifications`, `Ding2025SwitchableGFM`, `Muenz2024ProtectionGap`, `Yusuf2024SelfHealingProtection`, `IEEE1547_2018`, `IEEE2800_2022`.
- Batch 03, references **31–45**: `Ferrari2024FaultCurrentProtection`, `Bassey2020DynamicRestoration`, `Du2021DynamicGFMDistribution`, `Kudo2024VirtualImpedanceLVRT`, `Li2025LongLineGFMProtection`, `Zhao2024GFMFRT`, `Kim2024InverterFaultContribution`, `Hasan2025GFMProtectionReview`, `Nurunnabi2026InverterProtectionReview`, `Westman2025GFMOverloadMitigation`, `Seo2025MicrogridBlackStart`, `Li2026ProtectionInteroperableFRT`, `Davi2025InterconnectionProtection`, `ArjomandiNezhad2025FaultRecovery`, `Yang2025ConverterCLPURestoration`.
- Batch 04, references **46–60**: `Eladl2025StableRelayCoordination`, `Khan2025ImprovedGFMFRT`, `Luo2025ParallelGFMStability`, `Johansson2025DistanceGFM`, `Li2026RelayCurrentLimiter`, `Maharjan2025DynamicMicrogridRestoration`, `ChhetijaFerrari2025SequenceRelayCoordination`, `ChhetijaFerrari2025UnbalancedFaultProtection`, `BaeckelandYangSeo2025TransientStability`, `GeneralFramework2026AsymmetricGFM`, `Gross2024UniversalGFMVerification`, `Rauf2026MVProtectionReview`, `Crossforming2025`, `VoltageSustaining2026`, `CSEEFRT2026`.
- Batch 05, references **61–63**: `NegativeSequence2025`, `Liu2026MultiLoop`, `Le2026FaultAnalysis`.

## Acceptance gate
No claim of 100/100 or submission-ready until all 63 citations have individually traceable provenance, all numerical claims independently checked, and final author/anonymous PDFs built and inspected from a clean GitHub checkout. Engineering claims must remain limited to verified model evidence; no field/EMT or physical switching authorization.
