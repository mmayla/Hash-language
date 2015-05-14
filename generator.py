class Variable:
    def __init__(self,name,dtype):
        self.name = name
        self.datatype = dtype
        

class Generator:
    def __init__(self):
        self.registers = []
        self.assembly = []
        self.labelno = 0
        self.error = False
        self.tempvar = ""
        self.variables = []
        self.errors = []
    
    def printErrors(self):
        for i in range(0,len(self.errors)):
            print("> "+self.errors[i])
    
    def addVariable(self,var):
        self.variables.append(var)
        
    def isDeclared(self,var):
        for i in range (0,len(self.variables)):
            if self.variables[i].name == var:
                return True
        return False
    
    def addAssembly(self,line):
        self.assembly.append(line)
    
    def printAssembly(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        for i in range (0,len(self.assembly)):
            if len(self.assembly[i])>0:
                print(str(self.assembly[i]))
                
    def lastIndexOfInst(self,inst):
        idx = -1
        sub = len(inst)
        for i in range (0,len(self.assembly)):
            if self.assembly[i][:sub]==inst:
                idx = i
        return idx
    
    def getNewLabel(self):
        self.labelno = self.labelno+1
        return "label"+str(self.labelno)
    
    def getLabel(self):
        return "label"+str(self.labelno)
    
    def readFile(self,path):
        with open(path) as f:
            content = f.readlines()
            s = ""
            for i in range (0,len(content)):
                s = s + content[i]
            return s
    
    def writeAssemblyToFile(self,path):
        target = open(path,'w')
        for i in range(0,len(self.assembly)):
            if (self.assembly[i]!='{') and (self.assembly[i]!='}') and (self.assembly[i]!='#'):
                target.write(self.assembly[i])
                target.write("\n")
            
    def writeErrorFile(self,path,errorlineno,errormsg):
        error = open(path,'w')
        error.write(str(errorlineno))
        error.write("\n")
        error.write(str(errormsg))
        error.write("\n")