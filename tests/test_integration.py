"""
tests/test_integration.py

End-to-end integration test: full AkshayaLang source → Lexer → Parser → AST → Runtime.
"""

import unittest
from aks.interpreter import Interpreter


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_basic_script_execution(self):
        script = """
        bind a to 10
        bind b to 5
        bind c to a + b * 2
        mirror c
        """
        result = self.interpreter.run(script)
        self.assertEqual(result, 20)

    def test_string_and_type_cast(self):
        script = """
        bind name to "Siva"
        bind x to 108
        bind label to str(x)
        mirror label
        """
        result = self.interpreter.run(script)
        self.assertEqual(str(result), "108")

    def test_nested_function_call(self):
        script = """
        print("The result is:")
        mirror 2 + 3 * 4
        """
        result = self.interpreter.run(script)
        self.assertEqual(result, 14)


if __name__ == "__main__":
    unittest.main()