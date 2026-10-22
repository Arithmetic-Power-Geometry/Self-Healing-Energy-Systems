"""Three-fault-location relay uncertainty: independently varying primary/backup currents."""
import random,math,json
rng=random.Random(20261022)
def trip(i,p,s):
 q=i/p
 return math.inf if q<=1 else .14*s/(q**.02-1)
def valid(loc,pp,pb,sp,sb,margin,dp,db,fp,fb,tdp,tdb):
 for ip,ib in loc:
  a=trip(ip*fp,pp,sp)+tdp;b=trip(ib*fb,pb,sb)+tdb
  if not(math.isfinite(a) and math.isfinite(b) and a<=dp and b<=db and b-a>=margin):return False
 return True
out=dict(total=20000,nominal=0,endpoint_robust=0,nominal_fails_any=0,endpoint_fails_any=0,box_robust=0,box_robust_fails_any=0)
counterexamples=[]
for k in range(out['total']):
 pp=rng.uniform(.5,1.3);pb=rng.uniform(.5,1.3);sp=rng.uniform(.025,.12);sb=rng.uniform(.09,.38);margin=rng.uniform(.12,.30);dp=rng.uniform(.4,1.6);db=rng.uniform(1.5,4)
 loc=[(rng.uniform(1.3,3.8),rng.uniform(1.2,3.8)) for _ in range(3)]
 nominal=valid(loc,pp,pb,sp,sb,margin,dp,db,1,1,0,0)
 common=valid(loc,pp,pb,sp,sb,margin,dp,db,.7,.7,.04,.04)
 scenarios=[(fp,fb,ta,tb) for fp in (.7,.85,1.) for fb in (.7,.85,1.) for ta in (0.,.04) for tb in (0.,.04)]
 actual=all(valid(loc,pp,pb,sp,sb,margin,dp,db,*s) for s in scenarios)
 # Worst primary time (70%, +40ms) versus fastest backup (100%, +0ms).
 # Independently require slowest backup (70%, +40ms) to clear before deadline.
 box=valid(loc,pp,pb,sp,sb,margin,dp,db,.7,1.,.04,0.)
 box=box and all(math.isfinite(trip(ib*.7,pb,sb)) and trip(ib*.7,pb,sb)+.04<=db for _,ib in loc)
 out['nominal']+=nominal;out['endpoint_robust']+=common;out['nominal_fails_any']+=nominal and not actual
 out['endpoint_fails_any']+=common and not actual;out['box_robust']+=box;out['box_robust_fails_any']+=box and not actual
 if common and not actual and len(counterexamples)<3:counterexamples.append({'index':k,'fault_currents':loc,'primary_pickup':pp,'backup_pickup':pb,'primary_tds':sp,'backup_tds':sb,'margin':margin,'primary_deadline':dp,'backup_deadline':db})
print(json.dumps({'counts':out,'counterexamples':counterexamples},indent=2))
