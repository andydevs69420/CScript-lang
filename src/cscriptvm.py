

from compiler import Instruction
from compiler import CSOpCode

from linkage import __ALL__ as ln

# builtins
from csbuiltins import CSTypes
from csbuiltins import CSObject
from csbuiltins import csrawcode
from csbuiltins import CSInteger
from csbuiltins import CSDouble
from csbuiltins import CSString
from csbuiltins import CSBoolean
from csbuiltins import CSMethod
from csbuiltins.csnativefunction import CSNativeFunction
from csbuiltins.csnulltype import CSNullType
from csbuiltins.csfunction import CSFunction

# utility
from utility import __throw__
from utility import logger

class CSXEnvironment(object):
    """ environment while running
    """
    def __init__(self):
        self.scope = [Scope()] # scope 0 is the global scope
        self.stack = STACK()
        self.vheap = CSXMemory(self)
        


class STACK(object):

    def __init__(self):
        self.__internal = [
        ]
    
    def push(self, _any:CSObject):
        self.__internal.append(_any)

    def pop(self):
        return self.__internal.pop()
    
    def top(self):
        return self.__internal[-1]
    
    def all(self):
        return self.__internal


class CSXMemory(object):
    """ Serves as heap memory
    """

    def __init__(self, _env:CSXEnvironment):
        self.__bucket = []
        # unused index
        self.__unused = []
        self.__scopes = _env.scope
    
    def cs__malloc(self, _csobject:CSObject):
        # for singleton objects!!
        assert _csobject.offset == -69420, "double allocation!"

        if  len(self.__unused) > 0:
            _csobject.offset = self.__unused[-1]
            self.__bucket[self.__unused[-1]] = _csobject
            return self.__bucket[self.__unused.pop()]
        
        # creates new slot
        _csobject.offset = len(self.__bucket)
        self.__bucket.append(_csobject)
        return self.__bucket[-1]
    
    def cs__object_at(self, _address_offset_index:int):
        return self.__bucket[_address_offset_index]

    def gmark__phase(self):
        ...
    
    def sweep__phase(self):
        ...

    def collect(self):
        self.gmark__phase()
        self.sweep__phase()


class Scope(object):
    """ Acts as symbol table

        Parameters
        ----------
        _parent(optional) : Scope|None
    """

    def __init__(self, _parent=None):
        self.parent  = _parent
        self.symbols = ({
            # var_name: int->offset of object
        })
    
    def insert(self, _symbol:str, **_props):
        self.symbols[_symbol] = _props
    
    def update(self, _symbol:str, **_props):
        assert self.exists(_symbol, False), "null possibility not handled!"
        self.symbols[_symbol].update(_props)
    
    def lookup(self, _symbol:str):
        assert self.exists(_symbol, False), "null possibility not handled!"
        if  (_symbol in self.symbols.keys()):
            return self.symbols[_symbol]
        
        # until parent is none
        _parent = self.parent
        while _parent:
            if  _parent.exists(_symbol, _local=True):
                return _parent.lookup(_symbol)
            _parent = _parent.parent
        
        raise Exception("unhandled!!!")
    
    def exists(self, _symbol:str, _local:bool=True):
        if  (_symbol in self.symbols.keys()):
            return True
        
        if _local: return False

        # search while parent is None
        _node = self.parent
        while _node:
            if  _node.exists(_symbol):
                return True
            _node = _node.parent
        
        return False


""" Begin runtime functions
"""


def cs__error(_env:CSXEnvironment, _message:str, _location:str):
    """ ThrowsError or flush to try/except

        Parameters
        ----------
        _env : CSXEnvironment
        _message : str
        _location : str
    """
    return __throw__(
        _message
        + "\n"
        + _location
    )

def cs_format_name_error_0(_env:CSXEnvironment, _name:str):
    """ Formats name error message if not defined!

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        str
    """
    return "NameError: name '%s' is not defined in scope !!!" % _name


def cs_format_name_error_1(_env:CSXEnvironment, _name:str):
    """ Formats name error message if defined!

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        str
    """
    return "NameError: name '%s' was already defined in scope !!!" % _name


