from Quadruples import *
import os
from Memory import Memory

class VirtualMachine:
    def __init__(self):
        self.quadruples = Quadruples()
        self.constTable = {}
        self.dirFunction = {}
        self.const = Memory(0) 
        self.pointerManager = 0
        self.quadruplesAux = []
        self.numberOfQuads = 0
        self.globalVars = Memory(2)

    def printConstTable(self):
        print(self.constTable)
    
    def printFunctions(self):
        print(self.dirFunction)

    def printQuadruples(self):
        for i in self.quadruplesAux:
            print(i)

    def loadOvejota(self):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        programa = 'ovejota.txt'
        filename = os.path.join(fileDir, 'tomate/tests/' + programa )
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

                self.quadruplesAux.append([operator, left, right, temp])
                self.numberOfQuads += 1

            elif i != "$$\n" and status == 3: # We are reading Quads
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
                    print("no main")

            
    def createMemory(self):
        self.const = Memory(2)
        for i in self.constTable:
            self.const.add( int(i) , self.constTable[i] )

    def changeValueMemory(self,address,value):
        #print(address, value)
        self.globalVars.addGlobal(int(address),value)

    def printConstMemory(self):
        self.const.print()

    def addressManager(self,address):
        addressInt = int(address) 
        if addressInt >= 13000 and addressInt < 16000:
            return self.const.getValue(addressInt)
        if addressInt >= 1000 and addressInt < 2000:
            return self.globalVars.getValueGlobal(addressInt)

    def switch(self):
        currentQuad = self.quadruplesAux[self.pointerManager]
        operator = currentQuad[0]
        left = currentQuad[1]
        right = currentQuad[2]
        temp = currentQuad[3]
        
        if operator == "print" :
            print(self.addressManager(temp))
        elif operator == "=" :
            value = self.addressManager(left)
            #print(temp)
            self.changeValueMemory(temp,value)
            #print(self.addressManager(temp))

        self.pointerManager += 1

    def pointerSomething(self):
        while self.pointerManager < self.numberOfQuads:
            self.switch()

        
    

## refactoring que memory reciba la base y no tener que crear add y addGlobal
## recibir el tamano de memory para las que necesitamos, consts, globales, locakes
## memory recibar tambien floats, chars, bools
    # obviamente tambien hacer el handling de sus mamadas
# ir pensando en el stack de variables Locales aka stack de segmentos
# next step suma
    # crear memoria temporal global
#lalo-cal
