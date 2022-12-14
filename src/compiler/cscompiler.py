


# .
from .cseval import CSEval
from .blockcompiler import BlockCompiler
from .csxcompileerror import CSXCompileError

# utility
from utility import ExpressionType

# grammar
from grammarp import CSParser

# csbuiltins
from csbuiltins import csrawcode

TYPE= "type"


class RawBlock(BlockCompiler): pass
class RawBlock(BlockCompiler):
    """ Raw block parser
    """

    def __init__(self):
        super().__init__()
        self.while_stack = []
        self.break_stack = []
        self.modname     = ...


    """ EXPRESSION AREA OF COMPILING
    """

    # variable
    def cvariable(self, _node:dict):
        self.push_name(_node["var"], _node["loc"])

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
    
    # function expr
    def cfuncexpr(self, _node:dict):
        _fcom = FunctionCompiler(_node)
        self.push_code(_fcom.compile())

        # # push arg count
        self.push_integer(len(_node["params"]))

        # push func name
        self.push_string(_node["name"])

        # build function
        self.make_function()


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
    
    # allocation
    def callocation(self, _node:dict):

        for child in _node["arguments"][::-1]:
            self.visit(child)

        # compile right
        self.visit(_node["right-hand"])
        
        # unary new
        self.unary_op("new", len(_node["arguments"]), _node["loc"])
    
    # static member access
    def cstaticmember(self, _node:dict):
        # visit left
        self.visit(_node["left"])

        # add get attrib
        self.get_static(_node["member"], _node["loc"])

    # member access
    def cmember(self, _node:dict):
        # visit left
        self.visit(_node["left"])

        # add get attrib
        self.get_attrib(_node["member"], _node["loc"])
    
    # subscript
    def csubscript(self, _node:dict):
        # visit index|member
        self.visit(_node["index"])

        # visit left
        self.visit(_node["left"])

        # add subscript
        self.binary_subscript(_node["loc"])
    
    # call
    def ccall(self, _node:dict):
        _arguments = _node["args"]

        # compile reverse
        for _expr in _arguments[::-1]:
            # compile right-most
            self.visit(_expr)

        # push calling object
        match  _node["left"][TYPE]:
            
            case ExpressionType.MEMBER:
                # visit left
                self.visit(_node["left"]["left"])

                # add get attrib
                self.get_method(_node["left"]["member"], _node["left"]["loc"])

                # add call
                self.call_method(len(_arguments), _node["loc"])

            case _:
                self.visit(_node["left"])

                # add call
                self.call(len(_arguments), _node["loc"])
    
    # postfix expr
    def cpostfix(self, _node:dict):
        """ Compile the same way as unary op
        """
        # compile left hand
        self.visit(_node["left"])

        match _node["opt"]:
            case "++"|"--":
                match _node["left"][TYPE]:
                    case ExpressionType.VARIABLE |\
                         ExpressionType.MEMBER   |\
                         ExpressionType.SUBSCRIPT:
                        pass
                    case _:
                        return CSXCompileError.csx_Error(
                            ("SemanticError: invalid left-hand of operator (%s) !" % _node["opt"])
                            + "\n"
                            + _node["loc"]
                        )
        # add operator
        self.postfix_op(_node["opt"], _node["loc"])

    # unary expr
    def cunary(self, _node:dict):
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

        # compile right hand
        self.visit(_node["right"])

        match _node["opt"]:
            case "++"|"--":
                match _node["right"][TYPE]:
                    case ExpressionType.VARIABLE |\
                         ExpressionType.MEMBER   |\
                         ExpressionType.SUBSCRIPT:
                        pass
                    case _:
                        return CSXCompileError.csx_Error(
                            ("SemanticError: invalid right-hand of operator (%s) !" % _node["opt"])
                            + "\n"
                            + _node["loc"]
                        )
        # add operator
        self.unary_op(_node["opt"], 0, _node["loc"])

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
                self.binary_pow(_operator, _loc=_node["loc"])
            case '*':
                self.binary_mul(_operator, _loc=_node["loc"])
            case '/':
                self.binary_div(_operator, _loc=_node["loc"])
            case '%':
                self.binary_mod(_operator, _loc=_node["loc"])
            case '+':
                self.binary_add(_operator, _loc=_node["loc"])
            case '-':
                self.binary_sub(_operator, _loc=_node["loc"])
            # bitwise
            case "<<":
                self.binary_lshift(_operator, _loc=_node["loc"])
            case ">>":
                self.binary_rshift(_operator, _loc=_node["loc"])
            case '&':
                self.binary_and(_operator, _loc=_node["loc"])
            case '^':
                self.binary_xor(_operator, _loc=_node["loc"])
            case '|':
                self.binary_or (_operator, _loc=_node["loc"])
            case _:
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
        self.compare_op(_operator, _loc=_node["loc"])
    
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
                self.store_name(_node["left"]["var"], _node["left"]["loc"])
            
            # static member 
            case ExpressionType.STATIC_MEMBER:
                # compile owner
                self.visit(_node["left"]["left" ])

                # set attibute
                self.set_static(_node["left"]["member"], _node["left"]["loc"])

            # member assignment
            case ExpressionType.MEMBER:
                # compile owner
                self.visit(_node["left"]["left" ])

                # set attibute
                self.set_attrib(_node["left"]["member"], _node["left"]["loc"])

            # index|member assignment
            case ExpressionType.SUBSCRIPT:
                # compile index|member
                self.visit(_node["left"]["index"])

                # compile owner
                self.visit(_node["left"]["left" ])

                # add subscript
                self.set_subscript(_node["loc"])
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
                self.inplace_pow(_operator, _loc=_node["loc"])
            case "*=":
                self.inplace_mul(_operator, _loc=_node["loc"])
            case "/=":
                self.inplace_div(_operator, _loc=_node["loc"])
            case "%=":
                self.inplace_mod(_operator, _loc=_node["loc"])
            case "+=":
                self.inplace_add(_operator, _loc=_node["loc"])
            case "-=":
                self.inplace_sub(_operator, _loc=_node["loc"])
            case "<<=":
                self.inplace_lshift(_operator, _loc=_node["loc"])
            case ">>=":
                self.inplace_rshift(_operator, _loc=_node["loc"])
            case "&=":
                self.inplace_and(_operator, _loc=_node["loc"])
            case "^=":
                self.inplace_xor(_operator, _loc=_node["loc"])
            case "|=":
                self.inplace_or(_operator, _loc=_node["loc"])
            case _:
                raise NotImplementedError("unimplemented operator '%s'" % _operator)

        # duplicate top
        self.dup_top()
        
        match _node["left"][TYPE]:
            # variable assignment
            case ExpressionType.VARIABLE:
                self.store_name(_node["left"]["var"], _node["left"]["loc"])

            # static member 
            case ExpressionType.STATIC_MEMBER:
                # compile owner
                self.visit(_node["left"]["left" ])

                # set attibute
                self.set_static(_node["left"]["member"], _node["left"]["loc"])
                
            # member assignment
            case ExpressionType.MEMBER:
                # compile owner
                self.visit(_node["left"]["left" ])

                # set attibute
                self.set_attrib(_node["left"]["member"], _node["left"]["loc"])

            # index|member assignment
            case ExpressionType.SUBSCRIPT:
                # compile index|member
                self.visit(_node["left"]["index"])

                # compile owner
                self.visit(_node["left"]["left" ])

                # add subscript
                self.set_subscript(_node["loc"])

            # error
            case _:
                CSXCompileError.csx_Error("SemanticError: can't assign left-hand of operator '%s'!" % _node["opt"])


    """ STATEMENT AREA OF COMPILING
    """
    # class
    def cclass(self, _node:dict):
        _ccom = ClassCompiler(_node)
        self.push_code(_ccom.compile())

        # # push arg count
        self.push_integer(0)

        # push func name
        self.push_string(_node["name"])

        # build function
        self.make_function()

        # call csrawcode before
        # saving value
        self.call(0, _node["loc"])

        # store class
        self.make_var(_node["name"], _node["loc"])
    
    # class var
    def cvaldec(self, _node:dict):
        for _dec in _node["assignments"]:

            _value = _dec["val"]
            if  not _value:
                self.push_null(None)
            else:
                self.visit(_value)

            
            _varia = _dec["var"]

            self.dup_top()

            # make local
            self.make_local(_varia, _node["loc"])

            # attribute name
            self.push_string(_varia)

    
    # class func
    def cclassfunc(self, _node:dict):
        _fcom = FunctionCompiler(_node)
        self.push_code(_fcom.compile())

        # # push arg count
        self.push_integer(len(_node["params"]))

        # push func name
        self.push_string(_node["name"])

        # build function
        self.make_function()
        
        # attribute name
        self.push_string(_node["name"])

    # func
    def cfunc(self, _node:dict):
        _fcom = FunctionCompiler(_node)
        self.push_code(_fcom.compile())

        # # push arg count
        self.push_integer(len(_node["params"]))

        # push func name
        self.push_string(_node["name"])

        # build function
        self.make_function()

        # store func
        self.make_var(_node["name"], _node["loc"])
    
    # if statement
    def cifstmnt(self, _node:dict):
        _condition = self.evaluate(_node["condition"])
    
        if  _condition != ...:
            if  _condition:
                # compile if true
                self.visit(_node["statement"])
            else:
                if  _node["else"]:
                    # compile else
                    self.visit(_node["else"])
            return
            #####
        
        # compile whole statement

        match _node["condition"][TYPE]:

            case ExpressionType.LOGICAL_EXPR:
                _lhs = _node["condition"]["left" ]
                _rhs = _node["condition"]["right"]


                # compile rhs
                self.visit(_rhs)

                if  _node["condition"]["opt"] == "&&":
                    self.pop_jump_if_false(...)
                else:
                    self.pop_jump_if_true(...)
                
                _jump_t0 = self.peekLast()
                
                # compile lhs
                self.visit(_lhs)

                # jump lhs and rhs evaluates 
                # to false
                self.pop_jump_if_false(...)
                _jump_t1 = self.peekLast()


                # jump here if logical or
                # and rhs is satisfiable
                if  _node["condition"]["opt"] == "||":
                    _jump_t0.kwargs["target"] = self.getLine()

                # compile statement
                self.visit(_node["statement"])

                # jump to end if
                if  _node["else"]:
                    self.jump_to(...)
                    _jump_t2 = self.peekLast()

                if  _node["condition"]["opt"] == "&&":
                    _jump_t0.kwargs["target"] = self.getLine()

                # set jump target 1 here if 
                # condition is false
                _jump_t1.kwargs["target"] = self.getLine()

                # compile else
                if  _node["else"]:
                    self.visit(_node["else"])
                
                # set jump target 2 here
                # denotes finished control
                if  _node["else"]:
                    _jump_t2.kwargs["target"] = self.getLine()

            case _:

                # compile condition
                self.visit(_node["condition"])

                # jump to "else" if false
                self.pop_jump_if_false(...)
                _jump_t0 = self.peekLast()

                # compile statement
                self.visit(_node["statement"])

                # jump to end if
                self.jump_to(...)
                _jump_t1 = self.peekLast()

                # set jump target 0 here if false
                _jump_t0.kwargs["target"] = self.getLine()

                if  _node["else"]:
                    # compile else
                    self.visit(_node["else"])
                
                # set jump target 1 to end if
                _jump_t1.kwargs["target"] = self.getLine()

    # switch
    def cswitch(self, _node:dict):
        _to_stm = []
        _to_end = []
        for each_case in _node["body"]["cases"]:
            
            for each_match in each_case["case"]:

                # compile condition
                self.visit(_node["condition"])

                # compile
                self.visit(each_match)

                self.jump_equal(...)
                _to_stm.append(self.peekLast())
            
            # jump to next case
            self.jump_to(...)
            _next_case = self.peekLast()

            # jump here if equal
            for target in _to_stm:
                target.kwargs["target"] = self.getLine()
            
            # remove previous
            _to_stm.clear()

            # compile statemnt
            self.visit(each_case["stmnt"])

            # add jump to end
            self.jump_to(...)
            _to_end.append(self.peekLast())

            # prepare for next or end
            _next_case.kwargs["target"] = self.getLine()

        if  _node["body"]["else"]:
            # compile else
            self.visit(_node["body"]["else"])
        
        for end_switch in _to_end:
            end_switch.kwargs["target"] = self.getLine()

    # for statement
    def cfor(self, _node:dict):
        # compile initialize

        _break_count = len(self.break_stack)
        
        if  (_node["cond"]!= None and _node["cond"][TYPE]) and _node["cond"][TYPE] == ExpressionType.LOGICAL_EXPR:
            if  _node["init"]:
                self.visit(_node["init"])

            _begin_for = self.getLine()
            self.while_stack.append(_begin_for)

            # compile condition
            _jump_t0 = None
            if  _node["cond"]:
                self.visit(_node["cond"])
            
            # compile body
            self.visit(_node["body"])

            # compile inc/dec
            if  _node["inc_dec"]:
                self.visit(_node["inc_dec"])

            # repeat for
            self.absolute_jump(_begin_for)

            if  _jump_t0:
                # end for
                _jump_t0.kwargs["target"] == self.getLine()

            # end while
            self.while_stack.pop()

        else:
            
            if  _node["init"]:
                self.visit(_node["init"])

            _begin_for = self.getLine()
            self.while_stack.append(_begin_for)

            # compile condition
            _jump_t0 = None
            if  _node["cond"]:
                self.visit(_node["cond"])

                self.pop_jump_if_false(...)
                _jump_t0 = self.peekLast()
            
            
            # compile body
            self.visit(_node["body"])

            # compile inc/dec
            if  _node["inc_dec"]:
                self.visit(_node["inc_dec"])

            # repeat for
            self.absolute_jump(_begin_for)

            if  _jump_t0:
                # end for
                _jump_t0.kwargs["target"] = self.getLine()
        
            # end while
            self.while_stack.pop()
        

        for _r in range(len(self.break_stack) - _break_count):
            _break_jump = self.break_stack.pop()
            _break_jump.kwargs["target"] = self.getLine()

    # while statement
    def cwhile(self, _node:dict):
        _condition = self.evaluate(_node["condition"])
    
        if  _condition != ...:
            if  not _condition:
                # do not compile
                self.no_operation()
                return
            #####
        
        # compile whole statement
        # start

        _break_count = len(self.break_stack)

        _begin_while = self.getLine()
        self.while_stack.append(_begin_while)
        
        match _node["condition"][TYPE]:

            case ExpressionType.LOGICAL_EXPR:
                
                _lhs = _node["condition"]["left" ]
                _rhs = _node["condition"]["right"]

                # compile rhs
                self.visit(_rhs)

                if  _node["condition"]["opt"] == "&&":
                    self.pop_jump_if_false(...)
                else:
                    self.pop_jump_if_true(...)
                
                _jump_t0 = self.peekLast()
                
                # compile lhs
                self.visit(_lhs)

                # jump lhs and rhs evaluates 
                # to false
                self.pop_jump_if_false(...)
                _jump_t1 = self.peekLast()


                # jump here if logical or
                # and rhs is satisfiable
                if  _node["condition"]["opt"] == "||":
                    _jump_t0.kwargs["target"] = self.getLine()

                # compile statement
                self.visit(_node["body"])

                # repeat top
                self.absolute_jump(_begin_while)

                if  _node["condition"]["opt"] == "&&":
                    _jump_t0.kwargs["target"] = self.getLine()

                # set jump target 1 here if 
                # condition is false
                _jump_t1.kwargs["target"] = self.getLine()


            case _:

                # compile condition
                self.visit(_node["condition"])

                # jump lhs and rhs evaluates 
                # to false
                self.pop_jump_if_false(...)
                _jump_t0 = self.peekLast()

                # compile statement
                self.visit(_node["body"])

                # repeat top
                self.absolute_jump(_begin_while)

                # jump to end while
                _jump_t0.kwargs["target"] = self.getLine()

        self.while_stack.pop()
        
        for _r in range(len(self.break_stack) - _break_count):
            _break_jump = self.break_stack.pop()
            _break_jump.kwargs["target"] = self.getLine()

    # do while
    def cdowhile(self, _node:dict):
        _condition = self.evaluate(_node["condition"])
    
        if  _condition != ...:
            if  not _condition:
                # do not compile
                self.no_operation()
                return
            #####
        
        # compile whole statement
        # start

        _break_count = len(self.break_stack)

        _begin_while = self.getLine()
        self.while_stack.append(_begin_while)

        match _node["condition"][TYPE]:

            case ExpressionType.LOGICAL_EXPR:
                
                _lhs = _node["condition"]["left" ]
                _rhs = _node["condition"]["right"]

                # compile body
                self.visit(_node["body"])
                
                # compile rhs
                self.visit(_rhs)

                if  _node["condition"]["opt"] == "&&":
                    self.pop_jump_if_false(...)
                else:
                    self.pop_jump_if_true(...)
                
                _jump_t0 = self.peekLast()
                
                # compile lhs
                self.visit(_lhs)

                # jump lhs and rhs evaluates 
                # to false
                self.pop_jump_if_false(...)
                _jump_t1 = self.peekLast()


                # jump here if logical or
                # and rhs is satisfiable
                if  _node["condition"]["opt"] == "||":
                    _jump_t0.kwargs["target"] = self.getLine()

                # compile statement
                self.visit(_node["body"])

                # repeat top
                self.absolute_jump(_begin_while)

                if  _node["condition"]["opt"] == "&&":
                    _jump_t0.kwargs["target"] = self.getLine()

                # set jump target 1 here if 
                # condition is false
                _jump_t1.kwargs["target"] = self.getLine()
            
            case _:
                
                # compile body
                self.visit(_node["body"])

                # compile condition
                self.visit(_node["condition"])

                # jump to end do while
                self.pop_jump_if_false(...)
                _jump_t0 = self.peekLast()

                # repeat top
                self.absolute_jump(_begin_while)

                # jump here if false
                _jump_t0.kwargs["target"] = self.getLine()

        self.while_stack.pop()
        
        for _r in range(len(self.break_stack) - _break_count):
            _break_jump = self.break_stack.pop()
            _break_jump.kwargs["target"] = self.getLine()


    # try/except
    def ctryexcept(self, _node:dict):
        # setup
        self.setup_try(...)
        _jump_if_error = self.peekLast()

        # visit try block
        self.visit(_node["try_block"])

        # pop try block
        # pop before no error
        self.pop_try()

        # end try/except
        self.jump_to(...)
        _jump_end = self.peekLast()
        
        # make except block
        self.new_block()

        # jump here if error
        _jump_if_error.kwargs["target"] = self.getLine()

        # pop try block
        # pop before except
        self.pop_try()

        # store local
        self.make_local(_node["except_param"], _node["loc"])

        # compile except
        self.visit(_node["except_block"])

        # pop except block
        self.end_block()

        # jump end or finally
        _jump_end.kwargs["target"] = self.getLine()

        if  _node["finally_block"]:
            # compile finally
            self.visit(_node["finally_block"])

    # block
    def cblock(self, _node:dict):
        # new for scoping
        self.new_block()

        for _stmnt in _node["block"]:
            # compile statement
            self.visit(_stmnt)
        
        # end scope
        self.end_block()

    # var dec
    def cvardec(self, _node:dict):
        for _dec in _node["assignments"]:

            _value = _dec["val"]
            if  not _value:
                self.push_null(None)
            else:
                self.visit(_value)

            # attribute name
            _varia = _dec["var"]
            self.make_var(_varia, _node["loc"])
    
    # let dec
    def cletdec(self, _node:dict):
        for _dec in _node["assignments"]:

            _value = _dec["val"]
            if  not _value:
                self.push_null(None)
            else:
                self.visit(_value)

            # attribute name
            _varia = _dec["var"]
            self.make_local(_varia, _node["loc"])
    
    # throw
    def cthrow(self, _node:dict):
        # compile expression
        self.visit(_node["expression"])

        # add throw
        self.throw_error(_node["loc"])
    
    # assert
    def cassert(self, _node:dict):
        # compile condition
        self.visit(_node["condition"])

        # continue if not error
        self.pop_jump_if_true(...)
        _jump_t0 = self.peekLast()

        # compile message
        self.visit(_node["message"])

        # add throw
        self.throw_error(_loc=_node["loc"])

        # jump here if not error!
        _jump_t0.kwargs["target"] = self.getLine()
    
    #  continue statement
    def ccontinue(self, _node:dict):
        # add jump
        self.absolute_jump(self.while_stack[-1])

    #  break statement
    def cbreak(self, _node:dict):
        # add jump
        self.jump_to(...)

        self.break_stack.append(self.peekLast())

    # return
    def creturn(self, _node:dict):
        
        if  _node["expression"]:
            self.visit(_node["expression"])
        else:
            self.push_null(None)
        
        self.return_op()

    
    # print
    def cprint(self, _node:dict):
        for _expr in _node["expressions"][::-1]:
            # compile right-most
            self.visit(_expr)
        
        # add print
        self.print_object(len(_node["expressions"]))

    # empty statement node
    def cempty(self, _node:dict):
        # no oepration
        self.no_operation()

    # expression node
    def cexpression(self, _node:dict):
        # compile expression
        self.visit(_node["expression"])

        # add pop
        self.pop_top()

    # module node
    def cmodule(self, _node:dict):
        # module name
        self.modname = _node["modname"]

        for _child in _node["children"]:
            self.visit(_child)
        
        # for i in self.getInsntructions():
        #     print(i)



