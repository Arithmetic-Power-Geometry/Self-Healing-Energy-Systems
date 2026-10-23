"""IEEE123 graph with lines, transformers and regulator windings.
Graph is electrical-element adjacency, NOT a verified protection topology.
"""
from collections import defaultdict, deque
def busname(value):
 return str(value).split(".")[0].strip().lower()
def add_edges(graph,element,kind,terminals,phases=None):
 buses=[busname(x) for x in terminals]
 if any(not x for x in buses):raise ValueError("empty bus")
 for i in range(len(buses)):
  for j in range(i+1,len(buses)):
   if buses[i]==buses[j]:continue
   for u,v in ((buses[i],buses[j]),(buses[j],buses[i])):
    graph[u].append({"to":v,"element":element,"kind":kind,"phases":phases or []})
def graph_from_elements(elements):
 graph=defaultdict(list)
 for e in elements:
  if e.get("enabled",True):
   add_edges(graph,e["name"],e["kind"],e["buses"],e.get("phases"))
 return graph
def shortest_path(graph,source,target):
 q=deque([(source.lower(),[])]);seen={source.lower()}
 while q:
  u,path=q.popleft()
  if u==target.lower():return path
  for edge in sorted(graph[u],key=lambda x:(x["to"],x["element"])):
   v=edge["to"]
   if v not in seen:
    seen.add(v);q.append((v,path+[{"from":u,**edge}]))
 return None
def candidate_boundaries(graph,source,targets):
 out={}
 for target in targets:
  path=shortest_path(graph,source,target)
  out[target]={"reachable_in_element_graph":path is not None,
   "path":path,"candidate_primary_element":path[-1]["element"] if path else None,
   "candidate_backup_element":path[-2]["element"] if path and len(path)>1 else None,
   "installed_relay_verified":False,"protection_zone_validated":False}
 return out
def collect_elements(d):
 c=d.ActiveCircuit
 names=list(c.AllElementNames)
 result=[]
 for name in names:
  low=name.lower()
  if not low.startswith(("line.","transformer.","reactor.")):continue
  c.SetActiveElement(name);elem=c.ActiveCktElement
  if not elem.Enabled:continue
  buses=list(elem.BusNames)
  if len(buses)<2:continue
  result.append({"name":name,"kind":name.split(".")[0].lower(),"buses":buses,
   "enabled":bool(elem.Enabled),"phases":int(elem.NumPhases)})
 return result
