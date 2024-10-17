def traverse_ast(node, codegen):
    if node[0] == 'var_decl':
        # Variable declaration
        codegen.create_var(node[2], node[3])
    elif node[0] == 'assign':
        # Variable assignment
        codegen.assign_var(node[1], node[2])
    elif node[0] == 'add':
        # Addition operation
        codegen.add_instruction(node[1], node[2])
    elif node[0] == 'if':
        # If statement
        codegen.generate_if(node[1], node[2])
    elif node[0] == 'output':
        # Output statement
        codegen.generate_output(node[1])

# Example AST traversal
ast = parser.parse(code)
for node in ast:
    traverse_ast(node, codegen)
