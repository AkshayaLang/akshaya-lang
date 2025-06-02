# aks/memory.py

class Memory:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent  # Support for nested scopes (future)

    def set(self, name, value):
        """Set a variable in current scope."""
        self.variables[name] = value

    def get(self, name):
        """Retrieve variable, searching up scope chain if needed."""
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' not found")

    def exists(self, name):
        """Check if a variable exists in any accessible scope."""
        if name in self.variables:
            return True
        elif self.parent:
            return self.parent.exists(name)
        return False

    def __repr__(self):
        return f"<Memory: {self.variables}>"