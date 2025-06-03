"""
ast.py — AkshayaLang AST (Sovereign Refactored 10/10 Version)
"""

from aks.tokens import Token

# === Exception for Return Signals ===
class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


# === Base AST Node ===
class ASTNode:
    def evaluate(self, context):
        raise NotImplementedError("evaluate() not implemented.")

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


# === Literal Nodes ===
class NumberLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return self.value

    def __repr__(self):
        return f"NumberLiteral({self.value})"


class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return self.value

    def __repr__(self):
        return f"StringLiteral('{self.value}')"


class BooleanLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return self.value

    def __repr__(self):
        return f"BooleanLiteral({self.value})"


class ListLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

    def evaluate(self, context):
        return [el.evaluate(context) for el in self.elements]

    def __repr__(self):
        return f"ListLiteral({self.elements})"


class DictLiteral(ASTNode):
    def __init__(self, pairs):
        self.pairs = pairs  # list of (key_node, value_node)

    def evaluate(self, context):
        return {key.evaluate(context): value.evaluate(context) for key, value in self.pairs}

    def __repr__(self):
        return f"DictLiteral({self.pairs})"


class ObjectLiteral(ASTNode):
    def __init__(self, pairs):
        self.pairs = pairs  # list of (key, value)

    def evaluate(self, context):
        return {k: v.evaluate(context) for k, v in self.pairs}

    def __repr__(self):
        return f"ObjectLiteral({self.pairs})"


# === Identifier ===
class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        return context.get_variable(self.name)

    def __repr__(self):
        return f"Identifier('{self.name}')"


# === Binary and Unary Operations ===
class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self, context):
        l = self.left.evaluate(context)
        r = self.right.evaluate(context)
        ops = {
            '+': l + r,
            '-': l - r,
            '*': l * r,
            '/': l / r,
            '==': l == r,
            '!=': l != r,
            '<': l < r,
            '>': l > r,
            '<=': l <= r,
            '>=': l >= r,
            'and': l and r,
            'or': l or r
        }
        if self.operator in ops:
            return ops[self.operator]
        raise Exception(f"Unknown operator {self.operator}")

    def __repr__(self):
        return f"BinaryExpression({self.left}, '{self.operator}', {self.right})"


class UnaryExpression(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def evaluate(self, context):
        val = self.operand.evaluate(context)
        if self.operator == '-':
            return -val
        elif self.operator == 'not':
            return not val
        raise Exception(f"Unknown unary operator {self.operator}")

    def __repr__(self):
        return f"UnaryExpression('{self.operator}', {self.operand})"


# === Variable Binding & Assignment ===
class BindStatement(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def evaluate(self, context):
        value = self.expression.evaluate(context)
        context.set_variable(self.identifier.name, value)
        return value

    def __repr__(self):
        return f"Bind({self.name} = {self.expression})"


class AssignmentStatement(ASTNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def evaluate(self, context):
        if not context.has_variable(self.name):
            raise NameError(f"Variable '{self.name}' not defined")
        value = self.expression.evaluate(context)
        context.set_variable(self.name, value)
        return value

    def __repr__(self):
        return f"Assign({self.name} = {self.expression})"


# === Conditionals and Loops ===
class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def evaluate(self, context):
        if self.condition.evaluate(context):
            return self.then_branch.evaluate(context)
        elif self.else_branch:
            return self.else_branch.evaluate(context)
        return None

    def __repr__(self):
        return f"If({self.condition})"


class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def evaluate(self, context):
        result = None
        while self.condition.evaluate(context):
            result = self.body.evaluate(context)
        return result

    def __repr__(self):
        return f"While({self.condition})"


class ReturnStatement(ASTNode):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        raise ReturnSignal(self.value.evaluate(context))

    def __repr__(self):
        return f"Return({self.value})"


# === Function Support ===
class FunctionDeclaration(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def evaluate(self, context):
        context.set_variable(self.name, UserFunction(self.params, self.body))
        return None

    def __repr__(self):
        return f"FunctionDef({self.name})"


class FunctionCall(ASTNode):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

    def evaluate(self, context):
        func = self.callee.evaluate(context)
        args = [arg.evaluate(context) for arg in self.arguments]
        return func.call(args, context)

    def __repr__(self):
        return f"Call({self.callee})"


class UserFunction:
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def call(self, arguments, outer_context):
        local = outer_context.create_child()
        for name, value in zip(self.params, arguments):
            local.set_variable(name, value)
        try:
            self.body.evaluate(local)
        except ReturnSignal as rs:
            return rs.value
        return None

    def __repr__(self):
        return f"<UserFunction {self.params}>"


# === Block Statement ===
class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def evaluate(self, context):
        result = None
        for stmt in self.statements:
            result = stmt.evaluate(context)
        return result

    def __repr__(self):
        return f"Block({len(self.statements)} statements)"

# Add this to the bottom of ast.py

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements  # List[ASTNode]

    def evaluate(self, context):
        result = None
        for stmt in self.statements:
            result = stmt.evaluate(context)
        return result

class MirrorStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, context):
        value = self.expression.evaluate(context)
        print(f"🔮 {value}")
        return value
