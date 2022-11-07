

# .
from csbuiltins.csboolean import CSBoolean
from .cstypes import CSTypes
from .base.csobject import CSObject
from .csinteger import CSInteger
from .csdouble import CSDouble
from .csstring import CSString
from .csnulltype import CSNullType
from .csnan import CSNaN
from .csfunction import CSFunction
from .csnativefunction import CSNativeFunction


# utility
from utility import logger


PROTO_ATTR_NAME__pow__       = "__pow__"
PROTO_ATTR_NAME__mul__       = "__mul__"
PROTO_ATTR_NAME__div__       = "__div__"
PROTO_ATTR_NAME__mod__       = "__mod__"
PROTO_ATTR_NAME__add__       = "__add__"
PROTO_ATTR_NAME__sub__       = "__sub__"
PROTO_ATTR_NAME__lshift__    = "__lshift__"
PROTO_ATTR_NAME__rshift__    = "__rshift__"
PROTO_ATTR_NAME__lt__        = "__lt__"
PROTO_ATTR_NAME__lte__       = "__lte__"
PROTO_ATTR_NAME__gt__        = "__gt__"
PROTO_ATTR_NAME__gte__       = "__gte__"
PROTO_ATTR_NAME__eq__        = "__eq__"
PROTO_ATTR_NAME__neq__       = "__neq__"
PROTO_ATTR_NAME__and__       = "__and__"
PROTO_ATTR_NAME__xor__       = "__xor__"
PROTO_ATTR_NAME__or__        = "__or__"
PROTO_ATTR_NAME__toString__  = "__toString__"


def is_integer(_csobject:CSObject):
    """ Checks if CSObject is a csinteger

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return (_csobject.type == CSTypes.TYPE_CSINTEGER)

def is_double(_csobject:CSObject):
    """ Checks if CSObject is a csdouble

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return (_csobject.type == CSTypes.TYPE_CSDOUBLE)

def is_number(_csobject:CSObject):
    """ Checks if CSObject is a number

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return (is_integer(_csobject) or is_double(_csobject))


def is_string(_csobject):
    """ Checks if CSObject is a string

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return (_csobject.type == CSTypes.TYPE_CSSTRING)

def typeof(_left:CSObject, _right:CSObject):
    """ Checks if CSObject is a number

        Parameters
        ----------
        _left : CSObject
        _right : CSObject

        Returns
        -------
        CSType
    """
    if  is_number(_left) and is_number(_right):

        if  _left.type  == CSTypes.TYPE_CSDOUBLE or\
            _right.type == CSTypes.TYPE_CSDOUBLE:
            return CSDouble
        else:
            return CSInteger

    if  (_left.type == _right.type) == (_left.type == CSTypes.TYPE_CSSTRING):
        return CSString
    
    return CSNaN



# ============ object|
# ===================|
def csB__object_proto(_env):
    _csobject = _env.vheap.cs__malloc(CSObject())

    # proto attr
    _csobject.put(CSTypes.TYPE_CSOBJECT      , csB__object__constructor(_env)) # default constructor
    _csobject.put(PROTO_ATTR_NAME__pow__     , csB__object____pow__    (_env)) # __pow__
    _csobject.put(PROTO_ATTR_NAME__mul__     , csB__object____mul__    (_env)) # __mul__
    _csobject.put(PROTO_ATTR_NAME__div__     , csB__object____div__    (_env)) # __div__
    _csobject.put(PROTO_ATTR_NAME__mod__     , csB__object____mod__    (_env)) # __mod__
    _csobject.put(PROTO_ATTR_NAME__add__     , csB__object____add__    (_env)) # __add__
    _csobject.put(PROTO_ATTR_NAME__sub__     , csB__object____sub__    (_env)) # __sub__
    _csobject.put(PROTO_ATTR_NAME__lshift__  , csB__object____lshift__ (_env)) # __lshift__
    _csobject.put(PROTO_ATTR_NAME__rshift__  , csB__object____rshift__ (_env)) # __rshift__
    _csobject.put(PROTO_ATTR_NAME__lt__      , csB__object____lt__     (_env)) # __lt__
    _csobject.put(PROTO_ATTR_NAME__lte__     , csB__object____lte__    (_env)) # __lte__
    _csobject.put(PROTO_ATTR_NAME__gt__      , csB__object____gt__     (_env)) # __gt__
    _csobject.put(PROTO_ATTR_NAME__gte__     , csB__object____gte__    (_env)) # __gte__
    _csobject.put(PROTO_ATTR_NAME__eq__      , csB__object____eq__     (_env)) # __eq__
    _csobject.put(PROTO_ATTR_NAME__neq__     , csB__object____neq__    (_env)) # __neq__
    _csobject.put(PROTO_ATTR_NAME__and__     , csB__object____and__    (_env)) # __and__
    _csobject.put(PROTO_ATTR_NAME__xor__     , csB__object____xor__    (_env)) # __xor__
    _csobject.put(PROTO_ATTR_NAME__or__      , csB__object____or__     (_env)) # __or__
    _csobject.put(PROTO_ATTR_NAME__toString__, csB__object__toString__ (_env)) # default __toString__
    # proto attr

    _env.scope[-1].insert(CSTypes.TYPE_CSOBJECT, _address=_csobject.offset, _global=True)

    return _csobject

