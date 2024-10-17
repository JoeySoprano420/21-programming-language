import ply.lex as lex

tokens = [
    'VAR', 'INT', 'BOOL', 'REGISTER', 'NUMBER', 'IDENTIFIER', 'EQUAL', 'LESS', 'GREATER', 
    'IF', 'ELIF', 'ELSE', 'BLACKJACK', 'IS', 'OUTPUT', 'ADD', 'CHANGE', 'AND', 'OR'
]

t_VAR = r'var'
t_EQUAL = r'='
t_LESS = r'<'
t_GREATER = r'>'
t_IF = r'<IF:blackjack>'
t_ELIF = r'<ELIF>'
t_ELSE = r'<ELSE>'
t_IS = r':IS:'
t_OUTPUT = r'@|'
t_ADD = r'add'
t_CHANGE = r'change'
t_AND = r'&&'
t_OR = r'\|\|'
t_REGISTER = r'eax|ebx|ecx|edx'

# Handle identifiers and numbers
def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Handle newlines and spaces
t_ignore = ' \t\n'

# Error handling for illegal characters
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
