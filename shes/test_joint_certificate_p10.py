import math,unittest
from shes.joint_certificate_p10 import frequency_envelope,physical_gate,relay_ok,run
class JointTests(unittest.TestCase):
 def test_frequency_constant_input(self):
  self.assertAlmostEqual(frequency_envelope(0.,2.,2.,.2,.2,2.),.1*(1-math.exp(-2)))
 def test_frequency_rejects_bad_interval(self):
  with self.assertRaises(ValueError):frequency_envelope(0.,2.,2.,1.,-1.,2.)
 def test_gate_rejects_missing_evidence(self):
  self.assertFalse(physical_gate({}))
 def test_gate_requires_all_evidence(self):
  d=dict.fromkeys(("phase_continuity_verified","switching_feasibility_verified",
   "relay_orientation_verified","installed_relay_settings_verified",
   "inverter_current_limit_calibrated","breaker_delays_calibrated"),True)
  self.assertTrue(physical_gate(d))
  d["relay_orientation_verified"]=False
  self.assertFalse(physical_gate(d))
 def test_counterfactual_backup_finite(self):
  self.assertIsInstance(relay_ok(100.,80.,40.,35.,.05,.2,2.,4.,.1,
    .7,1.,.04,0.,"full"),bool)
 def test_no_field_claim(self):
  row=lambda b:{"bus":b,"fault_resistance_ohm":.1,"candidate_terminal_currents":{
   role:{"currents":[{"terminal":1,"conductor":1,"current_a":a}]}
   for role,a in (("primary",100.),("backup",80.))}}
  src={"pin":"test","sha256":{},"results":[row(b) for b in ("60","83") for _ in range(3)]}
  result=run(src,draws=2)
  self.assertEqual(result["population"],36)
  self.assertEqual(result["physical_certificates_issued"],0)
  for t in result["tables"].values():
   for matrix in t.values():self.assertEqual(sum(matrix.values()),12)
if __name__=="__main__":unittest.main()
