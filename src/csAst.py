import cstoken
from errortoken import show_error
from strongtyping.strong_typing import match_typing

# core
from cscriptvm.csevaluator import Evaluatable, Evaluator
from cscriptvm.cssymboltable import CSSymbolTable as ST
from cscriptvm.csvm import CSVirtualMachine as VM
from cscriptvm.compilable import Compilable
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
            None
        """
        raise NotImplementedError(f"{type(self).__name__}::compile method must be override!")


class Assignable(CSAst):
    def __init__(self):
        super().__init__()
    
    def compile(self):
        return super().compile()
    
    def offset(self):
        """ get reference

            Returns
            -------
            None
        """
        raise NotImplementedError(f"{type(self).__name__}::reference method must be override!")
    
    def assign(self):
        """ Compile as assign

            Returns
            -------
            None
        """
        raise NotImplementedError(f"{type(self).__name__}::assign method must be override!")



class ReferenceNode(Assignable):
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
        # check if exists
        if  not ST.exists(self.reference.token):
            return show_error("name \"%s\" is not defined" % self.reference.token, self.reference)

        # compile
        _s = ST.lookup(self.reference.token)
        self.push_name(self.reference, _s["_slot"])
    
    def assign(self):
        # check if exists
        if  not ST.exists(self.reference.token):
            return show_error("name \"%s\" is not defined" % self.reference.token, self.reference)

        # decrement where it is pointed first
        _s = ST.lookup(self.reference.token)
        VM.decRef(_s["_slot"])

        # compile
        self.store_name(self.reference, _s["_slot"])

        # push to stack new value
        self.push_name (self.reference, _s["_slot"])
    
    def offset(self):
        # check if exists
        if  not ST.exists(self.reference.token):
            return show_error("name \"%s\" is not defined" % self.reference.token, self.reference)

        _offset = ST.lookup(self.reference.token)

        # increase ref count
        VM.incRef(_offset["_slot"])

        return _offset
    
    def evaluate(self):
        """ Leave None!!!
        """
        return None



# OK!!! | PASSED
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




# OK!!! | PASSED
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



# OK!!! | PASSED
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



# OK!!! | PASSED
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




# OK!!!
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




# OK!!!
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
        # compile right most first!
        for node in self.elements[::-1]:
            _evaluated = node.evaluate()
            if  _evaluated:
                self.push_constant(_evaluated)
            else:
                node.compile()
        
        # array opcode
        self.make_array(len(self.elements))
    
    def evaluate(self):
        """ Leave None!!!
        """
        return None




# OK!!!
class ObjectNode(CSAst):
    """ Holds object node

        Parameters
        ----------
        _elements : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _elements:tuple):
        super().__init__()
        self.elements = _elements

    def compile(self):
        # compile right most first!
        for node in self.elements[::-1]:

            # value
            _evaluated = node["val"].evaluate()
            if  _evaluated:
                self.push_constant(_evaluated)
            else:
                node["val"].compile()
            
            # key|attrib
            self.push_constant(CSObject.new_string(node["key"].token))

        # object opcode
        self.make_object(len(self.elements))


    def evaluate(self):
        """ Leave None!!!
        """
        return None




# OK!!!
class AccessNode(Assignable):
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
        # compile lhs
        self.lefthand.compile()

        # attrib
        self.get_attrib(self.attribute)
    
    def assign(self):
        # compile lhs
        self.lefthand.compile()

        # attrib
        self.set_attrib(self.attribute)

    




# OK!!! NOTE: check static member
class StaticAccessNode(Assignable):
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
        # compile lhs
        self.lefthand.compile()

        # attrib
        self.get_attrib(self.attribute)
    
    def assign(self):
        # compile lhs
        self.lefthand.compile()

        # attrib
        self.set_attrib(self.attribute)






