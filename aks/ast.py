from abc import ABC, abstractmethod


class ASTNode(ABC):
    """Base class for all AST nodes."""
    @abstractmethod
    def evaluate(self, context):
        pass


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def evaluate(self, context):
        result = None
        for stmt in self.statements:
            result = stmt.evaluate(context)
        return result


class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return self.value


class String(ASTNode):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return self.value


class BooleanLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return self.value


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        return context.get_variable(self.name)


class Assignment(ASTNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def evaluate(self, context):
        value = self.expression.evaluate(context)
        context.set_variable(self.name, value)
        return value


class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self, context):
        left_val = self.left.evaluate(context)
        right_val = self.right.evaluate(context)

        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        elif self.operator == '*':
            return left_val * right_val
        elif self.operator == '/':
            return left_val / right_val
        else:
            raise Exception(f"Unsupported operator: {self.operator}")


class FunctionCall(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def evaluate(self, context):
        evaluated_args = [arg.evaluate(context) for arg in self.arguments]
        return context.call_function(self.name, evaluated_args)