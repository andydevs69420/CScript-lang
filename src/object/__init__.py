""" __init__.py initialize object modules

    author: andydevs69420
    github: http://github.com/andydevs69420/CScript-lang
"""
from .base.csobject import CSObject

# not so primitive thooooo, theyre all objects -_-
# for segregation purposess only!
from .primitive.csnumber import CSNumber
from .primitive.csinteger import CSInteger
from .primitive.csdouble import CSDouble
from .primitive.csboolean import CSBoolean
from .primitive.csnulltype import CSNullType

from .non_primitive.csarray import CSArray
from .non_primitive.csmap import CSMap
from .non_primitive.csstring import CSString


from .user_defined.csclass import CSClass
from .user_defined.cscallable import CSCallable