from rply import ParserGenerator

from emoji_types import Number, Add, Sub, Mul, Div, String, Program
from environment import Environment
from lexer import lexer
from variable import Variable, Assignment

env = Environment()
pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['NUMBER', 'OPEN_PARENS', 'CLOSE_PARENS',
     'PLUS', 'MINUS', 'MUL', 'DIV', 'IDENTIFIER', 'EQUAL', 'SEMICOLON',
     'STRING', 'NEWLINE', '$end'],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ]
)


@pg.production("main : program")
def main_program(env, p):
    return p[0]


@pg.production('program : statement_full')
def program_statement(env, p):
    return Program(p[0])


@pg.production('program : statement_full program')
def program_statement_program(env, p):
    if type(p[1]) is Program:
        program = p[1]
    else:
        program = Program(p[-1])

    program.add_statement(p[0])
    return p[1]


@pg.production('statement_full : statement NEWLINE')
@pg.production('statement_full : statement $end')
def statement_full(env, p):
    return p[0]


@pg.production('expression : STRING')
def string(env, p):
    return String(str(p[0].value))


@pg.production('expression : NUMBER')
def expression_number(env, p):
    # p is a list of the pieces matched by the right hand side of the
    # rule
    return Number(int(p[0].getstr()))


@pg.production('statement : IDENTIFIER EQUAL expression SEMICOLON')
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


#    with open('yes.em') as f:
#        e = lexer.lex(f.read().encode("unicode_escape").decode("utf-8"))
#        print(list(e))
#        parser.parse(e).eval()

if __name__ == '__main__':
    _string = 'Hello 👉 "test"⚓'

    lex = lexer.lex(_string)
    print(list(lex))
    parser.parse(lex, env).eval(env)
