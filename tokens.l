%{
#include <stdio.h>

%}

%%


[ \t\n]					        ;
"NO"					printf("TELSE ");
[a-zA-Z_][a-zA-Z0-9_]*  		printf("TIDENTIFIER ");
[0-9]+|[0-9]+\.[0-9]*			printf("TNUMBER ");
\".*\"					printf("TSTRING ");

"{"         				printf("TOCBRACE ");
"}"					printf("TCCBRACE ");
"("					printf("TORBRACKET ");
")"					printf("TCRBRACKET ");
"["					printf("TOSBRACKET ");
"]"					printf("TCSBRACKET ");

"\""					printf("TDOUBLEQUOTES ");
"'"					printf("TSINGLEQUOTE ");
"\\"					printf("TBACKSLASH ");
"/"					printf("TFORWARDSLASH ");
"#"					printf("TIF ");
"##"					printf("TLOOP ");
"?"					printf("TCOND ");

"="					printf("TEQUAL ");
"!"					printf("TNOT ");
"=="					printf("TEQUALTO ");	
"!="					printf("TNOTEQUAL ");
">"					printf("TGREATERTHAN ");
">="					printf("TGREATERTHANOREQUALTO ");
"<"					printf("TLESSTHAN ");
"<="					printf("TLESSTHANOREQUALTO ");
"&&"					printf("TAND ");
"||"					printf("TOR ");

.					printf("Undefined token ");

%%
