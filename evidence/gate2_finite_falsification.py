#!/usr/bin/env python3
"""Gate 2: exhaustive finite safe-decision vs full-identification tests.
Only abstract state/action semantics; NOT an electrical safety model.
Run: python3 evidence/gate2_finite_falsification.py
"""
from itertools import combinations, product

def partitions(n):
    # restricted growth strings enumerate all set partitions
    def rec(prefix, max_label):
        if len(prefix) == n:
            yield tuple(prefix)
        else:
            for x in range(max_label + 2):
                yield from rec(prefix + [x], max(max_label, x))
    yield from rec([0], 0)

def cells(belief, outcomes):
    d = {}
    for w in belief:
        d.setdefault(outcomes[w], set()).add(w)
    return list(d.values())

def worst_cost(belief, tests, actions, require_id=False):
    """Exact adaptive worst-case number of tests, unit cost."""
    memo = {}
    def solved(b):
        return len(b) == 1 if require_id else any(b <= safe for safe in actions)
    def rec(b):
        key = frozenset(b)
        if solved(b):
            return 0
        if key in memo:
            return memo[key]
        values = []
        for t in tests:
            parts = cells(b, t)
            if len(parts) == 1: continue
            sub = [rec(p) for p in parts]
            if all(v != float('inf') for v in sub):
                values.append(1 + max(sub))
        memo[key] = min(values, default=float('inf'))
        return memo[key]
    return rec(set(belief))
    
def run():
    # canonical strict separation: w0,w1,w2,w3; actions safe on {0,1} and {2,3};
    # one test reveals pair, but 2 more tests distinguish individual states.
    tests = [(0,0,1,1), (0,1,0,1)]
    actions = [{0,1},{2,3}]
    d = worst_cost(range(4),tests,actions)
    i = worst_cost(range(4),tests,actions,True)
    assert (d,i)==(1,2), (d,i)
    # impossibility: identical observations, incompatible safety; no useful robust action
    assert worst_cost(range(2),[(0,0)],[{0},{1}])==float('inf')
    # exhaustive: all 2-4 state safety action families (nonempty proper subsets),
    # all 1-2 binary tests; verify monotonicity: decision cost <= identification cost.
    count=0; strict=0; impossible=0
    for n in range(2,5):
        subsets=[set(c) for k in range(1,n) for c in combinations(range(n),k)]
        test_bank=list(product((0,1),repeat=n))[1:]
        for actions in combinations(subsets,2):
            if set.union(*actions) != set(range(n)):
                continue  # otherwise some true state has no safe action; decision may be impossible even with full ID
            for tests in combinations(test_bank,2):
                dc=worst_cost(range(n),tests,actions)
                ic=worst_cost(range(n),tests,actions,True)
                assert dc <= ic, (n,actions,tests,dc,ic)
                count+=1
                strict += dc < ic
                impossible += dc==float('inf')
    print(f"PASS cases={count} strict={strict} decision_impossible={impossible}")
    print("Witness decision=1 identification=2; unsafe indistinguishability=inf")
if __name__=="__main__": run()
