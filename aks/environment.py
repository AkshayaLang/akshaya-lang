# aks/environment.py

class ExecutionContext:
    def __init__(self):
        self.symbol_table = {}

    def get(self, name):
        if name in self.symbol_table:
            return self.symbol_table[name]
        raise NameError(f"Variable '{name}' is not defined")

    def set(self, name, value):
        self.symbol_table[name] = value

    def exists(self, name):
        return name in self.symbol_table

    def delete(self, name):
        if name in self.symbol_table:
            del self.symbol_table[name]
        else:
            raise NameError(f"Cannot delete undefined variable '{name}'")

    def dump(self):
        return dict(self.symbol_table)