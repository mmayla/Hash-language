%{
#include <string>

#define SAVE_TOKEN  yylval.string = new std::string(yytext, yyleng)
#define TOKEN(t)    (yylval.token = t)
%}

%option noyywrap

%%

[ \t\n]					        ;
[a-zA-Z_][a-zA-Z0-9_]*  		SAVE_TOKEN; return TIDENTIFIER;
[0-9]+|[0-9]+\.[0-9]*			SAVE_TOKEN; return TNUMBER;
"{"         				return TOKEN(TLBRACE);
"}"					return TOKEN(TRBRACE);
%%
