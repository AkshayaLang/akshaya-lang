"""
lexer.py — Sovereign Tokenizer for AkshayaLang
"""

import re
from aks.tokens import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS


def tokenize(source_code):
    tokens = []
    line = 1
    col = 1
    pos = 0
    length = len(source_code)

    def advance(n=1):
        nonlocal pos, col
        pos += n
        col += n

    while pos < length:
        char = source_code[pos]

        # Skip whitespace
        if char in " \t":
            advance()
            continue

        # Newlines
        if char == "\n":
            line += 1
            col = 1
            pos += 1
            continue

        # Single-char tokens
        if char in SINGLE_CHAR_TOKENS:
            token = Token(SINGLE_CHAR_TOKENS[char], char, (line, col))
            print(f"[DEBUG] Tokenized: {token.type} - {token.value}")
            tokens.append(token)
            advance()
            continue

        # Strings
        if char == '"':
            end = pos + 1
            while end < length and source_code[end] != '"':
                if source_code[end] == "\n":
                    break
                end += 1
            string_val = source_code[pos + 1:end]
            tokens.append(Token(TokenType.STRING, string_val, (line, col)))
            advance(end - pos + 1)
            continue

        # Numbers
        number_match = re.match(r'\d+(\.\d+)?', source_code[pos:])
        if number_match:
            val = float(number_match.group())
            tokens.append(Token(TokenType.NUMBER, val, (line, col)))
            advance(len(number_match.group()))
            continue

        # Identifiers or Keywords
        id_match = re.match(r'[A-Za-z_][A-Za-z0-9_]*', source_code[pos:])
        if id_match:
            val = id_match.group()
            token_type = KEYWORDS.get(val, TokenType.IDENTIFIER)
            token = Token(token_type, val, (line, col))
            print(f"[DEBUG] Tokenized: {token.type} - {token.value}")
            tokens.append(token)
            advance(len(val))
            continue

        # Unknown character
        raise SyntaxError(f"Unexpected character '{char}' at line {line}, column {col}")

    tokens.append(Token(TokenType.EOF, None, (line, col)))
    return tokens