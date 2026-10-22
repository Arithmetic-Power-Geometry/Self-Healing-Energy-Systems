"""Three-location synthetic relay coordination stress test; not an electrical feeder solve."""
import random,math,json
rng=random.Random(20261022)
def t(i,p,s):
 q=i/p
 return float('inf') if q<=1 else s*.14/(q**.02-1)
N=12000
c=dict(cases=N,nominal_accepted=0,robust_accepted=0,nominal_fail_under_derating=0,robust_fail_under_derating=0)
examples=[]
for k in range(N):
 pp=rng.uniform(.5,1.3);pb=rng.uniform(.5,1.3)
 sp=rng.uniform(.025,.12);sb=rng.uniform(.09,.38)
 margin=rng.uniform(.12,.30);dp=rng.uniform(.4,1.6);db=rng.uniform(1.5,4)
 currents=[(rng.uniform(1.3,3.8),rng.uniform(1.2,3.8)) for _ in range(3)]
 def valid(factor):
  for ip,ib in currents:
   a=t(factor*ip,pp,sp)+.04*(factor<1)
   b=t(factor*ib,pb,sb)+.04*(factor<1)
   if not (math.isfinite(a) and math.isfinite(b) and a<=dp and b<=db and b-a>=margin):
    return False
  return True
 nominal=valid(1.);robust=valid(.7)
 c['nominal_accepted']+=nominal;c['robust_accepted']+=robust
 c['nominal_fail_under_derating']+=nominal and not robust
 c['robust_fail_under_derating']+=robust and not valid(.7)
 if nominal and not robust and len(examples)<2:
  examples.append(dict(case=k,primary_pickup=pp,backup_pickup=pb,currents=currents))
print(json.dumps(dict(counts=c,examples=examples),indent=2))
