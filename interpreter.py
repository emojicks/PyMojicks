from lark import Lark, Transformer
from traceback import print_exc
from stmt import *
from expr import *
from environment import Environment, Program

parser = Lark.open('pymojicks.lark')
env = Environment()

class PymojicksTransformer(Transformer):
    def start(self, items):
        return Program(env, items)

    def print(self, items):
        (items,) = items
        return Print(env, items)

    def paren_expr(self, items):
        if len(items) > 0:
            (items,) = items
        else:
            items = None
        return items

    def expr(self, items):
        (items,) = items
        return items

    def identifier(self, items):
        (items,) = items
        return items

    def variable(self, items):
        (items,) = items
        return Variable(env, items)

    def convert_stmt(self, items):
        (stmt, conv_type) = items
        return Cast(env, stmt, conv_type)
        
    def bool_type(self, items):
        return Bool
    
    def float_type(self, items):
        return Float

    def string_type(self, items):
        return String

    def bool(self, items):
        (items,) = items
        return items

    def float(self, items):
        (items,) = items
        return Float(env, items)

    def true(self, items):
        return Bool(env, True)

    def false(self, items):
        return Bool(env, False)

    def var(self, items):
        (name, items) = items
        return Assignment(env, name, items)

    def stmts(self, items):
        (items,) = items
        return items

    def stmt(self, items):
        (items,) = items
        return items

    def input(self, items):
        (items,) = items
        return Input(env, items)

    def string(self, items):
        (items,) = items
        return String(env, items[1:-1])

    def func_arg(self, items):
        (type, name) = items
        return FuncArg(env, name, type)

    def func_args(self, items):
        return list(items)

    def func_body(self, items):
        return FuncBody(env, items)

    def function(self, items):
        (name, args, body) = items
        return Function(env, name, args, body)

    def function_call(self, items):
        (name, items) = items
        if not isinstance(items, list):
            items = [items]

        return FunctionCall(env, name, items)

    def exit(self, items):
        return Exit(env, Float(env, -1))


def run(code):
    tree = parser.parse(code)
    inst = PymojicksTransformer().transform(tree)
    inst.eval()

def main():
    while True:
        code = input('>>> ')
        try:
            run(code)
        except Exception as e:
            print_exc()



if __name__ == '__main__':
    main()

# ✏️ my_func (✒️ str, 🔢 times) ▶️
#    📤(str);
#    🔚();
# ◀️
# my_func("hello");
