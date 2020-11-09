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
globalMemory = []

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
        '''
        localMemory = dirFunctions[currentScope]["memory"]["local"]

        # add += 1 to local memory
        if type == "int":
            localMemory[0] += 1
        elif type == "float":
            localMemory[1] += 1
        elif type == "char":
            localMemory[2] += 1
        else :
            localMemory[3] += 1
        '''

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

    if varId in dirFunctions[dirFKeys[0]]['vars']:
        print("variable {} already declare".format(varId))
    else:
        type = ultTipo[-1]

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
        
        dirFunctions[dirFKeys[0]]['vars'][varId] = {"type": ultTipo[-1] , "virtualAddress":addressDirFunction}

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
def p_lista(p):
    ''' lista : ID
              | QUOTE OPEN_PAREN lista_2 CLOSE_PAREN
    '''

def p_lista_2(p):
    ''' lista_2 : CTEI lista_2
                | CTEF lista_2
                | CTEC lista_2
                | empty
    '''


##### LISTFUNCTIONS #####
def p_listfunctions(p):
    ''' listfunctions : returnelement
                      | returnlist
    '''

##### RETURNLIST #####
def p_returnlist(p):
    ''' returnlist : OPEN_PAREN returnlist_2 lista CLOSE_PAREN 
                    | append
                    | lista
                    | createlist
                    | map
                    | llamada
                    | filter
    '''

def p_returnlist_2(p):
    ''' returnlist_2 : CDR '''

##### RETURNELEMENT #####
def p_returnelement(p):
    ''' returnelement : OPEN_PAREN returnelement_2 returnlist CLOSE_PAREN
                     | TRUE
                     | FALSE 
    '''

def p_returnelement_2(p):
    ''' returnelement_2 : CAR
                        | LENGTH
                        | NULL_PREDICATE
                        | LIST_PREDICATE
                        | EMPTY_PREDICATE 
    '''

##### CREATELIST #####
def p_createlist(p):
    ''' createlist : OPEN_PAREN LIST createlist_2 CLOSE_PAREN '''

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
    ''' lambda : OPEN_PAREN  LAMBDA OPEN_PAREN lambda_2 np_add_lambda_scope CLOSE_PAREN OPEN_PAREN param np_insert_params CLOSE_PAREN bloque CLOSE_PAREN np_finish_lambda '''

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
            '''
            paramsMemory = dirFunctions[stackScope[-1]]["memory"]["params"]
            if typeParam == "int":
                paramsMemory[0] += 1
            elif typeParam == "float":
                paramsMemory[1] += 1
            elif typeParam == "char":
                paramsMemory[2] += 1
            else :
                paramsMemory[3] += 1
            '''
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
        '''
        paramsLambda = dirFunctions[name]["memory"]["params"]
        localLambda = dirFunctions[name]["memory"]["local"]
        totalInt = paramsLambda[0] + localLambda[0]
        totalFl = paramsLambda[1] + localLambda[1]
        totalCh = paramsLambda[2] + localLambda[2]
        totalBo = paramsLambda[3] + localLambda[3]

        if boolScopeGlobal(): 
            #estamos en global
            address["temp"]["int"] -= totalInt
            address["temp"]["float"] -= totalFl 
            address["temp"]["char"] -= totalCh
            address["temp"]["bool"] -= totalBo
        else:
            address["local"]["int"] -= totalInt
            address["local"]["float"] -= totalFl 
            address["local"]["char"] -= totalCh
            address["local"]["bool"] -= totalBo
        '''
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
    #print("lambda2")
    global contParamLambda 
    contParamLambda += 1

##### APPEND #####

def p_append(p):
    ''' append : OPEN_PAREN APPEND returnlist returnlist append_2 CLOSE_PAREN '''

def p_append_2(p):
    ''' append_2 : returnlist append_2
                | empty 
    '''

##### MAP #####
def p_map(p):
    ''' map : OPEN_PAREN MAP map_3 returnlist map_2 CLOSE_PAREN '''

def p_map_2(p):
    ''' map_2 : returnlist map_2
              | empty 
    '''
def p_map_3(p):
    ''' map_3 : OPEN_PAREN LAMBDA OPEN_PAREN param CLOSE_PAREN bloque CLOSE_PAREN '''


##### FILTER #####
def p_filter(p):
    ''' filter : OPEN_PAREN FILTER filter_2 returnlist CLOSE_PAREN '''

def p_filter_2(p):
    ''' filter_2 : OPEN_PAREN LAMBDA OPEN_PAREN param CLOSE_PAREN bloque CLOSE_PAREN
                 | EVEN_PREDICATE
                 | INT_PREDICATE
                 | FLOAT_PREDICATE '''

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
        #stackOperandos.append(virtualAddress)
        #stackTypes.append(type)
    
        #print("so", stackOperandos)
        #valueTemp = stackOperandos.pop()
        #typeTemp = stackTypes.pop() 
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
        
    
        print("$%$%·")
        f.write("vars ")
        for k, v in funGlobal.items():
            values = v.values()
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
                    f.write("{} ". format(k))
                    for x in range (0,len(j)):
                        f.write("{} ".format(j[x]))
                    f.write("\n")
                else:
                    f.write("{} {}\n".format(k,j))
            f.write("@@\n")
       
       
   

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
vm.initializeAddressManager()


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