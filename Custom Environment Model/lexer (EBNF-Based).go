statement       ::= variable_declaration | arithmetic_operation | conditional_statement
variable_declaration ::= "~|" "var" ":" type "[" identifier "=" value "]" "|~"
arithmetic_operation  ::= "~|" register "<-" value "|~" | "~|" "add" register "," identifier "|~"
conditional_statement ::= "<IF>" condition ":" action
