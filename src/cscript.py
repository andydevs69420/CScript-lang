
# core files
from sys import path, setrecursionlimit
path.append("./src/object"  )
path.append("./src/astnode" )
path.append("./src/csriptvm")
# ===========================
path.append("./lib"         )
path.append("./tests"       )

setrecursionlimit(15000)


from csparser import CSParser

# core
from cscriptvm.csvm import CSVM, ImportStack

# object
from cshelpers import __read__, __base__



def main(_args:dict):
    FILE     = "class_test.csx"
    ImportStack.is_push(__base__(FILE))

    parser   = CSParser(FILE, __read__(FILE))
    aST      = parser.parse()
    instruct = aST.compile()
    for ins in instruct:
        print(ins)
    print("Done!")
    CSVM.run(instruct)
    CSVM.VHEAP.collectlast()


main({})

