"""P12 final scope and archive integrity check. This does not verify field safety."""
import json,hashlib,pathlib
from shes.audit_program_p11 import audit
def main():
 r=audit()
 p10=json.loads(pathlib.Path("shes/ieee123_p10_joint_model.json").read_text())
 assert p10["corner_completeness_proved"] is False
 assert p10["physical_certificates_issued"]==0
 assert p10["interior_samples_checked"]==1458
 assert p10["interior_corner_approval_violations"]==0
 assert p10["joint_model_approvals"]==18
 assert p10["frequency_worst_pass"]==1097
 report={"status":"PASS_ARCHIVE_SCOPE_ONLY","replayed_p9":r["p9_cases"],
  "replayed_p10":r["p10_cases"],"interior_samples":1458,
  "continuum_robustness_proved":False,"physical_authorizations":0,
  "bibliography_external_metadata_verified":False,
  "figures_regenerated_from_original_data":False,
  "complete_manuscript_ci_verified":False}
 print(json.dumps(report,sort_keys=True))
if __name__=="__main__":main()
