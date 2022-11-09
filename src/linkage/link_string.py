from builtins import len

from . import PyLinkInterface, CSTypes, CSString, CSBoolean, CSInteger


""" Serves as CSInteger prototype
        and all CSInteger operation
            from
            constructo, concat, __toString__

    Strictly: do not modify!!!
    NOTE: you an create your own custom prototype attribute inside cscript
"""

class CSStringLink(PyLinkInterface):

    def __init__(self, _enherit=None):
        super().__init__(_enherit)
        self.linkname = CSTypes.TYPE_CSSTRING
        self.metadata = ({
            self.linkname      : {"name": self.linkname      , "argc": 1},
            "length"           : {"name": "length"           , "argc": 0},
            "__toString__"     : {"name": "__toString__"     , "argc": 1},
        })
    
    # constructor
    def CSString(self, _args:list):
        return _args[2]
    
    # length
    def length(self, _args:list):
        return self.malloc(_args[0], CSInteger(len(_args[1].this)))
    
    # __toString__
    def __toString__(self, _args:list):
        return _args[1]
    




