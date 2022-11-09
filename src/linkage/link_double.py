
from . import PyLinkInterface
from . import CSInteger, CSDouble, CSString, CSBoolean, CSTypes


""" Serves as CSDouble prototype
        and all CSDouble operation
            from
            unary, arithmetic, comparison

    Strictly: do not modify!!!
    NOTE: you an create your own custom prototype attribute inside cscript
"""

class CSDoubleLink(PyLinkInterface):

    def __init__(self, _enherit=None):
        super().__init__(_enherit)
        self.linkname = CSTypes.TYPE_CSDOUBLE
        self.metadata = ({
           self.linkname  : {"name": self.linkname  , "argc": 1},
            "__toString__": {"name": "__toString__" , "argc": 0},
        })
    
    def CSDouble(self, _args:list):
        return _args[2]
    
    # toString
    def __toString__(self, _args:list):
        return self.malloc(_args[0], CSString(_args[1].__str__()))
        
