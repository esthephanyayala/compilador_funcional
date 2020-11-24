from lexer import tokens
from Quadruples import *
from CuboSemantico import semanticCube
from VirtualMachine import *

quadruples = Quadruples()

ultTipo = []

dirFunctions = {}

queueParams = []
stackOperadores = []
stackOperandos = []
stackTypes = []
stackScope = []
stackConst = []
stackParams = []
scopeGlobal = ""
contCondiciones = 0
contParamLambda = 0
contLambdas = 0
contLists = 0
globalMemory = []
sizeMap = 0
#stackLists = []

stackListsAux = []
stackListsAuxComplete = []

# Virtual Address
address = { 
            "global" :  {
                            "int":  1000, 
                            "float":2000,
                            "char": 3000
                        },
            "temp" :    {
                            "int":  4000, 
                            "float":5000,
                            "char": 6000,
                            "bool": 7000
                        },
            "local":    {
                        "int": 8000,
                        "float": 9000,
                        "char": 10000,
                        "bool": 12000
                        },
            "const":    {
                        "int": 13000,
                        "float": 14000,
                        "char": 15000
                        }
        }

addressBases = { 
            "global" :  {
                            "int":  1000, 
                            "float":2000,
                            "char": 3000
                        },
            "temp" :    {
                            "int":  4000, 
                            "float":5000,
                            "char": 6000,
                            "bool": 7000
                        },
            "local":    {
                        "int": 8000,
                        "float": 9000,
                        "char": 10000,
                        "bool": 12000
                        },
            "const":    {
                        "int": 13000,
                        "float": 14000,
                        "char": 15000
                        }
        }

constTable = {}

def getAddress(addressType,type):

    # When we are in a function we save types we use
    if addressType == "temp" and not(boolScopeGlobal()):# and dirFunctions[stackScope[-1]]["type"] != "lambda" :
        
        #currentScope = stackScope[-1]
        
        #print(dirFunctions[currentScope]["type"])
        #if dirFunctions[currentScope]["type"] != "lambda":
        addressType = "local"

    ad = address[addressType][type]
    address[addressType][type] += 1
    return ad

def boolScopeGlobal():
    currentScope = stackScope[-1]
    return currentScope == scopeGlobal

def globalVariables():
    addressGlobal = address["global"]
    addressTemp = address["temp"]
    addressLocal = address["local"]
    addressConst = address["const"]

    addressGlobalB = addressBases["global"]
    addressTempB = addressBases["temp"]
    addressLocalB = addressBases["local"]
    addressConstB = addressBases["const"]

    globalInts = addressGlobal["int"] - addressGlobalB["int"]
    globalFloats = addressGlobal["float"] - addressGlobalB["float"]
    globalChars = addressGlobal["char"] - addressGlobalB["char"]

    tempInts = addressTemp["int"] - addressTempB["int"]
    tempFloats = addressTemp["float"] - addressTempB["float"]
    tempChars = addressTemp["char"] - addressTempB["char"]
    tempBools = addressTemp["bool"] - addressTempB["bool"]

    localInts = addressLocal["int"] - addressLocalB["int"]
    localFloats = addressLocal["float"] - addressLocalB["float"]
    localChars = addressLocal["char"] - addressLocalB["char"]
    localBools = addressLocal["bool"] - addressLocalB["bool"]

    contsInts = addressConst["int"] - addressConstB["int"]
    contsFloats = addressConst["float"] - addressConstB["float"]
    contsChars = addressConst["char"] - addressConstB["char"]

    global globalMemory

    globalMemory = [
                    [globalInts, globalFloats, globalChars],
                    [tempInts, tempFloats, tempChars, tempBools],
                    [localInts, localFloats, localChars, localBools],
                    [contsInts, contsFloats, contsChars]
                ]
    

##### PROGRAMA #####

def p_programa(p):
    ''' programa : OPEN_PAREN PROGRAM ID np_dirProgram programa_2 np_first_quad programa_3 np_fill_goto_main main CLOSE_PAREN'''
    
def p_np_first_quad(p):
    ''' np_first_quad : '''
    quadruples.addGoto()

def p_np_fill_goto_main(p):
    ''' np_fill_goto_main : '''
    quadruples.fillGoto()

def p_np_dirProgram(p):
    ''' np_dirProgram : '''
    programName = p[-1]
    dirFunctions[programName] = {"vars": {}}
    stackScope.append(programName)

    global scopeGlobal
    scopeGlobal = programName
    

def p_programa_2(p):
    ''' programa_2  : declaracionvariables
                    | empty '''

def p_programa_3(p):
    ''' programa_3  : declaracionfuncion
                    | empty '''

##### IMPRIMIR #####

def p_imprimir(p):
    ''' imprimir : OPEN_PAREN PRINT imprimir_2 CLOSE_PAREN '''
    address = stackOperandos.pop()
    stackTypes.pop()
    
    q = Quadruple("print","NULL","NULL", address)
    quadruples.add(q)

def p_imprimir_2(p):
    ''' imprimir_2  : CTEC np_stackCTEC
                    | expresion
                    | lambda
                    | listfunctions
    ''' 
    # e que pedo hay que agregar condicion aqui alv

def p_imprimirlista(p):
    ''' imprimirlista : OPEN_PAREN PRINTLISTA returnlist CLOSE_PAREN '''
    objList = stackListsAux.pop()
    name = objList[0]

    q = Quadruple("printlist","NULL","NULL", name)
    quadruples.add(q)


    '''
    print("printlist")

    objList = stackLists.pop()
    type = objList[0]
    base = objList[1]
    size = objList[2]

    q = Quadruple("printlist","NULL","NULL", objList)
    quadruples.add(q)

    print(type,base,size)

    
    print(stackLists)
    
    objList = dirFunctions[scopeGlobal]["vars"]['l']

    if "list" in objList :
        #print("kha")
        base = objList['virtualAddress']
        size = objList['list']
        
        q = Quadruple("printlist",size,"NULL", base)
        quadruples.add(q)

    else :
        print("Id provided is not a function")
    
        #print(objList)
    #print(p[3])
    '''


##### EXPRESION #####

def p_expresion(p):
    ''' expresion   : exp 
                    | OPEN_PAREN signosrelacionales exp exp CLOSE_PAREN 
                    | expresionesunarias'''

    #solo para el segundo caso (> i j)
    if len(p) == 6:

        #operator 
        operator = stackOperadores.pop()

        #right
        right = stackOperandos.pop()
        rightType = stackTypes.pop()

        #left 
        left = stackOperandos.pop()
        leftType = stackTypes.pop()

        # check semanticCube
        semanticCubeType = semanticCube[leftType][rightType][operator]
        
        if semanticCubeType != 'ERROR':
                
            ad = getAddress("temp",semanticCubeType)

            stackOperandos.append(ad)
            stackTypes.append(semanticCubeType)

            q = Quadruple(operator,left,right,ad)
            
            quadruples.add(q)

        else :
            print("Error de compilacion")


