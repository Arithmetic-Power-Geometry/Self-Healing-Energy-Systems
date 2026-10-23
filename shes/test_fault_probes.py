import copy, unittest
from run_ieee123_fault_probes import choose_switch, choose_locations, read_fault_current

class FakeBus:
 Nodes=[1,2,3]
class FakeCircuit:
 ActiveBus=FakeBus()
 def SetActiveBus(self,name):self.name=name
class FakeDSS:
 ActiveCircuit=FakeCircuit()
class Tests(unittest.TestCase):
 def test_missing_location_fails_closed(self):
  with self.assertRaises(ValueError):choose_locations(FakeDSS(),{"150":"150"})
 def test_phase_filter(self):
  out=choose_locations(FakeDSS(),{"150":"150","60":"60","83":"83"})
  self.assertEqual([x["phases"] for x in out],[[1,2,3]]*3)
 def test_switch_is_existing_line(self):
  lines=[{"name":"B","from":"150","to":"5"},{"name":"A","from":"9","to":"10"}]
  sel=choose_switch(lines,[{"bus":"150"},{"bus":"60"},{"bus":"83"}])
  self.assertEqual(sel["name"],"A")
 def test_no_safe_candidate_fails(self):
  with self.assertRaises(ValueError):
   choose_switch([{"name":"X","from":"150","to":"60"}],
    [{"bus":"150"},{"bus":"60"}])
if __name__=="__main__":unittest.main()
