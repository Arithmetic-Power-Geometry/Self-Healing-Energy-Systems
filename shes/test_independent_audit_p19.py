import unittest
from shes.independent_audit_p19 import audit
class P19Tests(unittest.TestCase):
 def test_fail_closed_manuscript(self):
  a=audit("shes")
  self.assertFalse(a["complete_manuscript_build_ready"])
  self.assertIn("references.bib",a["missing_manuscript_assets"])
  self.assertIn("main.tex:complete_documentclass",a["missing_manuscript_assets"])
 def test_replayed_model_counts(self):
  a=audit("shes")
  self.assertEqual(a["p17_recomputed"]["nominal"]["false_approvals"],19)
  self.assertEqual(a["p18_recomputed"]["coordination_margin"]["false_approvals"],22)
 def test_no_physical_certification(self):
  self.assertEqual(audit("shes")["physical_protection_authorizations"],0)
if __name__=="__main__":unittest.main()
