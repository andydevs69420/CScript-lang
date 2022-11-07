
# core files
from sys import path, setrecursionlimit

path.append("./src/object"    )
path.append("./src/utility"   )
path.append("./src/grammarp"  )
path.append("./src/compiler"  )
path.append("./src/csbuiltins")
# ===========================
path.append("./lib"           )
path.append("./tests"         )

setrecursionlimit(15000)



# core
from compiler.cscompiler import CSCompiler
from cscriptvm import cs__run



def main(_args:dict):
    FILE     = "tests/class_test.csx"
    compiler = CSCompiler(FILE, open(FILE, "r").read())
    cs__run(compiler.compile())
main({})

