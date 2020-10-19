from lexer import tokens
from Quadruples import Quadruple
from CuboSemantico import semanticCube

ultTipo = []
varTable = {}

stackIds = []
stackCTE = []

direcciones = {
        "direccionesGlobales" : {"int": [] , "float" : [] , "char" : [] } ,
        "direccionesTemp" : {"int": [] , "float" : [] , "char" : [] , "bool" : [] }   
    }

#direcciones = {"int": [] , "float" : [] , "char" : [] }
counterDirecciones = []
    
##### PROGRAMA #####

def p_programa(p):
    ''' programa : OPEN_PAREN PROGRAM ID programa_2 programa_3 main CLOSE_PAREN'''


def p_programa_2(p):
    ''' programa_2  : declaracionvariables
                    | empty '''

def p_programa_3(p):
    ''' programa_3  : declaracionfuncion
                    | empty '''

##### IMPRIMIR #####

def p_imprimir(p):
    ''' imprimir : OPEN_PAREN PRINT imprimir_2 CLOSE_PAREN '''

def p_imprimir_2(p):
    ''' imprimir_2  : CTEC 
                    | expresion
                    | lambda
                    | listfunctions
    ''' 

##### EXPRESION #####

def p_expresion(p):
    ''' expresion   : exp 
                    | OPEN_PAREN signosrelacionales exp exp CLOSE_PAREN 
                    | expresionesunarias'''


##### SIGNOSRELACIONALES #####

def p_signosrelacionales(p):
    ''' signosrelacionales  : LT 
                            | GT
                            | NE
                            | EQUAL '''

##### EXPRESIONESUNARIAS #####

def p_expresionesunarias(p):
    ''' expresionesunarias  : OPEN_PAREN expresionesunarias_2 exp CLOSE_PAREN 
                            | TRUE
                            | FALSE '''

def p_expresionesunarias_2(p):
    ''' expresionesunarias_2    : EVEN_PREDICATE 
                                | INT_PREDICATE
                                | FLOAT_PREDICATE
                                | LIST_PREDICATE
                                | NULL_PREDICATE
                                | EMPTY_PREDICATE '''

##### EXP #####

def p_exp(p):
    ''' exp : OPEN_PAREN PLUS exp exp CLOSE_PAREN
            | OPEN_PAREN MINUS exp exp CLOSE_PAREN 
            | OPEN_PAREN TIMES exp exp CLOSE_PAREN 
            | OPEN_PAREN DIVIDE exp exp CLOSE_PAREN 
            | OPEN_PAREN PLUS varcte CLOSE_PAREN 
            | OPEN_PAREN MINUS varcte CLOSE_PAREN 
            | varcte 
            | llamada
            | returnelement'''
    try:
        operator = p[2]

        # right 
        rightStackCTE = stackCTE.pop()
        
        if  not(rightStackCTE['isCTE']) :
            rightID = rightStackCTE['value']
            rightObject = varTable['vars'][rightID]
            rightType = rightObject['type']
            rightDir = rightObject['pointer']
            rightDirObject = 'direccionesGlobales'
        else :
            rightValue = rightStackCTE['value']
            rightType = rightStackCTE['type']
            rightDir = rightValue
            rightDirObject = "NULL"

        # left
        leftStackCTE = stackCTE.pop()

        if not(leftStackCTE['isCTE']) :
            leftID = leftStackCTE['value']
            leftObject = varTable['vars'][leftID]
            leftType = leftObject['type']
            leftDir = leftObject['pointer']
            leftDirObject = 'direccionesGlobales'
        else :
            leftValue = leftStackCTE['value']
            leftType = leftStackCTE['type']
            leftDir = leftValue
            leftDirObject = "NULL"

        #
        temp = 1
        q = Quadruple(operator,leftDir,rightDir,temp,leftDirObject,rightDirObject,'global',leftType,rightType,'int')
        q.print()
    except:
        print('nel')
    

##### SIGNOS 1 #####

def p_signos1(p):
    '''signos1 : PLUS 
                | MINUS ''' 
    
    print(p[1])

##### SIGNOS 2 #####

