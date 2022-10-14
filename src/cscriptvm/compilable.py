
from cstoken import CSToken

# core
from object.csobject import CSObject
from cscriptvm.csOpcode import CSOpCode



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
    
    INSTRUCTIONS:list[list[Instruction]] = [
        []
    ]

    def __init__(self):
        pass

    @staticmethod
    def peekLast():
        return Compilable.INSTRUCTIONS[-1][-1]
    
    @staticmethod
    def getLine():
        return len(Compilable.INSTRUCTIONS[-1]) * 2

    @staticmethod
    def push_name(_name:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.PUSH_NAME, name=_name
            )
        )

    @staticmethod
    def push_constant(_csobject:CSObject):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.PUSH_CONST, obj=_csobject
            )
        )
    
    @staticmethod
    def make_array(_size:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.MAKE_ARRAY, size=_size
            )
        )
    
    @staticmethod
    def make_object(_size:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.MAKE_OBJECT, size=_size
            )
        )
    
    @staticmethod
    def make_class(_size:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.MAKE_CLASS, size=_size
            )
        )
    
    @staticmethod
    def make_module():
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.MAKE_MODULE
            )
        )
    
    @staticmethod
    def get_attrib(_attrib:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.GET_ATTRIB, attr=_attrib
            )
        )

    @staticmethod
    def set_attrib(_attrib:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.SET_ATTRIB, attr=_attrib
            )
        )
    
    @staticmethod
    def call(_opt:CSToken, _size:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.CALL, opt=_opt, size=_size
            )
        )
    
    @staticmethod
    def unary_op(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.UNARY_OP, opt=_operator
            )
        )

    @staticmethod
    def binary_pow(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_POW, opt=_operator
            )
        )

    @staticmethod
    def binary_mul(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_MUL, opt=_operator
            )
        )
    
    @staticmethod
    def binary_div(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_DIV, opt=_operator
            )
        )
    
    @staticmethod
    def binary_mod(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_MOD, opt=_operator
            )
        )

    @staticmethod
    def binary_add(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_ADD, opt=_operator
            )
        )
    
    @staticmethod
    def binary_sub(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_SUB, opt=_operator
            )
        )

    @staticmethod
    def binary_lshift(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_LSHIFT, opt=_operator
            )
        )

    @staticmethod
    def binary_rshift(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_RSHIFT, opt=_operator
            )
        )
    
    @staticmethod
    def binary_and(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_AND, opt=_operator
            )
        )

    @staticmethod
    def binary_xor(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_XOR, opt=_operator
            )
        )
    
    @staticmethod
    def binary_or(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_OR, opt=_operator
            )
        )
    
    @staticmethod
    def binary_subscript(_opt:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.BINARY_SUBSCRIPT, opt=_opt
            )
        )
    
    @staticmethod
    def set_subscript(_opt:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.SET_SUBSCRIPT, opt=_opt
            )
        )
    
    @staticmethod
    def compare_op(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.COMPARE_OP, opt=_operator
            )
        )

    @staticmethod
    def pop_jump_if_false(_target:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.POP_JUMP_IF_FALSE, target=_target
            )
        )

    @staticmethod
    def pop_jump_if_true(_target:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.POP_JUMP_IF_TRUE, target=_target
            )
        )
    
    @staticmethod
    def jump_if_false_or_pop(_target:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.JUMP_IF_FALSE_OR_POP, target=_target
            )
        )
    
    @staticmethod
    def jump_if_true_or_pop(_target:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.JUMP_IF_TRUE_OR_POP, target=_target
            )
        )
    
    @staticmethod
    def jump_equal(_target:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.JUMP_EQUAL, target=_target
            )
        )
    
    @staticmethod
    def jump_not_equal(_target:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.JUMP_NOT_EQUAL, target=_target
            )
        )
    
    @staticmethod
    def jump_to(_target:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.JUMP_TO, target=_target
            )
        )
    
    @staticmethod
    def absolute_jump(_target:int):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.ABSOLUTE_JUMP, target=_target
            )
        )
    
    @staticmethod
    def no_operation():
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.NO_OPERATION
            )
        )

    @staticmethod
    def pop_top():
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.POP_TOP
            )
        )
    
    @staticmethod
    def return_op():
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(
                len(Compilable.INSTRUCTIONS[-1]) * 2,
                CSOpCode.RETURN_OP
            )
        )