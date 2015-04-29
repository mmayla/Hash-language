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


























































































































  GNU nano 2.0.9                File: A1.l                            Modified  

%option noyywrap
%{
        #include<stdio.h>
%}

%%

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

^G Get Help  ^O WriteOut  ^R Read File ^Y Prev Page ^K Cut Text  ^C Cur Pos
^X Exit      ^J Justify   ^W Where Is  ^V Next Page ^U UnCut Text^T To Spell


%%
