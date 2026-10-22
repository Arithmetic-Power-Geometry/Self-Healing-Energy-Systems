"""Closed-form frequency envelope for a scalar CLPU surrogate; no feeder/EMT claims."""
import itertools, json

def check(p):
    hi=p['p0']+p['clp'];vm=1-p['r']*hi
    if vm<=0 or vm<p['v_floor'] or hi/vm>p['imax']:return False
    low_p=min(p['pref'],p['imax']*vm)
    high_p=min(p['pref'],p['imax']*(1-p['r']*p['p0']))
    U=max(abs(low_p-hi),abs(high_p-p['p0']))
    if max(abs(p['f0']),U/p['d'])>p['fmax']:return False
    return min(p['ifault'],p['imax'])>=p['pickup'] and p['trip_delay']<=p['trip_deadline']

def main():
    base=dict(pref=.65,p0=.5,clp=.2,tau=.4,r=.12,imax=1.2,f0=0.,d=2.,m=1.,fmax=.18,v_floor=.85,ifault=1.1,pickup=.8,trip_delay=.1,trip_deadline=.15)
    dims=[('clp',(.05,.2,.4)),('imax',(.7,1.,1.4)),('pickup',(.6,1.,1.3)),('trip_delay',(.08,.2)),('fmax',(.12,.25)),('tau',(.15,.4,1.2)),('d',(1.2,3.)),('r',(.08,.18)),('m',(.7,1.3))]
    count=0;accepted=0;by_tau={str(t):0 for t in (.15,.4,1.2)}
    for values in itertools.product(*(vs for _,vs in dims)):
        p={**base,**dict(zip((name for name,_ in dims),values))};ok=check(p)
        count+=1;accepted+=ok;by_tau[str(p['tau'])]+=ok
    print(json.dumps({'total':count,'analytically_enclosed':accepted,'by_tau':by_tau,'scope':'scalar ODE only'},sort_keys=True))
if __name__=='__main__':main()