# constructor
def csB__object__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSOBJECT), CSInteger(0), object__constructor))

def object__constructor(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSObject())


# __pow__
def csB__object____pow__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__pow__), CSInteger(1), object____pow__))

def object____pow__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSNaN())
    #
    TYPE = typeof(_args[1], _args[2])
    return _args[0].vheap.cs__malloc(TYPE(_args[1].this ** _args[2].this))


# __mul__
def csB__object____mul__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__mul__), CSInteger(1), object____mul__))

def object____mul__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSNaN())
    #
    TYPE = typeof(_args[1], _args[2])
    return _args[0].vheap.cs__malloc(TYPE(_args[1].this * _args[2].this))

# __div__
def csB__object____div__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__div__), CSInteger(1), object____div__))

def object____div__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSNaN())
    #
    TYPE = typeof(_args[1], _args[2])
    return _args[0].vheap.cs__malloc(TYPE(_args[1].this / _args[2].this))

# __mod__
def csB__object____mod__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__mod__), CSInteger(1), object____mod__))

def object____mod__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSNaN())
    #
    TYPE = typeof(_args[1], _args[2])
    return _args[0].vheap.cs__malloc(TYPE(_args[1].this % _args[2].this))

# __add__
def csB__object____add__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__add__), CSInteger(1), object____add__))

def object____add__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  is_string(_args[2]):
        # concat mode
        return _args[0].vheap.cs__malloc(CSString(_args[1].__str__() + _args[2].__str__()))
    # each class must re-implement this
    return _args[0].vheap.cs__malloc(CSNaN())

# __sub__
def csB__object____sub__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__sub__), CSInteger(1), object____sub__))

def object____sub__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSNaN())
    #
    TYPE = typeof(_args[1], _args[2])
    return _args[0].vheap.cs__malloc(TYPE(_args[1].this - _args[2].this))

# __lshift__
def csB__object____lshift__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__lshift__), CSInteger(1), object____lshift__))

def object____lshift__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  is_integer(_args[1]):
        return _args[1]
    elif is_integer(_args[2]):
        return _args[2]
    return _args[0].vheap.cs__malloc(CSInteger(0))

# __rshift__
def csB__object____rshift__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__rshift__), CSInteger(1), object____rshift__))

def object____rshift__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  is_integer(_args[1]):
        return _args[1]
    elif is_integer(_args[2]):
        return _args[2]
    return _args[0].vheap.cs__malloc(CSInteger(0))

# __lt__
def csB__object____lt__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__lt__), CSInteger(1), object____lt__))

def object____lt__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSBoolean(False))

# __lte__
def csB__object____lte__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__lte__), CSInteger(1), object____lte__))

def object____lte__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSBoolean(False))

# __gt__
def csB__object____gt__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__gt__), CSInteger(1), object____gt__))

def object____gt__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSBoolean(False))

# __gte__
def csB__object____gte__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__gte__), CSInteger(1), object____gte__))

def object____gte__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSBoolean(False))

# __eq__
def csB__object____eq__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__eq__), CSInteger(1), object____eq__))

def object____eq__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    # compare memory location
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].offset == _args[2].offset))

