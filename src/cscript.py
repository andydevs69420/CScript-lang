
# core files
from sys import path, setrecursionlimit
path.append("./src/object"  )
path.append("./src/astnode" )
path.append("./src/csriptvm")
# ===========================
path.append("./lib"         )
path.append("./tests"       )

setrecursionlimit(15000)



# core
from compiler.cscompiler import CSCompiler



def main(_args:dict):
    FILE     = "tests/class_test.csx"
    compiler = CSCompiler(FILE, open(FILE, "r").read())
    compiler.compile()


main({})

