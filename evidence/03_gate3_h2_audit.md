# Gate 3 — H2 model, prior-art collision and preliminary falsification
Date: 2026-10-22. Status: CONDITIONAL / H2 not validated; Gate 4 not approved.

## Literature threats — publisher/official records
1. Baeckeland et al. 2024, IEEE TPEL 39(11):14493-14517, DOI 10.1109/TPEL.2024.3430316 — inverter current limiting, stability, protection and fault recovery reviewed. General current-limit-aware screening is not new.
2. Unified Model of Current-Limiting Grid-Forming Inverters for Large-Signal Analysis, IEEE TPWRS 41(1):198-213 (2026), DOI 10.1109/TPWRS.2025.3587224 — current-limiter mode impacts large-signal instability; validated using EMT and hardware. Authors not fully verified, hence pending.
3. Modeling Fault Recovery and Transient Stability of Grid-Forming Converters Equipped With Current Reference Limitation, IEEE TEC 40(2):1140-1152 (2025), DOI 10.1109/TEC.2024.3507544 — current saturation escape and stable/saturated/unstable post-fault modes.
4. Mohiuddin et al. 2025, IEEE TIA 61(4):6472-6483, DOI 10.1109/TIA.2025.3544164 — two-stage limiter with EMT simulation; current limiter dynamics are an existing engineering area.
5. Pal, Achlerkar, Panigrahi 2025, Electric Power Systems Research 242:111471, DOI 10.1016/j.epsr.2025.111471 — fault-induced current limitation and ride-through logic.
6. Baeckeland & Seo 2023/2024, NREL/CP-5D00-87250 — 1200 EMT black-start simulation comparisons. Distinct black-start novelty cannot rest on testing inverters alone.
7. Earlier Gate 1 source: Shi, Bai & Wang 2026, Nature Communications DOI 10.1038/s41467-026-76692-0 — black-start restoration with dynamics/protection already considered.

## Cross-disciplinary collision status
Reachability: generic interval/tube propagation is established; no claim of new formal method.
Barrier functions: invariant-set / barrier safety certification already exists generally; exact grid-specific comparison pending.
Robust MPC: established constrained receding-horizon control; no novelty asserted.
Protection coordination: limited fault currents can make conventional overcurrent selectivity unreliable; no real relay model implemented.
Hybrid dynamics: inverter limiter switching, protection trips, topology switching and cold-load pickup make single-mode steady-state bounds insufficient.
Benchmark realism: public IEEE feeders are primarily network test models, not calibrated inverter/controller/relay datasets.

## Mathematical surrogate (explicitly not power-grid model)
ODE x'(t)=-a*x(t)+d, with a in [amin,amax], amin>0, |d|<=D, x(0)=x0. For all t>=0,
|x(t)| <= |x0| exp(-amin*t) + (D/amin)(1-exp(-amin*t))
<= max(|x0|,D/amin).
Proof: variation-of-constants; |integral exp(-a(t-s))d ds| <= D(1-exp(-a*t))/a; monotonic comparison in a.
Sufficient certificate max(|x0|,D/amin)<=L. This is elementary and not a new result. It does NOT cover inverter current, voltage, frequency multi-state dynamics, relay selectivity, or switching transients.

## Independent numerical experiment
Run: python3 evidence/gate3_scalar_certificate.py
Grid: 5 initial states * 3 a-intervals * 3 d-intervals * 3 limits = 135 cases.
For each, sample 3 a values and 3 d values, integrate exact scalar affine ODE with zero-order-hold 0.5 ms steps to T=2s.
Output: cases=135 certified=67 rejected=68 false_safe=0 conservative_on_sample=1.
A zero sampled false-safe rate is NOT statistical or physical proof; the scalar analytical bound is sound under the stated scalar model only.
The 1 conservative sampled rejection may arise from a finite horizon or unsampled parameter combinations. No speedup versus EMT was measured.

## Public feeder / simulator acquisition
Candidate model source: https://github.com/GRIDAPPSD/Powergrid-Models (IEEE123, IEEE8500 etc.); OpenDSS https://opendss.epri.com/.
A local direct raw GitHub download attempt failed due unavailable network DNS. Therefore NO feeder files were obtained, licensed, checksummed, parsed or simulated in this gate. No OpenDSS or PSCAD/EMT run occurred. Feeder license, switch locations, DER parameters, protection settings, and controller data remain unverified.
This is a hard gate limitation, not an implied completion.

## Proposed next mathematically defensible model (not yet implemented)
Hybrid differential-algebraic system: mode q=(topology,limiter states,protection states), x=(angle/frequency,voltage-controller,filter,DC-link,load recovery states), algebraic y=AC network voltages/currents, x'=f_q(x,y,u,p), 0=g_q(x,y,u,p). Guards for current saturation, relay pickup/trip, switching and cold-load transitions. Uncertainty p in bounded physically justified set.
Safety predicate requires all trajectories and intermediate switching modes satisfy I_inv <= I_max(t), Vmin(t)<=V<=Vmax(t), frequency bounds, and fault selectivity/clearing within modeled times.
Certificate output: SAFE only when proven under a specified model; UNSURE otherwise. Compare against EMT numerical baselines, conservative interval reachability, full dynamic simulations, and known protection-aware restoration filters. Dynamic simulations alone are not formal soundness proofs.

## Falsification priority
F1 current saturation invalidates unsaturated linear droop approximation.
F2 protection pickup may fail because I_fault <= inverter clamp; steady-state feasible does not imply fault clearance.
F3 cold-load pickup causes transient current spikes despite final load feasibility.
F4 uncertain controller parameters cause instability despite nominal certificate.
F5 network reconfiguration intermediate modes violate constraints even if final topology feasible.
F6 overly conservative certificate always rejects; report certification coverage, not only zero unsafe accepts.
F7 no claimed novelty unless a new power-specific bound / efficient exact restricted algorithm survives comparison with prior art.

## Gate verdict
PARTIAL EVIDENCE ONLY. Surrogate math and test executed; actual feeder dataset, dynamic inverter model, relay model, independent EMT baseline and physical safety certificate NOT achieved. No publication readiness. Gate 4 must not start automatically.
