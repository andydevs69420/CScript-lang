"""
    Parsing utils for CScript
    author: Philipp Andrew Roa Redondo
    github: http://github.com/andydevs69420/parser-utils

"""
from errortoken import show_error
from cslexer import TokenType, CSToken, Lexer
from strongtyping.strong_typing import match_typing


__all__ = [
    "BaseParser"  ,
    "Parsable"    ,
    "tidentifier" ,
    "tinteger"    ,
    "tdouble"     ,
    "tstring"     ,
    "teof"        ,
    "raw"         ,
    "sequence"    ,
    "zero_or_one" ,
    "zero_or_more",
    "one_or_more" ,
    "alternative" ,
]

class BaseParser(object):
    """ Base paser for CScript
    """

    @match_typing
    def __init__(self, _fpath:str, _scode:str):
        self.fpath:str = _fpath
        self.scode:str = _scode
        self.lexer:Lexer   = Lexer(self.fpath, self.scode)
        self.token:CSToken = self.lexer.getNext()

    @match_typing
    def eat(self, _token_or_symbol:TokenType|str):
        """ Eats token if matches, otherwise error

            Parameters
            ----------
            _token_or_symbol : TokenType|str

            Returns
            -------
            None
        """
        if  self.token.matches(_token_or_symbol):
            self.token = self.lexer.getNext()
            return
        
        # otherwise error
        _unpack = (
            self.token.token,
            _token_or_symbol 
            if type(_token_or_symbol) == str 
            else 
                _token_or_symbol.name
        )
        return self.onError("unexpected token '{0}'. Did you mean '{1}'?" % _unpack, self.token)


    def parse(self):
        """ Parser entry point

            Returns
            -------
            CSAst
        """
        raise NotImplementedError("parse method must be overriten!")
    
    @match_typing
    def onError(self, _message:str, _token:CSToken):
        """ Basic error handler for parser

            Calls show_error

            Returns
            -------
            None
        """
        return show_error(self, _message, _token)
    


class Parsable(object):
    """ Parsable base class interface
    """

    def __init__(self, _parser:BaseParser):
        self.parser:BaseParser = _parser

    def parse(self):
        """ Parse input from parser

            Returns
            -------
            CSToken|list[CSToken]|list[list[CSToken]]|None
        """
        raise NotImplementedError("parse method must be overriten!")
    
    def onParse(self, _result):return _result



class terminal(Parsable):
    """ Parse terminal token

        Parameters
        ----------
        _parser   : BaseParser
        _terminal : TokenType|str
    """

    @match_typing
    def __init__(self, _parser:BaseParser, _terminal:TokenType|str):
        super().__init__(_parser)
        assert type(self) != terminal, "terminal must be overriten!"

        self.terminal:TokenType|str = _terminal
    
    def parse(self):
        """ Parse terminal token callback

            Returns
            -------
            CSToken|None
        """
        if self.parser.token.matches(self.terminal):
            return self.parser.token
        
        return None


class tidentifier(terminal):
    """ Parse identifier terminal token

        Parameters
        ----------
        _parser   : BaseParser
        _terminal : TokenType|str
    """

    @match_typing
    def __init__(self, _parser:BaseParser):
        super().__init__(_parser, TokenType.IDENTIFIER)
        
    def parse(self):
        """ Parse identifier terminal token callback

            Returns
            -------
            CSToken|None
        """
        _node:CSToken = super().parse()
        if not _node: return _node
       
        # assert if identifier
        if  not _node.matches(TokenType.IDENTIFIER):
            return None

        # consume token
        self.parser.eat(TokenType.IDENTIFIER)

        return self.onParse(_node)


class tinteger(terminal):
    """ Parse integer terminal token

        Parameters
        ----------
        _parser   : BaseParser
        _terminal : TokenType|str
    """

    @match_typing
    def __init__(self, _parser:BaseParser):
        super().__init__(_parser, TokenType.INTEGER)
    
    def parse(self):
        """ Parse integer terminal token callback

            Returns
            -------
            CSToken|None
        """
        _node:CSToken = super().parse()
        if not _node: return _node
       
        # assert if integer
        if  not _node.matches(TokenType.INTEGER):
            return None

        # consume token
        self.parser.eat(TokenType.INTEGER)

        return self.onParse(_node)


class tdouble(terminal):
    """ Parse double terminal token

        Parameters
        ----------
        _parser   : BaseParser
        _terminal : TokenType|str
    """

    @match_typing
    def __init__(self, _parser:BaseParser):
        super().__init__(_parser, TokenType.DOUBLE)
    
    def parse(self):
        """ Parse double terminal token callback

            Returns
            -------
            CSToken|None
        """
        _node:CSToken = super().parse()
        if not _node: return _node
       
        # assert if double
        if  not _node.matches(TokenType.DOUBLE):
            return None

        # consume token
        self.parser.eat(TokenType.DOUBLE)

        return self.onParse(_node)


