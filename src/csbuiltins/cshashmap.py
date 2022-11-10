

from .cstypes import CSTypes
from .base.csobject import CSObject


class CSHashMap(CSObject):

    def __init__(self):
        super().__init__()
        self.type = CSTypes.TYPE_CSHASHMAP
    
    def __str__(self):
        _keys   = self.keys()
        _attrib = ""
        for k in range(len(_keys)):
            _value  = self.get(_keys[k])
            _string = ...

            if  (self is _value) or self.offset == _value.offset:
                # refering to its self
                # to avoid recursion  
                _string = "{self}"
            else:
                _string = _value.__str__()

            if  _keys[k] not in self.hidden:
                _attrib += f"{_keys[k]}: {_string}"

                if  k < (len(_keys) - 1):
                    _attrib += ", "

        return "{" + f"{_attrib}" + "}"

