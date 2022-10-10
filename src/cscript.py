
# core files
from sys import path, setrecursionlimit
path.append("./src/object"   )
path.append("./src/csript-vm")

setrecursionlimit(15000)


from csparser import CSParser

FILE = "lib/test.cs"
parser = CSParser(FILE, open(FILE, "r").read())
print(parser.parse().evaluate().toString())