%{
#include <stdio.h>

%}

%%

[ \t\n]					        ;
"NO"					printf("TELSE ");
[a-zA-Z_][a-zA-Z0-9_]*  		printf("TIDENTIFIER ");
[0-9]+|[0-9]+\.[0-9]*			printf("TNUMBER ");
"{"         				printf("TOCBRACE ");
"}"					printf("TCCBRACE ");
"\""					printf("TDOUBLEQUOTES ");
"'"					printf("TSINGLEQUOTE ");
"\\"					printf("TBACKSLASH ");
"/"					printf("TFORWARDSLASH ");
"("					printf("TORBRACKET ");
")"					printf("TCRBRACKET ");
"["					printf("TOSBRACKET ");
"]"					printf("TCSBRACKET ");
\".*\"					printf("TSTRING ");
"="					printf("TEQUAL ");
"#"					printf("TIF ");
"##"					printf("TLOOP ");
"?"					printf("TCOND ");
.					printf("Undefined token ");c

%%
