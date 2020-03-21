from .expr import String
from .environment import Environment


class BaseStmt:
    def eval(self, env):
        return

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


class Cast(BaseStmt):
    def __init__(self, stmt, expr_type):
        self.stmt = stmt
        self.expr_type = expr_type

    def eval(self, env):
        return self.expr_type(self.stmt.eval(env))


class Assignment(BaseStmt):
    def __init__(self, name, value):
        self.name, self.value = name, value

    def eval(self, env):
        if isinstance(self.value, BaseStmt):
            v = self.value.eval(env)
        else:
            v = self.value
        return env.add_variable(self.name, v)

class Function(BaseStmt):
    def __init__(self, name, args, body=None, *, _global=False):
        self.name, self.args, self.body = name, args, body
        self._global = _global
    
    def eval(self, env):
        if not self._global:
            env.add_function(self.name, self)
        else:
            env.add_builtin(self.name, self)

        return self

    def exec(self, args, env):
        func_env = Environment(parent=env)
        for arg in args:
            Assignment(self.args[args.index(arg)].name.value, arg).eval(func_env)

        for instruction in self.body.stmts:
            instruction.eval(func_env)


class FunctionCall(BaseStmt):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    
    def eval(self, env):
        env.get_function(self.name).exec(self.args, env)
