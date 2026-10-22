import random, math, json
rng=random.Random(20261022)
N=20000
counts={k:0 for k in ['nominal_approved','nominal_false_approvals','robust_approved','robust_false_approvals','nominal_infinite_backup','nominal_coordination_failure','nominal_deadline_failure']}
examples=[]
def trip(I,pickup,tds):
 m=I/pickup
 return math.inf if m<=1 else tds*.14/(m**.02-1)
for k in range(N):
 Ip=rng.uniform(1.2,4);Ib=rng.uniform(1.2,4);pp=rng.uniform(.5,1.3);pb=rng.uniform(.5,1.3)
 sp=rng.uniform(.03,.2);sb=rng.uniform(.08,.5);margin=rng.uniform(.1,.35);deadline=rng.uniform(.2,2);backup_deadline=rng.uniform(1.0,5.0)
 tn=trip(Ip,pp,sp);bn=trip(Ib,pb,sb)
 ta=trip(.7*Ip,pp,sp)+.04;ba=trip(.7*Ib,pb,sb)+.04
 def ok(t,b):return math.isfinite(t) and math.isfinite(b) and t<=deadline and b<=backup_deadline and b-t>=margin
 nominal=ok(tn,bn);robust=ok(ta,ba)
 counts['nominal_approved']+=nominal;counts['robust_approved']+=robust
 counts['nominal_false_approvals']+=nominal and not robust
 counts['robust_false_approvals']+=robust and not ok(ta,ba)
 counts['nominal_infinite_backup']+=math.isfinite(tn) and not math.isfinite(bn) and tn<=deadline and bn-tn>=margin
 counts['nominal_coordination_failure']+=nominal and ba-ta<margin
 counts['nominal_deadline_failure']+=nominal and ta>deadline
 if nominal and not robust and len(examples)<3:examples.append(dict(case=k,primary_nominal=tn,backup_nominal=bn,primary_derated=ta,backup_derated=ba,margin=margin,deadline=deadline,backup_deadline=backup_deadline))
print(json.dumps(dict(cases=N,counts=counts,examples=examples),indent=2))
