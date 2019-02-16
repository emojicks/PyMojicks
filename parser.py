from rply import ParserGenerator
from environment import Environment
from emoji_types import Number, Add, Sub, Mul, Div, String
from lexer import lexer
from variable import Variable, Assignment

env = Environment()
pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['NUMBER', 'OPEN_PARENS', 'CLOSE_PARENS',
     'PLUS', 'MINUS', 'MUL', 'DIV', 'VAR', 'IDENTIFIER', 'EQUAL', 'SEMICOLON',
     'STRING'],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ]
)


@pg.production('expression : STRING')
def string(env, p):
    return String(str(p[0].value))


@pg.production('expression : NUMBER')
def expression_number(env, p):
    # p is a list of the pieces matched by the right hand side of the
    # rule
    return Number(int(p[0].getstr()))


@pg.production('statement : VAR IDENTIFIER EQUAL expression SEMICOLON')
def assignment(env, p):
    return Assignment(Variable(p[0].value), p[2])


@pg.production('expression : IDENTIFIER')
def variable(env, p):
    return Variable(p[0].value)


@pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
def expression_parens(env, p):
    return p[1]


@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')
def expression_binop(env, p):
    left = p[0]
    right = p[2]
    if p[1].gettokentype() == 'PLUS':
        return Add(left, right)
    elif p[1].gettokentype() == 'MINUS':
        return Sub(left, right)
    elif p[1].gettokentype() == 'MUL':
        return Mul(left, right)
    elif p[1].gettokentype() == 'DIV':
        return Div(left, right)
    else:
        raise AssertionError('Oops, this should not be possible!')


@pg.error
def error_handler(env, _token):
    raise ValueError("Ran into a %s where it wasn't expected" % _token.gettokentype())


parser = pg.build()


if __name__ == '__ma__':
    with open('yes.em') as f:
        e = lexer.lex(f.read().encode("unicode_escape").decode("utf-8"))
        print(list(e))
        parser.parse(e).eval()

if __name__ == '__main__':
    _string = 'var Hello = "test";'

    l = lexer.lex(_string)
    print(list(l))
    parser.parse(l, env).eval(env)
