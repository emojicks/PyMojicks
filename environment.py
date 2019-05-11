class Environment:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def add_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        return self.variables[name]