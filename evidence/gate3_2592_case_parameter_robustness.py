import math,json
from itertools import product
from scipy.integrate import solve_ivp

def cert(p):
 hi=p['p0']+p['clp'];vm=1-p['r']*hi
 if vm<=0 or vm<p['v_floor'] or hi/vm>p['imax']:return False
 lo=min(p['pref'],p['imax']*vm);up=min(p['pref'],p['imax'])
 U=max(abs(lo-hi),abs(up-p['p0']))
 if max(abs(p['f0']),U/p['d'])>p['fmax']:return False
 return min(p['ifault'],p['imax'])>=p['pickup'] and p['trip_delay']<=p['trip_deadline']

def sim(p):
 def rhs(t,y):
  load=p['p0']+p['clp']*math.exp(-t/p['tau']);v=1-p['r']*load
  return [(min(p['pref'],p['imax']*max(0,v))-load-p['d']*y[0])/p['m']]
 sol=solve_ivp(rhs,(0,3),[p['f0']],rtol=1e-9,atol=1e-11,max_step=.02,dense_output=True)
 peak=max(abs(float(sol.sol(i/50)[0])) for i in range(151))
 hi=p['p0']+p['clp'];vm=1-p['r']*hi
 return bool(sol.success and peak<=p['fmax']+1e-8 and vm>=p['v_floor'] and hi/vm<=p['imax'] and min(p['ifault'],p['imax'])>=p['pickup'] and p['trip_delay']<=p['trip_deadline'])
base=dict(pref=.65,p0=.5,clp=.2,tau=.4,r=.12,imax=1.2,f0=0.,d=2.,m=1.,fmax=.18,v_floor=.85,ifault=1.1,pickup=.8,trip_delay=.1,trip_deadline=.15)
counts=dict(total=0,certified=0,baseline_safe=0,false_accept=0,conservative=0)
for clp,imax,pickup,delay,fmax,tau,d,r,m in product((.05,.2,.4),(.7,1.,1.4),(.6,1.,1.3),(.08,.2),(.12,.25),(.15,.4,1.2),(1.2,3.0),(.08,.18),(.7,1.3)):
 p={**base,'clp':clp,'imax':imax,'pickup':pickup,'trip_delay':delay,'fmax':fmax,'tau':tau,'d':d,'r':r,'m':m};c=cert(p);s=sim(p)
 counts['total']+=1;counts['certified']+=int(c);counts['baseline_safe']+=int(s);counts['false_accept']+=int(c and not s);counts['conservative']+=int(s and not c)
print(json.dumps(counts,sort_keys=True))
