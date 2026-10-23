"""P15: source-pinned pre/post switching sensitivity, not operational approval."""
import argparse,collections,json,math,pathlib
from shes.run_ieee123_fault_probes import PIN,cmd,source_hashes
from shes.phase_topology_p14 import read_records,split_bus

def transformer_evidence(d):
 out=[]
 for name in d.ActiveCircuit.AllElementNames:
  if not name.lower().startswith("transformer."):continue
  d.ActiveCircuit.SetActiveElement(name);e=d.ActiveCircuit.ActiveCktElement
  out.append({"element":name,"terminal_buses":list(e.BusNames),
   "num_phases":int(e.NumPhases),"num_conductors":int(e.NumConductors),
   "connection_transfer_verified":False,
   "reason":"OpenDSS terminal bus labels and winding count alone do not certify a one-to-one phase transfer; neutral, delta, regulator and winding model require explicit treatment"})
 return out

def candidate_switches(records):
 # Only explicit named 'sw' line objects; never invent a tie or treat any line as switch.
 return [r for r in records if r["kind"]=="line" and
   r["name"].lower().split(".")[-1].startswith("sw") and r["enabled"]]

def bus_voltage_summary(d,buses=("60","83")):
 out={}
 for b in buses:
  d.ActiveCircuit.SetActiveBus(b);bus=d.ActiveCircuit.ActiveBus
  nodes=list(map(int,bus.Nodes));pu=list(map(float,bus.puVmagAngle))[::2]
  vals=[v for n,v in zip(nodes,pu) if n in (1,2,3)]
  out[b]={"phase_nodes":[n for n in nodes if n in (1,2,3)],
   "voltage_pu":[v for n,v in zip(nodes,pu) if n in (1,2,3)],
   "finite":bool(vals) and all(math.isfinite(x) for x in vals)}
 return out

def signed_terminal_current(d,name):
 d.ActiveCircuit.SetActiveElement(name);e=d.ActiveCircuit.ActiveCktElement
 raw=list(map(float,e.Currents));nc=int(e.NumConductors)
 if len(raw)<4*nc:raise ValueError("insufficient terminal complex currents")
 return {"element":name,"terminal_1":[[raw[2*i],raw[2*i+1]] for i in range(nc)],
   "terminal_2":[[raw[2*(nc+i)],raw[2*(nc+i)+1]] for i in range(nc)],
   "sign_convention":"OpenDSS currents into element terminals; NOT installed CT polarity",
   "ct_polarity_verified":False}

def analyze(root,output):
 from dss import DSS
 root=pathlib.Path(root).resolve();output=pathlib.Path(output).resolve()
 d=DSS.NewContext();master=root/"IEEE123Master.dss"
 cmd(d,f'compile "{master}"')
 base=read_records(d);switches=candidate_switches(base)
 if not switches:raise RuntimeError("no documented named switch candidates")
 transformers=transformer_evidence(d)
 # Exactly one reproducible switch-outage sensitivity. Closing a documented open tie
 # is NOT attempted, because no operationally permitted restoration plan is supplied.
 selected=switches[0];cases=[]
 for state in ("published","named_switch_disabled"):
  cmd(d,f'compile "{master}"')
  if state=="named_switch_disabled":cmd(d,f'edit {selected["name"]} enabled=no')
  cmd(d,"set mode=snapshot");cmd(d,"set controlmode=off")
  cmd(d,"set maxiterations=100");cmd(d,"solve")
  converged=bool(d.ActiveCircuit.Solution.Converged)
  volt=bus_voltage_summary(d)
  d.ActiveCircuit.SetActiveElement(selected["name"])
  e=d.ActiveCircuit.ActiveCktElement
  enabled=bool(e.Enabled)
  currents=signed_terminal_current(d,selected["name"]) if enabled and converged else None
  cases.append({"state":state,"converged":converged,
   "selected_element_enabled":enabled,"bus_voltage":volt,
   "terminal_currents":currents,"thermal_rating_verified":False,
   "energized_reachability_verified":False,
   "protection_zone_change_verified":False,
   "restoration_feasible":False})
 data={"status":"MODEL_SWITCH_SENSITIVITY_ONLY","upstream_commit":PIN,
  "dss_python_expected":"0.15.7","source_hashes":source_hashes(root),
  "switch_candidates":[{"element":r["name"],"buses":r["buses"],
    "enabled":r["enabled"],"open_conductors":r["open_conductors"]}
     for r in switches],"selected_switch":selected["name"],
  "transformers":transformers,"cases":cases,
  "transformer_phase_transfer_verified":False,
  "source_phase_reachability_verified":False,
  "thermal_constraints_verified":False,"signed_ct_direction_verified":False,
  "installed_protection_verified":False,"operational_switching_authorized":False,
  "restoration_safety_certificates":0,
  "limitations":"Named-switch outage sensitivity, not a restoration switching plan. No independent transformer winding transfer, CT orientation, thermal rating or relay protection zones."}
 output.parent.mkdir(parents=True,exist_ok=True)
 output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"switch":selected["name"],"switch_candidates":len(switches),
  "transformers":len(transformers),
  "cases":[{"state":x["state"],"converged":x["converged"],
   "bus60":x["bus_voltage"]["60"]["voltage_pu"],
   "bus83":x["bus_voltage"]["83"]["voltage_pu"]} for x in cases],
  "restoration_safety_certificates":0}))
 return data

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--feeder",required=True);p.add_argument("--output",required=True)
 a=p.parse_args();analyze(a.feeder,a.output)
