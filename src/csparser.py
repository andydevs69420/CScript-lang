
from lib2to3.pgen2 import token
from csAst import AccessNode, AllocDeallocNode, ArrayNode, BinaryExprNode, BoolNode, CallNode, IntegerNode, DoubleNode, NullNode, ObjectNode, ReferenceNode, StaticAccessNode, StringNode, SubscriptNode, TernaryNode, UnaryExprNode
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
        return show_error(self, "unexpected token \"%s\". Did you mean \"%s\"?" % _unpack, self.token)


    def parse(self):

        def invalid_keyword():
            if  self.token.matches(TokenType.IDENTIFIER) and \
                (self.token.matches("import"  ) or \
                 self.token.matches("class"   ) or \
                 self.token.matches("function") or \
                 self.token.matches("return"  ) or \
                 self.token.matches("assert"  ) or \
                 self.token.matches("throw"   ) or \
                 self.token.matches("var"     ) or \
                 self.token.matches("let"     )):
                # throw
                return show_error(self, "unexpected keyword for expresion \"%s\"" % self.token.token, self.token)
            
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
                return show_error(self, "expected identifier, got \"%s\"" % _idn.token, _idn)

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

            if  self.token.matches("true" ) or \
                self.token.matches("false"):
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

            _el = array_element()

            self.eat("]")

            # return as array
            return ArrayNode(_el)
        
        def array_element():
            _elements = []

            _el0 = nullable_expression()
            if not _el0: return tuple(_elements)

            _elements.append(_el0)
            while self.token.matches(","):

                _opt = self.token
                self.eat(_opt.ttype)

                _elN = nullable_expression()
                if  not _elN:
                    return show_error(self, "unexpected end of list", _opt)
                
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
                    return show_error(self, "unexpected end of list", _opt)
                
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
                    self.eat("[")

                    _expr = non_nullable_expression()

                    self.eat("]")

                    _node = SubscriptNode(_node, _expr)

                elif self.token.matches("("):
                    self.eat("(")

                    _args = call_args()

                    self.eat(")")

                    _node = CallNode(_node, _args)

            return _node
        
        def ternary():
            _node = member_access()
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

        def parenthesis():
            if  self.token.matches("("):
                self.eat("(")
                _expr = non_nullable_expression()
                self.eat(")")
                return _expr
            
            return ternary()
        
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

            return parenthesis()
        
        
        def power():
            _node = unary_op()
            if not _node: return _node
            
            while self.token.matches("^^"):
                
                _opt = self.token
                self.eat(_opt.ttype)

                _rhs = unary_op()
                if  not _rhs:
                    return show_error(self, "missing right-hand expression \"%s\"" % _opt.token, _opt)
            
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
                    return show_error(self, "missing right-hand expression \"%s\"" % _opt.token, _opt)
            
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
                    return show_error(self, "missing right-hand expression \"%s\"" % _opt.token, _opt)
            
                _node = BinaryExprNode(
                    _opt, _node, _rhs
                )

            # return node
            return _node
        
        def nullable_expression():
            return addetive()
        
        def non_nullable_expression():
            _exp = nullable_expression()
            if  not _exp:
                # error
                return show_error(self, "expression is required, got \"%s\"" % self.token.token, self.token)
            
            return _exp

        return addetive()
