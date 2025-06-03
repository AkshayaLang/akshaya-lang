# akshayalang/cli.py

import argparse
import logging
import sys
from aks.lexer import AKSLexer
from aks.parser import Parser
from aks.interpreter import Interpreter
from aks.execution_context import ExecutionContext

logger = logging.getLogger("AkshayaLang")
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def run(file_path: str, debug: bool = False):
    try:
        with open(file_path, 'r') as f:
            code = f.read()

        # Lexing
        lexer = AKSLexer(code)
        tokens = lexer.tokenize()

        # Parsing
        parser = Parser(tokens)
        ast_nodes = parser.parse()

        # Interpretation
        context = ExecutionContext()
        interpreter = Interpreter(context)
        for node in ast_nodes:
            result = interpreter.eval(node)
            if result is not None:
                print(result)

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        if debug:
            logger.exception("Runtime exception occurred")
        else:
            logger.error(f"Runtime error: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="AkshayaLang CLI Interpreter")
    parser.add_argument("script", help="Path to .aks file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logs")
    args = parser.parse_args()
    run(args.script, debug=args.debug)

if __name__ == "__main__":
    main()