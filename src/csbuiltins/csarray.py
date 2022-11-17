



from .cstypes import CSTypes
from .base.csobject import CSObject, cs_is_primitive_like


class CSArray(CSObject):
    """ Represents array in cscript
    """

    def __init__(self):
        super().__init__()
        self.type = CSTypes.TYPE_CSARRAY
        self.size = 0
        self.this = []
    
    def local_push(self, _other_object:CSObject):
        self.this.append(_other_object)
        self.size += 1

    def local_pop(self):
        _top = self.this.pop()
        self.size -= 1
        return _top
    
    def all(self):
        _temp = [*self.this]
        _temp.extend(super().all())
        return _temp
    
    def __str__(self):
        _all = self.this
        _fmt = ""
        for _r in range(len(_all)):

            if  self.offset == _all[_r].offset and self.offset >= 0:
                _fmt += "[self]"
            else:
                if  not cs_is_primitive_like(_all[_r]):
                    _fmt += "[%s]" % _all[_r].type
                else:
                    _fmt += _all[_r].__str__()

            if  _r < len(_all) - 1:
                _fmt += ", "


        return "[" + _fmt + "]"

