
import cstoken
from strongtyping.strong_typing import match_typing


from csobject import CSObject
from csevaluator import Evaluatable, Evaluator


class CSAst(object):
    """ CSAst ast for cscript
    """

    def __init__(self):
        super().__init__()
        
    
    def compile(self):
        """ Compiles ast

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("compile method must be override!")


class ReferenceNode(CSAst):
    """ Holds reference

        Parameters
        ----------
        _id : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _id:cstoken.CSToken):
        super().__init__()
        self.reference = _id
    
    def compile(self):
        return super().compile()


class IntegerNode(CSAst, Evaluatable):
    """ Holds string node

        Parameters
        ----------
        _str : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _int:cstoken.CSToken):
        super().__init__()
        self.integer = _int
        
    def compile(self):
        return super().compile()
    
    def evaluate(self):
        return CSObject.new_integer(int(self.integer.token))


class DoubleNode(CSAst, Evaluatable):
    """ Holds string node

        Parameters
        ----------
        _str : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _double:cstoken.CSToken):
        super().__init__()
        self.double = _double
        
    def compile(self):
        return super().compile()
    
    def evaluate(self):
        return CSObject.new_double(float(self.double.token))



class StringNode(CSAst, Evaluatable):
    """ Holds string node

        Parameters
        ----------
        _str : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _str:cstoken.CSToken):
        super().__init__()
        self.string = _str
        
    def compile(self):
        return super().compile()
    
    def evaluate(self):
        return CSObject.new_string(self.string.token)

class BoolNode(CSAst, Evaluatable):
    """ Holds boolean node

        Parameters
        ----------
        _bool : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _bool:cstoken.CSToken):
        super().__init__()
        self.boolean = _bool
        
    def compile(self):
        return super().compile()
    
    def evaluate(self):
        return CSObject.new_boolean(self.boolean.token)

class NullNode(CSAst, Evaluatable):
    """ Holds nulltype node

        Parameters
        ----------
        _null : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _null:cstoken.CSToken):
        super().__init__()
        self.nulltype = _null
        
    def compile(self):
        return super().compile()
    
    def evaluate(self):
        return CSObject.new_nulltype(self.nulltype.token)


class ArrayNode(CSAst):
    """ Holds array node

        Parameters
        ----------
        _elements : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _elements:tuple):
        super().__init__()
        self.elements = _elements
    
    def compile(self):
        return super().compile()


class ObjectNode(CSAst):
    """ Holds object node

        Parameters
        ----------
        _elements : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _elements:tuple):
        super().__init__()
    

    def compile(self):
        return super().compile()


class AccessNode(CSAst):
    """ Holds member access node

        Parameters
        ----------
        _lefthand  : CSAst
        _attribute : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _lefthand:CSAst, _attribute:cstoken.CSToken):
        super().__init__()
        self.lefthand  = _lefthand
        self.attribute = _attribute
    
    def compile(self):
        return super().compile()
    

class StaticAccessNode(CSAst):
    """ Holds static access node

        Parameters
        ----------
        _lefthand  : CSAst
        _attribute : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _lefthand:CSAst, _attribute:cstoken.CSToken):
        super().__init__()
        self.lefthand  = _lefthand
        self.attribute = _attribute
    
    def compile(self):
        return super().compile()


class SubscriptNode(CSAst):
    """ Holds subscription node

        Parameters
        ----------
        _lefthand : CSAst
        _expr     : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _lefthand:CSAst, _expr:CSAst):
        super().__init__()
        self.lefthand   = _lefthand
        self.expression = _expr
    
    def compile(self):
        return super().compile()

class CallNode(CSAst):
    """ Holds call node

        Parameters
        ----------
        _lefthand  : CSAst
        _arguments : tuple
    """

    @match_typing
    def __init__(self, _lefthand:CSAst, _arguments:tuple):
        super().__init__()
        self.lefthand  = _lefthand
        self.arguments = _arguments
    
    def compile(self):
        return super().compile()


class TernaryNode(CSAst):
    """ Holds ternary node

        Parameters
        ----------
        _condition : CSAst
        _true      : CSAst
        _false     : CSAst
    """

    @match_typing
    def __init__(self, _condition:CSAst, _true:CSAst, _false:CSAst):
        super().__init__()
        self.condition = _condition
        self.vtrue  = _true
        self.vfalse = _false
    
    def compile(self):
        return super().compile()

class AllocDeallocNode(CSAst, Evaluator):
    """ Holds allocate and deallocate expression node

        Parameters
        ----------
        _opt : cstoken.CSToken
        _rhs : CSAst
    """

    @match_typing
    def __init__(self, _opt:cstoken.CSToken, _rhs:CSAst):
        super().__init__()
        self.opt = _opt
        self.rhs = _rhs
    
    def compile(self):
        return super().compile()


class UnaryExprNode(CSAst, Evaluator):
    """ Holds unary expression node

        Parameters
        ----------
        _opt : cstoken.CSToken
        _rhs : CSAst
    """

    @match_typing
    def __init__(self, _opt:cstoken.CSToken, _rhs:CSAst):
        super().__init__()
        self.opt = _opt
        self.rhs = _rhs
    
    def compile(self):
        return super().compile()
    
    def evaluate(self):
        return self.evaluate_unary_op(self.opt, self.rhs)


class BinaryExprNode(CSAst, Evaluator):
    """ Holds binary expression node

        Parameters
        ----------
        _opt : cstoken.CSToken
        _lhs : CSAst
        _rhs : CSAst
    """

    @match_typing
    def __init__(self, _opt:cstoken.CSToken, _lhs:CSAst, _rhs:CSAst):
        super().__init__()
        self.opt = _opt
        self.lhs = _lhs
        self.rhs = _rhs
        
    def compile(self):

        _result = self.evaluate_bin_op(self.opt, self.lhs, self.rhs)

        return super().compile()
    
    def evaluate(self):
        return self.evaluate_bin_op(self.opt, self.lhs, self.rhs)