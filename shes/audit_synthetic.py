"""Reproduce source experiments and audit acceptance sets. Python 3.11, stdlib only."""
import json, subprocess, sys, pathlib, math, random
ROOT=pathlib.Path(__file__).resolve().parents[1]
SCRIPTS={
 "independent":"gate3_independent_relay_uncertainty_20000.py",
 "interrupted":"gate3_interrupted_pickup_20000.py",
 "finite":"gate3_finite_backup_trip_20000.py",
 "scalar":"gate3_scalar_analytic_envelope_2592.py",
 "inverse":"gate3_inverse_time_relay_20000.py",
 "pickup":"gate3_relay_uncertainty_10000.py",
}
def execute(name):
 p=subprocess.run([sys.executable,str(ROOT/"evidence"/SCRIPTS[name])],
  cwd=ROOT,capture_output=True,text=True,check=True,timeout=120)
 return json.loads(p.stdout)
def original_checks(results):
 a=results["independent"]["counts"]
 assert (a["total"],a["nominal"],a["nominal_fails_any"],a["endpoint_robust"],
  a["endpoint_fails_any"],a["box_robust"],a["box_robust_fails_any"]) == (
  20000,5796,4739,1533,476,1057,0)
 b=results["interrupted"]["counts"]
 assert (b["cases"],b["static_approved"],b["static_false_approvals"],
 b["dynamic_approved"],b["dynamic_false_approvals"])==(20000,19135,6457,12678,0)
 c=results["finite"]["counts"]
 assert (c["nominal_approved"],c["nominal_false_approvals"],
 c["robust_approved"],c["robust_false_approvals"])==(6634,3530,3233,0)
 assert results["scalar"]["total"]==2592
 return {"finite_contingency":{"both":c["nominal_approved"]-c["nominal_false_approvals"],
  "nominal_only":c["nominal_false_approvals"],
  "robust_only":c["robust_approved"]-(c["nominal_approved"]-c["nominal_false_approvals"]),
  "neither":20000-c["nominal_approved"]-c["robust_approved"]+
   (c["nominal_approved"]-c["nominal_false_approvals"])}}
def trip(I,p,s):
 q=I/p
 return math.inf if q<=1 else .14*s/(q**.02-1)
def feasible(ip,ib,pp,pb,sp,sb,dp,db,margin,gp,gb,tp,tb):
 p=trip(ip*gp,pp,sp)+tp
 b=trip(ib*gb,pb,sb)+tb
 return all(map(math.isfinite,(p,b))) and p<=dp and b<=db and b-p>=margin
def comparative(seed=20261023,n=5000,gmin=.7,delay=.04):
 """One common population: nominal, common, box; oracle enumerates independent corners."""
 rng=random.Random(seed)
 labels=("nominal","common","box")
 matrix={label:{"approved":0,"false_approval":0,"rejected_safe":0,"true_approval":0}
         for label in labels}
 for _ in range(n):
  pp,pb=rng.uniform(.5,1.3),rng.uniform(.5,1.3)
  sp,sb=rng.uniform(.025,.12),rng.uniform(.09,.38)
  margin=rng.uniform(.12,.30)
  dp,db=rng.uniform(.4,1.6),rng.uniform(1.5,4)
  loc=[(rng.uniform(1.3,3.8),rng.uniform(1.2,3.8)) for _ in range(3)]
  def allfault(gp,gb,tp,tb):
   return all(feasible(ip,ib,pp,pb,sp,sb,dp,db,margin,gp,gb,tp,tb) for ip,ib in loc)
  nominal=allfault(1.,1.,0.,0.)
  common=allfault(gmin,gmin,delay,delay)
  # Explicit independent-box extrema for each fault; include backup deadline separately.
  box=allfault(gmin,1.,delay,0.) and all(
   math.isfinite(trip(ib*gmin,pb,sb)) and trip(ib*gmin,pb,sb)+delay<=db for _,ib in loc)
  oracle=all(allfault(gp,gb,tp,tb) for gp in (gmin,1.) for gb in (gmin,1.)
     for tp in (0.,delay) for tb in (0.,delay))
  assert box==oracle, "box endpoint theorem mismatch"
  for label,accepted in zip(labels,(nominal,common,box)):
   row=matrix[label]
   row["approved"]+=accepted
   row["false_approval"]+=accepted and not oracle
   row["true_approval"]+=accepted and oracle
   row["rejected_safe"]+=(not accepted) and oracle
 return {"seed":seed,"cases":n,"gmin":gmin,"delay":delay,"oracle_safe":matrix["box"]["true_approval"],
  "screens":matrix}
def main():
 r={name:execute(name) for name in SCRIPTS}
 c=original_checks(r)
 comparisons=[comparative(gmin=g) for g in (.6,.7,.8)]
 output={"original_counts":{k:v.get("counts",v) for k,v in r.items()},
 "finite_contingency":c["finite_contingency"],"independent_corner_comparison":comparisons,
 "notes":["Synthetic model-relative outcomes only; no field reliability estimate.",
 "Box approval equals enumerated independent corners by monotonicity; zero false approvals is not independent validation.",
 "Different source experiments have different populations and cannot be pooled.",
 "The earlier inverse-time script sets robust_unsafe += 0 unconditionally; its zero is not an independently computed validation."]}
 print(json.dumps(output,indent=2,sort_keys=True))
if __name__=="__main__":main()
