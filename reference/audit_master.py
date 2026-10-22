#!/usr/bin/env python3
"""Offline BibTeX metadata audit; never invent or auto-promote sources."""
import collections
import json
import pathlib
import re
import sys

def audit(content):
    entries = re.findall(r"(?m)^@(\w+)\s*\{\s*([^,\s]+)\s*,", content)
    keys = [k for _, k in entries]
    dois = re.findall(r"(?im)^\s*doi\s*=\s*\{([^}]+)\}", content)
    norm = [x.strip().lower().removeprefix("https://doi.org/") for x in dois]
    duplicates = sorted([x for x, n in collections.Counter(keys).items() if n > 1])
    duplicate_dois = sorted([x for x, n in collections.Counter(norm).items() if n > 1])
    invalid_dois = sorted(x for x in norm if not re.fullmatch(r"10\.\d{4,9}/\S+", x))
    return {"total_records":len(entries),"by_type":dict(sorted(collections.Counter(t.lower() for t,_ in entries).items())),"doi_fields":len(dois),"without_doi":len(entries)-len(dois),"duplicate_keys":duplicates,"duplicate_dois":duplicate_dois,"invalid_dois":invalid_dois,"note":"Regex-based screening only; not complete BibTeX parsing or external metadata verification"}

def main():
    path=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "reference/master.bib")
    report=audit(path.read_text(encoding="utf-8"))
    print(json.dumps(report,indent=2))
    if any(report[k] for k in ("duplicate_keys","duplicate_dois","invalid_dois")):
        raise SystemExit("FAIL: duplicate or malformed bibliography identifiers")

if __name__=="__main__":
    main()
