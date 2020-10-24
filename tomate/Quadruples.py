class Quadruple:
    def __init__(self,operator,left,right,temp,numQ):
        self.operator = operator
        self.left = left
        self.right = right
        self.temp = temp
        self.numQ = numQ

    def print(self):
        print("[ {} , {} , {} , {} , {}]".format( self.operator,
                                                self.left,
                                                self.right,
                                                self.temp,
                                                self.numQ
                                                ))


class Quadruples:

    def __init__(self):
        self.quadruples = []

    def add(self, quadruple):
        self.quadruples.append(quadruple)

    def print(self):
        for i in self.quadruples:
            i.print()

    def fillGoto(self,numF,contQ ):
        for i in self.quadruples:
            if i.numQ == numF:
                i.temp = contQ
    
    