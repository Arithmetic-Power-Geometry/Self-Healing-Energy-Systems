"""Probe full element graph, energized bus voltages, and fault-case terminal currents."""
import argparse,json,pathlib,math
from shes.feeder_topology import collect_elements,graph_from_elements,candidate_boundaries
from shes.terminal_current_model import terminal_currents,uncertainty_envelope
from shes.run_ieee123_fault_probes import cmd,source_hashes,PIN
def run(root,output):
 root=root.resolve();output=output.resolve()
 output.parent.mkdir(parents=True,exist_ok=True);output.unlink(missing_ok=True)
 from dss import DSS
 d=DSS.NewContext();master=root/"IEEE123Master.dss"
 cmd(d,f'compile "{master}"')
 elements=collect_elements(d)
 graph=graph_from_elements(elements)
 # Source bus is derived from the first Vsource terminal, not assumed to be 150.
 source_elements=[n for n in d.ActiveCircuit.AllElementNames if n.lower().startswith("vsource.")]
 if not source_elements:raise RuntimeError("missing voltage source")
 d.ActiveCircuit.SetActiveElement(source_elements[0])
 source=d.ActiveCircuit.ActiveCktElement.BusNames[0].split(".")[0].lower()
 paths=candidate_boundaries(graph,source,["150","60","83"])
 results=[]
 for bus in ("150","60","83"):
  for resistance in (.01,.1,1.):
   cmd(d,f'compile "{master}"')
   cmd(d,"set mode=snapshot");cmd(d,"set controlmode=off")
   cmd(d,f"new Fault.shes_p8 phases=1 bus1={bus}.1 r={resistance}")
   cmd(d,"solve")
   if not d.ActiveCircuit.Solution.Converged:raise RuntimeError(f"failed solve {bus} {resistance}")
   d.ActiveCircuit.SetActiveBus(bus)
   voltage_nodes=list(map(int,d.ActiveCircuit.ActiveBus.Nodes))
   voltage_pu=list(map(float,d.ActiveCircuit.ActiveBus.puVmagAngle))[::2]
   if not voltage_pu or any(not math.isfinite(v) for v in voltage_pu):
    raise ValueError("nonfinite bus voltage")
   path=paths[bus]["path"]
   terminals={}
   if path:
    # These are element terminal currents, NOT proven relay measurements.
    for role,edge in (("primary",path[-1]),("backup",path[-2] if len(path)>1 else None)):
     if edge:terminals[role]={"element":edge["element"],
       "currents":terminal_currents(d,edge["element"])}
   results.append({"bus":bus,"fault_resistance_ohm":resistance,
    "fault_phase":1,"bus_nodes":voltage_nodes,"bus_voltage_pu":voltage_pu,
    "candidate_terminal_currents":terminals,"converged":True})
 data={"status":"PASS_TOPOLOGY_AND_TERMINAL_PROBES_ONLY","pin":PIN,
  "sha256":source_hashes(root),"source_bus":source,
  "element_count":len(elements),"element_kinds":{k:sum(e["kind"]==k for e in elements)
     for k in sorted({e["kind"] for e in elements})},
  "candidate_paths":paths,"results":results,
  "hypothetical_uncertainty":uncertainty_envelope(100.,80.),
  "installed_protection_verified":False,"relay_coordination_validated":False,
  "restoration_safe":False,"inverter_fault_current_validated":False,
  "notes":"Connectivity is element adjacency only; phases, switch openness, regulator behavior and energized connectivity require separate checks."}
 output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"source":source,"elements":data["element_kinds"],
  "paths":{k:{"reachable":v["reachable_in_element_graph"],
  "primary":v["candidate_primary_element"],"backup":v["candidate_backup_element"]}
  for k,v in paths.items()},"cases":len(results)}))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--feeder",type=pathlib.Path,required=True)
 p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 run(a.feeder,a.output)
