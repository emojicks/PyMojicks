from pathlib import Path
from lark import Lark, Transformer

from .stmt import *
from .expr import *
from .if_statement import *
from .builtin import GlobalFunctionCall
from .environment import Environment, Program

grammar = Path(__file__).parent.joinpath('pymojicks.lark')
parser = Lark.open(grammar)
MAIN_ENVIRONMENT = Environment()


def get_compares(items):
    if len(items) == 2:
            (left, right) = items
    else:
        (left,) = items
        right = Bool(True)

    return left, right


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
        return Body(items)

    def function(self, items):
        (name, args, body) = items
        return Function(name, args, body)

    def function_call(self, items):
        (name, items) = items
        if not isinstance(items, list):
            items = [items]

        return FunctionCall(name, items)

    def if_statement(self, items):
        return IfBlock(items)
    
    def first_if(self, items):
        (compare, body) = items
        return If(compare, body)

    def else_if(self, items):
        (compare, body) = items
        return ElseIf(compare, body)

    def final_else(self, items):
        (body,) = items
        return Else(body)

    def if_body(self, items):
        return Body(items)

    def compare_statement(self, items):
        (items,) = items
        return items

    def eq(self, items):
        left, right = get_compares(items)
        return Compare('__eq__', left, right)

    def gt(self, items):
        left, right = get_compares(items)
        return Compare('__gt__', left, right)

    def lt(self, items):
        left, right = get_compares(items)
        return Compare('__lt__', left, right)

    def ne(self, items):
        left, right = get_compares(items)
        return Compare('__ne__', left, right)

    def ge(self, items):
        left, right = get_compares(items)
        return Compare('__ge__', left, right)

    def le(self, items):
        left, right = get_compares(items)
        return Compare('__le__', left, right)

    def comparable(self, items):
        (items,) = items
        return items


def run(code):
    tree = parser.parse(code)
    program = PymojicksTransformer().transform(tree)
    program.run()
