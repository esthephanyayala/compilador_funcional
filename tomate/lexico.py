
reserved = {
    'print' : 'PRINT',
    'declare' : 'DECLARE',
    #'id' : 'ID', -- lo tenemos como palabra reservada pero no creo que sea el caso
    'if' : 'IF',
    'define' : 'DEFINE',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'lambda' : 'LAMBDA',# mismo caso que id con cte_XXX
    'program' : 'PROGRAM',
    'vars' : 'VARS',
    'functions' : 'FUNCTIONS',
    'main' : 'MAIN', #igual con epsilon
    'cdr' : 'CDR',
    'car' : 'CAR',
    'length' : 'LENGTH',
    'nullp' : 'NULL_PREDICATE',
    'listp' : 'LIST_PREDICATE',
    'emptyp' : 'EMPTY_PREDICATE',
    'append' : 'APPEND',
    'list' : 'LIST',
    'map' : 'MAP',
    'filter' : 'FILTER',
    'tt' : 'FALSE',
    'ff' : 'TRUE',
    'evenp' : 'EVEN_PREDICATE',
    'intp' : 'INT_PREDICATE',
    'floatp' : 'FLOAT_PREDICATE'
}

tokens = [
    'ID',
    'CTEI',
    'CTEF',
    'CTEC',
    'OPEN_PAREN','CLOSE_PAREN',
    'PLUS','MINUS','TIMES','DIVIDE',
    'LT','GT','NE','EQUAL',
    'QUOTE'
] + list(reserved.values())

digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
t_CTEI = r'(' + digit + r'+)'
t_CTEF = r'(' + digit + r'+(\.' + digit +  r')+)'
t_CTEC = r'\'(' + nondigit + r')\''
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LT = r'<'
t_GT = r'>'
t_NE = r'!='
t_EQUAL = r'='
t_QUOTE = r'\''

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')    # Check for reserved words
     return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

    
##### PROGRAMA #####

def p_programa(p):
    ''' programa : OPEN_PAREN PROGRAM programa_2 programa_3 main CLOSE_PAREN'''
    print("programa 0" , p[0])
    print("programa 1" ,p[1])
    print("programa 2" ,p[2])

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
    ''' exp : OPEN_PAREN signos1 exp exp CLOSE_PAREN
            | OPEN_PAREN signos2 exp exp CLOSE_PAREN 
            | OPEN_PAREN signos1 varcte CLOSE_PAREN 
            | varcte 
            | llamada
            | returnelement'''

##### SIGNOS 1 #####

def p_signos1(p):
    '''signos1 : PLUS 
                | MINUS ''' 

##### SIGNOS 2 #####

def p_signos2(p):
    '''signos2 : TIMES 
                | DIVIDE '''

##### VARCTE #####

def p_varcte(p):
    ''' varcte : ID 
                | CTEI
                | CTEF '''

                    
##### DECLARACIONFUNCION #####

def p_declaracionfuncion(p):
    ''' declaracionfuncion : OPEN_PAREN FUNCTIONS declaracionfuncion_2 CLOSE_PAREN '''

def p_declaracionfuncion_2(p):
    ''' declaracionfuncion_2    : funcion declaracionfuncion_2 
                                | empty'''

##### FUNCION #####

def p_funcion(p):
    ''' funcion : OPEN_PAREN DEFINE OPEN_PAREN ID param CLOSE_PAREN bloque CLOSE_PAREN '''

##### PARAM #####

def p_param(p):
    ''' param   : ID param
                | empty '''

##### DECLARACIONVARIABLES #####

def p_declaracionvariables(p):
    ''' declaracionvariables : OPEN_PAREN VARS declaracionvariables_2 CLOSE_PAREN '''
    print("vars 0" ,p[0])
    print("vars 1" ,p[1])
    print("vars 2" ,p[2])

def p_declaracionvariables_2(p):
    ''' declaracionvariables_2 : declare declaracionvariables_2
                                | empty '''

##### DECLARE #####

def p_declare(p):
    ''' declare : OPEN_PAREN DECLARE ID declare_2 CLOSE_PAREN '''

def p_declare_2(p):
    ''' declare_2   : definircte
                    | definirlista'''

##### DEFINIRCTE #####

def p_definircte(p):
    ''' definircte  : CTEI
                    | CTEF
                    | CTEC '''

##### DEFINIRLISTA #####

def p_definirlista(p):
    ''' definirlista : QUOTE OPEN_PAREN definirlista_2 CLOSE_PAREN '''

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
    print("main 0" ,p[0])
    print("main 1" ,p[1])
    print("main 2" ,p[2])

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

'''
# para testear con un file
import os
fileDir = os.path.dirname(os.path.realpath('__file__'))
print( fileDir)

#programa = input('file > ') #descoment este si quieres poner el nombre del file en la terminal

programa = 'test2.txt'
filename = os.path.join(fileDir, 'tests/' + programa )
f = open(filename, "r")

input = f.read()
yacc.parse(input)
'''

#''' # para testear a mano
while True:
    try:
        s = input('programa > ')
    except EOFError:
        break
    yacc.parse(s)
#'''