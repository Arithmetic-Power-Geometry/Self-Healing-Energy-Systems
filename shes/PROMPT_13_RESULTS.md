# SHES Prompt 13 — continuous-uncertainty mathematical audit

## New rigorous result
For fixed nonnegative piecewise-constant current templates scaled by a nonnegative gamma, and fixed initial progress, pickup, time multiplier and reset semantics (full/hold/linear), the stipulated inverse-time relay assertion time is nonincreasing in gamma. Therefore, if primary and backup scalings and both breaker delays vary independently over a Cartesian product of closed intervals, all-scenario clearing deadlines and the backup assertion versus primary clearing margin hold **if and only if** three endpoint inequalities hold with finite required assertions. See shes/p13_continuum_section.tex for formal statements and proofs.

## Counterexample
For a *common correlated gamma*, primary trace 1 A from 0–20 s, backup trace 0 A from 0–1 s then 1 A from 1–20 s, primary pickup .193 A, backup pickup .274 A, inverse-time constants .020 and .0046, exponent .02, and margin .4 s, the coordination difference at gamma=.28 is about 8.938 s, at gamma=.38 about .235 s, and at gamma=1 about .577 s. Both correlated endpoints pass but the interior fails. This is an analytic counterexample, not a statistical inference.

## Scope of theorem
- Exact for the stipulated scalar current-scale and reset timer model with a rectangular independent uncertainty set.
- The same rectangular test is sufficient but potentially conservative for correlated subsets of that rectangle.
- Endpoint tests along only a correlated diagonal are not sufficient.
- Does not cover gamma-dependent waveform shapes, varying reset parameters, manufacturer firmware, current-direction/CT effects, inverter limiter transients, or physical switching feasibility.
- Backup is a sustained-fault counterfactual; backup breaker delay enters its deadline, not the assertion-based coordination margin.
- Frequency envelope remains a separate model-level condition; no field restoration is authorized.

## Reproducibility
Source: shes/robust_continuum_p13.py
Adversarial regression: shes/test_robust_continuum_p13.py
Formal manuscript section: shes/p13_continuum_section.tex
CI: .github/workflows/shes-p13-continuum.yml

## Remaining work
1. Integrate this section into the full manuscript's main.tex and compile a clean bibliography-resolved PDF in GitHub; complete manuscript source transfer remains pending from Prompt 12.
2. Verify numerical witness against independent high-precision calculations.
3. For broader waveform uncertainty, develop interval-enclosed timer integration or formally state finite-scenario limitations.
4. Carry out Prompt 14 phase-aware energized feeder connectivity and switching-state audit.
