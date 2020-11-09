import os
from AddressManager import AddressManager

class VirtualMachine:
    def __init__(self):
        self.constTable = {}
        self.dirFunction = {}
        self.pointerManager = 0
        self.quadruples = []
        self.numberOfQuads = 0
        self.tgb = []
        self.tgs = []
       

        self.celia = []

        #function variables
        self.currentParams = []
        self.currentFunction = []
        self.migajitaDePan = []
        self.lastValue = []

    def initializeAddressManager(self):
        #tgb = [[1000, 2000, 3000], [4000, 5000, 6000, 7000], [8000, 9000, 10000, 12000], [13000, 14000, 15000]]
        #tgs = [[20, 20, 20], [20, 20, 20, 20], [20, 20, 20, 20], [20, 20, 20]]
        
        self.celia = AddressManager(self.tgb, self.tgs)
        self.fillConstMemory()
        
    def fillConstMemory(self):
        for i in self.constTable:
            self.celia.setValue(int(i) , self.constTable[i] )

    def loadOvejota(self):

        fileDir = os.path.dirname(os.path.realpath('__file__'))
        programa = 'ovj1.txt'
        #filename = os.path.join(fileDir, 'tomate/tests/' + programa )
        filename = os.path.join(fileDir, 'tests/' + programa )
        f = open(filename, "r")
        lines = f.readlines()

        status = 0
        contFunction = 0
        currentFunction = ""

        for i in lines:

            if i == "$$\n":
                status += 1
            
            if i != "$$\n" and status == 1: # We are reading const Table
                arrLine = i.split()

                const = arrLine[0]
                address = arrLine[1]

                self.constTable[address] = const
                

            elif i != "$$\n" and status == 2: # We are reading Quads
                arrLine = i.split()
                operator = arrLine[0]
                left = arrLine[1]
                right = arrLine[2]
                temp = arrLine[3]
                #print(operator, left, right, temp)

                self.quadruples.append([operator, left, right, temp])
                self.numberOfQuads += 1

            elif i != "$$\n" and status == 3: # We are reading Dir Function
                if i == "@@\n":
                    contFunction += 1
                
                if i != "@@\n" and contFunction == 1:
                    arrLine = i.split()

                    first = arrLine[0]

                    if first == "name":
                        currentFunction = arrLine[1]
                        self.dirFunction[currentFunction] = {"vars": {} }
                        
                    elif first == "vars":
                        rangeVars = int ( ( len(arrLine) - 1 ) / 3 )

                        for i in range(0 ,rangeVars):
                            start = int(i * 3)
                            variable = arrLine[1 + start]
                            type = arrLine[2 + start]
                            address = arrLine[3 + start]

                            self.dirFunction[currentFunction]["vars"][variable] = {"type" : type , "virtualAddress" : address }

                elif i != "@@\n" and contFunction > 1:
                    #print("no main")
                    arrLine = i.split()
                    first = arrLine[0]
                    #MEMORY AND TYPEPARAMS TIENEN VARIOS 
                    print("currentfunction", currentFunction)
                    if first == "name":
                        currentFunction = arrLine[1]
                        self.dirFunction[currentFunction] = {}
                    elif first  == "memory":
                        rangeMem = int ( ( len(arrLine) - 1 ) / 2 )
                        
                        memoryp = []
                        params = []
                        local = []
                        
                        for i in range(1, len(arrLine)): 
                            memoryp.append(int(arrLine[i]))
                        
                        for i in range(0 ,rangeMem):
                            params.append(memoryp[i])
                        
                        for i in range(rangeMem ,rangeMem*2):
                            local.append(memoryp[i])
                        
                        self.dirFunction[currentFunction][first] ={"params": params, "local": local}
                        #print(self.dirFunction)
                    
                    elif first == "typeParams":
                        #'typeParams': ['int', 'int']
                        typeParams = []
                        for i in range(1, len(arrLine)): 
                            typeParams.append(arrLine[i])
            
                        self.dirFunction[currentFunction][first] =typeParams
                        #print(self.dirFunction)


                    else:# first != "memory" and first != "typeParams" and first != "name":
                        self.dirFunction[currentFunction][first] = arrLine[1]
                        #print(self.dirFunction)

                    #print(self.dirFunction)    

                        


            elif i != "$$\n" and status == 4: # We are reading Temporal Global Sizes
                    arrLine = i.split()
                    
                    for i in range(0, len(arrLine)): 
                         arrLine[i] = int(arrLine[i])
                    
                    self.tgs.append(arrLine)

            elif i != "$$\n" and status == 5: # We are reading temporal Global Bases
                    arrLine = i.split()
                     
                    for i in range(0, len(arrLine)): 
                        arrLine[i] = int(arrLine[i])
                    
                    self.tgb.append(arrLine)


                    

        # esto es para probar, pero no deberia de estar :D
        #self.dirFunction['f1'] = {'type': 'int', 'quad': 5, 'memory': {'params': [2, 0, 0, 0], 'local': [2, 0, 0, 0]}, 'typeParams': ['int', 'int']}
        #self.dirFunction['f2'] = {'type': 'int', 'quad': 3, 'memory': {'params': [2, 0, 0, 0], 'local': [2, 0, 0, 0]}, 'typeParams': ['int', 'int']}
        print(self.dirFunction)
    def switch(self):

        # Get next Quad to be evaluated
        currentQuad = self.quadruples[self.pointerManager]

        # Get quad index
        operator = currentQuad[0]
        left = currentQuad[1]
        right = currentQuad[2]
        temp = currentQuad[3]

        #print(self.pointerManager, currentQuad)
        
        if operator == "print" :
            print(self.celia.getValue(int(temp)))

        elif operator == "=" :
            # Get the value of the address
            value = self.celia.getValue(int(left))
            
            # Set the value to temp address
            self.celia.setValue(int(temp),value)

            # if we are in a function we add the value to this stack in case it is the return
            if self.currentFunction != "" : 
                self.lastValue.append(value)
            
        elif operator == "+":

            # Get the value of the left address
            valueLeft = self.celia.getValue(int(left))

            # Get the value of the right address
            valueRight = self.celia.getValue(int(right))

            # Sum the values
            value = valueLeft + valueRight

            # Set the value to temp address
            self.celia.setValue(int(temp),value)

            # if we are in a function we add the value to this stack in case it is the return
            if self.currentFunction != "" :
                self.lastValue.append(value)

        elif operator == "-":

            valueLeft = self.celia.getValue(int(left))
            valueRight = self.celia.getValue(int(right))
           
            value = valueLeft - valueRight

            self.celia.setValue(temp,value)

        elif operator == "GOTO":
            # pointer manager is equal to temp - 1 (at the end of the switch there is a + 1 thats the reason)
            self.pointerManager = int(temp) - 1

        elif operator == "ERA":
            # We enter a new scope so we added to a new currentFunction
            # and a new params array
            self.currentFunction.append(temp)
            self.currentParams.append([])

        elif operator == "param":

            # Get the value of the left address
            value = self.celia.getValue(int(left))
 
            # Append the value to the array in the last position of currentParams
            self.currentParams[-1].append( value ) 

        elif operator == "GOSUB":
            # GOSUB means going to the quads of a function
            # we change the pointer manager
            # initialize a new memory on the stack of local memories inside Celia
            # and save the migajita of pan 

            self.fillParamsFunction()
            self.migajitaDePan.append(self.pointerManager)
            self.pointerManager = int(temp) - 1
        
        elif operator == "ENDFUNC":
            # At the ENDFUNC if the function is not void then we set the value of the address of the function
            # to the last value inside lastValue stack


            #print(self.lastValue)
            objectVars = self.dirFunction["factorial"]["vars"]

            if self.currentFunction[-1] in objectVars:

                address = objectVars[self.currentFunction[-1]]["virtualAddress"]
                self.celia.setValue( int(address) , self.lastValue.pop() )

            # Pop the local memory of the function
            self.celia.popLocalMemory()

            # Pop the current function to the function stacks
            self.currentFunction.pop()

            # Pop the currentParams 
            self.currentParams.pop()

            # Switch the pointer manager to the last migajita of pan
            self.pointerManager = self.migajitaDePan.pop()

            # Pop the lastValue array
            self.lastValue.pop()

        elif operator == "GOTOF":
            
            lastQuad = self.quadruples[self.pointerManager - 1]
           
            opLQ = lastQuad[0]
            leftLQ = lastQuad[1]
            rightLQ = lastQuad[2]
            
            valueLeftLQ = self.celia.getValue(int(leftLQ))
            valueRightLQ = self.celia.getValue(int(rightLQ))

            valueTrue = 1
            valueFalse = 0
            
            if opLQ == ">":
                if valueLeftLQ > valueRightLQ :
                   
                    self.celia.setValue(int(left),valueTrue)
                else:
                    
                    self.celia.setValue(int(left),valueFalse)
            elif opLQ  == "<":
                if valueLeftLQ < valueRightLQ :
                
                    self.celia.setValue(int(left),valueTrue)
                else:
                  
                    self.celia.setValue(int(left),valueFalse)
            elif opLQ  == "!=":
                if valueLeftLQ != valueRightLQ :
                  
                    self.celia.setValue(int(left),valueTrue)
                else:
                    
                    self.celia.setValue(int(left),valueFalse)
            elif opLQ == "=":
                if valueLeftLQ == valueRightLQ :
                   
                    self.celia.setValue(int(left),valueTrue)
                else:
                    
                    self.celia.setValue(int(left),valueFalse)
            else:
                print("Operador no existe")
            resultValue = self.celia.getValue(int(left))
            
            if resultValue == 0:
                self.pointerManager = temp - 1
            
                  
        
        self.pointerManager += 1

    def pointerSomething(self):
        while self.pointerManager < self.numberOfQuads:
            self.switch()

    def getMemorySizeFunction(self,funcName):
        memoryObj = self.dirFunction[funcName]['memory']
        paramsMemory = memoryObj['params']
        localMemory = memoryObj['local']

        sizeFunction = [
                            paramsMemory[0] + localMemory[0],
                            paramsMemory[1] + localMemory[1],
                            paramsMemory[2] + localMemory[2],
                            paramsMemory[3] + localMemory[3]
                        ]
        self.celia.addLocalMemory(sizeFunction)

    def fillParamsFunction(self):
        # This function is used after we gather the params of one function 
        # to give the address to the new function

        #print(self.currentParams)

        basesLocals = [8000, 9000, 10000, 12000]

        paramsCurrentFunction = self.dirFunction[self.currentFunction[-1]]['typeParams'].copy()

        self.getMemorySizeFunction(self.currentFunction[-1])
        paramsAux = self.currentParams[-1]

        #print(paramsCurrentFunction)
        
        for i in range(0, len(paramsCurrentFunction)):
            if paramsCurrentFunction[i] == "int":
                addressTemp = basesLocals[0]
                basesLocals[0] += 1
            elif paramsCurrentFunction[i] == "float":
                addressTemp = basesLocals[1]
                basesLocals[1] += 1
            elif paramsCurrentFunction[i] == "char":
                addressTemp = basesLocals[2]
                basesLocals[2] += 1
            elif paramsCurrentFunction[i] == "bool":
                addressTemp = basesLocals[3]
                basesLocals[3] += 1
            
            self.celia.setValue( addressTemp , paramsAux.pop() )

    def printConstTable(self):
        print(self.constTable)
    
    def printFunctions(self):
        print(self.dirFunction)

    def printQuadruples(self):
        for i in self.quadruples:
            print(i)
