import sys
import hashlex
import ply.yacc as yacc

# get tokens
tokens = hashlex.tokens

# assignment expressions
def p_assignment_expression_1(p):
    'assignment_expression : decleration EQUALS arithmatic_expression'
    print("assig. expr. 1")
    pass
    
def p_assignment_expression_2(p):
    'assignment_expression : ID EQUALS arithmatic_expression'
    print("assig. expr. 2")
    pass

# arithmatic expressions
def p_arithmatic_expression(p):
    '''arithmatic_expression : ID arithmatic_operator arithmatic_expression
                             | NCONST arithmatic_operator arithmatic_expression
                             | NCONST
                             | ID 
                             '''
    print("Arth. Exp.")
    pass

def p_decleration(p):
    ' decleration : ID data_type'
    print("decleration")
    pass
    
def p_arithmatic_operator(p):
    ''' arithmatic_operator : PLUS
                            | MINUS
                            | TIMES
                            | DIVIDE
                            | MOD
                            | POWER
                            '''
    print("arith. opr.")
    pass

def p_data_type(p):
    ''' data_type : NUMBER
                  | STRING
                  | BOOLEAN
                  '''
    print("data_type")
    pass                            

################ Testing Parser ################ 
#Build the grammar
yacc.yacc()

while 1:
    try:
        s = raw_input('p> ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)