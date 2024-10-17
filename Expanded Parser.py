import ply.yacc as yacc

# Dictionary to hold variables and their types/values
variables = {}

def p_statement_var_decl(p):
    '''statement : VAR ':' type '[' IDENTIFIER EQUAL NUMBER ']' '''
    variables[p[5]] = p[7]
    p[0] = ('var_decl', p[3], p[5], p[7])

def p_statement_arithmetic(p):
    '''statement : REGISTER ARROW NUMBER
                 | ADD REGISTER ',' IDENTIFIER'''
    if len(p) == 4:
        p[0] = ('assign', p[1], p[3])
    elif len(p) == 5:
        p[0] = ('add', p[2], p[4])

def p_statement_if_condition(p):
    '''statement : IF condition ':' action
                 | ELIF condition ':' action
                 | ELSE ':' action'''
    if len(p) == 5:
        p[0] = ('conditional', p[1], p[2], p[4])
    else:
        p[0] = ('else', p[3])

def p_condition(p):
    '''condition : IDENTIFIER IS condition_check'''
    p[0] = ('condition', p[1], p[3])

def p_condition_check(p):
    '''condition_check : NUMBER GREATER NUMBER
                       | NUMBER LESS NUMBER'''
    if p[2] == '>':
        p[0] = ('greater', p[1], p[3])
    else:
        p[0] = ('less', p[1], p[3])

def p_action_output(p):
    '''action : OUTPUT IDENTIFIER'''
    p[0] = ('output', p[2])

def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()
