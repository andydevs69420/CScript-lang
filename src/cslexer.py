
from cstoken import TokenType, CSToken
from errortoken import show_error
from strongtyping.strong_typing import match_typing

class LexUtils(object):
    """ Lexer utilities
    """

    def is_ignore_char(self):
        """ Checks if ignorable character

            Returns
            -------
            bool
        """
        ch = ord(self.clook)
        return (
            (ch == 0x00) or
            (ch == 0x08) or
            (ch == 0x09) or
            (ch == 0x0a) or
            (ch == 0x0d) or
            (ch == 0x20)
        )

    def is_identifier(self):
        """ Checks if identifier

            Returns
            -------
            bool
        """
        ch = ord(self.clook)
        return (
            (ch >= 0x61 and ch <= 0x7a) or
            (ch >= 0x41 and ch <= 0x5a) or
            (ch == 0x5f) or
            self.clook.isidentifier()
        )
    

    def is_digit(self):
        """ Checks for digit [0-9]

            Returns
            -------
            bool
        """
        ch = ord(self.clook)
        return (ch >= 0x30 and ch <= 0x39)
    
    def is_hex_part(self):
        """ Checks if hex part [a-fA-F0-9]+

            Returns
            -------
            bool
        """
        ch = ord(self.clook)
        return (
            (ch >= 0x61 and ch <= 0x66) or
            (ch >= 0x41 and ch <= 0x46) or
            self.is_digit()
        )

    def is_oct_part(self):
        """ Checks if oct part [0-7]+

            Returns
            -------
            bool
        """
        ch = ord(self.clook)
        return (ch >= 0x30 and ch <= 0x37)

    def is_bin_part(self):
        """ Checks if bin part [0-1]+

            Returns
            -------
            bool
        """
        ch = ord(self.clook)
        return (ch == 0x30 or ch == 0x31)
    
    def is_str_part(self):
        """ Checks if str part '"'

            Returns
            -------
            bool
        """
        return (ord(self.clook) == 0x22)

    def is_eof(self):
        """ Checks cursor is equal or greaterthan code length

            Returns
            -------
            bool
        """
        return self.cpntr >= len(self.scode)