##### SIGNOSRELACIONALES #####

def p_signosrelacionales(p):
    ''' signosrelacionales  : LT 
                            | GT
                            | NE
                            | EQUAL '''
    stackOperadores.append(p[1])

##### EXPRESIONESUNARIAS #####

def p_expresionesunarias(p):
    ''' expresionesunarias  : OPEN_PAREN expresionesunarias_2 exp CLOSE_PAREN 
                            | TRUE
                            | FALSE '''
    #solo primer caso (int? i)
    if len(p) == 5:

        #operator == 6:
        operator = stackOperadores.pop()

        #left  
        left = stackOperandos.pop()
        leftType = stackTypes.pop()

        semanticCubeType = 'bool'
        ad = getAddress("temp", semanticCubeType)
        stackOperandos.append(ad)
        stackTypes.append(semanticCubeType)

        q = Quadruple(operator,left,"NULL",ad)
        quadruples.add(q)
    
    else: ## para 2do y 3er caso
        
        ad = getAddress("temp","bool")

        if p[1] == 'tt':
            q = Quadruple("TRUE","NULL","NULL",ad)
        else :
            q = Quadruple("FALSE","NULL","NULL",ad)
        quadruples.add(q)

        stackOperandos.append(ad)
        stackTypes.append("bool")

        

def p_expresionesunarias_2(p):
    ''' expresionesunarias_2    : EVEN_PREDICATE 
                                | INT_PREDICATE
                                | FLOAT_PREDICATE
                                | LIST_PREDICATE
                                | NULL_PREDICATE
                                | EMPTY_PREDICATE '''
    stackOperadores.append(p[1])
    
##### EXP #####

def p_exp(p):
    ''' exp : OPEN_PAREN signos1 exp exp CLOSE_PAREN
            | OPEN_PAREN signos2 exp exp CLOSE_PAREN
            | varcte 
            | llamada 
            | returnelement
            | lambda''' 

    if len(p) == 6:

        # operator
        operator = stackOperadores.pop()

        # right
        right = stackOperandos.pop()
        rightType = stackTypes.pop()

        # left
        left = stackOperandos.pop()
        leftType = stackTypes.pop()

        # check semanticCube
        semanticCubeType = semanticCube[leftType][rightType][operator]

        if semanticCubeType != 'ERROR':
            ad = getAddress("temp",semanticCubeType)

            stackOperandos.append(ad)
            stackTypes.append(semanticCubeType)
            
            q = Quadruple(operator,left,right,ad)
            quadruples.add(q)   
            
        else :
            print("Error de compilacion")    



##### SIGNOS 1 #####

def p_signos1(p):
    '''signos1 : PLUS 
                | MINUS ''' 
    stackOperadores.append( p[1] )
    #print(p[1])
    

##### SIGNOS 2 #####

def p_signos2(p):
    '''signos2 : TIMES 
                | DIVIDE '''
    stackOperadores.append( p[1] )

##### VARCTE #####

def p_varcte(p):
    ''' varcte : ID np_stackCTEID
                | CTEI np_stackCTEI
                | CTEF np_stackCTEF '''


def p_np_stackCTEID(p):
    '''np_stackCTEID : '''
    value = p[-1]

    currentScope = stackScope[-1]

    varibleFound = False
    valueObject = []

    # La primera condicion verifica si estamos en el scope de una funcion
    # la segunda condicion verifica si esta la variable dentro de las variables de la funcion se guarda el value
    if not(boolScopeGlobal()) and value in dirFunctions[currentScope]["vars"]:
        varibleFound = True            
        valueObject = dirFunctions[currentScope]["vars"][value] 

    # la primera condicion es para verificar si aun estando en un scope de funcion no se encontro la variable en su scope,
    # buscarla en el scope global
    # y la segunda condicion es para verificar si existe
    if not(varibleFound) and value in dirFunctions[scopeGlobal]["vars"]:
        varibleFound = True
        valueObject = dirFunctions[scopeGlobal]["vars"][value] 

    
    # Condicion final para verificar si se encontro la variable, si no poder marcar el error correspondiente
    if not(varibleFound) :
        print("Variable {} not found".format(value))
    else :
        if 'list' in valueObject :
            stackListsAux.append([value,valueObject["type"],valueObject["size"]])
        else :
            address = valueObject['virtualAddress']
            type = valueObject['type']

            stackOperandos.append(address)
            stackTypes.append(type)
  
def p_np_stackCTEI(p):
    '''np_stackCTEI : '''
    value = p[-1]
    
    if value in constTable:
        addressConst = constTable[value]
    else:
        addressConst = getAddress("const","int")
        constTable[value] = addressConst

    stackOperandos.append(addressConst)
    stackTypes.append("int")
    
def p_np_stackCTEF(p):
    '''np_stackCTEF : '''

    value = p[-1]
    
    if value in constTable:
        addressConst = constTable[value]
    else:
        addressConst = getAddress("const","float")
        constTable[value] = addressConst

    stackOperandos.append(addressConst)
    stackTypes.append("float")

def p_np_stackCTEC(p):
    '''np_stackCTEC : '''

    value = p[-1]
    
    if value in constTable:
        addressConst = constTable[value]
    else:
        addressConst = getAddress("const","char")
        constTable[value] = addressConst

    stackOperandos.append(addressConst)
    stackTypes.append("char")

##### DECLARACIONFUNCION #####

def p_declaracionfuncion(p):
    ''' declaracionfuncion : OPEN_PAREN FUNCTIONS declaracionfuncion_2 CLOSE_PAREN '''
  

def p_declaracionfuncion_2(p):
    ''' declaracionfuncion_2    : funcion declaracionfuncion_2 
                                | empty'''

##### FUNCION #####

def p_funcion(p):
    ''' funcion : OPEN_PAREN DEFINE OPEN_PAREN OPEN_PAREN tipo ID np_create_dirFunc CLOSE_PAREN typeparam np_varTabFunc CLOSE_PAREN bloque CLOSE_PAREN np_finish_function '''

