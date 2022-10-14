
# core files
from sys import path, setrecursionlimit
path.append("./src/object"  )
path.append("./src/csriptvm")

setrecursionlimit(15000)


from csparser import CSParser

# core
from cscriptvm.compilable import Compilable
from cscriptvm.csvm import CSVirtualMachine

FILE = "lib/test.cs"
parser = CSParser(FILE, open(FILE, "r").read())
x = parser.parse()
x.compile()

for ins in Compilable.INSTRUCTIONS[-1]:
    print(ins)
print("Done!")

CSVirtualMachine.run(x.getInstructions())
