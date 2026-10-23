"""Synthetic definite-time relay with reset on loss of pickup. NOT an inverse-time relay or EMT model."""
import random,json
rng=random.Random(20261023)
N=20000
count={'cases':N,'static_approved':0,'static_false_approvals':0,'dynamic_approved':0,'dynamic_false_approvals':0}
examples=[]
for k in range(N):
    pickup=rng.uniform(.5,1.2)
    high=rng.uniform(1.25,2.0)*pickup
    low=rng.uniform(.3,.95)*pickup
    required=rng.uniform(.03,.15)
    deadline=rng.uniform(.10,.35)
    pulse=min(rng.uniform(.01,.13),deadline)
    gap=rng.uniform(.01,.15)
    recovery=max(0,deadline-pulse-gap)
    static=high>=pickup and required<=deadline
    actual=(pulse>=required) or (recovery>=required)
    dynamic=static and actual
    count['static_approved']+=static
    count['static_false_approvals']+=static and not actual
    count['dynamic_approved']+=dynamic
    count['dynamic_false_approvals']+=dynamic and not actual
    if static and not actual and len(examples)<3:
        examples.append(dict(index=k,pickup=pickup,high=high,low=low,required=required,deadline=deadline,pulse=pulse,gap=gap,recovery=recovery))
print(json.dumps({'counts':count,'examples':examples},indent=2))
