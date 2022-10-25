from sys import stderr, exit

def show_error(_message, _token):
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
    _header = f"[{_token.fsrce}:{_token.xS}:{_token.yS}] {_message}"
    
    print(_header + '\n' + _token.trace, file=stderr)
    exit(0x01)