"""Independent structural validation of IEEE123 fault-probe JSON."""
import argparse,json,math
from collections import defaultdict
def validate(d):
 if d.get("status")!="PASS_FAULT_PROBE_ONLY":raise ValueError("bad status")
 if d.get("upstream_commit")!="5005c668a72d20775f4c2d060feebb2866ba1d38":raise ValueError("unverified feeder revision")
 for k in ("relay_coordination_validated","protection_validated","frequency_dynamics_validated","emt_validated"):
  if d.get(k) is not False:raise ValueError("unsupported protection claim")
 h=d.get("feeder_hashes",{})
 if "IEEE123Master.dss" not in h or any(len(x)!=64 or any(c not in "0123456789abcdef" for c in x) for x in h.values()):raise ValueError("invalid source hashes")
 cases=d.get("cases",[])
 if not isinstance(cases,list) or len(cases)<18:raise ValueError("missing fault cases")
 seen=set(); groups=defaultdict(dict)
 for c in cases:
  key=(c["switch_state"],c["bus"],c["phase"],c["fault_resistance_ohm"])
  if key in seen:raise ValueError("duplicate case")
  seen.add(key)
  if c["switch_state"] not in ("as_published","line_disabled"):raise ValueError("unknown state")
  if c["bus"] not in ("150","60","83") or c["phase"] not in (1,2,3):raise ValueError("invalid location/phase")
  if c["fault_resistance_ohm"] not in (.01,.1,1.):raise ValueError("unexpected fault resistance")
  if c["converged"] is not True or not isinstance(c["fault_current_a"],(float,int)) or not math.isfinite(c["fault_current_a"]) or c["fault_current_a"]<0:raise ValueError("invalid fault result")
  groups[(c["switch_state"],c["bus"],c["phase"])][c["fault_resistance_ohm"]]=c["fault_current_a"]
 for k,v in groups.items():
  if set(v)!={.01,.1,1.}:raise ValueError("incomplete resistance sweep")
 for state in ("as_published","line_disabled"):
  for bus in ("150","60","83"):
   if not any(k[0]==state and k[1]==bus for k in groups):raise ValueError("missing switch/bus pairing")
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("json");a=p.parse_args()
 validate(json.load(open(a.json)));print("PASS: fault probe schema, completeness, provenance and claim scope")
