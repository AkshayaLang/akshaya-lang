"""
tokens.py — AkshayaLang Token System
"""

from enum import Enum, auto
from typing import Any, Optional


class TokenType(Enum):
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    DICT = auto()
    LIST = auto()

    ASSIGN = auto()
    COMMA = auto()
    COLON = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LPAREN = auto()
    RPAREN = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()

    NEWLINE = auto()
    EOF = auto()

    TO = auto()
    BIND = auto()
    RETURN = auto()
    MIRROR = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FN = auto()


KEYWORDS = {
    "mirror": TokenType.MIRROR,
    "print": TokenType.PRINT,
    "true": TokenType.BOOLEAN,
    "false": TokenType.BOOLEAN,
    "bind": TokenType.BIND,
    "to": TokenType.TO,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "return": TokenType.RETURN,
    "while": TokenType.WHILE,
    "fn": TokenType.FN,
}

SINGLE_CHAR_TOKENS = {
    "=": TokenType.ASSIGN,
    ",": TokenType.COMMA,
    ":": TokenType.COLON,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
}


class Token:
    def __init__(self, type_: TokenType, value: Any, position: Optional[tuple] = None):
        self.type = type_
        self.value = value
        self.position = position  # Optional: (line, column)

    def __repr__(self) -> str:
        return f"<Token type={self.type.name} value={repr(self.value)} pos={self.position}>"

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Token)
            and self.type == other.type
            and self.value == other.value
            and self.position == other.position
        )