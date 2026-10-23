"""Independent cross-artifact and deterministic-replay audit for SHES P1-P10.

Checks archived source provenance and result consistency; does NOT independently
validate physical feeder model or mathematically prove continuous uncertainty.
"""
import json,pathlib,math
from shes.feeder_certificate_p9 import evaluate
from shes.joint_certificate_p10 import run,frequency_envelope
from shes.validate_p9 import validate as validate_p9
from shes.validate_joint_p10 import validate as validate_p10
from shes.validate_topology_result import validate as validate_topology
def read(path):
 return json.loads(pathlib.Path(path).read_text())
def audit(root=pathlib.Path("shes")):
 synthetic=read(root/"results/synthetic_audit.json")
 dynamic=read(root/"results/time_domain_comparison.json")
 fault=read(root/"ieee123_fault_probe_result.json")
 topology=read(root/"ieee123_topology_result.json")
 p9=read(root/"ieee123_p9_screens.json")
 p10=read(root/"ieee123_p10_joint_model.json")
 validate_topology(topology);validate_p9(p9);validate_p10(p10)
 assert len(fault["cases"])==54
 assert fault["upstream_commit"]==topology["pin"]==p9["source_pin"]==p10["source_pin"]
 assert topology["sha256"]==p9["source_sha256"]==p10["source_sha256"]
 assert topology["element_kinds"]["line"]==126
 assert topology["element_kinds"]["transformer"]==8
 assert len(topology["results"])==9
 assert p9["population"]==1200 and p10["population"]==1440
 assert synthetic["original_counts"]["rk4"]=={"conservative":84,"refined":402,
   "refined_unsafe":0,"rk4_safe":486,"total":2592}
 assert synthetic["original_counts"]["independent"]["nominal_fails_any"]==4739
 assert synthetic["finite_contingency"]=={"both":3104,"neither":13237,
   "nominal_only":3530,"robust_only":129}
 assert dynamic["cases"]==4000 and dynamic["counts"]["box"]["false_approval"]==118
 assert sum(dynamic["counts"]["box"][k] for k in ("true_approval","false_approval"))==940
 assert p9["tables"]==evaluate(topology)["tables"]
 replay=run(topology)
 for key in ("tables","frequency_worst_pass","joint_model_approvals",
  "interior_samples_checked","interior_corner_approval_violations"):
  assert p10[key]==replay[key],key
 assert p10["corner_completeness_proved"] is False
 assert p10["physical_certificates_issued"]==0
 assert all(not v for v in p10["physical_gate"].values())
 # Analytic constant-input scalar ODE independently checked at grid points.
 for M,D,u,f0,T in ((2.,1.,.5,-.2,1.),(4.,2.,-.3,.1,2.),
  (3.,.5,.8,-.4,4.)):
  dt=T/10000.;f=f0
  for _ in range(10000):
   k1=(u-D*f)/M
   k2=(u-D*(f+dt*k1/2))/M
   k3=(u-D*(f+dt*k2/2))/M
   k4=(u-D*(f+dt*k3))/M
   f+=dt*(k1+2*k2+2*k3+k4)/6
  envelope=frequency_envelope(f0,M,D,u,u,T)
  assert abs(f)<=envelope+1e-8
 return {"status":"PASS_ARCHIVE_REPLAY_ONLY","p9_cases":1200,
  "p10_cases":1440,"p10_interior_samples":p10["interior_samples_checked"],
  "p10_interior_failures":p10["interior_corner_approval_violations"],
  "physical_safety_validated":False,
  "not_reproduced":["all original figures from source data",
   "field protection settings","phase-specific energized connectivity",
   "manufacturer relay firmware","inverter EMT","complete novelty search"]}
if __name__=="__main__":
 import sys
 out=audit()
 print(json.dumps(out,sort_keys=True))
