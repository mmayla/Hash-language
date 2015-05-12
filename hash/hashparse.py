import sys
import hashlex
import ply.yacc as yacc

# get tokens
tokens = hashlex.tokens

def p_assign(p):
    '''assign : NAME EQUALS expr'''
def p_expr(p):
    '''expr : expr PLUS term
            | expr MINUS term
            | expr AND term
            | expr OR term
            | expr NOT term
            | term'''
def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
def p_factor(p):
    '''factor : NUMBER'''
yacc.yacc()             # Build the parser

data="a=b+2"

t=yacc.parse(data)

print(t)
