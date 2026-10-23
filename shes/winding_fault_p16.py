"""P16 pinned electrical evidence: winding metadata and pre/post fault phasors.

A numerical OpenDSS result is not a CT orientation, thermal certificate,
phase-transfer proof, or authorized restoration operation.
"""
import argparse,json,math,pathlib
from shes.run_ieee123_fault_probes import PIN,cmd,source_hashes
from shes.switch_sensitivity_p15 import candidate_switches
from shes.phase_topology_p14 import read_records

def winding_metadata(d):
 c=d.ActiveCircuit;rows=[]
 for name in c.AllElementNames:
  if not name.lower().startswith("transformer."):continue
  c.SetActiveElement(name);e=c.ActiveCktElement
  t=c.Transformers;t.Name=name.split(".",1)[1]
  nw=int(t.NumWindings);windings=[]
  for w in range(1,nw+1):
   t.Wdg=w
   windings.append({"winding":w,"bus":str(e.BusNames[w-1]) if w<=len(e.BusNames) else None,
    "connection_code":int(t.IsDelta),"kv":float(t.kV),"kva":float(t.kVA),
    "tap":float(t.Tap)})
  rows.append({"element":name,"phases":int(e.NumPhases),
   "terminal_buses":list(e.BusNames),"windings":windings,
   "transfer_matrix_verified":False,
   "neutral_grounding_verified":False})
 return rows

def phasors(e):
 nc=int(e.NumConductors);nt=int(e.NumTerminals)
 raw=list(map(float,e.Currents))
 if len(raw)!=2*nc*nt:raise ValueError("complex current size mismatch")
 return [[[raw[2*(t*nc+i)],raw[2*(t*nc+i)+1]] for i in range(nc)]
  for t in range(nt)]

def fault_case(d,master,sw,state,bus,phase,resistance):
 cmd(d,f'compile "{master}"')
 if state=="disabled":cmd(d,f'edit {sw} enabled=no')
 cmd(d,"set mode=snapshot");cmd(d,"set controlmode=off")
 cmd(d,"set maxiterations=100")
 cmd(d,f"new Fault.shes_p16 phases=1 bus1={bus}.{phase} r={resistance}")
 cmd(d,"solve")
 converged=bool(d.ActiveCircuit.Solution.Converged)
 if not converged:return {"state":state,"bus":bus,"phase":phase,"r_ohm":resistance,
  "converged":False,"electrically_interpretable":False}
 d.ActiveCircuit.SetActiveElement("Fault.shes_p16")
 fault=phasors(d.ActiveCircuit.ActiveCktElement)
 currents={}
 for element in ("Line.l58","Line.l55","Line.l84","Line.l82"):
  d.ActiveCircuit.SetActiveElement(element)
  e=d.ActiveCircuit.ActiveCktElement
  currents[element]={"enabled":bool(e.Enabled),"terminal_buses":list(e.BusNames),
   "num_conductors":int(e.NumConductors),
   "complex_terminal_currents_a":phasors(e)}
 d.ActiveCircuit.SetActiveBus(bus)
 b=d.ActiveCircuit.ActiveBus
 node_voltage={str(n):v for n,v in zip(b.Nodes,list(map(float,b.puVmagAngle))[::2])}
 v=float(node_voltage.get(str(phase),0.))
 return {"state":state,"bus":bus,"phase":phase,"r_ohm":resistance,
  "converged":True,"fault_element_terminal_currents_a":fault,
  "fault_bus_phase_voltage_pu":v,
  "electrically_interpretable":v>1e-6,
  "candidate_terminal_currents":currents,
  "ct_polarity_verified":False,"relay_zone_verified":False}

def run(root,output):
 from dss import DSS
 root=pathlib.Path(root).resolve();output=pathlib.Path(output).resolve()
 d=DSS.NewContext();master=root/"IEEE123Master.dss"
 cmd(d,f'compile "{master}"')
 records=read_records(d);switches=candidate_switches(records)
 if not switches:raise ValueError("no named switches")
 sw=switches[0]["name"];windings=winding_metadata(d)
 cases=[]
 for state in ("published","disabled"):
  for bus in ("60","83"):
   cases.append(fault_case(d,master,sw,state,bus,1,.1))
 data={"status":"MODEL_ONLY_P16","upstream_commit":PIN,"dss_python_expected":"0.15.7",
  "source_hashes":source_hashes(root),"switch":sw,
  "winding_metadata":windings,"cases":cases,
  "transformer_transfer_verified":False,"neutral_grounding_verified":False,
  "phase_source_reachability_verified":False,
  "thermal_constraints_verified":False,"installed_ct_polarity_verified":False,
  "installed_protection_zones_verified":False,
  "switching_operationally_authorized":False,"physical_restoration_certificates":0,
  "limitations":"Winding connections and taps extracted from OpenDSS; no validated conductor transfer matrix, grounding impedance, source-reachable phase graph, thermal rating, relay settings or CT polarity. Complex currents follow simulator terminal-into-element convention."}
 output.parent.mkdir(parents=True,exist_ok=True)
 output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"switch":sw,"transformers":len(windings),
  "fault_cases":[{"state":c["state"],"bus":c["bus"],"converged":c["converged"],
    "fault_bus_voltage_pu":c.get("fault_bus_phase_voltage_pu"),
    "interpretable":c["electrically_interpretable"]} for c in cases],
  "physical_restoration_certificates":0}))
 return data

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--feeder",required=True);p.add_argument("--output",required=True)
 a=p.parse_args();run(a.feeder,a.output)
