# Sample 21 Language Code
code = """
~| var:int [ x = 10 ], var:bool [ flag = true ] |~
~| eax <- 5 |~
~| add eax, x |~
<IF:blackjack> x :IS: [greater than 5 and less than 15]
     @| OUTPUT "x is in range" |@
<ELSE>
     @| OUTPUT "x is out of range" |@
"""

# Parse the code
lexer.input(code)
for token in lexer:
    print(token)

# Generate LLVM IR from AST
ast = parser.parse(code)
codegen = LLVMCodeGenerator()
codegen.create_function()

# Traversing the AST and generating LLVM IR
for node in ast:
    if node[0] == 'var_decl':
        codegen.declare_variable(node[2], node[3])
    elif node[0] == 'assign':
        codegen.assign_register(node[1], node[2])
    elif node[0] == 'add':
        codegen.add_operation(node[1], node[2])

# Print the LLVM IR
codegen.generate_code()
