class Generator:
    def __init__(self):
        self.registers = []
        self.assembly = []
    
    def addAssembly(self,line):
        self.assembly.append(line)
        
    def printAssembly(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        for i in range (0,len(self.assembly)):
            print(str(self.assembly[i]))