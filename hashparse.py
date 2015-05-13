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
            | term POWER factor
            | factor'''
def p_factor(p):
    '''factor : NUMBER'''
def p_bitwise(p):
    '''bitwise : expr LAND expr
            | expr LOR expr
            | expr LNOT expr'''
def p_at(p):
     #if  tokens.type ==  ID
      '''at : @ tokens  @ LBRACE l1 RBRACE  '''  
def p_l1(p):
  '''l1 : tokens.value  expr leave l1'''   

# Build the parser
yacc.yacc()             

data="a=b+2"

t=yacc.parse(data)

print(t)
