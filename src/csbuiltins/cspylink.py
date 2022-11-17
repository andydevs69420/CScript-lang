from builtins import type, getattr

from .cstypes import CSTypes
from .base.csobject import CSObject
from .csinteger import CSInteger
from .csdouble import CSDouble
from .csstring import CSString
from .csboolean import CSBoolean
from .csnulltype import CSNullType
from .csfunction import CSFunction
from .csnativefunction import CSNativeFunction


# utility
from utility import logger

class PyLinkInterface(object):
    """ PyLinkInterface

        Creates linkage for python3 class or module

        Attributes
        ----------
        linkname : str
        metadata : dict
        variable : dict

        Methods
        -------
        malloc -> CSObject
        link   -> CSObject
    """
    TYPEOF_KEYS =str
    TYPEOF_NAME =str
    TYPEOF_ARGC =int

    def __init__(self, _enherit=None):
        self.linkname = "__prototype__"
        self.metadata = ({})
        self.variable = ({})
    

    def getName(self, _env, _name:str):
        """ Gets name from scope

            Paramters
            --------
            _env : CSXEnvironment
            _name : str


            Returns
            -------
            CSObject
        """
        _info = _env.scope[-1].lookup(_name)
        return _env.vheap.cs__object_at(_info["_address"])

    def malloc(self, _env, _csobject):
        """ Allocates object before return,
                required to call.
            
            example:
            
            def some_method(self, _args:list) -> CSString:
                # args: [0]. _env, [1]. thisArg, [2~N]. ...arguments

                return self.malloc(_args[0], CSString("Hello World!"))

            Parameters
            ----------
            _env : CSXEnvironment

            Returns
            -------
            CSObject
        """
        return _env.vheap.cs__malloc(_csobject)

    def link(self, _args:list):
        """ Creates a linkage for python

            Parameters
            ----------
            _args : list (# args: [0]. _env, [1]. thisArg, [2~N]. ...arguments)

            Returns
            -------
            CSObject
        """
        # args: [0]. _env, [1]. thisArg, [2~N]. ...arguments

        if  not (isinstance(self.metadata, dict) and isinstance(self.variable, dict)):
            return self.malloc(_args[0], CSObject())

        _csobject = CSObject()
        _obj = self.malloc(_args[0], _csobject)
        _args[0].scope[-1].insert(self.linkname, _address=_obj.offset, _global=True)


        for _var_name, _value in zip(self.variable.keys(), self.variable.values()):

            if  type(_var_name) != PyLinkInterface.TYPEOF_KEYS:
                logger("PyLinkInterface::link", "skipping %s..." % _method_name.__str__())
                continue
            
            if  not isinstance(_value, CSObject):
                logger("PyLinkInterface::link", "skipping %s (invalid type)..." % _var_name)
                continue
            
            _csobject.put(
                _var_name,
                self.malloc(_args[0], _value)
            )


        for _method_name, _data in zip(self.metadata.keys(), self.metadata.values()):

            if  type(_method_name) != PyLinkInterface.TYPEOF_KEYS:
                logger("PyLinkInterface::link", "skipping %s..." % _method_name.__str__())
                continue
            
            if  not hasattr(self, _method_name):
                logger("PyLinkInterface::link", "skipping %s (No such method)..." % _method_name.__str__())
                continue

            # building ....
            _score = 0

            for each_k in _data.keys():
                if  type(each_k) == PyLinkInterface.TYPEOF_KEYS:
                    if  each_k == "name":
                        if  type(_data[each_k]) == PyLinkInterface.TYPEOF_NAME:
                            _score += 1
                    elif each_k == "argc":
                        if  type(_data[each_k]) == PyLinkInterface.TYPEOF_ARGC:
                            _score += 1
                    continue
                break
            
            if  _score != len(_data):
                logger("PyLinkInterface::link", "skipping %s insufficient method metadata..." % _method_name)
                continue

            if  _score == len(_data):
                
                _name = self.malloc(_args[0], CSString (_data["name"]))
                _argc = self.malloc(_args[0], CSInteger(_data["argc"]))

                _csobject.put(
                    _data["name"],
                    self.malloc(_args[0], CSNativeFunction(_name, _argc, getattr(self, _method_name)))
                )
        