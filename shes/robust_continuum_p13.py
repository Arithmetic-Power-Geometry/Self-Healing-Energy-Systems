"""SHES P13: exact rectangular robust coordination under monotone timer dynamics.

A separate correlated-gamma counterexample shows why checking only common
uncertainty endpoints is NOT sufficient. Research model, not field protection.
"""
from math import isfinite,inf
from shes.relay_time_domain import Segment,relay_assertion,coordinated

def time_at_gamma(trace,gamma,pickup,tds,reset="full",reset_rate=1.):
 if gamma<0 or not isfinite(gamma):raise ValueError("gamma must be finite nonnegative")
 horizon=trace[-1].end
 return relay_assertion([Segment(s.start,s.end,s.current*gamma) for s in trace],
                        horizon,pickup,tds,reset=reset,reset_rate=reset_rate)

def rectangular_certificate(primary,backup,primary_pickup,backup_pickup,
  primary_tds,backup_tds,gp_interval,gb_interval,bp_interval,bb_interval,
  primary_deadline,backup_deadline,margin,reset="full",reset_rate=1.):
 """Exact iff for Cartesian-product scalar deratings/delays, fixed traces,
 fixed initial timer=0, and monotone progress/reset semantics. No correlations.
 """
 for lo,hi in (gp_interval,gb_interval,bp_interval,bb_interval):
  if not all(isfinite(x) for x in (lo,hi)) or lo<0 or lo>hi:
   raise ValueError("invalid uncertainty interval")
 if primary_deadline<0 or backup_deadline<0 or margin<0:
  raise ValueError("invalid deadlines or margin")
 tp_late=time_at_gamma(primary,gp_interval[0],primary_pickup,primary_tds,reset,reset_rate)
 tb_late=time_at_gamma(backup,gb_interval[0],backup_pickup,backup_tds,reset,reset_rate)
 tb_early=time_at_gamma(backup,gb_interval[1],backup_pickup,backup_tds,reset,reset_rate)
 # Finite assertion of both relays is an explicit requirement.
 return (all(isfinite(t) for t in (tp_late,tb_late,tb_early))
  and tp_late+bp_interval[1]<=primary_deadline
  and tb_late+bb_interval[1]<=backup_deadline
  and tb_early-(tp_late+bp_interval[1])>=margin)

def correlated_counterexample():
 # A common derating gamma, NOT independently variable primary/backup gamma.
 # Primary fault current begins at 0; backup is below pickup for first 1 s.
 # Both then have constant 1-A normalized current. IEC-type inverse-time
 # coefficient = .14*tds, exponent .02.
 primary=[Segment(0.,20.,1.)]
 backup=[Segment(0.,1.,0.),Segment(1.,20.,1.)]
 pp,pb=.193,.274
 tdsp,tdsb=.020/.14,.0046/.14
 samples=[]
 for g in (.28,.38,1.):
  tp=time_at_gamma(primary,g,pp,tdsp)
  tb=time_at_gamma(backup,g,pb,tdsb)
  samples.append({"gamma":g,"primary_assert_s":tp,
    "backup_assert_s":tb,"margin_s":tb-tp,
    "passes_margin_0_4":tb-tp>=.4})
 assert samples[0]["passes_margin_0_4"]
 assert not samples[1]["passes_margin_0_4"]
 assert samples[2]["passes_margin_0_4"]
 return {"uncertainty":"common correlated derating gamma in [0.28,1]",
  "primary_trace":"1 A for 0 to 20 s","backup_trace":"0 A for 0 to 1 s, then 1 A until 20 s",
  "pickup_primary_a":pp,"pickup_backup_a":pb,
  "tds_primary":tdsp,"tds_backup":tdsb,
  "deadline_primary_s":20.,"deadline_backup_s":20.,
  "breaker_delays_s":[0.,0.],"required_margin_s":.4,
  "samples":samples,
  "conclusion":"Both correlated endpoints pass but interior gamma=0.38 violates positive coordination margin."}
if __name__=="__main__":
 import json
 print(json.dumps(correlated_counterexample(),indent=2))
