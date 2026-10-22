import random,math,json
from scipy.integrate import solve_ivp
rng=random.Random(20261022)
out=dict(total=2000,nominal_accepted=0,robust_accepted=0,nominal_unsafe=0,robust_unsafe=0,robust_conservative_vs_actual=0)
for i in range(2000):
 p0=rng.uniform(.2,.65);clp=rng.uniform(.02,.4);r=rng.uniform(.04,.19);pref=rng.uniform(.45,1.1);imax=rng.uniform(.7,1.5);d=rng.uniform(1.,3.5);m=rng.uniform(.5,1.6);fmax=rng.uniform(.06,.22);tau=rng.uniform(.12,.9)
 hi=p0+clp;vm=1-r*hi
 if vm<.7 or hi/vm>imax:continue
 def P(L):return min(pref,imax*(1-r*L))
 def net(L,a):return a*P(L)-L
 nominal=max(abs(net(p0,1)),abs(net(hi,1)))/d<=fmax
 robust=max(abs(net(hi,.8)),abs(net(p0,1)))/d<=fmax
 def rhs(t,y):
  L=p0+clp*math.exp(-t/tau)
  return [(.8*P(L)-L-d*y[0])/m]
 sol=solve_ivp(rhs,(0,5),[0],rtol=1e-9,atol=1e-11,max_step=.04)
 safe=max(abs(x) for x in sol.y[0])<=fmax+1e-8
 out['nominal_accepted']+=nominal;out['robust_accepted']+=robust
 out['nominal_unsafe']+=nominal and not safe;out['robust_unsafe']+=robust and not safe
 out['robust_conservative_vs_actual']+=safe and not robust
print(json.dumps({k:int(v) for k,v in out.items()},sort_keys=True))
