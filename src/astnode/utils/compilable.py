
# ======= global|
# ==============|
from cstoken import CSToken
# ========== end|


# ======= object|
# ==============|
from base.csobject import CSObject
# ==============|



from cscriptvm.csOpcode import CSOpCode

__all__ = __ALL__ = ["Instruction", "Compilable"]

class Instruction(object):
    """ Holds cscript instruction|bytecode

        Parameters
        ----------
        _opcode : CSOpcode
        _kwargs : dict
    """

    def __init__(self, _offset:int, _opcode:CSOpCode, **_kwargs):
        self.offset = _offset
        self.opcode = _opcode
        self.kwargs = _kwargs
    
    def get(self, _key:str):
        return self.kwargs[_key]
    
    def __str__(self):
        _head = f"[{self.offset}] {self.opcode.name}"
        _args = ""
        for k,v in zip(self.kwargs.keys(), self.kwargs.values()):
            _args += f"{k} = {v.__str__()}"
            _args += ", "
        if _args.endswith(", "): _args = _args[0:-2]

        if len(_args) > 0:
            _head += " : "

        return _head + _args


class Compilable(object):
    
    def __init__(self):
        self.__instructions:list[Instruction] = []

    def getInsntructions(self):
        return self.__instructions
    
    def peekLast(self):
        return self.__instructions[-1]
    
    
    def getLine(self):
        return len(self.__instructions) * 2

    def load_module(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.LOAD_MODULE,
            )
        )
    
    def push_name(self, _name:CSToken, _offset:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_NAME, name=_name, offset=_offset
            )
        )
    
    
    def push_local(self, _name:CSToken, _offset:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_LOCAL, name=_name, offset=_offset
            )
        )

    
    def push_constant(self, _csobject:CSObject):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_CONST, obj=_csobject
            )
        )
    
    
    def make_array(self, _size:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.MAKE_ARRAY, size=_size
            )
        )
    
    
    def make_object(self, _size:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.MAKE_OBJECT, size=_size
            )
        )
    
    
    def make_class(self, _size:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.MAKE_CLASS, size=_size
            )
        )
    
    
    def make_module(self, _size:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.MAKE_MODULE, size=_size
            )
        )
    
    
    def get_attrib(self, _attrib:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.GET_ATTRIB, attr=_attrib
            )
        )
    
    def load_attrib(self, _attrib:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.LOAD_ATTRIB, attr=_attrib
            )
        )

    
    def set_attrib(self, _attrib:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.SET_ATTRIB, attr=_attrib
            )
        )
    
    
    def store_name(self, _name:CSToken, _offset:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.STORE_NAME, name=_name, offset=_offset
            )
        )
    
    
    def store_local(self, _name:CSToken, _offset:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.STORE_LOCAL, name=_name, offset=_offset
            )
        )
    
    
    def call(self, _location:CSToken, _size:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.CALL, location=_location, size=_size
            )
        )
    
    
    def unary_op(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.UNARY_OP, opt=_operator
            )
        )

    
    def binary_pow(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_POW, opt=_operator
            )
        )

    
    def binary_mul(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_MUL, opt=_operator
            )
        )
    
    
    def binary_div(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_DIV, opt=_operator
            )
        )
    
    
    def binary_mod(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_MOD, opt=_operator
            )
        )

    
    def binary_add(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_ADD, opt=_operator
            )
        )
    
    
    def binary_sub(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_SUB, opt=_operator
            )
        )

    
    def binary_lshift(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_LSHIFT, opt=_operator
            )
        )

    
    def binary_rshift(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_RSHIFT, opt=_operator
            )
        )
    
    
    def binary_and(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_AND, opt=_operator
            )
        )

    
    def binary_xor(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_XOR, opt=_operator
            )
        )
    
    
    def binary_or(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_OR, opt=_operator
            )
        )
    
    
    def binary_subscript(self, _subscript_location:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_SUBSCRIPT, location=_subscript_location
            )
        )
    
    
    def set_subscript(self, _subscript_location:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.SET_SUBSCRIPT, location=_subscript_location
            )
        )
    
    
    def compare_op(self, _operator:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.COMPARE_OP, opt=_operator
            )
        )
    
    
    def inplace_pow(self, _opt:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_POW, opt=_opt
            )
        )

    
    def inplace_mul(self, _opt:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_MUL, opt=_opt
            )
        )
    
    
    def inplace_div(self, _opt:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_DIV, opt=_opt
            )
        )
    
    
    def inplace_mod(self, _opt:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_MOD, opt=_opt
            )
        )
    
    
    def inplace_add(self, _opt:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_ADD, opt=_opt
            )
        )
    
    
    def inplace_sub(self, _opt:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_SUB, opt=_opt
            )
        )
    
    
    def inplace_lshift(self, _opt:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_LSHIFT, opt=_opt
            )
        )
    
    
    def inplace_rshift(self, _opt:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_RSHIFT, opt=_opt
            )
        )
    
    
    def inplace_and(self, _opt:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_AND, opt=_opt
            )
        )
    
    
    def inplace_xor(self, _opt:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_XOR, opt=_opt
            )
        )
    
    
    def inplace_or(self, _opt:CSToken):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_OR, opt=_opt
            )
        )

    
    def pop_jump_if_false(self, _target:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.POP_JUMP_IF_FALSE, target=_target
            )
        )

    
    def pop_jump_if_true(self, _target:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.POP_JUMP_IF_TRUE, target=_target
            )
        )
    
    
    def jump_if_false_or_pop(self, _target:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.JUMP_IF_FALSE_OR_POP, target=_target
            )
        )
    
    
    def jump_if_true_or_pop(self, _target:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.JUMP_IF_TRUE_OR_POP, target=_target
            )
        )
    
    
    
    def jump_equal(self, _target:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.JUMP_EQUAL, target=_target
            )
        )
    
    
    def jump_to(self, _target:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.JUMP_TO, target=_target
            )
        )
    
    # deprecated! 
    
    def jump_not_equal(self, _target:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.JUMP_NOT_EQUAL, target=_target
            )
        )
    
    
    def absolute_jump(self, _target:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.ABSOLUTE_JUMP, target=_target
            )
        )
    
    
    def setup_try(self, _target:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.SETUP_TRY, target=_target
            )
        )

    
    def pop_try(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.POP_TRY
            )
        )
    
    
    def print_object(self, _size:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PRINT_OBJECT, size=_size
            )
        )
    
    
    def no_operation(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.NO_OPERATION
            )
        )

    
    def pop_top(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.POP_TOP
            )
        )
    
    
    def return_op(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.RETURN_OP
            )
        )