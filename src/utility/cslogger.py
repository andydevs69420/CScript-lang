from colorama import Fore


def logger(_id, _message:str):
    """ log info

        Parameters
        ----------
        _id : Any
        _message : _any
    """
    print(f"{Fore.YELLOW}{_id}: {_message}{Fore.RESET}")
