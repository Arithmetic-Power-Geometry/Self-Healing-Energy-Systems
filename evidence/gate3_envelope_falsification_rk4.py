"""Independent fixed-step RK4 cross-check of scalar frequency envelope. Not EMT."""
import itertools,json,math
from gate3_scalar_analytic_envelope_2592 import check

def rk4_safe(p):
 def rhs(t,f):
  load=p['p0']+p['clp']*math.exp(-t/p['tau'])
  v=1-p['r']*load
  return (min(p['pref'],p['imax']*max(0,v))-load-p['d']*f)/p['m']
 f=p['f0'];peak=abs(f);h=.01
 for j in range(300):
  t=j*h
  a=rhs(t,f);b=rhs(t+h/2,f+h*a/2);c=rhs(t+h/2,f+h*b/2);d=rhs(t+h,f+h*c)
  f+=h*(a+2*b+2*c+d)/6;peak=max(peak,abs(f))
 hi=p['p0']+p['clp'];vm=1-p['r']*hi
 return peak<=p['fmax']+1e-9 and vm>=p['v_floor'] and hi/vm<=p['imax'] and min(p['ifault'],p['imax'])>=p['pickup'] and p['trip_delay']<=p['trip_deadline']
def main():
 base=dict(pref=.65,p0=.5,clp=.2,tau=.4,r=.12,imax=1.2,f0=0.,d=2.,m=1.,fmax=.18,v_floor=.85,ifault=1.1,pickup=.8,trip_delay=.1,trip_deadline=.15)
 dims=[('clp',(.05,.2,.4)),('imax',(.7,1.,1.4)),('pickup',(.6,1.,1.3)),('trip_delay',(.08,.2)),('fmax',(.12,.25)),('tau',(.15,.4,1.2)),('d',(1.2,3.)),('r',(.08,.18)),('m',(.7,1.3))]
 out=dict(total=0,refined=0,rk4_safe=0,refined_unsafe=0,conservative=0)
 for vals in itertools.product(*(v for _,v in dims)):
  p={**base,**dict(zip((n for n,_ in dims),vals))}
  a=check(p);b=rk4_safe(p)
  out['total']+=1;out['refined']+=a;out['rk4_safe']+=b;out['refined_unsafe']+=a and not b;out['conservative']+=b and not a
 print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
