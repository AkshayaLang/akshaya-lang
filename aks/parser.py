"""
aks/parser.py

Final production-grade parser for AkshayaLang.
Tokenizes input and constructs AST (Program, Assignment, BinaryOperation, etc.).
"""

from aks.lexer import tokenize, Token
from aks.ast import Program, Number, String, Variable, Assignment, FunctionCall, BinaryOperation, BooleanLiteral


class Parser:
    def __init__(self):
        self.tokens = []
        self.position = 0

    def parse(self, code):
        self.tokens = tokenize(code)
        self.position = 0
        statements = []

        while not self._eof():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)

        return Program(statements)

    def _parse_statement(self):
        token = self._peek()

        if token.type == "ID" and token.value == "bind":
            return self._parse_bind_statement()
        elif token.type == "ID":
            return self._parse_assignment_or_call()
        elif token.type == "NEWLINE":
            self._advance()
            return None
        else:
            # FINAL ADDITION: allow top-level expressions
            return self._parse_expression()

    def _parse_bind_statement(self):
        self._consume("ID")  # 'bind'
        name_token = self._consume("ID")
        to_token = self._consume("ID")
        if to_token.value != "to":
            raise SyntaxError("Expected 'to' after variable name in bind statement")
        expr = self._parse_expression()
        return Assignment(name=name_token.value, expression=expr)

    def _parse_assignment_or_call(self):
        name = self._consume("ID").value

        if self._match("ASSIGN"):
            expr = self._parse_expression()
            return Assignment(name=name, expression=expr)

        elif self._check("LPAREN"):
            self._consume("LPAREN")
            args = []
            if not self._check("RPAREN"):
                args.append(self._parse_expression())
                while self._match("COMMA"):
                    args.append(self._parse_expression())
            self._consume("RPAREN")
            return FunctionCall(name=name, arguments=args)

        else:
            # support symbolic: mirror a + b
            arg = self._parse_expression()
            return FunctionCall(name=name, arguments=[arg])

    def _parse_expression(self):
        return self._parse_term()

    def _parse_term(self):
        expr = self._parse_factor()

        while self._match("PLUS") or self._match("MINUS"):
            operator = self.tokens[self.position - 1].value
            right = self._parse_factor()
            expr = BinaryOperation(left=expr, operator=operator, right=right)

        return expr

    def _parse_factor(self):
        expr = self._parse_primary()

        while self._match("STAR") or self._match("SLASH"):
            operator = self.tokens[self.position - 1].value
            right = self._parse_primary()
            expr = BinaryOperation(left=expr, operator=operator, right=right)

        return expr

    def _parse_primary(self):
        token = self._peek()
    
        if token.type == "NUMBER":
            return Number(value=self._advance().value)
        elif token.type == "STRING":
            return String(value=self._advance().value)
        elif token.type == "BOOLEAN":
            return BooleanLiteral(value=self._advance().value)
        elif token.type == "ID":
            return Variable(name=self._advance().value)
        else:
            raise SyntaxError(f"Unexpected token in expression: {token}")

    def _peek(self):
        return self.tokens[self.position] if not self._eof() else Token("EOF", "", (0, 0))

    def _advance(self):
        self.position += 1
        return self.tokens[self.position - 1]

    def _check(self, token_type):
        return not self._eof() and self.tokens[self.position].type == token_type

    def _match(self, token_type):
        if self._check(token_type):
            self._advance()
            return True
        return False

    def _consume(self, token_type):
        if self._check(token_type):
            return self._advance()
        raise SyntaxError(f"Expected {token_type}, got {self._peek().type}")

    def _eof(self):
        return self.position >= len(self.tokens)