# __neq__
def csB__object____neq__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__neq__), CSInteger(1), object____neq__))

def object____neq__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    # compare memory location
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].offset != _args[2].offset))

# __and__
def csB__object____and__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__and__), CSInteger(1), object____and__))

def object____and__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  is_integer(_args[1]):
        return _args[1]
    elif is_integer(_args[2]):
        return _args[2]
    return _args[0].vheap.cs__malloc(CSInteger(0))

# __xor__
def csB__object____xor__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__xor__), CSInteger(1), object____xor__))

def object____xor__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  is_integer(_args[1]):
        return _args[1]
    elif is_integer(_args[2]):
        return _args[2]
    return _args[0].vheap.cs__malloc(CSInteger(0))

# __or__
def csB__object____or__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__or__), CSInteger(1), object____or__))

def object____or__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  is_integer(_args[1]):
        return _args[1]
    elif is_integer(_args[2]):
        return _args[2]
    return _args[0].vheap.cs__malloc(CSInteger(0))

# __toString__
def csB__object__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), object__toString__))

def object__toString__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))












# =========== integer|
# ===================|
def csB__integer_proto(_env, _enherit=None):
    _csinteger = _env.vheap.cs__malloc(CSObject())
    # alter object type
    _csinteger.type = CSTypes.TYPE_CSINTEGER

    if  _enherit:
        for _k in _enherit.keys():
            _csinteger.put(_k, _enherit.get(_k))

    # proto attr
    _csinteger.put(CSTypes.TYPE_CSINTEGER      , csB__integer__constructor(_env)) # default constructor
    _csinteger.put(PROTO_ATTR_NAME__add__      , csB__integer____add__    (_env)) # __add__
    _csinteger.put(PROTO_ATTR_NAME__lshift__   , csB__integer____lshift__ (_env)) # __lshift__
    _csinteger.put(PROTO_ATTR_NAME__rshift__   , csB__integer____rshift__ (_env)) # __rshift__
    _csinteger.put(PROTO_ATTR_NAME__lt__       , csB__integer____lt__     (_env)) # __lt__
    _csinteger.put(PROTO_ATTR_NAME__lte__      , csB__integer____lte__    (_env)) # __lte__
    _csinteger.put(PROTO_ATTR_NAME__gt__       , csB__integer____gt__     (_env)) # __gt__
    _csinteger.put(PROTO_ATTR_NAME__gte__      , csB__integer____gte__    (_env)) # __gte__
    _csinteger.put(PROTO_ATTR_NAME__eq__       , csB__integer____eq__     (_env)) # __eq__
    _csinteger.put(PROTO_ATTR_NAME__neq__      , csB__integer____neq__    (_env)) # __neq__
    _csinteger.put(PROTO_ATTR_NAME__and__      , csB__integer____and__    (_env)) # __and__
    _csinteger.put(PROTO_ATTR_NAME__xor__      , csB__integer____xor__    (_env)) # __xor__
    _csinteger.put(PROTO_ATTR_NAME__or__       , csB__integer____or__     (_env)) # __or__
    _csinteger.put(PROTO_ATTR_NAME__toString__ , csB__integer__toString__ (_env)) # default __toString__
    # proto attr
    _env.scope[-1].insert(CSTypes.TYPE_CSINTEGER, _address=_csinteger.offset, _global=True)

    return _csinteger

# constructor
def csB__integer__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSINTEGER), CSInteger(1), integer__constructor))

def integer__constructor(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(_args[2])

# __add__
def csB__integer____add__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__add__), CSInteger(1), integer____add__))

def integer____add__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        if  is_string(_args[2]):
            # concat mode
            return _args[0].vheap.cs__malloc(CSString(_args[1].__str__() + _args[2].__str__()))
        return _args[0].vheap.cs__malloc(CSNaN())
    # always int
    TYPE = typeof(_args[1], _args[2])
    return _args[0].vheap.cs__malloc(TYPE(_args[1].this + _args[2].this))


# __lshift__
def csB__integer____lshift__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__lshift__), CSInteger(1), integer____lshift__))