class TokenBuilder(LexUtils):
    """ Builds token
    """

    ESCAPES = ({
        "b" : "\b",
        "n" : "\n",
        "t" : "\t",
        "r" : "\r",
        "\"": "\"",
        "\'": "\'"
    })

    def ignore_char(self):
        """ Ignores character

            Returns
            -------
            None
        """
        while not self.is_eof() and self.is_ignore_char():
            self.forward()

    def next_identifier(self):
        """ Builds identifier token

            Returns
            -------
            CSToken
        """
        assert self.is_identifier(), "invalid identifier context"

        _builder = CSToken()
        _builder.update(self)

        # update for id start
        _builder.concat(self.identifier_start())
        _builder.update(self)

        if not self.is_digit(): return _builder

        # update digit follow
        _builder.concat(self.digit_start())
        _builder.update(self)
        
        return _builder
    
    def identifier_start(self):
        """ Builds identifier string [_a-zA-Z]+

            Returns
            -------
            str
        """
        assert self.is_identifier(), "invalid identifier context"

        _raw_start = ""
        
        while not self.is_eof() and self.is_identifier():
            _raw_start += self.clook
            self.forward()
        
        return _raw_start
    
    def next_number(self):
        """ Builds number 

            Returns
            -------
            CSToken
        """
        assert self.is_digit(), "invalid digit context"

        _builder = CSToken()
        _builder.update(self)

        _part = ""
        _part += self.digit_start()

        if  _part == "0":
            _cstate = self.snapshot()
            _clookc = str(self.clook)
            _follow = ""
            _buildF = (lambda: '')
            
            if _clookc.lower() in ('x', 'o', 'b'):
                # set known
                _builder.setType(TokenType.INTEGER)
                # append
                _follow += _clookc
                self.forward()

            match _clookc.lower():
                case 'x':
                    # builder function
                    _buildF = self.hex_part
                case 'o':
                    # builder function
                    _buildF = self.oct_part
                case 'b':
                    # builder function
                    _buildF = self.bin_part

            _follow += _buildF()
            
            if  len(_follow) > 1:
                # concat|update
                _builder.concat(str(eval(_part + _follow)))
                _builder.update(self)
                return _builder

            # restore
            self.restore(_cstate)
            del _cstate

        # continue normal number
        _cstate = self.snapshot()

        # update token type
        _builder.setType(TokenType.INTEGER)

        _clookc = self.clook.lower()

        if  _clookc == '.':
            # update first
            _builder.setType(TokenType.DOUBLE)
            # next
            self.forward()

            if  not self.is_digit():
                self.restore(_cstate)
            else:
                _part += _clookc + self.digit_start()

        if  _clookc == 'e':
            # update first
            _builder.setType(TokenType.DOUBLE)
            # next
            self.forward()

            if  not self.is_digit():
                self.restore(_cstate)
            else:
                _part += _clookc + self.digit_start()
        
        _builder.concat(_part)
        _builder.update(self )

        return _builder
    
    def digit_start(self):
        """ Builds digit start [0-9]+

            Returns
            -------
            str
        """
        assert self.is_digit(), "invalid digit context"

        _raw_start = ""
        
        while not self.is_eof() and self.is_digit():
            _raw_start += self.clook
            self.forward()
        
        return _raw_start
    
    def hex_part(self, _assert:bool=False):
        """ Builds hex part [a-zA-Z0-9]+

            Returns
            -------
            str
        """
        # optional assert!
        if  _assert:\
        assert self.is_hex_part(), "invalid hex context"

        _raw_part= ""
        
        while not self.is_eof() and self.is_hex_part():
            _raw_part += self.clook
            self.forward()
        
        return _raw_part

    def oct_part(self, _assert:bool=False):
        """ Builds oct part [0-7]+

            Returns
            -------
            str
        """
        # optional assert!
        if  _assert:\
        assert self.is_oct_part(), "invalid hex context"

        _raw_part= ""
        
        while not self.is_eof() and self.is_oct_part():
            _raw_part += self.clook
            self.forward()
        
        return _raw_part
    
    def bin_part(self, _assert:bool=False):
        """ Builds bin part [0-1]+

            Returns
            -------
            str
        """
        # optional assert!
        if  _assert:\
        assert self.is_bin_part(), "invalid bin context"

        _raw_part= ""
        
        while not self.is_eof() and self.is_bin_part():
            _raw_part += self.clook
            self.forward()
        
        return _raw_part
    
    def next_str(self):
        """ Builds string ".*"

            Returns
            -------
            str
        """
        assert self.is_str_part(), "invalid string context"

        _builder = CSToken(TokenType.STRING)
        _builder.update(self)

        _isOpen, _isClose = self.is_str_part(), False
        _sChunk = ""

        # forward next
        self.forward()

        _isClose = self.is_str_part()

        while not self.is_eof() and (_isOpen and not _isClose):
            
            if  self.clook == '\n':break

            if  ord(self.clook) == 0x5c:
                _bslash = self.clook

                if  self.clook in self.ESCAPES.keys():
                    _sChunk += self.ESCAPES[self.clook]
                else:
                    _sChunk += f"{_bslash}{self.clook}"

            else:
                _sChunk += self.clook
            
            self.forward()
            _isClose = self.is_str_part()
        
        # forward
        if  _isOpen and _isClose:
            self.forward()
        
        # error if not closed
        if  not _isClose:
            _builder.update(self)
            return show_error(self, "string is not properly closed", _builder)

        # update builder
        _builder.concat(_sChunk)
        _builder.update( self  )
        return _builder
    
    def next_operator(self):
        """ Builds operator

            Returns
            -------
            CSToken
        """
        _builder = CSToken(TokenType.OPERATOR)
        _builder.update(self)

        _part = ""

        def append():
            # save and forward
            _x = self.clook
            self.forward()
            # return
            return _x

        if  self.clook == '[' or \
            self.clook == ']' or \
            self.clook == '{' or \
            self.clook == '}' or \
            self.clook == '(' or \
            self.clook == ')':
            _part += append()

        elif self.clook == '*' or \
             self.clook == '/' or \
             self.clook == '%':
            _part += append()

            if self.clook == '=':
                _part += append()
            
        elif self.clook == '+':
            _part += append()

            if  self.clook == '+' or \
                self.clook == '=':
                _part += append()
        
        elif self.clook == '-':
            _part += append()

            if  self.clook == '-' or \
                self.clook == '>' or \
                self.clook == '=':
                _part += append()

        elif self.clook == '<':
            _part += append()

            if self.clook == '<':
                _part += append()

                if self.clook == '=':
                    _part += append()

            elif self.clook == '=':
                _part += append()
        
        elif self.clook == '>':
            _part += append()

            if  self.clook == '>':
                _part += append()

                if self.clook == '=':
                    _part += append()
                    
            elif self.clook == '=':
                _part += append()
        
        elif self.clook == '=':
            _part += append()

            if self.clook == '=':
                _part += append()
        
        elif self.clook == '!':
            _part += append()

            if self.clook == '=':
                _part += append()
        
        elif self.clook == '&':
            _part += append()

            if  self.clook == '&' or \
                self.clook == '=':
                _part += append()
        
        elif self.clook == '|':
            _part += append()

            if  self.clook == '|' or \
                self.clook == '=':
                _part += append()
        
        elif self.clook == '^':
            _part += append()

            if  self.clook == '^' or \
                self.clook == '=':
                _part += append()

        elif self.clook == ',' or \
             self.clook == ';':
            _part += append()
        
        elif self.clook == ':':
            _part += append()

            if self.clook == ':':
                _part += append()
        
        if  len(_part) <= 0:
            _builder.concat(self.error_part())
            _builder.update(self)
            # error
            return show_error(self, "unknown token", _builder)

        _builder.concat(_part)
        _builder.update(self)
        return _builder

    def error_part(self):
        """ Builds unknow token

            Returns
            -------
            str
        """

        _raw_error = ""

        while not self.is_eof() and not (
            self.is_ignore_char() or
            self.is_identifier()  or
            self.is_digit()       or
            self.is_str_part()
        ):
            _raw_error += self.clook
            self.forward()
        
        return _raw_error
    
    def emmit_eof(self):
        """ Builds eof token

            Returns
            -------
            CSToken
        """
        _builder = CSToken(TokenType.ENDOFFILE)
        _builder.concat("eof")
        _builder.update(self)
        return _builder


