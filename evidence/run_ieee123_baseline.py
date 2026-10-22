#!/usr/bin/env python3
"""Fail-closed IEEE123 three-phase load-flow diagnostic. No transient/relay claims."""
import argparse, hashlib, json, math, pathlib, re, traceback

def deps(root, filename, seen=None):
    root=root.resolve(); seen=set() if seen is None else seen
    p=(root/filename).resolve()
    if not p.is_relative_to(root): raise ValueError(f"Dependency escapes feeder: {p}")
    if not p.is_file(): raise FileNotFoundError(f"Missing DSS dependency: {p}")
    if p in seen: return seen
    seen.add(p)
    for raw in p.read_text(errors="replace").splitlines():
        line=raw.split("!")[0].strip()
        m=re.match(r'^(?:redirect|compile)\s+\(?\s*["\']?([^"\')]+?\.dss)',line,re.I)
        if m: deps(root,m.group(1).strip(),seen)
    return seen

def run(root, output):
    root=root.resolve()
    files=deps(root,"IEEE123Master.dss")
    hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    from dss import DSS
    d=DSS.NewContext()
    d.Text.Command = "clear"
    d.Text.Command = f'compile "{root / "IEEE123Master.dss"}"'
    if not d.ActiveCircuit.Name: raise RuntimeError("No circuit compiled")
    results=[]
    # Distinguish solver convergence from controller convergence; no silent defaults.
    for name,cmds in [
        ("static_off",["set mode=snapshot","set controlmode=off","set maxiterations=100","solve"]),
        ("static_controls",["set mode=snapshot","set controlmode=static","set maxiterations=100","set maxcontroliter=100","solve"]),
    ]:
        for cmd in cmds: d.Text.Command = cmd
        sol=d.ActiveCircuit.Solution
        ok=bool(sol.Converged)
        v=list(map(float,d.ActiveCircuit.AllBusVmagPu))
        if not v or any(not math.isfinite(x) for x in v):
            raise RuntimeError(f"Missing or nonfinite per-unit voltages in {name}")
        if not all(0.5 <= x <= 1.5 for x in v):
            raise RuntimeError(f"Implausible IEEE123 voltage range in {name}: {min(v)}..{max(v)}")
        row={"scenario":name,"converged":ok,"node_count":len(v),
             "iterations":int(sol.Iterations),"control_iterations":int(sol.ControlIterations),
             "vmin_pu":min(v) if v else None,"vmax_pu":max(v) if v else None,
             "total_power_kw_kvar":list(map(float,d.ActiveCircuit.TotalPower))}
        results.append(row)
        if not ok or not v or min(v)<=0: raise RuntimeError(f"Invalid/nonconvergent {name}: {row}")
    result={"status":"PASS_STATIC_ONLY","feeder":"IEEE123","solver_version":str(d.Version),
            "sha256":hashes,"scenarios":results,
            "gfm_dynamics_validated":False,"protection_validated":False,
            "emt_validated":False}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2))
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--feeder",type=pathlib.Path,required=True)
    a.add_argument("--output",type=pathlib.Path,default=pathlib.Path("evidence/ieee123_baseline_result.json"))
    args=a.parse_args()
    try:run(args.feeder,args.output)
    except Exception as e:
        print("HARD FAILURE: "+repr(e)); traceback.print_exc(); raise SystemExit(1)
if __name__=="__main__":main()
