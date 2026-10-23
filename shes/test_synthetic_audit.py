import unittest, sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from audit_synthetic import comparative, execute, original_checks

class SyntheticAuditTests(unittest.TestCase):
 def test_source_count_reproduction(self):
  names=("independent","interrupted","finite","scalar","rk4")
  original_checks({n:execute(n) for n in names})
 def test_contingency_arithmetic(self):
  c=original_checks({n:execute(n) for n in ("independent","interrupted","finite","scalar","rk4")})["finite_contingency"]
  self.assertEqual(c,{"both":3104,"nominal_only":3530,"robust_only":129,"neither":13237})
 def test_sensitivity_box_soundness(self):
  for g in (.6,.7,.8):
   out=comparative(n=300,seed=123,gmin=g)
   self.assertEqual(out["screens"]["box"]["false_approval"],0)
   self.assertEqual(out["screens"]["box"]["rejected_safe"],0)
 def test_false_approval_accounting(self):
  out=comparative(n=500,seed=5)
  for row in out["screens"].values():
   self.assertEqual(row["approved"],row["false_approval"]+row["true_approval"])
 def test_no_cross_population_pooled_rates(self):
  a=execute("independent")["counts"]
  b=execute("interrupted")["counts"]
  self.assertNotEqual(a["nominal"],b["static_approved"])
if __name__=="__main__":unittest.main()