def p_np_finish_function(p):
    ''' np_finish_function : '''
    funcName = stackScope.pop()
    
    global stackOperadores
    global stackOperandos
    global stackTypes
    global address
    global contCondiciones


    objectVars = dirFunctions[scopeGlobal]['vars']

    if funcName in objectVars:

        returnType = objectVars[funcName]["type"]
        numberOfReturnExpected = 1 + contCondiciones
        lenStack = len(stackOperandos)

        if numberOfReturnExpected != lenStack :
            print("Number of returns doesn't match the function {}".format(funcName))
        else :
            for _ in range(0,lenStack):
                currentTypeCheck = stackTypes.pop()
                if currentTypeCheck != returnType :
                    print("Return type doesn't the return type of the function {}".format(funcName))
            
    stackOperadores = []
    stackOperandos = []
    stackTypes = []

    localAddress = address["local"]
    localAddressBases = addressBases["local"]
    memoryObject = dirFunctions[funcName]["memory"]
    paramsFunction = memoryObject["params"]
    localMemory = memoryObject["local"]
    
    localInts = localAddress["int"] - localAddressBases["int"] - paramsFunction[0]
    localFloats = localAddress["float"] - localAddressBases["float"] - paramsFunction[1]
    localChars = localAddress["char"] - localAddressBases["char"] - paramsFunction[2]
    localBools = localAddress["bool"] - localAddressBases["bool"] - paramsFunction[3]

    localMemory[0] = localInts
    localMemory[1] = localFloats
    localMemory[2] = localChars
    localMemory[3] = localBools

    #print("local: " , localInts, localFloats , localChars , localBools)

    # Reset Temporal Address used by current Function
    address["local"] = addressBases["local"].copy()

    # Erase Vars from current function on dirFunctions
    del dirFunctions[funcName]["vars"]
    
    # Reset contCondiciones to zero
    contCondiciones = 0

    # Quadruple to end function
    q = Quadruple("ENDFUNC","NULL","NULL", "NULL")
    quadruples.add(q)

def p_np_create_dirFunc(p):
    ''' np_create_dirFunc : '''   
    funcName = p[-1]
    dirFKeys = list(dirFunctions)
 
    #para dirFunction
    if funcName in dirFunctions:
        print("function {} already declare".format(funcName))
    else:      
        currentQuad = quadruples.getCurrentQuad()
        stackScope.append(funcName)
        typeFunc = stackTypes.pop()
        memoryObject = {"params":[0,0,0,0],
                        "local":[0,0,0,0]}
        dirFunctions[funcName] = {"type":typeFunc, "quad": currentQuad, "vars" : {}, "memory":memoryObject} #dirFunction

        # if function is not void then push to var table
        if typeFunc != 'void':
            ad = getAddress("global",typeFunc)
            dirFunctions[dirFKeys[0]]['vars'][funcName] = {"type": typeFunc , "virtualAddress":ad}
    

def p_np_varTabFunc(p):
    ''' np_varTabFunc : '''
    funcName = p[-4]

    typesParam = []
    paramsMemory = dirFunctions[funcName]["memory"]["params"]
    
    for i in range(0,len(stackOperandos)):
        typeParam = stackTypes.pop()
        
        # add += 1 to memory
        if typeParam == "int":
            paramsMemory[0] += 1
        elif typeParam == "float":
            paramsMemory[1] += 1
        elif typeParam == "char":
            paramsMemory[2] += 1
        else :
            paramsMemory[3] += 1

        idparam = stackOperandos.pop()
        ad = getAddress("local", typeParam)
        typesParam.append(typeParam)
        paramsCar = {"type": typeParam, "virtualAddress": ad }
        dirFunctions[funcName]['vars'][idparam] = paramsCar
        
    dictTypes = {"typeParams": typesParam}

    dirFunctions[funcName]["memory"]
    dirFunctions[funcName].update(dictTypes)
    #print("param", typesParam)
   

##### TYPEPARAM #####

def p_typeparam(p):
    ''' typeparam  : tipovars ID np_idparam typeparam
                    | empty ''' 
    p[0] = p[-1]

def p_np_idparam(p):
    ''' np_idparam : '''
    #print(p[-1])
    stackOperandos.append(p[-1])

##### PARAM #####

def p_param(p):
    ''' param   : ID np_append_to_paramStack param 
                | empty '''

def p_np_append_to_paramStack(p):
    ''' np_append_to_paramStack : '''
    stackParams.append(p[-1])

##### DECLARACIONVARIABLES #####

def p_declaracionvariables(p):
    ''' declaracionvariables : OPEN_PAREN VARS declaracionvariables_2 CLOSE_PAREN '''


def p_declaracionvariables_2(p):
    ''' declaracionvariables_2 : declare declaracionvariables_2
                                | empty '''

##### DECLARE #####

def p_declare(p):
    ''' declare : OPEN_PAREN DECLARE ID declare_2 np_create_varTable CLOSE_PAREN '''
    #print("declare2 :", p[5])    

def p_np_create_varTable(p):
    ''' np_create_varTable : '''
    varId = p[-2] # o mejor poner vars
    dirFKeys = list(dirFunctions)

    global ultTipo

    if varId in dirFunctions[dirFKeys[0]]['vars']:
        print("variable {} already declare".format(varId))
    else:
        type = ultTipo[-1]

        if ultTipo[-1] == 'lista':
            #print("hay lista")
            ultTipo.pop()

            lenList = len(ultTipo)
            typeList = ultTipo[0]

            dirFunctions[dirFKeys[0]]['vars'][varId] = {"list":"1","type": typeList, "size":lenList}

            #stackListsAux.append([varId,typeList])
            stackListsAuxComplete.append([varId,lenList,typeList])
             
            for i in range(0, lenList ):
                if typeList != ultTipo[i]:
                    print("Type mismatch inside list declare")
                
                value = stackConst.pop(0)

                if value in constTable:
                    addressConst = constTable[value]
                else:
                    addressConst = getAddress("const",typeList)
                    constTable[value] = addressConst

                q = Quadruple("NDM",addressConst,"NULL", varId ) 
                quadruples.add(q)

                #else :
                    
            ultTipo = []

            #print("here:",ultTipo)
            #print(stackConst)
            #print("len: ", lenList)
            '''
            for i in range(0, lenList ):
                #print(i)
                #print(stackConst)
                addressDirFunction = getAddress("global",typeList)

                # if const ya existe
                value = stackConst.pop(0)
                
                if value in constTable:
                    addressConst = constTable[value]
                else:
                    addressConst = getAddress("const",typeList)
                    constTable[value] = addressConst

                q = Quadruple("=",addressConst,"NULL", addressDirFunction ) 
                quadruples.add(q)

                if i == 0:
            '''
            

        else :

            addressDirFunction = getAddress("global",type)

            # if const ya existe
            value = stackConst.pop()
            
            if value in constTable:
                addressConst = constTable[value]
            else:
                addressConst = getAddress("const",type)
                constTable[value] = addressConst

            q = Quadruple("=",addressConst,"NULL", addressDirFunction ) 
            quadruples.add(q)
            
            dirFunctions[dirFKeys[0]]['vars'][varId] = {"type": ultTipo.pop() , "virtualAddress":addressDirFunction}

