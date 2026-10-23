"""Independent, fail-closed structural validator for Prompt 9."""
import json,sys
def validate(r):
 if r.get("status")!="PASS_HYPOTHETICAL_SCREENS_ONLY":raise ValueError("status")
 if r.get("population")!=1200:raise ValueError("unexpected population")
 for key in ("phase_continuity_verified","switching_feasibility_verified",
  "relay_current_orientation_verified","installed_relay_settings_verified",
  "frequency_certificate_verified","restoration_safety_verified"):
  if r.get(key) is not False:raise ValueError("unsupported claim: "+key)
 for ref in ("constant_corner_oracle","full_reset_trace"):
  if ref not in r["tables"]:raise ValueError("missing reference")
  for name in ("nominal","common","box","full_reset_trace"):
   x=r["tables"][ref][name]
   if set(x)!={"TP","FP","FN","TN"} or any(type(v)!=int or v<0 for v in x.values()) or sum(x.values())!=1200:
    raise ValueError("bad contingency "+ref+"/"+name)
 if r["tables"]["constant_corner_oracle"]["box"]["FP"] or r["tables"]["constant_corner_oracle"]["box"]["FN"]:
  raise ValueError("box/corner theorem violated")
 if r["tables"]["full_reset_trace"]["full_reset_trace"]["FP"] or r["tables"]["full_reset_trace"]["full_reset_trace"]["FN"]:
  raise ValueError("self oracle violated")
 return True
if __name__=="__main__":
 validate(json.load(open(sys.argv[1])));print("PASS: 1200 model-relative cases, all contingency tables, conservative scope")
