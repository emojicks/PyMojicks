from pathlib import Path
from lark import Lark, Transformer

from .stmt import *
from .expr import *
from .builtin import GlobalFunctionCall
from .environment import Environment, Program

grammar = Path(__file__).parent.joinpath('pymojicks.lark')
parser = Lark.open(grammar)
MAIN_ENVIRONMENT = Environment()


class PymojicksTransformer(Transformer):
    def start(self, items):
        return Program(MAIN_ENVIRONMENT, items)

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

    def builtin(self, items):
        (name, items) = items
        if not isinstance(items, list):
            items = [items]

        return GlobalFunctionCall(name, items)

    def EMOJI(self, items):
        (items,) = items

        return items

    def variable(self, items):
        (items,) = items
        return Variable(items)

    def convert_stmt(self, items):
        (stmt, conv_type) = items
        return Cast(stmt, conv_type)
        
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
        return Float(items)

    def true(self, items):
        return Bool(True)

    def false(self, items):
        return Bool(False)

    def var(self, items):
        (name, items) = items
        return Assignment(name, items)

    def stmts(self, items):
        (items,) = items
        return items

    def stmt(self, items):
        (items,) = items
        return items

    def string(self, items):
        (items,) = items
        return String(items[1:-1])

    def func_arg(self, items):
        (type, name) = items
        return FuncArg(name, type)

    def func_args(self, items):
        return list(items)

    def func_body(self, items):
        return FuncBody(items)

    def function(self, items):
        (name, args, body) = items
        return Function(name, args, body)

    def function_call(self, items):
        (name, items) = items
        if not isinstance(items, list):
            items = [items]

        return FunctionCall(name, items)

def run(code):
    tree = parser.parse(code)
    program = PymojicksTransformer().transform(tree)
    program.run()
