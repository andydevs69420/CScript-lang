from builtins import open, print

import sys
from sys import stderr, exit
from os import path as ospath

from object.system.cssystem import CSSystem

EXTENSION= ".csx"

def __read__(_file_path:str):
    try:
        _file= open(__resolve__(_file_path), "r")
        return _file.read()
    except IOError:
        return __throw__("CScriptError: file \"%s\" is not found!" % _file_path)
    

def __resolve__(_path:str):
    """ validate if its a valid path
    """
    if  ospath.isdir(_path):
        return __throw__("CScriptError: \"%s\" is not a file" % _path)

    if  not _path.endswith(EXTENSION):
        return __throw__("CScriptError: \"%s\" is not a valid cscript file" % __base__(_path))

    if  ospath.exists(_path): return _path

    # look in cscript sypath
    for each_path in CSSystem.SYSTEM.get("path").python():

        _default = ospath.join(each_path , _path   )
        _current = ospath.join(__path__(), _default)

        if  ospath.exists(ospath.normpath(_current)):
            return _current
        elif ospath.exists(ospath.normpath(_default)):
            return _default
    
    # CSSystem.SYSTEM.get("paths")
    return __throw__("CScriptError: invalid file \"%s\"" % _path)



def __path__():
    _file = ospath.basename(sys.executable)
    _base = sys.executable[:-len(ospath.join("/", _file))]
    return ospath.dirname(_base)

def __trim__(_file_path:str):
    """ Removes unneccessary file name and extension
    """
    _dir_name= ospath.dirname(_file_path)
    return _dir_name

def __base__(_file_path:str):
    """ Extracts base name from path
    """
    _base= ospath.basename(_file_path)
    return _base



def __throw__(_message:str):
    import colorama
    colorama.init()

    print(f"{colorama.Fore.RED}{_message}{colorama.Fore.RESET}", file=stderr)
    exit(0x01)

if  __name__ == "__main__":
    __path__()