def p_declare_2(p):
    ''' declare_2   : definircte
                    | definirlista'''
    
##### DEFINIRCTE #####

def p_definircte(p):
    ''' definircte  : CTEI np_definicioni
                    | CTEF np_definicionf
                    | CTEC np_definicionc '''
    stackConst.append(p[1])
  
def p_np_definicioni(p):
    ''' np_definicioni : '''
    ultTipo.append("int")

def p_np_definicionf(p):
    ''' np_definicionf : '''
    ultTipo.append("float")

def p_np_definicionc(p):
    ''' np_definicionc : '''
    ultTipo.append("char")

##### DEFINIRLISTA #####

def p_definirlista(p):
    ''' definirlista : QUOTE OPEN_PAREN definirlista_2 CLOSE_PAREN '''
    ultTipo.append("lista")

def p_definirlista_2(p):
    ''' definirlista_2  : definircte definirlista_2
                        | empty'''


##### LISTA #####
def p_np_fondo_falso_lista(p):
    ''' np_fondo_falso_lista : '''
    ultTipo.append("*")

def p_lista(p):
    ''' lista : ID np_push_data_to_stack
              | QUOTE OPEN_PAREN np_fondo_falso_lista lista_2 CLOSE_PAREN
    '''
    if p[1] == '\'':
        global contLists
        newList = 'listAux' + str(contLists)
        contLists += 1
        listSize = 0

        stackTypesAux = []

        currentType = ultTipo.pop()
        listType = currentType

        while currentType != "*":
            if currentType != listType:
                print("Type mistmatch list definition")
            else:
                stackTypesAux.append(currentType)
                currentType = ultTipo.pop()

        listSize = len(stackTypesAux)

        for _ in range(0, listSize ):
            value = stackConst.pop()

            if value in constTable:
                addressConst = constTable[value]
            else:
                addressConst = getAddress("const",listType)
                constTable[value] = addressConst

            q = Quadruple("NDM", addressConst ,"NULL", newList)
            quadruples.add(q)

        stackListsAux.append([newList, listType, listSize])
        stackListsAuxComplete.append([newList, listSize])


    '''
    
    if len(p) > 3:
        global ultTipo
        stackConst.pop(0)


        lenList = len(ultTipo)
        typeList = ultTipo.pop(0)
            
        for i in range(0, lenList - 1 ):
            if typeList != ultTipo[i]:
                print("Type mismatch inside list declare")
            #else :
                
        ultTipo = []

        for i in range(0, lenList ):
            addressDirFunction = getAddress("temp",typeList)

            # if const ya existe
            value = stackConst.pop()
            
            if value in constTable:
                addressConst = constTable[value]
            else:
                addressConst = getAddress("const",typeList)
                constTable[value] = addressConst

            q = Quadruple("=",addressConst,"NULL", addressDirFunction ) 
            quadruples.add(q)

            if i == 0:
                stackLists.append([typeList, addressDirFunction, lenList ])
    '''

def p_np_push_data_to_stack(p):
    ''' np_push_data_to_stack : '''
    ##cambiar a checar si existe la variable primero
    objList = dirFunctions[scopeGlobal]["vars"][p[-1]]

    if "list" in objList :
        type = objList['type']
        size = objList['size']

        stackListsAux.append([p[-1],type,size])

    else:
        print("The Id provided is not a list")


    '''
    if "list" in objList :
        base = objList['virtualAddress']
        size = objList['list']
        type = objList['type']

        stackLists.append([type,base,size])
    '''

def p_lista_2(p):
    ''' lista_2 : CTEI np_definicioni lista_2
                | CTEF np_definicionf lista_2
                | CTEC np_definicionc lista_2
                | empty
    '''
    stackConst.append(p[1])

##### LISTFUNCTIONS #####
def p_listfunctions(p):
    ''' listfunctions : returnelement
                      | returnlist
    '''

##### RETURNLIST #####
def p_returnlist(p):
    ''' returnlist : OPEN_PAREN CDR returnlist CLOSE_PAREN 
                    | append
                    | lista
                    | createlist
                    | map
                    | llamada
                    | filter
    '''

    if len(p) > 2 :
        global contLists
        newList = "listAux" + str(contLists)
        contLists += 1

        objList = stackListsAux.pop()
        name = objList[0]
        type = objList[1]
        size = objList[2]

        stackListsAux.append([newList,type,size - 1])
        stackListsAuxComplete.append([newList,size - 1])

        q = Quadruple("CDR", name, "NULL", newList  )
        quadruples.add(q)

##### RETURNELEMENT #####
def p_returnelement(p):
    ''' returnelement : OPEN_PAREN returnelement_2 returnlist CLOSE_PAREN
                     | TRUE
                     | FALSE 
    '''
    
    if p[2] == 'car':
        currentList = stackListsAux.pop()
        name = currentList[0]
        type = currentList[1]
        address = getAddress("temp",type)

        stackOperandos.append(address)
        stackTypes.append(type)

        q = Quadruple("CAR",name,"NULL",address)
        quadruples.add(q)

    elif p[2] == 'length':
        currentList = stackListsAux.pop()
        name = currentList[0]

        type = 'int'
        address = getAddress("temp",type)

        stackOperandos.append(address)
        stackTypes.append(type)

        q = Quadruple("LENGTH",name,"NULL",address)
        quadruples.add(q)

    elif p[2] == 'tail':
        currentList = stackListsAux.pop()
        name = currentList[0]
        type = currentList[1]
        address = getAddress("temp",type)

        stackOperandos.append(address)
        stackTypes.append(type)

        q = Quadruple("TAIL",name,"NULL",address)
        quadruples.add(q)

def p_returnelement_2(p):
    ''' returnelement_2 : CAR 
                        | LENGTH
                        | NULL_PREDICATE
                        | LIST_PREDICATE
                        | EMPTY_PREDICATE 
                        | TAIL
    '''
    p[0] = p[1]
    

##### CREATELIST #####
def p_createlist(p):
    ''' createlist : OPEN_PAREN LIST np_fondo_falso_createlist createlist_2 CLOSE_PAREN '''
    
    global contLists
    newList = "listAux" + str(contLists)
    contLists += 1

    typeList = stackTypes[-1]
    listLen = 0

    currentListType = stackTypes.pop()

    stackOperandosAux = []

    while currentListType != "*":
        stackOperandosAux.append(stackOperandos.pop())
        
        listLen += 1

        if currentListType != typeList :
            print("Type mismatch in list definition")

        currentListType = stackTypes.pop()

    for _ in range(0, listLen):
        q = Quadruple("NDM",stackOperandosAux.pop(), "NULL", newList )
        quadruples.add(q)

    stackListsAux.append([newList,typeList, listLen])
    stackListsAuxComplete.append([newList, listLen])

