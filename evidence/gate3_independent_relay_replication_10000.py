"""Reproducible synthetic three-location independent relay-uncertainty falsification."""
import random,math,json
rng=random.Random(20261022)
def trip(i,p,s):
 q=i/p
 return math.inf if q<=1 else .14*s/(q**.02-1)
def test(loc,pp,pb,sp,sb,margin,dp,db,fp,fb,tdp,tdb):
 for ip,ib in loc:
  a=trip(fp*ip,pp,sp)+tdp;b=trip(fb*ib,pb,sb)+tdb
  if not(math.isfinite(a) and math.isfinite(b) and a<=dp and b<=db and b-a>=margin):return False
 return True
n=10000
out=dict(total=n,nominal=0,common_derating=0,box_certificate=0,nominal_unsafe=0,common_unsafe=0,box_unsafe=0)
for k in range(n):
 pp=rng.uniform(.5,1.3);pb=rng.uniform(.5,1.3);sp=rng.uniform(.025,.12);sb=rng.uniform(.09,.38)
 margin=rng.uniform(.12,.30);dp=rng.uniform(.4,1.6);db=rng.uniform(1.5,4)
 loc=[(rng.uniform(1.3,3.8),rng.uniform(1.2,3.8)) for _ in range(3)]
 args=(loc,pp,pb,sp,sb,margin,dp,db)
 nom=test(*args,1,1,0,0);common=test(*args,.7,.7,.04,.04)
 box=test(*args,.7,1,.04,0) and all(math.isfinite(trip(.7*ib,pb,sb)) and trip(.7*ib,pb,sb)+.04<=db for _,ib in loc)
 corners=[(fp,fb,ta,tb) for fp in (.7,1) for fb in (.7,1) for ta in (0,.04) for tb in (0,.04)]
 actual=all(test(*args,*c) for c in corners)
 out['nominal']+=nom;out['common_derating']+=common;out['box_certificate']+=box
 out['nominal_unsafe']+=nom and not actual;out['common_unsafe']+=common and not actual;out['box_unsafe']+=box and not actual
print(json.dumps(out,indent=2))
