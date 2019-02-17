from rply.token import BaseBox


class Number(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self.value


class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOp):
    def eval(self, env):
        return self.left.eval() + self.right.eval()


class Sub(BinaryOp):
    def eval(self, env):
        return self.left.eval() - self.right.eval()


class Mul(BinaryOp):
    def eval(self, env):
        return self.left.eval() * self.right.eval()


class Div(BinaryOp):
    def eval(self, env):
        return self.left.eval() / self.right.eval()


class String(BaseBox):
    def __init__(self, value):
        self.value = str(value)

    def eval(self, env):
        return self.value


class Program(BaseBox):
    def __init__(self, statement):
        self.statements = []
        self.statements.append(statement)
        self.run = False

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def eval(self, env):
        result = None
        for statement in self.statements:
            result = statement.eval(env)
        return result

    def get_statements(self):
        return self.statements