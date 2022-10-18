from astnode import *
from cslexer import (
    TokenType, 
    CSToken  , 
    CSLexer  , 
    show_error
)

class CSParser(object):
    """ CSParser

        Parameters
        ----------
        _fpath : str
        _scode : str
    """

    def __init__(self, _fpath:str, _scode:str):
        self.fpath:str = _fpath 
        self.scode:str = _scode
        self.cslexer   = CSLexer(self.fpath, self.scode)
        self.cstoken   = self.cslexer.getNext()

    def eat(self, _token):
        """ Consumes current token

            Parameters
            ----------
            _token : TokenType|str

            Returns
            -------
            None
        """
        if  self.cstoken.matches(_token):
            self.cstoken = self.cslexer.getNext()
            return
        
        # error
        _unpack = (
            self.cstoken.token,
            _token if type(_token) == str else _token.name.lower()
        )
        return show_error("unexpected token \"%s\". Did you mean \"%s\"?" % _unpack, self.cstoken)


    def parse(self):

        def invalid_keyword():
            if  self.cstoken.matches(TokenType.IDENTIFIER) and \
                (self.cstoken.matches("import"  ) or \
                 self.cstoken.matches("class"   ) or \
                 self.cstoken.matches("function") or \
                 self.cstoken.matches("return"  ) or \
                 self.cstoken.matches("assert"  ) or \
                 self.cstoken.matches("throw"   ) or \
                 self.cstoken.matches("if"      ) or \
                 self.cstoken.matches("else"    ) or \
                 self.cstoken.matches("do"      ) or \
                 self.cstoken.matches("while"   ) or \
                 self.cstoken.matches("switch"  ) or \
                 self.cstoken.matches("var"     ) or \
                 self.cstoken.matches("let"     ) or \
                 self.cstoken.matches("print"   )):
                # throw
                return show_error("unexpected keyword for expresion \"%s\"" % self.cstoken.token, self.cstoken)
            
            return None
        
        
        def boolean():
            _bool = self.cstoken
            if  not (_bool.matches("true") or _bool.matches("false")):
                return None
            
            # eat type
            self.eat(_bool.ttype)

            # return as bool
            return BoolNode(_bool)
        
        def nulltype():
            _null = self.cstoken
            if  not _null.matches("null"):
                return None
            
            # eat type
            self.eat(_null.ttype)

            # return as null
            return NullNode(_null)
        
        def raw_identifier():
            invalid_keyword()
            
            _idn = self.cstoken
            if  not _idn.matches(TokenType.IDENTIFIER):
                return show_error("expected identifier, got \"%s\"" % _idn.token, _idn)

            # eat type
            self.eat(_idn.ttype)

            # return as raw
            return _idn

        def identifier():
            invalid_keyword()

            _idn = self.cstoken
            if  not _idn.matches(TokenType.IDENTIFIER):
                return None
            
            # eat type
            self.eat(_idn.ttype)

            # return as ref
            return ReferenceNode(_idn)
   
        def integer():
            _int = self.cstoken
            if  not _int.matches(TokenType.INTEGER):
                return None
            
            # eat type
            self.eat(_int.ttype)

            # return as int
            return IntegerNode(_int)

        def double():
            _flt = self.cstoken
            if  not _flt.matches(TokenType.DOUBLE):
                return None
            
            # eat type
            self.eat(_flt.ttype)

            # return as double
            return DoubleNode(_flt)

        def string():
            _str = self.cstoken
            if  not _str.matches(TokenType.STRING):
                return None
            
            # eat type
            self.eat(_str.ttype)

            # return as str
            return StringNode(_str)
            

        def atom():

            invalid_keyword()

            if  self.cstoken.matches(TokenType.IDENTIFIER) and \
                (self.cstoken.matches("true" ) or \
                 self.cstoken.matches("false")):
                return boolean()
            elif  self.cstoken.matches("null"):
                return nulltype()
            elif  self.cstoken.matches(TokenType.IDENTIFIER):
                return identifier()
            elif self.cstoken.matches(TokenType.INTEGER):
                return integer()
            elif self.cstoken.matches(TokenType.DOUBLE):
                return double()
            elif self.cstoken.matches(TokenType.STRING):
                return string()
            
            return None

        
        def array():
            self.eat("[")

            _el = array_elements()

            self.eat("]")

            # return as array
            return ArrayNode(_el)
        
        def array_elements():
            _elements = []

            _el0 = nullable_expression()
            if not _el0: return tuple(_elements)

            _elements.append(_el0)
            while self.cstoken.matches(","):

                _opt = self.cstoken
                self.eat(_opt.ttype)

                _elN = nullable_expression()
                if  not _elN:
                    return show_error("unexpected end of list", _opt)
                
                _elements.append(_elN)

            return tuple(_elements)
        
        def csobject():
            self.eat("{")

            _elements = csobject_element()

            self.eat("}")

            # return as object
            return ObjectNode(_elements)
        
        def csobject_element():
            _elements = []

            _attr0 = single_attribute()
            if  not _attr0:
                return tuple(_elements)
            
            _elements.append(_attr0)
            while self.cstoken.matches(","):

                _opt = self.cstoken
                self.eat(_opt.ttype)

                _attrN = single_attribute()
                if  not _attrN:
                    return show_error("unexpected end of list", _opt)
                
                _elements.append(_attrN)
            
            return tuple(_elements)
        
        def single_attribute():
            if  not self.cstoken.matches(TokenType.IDENTIFIER):
                return None
            
            _key = raw_identifier()

            # eat operator
            self.eat(":")

            _val = non_nullable_expression()

            return ({
                "key": _key,
                "val": _val,
            })

        
        def other_type():
            _node = atom()
            if _node: return _node

            if  self.cstoken.matches("["):
                return array()
            elif self.cstoken.matches("{"):
                return csobject()

            return _node
        
        def call_args():
            return array_elements()

        def member_access():
            _o = self.cstoken
            _node = other_type()
            if not _node: return _node

            while self.cstoken.matches("->") or \
                  self.cstoken.matches("::") or \
                  self.cstoken.matches("[" ) or \
                  self.cstoken.matches("(" ):

                if  self.cstoken.matches("->"):
                    # eat type
                    self.eat(self.cstoken.ttype)

                    # attrib
                    _attr = raw_identifier()

                    _node = AccessNode(_node, _attr)

                elif self.cstoken.matches("["):
                    self.eat("[")

                    _expr = non_nullable_expression()

                    _c = self.cstoken
                    self.eat("]")

                    _subscript = CSToken(TokenType.DYNAMIC_OPERATOR)
                    _subscript.fsrce = self.fpath
                    _subscript.token = "[...]"
                    # xAxis
                    _subscript.xS = _o.xS
                    _subscript.xE = _c.xE
                    # yAxis
                    _subscript.yS = _o.yS
                    _subscript.yE = _c.yE
                    _subscript.addTrace(self)
                
                    _node = SubscriptNode(_node, _expr, _subscript)

                elif self.cstoken.matches("("):
                    self.eat("(")

                    _args = call_args()

                    _c = self.cstoken
                    self.eat(")")

                    _call = CSToken(TokenType.DYNAMIC_OPERATOR)
                    _call.fsrce = self.fpath
                    _call.token = "(...)"
                    # xAxis
                    _call.xS = _o.xS
                    _call.xE = _c.xE
                    # yAxis
                    _call.yS = _o.yS
                    _call.yE = _c.yE
                    _call.addTrace(self)

                    _node = CallNode(_node, _args, _call)

            return _node
        
        def parenthesis():
            if  self.cstoken.matches("("):
                self.eat("(")
                _expr = non_nullable_expression()
                self.eat(")")
                return _expr
            
            return member_access()
        
        def ternary():
            _node = parenthesis()
            if not _node: return _node

            if not self.cstoken.matches("?"):
                return _node
            
            # eat operator
            self.eat("?")

            _tv = non_nullable_expression()

            self.eat(":")

            _fv = non_nullable_expression()

            # return as ternary
            return TernaryNode(_node, _tv, _fv)
        
        def unary_op():

            if  self.cstoken.matches("del") or \
                self.cstoken.matches("new"):

                _opt = self.cstoken
                self.eat(_opt.ttype)

                _exp = unary_op()

                return AllocDeallocNode(_opt, _exp)

            if  self.cstoken.matches("~") or \
                self.cstoken.matches("!") or \
                self.cstoken.matches("+") or \
                self.cstoken.matches("-"):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _exp = unary_op()
                
                # return as unary expr
                return UnaryExprNode(_opt, _exp)

            return ternary()
        
        
        def power():
            _node = unary_op()
            if not _node: return _node
            
            while self.cstoken.matches("^^"):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = unary_op()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)
            
                _node = BinaryExprNode(
                    _opt, _node, _rhs
                )

            # return node
            return _node

        def multiplicative():
            _node = power()
            if not _node: return _node
            
            while self.cstoken.matches("*") or \
                  self.cstoken.matches("/") or \
                  self.cstoken.matches("%"):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = power()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)
            
                _node = BinaryExprNode(
                    _opt, _node, _rhs
                )

            # return node
            return _node

        def addetive():
            _node = multiplicative()
            if not _node: return _node

            while self.cstoken.matches("+") or \
                  self.cstoken.matches("-"):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = multiplicative()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)
            
                _node = BinaryExprNode(
                    _opt, _node, _rhs
                )

            # return node
            return _node
        
        def shift():
            _node = addetive()
            if not _node: return _node

            while self.cstoken.matches("<<") or \
                  self.cstoken.matches(">>"):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = addetive()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)
            
                _node = BinaryExprNode(
                    _opt, _node, _rhs
                )

            # return node
            return _node
        
        def relational():
            _node = shift()
            if not _node: return _node

            while self.cstoken.matches("<" ) or \
                  self.cstoken.matches("<=") or \
                  self.cstoken.matches(">" ) or \
                  self.cstoken.matches(">="):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = shift()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)
            
                _node = CompareExprNode(
                    _opt, _node, _rhs
                )

            # return node
            return _node
        
        def equality():
            _node = relational()
            if not _node: return _node

            while self.cstoken.matches("==" ) or \
                  self.cstoken.matches("!="):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = relational()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)
            
                _node = EqualityExprNode(
                    _opt, _node, _rhs
                )

            # return node
            return _node
        
        def bitwise():
            _node = equality()
            if not _node: return _node

            while self.cstoken.matches("&") or \
                  self.cstoken.matches("^") or \
                  self.cstoken.matches("|"):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = equality()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)
            
                _node = BinaryExprNode(
                    _opt, _node, _rhs
                )

            # return node
            return _node
        
        def logical():
            _node = bitwise()
            if not _node: return _node

            while self.cstoken.matches("&&") or \
                  self.cstoken.matches("||"):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = bitwise()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)
            
                _node = LogicalExprNode(
                    _opt, _node, _rhs
                )

            # return node
            return _node
    
        
        def simple_assignment():
            _node = logical()
            if not _node: return _node

            while self.cstoken.matches("="):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = logical()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)

                _node = SimpleAssignment(
                    _opt, _node, _rhs
                )

            return _node
        
        def augmented_assignment():
            _node = simple_assignment()
            if not _node: return _node

            while self.cstoken.matches("^^=") or\
                  self.cstoken.matches("*=" ) or\
                  self.cstoken.matches("/=" ) or\
                  self.cstoken.matches("%=" ) or\
                  self.cstoken.matches("+=" ) or\
                  self.cstoken.matches("-=" ) or\
                  self.cstoken.matches("<<=") or\
                  self.cstoken.matches(">>=") or\
                  self.cstoken.matches("&=" ) or\
                  self.cstoken.matches("^=" ) or\
                  self.cstoken.matches("|=" ):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = logical()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)

                _node = AugmentedAssignment(
                    _opt, _node, _rhs
                )

            return _node

        
        def nullable_expression():
            return augmented_assignment()
        
        def non_nullable_expression():
            _exp = nullable_expression()
            if  not _exp:
                # error
                return show_error("expression is required, got \"%s\"" % self.cstoken.token, self.cstoken)
            
            return _exp
        
        # ===================== STATEMENT
        # ===============================

        def class_dec():
            self.eat("class")

            # class name
            _name = raw_identifier()

            _base = None

            if  self.cstoken.matches(":"):
                self.eat(":")
                _base = raw_identifier()

            # body containing member
            _member = class_body()

            # return as class
            return ClassNode(_name, _base, _member)
        

        def class_body():
            _member = []

            self.eat("{")

            _id0 = class_member_pair()
            if  not _id0:
                return tuple(_member)
            
            _member.append(_id0)

            while self.cstoken.matches(","):

                _opt = self.cstoken
                self.eat(_opt.ttype)

                _idN = class_member_pair()

                if  not _idN:
                    return show_error("unexpected end of list", _opt)
                
                _member.append(_idN)

            self.eat("}")

            return tuple(_member)
        

        def class_member_pair():
            if  not self.cstoken.matches(TokenType.IDENTIFIER):
                return None
            
            _name  = raw_identifier()

            self.eat(":")

            _value = class_member_expression()

            return ({"name": _name, "value": _value})

        
        def class_member_expression():
            if  self.cstoken.matches("function"):
                return function_expression()

            return non_nullable_expression()

        
        def function_expression():
            self.eat("function")

            self.eat("(")

            self.eat(")")

            _func_body = block_stmnt()
        

        def function_dec():
            self.eat("function")

            _func_name = raw_identifier()

            self.eat("(")

            _parameters = function_parameters()

            self.eat(")")

            _func_body = block_stmnt()

            # return as function
            return FunctionNode(_func_name, _parameters, _func_body)
        

        # multi-purpose
        def function_parameters():
            _parameters = []

            _paramN = valid_parameters()

            if  not _paramN:
                return tuple(_parameters)

            _parameters.append(_paramN)
            
            while (self.cstoken.matches(",")):

                _opt = self.cstoken
                self.eat(_opt.ttype)

                _paramN = valid_parameters()

                if  not _paramN:
                    return show_error("unexpected end of list", _opt)

                _parameters.append(_paramN)

            return tuple(_parameters)

            
        def valid_parameters():
            if  not self.cstoken.matches(TokenType.IDENTIFIER):
                return None
            
            return raw_identifier()


        def if_stmnt():
            self.eat("if")

            self.eat("(")

            _condition = non_nullable_expression()

            self.eat(")")

            _statement = compound_stmnt()

            if  not self.cstoken.matches("else"):
                # return as if
                return IfStatementNode(_condition, _statement, None)

            # with else
            self.eat("else")

            _else_stmnt = compound_stmnt()

            # return as if|else node
            return IfStatementNode(_condition, _statement, _else_stmnt)

        def while_stmnt():
            self.eat("while")
            
            self.eat("(")

            _condition = non_nullable_expression()

            self.eat(")")

            _statement = compound_stmnt()

            # return as while
            return WhileNode(_condition, _statement)
        

        def do_while_stmnt():
            self.eat("do")

            _body = compound_stmnt()

            self.eat("while")

            self.eat("(")

            _condition = non_nullable_expression()

            self.eat(")")

            # return as do while
            return DoWhileNode(_condition, _body)


        def switch_stmnt():
            self.eat("switch")

            self.eat("(")

            _condition = non_nullable_expression()

            self.eat(")")

            _body = switch_body()

            # return as switch
            return SwitchNode(_condition, _body)
        

        def switch_body():
            _body = ({
                "cases": [],
                "else": None
            })
            self.eat("{")

            while self.cstoken.matches("case"):

                self.eat("case")

                _caseN = switch_matches()

                self.eat(":")

                _statement = compound_stmnt()

                _body["cases"].append({
                    "case": _caseN,
                    "stmnt": _statement
                })
            
            if  self.cstoken.matches("else"):
                self.eat("else")
                self.eat(":")

                _body["else"] = compound_stmnt()

            self.eat("}")

            return _body
        
        def switch_matches():
            return array_elements()

        def block_stmnt():
            _statements = []
            self.eat("{")

            _stmntN = compound_stmnt()
            while _stmntN:
                _statements.append(_stmntN)
                _stmntN = compound_stmnt()

            self.eat("}")

            # return as block node
            return BlockNode(tuple(_statements))
        

        def compound_stmnt():
            if  self.cstoken.matches("class"):
                return class_dec()
            elif self.cstoken.matches("function"):
                return function_dec()
            elif self.cstoken.matches("if"):
                return if_stmnt()
            elif self.cstoken.matches("do"):
                return do_while_stmnt()
            elif self.cstoken.matches("while"):
                return while_stmnt()
            elif self.cstoken.matches("switch"):
                return switch_stmnt()
            elif self.cstoken.matches("{"):
                return block_stmnt()
            
            return simple_stmnt()
        

        def var_stmnt():
            self.eat("var")

            _assignments = assignment_list()

            self.eat(";")

            # return as var node
            return VarNode(_assignments)


        def let_stmnt():
            self.eat("let")

            _assignments = assignment_list()

            self.eat(";")

            # retu as let node
            return LetNode(_assignments)

        
        def assignment_list():
            _assignment = []

            _assignment.append(
                assignment_pair()
            )

            while self.cstoken.matches(","):

                self.eat(",")

                _assignment.append(
                    assignment_pair()
                )

            return tuple(_assignment)
        

        def assignment_pair():
            # identifier
            _id = raw_identifier()
            
            if not self.cstoken.matches("="):
                return ({"var": _id, "val": None })
            
            # eat operator
            self.eat("=")

            _val = non_nullable_expression()

            return ({"var": _id, "val": _val })

        
        def print_stmnt():
            self.eat("print")
            self.eat(":")

            _expr_list = array_elements()

            self.eat(";")

            # return as print node
            return PrintNode(_expr_list)


        def expression_stmnt():
            _expr = nullable_expression()
            if not _expr: return _expr

            # eat
            self.eat(";")

            # return as expr stmnt
            return ExprStmntNode(_expr)
        


        def simple_stmnt():
            if  self.cstoken.matches("var"):
                return var_stmnt()
            elif self.cstoken.matches("let"):
                return let_stmnt()
            elif self.cstoken.matches("print"):
                return print_stmnt()
            return expression_stmnt()
        


        def module():
            _nodes = []
            
            while not self.cstoken.matches(TokenType.ENDOFFILE):
                _nodes.append(compound_stmnt())
            
            # return as module
            return ModuleNode(tuple(_nodes))

        return module()
