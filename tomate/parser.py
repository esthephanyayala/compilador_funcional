from lexer import tokens
from Quadruples import *
from CuboSemantico import semanticCube

queueParams = []

quadruples = Quadruples()

ultTipo = []
varTable = {}
dirFunctions = {}
scopeMemory = "factorial"
nextScopeMemory = ""

stackOperadores = []
stackOperandos = []
stackTypes = []

stackScope = []


stackSaltos = []

scopeMemory = 0


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
                        "bool": 11000
                        }
        }
    
##### PROGRAMA #####

def p_programa(p):
    ''' programa : np_first_quad OPEN_PAREN PROGRAM ID np_dirProgram programa_2 programa_3 np_fill_goto_main main CLOSE_PAREN'''
    
def p_np_first_quad(p):
    ''' np_first_quad : '''
    quadruples.addGoto()

def p_np_fill_goto_main(p):
    ''' np_fill_goto_main : '''
    quadruples.fillGoto()

def p_np_dirProgram(p):
    ''' np_dirProgram : '''
    dirFunctions[p[-1]] = {"vars": {}}
    global scopeMemory
    scopeMemory = p[-1]
    stackScope.append(p[-1])
    

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
            scope = "temp"
            ad = address[scope][semanticCubeType]
            address[scope][semanticCubeType] += 1

            stackOperandos.append(ad)
            stackTypes.append(semanticCubeType)

            q = Quadruple(operator,left,right,ad)
            
            quadruples.add(q)

            ##agregar gotF al quad 
            quadruples.addGotoF(ad)

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
        scope = "temp"
        ad = address[scope][semanticCubeType]
        address[scope][semanticCubeType] += 1
        stackOperandos.append(ad)
        stackTypes.append(semanticCubeType)

        q = Quadruple(operator,left,"NULL",ad)
        quadruples.add(q)
    
    else: ## para 2do y 3er caso
        semanticCubeType = 'bool'
        scope = "temp"
        ad = address[scope][semanticCubeType]
        address[scope][semanticCubeType] += 1
        stackOperandos.append(ad)
        stackTypes.append(semanticCubeType)

        

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
            | returnelement'''

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
            scope = "temp"
            ad = address[scope][semanticCubeType]
            address[scope][semanticCubeType] += 1

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
    #print(p[1])

def p_np_stackCTEID(p):
    '''np_stackCTEID : '''
    value = p[-1]
    #print(value)
    dirFKeys = list(dirFunctions)

    #valueObject = varTable["vars"][value]
    valueObject = dirFunctions[dirFKeys[0]]["vars"][value] 

  
    address = valueObject['virtualAddress']
    type = valueObject['type']

    stackOperandos.append(address)
    stackTypes.append(type)
    
  
def p_np_stackCTEI(p):
    '''np_stackCTEI : '''

    type = "int"
    scope = "temp"

    ad = address[scope][type]
    address[scope][type] += 1

    stackOperandos.append(ad)
    stackTypes.append(type)
    
def p_np_stackCTEF(p):
    '''np_stackCTEF : '''
    
    type = "float"
    scope = "temp"

    ad = address[scope][type]
    address[scope][type] += 1

    stackOperandos.append(ad)
    stackTypes.append(type)

def p_np_stackCTEC(p):
    '''np_stackCTEC : '''
    
    type = "char"
    scope = "temp"

    ad = address[scope][type]
    address[scope][type] += 1

    stackOperandos.append(ad)
    stackTypes.append(type)

##### DECLARACIONFUNCION #####

def p_declaracionfuncion(p):
    ''' declaracionfuncion : OPEN_PAREN FUNCTIONS np_create_funcObject declaracionfuncion_2 CLOSE_PAREN '''

def p_np_create_funcObject(p):
    ''' np_create_funcObject : '''
    funct = p[-1] # es la palabra "functions"
    #varTable[funct] = {} #creo que ya no lo necesitamos
  

def p_declaracionfuncion_2(p):
    ''' declaracionfuncion_2    : funcion declaracionfuncion_2 
                                | empty'''

##### FUNCION #####

def p_funcion(p):
    ''' funcion : OPEN_PAREN DEFINE OPEN_PAREN OPEN_PAREN tipo ID np_create_dirFunc CLOSE_PAREN typeparam np_varTabFunc CLOSE_PAREN bloque CLOSE_PAREN np_finish_function '''

def p_np_finish_function(p):
    ''' np_finish_function : '''
    q = Quadruple("ENDFUNC","NULL","NULL", "NULL")
    quadruples.add(q)

def p_np_create_dirFunc(p):
    ''' np_create_dirFunc : '''   
    funcName = p[-1]
    dirFKeys = list(dirFunctions)
    currentQuad = quadruples.getCurrentQuad()
    global scopeMemory

    #if funcName in varTable['functions']:
    # print("function {} already declare".format(funcName) ) # Aqui marcaremos el error de funcion ya definida
    #else:
        
    #para dirFunction
    if funcName in dirFunctions:
        print("function {} already declare".format(funcName))
    else:      
        typeFunc = stackTypes.pop()
        #varTable['functions'][funcName] = {"type":typeFunc, "quad" : 0 } #varTable
        dirFunctions[funcName] = {"type":typeFunc, "quad": currentQuad } #dirFunction
        scopeMemory = funcName
        

    # if function is not void then push to var table
    if typeFunc != 'void':
        scope = "global"
        ad = address[scope][typeFunc]
        address[scope][typeFunc] += 1
        #varTable['vars'][funcName] = {"type": typeFunc , "virtualAddress":ad}
        dirFunctions[dirFKeys[0]]['vars'][funcName] = {"type": typeFunc , "virtualAddress":ad}
    


def p_np_varTabFunc(p):
    ''' np_varTabFunc : '''
    funcName = p[-4]
    varTableFunc = {}
    varTableFunc[funcName] = {}
    typesParam = []
    
    for i in range(0,len(stackOperandos)):
        typeParam = stackTypes.pop()
        idparam = stackOperandos.pop()
        scope = "local"
        ad = address[scope][typeParam]
        address[scope][typeParam] += 1
        #varTableFunc[funcName][idparam] = {"type": typeParam, "virtualAdress":ad }
        typesParam.append(typeParam)
        #varTable['functions'][funcName][idparam] = {"typeParam": typeParam, "virtualAdressParam":ad }
        paramsCar = {"type": typeParam, "virtualAddress":ad }
        dirFunctions[funcName]['vars'] = { idparam: paramsCar }
        #print (varTableFunc)
    dictTypes = {"typeParams": typesParam}
    #varTable['functions'][funcName].update(dictTypes)
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
    ''' param   : ID param
                | empty '''

##### DECLARACIONVARIABLES #####

def p_declaracionvariables(p):
    ''' declaracionvariables : OPEN_PAREN VARS np_create_dirFuncVars declaracionvariables_2 CLOSE_PAREN '''

def p_np_create_dirFuncVars(p):
    ''' np_create_dirFuncVars : '''
    funcName = p[-1]
    varTable[funcName] = {}


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
    

    #print(varId)
  # if varId in varTable['vars']:
   #     print("variable {} already declare".format(varId)) #Aqui vamos a marcar el error de variable ya declarada
    #else :
    #if varId in dirFunctions
    #print("df vars:",dirFunctions)
    if varId in dirFunctions[dirFKeys[0]]['vars']:
        print("variable {} already declare".format(varId))
    else:
        type = ultTipo[-1]
        scope = "global"
        ad = address[scope][type]
        address[scope][type] += 1
        #varTable['vars'][varId] = {"type": ultTipo[-1] , "virtualAddress":ad}
        
        dirFunctions[dirFKeys[0]]['vars'][varId] = {"type": ultTipo[-1] , "virtualAddress":ad}

           


def p_declare_2(p):
    ''' declare_2   : definircte
                    | definirlista'''
    
##### DEFINIRCTE #####

def p_definircte(p):
    ''' definircte  : CTEI np_definicioni
                    | CTEF np_definicionf
                    | CTEC np_definicionc '''
  
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
    ''' condicion : OPEN_PAREN IF expresion bloque rellenar_gotof bloque fill_goto CLOSE_PAREN '''

def p_rellenar_gotof(p):
    ''' rellenar_gotof : '''
    quadruples.fillGotoF()
    quadruples.addGoto()

def p_fill_goto(p):
    ''' fill_goto : '''
    quadruples.fillGoto()


##### LAMBDA #####
def p_lambda(p):
    ''' lambda : OPEN_PAREN OPEN_PAREN LAMBDA OPEN_PAREN param CLOSE_PAREN bloque CLOSE_PAREN lambda_2 CLOSE_PAREN '''

def p_lambda_2(p):
    ''' lambda_2    : expresion
                    | empty '''

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
    ''' llamada : OPEN_PAREN ID np_check_func_exits llamada_2 np_check_params CLOSE_PAREN np_finish_llamada '''

def p_np_finish_llamada(p):
    ''' np_finish_llamada : '''
    stackScope.pop()
    #change scope

def p_np_check_func_exits(p):
    ''' np_check_func_exits : '''
    funcName = p[-1]
    stackScope.append(funcName)
    
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
    funcName = stackScope[-1]
    print(funcName)

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
#print(varTable)
print(dirFunctions)
print("scope", scopeMemory)
#print("direccionesGlobales " + str(direcciones["direccionesGlobales"]))
#print(direcciones)
#'''
quadruples.print()
#print(stackSaltos)
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