class tstring(terminal):
    """ Parse string terminal token

        Parameters
        ----------
        _parser   : BaseParser
        _terminal : TokenType|str
    """

    @match_typing
    def __init__(self, _parser:BaseParser):
        super().__init__(_parser, TokenType.STRING)
    
    def parse(self):
        """ Parse string terminal token callback

            Returns
            -------
            CSToken|None
        """
        _node:CSToken = super().parse()
        if not _node: return _node
       
        # assert if string
        if  not _node.matches(TokenType.STRING):
            return None

        # consume token
        self.parser.eat(TokenType.STRING)

        return self.onParse(_node)

class teof(terminal):
    """ Parse eof terminal token

        Parameters
        ----------
        _parser   : BaseParser
        _terminal : TokenType|str
    """

    @match_typing
    def __init__(self, _parser:BaseParser):
        super().__init__(_parser, TokenType.ENDOFFILE)
    
    def parse(self):
        """ Parse eof terminal token callback

            Returns
            -------
            CSToken|None
        """
        _node:CSToken = super().parse()
        if not _node: return _node
       
        # assert if eof
        if  not _node.matches(TokenType.ENDOFFILE):
            return None

        # consume token
        self.parser.eat(TokenType.ENDOFFILE)

        return self.onParse(_node)

class raw(Parsable):
    """ Parse if match

        Parameters
        ----------
        _raw : str
    """
    
    @match_typing
    def __init__(self, _parser:BaseParser, _raw:str):
        super().__init__(_parser)
        self.raw:str = _raw
    
    def parse(self):
        """ Parse if match callback

            Parameters
            ----------
            _raw : str
        """
        _node = self.parser.token

        # assert if match
        if  not _node.matches(self.raw):
            return None

        # consume token
        self.parser.eat(_node.ttype)
       
        return self.onParse(_node)


class sequence(Parsable):
    """ Builds sequence

        Parameters
        ----------
        _parser   : BaseParser
        _sequence : list[Parsable]
    """

    def __init__(self, _parser:BaseParser, *_sequence:Parsable):
        super().__init__(_parser)
        assert len(_sequence) >= 2, "invalid sequence!"
        self.sequence:list[Parsable] = _sequence
        
    def parse(self):
        """ Builds sequence

            Returns
            -------
            list[CSToken]|None
        """
        if len(self.sequence) <= 0: return None

        _sequence = []
        
        _1st = self.sequence[0].parse()
        if not _1st: return _1st

        _sequence.append(_1st)
        
        for seq in self.sequence[1:]:
            
            _2nd_above = seq.parse()
            
            if not _2nd_above:\
            return self.parser.onError(
                "unexpected from sequence '{0}'".format(self.parser.token.token), 
                self.parser.token
            )
            
            # continue
            _sequence.append(_2nd_above)

        return self.onParse(tuple(_sequence))
        


class zero_or_one(Parsable):
    """ Parse zero or one of a target

        Parameters
        ----------
        _zero_or_one_of : Parsable
    """
    
    @match_typing
    def __init__(self, _parser:BaseParser, _zero_or_one_of:Parsable):
        super().__init__(_parser)
        self.zero_or_one_of:Parsable = _zero_or_one_of
    
    def parse(self):
        """ Parse zero or one of a target callback

            Returns
            -------
            CSToken|None
        """
        return self.onParse(self.zero_or_one_of.parse())



class zero_or_more(Parsable):
    """ Parse zero or more of a target

        Parameters
        ----------
        _zero_or_more_of : Parsable
    """

    @match_typing
    def __init__(self, _parser:BaseParser, _zero_or_more_of:Parsable):
        super().__init__(_parser)
        self.zero_or_more_of:Parsable = _zero_or_more_of
    
    def parse(self):
        """ Parse zero or more of a target callback

            Returns
            -------
            list[list[CSToken]]|CSToken
        """
        _zero_or_more_item = []

        # first item
        _element = self.zero_or_more_of.parse()

        while _element:
            # append
            _zero_or_more_item.append(_element)
            
            # next item
            _element = self.zero_or_more_of.parse()
        
        return self.onParse(tuple(_zero_or_more_item))


class one_or_more(Parsable):

    def __init__(self, _parser: BaseParser, _one_or_more_of:Parsable):
        super().__init__(_parser)
        self.one_or_more_of:Parsable = _one_or_more_of

    def parse(self):
        _lst = []

        _1st = self.one_or_more_of.parse()
        if not _1st:\
        return self.parser.onError(
            "expected one or more value '{0}'".format(self.parser.token.token), 
            self.parser.token
        )

        _lst.append(_1st)

        _nxt = self.one_or_more_of.parse()

        while _nxt:
            _lst.append(_nxt)
            _nxt = self.one_or_more_of.parse()
        
        return self.onParse(tuple(_lst))
    

class alternative(Parsable):
    """ Selects an alternative

        Parameters
        ----------
        _parser       : BaseParser
        _alternatives : list[Parsable]
    """

    @match_typing
    def __init__(self, _parser:BaseParser, *_alternative:Parsable):
        super().__init__(_parser)
        self.alternatives:list[Parsable] = _alternative
    
    def parse(self):
        """ Selects an alternative callback

            Returns
            -------
            CSToken|list[CSToken]|None
        """
        for alternate in self.alternatives:
            evaluate = alternate.parse()
            if evaluate: return evaluate
        
        return None
