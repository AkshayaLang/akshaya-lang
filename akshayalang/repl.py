"""
akshayalang/repl.py

Interactive REPL for AkshayaLang — allows live typing and execution of .aks code.
"""

import traceback
from aks.interpreter import Interpreter
from aks.execution_context import ExecutionContext
from aks.stdlib import register_standard_library


def start_repl():
    print("\n🔮 AkshayaLang REPL v1.0 — Type 'exit' to quit\n")

    # 🔧 Initialize a shared execution context and register built-in functions
    context = ExecutionContext()
    register_standard_library(context)

    # 🧠 Launch interpreter
    interpreter = Interpreter(context)

    buffer = ""
    while True:
        try:
            line = input("🪔 > ").strip()
            if not line:
                continue

            if line.lower() in {"exit", "quit"}:
                print("👋 Exiting AkshayaLang.")
                break

            buffer += line + "\n"
            result = interpreter.run(buffer)

            if result is not None:
                print("🌀", result)

            buffer = ""  # 🔄 Reset input buffer after execution

        except Exception as e:
            traceback.print_exc()
            print("⚠️ Error:", e)
            buffer = ""


if __name__ == "__main__":
    start_repl()