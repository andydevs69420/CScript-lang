from csAst import AccessNode, AllocDeallocNode, ArrayNode, AugmentedAssignment, BinaryExprNode, BlockNode, BoolNode, CallNode, ClassNode, CompareExprNode, DoWileNode, EqualityExprNode, ExprStmntNode, IfStatementNode, IntegerNode, DoubleNode, LetNode, LogicalExprNode, ModuleNode, NullNode, ObjectNode, PrintNode, ReferenceNode, SimpleAssignment, StaticAccessNode, StringNode, SubscriptNode, SwitchNode, TernaryNode, UnaryExprNode, VarNode, WhileNode
from cstoken import TokenType, CSToken
from cslexer import CSLexer
from errortoken import show_error
from strongtyping.strong_typing import match_typing

class CSParser(object):

    @match_typing
    def __init__(self, _fpath:str, _scode:str):
        self.fpath:str = _fpath 
        self.scode:str = _scode
        self.lexer:CSLexer = CSLexer(self.fpath, self.scode)
        self.token:CSToken = self.lexer.getNext()

    @match_typing
    def eat(self, _token:TokenType|str):
        """ consumes current token

            Parametrs
            --------
            _token : TokenType|str

            Returns
            -------
            None
        """
        if  self.token.matches(_token):
            self.token = self.lexer.getNext()
            return
        
        # error
        _unpack = (
            self.token.token,
            _token if type(_token) == str else _token.name.lower()
        )
        return show_error("unexpected token \"%s\". Did you mean \"%s\"?" % _unpack, self.token)


    def parse(self):

        def invalid_keyword():
            if  self.token.matches(TokenType.IDENTIFIER) and \
                (self.token.matches("import"  ) or \
                 self.token.matches("class"   ) or \
                 self.token.matches("function") or \
                 self.token.matches("return"  ) or \
                 self.token.matches("assert"  ) or \
                 self.token.matches("throw"   ) or \
                 self.token.matches("if"      ) or \
                 self.token.matches("else"    ) or \
                 self.token.matches("do"      ) or \
                 self.token.matches("while"   ) or \
                 self.token.matches("switch"  ) or \
                 self.token.matches("var"     ) or \
                 self.token.matches("let"     ) or \
                 self.token.matches("print"   )):
                # throw
                return show_error("unexpected keyword for expresion \"%s\"" % self.token.token, self.token)
            
            return None
        
        
        def boolean():
            _bool = self.token
            if  not (_bool.matches("true") or _bool.matches("false")):
                return None
            
            # eat type
            self.eat(_bool.ttype)

            # return as bool
            return BoolNode(_bool)
        
        def nulltype():
            _null = self.token
            if  not _null.matches("null"):
                return None
            
            # eat type
            self.eat(_null.ttype)

            # return as null
            return NullNode(_null)
        
        def raw_identifier():
            invalid_keyword()
            
            _idn = self.token
            if  not _idn.matches(TokenType.IDENTIFIER):
                return show_error("expected identifier, got \"%s\"" % _idn.token, _idn)

            # eat type
            self.eat(_idn.ttype)

            # return as raw
            return _idn

        def identifier():
            invalid_keyword()

            _idn = self.token
            if  not _idn.matches(TokenType.IDENTIFIER):
                return None
            
            # eat type
            self.eat(_idn.ttype)

            # return as ref
            return ReferenceNode(_idn)
   
        def integer():
            _int = self.token
            if  not _int.matches(TokenType.INTEGER):
                return None
            
            # eat type
            self.eat(_int.ttype)

            # return as int
            return IntegerNode(_int)

        def double():
            _flt = self.token
            if  not _flt.matches(TokenType.DOUBLE):
                return None
            
            # eat type
            self.eat(_flt.ttype)

            # return as double
            return DoubleNode(_flt)

        def string():
            _str = self.token
            if  not _str.matches(TokenType.STRING):
                return None
            
            # eat type
            self.eat(_str.ttype)

            # return as str
            return StringNode(_str)
            

        def atom():

            invalid_keyword()

            if  self.token.matches(TokenType.IDENTIFIER) and \
                (self.token.matches("true" ) or \
                 self.token.matches("false")):
                return boolean()
            elif  self.token.matches("null"):
                return nulltype()
            elif  self.token.matches(TokenType.IDENTIFIER):
                return identifier()
            elif self.token.matches(TokenType.INTEGER):
                return integer()
            elif self.token.matches(TokenType.DOUBLE):
                return double()
            elif self.token.matches(TokenType.STRING):
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
            while self.token.matches(","):

                _opt = self.token
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
            while self.token.matches(","):

                _opt = self.token
                self.eat(_opt.ttype)

                _attrN = single_attribute()
                if  not _attrN:
                    return show_error("unexpected end of list", _opt)
                
                _elements.append(_attrN)
            
            return tuple(_elements)
        
        def single_attribute():
            if  not self.token.matches(TokenType.IDENTIFIER):
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

            if  self.token.matches("["):
                return array()
            elif self.token.matches("{"):
                return csobject()

            return _node
        
        def call_args():
            return csobject_element()

        def member_access():
            _node = other_type()
            if not _node: return _node

            while self.token.matches("->") or \
                  self.token.matches("::") or \
                  self.token.matches("[" ) or \
                  self.token.matches("(" ):

                if  self.token.matches("->"):
                    # eat type
                    self.eat(self.token.ttype)

                    # attrib
                    _attr = raw_identifier()

                    _node = AccessNode(_node, _attr)

                elif self.token.matches("::"):
                    # eat type
                    self.eat(self.token.ttype)

                    # attrib
                    _attr = raw_identifier()
                    
                    _node = StaticAccessNode(_node, _attr)

                elif self.token.matches("["):
                    _o = self.token
                    self.eat("[")

                    _expr = non_nullable_expression()

                    _c = self.token
                    self.eat("]")

                    _subscript = CSToken(TokenType.DYNAMIC_OPERATOR)
                    _subscript.token = "[...]"
                    # xAxis
                    _subscript.xS = _o.xS
                    _subscript.xE = _c.xE
                    # yAxis
                    _subscript.yS = _o.yS
                    _subscript.yE = _c.yE
                
                    _node = SubscriptNode(_node, _expr, _subscript)

                elif self.token.matches("("):
                    _o = self.token
                    self.eat("(")

                    _args = call_args()

                    _c = self.token
                    self.eat(")")

                    _call = CSToken(TokenType.DYNAMIC_OPERATOR)
                    _call.token = "(...)"
                    # xAxis
                    _call.xS = _o.xS
                    _call.xE = _c.xE
                    # yAxis
                    _call.yS = _o.yS
                    _call.yE = _c.yE

                    _node = CallNode(_node, _args, _call)

            return _node
        
        def parenthesis():
            if  self.token.matches("("):
                self.eat("(")
                _expr = non_nullable_expression()
                self.eat(")")
                return _expr
            
            return member_access()
        
        def ternary():
            _node = parenthesis()
            if not _node: return _node

            if not self.token.matches("?"):
                return _node
            
            # eat operator
            self.eat("?")

            _tv = non_nullable_expression()

            self.eat(":")

            _fv = non_nullable_expression()

            # return as ternary
            return TernaryNode(_node, _tv, _fv)
        
        def unary_op():

            if  self.token.matches("del") or \
                self.token.matches("new"):

                _opt = self.token
                self.eat(_opt.ttype)

                _exp = unary_op()

                return AllocDeallocNode(_opt, _exp)

            if  self.token.matches("~") or \
                self.token.matches("!") or \
                self.token.matches("+") or \
                self.token.matches("-"):
                
                _opt = self.token
                self.eat(_opt.ttype)

                _exp = unary_op()
                
                # return as unary expr
                return UnaryExprNode(_opt, _exp)

            return ternary()
        
        
        def power():
            _node = unary_op()
            if not _node: return _node
            
            while self.token.matches("^^"):
                
                _opt = self.token
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
            
            while self.token.matches("*") or \
                  self.token.matches("/") or \
                  self.token.matches("%"):
                
                _opt = self.token
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

            while self.token.matches("+") or \
                  self.token.matches("-"):
                
                _opt = self.token
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

            while self.token.matches("<<") or \
                  self.token.matches(">>"):
                
                _opt = self.token
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

            while self.token.matches("<" ) or \
                  self.token.matches("<=") or \
                  self.token.matches(">" ) or \
                  self.token.matches(">="):
                
                _opt = self.token
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

            while self.token.matches("==" ) or \
                  self.token.matches("!="):
                
                _opt = self.token
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

            while self.token.matches("&") or \
                  self.token.matches("^") or \
                  self.token.matches("|"):
                
                _opt = self.token
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

            while self.token.matches("&&") or \
                  self.token.matches("||"):
                
                _opt = self.token
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

            while self.token.matches("="):
                
                _opt = self.token
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

            while self.token.matches("^^=") or\
                  self.token.matches("*=" ) or\
                  self.token.matches("/=" ) or\
                  self.token.matches("%=" ) or\
                  self.token.matches("+=" ) or\
                  self.token.matches("-=" ) or\
                  self.token.matches("<<=") or\
                  self.token.matches(">>=") or\
                  self.token.matches("&=" ) or\
                  self.token.matches("^=" ) or\
                  self.token.matches("|=" ):
                
                _opt = self.token
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
                return show_error("expression is required, got \"%s\"" % self.token.token, self.token)
            
            return _exp
        
        # ===================== STATEMENT
        # ===============================

        def class_dec():
            self.eat("class")

            # class name
            _name = raw_identifier()

            _base = None

            if  self.token.matches(":"):
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

            while self.token.matches(","):

                _opt = self.token
                self.eat(_opt.ttype)

                _idN = class_member_pair()

                if  not _idN:
                    return show_error("unexpected end of list", _opt)
                
                _member.append(_idN)

            self.eat("}")

            return tuple(_member)
        

        def class_member_pair():
            if  not self.token.matches(TokenType.IDENTIFIER):
                return None
            
            _name  = raw_identifier()

            self.eat(":")

            _value = class_member_expression()

            return ({"name": _name, "value": _value})

        
        def class_member_expression():
            if  self.token.matches("function"):
                return function_expression()

            return non_nullable_expression()

        
        def function_expression():
            self.eat("function")

            self.eat("(")

            self.eat(")")


        def if_stmnt():
            self.eat("if")

            self.eat("(")

            _condition = non_nullable_expression()

            self.eat(")")

            _statement = compound_stmnt()

            if  not self.token.matches("else"):
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
            return DoWileNode(_condition, _body)


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

            while self.token.matches("case"):

                self.eat("case")

                _caseN = switch_matches()

                self.eat(":")

                _statement = compound_stmnt()

                _body["cases"].append({
                    "case": _caseN,
                    "stmnt": _statement
                })
            
            if  self.token.matches("else"):
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
            if  self.token.matches("class"):
                return class_dec()
            elif self.token.matches("if"):
                return if_stmnt()
            elif self.token.matches("do"):
                return do_while_stmnt()
            elif self.token.matches("while"):
                return while_stmnt()
            elif self.token.matches("switch"):
                return switch_stmnt()
            elif self.token.matches("{"):
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

            while self.token.matches(","):

                self.eat(",")

                _assignment.append(
                    assignment_pair()
                )

            return tuple(_assignment)
        

        def assignment_pair():
            # identifier
            _id = raw_identifier()
            
            if not self.token.matches("="):
                return {{"var": _id, "val": None }}
            
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
            if  self.token.matches("var"):
                return var_stmnt()
            elif self.token.matches("let"):
                return let_stmnt()
            elif self.token.matches("print"):
                return print_stmnt()
            return expression_stmnt()
        


        def module():
            _nodes = []
            
            while not self.token.matches(TokenType.ENDOFFILE):
                _nodes.append(compound_stmnt())
            
            # return as module
            return ModuleNode(tuple(_nodes))

        return module()
