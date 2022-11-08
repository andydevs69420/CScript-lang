
from . import PyLinkInterface
from . import CSInteger, CSDouble, CSString, CSBoolean, CSTypes


""" Serves as CSInteger prototype
        and all CSInteger operation
            from
            unary, arithmetic, shift, comparison, biwise logic

    Strictly: do not modify!!!
    NOTE: you an create your own custom prototype attribute inside cscript
"""

class CSDoubleLink(PyLinkInterface):

    def __init__(self, _enherit=None):
        super().__init__(_enherit)
        self.linkname = CSTypes.TYPE_CSDOUBLE
        self.metadata = ({
            self.linkname         : {"name": self.linkname          , "argc": 1},

            # unary/postfix
            "__log_not__"         : {"name": "__log_not__"          , "argc": 0},
            "__uplus__"           : {"name": "__uplus__"            , "argc": 0},
            "__uminus__"          : {"name": "__uminus__"           , "argc": 0},
            "__inc__"             : {"name": "__inc__"              , "argc": 0},
            "__dec__"             : {"name": "__dec__"              , "argc": 0},

            # arithmetics
            "__pow_CSInteger__"   : {"name": "__pow_CSInteger__"    , "argc": 1},
            "__pow_CSDouble__"    : {"name": "__pow_CSDouble__"     , "argc": 1},

            "__mul_CSInteger__"   : {"name": "__mul_CSInteger__"    , "argc": 1},
            "__mul_CSDouble__"    : {"name": "__mul_CSDouble__"     , "argc": 1},

            "__div_CSInteger__"   : {"name": "__div_CSInteger__"    , "argc": 1},
            "__div_CSDouble__"    : {"name": "__div_CSDouble__"     , "argc": 1},

            "__mod_CSInteger__"   : {"name": "__mod_CSInteger__"    , "argc": 1},
            "__mod_CSDouble__"    : {"name": "__mod_CSDouble__"     , "argc": 1},

            "__add_CSInteger__"   : {"name": "__add_CSInteger__"    , "argc": 1},
            "__add_CSDouble__"    : {"name": "__add_CSDouble__"     , "argc": 1},

            "__sub_CSInteger__"   : {"name": "__sub_CSInteger__"    , "argc": 1},
            "__sub_CSDouble__"    : {"name": "__sub_CSDouble__"     , "argc": 1},

            # comparison
            "__lt_CSInteger__"    : {"name": "__lt_CSInteger__"     , "argc": 1},
            "__lt_CSDouble__"     : {"name": "__lt_CSDouble__"      , "argc": 1},
            "__lte_CSInteger__"   : {"name": "__lte_CSInteger__"    , "argc": 1},
            "__lte_CSDouble__"    : {"name": "__lte_CSDouble__"     , "argc": 1},
            "__gt_CSInteger__"    : {"name": "__gt_CSInteger__"     , "argc": 1},
            "__gt_CSDouble__"     : {"name": "__gt_CSDouble__"      , "argc": 1},
            "__gte_CSInteger__"   : {"name": "__gte_CSInteger__"    , "argc": 1},
            "__gte_CSDouble__"    : {"name": "__gte_CSDouble__"     , "argc": 1},
            "__eq_CSInteger__"    : {"name": "__eq_CSInteger__"     , "argc": 1},
            "__eq_CSDouble__"     : {"name": "__eq_CSDouble__"      , "argc": 1},
            "__neq_CSInteger__"   : {"name": "__neq_CSInteger__"    , "argc": 1},
            "__neq_CSDouble__"    : {"name": "__neq_CSDouble__"     , "argc": 1},
        })
    
    def CSDouble(self, _args:list):
        return _args[2]
    
    # !
    def __log_not__(self, _args:list):
        """ negate int to bool
        """
        return self.malloc(_args[0], CSBoolean(not _args[1].this))
    
    # u+
    def __uplus__(self, _args:list):
        """ negate int to bool
        """
        return self.malloc(_args[0], CSInteger(+ _args[1].this))
    
    # u-
    def __uminus__(self, _args:list):
        """ negate int to bool
        """
        return self.malloc(_args[0], CSInteger(- _args[1].this))
    
    # ++
    def __inc__(self, _args:list):
        """ increment ++
        """
        _args[1].this += 1
        return _args[1]
    
    # --
    def __dec__(self, _args:list):
        """ decrement --
        """
        _args[1].this -= 1
        return _args[1]

    # ^^
    def __pow_CSInteger__(self, _args:list):
        """ raise CSInteger ^^ CSInteger
        """
        return self.malloc(_args[0], CSDouble(_args[1].this ** _args[2].this))
    
    def __pow_CSDouble__(self, _args:list):
        """ raise CSInteger ^^ CSDouble
        """
        return self.malloc(_args[0], CSDouble(_args[1].this ** _args[2].this))
    
    # *
    def __mul_CSInteger__(self, _args:list):
        """ multiply CSInteger * CSInteger
        """
        return self.malloc(_args[0], CSDouble(_args[1].this * _args[2].this))

    def __mul_CSDouble__(self, _args:list):
        """ multiply CSInteger * CSDouble
        """
        return self.malloc(_args[0], CSDouble(_args[1].this * _args[2].this))
    
    # /
    def __div_CSInteger__(self, _args:list):
        """ divide CSInteger / CSInteger
        """
        return self.malloc(_args[0], CSDouble(_args[1].this / _args[2].this))

    def __div_CSDouble__(self, _args:list):
        """ divide CSInteger / CSDouble
        """
        return self.malloc(_args[0], CSDouble(_args[1].this / _args[2].this))
    
    # %
    def __mod_CSInteger__(self, _args:list):
        """ remainder CSInteger % CSInteger
        """
        return self.malloc(_args[0], CSDouble(_args[1].this % _args[2].this))

    def __mod_CSDouble__(self, _args:list):
        """ remainder CSInteger % CSDouble
        """
        return self.malloc(_args[0], CSDouble(_args[1].this % _args[2].this))

    # +
    def __add_CSInteger__(self, _args:list):
        """ adds CSInteger + CSInteger
        """
        return self.malloc(_args[0], CSDouble(_args[1].this + _args[2].this))

    def __add_CSDouble__(self, _args:list):
        """ adds CSInteger + CSDouble
        """
        return self.malloc(_args[0], CSDouble(_args[1].this + _args[2].this))
    
    # -
    def __sub_CSInteger__(self, _args:list):
        """ subtract CSInteger - CSInteger
        """
        return self.malloc(_args[0], CSDouble(_args[1].this - _args[2].this))

    def __sub_CSDouble__(self, _args:list):
        """ subtract CSInteger - CSDouble
        """
        return self.malloc(_args[0], CSDouble(_args[1].this - _args[2].this))
    
    # lt
    def __lt_CSInteger__(self, _args:list):
        """ compare lessthan CSInteger < CSInteger
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this < _args[2].this))

    def __lt_CSDouble__(self, _args:list):
        """ compare lessthan CSInteger < CSDouble
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this < _args[2].this))
    
    # lte
    def __lte_CSInteger__(self, _args:list):
        """ compare lessthan equal CSInteger <= CSInteger
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this <= _args[2].this))

    def __lte_CSDouble__(self, _args:list):
        """ compare lessthan equal CSInteger <= CSDouble
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this <= _args[2].this))

    # gt
    def __gt_CSInteger__(self, _args:list):
        """ compare greaterthan CSInteger > CSInteger
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this > _args[2].this))

    def __gt_CSDouble__(self, _args:list):
        """ compare greaterthan CSInteger > CSDouble
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this > _args[2].this))
    
    # gte
    def __gte_CSInteger__(self, _args:list):
        """ compare greaterthan equal CSInteger >= CSInteger
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this >= _args[2].this))

    def __gte_CSDouble__(self, _args:list):
        """ compare lessthan equal CSInteger <= CSDouble
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this >= _args[2].this))
    
    # eq
    def __eq_CSInteger__(self, _args:list):
        """ equal CSInteger == CSInteger
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this == _args[2].this))

    def __eq_CSDouble__(self, _args:list):
        """ equal CSInteger == CSDouble
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this == _args[2].this))
    
    # neq
    def __neq_CSInteger__(self, _args:list):
        """ not equal CSInteger != CSInteger
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this != _args[2].this))

    def __neq_CSDouble__(self, _args:list):
        """ not equal CSInteger != CSDouble
        """
        return self.malloc(_args[0], CSBoolean(_args[1].this != _args[2].this))


    # toString
    def __toString__(self, _args:list):
        return self.malloc(_args[0], CSString(_args[1].__str__()))
        
