"""
execution_context.py — AkshayaLang Sovereign Execution Environment
"""

class AkshayaLangError(Exception):
    """Base exception for AkshayaLang runtime errors."""
    pass


class ExecutionContext:
    """
    Represents the runtime scope.
    Handles variables, functions, and inheritance from parent scopes.
    """

    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.parent = parent
        self._initialize_builtins()

    def _initialize_builtins(self):
        self.functions.update({
            "print": lambda *args: print(*args),
            "len": lambda x: len(x) if hasattr(x, '__len__') else 0,
            "type": lambda x: str(type(x).__name__),
        })

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_variable(name)
        raise NameError(f"Variable '{name}' is not defined.")

    def set_variable(self, name, value):
        self.variables[name] = value

    def has_variable(self, name):
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has_variable(name)
        return False

    def define_function(self, name, func):
        self.functions[name] = func

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise NameError(f"Function '{name}' is not defined.")

    def call_function(self, name, arguments):
        func = self.get_function(name)
        return func(*arguments)

    def create_child(self):
        return ExecutionContext(parent=self)

    def reset(self):
        self.variables.clear()
        self.functions.clear()
