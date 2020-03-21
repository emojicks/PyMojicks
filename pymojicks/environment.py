class Environment:
    def __init__(self, *, parent=None):
        self.parent = parent
        self.variables = {}
        self.functions = {}
        self.builtins = {}

        if parent:
            self.variables.update(parent.variables)
            self.functions.update(parent.functions)
            self.builtins = parent.builtins
        else:
            from .builtin import BUILTINS

            for b in BUILTINS:
                b_called = b()
                self.builtins[b_called.name] = b_called

    def add_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        return self.variables[name]

    def add_function(self, name, func):
        self.functions[name] = func

    def get_function(self, name):
        return self.functions[name]

    def add_builtin(self, name, func):
        self.builtins[name] = func

    def get_builtin(self, name):
        return self.builtins[name]

class Program:
    def __init__(self, env, instructions):
        self.env = env
        self.instructions = instructions

    def run(self):
        for instruction in self.instructions:
            instruction.eval(self.env)
