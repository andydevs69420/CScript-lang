
from . import PyLinkInterface
from . import CSInteger, CSDouble, CSString, CSBoolean, CSTypes


""" Serves as CSDouble prototype

    Strictly: do not modify!!!
    NOTE: you an create your own custom prototype attribute inside cscript
"""

class CSDoubleLink(PyLinkInterface):

    def __init__(self, _enherit=None):
        super().__init__(_enherit)
        self.linkname = CSTypes.TYPE_CSDOUBLE
        
        self.variable = ({
            "qualname" : CSString(self.linkname)
        })

        self.metadata = ({
            "initialize"  : {"name": "initialize"   , "argc": 1},
            "__toString__": {"name": "__toString__" , "argc": 0},
        })
    
    def initialize(self, _args:list):
        return _args[2]
    
    # toString
    def __toString__(self, _args:list):
        # check if "this exist!"
        if  not _args[0].scope[-1].exists("this"):
            return self.malloc(_args[0], CSString(""))

        # invoke "this"
        _this = self.getName(_args[0], "this")

        # return
        return self.malloc(_args[0], CSString(_this.__str__()))
        