def p_np_fondo_falso_createlist(p):
    ''' np_fondo_falso_createlist : '''
    stackTypes.append("*")

def p_createlist_2(p):
    ''' createlist_2 : expresion createlist_2 
                     | empty
    '''

##### BLOQUE #####

def p_bloque(p):
    ''' bloque : imprimir 
                | expresion
                | condicion 
                | lambda
                | listfunctions 
                | llamada 
                | imprimirlista
    '''
    

##### MAIN #####
def p_main(p):
    ''' main        : OPEN_PAREN MAIN main_2 CLOSE_PAREN
                    | empty '''

def p_main_2(p):
    ''' main_2      : bloque main_2 
                    | empty '''

##### CONDICION #####

def p_condicion(p):
    ''' condicion : OPEN_PAREN IF expresion np_add_gotoF bloque rellenar_gotof bloque fill_goto CLOSE_PAREN '''

def p_np_add_gotoF(p):
    ''' np_add_gotoF : '''
    ##agregar gotF al quad 
    ad = stackOperandos.pop()
    stackTypes.pop()
    quadruples.addGotoF(ad)

    # If we are inside a function we add 1 to contCondiciones for return handling
    global contCondiciones
    contCondiciones += 1

def p_rellenar_gotof(p):
    ''' rellenar_gotof : '''
    quadruples.fillGotoF()
    quadruples.addGoto()

def p_fill_goto(p):
    ''' fill_goto : '''
    quadruples.fillGoto()


##### LAMBDA #####
def p_lambda(p):
    ''' lambda : OPEN_PAREN LAMBDA OPEN_PAREN lambda_2 np_add_lambda_scope CLOSE_PAREN OPEN_PAREN param np_insert_params CLOSE_PAREN bloque CLOSE_PAREN np_finish_lambda '''

def p_np_insert_params(p):
    ''' np_insert_params : '''
    global contParamLambda

    lenParams = len(stackParams)
    lenOperandos = len(stackOperandos)

    #if lenOperandos == lenParams :
    if contParamLambda - 1  == lenParams:
        
        for _ in range(0,lenParams):
            
            address = stackOperandos.pop()
            typeParam = stackTypes.pop()
            variableName = stackParams.pop() 
            objAux = {"type": typeParam, "virtualAddress":address}
            dirFunctions[stackScope[-1]]["vars"][variableName] = objAux
            #dirFunctions[stackScope[-1]]["memory"] = memoryObject
             # add += 1 to memory
        #Agregar fondo falso al entrar a lambda, para diferenciar lambdas voids y !voids
        stackOperandos.append("*")
        stackTypes.append("*")
   
    else :
        print("Error on number of params in lambda")

    contParamLambda = 0 

def p_np_add_lambda_scope(p):
    ''' np_add_lambda_scope : '''
    global contLambdas
    nameLambda = "lambda" + str(contLambdas)
    contLambdas += 1
    #memoryObject = {"params":[0,0,0,0],
     #                   "local":[0,0,0,0]}
    stackScope.append(nameLambda)
    #dirFunctions[nameLambda] = {"type":"lambda" , "vars":{}, "memory": memoryObject}
    dirFunctions[nameLambda] = {"type":"lambda" , "vars":{}}

def p_np_finish_lambda(p):
    ''' np_finish_lambda : '''
    
    name = stackScope.pop()
    global address
    #print(dirFunctions)
    #del dirFunctions[name]
    del dirFunctions[name]
    #print("stacks", stackOperadores, stackTypes)
    #Sacamos los fondos falsos
    if stackOperandos[-1] == "*":
        stackOperandos.pop()
        stackTypes.pop()
    else: 

        temp = stackOperandos.pop()
        typeTemp = stackTypes.pop()
        addressTemp = getAddress("temp",typeTemp)
        q = Quadruple("=",temp, "NULL",addressTemp )
        quadruples.add(q)
        stackOperandos.pop()
        stackTypes.pop()
        stackOperandos.append(addressTemp)
        stackTypes.append(typeTemp)
        
        while stackOperandos[-1] == '*':
            stackOperandos.pop()
            stackTypes.pop()

def p_lambda_2(p):
    ''' lambda_2    : expresion lambda_2
                    | empty ''' #falta lisfunctions
    global contParamLambda 
    contParamLambda += 1

##### APPEND #####

def p_append(p):
    ''' append : OPEN_PAREN APPEND np_fondo_falso returnlist returnlist append_2 CLOSE_PAREN '''
    global contLists
    newList = "listAux" + str(contLists)
    contLists += 1
    listType = ""
    approxSize = 0

    stackAppend = []

    currentList = stackListsAux.pop()
    listType = currentList[1]

    while currentList != "*":
        stackAppend.append(currentList)
        currentList = stackListsAux.pop()

    for _ in range(0,len(stackAppend)) :

        currentList = stackAppend.pop()
        currentListType = currentList[1]

        if listType != currentListType :
            print("Type mismatch between append list's")

        else:
            listName = currentList[0]
            approxSize += currentList[2]
            q = Quadruple('APPEND', 'NULL', listName,newList)
            quadruples.add(q)
        
    stackListsAux.append([newList, listType, approxSize])
    stackListsAuxComplete.append([newList,approxSize])

def p_append_2(p):
    ''' append_2 : returnlist append_2
                | empty 
    '''

def p_np_fondo_falso(p):
    ''' np_fondo_falso : '''
    stackListsAux.append('*')

##### MAP #####
def p_map(p):
    ''' map : OPEN_PAREN MAP OPEN_PAREN LAMBDA OPEN_PAREN returnlist map_2 np_add_lambda_scope CLOSE_PAREN OPEN_PAREN parammap CLOSE_PAREN expresion CLOSE_PAREN CLOSE_PAREN '''
    print("map")
    global contLists
    newList = "listAux" + str(contLists)
    contLists += 1

    currentList = stackListsAux.pop()
    currentListName = currentList[0]
    currentListType = currentList[1]
    currentListSize = currentList[2]
    
    addressFinalLambda = stackOperandos.pop()
    typeFinalLambda = stackTypes.pop()

    if typeFinalLambda == 'bool':
        typeFinalLambda = 'int'

    if typeFinalLambda == 'char':
        print("Error not a char being return on lambda inside map")
    else :
        nameLambda = stackScope.pop()

        del dirFunctions[nameLambda]
        
        address = p[11][0]
        addressSecondParam = p[11][1]
        addressCont = p[11][2]
        quadJump = p[11][3]
        addressElement = addressFinalLambda

        q = Quadruple('NDM',addressElement, "NULL", newList)
        quadruples.add(q)

        valueOne = 1

        if valueOne in constTable:
            addressOne = constTable[valueOne]
        else:
            addressOne = getAddress("const","int")
            constTable[valueOne] = addressOne
        
        addressContAux = getAddress("temp","int")

        q = Quadruple('+',addressCont, addressOne, addressContAux)
        quadruples.add(q)

        q = Quadruple('=', addressContAux, 'NULL', addressCont)
        quadruples.add(q)
        
        quadruples.fillGotoF()

        q = Quadruple('GOTO', 'NULL', 'NULL', quadJump)
        quadruples.add(q)

        stackListsAux.append([newList,currentListType,currentListSize])
        stackListsAuxComplete.append([newList, currentListSize])

        while typeFinalLambda != '*':
            typeFinalLambda = stackTypes.pop()
            stackOperandos.pop()