def integer____lshift__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_integer(_args[1]) and is_integer(_args[2])):
        if  is_integer(_args[1]):
            return _args[1]
        elif is_integer(_args[2]):
            return _args[2]
        return _args[0].vheap.cs__malloc(CSInteger(0))
    # always int
    return _args[0].vheap.cs__malloc(CSInteger(_args[1].this << _args[2].this))


# __rshift__
def csB__integer____rshift__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__rshift__), CSInteger(1), integer____rshift__))

def integer____rshift__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_integer(_args[1]) and is_integer(_args[2])):
        if  is_integer(_args[1]):
            return _args[1]
        elif is_integer(_args[2]):
            return _args[2]
        return _args[0].vheap.cs__malloc(CSInteger(0))
    # always int
    return _args[0].vheap.cs__malloc(CSInteger(_args[1].this >> _args[2].this))

# __lt__
def csB__integer____lt__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__lt__), CSInteger(1), integer____lt__))

def integer____lt__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this < _args[2].this))

# __lte__
def csB__integer____lte__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__lte__), CSInteger(1), integer____lte__))

def integer____lte__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this <= _args[2].this))

# __gt__
def csB__integer____gt__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__gt__), CSInteger(1), integer____gt__))

def integer____gt__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this > _args[2].this))

# __gte__
def csB__integer____gte__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__gte__), CSInteger(1), integer____gte__))

def integer____gte__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this >= _args[2].this))

# __eq__
def csB__integer____eq__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__eq__), CSInteger(1), integer____eq__))

def integer____eq__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this == _args[2].this))

# __neq__
def csB__integer____neq__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__neq__), CSInteger(1), integer____neq__))

def integer____neq__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this == _args[2].this))

# __and__
def csB__integer____and__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__and__), CSInteger(1), integer____and__))

def integer____and__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_integer(_args[1]) or is_integer(_args[2])):
        if  is_integer(_args[1]):
            return _args[1]
        elif is_integer(_args[2]):
            return _args[2]
        return _args[0].vheap.cs__malloc(CSInteger(0))
    # always int
    return _args[0].vheap.cs__malloc(CSInteger(_args[1].this & _args[2].this))

# __xor__
def csB__integer____xor__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__xor__), CSInteger(1), integer____xor__))

def integer____xor__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_integer(_args[1]) and is_integer(_args[2])):
        if  is_integer(_args[1]):
            return _args[1]
        elif is_integer(_args[2]):
            return _args[2]
        return _args[0].vheap.cs__malloc(CSInteger(0))
    # always int
    return _args[0].vheap.cs__malloc(CSInteger(_args[1].this ^ _args[2].this))

# __or__
def csB__integer____or__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__or__), CSInteger(1), integer____or__))

def integer____or__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_integer(_args[1]) and is_integer(_args[2])):
        if  is_integer(_args[1]):
            return _args[1]
        elif is_integer(_args[2]):
            return _args[2]
        return _args[0].vheap.cs__malloc(CSInteger(0))
    # always int
    return _args[0].vheap.cs__malloc(CSInteger(_args[1].this | _args[2].this))


# __toString__
def csB__integer__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), integer__toString__))

def integer__toString__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))











# ============ double|
# ===================|
def csB__double_proto(_env, _enherit=None):
    _csdouble = _env.vheap.cs__malloc(CSObject())
    # alter object type
    _csdouble.type = CSTypes.TYPE_CSDOUBLE

    if  _enherit:
        for _k in _enherit.keys():
            _csdouble.put(_k, _enherit.get(_k))

    # proto attr
    _csdouble.put(CSTypes.TYPE_CSDOUBLE      , csB__double__constructor(_env)) # default constructor
    _csdouble.put(PROTO_ATTR_NAME__add__     , csB__double____add__    (_env)) # __lt__
    _csdouble.put(PROTO_ATTR_NAME__lt__      , csB__double____lt__     (_env)) # __lt__
    _csdouble.put(PROTO_ATTR_NAME__lte__     , csB__double____lte__    (_env)) # __lte__
    _csdouble.put(PROTO_ATTR_NAME__gt__      , csB__double____gt__     (_env)) # __gt__
    _csdouble.put(PROTO_ATTR_NAME__gte__     , csB__double____gte__    (_env)) # __gte__
    _csdouble.put(PROTO_ATTR_NAME__eq__      , csB__double____eq__     (_env)) # __eq__
    _csdouble.put(PROTO_ATTR_NAME__neq__     , csB__double____neq__    (_env)) # __neq__
    _csdouble.put(PROTO_ATTR_NAME__toString__, csB__double__toString__ (_env)) # default __toString__
    # proto attr

    _env.scope[-1].insert(CSTypes.TYPE_CSDOUBLE, _address=_csdouble.offset, _global=True)

    return _csdouble

