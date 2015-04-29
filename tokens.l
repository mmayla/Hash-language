%option noyywrap
%{
#include <stdio.h>



%}



%%



[ \t\n]					        ;

"@"   printf( "TAT"  );

"?"   printf( "TSWITCHCOND"  );

"leave"   printf( "TBREAK"  );

"default"   printf( "TSWITCHDEFAULT"  );

[a-zA-Z_][a-zA-Z0-9_]*  		printf("TIDENTIFIER ");

[0-9]+|[0-9]+\.[0-9]*			printf("TNUMBER ");

"{"         				printf("TOCBRACE ");

"}"					printf("TCCBRACE ");



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

"&"   printf( "TBWAND"  );

"|"   printf( "TBWOR"  );

"^"   printf( "TXOR"  );

"**"   printf( "TPOWER"  );



.+	printf("Undefined token");



%%

