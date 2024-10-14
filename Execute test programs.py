# Sample execution
source_code = """
~| var:int [ x = 10 ] |~
<IF:blackjack> x :IS: [greater than 5] 
    @| OUTPUT "x is valid" |@
<ELSE>
    @| OUTPUT "x is invalid" |@
"""

tokens = tokenize(source_code)
ast = parse(tokens)
vm = VirtualMachine()
vm.execute(ast)
