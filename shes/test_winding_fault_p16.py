import unittest
from shes.winding_fault_p16 import phasors
from shes.phase_topology_p14 import line_edges,reach
class Mock:
 NumConductors=2
 NumTerminals=2
 Currents=[1,2,3,4,-1,-2,-3,-4]
class P16Tests(unittest.TestCase):
 def test_signed_terminal_currents_not_magnitudes(self):
  self.assertEqual(phasors(Mock()),[[[1.,2.],[3.,4.]],[[-1.,-2.],[-3.,-4.]]])
 def test_wrong_current_vector_rejected(self):
  class Broken(Mock): Currents=[1,2]
  with self.assertRaises(ValueError):phasors(Broken())
 def test_transformer_without_transfer_is_not_phase_path(self):
  records=[{"name":"Line.a","kind":"line","enabled":True,
   "buses":["s.1","x.1"],"open_conductors":[]},
   {"name":"Transformer.r","kind":"transformer","enabled":True,
   "buses":["x.1","y.2"],"open_conductors":[]},
   {"name":"Line.b","kind":"line","enabled":True,
   "buses":["y.2","t.2"],"open_conductors":[]}]
  self.assertNotIn(("t",2),reach(line_edges(records),[("s",1)]))
if __name__=="__main__":unittest.main()
