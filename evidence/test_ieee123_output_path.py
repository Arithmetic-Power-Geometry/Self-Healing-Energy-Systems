"""Regression for OpenDSS compile changing cwd before result output."""
import json, os, pathlib, tempfile, types, unittest
from unittest.mock import patch
from run_ieee123_baseline import run

class FakeText:
 def __init__(self,root): self.root=root
 @property
 def Command(self): return ""
 @Command.setter
 def Command(self,value):
  if value.startswith("compile "): os.chdir(self.root)
class FakeSolution:
 Converged=True
 Iterations=3
 ControlIterations=1
class FakeCircuit:
 Name="ieee123"
 Solution=FakeSolution()
 AllBusVmagPu=[1.0]*278
 TotalPower=[-3400.0,-1900.0]
class FakeDSS:
 Version="mock-dss-for-path-regression"
 def __init__(self,root):
  self.Text=FakeText(root)
  self.Error=types.SimpleNamespace(Number=0,Description="")
  self.ActiveCircuit=FakeCircuit()
class PathRegression(unittest.TestCase):
 def test_compile_changes_cwd_but_output_stays_at_requested_location(self):
  initial=pathlib.Path.cwd()
  try:
   with tempfile.TemporaryDirectory() as temp:
    root=pathlib.Path(temp)
    feeder=root/"feeder"; feeder.mkdir()
    (feeder/"IEEE123Master.dss").write_text("clear\n")
    output=root/"result"/"baseline.json"
    d=types.SimpleNamespace(DSS=types.SimpleNamespace(NewContext=lambda:FakeDSS(feeder)))
    with patch.dict("sys.modules",{"dss":d}):
     run(feeder,output)
    self.assertTrue(output.exists())
    result=json.loads(output.read_text())
    self.assertEqual(result["status"],"PASS_STATIC_ONLY")
    self.assertEqual([s["node_count"] for s in result["scenarios"]],[278,278])
  finally:
   os.chdir(initial)
if __name__=="__main__":unittest.main()
