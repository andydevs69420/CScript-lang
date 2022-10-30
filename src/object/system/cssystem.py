


from base.csobject import CSObject
from system.csio import CSIO
from .csmodulesmap import CSModulesMap
from .cspath import CSPath

class CSSystem(CSObject):pass
class CSSystem(CSObject):

    SYSTEM= CSObject.new_module()

    # append PATH #
    SYSTEM.put("path", CSPath()) # csarray
    SYSTEM.get("path")\
        .push(CSObject.new_string("."))
    SYSTEM.get("path")\
        .push(CSObject.new_string("tests"))
    SYSTEM.get("path")\
        .push(CSObject.new_string("lib"))



    # append MODULE #
    SYSTEM.put("modules", CSModulesMap())  # csmap

    # append CSIO #
    SYSTEM.put("stdio", CSIO())  # csio



