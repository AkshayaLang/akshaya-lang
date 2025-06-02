"""
aks/lexer.py

Production-grade lexer for AkshayaLang.
Converts raw code into a list of tokens using regular expressions.
"""

import re

TOKEN_REGEX = [
    ("NUMBER",      r'\d+(\.\d+)?'),
    ("STRING",      r'".*?"|\'.*?\''),
    ("IDENTIFIER",  r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("ASSIGN",      r'='),
    ("PLUS",        r'\+'),
    ("MINUS",       r'-'),
    ("STAR",        r'\*'),
    ("SLASH",       r'/'),
    ("LPAREN",      r'\('),
    ("RPAREN",      r'\)'),
    ("COMMA",       r','),
    ("NEWLINE",     r'\n'),
    ("SKIP",        r'[ \t]+'),
    ("MISMATCH",    r'.'),
]

class Token:
    def __init__(self, type_, value, position):
        self.type = type_
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.position})"


class AKSLexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.line = 1
        self.column = 1

    def tokenize(self):
        pattern = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_REGEX)
        regex = re.compile(pattern)
        for match in regex.finditer(self.code):
            kind = match.lastgroup
            value = match.group()
            position = (self.line, self.column)

            if kind == "NUMBER":
                value = float(value) if '.' in value else int(value)
                self.tokens.append(Token("NUMBER", value, position))
            elif kind == "STRING":
                self.tokens.append(Token("STRING", value.strip('"\''), position))
            elif kind == "IDENTIFIER":
                if value == "true":
                    self.tokens.append(Token("BOOLEAN", True, position))
                elif value == "false":
                    self.tokens.append(Token("BOOLEAN", False, position))
                else:
                    self.tokens.append(Token("ID", value, position))
            elif kind in {"ASSIGN", "PLUS", "MINUS", "STAR", "SLASH", "LPAREN", "RPAREN", "COMMA"}:
                self.tokens.append(Token(kind, value, position))
            elif kind == "NEWLINE":
                self.line += 1
                self.column = 1
                continue
            elif kind == "SKIP":
                pass
            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected character {value!r} at line {self.line}, column {self.column}")

            self.column += len(match.group())  # ✅ always use original string length

        return self.tokens


def tokenize(code):
    """Entry function to tokenize raw code."""
    return AKSLexer(code).tokenize()