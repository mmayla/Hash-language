import sys
import hashlex
from ast import Node
import generator
import ply.yacc as yacc

# get tokens
tokens = hashlex.tokens

#define generator
codegenerator = generator.Generator()

# statement
#TODO support (exp) 
def p_statements_list(p):
    ''' statements_list : statement statements_list
                        | compound_statement
                        | statement
                        '''
    print("statements list")
    if len(p)==3:
        p[0] = Node('statements_list',[p[2]],p[1])
    else:
        p[0] = Node('statements_list',None,p[1])
    pass

def p_compound_statement(p):
    ' compound_statement : LBRACE statements_list RBRACE '
    #print("compound statement")
    p[0] = Node('compound_statement',None,p[2])
    pass

def p_statement(p):
    ''' statement : assignment_expression
                  | decleration
                  | switch_statement
                  | if_statement
                  | iteration_statement
                  '''
    print("statement")
    p[0] = Node('iteration_statement',None,p[1])
    pass

# iteration statements
# while statement
def p_iteration_statement_1(p):
    ' iteration_statement : HASH HASH logical_expression compound_statement '
    print("itr. stmnt. 1 - while")
    p[0] = Node('iteration_statement',[p[4]],p[3])
    pass

# for statement
#TODO empty for arguments
def p_iteration_statement_2(p):
    ' iteration_statement : HASH HASH assignment_expression COMMA logical_expression COMMA assignment_expression compound_statement '
    print("itr. stmnt. 2 - for")
    p[0] = Node('iteration_statement',[p[3],p[7],p[8]],p[5])
    pass

# repeat until statement
def p_iteration_statement_3(p):
    ' iteration_statement : HASH HASH compound_statement logical_expression '
    print("itr. stmnt. 3 - repeat-until")
    p[0] = Node('iteration_statement',[p[4]],p[3])
    pass

#conditional statements
def p_if_statement(p):
    ''' if_statement : HASH logical_expression compound_statement
                     | HASH logical_expression compound_statement ELSE compound_statement
                     '''
    print("if statement")
    if len(p)==6:
        p[0] = Node('switch_statement',[p[3],p[5]],p[2])
    else:
        p[0] = Node('switch_statement',[p[3]],p[2])  
    pass

# switch statement
def p_switch_statement(p):
    ''' switch_statement : AT ID AT LBRACE switch_statement_body switch_statement_default RBRACE
                         | AT ID AT LBRACE switch_statement_body RBRACE
                         '''
    print("switch statement")
    if len(p)==8:
        p[0] = Node('switch_statement',[p[5],p[6]],p[2])
    else:
        p[0] = Node('switch_statement',[p[5]],p[2])    
    pass

def p_switch_statement_body(p):
    ''' switch_statement_body : switch_statement_case switch_statement_body
                              | switch_statement_case
                              '''
    print("switch stmnt body")
    if len(p)==3:
        p[0] = Node('switch_statement_body',[p[2]],p[1])
    else:
        p[0] = Node('switch_statement_body',None,p[1])
    pass

def p_switch_statement_case(p):
    ''' switch_statement_case : NCONST COND statements_list BREAK
                              | NCONST COND statements_list
                              '''
    print("switch stmnt case")
    if len(p)==5:
        p[0] = Node('switch_statement_default',[p[3],p[4]],p[1])
    else:
        p[0] = Node('switch_statement_default',[p[3]],p[1])
    pass

def p_switch_statement_default(p):
    ''' switch_statement_default : DEFAULT COND statements_list BREAK
                                 | DEFAULT COND statements_list
                                 '''
    print("switch stmnt default")
    if len(p)==5:
        p[0] = Node('switch_statement_default',[p[3],p[4]],p[1])
    else:
        p[0] = Node('switch_statement_default',[p[3]],p[1])
    pass

# assignment expressions
def p_assignment_expression_1(p):
    ''' assignment_expression : decleration EQUALS arithmatic_expression
                              | ID EQUALS arithmatic_expression
                              '''
    print("assig. expr. 1")
    p[0] = p[1]
    codegenerator.addAssembly("ST "+str(p[1])+","+str(p[3]))
    pass

def p_assignment_expression_2(p):
    ''' assignment_expression : decleration EQUALS const_literal
                              | ID EQUALS const_literal
                              '''
    print("assig. expr. 2")
    p[0] = p[1]
    
    pass

def p_assignment_expression_3(p):
    ''' assignment_expression : ID EQUALS logical_expression
                              | decleration EQUALS logical_expression
                              '''
    print("assig. expr. 3")
    p[0] = Node('assignment_expression',[p[1],p[3]],p[2])
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
    if len(p)==5:
        p[0] = Node('logical_expression',[p[1],p[3]],p[2])
    else :
        p[0] = p[1]
    pass
  
# arithmatic expressions
# FIXME 5=5, 6<5 -> LHS=ID
def p_arithmatic_expression(p):
    '''arithmatic_expression : ID arithmatic_operator arithmatic_expression
                             | NCONST arithmatic_operator arithmatic_expression
                             | NCONST
                             | ID 
                             '''
    print("Arth. Exp.")
    if len(p)==4:
        p[0] = p[1]
    else:
        if p[1]=="ID":
            p[0] = p[1]
        else:
            codegenerator.registers.append(str(p[1]))
            p[0] = "R"+str(len(codegenerator.registers)-1)
            codegenerator.addAssembly("MOV "+p[0]+","+str(p[1]))
    pass

def p_decleration(p):
    ' decleration : ID data_type'
    print("decleration")
    p[0] = p[1]
    codegenerator.addAssembly(str(p[1])+" "+p[2])
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
    p[0] = p[1]
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
    p[0] = p[1]
    pass

def p_const_literal(p):
    ''' const_literal : SCONST
                      '''
    print("const. lit.")
    p[0] = p[1]
    pass
  
def p_data_type(p):
    ''' data_type : NUMBER
                  | STRING
                  | BOOLEAN
                  '''
    print("data_type")
    p[0] = p[1]
    pass
    
################ Testing Parser ################ 
#Build the grammar

code = r'''
in_var $NUMBER = 5
fn_var $NUMBER = 3.14
str_var $STRING = "I am a \"string\" \n"
sout_var $STRING
bool_var $BOOLEAN = $like
'''

yacc.yacc()

yacc.parse(code)

codegenerator.printAssembly()

'''
while 1:
    try:
        s = raw_input('p> ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)
'''