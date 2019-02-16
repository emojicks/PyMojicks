from rply import LexerGenerator

lg = LexerGenerator()

lg.add('NUMBER', r'\d+')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('MUL', r'\*')
lg.add('DIV', r'/')
lg.add('NEWLINE', r'\\n')
lg.add('OPEN_PARENS', r'\(')
lg.add('CLOSE_PARENS', r'\)')
lg.add('VAR', r'var')
lg.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')
lg.add('SEMICOLON', r';')
lg.add('EQUAL', r'=')
lg.add('STRING', r'(""".*?""")|(".*?")|(\'.*?\')')

"""
lg.add('LESS', r'<')
lg.add('MORE', r'>')
lg.add('R_BRACE', r'}')
lg.add('L_BRACE', r'{')
lg.add('QUOTE', r'"|\'')
lg.add('COMMA', r'\,')
lg.add('BANG', r'\!')
lg.add('PERIOD', r'\.')
"""

lg.ignore(r'\s+')


lexer = lg.build()

# with open('./yes.em') as f:
#     print(f.read())
#     for token in l.lex(f.read()):
#         print(token)
