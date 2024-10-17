# Combine Lexer, Parser, and LLVM Codegen

import ply.lex as lex
import ply.yacc as yacc
import llvmlite.ir as ir
import llvmlite.binding as llvm

# LEXER

tokens = [
    'VAR', 'REGISTER', 'INT', 'BOOL', 'IF', 'EQUAL', 'NUMBER', 'IDENTIFIER', 'ARROW', 'ADD', 'IS', 'OUTPUT'
]

t_VAR = r'var'
t_REGISTER = r'eax|ebx|ecx'
t_IF = r'<IF>'
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

# PARSER

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
    '''action : '@|' OUTPUT IDENTIFIER '|@' '''
    p[0] = ('output', p[3])

parser = yacc.yacc()

# LLVM CODE GENERATOR

class LLVMCodeGenerator:
    def __init__(self):
        # Initialize LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create the module and function builder
        self.module = ir.Module(name='Dynamic21')
        self.builder = None

        # Setup function signatures
        self.int_type = ir.IntType(32)
        self.bool_type = ir.IntType(1)

    def create_function(self):
        func_type = ir.FunctionType(self.int_type, [self.int_type])
        function = ir.Function(self.module, func_type, name="main")
        block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        return function

    def create_var(self, name, value):
        var = self.builder.alloca(self.int_type, name=name)
        self.builder.store(ir.Constant(self.int_type, value), var)
        return var

    def add_instruction(self, reg, val):
        loaded_reg = self.builder.load(reg, name='load_reg')
        added = self.builder.add(loaded_reg, ir.Constant(self.int_type, val))
        self.builder.store(added, reg)

    def generate_code(self):
        print(str(self.module))

    def execute_code(self):
        llvm_ir = str(self.module)

        # Create a target machine and compile
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        mod = llvm.parse_assembly(llvm_ir)
        mod.verify()

        # Compile the code to object code
        with open('output.o', 'wb') as f:
            f.write(target_machine.emit_object(mod))

# USAGE

codegen = LLVMCodeGenerator()
main_func = codegen.create_function()
x = codegen.create_var('x', 10)
codegen.add_instruction(x, 5)
codegen.generate_code()
codegen.execute_code()

# TEST

code = "~| var:int [ x = 10 ] |~"
lexer.input(code)
tokens = [token for token in lexer]
print(tokens)

ast = parser.parse(code)
print("AST:", ast)
