""" CSObject type prototype
"""


from . import PyLinkInterface, CSTypes


class CSObjectLink(PyLinkInterface):
    
    def __init__(self, _enherit=None):
        super().__init__(_enherit)
        self.linkname = CSTypes.TYPE_CSOBJECT
        self.metadata = ({})





