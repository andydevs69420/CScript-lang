
import cstoken
from compilable import Compilable
from strongtyping.strong_typing import match_typing

# core
from cscriptvm.csevaluator import Evaluatable, Evaluator
from object.csobject import CSObject


class CSAst(Compilable):
    """ CSAst ast for cscript
    """

    class COMPILE_STATE:
        ...

    def __init__(self):
        super().__init__()
        
    
    def compile(self):
        """ Compiles ast

            Returns
            -------
            CSObject
        """
        raise NotImplementedError(f"{type(self).__name__}::compile method must be override!")


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
    
    def evaluate(self):
        """ Leave None!!!
        """
        return None


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
        self.push_constant(self.evaluate())
    
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
        self.push_constant(self.evaluate())
    
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
        self.push_constant(self.evaluate())
    
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
        self.push_constant(self.evaluate())
    
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
        self.push_constant(self.evaluate())
    
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
        _condition = self.condition.evaluate()
        if  _condition:
            if  _condition.get("this"):
                self.vtrue.compile()
            else:
                self.vfalse.compile()
            return
        
        # continue compilation





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
        _result = self.evaluate()
        if  _result:
            self.push_constant(_result)
            return
    
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
        _result = self.evaluate()
        if  _result:
            self.push_constant(_result)
            return
        
        # continue compilation

        # compile rhs
        self.rhs.compile()
        # compile lhs
        self.lhs.compile()

        # select by op
        if  self.opt.matches("^^"):
            self.binary_pow(self.opt)
        elif self.opt.matches("*"):
            self.binary_mul(self.opt)
        elif self.opt.matches("/"):
            self.binary_div(self.opt)
        elif self.opt.matches("%"):
            self.binary_mod(self.opt)
        elif self.opt.matches("+"):
            self.binary_add(self.opt)
        elif self.opt.matches("-"):
            self.binary_sub(self.opt)
        elif self.opt.matches("<<"):
            self.binary_lshift(self.opt)
        elif self.opt.matches(">>"):
            self.binary_rshift(self.opt)
        elif self.opt.matches("&"):
            self.binary_and(self.opt)
        elif self.opt.matches("^"):
            self.binary_xor(self.opt)
        elif self.opt.matches("|"):
            self.binary_or(self.opt)
        else:\
        raise NotImplementedError("invalid operator \"%s\"" % self.opt.token)
    
    def evaluate(self):
        return self.evaluate_bin_op(self.opt, self.lhs, self.rhs)






class CompareExprNode(CSAst, Evaluator):
    """ Holds comparison expression node

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
        _result = self.evaluate()
        if  _result:
            self.push_constant(_result)
            return

        # continue compilation

        # compile rhs
        self.rhs.compile()
        # compile lhs
        self.lhs.compile()

        return super().compile()
    
    def evaluate(self):
        return self.evaluate_comp_op(self.opt, self.lhs, self.rhs)


class LogicalExprNode(CompareExprNode):
    """ Holds logical expression|jump

        Parameters
        ----------
        _opt : cstoken.CSToken
        _lhs : CSAst
        _rhs : CSAst
    """

    def __init__(self, _opt: cstoken.CSToken, _lhs: CSAst, _rhs: CSAst):
        super().__init__(_opt, _lhs, _rhs)
    
    def compile(self):
        _result = self.evaluate()
        if  _result:
            self.push_constant(_result)
            return

        # continue compilation

        # compile rhs
        self.rhs.compile()
        # compile lhs
        self.lhs.compile()
    
    def evaluate(self):
        return super().evaluate()


# =============================== BEGIN COMPOUND
# ==============================================