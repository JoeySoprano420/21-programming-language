import ply.lex as lex
import ply.yacc as yacc
import llvmlite.ir as ir
import llvmlite.binding as llvm

# Tokens
tokens = [
    'VAR', 'REGISTER', 'INT', 'BOOL', 'IF', 'ELIF', 'EQUAL', 'NUMBER', 'IDENTIFIER', 'ARROW', 'ADD', 'IS', 'OUTPUT', 'GT', 'LT', 'GE', 'LE'
]

# Token definitions
t_VAR = r'var'
t_REGISTER = r'eax|ebx|ecx|edx'
t_IF = r'<IF>'
t_ELIF = r'<ELIF>'
t_EQUAL = r'='
t_ARROW = r'<-'
t_ADD = r'add'
t_IS = r':IS:'
t_OUTPUT = r'@|'
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_ignore = ' \t'

# Identifiers and numbers
def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parser rules

def p_statement_var_decl(p):
    '''statement : VAR ':' type '[' IDENTIFIER EQUAL NUMBER ']' '''
    p[0] = ('var_decl', p[3], p[5], p[7])

def p_arithmetic_op(p):
    '''statement : REGISTER ARROW NUMBER'''
    p[0] = ('assign', p[1], p[3])

def p_add_op(p):
    '''statement : ADD REGISTER ',' IDENTIFIER'''
    p[0] = ('add', p[2], p[4])

def p_if_condition(p):
    '''statement : IF condition ':' action'''
    p[0] = ('if', p[2], p[4])

def p_condition(p):
    '''condition : IDENTIFIER IS condition_check'''
    p[0] = ('condition', p[1], p[3])

def p_condition_check(p):
    '''condition_check : NUMBER GT NUMBER
                       | NUMBER LT NUMBER
                       | NUMBER GE NUMBER
                       | NUMBER LE NUMBER '''
    p[0] = ('comparison', p[2], p[1], p[3])

def p_action_output(p):
    '''action : OUTPUT IDENTIFIER'''
    p[0] = ('output', p[2])

def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()
