
from . import PyLinkInterface, CSNullType, CSString


from colorama import Fore
from os import system


class ConsoleLink(PyLinkInterface):

    def __init__(self):
        super().__init__()
        self.linkname = "console"
        self.metadata = ({
            "log"     : {"name": "log"     , "argc": 1},
            "error"   : {"name": "error"   , "argc": 1},
            "warn"    : {"name": "warn"    , "argc": 1},
            "readLine": {"name": "readLine", "argc": 1},
            "clear"   : {"name": "clear"   , "argc": 0}
        })
    

    def log(self, _args:list):
        print(_args[2])
        return self.malloc(_args[0], CSNullType())
    
    def error(self, _args:list):
        print(f"{Fore.RED}{_args[2].__str__()}{Fore.RESET}")
        return self.malloc(_args[0], CSNullType())
    
    def warn(self, _args:list):
        print(f"{Fore.YELLOW}{_args[2].__str__()}{Fore.RESET}")
        return self.malloc(_args[0], CSNullType())
    
    def readLine(self, _args:list):
        while True:
            try:
                _input = input(_args[2].__str__())
                return self.malloc(_args[0], CSString(_input))
            except KeyboardInterrupt:
                pass
        return self.malloc(_args[0], CSNullType())
    
    def clear(self, _args:list):
        system("clear")
        return self.malloc(_args[0], CSNullType())
            


