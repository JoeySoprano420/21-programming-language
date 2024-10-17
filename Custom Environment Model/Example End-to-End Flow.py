if __name__ == '__main__':
    # Initialize the Dynamic 21 compiler
    dynamic_21_compiler = Dynamic21Compiler()

    # Sample 21 language code
    code = """
    ~| var:int [ x = 10 ], var:bool [ flag = true ] |~
    ~| eax <- 5 |~
    ~| add eax, x |~
    ~| store eax -> result |~
    """

    # Compile and run the code
    dynamic_21_compiler.compile_and_run(code)
