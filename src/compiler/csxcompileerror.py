from sys import exit, stderr
from colorama import Fore


class CSXCompileError:

    @staticmethod
    def csx_Error(_message:str):
        from colorama import Fore
        stderr.write(f"{Fore.RED}{_message}{Fore.RESET}\n")
        exit(0x01)

