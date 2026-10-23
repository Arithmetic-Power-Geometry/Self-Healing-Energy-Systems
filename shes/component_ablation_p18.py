"""SHES P18: controlled single-component ablations on P17 synthetic cases.

Exactness refers ONLY to the stipulated independent-rectangle relay model.
All ablations use identical cases. No physical protection or field inference.
"""
import argparse,json,math,pathlib,statistics,time
from shes.unified_benchmark_p17 import cases,confusion,frequency_ok,evaluate
from shes.robust_continuum_p13 import time_at_gamma,correlated_counterexample
from shes.relay_time_domain import coordinated

ABLATIONS=("frequency","primary_deadline","backup_deadline","coordination_margin",
           "timer_memory","independent_derating","breaker_delay")

def conditions(c, reset=None, gp=None, gb=None, delay=None):
    """Independent rectangular extrema; each component is independently auditable."""
    r=c["reset"] if reset is None else reset
    low=c["g_lo"] if gp is None else gp
    high_b=1. if gb is None else gb
    d=c["delay_hi"] if delay is None else delay
    pslow=time_at_gamma(c["primary"],low,c["pp"],c["tp"],r)
    bslow=time_at_gamma(c["backup"],low,c["pb"],c["tb"],r)
    bfast=time_at_gamma(c["backup"],high_b,c["pb"],c["tb"],r)
    return {"frequency":frequency_ok(c),
       "primary_deadline":math.isfinite(pslow) and pslow+d<=c["deadline_p"],
       "backup_deadline":math.isfinite(bslow) and bslow+d<=c["deadline_b"],
       "coordination_margin":all(map(math.isfinite,(pslow,bslow,bfast))) and
            bfast-pslow-d>=c["margin"],
       "finite_assertions":all(map(math.isfinite,(pslow,bslow,bfast)))}

def full(c):
    return all(conditions(c).values())

def ablated(c,name):
    if name not in ABLATIONS:raise ValueError(name)
    if name=="timer_memory":
        # Deliberate approximation: discard all prior progress at each segment
        # (full reset at EVERY segment boundary, including above pickup).
        # This is not an alternative vendor relay model.
        def no_memory(trace,gamma,pickup,tds):
            from shes.relay_time_domain import Segment,relay_assertion
            for seg in trace:
                shifted=[Segment(0.,seg.end-seg.start,seg.current*gamma)]
                t=relay_assertion(shifted,shifted[0].end,pickup,tds,reset="full")
                if math.isfinite(t):return seg.start+t
            return math.inf
        lo=c["g_lo"];d=c["delay_hi"]
        p=no_memory(c["primary"],lo,c["pp"],c["tp"])
        bl=no_memory(c["backup"],lo,c["pb"],c["tb"])
        bf=no_memory(c["backup"],1.,c["pb"],c["tb"])
        return frequency_ok(c) and all(map(math.isfinite,(p,bl,bf))) and (
          p+d<=c["deadline_p"] and bl+d<=c["deadline_b"] and bf-p-d>=c["margin"])
    if name=="independent_derating":
        # Restrict independent gamma_p/gamma_b to a common diagonal; finite
        # endpoint approximation, not correlated continuum certificate.
        return all(evaluate(c,g,g,c["delay_hi"],c["delay_hi"])
                   for g in (c["g_lo"],1.))
    if name=="breaker_delay":
        k=conditions(c,delay=0.)
        return all(k.values())
    k=conditions(c)
    k[name]=True
    return all(k.values())

def witness(c,name):
    k=conditions(c)
    return {"id":c["id"],"reset":c["reset"],"g_lo":c["g_lo"],
       "delay_hi_s":c["delay_hi"],"frequency_floor_hz":c["floor_hz"],
       "frequency_lower_hz":c["f0_hz"]-c["df_hz"],
       "component_truth":k,"full":full(c),"ablated":ablated(c,name)}

def overlap_table(data):
    failures={n:{c["id"] for c in data if ablated(c,n) and not full(c)} for n in ABLATIONS}
    return {"per_ablation_false_approval_ids":{n:sorted(s) for n,s in failures.items()},
       "pairwise_overlap":{a:{b:len(failures[a]&failures[b]) for b in ABLATIONS} for a in ABLATIONS}}

def sensitivity(data,widths=(0.,.1,.2,.3,.4)):
    result=[]
    for width in widths:
        modified=[dict(c,g_lo=1.-width) for c in data]
        yes=[full(c) for c in modified]
        result.append({"width":width,"approved":sum(yes),
            "rejected":len(yes)-sum(yes)})
    return result

def timing(data,repeats=9):
    records={n:[] for n in ("full",)+ABLATIONS}
    # Interleaved and rotated order to reduce systematic warmup bias.
    for r in range(repeats):
        names=list(records)
        names=names[r%len(names):]+names[:r%len(names)]
        for n in names:
            t=time.perf_counter_ns()
            result=[full(c) if n=="full" else ablated(c,n) for c in data]
            assert len(result)==len(data)
            records[n].append((time.perf_counter_ns()-t)/1e6)
    return {n:{"median_ms":statistics.median(v),"min_ms":min(v),"max_ms":max(v),
        "stdev_ms":statistics.stdev(v) if len(v)>1 else 0.,
        "repeats":len(v),"samples_ms":v} for n,v in records.items()}

def run(n=90,seed=1717,repeats=9):
    data=cases(n,seed)
    truth=[full(c) for c in data]
    from shes.unified_benchmark_p17 import screen
    assert truth==[screen(c,"rectangle") for c in data], "independent full reference mismatch"
    ab={}
    for name in ABLATIONS:
        pred=[ablated(c,name) for c in data]
        wrong=[c for c,p,t in zip(data,pred,truth) if p and not t]
        ab[name]={"confusion":confusion(pred,truth),
           "witness":witness(wrong[0],name) if wrong else None,
           "witness_status":"first observed counterexample by stable scenario ID" if wrong else
             "no false approval observed; NOT a proof of redundancy"}
    w=correlated_counterexample()
    assert [x["passes_margin_0_4"] for x in w["samples"]]==[True,False,True]
    return {"study":"SHES P18 synthetic single-component ablation",
       "seed":seed,"n":n,"reset_counts":{r:sum(c["reset"]==r for c in data)
          for r in ("full","hold","linear")},
       "full_approvals":sum(truth),"ablations":ab,"overlap":overlap_table(data),
       "uncertainty_width_sensitivity":sensitivity(data),
       "correlated_continuum_analytic_counterexample":w,
       "timing":timing(data,repeats),
       "definitions":{"timer_memory":"discard all progress at every segment boundary, even above pickup",
         "independent_derating":"common gamma at two endpoints only, not correlated continuum",
         "breaker_delay":"set both uncertain breaker delays to zero",
         "other_components":"omit only the named Boolean gate while retaining finite assertions",
         "reference":"theorem-backed fixed-template independent rectangular model; no field validity"},
       "limitations":["Synthetic model; no physical switching/relay verification",
         "Correlated diagonal endpoints do not prove correlated continuum",
         "Timing variability is descriptive, not statistical significance",
         "Ablations are counterfactual screen definitions, not physical controllers"],
       "physical_restoration_certificates":0}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True)
    p.add_argument("--n",type=int,default=90);p.add_argument("--repeats",type=int,default=9)
    a=p.parse_args();d=run(a.n,1717,a.repeats)
    out=pathlib.Path(a.output).resolve();out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"n":d["n"],"full_approvals":d["full_approvals"],
      "ablations":{k:v["confusion"] for k,v in d["ablations"].items()},
      "sensitivity":d["uncertainty_width_sensitivity"]}))
