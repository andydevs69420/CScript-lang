



from .cstypes import CSTypes
from .base.csobject import CSObject, cs_is_primitive_like


class CSArray(CSObject):
    """ Represents array in cscript
    """

    def __init__(self):
        super().__init__()
        self.type     = CSTypes.TYPE_CSARRAY
        self.size     = 0
        self.internal = CSObject()

    def local_put(self, _index_str:str, _object:CSObject):
        self.internal.put(_index_str, _object)
    
    def put(self, _other_object:CSObject):
        self.internal.put(str(self.size), _other_object)
        self.size += 1
    
    def all(self):
        _temp = [*self.internal.all()]
        _temp.extend(super().all())
        return _temp
    
    def __str__(self):
        _all = self.internal.all()
        _fmt = ""
        for _r in range(len(_all)):

            if  self.offset == _all[_r].offset:
                _fmt += "[self]"
            else:
                if  not cs_is_primitive_like(_all[_r]):
                    _fmt += "[%s]" % _all[_r].type
                else:
                    _fmt += _all[_r].__str__()

            if  _r < len(_all) - 1:
                _fmt += ", "


        return "[" + _fmt + "]"

