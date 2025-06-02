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

    # ✅ Initialize execution context and load symbolic stdlib
    context = ExecutionContext()
    register_standard_library(context)

    # 🔁 Attach context to interpreter
    interpreter = Interpreter(context)

    buffer = ""
    while True:
        try:
            line = input("🪔 > ")
            if line.strip().lower() in {"exit", "quit"}:
                print("👋 Exiting AkshayaLang.")
                break
            if not line.strip():
                continue

            buffer += line + "\n"
            result = interpreter.run(buffer)
            if result is not None:
                print("🌀", result)
            buffer = ""  # reset after execution

        except Exception as e:
            traceback.print_exc()
            print("⚠️ Error:", e)
            buffer = ""  # reset on error


if __name__ == "__main__":
    start_repl()