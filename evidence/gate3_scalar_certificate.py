#!/usr/bin/env python3
"""Conservative scalar linear surrogate; NOT AC power-flow, EMT, or relay certificate."""
import math
def certify(x0, amin, amax, dmin, dmax, limit):
    assert 0 < amin <= amax and dmin <= dmax and limit > 0
    bound=max(abs(x0),max(abs(dmin),abs(dmax))/amin)
    return bound <= limit,bound
def simulate(x0,a,d,dt=0.0005,T=2.0):
    x=x0;peak=abs(x);n=math.ceil(T/dt);h=T/n;alpha=math.exp(-a*h)
    for _ in range(n):
        x=x*alpha+(d/a)*(1-alpha)
        peak=max(peak,abs(x))
    return peak
def main():
    cases=safe=rejected=false_safe=conservative=0
    for x0 in (-0.7,-0.2,0.0,0.2,0.7):
      for amin,amax in ((0.5,1.0),(1.0,2.0),(2.0,4.0)):
       for dmin,dmax in ((-0.8,0.8),(-0.3,0.3),(0,0.5)):
        for limit in (0.3,0.6,1.0):
         ok,bound=certify(x0,amin,amax,dmin,dmax,limit)
         peak=max(simulate(x0,a,d) for a in (amin,(amin+amax)/2,amax) for d in (dmin,(dmin+dmax)/2,dmax))
         cases+=1
         if ok:safe+=1
         else:rejected+=1
         if ok and peak>limit+1e-9:false_safe+=1
         if not ok and peak<=limit+1e-9:conservative+=1
    assert false_safe==0
    print(f'cases={cases} certified={safe} rejected={rejected} false_safe={false_safe} conservative_on_sample={conservative}')
    print('Only scalar ODE; NOT electrical grid safety.')
if __name__=='__main__':main()
