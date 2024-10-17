%{
#include <stdio.h>
#include "y.tab.h"
%}

%token ID NUMBER STRING

%% 

program : statement
         | program statement
         ;

statement : assignment
          | expression
          ;

assignment : ID '=' expression ';'
           ;

expression : NUMBER
            | ID
            | STRING
            ;
%%
