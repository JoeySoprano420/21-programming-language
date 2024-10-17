import ply.yacc as yacc

# Define precedence
precedence = ()

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
    '''condition : IDENTIFIER ':' IS condition_check'''
    p[0] = ('condition', p[1], p[3])

def p_condition_check(p):
    '''condition_check : '[' NUMBER '>' NUMBER ']' '''
    p[0] = ('range', p[2], p[4])

def p_action(p):
    '''action : '@|' OUTPUT STRING '|@' '''
    p[0] = ('output', p[3])

parser = yacc.yacc()

# Example parse
code = "~| var:int [ x = 10 ] |~"
parser.parse(code)
