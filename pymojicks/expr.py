class BaseExpr:
    def __init__(self, value, _type):
        self.value = value
        self.type = _type

    def eval(self, env):
        return

    def __repr__(self):
        return '<{} value={}>'.format(self.type, self.value)


class String(BaseExpr):
    def __init__(self, value):
        super().__init__(value, _type="String")

    def eval(self, env):
        return str(self.value)


class Float(BaseExpr):
    def __init__(self, value):
        super().__init__(value, _type="Float")

    def eval(self, env):
        return float(self.value.eval(env))


class Bool(BaseExpr):
    def __init__(self, value):
        super().__init__(value, _type="Bool")

    def eval(self, env):
        return bool(self.value.eval(env))


class Variable(BaseExpr):
    def __init__(self, value):
        super().__init__(value, _type="Variable")

    def eval(self, env):
        return env.get_variable(self.value.value).eval(env)

class FuncArg(BaseExpr):
    def __init__(self, name, type):
        super().__init__(name, _type="FuncArg")
        self.type = type
        self.name = name

    def eval(self, env):
        return

class FuncBody(BaseExpr):
    def __init__(self, stmts):
        super().__init__(stmts, _type="FuncBody")
        self.stmts = stmts

    def eval(self, env):
        return self.instructions
