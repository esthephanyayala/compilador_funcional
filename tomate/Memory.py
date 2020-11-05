class Memory:
    def __init__(self, ints):
        self.int = [0] * ints
        #print(self.int)

    def add(self,index , value):
        base = 13000
        self.int[index - base] = value

    def addGlobal(self,index , value):
        base = 1000
        #print(self.int)
        self.int[index - base] = value

    def print(self):
        print(self.int)

    def getValue(self, index):
        base = 13000
        return self.int[index - base] 

    def getValueGlobal(self,index):
        base = 1000
        return self.int[index - base] 