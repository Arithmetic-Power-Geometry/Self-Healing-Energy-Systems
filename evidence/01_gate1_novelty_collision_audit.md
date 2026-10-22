# Gate 1 — Adversarial novelty and research collision audit
Date: 2026-10-22. Status: PROVISIONAL / conditional pass for mathematical scoping only. No theorem proved, experiment run, patent clearance established, or manuscript authorized.

## Scope and method
Targeted 2025–2026 publisher/IEEE/PNNL search and official benchmark repository inspection. Cross-disciplinary lenses: grid restoration, incomplete observability, active information acquisition, robust decision theory, formal verification, protection, renewable black-start, decentralized control, learning, and data realism. This is a targeted first-pass audit, NOT a PRISMA systematic review, exhaustive patent search, or verified worldwide novelty clearance.

## Direct competitors and collision matrix
|Source|Verified pointer|Already covers|Novelty implication|
|---|---|---|---|
|Shi, Bai & Wang (2026), Nature Communications 17:8498|10.1038/s41467-026-76692-0|bottom-up black-start; uncertainty-aware information-adaptive rolling horizon; dynamic/protection constraints; decision-relevant observability|Broad decision-aware restoration, sensing and protection claims collide|
|State-Awareness-Based Adaptive Restoration (2026), IEEE TSG|10.1109/TSG.2026.3710343|observable/controllable and unobservable states; adaptive centralized/decentralized restoration; 53/139 nodes|No blanket claim of first unobservable or communication-loss restoration|
|Sun et al. (2025), Scientific Reports 15:30661|10.1038/s41598-025-15440-8|topology reconstruction + risk-aware reconfiguration with fragmented data; 58-node simulation|Topology inference + restoration integration is existing|
|Eisenkraemer et al. (2026), IEEE Access 14:30702–30725|10.1109/ACCESS.2026.3667471|systematic review of coordinated restoration strategies|Coordinated strategies already surveyed|
|Nawaz et al. (2026), Journal of Electrical and Computer Engineering|10.1155/jece/1017506|multi-agent protection and restoration; OpenDSS/LinDistFlow; forgetting at 33-bus stage and incomplete mastery of 119-bus|MARL or joint protection-restoration is not new; cross-topology robustness is measurable|
|Li et al. (2026), Electric Power Systems Research|https://www.sciencedirect.com/science/article/pii/S0378779626010126|knowledge-graph DRL with uncertainty-aware safety-switching|Safety-aware learned switching already exists|
|Graph-Based Heterogeneous MARL (2026), IEEE TSMC|10.1109/TSMC.2025.3649418|graph attention and 123-bus OpenDSS restoration|Graph neural/heterogeneous multi-agent claims collide|
|Distribution Network Modeling, Parameters, and Metering Data (2026), IEEE Canadian J ECE|10.1109/ICJECE.2026.3693137|8 reconfigurable test networks, 9 smart-meter datasets, missing data critique|Must avoid ungrounded dataset realism claims|

## Ranked surviving hypotheses (all unproved)
### H1. Minimum decision-sufficient measurement certificates
Define belief set B of physically admissible post-fault states; action safe if safe for ALL x in B. Seek minimum adaptive measurements to certify at least one action delivering >= target service. Show restricted classes with exact polynomial algorithms or complexity/information lower bounds, and strict separation from full-state identification. Collision risks: robust POMDP, active diagnosis, decision-focused sensing, sensor placement, epistemic planning, certificate complexity. High conceptual promise; HIGH prior-art risk.
Falsifier: a known reduction completely subsumes the proposed theorem or minimum measurement calculation is a trivial hitting set formulation without novel structure.
### H2. Fast sound protection-and-transient screening for inverter-led restoration
Construct a computationally cheap sufficient (never unsafe-positive under specified bounded model uncertainty) action admissibility test combining inverter current limits, cold-load pickup, transient margins and protection selectivity. Need prove soundness for stated model and benchmark versus detailed electromagnetic transient simulations. Collision risks: reachability analysis, barrier certificates, transient stability screening, robust protection constraints. HIGH physical modeling burden.
Falsifier: existing screening gives equivalent guarantees and cost or model simplifications invalidate physical applicability.
### H3. Local restoration with communication loss and explicit safe-abstention guarantees
Controllers decide from local state under bounded message delay/dropout; show safety invariant and service guarantees or impossibility boundary. Collision risks: distributed model predictive control, islanding, fault-tolerant distributed algorithms and 2026 state-awareness paper.
Falsifier: guarantees already covered by known decentralized restoration or assumptions unrealistic.

## Zig-zag adversarial checks
1 Grid ↔ information theory: distinguish reconstructing all switch states from certifying one safe action; formalize observation cost, state partitions, and impossibility instances.
2 Grid ↔ formal verification: every switching sequence has intermediate-state constraints, not only final power flow; establish a sound independent checker.
3 Grid ↔ active learning: ask whether a measurement has decision value even if it yields little total entropy reduction; compare expected versus worst-case information policies.
4 Grid ↔ protection physics: test whether steady-state feasible actions fail relay coordination or inverter current limits.
5 Grid ↔ distributed systems: bounded delay/dropout and Byzantine measurements may force abstention; specify threat and timing models.
6 Grid ↔ ML: test topology transfer without retraining, forgetting, and OOD uncertainty; compare to exact optimization and robust heuristics.
7 Grid ↔ benchmark realism: switching controllability, normally-open ties, protection settings, phases, DER and fault telemetry often missing from feeder datasets; declare assumptions.
8 Grid ↔ intellectual property: search patents for FLISR, adaptive restoration, switching authorization and sensor placement; no patent claims or freedom-to-operate opinion without independent patent-family/claims search.

## Public benchmark audit
GRIDAPPSD/Powergrid-Models https://github.com/GRIDAPPSD/Powergrid-Models contains IEEE123, IEEE8500, PNNL and EPRI models; IEEE123 includes reconfiguration switches; model repository is not an actual outage event dataset. The 2026 IEEE Canadian J ECE resource documents omissions and assumptions. Need record model revisions/licenses and raw input checksums before experiments.

## Mandatory Gate 2 questions
Q1: Define finite state/observation/action/cost and electrical feasibility; is strict separation from full topology ID provable beyond toy examples?
Q2: Which formal safety properties can be guaranteed under steady-state AC/linearized models and which require dynamic EMT?
Q3: Does decision-sufficient observation reduce to known set cover, diagnosis or robust optimization; identify exact reduction and nontrivial restricted classes.
Q4: What is the strongest counterexample under unknown source energization, stuck switches, relay nonselectivity and bad telemetry?
Q5: What realistic sensor data and switch-status labels are available versus synthesized?

## Gate verdict
CONDITIONAL PASS to Gate 2 formal falsification, NOT approval to write manuscript. None of the three candidate novelty claims is established. No experimental improvement percentages are asserted.