# OK!!!
class SubscriptNode(Assignable):
    """ Holds subscription node

        Parameters
        ----------
        _lefthand : CSAst
        _expr     : CSAst
        _opt      : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _lefthand:CSAst, _expr:CSAst, _opt:cstoken.CSToken):
        super().__init__()
        self.lefthand   = _lefthand
        self.expression = _expr
        self.opt = _opt
    
    def compile(self):
        # compile left
        self.lefthand.compile()

        # compile expression
        self.expression.compile()

        # subscript opcode
        self.binary_subscript(self.opt)
    

    def assign(self):
        # compile left
        self.lefthand.compile()

        # compile expression
        self.expression.compile()

        # subscript opcode
        self.set_subscript(self.opt)




# OK!!!
class CallNode(CSAst):
    """ Holds call node

        Parameters
        ----------
        _lefthand  : CSAst
        _arguments : tuple
        _opt       : cstoken.CSToken
    """

    @match_typing
    def __init__(self, _lefthand:CSAst, _arguments:tuple, _opt:cstoken.CSToken):
        super().__init__()
        self.lefthand  = _lefthand
        self.arguments = _arguments
        self.opt = _opt
    
    def compile(self):
        # compile left
        self.lefthand.compile()

        # compile right most first!
        for node in self.arguments[::-1]:

            # value
            _evaluated = node["val"].evaluate()
            if  _evaluated:
                self.push_constant(_evaluated)
            else:
                node["val"].compile()
            
            # key|attrib
            self.push_constant(CSObject.new_string(node["key"].token))
        
        # call opcode
        self.call(self.opt, len(self.arguments))





# OK!!! | COMPILED | PASSED
class TernaryNode(CSAst, Evaluator):
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
        _result = self.evaluate()
        if  _result:
            self.push_constant(_result)
            return

        ## continue compilation ##
        self.condition.compile()

        self.pop_jump_if_false(...)
        _jump_t0 = self.peekLast()

        # compile true
        self.vtrue.compile()

        self.jump_to(...)
        _jump_t1 = self.peekLast()

        # set jump target 0
        _jump_t0.kwargs["target"] = self.getLine()

        # compile false
        self.vfalse.compile()

        # set jump target 1
        _jump_t1.kwargs["target"] = self.getLine()

    
    def evaluate(self):
        return self.evaluate_ternary_op(self.condition, self.vtrue, self.vfalse)




# TODO: implement
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





# OK!!! | COMPILED | PASSED
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
        
        # continue compilation

        # compile rhs
        self.rhs.compile()

        # add op
        self.unary_op(self.opt)
    
    def evaluate(self):
        return self.evaluate_unary_op(self.opt, self.rhs)





# OK!!! | COMPILED | PASSED
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







# OK!!! | COMPILED | PASSED
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

        # add op
        self.compare_op(self.opt)

    def evaluate(self):
        return self.evaluate_comp_op(self.opt, self.lhs, self.rhs)





# OK!!! | COMPILED | PASSED
class EqualityExprNode(CompareExprNode):
    """ Holds equality expression|jump

        Parameters
        ----------
        _opt : cstoken.CSToken
        _lhs : CSAst
        _rhs : CSAst
    """

    @match_typing
    def __init__(self, _opt: cstoken.CSToken, _lhs: CSAst, _rhs: CSAst):
        super().__init__(_opt, _lhs, _rhs)

    def compile(self):
        return super().compile()
    
    def evaluate(self):
        return super().evaluate()



# OK!!! | COMPILED | SHORT CIRCUITING | PASSED
class LogicalExprNode(CompareExprNode):
    """ Holds logical expression|jump|shortcircuit

        Parameters
        ----------
        _opt : cstoken.CSToken
        _lhs : CSAst
        _rhs : CSAst
    """

    @match_typing
    def __init__(self, _opt: cstoken.CSToken, _lhs: CSAst, _rhs: CSAst):
        super().__init__(_opt, _lhs, _rhs)
    
    def compile(self):
        _result = self.evaluate()
        if  _result:
            self.push_constant(_result)
            return

        # continue compilation
        """ Compile lhs first when 
            short-circuiting
        """

        # compile lhs
        self.lhs.compile()

        _jump_t0 = None

        if  self.opt.matches("&&"):
            # logical and
            self.jump_if_false_or_pop(...)
            _jump_t0 = self.peekLast()
        else:
            # logical or
            self.jump_if_true_or_pop(...)
            _jump_t0 = self.peekLast()

        # compile rhs
        self.rhs.compile()

        # set jump target 0
        _jump_t0.kwargs["target"] = self.getLine()

    def evaluate(self):
        return super().evaluate()



class Assignment(CSAst):
    """ Holds assignment

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
        return super().compile()


