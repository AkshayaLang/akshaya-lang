"""
tests/test_parser.py

Unit tests for AkshayaLang parser — validates token stream and AST node creation.
"""

import unittest
from aks.parser import Parser
from aks.ast import Program, Assignment, BinaryOperation, Number, Variable


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_simple_assignment(self):
        code = "bind x to 5"
        program = self.parser.parse(code)
        self.assertIsInstance(program, Program)
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, Assignment)
        self.assertEqual(stmt.name, "x")
        self.assertIsInstance(stmt.expression, Number)
        self.assertEqual(stmt.expression.value, 5)

    def test_binary_expression(self):
        code = "bind result to 2 + 3"
        program = self.parser.parse(code)
        stmt = program.statements[0]
        self.assertIsInstance(stmt.expression, BinaryOperation)
        self.assertIsInstance(stmt.expression.left, Number)
        self.assertIsInstance(stmt.expression.right, Number)
        self.assertEqual(stmt.expression.operator, "+")

    def test_variable_reference(self):
        code = "bind y to x + 1"
        program = self.parser.parse(code)
        stmt = program.statements[0]
        self.assertIsInstance(stmt.expression.left, Variable)
        self.assertEqual(stmt.expression.left.name, "x")


if __name__ == "__main__":
    unittest.main()