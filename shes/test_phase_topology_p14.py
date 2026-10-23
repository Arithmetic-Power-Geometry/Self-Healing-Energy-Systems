import unittest
from shes.phase_topology_p14 import split_bus,line_edges,reach,audit_records
def el(name,a,b,kind="line",enabled=True,opens=()):
 return {"name":name,"kind":kind,"buses":[a,b],"enabled":enabled,
         "open_conductors":[list(v) for v in opens]}
class PhaseTopologyTests(unittest.TestCase):
 def test_conductor_permutation_is_not_name_equivalence(self):
  g=line_edges([el("Line.swap","s.1.2","t.2.1")])
  self.assertIn(("t",2),reach(g,[("s",1)]))
  self.assertNotIn(("t",1),reach(g,[("s",1)]))
 def test_open_phase_breaks_path_but_not_other_phase(self):
  g=line_edges([el("Line.a","s.1.2","t.1.2",opens=[(1,1)])])
  self.assertNotIn(("t",1),reach(g,[("s",1)]))
  self.assertIn(("t",2),reach(g,[("s",2)]))
 def test_disabled_line_does_not_conduct(self):
  self.assertEqual(len(line_edges([el("Line.a","s.1","t.1",enabled=False)])),0)
 def test_transformer_adjacency_false_continuity(self):
  rs=[el("Line.a","s.1","x.1"),el("Transformer.reg","x.1","y.2","transformer"),
      el("Line.b","y.2","t.2")]
  out=audit_records(rs,"s",("t",))["t"]
  self.assertTrue(out["element_adjacency_reachable"])
  self.assertEqual(out["line_only_phase_nodes_reached"],[])
  self.assertFalse(out["transformer_transfer_verified"])
  self.assertFalse(out["installed_relay_and_ct_orientation_verified"])
 def test_mismatched_conductor_counts_fail_closed(self):
  self.assertEqual(len(line_edges([el("Line.bad","s.1.2","t.1")])),0)
 def test_phase_zero_is_not_energized_phase(self):
  self.assertEqual(len(line_edges([el("Line.n","s.0","t.0")])),0)
if __name__=="__main__":unittest.main()
