"""
aks/runtime.py

Symbolic runtime core for AkshayaLang — integrates built-in logic and AST execution.
Merges RuntimeEnvironment utilities with AST-based symbolic evaluation.
"""

import sys
from aks.execution_context import ExecutionContext
from aks.ast import Program


class RuntimeError(Exception):
    """Custom error class for the AKS runtime."""
    pass


class RuntimeEnvironment:
    """Provides built-in functions and user global state."""
    def __init__(self):
        self.builtins = {
            "print": self._print,
            "input": self._input,
            "len": self._len,
            "type": self._type,
            "exit": self._exit,
            "int": self._int,
            "str": self._str,
            "float": self._float
        }
        self.user_globals = {}

    def get(self, name):
        if name in self.user_globals:
            return self.user_globals[name]
        if name in self.builtins:
            return self.builtins[name]
        raise RuntimeError(f"RuntimeError: '{name}' is not defined.")

    def set(self, name, value):
        self.user_globals[name] = value

    def _print(self, *args):
        print(*args)

    def _input(self, prompt=""):
        return input(prompt)

    def _len(self, value):
        try:
            return len(value)
        except Exception:
            raise RuntimeError(f"Object of type '{type(value)}' has no len()")

    def _type(self, value):
        return str(type(value).__name__)

    def _exit(self, code=0):
        sys.exit(code)

    def _int(self, value):
        try:
            return int(value)
        except Exception:
            raise RuntimeError(f"Cannot convert '{value}' to int")

    def _str(self, value):
        try:
            return str(value)
        except Exception:
            raise RuntimeError(f"Cannot convert '{value}' to str")

    def _float(self, value):
        try:
            return float(value)
        except Exception:
            raise RuntimeError(f"Cannot convert '{value}' to float")


class Runtime:
    """High-level runtime engine for executing .aks programs using AST + Environment."""
    def __init__(self, context=None):
        self.env = RuntimeEnvironment()
        self.context = context or ExecutionContext()
        self._inject_builtins()

    def _inject_builtins(self):
        for name, func in self.env.builtins.items():
            self.context.define_function(name, func)

    def execute(self, node):
        if not isinstance(node, Program):
            raise ValueError("Root node must be a Program")
        return node.evaluate(self.context)