from lark import Lark, InlineTransformer

from environment import Environment
from expr import String, Float, Bool, Variable
from stmt import Print, Input, Assignment

env = Environment()


class CalculateTree(InlineTransformer):
    number = float


def calc(parsed):
    return CalculateTree().transform(parsed)


def stmt(*args):
    if args[0].data == 'print':
        res = ''
        if args[1].data == 'paren_expr':
            if args[1].children[0].data == 'float':
                res = Float(env, calc(args[1].children[0]).children[0])
            elif args[1].children[0].data == 'string':
                res = String(env, args[1].children[0].children[0].children[0].strip("'").strip('"'))
            elif args[1].children[0].data == 'bool':
                res = Bool(env, True if args[1].children[0].children[0].data == 'true' else False)
            elif args[1].children[0].data == 'variable':
                res = Variable(env, args[1].children[0].children[0].children[0].value)

        return Print(env, res)

    elif args[0].data == 'input':
        res = String(env, '')
        if args[1].data == 'paren_expr':
            if args[1].children[0].data == 'float':
                res = Float(env, calc(args[1].children[0]).children[0])
            elif args[1].children[0].data == 'string':
                res = String(env, args[1].children[0].children[0].children[0].strip("'").strip('"'))
            elif args[1].children[0].data == 'bool':
                res = Bool(env, True if args[0].children[1].children[0].data == 'true' else False)

        return Input(env, res)

    elif args[0].data == 'var':
        res = ''

        if args[0].children[1].data == 'float':
            res = Float(env, calc(args[0].children[1]).children[0])
        elif args[0].children[1].data == 'string':
            res = String(env, args[0].children[1].children[0].children[0].strip("'").strip('"'))
        elif args[0].children[1].data == 'bool':
            res = Bool(env, True if args[0].children[1].children[0].data == 'true' else False)
        elif args[0].children[1].data == 'stmt':
            # ✏ yeet 👉 📥("h"); 📤(yeet);
            # ✏ yoten 👉 "yeeter"; 📤(yoten);
            # ✏ yoted 👉 ✔; 📤(yoted);
            # print(args[0].children[1].children)
            res = stmt(*args[0].children[1].children)

        return Assignment(env, args[0].children[0].children[0].value, res)

    elif args[0].data == 'variable':
        return Variable(env, args[0].children[0])


def run_instruction(t):
    if t.data == 'stmt':
        return stmt(*t.children)
    else:
        raise SyntaxError('Unknown instruction: %s' % t.data)


with open('grammar.lark', 'r', encoding='utf-8') as f:
    parser = Lark(f.read())


def run_turtle(program):
    parse_tree = parser.parse(program)

    print(parse_tree.pretty())

    for inst in parse_tree.children:
        inst_ = run_instruction(inst)
        inst_.eval()


def main():
    while True:
        code = input('>>> ')
        try:
            run_turtle(code)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