def p_parammap(p):
    ''' parammap : ID map_3'''

    currentList = stackListsAux[-1]
    currentListName = currentList[0]
    currentListType = currentList[1]
    currentListSize = currentList[2]

    secondListName = 0
    secondListType = 0
    secondListSize = 0

    print(sizeMap)

    if sizeMap == 2:
        secondListName = currentListName
        secondListSize = currentListSize
        secondListType = currentListType

        currentList = stackListsAux[-2]
        currentListName = currentList[0]
        currentListType = currentList[1]
        currentListSize = currentList[2]

    #addres length
    addressLength = getAddress("temp","int")

    #address for every element
    addressParam = getAddress("temp",currentListType)
    addressParamSecondList = 0

    #address cont Filter
    addressCont = getAddress("temp","int")

    q = Quadruple('LENGTH',currentListName, 'NULL', addressLength)
    quadruples.add(q)

    if sizeMap == 2:
        #addres length
        addressLengthSecondList = getAddress("temp","int")
        q = Quadruple('LENGTH',secondListName, 'NULL', addressLengthSecondList)
        quadruples.add(q)

        q = Quadruple('CHECKLEN',addressLength, addressLengthSecondList, 'NULL')
        quadruples.add(q)

    valueCero = 0

    if valueCero in constTable:
        addressCero = constTable[valueCero]
    else:
        addressCero = getAddress("const","int")
        constTable[valueCero] = addressCero

    q = Quadruple('=',addressCont, 'NULL', addressCero)
    quadruples.add(q)

    addressBool = getAddress("temp","bool")

    quadJump = quadruples.getCont()

    q = Quadruple('<',addressCont, addressLength, addressBool)
    quadruples.add(q)

    quadruples.addGotoF(addressBool)

    q = Quadruple('INDEX',currentListName, addressCont, addressParam)
    quadruples.add(q)

    if sizeMap == 2:
        addressParamSecondList = getAddress("temp",secondListType)
        q = Quadruple('INDEX',secondListName, addressCont, addressParamSecondList)
        quadruples.add(q)

        objAux = {"type": secondListType, "virtualAddress":addressParamSecondList}
        dirFunctions[stackScope[-1]]["vars"][p[2]] = objAux

    objAux = {"type": currentListType, "virtualAddress":addressParam}
    dirFunctions[stackScope[-1]]["vars"][p[1]] = objAux

    stackOperandos.append("*")
    stackTypes.append("*")

    p[0] = [addressParam, addressParamSecondList, addressCont, quadJump]

def p_map_2(p):
    ''' map_2 : returnlist 
                | empty '''

    global sizeMap

    if p[1] == 'empty':
        sizeMap = 1
    else :
        sizeMap = 2

def p_map_3(p):
    ''' map_3 : ID 
                | empty '''
    p[0] = p[1]

##### FILTER #####
def p_filter(p):
    ''' filter : OPEN_PAREN FILTER filter_2  CLOSE_PAREN '''

def p_filter_2(p):
    ''' filter_2 : lambda_filter
                 | EVEN_PREDICATE returnlist
                 | INT_PREDICATE returnlist
                 | FLOAT_PREDICATE returnlist '''

    if p[1] == 'evenp':
        global contLists
        newList = "listAux" + str(contLists)
        contLists += 1

        currentList = stackListsAux.pop()
        currentListName = currentList[0]
        currentListType = currentList[1]
        currentListSize = currentList[2]

        #addres length
        addressLength = getAddress("temp","int")

        #address for every element
        address = getAddress("temp",currentListType)

        #address cont Filter
        addressCont = getAddress("temp","int")

        q = Quadruple('LENGTH',currentListName, 'NULL', addressLength)
        quadruples.add(q)

        valueCero = 0

        if valueCero in constTable:
            addressCero = constTable[valueCero]
        else:
            addressCero = getAddress("const","int")
            constTable[valueCero] = addressCero

        q = Quadruple('=',addressCont, 'NULL', addressCero)
        quadruples.add(q)

        addressBool = getAddress("temp","bool")

        quadJump = quadruples.getCont()

        q = Quadruple('<',addressCont, addressLength, addressBool)
        quadruples.add(q)

        quadruples.addGotoF(addressBool)

        q = Quadruple('INDEX',currentListName, addressCont, address)
        quadruples.add(q)

        addressBool2 = getAddress("temp","bool")

        q = Quadruple('evenp',address, 'NULL', addressBool2)
        quadruples.add(q)

        q = Quadruple('NDMV',addressBool2, address, newList)
        quadruples.add(q)

        valueOne = 1

        if valueOne in constTable:
            addressOne = constTable[valueOne]
        else:
            addressOne = getAddress("const","int")
            constTable[valueOne] = addressOne
        
        addressContAux = getAddress("temp","int")

        q = Quadruple('+',addressCont, addressOne, addressContAux)
        quadruples.add(q)

        q = Quadruple('=', addressContAux, 'NULL', addressCont)
        quadruples.add(q)
        
        quadruples.fillGotoF()

        q = Quadruple('GOTO', 'NULL', 'NULL', quadJump)
        quadruples.add(q)

        stackListsAux.append([newList,currentListType,currentListSize])
        stackListsAuxComplete.append([newList, currentListSize])

