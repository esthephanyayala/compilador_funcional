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
