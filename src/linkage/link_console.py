
from . import PyLinkInterface, CSNullType, CSString, CSObject


from colorama import Fore
from os import system


class ConsoleLink(PyLinkInterface):

    def __init__(self):
        super().__init__()
        self.linkname = "console"
        self.variable = ({
            "qualname" : CSString(self.linkname)
        })
        
        self.metadata = ({
            "initialize" : {"name": "initialize", "argc": 0},
            "write"      : {"name": "write"     , "argc": 1},
            "log"        : {"name": "log"       , "argc": 1},
            "error"      : {"name": "error"     , "argc": 1},
            "warn"       : {"name": "warn"      , "argc": 1},
            "readLine"   : {"name": "readLine"  , "argc": 1},
            "clear"      : {"name": "clear"     , "argc": 0}
        })
    
    def initialize(self, _args:list):
        return self.malloc(_args[0], CSObject())
    
    def write(self, _args:list):
        print(_args[1], end="")
        return self.malloc(_args[0], CSNullType())

    def log(self, _args:list):
        print(_args[1])
        return self.malloc(_args[0], CSNullType())
    
    def error(self, _args:list):
        print(f"{Fore.RED}{_args[1].__str__()}{Fore.RESET}")
        return self.malloc(_args[0], CSNullType())
    
    def warn(self, _args:list):
        print(f"{Fore.YELLOW}{_args[1].__str__()}{Fore.RESET}")
        return self.malloc(_args[0], CSNullType())
    
    def readLine(self, _args:list):
        while True:
            try:
                _input = input(_args[1].__str__())
                return self.malloc(_args[0], CSString(_input))
            except KeyboardInterrupt:
                print()
                continue
        return self.malloc(_args[0], CSNullType())
    
    def clear(self, _args:list):
        system("clear")
        return self.malloc(_args[0], CSNullType())
            


