import os
from Memory import Memory
from AddressManager import AddressManager

class VirtualMachine:
    def __init__(self):
        self.constTable = {}
        self.dirFunction = {}
        self.pointerManager = 0
        self.quadruples = []
        self.numberOfQuads = 0

        self.celia = []
        #self.initializeAddressManager()

    def initializeAddressManager(self):
        tgb = [[1000, 2000, 3000], [4000, 5000, 6000, 7000], [8000, 9000, 10000, 12000], [13000, 14000, 15000]]
        tgs = [[2, 1, 1], [1, 0, 0, 0], [0, 0, 0, 0], [2, 1, 1]]
        self.celia = AddressManager(tgb, tgs)
        #self.celia.printMemory()
        #self.celia.printLimits()
        #self.celia.setValue(4000,1)
        #self.celia.getValue(4000)
        
        self.fillConstMemory()
        #self.celia.printMemory()

    def fillConstMemory(self):
        #self.const = Memory(4,1,1,0)
        for i in self.constTable:
            self.celia.setValue(int(i) , self.constTable[i] )
        self.celia.printMemory()

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

                self.quadruples.append([operator, left, right, temp])
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

    def switch(self):
        currentQuad = self.quadruples[self.pointerManager]
        operator = currentQuad[0]
        left = currentQuad[1]
        right = currentQuad[2]
        temp = int( currentQuad[3] )
        
        if operator == "print" :
            print(self.celia.getValue(temp))

        elif operator == "=" :
            value = self.celia.getValue(int(left))

            self.celia.setValue(temp,value)
            
        elif operator == "+":

            valueLeft = self.celia.getValue(int(left))
            valueRight = self.celia.getValue(int(right))

            value = valueLeft + valueRight

            self.celia.setValue(temp,value)

        elif operator == "GOTO":
            self.pointerManager = temp - 1
        
        self.pointerManager += 1
        #print("pointer:" , self.pointerManager)

    def pointerSomething(self):
        while self.pointerManager < self.numberOfQuads:
            self.switch()

        #self.celia.printMemory()

## refactoring que memory reciba la base y no tener que crear add y addGlobal
## recibir el tamano de memory para las que necesitamos, consts, globales, locakes
## memory recibar tambien floats, chars, bools
    # obviamente tambien hacer el handling de sus mamadas
# ir pensando en el stack de variables Locales aka stack de segmentos
# next step suma
    # crear memoria temporal global
#lalo-cal


    def printConstTable(self):
        print(self.constTable)
    
    def printFunctions(self):
        print(self.dirFunction)

    def printQuadruples(self):
        for i in self.quadruples:
            print(i)
