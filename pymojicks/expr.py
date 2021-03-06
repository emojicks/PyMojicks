class BaseExpr:
    def __init__(self, value, _type):
        self.value = value
        self.type = _type

    def eval(self, env):
        return

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __gt__(self, other):
        return isinstance(other, self.__class__) and self.value > other.value
    
    def __lt__(self, other):
        return isinstance(other, self.__class__) and self.value < other.value

    def __ne__(self, other):
        return isinstance(other, self.__class__) and self.value != other.value

    def __ge__(self, other):
        return isinstance(other, self.__class__) and self.value >= other.value

    def __le__(self, other):
        return isinstance(other, self.__class__) and self.value <= other.value

    def __repr__(self):
        return '<{} value={}>'.format(self.type, self.value)


class String(BaseExpr):
    def __init__(self, value):
        super().__init__(value, _type="String")

    def eval(self, env):
        return str(self.value)

    def iter(self, env):
        return [String(s) for s in self.eval(env)]

NUMBER_TRANSLATE = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

class Number(BaseExpr):
    def __init__(self, value):
        if isinstance(value, list):
            actual_value = ''
            for number in value:
                actual_value += str(NUMBER_TRANSLATE.index(number.data))
            actual_value = String(actual_value)
        else:
            actual_value = value

        super().__init__(actual_value, _type="Number")

    def eval(self, env):
        return int(self.value.eval(env))

class Float(BaseExpr):
    def __init__(self, value):
        actual_value = ''
        for number in value:
            if number.value != 'decimal':
                actual_value += str(NUMBER_TRANSLATE.index(number.data))
            else:
                actual_value += '.'

        super().__init__(String(value), _type="Float")

    def eval(self, env):
        return float(self.value.eval(env))


class Bool(BaseExpr):
    def __init__(self, value):
        super().__init__(value, _type="Bool")

    def eval(self, env):
        return bool(self.value)


class Variable(BaseExpr):
    def __init__(self, value):
        super().__init__(value, _type="Variable")

    def eval(self, env):
        return env.get_variable(self.value.value).eval(env)

    def iter(self, env):
        return env.get_variable(self.value.value).iter(env)

class FuncArg(BaseExpr):
    def __init__(self, name, type):
        super().__init__(name, _type="FuncArg")
        self.type = type
        self.name = name

    def eval(self, env):
        return

class Body(BaseExpr):
    def __init__(self, stmts):
        super().__init__(stmts, _type="Body")
        self.stmts = stmts

    def eval(self, env):
        return self.stmts