def cs_format_att_error(_env:CSXEnvironment, _obj:CSObject, _attribute:str):
    """ Formats attribute error message

        Parameters
        ----------
        _env : CSXEnvironment
        _func : CSObject
        _attribute : str

        Returns
        -------
        str
    """
    return "AttributeError: missing attribute %s::%s !!!" % (_obj.type, _attribute)


def cs_format_method_error(_env:CSXEnvironment, _obj:CSObject, _attribute:str):
    """ Formats attribute error message

        Parameters
        ----------
        _env : CSXEnvironment
        _func : CSObject
        _attribute : str

        Returns
        -------
        str
    """
    return "AttributeError: missing method %s::%s !!!" % (_obj.type, _attribute)

def cs_format_arg_error(_env:CSXEnvironment, _func:CSObject, _arg_size:int):
    """ Formats argument error message

        Parameters
        ----------
        _env : CSXEnvironment
        _func : CSObject
        _arg_size : int

        Returns
        -------
        str
    """
    _fname = _func.get("name").__str__()
    _fargc = _func.get("argc").__str__()
    return "ArgumentError: %s expected arg count %s, got %d !!!" % (_fname, _fargc, _arg_size)


def cs_format_post_type_error(_env:CSXEnvironment, _opt:str, _lhs:CSObject):
    """ Formats type error message for postfix expression

        Parameters
        ----------
        _env : CSXEnvironment
        _opt : str
        _lhs : CSObject

        Returns
        -------
        str
    """
    return "TypeError: invalid postfix operator (%s) for type %s !!!" % (_opt, _lhs.type)

def cs_format_una_type_error(_env:CSXEnvironment, _opt:str, _rhs:CSObject):
    """ Formats type error message for unary expression

        Parameters
        ----------
        _env : CSXEnvironment
        _opt : str
        _rhs : CSObject

        Returns
        -------
        str
    """
    return "TypeError: invalid unary operator (%s) for type %s !!!" % (_opt, _rhs.type)


def cs_format_bin_type_error(_env:CSXEnvironment, _opt:str, _lhs:CSObject, _rhs:CSObject):
    """ Formats type error message for binary expression

        Parameters
        ----------
        _env : CSXEnvironment
        _opt : str
        _lhs : CSObject
        _rhs : CSObject

        Returns
        -------
        str
    """
    return "TypeError: invalid operator (%s) for operands type %s and %s !!!" % (_opt, _lhs.type, _rhs.type)


def cs_format_zero_division_error(_env:CSXEnvironment, _opt:str, _lhs:CSObject, _rhs:CSObject):
    """ Formats type error message for zero division

        Parameters
        ----------
        _env : CSXEnvironment
        _opt : str
        _lhs : CSObject
        _rhs : CSObject

        Returns
        -------
        str
    """
    return "ZeroDivisionError: divisor of dividend produces zero !!!"



