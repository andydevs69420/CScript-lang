
# core files
from sys import path, setrecursionlimit
path.append("./src/object"  )
path.append("./src/csriptvm")

setrecursionlimit(15000)


from csparser import CSParser
from compilable import Compilable

FILE = "lib/test.cs"
parser = CSParser(FILE, open(FILE, "r").read())
parser.parse().compile()
for ins in Compilable.INSTRUCTIONS[-1]:
    print(ins)