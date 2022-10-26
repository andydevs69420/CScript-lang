from obj_utils.csclassnames import CSClassNames
from base.csobject import CSToken, CSObject


class CSNullType(CSObject):
    """NullType backend for CScript

        Paramters
        ---------
        _null : NoneType
    """

    def __init__(self):
        super().__init__()
        self.initializeBound()

        self.dtype = CSClassNames.CSNullType
        self.put("this", None)

    # ======================== PYTHON|
    # ===============================|
    
    def __str__(self):
        return "null"
    
    # ==================== OPERATIONS|
    # ===============================|
    # must be private!. do not include as attribte
    """ CSInteger specific operation
    """
    def bin_not(self, _opt:CSToken):
        return CSObject.new_boolean("true" if not self.get("this") else "false")
