import unittest
from feeder_topology import graph_from_elements,shortest_path,candidate_boundaries
from terminal_current_model import uncertainty_envelope
class TopologyTests(unittest.TestCase):
 def test_transformer_bridges_line_only_gap(self):
  elements=[{"name":"Line.a","kind":"line","buses":["source.1","mid.1"]},
    {"name":"Transformer.reg","kind":"transformer","buses":["mid.1","down.1"]},
    {"name":"Line.b","kind":"line","buses":["down.1","target.1"]}]
  paths=candidate_boundaries(graph_from_elements(elements),"source",["target"])
  self.assertTrue(paths["target"]["reachable_in_element_graph"])
  self.assertEqual(paths["target"]["candidate_primary_element"],"Line.b")
  self.assertEqual(paths["target"]["candidate_backup_element"],"Transformer.reg")
  self.assertFalse(paths["target"]["installed_relay_verified"])
 def test_open_element_is_not_connected(self):
  g=graph_from_elements([{"name":"Line.a","kind":"line","buses":["s","t"],"enabled":False}])
  self.assertIsNone(shortest_path(g,"s","t"))
 def test_missing_path_does_not_fabricate_relays(self):
  r=candidate_boundaries(graph_from_elements([]),"s",["t"])["t"]
  self.assertIsNone(r["candidate_primary_element"])
 def test_invalid_uncertainty(self):
  with self.assertRaises(ValueError):uncertainty_envelope(1,1,gmin=1.1)
 def test_uncertainty_is_explicitly_hypothetical(self):
  d=uncertainty_envelope(100,80,.7,.04)
  self.assertEqual(d["primary_a"],[70,100])
  self.assertFalse(d["calibrated_to_equipment"])
if __name__=="__main__":unittest.main()
