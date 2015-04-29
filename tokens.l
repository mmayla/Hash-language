%{
#include <stdio.h>

%}

%%

[ \t\n]					        ;
[a-zA-Z_][a-zA-Z0-9_]*  		printf("TIDENTIFIER ");
[0-9]+|[0-9]+\.[0-9]*			printf("TNUMBER ");
"{"         				printf("TOCBRACE ");
"}"					printf("TCCBRACE ");
"!"					printf("TNOT");
"=="					printf("TEQUALTO");	
"!="					printf("TNOTEQUAL");
">"					printf("TGREATERTHAN");
">="					printf("TGREATERTHANOREQUALTO");
"<"					printf("TLESSTHAN");
"<="					printf("TLESSTHANOREQUALTO");
"&&"					printf("TAND");
"||"					printf("TOR");
"##"					printf("TLOOP");
.+					printf("Undefined token");
%%
