"""
aks/stdlib.py

Symbolic standard library for AkshayaLang.
Defines and registers built-in functions for runtime environment.
"""

from aks.execution_context import ExecutionContext
from aks.types import AKSString, AKSNumber, AKSBoolean, AKSNull


class StandardLibrary:
    def __init__(self, context: ExecutionContext):
        self.context = context
        self._register_builtins()

    def _register_builtins(self):
        self.context.define_function("print", lambda *args: print("🖨️", *args))
        self.context.define_function("input", lambda prompt="": input(prompt))

        def symbolic_len(x):
            try:
                if hasattr(x, '__len__'):
                    return len(x)
                if hasattr(x, 'value'):
                    return len(str(x.value))
                return len(str(x))
            except Exception:
                return 0

        self.context.define_function("len", symbolic_len)

        self.context.define_function(
            "type",
            lambda x: AKSString(x.type_name()) if hasattr(x, "type_name") else AKSString(type(x).__name__)
        )

        # Type coercion
        self.context.define_function("str", lambda x: AKSString(str(x)))
        self.context.define_function("int", lambda x: AKSNumber(int(x.value)) if hasattr(x, 'value') else AKSNumber(int(x)))
        self.context.define_function("float", lambda x: AKSNumber(float(x.value)) if hasattr(x, 'value') else AKSNumber(float(x)))
        self.context.define_function("bool", lambda x: AKSBoolean(bool(x)))

        # ✅ MIRROR — symbolic, flexible, returns last value
        def mirror(*args):
            for arg in args:
                print("🪞", arg)
            return args[-1] if args else AKSNull()

        self.context.define_function("mirror", mirror)

        self.context.define_function("exit", lambda: exit(0))
        self.context.define_function("null", lambda: AKSNull())

        # Introspection
        self.context.define_function("whoami", lambda: list(self.context.variables.keys()))
        self.context.define_function("symbols", lambda: list(self.context.functions.keys()))

        self.context.define_function("help", self._help)

    def _help(self):
        return AKSString("""
Available built-in functions:
- print(...): output values
- mirror(...): symbolic echo + return
- input(prompt): user input
- len(x): length
- type(x): symbolic type name
- str(x), int(x), float(x), bool(x): conversions
- null(): symbolic null
- exit(): end program
- whoami(): list bound variables
- symbols(): list functions
- help(): this message
""")


def register_standard_library(context: ExecutionContext):
    return StandardLibrary(context)