#!/usr/bin/env python3
"""Independent fail-closed schema and numerical consistency check for IEEE123 output."""
import argparse
import json
import math
from pathlib import Path

def validate(result):
    if result.get("status") != "PASS_STATIC_ONLY" or result.get("feeder") != "IEEE123":
        raise ValueError("Unexpected status or feeder")
    if any(result.get(k) is not False for k in ("gfm_dynamics_validated", "protection_validated", "emt_validated")):
        raise ValueError("Static experiment must not claim dynamic/protection/EMT validation")
    sha = result.get("sha256")
    if not isinstance(sha, dict) or "IEEE123Master.dss" not in sha:
        raise ValueError("Missing feeder source hashes")
    if any(not isinstance(v, str) or len(v) != 64 or any(c not in "0123456789abcdef" for c in v) for v in sha.values()):
        raise ValueError("Invalid SHA256 hashes")
    rows = result.get("scenarios")
    if not isinstance(rows, list) or len(rows) != 2 or {x.get("scenario") for x in rows} != {"static_off", "static_controls"}:
        raise ValueError("Expected exactly two distinct static scenarios")
    for row in rows:
        if row.get("converged") is not True:
            raise ValueError("Unconverged scenario")
        n = row.get("node_count")
        if not isinstance(n, int) or isinstance(n, bool) or n < 100:
            raise ValueError("Implausible IEEE123 voltage-node count")
        lo, hi = row.get("vmin_pu"), row.get("vmax_pu")
        if any(not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x) for x in (lo, hi)):
            raise ValueError("Nonfinite or missing voltage extrema")
        if not 0.5 <= lo <= hi <= 1.5:
            raise ValueError("Voltage bounds violated")
        power = row.get("total_power_kw_kvar")
        if not isinstance(power, list) or len(power) != 2 or any(not isinstance(x, (int, float)) or not math.isfinite(x) for x in power):
            raise ValueError("Invalid feeder power")
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    validate(json.loads(args.result.read_text()))
    print("PASS: static IEEE123 output schema and consistency only")

if __name__ == "__main__":
    main()
