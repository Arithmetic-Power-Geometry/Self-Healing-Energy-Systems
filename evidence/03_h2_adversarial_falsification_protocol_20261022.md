# Parallel increment: H2 falsification targets and OSTI literature — 2026-10-22

## Reference track
Four DOI-grounded records added to master.bib, bringing it from 21 to **25** entries. OSTI source identifiers:
- 2572778, Lyu et al., critical clearing time with circular and virtual impedance limiters, DOI 10.1109/TPWRS.2025.3527816.
- 2544234, Yang/Baeckeland/Seo, small-signal GFM stability with current limiting, DOI 10.1109/ECCE55643.2024.10861654.
- 2583465, Chatterjee et al., UNIFI reference inverter design and experimental implementation, DOI 10.2172/2583465.
- 2329414, Kroposki, UNIFI GFM specifications v2, DOI 10.2172/2329414.
Verification is bibliographic metadata and abstracts; not all full texts have been analyzed.

## Evidence track: falsifiable H2 experimental design
H2 cannot claim novelty from current limiting, critical clearing, feeder restoration or protection coordination in isolation. A switching-action-specific certificate must demonstrate:
1. **Soundness**: for each certified switching action and declared uncertainty set, prove no violation of voltage/frequency/current and protection constraints across the claimed horizon, with clearly stated model assumptions.
2. **Counterexample search**: adversarial sweep of fault type/location, GFM limiter mode and transition timing, motor pickup fraction/stall time, feeder switching order, protection pickup/time curves, measurement error and controller latency.
3. **Baseline comparison**: independent EMT/DAE model vs reduced-order certificate, with false-safe approvals explicitly counted. Compare at least against a no-certificate policy and a published GFM limiter/relay-compatible strategy where implementation is reproducible.
4. **Sensitivity and ablations**: remove relay selectivity, current-limiting, cold-load pickup and uncertainty margins individually; report changes in safety, conservatism and restoration feasibility.
5. **Replication**: fixed feeder model hashes, parameter files, solver versions, random seeds, complete trajectories, relay events and numerical tolerance checks.

## Observed vs planned
This is an experimental specification and novelty-screening update, NOT an executed electrical experiment. Latest inspected IEEE123 CI artifact still refers to prior failed run 39795417527. No successful current CI output was verified. Gate 3 remains open; manuscript locked.
