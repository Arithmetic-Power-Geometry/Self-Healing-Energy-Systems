# Literature evidence register — 2026-10-22

## Scope and count
Before this increment master.bib contained 16 records (13 articles, 2 proceedings, 1 repository). Three additional source-verified articles were appended, yielding **19** records (16 articles, 2 proceedings, 1 repository), **17 with DOI**. This is not a claim of having read 19 full texts: bibliographic records and abstract-level screening are distinct from full-text study.

## Newly verified records and relevance
1. **Lyu et al. (2024)**, IEEE Transactions on Power Systems 39(4):6107–6110, DOI 10.1109/TPWRS.2024.3402012. Metadata verified against PNNL publication record https://www.pnnl.gov/publications/criteria-grid-forming-inverters-transitioning-between-current-limiting-mode-and-normal . Abstract-level finding: provides criterion for switching out of inverter current-limiting mode after fault clearance; EMT validation with multiple limiter types. **Collision risk** for any H2 claim that switching-mode recovery criteria are wholly new.
2. **Ordono et al. (2024)**, Renewable and Sustainable Energy Reviews 202:114657, DOI 10.1016/j.rser.2024.114657. Metadata verified against publisher https://doi.org/10.1016/j.rser.2024.114657 . Abstract/highlight-level finding: review of current limiting strategies under low-voltage ride-through. **Use** taxonomy of GFM limiter assumptions and baselines; do not claim systematic full-text review yet.
3. **Li et al. (2022)**, IEEE Transactions on Smart Grid 13(4):2690–2702, DOI 10.1109/TSG.2021.3120555. Metadata verified against University of Hong Kong record https://hub.hku.hk/handle/10722/338418 . Abstract-level finding: restoration under decision-dependent cold-load pickup uncertainty. **Collision risk** for H2 cold-load-pickup novelty.

## Research study policy (from now on)
Maintain for each encountered work: citation key, verified DOI/stable identifier, title, complete authors, venue/year/volume/issue/pages, verification URL, retrieval date, access type (metadata / abstract / full text), specific method and assumptions, system benchmark, validation evidence, comparison to H2, novelty collision severity, and manuscript role. **Do not label abstract screening as full-text study.** Papers with missing/uncertain metadata go to reference/gate3_pending.md, never master.bib. Deduplicate by normalized DOI, then title.

## Coverage plan to at least 60 *verified and relevant* works
Target 10–12 studies per cluster: (A) restoration/reconfiguration, (B) GFM transient and current limiting, (C) relay selectivity and inverter fault response, (D) cold-load pickup and load dynamics, (E) verified safety certificates/robust control, (F) independent feeder/EMT validation. These are coverage targets, not invented citations. Review established work and recent results; seek contradictory evidence, not just supporting papers. A reference count alone does not establish Q1 novelty.

## Experiment and manuscript status
Real CI run 39795417527 failed due to DSS-Python Text.Command being a property; correction committed separately. No new successful feeder result verified in this increment. Gate 3 open, manuscript locked.
