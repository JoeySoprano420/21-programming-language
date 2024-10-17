if __name__ == '__main__':
    # Example code
    code = """
    ~| var:int [ x = 10 ], var:bool [ flag = true ] |~
    ~| eax <- 5 |~
    ~| add eax, x |~
    """

    # Lexing, Parsing, Code Generation
    lexer.input(code)
    for token in lexer:
        print(token)

    parser.parse(code)
    codegen = LLVMCodeGenerator()
    main_func = codegen.create_function()
    x = codegen.create_var('x', 10)
    codegen.add_instruction(x, 5)
    codegen.generate_code()
    codegen.execute_code()