class SimpleAssignment(Assignment):
    """ Holds simple assignment

        Parameters
        ----------
        _opt : cstoken.CSToken
        _lhs : CSAst
        _rhs : CSAst
    """
    
    @match_typing
    def __init__(self, _opt:cstoken.CSToken, _lhs:CSAst, _rhs:CSAst):
        super().__init__(_opt, _lhs, _rhs)
    
    def compile(self):
        # compile rhs
        self.rhs.compile()
        
        # make sure left hand is assignable
        if  not isinstance(self.lhs, Assignable):
            return show_error("invalid left-hand expression", self.opt)

        # compile lhs
        self.lhs.assign()




class AugmentedAssignment(Assignment):
    """ Holds augmented assignment

        Parameters
        ----------
        _opt : cstoken.CSToken
        _lhs : CSAst
        _rhs : CSAst
    """

    @match_typing
    def __init__(self, _opt:cstoken.CSToken, _lhs:CSAst, _rhs:CSAst):
        super().__init__(_opt, _lhs, _rhs)
    
    def compile(self):
        # compile rhs
        self.rhs.compile()

        # make sure left hand is assignable
        if  not isinstance(self.lhs, Assignable):
            return show_error("invalid left-hand expression", self.opt)

        # compile lhs
        self.lhs.compile()

        # compile by op
        if  self.opt.matches("*="):
            self.inplace_mul(self.opt)
        elif self.opt.matches("/="):
            self.inplace_div(self.opt)
        elif self.opt.matches("%="):
            self.inplace_mod(self.opt)
        elif self.opt.matches("+="):
            self.inplace_add(self.opt)
        elif self.opt.matches("-="):
            self.inplace_sub(self.opt)
        elif self.opt.matches("<<="):
            self.inplace_lshift(self.opt)
        elif self.opt.matches(">>="):
            self.inplace_rshift(self.opt)
        elif self.opt.matches("&="):
            self.inplace_and(self.opt)
        elif self.opt.matches("^="):
            self.inplace_xor(self.opt)
        elif self.opt.matches("|="):
            self.inplace_or(self.opt)
        else:\
        raise NotImplementedError("invalid operator \"%s\"" % self.opt.token)

        # compile lhs
        self.lhs.assign()


# =============================== BEGIN COMPOUND
# ==============================================


class SpitsCode(CSAst):
    def __init__(self):
        super().__init__()
        self.INSTRUCTIONS.append([])
    
    def getInstructions(self):
        return self.INSTRUCTIONS.pop()


class ModuleNode(SpitsCode):
    """
    """

    @match_typing
    def __init__(self, _child_nodes:tuple):
        super().__init__()
        self.child_nodes = _child_nodes
    
    def compile(self):
        ST.newScope()
        for node in self.child_nodes:
            node.compile()
        ST.endScope()
        
        # module opcode
        self.make_module()

        # add default return
        self.return_op()




class ClassNode(CSAst):
    """
    """

    @match_typing
    def __init__(self, _name:cstoken.CSToken, _base:cstoken.CSToken|None, _member:tuple):
        super().__init__()
        self.name   = _name
        self.base   = _base
        self.member = _member
    
    def compile(self):
        # push class name
        self.push_constant(CSObject.new_string(self.name.token))

        # TODO: evaluate base name

        for each_member in self.member:
            # compile value
            each_member["value"].compile()

            # push name
            self.push_constant(CSObject.new_string(each_member["name"].token))
        
        self.make_class(len(self.member))

        # push class name
        self.push_constant(CSObject.new_string(self.name.token))





