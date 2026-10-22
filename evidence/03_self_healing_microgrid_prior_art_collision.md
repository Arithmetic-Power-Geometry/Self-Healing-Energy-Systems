# Gate 3 novelty collision: protection approaches for self-healing microgrids

Source: Sandia National Laboratories conference manuscript SAND2024-02641C, Protection Approaches for Self-Healing Microgrids, https://www.osti.gov/servlets/purl/2540522 (public OSTI-hosted PDF). Screening date: 2026-10-22. Source inspected through indexed text; this is not a complete page-by-page full-text audit.

## Concrete collision
The source describes a self-healing microgrid with grid-forming inverters, protection relays, fault isolation, synchronization-check reclosing, and staged load restoration. The indexed PDF explicitly reports restoration of loads at 4.0 and 4.5 seconds, and reclosing at 4.83 and 4.87 seconds; it also reports inverters reaching current limits during faults, losing voltage regulation, then returning to regulation after fault isolation.

This is a **high-severity novelty collision** for any broad H2 framing that merely combines GFM current limits, relay coordination and self-healing restoration. It is NOT proof that a formally sound, switching-action-specific certificate already exists. To distinguish the proposed contribution, require a precise theorem/certificate with assumptions, formal soundness or independently falsifiable bounds, and numerical comparison against a published relay/GFM restoration implementation.

## Reproducibility and next actions
1. Retrieve author names and final publication venue/DOI for SAND2024-02641C before adding it to master.bib. Pending metadata must not be fabricated.
2. Build a scenario-matching benchmark for the published self-healing sequence: fault at 1 s, staged load restoration, sync-check reclosing, limiter engagement and release. Do not equate the paper's event times with universal feeder requirements.
3. Log relay trip/reclose event times, inverter current limit state, voltage/frequency trajectories, and certificate approvals and false-safe events.
4. Cross-check whether the original paper's exact topology, settings and source code are accessible; mark non-reproducible components rather than filling with assumptions.

## Evidence status
This increment adds source-grounded adversarial prior-art screening only, not executed electrical validation. Gate 3 remains OPEN and manuscript writing remains LOCKED.
