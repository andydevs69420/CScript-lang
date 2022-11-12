from builtins import len

from . import PyLinkInterface, CSTypes, CSString, CSBoolean, CSInteger


""" Serves as CSInteger prototype
        and all CSInteger operation
            from
            constructor, concat, __toString__

    Strictly: do not modify!!!
    NOTE: you an create your own custom prototype attribute inside cscript
"""

class CSNullTypeLink(PyLinkInterface):

    def __init__(self, _enherit=None):
        super().__init__(_enherit)
        self.linkname = CSTypes.TYPE_CSNULLTYPE
        self.metadata = ({
            "toString" : {"name": "toString"  , "argc": 0},
        })
    
    # toString
    def toString(self, _args:list):
        return self.malloc(_args[0], CSString("null"))