from Memory import DynamicMemory

class DynamicMemoryManager:
    def __init__(self, stackList):
        
        self.stackDictionary = {}
        self.nextDynamicMemory = 0

        self.dm = DynamicMemory(20) 

        for i in stackList:
            self.stackDictionary[i] = -1
     
    def setValue(self, listName, value):
        pointerBase = self.stackDictionary[listName]

        if pointerBase == -1:
            ndm = self.nextDynamicMemory
            self.stackDictionary[listName] = ndm

            self.dm.setValue(ndm, value)

        else :
            lastIndex = pointerBase
            nextPointer = self.dm.getPointer(pointerBase)
            
            while nextPointer != -1 :
                lastIndex = nextPointer
                nextPointer = self.dm.getPointer(lastIndex)
            
            
            ndm = self.nextDynamicMemory 
            self.dm.setValue(ndm, value)
            self.dm.setPointer(lastIndex,ndm)


        self.nextDynamicMemory += 1

        self.dm.printMemory()
        print(self.stackDictionary)

        #print(pointerBase)

    def print(self, listName):
        nextPointer = self.stackDictionary[listName]

        print('\'( ', end='')
        while nextPointer != -1 :
            value = self.dm.getValue(nextPointer)
            nextPointer = self.dm.getPointer(nextPointer)
            print( value , end=' ')
        print(')')

    def car(self, listName):
        pointerBase = self.stackDictionary[listName]

        if pointerBase != -1:
            return self.dm.getValue(pointerBase)

        else :
            return -1

    def cdr(self, listNameNew, listNameCopy):

        pointerBase = self.stackDictionary[listNameCopy]

        if pointerBase == -1:
            print("no tiene cdr(esta vacio)")
        else :

            nextPointer = self.dm.getPointer(pointerBase)

            if nextPointer == -1 :
                print("Lista vacia")
                self.stackDictionary[listNameNew] = -2

            else :
                self.stackDictionary[listNameNew] = nextPointer

        print(self.stackDictionary)

    def length(self,listName):
        pointerBase = self.stackDictionary[listName]

        lenAux = 1

        if pointerBase == -1 or pointerBase == -2  :
            return 0

        else :
            lastIndex = pointerBase
            nextPointer = self.dm.getPointer(pointerBase)
            
            while nextPointer != -1 :
                lastIndex = nextPointer
                nextPointer = self.dm.getPointer(lastIndex)
                lenAux += 1
            
        return lenAux

    def append(self,listToCopy, listToAppend):
        
        pointerBaseToAppend = self.stackDictionary[listToAppend]
        nextPointerToCopy = self.stackDictionary[listToCopy]

        while nextPointerToCopy != -1 :
            ndm = self.nextDynamicMemory 

            if nextPointerToCopy == self.stackDictionary[listToCopy] and pointerBaseToAppend != -1 :
                pointerLastList = pointerBaseToAppend + self.length(listToAppend) - 1
                self.dm.setPointer(pointerLastList,ndm)


            if pointerBaseToAppend == -1:
                self.stackDictionary[listToAppend] = ndm
                pointerBaseToAppend = ndm

            value = self.dm.getValue(nextPointerToCopy)

            self.dm.setValue(ndm,value)
            self.dm.setPointer(ndm,ndm+1)
            
            nextPointerToCopy = self.dm.getPointer(nextPointerToCopy)
        
            self.nextDynamicMemory += 1

        self.dm.setPointer(self.nextDynamicMemory -1 ,-1)

        self.dm.printMemory()
        print(self.stackDictionary)

    def filter(self, predicate, listToFilter, ListResult):
        pointerBaseToFilter = self.stackDictionary[listToFilter]
        pointerBaseResult = self.stackDictionary[ListResult]

        if predicate == "even" :

            while pointerBaseToFilter != -1 :
                value = self.dm.getValue(pointerBaseToFilter)
                pointerBaseToFilter = self.dm.getPointer(pointerBaseToFilter)

                if int(value % 2 == 0) :
                    
                    ndm = self.nextDynamicMemory 

                    if pointerBaseResult == -1:
                        self.stackDictionary[ListResult] = ndm
                        pointerBaseResult = ndm
                    else :
                        self.dm.setPointer( ndm - 1 , ndm )

                    self.dm.setValue(ndm,value)

                    self.nextDynamicMemory += 1

        print(self.stackDictionary)
