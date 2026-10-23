"""Independent structural audit of P10 result; no physical certificate permitted."""
import json,sys
def validate(r):
 if r.get("status")!="PASS_MODEL_ONLY_PHYSICAL_GATE_BLOCKED":raise ValueError("status")
 if r.get("population")!=1440:raise ValueError("population")
 if r.get("physical_certificates_issued")!=0 or r.get("physical_restoration_validated") is not False:
  raise ValueError("unsupported physical certificate")
 if not r.get("physical_gate") or any(v is not False for v in r["physical_gate"].values()):
  raise ValueError("gate must fail closed")
 if r.get("corner_completeness_proved") is not False:
  raise ValueError("unproved continuum corner completeness")
 if type(r.get("interior_samples_checked")) is not int or r["interior_samples_checked"]<0:
  raise ValueError("interior audit missing")
 if type(r.get("interior_corner_approval_violations")) is not int:
  raise ValueError("interior violation count missing")
 for reset in ("full","hold","linear"):
  t=r["tables"].get(reset,{})
  for name in ("nominal","common","box"):
   m=t.get(name,{})
   if set(m)!={"TP","FP","FN","TN"} or any(type(x)!=int or x<0 for x in m.values()) or sum(m.values())!=480:
    raise ValueError("bad confusion matrix")
  if t["box"]["FP"]!=0 or t["box"]["FN"]!=0:
   raise ValueError("exact independent corner oracle disagreement")
 return True
if __name__=="__main__":
 validate(json.load(open(sys.argv[1])));print("PASS: all reset-specific tables and fail-closed physical gate")
