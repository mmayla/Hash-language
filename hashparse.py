import sys
import hashlex
import ply.yacc as yacc

# get tokens
tokens = hashlex.tokens


# statement
#TODO support (exp) 
def p_statements_list(p):
    ''' statements_list : statement statements_list
                        | compound_statement
                        | statement
                        '''
    print("statements list")
    pass

def p_compound_statement(p):
    ' compound_statement : LBRACE statements_list RBRACE '
    print("compound statement")
    pass

def p_statement(p):
    ''' statement : assignment_expression
                  | decleration
                  | switch_statement
                  | if_statement
                  | iteration_statement
                  '''
    print("statement")
    pass

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

#conditional statements
# FIXME NO { } not defined
def p_if_statement(p):
    ''' if_statement : HASH logical_expression compound_statement
                     | HASH logical_expression compound_statement ELSE compound_statement
                     '''
    print("if statement")
    pass

# switch statement
def p_switch_statement(p):
    ''' switch_statement : AT ID AT LBRACE switch_statement_body switch_statement_default RBRACE
                         | AT ID AT LBRACE switch_statement_body RBRACE
                         '''
    print("switch statement")
    pass

def p_switch_statement_body(p):
    ''' switch_statement_body : switch_statement_case switch_statement_body
                              | switch_statement_case
                              '''
    print("switch stmnt body")
    pass

def p_switch_statement_case(p):
    ''' switch_statement_case : NCONST COND statements_list BREAK
                              | NCONST COND statements_list
                              '''
    print("switch stmnt case")
    pass

def p_switch_statement_default(p):
    ''' switch_statement_default : DEFAULT COND statements_list BREAK
                                 | DEFAULT COND statements_list
                                 '''
    print("switch stmnt default")
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
#TODO rewrite
def p_logical_expression(p):
    ''' logical_expression : ID logical_operator BCONST COND
                           | ID logical_operator NCONST COND
                           | BCONST logical_operator ID COND
                           | NCONST logical_operator ID COND
                           | ID logical_operator ID COND
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

code = r'''
in_var $NUMBER = 5
fn_var $NUMBER = 3.14
str_var $STRING = "I am a \"string\" \n"
sout_var $STRING
bool_var $BOOLEAN = $like


# in_var < fn_var ? {
	sout_var = "first less than second"
} $NO {
	sout_var = "second less than first"
}

i $NUMBER = 0
## i <= 5 ? {
	sout_var = i
	i = i+1
}

i = 0
## {
	sout_var = i
	i = i+1
} i<=5 ?

## k $NUMBER=0, k<5?, k=k+1 {
	sout_var = k
}

@i@{
	1 ? 
		sout_var = "i = 1"
	$leave
	
	2?
		sout_var = "i = 2"
	$leave

	$failed ?
		sout_var = "not found"
	$leave
}
'''

yacc.yacc()

yacc.parse(code)

'''
while 1:
    try:
        s = raw_input('p> ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)
'''