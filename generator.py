class Generator:
    def __init__(self):
        self.registers = []
        self.assembly = []
        self.labelno = 0
    
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