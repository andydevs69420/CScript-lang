from enum import Enum
from astnode import *
from cslexer import (
    TokenType, 
    CSToken  , 
    CSLexer  , 
    show_error
)



class ContextType(Enum):
    GLOBAL = 0x00
    LOCAL  = 0x01
    FUNCTION = 0x02
    LOOP = 0x03

class ContextUtils(object):

    def __init__(self):
        self.contextStack:list[ContextType] = []

    def enter(self, _context_type:ContextType):
        self.contextStack.append(_context_type)

    def leave(self):
        self.contextStack.pop()
    
    def bind(self, _context_type:ContextType, _immediate=False):
        _binded = False
        if  _immediate:
            _binded = _context_type == self.contextStack[-1]
        else:
            # check if in stack
            _binded = _context_type in self.contextStack

        if  not _binded:
            return show_error("invalid \"%s\" outside %s scope" % (self.cstoken.token, _context_type.name.lower()), self.cstoken)

class CSParser(ContextUtils):
    """ CSParser

        Parameters
        ----------
        _fpath : str
        _scode : str
    """

    def __init__(self, _fpath:str, _scode:str):
        super().__init__()
        self.fpath:str = _fpath 
        self.scode:str = _scode
        self.cslexer   = CSLexer(self.fpath, self.scode)
        self.cstoken   = self.cslexer.getNext()

    def eat(self, _token, _ttype=None):
        """ Consumes current token

            Parameters
            ----------
            _token : TokenType|str

            Returns
            -------
            None
        """
        if  self.cstoken.matches(_token):
            if  _ttype:
                if  self.cstoken.matches(_ttype):
                    self.cstoken = self.cslexer.getNext()
                    return
            else:
                self.cstoken = self.cslexer.getNext()
                return
        
        # error
        _unpack = (
            self.cstoken.ttype.name.lower(),
            self.cstoken.token,
            _ttype.name.lower() if _ttype else "symbol",
            _token if type(_token) == str else _token.name.lower()
        )
        return show_error("unexpected %s \"%s\". Did you mean %s \"%s\"?" % _unpack, self.cstoken)


    def parse(self):

        def invalid_keyword():
            if  self.cstoken.matches(TokenType.IDENTIFIER) and \
                (self.cstoken.matches("import"  ) or \
                 self.cstoken.matches("from"    ) or \
                 self.cstoken.matches("class"   ) or \
                 self.cstoken.matches("return"  ) or \
                 self.cstoken.matches("assert"  ) or \
                 self.cstoken.matches("throw"   ) or \
                 self.cstoken.matches("if"      ) or \
                 self.cstoken.matches("else"    ) or \
                 self.cstoken.matches("do"      ) or \
                 self.cstoken.matches("while"   ) or \
                 self.cstoken.matches("switch"  ) or \
                 self.cstoken.matches("try"     ) or \
                 self.cstoken.matches("except"  ) or \
                 self.cstoken.matches("finally" ) or \
                 self.cstoken.matches("var"     ) or \
                 self.cstoken.matches("let"     ) or \
                 self.cstoken.matches("print"   )):
                # throw
                return show_error("unexpected keyword for expresion \"%s\"" % self.cstoken.token, self.cstoken)
            
            return None

        def invalid_raw_identifier():
            if  self.cstoken.matches(TokenType.IDENTIFIER) and \
                (self.cstoken.matches("false"  ) or \
                 self.cstoken.matches("true"   ) or \
                 self.cstoken.matches("null"   ) or \
                 self.cstoken.matches("func"   )):
                # throw
                return show_error("unexpected keyword for identifier \"%s\"" % self.cstoken.token, self.cstoken)
            
            return None
        
        
        # bool: true|false
        def boolean():
            _bool = self.cstoken
            if  not (_bool.matches("true") or _bool.matches("false")):
                return None
            
            # eat type
            self.eat(_bool.ttype)

            # return as bool
            return BoolNode(_bool)
        
        # null:
        def nulltype():
            _null = self.cstoken
            if  not _null.matches("null"):
                return None
            
            # eat type
            self.eat(_null.ttype)

            # return as null
            return NullNode(_null)
        
        # function(){...}
        def function_expression():
            self.enter(ContextType.FUNCTION)

            self.eat("func", TokenType.IDENTIFIER)

            self.eat("(", TokenType.OPERATOR)

            _parameters = function_parameters()

            self.eat(")", TokenType.OPERATOR)

            _func_body = function_body()

            self.leave()

            # return as headless function
            return HeadlessFunctionNode(_parameters, _func_body)
        
        # cstoken: identifier
        def raw_identifier():
            invalid_raw_identifier()
            
            _idn = self.cstoken
            if  not _idn.matches(TokenType.IDENTIFIER):
                return show_error("expected identifier, got \"%s\"" % _idn.token, _idn)

            # eat type
            self.eat(_idn.ttype)

            # return as raw
            return _idn

        # identifier
        def identifier():
            invalid_keyword()

            _idn = self.cstoken
            if  not _idn.matches(TokenType.IDENTIFIER):
                return None
            
            # eat type
            self.eat(_idn.ttype)

            # return as ref
            return ReferenceNode(_idn)

        # ineteger
        def integer():
            _int = self.cstoken
            if  not _int.matches(TokenType.INTEGER):
                return None
            
            # eat type
            self.eat(_int.ttype)

            # return as int
            return IntegerNode(_int)

        # float|double
        def double():
            _flt = self.cstoken
            if  not _flt.matches(TokenType.DOUBLE):
                return None
            
            # eat type
            self.eat(_flt.ttype)

            # return as double
            return DoubleNode(_flt)



        # string
        def string():
            _str = self.cstoken

            # eat type
            self.eat(_str.ttype)

            # return as str
            return StringNode(_str)
        
        # atom: boolean
        # | nulltype
        # | function_expression
        # | identifier
        # | integer
        # | double
        # | string
        # | null(epsilon)
        # ;
        def atom():
            invalid_keyword()

            if  self.cstoken.matches(TokenType.IDENTIFIER)  and \
                (self.cstoken.matches("true" ) or \
                 self.cstoken.matches("false")):
                return boolean()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and \
                self.cstoken.matches("null"):
                return nulltype()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and \
                self.cstoken.matches("func"):
                return function_expression()
            elif self.cstoken.matches(TokenType.IDENTIFIER):
                return identifier()
            elif self.cstoken.matches(TokenType.INTEGER):
                return integer()
            elif self.cstoken.matches(TokenType.DOUBLE):
                return double()
            elif self.cstoken.matches(TokenType.STRING):
                return string()
            
            return None

        # array: '[' array_elements ']'
        def array():
            self.eat("[", TokenType.OPERATOR)

            _el = array_elements()

            self.eat("]", TokenType.OPERATOR)

            # return as array
            return ArrayNode(_el)
        
        # multi-purpose: used in: ["call_args", "array", "switch_matches", "print_stmnt"]
        # array_elements: nullable_expression (',' non_nullable_expression)*;
        def array_elements():
            _elements = []

            _el0 = nullable_expression()
            if not _el0: return tuple(_elements)

            _elements.append(_el0)
            while self.cstoken.matches(TokenType.OPERATOR) and self.cstoken.matches(","):

                _opt = self.cstoken
                self.eat(_opt.ttype)

                _elN = nullable_expression()
                if  not _elN:
                    return show_error("unexpected end of list", _opt)
                
                _elements.append(_elN)

            return tuple(_elements)
        
        # csobject: '{' csobject_element '}';
        def csobject():
            self.eat("{", TokenType.OPERATOR)

            _elements = csobject_element()

            self.eat("}", TokenType.OPERATOR)

            # return as object
            return ObjectNode(_elements)
        
        # csobject_element: single_attribute*;
        def csobject_element():
            _elements = []

            _attr0 = single_attribute()
            if  not _attr0:
                return tuple(_elements)
            
            _elements.append(_attr0)
            while self.cstoken.matches(TokenType.OPERATOR) and self.cstoken.matches(","):

                _opt = self.cstoken
                self.eat(_opt.ttype)

                _attrN = single_attribute()
                if  not _attrN:
                    return show_error("unexpected end of list", _opt)
                
                _elements.append(_attrN)
            
            return tuple(_elements)
        
        # single_attribute: raw_identifier ':' non_nullable_expression ;
        def single_attribute():
            if  not self.cstoken.matches(TokenType.IDENTIFIER):
                return None
            
            _key = raw_identifier()

            # eat operator
            self.eat(":", TokenType.OPERATOR)

            _val = non_nullable_expression()

            return ({
                "key": _key,
                "val": _val,
            })
        
        # parethesis: '(' non_nullable_expression ')' | member_access
        def parenthesis():
            self.eat("(", TokenType.OPERATOR)

            _expr = non_nullable_expression()

            self.eat(")", TokenType.OPERATOR)

            return _expr
            
           

        # other_type: array | csobject;
        def other_type():
            _node = atom()
            if _node: return _node

            if  self.cstoken.matches(TokenType.OPERATOR)  and \
                self.cstoken.matches("["):
                return array()
            elif self.cstoken.matches(TokenType.OPERATOR) and \
                self.cstoken.matches("{"):
                return csobject()
            elif self.cstoken.matches(TokenType.OPERATOR) and \
                self.cstoken.matches("("):
                return parenthesis()

            return _node
        
        # allocation: "new" member_expression
        # | other_type
        # ;
        def allocation():
            if  self.cstoken.matches(TokenType.IDENTIFIER) and \
                self.cstoken.matches("new"):
                _unary_opt = self.cstoken
                self.eat(_unary_opt.ttype)

                _exp = member_access()

                return AllocDeallocNode(_unary_opt, _exp)
            
            return other_type()

        # member_access: other_type
        # | other_type->raw_identifier
        # | other_type '[' non_nullable_expression ']'
        # ;
        def member_access():
            _open = self.cstoken
            _node = allocation()
            if not _node: return _node

            while  self.cstoken.matches(TokenType.OPERATOR) and \
                  (self.cstoken.matches("->") or \
                   self.cstoken.matches("[" )):

                if  self.cstoken.matches("->"):
                    # eat type
                    self.eat("->", TokenType.OPERATOR)

                    # attrib
                    _attr = raw_identifier()

                    _node = AccessNode(_node, _attr)

                elif self.cstoken.matches("["):
                    self.eat("[", TokenType.OPERATOR)

                    _expr = non_nullable_expression()

                    _c = self.cstoken
                    self.eat("]", TokenType.OPERATOR)

                    _subscript = CSToken(TokenType.DYNAMIC_LOCATION)
                    _subscript.fsrce = self.fpath
                    _subscript.token = "[...]"
                    # xAxis
                    _subscript.xS = _open.xS
                    _subscript.xE = _c.xE
                    # yAxis
                    _subscript.yS = _open.yS
                    _subscript.yE = _c.yE
                    _subscript.addTrace(self)
                
                    _node = SubscriptNode(_node, _expr, _subscript)

            return _node
        
        # call_args: array_elements;
        # multi-purpose: used in: ["call_expresion", "allocation"]
        def call_args():
            return array_elements()
        
        # call_expression: other_type
        # | other_type->raw_identifier
        # | other_type '[' non_nullable_expression ']'
        # | other_type '(' call_args ')'
        # ;
        def call_expression():
            _open = self.cstoken
            _node = member_access()
            if not _node: return _node

            while  self.cstoken.matches(TokenType.OPERATOR) and \
                  (self.cstoken.matches("->") or \
                   self.cstoken.matches("[" ) or \
                   self.cstoken.matches("(" )):

                if  self.cstoken.matches("->"):
                    # eat type
                    self.eat("->", TokenType.OPERATOR)

                    # attrib
                    _attr = raw_identifier()

                    _node = AccessNode(_node, _attr)

                elif self.cstoken.matches("["):
                    self.eat("[", TokenType.OPERATOR)

                    _expr = non_nullable_expression()

                    _c = self.cstoken
                    self.eat("]", TokenType.OPERATOR)

                    _subscript = CSToken(TokenType.DYNAMIC_LOCATION)
                    _subscript.fsrce = self.fpath
                    _subscript.token = "[...]"
                    # xAxis
                    _subscript.xS = _open.xS
                    _subscript.xE = _c.xE
                    # yAxis
                    _subscript.yS = _open.yS
                    _subscript.yE = _c.yE
                    _subscript.addTrace(self)
                
                    _node = SubscriptNode(_node, _expr, _subscript)

                elif self.cstoken.matches("("):
                    self.eat("(", TokenType.OPERATOR)

                    _args = call_args()

                    _c = self.cstoken
                    self.eat(")", TokenType.OPERATOR)

                    _call = CSToken(TokenType.DYNAMIC_LOCATION)
                    _call.fsrce = self.fpath
                    _call.token = "(...)"
                    # xAxis
                    _call.xS = _open.xS
                    _call.xE = _c.xE
                    # yAxis
                    _call.yS = _open.yS
                    _call.yE = _c.yE
                    _call.addTrace(self)

                    _node = CallNode(_node, _args, _call)

            return _node
        
        # unary_op: ternary
        # | ('~' | '!' | '+' | '-') unary_op
        # ;
        def unary_op():

            if   self.cstoken.matches(TokenType.OPERATOR) and \
                (self.cstoken.matches("~") or \
                 self.cstoken.matches("!") or \
                 self.cstoken.matches("+") or \
                 self.cstoken.matches("-")):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _exp = unary_op()
                
                # return as unary expr
                return UnaryExprNode(_opt, _exp)

            return call_expression()
        
        # power: unary_op 
        # | unary_op "^^" unary_op
        # ;
        def power():
            _node = unary_op()
            if not _node: return _node
            
            while self.cstoken.matches(TokenType.OPERATOR) and self.cstoken.matches("^^"):
                
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

        # multiplicative: power
        # | power '*' power
        # | power '/' power
        # | power '%' power
        # ;
        def multiplicative():
            _node = power()
            if not _node: return _node
            
            while  self.cstoken.matches(TokenType.OPERATOR) and \
                  (self.cstoken.matches("*") or \
                   self.cstoken.matches("/") or \
                   self.cstoken.matches("%")):
                
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

        # addetive: multiplicative 
        # | multiplicative '+' multiplicative
        # | multiplicative '-' multiplicative
        # ;
        def addetive():
            _node = multiplicative()
            if not _node: return _node

            while  self.cstoken.matches(TokenType.OPERATOR) and \
                  (self.cstoken.matches("+") or \
                   self.cstoken.matches("-")):
                
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
        
        # shift: addetive
        # | addetive "<<" addetive
        # | addetive ">>" addetive
        # ;
        def shift():
            _node = addetive()
            if not _node: return _node

            while self.cstoken.matches(TokenType.OPERATOR) and \
                 (self.cstoken.matches("<<") or \
                  self.cstoken.matches(">>")):
                
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
        
        # relational: shift
        # | shift '<'  shift
        # | shift "<=" shift
        # | shift '>'  shift
        # | shift ">=" shift
        # ;
        def relational():
            _node = shift()
            if not _node: return _node

            while  self.cstoken.matches(TokenType.OPERATOR) and \
                  (self.cstoken.matches("<" ) or \
                   self.cstoken.matches("<=") or \
                   self.cstoken.matches(">" ) or \
                   self.cstoken.matches(">=")):
                
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
        
        # equality: relational
        # | relational "=="  relational
        # | relational "!=" relational
        # ;
        def equality():
            _node = relational()
            if not _node: return _node

            while  self.cstoken.matches(TokenType.OPERATOR) and \
                  (self.cstoken.matches("==") or \
                   self.cstoken.matches("!=")):
                
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
        
        # bitwise: equality
        # | equality '&' equality 
        # | equality '^' equality 
        # | equality '|' equality 
        # ;
        def bitwise():
            _node = equality()
            if not _node: return _node

            while  self.cstoken.matches(TokenType.OPERATOR) and \
                  (self.cstoken.matches("&") or \
                   self.cstoken.matches("^") or \
                   self.cstoken.matches("|")):
                
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
        
        # logical: bitwise
        # | bitwise "&&" bitwise
        # | bitwise "||" bitwise
        # ;
        def logical():
            _node = bitwise()
            if not _node: return _node

            while  self.cstoken.matches(TokenType.OPERATOR) and \
                  (self.cstoken.matches("&&") or \
                   self.cstoken.matches("||")):
                
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
        
        # ternary: parenthesis ('?'non_nullable_expression ':' non_nullable_expression)? 
        def ternary():
            _node = logical()
            if not _node: return _node

            if not (self.cstoken.matches(TokenType.OPERATOR) and self.cstoken.matches("?")):
                return _node
            
            # eat operator
            self.eat("?", TokenType.OPERATOR)

            _tv = non_nullable_expression()

            self.eat(":", TokenType.OPERATOR)

            _fv = non_nullable_expression()

            # return as ternary
            return TernaryNode(_node, _tv, _fv)
    
        # simple_assignment: logical
        # | logical '=' logical
        # ;
        def simple_assignment():
            _node = ternary()
            if not _node: return _node

            while self.cstoken.matches(TokenType.OPERATOR) and self.cstoken.matches("="):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = ternary()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)

                _node = SimpleAssignment(
                    _opt, _node, _rhs
                )

            return _node
        
        # augmented_assignment: simple_assignment
        # | simple_assignment "^^=" simple_assignment
        # | simple_assignment "*="  simple_assignment
        # | simple_assignment "/="  simple_assignment
        # | simple_assignment "%="  simple_assignment
        # | simple_assignment "+="  simple_assignment
        # | simple_assignment "-="  simple_assignment
        # | simple_assignment "<<="  simple_assignment
        # | simple_assignment ">>="  simple_assignment
        # | simple_assignment "&="  simple_assignment
        # | simple_assignment "^="  simple_assignment
        # | simple_assignment "|="  simple_assignment
        # ;
        def augmented_assignment():
            _node = simple_assignment()
            if not _node: return _node

            while self.cstoken.matches(TokenType.OPERATOR) and \
                 (self.cstoken.matches("^^=") or\
                  self.cstoken.matches("*=" ) or\
                  self.cstoken.matches("/=" ) or\
                  self.cstoken.matches("%=" ) or\
                  self.cstoken.matches("+=" ) or\
                  self.cstoken.matches("-=" ) or\
                  self.cstoken.matches("<<=") or\
                  self.cstoken.matches(">>=") or\
                  self.cstoken.matches("&=" ) or\
                  self.cstoken.matches("^=" ) or\
                  self.cstoken.matches("|=" )):
                
                _opt = self.cstoken
                self.eat(_opt.ttype)

                _rhs = logical()
                if  not _rhs:
                    return show_error("missing right-hand expression \"%s\"" % _opt.token, _opt)

                _node = AugmentedAssignment(
                    _opt, _node, _rhs
                )

            return _node

        # nullable_expression: augmented_assignment?;
        def nullable_expression():
            return augmented_assignment()

        # non_nullable_expression: nullable_expression;
        def non_nullable_expression():
            _exp = nullable_expression()
            if  not _exp:
                # error
                return show_error("expression is required, got \"%s\"" % self.cstoken.token, self.cstoken)
            
            return _exp
        
        # ===================== STATEMENT
        # ===============================

        # class declairation: "class" raw_identifier (':' raw_identifier)? class_body;
        def class_dec():
            self.bind(ContextType.GLOBAL, _immediate=True)
            self.eat("class", TokenType.IDENTIFIER)

            # class name
            _name = raw_identifier()

            _base = None

            if  (self.cstoken.matches(TokenType.OPERATOR) and self.cstoken.matches(":")):
                self.eat(":", TokenType.OPERATOR)
                _base = raw_identifier()

            # body containing member
            _member = class_body_init()

            # return as class
            return ClassNode(_name, _base, _member)
        
        # class_body_init: '{' class_body '}';
        def class_body_init():
            self.eat("{", TokenType.OPERATOR)

            _body = class_body()

            self.eat("}", TokenType.OPERATOR)

            return _body
        
        # class_body: class_member_pair* ;
        def class_body():
            _member = []

            _id0 = class_member_pair()
            if  not _id0:
                return tuple(_member)
            
            _member.append(_id0)

            while (self.cstoken.matches(TokenType.OPERATOR) and self.cstoken.matches(",")):

                _opt = self.cstoken
                self.eat(_opt.ttype)

                _idN = class_member_pair()

                if  not _idN:
                    return show_error("unexpected end of list", _opt)
                
                _member.append(_idN)

            return tuple(_member)
        
        # class_member_pair: raw_identifier ':' non_nullable_expression
        def class_member_pair():
            if  not self.cstoken.matches(TokenType.IDENTIFIER):
                return None
            
            _name  = raw_identifier()

            self.eat(":", TokenType.OPERATOR)

            _value = non_nullable_expression()

            return ({"name": _name, "value": _value})

        # function_dec: "func" raw_identifier '(' function_parameters ')' block_stmnt;
        def function_dec():
            self.bind(ContextType.GLOBAL, _immediate=True)

            self.enter(ContextType.FUNCTION)

            self.eat("func", TokenType.IDENTIFIER)

            _func_name = raw_identifier()

            self.eat("(", TokenType.OPERATOR)

            _parameters = function_parameters()

            self.eat(")", TokenType.OPERATOR)

            _func_body = function_body()

            self.leave()

            # return as function
            return FunctionNode(_func_name, _parameters, _func_body)
        

        # multi-purpose: used in: ["functin_dec", "function_expression"]
        def function_parameters():
            _parameters = []

            _paramN = valid_parameters()

            if  not _paramN:
                return tuple(_parameters)

            _parameters.append(_paramN)
            
            while self.cstoken.matches(TokenType.OPERATOR) and self.cstoken.matches(","):

                _opt = self.cstoken
                self.eat(_opt.ttype)

                _paramN = valid_parameters()

                if  not _paramN:
                    return show_error("unexpected end of list", _opt)

                _parameters.append(_paramN)

            return tuple(_parameters)

        # valid_parameters: raw_identifier
        def valid_parameters():
            if  not self.cstoken.matches(TokenType.IDENTIFIER):
                return None
            
            return raw_identifier()
        
        def function_body():
            _statements = []

            self.enter(ContextType.LOCAL)

            self.eat("{", TokenType.OPERATOR)

            _stmntN = compound_stmnt()
            while _stmntN:
                _statements.append(_stmntN)
                _stmntN = compound_stmnt()

            self.eat("}", TokenType.OPERATOR)

            self.leave()

            return tuple(_statements)

        # if_stmnt: "if" '(' non_nullable_expression ')' compound_stmnt ("else" compound_stmnt)?;
        def if_stmnt():
            self.eat("if", TokenType.IDENTIFIER)

            self.eat("(", TokenType.OPERATOR)

            _condition = non_nullable_expression()

            self.eat(")", TokenType.OPERATOR)

            _statement = compound_stmnt()

            if  not (self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("else")):
                # return as if
                return IfStatementNode(_condition, _statement, None)

            # with else
            self.eat("else", TokenType.IDENTIFIER)

            _else_stmnt = compound_stmnt()

            # return as if|else node
            return IfStatementNode(_condition, _statement, _else_stmnt)

        # while_stmnt: "while" '(' non_nullable_expression ')' compound_stmnt ;
        def while_stmnt():
            self.enter(ContextType.LOOP)

            self.eat("while", TokenType.IDENTIFIER)
            
            self.eat("(", TokenType.OPERATOR)

            _condition = non_nullable_expression()

            self.eat(")", TokenType.OPERATOR)

            _statement = compound_stmnt()

            self.leave()

            # return as while
            return WhileNode(_condition, _statement)
        
        # do_while_stmnt: "do" compound_stmnt "while" '(' non_nullable_expression ')';
        def do_while_stmnt():
            self.enter(ContextType.LOOP)

            self.eat("do", TokenType.IDENTIFIER)

            _body = compound_stmnt()

            self.eat("while", TokenType.IDENTIFIER)

            self.eat("(", TokenType.OPERATOR)

            _condition = non_nullable_expression()

            self.eat(")", TokenType.OPERATOR)

            self.leave()

            # return as do while
            return DoWhileNode(_condition, _body)

        # switch_stmnt: "switch" '(' non_nullable_expression ')' switch_body;
        def switch_stmnt():
            self.eat("switch", TokenType.IDENTIFIER)

            self.eat("(", TokenType.OPERATOR)

            _condition = non_nullable_expression()

            self.eat(")", TokenType.OPERATOR)

            _body = switch_body()

            # return as switch
            return SwitchNode(_condition, _body)
        
        # switch_body: '{' ("case" switch_matches ':' compound_stmnt)* ("else" ':' compound_stmnt)? '}'
        def switch_body():
            _body = ({
                "cases": [],
                "else": None
            })
            self.eat("{", TokenType.OPERATOR)

            while (self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("case")):

                self.eat("case", TokenType.IDENTIFIER)

                _caseN = switch_matches()

                self.eat(":", TokenType.OPERATOR)

                _statement = compound_stmnt()

                _body["cases"].append({
                    "case": _caseN,
                    "stmnt": _statement
                })
            
            if  (self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("else")):
                self.eat("else", TokenType.IDENTIFIER)
                self.eat(":", TokenType.OPERATOR)

                _body["else"] = compound_stmnt()

            self.eat("}", TokenType.OPERATOR)

            return _body
        
        # switch_matches: array_elements;
        def switch_matches():
            return array_elements()
        

        # try/except
        def try_except():
            self.eat("try", TokenType.IDENTIFIER)

            _try_body = block_stmnt()

            self.eat("except", TokenType.IDENTIFIER)

            self.eat("(", TokenType.OPERATOR)

            _parameter = raw_identifier()
            
            self.eat(")", TokenType.OPERATOR)

            _except_body = block_stmnt()
            

            _finally_body = None
            if  (self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("finally")):
                self.eat("finally", TokenType.IDENTIFIER)

                _finally_body = block_stmnt()
            
            # return as try/except node
            return TryExceptNode(_try_body, _parameter, _except_body, _finally_body)


        # block_stmnt: '{' compound_stmnt* '}';
        # multi-purpose: used in: ["function_expression"]
        def block_stmnt():
            _statements = []

            self.enter(ContextType.LOCAL)

            self.eat("{", TokenType.OPERATOR)

            _stmntN = compound_stmnt()
            while _stmntN:
                _statements.append(_stmntN)
                _stmntN = compound_stmnt()

            self.eat("}", TokenType.OPERATOR)

            self.leave()

            # return as block node
            return BlockNode(tuple(_statements))
        
        # compound_stmnt: class_dec
        # | function_dec
        # | if_stmnt
        # | do_while_stmnt
        # | while_stmnt
        # | switch_stmnt
        # | block_stmnt
        # | simple_stmnt
        # ;
        def compound_stmnt():
            if  self.cstoken.matches(TokenType.IDENTIFIER)  and self.cstoken.matches("class"):
                return class_dec()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("func"):
                return function_dec()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("if"):
                return if_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("do"):
                return do_while_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("while"):
                return while_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("switch"):
                return switch_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("try"):
                return try_except()
            elif self.cstoken.matches(TokenType.OPERATOR  ) and self.cstoken.matches("{"):
                return block_stmnt()
            
            return simple_stmnt()
        
        # import_stmnt: "import" "[" function_parameters "]" "from" string;
        def import_stmnt():
            self.bind(ContextType.GLOBAL, _immediate=True)

            self.eat("import", TokenType.IDENTIFIER)

            self.eat("[", TokenType.OPERATOR)

            _imports = function_parameters()

            self.eat("]", TokenType.OPERATOR)

            self.eat("from", TokenType.IDENTIFIER)

            # location
            _import_loc = self.cstoken
            _source = string()

            self.eat(";", TokenType.OPERATOR)

            return ImportNode(_imports, _source, _import_loc)


        # var_stmnt: "var" assignment_list;
        def var_stmnt():
            # ===== check context|
            # ===================|
            self.bind(ContextType.GLOBAL, _immediate=True)

            self.eat("var", TokenType.IDENTIFIER)

            _assignments = assignment_list()

            self.eat(";", TokenType.OPERATOR)

            # return as var node
            return VarNode(_assignments)

        # let_stmnt: "let" assignment_list;
        def let_stmnt():
            self.bind(ContextType.LOCAL, _immediate=True)

            self.eat("let", TokenType.IDENTIFIER)

            _assignments = assignment_list()

            self.eat(";", TokenType.OPERATOR)

            # retu as let node
            return LetNode(_assignments)

        # assignment_list: assignment_pair+;
        def assignment_list():
            _assignment = []

            _assignment.append(
                assignment_pair()
            )

            while self.cstoken.matches(TokenType.OPERATOR) and self.cstoken.matches(","):

                self.eat(",", TokenType.OPERATOR)

                _assignment.append(
                    assignment_pair()
                )

            return tuple(_assignment)
        
        # assignment_pair: raw_identifier ('=' non_nullable_epxression)? ;
        def assignment_pair():
            # identifier
            _id = raw_identifier()
            
            if not (self.cstoken.matches(TokenType.OPERATOR) and self.cstoken.matches("=")):
                return ({"var": _id, "val": None})
            
            # eat operator
            self.eat("=", TokenType.OPERATOR)

            _val = non_nullable_expression()

            return ({"var": _id, "val": _val })
        
        # throw_stmnt: "throw" non_nullable_expression ';' ;
        def throw_stmnt():
            _o = self.cstoken
            self.eat("throw", TokenType.IDENTIFIER)

            _expr = non_nullable_expression()

            _c = self.cstoken
            self.eat(";", TokenType.OPERATOR)

            _loc = CSToken(TokenType.DYNAMIC_LOCATION)
            _loc.fsrce = self.fpath
            _loc.token = "[...]"
            # xAxis
            _loc.xS = _o.xS
            _loc.xE = _c.xE - 1
            # yAxis
            _loc.yS = _o.yS
            _loc.yE = _c.yE
            _loc.addTrace(self)

            return ThrowNode(_expr, _loc)
        
        # assert_stmnt: "assert" non_nullable_expression ',' non_nullable_expression ';';
        def assert_stmnt():
            _o = self.cstoken
            self.eat("assert", TokenType.IDENTIFIER)

            _cond = non_nullable_expression()

            self.eat(",", TokenType.OPERATOR)

            _message = non_nullable_expression()

            _c = self.cstoken
            self.eat(";", TokenType.OPERATOR)

            _loc = CSToken(TokenType.DYNAMIC_LOCATION)
            _loc.fsrce = self.fpath
            _loc.token = "[...]"
            # xAxis
            _loc.xS = _o.xS
            _loc.xE = _c.xE - 1
            # yAxis
            _loc.yS = _o.yS
            _loc.yE = _c.yE
            _loc.addTrace(self)

            return AssertNode(_cond, _message, _loc)
        
        # break_stmnt: "break" ';';
        def break_stmnt():
            self.bind(ContextType.LOOP)

            self.eat("break", TokenType.IDENTIFIER)
            self.eat(";", TokenType.OPERATOR)

            return BreakNode()
        
        # continue_stmnt: "continue" ';';
        def continue_stmnt():
            self.bind(ContextType.LOOP)

            self.eat("continue", TokenType.IDENTIFIER)
            self.eat(";", TokenType.OPERATOR)

            return ContinueNode()

        # return_stmnt: "return" nullable_expression ';';
        def return_stmnt():
            self.bind(ContextType.FUNCTION)

            self.eat("return", TokenType.IDENTIFIER)

            _expr = nullable_expression()

            self.eat(";", TokenType.OPERATOR)

            return ReturnNode(_expr)
        
        # yes! print is a statement here!
        # print_stmnt: "print" ':' array_elements ';';
        def print_stmnt():
            self.eat("print", TokenType.IDENTIFIER)
            self.eat(":", TokenType.OPERATOR)

            _expr_list = array_elements()

            self.eat(";", TokenType.OPERATOR)

            # return as print node
            return PrintNode(_expr_list)

        # expression_stmnt: (nullable_expression ';')? ;
        def expression_stmnt():
            _expr = nullable_expression()
            if not _expr: return _expr

            # eat
            self.eat(";", TokenType.OPERATOR)

            # return as expr stmnt
            return ExprStmntNode(_expr)
        

        # simple_stmnt: var_stmnt
        # | let_stmnt
        # | return_stmnt
        # | print_stmnt
        # | expression_stmnt
        # ;
        def simple_stmnt():
            if  self.cstoken.matches(TokenType.IDENTIFIER ) and self.cstoken.matches("import"):
                return import_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER ) and self.cstoken.matches("var"):
                return var_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("let"):
                return let_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("throw"):
                return throw_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("assert"):
                return assert_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("break"):
                return break_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("continue"):
                return continue_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("return"):
                return return_stmnt()
            elif self.cstoken.matches(TokenType.IDENTIFIER) and self.cstoken.matches("print"):
                return print_stmnt()
            return expression_stmnt()
        
        
        # module: flag_parser* EOF;
        def module():
            self.enter(ContextType.GLOBAL)
            _nodes = []
            
            while not self.cstoken.matches(TokenType.ENDOFFILE):
                _nodes.append(compound_stmnt())
            
            self.eat(TokenType.ENDOFFILE)

            self.leave()
            
            # return as module
            return ModuleNode(tuple(_nodes))

        return module()
