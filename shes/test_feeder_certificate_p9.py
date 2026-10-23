import unittest,math
from shes.feeder_certificate_p9 import screen,trace_screen,case_current,evaluate
class Tests(unittest.TestCase):
 def test_corner_theorem(self):
  for a in (.6,.7,.8):
   for ip in (1.5,2.,4.):
    for ib in (1.3,3.):
     screen(ip,ib,1.,1.,.05,.2,1.,4.,.2,a,.04)
 def test_breaker_delay_counterexample(self):
  early=screen(3.,3.,1.,1.,.03,.2,2.,6.,.2,.7,0.)
  late=screen(3.,3.,1.,1.,.03,.2,2.,6.,.2,.7,.5)
  self.assertIsInstance(early["box"],bool)
  self.assertIsInstance(late["box"],bool)
 def test_no_missing_terminal_imputation(self):
  self.assertIsNone(case_current({"candidate_terminal_currents":{}},"primary"))
 def test_time_domain_not_same_as_static(self):
  self.assertIsInstance(trace_screen(3,3,1,1,.04,.2,2,5,.2),bool)
 def test_scope_flags(self):
  source={"pin":"p","sha256":{},"results":[
   {"bus":"60","fault_resistance_ohm":.1,"candidate_terminal_currents":{
    "primary":{"currents":[{"terminal":1,"conductor":1,"current_a":100.}]},
    "backup":{"currents":[{"terminal":1,"conductor":1,"current_a":80.}]}}}]}
  r=evaluate(source,draws=8)
  self.assertEqual(r["population"],8)
  self.assertFalse(r["restoration_safety_verified"])
  for table in r["tables"].values():
   for cell in table.values():self.assertEqual(sum(cell.values()),8)
if __name__=="__main__":unittest.main()
