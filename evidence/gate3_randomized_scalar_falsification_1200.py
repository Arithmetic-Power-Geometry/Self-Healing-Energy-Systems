"""Reproducible randomized scalar certificate falsification (not EMT)."""
import json,math,random
from scipy.integrate import solve_ivp
SEED=20261022
def check(p):
 lo=p['p0'];hi=lo+p['clp'];v=1-p['r']*hi
 if v<=0 or v<p['v_floor'] or hi/v>p['imax']:return False
 def net(x):return min(p['pref'],p['imax']*(1-p['r']*x))-x
 U=max(abs(net(lo)),abs(net(hi)))
 return max(abs(p['f0']),U/p['d'])<=p['fmax'] and min(p['ifault'],p['imax'])>=p['pickup'] and p['trip_delay']<=p['trip_deadline']
def simulate(p):
 def rhs(t,y):
  L=p['p0']+p['clp']*math.exp(-t/p['tau'])
  return [(min(p['pref'],p['imax']*max(0,1-p['r']*L))-L-p['d']*y[0])/p['m']]
 s=solve_ivp(rhs,(0,5),[p['f0']],rtol=2e-10,atol=2e-12,max_step=.025,dense_output=True)
 peak=max(abs(float(s.sol(i*.01)[0])) for i in range(501))
 hi=p['p0']+p['clp'];v=1-p['r']*hi
 return bool(s.success and peak<=p['fmax']+1e-8 and v>=p['v_floor'] and hi/v<=p['imax'] and min(p['ifault'],p['imax'])>=p['pickup'] and p['trip_delay']<=p['trip_deadline']),peak
def main():
 rng=random.Random(SEED)
 counts=dict(seed=SEED,cases=0,certified=0,numerically_safe=0,unsafe_acceptances=0,conservative_rejections=0,max_certified_peak_ratio=0.0)
 for _ in range(1200):
  p=dict(p0=rng.uniform(.2,.7),clp=rng.uniform(0,.45),r=rng.uniform(.03,.25),pref=rng.uniform(.4,1.2),imax=rng.uniform(.65,1.6),f0=rng.uniform(-.07,.07),d=rng.uniform(.7,4),m=rng.uniform(.4,2.),tau=rng.uniform(.08,1.8),fmax=rng.uniform(.06,.28),v_floor=rng.uniform(.65,.92),ifault=rng.uniform(.5,1.6),pickup=rng.uniform(.5,1.4),trip_delay=rng.uniform(.02,.3),trip_deadline=rng.uniform(.05,.25))
  a=check(p);b,peak=simulate(p)
  counts['cases']+=1;counts['certified']+=int(a);counts['numerically_safe']+=int(b);counts['unsafe_acceptances']+=int(a and not b);counts['conservative_rejections']+=int(b and not a)
  if a:counts['max_certified_peak_ratio']=max(counts['max_certified_peak_ratio'],peak/p['fmax'])
  if a and not b:raise AssertionError('counterexample: '+json.dumps(p))
 print(json.dumps(counts,sort_keys=True))
if __name__=='__main__':main()
