"""Synthetic inverse-time relay pair stress test. No physical relay model."""
import random,math,json
rng=random.Random(20261022)
N=20000
counts={'cases':N,'nominal_approved':0,'robust_approved':0,'nominal_unsafe':0,'robust_unsafe':0,'coordination_failures_nominal':0}
examples=[]
def trip(I,pickup,tds):
 m=I/pickup
 return math.inf if m<=1 else tds*.14/(m**.02-1)
for i in range(N):
 Ip=rng.uniform(1.2,4.0);Ib=rng.uniform(1.2,4.0)
 pp=rng.uniform(.5,1.3);pb=rng.uniform(.5,1.3)
 sp=rng.uniform(.03,.2);sb=rng.uniform(.08,.5)
 margin=rng.uniform(.1,.35);deadline=rng.uniform(.2,2.)
 tn=trip(Ip,pp,sp);bn=trip(Ib,pb,sb)
 ta=trip(.7*Ip,pp,sp)+.04;ba=trip(.7*Ib,pb,sb)+.04
 nominal=tn<=deadline and bn-tn>=margin
 robust=ta<=deadline and ba-ta>=margin
 counts['nominal_approved']+=int(nominal)
 counts['robust_approved']+=int(robust)
 counts['nominal_unsafe']+=int(nominal and not robust)
 counts['robust_unsafe']+=0
 counts['coordination_failures_nominal']+=int(nominal and ba-ta<margin)
 if nominal and not robust and len(examples)<3:
  examples.append({'case':i,'primary_nominal':tn,'backup_nominal':bn,'primary_derated':ta,'backup_derated':ba,'deadline':deadline,'margin':margin})
print(json.dumps({'counts':counts,'examples':examples},indent=2))
