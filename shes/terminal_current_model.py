"""Extract phase-aware relay-terminal current magnitudes from DSS element arrays."""
import math
def terminal_currents(d,element_name):
 d.ActiveCircuit.SetActiveElement(element_name)
 e=d.ActiveCircuit.ActiveCktElement
 ncond=int(e.NumConductors);nterm=int(e.NumTerminals)
 values=list(map(float,e.CurrentsMagAng))
 if len(values)!=2*ncond*nterm:raise ValueError("unexpected DSS current-array length")
 buses=list(e.BusNames)
 result=[]
 for term in range(nterm):
  for cond in range(ncond):
   amp=values[2*(term*ncond+cond)]
   if not math.isfinite(amp) or amp<0:raise ValueError("invalid terminal current")
   result.append({"terminal":term+1,"conductor":cond+1,"bus":buses[term],
     "current_a":amp,"phase_identity_verified":False})
 return result
def uncertainty_envelope(primary,backup,gmin=.7,delay_max=.04):
 if not 0<gmin<=1 or delay_max<0:raise ValueError("invalid uncertainty")
 if min(primary,backup)<0:raise ValueError("invalid current")
 return {"primary_a":[gmin*primary,primary],"backup_a":[gmin*backup,backup],
   "independent_box":True,"common_derating_subset":True,
   "breaker_delay_s":[0,delay_max],
   "calibrated_to_equipment":False,"pickup_persistence_validated":False}
