
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
    'null?' : 'NULL_PREDICADE',
    'list?' : 'LIST_PREDICADE',
    'empty?' : 'EMPTY_PREDICADE',
    'append' : 'APPEND',
    'list' : 'LIST',
    'map' : 'MAP',
    'filter' : 'FILTER',
    '#t' : 'FALSE',
    '#f' : 'TRUE',
    'even?' : 'EVEN_PREDICADE',
    'int?' : 'INT_PREDICADE',
    'float?' : 'FLOAT_PREDICADE'
}

tokens = [
    'ID',
    'CTEI',
    'CTEF',
    'CTEC',
    'OPEN_PAREN','CLOSE_PAREN',
    'PLUS','MINUS','TIMES','DIVIDE',
    'LT','GT','NE','EQUAL'
] + list(reserved.values())

digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
t_CTEI = r'(' + digit + r'+)'
t_CTEF = r'(' + digit + r'+(\.' + digit +  r')+)'
t_CTEC = r'(' + nondigit + r'+)'
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LT = r'<'
t_GT = r'>'
t_NE = r'<>'
t_EQUAL = r'='


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

def p_programa(p):
    ''' programa : OPEN_PAREN PROGRAM CLOSE_PAREN'''


def p_error(p):
    print(f"Syntax error at {p.value!r}")

def p_empty(p):
     'empty :'
     pass

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input('programa > ')
    except EOFError:
        break
    yacc.parse(s)
