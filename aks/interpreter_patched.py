"""
interpreter.py — Sovereign Interpreter for AkshayaLang
"""

from aks.lexer import tokenize
from aks.parser import Parser
from aks.ast import Block, ASTNode
from aks.runtime import Runtime
from aks.execution_context import ExecutionContext


class Interpreter:
    """
    The sovereign orchestrator of AkshayaLang.
    Parses → builds AST → runs it via Runtime and ExecutionContext.
    """

    def __init__(self, context=None, debug=False):
        self.context = context or ExecutionContext()
        self.runtime = Runtime(self.context)
        self.debug = debug

    def run(self, code: str):
        """
        Run raw .aks code: tokenize → parse → evaluate AST.

        Args:
            code (str): The source code string.

        Returns:
            Any: Result of final AST evaluation.
        """
        try:
            tokens = tokenize(code)
            if self.debug:
                print("[Tokens]", tokens)

            parser = Parser(tokens)
            node = parser.parse()
            if self.debug:
                print("[AST Root]", repr(node))

            if not isinstance(node, ASTNode):
                raise RuntimeError("Parsed root is not a valid AST node.")

            return self.runtime.execute(node)

        except Exception as e:
            raise RuntimeError(f"Interpreter Error: {e}")


if __name__ == "__main__":
    sample_code = """
    bind x to 10
    bind y to 5
    mirror x + y * 2
    """
    result = Interpreter(debug=True).run(sample_code)
    print("[Result]:", result)
