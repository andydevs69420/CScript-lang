
# core files
from sys import path, setrecursionlimit
path.append("./src/object"  )
path.append("./src/astnode" )
path.append("./src/csriptvm")

setrecursionlimit(15000)


from csparser import CSParser

# core
from cscriptvm.csvm import CSVM

# object
from object.builtins.cshelpers import __read__



def main(_args:dict):
    FILE     = "eval.csx"
    parser   = CSParser(FILE, __read__(FILE))
    aST      = parser.parse()
    instruct = aST.compile()
    for ins in instruct:
        print(ins)
    print("Done!")
    CSVM.run(instruct)
    CSVM.VHEAP.collectlast()


main({})