def cs__call(_env:CSXEnvironment, _code:csrawcode):
    ...

    _ipointer = 0

    for i in _code:
        print(i)

    while _ipointer < len(_code):

        _opc = _code.code[_ipointer]
        _ipointer += 1

        match _opc.opcode:

            case CSOpCode.PUSH_CODE:
                """"""
                cs_new_code(_env, _opc.get("code"))

            case CSOpCode.PUSH_INTEGER:
                """"""
                cs_new_number(_env, _opc.get("const"))

            case CSOpCode.PUSH_DOUBLE:
                """"""
                cs_new_number(_env, _opc.get("const"))
            
            case CSOpCode.PUSH_STRING:
                """"""
                cs_new_string(_env, _opc.get("const"))
            
            case CSOpCode.PUSH_BOOLEAN:
                """"""
                cs_new_boolean(_env, _opc.get("const"))
            
            case CSOpCode.PUSH_NULL:
                """"""
                cs_new_nulltype(_env)

            case CSOpCode.PUSH_NAME:
                """"""
                if  not cs_has_name(_env, _opc.get("name")):
                    cs__error(_env, cs_format_name_error_0(_env, _opc.get("name")), _opc.get("loc"))
                    continue
                    
                #####
                cs_push_name(_env, _opc.get("name"))
            

            case CSOpCode.GET_ATTRIB:
                """"""
                if  not cs_has_attribute(_env, _env.stack.top(), _opc.get("attr")):
                    cs__error(_env, cs_format_att_error(_env, _env.stack.top(), _opc.get("attr")), _opc.get("loc"))
                    continue

                #####
                cs_get_attrib(_env, _opc.get("attr"))
            
            case CSOpCode.GET_METHOD:
                """"""
                if  not cs_has_method(_env, _env.stack.top(), _opc.get("attr")):
                    cs__error(_env, cs_format_method_error(_env, _env.stack.top(), _opc.get("attr")), _opc.get("loc"))
                    continue

                #####
                cs_get_method(_env, _opc.get("attr"))
            
            case CSOpCode.CALL_METHOD:
                """"""
                if  _env.stack.top().get("argc").this != _opc.get("size") +1:
                    cs__error(_env, cs_format_arg_error(_env, _env.stack.top(), _opc.get("size") +1), _opc.get("loc"))
                    continue
                    
                #####
                cs_method_call(_env, _opc.get("size") +1)
            


            case CSOpCode.CALL:
                """"""
                if  _env.stack.top().get("argc").this != _opc.get("size"):
                    cs__error(_env, cs_format_arg_error(_env, _env.stack.top(), _opc.get("size")), _opc.get("loc"))
                    continue
                    
                #####
                cs_function_call(_env, _opc.get("size"))
            

            case CSOpCode.POSTFIX_OP:

                match _opc.get("opt"):

                    case "++":
                        _top = _env.stack.pop()

                        if  not cs_is_number(_top):
                            cs__error(_env, cs_format_post_type_error(_env, _opc.get("opt"), _top), _opc.get("loc"))
                            continue
                    
                        #####
                        # push old
                        cs_new_number(_env, _top.this)

                        # inc
                        _top.this += 1

                    case "--":
                        _top = _env.stack.pop()

                        if  not cs_is_number(_top):
                            cs__error(_env, cs_format_post_type_error(_env, _opc.get("opt"), _top), _opc.get("loc"))
                            continue
                    
                        #####
                        # push old
                        cs_new_number(_env, _top.this)

                        # dec
                        _top.this -= 1


            case CSOpCode.UNARY_OP:

                match _opc.get("opt"):

                    case "new":
                        raise NotImplementedError("Not implemented class builder!!")

                    case "!":
                        _rhs = _env.stack.pop()

                        #####
                        cs_new_boolean(_env, not _rhs.this)

                    case "~":
                        _rhs = _env.stack.pop()

                        if  not cs_is_integer(_rhs):
                            cs__error(_env, cs_format_una_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                            continue

                        #####
                        cs_new_number(_env, ~ _rhs.this)
                    

                    case "+":
                        _rhs = _env.stack.pop()

                        if  not cs_is_number(_rhs):
                            cs__error(_env, cs_format_una_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                            continue

                        #####
                        cs_new_number(_env, + _rhs.this)
                    

                    case "-":
                        _rhs = _env.stack.pop()

                        if  not cs_is_number(_rhs):
                            cs__error(_env, cs_format_una_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                            continue

                        #####
                        cs_new_number(_env, - _rhs.this)
                    

                    case "++":
                        _rhs = _env.stack.top()

                        if  not cs_is_number(_rhs):
                            cs__error(_env, cs_format_una_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                            continue

                        #####
                        _rhs.this += 1
                    
                    case "--":
                        _rhs = _env.stack.top()

                        if  not cs_is_number(_rhs):
                            cs__error(_env, cs_format_una_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                            continue

                        #####
                        _rhs.this -= 1


            case CSOpCode.BINARY_POW:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not cs_is_number(_lhs) and cs_is_number(_rhs):
                    cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue

                #####
                cs_new_number(_env, _lhs.this ** _rhs.this)
            

            case CSOpCode.BINARY_MUL:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not cs_is_number(_lhs) and cs_is_number(_rhs):
                    cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue

                #####
                cs_new_number(_env, _lhs.this * _rhs.this)
            

            case CSOpCode.BINARY_DIV:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not cs_is_number(_lhs) and cs_is_number(_rhs):
                    cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue

                # zero divisor
                if  _rhs.this == 0:
                    cs__error(_env, cs_format_zero_division_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue

                #####
                cs_new_number(_env, _lhs.this / _rhs.this)
            

            case CSOpCode.BINARY_MOD:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not cs_is_number(_lhs) and cs_is_number(_rhs):
                    cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue

                # zero divisor
                if  _rhs.this == 0:
                    cs__error(_env, cs_format_zero_division_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue

                #####
                cs_new_number(_env, _lhs.this % _rhs.this)


            case CSOpCode.BINARY_ADD:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()
              
                if  not ((cs_is_number(_lhs) and cs_is_number(_rhs)) or \
                         (cs_is_string(_lhs) and cs_is_string(_rhs))):
                    cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue
                
                #####
                if cs_is_number(_lhs) and cs_is_number(_rhs):
                    cs_new_number(_env, _lhs.this + _rhs.this)
                else:
                    cs_new_string(_env, _lhs.this + _rhs.this)
            

            case CSOpCode.BINARY_SUB:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not cs_is_number(_lhs) and cs_is_number(_rhs):
                    cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue

                #####
                cs_new_number(_env, _lhs.this - _rhs.this)
            
            case CSOpCode.BINARY_LSHIFT:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not cs_is_integer(_lhs) and cs_is_integer(_rhs):
                    cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue

                #####
                cs_new_number(_env, _lhs.this << _rhs.this)
            

            case CSOpCode.BINARY_RSHIFT:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not cs_is_integer(_lhs) and cs_is_integer(_rhs):
                    cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue

                #####
                cs_new_number(_env, _lhs.this >> _rhs.this)
            
            case CSOpCode.COMPARE_OP:
                match _opc.get("opt"):

                    case "<":
                        _lhs = _env.stack.pop()
                        _rhs = _env.stack.pop()

                        if  not cs_is_number(_lhs) and cs_is_number(_rhs):
                            cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                            continue

                        #####
                        cs_new_boolean(_env, _lhs.this < _rhs.this)
                    
                    case "<=":
                        _lhs = _env.stack.pop()
                        _rhs = _env.stack.pop()

                        if  not cs_is_number(_lhs) and cs_is_number(_rhs):
                            cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                            continue

                        #####
                        cs_new_boolean(_env, _lhs.this <= _rhs.this)
                    

                    case ">":
                        _lhs = _env.stack.pop()
                        _rhs = _env.stack.pop()

                        if  not cs_is_number(_lhs) and cs_is_number(_rhs):
                            cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                            continue

                        #####
                        cs_new_boolean(_env, _lhs.this > _rhs.this)
                    
                    case ">=":
                        _lhs = _env.stack.pop()
                        _rhs = _env.stack.pop()

                        if  not cs_is_number(_lhs) and cs_is_number(_rhs):
                            cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                            continue

                        #####
                        cs_new_boolean(_env, _lhs.this >= _rhs.this)
                    
                    case "==":
                        _lhs = _env.stack.pop()
                        _rhs = _env.stack.pop()

                        if  not (cs_is_pointer(_lhs) and cs_is_pointer(_rhs)):
                            cs_new_boolean(_env, _lhs.this == _rhs.this)
                            continue
                      
                        ##### pointer: compare memory address
                        cs_new_boolean(_env, _lhs.offset == _rhs.offset)
                    

                    case "!=":
                        _lhs = _env.stack.pop()
                        _rhs = _env.stack.pop()

                        if  not (cs_is_pointer(_lhs) and cs_is_pointer(_rhs)):
                            cs_new_boolean(_env, _lhs.this != _rhs.this)
                            continue
                      
                        ##### pointer: compare memory address
                        cs_new_boolean(_env, _lhs.offset != _rhs.offset)
                    

            case CSOpCode.BINARY_AND:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                    cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue
                
                #####
                cs_new_number(_env, _lhs.this & _rhs.this)
            

            case CSOpCode.BINARY_XOR:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                    cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue
                
                #####
                cs_new_number(_env, _lhs.this ^ _rhs.this)
            

            case CSOpCode.BINARY_OR:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                    cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                    continue
                
                #####
                cs_new_number(_env, _lhs.this | _rhs.this)


            case CSOpCode.MAKE_FUNCTION:
                """"""
                cs_new_function(_env)

            case CSOpCode.MAKE_VAR:
                """"""
                if  cs_has_name(_env, _opc.get("name")):
                    cs__error(_env, cs_format_name_error_1(_env, _opc.get("name")), _opc.get("loc"))
                    continue

                #####
                cs_make_var(_env, _opc.get("name"))
            
            case CSOpCode.MAKE_LOCAL:
                """"""
                if  cs_has_local(_env, _opc.get("name")):
                    cs__error(_env, cs_format_name_error_1(_env, _opc.get("name")), _opc.get("loc"))
                    continue

                #####
                cs_make_local(_env, _opc.get("name"))
            
            case CSOpCode.POP_TOP:
                """"""
                _env.stack.pop()
            
            case CSOpCode.PRINT_OBJECT:
                """"""
                _size = _opc.get("size")
                _frmt = ""

                for _r in range(_size):
                    _frmt += _env.stack.pop().__str__()

                    if  _r < (_size - 1):
                        _frmt += " "
                
                print(_frmt)
            
            case CSOpCode.RETURN_OP:
                return

            case _:
                print("Not implemented", _opc.opcode.name)
                exit(1)



"""HELPERS"""

def cs_has_name(_env:CSXEnvironment, _name:str):
    """ Checks if name exists to scope

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        bool
    """
    return _env.scope[-1].exists(_name, _local=False)


def cs_has_local(_env:CSXEnvironment, _name:str):
    """ Checks if name exists to local scope

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        bool
    """
    return _env.scope[-1].exists(_name, _local=True)


def cs_has_class(_env:CSXEnvironment, _class_name:str):
    """ Checks if class exist

        Parameters
        ----------
        _env : CSXEnvironment
        _class_name : str

        Returns
        -------
        bool
    """
    _exist = _env.scope[-1].exists(_class_name, _local=False)
    if not _exist: return _exist

    _infor = _env.scope[-1].lookup(_class_name)
    # check if valid class
   
    _class = _env.vheap.cs__object_at(_infor["_address"])
    
    # check if has constructor
    # constructor must named to itself
    if  not _class.hasKey(_class_name):
        return False
    
    # check if callable
    return cs_is_callable(_env, _class.get(_class_name))




def cs_has_method(_env:CSXEnvironment, _obj:CSObject, _method_name:str):
    """ Checks if _obj has _method_name to its class proto

        Parameters
        ----------
        _env : CSXEnvironment
        _obj : CSObject
        _method_name : str

        Returns
        -------
        bool
    """
    if  not cs_has_class(_env, _obj.type): 
        return False

    # search in class
    _infor = _env.scope[-1].lookup(_obj.type)
    _class = _env.vheap.cs__object_at(_infor["_address"])

    if  not cs_has_attribute(_env, _class, _method_name):
        return False

    return cs_is_callable(_env, _class.get(_method_name))



def cs_has_attribute(_env:CSXEnvironment, _obj:CSObject, _attribute_name:str):
    """ Check if object has direct attribute/key

        Parameters
        ----------
        _env : CSXEnvironment
        _obj : CSObject
        _method_name : str

        Returns
        -------
        bool
    """
    return _obj.hasKey(_attribute_name)


def cs_is_callable(_env:CSXEnvironment, _obj:CSObject):
    """ Checks if object is a function

        Parameters
        ----------
        _env : CSXEnvironment
        _obj : CSObject

        Returns
        -------
        bool
    """ 
    return (
        _obj.type == CSTypes.TYPE_CSNATIVEFUNCTION or
        _obj.type == CSTypes.TYPE_CSFUNCTION       or
        _obj.type == CSTypes.TYPE_CSMETHOD
    )


def cs_is_rawcode(_csobject:CSObject):
    """ Checks if object is csrawcode

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return  _csobject.type == CSTypes.TYPE_CSRAWCODE



def cs_is_number(_csobject:CSObject):
    """ Checks if object is CSInteger or CSDouble

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return  cs_is_integer(_csobject) or cs_is_double(_csobject)


def cs_is_integer(_csobject:CSObject):
    """ Checks if object is CSInteger

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return _csobject.type == CSTypes.TYPE_CSINTEGER


def cs_is_double(_csobject:CSObject):
    """ Checks if object is CSDouble

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return _csobject.type == CSTypes.TYPE_CSDOUBLE


def cs_is_string(_csobject:CSObject):
    """ Checks if object is CSString

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return  _csobject.type == CSTypes.TYPE_CSSTRING


def cs_is_boolean(_csobject:CSObject):
    """ Checks if object is CSBoolean

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return  _csobject.type == CSTypes.TYPE_CSBOOLEAN



def cs_is_nulltype(_csobject:CSObject):
    """ Checks if object is CSNullType

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return  _csobject.type == CSTypes.TYPE_CSNULLTYPE


def cs_is_pointer(_csobject:CSObject):
    """ Checks if object is a pointer type

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return not (cs_is_number(_csobject) or cs_is_string(_csobject) or cs_is_boolean(_csobject) or cs_is_nulltype(_csobject))


"""OPCODE METHODS"""

def cs_make_var(_env:CSXEnvironment, _name:str):
    """ Creates global variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert not cs_has_name(_env, _name), "name '%s' already defined!" % _name

    # save var
    _env.scope[-1].insert(_name, _address=_env.stack.pop().offset, _global=True)


def cs_make_local(_env:CSXEnvironment, _name:str):
    """ Creates local variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert not cs_has_local(_env, _name), "name '%s' already defined!" % _name

    # save var
    _env.scope[-1].insert(_name, _address=_env.stack.pop().offset, _global=False)


def cs_new_code(_env:CSXEnvironment, _raw_code:csrawcode):
    """ Push number to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _raw_code : csrawcode
    """ 
    _env.stack.push(_env.vheap.cs__malloc(_raw_code))


def cs_new_number(_env:CSXEnvironment, _py_number:int|float):
    """ Push number to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _py_number : int|float
    """ 
    _obj = None
    if  type(_py_number) == int:
        _obj = _env.vheap.cs__malloc(CSInteger(_py_number))

    else:
        _obj = _env.vheap.cs__malloc(CSDouble (_py_number))

    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put("__proto__", _env.stack.pop())

    # push #
    _env.stack.push(_obj)


def cs_new_string(_env:CSXEnvironment, _py_string:str):
    """ Push string to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _py_string : str
    """ 

    _obj = CSString(_py_string)

    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put("__proto__", _env.stack.pop())

    _env.stack.push(_env.vheap.cs__malloc(_obj))


def cs_new_boolean(_env:CSXEnvironment, _py_boolean:bool):
    """ Push boolean to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _py_boolean : bool
    """ 

    _obj = CSBoolean(_py_boolean)

    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put("__proto__", _env.stack.pop())

    _env.stack.push(_env.vheap.cs__malloc(_obj))



def cs_new_nulltype(_env:CSXEnvironment):
    """ Push boolean to stack

        Parameters
        ----------
        _env : CSXEnvironment
    """ 

    _obj = CSNullType()

    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put("__proto__", _env.stack.pop())

    _env.stack.push(_env.vheap.cs__malloc(_obj))


def cs_new_function(_env:CSXEnvironment):
    """ Push/Builds a function

        Parameters
        ----------
        _env : CSXEnvironment
    """
    _fname = _env.stack.pop()
    _fargc = _env.stack.pop()
    _fcode = _env.stack.pop()

    _obj = CSFunction(_fname, _fargc, _fcode)
    
    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put("__proto__", _env.stack.pop())


    _env.stack.push(_env.vheap.cs__malloc(_obj))

def cs_push_name(_env:CSXEnvironment, _name:str):
    """ Gets variable value

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert cs_has_name(_env, _name), "no such name '%s'" % _name

    # retrieve
    _info = _env.scope[-1].lookup(_name)
    
    # push stack
    _env.stack.push(_env.vheap.cs__object_at(_info["_address"]))


def cs_get_class(_env:CSXEnvironment, _class_name:str):
    """ Retrievs class prototype

        Parameters
        ----------
        _env : CSXEnvironment
        _class_name : str
    """
    assert cs_has_class(_env, _class_name), "No such class" % _class_name

    # retrieve
    _info = _env.scope[-1].lookup(_class_name)
    
    # push stack
    _env.stack.push(_env.vheap.cs__object_at(_info["_address"]))


def cs_get_attrib(_env:CSXEnvironment, _attribute_name:str):
    """ Gets attribute of an object

        Parameters
        ----------
        _env : CSXEnvironment
        _attribute_name : str
    """
    assert cs_has_attribute(_env, _env.stack.top(), _attribute_name), "No such attribute '%s'" % _attribute_name

    _top = _env.stack.pop()

    # push to stack
    _env.stack.push(_top.get(_attribute_name))



def cs_get_method(_env:CSXEnvironment, _method_name:str):
    """ Extracts method from class prototype

        Parameters
        ----------
        _env : CSXEnvironment
        _method_name : str
        
    """
    assert cs_has_method(_env, _env.stack.top(), _method_name), "No such method '%s'" % _method_name

    # top object
    _objct = _env.stack.pop()
   
    # get class
    _infor = _env.scope[-1]\
        .lookup(_objct.type)

    _class = _env\
        .vheap\
        .cs__object_at(_infor["_address"])

    # push to stack
    _env.stack.push(_env.vheap.cs__malloc(CSMethod(_objct, _class.get(_method_name))))


"""FUNCTIONS"""
def cs_method_call(_env:CSXEnvironment, _argument_size:int):
    """ Calls a method

        Parameters
        ----------
        _env : CSXEnvironment
        _argument_size : int
    """
    #   stack
    # ---------
    #  method
    #  args 0
    #  args N

    # new scope
    _env.scope.append(Scope(_env.scope[-1]))

    assert cs_is_callable(_env, _env.stack.top()), "not a function!"

    # method
    _func = _env.stack.pop()

    # push_owner
    _env.stack.push(_func.get("owner"))

    match _func.meth:
        case CSTypes.TYPE_CSNATIVEFUNCTION:
            # call function
            _args = [_env]

            for _r in range(_argument_size):
                _args.append(_env.stack.pop())

            _env.stack.push(_func.call(_args))

        case CSTypes.TYPE_CSFUNCTION:
            # call function
            cs__call(_env, _func.get("code"))

    # end scope
    _env.scope.pop()


def cs_function_call(_env:CSXEnvironment, _argument_size:int):
    """ Calls a function

        Parameters
        ----------
        _env : CSXEnvironment
        _argument_size : int
    """
    #   stack
    # ---------
    #  method
    #  args 0
    #  args N

    # new scope
    _env.scope.append(Scope(_env.scope[-1]))

    assert cs_is_callable(_env, _env.stack.top()), "not a function!"

    # method
    _func = _env.stack.pop()

    match _func.type:
        case CSTypes.TYPE_CSNATIVEFUNCTION:
            # call function
            _args = [_env]

            for _r in range(_argument_size):
                _args.append(_env.stack.pop())

            _env.stack.push(_func.call(_args))

        case CSTypes.TYPE_CSFUNCTION:
            # call function
            cs__call(_env, _func.get("code"))

    # end scope
    _env.scope.pop()



def cs__init_builtin(_env:CSXEnvironment):
    """ Initialize builtins

        Parameters
        ----------
        _env : CSXEnvironment
    """ 
    # linkage
    for each_class in ln:\
    each_class().link([_env])



def cs__run(_code:csrawcode):
    _env = CSXEnvironment()

    # initialize before run
    cs__init_builtin(_env)

    # call module
    cs__call(_env, _code)