class CSCompiler(RawBlock, CSEval):pass
class CSCompiler(RawBlock, CSEval):

    def __init__(self, _fpath:str, _scode:str):
        super().__init__()
        self.fpath:str = _fpath 
        self.scode:str = _scode
        self.csparser = CSParser(self.fpath, self.scode)

    def compile(self):
        _root = self.csparser.parse()

        # compile root
        self.visit(_root)

        # add return
        self.push_integer(69420)

        # add return
        self.return_op()

        _raw = csrawcode(self.fpath, self.getInsntructions())

        assert len(self.while_stack) == 0, "not all while has terminated!!!"
        assert len(self.break_stack) == 0, "not all break has terminated!!!"

        # return raw code
        return _raw
    
    

class ClassCompiler(RawBlock, CSEval):
    """ Class compiler
    """

    def __init__(self, _node:dict):
        super().__init__()
        self.decl = 0
        self.node = _node
    
    def cvaldec(self, _node: dict):
        super().cvaldec(_node)
        # hack!
        self.decl += len(_node["assignments"])
    
    def cclassfunc(self, _node: dict):
        self.decl += 1
        return super().cclassfunc(_node)
        
    
    def compile(self):
        # ========== body|
        # ===============|
        for _child in self.node["body"]:
            # compile child
            self.visit(_child)

        # ==== push class|
        # ===============|
        self.push_string(self.node["name"])
        
        # === build class|
        # ===============|
        self.make_class(self.decl)

        # ======== return|
        # ===============|
        self.return_op()

        return csrawcode(self.node["name"], self.getInsntructions())


class FunctionCompiler(RawBlock, CSEval):
    """ Function/Method compiler
    """

    def __init__(self, _node:dict):
        super().__init__()
        self.node = _node
    
    def compile(self):
        # ==== parameters|
        # ===============|
        _offset = 0
        for _param in self.node["params"]:
            # compile parameters
            self.make_param(_param, _offset, self.node["loc"])
            _offset += 1
    
        # ========== body|
        # ===============|
        for _child in self.node["body"]:
            self.visit(_child)
        
        #  default return|
        # ===============|
        self.push_null(None)

        # ======== return|
        # ===============|
        self.return_op()

        return csrawcode(self.node["name"], self.getInsntructions())
