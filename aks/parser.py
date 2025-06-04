# parser.py — Final

from aks.tokens import Token, TokenType
from aks.ast import (
    ASTNode, MirrorStatement, BindStatement, BinaryExpression, UnaryExpression,
    NumberLiteral, StringLiteral, BooleanLiteral, Identifier,
    FunctionCall, ListLiteral, DictLiteral, FunctionDeclaration,
    IfStatement, WhileStatement, ReturnStatement, Block
)


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        statements = []
        while not self._match("EOF"):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        return Block(statements)

    def _parse_statement(self):
        if self._match("MIRROR"):
            expr = self._parse_expression()
            return MirrorStatement(expr)
        if self._match("BIND"):
            return self._parse_bind_statement()
        if self._match("FN"):
            return self._parse_function_declaration()
        if self._match("IF"):
            return self._parse_if_statement()
        if self._match("WHILE"):
            return self._parse_while_statement()
        if self._match("RETURN"):
            return self._parse_return_statement()
        return self._parse_expression()

    def _parse_bind_statement(self):
        name = self._consume("IDENTIFIER", "Expected variable name after 'bind'")
        self._consume("TO", "Expected 'to' after variable name")
        expr = self._parse_expression()
        return BindStatement(Identifier(name.value), expr)

    def _parse_function_declaration(self):
        name = self._consume("IDENTIFIER", "Expected function name")
        self._consume("LPAREN", "Expected '(' after function name")
        params = []
        if not self._check("RPAREN"):
            params.append(self._consume("IDENTIFIER", "Expected parameter").value)
            while self._match("COMMA"):
                params.append(self._consume("IDENTIFIER", "Expected parameter").value)
        self._consume("RPAREN", "Expected ')' after parameters")
        body = self._parse_block()
        return FunctionDeclaration(name.value, params, body)

    def _parse_if_statement(self):
        condition = self._parse_expression()
        then_branch = self._parse_block()
        else_branch = None
        if self._match("ELSE"):
            else_branch = self._parse_block()
        return IfStatement(condition, then_branch, else_branch)

    def _parse_while_statement(self):
        condition = self._parse_expression()
        body = self._parse_block()
        return WhileStatement(condition, body)

    def _parse_return_statement(self):
        value = self._parse_expression()
        return ReturnStatement(value)

    def _parse_block(self):
        self._consume("LBRACE", "Expected '{' to start block")
        statements = []
        while not self._check("RBRACE") and not self._is_at_end():
            statements.append(self._parse_statement())
        self._consume("RBRACE", "Expected '}' to close block")
        return Block(statements)

    def _parse_expression(self):
        return self._parse_binary_expression()

    def _parse_binary_expression(self):
        expr = self._parse_unary_expression()
        while self._check("PLUS") or self._check("MINUS") or self._check("STAR") or self._check("SLASH"):
            op_token = self._advance()
            op = op_token.value
            right = self._parse_unary_expression()
            expr = BinaryExpression(expr, op, right)
        return expr

    def _parse_unary_expression(self):
        if self._check("MINUS"):
            op = self._advance().value
            operand = self._parse_primary()
            return UnaryExpression(op, operand)
        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        token = self._advance()

        if token.type == TokenType.NUMBER:
            return NumberLiteral(float(token.value))

        if token.type == TokenType.STRING:
            return StringLiteral(token.value)

        if token.type == TokenType.IDENTIFIER:
            return Identifier(token.value)
        
        if token.type == TokenType.LPAREN:
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        if token.type == TokenType.LBRACE:
            pairs = []
            while not self._check(TokenType.RBRACE) and not self._is_at_end():
                key_token = self._advance()
                if key_token.type != TokenType.IDENTIFIER and key_token.type != TokenType.STRING:
                    raise ParserError(f"Expected identifier or string as dictionary key, got: {key_token.type}")
                
                self._consume(TokenType.COLON, "Expected ':' after dictionary key")
                value_expr = self._parse_expression()

                if key_token.type == TokenType.STRING:
                    key_node = StringLiteral(key_token.value)
                else:
                    key_node = StringLiteral(key_token.value)  # force identifier to string

                pairs.append((key_node, value_expr))

                if not self._check(TokenType.RBRACE):
                    self._consume(TokenType.COMMA, "Expected ',' or '}' in dictionary literal")

            self._consume(TokenType.RBRACE, "Expected '}' to close dictionary literal")
            return DictLiteral(pairs)

        if token.type == TokenType.BOOLEAN:
            return BooleanLiteral(token.value == "true")

        raise ParserError(f"Unexpected token: {token.type}")
        

    def _parse_dict_literal(self):
        pairs = []
        while not self._check("RBRACE") and not self._is_at_end():
            key_token = self._advance()
            if key_token.type == "IDENTIFIER":
                key_node = Identifier(key_token.value)
            elif key_token.type == "STRING":
                key_node = StringLiteral(key_token.value)
            else:
                raise ParserError("Dictionary keys must be identifiers or strings")

            self._consume("COLON", "Expected ':' after key")
            value_node = self._parse_expression()
            pairs.append((key_node, value_node))
            if not self._check("RBRACE"):
                self._consume("COMMA", "Expected ',' between key-value pairs")
        self._consume("RBRACE", "Expected '}' to close dictionary")
        return DictLiteral(pairs)

    # ====== Helpers ======

    def _match(self, expected_type, expected_value=None):
        if self._check(expected_type, expected_value):
            self._advance()
            return True
        return False

    def _check(self, expected_type, expected_value=None):
        if self._is_at_end():
            return False
        token = self._peek()
        if isinstance(expected_type, str):
            type_match = token.type == expected_type or \
                         (hasattr(token.type, "name") and token.type.name == expected_type)
        else:
            type_match = token.type == expected_type
        if not type_match:
            return False
        if expected_value is not None and token.value != expected_value:
            return False
        return True

    def _consume(self, expected_type, message):
        if self._check(expected_type):
            return self._advance()
        raise ParserError(message)

    def _advance(self):
        if not self._is_at_end():
            self.position += 1
        return self._previous()

    def _peek(self):
        return self.tokens[self.position]

    def _previous(self):
        return self.tokens[self.position - 1]

    def _is_at_end(self):
        return self._peek().type == "EOF"