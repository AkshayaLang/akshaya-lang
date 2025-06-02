"""
tests/test_runtime.py

Unit tests for AkshayaLang runtime system — evaluates AST execution and value propagation.
"""

import unittest
from aks.runtime import Runtime
from aks.ast import Program, Number, Assignment, Variable, BinaryOperation


class TestRuntime(unittest.TestCase):
    def setUp(self):
        self.runtime = Runtime()

    def test_execute_single_assignment(self):
        ast = Program([
            Assignment("a", Number(42))
        ])
        result = self.runtime.execute(ast)
        self.assertEqual(self.runtime.global_context.get_variable("a"), 42)
        self.assertEqual(result, 42)

    def test_binary_operation_execution(self):
        ast = Program([
            Assignment("sum", BinaryOperation(Number(10), "+", Number(5)))
        ])
        result = self.runtime.execute(ast)
        self.assertEqual(result, 15)
        self.assertEqual(self.runtime.global_context.get_variable("sum"), 15)

    def test_variable_dependency(self):
        ast = Program([
            Assignment("x", Number(7)),
            Assignment("y", BinaryOperation(Variable("x"), "*", Number(2)))
        ])
        result = self.runtime.execute(ast)
        self.assertEqual(self.runtime.global_context.get_variable("y"), 14)
        self.assertEqual(result, 14)


if __name__ == '__main__':
    unittest.main()