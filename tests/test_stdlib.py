"""
tests/test_stdlib.py

Unit tests for AkshayaLang standard library functions.
"""

import unittest
from aks.execution_context import ExecutionContext
from aks.stdlib import register_standard_library
from aks.types import AKSNumber, AKSString, AKSBoolean, AKSNull


class TestStdLib(unittest.TestCase):
    def setUp(self):
        self.context = ExecutionContext()
        self.lib = register_standard_library(self.context)

    def test_builtin_addition(self):
        result = self.context.call_function("add", [5, 7])
        self.assertEqual(result, 12)

    def test_type_function(self):
        result = self.context.call_function("type", [AKSNumber(42)])
        self.assertEqual(str(result), "Number")

    def test_string_concat(self):
        result = self.context.call_function("str", [AKSNumber(99)])
        self.assertIsInstance(result, AKSString)
        self.assertEqual(str(result), "99")

    def test_boolean_cast(self):
        result = self.context.call_function("bool", [AKSNumber(0)])
        self.assertIsInstance(result, AKSBoolean)
        self.assertFalse(bool(result))

    def test_null_return(self):
        result = self.context.call_function("null", [])
        self.assertIsInstance(result, AKSNull)

    def test_help_string(self):
        help_output = self.context.call_function("help", [])
        self.assertIn("Available built-in functions", str(help_output))


if __name__ == "__main__":
    unittest.main()