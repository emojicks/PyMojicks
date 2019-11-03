from expr import String


class BaseStmt:
    def __init__(self, env):
        self.env = env

    def eval(self):
        return

    def __repr__(self):
        return '<{} value={}>'.format(self.__class__.__name__, self.eval())


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


class Cast(BaseStmt):
    def __init__(self, env, stmt, expr_type):
        super().__init__(env)
        self.stmt = stmt
        self.expr_type = expr_type

    def eval(self):
        return self.expr_type(self.env, self.stmt.eval()).eval()


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
