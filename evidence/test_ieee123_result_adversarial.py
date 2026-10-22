#!/usr/bin/env python3
"""Adversarial fixtures for independent IEEE123 result validator; no electrical simulation."""
import copy
import unittest
from validate_ieee123_result import validate

BASE = {
 "status":"PASS_STATIC_ONLY","feeder":"IEEE123",
 "gfm_dynamics_validated":False,"protection_validated":False,"emt_validated":False,
 "sha256":{"IEEE123Master.dss":"a"*64},
 "scenarios":[
  {"scenario":"static_off","converged":True,"node_count":250,"vmin_pu":0.92,"vmax_pu":1.04,"total_power_kw_kvar":[-3500.0,-1200.0]},
  {"scenario":"static_controls","converged":True,"node_count":250,"vmin_pu":0.93,"vmax_pu":1.05,"total_power_kw_kvar":[-3500.0,-1200.0]}
 ]
}
class TestIndependentValidator(unittest.TestCase):
 def test_synthetic_valid_fixture(self):
  self.assertTrue(validate(copy.deepcopy(BASE)))
 def test_reject_unconverged(self):
  x=copy.deepcopy(BASE);x["scenarios"][0]["converged"]=False
  with self.assertRaises(ValueError):validate(x)
 def test_reject_false_safety_claim(self):
  x=copy.deepcopy(BASE);x["protection_validated"]=True
  with self.assertRaises(ValueError):validate(x)
 def test_reject_nonfinite_voltage(self):
  x=copy.deepcopy(BASE);x["scenarios"][0]["vmax_pu"]=float("nan")
  with self.assertRaises(ValueError):validate(x)
 def test_reject_duplicate_scenarios(self):
  x=copy.deepcopy(BASE);x["scenarios"][1]["scenario"]="static_off"
  with self.assertRaises(ValueError):validate(x)
 def test_reject_bad_source_hash(self):
  x=copy.deepcopy(BASE);x["sha256"]["IEEE123Master.dss"]="invalid"
  with self.assertRaises(ValueError):validate(x)
 def test_reject_too_few_nodes(self):
  x=copy.deepcopy(BASE);x["scenarios"][0]["node_count"]=2
  with self.assertRaises(ValueError):validate(x)
 def test_reject_missing_validation_flags(self):
  x=copy.deepcopy(BASE);del x["emt_validated"]
  with self.assertRaises(ValueError):validate(x)
 def test_reject_inverted_voltage_extrema(self):
  x=copy.deepcopy(BASE);x["scenarios"][0]["vmin_pu"]=1.10
  with self.assertRaises(ValueError):validate(x)
 def test_reject_boolean_power(self):
  x=copy.deepcopy(BASE);x["scenarios"][0]["total_power_kw_kvar"]=[True,0.0]
  with self.assertRaises(ValueError):validate(x)
 def test_reject_nonfinite_power(self):
  x=copy.deepcopy(BASE);x["scenarios"][1]["total_power_kw_kvar"]=[float("inf"),0.0]
  with self.assertRaises(ValueError):validate(x)
if __name__=="__main__":unittest.main()
