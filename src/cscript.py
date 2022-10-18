
# core files
from sys import path, setrecursionlimit
path.append("./src/object"  )
path.append("./src/astnode" )
path.append("./src/csriptvm")

setrecursionlimit(15000)


from csparser import CSParser

# core
from cscriptvm.csvm import CSVirtualMachine

FILE = "lib/test.cs"
parser = CSParser(FILE, open(FILE, "r").read())
x = parser.parse()
instruct =  x.compile()

for ins in instruct:
    print(ins)
print("Done!")

CSVirtualMachine.run(instruct)
