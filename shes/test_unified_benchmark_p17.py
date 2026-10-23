import unittest
from shes.unified_benchmark_p17 import run,cases,screen,confusion,frequency_ok
class P17Tests(unittest.TestCase):
 def test_seed_repeatable(self):
  a,b=cases(5,1717),cases(5,1717)
  self.assertEqual(a,b)
 def test_all_resets(self):
  self.assertEqual({c["reset"] for c in cases(9)},{"full","hold","linear"})
 def test_rectangle_matches_grid(self):
  d=run(30)
  self.assertEqual(d["rectangular_continuum_reference"]["time_domain_grid"]["false_approvals"],0)
  self.assertEqual(d["rectangular_continuum_reference"]["time_domain_grid"]["conservative_rejections"],0)
 def test_frequency_gate(self):
  c=cases(1)[0];c["df_hz"]=2.
  self.assertFalse(frequency_ok(c))
  self.assertFalse(screen(c,"rectangle"))
 def test_confusion(self):
  self.assertEqual(confusion([True,True,False,False],[True,False,True,False]),
   {"true_approvals":1,"false_approvals":1,"conservative_rejections":1,
    "true_rejections":1,"approval_count":2,"approval_fraction":.5})
 def test_interior_correlated_counterexample(self):
  from shes.robust_continuum_p13 import correlated_counterexample
  self.assertEqual([s["passes_margin_0_4"] for s in correlated_counterexample()["samples"]],[True,False,True])
if __name__=="__main__":unittest.main()