def p_lambda_filter(p):
    ''' lambda_filter : OPEN_PAREN LAMBDA OPEN_PAREN returnlist np_add_lambda_scope CLOSE_PAREN OPEN_PAREN params_lambda_filter CLOSE_PAREN expresion CLOSE_PAREN '''
    global contLists
    newList = "listAux" + str(contLists)
    contLists += 1

    currentList = stackListsAux.pop()
    currentListName = currentList[0]
    currentListType = currentList[1]
    currentListSize = currentList[2]
    
    addressFinalLambda = stackOperandos.pop()
    typeFinalLambda = stackTypes.pop()

    if typeFinalLambda != 'bool':
        print("Error not a boolean being return on lambda inside filter")
    else :
        nameLambda = stackScope.pop()

        del dirFunctions[nameLambda]
        
        address = p[8][0]
        addressCont = p[8][1]
        quadJump = p[8][2]
        addressBool = addressFinalLambda

        q = Quadruple('NDMV',addressBool, address, newList)
        quadruples.add(q)

        valueOne = 1

        if valueOne in constTable:
            addressOne = constTable[valueOne]
        else:
            addressOne = getAddress("const","int")
            constTable[valueOne] = addressOne
        
        addressContAux = getAddress("temp","int")

        q = Quadruple('+',addressCont, addressOne, addressContAux)
        quadruples.add(q)

        q = Quadruple('=', addressContAux, 'NULL', addressCont)
        quadruples.add(q)
        
        quadruples.fillGotoF()

        q = Quadruple('GOTO', 'NULL', 'NULL', quadJump)
        quadruples.add(q)

        stackListsAux.append([newList,currentListType,currentListSize])
        stackListsAuxComplete.append([newList, currentListSize])

        while typeFinalLambda != '*':
            typeFinalLambda = stackTypes.pop()
            stackOperandos.pop()

def p_params_lambda_filter(p):
    ''' params_lambda_filter : ID '''

    currentList = stackListsAux[-1]
    currentListName = currentList[0]
    currentListType = currentList[1]
    currentListSize = currentList[2]

    #addres length
    addressLength = getAddress("temp","int")

    #address for every element
    addressParam = getAddress("temp",currentListType)

    #address cont Filter
    addressCont = getAddress("temp","int")

    q = Quadruple('LENGTH',currentListName, 'NULL', addressLength)
    quadruples.add(q)

    valueCero = 0

    if valueCero in constTable:
        addressCero = constTable[valueCero]
    else:
        addressCero = getAddress("const","int")
        constTable[valueCero] = addressCero

    q = Quadruple('=',addressCont, 'NULL', addressCero)
    quadruples.add(q)

    addressBool = getAddress("temp","bool")

    quadJump = quadruples.getCont()

    q = Quadruple('<',addressCont, addressLength, addressBool)
    quadruples.add(q)

    quadruples.addGotoF(addressBool)

    q = Quadruple('INDEX',currentListName, addressCont, addressParam)
    quadruples.add(q)


    objAux = {"type": currentListType, "virtualAddress":addressParam}
    dirFunctions[stackScope[-1]]["vars"][p[1]] = objAux

    stackOperandos.append("*")
    stackTypes.append("*")

    p[0] = [addressParam, addressCont, quadJump]

###### TIPO #####
def p_tipo(p):
    ''' tipo : INT
            | FLOAT
            | CHAR
            | VOID
            | LIST
    '''
    stackTypes.append(p[1])

###### TIPOVARS #####
def p_tipovars(p):
    ''' tipovars : INT
            | FLOAT
            | CHAR
            | LIST
    '''
    #print(p[1])
    stackTypes.append(p[1])

##### LLAMADA #####
def p_llamada(p):
    ''' llamada : OPEN_PAREN ID np_check_func_exits llamada_2 np_check_params CLOSE_PAREN np_enter_to_stack'''

def p_np_enter_to_stack(p):
    ''' np_enter_to_stack : '''
    funcName = p[-5]
    objectVars = dirFunctions[scopeGlobal]["vars"]
    if funcName in objectVars:
        type = objectVars[funcName]["type"]
        virtualAddress = objectVars[funcName]["virtualAddress"]

        addressTemp = getAddress("temp",type)
        stackOperandos.append(addressTemp)
        stackTypes.append(type)

        q = Quadruple("=",virtualAddress, "NULL",addressTemp )
        quadruples.add(q)


def p_np_check_func_exits(p):
    ''' np_check_func_exits : '''
    funcName = p[-1]
    
    if funcName in dirFunctions:
        q = Quadruple("ERA","NULL","NULL", funcName ) 
        quadruples.add(q)
    else :
        print('Error function {} is not declare'.format(funcName))

def p_llamada_2(p):
    ''' llamada_2 : expresion np_append_params llamada_2
                  | listfunctions llamada_2 
                  | empty ''' #faltan el 2 y 3

def p_np_append_params(p):
    ''' np_append_params : '''
    address = stackOperandos.pop()
    type = stackTypes.pop()
    queueParams.append([address,type])

def p_np_check_params(p):
    ''' np_check_params : '''
    
    #function variables
    funcName = p[-3]

    funcObj = dirFunctions[funcName]
    funcQuad = funcObj["quad"]
    funcParams = funcObj["typeParams"].copy()
    lenParamsFunction = len(funcParams) 

    global queueParams
    lenParamstoCheck = len(queueParams) 
    
    # check if the definition of the function and the params match
    if lenParamsFunction != lenParamstoCheck :
        queueParams = []
        print("Number of arguments doesn't match the definition of the funcion")
    else:
        for i in range(0, lenParamsFunction ):
            currentParamObject = queueParams.pop(0)
            address = currentParamObject[0]
            type = currentParamObject[1]
            typeFunc = funcParams.pop()
            
            # if the variable on the call and on the definition are the same then we can continue, if not error
            if type == typeFunc: 
                q = Quadruple("param",address,"NULL", "param" + str(i + 1) ) 
                quadruples.add(q)
            else:
                print("Error type mismatch on params of functions")
    
    q = Quadruple("GOSUB","NULL","NULL", funcQuad )
    quadruples.add(q)
    

def p_error(p):
    print(f"Syntax error at {p.value!r}")

def p_empty(p):
    'empty :'
    pass
    p[0] = 'empty'

