
from csobject import CSObject

""" CSObject|Hashmap wrapper

    Use CSMap instead of object directly!
"""

class CSMap(CSObject):
    def __init__(self):
        super().__init__()
    
    # ============ PYTHON|
    # ===================|

    def all(self):
        return super().all()

    def isPointer(self):
        return True
    
    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte
    

    # ==================== OPERATIONS|
    # ===============================|
    # must be private!. do not include as attribte
