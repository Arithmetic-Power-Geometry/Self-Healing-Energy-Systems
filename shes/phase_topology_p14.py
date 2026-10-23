"""P14: fail-closed phase/conductor topology audit of pinned IEEE123.

Line conductor numbers are only a connectivity proxy; transformer/regulator
winding transfer, CT polarity and energized status require separate evidence.
"""
import argparse,collections,json,pathlib,sys
from shes.run_ieee123_fault_probes import PIN,cmd,source_hashes
from shes.feeder_topology import graph_from_elements,shortest_path

def split_bus(bus):
 a=str(bus).lower().split(".")
 return a[0],tuple(int(x) for x in a[1:] if x.isdigit())

def line_edges(records):
 graph=collections.defaultdict(list)
 for e in records:
  if e["kind"]!="line" or not e["enabled"]:continue
  if len(e["buses"])!=2:continue
  (a,an),(b,bn)=map(split_bus,e["buses"])
  # Fail closed if conductor positions cannot be mapped unambiguously.
  if not an or len(an)!=len(bn) or len(set(an))!=len(an) or len(set(bn))!=len(bn):continue
  for x,y in zip(an,bn):
   if x not in (1,2,3) or y not in (1,2,3):continue
   if [1,x] in e["open_conductors"] or [2,y] in e["open_conductors"]:continue
   graph[(a,x)].append(((b,y),e["name"]))
   graph[(b,y)].append(((a,x),e["name"]))
 return graph

def reach(graph,starts):
 q=collections.deque(starts);prev={x:None for x in starts}
 while q:
  u=q.popleft()
  for v,element in graph.get(u,()):
   if v not in prev:prev[v]=(u,element);q.append(v)
 return prev

def read_records(d):
 c=d.ActiveCircuit;out=[]
 for name in list(c.AllElementNames):
  if not name.lower().startswith(("line.","transformer.")):continue
  c.SetActiveElement(name);e=c.ActiveCktElement
  buses=list(e.BusNames)
  if len(buses)!=2:continue
  open_conductors=[]
  for terminal in (1,2):
   for conductor in range(1,int(e.NumConductors)+1):
    if bool(e.IsOpen(terminal,conductor)):open_conductors.append([terminal,conductor])
  out.append({"name":name,"kind":name.split(".")[0].lower(),
    "enabled":bool(e.Enabled),"buses":buses,
    "num_phases":int(e.NumPhases),"num_conductors":int(e.NumConductors),
    "open_conductors":open_conductors,
    "winding_transfer_verified":False if name.lower().startswith("transformer.") else None})
 return out

def audit_records(records,source="150",targets=("60","83")):
 graph=line_edges(records);prev=reach(graph,[(source,p) for p in (1,2,3)])
 all_edges=graph_from_elements([{"name":r["name"],"kind":r["kind"],
   "buses":r["buses"],"enabled":r["enabled"] and not bool(r["open_conductors"])}
   for r in records])
 candidates={}
 for target in targets:
  path=shortest_path(all_edges,source,target)
  candidates[target]={"element_adjacency_path":path,
   "element_adjacency_reachable":path is not None,
   "line_only_phase_nodes_reached":[p for p in (1,2,3) if (target,p) in prev],
   "phase_energization_verified":False,
   "transformer_transfer_verified":False,
   "installed_relay_and_ct_orientation_verified":False,
   "candidate_primary":path[-1]["element"] if path else None,
   "candidate_backup":path[-2]["element"] if path and len(path)>1 else None}
 return candidates

def run(root,output):
 from dss import DSS
 root=pathlib.Path(root).resolve()
 d=DSS.NewContext();cmd(d,f'compile "{root/"IEEE123Master.dss"}"')
 records=read_records(d)
 source_elements=[n for n in d.ActiveCircuit.AllElementNames if n.lower().startswith("vsource.")]
 if not source_elements:raise RuntimeError("no source")
 d.ActiveCircuit.SetActiveElement(source_elements[0])
 source=split_bus(d.ActiveCircuit.ActiveCktElement.BusNames[0])[0]
 paths=audit_records(records,source)
 data={"status":"PASS_CONSERVATIVE_PHASE_TOPOLOGY_AUDIT_ONLY",
  "upstream_commit":PIN,"dss_python_expected":"0.15.7",
  "feeder_sha256":source_hashes(root),"source_bus":source,
  "element_records":records,"targets":paths,
  "transformer_winding_transfer_resolved":False,
  "switching_feasibility_verified":False,
  "phase_energization_verified":False,
  "relay_or_ct_orientation_verified":False,
  "physical_protection_certificates":0,
  "limitations":"Conductor-index line graph is conservative; transformer winding transfers are deliberately not inferred. OpenDSS node indices are not CT polarity or protection zones. No voltage-based energized claim."}
 output=pathlib.Path(output);output.parent.mkdir(parents=True,exist_ok=True)
 output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"elements":len(records),"transformers":sum(r["kind"]=="transformer" for r in records),
  "open_conductor_elements":sum(bool(r["open_conductors"]) for r in records),
  "targets":{k:{"adjacency":v["element_adjacency_reachable"],
   "line_only_phases":v["line_only_phase_nodes_reached"],
   "primary":v["candidate_primary"],"backup":v["candidate_backup"]} for k,v in paths.items()},
  "physical_protection_certificates":0},sort_keys=True))
 return data

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--feeder",required=True);p.add_argument("--output",required=True)
 a=p.parse_args();run(a.feeder,a.output)
