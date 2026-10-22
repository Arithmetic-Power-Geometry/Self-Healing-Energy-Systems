#!/usr/bin/env python3
"""Regression guard for DSS-Python Text.Command property API (no solver needed)."""
import ast
import pathlib
import unittest

SOURCE = pathlib.Path(__file__).with_name("run_ieee123_baseline.py")

class TestDssCommandApi(unittest.TestCase):
    def test_no_callable_text_command(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        calls = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "Command"
            and isinstance(node.func.value, ast.Attribute)
            and node.func.value.attr == "Text"
        ]
        self.assertFalse(calls, "DSS-Python Text.Command is a settable property, not a callable")

    def test_stale_result_removed_before_solver(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        run_fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "run")
        source = ast.get_source_segment(SOURCE.read_text(encoding="utf-8"), run_fn)
        self.assertIn("output.unlink(missing_ok=True)", source)
        self.assertLess(source.index("output.unlink(missing_ok=True)"), source.index("from dss import DSS"))

    def test_convergence_checked_before_voltage_approval(self):
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn('if not ok:', source)
        self.assertLess(source.index('if not ok:'), source.index('if not v or any('))

    def test_assignments_exist(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        assignments = [
            target for node in ast.walk(tree)
            if isinstance(node, (ast.Assign, ast.AnnAssign))
            for target in (node.targets if isinstance(node, ast.Assign) else [node.target])
            if isinstance(target, ast.Attribute)
            and target.attr == "Command"
            and isinstance(target.value, ast.Attribute)
            and target.value.attr == "Text"
        ]
        self.assertGreaterEqual(len(assignments), 2)

if __name__ == "__main__":
    unittest.main()