class CSLexer(TokenBuilder):
    """ Lexical analyzer for CScript
    """
    
    @match_typing
    def __init__(self, _source:str="<stdin>", _code:str=""):
        self.fpath = _source
        self.scode = _code
        self.cpntr = 0
        self.xAxis = 1
        self.yAxis = 1
        self.clook = self.scode[0]\
            if len(self.scode) > 0\
            else '\0'
    
    def forward(self):
        """ Forwards cursor

            Returns
            -------
            None      
        """
        if ord(self.clook) != 0x0a:
            self.xAxis += 1
        else:
            self.xAxis  = 1
            self.yAxis += 1
        
        self.cpntr += 1
        if not self.is_eof():
            self.clook = self.scode[self.cpntr]
        else:
            self.clook = '\0'
    
    def getNext(self):
        """ Gets next token

            Returns
            -------
            CSToken
        """
        while not self.is_eof():
            
            if self.is_ignore_char():
                self.ignore_char()
            elif self.is_identifier():
                return self.next_identifier()
            elif self.is_digit():
                return self.next_number()
            elif self.is_str_part():
                return self.next_str()
            else: 
                return self.next_operator()
        
        return self.emmit_eof()
    
    def snapshot(self):
        """ Takes snapshot from lex state

            Returns
            -------
            dict
        """
        return ({
            "cpntr": self.cpntr,
            "xAxis": self.xAxis,
            "yAxis": self.yAxis,
            "clook": self.clook
        })
    
    def restore(self, snapshot:dict):
        """ Restores snapshot

            Parameters
            ----------
                snapshot : dict
            Returns
            -------
            None
        """
        self.cpntr = snapshot["cpntr"]
        self.xAxis = snapshot["xAxis"]
        self.yAxis = snapshot["yAxis"]
        self.clook = snapshot["clook"]

