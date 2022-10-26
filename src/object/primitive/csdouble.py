
from obj_utils.csclassnames import CSClassNames
from .csnumber import CSNumber


class CSDouble(CSNumber):
    """ Double backend for CScript

        Paramters
        ---------
        _flt : float
    """

    def __init__(self, _flt:float):
        super().__init__()
        self.dtype = CSClassNames.CSDouble
        self.put("this", float(_flt))
    
    # ======================== PYTHON|
    # ===============================|