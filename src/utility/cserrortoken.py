
# .
from .cshelpers import __throw__

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
    _header = f"[{_token.fsrce}] {_message}"
    
    return __throw__(_header + '\n' + _token.trace)