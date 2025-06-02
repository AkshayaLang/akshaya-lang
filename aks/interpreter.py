"""
aks/interpreter.py

Final production-grade interpreter for AkshayaLang.
Parses, evaluates, and runs .aks code using Parser → AST → Runtime.
Delegates logic to AST nodes and ExecutionContext for modular execution.
"""

from aks.parser import Parser
from aks.runtime import Runtime
from aks.ast import Program
from aks.execution_context import ExecutionContext


class Interpreter:
    """The orchestrator class for evaluating .aks source code."""

    def __init__(self, context=None):
        self.parser = Parser()
        self.runtime = Runtime(context or ExecutionContext())

    def run(self, code):
        """
        Run raw .aks code: parse → execute AST.

        Args:
            code (str): The raw source code as string.

        Returns:
            Any: Result of the final expression in the program.
        """
        ast = self.parser.parse(code)
        if not isinstance(ast, Program):
            raise RuntimeError("Invalid AST root. Must be a Program node.")
        return self.runtime.execute(ast)


if __name__ == "__main__":
    code = """
    bind a to 10
    bind b to 20
    mirror a + b
    """
    output = Interpreter().run(code)
    print("Result:", output)