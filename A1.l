%option noyywrap
%{
	#include<stdio.h>
%}

%%
[ \t\n]					        ;
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
"||"   printf( "TOR"  );
"&"   printf( "TBWAND" );
"|"   printf( "TBWOR" );
"^"   printf( "TBWXOR" );
"**"   printf( " TBWPOWER" );
      
%%
main() {
	yylex();

	printf("OK");
}