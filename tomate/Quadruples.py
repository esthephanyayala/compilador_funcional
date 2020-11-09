class Quadruple:
    def __init__(self,operator,left,right,temp):
        self.operator = operator
        self.left = left
        self.right = right
        self.temp = temp

    def assignTemp(self, temp):
        self.temp = temp

    def print(self):
        print("[ {} , {} , {} , {} ]".format( self.operator,
                                                self.left,
                                                self.right,
                                                self.temp
                                                ))
    def printNum(self,Num):
        print("{} : [ {} , {} , {} , {} ]".format( Num,
                                                        self.operator,
                                                        self.left,
                                                        self.right,
                                                        self.temp
                                                        ))                                      


class Quadruples:

    def __init__(self):
        self.quadruples = []
        self.cont = 0
        self.stackJumps = []

    def add(self, quadruple):
        self.quadruples.append(quadruple)
        self.cont += 1

    def print(self):
        print("Number of quads: " + str(self.cont))
        for i in range(0,self.cont):
            self.quadruples[i].printNum(i)
        print('Jumps')
        for i in self.stackJumps:
            print(i)

    def addGotoF(self,address):
        # saca del jump el cont del cuadruplo a llenar y le pone cont o cont+1 algo asi
        q = Quadruple("GOTOF",address,"NULL","NULL")
        self.add(q)
        self.addJump()

    def addGoto(self):
        q = Quadruple("GOTO","NULL","NULL","NULL")
        self.add(q)
        self.addJump()
    
    def fillGotoF(self):
        jump = self.stackJumps.pop()
        self.quadruples[jump].assignTemp(self.cont + 1)
    
    def fillGoto(self):
        jump = self.stackJumps.pop()
        self.quadruples[jump].assignTemp(self.cont)

    #def fillGotoAux(self):
        # saca del jump el cont del cuadroplo a llenar y le pone a que cont va ahora

    def addJump(self):
        self.stackJumps.append(self.cont - 1)
    
    def getCurrentQuad(self):
        return self.cont
