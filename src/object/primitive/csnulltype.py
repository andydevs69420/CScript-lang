from obj_utils.csclassnames import CSClassNames
from base.csobject import CSToken, CSObject
from obj_utils.nonpointer import NonPointer


class CSNullType(NonPointer):
    """NullType backend for CScript

        Paramters
        ---------
        _null : NoneType
    """
    THIS= "this"

    def __init__(self):
        super().__init__()
        
        self.dtype = CSClassNames.CSNullType
        self.thiso.put(CSNullType.THIS, None)

    def __str__(self):
        return "null"
    
    # ==================== OPERATIONS|
    # ===============================|
    # must be private!. do not include as attribte
    """ CSInteger specific operation
    """
    def bin_not(self, _opt:CSToken):
        return CSObject.new_boolean("true" if not self.python() else "false")

    def eq(self, _opt: CSToken, _object: CSObject):
        return  CSObject.new_boolean("true" if (self.offset == _object.offset) else "false" )

    def equals(self, _object: CSObject):
        return  CSObject.new_boolean("true" if (self.offset != _object.offset) else "false" )