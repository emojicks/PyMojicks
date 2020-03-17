from expr import String
from environment import Environment


class BaseStmt:
    def __init__(self, env):
        self.env = env

    def eval(self):
        return

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def change_env(self, env):
        self.env = env
        self.value.env = env


class Print(BaseStmt):
    def __init__(self, env, value):
        super().__init__(env)
        self.value = value

    def eval(self):
        print(self.value.eval())


class Input(BaseStmt):
    def __init__(self, env, prompt):
        super().__init__(env)
        self.prompt = prompt

    def eval(self):
        return String(self.env, input(self.prompt.eval()))

class Exit(BaseStmt):
    def __init__(self, env, value):
        super().__init__(env)
        self.value = value

    def eval(self):
        return exit(self.value.eval())

class Cast(BaseStmt):
    def __init__(self, env, stmt, expr_type):
        super().__init__(env)
        self.stmt = stmt
        self.expr_type = expr_type

    def eval(self):
        return self.expr_type(self.env, self.stmt.eval())


class Assignment(BaseStmt):
    def __init__(self, env, name, value):
        super().__init__(env)
        self.name, self.value = name, value

    def eval(self):
        if isinstance(self.value, BaseStmt):
            v = self.value.eval()
        else:
            v = self.value
        return self.env.add_variable(self.name, v)

class Function(BaseStmt):
    def __init__(self, env, name, args, body):
        super().__init__(env)
        self.name, self.args, self.body = name, args, body

        self.env.add_function(self.name, self)
    
    def eval(self):
        return self

    def exec(self, args):
        func_env = Environment()
        for arg in args:
            func_env.add_variable(self.args[args.index(arg)].name, arg)

        for instruction in self.body.stmts:
            instruction.change_env(func_env)
            instruction.eval()

class FunctionCall(BaseStmt):
    def __init__(self, env, name, args):
        super().__init__(env)
        self.name = name
        self.args = args
    
    def eval(self):
        self.env.get_function(self.name).exec(self.args)
