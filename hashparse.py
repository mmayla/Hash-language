import sys
import hashlex
import ply.yacc as yacc

# get tokens
tokens = hashlex.tokens

# iteration statements
# while statement
def p_iteration_statement_1(p):
    ' iteration_statement : HASH HASH logical_expression compound_statement '
    print("itr. stmnt. 1 - while")
    pass

# for statement
#TODO empty for arguments
def p_iteration_statement_2(p):
    ' iteration_statement : HASH HASH assignment_expression COMMA logical_expression COMMA assignment_expression compound_statement '
    print("itr. stmnt. 2 - for")
    pass

# repeat until statement
def p_iteration_statement_3(p):
    ' iteration_statement : HASH HASH compound_statement logical_expression '
    print("itr. stmnt. 3 - repeat-until")
    pass

#conditional statement
def p_if_statement(p):
    ''' if_statement : HASH logical_expression compound_statement
                     | HASH logical_expression compound_statement ELSE compound_statement
                     '''
    print("if statement")
    pass

# statements
def p_compound_statement(p):
    ' compound_statement : LBRACE statements_list RBRACE '
    print("compound statement")
    pass

def p_statements_list(p):
    ''' statements_list : statement statements_list
                       | statement
                       '''
    print("statements list")
    pass

def p_statement(p):
    ''' statement : assignment_expression
                  | decleration
                  | if_statement
                  '''
    print("statement")
    pass

# assignment expressions
def p_assignment_expression_1(p):
    ''' assignment_expression : decleration EQUALS arithmatic_expression
                              | ID EQUALS arithmatic_expression
                              '''
    print("assig. expr. 1")
    pass

def p_assignment_expression_3(p):
    ''' assignment_expression : decleration EQUALS const_literal
                              | ID EQUALS const_literal
                              '''
    print("assig. expr. 2")
    pass

def p_assignment_expression_5(p):
    ''' assignment_expression : ID EQUALS logical_expression
                              | decleration EQUALS logical_expression
                              '''
    print("assig. expr. 3")
    pass

#logical expressions
#TODO add x < 5 support
def p_logical_expression(p):
    ''' logical_expression : ID logical_operator BCONST COND
                           | ID logical_operator ID COND
                           | BCONST logical_operator ID COND
                           | BCONST
                           '''
    print("logical expr.")
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

# Operators   
def p_logical_operator(p):
    ''' logical_operator : LOR
                         | LAND
                         | LNOT
                         | LT
                         | GT
                         | LE
                         | GE
                         | EQ
                         | NE
                         '''
    print("log. opr.")
    pass
  
def p_arithmatic_operator(p):
    ''' arithmatic_operator : PLUS
                            | MINUS
                            | TIMES
                            | DIVIDE
                            | MOD
                            | POWER
                            | AND
                            | OR
                            | XOR
                            '''
    print("arith. opr.")
    pass

def p_const_literal(p):
    ''' const_literal : SCONST
                      '''
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