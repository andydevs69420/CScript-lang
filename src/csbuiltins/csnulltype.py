

from csbuiltins.cstypes import CSTypes
from .base.csobject import CSObject


class CSNullType(CSObject):
    """ Represents null in cscript
    """

    DEFAULT =None

    def __init__(self):
        super().__init__()
        self.type = CSTypes.TYPE_CSNULLTYPE
        self.this = None
    
    def __str__(self):
        return "null"

