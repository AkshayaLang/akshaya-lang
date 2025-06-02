"""
aks/execution_context.py

Manages variable bindings, function registry, and evaluation environment
for AkshayaLang (.aks) scripts.
"""


class ExecutionContext:
    """Symbolic execution context for .aks programs."""

    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.parent = parent

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get_variable(name)
        else:
            raise NameError(f"Variable '{name}' not defined")

    def define_function(self, name, func):
        self.functions[name] = func

    def call_function(self, name, args):
        if name in self.functions:
            return self.functions[name](*args)
        elif self.parent:
            return self.parent.call_function(name, args)
        else:
            raise NameError(f"Function '{name}' not defined")

    def create_child(self):
        return ExecutionContext(parent=self)