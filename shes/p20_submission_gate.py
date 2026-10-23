"""P20 fail-closed complete manuscript source gate. No PDF success implied."""
from pathlib import Path
import argparse,json
FILES=("main.tex","references.bib","figures/pickup_dropout.pdf",
"figures/relay_screen.pdf","figures/relay_uncertainty.pdf","figures/static_voltage.pdf",
"p13_continuum_section.tex","p14_phase_topology_section.tex",
"p15_switch_sensitivity_section.tex","p16_winding_fault_section.tex",
"p17_unified_benchmark_section.tex","p18_component_ablation_section.tex",
"p19_independent_audit_section.tex")
def audit(root):
 p=Path(root)
 missing=[f for f in FILES if not (p/f).is_file() or not (p/f).stat().st_size]
 main=(p/"main.tex").read_text() if (p/"main.tex").is_file() else ""
 if "\\documentclass" not in main:missing.append("main.tex:complete-document")
 if "\\bibliography{references}" not in main:missing.append("main.tex:bibliography-declaration")
 return {"ready":not missing,"missing":missing,
 "claim":"Only source gate. Passing it does not certify bibliography metadata, anonymity or PDF compilation."}
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--root",default="shes")
 a.add_argument("--require-ready",action="store_true");x=a.parse_args()
 result=audit(x.root);print(json.dumps(result,sort_keys=True))
 if x.require_ready and not result["ready"]:raise SystemExit(1)
