from Memory import MemoryAux

class AddressManager:
    def __init__(self, globalBases, globalSizes) :
        ## Global Memories
        self.globalVars = []
        self.globalConst = []
        self.globalTemp = []
        self.globalLocals = []

        self.globalBases = globalBases

        self.varsStart = 0
        self.tempStart = 0
        self.localStart = 0
        self.constStart = 0
        self.constLimit = 0

        self.stackLocals = []

        self.initializeGlobalMemories(globalSizes)
        self.initializeMemoryLimits()

    def initializeMemoryLimits(self):
        self.varsStart = self.globalBases[0][0]
        self.tempStart = self.globalBases[1][0]
        self.localStart = self.globalBases[2][0]
        self.constStart = self.globalBases[3][0]
        self.constLimit = self.globalBases[3][-1] + 1000

    def initializeGlobalMemories(self, globalSizes):
        
        variableSizes = globalSizes[0]
        tempSizes = globalSizes[1]
        localSizes = globalSizes[2]
        constSizes = globalSizes[3]

        self.globalVars = MemoryAux(   variableSizes[0],
                                            variableSizes[1],
                                            variableSizes[2],
                                            0
                                            )

        self.globalTemp = MemoryAux(        tempSizes[0],
                                            tempSizes[1],
                                            tempSizes[2],
                                            tempSizes[3]
                                            )

        self.globalLocals = MemoryAux (     localSizes[0],
                                            localSizes[1],
                                            localSizes[2],
                                            localSizes[3] 
                                            )

        self.globalConst = MemoryAux(       constSizes[0],
                                            constSizes[1],
                                            constSizes[2],
                                            0
                                            )

        self.stackLocals.append(self.globalLocals)

    def addLocalMemory(self,sizes):
        auxLocalMemory = MemoryAux( 
                                    sizes[0],
                                    sizes[1],
                                    sizes[2],
                                    sizes[3] 
                                    )

        self.stackLocals.append(auxLocalMemory)

    def popLocalMemory(self):
        self.stackLocals.pop()

    def printMemory(self):
        print("GlobalVars --------")
        self.globalVars.print()
        print("TemporalVars --------")
        self.globalTemp.print()
        print("LocalVars --------")

        for i in range(0, len(self.stackLocals)):
            print(i * -1)
            self.stackLocals[ i * -1 ].print()

        #self.stackLocals[-1].print()
        #self.globalLocals.print()

        print("ConstVars --------")
        self.globalConst.print()
        print("-------- --------")
    
    def printLimits(self):
        print("Vars Start: ", self.varsStart)
        print("Temp Start: ", self.tempStart)
        print("Local Start: ", self.localStart)
        print("Const Start: ", self.constStart)
        print("Const Limit: ", self.constLimit)

    def getValue(self,virtualAddress):
        index, dataType, memoryObject = self.chooseMemory(virtualAddress)
        #print(index, dataType, memoryObject)

        value = 0
        
        if memoryObject == "vars":
            value = self.globalVars.getValue(index, dataType)
        elif memoryObject == "temp":
            value = self.globalTemp.getValue(index, dataType)
        elif memoryObject == "local":
            value = self.stackLocals[-1].getValue(index, dataType)
            #value = self.globalLocals.getValue(index, dataType)
        elif memoryObject == "const":
            value = self.globalConst.getValue(index, dataType)
        else: 
            print("error")

        return value

    def setValue(self,virtualAddress,value):

        index, dataType, memoryObject = self.chooseMemory(virtualAddress)

        if memoryObject == "vars":
            self.globalVars.setValue(index, dataType, value )
        elif memoryObject == "temp":
            self.globalTemp.setValue(index, dataType, value )
        elif memoryObject == "local":
            #self.globalLocals.setValue(index, dataType, value )
            self.stackLocals[-1].setValue(index, dataType, value)
        elif memoryObject == "const":
            self.globalConst.setValue(index, dataType, value)
        else: 
            print("error")
        
    def chooseMemory(self,virtualAddress):

        varsBases = 0
        nextBaseLimit = 0
        memoryObject = ""

        if self.varsStart <= virtualAddress < self.tempStart:
            #print("vars")
            varsBases = self.globalBases[0] # [1000,2000,3000]
            nextBaseLimit = self.globalBases[1][0] # 4000
            memoryObject = "vars"

        elif self.tempStart <= virtualAddress < self.localStart:
            #print("temp")
            varsBases = self.globalBases[1] # [4000,5000,6000,7000]
            nextBaseLimit = self.globalBases[2][0] # 8000
            memoryObject = "temp"

        elif self.localStart <= virtualAddress < self.constStart:
            #print("local")
            varsBases = self.globalBases[2]
            nextBaseLimit = self.globalBases[3][0]
            memoryObject = "local"

        elif self.constStart <= virtualAddress < self.constLimit:
            #print("const")
            varsBases = self.globalBases[3]
            nextBaseLimit = self.globalBases[3][-1] + 1000
            memoryObject = "const"

        else :
            print("tu address esta mal vuelva pronto :D")

        index, dataType = self.chooseDataType(virtualAddress, varsBases, nextBaseLimit)

        return index, dataType, memoryObject
 
    def chooseDataType(self, virtualAddress, currentBases, nextMemoryLimit):

        intsStart = currentBases[0] #1000
        floatStart = currentBases[1] # 2000
        charStart = currentBases[2] # 3000

        indexValue = virtualAddress
        currentBase = 0
        currentDataType = "error" 

        # 1001 - 1000 = 1

        if len(currentBases) == 4 :

            boolStart = currentBases[3] # 4000

            if intsStart <= virtualAddress < floatStart:
                currentBase = intsStart 
                currentDataType = "int"
            elif floatStart <= virtualAddress < charStart:
                currentBase = floatStart
                currentDataType = "float"
            elif charStart <= virtualAddress < boolStart:
                currentBase = charStart
                currentDataType = "char"
            elif boolStart <= virtualAddress < nextMemoryLimit:
                currentBase = boolStart
                currentDataType = "bool"
            else :
                print("tu address no existe, vuelva pronto :D")

        else :

            if intsStart <= virtualAddress < floatStart:
                currentBase = intsStart 
                currentDataType = "int"
            elif floatStart <= virtualAddress < charStart:
                currentBase = floatStart
                currentDataType = "float"
            elif charStart <= virtualAddress < nextMemoryLimit:
                currentBase = charStart
                currentDataType = "char"
            else :
                print("tu address no existe, vuelva pronto :D")
        
        indexValue -= currentBase

        return indexValue, currentDataType
 
