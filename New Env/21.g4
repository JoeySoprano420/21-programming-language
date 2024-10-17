grammar 21;

// Lexer Rules
ID      : [a-zA-Z_][a-zA-Z0-9_]* ;
NUMBER  : [0-9]+ ;
STRING  : '"' (ESC | ~["\\])* '"' ;
ESC     : '\\' [bfnrt"'\\] ;
WS      : [ \t\n\r]+ -> skip ;

// Parser Rules
program : statement* ;
statement : assignment | expression ;

assignment : ID '=' expression ;
expression : NUMBER | ID | STRING ;
