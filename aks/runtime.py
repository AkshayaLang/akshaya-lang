# aks/runtime.py

from aks.execution_context import ExecutionContext
from aks.ast import (
    NumberLiteral, StringLiteral, BooleanLiteral, 
    Identifier, BinaryExpression, AssignmentStatement,
    FunctionCall, BindStatement, Program, 
    ListLiteral, DictLiteral
)

class Runtime:
    """
    The execution engine that evaluates AST nodes using the given context.
    This runtime supports scalar literals, lists, dicts, arithmetic, binding,
    and basic function calls.
    """

    def __init__(self, context=None):
        self.context = context or ExecutionContext()

    def execute(self, node):
        return node.evaluate(self.context)

# =====================
# Evaluation Extensions
# =====================

def _eval_number(self, context):
    return self.value

def _eval_string(self, context):
    return self.value

def _eval_boolean(self, context):
    return self.value

def _eval_identifier(self, context):
    return context.get_variable(self.name)

def _eval_binary_op(self, context):
    left = self.left.evaluate(context)
    right = self.right.evaluate(context)

    if self.operator == "+":
        return left + right
    elif self.operator == "-":
        return left - right
    elif self.operator == "*":
        return left * right
    elif self.operator == "/":
        return left / right
    elif self.operator == "%":
        return left % right
    else:
        raise ValueError(f"Unsupported operator '{self.operator}'")

def _eval_assignment(self, context):
    value = self.expression.evaluate(context)
    context.set_variable(self.name, value)
    return value

def _eval_bind(self, context):
    value = self.expression.evaluate(context)
    context.set_variable(self.identifier.name, value)
    return value

def _eval_call(self, context):
    args = [arg.evaluate(context) for arg in self.arguments]
    return context.call_function(self.name, args)

def _eval_program(self, context):
    result = None
    for stmt in self.statements:
        result = stmt.evaluate(context)
    return result

def _eval_list(self, context):
    return [element.evaluate(context) for element in self.elements]

def _eval_dict(self, context):
    return {k.value: v.evaluate(context) for k, v in self.pairs}

# ====================
# Bind evaluations
# ====================

NumberLiteral.evaluate = _eval_number
StringLiteral.evaluate = _eval_string
BooleanLiteral.evaluate = _eval_boolean
Identifier.evaluate = _eval_identifier
BinaryExpression.evaluate = _eval_binary_op
AssignmentStatement.evaluate = _eval_assignment
BindStatement.evaluate = _eval_bind
FunctionCall.evaluate = _eval_call
Program.evaluate = _eval_program
ListLiteral.evaluate = _eval_list
DictLiteral.evaluate = _eval_dict