from sys import stderr, exit
from strongtyping.strong_typing import match_typing

@match_typing
def show_error(_process, _message, _token):
    """ Shows error and exit

        Parameters
        ----------
        _process : Lexer|Parser
        _message : str
        _token   : CSToken

        Returns
        -------
        None
    """
    _header = f"[{_process.fpath}:{_token.xS}:{_token.yS}] {_message}"
    _format = ""
    
    _padding = 4
    _lines   = _process.scode.split('\n')
    
    _beginLine = _token.yS - _padding\
        if  _token.yS - _padding > 0 \
        else 0
    _endedLine = _token.yE + _padding\
        if  _token.yE + _padding < len(_lines) - 1 \
        else len(_lines) - 1
    
    _lines = _lines[_beginLine:_endedLine]
   
    for idx in range(1, len(_lines)):
        _lineno  = str(_beginLine + idx)
        _lineno  = ((len(str(_endedLine)) - len(_lineno)) * ' ') + _lineno
        _format += _lineno + " | "

        if  ((_beginLine + idx) >= _token.yS and (_beginLine + idx) <= _token.yE) and _token.yS != _token.yE:
            _format += " ~ "

        _format += _lines[idx-1]

        if  idx < (len(_lines)):
            _format += '\n'

        if  (_beginLine + idx) == _token.yS and _token.yS == _token.yE:
            _squiggle = (len(_lineno) + 3) * ' '

            for _ in range(len(_lines[idx-1])):
                if  (_+1) >= _token.xS and (_+1) < _token.xE:
                    _squiggle += "^"
                else:
                    _squiggle += " "
            _format += _squiggle + '\n'

    print(_header + '\n' + _format, file=stderr)
    exit(0x01)