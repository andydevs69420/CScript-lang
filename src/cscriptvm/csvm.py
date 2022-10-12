
from object.csobject import CSObject

class ExceptionTable:

    @staticmethod
    def make(_id:int, ):
        ...



class EvalStack:
    """ Evaluation stack for CSCript
    """
    
    EVAL_STACK = [
        # +------------+ ^
        # | CSObject N | |
        # +------------+ |
        #                |
        # +------------+ |
        # | CSObject 0 | |
        # +------------+ |
    ]

    @staticmethod
    def push(_object:CSObject):
        return EvalStack.EVAL_STACK\
            .append(_object)
    
    @staticmethod
    def peek():
        return EvalStack.EVAL_STACK[-1]

    @staticmethod    
    def pop():
        return EvalStack.EVAL_STACK\
            .pop()


class CallStack:
    
    CALL_STACK = [
        # CALL: N
        # +---------------+
        # | instruction 0 |
        # +---------------+
        # | ...           |
        # +---------------+
        # | instruction N |
        # +---------------+

        # CALL: 0
        # +---------------+
        # | instruction 0 |
        # +---------------+
        # | ...           |
        # +---------------+
        # | instruction N |
        # +---------------+
    ]


class CSVirtualMachine(
    ExceptionTable, 
    EvalStack     , 
    CallStack     ,
):
    
    
    @staticmethod
    def run():
        ...

    
