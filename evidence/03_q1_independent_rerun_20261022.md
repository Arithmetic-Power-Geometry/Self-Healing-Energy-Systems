# H2 Q1 verification and hard go/no-go (2026-10-22)
Independently rerun in local container:
- python /mnt/data/gate3/certificate.py -> cases=135 certified=67 rejected=68 false_safe=0 conservative_on_sample=1.
- python /mnt/data/gate3/hybrid_check.py -> total=108 certified=20 baseline_safe=22 false_accept=0 conservative=2.
- Python syntax compilation passed.
- dss import failed; pip install dss-python==0.15.7 failed DNS resolution. No feeder load flow, GFM model or EMT run.

Verified direct prior-art threat: Baeckeland, Yang and Seo (2026), IEEE TPWRS 41(1):198-213, DOI 10.1109/TPWRS.2025.3587224, unified GFM current limiter, large-signal stability, EMT and hardware validation. Earlier Gate 3 pending author metadata now resolved.

Other relevant sources: Baeckeland et al. 2024 IEEE TPEL DOI 10.1109/TPEL.2024.3430316; Mohiuddin et al. 2025 IEEE TIA DOI 10.1109/TIA.2025.3544164; Pal et al. 2025 EPSR DOI 10.1016/j.epsr.2025.111471.

Q1 requirements: (1) full provenance-verified IEEE123; (2) converged three-phase power flow; (3) calibrated GFM current limiter plus relay time-current/selectivity model; (4) independent EMT comparison and timestep convergence; (5) mathematically proven sound joint certificate; (6) strong baselines, adversarial faults and statistical performance; (7) renewed novelty/patent check.
NO GO: Gate 4 and paper locked. No claims of physical validation, novel theorem, speedup or acceptance probability.
