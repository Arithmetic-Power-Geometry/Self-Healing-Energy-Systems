# Gate 2 — Mathematical falsification report
Date: 2026-10-22. Verdict: FAIL original H1 novelty; conditional continuation only with genuinely power-specific constraints. No manuscript.

## Most consequential collision
Existing Decision Region Determination (DRD) permits overlapping decision regions; hypotheses=grid states, tests=measurements, regions=states where a given switching action is safe. Finite fixed-library minimax decision-sufficient sensing is therefore an established active-testing formulation, not a new primitive. Strong additional collision: https://github.com/Arithmetic-Power-Geometry/Decision-Resolution-Optimization explicitly documents finite ECD reductions. This user's pre-existing research must be cited/compared, not rebranded.

## Formal core
Finite W; nonempty safe-action regions R_a subset W; observation tests e:W->O_e; belief B subset W. Stop when exists a such that B subset R_a. Exact worst-case unit-cost recurrence:
V(B)=0 if some a has B subset R_a;
otherwise V(B)=min_{e with >1 distinct nonempty outcome classes} [1+max_o V(B intersect e^{-1}(o))], with min empty = infinity.
Full identification value U(B) has base |B|=1, same recurrence.
If every state admits at least one safe action, V(B)<=U(B) by decision tree simulation. If not, this inequality FAILS (counterexample: W={0,1}, fully discriminating test, only action safe in {0}; U=1, V=infinity). This caveat was found by an actual failed assertion and repaired, not hidden.

## Explicit strict-separation witness
W={0,1,2,3}, safe actions R_A={0,1}, R_B={2,3}. Binary tests e1=(0,0,1,1), e2=(0,1,0,1). One e1 identifies a safe action in all outcomes, V(W)=1; complete identification requires both e1 and e2, U(W)=2. This witness is NOT novel; DRD explains it.

## Executed exhaustive small-instance test
Script: evidence/gate2_finite_falsification.py. Independent local execution of same algorithm after correction: PASS cases=2754 strict=1596 decision_impossible=1035. Enumerated n=2,3,4; 2 nonempty proper safe-action regions whose union covers W; 2 distinct binary tests. In all cases V<=U. 1035 cases remain impossible to certify due to insufficient tests despite action coverage. No actual feeder model, voltage/current constraint, protection relay, or sensor cost was simulated.
Correction commit d259ef993eb9edb7a2ce635e0f5b1450ee90a1a3: add coverage condition to exclude no-safe-action states when testing V<=U.

## H1: minimum measurement certificates
Outcome: original novelty hypothesis REJECTED. New possibility: grid-specific physically coupled measurements, noisy/adversarial observation intervals, sequential switching safety, and AC feasibility. Need demonstrate a new restricted tractability theorem or lower bound beyond DRD/ECD and POMDPs. No proof yet.

## H2: protection/transient certificate
Outcome: OPEN, no theorem. Steady-state safety cannot certify inverter transient current/frequency or relay selectivity. A sound reduced-order sufficient certificate could be useful, but requires justified dynamics and numerical cross-checks. Nature Communications 2026 explicitly surveys conservative feasibility screening, so generic safety filters collide.

## H3: communication-loss local restoration
Outcome: OPEN, no theorem. Need formal assumptions about synchronized clocks, island boundary energization, message loss, switch controllability and distributed knowledge; show impossibility or achievable safety/performance bound beyond existing decentralized control. No experimental validation.

## Zig-zag falsifiers
1. Active learning: DRD reduction destroys broad H1 originality.
2. Information theory: strict decision-vs-identification separation is true but elementary.
3. Logical coverage: no-safe-action states destroy unqualified V<=U claim.
4. Physical grid: abstract safe regions cannot imply real voltage, protection, or transient safety.
5. Adversarial sensing: deterministic exact tests omit telemetry noise, corruption and latency.
6. Dynamic systems: each action changes W and observations; static DRD recurrence is inadequate but dynamic POMDP/planning prior art is substantial.
7. Communication: centralized test selection may fail under disconnection; distributed impossibility boundaries remain to formulate.
8. Reproducibility: exhaustive finite cases are tests of implementation and simple propositions, not field evidence.

## Decision
STOP before manuscript. For a Q1-strength candidate, prioritize H2 if engineering validation resources are available, otherwise formulate grid-specific constrained H1/H3 and prove a result not implied by DRD/ECD. Gate 3 should not be presented as approved until user decides direction. Patent audit and comprehensive theory bibliography still pending.
