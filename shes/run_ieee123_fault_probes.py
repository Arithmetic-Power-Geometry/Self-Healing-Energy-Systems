#!/usr/bin/env python3
"""Reproducible phase-aware IEEE123 OpenDSS fault probes; not relay validation."""
import argparse, hashlib, json, math, pathlib, re
from collections import deque
from evidence.run_ieee123_baseline import deps
from shes.candidate_protection_paths import candidate_paths

PIN="5005c668a72d20775f4c2d060feebb2866ba1d38"
def cmd(d,text):
 d.Text.Command=text
 if int(d.Error.Number): raise RuntimeError(f"{text}: {d.Error.Number} {d.Error.Description}")
def source_hashes(root):
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
         for p in sorted(deps(root,"IEEE123Master.dss"))}
def buses_and_lines(d):
 names={str(x).lower():str(x) for x in d.ActiveCircuit.AllBusNames}
 lines=[]
 if d.ActiveCircuit.Lines.First:
  while True:
   name=str(d.ActiveCircuit.Lines.Name); b1=str(d.ActiveCircuit.Lines.Bus1).split(".")[0].lower()
   b2=str(d.ActiveCircuit.Lines.Bus2).split(".")[0].lower()
   lines.append({"name":name,"from":b1,"to":b2})
   if not d.ActiveCircuit.Lines.Next: break
 return names,lines
def choose_locations(d,names):
 # Three deliberately named, auditable fault buses. Fail rather than silently substitute.
 locations=["150","60","83"]
 if any(b not in names for b in locations):
  raise ValueError(f"Required fault buses missing: {locations}; sample {list(names)[:20]}")
 out=[]
 for bus in locations:
  d.ActiveCircuit.SetActiveBus(names[bus])
  nodes=[int(x) for x in d.ActiveCircuit.ActiveBus.Nodes if 1<=int(x)<=3]
  if not nodes: raise ValueError(f"No energized phase nodes at bus {bus}")
  out.append({"bus":names[bus],"phases":sorted(set(nodes))})
 return out
def choose_switch(lines,locations):
 # Deterministic existing line selected from an auditable candidate list.
 # This is a line-outage sensitivity, NOT an operationally approved switch.
 fault_buses={x["bus"].lower() for x in locations}
 for item in sorted(lines,key=lambda x:x["name"].lower()):
  if item["from"] not in fault_buses and item["to"] not in fault_buses:
   return item
 raise ValueError("No candidate line for switching-state sensitivity")
def read_fault_current(d):
 d.ActiveCircuit.SetActiveElement("Fault.shes_probe")
 elem=d.ActiveCircuit.ActiveCktElement
 vals=list(map(float,elem.CurrentsMagAng))
 if len(vals)<2 or not math.isfinite(vals[0]) or vals[0]<0:
  raise ValueError("Invalid fault current magnitude")
 return vals[0]
def run(root,out):
 root=root.resolve();out=out.resolve()
 out.parent.mkdir(parents=True,exist_ok=True);out.unlink(missing_ok=True)
 hashes=source_hashes(root)
 from dss import DSS
 d=DSS.NewContext()
 cmd(d,f'compile "{root/"IEEE123Master.dss"}"')
 names,lines=buses_and_lines(d)
 locations=choose_locations(d,names)
 selected=choose_switch(lines,locations)
 cases=[]
 for state in ("as_published","line_disabled"):
  for loc in locations:
   for phase in loc["phases"]:
    for r in (0.01,0.1,1.0):
     # Fresh circuit for each scenario prevents fault and control-state leakage.
     cmd(d,f'compile "{root/"IEEE123Master.dss"}"')
     if state=="line_disabled":
      cmd(d,f'edit Line.{selected["name"]} enabled=no')
     cmd(d,"set mode=snapshot")
     cmd(d,"set controlmode=off")
     cmd(d,"set maxiterations=100")
     cmd(d,f"new Fault.shes_probe phases=1 bus1={loc['bus']}.{phase} r={r}")
     cmd(d,"solve")
     converged=bool(d.ActiveCircuit.Solution.Converged)
     if not converged: raise RuntimeError(f"Nonconvergent fault case {state}/{loc['bus']}/{phase}/{r}")
     amps=read_fault_current(d)
     cases.append({"switch_state":state,"bus":loc["bus"],"phase":phase,
       "fault_resistance_ohm":r,"fault_current_a":amps,"converged":True})
 if len(cases)<18:raise ValueError("Insufficient cases")
 data={"status":"PASS_FAULT_PROBE_ONLY","upstream_commit":PIN,"dss_python_expected":"0.15.7",
  "feeder_hashes":hashes,"switch_sensitivity":{"line":selected["name"],
   "bus1":selected["from"],"bus2":selected["to"],"states":["as_published","line_disabled"],
   "operationally_validated":False},
  "fault_locations":locations,"candidate_relay_boundaries":candidate_paths(lines,"150",["60","83"]),"cases":cases,"fault_current_validated":True,
  "relay_coordination_validated":False,"protection_validated":False,
  "frequency_dynamics_validated":False,"emt_validated":False,
  "limitations":"Single-phase-to-ground Fault element probes in snapshot solve; not dynamic inverter or relay operation."}
 out.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"cases":len(cases),"switch_line":selected["name"],
   "min_a":min(x["fault_current_a"] for x in cases),
   "max_a":max(x["fault_current_a"] for x in cases),"locations":locations}))
 return data
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--feeder",type=pathlib.Path,required=True)
 p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 run(a.feeder,a.output)
