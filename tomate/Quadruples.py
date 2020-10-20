class Quadruple:
    def __init__(self,operator,left,right,temp):
        self.operator = operator
        self.left = left
        self.right = right
        self.temp = temp

    def print(self):
        print("[ {} , {} , {} , {} ]".format( self.operator,
                                                self.left,
                                                self.right,
                                                self.temp
                                                ))


class Quadruples:

    def __init__(self):
        self.quadruples = []

    def add(self, quadruple):
        self.quadruples.append(quadruple)

    def print(self):
        for i in self.quadruples:
            i.print()