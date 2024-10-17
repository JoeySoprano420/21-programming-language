import ply.lex as lex
import ply.yacc as yacc
import llvmlite.ir as ir
import llvmlite.binding as llvm

# LEXER
tokens = [
    'VAR', 'REGISTER', 'INT', 'BOOL', 'IF', 'EQUAL', 'NUMBER', 'IDENTIFIER', 'ARROW', 'ADD', 'IS', 'OUTPUT'
]

# Token definitions
t_VAR = r'var'
t_REGISTER = r'eax|ebx|ecx'
t_IF = r'<IF>'
t_EQUAL = r'='
t_ARROW = r'<-'
t_ADD = r'add'
t_IS = r':IS:'
t_OUTPUT = r'@|'
t_ignore = ' \t'

# Identifier token
def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    return t

# Number token
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Error handling for illegal characters
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
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

def p_error(p):
    print("Syntax error in input!")

# Build the parser
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
        self.variables = {}  # To store variable references

        # Setup function signatures
        self.int_type = ir.IntType(32)
        self.bool_type = ir.IntType(1)

    def create_function(self):
        # Define a 'main' function
        func_type = ir.FunctionType(self.int_type, [])
        function = ir.Function(self.module, func_type, name="main")
        block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        return function

    def create_var(self, name, value):
        var = self.builder.alloca(self.int_type, name=name)
        self.builder.store(ir.Constant(self.int_type, value), var)
        self.variables[name] = var
        return var

    def assign_var(self, register, value):
        if register in self.variables:
            var = self.variables[register]
            self.builder.store(ir.Constant(self.int_type, value), var)
        else:
            raise ValueError(f"Variable {register} not found!")

    def add_instruction(self, reg, identifier):
        if reg in self.variables and identifier in self.variables:
            reg_val = self.builder.load(self.variables[reg])
            id_val = self.builder.load(self.variables[identifier])
            added_val = self.builder.add(reg_val, id_val)
            self.builder.store(added_val, self.variables[reg])
        else:
            raise ValueError(f"Variables {reg} or {identifier} not found!")

    def generate_if(self, condition, action):
        # Generate LLVM IR for an if condition
        true_block = self.builder.append_basic_block(name="true")
        end_block = self.builder.append_basic_block(name="end")

        # Condition comparison (greater than, less than, etc.)
        left = ir.Constant(self.int_type, condition[1])
        right = ir.Constant(self.int_type, condition[2])
        if condition[0] == '>':
            cmp = self.builder.icmp_signed('>', left, right)
        elif condition[0] == '<':
            cmp = self.builder.icmp_signed('<', left, right)
        elif condition[0] == '>=':
            cmp = self.builder.icmp_signed('>=', left, right)
        elif condition[0] == '<=':
            cmp = self.builder.icmp_signed('<=', left, right)

        self.builder.cbranch(cmp, true_block, end_block)

        # True block (action)
        self.builder.position_at_end(true_block)
        self.generate_output(action)
        self.builder.branch(end_block)

        # End block
        self.builder.position_at_end(end_block)

    def generate_output(self, output_var):
        if output_var in self.variables:
            output_val = self.builder.load(self.variables[output_var])
            print(f"Output: {output_val}")
        else:
            raise ValueError(f"Output variable {output_var} not found!")

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

# MAIN FUNCTION TO EXECUTE THE CODE
if __name__ == '__main__':
    # Example code in the 21-language syntax
    code = """
    ~| var:int [ x = 10 ], var:bool [ flag = true ] |~
    ~| eax <- 5 |~
    ~| add eax, x |~
    ~| store eax -> result |~
    """

    # Lexing and parsing
    lexer.input(code)
    for token in lexer:
        print(token)

    # Parse the code and generate AST
    ast = parser.parse(code)
    print("AST:", ast)

    # Generate and execute LLVM IR code
    codegen = LLVMCodeGenerator()
    main_func = codegen.create_function()
    codegen.create_var('x', 10)
    codegen.add_instruction('eax', 'x')
    codegen.generate_code()
    codegen.execute_code()
