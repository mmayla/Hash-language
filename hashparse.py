import sys
import hashlex
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
    codegenerator.assembly.insert(sid+1,codegenerator.getLabel()+":")
    codegenerator.addAssembly("JMP loop-"+codegenerator.getLabel())
    codegenerator.addAssembly("out"+codegenerator.getLabel()+":")
    
    sidx = codegenerator.lastIndexOfInst("CMP")
    codegenerator.assembly.insert(sidx,"loop-"+codegenerator.getLabel()+":")
    
    sidx = codegenerator.lastIndexOfInst("#")
    codegenerator.assembly.pop(sidx)
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
        p[0] = "if"
        idx = codegenerator.lastIndexOfInst("CMP")
        codegenerator.assembly.insert(idx+2,"JMP f"+codegenerator.getLabel())
        codegenerator.assembly.insert(idx+3,codegenerator.getLabel()+":")
        idx = codegenerator.lastIndexOfInst("{")
        codegenerator.assembly.insert(idx,"JMP out"+codegenerator.getLabel())
        codegenerator.assembly.insert(idx+1,"f"+codegenerator.getLabel()+":")
        idx = codegenerator.lastIndexOfInst("}")
        codegenerator.assembly.insert(idx,"out"+codegenerator.getLabel()+":")
    else:
        p[0] = "if"
        idx = codegenerator.lastIndexOfInst("CMP")
        codegenerator.assembly.insert(idx+2,"JMP out"+codegenerator.getLabel())
        codegenerator.assembly.insert(idx+3,codegenerator.getLabel()+":")
        idx = codegenerator.lastIndexOfInst("}")
        codegenerator.assembly.insert(idx,"out"+codegenerator.getLabel()+":")
    pass

# switch statement
def p_switch_statement(p):
    ''' switch_statement : switch_head left_brace switch_statement_body switch_statement_default right_brace
                         | switch_head left_brace switch_statement_body right_brace
                         '''
    print("switch statement")
    if len(p)==8:
        p[0] = "switch"
        codegenerator.addAssembly("label_end:")
    else:
        p[0] = "switch"
        codegenerator.addAssembly("label_end:")
    pass

def p_switch_head(p):
    ' switch_head : AT ID AT'
    print("switch head")
    p[0] = p[2]
    codegenerator.tempvar = p[0]
    #codegenerator.addAssembly(">"+str(p[2]))
    pass

def p_switch_statement_body(p):
    ''' switch_statement_body : switch_statement_case switch_statement_body
                              | switch_statement_case
                              '''
    print("switch stmnt body")
    if len(p)==3:
        p[0] = "switch body"
    else:
        p[0] = "switch body"
    pass

def p_switch_statement_case(p):
    ''' switch_statement_case : NCONST COND statements_list BREAK
                              | NCONST COND statements_list
                              '''
    print("switch stmnt case")

    p[0] = "switch case"
    codegenerator.addAssembly("JMP label_end")

    sidx = codegenerator.lastIndexOfInst("{")
    eidx = codegenerator.lastIndexOfInst("#")
    if sidx > eidx:
        eidx = sidx

    codegenerator.assembly.insert(eidx+1,"CMP "+codegenerator.tempvar+","+str(p[1]))
    codegenerator.assembly.insert(eidx+2,"JE "+codegenerator.getNewLabel()+"_"+str(p[1]))
    codegenerator.assembly.insert(eidx+3,"JMP"+ " label_end")
    codegenerator.assembly.insert(eidx+4,codegenerator.getLabel()+"_"+str(p[1])+":")
    codegenerator.addAssembly("#")
    pass

def p_switch_statement_default(p):
    ''' switch_statement_default : DEFAULT COND statements_list BREAK
                                 | DEFAULT COND statements_list
                                 '''
    print("switch stmnt default")
    if len(p)==5:
        p[0] = "switch default"
        #codegenerator.addAssembly("default")
    else:
        p[0] = "switch default"
        #codegenerator.addAssembly("default")
    pass

# assignment expressions
# TODO here
def p_assignment_expression_1(p):
    ''' assignment_expression : decleration EQUALS arithmatic_expression '''
    print("assig. expr. 1")
    p[0] = p[1]
    codegenerator.addAssembly("ST "+str(p[1])+","+str(p[3]))
    
    vartype = codegenerator.getVarType(str(p[1]))
    if vartype != '$NUMBER':
          codegenerator.errors.append("Can not convert "+str(vartype)+" to $NUMBER at line "+str(p.lineno(2)))
    pass

def p_assignment_expression_2(p):
    ''' assignment_expression : decleration EQUALS const_literal '''
    print("assig. expr. 2")
    p[0] = p[1]
    codegenerator.addAssembly("ST "+str(p[1])+","+str(p[3]))
    vartype = codegenerator.getVarType(str(p[1]))
    if vartype != '$STRING':
          codegenerator.errors.append("Can not convert "+str(vartype)+" to $STRING at line "+str(p.lineno(2)))
    pass

