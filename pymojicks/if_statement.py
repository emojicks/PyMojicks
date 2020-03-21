from .stmt import BaseStmt


class IfBlock(BaseStmt):
    def __init__(self, ifs):
        self.stmts = ifs

    def eval(self, env):
        for stmt in self.stmts:
            result = stmt.eval(env)
            if result:
                break


class If(BaseStmt):
    def __init__(self, compare, body):
        self.compare = compare
        self.body = body

    def eval(self, env):
        result = self.compare.eval(env)
        if result:
            self.exec(env)

        return result

    def exec(self, env):
        for stmt in self.body.eval(env):
            stmt.eval(env)


class ElseIf(If):
    pass


class Else(If):
    def __init__(self, body):
        super().__init__(None, body)

    def eval(self, env):
        self.exec(env)

        return True
