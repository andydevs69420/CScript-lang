from csobject import CSToken, CSObject


class CSNullType(CSObject):
    """NullType backend for CScript

        Paramters
        ---------
        _null : NoneType
    """

    def __init__(self):
        super().__init__()
        self.put("this", None)

    # ============ PYTHON|
    # ===================|
    
    def __str__(self):
        return "null"
    
    # ==================== OPERATIONS|
    # ===============================|
    # must be private!. do not include as attribte
    """ CSInteger specific operation
    """
    def bin_not(self, _opt:CSToken, _allocate:bool=True):
        return CSObject.new_boolean("true" if not self.get("this") else "false", _allocate)