def p_assignment_expression_3(p):
    ''' assignment_expression : decleration EQUALS logical_expression '''
    print("assig. expr. 3")
    p[0] = p[1]
    codegenerator.addAssembly("ST "+str(p[1])+","+str(p[3]))
    vartype = codegenerator.getVarType(str(p[1]))
    if vartype != '$BOOLEAN':
          codegenerator.errors.append("Can not convert "+str(vartype)+" to $BOOLEAN at line "+str(p.lineno(2)))
    pass

def p_assignment_expression_4(p):
    ''' assignment_expression : ID EQUALS const_literal'''
    print("assig. expr. 4")
    p[0] = p[1]
    codegenerator.addAssembly("ST "+str(p[1])+","+str(p[3]))
    
    if not codegenerator.isDeclared(str(p[1])):
        codegenerator.errors.append("The variable "+str(p[1])+" is not declared at line "+str(p.lineno(1)))
    else:
            vartype = codegenerator.getVarType(str(p[1]))
            if vartype != '$STRING':
                codegenerator.errors.append("Can not convert "+str(vartype)+" to $STRING at line "+str(p.lineno(2)))
    pass

def p_assignment_expression_5(p):
    ''' assignment_expression : ID EQUALS arithmatic_expression'''
    print("assig. expr. 5")
    p[0] = p[1]
    codegenerator.addAssembly("ST "+str(p[1])+","+str(p[3]))
    
    if not codegenerator.isDeclared(str(p[1])):
        codegenerator.errors.append("The variable "+str(p[1])+" is not declared at line "+str(p.lineno(1)))
    else:
            vartype = codegenerator.getVarType(str(p[1]))
            if vartype != '$NUMBER':
                codegenerator.errors.append("Can not convert "+str(vartype)+" to $NUMBER at line "+str(p.lineno(2)))
    pass

def p_assignment_expression_6(p):
    ''' assignment_expression : ID EQUALS logical_expression'''
    print("assig. expr. 6")
    p[0] = p[1]
    codegenerator.addAssembly("ST "+str(p[1])+","+str(p[3]))
    
    if not codegenerator.isDeclared(str(p[1])):
        codegenerator.errors.append("The variable "+str(p[1])+" is not declared at line "+str(p.lineno(1)))
    else:
            vartype = codegenerator.getVarType(str(p[1]))
            if vartype != '$BOOLEAN':
                codegenerator.errors.append("Can not convert "+str(vartype)+" to $BOOLEAN at line "+str(p.lineno(2)))
    pass

#logical expressions
#TODO rewrite
def p_logical_expression_1(p):
    ''' logical_expression : BCONST logical_operator ID COND
                           | NCONST logical_operator ID COND
                           | BCONST
                           '''
    print("logical expr.1")
    if len(p)==5:
        p[0] = "***"
        codegenerator.addAssembly("CMP "+p[1]+","+p[3])
        codegenerator.addAssembly(p[2]+" "+codegenerator.getNewLabel())
        vartype = codegenerator.getVarType(str(p[3]))
        if p[1]=='$like' or p[1]=='$dislike':
            if vartype != '$BOOLEAN':
                codegenerator.errors.append("Can not perform this operation on "+str(vartype)+" with $BOOLEAN at line "+str(p.lineno(1)))
        else:
            if vartype != '$NUMBER':
                codegenerator.errors.append("Can not perform this operation on "+str(vartype)+" with $NUMBER at line "+str(p.lineno(1)))
    else :
        if p[1]=='$like':
            p[1]="1"
        else:
            p[1]="0"
        p[0] = p[1]
    pass

def p_logical_expression_2(p):
    ''' logical_expression : ID logical_operator BCONST COND
                           | ID logical_operator NCONST COND
                           '''
    print("logical expr. 2")
    if len(p)==5:
        p[0] = "***"
        codegenerator.addAssembly("CMP "+p[1]+","+p[3])
        codegenerator.addAssembly(p[2]+" "+codegenerator.getNewLabel())
        vartype = codegenerator.getVarType(str(p[1]))
        if p[3]=='$like' or p[3]=='$dislike':
            if vartype != '$BOOLEAN':
                codegenerator.errors.append("Can not perform this operation on "+str(vartype)+" with $BOOLEAN at line "+str(p.lineno(1)))
        else:
            if vartype != '$NUMBER':
                codegenerator.errors.append("Can not perform this operation on "+str(vartype)+" with $NUMBER at line "+str(p.lineno(1)))
    else :
        if p[1]=='$like':
            p[1]="1"
        else:
            p[1]="0"
        p[0] = p[1]
    pass  

