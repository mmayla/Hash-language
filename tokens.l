%{
#include <stdio.h>

%}

%%

[ \t\n]					        ;
[a-zA-Z_][a-zA-Z0-9_]*  		printf("TIDENTIFIER ");
[0-9]+|[0-9]+\.[0-9]*			printf("TNUMBER ");
"{"         				printf("TOCBRACE ");
"}"					printf("TCCBRACE ");
.+					printf("Undefined token");
"+"    printf( "TADD" );
"-"    printf( "TSUB" );
"*"   printf( "TMUL" );
"/"   printf( "TDIV" );
"!"   printf( "TNOT" );
"=="    printf( "TEQUAL" );
"!="   printf( "TNOTEQUAL" );
">"   printf( "TGREATER" );
">="    printf( "TGREATEREQUAL" );
"<"    printf( "TLESS" );
"<="   printf( "TLESSEQUAL" );
"&&"   printf( "TAND"  );
%%
