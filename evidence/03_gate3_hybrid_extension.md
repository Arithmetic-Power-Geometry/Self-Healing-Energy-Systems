# Gate 3 extension — simplified hybrid inverter/protection screening
Date: 2026-10-22. No paper writing. This is a controlled model feasibility test, not a full engineering validation.

## Model and dimensions
Cold-load pickup P_L(t)=P0+Delta*exp(-t/tau).
Algebraic voltage proxy V(t)=1-r*P_L(t); load current proxy I_L=P_L/V.
Inverter power cap P_inv(t)=min(Pref,Imax*max(V(t),0)).
Frequency deviation f follows M*f' = P_inv(t)-P_L(t)-D*f.
Fault current is represented separately by I_fault_eff=min(I_fault,Imax).
Relay is an instantaneous pickup predicate followed by a fixed deterministic trip delay. Trip passes only when I_fault_eff >= I_pickup and trip_delay <= deadline. This is NOT a dynamic relay or protection selectivity model.
Modes: unsaturated vs power/current-limited command, relay pickup vs blind, relay trip before vs after deadline. No actual switching graph, line impedance matrix, EMT waveforms, or hybrid guard transition solver.

## Sufficient screening argument within toy model
Let L_hi=P0+Delta and V_min=1-r L_hi>0. Assume Delta>=0, r>=0, P0>=0, D>0, M>0, and positive voltage.
Then P_L(t) in [P0,L_hi], V(t) in [V_min,1], and P_inv(t) in [min(Pref,Imax*V_min),min(Pref,Imax)].
Hence |P_inv-P_L| <= U=max(|min(Pref,Imax*V_min)-L_hi|,|min(Pref,Imax)-P0|).
The comparison inequality for f'=(-D*f+u)/M gives |f(t)|<=max(|f(0)|,U/D) for t>=0.
Also I_L(t)=P_L(t)/(1-r P_L(t)) is monotone for 1-rP_L>0, so I_L<=L_hi/V_min.
The screen checks these sufficient bounds and the deterministic fault-current/pickup/deadline predicates.
This is a simple established comparison bound, NOT a new power-systems theorem.
The screening rule is sound only for these exact model definitions, parameter restrictions, and modeled constraints. It is NOT sound for real inverter dynamics, faults, relay curves or full power networks.

## Independent numerical baseline
SciPy solve_ivp RK adaptive integration of frequency equation, tight tolerances, sampled dense output every 2 ms over 3 seconds. Algebraic extrema and relay predicates are computed separately. It is independent from the comparison bound but uses the same simplified equations.
Enumerated 3 CLP amplitudes * 3 inverter current limits * 3 relay pickups * 2 relay delays * 2 frequency limits = 108 configurations.
Observed total=108; certified=20; baseline_safe=22; false_accept=0; conservative=2.
Conservative rejection witnesses: CLP=.4, Imax=1.4, pickup=.6 or 1.0, trip_delay=.08, fmax=.12; bound rejects on frequency, sampled peak frequency .0733. The finite numerical baseline is not a proof of global soundness.
Falsifier: CLP=.05, Imax=.7, relay pickup=1.0; nominal load remains within the inverter capability but fault current is capped below relay pickup, making protection blind.

## Hard gaps before Gate 4
1. This is NOT a physically defensible hybrid differential-algebraic inverter model. No PLL/GFM voltage phase, LCL filter, virtual oscillator/droop mode, limiter switching transients, protection time-current characteristic, phase-unbalance, line power flow, actual fault dynamics, cold-load stochasticity or inverter-control identification.
2. No licensed IEEE feeder file was acquired or executed. No OpenDSS, GridLAB-D, PSCAD, EMTP, PowerFactory or independent EMT baseline.
3. No validated protection selectivity, fault location uncertainty, current-clamp fault waveform or actual relay coordination.
4. No verified novelty against hybrid reachability, barrier functions, robust MPC and existing fast dynamic security screening.
5. No speedup benchmark or real-world deployment safety guarantee.

## Decision
Keep paper/ locked. This exercise confirms why current-limit and relay constraints must be separated, but does NOT satisfy the user-requested physically defensible model and independent electrical simulation baseline. Do not advance to Gate 4 yet. Next step: obtain official feeder plus documented GFM inverter model and implement/compare a hybrid DAE or EMT baseline, or partner with a qualified power-systems lab.
