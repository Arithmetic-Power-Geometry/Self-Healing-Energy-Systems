import unittest,math
from shes.component_ablation_p18 import (ABLATIONS,conditions,full,ablated,
    sensitivity,overlap_table,run)
from shes.unified_benchmark_p17 import cases,screen
class P18Tests(unittest.TestCase):
 def test_exact_reference_matches_independent_p17(self):
  data=cases(90,1717)
  self.assertEqual([full(c) for c in data],[screen(c,"rectangle") for c in data])
 def test_omission_gates_cannot_create_false_rejections(self):
  for c in cases(90,1717):
   for name in ("frequency","primary_deadline","backup_deadline",
                "coordination_margin","breaker_delay"):
    if full(c):self.assertTrue(ablated(c,name),(name,c["id"]))
 def test_repeatable_confusion_not_timing(self):
  a,b=run(15,1717,2),run(15,1717,2)
  self.assertEqual({k:v["confusion"] for k,v in a["ablations"].items()},
                   {k:v["confusion"] for k,v in b["ablations"].items()})
 def test_width_monotonicity(self):
  counts=[r["approved"] for r in sensitivity(cases(90,1717))]
  self.assertEqual(counts,sorted(counts,reverse=True))
 def test_witnesses_are_independently_replayable(self):
  d=run(90,1717,2);data=cases(90,1717)
  for name,entry in d["ablations"].items():
   w=entry["witness"]
   if w:
    c=data[w["id"]]
    self.assertFalse(full(c))
    self.assertTrue(ablated(c,name))
    self.assertEqual(w["component_truth"],conditions(c))
 def test_overlap_symmetric_and_counts(self):
  d=run(90,1717,2)
  for a in ABLATIONS:
   for b in ABLATIONS:
    self.assertEqual(d["overlap"]["pairwise_overlap"][a][b],
                     d["overlap"]["pairwise_overlap"][b][a])
   self.assertEqual(d["overlap"]["pairwise_overlap"][a][a],
                    d["ablations"][a]["confusion"]["false_approvals"])
 def test_analytic_correlated_interior_failure(self):
  w=run(3,1717,2)["correlated_continuum_analytic_counterexample"]
  self.assertEqual([x["passes_margin_0_4"] for x in w["samples"]],[True,False,True])
if __name__=="__main__":unittest.main()
