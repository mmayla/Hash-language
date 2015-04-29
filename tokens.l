%{
#include <stdio.h>

%}

%option noyywrap

%%

[ \t\n]					        ;
[a-zA-Z_][a-zA-Z0-9_]*  		printf("TIDENTIFIER ");
[0-9]+|[0-9]+\.[0-9]*			printf("TNUMBER ");
"{"         				printf("TOCBRACE ");
"}"					printf("TCCBRACE ");
.+					printf("Undefined token");
%%
