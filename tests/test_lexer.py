"""
tests/test_lexer.py

Unit tests for AkshayaLang lexer — ensures correct tokenization.
"""

import unittest
from aks.lexer import tokenize


class TestLexer(unittest.TestCase):
    def test_tokenize_numbers_and_identifiers(self):
        code = "bind a to 123"
        tokens = tokenize(code)
        types = [t.type for t in tokens]
        self.assertIn("ID", types)
        self.assertIn("NUMBER", types)

    def test_tokenize_arithmetic(self):
        code = "x + y - 3 * 5 / z"
        tokens = tokenize(code)
        token_map = {t.type for t in tokens}
        expected = {"ID", "PLUS", "MINUS", "STAR", "SLASH", "NUMBER"}
        self.assertTrue(expected.issubset(token_map))

    def test_string_token(self):
        code = 'bind name to "Akshaya"'
        tokens = tokenize(code)
        self.assertTrue(any(t.type == "STRING" and t.value == "Akshaya" for t in tokens))

    def test_invalid_character(self):
        with self.assertRaises(RuntimeError):
            tokenize("x = 5 $")


if __name__ == "__main__":
    unittest.main()