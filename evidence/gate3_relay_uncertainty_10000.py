"""Relay uncertainty stress test: synthetic assumptions, not a relay device model."""
import random,json
rng=random.Random(20261022)
count={'cases':0,'nominal_approved':0,'nominal_missed_trip':0,'robust_approved':0,'robust_missed_trip':0}
examples=[]
for k in range(10000):
 imax=rng.uniform(.8,1.8);ifault=rng.uniform(.8,2.2);pickup=rng.uniform(.4,1.5)
 delay=rng.uniform(.02,.20);deadline=rng.uniform(.08,.24)
 actual_current=.7*min(ifault,imax)
 actual_delay=delay+.04
 nominal=min(ifault,imax)>=pickup and delay<=deadline
 robust=actual_current>=pickup and actual_delay<=deadline
 actual=actual_current>=pickup and actual_delay<=deadline
 count['cases']+=1;count['nominal_approved']+=nominal
 count['nominal_missed_trip']+=nominal and not actual
 count['robust_approved']+=robust;count['robust_missed_trip']+=robust and not actual
 if nominal and not actual and len(examples)<3:
  examples.append({'case':k,'imax':imax,'ifault':ifault,'pickup':pickup,'delay':delay,'deadline':deadline,'actual_current':actual_current,'actual_delay':actual_delay})
print(json.dumps({'counts':count,'counterexamples':examples},indent=2))
