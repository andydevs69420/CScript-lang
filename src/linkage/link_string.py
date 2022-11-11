from builtins import len

from . import PyLinkInterface, CSTypes, CSString, CSBoolean, CSInteger


""" Serves as CSString prototype

    Strictly: do not modify!!!
    NOTE: you an create your own custom prototype attribute inside cscript
"""

class CSStringLink(PyLinkInterface):

    def __init__(self, _enherit=None):
        super().__init__(_enherit)
        self.linkname = CSTypes.TYPE_CSSTRING

        self.variable = ({
            "qualname" : CSString(self.linkname)
        })

        self.metadata = ({
            "initialize" : {"name": "initialize", "argc": 1},
            "length"     : {"name": "length"    , "argc": 0},
            "toString"   : {"name": "toString"  , "argc": 0},
        })
    
    # constructor
    def initialize(self, _args:list):
        return _args[2]
    
    # length
    def length(self, _args:list):
        return self.malloc(_args[0], CSInteger(len(self.getName(_args[0], "this").this)))
    
    # toString
    def toString(self, _args:list):
        # check if "this exist!"
        if  not _args[0].calls.top().locvars[-1].exists("this"):
            return self.malloc(_args[0], CSString(""))

        # invoke "this"
        _this = self.getName(_args[0], "this")

        # return
        return _this
    




