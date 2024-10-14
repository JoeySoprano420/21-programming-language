class TokenType:
    VAR, IF, ELIF, ELSE, LOGIC_OPERATOR, OUTPUT, ASSIGN, NUMBER, IDENTIFIER = range(9)

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

def tokenize(source_code):
    tokens = []
    # Simple tokenizer implementation
    for line in source_code.splitlines():
        line = line.strip()
        if line.startswith("~|"):
            # Handle variable declaration or assignment
            if "var:" in line:
                parts = line[3:-2].split("[")
                var_type = parts[0].split(":")[1].strip()
                var_name_value = parts[1][:-1].split("=")
                tokens.append(Token(TokenType.VAR, (var_type, var_name_value[0].strip(), var_name_value[1].strip())))
        elif line.startswith("<IF:"):
            # Handle conditionals
            tokens.append(Token(TokenType.IF, line[4:-1]))
        elif line.startswith("@|"):
            # Handle outputs
            tokens.append(Token(TokenType.OUTPUT, line[3:-2]))
        # Add more token parsing as necessary
    return tokens

class NodeType:
    VAR_DECLARATION, IF_STATEMENT, OUTPUT = range(3)

class Node:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

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
