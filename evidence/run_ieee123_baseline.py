#!/usr/bin/env python3
"""Gate 3 reproducible IEEE123 feeder baseline. Fail closed on missing files/engine.
Usage: python evidence/run_ieee123_baseline.py --feeder /path/to/123Bus
Requires: pip install dss-python==0.15.7
Does not add inverter or claim EMT validation.
"""
import argparse, hashlib, json, pathlib, re, sys

def dependencies(root, filename, visited=None):
    visited = visited or set()
    p = (root / filename).resolve()
    if not p.is_relative_to(root.resolve()):
        raise ValueError("DSS dependency escapes feeder directory: "+str(p))
    if not p.is_file():
        raise FileNotFoundError("Required DSS file missing: "+str(p))
    if p in visited: return visited
    visited.add(p)
    for line in p.read_text(errors="replace").splitlines():
        line = line.split("!")[0].strip()
        m = re.match(r"^(?:redirect|compile)\s+\(?[\"']?([^\"')]+\.dss)",line,re.I)
        if m: dependencies(root,m.group(1).strip(),visited)
    return visited

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--feeder",type=pathlib.Path,required=True)
    ap.add_argument("--output",type=pathlib.Path,default=pathlib.Path("evidence/ieee123_baseline_result.json"))
    args=ap.parse_args()
    root=args.feeder.resolve()
    files=dependencies(root,"IEEE123Master.dss")
    provenance={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    try:
        from dss import DSS
    except ImportError as e:
        raise RuntimeError("DSS-Python missing: install dss-python==0.15.7; no simulation run") from e
    engine=DSS.NewContext()
    engine.Text.Command('clear')
    engine.Text.Command(f'compile "{root / "IEEE123Master.dss"}"')
    engine.Text.Command("set mode=snapshot")
    engine.Text.Command("solve")
    if not engine.ActiveCircuit.Solution.Converged:
        raise RuntimeError("IEEE123 load flow did not converge")
    volts=list(map(float,engine.ActiveCircuit.AllBusVmagPu))
    if not volts or min(volts)<=0:
        raise RuntimeError("Missing/invalid bus voltage results")
    result={"model":"IEEE123 static baseline only","source_files_sha256":provenance,
            "engine_version":engine.Version,"converged":True,
            "node_count":len(volts),"vmin_pu":min(volts),"vmax_pu":max(volts),
            "no_dynamic_inverter":True,"no_protection_validation":True}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
