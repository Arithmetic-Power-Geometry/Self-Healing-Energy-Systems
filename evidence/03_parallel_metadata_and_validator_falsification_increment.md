# Parallel increment — 2026-10-22

## Bibliography
OSTI record 2572778 independently confirms that Lyu et al. critical clearing time paper appeared in IEEE Transactions on Power Systems, volume 40, issue 2 (2025), DOI 10.1109/TPWRS.2025.3527816. Master BibTeX corrected accordingly. No new entry; count remains 27.

## Electrical evidence
Added two additional negative fixtures to independent IEEE123 output validator tests:
- Missing explicit EMT-validation status must be rejected.
- Inverted voltage extrema (minimum greater than maximum) must be rejected.
These bring adversarial fixture methods to ten including one synthetic valid case. They test validator logic, not real feeder physics. No fresh IEEE123 execution output verified.

## Stronger literature collision
Yusuf, Ropp and Reno, *Protection Approaches for Self-Healing Microgrids Using Only Local Measurements*, Sandia manuscript SAND2024-02641C, OSTI 2540522, explicitly uses a Simulink IEEE123 case study with local-measurement-only relay partitioning. Authors verified from report cover; final publication metadata remains pending. See evidence/03_self_healing_microgrid_prior_art_collision.md.

## Status
Gate 3 OPEN; paper locked. Real static simulation and independent electrical validation remain decisive next steps.