# OK!!! | COMPILED | PASSED
class IfStatementNode(CSAst):

    def __init__(self, _condition:CSAst, _statement:CSAst, _else:CSAst):
        super().__init__()
        self.condition = _condition
        self.statement = _statement
        self.else_stmnt = _else

    def compile(self):
        _evaluated = self.condition.evaluate()
        if  _evaluated:
            if  _evaluated.get("this"):
                # condition met|true|satisfiable
                self.statement.compile()
            else:
                if  self.else_stmnt:
                    self.else_stmnt.compile()
            return
        
        # compile branching?
        if isinstance(self.condition, LogicalExprNode):
            self.logical()
        else:
            self.default()
    
    def logical(self):
        _jump_t0, _jump_t1 = None, None

        # extract rhs and compile
        _rhs_evaluated = self.condition.rhs.evaluate()
        _rhs_evaluated = _rhs_evaluated.get("this") if _rhs_evaluated else False

        if  not _rhs_evaluated:
            self.condition.rhs.compile()

            # check rhs
            if  self.condition.opt.matches("&&"):
                # logical and
                self.pop_jump_if_false(...)
            else:
                # logical or
                self.pop_jump_if_true(...)

            _jump_t0 = self.peekLast()
        
        _lhs_evaluated = self.condition.lhs.evaluate()
        _lhs_evaluated = _lhs_evaluated.get("this") if _lhs_evaluated else False

        if  not _lhs_evaluated:
            # extract lhs and compile
            self.condition.lhs.compile()

            # always pop jump if false lhs
            self.pop_jump_if_false(...)

            _jump_t1 = self.peekLast()

        # jump to this location if rhs is true when "logical or".
        # do not evaluate lhs
        if  self.condition.opt.matches("||"):
            if  not _rhs_evaluated:
                # set jump target 0
                _jump_t0.kwargs["target"] = self.getLine()

        # statement
        self.statement.compile()

        self.jump_to(...)
        _jump_t2 = self.peekLast()

        # jump to this location if rhs is false when "logical and".
        # do not evaluate lhs
        if  self.condition.opt.matches("&&"):
            if  not _rhs_evaluated:
                # set jump target 0
                _jump_t0.kwargs["target"] = self.getLine()

        if  not _lhs_evaluated:
            # set jump target 1
            _jump_t1.kwargs["target"] = self.getLine()

        # compile else
        if  self.else_stmnt:
            self.else_stmnt.compile()
        
        # set jump target 1
        _jump_t2.kwargs["target"] = self.getLine()


    def default(self):
        self.condition.compile()

        self.pop_jump_if_false(...)
        _jump_t0 = self.peekLast()
        
        # compile statement
        self.statement.compile()

        self.jump_to(...)
        _jump_t1 = self.peekLast()

        # set jump target 0
        _jump_t0.kwargs["target"] = self.getLine()

        # compile else
        if  self.else_stmnt:
            self.else_stmnt.compile()
        
        # set jump target 1
        _jump_t1.kwargs["target"] = self.getLine()



