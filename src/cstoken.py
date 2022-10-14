
from enum import Enum
from unicodedata import normalize
from strongtyping.strong_typing import match_typing



class TokenType(Enum):
    """ CSToken types
    """

    IDENTIFIER = 0x00 
    INTEGER    = 0x01
    DOUBLE     = 0x02
    STRING     = 0x03
    OPERATOR   = 0x04
    DYNAMIC_OPERATOR = 0x05
    ENDOFFILE  = 0x06



class CSToken(object):
    """ Token handler for CScript
    """

    @match_typing
    def __init__(self, _ttype:TokenType=TokenType.IDENTIFIER):
        self.fsrce = ...
        self.ttype = _ttype
        self.token = ""
        self.xS    = ...
        self.xE    = ...
        self.yS    = ...
        self.yE    = ...
        self.trace = ...
    
    @match_typing
    def setType(self, _ttype:TokenType):
        """ Sets token type

            Parameters
            ----------
                chunk : TokenType 
            
            Returns
            -------
            None
        """
        self.ttype = _ttype

    @match_typing
    def concat(self, chunk:str):
        """ Concat chunk

            Returns
            -------
            str
        """
        self.token += chunk
        self.token  = normalize("NFKC", self.token)
        return self.token
    
    @match_typing
    def update(self, _lexer):
        """ Updates token position

            Parameters
            ---------
            _lexer : cslexer.CSLexer

            Returns
            -------
            None
        """
        if  self.xS == ... and self.xE == ...:
            self.xS = _lexer.xAxis
            self.xE = self.xS + len(self.token)
        
        else:
            self.xE = _lexer.xAxis

        if  self.yS == ... and self.yE == ...:
            self.yS = _lexer.yAxis
            self.yE = self.yS
        
        else:
            self.yE = _lexer.yAxis
        self.fsrce  = _lexer.fpath
        self.trace  = trace_location(self, _lexer)
    
    def toDict(self):
        """ Produces instance to dict

            Returns
            -------
            dict
        """
        return ({
            "ttype": self.ttype,
            "token": self.token,
        })
    
    @staticmethod
    @match_typing
    def fromDict(_cstokendict:dict):
        """ Converts dictionary to CSToken

            Parameters
            ----------
            _cstokendict : dict

            Returns
            -------
            CSToken
        """
        new = CSToken()
        new.ttype = _cstokendict["ttype"]
        new.token = _cstokendict["token"]
        new.xS    = _cstokendict[ "xS"  ]
        new.xE    = _cstokendict[ "xE"  ]
        new.yS    = _cstokendict[ "yS"  ]
        new.yE    = _cstokendict[ "yE"  ]
        return new
    
    @match_typing
    def matches(self, _match:TokenType|str):
        if  type(_match) == TokenType:
            return (self.ttype == _match)
        else:
            return (self.token == _match)

    def __str__(self):
        return f"'{self.token}'"

    

def trace_location(self:CSToken, _lexer):
    _lines = _lexer.scode.split("\n")
    _lpadd = 3

    _paddS = (self.yS - 1) - _lpadd \
        if   (self.yS - 1) - _lpadd >= 0 else 0
    
    _paddE = (self.yE + _lpadd) \
        if   (self.yE + _lpadd) <= len(_lines) else len(_lines)

    _lines = _lines[_paddS:_paddE]
    
    _fmt = ""
    _idx = 0

    for line in _lines:
        _num  = str(_paddS + (_idx + 1))
        _num  = ((len(str(_paddE)) - len(_num)) * " ") + _num
        _fmt += _num + " | " + line

        if  _idx < (len(_lines) - 1):
            _fmt += "\n"

        if  _paddS + (_idx + 1) == self.yS:
            if  not (_idx < (len(_lines) - 1)):
                _fmt += "\n"
            ####
            _fmt += ((len(_num) + 3) * " ")

            for idx in range(len(line)):
                if  (idx + 1) >= self.xS and (idx + 1) < self.xE:
                    _fmt += "^"
                else:
                    _fmt += " "

            if  _idx < (len(_lines) - 1):
                _fmt += "\n"

        _idx += 1
        
    return _fmt