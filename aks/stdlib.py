"""
stdlib.py — AkshayaLang Symbolic Standard Library (Corelib v1.0)
"""

from aks.execution_context import ExecutionContext
from aks.types import AKSString, AKSNumber, AKSBoolean, AKSNull


class StandardLibrary:
    def __init__(self, context: ExecutionContext):
        self.context = context
        self._register_builtins()

    def _register_builtins(self):
        # Core I/O
        self.context.define_function("print", lambda *args: print("🖨️", *args))
        self.context.define_function("input", lambda prompt="": AKSString(input(prompt)))

        # Type coercion
        self.context.define_function("str", lambda x: AKSString(str(x)))
        self.context.define_function("int", lambda x: AKSNumber(int(x.value)) if hasattr(x, 'value') else AKSNumber(int(x)))
        self.context.define_function("float", lambda x: AKSNumber(float(x.value)) if hasattr(x, 'value') else AKSNumber(float(x)))
        self.context.define_function("bool", lambda x: AKSBoolean(bool(x)))

        # Symbolic utilities
        def mirror(*args):
            for arg in args:
                print("🪞", arg)
            return args[-1] if args else AKSNull()
        self.context.define_function("mirror", mirror)

        self.context.define_function("type", lambda x: AKSString(x.type_name()) if hasattr(x, "type_name") else AKSString(type(x).__name__))

        # Introspection
        self.context.define_function("whoami", lambda: AKSString("AkshayaLang v1.0 :: Sovereign Core"))
        self.context.define_function("null", lambda: AKSNull())

        # Exit
        self.context.define_function("exit", lambda: exit(0))
        
def register_standard_library(context: ExecutionContext):
        return StandardLibrary(context)