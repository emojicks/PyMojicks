from .stmt import Function, FunctionCall
from .expr import String, Float, FuncArg


class GlobalFunction(Function):
    def __init__(self, name, args):
        super().__init__(name, args, _global=True)

    def eval(self):
        return self


class GlobalFunctionCall(FunctionCall):
    def __init__(self, name, args):
        super().__init__(name, args)
        self.name = name

    def eval(self, env):
        return env.get_builtin(self.name).exec(self.args, env)


class Print(GlobalFunction):
    def __init__(self):
        super().__init__('📤', [FuncArg('text', String)])

    def exec(self, args, env):
        processed_args = []
        for arg in args:
            processed_args.append(arg.eval(env))
        
        print(*processed_args)


class Input(GlobalFunction):
    def __init__(self):
        super().__init__('📥', [FuncArg('prompt', String)])

    def exec(self, args, env):
        prompt = args[0]
        return String(input(prompt.eval(env)))


class Exit(GlobalFunction):
    def __init__(self):
        super().__init__('🔚', [FuncArg('code', Float)])

    def exec(self, args, env):
        value = args[0]
        return exit(value.eval(env))


BUILTINS = [Print, Input, Exit]
