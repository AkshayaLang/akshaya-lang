# aks/context.py

class ExecutionContext:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Undefined variable '{name}'")

    def exists(self, name):
        return name in self.variables or (self.parent and self.parent.exists(name))

    def clone(self):
        # Creates a shallow copy of the context for safe evaluation
        ctx = ExecutionContext(self.parent)
        ctx.variables = self.variables.copy()
        return ctx