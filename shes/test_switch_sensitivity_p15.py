import unittest
from shes.switch_sensitivity_p15 import candidate_switches
from shes.phase_topology_p14 import line_edges,reach
class SwitchingTests(unittest.TestCase):
 def test_only_named_switches_selected(self):
  records=[{"name":"Line.l58","kind":"line","enabled":True},
   {"name":"Line.sw1","kind":"line","enabled":True},
   {"name":"Line.sw2","kind":"line","enabled":False},
   {"name":"Transformer.swfake","kind":"transformer","enabled":True}]
  self.assertEqual([r["name"] for r in candidate_switches(records)],["Line.sw1"])
 def test_disconnected_phase_does_not_follow_bus_adjacency(self):
  r={"name":"Line.sw1","kind":"line","enabled":True,"buses":["s.1.2","t.1.2"],
   "open_conductors":[[1,1]]}
  self.assertNotIn(("t",1),reach(line_edges([r]),[("s",1)]))
  self.assertIn(("t",2),reach(line_edges([r]),[("s",2)]))
 def test_phase_permutation_is_not_phase_identity(self):
  r={"name":"Line.sw1","kind":"line","enabled":True,"buses":["s.1.2","t.2.1"],
   "open_conductors":[]}
  self.assertIn(("t",2),reach(line_edges([r]),[("s",1)]))
  self.assertNotIn(("t",1),reach(line_edges([r]),[("s",1)]))
if __name__=="__main__":unittest.main()
