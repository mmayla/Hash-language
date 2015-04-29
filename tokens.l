%{
#include <stdio.h>

%}

%option noyywrap

%%

[ \t\n]					        ;
"No"							printf("TELSE");
[a-zA-Z_][a-zA-Z0-9_]*  		printf("TIDENTIFIER");
[0-9]+|[0-9]+\.[0-9]*			printf("TNUMBER");
"="                   			printf("TEQUAL");
"#"								printf("TIF");
"##"				 			printf("TLOOP");
"?"								printf("TCOND");
"{"         					printf("TOCBRACE");
"}"								printf("TCCBRACE");
.+								printf("Undefined token");
%%