def createOvejota():
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        f= open("tomate/tests/ovj1.txt","w+")
        #f= open("tests/ovj1.txt","w+")
        
        ## escribir const Table
        f.write("$$\n")
        for i in constTable:
            
            f.write("{} {}\n".format(i,constTable[i]))
        f.write("$$\n")

        ## escribir quads
    
        for i in range(0,quadruples.cont):
            opvm, leftvm, rightvm, tempvm = quadruples.getQuad(i)
            f.write("{} {} {} {}\n". format(opvm,
                                            leftvm,
                                            rightvm,
                                            tempvm))
        f.write("$$\n")
       
       
        ## escribir dir table
        dirFKeys = list(dirFunctions)
        f.write("@@\n")
        f.write("name {}\n".format(dirFKeys[0]))
        funGlobal = dirFunctions[dirFKeys[0]]["vars"]
        funGlobalVars = list(funGlobal)  
        
        f.write("vars ")
        for k, v in funGlobal.items():
            values = v.values()
            
            if next(iter(v.keys())) != "list":

                value_iterator = iter(values)
                first_value = next(value_iterator)
                second_value = next(value_iterator)
                f.write("{} {} {} ".format(k,first_value,second_value))
        f.write("\n")
        f.write("@@\n")
        
        
        for i in range(1,len(dirFKeys)):
            fun = dirFunctions[dirFKeys[i]]
            f.write("name {}\n".format(dirFKeys[i]))
            for k,j in fun.items():
                
                if k == "memory":
                    f.write("{} ". format(k))
                    values = j.values()
                    value_iterator = iter(values)
                    first_value = next(value_iterator)
                    second_value = next(value_iterator)
                    for y in range (0,len(first_value)):
                        f.write("{} ".format(first_value[y]))
                    for z in range (0,len(second_value)):
                        f.write("{} ".format(second_value[z]))
                    #print(first_value,second_value)
                    f.write("\n")

                elif k == "typeParams":
                    f.write("{} ".format(k))
                    for x in range (0,len(j)):
                        f.write("{} ".format(j[x]))
                    f.write("\n")
                else:
                    f.write("{} {}\n".format(k,j))
            f.write("@@\n")
       
        #Para global sizes

        f.write("$$\n")
        for i in globalMemory:
            for j in i:
                f.write("{} ".format(j))
            f.write("\n")
        f.write("$$\n")

        #Para global bases 
        addrBKeys= list(addressBases)

        for i in addrBKeys:
            addrScope = addressBases[i]
            addrScopeK = list(addrScope)
            for j in addrScopeK:
                f.write("{} ".format(addrScope[j]))
            f.write("\n")
        f.write("$$\n")

        # Save stack list
        stringLists = ''
        maxLengthDM = 0
        for i in stackListsAuxComplete:
            #print(i[0])
            maxLengthDM += i[1]
            stringLists += i[0]
            stringLists += ' '

        f.write(str(maxLengthDM) + " ")
        f.write(stringLists)
        f.write("\n")

        #f.close() 

import ply.yacc as yacc
yacc.yacc()
    

#'''
# para testear con un file
import os
fileDir = os.path.dirname(os.path.realpath('__file__'))
programa = 'test3.txt'
filename = os.path.join(fileDir, 'tomate/tests/' + programa )
#filename = os.path.join(fileDir, 'tests/' + programa )
f = open(filename, "r")
input = f.read()
yacc.parse(input)

#print(stackOperadores)
print("stackListComplete: " + str(stackListsAuxComplete))
print("stackListAux: " + str(stackListsAux))
print("stackOperandos: " + str(stackOperandos))
print("stackTypes: " + str(stackTypes))
print("stackScope: " + str(stackScope))
print("Const Table: " + str(constTable))
print("Address: " + str(address))
print("DirFunctions: "+ str(dirFunctions))

#'''
quadruples.print()
globalVariables()
print(globalMemory)
createOvejota()

## VM
vm = VirtualMachine()
vm.loadOvejota()

#vm.printQuadruples()
#vm.printFunctions()
#vm.printConstTable()


vm.pointerSomething()
#vm.celia.printMemory()

#vm.createOvejota()

''' # para testear a mano
while True:
    try:
        s = input('programa > ')
    except EOFError:
        break
    yacc.parse(s)
'''

# add resultado de funcion to stack de types y operandos
# check variables dentro de funcion en global y funcion local 
# contadores raros de cuantos de cada tipo √√
# cambiar referencias a nuevo objeto √√


# las variables temporales que se creen dentro de una funcion se van a tratar como variables locales
    # voy a meter ese cambio de una √√
# los temporales dentro de una funcion tenemos que hacer que se guarden en la memorial local en lugar de la memoria temporal √√

# constantes no tratarlos como temp √√

# goto inicial despues de vars inicial √√

# faltan los negativos CAGAJOOOO

# return de functions esto no marca error √√

# returns de funciones, agregar logica :√√
# dentro de cada funcion vamos a contabilizar cuantos condiciones existieron
# if no void then 
#       len(stackOperandos) == 1 + contCondiciones
# si es diferente hay error
# 
# also
# resetear temporales al llegar al termino de una funcion √√
#
# lambda adentro de otro lambda

# tenemos generar el ovej
# leer el ovejota
    # add bases
    # add sizes
# agregar logica para cuando estemos en funcion
# agregar los demas operadores al switch
    # gotoF
    # era 
    # param
    # gosub

'''(define ( ( int f1 ) int i1 int i2)  
            ( if (< i1 1)
                (+ i1 i2)
                (print i2)    
            )
        )
'''
'''
$$
1000 2000 3000 
4000 5000 6000 7000
8000 9000 10000 12000
13000 14000 15000
$$
2 1 1
1 0 0 0
0 0 0 0
1 1 1 
'''
'''
from DynamicMemoryManager import *

mike = DynamicMemoryManager(['l1','l2','l3','l4','l5','l6','l7','l8','l9','l10'],20)

mike.setValue('l1',4) #0
mike.setValue('l1',2) #0
mike.setValue('l1',5) #0
mike.setValue('l1',10)
mike.setValue('l2',50)
mike.setValue('l2',4)
mike.print('l1')
print(mike.car('l1'))
mike.cdr('l3','l1')
print(mike.car('l3'))
mike.cdr('l4','l3')
print(mike.car('l4'))
mike.cdr('l5','l4')
print(mike.length('l1'))
print(mike.length('l2'))
print(mike.length('l3'))
print(mike.length('l4'))
print(mike.length('l5'))
mike.append('l1','l6')
#mike.append('l2','l6')
#mike.append('l3','l6')
#mike.dm.printMemory()
mike.print('l6')
print(mike.length('l6'))
mike.filter('even','l1','l7')
mike.setValue('l8',1.2)
mike.setValue('l8',2.3)
mike.setValue('l9','a')
mike.print('l9')
mike.cdr('l10','l9')
print(mike.tail('l2'))
print(mike.indexList(0,'l10'))
#mike.dm.printMemory()
'''
## Cuando tengamos un error para todo alv

# head 
# tail

'''
NDM 13000 NULL ListaAux1
13000 = 10
NDM 13001 NULL ListaAux1
2 
NDM 13002 NULL ListaAux1
30
NDM 13003 NULL ListaAux2
3
NDM 13004 NULL ListaAux2
4
NDM 13005 NULL ListaAux2

filter even ListaAux1 ListaAux3
cdr ListaAux1 ListaAux4

l1, l2, l3

stackLists
ListaAux1 , 0
ListaAux2 , 3
ListaAux3 , NULL

[[10,1],[2,2],[30,0],[3,4],[4,0],[0,0],[0,0],[0,0],[0,0]]

(append l1 l2 l3)

append l1 x l4
append l2 x l4
append l3 x l4
'''