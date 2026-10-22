"""Deterministic endpoint-bound adversarial property test for scalar surrogate."""
import math,random,json
rng=random.Random(20261022)
n=5000
out={'tested':n,'endpoint_bound_violations':0,'voltage_order_violations':0,'invalid_assumptions':0,'max_gap':0.0}
for _ in range(n):
 p0=rng.uniform(.1,.8);clp=rng.uniform(0,.6);r=rng.uniform(.01,.4);pref=rng.uniform(.2,1.5);imax=rng.uniform(.4,2.)
 lo=p0;hi=p0+clp
 if 1-r*hi<=0:
  out['invalid_assumptions']+=1;continue
 def g(L):return min(pref,imax*(1-r*L))-L
 bound=max(abs(g(lo)),abs(g(hi)))
 for j in range(51):
  L=lo+(hi-lo)*j/50
  gap=abs(g(L))-bound
  out['max_gap']=max(out['max_gap'],gap)
  if gap>1e-12:out['endpoint_bound_violations']+=1
  if not (1-r*hi-1e-12<=1-r*L<=1-r*lo+1e-12):out['voltage_order_violations']+=1
print(json.dumps(out,sort_keys=True))
