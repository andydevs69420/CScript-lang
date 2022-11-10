

# .
from .csopcode import CSOpCode



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
        self.hidden = _kwargs["__hidden__"] if "__hidden__" in _kwargs.keys() else []
    
    def get(self, _key:str):
        return self.kwargs[_key]
    
    def __str__(self):
        _head = f"[{self.offset}] {self.opcode.name}"
        _args = ""
        for k,v in zip(self.kwargs.keys(), self.kwargs.values()):

            if  k != "__hidden__" and k not in self.hidden:
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
                CSOpCode.LOAD_MODULE
            )
        )
    
    def push_integer(self, _const:int):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_INTEGER, const=_const
            )
        )
    
    def push_double(self, _const:float):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_DOUBLE, const=_const
            )
        )
    
    def push_string(self, _const:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_STRING, const=_const
            )
        )
    
    def push_boolean(self, _const:bool):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_BOOLEAN, const=_const
            )
        )
    
    def push_null(self, _const:None):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_NULL, const=_const
            )
        )
    
    def this_op(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.THIS_OP
            )
        )
    
    def push_object(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_OBJECT, content="{}"
            )
        )
    
    def push_code(self, _raw_code):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_CODE, code=_raw_code
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
    
    def make_function(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.MAKE_FUNCTION
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

    def push_name(self, _name:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_NAME, name=_name, loc=_loc, __hidden__=["loc"]
            )
        )
    
    
    def push_local(self, _name:str, _offset:int):
        """ Deprecated
        """
        raise RuntimeError("use of deprecated methods")
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.PUSH_LOCAL, name=_name, offset=_offset
            )
        )
    
    
    def get_attrib(self, _attrib:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.GET_ATTRIB, attr=_attrib, loc=_loc, __hidden__=["loc"]
            )
        )
    
    def get_method(self, _attrib:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.GET_METHOD, attr=_attrib, loc=_loc, __hidden__=["loc"]
            )
        )

    
    def set_attrib(self, _attrib:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.SET_ATTRIB, attr=_attrib, loc=_loc, __hidden__=["loc"]
            )
        )
    
    def make_var(self, _name:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.MAKE_VAR, name=_name, loc=_loc, __hidden__=["loc"]
            )
        )

    def make_local(self, _name:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.MAKE_LOCAL, name=_name, loc=_loc, __hidden__=["loc"]
            )
        )

    def store_name(self, _name:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.STORE_NAME, name=_name, loc=_loc, __hidden__=["loc"]
            )
        )
    
    def store_local(self, _name:str):
        """ Deprecated
        """
        raise RuntimeError("use of deprecated methods")
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.STORE_LOCAL, name=_name
            )
        )
    
    
    def call(self, _size:int, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.CALL, size=_size, loc=_loc, __hidden__=["loc"]
            )
        )
    
    def call_method(self, _size:int, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.CALL_METHOD, size=_size, loc=_loc, __hidden__=["loc"]
            )
        )

    def postfix_op(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.POSTFIX_OP, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )
    
    def unary_op(self, _operator:str, _size:int, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.UNARY_OP, opt=_operator, size=_size, loc=_loc, __hidden__=["loc"]
            )
        )

    
    def binary_pow(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_POW, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )

    
    def binary_mul(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_MUL, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )
    
    
    def binary_div(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_DIV, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )
    
    
    def binary_mod(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_MOD, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )

    
    def binary_add(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_ADD, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )
    
    
    def binary_sub(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_SUB, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )

    
    def binary_lshift(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_LSHIFT, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )

    
    def binary_rshift(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_RSHIFT, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )
    
    
    def binary_and(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_AND, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )

    
    def binary_xor(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_XOR, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )
    
    
    def binary_or(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_OR, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )
    
    
    def binary_subscript(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.BINARY_SUBSCRIPT
            )
        )
    
    
    def set_subscript(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.SET_SUBSCRIPT
            )
        )
    
    
    def compare_op(self, _operator:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.COMPARE_OP, opt=_operator, loc=_loc, __hidden__=["loc"]
            )
        )
    
    
    def inplace_pow(self, _opt:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_POW, opt=_opt
            )
        )

    
    def inplace_mul(self, _opt:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_MUL, opt=_opt
            )
        )
    
    
    def inplace_div(self, _opt:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_DIV, opt=_opt
            )
        )
    
    
    def inplace_mod(self, _opt:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_MOD, opt=_opt
            )
        )
    
    
    def inplace_add(self, _opt:str, _loc:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_ADD, opt=_opt, loc=_loc, __hidden__=["loc"]
            )
        )
    
    
    def inplace_sub(self, _opt:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_SUB, opt=_opt
            )
        )
    
    
    def inplace_lshift(self, _opt:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_LSHIFT, opt=_opt
            )
        )
    
    
    def inplace_rshift(self, _opt:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_RSHIFT, opt=_opt
            )
        )
    
    
    def inplace_and(self, _opt:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_AND, opt=_opt
            )
        )
    
    
    def inplace_xor(self, _opt:str):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.INPLACE_XOR, opt=_opt
            )
        )
    
    
    def inplace_or(self, _opt:str):
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
    
    def throw_error(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.THROW_ERROR
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

    def dup_top(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.DUP_TOP
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
    
    def new_block(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.NEW_BLOCK
            )
        )

    def end_block(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.END_BLOCK
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
    
    
    def return_op(self):
        self.__instructions\
        .append(
            Instruction(
                len(self.__instructions) * 2,
                CSOpCode.RETURN_OP
            )
        )