
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
            "initialize" : {"name": "initialize", "argc": 1},
            "toString"   : {"name": "toString"  , "argc": 1},
        })
    
    def initialize(self, _args:list):
        return _args[2]
    
    # toString
    def toString(self, _args:list):
        # return
        return CSString("not implemented")
        
