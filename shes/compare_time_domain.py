"""Cross-model stress test: constant-current screens versus two-pulse full-reset traces.
The time-domain trace is the stipulated oracle, NOT measured feeder current.
"""
import json, math, random
from relay_time_domain import Segment, relay_assertion, coordinated, inverse_time_constant

def evaluate(seed=20261023,n=4000,derating=.7):
 rng=random.Random(seed)
 counts={k:{"approved":0,"false_approval":0,"rejected_safe":0,"true_approval":0}
         for k in ("nominal","common","box","time_domain")}
 witnesses=[]
 for k in range(n):
  pp,pb=rng.uniform(.5,1.2),rng.uniform(.5,1.2)
  sp,sb=rng.uniform(.025,.12),rng.uniform(.09,.38)
  ip,ib=rng.uniform(1.3,3.8),rng.uniform(1.2,3.8)
  margin=rng.uniform(.06,.2); dp=rng.uniform(.5,1.5); db=rng.uniform(1.6,3.)
  breaker_p=rng.uniform(.01,.06); breaker_b=rng.uniform(.01,.06)
  high_dur=rng.uniform(.04,.35); gap=rng.uniform(.01,.25)
  horizon=max(dp,db)
  if high_dur+gap>=horizon:continue
  low_factor=rng.uniform(.05,.6)
  # Distinct primary and backup derating in actual trace
  gp,gb=rng.uniform(derating,1.),rng.uniform(derating,1.)
  def trace(high):
   return [Segment(0,high_dur,high),Segment(high_dur,high_dur+gap,high*low_factor),
    Segment(high_dur+gap,horizon,high)]
  # Inverter-limited currents may fall below pickup during the gap.
  tp=relay_assertion(trace(ip*gp),horizon,pp,sp,"full")
  tb=relay_assertion(trace(ib*gb),horizon,pb,sb,"full")
  actual=coordinated(tp,tb,breaker_p,breaker_b,dp,db,margin)
  def constant(gp0,gb0):
   return coordinated(inverse_time_constant(ip*gp0,pp,sp),
     inverse_time_constant(ib*gb0,pb,sb),breaker_p,breaker_b,dp,db,margin)
  nominal=constant(1.,1.)
  common=constant(derating,derating)
  # For independent interval under constant current, conservative extrema.
  tps=inverse_time_constant(ip*derating,pp,sp)
  tbe=inverse_time_constant(ib,pb,sb)
  tbl=inverse_time_constant(ib*derating,pb,sb)
  box=(math.isfinite(tps) and math.isfinite(tbe) and math.isfinite(tbl)
    and tps+breaker_p<=dp and tbl+breaker_b<=db
    and tbe-(tps+breaker_p)>=margin)
  for name,accept in (("nominal",nominal),("common",common),
                      ("box",box),("time_domain",actual)):
   row=counts[name];row["approved"]+=accept
   row["false_approval"]+=accept and not actual
   row["true_approval"]+=accept and actual
   row["rejected_safe"]+=(not accept) and actual
  if box and not actual and len(witnesses)<3:
   witnesses.append({"index":k,"primary_high":ip*gp,"backup_high":ib*gb,
    "low_factor":low_factor,"pulse":high_dur,"gap":gap,
    "primary_assertion":tp if math.isfinite(tp) else None,
    "backup_assertion":tb if math.isfinite(tb) else None})
 return {"cases":n,"seed":seed,"derating":derating,"counts":counts,
  "counterexamples_box_vs_time_domain":witnesses,
  "interpretation":"Full-reset piecewise-current synthetic oracle only. Different model than constant-current box."}
if __name__=="__main__":print(json.dumps(evaluate(),indent=2,sort_keys=True))
