"""Candidate upstream protection boundaries from line topology only.

Not a validated relay map: ignores regulators, transformers, open switches,
parallel paths, directional elements and protection equipment.
"""
from collections import defaultdict, deque
def candidate_paths(lines, source, targets):
 graph=defaultdict(list)
 for row in lines:
  u,v=row["from"].lower(),row["to"].lower()
  if not u or not v or u==v:raise ValueError("invalid line endpoint")
  graph[u].append((v,row["name"]))
  graph[v].append((u,row["name"]))
 result={}
 for target in targets:
  t=target.lower();q=deque([(source.lower(),[])])
  visited={source.lower()};paths=[]
  while q:
   node,path=q.popleft()
   if node==t:
    paths.append(path);break
   for nxt,name in sorted(graph[node]):
    if nxt not in visited:
     visited.add(nxt);q.append((nxt,path+[{"line":name,"from":node,"to":nxt}]))
  result[target]={"path":paths[0] if paths else None,
    "candidate_primary_boundary":paths[0][-1]["line"] if paths and paths[0] else None,
    "candidate_backup_boundary":paths[0][-2]["line"] if paths and len(paths[0])>=2 else None,
    "protection_zone_validated":False,"relay_installed_verified":False}
 return result