def p_signos2(p):
    '''signos2 : TIMES 
                | DIVIDE '''

##### VARCTE #####

def p_varcte(p):
    ''' varcte : ID np_stackCTEID
                | CTEI np_stackCTEI
                | CTEF np_stackCTEF '''
    #print(p[1])
    stackIds.append(p[1])

def p_np_stackCTEID(p):
    '''np_stackCTEID : '''
    value = p[-1]
    object = {
        "isCTE" : False,
        "value" : value
    }
    stackCTE.append( object )
    print(stackCTE)
  
def p_np_stackCTEI(p):
    '''np_stackCTEI : '''
    value = p[-1]
    object = {
        "isCTE" : True,
        "value" : int(value),
        "type" : "int"
    }
    stackCTE.append( object )
    print(stackCTE)
    
def p_np_stackCTEF(p):
    '''np_stackCTEF : '''
    value = p[-1]
    object = {
        "isCTE" : True,
        "value" : float(value),
        "type" : "float"
    }
    stackCTE.append( object )
    print(stackCTE)

##### DECLARACIONFUNCION #####

def p_declaracionfuncion(p):
    ''' declaracionfuncion : OPEN_PAREN FUNCTIONS np_create_funcObject declaracionfuncion_2 CLOSE_PAREN '''

def p_np_create_funcObject(p):
    ''' np_create_funcObject : '''
    funct = p[-1]
    varTable[funct] = {}

def p_declaracionfuncion_2(p):
    ''' declaracionfuncion_2    : funcion declaracionfuncion_2 
                                | empty'''

##### FUNCION #####

def p_funcion(p):
    ''' funcion : OPEN_PAREN DEFINE OPEN_PAREN ID np_create_dirFunc param CLOSE_PAREN bloque CLOSE_PAREN '''

def p_np_create_dirFunc(p):
    ''' np_create_dirFunc : '''   
    funcName = p[-1]

    if funcName in varTable['functions']:
        print("function {} already declare".format(funcName) ) # Aqui marcaremos el error de funcion ya definida
    else:
        varTable['functions'][funcName] = "tipo"


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
    #print(varId)
    if varId in varTable['vars']:
        print("variable {} already declare".format(varId)) #Aqui vamos a marcar el error de variable ya declarada
    else :
        varTable['vars'][varId] = {"type": ultTipo[-1] , "pointer":counterDirecciones[-1]}

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
    #print(p[-1])
    direcciones["direccionesGlobales"]["int"].append(p[-1])
    counterDirecciones.append(len(direcciones["direccionesGlobales"]["int"]) - 1)
    #print(direcciones)
    #print(counterDirecciones)

def p_np_definicionf(p):
    ''' np_definicionf : '''
    ultTipo.append("float")
    #print(p[-1])
    direcciones["direccionesGlobales"]["float"].append(p[-1])
    counterDirecciones.append(len(direcciones["direccionesGlobales"]["float"]) - 1)
    #print(direcciones)
    #print(counterDirecciones)

def p_np_definicionc(p):
    ''' np_definicionc : '''
    ultTipo.append("char")
    direcciones["direccionesGlobales"]["char"].append(p[-1])
    counterDirecciones.append(len(direcciones["direccionesGlobales"]["char"]) - 1)

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
    ''' condicion : OPEN_PAREN IF expresion bloque bloque CLOSE_PAREN '''

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
    '''

##### LLAMADA #####
def p_llamada(p):
    ''' llamada : OPEN_PAREN ID llamada_2 CLOSE_PAREN '''

def p_llamada_2(p):
    ''' llamada_2 : expresion llamada_2
                  | listfunctions llamada_2
                  | empty '''


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
programa = 'test4.txt'
filename = os.path.join(fileDir, 'tomate/tests/' + programa )
#filename = os.path.join(fileDir, 'tests/' + programa )
f = open(filename, "r")
input = f.read()
yacc.parse(input)

print(varTable)
print("direccionesGlobales " + str(direcciones["direccionesGlobales"]))
#'''

''' # para testear a mano
while True:
    try:
        s = input('programa > ')
    except EOFError:
        break
    yacc.parse(s)
'''