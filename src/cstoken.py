
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
    ENDOFFILE  = 0x05



class CSToken(object):
    """ Token handler for CScript
    """

    @match_typing
    def __init__(self, _ttype:TokenType=TokenType.IDENTIFIER):
        self.ttype = _ttype
        self.token = ""
        self.xS    = ...
        self.xE    = ...
        self.yS    = ...
        self.yE    = ...
    
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
        return f"{type(self).__name__}(type={self.ttype.name}|token='{self.token}'|col=[{self.xS}:{self.xE}]|line=[{self.yS}:{self.yE}]);"

    