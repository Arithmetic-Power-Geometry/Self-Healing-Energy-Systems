"""Fail-closed validation of model-relative topology/terminal probe evidence."""
import argparse,json,math
def validate(d):
 if d.get("status")!="PASS_TOPOLOGY_AND_TERMINAL_PROBES_ONLY":raise ValueError("status")
 if d.get("pin")!="5005c668a72d20775f4c2d060feebb2866ba1d38":raise ValueError("pin")
 if d.get("element_kinds",{}).get("line",0)<100 or d.get("element_kinds",{}).get("transformer",0)<1:raise ValueError("missing graph elements")
 for flag in ("installed_protection_verified","relay_coordination_validated","restoration_safe","inverter_fault_current_validated"):
  if d.get(flag) is not False:raise ValueError("unsupported claim "+flag)
 paths=d.get("candidate_paths",{})
 if set(paths)!={"150","60","83"}:raise ValueError("missing paths")
 for bus in ("60","83"):
  p=paths[bus]
  if p.get("reachable_in_element_graph") is not True or not p.get("path"):raise ValueError("unreachable "+bus)
  if p.get("installed_relay_verified") is not False or p.get("protection_zone_validated") is not False:raise ValueError("unsupported relay mapping")
 cases=d.get("results",[])
 if len(cases)!=9:raise ValueError("case count")
 seen=set()
 for c in cases:
  k=(c["bus"],c["fault_resistance_ohm"])
  if k in seen:raise ValueError("duplicate")
  seen.add(k)
  if c["bus"] not in ("150","60","83") or c["fault_resistance_ohm"] not in (.01,.1,1.):raise ValueError("case grid")
  if c["converged"] is not True:raise ValueError("nonconvergence")
  v=c["bus_voltage_pu"]
  if not v or any(not isinstance(x,(int,float)) or not math.isfinite(x) for x in v):raise ValueError("voltage")
  for role,t in c["candidate_terminal_currents"].items():
   if role not in ("primary","backup") or not t.get("currents"):raise ValueError("terminal")
   if any(not math.isfinite(x["current_a"]) or x["current_a"]<0 or x["phase_identity_verified"] is not False for x in t["currents"]):raise ValueError("terminal currents")
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("json");a=p.parse_args()
 validate(json.load(open(a.json)));print("PASS: topology, terminal arrays and scope limitations")
