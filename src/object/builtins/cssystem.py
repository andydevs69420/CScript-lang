


from base.csobject import CSObject
from .csmodulesmap import CSModulesMap
from .cspath import CSPath


class CSSystem(CSObject):

    SYSTEM= CSObject.new_module()
    # append PATH #
    SYSTEM.put("path", CSPath())
    SYSTEM.get("path")\
        .push(CSObject.new_string("tests"))
    SYSTEM.get("path")\
        .push(CSObject.new_string("lib"))
    # append PATH #
    SYSTEM.put("modules", CSModulesMap())

