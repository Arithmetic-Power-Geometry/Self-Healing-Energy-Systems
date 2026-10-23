import copy, unittest
from run_ieee123_fault_probes import choose_switch, choose_locations, read_fault_current
from candidate_protection_paths import candidate_paths

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
 def test_candidate_boundaries_not_validated(self):
  paths=candidate_paths([{"name":"L1","from":"a","to":"b"},
   {"name":"L2","from":"b","to":"c"}],"a",["c"])
  self.assertEqual(paths["c"]["candidate_primary_boundary"],"L2")
  self.assertEqual(paths["c"]["candidate_backup_boundary"],"L1")
  self.assertFalse(paths["c"]["protection_zone_validated"])
if __name__=="__main__":unittest.main()
