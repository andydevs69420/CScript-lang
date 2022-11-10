from builtins import len

from . import PyLinkInterface, CSTypes, CSString, CSBoolean, CSInteger


""" Serves as CSInteger prototype
        and all CSInteger operation
            from
            constructo, concat, __toString__

    Strictly: do not modify!!!
    NOTE: you an create your own custom prototype attribute inside cscript
"""

class CSNullTypeLink(PyLinkInterface):

    def __init__(self, _enherit=None):
        super().__init__(_enherit)
        self.linkname = CSTypes.TYPE_CSNULLTYPE
        self.metadata = ({
            "__toString__" : {"name": "__toString__", "argc": 1},
        })
    
    # __toString__
    def __toString__(self, _args:list):
        return self.malloc(_args[0], CSString("null"))