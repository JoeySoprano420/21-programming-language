if __name__ == '__main__':
    # Example code in Dynamic 21
    code = "~| var:int [ x = 10 ], var:int [ y = 5 ] |~ ~| eax <- 3 |~ ~| add eax, x |~"
    
    # Parse code
    result = parser.parse(code)
    
    # Generate LLVM code from AST
    codegen = LLVMCodeGenerator()
    codegen.generate_from_ast(result)
    
    # Print generated code
    codegen.generate_code()
    
    # Optionally, execute the code (compiles to object code)
    codegen.execute_code()