def p_logical_expression_3(p):
    ''' logical_expression : ID logical_operator ID COND '''
    print("logical expr. 3")
    if len(p)==5:
        p[0] = "***"
        codegenerator.addAssembly("CMP "+p[1]+","+p[3])
        codegenerator.addAssembly(p[2]+" "+codegenerator.getNewLabel())
        vartype1 = codegenerator.getVarType(str(p[1]))
        vartype2 = codegenerator.getVarType(str(p[3]))
        if vartype1 != vartype2:
                codegenerator.errors.append("Can not perform this operation on "+str(vartype1)+" with "+str(vartype2)+" at line "+str(p.lineno(1)))
    else :
        if p[1]=='$like':
            p[1]="1"
        else:
            p[1]="0"
        p[0] = p[1]
    pass  

# arithmatic expressions
# FIXME 5=5, 6<5 -> LHS=ID
def p_arithmatic_expression_1(p):
    '''arithmatic_expression : const_number arithmatic_operator arithmatic_expression
                             | const_number
                             '''
    print("Arth. Exp.1")
    if len(p)==4:
        codegenerator.addAssembly(p[2]+" "+p[1]+","+p[3])
        p[0]=p[1]
    else:
        if p[1][0]!="R":
            p[0] = p[1]
        else:
            codegenerator.registers.append(str(p[1]))
            p[0] = "R"+str(len(codegenerator.registers)-1)
            codegenerator.addAssembly("MOV "+p[0]+","+str(p[1]))
    pass
def p_arithmatic_expression_2(p):
    '''arithmatic_expression : ID arithmatic_operator arithmatic_expression
                             | ID
                             '''
    print("Arth. Exp.2")
    if len(p)==4:
        codegenerator.addAssembly(p[2]+" "+p[1]+","+p[3])
        p[0]=p[1]
        vartype = codegenerator.getVarType(str(p[1]))
        if vartype != '$NUMBER':
            codegenerator.errors.append("Can perform this operation on "+str(vartype)+" at line "+str(p.lineno(1)))
    else:
        vartype = codegenerator.getVarType(str(p[1]))
        if vartype != '$NUMBER':
            codegenerator.errors.append("Can perform this operation on "+str(vartype)+" at line "+str(p.lineno(1)))
        if p[1][0]!="R":
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
    
    if codegenerator.isDeclared(str(p[1])):
        codegenerator.errors.append("The variable name "+str(p[1])+" is declared before, rename the variable at line "+str(p.lineno(1)))
    else :
        codegenerator.addVariable(generator.Variable(str(p[1]),str(p[2])))
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
    if p[1]=="<":
        p[0] = "JLT"
    elif p[1]==">":
        p[0] = "JGT"
    elif p[1]=="<=":
        p[0] = "JLE"
    elif p[1]==">=":
        p[0] = "JGE"
    elif p[1]=="==":
        p[0] = "JEQ"
    elif p[1]=="!=":
        p[0] = "JNE"
    else:
        p[0] = "JMP"
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
    if p[1]=="+":
        p[0] = "ADD"
    elif p[1]=="-":
        p[0] = "SUB"
    elif p[1]=="*":
        p[0] = "MUL"
    elif p[1]=="~":
        p[0] = "DIV"
    elif p[1]=="%":
        p[0] = "MOD"
    elif p[1]=="&":
        p[0] = "AND"
    elif p[1]=="|":
        p[0] = "OR"
    elif p[1]=="**":
        p[0] = "XOR"
    elif p[1]=="^":
        p[0] = "POW"
    pass

def p_left_brace(p):
    ' left_brace : LBRACE '
    codegenerator.addAssembly("{")
    pass

def p_right_brace(p):
    ' right_brace : RBRACE '
    codegenerator.addAssembly("}")
    pass

def p_const_number(p):
    ' const_number : NCONST '
    codegenerator.registers.append(str(p[1]))
    p[0] = "R"+str(len(codegenerator.registers)-1)
    codegenerator.addAssembly("MOV "+p[0]+","+str(p[1]))
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


def p_error(p):
    if p != None:
        msg = "Syntax error: Token ("+str(p.type)+") at line: "+str(p.lineno)
        print(msg)
        #codegenerator.writeErrorFile("./workspace/error.out",p.lineno,msg)
        codegenerator.errors.append(msg)
    pass

################ Testing Parser ################ 
#Build the grammar

#input file
code = codegenerator.readFile("./workspace/input.hash")

yacc.yacc()

yacc.parse(code)

codegenerator.printAssembly()
codegenerator.printErrors()

codegenerator.writeAssemblyToFile("./workspace/output.hash")

if len(codegenerator.errors)==0 :
    codegenerator.writeErrorFile("./workspace/error.out",0,"Succeed")
else:
    codegenerator.writeErrorsToFile("./workspace/error.out")
    

'''
while 1:
    try:
        s = raw_input('p> ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)
'''