# constructor
def csB__double__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSDOUBLE), CSInteger(1), double__constructor))

def double__constructor(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(_args[2])

# __add__
def csB__double____add__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__add__), CSInteger(1), double____add__))

def double____add__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        if  is_string(_args[2]):
            # concat mode
            return _args[0].vheap.cs__malloc(CSString(_args[1].__str__() + _args[2].__str__()))
        return _args[0].vheap.cs__malloc(CSNaN())
        
    # always int
    TYPE = typeof(_args[1], _args[2])
    return _args[0].vheap.cs__malloc(TYPE(_args[1].this + _args[2].this))

# __lt__
def csB__double____lt__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__lt__), CSInteger(1), double____lt__))

def double____lt__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this < _args[2].this))

# __lte__
def csB__double____lte__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__lte__), CSInteger(1), double____lte__))

def double____lte__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this <= _args[2].this))

# __gt__
def csB__double____gt__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__gt__), CSInteger(1), double____gt__))

def double____gt__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this > _args[2].this))

# __gte__
def csB__double____gte__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__gte__), CSInteger(1), double____gte__))

def double____gte__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this >= _args[2].this))

# __eq__
def csB__double____eq__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__eq__), CSInteger(1), double____eq__))

def double____eq__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this == _args[2].this))

# __neq__
def csB__double____neq__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__neq__), CSInteger(1), double____neq__))

def double____neq__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    if  not (is_number(_args[1]) and is_number(_args[2])):
        return _args[0].vheap.cs__malloc(CSBoolean(False))
    # always bool
    return _args[0].vheap.cs__malloc(CSBoolean(_args[1].this == _args[2].this))

# __toString__
def csB__double__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), double__toString__))

def double__toString__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))










# ============ string|
# ===================|
def csB__string_proto(_env, _enherit):
    _csstring = _env.vheap.cs__malloc(CSObject())
    # alter object type
    _csstring.type = CSTypes.TYPE_CSSTRING

    if  _enherit:
        for _k in _enherit.keys():
            _csstring.put(_k, _enherit.get(_k))

    # proto attr
    _csstring.put(CSTypes.TYPE_CSSTRING      , csB__string__constructor(_env)) # default constructor
    _csstring.put(PROTO_ATTR_NAME__add__     , csB__string____add__    (_env)) # __add__
    _csstring.put(PROTO_ATTR_NAME__toString__, csB__string__toString__ (_env)) # default __toString__
    # proto attr
    _env.scope[-1].insert(CSTypes.TYPE_CSSTRING, _address=_csstring.offset, _global=True)

    return _csstring

# constructor
def csB__string__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSSTRING), CSInteger(1), string__constructor))

def string__constructor(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(_args[2]) # add cast(again)

# __add__
def csB__string____add__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__add__), CSInteger(1), string____add__))

def string____add__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    # always str
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__() + _args[2].__str__()))

# __toString__
def csB__string__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), string__toString__))

def string__toString__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[1] # return self







# =========== boolean|
# ===================|
def csB__boolean_proto(_env, _enherit):
    _csboolean = _env.vheap.cs__malloc(CSObject())
    # alter object type
    _csboolean.type = CSTypes.TYPE_CSBOOLEAN

    if  _enherit:
        for _k in _enherit.keys():
            _csboolean.put(_k, _enherit.get(_k))

    # proto attr
    _csboolean.put(CSTypes.TYPE_CSBOOLEAN     , csB__boolean__constructor(_env)) # default constructor
    _csboolean.put(PROTO_ATTR_NAME__toString__, csB__boolean__toString__ (_env)) # default __toString__
    # proto attr
    _env.scope[-1].insert(CSTypes.TYPE_CSBOOLEAN, _address=_csboolean.offset, _global=True)

    return _csboolean

