

# .
from csbuiltins.csfunction import CSFunction
from .cstypes import CSTypes
from .base.csobject import CSObject
from .csinteger import CSInteger
from .csdouble import CSDouble
from .csstring import CSString
from .csnulltype import CSNullType
from .csnativefunction import CSNativeFunction


# utility
from utility import logger


PROTO_ATTR_NAME__toString__  = "__toString__"



# ============ object|
# ===================|
def csB__object_proto(_env):
    _csobject = _env.vheap.cs__malloc(CSObject())

    # proto attr
    _csobject.put(CSTypes.TYPE_CSOBJECT      , csB__object__constructor(_env)) # default constructor
    _csobject.put(PROTO_ATTR_NAME__toString__, csB__object__toString__ (_env)) # default __toString__

    _env.scope[-1].insert(CSTypes.TYPE_CSOBJECT, _address=_csobject.offset, _global=True)

    return _csobject

# constructor
def csB__object__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSOBJECT), CSInteger(0), object__constructor))

def object__constructor(_args:list):
    # args: _env, thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSObject())

# __toString__
def csB__object__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), object__toString__))

def object__toString__(_args:list):
    # args: _env, thisArg, ...arguments
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
    _csdouble.put(PROTO_ATTR_NAME__toString__, csB__double__toString__ (_env)) # default __toString__
    # proto attr

    _env.scope[-1].insert(CSTypes.TYPE_CSDOUBLE, _address=_csdouble.offset, _global=True)

    return _csdouble

# constructor
def csB__double__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSDOUBLE), CSInteger(1), double__constructor))

def double__constructor(_args:list):
    # args: _env, thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(_args[2])

# __toString__
def csB__double__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), double__toString__))

def double__toString__(_args:list):
    # args: _env, thisArg, ...arguments
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
    _csinteger.put(CSTypes.TYPE_CSINTEGER     , csB__integer__constructor(_env)) # default constructor
    _csinteger.put(PROTO_ATTR_NAME__toString__, csB__integer__toString__ (_env)) # default __toString__

    # proto attr
    _env.scope[-1].insert(CSTypes.TYPE_CSINTEGER, _address=_csinteger.offset, _global=True)

    return _csinteger

# constructor
def csB__integer__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSINTEGER), CSInteger(1), integer__constructor))

def integer__constructor(_args:list):
    # args: _env, thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(_args[2])

# __toString__
def csB__integer__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), integer__toString__))

def integer__toString__(_args:list):
    # args: _env, thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))








# ============ string|
# ===================|
def csB__string_proto(_env, _enherit):
    _csboolean = _env.vheap.cs__malloc(CSObject())
    # alter object type
    _csboolean.type = CSTypes.TYPE_CSSTRING

    if  _enherit:
        for _k in _enherit.keys():
            _csboolean.put(_k, _enherit.get(_k))

    # proto attr
    _csboolean.put(CSTypes.TYPE_CSSTRING      , csB__string__constructor(_env)) # default constructor
    _csboolean.put(PROTO_ATTR_NAME__toString__, csB__string__toString__ (_env)) # default __toString__

    # proto attr
    _env.scope[-1].insert(CSTypes.TYPE_CSSTRING, _address=_csboolean.offset, _global=True)

    return _csboolean

# constructor
def csB__string__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSSTRING), CSInteger(1), string__constructor))

def string__constructor(_args:list):
    # args: _env, thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(_args[2]) # add cast(again)

# __toString__
def csB__string__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), string__toString__))

def string__toString__(_args:list):
    # args: _env, thisArg, ...arguments
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
    # args: _env, thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(_args[2])

# __toString__
def csB__boolean__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), boolean__toString__))

def boolean__toString__(_args:list):
    # args: _env, thisArg, ...arguments
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
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSBOOLEAN), CSInteger(1), nulltype__constructor))

def nulltype__constructor(_args:list):
    # args: _env, thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(_args[2])

# __toString__
def csB__nulltype__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), nulltype__toString__))

def nulltype__toString__(_args:list):
    # args: _env, thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))








# ========== function|
# ===================|
def csB__function_proto(_env, _enherit):
    _csfunction = _env.vheap.cs__malloc(CSObject())
    # alter object type
    _csfunction.type = CSTypes.TYPE_CSNULLTYPE

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
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSBOOLEAN), CSInteger(3), function__constructor))

def function__constructor(_args:list):
    # args: _env, thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(CSFunction(_args[2], _args[3], _args[4]))

# __toString__
def csB__function__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_ATTR_NAME__toString__), CSInteger(0), function__toString__))

def function__toString__(_args:list):
    # args: _env, thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))
