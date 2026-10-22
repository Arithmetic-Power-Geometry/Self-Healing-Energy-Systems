# Scalar CLPU analytical envelope: 2592 cases

Executed locally 2026-10-22 with Python 3. Observed JSON: `{"analytically_enclosed": 402, "by_tau": {"0.15": 134, "0.4": 134, "1.2": 134}, "scope": "scalar ODE only", "total": 2592}`.

For nonnegative pickup and voltage sensitivity, L(t) lies in [p0,p0+clp], v(t)=1-rL(t) lies in [1-r(p0+clp),1-r p0], and P(t)=min(pref,imax*v(t)) lies between its endpoint values. Therefore |P-L| is bounded by U=max(|Pmin-Lmax|,|Pmax-Lmin|). For m>0,d>0, m f'=P-L-d f implies |f(t)|<=max(|f(0)|,U/d) for all t>=0. This is a scalar ODE comparison bound, not an electrical power system theorem.

The previous 2592-case certificate used the looser Pmax=min(pref,imax), yielding 396 accepted; the refined endpoint bound yields 402 accepted. This difference is a tighter sufficient bound, not six independently confirmed physically safe cases. The algebraic voltage/current and relay checks remain idealized; physical feeder, EMT and protection selectivity gates are open.
