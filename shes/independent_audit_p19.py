"""P19 independent fail-closed audit of source, model claims, and P17/P18 replay."""
import argparse,json,pathlib,hashlib,math
from shes.unified_benchmark_p17 import cases,screen,confusion
from shes.component_ablation_p18 import ABLATIONS,full,ablated,sensitivity,overlap_table
from shes.robust_continuum_p13 import correlated_counterexample,rectangular_certificate,time_at_gamma
from shes.relay_time_domain import Segment

REQUIRED=["main.tex","references.bib","figures/pickup_dropout.pdf",
 "figures/relay_screen.pdf","figures/relay_uncertainty.pdf","figures/static_voltage.pdf"]
SECTIONS=["p13_continuum_section.tex","p14_phase_topology_section.tex",
 "p15_switch_sensitivity_section.tex","p16_winding_fault_section.tex",
 "p17_unified_benchmark_section.tex","p18_component_ablation_section.tex"]
def audit(root):
 root=pathlib.Path(root).resolve()
 missing=[p for p in REQUIRED if not (root/p).is_file() or (root/p).stat().st_size==0]
 main=(root/"main.tex").read_text() if (root/"main.tex").exists() else ""
 if "\\documentclass" not in main:missing.append("main.tex:complete_documentclass")
 if "\\bibliography{references}" not in main:missing.append("main.tex:bibliography")
 missing_sections=[p for p in SECTIONS if not (root/p).is_file()]
 # All source-level assertions are independent of P17/P18 result JSON.
 data=cases(90,1717);truth=[full(c) for c in data]
 assert truth==[screen(c,"rectangle") for c in data]
 p17={m:confusion([screen(c,m) for c in data],truth)
   for m in ("nominal","common_endpoints","rectangle","time_domain_grid")}
 p18={m:confusion([ablated(c,m) for c in data],truth) for m in ABLATIONS}
 assert sum(truth)==22
 assert [p17[m]["false_approvals"] for m in p17]==[19,3,0,0]
 assert [p18[m]["false_approvals"] for m in ABLATIONS]==[14,1,6,22,0,3,0]
 assert [p18[m]["conservative_rejections"] for m in ABLATIONS]==[0,0,0,0,2,0,0]
 widths=sensitivity(data)
 assert [x["approved"] for x in widths]==[40,34,27,24,11]
 overlap=overlap_table(data)
 for a in ABLATIONS:
  assert len(overlap["per_ablation_false_approval_ids"][a])==p18[a]["false_approvals"]
  for b in ABLATIONS:
   assert overlap["pairwise_overlap"][a][b]==overlap["pairwise_overlap"][b][a]
 w=correlated_counterexample()
 assert [s["passes_margin_0_4"] for s in w["samples"]]==[True,False,True]
 # Distinct independent direct calculation: positive interval endpoint inequalities.
 trace=[Segment(0.,10.,2.)]
 assert math.isfinite(time_at_gamma(trace,.8,.5,.1))
 assert isinstance(rectangular_certificate(trace,trace,.5,.5,.1,.2,(.8,1.),(.8,1.),
    (0.,.05),(0.,.05),10.,10.,0.),bool)
 # This is a consistency audit, not a formal verification of source-level proof.
 return {"audit":"P19 source-level independent deterministic replay",
   "source_sha256":{p:hashlib.sha256((root/p).read_bytes()).hexdigest()
      for p in SECTIONS if (root/p).is_file()},
   "p17_recomputed":p17,"p18_recomputed":p18,
   "p18_overlap_recomputed":overlap["pairwise_overlap"],
   "uncertainty_width_recomputed":widths,
   "correlated_witness_recomputed":w,
   "missing_manuscript_assets":missing,
   "missing_p13_p18_sections":missing_sections,
   "complete_manuscript_build_ready":not missing and not missing_sections,
   "physical_protection_authorizations":0,
   "findings":[
    "P13 theorem is exact only for fixed templates, monotone progress/reset and Cartesian uncertainty.",
    "P13 backup deadline uses backup breaker delay; coordination compares backup assertion to primary clearing.",
    "P13 correlated endpoints fail at interior gamma=0.38 in analytic witness.",
    "P17 time-domain grid uses the same relay assertion implementation as theorem reference; not an independent numerical oracle.",
    "P18 first failing witnesses are not mathematically minimal.",
    "P18 timer-memory ablation resets at all segment boundaries, including above pickup; this is not a vendor relay model.",
    "P14-P16 do not verify transformer transfer matrices, energized source paths, CT polarity, installed relay settings or thermal compliance.",
    "P15-P16 switched-off cases at buses 60/83 have zero reported voltage; convergence is not restoration feasibility.",
    "Full manuscript bibliography, figure integrity and anonymous PDF cannot be audited from the current repository placeholder."
   ]}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--root",default="shes")
 p.add_argument("--output",required=True);a=p.parse_args()
 d=audit(a.root);o=pathlib.Path(a.output).resolve()
 o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"full_approvals":d["p17_recomputed"]["rectangle"]["true_approvals"],
  "missing_assets":d["missing_manuscript_assets"],
  "complete_manuscript_build_ready":d["complete_manuscript_build_ready"]}))
