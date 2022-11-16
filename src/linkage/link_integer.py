
from . import PyLinkInterface
from . import CSInteger, CSDouble, CSString, CSBoolean, CSTypes


""" Serves as CSInteger prototype

    Strictly: do not modify!!!
    NOTE: you an create your own custom prototype attribute inside cscript
"""

class CSIntegerLink(PyLinkInterface):

    def __init__(self, _enherit=None):
        super().__init__(_enherit)
        self.linkname = CSTypes.TYPE_CSINTEGER

        self.variable = ({
            "qualname" : CSString(self.linkname)
        })

        self.metadata = ({
            "initialize" : {"name": "initialize", "argc": 1},
            "tryParse"   : {"name": "tryParse"  , "argc": 1},
            "toString"   : {"name": "toString"  , "argc": 0},
        })
    
    def initialize(self, _args:list):
        # constructor
        return _args[1]
    

    def tryParse(self, _args:list):
        _param = _args[1]
        if  _param.type == CSTypes.TYPE_CSINTEGER:
            return _param
        elif _param.type == CSTypes.TYPE_CSSTRING:
            _str = _param.this
            if  _str.isdigit():
                return self.malloc(_args[0], CSInteger(int(_str)))

        return self.malloc(_args[0], CSInteger(0))
   
    # toString
    def toString(self, _args:list):
        # check if "this exist!"
        if  not _args[0].scope[-1].exists("this"):
            return self.malloc(_args[0], CSString(""))

        # invoke "this"
        _this = self.getName(_args[0], "this")

        # return
        return self.malloc(_args[0], CSString(_this.__str__()))
        
