import ply.lex as lex

tokens = [
    'VAR', 'REGISTER', 'INT', 'BOOL', 'IF', 'ELIF', 'EQUAL', 'NUMBER', 'IDENTIFIER', 'ARROW', 'ADD', 'IS', 'OUTPUT'
]

t_VAR = r'var'
t_REGISTER = r'eax|ebx|ecx'
t_IF = r'<IF>'
t_ELIF = r'<ELIF>'
t_EQUAL = r'='
t_ARROW = r'<-'
t_ADD = r'add'
t_IS = r':IS:'
t_OUTPUT = r'@|'
t_ignore = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

lexer = lex.lex()

# Example usage
code = "~| var:int [ x = 10 ] |~"
lexer.input(code)
for token in lexer:
    print(token)
