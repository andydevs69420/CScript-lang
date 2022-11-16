
from .hashmap import HashMap
from csbuiltins import CSTypes

__ALL__=__all__ =["CSObject", "cs_is_primitive_like"]

# for typing
class CSObject(HashMap):pass
class CSObject(HashMap):
    """ Represents Object in CScript
    """
    
    def __init__(self):
        super().__init__()
        # ======== memory flags|
        # =====================|
        self.offset = -69420
        self.cstate = None
        self.objage = None

        self.type = type(self).__name__

        self.hidden = ["__proto__", "qualname"]

    def __str__(self):
        _keys   = self.keys()
        _attrib = ""

        for k in range(len(_keys)):
            _value  = self.get(_keys[k])
            _string = ...

            if  (self.offset == _value.offset):
                # refering to its self
                # to avoid recursion  
                _string = "{self}"
            else:
                if  not (cs_is_primitive_like(_value) or cs_is_code_like(_value)):
                    _string = "[%s]" % _value.type
                else:
                    _string = _value.__str__()

            if  _keys[k] not in self.hidden:
                _attrib += f"{_keys[k]}: {_string}"

                if  k < len(_keys) - 1:
                    _attrib += ", "

        return self.type + ":" + "{" + f"{_attrib}" + "}"
    

def cs_is_code_like(_csobject:CSObject):
    """ Checks if object is a primitive-like in CScript

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return (_csobject.type == CSTypes.TYPE_CSRAWCODE)


def cs_is_primitive_like(_csobject:CSObject):
    """ Checks if object is a primitive-like in CScript

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return _csobject.type in (
        CSTypes.TYPE_CSINTEGER  ,
        CSTypes.TYPE_CSDOUBLE   ,
        CSTypes.TYPE_CSSTRING   ,
        CSTypes.TYPE_CSBOOLEAN  ,
        CSTypes.TYPE_CSNULLTYPE ,
    )

