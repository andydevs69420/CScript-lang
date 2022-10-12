
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

    def __init__(self, _opcode:CSOpCode, **_kwargs):
        self.opcode = _opcode
        self.kwargs = _kwargs
    
    def __str__(self):
        _args = ""
        for k,v in zip(self.kwargs.keys(), self.kwargs.values()):
            _args += f"{k} = {v.__str__()}"
            _args += "|"
        if _args.endswith("|"): _args = _args[0:-1]
        return f"{self.opcode.name}: {_args}"


class Compilable(object):
    
    INSTRUCTIONS:list[list[Instruction]] = [
        []
    ]

    def __init__(self):
        pass
    
    

    @staticmethod
    def push_constant(_csobject:CSObject):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.PUSH_CONST, obj=_csobject)
        )

    @staticmethod
    def binary_pow(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.BINARY_POW, opt=_operator)
        )

    @staticmethod
    def binary_mul(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.BINARY_MUL, opt=_operator)
        )
    
    @staticmethod
    def binary_div(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.BINARY_DIV, opt=_operator)
        )
    
    @staticmethod
    def binary_mod(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.BINARY_MOD, opt=_operator)
        )

    @staticmethod
    def binary_add(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.BINARY_ADD, opt=_operator)
        )
    
    @staticmethod
    def binary_sub(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.BINARY_SUB, opt=_operator)
        )

    @staticmethod
    def binary_lshift(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.BINARY_LSHIFT, opt=_operator)
        )

    @staticmethod
    def binary_rshift(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.BINARY_RSHIFT, opt=_operator)
        )
    
    @staticmethod
    def binary_and(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.BINARY_AND, opt=_operator)
        )

    @staticmethod
    def binary_xor(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.BINARY_XOR, opt=_operator)
        )
    
    @staticmethod
    def binary_or(_operator:CSToken):
        Compilable.INSTRUCTIONS[-1]\
        .append(
            Instruction(CSOpCode.BINARY_OR, opt=_operator)
        )
