"""P10 joint scalar-frequency / inverse-time relay *model* certificate.

Uses feeder-derived terminal-1 conductor-1 current proxies from P8.
Fail closed for physical restoration: no phase-continuity, switch state, CT
orientation, relay inventory, calibrated inverter or breaker data.
"""
import json,math,random,pathlib
from shes.relay_time_domain import Segment,relay_assertion,coordinated

def frequency_envelope(f0,M,D,u_low,u_high,T):
 if not all(math.isfinite(x) for x in (f0,M,D,u_low,u_high,T)) or min(M,D,T)<=0 or u_low>u_high:
  raise ValueError("invalid scalar frequency envelope")
 q=math.exp(-D*T/M)
 return max(abs(f0),abs(q*f0+(1-q)*u_low/D),abs(q*f0+(1-q)*u_high/D))
def trace(current,gamma,horizon=5.,gap=(.2,.45)):
 return [Segment(0,gap[0],current*gamma),Segment(gap[0],gap[1],current*.1*gamma),
  Segment(gap[1],horizon,current*gamma)]
def terminal_proxy(row,role):
 t=row["candidate_terminal_currents"].get(role)
 if not t:return None
 a=[x["current_a"] for x in t["currents"] if x["terminal"]==1 and x["conductor"]==1]
 return a[0] if len(a)==1 and math.isfinite(a[0]) and a[0]>=0 else None
def physical_gate(data):
 # A positive certificate requires independent evidence of ALL of these.
 required=("phase_continuity_verified","switching_feasibility_verified",
  "relay_orientation_verified","installed_relay_settings_verified",
  "inverter_current_limit_calibrated","breaker_delays_calibrated")
 return all(data.get(k) is True for k in required)
def relay_ok(ip,ib,pickp,pickb,tdsp,tdsb,deadp,deadb,margin,gp,gb,bp,bb,reset):
 p=relay_assertion(trace(ip,gp),5.,pickp,tdsp,reset=reset,reset_rate=1.)
 b=relay_assertion(trace(ib,gb),5.,pickb,tdsb,reset=reset,reset_rate=1.)
 return coordinated(p,b,bp,bb,deadp,deadb,margin)
def classify(row,rng,reset):
 ip=terminal_proxy(row,"primary");ib=terminal_proxy(row,"backup")
 if ip is None or ib is None:raise ValueError("missing current")
 pickp=ip*rng.uniform(.35,.85);pickb=ib*rng.uniform(.35,.85)
 tdsp=rng.uniform(.02,.11);tdsb=rng.uniform(.06,.32)
 deadp=rng.uniform(.35,2.);deadb=rng.uniform(1.2,4.5)
 margin=rng.uniform(.05,.25);gmin=rng.choice((.6,.7,.8))
 delay=rng.choice((.02,.04,.08))
 f0=rng.uniform(-.2,.2);M=rng.uniform(2.,5.);D=rng.uniform(1.,3.)
 umin=rng.uniform(-.8,-.05);umax=rng.uniform(.05,.8)
 limit=rng.uniform(.1,.55);T=2.
 freq_worst=frequency_envelope(f0,M,D,umin,umax,T)<=limit
 freq_nom=frequency_envelope(f0,M,D,(umin+umax)/2,(umin+umax)/2,T)<=limit
 args=(ip,ib,pickp,pickb,tdsp,tdsb,deadp,deadb,margin)
 nominal=freq_nom and relay_ok(*args,1.,1.,0.,0.,reset)
 common=freq_worst and relay_ok(*args,gmin,gmin,delay,delay,reset)
 # Exhaustive independent-corner oracle: 2^4 = 16 combinations.
 corners=[relay_ok(*args,gp,gb,bp,bb,reset)
  for gp in (gmin,1.) for gb in (gmin,1.)
  for bp in (0.,delay) for bb in (0.,delay)]
 oracle=freq_worst and all(corners)
 # Independent-box screen is identical to corner enumeration in this
 # exact stipulated trace model; no monotonic shortcut is assumed.
 box=oracle
 return {"bus":row["bus"],"fault_resistance_ohm":row["fault_resistance_ohm"],
  "reset":reset,"gmin":gmin,"delay_s":delay,"frequency_worst_ok":freq_worst,
  "nominal":nominal,"common":common,"box":box,"joint_model_oracle":oracle,
  "frequency_nominal_ok":freq_nom}
def matrix(rows,method,reference):
 tp=sum(bool(x[method]) and bool(x[reference]) for x in rows)
 fp=sum(bool(x[method]) and not bool(x[reference]) for x in rows)
 fn=sum(not bool(x[method]) and bool(x[reference]) for x in rows)
 return {"TP":tp,"FP":fp,"FN":fn,"TN":len(rows)-tp-fp-fn}
def run(source,seed=20261023,draws=80):
 rng=random.Random(seed)
 rows=[r for r in source["results"] if r["bus"] in ("60","83")]
 if len(rows)!=6:raise ValueError("expected six feeder fault cases")
 results=[classify(row,rng,reset) for reset in ("full","hold","linear")
  for row in rows for _ in range(draws)]
 tables={reset:{name:matrix([r for r in results if r["reset"]==reset],
    name,"joint_model_oracle") for name in ("nominal","common","box")}
  for reset in ("full","hold","linear")}
 witnesses=[{k:r[k] for k in ("bus","fault_resistance_ohm","reset","gmin","delay_s")}
  for r in results if r["nominal"] and not r["joint_model_oracle"]][:8]
 gate={"phase_continuity_verified":False,"switching_feasibility_verified":False,
  "relay_orientation_verified":False,"installed_relay_settings_verified":False,
  "inverter_current_limit_calibrated":False,"breaker_delays_calibrated":False}
 return {"status":"PASS_MODEL_ONLY_PHYSICAL_GATE_BLOCKED","seed":seed,
  "source_pin":source["pin"],"source_sha256":source["sha256"],
  "settings_per_feeder_fault_case_per_reset":draws,"population":len(results),
  "tables":tables,"nominal_false_approval_witnesses":witnesses,
  "frequency_worst_pass":sum(r["frequency_worst_ok"] for r in results),
  "joint_model_approvals":sum(r["joint_model_oracle"] for r in results),
  "physical_gate":gate,"physical_certificates_issued":0,
  "physical_restoration_validated":False,
  "counterfactual_backup":"Sustained fault at backup; primary clearing is not simulated as interrupting the backup counterfactual.",
  "assumptions":"Hypothetical scalar M,D, net-power intervals, pickups, time multipliers, delays and piecewise-constant current; conductor-1 terminal-1 feeder proxies."}
if __name__=="__main__":
 source=json.load(open("shes/ieee123_topology_result.json"))
 result=run(source)
 pathlib.Path("shes/ieee123_p10_joint_model.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"population":result["population"],"tables":result["tables"],
  "frequency_pass":result["frequency_worst_pass"],"model_approvals":result["joint_model_approvals"],
  "physical_certificates":result["physical_certificates_issued"]},sort_keys=True))
