#!/usr/bin/env python3
"""Dependency and provenance preflight tests; no OpenDSS needed."""
import pathlib, tempfile, unittest
from run_ieee123_baseline import deps

class DependencyTests(unittest.TestCase):
    def test_all_redirects(self):
        with tempfile.TemporaryDirectory() as t:
            root=pathlib.Path(t)
            (root/"IEEE123Master.dss").write_text("clear\nRedirect IEEELinecodes.DSS\nRedirect IEEE123Regulators.DSS\nRedirect IEEE123Loads.DSS\n")
            for name in ["IEEELinecodes.DSS","IEEE123Regulators.DSS","IEEE123Loads.DSS"]:
                (root/name).write_text("! fixture\n")
            found=deps(root,"IEEE123Master.dss")
            self.assertEqual(len(found),4)
    def test_missing_case_sensitive_file_fails(self):
        with tempfile.TemporaryDirectory() as t:
            root=pathlib.Path(t)
            (root/"IEEE123Master.dss").write_text("Redirect IEEELinecodes.DSS\n")
            (root/"IEEELineCodes.DSS").write_text("! mismatch\n")
            with self.assertRaises(FileNotFoundError):
                deps(root,"IEEE123Master.dss")
    def test_escaping_path_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root=pathlib.Path(t)
            (root/"IEEE123Master.dss").write_text("Redirect ../outside.dss\n")
            with self.assertRaises(ValueError):
                deps(root,"IEEE123Master.dss")
    def test_cycle_safe(self):
        with tempfile.TemporaryDirectory() as t:
            root=pathlib.Path(t)
            (root/"IEEE123Master.dss").write_text("Redirect a.dss\n")
            (root/"a.dss").write_text("Redirect IEEE123Master.dss\n")
            self.assertEqual(len(deps(root,"IEEE123Master.dss")),2)

if __name__=="__main__":unittest.main()
