from rply.token import BaseBox
from emoji_types import BinaryOp


class Variable(BaseBox):
    def __init__(self, name):
        self.name = str(name)
        self.value = None

    def eval(self, env):
        if env.variables.get(self.name, None) is not None:
            self.value = env.variables[self.name].eval(env)
            return self.value
        raise NameError("Not yet defined")


class Assignment(BinaryOp):
    def eval(self, env):
        if isinstance(self.left, Variable):
            env.variables[self.left.name] = self.right
            return self.right.eval(env)
        else:
            raise NameError("Cannot assign to this")
