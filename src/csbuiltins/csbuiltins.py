

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

PROTO_NAME__constructor = "constructor"
PROTO_NAME__toString__  = "__toString__"


# PROTO is just an attr here. unlike JS

def csB__object_proto(_env):
    _csobject = _env.vheap.cs__malloc(CSObject())

    # proto
    _csobject.put(PROTO_NAME__constructor, csB__object__constructor(_env)) # default constructor
    _csobject.put(PROTO_NAME__toString__ , csB__object__toString__(_env))  # default __toString__

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
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_NAME__toString__), CSInteger(0), object__toString__))

def object__toString__(_args:list):
    # args: _env, thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))



# class
# ============= class|
# ===================|
def csB__class_proto(_env, _enherit=None):
    _csclass = _env.vheap.cs__malloc(CSObject())
    # alter object type
    _csclass.type = CSTypes.TYPE_CSDOUBLE

    if  _enherit:
        for _k in _enherit.keys():
            _csclass.put(_k, _enherit.get(_k))

    # proto
    _csclass.put(PROTO_NAME__constructor, csB__double__constructor(_env)) # default constructor
    _csclass.put(PROTO_NAME__toString__ , csB__double__toString__(_env))  # default __toString__

    # proto

    _env.scope[-1].insert(CSTypes.TYPE_CSDOUBLE, _address=_csclass.offset, _global=True)

    return _csclass

# constructor
def csB__class__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSDOUBLE), CSInteger(0), class__constructor))

def class__constructor(_args:list):
    # args: _env, thisArg, ...arguments
    # return type is null
    return

# __toString__
def csB__double__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_NAME__toString__), CSInteger(0), double__toString__))

def double__toString__(_args:list):
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

    # proto
    _csdouble.put(PROTO_NAME__constructor, csB__double__constructor(_env)) # default constructor
    _csdouble.put(PROTO_NAME__toString__ , csB__double__toString__(_env))  # default __toString__

    # proto

    _env.scope[-1].insert(CSTypes.TYPE_CSDOUBLE, _address=_csdouble.offset, _global=True)

    return _csdouble

# constructor
def csB__double__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSDOUBLE), CSInteger(1), double__constructor))

def double__constructor(_args:list):
    # args: _env, thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(CSDouble(_args[2].this)) # add cast(again)

# __toString__
def csB__double__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_NAME__toString__), CSInteger(0), double__toString__))

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

    # proto
    _csinteger.put(PROTO_NAME__constructor, csB__integer__constructor(_env)) # default constructor
    _csinteger.put(PROTO_NAME__toString__ , csB__integer__toString__(_env))  # default __toString__

    # proto
    _env.scope[-1].insert(CSTypes.TYPE_CSINTEGER, _address=_csinteger.offset, _global=True)

    return _csinteger

# constructor
def csB__integer__constructor(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(CSTypes.TYPE_CSINTEGER), CSInteger(1), integer__constructor))

def integer__constructor(_args:list):
    # args: _env, thisArg, ...arguments
    # return type is null
    return _args[0].vheap.cs__malloc(CSInteger(_args[2].this)) # add cast(again)

# __toString__
def csB__integer__toString__(_env):
    return _env.vheap.cs__malloc(CSNativeFunction(CSString(PROTO_NAME__toString__), CSInteger(0), integer__toString__))

def integer__toString__(_args:list):
    # args: _env, thisArg, ...arguments
    return _args[0].vheap.cs__malloc(CSString(_args[1].__str__()))








# ============ string|
# ===================|
def csB__string_proto(_env, _enherit):
    _env.scope[-1].insert()



