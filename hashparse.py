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
    ' compound_statement : left_brace statements_list right_brace '
    print("compound statement")
    p[0] = "cp"
    pass

def p_statement(p):
    ''' statement : assignment_expression
                  | decleration
                  | switch_statement
                  | if_statement
                  | iteration_statement
                  '''
    print("statement")
    p[0] = Node('statement',None,p[1])
    pass

# iteration statements
# while statement
def p_iteration_statement_1(p):
    ' iteration_statement : iteration_pre logical_expression compound_statement '
    print("itr. stmnt. 1 - while")
    p[0] = "while"
    idx = codegenerator.lastIndexOfInst("CMP")
    codegenerator.assembly.insert(idx,"loop-"+codegenerator.getLabel()+":")
    codegenerator.assembly.insert(idx+3,"JMP out"+codegenerator.getLabel())
    codegenerator.assembly.insert(idx+4,codegenerator.getLabel()+":")
    codegenerator.addAssembly("JMP loop-"+codegenerator.getLabel())
    codegenerator.addAssembly("out"+codegenerator.getLabel()+":")
    pass

# for statement
#TODO empty for arguments
def p_iteration_statement_2(p):
    ' iteration_statement : iteration_pre assignment_expression COMMA logical_expression COMMA assignment_expression compound_statement '
    print("itr. stmnt. 2 - for")
    p[0] = "for"
    sidx = codegenerator.lastIndexOfInst("CMP")
    eidx = codegenerator.lastIndexOfInst("{")
    lines = []
    for i in range (0,eidx-sidx-2):
        lines.append(codegenerator.assembly.pop(sidx+2))
        
    eidx = codegenerator.lastIndexOfInst("}")
    codegenerator.assembly.pop(eidx)
    for i in range (0,len(lines)):
        codegenerator.assembly.insert(i+eidx,lines[i])
    
    sid = codegenerator.lastIndexOfInst("{")
    codegenerator.assembly.pop(sid)
    codegenerator.assembly.insert(sid,"JMP out"+codegenerator.getLabel())
    
    codegenerator.addAssembly("JMP loop-"+codegenerator.getLabel())
    codegenerator.addAssembly("out"+codegenerator.getLabel()+":")
    
    sidx = codegenerator.lastIndexOfInst("CMP")
    codegenerator.assembly.insert(sidx,"loop-"+codegenerator.getLabel()+":")
    pass

# repeat until statement
def p_iteration_statement_3(p):
    ' iteration_statement : iteration_pre compound_statement logical_expression '
    print("itr. stmnt. 3 - repeat-until")
    p[0] = "ru"
    idx = codegenerator.lastIndexOfInst("#") #TODO if -1 error
    codegenerator.assembly.pop(idx) #remove #
    codegenerator.assembly.insert(idx,codegenerator.getLabel()+":")
    pass


def p_iteration_pre(p):
    ' iteration_pre : HASH HASH'
    codegenerator.addAssembly("#")
    pass

#conditional statements

def p_if_statement(p):
    ''' if_statement : HASH logical_expression compound_statement
                     | HASH logical_expression compound_statement ELSE compound_statement
                     '''
    print("if statement")
    if len(p)==6:
        p[0] = Node('if_statement',[p[3],p[5]],p[2])
    else:
        p[0] = "if"
        
    pass

# switch statement
def p_switch_statement(p):
    ''' switch_statement : AT ID AT left_brace switch_statement_body switch_statement_default right_brace
                         | AT ID AT left_brace switch_statement_body right_brace
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
    codegenerator.addAssembly("ST "+str(p[1])+","+str(p[3]))
    pass

def p_assignment_expression_3(p):
    ''' assignment_expression : ID EQUALS logical_expression
                              | decleration EQUALS logical_expression
                              '''
    print("assig. expr. 3")
    p[0] = p[1]
    codegenerator.addAssembly("ST "+str(p[1])+","+str(p[3]))
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
        p[0] = "***"
        codegenerator.addAssembly("CMP "+p[1]+","+p[3])
        codegenerator.addAssembly("JE "+codegenerator.getNewLabel()) #FIXME JMP to real
    else :
        if p[1]=='$like':
            p[1]="1"
        else:
            p[1]="0"
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
        #TODO complete
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

def p_left_brace(p):
    ' left_brace : LBRACE '
    codegenerator.addAssembly("{")
    pass

def p_right_brace(p):
    ' right_brace : RBRACE '
    codegenerator.addAssembly("}")
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
sout_var $STRING
## k $NUMBER=0, k<5?, k=k+1 {
	sout_var = k
}
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