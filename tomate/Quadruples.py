class Quadruple:
    def __init__(self,operator,left,right,temp,lo,ro,to,lt,rt,tt):
        self.operator = operator
        self.left = left
        self.right = right
        self.temp = temp
        self.leftObject = lo
        self.rightObject = ro
        self.tempObject = to
        self.leftType = lt
        self.rightType = rt
        self.tempType = tt

    def print(self):
        print("[ {} , [ {} , {}, {} ] , [ {} , {}, {} ] , {} ]".format( self.operator,
                                                                        self.left,
                                                                        self.leftType,
                                                                        self.leftObject,
                                                                        self.right,
                                                                        self.rightType,
                                                                        self.rightObject,
                                                                        self.temp))

class Quadruples:
    quadruples = []

    def add(self,quadruple):
        self.quadruples.append(quadruple)

    def print(self):
        print(self.quadruples)