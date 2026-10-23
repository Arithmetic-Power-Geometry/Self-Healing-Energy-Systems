# SHES Prompt 2 — mathematical certificate corrections (2026-10-23)

## Verified mathematical refinements
**Scalar model:** M f'(t)+D f(t)=u(t), M,D>0, u(t) in [Uminus,Uplus]. Define q(t)=exp(-Dt/M).
For every measurable admissible input, q(t)f0+(1-q(t))Uminus/D <= f(t) <= q(t)f0+(1-q(t))Uplus/D.
Therefore the finite-horizon *sign-aware* sufficient envelope is
Bsign(T)=max(|f0|, |q(T)f0+(1-q(T))Uminus/D|, |q(T)f0+(1-q(T))Uplus/D|).
Proof: variation of constants with positive kernel; endpoints are affine in q(t), which decreases from 1 to q(T), so extrema of their absolute values occur at horizon endpoints. For independent rectangular load and derating intervals, corner inputs can attain each signed endpoint. This is a guarantee only for the stipulated scalar model.

**Units:** f [Hz], t [s], P,L [power], M [power*s^2/Hz], D [power/Hz]. The symbol Imax in the original scalar equation is an effective *power-capacity proxy*, not physical amperes; r [1/power]. An electrical-current interpretation needs explicit voltage and conversion modeling.

**Relay:** for I>pickup, trip(I)=0.14 s * TDS / ((I/pickup)^0.02-1), with dimensionless TDS. Strict pickup at equality means non-operation. The function decreases with I; independent gamma_p,gamma_b in [gamma_min,1] and independent delay tau in [0,tau_max] imply the worst primary time at (gamma_min,tau_max), earliest backup at (1,0), and latest backup at (gamma_min,tau_max). These give sufficient primary deadline, backup hypothetical sustained-fault deadline, and coordination inequalities. Include breaker delay consistently if claimed.

**Joint semantics:** Frequency and relay predicates can be conjoined only over the same action, uncertainty domain, model and horizon. Constant-current inverse-time and time-varying full-reset definite-time are alternative relay abstractions, not automatically interchangeable. Backup trip time is counterfactual under sustained fault; backup should not trip after successful primary clearing.

**Full-reset definite-time:** zero initial timer, piecewise-constant intervals covering [0,deadline], strict pickup, full reset on below-pickup, positive dwell and inclusive deadline. A trip occurs iff a contiguous above-pickup segment reaches required dwell by the deadline.

## Local tests
Six unittest cases passed: 2500 randomized scalar inputs (100 intervals each); finite-horizon zero and sign-aware tightness; 2000 randomized relay configurations with 10 independent uncertainty draws each; relay pickup equality/monotonicity; timer reset, dwell and deadline boundaries.

## Source and validation
The complete revised LaTeX source and four PDF figures were assembled in the local downloadable Prompt 2 package; **they have not all been transferred to GitHub**. The current GitHub connector writes UTF-8 files but not binary PDFs; the runtime's git HTTPS remote is inaccessible. No new electrical feeder or hardware results were produced. pdflatex completed a single pass, but BibTeX is unavailable, so the compiled PDF is not a clean final reference-resolved build.

## Next research work
Implement formally compatible time-domain inverse-time integration/reset model, strengthen the joint theorem with explicit cross-domain uncertainty and breaker semantics, and add model-based adversarial test oracles. Avoid claiming physical safety or 100/100 before external validation.
