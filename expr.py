class BaseExpr:
    def __init__(self, env, value, _type):
        self.env = env
        self.value = value
        self.type = _type

    def eval(self):
        return

    def __repr__(self):
        return '<{} value={}>'.format(self.type, self.value)


class String(BaseExpr):
    def __init__(self, env, value):
        super().__init__(env, value, _type="String")

    def eval(self):
        return str(self.value)


class Float(BaseExpr):
    def __init__(self, env, value):
        super().__init__(env, value, _type="Float")

    def eval(self):
        return float(self.value)


class Bool(BaseExpr):
    def __init__(self, env, value):
        super().__init__(env, value, _type="Bool")

    def eval(self):
        return bool(self.value)


class Variable(BaseExpr):
    def __init__(self, env, value):
        super().__init__(env, value, _type="Variable")

    def eval(self):
        return self.env.get_variable(self.value).eval()

class FuncArg(BaseExpr):
    def __init__(self, env, name, type):
        super().__init__(env, name , _type="FuncArg")
        self.type = type
        self.name = name

    def eval(self):
        return None

class FuncBody(BaseExpr):
    def __init__(self, env, stmts):
        super().__init__(env, stmts, _type="FuncBody")
        self.stmts = stmts

    def eval(self):
        return self.stmts