# OK!!! | COMPILED | PASSED
class DoWileNode(CSAst):
    """ Holds while statement

        Parameters
        ----------
        _condition : CSAst
        _body      : CSAst
    """

    @match_typing
    def __init__(self, _condition:CSAst, _body:CSAst):
        super().__init__()
        self.condition = _condition
        self.body = _body
    
    def compile(self):
        _evaluated = self.condition.evaluate()
        if  _evaluated:
            if  not _evaluated.get("this"):
                # false condition|no operation
                self.no_operation()
                return

        # compile
        if isinstance(self.condition, LogicalExprNode):
            self.logical()
        else:
            self.default()

    
    def logical(self):
        _jump_t0, _jump_t1 = None, None

        _begin = self.getLine()

        # compile body
        self.body.compile()
        
        _rhs_evaluated = self.condition.rhs.evaluate()
        _rhs_evaluated = _rhs_evaluated.get("this") if _rhs_evaluated else False

        if  not _rhs_evaluated:
            # compile rhs
            self.condition.rhs.compile()

            if  self.condition.opt.matches("&&"):
                # logical and
                self.pop_jump_if_false(...)
            else:
                # logical or
                self.pop_jump_if_true(...)
            
            _jump_t0 = self.peekLast()

        _lhs_evaluated = self.condition.lhs.evaluate()
        _lhs_evaluated = _lhs_evaluated.get("this") if _lhs_evaluated else False

        if  not _lhs_evaluated:
            # compile rhs
            self.condition.lhs.compile()
            
            # always pop jump if false lhs
            self.pop_jump_if_false(...)
            
            _jump_t1 = self.peekLast()


        # # jump to this location if rhs is true when "logical or"!
        if  self.condition.opt.matches("||"):
            # set jump target 0
            _jump_t0.kwargs["target"] = self.getLine()

        # jumpt to condition
        self.absolute_jump(_begin)

        # jump to this|end location if rhs is false when "logical and"!
        # do not evaluate lhs
        if  self.condition.opt.matches("&&"):
            if  not _rhs_evaluated:
                # set jump target 0
                _jump_t0.kwargs["target"] = self.getLine()
        
        if  not _lhs_evaluated:
            # set jump target 0
            _jump_t1.kwargs["target"] = self.getLine()

    def default(self):
        _begin = self.getLine()

        # compile body
        self.body.compile()

        # compile condition
        self.condition.compile()

        self.pop_jump_if_false(...)
        _jump_t0 = self.peekLast()

        # jump to condition
        self.absolute_jump(_begin)

        # set jump target 0
        _jump_t0.kwargs["target"] = self.getLine()



# OK!!! | COMPILED | PASSED
class WhileNode(CSAst):
    """ Holds while statement

        Parameters
        ----------
        _condition : CSAst
        _body      : CSAst
    """

    @match_typing
    def __init__(self, _condition:CSAst, _body:CSAst):
        super().__init__()
        self.condition = _condition
        self.body = _body
    
    def compile(self):
        _evaluated = self.condition.evaluate()
        if  _evaluated:
            if  not _evaluated.get("this"):
                # false condition|no operation
                self.no_operation()
                return

        # compile
        if isinstance(self.condition, LogicalExprNode):
            self.logical()
        else:
            self.default()
    
    def logical(self):
        _jump_t0, _jump_t1 = None, None

        _begin = self.getLine()
        
        _rhs_evaluated = self.condition.rhs.evaluate()
        _rhs_evaluated = _rhs_evaluated.get("this") if _rhs_evaluated else False

        if  not _rhs_evaluated:
            # compile rhs
            self.condition.rhs.compile()

            if  self.condition.opt.matches("&&"):
                # logical and
                self.pop_jump_if_false(...)
            else:
                # logical or
                self.pop_jump_if_true(...)
            
            _jump_t0 = self.peekLast()

        _lhs_evaluated = self.condition.lhs.evaluate()
        _lhs_evaluated = _lhs_evaluated.get("this") if _lhs_evaluated else False

        if  not _lhs_evaluated:
            # compile rhs
            self.condition.lhs.compile()
            
            # always pop jump if false lhs
            self.pop_jump_if_false(...)
            
            _jump_t1 = self.peekLast()


        # # jump to this location if rhs is true when "logical or"!
        if  self.condition.opt.matches("||"):
            # set jump target 0
            _jump_t0.kwargs["target"] = self.getLine()

        # compile body
        self.body.compile()

        # jumpt to condition
        self.absolute_jump(_begin)

        # jump to this|end location if rhs is false when "logical and"!
        # do not evaluate lhs
        if  self.condition.opt.matches("&&"):
            if  not _rhs_evaluated:
                # set jump target 0
                _jump_t0.kwargs["target"] = self.getLine()
        
        if  not _lhs_evaluated:
            # set jump target 0
            _jump_t1.kwargs["target"] = self.getLine()
    
    def default(self):
        _begin = self.getLine()

        # compile condition
        self.condition.compile()

        self.pop_jump_if_false(...)
        _jump_t0 = self.peekLast()

        # compile body
        self.body.compile()

        # jump to condition
        self.absolute_jump(_begin)

        # set jump target 0
        _jump_t0.kwargs["target"] = self.getLine()


