class Environment:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def add_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        return self.variables[name]

    def add_function(self, name, func):
        self.functions[name] = func

    def get_function(self, name):
        return self.functions[name]

class Program:
    def __init__(self, env, instructions):
        self.env = env
        self.instructions = instructions

    def eval(self):
        for instruction in self.instructions:
            instruction.eval()
