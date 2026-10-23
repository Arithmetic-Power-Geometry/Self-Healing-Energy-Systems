"""P9 model-relative protection screens from P8 terminal-current evidence.
No installed relays or energized phase-specific path have been verified.
"""
import json,math,pathlib,random
from shes.relay_time_domain import inverse_time_constant,relay_assertion,Segment,coordinated
def screen(ip,ib,pickp,pickb,tdsp,tdsb,dp,db,margin,gmin=.7,delay=.04):
 def pair(gp,gb,bp,bb):
  return coordinated(inverse_time_constant(ip*gp,pickp,tdsp),
   inverse_time_constant(ib*gb,pickb,tdsb),bp,bb,dp,db,margin)
 nominal=pair(1,1,0,0)
 common=pair(gmin,gmin,delay,delay)
 tp=inverse_time_constant(ip*gmin,pickp,tdsp)
 tbmin=inverse_time_constant(ib,pickb,tdsb)
 tbmax=inverse_time_constant(ib*gmin,pickb,tdsb)
 box=(all(math.isfinite(x) for x in (tp,tbmin,tbmax))
  and tp+delay<=dp and tbmax+delay<=db and tbmin-(tp+delay)>=margin)
 oracle=all(pair(gp,gb,bp,bb) for gp in (gmin,1.) for gb in (gmin,1.)
   for bp in (0.,delay) for bb in (0.,delay))
 if box!=oracle:raise AssertionError("independent-box corner theorem failed")
 return {"nominal":nominal,"common":common,"box":box,"constant_corner_oracle":oracle}
def trace_screen(ip,ib,pickp,pickb,tdsp,tdsb,dp,db,margin,
  gmin=.7,delay=.04,pulse=.2,gap=.2,horizon=6.):
 # Counterfactual primary and backup receive the same stipulated dropout geometry.
 def make(i):
  return [Segment(0,pulse,i),Segment(pulse,pulse+gap,.1*i),
   Segment(pulse+gap,horizon,i)]
 p=relay_assertion(make(ip*gmin),horizon,pickp,tdsp,"full")
 b=relay_assertion(make(ib),horizon,pickb,tdsb,"full")
 return coordinated(p,b,delay,0.,dp,db,margin)
def case_current(row,role):
 t=row["candidate_terminal_currents"].get(role)
 if not t:return None
 # Conductor 1 at terminal 1 is a reproducible proxy; physical CT/phase mapping unknown.
 v=[x["current_a"] for x in t["currents"] if x["terminal"]==1 and x["conductor"]==1]
 return v[0] if len(v)==1 else None
def evaluate(data,seed=20261023,draws=200):
 rng=random.Random(seed);cases=[]
 for row in data["results"]:
  if row["bus"] not in ("60","83"):continue
  ip=case_current(row,"primary");ib=case_current(row,"backup")
  if ip is None or ib is None:raise ValueError("missing terminal currents")
  for k in range(draws):
   # Settings are intentionally hypothetical, drawn relative to model current.
   pickp=ip*rng.uniform(.35,.9);pickb=ib*rng.uniform(.35,.9)
   tdsp=rng.uniform(.02,.12);tdsb=rng.uniform(.06,.4)
   dp=rng.uniform(.35,1.8);db=rng.uniform(1.5,4.5)
   margin=rng.uniform(.05,.3);gmin=rng.choice((.6,.7,.8))
   delay=rng.choice((.02,.04,.08))
   s=screen(ip,ib,pickp,pickb,tdsp,tdsb,dp,db,margin,gmin,delay)
   time=trace_screen(ip,ib,pickp,pickb,tdsp,tdsb,dp,db,margin,gmin,delay)
   cases.append({"bus":row["bus"],"resistance":row["fault_resistance_ohm"],
    "draw":k,"gmin":gmin,"delay":delay,**s,"full_reset_trace":time,
    "primary_terminal_a":ip,"backup_terminal_a":ib})
 screens=("nominal","common","box","full_reset_trace")
 tables={}
 for reference in ("constant_corner_oracle","full_reset_trace"):
  tables[reference]={}
  for method in screens:
   tp=sum(bool(x[method]) and bool(x[reference]) for x in cases)
   fp=sum(bool(x[method]) and not bool(x[reference]) for x in cases)
   fn=sum(not bool(x[method]) and bool(x[reference]) for x in cases)
   tn=len(cases)-tp-fp-fn
   tables[reference][method]={"TP":tp,"FP":fp,"FN":fn,"TN":tn}
 sensitivity={}
 for g in (.6,.7,.8):
  sub=[x for x in cases if x["gmin"]==g]
  sensitivity[str(g)]={m:sum(bool(x[m]) for x in sub) for m in screens}
 witnesses=[{k:x[k] for k in ("bus","resistance","draw","gmin","delay","primary_terminal_a","backup_terminal_a")}
  for x in cases if x["box"] and not x["full_reset_trace"]][:5]
 return {"status":"PASS_HYPOTHETICAL_SCREENS_ONLY","source_pin":data["pin"],
  "source_sha256":data["sha256"],"seed":seed,"draws_per_fault_case":draws,
  "population":len(cases),"tables":tables,"sensitivity":sensitivity,
  "counterexamples":witnesses,"phase_continuity_verified":False,
  "switching_feasibility_verified":False,"relay_current_orientation_verified":False,
  "installed_relay_settings_verified":False,"frequency_certificate_verified":False,
  "restoration_safety_verified":False,
  "interpretation":"Conductor-1 terminal-1 model proxies and hypothetical settings; not a joint feeder restoration safety certificate."}
if __name__=="__main__":
 src=json.load(open("shes/ieee123_topology_result.json"))
 out=evaluate(src);pathlib.Path("shes/ieee123_p9_screens.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"population":out["population"],"tables":out["tables"],
  "witnesses":len(out["counterexamples"])},sort_keys=True))