# OK!!! | COMPILED | PASSED
class SwitchNode(CSAst):
    """ Holds switch statement

        Parameters
        ----------
        _condition : CSAst
        _body      : dict
    """

    @match_typing
    def __init__(self, _condition:CSAst, _body:dict):
        super().__init__()
        self.condition = _condition
        self.body = _body

    def compile(self):
        _jump_end = []
        
        for case in self.body["cases"]:

            _jump_to_stmnt = []

            for match in case["case"]:
                # compile current match
                match.compile()
                
                # compile condition
                self.condition.compile()

                self.jump_equal(...)
                _jump_to_stmnt.append(self.peekLast())
            
            self.absolute_jump(...)
            _jump_next = self.peekLast()
            
            # jump here if matches
            for matched in _jump_to_stmnt:
                matched.kwargs["target"] = self.getLine()

            # case statement
            case["stmnt"].compile()

            self.jump_to(...)
            _jump_end.append(self.peekLast())

            # jump to next case|else
            _jump_next.kwargs["target"] = self.getLine()
        
        if  self.body["else"]:
            self.body["else"].compile()
        
        for _jump in _jump_end:
            _jump.kwargs["target"] = self.getLine()
        

# OK!!! | COMPILED | PASSED
class VarNode(CSAst):
    """ Holds var declairation

        Parameters
        ----------
        _assignments : tuple
    """

    @match_typing
    def __init__(self, _assignments:tuple):
        super().__init__()
        self.assignments = _assignments
    
    def compile(self):
        for assignment in self.assignments:
            # compile value
            if  not assignment["val"]:
                self.push_constant(CSObject.new_nulltype("null"))
            else:
                assignment["val"].compile()
            
            _var = assignment["var"]

            # ================= RECORDING PURPOSE
            # ===================================
            # check existence
            if  ST.islocal(_var.token):
                return show_error("variable \"%s\" is already defined" % _var.token, _var)
            
            # make|get slot
            _s = assignment["val"].offset()["_slot"]         \
                if isinstance(assignment["val"], Assignable) \
                else VM.makeSlot()

            # save var_name
            ST.insert(_var.token, _slot = _s)

            # ============ MEMORY SETTING PURPOSE
            # ===================================
            # store name
            self.store_name(_var, _s)


class LetNode(CSAst):
    """ Holds let declairation

        Parameters
        ----------
        _assignments : tuple
    """

    @match_typing
    def __init__(self, _assignments:tuple):
        super().__init__()
        self.assignments = _assignments
    
    def compile(self):
        for assignment in self.assignments:
            # compile value
            if  not assignment["val"]:
                self.push_constant(CSObject.new_nulltype("null"))
            else:
                assignment["val"].compile()
            
            # push name
            self.push_constant(CSObject.new_string(assignment["var"].token))


# OK!!! | COMPILED | PASSED
class PrintNode(CSAst):
    """ Handles print statement

        Parameters
        ----------
        _expr_list : list
    """

    @match_typing
    def __init__(self, _expr_list:tuple):
        super().__init__()
        self.expressions = _expr_list

    
    def compile(self):
        # compile right most
        for node in self.expressions[::-1]:
            node.compile()
        
        # print opcode
        self.print_object(len(self.expressions))



# OK!!! | COMPILED | PASSED
class ExprStmntNode(CSAst):

    @match_typing
    def __init__(self, _expr:CSAst):
        super().__init__()
        self.expr = _expr
    
    def compile(self):
        # compile expr
        self.expr.compile()

        # pop code
        self.pop_top()
