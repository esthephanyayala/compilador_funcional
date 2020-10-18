

semanticCube = {
    "int" : {
        "int" : {
            "+" : "int",
            "-" : "int",
            "*" : "int",
            "/" : "int",
            "<" : "bool",
            ">" : "bool",
            "!=" : "bool",
            "=" : "bool"
        },

        "float" : {
            "+" : "float",
            "-" : "float",
            "*" : "float",
            "/" : "float",
            "<" : "bool",
            ">" : "bool",
            "!=" : "bool",
            "=" : "bool"
        },

        "bool" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },

        "char" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },
        
        "list" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        }
    },
    "float" : {
        "int" : {
            "+" : "float",
            "-" : "float",
            "*" : "float",
            "/" : "float",
            "<" : "bool",
            ">" : "bool",
            "!=" : "bool",
            "=" : "bool"
        },

        "float" : {
            "+" : "float",
            "-" : "float",
            "*" : "float",
            "/" : "float",
            "<" : "bool",
            ">" : "bool",
            "!=" : "bool",
            "=" : "bool"
        },

        "bool" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },

        "char" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },
        
        "list" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        }
    },
    "bool" : {
        "int" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },

        "float" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },

        "bool" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "bool",
            "=" : "bool"
        },

        "char" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },
        
        "list" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        }
    },
    "char" : {
        "int" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },

        "float" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },

        "bool" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },

        "char" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "bool",
            "=" : "bool"
        },
        
        "list" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        }
    },
    "list" : {
        "int" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },

        "float" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },

        "bool" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },

        "char" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        },

        "list" : {
            "+" : "ERROR",
            "-" : "ERROR",
            "*" : "ERROR",
            "/" : "ERROR",
            "<" : "ERROR",
            ">" : "ERROR",
            "!=" : "ERROR",
            "=" : "ERROR"
        }
    }
}

#print(semanticCube['int']['list']['+'])