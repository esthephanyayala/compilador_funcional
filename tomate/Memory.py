class Memory:
    def __init__(self, ints, floats, chars, bools):
        self.int = [0] * ints
        self.float = [0] * floats
        self.char = [0] * chars
        self.bool = [0] * bools
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

class MemoryAux:
    def __init__(self, ints, floats, chars, bools):
        self.int = [0] * ints
        self.float = [0] * floats
        self.char = [0] * chars
        self.bool = [0] * bools

    def print(self):
        print("Ints: " + str(self.int))
        print("Floats: " + str(self.float))
        print("Chars: " + str(self.char))
        print("Bools: " + str(self.bool))

    def getValue(self, index, dataType):
        if dataType == "int":
            return self.int[index]
        elif dataType == "float":
            return self.float[index]
        elif dataType == "char":
            return self.char[index]
        elif dataType == "bool":
            return self.bool[index]
        else :
            return "This datatype doesn't exists, vuelva pronto :D"

    def setValue(self, index, dataType, value):
        if dataType == "int":
            self.int[index] = int(value)
        elif dataType == "float":
            self.float[index] = float(value)
        elif dataType == "char":
            self.char[index] = value
        elif dataType == "bool":
            self.bool[index] = value
        else :
            print("This datatype doesn't exists, vuelva pronto :D")
    
    #vm -> am -> all(memory)

    #vs = 1000
    #tS = 4000
    #lS = 8000
    #cS = 13000
    #cL = 16000