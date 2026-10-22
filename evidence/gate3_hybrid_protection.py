"""Gate 3 extension: explicit simplified hybrid inverter/relay restoration model.
Not calibrated to a feeder; not an EMT or physical-grid safety certification.
Independent solve_ivp simulation versus conservative analytical screening.
Requires scipy. Run: python evidence/gate3_hybrid_protection.py
"""
from itertools import product
from math import exp
from scipy.integrate import solve_ivp

T = 3.0

def certificate(p):
    load_hi = p["p0"] + p["clp"]
    vmin = 1 - p["r"] * load_hi
    if vmin <= 0:
        return False, "voltage collapse bound"
    load_i = load_hi / vmin
    if vmin < p["v_floor"]:
        return False, "voltage"
    if load_i > p["imax"]:
        return False, "load current"
    pmin = min(p["pref"], p["imax"] * vmin)
    pmax = min(p["pref"], p["imax"])
    uabs = max(abs(pmin - load_hi), abs(pmax - p["p0"]))
    fbound = max(abs(p["f0"]), uabs / p["d"])
    if fbound > p["fmax"]:
        return False, "frequency"
    if min(p["ifault"], p["imax"]) < p["pickup"]:
        return False, "relay blind"
    if p["trip_delay"] > p["trip_deadline"]:
        return False, "relay slow"
    return True, "certified in toy model"

def baseline(p):
    def rhs(t, y):
        load = p["p0"] + p["clp"] * exp(-t / p["tau"])
        v = 1 - p["r"] * load
        cmd = min(p["pref"], p["imax"] * max(0, v))
        return [(cmd - load - p["d"] * y[0]) / p["m"]]
    sol = solve_ivp(rhs, (0, T), [p["f0"]], rtol=1e-10,
                    atol=1e-12, max_step=.003, dense_output=True)
    peak = max(abs(float(sol.sol(T * i / 1500)[0])) for i in range(1501))
    load_hi = p["p0"] + p["clp"]
    vmin = 1 - p["r"] * load_hi
    current = load_hi / vmin if vmin > 0 else float("inf")
    fault_i = min(p["ifault"], p["imax"])
    return (sol.success and peak <= p["fmax"] + 1e-8
            and vmin >= p["v_floor"] - 1e-8
            and current <= p["imax"] + 1e-8
            and fault_i >= p["pickup"]
            and p["trip_delay"] <= p["trip_deadline"]), peak

def run():
    base = dict(pref=.65, p0=.50, clp=.2, tau=.4, r=.12, imax=1.2,
                f0=0., d=2., m=1., fmax=.18, v_floor=.85,
                ifault=1.1, pickup=.8, trip_delay=.1, trip_deadline=.15)
    counts = dict(total=0, certified=0, baseline_safe=0,
                  false_accept=0, conservative=0)
    witnesses = []
    for clp, imax, pickup, delay, fmax in product(
        (.05, .2, .4), (.7, 1., 1.4), (.6, 1., 1.3), (.08, .2), (.12, .25)
    ):
        p = {**base, "clp": clp, "imax": imax, "pickup": pickup,
             "trip_delay": delay, "fmax": fmax}
        c, why = certificate(p)
        s, peak = baseline(p)
        counts["total"] += 1
        counts["certified"] += int(c)
        counts["baseline_safe"] += int(s)
        counts["false_accept"] += int(c and not s)
        counts["conservative"] += int(s and not c)
        if len(witnesses) < 8 and s != c:
            witnesses.append((clp, imax, pickup, delay, fmax,
                              why, round(peak, 4), s))
    assert counts["false_accept"] == 0, counts
    print(counts)
    print("discordant samples:", witnesses)
    p = {**base, "clp": .05, "imax": .7, "pickup": 1.0, "fmax": .25}
    assert certificate(p)[1] == "relay blind"
    print("counterexample: relay-blind despite nominal steady load: PASS")

if __name__ == "__main__":
    run()
