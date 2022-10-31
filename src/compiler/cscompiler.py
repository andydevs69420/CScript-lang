


# .
from compiler.csrawcode import rawcode
from .csxcompileerror import CSXCompileError
from .cseval import CSEval
from .blockcompiler import BlockCompiler

# utility
from utility.asttypes import ExpressionType

# grammar
from grammarp.csparser import CSParser


TYPE= "type"


class RawBlock(BlockCompiler): pass
class RawBlock(BlockCompiler):
    """ Raw block parser
    """

    def __init__(self):
        super().__init__()
    
    """ EXPRESSION AREA OF COMPILING
    """

    # variable
    def cvariable(self, _node:dict):
        self.push_name(_node["var"])

    # integer
    def cinteger(self, _node:dict):
        self.push_integer(self.evaluate(_node))
    
    # double
    def cdouble(self, _node:dict):
        self.push_double(self.evaluate(_node))
    
    # string
    def cstring(self, _node:dict):
        self.push_string(self.evaluate(_node))
    
    # boolean
    def cboolean(self, _node:dict):
        self.push_boolean(self.evaluate(_node))
    
    # null
    def cnull(self, _node:dict):
        self.push_null(self.evaluate(_node))

    # array build
    def carray(self, _node:dict):
        _elements = _node["elements"]

        # reverse
        for _expr in _elements[::-1]:
            # compile right-most
            self.visit(_expr)
        
        # compile array
        self.make_array(len(_elements))
    
    # object build
    def cobject(self, _node:dict):
        _elements = _node["elements"]

        # reverse
        for _expr in _elements[::-1]:
            # compile right-most
            self.visit(_expr["val"])

            # make name as string
            self.push_string(_expr["key"])
        
        # compile array
        self.make_object(len(_elements))
    
    # member access
    def cmember(self, _node:dict):
        # visit left
        self.visit(_node["left"])

        # add get attrib
        self.get_attrib(_node["member"])
    
    # subscript
    def csubscript(self, _node:dict):
        # visit index|member
        self.visit(_node["index"])

        # visit left
        self.visit(_node["left"])

        # add subscript
        self.binary_subscript()
    
    # call
    def ccall(self, _node:dict):
        _arguments = _node["args"]

        # compile reverse
        for _expr in _arguments[::-1]:
            # compile right-most
            self.visit(_expr)

        # push calling object
        self.visit(_node["left"])

        # add call
        self.call(len(_arguments))

    # binary expr
    def cbinary(self, _node:dict):
        # evaluated
        _value = self.evaluate(_node)

        # ensure ellipsis instead None|bool
        if  _value != ...:
            if   type(_value) == int  :
                self.push_integer(_value)
            elif type(_value) == float:
                self.push_double(_value)
            elif type(_value) == str  :
                self.push_string(_value)
            elif type(_value) == bool :
                self.push_boolean(_value)
            # if None
            elif not _value:
                self.push_null(_value)
            else:
                raise TypeError("unsupported type %s" % type(_value).__name__)
            return

        # otherwise compile

        # compile rhs
        self.visit(_node["right"])
        
        # compile lhs
        self.visit(_node["left" ])

        _operator = _node["opt"]

        match _operator:
            # arithmetic
            case "^^":
                self.binary_pow(_operator)
            case '*':
                self.binary_mul(_operator)
            case '/':
                self.binary_div(_operator)
            case '%':
                self.binary_mod(_operator)
            case '+':
                self.binary_add(_operator)
            case '-':
                self.binary_sub(_operator)
            # bitwise
            case "<<":
                self.binary_lshift(_operator)
            case ">>":
                self.binary_rshift(_operator)
            case '&':
                self.binary_and(_operator)
            case '^':
                self.binary_xor(_operator)
            case '|':
                self.binary_or (_operator)
        
        raise NotImplementedError("unimplemented operator '%s'" % _operator)

    # compare expr
    def ccompare(self, _node:dict):
        # evaluated
        _value = self.evaluate(_node)
        # ensure ellipsis instead None|bool
        if  _value != ...:
            if   type(_value) == int  :
                self.push_integer(_value)
            elif type(_value) == float:
                self.push_double(_value)
            elif type(_value) == str  :
                self.push_string(_value)
            elif type(_value) == bool :
                self.push_boolean(_value)
            # if None
            elif not _value:
                self.push_null(_value)
            else:
                raise TypeError("unsupported type %s" % type(_value).__name__)
            return

        # otherwise compile

        # compile rhs
        self.visit(_node["right"])
        
        # compile lhs
        self.visit(_node["left" ])

        # add operator
        _operator = _node["opt"]
        self.compare_op(_operator)
    
    # logical expr | short circuit
    def clogical(self, _node:dict):
        # evaluated
        _value = self.evaluate(_node)
        # ensure ellipsis instead None|bool
        if  _value != ...:
            if   type(_value) == int  :
                self.push_integer(_value)
            elif type(_value) == float:
                self.push_double(_value)
            elif type(_value) == str  :
                self.push_string(_value)
            elif type(_value) == bool :
                self.push_boolean(_value)
            # if None
            elif not _value:
                self.push_null(_value)
            else:
                raise TypeError("unsupported type %s" % type(_value).__name__)
            return

        # otherwise compile

        # compile left
        self.visit(_node["left" ])

        _jump_target_0 = ...

        _operator = _node["opt"]

        if  _operator == "&&":
            self.jump_if_false_or_pop(...)
        else:
            self.jump_if_true_or_pop(...)
        
        _jump_target_0 = self.peekLast()

        # add pop
        self.pop_top()

        # compile right
        self.visit(_node["right"])

        # set jump target 0 to this line
        _jump_target_0.kwargs["target"] = self.getLine()
    
    # ternary
    def cternary(self, _node:dict):
        # compile condition
        self.visit(_node["condition"])

        # add jump to false
        self.pop_jump_if_false(...)
        _jump_target_0 = self.peekLast()

        # compile true
        self.visit(_node["ift"])
        
        # add jump if true is evaluated
        self.jump_to(...)
        _jump_target_1 = self.peekLast()


        # set jump target 0 to this line if
        # condition is false
        _jump_target_0.kwargs["target"] = self.getLine()

        # compile false
        self.visit(_node["iff"])

        # set jump target 1 to this line if
        # true value is evaluated
        _jump_target_1.kwargs["target"] = self.getLine()


    # assignment
    def cassignment(self, _node:dict):
        # compile rhs
        self.visit(_node["right"])

        # duplicate top
        self.dup_top()
        
        match _node["left"][TYPE]:
            # variable assignment
            case ExpressionType.VARIABLE:
                self.store_name(_node["left"]["var"])
            # member assignment
            case ExpressionType.MEMBER:
                # compile owner
                self.visit(_node["left"]["left" ])

                # set attibute
                self.set_attrib(_node["left"]["member"])
            # index|member assignment
            case ExpressionType.SUBSCRIPT:
                # compile index|member
                self.visit(_node["left"]["index"])

                # compile owner
                self.visit(_node["left"]["left" ])

                # add subscript
                self.set_subscript()
            case _:
                CSXCompileError.csx_Error("SemanticError: can't assign left-hand of operator '%s'!" % _node["opt"])
    
    # augmented
    def caugmented(self, _node:dict):
        # compile rhs
        self.visit(_node["right"])

        # compile left
        self.visit(_node["left" ])

        _operator = _node["opt"]
        match _operator:
            case "^^=":
                self.inplace_pow(_operator)
            case "*=":
                self.inplace_mul(_operator)
            case "/=":
                self.inplace_div(_operator)
            case "%=":
                self.inplace_mod(_operator)
            case "+=":
                self.inplace_add(_operator)
            case "-=":
                self.inplace_sub(_operator)
            case "<<=":
                self.inplace_lshift(_operator)
            case ">>=":
                self.inplace_rshift(_operator)
            case "&=":
                self.inplace_and(_operator)
            case "^=":
                self.inplace_xor(_operator)
            case "|=":
                self.inplace_or(_operator)
            case _:
                raise NotImplementedError("unimplemented operator '%s'" % _operator)

        # duplicate top
        self.dup_top()
        
        match _node["left"][TYPE]:
            # variable assignment
            case ExpressionType.VARIABLE:
                self.store_name(_node["left"]["var"])
            # member assignment
            case ExpressionType.MEMBER:
                # compile owner
                self.visit(_node["left"]["left" ])

                # set attibute
                self.set_attrib(_node["left"]["member"])
            # index|member assignment
            case ExpressionType.SUBSCRIPT:
                # compile index|member
                self.visit(_node["left"]["index"])

                # compile owner
                self.visit(_node["left"]["left" ])

                # add subscript
                self.set_subscript()
            # error
            case _:
                CSXCompileError.csx_Error("SemanticError: can't assign left-hand of operator '%s'!" % _node["opt"])


    """ STATEMENT AREA OF COMPILING
    """
    # class
    def cclass(self, _node:dict):
        _ccom = ClassCompiler(_node)
        _ccom.compile()

        # make class
        self.make_class()
        
        # call class
        self.call(0)
    
    # func
    def cfunc(self, _node:dict):

        if  type(self) == ClassCompiler:
            # function is inside class
            ...
        else:
            ...

    # block
    def cblock(self, _node:dict):
        for _stmnt in _node["block"]:
            # compile statement
            self.visit(_stmnt)

    # expression node
    def cexpression(self, _node:dict):
        # compile expression
        self.visit(_node["expression"])

        # add pop
        self.pop_top()

    # module node
    def cmodule(self, _node:dict):
        for _child in _node["children"]:
            self.visit(_child)
        
        for i in self.getInsntructions():
            print(i)



class CSCompiler(RawBlock, CSEval):pass
class CSCompiler(RawBlock, CSEval):

    def __init__(self, _fpath:str, _scode:str):
        super().__init__()
        self.fpath:str = _fpath 
        self.scode:str = _scode
        self.csparser = CSParser(self.fpath, self.scode)

    def compile(self):
        _root = self.csparser.parse()
        self.visit(_root)

        # return raw code
        return rawcode(self.getInsntructions())
    
    

class ClassCompiler(RawBlock):
    """
    """

    def __init__(self, _node:dict):
        super().__init__()
        self.node = _node
    
    def compile(self):
        # push name as str
        self.push_string(self.node["name"])

        # class name
        self.store_name("__name__")

        for _child in self.node["body"]:
            # compile child
            self.visit(_child)
        
        # add default return expr
        self.push_null(None)

        # add return
        self.return_op()