# aks/tokens.py

from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    OPERATOR = auto()
    ASSIGN = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    COMMA = auto()
    EOF = auto()
    KEYWORD = auto()
    NEWLINE = auto()

# Keywords recognized by the language
KEYWORDS = {
    "let",
    "print",
    "if",
    "else",
    "while",
    "true",
    "false",
    "fn",
    "return",
}

# Set of valid single-character operators and punctuations
SINGLE_CHAR_TOKENS = {
    '=': TokenType.ASSIGN,
    '+': TokenType.OPERATOR,
    '-': TokenType.OPERATOR,
    '*': TokenType.OPERATOR,
    '/': TokenType.OPERATOR,
    '(': TokenType.LEFT_PAREN,
    ')': TokenType.RIGHT_PAREN,
    ',': TokenType.COMMA,
    '\n': TokenType.NEWLINE,
}