# constructor
def csB__boolean__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSBOOLEAN), CSInteger(1), boolean__constructor))

def boolean__constructor(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(_args[2])

# __toString__
def csB__boolean__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), boolean__toString__))

def boolean__toString__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[1] # return self








# ========== nulltype|
# ===================|
def csB__nulltype_proto(_env, _enherit):
    _nulltype = _env.vheap.cs__malloc(CSObject())
    # alter object type
    _nulltype.type = CSTypes.TYPE_CSNULLTYPE

    if  _enherit:
        for _k in _enherit.keys():
            _nulltype.put(_k, _enherit.get(_k))

    # proto attr
    _nulltype.put(CSTypes.TYPE_CSNULLTYPE    , csB__nulltype__constructor(_env)) # default constructor
    _nulltype.put(PROTO_ATTR_NAME__toString__, csB__nulltype__toString__ (_env)) # default __toString__
    # proto attr
    _env.scope[-1].insert(CSTypes.TYPE_CSNULLTYPE, _address=_nulltype.offset, _global=True)

    return _nulltype

# constructor
def csB__nulltype__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSNULLTYPE), CSInteger(1), nulltype__constructor))

def nulltype__constructor(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(_args[2])

# __toString__
def csB__nulltype__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), nulltype__toString__))

def nulltype__toString__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))




# =========== nantype|
# ===================|
def csB__nantype_proto(_env, _enherit):
    _nantype = _env.vheap.cs__malloc(CSObject())
    # alter object type
    _nantype.type = CSTypes.TYPE_CSNANTYPE

    if  _enherit:
        for _k in _enherit.keys():
            _nantype.put(_k, _enherit.get(_k))

    # proto attr
    _nantype.put(CSTypes.TYPE_CSNANTYPE     , csB__nantype__constructor(_env)) # default constructor
    _nantype.put(PROTO_ATTR_NAME__toString__, csB__nantype__toString__ (_env)) # default __toString__
    # proto attr
    _env.scope[-1].insert(CSTypes.TYPE_CSNANTYPE, _address=_nantype.offset, _global=True)

    return _nantype

# constructor
def csB__nantype__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSNANTYPE), CSInteger(1), nantype__constructor))

def nantype__constructor(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(_args[2])

# __toString__
def csB__nantype__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), nantype__toString__))

def nantype__toString__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))









# === native function|
# ===================|
def csB__nativefunction_proto(_env, _enherit):
    _csnfunction = _env.vheap.cs__malloc(CSObject())
    # alter object type
    _csnfunction.type = CSTypes.TYPE_CSNATIVEFUNCTION

    if  _enherit:
        for _k in _enherit.keys():
            _csnfunction.put(_k, _enherit.get(_k))

    # proto attr
    _csnfunction.put(PROTO_ATTR_NAME__toString__, csB__nativefunction__toString__ (_env)) # default __toString__
    # proto attr
    _env.scope[-1].insert(CSTypes.TYPE_CSNATIVEFUNCTION, _address=_csnfunction.offset, _global=True)

    return _csnfunction

# constructor
# no default constructor

# __toString__
def csB__nativefunction__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), nativefunction__toString__))

def nativefunction__toString__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))










# ========== function|
# ===================|
def csB__function_proto(_env, _enherit):
    _csfunction = _env.vheap.cs__malloc(CSObject())
    # alter object type
    _csfunction.type = CSTypes.TYPE_CSFUNCTION

    if  _enherit:
        for _k in _enherit.keys():
            _csfunction.put(_k, _enherit.get(_k))

    # proto attr
    _csfunction.put(CSTypes.TYPE_CSFUNCTION    , csB__function__constructor(_env)) # default constructor
    _csfunction.put(PROTO_ATTR_NAME__toString__, csB__function__toString__ (_env)) # default __toString__
    # proto attr
    _env.scope[-1].insert(CSTypes.TYPE_CSFUNCTION, _address=_csfunction.offset, _global=True)

    return _csfunction

# constructor
def csB__function__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSFUNCTION), CSInteger(3), function__constructor))

def function__constructor(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(CSFunction(_args[2], _args[3], _args[4]))

# __toString__
def csB__function__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), function__toString__))

def function__toString__(_args:list):
    # args: [0]. _env, [1]. thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))
