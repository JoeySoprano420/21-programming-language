def execute_program(program):
    context = Context()
    logic_handler = LogicHandler()
    
    tokens = tokenize(program)
    statements = parse(tokens)

    for statement in statements:
        if statement.node_type == NodeType.VAR_DECLARATION:
            var_type, var_name, var_value = statement.value
            context.set_variable(var_name, eval(var_value))  # Using eval for simplicity
            
        elif statement.node_type == NodeType.IF_STATEMENT:
            condition = statement.value
            eval_condition = eval(condition)  # Logic for evaluating condition
            if logic_handler.evaluate_logic(1 if eval_condition else 2):  # Example evaluation
                for child in statement.children:
                    if child.node_type == NodeType.OUTPUT:
                        print(child.value)

